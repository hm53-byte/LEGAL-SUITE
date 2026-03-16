# -----------------------------------------------------------------------------
# GENERATORI: Trgovacko pravo
# Drustveni ugovor, Odluka skupstine, Prijenos udjela, NDA, Zapisnik uprave
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur, _rimski_broj


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
            f"<div class='justified'>Temeljni kapital društva iznosi <b>{format_eur(temeljni_kapital)}</b>.</div><br>"
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
            f"<b>{format_eur(nominalni_iznos)}</b> u društvu:<br><br>"
            f"<b>{drustvo_info}</b><br><br>"
            f"Ovim ugovorom Prenositelj prenosi navedeni poslovni udio na Stjecatelja.</div><br>"
        )
        clanak += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Naknada)</div>"
            f"<div class='justified'>Ugovorena cijena za prijenos poslovnog udjela iznosi "
            f"<b>{format_eur(cijena)}</b>.<br><br>"
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
