# HANDOFF — preostali C-fixovi za sljedeću sesiju

**Datum**: 2026-04-27 (zatvaranje sesije)
**Sljedeća sesija ulazi s**: čistim kontekstom, full toks budgetom

---

## Što je danas isporučeno (kratko)

- **K1.5** UI ožičenje audit chain-a kroz 16 stranica × 88 call-sites — gotovo, push-an
- **K2** BRZ_MOZAK ciklus "Hermesov sync outbox" 7/7 USPJEH — promote-an, čeka cloud setup za implementaciju
- **K5.2** Refaktor Jednostavnog moda u objektivni katalog — gotovo, push-an (uklonjeno "Netko mi duguje novac" + Pravna Kata flow + svi prescriptive `aia` savjeti)
- **A1-A4** UX bugovi popravljeni: kartice ne izgledaju kao gumbi, auto-scroll fix, detalj-stavke clickable, sidebar "> " prefiks uklonjen
- **GOAT Ciklus 1** za odabir MOR platforme — pobjednik **Polar.sh** (vidi `GOAT/PREPORUKA_MOR.md`)
- Playwright load test script (`scripts/load_test.py`) — 20 useri stabilno, 200 puca na Windows fd limit (ne app bug)

Sve push-ano na `origin/main`, baseline commit `2464b1d` → trenutni HEAD nakon ovog handoff-a.

---

## Preostali C-fixovi (tehnički dug)

### C1: Ukloni `api_epredmet.py` modul

**Razlog**: e-Predmet javnog GraphQL API-ja **nikad nije bilo**. Endpoint `https://e-predmet.pravosudje.hr/api/` u kodu je fiktivan — uvijek vraća error → fallback na `_DEMO_SUDOVI` (statična lista 14 sudova). Korisnik vidi placeholder "API trenutačno nije dostupan, koristimo lokalnu bazu sudova" što stvara dojam kvar-a, a zapravo nikad nije radilo.

**Akcija**:

```bash
# 1. Obriši API klijent
rm api_epredmet.py

# 2. Obriši stranicu
rm stranice/epredmet.py

# 3. Ukloni iz stranice/__init__.py
# Ukloni red: from stranice.epredmet import render_epredmet

# 4. Ukloni iz LEGAL-SUITE.py:
#   - import linije: render_epredmet
#   - _MODULI dict: "e-Predmet" entry
#   - _alati listu na Početnoj: ("e-Predmet", "Pracenje sudskih predmeta")

# 5. Pytest verify
python -m pytest tests/ -q   # treba: 194/194 pass

# 6. Commit
git commit -m "feat(C1): ukloni api_epredmet — fiktivni GraphQL API"
```

**LOC**: -300 (api_epredmet.py 156 + stranice/epredmet.py 185 - imports/refs).

---

### C2: Port e-Oglasna scrapera iz RIJEKA_PRATILAC

**Razlog**: e-Oglasna API (`api_eoglasna.py`) je isto fiktivan. RIJEKA_PRATILAC u `C:\Users\Hrvoje Matej\Desktop\RIJEKA_PRATILAC\src\e_oglasna_scraper.py` ima **283 LOC pravi scraper** koji radi:
- BeautifulSoup + lxml za HTML parsing
- pypdf za PDF dokumente
- Rate limiter (2 req/s)
- Regex parsing UUID-a, brojeva predmeta, OIB-a
- Persist u DB

**Akcija**:

1. **Read referenca**: `C:\Users\Hrvoje Matej\Desktop\RIJEKA_PRATILAC\src\e_oglasna_scraper.py`

2. **Adaptacija za APLIKACIJA stack**:
   - Zamijeni `from .config import settings` s hardcoded base URL `https://e-oglasna.pravosudje.hr`
   - Zamijeni `from .db import upsert_document` s in-memory return liste (Streamlit nema DB — koristit `@st.cache_data` umjesto persist)
   - Zamijeni `from .http_utils import RateLimiter, make_client` s minimalnim httpx wrapper-om ili zadrži via mini http_utils.py adaptaciju
   - Zadrži `_parse_listing`, `_parse_detail`, `iter_listing`, `fetch_detail`

3. **Dependencies provjera**: `requirements.txt` mora imati `beautifulsoup4`, `lxml`, `pypdf` (ako nedostaju, dodaj).

4. **Refaktor `stranice/eoglasna.py`**: zameni call-eve fiktivnih API-ja s pravim scraper funkcijama.

5. **Pytest**: dodaj `tests/test_eoglasna_parser.py` (referenca: `RIJEKA_PRATILAC/tests/test_e_oglasna_parser.py`).

6. **Commit**: `feat(C2): port e-Oglasna scrapera iz RIJEKA_PRATILAC`

**LOC**: ~300 src + 50 test = 350 LOC, **~4-6h solo dev rok**.

**Glavni rizici**:
- HTML struktura e-Oglasna stranice se može promijeniti → scraper puca. Mitigacija: integration test mjesečno + alert ako 0 rezultata.
- Robots.txt poštovanje (RIJEKA_PRATILAC referenca već to radi, zadrži).
- PDF parsing failures — graceful degradation (vrati metadata bez PDF teksta).

---

## Što NIJE u C-fixovima (drugi prioriteti)

- **Pristojbe crash** — vjerojatno bila posljedica load testa 200 useri (Windows fd limit), ne bug u pristojbe modulu. Provjeri ponovo na svježem Streamlit pokretanju; ako se i dalje ruši, pošalji traceback.
- **NN bugovi** — `api_nn.py` koristi pravi NN endpoint (ELI/JSON-LD), vjerojatno radi. Provjeri pri testiranju, fix ako specifičan bug.
- **K2 implementacija** (Hermesov sync outbox) — čeka cloud setup
- **K3 → Polar migracija** — vidi `GOAT/PREPORUKA_MOR.md` za 345 LOC plan; čeka Polar account + sandbox test

---

## Ulaz u sljedeću sesiju

```bash
cd "C:\Users\Hrvoje Matej\Documents\APLIKACIJA"
git pull   # provjeri da imaš zadnji main
git log --oneline -10   # trebaš vidjeti GOAT Ciklus 1 commit kao zadnji
```

Prvi korak: pročitati ovaj handoff + `GOAT/PREPORUKA_MOR.md`. Onda krenuti C1 (~30 min) → C2 (~4-6h).

Nakon C-fixova: K3 → Polar migracija (vidi `PREPORUKA_MOR.md` integration plan, 5-7 dana).

---

## Stack status checkpoint

- **194/194 pytest pass** (lokalno)
- **Push-ano**: zadnji commit `0e7b639` (A4 sidebar prefix); GOAT Ciklus 1 commit slijedi
- **Cloud setup**: NIJE pokrenut (čeka Polar migraciju umjesto Stripe)
- **Streamlit Cloud deploy**: aktivan na `https://legal-suite-flh3jnmcj5kc7jp5y9w9eb.streamlit.app` ali **graceful degradation** drži — entitlements/audit_chain su no-op bez Supabase credentials

Spreman za clear context. Sljedeća sesija dolazi sa svježim tokenima.
