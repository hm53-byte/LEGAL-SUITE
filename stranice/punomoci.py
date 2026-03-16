# -----------------------------------------------------------------------------
# STRANICA: Punomoc (opca i posebna)
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, prikazi_dokument, odabir_suda
from generatori.punomoci import generiraj_punomoc


def render_punomoci():
    st.header("Punomoć")

    vrsta = st.radio(
        "Vrsta punomoći:",
        ["Opća punomoć", "Posebna punomoć"],
        horizontal=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        vlastodavac, _, _ = unos_stranke("VLASTODAVAC", "pm_v")
    with col2:
        punomocnik, _, _ = unos_stranke("PUNOMOĆNIK", "pm_p")

    mjesto = st.text_input("Mjesto", "Zagreb")

    podaci = {"mjesto": mjesto}

    if "Posebna" in vrsta:
        st.subheader("Opseg punomoći")
        podaci["sud"] = odabir_suda("Sud (ako je za sudski postupak)", key="pm_sud_odabir")
        podaci["poslovni_broj"] = st.text_input("Poslovni broj predmeta", placeholder="P-000/2024")
        podaci["opseg"] = st.text_area(
            "Opis predmeta / opseg ovlaštenja",
            placeholder="Opišite predmet u kojem punomoćnik zastupa vlastodavca...",
            height=120,
        )

    if st.button("Generiraj punomoć", type="primary"):
        vrsta_key = "opca" if "Opća" in vrsta else "posebna"
        doc = generiraj_punomoc(vrsta_key, vlastodavac, punomocnik, podaci)
        naziv = "Opca_punomoc.docx" if vrsta_key == "opca" else "Posebna_punomoc.docx"
        prikazi_dokument(doc, naziv, "Preuzmi dokument")
