# -----------------------------------------------------------------------------
# POMOCNE FUNKCIJE: escape, formatiranje, validacija, Word export, UI komponente
# -----------------------------------------------------------------------------
import html as _html_module
import streamlit as st
from datetime import date
from docx_export import pripremi_za_docx
from sudovi import (
    OPCINSKI_SUDOVI, TRGOVACKI_SUDOVI, ZUPANIJSKI_SUDOVI, UPRAVNI_SUDOVI,
    SVI_SUDOVI, dohvati_adresu_suda, format_sud_s_dijakriticima,
)


# --- Privatni helperi ---

def _escape(text):
    """Escapea HTML entitete u korisnickom unosu."""
    if not text:
        return ""
    return _html_module.escape(str(text))


def _strip_nondigits(key, max_len=None):
    """on_change callback — uklanja sve znakove koji nisu znamenke iz session_state[key]."""
    val = st.session_state.get(key, "")
    if val:
        cleaned = "".join(c for c in str(val) if c.isdigit())
        if max_len:
            cleaned = cleaned[:max_len]
        if cleaned != val:
            st.session_state[key] = cleaned


def _scroll_na_vrh():
    """Injektira JS koji scrolla main container na vrh stranice."""
    import streamlit.components.v1 as _comp
    import time
    _comp.html(
        f"<script>setTimeout(function(){{"
        f"var el=parent.document.querySelector('section.main');"
        f"if(el)el.scrollTo({{top:0,behavior:'smooth'}});"
        f"}},80);</script><!-- {time.time_ns()} -->",
        height=0,
    )


def _validiraj_oib(oib_str):
    """Provjerava OIB prema ISO 7064 mod-11-10 algoritmu.
    Vraca: (bool, str) - (ispravnost, poruka greske ili prazan string)
    """
    if not oib_str:
        return False, ""
    oib_str = oib_str.strip()
    if len(oib_str) != 11 or not oib_str.isdigit():
        return False, "OIB mora sadržavati točno 11 znamenki."
    # ISO 7064 mod-11-10 checksum
    carry = 10
    for digit_char in oib_str[:10]:
        carry = (carry + int(digit_char)) % 10
        if carry == 0:
            carry = 10
        carry = (carry * 2) % 11
    kontrolna = (11 - carry) % 10
    if kontrolna != int(oib_str[10]):
        return False, "OIB nije ispravan (kontrolna znamenka ne odgovara)."
    return True, ""


def _rimski_broj(n):
    """Pretvara pozitivan integer u rimski broj (bez ogranicenja)."""
    if n <= 0:
        return str(n)
    vrijednosti = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    rezultat = []
    for vrijednost, simbol in vrijednosti:
        while n >= vrijednost:
            rezultat.append(simbol)
            n -= vrijednost
    return "".join(rezultat)


def format_eur(iznos):
    """Formatira iznos u hrvatskom formatu: 10.000,00 EUR"""
    if iznos is None:
        return "0,00 EUR"
    try:
        iznos = float(iznos)
    except (ValueError, TypeError):
        return "0,00 EUR"
    # Formatira s 2 decimale i hrvatskim separatorima
    formatted = f"{iznos:,.2f}"
    # Zamijeni: 10,000.00 -> 10.000,00
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{formatted} EUR"


# =============================================================================
# PRETVORBA IZNOSA U RIJECI (SLOVIMA) — za pravne dokumente
# =============================================================================

def _broj_rijecima_hr(n):
    """Pretvara nenegativan cijeli broj u hrvatske rijeci (nominativ)."""
    if n < 0:
        return f"minus {_broj_rijecima_hr(-n)}"
    if n == 0:
        return "nula"

    JED = [
        "", "jedan", "dva", "tri", "četiri", "pet", "šest", "sedam", "osam", "devet",
        "deset", "jedanaest", "dvanaest", "trinaest", "četrnaest", "petnaest",
        "šesnaest", "sedamnaest", "osamnaest", "devetnaest",
    ]
    DESECI = ["", "", "dvadeset", "trideset", "četrdeset", "pedeset",
              "šezdeset", "sedamdeset", "osamdeset", "devedeset"]
    STOTICE = ["", "sto", "dvjesto", "tristo", "četiristo", "petsto",
               "šeststo", "sedamsto", "osamsto", "devetsto"]

    def _ispod_tisucu(m):
        if m == 0:
            return ""
        if m < 20:
            return JED[m]
        if m < 100:
            d, j = divmod(m, 10)
            return DESECI[d] + (" i " + JED[j] if j else "")
        s, ostatak = divmod(m, 100)
        return STOTICE[s] + (" " + _ispod_tisucu(ostatak) if ostatak else "")

    parts = []

    # Milijarde
    if n >= 1_000_000_000:
        mlrd, n = divmod(n, 1_000_000_000)
        if mlrd == 1:
            parts.append("jedna milijarda")
        elif mlrd == 2:
            parts.append("dvije milijarde")
        elif 3 <= mlrd <= 4:
            parts.append(f"{_broj_rijecima_hr(mlrd)} milijarde")
        else:
            parts.append(f"{_broj_rijecima_hr(mlrd)} milijardi")

    # Milijuni
    if n >= 1_000_000:
        mil, n = divmod(n, 1_000_000)
        if mil == 1:
            parts.append("jedan milijun")
        elif mil == 2:
            parts.append("dva milijuna")
        elif 3 <= mil <= 4:
            parts.append(f"{_broj_rijecima_hr(mil)} milijuna")
        else:
            parts.append(f"{_broj_rijecima_hr(mil)} milijuna")

    # Tisuce
    if n >= 1000:
        tis, n = divmod(n, 1000)
        if tis == 1:
            parts.append("tisuću")
        elif tis == 2:
            parts.append("dvije tisuće")
        elif 3 <= tis <= 4:
            parts.append(f"{_ispod_tisucu(tis)} tisuće")
        else:
            parts.append(f"{_ispod_tisucu(tis)} tisuća")

    # Ostatak (< 1000)
    if n > 0:
        parts.append(_ispod_tisucu(n))

    return " ".join(p for p in parts if p)


def iznos_slovima(iznos):
    """Pretvara iznos EUR u hrvatske rijeci.
    Npr: 1500.50 -> "tisuću petsto eura i 50/100"
         100.00  -> "sto eura"
    """
    try:
        iznos = float(iznos)
        if iznos < 0:
            return f"minus {iznos_slovima(-iznos)}"
        euri = int(iznos)
        centi = round((iznos - euri) * 100)
        if euri == 0 and centi == 0:
            return "nula eura"
        euri_str = _broj_rijecima_hr(euri) if euri > 0 else ""
        if centi > 0:
            if euri > 0:
                return f"{euri_str} eura i {centi:02d}/100"
            return f"nula eura i {centi:02d}/100"
        return f"{euri_str} eura"
    except Exception:
        return ""


def format_eur_s_rijecima(iznos):
    """Formatira iznos s rijecima u zagradama.
    Npr: 1500.50 -> "1.500,50 EUR (slovima: tisucu petsto eura i 50/100)"
    Koristi se u tijelu pravnih dokumenata (ne u tablicama troškova).
    """
    formatted = format_eur(iznos)
    rijecima = iznos_slovima(iznos)
    if rijecima:
        return f"{formatted} (slovima: {rijecima})"
    return formatted


# =============================================================================
# PADEZI — DEKLINACIJA PRAVNIH OZNAKA ULOGA
# =============================================================================

# Lookup: nominativ -> (genitiv, dativ, akuzativ, instrumental, lokativ)
_PADEZI_ULOGA = {
    "Stranka":        ("Stranke",        "Stranci",        "Stranku",        "Strankom",        "Stranci"),
    "Strana":         ("Strane",         "Strani",         "Stranu",         "Stranom",         "Strani"),
    "Tužitelj":       ("Tužitelja",      "Tužitelju",      "Tužitelja",      "Tužiteljem",      "Tužitelju"),
    "Tužiteljica":    ("Tužiteljice",    "Tužiteljici",    "Tužiteljicu",    "Tužiteljicom",    "Tužiteljici"),
    "Tuženik":        ("Tuženika",       "Tuženiku",       "Tuženika",       "Tuženikom",       "Tuženiku"),
    "Tužena":         ("Tužene",         "Tuženoj",        "Tuženu",         "Tuženom",         "Tuženoj"),
    "Vjerovnik":      ("Vjerovnika",     "Vjerovniku",     "Vjerovnika",     "Vjerovnikom",     "Vjerovniku"),
    "Dužnik":         ("Dužnika",        "Dužniku",        "Dužnika",        "Dužnikom",        "Dužniku"),
    "Prodavatelj":    ("Prodavatelja",   "Prodavatelju",   "Prodavatelja",   "Prodavateljem",   "Prodavatelju"),
    "Kupac":          ("Kupca",          "Kupcu",          "Kupca",          "Kupcem",          "Kupcu"),
    "Roditelj":       ("Roditelja",      "Roditelju",      "Roditelja",      "Roditeljem",      "Roditelju"),
    "Predlagatelj":   ("Predlagatelja",  "Predlagatelju",  "Predlagatelja",  "Predlagateljem",  "Predlagatelju"),
    "Protustranka":   ("Protustranke",   "Protustranci",   "Protustranku",   "Protustrankam",   "Protustranci"),
    "Obveznik":       ("Obveznika",      "Obvezniku",      "Obveznika",      "Obveznikom",      "Obvezniku"),
    "Primatelj":      ("Primatelja",     "Primatelju",     "Primatelja",     "Primateljem",     "Primatelju"),
    "Ovrhovoditelj":  ("Ovrhovoditelja", "Ovrhovoditelju", "Ovrhovoditelja", "Ovrhovoditeljem", "Ovrhovoditelju"),
    "Ovršenik":       ("Ovršenika",      "Ovršeniku",      "Ovršenika",      "Ovršenikom",      "Ovršeniku"),
    "Posloprimac":    ("Posloprimca",    "Posloprimcu",    "Posloprimca",    "Posloprimcem",    "Posloprimcu"),
    "Poslodavac":     ("Poslodavca",     "Poslodavcu",     "Poslodavca",     "Poslodavcem",     "Poslodavcu"),
    "Davatelj":       ("Davatelja",      "Davatelju",      "Davatelja",      "Davateljem",      "Davatelju"),
    "Jamac":          ("Jamca",          "Jamcu",          "Jamca",          "Jamcem",          "Jamcu"),
    "Zajmodavac":     ("Zajmodavca",     "Zajmodavcu",     "Zajmodavca",     "Zajmodavcem",     "Zajmodavcu"),
    "Zajmoprimac":    ("Zajmoprimca",    "Zajmoprimcu",    "Zajmoprimca",    "Zajmoprimcem",    "Zajmoprimcu"),
    "Darovatelj":     ("Darovatelja",    "Darovatelju",    "Darovatelja",    "Darovateljem",    "Darovatelju"),
    "Obdarenik":      ("Obdarenika",     "Obdareniku",     "Obdarenika",     "Obdarenikom",     "Obdareniku"),
    "Posrednik":      ("Posrednika",     "Posredniku",     "Posrednika",     "Posrednikom",     "Posredniku"),
    "Najmodavac":     ("Najmodavca",     "Najmodavcu",     "Najmodavca",     "Najmodavcem",     "Najmodavcu"),
    "Najmoprimac":    ("Najmoprimca",    "Najmoprimcu",    "Najmoprimca",    "Najmoprimcem",    "Najmoprimcu"),
}

_PADEZ_IDX = {"nom": -1, "gen": 0, "dat": 1, "akuz": 2, "instr": 3, "lok": 4}


def _padez_uloge(uloga, padez="gen"):
    """Deklinira oznaku uloge u trazeni padez.
    uloga: npr. 'Strana 1', 'Roditelj 2', 'Kupac'
    padez: 'nom'|'gen'|'dat'|'akuz'|'instr'|'lok'
    Vraca dekliniranu ulogu, ili uloga nepromijenjena ako nije u tablici.
    """
    if not uloga:
        return uloga
    idx = _PADEZ_IDX.get(padez, 0)
    if idx == -1:
        return uloga  # nominativ — vrati neizmijenjeno

    # Odvoji broj od uloge (npr. "Strana 1" → base="Strana", suffix=" 1")
    dijelovi = uloga.strip().split()
    if len(dijelovi) > 1 and dijelovi[-1].isdigit():
        base = " ".join(dijelovi[:-1])
        br_suffix = " " + dijelovi[-1]
    else:
        base = uloga.strip()
        br_suffix = ""

    if base in _PADEZI_ULOGA:
        return _PADEZI_ULOGA[base][idx] + br_suffix

    return uloga  # fallback: nepromijenjena


# PADEZI — DEKLINACIJA OSOBNIH IMENA
# =============================================================================

# Osnova za "nepostojano a" u imenima: petar → petr (gen: petra)
_NEPOSTOJANO_A_IME = {
    "petar": "petr",
    "nikola": None,  # završava na -a, poseban slucaj — vec obradjeno kao -a pattern
}

# Nastavci za padeze u obliku (gen, dat, akuz, instr, lok)
_PADEZ_IDX_IME = {"nom": -1, "gen": 0, "dat": 1, "akuz": 2, "instr": 3, "lok": 4}


def _deklinaj_token_ime(token, idx):
    """
    Deklinira jedan token (ime ili prezime) prema zadanom indeksu padeza.
    idx: 0=gen, 1=dat, 2=akuz, 3=instr, 4=lok
    Vraca originalni token ako pravilo nije primjenjivo.
    """
    if not token or len(token) < 2:
        return token

    t = token
    tl = t.lower()

    # Prezimena/imena na -ić (muška deklinacija: Babić → Babića, Babiću...)
    if tl.endswith("ić"):
        sufixes = ("ića", "iću", "ića", "ićem", "iću")
        return t[:-2] + sufixes[idx]

    # ASCII fallback na -ic (bez dijakritike)
    if tl.endswith("ic") and len(tl) > 3:
        sufixes = ("ica", "icu", "ica", "icem", "icu")
        return t[:-2] + sufixes[idx]

    # Nepostojano 'a' — iznimka za "Petar" → osnova "Petr"
    nepost = _NEPOSTOJANO_A_IME.get(tl)
    if nepost is not None:
        # Rekonstruiraj s originalnim velikim slovom
        base = t[0] + nepost[1:]  # sačuvaj prvo slovo
        sufixes = ("a", "u", "a", "om", "u")
        return base + sufixes[idx]

    # Imena/prezimena na -a (Ana, Marija, Luka, Nikola, Siniša...)
    if tl.endswith("a"):
        sufixes = ("e", "i", "u", "om", "i")
        return t[:-1] + sufixes[idx]

    # Prezimena/imena na -o (Marko, Ivo, Bruno...)
    if tl.endswith("o"):
        sufixes = ("a", "u", "a", "om", "u")
        return t[:-1] + sufixes[idx]

    # Muška imena/prezimena na suglasnik (Ivan, Horvat, Kovač, Matej...)
    samoglasnici = set("aeiouAEIOU")
    if tl[-1] not in samoglasnici:
        sufixes = ("a", "u", "a", "om", "u")
        return t + sufixes[idx]

    # Fallback — ne mijenjaj
    return t


# =============================================================================
# LOKATIV GRADOVA — "u Zagrebu", "pred Splitskim sudom"
# =============================================================================

_LOKATIV_GRADOVA = {
    "Zagreb":          "Zagrebu",
    "Split":           "Splitu",
    "Rijeka":          "Rijeci",
    "Osijek":          "Osijeku",
    "Zadar":           "Zadru",
    "Pula":            "Puli",
    "Slavonski Brod":  "Slavonskom Brodu",
    "Karlovac":        "Karlovcu",
    "Varaždin":        "Varaždinu",
    "Šibenik":         "Šibeniku",
    "Sisak":           "Sisku",
    "Velika Gorica":   "Velikoj Gorici",
    "Dubrovnik":       "Dubrovniku",
    "Bjelovar":        "Bjelovaru",
    "Vukovar":         "Vukovaru",
    "Koprivnica":      "Koprivnici",
    "Požega":          "Požegi",
    "Čakovec":         "Čakovcu",
    "Gospić":          "Gospiću",
    "Virovitica":      "Virovitici",
}


def u_lokativu(grad):
    """Vraća lokativni oblik naziva grada za 'u [grad]', 'Sklopljen u [grad]'.
    Ako grad nije u rječniku, vraća nepromijenjeni string (sigurni fallback).
    """
    return _LOKATIV_GRADOVA.get(grad, grad)


def _padez_ime(ime_prezime, padez="gen"):
    """
    Otprilike deklinira osobno ime i prezime na hrvatski.
    Radi za vecinu uobicajenih hrvatskih imena i prezimena.
    Za nejasne slucajeve (nepostojano a, slozenice) vraca nominativ.

    ime_prezime: npr. 'Ivan Horvat', 'Ana Babić', 'Nikola Jurić'
    padez: 'nom'|'gen'|'dat'|'akuz'|'instr'|'lok'

    Primjeri:
        _padez_ime('Ivan Horvat', 'gen')  → 'Ivana Horvata'
        _padez_ime('Ana Babić', 'gen')    → 'Ane Babić'  (prezime ostaje jer je zensko)
        _padez_ime('Marko Jurić', 'dat')  → 'Marku Juriću'
        _padez_ime('Petar Kovač', 'gen')  → 'Petra Kovača'
    """
    if not ime_prezime:
        return ime_prezime
    idx = _PADEZ_IDX_IME.get(padez, 0)
    if idx == -1:
        return ime_prezime

    tokens = ime_prezime.strip().split()
    declined = [_deklinaj_token_ime(t, idx) for t in tokens]
    return " ".join(declined)


# --- Javne pomocne funkcije (isti potpisi kao original) ---


def format_navodnici(text):
    """Pretvara americke navodnike u hrvatske „..." i tekst unutar navodnika u italic.
    Radi na vec escaped tekstu (nakon _escape).
    """
    import re
    if not text:
        return text
    # Zamijeni parove navodnika: "tekst" -> „<i>tekst</i>"
    # Radimo na HTML-escaped tekstu pa trazimo &quot; ili obicne "
    result = re.sub(
        r'(?:&quot;|"|\u201E|\u201C)(.+?)(?:&quot;|"|\u201D|\u201C)',
        '\u201E<i>\\1</i>\u201C',
        text,
    )
    return result


def format_text(text):
    if text:
        escaped = _escape(text).replace('\n', '<br>')
        return format_navodnici(escaped)
    return ""


def formatiraj_troskovnik(troskovi):
    if not troskovi:
        return ""
    stavka = troskovi.get('stavka', 0.0)
    pdv = troskovi.get('pdv', 0.0)
    materijalni = troskovi.get('materijalni', 0.0)
    pristojba = troskovi.get('pristojba', 0.0)
    ukupno = stavka + pdv + materijalni + pristojba

    parts = [
        f"<div class='section-title' style='margin-top: 30px;'>POPIS TROŠKOVA POSTUPKA:</div>",
        f"<table class='cost-table'>",
        f'<tr><td width="70%">1. Sastav podneska/isprave (Tbr. Tarife):</td><td width="30%" align="right">{format_eur(stavka)}</td></tr>',
    ]
    if pdv > 0:
        parts.append(f'<tr><td>2. PDV (25%) na stavku 1.:</td><td align="right">{format_eur(pdv)}</td></tr>')
    if materijalni > 0:
        parts.append(f'<tr><td>3. Materijalni troškovi / JB Nagrada:</td><td align="right">{format_eur(materijalni)}</td></tr>')
    if pristojba > 0:
        parts.append(f'<tr><td>4. Sudska pristojba:</td><td align="right">{format_eur(pristojba)}</td></tr>')
    parts.append(
        f'<tr style="font-weight: bold; background-color: #f0f0f0;">'
        f'<td style="padding: 10px;">UKUPNO:</td>'
        f'<td style="padding: 10px;" align="right">{format_eur(ukupno)}</td></tr></table>'
    )
    return "".join(parts)


def unos_stranke(oznaka, key_prefix):
    st.markdown(f"**{oznaka}**")
    tip = st.radio(
        f"Tip ({oznaka})",
        ["Fizička osoba", "Pravna osoba"],
        key=f"{key_prefix}_tip",
        horizontal=True,
        label_visibility="collapsed",
    )
    col1, col2 = st.columns(2)
    has_valid_data = False

    if tip == "Fizička osoba":
        ime = col1.text_input(
            f"Ime i Prezime", key=f"{key_prefix}_ime",
            help="Upišite ime u nominativu (tko? što?). Npr. 'Ivan Horvat', ne 'Ivana Horvata'.",
        )
        _oib_key = f"{key_prefix}_oib"
        oib = col2.text_input(f"OIB", max_chars=11, key=_oib_key,
                              on_change=_strip_nondigits, args=(_oib_key, 11))
        adresa = st.text_input(f"Adresa (Ulica, Grad)", key=f"{key_prefix}_adresa")
        if oib:
            oib_ok, oib_msg = _validiraj_oib(oib)
            if not oib_ok and oib_msg:
                st.warning(oib_msg)
        if ime and oib:
            has_valid_data = True
            return (
                f"<b>{_escape(ime)}</b><br>Adresa: {_escape(adresa)}<br>OIB: {_escape(oib)}",
                "Fizička",
                has_valid_data,
            )
        return "____________________ (ime), OIB: ____________________", "Fizička", has_valid_data
    else:
        tvrtka = col1.text_input(f"Tvrtka", key=f"{key_prefix}_tvrtka")
        _oib_pr_key = f"{key_prefix}_oib_pravna"
        oib = col2.text_input(f"OIB", max_chars=11, key=_oib_pr_key,
                              on_change=_strip_nondigits, args=(_oib_pr_key, 11))
        mbs = col1.text_input(f"MBS", max_chars=8, key=f"{key_prefix}_mbs")
        zastupnik = col2.text_input(f"Zastupan po", key=f"{key_prefix}_zastupnik")
        sjediste = st.text_input(f"Sjedište", key=f"{key_prefix}_sjediste")
        if oib:
            oib_ok, oib_msg = _validiraj_oib(oib)
            if not oib_ok and oib_msg:
                st.warning(oib_msg)
        if tvrtka and oib:
            has_valid_data = True
            return (
                f"<b>{_escape(tvrtka)}</b><br>Sjedište: {_escape(sjediste)}<br>"
                f"OIB: {_escape(oib)}, MBS: {_escape(mbs)}<br>"
                f"Zastupana po: {_escape(zastupnik)}",
                "Pravna",
                has_valid_data,
            )
        return "____________________ (tvrtka), OIB: ____________________", "Pravna", has_valid_data


def zaglavlje_sastavljaca():
    with st.expander("Podaci o zastupanju (punomoćnik)", expanded=False):
        status = st.radio(
            "Dokument sastavlja:",
            ["Stranka osobno", "Odvjetnik po punomoći"],
            horizontal=True,
        )
        if status == "Odvjetnik po punomoći":
            odvjetnik = st.text_input("Podaci o odvjetniku/uredu")
            return f"<br>Zastupan po punomoćniku: {_escape(odvjetnik)}<br>"
        return ""


def odabir_suda(label="Naslovni sud", vrsta=None, key=None, index=0):
    """Selectbox za odabir suda iz baze.
    vrsta: 'opcinski', 'trgovacki', 'upravni' ili None za sve sudove.
    Vraca: naziv suda s dijakriticima (za prikaz u dokumentu).
    """
    if vrsta == "opcinski":
        opcije = OPCINSKI_SUDOVI
    elif vrsta == "trgovacki":
        opcije = TRGOVACKI_SUDOVI
    elif vrsta == "zupanijski":
        opcije = ZUPANIJSKI_SUDOVI
    elif vrsta == "upravni":
        opcije = UPRAVNI_SUDOVI
    else:
        opcije = SVI_SUDOVI

    # Dodaj opciju rucnog unosa na kraj
    opcije_display = [format_sud_s_dijakriticima(s) for s in opcije] + ["-- Ručni unos --"]
    odabrano = st.selectbox(label, opcije_display, index=index, key=key)

    if odabrano == "-- Ručni unos --":
        return st.text_input("Unesite naziv suda", key=f"{key}_rucni" if key else None)
    return odabrano


def unos_vise_stranaka(oznaka, key_prefix, min_stranaka=1, max_stranaka=10):
    """Dinamicki unos vise stranaka (tuzitelji/tuzenici).
    Vraca: lista tuple-ova [(html_stranke, tip_stranke, has_valid_data), ...]
    """
    # Inicijaliziraj broj stranaka u session_state
    count_key = f"{key_prefix}_count"
    if count_key not in st.session_state:
        st.session_state[count_key] = min_stranaka

    st.markdown(f"**{oznaka}**")

    stranke = []
    for i in range(st.session_state[count_key]):
        suffix = f"{key_prefix}_{i}"
        if st.session_state[count_key] > 1:
            st.markdown(f"*{oznaka} {i + 1}:*")
        stranka = unos_stranke(f"{oznaka} {i + 1}" if st.session_state[count_key] > 1 else oznaka, suffix)
        stranke.append(stranka)

    # Gumbi za dodavanje/uklanjanje
    col_add, col_rem = st.columns(2)
    with col_add:
        if st.session_state[count_key] < max_stranaka:
            if st.button(f"+ Dodaj {oznaka.lower()}", key=f"{key_prefix}_add"):
                st.session_state[count_key] += 1
                st.rerun()
    with col_rem:
        if st.session_state[count_key] > min_stranaka:
            if st.button(f"- Ukloni zadnjeg", key=f"{key_prefix}_rem"):
                st.session_state[count_key] -= 1
                st.rerun()

    return stranke


def spoji_stranke_html(stranke_lista, oznaka_jednine="TUŽITELJ", oznaka_mnozine="TUŽITELJI"):
    """Spaja listu stranaka u HTML za prikaz u dokumentu.
    stranke_lista: lista tuple-ova iz unos_vise_stranaka
    """
    if len(stranke_lista) == 1:
        return stranke_lista[0][0]  # samo html jedne stranke
    parts = []
    oznaka = oznaka_mnozine if len(stranke_lista) > 1 else oznaka_jednine
    for i, (html, tip, valid) in enumerate(stranke_lista, 1):
        parts.append(f"{i}. {html}")
    return "<br>".join(parts)


def unos_tocaka(oznaka, key_prefix, placeholder="", min_tocaka=1, max_tocaka=20, height=80,
                s_dokazima=False, dokaz_placeholder="Dokaz za ovu točku..."):
    """Dinamicki unos vise tekstualnih tocaka za dokument.
    Koristi se za: cinjenicne navode, dokazne prijedloge, razloge, tocke tuzbenog zahtjeva itd.

    Ako s_dokazima=True, svaka tocka ima opcionalni dokaz.
    Vraca:
        - ako s_dokazima=False: lista stringova (nepraznih)
        - ako s_dokazima=True: lista dict-ova {'tekst': str, 'dokaz': str}
    """
    count_key = f"{key_prefix}_tocke_count"
    if count_key not in st.session_state:
        st.session_state[count_key] = max(min_tocaka, 1)

    tocke = []
    for i in range(st.session_state[count_key]):
        redni = i + 1
        label = f"Točka {redni}" if st.session_state[count_key] > 1 else oznaka

        if s_dokazima:
            with st.container():
                st.markdown(f"**{redni}.** točka")
                t = st.text_area(
                    f"Navod / činjenica ({redni})",
                    key=f"{key_prefix}_t_{i}",
                    placeholder=placeholder,
                    height=height,
                    label_visibility="collapsed",
                )
                d = st.text_input(
                    f"Dokaz ({redni})",
                    key=f"{key_prefix}_d_{i}",
                    placeholder=dokaz_placeholder,
                )
                if t and t.strip():
                    tocke.append({'tekst': t.strip(), 'dokaz': d.strip() if d else ''})
                if i < st.session_state[count_key] - 1:
                    st.markdown("---")
        else:
            t = st.text_area(
                label,
                key=f"{key_prefix}_t_{i}",
                placeholder=placeholder,
                height=height,
            )
            if t and t.strip():
                tocke.append(t.strip())

    col_add, col_rem = st.columns(2)
    with col_add:
        if st.session_state[count_key] < max_tocaka:
            if st.button("+ Dodaj točku", key=f"{key_prefix}_add_t"):
                st.session_state[count_key] += 1
                st.rerun()
    with col_rem:
        if st.session_state[count_key] > min_tocaka:
            if st.button("- Ukloni zadnju", key=f"{key_prefix}_rem_t"):
                st.session_state[count_key] -= 1
                st.rerun()

    return tocke


def formatiraj_tocke_html(tocke, stil="numbered"):
    """Formatira listu tocaka u HTML. Koristi se u generatorima.
    tocke: lista stringova ILI lista dict-ova {'tekst': str, 'dokaz': str}
    stil: 'numbered' (ol), 'bulleted' (ul), 'paragraphs' (br razmak)
    """
    if not tocke:
        return ""

    # Provjeri je li lista dict-ova (tocke s dokazima)
    ima_dokaze = isinstance(tocke[0], dict)

    if ima_dokaze:
        items = []
        for t in tocke:
            tekst = format_text(t['tekst'])
            dokaz = t.get('dokaz', '')
            if dokaz:
                items.append(f"<li>{tekst}<br><i>Dokaz: {format_text(dokaz)}</i></li>")
            else:
                items.append(f"<li>{tekst}</li>")
        if stil == "bulleted":
            return f"<ul>{''.join(items)}</ul>"
        return f"<ol>{''.join(items)}</ol>"

    if stil == "numbered":
        items = "".join(f"<li>{format_text(t)}</li>" for t in tocke)
        return f"<ol>{items}</ol>"
    elif stil == "bulleted":
        items = "".join(f"<li>{format_text(t)}</li>" for t in tocke)
        return f"<ul>{items}</ul>"
    else:
        return "<br><br>".join(format_text(t) for t in tocke)


def docx_opcije():
    """Prikazuje opcije za DOCX export (watermark, header). Poziva se prije generiranja."""
    with st.expander("DOCX opcije (watermark, zaglavlje)", expanded=False):
        col1, col2 = st.columns(2)
        watermark = col1.checkbox('Dodaj watermark "NACRT"', key="_docx_watermark")
        naslov_u_header = col2.checkbox("Dodaj naziv dokumenta u zaglavlje", value=True, key="_docx_header")
        return watermark, naslov_u_header


def _audit_safe(value):
    """Rekurzivno konvertira non-JSON tipove u JSON-safe (date/datetime → ISO string).

    Potrebno jer `audit_chain.canonical_input_hash` koristi `json.dumps`, koji
    ne podrzava date/datetime. Druge non-JSON tipove (Decimal, custom objekti)
    ostavlja netaknute — pozivatelj ih mora pripremiti ili ce audit pasti u tihi
    fall-through (docx_export.py:603-613).
    """
    from datetime import datetime
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _audit_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_audit_safe(v) for v in value]
    return value


def audit_kwargs(doc_type, input_dict, modul):
    """Helper za K1 audit chain. Vraca kwargs spreman za **unpack u prikazi_dokument().

    Primjer:
        prikazi_dokument(doc, "Tuzba.docx", "Preuzmi",
                         **audit_kwargs("tuzba", podaci, "tuzbe"))

    `modul` moze biti kratko ime ('tuzbe'), bez ekstenzije ('generatori/tuzbe')
    ili puna putanja ('generatori/tuzbe.py'). Helper resolva u 'generatori/<ime>.py'.
    """
    if "/" in modul:
        modul_path = modul if modul.endswith(".py") else f"{modul}.py"
    else:
        ime = modul[:-3] if modul.endswith(".py") else modul
        modul_path = f"generatori/{ime}.py"
    return {
        "doc_type": doc_type,
        "input_dict": _audit_safe(input_dict),
        "generator_module_path": modul_path,
    }


def prikazi_dokument(
    doc_html,
    naziv_datoteke,
    label_preuzmi="Preuzmi",
    *,
    doc_type=None,
    input_dict=None,
    generator_module_path=None,
):
    """Pomocna funkcija za prikaz dokumenta i download gumb (.docx format).

    K1 audit chain: kad su `doc_type`, `input_dict` i `generator_module_path`
    proslijedjeni, `pripremi_za_docx` racuna canonical hash, generator hash
    i upisuje u download_log. Bez njih je no-op (backwards-compat).
    Konvencija za `doc_type`: flat snake_case (npr. "ugovor_kupoprodaja",
    "ovrha_vjerodostojna", "tuzba_isplata").
    """
    # Success banner
    st.markdown(
        "<div style='background:linear-gradient(135deg,#059669 0%,#047857 100%);color:white;"
        "padding:1rem 1.5rem;border-radius:10px;margin:1rem 0;text-align:center;'>"
        "<span style='font-size:1.3rem;font-weight:700;'>"
        "\u2705 Dokument je spreman!</span><br>"
        "<span style='font-size:0.85rem;opacity:0.9;'>"
        "Pregledajte dokument ispod i preuzmite ga u DOCX formatu.</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Generiraj .docx
    docx_naziv = naziv_datoteke.replace('.doc', '.docx') if naziv_datoteke.endswith('.doc') else naziv_datoteke
    if not docx_naziv.endswith('.docx'):
        docx_naziv += '.docx'

    # Dohvati DOCX opcije iz session_state
    watermark_tekst = "NACRT" if st.session_state.get("_docx_watermark") else None
    naslov = docx_naziv.replace('.docx', '').replace('_', ' ') if st.session_state.get("_docx_header") else None

    docx_bytes = pripremi_za_docx(
        doc_html,
        watermark=watermark_tekst,
        naslov_dokumenta=naslov,
        doc_type=doc_type,
        input_dict=input_dict,
        generator_module_path=generator_module_path,
    )

    # Prominentan download gumb PRIJE dokumenta
    st.download_button(
        f"\u2b07\ufe0f {label_preuzmi} ({docx_naziv})",
        docx_bytes,
        docx_naziv,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    # Pregled dokumenta
    st.markdown(f"<div class='legal-doc'>{doc_html}</div>", unsafe_allow_html=True)


def odredi_nadlezni_sud(tip_stranke1, tip_stranke2, zadani_sud="OPĆINSKI GRAĐANSKI SUD U ZAGREBU"):
    """Odreduje nadlezni sud - Trgovacki ako su obje stranke pravne osobe."""
    if tip_stranke1 == "Pravna" and tip_stranke2 == "Pravna":
        return "TRGOVAČKI SUD U ZAGREBU"
    return zadani_sud


# =============================================================================
# PRIMJERI / PREDLOŠCI - "Napuni primjerom" za brži unos
# =============================================================================

# Pool nasumicnih podataka za primjere
_POOL_IMENA = [
    "Ivan Horvat", "Ana Marić", "Marko Novak", "Petra Jurić",
    "Ante Babić", "Maja Knežević", "Luka Tomić", "Sara Pavlović",
    "Josip Kovačević", "Ivana Matić", "Tomislav Perić", "Marina Vuković",
    "Davor Šimunović", "Katarina Blažević", "Filip Radić", "Nikolina Grgić",
]
_POOL_ADRESA = [
    "Ilica 42, 10000 Zagreb", "Vukovarska 15, 21000 Split",
    "Gundulićeva 8, 31000 Osijek", "Korzo 20, 51000 Rijeka",
    "Obala 3, 23000 Zadar", "Savska 25, 10000 Zagreb",
    "Draškovićeva 12, 10000 Zagreb", "Frankopanska 7, 10000 Zagreb",
    "Maksimirska 88, 10000 Zagreb", "Zvonimirova 19, 10000 Zagreb",
    "Stjepana Radića 5, 40000 Čakovec", "Trg bana Jelačića 1, 10000 Zagreb",
]
_POOL_OIBA = [
    "12345678903", "98765432101", "55443322110",
    "33221100998", "99887766554", "44556677889",
    "77665544332", "11998877665", "22334455667",
]
_POOL_TVRTKI = [
    "ABC d.o.o.", "DEF d.o.o.", "XYZ d.o.o.",
    "Tech Solutions d.o.o.", "Mega Trade d.o.o.", "Nova Gradnja d.o.o.",
    "Adriatic IT d.o.o.", "Plavi val d.o.o.", "Zeleni vrh d.o.o.",
]
_POOL_ZASTUPNIKA = [
    "Direktor Ivan Horvat", "Direktor Ana Marić", "Direktor Marko Novak",
    "Prokuristica Petra Jurić", "Član uprave Ante Babić",
    "Direktor Tomislav Perić", "Direktorica Marina Vuković",
]
_POOL_SJEDISTA = [
    "Heinzelova 33, 10000 Zagreb", "Radnička 47, 10000 Zagreb",
    "Savska 100, 10000 Zagreb", "Grada Vukovara 269, 10000 Zagreb",
    "Slavonska avenija 6, 10000 Zagreb", "Avenija Dubrovnik 15, 10000 Zagreb",
    "Ulica grada Vukovara 37, 10000 Zagreb",
]


def _randomiziraj_primjer(primjer):
    """Nasumicno zamjenjuje osobne podatke u primjeru.
    Svaki poziv daje drugacije podatke (eksplicitni re-seed).
    """
    import random
    import copy
    import time

    # Eksplicitni re-seed za svaki poziv — osigurava razlicite rezultate
    random.seed(time.time_ns())

    p = copy.deepcopy(primjer)

    imena = random.sample(_POOL_IMENA, min(len(_POOL_IMENA), 8))
    adrese = random.sample(_POOL_ADRESA, min(len(_POOL_ADRESA), 8))
    oibi = random.sample(_POOL_OIBA, min(len(_POOL_OIBA), 6))
    tvrtke = random.sample(_POOL_TVRTKI, min(len(_POOL_TVRTKI), 6))
    zastupnici = random.sample(_POOL_ZASTUPNIKA, min(len(_POOL_ZASTUPNIKA), 5))
    sjedista = random.sample(_POOL_SJEDISTA, min(len(_POOL_SJEDISTA), 5))

    idx = {'ime': 0, 'adr': 0, 'oib': 0, 'tvr': 0, 'zas': 0, 'sjd': 0}

    # Randomiziraj stranke
    for key in list(p.get('stranke', {}).keys()):
        if key.endswith('_tip'):
            continue
        if key.endswith('_ime') or key in ('tuzitelj', 'tuzenik'):
            p['stranke'][key] = imena[idx['ime'] % len(imena)]
            idx['ime'] += 1
        elif key.endswith('_adresa'):
            p['stranke'][key] = adrese[idx['adr'] % len(adrese)]
            idx['adr'] += 1
        elif key.endswith('_oib') or key.endswith('_oib_pravna'):
            p['stranke'][key] = oibi[idx['oib'] % len(oibi)]
            idx['oib'] += 1
        elif key.endswith('_tvrtka'):
            p['stranke'][key] = tvrtke[idx['tvr'] % len(tvrtke)]
            idx['tvr'] += 1
        elif key.endswith('_zastupnik'):
            p['stranke'][key] = zastupnici[idx['zas'] % len(zastupnici)]
            idx['zas'] += 1
        elif key.endswith('_sjediste'):
            p['stranke'][key] = sjedista[idx['sjd'] % len(sjedista)]
            idx['sjd'] += 1

    # Randomiziraj osobne podatke u podaci dict (ako sadrze imena/adrese)
    for key in list(p.get('podaci', {}).keys()):
        val = p['podaci'][key]
        if not isinstance(val, str):
            continue
        # Zamijeni poznata imena iz originalnog primjera s random imenima
        for orig_ime in _POOL_IMENA[:10]:
            if orig_ime in val:
                novo_ime = imena[idx['ime'] % len(imena)]
                val = val.replace(orig_ime, novo_ime)
                idx['ime'] += 1
                break
        p['podaci'][key] = val

    return p


# Rjecnik primjera za razne tipove dokumenata
# VAZNO: kljucevi stranaka moraju tocno odgovarati widget key-evima!
# Fizicka: {prefix}_ime, {prefix}_oib, {prefix}_adresa
# Pravna:  {prefix}_tip='Pravna osoba', {prefix}_tvrtka, {prefix}_oib_pravna,
#          {prefix}_sjediste, {prefix}_zastupnik, {prefix}_mbs
PRIMJERI = {
    'tuzba': {
        'opis': 'Tužba radi isplate - naplata dugovanja po računu',
        'stranke': {
            't1_ime': 'Ante Kovačević',
            't1_oib': '12345678903',
            't1_adresa': 'Ilica 42, 10000 Zagreb',
            't2_ime': 'Marko Novak',
            't2_oib': '98765432101',
            't2_adresa': 'Vukovarska 15, 21000 Split',
        },
        'podaci': {
            'vps': 5000.0,
            'vrsta': 'Isplate (dugovanja po računu)',
        },
        'cinjenice': [
            {'tekst': 'Dana 15.03.2024. tužitelj je tuženiku isporučio robu prema narudžbi br. 45/2024, za što je ispostavio račun br. R-78/2024 na iznos od 5.000,00 EUR s rokom plaćanja od 30 dana.',
             'dokaz': 'Račun br. R-78/2024 od 15.03.2024.'},
            {'tekst': 'Tuženik je robu zaprimio bez prigovora, što je potvrdio potpisom na otpremnici br. OTP-78/2024.',
             'dokaz': 'Otpremnica br. OTP-78/2024 s potpisom tuženika'},
            {'tekst': 'Unatoč proteku roka plaćanja i pisanoj opomeni od 20.05.2024., tuženik do danas nije podmirio dugovanje.',
             'dokaz': 'Opomena pred tužbu od 20.05.2024. s povratnicom'},
        ],
        'trosak_sastav': 312.50,
    },
    'ovrha': {
        'opis': 'Ovrha na temelju vjerodostojne isprave (nenaplaćeni račun)',
        'stranke': {
            'o1_tip': 'Pravna osoba',
            'o1_tvrtka': 'ABC d.o.o.',
            'o1_oib_pravna': '11223344556',
            'o1_sjediste': 'Heinzelova 33, 10000 Zagreb',
            'o2_tip': 'Pravna osoba',
            'o2_tvrtka': 'DEF d.o.o.',
            'o2_oib_pravna': '66554433221',
            'o2_sjediste': 'Radnička 47, 10000 Zagreb',
        },
    },
    'opomena': {
        'opis': 'Opomena pred tužbu za nepodmireni račun',
        'stranke': {
            'op_v_tip': 'Pravna osoba',
            'op_v_tvrtka': 'ABC d.o.o.',
            'op_v_oib_pravna': '11223344556',
            'op_v_sjediste': 'Heinzelova 33, 10000 Zagreb',
            'op_v_zastupnik': 'Direktor Ivan Horvat',
            'op_d_ime': 'Marko Novak',
            'op_d_oib': '98765432101',
            'op_d_adresa': 'Vukovarska 15, 21000 Split',
        },
        'podaci': {
            'glavnica': 3500.0,
        },
    },
    'kaznena_prijava': {
        'opis': 'Kaznena prijava za prijevaru (čl. 236. KZ)',
        'stranke': {
            'kp_ime': 'Ana Marić',
            'kp_oib': '12345678903',
            'kp_adresa': 'Gundulićeva 8, 10000 Zagreb',
        },
        'podaci': {
            'kp_clanak': 'čl. 236. st. 1. KZ (Prijevara)',
            'kp_osumnjicenik': 'Petar Babić, Draškovićeva 12, Zagreb, OIB: 99887766554',
            'kp_mjesto': 'Zagreb',
        },
    },
    'zalba_zup': {
        'opis': 'Žalba na rješenje o odbijanju zahtjeva (ZUP)',
        'stranke': {
            'zup_z_ime': 'Ivan Horvat',
            'zup_z_oib': '12345678903',
            'zup_z_adresa': 'Savska 25, 10000 Zagreb',
        },
        'podaci': {
            'zup_prvostupanjsko': 'Upravni odjel za komunalno gospodarstvo Grada Zagreba',
            'zup_drugostupanjsko': 'Ministarstvo prostornoga uređenja, graditeljstva i državne imovine',
            'zup_klasa': 'UP/I-361-01/24-01/123',
            'zup_urbroj': '251-13-11/2-24-5',
            'zup_mjesto': 'Zagreb',
        },
    },
    'zalba_presuda': {
        'opis': 'Žalba na presudu radi isplate - pogrešno utvrđeno činjenično stanje',
        'stranke': {
            'zal_tuzitelj': 'Ante Kovačević',
            'zal_tuzenik': 'Marko Novak',
        },
        'podaci': {
            'zal_broj_presude': 'P-456/2024',
            'zal_mjesto': 'Zagreb',
        },
    },
    'ugovor_kupoprodaja': {
        'opis': 'Ugovor o kupoprodaji rabljenog vozila',
        'stranke': {
            'u1_ime': 'Ivan Horvat',
            'u1_oib': '12345678903',
            'u1_adresa': 'Ilica 42, 10000 Zagreb',
            'u2_ime': 'Ana Marić',
            'u2_oib': '98765432101',
            'u2_adresa': 'Vukovarska 15, 21000 Split',
        },
    },
    'ugovor_o_radu': {
        'opis': 'Ugovor o radu na neodređeno vrijeme',
        'stranke': {
            'p_tip': 'Pravna osoba',
            'p_tvrtka': 'ABC d.o.o.',
            'p_oib_pravna': '11223344556',
            'p_sjediste': 'Heinzelova 33, 10000 Zagreb',
            'p_zastupnik': 'Direktor Petar Babić',
            'r_ime': 'Ana Marić',
            'r_oib': '98765432101',
            'r_adresa': 'Savska 25, 10000 Zagreb',
        },
        'podaci': {
            'ur_naziv_radnog_mjesta': 'Pravni savjetnik',
            'ur_opis_posla': 'Pravno savjetovanje, izrada ugovora i pravnih mišljenja, '
                             'zastupanje pred sudovima i tijelima uprave',
            'ur_mjesto_rada': 'sjedište Poslodavca',
            'ur_bruto_placa': 2000.0,
        },
    },
    'punomoc': {
        'opis': 'Posebna punomoć za zastupanje u parničnom postupku',
        'stranke': {
            'pm_v_ime': 'Ivan Horvat',
            'pm_v_oib': '12345678903',
            'pm_v_adresa': 'Ilica 42, 10000 Zagreb',
            'pm_p_ime': 'Marko Novak, odvjetnik',
            'pm_p_oib': '98765432101',
            'pm_p_adresa': 'Ulica kralja Zvonimira 5, 10000 Zagreb',
        },
        'podaci': {
            'pm_opseg': 'Zastupanje u parničnom postupku pred Općinskim građanskim sudom u Zagrebu, '
                        'poslovni broj P-123/2024, uključujući podnošenje tužbe, prisustvovanje ročištima, '
                        'sklapanje nagodbe, podnošenje pravnih lijekova i poduzimanje svih pravnih radnji '
                        'u postupku.',
            'pm_mjesto': 'Zagreb',
        },
    },
    'trgovacko_drustveni': {
        'opis': 'Društveni ugovor d.o.o. - jednostavno osnivanje',
        'podaci': {
            'naziv_drustva': 'Tech Solutions d.o.o.',
            'sjediste': 'Zagreb, Ilica 100',
            'temeljni_kapital': 2500.0,
            'predmet_poslovanja': '62.01 Računalno programiranje',
        },
    },
    'obvezno_darovanje': {
        'opis': 'Ugovor o darovanju nekretnine',
        'stranke': {
            'od_ime': 'Marija Horvat',
            'od_oib': '12345678903',
            'od_adresa': 'Savska 10, 10000 Zagreb',
            'op_ime': 'Ivan Horvat',
            'op_oib': '98765432101',
            'op_adresa': 'Savska 10, 10000 Zagreb',
        },
    },
    'obiteljsko_razvod': {
        'opis': 'Sporazumni prijedlog za razvod braka',
        'stranke': {
            'sr_p1_tip': 'Fizička osoba',
            'sr_p1_ime': 'Ivan Horvat',
            'sr_p1_oib': '12345678903',
            'sr_p1_adresa': 'Ilica 42, 10000 Zagreb',
            'sr_p2_tip': 'Fizička osoba',
            'sr_p2_ime': 'Ana Horvat',
            'sr_p2_oib': '98765432101',
            'sr_p2_adresa': 'Ilica 42, 10000 Zagreb',
        },
        'podaci': {
            'sr_mjesto_braka': 'Zagreb',
        },
    },
    'stecaj_potrosac': {
        'opis': 'Prijedlog za stečaj potrošača (osobni bankrot)',
        'stranke': {
            'sp_ime': 'Petar Babić',
            'sp_oib': '12345678903',
            'sp_adresa': 'Draškovićeva 12, 10000 Zagreb',
        },
        'podaci': {
            'ukupni_dug': 15000.0,
            'trajanje_blokade_dana': 120,
        },
    },
    'potrosac_reklamacija': {
        'opis': 'Reklamacija trgovcu za neispravan proizvod',
        'stranke': {
            'pr_ime': 'Ana Marić',
            'pr_oib': '98765432101',
            'pr_adresa': 'Vukovarska 15, 21000 Split',
        },
        'podaci': {
            'trgovac': 'ElektroShop d.o.o., Heinzelova 33, Zagreb, OIB: 11223344556',
            'proizvod': 'Prijenosno računalo HP Pavilion 15',
            'datum_kupnje': '15.01.2026.',
            'opis_nedostatka': 'Ekran prijenosnog računala prestao je raditi nakon 3 tjedna korištenja. '
                               'Pojavljuje se crni ekran pri pokretanju unatoč ispravnom napajanju.',
        },
    },
    'zemljisne_tabularna': {
        'opis': 'Tabularna isprava za uknjižbu prava vlasništva',
        'stranke': {
            'tp_ime': 'Marko Novak',
            'tp_oib': '12345678903',
            'tp_adresa': 'Vukovarska 15, 21000 Split',
            'tk_ime': 'Ivan Horvat',
            'tk_oib': '98765432101',
            'tk_adresa': 'Ilica 42, 10000 Zagreb',
        },
    },
}


def napuni_primjerom(tip_dokumenta, key_prefix=""):
    """Prikazuje gumb 'Napuni primjerom' i vraca dict s primjerom ili None.
    Svaki klik nasumicno zamjenjuje osobne podatke (imena, adrese, OIB-ove).
    Cisti suprotne kljuceve (fizicka vs pravna) da se izbjegnu "krive prozore".
    """
    if tip_dokumenta not in PRIMJERI:
        return None

    primjer = PRIMJERI[tip_dokumenta]
    btn_key = f"_primjer_{key_prefix}_{tip_dokumenta}" if key_prefix else f"_primjer_{tip_dokumenta}"

    with st.expander(f"Primjer: {primjer['opis']}", expanded=False):
        st.caption(
            "Kliknite gumb za automatsko popunjavanje forme primjerom. "
            "Zatim prilagodite podatke svojem slučaju."
        )
        if st.button("Napuni primjerom", key=btn_key, type="secondary"):
            import copy
            randomized = copy.deepcopy(primjer)

            # Prikupi prefikse stranaka iz primjera za ciscenje starih kljuceva
            stranke_keys = set(randomized.get('stranke', {}).keys())
            stranke_prefiksi = set()
            for k in stranke_keys:
                # Izvuci prefiks stranke (npr. 'o1' iz 'o1_ime', 'op_v' iz 'op_v_tvrtka')
                for suffix in ('_ime', '_oib', '_adresa', '_tvrtka', '_oib_pravna',
                               '_sjediste', '_zastupnik', '_mbs', '_tip'):
                    if k.endswith(suffix):
                        stranke_prefiksi.add(k[:-len(suffix)])
                        break

            # Cisti suprotne kljuceve za svaki prefiks stranke
            _fizicka_sufiksi = ('_ime', '_oib', '_adresa')
            _pravna_sufiksi = ('_tvrtka', '_oib_pravna', '_sjediste', '_zastupnik', '_mbs')
            for sp in stranke_prefiksi:
                tip_key = f"{key_prefix}_{sp}_tip" if key_prefix else f"{sp}_tip"
                tip_val = randomized.get('stranke', {}).get(f"{sp}_tip", "")
                if tip_val == "Pravna osoba":
                    # Ocisti fizicka polja
                    for suf in _fizicka_sufiksi:
                        fk = f"{key_prefix}_{sp}{suf}" if key_prefix else f"{sp}{suf}"
                        st.session_state.pop(fk, None)
                elif tip_val == "Fizička osoba":
                    # Ocisti pravna polja
                    for suf in _pravna_sufiksi:
                        fk = f"{key_prefix}_{sp}{suf}" if key_prefix else f"{sp}{suf}"
                        st.session_state.pop(fk, None)

            # Postavi nove vrijednosti
            for k, v in randomized.get('stranke', {}).items():
                full_key = f"{key_prefix}_{k}" if key_prefix else k
                st.session_state[full_key] = v
            for k, v in randomized.get('podaci', {}).items():
                full_key = f"{key_prefix}_{k}" if key_prefix else k
                st.session_state[full_key] = v
            st.rerun()
    return primjer


# =============================================================================
# PROVJERA ROKOVA I ZASTARE
# =============================================================================

def provjeri_zastaru(datum_dospijeca, rok_godina=5, opis_roka="opći zastarni rok"):
    """Provjerava zastaru i prikazuje upozorenje ako je blizu ili istekao.
    Args:
        datum_dospijeca: date objekt
        rok_godina: broj godina zastarnog roka (default 5 za opći rok, čl. 225. ZOO)
        opis_roka: opis pravnog temelja roka
    """
    if not datum_dospijeca:
        return
    from datetime import date as _date
    danas = _date.today()
    razlika = danas - datum_dospijeca
    dana = razlika.days
    godina = dana / 365.25

    rok_dana = rok_godina * 365

    if dana > rok_dana:
        prekoracenje = dana - rok_dana
        st.error(
            f"**Moguća zastara!** Od datuma dospijeća prošlo je {godina:.1f} godina "
            f"({opis_roka}: {rok_godina} god, čl. 225. ZOO). "
            f"Rok je istekao prije ~{prekoracenje} dana. "
            f"Razmotrite je li zastara prekinuta ili odgođena."
        )
    elif dana > rok_dana - 180:  # Unutar 6 mjeseci od zastare
        preostalo = rok_dana - dana
        st.warning(
            f"**Zastara se približava!** Od datuma dospijeća prošlo je {godina:.1f} godina. "
            f"{opis_roka} ({rok_godina} god) istječe za ~{preostalo} dana. "
            f"Preporučujemo hitno podnošenje tužbe."
        )
    elif dana > rok_dana - 365:  # Unutar godinu dana od zastare
        preostalo = rok_dana - dana
        st.info(
            f"Do isteka zastarnog roka ({opis_roka}: {rok_godina} god) preostalo je ~{preostalo} dana "
            f"({preostalo // 30} mjeseci)."
        )


def provjeri_rok_zalbe(datum_dostave=None, rok_dana=15, opis="rok za žalbu"):
    """Provjerava je li rok za žalbu istekao."""
    if not datum_dostave:
        return
    from datetime import date as _date
    danas = _date.today()
    razlika = danas - datum_dostave
    dana = razlika.days

    if dana > rok_dana:
        prekoracenje = dana - rok_dana
        st.error(
            f"**Rok istekao!** {opis.capitalize()} od {rok_dana} dana istekao je prije {prekoracenje} dana. "
            f"Žalba podnesena nakon roka bit će odbačena kao nepravodobna."
        )
    elif dana >= rok_dana - 3:
        preostalo = rok_dana - dana
        st.warning(
            f"**Hitno!** {opis.capitalize()} istječe za {preostalo} dan{'a' if preostalo != 1 else ''}!"
        )
    elif dana >= 0:
        preostalo = rok_dana - dana
        st.info(
            f"{opis.capitalize()}: preostalo {preostalo} dana (rok {rok_dana} dana od dostave)."
        )


def doc_selectbox(label: str, options: list, key: str = None, index: int = 0):
    """
    Prominentni selectbox za odabir vrste dokumenta.
    Prikazuje styled navy label iznad selectboxa.
    Kad se vrijednost promijeni, scrolla stranicu na vrh.
    """
    st.markdown(
        f'<div class="doc-selector-label">{label.upper()}</div>',
        unsafe_allow_html=True,
    )
    result = st.selectbox(label, options, key=key, index=index, label_visibility="collapsed")
    if key:
        _prev_key = f"_prev_docsel_{key}"
        prev_val = st.session_state.get(_prev_key)
        if prev_val is not None and prev_val != result:
            _scroll_na_vrh()
        st.session_state[_prev_key] = result
    return result


def clause_builder(kljuc_sesije: str, sekcije_default: list) -> list:
    """
    Prikazuje UI za odabir i redoslijed odjeljaka dokumenta.
    Vraća listu ID-ova odabranih odjeljaka u redoslijedu koji je korisnik postavio.

    kljuc_sesije: prefiks za session_state (npr. "pp_sekcije")
    sekcije_default: lista dicts s id, naziv, obavezno, ukljuceno (i opcionalno fiksna_pozicija)
    """
    import copy

    if kljuc_sesije not in st.session_state:
        st.session_state[kljuc_sesije] = copy.deepcopy(sekcije_default)

    sekcije = st.session_state[kljuc_sesije]

    fiksne_zadnje = [s for s in sekcije if s.get("fiksna_pozicija") == "zadnja"]
    slobodne = [s for s in sekcije if s.get("fiksna_pozicija") != "zadnja"]

    st.caption("Odaberite odjeljke i podesite redoslijed:")

    for i, sek in enumerate(slobodne):
        col_check, col_naziv, col_gore, col_dole = st.columns([0.5, 5, 0.5, 0.5])

        with col_check:
            if sek["obavezno"]:
                st.checkbox(
                    "", value=True, disabled=True,
                    key=f"{kljuc_sesije}_chk_{sek['id']}"
                )
            else:
                novo = st.checkbox(
                    "", value=sek["ukljuceno"],
                    key=f"{kljuc_sesije}_chk_{sek['id']}"
                )
                if novo != sek["ukljuceno"]:
                    st.session_state[kljuc_sesije][i]["ukljuceno"] = novo
                    st.rerun()

        with col_naziv:
            if sek["ukljuceno"] or sek["obavezno"]:
                st.markdown(f"**{sek['naziv']}**")
            else:
                st.markdown(f"<span style='color:#888'>{sek['naziv']}</span>", unsafe_allow_html=True)

        with col_gore:
            if i > 0 and st.button("↑", key=f"{kljuc_sesije}_gore_{i}"):
                slobodne[i], slobodne[i - 1] = slobodne[i - 1], slobodne[i]
                st.session_state[kljuc_sesije] = slobodne + fiksne_zadnje
                st.rerun()

        with col_dole:
            if i < len(slobodne) - 1 and st.button("↓", key=f"{kljuc_sesije}_dole_{i}"):
                slobodne[i], slobodne[i + 1] = slobodne[i + 1], slobodne[i]
                st.session_state[kljuc_sesije] = slobodne + fiksne_zadnje
                st.rerun()

    for sek in fiksne_zadnje:
        col_check, col_naziv, _, _ = st.columns([0.5, 5, 0.5, 0.5])
        with col_check:
            st.checkbox(
                "", value=True, disabled=True,
                key=f"{kljuc_sesije}_chk_{sek['id']}"
            )
        with col_naziv:
            st.markdown(f"**{sek['naziv']}**")

    return [s["id"] for s in (slobodne + fiksne_zadnje) if s.get("ukljuceno") or s.get("obavezno")]
