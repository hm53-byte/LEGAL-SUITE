# -----------------------------------------------------------------------------
# STRANICA: Kalkulator sudskih pristojbi
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import format_eur
from pristojbe import (
    pristojba_tuzba,
    pristojba_zalba,
    pristojba_revizija,
    pristojba_ovrha_jb,
    pristojba_ovrha_ovrsna_isprava,
    pristojba_prigovor_ovrhe,
    pristojba_zk_prijedlog,
    pristojba_zk_brisanje,
    pristojba_upravni_spor,
    pristojba_punomoc,
    OSLOBODENJA,
)


def render_pristojbe():
    st.header("Kalkulator sudskih pristojbi")
    st.caption("Prema Zakonu o sudskim pristojbama (NN 118/18) i Uredbi o tarifi (NN 129/19)")

    tip = st.selectbox(
        "Vrsta postupka:",
        [
            "Tužba (parnični postupak)",
            "Žalba na presudu",
            "Revizija",
            "Ovrha (vjerodostojna isprava / JB)",
            "Ovrha (ovršna isprava / presuda)",
            "Prigovor na rješenje o ovrsi",
            "ZK prijedlog (uknjižba, zabilježba...)",
            "ZK brisanje upisa",
            "Tužba u upravnom sporu",
            "Punomoć",
        ],
        key="prist_tip",
    )

    # Postupci koji ovise o VPS
    vps_postupci = {
        "Tužba (parnični postupak)": pristojba_tuzba,
        "Žalba na presudu": pristojba_zalba,
        "Revizija": pristojba_revizija,
        "Ovrha (vjerodostojna isprava / JB)": pristojba_ovrha_jb,
        "Ovrha (ovršna isprava / presuda)": pristojba_ovrha_ovrsna_isprava,
        "Prigovor na rješenje o ovrsi": pristojba_prigovor_ovrhe,
    }

    # Fiksne pristojbe
    fiksni_postupci = {
        "ZK prijedlog (uknjižba, zabilježba...)": pristojba_zk_prijedlog,
        "ZK brisanje upisa": pristojba_zk_brisanje,
        "Tužba u upravnom sporu": pristojba_upravni_spor,
        "Punomoć": pristojba_punomoc,
    }

    st.markdown("---")

    if tip in vps_postupci:
        vps = st.number_input(
            "Vrijednost predmeta spora (EUR)",
            min_value=0.0,
            step=100.0,
            key="prist_vps",
        )
        if vps > 0:
            iznos = vps_postupci[tip](vps)
            st.markdown("### Rezultat")
            col1, col2 = st.columns(2)
            col1.metric("Sudska pristojba", format_eur(iznos))
            col2.metric("VPS", format_eur(vps))

            # Dodatne informacije
            if tip == "Tužba (parnični postupak)":
                st.caption("Tbr. 1 Tarife sudskih pristojbi")
                st.markdown(
                    f"- Pristojba za presudu (Tbr. 2): **{format_eur(iznos)}** (isti iznos)\n"
                    f"- Pristojba za žalbu (Tbr. 3): **{format_eur(iznos * 2)}** (dvostruko)\n"
                    f"- Pristojba za reviziju (Tbr. 4): **{format_eur(iznos * 3)}** (trostruko)"
                )
            elif tip == "Žalba na presudu":
                st.caption("Tbr. 3 - Dvostruki iznos pristojbe za tužbu")
            elif tip == "Revizija":
                st.caption("Tbr. 4 - Trostruki iznos pristojbe za tužbu")
            elif "Ovrha" in tip:
                st.caption("Tbr. 10/11 - Polovica pristojbe za tužbu, min. 6,64 EUR")
        else:
            st.warning("Unesite vrijednost predmeta spora za izračun pristojbe.")
    else:
        iznos = fiksni_postupci[tip]()
        st.markdown("### Rezultat")
        st.metric("Sudska pristojba", format_eur(iznos))
        if tip == "ZK prijedlog (uknjižba, zabilježba...)":
            st.caption("Tbr. 20 - Fiksna pristojba za ZK prijedlog")
        elif tip == "ZK brisanje upisa":
            st.caption("Tbr. 21 - Fiksna pristojba za brisanje")
        elif tip == "Tužba u upravnom sporu":
            st.caption("Tbr. 30 - Fiksna pristojba za upravni spor")

    # Tablica svih tarifa
    with st.expander("Tablica svih tarifnih razreda"):
        st.markdown("**Pristojba za tužbu (Tbr. 1) prema VPS:**")
        razredi = [
            ("do 664 EUR", "13,27 EUR"),
            ("664 - 1.327 EUR", "26,54 EUR"),
            ("1.327 - 3.318 EUR", "53,09 EUR"),
            ("3.318 - 6.636 EUR", "79,63 EUR"),
            ("6.636 - 13.272 EUR", "119,45 EUR"),
            ("13.272 - 26.544 EUR", "199,08 EUR"),
            ("26.544 - 66.361 EUR", "398,17 EUR"),
            ("66.361 - 132.722 EUR", "663,61 EUR"),
            ("preko 132.722 EUR", "663,61 + 1% razlike, max 4.404,15 EUR"),
        ]
        tablica = "| VPS | Pristojba |\n|---|---|\n"
        for vps_r, prist_r in razredi:
            tablica += f"| {vps_r} | {prist_r} |\n"
        st.markdown(tablica)

        st.markdown(
            "\n**Ostali tarifni brojevi:**\n"
            "- Tbr. 2 (presuda) = Tbr. 1\n"
            "- Tbr. 3 (žalba) = 2 x Tbr. 1\n"
            "- Tbr. 4 (revizija) = 3 x Tbr. 1\n"
            "- Tbr. 10/11 (ovrha) = 0.5 x Tbr. 1, min 6,64 EUR\n"
            "- Tbr. 12 (prigovor ovrhe) = Tbr. 1\n"
            "- Tbr. 20 (ZK prijedlog) = 33,18 EUR\n"
            "- Tbr. 21 (ZK brisanje) = 13,27 EUR\n"
            "- Tbr. 30 (upravni spor) = 26,54 EUR\n"
            "- Tbr. 40 (punomoć) = 6,64 EUR"
        )

    # Oslobodenja
    with st.expander("Oslobođenja od pristojbi"):
        st.markdown("Sljedeći postupci su **oslobođeni** sudskih pristojbi:")
        for oslobodenje in OSLOBODENJA:
            st.markdown(f"- {oslobodenje}")
