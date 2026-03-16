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
        ime = col1.text_input(f"Ime i Prezime", key=f"{key_prefix}_ime")
        oib = col2.text_input(f"OIB", max_chars=11, key=f"{key_prefix}_oib")
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
        oib = col2.text_input(f"OIB", max_chars=11, key=f"{key_prefix}_oib_pravna")
        mbs = col1.text_input(f"MBS", key=f"{key_prefix}_mbs")
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


def prikazi_dokument(doc_html, naziv_datoteke, label_preuzmi="Preuzmi"):
    """Pomocna funkcija za prikaz dokumenta i download gumb (.docx format)."""
    st.markdown(f"<div class='legal-doc'>{doc_html}</div>", unsafe_allow_html=True)

    # Generiraj .docx
    docx_naziv = naziv_datoteke.replace('.doc', '.docx') if naziv_datoteke.endswith('.doc') else naziv_datoteke
    if not docx_naziv.endswith('.docx'):
        docx_naziv += '.docx'

    # Dohvati DOCX opcije iz session_state
    watermark_tekst = "NACRT" if st.session_state.get("_docx_watermark") else None
    naslov = docx_naziv.replace('.docx', '').replace('_', ' ') if st.session_state.get("_docx_header") else None

    docx_bytes = pripremi_za_docx(doc_html, watermark=watermark_tekst, naslov_dokumenta=naslov)
    st.download_button(
        label_preuzmi,
        docx_bytes,
        docx_naziv,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


def odredi_nadlezni_sud(tip_stranke1, tip_stranke2, zadani_sud="OPĆINSKI GRAĐANSKI SUD U ZAGREBU"):
    """Odreduje nadlezni sud - Trgovacki ako su obje stranke pravne osobe."""
    if tip_stranke1 == "Pravna" and tip_stranke2 == "Pravna":
        return "TRGOVAČKI SUD U ZAGREBU"
    return zadani_sud


# =============================================================================
# PRIMJERI / PREDLOŠCI - "Napuni primjerom" za brži unos
# =============================================================================

# Rjecnik primjera za razne tipove dokumenata
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
            'o1_ime': 'ABC d.o.o.',
            'o1_oib': '11223344556',
            'o1_sjediste': 'Heinzelova 33, 10000 Zagreb',
            'o2_ime': 'DEF d.o.o.',
            'o2_oib': '66554433221',
            'o2_sjediste': 'Radnička 47, 10000 Zagreb',
        },
    },
    'opomena': {
        'opis': 'Opomena pred tužbu za nepodmireni račun',
        'stranke': {
            'op_ime': 'Ivan Horvat',
            'op_oib': '12345678903',
            'op_adresa': 'Savska 25, 10000 Zagreb',
        },
        'podaci': {
            'glavnica': 3500.0,
            'opis': 'Pozivamo Vas da u roku od 8 dana od primitka ove opomene podmiriite dugovanje u iznosu od 3.500,00 EUR po osnovi računa br. R-123/2024 od 01.02.2024., u protivnom ćemo bez daljnjeg upozorenja pokrenuti ovršni postupak.',
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
            'clanak_kz': 'čl. 236. st. 1. KZ (Prijevara)',
            'osumnjicenik': 'Petar Babić, Draškovićeva 12, Zagreb, OIB: 99887766554',
        },
        'opis_djela': [
            {'tekst': 'Dana 10.01.2025. osumnjičenik je prijaviteljici lažno predstavio da prodaje rabljeni automobil marke VW Golf, reg. oznake ZG-1234-AB, te da je vozilo u ispravnom tehničkom stanju.',
             'dokaz': 'Oglas na njuskalo.hr (screenshot), WhatsApp prepiska'},
            {'tekst': 'Prijaviteljica je na temelju lažnih navoda osumnjičeniku uplatila kupoprodajnu cijenu od 8.500,00 EUR na IBAN HR1234567890123456789.',
             'dokaz': 'Potvrda o uplati od 11.01.2025.'},
            {'tekst': 'Nakon uplate, osumnjičenik je prestao odgovarati na pozive i poruke, a vozilo nikada nije predano prijaviteljici.',
             'dokaz': 'Evidencija poziva, WhatsApp poruke (screenshot)'},
        ],
    },
    'zalba_zup': {
        'opis': 'Žalba na rješenje o odbijanju zahtjeva (ZUP)',
        'podaci': {
            'prvostupanjsko_tijelo': 'Upravni odjel za komunalno gospodarstvo Grada Zagreba',
            'drugostupanjsko_tijelo': 'Ministarstvo prostornoga uređenja, graditeljstva i državne imovine',
            'klasa': 'UP/I-361-01/24-01/123',
            'urbroj': '251-13-11/2-24-5',
        },
        'razlozi': [
            {'tekst': 'Prvostupanjsko tijelo nije pravilno primijenilo čl. 136. Zakona o gradnji jer je odbilo zahtjev za izdavanje građevinske dozvole bez navođenja konkretnih nedostataka projektne dokumentacije.',
             'dokaz': 'Rješenje KLASA: UP/I-361-01/24-01/123 od 15.01.2025.'},
            {'tekst': 'Stranka nije saslušana u postupku čime je povrijeđeno pravo na saslušanje stranke iz čl. 30. ZUP-a.',
             'dokaz': 'Spis predmeta - nedostaje zapisnik o saslušanju'},
        ],
    },
}


def napuni_primjerom(tip_dokumenta, key_prefix=""):
    """Prikazuje gumb 'Napuni primjerom' i vraca dict s primjerom ili None."""
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
            for k, v in primjer.get('stranke', {}).items():
                full_key = f"{key_prefix}_{k}" if key_prefix else k
                st.session_state[full_key] = v
            for k, v in primjer.get('podaci', {}).items():
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
