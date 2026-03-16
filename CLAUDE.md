# CLAUDE.md - LegalTech Suite Pro Handoff

> **Last updated:** 2026-03-16
> **Status:** 60+ generators, 16 modules, 112 tests, court DB, fee calculator - COMPLETE

---

## 1. PROJECT OVERVIEW

**LegalTech Suite Pro** is a Streamlit-based Croatian legal document generator.
It produces `.docx` (python-docx) files for 60+ document types across 15 legal areas.
All documents follow Croatian court formatting conventions (Times New Roman 12pt, 2.5cm margins, justified, `dd.mm.yyyy.` date format).

**Run:** `streamlit run LEGAL-SUITE.py`
**Dependencies:** `streamlit>=1.28.0`, `python-docx>=1.0.0` (see `requirements.txt`)

---

## 2. ARCHITECTURE

```
LEGAL-SUITE.py          # Entry point: sidebar routing (3 radio groups, 16 modules)
config.py               # CSS stilovi, color variables (_PRIMARY, _ACCENT, etc.)
pomocne.py              # Shared helpers: _escape, _validiraj_oib (ISO 7064), _rimski_broj,
                        #   format_eur, format_text, format_navodnici, formatiraj_troskovnik,
                        #   unos_stranke, unos_vise_stranaka, spoji_stranke_html,
                        #   zaglavlje_sastavljaca, prikazi_dokument,
                        #   odredi_nadlezni_sud, odabir_suda
sudovi.py               # Baza 74 hrvatska suda (naziv, adresa, vrsta, grad)
                        #   dohvati_sudove(), format_sud_s_dijakriticima()
pristojbe.py            # Kalkulator sudskih pristojbi (NN 118/18)
                        #   pristojba_tuzba/zalba/revizija/ovrha/zk/upravni_spor
klauzule.py             # Biblioteka 17 standardnih ugovornih klauzula u 10 kategorija
docx_export.py          # _HtmlToDocxParser (HTMLParser subclass) -> python-docx
                        #   Supports: div classes, b/i/u, br, hr, table/tr/td, ul/ol/li, span
                        #   Functions: html_u_docx(), pripremi_za_docx()
                        #   Footer: "Stranica X od Y" (Word field codes)

generatori/             # Pure functions: take data -> return HTML string
  __init__.py           # Re-exports all 60+ generator functions
  ugovori.py            # 10: prilagodeni, standard, rad, otkaz, aneks, upozorenje,
                        #     rad_na_daljinu, sporazumni_prestanak, zabrana_natjecanja, potvrda
  tuzbe.py              # 2: tuzbu_pro, brisovnu_tuzbu
  ovrhe.py              # 7: ovrhu_pro, prigovor, ovrsna_isprava, nekretnina, placa,
                        #     obustava, privremena_mjera
  zalbe.py              # 1: zalbu_pro
  zemljisne.py          # 7: tabularna, zk_prijedlog, zabiljezba, predbiljezba,
                        #     hipoteka, brisanje_hipoteke, sluznost
  opomene.py            # 1: opomenu
  punomoci.py           # 1: punomoc
  trgovacko.py          # 5: drustveni_ugovor, odluka_skupstine, prijenos_udjela, nda, zapisnik
  obvezno.py            # 8: darovanje, cesija, kompenzacija, jamstvo, gradenje,
                        #     licencija, posredovanje, sporazumni_raskid
  obiteljsko.py         # 5: sporazum_razvod, tuzbu_razvod, bracni_ugovor,
                        #     roditeljska_skrb, ugovor_uzdrzavanje
  upravno.py            # 4: zalba_zup, tuzba_zus, zahtjev_informacije, prigovor_predstavka
  kazneno.py            # 3: kaznena_prijava, privatna_tuzba, zalba_kaznena_presuda
  stecajno.py           # 3: prijedlog_stecaj, prijava_trazbine, stecaj_potrosaca
  potrosaci.py          # 3: reklamacija, jednostrani_raskid, prijava_inspekciji

stranice/               # Streamlit UI pages: forms -> call generators -> prikazi_dokument()
  __init__.py           # Re-exports all 15 render_* functions
  ugovori.py            # render_ugovori() - st.selectbox for 10 document types
  tuzbe.py              # render_tuzbe()
  ovrhe.py              # render_ovrhe() - st.selectbox for 7 document types
  zalbe.py              # render_zalbe()
  zemljisne.py          # render_zemljisne() - st.selectbox for 7 types
  kamate.py             # render_kamate() - interest calculator (no generator)
  opomene.py            # render_opomene()
  punomoci.py           # render_punomoci()
  trgovacko.py          # render_trgovacko() - st.selectbox for 5 types
  obvezno.py            # render_obvezno() - st.selectbox for 8 types
  obiteljsko.py         # render_obiteljsko() - st.selectbox for 5 types
  upravno.py            # render_upravno() - st.selectbox for 4 types
  kazneno.py            # render_kazneno() - st.selectbox for 3 types
  stecajno.py           # render_stecajno() - st.selectbox for 3 types
  potrosaci.py          # render_potrosaci() - st.selectbox for 3 types
```

### Key Patterns

**Generator pattern** (all generators follow this):
```python
def generiraj_xxx(arg1, arg2, ...):
    """Generira HTML za [dokument]."""
    try:
        e = _escape  # from pomocne import _escape
        parts = []
        parts.append("<div class='header-doc'>NASLOV</div>")
        parts.append(f"<div class='party-info'>...")
        parts.append(f"<div class='doc-body'>...")
        # ... build document
        return "".join(parts)
    except Exception:
        return "<div class='doc-body'>Greska pri generiranju dokumenta.</div>"
```

**Page pattern** (all pages follow this):
```python
def render_xxx():
    st.header("Naziv modula")
    vrsta = st.selectbox("Vrsta dokumenta", [...])  # if multiple types
    # ... form inputs in st.expander sections
    if st.button("Generiraj", type="primary"):
        doc_html = generiraj_xxx(...)
        prikazi_dokument(doc_html, "Filename.docx", "Preuzmi")
```

**Document display** (`prikazi_dokument` in `pomocne.py`):
1. Renders HTML in `<div class='legal-doc'>` for on-screen preview
2. Passes HTML through `docx_export.pripremi_za_docx()` -> python-docx bytes
3. `st.download_button` with `.docx` mime type

**Sidebar routing** (`LEGAL-SUITE.py`):
- 3 `st.sidebar.radio` groups: `nav_ugovori` (6 items), `nav_sudski` (7 items), `nav_alati` (2 items)
- `_get_active_module()` tracks which group last changed via `st.session_state._prev_nav`
- Solves Streamlit's limitation of no cross-radio mutual exclusion

**CSS classes used in generated HTML** (defined in `config.py`):
- `.legal-doc` - outer wrapper (white bg, shadow, max-width 800px, centered)
- `.header-doc` - document title (centered, bold, uppercase, Times New Roman 14pt)
- `.party-info` - party info block (left-aligned)
- `.doc-body` / `.justified` - body text (justified, Times New Roman, line-height 1.5)
- `.section-title` - section heading (bold, uppercase, 11pt)
- `.cost-table` / `.cost-table td` - cost breakdown table
- `.clausula` - special clause box (italic, border, bg)
- `.signature-row` / `.signature-block` - signature area (flex, space-between)

**Formatting helpers:**
- `_escape(text)` -> `html.escape(str(text))` with None guard
- `_rimski_broj(n)` -> unlimited Roman numerals
- `format_eur(iznos)` -> `"10.000,00 EUR"` (Croatian format: dot=thousands, comma=decimal)
- `format_text(text)` -> escape + `\n` to `<br>` + format_navodnici
- `format_navodnici(text)` -> ASCII `"..."` to Croatian `„<i>...</i>"` (U+201E/U+201C)
- `formatiraj_troskovnik(troskovi)` -> HTML cost table from dict `{stavka, pdv, materijalni, pristojba}`
- `_validiraj_oib(oib_str)` -> ISO 7064 mod-11-10 checksum (warning only, non-blocking)
- `odabir_suda(label, vrsta, key)` -> selectbox from court database with manual input fallback
- `unos_vise_stranaka(oznaka, key_prefix)` -> dynamic add/remove multiple parties

---

## 3. WHAT IS COMPLETED

### Priority 1 - Core generators (Session 1)
- [x] Refactored from monolith to modular architecture
- [x] XSS protection (`_escape` on all user inputs)
- [x] OIB validation (11 digits, warning)
- [x] try-except in all generators
- [x] Unlimited Roman numerals
- [x] `format_eur()` Croatian currency formatting
- [x] DOCX export via python-docx (`docx_export.py`)

### Priority 2 - Extended generators (Session 2)
- [x] Opomene (1 doc), Punomoci (1 doc)
- [x] Trgovacko pravo (5 docs)
- [x] Obvezno pravo (8 docs)
- [x] Ovrhe extended (7 docs total)
- [x] Zemljisne knjige extended (7 docs total)
- [x] Ugovori extended (10 docs total, incl. radno pravo)
- [x] Tuzbe extended (2 docs total)

### Priority 3 - New legal areas (Session 3)
- [x] Obiteljsko pravo (5 docs)
- [x] Upravno pravo (4 docs)
- [x] Kazneno pravo (3 docs)
- [x] Stecajno pravo (3 docs)
- [x] Zastita potrosaca (3 docs)

### UI/UX (Session 3)
- [x] Professional UI in `config.py` (Inter font, gradient sidebar, gold accents)
- [x] Grouped sidebar navigation (3 sections with golden uppercase headers)
- [x] Centralized CSS with color variables
- [x] Print-friendly styles
- [x] All 16 modules tested via Streamlit

### Session 4 - Infrastructure & Quality
- [x] OIB ISO 7064 mod-11-10 proper checksum validation
- [x] Court database (`sudovi.py`) - 74 courts with selectbox helper
- [x] Multiple parties support (`unos_vise_stranaka`)
- [x] Court selectbox integrated in all 11 page modules (17+ fields)
- [x] Court fee calculator (`pristojbe.py` + `stranice/pristojbe_stranica.py`)
- [x] Auto-pristojba in tuzbe, zalbe, ovrhe, zemljisne pages
- [x] Template clauses library (`klauzule.py` - 17 clauses, 10 categories)
- [x] Smart Croatian quotation marks (`format_navodnici`)
- [x] DOCX footer page numbers ("Stranica X od Y")
- [x] DOCX `<hr>` tag support + signature horizontal lines
- [x] Input validation (VPS, empty field warnings, date_input)
- [x] Removed legacy `pripremi_za_word()` dead code
- [x] Removed local `_rimski()` copy from kazneno.py
- [x] 112 unit tests (pomocne, sudovi, pristojbe, all generators, docx_export, edge cases) -> now 116

### Session 5 - Consistency & Quality
- [x] `zaglavlje_sastavljaca()` integrated in all 7 remaining pages
- [x] Signature blocks standardized in all generators (replaced `<table>` with `signature-row`/`signature-block`)
- [x] Kamate calculator rewritten with HNB zakonske zatezne stope, DOCX export

### Session 6 - Polish & Deployment
- [x] Help tooltips on key form fields (tuzbe, ovrhe, zemljisne, obvezno, trgovacko)
- [x] 112 unit tests (+25 edge case tests: empty inputs, special chars, DOCX signature blocks)
- [x] XSS fix: `_escape(vrsta)` in tuzbe generator
- [x] `format_eur()` robustness (handles string/invalid input gracefully)
- [x] Informative landing page ("Pocetna") with overview of 60+ documents and 15 areas
- [x] Deployment guide (`upute.md`) for Streamlit Community Cloud

### Session 7 - DOCX Export Enhancements
- [x] DOCX watermark ("NACRT") via VML shape in header (diagonal, gray, 25% opacity)
- [x] DOCX header with document name (italic gray text + bottom border line)
- [x] `docx_opcije()` expander on all document pages (watermark + header checkboxes)
- [x] `pripremi_za_docx()` and `html_u_docx()` extended with `watermark` and `naslov_dokumenta` params
- [x] 116 unit tests (+4 watermark/header tests)

---

## 4. KNOWN ISSUES / TECH DEBT

1. **docx_export.py `_HtmlToDocxParser`** - handles most HTML but may miss edge cases with deeply nested tags, colspan/rowspan, or complex inline styles
2. **No input length limits** - text_area inputs have no max_chars
3. **Some pages lack date_input** - a few date fields still use text_input (roditeljska_skrb, ugovor_uzdrzavanje children dates)

---

## 5. NEXT TASKS

### Short-term (no new dependencies)
1. **e-Komunikacija preparation** - format documents for electronic court filing
2. **User guide / tooltips** - help text explaining each field's legal significance
3. **More comprehensive generator tests** - edge cases (empty inputs, very long text, special characters)

### Medium-term
4. **Legal database integration** - scrape/API from zakon.hr or nn.hr for current law text
5. **Multi-user support** - authentication, document history, saved drafts

### Long-term architectural vision (user's detailed spec)

The user has provided a comprehensive architectural vision for scaling to a production SaaS platform. Key elements (implement **only if achievable for free with limited risk**):

#### Database & Security
- **PostgreSQL with RLS (Row-Level Security)** - tenant isolation via `SET LOCAL app.current_tenant_id`
- **ABAC (Attribute-Based Access Control)** with Chinese Wall constraints (conflict-of-interest prevention between clients)
- **Event Sourcing** - immutable event log for all document mutations, `documents_events` table with `(aggregate_id, version, event_type, payload, created_by, created_at)`
- **GDPR crypto-shredding** - per-client AES-256-GCM encryption key in separate key vault; delete key = delete all data

#### Real-time Collaboration
- **WebSocket** via Socket.IO - operational transforms for concurrent document editing
- **Presence protocol** - cursor positions, active field indicators

#### Frontend (if migrating from Streamlit)
- **React Hook Form + Zod** for form validation with discriminated unions per document type
- **MDAST (Markdown Abstract Syntax Tree)** document assembly pipeline

#### Croatian-specific Features
- **OIB validation** - ISO 7064 mod-11-10 (algorithm: carry=10, for each digit: carry=(carry+digit)%10, if carry==0 carry=10, carry=(carry*2)%11; final: (11-carry)%10 == last_digit)
- **PostGIS court mapping** - spatial lookup of nadlezni sud by address coordinates
- **NLP Croatian name declension** - proper grammatical cases for names in legal documents (nominativ/genitiv/dativ/akuzativ/vokativ/lokativ/instrumental)
- **Token Bucket rate limiter** for Narodne Novine API integration

#### Digital Signatures & e-Filing
- **FINA e-Potpis** - qualified electronic signature integration
- **Peppol SBDH (Standard Business Document Header)** XML containers for e-invoicing/e-filing

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
3. Add UI form in `stranice/xxx.py` (inside existing `render_xxx()` with selectbox, or new file)
4. If new module: export from `stranice/__init__.py`, add to sidebar in `LEGAL-SUITE.py`
5. Pattern: `parts.append()` + `"".join(parts)`, wrap in try-except, use `_escape` on all inputs

---

## 7. ENVIRONMENT

- **Python:** 3.10+
- **OS:** Windows (paths use backslashes, terminal is cp1252 - emoji may show encoding warnings, harmless)
- **Launch:** `streamlit run LEGAL-SUITE.py --server.headless true` (port 8501)
- **IDE config:** `.claude/launch.json` configured for Streamlit
