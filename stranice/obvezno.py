# -----------------------------------------------------------------------------
# STRANICA: Obvezno pravo
# -----------------------------------------------------------------------------
import streamlit as st
from datetime import date
from pomocne import unos_stranke, zaglavlje_sastavljaca, prikazi_dokument, doc_selectbox
from generatori.obvezno import (
    generiraj_darovanje,
    generiraj_cesiju,
    generiraj_kompenzaciju,
    generiraj_jamstvo,
    generiraj_ugovor_o_gradenju,
    generiraj_licenciju,
    generiraj_posredovanje,
    generiraj_sporazumni_raskid,
)


def _render_darovanje():
    """Ugovor o darovanju - ZOO čl. 479-498."""
    st.subheader("Ugovor o darovanju")

    with st.expander("Pregled strukture dokumenta", expanded=False):
        st.markdown("""
**Dokument će sadržavati:**
- Zaglavlje — darovatelj i obdarenik
- Čl. 1. — Predmet darovanja (opis, vrsta: nekretnina / pokretnina / obećanje)
- Čl. 2. — Zemljišnoknjižni podaci (za nekretnine)
- Čl. 3. — Clausula intabulandi / Predaja (ovisno o vrsti predmeta)
- Čl. 4. — Pravo doživotnog uživanja (ako je odabrano)
- Čl. 5. — Jamstvo za pravne nedostatke
- Čl. 6. — Opoziv darovanja (ZOO čl. 490-498)
- Čl. 7. — Završne odredbe (javnobilježnička forma, primjerci)
- Potpisi stranaka
        """)

    s1, _, _ = unos_stranke("DAROVATELJ", "dar_s1")
    s2, _, _ = unos_stranke("OBDARENIK", "dar_s2")

    st.markdown("---")
    predmet_tip = st.selectbox(
        "Vrsta predmeta darovanja",
        ["nekretnina", "pokretnina_s_predajom", "obećanje_darovanja"],
        key="dar_predmet_tip",
        help="Za nekretnine je potreban javnobilježnički akt (čl. 482. ZOO). Obećanje darovanja mora biti u pisanom obliku."
    )
    predmet_opis = st.text_area(
        "Opis predmeta darovanja",
        key="dar_predmet_opis",
        placeholder="Opišite predmet darovanja...",
        help="Detaljno opišite što se daruje - za nekretnine navedite adresu i podatke iz ZK."
    )
    vrijednost = st.number_input(
        "Vrijednost predmeta (EUR)",
        min_value=0.0,
        key="dar_vrijednost",
        help="Procijenjena tržišna vrijednost. Bitna za porez na promet nekretnina (3%) i eventualni opoziv darovanja."
    )

    podaci_nekretnina = {}
    if predmet_tip == "nekretnina":
        st.markdown("**Podaci o nekretnini**")
        c1, c2 = st.columns(2)
        podaci_nekretnina['ko'] = c1.text_input(
            "Katastarska općina", key="dar_ko"
        )
        podaci_nekretnina['ulozak'] = c2.text_input(
            "Zemljišnoknjižni uložak", key="dar_ulozak"
        )
        podaci_nekretnina['cestica'] = c1.text_input(
            "Čestica", key="dar_cestica"
        )
        podaci_nekretnina['povrsina'] = c2.text_input(
            "Površina", key="dar_povrsina"
        )
        podaci_nekretnina['opis'] = st.text_area(
            "Opis nekretnine", key="dar_opis_nekretnine",
            placeholder="Npr. stan, kuća, zemljište...",
        )

    dozivotno_uzivanje = st.checkbox(
        "Pravo doživotnog uživanja", key="dar_dozivotno"
    )
    mjesto = st.text_input("Mjesto sklapanja", "Zagreb", key="dar_mjesto")

    st.markdown("---")
    if st.button("Generiraj ugovor o darovanju", type="primary", key="dar_btn"):
        podaci = {
            'predmet_tip': predmet_tip,
            'predmet_opis': predmet_opis,
            'vrijednost': vrijednost,
            'dozivotno_uzivanje': dozivotno_uzivanje,
            'mjesto': mjesto,
        }
        if predmet_tip == "nekretnina":
            podaci.update(podaci_nekretnina)
        doc = generiraj_darovanje(s1, s2, podaci)
        prikazi_dokument(doc, "Ugovor_o_darovanju.docx", "Preuzmi dokument")


def _render_cesija():
    """Ugovor o cesiji (ustupanju tražbine) - ZOO čl. 80-89."""
    st.subheader("Ugovor o cesiji")

    s1, _, _ = unos_stranke("CEDENT", "ces_s1")
    s2, _, _ = unos_stranke("CESIONAR", "ces_s2")

    st.markdown("---")
    iznos_trazbine = st.number_input(
        "Iznos tražbine (EUR)", min_value=0.0, key="ces_iznos"
    )
    opis_trazbine = st.text_area(
        "Opis tražbine", key="ces_opis",
        placeholder="Opišite tražbinu koja se ustupa...",
    )
    duznik_naziv = st.text_input(
        "Naziv dužnika", key="ces_duznik",
        placeholder="Ime/naziv osobe koja duguje...",
    )
    pravni_temelj = st.text_input(
        "Pravni temelj tražbine", key="ces_temelj",
        placeholder="Npr. Ugovor o kupoprodaji od 01.01.2025.",
    )

    c1, c2 = st.columns(2)
    jamstvo_veritet = c1.checkbox("Jamstvo za veritet (postojanje)", key="ces_veritet")
    jamstvo_bonitet = c2.checkbox("Jamstvo za bonitet (naplativost)", key="ces_bonitet")
    notifikacija_duznika = st.checkbox(
        "Notifikacija dužnika o cesiji", key="ces_notif"
    )

    naknada = st.number_input(
        "Naknada za ustupanje (EUR)", min_value=0.0, key="ces_naknada"
    )
    mjesto = st.text_input("Mjesto sklapanja", "Zagreb", key="ces_mjesto")

    st.markdown("---")
    if st.button("Generiraj ugovor o cesiji", type="primary", key="ces_btn"):
        podaci = {
            'iznos_trazbine': iznos_trazbine,
            'opis_trazbine': opis_trazbine,
            'duznik_naziv': duznik_naziv,
            'pravni_temelj': pravni_temelj,
            'jamstvo_veritet': jamstvo_veritet,
            'jamstvo_bonitet': jamstvo_bonitet,
            'notifikacija_duznika': notifikacija_duznika,
            'naknada': naknada,
            'mjesto': mjesto,
        }
        doc = generiraj_cesiju(s1, s2, podaci)
        prikazi_dokument(doc, "Ugovor_o_cesiji.docx", "Preuzmi dokument")


def _render_kompenzacija():
    """Ugovor o kompenzaciji (prebijanju) - ZOO čl. 195-202."""
    st.subheader("Ugovor o kompenzaciji")

    s1, _, _ = unos_stranke("STRANA A", "komp_s1")
    s2, _, _ = unos_stranke("STRANA B", "komp_s2")

    # Inicijalizacija dinamickih listi
    if 'komp_obveze_a' not in st.session_state:
        st.session_state.komp_obveze_a = [{'opis': '', 'iznos': 0.0}]
    if 'komp_obveze_b' not in st.session_state:
        st.session_state.komp_obveze_b = [{'opis': '', 'iznos': 0.0}]

    st.markdown("---")
    st.markdown("**Obveze strane A prema strani B**")
    for i, obveza in enumerate(st.session_state.komp_obveze_a):
        c1, c2 = st.columns([3, 1])
        st.session_state.komp_obveze_a[i]['opis'] = c1.text_input(
            f"Opis obveze A-{i+1}", value=obveza['opis'], key=f"komp_oa_opis_{i}"
        )
        st.session_state.komp_obveze_a[i]['iznos'] = c2.number_input(
            f"Iznos (EUR)", value=obveza['iznos'], min_value=0.0, key=f"komp_oa_iznos_{i}"
        )
    if st.button("Dodaj obvezu strane A", key="komp_add_a"):
        st.session_state.komp_obveze_a.append({'opis': '', 'iznos': 0.0})
        st.rerun()

    st.markdown("**Obveze strane B prema strani A**")
    for i, obveza in enumerate(st.session_state.komp_obveze_b):
        c1, c2 = st.columns([3, 1])
        st.session_state.komp_obveze_b[i]['opis'] = c1.text_input(
            f"Opis obveze B-{i+1}", value=obveza['opis'], key=f"komp_ob_opis_{i}"
        )
        st.session_state.komp_obveze_b[i]['iznos'] = c2.number_input(
            f"Iznos (EUR)", value=obveza['iznos'], min_value=0.0, key=f"komp_ob_iznos_{i}"
        )
    if st.button("Dodaj obvezu strane B", key="komp_add_b"):
        st.session_state.komp_obveze_b.append({'opis': '', 'iznos': 0.0})
        st.rerun()

    mjesto = st.text_input("Mjesto sklapanja", "Zagreb", key="komp_mjesto")

    st.markdown("---")
    if st.button("Generiraj ugovor o kompenzaciji", type="primary", key="komp_btn"):
        podaci = {
            'obveze_a': [o for o in st.session_state.komp_obveze_a if o['opis'].strip()],
            'obveze_b': [o for o in st.session_state.komp_obveze_b if o['opis'].strip()],
            'mjesto': mjesto,
        }
        doc = generiraj_kompenzaciju(s1, s2, podaci)
        prikazi_dokument(doc, "Ugovor_o_kompenzaciji.docx", "Preuzmi dokument")


def _render_jamstvo():
    """Ugovor o jamstvu - ZOO čl. 104-126."""
    st.subheader("Ugovor o jamstvu")

    s1, _, _ = unos_stranke("VJEROVNIK", "jam_s1")
    s2, _, _ = unos_stranke("JAMAC", "jam_s2")

    st.markdown("---")
    vrsta = st.radio(
        "Vrsta jamstva",
        ["jamac_platac", "obicno"],
        format_func=lambda x: "Jamac platac" if x == "jamac_platac" else "Obično jamstvo",
        key="jam_vrsta",
    )
    glavni_duznik_tekst = st.text_input(
        "Glavni dužnik (naziv/ime)", key="jam_duznik",
        placeholder="Unesite podatke o glavnom dužniku...",
    )
    opis_obveze = st.text_area(
        "Opis obveze za koju se jamči", key="jam_opis",
        placeholder="Opišite obvezu glavnog dužnika...",
    )
    iznos_obveze = st.number_input(
        "Iznos obveze (EUR)", min_value=0.0, key="jam_iznos"
    )
    rok_jamstva = st.text_input(
        "Rok trajanja jamstva", key="jam_rok",
        placeholder="Npr. do potpune isplate, 2 godine...",
    )
    mjesto = st.text_input("Mjesto sklapanja", "Zagreb", key="jam_mjesto")

    st.markdown("---")
    if st.button("Generiraj ugovor o jamstvu", type="primary", key="jam_btn"):
        podaci = {
            'vrsta': vrsta,
            'glavni_duznik_tekst': glavni_duznik_tekst,
            'opis_obveze': opis_obveze,
            'iznos_obveze': iznos_obveze,
            'rok_jamstva': rok_jamstva,
            'mjesto': mjesto,
        }
        doc = generiraj_jamstvo(s1, s2, podaci)
        prikazi_dokument(doc, "Ugovor_o_jamstvu.docx", "Preuzmi dokument")


def _render_gradenje():
    """Ugovor o građenju - ZOO čl. 620-636."""
    st.subheader("Ugovor o građenju")

    s1, _, _ = unos_stranke("NARUČITELJ", "grad_s1")
    s2, _, _ = unos_stranke("IZVOĐAČ", "grad_s2")

    st.markdown("---")
    predmet_radova = st.text_area(
        "Predmet radova", key="grad_predmet",
        placeholder="Opišite građevinske radove...",
    )
    lokacija = st.text_input(
        "Lokacija izvođenja radova", key="grad_lokacija",
        placeholder="Adresa ili opis lokacije...",
    )

    c1, c2 = st.columns(2)
    cijena = c1.number_input(
        "Cijena radova (EUR)", min_value=0.0, key="grad_cijena"
    )
    cijena_tip = c2.selectbox(
        "Tip cijene",
        ["ključ_u_ruke", "jedinicna_cijena"],
        format_func=lambda x: "Ključ u ruke" if x == "ključ_u_ruke" else "Jedinična cijena",
        key="grad_cijena_tip",
    )

    c3, c4 = st.columns(2)
    rok_izvedbe = c3.text_input(
        "Rok izvedbe", key="grad_rok",
        placeholder="Npr. 6 mjeseci od potpisa...",
    )
    jamstveni_rok = c4.text_input(
        "Jamstveni rok", "2 godine", key="grad_jamstveni_rok"
    )

    ugovorna_kazna_postotak = st.number_input(
        "Ugovorna kazna za kašnjenje (%)", min_value=0.0, value=1.0,
        key="grad_kazna",
    )
    mjesto = st.text_input("Mjesto sklapanja", "Zagreb", key="grad_mjesto")

    st.markdown("---")
    if st.button("Generiraj ugovor o građenju", type="primary", key="grad_btn"):
        podaci = {
            'predmet_radova': predmet_radova,
            'lokacija': lokacija,
            'cijena': cijena,
            'cijena_tip': cijena_tip,
            'rok_izvedbe': rok_izvedbe,
            'jamstveni_rok': jamstveni_rok,
            'ugovorna_kazna_postotak': ugovorna_kazna_postotak,
            'mjesto': mjesto,
        }
        doc = generiraj_ugovor_o_gradenju(s1, s2, podaci)
        prikazi_dokument(doc, "Ugovor_o_gradenju.docx", "Preuzmi dokument")


def _render_licencija():
    """Licencni ugovor - ZOO čl. 699-724."""
    st.subheader("Licencni ugovor")

    s1, _, _ = unos_stranke("DAVATELJ LICENCIJE", "lic_s1")
    s2, _, _ = unos_stranke("STJECATELJ LICENCIJE", "lic_s2")

    st.markdown("---")
    predmet_licencije = st.text_area(
        "Predmet licencije", key="lic_predmet",
        placeholder="Opišite predmet licencije (patent, know-how, žig...)...",
    )
    vrsta_licencije = st.radio(
        "Vrsta licencije",
        ["isključiva", "neisključiva"],
        format_func=lambda x: "Isključiva" if x == "isključiva" else "Neisključiva",
        key="lic_vrsta",
    )
    teritorij = st.text_input(
        "Teritorij", "Republika Hrvatska", key="lic_teritorij"
    )
    trajanje = st.text_input(
        "Trajanje licencije", key="lic_trajanje",
        placeholder="Npr. 5 godina, neodređeno...",
    )

    naknada_tip = st.selectbox(
        "Tip naknade",
        ["royalty", "pausalni"],
        format_func=lambda x: "Royalty (postotak)" if x == "royalty" else "Paušalni iznos",
        key="lic_naknada_tip",
    )
    naknada_iznos = st.number_input(
        "Iznos naknade (EUR)", min_value=0.0, key="lic_naknada_iznos"
    )
    royalty_postotak = 0.0
    if naknada_tip == "royalty":
        royalty_postotak = st.number_input(
            "Royalty postotak (%)", min_value=0.0, key="lic_royalty"
        )

    mjesto = st.text_input("Mjesto sklapanja", "Zagreb", key="lic_mjesto")

    st.markdown("---")
    if st.button("Generiraj licencni ugovor", type="primary", key="lic_btn"):
        podaci = {
            'predmet_licencije': predmet_licencije,
            'vrsta_licencije': vrsta_licencije,
            'teritorij': teritorij,
            'trajanje': trajanje,
            'naknada_tip': naknada_tip,
            'naknada_iznos': naknada_iznos,
            'royalty_postotak': royalty_postotak,
            'mjesto': mjesto,
        }
        doc = generiraj_licenciju(s1, s2, podaci)
        prikazi_dokument(doc, "Licencni_ugovor.docx", "Preuzmi dokument")


def _render_posredovanje():
    """Ugovor o posredovanju - ZOO čl. 835-848."""
    st.subheader("Ugovor o posredovanju")

    s1, _, _ = unos_stranke("POSREDNIK", "pos_s1")
    s2, _, _ = unos_stranke("NALOGODAVAC", "pos_s2")

    st.markdown("---")
    predmet_posredovanja = st.text_area(
        "Predmet posredovanja", key="pos_predmet",
        placeholder="Opišite posao za koji se posreduje...",
    )
    ekskluziva = st.checkbox(
        "Ekskluzivno posredovanje", key="pos_ekskluziva"
    )
    provizija_postotak = st.number_input(
        "Provizija (%)", min_value=0.0, key="pos_provizija"
    )
    trajanje = st.text_input(
        "Trajanje ugovora", key="pos_trajanje",
        placeholder="Npr. 12 mjeseci...",
    )
    mjesto = st.text_input("Mjesto sklapanja", "Zagreb", key="pos_mjesto")

    st.markdown("---")
    if st.button("Generiraj ugovor o posredovanju", type="primary", key="pos_btn"):
        podaci = {
            'predmet_posredovanja': predmet_posredovanja,
            'ekskluziva': ekskluziva,
            'provizija_postotak': provizija_postotak,
            'trajanje': trajanje,
            'mjesto': mjesto,
        }
        doc = generiraj_posredovanje(s1, s2, podaci)
        prikazi_dokument(doc, "Ugovor_o_posredovanju.docx", "Preuzmi dokument")


def _render_sporazumni_raskid():
    """Sporazumni raskid ugovora - ZOO čl. 355."""
    st.subheader("Sporazumni raskid ugovora")

    s1, _, _ = unos_stranke("STRANA 1", "rask_s1")
    s2, _, _ = unos_stranke("STRANA 2", "rask_s2")

    st.markdown("---")
    naziv_izvornog_ugovora = st.text_input(
        "Naziv izvornog ugovora", key="rask_naziv",
        placeholder="Npr. Ugovor o kupoprodaji...",
    )
    datum_izvornog_ugovora = st.date_input(
        "Datum izvornog ugovora", key="rask_datum"
    )
    forma_izvornog = st.selectbox(
        "Forma izvornog ugovora",
        ["pisana", "javnobilježnička"],
        format_func=lambda x: "Pisana forma" if x == "pisana" else "Javnobilježnička forma",
        key="rask_forma",
    )
    razlog_raskida = st.text_area(
        "Razlog raskida", key="rask_razlog",
        placeholder="Opišite razlog sporazumnog raskida...",
    )
    ucinak = st.radio(
        "Učinak raskida",
        ["ex_nunc", "ex_tunc"],
        format_func=lambda x: "Ex nunc (ubuduće)" if x == "ex_nunc" else "Ex tunc (od početka)",
        key="rask_ucinak",
    )
    obveze_vracanja = st.text_area(
        "Obveze vraćanja", key="rask_vracanja",
        placeholder="Opišite što stranke trebaju vratiti jedna drugoj...",
    )
    mjesto = st.text_input("Mjesto sklapanja", "Zagreb", key="rask_mjesto")

    st.markdown("---")
    if st.button("Generiraj sporazumni raskid", type="primary", key="rask_btn"):
        podaci = {
            'naziv_izvornog_ugovora': naziv_izvornog_ugovora,
            'datum_izvornog_ugovora': datum_izvornog_ugovora.strftime('%d.%m.%Y.'),
            'forma_izvornog': forma_izvornog,
            'razlog_raskida': razlog_raskida,
            'ucinak': ucinak,
            'obveze_vracanja': obveze_vracanja,
            'mjesto': mjesto,
        }
        doc = generiraj_sporazumni_raskid(s1, s2, podaci)
        prikazi_dokument(doc, "Sporazumni_raskid.docx", "Preuzmi dokument")


def render_obvezno():
    """Glavna render funkcija za modul Obvezno pravo."""
    st.header("Obvezno pravo")

    zaglavlje_sastavljaca()

    tip_dokumenta = doc_selectbox(
        "Odaberite vrstu dokumenta",
        [
            "Ugovor o darovanju",
            "Ugovor o cesiji",
            "Ugovor o kompenzaciji",
            "Ugovor o jamstvu",
            "Ugovor o građenju",
            "Licencni ugovor",
            "Ugovor o posredovanju",
            "Sporazumni raskid ugovora",
        ],
        key="obvezno_tip",
    )

    if tip_dokumenta == "Ugovor o darovanju":
        _render_darovanje()
    elif tip_dokumenta == "Ugovor o cesiji":
        _render_cesija()
    elif tip_dokumenta == "Ugovor o kompenzaciji":
        _render_kompenzacija()
    elif tip_dokumenta == "Ugovor o jamstvu":
        _render_jamstvo()
    elif tip_dokumenta == "Ugovor o građenju":
        _render_gradenje()
    elif tip_dokumenta == "Licencni ugovor":
        _render_licencija()
    elif tip_dokumenta == "Ugovor o posredovanju":
        _render_posredovanje()
    elif tip_dokumenta == "Sporazumni raskid ugovora":
        _render_sporazumni_raskid()
