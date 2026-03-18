# =============================================================================
# LegalTech Suite Pro - Glavni ulaz (entry point)
# v4.1 - UI overhaul, search, fix bugs, cleaner nav
# =============================================================================
import streamlit as st
import streamlit.components.v1 as components
from config import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT, CSS_STILOVI
from pomocne import docx_opcije
from auth import login_stranica, prikazi_korisnika_sidebar, provjeri_auth
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
    render_epredmet,
    render_eoglasna,
    render_kalendar,
    render_nn_pretraga,
)

# Konfiguracija stranice
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=PAGE_LAYOUT)

# Primjena CSS stilova + Google Fonts
st.markdown(
    "<link href='https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap' rel='stylesheet'>",
    unsafe_allow_html=True,
)
st.markdown(CSS_STILOVI, unsafe_allow_html=True)

# =============================================================================
# AUTENTIKACIJA
# =============================================================================

if not login_stranica():
    st.stop()

# =============================================================================
# NAVIGACIJSKA STRUKTURA
# =============================================================================

_MODULI = {
    "Pocetna":           {"render": None,             "grupa": None,    "docx": False, "opis": "Pocetna stranica"},
    "Ugovori":           {"render": render_ugovori,   "grupa": "Dokumenti", "docx": True,  "opis": "Kupoprodaja, najam, rad, NDA, raskid..."},
    "Opomena":           {"render": render_opomene,    "grupa": "Dokumenti", "docx": True,  "opis": "Opomena pred tuzbu"},
    "Punomoc":           {"render": render_punomoci,   "grupa": "Dokumenti", "docx": True,  "opis": "Punomoc za zastupanje"},
    "Obvezno pravo":     {"render": render_obvezno,    "grupa": "Dokumenti", "docx": True,  "opis": "Darovanje, cesija, kompenzacija, jamstvo..."},
    "Trgovacko pravo":   {"render": render_trgovacko,  "grupa": "Dokumenti", "docx": True,  "opis": "Drustveni ugovor, prijenos udjela, NDA..."},
    "Obiteljsko pravo":  {"render": render_obiteljsko, "grupa": "Dokumenti", "docx": True,  "opis": "Razvod, bracni ugovor, skrb, uzdrzavanje"},
    "Tuzbe":             {"render": render_tuzbe,      "grupa": "Sudski postupci", "docx": True,  "opis": "Tuzba za isplatu, naknada stete"},
    "Ovrsno pravo":      {"render": render_ovrhe,      "grupa": "Sudski postupci", "docx": True,  "opis": "Ovrha putem JB, prigovor, obustava"},
    "Zalbe":             {"render": render_zalbe,       "grupa": "Sudski postupci", "docx": True,  "opis": "Zalba na presudu"},
    "Zemljisne knjige":  {"render": render_zemljisne,   "grupa": "Sudski postupci", "docx": True,  "opis": "Uknjizba, hipoteka, sluznost..."},
    "Upravno pravo":     {"render": render_upravno,     "grupa": "Sudski postupci", "docx": True,  "opis": "Zalba ZUP, tuzba ZUS, pristup info"},
    "Kazneno pravo":     {"render": render_kazneno,     "grupa": "Sudski postupci", "docx": True,  "opis": "Kaznena prijava, privatna tuzba, zalba"},
    "Stecajno pravo":    {"render": render_stecajno,    "grupa": "Sudski postupci", "docx": True,  "opis": "Osobni stecaj, prijedlog, prijava trazbine"},
    "Zastita potrosaca": {"render": render_potrosaci,   "grupa": "Sudski postupci", "docx": True,  "opis": "Reklamacija, raskid online kupnje"},
    "e-Predmet":         {"render": render_epredmet,    "grupa": "Alati",  "docx": False, "opis": "Pracenje sudskih predmeta"},
    "Sudske objave":     {"render": render_eoglasna,    "grupa": "Alati",  "docx": False, "opis": "e-Oglasna ploca sudova"},
    "Propisi":           {"render": render_nn_pretraga, "grupa": "Alati",  "docx": False, "opis": "Narodne novine, baza zakona"},
    "Kalendar":          {"render": render_kalendar,    "grupa": "Alati",  "docx": False, "opis": "Rocista, rokovi, podsjetnici"},
    "Kamate":            {"render": render_kamate,      "grupa": "Alati",  "docx": False, "opis": "Kalkulator zakonskih zateznih kamata"},
    "Pristojbe":         {"render": render_pristojbe,   "grupa": "Alati",  "docx": False, "opis": "Kalkulator sudskih pristojbi"},
}

# Grupe za sidebar
_GRUPE = ["Dokumenti", "Sudski postupci", "Alati"]

if "_active_module" not in st.session_state:
    st.session_state._active_module = "Pocetna"

# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.markdown(
    "<div style='text-align:center;padding:0.3rem 0 0.5rem;'>"
    "<span style='color:#D4A843;font-size:1.1rem;font-weight:700;"
    "font-family:Inter,sans-serif;letter-spacing:0.3px;'>"
    "LegalTech Suite</span>"
    "</div>",
    unsafe_allow_html=True,
)
prikazi_korisnika_sidebar()

# Pretraga u sidebaru
_search_query = st.sidebar.text_input(
    "Pretrazi module",
    placeholder="npr. ugovor, ovrha, zalba...",
    key="_sidebar_search",
    label_visibility="collapsed",
)

# Filtrirani moduli
if _search_query:
    _q = _search_query.lower()
    _filtered = {
        k: v for k, v in _MODULI.items()
        if k != "Pocetna" and (_q in k.lower() or _q in v["opis"].lower())
    }
    if _filtered:
        for name in _filtered:
            is_active = st.session_state._active_module == name
            if st.sidebar.button(
                f"{'> ' if is_active else ''}{name}",
                key=f"_sb_{name}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
            ):
                st.session_state._active_module = name
                st.rerun()
    else:
        st.sidebar.caption("Nema rezultata.")
else:
    # Pocetna gumb
    is_home = st.session_state._active_module == "Pocetna"
    if st.sidebar.button(
        f"{'> ' if is_home else ''}Pocetna",
        key="_sb_Pocetna",
        type="primary" if is_home else "secondary",
        use_container_width=True,
    ):
        st.session_state._active_module = "Pocetna"
        st.rerun()

    st.sidebar.markdown("")

    for grupa in _GRUPE:
        st.sidebar.markdown(
            f"<p class='sidebar-section'>{grupa.upper()}</p>",
            unsafe_allow_html=True,
        )
        for name, cfg in _MODULI.items():
            if cfg["grupa"] != grupa:
                continue
            is_active = st.session_state._active_module == name
            if st.sidebar.button(
                f"{'> ' if is_active else ''}{name}",
                key=f"_sb_{name}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
            ):
                st.session_state._active_module = name
                st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='text-align:center;font-size:0.65rem;color:#64748B !important;"
    "font-family:Inter,sans-serif;padding:0.3rem 0;'>"
    "v4.1 &middot; 60+ dokumenata<br>"
    "&copy; 2026 LegalTech Suite Pro"
    "</div>",
    unsafe_allow_html=True,
)


# =============================================================================
# SCROLL-TO-TOP
# =============================================================================

def _scroll_to_top():
    """Injektira JS koji scrolla main container na vrh."""
    components.html(
        "<script>parent.document.querySelector('section.main').scrollTo(0,0);</script>",
        height=0,
    )

def _navigate_to(module_name):
    """Navigira na zadani modul."""
    st.session_state._active_module = module_name


# =============================================================================
# POCETNA STRANICA
# =============================================================================

_VODIC_KATEGORIJE = [
    {
        "naslov": "Netko mi duguje novac",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Opomena, ovrha ili tuzba za naplatu duga",
        "moduli": ["Opomena", "Ovrsno pravo", "Tuzbe"],
    },
    {
        "naslov": "Ne slazem se s presudom",
        "tezina": "Slozeno", "vrijeme": "~20 min",
        "opis": "Zalba na presudu \u2014 rok je 15 dana!",
        "moduli": ["Zalbe"],
    },
    {
        "naslov": "Problem s upravnim tijelom",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Zalba na rjesenje, tuzba upravnom sudu",
        "moduli": ["Upravno pravo"],
    },
    {
        "naslov": "Trebam ugovor",
        "tezina": "Jednostavno", "vrijeme": "~10 min",
        "opis": "Kupoprodaja, najam, rad, NDA, raskid...",
        "moduli": ["Ugovori", "Obvezno pravo"],
    },
    {
        "naslov": "Zrtva sam kaznenog djela",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Kaznena prijava ili privatna tuzba",
        "moduli": ["Kazneno pravo"],
    },
    {
        "naslov": "Problem s nekretninom",
        "tezina": "Srednje", "vrijeme": "~10 min",
        "opis": "Uknjizba, hipoteka, sluznost, brisovna tuzba",
        "moduli": ["Zemljisne knjige"],
    },
    {
        "naslov": "Problem kao potrosac",
        "tezina": "Jednostavno", "vrijeme": "~5 min",
        "opis": "Reklamacija, raskid online kupnje",
        "moduli": ["Zastita potrosaca"],
    },
    {
        "naslov": "Tvrtka / poslovni spor",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Drustveni ugovor, prijenos udjela, NDA",
        "moduli": ["Trgovacko pravo"],
    },
    {
        "naslov": "Obiteljski spor",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Razvod, bracni ugovor, skrb, uzdrzavanje",
        "moduli": ["Obiteljsko pravo"],
    },
    {
        "naslov": "Financijske poteskoce",
        "tezina": "Slozeno", "vrijeme": "~20 min",
        "opis": "Osobni stecaj, prijedlog, prijava trazbine",
        "moduli": ["Stecajno pravo"],
    },
]

_TEZINA_BOJA = {
    "Jednostavno": "#059669",
    "Srednje": "#D97706",
    "Slozeno": "#DC2626",
}

_VODIC_DETALJI = {
    "Netko mi duguje novac": {
        "upute": [
            ("1. Opomena pred tuzbu", "Posaljite duznik pisanu opomenu s rokom od 8 dana. Ovo je obavezni preduvjet za ovrhu."),
            ("2. Ovrha ili Tuzba", "Ovrha je brzi put ako imate racun/ugovor. Tuzba ako duznik osporava dug."),
            ("3. Kalkulator kamata", "Izracunajte zakonske zatezne kamate na dugovanje."),
        ],
        "rokovi": "Opci rok zastare: 5 godina (cl. 225. ZOO). Roba/usluge: 3 godine.",
    },
    "Ne slazem se s presudom": {
        "upute": [
            ("Rok za zalbu: 15 dana!", "Od dana dostave presude (cl. 348. ZPP). Podnosi se prvostupanjskom sudu."),
            ("Zalbeni razlozi", "Bitna povreda postupka, pogresno cinjenicno stanje, pogresna primjena prava."),
        ],
        "rokovi": "Rok za zalbu na presudu: 15 dana. Na rjesenje: 8 dana.",
    },
    "Problem s upravnim tijelom": {
        "upute": [
            ("Zalba na rjesenje (ZUP)", "Rok 15 dana od dostave rjesenja."),
            ("Tuzba upravnom sudu (ZUS)", "Rok 30 dana od dostave drugostupanjskog rjesenja."),
            ("Pristup informacijama (ZPPI)", "Tijelo mora odgovoriti u 15 dana."),
        ],
        "rokovi": "ZUP zalba: 15 dana. ZUS tuzba: 30 dana.",
    },
    "Trebam ugovor": {
        "upute": [
            ("Gradansko pravo", "Kupoprodaja, najam, djelo, zajam, NDA."),
            ("Radno pravo", "Ugovor o radu, aneks, rad na daljinu."),
            ("Obvezno pravo", "Darovanje, cesija, kompenzacija, jamstvo."),
        ],
        "rokovi": None,
    },
    "Zrtva sam kaznenog djela": {
        "upute": [
            ("Kaznena prijava", "Drzavnom odvjetnistvu, nema strogog roka."),
            ("Privatna tuzba", "Rok 3 mjeseca od saznanja (cl. 60. KZ). Npr. laka tjelesna ozljeda, kleveta."),
        ],
        "rokovi": "Privatna tuzba: 3 mjeseca od saznanja.",
    },
    "Problem s nekretninom": {
        "upute": [
            ("Uknjizba vlasnistva", "Tabularna isprava za upis vlasnistva."),
            ("Hipoteka", "Upis ili brisanje hipoteke."),
            ("Brisovna tuzba", "Pobijanje nevaljanog upisa u zemljisne knjige."),
        ],
        "rokovi": None,
    },
    "Problem kao potrosac": {
        "upute": [
            ("Reklamacija", "Pisani prigovor trgovcu. Rok odgovora: 15 dana."),
            ("Jednostrani raskid", "Online kupnja \u2014 14 dana bez razloga."),
            ("Prijava inspekciji", "Kad trgovac ne postuje prava potrosaca."),
        ],
        "rokovi": "Reklamacija: rok 2 godine. Online raskid: 14 dana.",
    },
    "Tvrtka / poslovni spor": {
        "upute": [
            ("Drustveni ugovor", "Osnivanje d.o.o."),
            ("Prijenos udjela", "Prodaja ili darovanje udjela."),
            ("NDA", "Ugovor o povjerljivosti."),
        ],
        "rokovi": None,
    },
    "Obiteljski spor": {
        "upute": [
            ("Sporazumni razvod", "Kad se oba supruznika slazu."),
            ("Tuzba za razvod", "Kad nema sporazuma."),
            ("Bracni ugovor / Skrb / Uzdrzavanje", "Reguliranje imovine i brige o djeci."),
        ],
        "rokovi": None,
    },
    "Financijske poteskoce": {
        "upute": [
            ("Osobni stecaj", "Dug >= 3.981,68 EUR, blokada >= 90 dana."),
            ("Prijedlog za stecaj", "Tvrtke u blokadi > 60 dana."),
            ("Prijava trazbine", "Ako ste vjerovnik u stecaju."),
        ],
        "rokovi": "Rok za prijavu trazbine: 60 dana od objave.",
    },
}


def _render_pocetna():
    """Pocetna stranica s vodicem."""

    # Hero
    st.markdown(
        "<div class='hero-section'>"
        "<h2 style='font-size:1.5rem !important;margin-bottom:0.3rem !important;'>"
        "Generirajte pravne dokumente u par klikova</h2>"
        "<p>Odaberite situaciju ispod ili odaberite modul iz izbornika.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # --- Vodic kartice ---
    st.markdown("##### Sto vam treba?")

    cols = st.columns(2)
    for i, kat in enumerate(_VODIC_KATEGORIJE):
        boja = _TEZINA_BOJA.get(kat["tezina"], "#475569")
        with cols[i % 2]:
            # Kartica s gumbom u istom retku
            st.markdown(
                f"<div class='module-card'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
                f"<b style='color:#1E3A5F;font-size:0.95rem;'>{kat['naslov']}</b>"
                f"<span style='background:{boja};color:white;padding:1px 6px;border-radius:3px;"
                f"font-size:0.65rem;font-weight:600;'>{kat['tezina']}</span>"
                f"</div>"
                f"<p style='color:#64748B;font-size:0.8rem;margin:0.3rem 0 0 !important;'>"
                f"{kat['opis']}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
            if st.button(
                f"Pokazi korake",
                key=f"_vk_{i}",
                use_container_width=True,
            ):
                st.session_state._vodic_odabir = kat["naslov"]
                st.rerun()

    # --- Vodic detalji ---
    odabir = st.session_state.get("_vodic_odabir", "")
    if odabir and odabir in _VODIC_DETALJI:
        st.markdown("---")
        detalji = _VODIC_DETALJI[odabir]
        st.markdown(f"### {odabir}")

        for naslov, opis in detalji["upute"]:
            st.markdown(
                f"<div style='background:#EFF3F8;padding:0.8rem 1rem;border-radius:8px;"
                f"border-left:3px solid #1E3A5F;margin-bottom:0.5rem;'>"
                f"<b>{naslov}</b><br>"
                f"<span style='color:#475569;font-size:0.85rem;'>{opis}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        if detalji.get("rokovi"):
            st.info(f"Rokovi: {detalji['rokovi']}")

        # Gumbi za navigaciju
        kat_data = next((k for k in _VODIC_KATEGORIJE if k["naslov"] == odabir), None)
        if kat_data:
            btn_cols = st.columns(len(kat_data["moduli"]))
            for col, modul in zip(btn_cols, kat_data["moduli"]):
                with col:
                    if st.button(f"Otvori: {modul}", key=f"_vn_{modul}", type="primary", use_container_width=True):
                        _navigate_to(modul)
                        st.rerun()

    # --- Alati ---
    st.markdown("---")
    st.markdown("##### Alati")
    _alati = [
        ("e-Predmet", "Pracenje sudskih predmeta"),
        ("Sudske objave", "e-Oglasna ploca sudova"),
        ("Propisi", "Narodne novine, baza zakona"),
        ("Kalendar", "Rocista, rokovi, podsjetnici"),
    ]
    cols = st.columns(4)
    for col, (modul, opis) in zip(cols, _alati):
        with col:
            if st.button(modul, key=f"_alat_{modul}", use_container_width=True):
                _navigate_to(modul)
                st.rerun()
            st.caption(opis)

    cols2 = st.columns(3)
    _alati2 = [
        ("Kamate", "Kalkulator kamata"),
        ("Pristojbe", "Kalkulator pristojbi"),
        ("Zastita potrosaca", "Reklamacija, raskid"),
    ]
    for col, (modul, opis) in zip(cols2, _alati2):
        with col:
            if st.button(modul, key=f"_alat2_{modul}", use_container_width=True):
                _navigate_to(modul)
                st.rerun()
            st.caption(opis)


# =============================================================================
# ROUTING
# =============================================================================

active = st.session_state._active_module

if active != "Pocetna":
    _scroll_to_top()

# DOCX opcije - samo za generatore dokumenata
modul_cfg = _MODULI.get(active, {})
if modul_cfg.get("docx", False):
    docx_opcije()

# Routing
if active == "Pocetna":
    _render_pocetna()
elif active in _MODULI and _MODULI[active]["render"]:
    _MODULI[active]["render"]()
else:
    st.warning(f"Modul '{active}' nije pronaden.")
    st.session_state._active_module = "Pocetna"
    st.rerun()
