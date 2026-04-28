// =============================================================================
// cloud/cf_worker_polar.ts — K3 Polar.sh webhook handler na Cloudflare Workers
// =============================================================================
// Polar.sh je Merchant of Record (MoR) — automatski rjesava EU PDV za sve
// jurisdikcije bez registracije po zemlji. Stoga je BOLJE od Stripe Tax-a za
// jednog dev-a koji prodaje SaaS u EU.
//
// Deploy:
//   npm install -g wrangler
//   wrangler login
//   wrangler init lts-polar-webhook (kopiraj ovaj file kao src/index.ts)
//   wrangler secret put POLAR_ACCESS_TOKEN          # polar_oat_xxx (Personal Access Token)
//   wrangler secret put POLAR_WEBHOOK_SECRET        # whsec_xxx (Polar Dashboard webhook config)
//   wrangler secret put POLAR_PRODUCT_ID_PRO        # uuid Polar Product/Price-a
//   wrangler secret put POLAR_ORG_ID                # uuid organizacije (opcionalno; za Polar JS SDK)
//   wrangler secret put SUPABASE_URL                # https://xxx.supabase.co
//   wrangler secret put SUPABASE_SERVICE_ROLE_KEY   # JWT s 'service_role' (bypass RLS)
//   wrangler secret put APP_RETURN_URL              # https://your-app.streamlit.app
//   wrangler deploy                                  # daje URL https://lts-polar-webhook.<sub>.workers.dev
//
// Onda u Polar Dashboard → Settings → Webhooks dodaj endpoint:
//   URL: https://lts-polar-webhook.<sub>.workers.dev/webhook
//   Events: order.created, order.refunded, subscription.created,
//           subscription.active, subscription.updated, subscription.canceled,
//           subscription.revoked, subscription.uncanceled
//
// Endpoints:
//   POST /webhook                  — Polar webhook (SVIX-style signature, idempotent)
//   POST /create-checkout-session  — od Streamlit-a, vraca checkout_url
//   GET  /health                   — JSON {ok:true} za UptimeRobot/Pingdom

interface Env {
    POLAR_ACCESS_TOKEN: string;
    POLAR_WEBHOOK_SECRET: string;
    POLAR_PRODUCT_ID_PRO: string;
    POLAR_ORG_ID?: string;
    SUPABASE_URL: string;
    SUPABASE_SERVICE_ROLE_KEY: string;
    APP_RETURN_URL: string;
}

const POLAR_API_BASE = "https://api.polar.sh/v1";

// =============================================================================
// Polar API helpers (raw fetch — bez SDK ovisnosti)
// =============================================================================

async function polarRequest<T = any>(env: Env, method: string, path: string, body?: object): Promise<T | null> {
    const r = await fetch(`${POLAR_API_BASE}${path}`, {
        method,
        headers: {
            "Authorization": `Bearer ${env.POLAR_ACCESS_TOKEN}`,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        body: body ? JSON.stringify(body) : undefined,
    });
    if (!r.ok) return null;
    return await r.json() as T;
}

// =============================================================================
// SVIX-style webhook signature verifikacija (Polar koristi Standard Webhooks)
// Spec: https://github.com/standard-webhooks/standard-webhooks
//   message_id  = webhook-id header
//   timestamp   = webhook-timestamp header (Unix seconds)
//   payload     = raw body string
//   signed_data = `${message_id}.${timestamp}.${payload}`
//   signatures  = webhook-signature header u formatu "v1,<base64-hmac-sha256>" (može više, space-separated)
// =============================================================================

async function verifyPolarSignature(
    secret: string,
    msgId: string,
    timestamp: string,
    rawBody: string,
    signatureHeader: string,
): Promise<boolean> {
    // Polar webhook secret format: "whsec_<base64>" — strip prefix
    const cleanSecret = secret.startsWith("whsec_") ? secret.substring(6) : secret;
    const secretBytes = Uint8Array.from(atob(cleanSecret), c => c.charCodeAt(0));

    const signedPayload = `${msgId}.${timestamp}.${rawBody}`;
    const enc = new TextEncoder();
    const key = await crypto.subtle.importKey(
        "raw",
        secretBytes,
        { name: "HMAC", hash: "SHA-256" },
        false,
        ["sign"],
    );
    const sig = await crypto.subtle.sign("HMAC", key, enc.encode(signedPayload));
    const expectedB64 = btoa(String.fromCharCode(...new Uint8Array(sig)));

    // signatureHeader može sadržavati više potpisa, space-separated, npr. "v1,abc v1,def"
    const sigs = signatureHeader.split(" ");
    for (const sigEntry of sigs) {
        const [version, value] = sigEntry.split(",");
        if (version === "v1" && timingSafeEqual(value, expectedB64)) {
            return true;
        }
    }
    return false;
}

function timingSafeEqual(a: string, b: string): boolean {
    if (a.length !== b.length) return false;
    let diff = 0;
    for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
    return diff === 0;
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
// Polar event types (subset — samo oni koji utjecu na entitlement)
// =============================================================================

interface PolarSubscriptionData {
    id: string;
    customer_id: string;
    status: "active" | "canceled" | "past_due" | "unpaid" | "incomplete" | "trialing" | "revoked";
    current_period_end?: string;  // ISO datetime
    metadata?: { user_id?: string; plan?: string };
    customer?: { external_id?: string; email?: string };
    product_id?: string;
}

interface PolarOrderData {
    id: string;
    customer_id: string;
    subscription_id?: string;
    status: "paid" | "refunded" | "partially_refunded";
    amount: number;
    currency: string;
    metadata?: { user_id?: string; plan?: string };
    customer?: { external_id?: string; email?: string };
    product_id?: string;
}

interface PolarEvent {
    type: string;
    data: PolarSubscriptionData | PolarOrderData | any;
}

// =============================================================================
// Webhook event processing (idempotent)
// =============================================================================

async function processPolarEvent(env: Env, eventId: string, event: PolarEvent): Promise<void> {
    // 1) Idempotency anchor: pokusaj INSERT u stripe_events (zadrzano ime tablice
    //    radi backward compat schemom; semanticki sad sluzi za sve payment gateway-e).
    const eventInsert = await supabaseUpsert(env, "stripe_events", {
        stripe_event_id: eventId,
        event_type: event.type,
        payload_json: event,
    });
    if (!eventInsert) {
        return;  // duplikat ili Supabase fail — konzervativno preskoci
    }

    // 2) Per-tip handler
    switch (event.type) {
        case "subscription.created":
        case "subscription.active":
        case "subscription.updated":
        case "subscription.uncanceled": {
            const sub = event.data as PolarSubscriptionData;
            const userId = sub.metadata?.user_id || sub.customer?.external_id;
            const plan = sub.metadata?.plan || "pro";
            if (!userId) break;

            const status = sub.status === "active" || sub.status === "trialing"
                ? "active"
                : sub.status === "past_due" ? "past_due" : "revoked";

            // Update user → polar_customer_id (zadrzano stripe_customer_id ime u schemi)
            if (sub.customer_id) {
                await supabaseUpsert(env, "users", {
                    id: userId,
                    stripe_customer_id: sub.customer_id,
                }, "id");
            }

            // UPSERT entitlement (stripe_subscription_id semanticki = payment_subscription_id)
            await supabaseUpsert(env, "entitlements", {
                user_id: userId,
                plan: plan,
                status: status,
                period_start: new Date().toISOString(),
                period_end: sub.current_period_end || null,
                stripe_subscription_id: sub.id,
            }, "user_id,plan");
            break;
        }

        case "order.created": {
            // One-time purchase ili prvi order subscription-a.
            // Za pay-per-doc bi se ovdje aktivirao kratki entitlement.
            const order = event.data as PolarOrderData;
            const userId = order.metadata?.user_id || order.customer?.external_id;
            const plan = order.metadata?.plan || "pro";
            if (!userId) break;

            // Ako je order vezan za subscription, subscription.* event handle-a entitlement.
            // Ako je standalone (pay-per-doc), zapisi short-lived entitlement.
            if (!order.subscription_id) {
                await supabaseUpsert(env, "entitlements", {
                    user_id: userId,
                    plan: plan,
                    status: "active",
                    period_start: new Date().toISOString(),
                    period_end: null,  // pay-per-doc: traje dok god UI ne provjeri (ili dodaj 24h TTL)
                    stripe_subscription_id: order.id,  // koristi order.id kao key
                }, "user_id,plan");
            }

            if (order.customer_id) {
                await supabaseUpsert(env, "users", {
                    id: userId,
                    stripe_customer_id: order.customer_id,
                }, "id");
            }
            break;
        }

        case "order.refunded": {
            // Refund punog ili djelomicnog iznosa → revoke vezano entitlement
            const order = event.data as PolarOrderData;
            const subId = order.subscription_id || order.id;
            await supabaseUpsert(env, "entitlements", {
                stripe_subscription_id: subId,
                status: "revoked",
            }, "stripe_subscription_id");
            break;
        }

        case "subscription.canceled":
        case "subscription.revoked": {
            const sub = event.data as PolarSubscriptionData;
            await supabaseUpsert(env, "entitlements", {
                stripe_subscription_id: sub.id,
                status: "revoked",
            }, "stripe_subscription_id");
            break;
        }

        // Ostali tipovi (customer.*, checkout.*) se logiraju ali nemaju side effect
    }

    // 3) Mark event kao processed
    await fetch(`${env.SUPABASE_URL}/rest/v1/stripe_events?stripe_event_id=eq.${eventId}`, {
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

        // ---- /health ---------------------------------------------------------
        if (url.pathname === "/health") {
            return new Response(JSON.stringify({ ok: true, ts: new Date().toISOString(), gateway: "polar" }), {
                headers: { "Content-Type": "application/json" },
            });
        }

        // ---- /webhook --------------------------------------------------------
        if (url.pathname === "/webhook" && request.method === "POST") {
            const msgId = request.headers.get("webhook-id");
            const timestamp = request.headers.get("webhook-timestamp");
            const sigHeader = request.headers.get("webhook-signature");
            if (!msgId || !timestamp || !sigHeader) {
                return new Response("missing webhook signature headers", { status: 400 });
            }

            const rawBody = await request.text();

            // Reject events older than 5 minutes (replay protection)
            const tsNum = parseInt(timestamp, 10);
            const now = Math.floor(Date.now() / 1000);
            if (Math.abs(now - tsNum) > 300) {
                return new Response("timestamp out of tolerance", { status: 400 });
            }

            const valid = await verifyPolarSignature(
                env.POLAR_WEBHOOK_SECRET,
                msgId,
                timestamp,
                rawBody,
                sigHeader,
            );
            if (!valid) {
                return new Response("signature verify failed", { status: 400 });
            }

            let event: PolarEvent;
            try {
                event = JSON.parse(rawBody);
            } catch (err: any) {
                return new Response(`invalid json: ${err.message}`, { status: 400 });
            }

            try {
                await processPolarEvent(env, msgId, event);
            } catch (err: any) {
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

            const users = await supabaseSelect(env, "users", { id: `eq.${body.user_id}`, limit: "1" });
            if (users.length === 0) return new Response("user not found", { status: 404 });

            // Polar Checkout API (POST /v1/checkouts/)
            // Polar je MoR — bez automatic_tax: Polar samostalno racuna PDV za sve EU jurisdikcije.
            const checkout = await polarRequest<any>(env, "POST", "/checkouts/", {
                product_id: env.POLAR_PRODUCT_ID_PRO,
                success_url: `${env.APP_RETURN_URL}?checkout=success&checkout_id={CHECKOUT_ID}`,
                customer_external_id: body.user_id,
                customer_email: users[0].email,
                metadata: { user_id: body.user_id, plan: body.plan || "pro" },
            });

            if (!checkout || !checkout.url) {
                return new Response(JSON.stringify({ error: "polar checkout creation failed" }), {
                    status: 502,
                    headers: { "Content-Type": "application/json" },
                });
            }

            return new Response(JSON.stringify({ checkout_url: checkout.url }), {
                headers: { "Content-Type": "application/json" },
            });
        }

        return new Response("not found", { status: 404 });
    },
};
