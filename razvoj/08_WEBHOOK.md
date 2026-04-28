# 08 — WEBHOOK: SUPABASE EDGE FUNCTION

> **Najsloženiji korak**, ali nakon ovog imaš end-to-end sustav. Vrijeme: 30-60 min.
>
> Pisat ćeš kratak TypeScript kod (~50 linija) koji živi na Supabase serveru i prima poruke od Lemon Squeezyja.

---

## 1. ŠTO JE EDGE FUNCTION

Zamisli **mali web server** koji:
- Sjedi na Supabase infrastrukturi
- Čeka HTTP zahtjeve na svom URL-u
- Kad dođe zahtjev — pokrene tvoj kod (Deno / TypeScript)
- Vrati odgovor

Razlika od pravog servera:
- **Bez konfiguracije infrastrukture** (Supabase to riješava)
- **Skalira automatski** (1 ili 1.000.000 zahtjeva — radi)
- **Free** do 500.000 poziva mjesečno
- **Vrlo brz cold start** (~50ms)

---

## 2. ŠTO ĆE NAŠA EDGE FUNCTION RADITI

```
Lemon Squeezy webhook stigne ──→ Edge Function provjeri potpis
                                          │
                                          ▼
                              Parsiraj JSON, dohvati user_id
                                          │
                                          ▼
                              UPSERT u subscriptions tablicu
                                          │
                                          ▼
                              Vrati 200 OK Lemon Squeezyju
```

---

## 3. INSTALACIJA SUPABASE CLI

Da bi deployao Edge Function, treba ti CLI alat.

### 3.1 Windows (PowerShell)

```powershell
# Preko scoop (najlakše)
scoop install supabase

# ILI preko npm (ako imaš Node.js)
npm install -g supabase

# Provjeri instalaciju
supabase --version
```

Ako nemaš ni jedno — prvo instaliraj **Node.js** (nodejs.org, LTS verzija) ili **scoop** (scoop.sh). Node.js je standardno za sve moderne dev alate.

### 3.2 Login u CLI

```powershell
supabase login
```

Otvorit će browser, prijavi se s istim accountom kao u Supabase web UI, klikni Authorize.

---

## 4. POVEZIVANJE LOKALNOG FOLDERA S TVOJIM PROJEKTOM

U `APLIKACIJA` folderu (PowerShell):

```powershell
cd C:\Users\{{WIN_USER}}\Documents\APLIKACIJA
supabase init
```

Ovo kreira:
```
APLIKACIJA/
├── supabase/
│   ├── config.toml
│   └── ... (default folderi)
```

### 4.1 Link s tvojim cloud projektom

Treba ti **project ref** (kratki ID iz URL-a):
- Tvoj Supabase URL je `https://abcdefghijkl.supabase.co`
- Project ref je `abcdefghijkl`

```powershell
supabase link --project-ref abcdefghijkl
```

Pita za database password (onaj koji si spremio u password manager). Ako ga zaboraviš → Settings → Database → Reset database password.

### 4.2 Provjeri da link radi

```powershell
supabase status
```

Trebao bi vidjeti detalje o tvom projektu.

---

## 5. KREIRANJE EDGE FUNCTION-A

```powershell
supabase functions new lemonsqueezy-webhook
```

Ovo kreira:
```
supabase/
└── functions/
    └── lemonsqueezy-webhook/
        ├── index.ts          ← TVOJ KOD IDE TU
        └── deno.json
```

---

## 6. TVOJ KOD — `index.ts`

Otvori `supabase/functions/lemonsqueezy-webhook/index.ts` i **zamijeni** sav sadržaj sljedećim:

```typescript
// =============================================================================
// LEMON SQUEEZY WEBHOOK HANDLER
// Prima webhook event-e iz Lemon Squeezyja, validira HMAC potpis,
// i sinhronizira subscription state u Supabase tablicu.
// =============================================================================

import { serve } from "https://deno.land/std@0.208.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.0";
import { createHmac } from "https://deno.land/std@0.208.0/node/crypto.ts";

// -----------------------------------------------------------------------------
// ENV VARIABLES — postavljaju se preko `supabase secrets set`
// -----------------------------------------------------------------------------
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const LS_WEBHOOK_SECRET = Deno.env.get("LS_WEBHOOK_SECRET")!;

// Kreiraj Supabase admin klijent (koristi service_role key — bypassa RLS)
const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

// -----------------------------------------------------------------------------
// MAIN HANDLER
// -----------------------------------------------------------------------------
serve(async (req: Request) => {
  // CORS preflight (LS ne šalje OPTIONS, ali za svaki slučaj)
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  // -------------------------------------------------------------------------
  // 1) DOHVATI RAW BODY (potreban za HMAC validaciju)
  // -------------------------------------------------------------------------
  const rawBody = await req.text();
  const signatureHeader = req.headers.get("x-signature") || "";

  // -------------------------------------------------------------------------
  // 2) VALIDIRAJ HMAC SHA-256 POTPIS
  // -------------------------------------------------------------------------
  const expectedSignature = createHmac("sha256", LS_WEBHOOK_SECRET)
    .update(rawBody)
    .digest("hex");

  if (signatureHeader !== expectedSignature) {
    console.error("Invalid signature", {
      received: signatureHeader.substring(0, 16),
      expected: expectedSignature.substring(0, 16),
    });
    return new Response("Invalid signature", { status: 401 });
  }

  // -------------------------------------------------------------------------
  // 3) PARSE JSON
  // -------------------------------------------------------------------------
  let event;
  try {
    event = JSON.parse(rawBody);
  } catch (e) {
    return new Response("Invalid JSON", { status: 400 });
  }

  const eventName = event?.meta?.event_name;
  const data = event?.data;
  const customData = event?.meta?.custom_data || {};
  const userId = customData.user_id;

  console.log(`Webhook received: ${eventName} for user ${userId}`);

  if (!userId) {
    console.error("Missing user_id in custom_data", { customData });
    return new Response("Missing user_id", { status: 400 });
  }

  // -------------------------------------------------------------------------
  // 4) HANDLE PER EVENT TYPE
  // -------------------------------------------------------------------------
  try {
    if (eventName?.startsWith("subscription_")) {
      await handleSubscriptionEvent(eventName, data, userId);
    } else if (eventName === "order_created") {
      // Jednokratne kupnje — možeš ignorirati ili logirati
      console.log("One-time order received (not handled)");
    } else {
      console.log(`Ignoring event type: ${eventName}`);
    }
  } catch (error) {
    console.error("Error processing event:", error);
    return new Response(`Error: ${error.message}`, { status: 500 });
  }

  return new Response("OK", { status: 200, headers: corsHeaders });
});

// -----------------------------------------------------------------------------
// SUBSCRIPTION EVENT HANDLER
// -----------------------------------------------------------------------------
async function handleSubscriptionEvent(
  eventName: string,
  data: any,
  userId: string,
) {
  const attrs = data?.attributes || {};

  const subscriptionRecord = {
    user_id: userId,
    ls_subscription_id: String(data.id),
    ls_customer_id: String(attrs.customer_id || ""),
    variant_id: String(attrs.variant_id || ""),
    status: attrs.status || "unknown",
    renews_at: attrs.renews_at || null,
    ends_at: attrs.ends_at || null,
    updated_at: new Date().toISOString(),
  };

  // UPSERT — insert ako ne postoji, update ako postoji (po ls_subscription_id)
  const { error } = await supabase
    .from("subscriptions")
    .upsert(subscriptionRecord, { onConflict: "ls_subscription_id" });

  if (error) {
    console.error("Supabase upsert error:", error);
    throw new Error(`DB error: ${error.message}`);
  }

  console.log(`Subscription ${eventName}: user=${userId}, status=${attrs.status}`);
}

// -----------------------------------------------------------------------------
// CORS HEADERS
// -----------------------------------------------------------------------------
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-signature",
};
```

---

## 7. OBJAŠNJENJE KODA (LAIČKI)

### 7.1 `serve(async (req) => { ... })`

Pokreni server koji za svaki dolazni zahtjev pokrene ovu funkciju. Deno standardna stvar.

### 7.2 HMAC validacija

**Što je HMAC:** matematički potpis. Lemon Squeezy uzme tvoj webhook secret + body poruke, izračuna SHA-256 hash. Pošalje hash u `x-signature` header. Ti to isto izračunaš na svojoj strani — ako se podudara, poruka je autentična. Ako ne — netko se pretvara da je LS.

**Zašto je važno:** bez HMAC, bilo tko može pošaljati lažan webhook tipa "user X je platio 1.000 EUR" i dobiti pretplatu badava.

### 7.3 `customData.user_id`

Ovo je `user_id` koji si "uvukao" u checkout URL kad je korisnik kliknuo "Pretplati se" (vidi `billing._ls_checkout_url()`). Bez toga — ne znaš kome pripada pretplata.

### 7.4 Status mapping

LS šalje različite event-e (`subscription_created`, `subscription_payment_success`, `subscription_cancelled`...). Svi imaju `attributes.status` polje koje govori trenutni stanje.

| Event | status u DB |
|-------|-------------|
| subscription_created | active / on_trial |
| subscription_payment_success | active |
| subscription_cancelled | cancelled (s `ends_at` na kraj plaćenog razdoblja) |
| subscription_expired | expired |
| subscription_payment_failed | past_due |
| subscription_paused | paused |

Mi samo "kopiramo" što LS šalje — ne tumačimo.

### 7.5 UPSERT (umjesto INSERT)

UPSERT = insert ako ne postoji + update ako postoji. Ključ za "isto" je `ls_subscription_id`.

**Zašto:** isti subscription ima više event-a (created → payment_success → cancelled). Sve trebaju ažurirati isti red.

### 7.6 `service_role` key

Edge Function koristi **service_role** Supabase ključ (full pristup, bypassa RLS). To je sigurno jer key ne ide nigdje izvan Supabase infrastrukture — samo Edge Function ga vidi.

⚠️ **NIKAD** ovaj ključ ne stavljaj u Streamlit secrets ili frontend kod.

---

## 8. POSTAVLJANJE SECRETS

Edge Function treba 3 environment varijable. Postavi ih:

```powershell
# SUPABASE_URL i SUPABASE_SERVICE_ROLE_KEY su automatski dostupni Edge Function-u
# (Supabase ih injecta), ne moraš ih postavljati.

# Trebaš samo LS_WEBHOOK_SECRET:
supabase secrets set LS_WEBHOOK_SECRET=ls_whsec_abcd1234efgh5678
```

(Zamijeni s tvojim secret-om iz Lemon Squeezy → Settings → Webhooks.)

Provjera:

```powershell
supabase secrets list
```

Trebao bi vidjeti `LS_WEBHOOK_SECRET` na popisu (vrijednost je sakrivena).

---

## 9. DEPLOY

```powershell
supabase functions deploy lemonsqueezy-webhook --no-verify-jwt
```

**`--no-verify-jwt`** je važan — kaže "ne traži Supabase auth token za pristup ovoj funkciji" jer LS ne zna za naše tokene.

Output bi trebao biti nešto poput:
```
Deployed Function lemonsqueezy-webhook on project abcdef
You can inspect your deployment in the Dashboard:
https://app.supabase.com/project/abcdef/functions
```

### 9.1 Provjeri deploy

Vrati se u Supabase web UI:
- Lijevo izborniku → **Edge Functions**
- Trebao bi vidjeti `lemonsqueezy-webhook` u listi
- Status: **Active**

URL funkcije:
```
https://<TVOJ_ID>.supabase.co/functions/v1/lemonsqueezy-webhook
```

---

## 10. POVEZIVANJE S LEMON SQUEEZY

Vrati se u Lemon Squeezy:
1. Settings → Webhooks
2. Klikni na webhook koji si kreirao u koraku 04
3. **Callback URL:** zalijepi gornji Edge Function URL (ako nisi već)
4. Save

---

## 11. TESTIRANJE

### 11.1 Test webhook iz LS dashboard-a

1. LS Settings → Webhooks → tvoj webhook
2. Klikni **"Send test webhook"**
3. Odaberi event: `subscription_created`
4. Klikni Send

LS pošalje fake event tvojoj Edge Function. Provjeri:

### 11.2 Provjeri logove Edge Function-a

```powershell
supabase functions logs lemonsqueezy-webhook
```

Ili u web UI: **Edge Functions → lemonsqueezy-webhook → Logs** tab.

Trebao bi vidjeti:
```
Webhook received: subscription_created for user undefined
Missing user_id in custom_data
```

To je **OK** — test webhook nema `custom_data` (jer nije pravna kupnja). Bitno je da:
1. Funkcija je primljena (status 200/400, ne 500)
2. HMAC validacija je prošla (nema "Invalid signature")

### 11.3 Pravi end-to-end test

1. U svojoj Streamlit aplikaciji prijavi se kao test user
2. Iskoristi besplatni dokument
3. Pojavi se paywall — klikni "Pretplati se mjesečno"
4. **Test mode kartica:** `4242 4242 4242 4242`, exp datum u budućnosti, CVC `123`
5. Plati

Sad provjeri:
- LS dashboard → **Orders** → trebaš vidjeti novi order
- Edge Function logs → trebao bi vidjeti `subscription_created` poruku
- Supabase Table Editor → **subscriptions** → trebao bi vidjeti novi red s tvojim `user_id` i `status='active'`
- Vrati se u Streamlit, klikni "Generiraj" — trebao bi raditi neograničeno

### 11.4 Test cancelacije

1. U LS dashboard → Orders → klikni na svoj test order → Subscription details → **Cancel subscription**
2. Webhook stiže, `subscriptions.status` postaje `cancelled` s `ends_at` u budućnosti (do kraja plaćenog razdoblja)
3. Korisnik može i dalje koristiti dok ne istekne

### 11.5 Test isteka

Ne možeš lako simulirati istek u test mode-u. Najbolji test:
- Ručno UPDATE u Supabase: `UPDATE subscriptions SET ends_at = '2020-01-01' WHERE user_id = '<uid>'`
- Obriši cache: u Streamlit `Settings → Clear cache` ili refresh
- Sad bi paywall trebao opet biti aktivan

---

## 12. MONITORING

### 12.1 LS dashboard

- **Orders** — sve transakcije
- **Subscriptions** — aktivne pretplate i statusi
- **Customers** — popis kupaca

### 12.2 Supabase Edge Function logs

```powershell
# Live tail logova
supabase functions logs lemonsqueezy-webhook --follow
```

Ili u web UI s filterom po vremenu.

### 12.3 Supabase database

- Table Editor → subscriptions — trenutno stanje svih
- SQL Editor:
  ```sql
  SELECT status, COUNT(*) FROM subscriptions GROUP BY status;
  ```

---

## 13. EDGE CASE — DEAD LETTER QUEUE

**Problem:** što ako Edge Function padne kad webhook dođe? LS pokušava 3× s exponential backoff (5s, 30s, 5min), zatim odustaje. Možeš izgubiti pretplatu update.

**Rješenje (za v6, ne sad):**
- Dodaj `webhook_log` tablicu u Supabase
- Edge Function PRVI korak: insert u `webhook_log` (raw payload)
- Drugi korak: pokušaj process
- Ako padne — log ostaje, ručno možeš re-process kasnije

Za MVP — Edge Function je dovoljno pouzdana (Supabase 99.9% uptime). Ako se nešto nikad ne sinhronizira → ručno SQL UPDATE.

---

## 14. AŽURIRANJE EDGE FUNCTION-A KASNIJE

Kad mijenjaš `index.ts`:

```powershell
supabase functions deploy lemonsqueezy-webhook --no-verify-jwt
```

To je sve. Deploy je instant, no downtime.

---

## TIPIČNI PROBLEMI

**"`supabase: command not found`"**
→ CLI nije u PATH-u. Restartaj terminal. Ili koristi punu putanju (`C:\Users\<you>\scoop\shims\supabase.exe`).

**"`supabase functions deploy` javlja Auth error"**
→ Nisi `supabase login`. Pokreni opet.

**"Edge Function deploya ali Logs prazni"**
→ Logovi se filtriraju po vremenu. Provjeri da je vremenski raspon dovoljan. Pokreni test webhook iz LS i odmah pogledaj logove.

**"Invalid signature error u logovima"**
→ Webhook secret nije sinhroniziran. Pokreni:
```powershell
supabase secrets set LS_WEBHOOK_SECRET=<točan-secret-iz-LS>
```
i provjeri u LS Settings → Webhooks da je secret koji vidi LS isti kao taj.

**"`Missing user_id` u logovima nakon prave kupnje"**
→ Tvoj `_ls_checkout_url()` ne uvlači `custom_data` ispravno. Provjeri da URL koji se generira ima `?checkout[custom][user_id]=...`. Test: copy paste URL u browser, vidiš query string.

**"`relation 'subscriptions' does not exist`"**
→ SQL schema iz koraka `03` nije pokrenuta. Vrati se i pokreni.

**"Cold start je spor (~3-5 sekundi)"**
→ Normalno za prvi poziv nakon dugog mirovanja. Drugi poziv je <100ms. LS retry-a 3×, dovoljno vremena.

**"Hoće li Edge Function trošiti free tier brzo?"**
→ 500.000 poziva mjesečno. Realističko korištenje 100-1000 webhookova/mj — daleko ispod limita.

---

## 15. ŠTO SI POSTIGAO

✅ Edge Function deployan na Supabase
✅ HMAC validacija sigurnih webhookova
✅ Auto-sinhronizacija LS pretplata u tvoju bazu
✅ End-to-end tok radi: korisnik plati → webhook → DB → app vidi pretplatu

**Sad imaš funkcionalan sustav.**

---

## SLJEDEĆI KORAK

Otvori `09_LANSIRANJE.md` — checklist prije nego pustiš stvarne ljude unutra.
