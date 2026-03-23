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

# Lucide-style inline SVG ikone (24x24, stroke 2, profesionalne)
def _svg(paths, vb="0 0 24 24"):
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='{vb}' "
        f"fill='none' stroke='white' stroke-width='2' stroke-linecap='round' "
        f"stroke-linejoin='round'>{paths}</svg>"
    )

_IKONE = {
    "kupnja_auta": _svg(
        "<path d='M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2'/>"
        "<circle cx='7' cy='17' r='2'/><circle cx='17' cy='17' r='2'/>"
    ),
    "najam_stana": _svg(
        "<path d='m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/>"
        "<polyline points='9 22 9 12 15 12 15 22'/>"
    ),
    "posudba_novca": _svg(
        "<rect width='20' height='12' x='2' y='6' rx='2'/>"
        "<circle cx='12' cy='12' r='2'/><path d='M6 12h.01M18 12h.01'/>"
    ),
    "reklamacija": _svg(
        "<path d='m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z'/>"
        "<path d='M12 9v4'/><path d='M12 17h.01'/>"
    ),
    "online_raskid": _svg(
        "<circle cx='8' cy='21' r='1'/><circle cx='19' cy='21' r='1'/>"
        "<path d='M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12'/>"
    ),
    "punomoc": _svg(
        "<path d='M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z'/>"
        "<path d='M14 2v4a2 2 0 0 0 2 2h4'/><path d='M10 12l2 2 4-4'/>"
    ),
    "dugovanje": _svg(
        "<path d='m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z'/>"
        "<path d='m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z'/>"
        "<path d='M7 21h10'/><path d='M12 3v18'/><path d='M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2'/>"
    ),
    "osnivanje_tvrtke": _svg(
        "<rect width='16' height='20' x='4' y='2' rx='2'/>"
        "<path d='M9 22v-4h6v4'/><path d='M8 6h.01'/><path d='M16 6h.01'/>"
        "<path d='M12 6h.01'/><path d='M12 10h.01'/><path d='M12 14h.01'/>"
        "<path d='M16 10h.01'/><path d='M16 14h.01'/><path d='M8 10h.01'/><path d='M8 14h.01'/>"
    ),
    "zaposlavanje": _svg(
        "<path d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'/>"
        "<circle cx='9' cy='7' r='4'/><path d='M19 8v6'/><path d='M22 11h-6'/>"
    ),
    "bracni_ugovor": _svg(
        "<path d='M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z'/>"
    ),
    "sporazumni_razvod": _svg(
        "<path d='M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z'/>"
        "<path d='M14 2v4a2 2 0 0 0 2 2h4'/><path d='M8 15h8'/>"
    ),
    "kupnja_motora": _svg(
        "<path d='M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2'/>"
        "<path d='M15 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 13.52 9H12'/>"
        "<circle cx='7' cy='18' r='2'/><circle cx='17' cy='18' r='2'/>"
    ),
    "primopredajni": _svg(
        "<path d='M9 5H2v7l6.29 6.29c.94.94 2.48.94 3.42 0l3.58-3.58c.94-.94.94-2.48 0-3.42L9 5Z'/>"
        "<path d='M6 9.01V9'/><path d='m15 5 6.3 6.3a2.4 2.4 0 0 1 0 3.4L17 19'/>"
    ),
    "raskid_najma": _svg(
        "<path d='m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/>"
        "<line x1='9' y1='21' x2='9' y2='9'/><line x1='15' y1='21' x2='15' y2='9'/>"
        "<line x1='3' y1='15' x2='21' y2='15'/>"
    ),
    "potvrda_povrata": _svg(
        "<path d='M22 11.08V12a10 10 0 1 1-5.93-9.14'/>"
        "<polyline points='22 4 12 14.01 9 11.01'/>"
    ),
    "predugovor_kapara": _svg(
        "<rect width='18' height='18' x='3' y='3' rx='2'/>"
        "<path d='M12 8v8'/><path d='M8 12h8'/>"
    ),
    "kupoprodaja_nekretnine": _svg(
        "<path d='m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/>"
        "<path d='M9 22V12h6v10'/>"
    ),
    "ugovor_o_djelu": _svg(
        "<path d='M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76Z'/>"
    ),
    "kupoprodaja_stvari": _svg(
        "<path d='m7.5 4.27 9 5.15'/>"
        "<path d='M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z'/>"
        "<path d='m3.3 7 8.7 5 8.7-5'/><path d='M12 22V12'/>"
    ),
    "suglasnost_stana": _svg(
        "<path d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'/>"
        "<circle cx='9' cy='7' r='4'/><path d='M22 21v-2a4 4 0 0 0-3-3.87'/>"
        "<path d='M16 3.13a4 4 0 0 1 0 7.75'/>"
    ),
    "kupoprodaja_plovila": _svg(
        "<path d='M2 21c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1 .6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1'/>"
        "<path d='M19.38 20A11.6 11.6 0 0 0 21 14l-9-4-9 4c0 2.9.94 5.34 2.81 7.76'/>"
        "<path d='M19 13V7a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v6'/><path d='M12 10v4'/>"
    ),
}

_SITUACIJE = [
    {
        "id": "kupnja_auta",
        "naslov": "Kupujem ili prodajem auto",
        "opis": "Trebate pisani ugovor za kupoprodaju vozila",
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
    {
        "id": "kupnja_motora",
        "naslov": "Kupujem ili prodajem motocikl",
        "opis": "Ugovor za kupoprodaju motocikla, skutera ili mopeda",
        "aia": (
            "Bez pisanog ugovora ne možete dokazati dogovorenu cijenu "
            "niti stanje vozila u trenutku prodaje.|"
            "Prodavatelj odgovara za skrivene nedostatke 2 godine od predaje "
            "(čl. 404. st. 2. ZOO).|"
            "Motocikli imaju specifične podatke (kubikaza, tip motora) "
            "koje treba upisati u ugovor za pravnu zaštitu."
        ),
        "aia_zakoni": "čl. 286. st. 1., čl. 400.-410. ZOO",
        "modul_pro": "Ugovori",
    },
    {
        "id": "primopredajni",
        "naslov": "Primopredaja stana",
        "opis": "Zapisnik o stanju stana pri useljenju ili iseljenju",
        "aia": (
            "Bez zapisnika ne možete dokazati u kakvom ste stanju "
            "primili stan — najmodavac može tvrditi da ste vi uzrokovali oštećenja.|"
            "Zapisnik mora sadržavati stanja brojila (struja, voda, plin) — "
            "inače plaćate tuđe račune.|"
            "Fotografije uz zapisnik su dodatni dokaz, ali pisani zapisnik "
            "je pravno jači temelj."
        ),
        "aia_zakoni": "čl. 557. ZOO (obveze najmoprimca pri povratu)",
        "modul_pro": "Ugovori",
    },
    {
        "id": "raskid_najma",
        "naslov": "Sporazumni raskid najma",
        "opis": "Kad se najmodavac i najmoprimac dogovore o prekidu najma",
        "aia": (
            "Bez pisanog raskida, najam formalno i dalje traje — "
            "najmodavac može tražiti najamninu za mjesece nakon iseljenja.|"
            "Raskid mora urediti: povrat jamčevine, stanje stana, "
            "zadnji dan najma i podmirenje režija.|"
            "Usmeni dogovor o raskidu ne vrijedi kao dokaz pred sudom."
        ),
        "aia_zakoni": "čl. 286., čl. 550.-557. ZOO",
        "modul_pro": "Ugovori",
    },
    {
        "id": "potvrda_povrata",
        "naslov": "Potvrda o povratu duga",
        "opis": "Dužnik vratio novac — potvrda da je dug podmiren",
        "aia": (
            "Bez pisane potvrde, vjerovnik može ponovo tražiti isti novac — "
            "nećete imati dokaz da ste platili.|"
            "Potvrda mora navesti TOČAN iznos, datum povrata i "
            "osnovu duga (koji zajam/račun).|"
            "Čuvajte potvrdu minimalno 5 godina (opći rok zastare, čl. 225. ZOO)."
        ),
        "aia_zakoni": "čl. 225., čl. 168.-170. ZOO (namirenje obveze)",
        "modul_pro": "Obvezno pravo",
    },
    {
        "id": "predugovor_kapara",
        "naslov": "Predugovor s kaparom (nekretnina)",
        "opis": "Prvi korak pri kupnji stana — kapara i rok za glavni ugovor",
        "aia": (
            "Kapara je novac koji GUBITE ako vi odustanete od kupnje. "
            "Ako prodavatelj odustane, mora vam vratiti DVOSTRUKU kaparu (čl. 303. ZOO).|"
            "Bez pisanog predugovora, kapara je samo 'dani novac' — "
            "ne možete dokazati uvjete dogovora.|"
            "Predugovor MORA sadržavati rok za sklapanje glavnog ugovora, "
            "inače nema pravni učinak."
        ),
        "aia_zakoni": "čl. 268. (predugovor), čl. 303. (kapara) ZOO",
        "modul_pro": "Obvezno pravo",
    },
    {
        "id": "kupoprodaja_nekretnine",
        "naslov": "Kupoprodaja nekretnine",
        "opis": "Glavni ugovor za kupnju/prodaju stana, kuće ili zemljišta",
        "aia": (
            "Ugovor o kupoprodaji nekretnine MORA biti u pisanom obliku i "
            "ovjeren kod javnog bilježnika — usmeni dogovor je ništavan (čl. 9. ZV).|"
            "Bez clausule intabulandi (izjave o dozvoli upisa), kupac se "
            "NE MOŽE upisati kao vlasnik u zemljišne knjige.|"
            "Porez na promet nekretnina iznosi 3% — plaća ga kupac."
        ),
        "aia_zakoni": "čl. 9. Zakona o vlasništvu, čl. 376. ZOO, čl. 52. ZZK",
        "modul_pro": "Ugovori",
    },
    {
        "id": "ugovor_o_djelu",
        "naslov": "Ugovor o djelu (majstor)",
        "opis": "Dogovor s majstorom za renovaciju, popravak ili ugradnju",
        "aia": (
            "Bez pisanog ugovora, ne možete dokazati dogovorenu cijenu "
            "niti rok završetka radova.|"
            "Izvođač odgovara za nedostatke rada 2 godine od završetka "
            "(čl. 633. ZOO). Bez ugovora, teško ćete to dokazati.|"
            "Ugovor mora navesti: opis posla, cijenu, rok, tko nabavlja materijal "
            "i što se događa ako radovi kasne."
        ),
        "aia_zakoni": "čl. 590.-619., čl. 633. ZOO",
        "modul_pro": "Obvezno pravo",
    },
    {
        "id": "kupoprodaja_stvari",
        "naslov": "Kupoprodaja stvari",
        "opis": "Prodaješ/kupuješ namještaj, elektroniku, opremu između dvoje ljudi",
        "aia": (
            "Za stvari veće vrijednosti (>500 EUR) pisani ugovor je bitna zaštita — "
            "dokazuje cijenu, stanje stvari i identitet kupca/prodavatelja.|"
            "Prodavatelj odgovara za skrivene nedostatke "
            "(čl. 400. ZOO) čak i kod rabljenih stvari.|"
            "Bez ugovora, kupac ne može dokazati da je stvar kupljena, "
            "a ne pokradena."
        ),
        "aia_zakoni": "čl. 376.-437. ZOO",
        "modul_pro": "Ugovori",
    },
    {
        "id": "suglasnost_stana",
        "naslov": "Suglasnost za korištenje stana",
        "opis": "Vlasnik stana daje suglasnost za prijavu prebivališta",
        "aia": (
            "MUP zahtijeva pisanu suglasnost vlasnika za prijavu prebivališta "
            "na tuđoj adresi (čl. 5. Zakona o prebivalištu).|"
            "Bez suglasnosti ne možete prijaviti prebivalište, "
            "što blokira osobnu iskaznicu, zdravstveno i ostala prava.|"
            "Suglasnost mora sadržavati potpis vlasnika i podatke o nekretnini."
        ),
        "aia_zakoni": "čl. 5. Zakona o prebivalištu (NN 144/12)",
        "modul_pro": "Ugovori",
    },
    {
        "id": "kupoprodaja_plovila",
        "naslov": "Kupoprodaja plovila",
        "opis": "Ugovor za čamac, gumenjak, jet-ski ili brodicu",
        "aia": (
            "Plovila registrirana u Lučkoj kapetaniji zahtijevaju pisani ugovor "
            "za prijenos vlasništva.|"
            "Prodavatelj odgovara za skrivene nedostatke 2 godine "
            "(čl. 404. st. 2. ZOO) — motor, trup, oprema.|"
            "Bez ugovora s brojem trupa (HIN), ne možete obaviti prijenos registracije."
        ),
        "aia_zakoni": "čl. 286., čl. 400.-410. ZOO, Pomorski zakonik",
        "modul_pro": "Ugovori",
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


def _generiraj_blank_motocikl():
    return (
        f"<div class='header-doc'>UGOVOR O KUPOPRODAJI MOTOCIKLA</div>"
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
        f"<div class='doc-body'>Prodavatelj prodaje, a Kupac kupuje motocikl:"
        f"<br>Marka i model: {_bp()}"
        f"<br>Kubikaza (ccm): {_bp(10)}"
        f"<br>Kategorija (AM/A1/A2/A): {_bp(5)}"
        f"<br>Tip motora: {_bp(15)}"
        f"<br>Broj motora: {_bp(20)}"
        f"<br>Broj šasije (VIN): {_bp(17)}"
        f"<br>Registarska oznaka: {_bp(15)}"
        f"<br>Godina proizvodnje: {_bp(10)}"
        f"<br>Stanje kilometara: {_bp(15)} km</div>"
        f"<div class='section-title'>Članak 2. — Cijena</div>"
        f"<div class='doc-body'>Kupac se obvezuje platiti kupoprodajnu cijenu u iznosu od "
        f"{_bp(15)} EUR (slovima: {_bp()})."
        f"<br>Način plaćanja (zaokružiti): gotovina / uplata na račun / na rate</div>"
        f"<div class='section-title'>Članak 3. — Predaja motocikla</div>"
        f"<div class='doc-body'>Prodavatelj se obvezuje predati motocikl Kupcu "
        f"dana ___.___.________. u stanju u kakvom se nalazi u trenutku sklapanja ovog Ugovora.</div>"
        f"<div class='section-title'>Članak 4. — Odgovornost za nedostatke</div>"
        f"<div class='doc-body'>Prodavatelj jamči da motocikl nema pravnih nedostataka "
        f"(da nije predmet spora, ovrhe niti založen). Prodavatelj odgovara za skrivene materijalne "
        f"nedostatke sukladno čl. 400.-410. Zakona o obveznim odnosima.</div>"
        f"<div class='section-title'>Članak 5. — Prijenos vlasništva</div>"
        f"<div class='doc-body'>Kupac stječe pravo vlasništva predajom motocikla i "
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


def _generiraj_blank_primopredajni():
    return (
        f"<div class='header-doc'>ZAPISNIK O PRIMOPREDAJI STANA</div>"
        f"<div class='doc-body'>Sastavljen u {_bp(20)}, dana ___.___.________. godine.</div>"
        f"<div class='party-info'>"
        f"1. <b>NAJMODAVAC (predaje):</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='party-info'>"
        f"2. <b>NAJMOPRIMAC (prima):</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='section-title'>I. PODACI O STANU</div>"
        f"<div class='doc-body'>"
        f"Adresa stana: {_bp()}<br>"
        f"Broj soba: {_bp(5)}, Površina: {_bp(10)} m²<br>"
        f"Kat: {_bp(5)}, Broj stana: {_bp(5)}</div>"
        f"<div class='section-title'>II. STANJA BROJILA</div>"
        f"<div class='doc-body'>"
        f"Struja — broj brojila: {_bp(15)}, stanje: {_bp(10)} kWh<br>"
        f"Voda — broj brojila: {_bp(15)}, stanje: {_bp(10)} m³<br>"
        f"Plin — broj brojila: {_bp(15)}, stanje: {_bp(10)} m³</div>"
        f"<div class='section-title'>III. POPIS OŠTEĆENJA</div>"
        f"<div class='doc-body'>"
        f"1. {_bp(50)}<br>"
        f"2. {_bp(50)}<br>"
        f"3. {_bp(50)}<br>"
        f"4. {_bp(50)}</div>"
        f"<div class='section-title'>IV. POPIS INVENTARA</div>"
        f"<div class='doc-body'>"
        f"1. {_bp(50)}<br>"
        f"2. {_bp(50)}<br>"
        f"3. {_bp(50)}<br>"
        f"4. {_bp(50)}</div>"
        f"<div class='section-title'>V. KLJUČEVI</div>"
        f"<div class='doc-body'>"
        f"Broj predanih ključeva: {_bp(5)} komada<br>"
        f"Napomena: {_bp(40)}</div>"
        f"<div class='section-title'>VI. NAPOMENE</div>"
        f"<div class='doc-body'>{_bp(50)}<br>{_bp(50)}</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>NAJMODAVAC</b><br><br><br>______________________</div>"
        f"<div class='signature-block'><b>NAJMOPRIMAC</b><br><br><br>______________________</div>"
        f"</div>"
    )


def _generiraj_blank_raskid_najma():
    return (
        f"<div class='header-doc'>SPORAZUMNI RASKID UGOVORA O NAJMU</div>"
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
        f"<div class='section-title'>Članak 1. — Referenca na ugovor</div>"
        f"<div class='doc-body'>Stranke su dana ___.___.________. sklopile Ugovor o najmu stana "
        f"na adresi {_bp()}, koji ovim Sporazumom sporazumno raskidaju.</div>"
        f"<div class='section-title'>Članak 2. — Datum raskida</div>"
        f"<div class='doc-body'>Ugovor o najmu prestaje važiti dana ___.___.________. "
        f"(zadnji dan najma). Najmoprimac se obvezuje iseliti i predati stan Najmodavcu "
        f"najkasnije do tog datuma.</div>"
        f"<div class='section-title'>Članak 3. — Jamčevina</div>"
        f"<div class='doc-body'>Najmodavac se obvezuje (zaokružiti):"
        f"<br>a) vratiti jamčevinu u punom iznosu od {_bp(15)} EUR"
        f"<br>b) zadržati jamčevinu u cijelosti"
        f"<br>c) vratiti djelomično iznos od {_bp(15)} EUR"
        f"<br>Razlog zadržavanja: {_bp(40)}</div>"
        f"<div class='section-title'>Članak 4. — Režijski troškovi</div>"
        f"<div class='doc-body'>Najmoprimac se obvezuje podmiriti sve režijske troškove "
        f"(struja, voda, plin, pričuva) zaključno s datumom ___.___.________.</div>"
        f"<div class='section-title'>Članak 5. — Stanje stana</div>"
        f"<div class='doc-body'>Stanje stana utvrdit će se primopredajnim zapisnikom "
        f"na dan iseljenja.</div>"
        f"<div class='section-title'>Članak 6. — Završne odredbe</div>"
        f"<div class='doc-body'>Ovaj Sporazum sastavljen je u 2 (dva) istovjetna primjerka, "
        f"po jedan za svaku ugovornu stranu.</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>NAJMODAVAC</b><br><br><br>______________________</div>"
        f"<div class='signature-block'><b>NAJMOPRIMAC</b><br><br><br>______________________</div>"
        f"</div>"
    )


def _generiraj_blank_potvrda_povrata():
    return (
        f"<div class='header-doc'>POTVRDA O POVRATU DUGA</div>"
        f"<div class='doc-body'>Izdana u {_bp(20)}, dana ___.___.________. godine.</div>"
        f"<br>"
        f"<div class='party-info'>"
        f"<b>VJEROVNIK:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='party-info'>"
        f"<b>DUŽNIK:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<br>"
        f"<div class='doc-body'>Ja, kao Vjerovnik, ovime potvrđujem da je Dužnik "
        f"<b>u cijelosti vratio</b> dug u iznosu od:</div>"
        f"<div class='doc-body' style='margin-top:0.5rem;'>"
        f"<b>Iznos: {_bp(15)} EUR</b> (slovima: {_bp()})</div>"
        f"<div class='section-title'>Osnova duga</div>"
        f"<div class='doc-body'>(zaokružiti/upisati): zajam / račun / opomena "
        f"od dana ___.___.________.<br>"
        f"Opis: {_bp(40)}</div>"
        f"<div class='section-title'>Način povrata</div>"
        f"<div class='doc-body'>(zaokružiti): gotovina / uplata na račun / "
        f"drugi način: {_bp(20)}<br>"
        f"Datum povrata: ___.___.________.</div>"
        f"<br>"
        f"<div class='doc-body' style='border:1px solid #666;padding:10px;'>"
        f"Vjerovnik izjavljuje da <b>nema daljnjih potraživanja</b> prema Dužniku "
        f"po navedenoj osnovi te da je dug u potpunosti podmiren.</div>"
        f"<br>"
        f"<div class='doc-body'>Ovu potvrdu čuvajte minimalno 5 godina "
        f"(opći rok zastare, čl. 225. ZOO).</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>VJEROVNIK</b><br><br><br>______________________<br>"
        f"(vlastoručni potpis)</div>"
        f"</div>"
    )


def _generiraj_blank_predugovor_kapara():
    return (
        f"<div class='header-doc'>PREDUGOVOR O KUPOPRODAJI NEKRETNINE S KAPAROM</div>"
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
        f"<div class='section-title'>Članak 1. — Predmet predugovora</div>"
        f"<div class='doc-body'>Stranke se obvezuju sklopiti glavni ugovor o kupoprodaji nekretnine:"
        f"<br>Adresa: {_bp()}"
        f"<br>ZK uložak br.: {_bp(15)}, k.o. {_bp(15)}"
        f"<br>Površina: {_bp(10)} m²</div>"
        f"<div class='section-title'>Članak 2. — Cijena</div>"
        f"<div class='doc-body'>Dogovorena kupoprodajna cijena iznosi "
        f"<b>{_bp(15)} EUR</b> (slovima: {_bp()}).</div>"
        f"<div class='section-title'>Članak 3. — Kapara</div>"
        f"<div class='doc-body'>Kupac uplaćuje kaparu u iznosu od <b>{_bp(15)} EUR</b> "
        f"(slovima: {_bp()})."
        f"<br>Način uplate (zaokružiti): gotovina / uplata na IBAN: {_bp(25)}"
        f"<br><br>Sukladno čl. 303. ZOO:"
        f"<br>— Kapara se uračunava u kupoprodajnu cijenu."
        f"<br>— Ako Kupac odustane, gubi kaparu."
        f"<br>— Ako Prodavatelj odustane, vraća Kupcu dvostruku kaparu.</div>"
        f"<div class='section-title'>Članak 4. — Rok za glavni ugovor</div>"
        f"<div class='doc-body'>Stranke se obvezuju sklopiti glavni ugovor o kupoprodaji "
        f"najkasnije do ___.___.________. godine.</div>"
        f"<div class='section-title'>Članak 5. — Završne odredbe</div>"
        f"<div class='doc-body'>Za sve što nije uređeno ovim Predugovorom, "
        f"primjenjuju se odredbe Zakona o obveznim odnosima. "
        f"Ovaj Predugovor sastavljen je u 2 (dva) istovjetna primjerka.</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>PRODAVATELJ</b><br><br><br>______________________</div>"
        f"<div class='signature-block'><b>KUPAC</b><br><br><br>______________________</div>"
        f"</div>"
    )


def _generiraj_blank_kupoprodaja_nekretnine():
    return (
        f"<div class='header-doc'>UGOVOR O KUPOPRODAJI NEKRETNINE</div>"
        f"<div class='doc-body'>Sklopljen u {_bp(20)}, dana ___.___.________. godine, između:</div>"
        f"<div class='party-info'>"
        f"1. <b>PRODAVATELJ:</b><br>"
        f"Ime i prezime/Naziv: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='party-info'>"
        f"2. <b>KUPAC:</b><br>"
        f"Ime i prezime/Naziv: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='section-title'>Članak 1. — Predmet ugovora</div>"
        f"<div class='doc-body'>Prodavatelj prodaje, a Kupac kupuje nekretninu:"
        f"<br>Adresa: {_bp()}"
        f"<br>ZK uložak br.: {_bp(15)}, k.o. {_bp(15)}"
        f"<br>Kat. čestica br.: {_bp(15)}"
        f"<br>Površina: {_bp(10)} m²"
        f"<br>Etaža/Kat: {_bp(10)}"
        f"<br>Opis: {_bp(40)}</div>"
        f"<div class='section-title'>Članak 2. — Cijena i način plaćanja</div>"
        f"<div class='doc-body'>Kupoprodajna cijena iznosi <b>{_bp(15)} EUR</b> "
        f"(slovima: {_bp()})."
        f"<br>Način plaćanja (zaokružiti): jednokratno / u ratama / putem kredita"
        f"<br>IBAN prodavatelja: {_bp(25)}</div>"
        f"<div class='section-title'>Članak 3. — Clausula intabulandi</div>"
        f"<div class='doc-body'>Prodavatelj izričito i bezuvjetno dozvoljava da se na temelju "
        f"ovog Ugovora u zemljišnim knjigama kod nadležnog suda izvrši uknjižba prava vlasništva "
        f"na nekretnini iz čl. 1. ovog Ugovora u korist Kupca.</div>"
        f"<div class='section-title'>Članak 4. — Jamstva prodavatelja</div>"
        f"<div class='doc-body'>Prodavatelj jamči:"
        f"<br>— da je isključivi vlasnik nekretnine"
        f"<br>— da nekretnina nije opterećena hipotekom, služnošću niti drugim teretom"
        f"<br>— da se ne vodi spor niti ovrha u vezi nekretnine"
        f"<br>— da nema dugovanja po osnovi pričuve, komunalnih naknada i poreza</div>"
        f"<div class='section-title'>Članak 5. — Troškovi</div>"
        f"<div class='doc-body'>Porez na promet nekretnina (3%) snosi Kupac. "
        f"Troškove javnog bilježnika stranke snose (zaokružiti): "
        f"svaka svoju polovicu / Kupac / Prodavatelj.</div>"
        f"<div class='section-title'>Članak 6. — Primopredaja</div>"
        f"<div class='doc-body'>Prodavatelj se obvezuje predati nekretninu Kupcu "
        f"najkasnije do ___.___.________. godine, uključujući sve ključeve.</div>"
        f"<div class='section-title'>Članak 7. — Završne odredbe</div>"
        f"<div class='doc-body'>Ovaj Ugovor sastavljen je u {_bp(5)} istovjetnih primjeraka. "
        f"Za sporove je nadležan sud u {_bp(20)}.</div>"
        f"<br>"
        f"<div class='doc-body' style='border:1px solid #666;padding:10px;'>"
        f"<b>NAPOMENA:</b> Ovaj ugovor zahtijeva ovjeru kod javnog bilježnika "
        f"(čl. 9. Zakona o vlasništvu i drugim stvarnim pravima).</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>PRODAVATELJ</b><br><br><br>______________________</div>"
        f"<div class='signature-block'><b>KUPAC</b><br><br><br>______________________</div>"
        f"</div>"
    )


def _generiraj_blank_ugovor_o_djelu():
    return (
        f"<div class='header-doc'>UGOVOR O DJELU</div>"
        f"<div class='doc-body'>Sklopljen u {_bp(20)}, dana ___.___.________. godine, između:</div>"
        f"<div class='party-info'>"
        f"1. <b>NARUČITELJ:</b><br>"
        f"Ime i prezime/Naziv: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='party-info'>"
        f"2. <b>IZVOĐAČ:</b><br>"
        f"Ime i prezime/Naziv: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='section-title'>Članak 1. — Predmet ugovora (opis radova)</div>"
        f"<div class='doc-body'>"
        f"Izvođač se obvezuje izvršiti sljedeće radove:<br>"
        f"1. {_bp(50)}<br>"
        f"2. {_bp(50)}<br>"
        f"3. {_bp(50)}<br>"
        f"4. {_bp(50)}</div>"
        f"<div class='section-title'>Članak 2. — Materijal</div>"
        f"<div class='doc-body'>Materijal za izvođenje radova nabavlja (zaokružiti): "
        f"Naručitelj / Izvođač."
        f"<br>Troškove materijala snosi (zaokružiti): Naručitelj / Izvođač / podijeljeno.</div>"
        f"<div class='section-title'>Članak 3. — Cijena</div>"
        f"<div class='doc-body'>Ukupna cijena radova iznosi <b>{_bp(15)} EUR</b> "
        f"(slovima: {_bp()})."
        f"<br>Način plaćanja (zaokružiti):"
        f"<br>a) avans {_bp(10)} EUR + ostatak po završetku"
        f"<br>b) u cijelosti po završetku radova"
        f"<br>c) u ratama: {_bp(30)}</div>"
        f"<div class='section-title'>Članak 4. — Rokovi</div>"
        f"<div class='doc-body'>Početak radova: ___.___.________."
        f"<br>Završetak radova: ___.___.________.</div>"
        f"<div class='section-title'>Članak 5. — Jamstvo za kvalitetu</div>"
        f"<div class='doc-body'>Izvođač odgovara za nedostatke rada u skladu s "
        f"čl. 633. ZOO (2 godine od završetka radova). "
        f"Izvođač se obvezuje o svom trošku otkloniti sve nedostatke "
        f"nastale uslijed neispravnog izvođenja.</div>"
        f"<div class='section-title'>Članak 6. — Ugovorna kazna za kašnjenje</div>"
        f"<div class='doc-body'>(opcionalno) U slučaju prekoračenja roka, Izvođač plaća "
        f"ugovornu kaznu u iznosu od {_bp(10)} EUR za svaki dan kašnjenja, "
        f"ali ne više od {_bp(10)} % ukupne cijene.</div>"
        f"<div class='section-title'>Članak 7. — Završne odredbe</div>"
        f"<div class='doc-body'>Ovaj Ugovor sastavljen je u 2 (dva) istovjetna primjerka. "
        f"Za sporove je nadležan sud u {_bp(20)}.</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>NARUČITELJ</b><br><br><br>______________________</div>"
        f"<div class='signature-block'><b>IZVOĐAČ</b><br><br><br>______________________</div>"
        f"</div>"
    )


def _generiraj_blank_kupoprodaja_stvari():
    return (
        f"<div class='header-doc'>UGOVOR O KUPOPRODAJI STVARI</div>"
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
        f"<div class='doc-body'>Prodavatelj prodaje, a Kupac kupuje sljedeću stvar:"
        f"<br>Naziv/Opis: {_bp()}"
        f"<br>Stanje (zaokružiti): novo / rabljeno"
        f"<br>Serijski broj (ako postoji): {_bp(20)}</div>"
        f"<div class='section-title'>Članak 2. — Cijena</div>"
        f"<div class='doc-body'>Kupoprodajna cijena iznosi <b>{_bp(15)} EUR</b> "
        f"(slovima: {_bp()})."
        f"<br>Način plaćanja (zaokružiti): gotovina / uplata na račun</div>"
        f"<div class='section-title'>Članak 3. — Predaja</div>"
        f"<div class='doc-body'>Predaja stvari obavlja se dana ___.___.________. "
        f"na lokaciji: {_bp()}.</div>"
        f"<div class='section-title'>Članak 4. — Odgovornost za nedostatke</div>"
        f"<div class='doc-body'>Prodavatelj odgovara za skrivene nedostatke stvari "
        f"sukladno čl. 400. ZOO. Kupac je dužan pregledati stvar prilikom preuzimanja.</div>"
        f"<div class='section-title'>Članak 5. — Završne odredbe</div>"
        f"<div class='doc-body'>Ovaj Ugovor sastavljen je u 2 (dva) istovjetna primjerka.</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>PRODAVATELJ</b><br><br><br>______________________</div>"
        f"<div class='signature-block'><b>KUPAC</b><br><br><br>______________________</div>"
        f"</div>"
    )


def _generiraj_blank_suglasnost():
    return (
        f"<div class='header-doc'>SUGLASNOST ZA KORIŠTENJE STANA</div>"
        f"<div class='doc-body'>Izdana u {_bp(20)}, dana ___.___.________. godine.</div>"
        f"<br>"
        f"<div class='doc-body'>Ja, <b>{_bp()}</b>, "
        f"OIB: {_bp(11)}, s prebivalištem na adresi {_bp()}, "
        f"kao vlasnik nekretnine na adresi:</div>"
        f"<div class='doc-body' style='margin-top:0.5rem;'>"
        f"Adresa stana: {_bp()}<br>"
        f"ZK uložak br.: {_bp(15)}, k.o. {_bp(15)}</div>"
        f"<br>"
        f"<div class='doc-body'>ovime dajem <b>suglasnost</b> osobi:</div>"
        f"<div class='party-info'>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Datum rođenja: ___.___.________.</div>"
        f"<br>"
        f"<div class='doc-body'>da koristi navedeni stan te da na toj adresi "
        f"<b>prijavi prebivalište</b> sukladno čl. 5. Zakona o prebivalištu (NN 144/12).</div>"
        f"<br>"
        f"<div class='doc-body'>Ova suglasnost vrijedi do opoziva.</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>VLASNIK STANA</b><br><br><br>______________________<br>"
        f"(vlastoručni potpis)</div>"
        f"</div>"
    )


def _generiraj_blank_plovilo():
    return (
        f"<div class='header-doc'>UGOVOR O KUPOPRODAJI PLOVILA</div>"
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
        f"<div class='doc-body'>Prodavatelj prodaje, a Kupac kupuje plovilo:"
        f"<br>Tip plovila (zaokružiti): čamac / gumenjak / jet-ski / brodica / jedrilica"
        f"<br>Marka i model: {_bp()}"
        f"<br>Duljina: {_bp(10)} m"
        f"<br>HIN (Hull Identification Number): {_bp(17)}"
        f"<br>Snaga motora: {_bp(10)} kW ({_bp(10)} KS)"
        f"<br>Broj motora: {_bp(20)}"
        f"<br>Registracija lučke kapetanije: {_bp(20)}"
        f"<br>Stanje radnih sati motora: {_bp(10)} h</div>"
        f"<div class='section-title'>Članak 2. — Cijena</div>"
        f"<div class='doc-body'>Kupoprodajna cijena iznosi <b>{_bp(15)} EUR</b> "
        f"(slovima: {_bp()})."
        f"<br>Način plaćanja (zaokružiti): gotovina / uplata na račun / na rate</div>"
        f"<div class='section-title'>Članak 3. — Predaja plovila</div>"
        f"<div class='doc-body'>Prodavatelj se obvezuje predati plovilo Kupcu "
        f"dana ___.___.________. u luci/marini: {_bp(20)}.</div>"
        f"<div class='section-title'>Članak 4. — Odgovornost za nedostatke</div>"
        f"<div class='doc-body'>Prodavatelj jamči da plovilo nema pravnih nedostataka. "
        f"Prodavatelj odgovara za skrivene materijalne nedostatke (motor, trup, oprema) "
        f"sukladno čl. 400.-410. ZOO.</div>"
        f"<div class='section-title'>Članak 5. — Prijenos vlasništva</div>"
        f"<div class='doc-body'>Kupac stječe pravo vlasništva predajom plovila. "
        f"Troškove prijenosa registracije pri Lučkoj kapetaniji snosi Kupac.</div>"
        f"<div class='section-title'>Članak 6. — Završne odredbe</div>"
        f"<div class='doc-body'>Ovaj Ugovor sastavljen je u 2 (dva) istovjetna primjerka. "
        f"Za sporove je nadležan sud u {_bp(20)}.</div>"
        f"<br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>PRODAVATELJ</b><br><br><br>______________________<br>"
        f"(vlastoručni potpis)</div>"
        f"<div class='signature-block'><b>KUPAC</b><br><br><br>______________________<br>"
        f"(vlastoručni potpis)</div>"
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
    "kupnja_motora": ("Kupoprodaja_motocikla.docx", _generiraj_blank_motocikl),
    "primopredajni": ("Primopredajni_zapisnik.docx", _generiraj_blank_primopredajni),
    "raskid_najma": ("Sporazumni_raskid_najma.docx", _generiraj_blank_raskid_najma),
    "potvrda_povrata": ("Potvrda_o_povratu_duga.docx", _generiraj_blank_potvrda_povrata),
    "predugovor_kapara": ("Predugovor_s_kaparom.docx", _generiraj_blank_predugovor_kapara),
    "kupoprodaja_nekretnine": ("Kupoprodaja_nekretnine.docx", _generiraj_blank_kupoprodaja_nekretnine),
    "ugovor_o_djelu": ("Ugovor_o_djelu.docx", _generiraj_blank_ugovor_o_djelu),
    "kupoprodaja_stvari": ("Kupoprodaja_stvari.docx", _generiraj_blank_kupoprodaja_stvari),
    "suglasnost_stana": ("Suglasnost_za_stan.docx", _generiraj_blank_suglasnost),
    "kupoprodaja_plovila": ("Kupoprodaja_plovila.docx", _generiraj_blank_plovilo),
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
        "<div class='hero-section'>"
        "<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;"
        "font-weight:600;color:rgba(255,255,255,0.5);margin-bottom:0.6rem !important;"
        "position:relative;z-index:1;'>Jednostavni mod</p>"
        "<h2 style='font-size:1.9rem !important;margin-bottom:0.5rem !important;"
        "line-height:1.2 !important;'>Brzi pravni dokumenti</h2>"
        "<p style='font-size:1rem !important;line-height:1.6 !important;'>"
        "Bez pravnog znanja. Odaberite situaciju, "
        "isprintajte dokument, ispunite rucno.</p>"
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
        "<div style='background:#FFF7ED;border:1px solid #FED7AA;border-radius:12px;"
        "padding:0.9rem 1.1rem;font-size:0.75rem;color:#92400E;line-height:1.6;'>"
        "<b>Napomena:</b> Ove informacije su opce pravne cinjenice iz javno dostupnih zakona, "
        "ne pravni savjet. Za slozene situacije konzultirajte odvjetnika. "
        "Dokumente provjerite prije potpisa."
        "</div>",
        unsafe_allow_html=True,
    )


_KATEGORIJE = [
    ("Nekretnine i stanovanje", [
        "najam_stana", "raskid_najma", "primopredajni", "suglasnost_stana",
        "predugovor_kapara", "kupoprodaja_nekretnine",
    ]),
    ("Vozila i plovila", [
        "kupnja_auta", "kupnja_motora", "kupoprodaja_plovila",
    ]),
    ("Novac i dugovi", [
        "posudba_novca", "potvrda_povrata", "dugovanje",
    ]),
    ("Kupovina i potrosaci", [
        "kupoprodaja_stvari", "reklamacija", "online_raskid",
    ]),
    ("Posao i usluge", [
        "ugovor_o_djelu", "punomoc", "osnivanje_tvrtke", "zaposlavanje",
    ]),
    ("Obitelj", [
        "bracni_ugovor", "sporazumni_razvod",
    ]),
]

# Brzi lookup situacija po ID-u
_SIT_PO_ID = {s["id"]: s for s in _SITUACIJE}


def _prikazi_situacije():
    """Prikaz kartica sa situacijama, grupirano po kategorijama."""
    st.markdown("##### Što vam treba?")

    btn_idx = 0
    for kat_naslov, kat_ids in _KATEGORIJE:
        st.markdown(
            f"<div style='margin:1.2rem 0 0.5rem;padding-bottom:0.3rem;"
            f"border-bottom:2px solid #E2E0DC;'>"
            f"<span style='font-size:0.8rem;font-weight:700;color:#162D50;"
            f"text-transform:uppercase;letter-spacing:0.06em;'>"
            f"{kat_naslov}</span></div>",
            unsafe_allow_html=True,
        )
        situacije = [_SIT_PO_ID[sid] for sid in kat_ids if sid in _SIT_PO_ID]
        cols = st.columns(2)
        for j, sit in enumerate(situacije):
            with cols[j % 2]:
                kata_oznaka = (
                    "<span style='background:#7C3AED;color:white;padding:2px 8px;"
                    "border-radius:4px;font-size:0.55rem;font-weight:700;"
                    "letter-spacing:0.05em;text-transform:uppercase;"
                    "margin-left:6px;'>VODIC</span>"
                    if sit.get("kata") else ""
                )
                st.markdown(
                    f"<div class='module-card'>"
                    f"<div style='display:flex;align-items:center;gap:0.75rem;'>"
                    f"<span style='background:#162D50;min-width:2.1rem;height:2.1rem;"
                    f"border-radius:8px;display:inline-flex;align-items:center;justify-content:center;"
                    f"flex-shrink:0;'>"
                    f"{_IKONE.get(sit['id'], '')}</span>"
                    f"<div>"
                    f"<b style='color:#162D50;font-size:0.95rem;letter-spacing:-0.01em;'>"
                    f"{sit['naslov']}</b>"
                    f"{kata_oznaka}"
                    f"<br><span style='color:#3D4A5C;font-size:0.82rem;line-height:1.5;'>"
                    f"{sit['opis']}</span>"
                    f"</div></div></div>",
                    unsafe_allow_html=True,
                )
                if st.button("Odaberi", key=f"_jed_sit_{btn_idx}", use_container_width=True):
                    st.session_state._jed_odabir = sit["id"]
                    st.rerun()
                btn_idx += 1


def _prikazi_detalje(situacija, navigate_fn):
    """Prikaz detalja situacije: AIA + blank DOCX + opcija za Pro."""

    # Scroll na vrh kad se otvore detalji
    _scroll_to_top()

    # Gumb za nazad
    if st.button("← Natrag na sve situacije", key="_jed_nazad"):
        st.session_state._jed_odabir = None
        st.rerun()

    st.markdown(f"### {situacija['naslov']}")

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
        boja_broja = "#162D50"
        st.markdown(
            f"<div style='background:white;border:1px solid #DDD8D0;border-radius:14px;"
            f"padding:1.1rem 1.3rem;margin-bottom:0.8rem;"
            f"border-left:4px solid {boja_broja};"
            f"box-shadow:0 2px 8px rgba(22,45,80,0.05);'>"
            f"<div style='display:flex;align-items:flex-start;gap:0.8rem;'>"
            f"<div style='background:{boja_broja};color:white;min-width:2rem;height:2rem;"
            f"border-radius:50%;display:flex;align-items:center;justify-content:center;"
            f"font-weight:700;font-size:0.9rem;'>{korak['broj']}</div>"
            f"<div>"
            f"<div style='font-weight:700;color:#162D50;font-size:0.95rem;"
            f"margin-bottom:0.3rem;'>{korak['naslov']}</div>"
            f"<div style='color:#3D4A5C;font-size:0.85rem;line-height:1.5;'>{korak['opis']}</div>"
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
