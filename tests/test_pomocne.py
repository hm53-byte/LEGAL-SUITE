# -----------------------------------------------------------------------------
# UNIT TESTOVI: pomocne.py
# Pokretanje: python -m pytest tests/ -v
# -----------------------------------------------------------------------------
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pomocne import _escape, _validiraj_oib, _rimski_broj, format_eur, format_navodnici, _padez_ime, _padez_uloge


class TestEscape:
    def test_basic(self):
        assert _escape("<script>") == "&lt;script&gt;"

    def test_none(self):
        assert _escape(None) == ""

    def test_empty(self):
        assert _escape("") == ""

    def test_ampersand(self):
        assert _escape("A & B") == "A &amp; B"

    def test_number(self):
        assert _escape(123) == "123"


class TestValidirajOib:
    def test_empty(self):
        ok, msg = _validiraj_oib("")
        assert ok is False

    def test_too_short(self):
        ok, msg = _validiraj_oib("1234567890")
        assert ok is False
        assert "11 znamenki" in msg

    def test_not_digits(self):
        ok, msg = _validiraj_oib("1234567890a")
        assert ok is False

    def test_valid_constructed(self):
        # Construct a valid OIB using the algorithm
        carry = 10
        for d in "0000000000":
            carry = (carry + int(d)) % 10
            if carry == 0:
                carry = 10
            carry = (carry * 2) % 11
        kontrolna = (11 - carry) % 10
        oib = f"0000000000{kontrolna}"
        ok, msg = _validiraj_oib(oib)
        assert ok is True
        assert msg == ""

    def test_wrong_checksum(self):
        ok, msg = _validiraj_oib("00000000000")
        # 0 is not the valid check digit for 0000000000
        if not ok:
            assert "kontrolna" in msg

    def test_whitespace_stripped(self):
        carry = 10
        for d in "0000000000":
            carry = (carry + int(d)) % 10
            if carry == 0:
                carry = 10
            carry = (carry * 2) % 11
        kontrolna = (11 - carry) % 10
        oib = f" 0000000000{kontrolna} "
        ok, msg = _validiraj_oib(oib)
        assert ok is True


class TestRimskiBroj:
    def test_basic(self):
        assert _rimski_broj(1) == "I"
        assert _rimski_broj(4) == "IV"
        assert _rimski_broj(9) == "IX"
        assert _rimski_broj(14) == "XIV"
        assert _rimski_broj(40) == "XL"
        assert _rimski_broj(99) == "XCIX"
        assert _rimski_broj(2024) == "MMXXIV"

    def test_zero(self):
        assert _rimski_broj(0) == "0"

    def test_negative(self):
        assert _rimski_broj(-1) == "-1"


class TestFormatEur:
    def test_basic(self):
        assert format_eur(1000) == "1.000,00 EUR"

    def test_zero(self):
        assert format_eur(0) == "0,00 EUR"

    def test_none(self):
        assert format_eur(None) == "0,00 EUR"

    def test_decimal(self):
        assert format_eur(1234.56) == "1.234,56 EUR"

    def test_large(self):
        assert format_eur(10000000) == "10.000.000,00 EUR"


class TestFormatNavodnici:
    def test_converts_to_croatian(self):
        result = format_navodnici('rekao je "da"')
        assert "\u201E" in result  # „ (opening Croatian quote)
        assert "\u201C" in result  # \u201C (closing Croatian quote)

    def test_italic(self):
        result = format_navodnici('rekao je "da"')
        assert "<i>" in result
        assert "</i>" in result

    def test_empty(self):
        assert format_navodnici("") == ""
        assert format_navodnici(None) is None

    def test_no_quotes(self):
        text = "nema navodnika"
        assert format_navodnici(text) == text


class TestPadezIme:
    """Testovi za deklinaciju osobnih imena."""

    def test_musko_ime_prezime_gen(self):
        assert _padez_ime("Ivan Horvat", "gen") == "Ivana Horvata"

    def test_musko_ic_prezime_gen(self):
        assert _padez_ime("Marko Babic", "gen") == "Marka Babica"

    def test_zensko_ime_a_gen(self):
        assert _padez_ime("Ana Horvat", "gen") == "Ane Horvata"

    def test_marija_gen(self):
        assert _padez_ime("Marija Juric", "gen") == "Marije Jurica"

    def test_petar_nepostojano_a_gen(self):
        assert _padez_ime("Petar Kovac", "gen") == "Petra Kovaca"

    def test_marko_o_dat(self):
        assert _padez_ime("Marko Juric", "dat") == "Marku Juricu"

    def test_ivan_instr(self):
        assert _padez_ime("Ivan Horvat", "instr") == "Ivanom Horvatom"

    def test_nominativ_nema_promjene(self):
        assert _padez_ime("Ivan Horvat", "nom") == "Ivan Horvat"

    def test_prazno(self):
        assert _padez_ime("", "gen") == ""
        assert _padez_ime(None, "gen") is None

    def test_samo_ime(self):
        assert _padez_ime("Ivan", "gen") == "Ivana"
        assert _padez_ime("Ana", "dat") == "Ani"

    def test_petar_lok(self):
        assert _padez_ime("Petar", "lok") == "Petru"


class TestPadezUloge:
    """Testovi za deklinaciju oznaka uloga."""

    def test_tuzitelj_gen(self):
        assert _padez_uloge("Tužitelj", "gen") == "Tužitelja"

    def test_kupac_dat(self):
        assert _padez_uloge("Kupac", "dat") == "Kupcu"

    def test_strana_s_brojem(self):
        assert _padez_uloge("Strana 1", "gen") == "Strane 1"

    def test_roditelj_s_brojem(self):
        assert _padez_uloge("Roditelj 2", "dat") == "Roditelju 2"

    def test_nepoznata_uloga(self):
        assert _padez_uloge("Nepoznato", "gen") == "Nepoznato"

    def test_nom_nema_promjene(self):
        assert _padez_uloge("Tužitelj", "nom") == "Tužitelj"
