// =============================================================================
// cloud/cf_worker_stripe.ts — K3 Stripe webhook handler na Cloudflare Workers
// =============================================================================
// Deploy:
//   npm install -g wrangler
//   wrangler login
//   wrangler init lts-stripe-webhook (kopiraj ovaj file kao src/index.ts)
//   wrangler secret put STRIPE_API_KEY              # sk_test_xxx ili sk_live_xxx
//   wrangler secret put STRIPE_WEBHOOK_SECRET       # whsec_xxx (iz Stripe dashboard webhook config)
//   wrangler secret put STRIPE_PRICE_ID_PRO         # price_xxx (Stripe Product/Price)
//   wrangler secret put SUPABASE_URL                # https://xxx.supabase.co
//   wrangler secret put SUPABASE_SERVICE_ROLE_KEY   # JWT s 'service_role' (bypass RLS)
//   wrangler secret put APP_RETURN_URL              # https://your-app.streamlit.app
//   wrangler deploy                                  # daje URL https://lts-stripe-webhook.<sub>.workers.dev
//
// Onda u Stripe Dashboard → Webhooks dodaj endpoint:
//   URL: https://lts-stripe-webhook.<sub>.workers.dev/webhook
//   Events: checkout.session.completed, customer.subscription.updated,
//           customer.subscription.deleted, charge.refunded, charge.dispute.created
//
// Endpoints:
//   POST /webhook                  — Stripe webhook (signature verified, idempotent)
//   POST /create-checkout-session  — od Streamlit-a, vraca checkout_url
//   GET  /health                   — JSON {ok:true} za UptimeRobot/Pingdom

// @ts-ignore — types se dohvacaju iz @cloudflare/workers-types u dev env-u
import Stripe from "stripe";

interface Env {
    STRIPE_API_KEY: string;
    STRIPE_WEBHOOK_SECRET: string;
    STRIPE_PRICE_ID_PRO: string;
    SUPABASE_URL: string;
    SUPABASE_SERVICE_ROLE_KEY: string;
    APP_RETURN_URL: string;
}

// =============================================================================
// Supabase REST helpers (service_role bypass RLS)
// =============================================================================

async function supabaseUpsert(env: Env, table: string, payload: object, onConflict?: string): Promise<boolean> {
    const url = new URL(`${env.SUPABASE_URL}/rest/v1/${table}`);
    if (onConflict) url.searchParams.set("on_conflict", onConflict);
    const r = await fetch(url.toString(), {
        method: "POST",
        headers: {
            "apikey": env.SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": `Bearer ${env.SUPABASE_SERVICE_ROLE_KEY}`,
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=minimal",
        },
        body: JSON.stringify(payload),
    });
    return r.ok;
}

async function supabaseSelect(env: Env, table: string, params: Record<string, string>): Promise<any[]> {
    const url = new URL(`${env.SUPABASE_URL}/rest/v1/${table}`);
    for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
    const r = await fetch(url.toString(), {
        method: "GET",
        headers: {
            "apikey": env.SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": `Bearer ${env.SUPABASE_SERVICE_ROLE_KEY}`,
        },
    });
    if (!r.ok) return [];
    return await r.json();
}

// =============================================================================
// Webhook event processing (idempotent)
// =============================================================================

async function processStripeEvent(env: Env, event: Stripe.Event): Promise<void> {
    // 1) Idempotency anchor: pokusaj INSERT u stripe_events. Ako duplikat → return early.
    const eventInsert = await supabaseUpsert(env, "stripe_events", {
        stripe_event_id: event.id,
        event_type: event.type,
        payload_json: event,
    });
    if (!eventInsert) {
        // Vec postoji ili Supabase fail. Konzervativno: ne procesuiraj duplikat.
        return;
    }

    // 2) Per-tip handler
    switch (event.type) {
        case "checkout.session.completed": {
            const session = event.data.object as Stripe.Checkout.Session;
            const userId = session.metadata?.user_id;
            const plan = session.metadata?.plan || "pro";
            if (!userId) break;

            // Update user → stripe_customer_id
            if (session.customer) {
                await supabaseUpsert(env, "users", {
                    id: userId,
                    stripe_customer_id: session.customer,
                }, "id");
            }

            // UPSERT entitlement
            const periodEnd = session.subscription
                ? new Date(((session as any).current_period_end ?? 0) * 1000).toISOString()
                : null;
            await supabaseUpsert(env, "entitlements", {
                user_id: userId,
                plan: plan,
                status: "active",
                period_start: new Date().toISOString(),
                period_end: periodEnd,
                stripe_subscription_id: session.subscription || null,
            }, "user_id,plan");
            break;
        }
        case "customer.subscription.updated": {
            const sub = event.data.object as Stripe.Subscription;
            const status = sub.status === "active" || sub.status === "trialing"
                ? "active"
                : sub.status === "past_due" ? "past_due" : "revoked";
            await supabaseUpsert(env, "entitlements", {
                stripe_subscription_id: sub.id,
                status: status,
                period_end: new Date(((sub as any).current_period_end ?? 0) * 1000).toISOString(),
            }, "stripe_subscription_id");
            break;
        }
        case "customer.subscription.deleted":
        case "charge.refunded":
        case "charge.dispute.created": {
            // Revoke svih entitlements za ovog customer-a (mild — moze se profiniti per-sub)
            const subId = (event.data.object as any).id || (event.data.object as any).subscription;
            if (subId) {
                await supabaseUpsert(env, "entitlements", {
                    stripe_subscription_id: subId,
                    status: "revoked",
                }, "stripe_subscription_id");
            }
            break;
        }
        // Ostali tipovi se logiraju u stripe_events ali nemaju side effect
    }

    // 3) Mark event kao processed (idempotency anchor: drugi run vidi processed_at)
    await fetch(`${env.SUPABASE_URL}/rest/v1/stripe_events?stripe_event_id=eq.${event.id}`, {
        method: "PATCH",
        headers: {
            "apikey": env.SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": `Bearer ${env.SUPABASE_SERVICE_ROLE_KEY}`,
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
        body: JSON.stringify({ processed_at: new Date().toISOString() }),
    });
}

// =============================================================================
// HTTP handler
// =============================================================================

export default {
    async fetch(request: Request, env: Env): Promise<Response> {
        const url = new URL(request.url);
        const stripe = new Stripe(env.STRIPE_API_KEY, {
            apiVersion: "2024-11-20.acacia" as any,
            httpClient: Stripe.createFetchHttpClient(),
        });

        // ---- /health ---------------------------------------------------------
        if (url.pathname === "/health") {
            return new Response(JSON.stringify({ ok: true, ts: new Date().toISOString() }), {
                headers: { "Content-Type": "application/json" },
            });
        }

        // ---- /webhook --------------------------------------------------------
        if (url.pathname === "/webhook" && request.method === "POST") {
            const sig = request.headers.get("stripe-signature");
            if (!sig) return new Response("missing signature", { status: 400 });

            const rawBody = await request.text();
            let event: Stripe.Event;
            try {
                event = await stripe.webhooks.constructEventAsync(
                    rawBody,
                    sig,
                    env.STRIPE_WEBHOOK_SECRET,
                );
            } catch (err: any) {
                return new Response(`signature verify failed: ${err.message}`, { status: 400 });
            }

            // Vrati 200 BRZO (Stripe SLA <5s); procesuiraj background-style
            // (CF Workers nema setTimeout pa sinkrono; <5s je OK za <10 DB pinga)
            try {
                await processStripeEvent(env, event);
            } catch (err: any) {
                // Stripe ce automatski retry-at ako vratimo 5xx
                return new Response(`process failed: ${err.message}`, { status: 500 });
            }
            return new Response(JSON.stringify({ received: true }), {
                headers: { "Content-Type": "application/json" },
            });
        }

        // ---- /create-checkout-session ---------------------------------------
        if (url.pathname === "/create-checkout-session" && request.method === "POST") {
            const body = await request.json() as { user_id: string; plan?: string };
            if (!body.user_id) {
                return new Response("missing user_id", { status: 400 });
            }

            // Lookup ili kreiraj Stripe customer
            const users = await supabaseSelect(env, "users", { id: `eq.${body.user_id}`, limit: "1" });
            if (users.length === 0) return new Response("user not found", { status: 404 });
            let customerId = users[0].stripe_customer_id;
            if (!customerId) {
                const cust = await stripe.customers.create({
                    email: users[0].email,
                    metadata: { user_id: body.user_id },
                });
                customerId = cust.id;
            }

            const session = await stripe.checkout.sessions.create({
                mode: "subscription",
                customer: customerId,
                line_items: [{ price: env.STRIPE_PRICE_ID_PRO, quantity: 1 }],
                metadata: { user_id: body.user_id, plan: body.plan || "pro" },
                success_url: `${env.APP_RETURN_URL}?checkout=success`,
                cancel_url: `${env.APP_RETURN_URL}?checkout=cancel`,
                automatic_tax: { enabled: true },  // Stripe Tax za HR PDV
            });

            return new Response(JSON.stringify({ checkout_url: session.url }), {
                headers: { "Content-Type": "application/json" },
            });
        }

        return new Response("not found", { status: 404 });
    },
};
