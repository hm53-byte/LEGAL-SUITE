# LegalTech Suite Pro — Plan rasta tržišne vrijednosti

> Datum: 2026-03-17
> Trenutno stanje: Pre-revenue, Streamlit Community Cloud, 0 korisnika, 0 MRR
> Procjena trenutne vrijednosti: $0–$2,000 (samo kod + ideja)

---

## 1. TRENUTNO STANJE (Brutalno iskreno)

| Metrika | Vrijednost |
|---------|-----------|
| MRR | $0 |
| Korisnici koji plaćaju | 0 |
| Ukupni korisnici | 0 (osim tebe) |
| Hosting | Streamlit Community Cloud (besplatno, ograničenja za komercijalnu upotrebu) |
| API integracije | 0 |
| Vanjski izvori podataka | 0 (sve je hardkodirano — sudovi, pristojbe) |
| SEO prisutnost | 0 |
| IP zaštita | 0 (nema zaštitnog znaka, nema patenta) |
| Dokumentacija za kupce | 0 |
| Recurring revenue mehanizam | Ne postoji |

### Što aplikacija JEST danas:
- 60+ generatora pravnih dokumenata (DOCX) za 15 pravnih područja
- Baza 74 hrvatska suda
- Kalkulator pristojbi i kamata
- OIB validacija (ISO 7064)
- Vodič za neuke korisnike
- Kvalitetan kod (129 testova, modularna arhitektura)

### Što aplikacija NIJE:
- Ne vuče nikakve podatke izvana (zakoni, sudske odluke, registri)
- Nema AI/LLM komponentu
- Nema autentikaciju ni korisničke račune
- Nema plaćanje
- Nema analitiku korištenja
- Nema SEO, nema landing page, nema marketing

---

## 2. TRŽIŠNI KONTEKST

### Globalno LegalTech tržište
- **2026.:** 38.1 milijardi USD
- **2036.:** 78.1 milijardi USD (CAGR 7.6%)
- CLM (upravljanje ugovorima) raste 19.12% godišnje do 2030.
- SME segment raste 17.15% godišnje

### Hrvatsko tržište — PRAZNINA
- **~5,500 odvjetnika** (HOK)
- **~360 javnih bilježnika**
- **~240,000 aktivnih tvrtki** (99.8% su SME, 92.1% mikro-poduzeća)
- **~550,000–670,000 sudskih predmeta godišnje**
- **109 zemljišnoknjižnih odjela**

### Konkurencija u Hrvatskoj
| Konkurent | Što nudi | Opseg | Cijena |
|-----------|---------|-------|--------|
| **eOvrhe.hr** | Automatizacija ovršnih dokumenata | Samo ovrhe | Besplatna registracija + ? |
| **JusticeFusion** | AI pravni asistent (HR/BiH/SR) | Širok, AI-baziran | Enterprise (kontakt) |
| **e-Odvjetnik.hr** | Marketplace za odvjetnike | Spajanje klijenata s odvjetnicima | Per-usluga |
| **Legal-IS** | Upravljanje odvjetničkim uredom | Interno za urede | Pretplata |
| **LegalTech Suite Pro** | Generator 60+ dokumenata | Najširi opseg dokumenata | $0 (još nema) |

**Zaključak:** Nijedna hrvatska tvrtka ne nudi self-service generator pravnih dokumenata širokog spektra. eOvrhe pokriva samo ovrhe. JusticeFusion je AI ali ciljaju enterprise. PRAZNINA JE REALNA.

### Regionalna ekspanzija (potencijal)
- **Slovenija:** PravniDokumenti.si (samo ugovori)
- **Srbija:** Draftomat (enterprise, BDK Advokati spin-off)
- **BiH:** JusticeFusion pokriva, ali nema self-service alat
- Jezične i zakonske sličnosti omogućuju ekspanziju uz umjerene prilagodbe

### Pricing benchmarci
| Tržište | Servis | Model | Cijena |
|---------|--------|-------|--------|
| US | Rocket Lawyer | Pretplata | $39.99/mj |
| US | LegalZoom | Per-dokument + pretplata | $59/dok ili $99/mj |
| US | LawDepot | Pretplata | $8.99/mj (godišnje) |
| EU | Documentify | Pretplata | $35/mj |
| **HR (preporučeno)** | **LegalTech Suite Pro** | **Freemium** | **Besplatno / 10–25 EUR/mj Pro / 50–100 EUR/mj Business** |

---

## 3. DOSTUPNI JAVNI API-JI (BESPLATNI!)

Ovo je ključna prednost — hrvatska država ima **4 besplatna javna API-ja** koja nitko ne koristi u kontekstu LegalTech-a:

### 3.1. e-Oglasna ploča sudova (REST API)
- **URL:** https://e-oglasna.pravosudje.hr/
- **API dokumentacija:** https://e-oglasna.pravosudje.hr/dokumenti/api
- **Spec:** OpenAPI YAML (`e-oglasna_API_v1.yaml`)
- **Podaci:** Elektroničke oglasne ploče svih sudova, FINA-e, javnih bilježnika
- **Licenca:** Otvorena (open data, CKAN: data.gov.hr)
- **Auth:** Provjeriti YAML spec (vjerojatno bez)
- **Integracija:** LAKA — REST API, otvoreni podaci
- **Vrijednost za korisnike:** Pretraga sudskih objava, praćenje ovrha, stečajeva, dražbi

### 3.2. e-Predmet — Praćenje sudskih predmeta (GraphQL API)
- **Endpoint:** `https://e-predmet.pravosudje.hr/api/`
- **Schema:** `https://e-predmet.pravosudje.hr/api/schema.graphql`
- **Upiti:**
  - `Courts` — lista sudova s ID-jevima
  - `Case` — detalji predmeta po broju i sudu
- **Osvježavanje:** Jednom dnevno (preporučeno dohvaćanje 01:00–05:00)
- **Auth:** Nema (javni pristup)
- **Integracija:** LAKA — GraphQL, bez registracije
- **Vrijednost za korisnike:** Praćenje statusa svojih predmeta, provjera dodijeljenog suca, povijest postupka

### 3.3. Narodne novine — ELI/JSON-LD (Zakonski tekstovi)
- **URL:** https://narodne-novine.nn.hr/
- **ELI URL format:** `https://narodne-novine.nn.hr/eli/sluzbeni/{god}/{broj}/{id}`
- **Formati:** RDFa (HTML), RDF/XML (`/rdf`), JSON-LD (`/json-ld`)
- **Pretraga:** Full-text s boolean izrazima
- **Rate limit:** 3 zahtjeva/sekundi
- **Auth:** Nema
- **Integracija:** SREDNJA — treba parser za ELI, ali dobro dokumentirano
- **Vrijednost za korisnike:** Automatske reference na zakone, linkovi na NN članke u generiranim dokumentima, provjera važećih propisa

### 3.4. Sudski registar — Podaci o tvrtkama (REST API + OAuth2)
- **URL:** https://sudreg-data.gov.hr/
- **OpenAPI:** https://sudreg-data.gov.hr/api/OpenAPIs/OpenAPIJavni
- **Auth:** OAuth2 client_credentials (besplatna registracija)
- **Endpoint:** `GET /api/javni/detalji_subjekta` (po OIB-u ili MBS-u)
- **Podaci:** Naziv tvrtke, sjedište, OIB, MBS, zastupnik
- **Token:** Valjan 6 sati
- **Integracija:** SREDNJA — OAuth2 flow, ali dobro dokumentirano
- **Vrijednost za korisnike:** Auto-popunjavanje podataka o pravnim osobama po OIB-u/MBS-u — umjesto ručnog unosa, unesi OIB i svi podaci se povuku automatski

### Nedostupni servisi (zahtijevaju NIAS/FINA certifikat):
- **e-Komunikacija sa sudovima** — zatvoreni sustav, nema API-ja
- **Zemljišne knjige (OSS)** — nema API-ja, NIAS za puni pristup
- **FINA/RGFI** — web sučelje, FINA certifikat, zabranjena redistribucija podataka

---

## 4. FAZA 1 — VALIDACIJA (0–3 mjeseca)

**Cilj:** Dokazati da netko želi platiti. Skupiti 10 plaćajućih korisnika.

### 4.1. Infrastruktura (Tjedan 1–2)
- [ ] **Preseli hosting s Streamlit Community Cloud**
  - Opcije: Railway ($5/mj), Render (free tier + $7/mj), DigitalOcean ($5–12/mj)
  - Streamlit CC ima ograničenja za komercijalnu upotrebu
  - Potreban je vlastiti domena (npr. legalsuite.hr — provjeri dostupnost)
- [ ] **Dodaj Google Analytics / Plausible**
  - Prati koliko ljudi koristi aplikaciju, koje module, conversion rate
  - Plausible je GDPR-compliant, open source, self-hosted opcija
- [ ] **Landing page s SEO**
  - Svaka pravna kategorija dobije svoju stranicu s meta opisom
  - Target ključne riječi: "generator pravnih dokumenata", "obrazac za tužbu", "opomena pred tužbu obrazac", "žalba na rješenje ZUP"
  - Blog sekcija: pisati članke o pravnim postupcima (SEO + autoritet)

### 4.2. Prva API integracija — Sudski registar (Tjedan 2–4)
- [ ] **Registriraj se na sudreg-data.gov.hr** (besplatno)
- [ ] **Implementiraj OAuth2 client_credentials flow**
- [ ] **Dodaj "Pretraži tvrtku" gumb u `unos_stranke()` za pravne osobe**
  - Korisnik unese OIB ili MBS → API povuče: naziv, sjedište, OIB, MBS, zastupnik
  - Auto-popuni sva polja za pravnu osobu
  - Ogromna ušteda vremena za korisnike
- [ ] **Cache rezultate** (6 sati, koliko traje token)

### 4.3. Druga API integracija — e-Predmet (Tjedan 4–6)
- [ ] **Implementiraj GraphQL klijent** za `https://e-predmet.pravosudje.hr/api/`
- [ ] **Novi modul: "Praćenje predmeta"**
  - Korisnik unese broj predmeta + odabere sud → prikaži status, suca, povijest
  - Ovo ne postoji nigdje kao dio LegalTech alata
- [ ] **Integriraj s generatorima:** kad korisnik ima aktivan predmet, ponudi relevantne dokumente

### 4.4. Treća API integracija — Narodne novine (Tjedan 6–8)
- [ ] **Implementiraj NN ELI parser** (JSON-LD format)
- [ ] **Dodaj linkove na zakone u generiranim dokumentima**
  - Kad dokument referencira "čl. 225. ZOO", generiraj link na NN
  - Poveži s bazom propisa: ZOO, ZPP, Ovršni zakon, ZTD, Obiteljski zakon, ZUP, ZUS
- [ ] **Modul "Pretraga zakona"** — full-text pretraga NN-a iz aplikacije
- [ ] **Poštuj rate limit: 3 req/s** (implementiraj token bucket)

### 4.5. Monetizacija (Tjedan 4–8)
- [ ] **Stripe integracija** (ili Braintree za HR)
  - Stripe podržava hrvatske tvrtke od 2023.
  - Alternativa: Monri (hrvatski payment gateway)
- [ ] **Freemium model:**
  - **Free:** 3 dokumenta mjesečno, osnovni generatori, vodič
  - **Pro (15–25 EUR/mj):** Neograničeni dokumenti, API integracije (sudski registar, e-Predmet), DOCX watermark uklonjen, prioritetna podrška
  - **Business (50–100 EUR/mj):** Bulk generiranje, višekorisnički pristup, API pristup, custom branding
- [ ] **Implementiraj auth (Streamlit-Authenticator ili vlastiti)**
  - Email + lozinka za početak
  - Kasnije: OAuth2 (Google login), NIAS (e-Građani)

### 4.6. Beta korisnici (Tjedan 6–12)
- [ ] **Ciljaj 10 beta korisnika:**
  - Manji odvjetnički uredi (1–3 odvjetnika) — trebaju efikasnost
  - HR odjeli malih tvrtki — trebaju ugovore o radu, otkaze
  - Udruge za zaštitu prava — trebaju žalbe, prijave
  - Računovodstveni servisi — trebaju osnivačke akte, odluke
- [ ] **Ponudi prvu godinu po sniženoj cijeni** (50% popust za early adopters)
- [ ] **Skupljaj feedback aktivno** — Intercom, email, ankete

---

## 5. FAZA 2 — RAST (3–12 mjeseci)

**Cilj:** $500–$2,000 MRR

### 5.1. e-Oglasna ploča — Četvrta API integracija
- [ ] **Dohvati API spec** (`e-oglasna_API_v1.yaml`)
- [ ] **Novi modul: "Sudske objave"**
  - Pretraga objava po sudu, tipu, datumu
  - Praćenje specifičnih objava (notifikacije)
  - Filtriranje: ovrhe, stečajevi, dražbe, dostave
- [ ] **Alert sustav:** Email/push kad se pojavi objava koja odgovara kriterijima korisnika
  - Npr. "Obavijesti me kad se objavi dražba nekretnine u Splitu"
  - Ovo je PREMIUM feature koji sam po sebi opravdava pretplatu

### 5.2. AI komponenta (LLM integracija)
- [ ] **Dodaj AI pravnog asistenta**
  - Claude API ili OpenAI API za analizu pravnih situacija
  - Fine-tune na hrvatskim zakonima (NN podaci)
  - **Ključna funkcionalnost:** Korisnik opisuje situaciju → AI analizira → predlaže dokumente → generira
  - Disclaimer: "Ovo nije pravni savjet. Za kompleksne situacije konzultirajte odvjetnika."
- [ ] **AI-asistirana popuna obrazaca**
  - Korisnik opisuje situaciju slobodnim tekstom → AI izvlači podatke → popuni obrazac
  - Npr. "Dužnik mi duguje 5000 EUR od 15.3.2024., poslao sam opomenu ali nije platio"
    → AI popuni: VPS=5000, datum=15.03.2024., tip=tužba za naplatu
- [ ] **RAG sustav s bazom zakona**
  - Vektorska baza s NN tekstovima
  - AI odgovara na pravna pitanja s citatima zakona

### 5.3. Content marketing + SEO
- [ ] **Blog (min 2 članka tjedno):**
  - "Kako napisati opomenu pred tužbu — vodič za 2026."
  - "Žalba na rješenje ZUP — rok, sadržaj, primjer"
  - "Ovrha putem javnog bilježnika — postupak korak po korak"
  - "Ugovor o radu 2026. — što mora sadržavati"
- [ ] **YouTube kanal** — video vodiči za pravne postupke
- [ ] **Social media:** LinkedIn (B2B), Facebook grupe za poduzetnike
- [ ] **SEO optimizacija:**
  - Svaki modul = zasebna URL stranica (trenutno je SPA)
  - Meta tagovi, structured data (LegalService schema.org)
  - Google Business Profile

### 5.4. Napredne features
- [ ] **Višekorisnički pristup** (za odvjetničke urede)
  - Timski account, zajedničko spremanje dokumenata
  - Role-based access: admin, odvjetnik, asistent
- [ ] **Povijest dokumenata**
  - Spremanje generiranih dokumenata u korisnički profil
  - Verzioniranje, ponovni pristup
- [ ] **E-potpis integracija**
  - FINA e-Potpis (kvalificirani elektronički potpis)
  - Ili SimplSign/DocuSign za nekvalificirane potpise
- [ ] **Email dostava dokumenta**
  - Generiraj → potpiši → pošalji — sve iz jednog sučelja

---

## 6. FAZA 3 — SKALIRANJE (12–24 mjeseca)

**Cilj:** $5,000+ MRR, priprema za exit ili dugoročni prihod

### 6.1. B2B pivot
- [ ] **Odvjetnički uredi** — paketi po broju odvjetnika
- [ ] **Javni bilježnici** — specijalizirani moduli za JB postupke
- [ ] **Računovodstveni servisi** — integracija s fakturiranjem
- [ ] **Sindikati** — bulk generiranje za članove
- [ ] **White-label** — brandirana verzija za odvjetničke komore

### 6.2. API pristup (PaaS model)
- [ ] **LegalTech Suite API**
  - REST API za generiranje dokumenata programski
  - Drugi developeri / platforme mogu koristiti tvoj engine
  - Pay-per-call model: 0.10–0.50 EUR po generiranom dokumentu
- [ ] **Webhook notifikacije** — za integraciju s CRM-ovima

### 6.3. Regionalna ekspanzija
- [ ] **Slovenija** — prilagodba za slovenski ZUP, ZPP, OZ
  - Jezik sličan ali različit — treba prijevod
  - Pravni sustav sličniji njemačkom — značajne prilagodbe
- [ ] **Srbija** — najlakša ekspanzija
  - Isti jezik (ćirilica + latinica)
  - Slični zakoni (zajedničko jugoslavensko naslijeđe)
  - Tržište: ~7M ljudi, ~30,000 odvjetnika
- [ ] **Bosna i Hercegovina** — kompleksno (entitetski zakoni)
  - RS i FBiH imaju različite zakone
  - Ali jezično identično

### 6.4. Partnerstva i ugovori
- [ ] **Ministarstvo pravosuđa** — digitalizacijski projekti
  - Hugo.legal (Estonija) dobio 3.5M EUR gov ugovor
  - Hrvatska ima Nacionalni plan oporavka s komponentom digitalizacije pravosuđa
- [ ] **Odvjetnička komora (HOK)** — preporučeni alat za članove
- [ ] **Pravni fakulteti** — edukacijski alat za studente

---

## 7. PROCJENA VRIJEDNOSTI PO FAZAMA

| Faza | Mjesec | MRR | Godišnji prihod | Procjena (4–6x ARR) |
|------|--------|-----|-----------------|---------------------|
| Sad | 0 | $0 | $0 | $0–$2K (samo kod) |
| Validacija | 3 | $100–200 | $1,200–2,400 | $5K–$15K |
| Rani rast | 6 | $500 | $6,000 | $24K–$36K |
| Rast | 12 | $2,000 | $24,000 | $96K–$144K |
| Skaliranje | 24 | $5,000+ | $60,000+ | $240K–$360K+ |

### Multiplikatori za exit
- SaaS s niskim churnom: 4–10x ARR
- SaaS s AI komponentom: 6–15x ARR
- Nišni tržišni lider (Hrvatska): premium od 20–50% jer nema konkurencije
- Acqui-hire: +$50K–$100K za tim/znanje

---

## 8. PLATFORME I KUPCI ZA EXIT

### Gdje prodati
- **Acquire.com** — vodeća platforma za SaaS akvizicije (500M+ USD transakcija). Besplatno za prodavače.
- **Microns.io** — specijaliziran za micro-SaaS ($1K–$50K dealovi)
- **Flippa** — širi marketplace

### Potencijalni kupci
1. **Regionalni LegalTech igrači** — Draftomat (Srbija), JusticeFusion (BiH/HR/SR) — žele ekspanziju
2. **Odvjetnički uredi** — žele interni alat bez razvoja
3. **SaaS agregatori** — kupuju nišne alate i skaliraju
4. **Acqui-hire** — netko plati za tebe + kod

### Ključne metrike za kupce
- MRR trend (rastući)
- Churn rate (<5% mjesečno)
- CAC (cost of acquisition) vs LTV (lifetime value)
- Diversifikacija prihoda (nijedan klijent >10%)
- Dokumentacija kvaliteta (README, API docs, testovi — ovo VEĆ imaš)

---

## 9. KAKO MAKSIMIZIRATI VRIJEDNOST PRIJE PRODAJE

### Tehničko
- [ ] **Čista dokumentacija** — README, API docs, arhitektura dijagrami
- [ ] **CI/CD pipeline** — GitHub Actions, automatski testovi, deploy
- [ ] **Monitoring** — uptime, error tracking (Sentry), performance
- [ ] **GDPR compliance** — privacy policy, data processing agreement, cookie consent
- [ ] **Security audit** — OWASP top 10 provjera (XSS već riješen)

### Poslovno
- [ ] **Zaštitni znak** — registriraj "LegalTech Suite Pro" pri DZIV-u (~150 EUR)
- [ ] **Recurring revenue** — pretplata, ne jednokratne prodaje
- [ ] **Niski churn** — fokus na retenciju (email onboarding, feature tours)
- [ ] **Testimoniali** — skupljaj izjave zadovoljnih korisnika
- [ ] **Financial tracking** — uredan P&L, MRR dashboard, churn metrike

---

## 10. PRIORITETNI REDOSLIJED IMPLEMENTACIJE

### SPRINT 1 (Tjedan 1–2): Infrastruktura
1. Preseli na Railway/Render
2. Dodaj analytics (Plausible)
3. Kupi domenu (legalsuite.hr ili pravni-dokumenti.hr)

### SPRINT 2 (Tjedan 2–4): Sudski registar API
4. Registracija na sudreg-data.gov.hr
5. OAuth2 flow implementacija
6. "Pretraži tvrtku po OIB-u" u unos_stranke()

### SPRINT 3 (Tjedan 4–6): e-Predmet API
7. GraphQL klijent
8. Modul "Praćenje predmeta"

### SPRINT 4 (Tjedan 6–8): Monetizacija
9. Auth sustav (email + password)
10. Stripe/Monri integracija
11. Freemium wall (3 dok/mj besplatno)

### SPRINT 5 (Tjedan 8–10): NN integracija
12. ELI parser za Narodne novine
13. Auto-linkovi na zakone u dokumentima
14. Modul "Pretraga zakona"

### SPRINT 6 (Tjedan 10–12): Beta launch
15. Landing page + SEO
16. 10 beta korisnika
17. Feedback loop

---

## 11. TROŠKOVI (MJESEČNO)

| Stavka | Cijena | Napomena |
|--------|--------|----------|
| Hosting (Railway/Render) | $5–12 | Starter plan |
| Domena (.hr) | ~10 EUR/god | ~0.85 EUR/mj |
| Stripe fees | 1.4% + 0.25 EUR | Po transakciji |
| Analytics (Plausible) | $9/mj | Ili self-hosted: $0 |
| Email (Resend/Mailgun) | $0–20 | Free tier dovoljan za start |
| Claude/OpenAI API | $20–100 | Ovisno o korištenju |
| **UKUPNO (bez AI)** | **~$15–25/mj** | |
| **UKUPNO (s AI)** | **~$35–125/mj** | |

**Break-even:** 2–3 Pro korisnika (15 EUR/mj) pokrivaju sve troškove bez AI-ja.
S AI-jem: 5–10 Pro korisnika.

---

## 12. RIZICI I MITIGACIJE

| Rizik | Vjerojatnost | Utjecaj | Mitigacija |
|-------|-------------|---------|------------|
| API-ji se ugase/promijene | Niska | Visok | Graceful degradation, cache, fallback na ručni unos |
| Regulatorni rizik (pravni savjeti bez licence) | Srednja | Visok | Jasni disclaimeri: "Ovo nije pravni savjet", ne zamjenjuje odvjetnika |
| JusticeFusion/Draftomat uđu na HR tržište | Srednja | Srednji | First-mover advantage, lokalizacija, niska cijena |
| Niska willingness to pay | Srednja | Visok | Freemium, dokazati ROI (ušteda 30min po dokumentu x 100 EUR/sat odvjetnika) |
| Streamlit performance ograničenja | Srednja | Srednji | Migracija na FastAPI + React kad bude potrebno |
| GDPR kršenje | Niska | Visok | Privacy by design, DPO, ne spremaj osobne podatke nepotrebno |

---

## 13. KEY METRICS ZA PRAĆENJE

### Faza 1 (Validacija)
- [ ] Broj registriranih korisnika
- [ ] Broj generiranih dokumenata (ukupno + po modulu)
- [ ] Conversion rate: registracija → plaćanje
- [ ] Willingness to pay (ankete, A/B test cijena)

### Faza 2 (Rast)
- [ ] MRR (monthly recurring revenue)
- [ ] Churn rate (mjesečni)
- [ ] CAC (cost of customer acquisition)
- [ ] LTV (lifetime value)
- [ ] NPS (net promoter score)

### Faza 3 (Skaliranje)
- [ ] ARR (annual recurring revenue)
- [ ] Rule of 40 (growth rate + profit margin > 40%)
- [ ] Revenue per employee
- [ ] Market share u Hrvatskoj

---

## ZAVRŠENO (Sesija 10 — UI Overhaul + Bug Fix)

- [x] FIX: nn_pretraga.py StreamlitAPIException — popular query buttons crashed app (pending key pattern)
- [x] FIX: eoglasna.py brze pretrage — same session_state widget-key bug
- [x] FIX: kalendar.py st.time_input(value=None) — replaced with default time
- [x] FIX: kalendar.py st.secrets.get() crash without secrets config — added try/except
- [x] FIX: auth.py guest login — made "Isprobaj besplatno" the primary CTA (no login wall)
- [x] UI: Removed emoji overuse across all pages (nn_pretraga, eoglasna, epredmet, kalendar)
- [x] UI: Redesigned login page — guest access prominent, cleaner layout, removed disabled OAuth buttons
- [x] UI: Simplified sidebar — fewer items, shorter names, global search bar
- [x] UI: Cleaned up landing page — less information overload, cleaner cards
- [x] UI: Updated config.py CSS — sidebar search styling, tighter spacing, consistent sizes
- [x] UI: Refactored LEGAL-SUITE.py routing — data-driven _MODULI dict instead of hardcoded nav
- [x] 129 tests still passing

## UI KRITIKA — Preostali zadaci (prioritizirano)

### Prioritet 1: Funkcionalni problemi
- [ ] API graceful degradation — e-Predmet, e-Oglasna, NN padaju ako API ne odgovara; trebaju fallback s demo podacima
- [ ] Kalendar persistencija — eventi se gube pri reloadu; treba JSON file storage ili database
- [ ] Napuni primjerom na svim stranicama — trenutno samo tuzbe, kazneno, opomene, upravno
- [ ] Forme: input length limits — text_area nema max_chars, potencijalno zloupotreba

### Prioritet 2: UX poboljsanja
- [ ] Breadcrumbs — korisnik ne zna gdje je u app hijerarhiji
- [ ] Generirani dokument na vrhu — trenutno treba scrollati ispod forme
- [ ] Keyboard shortcuts — Ctrl+Enter za generiranje
- [ ] Nedavno koristeni moduli — quick access na landing page
- [ ] Onboarding flow — prvi put koristenje, guided tour
- [ ] Vodic: direktni quick-link gumbi umjesto "Pokazi korake" pa tek onda navigacija

### Prioritet 3: Vizualni polish
- [ ] Dark mode podrska
- [ ] Responsive design — mobile sidebar problema
- [ ] Form grouping — vizualno odvojiti sekcije forme (stranke, detalji, dokumenti)
- [ ] Loading skeleton states umjesto spinnera
- [ ] Konzistentna tipografija — neki headeri koriste emoji, neki ne

### Prioritet 4: Arhitekturalno
- [ ] Migracija na FastAPI + React za bolje iskustvo (long-term)
- [ ] Database za korisnike, dokumente, kalendar
- [ ] OAuth2 implementacija (Google, Apple) s pravim credentials
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Error tracking (Sentry)

## ZAVRŠENO (prethodne sesije - tehnički development)

- [x] 60+ generatora pravnih dokumenata (15 pravnih područja)
- [x] Baza 74 hrvatska suda + selectbox helper
- [x] OIB ISO 7064 mod-11-10 checksum validacija
- [x] Podrška za više stranaka (dinamičko dodavanje/uklanjanje)
- [x] Kalkulator sudskih pristojbi (pristojbe.py + stranica + integracija)
- [x] Odvjetnička tarifa auto-izračun (Tbr. 7) za troškovnik u tužbama
- [x] Predlošci standardnih klauzula (klauzule.py, 17 klauzula)
- [x] DOCX export s watermarkom, headerom, page numbers
- [x] Vodič integriran u početnu stranicu
- [x] Scroll-to-top na navigaciju, auto-scroll na vodič detalje
- [x] Sidebar button navigacija s ikonama
- [x] Napuni primjerom (tužbe, kazneno, opomene, upravno)
- [x] Provjera zastare i rokova žalbe
- [x] 129 unit testova
- [x] ZK bold tag bug fix (format_text double-escape)
- [x] DOCX hard break fix (OxmlElement w:br)

---

*Ovaj dokument je živi plan — ažuriraj ga nakon svakog sprinta.*
