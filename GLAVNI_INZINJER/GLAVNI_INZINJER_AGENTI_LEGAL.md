# GLAVNI_INZINJER_AGENTI_LEGAL.md — Orkestrator protokol za LegalTech P2 hibrid

**Verzija**: v1.0 LEGAL (2026-04-27)
**Domena**: LegalTechSuite Pro
**Modus**: P2 hibrid (sub-agentni Filozof 2A + Sudac 5; inline Agenti 1, 2B, 3) — dogovoreno s korisnikom 2026-04-27
**Naslijeđuje**: GLAVNI_INZINJER_AGENTI.md iz RIJEKA_PRATILAC (cijeli protokol pun pipeline P1)

---

## Tri opcije pokretanja (bira korisnik per ciklus)

| Opcija | Subagenti | Tokeni | Što dobivamo |
|---|---|---|---|
| **P1 (pun)** | 1, 2A, 2B, 3, 5 — svi odvojeni | ~100k po ciklusu | Maksimalan rigor, strikt kineski zid, full nezavisnost |
| **P2 (hibrid)** | **2A i 5 odvojeni**, **1 + 2B + 3 inline u glavnoj sesiji** | ~30k po ciklusu | Strikt kineski zid (Filozof) + nezavisni SUDAC; 70% ušteda |
| **P3 (inline)** | nijedan subagent | ~5k po ciklusu | Najbrži; sycophancy rizik (transparentno priznato) |

**Default za LegalTech v1**: **P2** (dogovoreno).

P1 se čuva za posebno kompleksne kandidate (npr. ako se uvodi neka kriptografska sigurnosna komponenta gdje je nezavisni 2A FILOZOF-ov perspektiv najvažniji).

P3 se ne koristi za nove kandidate; samo za sub-zadatke (npr. K3 A/B/D dovršetak istog kandidata).

---

## P2 hibrid — detaljan protokol

### Korak 0 — Orkestrator (glavna sesija)

Orkestrator (Claude u glavnoj sesiji s korisnikom) priprema:

- Naziv ciklusa: `CIKLUS_<int>_<YYYY-MM-DD>` (npr. `CIKLUS_K1_2026-04-28`)
- SEED (random int za reproducibility)
- Glavni izazov u 1-2 rečenice: što se nastoji riješiti
- Output direktorij: `GLAVNI_INZINJER/IDEJE/CIKLUS_<int>_<date>.md`

### Korak 1 — Agent 1 IZVIDNIK (inline, glavna sesija)

Inline u glavnoj sesiji čita LEGAL_ARHITEKTURA.md (puni) + APLIKACIJA/README.md sekcije + PROBLEM_S_APP.md + file tree i:

- Enumerira 15+ primitiva iz LEGAL_ARHITEKTURA (§I-V) primjenjivih na trenutni izazov
- Anti-atraktor (Pravilo 14) eliminira top 30% očitih
- Pravilo L6 anti-AI: eliminira sve s AI/ML/recommender konotacijama
- Pravilo 14B tehnoloska sprancara: eliminira no-code/vendor SaaS
- Rangira preostale 3-5 po ROI potencijalu (Pravilo L4)

Output: lista 1-3 najjača primitiva + APLIKACIJA file/modul mapiranje. Pisano u glavnoj sesiji, vidljivo korisniku.

### Korak 2A — Agent 2A FILOZOF (ODVOJEN SUBAGENT, prazan context)

**Pokretanje**: orkestrator koristi `Agent` tool s `subagent_type: "general-purpose"` i sljedećim prompt template-om:

```
ROLE: Ti si Agent 2A FILOZOF u GLAVNI INZINJER LEGAL pipeline-u.

KONTEKST: Ti NE ZNAS NIŠTA o aplikaciji za koju radimo. Ne znaš domenu, stack,
postojeći kod, problem koji se rješava. To je NAMJERNO (Pravilo L3 strikt
kineski zid). Tvoj zadatak je destilirati apstraktne principe iz kulturoloških
izvora — domena je već poznata Agentu 2B koji će tvoj output spojiti s
arhitekturom.

INPUT KOJE PRIMAS:
1. INOVACIJA_pojam.md (43 linije, originalna metodologija)
2. CLAUDE_CORE.md (75 linija, jezgra)
3. CLAUDE_FILTERI.md (Pravilo 14 anti-atraktor + numerology test)
4. Lista 5 ČUDNIH IZVORA — eksplicitno iz kulturoloških domena:
   <SEED-based izbor; orkestrator ti bira 5>

INPUT KOJI NE SMIJES TRAŽITI niti čitati:
- LEGAL_ARHITEKTURA.md
- README.md bilo kojeg tipa
- File tree
- Output drugih agenata
- Bilo što iz APLIKACIJA, RIJEKA_PRATILAC, ili sličnih repo-a
- Bilo što što sugerira tehničku domenu (ML, kriptografija, web, mobile)

OUTPUT:
3-5 kristala u formatu:

KRISTAL <N>: <kratak razumljiv naziv (Pravilo 32)>
  Izvor: <citiranje, npr. "Borges, 'Tlön, Uqbar, Orbis Tertius' (1940)">
  Apstraktni princip: <jedna rečenica destiliranog principa>
  Mehanicki kostur: <2-3 rečenice opisujući princip kao mjerljiv proces, bez
                     domenskog rječnika>
  Diskriminantni uvjet: <što čini ovaj princip neprimjenjivim na
                         astrologiju/numerologiju (Pravilo 12 numerology test)>
  [ERROR/FIX] markeri: <minimum 3 sycophancy flag-a unutar destilacije>

VRATI samo te kristale, jednu po jednu. Ne pokušavaj ih spojiti s nekom domenom
— to je posao Agenta 2B, ne tvoj.
```

**Trajanje**: subagent radi u svojem context-u (cca 5-15 min wall clock). Vraća output u jednu poruku.

**5 čudnih izvora**: orkestrator bira preliminarnu listu prije pokretanja, npr.:
- Knjizevnost: Borges "Garden of Forking Paths", Calvino "If on a winter's night a traveler", Stanisław Lem "Solaris", Ursula K. Le Guin "The Dispossessed"
- Mitologija: Ariadne i Tezej (Minotauer i nit), Janus (dvolicni bog), Mnemozyne (boginja pamćenja), Erinije (čuvarice zakletve)
- Filozofija: Wittgenstein "Tractatus" (granice jezika), Pascal "Misli" (kladim se), Kierkegaard "Strah i drhtanje"
- Antropologija: Levi-Strauss "Tužni tropi", Mauss "The Gift", Turner "The Ritual Process"
- Povijest knjizevnosti: Lichtenberg "Sudoperni knjigovođa", marginalne note srednjevjekovnih kompendija

Konkretan izbor 5 ide po SEED-u (reproducibility) — bilo koji od kategorija ako je SEED npr. 1234, vidljivost izvora odgovara konkretnoj kombinaciji.

### Korak 2B — Agent 2B INŽENJER (inline, glavna sesija)

Glavna sesija prima output Agenta 2A (3-5 kristala). Sad **prvi put** spaja:

- Kristali (od 2A)
- Filtrirane primitive (od 1 — iz Koraka 1)
- APLIKACIJA stack (već u kontekstu glavne sesije)

Bira **najbolji spoj** — 1, max 2 kandidata (Pravilo L5 depth > breadth).

Svaki kandidat MORA biti Tip A/B/C (Pravilo L1) i imati:
- Postojeću APLIKACIJA komponentu (path)
- Novu komponentu iz LEGAL_ARHITEKTURA §I-V
- Mjerljiv ROI broj (Pravilo L4, 3+ metrike)
- Eksplicitnu izjavu "Ne uvodi AI inferenciju, klasifikaciju, predikciju ili rekomendaciju"

Output u **kompozitnom template-u v1 LEGAL**:

```markdown
# Kandidat: <NAZIV>

**Tip (Pravilo L1)**: A / B / C
**Source ciklus**: CIKLUS_<int>_<date>
**Filozofski izvor**: <kristal N od Agenta 2A>
**Inženjerska teza**: <2-3 rečenice>

## Postojeća komponenta (mijenja se)
- File path: ...
- Trenutno ponašanje: ...

## Nova komponenta (iz LEGAL_ARHITEKTURA)
- §<I-V>.<broj>: ...
- Razlog: ...

## ROI metrike (Pravilo L4, 3+)
| # | Metrika | Prije | Poslije | Anchor |
| - | ------- | ----- | ------- | ------ |
| 1 | ...

## PhD-tehnička pitanja (Pravilo 16, 3+/5)
1. **Distribution shift**: ...
2. **Calibration**: ...
3. **Failure mode taxonomy**: ...

## 5 NAPADA + pobijanja (Pravilo 6)
| # | NAPAD | Pobijanje |
| - | ----- | --------- |

## Anti-AI izjava (Pravilo L6)
"Ovaj kandidat ne uvodi: AI inferenciju, klasifikator, prediktivni model,
generative AI sloj, recommender, personalizaciju. Ne aktivira AI Act
Article 3(1) AI system definiciju."

## Reference (Pravilo 24, 3 kategorije)
(a) AKADEMSKA: ...
(b) VENDOR: ...
(c) ANALOG (regulatorna ili kriptografska): ...

## LOC realnost (Pravilo 27)
src LOC: <X>; test LOC: <Y>; formula: X/75 + Y/50 + 2 = <Z> dana

## Patch summary (Pravilo 23 commit-able)
| File | Status | LOC |
| ---- | ------ | --- |

## Rollback plan
- Feature flag: ...
- Migracije idempotentne / drop-able: ...
```

### Korak 3 — Agent 3 UBOJICA (inline, glavna sesija)

Inline 7-test analiza:

- **Test 1 (Originalnost)**: ne-trivijan spoj? grep za "kao Stripe" / "kao Supabase" — ako >3 referenca → -1 bod
- **Test 2 (Snaga)**: 3+ ROI metrika s brojevima? Bez 3+ → FAIL
- **Test 3 (Primjenjivost)**: commit-able patch summary? File path-ovi specifirani?
- **Test 4 (Iskrenost)**: reference fact-check (Pravilo 29) — postoji li akademski paper s navedenim authorom/godinom?
- **Test 5 (Neočekivanost)**: alternativni stručnjak bi rekao "ovo je za drugu domenu, ne za nas"?
- **Test 6 (Razlikovnost)**: razlikuje se od ostalih kandidata u IDEJE/?
- **Test 7 (Alkemija)**: STRIKT — anti-AI grep (Pravilo L6); ako >2 AI-drift fraza → FAIL Test 7

Score 0-7. **Prijedlog**, finalni score od Agenta 5.

### Korak 5 — Agent 5 NEZAVISNI SUDAC (ODVOJEN SUBAGENT, prazan context)

**Pokretanje**: orkestrator koristi `Agent` tool s `subagent_type: "general-purpose"`:

```
ROLE: Ti si Agent 5 NEZAVISNI SUDAC u GLAVNI INZINJER LEGAL pipeline-u.

KONTEKST: tvoj zadatak je dati neovisnu ocjenu kandidatu kojeg je već proizveo
Agent 2B i provjerio Agent 3. Ti NE ZNAS njihov score (sycophancy zaštita).

INPUT KOJE PRIMAS:
1. Kandidat opis (u Pravilu L4 formatu)
2. Lista ostalih kandidata u trenutnom pass-u (samo imena + primarni ROI broj,
   ne puni opisi) — za Pravilo 28 anti-monoculture check
3. Tvoj vlastiti protokol: NEZAVISNI_SUDAC_LEGAL.md (ovaj dokument, sekcija
   "Sudac protokol")
4. PRAVILA L1-L6 (iz GLAVNI_INZINJER_PRAVILA_LEGAL_v1.md) — referenca

INPUT KOJI NE PRIMAŠ:
- Score od Agenta 3 UBOJICE
- Reasoning od Agenta 2B INŽENJERA (osim onog što je u kandidat opisu)
- Output od Agenta 1 IZVIDNIKA
- Glavni sesijski context (samo sažetak)

OUTPUT:
- 7-test STRICT review (vlastita ocjena, neovisno o UBOJICA)
- 5 realnost-provjera:
  R1 ROI realnost (Pravilo L4, spot-check 1 metrike)
  R2 LOC realnost (Pravilo 27)
  R3 Anti-monoculture (Pravilo 28 modificirano — po arhitekturnom obrascu)
  R4 Reference fact-check (Pravilo 29)
  R5 Over-engineering (Pravilo 30)
- DIVERGENCE REPORT ako delta od UBOJICA > 1 bod (orkestrator ti dade UBOJICA
  score nakon tvog grade-a, ne prije)
- REFRAKTOR signal: što treba popraviti
- SUDAC SIGNATURE: tvoja konacna ocjena (X/7)

Vrati u jednoj poruci.
```

**Trajanje**: 5-15 min wall clock.

### Korak 6 — Refrakcija + final commit (orkestrator, glavna sesija)

Orkestrator usporedi UBOJICA score (Korak 3) i SUDAC score (Korak 5):

- Ako delta > 1 bod → REFRAKTOR ciklus (Agent 2B prepravlja kandidat na temelju SUDAC signala, pa ide nazad u Agent 3 + Agent 5)
- Ako delta ≤ 1 bod i SUDAC ocjena ≥ 6/7 → kandidat **PROMOTE-ABLE** u `IDEJE/Ideja_<NAZIV>.md`
- Ako SUDAC < 6/7 → kandidat BACKLOG u `IDEJE/BACKLOG/`

### Korak 7 — Implementacija (sljedeća sesija ili u toj istoj)

Promote-an kandidat se implementira po patch summary-u. Tijekom implementacije:

- Pravilo 23 commit-able patch: svaki commit message referira CIKLUS_<int>_<date>
- LOC tracking: stvarni LOC se uspoređuje s procjenom u kandidatu (zatvori MTTR ako delta > 30%)
- A/B test ako kandidat ima feature flag

---

## Sudac protokol (NEZAVISNI_SUDAC_LEGAL.md ekvivalent inline)

**Test 1 (Originalnost)**: kandidat NIJE direktna kopija nečega što već postoji u APLIKACIJA repo-u ili open-source projektu. Ako jest → -1 bod.

**Test 2 (Snaga)**: 3+ ROI metrike s brojevima i anchor referencama. Bez 3+ → FAIL.

**Test 3 (Primjenjivost)**: patch summary sadrži file path-ove + LOC procjenu + rollback plan. Bez ova 3 → FAIL.

**Test 4 (Iskrenost)**: reference fact-check (Pravilo 29). Spot-check 1 nasumicnu referencu — ako autor/godina/naslov ne postoji → FAIL.

**Test 5 (Neočekivanost)**: zadovoljava li uvjet "stručnjak za drugu domenu reagira pozitivno"? Subjektivno; daj +1 ako da, 0 ako neutralno, -1 ako "ovo je trivijalno".

**Test 6 (Razlikovnost)**: razlikuje se od drugih kandidata u trenutnom pass-u (imena lista koju primaš)? Pravilo 28 anti-monoculture: ako 2+ kandidata isti arhitekturni obrazac (npr. svi mijenjaju watermark) → -1 bod.

**Test 7 (Alkemija — STRIKT)**: anti-AI grep (Pravilo L6) + anti-business grep:
- AI-drift fraze: "klasifikator", "model" (ML), "embedding", "LLM", "GPT", "Claude" (osim u "Anti-AI izjavi"), "AI sloj", "smart", "intelligent", "personalizacija", "recommender"
- Business-drift fraze: "EUR/mj" (osim u "ROI metrike #5" kao derivativni broj), "tier", "segment", "TAM", "ARR"
- Ako >2 hit-a → FAIL Test 7

**Realnost provjere R1-R5**: kao gore u prompt template-u. R1 i R5 najvažnije.

**Output format**:

```markdown
## Agent 5 NEZAVISNI SUDAC review

Kandidat: <NAZIV>
SEED: <broj>

### 7-test
T1 Originalnost: <0-1>/1
T2 Snaga: <0-1>/1
T3 Primjenjivost: <0-1>/1
T4 Iskrenost: <0-1>/1
T5 Neocekivanost: <0-1>/1
T6 Razlikovnost: <0-1>/1
T7 Alkemija (STRIKT): <0-1>/1

UKUPNO: <X>/7

### Realnost
R1 ROI realnost: PASS / DIVERGENCE (...)
R2 LOC realnost: PASS / FAIL (...)
R3 Anti-monoculture: PASS / WARN (...)
R4 Reference fact-check: PASS / FAIL (referenca <X> ne postoji)
R5 Over-engineering: PASS / FAIL (kompleksnost > vrijednost)

### REFRAKTOR signali
1. ...
2. ...

### SUDAC SIGNATURE
Kandidat <NAZIV>: <X>/7 USPJEH / POTENCIJALNO / BACKLOG.
Datum: <YYYY-MM-DD>
SEED: <broj>
```

---

## Integracija s IDEJE folderom

Promote-an kandidat ide u `APLIKACIJA/GLAVNI_INZINJER/IDEJE/Ideja_<NAZIV>.md`. Format:

```markdown
# Ideja: <NAZIV>

**Status**: USPJEH 7/7 / POTENCIJALNO 6/7 / BACKLOG <X>/7
**Datum**: YYYY-MM-DD
**Source ciklus**: CIKLUS_<int>_<date>.md
**Pipeline modus**: P1 / P2 / P3
**Tip (Pravilo L1)**: A / B / C

[full kandidat opis u L4 formatu]

[full Agent 5 SUDAC review]

[implementacijski plan: koje datoteke, kojim redoslijedom]
```

`IDEJE/CIKLUS_<int>_<date>.md` čuva sve agent output-e (Agent 1, 2A, 2B, 3, 5) za audit.

`IDEJE/BACKLOG/` sadrži kandidate koji nisu prošli SUDAC ≥ 6/7 — može se preispitati u budućnosti ako kontekst se promijeni.

---

## Geneza

Nastalo: 2026-04-27 popodne.
Razlog: korisnik je odobrio P2 hibrid kao default za APLIKACIJA cikluse. Trebao je standalone protokol koji ne ovisi o RIJEKA_PRATILAC GLAVNI_INZINJER_AGENTI.md (koji koristi pun P1 default).
Cilj: K1 LegalTech ciklus (Forensic audit trail per-output) može se pokrenuti čim je ovaj dokument završen.
