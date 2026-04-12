# CLAUDE.md - LegalTech Suite Pro Handoff

> **Last updated:** 2026-04-12 (Session 11)
> **Status:** 60+ generators, 21 modules, 142 tests; iznosi slovima, padezi, ZZK uputa, CZSS→ZAVOD ZA SOCIJALNI RAD
> **Deploy:** Streamlit Community Cloud from `hm53-byte/LEGAL-SUITE` main branch

---

## 1. PROJECT OVERVIEW & STACK

**LegalTech Suite Pro** is a Streamlit-based Croatian legal document generator.
It produces `.docx` (python-docx) files for 60+ document types across 15 legal areas.
All documents follow Croatian court formatting conventions (Times New Roman 12pt, 2.5cm margins, justified, `dd.mm.yyyy.` date format).

**Stack:** Python 3.10+, Streamlit ≥1.28.0, python-docx ≥1.0.0
**Run:** `streamlit run LEGAL-SUITE.py`
**Tests:** `python -m pytest tests/ -x -q` (129 tests, <1s)
**Deploy URL:** `https://legal-suite-flh3jnmcj5kc7jp5y9w9eb.streamlit.app`

---

## 2. ARCHITECTURE

```
LEGAL-SUITE.py          # Entry point: button sidebar nav + routing + landing page + vodič
                        # Navigation: st.session_state._active_module + st.button per module
                        # _NAV_SECTIONS dict defines 3 groups, _render_pocetna(), _render_vodic()
config.py               # CSS stilovi, design tokens (_BRAND, _ACCENT, _SIDEBAR_BG, etc.)
                        # Sidebar button styles, tab pills, hero-section, module-card
pomocne.py              # Shared helpers: _escape, _validiraj_oib (ISO 7064), _rimski_broj,
                        #   format_eur, format_text, format_navodnici, formatiraj_troskovnik,
                        #   unos_stranke, unos_vise_stranaka, spoji_stranke_html,
                        #   zaglavlje_sastavljaca, prikazi_dokument, docx_opcije,
                        #   odredi_nadlezni_sud, odabir_suda, unos_tocaka,
                        #   napuni_primjerom, provjeri_zastaru, provjeri_rok_zalbe,
                        #   PRIMJERI dict (5 document types with example data)
sudovi.py               # Baza 74 hrvatska suda (naziv, adresa, vrsta, grad)
pristojbe.py            # Kalkulator sudskih pristojbi (NN 118/18)
klauzule.py             # Biblioteka 17 standardnih ugovornih klauzula u 10 kategorija
docx_export.py          # _HtmlToDocxParser (HTMLParser subclass) -> python-docx
                        #   Supports: div classes, b/i/u, br, hr, table/tr/td, ul/ol/li, span
                        #   Watermark (VML), header with doc name, page numbers footer

generatori/             # Pure functions: take data -> return HTML string (60+ functions)
  ugovori.py            # 10 types    tuzbe.py    # 2 types    ovrhe.py    # 7 types
  zalbe.py              # 1 type      zemljisne.py # 7 types   opomene.py  # 1 type
  punomoci.py           # 1 type      trgovacko.py # 5 types   obvezno.py  # 8 types
  obiteljsko.py         # 5 types     upravno.py   # 4 types   kazneno.py  # 3 types
  stecajno.py           # 3 types     potrosaci.py # 3 types

stranice/               # Streamlit UI pages: forms -> call generators -> prikazi_dokument()
  # Pages with st.tabs (≤4 types): kazneno, upravno, potrosaci, stecajno
  # Pages with st.selectbox (>4 types): ugovori, ovrhe, zemljisne, trgovacko, obvezno, obiteljsko
  # Single-form pages: tuzbe, zalbe, opomene, punomoci, kamate, pristojbe
```

### Key Patterns

**Sidebar navigation** (`LEGAL-SUITE.py`):
```python
# Button-based nav (replaced radio groups in Session 8)
_NAV_SECTIONS = {"Ugovori i dokumenti": [...], "Sudski postupci": [...], "Alati i ostalo": [...]}
st.session_state._active_module = "Početna"  # tracks active module
# Each module is a st.sidebar.button with type="primary" if active, "secondary" otherwise
# Click -> set _active_module -> st.rerun()
```

**Generator pattern:** `def generiraj_xxx(...) -> str` returns HTML fragments using `parts.append()`, wrapped in try-except, all inputs through `_escape()`.

**Page pattern:** `def render_xxx()` with st.header, form inputs, `if st.button("Generiraj"): prikazi_dokument(doc_html, "File.docx", "Preuzmi")`

**CSS classes in generated HTML** (defined in `config.py`):
- `.header-doc`, `.party-info`, `.doc-body`, `.justified`, `.section-title`
- `.cost-table`, `.clausula`, `.signature-row`, `.signature-block`

---

## 3. WHAT WE JUST COMPLETED (Session 8)

### Sidebar Navigation Rewrite
- **Replaced 3 `st.radio` groups with `st.button` navigation** — fixes critical bug where user couldn't re-click already-selected module
- `_active_module` session_state key tracks current module
- `_NAV_SECTIONS` dict organizes 18 modules into 3 sections
- Golden uppercase section headers via `.sidebar-section` CSS class

### Sidebar Button Visibility Fix
- **Secondary buttons had white text on white background** — CSS rule `[data-testid="stSidebar"] * { color: _SIDEBAR_TEXT }` was overriding button text color
- **Fix:** Added explicit CSS for sidebar buttons: `background-color: transparent`, `color: _SIDEBAR_TEXT`, `border: rgba(203,213,225,0.15)`
- Active button: navy gradient with white text; inactive: transparent with light gray text

### Vodič "Koji dokument mi treba?"
- Interactive wizard in `_render_vodic()` in `LEGAL-SUITE.py`
- 10 problem categories (dugovanje, presuda, upravno, ugovor, kazneno, nekretnina, potrošač, tvrtka, obitelj, dužnik)
- Each shows step-by-step legal guidance with deadlines and "Izradi →" buttons that navigate to relevant modules
- Added to sidebar under "ALATI I OSTALO"

### "Napuni primjerom" System
- `PRIMJERI` dict in `pomocne.py` with 5 document types: tuzba, ovrha, opomena, kaznena_prijava, zalba_zup
- `napuni_primjerom(tip, prefix)` shows expander with description + button that populates session_state and reruns
- Integrated in: `stranice/tuzbe.py`, `stranice/kazneno.py`

### Deadline Checking
- `provjeri_zastaru(datum, rok_godina, opis)` — checks statute of limitations (expired/approaching/info)
- `provjeri_rok_zalbe(datum, rok_dana, opis)` — checks appeal deadline
- Integrated in: tuzbe (5yr zastara), zalbe (15-day rok)

### UI Improvements (earlier in session)
- Pages with ≤4 types converted from selectbox to `st.tabs`: kazneno, upravno, potrosaci, stecajno
- Landing page with hero section, module cards, "Otvori →" buttons
- `zaglavlje_sastavljaca()` added to: zalbe, ovrhe, punomoci, upravno (was missing)
- `unos_tocaka()` with `s_dokazima=True` for structured evidence in tuzbe, zalbe

### Tests
- 129 tests passing (up from 116)

---

## 4. CURRENT STATE & KNOWN ISSUES

### Known Bugs
1. **Sidebar button CSS may not apply on Streamlit Cloud** — the CSS selector `[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]` works locally but Streamlit Cloud may cache old CSS or use different DOM structure. If buttons still show white-on-white, the CSS selectors may need updating for the specific Streamlit version deployed.
2. **`napuni_primjerom` key mapping** — the function sets `session_state[f"{prefix}_{key}"]` but this only works if widget keys in `unos_stranke()` match the pattern. Currently only verified for tuzbe and kaznena_prijava. Other pages need PRIMJERI entries + key mapping verification.

### Tech Debt
1. **docx_export.py** — may miss edge cases with deeply nested tags, colspan/rowspan
2. **No input length limits** — text_area inputs have no max_chars
3. **Some date fields still use text_input** — roditeljska_skrb, ugovor_uzdrzavanje children dates
4. **`napuni_primjerom` only on 2 pages** — user wants it on all form pages

### Files Modified This Session
- `LEGAL-SUITE.py` — **complete rewrite** (sidebar buttons, vodič, landing page)
- `config.py` — sidebar button CSS, tab pills CSS, hero/card CSS
- `pomocne.py` — PRIMJERI, napuni_primjerom, provjeri_zastaru, provjeri_rok_zalbe, unos_tocaka
- `stranice/tuzbe.py` — napuni_primjerom + provjeri_zastaru
- `stranice/zalbe.py` — zaglavlje_sastavljaca + provjeri_rok_zalbe + date_input
- `stranice/kazneno.py` — st.tabs + napuni_primjerom
- `stranice/upravno.py` — st.tabs + zaglavlje_sastavljaca
- `stranice/potrosaci.py` — st.tabs
- `stranice/stecajno.py` — st.tabs
- `stranice/ovrhe.py` — zaglavlje_sastavljaca
- `stranice/punomoci.py` — zaglavlje_sastavljaca

---

## 5. IMMEDIATE NEXT TASKS

### Priority 1: Fix Streamlit Cloud deploy
The deployed app may still show old CSS (white sidebar buttons). Verify by visiting the deploy URL. If broken:
- Check Streamlit version on Cloud vs local
- May need to reboot app from Streamlit Cloud dashboard
- CSS selectors may need adjustment for Cloud's Streamlit version

### Priority 2: Add `napuni_primjerom` to more pages
Currently only on tuzbe and kaznena_prijava. Add to:
- `stranice/ovrhe.py` — use PRIMJERI['ovrha']
- `stranice/opomene.py` — use PRIMJERI['opomena']
- `stranice/upravno.py` — use PRIMJERI['zalba_zup']
- Need to verify key mappings match widget keys in each page

### Priority 3: Remaining short-term improvements
User's explicit roadmap (verbatim):

**Kratkoročno (no new dependencies):**
- PDF preskočiti jer je poanta docx da bude lakše urediti dokument
- ~~Predlošci sudova~~ ✅ DONE (sudovi.py, 74 courts)
- ~~OIB kontrola sume~~ ✅ DONE (ISO 7064 mod-11-10)
- ~~Podrška za više stranaka~~ ✅ DONE (unos_vise_stranaka)
- ~~Predlošci članaka~~ ✅ DONE (klauzule.py, 17 clauses)

**Srednjoročno:**
1. Baza propisa — integracija s zakon.hr ili nn.hr za dohvat aktualnih zakonskih tekstova
2. ~~Kalkulator sudskih pristojbi~~ ✅ DONE (pristojbe.py)
3. e-Komunikacija — priprema dokumenata za elektroničko podnošenje sudu
4. ~~Vodič za korisnike~~ ✅ DONE (vodič wizard)
5. Višekorisnička podrška — prijava, spremanje dokumenata, povijest

### Long-term architectural vision

User has provided an extensive technical spec for scaling to production SaaS. Key constraint: **implement ONLY if achievable for free with limited risk.** Major elements:

- **PostgreSQL + RLS** for multi-tenant isolation (Chinese Wall conflict-of-interest prevention)
- **Event Sourcing** with audit.change_log (AFTER triggers, JSONB old_data/new_data, GIN indexes)
- **GDPR crypto-shredding** — per-client AES-256-GCM key; destroy key = destroy data
- **WebSocket collaboration** via Socket.IO (presence detection, optimistic locking with version column)
- **React Hook Form + Zod** if migrating from Streamlit (useFieldArray for multiple parties, superRefine for cross-field validation)
- **PostGIS court mapping** — ST_Contains() for jurisdiction lookup by coordinates
- **pg_trgm fuzzy search** for court name matching
- **NLP Croatian declension** — grammatical cases for names in documents (python `deklinacija` library)
- **MDAST document assembly** — AST-based template engine instead of string concatenation
- **Token Bucket rate limiter** for Narodne Novine API (3 req/s, asyncio.Lock)
- **FINA e-Potpis** — qualified electronic signature via Cloud API
- **Peppol SBDH** — XML containers for e-filing with courts
- **OIB validation** — already done (ISO 7064 mod-11-10 in pomocne.py)

---

## 6. CONVENTIONS

### Code Style
- **Language:** Python code in English (function names, variables), UI text in Croatian
- **Comments/docstrings:** Croatian (informal)
- **Generator functions:** Always prefix `generiraj_` + document type
- **Page functions:** Always prefix `render_` + module name
- **Private helpers:** Prefix `_` (e.g., `_escape`, `_rimski_broj`)
- **Streamlit widget keys:** Use prefixes per document type to avoid collisions (e.g., `sr_`, `zup_`, `ps_`)

### Legal Document Formatting
- **Font:** Times New Roman 12pt (body), 14pt (headers), 11pt (section titles)
- **Margins:** 2.5cm all sides
- **Text:** Justified, line-height 1.5
- **Currency:** `format_eur()` -> `10.000,00 EUR`
- **Date:** `dd.mm.yyyy.` (trailing dot is standard in Croatian)
- **OIB:** 11-digit national ID, displayed as plain number

### HTML Structure in Generators
All generators output HTML fragments (not full documents). The wrapper `<div class='legal-doc'>` is added by `prikazi_dokument()`. Use only these CSS classes:
- `header-doc`, `party-info`, `doc-body`, `justified`, `section-title`
- `cost-table`, `clausula`, `signature-row`, `signature-block`
- Inline styles allowed for: `text-align`, `font-weight`, `margin-top`, `font-size`

### Adding a New Document Type
1. Add generator function in appropriate `generatori/xxx.py`
2. Export from `generatori/__init__.py`
3. Add UI form in `stranice/xxx.py` (inside existing `render_xxx()` with selectbox/tabs, or new file)
4. If new module: export from `stranice/__init__.py`, add to `_NAV_SECTIONS` in `LEGAL-SUITE.py`
5. Pattern: `parts.append()` + `"".join(parts)`, wrap in try-except, use `_escape` on all inputs

---

## 7. ENVIRONMENT

- **Python:** 3.10+
- **OS:** Windows (paths use backslashes, terminal is cp1252 - emoji may show encoding warnings, harmless)
- **Launch:** `streamlit run LEGAL-SUITE.py --server.headless true` (port 8501)
- **IDE config:** `.claude/launch.json` configured for Streamlit
- **Git remote:** `https://github.com/hm53-byte/LEGAL-SUITE.git` (main branch)
- **Deploy:** Streamlit Community Cloud auto-deploys from main

---

## 8. SESSION HISTORY

| Session | Key Deliverables |
|---------|-----------------|
| 1 | Monolith → modular architecture, XSS, OIB, DOCX export |
| 2 | Extended generators (opomene, punomoci, trgovacko, obvezno, ovrhe, zemljisne, ugovori, tuzbe) |
| 3 | New legal areas (obiteljsko, upravno, kazneno, stecajno, potrosaci) + professional UI |
| 4 | Court DB, multi-party support, fee calculator, clause library, 112 tests |
| 5 | zaglavlje_sastavljaca consistency, signature blocks, kamate calculator |
| 6 | Tooltips, landing page, deployment guide, 112+ tests |
| 7 | DOCX watermark, DOCX header, docx_opcije, 116 tests |
| 8 | Button sidebar nav, vodič wizard, napuni_primjerom, deadline checks, tabs, CSS fixes, 129 tests |
| 9 | **Sidebar CSS fix (Cloud), ikone u sidebaru, vodič redizajn (kartice+težina), quick start, success banner, help tekst, napuni_primjerom na opomene/upravno** |
| 10 | **UI overhaul: fix nn_pretraga/eoglasna/kalendar bugs, redesign login (guest-first), sidebar search, emoji cleanup, data-driven routing, CSS polish** |
