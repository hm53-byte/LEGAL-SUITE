# 10 — NAKON LANSIRANJA: ŠTO PRATITI, KAD SKALIRATI, KAD MIJENJATI

> Aplikacija je živa. Sad si u "operate" fazi. Ovaj dokument kaže **na što obraćati pažnju** prvih 6 mjeseci, kad se vrijedi nešto mijenjati, i kad razmišljati o sljedećoj fazi (eksterno financiranje, prodaja).

---

## 1. KLJUČNI METRIČKI POJMOVI

Naučit ćeš ih jer ćeš ih čuti svakim novim prijateljem-investitorom-konkurentom.

| Pojam | Što znači | Cilj za tvoju app (1. godina) |
|-------|-----------|--------------------------------|
| **MAU** (Monthly Active Users) | Korisnici koji su barem jednom otvorili app u 30 dana | 500-2.000 |
| **Conversion rate** | % registriranih → plaćenih | 3-7% (industry avg za SaaS) |
| **MRR** (Monthly Recurring Revenue) | Mjesečni ponavljajući prihod | 1.000-5.000 EUR |
| **ARR** (Annual Recurring Revenue) | MRR × 12 | 12-60k EUR |
| **Churn rate** | % korisnika koji otkažu mjesečno | <8% (dobro), <5% (odlično) |
| **LTV** (Lifetime Value) | Koliko prosječan korisnik plati u ukupnom životu | 60-200 EUR |
| **CAC** (Customer Acquisition Cost) | Koliko košta dobiti 1 plaćenog korisnika | <30 EUR |
| **LTV:CAC ratio** | LTV / CAC | >3 (zdravo) |
| **Payback period** | Koliko mjeseci treba da se CAC isplati | <12 mj |

---

## 2. SVAKODNEVNI MONITORING (5 MIN/DAN)

Svaki dan ujutro:

### 2.1 Supabase dashboard

- **Auth → Users:** koliko novih registracija jučer?
- **SQL Editor → saved query:** "MRR + churn ovog tjedna"
- **Edge Functions → Logs:** ima li grešaka u zadnjih 24h?

### 2.2 Lemon Squeezy dashboard

- **Dashboard:** today's revenue
- **Subscriptions:** koliko novih, koliko otkazanih
- **Failed payments:** kartice odbijene? (Treba intervencija)

### 2.3 Streamlit Cloud

- **App → Logs:** error rate
- **App → Analytics:** pageviews, sessions

---

## 3. TJEDNI REVIEW (30 MIN/TJEDAN)

Petak navečer ili nedjelja:

### 3.1 Pitanja za sebe

1. **Conversion rate ovaj tjedan?** Ako pada → zašto? (Bug? Konkurencija?)
2. **Churn ovaj tjedan?** Ako raste → kontaktiraj otkazane, pitaj zašto
3. **Top 3 dokumenta po generaciji?** → fokusiraj UX poboljšanja na njih
4. **Failed payments?** → kontaktiraj korisnike, pomozi
5. **Support tickets?** → koje pitanja se ponavljaju? Stavi u FAQ

### 3.2 Cohort analiza

```sql
-- Konverzija po tjednu registracije
WITH cohorts AS (
  SELECT
    DATE_TRUNC('week', created_at) AS cohort_week,
    id AS user_id
  FROM auth.users
)
SELECT
  c.cohort_week,
  COUNT(DISTINCT c.user_id) AS registered,
  COUNT(DISTINCT s.user_id) AS converted,
  ROUND(100.0 * COUNT(DISTINCT s.user_id) / COUNT(DISTINCT c.user_id), 2) AS pct
FROM cohorts c
LEFT JOIN public.subscriptions s ON s.user_id = c.user_id AND s.status IN ('active', 'cancelled', 'expired')
GROUP BY c.cohort_week
ORDER BY c.cohort_week DESC
LIMIT 12;
```

Vidiš li trendove? Promo kampanja u tjednu X dignula konverziju? UI promjena pomogla?

---

## 4. MJESEČNI REVIEW (2-3H/MJESEC)

Prvi tjedan u mjesecu:

### 4.1 P&L (Profit & Loss)

| Stavka | EUR |
|--------|-----|
| Bruto prihod (LS gross sales) | XXXX |
| - LS fee (5% + 0.50/tx) | -XXX |
| - VAT (LS već platio kupcima' zemljama) | (već odvojeno) |
| **Net prihod od LS** | XXXX |
| - Doprinosi obrta | -260 |
| - Knjigovođa | -40 |
| - Domain + email | -10 |
| - Marketing (Google Ads + ostalo) | -XXX |
| - Supabase (kad pređeš free) | -25 |
| **Net dobit** | XXXX |

Ako je net dobit pozitivan već 3-6 mjeseci → razmisli o reinvestu (više marketing, freelance dizajner, dodatne značajke).

### 4.2 Customer interviews (PRESUDNO!)

**Posveti 1-2h mjesečno na razgovor s 5 korisnika.** Ne survey, **video razgovor**. Pitaj:
- Što ti je bilo najteže?
- Koji dokument si pokušao a nismo imali?
- Što bi te natjeralo da otkažeš?
- Što bi te natjeralo da preporučiš prijateljima?

**Ovo je najvrjedniji input za roadmap.** Više nego bilo kakav analytics.

---

## 5. KAD MIJENJATI CIJENE

### 5.1 Crveni signali (cijena prevelika)

- Conversion rate <1% nakon 1.000+ posjeta
- Mnogi otkažu odmah nakon prve naplate
- Komentari "preskupo" u feedback-u

→ **Sniži cijenu** ili uvedi tier nižu (npr. 4,99/tjedno za "Basic" s manje funkcija).

### 5.2 Zeleni signali (cijena premala)

- Conversion 10%+
- Niski churn
- Korisnici sami sugeriraju "garancije, dodatne usluge, premium support"

→ **Diži cijenu** (npr. mjesečna 24,99 umjesto 19,99). **Postojećim korisnicima ostavi staru cijenu** — to se zove "grandfathering" i jako poboljšava lojalnost.

### 5.3 Kako sigurno povećati cijenu

1. Najavi korisnicima 30 dana unaprijed: "Cijene rastu od 1. lipnja"
2. Postojeći ostaju na staroj **dok imaju aktivnu pretplatu**
3. Daj im opciju da plate **godišnju po staroj** prije promjene → upselling
4. Novi korisnici od datuma X plaćaju novu cijenu

LS to podržava preko više **Variants** istog Producta.

---

## 6. KAD DODATI NOVE ZNAČAJKE

### 6.1 Pravilo 70/20/10

- **70%** vremena: poboljšaj postojeće (bug fixes, UX, performance)
- **20%** vremena: nove značajke koje korisnici eksplicitno traže (3+ neovisna zahtjeva)
- **10%** vremena: eksperimentalne ideje (ne ulaganje u produkciju dok ne potvrde)

### 6.2 Što NE raditi

- **Ne dodaji značajku jer je ti misliš cool** — testiraj prvo s 5 korisnika
- **Ne preselit na novi tech stack** (npr. React) dok stvarno ne udari u zid
- **Ne klonarati konkurente bez razloga** — diferencijacija je vrjednija od parity-a

### 6.3 Pristup novim dokumentima

Imaš već 60+ generatora. Roadmap za nove (vidi `RAZVOJ_PRIJEDLOZI.md`):
- Aneks ugovora o radu (Prioritet 1 u tvojoj listi)
- Drustveni ugovor d.o.o.
- NDA

**Prije nego dodaš novi dokument:**
1. Pretraži `usage_log` — koji dokumenti se traže ali ne postoje? (možeš to znati ako kreiraš "Predloži novi dokument" formu i logiraš)
2. Pitaj 3 stvarna korisnika: "Bi li ovo koristio? Koliko puta godišnje?"
3. Estimate koliko sati treba (~4-8h za novi generator)

---

## 7. KAD POVEZATI PRAVU DOMENU

Default Streamlit URL je ružan: `https://legal-suite-flh3jnmcj5kc7jp5y9w9eb.streamlit.app`.

### 7.1 Kupi domenu

- **Namecheap, Porkbun, Cloudflare:** ~10 EUR/godinu za .hr je teže (oko 30 EUR/g, treba HR rezident), .com je 12 EUR/g
- Preporučujem: `legalsuite.hr` ili `pravnitemplati.hr` ili `dokpraktik.hr`

### 7.2 Custom domain na Streamlit Community Cloud

**Problem:** Community Cloud **NE podržava** custom domains. Trebaš upgrade na **Team plan** (~100 USD/mj) ili migrirati.

**Bolje rješenje za sad:** koristi **Cloudflare Tunnel** ili **Vercel reverse proxy** da prosljeđuje `legalsuite.hr` na tvoj Streamlit URL. Free, 30 min posla.

### 7.3 Email na vlastitoj domeni

- Cloudflare Email Routing (free): `info@legalsuite.hr` → forward na tvoj Gmail
- Ili Google Workspace: 6 EUR/mj po mailboxu (više profesionalno)

---

## 8. KAD MIGRIRATI SA STREAMLITA

Streamlit je odličan za MVP. Ali ima limitacije:

### 8.1 Crveni signali za migraciju

- Korisnici žale se na sporo učitavanje (cold starts)
- Više od 1.000 simultanih korisnika (Streamlit Cloud limit)
- Trebaš stvarni mobile UI (Streamlit nije optimiziran za mobile)
- Trebaš real-time funkcije (chat, notifikacije)

### 8.2 Što umjesto Streamlita

- **Next.js + Tailwind + Supabase** — moderni full-stack JS
- **Astro + React** ako trebaš heavy SEO
- **Django** ako želiš ostati u Pythonu sa pravim backendom

**Migracija je puno posla** (1-3 mjeseca). Ne radiš to dok ne udari u zid.

### 8.3 Hybrid pristup

Možeš ostaviti **generaciju dokumenata** u Streamlitu (jer radi), a dodati **marketing site + login + dashboard** u Next.js. Streamlit je ugnijezden u iframe ili linka iz dashboarda. Postupna migracija.

---

## 9. KAD POVEĆATI TIM

### 9.1 Prvi vanjski suradnici (kad MRR > 2k EUR/mj)

- **Knjigovođa:** ako još nemaš → uzmi (60-100 EUR/mj)
- **Freelance dizajner:** za UI redizajn jednom (~500-1500 EUR jedanput)
- **Pravni savjetnik:** kad ti dođe prva pravna primjedba (refund spor, GDPR upit) — uzmi odvjetnika za ad-hoc 1-2 sata

### 9.2 Prvi virtualni asistent (kad MRR > 5k EUR/mj)

- Email podrška, FAQ ažuriranje, social media → 5-10h/tj VA = 200-400 EUR/mj
- Upwork, OnlineJobs.ph (filipinski VA su jeftini i kvalitetni za EN podršku; za HR podršku traži lokalno na Indeed/JobAdriatic)

### 9.3 Prvi tehnički zaposlenik (kad MRR > 10k EUR/mj)

- Junior dev / full stack za ~1.500-2.500 EUR/mj
- Treba ti freelance-on-retainer ili part-time

---

## 10. KAD RAZMIŠLJATI O EKSTERNOM KAPITALU

**Većini SaaS-a u tvom segmentu (HR pravo) — eksterni kapital nije potreban.** Lako bootstrapaš do 10-20k EUR MRR.

**Razmotri vanjsko ulaganje samo ako:**
- Imaš stvarno veliku ambiciju (regija EU, više od HR)
- Konkurent dobije ulaganje pa moraš accelerirati
- Vidiš veliku tržišnu mogućnost koja se zatvara (npr. EU zakon koji presudno mijenja pravila)

**Tipovi:**
- **Bootstrap** (no investicija) — najjednostavnije, najveća kontrola
- **Friends & Family round** (5-50k EUR) — od najbližih
- **Angel investment** (50-200k EUR) — pojedinci s biznis iskustvom
- **VC seed round** (200k-1M EUR) — pretjerano za tvoj segment

**HR opcije:** South Central Ventures, Fil Rouge Capital, Croatian Venture Fund. Svi traže "big market" — pravne usluge u HR vjerojatno premali za njih.

**Bolji put za tebe:** organic growth + eventually exit ili strategic sale.

---

## 11. KAD PRODATI APLIKACIJU

Vraćamo se na pitanje s početka.

### 11.1 Crveni signali da ti je vrijeme za exit

- Ne uživaš više raditi na njoj
- Imaš drugi projekt koji te više zanima
- Veliki ponuđač pojavljuje se s konkretnom ponudom
- Stigao si do plafona koji ne možeš sam preći

### 11.2 Realna vrijednost (multiple od ARR)

| Faza | Multiple | Primjer |
|------|----------|---------|
| Prototip, malo korisnika | 1-3× ARR | 10k ARR → 10-30k EUR |
| 6-12 mjeseci traction | 3-5× ARR | 50k ARR → 150-250k EUR |
| Profitabilna 1+ godina, niski churn | 5-8× ARR | 100k ARR → 500-800k EUR |
| Strategic acquisition (IUS-INFO ima sinergiju) | može +50% | 100k ARR → 1M EUR |

### 11.3 Tipovi exit-a

- **Asset sale:** kupnja koda, korisnika, brand-a u jednom paketu. Najčešće.
- **Stock sale:** ako imaš tvrtku (j.d.o.o.), kupac kupuje udjele. Komplicirano za solo dev.
- **Acqui-hire:** kupac primarno želi tebe kao zaposlenika, app je bonus
- **Earnout:** dio cijene unaprijed, dio kroz 1-3 godine ovisno o budućoj performansi

### 11.4 Realan target za prvi exit

- 12-18 mjeseci konzistentnog rasta
- 10-30k EUR ARR
- 100-500 plaćenih korisnika
- 5-10% mjesečni rast
- <8% mjesečni churn

S tim → realna ponuda u rasponu **30-150k EUR** od strategic buyera (IUS-INFO, NN, akumulator startup-a poput Constellation Software-a EU divizije).

---

## 12. ŠTO NE RADITI (TIPIČNE GREŠKE)

1. **Premature optimization** — ne radi load balancer prije nego imaš 1000 korisnika
2. **Feature creep** — ne dodavaj značajke bez signala iz korisnika
3. **Premature international expansion** — fokus na HR + RH dijaspora prvih 12 mj
4. **Ignoriranje churn-a** — bolje je zadržati 1 starog nego dobiti 1 novog
5. **Ne komunicirati s korisnicima** — solo dev koji se sakriva ne raste
6. **Ovisnost o jednom kanalu** — ako ti Google Ads padne, sve pada
7. **Pretjerano diskontiranje** — 80% off promo signaling "očajan sam"
8. **Pomaganje besplatno previše dugo** — postavi granice, ne radi 12h podršku za 9.99 EUR/tj korisnika

---

## 13. RESURSI ZA DALJNJI RAST

### 13.1 Knjige

- **"Hooked"** by Nir Eyal — habit-forming products
- **"Lean Startup"** by Eric Ries — MVP, validated learning
- **"Traction"** by Gabriel Weinberg — 19 marketing channels
- **"From Impossible to Inevitable"** by Aaron Ross — repeatable sales

### 13.2 Online resursi

- **Indie Hackers** (indiehackers.com) — solo founder community
- **r/SaaS, r/Entrepreneur** na Reddit-u
- **MicroConf** — konferencija za bootstrapped SaaS founders

### 13.3 HR specifično

- **Startups.hr** — lokalna scene
- **Croatian Founders** Slack/Discord grupa
- **CISEx** (Croatian Investors Network)

---

## 14. ZAVRŠNA RIJEČ

Imaš **20.000 linija koda** koji rješava stvarni problem. To je više nego što većina ljudi ikad napravi. Većina solo SaaS-a ne preživi prvu godinu zbog:

1. **Loše distribucije** (nitko ne sazna za njih)
2. **Loše naplate** (nikako ne pretvaraju u plaćeno)
3. **Loše pravne baze** (kazne ih razbiju)

Ovaj plan adresira svih troje. Ako ga slijediš → imaš realne šanse za održiv mali biznis (1-5k EUR/mj net) unutar 12 mjeseci.

**Ako se to ne dogodi — i dalje imaš kvalitetan portfolio projekt + iskustvo + opciju prodaje.**

Ne podcjenjuj nijedno od toga.

---

## SLJEDEĆI KORACI

1. Pročitaj cijeli ovaj plan još jednom (svih 10 dokumenata)
2. Otvori `01_PRAVNI_OKVIR.md` i kreni s registracijom obrta
3. Tek kad obrt bude gotov → ide tehnička implementacija
4. Postavi sebi 2-mjesečni rok za "live s prvim plaćenim korisnikom"
5. Javi ako zapneš na bilo kojem koraku

**Sretno.**
