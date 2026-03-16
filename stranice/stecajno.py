# -----------------------------------------------------------------------------
# STRANICA: Stecajno pravo - svi dokumenti
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, zaglavlje_sastavljaca, prikazi_dokument, odabir_suda, unos_tocaka
from generatori.stecajno import (
    generiraj_prijedlog_stecaj,
    generiraj_prijavu_trazbine,
    generiraj_stecaj_potrosaca,
)


def _render_prijedlog_stecaj():
    """Prijedlog za otvaranje stecajnog postupka."""
    st.info(
        "Prijedlog za otvaranje stecajnog postupka moze podnijeti vjerovnik ili sam duznik. "
        "Potrebno je dokazati nesposobnost za placanje ili prezaduzenost."
    )

    sud = odabir_suda("Nadležni trgovački sud", vrsta="trgovacki", key="ps_sud")

    col1, col2 = st.columns(2)
    with col1:
        predlagatelj, _, _ = unos_stranke("PREDLAGATELJ", "ps_pred")

    with col2:
        with st.expander("Podaci o duzniku", expanded=True):
            duznik_tvrtka = st.text_input("Tvrtka duznika", key="ps_duz_tvrtka")
            duznik_oib = st.text_input("OIB duznika", key="ps_duz_oib")
            duznik_mbs = st.text_input("MBS (maticni broj subjekta)", key="ps_duz_mbs")
            duznik_sjediste = st.text_input("Sjediste duznika", key="ps_duz_sjediste")

    duznik = {
        'tvrtka': duznik_tvrtka,
        'oib': duznik_oib,
        'mbs': duznik_mbs,
        'sjediste': duznik_sjediste,
    }

    st.subheader("Razlog za otvaranje stecaja")
    razlog = st.radio(
        "Stecajni razlog:",
        ["nesposobnost_za_placanje", "prezaduzenost"],
        format_func=lambda x: "Nesposobnost za placanje" if x == "nesposobnost_za_placanje" else "Prezaduzenost",
        horizontal=True,
        key="ps_razlog",
    )

    blokada_dana = st.number_input(
        "Broj dana blokade racuna", min_value=0, value=60, key="ps_blokada"
    )
    if razlog == "nesposobnost_za_placanje" and blokada_dana < 60:
        st.warning("Nesposobnost za placanje pretpostavlja se ako je duznik u blokadi vise od 60 dana neprekidno.")

    st.subheader("Tražbina predlagatelja")
    st.caption("Navedite osnov i opis tražbine po točkama.")
    opis_tocke = unos_tocaka(
        "Osnov tražbine", "ps_opis",
        placeholder="Npr. Temeljem Ugovora o isporuci robe br. 123/2024, dužnik duguje iznos od...",
        min_tocaka=1, max_tocaka=10, height=80,
    )
    opis_trazbine = "\n\n".join(f"{i+1}. {t}" for i, t in enumerate(opis_tocke)) if opis_tocke else ""
    iznos_trazbine = st.number_input("Iznos trazbine (EUR)", min_value=0.0, key="ps_iznos")

    predujam = st.number_input(
        "Predujam za troskove postupka (EUR)", min_value=0.0, value=1.000, key="ps_predujam"
    )

    mjesto = st.text_input("Mjesto", "Zagreb", key="ps_mjesto")

    podaci = {
        'sud': sud,
        'razlog': razlog,
        'blokada_dana': blokada_dana,
        'opis_trazbine': opis_trazbine,
        'iznos_trazbine': iznos_trazbine,
        'predujam': predujam,
        'mjesto': mjesto,
    }

    st.subheader("Troskovnik")
    ct1, ct2 = st.columns(2)
    trosak_stavka = ct1.number_input("Sastav podneska (EUR)", 0.0, key="ps_stavka")
    trosak_pdv = trosak_stavka * 0.25 if ct1.checkbox("Dodaj PDV (25%)", key="ps_pdv") else 0.0
    trosak_pristojba = ct2.number_input("Sudska pristojba (EUR)", 0.0, key="ps_pristojba")

    troskovi_dict = {
        'stavka': trosak_stavka,
        'pdv': trosak_pdv,
        'pristojba': trosak_pristojba,
    }

    st.markdown("---")
    if st.button("Generiraj prijedlog za stecaj", type="primary", key="ps_btn"):
        doc = generiraj_prijedlog_stecaj(predlagatelj, duznik, podaci, troskovi_dict)
        prikazi_dokument(doc, "Prijedlog_stecaj.docx", "Preuzmi dokument")


def _render_prijava_trazbine():
    """Prijava trazbine u stecajnom postupku."""
    st.info(
        "Vjerovnici prijavljuju trazbine stecajnom upravitelju u roku od 60 dana "
        "od objave otvaranja stecajnog postupka."
    )

    sud = odabir_suda("Nadležni trgovački sud", vrsta="trgovacki", key="pt_stec_sud")

    col1, col2 = st.columns(2)
    with col1:
        vjerovnik, _, _ = unos_stranke("VJEROVNIK", "pt_stec_vj")
    with col2:
        stecajni_upravitelj = st.text_input("Stecajni upravitelj", key="pt_stec_upravitelj")
        broj_predmeta = st.text_input("Poslovni broj stecajnog predmeta", placeholder="St-000/2024", key="pt_stec_pbr")
        duznik_naziv = st.text_input("Naziv duznika (u stecaju)", key="pt_stec_duznik")

    st.subheader("Trazbina")
    c1, c2, c3 = st.columns(3)
    glavnica = c1.number_input("Glavnica (EUR)", min_value=0.0, key="pt_stec_glav")
    kamate = c2.number_input("Kamate (EUR)", min_value=0.0, key="pt_stec_kam")
    troskovi_spora = c3.number_input("Troskovi spora (EUR)", min_value=0.0, key="pt_stec_tros")

    ima_razlucno_pravo = st.checkbox("Imam razlucno pravo (zalozno pravo, hipoteka i sl.)", key="pt_stec_razlucno")
    razlucno_opis = ""
    if ima_razlucno_pravo:
        razlucno_opis = st.text_area(
            "Opis razlucnog prava",
            placeholder="Navedite osnov i predmet razlucnog prava...",
            height=100,
            key="pt_stec_razlucno_opis",
        )

    iban = st.text_input("IBAN za isplatu", key="pt_stec_iban")
    mjesto = st.text_input("Mjesto", "Zagreb", key="pt_stec_mjesto")

    podaci = {
        'stecajni_upravitelj': stecajni_upravitelj,
        'sud': sud,
        'broj_predmeta': broj_predmeta,
        'duznik_naziv': duznik_naziv,
        'glavnica': glavnica,
        'kamate': kamate,
        'troskovi_spora': troskovi_spora,
        'ima_razlucno_pravo': ima_razlucno_pravo,
        'razlucno_opis': razlucno_opis,
        'iban': iban,
        'mjesto': mjesto,
    }

    st.markdown("---")
    if st.button("Generiraj prijavu trazbine", type="primary", key="pt_stec_btn"):
        doc = generiraj_prijavu_trazbine(vjerovnik, podaci)
        prikazi_dokument(doc, "Prijava_trazbine.docx", "Preuzmi dokument")


def _render_stecaj_potrosaca():
    """Prijedlog za stecaj potrosaca."""
    st.warning(
        "Stecaj potrosaca moze pokrenuti fizicka osoba koja ima nepodmirene obveze u iznosu "
        "od najmanje 3.981,68 EUR i koja je u blokadi najmanje 90 dana uzastopno."
    )

    col1, col2 = st.columns(2)
    with col1:
        podnositelj, _, _ = unos_stranke("PODNOSITELJ PRIJEDLOGA", "sp_pod")
    with col2:
        mjesto = st.text_input("Mjesto", "Zagreb", key="sp_mjesto")
        ukupni_dug = st.number_input("Ukupni dug (EUR)", min_value=0.0, key="sp_dug")
        broj_vjerovnika = st.number_input("Broj vjerovnika", min_value=1, value=1, key="sp_br_vjer")
        trajanje_blokade_dana = st.number_input("Trajanje blokade (dana)", min_value=0, value=90, key="sp_blokada")

    if trajanje_blokade_dana < 90:
        st.warning("Uvjet za pokretanje stecaja potrosaca je blokada od najmanje 90 dana uzastopno.")
    if ukupni_dug < 3981.68:
        st.warning("Minimalni iznos duga za pokretanje stecaja potrosaca je 3.981,68 EUR.")

    st.subheader("Financijsko stanje")
    c1, c2 = st.columns(2)
    mjesecni_prihod = c1.number_input("Mjesecni prihod (EUR)", min_value=0.0, key="sp_prihod")
    mjesecni_rashod = c2.number_input("Mjesecni rashod (EUR)", min_value=0.0, key="sp_rashod")

    plan_ispunjenja = st.text_area(
        "Plan ispunjenja obveza",
        placeholder="Opsite plan otplate dugova u razdoblju do 5 godina...",
        height=150,
        key="sp_plan",
    )

    # --- Dinamicka lista vjerovnika ---
    st.subheader("Popis vjerovnika")
    if "popis_vjerovnika_sp" not in st.session_state:
        st.session_state.popis_vjerovnika_sp = [{"naziv": "", "iznos": 0.0}]

    popis_vjerovnika = []
    for i, vj in enumerate(st.session_state.popis_vjerovnika_sp):
        with st.expander(f"Vjerovnik {i + 1}", expanded=(i < 3)):
            c1, c2 = st.columns([2, 1])
            naziv = c1.text_input("Naziv vjerovnika", key=f"sp_vj_naziv_{i}")
            iznos = c2.number_input("Iznos duga (EUR)", min_value=0.0, key=f"sp_vj_iznos_{i}")
            popis_vjerovnika.append({"naziv": naziv, "iznos": iznos})

    if st.button("Dodaj vjerovnika", key="sp_dodaj_vj"):
        st.session_state.popis_vjerovnika_sp.append({"naziv": "", "iznos": 0.0})
        st.rerun()

    # --- Dinamicka lista imovine ---
    st.subheader("Popis imovine")
    if "popis_imovine_sp" not in st.session_state:
        st.session_state.popis_imovine_sp = [{"opis": "", "vrijednost": 0.0}]

    popis_imovine = []
    for i, im in enumerate(st.session_state.popis_imovine_sp):
        with st.expander(f"Imovina {i + 1}", expanded=(i < 3)):
            c1, c2 = st.columns([2, 1])
            opis = c1.text_input("Opis imovine", key=f"sp_im_opis_{i}")
            vrijednost = c2.number_input("Vrijednost (EUR)", min_value=0.0, key=f"sp_im_vrij_{i}")
            popis_imovine.append({"opis": opis, "vrijednost": vrijednost})

    if st.button("Dodaj imovinu", key="sp_dodaj_im"):
        st.session_state.popis_imovine_sp.append({"opis": "", "vrijednost": 0.0})
        st.rerun()

    podaci = {
        'mjesto': mjesto,
        'ukupni_dug': ukupni_dug,
        'broj_vjerovnika': broj_vjerovnika,
        'trajanje_blokade_dana': trajanje_blokade_dana,
        'popis_vjerovnika': popis_vjerovnika,
        'popis_imovine': popis_imovine,
        'mjesecni_prihod': mjesecni_prihod,
        'mjesecni_rashod': mjesecni_rashod,
        'plan_ispunjenja': plan_ispunjenja,
    }

    st.markdown("---")
    if st.button("Generiraj prijedlog za stecaj potrosaca", type="primary", key="sp_btn"):
        doc = generiraj_stecaj_potrosaca(podnositelj, podaci)
        prikazi_dokument(doc, "Stecaj_potrosaca.docx", "Preuzmi dokument")


def render_stecajno():
    st.header("Stečajno pravo")

    zaglavlje_sastavljaca()

    tab1, tab2, tab3 = st.tabs([
        "Prijedlog za stečaj",
        "Prijava tražbine",
        "Stečaj potrošača",
    ])

    with tab1:
        _render_prijedlog_stecaj()
    with tab2:
        _render_prijava_trazbine()
    with tab3:
        _render_stecaj_potrosaca()
