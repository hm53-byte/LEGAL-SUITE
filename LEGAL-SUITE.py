# =============================================================================
# LegalTech Suite Pro - Glavni ulaz (entry point)
# v4.1 - UI overhaul, search, fix bugs, cleaner nav
# =============================================================================
import streamlit as st
import streamlit.components.v1 as components
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
    render_epredmet,
    render_eoglasna,
    render_kalendar,
    render_nn_pretraga,
    render_jednostavno,
    render_posrednik_najam,
    render_pravila,
)
from auth import login_stranica, prikazi_korisnika_sidebar, provjeri_auth, _authenticate

# Konfiguracija stranice
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=PAGE_LAYOUT)

# Primjena CSS stilova (Inter Variable Font ucitava se iz config.py via @import)
st.markdown(CSS_STILOVI, unsafe_allow_html=True)

# =============================================================================
# JS: OIB (11 znakova) i MBS (8 znakova) - samo brojevi (numeric input filter)
# =============================================================================
components.html("""
<script>
(function(){
    function enforceNumeric(){
        var inputs=parent.document.querySelectorAll('input[maxlength="11"],input[maxlength="8"]');
        inputs.forEach(function(inp){
            if(inp._numFilter) return;
            inp._numFilter=true;
            inp.setAttribute('inputmode','numeric');
            inp.addEventListener('keydown',function(e){
                if([8,9,13,27,46,35,36,37,38,39,40].indexOf(e.keyCode)!==-1||
                   (e.ctrlKey&&[65,67,86,88].indexOf(e.keyCode)!==-1)||
                   (e.metaKey&&[65,67,86,88].indexOf(e.keyCode)!==-1)) return;
                if((e.shiftKey||(e.keyCode<48||e.keyCode>57))&&(e.keyCode<96||e.keyCode>105)){
                    e.preventDefault();
                }
            });
            inp.addEventListener('paste',function(e){
                var d=(e.clipboardData||window.clipboardData).getData('text');
                if(!/^\\d*$/.test(d)){
                    e.preventDefault();
                    var clean=d.replace(/\\D/g,'');
                    if(clean) document.execCommand('insertText',false,clean);
                }
            });
        });
    }
    enforceNumeric();
    new MutationObserver(enforceNumeric).observe(parent.document.body,{childList:true,subtree:true});
})();
</script>
""", height=0)

# =============================================================================
# MODE TOGGLE: Jednostavno / Napredno
# =============================================================================

if "_app_mode" not in st.session_state:
    st.session_state._app_mode = "jednostavno"

# Jednostavni mod — auto-authenticate kao gost, bez login stranice
if st.session_state._app_mode == "jednostavno":
    if not provjeri_auth():
        _authenticate("gost@legalsuite.hr", "Gost", role="guest", provider="guest")
else:
    # Napredno — standardna autentikacija
    if not login_stranica():
        st.stop()

# =============================================================================
# NAVIGACIJSKA STRUKTURA
# =============================================================================

_MODULI = {
    "Početna":           {"render": None,             "grupa": None,    "docx": False, "opis": "Početna stranica"},
    "Ugovori":           {"render": render_ugovori,   "grupa": "Dokumenti", "docx": True,  "opis": "Kupoprodaja, najam, rad, NDA, raskid..."},
    "Opomena":           {"render": render_opomene,    "grupa": "Dokumenti", "docx": True,  "opis": "Opomena pred tužbu"},
    "Punomoć":           {"render": render_punomoci,   "grupa": "Dokumenti", "docx": True,  "opis": "Punomoć za zastupanje"},
    "Obvezno pravo":     {"render": render_obvezno,    "grupa": "Dokumenti", "docx": True,  "opis": "Darovanje, cesija, kompenzacija, jamstvo..."},
    "Trgovačko pravo":   {"render": render_trgovacko,  "grupa": "Dokumenti", "docx": True,  "opis": "Društveni ugovor, prijenos udjela, NDA..."},
    "Obiteljsko pravo":  {"render": render_obiteljsko, "grupa": "Dokumenti", "docx": True,  "opis": "Razvod, bračni ugovor, skrb, uzdržavanje"},
    "Posrednik u najmu": {"render": render_posrednik_najam, "grupa": "Dokumenti", "docx": True, "opis": "Korporativni smještaj: A-B najam + B-C upravljanje"},
    "Tužbe":             {"render": render_tuzbe,      "grupa": "Sudski postupci", "docx": True,  "opis": "Tužba za isplatu, naknada štete"},
    "Ovršno pravo":      {"render": render_ovrhe,      "grupa": "Sudski postupci", "docx": True,  "opis": "Ovrha putem JB, prigovor, obustava"},
    "Žalbe":             {"render": render_zalbe,       "grupa": "Sudski postupci", "docx": True,  "opis": "Žalba na presudu"},
    "Zemljišne knjige":  {"render": render_zemljisne,   "grupa": "Sudski postupci", "docx": True,  "opis": "Uknjižba, hipoteka, služnost..."},
    "Upravno pravo":     {"render": render_upravno,     "grupa": "Sudski postupci", "docx": True,  "opis": "Žalba ZUP, tužba ZUS, pristup info"},
    "Kazneno pravo":     {"render": render_kazneno,     "grupa": "Sudski postupci", "docx": True,  "opis": "Kaznena prijava, privatna tužba, žalba"},
    "Stečajno pravo":    {"render": render_stecajno,    "grupa": "Sudski postupci", "docx": True,  "opis": "Osobni stečaj, prijedlog, prijava tražbine"},
    "Zaštita potrošača": {"render": render_potrosaci,   "grupa": "Sudski postupci", "docx": True,  "opis": "Reklamacija, raskid online kupnje"},
    "e-Predmet":         {"render": render_epredmet,    "grupa": "Alati",  "docx": False, "opis": "Praćenje sudskih predmeta"},
    "Sudske objave":     {"render": render_eoglasna,    "grupa": "Alati",  "docx": False, "opis": "e-Oglasna ploča sudova"},
    "Propisi":           {"render": render_nn_pretraga, "grupa": "Alati",  "docx": False, "opis": "Narodne novine, baza zakona"},
    "Kalendar":          {"render": render_kalendar,    "grupa": "Alati",  "docx": False, "opis": "Ročišta, rokovi, podsjetnici"},
    "Kamate":            {"render": render_kamate,      "grupa": "Alati",  "docx": False, "opis": "Kalkulator zakonskih zateznih kamata"},
    "Pristojbe":         {"render": render_pristojbe,   "grupa": "Alati",  "docx": False, "opis": "Kalkulator sudskih pristojbi"},
    "Pravila i privatnost": {"render": render_pravila,  "grupa": "Alati",  "docx": False, "opis": "Uvjeti korištenja, GDPR, watermark"},
}

# Grupe za sidebar
_GRUPE = ["Dokumenti", "Sudski postupci", "Alati"]

if "_active_module" not in st.session_state:
    st.session_state._active_module = "Početna"

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

# Mode toggle
_current_mode = st.session_state.get("_app_mode", "jednostavno")
_mode_label = "Jednostavno" if _current_mode == "jednostavno" else "Napredno"
_toggle_label = "Prebaci na Napredno" if _current_mode == "jednostavno" else "Prebaci na Jednostavno"

st.sidebar.markdown(
    f"<div style='background:rgba(255,255,255,0.06);padding:0.4rem 0.7rem;"
    f"border-radius:6px;margin-bottom:0.5rem;text-align:center;'>"
    f"<span style='font-size:0.7rem;color:#94A3B8;'>Nacin rada: </span>"
    f"<span style='font-size:0.75rem;color:#D4A843;font-weight:600;'>{_mode_label}</span>"
    f"</div>",
    unsafe_allow_html=True,
)
if st.sidebar.button(_toggle_label, key="_mode_toggle", use_container_width=True):
    if _current_mode == "jednostavno":
        st.session_state._app_mode = "napredno"
    else:
        st.session_state._app_mode = "jednostavno"
        st.session_state._jed_odabir = None
    st.rerun()

st.sidebar.markdown("")

# Sidebar navigacija - skrivena u jednostavnom modu
_is_simple_mode = st.session_state.get("_app_mode") == "jednostavno"
if _is_simple_mode:
    st.sidebar.markdown(
        "<div style='color:#64748B;font-size:0.75rem;padding:0.5rem 0.7rem;"
        "line-height:1.5;'>Koristite jednostavni nacin rada. "
        "Prebacite na <b>Napredno</b> za puni pristup svim modulima.</div>",
        unsafe_allow_html=True,
    )

# Pretraga u sidebaru
_search_query = "" if _is_simple_mode else st.sidebar.text_input(
    "Pretrazi module",
    placeholder="npr. ugovor, ovrha, zalba...",
    key="_sidebar_search",
    label_visibility="collapsed",
)

# Filtrirani moduli — skriveni u jednostavnom modu
if not _is_simple_mode:
    if _search_query:
        _q = _search_query.lower()
        _filtered = {
            k: v for k, v in _MODULI.items()
            if k != "Početna" and (_q in k.lower() or _q in v["opis"].lower())
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
        # Početna gumb
        is_home = st.session_state._active_module == "Početna"
        if st.sidebar.button(
            f"{'> ' if is_home else ''}Početna",
            key="_sb_Početna",
            type="primary" if is_home else "secondary",
            use_container_width=True,
        ):
            st.session_state._active_module = "Početna"
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

# K3 monetizacija (2026-04-27): "Pretplati se na PRO" CTA u sidebar.
# Gumb se prikazuje SAMO ako su Streamlit secrets postavljeni (Supabase + CF Worker URL)
# I ako je korisnik logiran I NIJE vec PRO. Inace je no-op (sidebar tih).
try:
    import entitlements as _ent
    with st.sidebar:
        _ent.render_subscribe_cta(label="Pretplati se na PRO", key="_pro_cta_sidebar")
except Exception:
    # entitlements modul nije dostupan ili Supabase ne odgovara — sidebar nastavlja bez CTA
    pass

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
    import time
    components.html(
        f"<script>setTimeout(function(){{"
        f"var el=parent.document.querySelector('section.main');"
        f"if(el)el.scrollTo(0,0);"
        f"}},50);</script><!-- {time.time()} -->",
        height=0,
    )

def _scroll_to_element(css_selector):
    """Injektira JS koji scrolla main container do specificnog elementa.

    Koristi MutationObserver + 600ms timeout fallback jer Streamlit iframe
    rerender ima varijabilan timing — element ponekad jos nije renderiran
    300ms nakon st.rerun.
    """
    import time
    components.html(
        f"<script>(function(){{"
        f"var attempts=0;"
        f"function tryScroll(){{"
        f"var target=parent.document.querySelector('{css_selector}');"
        f"var container=parent.document.querySelector('section.main');"
        f"if(target&&container){{"
        f"var rect=target.getBoundingClientRect();"
        f"var cRect=container.getBoundingClientRect();"
        f"container.scrollTo({{top:container.scrollTop+(rect.top-cRect.top)-20,"
        f"behavior:'smooth'}});"
        f"return true;"
        f"}}"
        f"return false;"
        f"}}"
        f"// Pokusaj odmah, pa 200ms i 600ms ako element jos nije renderiran"
        f"if(tryScroll()) return;"
        f"setTimeout(function(){{if(tryScroll()) return;"
        f"setTimeout(tryScroll,400);}},200);"
        f"}})();</script><!-- {time.time_ns()} -->",
        height=0,
    )

def _navigate_to(module_name):
    """Navigira na zadani modul."""
    st.session_state._active_module = module_name


# =============================================================================
# POČETNA STRANICA
# =============================================================================

# Katalog pravnih područja (objektivna taksonomija po HR pravu).
# Refactor 2026-04-27 K5: prijašnji "_VODIC_KATEGORIJE" je klasificirao korisnikov
# problem u prirodnom jeziku ("Netko mi duguje novac" -> ovrha) — to je impliciran
# klasifikator pravnog problema (rub nadripisarstva ZO čl. 72; AI Act 2026 Annex
# III pt. 8 visoko-rizična zona). Preimenovan u _PODRUCJA_KATALOG s objektivnim
# pravnim područjima — korisnik sam bira što treba, app ne klasificira.
# Polja "tezina"/"vrijeme" ostaju kao **objektivna kompleksnost forme** (broj polja
# za popunit), NE kao "kompliciranost vašeg slučaja". Stari naziv varijable ostavljen
# kao alias da se ne lome eventualni vanjski importi.
_PODRUCJA_KATALOG = [
    {
        "naslov": "Ovršno pravo",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Opomene, ovršni prijedlozi, prigovori",
        "moduli": ["Opomena", "Ovršno pravo"],
    },
    {
        "naslov": "Tužbe i parnica",
        "tezina": "Složeno", "vrijeme": "~20 min",
        "opis": "Tužbe za isplatu, naknadu štete, utvrđenje",
        "moduli": ["Tužbe"],
    },
    {
        "naslov": "Žalbe (ZPP)",
        "tezina": "Složeno", "vrijeme": "~20 min",
        "opis": "Žalbe na presude i rješenja u parničnom postupku",
        "moduli": ["Žalbe"],
    },
    {
        "naslov": "Upravno pravo",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Žalbe na rješenja, tužbe upravnom sudu, ZPPI zahtjevi",
        "moduli": ["Upravno pravo"],
    },
    {
        "naslov": "Ugovori",
        "tezina": "Jednostavno", "vrijeme": "~10 min",
        "opis": "Kupoprodaja, najam, ugovor o radu, NDA, raskid",
        "moduli": ["Ugovori", "Obvezno pravo"],
    },
    {
        "naslov": "Kazneno pravo",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Kaznene prijave, privatne tužbe",
        "moduli": ["Kazneno pravo"],
    },
    {
        "naslov": "Zemljišne knjige",
        "tezina": "Srednje", "vrijeme": "~10 min",
        "opis": "Uknjižba, hipoteka, služnost, brisovne tužbe",
        "moduli": ["Zemljišne knjige"],
    },
    {
        "naslov": "Zaštita potrošača",
        "tezina": "Jednostavno", "vrijeme": "~5 min",
        "opis": "Reklamacije, raskid online kupnje, prigovori",
        "moduli": ["Zaštita potrošača"],
    },
    {
        "naslov": "Trgovačko pravo",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Društveni ugovori, prijenosi udjela, NDA",
        "moduli": ["Trgovačko pravo"],
    },
    {
        "naslov": "Obiteljsko pravo",
        "tezina": "Srednje", "vrijeme": "~15 min",
        "opis": "Razvodi, bračni ugovori, skrb, uzdržavanje",
        "moduli": ["Obiteljsko pravo"],
    },
    {
        "naslov": "Stečajno pravo",
        "tezina": "Složeno", "vrijeme": "~20 min",
        "opis": "Osobni stečaj, prijedlozi, prijave tražbina",
        "moduli": ["Stečajno pravo"],
    },
]
# Backwards-compatibility alias za eventualne vanjske importe.
_VODIC_KATEGORIJE = _PODRUCJA_KATALOG
_TEZINA_BOJA = {
    "Jednostavno": "#059669",
    "Srednje": "#D97706",
    "Složeno": "#DC2626",
}

# Faktički katalog dokumenata po pravnom području.
# Refactor 2026-04-27 K5: prijašnji "_VODIC_DETALJI" je sadržavao savjetodavne upute
# tipa "rok je 15 dana — žuri se!" što je rub nadripisarstva (ZO čl. 72) i ulazi
# u AI Act 2026 Annex III pt. 8 zonu ("AI in administration of justice"). Refaktoriran
# u faktičku enumeraciju dokumenata bez vremenskih push-ova ili procesualnih savjeta.
# Zakonski rokovi se ne prikazuju ovdje — oni su dio konkretnog dokumenta i provjeravaju
# se u zakonu ili kod odvjetnika; app ih ne sugerira u UI-u.
_PODRUCJA_DETALJI = {
    "Ovršno pravo": {
        "dokumenti": [
            ("Opomena pred tužbu", "Pisana opomena dužniku."),
            ("Ovršni prijedlog", "Prijedlog za ovrhu na temelju vjerodostojne ili ovršne isprave."),
            ("Kalkulator kamata", "Izračun zakonskih zateznih kamata (informativni alat, ne pravni savjet)."),
        ],
    },
    "Tužbe i parnica": {
        "dokumenti": [
            ("Tužba za isplatu", "Tužbeni zahtjev za novčanu obvezu."),
            ("Tužba za naknadu štete", "Tužbeni zahtjev za materijalnu/nematerijalnu štetu."),
        ],
    },
    "Žalbe (ZPP)": {
        "dokumenti": [
            ("Žalba na presudu", "Pravni lijek protiv prvostupanjske presude (ZPP)."),
            ("Žalba na rješenje", "Pravni lijek protiv prvostupanjskog rješenja (ZPP)."),
        ],
    },
    "Upravno pravo": {
        "dokumenti": [
            ("Žalba na rješenje (ZUP)", "Pravni lijek protiv prvostupanjskog upravnog rješenja."),
            ("Tužba upravnom sudu (ZUS)", "Tužba protiv drugostupanjskog upravnog rješenja."),
            ("Zahtjev za pristup informacijama (ZPPI)", "Zahtjev tijelu javne vlasti."),
        ],
    },
    "Ugovori": {
        "dokumenti": [
            ("Građanski ugovori", "Kupoprodaja, najam, djelo, zajam, NDA."),
            ("Radni ugovori", "Ugovor o radu, aneks, rad na daljinu."),
            ("Obvezno pravo", "Darovanje, cesija, kompenzacija, jamstvo."),
        ],
    },
    "Kazneno pravo": {
        "dokumenti": [
            ("Kaznena prijava", "Prijava državnom odvjetništvu."),
            ("Privatna tužba", "Privatna tužba u kaznenom postupku."),
        ],
    },
    "Zemljišne knjige": {
        "dokumenti": [
            ("Uknjižba vlasništva", "Tabularna isprava za upis vlasništva."),
            ("Hipoteka", "Upis ili brisanje hipoteke."),
            ("Brisovna tužba", "Tužba radi brisanja upisa u zemljišne knjige."),
        ],
    },
    "Zaštita potrošača": {
        "dokumenti": [
            ("Reklamacija", "Pisani prigovor trgovcu."),
            ("Jednostrani raskid online kupnje", "Obavijest o raskidu ugovora sklopljenog na daljinu."),
            ("Prijava inspekciji", "Prijava nadležnoj inspekciji."),
        ],
    },
    "Trgovačko pravo": {
        "dokumenti": [
            ("Društveni ugovor", "Osnivački akt d.o.o."),
            ("Prijenos udjela", "Ugovor o prodaji ili darovanju udjela."),
            ("NDA", "Ugovor o povjerljivosti."),
        ],
    },
    "Obiteljsko pravo": {
        "dokumenti": [
            ("Sporazumni razvod", "Sporazumni prijedlog za razvod braka."),
            ("Tužba za razvod", "Tužbeni zahtjev za razvod braka."),
            ("Bračni ugovor / skrb / uzdržavanje", "Reguliranje imovinskih odnosa, skrbi i uzdržavanja."),
        ],
    },
    "Stečajno pravo": {
        "dokumenti": [
            ("Osobni stečaj", "Prijedlog za otvaranje postupka osobnog stečaja."),
            ("Prijedlog za stečaj (pravne osobe)", "Prijedlog za otvaranje stečajnog postupka."),
            ("Prijava tražbine", "Prijava vjerovnika u stečajnom postupku."),
        ],
    },
}
# Backwards-compatibility alias.
_VODIC_DETALJI = _PODRUCJA_DETALJI


def _render_pocetna():
    """Početna stranica s vodičem."""

    # Hero
    st.markdown(
        "<div class='hero-section'>"
        "<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;"
        "font-weight:600;color:rgba(255,255,255,0.5);margin-bottom:0.6rem !important;"
        "position:relative;z-index:1;'>LegalTech Suite Pro</p>"
        "<h2 style='font-size:2rem !important;margin-bottom:0.6rem !important;"
        "line-height:1.2 !important;'>Generirajte pravne dokumente<br>"
        "u par klikova</h2>"
        "<p style='font-size:1.05rem !important;line-height:1.6 !important;'>"
        "60+ hrvatskih pravnih dokumenata. Odaberite modul iz kataloga "
        "ispod ili iz bočnog izbornika. Aplikacija ne pruža pravne savjete.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # --- Disclaimer (K5 refactor 2026-04-27, anti-nadripisarstvo + AI Act 2026 Annex III pt. 8 out-of-scope) ---
    st.markdown(
        "<div style='background:#FEF3C7;border-left:3px solid #D97706;"
        "padding:0.7rem 1rem;margin:0.4rem 0 1rem 0;border-radius:6px;font-size:0.82rem;"
        "color:#451A03;line-height:1.5;'>"
        "<b>Napomena:</b> aplikacija ne pruža pravne savjete niti analizira vašu situaciju. "
        "Generira deterministički ispunjene .docx dokumente iz polja koje sami unesete. "
        "Ako niste sigurni što vam treba, posavjetujte se s odvjetnikom "
        "(<a href='https://www.hok-cba.hr' target='_blank'>HOK Imenik</a>)."
        "</div>",
        unsafe_allow_html=True,
    )

    # --- Katalog kartice ---
    st.markdown("##### Pregled po pravnom području")

    cols = st.columns(2)
    for i, kat in enumerate(_VODIC_KATEGORIJE):
        boja = _TEZINA_BOJA.get(kat["tezina"], "#475569")
        with cols[i % 2]:
            st.markdown(
                f"<div class='module-card'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center;"
                f"margin-bottom:0.4rem;'>"
                f"<b style='color:#162D50;font-size:0.95rem;letter-spacing:-0.01em;'>"
                f"{kat['naslov']}</b>"
                f"<span style='background:{boja};color:white;padding:2px 8px;border-radius:4px;"
                f"font-size:0.6rem;font-weight:700;letter-spacing:0.03em;text-transform:uppercase;'>"
                f"{kat['tezina']}</span>"
                f"</div>"
                f"<p style='color:#3D4A5C;font-size:0.82rem;margin:0 !important;"
                f"line-height:1.5;'>{kat['opis']}</p>"
                f"<div style='display:flex;gap:0.4rem;margin-top:0.5rem;flex-wrap:wrap;'>"
                + "".join(
                    f"<span style='font-size:0.6rem;color:#8494A7;background:#F0F0EB;"
                    f"padding:1px 6px;border-radius:3px;'>{m}</span>"
                    for m in kat["moduli"]
                )
                + f"</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            if st.button(
                f"Otvori pregled →",
                key=f"_vk_{i}",
                use_container_width=True,
                type="primary",
            ):
                st.session_state._vodic_odabir = kat["naslov"]
                st.rerun()

    # --- Vodic detalji ---
    odabir = st.session_state.get("_vodic_odabir", "")
    if odabir and odabir in _VODIC_DETALJI:
        st.markdown("---")
        st.markdown("<div class='vodic-scroll-target'></div>", unsafe_allow_html=True)
        detalji = _VODIC_DETALJI[odabir]
        st.markdown(f"### Tipovi dokumenata: {odabir}")

        for naslov, opis in detalji["dokumenti"]:
            st.markdown(
                f"<div style='background:white;padding:1rem 1.2rem;border-radius:12px;"
                f"border-left:3px solid #162D50;margin-bottom:0.6rem;"
                f"box-shadow:0 2px 8px rgba(22,45,80,0.06);'>"
                f"<b style='color:#162D50;font-size:0.9rem;'>{naslov}</b><br>"
                f"<span style='color:#3D4A5C;font-size:0.85rem;line-height:1.6;'>{opis}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        # Gumbi za navigaciju
        kat_data = next((k for k in _VODIC_KATEGORIJE if k["naslov"] == odabir), None)
        if kat_data:
            btn_cols = st.columns(len(kat_data["moduli"]))
            for col, modul in zip(btn_cols, kat_data["moduli"]):
                with col:
                    if st.button(f"Otvori: {modul}", key=f"_vn_{modul}", type="primary", use_container_width=True):
                        _navigate_to(modul)
                        st.rerun()

        # Auto-scroll: samo kad se odabir upravo promijenio
        _prev_odabir = st.session_state.get("_vodic_odabir_prev", "")
        if _prev_odabir != odabir:
            _scroll_to_element('.vodic-scroll-target')
        st.session_state["_vodic_odabir_prev"] = odabir

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
        ("Zaštita potrošača", "Reklamacija, raskid"),
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

# Jednostavni mod — prikaži render_jednostavno umjesto standardne navigacije
if st.session_state.get("_app_mode") == "jednostavno":
    # Autoscroll na vrh pri promjeni odabira u jednostavnom modu
    _prev_jed = st.session_state.get("_prev_jed_odabir", None)
    _curr_jed = st.session_state.get("_jed_odabir", None)
    if _prev_jed != _curr_jed:
        _scroll_to_top()
    st.session_state._prev_jed_odabir = _curr_jed
    render_jednostavno(navigate_fn=_navigate_to)
else:
    active = st.session_state._active_module

    # Scroll na vrh kad se modul promijeni (ili pri prvom ulasku u napredno)
    _prev_module = st.session_state.get("_prev_module", None)
    if _prev_module != active:
        _scroll_to_top()
    st.session_state._prev_module = active

    # DOCX opcije - samo za generatore dokumenata
    modul_cfg = _MODULI.get(active, {})
    if modul_cfg.get("docx", False):
        docx_opcije()

    # Routing
    if active == "Početna":
        _render_pocetna()
    elif active in _MODULI and _MODULI[active]["render"]:
        _MODULI[active]["render"]()
    else:
        st.warning(f"Modul '{active}' nije pronaden.")
        st.session_state._active_module = "Početna"
        st.rerun()
