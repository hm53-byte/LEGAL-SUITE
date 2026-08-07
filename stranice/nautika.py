# -----------------------------------------------------------------------------
# STRANICA: Nautika (brodice, jahte)
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, prikazi_dokument, zaglavlje_sastavljaca, audit_kwargs, napuni_primjerom
from generatori.nautika import (
    generiraj_kupoprodaju_brodice,
    generiraj_tabularnu_brodice,
    generiraj_punomoc_prodaje_brodice,
    generiraj_zalog_brodice,
)


def _polja_brodice(prefix):
    """Zajednicka polja za identifikaciju brodice."""
    st.subheader("Identifikacija brodice")
    col1, col2 = st.columns(2)
    with col1:
        naziv = st.text_input("Naziv plovila", key=f"{prefix}_naziv", placeholder="npr. Galeb")
        oznaka = st.text_input("Registracijska oznaka", key=f"{prefix}_oznaka", placeholder="npr. RI-1234")
        luka = st.text_input("Luka upisa", key=f"{prefix}_luka", placeholder="npr. Rijeka")
        kapetanija = st.text_input("Lučka kapetanija", key=f"{prefix}_kap", placeholder="npr. Lučka kapetanija Rijeka")
        proizvodjac = st.text_input("Proizvođač", key=f"{prefix}_proiz", placeholder="npr. Bénéteau")
        model = st.text_input("Model", key=f"{prefix}_model", placeholder="npr. Antares 8")
    with col2:
        god = st.text_input("Godina proizvodnje", key=f"{prefix}_god", placeholder="npr. 2018")
        duljina = st.text_input("Duljina (m)", key=f"{prefix}_dulj", placeholder="npr. 7,80")
        motor = st.text_input("Motor (proizvođač i model)", key=f"{prefix}_mot", placeholder="npr. Mercury Verado 200")
        snaga = st.text_input("Snaga motora (kW)", key=f"{prefix}_snaga", placeholder="npr. 147")
        serijski = st.text_input("Serijski broj trupa (HIN)", key=f"{prefix}_hin", placeholder="opcionalno")

    return {
        'naziv_brodice': naziv,
        'registracijska_oznaka': oznaka,
        'luka_upisa': luka,
        'lucka_kapetanija': kapetanija,
        'proizvodjac': proizvodjac,
        'model': model,
        'godina_proizvodnje': god,
        'duljina_m': duljina,
        'motor': motor,
        'snaga_kw': snaga,
        'serijski_broj_trupa': serijski,
    }


def render_nautika():
    st.header("Nautika — brodice i jahte")
    st.caption("Pravni temelj: Pomorski zakonik (NN 181/04 i izmjene) + ZOO. Upisnik brodica vodi nadležna Lučka kapetanija.")

    zaglavlje_sastavljaca()

    tip = st.selectbox(
        "Vrsta dokumenta",
        [
            "Ugovor o kupoprodaji brodice",
            "Tabularna izjava (clausula intabulandi) za brodicu",
            "Specijalna punomoć za prodaju brodice",
            "Sporazum o zasnivanju založnog prava na brodici",
        ],
        key="naut_tip",
    )

    if tip == "Ugovor o kupoprodaji brodice":
        napuni_primjerom('kupoprodaja_brodice', '')
        col1, col2 = st.columns(2)
        with col1:
            prodavatelj, _, _ = unos_stranke("PRODAVATELJ", "naut_kup_pro")
        with col2:
            kupac, _, _ = unos_stranke("KUPAC", "naut_kup_kup")

        podaci = _polja_brodice("naut_kup_b")

        st.subheader("Uvjeti kupoprodaje")
        c1, c2 = st.columns(2)
        with c1:
            podaci['cijena_eur'] = st.number_input("Kupoprodajna cijena (EUR)", min_value=0.0, step=100.0, key="naut_kup_cij")
            podaci['nacin_placanja'] = st.text_input(
                "Način plaćanja",
                value="jednokratno na transakcijski račun prodavatelja u roku od 8 dana od potpisa Ugovora",
                key="naut_kup_nac",
            )
            podaci['mjesto'] = st.text_input("Mjesto sklapanja", "Zagreb", key="naut_kup_mj")
        with c2:
            podaci['rok_predaje'] = st.text_input("Rok predaje brodice", "8 dana od potpisa Ugovora", key="naut_kup_rok")
            podaci['mjesto_predaje'] = st.text_input("Mjesto predaje (luka)", key="naut_kup_mp", placeholder="npr. ACI marina Opatija")
            podaci['tereti'] = st.text_input("Pravno stanje (tereti)", "bez tereta i prava trećih osoba", key="naut_kup_ter")

        if st.button("Generiraj ugovor", type="primary"):
            doc = generiraj_kupoprodaju_brodice(prodavatelj, kupac, podaci)
            audit_input = {"prodavatelj_html": prodavatelj, "kupac_html": kupac, "podaci": podaci}
            prikazi_dokument(doc, "Ugovor_kupoprodaja_brodice.docx", "Preuzmi ugovor",
                             **audit_kwargs("kupoprodaja_brodice", audit_input, "nautika"))

    elif tip == "Tabularna izjava (clausula intabulandi) za brodicu":
        napuni_primjerom('tabularna_brodice', '')
        col1, col2 = st.columns(2)
        with col1:
            prodavatelj, _, _ = unos_stranke("PRODAVATELJ", "naut_tab_pro")
        with col2:
            kupac, _, _ = unos_stranke("KUPAC", "naut_tab_kup")

        podaci = _polja_brodice("naut_tab_b")

        col_a, col_b = st.columns(2)
        with col_a:
            podaci['datum_ugovora'] = st.text_input("Datum Ugovora o kupoprodaji", key="naut_tab_du", placeholder="dd.mm.yyyy.")
        with col_b:
            podaci['mjesto'] = st.text_input("Mjesto izdavanja", "Zagreb", key="naut_tab_mj")

        if st.button("Generiraj tabularnu", type="primary"):
            doc = generiraj_tabularnu_brodice(prodavatelj, kupac, podaci)
            audit_input = {"prodavatelj_html": prodavatelj, "kupac_html": kupac, "podaci": podaci}
            prikazi_dokument(doc, "Tabularna_brodica.docx", "Preuzmi tabularnu",
                             **audit_kwargs("tabularna_brodice", audit_input, "nautika"))

    elif tip == "Specijalna punomoć za prodaju brodice":
        napuni_primjerom('punomoc_prodaje_brodice', '')
        col1, col2 = st.columns(2)
        with col1:
            vlastodavac, _, _ = unos_stranke("VLASTODAVAC (vlasnik)", "naut_pun_v")
        with col2:
            punomocnik, _, _ = unos_stranke("PUNOMOĆNIK", "naut_pun_p")

        podaci = _polja_brodice("naut_pun_b")

        c1, c2 = st.columns(2)
        with c1:
            podaci['minimalna_cijena_eur'] = st.number_input(
                "Minimalna prihvatljiva cijena (EUR, opcionalno)",
                min_value=0.0, step=100.0, key="naut_pun_min",
                help="Ako 0 — punomoćnik može pregovarati slobodno.",
            )
            podaci['mjesto'] = st.text_input("Mjesto izdavanja", "Zagreb", key="naut_pun_mj")
        with c2:
            podaci['rok_vazenja'] = st.text_input("Rok važenja punomoći", "12 (dvanaest) mjeseci od datuma ovjere", key="naut_pun_rok")

        if st.button("Generiraj punomoć", type="primary"):
            doc = generiraj_punomoc_prodaje_brodice(vlastodavac, punomocnik, podaci)
            audit_input = {"vlastodavac_html": vlastodavac, "punomocnik_html": punomocnik, "podaci": podaci}
            prikazi_dokument(doc, "Punomoc_prodaja_brodice.docx", "Preuzmi punomoć",
                             **audit_kwargs("punomoc_prodaja_brodice", audit_input, "nautika"))

    elif tip == "Sporazum o zasnivanju založnog prava na brodici":
        napuni_primjerom('zalog_brodice', '')
        col1, col2 = st.columns(2)
        with col1:
            vjerovnik, _, _ = unos_stranke("VJEROVNIK", "naut_zal_vj")
        with col2:
            zalozni_duznik, _, _ = unos_stranke("ZALOŽNI DUŽNIK (vlasnik)", "naut_zal_zd")

        podaci = _polja_brodice("naut_zal_b")

        st.subheader("Tražbina koja se osigurava")
        c1, c2 = st.columns(2)
        with c1:
            podaci['iznos_trazbine_eur'] = st.number_input("Iznos tražbine (EUR)", min_value=0.0, step=100.0, key="naut_zal_iz")
            podaci['kamatna_stopa'] = st.text_input("Kamata", "zakonska zatezna kamata", key="naut_zal_kam")
            podaci['mjesto'] = st.text_input("Mjesto sklapanja", "Zagreb", key="naut_zal_mj")
        with c2:
            podaci['rok_dospijeca'] = st.text_input("Rok dospijeća tražbine", key="naut_zal_rd", placeholder="npr. 31.12.2027.")
            podaci['osnova_trazbine'] = st.text_area(
                "Osnova tražbine",
                placeholder="npr. Ugovor o zajmu od dd.mm.yyyy. u iznosu od 50.000 EUR",
                height=80, key="naut_zal_os",
            )

        if st.button("Generiraj sporazum", type="primary"):
            doc = generiraj_zalog_brodice(vjerovnik, zalozni_duznik, podaci)
            audit_input = {"vjerovnik_html": vjerovnik, "zalozni_duznik_html": zalozni_duznik, "podaci": podaci}
            prikazi_dokument(doc, "Zalog_brodica.docx", "Preuzmi sporazum",
                             **audit_kwargs("zalog_brodice", audit_input, "nautika"))
