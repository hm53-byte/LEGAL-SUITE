"""Operacije koje dijele MCP poslužitelj i CLI. Svaka vraća običan rječnik spreman za JSON."""

from __future__ import annotations

import re

from pristup.generiranje import GreskaUnosa, generiraj, nadji
from pristup.katalog import trazi

UPUTA = (
    "LegalTechSuite Pro sastavlja hrvatske pravne dokumente (tužbe, ovrhe, žalbe, ugovore, zemljišnoknjižne "
    "prijedloge, opomene, punomoći, trgovačke i obiteljske isprave) deterministički iz zadanih polja; nema jezičnog "
    "modela ni pravnog savjeta. Postupak: 1) katalog (po potrebi s upitom) za izbor dokumenta; 2) opis_dokumenta za "
    "polja i primjer koji prolazi; 3) generiraj_dokument s vrijednostima iz korisnikova slučaja; 4) pročitaj vraćeni "
    "tekst i popis praznina i provjeri ga s korisnikom; 5) korisniku daj poveznicu na .docx. Stranke se zadaju kao "
    "objekt {tip:'fizicka', ime, oib, adresa} ili {tip:'pravna', tvrtka, oib, mbs, sjediste, zastupnik}; datumi kao "
    "2026-01-15; iznosi kao broj u eurima. OIB provjeri alatom provjeri_oib, sud nađi alatom sudovi, pristojbu "
    "izračunaj alatom pristojba. Za odluku o pravnom putu i rokovima korisnik se treba posavjetovati s odvjetnikom."
)

_PRAZNINA = re.compile(r"_{4,}|\[[^\]\n]{1,60}\]")


def katalog(upit: str = "", podrucje: str = "") -> dict:
    docs = trazi(upit, podrucje)
    return {"broj": len(docs),
            "dokumenti": [{"oznaka": d.oznaka, "podrucje": d.podrucje, "naziv": d.naziv} for d in docs]}


def opis(oznaka: str) -> dict:
    return nadji(oznaka).kao_rjecnik()


def praznine(tekst: str) -> list[str]:
    """Mjesta koja su ostala nepopunjena (____ ili [polje]) s malo okolnog teksta."""
    van = []
    for m in _PRAZNINA.finditer(tekst):
        a, b = max(0, m.start() - 40), min(len(tekst), m.end() + 20)
        van.append(" ".join(tekst[a:b].split()))
        if len(van) >= 40:
            break
    return van


def sastavi(oznaka: str, argumenti: dict | None = None, *, popuni_primjerom: bool = False) -> tuple[dict, object]:
    """Generira dokument; vraća (sažetak za pozivatelja, Rezultat za izvoz .docx)."""
    r = generiraj(oznaka, argumenti, popuni_primjerom=popuni_primjerom)
    return {"oznaka": r.dokument.oznaka, "naziv": r.dokument.naziv, "datoteka": r.naziv_datoteke,
            "tekst": r.tekst, "praznine": praznine(r.tekst)}, r


def provjeri_oib(oib: str) -> dict:
    from pomocne import _validiraj_oib

    ok, poruka = _validiraj_oib(str(oib or ""))
    return {"oib": str(oib or "").strip(), "ispravan": ok, "poruka": poruka or ("OIB je ispravan." if ok else "")}


VRSTE_PRISTOJBE = ["tuzba", "presuda", "zalba", "revizija", "ovrha_jb", "ovrha_ovrsna", "prigovor_ovrhe",
                   "zk_prijedlog", "zk_brisanje", "zk_izvadak", "upravni_spor", "punomoc", "zalba_zup"]


def pristojba(vrsta: str, vrijednost_predmeta: float = 0.0) -> dict:
    from pristojbe import izracunaj_pristojbu, odvjetnicka_nagrada_sastav

    if vrsta not in VRSTE_PRISTOJBE:
        raise GreskaUnosa(f"Vrsta pristojbe mora biti jedno od: {', '.join(VRSTE_PRISTOJBE)}.")
    van = {"vrsta": vrsta, "vrijednost_predmeta": vrijednost_predmeta,
           "pristojba_eur": izracunaj_pristojbu(vrsta, float(vrijednost_predmeta or 0)),
           "izvor": "Zakon o sudskim pristojbama i Uredba o tarifi sudskih pristojbi (NN 118/18)"}
    if vrijednost_predmeta:
        van["odvjetnicka_nagrada_sastav_eur"] = odvjetnicka_nagrada_sastav(float(vrijednost_predmeta))
    return van


def sudovi(vrsta: str = "", upit: str = "") -> dict:
    from sudovi import SUDOVI, format_sud_s_dijakriticima

    rijeci = [r for r in upit.upper().replace("Č", "C").replace("Ć", "C").replace("Đ", "D").replace("Š", "S")
              .replace("Ž", "Z").split() if r]
    van = []
    for naziv, d in sorted(SUDOVI.items()):
        if vrsta and d.get("vrsta") != vrsta:
            continue
        if rijeci and not all(r in f"{naziv} {d.get('grad', '')}".upper() for r in rijeci):
            continue
        van.append({"naziv": format_sud_s_dijakriticima(naziv), "vrsta": d.get("vrsta"), "grad": d.get("grad"),
                    "adresa": d.get("adresa")})
    return {"broj": len(van), "sudovi": van}


def klauzule(kategorija: str = "") -> dict:
    from klauzule import KATEGORIJE, dohvati_klauzule

    return {"kategorije": KATEGORIJE, "klauzule": dohvati_klauzule(kategorija or None)}
