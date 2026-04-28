# 09 — LANSIRANJE: CHECKLIST PRIJE PRODUKCIJE

> Sve je tehnički postavljeno. Sad ide finiš — popunjavanje secrets-a, testovi, pravna dokumentacija, prvi pravi launch.
>
> **Ne preskoči ovaj korak.** Svaki bug koji uđe u produkciju gubi povjerenje korisnika.

---

## 1. POPUNI `.streamlit/secrets.toml`

### 1.1 Lokalno

Kreiraj file `APLIKACIJA/.streamlit/secrets.toml` (ako ne postoji folder, kreiraj `.streamlit` prvo).

```toml
# =============================================================================
# .streamlit/secrets.toml — sve API ključeve i konfiguracije
# DODAJ U .gitignore — NIKAD NE COMMITAJ NA GITHUB!
# =============================================================================

# ----- SUPABASE -----
SUPABASE_URL = "https://abcdefghijkl.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR..."
# NAPOMENA: SUPABASE_SERVICE_KEY se NE STAVLJA ovdje
# (koristi se samo u Edge Function-u, ne u Streamlit aplikaciji)

# ----- LEMON SQUEEZY -----
# Checkout URL-ovi (pojedinačnih varijanti pretplate)
LS_CHECKOUT_WEEKLY  = "https://legaltech-suite-pro.lemonsqueezy.com/buy/uuid-weekly"
LS_CHECKOUT_MONTHLY = "https://legaltech-suite-pro.lemonsqueezy.com/buy/uuid-monthly"
LS_CHECKOUT_YEARLY  = "https://legaltech-suite-pro.lemonsqueezy.com/buy/uuid-yearly"

# (LS_API_KEY i LS_WEBHOOK_SECRET nisu potrebni u Streamlit aplikaciji,
#  samo u Edge Function gdje su već postavljeni preko `supabase secrets set`)

# ----- APP CONFIG -----
APP_URL = "https://{{STREAMLIT_APP_ID}}.streamlit.app"

# ----- ADMIN (opcionalno, za buduće admin features) -----
ADMIN_EMAIL = "tvoj@email.com"
```

### 1.2 Dodaj u `.gitignore`

Otvori (ili kreiraj) `APLIKACIJA/.gitignore`:

```gitignore
# Streamlit secrets (NIKAD NE COMMITATI!)
.streamlit/secrets.toml

# Stara JSON baza
.users.json

# Backup auth
auth_old.py

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Supabase
supabase/.temp/
```

### 1.3 Streamlit Cloud secrets

Kad pushaš na GitHub, secrets neće ići s tobom (jer su u .gitignore). Trebaš ih unijeti u Streamlit Cloud:

1. Idi na **share.streamlit.io**
2. Tvoja app → **Settings** → **Secrets**
3. Zalijepi cijeli sadržaj `secrets.toml` u tekstualno polje
4. Save

Aplikacija se restartira s novim secrets-ima.

---

## 2. PRAVNI DOKUMENTI (PRIVACY POLICY + TERMS)

### 2.1 Generiraj besplatno

1. Idi na **https://termly.io** ili **https://app.freeprivacypolicy.com**
2. Sign up free
3. Generate Privacy Policy:
   - Tip biznisa: SaaS / Software
   - Zemlja: Croatia
   - Što sakupljaš: Email, ime, IP adresu (hashirana), podatke o plaćanju (preko LS)
   - Treća strana: Supabase, Lemon Squeezy, Google (ako Auth), Streamlit
4. Generate Terms of Service:
   - Refund policy: 14 days money-back if no documents generated
   - Disclaimer: "Software, ne pravna usluga"
   - Jurisdiction: Croatia, court in Zagreb

### 2.2 Postavi linkove

Dvije opcije:

**A) Hostaj na vlastitoj domeni** (ako imaš)
- npr. legalsuite.hr/privacy i legalsuite.hr/terms

**B) Stavi unutar Streamlit aplikacije**
- Kreiraj `stranice/pravni.py` s `render_privacy()` i `render_terms()` funkcijama
- Dodaj u sidebar nav: "Pravni dokumenti"
- Linkovi koje koristiš u registraciji i footer-u: `?page=privacy` (Streamlit query params)

### 2.3 Specifični za HR pravnu app

Posebno istakni u Terms:

```
DISCLAIMER:
LegalTech Suite Pro je softverski alat za izradu pravnih dokumenata.
Aplikacija ne pruža pravnu pomoć niti pravne savjete u smislu
Zakona o odvjetništvu (NN 9/94 i kasnije izmjene).

Generirani dokumenti su predlošci koje korisnik samostalno popunjava
i koristi na vlastiti rizik. Tvorca aplikacije ne može jamčiti
pravnu valjanost niti ishod postupaka u kojima se predlošci koriste.

Za konkretne pravne situacije snažno preporučujemo savjetovanje
s registriranim odvjetnikom.
```

---

## 3. COOKIE BANNER

Najjednostavniji u Streamlit-u:

```python
# U LEGAL-SUITE.py, na vrhu (poslije st.set_page_config):
if "_cookie_consent" not in st.session_state:
    cookie_box = st.empty()
    with cookie_box.container():
        c1, c2 = st.columns([4, 1])
        c1.info(
            "Ova aplikacija koristi kolačiće za održavanje sesije i analitiku. "
            "[Saznajte više](?page=privacy)"
        )
        if c2.button("Slažem se"):
            st.session_state._cookie_consent = True
            cookie_box.empty()
            st.rerun()
```

Bez agresivnog GDPR consent management platforme — za solo dev je dovoljno.

---

## 4. EMAIL — POVEZANJE PRAVOG SMTP-A

Supabase free SMTP šalje **4 emaila/sat**, što je premalo za stvarne korisnike.

### 4.1 Resend (preporučeno)

1. **resend.com** → Sign up
2. Dodaj svoju domenu (ili koristi default `onboarding@resend.dev` za test)
3. Verificiraj DNS zapise (10 min ako kontroliraš domenu)
4. Settings → API Keys → Generate

### 4.2 Postavi u Supabase

1. Supabase → Authentication → Settings → SMTP Settings
2. Toggle **Enable Custom SMTP**:
   - Sender email: `noreply@tvoja-domena.hr` (ili `onboarding@resend.dev` za početak)
   - Sender name: `LegalTech Suite Pro`
   - Host: `smtp.resend.com`
   - Port: `465`
   - Username: `resend`
   - Password: tvoj Resend API key
3. Save

Limit Resend free: 3.000 mailova/mj, 100/dan. Više nego dovoljno za početak.

---

## 5. EMAIL TEMPLATES (LIČNI DODIR)

Supabase → Authentication → Email Templates → uredi:

### 5.1 Confirm Signup

```html
<h2>Dobrodošli u LegalTech Suite Pro</h2>

<p>Hvala što ste se registrirali. Kliknite donji link da potvrdite email:</p>

<p><a href="{{ .ConfirmationURL }}">Potvrdi email</a></p>

<p>Vaš prvi dokument je <strong>besplatan</strong>. Nakon toga je dostupna pretplata
od 9,99 EUR tjedno ili 19,99 EUR mjesečno (s mogućnošću otkaza bilo kada).</p>

<p>Pozdrav,<br>LegalTech Suite Pro tim</p>
```

### 5.2 Reset Password

```html
<h2>Zatraženi reset lozinke</h2>

<p>Kliknite donji link za postavljanje nove lozinke:</p>

<p><a href="{{ .ConfirmationURL }}">Postavi novu lozinku</a></p>

<p>Ako niste vi to zatražili, ignorirajte ovaj email.</p>
```

---

## 6. TEST SCENARIJI (PROĐI SVE PRIJE LAUNCHA)

### 6.1 Happy path

- [ ] Otvori app na Streamlit Cloud URL-u
- [ ] Vidiš login ekran
- [ ] Registracija s novim emailom
- [ ] Email confirmation stiže
- [ ] Klik na link → prijava
- [ ] Generiraj 1 dokument → uspješno, banner "iskorišten 1/1"
- [ ] Generiraj još jedan → paywall
- [ ] Klik "Pretplati se mjesečno" → LS checkout
- [ ] Plati test karticom
- [ ] Vrati se u app → "PRO" badge u sidebar-u
- [ ] Generiraj još 5 dokumenata → svi rade
- [ ] U LS dashboard → vidiš subscription
- [ ] U Supabase → vidiš subscription u tablici, status active

### 6.2 Otkaz pretplate

- [ ] U LS dashboard → cancel test subscription
- [ ] Webhook stiže (provjeri Edge Function logs)
- [ ] U Supabase → status='cancelled', ends_at u budućnosti
- [ ] U app → još uvijek možeš generirati (do `ends_at`)
- [ ] Ručno UPDATE `ends_at = '2020-01-01'` da simuliraš istek
- [ ] Refresh app → paywall opet aktivan

### 6.3 Zaboravljena lozinka

- [ ] Login → "Zaboravljena lozinka"
- [ ] Unesi email
- [ ] Reset email stiže
- [ ] Klik link → postavi novu lozinku
- [ ] Login s novom lozinkom

### 6.4 Multi-device test

- [ ] Login na laptopu — generiraj 1 dokument
- [ ] Login na telefonu (incognito) s **istim** emailom
- [ ] Pokušaj generirati — odmah paywall (jer je 1/1 iscrpljen na laptopu)

### 6.5 Brute-force registracija

- [ ] Pokušaj registrirati 5 puta isti email
- [ ] Trebao bi vidjeti "Korisnik već postoji"
- [ ] **Bonus test:** isti IP, 5 različitih emailova brzo
   - Trenutno nemaš rate limiting — dodaj kasnije ako bude problem

### 6.6 Pogrešna prijava

- [ ] Unesi pogrešnu lozinku 5 puta
- [ ] Supabase ima default rate limit (15 pokušaja u 1 min)
- [ ] Treba vidjeti "Too many requests" nakon nekog broja

### 6.7 GDPR delete request

- [ ] Korisnik traži brisanje (recimo emailom tebi)
- [ ] U Supabase Auth → Users → klik na usera → Delete
- [ ] Cascade delete obriše profil, subscriptions, usage_log za tog usera
- [ ] (LS subscription treba se zasebno otkazati u LS dashboard-u — ostaje samo data tamo)

---

## 7. ANALYTICS (OSNOVNA)

Bez Google Analyticsa — Supabase već ima sve podatke.

### 7.1 Korisni SQL upiti za dashboard

```sql
-- Broj registriranih
SELECT COUNT(*) AS total_users FROM auth.users;

-- Broj aktivnih pretplata
SELECT status, COUNT(*) FROM public.subscriptions GROUP BY status;

-- MRR (Monthly Recurring Revenue) — okvirni
SELECT
  variant_id,
  COUNT(*) AS subs,
  CASE
    WHEN variant_id LIKE '%weekly%' THEN COUNT(*) * 9.99 * 4
    WHEN variant_id LIKE '%monthly%' THEN COUNT(*) * 19.99
    WHEN variant_id LIKE '%yearly%' THEN COUNT(*) * 149 / 12
  END AS mrr_eur
FROM public.subscriptions
WHERE status = 'active'
GROUP BY variant_id;

-- Top 10 dokumenata po generaciji
SELECT document_type, COUNT(*) AS count
FROM public.usage_log
GROUP BY document_type
ORDER BY count DESC
LIMIT 10;

-- Conversion rate (registrirani vs plaćeni)
WITH stats AS (
  SELECT
    (SELECT COUNT(*) FROM auth.users) AS registered,
    (SELECT COUNT(DISTINCT user_id) FROM public.subscriptions WHERE status = 'active') AS paid
)
SELECT
  registered,
  paid,
  ROUND(100.0 * paid / NULLIF(registered, 0), 2) AS conversion_pct
FROM stats;

-- Korisnici koji su iscrpili free i nisu pretplaćeni (potencijalni upsell)
SELECT p.email, p.free_documents_used, p.created_at
FROM public.profiles p
LEFT JOIN public.subscriptions s ON s.user_id = p.id AND s.status = 'active'
WHERE p.free_documents_used >= 1 AND s.id IS NULL
ORDER BY p.created_at DESC;
```

### 7.2 Spremiti kao Saved Queries u Supabase

SQL Editor → Save query → naziv. Možeš ih opet pokrenuti jedan klik.

---

## 8. MIGRACIJA POSTOJEĆIH KORISNIKA (AKO IH IMAŠ)

Ako imaš `.users.json` s aktivnim korisnicima koje ne želiš izgubiti:

### 8.1 Skripta za migraciju

```python
# migracija_users.py — pokreni jednom, lokalno
import json
from supabase import create_client

SUPABASE_URL = "https://....supabase.co"
SUPABASE_SERVICE_KEY = "..."  # service_role key, NE anon

sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

with open(".users.json", "r", encoding="utf-8") as f:
    users = json.load(f)

for email, data in users.items():
    name = data.get("name", email)
    # Ne možemo prenijeti staru hashiranu lozinku (Supabase koristi drugi alg)
    # Šaljemo magic link da postave novu
    try:
        resp = sb.auth.admin.invite_user_by_email(email, {
            "data": {"full_name": name},
            "redirect_to": "https://{{STREAMLIT_APP_ID}}.streamlit.app",
        })
        print(f"Migrated: {email}")
    except Exception as e:
        print(f"Failed: {email} — {e}")
```

Korisnici dobivaju email "Postavite lozinku" i mogu nastaviti.

---

## 9. SLANJE PRVIH KORISNIKA (LAUNCH STRATEGY)

### 9.1 Soft launch (tjedan 1-2)

- 5-10 prijatelja / kolega
- "Probajte besplatno, recite mi što ne valja"
- Cilj: ulov bugove, ne novac

### 9.2 Targeted reach (tjedan 3-4)

- Facebook grupe: "Pravo i pravnici", "Mali poduzetnici Hrvatska", "Knjigovodstvo"
- LinkedIn: post u kojem dijeliš svoju priču
- Reddit r/croatia, r/programiranje
- Hacker News (s engleskim opisom + EN landing page)

### 9.3 Paid acquisition (tjedan 5+)

- Google Ads na pojmove: "tužba obrazac", "ovrha obrazac", "ugovor o radu predložak"
- Realan budget za testiranje: 200-500 EUR
- Mjeri konverziju: koliko ad klik košta vs koliko vrijedi pretplatnik

---

## 10. CIJENJE I PROMO STRATEGIJA

### 10.1 Launch promo

- **EARLY50** kupon: 50% popust na prvi mjesec
- Komuniciraj kao "Prvih 100 korisnika"
- Stvara hitnost

### 10.2 Refund policy

Jasno u Terms:
> Korisnik može tražiti puni povrat unutar **14 dana** ako **nije generirao niti jedan dokument iza pretplate**. Nakon prvog generiranja, refund nije moguć (jer je usluga iskorištena).

### 10.3 Anti-churn (zadržavanje)

- Email "Vaša pretplata istječe za 3 dana, kliknite za nastavak"
- Win-back email otkazanim: "Vratite se s 30% popustom" (mjesec dana nakon otkaza)
- LS automatski šalje neke od ovih, ali zna se prilagoditi

---

## 11. PODRŠKA KORISNICIMA

### 11.1 Email kanal

- **support@tvoja-domena.hr** ili Gmail "legalsuite.support@gmail.com"
- Ostavi u footer-u i u svim email template-ovima

### 11.2 Help / FAQ stranica

- "Kako otkazati pretplatu?" → preusmjeri na LS customer portal
- "Račun za moju tvrtku?" → LS to radi automatski preko checkout-a (kupac unosi VAT ID)
- "Treba mi dokument koji nemate?" → pošaljite email, dodajemo top requestane

### 11.3 Response time

Solo dev: 24h response time je razumno. Komuniciraj to.

---

## 12. FINALNI PRE-LAUNCH CHECKLIST

```
[ ] Obrt registriran, IBAN otvoren, LS verificirao
[ ] Supabase schema deploya, RLS aktiviran
[ ] Edge Function deployan i testiran
[ ] LS proizvodi kreirani, webhook spojen
[ ] Streamlit secrets popunjeni (lokalno + Cloud)
[ ] auth.py refaktoriran, billing.py kreiran, paywall integriran
[ ] Privacy Policy + Terms uploaded
[ ] Cookie banner u app-u
[ ] Custom SMTP postavljen (Resend)
[ ] Email templates uređeni
[ ] Sve test scenarije prošle
[ ] Demo video snimljen (1-2 min, kako se radi tužba)
[ ] Posljednja promjena commitana i deployana
[ ] Live URL otvoren incognito i isproban od početka do kraja
```

---

## 13. ŠTO AKO NEŠTO PUKNE NA PRODUKCIJI

### 13.1 Sažetak fixova

| Problem | Brzo rješenje |
|---------|---------------|
| Korisnik se ne može prijaviti | Provjeri Supabase status (status.supabase.com) |
| Plaćanje prošlo, ali nema pristupa | Provjeri Edge Function logs, ako je failed → ručno UPSERT u subscriptions |
| Cijela app vraća "Internal error" | Streamlit Cloud "Reboot app" iz dashboarda |
| Webhook ne stiže | LS Settings → Webhooks → klik na webhook → vidiš history; ako stalno fail-a → reboot Edge Function (`supabase functions deploy`) |
| User žali se na sporo učitavanje | Streamlit Cloud spava, prvi pristup nakon dugog mirovanja je 30s; reboot ili upgrade na Team plan |

### 13.2 Status page (kasnije)

Kad imaš stabilnu bazu korisnika — postavi `status.tvoja-domena.hr` da pokaže uptime svake komponente. **statusgator.com** ima besplatan plan.

---

## SLJEDEĆI KORAK

Otvori `10_NAKON_LANSIRANJA.md` — što pratiti, kad skalirati, kad mijenjati cijene.
