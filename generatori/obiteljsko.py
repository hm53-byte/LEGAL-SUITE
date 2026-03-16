# -----------------------------------------------------------------------------
# GENERATORI: Obiteljsko pravo (razvod, bracni ugovor, roditeljska skrb, uzdrzavanje)
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur, _rimski_broj


def generiraj_sporazum_razvod(predlagatelj1, predlagatelj2, podaci):
    """
    Generira prijedlog za sporazumni razvod braka.
    Pravni temelj: Obiteljski zakon (NN 103/15, 98/19, 47/20, 49/23) cl. 50-55.
    """
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum_braka = podaci.get('datum_braka', '________')
        mjesto_braka = podaci.get('mjesto_braka', '________')
        djeca = podaci.get('djeca', [])
        ima_savjetovanje = podaci.get('ima_savjetovanje', False)
        plan_roditeljske_skrbi = podaci.get('plan_roditeljske_skrbi', '')
        petitum = podaci.get('petitum', '')

        parts = [
            f"<div style='font-weight: bold; font-size: 14px; text-align: left;'>"
            f"OPĆINSKI SUD U {format_text(mjesto).upper()}</div><br>",

            f"<div class='party-info'>"
            f"<b>PREDLAGATELJ 1:</b><br>{predlagatelj1}<br><br>"
            f"<b>PREDLAGATELJ 2:</b><br>{predlagatelj2}"
            f"</div><br>",

            f"<div class='header-doc'>PRIJEDLOG ZA SPORAZUMNI RAZVOD BRAKA</div>",

            f"<div class='section-title'>I. ČINJENIČNO STANJE</div>",
            f"<div class='justified'>"
            f"Predlagatelji su sklopili brak dana <b>{format_text(datum_braka)}</b> "
            f"u mjestu <b>{format_text(mjesto_braka)}</b>, što se dokazuje izvatkom iz matice vjenčanih.<br><br>"
            f"<b>Dokaz:</b> Izvadak iz matice vjenčanih."
            f"</div>",

            f"<div class='section-title'>II. POREMEĆAJ BRAČNIH ODNOSA</div>",
            f"<div class='justified'>"
            f"Predlagatelji sporazumno izjavljuju da su njihovi bračni odnosi teško i trajno poremećeni, "
            f"da su pokušali riješiti međusobne nesuglasice, ali u tome nisu uspjeli, te da zajednički "
            f"predlažu razvod braka sukladno članku 50. Obiteljskog zakona."
            f"</div>",
        ]

        # III. MALOLJETNA DJECA
        if djeca:
            parts.append(f"<div class='section-title'>III. MALOLJETNA DJECA</div>")
            parts.append(f"<div class='justified'>")
            parts.append(f"Iz braka Predlagatelja potječu sljedeća maloljetna djeca:<br><br>")
            for i, dijete in enumerate(djeca, 1):
                ime = format_text(dijete.get('ime', ''))
                datum_r = format_text(dijete.get('datum_rodjenja', ''))
                parts.append(f"{i}. <b>{ime}</b>, rođen/a dana {datum_r}<br>")
            parts.append(f"<br>")
            if ima_savjetovanje:
                parts.append(
                    f"Predlagatelji su sudjelovali u obveznom savjetovanju "
                    f"prije pokretanja sudskog postupka, sukladno članku 321. Obiteljskog zakona."
                    f"<br><br>"
                )
            else:
                parts.append(
                    f"<i>Napomena: Sukladno članku 321. Obiteljskog zakona, bračni drugovi koji imaju "
                    f"zajedničku maloljetnu djecu dužni su prije pokretanja postupka sudjelovati "
                    f"u obveznom savjetovanju.</i><br><br>"
                )
            if plan_roditeljske_skrbi:
                parts.append(
                    f"Predlagatelji prilažu plan o zajedničkoj roditeljskoj skrbi: "
                    f"<b>{format_text(plan_roditeljske_skrbi)}</b>.<br>"
                )
            parts.append(f"</div>")

            # IV. PETITUM
            parts.append(f"<div class='section-title'>IV. PETITUM</div>")
        else:
            # III. PETITUM (nema djece)
            parts.append(f"<div class='section-title'>III. PETITUM</div>")

        if petitum:
            parts.append(f"<div class='justified'>{format_text(petitum)}</div>")
        else:
            parts.append(
                f"<div class='justified'>"
                f"Predlagatelji predlažu da naslovni sud donese sljedeće<br><br>"
                f"<div style='text-align: center; font-weight: bold;'>RJEŠENJE</div><br>"
                f"<b>Razvodi se brak</b> sklopljen dana <b>{format_text(datum_braka)}</b> "
                f"u <b>{format_text(mjesto_braka)}</b> između Predlagatelja 1 i Predlagatelja 2."
                f"</div>"
            )

        # Napomena o savjetovanju
        if djeca and not ima_savjetovanje:
            parts.append(
                f"<br><div style='border: 1px solid #cc0000; padding: 10px; margin: 15px 0; "
                f"background-color: #fff5f5;'>"
                f"<b>VAŽNA NAPOMENA:</b> Bračni drugovi koji imaju zajedničku maloljetnu djecu "
                f"obvezni su prije podnošenja prijedloga za razvod braka sudjelovati u postupku "
                f"obveznog savjetovanja (čl. 321.-325. Obiteljskog zakona). Prijedlogu se prilaže "
                f"potvrda o provedenom obveznom savjetovanju."
                f"</div>"
            )

        parts.append(f"<br><div class='justified'>U {format_text(mjesto)}, dana {datum}</div>")

        parts.append(f"""
        <div class='signature-row'>
            <div class='signature-block'>
                <b>PREDLAGATELJ 1</b>
                <br><br><br>
                ______________________
            </div>
            <div class='signature-block'>
                <b>PREDLAGATELJ 2</b>
                <br><br><br>
                ______________________
            </div>
        </div>
        """)

        parts.append(
            f"<br><div class='justified'><b>PRILOZI:</b><br>"
            f"1. Izvadak iz matice vjenčanih<br>"
            f"2. Izvadci iz matice rođenih za djecu (ako ih ima)<br>"
            f"3. Potvrda o provedenom obveznom savjetovanju (ako ima maloljetne djece)<br>"
            f"4. Plan o zajedničkoj roditeljskoj skrbi (ako ima maloljetne djece)<br>"
            f"5. Preslika osobnih iskaznica Predlagatelja"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_tuzbu_razvod(tuzitelj, tuzenik, podaci):
    """
    Generira tuzbu za razvod braka (sporni razvod).
    Pravni temelj: Obiteljski zakon (NN 103/15, 98/19, 47/20, 49/23) cl. 47-49.
    """
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get('mjesto', 'Zagreb')
        sud = podaci.get('sud', f'OPĆINSKI SUD U {mjesto.upper()}')
        datum_braka = podaci.get('datum_braka', '________')
        mjesto_braka = podaci.get('mjesto_braka', '________')
        djeca = podaci.get('djeca', [])
        razlog = podaci.get('razlog', '')
        ima_savjetovanje = podaci.get('ima_savjetovanje', False)
        zahtjev_djeca = podaci.get('zahtjev_djeca', '')
        vps = podaci.get('vps', 0)

        parts = [
            f"<div style='font-weight: bold; font-size: 14px; text-align: left;'>"
            f"{format_text(sud).upper()}</div><br>",
        ]

        if vps:
            parts.append(
                f"<div style='text-align: right; font-size: 10pt;'>"
                f"VPS: {format_eur(vps)}</div><br>"
            )

        parts.append(
            f"<div class='party-info'>"
            f"<b>TUŽITELJ:</b><br>{tuzitelj}<br><br>"
            f"<b>TUŽENIK:</b><br>{tuzenik}"
            f"</div>"
            f"<div class='party-info'><b>Radi:</b> Razvoda braka</div><br>"
        )

        parts.append(f"<div class='header-doc'>TUŽBA ZA RAZVOD BRAKA</div>")

        # I. ČINJENIČNO STANJE
        parts.append(f"<div class='section-title'>I. ČINJENIČNO STANJE</div>")
        parts.append(
            f"<div class='justified'>"
            f"Stranke su sklopile brak dana <b>{format_text(datum_braka)}</b> "
            f"u mjestu <b>{format_text(mjesto_braka)}</b>, što je upisano u maticu vjenčanih.<br><br>"
            f"<b>Dokaz:</b> Izvadak iz matice vjenčanih."
            f"</div>"
        )

        # II. RAZLOZI RAZVODA
        parts.append(f"<div class='section-title'>II. RAZLOZI RAZVODA</div>")
        parts.append(
            f"<div class='justified'>"
            f"Bračni odnosi stranaka su teško i trajno poremećeni. "
        )
        if razlog:
            parts.append(f"{format_text(razlog)}<br><br>")
        else:
            parts.append(
                f"Tužitelj navodi da su bračni odnosi postali nepodnošljivi "
                f"te da ne postoji mogućnost njihovog popravljanja.<br><br>"
            )
        parts.append(
            f"Sukladno članku 47. Obiteljskog zakona, svaki bračni drug može tužbom tražiti "
            f"razvod braka ako su bračni odnosi teško i trajno poremećeni, odnosno ako bračni "
            f"drugovi žive odvojeno više od jedne godine.<br><br>"
            f"<b>Dokaz:</b> Saslušanje stranaka, svjedoci."
            f"</div>"
        )

        # III. MALOLJETNA DJECA
        if djeca:
            parts.append(f"<div class='section-title'>III. MALOLJETNA DJECA</div>")
            parts.append(f"<div class='justified'>")
            parts.append(f"Iz braka stranaka potječu sljedeća maloljetna djeca:<br><br>")
            for i, dijete in enumerate(djeca, 1):
                ime = format_text(dijete.get('ime', ''))
                datum_r = format_text(dijete.get('datum_rodjenja', ''))
                parts.append(f"{i}. <b>{ime}</b>, rođen/a dana {datum_r}<br>")
            parts.append(f"<br>")
            if ima_savjetovanje:
                parts.append(
                    f"Tužitelj je sudjelovao u obveznom savjetovanju sukladno "
                    f"članku 321. Obiteljskog zakona.<br><br>"
                )
            if zahtjev_djeca:
                parts.append(
                    f"U pogledu roditeljske skrbi i uzdržavanja djece, Tužitelj predlaže:<br>"
                    f"{format_text(zahtjev_djeca)}<br><br>"
                )
            parts.append(
                f"<b>Dokaz:</b> Izvadci iz matice rođenih za djecu, "
                f"potvrda o provedenom obveznom savjetovanju."
            )
            parts.append(f"</div>")

            # IV. TUŽBENI ZAHTJEV
            parts.append(f"<div class='section-title'>IV. TUŽBENI ZAHTJEV</div>")
        else:
            # III. TUŽBENI ZAHTJEV (nema djece)
            parts.append(f"<div class='section-title'>III. TUŽBENI ZAHTJEV</div>")

        parts.append(
            f"<div class='justified'>"
            f"Slijedom svega navedenog, Tužitelj predlaže da naslovni sud donese sljedeću<br><br>"
            f"<div style='text-align: center; font-weight: bold;'>PRESUDU</div><br>"
            f"<b>I.</b> Razvodi se brak sklopljen dana <b>{format_text(datum_braka)}</b> "
            f"u <b>{format_text(mjesto_braka)}</b> između Tužitelja i Tuženika.<br><br>"
        )

        if djeca and zahtjev_djeca:
            parts.append(
                f"<b>II.</b> {format_text(zahtjev_djeca)}<br><br>"
                f"<b>III.</b> Nalaže se Tuženiku naknaditi Tužitelju troškove ovog postupka."
            )
        else:
            parts.append(
                f"<b>II.</b> Nalaže se Tuženiku naknaditi Tužitelju troškove ovog postupka."
            )

        parts.append(f"</div>")

        parts.append(f"<br><div class='justified'>U {format_text(mjesto)}, dana {datum}</div>")

        parts.append(
            f"<br><div class='justified'><b>PRILOZI:</b><br>"
            f"1. Izvadak iz matice vjenčanih<br>"
            f"2. Preslika osobne iskaznice Tužitelja<br>"
            f"3. Dokaz o uplati sudske pristojbe<br>"
        )
        if djeca:
            parts.append(
                f"4. Izvadci iz matice rođenih za djecu<br>"
                f"5. Potvrda o provedenom obveznom savjetovanju<br>"
            )
        parts.append(f"</div>")

        parts.append(f"""
        <br>
        <div class='signature-row'>
            <div style='display:inline-block; width: 50%;'></div>
            <div class='signature-block'>
                <b>TUŽITELJ</b>
                <br><br><br>
                ______________________
            </div>
        </div>
        """)

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_bracni_ugovor(strana1, strana2, podaci):
    """
    Generira bracni ugovor (ugovor o uredjenju imovinskih odnosa / diobi bracne imovine).
    ZAHTIJEVANA FORMA: Javnobiljeznicki akt ili solemnizacija (cl. 40. Obiteljskog zakona).
    """
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get('mjesto', 'Zagreb')
        vrsta = podaci.get('vrsta', 'bracni')
        imovina_items = podaci.get('imovina_items', [])
        clausula_intabulandi = podaci.get('clausula_intabulandi', False)
        dozvola_uknjizbe_tekst = podaci.get('dozvola_uknjizbe_tekst', '')

        if vrsta == 'dioba':
            naslov = "UGOVOR O DIOBI BRAČNE IMOVINE"
        else:
            naslov = "UGOVOR O UREĐENJU IMOVINSKIH ODNOSA"

        parts = [
            f"<div style='border: 2px solid black; padding: 10px; margin-bottom: 20px; "
            f"text-align: center; background-color: #f9f9f9;'>"
            f"<b>ZAHTIJEVANA FORMA:</b><br>"
            f"JAVNOBILJEŽNIČKI AKT ILI SOLEMNIZACIJA<br>"
            f"<span style='font-size: 10pt;'>(čl. 40. Obiteljskog zakona)</span>"
            f"</div>",

            f"<div class='header-doc'>{naslov}</div>",

            f"<div class='justified'>"
            f"Sklopljen u mjestu <b>{format_text(mjesto)}</b>, dana {datum} godine, između:"
            f"</div><br>",

            f"<div class='party-info'>"
            f"1. <b>UGOVORNA STRANA 1:</b><br>{strana1}<br><br>"
            f"2. <b>UGOVORNA STRANA 2:</b><br>{strana2}"
            f"</div><br>",
        ]

        brojac_clanka = 1

        # Clanak 1: Stranke i brak
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {brojac_clanka}.</div>"
        )
        if vrsta == 'predbracni':
            parts.append(
                f"<div class='justified'>"
                f"Ugovorne strane namjeravaju sklopiti brak te ovim Ugovorom, sukladno "
                f"člancima 34.-40. Obiteljskog zakona, uređuju svoje imovinske odnose "
                f"za vrijeme trajanja braka i u slučaju njegova prestanka."
                f"</div>"
            )
        elif vrsta == 'dioba':
            parts.append(
                f"<div class='justified'>"
                f"Ugovorne strane ovim Ugovorom provode diobu bračne stečevine, "
                f"sukladno člancima 34.-40. i 248.-259. Obiteljskog zakona. "
                f"Svaka strana postaje isključivi vlasnik imovine kako je navedeno u nastavku."
                f"</div>"
            )
        else:
            parts.append(
                f"<div class='justified'>"
                f"Ugovorne strane su bračni drugovi te ovim Ugovorom, sukladno "
                f"člancima 34.-40. Obiteljskog zakona, uređuju svoje imovinske odnose "
                f"za vrijeme trajanja braka i u slučaju njegova prestanka."
                f"</div>"
            )
        brojac_clanka += 1

        # Clanci za svaki imovinski predmet
        for item in imovina_items:
            parts.append(
                f"<div class='section-title' style='text-align: center;'>Članak {brojac_clanka}.</div>"
            )
            opis = format_text(item.get('opis', ''))
            vrsta_imovine = item.get('vrsta', 'pokretnina')
            vlasnik = format_text(item.get('vlasnik', ''))
            zk_podaci = item.get('zk_podaci', {})

            parts.append(f"<div class='justified'>")
            parts.append(f"Ugovorne strane sporazumno utvrđuju da sljedeća imovina:<br><br>")
            parts.append(f"<b>Opis:</b> {opis}<br>")
            parts.append(f"<b>Vrsta:</b> {format_text(vrsta_imovine)}<br>")

            if vrsta_imovine == 'nekretnina' and zk_podaci:
                ko = format_text(zk_podaci.get('ko', ''))
                ulozak = format_text(zk_podaci.get('ulozak', ''))
                cestica = format_text(zk_podaci.get('cestica', ''))
                parts.append(
                    f"<br><b>Zemljišnoknjižni podaci:</b><br>"
                    f"Katastarska općina (k.o.): {ko}<br>"
                    f"Broj zk. uloška: {ulozak}<br>"
                    f"Broj čestice (k.č.br.): {cestica}<br>"
                )

            parts.append(f"<br>pripada u isključivo vlasništvo: <b>{vlasnik}</b>.")
            parts.append(f"</div>")
            brojac_clanka += 1

        # Clausula intabulandi
        if clausula_intabulandi:
            parts.append(
                f"<div class='section-title' style='text-align: center;'>Članak {brojac_clanka}.</div>"
            )
            parts.append(
                f"<div class='justified clausula'>"
            )
            if dozvola_uknjizbe_tekst:
                parts.append(f"{format_text(dozvola_uknjizbe_tekst)}")
            else:
                parts.append(
                    f"Ugovorna strana koja se odriče prava vlasništva na nekretnini navedenoj "
                    f"u ovom Ugovoru daje izričitu, bezuvjetnu i neopoziva suglasnost "
                    f"(<i>clausula intabulandi</i>) da se u zemljišnoj knjizi, bez njezina "
                    f"daljnjeg pitanja ili odobrenja, provede uknjižba prava vlasništva "
                    f"u korist druge Ugovorne strane."
                )
            parts.append(f"</div>")
            brojac_clanka += 1

        # Zavrsne odredbe
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {brojac_clanka}.</div>"
        )
        parts.append(
            f"<div class='justified'>"
            f"Ovaj Ugovor sastavljen je u četiri (4) istovjetna primjerka, od kojih svaka "
            f"Ugovorna strana zadržava po jedan primjerak, a dva primjerka se zadržavaju "
            f"u spisu javnog bilježnika."
            f"</div>"
        )
        brojac_clanka += 1

        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {brojac_clanka}.</div>"
        )
        parts.append(
            f"<div class='justified'>"
            f"Ugovorne strane potvrđuju da su ovaj Ugovor pročitale, da razumiju njegov "
            f"sadržaj i pravne učinke, te da ga potpisuju kao izraz svoje slobodne volje."
            f"</div>"
        )

        # JB ovjera
        parts.append(
            f"<br><div style='border: 1px dashed #333; padding: 15px; margin: 20px 0;'>"
            f"<b>JAVNOBILJEŽNIČKA OVJERA / SOLEMNIZACIJA</b><br><br>"
            f"Javni bilježnik: ________________________________________<br>"
            f"Sjedište: ________________________________________<br>"
            f"Poslovni broj: ________________________________________<br><br>"
            f"Potvrđujem da su Ugovorne strane vlastoručno potpisale ovaj Ugovor "
            f"pred javnim bilježnikom, nakon što im je pročitan i objašnjen.<br><br>"
            f"<div style='text-align: right;'>Javni bilježnik<br><br><br>"
            f"______________________<br>(pečat i potpis)</div>"
            f"</div>"
        )

        parts.append(f"<br><div class='justified'>U {format_text(mjesto)}, dana {datum}</div>")

        parts.append(f"""
        <div class='signature-row'>
            <div class='signature-block'>
                <b>UGOVORNA STRANA 1</b>
                <br>(vlastoručni potpis pred javnim bilježnikom)
                <br><br><br>
                ______________________
            </div>
            <div class='signature-block'>
                <b>UGOVORNA STRANA 2</b>
                <br>(vlastoručni potpis pred javnim bilježnikom)
                <br><br><br>
                ______________________
            </div>
        </div>
        """)

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_roditeljsku_skrb(roditelj1, roditelj2, podaci):
    """
    Generira plan o zajednickoj roditeljskoj skrbi.
    Pravni temelj: Obiteljski zakon (NN 103/15, 98/19, 47/20, 49/23) cl. 104-106.
    """
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get('mjesto', 'Zagreb')
        djeca = podaci.get('djeca', [])
        stanovanje_kod = podaci.get('stanovanje_kod', 1)
        adresa_djeteta = podaci.get('adresa_djeteta', '')
        raspored_kontakta = podaci.get('raspored_kontakta', '')
        praznici = podaci.get('praznici', '')
        ljetni_odmor = podaci.get('ljetni_odmor', '')
        alimentacija_iznos = podaci.get('alimentacija_iznos', 0)
        alimentacija_datum_dospijeca = podaci.get('alimentacija_datum_dospijeca', '')
        alimentacija_iban = podaci.get('alimentacija_iban', '')
        posebne_odredbe = podaci.get('posebne_odredbe', '')

        roditelj_stanovanje = "Roditelja 1" if stanovanje_kod == 1 else "Roditelja 2"

        parts = [
            f"<div class='header-doc'>PLAN O ZAJEDNIČKOJ RODITELJSKOJ SKRBI</div>",

            f"<div class='justified'>"
            f"Sastavljen u mjestu <b>{format_text(mjesto)}</b>, dana {datum}, između:"
            f"</div><br>",

            f"<div class='party-info'>"
            f"<b>RODITELJ 1:</b><br>{roditelj1}<br><br>"
            f"<b>RODITELJ 2:</b><br>{roditelj2}"
            f"</div><br>",

            f"<div class='justified'>"
            f"Roditelji su, sukladno člancima 104.-106. Obiteljskog zakona, "
            f"sporazumno sastavili ovaj Plan o zajedničkoj roditeljskoj skrbi."
            f"</div><br>",
        ]

        # I. PODACI O DJECI
        parts.append(f"<div class='section-title'>I. PODACI O DJECI</div>")
        parts.append(f"<div class='justified'>")
        if djeca:
            for i, dijete in enumerate(djeca, 1):
                ime = format_text(dijete.get('ime', ''))
                datum_r = format_text(dijete.get('datum_rodjenja', ''))
                oib = format_text(dijete.get('oib', ''))
                parts.append(f"{i}. <b>{ime}</b><br>")
                parts.append(f"&nbsp;&nbsp;&nbsp;Datum rođenja: {datum_r}<br>")
                if oib:
                    parts.append(f"&nbsp;&nbsp;&nbsp;OIB: {oib}<br>")
                parts.append(f"<br>")
        else:
            parts.append(f"(navesti podatke o djeci)<br>")
        parts.append(f"</div>")

        # II. MJESTO STANOVANJA DJETETA
        parts.append(f"<div class='section-title'>II. MJESTO STANOVANJA DJETETA</div>")
        parts.append(
            f"<div class='justified'>"
            f"Roditelji sporazumno utvrđuju da će dijete/djeca imati prebivalište "
            f"kod <b>{roditelj_stanovanje}</b>"
        )
        if adresa_djeteta:
            parts.append(f", na adresi: <b>{format_text(adresa_djeteta)}</b>")
        parts.append(
            f".<br><br>"
            f"Promjena prebivališta djeteta moguća je samo uz suglasnost oba roditelja "
            f"ili odlukom suda."
            f"</div>"
        )

        # III. VRIJEME PROVODJENJA S DJETETOM
        parts.append(f"<div class='section-title'>III. VRIJEME PROVOĐENJA S DJETETOM</div>")
        parts.append(f"<div class='justified'>")

        parts.append(f"<b>A) Redoviti raspored kontakta:</b><br>")
        if raspored_kontakta:
            parts.append(f"{format_text(raspored_kontakta)}<br><br>")
        else:
            parts.append(f"(navesti detaljan raspored)<br><br>")

        parts.append(f"<b>B) Praznici i blagdani:</b><br>")
        if praznici:
            parts.append(f"{format_text(praznici)}<br><br>")
        else:
            parts.append(f"(navesti raspored za praznike)<br><br>")

        parts.append(f"<b>C) Ljetni odmor:</b><br>")
        if ljetni_odmor:
            parts.append(f"{format_text(ljetni_odmor)}<br><br>")
        else:
            parts.append(f"(navesti raspored za ljetni odmor)<br><br>")

        parts.append(f"</div>")

        # IV. UZDRZAVANJE DJETETA
        parts.append(f"<div class='section-title'>IV. UZDRŽAVANJE DJETETA</div>")
        parts.append(f"<div class='justified'>")

        roditelj_obveznik = "Roditelj 2" if stanovanje_kod == 1 else "Roditelj 1"
        roditelj_primatelj = "Roditelj 1" if stanovanje_kod == 1 else "Roditelj 2"

        parts.append(
            f"<b>{roditelj_obveznik}</b> obvezuje se uplaćivati mjesečni iznos za "
            f"uzdržavanje djeteta/djece u iznosu od <b>{format_eur(alimentacija_iznos)}</b>.<br><br>"
        )

        if alimentacija_datum_dospijeca:
            parts.append(
                f"Uzdržavanje dospijeva svakog <b>{format_text(alimentacija_datum_dospijeca)}.</b> "
                f"u mjesecu za tekući mjesec.<br><br>"
            )

        if alimentacija_iban:
            parts.append(
                f"Uplata se vrši na IBAN: <b>{format_text(alimentacija_iban)}</b>, "
                f"koji glasi na {roditelj_primatelj}.<br><br>"
            )

        parts.append(
            f"Iznos uzdržavanja može se uskladiti jednom godišnje prema promjeni životnih "
            f"troškova, sporazumom roditelja ili odlukom suda."
        )
        parts.append(f"</div>")

        # V. POSEBNE ODREDBE
        if posebne_odredbe:
            parts.append(f"<div class='section-title'>V. POSEBNE ODREDBE</div>")
            parts.append(
                f"<div class='justified'>{format_text(posebne_odredbe)}</div>"
            )

        # Napomena
        parts.append(
            f"<br><div style='border: 1px solid #666; padding: 10px; margin: 15px 0; "
            f"background-color: #f5f5f5;'>"
            f"<b>NAPOMENA:</b> Ovaj plan podliježe odobrenju suda. "
            f"Tek pravomoćnošću sudskog rješenja kojim se plan odobrava, "
            f"plan postaje ovršna isprava u smislu članka 106. stavka 4. "
            f"Obiteljskog zakona. Do tada plan predstavlja sporazum roditelja "
            f"koji nema svojstvo ovršne isprave."
            f"</div>"
        )

        parts.append(f"<br><div class='justified'>U {format_text(mjesto)}, dana {datum}</div>")

        parts.append(f"""
        <div class='signature-row'>
            <div class='signature-block'>
                <b>RODITELJ 1</b>
                <br><br><br>
                ______________________
            </div>
            <div class='signature-block'>
                <b>RODITELJ 2</b>
                <br><br><br>
                ______________________
            </div>
        </div>
        """)

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_ugovor_uzdrzavanje(obveznik, primatelj, podaci):
    """
    Generira ugovor o uzdrzavanju.
    ZAHTIJEVANA FORMA: Solemnizacija pred javnim biljeznickom (za ovrsnost).
    Pravni temelj: Obiteljski zakon (NN 103/15, 98/19, 47/20, 49/23) cl. 307-312.
    """
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get('mjesto', 'Zagreb')
        iznos_mjesecno = podaci.get('iznos_mjesecno', 0)
        datum_dospijeca = podaci.get('datum_dospijeca', '')
        iban = podaci.get('iban', '')
        dijete_ime = podaci.get('dijete_ime', '')
        dijete_datum_rodjenja = podaci.get('dijete_datum_rodjenja', '')
        zakonski_zastupnik = podaci.get('zakonski_zastupnik', False)
        clausula_exequendi = podaci.get('clausula_exequendi', False)

        parts = [
            f"<div style='border: 2px solid black; padding: 10px; margin-bottom: 20px; "
            f"text-align: center; background-color: #f9f9f9;'>"
            f"<b>ZAHTIJEVANA FORMA:</b><br>"
            f"SOLEMNIZACIJA PRED JAVNIM BILJEŽNIKOM<br>"
            f"<span style='font-size: 10pt;'>(čl. 310. Obiteljskog zakona - za ovršnost ugovora)</span>"
            f"</div>",

            f"<div class='header-doc'>UGOVOR O UZDRŽAVANJU</div>",

            f"<div class='justified'>"
            f"Sklopljen u mjestu <b>{format_text(mjesto)}</b>, dana {datum} godine, između:"
            f"</div><br>",

            f"<div class='party-info'>"
            f"1. <b>OBVEZNIK UZDRŽAVANJA:</b><br>{obveznik}<br><br>"
            f"2. <b>PRIMATELJ UZDRŽAVANJA:</b><br>{primatelj}",
        ]

        if zakonski_zastupnik:
            parts.append(
                f"<br><i>(maloljetno dijete, zastupano po zakonskom zastupniku)</i>"
            )
        parts.append(f"</div><br>")

        brojac_clanka = 1

        # Clanak 1: Predmet ugovora
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {brojac_clanka}.</div>"
        )
        parts.append(
            f"<div class='justified'>"
            f"Obveznik uzdržavanja obvezuje se uzdržavati "
        )
        if dijete_ime:
            parts.append(
                f"maloljetno dijete <b>{format_text(dijete_ime)}</b>"
            )
            if dijete_datum_rodjenja:
                parts.append(f", rođeno dana {format_text(dijete_datum_rodjenja)}")
        else:
            parts.append(f"Primatelja uzdržavanja")
        parts.append(
            f", sukladno odredbama članaka 307.-312. Obiteljskog zakona."
            f"</div>"
        )
        brojac_clanka += 1

        # Clanak 2: Iznos
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {brojac_clanka}.</div>"
        )
        parts.append(
            f"<div class='justified'>"
            f"Obveznik uzdržavanja obvezuje se plaćati mjesečni iznos uzdržavanja "
            f"u iznosu od <b>{format_eur(iznos_mjesecno)}</b>.<br><br>"
            f"Navedeni iznos uzdržavanja može se uskladiti jednom godišnje sukladno "
            f"promjenama troškova života ili promijenjenim okolnostima, sporazumom stranaka "
            f"ili odlukom suda."
            f"</div>"
        )
        brojac_clanka += 1

        # Clanak 3: Datum dospijeca i IBAN
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {brojac_clanka}.</div>"
        )
        parts.append(
            f"<div class='justified'>"
            f"Mjesečni iznos uzdržavanja dospijeva svakog <b>{format_text(datum_dospijeca)}.</b> "
            f"u mjesecu za tekući mjesec.<br><br>"
        )
        if iban:
            parts.append(
                f"Uplata se vrši na račun Primatelja uzdržavanja:<br>"
                f"<b>IBAN: {format_text(iban)}</b><br><br>"
            )
        parts.append(
            f"Obveza uzdržavanja teče od dana sklapanja ovog Ugovora i traje do prestanka "
            f"zakonske obveze uzdržavanja."
            f"</div>"
        )
        brojac_clanka += 1

        # Clanak 4: Clausula exequendi (ako je primjenjivo)
        if clausula_exequendi:
            parts.append(
                f"<div class='section-title' style='text-align: center;'>Članak {brojac_clanka}.</div>"
            )
            parts.append(
                f"<div class='justified clausula'>"
                f"<b>KLAUZULA OVRŠNOSTI (clausula exequendi)</b><br><br>"
                f"Obveznik uzdržavanja daje izričitu suglasnost da se, u slučaju "
                f"zakašnjenja s plaćanjem bilo kojeg mjesečnog obroka uzdržavanja, "
                f"na temelju ovog Ugovora, koji je solemniziran pred javnim bilježnikom, "
                f"može neposredno provesti prisilna ovrha na cjelokupnoj imovini "
                f"Obveznika uzdržavanja radi naplate dospjelih, a neplaćenih iznosa "
                f"uzdržavanja, bez prethodnog vođenja parničnog postupka.<br><br>"
                f"Ovaj Ugovor, nakon solemnizacije, ima snagu ovršne isprave "
                f"sukladno članku 310. Obiteljskog zakona i članku 54. Zakona o javnom "
                f"bilježništvu."
                f"</div>"
            )
            brojac_clanka += 1

        # Zavrsni clanak
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {brojac_clanka}.</div>"
        )
        parts.append(
            f"<div class='justified'>"
            f"Ovaj Ugovor sastavljen je u četiri (4) istovjetna primjerka, od kojih svaka "
            f"strana zadržava po jedan, a dva se primjerka zadržavaju u spisu javnog bilježnika.<br><br>"
            f"Ugovorne strane potvrđuju da su ovaj Ugovor pročitale, razumjele njegov sadržaj "
            f"i pravne učinke, te da ga potpisuju kao izraz svoje slobodne i ozbiljne volje."
            f"</div>"
        )

        # JB ovjera
        parts.append(
            f"<br><div style='border: 1px dashed #333; padding: 15px; margin: 20px 0;'>"
            f"<b>JAVNOBILJEŽNIČKA SOLEMNIZACIJA</b><br><br>"
            f"Javni bilježnik: ________________________________________<br>"
            f"Sjedište: ________________________________________<br>"
            f"Poslovni broj: ________________________________________<br><br>"
            f"Potvrđujem da sam stranke upozorio/la na pravne posljedice ovog Ugovora, "
            f"uključujući ovršnost, te da su stranke vlastoručno potpisale ovaj Ugovor "
            f"nakon čitanja i objašnjenja.<br><br>"
            f"<div style='text-align: right;'>Javni bilježnik<br><br><br>"
            f"______________________<br>(pečat i potpis)</div>"
            f"</div>"
        )

        # Upozorenje
        parts.append(
            f"<br><div style='border: 1px solid #cc0000; padding: 10px; margin: 15px 0; "
            f"background-color: #fff5f5;'>"
            f"<b>UPOZORENJE:</b> Sukladno Obiteljskom zakonu, uzdržavanje maloljetnog "
            f"djeteta mora biti primjereno potrebama djeteta i mogućnostima obveznika. "
            f"Sud može promijeniti ugovoreni iznos ako utvrdi da nije u interesu djeteta. "
            f"Minimalni iznos uzdržavanja određuje se prema tablici Ministarstva socijalne "
            f"politike i mladih."
            f"</div>"
        )

        parts.append(f"<br><div class='justified'>U {format_text(mjesto)}, dana {datum}</div>")

        parts.append(f"""
        <div class='signature-row'>
            <div class='signature-block'>
                <b>OBVEZNIK UZDRŽAVANJA</b>
                <br>(vlastoručni potpis pred javnim bilježnikom)
                <br><br><br>
                ______________________
            </div>
            <div class='signature-block'>
                <b>PRIMATELJ UZDRŽAVANJA</b>
                <br>(vlastoručni potpis pred javnim bilježnikom)
                <br><br><br>
                ______________________
            </div>
        </div>
        """)

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
