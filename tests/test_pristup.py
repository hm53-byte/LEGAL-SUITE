"""Vanjski pristup (pristup/): katalog, generiranje iz argumenata, CLI i MCP poslužitelj."""

from __future__ import annotations

import io
import json
import zipfile

import pytest

pytest.importorskip("mcp")

from pristup import usluge  # noqa: E402
from pristup.generiranje import GreskaUnosa, generiraj, stranka_html, u_datum  # noqa: E402
from pristup.katalog import dokumenti  # noqa: E402


def test_katalog_pokriva_sve_generatore():
    import importlib
    import inspect
    import pkgutil

    import generatori

    ocekivano = set()
    for m in pkgutil.iter_modules(generatori.__path__):
        mod = importlib.import_module(f"generatori.{m.name}")
        for ime, f in vars(mod).items():
            if ime.startswith("generiraj_") and inspect.isfunction(f) and f.__module__ == mod.__name__:
                ocekivano.add(f"{m.name}/{ime[len('generiraj_'):]}")
    assert set(dokumenti()) == ocekivano and len(ocekivano) >= 80


@pytest.mark.parametrize("oznaka", sorted(dokumenti()))
def test_svaki_dokument_nastaje_iz_svojeg_primjera(oznaka):
    d = dokumenti()[oznaka]
    r = generiraj(oznaka, d.primjer)
    assert len(r.tekst) > 100
    sadrzaj = r.docx()
    assert zipfile.ZipFile(io.BytesIO(sadrzaj)).testzip() is None


def test_primjer_je_json_i_stranke_su_objekti():
    for d in dokumenti().values():
        json.dumps(d.kao_rjecnik(), ensure_ascii=False)
        for p in d.parametri:
            if p.vrsta == "stranka" and p.ime in d.primjer:
                assert not str(d.primjer[p.ime]).startswith("<b>"), d.oznaka


def test_stranka_i_tekst_se_ciste_od_html():
    h = stranka_html({"tip": "fizicka", "ime": "<script>x</script> Ana", "oib": "1", "adresa": "A & B"})
    assert "<script>" not in h and "&lt;script&gt;" in h and h.startswith("<b>")
    p = stranka_html({"tip": "pravna", "tvrtka": "Firma d.o.o.", "oib": "2", "mbs": "3", "sjediste": "Rijeka",
                      "zastupnik": "Iva"})
    assert "Sjedište: Rijeka" in p and "MBS: 3" in p
    r = generiraj("opomene/opomenu", {**dokumenti()["opomene/opomenu"].primjer,
                                      "podaci": {"opis_osnove": "račun <b>br. 5</b>", "mjesto": "Split"}})
    assert "<b>br. 5</b>" not in r.html and "Split" in r.tekst


def test_datumi_i_greske_unosa():
    assert str(u_datum("2026-03-04", "x")) == "2026-03-04" == str(u_datum("04.03.2026.", "x"))
    with pytest.raises(GreskaUnosa):
        u_datum("sutra", "x")
    with pytest.raises(GreskaUnosa, match="Nepoznat dokument"):
        generiraj("nema/takvog", {})
    with pytest.raises(GreskaUnosa, match="nema parametre"):
        generiraj("opomene/opomenu", {"izmisljeno": 1}, popuni_primjerom=True)
    with pytest.raises(GreskaUnosa, match="traži parametar"):
        generiraj("opomene/opomenu", {})


def test_praznine_se_prijavljuju():
    s, _ = usluge.sastavi("opomene/opomenu", {}, popuni_primjerom=True)
    assert isinstance(s["praznine"], list)
    assert usluge.praznine("Rok: ________ dana, [mjesto] i ništa više")[:2]


def test_pomocni_alati():
    assert usluge.provjeri_oib("12345678903")["ispravan"] is True
    assert usluge.provjeri_oib("12345678900")["ispravan"] is False
    assert usluge.pristojba("tuzba", 5000)["pristojba_eur"] > 0
    with pytest.raises(GreskaUnosa):
        usluge.pristojba("nepostojeca")
    assert usluge.sudovi(upit="Rijeka")["broj"] >= 1
    assert usluge.katalog("ovrha")["broj"] >= 3


def test_cli_primjer_i_generiraj(tmp_path, capsys):
    from pristup import cli

    assert cli.main(["primjer", "opomene/opomenu"]) == 0
    primjer = json.loads(capsys.readouterr().out)
    ulaz = tmp_path / "ulaz.json"
    ulaz.write_text(json.dumps(primjer, ensure_ascii=False), encoding="utf-8")
    izlaz = tmp_path / "opomena.docx"
    assert cli.main(["generiraj", "opomene/opomenu", str(ulaz), "-o", str(izlaz)]) == 0
    assert json.loads(capsys.readouterr().out)["docx"].endswith("opomena.docx") and izlaz.stat().st_size > 1000
    assert cli.main(["generiraj", "nema/takvog"]) == 2


def test_mcp_preko_http_i_preuzimanje(tmp_path, monkeypatch):
    from starlette.testclient import TestClient

    from pristup import mcp_posluzitelj as srv

    monkeypatch.setattr(srv, "SPREMISTE", tmp_path)
    monkeypatch.setattr(srv, "JAVNA", "http://127.0.0.1:8620")
    app = srv.mcp.streamable_http_app()
    zaglavlja = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json",
                 "Host": "127.0.0.1:8620"}

    def poziv(k, metoda, params, id_=1):
        r = k.post("/mcp", headers=zaglavlja, json={"jsonrpc": "2.0", "id": id_, "method": metoda, "params": params})
        assert r.status_code == 200, r.text
        return r.json()

    with TestClient(app, base_url="http://127.0.0.1:8620") as k:
        init = poziv(k, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                       "clientInfo": {"name": "test", "version": "1"}})
        assert init["result"]["serverInfo"]["name"] == "LegalTechSuite Pro"
        alati = {t["name"] for t in poziv(k, "tools/list", {}, 2)["result"]["tools"]}
        assert {"katalog", "opis_dokumenta", "generiraj_dokument", "provjeri_oib", "pristojba", "sudovi",
                "klauzule"} <= alati
        rez = poziv(k, "tools/call", {"name": "generiraj_dokument",
                                      "arguments": {"oznaka": "opomene/opomenu", "argumenti": {},
                                                    "popuni_primjerom": True}}, 3)["result"]
        sadrzaj = rez.get("structuredContent") or json.loads(rez["content"][0]["text"])
        poveznica = sadrzaj["preuzimanje_docx"]
        assert poveznica.startswith("http://127.0.0.1:8620/preuzmi/")
        d = k.get(poveznica.replace("http://127.0.0.1:8620", ""), headers={"Host": "127.0.0.1:8620"})
        assert d.status_code == 200 and d.content[:2] == b"PK"
        assert k.get("/preuzmi/nepostojeci_token_000000000000").status_code == 404
        tudji = k.post("/mcp", headers={**zaglavlja, "Host": "zli.example"}, json={"jsonrpc": "2.0", "id": 9,
                                                                               "method": "tools/list"})
        assert tudji.status_code in (400, 421)
