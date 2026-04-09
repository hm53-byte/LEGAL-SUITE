# -----------------------------------------------------------------------------
# STRANICA: Obiteljsko pravo
# Sporazumni razvod, Tuzba za razvod, Bracni ugovor, Roditeljska skrb,
# Ugovor o uzdrzavanju
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, odabir_suda, zaglavlje_sastavljaca, prikazi_dokument, doc_selectbox
from generatori.obiteljsko import (
    generiraj_sporazum_razvod,
    generiraj_tuzbu_razvod,
    generiraj_bracni_ugovor,
    generiraj_roditeljsku_skrb,
    generiraj_ugovor_uzdrzavanje,
)


def render_obiteljsko():
    """Glavna render funkcija za modul Obiteljsko pravo."""
    st.header("Obiteljsko pravo")

    zaglavlje_sastavljaca()

    kategorija = doc_selectbox(
        "Odaberite dokument",
        [
            "Prijedlog za sporazumni razvod braka",
            "Tužba za razvod braka",
            "Bračni / predbračni ugovor",
            "Sporazum o roditeljskoj skrbi",
            "Ugovor o uzdržavanju",
        ],
    )

    if kategorija == "Prijedlog za sporazumni razvod braka":
        _render_sporazum_razvod()
    elif kategorija == "Tužba za razvod braka":
        _render_tuzba_razvod()
    elif kategorija == "Bračni / predbračni ugovor":
        _render_bracni_ugovor()
    elif kategorija == "Sporazum o roditeljskoj skrbi":
        _render_roditeljska_skrb()
    elif kategorija == "Ugovor o uzdržavanju":
        _render_ugovor_uzdrzavanje()


# ---- 1. Sporazumni razvod braka ----

def _render_sporazum_razvod():
    """Prijedlog za sporazumni razvod braka - ObZ čl. 50-55."""
    st.info(
        "Sporazumni razvod braka: bračni drugovi zajednički podnose prijedlog. "
        "Obavezno prethodno savjetovanje kod CZSS-a (ObZ čl. 321-331)."
    )

    c1, c2 = st.columns(2)
    with c1:
        predlagatelj1, _, _ = unos_stranke("PREDLAGATELJ 1", "sr_p1")
    with c2:
        predlagatelj2, _, _ = unos_stranke("PREDLAGATELJ 2", "sr_p2")

    st.subheader("Podaci o braku")
    c1, c2 = st.columns(2)
    with c1:
        sud = odabir_suda("Naslovni sud", vrsta="opcinski", key="sr_sud")
    mjesto_braka = c2.text_input("Mjesto sklapanja braka", key="sr_mjesto_braka")
    datum_braka = st.date_input("Datum sklapanja braka", key="sr_datum_braka")

    ima_savjetovanje = st.checkbox(
        "Provedeno obvezno savjetovanje kod CZSS-a", key="sr_savjetovanje"
    )

    st.subheader("Zajednička djeca")
    if "djeca_sr" not in st.session_state:
        st.session_state.djeca_sr = []

    djeca_data = []
    for i in range(len(st.session_state.djeca_sr)):
        with st.expander(f"Dijete {i + 1}", expanded=True):
            c1, c2 = st.columns(2)
            ime = c1.text_input("Ime i prezime", key=f"sr_dijete_ime_{i}")
            datum_r = c2.text_input(
                "Datum rođenja (dd.mm.gggg.)", key=f"sr_dijete_dr_{i}"
            )
            djeca_data.append({"ime": ime, "datum_rodjenja": datum_r})

    if st.button("Dodaj dijete", key="sr_dodaj_dijete"):
        st.session_state.djeca_sr.append({})
        st.rerun()

    plan_roditeljske_skrbi = st.text_area(
        "Plan o zajedničkoj roditeljskoj skrbi (ako ima djece)",
        key="sr_plan",
        height=120,
        placeholder="Navesti s kim djeca žive, raspored kontakta s drugim roditeljem, uzdržavanje...",
    )

    petitum = st.text_area(
        "Petitum (prijedlog odluke suda)",
        key="sr_petitum",
        height=100,
        placeholder="Predlažemo da sud donese rješenje o razvodu braka...",
    )

    st.markdown("---")
    if st.button("Generiraj prijedlog za sporazumni razvod", type="primary"):
        doc = generiraj_sporazum_razvod(
            predlagatelj1,
            predlagatelj2,
            {
                "mjesto": sud,
                "datum_braka": datum_braka.strftime('%d.%m.%Y.'),
                "mjesto_braka": mjesto_braka,
                "djeca": djeca_data,
                "ima_savjetovanje": ima_savjetovanje,
                "plan_roditeljske_skrbi": plan_roditeljske_skrbi,
                "petitum": petitum,
            },
        )
        prikazi_dokument(doc, "Sporazumni_razvod.docx", "Preuzmi dokument")


# ---- 2. Tuzba za razvod braka ----

def _render_tuzba_razvod():
    """Tužba za razvod braka - ObZ čl. 47-49."""
    st.info(
        "Tužba za razvod braka: podnosi jedan bračni drug. "
        "Obavezno prethodno savjetovanje kod CZSS-a (ObZ čl. 321-331)."
    )

    c1, c2 = st.columns(2)
    with c1:
        tuzitelj, _, _ = unos_stranke("TUŽITELJ", "tr_tuz")
    with c2:
        tuzenik, _, _ = unos_stranke("TUŽENIK", "tr_tuzenik")

    st.subheader("Podaci o braku i postupku")
    c1, c2 = st.columns(2)
    with c1:
        sud = odabir_suda("Naslovni sud", vrsta="opcinski", key="tr_sud")
    c1, c2 = st.columns(2)
    datum_braka = c1.date_input("Datum sklapanja braka", key="tr_datum_braka")
    mjesto_braka = c2.text_input("Mjesto sklapanja braka", key="tr_mjesto_braka")

    ima_savjetovanje = st.checkbox(
        "Provedeno obvezno savjetovanje kod CZSS-a", key="tr_savjetovanje"
    )

    razlog = st.text_area(
        "Razlog za razvod braka (obrazloženje)",
        key="tr_razlog",
        height=150,
        placeholder="Bračni odnosi su teško i trajno poremećeni...",
    )

    st.subheader("Zajednička djeca")
    if "djeca_tr" not in st.session_state:
        st.session_state.djeca_tr = []

    djeca_data = []
    for i in range(len(st.session_state.djeca_tr)):
        with st.expander(f"Dijete {i + 1}", expanded=True):
            c1, c2 = st.columns(2)
            ime = c1.text_input("Ime i prezime", key=f"tr_dijete_ime_{i}")
            datum_r = c2.text_input(
                "Datum rođenja (dd.mm.gggg.)", key=f"tr_dijete_dr_{i}"
            )
            djeca_data.append({"ime": ime, "datum_rodjenja": datum_r})

    if st.button("Dodaj dijete", key="tr_dodaj_dijete"):
        st.session_state.djeca_tr.append({})
        st.rerun()

    zahtjev_djeca = st.text_area(
        "Zahtjev glede djece (neobavezno)",
        key="tr_zahtjev_djeca",
        height=100,
        placeholder="Zahtjev da se dijete povjeri na stanovanje tužitelju, uzdržavanje...",
    )

    vps = st.number_input(
        "Vrijednost predmeta spora (EUR)", min_value=0.0, value=0.0, key="tr_vps"
    )

    st.markdown("---")
    if st.button("Generiraj tužbu za razvod braka", type="primary"):
        doc = generiraj_tuzbu_razvod(
            tuzitelj,
            tuzenik,
            {
                "mjesto": sud,
                "sud": sud,
                "datum_braka": datum_braka.strftime('%d.%m.%Y.'),
                "mjesto_braka": mjesto_braka,
                "djeca": djeca_data,
                "razlog": razlog,
                "ima_savjetovanje": ima_savjetovanje,
                "zahtjev_djeca": zahtjev_djeca,
                "vps": vps,
            },
        )
        prikazi_dokument(doc, "Tuzba_razvod_braka.docx", "Preuzmi dokument")


# ---- 3. Bracni / predbracni ugovor ----

def _render_bracni_ugovor():
    """Bračni / predbračni ugovor - ObZ čl. 40-46."""
    st.info(
        "Bračni ugovor mora biti sklopljen u pisanom obliku i ovjeren kod javnog bilježnika "
        "(ObZ čl. 40). Clausula intabulandi je potrebna za nekretnine."
    )

    vrsta = st.selectbox(
        "Vrsta ugovora",
        ["bracni", "predbracni", "dioba"],
        format_func=lambda x: {
            "bracni": "Bračni ugovor",
            "predbracni": "Predbračni ugovor",
            "dioba": "Ugovor o diobi bračne stečevine",
        }[x],
        key="bu_vrsta",
    )

    c1, c2 = st.columns(2)
    with c1:
        strana1, _, _ = unos_stranke("STRANA 1 (muž/budući muž)", "bu_s1")
    with c2:
        strana2, _, _ = unos_stranke("STRANA 2 (žena/buduća žena)", "bu_s2")

    mjesto = st.text_input("Mjesto", "Zagreb", key="bu_mjesto")

    clausula = st.checkbox(
        "Clausula intabulandi (za nekretnine)",
        value=True,
        key="bu_clausula",
    )

    st.subheader("Imovina")
    if "imovina_bu" not in st.session_state:
        st.session_state.imovina_bu = [{}]

    imovina_data = []
    for i in range(len(st.session_state.imovina_bu)):
        with st.expander(f"Imovina {i + 1}", expanded=True):
            opis = st.text_area(
                "Opis imovine",
                key=f"bu_imov_opis_{i}",
                height=80,
                placeholder="Stan u Zagrebu, ul. Ilica 10, površine 65 m²...",
            )
            c1, c2 = st.columns(2)
            vrsta_imov = c1.selectbox(
                "Vrsta",
                ["nekretnina", "pokretnina"],
                key=f"bu_imov_vrsta_{i}",
            )
            vlasnik = c2.selectbox(
                "Pripada",
                ["Strana 1", "Strana 2", "Zajedničko"],
                key=f"bu_imov_vlasnik_{i}",
            )

            zk_podaci = {}
            if vrsta_imov == "nekretnina":
                st.markdown("*Zemljišnoknjižni podaci:*")
                c1, c2, c3 = st.columns(3)
                ko = c1.text_input("Katastarska općina", key=f"bu_zk_ko_{i}")
                ulozak = c2.text_input("Zk. uložak", key=f"bu_zk_ul_{i}")
                cestica = c3.text_input("Čestica", key=f"bu_zk_cs_{i}")
                zk_podaci = {"ko": ko, "ulozak": ulozak, "cestica": cestica}

            imovina_data.append({
                "opis": opis,
                "vrsta": vrsta_imov,
                "vlasnik": vlasnik,
                "zk_podaci": zk_podaci,
            })

    if st.button("Dodaj imovinu", key="bu_dodaj_imovinu"):
        st.session_state.imovina_bu.append({})
        st.rerun()

    st.markdown("---")
    if st.button("Generiraj bračni ugovor", type="primary"):
        doc = generiraj_bracni_ugovor(
            strana1,
            strana2,
            {
                "mjesto": mjesto,
                "vrsta": vrsta,
                "imovina_items": imovina_data,
                "clausula_intabulandi": clausula,
            },
        )
        prikazi_dokument(doc, "Bracni_ugovor.docx", "Preuzmi dokument")


# ---- 4. Sporazum o roditeljskoj skrbi ----

def _render_roditeljska_skrb():
    """Sporazum o roditeljskoj skrbi - ObZ čl. 104-112."""
    st.info(
        "Sporazum o roditeljskoj skrbi uređuje stanovanje djeteta, raspored kontakta "
        "s drugim roditeljem i uzdržavanje (ObZ čl. 104-112)."
    )

    c1, c2 = st.columns(2)
    with c1:
        roditelj1, _, _ = unos_stranke("RODITELJ 1", "rs_r1")
    with c2:
        roditelj2, _, _ = unos_stranke("RODITELJ 2", "rs_r2")

    mjesto = st.text_input("Mjesto", "Zagreb", key="rs_mjesto")

    st.subheader("Djeca")
    if "djeca_rs" not in st.session_state:
        st.session_state.djeca_rs = [{}]

    djeca_data = []
    for i in range(len(st.session_state.djeca_rs)):
        with st.expander(f"Dijete {i + 1}", expanded=True):
            c1, c2, c3 = st.columns(3)
            ime = c1.text_input("Ime i prezime", key=f"rs_dijete_ime_{i}")
            datum_r = c2.text_input(
                "Datum rođenja (dd.mm.gggg.)", key=f"rs_dijete_dr_{i}"
            )
            oib = c3.text_input("OIB djeteta", max_chars=11, key=f"rs_dijete_oib_{i}")
            djeca_data.append({
                "ime": ime,
                "datum_rodjenja": datum_r,
                "oib": oib,
            })

    if st.button("Dodaj dijete", key="rs_dodaj_dijete"):
        st.session_state.djeca_rs.append({})
        st.rerun()

    st.subheader("Stanovanje i kontakt")
    stanovanje_kod = st.radio(
        "Dijete/djeca stanuju kod:",
        [1, 2],
        format_func=lambda x: f"Roditelj {x}",
        horizontal=True,
        key="rs_stanovanje",
    )
    adresa_djeteta = st.text_input(
        "Adresa stanovanja djeteta", key="rs_adresa_djeteta"
    )

    raspored_kontakta = st.text_area(
        "Raspored kontakta s drugim roditeljem",
        key="rs_raspored",
        height=120,
        placeholder="Svaki drugi vikend (petak 17h - nedjelja 19h), srijedom od 16h do 19h...",
    )
    c1, c2 = st.columns(2)
    praznici = c1.text_area(
        "Raspored za praznike",
        key="rs_praznici",
        height=100,
        placeholder="Božić parnih godina kod Roditelja 1, neparnih kod Roditelja 2...",
    )
    ljetni_odmor = c2.text_area(
        "Ljetni odmor",
        key="rs_ljetni",
        height=100,
        placeholder="Svaki roditelj provodi 2 tjedna ljetnog odmora s djecom...",
    )

    st.subheader("Uzdržavanje")
    c1, c2 = st.columns(2)
    alimentacija_iznos = c1.number_input(
        "Mjesečni iznos uzdržavanja (EUR)", min_value=0.0, key="rs_alim_iznos"
    )
    alimentacija_datum = c2.text_input(
        "Datum dospijeća (npr. 15. u mjesecu)", key="rs_alim_datum"
    )
    alimentacija_iban = st.text_input("IBAN za uplate", key="rs_alim_iban", max_chars=21)

    posebne_odredbe = st.text_area(
        "Posebne odredbe (neobavezno)",
        key="rs_posebne",
        height=100,
        placeholder="Obveze roditelja glede zdravlja, obrazovanja, izvannastavnih aktivnosti...",
    )

    st.markdown("---")
    if st.button("Generiraj sporazum o roditeljskoj skrbi", type="primary"):
        doc = generiraj_roditeljsku_skrb(
            roditelj1,
            roditelj2,
            {
                "mjesto": mjesto,
                "djeca": djeca_data,
                "stanovanje_kod": stanovanje_kod,
                "adresa_djeteta": adresa_djeteta,
                "raspored_kontakta": raspored_kontakta,
                "praznici": praznici,
                "ljetni_odmor": ljetni_odmor,
                "alimentacija_iznos": alimentacija_iznos,
                "alimentacija_datum_dospijeca": alimentacija_datum,
                "alimentacija_iban": alimentacija_iban,
                "posebne_odredbe": posebne_odredbe,
            },
        )
        prikazi_dokument(doc, "Roditeljska_skrb.docx", "Preuzmi dokument")


# ---- 5. Ugovor o uzdrzavanju ----

def _render_ugovor_uzdrzavanje():
    """Ugovor o uzdržavanju - ObZ čl. 285-305."""
    st.info(
        "Ugovor o uzdržavanju djeteta mora biti ovjeren kod javnog bilježnika "
        "i ima snagu ovršne isprave - clausula exequendi (ObZ čl. 305)."
    )

    c1, c2 = st.columns(2)
    with c1:
        obveznik, _, _ = unos_stranke("OBVEZNIK UZDRŽAVANJA", "uu_obv")
    with c2:
        primatelj, _, _ = unos_stranke("PRIMATELJ UZDRŽAVANJA", "uu_pri")

    mjesto = st.text_input("Mjesto", "Zagreb", key="uu_mjesto")

    st.subheader("Podaci o djetetu")
    c1, c2 = st.columns(2)
    dijete_ime = c1.text_input("Ime i prezime djeteta", key="uu_dijete_ime")
    dijete_datum = c2.text_input(
        "Datum rođenja djeteta (dd.mm.gggg.)", key="uu_dijete_dr"
    )
    zakonski_zastupnik = st.text_input(
        "Zakonski zastupnik djeteta (ime i prezime)",
        key="uu_zak_zastupnik",
        help="Roditelj koji zastupa dijete u ovom ugovoru",
    )

    st.subheader("Uzdržavanje")
    c1, c2 = st.columns(2)
    iznos = c1.number_input(
        "Mjesečni iznos uzdržavanja (EUR)", min_value=0.0, key="uu_iznos"
    )
    datum_dospijeca = c2.text_input(
        "Datum dospijeća (npr. 15. u mjesecu)", key="uu_datum_dosp"
    )
    iban = st.text_input("IBAN za uplate", key="uu_iban", max_chars=21)

    clausula = st.checkbox(
        "Clausula exequendi (ovršna klauzula)",
        value=True,
        key="uu_clausula",
        help="Ugovor s ovom klauzulom ima snagu ovršne isprave",
    )

    st.markdown("---")
    if st.button("Generiraj ugovor o uzdržavanju", type="primary"):
        doc = generiraj_ugovor_uzdrzavanje(
            obveznik,
            primatelj,
            {
                "mjesto": mjesto,
                "iznos_mjesecno": iznos,
                "datum_dospijeca": datum_dospijeca,
                "iban": iban,
                "dijete_ime": dijete_ime,
                "dijete_datum_rodjenja": dijete_datum,
                "zakonski_zastupnik": zakonski_zastupnik,
                "clausula_exequendi": clausula,
            },
        )
        prikazi_dokument(doc, "Ugovor_uzdrzavanje.docx", "Preuzmi dokument")
