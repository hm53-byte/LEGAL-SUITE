# =============================================================================
# JEDNOSTAVNO SUČELJE — "Pravni Kata" za ne-pravnike
# Situacijski ulaz → AIA upozorenje → blank DOCX ili formular
# =============================================================================
import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import date
from docx_export import pripremi_za_docx


def _scroll_to_top():
    """Injektira JS koji scrolla main container na vrh."""
    components.html(
        f"<script>setTimeout(function(){{"
        f"var el=parent.document.querySelector('section.main');"
        f"if(el)el.scrollTo(0,0);"
        f"}},50);</script><!-- {time.time()} -->",
        height=0,
    )

# =============================================================================
# SITUACIJE — mapiranje životnih događaja na pravne dokumente
# =============================================================================

_SITUACIJE = [
    {
        "id": "kupnja_auta",
        "naslov": "Kupujem ili prodajem auto",
        "opis": "Trebate pisani ugovor za kupoprodaju vozila",
        "ikona": "🚗",
        "aia": (
            "Ugovor se može sklopiti i usmeno (čl. 286. st. 1. ZOO), ali bez pisanog "
            "dokumenta ne možete dokazati dogovorenu cijenu ni uvjete prodaje.|"
            "Prodavatelj odgovara za skrivene nedostatke 2 godine od predaje "
            "(čl. 404. st. 2. ZOO). Bez ugovora, teško ćete ostvariti to pravo.|"
            "U slučaju spora, pisani ugovor je ključni dokaz pred sudom."
        ),
        "aia_zakoni": "čl. 286. st. 1., čl. 400.-410., čl. 404. st. 2. ZOO",
        "modul_pro": "Ugovori",
    },
    {
        "id": "najam_stana",
        "naslov": "Iznajmljujem stan",
        "opis": "Ugovor o najmu za najmodavca ili najmoprimca",
        "ikona": "🏠",
        "aia": (
            "Tražbina najamnine zastarijeva za 3 godine (čl. 229. ZOO). "
            "Bez pisanog ugovora, teško ćete dokazati dogovorenu najamninu.|"
            "Bez ugovora, najmoprimac nema dokaz o pravu korištenja stana — "
            "najmodavac može tvrditi da je neovlašteno useljenje.|"
            "Usmeni najam ne štiti od jednostranog povećanja cijene."
        ),
        "aia_zakoni": "čl. 229., čl. 286. st. 1. ZOO",
        "modul_pro": "Ugovori",
    },
    {
        "id": "posudba_novca",
        "naslov": "Posuđujem novac nekome",
        "opis": "Pisani ugovor o zajmu — zaštita za obje strane",
        "ikona": "💰",
        "aia": (
            "Tražbine zastarijevaju za 5 godina (čl. 225. ZOO). "
            "Bez pisanog dokaza o posudbi, sud ne može utvrditi da je posudba postojala.|"
            "Bez ugovora, ne možete pokrenuti ovrhu za povrat novca — "
            "preostaje samo tužba s neizvjesnim ishodom.|"
            "Pisani ugovor štiti i dužnika od tvrdnji da je posuđeno više nego što jest."
        ),
        "aia_zakoni": "čl. 225., čl. 286. st. 1. ZOO",
        "modul_pro": "Ugovori",
    },
    {
        "id": "reklamacija",
        "naslov": "Kupljeni proizvod ne valja",
        "opis": "Pisani prigovor trgovcu za neispravan proizvod",
        "ikona": "📦",
        "aia": (
            "Skrivene nedostatke morate prijaviti u roku od 2 mjeseca "
            "od otkrivanja (čl. 404. st. 1. ZOO).|"
            "Prodavatelj ne odgovara za nedostatke nakon 2 godine od predaje "
            "(čl. 404. st. 2. ZOO).|"
            "Trgovac je dužan odgovoriti na pisani prigovor u roku od 15 dana "
            "(čl. 10. st. 3. Zakona o zaštiti potrošača)."
        ),
        "aia_zakoni": "čl. 400.-410. ZOO, čl. 10. ZZP",
        "modul_pro": "Zaštita potrošača",
    },
    {
        "id": "online_raskid",
        "naslov": "Vraćam online kupnju",
        "opis": "Imate 14 dana za raskid bez navođenja razloga",
        "ikona": "🛒",
        "aia": (
            "Imate pravo na jednostrani raskid online kupnje u roku od 14 dana "
            "od primitka robe, bez navođenja razloga (čl. 79. ZZP).|"
            "Nakon 14 dana, gubite to pravo bez obzira na razlog.|"
            "Obrazac za raskid morate poslati PISANIM putem (email ili pošta)."
        ),
        "aia_zakoni": "čl. 79. Zakona o zaštiti potrošača",
        "modul_pro": "Zaštita potrošača",
    },
    {
        "id": "punomoc",
        "naslov": "Trebam dati nekome punomoć",
        "opis": "Ovlastite drugu osobu da vas zastupa",
        "ikona": "📝",
        "aia": (
            "Bez pisane punomoći, treća osoba ne može pravno valjano zastupati "
            "vaše interese pred institucijama.|"
            "Usmena punomoć je pravno valjana među strankama, "
            "ali je treće osobe (banka, sud, ured) neće prihvatiti.|"
            "Jasna pisana punomoć štiti vas od prekoračenja ovlasti."
        ),
        "aia_zakoni": "čl. 313.-321. ZOO",
        "modul_pro": "Punomoć",
    },
    {
        "id": "dugovanje",
        "naslov": "Netko mi duguje novac",
        "opis": "Korak-po-korak vodič za naplatu duga",
        "ikona": "⚖️",
        "kata": True,
        "aia": (
            "Svaka odgoda povećava rizik zastare potraživanja — "
            "opći rok je 5 godina (čl. 225. ZOO).|"
            "Svjedoci zaboravljaju, poruke se brišu, dokazi nestaju.|"
            "Dužnik može rasprodati imovinu prije nego pokrenete naplatu."
        ),
        "aia_zakoni": "čl. 225.-232. ZOO",
        "modul_pro": "Opomena",
    },
    {
        "id": "osnivanje_tvrtke",
        "naslov": "Osnivam tvrtku (d.o.o.)",
        "opis": "Društveni ugovor za osnivanje trgovačkog društva",
        "ikona": "🏢",
        "aia": (
            "Društveni ugovor je zakonski obavezan za osnivanje d.o.o. "
            "(čl. 387. Zakona o trgovačkim društvima).|"
            "Bez ispravnog društvenog ugovora, Trgovački sud neće upisati "
            "društvo u sudski registar.|"
            "Nejasan ugovor može dovesti do sporova među osnivačima."
        ),
        "aia_zakoni": "čl. 387. ZTD",
        "modul_pro": "Trgovačko pravo",
    },
    {
        "id": "zaposlavanje",
        "naslov": "Zapošljavam nekoga",
        "opis": "Ugovor o radu za poslodavca i radnika",
        "ikona": "👔",
        "aia": (
            "Ugovor o radu mora biti sklopljen u pisanom obliku "
            "(čl. 14. st. 1. Zakona o radu).|"
            "Bez pisanog ugovora, smatra se da je radnik zaposlen "
            "na neodređeno s punim radnim vremenom (čl. 14. st. 3. ZR).|"
            "Poslodavac bez ugovora krši zakon i podložan je inspekcijskom nadzoru."
        ),
        "aia_zakoni": "čl. 14. Zakona o radu",
        "modul_pro": "Ugovori",
    },
    {
        "id": "bracni_ugovor",
        "naslov": "Želim bračni ugovor",
        "opis": "Reguliranje imovinskih odnosa bračnih drugova",
        "ikona": "💍",
        "aia": (
            "Bez bračnog ugovora, primjenjuje se zakonski režim — "
            "sva imovina stečena u braku je bračna stečevina (čl. 36. Obiteljskog zakona).|"
            "U slučaju razvoda, podjela bračne stečevine može biti duga i skupa.|"
            "Bračni ugovor mora biti u pisanom obliku i ovjeren kod javnog bilježnika."
        ),
        "aia_zakoni": "čl. 36., čl. 40. Obiteljskog zakona",
        "modul_pro": "Obiteljsko pravo",
    },
    {
        "id": "sporazumni_razvod",
        "naslov": "Sporazumni razvod braka",
        "opis": "Kad se obje strane slažu oko razvoda",
        "ikona": "📋",
        "aia": (
            "Sporazumni razvod je brži i jeftiniji od tužbe za razvod.|"
            "Sporazum mora urediti: djecu (skrb, uzdržavanje, kontakte), "
            "imovinu, i stan (tko ostaje).|"
            "Bez sporazuma, sud sam odlučuje o svemu — "
            "a to može trajati godinama."
        ),
        "aia_zakoni": "čl. 50.-56. Obiteljskog zakona",
        "modul_pro": "Obiteljsko pravo",
    },
]


# =============================================================================
# BLANK HTML GENERATORI — puni pravni dokumenti s praznim poljima
# =============================================================================

def _bp(sirina=30):
    """Blank polje — crta za ručno upisivanje kemijskom olovkom."""
    return "_" * sirina


def _generiraj_blank_kupoprodaja():
    return (
        f"<div class='header-doc'>UGOVOR O KUPOPRODAJI MOTORNOG VOZILA</div>"
        f"<div class='doc-body'>Sklopljen u {_bp(20)}, dana ___.___.________. godine, između:</div>"
        f"<div class='party-info'>"
        f"1. <b>PRODAVATELJ:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='party-info'>"
        f"2. <b>KUPAC:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='section-title'>Članak 1. — Predmet ugovora</div>"
        f"<div class='doc-body'>Prodavatelj prodaje, a Kupac kupuje motorno vozilo:"
        f"<br>Marka i model: {_bp()}"
        f"<br>Godina proizvodnje: {_bp(10)}"
        f"<br>Broj šasije (VIN): {_bp(17)}"
        f"<br>Registarska oznaka: {_bp(15)}"
        f"<br>Stanje kilometara: {_bp(15)} km</div>"
        f"<div class='section-title'>Članak 2. — Cijena</div>"
        f"<div class='doc-body'>Kupac se obvezuje platiti kupoprodajnu cijenu u iznosu od "
        f"{_bp(15)} EUR (slovima: {_bp()})."
        f"<br>Način plaćanja (zaokružiti): gotovina / uplata na račun / na rate</div>"
        f"<div class='section-title'>Članak 3. — Predaja vozila</div>"
        f"<div class='doc-body'>Prodavatelj se obvezuje predati vozilo Kupcu "
        f"dana ___.___.________. u stanju u kakvom se nalazi u trenutku sklapanja ovog Ugovora.</div>"
        f"<div class='section-title'>Članak 4. — Odgovornost za nedostatke</div>"
        f"<div class='doc-body'>Prodavatelj jamči da vozilo nema pravnih nedostataka "
        f"(da nije predmet spora, ovrhe niti založeno). Prodavatelj odgovara za skrivene materijalne "
        f"nedostatke sukladno čl. 400.-410. Zakona o obveznim odnosima.</div>"
        f"<div class='section-title'>Članak 5. — Prijenos vlasništva</div>"
        f"<div class='doc-body'>Kupac stječe pravo vlasništva predajom vozila i "
        f"upisom u evidenciju nadležnog tijela (MUP). Troškove prijenosa registracije snosi Kupac.</div>"
        f"<div class='section-title'>Članak 6. — Završne odredbe</div>"
        f"<div class='doc-body'>Ovaj Ugovor sastavljen je u 2 (dva) istovjetna primjerka, "
        f"po jedan za svaku ugovornu stranu. Za sve što nije uređeno ovim Ugovorom, "
        f"primjenjuju se odredbe Zakona o obveznim odnosima.</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>PRODAVATELJ</b><br><br><br>______________________<br>"
        f"(vlastoručni potpis)</div>"
        f"<div class='signature-block'><b>KUPAC</b><br><br><br>______________________<br>"
        f"(vlastoručni potpis)</div>"
        f"</div>"
    )


def _generiraj_blank_najam():
    return (
        f"<div class='header-doc'>UGOVOR O NAJMU STANA</div>"
        f"<div class='doc-body'>Sklopljen u {_bp(20)}, dana ___.___.________. godine, između:</div>"
        f"<div class='party-info'>"
        f"1. <b>NAJMODAVAC:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='party-info'>"
        f"2. <b>NAJMOPRIMAC:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='section-title'>Članak 1. — Predmet najma</div>"
        f"<div class='doc-body'>Najmodavac daje u najam, a Najmoprimac prima u najam stan na adresi:"
        f"<br>{_bp()}"
        f"<br>Površina: {_bp(10)} m², broj soba: {_bp(5)}</div>"
        f"<div class='section-title'>Članak 2. — Trajanje najma</div>"
        f"<div class='doc-body'>Najam se sklapa na razdoblje od ___.___.________. do ___.___.________."
        f"<br>Otkazni rok: {_bp(10)} dana pisanom obavijesti.</div>"
        f"<div class='section-title'>Članak 3. — Najamnina</div>"
        f"<div class='doc-body'>Mjesečna najamnina iznosi {_bp(15)} EUR, "
        f"plativa do {_bp(5)} u mjesecu na račun: {_bp(25)}."
        f"<br>Režijski troškovi (zaokružiti): uključeni / zasebno / paušalno</div>"
        f"<div class='section-title'>Članak 4. — Jamčevina (polog)</div>"
        f"<div class='doc-body'>Najmoprimac plaća jamčevinu u iznosu od {_bp(15)} EUR, "
        f"koja se vraća po isteku najma umanjeno za eventualna potraživanja Najmodavca.</div>"
        f"<div class='section-title'>Članak 5. — Prava i obveze</div>"
        f"<div class='doc-body'>Najmodavac se obvezuje predati stan u ispravnom stanju. "
        f"Najmoprimac se obvezuje koristiti stan pažnjom dobrog domaćina, ne vršiti preinake "
        f"bez suglasnosti Najmodavca, te po isteku najma vratiti stan u stanju u kojem ga je primio.</div>"
        f"<div class='section-title'>Članak 6. — Završne odredbe</div>"
        f"<div class='doc-body'>Ovaj Ugovor sastavljen je u 2 (dva) istovjetna primjerka. "
        f"Za sporove je nadležan sud u {_bp(20)}.</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>NAJMODAVAC</b><br><br><br>______________________</div>"
        f"<div class='signature-block'><b>NAJMOPRIMAC</b><br><br><br>______________________</div>"
        f"</div>"
    )


def _generiraj_blank_zajam():
    return (
        f"<div class='header-doc'>UGOVOR O ZAJMU</div>"
        f"<div class='doc-body'>Sklopljen u {_bp(20)}, dana ___.___.________. godine, između:</div>"
        f"<div class='party-info'>"
        f"1. <b>ZAJMODAVAC:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='party-info'>"
        f"2. <b>ZAJMOPRIMAC:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='section-title'>Članak 1. — Predmet ugovora</div>"
        f"<div class='doc-body'>Zajmodavac daje, a Zajmoprimac prima u zajam novčani iznos od "
        f"{_bp(15)} EUR (slovima: {_bp()}).</div>"
        f"<div class='section-title'>Članak 2. — Rok vraćanja</div>"
        f"<div class='doc-body'>Zajmoprimac se obvezuje vratiti zajam najkasnije do "
        f"___.___.________. godine."
        f"<br>Način vraćanja (zaokružiti): jednokratno / u ratama od {_bp(10)} EUR mjesečno</div>"
        f"<div class='section-title'>Članak 3. — Kamate</div>"
        f"<div class='doc-body'>Na zajam se (zaokružiti) obračunavaju / NE obračunavaju kamate. "
        f"Ugovorena kamatna stopa: {_bp(10)} % godišnje.</div>"
        f"<div class='section-title'>Članak 4. — Zakašnjenje</div>"
        f"<div class='doc-body'>U slučaju zakašnjenja s vraćanjem, "
        f"Zajmoprimac je dužan platiti zakonske zatezne kamate "
        f"sukladno čl. 29. ZOO.</div>"
        f"<div class='section-title'>Članak 5. — Završne odredbe</div>"
        f"<div class='doc-body'>Ovaj Ugovor sastavljen je u 2 (dva) istovjetna primjerka. "
        f"Za sporove je nadležan sud u {_bp(20)}.</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>ZAJMODAVAC</b><br><br><br>______________________</div>"
        f"<div class='signature-block'><b>ZAJMOPRIMAC</b><br><br><br>______________________</div>"
        f"</div>"
    )


def _generiraj_blank_opomena():
    danas = date.today().strftime("%d.%m.%Y.")
    return (
        f"<div style='text-align: right; font-size: 10pt;'>{_bp(20)}, {danas}</div><br>"
        f"<div class='party-info'><b>VJEROVNIK:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='party-info'><b>DUŽNIK:</b><br>"
        f"Ime i prezime/Naziv: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div><br>"
        f"<div class='header-doc'>OPOMENA PRED TUŽBU</div>"
        f"<div class='justified'>Na temelju odredbi Zakona o obveznim odnosima, "
        f"ovime Vas pozivamo da u roku od <b>8 (osam) dana</b> od primitka ove opomene "
        f"podmirite dospjelu obvezu u ukupnom iznosu od "
        f"<b>{_bp(15)} EUR</b>.</div><br>"
        f"<div class='section-title'>OSNOVA TRAŽBINE</div>"
        f"<div class='justified'>(opišite osnovu duga — ugovor, račun, posudba...):<br><br>"
        f"{_bp(50)}<br><br>{_bp(50)}<br><br>{_bp(50)}</div><br>"
        f"<div class='justified'>Obveza je dospjela dana <b>___.___.________.</b> "
        f"te do danas nije podmirena, ni djelomično ni u cijelosti.</div><br>"
        f"<div class='justified'>Ukoliko u ostavljenom roku ne podmirite navedeni iznos, "
        f"bit ćemo primorani, bez daljnje obavijesti, pristupiti "
        f"<b>pokretanju parničnog postupka pred nadležnim sudom</b>, "
        f"čime će Vam nastati i obveza naknade troškova postupka.</div><br>"
        f"<div class='section-title'>PODACI ZA UPLATU</div>"
        f"<div class='justified'>"
        f"Iznos: <b>{_bp(15)} EUR</b><br>"
        f"IBAN: HR__ ____ ____ ____ ____ _<br>"
        f"Poziv na broj: {_bp(15)}<br>"
        f"Opis plaćanja: podmirenje duga po opomeni"
        f"</div><br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>VJEROVNIK</b><br><br><br>______________________</div>"
        f"</div>"
    )


def _generiraj_blank_reklamacija():
    danas = date.today().strftime("%d.%m.%Y.")
    return (
        f"<div style='text-align: right; font-size: 10pt;'>{_bp(20)}, {danas}</div><br>"
        f"<div class='party-info'><b>TRGOVAC:</b><br>"
        f"Naziv: {_bp()}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='party-info' style='text-align: right;'>"
        f"<b>POTROŠAČ:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"Adresa: {_bp()}<br>"
        f"Telefon/email: {_bp()}</div><br>"
        f"<div class='header-doc'>PISANI PRIGOVOR / REKLAMACIJA</div>"
        f"<div class='section-title'>I. PODACI O KUPNJI</div>"
        f"<div class='doc-body'>"
        f"Datum kupnje: <b>___.___.________.</b><br>"
        f"Broj računa: <b>{_bp(20)}</b><br>"
        f"Opis proizvoda: <b>{_bp()}</b><br>"
        f"Plaćena cijena: <b>{_bp(15)} EUR</b></div>"
        f"<div class='section-title'>II. OPIS NEDOSTATKA</div>"
        f"<div class='doc-body'>"
        f"Kupljeni proizvod ima materijalni nedostatak u smislu čl. 400. ZOO, "
        f"koji se očituje u sljedećem:<br><br>"
        f"{_bp(50)}<br><br>{_bp(50)}</div>"
        f"<div class='section-title'>III. ZAHTJEV</div>"
        f"<div class='doc-body'>Sukladno čl. 410. ZOO, zahtijevam (zaokružiti): "
        f"popravak / zamjenu / povrat novca / sniženje cijene</div><br>"
        f"<div class='doc-body' style='border: 1px solid #666; padding: 10px;'>"
        f"<b>NAPOMENA:</b> Sukladno čl. 10. st. 3. Zakona o zaštiti potrošača, "
        f"trgovac je dužan odgovoriti na pisani prigovor u roku od <b>15 dana</b>.</div><br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>POTROŠAČ</b><br><br><br>______________________</div>"
        f"</div>"
    )


def _generiraj_blank_raskid_online():
    danas = date.today().strftime("%d.%m.%Y.")
    return (
        f"<div style='text-align: right; font-size: 10pt;'>{_bp(20)}, {danas}</div><br>"
        f"<div class='party-info'><b>TRGOVAC:</b><br>"
        f"Naziv: {_bp()}<br>"
        f"Adresa/Email: {_bp()}</div>"
        f"<div class='party-info' style='text-align: right;'>"
        f"<b>POTROŠAČ:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"Adresa: {_bp()}</div><br>"
        f"<div class='header-doc'>IZJAVA O JEDNOSTRANOM RASKIDU UGOVORA</div>"
        f"<div class='justified'>Na temelju članka 79. Zakona o zaštiti potrošača (NN 19/22), "
        f"ovime izjavljujem da jednostrano raskidam ugovor sklopljen na daljinu za sljedeći proizvod/uslugu:</div><br>"
        f"<div class='doc-body'>"
        f"Naziv proizvoda: <b>{_bp()}</b><br>"
        f"Datum narudžbe: <b>___.___.________.</b><br>"
        f"Datum primitka: <b>___.___.________.</b><br>"
        f"Broj narudžbe: <b>{_bp(20)}</b><br>"
        f"Plaćena cijena: <b>{_bp(15)} EUR</b></div><br>"
        f"<div class='justified'>Zahtijevam povrat uplaćenog iznosa u roku od 14 dana "
        f"od primitka ove izjave, na način na koji je plaćanje izvršeno.</div><br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>POTROŠAČ</b><br><br><br>______________________</div>"
        f"</div>"
    )


def _generiraj_blank_punomoc():
    danas = date.today().strftime("%d.%m.%Y.")
    return (
        f"<div class='header-doc'>PUNOMOĆ</div>"
        f"<div class='justified'>Ja, {_bp()}, "
        f"OIB: {_bp(11)}, s prebivalištem na adresi {_bp()}, "
        f"ovime dajem punomoć:</div><br>"
        f"<div class='justified'><b>OPUNOMOĆENIKU:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div><br>"
        f"<div class='justified'>da me zastupa i poduzima sve pravne radnje u vezi:</div><br>"
        f"<div class='doc-body'>"
        f"{_bp(50)}<br><br>{_bp(50)}</div><br>"
        f"<div class='justified'>Ova punomoć vrijedi do ___.___.________. / do opoziva.</div><br>"
        f"<div style='text-align: right; font-size: 10pt;'>"
        f"U {_bp(20)}, dana {danas}</div><br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>DAVATELJ PUNOMOĆI</b><br><br><br>______________________</div>"
        f"</div>"
    )


# Mapiranje ID-a situacije na generator blank dokumenta
_BLANK_GENERATORI = {
    "kupnja_auta": ("Kupoprodaja_automobila.docx", _generiraj_blank_kupoprodaja),
    "najam_stana": ("Ugovor_o_najmu.docx", _generiraj_blank_najam),
    "posudba_novca": ("Ugovor_o_zajmu.docx", _generiraj_blank_zajam),
    "reklamacija": ("Reklamacija.docx", _generiraj_blank_reklamacija),
    "online_raskid": ("Raskid_online_kupnje.docx", _generiraj_blank_raskid_online),
    "punomoc": ("Punomoc.docx", _generiraj_blank_punomoc),
    "dugovanje": ("Opomena_pred_tuzbu.docx", _generiraj_blank_opomena),
}


# =============================================================================
# KATA TOK — koraci za "Netko mi duguje novac"
# =============================================================================

_KATA_DUGOVANJE = [
    {
        "broj": 1,
        "naslov": "Pošaljite pisanu opomenu",
        "opis": (
            "Dužniku pošaljite pisanu opomenu s rokom od 8 dana. "
            "Ovo je prvi i najvažniji korak — mnogi dugovi se naplate već ovdje."
        ),
        "savjet": "Pošaljite PREPORUČENOM POŠTOM s povratnicom — to je vaš dokaz da je dužnik primio opomenu.",
        "dokument": "dugovanje",
    },
    {
        "broj": 2,
        "naslov": "Sačekajte 8 dana",
        "opis": (
            "Rok počinje od dana kad dužnik PRIMI opomenu "
            "(datum na povratnici). Sačuvajte povratnicu!"
        ),
        "savjet": None,
        "dokument": None,
    },
    {
        "broj": 3,
        "naslov": "Ako nije platio — odlučite o sljedećem koraku",
        "opis": (
            "Ako imate pisani ugovor, račun ili drugu ovršnu ispravu — "
            "možete pokrenuti OVRHU (brže i jeftinije). "
            "Ako nemate — morate tužiti na sudu."
        ),
        "savjet": (
            "Za ovrhu i tužbu preporučamo da se prebacite na napredni mod "
            "ili konzultirate odvjetnika."
        ),
        "dokument": None,
    },
]


# =============================================================================
# GLAVNA RENDER FUNKCIJA
# =============================================================================

def render_jednostavno(navigate_fn=None):
    """Renderira pojednostavljeno sučelje za ne-pravnike."""

    # Hero sekcija
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1E3A5F 0%,#2D4A6F 100%);"
        "color:white;padding:1.8rem 2rem;border-radius:12px;margin-bottom:1.5rem;'>"
        "<h2 style='color:white !important;font-size:1.5rem !important;"
        "margin-bottom:0.4rem !important;font-weight:700;'>Brzi pravni dokumenti</h2>"
        "<p style='color:rgba(255,255,255,0.85) !important;font-size:0.95rem;"
        "margin:0 !important;'>Bez pravnog znanja. Odaberite situaciju, "
        "isprintajte dokument, ispunite ručno.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Inicijalizacija stanja
    if "_jed_odabir" not in st.session_state:
        st.session_state._jed_odabir = None

    # ─── Prikaz situacija ───────────────────────────────────────────────
    odabir = st.session_state._jed_odabir

    if odabir is None:
        _prikazi_situacije()
    else:
        situacija = next((s for s in _SITUACIJE if s["id"] == odabir), None)
        if situacija is None:
            st.session_state._jed_odabir = None
            st.rerun()
        else:
            _prikazi_detalje(situacija, navigate_fn)

    # ─── Disclaimer ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<div style='background:#FFF7ED;border:1px solid #FED7AA;border-radius:8px;"
        "padding:0.8rem 1rem;font-size:0.75rem;color:#92400E;line-height:1.5;'>"
        "<b>Napomena:</b> Ove informacije su opće pravne činjenice iz javno dostupnih zakona, "
        "ne pravni savjet. Za složene situacije konzultirajte odvjetnika. "
        "Dokumente provjerite prije potpisa."
        "</div>",
        unsafe_allow_html=True,
    )


def _prikazi_situacije():
    """Prikaz kartica sa situacijama."""
    st.markdown("##### Što vam treba?")

    cols = st.columns(2)
    for i, sit in enumerate(_SITUACIJE):
        with cols[i % 2]:
            kata_oznaka = (
                "<span style='background:#7C3AED;color:white;padding:1px 6px;"
                "border-radius:3px;font-size:0.6rem;font-weight:600;"
                "margin-left:6px;'>VODIČ</span>"
                if sit.get("kata") else ""
            )
            st.markdown(
                f"<div style='background:white;border:1px solid #E2E8F0;border-radius:10px;"
                f"padding:1rem 1.2rem;margin-bottom:0.5rem;"
                f"transition:border-color 0.15s ease,box-shadow 0.15s ease;'>"
                f"<div style='display:flex;align-items:center;gap:0.6rem;'>"
                f"<span style='font-size:1.5rem;'>{sit['ikona']}</span>"
                f"<div>"
                f"<b style='color:#1E3A5F;font-size:0.95rem;'>{sit['naslov']}</b>"
                f"{kata_oznaka}"
                f"<br><span style='color:#64748B;font-size:0.8rem;'>{sit['opis']}</span>"
                f"</div></div></div>",
                unsafe_allow_html=True,
            )
            if st.button("Odaberi", key=f"_jed_sit_{i}", use_container_width=True):
                st.session_state._jed_odabir = sit["id"]
                st.rerun()


def _prikazi_detalje(situacija, navigate_fn):
    """Prikaz detalja situacije: AIA + blank DOCX + opcija za Pro."""

    # Scroll na vrh kad se otvore detalji
    _scroll_to_top()

    # Gumb za nazad
    if st.button("← Natrag na sve situacije", key="_jed_nazad"):
        st.session_state._jed_odabir = None
        st.rerun()

    st.markdown(f"### {situacija['ikona']} {situacija['naslov']}")

    # ─── AIA BOX ───────────────────────────────────────────────────────
    aia_tocke = situacija["aia"].split("|")
    aia_html = "".join(
        f"<li style='margin-bottom:0.4rem;'>{t.strip()}</li>"
        for t in aia_tocke
    )
    st.markdown(
        f"<div style='background:linear-gradient(135deg,#FEF2F2,#FFF1F2);"
        f"border:1px solid #FECACA;border-left:4px solid #DC2626;border-radius:8px;"
        f"padding:1rem 1.2rem;margin:0.8rem 0 1.2rem;'>"
        f"<div style='color:#991B1B;font-weight:700;font-size:0.9rem;"
        f"margin-bottom:0.5rem;'>Bez ovog dokumenta riskirate:</div>"
        f"<ul style='color:#7F1D1D;font-size:0.85rem;margin:0;padding-left:1.2rem;"
        f"line-height:1.6;'>{aia_html}</ul>"
        f"<div style='margin-top:0.6rem;padding-top:0.5rem;border-top:1px solid #FECACA;"
        f"color:#9CA3AF;font-size:0.7rem;'>"
        f"Pravni temelj: {situacija['aia_zakoni']}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ─── KATA TOK (za multi-step situacije) ────────────────────────────
    if situacija.get("kata"):
        _prikazi_kata(situacija, navigate_fn)
        return

    # ─── SINGLE-STEP: Blank DOCX + Pro opcija ─────────────────────────
    st.markdown("##### Kako želite nastaviti?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "<div style='background:#F0FDF4;border:1px solid #BBF7D0;border-radius:10px;"
            "padding:1rem 1.2rem;height:100%;'>"
            "<div style='font-weight:700;color:#166534;font-size:0.9rem;"
            "margin-bottom:0.5rem;'>Isprintaj i ispuni ručno</div>"
            "<div style='color:#15803D;font-size:0.8rem;line-height:1.5;'>"
            "Gotov dokument s praznim poljima. Isprintajte ga i ispunite kemijskom olovkom. "
            "Sadrži SVE pravne klauzule i članke."
            "</div></div>",
            unsafe_allow_html=True,
        )
        blank_info = _BLANK_GENERATORI.get(situacija["id"])
        if blank_info:
            naziv, gen_fn = blank_info
            doc_html = gen_fn()
            docx_bytes = pripremi_za_docx(doc_html, watermark=None, naslov_dokumenta=naziv.replace('.docx', ''))
            st.download_button(
                f"Preuzmi ({naziv})",
                docx_bytes,
                naziv,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key=f"_jed_dl_{situacija['id']}",
            )

    with col2:
        st.markdown(
            "<div style='background:#EFF6FF;border:1px solid #BFDBFE;border-radius:10px;"
            "padding:1rem 1.2rem;height:100%;'>"
            "<div style='font-weight:700;color:#1E40AF;font-size:0.9rem;"
            "margin-bottom:0.5rem;'>Ispuni na računalu</div>"
            "<div style='color:#1D4ED8;font-size:0.8rem;line-height:1.5;'>"
            "Otvorite puni formular, unesite podatke, i preuzmite gotov dokument. "
            "Uključuje OIB provjeru i sve opcije."
            "</div></div>",
            unsafe_allow_html=True,
        )
        if navigate_fn and situacija.get("modul_pro"):
            if st.button(
                f"Otvori formular →",
                use_container_width=True,
                type="primary",
                key=f"_jed_pro_{situacija['id']}",
            ):
                st.session_state._app_mode = "napredno"
                navigate_fn(situacija["modul_pro"])
                st.rerun()

    # ─── Pregled blank dokumenta ───────────────────────────────────────
    if blank_info:
        with st.expander("Pregledaj dokument prije preuzimanja"):
            st.markdown(f"<div class='legal-doc'>{doc_html}</div>", unsafe_allow_html=True)


def _prikazi_kata(situacija, navigate_fn):
    """Prikaz korak-po-korak vodića za multi-step situacije."""

    st.markdown("##### Koraci za naplatu duga")

    for korak in _KATA_DUGOVANJE:
        # Broj i naslov koraka
        boja_broja = "#1E3A5F"
        st.markdown(
            f"<div style='background:white;border:1px solid #E2E8F0;border-radius:10px;"
            f"padding:1rem 1.2rem;margin-bottom:0.8rem;"
            f"border-left:4px solid {boja_broja};'>"
            f"<div style='display:flex;align-items:flex-start;gap:0.8rem;'>"
            f"<div style='background:{boja_broja};color:white;min-width:2rem;height:2rem;"
            f"border-radius:50%;display:flex;align-items:center;justify-content:center;"
            f"font-weight:700;font-size:0.9rem;'>{korak['broj']}</div>"
            f"<div>"
            f"<div style='font-weight:700;color:#1E3A5F;font-size:0.95rem;"
            f"margin-bottom:0.3rem;'>{korak['naslov']}</div>"
            f"<div style='color:#475569;font-size:0.85rem;line-height:1.5;'>{korak['opis']}</div>"
            + (
                f"<div style='background:#FFFBEB;border:1px solid #FDE68A;border-radius:6px;"
                f"padding:0.5rem 0.7rem;margin-top:0.5rem;font-size:0.8rem;color:#92400E;'>"
                f"<b>Savjet:</b> {korak['savjet']}</div>"
                if korak.get("savjet") else ""
            )
            + f"</div></div></div>",
            unsafe_allow_html=True,
        )

        # Gumb za blank download na koraku 1
        if korak.get("dokument"):
            blank_info = _BLANK_GENERATORI.get(korak["dokument"])
            if blank_info:
                naziv, gen_fn = blank_info
                doc_html = gen_fn()
                docx_bytes = pripremi_za_docx(doc_html, watermark=None, naslov_dokumenta="Opomena pred tužbu")
                col_dl, col_pro = st.columns(2)
                with col_dl:
                    st.download_button(
                        f"Preuzmi prazan obrazac",
                        docx_bytes,
                        naziv,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                        key=f"_kata_dl_{korak['broj']}",
                    )
                with col_pro:
                    if navigate_fn:
                        if st.button(
                            "Ispuni na računalu →",
                            use_container_width=True,
                            type="primary",
                            key=f"_kata_pro_{korak['broj']}",
                        ):
                            st.session_state._app_mode = "napredno"
                            navigate_fn("Opomena")
                            st.rerun()

    # Info o sljedećem koraku
    st.markdown(
        "<div style='background:#F5F3FF;border:1px solid #DDD6FE;border-radius:8px;"
        "padding:0.8rem 1rem;margin-top:0.5rem;'>"
        "<div style='color:#5B21B6;font-weight:600;font-size:0.85rem;'>"
        "Ako dužnik ni nakon opomene ne plati:</div>"
        "<div style='color:#6D28D9;font-size:0.82rem;margin-top:0.3rem;line-height:1.5;'>"
        "Za ovrhu ili tužbu preporučamo napredni mod aplikacije ili konzultaciju s odvjetnikom. "
        "Ti postupci zahtijevaju precizno popunjavanje podataka.</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    if navigate_fn:
        c1, c2 = st.columns(2)
        with c1:
            if st.button(
                "Otvori modul: Ovrhe →",
                use_container_width=True,
                key="_kata_ovrha",
            ):
                st.session_state._app_mode = "napredno"
                navigate_fn("Ovršno pravo")
                st.rerun()
        with c2:
            if st.button(
                "Otvori modul: Tužbe →",
                use_container_width=True,
                key="_kata_tuzba",
            ):
                st.session_state._app_mode = "napredno"
                navigate_fn("Tužbe")
                st.rerun()
