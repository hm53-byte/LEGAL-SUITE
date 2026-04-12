# UPUTE ZA SESIJU 12 — LegalTech Suite Pro

> Napravljeno u sesiji 11 (2026-04-12). Stanje: 142 testa, svi prolaze.
> Git: `hm53-byte/LEGAL-SUITE` main branch, commit `00025bc`
> Deploy: `https://legal-suite-flh3jnmcj5kc7jp5y9w9eb.streamlit.app`

---

## ŠTO JE NAPRAVLJENO U SESIJI 11

### 1. Iznosi slovima (`pomocne.py`)
- Dodane funkcije: `_broj_rijecima_hr(n)`, `iznos_slovima(iznos)`, `format_eur_s_rijecima(iznos)`
- `format_eur_s_rijecima()` vraća: `1.500,00 EUR (slovima: tisuću petsto eura)`
- Primijenjeno u generatorima: opomene, ovrhe, tužbe, obiteljsko, stečajno, obvezno, potrošači, posrednik_najam, zemljišne, trgovačko
- **NAPOMENA:** `formatiraj_troskovnik()` u `pomocne.py` namjerno i dalje koristi `format_eur()` (tablice troškova ne trebaju slovima)

### 2. Padezi (`pomocne.py`)
- Dodan `_PADEZI_ULOGA` dict (30+ pravnih uloga) i `_padez_uloge(uloga, padez)` funkcija
- Primjeri: `_padez_uloge("Strana 1", "gen")` → `"Strane 1"`, `_padez_uloge("Kupac", "dat")` → `"Kupcu"`
- Ispravljen konkretan bug u `generatori/obiteljsko.py`: "koji glasi na Roditelja N"

### 3. UI opomene (`stranice/opomene.py`)
- `st.radio` zamijenjen s `doc_selectbox` za vrstu opomene (usklađeno s ostalim modulima)

### 4. Autoscroll (`LEGAL-SUITE.py`)
- Scroll na vrh radi u napredno modu (već radio) i sada i u **jednostavnom modu** pri promjeni odabira

### 5. ZZK upozorenje (`stranice/zemljisne.py`)
- Na formi "ZK Prijedlog (Uknjižba)" dodan `st.warning` s uputom o obvezi angažiranja odvjetnika/javnog bilježnika (čl. 109. ZZK, Zakon o javnom bilježništvu)

### 6. CZSS → ZAVOD ZA SOCIJALNI RAD
- `generatori/obiteljsko.py`: sva pojavljivanja → `<b>ZAVODOM ZA SOCIJALNI RAD</b>` (boldano u dokumentu)
- `stranice/obiteljsko.py`: sva pojavljivanja → "Zavod za socijalni rad" (u UI info/checkbox tekstovima)

---

## ŠTO NIJE NAPRAVLJENO (OSTAJE ZA SESIJU 12)

### PRIORITET 1 — Pregled strukture dokumenta za sve dokumente
Korisnik je rekao: *"Pregled strukture dokumenta iz prodaje poduzeća bi bio koristan i kod drugih"*

Trenutno `clause_builder` postoji samo za "Ugovor o prodaji poduzeća" (`stranice/trgovacko.py`).
Treba dodati **collapsible `st.expander("Pregled strukture dokumenta")`** kao read-only pregled
strukture (s popisom odjeljaka/članaka koji će se generirati) za:

| Dokument | Stranica | Generator |
|----------|----------|-----------|
| Bračni / predbračni ugovor | `stranice/obiteljsko.py` → `_render_bracni_ugovor()` | `generatori/obiteljsko.py` → `generiraj_bracni_ugovor()` |
| Plan o roditeljskoj skrbi | `stranice/obiteljsko.py` → `_render_roditeljska_skrb()` | `generatori/obiteljsko.py` → `generiraj_roditeljsku_skrb()` |
| Ugovor o uzdržavanju | `stranice/obiteljsko.py` → `_render_ugovor_uzdrzavanje()` | `generatori/obiteljsko.py` → `generiraj_ugovor_uzdrzavanje()` |
| Prijedlog za sporazumni razvod | `stranice/obiteljsko.py` → `_render_sporazum_razvod()` | `generatori/obiteljsko.py` → `generiraj_sporazum_razvod()` |
| Tužba za razvod | `stranice/obiteljsko.py` → `_render_tuzba_razvod()` | `generatori/obiteljsko.py` → `generiraj_tuzbu_razvod()` |
| Ugovor o darovanju | `stranice/obvezno.py` | `generatori/obvezno.py` → `generiraj_darovanje()` |
| Prijedlog za ovrhu | `stranice/ovrhe.py` | `generatori/ovrhe.py` → `generiraj_ovrhu_pro()` |
| Tužba | `stranice/tuzbe.py` | `generatori/tuzbe.py` → `generiraj_tuzbu_pro()` |

**Implementacijski uzorak** (kopirati s prodaje poduzeća):
```python
with st.expander("Pregled strukture dokumenta", expanded=False):
    st.markdown("""
    **Dokument će sadržavati:**
    - I. Uvod / stranke
    - II. Predmet
    - III. ...
    - Potpisi
    """)
```

Nije potreban dinamički clause_builder za ove — samo statički popis odjeljaka je dovoljan.

---

### PRIORITET 2 — Provjera i ažuriranje zakonskih članaka

Korisnik je zatražio: *"Provjeriti članke na koje se referira za ugovore itd"*

Sesija 11 to nije napravila. Treba sistematski proći kroz generatore i provjeriti jesu li
reference na zakone aktualne. Posebno provjeriti:

- `generatori/ugovori.py` — ZOO, ZR, ZN reference
- `generatori/obvezno.py` — ZOO čl. 479-498 (darovanje), cesija, jamstvo
- `generatori/obiteljsko.py` — Obiteljski zakon (NN 103/15, 98/19, 47/20, 49/23)
- `generatori/stecajno.py` — Stečajni zakon (NN 71/15, 104/17) + izmjene
- `generatori/kazneno.py` — Kazneni zakon (NN 125/11 + izmjene do 2023.)
- `generatori/upravno.py` — ZUP (NN 47/09 + izmjene), ZUS (NN 20/10 + izmjene)

**Kako provjeriti:** Usporediti reference u kodu s aktualnim popisom NN glasnika na zakon.hr

---

### PRIORITET 3 — Poboljšanje deklinacije (padezi)

Trenutna implementacija `_padez_uloge()` pokriva role-labele (Tužitelj, Kupac, Strana 1...).
Što još nedostaje:

1. **Osobna imena u koso padežima** — Implementirati `_padez_ime(ime_prezime, padez)` s osnovnim
   hrvatskim pravilima (muška/ženska prezimena, -a deklinacija za ženska imena)

2. **Mjesta u raznim padežima** — "u Zagrebu" (lok.), "prema Splitu" (dat.) — trenutno se mjesta
   uvijek umeću bez deklinacije

3. **Primjena u generatorima** — Identificirati sve `format_text(mjesto)` u generatorima gdje
   bi trebao biti lokativ i primijeniti deklinaciju

---

### PRIORITET 4 — napuni_primjerom na više stranica

Prema CLAUDE.md, `napuni_primjerom()` trenutno radi samo na:
- `stranice/tuzbe.py`
- `stranice/kazneno.py`
- `stranice/opomene.py`
- `stranice/upravno.py`

Treba dodati na:
- `stranice/ovrhe.py` — koristiti `PRIMJERI['ovrha']`
- `stranice/obiteljsko.py` — dodati primjer za razvod braka
- `stranice/ugovori.py` — primjer kupoprodajnog ugovora

---

## KAKO POKRENUTI APP LOKALNO

```bash
cd "C:\Users\Hrvoje Matej\Documents\APLIKACIJA"
streamlit run LEGAL-SUITE.py
# Otvori http://localhost:8501
```

## KAKO POKRENUTI TESTOVE

```bash
cd "C:\Users\Hrvoje Matej\Documents\APLIKACIJA"
python -m pytest tests/ -x -q
# Očekivano: 142 passed
```

## DEPLOY

Push na `main` branch → Streamlit Community Cloud auto-deploys.

---

## KLJUČNE DATOTEKE I GDJE ŠTO TRAŽITI

| Što tražiš | Gdje |
|------------|------|
| Utility funkcije (format_eur, iznos_slovima, padezi...) | `pomocne.py` |
| CSS stilovi | `config.py` |
| HTML→DOCX konverzija | `docx_export.py` |
| Generatori dokumenata | `generatori/*.py` |
| Streamlit forme (UI) | `stranice/*.py` |
| Entry point + navigacija | `LEGAL-SUITE.py` |
| Testovi | `tests/` |

## NAPOMENE ZA AI ASISTENTA

- **Nikad ne mijenjaj `formatiraj_troskovnik()`** da koristi `format_eur_s_rijecima` — tablice troškova trebaju samo broj, ne i slovima
- **Testovi provjeravaju `format_eur(1000) == "1.000,00 EUR"`** — ne mijenjaj potpis `format_eur()`
- **Sve stranice moraju imati `doc_selectbox` za odabir vrste** — ne koristiti `st.radio` za vrstu dokumenta
- **Kod u Pythonu, UI tekst na hrvatskom** (konvencija projekta)
- **Generator funkcije uvijek vraćaju HTML string**, ne modificiraju session_state
- **Uvijek pokreni testove prije git push-a**: `python -m pytest tests/ -x -q`
