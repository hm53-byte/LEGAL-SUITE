# -----------------------------------------------------------------------------
# STRANICA: Trgovacko pravo
# Drustveni ugovor, Odluka skupstine, Prijenos udjela, NDA, Zapisnik uprave
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, zaglavlje_sastavljaca, prikazi_dokument, clause_builder, doc_selectbox
from generatori.trgovacko import (
    generiraj_drustveni_ugovor,
    generiraj_odluku_skupstine,
    generiraj_prijenos_udjela,
    generiraj_nda,
    generiraj_zapisnik_uprave,
    generiraj_prodaju_poduzeca,
    SEKCIJE_PRODAJA_PODUZECA,
)


def render_trgovacko():
    """Glavna render funkcija za modul Trgovacko pravo."""
    st.header("Trgovačko pravo")

    zaglavlje_sastavljaca()

    kategorija = doc_selectbox(
        "Odaberite dokument",
        [
            "Društveni ugovor d.o.o.",
            "Odluka skupštine / jednog člana",
            "Prijenos poslovnog udjela",
            "Ugovor o povjerljivosti (NDA)",
            "Zapisnik sjednice uprave",
            "Ugovor o prodaji poduzeća",
        ],
        key="trg_kategorija",
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
    elif kategorija == "Ugovor o prodaji poduzeća":
        _render_prodaja_poduzeca()


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


def _render_prodaja_poduzeca():
    """Ugovor o prodaji poduzeća kao organizirane gospodarske cjeline - ZOO, ZTD, ZR."""
    st.info(
        "Prodaja poduzeća kao organizirane gospodarske cjeline (ZTD čl. 301.a, ZOO, ZR čl. 137). "
        "Za prijenos nekretnina obvezna je clausula intabulandi; preporučuje se javnobilježnička solemnizacija."
    )

    c1, c2 = st.columns(2)
    with c1:
        prodavatelj, _, _ = unos_stranke("PRODAVATELJ", "pp_prod")
    with c2:
        kupac, _, _ = unos_stranke("KUPAC", "pp_kup")

    c1, c2 = st.columns(2)
    mjesto = c1.text_input("Mjesto sklapanja", "Zagreb", key="pp_mjesto")
    sud_mjesto = c2.text_input("Nadležni sud (grad)", "Zagrebu", key="pp_sud")

    djelatnost = st.text_area(
        "Djelatnost poduzeća",
        placeholder="npr. proizvodnjom i prodajom prehrambenih proizvoda",
        key="pp_djelatnost",
        height=60,
    )

    st.subheader("Kupoprodajna cijena i plaćanje")
    c1, c2 = st.columns(2)
    kupoprodajna_cijena = c1.number_input(
        "Ukupna kupoprodajna cijena (EUR)", min_value=0.0, key="pp_cijena",
        help="Ukupna ugovorena cijena za prodaju poduzeća."
    )
    rok_placanja = c2.number_input(
        "Rok plaćanja ostatka (dana)", min_value=1, value=30, key="pp_rok"
    )

    with st.expander("Prijeboj (kompenzacija) — neobavezno"):
        c1, c2 = st.columns(2)
        prijeboj_iznos = c1.number_input(
            "Iznos prijeboja (EUR, 0 = bez)", min_value=0.0, key="pp_prijeboj_iznos",
            help="Dio cijene koji se namiruje prijebojem tražbine Kupca prema Prodavatelju."
        )
        prijeboj_opis = c2.text_area(
            "Opis tražbine koja se prebija", key="pp_prijeboj_opis", height=68,
            placeholder="npr. tražbina po ugovoru o prodaji sirovina od dana X, s dospijećem Y"
        )

    st.subheader("Imovina koja se prenosi")
    st.caption("Označite vrste imovine koje se prenose i opišite ih.")

    with st.expander("A) Nekretnine"):
        ima_nekretninu = st.checkbox("Prenose se nekretnine", key="pp_ima_nekr")
        nekretnina_opis = st.text_area(
            "Opis nekretnine(a)", key="pp_nekr_opis", height=80,
            placeholder="npr. Zgrada na z.k. čestici br. X, upisana u z.k. ulošku br. Y, k.o. Z..."
        )
        ima_hipoteku = st.checkbox("Nekretnina je opterećena hipotekom", key="pp_ima_hip")
        c1, c2 = st.columns(2)
        hipoteka_iznos = c1.number_input("Iznos hipoteke (EUR)", min_value=0.0, key="pp_hip_iznos")
        hipoteka_banka = c2.text_input("Hipotekarni vjerovnik (banka)", key="pp_hip_banka")

    with st.expander("B) Tražbine (cesija)"):
        ima_trabinu = st.checkbox("Prenose se tražbine cesijom", key="pp_ima_trab")
        trabina_opis = st.text_area(
            "Opis tražbine(a)", key="pp_trab_opis", height=80,
            placeholder="npr. Tražbina u iznosu od EUR X prema društvu Y, s dospijećem Z..."
        )

    with st.expander("C) Mjenice (indosament)"):
        ima_mjenice = st.checkbox("Prenose se mjenice", key="pp_ima_mj")
        mjenice_opis = st.text_area(
            "Opis mjenica", key="pp_mj_opis", height=80,
            placeholder="npr. 4 trasirane mjenice, svaka na iznos EUR X, trasirao Y..."
        )

    with st.expander("D) Poslovni udjeli u drugim društvima"):
        ima_poslovnih_udjela = st.checkbox("Prenose se poslovni udjeli", key="pp_ima_pu")
        poslovni_udjeli_opis = st.text_area(
            "Opis poslovnih udjela", key="pp_pu_opis", height=80,
            placeholder="npr. Poslovni udio od EUR X u društvu Y (Z% temeljnog kapitala)..."
        )

    with st.expander("E) Pokretnine"):
        ima_pokretnine = st.checkbox("Prenose se pokretnine", key="pp_ima_pokr")
        pokretnine_opis = st.text_area(
            "Opis pokretnina", key="pp_pokr_opis", height=80,
            placeholder="npr. Vozila, strojevi, oprema, zalihe — prema popisu u Prilogu..."
        )

    with st.expander("F) Vrijednosni papiri"):
        ima_vrijednosnih_papira = st.checkbox("Prenose se vrijednosni papiri", key="pp_ima_vp")
        vrijednosni_papiri_opis = st.text_area(
            "Opis vrijednosnih papira", key="pp_vp_opis", height=80,
            placeholder="npr. 100 dionica društva X, serije A, kontrolni brojevi Y-Z..."
        )

    with st.expander("G) Novčana sredstva na žiro-računu"):
        prenosi_novac = st.checkbox("Prenose se novčana sredstva", key="pp_ima_novac")
        novcana_sredstva = st.number_input(
            "Iznos novčanih sredstava (EUR)", min_value=0.0, key="pp_novac_iznos"
        )

    st.subheader("Obveze i radnici")
    preuzete_obveze = st.text_area(
        "Preuzete obveze (neobavezno)",
        key="pp_obveze",
        height=80,
        placeholder="npr. Dug prema dobavljaču X u iznosu EUR Y; preuzimanje parničnog postupka Z...",
        help="Navedite specifične obveze koje Kupac preuzima. Ako nema posebnih, ostavite prazno."
    )
    c1, c2 = st.columns(2)
    broj_zaposlenika = c1.number_input(
        "Broj zaposlenika koji se prenose (0 = bez)", min_value=0, key="pp_zaposlenici",
        help="Sukladno čl. 137. ZR-a, zaposlenici se prenose po sili zakona."
    )

    tekuci_ugovori = st.text_area(
        "Tekući ugovori koji se prenose (neobavezno)",
        key="pp_ugovori",
        height=80,
        placeholder="npr. Ugovor s dobavljačem X o isporuci Y; ugovor s kupcem Z o prodaji W...",
        help="Ustupanje ugovora sukladno čl. 127.–131. ZOO-a. Zahtijeva suglasnost druge ugovorne strane."
    )

    st.subheader("Posebne odredbe")

    with st.expander("Zabrana natjecanja (Non-Compete) — neobavezno"):
        zabrana_natjecanja = st.checkbox("Ugovori se zabrana natjecanja", key="pp_zabrana")
        c1, c2 = st.columns(2)
        zabrana_trajanje = c1.text_input(
            "Trajanje zabrane", "3 (tri) godine", key="pp_zab_trajanje"
        )
        zabrana_kazna = c2.number_input(
            "Ugovorna kazna za kršenje (EUR)", min_value=0.0, value=50000.0, key="pp_zab_kazna"
        )

    with st.expander("Preživjela jamstva prema trećim osobama — neobavezno"):
        ima_prezivjelih_jamstava = st.checkbox(
            "Prodavatelj ima preživjela jamstva prema trećim osobama",
            key="pp_prezivjela",
            help="Aktivira mehanizam supstitucije jamstava, fiducijarnog depozita i negativne suglasnosti."
        )

    st.subheader("Odgovornost i završne odredbe")
    c1, c2, c3 = st.columns(3)
    cap_odgovornosti_posto = c1.number_input(
        "Cap odgovornosti (%)", min_value=1, max_value=100, value=20, key="pp_cap",
        help="Ukupna odgovornost Prodavatelja po jamstvima ograničena je na ovaj postotak kupoprodajne cijene."
    )
    survival_period = c2.number_input(
        "Survival Period (godina)", min_value=1, max_value=10, value=2, key="pp_survival",
        help="Rok u kojemu Kupac mora podnijeti zahtjeve temeljem izjava i jamstava."
    )
    ugovorna_kazna = c3.number_input(
        "Ugovorna kazna za odustanak (EUR)", min_value=0.0, value=100000.0, key="pp_uk"
    )

    st.subheader("Struktura dokumenta")
    with st.expander("Odaberi i poredaj odjeljke", expanded=False):
        odabrane_sekcije = clause_builder("pp_sekcije", SEKCIJE_PRODAJA_PODUZECA)

    st.markdown("---")
    if st.button("Generiraj ugovor o prodaji poduzeća", type="primary"):
        doc = generiraj_prodaju_poduzeca(
            prodavatelj,
            kupac,
            {
                "mjesto": mjesto,
                "sud_mjesto": sud_mjesto,
                "djelatnost": djelatnost,
                "kupoprodajna_cijena": kupoprodajna_cijena,
                "rok_placanja": rok_placanja,
                "prijeboj_iznos": prijeboj_iznos,
                "prijeboj_opis": prijeboj_opis,
                "ima_nekretninu": ima_nekretninu,
                "nekretnina_opis": nekretnina_opis,
                "ima_hipoteku": ima_hipoteku,
                "hipoteka_iznos": hipoteka_iznos,
                "hipoteka_banka": hipoteka_banka,
                "ima_trabinu": ima_trabinu,
                "trabina_opis": trabina_opis,
                "ima_mjenice": ima_mjenice,
                "mjenice_opis": mjenice_opis,
                "ima_poslovnih_udjela": ima_poslovnih_udjela,
                "poslovni_udjeli_opis": poslovni_udjeli_opis,
                "ima_pokretnine": ima_pokretnine,
                "pokretnine_opis": pokretnine_opis,
                "ima_vrijednosnih_papira": ima_vrijednosnih_papira,
                "vrijednosni_papiri_opis": vrijednosni_papiri_opis,
                "prenosi_novac": prenosi_novac,
                "novcana_sredstva": novcana_sredstva,
                "preuzete_obveze": preuzete_obveze,
                "broj_zaposlenika": broj_zaposlenika,
                "tekuci_ugovori": tekuci_ugovori,
                "zabrana_natjecanja": zabrana_natjecanja,
                "zabrana_trajanje": zabrana_trajanje,
                "zabrana_kazna": zabrana_kazna,
                "ima_prezivjelih_jamstava": ima_prezivjelih_jamstava,
                "cap_odgovornosti_posto": cap_odgovornosti_posto,
                "survival_period_godina": survival_period,
                "ugovorna_kazna": ugovorna_kazna,
            },
            sekcije_redoslijed=odabrane_sekcije,
        )
        prikazi_dokument(doc, "Ugovor_o_prodaji_poduzeca.docx", "Preuzmi dokument")


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
