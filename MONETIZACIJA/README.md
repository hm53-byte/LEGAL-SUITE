# MONETIZACIJA — Master plan LegalTech Suite Pro

> **Datum nastanka**: 2026-04-27
> **Status**: AKTIVNI PLAN (faza 0 — priprema)
> **Vlasnik odluka**: Hrvoje Matej Lešić
> **Glavni dokument**: ovaj README orkestrira sve sub-dokumente

---

## TL;DR

| Faza | Trajanje | Glavna isporuka | Trošak | Risk |
|---|---|---|---|---|
| **0 — Priprema** | 2-4 tj | C1+C2 fix, scraper rezanje, AZOP DPIA draft | 0 € | Nizak |
| **1 — Pravna struktura** | 1-2 tj | j.d.o.o. otvoren, IBAN, knjigovodstvo | ~150-300 € | Srednji |
| **2 — MVP s plaćanjem** | 3-5 tj | Polar.sh integracija, prvih 10 platežnih usera | ~50 €/mj run | Srednji |
| **3 — Skaliranje** | 3-6 mj | 50-100 platežnih usera, vlastiti VPS | ~30 €/mj | Visok |
| **4 — Profesionalni segment** | 6-12 mj | NPL/banke pilot, premium tier | varijabilno | Visok |

**Glavna teza:** započni kao paušalni obrt **NIJE VALJANO** za SaaS prema HR poreznom režimu (slobodno zanimanje + B2B usluge — vidi `02_PRAVNA_STRUKTURA.md`); ide se direktno na **j.d.o.o.** s 1.250 EUR temeljnog kapitala (najbrži, najjeftiniji, ograničena odgovornost).

**Prvi konkretan korak (sljedeća sesija):** ZAUSTAVI port e-Oglasna scrapera (C2 iz handoff-a). Razlog: politika privatnosti e-Oglasne **eksplicit navodi tehničke zaštite protiv scraping-a** ("Ugrađene su zaštite od prikupljanja podataka Internet pretraživača"). Idi na alternativu — Sudski registar API (CC-BY, otvoreni podaci, već imaš `api_sudreg.py`).

---

## Sadržaj plana

| # | Dokument | Sažetak |
|---|---|---|
| 01 | [Pravna analiza scrapera](01_PRAVNA_ANALIZA_SCRAPERA.md) | robots.txt + politika privatnosti e-Oglasne; AZOP DPIA obveza; Sudski registar API kao alternativa |
| 02 | [Pravna struktura](02_PRAVNA_STRUKTURA.md) | Paušalni obrt vs j.d.o.o. vs d.o.o.; zašto je SaaS isključen iz paušala; porez na dobit 2026; Fiskalizacija 2.0 |
| 03 | [Tehnički stack](03_TEHNICKI_STACK.md) | Streamlit Cloud → Hetzner VPS migracijski plan; Polar.sh KYC za HR d.o.o.; data residency |
| 04 | [Cjenovni model](04_CJENOVNI_MODEL.md) | Three-tier ladder; freemium guarda; pricing testovi; B2B premium |
| 05 | [GTM strategija](05_GTM_STRATEGIJA.md) | Segmenti (mali odvjetnici → NPL → banke); content+SEO; ne ulaziš u Mailchimp drip |
| 06 | [Milestones](06_MILESTONES.md) | Faze 0-4 s KPI-jevima i decision gate-ima |
| 07 | [Budući GOAT ciklusi](07_BUDUCI_GOAT_CIKLUSI.md) | Lista odluka koje treba formalno proći GOAT pipeline |
| 08 | [Rizici](08_RIZICI_I_MITIGACIJE.md) | AZOP, AI Act 2026, nadripisarstvo, Polar.sh API churn |
| **★** | [**FINISH**](FINISH.md) | **Pre-launch checklist + studentska prava + doktorat scenariji — glavni operativni dokument** |

---

## Odluka: GOAT ili BRZ_MOZAK ciklus za ovaj plan?

**Odluka: NI JEDAN.** Razlozi:

1. **GOAT format** (3 koraka, decision matrix) je za **discrete decisions** s 3-4 jasno definirane opcije (kao Paddle vs LMSQZY vs Polar u Ciklusu 1). Master plan **nije discrete decision** — to je sintezni dokument koji konsolidira odluke + definira faze.

2. **BRZ_MOZAK format** (5 koraka, no-AI, code patch output) je za **arhitekturni patch koda** (kao "Hermesov sync outbox" K2). Master plan **nije code patch**.

3. **Sub-odluke** unutar plana **trebaju vlastite GOAT cikluse** — vidi `07_BUDUCI_GOAT_CIKLUSI.md`. Te se zakazuju kasnije, kad konkretna odluka stigne na red, **ne preventivno**.

**Što je ovaj dokument:** sintezni roadmap koji:
- Konsolidira nalaze iz današnje WebSearch/WebFetch sesije
- Definira faze i decision gate-ove
- Identificira buduće GOAT cikluse
- Pruža konkretne next-steps za sljedeću sesiju

**Trošak izrade**: ~25k tokena (već potrošeno) bez ciklusa, vs ~75-90k da je išlo kroz GOAT (Ciklus 1 = 75k).

---

## Sljedeća tri koraka (sljedeća sesija)

1. **PROČITAJ ovaj README + dokumente 01, 02 redom** (~10 min)
2. **ODLUKA: zatvori e-Oglasna scraper port** (C2 iz handoff-a) — ide na alternativu prema `01_PRAVNA_ANALIZA_SCRAPERA.md`
3. **POKRENI Fazu 1**: pripremi listu dokumenata za START platformu (j.d.o.o.) — vidi `06_MILESTONES.md` Faza 1

---

## Veza s postojećim dokumentima

- `GOAT/PREPORUKA_MOR.md` — Polar.sh izabran (Ciklus 1) — referencirano u `03_TEHNICKI_STACK.md`
- `HANDOFF_C_FIXES_2026-04-27.md` — C1 OK, **C2 STOP** (vidi `01_PRAVNA_ANALIZA_SCRAPERA.md`)
- `CLAUDE.md` — projektni kontekst, ostaje vrijedi
- `tasks.md` — operativni todo, dopunit će se nakon Faze 1

---

## Audit log promjena ovog plana

| Datum | Promjena | Razlog |
|---|---|---|
| 2026-04-27 | Inicijalna izrada | Korisnikov zahtjev za monetizacijski masterplan |
