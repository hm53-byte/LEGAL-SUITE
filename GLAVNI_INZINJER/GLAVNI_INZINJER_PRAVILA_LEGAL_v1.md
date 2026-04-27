# GLAVNI_INZINJER_PRAVILA_LEGAL_v1.md — adaptirana pravila za LegalTech domenu

**Verzija**: v1.0 LEGAL (2026-04-27)
**Domena**: LegalTechSuite Pro (deterministic document generator)
**Naslijeđuje**: Pravila 1-32 iz RIJEKA_PRATILAC v1-v4 (univerzalna metodologija) + adaptirane verzije Pravila 33-38 za LegalTech-specific risk management.

---

## Što vrijedi nepromijenjeno iz RIJEKA_PRATILAC

| Pravilo | Sadržaj | Status |
|---|---|---|
| 1-12 (CLAUDE_CORE) | Uloga, metodologija, 7 testova, ERROR/FIX markeri | **VRIJEDI doslovno** |
| 14 (anti-atraktor) | Eliminira top-of-mind primitive | **VRIJEDI doslovno** |
| 14B (tehnoloska sprancara) | Penalizira no-code, vendor SaaS | **VRIJEDI doslovno** |
| 16 (PhD-ML pitanja) | 3+ od 5 dubinskih pitanja (distribution shift, calibration, causal vs correlational, identifiability, failure mode taxonomy) | **VRIJEDI doslovno** — ali fokus se mijenja: u LegalTech "calibration" znači HR PDV / pristojbe točnost; "failure mode taxonomy" znači UX FP/FN gdje je FP "wrong dokument za korisnikovu situaciju" |
| 24 (3 reference iz 3 kategorije) | Akademska + vendor + analog | **VRIJEDI doslovno** — ali kategorija "AKADEMSKA" sad zahtjeva referencu na sigurnosni/kriptografski paper (Schneier, RFC 6962, Petitcolas) ili pravni paper, ne ML paper |
| 25 (NEZAVISNI SUDAC) | Odvojen subagent koji ne zna za UBOJICA score | **VRIJEDI doslovno; obvezno za P2 hibrid** |
| 27 (LOC realnost) | Formula MVP_dani = LOC/75 + LOC*0.3/50 + 2 | **VRIJEDI doslovno** |
| 30 (anti-over-engineering) | SDC schema + integracijska kompleksnost | **VRIJEDI doslovno** |
| 32 (anti-jargon naziv) | Kratak, čovjeku razumljiv naziv | **VRIJEDI** |

## Što je adaptirano (Pravila L1-L6)

Numeracija: koristim L-prefix (LegalTech) umjesto v5 numeracije 33-38 da označim **adaptaciju, ne nasljeđivanje**.

---

## Pravilo L1 — Misija inženjera u LegalTech (Tip A/B/C, anti-AI specifično)

### Razlog

RIJEKA_PRATILAC Pravilo 33 v5 dozvoljava arhitekturne kompozicije s ML primitivima (vLLM + spec-decoding + Mamba). Za LegalTech, takve kompozicije **automatski aktiviraju AI Act Annex III pt. 8 visoko-rizičnu zonu** + nadripisarstvo (ZO čl. 72). Strukturna pozicija APLIKACIJA je *deterministic templating, no AI* — to je **konkurentska prednost**, ne ograničenje.

### Pravilo

Kandidat **MORA** biti jedan od tri tipa:

**Tip A — Deterministic substitucija**:
> "Zamijeni komponentu X u APLIKACIJA s komponentom Y iz LEGAL_ARHITEKTURA.md koja daje mjerljiv ROI Z, **bez uvođenja AI inferencije ili klasifikatora**."

**Tip B — Deterministic kompozicija**:
> "Spoji komponente X1, X2, X3 iz LEGAL_ARHITEKTURA.md (sve deterministic) na način koji daje emergentnu vrijednost ROI Z za LegalTech use case, **bez ulaska u Annex III pt. 8 zonu**."

**Tip C — Cryptographic ekstrakcija**:
> "Iz vec implementiranog koda u APLIKACIJA, izvuci komponentu X i reorganiziraj je u Y obrazac (kriptografski audit / forensic / schema versioning) koji daje sekundarni ROI Z (npr. pravna obranjivost, GDPR compliance, audit trail)."

### Što NIJE valjan kandidat (eksplicit eliminirano u Agent 1 IZVIDNIK)

- ❌ "AI klasifikator koji dokument korisnik treba" — Annex III pt. 8 high-risk
- ❌ "AI-generirane personalizirane klauzule" — Article 50 transparency obligation + nadripisarstvo
- ❌ "Predikcija ishoda postupka iz povijesnih podataka" — Annex III pt. 8
- ❌ "Smart wizard koji iz prirodnog jezika zaključuje korisnikov problem" — high-risk
- ❌ "Recommender 'korisnici poput vas su koristili...'" — Article 50 + UX manipulacija pravne odluke
- ❌ "AI summarizer sudskih odluka koje korisnik priloži" — high-risk + privacy
- ❌ Bilo koji RAG sustav koji odgovara na pravna pitanja korisnika — high-risk

### Što JEST valjan kandidat

- ✅ Per-doc forensic watermark (K3, gotovo)
- ✅ SHA256 audit trail per output (K1)
- ✅ Service Worker + IndexedDB offline-first (K2)
- ✅ Generator versioning registry (K4)
- ✅ Stripe entitlement system (K3, gotovo)
- ✅ HR PDV automatizacija kroz Stripe Tax (K3, gotovo)
- ✅ JSON Schema validacija forme prije generiranja (potencijalan novi kandidat)
- ✅ eIDAS qualified timestamp add-on (PRO upsell, novi kandidat)

### Enforcement

Agent 1 IZVIDNIK: ako enumerira "primitiv" koji je iz `OSNOVE_ARHITEKTURE.md` ML kataloga (ne LEGAL_ARHITEKTURA.md), automatski ELIMINIRANO.

Agent 2B INŽENJER: kandidat MORA imati:
- Postojeću APLIKACIJA komponentu koju mijenja (path do file-a)
- Novu komponentu iz **LEGAL_ARHITEKTURA.md §I-V** (ne OSNOVE_ARHITEKTURE.md)
- Mjerljiv ROI broj (vidi Pravilo L4)
- Eksplicitnu izjavu "Ne uvodi AI inferenciju, klasifikaciju, predikciju ili rekomendaciju"

Bez sva četiri → kandidat odmah BACKLOG, max 4/7.

---

## Pravilo L2 — Input stack za LegalTech domenu

Agent 1 IZVIDNIK i Agent 2B INŽENJER **OBVEZNO** čitaju u svaki ciklus:

1. **`LEGAL_ARHITEKTURA.md`** (ovaj direktorij) — primarni izvor primitiva (kriptografija + PWA + idempotency + schema versioning + deterministic templating)
2. **`APLIKACIJA/README.md`** sekcije: "Što sustav radi", "Stack i ovisnosti", "Monetizacija", "AI Act 2026 i nadripisarstvo"
3. **`APLIKACIJA/PROBLEM_S_APP.md`** — ažurni popis poznatih problema s prioritetima
4. **Trenutni file tree**: `find . -name "*.py" -not -path "*/.venv/*"`

Agent 2A FILOZOF **NE SMIJE** čitati niti jedno od gore navedenog (Pravilo 35 strikt kineski zid, vidi GLAVNI_INZINJER_AGENTI_LEGAL.md).

### Zabranjeno za inženjerske agente (1, 2B, 3, 5)

- `OSNOVE_ARHITEKTURE.md` iz RIJEKA_PRATILAC (kontaminacija ML primitivima)
- `arhitektura-nadopuna.md` iz RIJEKA_PRATILAC (conformal/Bayes/bitemporal — sve ML/stats)
- IDEJA_*.md iz APLIKACIJA `razvoj/` ili sličnih foldera (ako postoje pre-LegalTech ideje)
- Marketing/sales materijali ako postoje
- Job ad-ovi i karijerne note (RAZVOJ_PRIJEDLOZI.md sadrži takve sadržaje koji su slop, ne input)

---

## Pravilo L3 — Strikt kineski zid oko Agenta 2A FILOZOFA

Identičan Pravilu 35 v5. Razlog se ne mijenja u LegalTech:

Agent 2A FILOZOF mora biti pokrenut u **odvojenoj subagent instanci** s praznim contextom. Prima samo:

- INOVACIJA_pojam.md (kopirat iz RIJEKA_PRATILAC ili napisat ekvivalent)
- CLAUDE_CORE.md (75 linija, originalna jezgra)
- CLAUDE_FILTERI.md (numerology test inline)
- Lista 5 čudnih izvora — eksplicitno iz kulturoloških domena (književnost, mitologija, filozofija, antropologija, povijest knjizevnosti)

NE prima: LEGAL_ARHITEKTURA.md, APLIKACIJA README, file tree, output Agenta 1.

Output: 3-5 kristala s mehaničkim kosturom + diskriminantnim uvjetom + ERROR/FIX markerima.

Agent 2B INŽENJER prvi put vidi kristale + filtrirane primitive iz LEGAL_ARHITEKTURA + APLIKACIJA stack i pita: **"koji deterministic primitiv iz LEGAL_ARHITEKTURA nosi taj princip, i kako se može spojiti s APLIKACIJA stack-om za mjerljiv ROI BEZ uvođenja AI?"**

---

## Pravilo L4 — ROI metrike za LegalTech

Zamjena RIJEKA_PRATILAC Pravila 36 (ML-fokusiran). Svaki kandidat ima 3+ od 7 sljedećih metrika:

1. **Pravna obranjivost delta**: "Prije: korisnik može tvrditi 'nisam ja generirao' → Davatelj nema dokaz; Poslije: forensic chain serial → user_id u download_log → potvrda autentičnosti pred sudom"
2. **AI Act compliance margin**: "Prije: rub Annex III pt. 8 (npr. implicit klasifikator vodiča); Poslije: out-of-scope (objektivan katalog, no inferencija)"
3. **GDPR compliance delta**: "Prije: <X> nepotrebnih osobnih podataka u DB; Poslije: <Y>; data minimization Article 5(1)(c) ratio"
4. **DRM efektivnost**: "Prije: 0% (downloadan docx je trajna spranca); Poslije: ~85-90% (visible footer + invisible XML metadata)"
5. **MRR konverzija proxy / Per-doc trošak**: "Cost per document: <X> EUR (Stripe %); konverzija free→pro <Y%>" (samo ako kandidat utječe na monetizaciju)
6. **Latency P50/P90/P99**: docx generacija ms (deterministic = predictable; AI bi uvelo varijancu)
7. **MTTR / Idempotency garancija**: "Stripe webhook duplikati → 0 dvostruke obrade (UNIQUE constraint); reconciliation cron-a 24h SLA"

Brojevi MORAJU biti **plausibilni** (Agent 3 UBOJICA i Agent 5 SUDAC spot-checkaju), idealno s anchor referencom (npr. "Stripe webhook idempotency Best Practices 2024").

### Forenzika za ROI

Format obvezan u kandidatu:

```
ROI METRIKE (Pravilo L4):

| # | Metrika | Prije | Poslije | Anchor referenca |
|---|---------|-------|---------|------------------|
| 1 | DRM efektivnost | 0% | ~85-90% | Petitcolas IEEE 1999 forensic vs robust |
| 2 | AI Act compliance margin | rub Annex III | out-of-scope | EU Reg 2024/1689 Art 3(1) |
| 3 | GDPR data minimization | retain user_id u XML | retain hash[:8] | GDPR Art 5(1)(c) |

PRIMARNI ROI: <jedna rečenica> → <konkretan operativni utjecaj>

SEKUNDARNI ROI: <jedna rečenica>

RIZIK NA ROI: <što može poći krivo, kako se mitigira>
```

### Enforcement

UBOJICA Test 2 (Snaga) zahtjeva minimum 3 ROI metrike s brojevima. Bez 3+ → automatic FAIL Test 2.

NEZAVISNI SUDAC u R1 (ROI realnost): spot-checka 1 nasumičnu metriku. Ako napuhana > 50% → ROI_DIVERGENCE block.

---

## Pravilo L5 — Jedna ideja po ciklusu (depth > breadth)

Identičan Pravilu 37 v5. Jedan ciklus = jedna duboka ideja = 1-2 kandidata, ne 6.

Iznimka: ako Agent 1 IZVIDNIK detektira da su 2+ primitiva iz LEGAL_ARHITEKTURA **ortogonalna** (rješavaju različite probleme APLIKACIJA — npr. K1 audit trail vs K2 PWA), može predložiti dva paralelna ciklusa, ali svaki je i dalje "jedna ideja". Orkestrator (korisnik) odlučuje paralelizaciju.

---

## Pravilo L6 — Anti-AI drift + Anti-business drift (LegalTech specific)

Zamjena Pravila 38 v5 (anti-business drift) s **dvostrukom prohibicijom**.

### Razlog

LLM-ovi imaju dvije tendencije sklizanja u LegalTech kontekstu:

1. **AI drift** (specifičnije za LegalTech): "samo dodaj AI klasifikator/wizard/recommender" se predlaže u 2026 jer je AI dominantan obrazac u LLM training datasetu. To je upravo zona koju moramo izbjeći.
2. **Business drift** (slično v5 Pravilo 38): "ovo bi NPL agencije platile..." — pricing/segment fokus umjesto inženjerske strogosti.

### Pravilo

Kandidat **NE SMIJE** sadržavati:

**Anti-AI drift (LegalTech specific)**:
- AI inferenciju, klasifikator, prediktivni model, generative AI sloj
- "ML pipeline", "trening dataset", "fine-tuning", "embedding"
- "Smart" / "Intelligent" / "Cognitive" framing
- LLM API pozive (osim za ne-pravne use cases — npr. translation, ali ne za pravni sadržaj)
- Recommender / personalizaciju / "korisnici poput vas"
- Bilo što što aktivira **AI Act Article 3(1) "AI system" definiciju**

**Anti-business drift (naslijeđeno)**:
- Naziv segmenta (NPL agencije, banke, osiguravatelji, korp. compliance)
- Cijenu (EUR/mj, tier ime kao primary cilj — može biti DERIVATIVNI ROI metrika u L4)
- Sales metrike (TAM, ARR, MRR, CAC, LTV) kao primary cilj
- Frazu "tko će ovo platiti" — ROI je mjeren u kodu, ne u prodaji

### Iznimka

**LegalTechSuite Pro je izričito out-of-scope AI Act-a JER NE KORISTI AI**. Kandidat može (i mora) **referirati taj fakat** kao argument za ROI metriku #2 (AI Act compliance margin). To je ne-AI use, dakle dozvoljeno.

Primjer dozvoljen:
> "Ovaj patch eliminira implicit klasifikator iz vodiča, što vraća APLIKACIJA u out-of-scope poziciju AI Act Annex III pt. 8."

Primjer NEDOZVOLJEN:
> "Dodaj GPT-4 wrapper koji iz prirodnog jezika zaključuje koji obrazac korisnik treba."

### Enforcement

Agent 3 UBOJICA i Agent 5 NEZAVISNI SUDAC u Test 7 (Alkemija):

- Grep kandidat za **AI-drift fraze**: "klasifikator", "model", "trening", "embedding", "LLM", "GPT", "Claude", "AI sloj", "neuronska mreža", "smart", "intelligent", "personalizacija", "recommender"
- Grep za **business-drift fraze** (kao v5 Pravilo 38)
- Ako >2 hit-a u bilo kojoj kategoriji → automatic FAIL Test 7 + REFRAKTOR signal "ukloni AI/business jezik, vrati se na deterministic kriptografski audit"

### Iznimke (legitimne)

- "AI Act" — dozvoljen kao zakonska referenca (npr. ROI metrika #2)
- "AI klasifikator" — dozvoljen ako je u kontekstu **ELIMINACIJE**, ne dodavanja ("Ovaj patch UKLANJA AI klasifikator")
- "Klasificiraju" — dozvoljen kao opis problema kojeg refactor rješava ("ranija verzija je klasificirala...")
- "Model" — dozvoljen ako se odnosi na podatkovni model (DB schema), ne ML model

---

## Mapa Pravila: što vrijedi gdje

| Pravilo | RIJEKA_PRATILAC v5 | LegalTech v1 (ovaj dokument) |
|---|---|---|
| 1-12 (CLAUDE_CORE) | doslovno | doslovno |
| 13 (sub-agenti) | vrijedi | vrijedi (P2 hibrid varijanta — vidi GLAVNI_INZINJER_AGENTI_LEGAL.md) |
| 14, 14B | doslovno | doslovno |
| 15, 20 | gasi se | nije primjenjivo (LegalTech ima drugu ekonomiju) |
| 16 | doslovno | doslovno (s LegalTech adaptacijom u opisu) |
| 17 | vrijedi | vrijedi |
| 18, 19, 21 | vrijedi | vrijedi |
| 22 | vrijedi | vrijedi |
| 23 (commit-able patch) | pojačano | pojačano |
| 24 (3 reference) | vrijedi (s ML fokusom) | vrijedi (s LegalTech fokusom — kriptografija/RFC/eIDAS, ne ML) |
| 25 (NEZAVISNI SUDAC) | vrijedi | vrijedi (obvezan u P2 hibrid) |
| 26 | zamijenjeno Pravilom 36 | zamijenjeno Pravilom **L4** |
| 27 (LOC) | doslovno | doslovno |
| 28 (anti-monoculture) | modificirano (po arhitekturnom obrascu) | modificirano (po obrascu — ne 5/6 kandidata svi mijenjaju monetizaciju) |
| 29 (reference fact-check) | vrijedi | vrijedi |
| 30, 31, 32 | doslovno | doslovno |
| 33 (misija inženjera) | RIJEKA_PRATILAC ML kompozicije | zamijenjeno Pravilom **L1** (LegalTech anti-AI Tip A/B/C) |
| 34 (input stack) | OSNOVE_ARHITEKTURE.md + README.md RIJEKA | zamijenjeno Pravilom **L2** (LEGAL_ARHITEKTURA.md + README.md APLIKACIJA) |
| 35 (kineski zid 2A) | doslovno | zamijenjeno Pravilom **L3** (identičan, ali eksplicitno za LegalTech) |
| 36 (ROI metrika) | latency/VRAM/throughput | zamijenjeno Pravilom **L4** (DRM/AI Act margin/GDPR/MRR) |
| 37 (jedna ideja) | doslovno | zamijenjeno Pravilom **L5** (identičan) |
| 38 (anti-business drift) | grep za pricing/segment | zamijenjeno Pravilom **L6** (Anti-AI + Anti-business) |

---

## Geneza

Nastalo: 2026-04-27 popodne.
Razlog: korisnikova primjedba da BRZ_MOZAK pravila iz RIJEKA_PRATILAC referenciraju ML primitive koji bi za APLIKACIJA aktivirali AI Act high-risk + nadripisarstvo. Nužna je adaptacija + zaštitni filter (Pravilo L6 anti-AI drift).
Cilj: pokrenuti P2 hibridni pipeline za K1 LegalTech kandidat (Forensic audit trail per-output) bez rizika sklizanja u zabranjene zone.
