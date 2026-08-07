# -----------------------------------------------------------------------------
# BIBLIOTEKA STANDARDNIH UGOVORNIH KLAUZULA
# Svaka klauzula je dict s 'naziv', 'kategorija', 'tekst'
# Tekst sadrzi placeholder {stranke} koji se zamjenjuje u generatoru
# -----------------------------------------------------------------------------

KATEGORIJE = [
    "Raskid ugovora",
    "Ugovorna kazna",
    "Viša sila (force majeure)",
    "Nadležnost suda",
    "Salvatorna klauzula",
    "Povjerljivost / GDPR",
    "Intelektualno vlasništvo",
    "Komunikacija između stranaka",
    "Primjena prava",
    "Završne odredbe",
]

KLAUZULE = [
    # --- RASKID UGOVORA ---
    {
        "naziv": "Raskid ugovora - opći",
        "kategorija": "Raskid ugovora",
        "tekst": (
            "Svaka ugovorna strana može raskinuti ovaj Ugovor pisanom izjavom drugoj strani, "
            "uz otkazni rok od 30 (trideset) dana. Raskid proizvodi pravne učinke istekom "
            "otkaznog roka od dana primitka pisane izjave o raskidu."
        ),
    },
    {
        "naziv": "Raskid zbog bitne povrede",
        "kategorija": "Raskid ugovora",
        "tekst": (
            "U slučaju bitne povrede ugovorne obveze od strane jedne ugovorne strane, "
            "druga strana ima pravo raskinuti ovaj Ugovor bez otkaznog roka, pisanom izjavom, "
            "pod uvjetom da je prethodno ostavila primjereni rok za ispunjenje koji ne može biti "
            "kraći od 15 (petnaest) dana (čl. 362. ZOO)."
        ),
    },
    {
        "naziv": "Raskid - automatski prestanak",
        "kategorija": "Raskid ugovora",
        "tekst": (
            "Ovaj Ugovor prestaje važiti istekom roka na koji je sklopljen, ispunjenjem svih "
            "ugovornih obveza obiju strana, sporazumnim raskidom u pisanom obliku, ili nastupom "
            "nemogućnosti ispunjenja koja nije uzrokovana krivnjom ni jedne strane."
        ),
    },

    # --- UGOVORNA KAZNA ---
    {
        "naziv": "Ugovorna kazna - fiksna",
        "kategorija": "Ugovorna kazna",
        "tekst": (
            "U slučaju neispunjenja ili neurednog ispunjenja ugovornih obveza, strana koja ne "
            "ispuni obvezu obvezuje se drugoj strani platiti ugovornu kaznu u iznosu od "
            "__________ EUR. Ugovorna kazna ne utječe na pravo na naknadu štete koja "
            "prelazi iznos ugovorne kazne (čl. 353. ZOO)."
        ),
    },
    {
        "naziv": "Ugovorna kazna - dnevna",
        "kategorija": "Ugovorna kazna",
        "tekst": (
            "Za svaki dan zakašnjenja u ispunjenju obveze, strana koja kasni obvezuje se "
            "platiti ugovornu kaznu u iznosu od __________ EUR dnevno, ali ukupno ne više "
            "od __________% vrijednosti ugovora. Plaćanje ugovorne kazne ne oslobađa "
            "dužnika obveze ispunjenja (čl. 354. ZOO)."
        ),
    },

    # --- VISA SILA ---
    {
        "naziv": "Viša sila - standardna",
        "kategorija": "Viša sila (force majeure)",
        "tekst": (
            "Nijedna ugovorna strana neće odgovarati za neispunjenje ili zakašnjenje u "
            "ispunjenju svojih obveza ako je to uzrokovano okolnostima više sile. Višom silom "
            "smatraju se izvanredne okolnosti nastale nakon sklapanja ugovora koje se nisu mogle "
            "predvidjeti niti spriječiti, uključujući, ali ne ograničavajući se na: prirodne "
            "katastrofe, rat, terorizam, epidemije/pandemije, vladine mjere, štrajkove i "
            "obustave rada. Strana pogođena višom silom dužna je o tome obavijestiti drugu "
            "stranu u roku od 7 (sedam) dana od nastupa takvih okolnosti (čl. 373. ZOO)."
        ),
    },

    # --- NADLEZNOST SUDA ---
    {
        "naziv": "Nadležnost - mjesna (sporazumna)",
        "kategorija": "Nadležnost suda",
        "tekst": (
            "Za sve sporove koji proizlaze iz ovog Ugovora ili u vezi s njim, ugovorne "
            "strane sporazumno ugovaraju mjesnu nadležnost suda u __________."
        ),
    },
    {
        "naziv": "Nadležnost - arbitraža (HGK)",
        "kategorija": "Nadležnost suda",
        "tekst": (
            "Sve sporove koji proizlaze iz ovog Ugovora ili u vezi s njim, uključujući "
            "sporove o njegovom valjanom nastanku, sadržaju ili prestanku, ugovorne strane "
            "će nastojati riješiti mirnim putem. Ako to ne uspije, sporove će konačno riješiti "
            "arbitraža pri Stalnom izbranom sudištu Hrvatske gospodarske komore u Zagrebu, "
            "prema važećem Pravilniku tog Sudišta."
        ),
    },

    # --- SALVATORNA KLAUZULA ---
    {
        "naziv": "Salvatorna klauzula - standardna",
        "kategorija": "Salvatorna klauzula",
        "tekst": (
            "Ako se bilo koja odredba ovog Ugovora pokaže ništetnom, nevažećom ili "
            "neprovedivom, to neće utjecati na valjanost i provedivost ostalih odredbi "
            "ovog Ugovora. Ugovorne strane se obvezuju ništetnu ili nevažeću odredbu "
            "zamijeniti valjanom odredbom koja najviše odgovara gospodarskom smislu i "
            "svrsi zamijenjene odredbe."
        ),
    },

    # --- POVJERLJIVOST / GDPR ---
    {
        "naziv": "Povjerljivost - opća",
        "kategorija": "Povjerljivost / GDPR",
        "tekst": (
            "Ugovorne strane se obvezuju čuvati povjerljivost svih podataka, informacija "
            "i dokumenata do kojih dođu u vezi s izvršenjem ovog Ugovora. Obveza čuvanja "
            "povjerljivosti traje i nakon prestanka ovog Ugovora, bez vremenskog ograničenja, "
            "osim za podatke koji postanu javno dostupni bez krivnje ugovorne strane."
        ),
    },
    {
        "naziv": "GDPR klauzula - obrada osobnih podataka",
        "kategorija": "Povjerljivost / GDPR",
        "tekst": (
            "Ugovorne strane se obvezuju obrađivati osobne podatke isključivo u svrhu "
            "izvršenja ovog Ugovora, u skladu s Općom uredbom o zaštiti podataka (GDPR) "
            "i Zakonom o provedbi Opće uredbe o zaštiti podataka (NN 42/18). Svaka strana "
            "je voditelj obrade za osobne podatke koje prikuplja u svrhu izvršenja svojih "
            "ugovornih obveza."
        ),
    },

    # --- INTELEKTUALNO VLASNISTVO ---
    {
        "naziv": "IP - zadržavanje prava",
        "kategorija": "Intelektualno vlasništvo",
        "tekst": (
            "Sva prava intelektualnog vlasništva koja su postojala prije sklapanja ovog "
            "Ugovora ostaju vlasništvo strane kojoj su izvorno pripadala. Ovaj Ugovor ne "
            "prenosi nikakva prava intelektualnog vlasništva s jedne strane na drugu, osim "
            "ako nije izričito drugačije ugovoreno."
        ),
    },
    {
        "naziv": "IP - prijenos autorskih prava",
        "kategorija": "Intelektualno vlasništvo",
        "tekst": (
            "Autor/Izvršitelj prenosi na Naručitelja sva imovinska autorska prava na "
            "djelima nastalim u izvršenju ovog Ugovora, bez vremenskog i prostornog "
            "ograničenja, uključujući pravo reproduciranja, distribucije, priopćavanja "
            "javnosti, prerade i stavljanja na raspolaganje javnosti (čl. 44. ZAPSP)."
        ),
    },

    # --- KOMUNIKACIJA ---
    {
        "naziv": "Komunikacija - adrese za dostavu",
        "kategorija": "Komunikacija između stranaka",
        "tekst": (
            "Sve obavijesti, zahtjevi i drugi akti u vezi s ovim Ugovorom dostavljaju se "
            "pisanim putem na adrese navedene u zaglavlju ovog Ugovora, ili na adrese "
            "elektroničke pošte koje strane naknadno pisano priopće. Dostava se smatra "
            "izvršenom danom primitka, a u slučaju preporučene pošte - trećeg radnog dana "
            "od dana predaje pošiljke pošti."
        ),
    },

    # --- PRIMJENA PRAVA ---
    {
        "naziv": "Primjena hrvatskog prava",
        "kategorija": "Primjena prava",
        "tekst": (
            "Na ovaj Ugovor primjenjuje se pravo Republike Hrvatske. Za sva pitanja koja "
            "nisu uređena ovim Ugovorom primjenjuju se odredbe Zakona o obveznim odnosima "
            "i drugih relevantnih propisa Republike Hrvatske."
        ),
    },

    # --- ZAVRSNE ODREDBE ---
    {
        "naziv": "Završne odredbe - standardne",
        "kategorija": "Završne odredbe",
        "tekst": (
            "Ovaj Ugovor stupa na snagu danom potpisa obiju ugovornih strana. Izmjene i "
            "dopune ovog Ugovora valjane su samo u pisanom obliku i uz potpis obiju strana. "
            "Ovaj Ugovor je sastavljen u __________ (________) istovjetnih primjeraka, od "
            "kojih svaka strana zadržava po __________ primjerak/primjerka."
        ),
    },
    {
        "naziv": "Završne odredbe - s javnobilježničkom ovjerom",
        "kategorija": "Završne odredbe",
        "tekst": (
            "Ovaj Ugovor stupa na snagu danom javnobilježničke ovjere potpisa obiju strana. "
            "Izmjene i dopune ovog Ugovora valjane su samo u pisanom obliku uz potpis obiju "
            "strana i javnobilježničku ovjeru. Troškove ovjere snosi __________ strana."
        ),
    },
]


def dohvati_klauzule(kategorija=None):
    """Vraca listu klauzula, opcionalno filtriranu po kategoriji."""
    if kategorija:
        return [k for k in KLAUZULE if k["kategorija"] == kategorija]
    return KLAUZULE


def dohvati_klauzulu_po_nazivu(naziv):
    """Vraca tekst klauzule po nazivu."""
    for k in KLAUZULE:
        if k["naziv"] == naziv:
            return k["tekst"]
    return ""
