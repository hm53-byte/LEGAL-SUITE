# -----------------------------------------------------------------------------
# GENERATORI: Trgovacko pravo
# Drustveni ugovor, Odluka skupstine, Prijenos udjela, NDA, Zapisnik uprave
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur, format_eur_s_rijecima, _rimski_broj


# ---------------------------------------------------------------------------
# Clause Builder — popis odjeljaka za Ugovor o prodaji poduzeća
# ---------------------------------------------------------------------------
SEKCIJE_PRODAJA_PODUZECA = [
    {"id": "predmet", "naziv": "Predmet ugovora", "obavezno": True, "ukljuceno": True},
    {"id": "cijena", "naziv": "Kupoprodajna cijena i plaćanje", "obavezno": True, "ukljuceno": True},
    {"id": "nekretnine", "naziv": "Imovina — Nekretnine", "obavezno": False, "ukljuceno": False},
    {"id": "trabine", "naziv": "Imovina — Tražbine (cesija)", "obavezno": False, "ukljuceno": False},
    {"id": "mjenice", "naziv": "Imovina — Mjenice", "obavezno": False, "ukljuceno": False},
    {"id": "poslovni_udjeli", "naziv": "Imovina — Poslovni udjeli", "obavezno": False, "ukljuceno": False},
    {"id": "pokretnine", "naziv": "Imovina — Pokretnine", "obavezno": False, "ukljuceno": False},
    {"id": "vrijednosni_papiri", "naziv": "Imovina — Vrijednosni papiri", "obavezno": False, "ukljuceno": False},
    {"id": "novcana_sredstva", "naziv": "Imovina — Novčana sredstva", "obavezno": False, "ukljuceno": False},
    {"id": "preuzete_obveze", "naziv": "Preuzete obveze", "obavezno": False, "ukljuceno": False},
    {"id": "radni_odnosi", "naziv": "Prijenos ugovora o radu", "obavezno": False, "ukljuceno": False},
    {"id": "tekuci_ugovori", "naziv": "Prijenos tekućih ugovora", "obavezno": False, "ukljuceno": False},
    {"id": "zabrana_natjecanja", "naziv": "Zabrana natjecanja (Non-Compete)", "obavezno": False, "ukljuceno": False},
    {"id": "prezivjela_jamstva", "naziv": "Preživjela jamstva", "obavezno": False, "ukljuceno": False},
    {"id": "izjave_jamstva", "naziv": "Izjave i jamstva", "obavezno": True, "ukljuceno": True},
    {"id": "porezne_odredbe", "naziv": "Porezne odredbe", "obavezno": False, "ukljuceno": True},
    {"id": "primopredaja", "naziv": "Primopredaja poduzeća", "obavezno": True, "ukljuceno": True},
    {"id": "nedostaci", "naziv": "Odgovornost za nedostatke", "obavezno": False, "ukljuceno": True},
    {"id": "ugovorna_kazna", "naziv": "Ugovorna kazna", "obavezno": False, "ukljuceno": True},
    {"id": "povjerljivost", "naziv": "Povjerljivost", "obavezno": False, "ukljuceno": True},
    {"id": "sporovi", "naziv": "Rješavanje sporova", "obavezno": True, "ukljuceno": True},
    {
        "id": "zavrsne",
        "naziv": "Završne odredbe",
        "obavezno": True,
        "ukljuceno": True,
        "fiksna_pozicija": "zadnja",
    },
]


def generiraj_drustveni_ugovor(osnivaci, podaci):
    """
    Društveni ugovor d.o.o. - ZTD čl. 387+
    ZAHTIJEVANA FORMA: JAVNOBILJEŽNIČKI AKT ili SOLEMNIZACIJA
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        tvrtka = podaci.get("tvrtka", "")
        skracena = podaci.get("skracena_tvrtka", "")
        sjediste = podaci.get("sjediste", "")
        temeljni_kapital = podaci.get("temeljni_kapital", 2500)
        djelatnosti = podaci.get("djelatnosti", "")
        trajanje = podaci.get("trajanje", "neodređeno")
        zastupanje = podaci.get("zastupanje", "samostalno i pojedinačno")

        parts = [
            "<div style='text-align: center; font-size: 10pt; font-weight: bold; "
            "border: 1px solid black; padding: 8px; margin-bottom: 20px;'>"
            "ZAHTIJEVANA FORMA: JAVNOBILJEŽNIČKI AKT ILI SOLEMNIZACIJA</div>",
            "<div class='header-doc'>DRUŠTVENI UGOVOR<br>"
            "<span style='font-size: 12pt; font-weight: normal;'>"
            "o osnivanju društva s ograničenom odgovornošću</span></div>",
            f"<div class='justified'>Sklopljen u {mjesto}, dana {danas} godine, između osnivača:</div><br>",
        ]

        for i, osn in enumerate(osnivaci, 1):
            udio = osn.get("udio", 0)
            parts.append(
                f"<div class='party-info'><b>{i}. OSNIVAČ:</b><br>{osn['tekst']}<br>"
                f"Poslovni udio: <b>{format_eur(udio)}</b></div>"
            )

        clanak = 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}.</div>"
            f"<div class='section-title' style='text-align: center;'>(Tvrtka i sjedište)</div>"
            f"<div class='justified'>Tvrtka društva glasi: <b>{format_text(tvrtka)}</b><br>"
            f"Skraćena tvrtka: <b>{format_text(skracena)}</b><br>"
            f"Sjedište društva je u: <b>{format_text(sjediste)}</b>.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}.</div>"
            f"<div class='section-title' style='text-align: center;'>(Predmet poslovanja)</div>"
            f"<div class='justified'>Društvo će obavljati sljedeće djelatnosti sukladno "
            f"Nacionalnoj klasifikaciji djelatnosti (NKD):<br><br>"
            f"{format_text(djelatnosti)}</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}.</div>"
            f"<div class='section-title' style='text-align: center;'>(Temeljni kapital i poslovni udjeli)</div>"
            f"<div class='justified'>Temeljni kapital društva iznosi <b>{format_eur_s_rijecima(temeljni_kapital)}</b>.</div><br>"
            f"<div class='justified'>Temeljni kapital podijeljen je na poslovne udjele kako slijedi:</div><br>"
        )
        for i, osn in enumerate(osnivaci, 1):
            udio = osn.get("udio", 0)
            parts.append(
                f"<div class='justified'>{i}. {osn.get('naziv', 'Osnivač ' + str(i))} "
                f"— udio u nominalnom iznosu od <b>{format_eur(udio)}</b></div>"
            )
        parts.append(
            "<br><div class='justified'>Osnivači se obvezuju uplatiti svoje udjele u cijelosti "
            "prije podnošenja prijave za upis u sudski registar.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}.</div>"
            f"<div class='section-title' style='text-align: center;'>(Uprava i zastupanje)</div>"
            f"<div class='justified'>Društvo ima jednog ili više direktora koje imenuje skupština društva. "
            f"Mandat članova uprave traje 4 (četiri) godine, s mogućnošću ponovnog imenovanja.<br><br>"
            f"Članovi uprave zastupaju društvo <b>{format_text(zastupanje)}</b>.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}.</div>"
            f"<div class='section-title' style='text-align: center;'>(Skupština)</div>"
            f"<div class='justified'>Skupštinu čine svi članovi društva. Skupština odlučuje "
            f"o svim pitanjima sukladno Zakonu o trgovačkim društvima i ovom Društvenom ugovoru.<br><br>"
            f"Skupština donosi odluke većinom glasova svih članova, osim u slučajevima "
            f"kada zakon propisuje kvalificiranu većinu.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}.</div>"
            f"<div class='section-title' style='text-align: center;'>(Raspodjela dobiti)</div>"
            f"<div class='justified'>Dobit društva raspodjeljuje se razmjerno poslovnim udjelima osnivača, "
            f"osim ako skupština ne odluči drugačije.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}.</div>"
            f"<div class='section-title' style='text-align: center;'>(Trajanje društva)</div>"
            f"<div class='justified'>Društvo se osniva na <b>{format_text(trajanje)}</b> vrijeme.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}.</div>"
            f"<div class='section-title' style='text-align: center;'>(Troškovi osnivanja)</div>"
            f"<div class='justified'>Troškove osnivanja društva (javnobilježnički troškovi, "
            f"sudske pristojbe, troškovi objave) snosi društvo do iznosa od 2.000,00 EUR.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}.</div>"
            f"<div class='section-title' style='text-align: center;'>(Završne odredbe)</div>"
            f"<div class='justified'>Na sva pitanja koja nisu uređena ovim Društvenim ugovorom "
            f"primjenjuju se odredbe Zakona o trgovačkim društvima (NN 111/93, 34/99, 121/99, "
            f"52/00, 118/03, 107/07, 146/08, 137/09, 125/11, 152/11, 111/12, 68/13, 110/15, "
            f"40/19, 34/22, 114/22, 18/23, 130/23).<br><br>"
            f"Ovaj Društveni ugovor sastavljen je u potrebnom broju primjeraka.</div><br>"
        )

        # Potpisi osnivača
        parts.append("<br>")
        for i, osn in enumerate(osnivaci, 1):
            parts.append(
                f'<div style="text-align: center; margin: 20px 0;">'
                f'<b>{i}. OSNIVAČ</b><br><br><br>______________________<br>'
                f'<small>(vlastoručni potpis pred javnim bilježnikom)</small></div>'
            )

        # JB ovjera
        parts.append(
            "<br><div style='border: 2px solid black; padding: 15px; margin-top: 30px;'>"
            "<div class='section-title' style='text-align: center;'>"
            "PROSTOR ZA JAVNOBILJEŽNIČKU OVJERU / SOLEMNIZACIJU</div>"
            "<div class='justified' style='font-size: 10pt;'>"
            "Ovaj Društveni ugovor solemniziran je / sastavljen kao javnobilježnički akt "
            "od strane javnog bilježnika _________________________, "
            "pod brojem OV-_____/______, dana ____________.<br><br>"
            "Javni bilježnik: ______________________<br>"
            "Pečat i potpis</div></div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_odluku_skupstine(drustvo, podaci):
    """
    Odluka skupštine / jednog člana društva - ZTD čl. 441+
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        vrsta = podaci.get("vrsta", "Imenovanje direktora")
        donositelj = podaci.get("donositelj", "skupština")
        izreka = podaci.get("izreka", "")
        obrazlozenje = podaci.get("obrazlozenje", "")
        pravni_temelj_clanak = podaci.get("pravni_temelj_clanak", "441.")

        drustvo_info = (
            f"<b>{drustvo.get('tvrtka', '')}</b><br>"
            f"Sjedište: {drustvo.get('sjediste', '')}<br>"
            f"OIB: {drustvo.get('oib', '')}, MBS: {drustvo.get('mbs', '')}"
        )

        donositelj_tekst = (
            "jedini član društva" if donositelj == "jedini_clan"
            else "skupština društva"
        )

        return (
            f"<div class='party-info' style='font-size: 10pt;'>{drustvo_info}</div>"
            f"<div style='text-align: right; font-size: 10pt;'>"
            f"{mjesto}, {danas}</div><br>"
            f"<div class='justified'>Na temelju članka {pravni_temelj_clanak} Zakona o trgovačkim društvima "
            f"te odgovarajućeg članka Društvenog ugovora, {donositelj_tekst} donosi sljedeću</div><br>"
            f"<div class='header-doc'>ODLUKU<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>"
            f"{format_text(vrsta)}</span></div>"
            f"<div class='section-title' style='text-align: center;'>IZREKA</div>"
            f"<div class='justified'>{format_text(izreka)}</div><br>"
            + (
                f"<div class='section-title'>OBRAZLOŽENJE</div>"
                f"<div class='justified'>{format_text(obrazlozenje)}</div><br>"
                if obrazlozenje else ""
            )
            + f"<div class='justified'>Ova Odluka stupa na snagu danom donošenja.</div>"
            f"<br><br>"
            f'<table width="100%" border="0"><tr>'
            f'<td width="50%" align="left"></td>'
            f'<td width="50%" align="center">'
            f"<b>{'JEDINI ČLAN DRUŠTVA' if donositelj == 'jedini_clan' else 'PREDSJEDNIK SKUPŠTINE'}</b>"
            f"<br><br><br>______________________<br>"
            f"<small>(potpis i pečat društva)</small></td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_prijenos_udjela(prenositelj, stjecatelj, drustvo, podaci):
    """
    Ugovor o prijenosu poslovnog udjela - ZTD čl. 412
    ZAHTIJEVANA FORMA: JAVNOBILJEŽNIČKA OVJERA POTPISA (ad solemnitatem)
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        nominalni_iznos = podaci.get("nominalni_iznos", 0)
        cijena = podaci.get("cijena", 0)
        nacin_placanja = podaci.get("nacin_placanja", "")

        drustvo_info = (
            f"{drustvo.get('tvrtka', '')}, OIB: {drustvo.get('oib', '')}, "
            f"MBS: {drustvo.get('mbs', '')}, sjedište: {drustvo.get('sjediste', '')}"
        )

        clanak = 1
        parts = [
            "<div style='text-align: center; font-size: 10pt; font-weight: bold; "
            "border: 1px solid black; padding: 8px; margin-bottom: 20px;'>"
            "ZAHTIJEVANA FORMA: JAVNOBILJEŽNIČKA OVJERA POTPISA</div>",
            "<div class='header-doc'>UGOVOR O PRIJENOSU POSLOVNOG UDJELA</div>",
            f"<div class='justified'>Sklopljen u {mjesto}, dana {danas} godine, između:</div><br>",
            f"<div class='party-info'><b>1. PRENOSITELJ (prodavatelj udjela):</b><br>{prenositelj}</div>",
            f"<div class='party-info'><b>2. STJECATELJ (kupac udjela):</b><br>{stjecatelj}</div><br>",
        ]

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Predmet ugovora)</div>"
            f"<div class='justified'>Prenositelj je imatelj poslovnog udjela u nominalnom iznosu od "
            f"<b>{format_eur_s_rijecima(nominalni_iznos)}</b> u društvu:<br><br>"
            f"<b>{drustvo_info}</b><br><br>"
            f"Ovim ugovorom Prenositelj prenosi navedeni poslovni udio na Stjecatelja.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Naknada)</div>"
            f"<div class='justified'>Ugovorena cijena za prijenos poslovnog udjela iznosi "
            f"<b>{format_eur_s_rijecima(cijena)}</b>.<br><br>"
            f"{format_text(nacin_placanja) if nacin_placanja else 'Cijena se plaća u roku od 8 dana od potpisa ovog ugovora.'}"
            f"</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Izjave Prenositelja)</div>"
            f"<div class='justified'>Prenositelj pod materijalnom i kaznenom odgovornošću izjavljuje:<br><br>"
            f"a) da je poslovni udio u njegovom isključivom vlasništvu;<br>"
            f"b) da je poslovni udio slobodan od svih tereta, zaloga i prava trećih osoba;<br>"
            f"c) da je temeljni ulog na koji se odnosi poslovni udio u cijelosti uplaćen.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Clausula intabulandi)</div>"
            f"<div class='justified'>Prenositelj ovime bezuvjetno i neopozivo ovlašćuje i dopušta "
            f"Stjecatelju da se na temelju ovog ugovora upiše u Knjigu poslovnih udjela društva "
            f"kao novi član (imatelj udjela), bez daljnjeg pitanja i odobrenja Prenositelja.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Troškovi)</div>"
            f"<div class='justified'>Troškove javnobilježničke ovjere potpisa snosi Stjecatelj, "
            f"osim ako se strane ne dogovore drugačije.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Završne odredbe)</div>"
            f"<div class='justified'>Na temelju članka 412. Zakona o trgovačkim društvima, "
            f"ovaj ugovor proizvodi pravne učinke prema društvu tek od trenutka kada se "
            f"društvu službeno prijavi prijenos i preda ovjereni primjerak ovog ugovora.<br><br>"
            f"Ovaj Ugovor sastavljen je u potrebnom broju primjeraka.</div><br>"
        )

        parts.append(
            "<div class='signature-row'>"
            "<div class='signature-block'><b>PRENOSITELJ</b><br><br><br>______________________<br>"
            "<small>(ovjera potpisa kod JB)</small></div>"
            "<div class='signature-block'><b>STJECATELJ</b><br><br><br>______________________<br>"
            "<small>(ovjera potpisa kod JB)</small></div></div>"
        )

        # JB ovjera
        parts.append(
            "<br><div style='border: 2px solid black; padding: 15px; margin-top: 30px;'>"
            "<div class='section-title' style='text-align: center;'>"
            "JAVNOBILJEŽNIČKA OVJERA POTPISA</div>"
            "<div class='justified' style='font-size: 10pt;'>"
            "Potpisi ugovornih strana ovjereni su od strane javnog bilježnika "
            "_________________________, pod brojem OV-_____/______, dana ____________.<br><br>"
            "Javni bilježnik: ______________________<br>"
            "Pečat i potpis</div></div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_nda(strana_a, strana_b, podaci):
    """
    Ugovor o tajnosti (NDA) - ZOO, Zakon o zaštiti neobjavljenih informacija
    ZAHTIJEVANA FORMA: PISANA (javnobilježnička ovjera nije potrebna)
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        vrsta = podaci.get("vrsta", "uzajamni")
        trajanje_razmjene = podaci.get("trajanje_razmjene", "12 mjeseci")
        trajanje_obveze = podaci.get("trajanje_obveze", "3 godine")
        ugovorna_kazna = podaci.get("ugovorna_kazna", 0)
        opis_informacija = podaci.get("opis_informacija", "")

        clanak = 1
        parts = [
            "<div style='text-align: center; font-size: 10pt; "
            "border: 1px solid #999; padding: 8px; margin-bottom: 20px;'>"
            "ZAHTIJEVANA FORMA: PISANA</div>",
            "<div class='header-doc'>UGOVOR O POVJERLJIVOSTI<br>"
            "<span style='font-size: 11pt; font-weight: normal;'>"
            "(Non-Disclosure Agreement / NDA)</span></div>",
            f"<div class='justified'>Sklopljen u {mjesto}, dana {danas} godine, između:</div><br>",
            f"<div class='party-info'><b>1. STRANA A "
            f"({'Davatelj i Primatelj informacija' if vrsta == 'uzajamni' else 'Davatelj informacija'}):</b><br>"
            f"{strana_a}</div>",
            f"<div class='party-info'><b>2. STRANA B "
            f"({'Davatelj i Primatelj informacija' if vrsta == 'uzajamni' else 'Primatelj informacija'}):</b><br>"
            f"{strana_b}</div><br>",
        ]

        uzajamno = vrsta == "uzajamni"
        tekst_strana = "obje Ugovorne strane uzajamno" if uzajamno else "Primatelj"

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Definicije)</div>"
            f"<div class='justified'>Pod pojmom <b>\"Povjerljive informacije\"</b> u smislu ovog Ugovora "
            f"smatraju se sve informacije, podaci, dokumenti i materijali, u bilo kojem obliku "
            f"(pisanom, usmenom, elektroničkom), koji se odnose na:<br><br>"
            f"{format_text(opis_informacija) if opis_informacija else '(financijski podaci, poslovni planovi, know-how, popisi klijenata, izvorni kod, strategije, M&amp;A namjere)'}"
            f"<br><br>Povjerljivom informacijom smatra se i sama činjenica vođenja pregovora "
            f"između Ugovornih strana.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Obveze čuvanja)</div>"
            f"<div class='justified'>{tekst_strana.capitalize()} se obvezuje:<br><br>"
            f"a) čuvati sve Povjerljive informacije u strogoj tajnosti;<br>"
            f"b) koristiti Povjerljive informacije isključivo u svrhu za koju su dane;<br>"
            f"c) ne umnožavati dokumente koji sadrže Povjerljive informacije bez pisane suglasnosti;<br>"
            f"d) ograničiti pristup Povjerljivim informacijama isključivo na zaposlenike i savjetnike "
            f"kojima su te informacije nužno potrebne za obavljanje zadataka (načelo \"need-to-know\");<br>"
            f"e) ne provoditi reverzni inženjering (reverse engineering) na bilo kojem materijalu.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Iznimke)</div>"
            f"<div class='justified'>Obveza čuvanja tajnosti ne odnosi se na informacije koje:<br><br>"
            f"a) su u trenutku primitka već bile javno poznate ili su to naknadno postale bez krivnje Primatelja;<br>"
            f"b) je Primatelj neovisno razvio bez korištenja Povjerljivih informacija;<br>"
            f"c) su Primatelju zakonito dostupne od treće strane bez obveze povjerljivosti;<br>"
            f"d) Primatelj mora otkriti po sili zakona, nalogu suda ili regulatornog tijela, "
            f"uz prethodnu pisanu obavijest Davatelju.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Trajanje)</div>"
            f"<div class='justified'>Razdoblje razmjene Povjerljivih informacija traje "
            f"<b>{format_text(trajanje_razmjene)}</b> od dana potpisa ovog Ugovora.<br><br>"
            f"Obveza čuvanja tajnosti traje <b>{format_text(trajanje_obveze)}</b> "
            f"nakon isteka ili raskida ovog Ugovora.</div><br>"
        )
        clanak += 1

        if ugovorna_kazna and ugovorna_kazna > 0:
            parts.append(
                f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Ugovorna kazna)</div>"
                f"<div class='justified'>U slučaju povrede obveze čuvanja tajnosti, strana koja je povrijedila "
                f"ovu obvezu dužna je drugoj strani isplatiti ugovornu kaznu u iznosu od "
                f"<b>{format_eur(ugovorna_kazna)}</b> za svaku utvrđenu povredu, "
                f"neovisno o pravu na naknadu pretrpljene štete.</div><br>"
            )
            clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Završne odredbe)</div>"
            f"<div class='justified'>Ovaj Ugovor sastavljen je u 2 (dva) istovjetna primjerka, "
            f"po jedan za svaku Ugovornu stranu.<br><br>"
            f"Na ovaj Ugovor primjenjuje se pravo Republike Hrvatske. "
            f"Za sporove iz ovog Ugovora nadležan je stvarno nadležni sud u {mjesto}.</div><br>"
        )

        parts.append(
            "<div class='signature-row'>"
            "<div class='signature-block'><b>STRANA A</b><br><br><br>______________________</div>"
            "<div class='signature-block'><b>STRANA B</b><br><br><br>______________________</div></div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def _sec_predmet(podaci, clanak_ref):
    djelatnost = podaci.get("djelatnost", "")
    n = clanak_ref[0]; clanak_ref[0] += 1
    n2 = clanak_ref[0]; clanak_ref[0] += 1
    return (
        "<div class='section-title' style='text-align: center;'>PREDMET UGOVORA</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
        f"<div class='justified'>(1) Prodavatelj je vlasnik poduzeća koje se bavi "
        f"{(format_text(djelatnost) if djelatnost else '(opis djelatnosti)')} "
        f"(u daljnjem tekstu: <b>Poduzeće</b>).<br><br>"
        f"(2) Ovim Ugovorom Prodavatelj prodaje, a Kupac kupuje Poduzeće kao organiziranu "
        f"gospodarsku cjelinu, sa svim njegovim objektivnim, subjektivnim i ustrojbenim "
        f"elementima, uključujući svu imovinu, prava, obveze, ugovorne odnose i radnopravne "
        f"odnose koji su s tim Poduzećem povezani, a kako je to detaljno navedeno u "
        f"člancima ovog Ugovora.<br><br>"
        f"(3) Na ovaj Ugovor primjenjuju se odredbe Zakona o obveznim odnosima "
        f"(NN 35/05 i izmjene; dalje: ZOO), Zakona o trgovačkim društvima "
        f"(NN 111/93 i izmjene; dalje: ZTD), Zakona o radu "
        f"(NN 93/14 i izmjene; dalje: ZR) te drugih relevantnih propisa.</div><br>"
        f"<div class='section-title' style='text-align: center;'>Članak {n2}.</div>"
        f"<div class='justified'>(1) Prodavatelj izjavljuje i jamči da je pravni položaj "
        f"Poduzeća, uključujući njegovu imovinu i obveze, na dan sklapanja ovog Ugovora u "
        f"cijelosti onakav kakav je opisan u ovom Ugovoru, te da izvan ovog Ugovora ne "
        f"postoje nikakve dodatne obveze, tereti ili ograničenja koja bi teretila Poduzeće, "
        f"a koja nisu navedena u ovom Ugovoru.<br><br>"
        f"(2) Prodavatelj izjavljuje da je prije sklapanja ovog Ugovora proveden postupak "
        f"dubinskog snimanja (due diligence) Poduzeća, čiji je izvještaj prilog ovom Ugovoru "
        f"(Prilog 1.) te čini njegov sastavni dio.</div><br>"
    )


def _sec_cijena(podaci, clanak_ref):
    kupoprodajna_cijena = podaci.get("kupoprodajna_cijena", 0)
    prijeboj_iznos = podaci.get("prijeboj_iznos", 0)
    prijeboj_opis = podaci.get("prijeboj_opis", "")
    rok_placanja = podaci.get("rok_placanja", 30)
    preostali_iznos = kupoprodajna_cijena - prijeboj_iznos
    n1 = clanak_ref[0]; clanak_ref[0] += 1
    n2 = clanak_ref[0]; clanak_ref[0] += 1
    n3 = clanak_ref[0]; clanak_ref[0] += 1
    cijena_art = (
        "<div class='section-title' style='text-align: center;'>KUPOPRODAJNA CIJENA I NAČIN PLAĆANJA</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n1}.</div>"
        f"<div class='justified'>(1) Ugovorne strane su suglasne da ukupna kupoprodajna "
        f"cijena za Poduzeće iznosi <b>{format_eur_s_rijecima(kupoprodajna_cijena)}</b>.<br><br>"
        f"(2) Kupoprodajna cijena utvrđena je na temelju provedenog dubinskog snimanja, "
        f"financijskih izvješća Prodavatelja te sporazuma ugovornih strana.</div><br>"
    )
    if prijeboj_iznos > 0 and prijeboj_opis:
        placanje_art = (
            f"<div class='section-title' style='text-align: center;'>Članak {n2}.</div>"
            f"<div class='justified'>(1) Kupac se obvezuje platiti kupoprodajnu cijenu "
            f"na sljedeći način:<br><br>"
            f"a) Iznos od <b>{format_eur_s_rijecima(prijeboj_iznos)}</b> namiruje se prijebojem "
            f"(kompenzacijom) s dospjelom tražbinom sukladno čl. 195. ZOO-a: "
            f"{format_text(prijeboj_opis)}. Ugovorne strane su suglasne da se navedenim "
            f"prijebojem u cijelosti namiruje predmetna tražbina Kupca prema Prodavatelju.<br><br>"
            f"b) Preostali iznos od <b>{format_eur_s_rijecima(preostali_iznos)}</b> Kupac će uplatiti "
            f"na žiro-račun Prodavatelja u roku od {rok_placanja} ({rok_placanja}) dana "
            f"od dana sklapanja ovog Ugovora.<br><br>"
            f"(2) U slučaju zakašnjenja s plaćanjem, Kupac se obvezuje platiti zakonske "
            f"zatezne kamate sukladno čl. 29. ZOO-a.</div><br>"
        )
    else:
        placanje_art = (
            f"<div class='section-title' style='text-align: center;'>Članak {n2}.</div>"
            f"<div class='justified'>(1) Kupac se obvezuje kupoprodajnu cijenu u iznosu "
            f"od <b>{format_eur_s_rijecima(kupoprodajna_cijena)}</b> uplatiti na žiro-račun "
            f"Prodavatelja u roku od {rok_placanja} ({rok_placanja}) dana od dana "
            f"sklapanja ovog Ugovora.<br><br>"
            f"(2) U slučaju zakašnjenja s plaćanjem, Kupac se obvezuje platiti zakonske "
            f"zatezne kamate sukladno čl. 29. ZOO-a.</div><br>"
        )
    trueup_art = (
        f"<div class='section-title' style='text-align: center;'>Članak {n3}. "
        f"(Mehanizam usklađenja cijene / True-up)</div>"
        f"<div class='justified'>(1) Kupoprodajna cijena iz prethodnog članka utvrđena je "
        f"na temelju referentnog stanja Poduzeća na dan sklapanja ovog Ugovora "
        f"(<b>Referentni datum</b>). Stranke su suglasne da će se između Referentnog datuma "
        f"i dana primopredaje stanje zaliha i obrtnih sredstava promijeniti, te se ugovara "
        f"sljedeći mehanizam usklađenja:<br><br>"
        f"(2) Na dan primopredaje, ovlašteni predstavnici obiju ugovornih strana zajedno će "
        f"utvrditi stvarno stanje zaliha popisom (inventurom) te sačiniti Zapisnik o stanju "
        f"zaliha na dan primopredaje (dalje: <b>Zapisnik o zalihama</b>), koji čini sastavni "
        f"dio Zapisnika o primopredaji.<br><br>"
        f"(3) Ako ukupna tržišna vrijednost stvarnih zaliha premašuje ili ne dostiže "
        f"referentnu vrijednost za više od <b>5.000,00 EUR (slovima: pet tisuća eura)</b> "
        f"(dalje: Prag de minimis), razliku nadoplaćuje ili vraća odgovarajuća strana u "
        f"roku od 15 (petnaest) dana od potpisivanja Zapisnika o primopredaji. "
        f"Razlike ispod praga od 5.000,00 EUR (slovima: pet tisuća eura) ne podliježu "
        f"usklađenju.<br><br>"
        f"(4) Ako stranke ne postignu suglasnost o vrijednosti zaliha, imenuju neovisnog "
        f"ovlaštenog procjenitelja (metodom naizmjeničnog isključivanja s liste HGK) čiji "
        f"nalaz je konačan i obvezujući za obje stranke. Troškovi procjenitelja snose se "
        f"na jednake dijelove.</div><br>"
    )
    return cijena_art + placanje_art + trueup_art


def _sec_nekretnine(podaci, clanak_ref):
    nekretnina_opis = podaci.get("nekretnina_opis", "")
    ima_hipoteku = podaci.get("ima_hipoteku", False)
    hipoteka_iznos = podaci.get("hipoteka_iznos", 0)
    hipoteka_banka = podaci.get("hipoteka_banka", "")
    n = clanak_ref[0]; clanak_ref[0] += 1
    parts = [
        f"<div class='section-title' style='text-align: center;'>NEKRETNINE<br>"
        f"Članak {n}.</div>"
        f"<div class='justified'>(1) Prodavatelj prodaje i prenosi na Kupca sljedeću "
        f"nekretninu:<br><br>{format_text(nekretnina_opis)}<br><br>"
    ]
    if ima_hipoteku and hipoteka_banka and hipoteka_iznos > 0:
        parts.append(
            f"(2) Nekretnina iz stavka 1. ovog članka opterećena je hipotekom za "
            f"osiguranje tražbine u iznosu od <b>{format_eur_s_rijecima(hipoteka_iznos)}</b> "
            f"u korist {format_text(hipoteka_banka)}. Kupac izjavljuje da je upoznat "
            f"s postojanjem hipoteke te preuzima nekretninu s navedenim teretom.<br><br>"
            f"(3) Prodavatelj se obvezuje pribaviti suglasnost navedene banke za "
            f"prijenos nekretnine na Kupca. Kupac se obvezuje preuzeti obveze koje "
            f"proizlaze iz hipotekarnog odnosa ili s bankom sklopiti novi ugovor o "
            f"osiguranju tražbine.<br><br>"
        )
    parts.append(
        f"<b>CLAUSULA INTABULANDI:</b><br>"
        f"Prodavatelj daje izričitu, bezuvjetnu i neopozivo suglasnost da se u "
        f"zemljišnoj knjizi, na nekretnini opisanoj u stavku 1. ovog članka, "
        f"izvrši uknjižba prava vlasništva u korist Kupca, bez ikakvih daljnjih "
        f"uvjeta ili odobrenja Prodavatelja.</div><br>"
    )
    return "".join(parts)


def _sec_trabine(podaci, clanak_ref):
    trabina_opis = podaci.get("trabina_opis", "")
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>TRAŽBINE<br>"
        f"Članak {n}.</div>"
        f"<div class='justified'>(1) Prodavatelj ovim Ugovorom ustupa (cedira) Kupcu, "
        f"sukladno čl. 80.–89. ZOO-a, sljedeću tražbinu:<br><br>"
        f"{format_text(trabina_opis)}<br><br>"
        f"(2) Prodavatelj (cedent) izjavljuje da je navedena tražbina valjana, "
        f"postojeća i utuživa, te da ne postoje okolnosti koje bi sprječavale "
        f"njezinu naplatu.<br><br>"
        f"(3) Prodavatelj se obvezuje bez odgode obavijestiti dužnika o izvršenoj "
        f"cesiji sukladno čl. 82. ZOO-a te mu dostaviti primjerak obavijesti o "
        f"cesiji (denuntiatio cessionis).</div><br>"
    )


def _sec_mjenice(podaci, clanak_ref):
    mjenice_opis = podaci.get("mjenice_opis", "")
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>MJENICE<br>"
        f"Članak {n}.</div>"
        f"<div class='justified'>(1) Prodavatelj prenosi na Kupca sljedeće mjenice "
        f"putem indosamenta, sukladno odredbama Zakona o mjenici (NN 74/94, 92/10):"
        f"<br><br>{format_text(mjenice_opis)}<br><br>"
        f"(2) Prijenos mjenica izvršit će se stavljanjem indosamenta na poleđinu "
        f"svake mjenice u korist Kupca te fizičkom predajom mjenica Kupcu na dan "
        f"potpisa ovog Ugovora.<br><br>"
        f"(3) Prodavatelj jamči da su mjenice valjane, da na njima nema nikakvih "
        f"nedostataka te da su sve dosadašnje prijenosne radnje (indosamenti) "
        f"izvršene u skladu sa zakonom.</div><br>"
    )


def _sec_poslovni_udjeli(podaci, clanak_ref):
    poslovni_udjeli_opis = podaci.get("poslovni_udjeli_opis", "")
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>POSLOVNI UDJELI<br>"
        f"Članak {n}.</div>"
        f"<div class='justified'>(1) Prodavatelj prenosi na Kupca sljedeće poslovne "
        f"udjele:<br><br>{format_text(poslovni_udjeli_opis)}<br><br>"
        f"(2) Prijenos poslovnih udjela izvršit će se u obliku javnobilježničkog akta "
        f"ili privatne isprave koju potvrdi javni bilježnik, sukladno čl. 412. st. 3. "
        f"ZTD-a, koji je prilog ovom Ugovoru (Prilog 2.).<br><br>"
        f"(3) Prodavatelj se obvezuje bez odgode obavijestiti predmetna društva o "
        f"prijenosu te zatražiti upis Kupca kao novog imatelja poslovnih udjela, "
        f"sukladno čl. 411. ZTD-a.<br><br>"
        f"(4) Prodavatelj izjavljuje da poslovni udjeli nisu opterećeni zalogom ni "
        f"drugim pravima trećih osoba, da nisu predmet spora, te da ne postoje "
        f"ograničenja raspolaganja tim udjelima koja bi sprječavala njihov "
        f"prijenos.</div><br>"
    )


def _sec_pokretnine(podaci, clanak_ref):
    pokretnine_opis = podaci.get("pokretnine_opis", "")
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>POKRETNINE<br>"
        f"Članak {n}.</div>"
        f"<div class='justified'>(1) Prodavatelj predaje Kupcu u posjed i vlasništvo "
        f"sljedeće pokretnine:<br><br>{format_text(pokretnine_opis)}<br><br>"
        f"(2) Prijenos vlasništva pokretnina izvršit će se predajom u posjed Kupca "
        f"na dan potpisa ovog Ugovora, odnosno najkasnije u roku od 15 (petnaest) "
        f"dana od dana potpisa ovog Ugovora, čime Kupac stječe pravo vlasništva "
        f"sukladno čl. 116. Zakona o vlasništvu i drugim stvarnim pravima.<br><br>"
        f"(3) O primopredaji pokretnina sastavit će se primopredajni zapisnik koji "
        f"potpisuju obje ugovorne strane (Prilog 3.).</div><br>"
    )


def _sec_vrijednosni_papiri(podaci, clanak_ref):
    vrijednosni_papiri_opis = podaci.get("vrijednosni_papiri_opis", "")
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>VRIJEDNOSNI PAPIRI<br>"
        f"Članak {n}.</div>"
        f"<div class='justified'>(1) Prodavatelj prenosi na Kupca sljedeći portfelj "
        f"vrijednosnih papira:<br><br>{format_text(vrijednosni_papiri_opis)}<br><br>"
        f"(2) Prijenos se vrši sukladno prirodi vrijednosnih papira (fizičkom predajom "
        f"ili nalogom za prijenos kod SKDD-a).<br><br>"
        f"(3) Prodavatelj se obvezuje dati nalog za prijenos vrijednosnih papira na "
        f"račun Kupca kod SKDD-a, ako su papiri evidentirani u depozitoriju.</div><br>"
    )


def _sec_novcana_sredstva(podaci, clanak_ref):
    novcana_sredstva = podaci.get("novcana_sredstva", 0)
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>NOVČANA SREDSTVA<br>"
        f"Članak {n}.</div>"
        f"<div class='justified'>(1) Prodavatelj prenosi na Kupca novčana sredstva u "
        f"iznosu od <b>{format_eur_s_rijecima(novcana_sredstva)}</b> koja se na dan sklapanja "
        f"ovog Ugovora nalaze na žiro-računu Prodavatelja.<br><br>"
        f"(2) Prijenos novčanih sredstava izvršit će se nalogom za prijenos na "
        f"žiro-račun Kupca u roku od 5 (pet) radnih dana od dana potpisa ovog "
        f"Ugovora.</div><br>"
    )


def _sec_preuzete_obveze(podaci, clanak_ref):
    preuzete_obveze = podaci.get("preuzete_obveze", "")
    n = clanak_ref[0]; clanak_ref[0] += 1
    header = (
        "<div class='section-title' style='text-align: center;'>OBVEZE KOJE SE PRENOSE</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
    )
    if preuzete_obveze:
        body = (
            f"<div class='justified'>(1) Kupac preuzima sljedeće obveze Prodavatelja "
            f"vezane uz Poduzeće:<br><br>{format_text(preuzete_obveze)}<br><br>"
            f"(2) Preuzimanje dugova vrši se uz suglasnost vjerovnika sukladno čl. "
            f"96.–100. ZOO-a. Ukoliko vjerovnik uskrati suglasnost, Prodavatelj ostaje "
            f"solidarno odgovoran s Kupcem za namirenje obveze.<br><br>"
            f"(3) Prodavatelj izjavljuje i jamči da, osim obveza navedenih u ovom "
            f"članku, ne postoje nikakve druge obveze vezane uz Poduzeće.</div><br>"
        )
    else:
        body = (
            f"<div class='justified'>(1) Kupac ne preuzima posebne obveze Prodavatelja, "
            f"osim onih koje po sili zakona prelaze uz Poduzeće kao gospodarsku "
            f"cjelinu.<br><br>"
            f"(2) Prodavatelj izjavljuje i jamči da ne postoje skrivene obveze vezane "
            f"uz Poduzeće koje nisu navedene u ovom Ugovoru.</div><br>"
        )
    return header + body


def _sec_radni_odnosi(podaci, clanak_ref):
    broj_zaposlenika = podaci.get("broj_zaposlenika", 0)
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        "<div class='section-title' style='text-align: center;'>PRIJENOS UGOVORA O RADU</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
        f"<div class='justified'>(1) Sukladno čl. 137. Zakona o radu, prodajom "
        f"Poduzeća kao organizirane gospodarske cjeline svi ugovori o radu "
        f"<b>{broj_zaposlenika} ({broj_zaposlenika})</b> zaposlenika zaposlenih na "
        f"neodređeno vrijeme u Poduzeću Prodavatelja prenose se na Kupca po sili "
        f"zakona.<br><br>"
        f"(2) Na radne odnose prenesenih zaposlenika nastavlja se primjenjivati "
        f"mjerodavni kolektivni ugovor najmanje godinu dana od prijenosa, sukladno "
        f"čl. 137. st. 3. ZR-a.<br><br>"
        f"(3) Kupac preuzima sva prava i obveze iz prenesenih ugovora o radu u "
        f"neizmijenjenom obliku i opsegu od dana prijenosa Poduzeća.<br><br>"
        f"(4) Prodavatelj se obvezuje pravodobno obavijestiti zaposlenike i radničko "
        f"vijeće (ako je ustrojeno) o namjeravanom prijenosu, razlozima prijenosa te "
        f"planiranim mjerama, sukladno čl. 137. st. 5.–7. ZR-a.<br><br>"
        f"(5) Prodavatelj i Kupac solidarno odgovaraju za obveze iz radnog odnosa "
        f"nastale do dana prijenosa Poduzeća prema zaposlenicima. Za obveze nastale "
        f"do i uključujući dan primopredaje (neiskorišteni odmori, neisplaćeni bonusi "
        f"i stimulacije, prekovremeni rad) Prodavatelj se obvezuje naknadom štete "
        f"zaštititi Kupca od takvih zahtjeva, u roku od 15 (petnaest) "
        f"dana od podnošenja pisanog zahtjeva s dokazima.</div><br>"
    )


def _sec_tekuci_ugovori(podaci, clanak_ref):
    tekuci_ugovori = podaci.get("tekuci_ugovori", "")
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        "<div class='section-title' style='text-align: center;'>PRIJENOS TEKUĆIH UGOVORA</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
        f"<div class='justified'>(1) Kupac preuzima sljedeće tekuće ugovore "
        f"Prodavatelja vezane uz poslovanje Poduzeća:<br><br>"
        f"{format_text(tekuci_ugovori)}<br><br>"
        f"(2) Prijenos ugovora vrši se sukladno čl. 127.–131. ZOO-a (ustupanje "
        f"ugovora). Prodavatelj se obvezuje pribaviti suglasnost ugovornih strana "
        f"za prijenos ugovora na Kupca.<br><br>"
        f"(3) U slučaju da neka od navedenih ugovornih strana uskrati suglasnost, "
        f"Prodavatelj se obvezuje surađivati s Kupcem radi sklapanja novih ugovora "
        f"s istim ili sličnim uvjetima.</div><br>"
    )


def _sec_zabrana_natjecanja(podaci, clanak_ref):
    zabrana_trajanje = podaci.get("zabrana_trajanje", "3 (tri) godine")
    zabrana_kazna = podaci.get("zabrana_kazna", 50000)
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        "<div class='section-title' style='text-align: center;'>ZABRANA NATJECANJA (NON-COMPETE)</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
        f"<div class='justified'>(1) Prodavatelj se obvezuje da u razdoblju od "
        f"<b>{format_text(zabrana_trajanje)}</b> od dana primopredaje Poduzeća neće, "
        f"ni izravno ni neizravno:<br><br>"
        f"a) osnivati, stjecati, voditi, financirati ili na drugi način sudjelovati u "
        f"subjektu koji se bavi istim ili srodnim poslovanjem na teritoriju Republike "
        f"Hrvatske;<br>"
        f"b) preuzimati ili pokušavati preuzimati zaposlenike, dobavljače ili kupce "
        f"Poduzeća koji su na dan primopredaje bili u ugovornom odnosu s Poduzećem;<br>"
        f"c) koristiti poslovne tajne, know-how, baze podataka ili bilo koje "
        f"povjerljive informacije stečene u okviru vođenja Poduzeća.<br><br>"
        f"(2) Zabrana iz stavka 1. ovog članka ne odnosi se na pasivno vlasništvo "
        f"do 5% javno uvrštenih dionica konkurentskog društva.<br><br>"
        f"(3) Za svako utvrđeno kršenje zabrane, Prodavatelj je dužan Kupcu platiti "
        f"ugovornu kaznu u iznosu od <b>{format_eur_s_rijecima(zabrana_kazna)}</b> za svaki "
        f"pojedini slučaj kršenja, neovisno o naknadi stvarne štete. Kupac zadržava "
        f"pravo zahtijevati i sudsku zabranu nastavka štetne radnje.<br><br>"
        f"(4) Prodavatelj izjavljuje da prihvaća ovu obvezu dobrovoljno te da je "
        f"smatraju razmjernom i pravno valjanom (ZOO čl. 9).</div><br>"
    )


def _sec_prezivjela_jamstva(podaci, clanak_ref):
    n1 = clanak_ref[0]; clanak_ref[0] += 1
    n2 = clanak_ref[0]; clanak_ref[0] += 1
    n3 = clanak_ref[0]; clanak_ref[0] += 1
    return (
        "<div class='section-title' style='text-align: center;'>"
        "ZAŠTITA PRODAVATELJA OD PREŽIVJELIH JAMSTAVA I GARANCIJA</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n1}. "
        f"(Katalog preživjelih jamstava)</div>"
        f"<div class='justified'>(1) Prodavatelj se obvezuje, najkasnije do dana "
        f"primopredaje Poduzeća, izraditi i predati Kupcu potpun i točan popis "
        f"(katalog) svih jamstava, garancija, jemstava, osiguranja i sličnih obveza "
        f"koje je Prodavatelj dao trećim osobama u vezi s poslovanjem Poduzeća, a "
        f"koje na dan primopredaje nisu ugašene (<b>Preživjela jamstva</b>).<br><br>"
        f"(2) Katalog preživjelih jamstava čini prilog ovom Ugovoru i sadrži za "
        f"svako preživjelo jamstvo: naziv i sjedište vjerovnika, pravni temelj, "
        f"vrstu jamstva, iznos, rok trajanja, uvjete aktivacije i podatak o "
        f"prenosivosti.<br><br>"
        f"(3) Prodavatelj izjavljuje i jamči da katalog obuhvaća sva jamstva i "
        f"garancije dane trećim osobama u vezi s Poduzećem.</div><br>"
        f"<div class='section-title' style='text-align: center;'>Članak {n2}. "
        f"(Obveza supstitucije jamstava)</div>"
        f"<div class='justified'>(1) Kupac se obvezuje uložiti sve razumno očekivane "
        f"napore da, u roku od 90 (devedeset) dana od dana primopredaje, za svako "
        f"preživjelo jamstvo iz kataloga ishodi: zamjenu jamstva Prodavatelja vlastitim "
        f"jamstvom Kupca prema istom vjerovniku, oslobođenje Prodavatelja od obveze "
        f"po jamstvu uz suglasnost vjerovnika, ili prestanak jamstva na drugi zakonit "
        f"način.<br><br>"
        f"(2) Za svako preživjelo jamstvo koje nije supstituirano u roku iz stavka 1., "
        f"Kupac je dužan Prodavatelju plaćati naknadu za preostalu izloženost u iznosu "
        f"od <b>0,015% dnevno</b> od nominalne vrijednosti svakog pojedinog preživjelog "
        f"jamstva, počevši od prvog dana nakon isteka roka iz stavka 1. Ukupna "
        f"kumulativna naknada ograničena je na 15% ukupne nominalne vrijednosti svih "
        f"preživjelih jamstava.<br><br>"
        f"(3) Ukoliko se bilo koje preživjelo jamstvo aktivira prije supstitucije, "
        f"Kupac je dužan Prodavatelju naknaditi cjelokupni iznos koji je Prodavatelj "
        f"platio po aktiviranom jamstvu, uvećan za sve troškove i zatezne kamate, "
        f"u roku od 15 (petnaest) dana od pisanog poziva.</div><br>"
        f"<div class='section-title' style='text-align: center;'>Članak {n3}. "
        f"(Jamstveni fiducijarni depozit)</div>"
        f"<div class='justified'>(1) Na dan primopredaje Poduzeća, Kupac se obvezuje "
        f"položiti na poseban fiducijarni (namjenski) račun iznos koji odgovara "
        f"<b>25% (dvadesetpet posto)</b> ukupne nominalne vrijednosti svih preživjelih "
        f"jamstava iz kataloga (<b>Jamstveni fiducijarni depozit</b>).<br><br>"
        f"(2) Fiducijar je javni bilježnik ili odvjetnik s podračunom klijentskih "
        f"sredstava, kojeg sporazumno imenuju ugovorne strane temeljem zasebnog "
        f"Ugovora o fiduciji koji čini prilog ovom Ugovoru.<br><br>"
        f"(3) Sredstva s fiducijarnog računa otpuštaju se: u korist Kupca — "
        f"proporcionalno za svako supstituirano ili ugašeno jamstvo; u korist "
        f"Prodavatelja — sukladno postupku negativne suglasnosti iz stavka 4. ovog "
        f"članka, ako se preživjelo jamstvo aktivira.<br><br>"
        f"(4) Prodavatelj koji je platio po aktiviranom jamstvu upućuje Kupcu pisanu "
        f"obavijest s dokazima. Kupac ima <b>15 (petnaest) radnih dana</b> da dostavi "
        f"Fiducijaru pisani prigovor. Ako Kupac u tom roku ne dostavi prigovor "
        f"(ugovorno uređena negativna suglasnost, sukladno načelu slobode uređivanja "
        f"obveznih odnosa, čl. 2. i čl. 17. ZOO-a, te odredbama Ugovora o fiduciji "
        f"koji čini prilog ovom Ugovoru), Fiducijar otpušta "
        f"sredstva Prodavatelju u roku od 5 (pet) radnih dana od isteka roka za prigovor. "
        f"Ako Kupac pravodobno dostavi prigovor, spor se rješava u ubrzanom "
        f"arbitražnom postupku pri Stalnom izbranom sudištu HGK.<br><br>"
        f"(5) Fiducijarni račun ostaje aktivan do dana kad su sva preživjela jamstva "
        f"supstituirana, ugašena ili na drugi način prestala, odnosno najdulje "
        f"36 (tridesetšest) mjeseci od dana primopredaje.</div><br>"
    )


def _sec_izjave_jamstva(podaci, clanak_ref):
    kupoprodajna_cijena = podaci.get("kupoprodajna_cijena", 0)
    cap_odgovornosti_posto = podaci.get("cap_odgovornosti_posto", 20)
    cap_eur = kupoprodajna_cijena * cap_odgovornosti_posto / 100
    survival_period = podaci.get("survival_period_godina", 2)
    n1 = clanak_ref[0]; clanak_ref[0] += 1
    n2 = clanak_ref[0]; clanak_ref[0] += 1
    god_oblik = "godinu" if survival_period == 1 else ("godine" if survival_period < 5 else "godina")
    return (
        "<div class='section-title' style='text-align: center;'>IZJAVE I JAMSTVA PRODAVATELJA</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n1}.</div>"
        f"<div class='justified'>(1) Prodavatelj izjavljuje i jamči Kupcu:<br><br>"
        f"a) Da je Prodavatelj valjano osnovan i registriran te da ima sve potrebne "
        f"ovlasti za sklapanje i izvršenje ovog Ugovora, uključujući odluku glavne "
        f"skupštine sukladno čl. 301.a ZTD-a;<br>"
        f"b) Da imovina navedena u ovom Ugovoru čini cjelokupnu imovinu Poduzeća;<br>"
        f"c) Da, osim eventualne hipoteke navedene u ovom Ugovoru, ne postoje drugi "
        f"tereti ili prava trećih osoba na imovini Poduzeća;<br>"
        f"d) Da su financijska izvješća Prodavatelja istinita, potpuna i točna;<br>"
        f"e) Da Prodavatelj uredno ispunjava sve porezne obveze;<br>"
        f"f) Da, osim sporova navedenih u ovom Ugovoru, ne postoje drugi sudski, "
        f"arbitražni ili upravni postupci vezani uz Poduzeće.<br><br>"
        f"(2) Ukupna kumulativna odgovornost Prodavatelja po osnovi svih zahtjeva "
        f"koji se temelje na povredi izjava i jamstava iz stavka 1. ovog članka "
        f"ograničena je na iznos od <b>{format_eur_s_rijecima(cap_eur)}</b> "
        f"({cap_odgovornosti_posto}% kupoprodajne cijene; dalje: <b>Gornja granica odgovornosti</b>).<br><br>"
        f"(3) Kupac nema pravo podnijeti zahtjev Prodavatelju za povredu izjave ili "
        f"jamstva ako iznos tog pojedinog zahtjeva ne prelazi "
        f"<b>{format_eur_s_rijecima(5000)}</b> "
        f"(dalje: <b>Prag de minimis</b>). Ako zbroj više zahtjeva koji su svaki ispod "
        f"Praga de minimis prelazi {format_eur_s_rijecima(20000)}, Kupac ima pravo "
        f"podnijeti zahtjev za cijeli zbroj.<br><br>"
        f"(4) Svi zahtjevi temeljem izjava i jamstava moraju biti podneseni najkasnije u "
        f"roku od <b>{survival_period} ({survival_period}) {god_oblik}</b> "
        f"od dana primopredaje Poduzeća, uz iznimku poreznih i radnopravnih zahtjeva za "
        f"koje rok iznosi 3 (tri) godine (dalje: <b>Rok važenja jamstava</b>).</div><br>"
        f"<div class='section-title' style='text-align: center;'>IZJAVE I JAMSTVA KUPCA</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n2}.</div>"
        f"<div class='justified'>Kupac izjavljuje i jamči Prodavatelju:<br><br>"
        f"a) Da je Kupac valjano osnovan i registriran te da ima sve potrebne ovlasti "
        f"za sklapanje i izvršenje ovog Ugovora;<br>"
        f"b) Da Kupac raspolaže financijskim sredstvima potrebnim za plaćanje "
        f"kupoprodajne cijene;<br>"
        f"c) Da je Kupac upoznat sa stanjem Poduzeća na temelju provedenog dubinskog "
        f"snimanja te da Poduzeće kupuje u viđenom stanju.</div><br>"
    )


def _sec_porezne_odredbe(podaci, clanak_ref):
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>Porezne odredbe</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
        f"<div class='justified'>(1) Porez na promet nekretnina koji temeljem ovog "
        f"Ugovora tereti prijenos nekretnine snosi Kupac, sukladno Zakonu o porezu na "
        f"promet nekretnina.<br><br>"
        f"(2) Ugovorne strane suglasno utvrđuju da se ovim Ugovorom prenosi Poduzeće "
        f"kao gospodarska cjelina u smislu čl. 8. Zakona o porezu na dodanu vrijednost, "
        f"zbog čega taj prijenos ne podliježe oporezivanju PDV-om, pod uvjetom da Kupac "
        f"nastavlja obavljati istu gospodarsku djelatnost. Kupac izričito izjavljuje da "
        f"namjerava nastaviti obavljati predmetnu djelatnost te se obvezuje bez odgode "
        f"obavijestiti nadležnu ispostavu Porezne uprave o stjecanju gospodarske cjeline. "
        f"Ako zbog Kupčeve radnje ili propusta Porezna uprava naknadno razreže PDV, "
        f"isključivi teret tog razreza snosi Kupac te se obvezuje Prodavatelja "
        f"obeštećenjem zaštititi od takvih tražbina.<br><br>"
        f"(3) Sve ostale poreze i javna davanja snose ugovorne strane sukladno "
        f"zakonskim odredbama.</div><br>"
    )


def _sec_primopredaja(podaci, clanak_ref):
    rok = podaci.get("rok_primopredaje", 0)
    rok_tekst = f"{rok} ({rok}) dana" if rok else "___"
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>Primopredaja Poduzeća</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
        f"<div class='justified'>(1) Primopredaja Poduzeća izvršit će se u roku od "
        f"<b>{rok_tekst}</b> od dana potpisa ovog Ugovora, osim ako ovim Ugovorom za "
        f"pojedine dijelove imovine nije predviđen drukčiji rok.<br><br>"
        f"(2) O primopredaji će se sastaviti zapisnik koji potpisuju obje ugovorne strane, "
        f"a koji će sadržavati detaljan popis sve prenesene imovine, obveza, ugovora i "
        f"dokumentacije.<br><br>"
        f"(3) Rizik slučajne propasti ili oštećenja imovine Poduzeća prelazi na Kupca "
        f"danom primopredaje, sukladno čl. 378. ZOO-a.</div><br>"
    )


def _sec_nedostaci(podaci, clanak_ref):
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>Odgovornost za materijalne i pravne nedostatke</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
        f"<div class='justified'>(1) Prodavatelj odgovara Kupcu za materijalne i pravne "
        f"nedostatke prenesene imovine sukladno odredbama ZOO-a (čl. 400.–422. ZOO-a).<br><br>"
        f"(2) Kupac je dužan pregledati Poduzeće pri preuzimanju te o eventualnim "
        f"vidljivim nedostacima bez odgode obavijestiti Prodavatelja.<br><br>"
        f"(3) Za skrivene nedostatke koji se pokažu u roku od 2 (dvije) godine od "
        f"primopredaje, Kupac je dužan obavijestiti Prodavatelja u roku od 2 (dva) "
        f"mjeseca od otkrivanja nedostatka.</div><br>"
    )


def _sec_ugovorna_kazna(podaci, clanak_ref):
    ugovorna_kazna = podaci.get("ugovorna_kazna", 100000)
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>Ugovorna kazna</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
        f"<div class='justified'>(1) U slučaju da bilo koja ugovorna strana ne ispuni "
        f"ili neuredno ispuni svoje obveze iz ovog Ugovora, druga strana ima pravo "
        f"zahtijevati ispunjenje obveze te naknadu štete sukladno općim pravilima ZOO-a.<br><br>"
        f"(2) U slučaju da Prodavatelj odustane od izvršenja ovog Ugovora nakon njegova "
        f"sklapanja, dužan je Kupcu platiti ugovornu kaznu u iznosu od "
        f"<b>{format_eur_s_rijecima(ugovorna_kazna)}</b>, neovisno o eventualnoj naknadi štete.<br><br>"
        f"(3) U slučaju da Kupac odustane od izvršenja ovog Ugovora nakon njegova "
        f"sklapanja, dužan je Prodavatelju platiti ugovornu kaznu u istom iznosu od "
        f"<b>{format_eur_s_rijecima(ugovorna_kazna)}</b>, neovisno o eventualnoj naknadi štete.</div><br>"
    )


def _sec_povjerljivost(podaci, clanak_ref):
    rok = podaci.get("rok_povjerljivosti", 0)
    rok_tekst = f"{rok} ({rok}) {('godinu' if rok == 1 else 'godine' if rok < 5 else 'godina')}" if rok else "___"
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>Povjerljivost</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
        f"<div class='justified'>(1) Ugovorne strane se obvezuju čuvati kao poslovnu "
        f"tajnu sve informacije i podatke koje su saznale u vezi s ovim Ugovorom, "
        f"uključujući podatke iz postupka dubinskog snimanja, a koje nisu javno dostupne.<br><br>"
        f"(2) Obveza povjerljivosti traje <b>{rok_tekst}</b> od dana sklapanja ovog "
        f"Ugovora.</div><br>"
    )


def _sec_sporovi(podaci, clanak_ref):
    sud_mjesto = podaci.get("sud_mjesto", "Zagrebu")
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>Rješavanje sporova</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
        f"<div class='justified'>(1) Ugovorne strane će nastojati sve sporove koji "
        f"proizlaze iz ovog Ugovora riješiti sporazumno, mirnim putem.<br><br>"
        f"(2) U slučaju da sporazumno rješavanje nije moguće u roku od 30 (trideset) "
        f"dana od nastanka spora, za rješavanje spora nadležan je stvarno i mjesno "
        f"nadležni sud u {format_text(sud_mjesto)}.</div><br>"
    )


def _sec_zavrsne(podaci, clanak_ref):
    broj_primjeraka = podaci.get("broj_primjeraka", 0)
    primjerci_tekst = f"{broj_primjeraka} ({broj_primjeraka})" if broj_primjeraka else "___"
    n = clanak_ref[0]; clanak_ref[0] += 1
    return (
        f"<div class='section-title' style='text-align: center;'>Završne odredbe</div>"
        f"<div class='section-title' style='text-align: center;'>Članak {n}.</div>"
        f"<div class='justified'>(1) Ovaj Ugovor stupa na snagu danom potpisa obiju "
        f"ugovornih strana.<br><br>"
        f"(2) Izmjene i dopune ovog Ugovora valjane su samo ako su učinjene u pisanom "
        f"obliku i potpisane od obiju ugovornih strana.<br><br>"
        f"(3) Ako se bilo koja odredba ovog Ugovora pokaže ništetnom ili nevažećom, "
        f"to neće utjecati na valjanost preostalih odredaba, a ništetna odredba "
        f"zamijenit će se valjanom odredbom koja najbliže odgovara gospodarskoj svrsi "
        f"i namjeri ugovornih strana.<br><br>"
        f"(4) Na sva pitanja koja nisu uređena ovim Ugovorom primjenjuju se odredbe "
        f"ZOO-a, ZTD-a, ZR-a i drugih relevantnih propisa Republike Hrvatske.<br><br>"
        f"(5) Ovaj Ugovor sastavljen je u <b>{primjerci_tekst}</b> istovjetnih primjeraka, "
        f"od kojih svaka ugovorna strana zadržava po jednak broj primjeraka.</div><br>"
    )


_SEKCIJE_FN_PRODAJA = {
    "predmet": _sec_predmet,
    "cijena": _sec_cijena,
    "nekretnine": _sec_nekretnine,
    "trabine": _sec_trabine,
    "mjenice": _sec_mjenice,
    "poslovni_udjeli": _sec_poslovni_udjeli,
    "pokretnine": _sec_pokretnine,
    "vrijednosni_papiri": _sec_vrijednosni_papiri,
    "novcana_sredstva": _sec_novcana_sredstva,
    "preuzete_obveze": _sec_preuzete_obveze,
    "radni_odnosi": _sec_radni_odnosi,
    "tekuci_ugovori": _sec_tekuci_ugovori,
    "zabrana_natjecanja": _sec_zabrana_natjecanja,
    "prezivjela_jamstva": _sec_prezivjela_jamstva,
    "izjave_jamstva": _sec_izjave_jamstva,
    "porezne_odredbe": _sec_porezne_odredbe,
    "primopredaja": _sec_primopredaja,
    "nedostaci": _sec_nedostaci,
    "ugovorna_kazna": _sec_ugovorna_kazna,
    "povjerljivost": _sec_povjerljivost,
    "sporovi": _sec_sporovi,
    "zavrsne": _sec_zavrsne,
}


def generiraj_prodaju_poduzeca(prodavatelj, kupac, podaci, sekcije_redoslijed=None):
    """
    Ugovor o prodaji poduzeća kao organizirane gospodarske cjeline - ZOO, ZTD čl. 275, ZR čl. 137
    ZAHTIJEVANA FORMA: PISANA (javnobilježnička ovjera preporučena; clausula intabulandi obvezna za nekretnine)
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")

        if sekcije_redoslijed is None:
            sekcije_redoslijed = [s["id"] for s in SEKCIJE_PRODAJA_PODUZECA if s["ukljuceno"]]

        clanak_ref = [1]
        parts = [
            "<div style='text-align: center; font-size: 10pt; "
            "border: 1px solid #999; padding: 8px; margin-bottom: 20px;'>"
            "ZAHTIJEVANA FORMA: PISANA — za prijenos nekretnina obvezna clausula intabulandi; "
            "preporučuje se javnobilježnička solemnizacija</div>",
            "<div class='header-doc'>UGOVOR O PRODAJI PODUZEĆA</div>",
            f"<div class='justified'>Sklopljen u {mjesto}, dana {danas} godine, između:</div><br>",
            f"<div class='party-info'><b>1. PRODAVATELJ:</b><br>{prodavatelj}</div>",
            f"<div class='party-info'><b>2. KUPAC:</b><br>{kupac}</div><br>",
        ]

        for sek_id in sekcije_redoslijed:
            fn = _SEKCIJE_FN_PRODAJA.get(sek_id)
            if fn:
                parts.append(fn(podaci, clanak_ref))

        parts.append(
            f"<div class='justified'>{mjesto}, dana {danas} godine.</div><br><br>"
            f"<table width='100%' border='0'><tr>"
            f"<td width='50%' align='center'>"
            f"<b>ZA PRODAVATELJA</b><br><br><br>"
            f"______________________<br>"
            f"<small>(potpis i pečat)</small></td>"
            f"<td width='50%' align='center'>"
            f"<b>ZA KUPCA</b><br><br><br>"
            f"______________________<br>"
            f"<small>(potpis i pečat)</small></td>"
            f"</tr></table>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"



def generiraj_zapisnik_uprave(drustvo, podaci):
    """
    Zapisnik sjednice uprave - ZTD, Poslovnik o radu uprave
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        vrijeme_pocetak = podaci.get("vrijeme_pocetak", "10:00")
        vrijeme_kraj = podaci.get("vrijeme_kraj", "11:00")
        prisutni = podaci.get("prisutni", "")
        odsutni = podaci.get("odsutni", "")
        dnevni_red = podaci.get("dnevni_red", [])
        predsjednik = podaci.get("predsjednik_uprave", "")
        zapisnicar = podaci.get("zapisnicar", "")

        drustvo_info = (
            f"<b>{drustvo.get('tvrtka', '')}</b><br>"
            f"Sjedište: {drustvo.get('sjediste', '')}<br>"
            f"OIB: {drustvo.get('oib', '')}, MBS: {drustvo.get('mbs', '')}"
        )

        parts = [
            f"<div class='party-info' style='font-size: 10pt;'>{drustvo_info}</div><br>",
            "<div class='header-doc'>ZAPISNIK<br>"
            "<span style='font-size: 12pt; font-weight: normal;'>"
            "sjednice Uprave društva</span></div>",
            f"<div class='justified'>"
            f"Sjednica Uprave održana je u {mjesto}, dana <b>{danas}</b>, "
            f"s početkom u {vrijeme_pocetak} sati.</div><br>",
            f"<div class='justified'><b>Prisutni članovi Uprave:</b> {format_text(prisutni)}</div>",
        ]

        if odsutni:
            parts.append(
                f"<div class='justified'><b>Odsutni:</b> {format_text(odsutni)}</div>"
            )

        if zapisnicar:
            parts.append(
                f"<div class='justified'><b>Zapisničar:</b> {format_text(zapisnicar)}</div>"
            )

        parts.append(
            "<br><div class='justified'>Predsjednik Uprave konstatira da je sjednica "
            "pravovaljano sazvana te da postoji kvorum potreban za donošenje pravovaljanih odluka.</div><br>"
        )

        parts.append("<div class='section-title'>DNEVNI RED:</div>")
        for i, tocka in enumerate(dnevni_red, 1):
            naslov = tocka.get("naslov", "")
            rasprava = tocka.get("rasprava", "")
            odluka = tocka.get("odluka", "")
            glasovi = tocka.get("glasovi", "jednoglasno")

            parts.append(f"<div class='justified'>{i}. {format_text(naslov)}</div>")

        parts.append("<br>")

        for i, tocka in enumerate(dnevni_red, 1):
            naslov = tocka.get("naslov", "")
            rasprava = tocka.get("rasprava", "")
            odluka = tocka.get("odluka", "")
            glasovi = tocka.get("glasovi", "jednoglasno")

            parts.append(
                f"<div class='section-title'>Ad {i}. {format_text(naslov)}</div>"
            )
            if rasprava:
                parts.append(
                    f"<div class='justified'>{format_text(rasprava)}</div><br>"
                )
            if odluka:
                parts.append(
                    f"<div class='justified'><b>ODLUKA:</b> {format_text(odluka)}</div>"
                    f"<div class='justified'><i>Glasovanje: {format_text(glasovi)}</i></div><br>"
                )

        parts.append(
            f"<div class='justified'>Sjednica je završena u {vrijeme_kraj} sati.</div>"
            f"<br><br>"
            f'<table width="100%" border="0"><tr>'
            f'<td width="50%" align="center"><b>ZAPISNIČAR</b><br><br><br>______________________</td>'
            f'<td width="50%" align="center"><b>PREDSJEDNIK UPRAVE</b><br><br><br>______________________</td>'
            f"</tr></table>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
