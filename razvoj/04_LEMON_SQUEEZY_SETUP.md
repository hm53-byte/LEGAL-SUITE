# 04 — POSTAVLJANJE LEMON SQUEEZY (NAPLATA)

> Sad postavljaš mehanizam koji **stvarno uzima novac od korisnika**. Vrijeme: 30-45 minuta.
>
> **PREDUVJET:** moraš imati registriran obrt (vidi `01_PRAVNI_OKVIR.md`) jer Lemon Squeezy traži podatke o pravnom subjektu prije isplate.

---

## 1. ZAŠTO LEMON SQUEEZY (A NE STRIPE)

Stripe je standard u industriji, jeftiniji (~1.5% naspram 5%). **Ali:**

- Stripe **NE** rješava EU PDV. Ti moraš sam.
- Za digitalne usluge u EU — VAT MOSS / OSS prijave kvartalno za 27 zemalja
- Solo developer to ne stigne
- **Lemon Squeezy je Merchant of Record** — oni postaju prodavač, oni rješavaju PDV
- Plaćaš 5% premium da ti netko drugi rješava poreze

**Drugi MoR konkurenti:** Paddle, Gumroad, Polar.sh, FastSpring. Svi rade slično. Lemon Squeezy je trenutno najpopularniji za softver-as-service.

---

## 2. OTVARANJE RAČUNA

### 2.1 Sign up

1. Idi na **https://www.lemonsqueezy.com**
2. **Sign up** (može s Google nalogom)
3. Potvrdi email

### 2.2 Onboarding wizard

LS će te provesti kroz nekoliko ekrana:

1. **What are you selling?** → odaberi **"SaaS / Subscription"**
2. **Where are you based?** → **Croatia**
3. **Have you sold online before?** → odaberi što već

### 2.3 Kreiranje Store-a

**Store** je kao "trgovina" — može imati više proizvoda.

1. Klikni **"Create your first store"**
2. **Store name:** `LegalTech Suite Pro` (vidljivo kupcima)
3. **Store URL slug:** `legaltech-suite-pro` (postaje `legaltech-suite-pro.lemonsqueezy.com`)
4. **Store currency:** **EUR**
5. **Industry:** Software / SaaS
6. Save

---

## 3. POPUNJAVANJE PODATAKA O VLASNIKU (BUSINESS DETAILS)

Bez ovoga ti neće isplatiti niti euro.

1. Settings (gornji desni) → **Account** → **Settings**
2. **Business details:**
   - **Business name:** točan naziv tvog obrta (npr. "LegalTech Suite, obrt vl. Hrvoje Matej")
   - **Business address:** adresa obrta (kao na rješenju o registraciji)
   - **Tax ID / VAT number:** tvoj OIB (ili PDV-id ako si u sustavu PDV-a)
   - **Country:** Croatia
3. **Personal details:**
   - Ime, prezime, datum rođenja
4. **Bank account / Payout details:**
   - **IBAN** poslovnog računa obrta
   - **SWIFT/BIC** banke
   - **Beneficiary name:** točan naziv obrta (mora se podudarati s vlasnikom IBAN-a)

5. **Tax forms:**
   - **W-8BEN** — popunjavaš da nisi američki rezident → 0% US tax withholding
   - To je samo formalnost, kliki "Yes I'm not a US person" i potpiši elektronski

6. Save sve

⚠️ **Verifikacija:** LS može tražiti dokumente (rješenje o obrtu, IBAN potvrdu) prije aktivacije isplata. Pripremi PDF-ove. Trajanje provjere: 1-3 radna dana.

---

## 4. KREIRANJE PROIZVODA (PROIZVODA = PRETPLATE)

Sad kreiraš tri pretplate koje korisnici mogu kupiti.

### 4.1 Tjedna pretplata

1. Lijevo izborniku → **Products** → **New product**
2. Popuni:
   - **Name:** `Tjedna pretplata`
   - **Description:** `Neograničeno generiranje pravnih dokumenata na 7 dana. Automatska obnova svakih 7 dana, otkaz u bilo kojem trenutku.`
   - **Status:** Published
3. Scroll na **Pricing**:
   - **Pricing model:** **Subscription**
   - **Price:** `9.99` EUR
   - **Billing interval:** Every `1` `Week`
4. **Trial period:** ostavi 0 dana (možeš dodati 3 dana free trial kasnije ako želiš)
5. **Tax behaviour:** **Inclusive** (Lemon Squeezy uračunava PDV u prikazanu cijenu)
6. Save

Nakon save-a vidiš:
- **Product ID** — koristit ćeš u kodu (npr. `123456`)
- **Variant ID** — još bitnije (npr. `654321`)
- **Checkout URL** — link gdje korisnik plaća (npr. `https://legaltech-suite-pro.lemonsqueezy.com/buy/abc-uuid`)

**Kopiraj checkout URL u svoj `notes.txt`** kao `LS_CHECKOUT_WEEKLY`.

### 4.2 Mjesečna pretplata

Ponovi isto:
- Name: `Mjesečna pretplata`
- Price: `19.99` EUR
- Billing interval: Every `1` `Month`
- Spremi checkout URL kao `LS_CHECKOUT_MONTHLY`

### 4.3 Godišnja pretplata

- Name: `Godišnja pretplata`
- Price: `149` EUR
- Billing interval: Every `1` `Year`
- Spremi checkout URL kao `LS_CHECKOUT_YEARLY`
- (Promo): u opisu napiši "Ušteda 38% u odnosu na mjesečnu"

---

## 5. CHECKOUT PRILAGODBA (LIČNI DODIR)

1. Settings → **Checkout** (per Store level)
2. **Logo:** upload-aj svoj logo (ako imaš)
3. **Primary color:** `#1E3A5F` (mornarsko plava, kao u tvojoj app)
4. **Display business address:** ON (za uredne račune kupcima)
5. **Allowed payment methods:**
   - **Cards:** ON (Visa, Mastercard, Amex)
   - **PayPal:** ON
   - **SEPA Direct Debit:** ON (popularan u EU za pretplate)
   - **Apple Pay / Google Pay:** ON

6. **Customer portal:**
   - **Enable customer portal:** ON
   - To znači da korisnik dobiva link gdje može sam upravljati pretplatom (ažurirati karticu, otkazati, vidjeti račune) bez tebe

7. Save

---

## 6. POSTAVLJANJE WEBHOOKA (NAJVAŽNIJI DIO)

Webhook je **kako Lemon Squeezy javlja tvojoj bazi da je netko platio**. Bez ovoga, baza nikad ne sazna.

### 6.1 Kreiranje webhook URL-a

Trebat ćeš URL Edge Function-a koju ćeš deployati u koraku `08_WEBHOOK.md`. Već sad rezerviraš ime:

URL će biti:
```
https://<TVOJ_SUPABASE_ID>.supabase.co/functions/v1/lemonsqueezy-webhook
```

(Zamijeni `<TVOJ_SUPABASE_ID>` s tvojim ID-om iz `notes.txt`.)

### 6.2 Dodavanje webhooka u LS

1. Settings → **Webhooks** → **+ webhook**
2. **Callback URL:** zalijepi gornji URL
3. **Signing secret:** klikni **"Generate new"** → kopiraj generirani secret u `notes.txt` kao `LS_WEBHOOK_SECRET`
4. **Events to subscribe** — označi sve subscription event-e:
   - `subscription_created`
   - `subscription_updated`
   - `subscription_cancelled`
   - `subscription_resumed`
   - `subscription_expired`
   - `subscription_paused`
   - `subscription_unpaused`
   - `subscription_payment_success`
   - `subscription_payment_failed`
   - `subscription_payment_recovered`

   (Ako prodaješ i jednokratne kupnje: + `order_created`, `order_refunded`)

5. Save

### 6.3 Testiranje webhooka — kasnije

Webhook **neće raditi sad** jer Edge Function još ne postoji. To je OK. Postavi sve kako je gore navedeno, a kad u koraku 08 deployaš Edge Function — webhook će automatski profunkcionirati.

LS ima i **Test webhook** gumb koji šalje fake event — koristit ćemo ga za debug u koraku 08.

---

## 7. POREZ (TAX SETTINGS)

Najvažnija opcija da Lemon Squeezy postane tvoj MoR:

1. Settings → **Taxes**
2. **Lemon Squeezy handles tax for you:** **ON** ✅
3. Pojavit će se popis zemalja gdje LS zaračunava porez. Sve OK, ostavi kako je.

To znači:
- Hrvatski kupac plati 19.99 EUR + 25% PDV = ~24.99 EUR (LS automatski izračuna)
- Njemački kupac plati 19.99 EUR + 19% PDV = ~23.79 EUR
- Američki kupac plati 19.99 EUR + state sales tax (varira)
- LS prikuplja sav porez i sam ga prijavljuje vladama
- Tebi dolazi tvojih 19.99 EUR (minus 5% + 0.50 EUR fee)

**Ovo te oslobađa odgovornosti za EU VAT MOSS / OSS prijave.**

---

## 8. ISPLATE (PAYOUT SCHEDULE)

1. Settings → **Payouts**
2. **Payout schedule:** odaberi
   - **Daily** (svaki dan kad ima minimum 10 USD) — najčešće
   - **Weekly** (svaki ponedjeljak) — preporučujem
   - **Monthly** (1. u mjesecu)
3. **Minimum payout:** **10 USD** (LS minimum)
4. **Currency:** EUR (već je)

**Kako stvarno funkcionira:**
- Kupac plati danas
- LS drži novac u "balance"
- Po payout schedule-u, prebaci na tvoj IBAN
- **Holding period:** prvih 30 dana mogu držati za chargeback risk (standardno)
- Nakon 30 dana → svi payouti odmah

---

## 9. PRIVATNOST I PRAVNI DOKUMENTI (LS UPLOAD)

LS treba znati tvoj Privacy Policy i Terms da prikaže kupcima.

1. Settings → **Legal**
2. **Terms of Service URL:** stavi link na svoj Terms (vidi `01_PRAVNI_OKVIR.md` — koristi termly.io)
3. **Privacy Policy URL:** isto
4. **Refund Policy URL:** napiši kratku refund policy (npr. "14-day money-back guarantee" ili "Bez refundova nakon prvog korištenja")

**EU zakon o digitalnim sadržajima:** korisnik može tražiti refund unutar 14 dana **osim ako je već koristio uslugu**. Tipično se kaže: "Klikom na 'Generiraj prvi dokument' korisnik se odriče prava na refund."

---

## 10. TEST KUPNJA (S TEST KARTICOM)

Prije nego pustiš na produkciju — testiraj.

LS ima **test mode**:

1. Settings → **General** → toggle **Test mode** ON
2. Sad si u test okruženju
3. Idi na svoj checkout URL (npr. mjesečna pretplata)
4. Popuni:
   - Email: tvoj test email
   - **Card number:** `4242 4242 4242 4242` (Stripe test kartica)
   - Expiry: bilo koji budući datum
   - CVC: bilo koja 3 broja
5. **Pay**
6. Trebao bi vidjeti success ekran

U LS dashboard → **Orders** → vidiš test order.

⚠️ Webhook se **isto okida u test mode-u** — to ti pomaže testirati Edge Function.

Kad završiš s testiranjem → toggle Test mode OFF prije produkcije.

---

## 11. ZAPISI ZA `secrets.toml`

U svoj `notes.txt` trebaš sad imati:

```
SUPABASE_URL = "https://<id>.supabase.co"
SUPABASE_ANON_KEY = "..."
SUPABASE_SERVICE_KEY = "..."

LS_API_KEY = "..."             (iz Settings → API)
LS_WEBHOOK_SECRET = "..."      (iz Settings → Webhooks)
LS_CHECKOUT_WEEKLY  = "https://legaltech-suite-pro.lemonsqueezy.com/buy/<uuid-1>"
LS_CHECKOUT_MONTHLY = "https://legaltech-suite-pro.lemonsqueezy.com/buy/<uuid-2>"
LS_CHECKOUT_YEARLY  = "https://legaltech-suite-pro.lemonsqueezy.com/buy/<uuid-3>"

APP_URL = "https://legal-suite-flh3jnmcj5kc7jp5y9w9eb.streamlit.app"
```

Ovi će se zalijepiti u secrets u `09_LANSIRANJE.md`.

---

## 12. ŠTO SI POSTIGAO

✅ Otvoren Lemon Squeezy račun s podacima obrta
✅ Tri pretplate kreirane (tjedna, mjesečna, godišnja)
✅ Checkout prilagođen tvom brendingu
✅ Webhook URL spreman (čeka Edge Function)
✅ MoR mode aktiviran — LS rješava PDV
✅ Test kupnja prošla

**Nemaš još koda — to je sljedeći korak.**

---

## TIPIČNI PROBLEMI

**"LS traži dokumente za verifikaciju, koje?"**
→ Skeniran rješenje o registraciji obrta (1 stranica), kopija osobne, IBAN potvrda iz banke. Sve PDF, max 5 MB svaki. Verifikacija 1-3 dana.

**"Cijena u checkout-u je drukčija od one koju sam stavio"**
→ To je PDV (npr. 19.99 + 25% = 24.99 za HR kupca). Možeš podesiti **Tax behaviour: Exclusive** ili **Inclusive** (preporučujem Inclusive — jasnije korisniku).

**"Korisnik želi otkazati pretplatu — gdje?"**
→ Customer portal link. Pošalji im link iz njihovog email računa LS-a (svi LS emailovi imaju "Manage subscription" gumb), ili dodaj u svojoj app gumb koji ih vodi na `https://my-customer.lemonsqueezy.com/billing`.

**"Što ako kartica bude odbijena pri obnovi?"**
→ LS automatski pokušava 3 puta tijekom 7 dana (smart retry). Status pretplate je `past_due`. Tijekom toga korisnik i dalje ima pristup (3-day grace period u tvojoj logici). Ako se ne obnovi — pretplata postaje `unpaid` i prekida.

**"Mogu li imati promo kod?"**
→ Da, **Discounts** sekcija u LS dashboard-u. Kreiraš kod (npr. `LAUNCH50` za 50% off prvog mjeseca), korisnik unese pri checkout-u.

**"Što ako želim mijenjati cijenu kasnije?"**
→ Nova **Variant** istog Producta s novom cijenom. Postojeći pretplatnici plaćaju staru cijenu (grandfather clause), novi plaćaju novu. To je profesionalna praksa.

**"Hrvatski IBAN — radi li?"**
→ Da, LS isplaćuje na bilo koji EU IBAN bez problema. SEPA wire, nema dodatnog troška.

**"Kad ću prvi put dobiti payout?"**
→ Nakon 30 dana hold periode + tvoj payout schedule. Realno: prva uplata na IBAN otprilike 5-6 tjedana nakon prve naplate.

---

## SLJEDEĆI KORAK

Otvori `05_KOD_BILLING.md` — **sad počinje pisanje koda.**
