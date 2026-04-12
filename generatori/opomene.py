# -----------------------------------------------------------------------------
# GENERATORI: Opomena pred tuzbu / ovrhu
# Pravni temelj: ZOO, Ovrsni zakon
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur, format_eur_s_rijecima


def generiraj_opomenu(
    vrsta, vjerovnik, duznik, trazbina, podaci, zastupanje=""
):
    """
    Generira opomenu pred tuzbu ili opomenu pred ovrhu.
    vrsta: 'tuzba' ili 'ovrha'
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        naslov = "OPOMENA PRED TUŽBU" if vrsta == "tuzba" else "OPOMENA PRED OVRHU"
        rok = podaci.get("rok_dana", 8)
        mjesto = podaci.get("mjesto", "Zagreb")

        najava = (
            "pokretanja parničnog postupka pred nadležnim sudom"
            if vrsta == "tuzba"
            else "pokretanja ovršnog postupka radi prisilne naplate"
        )

        pravni_temelj = (
            "Na temelju odredbi Zakona o obveznim odnosima (NN 35/05, 41/08, 125/11, 78/15, 29/18, 126/21, 114/22, 156/22)"
            if vrsta == "tuzba"
            else "Na temelju odredbi Ovršnog zakona (NN 112/12, 25/13, 93/14, 55/16, 73/17, 131/20)"
        )

        opis_osnove = format_text(podaci.get("opis_osnove", ""))

        return (
            f"<div style='text-align: right; font-size: 10pt;'>{mjesto}, {danas}</div><br>"
            f"{zastupanje}"
            f"<div class='party-info'><b>VJEROVNIK:</b><br>{vjerovnik}</div>"
            f"<div class='party-info'><b>DUŽNIK:</b><br>{duznik}</div><br>"
            f"<div class='header-doc'>{naslov}</div>"
            f"<div class='justified'>{pravni_temelj}, ovime Vas pozivamo "
            f"da u roku od <b>{rok} ({_broj_rijecima(rok)}) dana</b> od primitka ove opomene "
            f"podmirite dospjelu obvezu u ukupnom iznosu od "
            f"<b>{format_eur_s_rijecima(trazbina['glavnica'])}</b>.</div><br>"
            f"<div class='section-title'>OSNOVA TRAŽBINE</div>"
            f"<div class='justified'>{opis_osnove}</div><br>"
            f"<div class='justified'>Obveza je dospjela dana <b>{podaci.get('datum_dospijeca', '________')}</b> "
            f"te do danas nije podmirena, ni djelomično ni u cijelosti.</div><br>"
            f"<div class='justified'>Ukoliko u ostavljenom roku ne podmiri navedeni iznos, "
            f"bit ćemo primorani, bez daljnje obavijesti, pristupiti "
            f"<b>{najava}</b>, čime će Vam nastati i obveza naknade troškova postupka "
            f"(odvjetnički troškovi, sudska pristojba, zatezne kamate).</div><br>"
            f"<div class='justified'>Ova opomena ima značaj prethodnog poziva za ispunjenje "
            f"obveze u smislu odredbi Zakona o obveznim odnosima.</div><br>"
            f"<div class='section-title'>PODACI ZA UPLATU</div>"
            f"<div class='justified'>"
            f"Iznos: <b>{format_eur_s_rijecima(trazbina['glavnica'])}</b><br>"
            f"IBAN: {podaci.get('iban', '____________________')}<br>"
            f"Poziv na broj: {podaci.get('poziv_na_broj', '____________________')}<br>"
            f"Opis plaćanja: {podaci.get('opis_placanja', 'Podmirenje duga po opomeni')}"
            f"</div>"
            f"<br>"
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>VJEROVNIK</b><br>(po punomoćniku)</div>"
            f"</div>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def _broj_rijecima(n):
    """Jednostavna konverzija broja u rijeci za male brojeve."""
    rijeci = {
        1: "jedan", 2: "dva", 3: "tri", 4: "četiri", 5: "pet",
        6: "šest", 7: "sedam", 8: "osam", 9: "devet", 10: "deset",
        15: "petnaest", 30: "trideset",
    }
    return rijeci.get(n, str(n))
