# -----------------------------------------------------------------------------
# STRANICA: Obvezno pravo
# -----------------------------------------------------------------------------
import streamlit as st
from datetime import date
from pomocne import unos_stranke, zaglavlje_sastavljaca, prikazi_dokument, doc_selectbox, audit_kwargs, napuni_primjerom
from generatori.obvezno import (
    generiraj_darovanje,
    generiraj_cesiju,
    generiraj_kompenzaciju,
    generiraj_jamstvo,
    generiraj_ugovor_o_gradenju,
    generiraj_licenciju,
    generiraj_posredovanje,
    generiraj_sporazumni_raskid,
    generiraj_predugovor,
    generiraj_raskid_najma,
    generiraj_raskid_ugovora_djelu,
    generiraj_raskid_kupoprodaje,
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
        audit_input = {"darovatelj_html": s1, "obdarenik_html": s2, "podaci": podaci}
        prikazi_dokument(doc, "Ugovor_o_darovanju.docx", "Preuzmi dokument",
                         **audit_kwargs("darovanje", audit_input, "obvezno"))


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
        audit_input = {"cedent_html": s1, "cesionar_html": s2, "podaci": podaci}
        prikazi_dokument(doc, "Ugovor_o_cesiji.docx", "Preuzmi dokument",
                         **audit_kwargs("cesija", audit_input, "obvezno"))


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
        audit_input = {"strana_a_html": s1, "strana_b_html": s2, "podaci": podaci}
        prikazi_dokument(doc, "Ugovor_o_kompenzaciji.docx", "Preuzmi dokument",
                         **audit_kwargs("kompenzacija", audit_input, "obvezno"))


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
        audit_input = {"vjerovnik_html": s1, "jamac_html": s2, "podaci": podaci}
        prikazi_dokument(doc, "Ugovor_o_jamstvu.docx", "Preuzmi dokument",
                         **audit_kwargs(f"jamstvo_{vrsta}", audit_input, "obvezno"))


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
        audit_input = {"narucitelj_html": s1, "izvodac_html": s2, "podaci": podaci}
        prikazi_dokument(doc, "Ugovor_o_gradenju.docx", "Preuzmi dokument",
                         **audit_kwargs("ugovor_gradenje", audit_input, "obvezno"))


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
        audit_input = {"davatelj_html": s1, "stjecatelj_html": s2, "podaci": podaci}
        prikazi_dokument(doc, "Licencni_ugovor.docx", "Preuzmi dokument",
                         **audit_kwargs("licencija", audit_input, "obvezno"))


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
        audit_input = {"posrednik_html": s1, "nalogodavac_html": s2, "podaci": podaci}
        prikazi_dokument(doc, "Ugovor_o_posredovanju.docx", "Preuzmi dokument",
                         **audit_kwargs("posredovanje", audit_input, "obvezno"))


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
        audit_input = {"strana1_html": s1, "strana2_html": s2, "podaci": podaci}
        prikazi_dokument(doc, "Sporazumni_raskid.docx", "Preuzmi dokument",
                         **audit_kwargs("sporazumni_raskid", audit_input, "obvezno"))


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
            "Predugovor",
            "Raskid ugovora o najmu",
            "Raskid ugovora o djelu",
            "Raskid kupoprodaje (zbog neispunjenja)",
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
    elif tip_dokumenta == "Predugovor":
        _render_predugovor()
    elif tip_dokumenta == "Raskid ugovora o najmu":
        _render_raskid_najma()
    elif tip_dokumenta == "Raskid ugovora o djelu":
        _render_raskid_djelo()
    elif tip_dokumenta == "Raskid kupoprodaje (zbog neispunjenja)":
        _render_raskid_kupoprodaje()


def _render_predugovor():
    """Predugovor — ZOO čl. 268."""
    st.subheader("Predugovor")
    st.caption("ZOO čl. 268 — obveza sklapanja glavnog ugovora u dogovorenom roku.")
    napuni_primjerom('predugovor', '')

    s1, _, _ = unos_stranke("1. STRANA (budući prodavatelj/davatelj)", "pred_s1")
    s2, _, _ = unos_stranke("2. STRANA (budući kupac/primatelj)", "pred_s2")

    col1, col2 = st.columns(2)
    with col1:
        vrsta = st.selectbox(
            "Vrsta glavnog ugovora",
            ["kupoprodajni ugovor", "ugovor o najmu", "ugovor o djelu", "ugovor o radu", "ostalo"],
            key="pred_vrsta",
        )
        cijena = st.number_input("Cijena/vrijednost (EUR)", 0.0, step=1000.0, key="pred_cij")
        kapara = st.number_input("Kapara (EUR, opcionalno)", 0.0, step=100.0, key="pred_kap")
    with col2:
        rok = st.text_input("Rok za sklapanje glavnog ugovora", placeholder="npr. 01.07.2026.", key="pred_rok")
        forma = st.text_input("Forma glavnog ugovora", "pisana, s ovjerom potpisa kod javnog bilježnika", key="pred_for")
        mjesto = st.text_input("Mjesto sklapanja", "Zagreb", key="pred_mj")

    predmet = st.text_area(
        "Predmet budućeg glavnog ugovora",
        placeholder="npr. Stan na adresi Ilica 100, Zagreb, površine 65 m², k.č. 1234/5, k.o. Centar, zk.ul. 5678",
        height=100, key="pred_pre",
    )
    bitni = st.text_area(
        "Bitni uvjeti (opcionalno)",
        placeholder="Dodatni bitni uvjeti glavnog ugovora",
        height=80, key="pred_bit",
    )

    if st.button("Generiraj predugovor", type="primary"):
        podaci = {
            'vrsta_glavnog_ugovora': vrsta, 'predmet': predmet,
            'cijena_eur': cijena, 'kapara_eur': kapara,
            'rok_sklapanja_glavnog': rok, 'bitni_uvjeti': bitni,
            'forma_glavnog': forma, 'mjesto': mjesto,
        }
        doc = generiraj_predugovor(s1, s2, podaci)
        audit_input = {"strana1_html": s1, "strana2_html": s2, "podaci": podaci}
        prikazi_dokument(doc, "Predugovor.docx", "Preuzmi predugovor",
                         **audit_kwargs("predugovor", audit_input, "obvezno"))


def _render_raskid_najma():
    """Raskid ugovora o najmu — ZOO čl. 552-558."""
    st.subheader("Raskid ugovora o najmu")
    st.caption("ZOO čl. 552-558. Razlikuj redoviti otkaz (s rokom) i izvanredni raskid (zbog neispunjenja, npr. neplaćanje 2+ mjeseca).")
    napuni_primjerom('raskid_najma', '')

    najmodavac, _, _ = unos_stranke("NAJMODAVAC", "rn_nd")
    najmoprimac, _, _ = unos_stranke("NAJMOPRIMAC", "rn_np")

    vrsta = st.radio(
        "Vrsta raskida",
        ["redoviti", "izvanredni"],
        format_func=lambda x: "Redoviti otkaz (s otkaznim rokom)" if x == "redoviti" else "Izvanredni raskid (bez roka — zbog neispunjenja)",
        key="rn_vrsta",
    )

    col1, col2 = st.columns(2)
    with col1:
        ugovor_datum = st.text_input("Datum sklapanja ugovora o najmu", placeholder="dd.mm.yyyy.", key="rn_ud")
        adresa = st.text_input("Adresa nekretnine", key="rn_adr")
        mjesto = st.text_input("Mjesto", "Zagreb", key="rn_mj")
    with col2:
        if vrsta == "redoviti":
            rok = st.text_input("Otkazni rok", "30 dana", key="rn_rok")
            datum_iseljenja = st.text_input("Datum predaje nekretnine (opcionalno)", placeholder="ostavi prazno za 'po isteku roka'", key="rn_di_red")
            razlog = ""
            zaostala = 0.0
        else:
            rok = ""
            datum_iseljenja = st.text_input("Rok za iseljenje", "8 dana od primitka raskida", key="rn_di_izv")
            zaostala = st.number_input("Zaostala najamnina (EUR, opcionalno)", 0.0, step=100.0, key="rn_zao")
            razlog = ""

    if vrsta == "izvanredni":
        razlog = st.text_area(
            "Razlog izvanrednog raskida",
            placeholder="npr. Najmoprimac nije plaćao najamninu za mjesece veljača, ožujak i travanj 2026. godine, unatoč pisanim opomenama od dd.mm.yyyy.",
            height=100, key="rn_raz",
        )

    if st.button("Generiraj otkaz/raskid", type="primary"):
        podaci = {
            'vrsta_raskida': vrsta,
            'ugovor_datum': ugovor_datum,
            'adresa_najma': adresa,
            'otkazni_rok': rok,
            'razlog_izvanredni': razlog,
            'datum_iseljenja': datum_iseljenja,
            'zaostala_najamnina_eur': zaostala,
            'mjesto': mjesto,
        }
        doc = generiraj_raskid_najma(najmodavac, najmoprimac, podaci)
        naziv = "Izvanredni_raskid_najma.docx" if vrsta == "izvanredni" else "Otkaz_najma.docx"
        audit_input = {"najmodavac_html": najmodavac, "najmoprimac_html": najmoprimac, "podaci": podaci}
        prikazi_dokument(doc, naziv, "Preuzmi dokument",
                         **audit_kwargs(f"raskid_najma_{vrsta}", audit_input, "obvezno"))


def _render_raskid_djelo():
    """Raskid ugovora o djelu — ZOO čl. 633."""
    st.subheader("Raskid ugovora o djelu")
    st.caption("ZOO čl. 633 — naručitelj uvijek može raskinuti ugovor; obvezan je platiti izvršeni rad i razumno obeštećenje.")
    napuni_primjerom('raskid_djelo', '')

    narucitelj, _, _ = unos_stranke("NARUČITELJ", "rd_nar")
    izvodac, _, _ = unos_stranke("IZVOĐAČ", "rd_izv")

    col1, col2 = st.columns(2)
    with col1:
        ugovor_datum = st.text_input("Datum sklapanja ugovora o djelu", placeholder="dd.mm.yyyy.", key="rd_ud")
        ponuda = st.number_input("Ponuda naknade za izvršeni rad (EUR)", 0.0, step=100.0, key="rd_pon")
    with col2:
        mjesto = st.text_input("Mjesto", "Zagreb", key="rd_mj")
        razlog = st.text_input("Razlog raskida (opcionalno)", placeholder="npr. promjena okolnosti naručitelja", key="rd_raz")

    opis = st.text_area(
        "Opis djela",
        placeholder="npr. Izrada drvene terase 30 m² na adresi Ilica 1, Zagreb, prema specifikaciji od dd.mm.yyyy.",
        height=80, key="rd_opi",
    )
    izvrseno = st.text_area(
        "Što je izvršeno do dana raskida (opcionalno)",
        placeholder="npr. Postavljena nosiva konstrukcija, isporučen materijal za podnu oblogu (50%)",
        height=80, key="rd_izv_o",
    )

    if st.button("Generiraj raskid", type="primary"):
        podaci = {
            'ugovor_datum': ugovor_datum, 'opis_djela': opis,
            'razlog_raskida': razlog, 'izvrseno_dio': izvrseno,
            'ponuda_naknade_eur': ponuda, 'mjesto': mjesto,
        }
        doc = generiraj_raskid_ugovora_djelu(narucitelj, izvodac, podaci)
        audit_input = {"narucitelj_html": narucitelj, "izvodac_html": izvodac, "podaci": podaci}
        prikazi_dokument(doc, "Raskid_ugovora_o_djelu.docx", "Preuzmi raskid",
                         **audit_kwargs("raskid_djelo", audit_input, "obvezno"))


def _render_raskid_kupoprodaje():
    """Raskid kupoprodaje zbog neispunjenja — ZOO čl. 360-368."""
    st.subheader("Raskid kupoprodaje (zbog neispunjenja)")
    st.caption("ZOO čl. 360-368. Tri tipa razloga: neplaćanje cijene (raskida prodavatelj), nepredaja stvari (raskida kupac), materijalni nedostaci (kupac, čl. 410).")
    napuni_primjerom('raskid_kupoprodaje', '')

    prodavatelj, _, _ = unos_stranke("PRODAVATELJ", "rk_pro")
    kupac, _, _ = unos_stranke("KUPAC", "rk_kup")

    razlog_tip = st.selectbox(
        "Razlog raskida",
        ["neplacanje", "nepredaja", "nedostaci"],
        format_func=lambda x: {
            "neplacanje": "Kupac nije platio cijenu (raskida prodavatelj)",
            "nepredaja": "Prodavatelj nije predao stvar (raskida kupac)",
            "nedostaci": "Materijalni nedostaci stvari (raskida kupac, čl. 410)",
        }[x],
        key="rk_tip",
    )

    col1, col2 = st.columns(2)
    with col1:
        ugovor_datum = st.text_input("Datum sklapanja ugovora", placeholder="dd.mm.yyyy.", key="rk_ud")
        cijena = st.number_input("Kupoprodajna cijena (EUR)", 0.0, step=100.0, key="rk_cij")
        mjesto = st.text_input("Mjesto", "Zagreb", key="rk_mj")
    with col2:
        rok_ostavljen = st.text_input(
            "Datum kad je ostavljen naknadni rok (opcionalno)",
            placeholder="dd.mm.yyyy.",
            help="Ako je drugoj strani već ostavljen primjereni rok za ispunjenje (ZOO čl. 362), upiši datum.",
            key="rk_rok",
        )

    predmet = st.text_area("Predmet kupoprodaje", height=80, key="rk_pre")
    opis = st.text_area(
        "Opis neispunjenja",
        placeholder="npr. Kupac nije platio kupoprodajnu cijenu o roku 01.05.2026. unatoč opomeni od 10.05.2026.",
        height=100, key="rk_opi",
    )
    zahtjev_povrat = st.text_area(
        "Zahtjev za povrat (opcionalno)",
        placeholder="Specifični zahtjev za povrat stvari/cijene; ako prazno, koristi se default formulacija ZOO čl. 368.",
        height=80, key="rk_pov",
    )

    if st.button("Generiraj raskid", type="primary"):
        podaci = {
            'razlog_tip': razlog_tip, 'ugovor_datum': ugovor_datum,
            'predmet': predmet, 'opis_neispunjenja': opis,
            'cijena_eur': cijena, 'rok_ostavljen': rok_ostavljen,
            'zahtjev_povrat': zahtjev_povrat, 'mjesto': mjesto,
        }
        doc = generiraj_raskid_kupoprodaje(prodavatelj, kupac, podaci)
        audit_input = {"prodavatelj_html": prodavatelj, "kupac_html": kupac, "podaci": podaci}
        prikazi_dokument(doc, "Raskid_kupoprodaje.docx", "Preuzmi raskid",
                         **audit_kwargs(f"raskid_kupoprodaje_{razlog_tip}", audit_input, "obvezno"))
