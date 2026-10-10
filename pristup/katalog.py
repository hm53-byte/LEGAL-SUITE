"""Katalog generatora za vanjski pristup (MCP i CLI).

Svaki dokument je jedna funkcija generiraj_* u generatori/<podrucje>.py. Oznaka dokumenta je
"<podrucje>/<ime bez generiraj_>", npr. "opomene/opomenu". Katalog ne mijenja generatore: polja se citaju
iz potpisa funkcije i iz koda (podaci.get("kljuc", zadano) i podaci["kljuc"]), a primjer argumenata dolazi
iz pristup/primjeri.json (prvi uspjesan poziv iz testova) ili se slaze iz procitanih polja.
"""

from __future__ import annotations

import ast
import html
import importlib
import inspect
import json
import pkgutil
import re
import textwrap
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import generatori

PRIMJERI = Path(__file__).with_name("primjeri.json")

# argumenti koji su blok stranke (HTML iz pomocne.unos_stranke); u MCP-u i CLI-ju zadaju se kao objekt
IMENA_STRANAKA = {
    "vjerovnik", "duznik", "tuzitelj", "tuzenik", "ovrhovoditelj", "ovrsenik", "prodavatelj", "kupac",
    "najmodavac", "najmoprimac", "zakupodavac", "zakupnik", "darovatelj", "daroprimac", "zajmodavac",
    "zajmoprimac", "narucitelj", "izvodjac", "poslodavac", "radnik", "opunomocitelj", "punomocnik",
    "podnositelj", "zalitelj", "predlagatelj", "protustranka", "stranka", "osoba", "vlasnik", "drustvo",
    "osnivac", "cedent", "cesionar", "dužnik", "jamac", "zalozni_vjerovnik", "zalogodavac", "posrednik",
    "nalogodavac", "iznajmljivac", "gost", "brodar", "kupac_brodice", "prodavatelj_brodice", "uknjizeni",
    "predlagatelj_upisa", "protivnik", "okrivljenik", "ostecenik", "privatni_tuzitelj", "prijavitelj",
    "zalitelj_stranka", "dioničar", "clan", "prenositelj", "stjecatelj", "korisnik", "trgovac", "potrosac",
}

# nazivi za prikaz kad prvi redak docstringa nije naziv u nominativu (ili docstringa nema)
NAZIVI = {
    "apartmani/suglasnost_obitelji": "Suglasnost vlasnika nekretnine članu obitelji za iznajmljivanje turistima",
    "apartmani/suglasnost_suvlasnika": "Suglasnost suvlasnika nekretnine za pružanje ugostiteljskih usluga",
    "apartmani/zahtjev_kategorizacija": "Zahtjev za rješenje o razvrstavanju i kategorizaciji apartmana ili sobe",
    "apartmani/zahtjev_mtu": "Zahtjev za rješenje o minimalnim tehničkim uvjetima (MTU)",
    "kazneno/kaznenu_prijavu": "Kaznena prijava",
    "kazneno/privatnu_tuzbu": "Privatna kaznena tužba",
    "kazneno/zalbu_kaznena_presuda": "Žalba protiv kaznene presude",
    "nautika/kupoprodaju_brodice": "Ugovor o kupoprodaji brodice",
    "nautika/punomoc_prodaje_brodice": "Specijalna punomoć za prodaju brodice",
    "nautika/tabularnu_brodice": "Tabularna izjava za upis vlasništva brodice",
    "nautika/zalog_brodice": "Sporazum o zasnivanju založnog prava na brodici",
    "obiteljsko/bracni_ugovor": "Bračni ugovor (imovinski odnosi bračnih drugova)",
    "obiteljsko/roditeljsku_skrb": "Plan o zajedničkoj roditeljskoj skrbi",
    "obiteljsko/tuzbu_razvod": "Tužba za razvod braka",
    "obiteljsko/ugovor_uzdrzavanje": "Ugovor o uzdržavanju",
    "obvezno/predugovor": "Predugovor",
    "obvezno/raskid_kupoprodaje": "Izjava o raskidu kupoprodaje zbog neispunjenja",
    "obvezno/raskid_najma": "Otkaz ili raskid ugovora o najmu",
    "obvezno/raskid_ugovora_djelu": "Raskid ugovora o djelu voljom naručitelja",
    "opomene/opomenu": "Opomena pred tužbu ili pred ovrhu",
    "ovrhe/ovrhu_pro": "Prijedlog za ovrhu na temelju vjerodostojne isprave",
    "pokretnine/zalog_pokretnine": "Sporazum o zasnivanju založnog prava na pokretnini",
    "pokretnine/zalog_vozila": "Sporazum o zasnivanju založnog prava na motornom vozilu",
    "posrednik_najam/ugovor_upravljanje_bc": "Ugovor o upravljanju i osiguranju smještajnog kapaciteta",
    "potrosaci/prigovor_racunu": "Prigovor na iznos računa davatelju usluga",
    "potrosaci/prijavu_inspekciji": "Prijava Državnom inspektoratu protiv trgovca",
    "potrosaci/reklamaciju": "Reklamacija (pisani prigovor) trgovcu",
    "punomoci/punomoc": "Punomoć (opća ili posebna)",
    "trgovacko/prodaju_poduzeca": "Ugovor o prodaji poduzeća",
    "trgovacko/zalog_udjela": "Sporazum o zasnivanju založnog prava na poslovnom udjelu d.o.o.",
    "tuzbe/brisovnu_tuzbu": "Brisovna tužba (zemljišnoknjižna)",
    "tuzbe/tuzbu_pro": "Tužba (parnični postupak)",
    "ugovori/otkaz": "Otkaz ugovora o radu",
    "ugovori/potvrdu_o_zaposlenju": "Potvrda o zaposlenju",
    "ugovori/prilagodeni_ugovor": "Prilagođeni ugovor (vlastita struktura članaka)",
    "ugovori/ugovor_standard": "Ugovor iz predloška (kupoprodaja, najam ili zakup, djelo, zajam)",
    "upravno/prigovor_predstavku": "Prigovor ili predstavka na rad tijela državne uprave",
    "upravno/tuzbu_zus": "Tužba u upravnom sporu",
    "upravno/zahtjev_informacije": "Zahtjev za pristup informacijama",
    "upravno/zalbu_zup": "Žalba u upravnom postupku",
    "zalbe/zalbu_pro": "Žalba protiv presude (parnični postupak)",
    "zemljisne/brisanje_hipoteke": "Prijedlog za brisanje hipoteke",
    "zemljisne/brisovno_ocitovanje": "Brisovno očitovanje vjerovnika",
    "zemljisne/predbiježbu": "Prijedlog za predbilježbu",
    "zemljisne/punomoc_prodaje_nekretnine": "Specijalna punomoć za prodaju nekretnine",
    "zemljisne/tabularnu_doc": "Tabularna izjava (clausula intabulandi)",
    "zemljisne/upis_hipoteke": "Prijedlog za upis hipoteke",
    "zemljisne/upis_plodouzivanja": "Prijedlog za uknjižbu prava plodouživanja",
    "zemljisne/upis_sluznosti": "Prijedlog za upis služnosti",
    "zemljisne/zabilježbu": "Prijedlog za zabilježbu",
    "zemljisne/zk_prijedlog": "Zemljišnoknjižni prijedlog (uknjižba prava vlasništva)",
}


@dataclass
class Parametar:
    ime: str
    vrsta: str                       # stranka | objekt | popis | tekst | broj | datum | izbor | da_ne
    obavezan: bool
    zadano: object = None
    kljucevi: dict = field(default_factory=dict)   # za vrsta == "objekt": kljuc -> zadana vrijednost ili None
    datumski: list = field(default_factory=list)    # kljucevi objekta koji su datumi (zadaju se kao 2026-01-15)
    element: dict = field(default_factory=dict)     # za vrsta == "popis": kljucevi jednog elementa
    izbori: list = field(default_factory=list)      # za vrsta == "izbor": dopustene vrijednosti


@dataclass
class Dokument:
    oznaka: str
    podrucje: str
    funkcija: str
    naziv: str
    opis: str
    parametri: list
    primjer: dict
    primjer_iz_testa: bool

    def fn(self):
        mod = importlib.import_module(f"generatori.{self.podrucje}")
        return getattr(mod, self.funkcija)

    def kao_rjecnik(self, s_primjerom: bool = True) -> dict:
        d = {
            "oznaka": self.oznaka, "podrucje": self.podrucje, "naziv": self.naziv, "opis": self.opis,
            "parametri": [
                {"ime": p.ime, "vrsta": p.vrsta, "obavezan": p.obavezan,
                 **({"zadano": p.zadano} if not p.obavezan else {}),
                 **({"kljucevi": p.kljucevi} if p.kljucevi else {}),
                 **({"datumski_kljucevi": p.datumski} if p.datumski else {}),
                 **({"element": p.element} if p.element else {}),
                 **({"izbori": p.izbori} if p.izbori else {})}
                for p in self.parametri
            ],
        }
        if s_primjerom:
            d["primjer"] = self.primjer
            d["primjer_iz_testa"] = self.primjer_iz_testa
        return d


@dataclass
class Analiza:
    """Sto funkcija radi s jednim parametrom, procitano iz koda."""
    kljucevi: dict = field(default_factory=dict)       # x.get("k", zadano) / x["k"]
    datumski: set = field(default_factory=set)         # kljucevi na kojima se zove .strftime
    je_datum: bool = False                             # sam parametar.strftime(...)
    je_popis: bool = False                             # for e in parametar
    element: dict = field(default_factory=dict)        # kljucevi elementa popisa
    izbori: list = field(default_factory=list)         # rjecnik[parametar] nad rjecnikom iz koda

    def spoji(self, o: "Analiza") -> None:
        for k, v in o.kljucevi.items():
            self.kljucevi.setdefault(k, v)
        self.datumski |= o.datumski
        self.je_datum |= o.je_datum
        self.je_popis |= o.je_popis
        for k, v in o.element.items():
            self.element.setdefault(k, v)
        self.izbori = self.izbori or o.izbori


def _konst(cvor):
    try:
        return ast.literal_eval(cvor)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return None


def _stablo(fn):
    try:
        return ast.parse(textwrap.dedent(inspect.getsource(fn))).body[0]
    except (OSError, SyntaxError, IndexError, TypeError):
        return None


def _kljuc_citanja(c, ime: str):
    if (isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute) and c.func.attr == "get"
            and isinstance(c.func.value, ast.Name) and c.func.value.id == ime
            and c.args and isinstance(c.args[0], ast.Constant) and isinstance(c.args[0].value, str)):
        return c.args[0].value
    if (isinstance(c, ast.Subscript) and isinstance(c.value, ast.Name) and c.value.id == ime
            and isinstance(c.slice, ast.Constant) and isinstance(c.slice.value, str)):
        return c.slice.value
    return None


def _citanja(stablo, ime: str) -> tuple[dict, set]:
    """Kljucevi koje stablo cita s imena `ime` (sa zadanim vrijednostima) i kljucevi koji su datumi."""
    kljucevi, datumski, lokalni = {}, set(), {}
    for c in ast.walk(stablo):
        if isinstance(c, ast.Assign) and len(c.targets) == 1 and isinstance(c.targets[0], ast.Name):
            k = _kljuc_citanja(c.value, ime)
            if k:
                lokalni[c.targets[0].id] = k
    for c in ast.walk(stablo):
        k = _kljuc_citanja(c, ime)
        if k and k not in kljucevi:
            kljucevi[k] = _konst(c.args[1]) if isinstance(c, ast.Call) and len(c.args) > 1 else None
        if isinstance(c, ast.Attribute) and c.attr == "strftime":
            k = _kljuc_citanja(c.value, ime)
            if k:
                datumski.add(k)
            elif isinstance(c.value, ast.Name) and c.value.id in lokalni:
                datumski.add(lokalni[c.value.id])
    return kljucevi, datumski


def _analiziraj(fn, ime: str, dubina: int = 1) -> Analiza:
    """Analiza jednog parametra; prosljedjivanje pomocnoj funkciji (f(..., ime, ...)) prati se jednu razinu."""
    a = Analiza()
    stablo = _stablo(fn)
    if stablo is None:
        return a
    a.kljucevi, a.datumski = _citanja(stablo, ime)
    rjecnici = {c.targets[0].id: c.value for c in ast.walk(stablo)
                if isinstance(c, ast.Assign) and len(c.targets) == 1 and isinstance(c.targets[0], ast.Name)
                and isinstance(c.value, ast.Dict)}
    for c in ast.walk(stablo):
        if isinstance(c, ast.Attribute) and c.attr == "strftime" and isinstance(c.value, ast.Name) and c.value.id == ime:
            a.je_datum = True
        if isinstance(c, ast.For):
            it = c.iter
            if isinstance(it, ast.Call) and isinstance(it.func, ast.Name) and it.func.id == "enumerate" and it.args:
                it = it.args[0]
            if isinstance(it, ast.Name) and it.id == ime:
                a.je_popis = True
                cilj = c.target
                if isinstance(cilj, ast.Tuple) and cilj.elts:
                    cilj = cilj.elts[-1]
                if isinstance(cilj, ast.Name):
                    el, _ = _citanja(c, cilj.id)
                    a.element.update(el)
        if (isinstance(c, ast.Subscript) and isinstance(c.slice, ast.Name) and c.slice.id == ime
                and isinstance(c.value, ast.Name) and c.value.id in rjecnici):
            a.izbori = [_konst(k) for k in rjecnici[c.value.id].keys if isinstance(_konst(k), str)]
        if dubina and isinstance(c, ast.Call) and isinstance(c.func, ast.Name):
            for poz, arg in enumerate(c.args):
                if isinstance(arg, ast.Name) and arg.id == ime:
                    cilj = (getattr(fn, "__globals__", {}) or {}).get(c.func.id)
                    if inspect.isfunction(cilj):
                        imena = list(inspect.signature(cilj).parameters)
                        if poz < len(imena):
                            a.spoji(_analiziraj(cilj, imena[poz], dubina - 1))
    return a


def _vrsta(ime: str, primjer_vrijednost, a: Analiza) -> str:
    if a.je_datum:
        return "datum"
    if a.izbori:
        return "izbor"
    if a.je_popis or isinstance(primjer_vrijednost, list):
        return "popis"
    if isinstance(primjer_vrijednost, dict) or a.kljucevi:
        return "objekt"
    if ime in IMENA_STRANAKA or (isinstance(primjer_vrijednost, str) and primjer_vrijednost.startswith("<b>")):
        return "stranka"
    if isinstance(primjer_vrijednost, bool):
        return "da_ne"
    if isinstance(primjer_vrijednost, (int, float)):
        return "broj"
    return "tekst"


_NOVCANI = ("iznos", "glavnica", "cijena", "vrijednost", "stavka", "pdv", "kamata", "materijalni", "pristojba",
            "najamnina", "zakupnina", "kapara", "polog", "kapital", "temeljni", "nominal", "trazbina",
            "dug", "naknada", "osnovica")


def _vrijednost_kljuca(k: str, zadano, datumski: set):
    if zadano is not None:
        return zadano
    if k in datumski:
        return "2026-01-15"
    if any(s in k for s in _NOVCANI):
        return 1000.0
    if "datum" in k:
        return "15.01.2026."
    return f"[{k}]"


def _sintetiziraj(vrsta: str, ime: str, a: Analiza):
    """Primjer vrijednosti kad ga testovi ne daju; generator mora s njim proci (provjerava tests/test_pristup.py)."""
    if vrsta == "stranka":
        return {"tip": "fizicka", "ime": "Ivan Horvat", "oib": "12345678903", "adresa": "Ilica 1, Zagreb"}
    if vrsta == "objekt":
        return {k: _vrijednost_kljuca(k, z, a.datumski) for k, z in a.kljucevi.items()}
    if vrsta == "popis":
        if a.element:
            return [{k: _vrijednost_kljuca(k, z, set()) for k, z in a.element.items()}]
        return ["[stavka]"]
    if vrsta == "datum":
        return "2026-01-15"
    if vrsta == "izbor":
        return a.izbori[0]
    if vrsta == "broj":
        return 1000.0
    if ime == "zastupanje":
        return ""
    if ime == "sud":
        return "Općinski građanski sud u Zagrebu"
    return f"[{ime}]"


def _za_json(v):
    try:
        json.dumps(v)
        return v
    except TypeError:
        return str(v)


_STRANKA_FIZ = re.compile(r"^<b>(?P<ime>.*?)</b><br>Adresa: (?P<adresa>.*?)<br>OIB: (?P<oib>.*)$", re.S)
_STRANKA_PRAV = re.compile(r"^<b>(?P<tvrtka>.*?)</b><br>Sjedište: (?P<sjediste>.*?)<br>OIB: (?P<oib>.*?), "
                           r"MBS: (?P<mbs>.*?)<br>Zastupana po: (?P<zastupnik>.*)$", re.S)


def _za_prikaz(vrsta: str, ime: str, v):
    """Vrijednost iz testa u obliku koji vanjski pozivatelj zadaje: blok stranke -> objekt, zastupanje -> ime."""
    if vrsta == "stranka" and isinstance(v, str):
        m = _STRANKA_PRAV.match(v)
        if m:
            return {"tip": "pravna", **{k: html.unescape(x) for k, x in m.groupdict().items()}}
        m = _STRANKA_FIZ.match(v)
        if m:
            return {"tip": "fizicka", **{k: html.unescape(x) for k, x in m.groupdict().items()}}
        return html.unescape(re.sub(r"<br\s*/?>", "\n", re.sub(r"</?b>", "", v)))
    if ime == "zastupanje" and isinstance(v, str):
        m = re.search(r"punomoćniku: (.*?)<br>", v)
        return html.unescape(m.group(1)) if m else ""
    return v


@lru_cache(maxsize=1)
def dokumenti() -> dict[str, Dokument]:
    primjeri = json.loads(PRIMJERI.read_text(encoding="utf-8")) if PRIMJERI.exists() else {}
    van: dict[str, Dokument] = {}
    for m in sorted(pkgutil.iter_modules(generatori.__path__), key=lambda x: x.name):
        mod = importlib.import_module(f"generatori.{m.name}")
        for ime, fn in sorted(vars(mod).items()):
            fn = inspect.unwrap(fn) if callable(fn) else fn
            if not (ime.startswith("generiraj_") and inspect.isfunction(fn)
                    and getattr(fn, "__module__", "") == mod.__name__):
                continue
            oznaka = f"{m.name}/{ime[len('generiraj_'):]}"
            sig = inspect.signature(fn)
            pr = primjeri.get(oznaka, {})
            parametri, primjer = [], {}
            for p in sig.parameters.values():
                if p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
                    continue
                an = _analiziraj(fn, p.name)
                if isinstance(pr.get(p.name), dict):
                    for k in pr[p.name]:
                        an.kljucevi.setdefault(k, None)
                vrsta = _vrsta(p.name, pr.get(p.name, p.default if p.default is not p.empty else None), an)
                obavezan = p.default is p.empty
                parametri.append(Parametar(
                    p.name, vrsta, obavezan, None if obavezan else _za_json(p.default),
                    an.kljucevi if vrsta == "objekt" else {}, sorted(an.datumski) if vrsta == "objekt" else [],
                    an.element if vrsta == "popis" else {}, an.izbori if vrsta == "izbor" else []))
                if p.name in pr:
                    primjer[p.name] = _za_prikaz(vrsta, p.name, pr[p.name])
                elif obavezan:
                    primjer[p.name] = _sintetiziraj(vrsta, p.name, an)
            doc = inspect.getdoc(fn) or ""
            prvi = doc.strip().splitlines()[0] if doc.strip() else ""
            naziv = prvi.removeprefix("Generira ").rstrip(".") if prvi else ime[len("generiraj_"):].replace("_", " ")
            naziv = NAZIVI.get(oznaka) or naziv.split(" - ")[0].split(" — ")[0].strip()
            van[oznaka] = Dokument(oznaka, m.name, ime, naziv[:1].upper() + naziv[1:], doc, parametri, primjer,
                                   bool(pr))
    return van


_DIJAKRITIKA = str.maketrans("čćđšžČĆĐŠŽ", "ccdszCCDSZ")


def _normaliziraj(t: str) -> str:
    return t.lower().translate(_DIJAKRITIKA).replace("_", " ").replace("/", " ")


def _osnova(r: str) -> str:
    """Grubo skidanje padežnog nastavka: ovrha, ovrhu, ovrhe -> ovrh; žalba -> zalb."""
    r = _normaliziraj(r)
    for nastavak in ("ama", "ima", "om", "em", "u", "a", "e", "i", "o"):
        if len(r) > 4 and r.endswith(nastavak):
            return r[: -len(nastavak)]
    return r


def trazi(upit: str = "", podrucje: str = "") -> list[Dokument]:
    """Dokumenti kojima oznaka, naziv ili opis sadrže osnove svih riječi upita (bez dijakritika i nastavaka)."""
    osnove = [_osnova(r) for r in upit.split() if r.strip()]
    van = []
    for d in dokumenti().values():
        if podrucje and d.podrucje != podrucje:
            continue
        tekst = _normaliziraj(f"{d.oznaka} {d.naziv} {d.opis}")
        if all(o in tekst for o in osnove):
            van.append(d)
    return van
