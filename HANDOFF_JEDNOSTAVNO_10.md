# HANDOFF — 10 novih blank dokumenata za jednostavni mod

**Datum:** 2026-03-23
**Status:** Ikone dodane (10 novih), ostaje: situacije + generatori + registracija

---

## ŠTO JE NAPRAVLJENO

1. U `stranice/jednostavno.py` dodano 10 novih SVG ikona u `_IKONE` dict:
   `kupnja_motora`, `primopredajni`, `raskid_najma`, `potvrda_povrata`, `predugovor_kapara`, `kupoprodaja_nekretnine`, `ugovor_o_djelu`, `kupoprodaja_stvari`, `suglasnost_stana`, `kupoprodaja_plovila`

---

## ŠTO TREBA NAPRAVITI

### Korak 1: Dodati 10 novih situacija u `_SITUACIJE` listu

Dodati PRIJE `]` na liniji 281 (nakon sporazumni_razvod entry-ja):

```python
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
```

### Korak 2: Dodati 10 novih `_generiraj_blank_*` funkcija

Dodati PRIJE linije `# Mapiranje ID-a situacije na generator blank dokumenta`. Svaka funkcija koristi `_bp()` helper za prazna polja. Koristiti isti HTML pattern kao postojeći generatori (`header-doc`, `party-info`, `doc-body`, `section-title`, `signature-row`, `signature-block`).

Dokumenti za generiranje:

#### 1. `_generiraj_blank_motocikl()`
Kao kupoprodaja auta ali s poljima: marka/model, kubikaza, broj motora, VIN, registracija, kategorija (AM/A1/A2/A), stanje km.

#### 2. `_generiraj_blank_primopredajni()`
Zapisnik s: datum, najmodavac, najmoprimac, adresa stana, broj soba, stanja brojila (struja, voda, plin), popis oštećenja (3-4 retka), popis inventara (3-4 retka), ključevi (broj komada), potpisi obiju strana.

#### 3. `_generiraj_blank_raskid_najma()`
Sporazumni raskid: stranke, referenca na originalni ugovor o najmu (datum, adresa), zadnji dan najma, stanje jamčevine (vraća se / zadržava / djelomično), obveza podmirenja režija do datuma, potpisi.

#### 4. `_generiraj_blank_potvrda_povrata()`
Kratki dokument: vjerovnik potvrđuje da je dužnik vratio iznos X EUR, osnova duga (zajam/račun/opomena od datuma), način plaćanja (gotovina/uplata), vjerovnik nema daljnjih potraživanja po toj osnovi, datum, potpis vjerovnika.

#### 5. `_generiraj_blank_predugovor_kapara()`
Predugovor: stranke, opis nekretnine (adresa, ZK uložak, površina), dogovorena cijena, kapara (iznos, način uplate, IBAN), rok za sklapanje glavnog ugovora, čl. 303 ZOO (kapara se uračunava u cijenu, ako kupac odustane gubi kaparu, ako prodavatelj odustane vraća dvostruku), potpisi.

#### 6. `_generiraj_blank_kupoprodaja_nekretnine()`
Puni ugovor: stranke s OIB, opis nekretnine (adresa, ZK uložak, kat. čestica, površina, etaža), cijena i način plaćanja, clausula intabulandi (izjava prodavatelja da dozvoljava uknjižbu), jamstvo da nema tereta/hipoteka/ovrha, troškovi (porez kupac, JB po dogovoru), primopredaja (rok, ključevi), završne odredbe, potpisi. Napomena: OVA VERZIJA ZAHTIJEVA OVJERU KOD JAVNOG BILJEŽNIKA.

#### 7. `_generiraj_blank_ugovor_o_djelu()`
Stranke (naručitelj + izvođač), opis radova (3-4 retka), materijal (tko nabavlja, tko plaća), cijena (ukupno ili po stavkama), način plaćanja (avans/po završetku/rate), rok početka i završetka, jamstvo za kvalitetu radova (čl. 633 ZOO, 2 godine), ugovorna kazna za kašnjenje (opcionalno), potpisi.

#### 8. `_generiraj_blank_kupoprodaja_stvari()`
Jednostavan ugovor: stranke, opis stvari (naziv, stanje novo/rabljeno, serijski broj ako postoji), cijena, način plaćanja, predaja (datum/mjesto), prodavatelj jamči za nedostatke čl. 400 ZOO, potpisi.

#### 9. `_generiraj_blank_suglasnost()`
Kratka izjava: vlasnik (ime, OIB, adresa) daje suglasnost osobi (ime, OIB) da koristi stan na adresi (adresa, ZK podaci) za prijavu prebivališta. Suglasnost vrijedi do opoziva. Datum, potpis vlasnika.

#### 10. `_generiraj_blank_plovilo()`
Kao kupoprodaja auta ali s poljima: tip plovila (čamac/gumenjak/jet-ski/brodica), marka/model, duljina, HIN (hull identification number), snaga motora (kW/KS), broj motora, registracija lučke kapetanije, stanje radnih sati motora.

### Korak 3: Registrirati u `_BLANK_GENERATORI` dict

Dodati u `_BLANK_GENERATORI`:
```python
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
```

---

## REFERENCA: Pattern za blank generator

```python
def _generiraj_blank_NAZIV():
    return (
        f"<div class='header-doc'>NASLOV DOKUMENTA</div>"
        f"<div class='doc-body'>Sklopljen u {_bp(20)}, dana ___.___.________. godine, između:</div>"
        f"<div class='party-info'>"
        f"1. <b>STRANKA 1:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        f"<div class='party-info'>"
        f"2. <b>STRANKA 2:</b><br>"
        f"Ime i prezime: {_bp()}<br>"
        f"OIB: {_bp(11)}<br>"
        f"Adresa: {_bp()}</div>"
        # ... članci ...
        f"<div class='section-title'>Članak 1. — Predmet</div>"
        f"<div class='doc-body'>Tekst s {_bp()} praznim poljima</div>"
        # ... potpisi ...
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>STRANKA 1</b><br><br><br>______________________</div>"
        f"<div class='signature-block'><b>STRANKA 2</b><br><br><br>______________________</div>"
        f"</div>"
    )
```

Helper: `_bp(sirina=30)` vraća `"_" * sirina` — crta za ručni upis.

---

## INOVACIJA KONTEKST

U istoj sesiji napravljena je inovacija "Transparentna Ekvivalencija" (TE) za LEGAL-SUITE53 projekt.
Svi artefakti su u: `C:/Users/Hrvoje Matej/Desktop/PRAKTIČNA PRIMJENA AI-ja U PRAVU/MD verzije/claude/PROJEKTI/LEGAL-SUITE53/`
- PLAN.md, CUDNI_IZVORI.md, FILOZOFIRANJE_SLOJ_PRVI.md, PRIMJENA_A.md, PRIMJENA_B.md
- SLOJ_DRUGI.md, SLOJ_2_5_NUMEROLOGY_TEST.md, SLOJ_TRECI.md (KANDIDAT), STRES_TEST.md
- Ocjena: A- (7/7 testova, implementabilno)

TE implementacija (vizualna transformacija narativ→klauzula) je ZASEBNA od ovih 10 blank dokumenata — može se raditi poslije.
