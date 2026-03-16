# -----------------------------------------------------------------------------
# UNIT TESTOVI: sudovi.py
# -----------------------------------------------------------------------------
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudovi import (
    SUDOVI, dohvati_sudove, dohvati_adresu_suda, format_sud_s_dijakriticima,
    OPCINSKI_SUDOVI, TRGOVACKI_SUDOVI, ZUPANIJSKI_SUDOVI, UPRAVNI_SUDOVI,
)


class TestBazaSudova:
    def test_total_count(self):
        assert len(SUDOVI) >= 70

    def test_opcinski_count(self):
        assert len(OPCINSKI_SUDOVI) >= 30

    def test_trgovacki_count(self):
        assert len(TRGOVACKI_SUDOVI) >= 8

    def test_upravni_count(self):
        assert len(UPRAVNI_SUDOVI) >= 4

    def test_all_have_required_fields(self):
        for naziv, data in SUDOVI.items():
            assert "adresa" in data, f"{naziv} nema adresu"
            assert "vrsta" in data, f"{naziv} nema vrstu"
            assert "grad" in data, f"{naziv} nema grad"


class TestDohvatiSudove:
    def test_all(self):
        svi = dohvati_sudove()
        assert len(svi) == len(SUDOVI)

    def test_filtered(self):
        opcinski = dohvati_sudove("opcinski")
        for s in opcinski:
            assert SUDOVI[s]["vrsta"] == "opcinski"

    def test_sorted(self):
        svi = dohvati_sudove()
        assert svi == sorted(svi)


class TestDohvatiAdresuSuda:
    def test_existing(self):
        adresa = dohvati_adresu_suda("OPCINSKI GRADANSKI SUD U ZAGREBU")
        assert "Zagreb" in adresa

    def test_nonexistent(self):
        assert dohvati_adresu_suda("NEPOSTOJECI SUD") == ""


class TestFormatDijakriticima:
    def test_opcinski(self):
        result = format_sud_s_dijakriticima("OPCINSKI GRADANSKI SUD U ZAGREBU")
        assert "OPĆINSKI" in result
        assert "GRAĐANSKI" in result

    def test_trgovacki(self):
        result = format_sud_s_dijakriticima("TRGOVACKI SUD U ZAGREBU")
        assert "TRGOVAČKI" in result

    def test_no_change_needed(self):
        assert format_sud_s_dijakriticima("SUD U ZAGREBU") == "SUD U ZAGREBU"
