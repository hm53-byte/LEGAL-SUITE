# -----------------------------------------------------------------------------
# STRANICA: Punomoc (opca i posebna)
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, prikazi_dokument, odabir_suda, zaglavlje_sastavljaca, napuni_primjerom, audit_kwargs
from generatori.punomoci import generiraj_punomoc


def render_punomoci():
    st.header("Punomoć")

    zaglavlje_sastavljaca()
    napuni_primjerom('punomoc', '')

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

    mjesto = st.text_input("Mjesto", "Zagreb", key="pm_mjesto")

    podaci = {"mjesto": mjesto}

    if "Posebna" in vrsta:
        st.subheader("Opseg punomoći")
        podaci["sud"] = odabir_suda("Sud (ako je za sudski postupak)", key="pm_sud_odabir")
        podaci["poslovni_broj"] = st.text_input("Poslovni broj predmeta", placeholder="P-000/2024")
        podaci["opseg"] = st.text_area(
            "Opis predmeta / opseg ovlaštenja",
            placeholder="Opišite predmet u kojem punomoćnik zastupa vlastodavca...",
            height=120,
            key="pm_opseg",
        )

    if st.button("Generiraj punomoć", type="primary"):
        vrsta_key = "opca" if "Opća" in vrsta else "posebna"
        doc = generiraj_punomoc(vrsta_key, vlastodavac, punomocnik, podaci)
        naziv = "Opca_punomoc.docx" if vrsta_key == "opca" else "Posebna_punomoc.docx"
        audit_input = {
            "vrsta_key": vrsta_key,
            "vlastodavac_html": vlastodavac,
            "punomocnik_html": punomocnik,
            "podaci": podaci,
        }
        prikazi_dokument(doc, naziv, "Preuzmi dokument",
                         **audit_kwargs(f"punomoc_{vrsta_key}", audit_input, "punomoci"))
