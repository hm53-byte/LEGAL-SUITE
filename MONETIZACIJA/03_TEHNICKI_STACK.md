# 03 — Tehnički stack: hosting, plaćanja, data residency

> **Datum**: 2026-04-27
> **Polazna točka**: Streamlit Cloud + Cloudflare Workers + Supabase + Polar.sh (per `GOAT/PREPORUKA_MOR.md`)
> **Cilj**: definirati evoluciju stack-a kroz Faze 0-4

---

## SAŽETAK STACKA PO FAZAMA

| Komponenta | Faza 0-1 (MVP) | Faza 2 (do 50 platežnih) | Faza 3 (50-500) | Faza 4 (B2B) |
|---|---|---|---|---|
| **Web app** | Streamlit Cloud (free) | Streamlit Cloud + Polar | **Hetzner CPX22** (~8 €/mj) | Hetzner CPX32 + load balancer |
| **MOR / Plaćanja** | Manual (Faza 0) → Polar.sh | Polar.sh | Polar.sh + B2B invoice | Polar.sh B2C + direktna B2B |
| **Edge worker** | Cloudflare Workers (free) | CF Workers (free) | CF Workers Paid (~5 $/mj) | CF Workers + custom |
| **DB** | Supabase free | Supabase Pro (~25 $/mj) | Supabase Pro | Supabase Team / self-hosted |
| **Audit chain** | Supabase + Postgres triggers | isto | isto | + WORM storage (Hetzner Storage Box) |
| **eRačun** | nije primjenjivo | FINA Moj eRačun (free) | isto | Helena ili custom Peppol |
| **Knjigovodstvo** | nije primjenjivo | Eksterno (~150 €/mj) | isto | + interni controller |
| **Domena** | streamlit.app subdomena | **vlastita domena** (~12 €/god) | isto | isto |
| **Fiksni mjesečni trošak** | 0 € | **~25-40 $/mj** + pravna struktura | **~50-70 €/mj** | varijabilno |

---

## 1. Hosting — odluka po fazama

### 1.1 Faza 0-1: Streamlit Cloud (status quo)
**Razlozi za zadržavanje:**
- Free tier dostatno za 0-50 platežnih usera
- Bez DevOps overhead-a (deploy = `git push`)
- Auto SSL, CDN, restart
- **AWS infrastrukturna IP** — *minus*: e-Oglasna scraping bi puknuo na cloudflare anti-bot, *plus*: nije relevantno jer e-Oglasna NE radimo (vidi 01_PRAVNA_ANALIZA_SCRAPERA.md)

**Limitacije:**
- 1 GB RAM, 1 CPU core efektivno
- Restart nakon ~30 min neaktivnosti (cold start ~10-30s)
- Nema persistent volume — `entitlements.py` `audit_chain.py` rade samo s Supabase backed
- Nema cron / background workers — sve je on-demand

### 1.2 Faza 2-3: Hetzner CPX22 (Frankfurt)
**Trigger za migraciju**: 50+ platežnih usera ILI prvi B2B klijent (NPL/banka).

**Razlozi:**
- **Dedicirana IP** (jedan korisnik = jedan IP iz pool-a, predvidljivo)
- **EU/Frankfurt data residency** — GDPR friendly default ([Hetzner GDPR](https://www.hetzner.com/cloud-made-in-germany))
- **8 €/mj** (CPX22: 2 vCPU, 4 GB RAM, 80 GB NVMe SSD, 20 TB transfer) — od **2026-04** Hetzner povećao s 5,99 → 7,99 €/mj
- **Backup snapshots** za 20% cijene (~2 €/mj)
- **DDoS zaštita** uključena
- **No vendor lock-in** — možeš migrirati u sat vremena

**Migracijski plan**:
1. Setup Hetzner CPX22 + Caddy/Traefik za SSL
2. Streamlit kao systemd service iza reverse proxy-ja
3. Supabase ostaje vanjski (managed) — ne self-hostaj zbog kompleksnosti
4. Polar.sh ostaje (MOR ne ovisi o lokaciji web app-a)
5. Domain DNS prebaciš na Hetzner IP

**Risk**: full DevOps responsibility — ti si sysadmin, ti updateaš OS, ti gledaš logs.

**Mitigacija**: Coolify (self-hosted PaaS na Hetzner-u, OSS) — daje ti push-to-deploy + SSL + monitoring uz ~30 min setup. Alternativa: Dokploy.

### 1.3 Faza 4: Hetzner CPX32 + LB
**Trigger**: 200+ platežnih usera ILI prvi enterprise klijent (banka).
- CPX32 (8 GB RAM) ~13 €/mj
- Hetzner Load Balancer ~5 €/mj
- Multi-region (EU + možda US-East ako stranicu B2B traži)
- Storage Box (~10 €/mj 1 TB) za WORM audit chain

**Alternativa Faza 4**: Render.com Pro (~25 $/mj per service) ako želiš managed DevOps. Skuplji ali zero-touch.

### 1.4 Tablica usporedba (zašto NE druge platforme)

| Platforma | Trošak/mj | EU regija | Cold start | Verdict |
|---|---|---|---|---|
| **Streamlit Cloud** | 0 € | US (Streamlit infra) | ~10-30s | OK Faza 0-1, NE Faza 2+ (data residency) |
| **Render** | 25 $/mj | EU (Frankfurt) | <1s | OK ali skuplji od Hetzner-a |
| **Fly.io** | ~5-15 $/mj | EU (Amsterdam, Frankfurt) | <1s | OK ali manji ekosystem |
| **Vercel** | 20 $/mj | global edge | 0s | NE (Streamlit ne ide na serverless) |
| **Hetzner CPX22** | 8 €/mj | DE Frankfurt | 0s | **PREPORUKA Faza 2+** |
| **Contabo VPS** | 5-10 €/mj | DE | 0s | OK ali manje pouzdano (manji CDN) |
| **AWS Lightsail** | ~10 $/mj | EU (Frankfurt) | 0s | OK ali AWS billing kompleksniji |

---

## 2. Plaćanja — Polar.sh (potvrđeno iz GOAT C1)

### 2.1 Status
**Pobjednik GOAT Ciklus 1**: Polar.sh sa scoreom 4.20/5 (vs Paddle 3.90, LMSQZY 2.45). Plan migracije Stripe → Polar dokumentiran u `GOAT/PREPORUKA_MOR.md` (~345 LOC, 5-7 dana).

### 2.2 Polar.sh KYC za HR d.o.o.

Iz istraživanja danas (2026-04-27):
- Polar koristi **Stripe Connect Express** za payout — Croatia eksplicit podržana
- KYC dokumenti: passport/ID + selfie (Stripe Identity)
- Za d.o.o. dodatno: company registration documents, director ID, **UBO (ultimate beneficial owner) podaci**
- HR posebnost: **MBS + OIB pravne osobe + adresa sjedišta + zastupnik podaci**
- **Account review process** — Polar može vršiti review prije aktivacije (pogotovo legal SaaS jer ima više regulatornog rizika)

**Akcija (Faza 2)**:
1. Otvori Polar account u sandbox modu
2. Pošalji preliminarni upit Polar support-u: *"Pravni SaaS u Hrvatskoj koji generira sudske dokumente — postoji li posebni acceptable use policy ili dodatni review koji mi treba znati prije submita?"*
3. Pripremi KYC dokumente prije submit-a (osvjetlost selfija, izvod iz sudskog registra ne stariji od 30 dana)

### 2.3 Polar.sh integracijski rizici

Iz GOAT C1:
- API versioning policy nije publicly dokumentirana → **pin SDK verziju** + integration test pri svakoj nadogradnji
- Cloudflare Bot Fight Mode može blokirati webhook delivery → whitelist Polar webhook source IPs
- Manje history (open-source platforma) → sekundarni fallback plan: dokumentiran Paddle path ako Polar postane unstable

### 2.4 B2B billing (Faza 4)
Polar.sh primarno ciljani na **B2C SaaS subscriptions**. Za **NPL agencije i banke**, koje očekuju:
- 30-60 dana payment terms
- POnara, predračun, izvornik fakture
- eRačun (FINA Peppol)
- Custom billing cycle
- Quarterly invoicing

→ **Polar nije pravi tool za B2B**. **Plan**:
- B2C ostaje na Polar.sh
- B2B billing radiš **direktno** preko HR računovodstvenog servisa s eRačun integracijom
- B2B usera handle-aš ručno (manual entitlement aktivacija u entitlements.py)
- Tek na 5-10 B2B klijenata razmotri proper B2B billing tool (Stripe Billing, Chargebee — ali sve EU rezidentne opcije, **GOAT C5+ za detalje**)

---

## 3. Database — Supabase

### 3.1 Status
- Već u stack-u (`cloud/supabase_schema.sql`, `cloud/0007_audit_chain.sql`)
- Free tier: 500 MB DB, 1 GB file storage, 2 GB transfer
- Pro: 25 $/mj (8 GB DB, 100 GB transfer, dnevni backupi)

### 3.2 Trigger za upgrade
- **Free → Pro**: kad korisnička baza prijeđe ~500 PRO usera (audit_chain najbrže puni)
- **Pro → Team (599 $/mj)**: kad B2B klijent zatraži dedicated isolation ili PITR (point-in-time recovery)

### 3.3 Data residency
Supabase nudi izbor regije pri kreiranju projekta:
- **eu-central-1 (Frankfurt)** ili **eu-west-1 (Ireland)** — preporuka za HR
- **GDPR-compliant by default** kad je projekt u EU regiji

**Akcija (sada)**: provjeri trenutnu regiju u Supabase dashboard-u. Ako je US, **migracija** je nužna prije Faze 2.

### 3.4 Self-hosted alternativa
**Faza 4 razmatranje**: ako enterprise klijent (banka) zahtjeva self-hosted DB (njihova infrastruktura, on-prem):
- Supabase je open-source — može se self-hostati
- Trošak: 1-2 mj DevOps engagement (~2-5k € outsourced)
- ROI: samo ako enterprise ugovor > 50k €/god

---

## 4. Edge / API gateway — Cloudflare Workers

### 4.1 Status
- `cloud/cf_worker_stripe.ts` (rename → `cf_worker_polar.ts` u Faza 2)
- Free tier: 100k req/dan, 10ms CPU per req

### 4.2 Trigger za upgrade
- Free → Paid (5 $/mj baseline + per request): kad webhook traffic prijeđe ~3M req/mj (skoro nemoguće za solo SaaS)
- **Praktično**: ostaje free do Faze 4

### 4.3 Što ide na Workers, što ne
**Workers = OK za:**
- Polar webhook receiver (ovaj kojeg već imaš)
- Auth proxy / token refresh
- Rate limiting / abuse prevention

**Workers ≠ OK za:**
- Streamlit app (ne radi na serverless, treba persistent process)
- Heavy data processing (10ms CPU limit)
- Database connections (treba HTTP client, ne native PG driver)

---

## 5. Domena + brand

### 5.1 Domena
Trenutno: `legal-suite-flh3jnmcj5kc7jp5y9w9eb.streamlit.app` (auto-generirana Streamlit subdomena)

**Faza 1**: kupi vlastitu domenu (~12 €/god)
- **Predložene varijante**:
  - `legalsuite.hr` (provjeri dostupnost na CARNet WHOIS)
  - `legalsuite.com.hr`
  - `pravoassist.hr`
  - `legalix.hr`

**Hosting domene**: Cloudflare Registrar (cijene at-cost, oko 10 €/god .com, .hr ide preko CARNet ~25 €/god)

### 5.2 Email
**Profesionalni email** (Faza 1):
- Google Workspace Business Starter (~6 €/mj/user) — oversoldano
- **Zoho Mail Free** (5 user, 5 GB) — preporuka za solo dev fazu
- ProtonMail Business (~7 €/mj/user) — privacy oriented, EU-rezidentno

**Polar.sh će tražiti e-mail s domenom kompatibilnom s d.o.o. nazivom** za KYC (npr. `hrvoje@legalsuite.hr`, ne gmail).

---

## 6. Audit, monitoring, ops

### 6.1 Audit chain (već imaš)
- `audit_chain.py` + `cloud/0007_audit_chain.sql` — hash chain u Supabase
- Forenzički branjivo (per memory `feedback_brz_mozak_inzenjerski`)
- **Faza 4**: dodaj WORM storage (Hetzner Storage Box) kao tertiary archive

### 6.2 Error tracking
**Faza 0-1**: ništa — Streamlit logs su dovoljno
**Faza 2+**: Sentry (free do 5k events/mj) — preporuka

### 6.3 Uptime monitoring
**Faza 1+**: Better Stack ili UptimeRobot (free tier)
**Faza 4**: Better Stack Pro (10 $/mj) za PagerDuty integration

---

## 7. Sigurnost — minimum

### 7.1 Faza 0-1
- Streamlit secrets (env vars) za API ključeve — **NE git commit-aj**
- HTTPS automatski preko Streamlit Cloud
- 2FA na svim računima (GitHub, Streamlit, Supabase, Polar, Hetzner)

### 7.2 Faza 2+
- Hetzner firewall (samo 22, 80, 443) + fail2ban za SSH
- Cloudflare proxy (DDoS + WAF) ispred Streamlit endpoint-a
- Backup encryption (Restic + age + S3-compatible Hetzner Object Storage)
- **Vault** za secrets (Hashicorp Vault self-hosted, ili Bitwarden Send za jednokratne)

### 7.3 Faza 4 (B2B)
- SOC 2 Type I (~10-20k € uz auditora) — može ti tražiti enterprise klijent
- ISO 27001 (~30k €+) — samo ako bankarski klijent
- Penetration test (~3-7k €) — godišnje preporuka

---

## 8. eRačun (od 2026-01-01 obvezno za PDV obveznike)

### 8.1 Opcije
- **FINA Moj eRačun** — besplatno, jednostavno, ali ručno (preko web sučelja)
- **Helena** (helena.hr) — ~5-15 €/mj, ima API za integraciju
- **Moj eRačun** (mojeracun.hr) — slično
- **Custom Peppol integration** — samo Faza 4 ako trebaš puni control

### 8.2 Preporuka po fazama
- Faza 0-1: nije primjenjivo (nije PDV obveznik)
- Faza 2: FINA Moj eRačun (kad pređeš PDV prag)
- Faza 3: Helena ili Moj eRačun s API-jem (auto-fakturiranje za Polar uplate)
- Faza 4: Helena/custom Peppol za B2B

---

## 9. Stack-related dependencies u kodu

### 9.1 Što već imaš (per `requirements.txt` snimak):
- `streamlit >= 1.28.0`
- `python-docx >= 1.0.0`
- (provjeri dodatno) — `requests`, `httpx`, `beautifulsoup4`, `lxml`, `pypdf` — ako nisu, dodaj kad bude potrebno

### 9.2 Što ćeš dodati (Faza 2):
- `supabase` Python klijent
- `polar-sdk` ili direktni `httpx` calls
- `cryptography` za audit_chain hashing (vjerojatno već imaš)

### 9.3 Što NE dodavati (per `feedback_brz_mozak_inzenjerski`)
- AI/ML libraries (`openai`, `anthropic`, `transformers`, `langchain`) — Pravilo L6 anti-AI drift je in effect
- AI Act 2026 + nadripisarstvo dvije linije obrane → no AI in app code

---

## 10. Sljedeći koraci (mapping na Faze)

**Faza 0 (sljedeća sesija)**:
- Provjeri Supabase regiju (mora biti EU)
- Validiraj `api_sudreg.py` registracijom na sudreg-data.gov.hr
- Skupi cijene HR domena (.hr preko CARNet vs .com.hr)

**Faza 1 (j.d.o.o. otvoren)**:
- Kupi domenu
- Setup Zoho Mail s d.o.o. domenom
- Otvori Polar.sh sandbox account

**Faza 2 (MVP s plaćanjem)**:
- Migrate Stripe → Polar (per `GOAT/PREPORUKA_MOR.md`)
- DPA potpisati s Streamlit, Polar, Supabase
- Setup Sentry (free)

**Faza 3 (skaliranje)**:
- Migrate Streamlit Cloud → Hetzner CPX22 + Coolify
- Cloudflare proxy ispred
- Helena eRačun integracija ako PDV obveznik

**Faza 4 (B2B)**:
- Hetzner CPX32 + Load Balancer
- WORM audit storage
- SOC 2 Type I priprema (ako enterprise traži)
