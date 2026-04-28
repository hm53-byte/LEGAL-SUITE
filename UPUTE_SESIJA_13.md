# UPUTE ZA SESIJU 13 — LegalTech Suite Pro

> Napravljeno u sesiji 12 (2026-04-12). Stanje: 159 testova, svi prolaze.
> Git: `{{GITHUB_KORISNIK}}/LEGAL-SUITE` main branch, commit `778d165`
> Deploy: `https://{{STREAMLIT_APP_ID}}.streamlit.app`

---

## ŠTO JE NAPRAVLJENO U SESIJI 12

### 1. Pregled strukture dokumenta (8 formi)
`st.expander("Pregled strukture dokumenta", expanded=False)` dodan na:
- `stranice/obiteljsko.py`: sporazumni razvod, tužba za razvod, bračni ugovor, roditeljska skrb, ugovor o uzdržavanju
- `stranice/obvezno.py`: ugovor o darovanju
- `stranice/ovrhe.py`: prijedlog za ovrhu (vjerodostojna isprava)
- `stranice/tuzbe.py`: tužba (parnični postupak)

### 2. Ažurirane zakonske reference
- `generatori/upravno.py`: ZUP `NN 47/09, 110/21` → `NN 47/09, 110/21, 104/25` (pročišćeni tekst zakon.hr 24.10.2025)
- `generatori/upravno.py`: ZUS dodana izmjena `NN 36/24` i pročišćeni tekst `NN 104/25`
- `generatori/upravno.py`: ZPPI → `NN 25/13, 85/15, 69/22, 104/25`
- `generatori/kazneno.py`: dodan header komentar s punim popisom NN izmjena za KZ (do `NN 36/24`) i ZKP

### 3. Deklinacija osobnih imena (`pomocne.py`)
- Dodan `_deklinaj_token_ime(token, idx)` — privatna helper funkcija
- Dodana `_padez_ime(ime_prezime, padez)` — javna funkcija za deklinaciju punog imena
- Pokriva: -ić prezimena, -a pattern (Ana, Marija, Luka, Nikola, Siniša), -o pattern (Marko, Bruno), suglasnik (Ivan, Horvat)
- Iznimka: `Petar → Petra` (nepostojano a)
- 11 novih testova u `TestPadezIme`

### 4. napuni_primjerom na više stranica
- `stranice/ovrhe.py` — `_render_prijedlog_ovrhe()` sada poziva `napuni_primjerom('ovrha', '')`
- `stranice/obiteljsko.py` — `_render_sporazum_razvod()` poziva `napuni_primjerom('obiteljsko_razvod', '')`
- `stranice/ugovori.py` — `_render_gradjansko_pravo()` poziva `napuni_primjerom('ugovor_kupoprodaja', '')` samo kada je odabrana Kupoprodaja
- ISPRAVKA: `PRIMJERI['obiteljsko_razvod']` ažuriran s ispravnim ključevima: `sr_p1_*`, `sr_p2_*` (prethodno koristio `ob1_*`, `ob2_*` koji ne odgovaraju formi)

---

## ŠTO NIJE NAPRAVLJENO (OSTAJE ZA SESIJU 13)

### PRIORITET 1 — Primjena _padez_ime() u generatorima

Funkcija `_padez_ime()` je implementirana ali nije primijenjena nigdje u generatorima.
Treba identificirati mjesta gdje bi koristila:

1. `generatori/obiteljsko.py` — traženje po tekstu: mjesta gdje se koristi ime stranke
   u kosim padežima (genitiv, dativ). Npr. rečenice koje govore "obveze [Ime] po ovom ugovoru"
2. `generatori/obvezno.py` — darovanje: "Darovatelj [Ime] daruje Obdareniku [Ime]..."
3. Ostali generatori gdje se ime pojavljuje u oblom padežu

**Napomena:** Funkcija je konzervativna (bolje nominativ nego pogrešan padež).
Koristiti samo tamo gdje je genitiv/dativ 100% siguran.

---

### PRIORITET 2 — Provjera preostalih zakonskih referenci

Provjere iz sesije 12 su pokrile ZUP, ZUS, ZPPI, KZ, ZKP.
Preostaje provjera:

- **Stečajni zakon**: App ima `NN 71/15, 104/17` — vjerojatno ima novijih izmjena
  (Pretražiti u FAKS materijalima ili online)
- **Obiteljski zakon**: App ima `NN 103/15, 98/19, 47/20, 49/23` — provjeri je li aktualno
- **ZOO** (u obvezno.py): App ima `NN 35/05, 41/08, 125/11, 78/15, 29/18, 126/21, 114/22, 156/22`
  — provjeri s aktualnim pročišćenim tekstom na zakon.hr
- **OZ** (Ovršni zakon, ovrhe.py): `NN 112/12, 25/13, 93/14, 55/16, 73/17, 131/20` — provjeri izmjene

---

### PRIORITET 3 — napuni_primjerom na preostalim stranicama

Još nije dodano na:
- `stranice/ugovori.py` → `_render_ugovor_o_radu()` — koristiti `PRIMJERI['ugovor_o_radu']`
- `stranice/zalbe.py` — koristiti `PRIMJERI['zalba_presuda']`
- `stranice/punomoci.py` — koristiti `PRIMJERI['punomoc']`

---

### PRIORITET 4 — Mjesta u raznim padežima (lokativ)

Lokativ za gradove: "u Zagrebu", "prema Splitu", "iz Rijeke".
Trenutno se mjesta uvijek umeću u nominativu.

Opcija A: Statičan rječnik za 20 najčešćih gradova:
```python
_LOKATIV_GRADOVA = {
    'zagreb': 'Zagrebu', 'split': 'Splitu', 'rijeka': 'Rijeci',
    'osijek': 'Osijeku', 'zadar': 'Zadru', ...
}
```

Opcija B: Preskočiti (premalo dobiti za kompleksnost).

Preporučujem Opciju A — ograničen scope, visoka korisnost.

---

## KAKO POKRENUTI APP LOKALNO

```bash
cd "C:\Users\{{WIN_USER}}\Documents\APLIKACIJA"
streamlit run LEGAL-SUITE.py
# Otvori http://localhost:8501
```

## KAKO POKRENUTI TESTOVE

```bash
cd "C:\Users\{{WIN_USER}}\Documents\APLIKACIJA"
python -m pytest tests/ -x -q
# Očekivano: 159 passed
```

## DEPLOY

Push na `main` branch → Streamlit Community Cloud auto-deploys.

---

## NAPOMENE ZA AI ASISTENTA

- `_padez_ime()` je u `pomocne.py` — može se importati gdje treba
- `_padez_uloge()` već postoji i radi za pravne oznake (Tužitelj, Kupac, itd.)
- **NIKAD** ne mijenjaj `formatiraj_troskovnik()` da koristi `format_eur_s_rijecima`
- **Testovi provjeravaju `format_eur(1000) == "1.000,00 EUR"`** — ne mijenjaj potpis
- Sve stranice moraju imati `doc_selectbox` za odabir vrste — ne `st.radio`
- Generator funkcije uvijek vraćaju HTML string, ne modificiraju session_state
- Uvijek pokreni testove prije git push-a: `python -m pytest tests/ -x -q`
