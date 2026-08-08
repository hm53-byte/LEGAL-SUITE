"""Retencija download_loga preko PostgREST-a, pricuva za slucaj bez pg_cron.

Radi isto sto i SQL funkcija download_log_anonimiziraj() iz
cloud/0008_retencija_download_log.sql: redke starije od 24 mjeseca ne brise,
nego im prazni osobne stupce i ostavlja generated_at, parent_hash i
current_hash, da veza u lancu heseva ostane cjelovita.

Zasto REST, a ne poziv te SQL funkcije preko RPC-a: ovako je posao neovisan o
tome je li vlasnik uspio dobiti prava na shemu cron i na EXECUTE, a suhi hod
moze ispisati sto bi tocno dirao. Pravilo je na dva mjesta, pa je usporedba
uvjeta (anonymized_at IS NULL AND generated_at <= granica) obavezna pri svakoj
izmjeni jednoga od njih.

Trazi dvije varijable okoline:
    SUPABASE_URL                npr. https://xxxx.supabase.co
    SUPABASE_SERVICE_ROLE_KEY   service_role kljuc, NIKAD anon

Service_role je nuzan: download_log ima RLS bez politike za UPDATE, pa anon
kljuc i korisnicki JWT ne mogu mijenjati retke. Zbog toga ovaj kljuc ne smije
zavrsiti u Streamlit secrets ni u repozitoriju.

Pokretanje (suhi hod je zadano stanje, nista se ne mijenja bez --izvrsi):

    python -m scripts.retencija_download_log
    python -m scripts.retencija_download_log --izvrsi
    python -m scripts.retencija_download_log --mjeseci 24 --izvrsi

Primjer za obicni cron, svaki dan u 03:17:

    17 3 * * * cd /put/do/LEGAL-SUITE && SUPABASE_URL=... \\
      SUPABASE_SERVICE_ROLE_KEY=... /put/do/python \\
      -m scripts.retencija_download_log --izvrsi >> /var/log/retencija.log 2>&1

Izlazni kodovi:
    0  gotovo (ukljucujuci suhi hod i slucaj bez redaka za obradu)
    2  nije podeseno, posao odbijen
    3  greska u komunikaciji sa Supabaseom (ukljucujuci prekid mreze i istek
       vremena; vidi napomenu o dvojbenom ishodu nize)
    4  neispravan argument

DVOJBEN ISHOD. Pisanje je jedan PATCH, dakle jedan UPDATE u jednoj transakciji:
ili prodje sav ili nijedan redak, pa djelomicno ispraznjena tablica nije moguca.
Ali ako se veza prekine nakon sto je poslani zahtjev vec izvrsen, klijent vidi
gresku i vraca 3, a redci su ipak ispraznjeni. Suprotno se ne dogadja. Zato kod
3 znaci "ne znam je li prošlo", ne "nije proslo": provjeri upitom iz koraka 5 u
docs/brisanje_podataka.md. Ponovno pokretanje je bezopasno jer uvjet
anonymized_at IS NULL preskace vec obradjene retke.
"""
from __future__ import annotations

import argparse
import base64
import calendar
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Callable, Iterable

import requests


RETENCIJA_MJESECI = 24
"""Rok iz stranice/privacy_policy.md, tablica u tocki 7. Mijenja se zajedno s
politikom privatnosti i sa SQL funkcijom, nikad samo ovdje."""

TABLICA = "download_log"

PRAZNI_STUPCI: dict[str, None] = {
    "user_id": None,
    "doc_type": None,
    "doc_subtype": None,
    "serial_hash": None,
    "plan_at_download": None,
    "input_canonical_hash": None,
    "output_sha256": None,
    "generator_version_hash": None,
    "input_schema_version": None,
}
"""Stupci koji se prazne. Popis mora biti identican onome u SQL funkciji, inace
CHECK download_log_zivi_ili_nadgrobni odbije upis i posao stane s greskom.

parent_hash, current_hash i generated_at namjerno NISU na popisu: bez njih
sljedeci redak u lancu ostaje bez roditelja i provjera ga ne moze razlikovati
od krivotvorine."""


class Nepodeseno(RuntimeError):
    """Nedostaje ili je neispravna konfiguracija; posao se ne smije pokrenuti."""


class GreskaRest(RuntimeError):
    """Supabase nije odgovorio kako treba."""


# =============================================================================
# Racun granice
# =============================================================================


def oduzmi_mjesece(trenutak: datetime, mjeseci: int) -> datetime:
    """Oduzmi kalendarske mjesece, uz podrezivanje dana na zadnji dan mjeseca.

    Ponasa se kao Postgresov `now() - make_interval(months => n)`, koji takodjer
    podrezuje: 31.03. minus 1 mjesec daje 28.02. (ili 29.02. u prijestupnoj).
    Bez toga bi Python i SQL put obradjivali razlicite skupove redaka na kraju
    mjeseca. `dateutil` se ne koristi jer nije medju ovisnostima projekta.

    PREDUVJET ZA POKLAPANJE SA SQL-om: baza mora imati `TimeZone = 'UTC'` (to je
    zadano u Supabaseu). Postgres racuna `timestamptz - interval` s mjesecima u
    lokalnom vremenu sesije, a ovdje se racuna u UTC-u. Za rok koji je visekratnik
    12 mjeseci razlike nema ni u zoni s ljetnim racunanjem vremena, jer su obje
    tocke iste godisnje dobe; za `--mjeseci 6` ili 18 u zoni tipa Europe/Zagreb
    granice se mogu razici za sat vremena. Provjeri s `SHOW TimeZone;` ako
    mijenjas rok na broj koji nije visekratnik 12.

    PRIJESTUPNI DAN: redak od 29.02.2024. ne uhvati se 28.02.2026. (podrezivanje
    daje granicu 28.02.2024.), nego tek 01.03.2026., dakle 731 dan umjesto 730.
    Isto radi i SQL, pa se dva puta ne razilaze, ali to je jedini slucaj u kojem
    se rok probija za jedan dan umjesto da se skrati. Vidi
    tests/test_retencija.py::test_prijestupni_dan_kasni_jedan_dan.
    """
    if mjeseci < 0:
        raise ValueError("mjeseci ne smije biti negativan")
    ukupno = trenutak.year * 12 + (trenutak.month - 1) - mjeseci
    godina, mjesec0 = divmod(ukupno, 12)
    mjesec = mjesec0 + 1
    zadnji_dan = calendar.monthrange(godina, mjesec)[1]
    return trenutak.replace(
        year=godina, month=mjesec, day=min(trenutak.day, zadnji_dan)
    )


def u_utc(trenutak: datetime) -> datetime:
    """Naivan trenutak tumaci se kao UTC; generated_at je TIMESTAMPTZ."""
    if trenutak.tzinfo is None:
        return trenutak.replace(tzinfo=timezone.utc)
    return trenutak.astimezone(timezone.utc)


def granica_iso(sada: datetime, mjeseci: int = RETENCIJA_MJESECI) -> str:
    """Najkasniji generated_at koji se jos obradjuje, u ISO 8601 zapisu.

    Granica je ukljuciva: usporedba je `generated_at <= granica`, pa se redak
    star tocno `mjeseci` obradjuje. Obecani rok je gornja granica cuvanja, pa
    dvojba ide u korist ranijeg brisanja (GDPR cl. 5 st. 1 t. (e)).
    """
    return u_utc(oduzmi_mjesece(u_utc(sada), mjeseci)).isoformat()


# =============================================================================
# Konfiguracija
# =============================================================================


def _uloga_iz_kljuca(kljuc: str) -> str | None:
    """Procitaj claim `role` iz Supabase JWT kljuca; None ako to nije JWT.

    Noviji Supabase kljucevi (sb_secret_...) nisu JWT, pa None znaci samo
    "ne mogu procitati", nikad "nije ispravan".
    """
    dijelovi = kljuc.split(".")
    if len(dijelovi) != 3:
        return None
    tijelo = dijelovi[1]
    tijelo += "=" * (-len(tijelo) % 4)
    try:
        podaci = json.loads(base64.urlsafe_b64decode(tijelo).decode("utf-8"))
    except Exception:
        return None
    uloga = podaci.get("role")
    return uloga if isinstance(uloga, str) else None


def ucitaj_konfiguraciju(okolina: dict[str, str] | None = None) -> tuple[str, str]:
    """Vrati (url, service_role_kljuc) ili baci Nepodeseno s uputom sto nedostaje."""
    okolina = os.environ if okolina is None else okolina
    url = (okolina.get("SUPABASE_URL") or "").strip()
    kljuc = (okolina.get("SUPABASE_SERVICE_ROLE_KEY") or "").strip()

    nedostaje = []
    if not url:
        nedostaje.append("SUPABASE_URL")
    if not kljuc:
        nedostaje.append("SUPABASE_SERVICE_ROLE_KEY")
    if nedostaje:
        raise Nepodeseno(
            "Nedostaje varijabla okoline: "
            + ", ".join(nedostaje)
            + ". Posao nije pokrenut. Postavi obje varijable pa pokusaj ponovno; "
            "SUPABASE_SERVICE_ROLE_KEY je service_role kljuc iz Supabase "
            "Dashboarda (Project Settings -> API), ne anon kljuc."
        )

    if not url.startswith(("http://", "https://")):
        raise Nepodeseno(
            "SUPABASE_URL mora poceti s http:// ili https:// (dobiveno: "
            + url[:40]
            + "). Posao nije pokrenut."
        )

    uloga = _uloga_iz_kljuca(kljuc)
    if uloga is not None and uloga != "service_role":
        raise Nepodeseno(
            "SUPABASE_SERVICE_ROLE_KEY nosi ulogu '"
            + uloga
            + "', a treba 'service_role'. S tom ulogom RLS ne dopusta izmjenu "
            "download_loga pa bi posao tiho obradio nula redaka. Posao nije "
            "pokrenut."
        )

    return url, kljuc


# =============================================================================
# Sloj prema Supabaseu
# =============================================================================


def _broj_iz_content_range(zaglavlje: str | None) -> int:
    """PostgREST vraca ukupan broj u zaglavlju Content-Range, oblika '0-9/57'."""
    if not zaglavlje:
        raise GreskaRest("Supabase nije vratio Content-Range; broj redaka nepoznat.")
    if "/" not in zaglavlje:
        raise GreskaRest("Neocekivan Content-Range: " + str(zaglavlje))
    dio = zaglavlje.rsplit("/", 1)[-1].strip()
    if not dio.isdigit():
        raise GreskaRest("Neocekivan Content-Range: " + str(zaglavlje))
    return int(dio)


class SupabaseRest:
    """Tanak sloj nad PostgREST-om. Testovi ga zamjenjuju laznim klijentom."""

    def __init__(self, url: str, kljuc: str, timeout: float = 15.0) -> None:
        self._url = url.rstrip("/") + "/rest/v1/" + TABLICA
        self._kljuc = kljuc
        self._timeout = timeout

    def _posalji(self, metoda: Callable[..., Any], **kw: Any) -> Any:
        """Pretvori svaki kvar mreze u GreskaRest.

        Bez ovoga prekid veze ili istek vremena izlazi iz procesa kao trag steka
        i izlazni kod 1, kojeg nema u tablici izlaznih kodova. Cron zapisuje
        traceback, a vlasnik nema nacin da razlikuje "nije radilo" od "ne znam".
        Iznimka se ne guta, njezin tekst ulazi u poruku.
        """
        try:
            return metoda(**kw)
        except requests.exceptions.RequestException as greska:
            raise GreskaRest(
                "Supabase nije dostupan (" + type(greska).__name__ + "): "
                + str(greska)[:200]
            ) from greska

    @staticmethod
    def _json(odgovor: Any) -> Any:
        """PostgREST u kvaru zna vratiti HTML ili prazno tijelo, ne JSON."""
        try:
            return odgovor.json()
        except ValueError as greska:
            raise GreskaRest(
                "Supabase nije vratio JSON: " + str(greska)[:200]
            ) from greska

    def _zaglavlja(self, dodatno: dict[str, str] | None = None) -> dict[str, str]:
        z = {
            "apikey": self._kljuc,
            "Authorization": "Bearer " + self._kljuc,
            "Accept": "application/json",
        }
        if dodatno:
            z.update(dodatno)
        return z

    @staticmethod
    def _filtri(granica: str) -> dict[str, str]:
        """Jedino mjesto gdje se gradi uvjet odabira.

        PostgREST bez filtra mijenja cijelu tablicu, pa se uvjet ne sastavlja
        na pozivnom mjestu nego ovdje, i provjerava prije svakog PATCH-a.
        """
        return {"generated_at": "lte." + granica, "anonymized_at": "is.null"}

    def _provjeri(self, odgovor: Any) -> None:
        if odgovor.status_code not in (200, 201, 204, 206):
            tijelo = (odgovor.text or "")[:300]
            raise GreskaRest(
                "Supabase HTTP " + str(odgovor.status_code) + ": " + tijelo
            )

    def prebroji(self, granica: str) -> int:
        params = dict(self._filtri(granica))
        params.update({"select": "id", "limit": "1"})
        odgovor = self._posalji(
            requests.get,
            url=self._url,
            headers=self._zaglavlja({"Prefer": "count=exact"}),
            params=params,
            timeout=self._timeout,
        )
        self._provjeri(odgovor)
        return _broj_iz_content_range(odgovor.headers.get("Content-Range"))

    def uzorak(self, granica: str, koliko: int) -> list[dict[str, Any]]:
        """Nekoliko najstarijih pogodjenih redaka za ispis u suhom hodu.

        Namjerno se ne dohvaca user_id ni serial_hash: ispis zavrsava u cron
        logu, koji je manje zasticen od baze, pa nema razloga da osobni podatak
        izadje iz nje.
        """
        params = dict(self._filtri(granica))
        params.update(
            {
                "select": "id,generated_at,doc_type",
                "order": "generated_at.asc",
                "limit": str(max(1, koliko)),
            }
        )
        odgovor = self._posalji(
            requests.get,
            url=self._url,
            headers=self._zaglavlja(),
            params=params,
            timeout=self._timeout,
        )
        self._provjeri(odgovor)
        podaci = self._json(odgovor)
        return podaci if isinstance(podaci, list) else []

    def anonimiziraj(self, granica: str, oznaka: str) -> int | None:
        """Isprazni pogodjene retke. Vraca broj obradjenih ili None ako ga
        PostgREST nije prijavio."""
        params = self._filtri(granica)
        if "generated_at" not in params or "anonymized_at" not in params:
            raise GreskaRest(
                "Odbijen PATCH bez oba filtra; bez njih bi se ispraznila "
                "cijela tablica."
            )
        tijelo: dict[str, Any] = dict(PRAZNI_STUPCI)
        # Vrijeme se uzima s klijenta jer PostgREST nema now() u tijelu zahtjeva.
        # Sluzi samo kao oznaka kad je posao radio, ne ulazi ni u jedan hes.
        tijelo["anonymized_at"] = oznaka
        odgovor = self._posalji(
            requests.patch,
            url=self._url,
            headers=self._zaglavlja(
                {
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal,count=exact",
                }
            ),
            params=params,
            json=tijelo,
            timeout=self._timeout,
        )
        self._provjeri(odgovor)
        zaglavlje = odgovor.headers.get("Content-Range")
        if not zaglavlje:
            return None
        return _broj_iz_content_range(zaglavlje)


# =============================================================================
# Posao
# =============================================================================


def pokreni(
    klijent: Any,
    mjeseci: int = RETENCIJA_MJESECI,
    izvrsi: bool = False,
    sada: datetime | None = None,
    velicina_uzorka: int = 10,
    ispis: Callable[[str], Any] = print,
) -> int:
    """Odradi jedan prolaz. Vraca izlazni kod procesa.

    `klijent` mora imati prebroji(granica), uzorak(granica, n) i
    anonimiziraj(granica, oznaka). Testovi ubacuju lazni klijent, pa se nijedan
    test ne oslanja na pravi Supabase.
    """
    # Gornja granica postoji jer bi veci broj odveo racun ispod godine 1 i
    # oduzmi_mjesece bi pukao s tragom steka umjesto s izlaznim kodom 4.
    # 1200 mjeseci je 100 godina; duljeg roka cuvanja nema.
    if (
        isinstance(mjeseci, bool)
        or not isinstance(mjeseci, int)
        or not 1 <= mjeseci <= 1200
    ):
        ispis(
            "Greska: broj mjeseci mora biti cijeli broj >= 1 i <= 1200, dobiveno: "
            + repr(mjeseci)
        )
        return 4

    sada = u_utc(sada or datetime.now(timezone.utc))
    granica = granica_iso(sada, mjeseci)

    ispis("Retencija download_loga")
    ispis("  sada:     " + sada.isoformat())
    ispis("  rok:      " + str(mjeseci) + " mjeseci")
    ispis("  granica:  generated_at <= " + granica + " (ukljucivo)")
    ispis("  nacin:    " + ("IZVRSENJE" if izvrsi else "SUHI HOD"))

    try:
        broj = klijent.prebroji(granica)
    except GreskaRest as greska:
        ispis("Greska: " + str(greska))
        return 3

    ispis("  pogodjeno redaka: " + str(broj))

    if broj == 0:
        ispis("Nema redaka za obradu. Kraj.")
        return 0

    try:
        redci = klijent.uzorak(granica, velicina_uzorka)
    except GreskaRest as greska:
        ispis("Greska: " + str(greska))
        return 3

    if redci:
        ispis("  najstariji pogodjeni (najvise " + str(velicina_uzorka) + "):")
        for redak in redci:
            ispis(
                "    "
                + str(redak.get("generated_at"))
                + "  "
                + str(redak.get("doc_type") or "?")
                + "  id="
                + str(redak.get("id", ""))[:8]
            )

    if not izvrsi:
        ispis(
            "SUHI HOD: nista nije promijenjeno. Za stvarnu obradu dodaj --izvrsi."
        )
        return 0

    try:
        obradjeno = klijent.anonimiziraj(granica, sada.isoformat())
    except GreskaRest as greska:
        ispis("Greska: " + str(greska))
        return 3

    if obradjeno is None:
        ispis("Obradjeno: broj nepoznat (Supabase nije vratio Content-Range).")
    else:
        ispis("Obradjeno redaka: " + str(obradjeno))
    ispis(
        "Ispraznjeni stupci: " + ", ".join(sorted(PRAZNI_STUPCI))
    )
    ispis(
        "Zadrzano radi lanca: generated_at, parent_hash, current_hash "
        "(vidi audit_chain.verify_chain_retention_aware)."
    )
    return 0


def _argumenti(argv: Iterable[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="retencija_download_log",
        description=(
            "Anonimizira retke download_loga starije od zadanog roka. "
            "Bez --izvrsi radi suhi hod i nista ne mijenja."
        ),
    )
    parser.add_argument(
        "--mjeseci",
        type=int,
        default=RETENCIJA_MJESECI,
        help="rok cuvanja u mjesecima (zadano: %(default)s)",
    )
    parser.add_argument(
        "--izvrsi",
        action="store_true",
        help="stvarno isprazni retke; bez ove zastavice je suhi hod",
    )
    parser.add_argument(
        "--suhi-hod",
        action="store_true",
        help="izricit suhi hod; suvisno jer je to zadano stanje, ali cini "
             "namjeru vidljivom u cron retku",
    )
    parser.add_argument(
        "--uzorak",
        type=int,
        default=10,
        help="koliko najstarijih redaka ispisati (zadano: %(default)s)",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def main(argv: Iterable[str] | None = None) -> int:
    args = _argumenti(argv)

    # Suhi hod pobjedjuje ako su navedene obje zastavice: kod posla koji brise
    # podatke sigurniji ishod ima prednost pred namjerom koju ne mozemo pogoditi.
    izvrsi = args.izvrsi and not args.suhi_hod

    try:
        url, kljuc = ucitaj_konfiguraciju()
    except Nepodeseno as greska:
        print(str(greska), file=sys.stderr)
        return 2

    return pokreni(
        SupabaseRest(url, kljuc),
        mjeseci=args.mjeseci,
        izvrsi=izvrsi,
        velicina_uzorka=args.uzorak,
    )


if __name__ == "__main__":
    sys.exit(main())
