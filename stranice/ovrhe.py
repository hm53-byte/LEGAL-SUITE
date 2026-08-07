# -----------------------------------------------------------------------------
# STRANICA: Ovrsno pravo - svi dokumenti
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, prikazi_dokument, odabir_suda, unos_tocaka, zaglavlje_sastavljaca, napuni_primjerom, doc_selectbox, audit_kwargs
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
    napuni_primjerom('ovrha', '')

    with st.expander("Pregled strukture dokumenta", expanded=False):
        st.markdown("""
**Dokument će sadržavati:**
- Zaglavlje — javni bilježnik, ovrhovoditelj i ovršenik
- Uvod — prijedlog za ovrhu temeljem vjerodostojne isprave (čl. 278. OZ)
- Vjerodostojna isprava — naziv, datum i iznos glavnice
- Tražbina — glavnica, zatezne kamate od datuma dospijeća (čl. 29. ZOO)
- Troškovnik — odvjetnička nagrada, nagrada JB-u, PDV, sudska pristojba
- Prijedlog ovrhe — sredstvo i predmet ovrhe (novčana sredstva)
- Potpis predlagatelja
        """)

    jb = st.text_input("Javni bilježnik (Ime, Prezime, Grad)", placeholder="Ivan Horvat, Zagreb",
                       help="Javni bilježnik kojem se podnosi prijedlog za ovrhu na temelju vjerodostojne isprave (čl. 278. OZ).")

    col1, col2 = st.columns(2)
    with col1:
        o1, _, _ = unos_stranke("OVRHOVODITELJ (Vjerovnik)", "o1")
    with col2:
        o2, _, _ = unos_stranke("OVRŠENIK (Dužnik)", "o2")

    st.subheader("Dugovanje - vjerodostojne isprave")
    st.caption("Dodajte jednu ili više isprava na temelju kojih tražite ovrhu.")

    # Dinamicke isprave
    isprave_key = "ovrha_isprave_count"
    if isprave_key not in st.session_state:
        st.session_state[isprave_key] = 1

    ukupna_glavnica = 0.0
    isprave_tekst = []
    for idx in range(st.session_state[isprave_key]):
        with st.container():
            if st.session_state[isprave_key] > 1:
                st.markdown(f"**Isprava {idx + 1}**")
            c1, c2, c3 = st.columns(3)
            isp_opis = c1.text_input("Vjerodostojna isprava", placeholder="Račun br. 100-2024",
                                     key=f"ovrha_isp_opis_{idx}",
                                     help="Račun, mjenica, ček, izvadak iz poslovnih knjiga ili druga isprava po čl. 279. OZ.")
            isp_datum = c2.date_input("Datum isprave", key=f"ovrha_isp_dat_{idx}")
            isp_glavnica = c3.number_input("Glavnica (EUR)", min_value=0.0, key=f"ovrha_isp_glav_{idx}")
            isp_dospjece = st.date_input("Datum dospijeća", key=f"ovrha_isp_dosp_{idx}",
                                          help="Od ovog datuma teku zatezne kamate.")
            if isp_opis:
                isprave_tekst.append({
                    'opis': isp_opis,
                    'datum': isp_datum.strftime('%d.%m.%Y.'),
                    'glavnica': isp_glavnica,
                    'dospjece': isp_dospjece.strftime('%d.%m.%Y.'),
                })
                ukupna_glavnica += isp_glavnica
            if idx < st.session_state[isprave_key] - 1:
                st.markdown("---")

    col_a, col_r = st.columns(2)
    with col_a:
        if st.session_state[isprave_key] < 20:
            if st.button("+ Dodaj ispravu", key="ovrha_add_isp"):
                st.session_state[isprave_key] += 1
                st.rerun()
    with col_r:
        if st.session_state[isprave_key] > 1:
            if st.button("- Ukloni zadnju", key="ovrha_rem_isp"):
                st.session_state[isprave_key] -= 1
                st.rerun()

    # Za kompatibilnost s generatorom koristimo prvu ispravu ili spojimo sve
    if isprave_tekst:
        opis_isprave = ", ".join(f"{isp['opis']} od {isp['datum']}" for isp in isprave_tekst)
        glavnica = ukupna_glavnica
        dat_racuna_str = isprave_tekst[0]['datum']
        dospjece_str = isprave_tekst[0]['dospjece']
    else:
        opis_isprave = ""
        glavnica = 0.0
        dat_racuna_str = ""
        dospjece_str = ""

    st.subheader("Troškovnik")
    predlozena_pristojba = pristojba_ovrha_jb(glavnica) if glavnica > 0 else 0.0
    if predlozena_pristojba > 0:
        st.info(f"Pristojba za ovrhu kod javnog bilježnika (polovica pristojbe za tužbu, min 6,64 EUR): **{predlozena_pristojba:,.2f} EUR**")
    ct1, ct2, ct3 = st.columns(3)
    trosak_odvjetnik = ct1.number_input("Odvjetnička nagrada (EUR)", 0.0,
                                         help="Nagrada odvjetniku za sastav prijedloga za ovrhu.")
    trosak_jb_nagrada = ct2.number_input("Nagrada javnom bilježniku (EUR)", 0.0,
                                          help="Nagrada javnom bilježniku za provođenje ovrhe.")
    trosak_pdv = (trosak_odvjetnik + trosak_jb_nagrada) * 0.25 if ct3.checkbox("Obračunaj PDV?") else 0.0

    if st.button("Generiraj ovršni prijedlog", type="primary"):
        trazbina = {
            'glavnica': glavnica,
            'datum_racuna': dat_racuna_str,
            'dospjece': dospjece_str,
        }
        troskovnik = {
            'stavka': trosak_odvjetnik,
            'materijalni': trosak_jb_nagrada,
            'pdv': trosak_pdv,
            'pristojba': predlozena_pristojba,
        }
        doc = generiraj_ovrhu_pro(jb, o1, o2, trazbina, opis_isprave, troskovnik)
        audit_input = {
            "javni_biljeznik": jb,
            "ovrhovoditelj_html": o1,
            "ovrsenik_html": o2,
            "trazbina": trazbina,
            "opis_isprave": opis_isprave,
            "isprave_detail": isprave_tekst,
            "troskovnik": troskovnik,
        }
        prikazi_dokument(doc, "Ovrha.docx", "Preuzmi dokument",
                         **audit_kwargs("ovrha_vjerodostojna", audit_input, "ovrhe"))


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

    st.subheader("Razlozi prigovora")
    st.caption("Označite uobičajene razloge i/ili dodajte vlastite točke obrazloženja.")

    # Uobicajeni razlozi prigovora (čl. 58. OZ)
    r_ne_postoji = st.checkbox("Tražbina ne postoji (nikada nije ni nastala)", key="pr_r1")
    r_nije_dospjela = st.checkbox("Tražbina nije dospjela", key="pr_r2")
    r_placeno = st.checkbox("Tražbina je već podmirena (plaćena)", key="pr_r3")
    r_zastara = st.checkbox("Tražbina je zastarjela", key="pr_r4")
    r_isprava = st.checkbox("Isprava nije vjerodostojna", key="pr_r5")
    r_kompenzacija = st.checkbox("Tražbina je prestala kompenzacijom (prijebojem)", key="pr_r6")

    uobicajeni = []
    if r_ne_postoji:
        uobicajeni.append("Tražbina iz vjerodostojne isprave ne postoji - obveza između stranaka nikada nije nastala.")
    if r_nije_dospjela:
        uobicajeni.append("Tražbina nije dospjela - rok za ispunjenje obveze nije istekao.")
    if r_placeno:
        uobicajeni.append("Tražbina je već u cijelosti podmirena, što se dokazuje priloženim dokazima o uplati.")
    if r_zastara:
        uobicajeni.append("Tražbina je zastarjela sukladno odredbama Zakona o obveznim odnosima.")
    if r_isprava:
        uobicajeni.append("Isprava na temelju koje je doneseno rješenje o ovrsi nije vjerodostojna isprava u smislu čl. 279. Ovršnog zakona.")
    if r_kompenzacija:
        uobicajeni.append("Tražbina je prestala kompenzacijom (prijebojem) s protutražbinom Ovršenika.")

    st.markdown("**Dodatno obrazloženje** *(detaljniji opis razloga)*")
    dodatne_tocke = unos_tocaka(
        "Obrazloženje", "pr_obrazlozenje",
        placeholder="Detaljnije obrazložite razlog prigovora...",
        min_tocaka=1, max_tocaka=10, height=100,
    )

    # Spoji sve razloge u jedan tekst
    svi_razlozi = uobicajeni + dodatne_tocke
    razlozi = "\n\n".join(f"{i+1}. {r}" for i, r in enumerate(svi_razlozi)) if svi_razlozi else ""

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
        podaci = {
            'poslovni_broj': poslovni_broj,
            'datum_rjesenja': datum_rjesenja.strftime('%d.%m.%Y.'),
            'javni_bilježnik': jb,
            'razlozi': razlozi,
            'mjesto': mjesto,
        }
        doc = generiraj_prigovor_ovrhe(sud, ovrsenik, ovrhovoditelj, podaci, troskovi)
        audit_input = {
            "sud": sud,
            "ovrsenik_html": ovrsenik,
            "ovrhovoditelj_html": ovrhovoditelj,
            "podaci": podaci,
            "troskovnik": troskovi,
        }
        prikazi_dokument(doc, "Prigovor_ovrha.docx", "Preuzmi dokument",
                         **audit_kwargs("prigovor_ovrhe", audit_input, "ovrhe"))


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
    sredstvo_ovrhe = st.selectbox(
        "Sredstvo ovrhe",
        [
            ("novčana sredstva", "Novčana sredstva (računi kod banaka)"),
            ("nekretnina", "Nekretnina"),
            ("plaća", "Plaća i stalna primanja"),
            ("pokretnine", "Pokretnine"),
            ("vise_sredstava", "Više sredstava ovrhe"),
        ],
        format_func=lambda x: x[1],
        key="ooi_sredstvo",
        help="Odaberite na čemu se provodi ovrha. Može se odabrati više sredstava.",
    )

    # Ako je više sredstava, omogući unos
    if sredstvo_ovrhe[0] == "vise_sredstava":
        st.caption("Navedite sredstva ovrhe po točkama.")
        sredstva_tocke = unos_tocaka(
            "Sredstvo ovrhe", "ooi_sredstva",
            placeholder="Npr. Novčana sredstva na svim računima kod banaka...",
            min_tocaka=1, max_tocaka=5, height=60,
        )
        sredstvo_za_gen = "\n".join(sredstva_tocke) if sredstva_tocke else "novčana sredstva"
    else:
        sredstvo_za_gen = sredstvo_ovrhe[0]

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
        podaci = {
            'ovrsna_isprava': ovrsna_isprava,
            'poslovni_broj_isprave': poslovni_broj_isprave,
            'datum_isprave': datum_isprave.strftime('%d.%m.%Y.'),
            'glavnica': glavnica,
            'kamate_od': kamate_od.strftime('%d.%m.%Y.'),
            'sredstvo_ovrhe': sredstvo_za_gen,
            'mjesto': mjesto,
        }
        troskovnik = {
            'stavka': trosak_stavka,
            'pdv': trosak_pdv,
            'pristojba': trosak_pristojba,
        }
        doc = generiraj_ovrhu_ovrsna_isprava(sud, o1, o2, podaci, troskovnik)
        audit_input = {
            "sud": sud,
            "ovrhovoditelj_html": o1,
            "ovrsenik_html": o2,
            "podaci": podaci,
            "troskovnik": troskovnik,
        }
        prikazi_dokument(doc, "Ovrha_ovrsna_isprava.docx", "Preuzmi dokument",
                         **audit_kwargs("ovrha_ovrsna_isprava", audit_input, "ovrhe"))


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
        podaci = {
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
        }
        troskovnik = {
            'stavka': trosak_stavka,
            'pdv': trosak_pdv,
            'pristojba': trosak_pristojba,
        }
        doc = generiraj_ovrhu_na_nekretnini(sud, o1, o2, podaci, troskovnik)
        audit_input = {
            "sud": sud,
            "ovrhovoditelj_html": o1,
            "ovrsenik_html": o2,
            "podaci": podaci,
            "troskovnik": troskovnik,
        }
        prikazi_dokument(doc, "Ovrha_nekretnina.docx", "Preuzmi dokument",
                         **audit_kwargs("ovrha_nekretnina", audit_input, "ovrhe"))


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
        podaci = {
            'ovrsna_isprava': ovrsna_isprava,
            'poslovni_broj_isprave': poslovni_broj_isprave,
            'datum_isprave': datum_isprave.strftime('%d.%m.%Y.'),
            'glavnica': glavnica,
            'kamate_od': kamate_od.strftime('%d.%m.%Y.'),
            'poslodavac_ovrs': poslodavac_ovrs,
            'mjesto': mjesto,
        }
        troskovnik = {
            'stavka': trosak_stavka,
            'pdv': trosak_pdv,
            'pristojba': trosak_pristojba,
        }
        doc = generiraj_ovrhu_na_placi(sud, o1, o2, podaci, troskovnik)
        audit_input = {
            "sud": sud,
            "ovrhovoditelj_html": o1,
            "ovrsenik_html": o2,
            "podaci": podaci,
            "troskovnik": troskovnik,
        }
        prikazi_dokument(doc, "Ovrha_placa.docx", "Preuzmi dokument",
                         **audit_kwargs("ovrha_placa", audit_input, "ovrhe"))


def _render_obustava_ovrhe():
    """Prijedlog za obustavu ovršnog postupka."""
    sud = odabir_suda("Nadležni sud", vrsta="opcinski", key="ob_sud")
    poslovni_broj_spisa = st.text_input("Poslovni broj spisa", placeholder="Ovr-000/2024", key="ob_pbr")

    col1, col2 = st.columns(2)
    ovrhovoditelj_tekst = col1.text_input("Ovrhovoditelj", key="ob_ovrhovoditelj")
    ovrsenik_tekst = col2.text_input("Ovršenik", key="ob_ovrsenik")

    razlog = st.selectbox("Razlog obustave", ["namirenje", "nagodba", "ostalo"], key="ob_razlog",
                          help="Najčešći razlozi: tražbina je namirena, stranke su sklopile nagodbu, ili drugi razlog.")
    razlog_tekst = ""
    if razlog == "ostalo":
        st.markdown("**Obrazloženje razloga obustave**")
        razlog_tocke = unos_tocaka(
            "Razlog", "ob_razlog_tocke",
            placeholder="Navedite razlog zašto se traži obustava ovršnog postupka...",
            min_tocaka=1, max_tocaka=5, height=80,
        )
        razlog_tekst = "\n\n".join(razlog_tocke) if razlog_tocke else ""

    ima_zabilježbu = st.checkbox("Postoji zabilježba ovrhe u zemljišnoj knjizi", key="ob_zabilježba")

    mjesto = st.text_input("Mjesto", "Zagreb", key="ob_mjesto")

    if st.button("Generiraj prijedlog za obustavu", type="primary", key="ob_btn"):
        podaci = {
            'poslovni_broj_spisa': poslovni_broj_spisa,
            'ovrhovoditelj': ovrhovoditelj_tekst,
            'ovrsenik': ovrsenik_tekst,
            'razlog': razlog,
            'razlog_tekst': razlog_tekst,
            'ima_zabilježbu': ima_zabilježbu,
            'mjesto': mjesto,
        }
        doc = generiraj_obustavu_ovrhe(sud, podaci)
        audit_input = {"sud": sud, "podaci": podaci}
        prikazi_dokument(doc, "Obustava_ovrhe.docx", "Preuzmi dokument",
                         **audit_kwargs(f"obustava_ovrhe_{razlog}", audit_input, "ovrhe"))


def _render_privremena_mjera():
    """Prijedlog za privremenu mjeru."""
    sud = odabir_suda("Nadležni sud", vrsta="opcinski", key="pm_sud")

    col1, col2 = st.columns(2)
    with col1:
        pred, _, _ = unos_stranke("PREDLAGATELJ OSIGURANJA", "pm_pred")
    with col2:
        prot, _, _ = unos_stranke("PROTIVNIK OSIGURANJA", "pm_prot")

    vrsta_trazbine = st.selectbox("Vrsta tražbine", ["novčana", "nenovčana"], key="pm_vrsta")

    st.markdown("**Fumus boni iuris** *(vjerojatnost postojanja tražbine)*")
    st.caption("Navedite činjenice i dokaze koji čine vjerojatnim da tražbina postoji.")
    fumus_tocke = unos_tocaka(
        "Vjerojatnost tražbine", "pm_fumus",
        placeholder="Npr. Predlagatelj je s Protivnikom sklopio Ugovor o kupoprodaji od 01.01.2025...",
        min_tocaka=1, max_tocaka=10, height=100,
    )
    fumus_boni_iuris = "\n\n".join(f"{i+1}. {t}" for i, t in enumerate(fumus_tocke)) if fumus_tocke else ""

    st.markdown("**Periculum in mora** *(opasnost za ostvarenje tražbine)*")
    st.caption("Navedite zašto postoji opasnost da bez privremene mjere tražbina neće moći biti naplaćena.")
    periculum_tocke = unos_tocaka(
        "Opasnost", "pm_periculum",
        placeholder="Npr. Protivnik osiguranja ubrzano rasprodaje svoju imovinu...",
        min_tocaka=1, max_tocaka=10, height=100,
    )
    periculum_in_mora = "\n\n".join(f"{i+1}. {t}" for i, t in enumerate(periculum_tocke)) if periculum_tocke else ""

    mjera = st.selectbox(
        "Predložena mjera",
        [
            ("zabrana_raspolaganja", "Zabrana raspolaganja imovinom"),
            ("blokada_racuna", "Blokada bankovnih računa"),
            ("zabrana_otudenja", "Zabrana otuđenja i opterećenja nekretnina"),
            ("ostalo", "Drugo (ručni unos)"),
        ],
        format_func=lambda x: x[1],
        key="pm_mjera",
    )
    poslovni_broj_parnice = st.text_input("Poslovni broj parnice (neobavezno)", key="pm_parnica")

    st.subheader("Troškovnik")
    ct1, ct2 = st.columns(2)
    trosak_stavka = ct1.number_input("Sastav podneska (EUR)", 0.0, key="pm_stavka")
    trosak_pdv = trosak_stavka * 0.25 if ct1.checkbox("Dodaj PDV (25%)", key="pm_pdv") else 0.0
    trosak_pristojba = ct2.number_input("Sudska pristojba (EUR)", 0.0, key="pm_pristojba")

    mjesto = st.text_input("Mjesto", "Zagreb", key="pm_mjesto")

    if st.button("Generiraj prijedlog za privremenu mjeru", type="primary", key="pm_btn"):
        podaci = {
            'vrsta_trazbine': vrsta_trazbine,
            'fumus_boni_iuris': fumus_boni_iuris,
            'periculum_in_mora': periculum_in_mora,
            'mjera': mjera[0],
            'poslovni_broj_parnice': poslovni_broj_parnice,
            'mjesto': mjesto,
        }
        troskovnik = {
            'stavka': trosak_stavka,
            'pdv': trosak_pdv,
            'pristojba': trosak_pristojba,
        }
        doc = generiraj_privremenu_mjeru(sud, pred, prot, podaci, troskovnik)
        audit_input = {
            "sud": sud,
            "predlagatelj_html": pred,
            "protivnik_html": prot,
            "podaci": podaci,
            "troskovnik": troskovnik,
        }
        prikazi_dokument(doc, "Privremena_mjera.docx", "Preuzmi dokument",
                         **audit_kwargs("privremena_mjera", audit_input, "ovrhe"))


def render_ovrhe():
    st.header("Ovršno pravo")

    zaglavlje_sastavljaca()

    tip = doc_selectbox(
        "Odaberite dokument",
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
