# =============================================================================
# TESTS/TEST_GDPR_OBAVIJEST.PY
# =============================================================================
# Clanak 13. Opce uredbe trazi obavijest U TRENUTKU prikupljanja. Politika
# privatnosti kao zasebna stavka izbornika to ne ispunjava.
#
# Najvazniji test ovdje nije onaj koji provjerava tekst, nego
# `test_svaka_stranica_s_unosom_ima_obavijest`: on iz izvornog koda otkriva
# koje stranice imaju polje za unos i trazi da svaka od njih zove
# `prikazi_obavijest_o_obradi`. Nova stranica s unosom pada na tom testu i
# prije nego je itko pogleda; popis stranica se nigdje ne odrzava rucno, pa
# ne moze zastarjeti.

import ast
import io
import os

import pytest

import privatnost


KORIJEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_STRANICE = os.path.join(KORIJEN, "stranice")

FUNKCIJA = "prikazi_obavijest_o_obradi"

# Streamlit widgeti kroz koje korisnik moze upisati ime, OIB, adresu, podatke o
# predmetu ili prilozenu datoteku. Broj, datum i padajuci izbornik nisu ovdje:
# oni sami po sebi ne nose osobni podatak (kalkulatori kamata i pristojbi).
WIDGETI_UNOSA = {
    "text_input",
    "text_area",
    "file_uploader",
    "chat_input",
    "camera_input",
}

# Datoteke koje se pregledavaju: sve stranice plus prijavna stranica, jer se i
# na njoj (registracija) prikupljaju osobni podaci.
def _datoteke_za_pregled():
    putevi = []
    for ime in sorted(os.listdir(DIR_STRANICE)):
        if ime.endswith(".py") and ime != "__init__.py":
            putevi.append(os.path.join(DIR_STRANICE, ime))
    putevi.append(os.path.join(KORIJEN, "auth.py"))
    return putevi


def _izvor(put):
    with io.open(put, "r", encoding="utf-8") as f:
        return f.read()


def _ima_widget(cvor):
    """Otvara li tijelo ovog cvora polje za slobodan unos."""
    for pod in ast.walk(cvor):
        if not isinstance(pod, ast.Call):
            continue
        fn = pod.func
        if isinstance(fn, ast.Attribute) and fn.attr in WIDGETI_UNOSA:
            return True
    return False


def _izvedi_helpere_unosa():
    """Imena funkcija iz modula u korijenu koje iznutra otvaraju polja za unos.

    Popis se NE odrzava rucno. Rucni popis je vec jednom bio nepotpun: sadrzavao
    je cetiri imena iz `pomocne.py`, a `odabir_suda` (koji ima rucni unos naziva
    suda) nije bio na njemu, kao ni bilo koja buduca pomocna funkcija u drugom
    modulu. Ovdje se skup racuna iz izvornog koda i zatvara do fiksne tocke, pa
    ulazi i `unos_vise_stranaka`, koja sama nema widget nego zove `unos_stranke`.
    """
    tijela = {}
    for ime in sorted(os.listdir(KORIJEN)):
        if not ime.endswith(".py"):
            continue
        try:
            stablo = ast.parse(_izvor(os.path.join(KORIJEN, ime)))
        except (SyntaxError, UnicodeDecodeError):
            continue
        for cvor in ast.walk(stablo):
            if isinstance(cvor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                tijela[cvor.name] = cvor

    helperi = {ime for ime, cvor in tijela.items() if _ima_widget(cvor)}
    # Fiksna tocka: funkcija koja zove helper i sama je helper.
    promjena = True
    while promjena:
        promjena = False
        for ime, cvor in tijela.items():
            if ime in helperi:
                continue
            for pod in ast.walk(cvor):
                if not isinstance(pod, ast.Call):
                    continue
                fn = pod.func
                zvano = fn.id if isinstance(fn, ast.Name) else getattr(fn, "attr", None)
                if zvano in helperi:
                    helperi.add(ime)
                    promjena = True
                    break
    return helperi


HELPERI_UNOSA = _izvedi_helpere_unosa()


def _prikuplja_podatke(stablo):
    """Ima li datoteka polje kroz koje korisnik upisuje podatke.

    Poziv helpera hvata se u oba oblika: `unos_stranke(...)` i
    `pomocne.unos_stranke(...)`. Raniji detektor je prepoznavao samo prvi, pa je
    stranica koja unos radi preko `pomocne.` prefiksa prolazila kao da nema
    polja za unos (test se tiho preskakao).
    """
    for cvor in ast.walk(stablo):
        if not isinstance(cvor, ast.Call):
            continue
        fn = cvor.func
        if isinstance(fn, ast.Attribute):
            if fn.attr in WIDGETI_UNOSA or fn.attr in HELPERI_UNOSA:
                return True
        if isinstance(fn, ast.Name) and fn.id in HELPERI_UNOSA:
            return True
    return False


def _pozivi_obavijesti(stablo):
    """Vrati listu (kontekst, ime_funkcije_u_kojoj_je_poziv) za svaki poziv.

    `kontekst` je None ako nije naveden kao literal (tada se ne moze provjeriti
    da je valjan, pa test to tretira kao gresku).
    """
    nadredena = {}
    for cvor in ast.walk(stablo):
        if isinstance(cvor, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for dijete in ast.walk(cvor):
                nadredena.setdefault(id(dijete), cvor.name)

    nadeni = []
    for cvor in ast.walk(stablo):
        if not isinstance(cvor, ast.Call):
            continue
        fn = cvor.func
        ime = fn.id if isinstance(fn, ast.Name) else getattr(fn, "attr", None)
        if ime != FUNKCIJA:
            continue
        kontekst = None
        if cvor.args and isinstance(cvor.args[0], ast.Constant):
            kontekst = cvor.args[0].value
        for kw in cvor.keywords:
            if kw.arg == "kontekst" and isinstance(kw.value, ast.Constant):
                kontekst = kw.value.value
        nadeni.append((kontekst, nadredena.get(id(cvor))))
    return nadeni


_PUTEVI = _datoteke_za_pregled()
_IMENA = [os.path.relpath(p, KORIJEN) for p in _PUTEVI]


# =============================================================================
# GLAVNI TEST: obavijest na svakom mjestu prikupljanja
# =============================================================================

@pytest.mark.parametrize("put", _PUTEVI, ids=_IMENA)
def test_svaka_stranica_s_unosom_ima_obavijest(put):
    stablo = ast.parse(_izvor(put))
    ime = os.path.relpath(put, KORIJEN)

    if not _prikuplja_podatke(stablo):
        pytest.skip("nema polja za unos, obavijest se ne trazi")

    pozivi = _pozivi_obavijesti(stablo)
    assert pozivi, (
        "%s ima polje za unos osobnih podataka, ali ne zove %s(). "
        "GDPR cl. 13 trazi obavijest u trenutku prikupljanja, a ne samo "
        "postojanje politike privatnosti u izborniku." % (ime, FUNKCIJA)
    )


@pytest.mark.parametrize("put", _PUTEVI, ids=_IMENA)
def test_kontekst_obavijesti_postoji(put):
    stablo = ast.parse(_izvor(put))
    ime = os.path.relpath(put, KORIJEN)

    for kontekst, _ in _pozivi_obavijesti(stablo):
        assert kontekst is not None, (
            "%s zove %s bez konteksta kao doslovnog niza; tada se ne moze "
            "provjeriti da opis obrade odgovara stranici." % (ime, FUNKCIJA)
        )
        assert kontekst in privatnost.KONTEKSTI, (
            "%s trazi kontekst %r, koji ne postoji u privatnost.KONTEKSTI."
            % (ime, kontekst)
        )


@pytest.mark.parametrize("put", _PUTEVI, ids=_IMENA)
def test_obavijest_je_u_funkciji_koja_crta_stranicu(put):
    """Poziv mora biti u render funkciji (ili na prijavnoj stranici).

    Poziv izvan njih ne bi se izvrsio pri prikazu obrasca, pa bi test iz
    prethodne tocke prolazio a korisnik obavijest ne bi vidio.
    """
    stablo = ast.parse(_izvor(put))
    ime = os.path.relpath(put, KORIJEN)

    for _, funkcija in _pozivi_obavijesti(stablo):
        assert funkcija is not None, "%s: poziv %s je izvan funkcije" % (ime, FUNKCIJA)
        assert funkcija.startswith("render_") or funkcija == "login_stranica", (
            "%s: poziv %s je u funkciji %s, koja se ne izvodi pri prikazu "
            "stranice." % (ime, FUNKCIJA, funkcija)
        )


def test_detektor_hvata_novu_stranicu_bez_obavijesti():
    """Dokaz da gornji test doista pada na novoj stranici s unosom.

    Bez ovoga bi tiha greska u detekciji ucinila cijeli komplet beskorisnim:
    testovi bi prolazili jer nista ne bi bilo prepoznato kao prikupljanje.
    """
    nova_bez = ast.parse(
        "import streamlit as st\n"
        "def render_novo():\n"
        "    ime = st.text_input('Ime i prezime')\n"
    )
    assert _prikuplja_podatke(nova_bez) is True
    assert _pozivi_obavijesti(nova_bez) == []

    nova_preko_helpera = ast.parse(
        "from pomocne import unos_stranke\n"
        "def render_novo():\n"
        "    t, _, _ = unos_stranke('TUZITELJ', 't1')\n"
    )
    assert _prikuplja_podatke(nova_preko_helpera) is True

    nova_s_obavijesti = ast.parse(
        "import streamlit as st\n"
        "from privatnost import prikazi_obavijest_o_obradi\n"
        "def render_novo():\n"
        "    prikazi_obavijest_o_obradi('dokument')\n"
        "    ime = st.text_input('Ime i prezime')\n"
    )
    assert _pozivi_obavijesti(nova_s_obavijesti) == [("dokument", "render_novo")]

    kalkulator = ast.parse(
        "import streamlit as st\n"
        "def render_kamate():\n"
        "    iznos = st.number_input('Glavnica (EUR)')\n"
    )
    assert _prikuplja_podatke(kalkulator) is False


def test_detektor_hvata_helper_pozvan_preko_imena_modula():
    """Oba oblika poziva helpera moraju se hvatati.

    Prvi detektor je gledao samo `unos_stranke(...)` kao golo ime. Stranica
    napisana kao `import pomocne` pa `pomocne.unos_stranke(...)` prikuplja ime,
    OIB i adresu, a prolazila je kao datoteka bez polja za unos: glavni test se
    na njoj preskakao umjesto da padne.
    """
    preko_modula = ast.parse(
        "import pomocne\n"
        "def render_novo():\n"
        "    t = pomocne.unos_stranke('TUZITELJ', 't1')\n"
    )
    assert _prikuplja_podatke(preko_modula) is True
    assert _pozivi_obavijesti(preko_modula) == []

    kao_alias = ast.parse(
        "import pomocne as p\n"
        "def render_novo():\n"
        "    t = p.unos_vise_stranaka('TUZITELJI', 't')\n"
    )
    assert _prikuplja_podatke(kao_alias) is True


def test_popis_helpera_se_izvodi_iz_koda_a_ne_odrzava_rucno():
    """Skup helpera mora doci iz izvornog koda, i ne smije biti prazan.

    Prazan skup bi ucinio detekciju preko helpera nijemom, a da nijedan test ne
    padne. Cetiri imena ispod su ona koja su bila u ranijem rucnom popisu;
    `odabir_suda` je dokaz da izvedeni skup hvata i ono sto rucni nije.
    """
    for ime in ("unos_stranke", "unos_vise_stranaka", "unos_tocaka",
                "zaglavlje_sastavljaca", "odabir_suda"):
        assert ime in HELPERI_UNOSA, sorted(HELPERI_UNOSA)


def test_stranice_koje_prikupljaju_nisu_prazan_skup():
    """Zastita od suprotne tihe greske: da detektor ne prepozna nista."""
    prikupljaju = [
        os.path.basename(p)
        for p in _PUTEVI
        if _prikuplja_podatke(ast.parse(_izvor(p)))
    ]
    # Utvrdjeno citanjem koda: 18 stranica s generatorima dokumenata, kalendar,
    # pretraga Narodnih novina i prijavna stranica.
    assert len(prikupljaju) >= 21, prikupljaju
    for ocekivana in ("tuzbe.py", "kazneno.py", "kalendar.py", "auth.py"):
        assert ocekivana in prikupljaju


# =============================================================================
# SADRZAJ OBAVIJESTI
# =============================================================================

@pytest.mark.parametrize("kontekst", sorted(privatnost.KONTEKSTI))
def test_obavijest_ima_svih_pet_elemenata(kontekst):
    tekst = privatnost.tekst_obavijesti(kontekst)
    assert "Tko obrađuje" in tekst
    assert "Što se prikuplja" in tekst
    assert "Svrha" in tekst
    assert "Osnova" in tekst
    assert "čl. 6." in tekst
    assert "Koliko se čuva" in tekst
    assert "Vaša prava" in tekst
    assert "azop.hr" in tekst


@pytest.mark.parametrize("kontekst", sorted(privatnost.KONTEKSTI))
def test_voditelj_obrade_nije_izmisljen(kontekst):
    """Voditelj obrade nije poznat ni u politici, pa se ne smije imenovati."""
    tekst = privatnost.tekst_obavijesti(kontekst)
    assert privatnost.VODITELJ_PLACEHOLDER in tekst


def test_oznaka_je_ista_kao_u_politici():
    assert privatnost.VODITELJ_PLACEHOLDER.startswith("<<< VLASNIK UPISUJE:")
    assert privatnost.VODITELJ_PLACEHOLDER.endswith(">>>")
    politika = _izvor(os.path.join(DIR_STRANICE, "privacy_policy.md"))
    assert "<<< VLASNIK UPISUJE:" in politika


@pytest.mark.parametrize(
    "kontekst,ocekivano",
    [
        # Sadrzaj obrasca se ne pohranjuje (docx_export gradi datoteku u
        # memoriji), pa roka nema jer nema ni pohrane.
        ("dokument", "ne čuva se"),
        # Kalendar i racun se pisu u datoteku, automatskog brisanja u kodu
        # nema, rok nije nigdje odreden. To se mora reci, a ne izmisliti.
        ("kalendar", "rok čuvanja nije utvrđen"),
        ("racun", "rok čuvanja nije utvrđen"),
        # Upit se salje vanjskoj usluzi i drzi u meduspremniku; u aplikaciji se
        # ne pohranjuje.
        ("pretraga", "ne zapisuje"),
    ],
)
def test_rok_cuvanja_nije_izmisljen(kontekst, ocekivano):
    assert ocekivano in privatnost.tekst_obavijesti(kontekst)


def test_nema_tvrdnje_o_automatskom_brisanju():
    """U kodu ne postoji nijedan posao koji sam brise podatke.

    Politika je jednom vec javno tvrdila brisanje koje se ne provodi
    (`stranice/privacy_policy.md`, uvod). Obavijest tu gresku ne smije ponoviti.
    """
    for kontekst in privatnost.KONTEKSTI:
        tekst = privatnost.tekst_obavijesti(kontekst)
        assert "automatski briše" not in tekst
        assert "automatski se briše" not in tekst


def test_nepoznat_kontekst_puca_umjesto_da_prikaze_pogresan_tekst():
    with pytest.raises(KeyError):
        privatnost.tekst_obavijesti("nepostojeci")


# =============================================================================
# NACIN PRIKAZA
# =============================================================================

def test_obavijest_je_sklopiva_a_ne_modalna():
    """Zahtjev: ne smije zaklanjati posao ni traziti zatvaranje pri svakom koraku."""
    izvor = _izvor(os.path.join(KORIJEN, "privatnost.py"))
    assert "st.expander(" in izvor
    assert "expanded=False" in izvor
    assert "st.dialog" not in izvor
    assert "st.modal" not in izvor


def test_poveznica_vodi_na_modul_koji_postoji():
    """Ako se stavka izbornika preimenuje, gumb vodi u prazno."""
    app = _izvor(os.path.join(KORIJEN, "LEGAL-SUITE.py"))
    assert '"%s"' % privatnost.MODUL_POLITIKA in app


# =============================================================================
# PROVJERA NA POKRENUTOJ APLIKACIJI
# =============================================================================
# Testovi iznad citaju izvorni kod. Ovaj pokrece aplikaciju i gleda sto je na
# ekranu, jer poziv u kodu i prikaz na stranici nisu isto: poziv u grani koja
# se ne izvodi prosao bi staticku provjeru.

def _pokreni(modul, prijavljen=True):
    AppTest = pytest.importorskip("streamlit.testing.v1").AppTest
    at = AppTest.from_file(os.path.join(KORIJEN, "LEGAL-SUITE.py"), default_timeout=60)
    at.session_state["_app_mode"] = "napredno"
    if prijavljen:
        at.session_state["_authenticated"] = True
        at.session_state["_user"] = {
            "email": "gost@legalsuite.hr",
            "name": "Gost",
            "role": "guest",
            "provider": "guest",
        }
        at.session_state["_active_module"] = modul
    at.run()
    assert not at.exception, at.exception
    return [e.label for e in at.get("expander")]


@pytest.mark.parametrize(
    "modul,ocekivani_naslov",
    [
        ("Tužbe", privatnost.KONTEKSTI["dokument"]["naslov"]),
        ("Kazneno pravo", privatnost.KONTEKSTI["dokument"]["naslov"]),
        ("Kalendar", privatnost.KONTEKSTI["kalendar"]["naslov"]),
        ("Propisi", privatnost.KONTEKSTI["pretraga"]["naslov"]),
    ],
)
def test_obavijest_je_vidljiva_u_aplikaciji(modul, ocekivani_naslov):
    assert ocekivani_naslov in _pokreni(modul)


def test_obavijest_je_vidljiva_na_prijavnoj_stranici():
    naslovi = _pokreni(None, prijavljen=False)
    assert privatnost.KONTEKSTI["racun"]["naslov"] in naslovi


def test_obavijest_se_ne_prikazuje_gdje_nema_prikupljanja():
    """Kontrola smisla: da obavijest ne dolazi sama od sebe na svaku stranicu.

    Bez ovoga bi gornji testovi prolazili i da je obavijest zalijepljena
    globalno, pa ne bi dokazivali nista o pojedinoj stranici.
    """
    naslovi = _pokreni("Kamate")
    for kontekst in privatnost.KONTEKSTI.values():
        assert kontekst["naslov"] not in naslovi
