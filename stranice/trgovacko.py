# -----------------------------------------------------------------------------
# STRANICA: Trgovacko pravo
# Drustveni ugovor, Odluka skupstine, Prijenos udjela, NDA, Zapisnik uprave
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, zaglavlje_sastavljaca, prikazi_dokument
from generatori.trgovacko import (
    generiraj_drustveni_ugovor,
    generiraj_odluku_skupstine,
    generiraj_prijenos_udjela,
    generiraj_nda,
    generiraj_zapisnik_uprave,
)


def render_trgovacko():
    """Glavna render funkcija za modul Trgovacko pravo."""
    st.header("Trgovačko pravo")

    zaglavlje_sastavljaca()

    kategorija = st.radio(
        "Odaberite dokument:",
        [
            "Društveni ugovor d.o.o.",
            "Odluka skupštine / jednog člana",
            "Prijenos poslovnog udjela",
            "Ugovor o povjerljivosti (NDA)",
            "Zapisnik sjednice uprave",
        ],
        horizontal=True,
    )

    if kategorija == "Društveni ugovor d.o.o.":
        _render_drustveni_ugovor()
    elif kategorija == "Odluka skupštine / jednog člana":
        _render_odluka_skupstine()
    elif kategorija == "Prijenos poslovnog udjela":
        _render_prijenos_udjela()
    elif kategorija == "Ugovor o povjerljivosti (NDA)":
        _render_nda()
    elif kategorija == "Zapisnik sjednice uprave":
        _render_zapisnik_uprave()


def _render_drustveni_ugovor():
    """Društveni ugovor d.o.o. - ZTD čl. 387+."""
    st.info("Zahtijevana forma: Javnobilježnički akt ili solemnizacija (ZTD čl. 387+)")

    st.subheader("Podaci o društvu")
    c1, c2 = st.columns(2)
    tvrtka = c1.text_input("Tvrtka (puni naziv)", key="du_tvrtka",
                           help="Puni naziv društva s oznakom pravnog oblika (npr. 'Primjer d.o.o.').")
    skracena = c2.text_input("Skraćena tvrtka", key="du_skracena",
                             help="Skraćeni naziv koji se koristi u poslovnom prometu.")
    c1, c2 = st.columns(2)
    sjediste = c1.text_input("Sjedište", "Zagreb", key="du_sjediste",
                             help="Mjesto sjedišta društva. Mora biti na području RH.")
    temeljni_kapital = c2.number_input(
        "Temeljni kapital (EUR)", min_value=2500.0, value=2500.0, key="du_kapital",
        help="Minimalni temeljni kapital za d.o.o. je 2.500,00 EUR (čl. 389. ZTD)."
    )
    djelatnosti = st.text_area("Djelatnosti (NKD)", key="du_djelatnosti", height=100,
                               help="Navedite djelatnosti prema Nacionalnoj klasifikaciji djelatnosti (NKD 2007).")
    c1, c2 = st.columns(2)
    trajanje = c1.selectbox("Trajanje društva", ["neodređeno", "određeno"], key="du_trajanje")
    zastupanje = c2.selectbox(
        "Zastupanje",
        ["samostalno i pojedinačno", "skupno"],
        key="du_zastupanje",
    )
    mjesto = st.text_input("Mjesto", "Zagreb", key="du_mjesto")

    st.subheader("Osnivači")
    if "osnivaci_du" not in st.session_state:
        st.session_state.osnivaci_du = [{"tekst": "", "udio": 0, "naziv": ""}]

    osnivaci_data = []
    for i, osn in enumerate(st.session_state.osnivaci_du):
        with st.expander(f"Osnivač {i + 1}", expanded=(i < 2)):
            tekst, _, _ = unos_stranke(f"Osnivač {i + 1}", f"du_osn_{i}")
            udio = st.number_input(
                "Poslovni udio (EUR)", min_value=0.0, key=f"du_udio_{i}"
            )
            osnivaci_data.append({"tekst": tekst, "udio": udio, "naziv": f"Osnivač {i + 1}"})

    if st.button("Dodaj osnivača"):
        st.session_state.osnivaci_du.append({"tekst": "", "udio": 0, "naziv": ""})
        st.rerun()

    st.markdown("---")
    if st.button("Generiraj društveni ugovor", type="primary"):
        doc = generiraj_drustveni_ugovor(
            osnivaci_data,
            {
                "tvrtka": tvrtka,
                "skracena_tvrtka": skracena,
                "sjediste": sjediste,
                "temeljni_kapital": temeljni_kapital,
                "djelatnosti": djelatnosti,
                "trajanje": trajanje,
                "zastupanje": zastupanje,
                "mjesto": mjesto,
            },
        )
        prikazi_dokument(doc, "Drustveni_ugovor.docx", "Preuzmi dokument")


def _render_odluka_skupstine():
    """Odluka skupštine / jednog člana društva."""
    with st.expander("Podaci o društvu", expanded=True):
        c1, c2 = st.columns(2)
        tvrtka = c1.text_input("Tvrtka", key="os_tvrtka")
        oib = c2.text_input("OIB društva", max_chars=11, key="os_oib")
        c1, c2 = st.columns(2)
        mbs = c1.text_input("MBS", key="os_mbs")
        sjediste = c2.text_input("Sjedište", key="os_sjediste")

    donositelj = st.radio(
        "Odluku donosi:",
        ["skupština", "jedini_clan"],
        format_func=lambda x: "Skupština društva" if x == "skupština" else "Jedini član društva",
        horizontal=True,
        key="os_donositelj",
    )

    vrsta = st.selectbox(
        "Vrsta odluke",
        [
            "Imenovanje direktora",
            "Razrješenje direktora",
            "Odobrenje godišnjih financijskih izvještaja",
            "Raspodjela dobiti",
            "Izmjena Društvenog ugovora",
            "Ostalo",
        ],
        key="os_vrsta",
    )
    pravni_temelj = st.text_input(
        "Pravni temelj (članak ZTD-a)", "441.", key="os_pt"
    )
    izreka = st.text_area("Izreka odluke", key="os_izreka", height=150)
    obrazlozenje = st.text_area(
        "Obrazloženje (neobavezno)", key="os_obrazlozenje", height=100
    )
    mjesto = st.text_input("Mjesto", "Zagreb", key="os_mjesto")

    st.markdown("---")
    if st.button("Generiraj odluku", type="primary"):
        doc = generiraj_odluku_skupstine(
            {"tvrtka": tvrtka, "oib": oib, "mbs": mbs, "sjediste": sjediste},
            {
                "vrsta": vrsta,
                "donositelj": donositelj,
                "izreka": izreka,
                "obrazlozenje": obrazlozenje,
                "pravni_temelj_clanak": pravni_temelj,
                "mjesto": mjesto,
            },
        )
        prikazi_dokument(doc, "Odluka_skupstine.docx", "Preuzmi dokument")


def _render_prijenos_udjela():
    """Ugovor o prijenosu poslovnog udjela - ZTD čl. 412."""
    st.info("Zahtijevana forma: Javnobilježnička ovjera potpisa (ZTD čl. 412)")

    c1, c2 = st.columns(2)
    with c1:
        prenositelj, _, _ = unos_stranke("PRENOSITELJ", "pu_pre")
    with c2:
        stjecatelj, _, _ = unos_stranke("STJECATELJ", "pu_stj")

    with st.expander("Podaci o društvu", expanded=True):
        c1, c2 = st.columns(2)
        tvrtka = c1.text_input("Tvrtka društva", key="pu_tvrtka")
        oib = c2.text_input("OIB društva", max_chars=11, key="pu_oib")
        c1, c2 = st.columns(2)
        mbs = c1.text_input("MBS", key="pu_mbs")
        sjediste = c2.text_input("Sjedište", key="pu_sjediste")

    st.subheader("Podaci o udjelu")
    c1, c2 = st.columns(2)
    nominalni = c1.number_input(
        "Nominalni iznos udjela (EUR)", min_value=0.0, key="pu_nom"
    )
    cijena = c2.number_input(
        "Cijena prijenosa (EUR)", min_value=0.0, key="pu_cijena"
    )
    nacin_placanja = st.text_area(
        "Način plaćanja (neobavezno)", key="pu_nacin", height=80
    )
    mjesto = st.text_input("Mjesto", "Zagreb", key="pu_mjesto")

    st.markdown("---")
    if st.button("Generiraj ugovor o prijenosu", type="primary"):
        doc = generiraj_prijenos_udjela(
            prenositelj,
            stjecatelj,
            {"tvrtka": tvrtka, "oib": oib, "mbs": mbs, "sjediste": sjediste},
            {
                "nominalni_iznos": nominalni,
                "cijena": cijena,
                "nacin_placanja": nacin_placanja,
                "mjesto": mjesto,
            },
        )
        prikazi_dokument(doc, "Prijenos_udjela.docx", "Preuzmi dokument")


def _render_nda():
    """Ugovor o povjerljivosti (NDA)."""
    vrsta = st.radio(
        "Vrsta NDA:",
        ["uzajamni", "jednostrani"],
        format_func=lambda x: "Uzajamni (obostrani)" if x == "uzajamni" else "Jednostrani",
        horizontal=True,
        key="nda_vrsta",
    )

    c1, c2 = st.columns(2)
    with c1:
        strana_a, _, _ = unos_stranke("STRANA A", "nda_a")
    with c2:
        strana_b, _, _ = unos_stranke("STRANA B", "nda_b")

    opis = st.text_area(
        "Opis povjerljivih informacija",
        placeholder="financijski podaci, poslovni planovi, know-how, popisi klijenata...",
        key="nda_opis",
    )
    c1, c2, c3 = st.columns(3)
    trajanje_razmjene = c1.text_input(
        "Trajanje razmjene", "12 mjeseci", key="nda_tr"
    )
    trajanje_obveze = c2.text_input(
        "Trajanje obveze tajnosti", "3 godine", key="nda_to"
    )
    ugovorna_kazna = c3.number_input(
        "Ugovorna kazna (EUR, 0 = bez)", min_value=0.0, key="nda_kazna"
    )
    mjesto = st.text_input("Mjesto", "Zagreb", key="nda_mjesto")

    st.markdown("---")
    if st.button("Generiraj NDA", type="primary"):
        doc = generiraj_nda(
            strana_a,
            strana_b,
            {
                "vrsta": vrsta,
                "opis_informacija": opis,
                "trajanje_razmjene": trajanje_razmjene,
                "trajanje_obveze": trajanje_obveze,
                "ugovorna_kazna": ugovorna_kazna,
                "mjesto": mjesto,
            },
        )
        prikazi_dokument(doc, "NDA.docx", "Preuzmi dokument")


def _render_zapisnik_uprave():
    """Zapisnik sjednice uprave."""
    with st.expander("Podaci o društvu", expanded=True):
        c1, c2 = st.columns(2)
        tvrtka = c1.text_input("Tvrtka", key="zu_tvrtka")
        oib = c2.text_input("OIB društva", max_chars=11, key="zu_oib")
        c1, c2 = st.columns(2)
        mbs = c1.text_input("MBS", key="zu_mbs")
        sjediste = c2.text_input("Sjedište", key="zu_sjediste")

    st.subheader("Podaci o sjednici")
    c1, c2, c3 = st.columns(3)
    mjesto = c1.text_input("Mjesto održavanja", "Zagreb", key="zu_mjesto")
    vrijeme_pocetak = c2.text_input("Početak", "10:00", key="zu_poc")
    vrijeme_kraj = c3.text_input("Završetak", "11:00", key="zu_kraj")

    prisutni = st.text_input("Prisutni članovi uprave", key="zu_prisutni")
    c1, c2 = st.columns(2)
    odsutni = c1.text_input("Odsutni (neobavezno)", key="zu_odsutni")
    predsjednik_uprave = c2.text_input("Predsjednik uprave", key="zu_predsjednik")
    zapisnicar = st.text_input("Zapisničar (neobavezno)", key="zu_zap")

    st.subheader("Dnevni red")
    if "dnevni_red_zu" not in st.session_state:
        st.session_state.dnevni_red_zu = [
            {"naslov": "", "rasprava": "", "odluka": "", "glasovi": "jednoglasno"}
        ]

    dnevni_red = []
    for i, tocka in enumerate(st.session_state.dnevni_red_zu):
        with st.expander(f"Točka {i + 1}", expanded=True):
            naslov = st.text_input("Naslov točke", key=f"zu_naslov_{i}")
            rasprava = st.text_area("Rasprava", key=f"zu_rasprava_{i}", height=80)
            odluka = st.text_area("Odluka", key=f"zu_odluka_{i}", height=80)
            glasovi = st.selectbox(
                "Glasovanje",
                ["jednoglasno", "većinom glasova", "nije glasovano"],
                key=f"zu_glasovi_{i}",
            )
            dnevni_red.append({
                "naslov": naslov,
                "rasprava": rasprava,
                "odluka": odluka,
                "glasovi": glasovi,
            })

    if st.button("Dodaj točku dnevnog reda"):
        st.session_state.dnevni_red_zu.append(
            {"naslov": "", "rasprava": "", "odluka": "", "glasovi": "jednoglasno"}
        )
        st.rerun()

    st.markdown("---")
    if st.button("Generiraj zapisnik", type="primary"):
        doc = generiraj_zapisnik_uprave(
            {"tvrtka": tvrtka, "oib": oib, "mbs": mbs, "sjediste": sjediste},
            {
                "mjesto": mjesto,
                "vrijeme_pocetak": vrijeme_pocetak,
                "vrijeme_kraj": vrijeme_kraj,
                "prisutni": prisutni,
                "odsutni": odsutni,
                "predsjednik_uprave": predsjednik_uprave,
                "zapisnicar": zapisnicar,
                "dnevni_red": dnevni_red,
            },
        )
        prikazi_dokument(doc, "Zapisnik_uprave.docx", "Preuzmi dokument")
