# -----------------------------------------------------------------------------
# STRANICA: Tuzbe (parnicni postupak)
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import (
    unos_stranke,
    unos_vise_stranaka,
    spoji_stranke_html,
    zaglavlje_sastavljaca,
    prikazi_dokument,
    odredi_nadlezni_sud,
    odabir_suda,
    unos_tocaka,
)
from generatori.tuzbe import generiraj_tuzbu_pro
from pristojbe import pristojba_tuzba


def render_tuzbe():
    st.header("Tužba (parnični postupak)")

    zastupanje = zaglavlje_sastavljaca()

    # Vise tuzitelja/tuzenika
    vise_stranaka = st.checkbox("Više tužitelja / tuženika", key="tuzbe_vise")

    if vise_stranaka:
        col1, col2 = st.columns(2)
        with col1:
            tuzitelji = unos_vise_stranaka("TUŽITELJ", "t1")
        with col2:
            tuzenici = unos_vise_stranaka("TUŽENIK", "t2")
        t1 = spoji_stranke_html(tuzitelji, "TUŽITELJ", "TUŽITELJI")
        t2 = spoji_stranke_html(tuzenici, "TUŽENIK", "TUŽENICI")
        tip1 = tuzitelji[0][1]
        tip2 = tuzenici[0][1]
    else:
        col1, col2 = st.columns(2)
        with col1:
            t1, tip1, _ = unos_stranke("TUŽITELJ", "t1")
        with col2:
            t2, tip2, _ = unos_stranke("TUŽENIK", "t2")

    # Automatsko odredjivanje nadleznog suda
    if tip1 == "Pravna" and tip2 == "Pravna":
        st.info(
            "Kada su obje stranke pravne osobe (trgovačka društva), "
            "nadležan je Trgovački sud."
        )

    st.subheader("Predmet spora")
    vrsta_suda = "trgovacki" if (tip1 == "Pravna" and tip2 == "Pravna") else "opcinski"
    sud = odabir_suda("Naslovni sud", vrsta=vrsta_suda, key="tuzbe_sud")
    vps = st.number_input("Vrijednost spora (Glavnica duga)", min_value=0.0,
                          help="Iznos u EUR koji se potražuje. Određuje nadležnost suda i visinu pristojbe.")
    datum_dospijeca = st.date_input("Datum dospijeća (Od kada teku kamate?)",
                                    help="Datum od kojeg se obračunavaju zakonske zatezne kamate (čl. 29. ZOO).")
    vrsta = st.text_input("Radi (kratki opis)", "Isplate (Dugovanja)",
                          help="Kratki opis predmeta spora, npr. 'Isplate', 'Naknade štete', 'Ispunjenja ugovora'.")

    st.subheader("I. Činjenični navodi")
    st.caption("Navedite kronološki relevantne činjenice - svaku činjenicu u zasebnu točku.")
    cinjenice_tocke = unos_tocaka(
        "Činjenični navod", "tuzba_cinj",
        placeholder="Npr. Dana 15.03.2024. tužitelj i tuženik sklopili su Ugovor o kupoprodaji robe br. 123/2024...",
        min_tocaka=1, max_tocaka=20, height=100,
    )
    # Spoji u jedan tekst za generator (kompatibilnost)
    cinjenice = "\n\n".join(f"{i+1}. {c}" for i, c in enumerate(cinjenice_tocke)) if cinjenice_tocke else ""

    st.subheader("II. Dokazni prijedlozi")
    st.caption("Navedite dokaze kojima potkrjepljujete tužbeni zahtjev.")
    dokazi_tocke = unos_tocaka(
        "Dokaz", "tuzba_dokazi",
        placeholder="Npr. Ugovor o kupoprodaji br. 123/2024 od 15.03.2024.",
        min_tocaka=1, max_tocaka=15, height=60,
    )
    dokazi = "\n".join(f"- {d}" for d in dokazi_tocke) if dokazi_tocke else ""

    st.subheader("Troškovnik")
    # Auto-izracun sudske pristojbe prema VPS
    predlozena_pristojba = pristojba_tuzba(vps) if vps > 0 else 0.0
    if predlozena_pristojba > 0:
        st.info(f"Izracunata sudska pristojba za VPS {vps:,.2f} EUR: **{predlozena_pristojba:,.2f} EUR** (Tbr. 1 Tarife)")

    col_tr1, col_tr2, col_tr3 = st.columns(3)
    trosak_sastav = col_tr1.number_input("Sastav tužbe (EUR)", 0.0)
    trosak_pdv = trosak_sastav * 0.25 if col_tr2.checkbox("Dodaj PDV (25%)", value=True) else 0.0
    trosak_pristojba = col_tr3.number_input("Sudska pristojba (EUR)", value=predlozena_pristojba)

    if st.button("Generiraj tužbu", type="primary"):
        if vps <= 0:
            st.warning("Unesite vrijednost predmeta spora (VPS) veću od 0.")
        if not cinjenice.strip():
            st.warning("Preporučljivo je unijeti činjenice spora.")
        doc = generiraj_tuzbu_pro(
            sud, zastupanje, t1, t2, vps, vrsta,
            {
                'cinjenice': cinjenice,
                'dokazi': dokazi,
                'datum_dospijeca': datum_dospijeca.strftime('%d.%m.%Y.'),
            },
            {
                'stavka': trosak_sastav,
                'pdv': trosak_pdv,
                'pristojba': trosak_pristojba,
            },
        )
        prikazi_dokument(doc, "Tuzba.docx", "Preuzmi dokument")
