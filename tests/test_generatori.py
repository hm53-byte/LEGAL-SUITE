# -----------------------------------------------------------------------------
# UNIT TESTOVI: Generatori - provjera da svaki generator vraca validan HTML
# Pokretanje: python -m pytest tests/test_generatori.py -v
# -----------------------------------------------------------------------------
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# --- Pomocne konstante za testove ---
STRANKA = "<b>Test Stranka</b><br>Adresa: Test 1<br>OIB: 12345678901"
STRANKA2 = "<b>Test Stranka 2</b><br>Adresa: Test 2<br>OIB: 98765432109"
PODACI_MIN = {}  # minimalni podaci


def _assert_valid_html(result):
    """Provjera da generator vraca validan HTML string."""
    assert isinstance(result, str), f"Rezultat nije string: {type(result)}"
    assert len(result) > 50, "Rezultat prekratak - vjerovatno greska"
    assert "<div" in result or "<b>" in result or "<table" in result, "Nema HTML tagova"


# =============================================================================
# TUZBE
# =============================================================================

class TestTuzbe:
    def test_tuzba_pro(self):
        from generatori.tuzbe import generiraj_tuzbu_pro
        result = generiraj_tuzbu_pro(
            "SUD", "", STRANKA, STRANKA2, 5000.0, "Isplate",
            {'cinjenice': 'Test', 'dokazi': 'Dokaz', 'datum_dospijeca': '01.01.2025.'},
            {'stavka': 100, 'pdv': 25, 'pristojba': 80},
        )
        _assert_valid_html(result)

    def test_brisovna_tuzba(self):
        from generatori.tuzbe import generiraj_brisovnu_tuzbu
        result = generiraj_brisovnu_tuzbu(
            "SUD", "", STRANKA, STRANKA2,
            {'ko': 'Zagreb', 'cestica': '1234', 'ulozak': '100'},
            {'razlog': 'Test', 'pravni_temelj': 'Zakon'},
            {'stavka': 100, 'pdv': 25, 'pristojba': 80},
        )
        _assert_valid_html(result)


# =============================================================================
# OVRHE
# =============================================================================

class TestOvrhe:
    def test_ovrha_pro(self):
        from generatori.ovrhe import generiraj_ovrhu_pro
        result = generiraj_ovrhu_pro(
            "FINA", STRANKA, STRANKA2, 1000.0, "Racun 1/2025",
            {'stavka': 50, 'pdv': 0, 'pristojba': 7},
        )
        _assert_valid_html(result)

    def test_prigovor_ovrhe(self):
        from generatori.ovrhe import generiraj_prigovor_ovrhe
        result = generiraj_prigovor_ovrhe(
            "SUD", STRANKA, STRANKA2,
            {'broj_rjesenja': 'Ovr-1/2025', 'datum_rjesenja': '01.01.2025.', 'razlozi': 'Test'},
            {'stavka': 50, 'pdv': 0, 'pristojba': 0},
        )
        _assert_valid_html(result)

    def test_ovrha_ovrsna_isprava(self):
        from generatori.ovrhe import generiraj_ovrhu_ovrsna_isprava
        result = generiraj_ovrhu_ovrsna_isprava(
            "SUD", STRANKA, STRANKA2,
            {'iznos': 5000, 'ovrsna_isprava': 'Presuda', 'datum_isprave': '01.01.2025.',
             'sredstvo_ovrhe': 'nekretnina', 'opis_sredstva': 'Stan'},
            {'stavka': 100, 'pdv': 25, 'pristojba': 50},
        )
        _assert_valid_html(result)


# =============================================================================
# ZALBE
# =============================================================================

class TestZalbe:
    def test_zalba_pro(self):
        from generatori.zalbe import generiraj_zalbu_pro
        result = generiraj_zalbu_pro(
            "Sud prvi", "Sud drugi",
            {'tuzitelj': 'A', 'tuzenik': 'B'},
            {'broj': 'P-1/25', 'datum': '01.01.2025.', 'opseg': 'u cijelosti', 'mjesto': 'Zagreb'},
            ['Razlog 1'], 'Obrazlozenje tekst',
            {'stavka': 0, 'pdv': 0, 'pristojba': 0},
        )
        _assert_valid_html(result)


# =============================================================================
# UGOVORI
# =============================================================================

class TestUgovori:
    def test_prilagodeni(self):
        from generatori.ugovori import generiraj_prilagodeni_ugovor
        result = generiraj_prilagodeni_ugovor(
            "Test Ugovor", "Zagreb", "01.01.2025.", "1 godina",
            STRANKA, STRANKA2, "001/25",
            [{'naslov': 'Cl. 1', 'sadrzaj': 'Tekst'}],
        )
        _assert_valid_html(result)

    def test_ugovor_o_radu(self):
        from generatori.ugovori import generiraj_ugovor_o_radu
        result = generiraj_ugovor_o_radu(
            STRANKA, STRANKA2,
            {'radno_mjesto': 'Developer', 'placa': 2000, 'pocetak_rada': '01.01.2025.',
             'trajanje': 'neodredeno', 'mjesto_rada': 'Zagreb', 'radno_vrijeme': 'puno'},
        )
        _assert_valid_html(result)

    def test_otkaz(self):
        from generatori.ugovori import generiraj_otkaz
        result = generiraj_otkaz(
            STRANKA, STRANKA2,
            {'vrsta_otkaza': 'redoviti', 'razlog': 'Test', 'otkazni_rok': '30 dana',
             'datum_otkaza': '01.01.2025.'},
        )
        _assert_valid_html(result)


# =============================================================================
# OPOMENE I PUNOMOCI
# =============================================================================

class TestOpomenePunomoci:
    def test_opomena(self):
        from generatori.opomene import generiraj_opomenu
        result = generiraj_opomenu(
            "pred_tuzbu", STRANKA, STRANKA2, 1000.0,
            {'opis_trazbine': 'Racun 1/2025', 'rok_dana': 8, 'mjesto': 'Zagreb'},
        )
        _assert_valid_html(result)

    def test_punomoc(self):
        from generatori.punomoci import generiraj_punomoc
        result = generiraj_punomoc(
            "opca", STRANKA, STRANKA2,
            {'sud': 'SUD', 'opis_spora': 'Test', 'mjesto': 'Zagreb'},
        )
        _assert_valid_html(result)


# =============================================================================
# ZEMLJISNE KNJIGE
# =============================================================================

class TestZemljisne:
    def test_tabularna(self):
        from generatori.zemljisne import generiraj_tabularnu_doc
        result = generiraj_tabularnu_doc(
            STRANKA, STRANKA2, "Zagreb", "1234", "100", "Stan", "01.01.2025."
        )
        _assert_valid_html(result)

    def test_zk_prijedlog(self):
        from generatori.zemljisne import generiraj_zk_prijedlog
        result = generiraj_zk_prijedlog(
            "SUD", STRANKA, STRANKA2,
            {'ko': 'Zagreb', 'cestica': '1234', 'ulozak': '100'},
            ['Ugovor'], {'stavka': 50, 'pdv': 0, 'pristojba': 33},
        )
        _assert_valid_html(result)


# =============================================================================
# TRGOVACKO PRAVO
# =============================================================================

class TestTrgovacko:
    def test_drustveni_ugovor(self):
        from generatori.trgovacko import generiraj_drustveni_ugovor
        result = generiraj_drustveni_ugovor(
            [{'html': STRANKA, 'udjel': 100, 'ulog': 2500}],
            {'naziv_drustva': 'Test d.o.o.', 'sjediste': 'Zagreb', 'temeljni_kapital': 2500,
             'djelatnosti': 'IT', 'zastupanje': 'Direktor'},
        )
        _assert_valid_html(result)

    def test_nda(self):
        from generatori.trgovacko import generiraj_nda
        result = generiraj_nda(
            STRANKA, STRANKA2,
            {'predmet': 'Poslovne informacije', 'trajanje': '2 godine',
             'ugovorna_kazna': 10000, 'mjesto': 'Zagreb'},
        )
        _assert_valid_html(result)


# =============================================================================
# OBVEZNO PRAVO
# =============================================================================

class TestObvezno:
    def test_darovanje(self):
        from generatori.obvezno import generiraj_darovanje
        result = generiraj_darovanje(
            STRANKA, STRANKA2,
            {'predmet_tip': 'pokretnina_s_predajom', 'predmet_opis': 'Auto',
             'vrijednost': 5000, 'dozivotno_uzivanje': False, 'mjesto': 'Zagreb'},
        )
        _assert_valid_html(result)

    def test_cesija(self):
        from generatori.obvezno import generiraj_cesiju
        result = generiraj_cesiju(
            STRANKA, STRANKA2,
            {'iznos_trazbine': 1000, 'opis_trazbine': 'Dug', 'duznik_naziv': 'Duznik',
             'pravni_temelj': 'Ugovor', 'jamstvo_veritet': True, 'jamstvo_bonitet': False,
             'notifikacija_duznika': True, 'naknada': 900, 'mjesto': 'Zagreb'},
        )
        _assert_valid_html(result)


# =============================================================================
# OBITELJSKO PRAVO
# =============================================================================

class TestObiteljsko:
    def test_sporazum_razvod(self):
        from generatori.obiteljsko import generiraj_sporazum_razvod
        result = generiraj_sporazum_razvod(
            STRANKA, STRANKA2,
            {'mjesto': 'SUD', 'datum_braka': '01.01.2010.', 'mjesto_braka': 'Zagreb',
             'djeca': [], 'ima_savjetovanje': True,
             'plan_roditeljske_skrbi': '', 'petitum': 'Razvod'},
        )
        _assert_valid_html(result)

    def test_bracni_ugovor(self):
        from generatori.obiteljsko import generiraj_bracni_ugovor
        result = generiraj_bracni_ugovor(
            STRANKA, STRANKA2,
            {'mjesto': 'Zagreb', 'vrsta': 'bracni',
             'imovina_items': [{'opis': 'Stan', 'vrsta': 'nekretnina',
                                'vlasnik': 'Zajedničko', 'zk_podaci': {}}],
             'clausula_intabulandi': True},
        )
        _assert_valid_html(result)


# =============================================================================
# UPRAVNO PRAVO
# =============================================================================

class TestUpravno:
    def test_zalba_zup(self):
        from generatori.upravno import generiraj_zalbu_zup
        result = generiraj_zalbu_zup(
            STRANKA,
            {'prvostupanjsko_tijelo': 'Grad Zagreb', 'drugostupanjsko_tijelo': 'Ministarstvo',
             'klasa_rjesenja': 'UP/I-123/25', 'urbroj_rjesenja': '123-01-25-1',
             'datum_rjesenja': '01.01.2025.', 'datum_primitka': '05.01.2025.',
             'razlozi': 'Test', 'zahtjev': 'Ponistiti', 'mjesto': 'Zagreb'},
        )
        _assert_valid_html(result)

    def test_zahtjev_informacije(self):
        from generatori.upravno import generiraj_zahtjev_informacije
        result = generiraj_zahtjev_informacije(
            STRANKA,
            {'tijelo': 'Grad Zagreb', 'informacije_opis': 'Podaci',
             'nacin_pristupa': 'email', 'pravni_interes': '', 'mjesto': 'Zagreb'},
        )
        _assert_valid_html(result)


# =============================================================================
# KAZNENO PRAVO
# =============================================================================

class TestKazneno:
    def test_kaznena_prijava(self):
        from generatori.kazneno import generiraj_kaznenu_prijavu
        result = generiraj_kaznenu_prijavu(
            STRANKA,
            {'sud': 'SUD', 'prijavljenik': 'Osumnjiceni',
             'kazneno_djelo': 'Prijevara', 'opis_djela': 'Test opis',
             'dokazi': ['Dokaz 1'], 'mjesto': 'Zagreb'},
        )
        _assert_valid_html(result)


# =============================================================================
# STECAJNO PRAVO
# =============================================================================

class TestStecajno:
    def test_prijedlog_stecaj(self):
        from generatori.stecajno import generiraj_prijedlog_stecaj
        result = generiraj_prijedlog_stecaj(
            STRANKA, STRANKA2,
            {'sud': 'SUD', 'razlog': 'Nelikvidnost', 'trazbina_iznos': 50000,
             'trazbina_opis': 'Neplaceni racuni', 'dokazi': ['Racun'],
             'mjesto': 'Zagreb'},
            {'stavka': 100, 'pdv': 25, 'pristojba': 0},
        )
        _assert_valid_html(result)


# =============================================================================
# POTROSACI
# =============================================================================

class TestPotrosaci:
    def test_reklamacija(self):
        from generatori.potrosaci import generiraj_reklamaciju
        result = generiraj_reklamaciju(
            STRANKA,
            {'trgovac': 'Trgovac d.o.o.', 'proizvod': 'Laptop', 'datum_kupnje': '01.01.2025.',
             'opis_nedostatka': 'Ne radi', 'zahtjev': 'zamjena', 'mjesto': 'Zagreb',
             'broj_racuna': 'R-1/25'},
        )
        _assert_valid_html(result)

    def test_prijava_inspekciji(self):
        from generatori.potrosaci import generiraj_prijavu_inspekciji
        result = generiraj_prijavu_inspekciji(
            STRANKA,
            {'inspekcija': 'Trzisna inspekcija', 'prijavljenik': 'Trgovac',
             'opis_krsenja': 'Lazno oglasavanje', 'dokazi': ['Screenshot'],
             'mjesto': 'Zagreb'},
        )
        _assert_valid_html(result)
