# -----------------------------------------------------------------------------
# STRANICA: Kalkulator kamata
# Zakonske zatezne kamate prema Zakonu o obveznim odnosima (ZOO cl. 29)
# -----------------------------------------------------------------------------
import streamlit as st
from datetime import date
from pomocne import format_eur, prikazi_dokument


# Zakonske zatezne kamate RH (prema HNB, polugodisnje)
# Stopa = eskontna stopa HNB + zakonski dodatak (5% za trgovacke, 3% za ostale)
ZAKONSKE_STOPE = {
    "2025-H1": {"eskontna": 3.75, "trgovacka": 8.75, "gradanska": 6.75, "od": "01.01.2025.", "do": "30.06.2025."},
    "2024-H2": {"eskontna": 3.75, "trgovacka": 8.75, "gradanska": 6.75, "od": "01.07.2024.", "do": "31.12.2024."},
    "2024-H1": {"eskontna": 4.50, "trgovacka": 9.50, "gradanska": 7.50, "od": "01.01.2024.", "do": "30.06.2024."},
    "2023-H2": {"eskontna": 4.50, "trgovacka": 9.50, "gradanska": 7.50, "od": "01.07.2023.", "do": "31.12.2023."},
    "2023-H1": {"eskontna": 3.00, "trgovacka": 8.00, "gradanska": 6.00, "od": "01.01.2023.", "do": "30.06.2023."},
    "2022-H2": {"eskontna": 2.50, "trgovacka": 7.50, "gradanska": 5.50, "od": "01.07.2022.", "do": "31.12.2022."},
    "2022-H1": {"eskontna": 2.50, "trgovacka": 7.50, "gradanska": 5.50, "od": "01.01.2022.", "do": "30.06.2022."},
}


def _izracunaj_kamatu(glavnica, stopa, datum_od, datum_do):
    """Izracunava kamatu za period. Vraca (kamata, dana)."""
    dana = (datum_do - datum_od).days
    if dana <= 0:
        return 0.0, 0
    kamata = (glavnica * stopa * dana) / 36500
    return round(kamata, 2), dana


def _generiraj_obracun_html(glavnica, stopa, datum_od, datum_do, kamata, dana, vrsta_stope):
    """Generira HTML prikaz obracuna kamata za DOCX export."""
    ukupno = glavnica + kamata
    return (
        f"<div class='header-doc'>OBRAČUN ZATEZNIH KAMATA</div>"
        f"<div class='justified'>"
        f"Na temelju članka 29. Zakona o obveznim odnosima (NN 35/05, 41/08, 125/11, 78/15, 29/18, 126/21, 114/22, 156/22) "
        f"izračunavaju se zatezne kamate kako slijedi:</div><br>"
        f"<table class='cost-table'>"
        f"<tr><td width='60%'>Glavnica:</td><td width='40%' align='right'><b>{format_eur(glavnica)}</b></td></tr>"
        f"<tr><td>Kamatna stopa ({vrsta_stope}):</td><td align='right'>{stopa:.2f}% godišnje</td></tr>"
        f"<tr><td>Razdoblje:</td><td align='right'>{datum_od.strftime('%d.%m.%Y.')} - {datum_do.strftime('%d.%m.%Y.')}</td></tr>"
        f"<tr><td>Broj dana:</td><td align='right'>{dana}</td></tr>"
        f"<tr><td>Zatezne kamate:</td><td align='right'><b>{format_eur(kamata)}</b></td></tr>"
        f"<tr style='font-weight: bold; background-color: #f0f0f0;'>"
        f"<td style='padding: 10px;'>UKUPNO (glavnica + kamate):</td>"
        f"<td style='padding: 10px;' align='right'>{format_eur(ukupno)}</td></tr>"
        f"</table><br>"
        f"<div class='justified'><b>Formula:</b> Kamata = (Glavnica × Stopa × Broj dana) / 36.500</div>"
        f"<div class='justified'>Kamata = ({format_eur(glavnica)} × {stopa:.2f}% × {dana}) / 36.500 = <b>{format_eur(kamata)}</b></div>"
    )


def render_kamate():
    st.header("Kalkulator kamata")

    vrsta = st.radio(
        "Vrsta obračuna:",
        ["zakonska", "ugovorna"],
        format_func=lambda x: "Zakonska zatezna kamata (ZOO čl. 29)" if x == "zakonska" else "Ugovorna kamata (slobodna stopa)",
        horizontal=True,
    )

    iznos = st.number_input("Glavnica (EUR)", min_value=0.0, key="kam_iznos")
    c1, c2 = st.columns(2)
    d1 = c1.date_input("Dospijeće (od kada teku kamate)", key="kam_d1")
    d2 = c2.date_input("Datum obračuna (do)", key="kam_d2")

    if vrsta == "zakonska":
        tip_odnosa = st.radio(
            "Vrsta odnosa:",
            ["gradanska", "trgovacka"],
            format_func=lambda x: "Građanski (fizičke osobe)" if x == "gradanska" else "Trgovački (pravne osobe)",
            horizontal=True,
        )
        # Prikaži tablicu zakonskih stopa
        with st.expander("Zakonske zatezne kamate RH (prema HNB)"):
            st.markdown("| Razdoblje | Eskontna | Trgovačka | Građanska |")
            st.markdown("|-----------|----------|-----------|-----------|")
            for _, s in ZAKONSKE_STOPE.items():
                st.markdown(f"| {s['od']} - {s['do']} | {s['eskontna']:.2f}% | {s['trgovacka']:.2f}% | {s['gradanska']:.2f}% |")

        # Koristimo najnoviju stopu (pojednostavljeno - ne sjecemo po periodima)
        najnovija = list(ZAKONSKE_STOPE.values())[0]
        stopa = najnovija[tip_odnosa]
        st.info(f"Primjenjuje se stopa: **{stopa:.2f}%** ({tip_odnosa} odnos, {najnovija['od']} - {najnovija['do']})")
        vrsta_stope = f"zakonska {tip_odnosa}"
    else:
        stopa = st.number_input("Kamatna stopa (%)", value=12.0, min_value=0.0, key="kam_stopa")
        vrsta_stope = "ugovorna"

    if st.button("Izračunaj", type="primary"):
        if iznos <= 0:
            st.warning("Glavnica mora biti veća od 0.")
            return
        dana = (d2 - d1).days
        if dana <= 0:
            st.error("Datum obračuna mora biti poslije dospijeća.")
            return

        kamata, dana = _izracunaj_kamatu(iznos, stopa, d1, d2)
        ukupno = iznos + kamata

        st.success(f"Zatezna kamata: **{format_eur(kamata)}** (za {dana} dana po stopi {stopa:.2f}%)")
        c1, c2, c3 = st.columns(3)
        c1.metric("Glavnica", format_eur(iznos))
        c2.metric("Kamate", format_eur(kamata))
        c3.metric("Ukupno", format_eur(ukupno))

        # DOCX export obracuna
        doc_html = _generiraj_obracun_html(iznos, stopa, d1, d2, kamata, dana, vrsta_stope)
        prikazi_dokument(doc_html, "Obracun_kamata.docx", "Preuzmi obračun (DOCX)")
