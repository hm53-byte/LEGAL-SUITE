# 08 — Rizici i mitigacije

> **Datum**: 2026-04-27
> **Format**: Risk register s scoring (P × I), mitigacija, monitoring

---

## SCORING

- **P** (probability): 1 (Vrlo niska) — 2 (Niska) — 3 (Srednja) — 4 (Visoka) — 5 (Vrlo visoka)
- **I** (impact): 1 (Marginalan) — 2 (Mali) — 3 (Srednji) — 4 (Veliki) — 5 (Egzistencijalni)
- **Risk score**: P × I (1-25)

---

## RISK REGISTER

### R01 — AZOP rješenje (komercijalna obrada javnih registara)

| Field | Value |
|---|---|
| Domena | GDPR |
| Probability | **3** (Srednja) |
| Impact | **5** (Egzistencijalni) — kazna do 20M EUR / 4% globalnog prometa |
| Score | **15** |

**Što može poći krivo**:
AZOP zaprimi pritužbu od subjekta čiji su podaci u dokumentu. Otvara postupak. Cross-reference NN + Sudski registar + interni baze = "data matching" obrada. DPIA nije bila napravljena ili je nedovoljna. Voditelj obrade (j.d.o.o.) dobija upozorenje + kaznu.

**Mitigacija**:
1. **DPIA prije Faze 2** — AZOP službeni obrazac, popunjen, spremljen
2. **DPA potpisani** s Streamlit/Polar/Supabase/Hetzner — izvršitelji obrade
3. **Privacy Policy** transparentan + pristanak korisnika za obradu OIB-a u dokumentima
4. **Razdoblje čuvanja** — automatic deletion script po 5-10 godina (procesni zakon limit)
5. **AZOP Help-Desk** — koristi besplatne konzultacije prije launch-a
6. **Pravna konsultacija** — 2-3h s odvjetnikom specijaliziranim za GDPR (~600 €)

**Monitoring**:
- Pratiti AZOP objave rješenja relevantne za legaltech / komercijalne registar baze
- Pretraga "azop.hr/odluke" 1× mjesečno

**Worst-case action plan**:
- Ako kazna upućena: pravni odbojnik + plaćanje (max 10% poslovnog kapitala) + javni response
- Pivot proizvoda na "alat za odvjetnike, ne građane" — manja izloženost

---

### R02 — Nadripisarstvo prijava (HOK, državno odvjetništvo)

| Field | Value |
|---|---|
| Domena | Pravna |
| Probability | **2** (Niska) |
| Impact | **5** (Egzistencijalni) — KZ čl. 311 (nadripisarstvo) — novčana kazna ili zatvor do 1 god |
| Score | **10** |

**Što može poći krivo**:
HOK podnosi prijavu DOU prema Hrvoju Mateju kao fizičkoj osobi (ako je fizička osoba aktivna na proizvodu) ili prema d.o.o.-u. Argument: proizvod izrađuje pravne dokumente uz naplatu = obavlja odvjetničku djelatnost bez položenog pravosudnog ispita.

**Mitigacija**:
1. **Disclaimer** transparentan u UI: "Alat za izradu dokumenata, ne pravna usluga. Korisnik je odgovoran za sadržaj."
2. **NKD** glavna djelatnost **62.01** (računalno programiranje), **NE** 69.10 (pravne djelatnosti)
3. **Marketing copy** — nikad "zamjena za odvjetnika", "automatska tužba", "pravni savjet" → uvijek "alat", "softverska podrška", "templejti"
4. **HOK Partnership pokušaj** (Faza 4) — ako HOK postane partner, neutralizirao si glavnog adversary-ja
5. **Pravna konsultacija** s odvjetnikom HR Bar specijalizacija — 1h, ~150 €

**Monitoring**:
- Pratiti HOK objave o nadripisarstvu (bilten, web)
- Pretraga "nadripisarstvo presuda" Google quarterly

**Worst-case action plan**:
- Ako prijava: pravni odbojnik (~3-5k € obrana 1. instance)
- Pivot na **"closed market"** — proizvod samo za odvjetnike s licencom HOK-a (registracija OIB → check)

---

### R03 — Polar.sh KYC odbijanje

| Field | Value |
|---|---|
| Domena | Operativni |
| Probability | **3** (Srednja) |
| Impact | **3** (Srednji) — odgađa Faza 2 launch ali nije fatalan |
| Score | **9** |

**Što može poći krivo**:
Polar.sh KYC review odbije aplicaciju jer:
- Pravni SaaS je "elevated risk category"
- HR d.o.o. je manje frekventan customer
- Stripe Connect Express ima nepoznate kriterije

**Mitigacija**:
1. **Preliminarni email** Polar support-u prije submit-a — dobiti pisano OK
2. **Backup plan: Paddle migracija** (per `GOAT/PREPORUKA_MOR.md`, dokumentiran path)
3. **Sandbox testing** prije live submit-a — verificiraj svi flow-ovi rade
4. **KYC dokumenti complete**: izvod sudskog registra (≤30 dana), passport HD, selfie + dokument verifikacija

**Monitoring**:
- Polar status page + community Discord (oni objavljuju ako review queue raste)

**Worst-case action plan**:
- Switch na Paddle (5-7 dana migracija) — ostaje funkcionalan stack
- LemonSqueezy je already eliminated po GOAT C1

---

### R04 — Streamlit Cloud limitacije

| Field | Value |
|---|---|
| Domena | Tehnički |
| Probability | **4** (Visoka) — postaje veće s rastom usera |
| Impact | **2** (Mali) — graceful degradation moguć |
| Score | **8** |

**Što može poći krivo**:
- Memory limit (1 GB RAM) — prepuni cache → OOM error
- Cold start ~30s — frustrira nove korisnike
- US infra → GDPR data residency upitno (iako Streamlit ima EU offerings, free tier ne)
- Random restarts → audit chain in-memory podaci izgubljeni (ALI: trajno spremljeni u Supabase)

**Mitigacija**:
1. **Aggressive cache TTL** — 1h max, ne forever
2. **Lazy imports** — ne ucitavati sva 60+ generatora odmah
3. **Supabase persistent** — sve što treba persistance ide u Supabase, nikad in-memory
4. **Migration trigger jasan** — Faza 3 = Hetzner

**Monitoring**:
- Sentry error rate (Faza 2+)
- Supabase audit_chain count vs Streamlit memory pressure (logs)

---

### R05 — Sudski registar API odbija komercijalnu uporabu

| Field | Value |
|---|---|
| Domena | Pravni |
| Probability | **2** (Niska) — CC-BY je explicitan |
| Impact | **3** (Srednji) — gubitak primary HR data izvora |
| Score | **6** |

**Što može poći krivo**:
Iako je `data.gov.hr` CC-BY, MP može uvesti tier sistem (komercijalna licenca, naknada per request). Tvoj proizvod već ovisi o `api_sudreg.py` — ako traži cash, narušava unit economics.

**Mitigacija**:
1. **Pisana potvrda** prije Faze 2 — email `sudski.registar@pravosudje.hr`
2. **Atribucija** u footer pravila uvijek vidljiva
3. **Fallback** — `pretrazi_subjekt()` graceful degradation (vrati "API nije dostupan" placeholder)

**Monitoring**:
- `data.gov.hr` notifikacije za Sudski registar dataset
- Periodična provjera CC-BY licence (1× godišnje)

---

### R06 — AI Act 2026 + memory `feedback_brz_mozak_inzenjerski` violation

| Field | Value |
|---|---|
| Domena | Compliance |
| Probability | **1** (Vrlo niska) — Pravilo L6 je čvrsto u kodu |
| Impact | **5** (Egzistencijalni) — AI Act kazne do 35M EUR / 7% globalnog prometa |
| Score | **5** |

**Što može poći krivo**:
- Slučajni dodatak `openai`/`anthropic` u `requirements.txt` (treba auditirati)
- Subagent ili contributor dodaje LLM call u generator
- Marketing copy spomene "AI" → false advertising + AI Act trigger

**Mitigacija**:
1. **Pravilo L6 anti-AI drift** je čvrsto — `bmh validate-prompt` provjera
2. **Pre-commit hook** koji blocka `openai|anthropic|langchain|transformers` u kodu
3. **Marketing audit** — copy review prije launcha (zabranjeni termini)
4. **Disclaimer** u Privacy Policy — eksplicit "no AI/ML used in document generation"

**Monitoring**:
- `bmh validate-prompt` u CI (per memory existing tool)
- `requirements.txt` git diff alerts (npr. dependabot custom rule)

---

### R07 — Fiskalizacija 2.0 propust

| Field | Value |
|---|---|
| Domena | Porezni |
| Probability | **3** (Srednja) — kompleksan zahtjev, lako pogriješiti |
| Impact | **3** (Srednji) — kazne, ne fatalan |
| Score | **9** |

**Što može poći krivo**:
- 2026-01-01 obvezno zaprimanje eRačuna za PDV obveznike — propust = kazne
- 2027 očekivano izdavanje eRačuna — ako solo dev → Helena/Moj eRačun **MORA** raditi
- B2B klijent traži eRačun specijalan format → tvoj rješenje ne podržava → loss of deal

**Mitigacija**:
1. **Računovodstveni servis** vodi compliance — eksternalize na profesionalca (Faza 1)
2. **Helena** API integracija prije nego ulaziš u PDV obvezu (Faza 3)
3. **Test eRačun flow** u sandbox-u prije pravog klijenta

**Monitoring**:
- FINA Fiskalizacija newsletter
- Računovodstveni servis quarterly review

---

### R08 — Single-founder bus factor

| Field | Value |
|---|---|
| Domena | Operativni |
| Probability | **5** (Vrlo visoka — solo dev) |
| Impact | **3** (Srednji — proizvod stane) |
| Score | **15** |

**Što može poći krivo**:
- Bolest, povreda, mentalno health → proizvod stane
- Burn-out → kvalitet raste sporije, korisnici odlaze
- Akutni problem (hospitalizacija) → korisnici ne dobivaju support → churn

**Mitigacija**:
1. **Dokumentacija** — `CLAUDE.md`, `HANDOFF*.md`, `MONETIZACIJA/*` osigurava transfer of knowledge
2. **Automatske procedure** — što više možeš auto-pilot (no manual entitlement aktivacija)
3. **Acquisition friendly** — proizvod treba biti **prodavabilan** uvijek (čist code, čist legal, čist financijski) — exit option ako trebaš
4. **Faza 4 razmotri suosnivača/co-CEO** ako ozbiljno skalira

**Monitoring**:
- Self-check: 1× mjesečno revisit "do I want to keep doing this?"
- Sleep, exercise, mental load (memory note: PC se gasi noću, dakle radiš zdrave granice — drži)

---

### R09 — Streamlit Cloud / Polar / Supabase platform shutdown

| Field | Value |
|---|---|
| Domena | Vendor risk |
| Probability | **1** (Vrlo niska — sve aktivni products) |
| Impact | **4** (Veliki — migracija nužna) |
| Score | **4** |

**Što može poći krivo**:
- Streamlit Snowflake akvizicija → sunset Streamlit Cloud — korisnik mora premjestiti
- Polar pivot away from Croatia
- Supabase change pricing dramatically

**Mitigacija**:
1. **Multi-vendor strategija** dokumentirana — vidi `03_TEHNICKI_STACK.md`
2. **Code portability** — ne over-couple s vendor-specific features
3. **Hetzner migration plan ready** — 1 dan migracija od Streamlit Cloud-a

---

### R10 — Veliki konkurent ulazi u HR (MS Copilot Legal, Lexis-Nexis, etc.)

| Field | Value |
|---|---|
| Domena | Tržišni |
| Probability | **2** (Niska — HR market premali za top tier) |
| Impact | **3** (Srednji) — gubi growth velocity |
| Score | **6** |

**Mitigacija** (per `05_GTM_STRATEGIJA.md`):
1. **HR specifičnost** — sudovi, OIB, NN integracija, padezi — kompetitor ne može lako replicirati
2. **AI-free pozicija** — diferencijacija u 2026 gdje konkurenti svi mašu AI hype-om
3. **Niža cijena** — €9 nikad ne natuče se s €100+ enterprise tools
4. **Forenzički audit chain** — unique value prop

---

## RISK HEAT MAP

```
                    P=1     P=2     P=3     P=4     P=5
I=5 ─────────────────────  R02  R01     ────────────────
I=4 ──────────────────────────────  R09  ─────────  ────
I=3 ──────────────────────  R10   R03   R07   ────  R08
I=2 ────────────────────────────────────  R04  ───────
I=1 ──────  R05  R06  ───────────────────────────────
```

Top 3 (akcija prioritet):
1. **R01 (AZOP)** — score 15 — DPIA + DPA priority
2. **R08 (Single-founder)** — score 15 — dokumentacija + automation
3. **R02 (Nadripisarstvo)** — score 10 — disclaimer + marketing review

---

## REGULAR REVIEW CYCLE

| Frekvencija | Activity |
|---|---|
| **Mjesečno** | Pregled R01-R03 (high score) — provjeri jesu li nove vijesti, AZOP odluke, HOK objave |
| **Kvartalno** | Full risk register review — adjust scores, dodati nove rizike |
| **Per fazni gate** | Pre-launch security/legal audit — minimum sat vremena samog ili s pravnim/tehničkim mentorom |

---

## OUT-OF-SCOPE rizici (ne pratimo aktivno)

- **HRK reintroduction** (extremely unlikely)
- **EU dissolution** (extremely unlikely 2026-27)
- **Asteroid impact** (unlikely)

Ne trošimo cycles na njih.

---

## REFERENCES

- AZOP: [azop.hr](https://azop.hr)
- HOK: [hok.hr](https://www.hok.hr)
- KZ čl. 311 (nadripisarstvo): NN 125/11, ...
- AI Act 2026: Uredba (EU) 2024/1689
- GDPR čl. 35 (DPIA): Uredba (EU) 2016/679
