# -----------------------------------------------------------------------------
# STRANICA: Upravno pravo
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, prikazi_dokument, odabir_suda, unos_tocaka
from generatori.upravno import (
    generiraj_zalbu_zup,
    generiraj_tuzbu_zus,
    generiraj_zahtjev_informacije,
    generiraj_prigovor_predstavku,
)


def _render_zalba_zup():
    """Žalba u upravnom postupku (ZUP)."""
    st.info(
        "Rok za žalbu u upravnom postupku je **15 dana** od dana dostave "
        "prvostupanjskog rješenja (čl. 109. ZUP-a)."
    )

    col1, col2 = st.columns(2)
    with col1:
        zalitelj, _, _ = unos_stranke("ŽALITELJ", "zup_z")

    with col2:
        st.markdown("**TIJELA**")
        prvostupanjsko_tijelo = st.text_input(
            "Prvostupanjsko tijelo (koje je donijelo rješenje)",
            key="zup_prvostupanjsko",
            placeholder="Upravni odjel za...",
        )
        drugostupanjsko_tijelo = st.text_input(
            "Drugostupanjsko tijelo (kojemu se žalba podnosi)",
            key="zup_drugostupanjsko",
            placeholder="Ministarstvo...",
        )

    st.subheader("Podaci o rješenju")
    c1, c2, c3 = st.columns(3)
    klasa = c1.text_input("KLASA", key="zup_klasa", placeholder="UP/I-000-00/00-00/0")
    urbroj = c2.text_input("URBROJ", key="zup_urbroj", placeholder="000-00-00-0")
    datum_rjesenja = c3.date_input("Datum rješenja", key="zup_datum")

    mjesto = st.text_input("Mjesto", "Zagreb", key="zup_mjesto")

    st.subheader("Sadržaj žalbe")
    st.caption("Svaki razlog žalbe navedite u zasebnu točku. Možete pridružiti dokaz svakoj točki.")
    razlozi_tocke = unos_tocaka(
        "Razlog žalbe", "zup_razlozi",
        placeholder="Npr. Prvostupanjsko tijelo nije pravilno primijenilo čl. XX Zakona o...",
        min_tocaka=1, max_tocaka=10, height=100,
        s_dokazima=True,
        dokaz_placeholder="Npr. Rješenje KLASA: ..., dopis od ...",
    )
    if razlozi_tocke:
        parts = []
        for i, t in enumerate(razlozi_tocke):
            line = f"{i+1}. {t['tekst']}"
            if t.get('dokaz'):
                line += f"\n   Dokaz: {t['dokaz']}"
            parts.append(line)
        razlozi = "\n\n".join(parts)
    else:
        razlozi = ""

    zalbeni_prijedlog = st.radio(
        "Žalbeni prijedlog",
        ["poništi i vrati", "izmijeni"],
        key="zup_prijedlog",
        horizontal=True,
    )

    st.markdown("---")
    if st.button("Generiraj žalbu (ZUP)", type="primary", key="zup_btn"):
        doc = generiraj_zalbu_zup(
            zalitelj,
            {
                'mjesto': mjesto,
                'drugostupanjsko_tijelo': drugostupanjsko_tijelo,
                'prvostupanjsko_tijelo': prvostupanjsko_tijelo,
                'klasa': klasa,
                'urbroj': urbroj,
                'datum_rjesenja': datum_rjesenja.strftime('%d.%m.%Y.'),
                'razlozi': razlozi,
                'zalbeni_prijedlog': zalbeni_prijedlog,
            },
        )
        prikazi_dokument(doc, "Zalba_ZUP.docx", "Preuzmi dokument")


def _render_tuzba_zus():
    """Tužba u upravnom sporu (ZUS)."""
    st.info(
        "Rok za podnošenje tužbe u upravnom sporu je **30 dana** od dostave "
        "osporenog rješenja (čl. 24. ZUS-a)."
    )

    col1, col2 = st.columns(2)
    with col1:
        tuzitelj, _, _ = unos_stranke("TUŽITELJ", "zus_t")
    with col2:
        st.markdown("**TUŽENIK (javnopravno tijelo)**")
        tuzenik_tijelo = st.text_input(
            "Naziv javnopravnog tijela",
            key="zus_tuzenik",
            placeholder="Ministarstvo...",
        )

    st.subheader("Nadležni sud")
    sud = odabir_suda("Upravni sud", vrsta="upravni", key="zus_sud")

    st.subheader("Podaci o osporenom rješenju")
    c1, c2, c3 = st.columns(3)
    klasa = c1.text_input("KLASA", key="zus_klasa", placeholder="UP/II-000-00/00-00/0")
    urbroj = c2.text_input("URBROJ", key="zus_urbroj", placeholder="000-00-00-0")
    datum_rjesenja = c3.date_input("Datum rješenja", key="zus_datum")

    mjesto = st.text_input("Mjesto", "Zagreb", key="zus_mjesto")

    st.subheader("Sadržaj tužbe")
    st.caption("Navedite razloge nezakonitosti - svakom možete pridružiti dokaz.")
    razlozi_tocke = unos_tocaka(
        "Razlog nezakonitosti", "zus_razlozi",
        placeholder="Npr. Tuženik nije proveo postupak sukladno čl. XX ZUP-a...",
        min_tocaka=1, max_tocaka=10, height=100,
        s_dokazima=True,
        dokaz_placeholder="Npr. Rješenje, zapisnik, dopis...",
    )
    if razlozi_tocke:
        parts = []
        for i, t in enumerate(razlozi_tocke):
            line = f"{i+1}. {t['tekst']}"
            if t.get('dokaz'):
                line += f"\n   Dokaz: {t['dokaz']}"
            parts.append(line)
        razlozi_nezakonitosti = "\n\n".join(parts)
    else:
        razlozi_nezakonitosti = ""

    tuzbeni_zahtjev = st.radio(
        "Tužbeni zahtjev",
        ["poništenje", "spor pune jurisdikcije"],
        key="zus_zahtjev",
        horizontal=True,
    )

    st.subheader("Dodatni zahtjevi")
    zahtjev_rasprava = st.checkbox("Zahtjev za održavanje usmene rasprave", key="zus_rasprava")
    zahtjev_privremena_mjera = st.checkbox("Zahtjev za privremenu mjeru", key="zus_privremena")

    privremena_mjera_razlog = ""
    if zahtjev_privremena_mjera:
        privremena_mjera_razlog = st.text_area(
            "Razlog za privremenu mjeru",
            key="zus_privremena_razlog",
            height=100,
            placeholder="Navedite razloge zbog kojih je potrebna privremena mjera...",
        )

    st.markdown("---")
    if st.button("Generiraj tužbu (ZUS)", type="primary", key="zus_btn"):
        doc = generiraj_tuzbu_zus(
            tuzitelj,
            tuzenik_tijelo,
            {
                'mjesto': mjesto,
                'sud': sud,
                'klasa': klasa,
                'urbroj': urbroj,
                'datum_rjesenja': datum_rjesenja.strftime('%d.%m.%Y.'),
                'razlozi_nezakonitosti': razlozi_nezakonitosti,
                'zahtjev_rasprava': zahtjev_rasprava,
                'zahtjev_privremena_mjera': zahtjev_privremena_mjera,
                'privremena_mjera_razlog': privremena_mjera_razlog,
                'tuzbeni_zahtjev': tuzbeni_zahtjev,
            },
        )
        prikazi_dokument(doc, "Tuzba_ZUS.docx", "Preuzmi dokument")


def _render_zahtjev_informacije():
    """Zahtjev za pristup informacijama (ZPPI)."""
    st.info(
        "Tijelo javne vlasti dužno je odlučiti o zahtjevu u roku od **15 dana** "
        "od dana podnošenja zahtjeva (čl. 20. ZPPI-a)."
    )

    col1, col2 = st.columns(2)
    with col1:
        podnositelj, _, _ = unos_stranke("PODNOSITELJ ZAHTJEVA", "zppi_p")
    with col2:
        st.markdown("**TIJELO JAVNE VLASTI**")
        tijelo_javne_vlasti = st.text_input(
            "Naziv tijela javne vlasti",
            key="zppi_tijelo",
            placeholder="Ministarstvo..., Grad..., Općina...",
        )

    mjesto = st.text_input("Mjesto", "Zagreb", key="zppi_mjesto")

    st.subheader("Sadržaj zahtjeva")
    opis_informacije = st.text_area(
        "Opis tražene informacije",
        key="zppi_opis",
        height=150,
        placeholder="Opišite informaciju kojoj želite pristupiti...",
    )

    nacin_pristupa = st.radio(
        "Način pristupa informaciji",
        ["neposredan uvid", "pisana dostava", "preslika", "elektronička pošta"],
        key="zppi_nacin",
        horizontal=True,
    )

    st.markdown("---")
    if st.button("Generiraj zahtjev za pristup informacijama", type="primary", key="zppi_btn"):
        doc = generiraj_zahtjev_informacije(
            podnositelj,
            {
                'mjesto': mjesto,
                'tijelo_javne_vlasti': tijelo_javne_vlasti,
                'opis_informacije': opis_informacije,
                'nacin_pristupa': nacin_pristupa,
            },
        )
        prikazi_dokument(doc, "Zahtjev_informacije.docx", "Preuzmi dokument")


def _render_prigovor_predstavka():
    """Prigovor / predstavka na rad javnopravnog tijela."""
    st.info(
        "Čelnik tijela dužan je odgovoriti na prigovor/predstavku u roku od "
        "**30 dana** od dana podnošenja (čl. 122. ZUP-a)."
    )

    col1, col2 = st.columns(2)
    with col1:
        podnositelj, _, _ = unos_stranke("PODNOSITELJ", "pp_p")
    with col2:
        st.markdown("**TIJELO**")
        tijelo = st.text_input(
            "Naziv tijela",
            key="pp_tijelo",
            placeholder="Upravni odjel za...",
        )
        celnik_tijela = st.text_input(
            "Čelnik tijela (ime i funkcija)",
            key="pp_celnik",
            placeholder="Predstojnik..., Pročelnik...",
        )

    mjesto = st.text_input("Mjesto", "Zagreb", key="pp_mjesto")

    st.subheader("Podaci o predmetu")
    c1, c2 = st.columns(2)
    klasa_predmeta = c1.text_input("KLASA predmeta (neobavezno)", key="pp_klasa")
    sluzbenici = c2.text_input(
        "Službenik/ci na čiji se rad odnosi prigovor",
        key="pp_sluzbenici",
        placeholder="Ime i prezime službenika",
    )

    tip = st.radio(
        "Vrsta podneska",
        ["prigovor", "predstavka"],
        key="pp_tip",
        horizontal=True,
    )

    st.markdown("**Opis problema**")
    st.caption("Opišite problem po točkama. Svakoj točki možete pridružiti dokaz.")
    opis_tocke = unos_tocaka(
        "Opis problema", "pp_opis",
        placeholder="Opišite problem, nepravilnost ili nezakonito postupanje...",
        min_tocaka=1, max_tocaka=10, height=100,
        s_dokazima=True,
        dokaz_placeholder="Npr. Dopis, zapisnik, svjedok...",
    )
    if opis_tocke:
        parts = []
        for i, t in enumerate(opis_tocke):
            line = f"{i+1}. {t['tekst']}"
            if t.get('dokaz'):
                line += f"\n   Dokaz: {t['dokaz']}"
            parts.append(line)
        opis_problema = "\n\n".join(parts)
    else:
        opis_problema = ""

    st.markdown("---")
    if st.button("Generiraj prigovor / predstavku", type="primary", key="pp_btn"):
        doc = generiraj_prigovor_predstavku(
            podnositelj,
            {
                'mjesto': mjesto,
                'tijelo': tijelo,
                'celnik_tijela': celnik_tijela,
                'opis_problema': opis_problema,
                'sluzbenici': sluzbenici,
                'klasa_predmeta': klasa_predmeta,
                'tip': tip,
            },
        )
        prikazi_dokument(doc, "Prigovor_predstavka.docx", "Preuzmi dokument")


def render_upravno():
    st.header("Upravno pravo")
    tip = st.selectbox(
        "Odaberite dokument:",
        [
            "Žalba u upravnom postupku (ZUP)",
            "Tužba u upravnom sporu (ZUS)",
            "Zahtjev za pristup informacijama (ZPPI)",
            "Prigovor / predstavka na rad tijela",
        ],
    )

    if tip == "Žalba u upravnom postupku (ZUP)":
        _render_zalba_zup()
    elif tip == "Tužba u upravnom sporu (ZUS)":
        _render_tuzba_zus()
    elif tip == "Zahtjev za pristup informacijama (ZPPI)":
        _render_zahtjev_informacije()
    elif tip == "Prigovor / predstavka na rad tijela":
        _render_prigovor_predstavka()
