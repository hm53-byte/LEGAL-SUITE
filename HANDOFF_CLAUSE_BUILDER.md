# HANDOFF: Clause Builder Feature

> **Sesija:** Sljedeća nakon Session 10
> **Prioritet:** Srednji — nova UI funkcionalnost za sve generatore
> **Procjena:** 1 sesija, bez novih ovisnosti

---

## Što treba napraviti

Dodati sustav za **dinamično upravljanje odjeljcima dokumenta** — korisnik checkboxima bira koje klauzule/odjeljke želi u dokumentu, a strelicama ↑↓ mijenja njihov redoslijed. Generator tada generira samo odabrane odjeljke, u odabranom redoslijedu.

### Izgled u UI-u (Streamlit)

```
Odabir i redoslijed odjeljaka:
─────────────────────────────────────────────
[x] I.   Predmet ugovora                  —
[x] II.  Kupoprodajna cijena              ↑ ↓
[x] III. Imovina — Nekretnine             ↑ ↓
[ ] III. Imovina — Tražbine (cesija)      —
[x] III. Imovina — Pokretnine             ↑ ↓
[ ] IV.  Preuzete obveze                  —
[x] V.   Prijenos radnih odnosa           ↑ ↓
[ ] VI.  Tekući ugovori                   —
[ ] VII. Zabrana natjecanja               —
[x] VIII.Izjave i jamstva                 ↑ ↓
[x] IX.  Porezne odredbe                  ↑ ↓
[x] X.   Primopredaja                     ↑ ↓
[x] XI.  Ugovorna kazna                   ↑ ↓
[x] XII. Završne odredbe                  —  ← uvijek zadnji, nema ↓
─────────────────────────────────────────────
```

- Checkbox = uključi/isključi odjeljak u generiranom dokumentu
- ↑↓ = pomakni odjeljak gore/dolje u redoslijedu
- Neki odjeljci su **obavezni** (predmet, završne odredbe) — checkbox disabled, uvijek uključeni
- Neki su **uvijek na fiksnoj poziciji** (završne odredbe uvijek zadnje)

---

## Arhitektura — kako implementirati

### Korak 1: Definirati `SEKCIJE` strukturu za svaki dokument

Svaki generator dobiva rječnik koji opisuje svoje odjeljke. Primjer za `prodaju_poduzeca`:

```python
# Na vrhu generatori/trgovacko.py ili u zasebnoj datoteci sekcije.py

SEKCIJE_PRODAJA_PODUZECA = [
    {
        "id": "predmet",
        "naziv": "Predmet ugovora",
        "obavezno": True,
        "ukljuceno": True,
    },
    {
        "id": "cijena",
        "naziv": "Kupoprodajna cijena i plaćanje",
        "obavezno": True,
        "ukljuceno": True,
    },
    {
        "id": "nekretnine",
        "naziv": "Imovina — Nekretnine",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "trabine",
        "naziv": "Imovina — Tražbine (cesija)",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "mjenice",
        "naziv": "Imovina — Mjenice",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "poslovni_udjeli",
        "naziv": "Imovina — Poslovni udjeli",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "pokretnine",
        "naziv": "Imovina — Pokretnine",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "vrijednosni_papiri",
        "naziv": "Imovina — Vrijednosni papiri",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "novcana_sredstva",
        "naziv": "Imovina — Novčana sredstva",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "preuzete_obveze",
        "naziv": "Preuzete obveze",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "radni_odnosi",
        "naziv": "Prijenos ugovora o radu",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "tekuci_ugovori",
        "naziv": "Prijenos tekućih ugovora",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "zabrana_natjecanja",
        "naziv": "Zabrana natjecanja (Non-Compete)",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "prezivjela_jamstva",
        "naziv": "Preživjela jamstva",
        "obavezno": False,
        "ukljuceno": False,
    },
    {
        "id": "izjave_jamstva",
        "naziv": "Izjave i jamstva",
        "obavezno": True,
        "ukljuceno": True,
    },
    {
        "id": "porezne_odredbe",
        "naziv": "Porezne odredbe",
        "obavezno": False,
        "ukljuceno": True,
    },
    {
        "id": "primopredaja",
        "naziv": "Primopredaja poduzeća",
        "obavezno": True,
        "ukljuceno": True,
    },
    {
        "id": "nedostaci",
        "naziv": "Odgovornost za nedostatke",
        "obavezno": False,
        "ukljuceno": True,
    },
    {
        "id": "ugovorna_kazna",
        "naziv": "Ugovorna kazna",
        "obavezno": False,
        "ukljuceno": True,
    },
    {
        "id": "povjerljivost",
        "naziv": "Povjerljivost",
        "obavezno": False,
        "ukljuceno": True,
    },
    {
        "id": "sporovi",
        "naziv": "Rješavanje sporova",
        "obavezno": True,
        "ukljuceno": True,
    },
    {
        "id": "zavrsne",
        "naziv": "Završne odredbe",
        "obavezno": True,
        "ukljuceno": True,
        "fiksna_pozicija": "zadnja",  # uvijek ostaje zadnja
    },
]
```

### Korak 2: Helper funkcija za UI (u pomocne.py)

```python
def clause_builder(kljuc_sesije: str, sekcije_default: list) -> list:
    """
    Prikazuje UI za odabir i redoslijed odjeljaka dokumenta.
    Vraća listu ID-ova odjeljaka u odabranom redoslijedu (samo ukljuceni).
    
    kljuc_sesije: prefiks za session_state (npr. "pp_sekcije")
    sekcije_default: lista dicts s id, naziv, obavezno, ukljuceno
    """
    import streamlit as st
    import copy

    # Inicijalizacija session_state
    if kljuc_sesije not in st.session_state:
        st.session_state[kljuc_sesije] = copy.deepcopy(sekcije_default)

    sekcije = st.session_state[kljuc_sesije]
    
    # Odvoji fiksne od slobodnih
    fiksne_zadnje = [s for s in sekcije if s.get("fiksna_pozicija") == "zadnja"]
    slobodne = [s for s in sekcije if s.get("fiksna_pozicija") != "zadnja"]

    st.caption("Odaberite odjeljke i podesite redoslijed:")

    for i, sek in enumerate(slobodne):
        col_check, col_naziv, col_gore, col_dole = st.columns([0.5, 5, 0.5, 0.5])
        
        with col_check:
            if sek["obavezno"]:
                st.checkbox("", value=True, disabled=True, key=f"{kljuc_sesije}_chk_{sek['id']}")
            else:
                novo = st.checkbox("", value=sek["ukljuceno"], key=f"{kljuc_sesije}_chk_{sek['id']}")
                if novo != sek["ukljuceno"]:
                    st.session_state[kljuc_sesije][i]["ukljuceno"] = novo
                    st.rerun()
        
        with col_naziv:
            prefix = "**" if sek["ukljuceno"] else ""
            suffix = "**" if sek["ukljuceno"] else ""
            st.markdown(f"{prefix}{sek['naziv']}{suffix}")
        
        with col_gore:
            if i > 0 and st.button("↑", key=f"{kljuc_sesije}_gore_{i}"):
                slobodne[i], slobodne[i-1] = slobodne[i-1], slobodne[i]
                st.session_state[kljuc_sesije] = slobodne + fiksne_zadnje
                st.rerun()
        
        with col_dole:
            if i < len(slobodne) - 1 and st.button("↓", key=f"{kljuc_sesije}_dole_{i}"):
                slobodne[i], slobodne[i+1] = slobodne[i+1], slobodne[i]
                st.session_state[kljuc_sesije] = slobodne + fiksne_zadnje
                st.rerun()

    # Prikaži fiksne zadnje (disabled)
    for sek in fiksne_zadnje:
        col_check, col_naziv, _, _ = st.columns([0.5, 5, 0.5, 0.5])
        with col_check:
            st.checkbox("", value=True, disabled=True, key=f"{kljuc_sesije}_chk_{sek['id']}")
        with col_naziv:
            st.markdown(f"**{sek['naziv']}**")

    # Vrati listu ukljucenih ID-ova u redoslijedu
    return [s["id"] for s in (slobodne + fiksne_zadnje) if s["ukljuceno"]]
```

### Korak 3: Refaktorirati generator da prihvaća `sekcije_redoslijed`

Trenutni generator `generiraj_prodaju_poduzeca` gradi HTML u fiksnom redoslijedu unutar funkcije. Treba ga refaktorirati da svaki odjeljak bude zasebna funkcija, a zatim ih pozivati prema listi:

```python
# Svaki odjeljak postaje privatna funkcija koja vraća HTML string

def _sec_predmet(podaci, clanak_ref):
    # ... returns html string, incrementira clanak_ref[0]
    pass

def _sec_cijena(podaci, clanak_ref):
    pass

# itd.

# Dispatcher
_SEKCIJE_FN = {
    "predmet": _sec_predmet,
    "cijena": _sec_cijena,
    "nekretnine": _sec_nekretnine,
    # ...
}

def generiraj_prodaju_poduzeca(prodavatelj, kupac, podaci, sekcije_redoslijed=None):
    if sekcije_redoslijed is None:
        # defaultni redoslijed = svi obavezni + svi ukljuceni po defaultu
        sekcije_redoslijed = [s["id"] for s in SEKCIJE_PRODAJA_PODUZECA if s["ukljuceno"]]
    
    clanak_ref = [1]  # mutable ref za auto-numeraciju
    parts = [header_html]
    
    for sek_id in sekcije_redoslijed:
        fn = _SEKCIJE_FN.get(sek_id)
        if fn:
            parts.append(fn(podaci, clanak_ref))
    
    parts.append(footer_html)
    return "".join(parts)
```

### Korak 4: Integracija u stranicu

```python
# U stranice/trgovacko.py, _render_prodaja_poduzeca():

from pomocne import clause_builder
from generatori.trgovacko import SEKCIJE_PRODAJA_PODUZECA

# ... (unos stranaka, podaci o cijeni itd.) ...

st.subheader("Struktura dokumenta")
with st.expander("Odaberi i poredaj odjeljke", expanded=False):
    odabrane_sekcije = clause_builder("pp_sekcije", SEKCIJE_PRODAJA_PODUZECA)

if st.button("Generiraj", type="primary"):
    doc = generiraj_prodaju_poduzeca(
        prodavatelj, kupac, podaci,
        sekcije_redoslijed=odabrane_sekcije
    )
    prikazi_dokument(doc, "Prodaja_poduzeca.docx", "Preuzmi")
```

---

## Redoslijed implementacije (po prioritetu)

### Faza A — samo za `prodaju_poduzeca` (pilot)
1. Refaktorirati `generiraj_prodaju_poduzeca` na `_sec_*` podfunkcije
2. Dodati `SEKCIJE_PRODAJA_PODUZECA` listu
3. Implementirati `clause_builder()` u `pomocne.py`
4. Integrirati u `stranice/trgovacko.py`
5. Testirati

### Faza B — ostali dokumenti (ako Faza A prođe dobro)
Dokumenti koji bi imali najviše koristi (jer imaju mnogo opcionalnih odjeljaka):
- `ugovori.py` — kupoprodajni, najam, ugovor o djelu
- `obvezno.py` — složeniji ugovori
- `ovrhe.py` — razne vrste ovrha

Dokumenti koji **ne trebaju** clause builder (jednostavni, malo odjeljaka):
- opomene, punomoci, zapisnici

---

## Što NE raditi

- **Nemoj** koristiti drag & drop JS biblioteke — preteško za integrirati u Streamlit
- **Nemoj** raditi fiksni side panel — nije moguće u Streamlitu bez hakiranja CSS-a
- **Nemoj** migrirati s Streamlita — preveliki rewrite bez jasnog dobitka
- **Nemoj** raditi Fazu B dok Faza A nije testirana i stabilna

---

## Testovi koji treba dodati

```python
# tests/test_clause_builder.py

def test_sve_sekcije_imaju_id():
    for sek in SEKCIJE_PRODAJA_PODUZECA:
        assert "id" in sek
        assert "obavezno" in sek

def test_generator_s_praznim_redoslijedom():
    # Samo obavezni odjeljci
    html = generiraj_prodaju_poduzeca("A", "B", {}, sekcije_redoslijed=["predmet", "zavrsne"])
    assert "PREDMET UGOVORA" in html
    assert "Završne odredbe" in html
    assert "Imovina" not in html

def test_generator_s_custom_redoslijedom():
    # Zabrana natjecanja ispred izjava i jamstava
    html = generiraj_prodaju_poduzeca("A", "B", 
        {"zabrana_natjecanja": True},
        sekcije_redoslijed=["predmet", "cijena", "zabrana_natjecanja", "izjave_jamstva", "zavrsne"]
    )
    pos_zabrana = html.find("NON-COMPETE")
    pos_izjave = html.find("IZJAVE I JAMSTVA")
    assert pos_zabrana < pos_izjave
```

---

## Trenutno stanje koda (za referencu)

- `generatori/trgovacko.py` — `generiraj_prodaju_poduzeca()` postoji, gradi HTML sekvencijalno u jednoj funkciji (~400 linija). **Treba refaktorirati na _sec_ podfunkcije.**
- `stranice/trgovacko.py` — `_render_prodaja_poduzeca()` postoji, ima expander grupe za imovinu.
- `pomocne.py` — `clause_builder()` **ne postoji još**, treba dodati.
- Svi testovi su u `tests/` direktoriju, pokreću se s `python -m pytest tests/ -x -q`.

---

## Napomena o članku ZOO

U prethodnoj sesiji ispravljeno:
- Preuzimanje duga: ~~čl. 446–450~~ → **čl. 96–100 ZOO**
- Skupštinska suglasnost: ~~čl. 275~~ → **čl. 301.a ZTD**
