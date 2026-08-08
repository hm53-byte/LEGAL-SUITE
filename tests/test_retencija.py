"""Testovi retencije download_loga (24 mjeseca) i ponasanja lanca heseva.

Nijedan test ne dira pravi Supabase. Sloj prema bazi zamijenjen je laznim
klijentom koji oponasa PostgREST filtre nad listom u memoriji, pa se testira
pravilo odabira, a ne mreza.

Granica: usporedba je `generated_at <= granica`, dakle UKLJUCIVA. Redak star
tocno 24 mjeseca se obradjuje. Obrazlozenje: obecani rok je gornja granica
cuvanja, pa se dvojba rjesava u korist ranijeg brisanja (GDPR cl. 5 st. 1
t. (e)). Isti se izbor mora zadrzati i u SQL funkciji.
"""
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from scripts import retencija_download_log as rd


KORIJEN = Path(__file__).resolve().parent.parent
SQL_PUT = KORIJEN / "cloud" / "0008_retencija_download_log.sql"

SADA = datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)
GRANICA_24 = datetime(2024, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def _iso(t: datetime) -> str:
    return t.astimezone(timezone.utc).isoformat()


def _redak(generated_at: datetime, ident: str = "id-1", **preglasi) -> dict:
    redak = {
        "id": ident,
        "user_id": "11111111-1111-1111-1111-111111111111",
        "doc_type": "tuzba",
        "doc_subtype": "parnicna",
        "serial_hash": "a" * 64,
        "plan_at_download": "free",
        "generated_at": _iso(generated_at),
        "input_canonical_hash": "b" * 64,
        "output_sha256": "c" * 64,
        "parent_hash": "d" * 64,
        "current_hash": "e" * 64,
        "generator_version_hash": "f" * 64,
        "input_schema_version": "v1",
        "anonymized_at": None,
    }
    redak.update(preglasi)
    return redak


class LazniSupabase:
    """Oponasa PostgREST uvjet `anonymized_at is.null AND generated_at lte.X`.

    Usporedba ide nad ISO nizovima s istim pomakom (+00:00), gdje je leksicki
    poredak jednak vremenskom, isto kao sto bi Postgres usporedio timestamptz.
    """

    def __init__(self, redci):
        self.redci = [dict(r) for r in redci]
        self.pozivi = []

    def _pogodjeni(self, granica):
        return [
            r
            for r in self.redci
            if r.get("anonymized_at") is None and r["generated_at"] <= granica
        ]

    def prebroji(self, granica):
        self.pozivi.append(("prebroji", granica))
        return len(self._pogodjeni(granica))

    def uzorak(self, granica, koliko):
        self.pozivi.append(("uzorak", granica, koliko))
        redci = sorted(self._pogodjeni(granica), key=lambda r: r["generated_at"])
        return [
            {
                "id": r["id"],
                "generated_at": r["generated_at"],
                "doc_type": r["doc_type"],
            }
            for r in redci[:koliko]
        ]

    def anonimiziraj(self, granica, oznaka):
        self.pozivi.append(("anonimiziraj", granica, oznaka))
        broj = 0
        for redak in self._pogodjeni(granica):
            redak.update(rd.PRAZNI_STUPCI)
            redak["anonymized_at"] = oznaka
            broj += 1
        return broj


def _pokreni(klijent, **kw):
    """Pokreni posao i vrati (izlazni_kod, ispis kao jedan niz)."""
    redovi = []
    kod = rd.pokreni(klijent, sada=SADA, ispis=redovi.append, **kw)
    return kod, "\n".join(redovi)


# =============================================================================
# Granica roka
# =============================================================================


def test_granica_je_tocno_24_mjeseca_prije_sada():
    assert rd.granica_iso(SADA, 24) == _iso(GRANICA_24)


def test_redak_stariji_od_24_mjeseca_se_obradi():
    klijent = LazniSupabase([_redak(GRANICA_24 - timedelta(days=1))])
    kod, ispis = _pokreni(klijent, izvrsi=True)
    assert kod == 0
    assert "Obradjeno redaka: 1" in ispis
    assert klijent.redci[0]["anonymized_at"] is not None


def test_redak_mladji_od_24_mjeseca_se_ne_dira():
    klijent = LazniSupabase([_redak(GRANICA_24 + timedelta(seconds=1))])
    kod, ispis = _pokreni(klijent, izvrsi=True)
    assert kod == 0
    assert "Nema redaka za obradu" in ispis
    assert klijent.redci[0]["anonymized_at"] is None
    assert klijent.redci[0]["user_id"] is not None


def test_redak_star_tocno_24_mjeseca_se_obradi():
    """Granica je ukljuciva; sekundu mladji redak ostaje netaknut."""
    klijent = LazniSupabase(
        [
            _redak(GRANICA_24, ident="na-granici"),
            _redak(GRANICA_24 + timedelta(seconds=1), ident="sekundu-mladji"),
        ]
    )
    kod, _ = _pokreni(klijent, izvrsi=True)
    assert kod == 0
    po_id = {r["id"]: r for r in klijent.redci}
    assert po_id["na-granici"]["anonymized_at"] is not None
    assert po_id["sekundu-mladji"]["anonymized_at"] is None


def test_oduzmi_mjesece_podrezuje_dan_na_zadnji_u_mjesecu():
    """Isto ponasanje kao Postgresov make_interval: 31.03. minus 1 mjesec je
    28.02., odnosno 29.02. u prijestupnoj godini."""
    assert rd.oduzmi_mjesece(
        datetime(2026, 3, 31, 8, 0, tzinfo=timezone.utc), 1
    ) == datetime(2026, 2, 28, 8, 0, tzinfo=timezone.utc)
    assert rd.oduzmi_mjesece(
        datetime(2024, 3, 31, 8, 0, tzinfo=timezone.utc), 1
    ) == datetime(2024, 2, 29, 8, 0, tzinfo=timezone.utc)


def test_oduzmi_mjesece_preko_granice_godine():
    assert rd.oduzmi_mjesece(
        datetime(2026, 1, 15, 0, 0, tzinfo=timezone.utc), 24
    ) == datetime(2024, 1, 15, 0, 0, tzinfo=timezone.utc)
    assert rd.oduzmi_mjesece(
        datetime(2024, 2, 29, 0, 0, tzinfo=timezone.utc), 12
    ) == datetime(2023, 2, 28, 0, 0, tzinfo=timezone.utc)


def test_naivan_trenutak_tumaci_se_kao_utc():
    naivan = datetime(2026, 8, 9, 12, 0, 0)
    assert rd.granica_iso(naivan, 24) == _iso(GRANICA_24)


def test_prijestupni_dan_kasni_jedan_dan():
    """Jedini slucaj u kojem se rok probija umjesto da se skrati.

    Redak od 29.02.2024. nije uhvacen 28.02.2026. jer podrezivanje daje granicu
    28.02.2024., nego tek 01.03.2026., dakle 731 dan. Test postoji da promjena
    racuna granice ne prodje nezapazeno; obrazlozenje i cijena alternative su u
    komentaru uz funkciju download_log_anonimiziraj u SQL migraciji.
    """
    redak = datetime(2024, 2, 29, 12, 0, tzinfo=timezone.utc)
    assert rd.granica_iso(datetime(2026, 2, 28, 12, 0, tzinfo=timezone.utc), 24) < _iso(redak)
    assert rd.granica_iso(datetime(2026, 3, 1, 12, 0, tzinfo=timezone.utc), 24) > _iso(redak)
    assert (datetime(2026, 3, 1, 12, 0, tzinfo=timezone.utc) - redak).days == 731


def test_svaki_drugi_datum_pogodjen_na_730_ili_731_dan():
    """Podrezivanje ne smije nikoga zadrzati dulje od dana viska.

    Prolazi kroz sve dane dvije godine i trazi prvi trenutak u kojem redak
    upada u granicu. Bez ove provjere jedna izmjena racuna mogla bi produljiti
    cuvanje za citav mjesec, a nijedan drugi test to ne bi vidio.
    """
    najgori = 0
    dan = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    while dan.year < 2026:
        pogodjen = dan + timedelta(days=729)
        while rd.granica_iso(pogodjen, 24) < _iso(dan):
            pogodjen += timedelta(days=1)
        najgori = max(najgori, (pogodjen - dan).days)
        dan += timedelta(days=1)
    assert najgori == 731, "najdulje cuvanje je %d dana" % najgori


# =============================================================================
# Suhi hod
# =============================================================================


def test_suhi_hod_je_zadano_stanje_i_nista_ne_mijenja():
    klijent = LazniSupabase([_redak(GRANICA_24 - timedelta(days=100))])
    prije = dict(klijent.redci[0])
    kod, ispis = _pokreni(klijent)
    assert kod == 0
    assert "SUHI HOD" in ispis
    assert klijent.redci[0] == prije
    assert not any(p[0] == "anonimiziraj" for p in klijent.pozivi)


def test_suhi_hod_ispisuje_koliko_bi_redaka_dirao():
    redci = [
        _redak(GRANICA_24 - timedelta(days=d), ident="id-%d" % d)
        for d in (10, 20, 30)
    ]
    kod, ispis = _pokreni(LazniSupabase(redci))
    assert kod == 0
    assert "pogodjeno redaka: 3" in ispis
    assert "tuzba" in ispis


def test_suhi_hod_ne_ispisuje_user_id():
    """Ispis zavrsava u cron logu, pa iz baze ne izlazi osobni identifikator."""
    klijent = LazniSupabase([_redak(GRANICA_24 - timedelta(days=5))])
    _, ispis = _pokreni(klijent)
    assert "11111111-1111-1111-1111-111111111111" not in ispis


# =============================================================================
# Izvrsenje
# =============================================================================


def test_izvrsenje_prazni_sve_osobne_stupce():
    klijent = LazniSupabase([_redak(GRANICA_24 - timedelta(days=5))])
    kod, _ = _pokreni(klijent, izvrsi=True)
    assert kod == 0
    redak = klijent.redci[0]
    for stupac in rd.PRAZNI_STUPCI:
        assert redak[stupac] is None, stupac


def test_izvrsenje_cuva_kariku_lanca_i_datum():
    redak = _redak(GRANICA_24 - timedelta(days=5))
    klijent = LazniSupabase([redak])
    _pokreni(klijent, izvrsi=True)
    obradjen = klijent.redci[0]
    assert obradjen["parent_hash"] == redak["parent_hash"]
    assert obradjen["current_hash"] == redak["current_hash"]
    assert obradjen["generated_at"] == redak["generated_at"]


def test_ponovno_pokretanje_ne_dira_vec_obradjene_retke():
    klijent = LazniSupabase([_redak(GRANICA_24 - timedelta(days=5))])
    _pokreni(klijent, izvrsi=True)
    oznaka_prvog_prolaza = klijent.redci[0]["anonymized_at"]

    kod, ispis = _pokreni(klijent, izvrsi=True)
    assert kod == 0
    assert "Nema redaka za obradu" in ispis
    assert klijent.redci[0]["anonymized_at"] == oznaka_prvog_prolaza


def test_prazna_tablica_ne_pada():
    kod, ispis = _pokreni(LazniSupabase([]), izvrsi=True)
    assert kod == 0
    assert "pogodjeno redaka: 0" in ispis


def test_neispravan_broj_mjeseci_odbijen():
    for lose in (0, -1, "24", True, None):
        kod, ispis = _pokreni(LazniSupabase([]), mjeseci=lose)
        assert kod == 4, lose
        assert "cijeli broj >= 1" in ispis


def test_neispravan_broj_mjeseci_iznad_gornje_granice():
    """Bez gornje granice racun granice odlazi ispod godine 1 i skripta zavrsi
    tragom steka i izlaznim kodom 1, kojeg nema u tablici izlaznih kodova."""
    kod, ispis = _pokreni(LazniSupabase([]), mjeseci=100000)
    assert kod == 4
    assert "1200" in ispis


def test_greska_u_komunikaciji_daje_izlazni_kod_3():
    class Pukne(LazniSupabase):
        def prebroji(self, granica):
            raise rd.GreskaRest("Supabase HTTP 503")

    kod, ispis = _pokreni(Pukne([]), izvrsi=True)
    assert kod == 3
    assert "503" in ispis


@pytest.mark.parametrize(
    "korak", ["prebroji", "uzorak", "anonimiziraj"]
)
def test_prekid_mreze_daje_izlazni_kod_3_a_ne_trag_steka(korak):
    """Mreza puca u bilo kojem od tri koraka; ishod mora biti dokumentiran kod.

    Skripta se pokrece iz crona i vlasnik je prati po izlaznom kodu. Nepokrivena
    iznimka iz requestsa daje kod 1, koji u docs/brisanje_podataka.md ne postoji,
    pa vlasnik ne zna je li posao radio.
    """
    import requests

    class PukniMrezu(LazniSupabase):
        pass

    def puca(*a, **kw):
        raise requests.exceptions.ConnectionError("Connection aborted")

    klijent = PukniMrezu([_redak(GRANICA_24 - timedelta(days=5))])
    # Sloj prema Supabaseu iznimke mreze pretvara u GreskaRest; ovdje se
    # oponasa taj sloj, jer lazni klijent inace nikad ne dira requests.
    def omotaj(izvorna):
        def unutra(*a, **kw):
            if izvorna.__name__ == korak:
                try:
                    puca()
                except requests.exceptions.RequestException as greska:
                    raise rd.GreskaRest("Supabase nije dostupan: " + str(greska))
            return izvorna(*a, **kw)
        return unutra

    for ime in ("prebroji", "uzorak", "anonimiziraj"):
        setattr(klijent, ime, omotaj(getattr(klijent, ime)))

    kod, ispis = _pokreni(klijent, izvrsi=True)
    assert kod == 3
    assert "Supabase nije dostupan" in ispis
    assert klijent.redci[0]["user_id"] is not None


def test_sloj_prema_supabaseu_hvata_iznimke_requestsa(monkeypatch):
    """Provjera pravog sloja, ne laznog: bez ovoga bi ConnectionError izisao iz
    procesa prije nego ga pokreni() vidi."""
    import requests

    klijent = rd.SupabaseRest("https://x.supabase.co", "kljuc")

    def puca(*a, **kw):
        raise requests.exceptions.ConnectTimeout("timed out")

    monkeypatch.setattr(rd.requests, "get", puca)
    monkeypatch.setattr(rd.requests, "patch", puca)
    for poziv in (
        lambda: klijent.prebroji(_iso(GRANICA_24)),
        lambda: klijent.uzorak(_iso(GRANICA_24), 5),
        lambda: klijent.anonimiziraj(_iso(GRANICA_24), _iso(SADA)),
    ):
        with pytest.raises(rd.GreskaRest) as greska:
            poziv()
        assert "ConnectTimeout" in str(greska.value)


def test_odgovor_koji_nije_json_daje_gresku_a_ne_trag_steka(monkeypatch):
    """Supabase u kvaru zna vratiti HTML stranicu s kodom 200."""

    class HtmlOdgovor:
        status_code = 200
        headers = {"Content-Range": "0-0/1"}
        text = "<html>502</html>"

        def json(self):
            raise ValueError("Expecting value: line 1 column 1 (char 0)")

    klijent = rd.SupabaseRest("https://x.supabase.co", "kljuc")
    monkeypatch.setattr(rd.requests, "get", lambda *a, **kw: HtmlOdgovor())
    with pytest.raises(rd.GreskaRest) as greska:
        klijent.uzorak(_iso(GRANICA_24), 5)
    assert "nije vratio JSON" in str(greska.value)


# =============================================================================
# Nepodesen rad
# =============================================================================


def test_bez_ijedne_varijable_posao_se_odbija():
    with pytest.raises(rd.Nepodeseno) as greska:
        rd.ucitaj_konfiguraciju({})
    poruka = str(greska.value)
    assert "SUPABASE_URL" in poruka
    assert "SUPABASE_SERVICE_ROLE_KEY" in poruka
    assert "nije pokrenut" in poruka


def test_bez_kljuca_posao_se_odbija():
    with pytest.raises(rd.Nepodeseno) as greska:
        rd.ucitaj_konfiguraciju({"SUPABASE_URL": "https://x.supabase.co"})
    assert "SUPABASE_SERVICE_ROLE_KEY" in str(greska.value)


def test_url_bez_sheme_odbijen():
    with pytest.raises(rd.Nepodeseno) as greska:
        rd.ucitaj_konfiguraciju(
            {"SUPABASE_URL": "x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k"}
        )
    assert "https://" in str(greska.value)


def _jwt_s_ulogom(uloga: str) -> str:
    import base64
    import json

    def dio(podaci):
        sirovo = json.dumps(podaci, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(sirovo).decode("ascii").rstrip("=")

    return dio({"alg": "HS256"}) + "." + dio({"role": uloga}) + ".potpis"


def test_anon_kljuc_odbijen_s_objasnjenjem():
    """S anon kljucem RLS ne dopusta izmjenu, pa bi posao tiho obradio nulu."""
    with pytest.raises(rd.Nepodeseno) as greska:
        rd.ucitaj_konfiguraciju(
            {
                "SUPABASE_URL": "https://x.supabase.co",
                "SUPABASE_SERVICE_ROLE_KEY": _jwt_s_ulogom("anon"),
            }
        )
    poruka = str(greska.value)
    assert "anon" in poruka
    assert "service_role" in poruka


def test_service_role_kljuc_prihvacen():
    url, kljuc = rd.ucitaj_konfiguraciju(
        {
            "SUPABASE_URL": "https://x.supabase.co/",
            "SUPABASE_SERVICE_ROLE_KEY": _jwt_s_ulogom("service_role"),
        }
    )
    assert url == "https://x.supabase.co/"
    assert kljuc.count(".") == 2


def test_kljuc_koji_nije_jwt_prolazi():
    """Noviji Supabase kljucevi (sb_secret_...) nisu JWT; ne mozemo im procitati
    ulogu, pa se ne odbijaju."""
    url, kljuc = rd.ucitaj_konfiguraciju(
        {
            "SUPABASE_URL": "https://x.supabase.co",
            "SUPABASE_SERVICE_ROLE_KEY": "sb_secret_abcdef",
        }
    )
    assert kljuc == "sb_secret_abcdef"


def test_main_vraca_2_i_pise_na_stderr_kad_nije_podeseno(monkeypatch, capsys):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    assert rd.main([]) == 2
    zabiljezeno = capsys.readouterr()
    assert "SUPABASE_URL" in zabiljezeno.err


def test_main_ne_izvrsava_kad_su_zadane_obje_zastavice(monkeypatch):
    """Suhi hod pobjedjuje nad --izvrsi; sigurniji ishod ima prednost."""
    zabiljezeno = {}

    def lazni_pokreni(klijent, **kw):
        zabiljezeno.update(kw)
        return 0

    monkeypatch.setattr(
        rd, "ucitaj_konfiguraciju", lambda *a, **k: ("https://x", "kljuc")
    )
    monkeypatch.setattr(rd, "pokreni", lazni_pokreni)
    assert rd.main(["--izvrsi", "--suhi-hod"]) == 0
    assert zabiljezeno["izvrsi"] is False


# =============================================================================
# Zastita od praznjenja cijele tablice
# =============================================================================


def test_patch_bez_filtra_odbijen_prije_slanja(monkeypatch):
    klijent = rd.SupabaseRest("https://x.supabase.co", "kljuc")
    monkeypatch.setattr(rd.SupabaseRest, "_filtri", staticmethod(lambda granica: {}))

    def ne_smije_se_pozvati(*a, **kw):
        raise AssertionError("PATCH je poslan bez filtra")

    monkeypatch.setattr(rd.requests, "patch", ne_smije_se_pozvati)
    with pytest.raises(rd.GreskaRest) as greska:
        klijent.anonimiziraj(_iso(GRANICA_24), _iso(SADA))
    assert "cijela tablica" in str(greska.value)


def test_filtri_uvijek_sadrze_oba_uvjeta():
    filtri = rd.SupabaseRest._filtri(_iso(GRANICA_24))
    assert filtri["anonymized_at"] == "is.null"
    assert filtri["generated_at"].startswith("lte.")


def test_prazni_stupci_ne_ukljucuju_kariku_lanca():
    """Ako bi netko dodao parent_hash ili current_hash na popis, lanac bi se
    raspao a testovi retencije bi i dalje prolazili. Zato izricita brana."""
    for cuvani in ("parent_hash", "current_hash", "generated_at", "id"):
        assert cuvani not in rd.PRAZNI_STUPCI, cuvani
    for osobni in ("user_id", "doc_type", "doc_subtype", "serial_hash",
                   "plan_at_download", "input_canonical_hash", "output_sha256"):
        assert osobni in rd.PRAZNI_STUPCI, osobni


def _tijela_sql_funkcija() -> dict:
    """Razdvoji SQL datoteku na tijela pojedinih funkcija.

    Nuzno je gledati svaku zasebno: obje funkcije prazne isti popis stupaca, pa
    bi provjera nad cijelom datotekom prosla i kad jedna od njih izgubi stupac,
    jer bi ga druga i dalje spominjala.
    """
    sql = SQL_PUT.read_text(encoding="utf-8")
    tijela = {}
    for naziv in ("download_log_anonimiziraj", "download_log_anonimiziraj_korisnika"):
        pocetak = sql.index("CREATE OR REPLACE FUNCTION " + naziv + "(")
        tijela[naziv] = sql[pocetak:].split("$fn$;", 1)[0]
    # Duze ime sadrzi krace kao prefiks, pa `index` na krace pogodi pravo mjesto
    # samo ako je definicija krace funkcije prva u datoteci. Ovo to potvrdjuje.
    assert "p_mjeseci" in tijela["download_log_anonimiziraj"]
    assert "p_user_id" in tijela["download_log_anonimiziraj_korisnika"]
    return tijela


def test_sql_i_python_prazne_iste_stupce():
    """Pravilo postoji na tri mjesta (dvije SQL funkcije i ova skripta). Ako se
    raziđu, jedan bi put ostavljao podatke koje drugi brise."""
    for naziv, tijelo in _tijela_sql_funkcija().items():
        iz_sqla = set(re.findall(r"(\w+)\s*=\s*NULL", tijelo))
        assert iz_sqla == set(rd.PRAZNI_STUPCI), (
            "%s prazni %s, Python %s"
            % (naziv, sorted(iz_sqla), sorted(rd.PRAZNI_STUPCI))
        )


def test_check_ogranicenje_pokriva_svaki_ispraznjeni_stupac():
    """CHECK je jedina obrana ako se funkcija naknadno izmijeni.

    Stupac koji se prazni, a nije naveden u nadgrobnoj grani ogranicenja, moze
    ostati popunjen a da baza to prihvati kao uredan nadgrobni redak.
    """
    sql = SQL_PUT.read_text(encoding="utf-8")
    grana = sql.split("ADD CONSTRAINT download_log_zivi_ili_nadgrobni")[1].split(");")[0]
    u_ogranicenju = set(re.findall(r"AND\s+(\w+)\s+IS NULL", grana))
    nepokriveno = set(rd.PRAZNI_STUPCI) - u_ogranicenju
    assert not nepokriveno, "CHECK ne trazi NULL za: %s" % sorted(nepokriveno)


def test_sql_koristi_ukljucivu_granicu_i_preskace_obradjene():
    sql = SQL_PUT.read_text(encoding="utf-8")
    assert "generated_at  <= v_granica" in sql
    assert "anonymized_at IS NULL" in sql
    assert "make_interval(months => p_mjeseci)" in sql


# =============================================================================
# Lanac heseva nakon anonimizacije
# =============================================================================


POCETAK_LANCA = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)


def _lanac(koliko: int) -> list:
    import audit_chain as ac

    redci = []
    roditelj = None
    for i in range(koliko):
        ulaz = ("a" * 60) + ("%04d" % i)
        izlaz = ("b" * 60) + ("%04d" % i)
        generator = "c" * 64
        trenutni = ac.build_chain_link(ulaz, izlaz, generator, roditelj)
        redci.append(
            {
                "generated_at": _iso(POCETAK_LANCA + timedelta(days=i)),
                "input_canonical_hash": ulaz,
                "output_sha256": izlaz,
                "generator_version_hash": generator,
                "parent_hash": roditelj,
                "current_hash": trenutni,
                "input_schema_version": "v1",
                "anonymized_at": None,
            }
        )
        roditelj = trenutni
    return redci


def _u_nadgrobni(redak: dict, anonymized_at: str = "2026-08-09T03:17:00+00:00") -> dict:
    novi = dict(redak)
    for stupac in rd.PRAZNI_STUPCI:
        if stupac in novi:
            novi[stupac] = None
    novi["anonymized_at"] = anonymized_at
    return novi


def test_nadgrobni_redak_cuva_lanac():
    import audit_chain as ac

    redci = _lanac(5)
    redci[0] = _u_nadgrobni(redci[0])
    redci[1] = _u_nadgrobni(redci[1])
    assert ac.verify_chain_retention_aware(redci) == (True, None, None)


def test_stara_verify_chain_puca_na_nadgrobnom_retku():
    """Dokumentira zasto postoji nova funkcija.

    Stara verify_chain ne poznaje nadgrobne retke i na praznim hesevima ne vrati
    ni (False, indeks), nego digne TypeError iz build_chain_link. Ostavljena je
    nepromijenjena zbog zatecenih poziva; sve nove provjere idu kroz
    verify_chain_retention_aware.
    """
    import audit_chain as ac

    redci = _lanac(3)
    redci[0] = _u_nadgrobni(redci[0])
    with pytest.raises(TypeError):
        ac.verify_chain(redci)


def test_redak_od_prije_k1_se_preskace():
    """Zivi redak bez ijednog hesa nikad nije bio u lancu (0007_audit_chain.sql),
    pa ne smije rusiti provjeru ni javljati laznu uzbunu."""
    import audit_chain as ac

    redci = _lanac(2)
    prije_k1 = {
        "input_canonical_hash": None,
        "output_sha256": None,
        "generator_version_hash": None,
        "parent_hash": None,
        "current_hash": None,
        "input_schema_version": None,
        "anonymized_at": None,
    }
    assert ac.verify_chain_retention_aware([prije_k1] + redci) == (True, None, None)


def test_redak_od_prije_k1_izmedju_karika_ne_lomi_lanac():
    import audit_chain as ac

    redci = _lanac(3)
    prije_k1 = {
        "input_canonical_hash": None,
        "output_sha256": None,
        "generator_version_hash": None,
        "parent_hash": None,
        "current_hash": None,
        "input_schema_version": None,
        "anonymized_at": None,
    }
    izmijesano = [redci[0], prije_k1, redci[1], redci[2]]
    assert ac.verify_chain_retention_aware(izmijesano) == (True, None, None)


def test_mutacija_zivog_retka_i_dalje_se_hvata():
    import audit_chain as ac

    redci = _lanac(4)
    redci[0] = _u_nadgrobni(redci[0])
    redci[2]["output_sha256"] = "9" * 64
    u_redu, indeks, razlog = ac.verify_chain_retention_aware(redci)
    assert u_redu is False
    assert indeks == 2
    assert razlog == "mutacija"


def test_nadgrobni_redak_se_ne_prijavljuje_kao_mutacija():
    import audit_chain as ac

    redci = _lanac(3)
    nadgrobni = _u_nadgrobni(redci[1])
    assert ac.je_nadgrobni(nadgrobni)
    redci[1] = nadgrobni
    assert ac.verify_chain_retention_aware(redci)[0] is True


def test_tvrdo_obrisan_prethodnik_daje_prekinutu_vezu():
    """Bez nadgrobnog retka veza vodi u prazno; upit u bazu to potvrdjuje."""
    import audit_chain as ac

    redci = _lanac(4)
    preostali = redci[1:]
    u_redu, indeks, razlog = ac.verify_chain_retention_aware(
        preostali, parent_postoji=lambda hes: False
    )
    assert u_redu is False
    assert indeks == 0
    assert razlog == "prekinuta_veza"


def test_anonimiziran_prethodnik_izvan_liste_prolazi_uz_upit():
    """Dohvat po korisniku ne vraca nadgrobne retke (nemaju user_id), pa prvi
    redak redovito ima roditelja izvan liste. To nije kvar."""
    import audit_chain as ac

    redci = _lanac(4)
    postojeci = {r["current_hash"] for r in redci}
    preostali = redci[1:]
    assert ac.verify_chain_retention_aware(
        preostali, parent_postoji=lambda hes: hes in postojeci
    ) == (True, None, None)


def test_bez_upita_korijen_s_roditeljem_nije_potvrdjen():
    import audit_chain as ac

    redci = _lanac(3)[1:]
    u_redu, indeks, razlog = ac.verify_chain_retention_aware(redci)
    assert u_redu is False
    assert indeks == 0
    assert razlog == "nepoznat_korijen"


def test_rupa_u_sredini_liste_kad_redak_postoji_u_bazi():
    import audit_chain as ac

    redci = _lanac(4)
    postojeci = {r["current_hash"] for r in redci}
    bez_sredine = [redci[0], redci[2], redci[3]]
    u_redu, indeks, razlog = ac.verify_chain_retention_aware(
        bez_sredine, parent_postoji=lambda hes: hes in postojeci
    )
    assert u_redu is False
    assert indeks == 1
    assert razlog == "nepotpun_prikaz"


def test_rupa_u_sredini_liste_kad_redak_ne_postoji():
    import audit_chain as ac

    redci = _lanac(4)
    bez_sredine = [redci[0], redci[2], redci[3]]
    u_redu, indeks, razlog = ac.verify_chain_retention_aware(
        bez_sredine, parent_postoji=lambda hes: False
    )
    assert u_redu is False
    assert indeks == 1
    assert razlog == "prekinuta_veza"


def test_nadgrobni_bez_heseva_prijavljuje_izgubljenu_kariku():
    import audit_chain as ac

    redci = _lanac(3)
    nadgrobni = _u_nadgrobni(redci[1])
    nadgrobni["current_hash"] = None
    redci[1] = nadgrobni
    u_redu, indeks, razlog = ac.verify_chain_retention_aware(redci)
    assert u_redu is False
    assert indeks == 1
    assert razlog == "nadgrobni_bez_hesa"


def test_geneza_bez_roditelja_prolazi_bez_upita():
    import audit_chain as ac

    assert ac.verify_chain_retention_aware(_lanac(3)) == (True, None, None)


def test_prazna_lista_nema_sto_oboriti():
    import audit_chain as ac

    assert ac.verify_chain_retention_aware([]) == (True, None, None)


# =============================================================================
# Sto provjera lanca NE moze, potvrdjeno testom
# =============================================================================


def test_rano_ispraznjen_redak_prolazi_bez_zadanog_roka():
    """Ovo je granica dosega, ne propust koji treba popraviti tiho.

    Nadgrobni redak se ne moze prerecunati, pa tko ima pravo pisanja moze bilo
    kojem retku obrisati sadrzaj i oznaciti ga kao anonimiziran. Bez zadanog
    roka provjera to prima kao zakonitu retenciju.
    """
    import audit_chain as ac

    redci = _lanac(4)
    redci[2] = _u_nadgrobni(redci[2], anonymized_at=_iso(POCETAK_LANCA + timedelta(days=5)))
    assert ac.verify_chain_retention_aware(redci) == (True, None, None)


def test_rano_ispraznjen_redak_prijavljen_kad_je_rok_zadan():
    import audit_chain as ac

    redci = _lanac(4)
    redci[2] = _u_nadgrobni(redci[2], anonymized_at=_iso(POCETAK_LANCA + timedelta(days=5)))
    u_redu, indeks, razlog = ac.verify_chain_retention_aware(redci, mjeseci_retencije=24)
    assert u_redu is False
    assert indeks == 2
    assert razlog == "rana_anonimizacija"


def test_zakonita_retencija_ne_pada_u_ranu_anonimizaciju():
    """28 dana po mjesecu je donja ocjena; redak ispraznjen tocno na 730 dana
    mora proci, inace bi provjera prijavljivala vlastiti posao retencije."""
    import audit_chain as ac

    redci = _lanac(3)
    for i in (0, 1):
        redci[i] = _u_nadgrobni(
            redci[i],
            anonymized_at=_iso(POCETAK_LANCA + timedelta(days=730 + i)),
        )
    assert ac.verify_chain_retention_aware(redci, mjeseci_retencije=24) == (
        True,
        None,
        None,
    )


def test_neprepoznat_zapis_vremena_ne_rusi_provjeru():
    """Provjera lanca ne smije pasti zbog oblika datuma koji ne razumije."""
    import audit_chain as ac

    redci = _lanac(3)
    redci[1] = _u_nadgrobni(redci[1], anonymized_at="nije datum")
    assert ac.verify_chain_retention_aware(redci, mjeseci_retencije=24) == (
        True,
        None,
        None,
    )


def test_oblik_s_z_na_kraju_se_cita():
    """PostgREST zna vratiti i '...Z'; Python 3.9 fromisoformat to ne prima."""
    import audit_chain as ac

    redci = _lanac(3)
    redci[1] = _u_nadgrobni(redci[1], anonymized_at="2024-01-08T12:00:00Z")
    u_redu, _, razlog = ac.verify_chain_retention_aware(redci, mjeseci_retencije=24)
    assert u_redu is False
    assert razlog == "rana_anonimizacija"


def test_rls_pogled_korisnika_daje_laznu_uzbunu():
    """Zabiljezeno ponasanje, ne zeljeno.

    Zastita na razini retka je `user_id = auth.uid()`, a nadgrobni redak nema
    user_id. Implementacija parent_postoji preko korisnickog kljuca zato ne vidi
    anonimiziranog prethodnika i provjera javi prekinutu vezu. Radi ispravno
    samo sa servisnim kljucem; zato to pise u opisu funkcije.
    """
    import audit_chain as ac

    redci = _lanac(4)
    redci[0] = _u_nadgrobni(redci[0])
    dohvat_korisnika = redci[1:]  # nadgrobni ispada, nema user_id

    vidljivo_korisniku = {r["current_hash"] for r in dohvat_korisnika}
    assert ac.verify_chain_retention_aware(
        dohvat_korisnika, parent_postoji=lambda h: h in vidljivo_korisniku
    ) == (False, 0, "prekinuta_veza")

    vidljivo_servisu = {r["current_hash"] for r in redci}
    assert ac.verify_chain_retention_aware(
        dohvat_korisnika, parent_postoji=lambda h: h in vidljivo_servisu
    ) == (True, None, None)
