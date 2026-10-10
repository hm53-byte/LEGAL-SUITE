"""MCP poslužitelj (Streamable HTTP) za LegalTechSuite Pro: Claude ili drugi MCP klijent preko poveznice
pretražuje katalog, sastavlja dokumente i preuzima .docx.

Pokretanje:  python -m pristup.mcp_posluzitelj            (127.0.0.1:8620, putanja /mcp)
Okolina:
  LEGAL_MCP_PORT        port (zadano 8620)
  LEGAL_JAVNA_ADRESA    javna osnova za poveznice na .docx, npr. https://<stroj>.ts.net/legal (zadano lokalna)
  LEGAL_MCP_SPREMISTE   mapa za privremene .docx (zadano .mcp_dokumenti uz repozitorij)
  LEGAL_MCP_ROK_SATI    koliko sati .docx ostaje dostupan (zadano 24)
  LEGAL_MCP_HOSTOVI     dodatni dopušteni Host zaglavlja, zarezom (uz 127.0.0.1 i localhost)

Osobni podaci: dokumenti sadrže podatke stranaka; .docx se čuva samo do isteka roka pod slučajnim tokenom,
a dnevnik bilježi samo naziv alata i oznaku dokumenta, nikad vrijednosti polja.
"""

from __future__ import annotations

import json
import logging
import os
import re
import secrets
import time
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, PlainTextResponse

from pristup import usluge
from pristup.generiranje import GreskaUnosa

log = logging.getLogger("legal_mcp")

KORIJEN = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("LEGAL_MCP_PORT", "8620"))
JAVNA = os.environ.get("LEGAL_JAVNA_ADRESA", f"http://127.0.0.1:{PORT}").rstrip("/")
SPREMISTE = Path(os.environ.get("LEGAL_MCP_SPREMISTE", KORIJEN / ".mcp_dokumenti"))
ROK_S = float(os.environ.get("LEGAL_MCP_ROK_SATI", "24")) * 3600
_TOKEN = re.compile(r"^[A-Za-z0-9_-]{20,64}$")


def _hostovi() -> list[str]:
    h = ["127.0.0.1", f"127.0.0.1:{PORT}", "localhost", f"localhost:{PORT}"]
    if JAVNA.startswith("https://"):
        h.append(JAVNA.split("/")[2])
    h += [x.strip() for x in os.environ.get("LEGAL_MCP_HOSTOVI", "").split(",") if x.strip()]
    return h


mcp = FastMCP(
    "LegalTechSuite Pro",
    instructions=usluge.UPUTA,
    host="127.0.0.1",
    port=PORT,
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=_hostovi(),
        allowed_origins=["https://claude.ai", "https://claude.com", f"http://127.0.0.1:{PORT}"],
    ),
)


def _greska(e: Exception) -> dict:
    return {"greska": str(e)}


def _pocisti() -> None:
    granica = time.time() - ROK_S
    for f in SPREMISTE.glob("*.docx"):
        try:
            if f.stat().st_mtime < granica:
                f.unlink(missing_ok=True)
                f.with_suffix(".json").unlink(missing_ok=True)
        except OSError:
            pass


def _spremi(sadrzaj: bytes, naziv: str) -> str:
    SPREMISTE.mkdir(parents=True, exist_ok=True)
    _pocisti()
    token = secrets.token_urlsafe(24)
    (SPREMISTE / f"{token}.docx").write_bytes(sadrzaj)
    (SPREMISTE / f"{token}.json").write_text(json.dumps({"naziv": naziv}), encoding="utf-8")
    return f"{JAVNA}/preuzmi/{token}"


@mcp.tool()
def katalog(upit: str = "", podrucje: str = "") -> dict:
    """Popis dokumenata koje aplikacija sastavlja (oznaka, područje, naziv).

    upit: riječi koje oznaka, naziv ili opis moraju sadržavati (npr. "ovrha nekretnina", "žalba", "najam");
    podrucje: ime modula (npr. ovrhe, tuzbe, ugovori, zemljisne, obvezno, trgovacko, obiteljsko, upravno, kazneno).
    Prazno vraća sve dokumente."""
    log.info("katalog")
    return usluge.katalog(upit, podrucje)


@mcp.tool()
def opis_dokumenta(oznaka: str) -> dict:
    """Polja jednog dokumenta: ime, vrsta (stranka, objekt, popis, tekst, broj, datum, izbor), obaveznost, ključevi
    objekata, datumski ključevi, dopušteni izbori i primjer argumenata koji prolazi. oznaka je iz kataloga,
    npr. "opomene/opomenu"."""
    log.info("opis_dokumenta %s", oznaka)
    try:
        return usluge.opis(oznaka)
    except GreskaUnosa as e:
        return _greska(e)


@mcp.tool()
def generiraj_dokument(oznaka: str, argumenti: dict[str, Any], popuni_primjerom: bool = False,
                       nacrt: bool = False) -> dict:
    """Sastavi dokument i vrati njegov tekst, popis nepopunjenih mjesta i poveznicu na .docx.

    argumenti: rječnik parametar -> vrijednost prema opis_dokumenta (stranke kao objekt, datumi 2026-01-15,
    iznosi u eurima). popuni_primjerom=true nadopuni nezadana polja primjerom (samo za probu, ne za stvarni
    dokument). nacrt=true dodaje vodeni žig NACRT. Poveznica vrijedi ograničeno vrijeme (zadano 24 sata)."""
    log.info("generiraj_dokument %s", oznaka)
    try:
        sazetak, rez = usluge.sastavi(oznaka, argumenti, popuni_primjerom=popuni_primjerom)
        sazetak["preuzimanje_docx"] = _spremi(rez.docx(nacrt=nacrt), rez.naziv_datoteke)
        sazetak["vrijedi_sati"] = round(ROK_S / 3600)
        return sazetak
    except GreskaUnosa as e:
        return _greska(e)


@mcp.tool()
def provjeri_oib(oib: str) -> dict:
    """Provjera kontrolne znamenke OIB-a (ISO 7064, MOD 11,10). Ne provjerava postoji li osoba."""
    log.info("provjeri_oib")
    return usluge.provjeri_oib(oib)


@mcp.tool()
def pristojba(vrsta: str, vrijednost_predmeta: float = 0.0) -> dict:
    """Sudska pristojba u eurima i, uz vrijednost predmeta, odvjetnička nagrada za sastav podneska.
    vrsta: tuzba, presuda, zalba, revizija, ovrha_jb, ovrha_ovrsna, prigovor_ovrhe, zk_prijedlog, zk_brisanje,
    zk_izvadak, upravni_spor, punomoc, zalba_zup."""
    log.info("pristojba %s", vrsta)
    try:
        return usluge.pristojba(vrsta, vrijednost_predmeta)
    except GreskaUnosa as e:
        return _greska(e)


@mcp.tool()
def sudovi(vrsta: str = "", upit: str = "") -> dict:
    """Hrvatski sudovi s adresama. vrsta: opcinski, trgovacki, zupanijski, visoki, upravni, vrhovni;
    upit: riječi iz naziva ili grada (npr. "Rijeka")."""
    log.info("sudovi")
    return usluge.sudovi(vrsta, upit)


@mcp.tool()
def klauzule(kategorija: str = "") -> dict:
    """Standardne ugovorne klauzule (naziv, kategorija, tekst) za umetanje u ugovore."""
    log.info("klauzule")
    return usluge.klauzule(kategorija)


@mcp.custom_route("/preuzmi/{token}", methods=["GET"])
async def preuzmi(request: Request):
    token = request.path_params.get("token", "")
    if not _TOKEN.match(token):
        return PlainTextResponse("Nepoznata poveznica.", status_code=404)
    f = SPREMISTE / f"{token}.docx"
    if not f.exists() or f.stat().st_mtime < time.time() - ROK_S:
        return PlainTextResponse("Poveznica je istekla ili ne postoji.", status_code=404)
    try:
        naziv = json.loads(f.with_suffix(".json").read_text(encoding="utf-8")).get("naziv", "dokument.docx")
    except (OSError, ValueError):
        naziv = "dokument.docx"
    return FileResponse(f, filename=naziv, headers={"Cache-Control": "no-store"},
                        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


@mcp.custom_route("/zdravlje", methods=["GET"])
async def zdravlje(request: Request):
    from pristup.katalog import dokumenti

    return JSONResponse({"status": "ok", "dokumenata": len(dokumenti())})


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    from pristup.katalog import dokumenti

    dokumenti()  # zagrij katalog prije prvog zahtjeva
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
