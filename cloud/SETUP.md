# K3 Cloud Setup — LegalTechSuite Pro

> **Cilj**: Postaviti cloud stack tako da app radi 24/7 **kad je PC isključen**.
> Sve komponente u free tier-u; total trošak ≤ 0 EUR/mj dok god si ispod limita.
>
> **Vrijeme**: ~45 min (jednokratno).

---

## Pregled stack-a

```
[Korisnik browser]
      │
      ▼
[Streamlit Community Cloud]  (postojeci, https://legal-suite-flh3jnmcj5kc7jp5y9w9eb.streamlit.app)
      │  cita entitlement pri svakom download-u
      ▼
[Supabase Postgres]  ◄────  upsert iz CF Worker-a (preko service_role)
      ▲
      │  sve REST pozivi
      │
[Cloudflare Worker]  (https://lts-stripe-webhook.<sub>.workers.dev)
      ▲
      │  Stripe webhook
[Stripe]  (Checkout + Subscription)
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

6. **Dohvati credentials**:
   - **Settings → API**
   - Spremi (potrebno kasnije):
     - `Project URL` → bit će `SUPABASE_URL`
     - `anon public` key → bit će `SUPABASE_ANON_KEY` (za Streamlit klijent, RLS-zaštićen)
     - `service_role` secret key → bit će `SUPABASE_SERVICE_ROLE_KEY` (za CF Worker, **NIKAD u Streamlit secrets!**)

---

## 2. Stripe setup (~10 min)

1. Idi na **https://stripe.com** → Sign up
2. **Test mode** (toggle gore desno) — radi sve test prije live
3. **Products → Add product**:
   - Name: `LegalTechSuite PRO`
   - Pricing model: **Recurring**
   - Price: `9.99 EUR` (ili tvoj broj)
   - Billing period: **Monthly**
   - Save → kopiraj `Price ID` (oblik `price_xxx`) → bit će `STRIPE_PRICE_ID_PRO`

4. **Developers → API keys**:
   - **Publishable key** (`pk_test_xxx`) — Streamlit (UI ne treba ako koristimo CF Worker za checkout, ali korisno)
   - **Secret key** (`sk_test_xxx`) — CF Worker → bit će `STRIPE_API_KEY`

5. **Webhook setup** (radit ćeš ovo NAKON CF Worker deploya u koraku 3):
   - Developers → Webhooks → **Add endpoint**
   - Endpoint URL: `https://lts-stripe-webhook.<sub>.workers.dev/webhook` (popuniš nakon koraka 3)
   - Events to send (klikni "Select events"):
     - `checkout.session.completed`
     - `customer.subscription.updated`
     - `customer.subscription.deleted`
     - `charge.refunded`
     - `charge.dispute.created`
   - Save → **Signing secret** (`whsec_xxx`) → bit će `STRIPE_WEBHOOK_SECRET`

6. **Stripe Tax** (HR PDV automatski):
   - Settings → Tax → Activate
   - Origin: Croatia
   - Save

---

## 3. Cloudflare Worker deploy (~15 min)

1. Idi na **https://dash.cloudflare.com** → Sign up
2. Lokalno na svom računalu (jednom):

   ```bash
   npm install -g wrangler
   wrangler login   # otvori browser, autoriziraj
   ```

3. Deploy:

   ```bash
   cd "C:/Users/Hrvoje Matej/Documents/APLIKACIJA/cloud"
   npm install                # dohvati stripe + cloudflare-types
   wrangler deploy            # daje URL: https://lts-stripe-webhook.<sub>.workers.dev
   ```

   Spremi taj URL.

4. **Postavi secrets** (svaki je odvojena `wrangler secret put` komanda — wrangler će pitati vrijednost):

   ```bash
   wrangler secret put STRIPE_API_KEY              # paste sk_test_xxx
   wrangler secret put STRIPE_WEBHOOK_SECRET       # paste whsec_xxx (iz Stripe Webhook config)
   wrangler secret put STRIPE_PRICE_ID_PRO         # paste price_xxx
   wrangler secret put SUPABASE_URL                # paste https://xxx.supabase.co
   wrangler secret put SUPABASE_SERVICE_ROLE_KEY   # paste service_role key (TAJNO!)
   wrangler secret put APP_RETURN_URL              # paste https://legal-suite-flh3jnmcj5kc7jp5y9w9eb.streamlit.app
   ```

5. **Re-deploy** da pokupi secrets:

   ```bash
   wrangler deploy
   ```

6. **Health check**:

   ```bash
   curl https://lts-stripe-webhook.<sub>.workers.dev/health
   # ocekivan output: {"ok":true,"ts":"2026-04-27T..."}
   ```

7. **Vrati se u Stripe Dashboard** (korak 2.5) i dovrši webhook setup s URL-om iz koraka 3.3.

---

## 4. Streamlit Cloud secrets (~5 min)

1. Idi na **https://share.streamlit.io** → tvoj `LEGAL-SUITE` app
2. Klikni `⋮` → **Settings → Secrets**
3. Dodaj (TOML format):

   ```toml
   SUPABASE_URL = "https://xxx.supabase.co"
   SUPABASE_ANON_KEY = "eyJh..."   # anon key, NE service_role!
   STRIPE_CHECKOUT_URL_BASE = "https://lts-stripe-webhook.<sub>.workers.dev"
   ```

4. **Save**. Streamlit će auto-restart-ati app (~30s).

---

## 5. End-to-end smoke test (~5 min)

1. **Otvori** `https://legal-suite-flh3jnmcj5kc7jp5y9w9eb.streamlit.app`
2. **Registriraj** test korisnika (email + lozinka kroz postojeći auth — migracija na Supabase auth je odvojen task)
3. Klikni **Pretplati se na PRO** → otvori Stripe Checkout
4. **Test kartica**: `4242 4242 4242 4242`, datum: bilo koji budući, CVC: `123`
5. Završi checkout → Stripe te vrati na app (`?checkout=success`)
6. Refresh stranice
7. Generiraj bilo koji dokument → docx footer treba imati `ID: NN-NNNN-NNNNNN` (bez "Generirano iz LegalTechSuite Pro" jer si PRO)
8. Provjeri u Supabase Dashboard → **Table Editor → entitlements** → trebao bi vidjeti red s `plan='pro'`, `status='active'`

---

## 6. Production switch (kad je sve test mode OK)

1. Stripe Dashboard → toggle **Live mode** (gore desno)
2. Ponovi korak 2.3-2.5 s **live keys** (`sk_live_xxx`, `whsec_xxx`, `price_xxx`)
3. `wrangler secret put` zamijeni sve secrets na live
4. Stripe Dashboard → **Activate Tax** za live mode (HR PDV)
5. Stripe Dashboard → **Settings → Business settings** popuni HR poslovne podatke (OIB, adresa)

---

## Troubleshooting

### Webhook "signature verify failed"

`STRIPE_WEBHOOK_SECRET` u CF Worker secret-u ne odgovara onom u Stripe Dashboard webhook config-u. Provjeri `wrangler secret list` i regeneriraj webhook secret u Stripe.

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
| Stripe | bez API limita test mode | Live mode 25 EUR mj minimum kartični promet (besplatan ispod tog) |

### Korisnik download-a docx u offline mode-u

Kad je Streamlit gore ali Supabase/CF down: `entitlements.is_pro()` vraća `False` (graceful degradation), korisnik dobije **free tier** docx (s vidljivim footer-om). Ne crashes; PROnost se "vrati" kad se Supabase oporavi.
