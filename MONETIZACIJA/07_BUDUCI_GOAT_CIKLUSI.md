# 07 — Budući GOAT ciklusi

> **Datum**: 2026-04-27
> **Status**: REGISTAR — Ciklusi se pokreću po triggeru, ne preventivno
> **Format**: per `GOAT/CIKLUS_1_2026-04-27.md` template

---

## SAŽETAK

| Ciklus | Tema | Trigger | Procijenjen trošak |
|---|---|---|---|
| **C1** ✅ | Odabir MOR platforme (Polar.sh winner) | Završen 2026-04-27 | 75k tokena |
| **C2** | Pravna struktura (paušal vs j.d.o.o. vs d.o.o.) | Faza 1 start | 10-15k tokena |
| **C3** | Hosting platforma (Streamlit vs Hetzner vs Render vs Fly) | Faza 3 trigger | 10-15k tokena |
| **C4** | Računovodstveni servis (in-house vs servis vs SaaS) | Faza 1 — istraživanje 2-3 ponude | 5-10k tokena |
| **C5** | Cjenovna struktura finalna (€9 vs €12, trial duration, freemium limit) | Faza 3 prije A/B testa | 10-15k tokena |
| **C6** | eRačun rješenje (FINA vs Helena vs custom Peppol) | Faza 3 PDV obveza ulazi | 5-10k tokena |
| **C7** | DevOps PaaS (Coolify vs Dokploy vs DIY) | Faza 3 Hetzner migracija | 5-10k tokena |
| **C8** | B2B billing tool (Polar manual vs Stripe Billing vs Chargebee) | Faza 4 5+ B2B klijenata | 10-15k tokena |
| **C9** | SOC 2 vs ISO 27001 (compliance certification) | Faza 4 enterprise klijent traži | 10-15k tokena |

---

## C2 — Pravna struktura (Faza 1 trigger)

### Kontekst
`02_PRAVNA_STRUKTURA.md` već daje preliminarnu preporuku **j.d.o.o.**. ALI:
- Razlog za GOAT C2 je **3-opcijska decision** s nuancama porez vs administrativni teret vs migration path
- Dodatni input: **lokalni računovodstveni servis** može imati specifičnu preporuku temeljenu na konkretnoj situaciji

### 3 opcije za GOAT C2
1. **Direktno j.d.o.o.** (preporuka iz dok 02)
2. **Paušalni obrt fazno** (3-6 mj kao test market) → konverzija u j.d.o.o.
3. **Direktno d.o.o.** (preskoči j.d.o.o. fazu — manje administracije, više TK)

### Ključni kriteriji za vaganje
- K1 Trošak prve godine
- K2 Pravna sigurnost (GDPR voditelj obrade, nadripisarstvo)
- K3 Skalibilnost (kada migrirati gore)
- K4 Tax optimization (porez na dobit + dohodak od kapitala)
- K5 Vendor compatibility (Polar.sh KYC accepts what?)

### Trigger
Pokreće se **prije** korak 1.3 u `06_MILESTONES.md` (otvaranje START platforma sesije).

---

## C3 — Hosting platforma (Faza 3 trigger)

### Kontekst
`03_TEHNICKI_STACK.md` predlaže Hetzner CPX22 za Faza 3, ali **kvantitativni** decision matrix nije napravljen formalno. Faza 3 trigger = 50+ platežnih usera.

### 3-4 opcije
1. **Streamlit Cloud Pro** (kad postoji — još ne 2026-04)
2. **Hetzner CPX22 + Coolify**
3. **Render.com Pro**
4. **Fly.io**

### Ključni kriteriji
- K1 Mjesečni trošak na 100 platežnih userva volumen
- K2 EU data residency (GDPR)
- K3 DevOps overhead (auto vs manual)
- K4 Cold start performance
- K5 Skalibilnost na 1000 usera

---

## C4 — Računovodstveni servis (Faza 1 trigger)

### Kontekst
HR računovodstvo je kompleksno. Solo dev često griješi → kazne. Outsourcing je standard.

### 3 opcije
1. **Lokalni servis** (Aning, Brojevi, Aestus, mali agencije Zagreb) — 100-200 €/mj
2. **SaaS knjigovodstvo** (Minimax, MojePoslovanje) — 60-80 €/mj + ručni unos
3. **Hibrid** — SaaS + povremeni paid pregled (~50 €/mj + 200 €/quarter)

### Ključni kriteriji
- K1 Mjesečni trošak
- K2 Risk pri grešci (PU kazne)
- K3 Vrijeme dev-a tjedno (10h vs 1h)
- K4 eRačun integracija (Faza 3 obvezna)
- K5 PDV handling experience

### Trigger
Pokreće se **istovremeno s Fazom 1** (treba ti servis prije nego pravna osoba postane operativna).

---

## C5 — Cjenovna struktura finalna (Faza 3 trigger)

### Kontekst
`04_CJENOVNI_MODEL.md` daje preliminarne brojke (9€/29€). Faza 3 podaci o A/B testovima → finalni decision.

### 3-4 opcije za svaki sub-decision
**Sub-decision A: PRO cijena**
1. €9/mj baseline
2. €12/mj +33%
3. €7/mj -22%

**Sub-decision B: Free trial duration**
1. 7 dana
2. 14 dana
3. 30 dana

**Sub-decision C: Annual discount %**
1. 15%
2. 20%
3. 25%

**Sub-decision D: Free tier limit**
1. 5 dok/mj
2. 10 dok/mj
3. 3 dok/mj

### Ključni kriteriji
- K1 Conversion rate (FREE → PRO)
- K2 Churn rate (PRO retention)
- K3 LTV impact
- K4 CAC payback period

### Trigger
Pokreće se **nakon** ~2 mj A/B test podataka iz Faze 3. Nije preventivni decision.

---

## C6 — eRačun rješenje (Faza 3 PDV obveza)

### Kontekst
Od 2026-01-01 svi PDV obveznici obvezni zaprimati eRačune. Faza 3 ulazi u PDV obvezu (~40k EUR/god prihod).

### 3 opcije
1. **FINA Moj eRačun** (besplatno, web-only)
2. **Helena** (~5-15 €/mj, API)
3. **Custom Peppol** (Faza 4, full control)

### Ključni kriteriji
- K1 Trošak/mj
- K2 API integracija (auto-fakturiranje za Polar uplate)
- K3 B2B klijent compatibility (custom invoice fields)
- K4 Dev time za integraciju

### Trigger
Pokreće se **kad prihod prijeđe 30k EUR/god** (3 mj prije PDV obveze).

---

## C7 — DevOps PaaS (Faza 3 trigger)

### Kontekst
Hetzner sam je VPS. Treba PaaS layer za auto-deploy, SSL, monitoring.

### 3 opcije
1. **Coolify** (OSS, popular, active)
2. **Dokploy** (OSS, mlađa alternativa)
3. **DIY** (Caddy + Docker + GH Actions)

### Ključni kriteriji
- K1 Setup time (1h vs 1 dan)
- K2 Ongoing maintenance (security updates)
- K3 Feature set (auto SSL, backups, monitoring)
- K4 Vendor lock-in / migration risk

### Trigger
Pokreće se **istovremeno s Faza 3 task 3.1** (Streamlit → Hetzner migracija).

---

## C8 — B2B billing tool (Faza 4 trigger)

### Kontekst
Polar.sh je B2C-fokusiran. B2B (5+ klijenata) zahtjeva drukčije billing.

### 3 opcije
1. **Polar manual** (extended) — ručni invoice za B2B, Polar samo B2C
2. **Stripe Billing** (više komercijalan, manje friendly EU)
3. **Chargebee** (industry standard, skuplji)

### Ključni kriteriji
- K1 Custom billing cycles (quarterly, annual)
- K2 Net 30/60 payment terms
- K3 PO/predračun support
- K4 eRačun integracija (Peppol)
- K5 Cijena (% per tx)

### Trigger
Pokreće se **kad imaš 5+ B2B klijenata** (manual billing postaje neizdrživ).

---

## C9 — Compliance certification (Faza 4 enterprise traži)

### Kontekst
Banka klijent može tražiti SOC 2 / ISO 27001 / HRPGDPR cert.

### 3 opcije
1. **SOC 2 Type I** — ~10-20k €, 6-12 mj
2. **ISO 27001** — ~30k €+, 12-18 mj
3. **HR DPA pisana potvrda od AZOP-a** — besplatno, slabiji marketing weight

### Ključni kriteriji
- K1 Klijent traženje (mandatory for ugovor close?)
- K2 Trošak vs ugovor vrijednost (LTV B2B klijenta)
- K3 Vrijeme do certificate
- K4 Multi-klijent reusability

### Trigger
Pokreće se **kad enterprise klijent eksplicit traži** (ne preventivno — skup je process).

---

## Pravila pokretanja

### Kad pokrenuti GOAT ciklus
1. **Discrete decision** s 3-4 jasno definirane opcije
2. **Trigger** je nastupio (faza, prihod, klijent)
3. **Trošak ne-odluke** > trošak ciklusa (~10-15k tokena)

### Kad NE pokrenuti
1. **Već donesena odluka** — ne re-litigate ako sub-dokument već daje preporuku temeljenu na konkretnoj evidence
2. **Nema 3+ opcije** — onda nije decision matrix problem, samo "should I or shouldn't I"
3. **Premali ulog** — npr. "domain registrar Cloudflare vs Namecheap" — 2 €/god razlika, nije vrijedno ciklusa

### Format svakog ciklusa
Per `GOAT/CIKLUS_1_2026-04-27.md`:
1. **TRŽIŠNI ISTRAŽIVAČ** — subagent s clean context, WebSearch+WebFetch, prazan sheet
2. **VAGAR** — orkestrator (ti + Claude), inicijalna decision matrix
3. **REVIZOR** — neovisan subagent fact-check 4 nasumično odabranih tvrdnji
4. **Refrakcija** — V2 matrix s korekcijama
5. **PREPORUKA** — final decision dokument u `GOAT/PREPORUKA_<topic>.md`

### Numeracija
- C1 ✅ MOR (završen)
- C2... bilo koja sljedeća (ne mora biti redom)
- Trenutno aktivni se prati u `MONETIZACIJA/README.md` audit log
