# K3 Cloud Setup — LegalTechSuite Pro

> **Cilj**: Postaviti cloud stack tako da app radi 24/7 **kad je PC isključen**.
> Sve komponente u free tier-u; total trošak ≤ 0 EUR/mj dok god si ispod limita.
>
> **Payment gateway**: **Polar.sh** (Merchant of Record). Polar automatski rješava EU PDV za sve jurisdikcije bez registracije po zemlji — bolje za jednog dev-a koji prodaje SaaS u EU od Stripe Tax + direct payments.
>
> **Vrijeme**: ~45 min (jednokratno).

---

## Pregled stack-a

```
[Korisnik browser]
      │
      ▼
[Streamlit Community Cloud]  (postojeci, https://{{STREAMLIT_APP_ID}}.streamlit.app)
      │  cita entitlement pri svakom download-u
      ▼
[Supabase Postgres]  ◄────  upsert iz CF Worker-a (preko service_role)
      ▲
      │  sve REST pozivi
      │
[Cloudflare Worker]  (https://lts-polar-webhook.<sub>.workers.dev)
      ▲
      │  Polar webhook (SVIX-style signed)
[Polar.sh]  (Hosted Checkout + Subscription, MoR)
```

---

## 1. Supabase setup (~10 min)

1. Idi na **https://supabase.com** → Sign up (preporučeno: GitHub auth)
2. Klikni **New project**:
   - Name: `legalsuite-pro`
   - DB password: generiraj jak (spremi u password manager)
   - Region: `Frankfurt (eu-central-1)` (najbliži HR)
3. Pricing: **Free** (500 MB DB, 50k MAU)
4. Pričekaj ~2 min da se projekt provisiona

5. **Učitaj schema**:
   - Lijevi menu → **SQL Editor** → **New query**
   - Paste sadržaj `cloud/supabase_schema.sql`
   - **Run** (bottom-right)
   - Provjera: Lijevi menu → **Database → Tables** → trebao bi vidjeti 4 tablice (`users`, `entitlements`, `download_log`, `stripe_events`)

   > **Note**: Tablica i kolone još uvijek nose `stripe_*` imena (`stripe_event_id`, `stripe_subscription_id`, `stripe_customer_id`). To je legacy iz Stripe MVP-a — schema je payment-gateway-neutralna i Polar event ID-jevi i subscription/customer ID-jevi normalno se upisuju u te kolone. Cosmetic rename (`payment_*`) može se napraviti naknadno migration-om.

6. **Dohvati credentials**:
   - **Settings → API**
   - Spremi (potrebno kasnije):
     - `Project URL` → bit će `SUPABASE_URL`
     - `anon public` key → bit će `SUPABASE_ANON_KEY` (za Streamlit klijent, RLS-zaštićen)
     - `service_role` secret key → bit će `SUPABASE_SERVICE_ROLE_KEY` (za CF Worker, **NIKAD u Streamlit secrets!**)

---

## 2. Polar.sh setup (~10 min)

1. Idi na **https://polar.sh** → **Sign in** (GitHub auth preporučeno)
2. **Create organization**:
   - Name: `LegalTechSuite Pro` (ili tvoja j.d.o.o. tvrtka)
   - Slug: `legaltechsuite` (bit će u URL-u checkout-a)
3. **Sandbox mode** (toggle u dashboardu) — radi sve test prije nego ideš live

4. **Products → Create new product**:
   - Name: `LegalTechSuite PRO`
   - Type: **Subscription** (Recurring) — ili dodaj posebne **One-time** produkte za pay-per-doc
   - Pricing: `9,99 EUR / month`
   - Save → kopiraj **Product ID** (UUID format) → bit će `POLAR_PRODUCT_ID_PRO`

5. **Settings → Developer → Personal Access Tokens** → **Create token**:
   - Name: `lts-cloudflare-worker`
   - Scope: `checkouts:write`, `subscriptions:read`, `orders:read`, `customers:read`
   - Spremi token (`polar_oat_xxx`) → bit će `POLAR_ACCESS_TOKEN`

6. **Webhook setup** (radit ćeš ovo NAKON CF Worker deploya u koraku 3):
   - **Settings → Webhooks → Add endpoint**
   - URL: `https://lts-polar-webhook.<sub>.workers.dev/webhook` (popuniš nakon koraka 3)
   - Format: **Standard Webhooks (SVIX-compatible)** — Polar koristi ovaj format po defaultu
   - Events to send (klikni "Select events"):
     - `order.created`
     - `order.refunded`
     - `subscription.created`
     - `subscription.active`
     - `subscription.updated`
     - `subscription.canceled`
     - `subscription.revoked`
     - `subscription.uncanceled`
   - Save → kopiraj **Signing secret** (`whsec_xxx`) → bit će `POLAR_WEBHOOK_SECRET`

7. **EU PDV (Polar to rješava)**:
   - Polar je MoR — automatski računa i prijavljuje EU PDV za sve države. Ne trebaš ništa konfigurirati za HR PDV ili reverse charge — Polar to radi za tebe.
   - **Settings → Tax** → potvrdi da je "Polar handles tax remittance" uključeno (default).

---

## 3. Cloudflare Worker deploy (~15 min)

1. Idi na **https://dash.cloudflare.com** → Sign up
2. Lokalno na svom računalu (jednom):

   ```bash
   npm install -g wrangler
   wrangler login   # otvori browser, autoriziraj
   ```

3. **Pripremi worker direktorij**:

   ```bash
   cd "C:/Users/{{WIN_USER}}/Documents/APLIKACIJA/cloud"
   npm install                # dohvati cloudflare-types
   ```

   Provjeri da je u `wrangler.toml` `main = "cf_worker_polar.ts"` (ili da je tvoj entry point). Ako ne — promijeni:

   ```toml
   name = "lts-polar-webhook"
   main = "cf_worker_polar.ts"
   compatibility_date = "2026-01-01"
   ```

4. **Deploy**:

   ```bash
   wrangler deploy            # daje URL: https://lts-polar-webhook.<sub>.workers.dev
   ```

   Spremi taj URL.

5. **Postavi secrets** (svaki je odvojena `wrangler secret put` komanda — wrangler će pitati vrijednost):

   ```bash
   wrangler secret put POLAR_ACCESS_TOKEN          # paste polar_oat_xxx
   wrangler secret put POLAR_WEBHOOK_SECRET        # paste whsec_xxx (iz Polar Webhook config)
   wrangler secret put POLAR_PRODUCT_ID_PRO        # paste UUID Product-a
   wrangler secret put SUPABASE_URL                # paste https://xxx.supabase.co
   wrangler secret put SUPABASE_SERVICE_ROLE_KEY   # paste service_role key (TAJNO!)
   wrangler secret put APP_RETURN_URL              # paste https://{{STREAMLIT_APP_ID}}.streamlit.app
   ```

6. **Re-deploy** da pokupi secrets:

   ```bash
   wrangler deploy
   ```

7. **Health check**:

   ```bash
   curl https://lts-polar-webhook.<sub>.workers.dev/health
   # ocekivan output: {"ok":true,"ts":"2026-04-28T...","gateway":"polar"}
   ```

8. **Vrati se u Polar Dashboard** (korak 2.6) i dovrši webhook setup s URL-om iz koraka 3.4.

---

## 4. Streamlit Cloud secrets (~5 min)

1. Idi na **https://share.streamlit.io** → tvoj `LEGAL-SUITE` app
2. Klikni `⋮` → **Settings → Secrets**
3. Dodaj (TOML format):

   ```toml
   SUPABASE_URL = "https://xxx.supabase.co"
   SUPABASE_ANON_KEY = "eyJh..."   # anon key, NE service_role!
   CHECKOUT_URL_BASE = "https://lts-polar-webhook.<sub>.workers.dev"
   ```

   > Backward-compat: ako i dalje koristiš stari secret `STRIPE_CHECKOUT_URL_BASE`, `entitlements.py` ga čita kao fallback. Ali za nove deployeve preferiraj `CHECKOUT_URL_BASE`.

4. **Save**. Streamlit će auto-restart-ati app (~30s).

---

## 5. End-to-end smoke test (~5 min)

1. **Otvori** `https://{{STREAMLIT_APP_ID}}.streamlit.app`
2. **Registriraj** test korisnika (email + lozinka kroz postojeći auth — migracija na Supabase auth je odvojen task)
3. Klikni **Pretplati se na PRO** → klikom otvori **Polar Checkout**
4. **Test kartica** (Polar Sandbox mode prihvaća standardne test brojeve):
   - Card: `4242 4242 4242 4242`
   - Datum: bilo koji budući
   - CVC: `123`
5. Završi checkout → Polar te vrati na app (`?checkout=success&checkout_id=...`)
6. Refresh stranice
7. Generiraj bilo koji dokument → docx footer treba imati `ID: NN-NNNN-NNNNNN` (bez "Generirano iz LegalTechSuite Pro" jer si PRO)
8. Provjeri u Supabase Dashboard → **Table Editor → entitlements** → trebao bi vidjeti red s `plan='pro'`, `status='active'`, te `stripe_subscription_id` popunjen Polar subscription UUID-em
9. Provjeri u Supabase **stripe_events** → trebao bi vidjeti red s `event_type='subscription.active'` (ili `order.created`) i `processed_at` popunjeno

---

## 6. Production switch (kad je sve sandbox OK)

1. Polar Dashboard → toggle **Production mode** (gore desno)
2. Ponovi korake 2.4-2.6 u Production mode-u (Product, Personal Access Token, Webhook signing secret)
3. `wrangler secret put` zamijeni sve secrets s production vrijednostima
4. Polar Dashboard → **Settings → Business** popuni HR poslovne podatke (OIB, adresa j.d.o.o., bankovni račun za payout)
5. **Settings → Tax** → ostaje "Polar handles tax remittance" (Polar šalje payout-e umanjene za PDV koji oni prijavljuju u svakoj jurisdikciji)

---

## Troubleshooting

### Webhook "signature verify failed"

`POLAR_WEBHOOK_SECRET` u CF Worker secret-u ne odgovara onom u Polar Dashboard webhook config-u. Provjeri:

```bash
wrangler secret list   # u cloud/ direktoriju
```

I regeneriraj webhook secret u Polar Dashboard ako treba. Polar koristi Standard Webhooks signature scheme (`webhook-id`, `webhook-timestamp`, `webhook-signature` headeri) — `cf_worker_polar.ts` to verificira preko HMAC-SHA256 nad `${msgId}.${timestamp}.${rawBody}`.

### Webhook "timestamp out of tolerance"

Worker odbacuje webhooke starije od 5 minuta (replay protection). Ako vidiš ovu grešku, sat na tvom Cloudflare Worker-u ili Polar serveru je drift-an. Provjeri:

```bash
curl https://lts-polar-webhook.<sub>.workers.dev/health
# ts u outputu treba biti ±5s od stvarnog vremena
```

### Streamlit ne reflektira novi entitlement

TTL cache 30s u `entitlements.py`. Korisnik može:
- Refresh-ati 30+ sekundi nakon checkout-a
- Ili dodaj UI gumb "Refresh status" koji poziva `entitlements.invalidate_cache(user_id)`

### "Free tier limit exceeded"

| Servis | Limit | Mitigacija |
|---|---|---|
| Supabase | 500 MB DB | Prune `download_log` starija od 24 mj (cron) |
| CF Workers | 100k req/dan | Webhook ~10 ev/dan; checkout ~5/dan; daleko ispod |
| Streamlit | 1 GB RAM, public repo | Optimiziraj imports (lazy load); upgrade na paid ako treba |
| Polar | bez API limita sandbox | Production: Polar uzima ~4-5% provizije + fixed fee po transakciji (varira po pricing planu) |

### Korisnik download-a docx u offline mode-u

Kad je Streamlit gore ali Supabase/CF down: `entitlements.is_pro()` vraća `False` (graceful degradation), korisnik dobije **free tier** docx (s vidljivim footer-om). Ne crashes; PROnost se "vrati" kad se Supabase oporavi.

---

## Migracija s legacy Stripe deploya

Ako si već deploy-ao Stripe verziju (`cf_worker_stripe.ts`) prije 2026-04-28:

1. Zadrži postojeći Supabase projekt (schema je payment-neutralna).
2. Deploy novi CF Worker s `cf_worker_polar.ts` na **drugi worker name** (npr. `lts-polar-webhook`) da paralelno radi tijekom prelaska.
3. U Streamlit secrets dodaj `CHECKOUT_URL_BASE` koji pokazuje na novi Polar worker. Stari `STRIPE_CHECKOUT_URL_BASE` možeš zadržati kao fallback dok ne migriraš sve postojeće subscriptions na Polar (ako ih ima).
4. Stripe → Polar migration postojećih pretplata je manualan posao (nema oficijalni alat) — najlakše: ostavi Stripe pretplate aktivne dok ne isteknu, pa nove samo na Polar.
