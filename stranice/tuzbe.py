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
    napuni_primjerom,
    provjeri_zastaru,
)
from generatori.tuzbe import generiraj_tuzbu_pro
from pristojbe import pristojba_tuzba


def render_tuzbe():
    st.header("Tužba (parnični postupak)")

    zastupanje = zaglavlje_sastavljaca()

    napuni_primjerom('tuzba', 't')

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
    vps = st.number_input("Vrijednost predmeta spora - VPS (EUR)", min_value=0.0,
                          help="Iznos u EUR koji tražite od tuženika. Na temelju VPS-a izračunava se sudska pristojba i određuje nadležnost suda.")
    datum_dospijeca = st.date_input("Datum dospijeća (Od kada teku kamate?)",
                                    help="Datum od kojeg se obračunavaju zakonske zatezne kamate (čl. 29. ZOO).")
    provjeri_zastaru(datum_dospijeca, rok_godina=5, opis_roka="opći zastarni rok (čl. 225. ZOO)")
    vrsta = st.text_input("Radi (kratki opis)", "Isplate (Dugovanja)",
                          help="Kratki opis predmeta spora, npr. 'Isplate', 'Naknade štete', 'Ispunjenja ugovora'.")

    st.subheader("I. Činjenični navodi i dokazi")
    st.caption("Svaku činjenicu navedite u zasebnu točku. Svakoj točki možete pridružiti dokaz.")
    cinjenice_tocke = unos_tocaka(
        "Činjenični navod", "tuzba_cinj",
        placeholder="Npr. Dana 15.03.2024. tužitelj i tuženik sklopili su Ugovor o kupoprodaji robe br. 123/2024...",
        min_tocaka=1, max_tocaka=20, height=100,
        s_dokazima=True,
        dokaz_placeholder="Npr. Ugovor o kupoprodaji br. 123/2024 od 15.03.2024.",
    )
    # Spoji u tekst za generator (kompatibilnost)
    if cinjenice_tocke:
        cinj_parts = []
        dok_parts = []
        for i, t in enumerate(cinjenice_tocke):
            cinj_parts.append(f"{i+1}. {t['tekst']}")
            if t.get('dokaz'):
                dok_parts.append(f"- {t['dokaz']}")
        cinjenice = "\n\n".join(cinj_parts)
        dokazi = "\n".join(dok_parts) if dok_parts else ""
    else:
        cinjenice = ""
        dokazi = ""

    st.subheader("Troškovnik")
    # Auto-izracun sudske pristojbe prema VPS
    predlozena_pristojba = pristojba_tuzba(vps) if vps > 0 else 0.0
    if predlozena_pristojba > 0:
        st.info(f"Izracunata sudska pristojba za VPS {vps:,.2f} EUR: **{predlozena_pristojba:,.2f} EUR** (Tbr. 1 Tarife)")

    col_tr1, col_tr2, col_tr3 = st.columns(3)
    trosak_sastav = col_tr1.number_input("Sastav tužbe (EUR)", 0.0,
                                        help="Odvjetnička nagrada za sastav tužbe prema Tarifi o nagradama.")
    trosak_pdv = trosak_sastav * 0.25 if col_tr2.checkbox("Dodaj PDV (25%)", value=True) else 0.0
    trosak_pristojba = col_tr3.number_input("Sudska pristojba (EUR)", value=predlozena_pristojba,
                                             help="Pristojba koju plaćate sudu. Automatski izračunata prema VPS-u.")

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
