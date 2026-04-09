"""
Testovi za clause_builder feature — SEKCIJE lista + refaktorirani generator.
"""
import pytest
from generatori.trgovacko import (
    generiraj_prodaju_poduzeca,
    SEKCIJE_PRODAJA_PODUZECA,
    _SEKCIJE_FN_PRODAJA,
)


# ---------------------------------------------------------------------------
# Testovi za SEKCIJE_PRODAJA_PODUZECA listu
# ---------------------------------------------------------------------------

def test_sve_sekcije_imaju_obavezna_polja():
    for sek in SEKCIJE_PRODAJA_PODUZECA:
        assert "id" in sek, f"Sekcija nema 'id': {sek}"
        assert "naziv" in sek, f"Sekcija nema 'naziv': {sek}"
        assert "obavezno" in sek, f"Sekcija nema 'obavezno': {sek}"
        assert "ukljuceno" in sek, f"Sekcija nema 'ukljuceno': {sek}"


def test_sekcije_id_su_jedinstveni():
    ids = [s["id"] for s in SEKCIJE_PRODAJA_PODUZECA]
    assert len(ids) == len(set(ids)), "Duplikat ID u SEKCIJE_PRODAJA_PODUZECA"


def test_zavrsne_je_fiksna_zadnja():
    zavrsna = next(s for s in SEKCIJE_PRODAJA_PODUZECA if s["id"] == "zavrsne")
    assert zavrsna.get("fiksna_pozicija") == "zadnja"


def test_obavezne_sekcije_su_ukljucene():
    for sek in SEKCIJE_PRODAJA_PODUZECA:
        if sek["obavezno"]:
            assert sek["ukljuceno"], f"Obavezna sekcija '{sek['id']}' nije ukljucena"


def test_dispatcher_pokriven_sve_sekcije():
    ids = {s["id"] for s in SEKCIJE_PRODAJA_PODUZECA}
    dispatcher_ids = set(_SEKCIJE_FN_PRODAJA.keys())
    assert ids == dispatcher_ids, f"Razlika: {ids.symmetric_difference(dispatcher_ids)}"


# ---------------------------------------------------------------------------
# Testovi za generator s defaultnim redoslijedom
# ---------------------------------------------------------------------------

PODACI_MIN = {
    "kupoprodajna_cijena": 100000,
    "cap_odgovornosti_posto": 20,
    "survival_period_godina": 2,
    "ugovorna_kazna": 10000,
}


def test_generator_defaultni_redoslijed():
    html = generiraj_prodaju_poduzeca("Prodavatelj d.o.o.", "Kupac d.o.o.", PODACI_MIN)
    assert "PREDMET UGOVORA" in html
    assert "KUPOPRODAJNA CIJENA" in html
    assert "IZJAVE I JAMSTVA" in html
    assert "Završne odredbe" in html
    assert "Članak 1." in html


def test_generator_samo_obavezni():
    redoslijed = ["predmet", "cijena", "izjave_jamstva", "sporovi", "zavrsne"]
    html = generiraj_prodaju_poduzeca("A", "B", PODACI_MIN, sekcije_redoslijed=redoslijed)
    assert "PREDMET UGOVORA" in html
    assert "Završne odredbe" in html
    assert "NON-COMPETE" not in html
    assert "NEKRETNINE" not in html


def test_generator_custom_redoslijed_zabrana_ispred_izjava():
    redoslijed = ["predmet", "cijena", "zabrana_natjecanja", "izjave_jamstva", "zavrsne"]
    podaci = {**PODACI_MIN, "zabrana_kazna": 50000}
    html = generiraj_prodaju_poduzeca("A", "B", podaci, sekcije_redoslijed=redoslijed)
    pos_zabrana = html.find("NON-COMPETE")
    pos_izjave = html.find("IZJAVE I JAMSTVA")
    assert pos_zabrana > 0
    assert pos_izjave > 0
    assert pos_zabrana < pos_izjave


def test_generator_prazni_redoslijed():
    html = generiraj_prodaju_poduzeca("A", "B", PODACI_MIN, sekcije_redoslijed=[])
    assert "UGOVOR O PRODAJI PODUZEĆA" in html
    assert "Članak 1." not in html


def test_generator_clanaci_su_sekvencijalni():
    redoslijed = ["predmet", "cijena", "izjave_jamstva", "zavrsne"]
    html = generiraj_prodaju_poduzeca("A", "B", PODACI_MIN, sekcije_redoslijed=redoslijed)
    # predmet = 2 clanka, cijena = 3, izjave_jamstva = 2, zavrsne = 1 => ukupno 8
    assert "Članak 1." in html
    assert "Članak 8." in html
    assert "Članak 9." not in html


def test_generator_s_imovinom():
    redoslijed = ["predmet", "cijena", "nekretnine", "pokretnine", "izjave_jamstva", "zavrsne"]
    podaci = {**PODACI_MIN, "nekretnina_opis": "Zgrada u Osijeku", "pokretnine_opis": "Vozila"}
    html = generiraj_prodaju_poduzeca("A", "B", podaci, sekcije_redoslijed=redoslijed)
    assert "NEKRETNINE" in html
    assert "POKRETNINE" in html
    assert "CLAUSULA INTABULANDI" in html


def test_generator_hipoteka_samo_ako_ima_podatke():
    podaci = {
        **PODACI_MIN,
        "nekretnina_opis": "Stan u Splitu",
        "ima_hipoteku": True,
        "hipoteka_iznos": 50000,
        "hipoteka_banka": "Erste banka",
    }
    html = generiraj_prodaju_poduzeca(
        "A", "B", podaci, sekcije_redoslijed=["predmet", "nekretnine", "zavrsne"]
    )
    assert "hipotekom" in html
    assert "Erste banka" in html


def test_generator_nema_greske_pri_minimalnim_podacima():
    html = generiraj_prodaju_poduzeca("A", "B", {})
    assert "Greška" not in html
    assert "UGOVOR O PRODAJI PODUZEĆA" in html
