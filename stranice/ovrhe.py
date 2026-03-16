# -----------------------------------------------------------------------------
# STRANICA: Ovrsno pravo - svi dokumenti
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, prikazi_dokument, odabir_suda
from pristojbe import pristojba_ovrha_jb, pristojba_ovrha_ovrsna_isprava
from generatori.ovrhe import (
    generiraj_ovrhu_pro,
    generiraj_prigovor_ovrhe,
    generiraj_ovrhu_ovrsna_isprava,
    generiraj_ovrhu_na_nekretnini,
    generiraj_ovrhu_na_placi,
    generiraj_obustavu_ovrhe,
    generiraj_privremenu_mjeru,
)


def _render_prijedlog_ovrhe():
    """Prijedlog za ovrhu na temelju vjerodostojne isprave."""
    jb = st.text_input("Javni bilježnik (Ime, Prezime, Grad)", placeholder="Ivan Horvat, Zagreb",
                       help="Javni bilježnik kojem se podnosi prijedlog za ovrhu na temelju vjerodostojne isprave (čl. 278. OZ).")

    col1, col2 = st.columns(2)
    with col1:
        o1, _, _ = unos_stranke("OVRHOVODITELJ (Vjerovnik)", "o1")
    with col2:
        o2, _, _ = unos_stranke("OVRŠENIK (Dužnik)", "o2")

    st.subheader("Dugovanje")
    c1, c2, c3 = st.columns(3)
    opis_isprave = c1.text_input("Vjerodostojna isprava", placeholder="Račun br. 100-2024",
                                help="Račun, mjenica, ček, izvadak iz poslovnih knjiga ili druga isprava po čl. 279. OZ.")
    dat_racuna = c2.date_input("Datum izdavanja računa",
                               help="Datum kada je izdana vjerodostojna isprava.")
    glavnica = c3.number_input("Glavnica duga (EUR)", min_value=0.0,
                               help="Iznos dospjele nenaplaćene tražbine u EUR.")
    dospjece = st.date_input("Datum dospijeća",
                             help="Datum dospijeća obveze - od ovog datuma teku zatezne kamate.")

    st.subheader("Troškovnik")
    predlozena_pristojba = pristojba_ovrha_jb(glavnica) if glavnica > 0 else 0.0
    if predlozena_pristojba > 0:
        st.info(f"Pristojba za ovrhu JB (½ tužbe, min 6,64): **{predlozena_pristojba:,.2f} EUR** (Tbr. 10)")
    ct1, ct2, ct3 = st.columns(3)
    trosak_odvjetnik = ct1.number_input("Odvjetnik", 0.0)
    trosak_jb_nagrada = ct2.number_input("JB Nagrada", 0.0)
    trosak_pdv = (trosak_odvjetnik + trosak_jb_nagrada) * 0.25 if ct3.checkbox("Obračunaj PDV?") else 0.0

    if st.button("Generiraj ovršni prijedlog", type="primary"):
        doc = generiraj_ovrhu_pro(
            jb, o1, o2,
            {
                'glavnica': glavnica,
                'datum_racuna': dat_racuna.strftime('%d.%m.%Y.'),
                'dospjece': dospjece.strftime('%d.%m.%Y.'),
            },
            opis_isprave,
            {
                'stavka': trosak_odvjetnik,
                'materijalni': trosak_jb_nagrada,
                'pdv': trosak_pdv,
                'pristojba': predlozena_pristojba,
            },
        )
        prikazi_dokument(doc, "Ovrha.docx", "Preuzmi dokument")


def _render_prigovor():
    """Prigovor protiv rješenja o ovrsi na temelju vjerodostojne isprave."""
    sud = odabir_suda("Nadležni sud", vrsta="opcinski", key="pr_sud")

    col1, col2 = st.columns(2)
    with col1:
        ovrsenik, _, _ = unos_stranke("OVRŠENIK (predlagatelj prigovora)", "pr_o")
    with col2:
        ovrhovoditelj, _, _ = unos_stranke("OVRHOVODITELJ (protivna strana)", "pr_ov")

    st.subheader("Podaci o rješenju")
    c1, c2 = st.columns(2)
    poslovni_broj = c1.text_input("Poslovni broj rješenja", placeholder="Ovrv-000/2024",
                                  help="Poslovni broj rješenja o ovrsi koje osporavate.")
    datum_rjesenja = c2.date_input("Datum rješenja o ovrsi",
                                   help="Rok za prigovor je 8 dana od dostave rješenja (čl. 57. OZ).")
    jb = st.text_input("Javni bilježnik koji je donio rješenje", placeholder="Ivan Horvat, Zagreb",
                       help="Javni bilježnik koji je donio rješenje o ovrsi na temelju vjerodostojne isprave.")

    razlozi = st.text_area(
        "Razlozi prigovora",
        placeholder="Navedite razloge zbog kojih osporavate rješenje o ovrsi...",
        height=200,
        help="Razlozi iz čl. 58. OZ: tražbina ne postoji, nije dospjela, isprava nije vjerodostojna, dug je plaćen itd."
    )

    mjesto = st.text_input("Mjesto", "Zagreb")

    st.subheader("Troškovnik")
    add_trosak = st.checkbox("Potražujem troškove postupka")
    troskovi = {'stavka': 0, 'pdv': 0, 'pristojba': 0}
    if add_trosak:
        c1, c2 = st.columns(2)
        troskovi['stavka'] = c1.number_input("Sastav prigovora (EUR)", 0.0)
        if c1.checkbox("Dodaj PDV (25%)"):
            troskovi['pdv'] = troskovi['stavka'] * 0.25
        troskovi['pristojba'] = c2.number_input("Sudska pristojba (EUR)", 0.0)

    if st.button("Generiraj prigovor", type="primary"):
        doc = generiraj_prigovor_ovrhe(
            sud, ovrsenik, ovrhovoditelj,
            {
                'poslovni_broj': poslovni_broj,
                'datum_rjesenja': datum_rjesenja.strftime('%d.%m.%Y.'),
                'javni_bilježnik': jb,
                'razlozi': razlozi,
                'mjesto': mjesto,
            },
            troskovi,
        )
        prikazi_dokument(doc, "Prigovor_ovrha.docx", "Preuzmi dokument")


def _render_ovrha_ovrsna_isprava():
    """Prijedlog za ovrhu na temelju ovršne isprave."""
    sud = odabir_suda("Nadležni sud", vrsta="opcinski", key="ooi_sud")

    col1, col2 = st.columns(2)
    with col1:
        o1, _, _ = unos_stranke("OVRHOVODITELJ", "ooi_o1")
    with col2:
        o2, _, _ = unos_stranke("OVRŠENIK", "ooi_o2")

    st.subheader("Ovršna isprava")
    c1, c2, c3 = st.columns(3)
    ovrsna_isprava = c1.text_input("Ovršna isprava", placeholder="Pravomoćna presuda", key="ooi_isprava")
    poslovni_broj_isprave = c2.text_input("Poslovni broj isprave", placeholder="P-000/2024", key="ooi_pbr")
    datum_isprave = c3.date_input("Datum isprave", key="ooi_dat")

    st.subheader("Tražbina")
    c1, c2 = st.columns(2)
    glavnica = c1.number_input("Glavnica duga (EUR)", min_value=0.0, key="ooi_glav")
    kamate_od = c2.date_input("Kamate od", key="ooi_kam")
    sredstvo_ovrhe = st.selectbox("Sredstvo ovrhe", ["novčana sredstva", "nekretnina", "plaća"], key="ooi_sredstvo")

    st.subheader("Troškovnik")
    predlozena_ooi = pristojba_ovrha_ovrsna_isprava(glavnica) if glavnica > 0 else 0.0
    if predlozena_ooi > 0:
        st.info(f"Pristojba za ovrhu (½ tužbe, min 6,64): **{predlozena_ooi:,.2f} EUR** (Tbr. 11)")
    ct1, ct2 = st.columns(2)
    trosak_stavka = ct1.number_input("Sastav podneska (EUR)", 0.0, key="ooi_stavka")
    trosak_pdv = trosak_stavka * 0.25 if ct1.checkbox("Dodaj PDV (25%)", key="ooi_pdv") else 0.0
    trosak_pristojba = ct2.number_input("Sudska pristojba (EUR)", value=predlozena_ooi, key="ooi_pristojba")

    mjesto = st.text_input("Mjesto", "Zagreb", key="ooi_mjesto")

    if st.button("Generiraj prijedlog za ovrhu", type="primary", key="ooi_btn"):
        doc = generiraj_ovrhu_ovrsna_isprava(
            sud, o1, o2,
            {
                'ovrsna_isprava': ovrsna_isprava,
                'poslovni_broj_isprave': poslovni_broj_isprave,
                'datum_isprave': datum_isprave.strftime('%d.%m.%Y.'),
                'glavnica': glavnica,
                'kamate_od': kamate_od.strftime('%d.%m.%Y.'),
                'sredstvo_ovrhe': sredstvo_ovrhe,
                'mjesto': mjesto,
            },
            {
                'stavka': trosak_stavka,
                'pdv': trosak_pdv,
                'pristojba': trosak_pristojba,
            },
        )
        prikazi_dokument(doc, "Ovrha_ovrsna_isprava.docx", "Preuzmi dokument")


def _render_ovrha_nekretnina():
    """Prijedlog za ovrhu na nekretnini."""
    sud = odabir_suda("Nadležni sud", vrsta="opcinski", key="on_sud")

    col1, col2 = st.columns(2)
    with col1:
        o1, _, _ = unos_stranke("OVRHOVODITELJ", "on_o1")
    with col2:
        o2, _, _ = unos_stranke("OVRŠENIK", "on_o2")

    st.subheader("Ovršna isprava")
    c1, c2, c3 = st.columns(3)
    ovrsna_isprava = c1.text_input("Ovršna isprava", placeholder="Pravomoćna presuda", key="on_isprava")
    poslovni_broj_isprave = c2.text_input("Poslovni broj isprave", placeholder="P-000/2024", key="on_pbr")
    datum_isprave = c3.date_input("Datum isprave", key="on_dat")

    st.subheader("Tražbina")
    c1, c2 = st.columns(2)
    glavnica = c1.number_input("Glavnica duga (EUR)", min_value=0.0, key="on_glav")
    kamate_od = c2.date_input("Kamate od", key="on_kam")

    st.subheader("Nekretnina")
    c1, c2 = st.columns(2)
    ko = c1.text_input("Katastarska općina", key="on_ko")
    ulozak = c2.text_input("Zemljišnoknjižni uložak", key="on_ulozak")
    c3, c4 = st.columns(2)
    cestica = c3.text_input("Katastarska čestica", key="on_cestica")
    opis_nekretnine = c4.text_input("Opis nekretnine", placeholder="Stan, 3-sobni, 75 m²", key="on_opis")

    st.subheader("Troškovnik")
    ct1, ct2 = st.columns(2)
    trosak_stavka = ct1.number_input("Sastav podneska (EUR)", 0.0, key="on_stavka")
    trosak_pdv = trosak_stavka * 0.25 if ct1.checkbox("Dodaj PDV (25%)", key="on_pdv") else 0.0
    trosak_pristojba = ct2.number_input("Sudska pristojba (EUR)", 0.0, key="on_pristojba")

    mjesto = st.text_input("Mjesto", "Zagreb", key="on_mjesto")

    if st.button("Generiraj prijedlog za ovrhu na nekretnini", type="primary", key="on_btn"):
        doc = generiraj_ovrhu_na_nekretnini(
            sud, o1, o2,
            {
                'ovrsna_isprava': ovrsna_isprava,
                'poslovni_broj_isprave': poslovni_broj_isprave,
                'datum_isprave': datum_isprave.strftime('%d.%m.%Y.'),
                'glavnica': glavnica,
                'kamate_od': kamate_od.strftime('%d.%m.%Y.'),
                'ko': ko,
                'ulozak': ulozak,
                'cestica': cestica,
                'opis_nekretnine': opis_nekretnine,
                'mjesto': mjesto,
            },
            {
                'stavka': trosak_stavka,
                'pdv': trosak_pdv,
                'pristojba': trosak_pristojba,
            },
        )
        prikazi_dokument(doc, "Ovrha_nekretnina.docx", "Preuzmi dokument")


def _render_ovrha_placa():
    """Prijedlog za ovrhu na plaći."""
    sud = odabir_suda("Nadležni sud", vrsta="opcinski", key="op_sud")

    col1, col2 = st.columns(2)
    with col1:
        o1, _, _ = unos_stranke("OVRHOVODITELJ", "op_o1")
    with col2:
        o2, _, _ = unos_stranke("OVRŠENIK", "op_o2")

    poslodavac_ovrs = st.text_input("Poslodavac ovršenika", placeholder="Naziv i adresa poslodavca", key="op_poslodavac")

    st.subheader("Ovršna isprava")
    c1, c2, c3 = st.columns(3)
    ovrsna_isprava = c1.text_input("Ovršna isprava", placeholder="Pravomoćna presuda", key="op_isprava")
    poslovni_broj_isprave = c2.text_input("Poslovni broj isprave", placeholder="P-000/2024", key="op_pbr")
    datum_isprave = c3.date_input("Datum isprave", key="op_dat")

    st.subheader("Tražbina")
    c1, c2 = st.columns(2)
    glavnica = c1.number_input("Glavnica duga (EUR)", min_value=0.0, key="op_glav")
    kamate_od = c2.date_input("Kamate od", key="op_kam")

    st.subheader("Troškovnik")
    ct1, ct2 = st.columns(2)
    trosak_stavka = ct1.number_input("Sastav podneska (EUR)", 0.0, key="op_stavka")
    trosak_pdv = trosak_stavka * 0.25 if ct1.checkbox("Dodaj PDV (25%)", key="op_pdv") else 0.0
    trosak_pristojba = ct2.number_input("Sudska pristojba (EUR)", 0.0, key="op_pristojba")

    mjesto = st.text_input("Mjesto", "Zagreb", key="op_mjesto")

    if st.button("Generiraj prijedlog za ovrhu na plaći", type="primary", key="op_btn"):
        doc = generiraj_ovrhu_na_placi(
            sud, o1, o2,
            {
                'ovrsna_isprava': ovrsna_isprava,
                'poslovni_broj_isprave': poslovni_broj_isprave,
                'datum_isprave': datum_isprave.strftime('%d.%m.%Y.'),
                'glavnica': glavnica,
                'kamate_od': kamate_od.strftime('%d.%m.%Y.'),
                'poslodavac_ovrs': poslodavac_ovrs,
                'mjesto': mjesto,
            },
            {
                'stavka': trosak_stavka,
                'pdv': trosak_pdv,
                'pristojba': trosak_pristojba,
            },
        )
        prikazi_dokument(doc, "Ovrha_placa.docx", "Preuzmi dokument")


def _render_obustava_ovrhe():
    """Prijedlog za obustavu ovršnog postupka."""
    sud = odabir_suda("Nadležni sud", vrsta="opcinski", key="ob_sud")
    poslovni_broj_spisa = st.text_input("Poslovni broj spisa", placeholder="Ovr-000/2024", key="ob_pbr")

    col1, col2 = st.columns(2)
    ovrhovoditelj_tekst = col1.text_input("Ovrhovoditelj", key="ob_ovrhovoditelj")
    ovrsenik_tekst = col2.text_input("Ovršenik", key="ob_ovrsenik")

    razlog = st.selectbox("Razlog obustave", ["namirenje", "nagodba", "ostalo"], key="ob_razlog")
    razlog_tekst = ""
    if razlog == "ostalo":
        razlog_tekst = st.text_area("Obrazloženje razloga obustave", key="ob_razlog_tekst", height=150)

    ima_zabilježbu = st.checkbox("Postoji zabilježba ovrhe u zemljišnoj knjizi", key="ob_zabilježba")

    mjesto = st.text_input("Mjesto", "Zagreb", key="ob_mjesto")

    if st.button("Generiraj prijedlog za obustavu", type="primary", key="ob_btn"):
        doc = generiraj_obustavu_ovrhe(
            sud,
            {
                'poslovni_broj_spisa': poslovni_broj_spisa,
                'ovrhovoditelj': ovrhovoditelj_tekst,
                'ovrsenik': ovrsenik_tekst,
                'razlog': razlog,
                'razlog_tekst': razlog_tekst,
                'ima_zabilježbu': ima_zabilježbu,
                'mjesto': mjesto,
            },
        )
        prikazi_dokument(doc, "Obustava_ovrhe.docx", "Preuzmi dokument")


def _render_privremena_mjera():
    """Prijedlog za privremenu mjeru."""
    sud = odabir_suda("Nadležni sud", vrsta="opcinski", key="pm_sud")

    col1, col2 = st.columns(2)
    with col1:
        pred, _, _ = unos_stranke("PREDLAGATELJ OSIGURANJA", "pm_pred")
    with col2:
        prot, _, _ = unos_stranke("PROTIVNIK OSIGURANJA", "pm_prot")

    vrsta_trazbine = st.selectbox("Vrsta tražbine", ["novčana", "nenovčana"], key="pm_vrsta")
    fumus_boni_iuris = st.text_area("Fumus boni iuris (vjerojatnost tražbine)", key="pm_fumus", height=150)
    periculum_in_mora = st.text_area("Periculum in mora (opasnost)", key="pm_periculum", height=150)
    mjera = st.selectbox("Predložena mjera", ["zabrana_raspolaganja", "blokada_racuna", "zabrana_otudenja", "ostalo"], key="pm_mjera")
    poslovni_broj_parnice = st.text_input("Poslovni broj parnice (neobavezno)", key="pm_parnica")

    st.subheader("Troškovnik")
    ct1, ct2 = st.columns(2)
    trosak_stavka = ct1.number_input("Sastav podneska (EUR)", 0.0, key="pm_stavka")
    trosak_pdv = trosak_stavka * 0.25 if ct1.checkbox("Dodaj PDV (25%)", key="pm_pdv") else 0.0
    trosak_pristojba = ct2.number_input("Sudska pristojba (EUR)", 0.0, key="pm_pristojba")

    mjesto = st.text_input("Mjesto", "Zagreb", key="pm_mjesto")

    if st.button("Generiraj prijedlog za privremenu mjeru", type="primary", key="pm_btn"):
        doc = generiraj_privremenu_mjeru(
            sud, pred, prot,
            {
                'vrsta_trazbine': vrsta_trazbine,
                'fumus_boni_iuris': fumus_boni_iuris,
                'periculum_in_mora': periculum_in_mora,
                'mjera': mjera,
                'poslovni_broj_parnice': poslovni_broj_parnice,
                'mjesto': mjesto,
            },
            {
                'stavka': trosak_stavka,
                'pdv': trosak_pdv,
                'pristojba': trosak_pristojba,
            },
        )
        prikazi_dokument(doc, "Privremena_mjera.docx", "Preuzmi dokument")


def render_ovrhe():
    st.header("Ovršno pravo")
    tip = st.selectbox(
        "Odaberite dokument:",
        [
            "Prijedlog za ovrhu (vjerodostojna isprava)",
            "Prigovor protiv rješenja o ovrsi",
            "Ovrha na temelju ovršne isprave",
            "Ovrha na nekretnini",
            "Ovrha na plaći",
            "Obustava ovršnog postupka",
            "Privremena mjera",
        ],
    )

    if tip == "Prijedlog za ovrhu (vjerodostojna isprava)":
        _render_prijedlog_ovrhe()
    elif tip == "Prigovor protiv rješenja o ovrsi":
        _render_prigovor()
    elif tip == "Ovrha na temelju ovršne isprave":
        _render_ovrha_ovrsna_isprava()
    elif tip == "Ovrha na nekretnini":
        _render_ovrha_nekretnina()
    elif tip == "Ovrha na plaći":
        _render_ovrha_placa()
    elif tip == "Obustava ovršnog postupka":
        _render_obustava_ovrhe()
    elif tip == "Privremena mjera":
        _render_privremena_mjera()
