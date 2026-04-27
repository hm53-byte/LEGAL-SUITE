# LegalTechSuite Pro

**Generator hrvatskih pravnih dokumenata u par klikova.**

Web aplikacija na koju korisnik dođe, popuni formu (npr. podatke o tužitelju i tuženiku, iznos, opis duga), klikne **Generiraj** i preuzme gotov `.docx` dokument koji može odštampati i odnijeti na sud ili pošaljati strani. Aplikacija pokriva 60+ tipova dokumenata u 15 pravnih područja: ugovori, tužbe, ovrhe, žalbe, zemljišne knjige, opomene, punomoći, trgovačko, obvezno, obiteljsko, upravno, kazneno, stečajno pravo te zaštita potrošača.

**Što aplikacija NE radi**: ne pruža pravne savjete, ne klasificira korisnikov slučaj, ne predviđa ishod postupka. To su poslovi odvjetnika. Aplikacija je determinističko popunjavanje obrazaca — radi isto kao Word kad otvoriš template i upisuješ u prazna polja, samo s 60+ već pripremljenih predložaka i hrvatskim sudskim formatiranjem (Times New Roman 12, marže 2,5 cm, datumi `dd.mm.yyyy.`).

---

## Sadržaj

1. [Što sustav radi](#što-sustav-radi)
2. [Što sustav ne radi (pravna pozicija)](#što-sustav-ne-radi-pravna-pozicija)
3. [Rječnik termina](#rječnik-termina)
4. [Kontekst nastanka](#kontekst-nastanka)
5. [Arhitektura i tijek podataka](#arhitektura-i-tijek-podataka)
6. [Stack i ovisnosti](#stack-i-ovisnosti)
7. [Instalacija (lokalno)](#instalacija-lokalno)
8. [Pokretanje](#pokretanje)
9. [Konfiguracija (`.env` i Streamlit secrets)](#konfiguracija-env-i-streamlit-secrets)
10. [Generatori dokumenata (60+ tipova)](#generatori-dokumenata-60-tipova)
11. [Katalog po pravnom području (vodič)](#katalog-po-pravnom-području-vodič)
12. [Per-document watermark (forensic audit trail)](#per-document-watermark-forensic-audit-trail)
13. [**MONETIZACIJA**](#monetizacija)
14. [AI Act 2026 i nadripisarstvo — kako aplikacija ostaje izvan rizika](#ai-act-2026-i-nadripisarstvo--kako-aplikacija-ostaje-izvan-rizika)
15. [Razvojno okruženje](#razvojno-okruženje)
16. [Testovi](#testovi)
17. [Otklanjanje grešaka (troubleshooting)](#otklanjanje-grešaka-troubleshooting)
18. [Struktura direktorija](#struktura-direktorija)

---

## Što sustav radi

Pet logičkih slojeva, redom:

| Sloj | Komponenta (datoteka) | Što radi |
|---|---|---|
| 1. Korisničko sučelje | `LEGAL-SUITE.py`, `stranice/*.py` | Streamlit forme: korisnik popunjava polja (imena stranaka, OIB, iznos, opis dokumenta, sud nadležnosti). Sve forme rade po jedinstvenom obrascu (vidi `_render_pocetna()` i `_NAV_SECTIONS`). |
| 2. Pomoćne funkcije | `pomocne.py`, `sudovi.py`, `pristojbe.py`, `klauzule.py` | Validacija OIB-a (ISO 7064 algoritam), formatiranje hrvatskih iznosa ("12.500,50 EUR"), baza 74 hrvatska suda s adresama, kalkulator sudskih pristojbi (NN 118/18), biblioteka 17 standardnih ugovornih klauzula. |
| 3. Generatori dokumenata | `generatori/*.py` (10 modula, 60+ funkcija) | Čiste Python funkcije: prima rječnik s podacima, vraća HTML niz. Bez side-effekata. Primjer: `generiraj_ugovor_o_kupoprodaji(podaci) -> str`. |
| 4. Pretvorba u Word | `docx_export.py` | HTML iz generatora se parsira pa pretvara u `python-docx` Document, dodaju se zaglavlje s nazivom dokumenta, footer sa stranicama, watermark s ID brojem. Korisnik dobije `.docx` koji može otvoriti u Word/LibreOffice. |
| 5. Vanjski registri (read-only) | `api_eoglasna.py`, `api_epredmet.py`, `api_nn.py`, `api_sudreg.py` | Skripte za pretragu javnih registara: e-Oglasna ploča sudova, ePredmet (status sudskog predmeta), Narodne novine (propisi), Sudski registar (tvrtke). Aplikacija samo čita; ne mijenja podatke u registrima. |

**Tipičan korisnički put**:

1. Korisnik otvori web aplikaciju (browser).
2. Lijevo bira modul (npr. "Ugovori"), zatim tip dokumenta (npr. "Kupoprodajni ugovor").
3. Popunjava formu: imena, OIB-i, predmet ugovora, iznos, mjesto, datum.
4. Klikne **Generiraj**.
5. Pojavi se preview na stranici + gumb **Preuzmi**.
6. Klikom dobije `.docx` koji može otvoriti, dotjerati i odštampati.

---

## Što sustav ne radi (pravna pozicija)

Aplikacija je **determinističko popunjavanje obrazaca** — kao Word makro, ali web. Razlozi za ovu strogu poziciju:

- **Hrvatski Zakon o odvjetništvu, čl. 72**: neovlašteno pružanje pravne pomoći je kazneno djelo (nadripisarstvo). Aplikacija ne smije ni implicitno preporučiti korisniku što da napravi u njegovoj situaciji.
- **EU AI Act 2024/1689 (vrijedi od 2026)**, Annex III točka 8: AI sustavi koji se koriste u "primjeni prava na konkretne slučajeve" klasificiraju se kao visokorizični i podliježu strogim obavezama (kazne do 35 mil. EUR ili 7 % globalnog prometa). Aplikacija nema AI sloj koji bi to mogao biti — sve je determinističko popunjavanje obrazaca.

Konkretno, aplikacija:

- ✅ **Generira dokument iz polja koje korisnik sam unese.** Korisnik je odgovoran za sadržaj. Aplikacija samo formatira.
- ✅ **Pokazuje katalog dostupnih dokumenata po pravnom području** (objektivna taksonomija — npr. "Ovršno pravo: opomene, ovršni prijedlozi, prigovori"). Korisnik sam bira.
- ❌ **NE klasificira korisnikov problem** ("vaš slučaj je tužba radi X"). Ranija verzija je imala vodič tipa "Netko mi duguje novac → ovrha"; refaktoriran 2026-04-27 u objektivni katalog (vidi K5 u sekciji Razvojni okoliš).
- ❌ **Ne preporučuje pravni postupak** ili rok djelovanja (rokovi su dio konkretnog dokumenta, nisu push-poruka u UI-u).
- ❌ **Ne predviđa ishod**, ne procjenjuje vjerojatnost uspjeha, ne savjetuje strategije.
- ❌ **Ne koristi generativni AI** za sadržaj dokumenata. Predlošci su ručno napisani Python kodom.

Disclaimer banner se prikazuje na početnoj stranici: *"Aplikacija ne pruža pravne savjete niti analizira vašu situaciju. Generira deterministički ispunjene .docx dokumente iz polja koje sami unesete. Ako niste sigurni što vam treba, posavjetujte se s odvjetnikom (HOK Imenik)."*

---

## Rječnik termina

Sve skraćenice koje se pojavljuju u kodu i ovom dokumentu:

| Skraćenica | Puni naziv | Značenje |
|---|---|---|
| **OIB** | Osobni identifikacijski broj | 11-znamenkasti jedinstveni identifikator pravne ili fizičke osobe u Hrvatskoj |
| **MBS** | Matični broj subjekta | Identifikator pravne osobe u Sudskom registru |
| **ZOO** | Zakon o obveznim odnosima | NN 35/05 i izmjene |
| **ZPP** | Zakon o parničnom postupku | NN 53/91 i izmjene; uređuje tužbe i žalbe u građanskim sporovima |
| **ZUP** | Zakon o općem upravnom postupku | NN 47/09; uređuje žalbe na upravna rješenja |
| **ZUS** | Zakon o upravnim sporovima | NN 20/10; uređuje tužbe upravnom sudu |
| **ZPPI** | Zakon o pravu na pristup informacijama | NN 25/13; zahtjevi tijelima javne vlasti |
| **ObZ** | Obiteljski zakon | NN 103/15 |
| **SZ** | Stečajni zakon | NN 71/15 |
| **HOK** | Hrvatska odvjetnička komora | hok-cba.hr; Imenik odvjetnika |
| **e-Oglasna** | e-Oglasna ploča sudova | Portal pravosudje.hr na kojem se objavljuju stečajni postupci, ovrhe, dražbe |
| **ePredmet** | Status sudskog predmeta | sudovi.pravosudje.hr — provjera statusa predmeta po broju |
| **NN** | Narodne novine | Službeno glasilo RH |
| **St-XXX/YYYY** | Oznaka stečajnog predmeta | Format broja: vrsta postupka (St=stečaj, Ovr=ovrha, P=parnica), redni broj, godina |
| **DOCX** | Office Open XML | Format datoteke koji aplikacija generira (čita ga Word, LibreOffice, Google Docs) |
| **AI Act** | Akt o umjetnoj inteligenciji EU | Regulacija 2024/1689; vrijedi za AI sustave u EU |
| **GDPR** | Opća uredba o zaštiti podataka | EU regulacija o osobnim podacima; primijenjuje se i na aplikaciju |

---

## Kontekst nastanka

Aplikacija je započela kao alat **za samog autora** (student prava + razvoj softvera) — generiranje vlastitih obrazaca brže nego kopiranjem iz starih predmeta. Tijekom razvoja je narastao na 60+ tipova dokumenata jer je svaki novi predmet trebao novi obrazac.

Odluke o smjeru kao proizvod (ne samo osobni alat):

- **Cilj segment**: građanin / mali poduzetnik koji **ne zna i ne treba znati** pravni žargon. Aplikacija mu nudi obrazac s opisima polja u običnom hrvatskom jeziku.
- **Cijena**: ostaje free za core generiranje, monetizacija ide kroz **PRO pretplatu** (vidi sekciju "Monetizacija") koja eliminira watermark, daje neograničene download-e, čišću predloškastu istragu.
- **Što namjerno NIJE u aplikaciji**: AI klasifikator slučaja, AI generirane klauzule, predikcija ishoda. To su zone visokorizične klasifikacije AI Acta i kaznene zone nadripisarstva (vidi sekciju "AI Act 2026 i nadripisarstvo"). Stati izvan njih je **konkurentska prednost**, ne ograničenje — aplikacija može doseći B2C tržište bez regulatorne barijere koja muči SaaS legaltech konkurente.

---

## Arhitektura i tijek podataka

```
┌─────────────────────────────────────────────────────────────┐
│  KORISNIK (web browser)                                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STREAMLIT APLIKACIJA  (Streamlit Community Cloud, 24/7)    │
│  LEGAL-SUITE.py                                             │
│   - Sidebar: 18 modula u 3 sekcije                          │
│   - Početna: katalog 11 pravnih područja (passive)          │
│   - Forme za podatke (stranice/*.py)                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  GENERATOR DOKUMENATA  (čista Python funkcija)              │
│  generatori/ugovori.py, tuzbe.py, ovrhe.py, ...             │
│   - prima dict s podacima                                   │
│   - vraća HTML string                                       │
│   - bez state-a, bez side-effekata                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  PRETVORBA HTML → DOCX  docx_export.py                      │
│   - parse HTML (HTMLParser subclass)                        │
│   - mapping na python-docx (paragrafi, tablice, formati)    │
│   - dodaje header (naziv dokumenta), footer (stranice + ID) │
│   - utiskuje per-doc serial broj u XML metadata             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  SUPABASE POSTGRES  (cloud, 24/7)                           │
│   - users, entitlements, download_log, stripe_events        │
│   - upis koji dokument je generiran (forensic audit)        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  KORISNIK PREUZIMA .docx                                    │
│   - lokalno u Word / LibreOffice / Google Docs              │
└─────────────────────────────────────────────────────────────┘
```

**Vanjske integracije (read-only)**:

```
   api_nn.py        ─────► Narodne novine ELI sitemap (provjera propisa)
   api_eoglasna.py  ─────► e-Oglasna ploča (sudski oglasi)
   api_epredmet.py  ─────► ePredmet (status predmeta)
   api_sudreg.py    ─────► Sudski registar (tvrtke)
```

Korisnik može u aplikaciji upisati broj predmeta i dobiti status iz ePredmeta, ili pretražiti tvrtku u Sudreg-u prije nego upiše OIB u tužbu. Aplikacija samo **čita** — nikad ne piše u te registre.

---

## Stack i ovisnosti

| Komponenta | Tehnologija | Razlog izbora |
|---|---|---|
| Programski jezik | Python 3.10+ | Većina libova za PDF/DOCX/scraping je Python; Streamlit je Python-native |
| Web framework | Streamlit ≥1.28 | Najjednostavniji način napraviti formu + preview + download. Bez React/Vue toolchain-a. |
| Generiranje DOCX | python-docx ≥1.0 | Native Python, nema vanjskih ovisnosti, radi na Windows/Linux |
| HTML parsiranje | lxml + standardni `html.parser` | `docx_export.py` koristi HTMLParser subclass za HTML → DOCX |
| HTTP klijent | requests | Za vanjske registre (ePredmet, Sudreg) i Supabase REST API |
| Hosting | Streamlit Community Cloud | Free tier, public repo, auto-deploy iz GitHub-a |
| Baza podataka (monetizacija) | Supabase Postgres | Free tier 500 MB, 50k MAU, REST API + Row-Level Security |
| Plaćanje | Stripe Checkout + Subscription | Industry standard, HR PDV preko Stripe Tax |
| Webhook handler | Cloudflare Workers | Free tier 100k zahtjeva/dan, stable URL, low latency edge |
| Auth | Streamlit + lokalni `.users.json` (postojeći) → Supabase Auth (planirano) | Migracija u tijeku — vidi sekciju "Što ostaje" |

**Ne ovisi o**: GPU, lokalnom AI modelu, posebnom hardveru, internetskom plaćanju izvan Stripe-a, vlastitom mail serveru.

---

## Instalacija (lokalno)

### Windows (preporučeno za razvoj)

```powershell
cd $env:USERPROFILE\Documents\APLIKACIJA
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Python 3.10+ je obavezan. Testirano na Pythonu 3.13 / Windows 11.

### Linux / WSL

```bash
cd ~/APLIKACIJA
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### macOS

Isto kao Linux. Provjereno na Sequoia 15.

---

## Pokretanje

### Lokalno

```bash
streamlit run LEGAL-SUITE.py
```

Otvori `http://localhost:8501` u browseru.

### Deploy na Streamlit Community Cloud

Detaljne upute u [`upute.md`](upute.md). Sažeto:

1. Push kod na GitHub repo `hm53-byte/LEGAL-SUITE`.
2. Idi na https://share.streamlit.io → **New app** → odaberi repo, branch `main`, file `LEGAL-SUITE.py`.
3. Streamlit Cloud auto-deploya pri svakom git push-u.

Trenutni live URL: `https://legal-suite-flh3jnmcj5kc7jp5y9w9eb.streamlit.app`

---

## Konfiguracija (`.env` i Streamlit secrets)

### Lokalni razvoj — `.env`

```ini
# Trenutno aplikacija ne treba .env za core funkcionalnost (sve je deterministic).
# Monetizacija (Supabase + Stripe + Cloudflare) zahtijeva secrets — vidi dolje.
```

### Streamlit Cloud — Settings → Secrets (TOML format)

Potrebno za monetizaciju (vidi sekciju "Monetizacija"):

```toml
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_ANON_KEY = "eyJh..."   # public anon key (RLS-zaštićen, OK za client)
STRIPE_CHECKOUT_URL_BASE = "https://lts-stripe-webhook.<sub>.workers.dev"
```

**NE STAVLJATI** u Streamlit secrets:
- `SUPABASE_SERVICE_ROLE_KEY` (admin bypass; pripada Cloudflare Worker-u)
- `STRIPE_API_KEY` (secret; pripada Cloudflare Worker-u)
- `STRIPE_WEBHOOK_SECRET` (signature verify; pripada Cloudflare Worker-u)

---

## Generatori dokumenata (60+ tipova)

Svaki generator je čista Python funkcija — `def generiraj_xxx(podaci: dict) -> str` koja vraća HTML niz. Sve dijaktolitičke specifičnosti hrvatskog jezika (vokativ, lokativ, padeži imena) idu kroz `pomocne._padez_ime()` i `pomocne.u_lokativu()`.

Pregled po modulima u `generatori/`:

| Modul | Broj tipova | Primjeri dokumenata |
|---|---|---|
| `ugovori.py` | 10 | Kupoprodajni ugovor, ugovor o najmu, ugovor o radu, NDA, ugovor o djelu, sporazum o raskidu |
| `tuzbe.py` | 2 | Tužba za isplatu duga, tužba za naknadu štete |
| `ovrhe.py` | 7 | Ovršni prijedlog na temelju vjerodostojne isprave, prigovor protiv rješenja o ovrsi |
| `zalbe.py` | 1 | Žalba na presudu (ZPP) |
| `zemljisne.py` | 7 | Prijedlog za uknjižbu, brisovna tužba, prijedlog za upis hipoteke |
| `opomene.py` | 1 | Opomena pred tužbu |
| `punomoci.py` | 1 | Specijalna punomoć |
| `trgovacko.py` | 5 | Društveni ugovor d.o.o., ugovor o prijenosu udjela, NDA poslovni |
| `obvezno.py` | 8 | Cesija, kompenzacija, jamstvo, ugovor o darovanju, sporazum o priznanju duga |
| `obiteljsko.py` | 5 | Sporazumni razvod, tužba za razvod, bračni ugovor |
| `upravno.py` | 4 | Žalba ZUP, tužba upravnom sudu (ZUS), zahtjev ZPPI |
| `kazneno.py` | 3 | Kaznena prijava, privatna tužba |
| `stecajno.py` | 3 | Prijedlog za osobni stečaj, prijava tražbine |
| `potrosaci.py` | 3 | Reklamacija, jednostrani raskid online kupnje, prijava inspekciji |

Svaki dokument prati hrvatske formalne konvencije: Times New Roman 12 pt, marže 2,5 cm, justified, datumi `dd.mm.yyyy.`.

---

## Katalog po pravnom području (vodič)

Početna stranica prikazuje **objektivni katalog** od 11 pravnih područja (refaktoriran 2026-04-27, vidi K5 u sekciji Razvojni okoliš). Korisnik sam bira područje koje ga zanima, klikom **Vidi tipove dokumenata** dobije listu dostupnih dokumenata u tom području, klikom **Otvori: <modul>** prelazi na odgovarajuću formu.

Što katalog **ne** radi:

- ❌ Ne klasificira korisnikov problem ("Netko mi duguje novac → ovrha")
- ❌ Ne savjetuje koji dokument koristiti
- ❌ Ne postavlja žurnost ("rok je 15 dana — žuri se!")

Razlog: takav UI bi bio implicit pravni klasifikator, što ulazi u zonu nadripisarstva (ZO čl. 72) i visokorizičnu zonu AI Acta (Annex III pt. 8) — čak i ako klasifikator nije AI nego heuristic. Detalji u sekciji "AI Act 2026 i nadripisarstvo".

---

## Per-document watermark (forensic audit trail)

Svaki generiran `.docx` dobije **jedinstveni serijski broj** u formatu `AB-CDEF-123456` (12 hex znakova). Serijski broj se utisne na dva mjesta:

1. **Vidljiv u footer-u dokumenta**: na zadnjoj stranici stoji *"Generirano iz LegalTechSuite Pro — ID: AB-CDEF-123456"*. Korisnik to može ručno ukloniti otvarajući docx u Word-u, ali default je tu.
2. **Nevidljiv u XML metapodacima** (Office Open XML `dc:identifier`): forensic alati (ExifTool, Microsoft "Document Properties") to vide. Skriven od casual korisnika.

**Što watermark NIJE**: nije DRM koji onemogućuje korištenje. Korisnik može slobodno ukloniti vidljivi footer i čak nevidljive XML metapodatke ako zna OOXML strukturu. Watermark je **forensic** (Petitcolas, Anderson, Kuhn 1999, IEEE 87(7)) — daje dokaz autentičnosti **kad se docx pojavi u sporu**, ne sprečava kopiranje.

**Privatnost**: serijski broj je SHA256 hash od `(user_id, doc_type, timestamp, random nonce)`. NE pohranjuje korisničko ime ni OIB u XML — samo serijski broj. Forensic chain ide preko `download_log` tablice u Supabase: `serial_hash → user_id`.

PRO korisnici (vidi Monetizacija) dobivaju **cleaner footer** (samo ID, bez "Generirano iz" reklame) ali per-doc serial je i kod njih prisutan u XML metapodacima.

---

## MONETIZACIJA

Aplikacija je **freemium**: core generiranje dokumenata je besplatno, **PRO pretplata** otključava neograničene download-e, čišći footer i prioritet kod budućih novih dokumenata.

Cijela monetizacija je **cloud-native** — radi 24/7 čak i kad je razvojni PC isključen. Sve komponente su u free tier-u dok god je promet ispod limita; pri padu na live mode jedini fiksni trošak je **Stripe-ov 2,9 % + 0,30 EUR po transakciji**.

### Arhitektura monetizacije

```
[Korisnik browser]
        │
        ▼
[Streamlit Community Cloud] ──► čita entitlement (plan: free/pro) iz ──► [Supabase Postgres]
        │   (pri svakom download-u)                                              ▲
        │                                                                        │
        │ "Pretplati se"                                                         │
        ▼                                                                        │
[Stripe Checkout]                                                                │
        │                                                                        │
        │ webhook event (checkout.session.completed itd.)                        │
        ▼                                                                        │
[Cloudflare Worker]  ─────► verify Stripe signature ─────► UPSERT entitlement ──┘
                            (bypass Row-Level Security
                             preko service_role key-a)
```

### Komponente

#### 1. Supabase Postgres — baza korisnika i pretplata

Free tier 500 MB DB, 50k aktivnih korisnika mjesečno. 4 tablice:

| Tablica | Što čuva |
|---|---|
| `users` | E-mail, hash lozinke (PBKDF2-SHA256), Stripe customer ID |
| `entitlements` | Per-user plan (`free` ili `pro`), status (`active` / `past_due` / `revoked`), period_end (datum isteka pretplate) |
| `download_log` | Forensic audit: per-doc serial broj, koji korisnik ga je generirao, kada, koji tier |
| `stripe_events` | Idempotency anchor: svaki Stripe webhook event upisuje se UNIQUE; duplikat se ignorira |

**Row-Level Security (RLS)**: korisnik vidi samo svoje retke. `users_self_select`, `entitlements_self_read`, `download_log_self_read` policies. Webhook handler bypassa RLS preko `service_role` ključa (samo on, ne klijent).

Schema je u `cloud/supabase_schema.sql` — copy-paste u Supabase Dashboard SQL Editor. Idempotent (`CREATE TABLE IF NOT EXISTS`), siguran ponovni run.

#### 2. Stripe — Checkout + Subscription

Stripe je standardni payment gateway. Ima podršku za:

- **Subscription** (`mode: 'subscription'` u Checkout-u): korisnik plati prvi put, Stripe nastavlja naplatu mjesečno automatski.
- **Stripe Tax**: HR PDV (25%) se automatski računa i prikazuje korisniku prije naplate. Korisnik aplikacije ne treba implementirati porezni kalkulator.
- **Webhooks**: Stripe šalje HTTP POST na naš endpoint pri svakoj promjeni (uspješna naplata, refund, dispute, otkazivanje pretplate). Mi onda updiramo `entitlements` u Supabase.
- **Test mode**: prije live mode-a sve se testira s test karticom `4242 4242 4242 4242`. Beskonačno besplatno.
- **Live mode**: prebacuje se kad je sve provjereno. Stripe ne uzima minimum fee; samo % po transakciji.

#### 3. Cloudflare Workers — webhook handler

Stripe webhook treba **stable HTTP endpoint** koji uvijek radi (24/7) i ima brz odgovor (<5 sekundi po Stripe SLA). Streamlit Community Cloud nije dobar za to — ima ephemeral URL i moguće je da uspava se.

**Cloudflare Workers** je serverless platforma (kao AWS Lambda, ali edge — radi blizu korisnika u 320+ gradova). Free tier daje 100 000 zahtjeva dnevno; mi tipično trebamo <50 zahtjeva dnevno (svaki kupac generira 5-10 webhook eventova).

Worker (`cloud/cf_worker_stripe.ts`) ima 3 endpointa:

- `POST /webhook` — Stripe pošalje event, mi verificiramo signature, idempotent UPSERT u Supabase.
- `POST /create-checkout-session` — Streamlit aplikacija pošalje `{user_id, plan}`, mi vratimo Stripe Checkout URL.
- `GET /health` — uptime monitoring (UptimeRobot, Pingdom).

Worker ima **service_role key** (admin bypass RLS) jer mora pisati u `entitlements` u ime korisnika. Ovaj ključ NIKAD ne ide u Streamlit klijent.

#### 4. Streamlit Cloud — već postoji

Streamlit Community Cloud auto-deploya iz GitHub repo-a `hm53-byte/LEGAL-SUITE` na svaki push. Samo treba dodati 3 secrets (Settings → Secrets) za monetizaciju:

```toml
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_ANON_KEY = "eyJh..."
STRIPE_CHECKOUT_URL_BASE = "https://lts-stripe-webhook.<sub>.workers.dev"
```

### Setup (jednom, ~45 min)

Detaljne upute u [`cloud/SETUP.md`](cloud/SETUP.md). Sažeto:

1. **Supabase**: kreiraj projekt → SQL Editor → paste `cloud/supabase_schema.sql` → Run → kopiraj URL + 2 ključa (anon + service_role).
2. **Stripe**: account → Product `LegalTechSuite PRO` → kopiraj Price ID + Secret key. (Test mode prvi.)
3. **Cloudflare**: `npm install -g wrangler && wrangler login && cd cloud && npm install && wrangler deploy` → kopiraj URL + dodaj 6 secrets.
4. **Streamlit**: dodaj 3 secrets u Settings.
5. **Stripe Webhook config**: dodaj endpoint URL od Worker-a, kopiraj signing secret nazad u Worker secrets.
6. **End-to-end test**: testna kartica `4242 4242 4242 4242`.
7. **Production switch**: kad sve radi u test mode-u, prebaci Stripe na live, regeneriraj keys, ponovno deploy.

### Kako radi gumb "Pretplati se na PRO"

`entitlements.render_subscribe_cta()` se zove iz sidebar-a Streamlit aplikacije. Ako korisnik nije logiran ili nije konfigurirana monetizacija, gumb se ne prikazuje. Ako je free tier, gumb je vidljiv. Klik:

1. Streamlit pošalje `POST /create-checkout-session` na Cloudflare Worker s `{user_id}`.
2. Worker stvori Stripe Checkout sesiju s `metadata: {user_id, plan: 'pro'}` i vrati `checkout_url`.
3. Streamlit prikaže link **Otvori Stripe Checkout** (klik otvori novu stranicu).
4. Korisnik plati. Stripe redirekta natrag na aplikaciju s `?checkout=success`.
5. U pozadini: Stripe pošalje `checkout.session.completed` webhook → Worker → UPSERT entitlement → status 'active'.
6. Korisnik refresh-a stranicu → `entitlements.is_pro()` vraća `True` (TTL cache 30 s) → gumb nestaje, footer je sada PRO verzija.

### Što se dogodi pri refundu / otkazivanju

- **Refund** (`charge.refunded` webhook): Worker postavi `entitlements.status = 'revoked'` → korisnik odmah gubi PRO.
- **Otkazivanje pretplate** (`customer.subscription.deleted`): isto.
- **Failed payment** (`customer.subscription.updated` s `status: 'past_due'`): Worker postavi `past_due` → grace period 24 h prije revoke-a (planiran cron — vidi "Što ostaje").

### Trošak (mjesečna procjena za free tier)

| Servis | Limit | Naša procjena | Trošak |
|---|---|---|---|
| Streamlit Cloud | 1 GB RAM, public repo | <500 MB | **0 EUR** |
| Supabase | 500 MB DB, 50k MAU, 5 GB transfera | <100 MB DB, <100 MAU | **0 EUR** |
| Cloudflare Workers | 100k req/dan | <100 req/dan | **0 EUR** |
| Stripe (test mode) | bez | bez | **0 EUR** |
| Stripe (live mode) | 2,9 % + 0,30 EUR po transakciji | per platilac | **% prihoda** |

Ukupno: **0 EUR fiksnih troškova** dok god je u limitima. Stripe % se uzima iz uplata pretplatnika.

---

## AI Act 2026 i nadripisarstvo — kako aplikacija ostaje izvan rizika

EU AI Act 2024/1689 i hrvatski Zakon o odvjetništvu nameću ozbiljne obaveze i kazne za sustave koji:

- **Klasificiraju pravni problem korisnika u prirodnom jeziku** (AI Act Annex III pt. 8 — visok rizik, kazne do 35 mil. EUR / 7 % prometa)
- **Pružaju pravni savjet bez odvjetničke licence** (ZO čl. 72 — nadripisarstvo, kazneno djelo)
- **Predviđaju ishod sudskog postupka** (Annex III pt. 8)
- **Preporučuju strategiju vođenja postupka** (Annex III pt. 8 + ZO čl. 72)

Aplikacija je **strukturno** dizajnirana izvan ovih zona:

| Što aplikacija radi | Klasifikacija pod AI Aktom | Razlog |
|---|---|---|
| Generira docx iz polja koje korisnik sam unese | **Out-of-scope** | Determinističko popunjavanje obrazaca, ne AI sustav (Article 3(1) — "AI system" zahtijeva inferenciju, ne pukog templating) |
| Prikazuje katalog dokumenata po pravnom području | Out-of-scope | Objektivna taksonomija, ne klasifikator |
| Validira OIB s ISO 7064 algoritmom | Out-of-scope | Matematička provjera, nije AI |
| Računa zakonske zatezne kamate (kalkulator) | Out-of-scope | Aritmetika |
| Prikazuje status sudskog predmeta iz ePredmeta | Out-of-scope | Read-only prikaz javno dostupnog podatka |

Što aplikacija namjerno **NE** radi (čak i ako bi to bilo tehnički moguće):

- ❌ AI klasifikator "koji dokument vam treba?" — Annex III pt. 8 visok rizik
- ❌ AI generirane klauzule personalizirane na korisnikov slučaj — Article 50 transparency obligation + nadripisarstvo
- ❌ AI completion forme ("dovrši ovu klauzulu") — visok rizik
- ❌ Predikcija ishoda postupka — Annex III pt. 8 + ZO čl. 72
- ❌ "Smart" vodič koji zaključuje korisnikov problem iz prirodnog jezika — visok rizik

Ova ograničenja **nisu kompromis kvalitete** — to je strateška pozicija koja:

1. Eliminira regulatorni rizik (kazne, ban u EU)
2. Eliminira pravnu odgovornost autora aplikacije
3. Daje aplikaciji **konkurentsku prednost** nad SaaS legaltech konkurentima koji pokušavaju AI klasifikaciju i sad muče s compliance-om

---

## Razvojno okruženje

### BRZ_MOZAK GLAVNI INŽENJER metodologija

Razvoj aplikacije slijedi BRZ_MOZAK GLAVNI INŽENJER v5 protokol — strukturirani 5-agentni pipeline za arhitekturne izmjene s anti-business filterom, anti-atraktor filterom i nezavisnim sucem. Detalji o metodologiji su u sestrinskom projektu `RIJEKA_PRATILAC` (`GLAVNI INZINJER/`).

Razvojni ciklusi se vode kao **Kandidati K1, K2, K3, ...** Svaki kandidat je arhitekturna izmjena s mjerljivim ROI-em.

### Implementirani kandidati

#### K5 — Refaktor vodiča u passive katalog (2026-04-27)

**Što**: ranija verzija je imala "Vodič koji dokument mi treba?" s 10 kategorija u prvom licu ("Netko mi duguje novac → ovrha"). To je implicit klasifikator pravnog problema — rub nadripisarstva (ZO čl. 72) i visokorizična zona AI Acta (Annex III pt. 8). Refaktoriran u objektivni katalog 11 pravnih područja u trećem licu ("Ovršno pravo: opomene, ovrhe, prigovori"). Korisnik sam bira; aplikacija ne klasificira.

**LOC**: net -2 (uklonjen rokovi UI block + reframe stringovi). 159/159 testova nakon refaktora pass (0 regresija).

#### K3 — Cloud-native monetizacija (cloud kod gotov, čeka korisnikov setup)

**Što**: Stripe Checkout + Supabase entitlements + Cloudflare Worker webhook + per-doc forensic watermark. PC korisnika može biti isključen — sve cloud komponente rade 24/7 u free tier-u.

**Trenutni status**: cloud kod napisan i testiran lokalno (194/194 pytest pass). ToS + Privacy Policy nacrti dodani u `stranice/`. Korisnički setup (Supabase + Stripe + Cloudflare accounts) ostaje — vidi `cloud/SETUP.md`.

**LOC**: 480 src + 60 test = 540 (Python entitlements + watermark + TypeScript Cloudflare Worker + SQL schema).

#### K1 — Janusov audit lanac (forensic reproducibility, 2026-04-27)

**Što**: SHA256 hash chain nad `download_log` retcima + RFC 8785 JCS canonical input form + generator bytecode versioning registry. Svaki generirani docx producira `(input_canonical_hash, output_sha256, parent_hash, current_hash, generator_version_hash, input_schema_version)` — bit-by-bit reproducibility 6+ mjeseci kasnije iz `git checkout <commit>` + pohranjenog inputa.

**Status**: BRZ_MOZAK P2 hibrid ciklus zatvoren 7/7 USPJEH (vidi `GLAVNI_INZINJER/IDEJE/CIKLUS_K1_2026-04-27.md`). Implementirano: `audit_chain.py` (RFC 8785 JCS + chain link build/verify), `cloud/0007_audit_chain.sql` (idempotent ALTER), `entitlements.py` proširen, `scripts/build_generators_registry.py`, `scripts/replay_docx.py`, `tests/test_audit_chain.py` (15 testova).

**LOC**: 305 (225 src + 80 test).

#### K1.5 — UI ožičenje audit chain-a (2026-04-27)

**Što**: K1 audit chain je opt-in preko `pripremi_za_docx(input_dict, generator_module_path, doc_type)`. K1.5 prosljeđuje te parametre kroz svih 16 `stranice/*.py` fajlova × 88 call-sitea. Centralni helper `audit_kwargs()` u `pomocne.py` sažima logiku — call-site postaje 1-line `prikazi_dokument(..., **audit_kwargs("ugovor_kupoprodaja", podaci, "ugovori"))`.

**Status**: ZATVORENO. 13 granularnih commit-ova (1 helper + 1 baseline + 11 stranica + 1 jednostavno). Slugovi flat snake_case — npr. `tuzba`, `opomena_pred_tuzbu`, `ovrha_vjerodostojna`, `f"otkaz_{vrsta}"`, `jednostavno_kupnja_auta`. 194/194 pytest pass.

**LOC**: 160 (helper + 88 call-site izmjena).

#### K2 — Hermesov sync outbox (BRZ_MOZAK P2 hibrid ciklus, promote-an 2026-04-27)

**Što**: offline-first PWA arhitektura kompatibilna s K1 audit lancem. Service Worker presretač + IndexedDB outbox + idempotency UUID; **generacija docx-a ostaje 100% server-side** (Python pure functions) jer port na JS bi razbio K1 deterministic guarantee. Klijent serijalizira formu u outbox kad offline; sync worker POST-a na Cloudflare Worker `/api/sync` koji validira UNIQUE constraint na `client_event_id`, prosljeđuje na Streamlit, i K1 chain link se računa server-side u istoj transakciji.

**Status**: BRZ_MOZAK P2 ciklus zatvoren 7/7 USPJEH (UBOJICA 7/7 + SUDAC 7/7, delta 0). Vidi `GLAVNI_INZINJER/IDEJE/CIKLUS_K2_2026-04-27.md` (audit log) i `GLAVNI_INZINJER/IDEJE/Ideja_K2_Hermesov_sync_outbox.md` (implementacijski plan). **Implementacija nije pokrenuta** — preduvjeti: Supabase + CF Worker live deploy.

**LOC procjena**: 665 (545 src + 120 test) = 11.7 dana solo dev rok.

### Roadmap

Po dogovorenom prioritetu:

- **K2 implementacija** — kad cloud setup završen (Supabase + Stripe + CF Worker deploy)
- **K4 — Generator versioning registry proširenje**: dodati `schema_in`/`schema_out` JSON Schema polja u postojeći `generators_registry.json`; per-generator validacija; sinergija s K2 (client-side IDB validation prije save-a u outbox).
- **K1 faza 2 — Merkle root javno** (BACKLOG): aktivira se kad korporativni klijent zatraži external auditability.

### Auth migracija (planirano, blocker za K3 produkciju)

Trenutno `auth.py` koristi lokalni `.users.json`. Streamlit Community Cloud disk je ephemeral — restart svakih 7 dana briše korisnike. Migracija na Supabase Auth je preduvjet za stabilnu monetizaciju (PRO korisnici se moraju vidjeti i nakon Streamlit restart-a).

---

## Testovi

```bash
python -m pytest tests/ -q
```

Trenutno **179 testova** (~1 sekunda runtime). Pokriva:

- Validacije (OIB ISO 7064, IBAN, datumi)
- Generatore (smoke testovi za svaki tip dokumenta — provjeri da vraća HTML, da uključuje obavezna polja, da pravilno formatira hrvatske iznose)
- Pomoćne funkcije (padeži imena, sudovi lookup, pristojbe kalkulator)
- HTML → DOCX konverziju
- K3 monetizaciju: watermark serial generator (12 testova), entitlements TTL cache + graceful degradation (8 testova)

---

## Otklanjanje grešaka (troubleshooting)

### Streamlit Cloud app pokazuje "Error" nakon push-a

```bash
git log -1 --stat
streamlit run LEGAL-SUITE.py     # provjeri lokalno radi li
python -m pytest tests/ -q       # svi testovi prolaze?
```

Najčešći uzrok: novi import koji ne postoji u `requirements.txt`. Streamlit Cloud build-a fresh venv pri svakom push-u, lokalno može imati lib koji nije u requirements.

### "ModuleNotFoundError: No module named 'docx'"

```bash
pip install python-docx
```

Ne `pip install docx` (drugi paket).

### Hrvatski znakovi (ČĆŽŠĐ) ne rade u terminal output-u (Windows)

```powershell
$env:PYTHONIOENCODING = "utf-8"
```

Ili u Python skripti:

```python
import sys
sys.stdout.reconfigure(encoding="utf-8")
```

### Supabase: "JWT expired"

`SUPABASE_ANON_KEY` je validan dok god ga ne regeneriraš u Supabase Dashboard. Ako vidiš "JWT expired", regeneriraj key u Settings → API → Reset i ažuriraj Streamlit secrets.

### Stripe webhook "signature verify failed"

`STRIPE_WEBHOOK_SECRET` u Cloudflare Worker secret-u ne odgovara onom u Stripe Dashboard webhook konfiguraciji. Provjeri:

```bash
wrangler secret list   # u cloud/ direktoriju
```

I regeneriraj webhook secret u Stripe Dashboard ako treba.

### "Pretplati se" gumb se ne prikazuje

Provjeri redom:

1. Korisnik je logiran (`st.session_state._user_id` je postavljen)?
2. Streamlit secrets imaju `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `STRIPE_CHECKOUT_URL_BASE`?
3. Korisnik već je PRO? (Tada se gumb sakriva.)

```python
import entitlements as ent
print(ent._is_configured())  # True ako secrets postoje
print(ent.current_user_id())  # user_id ili None
print(ent.is_pro())           # True/False
```

---

## Struktura direktorija

```
APLIKACIJA/
├── LEGAL-SUITE.py                 # Streamlit entry point
├── auth.py                         # Login/registracija (lokalno .users.json, migracija u tijeku)
├── config.py                       # CSS stilovi, design tokens
├── pomocne.py                      # OIB/datum/iznos validacije, pomoćne UI funkcije
├── docx_export.py                  # HTML → DOCX konverzija
├── sudovi.py                       # Baza 74 hrvatska suda
├── pristojbe.py                    # Kalkulator sudskih pristojbi (NN 118/18)
├── klauzule.py                     # 17 standardnih ugovornih klauzula
├── entitlements.py                 # K3: Supabase entitlement klijent (TTL cache, graceful degradation)
├── watermark.py                    # K3: per-doc forensic serial broj generator
├── api_eoglasna.py                 # Read e-Oglasna ploča sudova
├── api_epredmet.py                 # Read ePredmet status
├── api_nn.py                       # Read Narodne novine
├── api_sudreg.py                   # Read Sudski registar
├── generatori/                     # 60+ generatora dokumenata
│   ├── ugovori.py                  # 10 tipova
│   ├── tuzbe.py                    # 2 tipa
│   ├── ovrhe.py                    # 7 tipova
│   ├── zalbe.py                    # 1 tip
│   ├── zemljisne.py                # 7 tipova
│   ├── opomene.py                  # 1 tip
│   ├── punomoci.py                 # 1 tip
│   ├── trgovacko.py                # 5 tipova
│   ├── obvezno.py                  # 8 tipova
│   ├── obiteljsko.py               # 5 tipova
│   ├── upravno.py                  # 4 tipa
│   ├── kazneno.py                  # 3 tipa
│   ├── stecajno.py                 # 3 tipa
│   └── potrosaci.py                # 3 tipa
├── stranice/                       # Streamlit forme za svaki modul
├── tests/                          # 179 pytest testova
│   ├── test_watermark.py           # K3: serial generator + footer + XML metadata
│   ├── test_entitlements.py        # K3: TTL cache, graceful degradation
│   └── ...
├── cloud/                          # K3: Cloud-native monetizacija
│   ├── supabase_schema.sql         # Postgres schema (4 tablice + RLS)
│   ├── cf_worker_stripe.ts         # Cloudflare Worker (Stripe webhook + checkout)
│   ├── wrangler.toml               # Worker deploy config
│   ├── package.json                # Worker npm deps
│   └── SETUP.md                    # 45-min step-by-step setup guide
├── agent_docs/                     # BRZ_MOZAK procesni dokumenti (sub-agentne sesije)
├── razvoj/                         # Razvojne note, prijedlozi, prošli problemi
├── HANDOFF*.md                     # Session handoff dokumenti (BRZ_MOZAK metodologija)
├── PROBLEM_S_APP.md                # Lista poznatih problema s prioritetima
├── RAZVOJ_PRIJEDLOZI.md            # Prijedlozi za razmatranje (mješani inputi)
├── CLAUDE.md                       # Instrukcije za AI asistenta (handoff za Claude Code)
├── upute.md                        # Streamlit Cloud deploy instrukcije
├── requirements.txt                # Python deps
└── README.md                       # Ovaj dokument
```

---

## Licenca i pravna napomena

Aplikacija je u privatnom razvoju autora. Korisnik koji koristi aplikaciju je **odgovoran** za sadržaj generiranih dokumenata. Aplikacija samo formatira polja koje korisnik sam unese.

Aplikacija ne pruža pravne savjete. Ako trebaš pravni savjet, posavjetuj se s odvjetnikom (HOK Imenik: https://www.hok-cba.hr).
