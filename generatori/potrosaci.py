# -----------------------------------------------------------------------------
# GENERATORI: Zastita potrosaca
# Pravni temelj: Zakon o zastiti potrosaca, ZOO, EU Direktiva 2011/83/EU
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur, format_eur_s_rijecima


def generiraj_reklamaciju(potrosac, podaci):
    """
    Pisani prigovor / Reklamacija trgovcu.
    Pravni temelj: Zakon o zaštiti potrošača (NN 19/22), ZOO čl. 400-422.
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        trgovac_naziv = format_text(podaci.get("trgovac_naziv", ""))
        trgovac_adresa = format_text(podaci.get("trgovac_adresa", ""))
        datum_kupnje = podaci.get("datum_kupnje", "________")
        broj_racuna = format_text(podaci.get("broj_racuna", ""))
        opis_proizvoda = format_text(podaci.get("opis_proizvoda", ""))
        opis_nedostatka = format_text(podaci.get("opis_nedostatka", ""))
        zahtjev = podaci.get("zahtjev", "popravak")
        cijena = podaci.get("cijena", 0)

        zahtjev_tekst = {
            "popravak": (
                "Sukladno članku 410. Zakona o obveznim odnosima, zahtijevam <b>popravak proizvoda</b> "
                "u razumnom roku, bez naknade, te bez znatnih neugodnosti za potrošača."
            ),
            "zamjena": (
                "Sukladno članku 410. Zakona o obveznim odnosima, zahtijevam <b>zamjenu proizvoda</b> "
                "novim ispravnim proizvodom iste vrste i svojstava, bez naknade."
            ),
            "povrat_novca": (
                "Sukladno člancima 410. i 412. Zakona o obveznim odnosima, zahtijevam "
                "<b>raskid ugovora i povrat kupovnine</b> u iznosu od "
                f"<b>{format_eur_s_rijecima(cijena)}</b>, obzirom da popravak ili zamjena nisu mogući "
                "odnosno predstavljaju nerazmjerno opterećenje."
            ),
            "snizenje_cijene": (
                "Sukladno članku 412. Zakona o obveznim odnosima, zahtijevam "
                "<b>razmjerno sniženje cijene</b> s obzirom na utvrđeni nedostatak proizvoda."
            ),
        }

        parts = [
            f"<div style='text-align: right; font-size: 10pt;'>{mjesto}, {danas}</div><br>",
            # Primatelj - trgovac
            f"<div class='party-info' style='text-align: left;'>"
            f"<b>{trgovac_naziv}</b><br>"
            f"{trgovac_adresa}</div><br>",
            # Pošiljatelj - potrošač
            f"<div class='party-info' style='text-align: right;'>"
            f"<b>Potrošač:</b><br>{potrosac}</div><br>",
            # Naslov
            "<div class='header-doc'>PISANI PRIGOVOR / REKLAMACIJA</div>",
            "<div class='justified' style='text-align: center; font-style: italic; margin-bottom: 15px;'>"
            "na temelju Zakona o zaštiti potrošača i Zakona o obveznim odnosima</div><br>",
        ]

        # I. PODACI O KUPNJI
        parts.append(
            "<div class='section-title'>I. PODACI O KUPNJI</div>"
            "<div class='justified'>"
            f"Datum kupnje: <b>{datum_kupnje}</b><br>"
            f"Broj fiskalnog računa: <b>{broj_racuna}</b><br>"
            f"Opis proizvoda/usluge: <b>{opis_proizvoda}</b><br>"
            f"Plaćena cijena: <b>{format_eur_s_rijecima(cijena)}</b>"
            "</div><br>"
        )

        # II. OPIS NEDOSTATKA
        parts.append(
            "<div class='section-title'>II. OPIS NEDOSTATKA</div>"
            "<div class='justified'>"
            "Kupljeni proizvod ima <b>materijalni nedostatak stvari</b> u smislu članka 400. "
            "Zakona o obveznim odnosima, koji se očituje u sljedećem:<br><br>"
            f"{opis_nedostatka}<br><br>"
            "Navedeni nedostatak postojao je u trenutku prijelaza rizika na potrošača, odnosno se "
            "pojavio unutar zakonskog roka u kojem se presumira da je nedostatak postojao "
            "od ranije (članak 404. ZOO).</div><br>"
        )

        # III. ZAHTJEV POTROŠAČA
        parts.append(
            "<div class='section-title'>III. ZAHTJEV POTROŠAČA</div>"
            f"<div class='justified'>{zahtjev_tekst.get(zahtjev, zahtjev_tekst['popravak'])}</div><br>"
        )

        # Napomene
        parts.append(
            "<div class='justified' style='border: 1px solid #666; padding: 10px; margin: 15px 0;'>"
            "<b>NAPOMENA:</b><br>"
            "Sukladno članku 10. stavak 3. Zakona o zaštiti potrošača (NN 19/22), trgovac je "
            "<b>dužan odgovoriti na pisani prigovor u roku od 15 dana</b> od dana zaprimanja. "
            "Ukoliko u navedenom roku ne zaprimim odgovor, zadržavam pravo obratiti se "
            "Državnom inspektoratu, nadležnom sudu ili tijelu za alternativno rješavanje sporova.<br><br>"
            "Preporučuje se slanje preporučenom poštom s povratnicom kao dokaz o predaji prigovora.</div><br>"
        )

        # Prilog
        parts.append(
            "<div class='justified'><b>Prilog:</b><br>"
            "- Kopija fiskalnog računa br. " + broj_racuna + "</div><br><br>"
        )

        # Potpis
        parts.append(
            '<table width="100%" border="0"><tr>'
            '<td width="50%" align="left"></td>'
            '<td width="50%" align="center"><b>POTROŠAČ</b><br><br><br>'
            "______________________<br>"
            "<small>(vlastoručni potpis)</small></td>"
            "</tr></table>"
        )

        return "".join(parts)

    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_jednostrani_raskid(potrosac, podaci):
    """
    Jednostrani raskid ugovora sklopljenog na daljinu.
    Pravni temelj: Zakon o zaštiti potrošača (NN 19/22) čl. 72-85,
    EU Direktiva 2011/83/EU o pravima potrošača.
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        trgovac_naziv = format_text(podaci.get("trgovac_naziv", ""))
        trgovac_adresa = format_text(podaci.get("trgovac_adresa", ""))
        datum_narudzbe = podaci.get("datum_narudzbe", "________")
        datum_isporuke = podaci.get("datum_isporuke", "________")
        opis_proizvoda = format_text(podaci.get("opis_proizvoda", ""))
        broj_narudzbe = format_text(podaci.get("broj_narudzbe", ""))

        parts = [
            f"<div style='text-align: right; font-size: 10pt;'>{mjesto}, {danas}</div><br>",
            # Naslov
            "<div class='header-doc'>OBAVIJEST O JEDNOSTRANOM RASKIDU UGOVORA</div>",
            "<div class='justified' style='text-align: center; font-style: italic; margin-bottom: 15px;'>"
            "Standardni informacijski obrazac za jednostrani raskid ugovora<br>"
            "(Zakon o zaštiti potrošača, čl. 79.)</div><br>",
        ]

        # Primatelj
        parts.append(
            "<div class='justified'>"
            f"<b>Primatelj:</b><br>"
            f"{trgovac_naziv}<br>"
            f"{trgovac_adresa}</div><br>"
        )

        # Izjava o raskidu
        parts.append(
            "<div class='justified'>"
            "Ovime Vas obavješćujem da želim raskinuti ugovor o kupnji sljedećeg proizvoda/usluge:"
            "</div><br>"
        )

        # Podaci o proizvodu
        parts.append(
            "<div class='justified' style='border-left: 3px solid #333; padding-left: 15px;'>"
            f"Opis proizvoda/usluge: <b>{opis_proizvoda}</b><br>"
            f"Broj narudžbe: <b>{broj_narudzbe}</b><br>"
            f"Datum narudžbe: <b>{datum_narudzbe}</b><br>"
            f"Datum primitka robe: <b>{datum_isporuke}</b>"
            "</div><br>"
        )

        # Podaci o potrošaču
        parts.append(
            "<div class='justified'>"
            f"<b>Ime i adresa potrošača:</b><br>"
            f"{potrosac}</div><br>"
        )

        # Datum i potpis
        parts.append(
            f"<div class='justified'>Datum: {danas}</div><br>"
        )

        # Pravna osnova i napomene
        parts.append(
            "<div class='section-title'>PRAVNA POUKA</div>"
            "<div class='justified'>"
            "Na temelju članka 72. Zakona o zaštiti potrošača (NN 19/22), potrošač ima pravo "
            "na <b>jednostrani raskid ugovora sklopljenog izvan poslovnih prostorija ili na daljinu "
            "u roku od 14 dana</b> od dana primitka robe, bez obveze navođenja razloga.<br><br>"
            "<b>Obveze trgovca:</b> Trgovac je dužan bez odgađanja, a najkasnije u roku od "
            "<b>14 dana od dana primitka ove obavijesti</b>, vratiti potrošaču sve uplaćene iznose, "
            "uključujući troškove isporuke (članak 77. ZZP).<br><br>"
            "<b>Obveze potrošača:</b> Potrošač je dužan robu vratiti trgovcu bez odgađanja, a "
            "najkasnije u roku od <b>14 dana</b> od slanja ove obavijesti. Troškove povrata robe "
            "snosi potrošač, osim ako se trgovac obvezao snositi te troškove ili ako nije prethodno "
            "obavijestio potrošača o obvezi snošenja troškova povrata.</div><br>"
        )

        # Upozorenje o produljenom roku
        parts.append(
            "<div class='justified' style='border: 1px solid #666; padding: 10px; margin: 15px 0;'>"
            "<b>VAŽNO:</b> Ako trgovac nije potrošača obavijestio o pravu na jednostrani raskid "
            "ugovora sukladno članku 63. stavak 1. točka 7. ZZP-a, pravo na raskid <b>produljuje se "
            "na 12 mjeseci i 14 dana</b> od isteka izvornog roka za raskid (članak 74. ZZP).</div><br>"
        )

        # Potpis
        parts.append(
            '<table width="100%" border="0"><tr>'
            '<td width="50%" align="left"></td>'
            '<td width="50%" align="center"><b>POTROŠAČ</b><br><br><br>'
            "______________________<br>"
            "<small>(vlastoručni potpis)</small></td>"
            "</tr></table>"
        )

        return "".join(parts)

    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_prijavu_inspekciji(podnositelj, podaci):
    """
    Prijava građana Državnom inspektoratu protiv gospodarskog subjekta.
    Pravni temelj: Zakon o Državnom inspektoratu (NN 115/18, 117/21),
    Zakon o zaštiti potrošača (NN 19/22).
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        trgovac_naziv = format_text(podaci.get("trgovac_naziv", ""))
        trgovac_adresa = format_text(podaci.get("trgovac_adresa", ""))
        trgovac_oib = format_text(podaci.get("trgovac_oib", ""))
        opis_krsenja = format_text(podaci.get("opis_krsenja", ""))
        datum_krsenja = podaci.get("datum_krsenja", "________")
        prethodni_prigovor = podaci.get("prethodni_prigovor", False)
        datum_prigovora = podaci.get("datum_prigovora", "________")
        odgovor_trgovca = format_text(podaci.get("odgovor_trgovca", "bez odgovora"))
        prilozi = podaci.get("prilozi", [])

        parts = [
            f"<div style='text-align: right; font-size: 10pt;'>{mjesto}, {danas}</div><br>",
            # Naslov
            "<div class='header-doc'>PRIJAVA GRAĐANA PROTIV GOSPODARSKOG SUBJEKTA</div>",
        ]

        # Primatelj - Inspektorat
        parts.append(
            "<div class='party-info' style='text-align: left;'>"
            "<b>DRŽAVNI INSPEKTORAT REPUBLIKE HRVATSKE</b><br>"
            "Sektor za nadzor tržišta<br>"
            "Šubićeva 29<br>"
            "10000 Zagreb</div><br>"
        )

        # I. PODACI O PODNOSITELJU
        parts.append(
            "<div class='section-title'>I. PODACI O PODNOSITELJU PRIJAVE</div>"
            f"<div class='party-info'>{podnositelj}</div><br>"
        )

        # II. PODACI O PRIJAVLJENOM SUBJEKTU
        parts.append(
            "<div class='section-title'>II. PODACI O PRIJAVLJENOM SUBJEKTU</div>"
            "<div class='justified'>"
            f"Naziv / ime: <b>{trgovac_naziv}</b><br>"
            f"Adresa sjedišta / poslovnice: <b>{trgovac_adresa}</b><br>"
            f"OIB: <b>{trgovac_oib}</b>"
            "</div><br>"
        )

        # III. OPIS KRŠENJA
        parts.append(
            "<div class='section-title'>III. OPIS KRŠENJA</div>"
            "<div class='justified'>"
            f"Dana <b>{datum_krsenja}</b> prijavljeni subjekt je postupio protivno odredbama "
            "propisa o zaštiti potrošača, na sljedeći način:<br><br>"
            f"{opis_krsenja}</div><br>"
        )

        # IV. PRETHODNO PODNESENI PRIGOVOR
        parts.append(
            "<div class='section-title'>IV. PRETHODNO PODNESENI PRIGOVOR TRGOVCU</div>"
        )

        if prethodni_prigovor:
            parts.append(
                "<div class='justified'>"
                f"Podnositelj je dana <b>{datum_prigovora}</b> uputio pisani prigovor "
                "trgovcu sukladno članku 10. Zakona o zaštiti potrošača.<br><br>"
                f"<b>Odgovor trgovca:</b> {odgovor_trgovca}</div><br>"
            )
        else:
            parts.append(
                "<div class='justified' style='border: 2px solid #cc0000; padding: 10px; "
                "margin: 10px 0; background-color: #fff5f5;'>"
                "<b>⚠ UPOZORENJE:</b> Podnositelj <b>nije prethodno uputio pisani prigovor</b> "
                "trgovcu. Sukladno članku 10. Zakona o zaštiti potrošača, potrošač je dužan "
                "najprije podnijeti pisani prigovor trgovcu te sačekati rok od 15 dana za odgovor. "
                "Državni inspektorat može zahtijevati dokaz o prethodno podnesenom prigovoru kao "
                "preduvjet za postupanje.</div><br>"
            )

        # V. PRILOZI
        parts.append(
            "<div class='section-title'>V. PRILOZI</div>"
        )
        if prilozi:
            parts.append("<div class='justified'><ol>")
            for prilog in prilozi:
                parts.append(f"<li>{format_text(prilog)}</li>")
            parts.append("</ol></div><br>")
        else:
            parts.append(
                "<div class='justified'>Bez priloga.</div><br>"
            )

        # Napomena
        parts.append(
            "<div class='justified' style='border: 1px solid #666; padding: 10px; margin: 15px 0;'>"
            "<b>NAPOMENA:</b> Državni inspektorat provodi inspekcijski nadzor i donosi "
            "<b>upravno rješenje</b> kojim može izreći prekršajne kazne, zabraniti obavljanje djelatnosti "
            "ili naložiti otklanjanje nepravilnosti. Inspektorat ne vodi kazneni progon niti "
            "odlučuje o imovinskopravnim zahtjevima potrošača. Za naknadu štete potrošač se "
            "upućuje na nadležni sud ili tijelo za alternativno rješavanje potrošačkih sporova.</div><br>"
        )

        # Potpis
        parts.append(
            '<table width="100%" border="0"><tr>'
            '<td width="50%" align="left"></td>'
            '<td width="50%" align="center"><b>PODNOSITELJ PRIJAVE</b><br><br><br>'
            "______________________<br>"
            "<small>(vlastoručni potpis)</small></td>"
            "</tr></table>"
        )

        return "".join(parts)

    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_prigovor_racunu(potrosac, podaci):
    """Prigovor na iznos racuna davatelju usluga.
    Sektori i pravni temelji:
      - telekom: Zakon o elektronickim komunikacijama (NN 76/22), HAKOM Pravilnik
      - energetika: Zakon o energiji, opci uvjeti opskrbe HEP/RWE
      - voda/komunalije: Zakon o vodama, opci uvjeti komunalnih usluga
    Pravo na prigovor opcenito: ZZP cl. 10 (pravo na pisani prigovor),
    ZOO cl. 295-296 (osporavanje obveze)."""
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        sektor = podaci.get('sektor', 'telekom')
        davatelj = format_text(podaci.get('davatelj', ''))
        davatelj_adresa = format_text(podaci.get('davatelj_adresa', ''))
        broj_racuna = format_text(podaci.get('broj_racuna', ''))
        datum_racuna = format_text(podaci.get('datum_racuna', ''))
        razdoblje = format_text(podaci.get('razdoblje', ''))
        sporni_iznos = podaci.get('sporni_iznos_eur', 0)
        sporni_str = format_eur(sporni_iznos) if sporni_iznos else ''
        ukupno_racun = podaci.get('ukupno_racun_eur', 0)
        ukupno_str = format_eur(ukupno_racun) if ukupno_racun else ''
        razlog = format_text(podaci.get('razlog_prigovora', ''))
        broj_korisnika = format_text(podaci.get('broj_korisnika', ''))  # broj ugovora / korisnicki broj
        zahtjev_storno = podaci.get('zahtjev_storno', True)
        mjesto = podaci.get('mjesto', 'Zagreb')

        sektor_konfig = {
            'telekom': {
                'naslov': "PRIGOVOR NA IZNOS RAČUNA — TELEKOMUNIKACIJSKE USLUGE",
                'temelj': (
                    "Zakon o elektroničkim komunikacijama (NN 76/22), "
                    "Pravilnik o načinu i uvjetima obavljanja djelatnosti elektroničkih komunikacijskih mreža (HAKOM), "
                    "Opći uvjeti poslovanja {davatelj}"
                ),
                'rok': "u roku od 30 dana od primitka računa (ZEK)",
                'tijelo_drugi_stupanj': "Hrvatska regulatorna agencija za mrežne djelatnosti — HAKOM",
                'oznaka_korisnika': "Korisnički broj / broj ugovora",
            },
            'energetika': {
                'naslov': "PRIGOVOR NA IZNOS RAČUNA — ENERGETSKA USLUGA",
                'temelj': (
                    "Zakon o tržištu električne energije (NN 111/21) / Zakon o tržištu plina, "
                    "Opći uvjeti opskrbe {davatelj}, ZOO čl. 295-296"
                ),
                'rok': "u roku od 15 dana od primitka računa (Opći uvjeti opskrbe)",
                'tijelo_drugi_stupanj': "Hrvatska energetska regulatorna agencija — HERA",
                'oznaka_korisnika': "Šifra obračunskog mjernog mjesta (OMM) / broj ugovora",
            },
            'voda': {
                'naslov': "PRIGOVOR NA IZNOS RAČUNA — KOMUNALNE / VODNE USLUGE",
                'temelj': (
                    "Zakon o vodnim uslugama (NN 66/19), "
                    "Opći uvjeti isporuke vodnih usluga {davatelj}, "
                    "Zakon o komunalnom gospodarstvu (NN 68/18), ZOO čl. 295-296"
                ),
                'rok': "u roku od 15 dana od primitka računa",
                'tijelo_drugi_stupanj': "Vijeće za vodne usluge",
                'oznaka_korisnika': "Šifra korisnika / broj ugovora o opskrbi",
            },
        }
        cfg = sektor_konfig.get(sektor, sektor_konfig['telekom'])

        adresa_html = (
            f"<b>{davatelj}</b><br>{davatelj_adresa}"
            if davatelj_adresa else f"<b>{davatelj}</b>"
        )

        racun_info = []
        racun_info.append(f"<b>Broj računa:</b> {broj_racuna}")
        if datum_racuna:
            racun_info.append(f"<b>Datum izdavanja računa:</b> {datum_racuna}")
        if razdoblje:
            racun_info.append(f"<b>Obračunsko razdoblje:</b> {razdoblje}")
        if ukupno_str:
            racun_info.append(f"<b>Ukupan iznos računa:</b> {ukupno_str}")
        if sporni_str:
            racun_info.append(f"<b>Sporni iznos:</b> {sporni_str}")
        if broj_korisnika:
            racun_info.append(f"<b>{cfg['oznaka_korisnika']}:</b> {broj_korisnika}")
        racun_html = "<br>".join(racun_info)

        zahtjev_html = ""
        if zahtjev_storno and sporni_str:
            zahtjev_html = (
                f"<div class='doc-body'><b>ZAHTJEV:</b><br>"
                f"Tražim da se sporni iznos od <b>{sporni_str}</b> stornira (poništi) i izda ispravljeni račun. "
                f"Sve do okončanja postupka po ovom Prigovoru, smatram da nemam obvezu plaćanja spornog dijela "
                f"računa, sukladno {cfg['rok']}. Tražim također obustavu daljnjih postupaka naplate, "
                f"opomena i obustave usluge u dijelu koji se odnosi na sporni iznos.</div>"
            )
        elif zahtjev_storno:
            zahtjev_html = (
                f"<div class='doc-body'><b>ZAHTJEV:</b><br>"
                f"Tražim da se račun preispita i da se sporni dio stornira (poništi) ili izda ispravljeni račun. "
                f"Tražim također obustavu daljnjih postupaka naplate dok se prigovor riješi.</div>"
            )

        return (
            f"<div style='font-weight:bold;font-size:14px;'>{adresa_html}</div><br><br>"
            f"<div class='party-info'><b>PODNOSITELJ PRIGOVORA (potrošač):</b><br>{potrosac}</div><br>"
            f"<div class='header-doc'>{cfg['naslov']}</div>"
            f"<div class='doc-body'>"
            f"Na temelju {cfg['temelj'].format(davatelj=davatelj)}, te "
            f"članka 10. Zakona o zaštiti potrošača (pravo na pisani prigovor), "
            f"podnosim pisani prigovor na iznos sljedećeg računa:</div>"
            f"<div class='section-title'>I. PODACI O RAČUNU</div>"
            f"<div class='doc-body'>{racun_html}</div>"
            f"<div class='section-title'>II. RAZLOG PRIGOVORA</div>"
            f"<div class='doc-body'>{razlog}</div>"
            f"<div class='section-title'>III. ZAHTJEV</div>"
            f"{zahtjev_html}"
            f"<div class='section-title'>IV. ROK ZA ODGOVOR</div>"
            f"<div class='doc-body'>Tražim da na ovaj Prigovor odgovorite u pisanom obliku u roku od "
            f"<b>15 (petnaest) dana</b> od primitka, sukladno čl. 10. ZZP. Ako u navedenom roku "
            f"ne dobijem zadovoljavajući odgovor, podnijet ću prigovor nadležnom regulatornom tijelu "
            f"(<b>{cfg['tijelo_drugi_stupanj']}</b>) i, prema potrebi, pokrenuti sudski postupak za "
            f"utvrđenje neosnovanosti spornog iznosa.</div>"
            f"<div class='section-title'>V. PRILOZI</div>"
            f"<div class='doc-body'><ol>"
            f"<li>Preslika spornog računa</li>"
            f"<li>Dokaz o (eventualnom) prethodnom usmenom prigovoru</li>"
            f"<li>Dokumentacija na temelju koje se osporava iznos (mjerni podaci, prethodni računi i sl.)</li>"
            f"</ol></div>"
            f"<br>"
            f"<div class='justified'>U {mjesto}, dana {danas}.</div><br>"
            f"<table width='100%'><tr>"
            f"<td width='40%'></td>"
            f"<td width='60%' align='center'><b>PODNOSITELJ PRIGOVORA</b><br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
