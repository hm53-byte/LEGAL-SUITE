# =============================================================================
# LegalTech Suite Pro - Glavni ulaz (entry point)
# v4.0 - Auth, API integracije, kalendar, propisi
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

# Primjena CSS stilova + Google Fonts (link tag je non-blocking)
st.markdown(
    "<link href='https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap' rel='stylesheet'>",
    unsafe_allow_html=True,
)
st.markdown(CSS_STILOVI, unsafe_allow_html=True)

# =============================================================================
# AUTENTIKACIJA - Login ekran prije svega
# =============================================================================

if not login_stranica():
    st.stop()

# =============================================================================
# SIDEBAR NAVIGACIJA
# =============================================================================

_NAV_ICONS = {
    "Početna": "\U0001f3e0",
    "Ugovori i odluke": "\U0001f4dd",
    "Opomena pred tužbu": "\u2709\ufe0f",
    "Punomoć": "\U0001f91d",
    "Obvezno pravo": "\U0001f4d1",
    "Trgovačko pravo": "\U0001f3e2",
    "Obiteljsko pravo": "\U0001f46a",
    "Tužbe": "\u2696\ufe0f",
    "Ovršno pravo": "\U0001f4b0",
    "Žalbe": "\U0001f4e3",
    "Zemljišne knjige": "\U0001f3d7\ufe0f",
    "Upravno pravo": "\U0001f3db\ufe0f",
    "Kazneno pravo": "\U0001f6a8",
    "Stečajno pravo": "\U0001f4c9",
    "e-Predmet": "\U0001f50d",
    "Sudske objave": "\U0001f4cb",
    "Propisi i zakoni": "\U0001f4da",
    "Kalendar": "\U0001f4c5",
    "Kalkulator kamata": "\U0001f4ca",
    "Kalkulator pristojbi": "\U0001f9ee",
    "Zaštita potrošača": "\U0001f6e1\ufe0f",
}

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
    "Praćenje i baze": [
        "e-Predmet",
        "Sudske objave",
        "Propisi i zakoni",
        "Kalendar",
    ],
    "Alati": [
        "Kalkulator kamata",
        "Kalkulator pristojbi",
        "Zaštita potrošača",
    ],
}

if "_active_module" not in st.session_state:
    st.session_state._active_module = "Početna"

# Sidebar header + korisnik
st.sidebar.title("LegalTech Suite Pro")
prikazi_korisnika_sidebar()
st.sidebar.markdown("---")

for section_name, modules in _NAV_SECTIONS.items():
    st.sidebar.markdown(f"<p class='sidebar-section'>{section_name.upper()}</p>", unsafe_allow_html=True)
    for module_name in modules:
        is_active = st.session_state._active_module == module_name
        btn_type = "primary" if is_active else "secondary"
        icon = _NAV_ICONS.get(module_name, "")
        label = f"{'▸ ' if is_active else ''}{icon} {module_name}"
        if st.sidebar.button(
            label,
            key=f"_sb_{module_name}",
            type=btn_type,
            use_container_width=True,
        ):
            st.session_state._active_module = module_name
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='text-align: center; font-size: 0.7rem; color: #94A3B8 !important; "
    "font-family: Inter, sans-serif; padding: 0.5rem 0;'>"
    "v4.0 &middot; 60+ dokumenata &middot; 4 API-ja<br>"
    "LegalTech Suite Pro &copy; 2026"
    "</div>",
    unsafe_allow_html=True,
)


# =============================================================================
# SCROLL-TO-TOP - Svaka promjena modula scrolla na vrh
# =============================================================================

def _scroll_to_top():
    """Injektira JS koji scrolla Streamlit main container na vrh."""
    components.html(
        "<script>parent.document.querySelector('section.main').scrollTo(0, 0);</script>",
        height=0,
    )


def _scroll_to_anchor(anchor_id):
    """Injektira JS koji scrolla do specificnog elementa."""
    components.html(
        f"<script>"
        f"var el = parent.document.getElementById('{anchor_id}');"
        f"if (el) el.scrollIntoView({{behavior: 'smooth', block: 'start'}});"
        f"</script>",
        height=0,
    )


def _navigate_to(module_name):
    """Navigira na zadani modul."""
    st.session_state._active_module = module_name


# =============================================================================
# POCETNA STRANICA (s integriranim vodicem)
# =============================================================================

_VODIC_KATEGORIJE = [
    {
        "ikona": "\U0001f4b8", "naslov": "Netko mi duguje novac",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Opomena, ovrha ili tužba za naplatu duga",
    },
    {
        "ikona": "\U0001f4e3", "naslov": "Ne slažem se s presudom",
        "tezina": "Složeno", "vrijeme": "~20 min",
        "opis": "Žalba na presudu \u2014 rok je 15 dana!",
    },
    {
        "ikona": "\U0001f3db\ufe0f", "naslov": "Problem s upravnim tijelom",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Žalba na rješenje, tužba, pristup informacijama",
    },
    {
        "ikona": "\U0001f4dd", "naslov": "Trebam ugovor",
        "tezina": "Jednostavno", "vrijeme": "~10 min",
        "opis": "Kupoprodaja, najam, rad, NDA, raskid...",
    },
    {
        "ikona": "\U0001f6a8", "naslov": "Žrtva sam kaznenog djela",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Kaznena prijava ili privatna tužba",
    },
    {
        "ikona": "\U0001f3d7\ufe0f", "naslov": "Problem s nekretninom",
        "tezina": "Srednje", "vrijeme": "~10 min",
        "opis": "Uknjižba, hipoteka, služnost, brisovna tužba",
    },
    {
        "ikona": "\U0001f6e1\ufe0f", "naslov": "Problem kao potrošač",
        "tezina": "Jednostavno", "vrijeme": "~5 min",
        "opis": "Reklamacija, raskid online kupnje, inspekcija",
    },
    {
        "ikona": "\U0001f3e2", "naslov": "Tvrtka / poslovni spor",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Društveni ugovor, prijenos udjela, NDA",
    },
    {
        "ikona": "\U0001f46a", "naslov": "Obiteljski spor",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Razvod, bračni ugovor, skrb, uzdržavanje",
    },
    {
        "ikona": "\U0001f4c9", "naslov": "Financijske poteškoće",
        "tezina": "Složeno", "vrijeme": "~20 min",
        "opis": "Osobni stečaj, prijedlog za stečaj, prijava tražbine",
    },
]

_TEZINA_BOJA = {
    "Jednostavno": "#059669",
    "Srednje": "#D97706",
    "Složeno": "#DC2626",
}


def _render_vodic_detalji(odabir):
    """Prikazuje detaljne korake za odabranu vodic kategoriju."""
    st.markdown("<div id='vodic-detalji'></div>", unsafe_allow_html=True)
    st.markdown("---")

    if odabir == "Netko mi duguje novac":
        st.markdown("### \U0001f4b8 Koraci za naplatu dugovanja")
        st.markdown(
            "<div style='background:#EFF3F8;padding:1rem 1.2rem;border-radius:8px;"
            "border-left:4px solid #1E3A5F;margin-bottom:1rem;'>"
            "<b>1. Opomena pred tužbu</b> (preporučeno prvo)<br>"
            "Pošaljite dužniku pisanu opomenu s rokom od 8 dana. "
            "Ovo je obavezni preduvjet za ovrhu. Sačuvajte dokaz slanja."
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("\u2709\ufe0f Izradi opomenu", key="_v_opomena", type="primary"):
            _navigate_to("Opomena pred tužbu")
            st.rerun()

        st.markdown(
            "<div style='background:#EFF3F8;padding:1rem 1.2rem;border-radius:8px;"
            "border-left:4px solid #1E3A5F;margin-bottom:1rem;'>"
            "<b>2. Ovrha ili Tužba</b> (ako dužnik ne plati)<br>"
            "<b>Ovrha</b> \u2014 brži put ako imate račun/ugovor \u2192 javni bilježnik<br>"
            "<b>Tužba</b> \u2014 ako dužnik osporava dug \u2192 sud"
            "</div>",
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        if c1.button("\U0001f4b0 Ovrha", key="_v_ovrha", type="primary", use_container_width=True):
            _navigate_to("Ovršno pravo")
            st.rerun()
        if c2.button("\u2696\ufe0f Tužba", key="_v_tuzba", type="primary", use_container_width=True):
            _navigate_to("Tužbe")
            st.rerun()

        st.markdown(
            "<div style='background:#EFF3F8;padding:1rem 1.2rem;border-radius:8px;"
            "border-left:4px solid #1E3A5F;margin-bottom:1rem;'>"
            "<b>3. Kalkulator kamata</b><br>"
            "Izračunajte zakonske zatezne kamate na dugovanje."
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("\U0001f4ca Kalkulator kamata", key="_v_kamate"):
            _navigate_to("Kalkulator kamata")
            st.rerun()

        with st.expander("Važni zastarni rokovi"):
            st.markdown(
                "- **Opći rok:** 5 godina (čl. 225. ZOO)\n"
                "- **Roba/usluge:** 3 godine (čl. 226. ZOO)\n"
                "- **Naknada štete:** 3 god. od saznanja / 5 god. objektivno\n"
                "- **Radnopravna:** 5 godina (čl. 135. ZR)"
            )

    elif odabir == "Ne slažem se s presudom":
        st.markdown("### \U0001f4e3 Žalba na presudu")
        st.error("**Rok za žalbu je 15 dana** od dana dostave presude (čl. 348. ZPP). Hitno!")
        st.markdown(
            "- Žalba se podnosi prvostupanjskom sudu, a o njoj odlučuje drugostupanjski\n"
            "- Žalbeni razlozi: bitna povreda postupka, pogrešno činjenično stanje, pogrešna primjena prava\n"
            "- Trebate: poslovni broj presude, datum dostave, obrazloženje"
        )
        if st.button("\U0001f4e3 Izradi žalbu", key="_v_zalba", type="primary"):
            _navigate_to("Žalbe")
            st.rerun()

    elif odabir == "Problem s upravnim tijelom":
        st.markdown("### \U0001f3db\ufe0f Upravno pravo")
        st.markdown(
            "**Žalba na rješenje (ZUP)** \u2014 rok **15 dana** od dostave\n\n"
            "**Tužba upravnom sudu (ZUS)** \u2014 rok **30 dana** od dostave drugostupanjskog rješenja\n\n"
            "**Pristup informacijama (ZPPI)** \u2014 tijelo mora odgovoriti u **15 dana**"
        )
        if st.button("\U0001f3db\ufe0f Upravno pravo", key="_v_upravno", type="primary"):
            _navigate_to("Upravno pravo")
            st.rerun()

    elif odabir == "Trebam ugovor":
        st.markdown("### \U0001f4dd Ugovori")
        st.markdown(
            "**Građansko pravo** \u2014 kupoprodaja, najam, djelo, zajam\n\n"
            "**Radno pravo** \u2014 ugovor o radu, otkaz, aneks, rad na daljinu\n\n"
            "**Obvezno pravo** \u2014 darovanje, cesija, kompenzacija, jamstvo\n\n"
            "**Slobodna forma** \u2014 ugovor po mjeri s bibliotekom klauzula"
        )
        c1, c2 = st.columns(2)
        if c1.button("\U0001f4dd Ugovori", key="_v_ugovori", type="primary", use_container_width=True):
            _navigate_to("Ugovori i odluke")
            st.rerun()
        if c2.button("\U0001f4d1 Obvezno pravo", key="_v_obvezno", type="primary", use_container_width=True):
            _navigate_to("Obvezno pravo")
            st.rerun()

    elif odabir == "Žrtva sam kaznenog djela":
        st.markdown("### \U0001f6a8 Kazneno pravo")
        st.markdown(
            "**Kaznena prijava** \u2014 Državnom odvjetništvu, nema strogog roka\n\n"
            "**Privatna tužba** \u2014 rok **3 mjeseca** od saznanja (čl. 60. KZ)\n"
            "Npr. laka tjelesna ozljeda, kleveta, uvreda"
        )
        if st.button("\U0001f6a8 Kazneno pravo", key="_v_kazneno", type="primary"):
            _navigate_to("Kazneno pravo")
            st.rerun()

    elif odabir == "Problem s nekretninom":
        st.markdown("### \U0001f3d7\ufe0f Zemljišne knjige")
        st.markdown(
            "**Uknjižba vlasništva** \u2014 tabularna isprava za upis\n\n"
            "**Hipoteka** \u2014 upis/brisanje\n\n"
            "**Služnost** \u2014 osnivanje prava služnosti\n\n"
            "**Brisovna tužba** \u2014 pobijanje nevaljanog upisa"
        )
        if st.button("\U0001f3d7\ufe0f Zemljišne knjige", key="_v_zk", type="primary"):
            _navigate_to("Zemljišne knjige")
            st.rerun()

    elif odabir == "Problem kao potrošač":
        st.markdown("### \U0001f6e1\ufe0f Zaštita potrošača")
        st.markdown(
            "**Reklamacija** \u2014 pisani prigovor trgovcu (rok odgovora: **15 dana**)\n\n"
            "**Jednostrani raskid** \u2014 online kupnja, **14 dana** bez razloga\n\n"
            "**Prijava inspekciji** \u2014 kad trgovac ne poštuje prava"
        )
        if st.button("\U0001f6e1\ufe0f Zaštita potrošača", key="_v_potrosaci", type="primary"):
            _navigate_to("Zaštita potrošača")
            st.rerun()

    elif odabir == "Tvrtka / poslovni spor":
        st.markdown("### \U0001f3e2 Trgovačko pravo")
        st.markdown(
            "**Društveni ugovor** \u2014 osnivanje d.o.o.\n\n"
            "**Prijenos udjela** \u2014 prodaja/darovanje udjela\n\n"
            "**Odluka/Zapisnik skupštine** \u2014 formalne odluke\n\n"
            "**NDA** \u2014 ugovor o povjerljivosti"
        )
        if st.button("\U0001f3e2 Trgovačko pravo", key="_v_trgovacko", type="primary"):
            _navigate_to("Trgovačko pravo")
            st.rerun()

    elif odabir == "Obiteljski spor":
        st.markdown("### \U0001f46a Obiteljsko pravo")
        st.markdown(
            "**Sporazumni razvod** \u2014 kad se oba supružnika slažu\n\n"
            "**Tužba za razvod** \u2014 kad nema sporazuma\n\n"
            "**Bračni ugovor** \u2014 reguliranje imovine\n\n"
            "**Roditeljska skrb / Uzdržavanje**"
        )
        if st.button("\U0001f46a Obiteljsko pravo", key="_v_obiteljsko", type="primary"):
            _navigate_to("Obiteljsko pravo")
            st.rerun()

    elif odabir == "Financijske poteškoće":
        st.markdown("### \U0001f4c9 Stečajno pravo")
        st.markdown(
            "**Osobni stečaj** \u2014 dug \u2265 3.981,68 EUR, blokada \u2265 90 dana\n\n"
            "**Prijedlog za stečaj** \u2014 tvrtke u blokadi > 60 dana\n\n"
            "**Prijava tražbine** \u2014 ako ste vjerovnik u stečaju"
        )
        if st.button("\U0001f4c9 Stečajno pravo", key="_v_stecajno", type="primary"):
            _navigate_to("Stečajno pravo")
            st.rerun()


def _render_pocetna():
    """Pocetna stranica s integriranim vodicem."""

    # Hero sekcija
    st.markdown(
        "<div class='hero-section'>"
        "<h2>LegalTech Suite Pro</h2>"
        "<p>Odaberite situaciju u kojoj se nalazite i dobit ćete upute korak po korak, "
        "ili izaberite uslugu iz izbornika.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ----- VODIC: kartice problema u 2 stupca -----
    st.markdown("##### \U0001f9ed Što vam treba?")
    st.caption("Kliknite na svoju situaciju \u2014 dobit ćete upute i link na pravi dokument.")

    cols = st.columns(2)
    for i, kat in enumerate(_VODIC_KATEGORIJE):
        boja = _TEZINA_BOJA.get(kat["tezina"], "#475569")
        with cols[i % 2]:
            st.markdown(
                f"<div class='module-card' style='cursor:pointer;'>"
                f"<h4>{kat['ikona']} {kat['naslov']}</h4>"
                f"<p>{kat['opis']}</p>"
                f"<p style='margin-top:0.4rem !important;'>"
                f"<span style='background:{boja};color:white;padding:2px 8px;border-radius:4px;"
                f"font-size:0.7rem;font-weight:600;'>{kat['tezina']}</span>"
                f"&nbsp;&nbsp;<span style='color:#94A3B8;font-size:0.75rem;'>{kat['vrijeme']}</span>"
                f"</p></div>",
                unsafe_allow_html=True,
            )
            if st.button(
                f"Pokaži korake \u2192",
                key=f"_vk_{i}",
                use_container_width=True,
            ):
                st.session_state._vodic_odabir = kat["naslov"]
                st.rerun()

    # ----- VODIC DETALJI (ako je odabrana kategorija) -----
    odabir = st.session_state.get("_vodic_odabir", "")
    if odabir:
        _render_vodic_detalji(odabir)
        _scroll_to_anchor("vodic-detalji")

    # ----- ALATI (kompaktno) -----
    st.markdown("---")
    st.markdown("##### Alati i baze podataka")
    col1, col2, col3, col4 = st.columns(4)
    _alati = [
        ("\U0001f50d e-Predmet", "e-Predmet"),
        ("\U0001f4cb Sudske objave", "Sudske objave"),
        ("\U0001f4da Propisi", "Propisi i zakoni"),
        ("\U0001f4c5 Kalendar", "Kalendar"),
    ]
    for col, (label, modul) in zip([col1, col2, col3, col4], _alati):
        with col:
            if st.button(label, key=f"_alat_{modul}", use_container_width=True):
                _navigate_to(modul)
                st.rerun()

    col5, col6, col7 = st.columns(3)
    _alati2 = [
        ("\U0001f4ca Kalkulator kamata", "Kalkulator kamata"),
        ("\U0001f9ee Kalkulator pristojbi", "Kalkulator pristojbi"),
        ("\U0001f6e1\ufe0f Zaštita potrošača", "Zaštita potrošača"),
    ]
    for col, (label, modul) in zip([col5, col6, col7], _alati2):
        with col:
            if st.button(label, key=f"_alat2_{modul}", use_container_width=True):
                _navigate_to(modul)
                st.rerun()

    st.caption(
        "Svi dokumenti generiraju se u DOCX formatu (Microsoft Word) "
        "s hrvatskim pravnim formatiranjem \u2014 Times New Roman 12pt, margine 2.5cm."
    )


# =============================================================================
# ROUTING
# =============================================================================

active = st.session_state._active_module

# Scroll na vrh pri svakoj promjeni modula (osim Pocetne pri prvom ulasku)
if active != "Početna":
    _scroll_to_top()

# DOCX opcije - samo za generatore dokumenata
_NO_DOCX_OPTS = {
    "Početna", "Kalkulator kamata", "Kalkulator pristojbi",
    "e-Predmet", "Sudske objave", "Propisi i zakoni", "Kalendar",
}
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
elif active == "e-Predmet":
    render_epredmet()
elif active == "Sudske objave":
    render_eoglasna()
elif active == "Propisi i zakoni":
    render_nn_pretraga()
elif active == "Kalendar":
    render_kalendar()
elif active == "Kalkulator kamata":
    render_kamate()
elif active == "Kalkulator pristojbi":
    render_pristojbe()
elif active == "Zaštita potrošača":
    render_potrosaci()
