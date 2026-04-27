# -----------------------------------------------------------------------------
# STRANICA: Zalbe
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import prikazi_dokument, odabir_suda, unos_tocaka, zaglavlje_sastavljaca, provjeri_rok_zalbe, napuni_primjerom, audit_kwargs
from generatori.zalbe import generiraj_zalbu_pro
from pristojbe import pristojba_zalba


def render_zalbe():
    st.header("Žalba na presudu")

    zaglavlje_sastavljaca()
    napuni_primjerom('zalba_presuda', '')

    with st.expander("Podaci o sudu i presudi", expanded=True):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            sud_prvi = odabir_suda("Prvostupanjski sud", vrsta="opcinski", key="zal_sud1")
        with col_s2:
            sud_drugi = odabir_suda("Drugostupanjski sud", vrsta="zupanijski", key="zal_sud2")
        c1, c2, c3 = st.columns(3)
        broj_presude = c1.text_input("Poslovni broj presude", key="zal_broj_presude")
        datum_presude_input = c2.date_input("Datum dostave presude", key="zal_datum_dostave",
                                             help="Datum kad ste primili presudu. Rok za žalbu je 15 dana od dostave.")
        datum_presude = datum_presude_input.strftime('%d.%m.%Y.')
        mjesto = c3.text_input("Mjesto", value="Zagreb", key="zal_mjesto")
        provjeri_rok_zalbe(datum_presude_input, rok_dana=15, opis="rok za žalbu (čl. 348. ZPP)")

    with st.expander("Stranke", expanded=False):
        col_tuz, col_tuzen = st.columns(2)
        stranke = {
            'tuzitelj': col_tuz.text_input("Tužitelj", key="zal_tuzitelj"),
            'tuzenik': col_tuzen.text_input("Tuženik", key="zal_tuzenik"),
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
        st.caption("Svaku tvrdnju navedite u zasebnu točku. Svakoj točki možete pridružiti dokaz ili poziv na spis.")

        obrazlozenje_tocke = unos_tocaka(
            "Obrazloženje", "zal_obrazlozenje",
            placeholder="Npr. Prvostupanjski sud pogrešno je utvrdio činjenično stanje jer nije izveo dokaz saslušanjem svjedoka...",
            min_tocaka=1, max_tocaka=15, height=120,
            s_dokazima=True,
            dokaz_placeholder="Npr. Zapisnik s rasprave od 01.01.2025., str. 3-5 spisa",
        )
        if obrazlozenje_tocke:
            parts = []
            for i, t in enumerate(obrazlozenje_tocke):
                line = f"{i+1}. {t['tekst']}"
                if t.get('dokaz'):
                    line += f"\n   Dokaz: {t['dokaz']}"
                parts.append(line)
            obrazlozenje = "\n\n".join(parts)
        else:
            obrazlozenje = ""

    with st.expander("Troškovnik žalbe", expanded=False):
        vps_zalba = st.number_input("Vrijednost predmeta spora - VPS (EUR)", min_value=0.0, key="zal_vps",
                                     help="Isti iznos kao u prvostupanjskom postupku. Služi za izračun pristojbe za žalbu.")
        predlozena = pristojba_zalba(vps_zalba) if vps_zalba > 0 else 0.0
        if predlozena > 0:
            st.info(f"Pristojba za žalbu (dvostruka pristojba za tužbu): **{predlozena:,.2f} EUR**")

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
        presuda = {
            'broj': broj_presude,
            'datum': datum_presude,
            'opseg': opseg,
            'mjesto': mjesto,
        }
        doc_html = generiraj_zalbu_pro(
            sud_prvi, sud_drugi, stranke, presuda,
            razlozi_lista, obrazlozenje, troskovnik_data,
        )
        audit_input = {
            "sud_prvi": sud_prvi,
            "sud_drugi": sud_drugi,
            "stranke": stranke,
            "presuda": presuda,
            "razlozi": razlozi_lista,
            "obrazlozenje": obrazlozenje,
            "troskovnik": troskovnik_data,
        }
        prikazi_dokument(doc_html, "Zalba.docx", "Preuzmi dokument",
                         **audit_kwargs("zalba_presuda", audit_input, "zalbe"))
