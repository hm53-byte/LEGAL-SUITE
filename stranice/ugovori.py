# -----------------------------------------------------------------------------
# STRANICA: Ugovori i Odluke
# -----------------------------------------------------------------------------
import streamlit as st
from datetime import date
from pomocne import (
    unos_stranke,
    zaglavlje_sastavljaca,
    prikazi_dokument,
    _rimski_broj,
    doc_selectbox,
    napuni_primjerom,
)
from klauzule import KATEGORIJE, dohvati_klauzule, dohvati_klauzulu_po_nazivu
from generatori.ugovori import (
    generiraj_prilagodeni_ugovor,
    generiraj_ugovor_standard,
    generiraj_ugovor_o_radu,
    generiraj_otkaz,
    generiraj_aneks_ugovora_o_radu,
    generiraj_upozorenje_radniku,
    generiraj_ugovor_rad_na_daljinu,
    generiraj_sporazumni_prestanak,
    generiraj_zabranu_natjecanja,
    generiraj_potvrdu_o_zaposlenju,
)


def _render_slobodna_forma():
    """Slobodna forma - personalizirani ugovor."""
    st.subheader("Izrada ugovora po mjeri")

    if 'custom_contract' not in st.session_state:
        st.session_state.custom_contract = [
            {'naslov': 'Opći uvjeti', 'clanci': ['']}
        ]

    with st.expander("Zaglavlje ugovora", expanded=True):
        col_naslov, col_urbroj = st.columns([2, 1])
        naslov_ugovora = col_naslov.text_input("Naslov ugovora", "UGOVOR O POSLOVNOJ SURADNJI")
        urbroj = col_urbroj.text_input("UrBroj (opcionalno)", placeholder="npr. 2024-01-01")

        c1, c2, c3 = st.columns(3)
        mjesto = c1.text_input("Mjesto sklapanja", "Zagreb")
        datum = c2.date_input("Datum sklapanja")
        rok_vazenja = c3.date_input("Vrijedi do (opcionalno)", value=None)

    with st.expander("Stranke", expanded=True):
        col_s1, col_s2 = st.columns(2)

        with col_s1:
            st.markdown("**Prva strana**")
            uloga1 = st.text_input("Uloga (npr. Naručitelj)", "Naručitelj")
            s1_tekst, _, _ = unos_stranke("Podaci prve strane", "cust_s1")

        with col_s2:
            st.markdown("**Druga strana**")
            uloga2 = st.text_input("Uloga (npr. Izvođač)", "Izvođač")
            s2_tekst, _, _ = unos_stranke("Podaci druge strane", "cust_s2")

    st.markdown("---")
    st.subheader("Sadržaj ugovora")

    for i, poglavlje in enumerate(st.session_state.custom_contract):
        oznaka = _rimski_broj(i + 1)
        st.markdown(f"**Dio {i+1} ({oznaka})**")

        col_pog_naslov, col_pog_btn = st.columns([4, 1])
        novi_naslov = col_pog_naslov.text_input(
            f"Naslov dijela {i+1}", value=poglavlje['naslov'], key=f"naslov_{i}"
        )
        poglavlje['naslov'] = novi_naslov

        if col_pog_btn.button("Obriši dio", key=f"del_sec_{i}"):
            st.session_state.custom_contract.pop(i)
            st.rerun()

        for j, clanak in enumerate(poglavlje['clanci']):
            cl_text = st.text_area(
                f"Članak (Dio {i+1})",
                value=clanak,
                height=100,
                key=f"cl_{i}_{j}",
                placeholder="Unesite tekst članka...",
            )
            st.session_state.custom_contract[i]['clanci'][j] = cl_text

        c_add, _ = st.columns([2, 4])
        if c_add.button(f"Dodaj članak u dio {i+1}", key=f"add_art_{i}"):
            st.session_state.custom_contract[i]['clanci'].append("")
            st.rerun()

        st.divider()

    col_add_sec, col_add_clause = st.columns(2)
    with col_add_sec:
        if st.button("Dodaj novi dio ugovora"):
            st.session_state.custom_contract.append({'naslov': '', 'clanci': ['']})
            st.rerun()

    # Biblioteka standardnih klauzula
    with st.expander("Biblioteka standardnih klauzula", expanded=False):
        kat = st.selectbox("Kategorija klauzule", KATEGORIJE, key="kl_kat")
        klauzule_u_kat = dohvati_klauzule(kat)
        nazivi = [k["naziv"] for k in klauzule_u_kat]
        if nazivi:
            odabrana = st.selectbox("Odaberite klauzulu", nazivi, key="kl_naziv")
            tekst_klauzule = dohvati_klauzulu_po_nazivu(odabrana)
            st.text_area("Pregled klauzule", value=tekst_klauzule, height=120, disabled=True, key="kl_preview")
            if st.button("Dodaj klauzulu kao novi dio ugovora", key="kl_dodaj"):
                st.session_state.custom_contract.append({
                    'naslov': odabrana,
                    'clanci': [tekst_klauzule],
                })
                st.rerun()

    st.markdown("---")
    if st.button("Generiraj ugovor", type="primary"):
        s1_data = {'uloga': uloga1, 'tekst': s1_tekst}
        s2_data = {'uloga': uloga2, 'tekst': s2_tekst}

        doc = generiraj_prilagodeni_ugovor(
            naslov_ugovora, mjesto, datum, rok_vazenja,
            s1_data, s2_data, urbroj, st.session_state.custom_contract,
        )
        prikazi_dokument(doc, "Ugovor.docx", "Preuzmi dokument")


def _render_gradjansko_pravo():
    """Gradjansko pravo - predlosci ugovora."""
    st.subheader("Građansko pravo")
    tip = doc_selectbox(
        "Odaberite vrstu ugovora",
        ["Kupoprodaja", "Najam/Zakup", "Ugovor o djelu (Usluga)", "Zajam"],
        key="ug_gp_tip",
    )

    if tip == "Kupoprodaja":
        napuni_primjerom('ugovor_kupoprodaja', '')

    c1, c2 = st.columns(2)
    s1, _, _ = unos_stranke("PRVA STRANA", "u1")
    s2, _, _ = unos_stranke("DRUGA STRANA", "u2")
    opcije = {
        'kapara': st.checkbox("Kapara?"),
        'solemnizacija': st.checkbox("Solemnizacija?"),
    }
    if opcije['kapara']:
        opcije['iznos_kapare'] = st.number_input("Iznos kapare")

    data = {'mjesto': "Zagreb"}
    if tip == "Kupoprodaja":
        data['predmet_clanak'] = st.text_area(
            "Predmet ugovora", placeholder="Opišite predmet (npr. Vozilo marke BMW, šasija...)"
        )
        data['cijena_clanak'] = f"Cijena: {st.number_input('Cijena')} EUR."
        data['rok_clanak'] = "Odmah po isplati cijene."
    elif tip == "Najam/Zakup":
        data['predmet_clanak'] = st.text_input("Prostor (Adresa i opis)")
        data['cijena_clanak'] = f"Mjesečna najamnina/zakupnina: {st.number_input('Mjesečni iznos')} EUR."
        data['rok_clanak'] = "Trajanje ugovora: 1 godina (ili upišite drugo)."
    elif tip == "Ugovor o djelu (Usluga)":
        data['predmet_clanak'] = st.text_area("Opis posla/usluge")
        data['cijena_clanak'] = f"Honorar (neto/bruto): {st.number_input('Iznos honorara')} EUR."
        data['rok_clanak'] = "Rok izvršenja posla: 30 dana."
    elif tip == "Zajam":
        data['predmet_clanak'] = "Predmet ugovora je novčani zajam."
        data['cijena_clanak'] = f"Glavnica zajma: {st.number_input('Iznos zajma')} EUR."
        data['rok_clanak'] = f"Rok povrata: {st.date_input('Datum povrata').strftime('%d.%m.%Y.')}"

    st.markdown("---")
    add_trosak = st.checkbox("Dodaj troškovnik sastava ugovora (za odvjetnike)")
    troskovi = None
    if add_trosak:
        col_t1, col_t2 = st.columns(2)
        sastav = col_t1.number_input("Cijena sastava", 0.0)
        pdv_ug = col_t1.checkbox("PDV?", value=True)
        pdv_iznos = sastav * 0.25 if pdv_ug else 0
        troskovi = {'stavka': sastav, 'pdv': pdv_iznos}

    if st.button("Generiraj ugovor", type="primary", key="btn_gp"):
        doc = generiraj_ugovor_standard(tip, s1, s2, data, opcije, troskovi)
        prikazi_dokument(doc, f"{tip}.docx", "Preuzmi dokument")


def _render_radno_pravo():
    """Radno pravo - ugovor o radu, otkaz, aneks, upozorenje."""
    st.subheader("Radno pravo")
    tip = doc_selectbox(
        "Odaberite dokument",
        ["Ugovor o radu", "Rad na daljinu", "Odluka o otkazu", "Aneks ugovora o radu",
         "Upozorenje radniku", "Sporazumni prestanak", "Zabrana natjecanja", "Potvrda o zaposlenju"],
        key="ug_rp_tip",
    )

    if tip == "Ugovor o radu":
        _render_ugovor_o_radu()
    elif tip == "Rad na daljinu":
        _render_rad_na_daljinu()
    elif tip == "Odluka o otkazu":
        _render_otkaz()
    elif tip == "Aneks ugovora o radu":
        _render_aneks()
    elif tip == "Upozorenje radniku":
        _render_upozorenje()
    elif tip == "Sporazumni prestanak":
        _render_sporazumni_prestanak()
    elif tip == "Zabrana natjecanja":
        _render_zabrana_natjecanja()
    elif tip == "Potvrda o zaposlenju":
        _render_potvrda_o_zaposlenju()


def _render_ugovor_o_radu():
    c1, c2 = st.columns(2)
    p, _, _ = unos_stranke("POSLODAVAC", "p")
    r, _, _ = unos_stranke("RADNIK", "r")

    col_d1, col_d2 = st.columns(2)
    datum_start = col_d1.date_input("Početak rada")
    mjesto_sklapanja = col_d2.text_input("Mjesto sklapanja", "Zagreb")

    podaci = {
        'vrsta': st.radio("Vrsta", ["Neodređeno", "Određeno"]),
        'datum_do': None,
        'razlog_odredeno': "",
        'probni_rad': False,
    }
    if podaci['vrsta'] == "Određeno":
        d_do = st.date_input("Do (Datum)")
        podaci['datum_do'] = d_do.strftime('%d.%m.%Y.')
        podaci['razlog_odredeno'] = st.text_input("Razlog za određeno (npr. zamjena)")

    c_prob, c_go = st.columns(2)
    podaci['probni_rad'] = c_prob.checkbox("Probni rad")
    if podaci['probni_rad']:
        podaci['probni_rad_mj'] = c_prob.number_input("Trajanje (mjeseci)", 1, 6, 3)
    podaci['godisnji_odmor'] = c_go.number_input("Godišnji odmor (dana)", value=24)
    podaci['naziv_radnog_mjesta'] = st.text_input("Radno mjesto")
    podaci['opis_posla'] = st.text_area("Opis poslova (kratko)")
    podaci['mjesto_rada'] = st.text_input("Mjesto rada", "sjedište Poslodavca")
    c_sat, c_pla = st.columns(2)
    podaci['radno_vrijeme'] = c_sat.number_input("Tjedno radno vrijeme (sati)", value=40)
    podaci['bruto_placa'] = c_pla.number_input("Bruto plaća (EUR)")
    podaci['datum_start'] = datum_start.strftime('%d.%m.%Y.')
    podaci['mjesto_sklapanja'] = mjesto_sklapanja

    if st.button("Generiraj ugovor o radu", type="primary"):
        doc = generiraj_ugovor_o_radu(p, r, podaci)
        prikazi_dokument(doc, "Ugovor_o_radu.docx", "Preuzmi dokument")


def _render_otkaz():
    vrsta = st.selectbox(
        "Vrsta otkaza",
        ["Poslovno uvjetovani", "Osobno uvjetovani", "Skrivljeno ponašanje", "Izvanredni otkaz"],
    )
    c1, c2 = st.columns(2)
    p, _, _ = unos_stranke("POSLODAVAC", "po")
    r, _, _ = unos_stranke("RADNIK", "ro")
    podaci = {
        'vrsta_otkaza': vrsta,
        'mjesto': "Zagreb",
        'tekst_obrazlozenja': st.text_area("Obrazloženje otkaza (obavezno detaljno)"),
        'otkazni_rok': st.text_input("Otkazni rok"),
    }
    if st.button("Generiraj otkaz", type="primary"):
        doc = generiraj_otkaz(p, r, podaci)
        prikazi_dokument(doc, "Otkaz.docx", "Preuzmi dokument")


def _render_aneks():
    """Aneks ugovora o radu - Zakon o radu čl. 12."""
    c1, c2 = st.columns(2)
    p, _, _ = unos_stranke("POSLODAVAC", "an_p")
    r, _, _ = unos_stranke("RADNIK", "an_r")

    mjesto = st.text_input("Mjesto", "Zagreb", key="an_mj")
    datum_osnovnog = st.date_input("Datum osnovnog ugovora o radu")
    datum_primjene = st.date_input("Datum stupanja na snagu aneksa")

    razlog = st.text_area("Razlog izmjene (opcionalno)", height=80,
                          placeholder="Npr. promjena organizacijske strukture...")

    st.subheader("Izmjene")
    if 'aneks_promjene' not in st.session_state:
        st.session_state.aneks_promjene = [""]

    for i, promjena in enumerate(st.session_state.aneks_promjene):
        st.session_state.aneks_promjene[i] = st.text_area(
            f"Izmjena {i+1}",
            value=promjena,
            key=f"aneks_pr_{i}",
            placeholder="Npr. Bruto plaća se mijenja na 2.500,00 EUR mjesečno.",
            height=80,
        )

    if st.button("Dodaj izmjenu"):
        st.session_state.aneks_promjene.append("")
        st.rerun()

    if st.button("Generiraj aneks", type="primary"):
        doc = generiraj_aneks_ugovora_o_radu(p, r, {
            'mjesto': mjesto,
            'datum_osnovnog_ugovora': datum_osnovnog.strftime('%d.%m.%Y.'),
            'datum_primjene': datum_primjene.strftime('%d.%m.%Y.'),
            'razlog': razlog,
            'promjene': [pr for pr in st.session_state.aneks_promjene if pr.strip()],
        })
        prikazi_dokument(doc, "Aneks_ugovor_o_radu.docx", "Preuzmi dokument")


def _render_upozorenje():
    """Upozorenje radniku - Zakon o radu čl. 119."""
    c1, c2 = st.columns(2)
    p, _, _ = unos_stranke("POSLODAVAC", "up_p")
    r, _, _ = unos_stranke("RADNIK", "up_r")

    mjesto = st.text_input("Mjesto", "Zagreb", key="up_mj")
    datum_povrede = st.date_input("Datum povrede obveze")

    opis_povrede = st.text_area(
        "Opis povrede obveze iz radnog odnosa",
        placeholder="Detaljno opišite što je radnik učinio/propustio...",
        height=150,
    )

    rok = st.number_input("Rok za očitovanje (dana)", min_value=1, value=8)

    if st.button("Generiraj upozorenje", type="primary"):
        doc = generiraj_upozorenje_radniku(p, r, {
            'mjesto': mjesto,
            'datum_povrede': datum_povrede.strftime('%d.%m.%Y.'),
            'opis_povrede': opis_povrede,
            'rok_ocitovanja': rok,
        })
        prikazi_dokument(doc, "Upozorenje_radniku.docx", "Preuzmi dokument")


def _render_rad_na_daljinu():
    """Ugovor o radu na daljinu / izdvojenom mjestu rada."""
    c1, c2 = st.columns(2)
    p, _, _ = unos_stranke("POSLODAVAC", "rd_p")
    r, _, _ = unos_stranke("RADNIK", "rd_r")

    vrsta_rada = st.radio("Vrsta rada", ["na_daljinu", "izdvojeno_mjesto"], key="rd_vrsta")
    col_d, col_m = st.columns(2)
    datum_start = col_d.date_input("Početak rada", key="rd_datum")
    mjesto_sklapanja = col_m.text_input("Mjesto sklapanja", "Zagreb", key="rd_mjesto")

    naziv_radnog_mjesta = st.text_input("Naziv radnog mjesta", key="rd_radno_mjesto")
    opis_posla = st.text_area("Opis poslova", key="rd_opis")
    oprema = st.text_input("Oprema", "prijenosno računalo, monitor, tipkovnica, miš", key="rd_oprema")

    col_n, col_rv = st.columns(2)
    naknada_troskova = col_n.number_input("Naknada troškova (EUR)", key="rd_naknada")
    radno_vrijeme = col_rv.number_input("Tjedno radno vrijeme (sati)", value=40, key="rd_sati")

    col_p, col_go = st.columns(2)
    bruto_placa = col_p.number_input("Bruto plaća (EUR)", key="rd_placa")
    godisnji_odmor = col_go.number_input("Godišnji odmor (dana)", value=24, key="rd_go")

    podaci = {
        'vrsta_rada': vrsta_rada,
        'datum_start': datum_start.strftime('%d.%m.%Y.'),
        'naziv_radnog_mjesta': naziv_radnog_mjesta,
        'opis_posla': opis_posla,
        'oprema': oprema,
        'naknada_troskova': naknada_troskova,
        'radno_vrijeme': radno_vrijeme,
        'bruto_placa': bruto_placa,
        'godisnji_odmor': godisnji_odmor,
        'mjesto_sklapanja': mjesto_sklapanja,
    }

    if st.button("Generiraj ugovor", type="primary", key="rd_btn"):
        doc = generiraj_ugovor_rad_na_daljinu(p, r, podaci)
        prikazi_dokument(doc, "Ugovor_rad_na_daljinu.docx", "Preuzmi dokument")


def _render_sporazumni_prestanak():
    """Sporazumni prestanak ugovora o radu."""
    c1, c2 = st.columns(2)
    p, _, _ = unos_stranke("POSLODAVAC", "sp_p")
    r, _, _ = unos_stranke("RADNIK", "sp_r")

    col_d1, col_d2 = st.columns(2)
    datum_osnovnog_ugovora = col_d1.date_input("Datum osnovnog ugovora o radu", key="sp_datum_ug")
    datum_prestanka = col_d2.date_input("Datum prestanka radnog odnosa", key="sp_datum_pr")

    col_go, col_otp = st.columns(2)
    godisnji_odmor_neiskoristen = col_go.number_input("Neiskorišteni GO (dana)", value=0, key="sp_go")
    naknada_go = st.checkbox("Isplatiti naknadu za GO?", key="sp_naknada_go")
    otpremnina = col_otp.number_input("Otpremnina (EUR)", value=0.0, key="sp_otpremnina")

    povrat_imovine = st.text_input("Povrat imovine poslodavca", key="sp_povrat")
    mjesto = st.text_input("Mjesto", "Zagreb", key="sp_mjesto")

    podaci = {
        'datum_osnovnog_ugovora': datum_osnovnog_ugovora.strftime('%d.%m.%Y.'),
        'datum_prestanka': datum_prestanka.strftime('%d.%m.%Y.'),
        'godisnji_odmor_neiskoristen': godisnji_odmor_neiskoristen,
        'naknada_go': naknada_go,
        'otpremnina': otpremnina,
        'povrat_imovine': povrat_imovine,
        'mjesto': mjesto,
    }

    if st.button("Generiraj sporazumni prestanak", type="primary", key="sp_btn"):
        doc = generiraj_sporazumni_prestanak(p, r, podaci)
        prikazi_dokument(doc, "Sporazumni_prestanak.docx", "Preuzmi dokument")


def _render_zabrana_natjecanja():
    """Ugovorna zabrana natjecanja - Zakon o radu čl. 101-106."""
    c1, c2 = st.columns(2)
    p, _, _ = unos_stranke("POSLODAVAC", "zn_p")
    r, _, _ = unos_stranke("RADNIK", "zn_r")

    opis_zabrane = st.text_area("Materijalni opseg zabrane", key="zn_opis",
                                 placeholder="Opišite djelatnosti koje se zabranjuju...")
    teritorij = st.text_input("Teritorijalni opseg", "Republika Hrvatska", key="zn_teritorij")

    col_t, col_mn = st.columns(2)
    trajanje_mjeseci = col_t.number_input("Trajanje zabrane (mjeseci)", min_value=1, max_value=24, value=12, key="zn_trajanje")
    mjesecna_naknada = col_mn.number_input("Mjesečna naknada (EUR)", key="zn_naknada")

    ugovorna_kazna = st.number_input("Ugovorna kazna (EUR)", key="zn_kazna")
    mjesto = st.text_input("Mjesto", "Zagreb", key="zn_mjesto")

    podaci = {
        'opis_zabrane': opis_zabrane,
        'teritorij': teritorij,
        'trajanje_mjeseci': trajanje_mjeseci,
        'mjesecna_naknada': mjesecna_naknada,
        'ugovorna_kazna': ugovorna_kazna,
        'mjesto': mjesto,
    }

    if st.button("Generiraj zabranu natjecanja", type="primary", key="zn_btn"):
        doc = generiraj_zabranu_natjecanja(p, r, podaci)
        prikazi_dokument(doc, "Zabrana_natjecanja.docx", "Preuzmi dokument")


def _render_potvrda_o_zaposlenju():
    """Potvrda o zaposlenju."""
    c1, c2 = st.columns(2)
    p, _, _ = unos_stranke("POSLODAVAC", "pz_p")
    r, _, _ = unos_stranke("RADNIK", "pz_r")

    col_d1, col_d2 = st.columns(2)
    datum_od = col_d1.date_input("Zaposlen od", key="pz_od")
    datum_do = col_d2.date_input("Zaposlen do", key="pz_do")

    opis_poslova = st.text_input("Opis poslova", key="pz_opis")
    mjesto = st.text_input("Mjesto", "Zagreb", key="pz_mjesto")

    podaci = {
        'datum_od': datum_od.strftime('%d.%m.%Y.'),
        'datum_do': datum_do.strftime('%d.%m.%Y.'),
        'opis_poslova': opis_poslova,
        'mjesto': mjesto,
    }

    if st.button("Generiraj potvrdu", type="primary", key="pz_btn"):
        doc = generiraj_potvrdu_o_zaposlenju(p, r, podaci)
        prikazi_dokument(doc, "Potvrda_o_zaposlenju.docx", "Preuzmi dokument")


def render_ugovori():
    """Glavna render funkcija za modul Ugovori i Odluke."""
    st.header("Ugovori i odluke")

    zaglavlje_sastavljaca()

    if "ug_kategorija" not in st.session_state:
        st.session_state.ug_kategorija = "Slobodna forma"

    st.markdown('<div class="doc-selector-label">KATEGORIJA</div>', unsafe_allow_html=True)
    for kat in ["Slobodna forma", "Građansko pravo", "Radno pravo"]:
        if st.button(
            kat,
            key=f"ug_kat_{kat}",
            type="primary" if st.session_state.ug_kategorija == kat else "secondary",
        ):
            st.session_state.ug_kategorija = kat
            st.rerun()

    st.markdown("---")
    kategorija = st.session_state.ug_kategorija
    if kategorija == "Slobodna forma":
        _render_slobodna_forma()
    elif kategorija == "Građansko pravo":
        _render_gradjansko_pravo()
    elif kategorija == "Radno pravo":
        _render_radno_pravo()
