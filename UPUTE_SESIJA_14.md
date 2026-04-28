# UPUTE ZA SESIJU 14 — LegalTech Suite Pro

> Napravljeno u sesiji 13 (2026-04-12). Stanje: 159 testova, svi prolaze.
> Git: `{{GITHUB_KORISNIK}}/LEGAL-SUITE` main branch, commit `be3b1ad`
> Deploy: `https://{{STREAMLIT_APP_ID}}.streamlit.app`

---

## ŠTO JE NAPRAVLJENO U SESIJI 13

### 1. Bug fixi (4 komada)
- **Scroll "Pokaži korake"** — `_scroll_to_element` koristi `scrollTo` umjesto `scrollIntoView`; prati `_vodic_odabir_prev` pa se scrolla samo kad se odabir upravo promijenio
- **Scroll na vrh pri promjeni doc_selectbox** — `doc_selectbox()` prati prethodnu vrijednost i zove `_scroll_na_vrh()` pri promjeni
- **OIB samo znamenke** — `_strip_nondigits` on_change callback na oba OIB polja u `unos_stranke()`
- **Fiksni primjer** — `napuni_primjerom()` koristi `copy.deepcopy(primjer)` umjesto `_randomiziraj_primjer()`; tekst gumba ažuriran

### 2. Ugovor o prodaji poduzeća — usklađivanje s predloškom
- Engleski termini → hrv: "Closing Inventory", "indemnityjem", "Cap odgovornosti", "Survival Period"
- ZOO ref za negativnu suglasnost: čl. 265 → čl. 2. i 17. (sloboda ugovaranja)
- Typo: "stječa" → "stječe"
- Odvojeni naslovi sekcija za kasne odjeljke (kao u ugovoru)
- `format_eur` → `format_eur_s_rijecima` za sve iznose u tijelu dokumenta

### 3. Defaulti na 0 u formi prodaje poduzeća
- Rok primopredaje, rok povjerljivosti, broj primjeraka — parametri s default=0, u dokumentu pokazuje `___`
- Rok plaćanja, zabrana kazna, gornja granica odgovornosti, ugovorna kazna — default 0
- Labeli: "Cap odgovornosti" → "Gornja granica odgovornosti", "Survival Period" → "Rok važenja jamstava"

### 4. format_eur → format_eur_s_rijecima globalno
- Svi iznosi u tijelu rečenica (ne u tablicama) sada imaju "(slovima: ...)" u: `ugovori.py`, `obvezno.py`, `stecajno.py`, `ovrhe.py`, `trgovacko.py` (NDA)

---

## PLAN ZA SESIJU 14

### PRIORITET 1 — napuni_primjerom na preostalim stranicama

Nedostaje na:
- `stranice/zalbe.py` → `PRIMJERI['zalba_presuda']` (ključevi: `z1_*`, `z2_*`)
- `stranice/punomoci.py` → `PRIMJERI['punomoc']` (ključevi: `pm_*`)
- `stranice/ugovori.py` → `_render_ugovor_o_radu()` → `PRIMJERI['ugovor_o_radu']`

**Napomena:** Prije dodavanja provjeriti da ključevi u `PRIMJERI` odgovaraju widget key-evima u formi.

---

### PRIORITET 2 — Lokativ gradova

Dodati statički rječnik u `pomocne.py`:
```python
_LOKATIV_GRADOVA = {
    'zagreb': 'Zagrebu', 'split': 'Splitu', 'rijeka': 'Rijeci',
    'osijek': 'Osijeku', 'zadar': 'Zadru', 'pula': 'Puli',
    'slavonski brod': 'Slavonskom Brodu', 'karlovac': 'Karlovcu',
    'varaždin': 'Varaždinu', 'šibenik': 'Šibeniku',
    'dubrovnik': 'Dubrovniku', 'sisak': 'Sisku',
    'velika gorica': 'Velikoj Gorici', 'petrinja': 'Petrinji',
    'koprivnica': 'Koprivnici', 'bjelovar': 'Bjelovaru',
    'vukovar': 'Vukovaru', 'vinkovci': 'Vinkovcima',
    'požega': 'Požegi', 'virovitica': 'Virovitici',
}

def lokativ_grada(grad: str) -> str:
    return _LOKATIV_GRADOVA.get(grad.lower().strip(), grad)
```

Primijeniti u generatorima gdje se pojavljuje "u {mjesto}" (tužbe, ovrhe, ugovori).

---

### PRIORITET 3 — Automatska lista Priloga

Za `generiraj_prodaju_poduzeca` — na kraju dokumenta generirati popis Priloga na temelju odabranih sekcija:

```python
# Mapping sekcija → prilog
_PRILOZI_PRODAJA = {
    'predmet': 'Izvještaj o dubinskom snimanju (due diligence)',
    'nekretnine': 'Clausula intabulandi / tabularni zahtjev',
    'poslovni_udjeli': 'Javnobilježnički akt o prijenosu poslovnih udjela',
    'pokretnine': 'Primopredajni zapisnik za pokretnine',
    'prezivjela_jamstva': 'Katalog preživjelih jamstava + Ugovor o fiduciji',
    'primopredaja': 'Zapisnik o primopredaji Poduzeća (sa Zapisnikom o zalihama)',
}
```

Prilog lista se generira samo za uključene sekcije, numerirana redoslijedom.

---

### PRIORITET 4 — Provjera zakonskih referenci (ostatak iz sesije 12)

- **Stečajni zakon**: App ima `NN 71/15, 104/17` — provjeriti izmjene
- **Obiteljski zakon**: App ima `NN 103/15, 98/19, 47/20, 49/23` — provjeriti
- **ZOO**: App ima `NN 35/05, 41/08, 125/11, 78/15, 29/18, 126/21, 114/22, 156/22`
- **OZ** (Ovršni zakon): `NN 112/12, 25/13, 93/14, 55/16, 73/17, 131/20`

Lokacija FAKS zakona: `C:\Users\{{WIN_USER}}\Documents\faks\TRGOVAČKO\VJEZBE - TRG\zakoni\`

---

### PRIORITET 5 — Pregled strukture dokumenta (preostale forme)

Sesija 12 je dodala na 8 formi. Još nije dodano na:
- `stranice/ugovori.py` → `_render_ugovor_o_radu()`, `_render_najam()`
- `stranice/zalbe.py`
- `stranice/punomoci.py`
- `stranice/kazneno.py` (tabs — provjeriti koje tab forme nemaju)

---

## NAPOMENE ZA AI ASISTENTA

- `_strip_nondigits(key, max_len)` je u `pomocne.py` — koristiti za nova numerička polja
- `_scroll_na_vrh()` je u `pomocne.py` — koristiti gdje treba scroll nakon akcije
- `_padez_ime()` je implementiran ali još NIJE primijenjen u generatorima (PRIORITET iz sesije 12!)
- `format_eur_s_rijecima` → koristiti u tijelu dokumenata; `format_eur` → tablice i labele
- **NIKAD** ne mijenjaj `formatiraj_troskovnik()` ni `format_eur()` potpis
- Testovi: `python -m pytest tests/ -x -q` — mora biti 159 passed
- Deploy: push na main → auto-deploy; reboot na Streamlit Cloud dashboardu ako treba
