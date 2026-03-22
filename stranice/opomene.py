# -----------------------------------------------------------------------------
# STRANICA: Opomena pred tuzbu / ovrhu
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, zaglavlje_sastavljaca, prikazi_dokument, napuni_primjerom
from generatori.opomene import generiraj_opomenu


def render_opomene():
    st.header("Opomena pred tužbu / ovrhu")

    zastupanje = zaglavlje_sastavljaca()

    napuni_primjerom('opomena', '')

    vrsta = st.radio(
        "Vrsta opomene:",
        ["Opomena pred tužbu", "Opomena pred ovrhu"],
        horizontal=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        v, _, _ = unos_stranke("VJEROVNIK", "op_v")
    with col2:
        d, _, _ = unos_stranke("DUŽNIK", "op_d")

    st.subheader("Podaci o tražbini")
    c1, c2 = st.columns(2)
    glavnica = c1.number_input("Iznos duga (EUR)", min_value=0.0, key="glavnica")
    rok = c2.number_input("Rok za ispunjenje (dana)", min_value=1, value=8, key="rok")
    datum_dospijeca = st.date_input("Datum dospijeća obveze")

    opis_osnove = st.text_area(
        "Osnova tražbine",
        placeholder="Opišite pravnu osnovu duga (ugovor, račun, isporuka...)",
        height=120,
    )

    with st.expander("Podaci za uplatu", expanded=False):
        iban = st.text_input("IBAN", placeholder="HR00 0000 0000 0000 0000 0", max_chars=21)
        poziv = st.text_input("Poziv na broj", placeholder="HR00 00000000-000000")
        opis_placanja = st.text_input("Opis plaćanja", "Podmirenje duga po opomeni")

    mjesto = st.text_input("Mjesto", "Zagreb")

    if st.button("Generiraj opomenu", type="primary"):
        vrsta_key = "tuzba" if "tužbu" in vrsta else "ovrha"
        doc = generiraj_opomenu(
            vrsta_key, v, d,
            {"glavnica": glavnica},
            {
                "rok_dana": rok,
                "datum_dospijeca": datum_dospijeca.strftime("%d.%m.%Y."),
                "opis_osnove": opis_osnove,
                "mjesto": mjesto,
                "iban": iban if iban else "____________________",
                "poziv_na_broj": poziv if poziv else "____________________",
                "opis_placanja": opis_placanja,
            },
            zastupanje,
        )
        naziv = "Opomena_pred_tuzbu.docx" if vrsta_key == "tuzba" else "Opomena_pred_ovrhu.docx"
        prikazi_dokument(doc, naziv, "Preuzmi dokument")
