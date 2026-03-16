# -----------------------------------------------------------------------------
# STRANICA: Zalbe
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import prikazi_dokument, odabir_suda, unos_tocaka
from generatori.zalbe import generiraj_zalbu_pro
from pristojbe import pristojba_zalba


def render_zalbe():
    st.header("Žalba na presudu")

    with st.expander("Podaci o sudu i presudi", expanded=True):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            sud_prvi = odabir_suda("Prvostupanjski sud", vrsta="opcinski", key="zal_sud1")
        with col_s2:
            sud_drugi = odabir_suda("Drugostupanjski sud", vrsta="zupanijski", key="zal_sud2")
        c1, c2 = st.columns(2)
        broj_presude = c1.text_input("Poslovni broj presude")
        datum_presude = c2.text_input("Datum donošenja presude")
        mjesto = st.text_input("Mjesto sastava žalbe", value="Zagreb")

    with st.expander("Stranke", expanded=False):
        col_tuz, col_tuzen = st.columns(2)
        stranke = {
            'tuzitelj': col_tuz.text_input("Tužitelj"),
            'tuzenik': col_tuzen.text_input("Tuženik"),
        }

    with st.expander("Sadržaj žalbe", expanded=True):
        opseg = st.radio(
            "Pobijate li presudu:",
            ["u cijelosti", "u dijelu odluke o trošku", "u dosuđujućem dijelu"],
            horizontal=True,
        )
        st.markdown("**Žalbeni razlozi (čl. 353. ZPP):**")
        r1 = st.checkbox("Bitna povreda odredaba parničnog postupka")
        r2 = st.checkbox("Pogrešno ili nepotpuno utvrđeno činjenično stanje")
        r3 = st.checkbox("Pogrešna primjena materijalnog prava")
        razlozi_lista = [
            r
            for r, checked in [
                ("Zbog bitne povrede odredaba parničnog postupka", r1),
                ("Zbog pogrešno ili nepotpuno utvrđenog činjeničnog stanja", r2),
                ("Zbog pogrešne primjene materijalnog prava", r3),
            ]
            if checked
        ]
        if not razlozi_lista:
            razlozi_lista.append("(Navesti razloge)")

        st.markdown("---")
        st.markdown("**Obrazloženje žalbe**")
        st.caption("Strukturirajte obrazloženje po točkama - svaka točka obrazlaže jedan žalbeni razlog ili navod.")

        obrazlozenje_tocke = unos_tocaka(
            "Obrazloženje", "zal_obrazlozenje",
            placeholder="Npr. Prvostupanjski sud pogrešno je utvrdio činjenično stanje jer nije izveo dokaz saslušanjem svjedoka...",
            min_tocaka=1, max_tocaka=15, height=120,
        )
        obrazlozenje = "\n\n".join(f"{i+1}. {t}" for i, t in enumerate(obrazlozenje_tocke)) if obrazlozenje_tocke else ""

    with st.expander("Troškovnik žalbe", expanded=False):
        vps_zalba = st.number_input("Vrijednost predmeta spora (VPS) za izračun pristojbe", min_value=0.0, key="zal_vps")
        predlozena = pristojba_zalba(vps_zalba) if vps_zalba > 0 else 0.0
        if predlozena > 0:
            st.info(f"Pristojba za žalbu (2x tužba): **{predlozena:,.2f} EUR** (Tbr. 3 Tarife)")

        troskovnik_data = {'stavka': 0.0, 'pdv': 0.0, 'pristojba': 0.0}
        if st.checkbox("Potražujem trošak", value=True):
            col_tr1, col_tr2 = st.columns(2)
            troskovnik_data['stavka'] = col_tr1.number_input("Cijena sastava", min_value=0.0)
            if col_tr1.checkbox("Dodaj PDV"):
                troskovnik_data['pdv'] = troskovnik_data['stavka'] * 0.25
            troskovnik_data['pristojba'] = col_tr2.number_input("Sudska pristojba", min_value=0.0, value=predlozena)

    if st.button("Generiraj žalbu", type="primary"):
        if not broj_presude.strip():
            st.warning("Unesite poslovni broj presude.")
        if not obrazlozenje.strip():
            st.warning("Preporučljivo je unijeti obrazloženje žalbe.")
        doc_html = generiraj_zalbu_pro(
            sud_prvi, sud_drugi, stranke,
            {
                'broj': broj_presude,
                'datum': datum_presude,
                'opseg': opseg,
                'mjesto': mjesto,
            },
            razlozi_lista, obrazlozenje, troskovnik_data,
        )
        prikazi_dokument(doc_html, "Zalba.docx", "Preuzmi dokument")
