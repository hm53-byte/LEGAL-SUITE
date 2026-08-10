# =============================================================================
# PRIVATNOST.PY - obavijest o obradi u trenutku prikupljanja (GDPR cl. 13)
# =============================================================================
# Politika privatnosti postoji kao zasebna stranica ("Pravila i privatnost"),
# ali clanak 13. Opce uredbe trazi da ispitanik obavijest dobije U TRENUTKU
# prikupljanja, na mjestu na kojem podatke daje. Zato ovaj modul: jedan tekst,
# jedna funkcija, pozvana na svakom mjestu na kojem se podaci doista unose.
#
# Pravilo za sadrzaj: ovdje smije stajati samo ono sto se moze pokazati u kodu.
# Sve ostalo je oznaceno kao neutvrdjeno ili nosi oznaku
# "<<< VLASNIK UPISUJE: ... >>>", istu koja se koristi u
# stranice/privacy_policy.md. Izmisljen rok cuvanja je gora greska od
# izostavljenog roka.
#
# Izvori tvrdnji u tekstu (provjereno citanjem koda 2026-08-10):
#   dokument  - docx_export.pripremi_za_docx gradi .docx u BytesIO i vraca
#               bajtove; nigdje se ne zapisuje na disk. entitlements.record_download
#               izlazi bez upisa kad nema oznake korisnika (redci 246-248), a
#               auth.py je ne stvara, pa zapisa o preuzimanju nema.
#   kalendar  - stranice/kalendar.py: _spremi_u_datoteku pise u _data/kalendar.json,
#               _dohvati_eventi cita cijelu datoteku bez filtra po korisniku.
#               Brisanje postoji samo kao gumb "Ukloni"; automatskog nema.
#   racun     - auth.py: _save_users pise u .users.json (ime, e-mail, PBKDF2-SHA256
#               sazetak lozinke, datum, uloga). Brisanja racuna u kodu nema.
#   pretraga  - api_nn.pretrazi_nn salje upit na narodne-novine.nn.hr i rezultat
#               drzi u st.cache_data s ttl=3600.

import streamlit as st

# Naziv modula u izborniku (LEGAL-SUITE.py, _MODULI). Ako se preimenuje,
# poveznica iz obavijesti prestaje voditi na politiku, pa to hvata test.
MODUL_POLITIKA = "Pravila i privatnost"

# Voditelj obrade nije upisan ni u politici privatnosti (clanak 1). Dok je tako,
# obavijest ga ne smije izmisliti. Ista oznaka, isti razlog.
VODITELJ_PLACEHOLDER = (
    "<<< VLASNIK UPISUJE: naziv, adresa i e-mail voditelja obrade >>>"
)

_TKO = (
    "**Tko obrađuje:** " + VODITELJ_PLACEHOLDER + ". "
    "Voditelj obrade još nije upisan ni u politiku privatnosti, pa se ovdje ne "
    "može imenovati."
)

_PRAVA = (
    "**Vaša prava:** pristup podacima, ispravak, brisanje, ograničenje obrade, "
    "prenosivost i prigovor. Zahtjev se šalje na kontakt voditelja obrade iz "
    "prve točke, koji još nije upisan; dok je tako, zahtjev nema kamo. "
    "Pritužbu možete podnijeti Agenciji za zaštitu osobnih podataka "
    "(https://azop.hr)."
)

# Svaki kontekst opisuje jedno stvarno mjesto prikupljanja. Tekst je ovdje i
# nigdje drugdje; stranice ga ne prepisuju.
KONTEKSTI = {
    "dokument": {
        "naslov": "Što se događa s podacima koje upišete u obrazac",
        "prikuplja": (
            "**Što se prikuplja:** sve što sami upišete u polja obrasca. To u "
            "pravilu uključuje ime ili naziv, OIB, adresu i podatke o predmetu, "
            "a može uključivati i podatke o drugim osobama koje spominjete."
        ),
        "svrha": (
            "**Svrha:** popunjavanje predloška koji ste odabrali i izrada .docx "
            "datoteke koju preuzimate. Ni za što drugo: nema profiliranja, "
            "oglašavanja ni učenja modela."
        ),
        "osnova": (
            "**Osnova:** obrada je nužna za uslugu koju ste sami zatražili "
            "(čl. 6. st. 1. t. (b) Opće uredbe)."
        ),
        "cuvanje": (
            "**Koliko se čuva:** ne čuva se. Upisani sadržaj postoji samo u "
            "memoriji poslužitelja dok traje izrada dokumenta; gotova datoteka "
            "gradi se u memoriji i predaje vam se na preuzimanje, bez zapisa na "
            "disk i bez kopije. Za preuzimanja je u bazi predviđen zapis bez "
            "sadržaja dokumenta, ali se u ovoj postavi ne stvara jer prijava ne "
            "stvara oznaku korisnika."
        ),
        "upozorenje": "",
    },
    "kalendar": {
        "naslov": "Što se događa s podacima koje upišete u kalendar",
        "prikuplja": (
            "**Što se prikuplja:** naslov, datum i vrijeme, opis, tip događaja, "
            "broj predmeta i, ako je upišete, e-mail adresa za podsjetnik."
        ),
        "svrha": (
            "**Svrha:** prikaz događaja u kalendaru i slanje podsjetnika e-mailom."
        ),
        "osnova": (
            "**Osnova:** obrada je nužna za uslugu koju ste sami zatražili "
            "(čl. 6. st. 1. t. (b) Opće uredbe)."
        ),
        "cuvanje": (
            "**Koliko se čuva:** unos se zapisuje u datoteku "
            "`_data/kalendar.json` na poslužitelju i ostaje dok ga sami ne "
            "uklonite gumbom \"Ukloni\". Automatskog brisanja nema i rok čuvanja "
            "nije utvrđen."
        ),
        "upozorenje": (
            "**Upozorenje:** unosi nisu odvojeni po korisniku. Svi koji koriste "
            "istu instancu aplikacije vide iste događaje. Ne upisujte podatke o "
            "strankama ni tuđu e-mail adresu."
        ),
    },
    "racun": {
        "naslov": "Što se događa s podacima koje upišete pri registraciji",
        "prikuplja": (
            "**Što se prikuplja:** ime i prezime, e-mail adresa, lozinka i datum "
            "registracije. Lozinka se pohranjuje isključivo kao PBKDF2-SHA256 "
            "sažetak sa slučajnom soli, nikad u čitljivom obliku."
        ),
        "svrha": (
            "**Svrha:** otvaranje i korištenje korisničkog računa. Registracija "
            "nije uvjet korištenja: gostujući pristup radi bez ijednog od ovih "
            "podataka."
        ),
        "osnova": (
            "**Osnova:** izvršenje ugovora o korištenju računa "
            "(čl. 6. st. 1. t. (b) Opće uredbe)."
        ),
        "cuvanje": (
            "**Koliko se čuva:** podaci se zapisuju u datoteku `.users.json` na "
            "poslužitelju i ostaju dok račun postoji. Automatskog brisanja nema, "
            "rok čuvanja nije utvrđen, a brisanje računa nije ugrađeno u "
            "sučelje: izvodi se ručno, na zahtjev poslan voditelju obrade."
        ),
        "upozorenje": (
            "**Prijava Google računom:** e-mail i ime s Google profila ostaju "
            "samo u tekućoj sesiji i ne upisuju se ni u datoteku ni u bazu."
        ),
    },
    "pretraga": {
        "naslov": "Što se događa s pojmom koji upišete u pretragu",
        "prikuplja": "**Što se prikuplja:** tekst upita koji upišete.",
        "svrha": "**Svrha:** pretraživanje službenog izdanja Narodnih novina.",
        "osnova": (
            "**Osnova:** obrada je nužna za uslugu koju ste sami zatražili "
            "(čl. 6. st. 1. t. (b) Opće uredbe)."
        ),
        "cuvanje": (
            "**Koliko se čuva:** upit se šalje poslužitelju Narodnih novina "
            "(narodne-novine.nn.hr) i drži se u međuspremniku aplikacije jedan "
            "sat radi ponovljene pretrage. U datoteku ni u bazu se ne zapisuje. "
            "Što Narodne novine rade sa zahtjevom, nije pod nadzorom ove "
            "aplikacije."
        ),
        "upozorenje": (
            "**Upozorenje:** ne upisujte osobne podatke u upit. Pretraga služi "
            "za pojmove iz propisa."
        ),
    },
}


def tekst_obavijesti(kontekst="dokument"):
    """Vrati tekst obavijesti za zadani kontekst, kao markdown.

    Odvojeno od prikaza da bi se sadrzaj mogao provjeriti testom bez pokretanja
    Streamlita.
    """
    if kontekst not in KONTEKSTI:
        raise KeyError(
            "Nepoznat kontekst obavijesti: %r. Dopusteni: %s"
            % (kontekst, ", ".join(sorted(KONTEKSTI)))
        )
    k = KONTEKSTI[kontekst]
    redci = [
        _TKO,
        k["prikuplja"],
        k["svrha"],
        k["osnova"],
        k["cuvanje"],
        _PRAVA,
    ]
    if k["upozorenje"]:
        redci.insert(5, k["upozorenje"])
    return "\n\n".join(redci)


def prikazi_obavijest_o_obradi(kontekst="dokument", kljuc=None, navigacija=True):
    """Prikazi obavijest iz cl. 13. na mjestu na kojem se podaci prikupljaju.

    Sklopiva je i zatvorena po zadanom, pa ne zaklanja posao. Naslov je vidljiv
    i bez otvaranja, tako da korisnik i zatvorenu obavijest vidi.

    kontekst   - kljuc iz KONTEKSTI; odreduje sto se navodi kao prikupljeno,
                 gdje zavrsava i koliko se cuva.
    kljuc      - prefiks kljuca widgeta; potreban samo ako se na istoj stranici
                 obavijest prikazuje vise puta.
    navigacija - kad je True, nudi gumb koji vodi na punu politiku. Na prijavnoj
                 stranici mora biti False: dok korisnik nije prijavljen,
                 usmjeravanje po modulima se ne izvodi, pa bi gumb bio mrtav.
    """
    tekst = tekst_obavijesti(kontekst)
    naslov = KONTEKSTI[kontekst]["naslov"]
    kljuc = kljuc or ("_gdpr13_%s" % kontekst)

    with st.expander(naslov, expanded=False):
        st.markdown(tekst)
        if navigacija:
            if st.button(
                "Otvori punu politiku privatnosti",
                key=kljuc + "_politika",
            ):
                st.session_state._active_module = MODUL_POLITIKA
                st.rerun()
        else:
            st.caption(
                "Puni tekst politike privatnosti nalazi se u aplikaciji, u "
                "izborniku \"%s\"." % MODUL_POLITIKA
            )
