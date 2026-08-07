# -----------------------------------------------------------------------------
# UNIT TESTOVI: Generatori dodani u Fazi 1-3 (nautika, apartmani, pokretnine,
# zemljisne ext, obvezno ext, potrosaci ext, trgovacko ext)
# Pokretanje: python -m pytest tests/test_generatori_novi.py -v
# -----------------------------------------------------------------------------
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


STRANKA = "<b>IVAN HORVAT</b><br>OIB: 12345678901<br>Ilica 1, Zagreb"
STRANKA2 = "<b>MARKO MARIĆ</b><br>OIB: 98765432109<br>Splitska 2, Split"


def _assert_valid_html(result):
    """Provjera da generator vraca validan HTML string."""
    assert isinstance(result, str), f"Rezultat nije string: {type(result)}"
    assert len(result) > 50, f"Rezultat prekratak ({len(result)} chars) - vjerovatno greska"
    assert "<div" in result or "<table" in result, "Nema HTML tagova"
    assert "Greška pri generiranju" not in result, "Generator je vratio gresku"


# =============================================================================
# FAZA 1A — NAUTIKA
# =============================================================================

class TestNautika:
    BRODICA = {
        'naziv_brodice': 'Galeb',
        'registracijska_oznaka': 'RI-1234',
        'luka_upisa': 'Rijeka',
        'lucka_kapetanija': 'Lučka kapetanija Rijeka',
        'proizvodjac': 'Bénéteau',
        'model': 'Antares 8',
        'godina_proizvodnje': '2018',
        'duljina_m': '7,80',
        'motor': 'Mercury Verado 200',
        'snaga_kw': '147',
        'serijski_broj_trupa': 'BAH12345D818',
        'mjesto': 'Rijeka',
    }

    def test_kupoprodaja_brodice(self):
        from generatori.nautika import generiraj_kupoprodaju_brodice
        podaci = {**self.BRODICA, 'cijena_eur': 75000.0,
                  'rok_predaje': '8 dana', 'tereti': 'bez tereta',
                  'nacin_placanja': 'jednokratno'}
        result = generiraj_kupoprodaju_brodice(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "UGOVOR O KUPOPRODAJI BRODICE" in result
        assert "75.000,00 EUR" in result
        assert "Galeb" in result
        assert "Pomorski" in result or "Lučka kapetanija" in result

    def test_tabularna_brodice(self):
        from generatori.nautika import generiraj_tabularnu_brodice
        podaci = {**self.BRODICA, 'datum_ugovora': '01.05.2026.'}
        result = generiraj_tabularnu_brodice(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "TABULARNA IZJAVA" in result
        assert "Clausula Intabulandi" in result
        assert "01.05.2026." in result
        assert "Galeb" in result

    def test_punomoc_prodaje_brodice(self):
        from generatori.nautika import generiraj_punomoc_prodaje_brodice
        podaci = {**self.BRODICA, 'minimalna_cijena_eur': 65000.0,
                  'rok_vazenja': '12 mjeseci'}
        result = generiraj_punomoc_prodaje_brodice(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "SPECIJALNA PUNOMOĆ" in result
        assert "65.000,00 EUR" in result
        assert "Galeb" in result

    def test_zalog_brodice(self):
        from generatori.nautika import generiraj_zalog_brodice
        podaci = {**self.BRODICA, 'iznos_trazbine_eur': 50000.0,
                  'kamatna_stopa': 'zakonska zatezna',
                  'rok_dospijeca': '31.12.2027.',
                  'osnova_trazbine': 'Ugovor o zajmu'}
        result = generiraj_zalog_brodice(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "ZALOŽNOG PRAVA" in result
        assert "50.000,00 EUR" in result
        assert "Upisnik brodica" in result


# =============================================================================
# FAZA 1B — APARTMANI
# =============================================================================

class TestApartmani:
    NEKRETNINA = {
        'adresa': 'Ilica 100, 10000 Zagreb',
        'kat_opis': '1. kat, stan 4',
        'povrsina_m2': '65',
        'ko': 'Centar', 'cestica': '1234/5', 'ulozak': '5678',
        'mjesto': 'Zagreb',
    }

    def test_suglasnost_obitelji(self):
        from generatori.apartmani import generiraj_suglasnost_obitelji
        podaci = {**self.NEKRETNINA, 'srodstvo': 'sin', 'rok_vazenja': 'do opoziva',
                  'broj_smjestajnih_jedinica': '2'}
        result = generiraj_suglasnost_obitelji(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "SUGLASNOST" in result
        assert "sin" in result
        assert "minimalnih tehničkih uvjeta" in result or "MTU" in result
        assert "kategorizacij" in result.lower()

    def test_suglasnost_suvlasnika(self):
        from generatori.apartmani import generiraj_suglasnost_suvlasnika
        podaci = {**self.NEKRETNINA}
        suvl = "IVAN HORVAT, OIB: 12345678901<br>MARIJA HORVAT, OIB: 98765432109"
        result = generiraj_suglasnost_suvlasnika(suvl, STRANKA, podaci)
        _assert_valid_html(result)
        assert "SUVLASNIKA" in result
        assert "PREDLAGATELJ" in result
        assert "MTU" in result or "minimalnih tehničkih uvjeta" in result

    def test_zahtjev_mtu(self):
        from generatori.apartmani import generiraj_zahtjev_mtu
        podaci = {**self.NEKRETNINA, 'vrsta_objekta': 'Apartman',
                  'broj_smjestajnih_jedinica': '2', 'broj_kreveta': '4',
                  'zupanija': 'Primorsko-goranska'}
        result = generiraj_zahtjev_mtu(STRANKA, podaci)
        _assert_valid_html(result)
        assert "minimalnih tehničkih uvjeta" in result or "MTU" in result
        assert "9/16" in result
        assert "Apartman" in result

    def test_zahtjev_kategorizacija(self):
        from generatori.apartmani import generiraj_zahtjev_kategorizacija
        podaci = {**self.NEKRETNINA, 'vrsta_objekta': 'Apartman',
                  'zatrazena_kategorija': '4★', 'broj_smjestajnih_jedinica': '2',
                  'broj_kreveta': '4', 'mtu_klasa': 'UP/I-335-02/26-01/123',
                  'mtu_datum': '15.03.2026.', 'opremljenost': 'kuhinja, klima, WiFi',
                  'zupanija': 'Primorsko-goranska'}
        result = generiraj_zahtjev_kategorizacija(STRANKA, podaci)
        _assert_valid_html(result)
        assert "kategorizacij" in result.lower()
        assert "56/16" in result
        assert "4★" in result
        assert "UP/I-335-02/26-01/123" in result


# =============================================================================
# FAZA 2A — ZEMLJISNE EXT
# =============================================================================

class TestZemljisneExt:
    NEKRETNINA = {
        'ko': 'Centar', 'ulozak': '5678', 'cestica': '1234/5',
        'opis_nekretnine': 'stan površine 65 m²',
    }

    def test_brisovno_ocitovanje(self):
        from generatori.zemljisne import generiraj_brisovno_ocitovanje
        podaci = {**self.NEKRETNINA,
                  'z_broj': 'Z-1234/2018', 'datum_upisa': '15.06.2018.',
                  'iznos_trazbine': '100.000,00 EUR',
                  'razlog_prestanka': 'isplate cjelokupne tražbine',
                  'mjesto': 'Zagreb'}
        result = generiraj_brisovno_ocitovanje(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "BRISOVNO OČITOVANJE" in result
        assert "Clausula Intabulandi" in result
        assert "isplate cjelokupne" in result
        assert "Z-1234/2018" in result

    def test_brisovno_ocitovanje_bez_z_broja(self):
        """Provjera fallback default upisa kad nema z_broj/datum/iznos."""
        from generatori.zemljisne import generiraj_brisovno_ocitovanje
        podaci = {**self.NEKRETNINA, 'mjesto': 'Zagreb'}
        result = generiraj_brisovno_ocitovanje(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "Centar" in result
        assert "5678" in result
        assert "Teretovnicu" in result

    def test_upis_plodouzivanja(self):
        from generatori.zemljisne import generiraj_upis_plodouzivanja
        podaci = {**self.NEKRETNINA,
                  'opseg': 'puno plodouživanje',
                  'pravni_temelj': 'Ugovor o osnivanju plodouživanja od 01.05.2026.',
                  'naknada': 'bez naknade',
                  'trajanje': 'doživotno',
                  'mjesto': 'Zagreb'}
        result = generiraj_upis_plodouzivanja(
            "Općinski sud u Zagrebu", STRANKA, STRANKA2, podaci, {'pristojba': 200.0}
        )
        _assert_valid_html(result)
        assert "PLODOUŽIVANJA" in result
        assert "199. — 213." in result or "199-213" in result or "199" in result
        assert "doživotno" in result
        assert "OPĆINSKI SUD" in result.upper()

    def test_punomoc_prodaje_nekretnine(self):
        from generatori.zemljisne import generiraj_punomoc_prodaje_nekretnine
        podaci = {**self.NEKRETNINA,
                  'adresa': 'Ilica 100, Zagreb', 'povrsina_m2': '65',
                  'minimalna_cijena_eur': 200000.0, 'rok_vazenja': '12 mjeseci',
                  'mjesto': 'Zagreb'}
        result = generiraj_punomoc_prodaje_nekretnine(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "SPECIJALNA PUNOMOĆ" in result
        assert "200.000,00 EUR" in result
        assert "Ilica 100" in result
        assert "Tabularnu izjavu" in result


# =============================================================================
# FAZA 2B — OBVEZNO EXT (predugovor + raskidi)
# =============================================================================

class TestObveznoExt:
    def test_predugovor(self):
        from generatori.obvezno import generiraj_predugovor
        podaci = {
            'vrsta_glavnog_ugovora': 'kupoprodajni ugovor',
            'predmet': 'Stan u Zagrebu, 65 m²',
            'cijena_eur': 200000.0, 'kapara_eur': 20000.0,
            'rok_sklapanja_glavnog': '01.07.2026.',
            'forma_glavnog': 'pisana s ovjerom',
            'mjesto': 'Zagreb',
        }
        result = generiraj_predugovor(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "PREDUGOVOR" in result
        assert "ZOO čl. 268" in result
        assert "200.000,00 EUR" in result
        assert "20.000,00 EUR" in result

    def test_raskid_najma_redoviti(self):
        from generatori.obvezno import generiraj_raskid_najma
        podaci = {
            'vrsta_raskida': 'redoviti',
            'ugovor_datum': '01.01.2025.',
            'adresa_najma': 'Ilica 50, Zagreb',
            'otkazni_rok': '30 dana',
            'datum_iseljenja': '15.05.2026.',
            'mjesto': 'Zagreb',
        }
        result = generiraj_raskid_najma(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "OTKAZ UGOVORA O NAJMU" in result
        assert "30 dana" in result
        assert "Ilica 50" in result

    def test_raskid_najma_izvanredni(self):
        from generatori.obvezno import generiraj_raskid_najma
        podaci = {
            'vrsta_raskida': 'izvanredni',
            'ugovor_datum': '01.01.2025.',
            'adresa_najma': 'Ilica 50, Zagreb',
            'razlog_izvanredni': 'Neplaćanje 3 mjeseca',
            'datum_iseljenja': '15.05.2026.',
            'zaostala_najamnina_eur': 1500.0,
            'mjesto': 'Zagreb',
        }
        result = generiraj_raskid_najma(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "IZVANREDNI RASKID" in result
        assert "1.500,00 EUR" in result
        assert "ZOO čl. 555" in result

    def test_raskid_ugovora_djelu(self):
        from generatori.obvezno import generiraj_raskid_ugovora_djelu
        podaci = {
            'ugovor_datum': '15.03.2026.',
            'opis_djela': 'Izrada drvene terase',
            'razlog_raskida': 'Promjena okolnosti',
            'ponuda_naknade_eur': 800.0,
            'mjesto': 'Zagreb',
        }
        result = generiraj_raskid_ugovora_djelu(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "RASKID UGOVORA O DJELU" in result
        assert "ZOO čl. 633" in result
        assert "800,00 EUR" in result

    def test_raskid_kupoprodaje_neplacanje(self):
        from generatori.obvezno import generiraj_raskid_kupoprodaje
        podaci = {
            'razlog_tip': 'neplacanje',
            'ugovor_datum': '01.04.2026.',
            'predmet': 'VW Golf, ZG-1234-AB',
            'opis_neispunjenja': 'Kupac nije platio cijenu',
            'cijena_eur': 8000.0,
            'rok_ostavljen': '20.04.2026.',
            'mjesto': 'Zagreb',
        }
        result = generiraj_raskid_kupoprodaje(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "RASKIDU KUPOPRODAJE" in result
        assert "neispunjenja obveze plaćanja" in result
        assert "8.000,00 EUR" in result
        assert "PRODAVATELJ" in result


# =============================================================================
# FAZA 2C — PRIGOVOR RACUNU (3 sektora)
# =============================================================================

class TestPrigovorRacunu:
    POTROSAC = STRANKA

    def _podaci(self, sektor, davatelj):
        return {
            'sektor': sektor,
            'davatelj': davatelj,
            'davatelj_adresa': 'Vrtni put 1, Zagreb',
            'broj_racuna': '12345/2026',
            'datum_racuna': '15.04.2026.',
            'razdoblje': 'ožujak 2026.',
            'sporni_iznos_eur': 45.50,
            'ukupno_racun_eur': 89.20,
            'razlog_prigovora': 'Naplaćena usluga koju nisam koristio',
            'broj_korisnika': '987654321',
            'mjesto': 'Zagreb',
        }

    def test_prigovor_telekom(self):
        from generatori.potrosaci import generiraj_prigovor_racunu
        result = generiraj_prigovor_racunu(self.POTROSAC, self._podaci('telekom', 'A1 HRVATSKA d.o.o.'))
        _assert_valid_html(result)
        assert "TELEKOMUNIKACIJSKE" in result
        assert "HAKOM" in result
        assert "elektroničkim komunikacijama" in result
        assert "45,50 EUR" in result

    def test_prigovor_energetika(self):
        from generatori.potrosaci import generiraj_prigovor_racunu
        result = generiraj_prigovor_racunu(self.POTROSAC, self._podaci('energetika', 'HEP-Opskrba d.o.o.'))
        _assert_valid_html(result)
        assert "ENERGETSKA" in result
        assert "HERA" in result
        assert "45,50 EUR" in result

    def test_prigovor_voda(self):
        from generatori.potrosaci import generiraj_prigovor_racunu
        result = generiraj_prigovor_racunu(self.POTROSAC, self._podaci('voda', 'Vodovod d.o.o.'))
        _assert_valid_html(result)
        assert "KOMUNALNE" in result or "VODNE" in result
        assert "vodnim uslugama" in result
        assert "45,50 EUR" in result


# =============================================================================
# FAZA 3A — TRGOVACKO EXT (zalog na udjelu d.o.o.)
# =============================================================================

class TestZalogUdjela:
    def test_zalog_udjela(self):
        from generatori.trgovacko import generiraj_zalog_udjela
        podaci = {
            'oib_drustva': '99999999999',
            'mbs_drustva': '12345678',
            'sjediste_drustva': 'Vukovarska 5, Zagreb',
            'nominalni_iznos_eur': 50000.0,
            'postotak_udjela': '50%',
            'iznos_trazbine_eur': 30000.0,
            'kamatna_stopa': '5% godišnje',
            'rok_dospijeca': '31.12.2027.',
            'osnova_trazbine': 'Ugovor o zajmu od 01.05.2026.',
            'glasacka_prava': 'duznik',
            'dividenda_kome': 'duznik',
            'mjesto': 'Zagreb',
        }
        result = generiraj_zalog_udjela(STRANKA, STRANKA2, "NOVA TVRTKA d.o.o.", podaci)
        _assert_valid_html(result)
        assert "ZTD čl. 412" in result
        assert "50.000,00 EUR" in result
        assert "30.000,00 EUR" in result
        assert "Sudski registar" in result
        assert "NOVA TVRTKA" in result
        assert "50%" in result

    def test_zalog_udjela_glas_vjerovniku(self):
        """Provjera alternativne klauzule glasačkih prava."""
        from generatori.trgovacko import generiraj_zalog_udjela
        podaci = {
            'iznos_trazbine_eur': 10000.0,
            'osnova_trazbine': 'Test',
            'glasacka_prava': 'vjerovnik',
            'dividenda_kome': 'vjerovnik',
            'mjesto': 'Zagreb',
        }
        result = generiraj_zalog_udjela(STRANKA, STRANKA2, "TEST d.o.o.", podaci)
        _assert_valid_html(result)
        assert "izvršava Založni vjerovnik" in result
        assert "pripadaju Založnom vjerovniku" in result


# =============================================================================
# FAZA 3B — POKRETNINE (FINA zalog + vozilo)
# =============================================================================

class TestPokretnine:
    def test_zalog_pokretnine_bezdrzavinski(self):
        from generatori.pokretnine import generiraj_zalog_pokretnine
        podaci = {
            'opis_predmeta': 'CNC stroj XYZ Model A1',
            'identifikacija': 'SN-998877',
            'procjena_vrijednosti_eur': 25000.0,
            'iznos_trazbine_eur': 15000.0,
            'kamatna_stopa': 'zakonska zatezna',
            'rok_dospijeca': '31.12.2027.',
            'osnova_trazbine': 'Ugovor o zajmu',
            'mjesto_pohrane': 'Skladište d.d., Zagreb',
            'oblik_zaloga': 'bezdrzavinski',
            'mjesto': 'Zagreb',
        }
        result = generiraj_zalog_pokretnine(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "ZALOŽNOG PRAVA NA POKRETNINI" in result
        assert "FINA" in result
        assert "121/05" in result
        assert "15.000,00 EUR" in result
        assert "CNC stroj" in result
        assert "Skladište d.d." in result

    def test_zalog_pokretnine_drzavinski(self):
        """Provjera alternative posjedovne klauzule."""
        from generatori.pokretnine import generiraj_zalog_pokretnine
        podaci = {
            'opis_predmeta': 'Umjetnička slika',
            'iznos_trazbine_eur': 5000.0,
            'osnova_trazbine': 'Zajam',
            'oblik_zaloga': 'drzavinski',
            'mjesto': 'Zagreb',
        }
        result = generiraj_zalog_pokretnine(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "u posjed Vjerovnika" in result or "predaje u posjed" in result

    def test_zalog_vozila(self):
        from generatori.pokretnine import generiraj_zalog_vozila
        podaci = {
            'marka': 'Volkswagen', 'model': 'Golf',
            'godina_proizvodnje': '2020',
            'registracijska_oznaka': 'ZG-1234-AB',
            'broj_sasije_vin': 'WVWZZZ1KZ8W123456',
            'broj_motora': 'CBA1234',
            'boja': 'srebrna metalik',
            'prijedeni_km': '85.000',
            'procjena_vrijednosti_eur': 18000.0,
            'iznos_trazbine_eur': 12000.0,
            'kamatna_stopa': 'zakonska zatezna',
            'rok_dospijeca': '31.12.2027.',
            'osnova_trazbine': 'Ugovor o zajmu',
            'mjesto': 'Zagreb',
        }
        result = generiraj_zalog_vozila(STRANKA, STRANKA2, podaci)
        _assert_valid_html(result)
        assert "MOTORNOM VOZILU" in result
        assert "Volkswagen" in result
        assert "Golf" in result
        assert "ZG-1234-AB" in result
        assert "WVWZZZ1KZ8W123456" in result
        assert "12.000,00 EUR" in result
        assert "prometn" in result.lower()
        assert "FINA" in result


# =============================================================================
# REGRESIJSKI: Sidebar search keywords pokrivaju nove dokumente
# =============================================================================

class TestSearchKeywords:
    """Provjera da je sidebar search bug ostao zatvoren — keywords moraju
    pokrivati dokumente unutar modula, ne samo nazive modula."""

    def test_tabularna_se_pronalazi(self):
        """Bug korisnika: 'tabularna' nije nalazila Zemljišne knjige."""
        content = open(
            os.path.join(os.path.dirname(__file__), '..', 'LEGAL-SUITE.py'),
            encoding='utf-8',
        ).read()
        # Naci redak za Zemljisne knjige modul
        zem_idx = content.find('"Zemljišne knjige":')
        assert zem_idx > 0, "Modul 'Zemljišne knjige' ne postoji"
        zem_block = content[zem_idx:zem_idx + 1000]
        assert 'tabularna' in zem_block.lower()
        assert 'plodouziv' in zem_block.lower() or 'plodouz' in zem_block.lower()
        assert 'brisovno' in zem_block.lower()

    def test_brodica_se_pronalazi(self):
        content = open(
            os.path.join(os.path.dirname(__file__), '..', 'LEGAL-SUITE.py'),
            encoding='utf-8',
        ).read()
        naut_idx = content.find('"Nautika":')
        assert naut_idx > 0
        block = content[naut_idx:naut_idx + 800]
        assert 'brodic' in block.lower()
        assert 'tabularna' in block.lower()
        assert 'pomorski zakonik' in block.lower()

    def test_mtu_kategorizacija_se_pronalaze(self):
        content = open(
            os.path.join(os.path.dirname(__file__), '..', 'LEGAL-SUITE.py'),
            encoding='utf-8',
        ).read()
        ap_idx = content.find('"Apartmani":')
        assert ap_idx > 0
        block = content[ap_idx:ap_idx + 800]
        assert 'mtu' in block.lower()
        assert 'kategorizac' in block.lower()
        assert '9/16' in block
        assert '56/16' in block

    def test_predugovor_raskid_pronalaze(self):
        content = open(
            os.path.join(os.path.dirname(__file__), '..', 'LEGAL-SUITE.py'),
            encoding='utf-8',
        ).read()
        obv_idx = content.find('"Obvezno pravo":')
        assert obv_idx > 0
        block = content[obv_idx:obv_idx + 800]
        assert 'predugovor' in block.lower()
        assert 'raskid' in block.lower()

    def test_zalog_pokretnine_pronalaze(self):
        content = open(
            os.path.join(os.path.dirname(__file__), '..', 'LEGAL-SUITE.py'),
            encoding='utf-8',
        ).read()
        pkr_idx = content.find('"Pokretnine":')
        assert pkr_idx > 0
        block = content[pkr_idx:pkr_idx + 800]
        assert 'zalog' in block.lower()
        assert 'fina' in block.lower()
        assert 'vozilo' in block.lower() or 'vin' in block.lower()
