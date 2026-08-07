# -----------------------------------------------------------------------------
# UNIT TESTOVI: pristojbe.py
# -----------------------------------------------------------------------------
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pristojbe import (
    pristojba_tuzba, pristojba_zalba, pristojba_revizija,
    pristojba_ovrha_jb, pristojba_zk_prijedlog, pristojba_upravni_spor,
    izracunaj_pristojbu,
)


class TestPristojbaTuzba:
    def test_zero_vps(self):
        assert pristojba_tuzba(0) == 0.0

    def test_small_vps(self):
        assert pristojba_tuzba(500) == 13.27

    def test_medium_vps(self):
        assert pristojba_tuzba(5000) == 79.63

    def test_large_vps(self):
        # 50000 EUR is in range 26.544-66.361 EUR -> 398.17 EUR
        assert pristojba_tuzba(50000) == 398.17

    def test_very_large_vps(self):
        result = pristojba_tuzba(200000)
        assert result <= 4404.15  # max cap

    def test_monotonic_increase(self):
        """Pristojba raste s VPS-om."""
        prev = 0
        for vps in [100, 1000, 5000, 10000, 50000, 100000]:
            current = pristojba_tuzba(vps)
            assert current >= prev
            prev = current


class TestPristojbaZalba:
    def test_double_tuzba(self):
        for vps in [1000, 5000, 50000]:
            assert pristojba_zalba(vps) == round(pristojba_tuzba(vps) * 2, 2)


class TestPristojbaRevizija:
    def test_triple_tuzba(self):
        for vps in [1000, 5000, 50000]:
            assert pristojba_revizija(vps) == round(pristojba_tuzba(vps) * 3, 2)


class TestPristojbaOvrha:
    def test_half_tuzba(self):
        vps = 50000
        result = pristojba_ovrha_jb(vps)
        assert result == round(max(pristojba_tuzba(vps) / 2, 6.64), 2)

    def test_min_cap(self):
        assert pristojba_ovrha_jb(100) >= 6.64


class TestFiksne:
    def test_zk_prijedlog(self):
        assert pristojba_zk_prijedlog() == 33.18

    def test_upravni_spor(self):
        assert pristojba_upravni_spor() == 26.54


class TestIzracunajPristojbu:
    def test_tuzba(self):
        assert izracunaj_pristojbu('tuzba', vps=5000) == pristojba_tuzba(5000)

    def test_unknown(self):
        assert izracunaj_pristojbu('nepostojeci') == 0.0

    def test_zk(self):
        assert izracunaj_pristojbu('zk_prijedlog') == 33.18
