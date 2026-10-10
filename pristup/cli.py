"""CLI za LegalTechSuite Pro: iste operacije kao MCP, iz naredbenog retka.

  python -m pristup.cli katalog [upit] [--podrucje ovrhe]
  python -m pristup.cli opis opomene/opomenu
  python -m pristup.cli primjer opomene/opomenu > ulaz.json         (argumenti koji prolaze, za uređivanje)
  python -m pristup.cli generiraj opomene/opomenu ulaz.json [-o opomena.docx] [--nacrt] [--tekst]
  python -m pristup.cli generiraj opomene/opomenu - < ulaz.json     (argumenti sa standardnog ulaza)
  python -m pristup.cli oib 12345678903
  python -m pristup.cli pristojba tuzba 5000
  python -m pristup.cli sudovi [upit] [--vrsta opcinski]
  python -m pristup.cli klauzule [kategorija]

Izlaz je JSON (UTF-8), osim --tekst koji ispiše tekst dokumenta. Izlazni kod 2 znači grešku unosa.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pristup import usluge
from pristup.generiranje import GreskaUnosa


def _ispis(d) -> None:
    sys.stdout.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")


def _ulaz(putanja: str) -> dict:
    tekst = sys.stdin.read() if putanja == "-" else Path(putanja).read_text(encoding="utf-8")
    d = json.loads(tekst or "{}")
    if not isinstance(d, dict):
        raise GreskaUnosa("Ulazni JSON mora biti objekt parametar -> vrijednost.")
    return d


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="legal-suite", description="LegalTechSuite Pro iz naredbenog retka")
    pod = ap.add_subparsers(dest="naredba", required=True)
    k = pod.add_parser("katalog"); k.add_argument("upit", nargs="*"); k.add_argument("--podrucje", default="")
    o = pod.add_parser("opis"); o.add_argument("oznaka")
    p = pod.add_parser("primjer"); p.add_argument("oznaka")
    g = pod.add_parser("generiraj"); g.add_argument("oznaka"); g.add_argument("ulaz", nargs="?", default="")
    g.add_argument("-o", "--izlaz", default=""); g.add_argument("--nacrt", action="store_true")
    g.add_argument("--tekst", action="store_true", help="ispiši tekst dokumenta umjesto JSON-a")
    g.add_argument("--popuni-primjerom", action="store_true")
    b = pod.add_parser("oib"); b.add_argument("oib")
    s = pod.add_parser("pristojba"); s.add_argument("vrsta"); s.add_argument("vrijednost", nargs="?", type=float, default=0.0)
    u = pod.add_parser("sudovi"); u.add_argument("upit", nargs="*"); u.add_argument("--vrsta", default="")
    c = pod.add_parser("klauzule"); c.add_argument("kategorija", nargs="?", default="")
    a = ap.parse_args(argv)
    try:
        if a.naredba == "katalog":
            _ispis(usluge.katalog(" ".join(a.upit), a.podrucje))
        elif a.naredba == "opis":
            _ispis(usluge.opis(a.oznaka))
        elif a.naredba == "primjer":
            _ispis(usluge.opis(a.oznaka)["primjer"])
        elif a.naredba == "generiraj":
            argumenti = _ulaz(a.ulaz) if a.ulaz else {}
            sazetak, rez = usluge.sastavi(a.oznaka, argumenti, popuni_primjerom=a.popuni_primjerom)
            izlaz = Path(a.izlaz or rez.naziv_datoteke)
            izlaz.write_bytes(rez.docx(nacrt=a.nacrt))
            sazetak["docx"] = str(izlaz.resolve())
            if a.tekst:
                sys.stdout.write(sazetak["tekst"] + "\n")
            else:
                _ispis(sazetak)
        elif a.naredba == "oib":
            _ispis(usluge.provjeri_oib(a.oib))
        elif a.naredba == "pristojba":
            _ispis(usluge.pristojba(a.vrsta, a.vrijednost))
        elif a.naredba == "sudovi":
            _ispis(usluge.sudovi(a.vrsta, " ".join(a.upit)))
        elif a.naredba == "klauzule":
            _ispis(usluge.klauzule(a.kategorija))
    except (GreskaUnosa, json.JSONDecodeError, OSError) as e:
        sys.stderr.write(f"greška: {e}\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
