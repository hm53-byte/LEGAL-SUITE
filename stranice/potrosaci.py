# -----------------------------------------------------------------------------
# STRANICA: Zastita potrosaca (Consumer protection)
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, zaglavlje_sastavljaca, prikazi_dokument, audit_kwargs
from generatori.potrosaci import (
    generiraj_reklamaciju,
    generiraj_jednostrani_raskid,
    generiraj_prijavu_inspekciji,
)


def _render_reklamacija():
    """Reklamacija proizvoda / usluge."""
    st.subheader("Podaci o potrošaču")
    potrosac, _, _ = unos_stranke("POTROŠAČ", "rek_potrosac")

    st.subheader("Podaci o trgovcu")
    col1, col2 = st.columns(2)
    trgovac_naziv = col1.text_input("Naziv trgovca", key="rek_trgovac_naziv")
    trgovac_adresa = col2.text_input("Adresa trgovca", key="rek_trgovac_adresa")

    st.subheader("Podaci o kupnji")
    c1, c2, c3 = st.columns(3)
    mjesto = c1.text_input("Mjesto", "Zagreb", key="rek_mjesto")
    datum_kupnje = c2.date_input("Datum kupnje", key="rek_datum_kupnje")
    broj_racuna = c3.text_input("Broj računa", key="rek_broj_racuna")

    opis_proizvoda = st.text_input(
        "Opis proizvoda / usluge",
        key="rek_opis_proizvoda",
        placeholder="npr. Laptop Lenovo ThinkPad T14",
    )
    cijena = st.number_input("Cijena (EUR)", min_value=0.0, key="rek_cijena")

    st.subheader("Reklamacija")
    opis_nedostatka = st.text_area(
        "Opis nedostatka",
        key="rek_opis_nedostatka",
        height=150,
        placeholder="Opišite nedostatak proizvoda ili usluge...",
    )
    zahtjev = st.selectbox(
        "Zahtjev potrošača",
        ["popravak", "zamjena", "povrat_novca", "snizenje_cijene"],
        format_func=lambda x: {
            "popravak": "Popravak proizvoda",
            "zamjena": "Zamjena proizvoda",
            "povrat_novca": "Povrat novca",
            "snizenje_cijene": "Sniženje cijene",
        }[x],
        key="rek_zahtjev",
    )

    st.info(
        "Trgovac je dužan odgovoriti na reklamaciju u roku od **15 dana** "
        "od dana primitka pisanog prigovora (čl. 10. Zakona o zaštiti potrošača)."
    )

    st.markdown("---")
    if st.button("Generiraj reklamaciju", type="primary", key="rek_btn"):
        podaci = {
            "mjesto": mjesto,
            "trgovac_naziv": trgovac_naziv,
            "trgovac_adresa": trgovac_adresa,
            "datum_kupnje": datum_kupnje.strftime("%d.%m.%Y."),
            "broj_racuna": broj_racuna,
            "opis_proizvoda": opis_proizvoda,
            "opis_nedostatka": opis_nedostatka,
            "zahtjev": zahtjev,
            "cijena": cijena,
        }
        doc = generiraj_reklamaciju(potrosac, podaci)
        audit_input = {"potrosac_html": potrosac, "podaci": podaci}
        prikazi_dokument(doc, "Reklamacija.docx", "Preuzmi dokument",
                         **audit_kwargs(f"reklamacija_{zahtjev}", audit_input, "potrosaci"))


def _render_jednostrani_raskid():
    """Jednostrani raskid ugovora sklopljenog na daljinu."""
    st.subheader("Podaci o potrošaču")
    potrosac, _, _ = unos_stranke("POTROŠAČ", "jr_potrosac")

    st.subheader("Podaci o trgovcu")
    col1, col2 = st.columns(2)
    trgovac_naziv = col1.text_input("Naziv trgovca", key="jr_trgovac_naziv")
    trgovac_adresa = col2.text_input("Adresa trgovca", key="jr_trgovac_adresa")

    st.subheader("Podaci o narudžbi")
    c1, c2 = st.columns(2)
    mjesto = c1.text_input("Mjesto", "Zagreb", key="jr_mjesto")
    broj_narudzbe = c2.text_input("Broj narudžbe", key="jr_broj_narudzbe")

    c3, c4 = st.columns(2)
    datum_narudzbe = c3.date_input("Datum narudžbe", key="jr_datum_narudzbe")
    datum_isporuke = c4.date_input("Datum isporuke", key="jr_datum_isporuke")

    opis_proizvoda = st.text_input(
        "Opis proizvoda",
        key="jr_opis_proizvoda",
        placeholder="npr. Bežične slušalice Sony WH-1000XM5",
    )

    st.info(
        "Potrošač ima pravo na jednostrani raskid ugovora sklopljenog izvan poslovnih "
        "prostorija ili na daljinu u roku od **14 dana** bez navođenja razloga "
        "(čl. 79. Zakona o zaštiti potrošača)."
    )

    st.markdown("---")
    if st.button("Generiraj izjavu o raskidu", type="primary", key="jr_btn"):
        podaci = {
            "mjesto": mjesto,
            "trgovac_naziv": trgovac_naziv,
            "trgovac_adresa": trgovac_adresa,
            "datum_narudzbe": datum_narudzbe.strftime("%d.%m.%Y."),
            "datum_isporuke": datum_isporuke.strftime("%d.%m.%Y."),
            "opis_proizvoda": opis_proizvoda,
            "broj_narudzbe": broj_narudzbe,
        }
        doc = generiraj_jednostrani_raskid(potrosac, podaci)
        audit_input = {"potrosac_html": potrosac, "podaci": podaci}
        prikazi_dokument(doc, "Jednostrani_raskid.docx", "Preuzmi dokument",
                         **audit_kwargs("jednostrani_raskid", audit_input, "potrosaci"))


def _render_prijava_inspekciji():
    """Prijava tržišnoj inspekciji."""
    st.subheader("Podaci o podnositelju prijave")
    podnositelj, _, _ = unos_stranke("PODNOSITELJ PRIJAVE", "pi_podnositelj")

    st.subheader("Podaci o trgovcu")
    col1, col2 = st.columns(2)
    trgovac_naziv = col1.text_input("Naziv trgovca", key="pi_trgovac_naziv")
    trgovac_adresa = col2.text_input("Adresa trgovca", key="pi_trgovac_adresa")
    trgovac_oib = st.text_input("OIB trgovca (ako je poznat)", max_chars=11, key="pi_trgovac_oib")

    st.subheader("Opis kršenja")
    c1, c2 = st.columns(2)
    mjesto = c1.text_input("Mjesto", "Zagreb", key="pi_mjesto")
    datum_krsenja = c2.date_input("Datum kršenja", key="pi_datum_krsenja")

    opis_krsenja = st.text_area(
        "Opis kršenja prava potrošača",
        key="pi_opis_krsenja",
        height=200,
        placeholder="Detaljno opišite na koji način je trgovac prekršio vaša prava...",
    )

    st.subheader("Prethodni prigovor trgovcu")
    prethodni_prigovor = st.checkbox(
        "Već sam uputio/la pisani prigovor trgovcu", key="pi_prethodni_prigovor"
    )

    datum_prigovora = None
    odgovor_trgovca = ""
    if prethodni_prigovor:
        c3, c4 = st.columns(2)
        datum_prigovora = c3.date_input("Datum prigovora", key="pi_datum_prigovora")
        odgovor_trgovca = c4.text_input(
            "Odgovor trgovca",
            key="pi_odgovor_trgovca",
            placeholder="npr. Nije odgovorio / Odbio reklamaciju",
        )
    else:
        st.warning(
            "Preporučuje se najprije uputiti **pisani prigovor trgovcu** prije podnošenja "
            "prijave tržišnoj inspekciji. Trgovac je dužan odgovoriti u roku od 15 dana."
        )

    st.subheader("Prilozi")
    if "pi_prilozi" not in st.session_state:
        st.session_state.pi_prilozi = []

    for i, prilog in enumerate(st.session_state.pi_prilozi):
        col_p, col_del = st.columns([4, 1])
        st.session_state.pi_prilozi[i] = col_p.text_input(
            f"Prilog {i + 1}", value=prilog, key=f"pi_prilog_{i}"
        )
        if col_del.button("Ukloni", key=f"pi_del_prilog_{i}"):
            st.session_state.pi_prilozi.pop(i)
            st.rerun()

    if st.button("Dodaj prilog", key="pi_dodaj_prilog"):
        st.session_state.pi_prilozi.append("")
        st.rerun()

    st.markdown("---")
    if st.button("Generiraj prijavu inspekciji", type="primary", key="pi_btn"):
        podaci = {
            "mjesto": mjesto,
            "trgovac_naziv": trgovac_naziv,
            "trgovac_adresa": trgovac_adresa,
            "trgovac_oib": trgovac_oib,
            "opis_krsenja": opis_krsenja,
            "datum_krsenja": datum_krsenja.strftime("%d.%m.%Y."),
            "prethodni_prigovor": prethodni_prigovor,
            "datum_prigovora": datum_prigovora.strftime("%d.%m.%Y.") if datum_prigovora else "",
            "odgovor_trgovca": odgovor_trgovca,
            "prilozi": [p for p in st.session_state.pi_prilozi if p.strip()],
        }
        doc = generiraj_prijavu_inspekciji(podnositelj, podaci)
        audit_input = {"podnositelj_html": podnositelj, "podaci": podaci}
        prikazi_dokument(doc, "Prijava_inspekciji.docx", "Preuzmi dokument",
                         **audit_kwargs("prijava_inspekciji", audit_input, "potrosaci"))


def render_potrosaci():
    st.header("Zaštita potrošača")

    zaglavlje_sastavljaca()

    tab1, tab2, tab3 = st.tabs([
        "Reklamacija",
        "Jednostrani raskid",
        "Prijava inspekciji",
    ])

    with tab1:
        _render_reklamacija()
    with tab2:
        _render_jednostrani_raskid()
    with tab3:
        _render_prijava_inspekciji()
