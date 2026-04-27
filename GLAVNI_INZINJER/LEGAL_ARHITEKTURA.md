# LEGAL_ARHITEKTURA.md — Katalog determinističkih i sigurnosnih primitiva za LegalTech

**Verzija**: v1.0 (2026-04-27)
**Domena**: LegalTechSuite Pro (deterministic document generator, izvan AI Act high-risk zone)
**Uloga**: zamjena `OSNOVE_ARHITEKTURE.md` (RIJEKA_PRATILAC, ML/inference engine domena) za APLIKACIJA-specific cikluse.

---

## Zašto novi katalog (Pravilo 33 v1 LEGAL)

`OSNOVE_ARHITEKTURE.md` iz RIJEKA_PRATILAC je katalog ML i inference engine primitiva (RNN/CNN/Transformer/Mamba/Triton/vLLM/spec-decoding/GGUF). Ako Agent 2A FILOZOF i Agent 2B INŽENJER za LegalTechSuite Pro uđu s tim input-om, neizbježno će sintetizirati AI rješenja. Čim u kod uđe **klasifikator** ili **prediktivni model**, aplikacija prelazi:

- **EU AI Act 2024/1689**, Annex III pt. 8 (visok rizik, kazne €35M / 7 % prometa) — "AI sustavi za primjenu prava na konkretne slučajeve"
- **Hrvatski Zakon o odvjetništvu**, čl. 72 (kazneno djelo nadripisarstva)

**LegalTechSuite Pro je strukturno postavljen IZVAN tih zona** (deterministic templating, ne AI). Konkurentska prednost je upravo to — možemo doseći B2C tržište bez regulatorne barijere koja muči SaaS legaltech konkurente.

Ovaj katalog stoga **isključuje** sve AI/ML primitive i **uključuje** isključivo determinističke i sigurnosne primitive koji čuvaju AI Act out-of-scope poziciju.

---

## §I — Kriptografski audit i forensic primitive

### I.1 SHA-256 hash chains

**Princip**: svaki output (npr. generirani docx) producira `(serial, sha256_of_input_canonical_form, parent_hash)`. Lanac je nepromjenjiv — ako se bilo koji raniji output retroaktivno modificira, svi sljedeći hash-evi se ne podudaraju.

**Reference**:
- Schneier 1996, *Applied Cryptography*, ch. 18.7 — hash chains
- RFC 6962 — Certificate Transparency log structure (Merkle hash chain pattern)

**Primjena u LegalTech**:
- Per-doc serial = SHA256(`user_id|doc_type|timestamp|nonce`)[:12] (postoji u K3, watermark.py)
- Audit trail tablica `download_log` može se ekstendirati s `parent_hash` da postane verificabilan log

### I.2 Merkle stabla

**Princip**: balansirano binarno stablo gdje su listovi hash-evi pojedinih dokumenata, unutarnji čvorovi hash konkatenacije djece. Korijen čini *root commitment* nad cijelim setom — može se javno objaviti dnevno (transparency log).

**Reference**:
- Merkle 1980, "Protocols for Public Key Cryptosystems" (originalni patent)
- Laurie, Langley, Kasper 2013, RFC 6962 — Certificate Transparency

**Primjena u LegalTech**:
- Dnevni Merkle root nad svim `download_log` redovima → objavljen na public chain (Bitcoin OP_RETURN, Ethereum log) ili samo u javnom GitHub fileu → daje *cryptographic audit trail proof* da Davatelj nije retroaktivno mijenjao logove (forensic dokaz pred sudom)

### I.3 Detached signatures (RFC 3161 / RFC 5652)

**Princip**: dokument se ne mijenja, ali odvojena signature datoteka (ASN.1 strukturirana) sadrži timestamp + hash + javni ključ. Vremenski žig može biti od QTSP-a (npr. FINA u Hrvatskoj) za eIDAS-validan dokaz.

**Reference**:
- RFC 3161 — Time-Stamp Protocol (TSP)
- eIDAS Regulation 910/2014, Art. 41 (qualified electronic time stamps)
- FINA TSA: https://www.fina.hr (HR akreditirani QTSP)

**Primjena u LegalTech**:
- PRO korisnik može (kao add-on) dobiti eIDAS-validan timestamp na svoj generirani docx → koristit u sudu kao dokaz "ovaj dokument postojao je u ovo vrijeme"
- Davatelj NE potpisuje sadržaj (samo timestamp); izbjegava se odgovornost za točnost

### I.4 Content-addressed storage

**Princip**: dokumenti se identificiraju **hash-em sadržaja**, ne UUID-om ili sekvencijalnim ID-em. Ako dva korisnika generiraju isti dokument, dijeljena je referenca (deduplikacija + nepromjenjivost).

**Reference**:
- Git object model (Linus Torvalds, 2005)
- IPFS specifikacija (Benet 2014)

**Primjena u LegalTech**:
- Predlošci se identificiraju `content_hash` umjesto `version_string` → automatska deduplikacija + lakši audit ("verzija X = sha256:abcd...")

---

## §II — Offline-first PWA i client-side arhitekture

### II.1 Service Worker pattern

**Princip**: JavaScript skripta koja sjedi između browsera i mreže, presreće requests. Može cache-irati, raditi offline, push notifikacije.

**Reference**:
- W3C Service Workers Specification (Russell, Song, et al. 2014, latest 2024)
- Google Web Fundamentals — Offline Cookbook

**Primjena u LegalTech**:
- Aplikacija se cache-ira lokalno; korisnik može generirati docx offline (nakon prvog load-a)
- Smanjuje server trošak (manje requests prema Streamlit Cloud)
- **K2 kandidat** u redu prioriteta

### II.2 IndexedDB

**Princip**: lokalna baza u browser-u (do nekoliko GB). Strukturirana, indeksirana, transactional.

**Reference**:
- W3C Indexed Database API spec
- MDN IndexedDB tutorial

**Primjena u LegalTech**:
- Korisnikove forme persistirane lokalno (auto-save) — recovery ako browser crash-ne
- Generirani dokumenti cached lokalno — re-download bez novog server hit-a
- Privatnost: sadržaj nikad ne ide preko mreže (lokalna obrada)

### II.3 IndexedDB + Web Crypto API za client-side encryption

**Princip**: forme i dokumenti se enkriptiraju **u browseru** prije pohrane u IndexedDB; ključ derivira iz korisničke lozinke (PBKDF2-SHA256). Server nikad ne vidi plaintext.

**Reference**:
- W3C Web Cryptography API
- OWASP Cryptographic Storage Cheat Sheet

**Primjena u LegalTech**:
- Korisnikovi privatni podaci (OIB-i, brojevi računa, klauzule s povjerljivim sadržajem) ostaju enkriptirani na njegovom uređaju
- Privatna pretplata: ako korisnik izgubi lozinku, gubi pristup; Davatelj ne može oporaviti
- Argument za *ne-mogućnost* dolaska sadržajem dokumenta → smanjuje GDPR exposure

### II.4 PWA installable manifest

**Princip**: `manifest.json` opisuje aplikaciju (ime, ikona, start URL, theme); browseri (Chrome, Edge, Safari) je tretiraju kao standalone app — može biti "instalirana" na desktop/home screen.

**Reference**:
- W3C Web App Manifest specification
- Chrome PWA install criteria

**Primjena u LegalTech**:
- Korisnik dodaje aplikaciju kao desktop ikonu → izbjegava Streamlit branding u browser tab-u
- Bolji UX za frequent users

---

## §III — Idempotentni webhook obrasci

### III.1 Idempotency key u tablici

**Princip**: svaka externa poruka (Stripe webhook event) ima jedinstven `event_id`. Tablica događaja ima UNIQUE constraint na taj ID. Drugi pokušaj insert-a → IGNORE → nema dvostruke obrade.

**Reference**:
- Stripe Webhook Documentation, "Handle duplicate events"
- IETF draft "The Idempotency-Key HTTP Header Field"

**Primjena u LegalTech**:
- `stripe_events` tablica u K3 schema (postoji)
- Isti pattern primjenjiv na bilo koji vanjski signal: refund, dispute, FINA notifikacija, sudski webhook

### III.2 Cron reconciliation

**Princip**: dnevno (ili satno) skripta uspoređuje stanje u našoj bazi vs stanje kod externog sustava (Stripe). Ako se razilaze (npr. neki webhook je propušten), reconciliation skripta sinkronizira.

**Reference**:
- Hellerstein, Stonebraker 2005, "Readings in Database Systems" — eventual consistency patterns
- Stripe Connect Best Practices, "Reconciliation"

**Primjena u LegalTech**:
- Dnevni cron koji povlači `stripe.subscriptions.list()` i provjerava `entitlements` u Supabase — ako neki past_due/canceled nije reflektiran, fix
- Koristi Cloudflare Cron Triggers (free tier) ili Supabase scheduled function

### III.3 Outbox pattern

**Princip**: svaka akcija koja zahtijeva externu komunikaciju **prvo** se zapiše u lokalni `outbox` tablicu unutar iste transakcije kao biz logika. Pozadinski worker periodically pošalje event-e iz outbox-a. Garantira "at-least-once delivery" čak i ako mreža/external sustav padne između biz logike i poziva.

**Reference**:
- Microservices Patterns (Richardson 2018), pp. 110-115
- Debezium CDC dokumentacija (Outbox event router)

**Primjena u LegalTech**:
- Refund processing: `UPDATE entitlements; INSERT INTO outbox (target='email', payload='refund-confirmation')` u istoj transakciji → pozadinski email worker pošalje, retry on fail

---

## §IV — Schema versioning i registry obrasci

### IV.1 Generator versioning registry (K4 kandidat)

**Princip**: svaka generator funkcija ima `(generator_id, version, schema_in, schema_out, sha256_of_function_bytecode)` zapis u JSON registry-u. Stari outputi reproducibilni: `git checkout <sha> && python -m generators.replay <serial>` daje bit-by-bit istu docx datoteku.

**Reference**:
- MLflow Model Registry (forenzički audit za ML modele, ali pattern je generic)
- Confluent Schema Registry

**Primjena u LegalTech**:
- Audit defense: ako korisnik tvrdi "ovaj dokument je drugačije izgledao kad sam ga generirao 6 mjeseci ranije", possible to recreate
- Compliance argument: "ovo nije AI, ovo je registry verzije X.Y" (deterministic proof)

### IV.2 JSON Schema validation

**Princip**: prije save-a u DB ili slanja preko API-ja, payload se validira protiv JSON Schema (draft 2020-12). Schema je versioned uz svoj `$id`.

**Reference**:
- JSON Schema specifikacija 2020-12
- OpenAPI 3.1 (koristi JSON Schema)

**Primjena u LegalTech**:
- Sve forme imaju JSON Schema → validation prije generiranja docx-a (catch typos rano)
- Schema je dio registry-a (točka IV.1)

### IV.3 Migrations s expand/contract pattern

**Princip**: schema se mijenja u dva koraka: (1) expand (dodaj novu kolonu, oba write paths zapisuju), (2) contract (obriši staru kolonu). Cijelo vrijeme app radi bez downtime-a.

**Reference**:
- Refactoring Databases (Ambler, Sadalage 2006)
- PostgreSQL ALTER TABLE bez locks

**Primjena u LegalTech**:
- Supabase migracije (Postgres) slijede ovaj pattern → app na Streamlit Cloud nikad ne pada zbog DB schema change-a

---

## §V — Deterministički templating i HTML→DOCX

### V.1 Pure-function templating

**Princip**: generator je `def generate(data: dict) -> str`, čista funkcija bez side-effekata. Isti input → isti output. Lako testabilno, lako auditabilno, izvan AI Act scope-a.

**Reference**:
- Jinja2 dokumentacija (template engines best practices)
- Functional programming principles (Hughes 1989, "Why Functional Programming Matters")

**Primjena u LegalTech**:
- 60+ generatora u `generatori/*.py` slijedi ovaj pattern (postoji)
- AI Act Article 3(1) "AI system" definition zahtijeva inferenciju — pure function NIJE AI

### V.2 HTML kao međuformat

**Princip**: generator vraća HTML string, ne direktno docx. HTML→DOCX konverter je odvojen modul. Prednost: HTML se može preview-ati u browser-u (live preview), lako mijenjati stil bez da diram generator logiku.

**Reference**:
- python-docx HTMLParser (custom)
- Pandoc (universal document converter)

**Primjena u LegalTech**:
- `docx_export.py` je HTML→DOCX (postoji)
- Future: dodati HTML→PDF kroz weasyprint (alternative format download)

### V.3 OOXML core properties za audit

**Princip**: Office Open XML (ISO/IEC 29500) ima `core.xml` s metadata polja: `dc:identifier`, `dc:creator`, `cp:created`. Forenzički alati (ExifTool, Microsoft Office Document Properties) ih čitaju.

**Reference**:
- ISO/IEC 29500-1:2016 (Office Open XML)
- Petitcolas, Anderson, Kuhn 1999, "Information Hiding: A Survey", IEEE 87(7) — forensic vs robust watermarking distinkcija

**Primjena u LegalTech**:
- Per-doc serial broj u `dc:identifier` (postoji, K3 watermark.py)
- Forensic chain: serial → `download_log` → user_id

### V.4 Hrvatski jezik / padeži formal

**Princip**: hrvatski pravni dokumenti zahtijevaju gramatičku ispravnost padeža (vokativ, lokativ, instrumental). Determinističko rješenje: rječnik pravila + lookup tablica iznimaka. NE LLM, ne ML.

**Reference**:
- Babić, Ham, Težak 1992, *Hrvatski školski pravopis*
- Pomocne._padez_ime() (postoji u APLIKACIJA)

**Primjena u LegalTech**:
- Sve forme prolaze kroz padežne funkcije prije renderiranja → "tužitelj Ivan Horvat" → vokativ "tužitelju Ivane Horvat" itd.

---

## Što ovaj katalog NE sadrži (eksplicit eksluzija)

| Domena | Razlog isključenja |
|---|---|
| LLM inferencija (vLLM, llama.cpp, Ollama) | Aktivira AI Act Article 3(1) "AI system" definiciju |
| Klasifikatori (CNN, Transformer, NHP) | Annex III pt. 8 high-risk + nadripisarstvo |
| Predikcijski modeli (GRU, LSTM, ARIMA) | Annex III pt. 8 |
| Generative AI za sadržaj dokumenata | Article 50 transparency obligation + nadripisarstvo |
| Personalizacija based na korisnikovom slučaju | High-risk + nadripisarstvo |
| Recommender sistemi ("ovaj dokument vam treba") | High-risk + nadripisarstvo |
| Conformal prediction, Bayesian inference | Sve su ML — out of scope |
| Speech-to-text, OCR pravnih dokumenata | Annex III ovisno o kontekstu, riskantno |

Ako budući kandidat predloži nešto iz ove tablice, **automatski ELIMINIRAN** u Agent 1 IZVIDNIK fazi (Pravilo 33 v1 LEGAL).

---

## Kako koristit ovaj katalog (input stack za GLAVNI INŽENJER LEGAL pipeline)

Svaki ciklus počinje s:

```
INPUT_STACK:
  - LEGAL_ARHITEKTURA.md (ovaj fajl, primarni)
  - APLIKACIJA/README.md (sekcije: stack, generatori, monetizacija)
  - APLIKACIJA file tree (output `find . -name "*.py" -not -path "*/.venv/*"`)
  - Output Agenta <N-1>: <path>
PRAVILNIK: GLAVNI_INZINJER_PRAVILA_LEGAL_v1.md (Pravila L1-L6, naslijeđena 1-32 iz RIJEKA_PRATILAC v1-v4)
PIPELINE: GLAVNI_INZINJER_AGENTI_LEGAL.md
```

Agent 2A FILOZOF NE čita ovaj fajl (Pravilo 35 strikt kineski zid). Filozof vidi samo kulturološke izvore (književnost, mitologija, antropologija, povijest knjizevnosti, filozofija).

---

## Geneza

Nastalo: 2026-04-27 popodne.
Razlog: korisnikova primjedba da je BRZ_MOZAK metodologija primjenjena na APLIKACIJA inline (bez subagenata) jer originalna pravila v5 referenciraju RIJEKA_PRATILAC ML domenu. Nužna je adaptacija pravila + zamjena input stack-a za LegalTech specifične primitive.
Cilj: omogućiti pun 5-agentni P2 hibridni pipeline za K1, K2, K4 LegalTech kandidate bez rizika da Agent 2B INŽENJER predloži AI klasifikator (što bi aktiviralo AI Act high-risk + nadripisarstvo).
