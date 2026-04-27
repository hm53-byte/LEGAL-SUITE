# 06 — Milestones, faze, decision gates

> **Datum**: 2026-04-27
> **Horizont**: 12 mjeseci aktivnih + 24 mj outlook
> **Pristup**: pojedinačno completion-driven, ne datum-driven

---

## ROADMAP — kompletni overview

```
2026-04-27 ──────────────────────────────────────────────────────────► 2027-04
            │       │       │       │       │       │       │       │
            ▼       ▼       ▼       ▼       ▼       ▼       ▼       ▼
        FAZA 0  FAZA 1  ─FAZA 2────  ──FAZA 3──  ──────FAZA 4──────
        2-4 tj  1-2 tj  3-5 tj      3-6 mj      6-12 mj
        Pripr.  d.o.o.  MVP plać.   Skaliranje  B2B pilot
```

---

## FAZA 0 — Priprema (sadašnji trenutak — 2-4 tjedna)

### Goal
Razriješiti tehnički dug, pravne rizike, validirati build-ready proizvod prije ulaganja u pravnu strukturu.

### Tasks
| # | Task | Estimacija | Akcija |
|---|---|---|---|
| 0.1 | Ukloni `api_epredmet.py` (C1 iz handoff-a) | 30 min | Već u planu |
| 0.2 | **OTKAZI** C2 (port e-Oglasna) — refaktor u outbound link placeholder | 1-2h | Per `01_PRAVNA_ANALIZA_SCRAPERA.md` |
| 0.3 | Registriraj se na sudreg-data.gov.hr i validiraj `api_sudreg.py` | 1h | OAuth credentials u Streamlit secrets |
| 0.4 | Email `sudski.registar@pravosudje.hr` za pisanu komercijalnu licencu | 15 min | Pošalji kratki upit |
| 0.5 | Provjeri Supabase regiju (mora biti EU-Frankfurt ili EU-Ireland) | 5 min | Ako nije, planiraj migraciju |
| 0.6 | DPIA template skidaj s azop.hr i počni popunjavati | 2-3h | Spremi u `MONETIZACIJA/dpia/` |
| 0.7 | Skupi cijene HR domena (.hr CARNet, .com.hr, alternativne brand options) | 1h | Provjeri dostupnost CARNet WHOIS |
| 0.8 | Skupi 2-3 ponude za računovodstveni servis u Zagrebu | 2h | Aning, Brojevi, Aestus |

### Decision gate: prelazak Faza 0 → Faza 1
**Ispunjeno kad**:
- e-Oglasna scraper više nije u backlog-u
- `api_sudreg.py` radi s pisanim potvrdom za komercijalnu uporabu
- DPIA template populated do 50%+ (osnovne kategorije)
- Sve fiktivne API klijente (`api_epredmet.py`, `api_eoglasna.py`) uklonjeni
- 2/2 računovodstveni servis dao ponudu

### Cost
**0 € izvan radnog vremena** (sve manual + research)

### Risk
- **Low** — nema komercijalnog izlaganja
- **Mitigation**: ne počinje plaćeni model dok Faza 1 nije gotova

---

## FAZA 1 — Pravna struktura (1-2 tjedna paralelno s Faza 0)

### Goal
Otvoriti j.d.o.o., HR IBAN, postaviti operativnu poslovnu infrastrukturu.

### Tasks
| # | Task | Estimacija | Akcija |
|---|---|---|---|
| 1.1 | Provjeri eOsobnu iskaznicu (s čitačem) ili mToken | 1h | Ako nemaš, dogovori s Erste/PBZ certA |
| 1.2 | Izaberi naziv tvrtke + provjeri dostupnost u sudskom registru | 30 min | sudreg.pravosudje.hr search |
| 1.3 | Otvori START platforma sesiju, popuni j.d.o.o. obrazac | 1-2h | start.gov.hr |
| 1.4 | Plati pristojbu, dogovori javnobilježnički termin (ako START traži) | 30 min | ~26 € online + 120-200 € JB |
| 1.5 | Otvori HR IBAN business (Erste Mojo ili PBZ Online) | 2-3h (hod) | Uz potvrdu osnivanja |
| 1.6 | Uplati temeljni kapital 1.250 € na novi IBAN | 1 transfer | Iz tvog osobnog računa |
| 1.7 | Predaj sudu potvrdu uplate (preko START-a) | automatski | 2-3 radna dana |
| 1.8 | Aktiviraj OIB pravne osobe u Poreznoj | 30 min | eOsobna ili odlazak u poreznu |
| 1.9 | Aktiviraj HZZO + HZMO (mirovinsko + zdravstveno) | 30 min | mirovinsko.hr |
| 1.10 | Potpiši ugovor s računovodstvenim servisom | 1h | Iz najboljih 2 ponuda Faza 0 |
| 1.11 | Kupi domenu (npr. `legalsuite.hr` preko CARNet) | 30 min | ~25 €/god |
| 1.12 | Setup Zoho Mail (free) s d.o.o. domenom | 1h | DNS records |

### Decision gate: prelazak Faza 1 → Faza 2
**Ispunjeno kad**:
- Izvod iz sudskog registra dostupan
- HR IBAN aktivan, prima uplate
- OIB pravne osobe aktivan
- Računovodstveni servis preuzeo brigu
- Domena radi, business email aktivan

### Cost
- Pristojbe: ~26 € (online) + ~120-200 € (JB) = ~150-250 €
- Temeljni kapital: 1.250 € (vraća se kao imovina d.o.o.)
- Domena: ~25 €/god
- Knjigovodstvo: ~150-200 €/mj × 1 mj = ~200 € (prvi mjesec često besplatan)
- Email: 0 € (Zoho free 5 user)
- **Ukupno first-time**: ~400 € + 1.250 € TK
- **Mjesečno fix**: ~200-250 €/mj (knjigovodstvo + business banka)

### Risk
- **Mid** — administrativne komplikacije s START platformom
- **Mitigation**: ako online ne radi, idi klasični (javnobilježnički + sud osobno) → +200 € trošak ali sigurno radi

---

## FAZA 2 — MVP s plaćanjem (3-5 tjedana)

### Goal
Prvi platežni korisnici. Polar.sh integracija live. Validacija product-market fita.

### Tasks
| # | Task | Estimacija | Akcija |
|---|---|---|---|
| 2.1 | Polar.sh sandbox account + KYC priprema | 2-3 dana | Per `03_TEHNICKI_STACK.md` |
| 2.2 | Stripe → Polar migracija (per `GOAT/PREPORUKA_MOR.md`) | **5-7 dana** | ~345 LOC izmjene |
| 2.3 | DPA potpisati: Streamlit, Polar, Supabase, Hetzner | 1-2 dana | Email round trip |
| 2.4 | DPIA finaliziraj + spremi u `MONETIZACIJA/dpia/` | 1 dan | Internal record |
| 2.5 | Watermark logika za FREE tier (already existing watermark.py) | 4h | conditional aktivacija |
| 2.6 | Pricing page implementacija (3 tier-a) | 1 dan | per `04_CJENOVNI_MODEL.md` |
| 2.7 | Cancellation flow self-service | 4h | settings.py UI |
| 2.8 | Live Polar testing (sandbox) — full flow + edge cases | 1-2 dana | testovi |
| 2.9 | Polar live mode aktivacija (KYC submitted, account approved) | 3-7 dana | čeka Polar review |
| 2.10 | Pricing page launch + email blast (~50 friends&family beta) | 1 dan | F&F + LinkedIn announce |
| 2.11 | Prvih 5-10 platežnih usera dovedi (manual outreach) | 1-2 tj | Friends, kolege, LinkedIn |

### Decision gate: prelazak Faza 2 → Faza 3
**Ispunjeno kad**:
- 5+ platežnih PRO usera
- Polar live, refundovi rade, payouts stižu na HR IBAN
- DPA-ovi potpisani
- Prva fakturacija od strane računovodstvenog servisa uspješno (mjesečna)
- < 5% churn u prvih 30 dana

### Cost
- Polar fees: ~6.5% × prihod = ~5-15 €/mj prvi mjesec
- Streamlit Cloud: 0 €
- Supabase Pro upgrade (kad audit_chain prijeđe 500 zapisa): 25 $/mj
- Total mj 1-2: ~25-40 €/mj na top of Faza 1 fixed

### Risk
- **Mid-High** — Polar.sh KYC može odbiti ili tražiti dodatne dokumente
- **Mitigation**: backup plan = Paddle migracija (per GOAT C1 fallback)

---

## FAZA 3 — Skaliranje (3-6 mjeseci)

### Goal
50-200 platežnih PRO usera, prva STUDIO konverzija, paid acquisition validacija, infrastruktura migracija na Hetzner.

### Tasks
| # | Task | Estimacija | Akcija |
|---|---|---|---|
| 3.1 | Migrate Streamlit Cloud → Hetzner CPX22 + Coolify | 1-2 dana | per `03_TEHNICKI_STACK.md` |
| 3.2 | Cloudflare proxy ispred (DDoS + WAF + analytics) | 4h | DNS + page rules |
| 3.3 | Sentry error tracking (free tier) | 2h | python-sdk integration |
| 3.4 | Better Stack uptime monitoring (free) | 1h | https checks every 1 min |
| 3.5 | A/B test framework (manual ili GrowthBook free) | 1-2 dana | per `04_CJENOVNI_MODEL.md` |
| 3.6 | A/B test pricing 9€ vs 12€ | 4-6 tj data collection | run continuous |
| 3.7 | Multi-user / team management u app-u | 1-2 tj | STUDIO tier |
| 3.8 | Email drip — onboarding sequence (3 emaila) | 3 dana | Postmark/Mailgun integration |
| 3.9 | Blog setup + 5-10 SEO članaka | 2-3 tj continuous | per `05_GTM_STRATEGIJA.md` |
| 3.10 | Google Ads test budžet 100 €/mj | continuous | optimize CPC |
| 3.11 | Helena eRačun integracija (PDV obveza ulazi) | 3-5 dana | API integration |
| 3.12 | NN auto-update notification (cron na Hetzneru) | 1 tj | per Faza 3 retention plan |

### Decision gate: prelazak Faza 3 → Faza 4
**Ispunjeno kad**:
- 50+ platežnih PRO + 5+ STUDIO usera
- MRR ≥ 500 €/mj
- LTV:CAC ≥ 3x (validna paid acquisition)
- Infrastruktura na Hetzneru, Streamlit Cloud kao staging only
- Prvi cold lead iz NPL/banke segmenta (manual outreach validacija)

### Cost
- Hetzner CPX22: 8 €/mj
- Coolify: 0 € (self-hosted)
- Cloudflare: 0 € (free tier)
- Sentry: 0 € (free)
- Better Stack: 0 € (free)
- Helena eRačun: ~5-15 €/mj
- Postmark/Mailgun: ~10 €/mj (low volume)
- Google Ads: 100 €/mj test
- **Total mj fix**: ~130-150 €/mj na top of Faza 1 fixed (~330-400 €/mj total)

### Risk
- **High** — paid acquisition može pokazati LTV:CAC < 1 → **walking dead** model
- **Mitigation**: kill switch na Google Ads ako CAC > 50 € po 3 mj continuous

---

## FAZA 4 — B2B pilot (6-12 mjeseci)

### Goal
Prvi B2B klijent (NPL agencija). Custom plan, dedicated support, validacija da B2B segment zarađuje.

### Tasks
| # | Task | Estimacija | Akcija |
|---|---|---|---|
| 4.1 | Lista 30-50 NPL agencija (LinkedIn Sales Navigator $80) | 1 tj | Outreach prep |
| 4.2 | Cold outreach (LinkedIn + email) | continuous | 5-10 demo calls/tj cilj |
| 4.3 | Demo materials: one-pager + 5-min screencast | 1 tj | per `05_GTM_STRATEGIJA.md` |
| 4.4 | Master Service Agreement template (s odvjetnikom) | 1 tj + 500-1000 € | reusable |
| 4.5 | Custom B2B entitlement system u app-u (manual aktivacija) | 1 tj | hard-coded plans |
| 4.6 | Hetzner CPX32 upgrade ako traffic raste | 1 dan | scale up |
| 4.7 | WORM audit storage (Hetzner Storage Box) | 2-3 dana | tertiary archive |
| 4.8 | SOC 2 Type I priprema (ako enterprise klijent traži) | 6-12 mj proces, ~10-20k € | optional |
| 4.9 | Sponzorstvo HRBARLEX-a (Faza 4 marketing investment) | 3-5k € | brand visibility |
| 4.10 | First customer reference / case study | 2-3 dana | uz pristanak klijenta |

### Decision gate: što sljedeće (12-24 mj outlook)
**Ako uspijeva**:
- 5-10 B2B klijenata × 300-1000 €/mj = 18-120k €/god ARR samo iz B2B
- + 200-500 PRO/STUDIO × 9-29 €/mj = 22-175k €/god ARR B2C
- **Combined**: 40-300k €/god ARR
- **Action**: razmotri d.o.o. konverziju (j.d.o.o. → d.o.o.) ako TK > 2.500 €
- **Action**: razmisli o angel/seed fundingu (ali tek ako trebaš scale ekipi)

**Ako stagnira**:
- < 3 B2B klijenata u 12 mj → re-evaluacija segmentacije
- < 100 PRO usera → re-evaluacija pricing-a (možda predugo si)
- **Action**: razmotri pivot — možda bolje sustainable solo dev (50-100k €/god je odlična plaća)

### Cost
- Hetzner CPX32 + LB: ~20 €/mj
- WORM Storage Box: ~10 €/mj
- LinkedIn Sales Navigator: $80 × 3 mj = $240 (otkaz nakon list build-a)
- MSA odvjetnik: 500-1000 € one-time
- Conference sponzorstvo: 3-5k € one-time
- SOC 2 Type I (optional): 10-20k €
- **Total Faza 4 OPEX**: ~50-70 €/mj fix + 5-25k € one-time investments
- **Total Faza 4 revenue target**: 30-60k €/god ARR (cilj: pokriti d.o.o. break-even +30%)

### Risk
- **High** — B2B sales cycles su 3-9 mj, može dugo trajati bez signed deal-a
- **Mitigation**: paralelna B2C kampanja se vrti i nosi MRR dok B2B cooks

---

## CROSS-FAZNA pravila

### Atomic commits (per BRZ_MOZAK + CIKLUS isporuke)
Svaki technical task = atomic git commit s jasnom porukom u standardu projekta.

### Pravna konsultacija
**Svaka faza** ima budget za **1-2h pravne konsultacije** (~150-300 €) za:
- Faza 0: nadripisarstvo + AZOP DPIA review
- Faza 1: ugovor o osnivanju d.o.o. (preliminarno čitanje)
- Faza 2: T&C + Privacy Policy review
- Faza 3: Master Service Agreement (B2B)
- Faza 4: SOC 2 / ISO 27001 ako relevantno

### Tehnička konsultacija (DevOps)
**Faza 3 → 4**: razmotri 1 vanjski DevOps konzultant na pola dana (~200-400 €) za Hetzner setup review + security audit.

---

## Sažeta tablica milestones (jednim pogledom)

| Faza | Trajanje | Goal | $ Cost | $ Revenue cilj | Decision gate |
|---|---|---|---|---|---|
| 0 | 2-4 tj | Cleanup + research | ~0 € | 0 € | Sve fiktivne API uklonjeni, DPIA pripremljen |
| 1 | 1-2 tj | j.d.o.o. otvoren | ~400 € + 1.250 € TK | 0 € | Pravna osoba operativna |
| 2 | 3-5 tj | MVP s plaćanjem | ~330-400 €/mj | 50-100 €/mj | 5+ platežnih, Polar live |
| 3 | 3-6 mj | Scaling + Hetzner | ~330-400 €/mj | 500-1.500 €/mj | 50+ platežnih, MRR rast |
| 4 | 6-12 mj | B2B pilot | ~400-500 €/mj | 2-10k €/mj | 1-3 B2B klijenta |

**Cumulative timeline**: ~8-15 mjeseci do operacijskog "ozbiljnog" SaaS biznisa.
