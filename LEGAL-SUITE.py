# =============================================================================
# LegalTech Suite Pro - Glavni ulaz (entry point)
# =============================================================================
import streamlit as st
from config import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT, CSS_STILOVI
from pomocne import docx_opcije
from stranice import (
    render_ugovori,
    render_tuzbe,
    render_ovrhe,
    render_zalbe,
    render_zemljisne,
    render_kamate,
    render_opomene,
    render_punomoci,
    render_trgovacko,
    render_obvezno,
    render_obiteljsko,
    render_upravno,
    render_kazneno,
    render_stecajno,
    render_potrosaci,
    render_pristojbe,
)

# Konfiguracija stranice
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=PAGE_LAYOUT)

# Primjena CSS stilova
st.markdown(CSS_STILOVI, unsafe_allow_html=True)

# =============================================================================
# SIDEBAR NAVIGACIJA - Gumbi umjesto radio (rjesava problem ponovnog klika)
# =============================================================================

# Definicija navigacijskih modula po sekcijama
_NAV_SECTIONS = {
    "Ugovori i dokumenti": [
        "Početna",
        "Ugovori i odluke",
        "Opomena pred tužbu",
        "Punomoć",
        "Obvezno pravo",
        "Trgovačko pravo",
        "Obiteljsko pravo",
    ],
    "Sudski postupci": [
        "Tužbe",
        "Ovršno pravo",
        "Žalbe",
        "Zemljišne knjige",
        "Upravno pravo",
        "Kazneno pravo",
        "Stečajno pravo",
    ],
    "Alati i ostalo": [
        "Vodič",
        "Kalkulator kamata",
        "Kalkulator pristojbi",
        "Zaštita potrošača",
    ],
}

# Inicijaliziraj aktivni modul
if "_active_module" not in st.session_state:
    st.session_state._active_module = "Početna"

st.sidebar.title("LegalTech Suite Pro")
st.sidebar.caption("Generator pravnih dokumenata")
st.sidebar.markdown("---")

for section_name, modules in _NAV_SECTIONS.items():
    st.sidebar.markdown(f"<p class='sidebar-section'>{section_name.upper()}</p>", unsafe_allow_html=True)
    for module_name in modules:
        is_active = st.session_state._active_module == module_name
        btn_type = "primary" if is_active else "secondary"
        if st.sidebar.button(
            f"{'▸ ' if is_active else '  '}{module_name}",
            key=f"_sb_{module_name}",
            type=btn_type,
            use_container_width=True,
        ):
            st.session_state._active_module = module_name
            st.rerun()

# Footer u sidebaru
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='text-align: center; font-size: 0.7rem; color: #94A3B8 !important; "
    "font-family: Inter, sans-serif; padding: 0.5rem 0;'>"
    "v3.0 &middot; 60+ dokumenata &middot; 15 područja<br>"
    "LegalTech Suite Pro &copy; 2025"
    "</div>",
    unsafe_allow_html=True,
)


# =============================================================================
# POCETNA STRANICA
# =============================================================================

def _navigate_to(module_name):
    """Navigira na zadani modul."""
    st.session_state._active_module = module_name


def _render_pocetna():
    """Informativna pocetna stranica."""

    # Hero sekcija
    st.markdown(
        "<div class='hero-section'>"
        "<h2>LegalTech Suite Pro</h2>"
        "<p>Profesionalni generator pravnih dokumenata u DOCX formatu. "
        "60+ dokumenata iz 15 pravnih područja, baza 74 hrvatska suda, "
        "kalkulator kamata i pristojbi.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Metrike
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Dokumenata", "60+")
    col2.metric("Pravnih područja", "15")
    col3.metric("Format", "DOCX")
    col4.metric("Sudova u bazi", "74")

    st.markdown("")

    # Definicija modula za kartice
    _ugovori_moduli = [
        ("Ugovori i odluke", "10 tipova — radno pravo, otkaz, aneks, NDA, potvrda..."),
        ("Obvezno pravo", "8 tipova — darovanje, cesija, kompenzacija, jamstvo..."),
        ("Trgovačko pravo", "5 tipova — društveni ugovor, prijenos udjela, NDA..."),
        ("Obiteljsko pravo", "5 tipova — razvod, bračni ugovor, skrb, uzdržavanje..."),
        ("Opomena pred tužbu", "Opomena pred tužbu ili ovrhu s rokom za plaćanje"),
        ("Punomoć", "Opća i posebna punomoć za zastupanje"),
    ]
    _sudski_moduli = [
        ("Tužbe", "Parnični postupak, brisovna tužba, auto-pristojba"),
        ("Ovršno pravo", "7 tipova — ovrha JB, prigovor, nekretnina, plaća..."),
        ("Žalbe", "Žalba na presudu s obrazloženjem i troškovnikom"),
        ("Zemljišne knjige", "7 tipova — uknjižba, hipoteka, služnost, brisanje..."),
        ("Upravno pravo", "Žalba ZUP, tužba ZUS, pristup informacijama..."),
        ("Kazneno pravo", "Kaznena prijava, privatna tužba, žalba na presudu"),
        ("Stečajno pravo", "Prijedlog za stečaj, prijava tražbine, osobni stečaj"),
    ]

    # Dva stupca s gumbima
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Ugovori i dokumenti")
        for naziv, opis in _ugovori_moduli:
            with st.container(border=True):
                st.markdown(f"**{naziv}**")
                st.caption(opis)
                if st.button("Otvori →", key=f"_nav_{naziv}", type="primary", use_container_width=True):
                    _navigate_to(naziv)
                    st.rerun()

    with col2:
        st.markdown("##### Sudski postupci")
        for naziv, opis in _sudski_moduli:
            with st.container(border=True):
                st.markdown(f"**{naziv}**")
                st.caption(opis)
                if st.button("Otvori →", key=f"_nav_{naziv}", type="primary", use_container_width=True):
                    _navigate_to(naziv)
                    st.rerun()

    st.markdown("")

    # Alati
    st.markdown("##### Alati")
    col1, col2, col3 = st.columns(3)
    _alati = [
        ("Kalkulator kamata", "Zakonske zatezne kamate prema HNB stopama. DOCX export."),
        ("Kalkulator pristojbi", "Sudske pristojbe prema VPS-u, žalbe, ovrhe, ZK."),
        ("Zaštita potrošača", "Reklamacija, jednostrani raskid, prijava inspekciji."),
    ]
    for col, (naziv, opis) in zip([col1, col2, col3], _alati):
        with col:
            with st.container(border=True):
                st.markdown(f"**{naziv}**")
                st.caption(opis)
                if st.button("Otvori →", key=f"_nav_{naziv}", type="primary", use_container_width=True):
                    _navigate_to(naziv)
                    st.rerun()

    st.caption(
        "Svi dokumenti generiraju se u DOCX formatu (Microsoft Word) "
        "s hrvatskim pravnim formatiranjem — Times New Roman 12pt, margine 2.5cm."
    )


# =============================================================================
# VODIČ - "Koji dokument mi treba?"
# =============================================================================

def _render_vodic():
    """Interaktivni vodic koji pomaze korisnicima odabrati pravi dokument."""
    st.header("Koji dokument mi treba?")
    st.markdown("Odgovorite na pitanja i sustav će preporučiti pravne korake i dokumente.")

    st.markdown("")

    problem = st.selectbox(
        "Kakav problem imate?",
        [
            "— Odaberite —",
            "Netko mi duguje novac",
            "Dobio/la sam presudu s kojom se ne slažem",
            "Imam problem s upravnim tijelom (rješenje, dozvola...)",
            "Želim sklopiti ili raskinuti ugovor",
            "Žrtva sam kaznenog djela",
            "Imam problem s nekretninom (zemljišne knjige)",
            "Imam problem kao potrošač",
            "Tvrtka / poslovni spor",
            "Obiteljski spor (razvod, djeca, uzdržavanje)",
            "Dužnik sam u financijskim poteškoćama",
        ],
        key="_vodic_problem",
    )

    if problem == "— Odaberite —":
        st.info("Odaberite vrstu problema iz padajućeg izbornika iznad.")
        return

    st.markdown("---")

    if problem == "Netko mi duguje novac":
        st.markdown("### Koraci za naplatu dugovanja")
        st.markdown("""
**1. korak: Opomena pred tužbu** *(preporučeno prvi)*
- Pošaljite dužniku pisanu opomenu s rokom od 8 dana
- Ovo je obavezni preduvjet za ovrhu na temelju vjerodostojne isprave
- Sačuvajte dokaz slanja (povratnica, email)
        """)
        if st.button("Izradi opomenu →", key="_v_opomena", type="primary"):
            _navigate_to("Opomena pred tužbu")
            st.rerun()

        st.markdown("""
**2. korak: Ovrha ili Tužba** *(ako dužnik ne plati)*
- **Ovrha (brži put)** — ako imate račun, ugovor ili drugu vjerodostojnu ispravu → prijedlog javnom bilježniku
- **Tužba (sporni put)** — ako dužnik osporava dug → parnični postupak pred sudom
        """)
        c1, c2 = st.columns(2)
        if c1.button("Izradi prijedlog za ovrhu →", key="_v_ovrha", type="primary", use_container_width=True):
            _navigate_to("Ovršno pravo")
            st.rerun()
        if c2.button("Izradi tužbu →", key="_v_tuzba", type="primary", use_container_width=True):
            _navigate_to("Tužbe")
            st.rerun()

        st.markdown("""
**3. korak: Žalba / prigovor** *(ako ovrha bude osporena)*
- Dužnik može podnijeti prigovor na rješenje o ovrsi
- Vi odgovarate podneskom ili podnosite tužbu

**Kalkulator kamata** — izračunajte zakonske zatezne kamate na dugovanje
        """)
        if st.button("Kalkulator kamata →", key="_v_kamate"):
            _navigate_to("Kalkulator kamata")
            st.rerun()

        with st.expander("Važni rokovi"):
            st.markdown("""
- **Opći zastarni rok:** 5 godina (čl. 225. ZOO)
- **Ugovori o prometu robe/usluga:** 3 godine (čl. 226. ZOO)
- **Naknada štete:** 3 godine od saznanja / 5 godina objektivno (čl. 230. ZOO)
- **Radnopravna potraživanja:** 5 godina (čl. 135. ZR)
            """)

    elif problem == "Dobio/la sam presudu s kojom se ne slažem":
        st.markdown("### Žalba na presudu")
        st.warning("**Rok za žalbu je 15 dana** od dana dostave presude (čl. 348. ZPP). Hitno!")
        st.markdown("""
- Žalba se podnosi prvostupanjskom sudu, a o njoj odlučuje drugostupanjski
- Žalbeni razlozi: bitna povreda postupka, pogrešno činjenično stanje, pogrešna primjena prava
- Potrebno: poslovni broj presude, datum dostave, obrazloženje
        """)
        if st.button("Izradi žalbu →", key="_v_zalba", type="primary"):
            _navigate_to("Žalbe")
            st.rerun()

    elif problem == "Imam problem s upravnim tijelom (rješenje, dozvola...)":
        st.markdown("### Upravno pravo — žalba i tužba")
        st.markdown("""
**Žalba na rješenje (ZUP)** — rok **15 dana** od dostave
- Podnosi se drugostupanjskom tijelu putem prvostupanjskog

**Tužba upravnom sudu (ZUS)** — rok **30 dana** od dostave drugostupanjskog rješenja
- Kada je iscrpljena žalba ili žalba nije dopuštena

**Zahtjev za pristup informacijama (ZPPI)**
- Tijelo mora odgovoriti u **15 dana**
        """)
        if st.button("Upravno pravo →", key="_v_upravno", type="primary"):
            _navigate_to("Upravno pravo")
            st.rerun()

    elif problem == "Želim sklopiti ili raskinuti ugovor":
        st.markdown("### Ugovori")
        st.markdown("""
**Sklapanje ugovora** — 10 tipova ugovora (kupoprodaja, rad, najam, NDA...)
**Raskid ugovora** — sporazumni raskid, otkaz, aneks
**Obvezno pravo** — darovanje, cesija, kompenzacija, jamstvo, licencija...
        """)
        c1, c2 = st.columns(2)
        if c1.button("Ugovori →", key="_v_ugovori", type="primary", use_container_width=True):
            _navigate_to("Ugovori i odluke")
            st.rerun()
        if c2.button("Obvezno pravo →", key="_v_obvezno", type="primary", use_container_width=True):
            _navigate_to("Obvezno pravo")
            st.rerun()

    elif problem == "Žrtva sam kaznenog djela":
        st.markdown("### Kazneno pravo")
        st.markdown("""
**Kaznena prijava** — podnosi se Državnom odvjetništvu
- Za teža kaznena djela (krađa, prijevara, tjelesna ozljeda...)
- Nema roka za podnošenje, ali što prije to bolje

**Privatna tužba** — za kaznena djela koja se gone po privatnoj tužbi
- Rok: **3 mjeseca** od saznanja za djelo i počinitelja (čl. 60. KZ)
- Npr. laka tjelesna ozljeda, kleveta, uvreda
        """)
        if st.button("Kazneno pravo →", key="_v_kazneno", type="primary"):
            _navigate_to("Kazneno pravo")
            st.rerun()

    elif problem == "Imam problem s nekretninom (zemljišne knjige)":
        st.markdown("### Zemljišne knjige")
        st.markdown("""
**Uknjižba prava vlasništva** — tabularna isprava za upis u ZK
**Hipoteka** — upis/brisanje hipoteke
**Služnost** — osnivanje prava služnosti
**Zabilježba** — spora, ovrhe, prvokupa...
**Brisovna tužba** — pobijanje nevaljanog ZK upisa
        """)
        if st.button("Zemljišne knjige →", key="_v_zk", type="primary"):
            _navigate_to("Zemljišne knjige")
            st.rerun()

    elif problem == "Imam problem kao potrošač":
        st.markdown("### Zaštita potrošača")
        st.markdown("""
**Reklamacija** — pisani prigovor trgovcu (rok za odgovor: **15 dana**)
**Jednostrani raskid** — za online kupnju imate **14 dana** bez razloga
**Prijava inspekciji** — ako trgovac ne poštuje prava potrošača
        """)
        if st.button("Zaštita potrošača →", key="_v_potrosaci", type="primary"):
            _navigate_to("Zaštita potrošača")
            st.rerun()

    elif problem == "Tvrtka / poslovni spor":
        st.markdown("### Trgovačko pravo")
        st.markdown("""
**Društveni ugovor** — za osnivanje d.o.o.
**Prijenos udjela** — prodaja/darovanje poslovnog udjela
**Odluka skupštine** — formalne odluke članova društva
**NDA** — ugovor o povjerljivosti
**Zapisnik skupštine** — formalni zapisnik sjednice
        """)
        if st.button("Trgovačko pravo →", key="_v_trgovacko", type="primary"):
            _navigate_to("Trgovačko pravo")
            st.rerun()

    elif problem == "Obiteljski spor (razvod, djeca, uzdržavanje)":
        st.markdown("### Obiteljsko pravo")
        st.markdown("""
**Sporazumni razvod** — kad se oba supružnika slažu
**Tužba za razvod** — kad nema sporazuma
**Bračni ugovor** — reguliranje imovine
**Roditeljska skrb** — sporazum o djeci
**Uzdržavanje** — ugovor o uzdržavanju
        """)
        if st.button("Obiteljsko pravo →", key="_v_obiteljsko", type="primary"):
            _navigate_to("Obiteljsko pravo")
            st.rerun()

    elif problem == "Dužnik sam u financijskim poteškoćama":
        st.markdown("### Stečajno pravo")
        st.markdown("""
**Stečaj potrošača (osobni stečaj)** — za fizičke osobe
- Uvjeti: dug ≥ 3.981,68 EUR, blokada ≥ 90 dana
- Plan otplate do 5 godina

**Prijedlog za stečaj** — za tvrtke u blokadi > 60 dana
**Prijava tražbine** — ako ste vjerovnik u stečaju
        """)
        if st.button("Stečajno pravo →", key="_v_stecajno", type="primary"):
            _navigate_to("Stečajno pravo")
            st.rerun()


# =============================================================================
# ROUTING
# =============================================================================

active = st.session_state._active_module

# DOCX opcije - prikazuju se na svim stranicama osim pocetne, vodica i kalkulatora
_NO_DOCX_OPTS = {"Početna", "Vodič", "Kalkulator kamata", "Kalkulator pristojbi"}
if active not in _NO_DOCX_OPTS:
    docx_opcije()

# Routing
if active == "Početna":
    _render_pocetna()
elif active == "Vodič":
    _render_vodic()
elif active == "Ugovori i odluke":
    render_ugovori()
elif active == "Opomena pred tužbu":
    render_opomene()
elif active == "Punomoć":
    render_punomoci()
elif active == "Obvezno pravo":
    render_obvezno()
elif active == "Trgovačko pravo":
    render_trgovacko()
elif active == "Obiteljsko pravo":
    render_obiteljsko()
elif active == "Tužbe":
    render_tuzbe()
elif active == "Ovršno pravo":
    render_ovrhe()
elif active == "Žalbe":
    render_zalbe()
elif active == "Zemljišne knjige":
    render_zemljisne()
elif active == "Upravno pravo":
    render_upravno()
elif active == "Kazneno pravo":
    render_kazneno()
elif active == "Stečajno pravo":
    render_stecajno()
elif active == "Kalkulator kamata":
    render_kamate()
elif active == "Kalkulator pristojbi":
    render_pristojbe()
elif active == "Zaštita potrošača":
    render_potrosaci()
