# -----------------------------------------------------------------------------
# STRANICA: Kazneno pravo
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, prikazi_dokument, zaglavlje_sastavljaca, formatiraj_troskovnik, odabir_suda
from generatori.kazneno import (
    generiraj_kaznenu_prijavu,
    generiraj_privatnu_tuzbu,
    generiraj_zalbu_kaznena_presuda,
)


def _render_kaznena_prijava():
    """Kaznena prijava."""
    prijavitelj, _, _ = unos_stranke("PRIJAVITELJ", "kp_prij")

    st.subheader("Podaci o prijavi")
    nadlezno_tijelo = st.text_input(
        "Nadležno tijelo",
        value="DRŽAVNO ODVJETNIŠTVO REPUBLIKE HRVATSKE",
        key="kp_tijelo",
    )
    osumnjicenik_tekst = st.text_area(
        "Osumnjičenik (ime, adresa, OIB ako je poznat)",
        placeholder="Navesti podatke o osumnjičeniku...",
        key="kp_osumnjicenik",
        height=100,
    )
    clanak_kz = st.text_input(
        "Članak Kaznenog zakona",
        placeholder="čl. 228. st. 1. KZ",
        key="kp_clanak",
    )

    st.subheader("Opis kaznenog djela")
    opis_djela = st.text_area(
        "Opis djela",
        placeholder="Opišite okolnosti, vrijeme, mjesto i način počinjenja kaznenog djela...",
        key="kp_opis",
        height=200,
    )

    st.subheader("Dokazi")
    if "kp_dokazi" not in st.session_state:
        st.session_state.kp_dokazi = [""]

    for i, dokaz in enumerate(st.session_state.kp_dokazi):
        st.session_state.kp_dokazi[i] = st.text_input(
            f"Dokaz {i + 1}",
            value=dokaz,
            key=f"kp_dokaz_{i}",
        )

    if st.button("Dodaj dokaz", key="kp_dodaj_dokaz"):
        st.session_state.kp_dokazi.append("")
        st.rerun()

    mjesto = st.text_input("Mjesto", "Zagreb", key="kp_mjesto")

    st.markdown("---")

    if st.button("Generiraj kaznenu prijavu", type="primary", key="kp_btn"):
        dokazi_lista = [d for d in st.session_state.kp_dokazi if d.strip()]
        doc = generiraj_kaznenu_prijavu(
            prijavitelj,
            {
                'nadlezno_tijelo': nadlezno_tijelo,
                'osumnjicenik_tekst': osumnjicenik_tekst,
                'clanak_kz': clanak_kz,
                'opis_djela': opis_djela,
                'dokazi': dokazi_lista,
                'mjesto': mjesto,
            },
        )
        prikazi_dokument(doc, "Kaznena_prijava.docx", "Preuzmi dokument")


def _render_privatna_tuzba():
    """Privatna tužba."""
    st.warning(
        "Privatna tužba se podnosi u roku od **3 mjeseca** od dana kad je "
        "ovlašteni tužitelj saznao za kazneno djelo i počinitelja (čl. 60. KZ)."
    )

    col1, col2 = st.columns(2)
    with col1:
        tuzitelj, _, _ = unos_stranke("TUŽITELJ (privatni)", "pt_tuz")
    with col2:
        okrivljenik, _, _ = unos_stranke("OKRIVLJENIK", "pt_okr")

    st.subheader("Podaci o predmetu")
    sud = odabir_suda("Nadležni sud", vrsta="opcinski", key="pt_sud")
    clanak_kz = st.text_input(
        "Članak Kaznenog zakona",
        placeholder="čl. 148. st. 1. KZ",
        key="pt_clanak",
    )
    c1, c2 = st.columns(2)
    datum_djela = c1.date_input("Datum počinjenja djela", key="pt_datum")
    mjesto_djela = c2.text_input("Mjesto počinjenja djela", key="pt_mjesto_djela")

    st.subheader("Opis kaznenog djela")
    opis_djela = st.text_area(
        "Opis djela",
        placeholder="Opišite okolnosti kaznenog djela...",
        key="pt_opis",
        height=200,
    )

    st.subheader("Dokazi")
    if "pt_dokazi" not in st.session_state:
        st.session_state.pt_dokazi = [""]

    for i, dokaz in enumerate(st.session_state.pt_dokazi):
        st.session_state.pt_dokazi[i] = st.text_input(
            f"Dokaz {i + 1}",
            value=dokaz,
            key=f"pt_dokaz_{i}",
        )

    if st.button("Dodaj dokaz", key="pt_dodaj_dokaz"):
        st.session_state.pt_dokazi.append("")
        st.rerun()

    kazneni_zahtjev = st.text_area(
        "Kazneni zahtjev (prijedlog kazne)",
        placeholder="Predlažem da sud okrivljenika proglasi krivim i osudi na...",
        key="pt_zahtjev",
        height=100,
    )

    mjesto = st.text_input("Mjesto sastava", "Zagreb", key="pt_mjesto")

    st.subheader("Troškovnik")
    ct1, ct2 = st.columns(2)
    trosak_stavka = ct1.number_input("Sastav tužbe (EUR)", 0.0, key="pt_stavka")
    trosak_pdv = trosak_stavka * 0.25 if ct1.checkbox("Dodaj PDV (25%)", key="pt_pdv") else 0.0
    trosak_pristojba = ct2.number_input("Sudska pristojba (EUR)", 0.0, key="pt_pristojba")

    st.markdown("---")

    if st.button("Generiraj privatnu tužbu", type="primary", key="pt_btn"):
        dokazi_lista = [d for d in st.session_state.pt_dokazi if d.strip()]
        doc = generiraj_privatnu_tuzbu(
            tuzitelj,
            okrivljenik,
            {
                'sud': sud,
                'clanak_kz': clanak_kz,
                'datum_djela': datum_djela.strftime('%d.%m.%Y.'),
                'mjesto_djela': mjesto_djela,
                'opis_djela': opis_djela,
                'dokazi': dokazi_lista,
                'kazneni_zahtjev': kazneni_zahtjev,
                'mjesto': mjesto,
            },
            {
                'stavka': trosak_stavka,
                'pdv': trosak_pdv,
                'pristojba': trosak_pristojba,
            },
        )
        prikazi_dokument(doc, "Privatna_tuzba.docx", "Preuzmi dokument")


def _render_zalba_kaznena_presuda():
    """Žalba na kaznenu presudu."""
    st.warning(
        "Rok za žalbu na presudu u kaznenom postupku iznosi **15 dana** "
        "od dana dostave presude (čl. 464. ZKP)."
    )

    zalitelj, _, _ = unos_stranke("ŽALITELJ", "zkp_zal")

    st.subheader("Podaci o presudi")
    c1, c2 = st.columns(2)
    with c1:
        sud_prvostupanjski = odabir_suda("Prvostupanjski sud", vrsta="opcinski", key="zkp_sud1")
    with c2:
        sud_drugostupanjski = odabir_suda("Drugostupanjski sud", vrsta="zupanijski", key="zkp_sud2")
    c3, c4 = st.columns(2)
    poslovni_broj = c3.text_input("Poslovni broj presude", placeholder="K-000/2024", key="zkp_pbr")
    datum_presude = c4.text_input("Datum donošenja presude", placeholder="01.01.2024.", key="zkp_dat")

    izreka_presude = st.text_area(
        "Izreka presude (dispozitiv)",
        placeholder="Navedite sadržaj izreke presude koja se pobija...",
        key="zkp_izreka",
        height=150,
    )

    st.subheader("Žalbeni razlozi")
    razlozi = {}

    with st.expander("1. Bitna povreda odredaba kaznenog postupka (čl. 468. ZKP)"):
        r1_aktivan = st.checkbox("Pozivam se na ovaj razlog", key="zkp_r1_cb")
        razlozi['bitna_povreda'] = ""
        if r1_aktivan:
            razlozi['bitna_povreda'] = st.text_area(
                "Obrazloženje bitne povrede",
                placeholder="Opišite u čemu se sastoji bitna povreda odredaba kaznenog postupka...",
                key="zkp_r1_tekst",
                height=150,
            )

    with st.expander("2. Povreda kaznenog zakona (čl. 469. ZKP)"):
        r2_aktivan = st.checkbox("Pozivam se na ovaj razlog", key="zkp_r2_cb")
        razlozi['materijalni_zakon'] = ""
        if r2_aktivan:
            razlozi['materijalni_zakon'] = st.text_area(
                "Obrazloženje povrede kaznenog zakona",
                placeholder="Opišite u čemu se sastoji povreda kaznenog zakona...",
                key="zkp_r2_tekst",
                height=150,
            )

    with st.expander("3. Pogrešno ili nepotpuno utvrđeno činjenično stanje (čl. 470. ZKP)"):
        r3_aktivan = st.checkbox("Pozivam se na ovaj razlog", key="zkp_r3_cb")
        razlozi['cinjenicno_stanje'] = ""
        if r3_aktivan:
            razlozi['cinjenicno_stanje'] = st.text_area(
                "Obrazloženje pogrešno utvrđenog činjeničnog stanja",
                placeholder="Opišite što je sud pogrešno utvrdio...",
                key="zkp_r3_tekst",
                height=150,
            )

    with st.expander("4. Odluka o kaznenoj sankciji (čl. 471. ZKP)"):
        r4_aktivan = st.checkbox("Pozivam se na ovaj razlog", key="zkp_r4_cb")
        razlozi['odluka_o_kazni'] = ""
        if r4_aktivan:
            razlozi['odluka_o_kazni'] = st.text_area(
                "Obrazloženje odluke o kaznenoj sankciji",
                placeholder="Opišite zašto smatrate da je kazna neprimjerena...",
                key="zkp_r4_tekst",
                height=150,
            )

    st.subheader("Žalbeni prijedlog")
    zalbeni_prijedlog = st.selectbox(
        "Predlažem da drugostupanjski sud presudu:",
        ["preinači", "ukine i vrati"],
        key="zkp_prijedlog",
    )

    mjesto = st.text_input("Mjesto", "Zagreb", key="zkp_mjesto")

    st.subheader("Troškovnik")
    ct1, ct2 = st.columns(2)
    trosak_stavka = ct1.number_input("Sastav žalbe (EUR)", 0.0, key="zkp_stavka")
    trosak_pdv = trosak_stavka * 0.25 if ct1.checkbox("Dodaj PDV (25%)", key="zkp_pdv") else 0.0
    trosak_pristojba = ct2.number_input("Sudska pristojba (EUR)", 0.0, key="zkp_pristojba")

    st.markdown("---")

    if st.button("Generiraj žalbu", type="primary", key="zkp_btn"):
        doc = generiraj_zalbu_kaznena_presuda(
            zalitelj,
            {
                'sud_drugostupanjski': sud_drugostupanjski,
                'sud_prvostupanjski': sud_prvostupanjski,
                'poslovni_broj': poslovni_broj,
                'datum_presude': datum_presude,
                'izreka_presude': izreka_presude,
                'razlozi': razlozi,
                'zalbeni_prijedlog': zalbeni_prijedlog,
                'mjesto': mjesto,
            },
            {
                'stavka': trosak_stavka,
                'pdv': trosak_pdv,
                'pristojba': trosak_pristojba,
            },
        )
        prikazi_dokument(doc, "Zalba_kaznena_presuda.docx", "Preuzmi dokument")


def render_kazneno():
    st.header("Kazneno pravo")

    zaglavlje_sastavljaca()

    tip = st.selectbox(
        "Odaberite dokument:",
        [
            "Kaznena prijava",
            "Privatna tužba",
            "Žalba na kaznenu presudu",
        ],
    )

    if tip == "Kaznena prijava":
        _render_kaznena_prijava()
    elif tip == "Privatna tužba":
        _render_privatna_tuzba()
    elif tip == "Žalba na kaznenu presudu":
        _render_zalba_kaznena_presuda()
