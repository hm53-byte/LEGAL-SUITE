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
# SIDEBAR NAVIGACIJA - Grupirano po pravnim podrucjima
# =============================================================================
st.sidebar.title("LegalTech Suite Pro")
st.sidebar.caption("Generator pravnih dokumenata")
st.sidebar.markdown("---")

# Sekcija: Ugovori i dokumenti
st.sidebar.markdown("<p class='sidebar-section'>Ugovori i dokumenti</p>", unsafe_allow_html=True)
modul = st.sidebar.radio(
    "Navigacija",
    [
        "Početna",
        "Ugovori i odluke",
        "Opomena pred tužbu",
        "Punomoć",
        "Obvezno pravo",
        "Trgovačko pravo",
        "Obiteljsko pravo",
    ],
    label_visibility="collapsed",
    key="nav_ugovori",
)

# Sekcija: Sudski postupci
st.sidebar.markdown("<p class='sidebar-section'>Sudski postupci</p>", unsafe_allow_html=True)
modul2 = st.sidebar.radio(
    "Navigacija 2",
    [
        "Tužbe",
        "Ovršno pravo",
        "Žalbe",
        "Zemljišne knjige",
        "Upravno pravo",
        "Kazneno pravo",
        "Stečajno pravo",
    ],
    label_visibility="collapsed",
    key="nav_sudski",
)

# Sekcija: Alati
st.sidebar.markdown("<p class='sidebar-section'>Alati i ostalo</p>", unsafe_allow_html=True)
modul3 = st.sidebar.radio(
    "Navigacija 3",
    [
        "Kalkulator kamata",
        "Kalkulator pristojbi",
        "Zaštita potrošača",
    ],
    label_visibility="collapsed",
    key="nav_alati",
)

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
# ROUTING - Samo jedan radio moze biti aktivan
# Koristimo session_state za pracenje aktivnog modula
# =============================================================================

# Odredimo koji je radio zadnji kliknut
def _get_active_module():
    """Vraca aktivni modul na temelju session_state radio widgeta."""
    # Ako je korisnik kliknuo gumb na pocetnoj stranici
    if "_force_module" in st.session_state:
        forced = st.session_state._force_module
        del st.session_state._force_module
        return forced

    # Streamlit radio ne podrzava medusobno iskljucivanje grupa
    # pa koristimo tracker za zadnju promjenu
    current = {
        "nav_ugovori": st.session_state.get("nav_ugovori", "Ugovori i odluke"),
        "nav_sudski": st.session_state.get("nav_sudski", "Tužbe"),
        "nav_alati": st.session_state.get("nav_alati", "Kalkulator kamata"),
    }

    # Zapamti prethodno stanje
    if "_prev_nav" not in st.session_state:
        st.session_state._prev_nav = current.copy()
        return "Početna"

    prev = st.session_state._prev_nav

    # Pronadji koji se promijenio
    for key in ["nav_ugovori", "nav_sudski", "nav_alati"]:
        if current[key] != prev.get(key):
            st.session_state._prev_nav = current.copy()
            st.session_state._active_group = key
            return current[key]

    # Ako se nista nije promijenilo, vrati zadnji aktivni
    active_group = st.session_state.get("_active_group", "nav_ugovori")
    return current[active_group]


def _navigate_to(module_name):
    """Navigira na zadani modul postavljanjem session_state."""
    st.session_state._force_module = module_name


def _render_pocetna():
    """Informativna pocetna stranica - Trust-Centric dizajn."""

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
                if st.button("Otvori", key=f"_nav_{naziv}", type="primary"):
                    _navigate_to(naziv)
                    st.rerun()

    st.caption(
        "Svi dokumenti generiraju se u DOCX formatu (Microsoft Word) "
        "s hrvatskim pravnim formatiranjem — Times New Roman 12pt, margine 2.5cm."
    )


active = _get_active_module()

# DOCX opcije - prikazuju se na svim stranicama osim pocetne i kalkulatora
_NO_DOCX_OPTS = {"Početna", "Kalkulator kamata", "Kalkulator pristojbi"}
if active not in _NO_DOCX_OPTS:
    docx_opcije()

# Routing
if active == "Početna":
    _render_pocetna()
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
