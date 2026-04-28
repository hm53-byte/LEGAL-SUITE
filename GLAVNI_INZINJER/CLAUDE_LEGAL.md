# CLAUDE_LEGAL.md — GLAVNI INŽENJER mod (LegalTech adaptacija)

**Verzija**: v1.0 LEGAL (2026-04-27)
**Domena**: LegalTechSuite Pro (deterministic document generator)
**Modus**: P2 hibrid (default; P1 i P3 dostupni za posebne slučajeve)

---

## Misija

GLAVNI INŽENJER LEGAL mod proizvodi **arhitekturne patcheve** koji:

1. Preuzimaju **deterministic primitive iz LEGAL_ARHITEKTURA.md** (kriptografski audit, PWA/offline, idempotentni webhooci, schema versioning, deterministic templating)
2. Spajaju ih s **postojećim APLIKACIJA stack-om** (Streamlit + python-docx + Supabase + Stripe + Cloudflare Workers)
3. Daju **mjerljiv ROI** (Pravilo L4 — DRM efektivnost, AI Act compliance margin, GDPR data minimization, MRR konverzija proxy, latency, MTTR)
4. **Ne uvode AI inferenciju, klasifikator, prediktivni model, recommender** — to bi aktiviralo AI Act high-risk + nadripisarstvo (Pravilo L6)

NIJE valjan kandidat: novi AI sloj / novi ML pipeline / "smart" wizard / personalizacija / recommender.

---

## Razlika od RIJEKA_PRATILAC GLAVNI INŽENJER v5

| Aspekt | RIJEKA_PRATILAC (v5) | LegalTech (v1) |
|---|---|---|
| Domena | ML inference engine + temporalni sonar | Deterministic legal document generator |
| Primarni input | OSNOVE_ARHITEKTURE.md (RNN/CNN/Transformer/Mamba/vLLM/spec-decoding) | **LEGAL_ARHITEKTURA.md** (SHA256/Merkle/PWA/idempotency/registry/templating) |
| Pipeline default | P1 pun (5 subagenata) | **P2 hibrid** (Filozof + Sudac subagenti; ostali inline) |
| Tip kandidata | A/B/C arhitekturna integracija (može uključivati AI) | A/B/C arhitekturna integracija (**bez AI** — Pravilo L6) |
| Anti-business filter | Pravilo 38 (segment/pricing/TAM) | **Pravilo L6** (anti-AI drift + anti-business drift) |
| Tržišni filter | Pravilo 15 (gasi se u v5) | Ne primjenjuje se (LegalTech ima drugu ekonomiju, B2C dominanto) |
| ROI metrike | Latency / VRAM / throughput / MTTR | **DRM / AI Act margin / GDPR / MRR / latency / MTTR** |
| Filozofski izvor (Agent 2A) | Pojam INOVACIJE + 5 čudnih kulturoloških izvora | Identičan (kineski zid je identičan u oba moda) |

Ovaj mod stoga **NIJE direktna primjena v5 pravila**. To je adaptacija koja čuva **out-of-scope** poziciju AI Acta.

---

## Moduli (file index)

| File | Linije (~) | Sadržaj | Kad se čita |
|---|---|---|---|
| `CLAUDE_LEGAL.md` | ~150 | Ovaj dokument; entry point | Orkestrator, na početku svakog ciklusa |
| `LEGAL_ARHITEKTURA.md` | ~330 | Katalog deterministic + cryptographic primitiva (§I-V) | Agent 1 IZVIDNIK i Agent 2B INŽENJER (NE Agent 2A FILOZOF) |
| `GLAVNI_INZINJER_PRAVILA_LEGAL_v1.md` | ~280 | Pravila L1-L6 + mapa naslijeđenih 1-32 | Svi inženjerski agenti (1, 2B, 3, 5) |
| `GLAVNI_INZINJER_AGENTI_LEGAL.md` | ~300 | P2 hibrid orkestrator protokol + sudac protokol | Orkestrator |
| `IDEJE/` | varies | Promote-ani kandidati + CIKLUS log + BACKLOG | Akumulira se kroz cikluse |

Reference iz RIJEKA_PRATILAC (univerzalni, čitaju se direktno odande):

- `CLAUDE_CORE.md` (~75 linija) — uloga, metodologija, Pravila 1-12, 7 testova
- `CLAUDE_FILTERI.md` (~80 linija) — Pravilo 14 anti-atraktor + numerology test
- `CLAUDE_FILTERI_v2_ADDENDUM.md` (~155 linija) — Pravila 14B (sprancara), 15A (UBOJICA kalibracija), 16A (nadripisarstvo)
- `INOVACIJA_pojam.md` (~43 linije) — pojam inovacije za Agent 2A FILOZOF

Putevi:
```
C:\Users\{{WIN_USER}}\Desktop\RIJEKA_PRATILAC\GLAVNI INZINJER\BRZ_MOZAK - nacin drukcijeg razmisljanja - drugi skut sagledavanja problema\CLAUDE_CORE.md
C:\Users\{{WIN_USER}}\Desktop\RIJEKA_PRATILAC\GLAVNI INZINJER\BRZ_MOZAK - nacin drukcijeg razmisljanja - drugi skut sagledavanja problema\CLAUDE_FILTERI.md
... itd
```

Orkestrator ih čita iz tih puteva i prosljeđuje u Agent 2A FILOZOF subagent prompt (kineski zid garantira da Filozof NE čita LegalTech specifične dokumente).

---

## P2 hibrid — sažeti tok (detalji u GLAVNI_INZINJER_AGENTI_LEGAL.md)

```
[Korisnik traži novi ciklus K<N>]
              │
              ▼
[Orkestrator: priprema CIKLUS_<N>_<date>.md, SEED, izazov]
              │
              ▼
[Agent 1 IZVIDNIK — inline] enumerira 15+ primitiva iz LEGAL_ARHITEKTURA,
                            anti-atraktor + L6 anti-AI filter, rangira 3
              │
              ▼
[Agent 2A FILOZOF — ODVOJEN SUBAGENT, prazan context]
                            kineski zid (Pravilo L3); 5 kulturoloških izvora;
                            output: 3-5 kristala
              │
              ▼
[Agent 2B INŽENJER — inline] spaja kristale + primitive + APLIKACIJA stack;
                              bira 1-2 kandidata u L4 formatu
              │
              ▼
[Agent 3 UBOJICA — inline] 7-test STRICT (anti-AI grep u T7); prijedlog score
              │
              ▼
[Agent 5 NEZAVISNI SUDAC — ODVOJEN SUBAGENT, prazan context]
                              7-test neovisno + 5 realnost-provjera; final score
              │
              ▼
[Orkestrator: refractor ili promote]
```

P2 trošak: ~30k tokena (vs P1 ~100k) — 70% ušteda uz zadržan rigor (kineski zid + nezavisni sudac).

---

## Kad koristit P1, P2, P3

| Situacija | Modus |
|---|---|
| Standardni novi kandidat (K1, K2, K4) | **P2** (default) |
| Posebno složen / sigurnosni-kritičan kandidat (npr. eIDAS qualified timestamp integration) | **P1 pun** |
| Sub-zadatak istog već-odobrenog kandidata (npr. K3 A/B/D dovršetak nakon glavnog kandidata) | **P3 inline** |
| Sysadmin / DevOps / UI bug fix | Ne koristi se BRZ_MOZAK; direktna implementacija |

---

## Što GLAVNI INŽENJER LEGAL NE radi

- **Ne odlučuje** koji kandidat ide u implementaciju — to je orkestrator (korisnik) odluka nakon SUDAC review-a.
- **Ne implementira automatski** — promote-an kandidat ide u IDEJE folder kao plan; korisnik bira kad i kojim redoslijedom implementira.
- **Ne radi pravne savjete** — sve mora ostati izvan AI Act high-risk i nadripisarstva (Pravilo L6 enforcement).
- **Ne radi pricing decisions** — ROI metrika #5 (MRR proxy) je derivativni broj, ne primary cilj. Pricing odluke su business strategy, ne inženjering.

---

## Kako pokrenuti prvi ciklus (K1 — Forensic audit trail per-output)

1. Korisnik (orkestrator): "Pokreni K1 ciklus, P2 modus, SEED=<broj>"
2. Orkestrator priprema CIKLUS_K1_2026-04-XX.md s:
   - Izazov: "Kako garantirati bit-by-bit reproducibility svakog generiranog docx-a iz {input fields, generator verzije, timestamp} 6+ mjeseci kasnije? Koja je arhitekturna kompozicija primitiva iz LEGAL_ARHITEKTURA §I (kriptografija) i §IV (versioning) koja to omogućava?"
3. Pokreće Agent 1 IZVIDNIK inline
4. Pokreće Agent 2A FILOZOF subagent (Pravilo L3)
5. Sintetizira u Agent 2B
6. UBOJICA inline 7-test
7. Pokreće Agent 5 SUDAC subagent (Pravilo 25)
8. Prima oba score-a, refrakcija ako delta > 1
9. Promote ili BACKLOG

---

## Geneza

Nastalo: 2026-04-27 popodne.
Razlog: korisnik je odobrio adaptaciju RIJEKA_PRATILAC BRZ_MOZAK metodologije na LegalTech domenu, s dvostrukim ciljem: (a) eliminirati ML primitive iz input stack-a (LEGAL_ARHITEKTURA.md), (b) pojačati anti-AI filter u Pravilu L6.
Cilj: omogućiti pun P2 hibridni pipeline za APLIKACIJA cikluse od K1 nadalje, bez rizika sklizanja u Annex III pt. 8 / nadripisarstvo zone.
