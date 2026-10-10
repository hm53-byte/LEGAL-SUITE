"""Generiranje dokumenta iz argumenata zadanih izvana (MCP, CLI): stranke kao objekti, ostalo kao JSON.

Aplikacija ostaje deterministicko popunjavanje obrazaca: ovdje nema jezicnog modela. Tko zove (covjek kroz CLI
ili Claude kroz MCP) sam bira dokument i vrijednosti polja.

Sigurnost unosa: generatori umecu dio vrijednosti u HTML bez escapea (forme ih escapeaju prije poziva), pa se
ovdje u svakom tekstu iz vana znakovi < i > zamjenjuju s ‹ i › (generatori koji koriste format_text dodatno
escapeaju &, pa se & ne dira da ne nastane &amp;amp;). Blok stranke slaze se istim oblikom kao pomocne.unos_stranke.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import date, datetime
from html.parser import HTMLParser

from pristup.katalog import Dokument, dokumenti


class GreskaUnosa(ValueError):
    """Neispravan zahtjev: nepoznat dokument, nedostaje obavezno polje, kriva vrsta vrijednosti."""


def _ocisti(v):
    if isinstance(v, str):
        return v.replace("<", "‹").replace(">", "›")
    if isinstance(v, dict):
        return {k: _ocisti(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_ocisti(x) for x in v]
    return v


def stranka_html(s) -> str:
    """Objekt stranke -> blok kakav vraca pomocne.unos_stranke. Tekst se prihvaca i escapea (novi red -> <br>)."""
    e = lambda x: html.escape(str(x or ""))
    if isinstance(s, str):
        return e(s).replace("\n", "<br>")
    if not isinstance(s, dict):
        raise GreskaUnosa("Stranka se zadaje kao objekt {tip, ime, oib, adresa} ili {tip: 'pravna', tvrtka, oib, mbs, sjediste, zastupnik}.")
    if (s.get("tip") or "fizicka").lower().startswith("prav") or s.get("tvrtka"):
        return (f"<b>{e(s.get('tvrtka'))}</b><br>Sjedište: {e(s.get('sjediste'))}<br>"
                f"OIB: {e(s.get('oib'))}, MBS: {e(s.get('mbs'))}<br>"
                f"Zastupana po: {e(s.get('zastupnik'))}")
    return f"<b>{e(s.get('ime'))}</b><br>Adresa: {e(s.get('adresa'))}<br>OIB: {e(s.get('oib'))}"


def zastupanje_html(z) -> str:
    """Ime punomocnika -> redak kakav vraca pomocne.zaglavlje_sastavljaca; prazno ostaje prazno."""
    if not z:
        return ""
    if isinstance(z, str) and z.lstrip().startswith("<br>"):
        return z
    return f"<br>Zastupan po punomoćniku: {html.escape(str(z))}<br>"


def u_datum(v, ime: str):
    """'2026-01-15', '15.01.2026.' ili '15.1.2026' -> date; prazno -> None."""
    if v in (None, ""):
        return None
    if isinstance(v, date):
        return v
    t = str(v).strip().rstrip(".")
    for oblik in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(t, oblik).date()
        except ValueError:
            pass
    raise GreskaUnosa(f"'{ime}' mora biti datum (2026-01-15 ili 15.01.2026.), a ne '{v}'.")


class _Tekst(HTMLParser):
    BLOK = {"div", "p", "br", "tr", "li", "h1", "h2", "h3", "table"}

    def __init__(self):
        super().__init__()
        self.dijelovi: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.BLOK:
            self.dijelovi.append("\n")

    def handle_endtag(self, tag):
        if tag in self.BLOK:
            self.dijelovi.append("\n")

    def handle_data(self, data):
        self.dijelovi.append(data)


def html_u_tekst(h: str) -> str:
    p = _Tekst()
    p.feed(h)
    t = "".join(p.dijelovi)
    t = re.sub(r"[ \t]+\n", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


@dataclass
class Rezultat:
    dokument: Dokument
    html: str
    tekst: str
    argumenti: dict

    def docx(self, *, nacrt: bool = False) -> bytes:
        from docx_export import pripremi_za_docx

        return pripremi_za_docx(self.html, watermark="NACRT" if nacrt else None,
                                doc_type=self.dokument.oznaka.replace("/", "_"), plan="free")

    @property
    def naziv_datoteke(self) -> str:
        return re.sub(r"[^A-Za-z0-9_]+", "_", self.dokument.oznaka.replace("/", "_")).strip("_") + ".docx"


def nadji(oznaka: str) -> Dokument:
    d = dokumenti().get((oznaka or "").strip())
    if d is None:
        raise GreskaUnosa(f"Nepoznat dokument '{oznaka}'. Popis daje alat katalog (CLI: katalog).")
    return d


def generiraj(oznaka: str, argumenti: dict | None = None, *, popuni_primjerom: bool = False) -> Rezultat:
    """Slozi argumente po katalogu i pozove generator. popuni_primjerom=True nadopuni nezadana polja primjerom."""
    d = nadji(oznaka)
    argumenti = dict(argumenti or {})
    nepoznati = set(argumenti) - {p.ime for p in d.parametri}
    if nepoznati:
        raise GreskaUnosa(f"Dokument {oznaka} nema parametre: {', '.join(sorted(nepoznati))}.")
    pozivni = {}
    for p in d.parametri:
        if p.ime in argumenti:
            v = argumenti[p.ime]
        elif popuni_primjerom and p.ime in d.primjer:
            v = d.primjer[p.ime]
        elif p.obavezan:
            raise GreskaUnosa(f"Dokument {oznaka} traži parametar '{p.ime}' ({p.vrsta}).")
        else:
            continue
        if v is None and not p.obavezan:
            pozivni[p.ime] = None
            continue
        if p.vrsta == "stranka":
            v = stranka_html(_ocisti(v))
        elif p.ime == "zastupanje":
            v = zastupanje_html(_ocisti(v))
        elif p.vrsta == "objekt":
            if not isinstance(v, dict):
                raise GreskaUnosa(f"Parametar '{p.ime}' je objekt s ključevima: {', '.join(p.kljucevi) or '(slobodni)'}.")
            if popuni_primjerom and isinstance(d.primjer.get(p.ime), dict):
                v = {**d.primjer[p.ime], **v}
            v = _ocisti(v)
            for k in p.datumski:
                if k in v:
                    v[k] = u_datum(v[k], f"{p.ime}.{k}")
        elif p.vrsta == "datum":
            v = u_datum(v, p.ime)
        elif p.vrsta == "izbor" and p.izbori and v not in p.izbori:
            raise GreskaUnosa(f"'{p.ime}' mora biti jedno od: {', '.join(p.izbori)}.")
        elif p.vrsta == "popis":
            if not isinstance(v, list):
                raise GreskaUnosa(f"Parametar '{p.ime}' je popis.")
            v = _ocisti(v)
        else:
            v = _ocisti(v)
        pozivni[p.ime] = v
    try:
        h = d.fn()(**pozivni)
    except (KeyError, TypeError, ValueError, AttributeError) as e:
        raise GreskaUnosa(f"Generator {oznaka} nije prihvatio unos: {type(e).__name__}: {e}") from None
    if not isinstance(h, str):
        raise GreskaUnosa(f"Generator {oznaka} nije vratio dokument.")
    if "Greška pri generiranju" in h[:300]:
        raise GreskaUnosa(f"Generator {oznaka} javlja grešku: {html_u_tekst(h)}")
    return Rezultat(d, h, html_u_tekst(h), pozivni)
