# -----------------------------------------------------------------------------
# GENERATORI: Ugovori (prilagodeni, standardni, radno pravo)
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, formatiraj_troskovnik, format_eur, _rimski_broj, u_lokativu, _padez_ime


def generiraj_prilagodeni_ugovor(naslov, mjesto, datum, rok_vazenja, s1, s2, urbroj, struktura):
    """
    Generira ugovor na temelju dinamicke strukture koju je korisnik slozio.
    """
    try:
        datum_str = datum.strftime("%d.%m.%Y.") if datum else date.today().strftime("%d.%m.%Y.")
        rok_str = (
            f"<br>Ugovor vrijedi do: <b>{rok_vazenja.strftime('%d.%m.%Y.')}</b>"
            if rok_vazenja
            else "<br>Ugovor se sklapa na neodređeno vrijeme."
        )
        urbroj_str = (
            f"<div style='text-align: right; font-size: 10pt;'>UrBroj: {urbroj}</div><br>"
            if urbroj
            else ""
        )

        parts = [
            f"{urbroj_str}",
            f"<div class='header-doc'>{naslov.upper()}</div>",
            f"<div class='justified'>",
            f"Sklopljen u mjestu <b>{mjesto}</b>, dana {datum_str} godine.",
            f"<br><br>",
            f"<b>IZMEĐU:</b>",
            f"<br><br>",
            f"1. <b>{s1['uloga']}:</b><br>",
            f"{s1['tekst']}",
            f"<br><br>",
            f"2. <b>{s2['uloga']}:</b><br>",
            f"{s2['tekst']}",
            f"<br><br>",
            f"{rok_str}",
            f"</div>",
            f"<br>",
        ]

        brojac_clanka = 1

        for i, dio in enumerate(struktura):
            oznaka_dijela = _rimski_broj(i + 1)

            if dio.get('naslov'):
                parts.append(
                    f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px; margin-bottom: 10px;'>"
                    f"{oznaka_dijela}. {dio['naslov'].upper()}</div>"
                )

            clanci = dio.get('clanci') or []
            for tekst_clanka in clanci:
                if tekst_clanka and tekst_clanka.strip():
                    parts.append(
                        f"<div class='section-title' style='text-align: center;'>Članak {brojac_clanka}.</div>"
                    )
                    parts.append(f"<div class='justified'>{format_text(tekst_clanka)}</div>")
                    brojac_clanka += 1

        parts.append(f"""
        <div class='signature-row'>
            <div class='signature-block'>
                <b>{s1['uloga'].upper()}</b>
                <br><br><br>
                ______________________
            </div>
            <div class='signature-block'>
                <b>{s2['uloga'].upper()}</b>
                <br><br><br>
                ______________________
            </div>
        </div>
        """)

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_ugovor_standard(tip_ugovora, stranka1, stranka2, podaci, opcije, troskovi_dict=None):
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        dodatni_tekst = (
            f"<br><b>Kapara:</b> Ugovorne strane potvrđuju da je Kupac isplatio kaparu u iznosu od {opcije['iznos_kapare']} EUR."
            if opcije.get('kapara')
            else ""
        )
        solemnizacija_clanak = (
            """<div class='section-title'>Članak (Solemnizacija)</div>"""
            """<div class='doc-body'>Ugovorne strane suglasne su da se ovaj Ugovor solemnizira (potvrdi) kod Javnog bilježnika.</div>"""
            if opcije.get('solemnizacija')
            else ""
        )
        titles = {
            "Kupoprodaja": ("UGOVOR O KUPOPRODAJI", "PRODAVATELJ", "KUPAC"),
            "Najam/Zakup": ("UGOVOR O NAJMU", "NAJMODAVAC", "NAJMOPRIMAC"),
            "Ugovor o djelu (Usluga)": ("UGOVOR O DJELU", "NARUČITELJ", "IZVOĐAČ"),
            "Zajam": ("UGOVOR O ZAJMU", "ZAJMODAVAC", "ZAJMOPRIMAC"),
        }
        naslov, u1, u2 = titles[tip_ugovora]
        trosak_prikaz = formatiraj_troskovnik(troskovi_dict) if troskovi_dict else ""
        return (
            f"<div class='header-doc'>{naslov}</div>"
            f"<div class='doc-body'>Sklopljen u {u_lokativu(podaci['mjesto'])}, dana {datum}, između:</div>"
            f"<div class='party-info'>1. <b>{u1}:</b><br>{stranka1}<br><br>2. <b>{u2}:</b><br>{stranka2}</div>"
            f"<div class='section-title'>Članak 1.</div>"
            f"<div class='doc-body'>{format_text(podaci['predmet_clanak'])}</div>"
            f"<div class='section-title'>Članak 2.</div>"
            f"<div class='doc-body'>{format_text(podaci['cijena_clanak'])}{dodatni_tekst}</div>"
            f"<div class='section-title'>Članak 3.</div>"
            f"<div class='doc-body'>{format_text(podaci['rok_clanak'])}</div>"
            f"{solemnizacija_clanak}<br><br>{trosak_prikaz}<br>"
            f'<table width="100%"><tr>'
            f'<td width="50%" align="center"><b>{u1}</b><br><br>__________</td>'
            f'<td width="50%" align="center"><b>{u2}</b><br><br>__________</td>'
            f'</tr></table>'
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_ugovor_o_radu(poslodavac, radnik, podaci):
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        vrsta_tekst = "NA NEODREĐENO VRIJEME"
        clanak_trajanje = "Ugovor se sklapa na neodređeno vrijeme."
        if podaci.get('vrsta') == "Određeno":
            vrsta_tekst = "NA ODREĐENO VRIJEME"
            clanak_trajanje = (
                f"Ugovor se sklapa na određeno vrijeme do {podaci.get('datum_do', '_______')}, "
                f"zbog: {podaci.get('razlog_odredeno', 'povećanog opsega posla')}."
            )
        probni_rad_txt = (
            f"Ugovara se probni rad u trajanju od {podaci.get('probni_rad_mj', 3)} mjeseca/mjeseci."
            if podaci.get('probni_rad')
            else ""
        )
        return f"""
        <div class='header-doc'>UGOVOR O RADU<br><span style='font-size: 12pt; font-weight: normal;'>{vrsta_tekst}</span></div>
        <div class='justified'>Sklopljen u {u_lokativu(podaci.get('mjesto_sklapanja', 'Zagreb'))}, dana {datum} godine, između:<br><br>1. <b>POSLODAVAC:</b><br>{poslodavac}<br><br>2. <b>RADNIK:</b><br>{radnik}</div>
        <div class='section-title'>Članak 1. (Predmet i početak rada)</div><div class='justified'>Radnik počinje s radom dana <b>{podaci.get('datum_start', '_______')}</b>. {clanak_trajanje} {probni_rad_txt}</div>
        <div class='section-title'>Članak 2. (Mjesto i opis poslova)</div><div class='justified'>Radnik će obavljati poslove na radnom mjestu: <b>{podaci.get('naziv_radnog_mjesta', '_______')}</b>.<br><b>Opis poslova:</b> {podaci.get('opis_posla', 'Opisani u opisu radnog mjesta kod Poslodavca')}.<br>Mjesto rada je: {podaci.get('mjesto_rada', 'u sjedištu Poslodavca i na terenu po potrebi')}.</div>
        <div class='section-title'>Članak 3. (Radno vrijeme i odmori)</div><div class='justified'>Radnik će raditi u punom radnom vremenu od {podaci.get('radno_vrijeme', 40)} sati tjedno. Radnik ima pravo na dnevni odmor (stanku) u trajanju od 30 minuta.</div>
        <div class='section-title'>Članak 4. (Plaća i naknade)</div><div class='justified'>Za obavljeni rad Poslodavac će Radniku isplaćivati osnovnu bruto plaću u iznosu od <b>{format_eur_s_rijecima(podaci.get('bruto_placa', 0))}</b> mjesečno.</div>
        <div class='section-title'>Članak 5. (Godišnji odmor)</div><div class='justified'>Radnik ima pravo na plaćeni godišnji odmor u trajanju od najmanje {podaci.get('godisnji_odmor', 20)} radnih dana.</div>
        <div class='section-title'>Članak 6. (Završne odredbe)</div><div class='justified'>Ovaj Ugovor sastavljen je u 3 (tri) istovjetna primjerka.</div>
        <div class='signature-row'><div class='signature-block'><b>ZA POSLODAVCA</b><br><br><br>______________________</div><div class='signature-block'><b>RADNIK</b><br><br><br>______________________</div></div>
        """
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_otkaz(poslodavac, radnik, podaci):
    try:
        return (
            f"<div class='header-doc'>ODLUKA O OTKAZU</div>"
            f"<div class='doc-body'>1. Otkazuje se ugovor radniku {radnik}.</div>"
            f"<div class='section-title'>Obrazloženje</div>"
            f"<div class='doc-body'>{podaci['tekst_obrazlozenja']}</div>"
            f'<br><br><table width="100%"><tr><td align="center">'
            f"<b>POSLODAVAC</b><br>__________</td></tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_aneks_ugovora_o_radu(poslodavac, radnik, podaci):
    """
    Generira aneks (dodatak) ugovora o radu.
    Pravni temelj: Zakon o radu čl. 12
    """
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        datum_osnovnog = podaci.get("datum_osnovnog_ugovora", "________")
        razlog = format_text(podaci.get("razlog", ""))
        promjene = podaci.get("promjene", [])
        datum_primjene = podaci.get("datum_primjene", datum)

        parts = [
            f"<div class='header-doc'>ANEKS UGOVORA O RADU<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>"
            f"(Dodatak Ugovoru o radu od {datum_osnovnog})</span></div>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {datum} godine, između:<br><br>"
            f"1. <b>POSLODAVAC:</b><br>{poslodavac}<br><br>"
            f"2. <b>RADNIK:</b><br>{radnik}</div><br>",
            f"<div class='section-title'>Članak 1. (Predmet aneksa)</div>"
            f"<div class='justified'>Na temelju članka 12. Zakona o radu (NN 93/14, 127/17, 98/19, 151/22, 64/23) "
            f"te suglasne volje ugovornih strana, ovim Aneksom mijenjaju se odredbe "
            f"Ugovora o radu sklopljenog dana {datum_osnovnog}.</div><br>",
        ]

        if razlog:
            parts.append(
                f"<div class='section-title'>Članak 2. (Razlog izmjene)</div>"
                f"<div class='justified'>{razlog}</div><br>"
            )

        clanak_br = 3 if razlog else 2
        parts.append(f"<div class='section-title'>Članak {clanak_br}. (Izmjene)</div>")
        parts.append("<div class='justified'>Ugovorne strane suglasno utvrđuju sljedeće izmjene:<br><br>")
        for idx, promjena in enumerate(promjene, 1):
            parts.append(f"<b>{idx}.</b> {format_text(promjena)}<br><br>")
        parts.append("</div>")
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Primjena)</div>"
            f"<div class='justified'>Ovaj Aneks stupa na snagu dana <b>{datum_primjene}</b>.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Ostale odredbe)</div>"
            f"<div class='justified'>Sve ostale odredbe Ugovora o radu od {datum_osnovnog} "
            f"koje nisu izmijenjene ovim Aneksom ostaju na snazi. "
            f"Ovaj Aneks sastavljen je u 3 (tri) istovjetna primjerka.</div><br>"
        )

        parts.append(
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>ZA POSLODAVCA</b><br><br><br>______________________</div>"
            f"<div class='signature-block'><b>RADNIK</b><br><br><br>______________________</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_upozorenje_radniku(poslodavac, radnik, podaci):
    """
    Generira upozorenje radniku prije otkaza zbog skrivljenog ponašanja.
    Pravni temelj: Zakon o radu čl. 119
    """
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        opis_povrede = format_text(podaci.get("opis_povrede", ""))
        datum_povrede = podaci.get("datum_povrede", "________")
        rok_ocitovanja = podaci.get("rok_ocitovanja", 8)

        return (
            f"<div style='text-align: right; font-size: 10pt;'>{mjesto}, {datum}</div><br>"
            f"<div class='party-info'><b>POSLODAVAC:</b><br>{poslodavac}</div>"
            f"<div class='party-info'><b>RADNIK:</b><br>{radnik}</div><br>"
            f"<div class='header-doc'>UPOZORENJE RADNIKU<br>"
            f"<span style='font-size: 11pt; font-weight: normal;'>prije otkazivanja uvjetovanog "
            f"skrivljenim ponašanjem radnika</span></div>"
            f"<div class='justified'>Na temelju članka 119. Zakona o radu (NN 93/14, 127/17, 98/19, 151/22, 64/23), "
            f"Poslodavac Vam ovime upućuje pisano upozorenje.</div><br>"
            f"<div class='section-title'>I. OPIS POVREDE OBVEZE IZ RADNOG ODNOSA</div>"
            f"<div class='justified'>Dana <b>{datum_povrede}</b> utvrđena je sljedeća povreda "
            f"obveze iz radnog odnosa:<br><br>{opis_povrede}</div><br>"
            f"<div class='section-title'>II. UPOZORENJE</div>"
            f"<div class='justified'>Upozoravamo Vas da ste navedenim postupanjem povrijedili "
            f"obveze iz radnog odnosa te da će Poslodavac, u slučaju nastavka ili ponavljanja "
            f"istovrsnog ili sličnog ponašanja, donijeti <b>odluku o otkazu ugovora o radu "
            f"uvjetovanog skrivljenim ponašanjem radnika</b>, sukladno članku 116. stavku 1. "
            f"točki 3. Zakona o radu.</div><br>"
            f"<div class='section-title'>III. PRAVO NA OČITOVANJE</div>"
            f"<div class='justified'>Sukladno članku 119. stavku 2. Zakona o radu, "
            f"imate pravo očitovati se o navedenim navodima u roku od <b>{rok_ocitovanja} dana</b> "
            f"od dana primitka ovog upozorenja.</div><br>"
            f"<div class='justified'>Vaše očitovanje možete dostaviti pisanim putem na adresu "
            f"Poslodavca.</div>"
            f"<br><br>"
            f'<table width="100%" border="0"><tr>'
            f'<td width="50%" align="left"></td>'
            f'<td width="50%" align="center"><b>ZA POSLODAVCA</b><br><br><br>______________________</td>'
            f"</tr></table><br>"
            f"<div class='justified' style='font-size: 10pt;'>"
            f"Dostaviti: Radniku osobno uz potpis primitka ili poštom s povratnicom.</div>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_ugovor_rad_na_daljinu(poslodavac, radnik, podaci):
    """
    Generira ugovor o radu na daljinu / izdvojenom mjestu rada.
    Pravni temelj: Zakon o radu čl. 17 i 17.a
    """
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto_sklapanja", "Zagreb")
        vrsta_rada = podaci.get("vrsta_rada", "na_daljinu")
        vrsta_tekst = "NA DALJINU" if vrsta_rada == "na_daljinu" else "NA IZDVOJENOM MJESTU RADA"

        parts = [
            f"<div class='header-doc'>UGOVOR O RADU NA DALJINU<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>{vrsta_tekst}</span></div>",
            f"<div class='justified' style='font-size: 10pt;'>"
            f"ZAHTIJEVANA FORMA: PISANA (ZoR čl. 17 i 17.a)</div><br>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {datum} godine, između:<br><br>"
            f"1. <b>POSLODAVAC:</b><br>{poslodavac}<br><br>"
            f"2. <b>RADNIK:</b><br>{radnik}</div><br>",
        ]

        clanak_br = 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Predmet i početak rada)</div>"
            f"<div class='justified'>Radnik počinje s radom dana <b>{podaci.get('datum_start', '_______')}</b> "
            f"na radnom mjestu: <b>{podaci.get('naziv_radnog_mjesta', '_______')}</b>.</div><br>"
        )
        clanak_br += 1

        if vrsta_rada == "na_daljinu":
            mjesto_rada_opis = (
                "Rad se obavlja na daljinu, odnosno na mjestu koje Radnik sam odabere, "
                "a koje nije prostor Poslodavca, sukladno članku 17.a Zakona o radu."
            )
        else:
            mjesto_rada_opis = (
                "Rad se obavlja na izdvojenom mjestu rada (izvan prostorija Poslodavca), "
                "sukladno članku 17. Zakona o radu."
            )
        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Mjesto rada)</div>"
            f"<div class='justified'>{mjesto_rada_opis}</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Opis poslova)</div>"
            f"<div class='justified'>Radnik će obavljati sljedeće poslove: "
            f"{podaci.get('opis_posla', 'Opisani u opisu radnog mjesta kod Poslodavca')}.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Sredstva rada i oprema)</div>"
            f"<div class='justified'>Poslodavac je dužan nabaviti, instalirati i održavati opremu "
            f"potrebnu za obavljanje rada na daljinu.<br><br>"
            f"<b>Oprema:</b> {podaci.get('oprema', 'prijenosno računalo, monitor, tipkovnica, miš')}.<br><br>"
            f"Oprema ostaje vlasništvo Poslodavca i Radnik ju je dužan vratiti po prestanku ugovora.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Naknada operativnih troškova)</div>"
            f"<div class='justified'>Poslodavac će Radniku mjesečno nadoknađivati troškove rada na daljinu "
            f"(režije, internetska veza, električna energija i sl.) u paušalnom iznosu od "
            f"<b>{format_eur_s_rijecima(podaci.get('naknada_troskova', 0))}</b>.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Radno vrijeme i pravo na isključenje)</div>"
            f"<div class='justified'>Radnik će raditi u punom radnom vremenu od "
            f"{podaci.get('radno_vrijeme', 40)} sati tjedno.<br><br>"
            f"Radnik ima pravo na isključenje od sredstava rada, sukladno članku 17.a Zakona o radu. "
            f"{podaci.get('pravo_na_iskljucenje', 'Izvan radnog vremena Radnik nije dužan biti dostupan putem elektroničkih sredstava komunikacije.')}</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Plaća)</div>"
            f"<div class='justified'>Za obavljeni rad Poslodavac će Radniku isplaćivati osnovnu bruto plaću "
            f"u iznosu od <b>{format_eur(podaci.get('bruto_placa', 0))}</b> mjesečno.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Godišnji odmor)</div>"
            f"<div class='justified'>Radnik ima pravo na plaćeni godišnji odmor u trajanju od najmanje "
            f"{podaci.get('godisnji_odmor', 20)} radnih dana.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Zaštita na radu)</div>"
            f"<div class='justified'>Poslodavac je odgovoran za sigurne uvjete rada Radnika i na izdvojenom "
            f"mjestu rada, odnosno pri radu na daljinu. Poslodavac je dužan Radnika poučiti o sigurnom radu "
            f"s opremom te o pravilnom uređenju radnog mjesta.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Jednakost uvjeta)</div>"
            f"<div class='justified'>Radnik koji radi na daljinu ostvaruje jednaka prava kao i radnik koji "
            f"radi u prostorima Poslodavca, sukladno Zakonu o radu. Zabranjena je svaka diskriminacija "
            f"Radnika zbog rada na daljinu.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Završne odredbe)</div>"
            f"<div class='justified'>Ovaj Ugovor sastavljen je u 3 (tri) istovjetna primjerka, od kojih "
            f"svaka ugovorna strana zadržava po jedan, a jedan primjerak se pohranjuje u personalnom "
            f"dosjeu Radnika.</div><br>"
        )

        parts.append(
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>ZA POSLODAVCA</b><br><br><br>______________________</div>"
            f"<div class='signature-block'><b>RADNIK</b><br><br><br>______________________</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_sporazumni_prestanak(poslodavac, radnik, podaci):
    """
    Generira sporazum o prestanku ugovora o radu.
    Pravni temelj: Zakon o radu čl. 113
    """
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        datum_osnovnog = podaci.get("datum_osnovnog_ugovora", "________")
        datum_prestanka = podaci.get("datum_prestanka", "________")
        go_neiskoristen = podaci.get("godisnji_odmor_neiskoristen", 0)
        naknada_go = podaci.get("naknada_go", False)
        otpremnina = podaci.get("otpremnina", 0)
        povrat_imovine = podaci.get("povrat_imovine", "")

        parts = [
            f"<div class='header-doc'>SPORAZUM O PRESTANKU UGOVORA O RADU</div>",
            f"<div class='justified' style='font-size: 10pt;'>"
            f"ZAHTIJEVANA FORMA: PISANA (ZoR čl. 113 – nevaljanost bez pisanog oblika)</div><br>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {datum} godine, između:<br><br>"
            f"1. <b>POSLODAVAC:</b><br>{poslodavac}<br><br>"
            f"2. <b>RADNIK:</b><br>{radnik}</div><br>",
        ]

        clanak_br = 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Poziv na ugovor o radu)</div>"
            f"<div class='justified'>Ugovorne strane suglasno utvrđuju da su dana {datum_osnovnog} "
            f"sklopile Ugovor o radu (u daljnjem tekstu: Ugovor) te da sporazumno pristupaju "
            f"prestanku navedenog Ugovora.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Datum prestanka)</div>"
            f"<div class='justified'>Ugovorne strane sporazumno utvrđuju da radni odnos Radnika "
            f"prestaje zaključno s danom <b>{datum_prestanka}</b>.</div><br>"
        )
        clanak_br += 1

        if go_neiskoristen > 0:
            if naknada_go:
                go_tekst = (
                    f"Radnik na dan prestanka radnog odnosa ima {go_neiskoristen} dana neiskorištenog "
                    f"godišnjeg odmora. Poslodavac će Radniku isplatiti naknadu za neiskorišteni "
                    f"godišnji odmor sukladno zakonu."
                )
            else:
                go_tekst = (
                    f"Radnik na dan prestanka radnog odnosa ima {go_neiskoristen} dana neiskorištenog "
                    f"godišnjeg odmora. Radnik će neiskorišteni godišnji odmor koristiti u naravi "
                    f"prije prestanka radnog odnosa."
                )
        else:
            go_tekst = "Radnik je iskoristio cjelokupni godišnji odmor prije prestanka radnog odnosa."

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Godišnji odmor)</div>"
            f"<div class='justified'>{go_tekst}</div><br>"
        )
        clanak_br += 1

        if otpremnina and otpremnina > 0:
            parts.append(
                f"<div class='section-title'>Članak {clanak_br}. (Otpremnina)</div>"
                f"<div class='justified'>Poslodavac se obvezuje Radniku isplatiti otpremninu u iznosu od "
                f"<b>{format_eur_s_rijecima(otpremnina)}</b> bruto, najkasnije s posljednjom plaćom. "
                f"Visina otpremnine ugovorena je slobodnom voljom ugovornih strana.</div><br>"
            )
            clanak_br += 1

        if povrat_imovine:
            parts.append(
                f"<div class='section-title'>Članak {clanak_br}. (Povrat imovine)</div>"
                f"<div class='justified'>Radnik se obvezuje najkasnije na dan prestanka radnog odnosa "
                f"Poslodavcu vratiti svu povjerenu imovinu, uključujući: {povrat_imovine}.</div><br>"
            )
            clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Odjava s osiguranja)</div>"
            f"<div class='justified'>Poslodavac će Radnika odjaviti s obveznih osiguranja "
            f"(HZMO, HZZO) s danom prestanka radnog odnosa.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Odricanje od potraživanja)</div>"
            f"<div class='justified'>Potpisom ovog Sporazuma ugovorne strane izjavljuju da nemaju "
            f"međusobnih potraživanja iz radnog odnosa ili u vezi s radnim odnosom, osim onih "
            f"izričito navedenih u ovom Sporazumu.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Završne odredbe)</div>"
            f"<div class='justified'>Ovaj Sporazum sastavljen je u 3 (tri) istovjetna primjerka, "
            f"od kojih svaka ugovorna strana zadržava po jedan.</div><br>"
        )

        parts.append(
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>ZA POSLODAVCA</b><br><br><br>______________________</div>"
            f"<div class='signature-block'><b>RADNIK</b><br><br><br>______________________</div>"
            f"</div>"
        )

        parts.append(
            f"<br><div class='justified' style='font-size: 9pt; color: #555;'>"
            f"<b>Napomena:</b> Radnik koji sklopi sporazumni prestanak ugovora o radu nema pravo na "
            f"novčanu naknadu za vrijeme nezaposlenosti pri Hrvatskom zavodu za zapošljavanje (HZZ), "
            f"sukladno Zakonu o tržištu rada.</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_zabranu_natjecanja(poslodavac, radnik, podaci):
    """
    Generira ugovor o zabrani natjecanja.
    Pravni temelj: Zakon o radu čl. 101-105
    """
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        trajanje = podaci.get("trajanje_mjeseci", 24)
        if trajanje > 24:
            trajanje = 24

        parts = [
            f"<div class='header-doc'>UGOVOR O ZABRANI NATJECANJA</div>",
            f"<div class='justified' style='font-size: 10pt;'>"
            f"ZAHTIJEVANA FORMA: PISANA (ZoR čl. 101-105 – ništetnost bez pisanog oblika)</div><br>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {datum} godine, između:<br><br>"
            f"1. <b>POSLODAVAC:</b><br>{poslodavac}<br><br>"
            f"2. <b>RADNIK:</b><br>{radnik}</div><br>",
        ]

        clanak_br = 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Predmet i opseg zabrane)</div>"
            f"<div class='justified'>Radnik se obvezuje da nakon prestanka radnog odnosa kod Poslodavca "
            f"neće obavljati poslove niti sudjelovati u poslovanju koje je u tržišnom natjecanju "
            f"s djelatnošću Poslodavca.<br><br>"
            f"<b>Materijalni opseg zabrane:</b> {podaci.get('opis_zabrane', '_______')}.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Teritorijalno ograničenje)</div>"
            f"<div class='justified'>Zabrana natjecanja primjenjuje se na sljedećem području: "
            f"<b>{podaci.get('teritorij', 'Republika Hrvatska')}</b>.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Trajanje)</div>"
            f"<div class='justified'>Zabrana natjecanja vrijedi u trajanju od <b>{trajanje} mjeseci</b> "
            f"od dana prestanka radnog odnosa. Sukladno članku 102. Zakona o radu, ugovorena zabrana "
            f"natjecanja ne može trajati dulje od dvije (2) godine.</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Naknada)</div>"
            f"<div class='justified'>Poslodavac se obvezuje Radniku za vrijeme trajanja zabrane natjecanja "
            f"mjesečno isplaćivati naknadu u iznosu od <b>{format_eur_s_rijecima(podaci.get('mjesecna_naknada', 0))}</b>.<br><br>"
            f"Sukladno članku 102. stavku 3. Zakona o radu, naknada ne smije biti manja od polovice "
            f"prosječne plaće isplaćene Radniku u tri mjeseca prije prestanka radnog odnosa. "
            f"<b>Bez ugovorene naknade ugovorna zabrana natjecanja nema pravnog učinka.</b></div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Ugovorna kazna)</div>"
            f"<div class='justified'>U slučaju kršenja zabrane natjecanja, Radnik se obvezuje Poslodavcu "
            f"platiti ugovornu kaznu u iznosu od <b>{format_eur_s_rijecima(podaci.get('ugovorna_kazna', 0))}</b>.<br><br>"
            f"Plaćanjem ugovorne kazne prestaje obveza zabrane natjecanja.</div><br>"
        )
        clanak_br += 1

        datum_prestanka_ro = podaci.get("datum_prestanka_radnog_odnosa", "")
        prestanak_tekst = ""
        if datum_prestanka_ro:
            prestanak_tekst = (
                f" Radni odnos Radnika prestao je dana {datum_prestanka_ro}."
            )

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Prestanak zabrane)</div>"
            f"<div class='justified'>Sukladno članku 102. Zakona o radu, ako Poslodavac otkaže ugovor o radu, "
            f"a za otkaz nema opravdanog razloga, ili ako Radnik otkaže ugovor o radu izvanrednim otkazom "
            f"zbog ponašanja Poslodavca, ugovorena zabrana natjecanja prestaje.{prestanak_tekst}</div><br>"
        )
        clanak_br += 1

        parts.append(
            f"<div class='section-title'>Članak {clanak_br}. (Završne odredbe)</div>"
            f"<div class='justified'>Ovaj Ugovor sastavljen je u 3 (tri) istovjetna primjerka, "
            f"od kojih svaka ugovorna strana zadržava po jedan.</div><br>"
        )

        parts.append(
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>ZA POSLODAVCA</b><br><br><br>______________________</div>"
            f"<div class='signature-block'><b>RADNIK</b><br><br><br>______________________</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_potvrdu_o_zaposlenju(poslodavac, radnik, podaci):
    """
    Generira potvrdu o zaposlenju.
    """
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        datum_od = podaci.get("datum_od", "________")
        datum_do = podaci.get("datum_do", "________")
        opis_poslova = podaci.get("opis_poslova", "________")
        radnik_ime_gen = _padez_ime(podaci.get("radnik_ime", ""), "gen")
        radnik_prikaz = f"<b>{radnik_ime_gen}</b>" if radnik_ime_gen else radnik

        parts = [
            f"<div class='party-info'><b>POSLODAVAC:</b><br>{poslodavac}</div><br>",
            f"<div class='header-doc'>POTVRDA O ZAPOSLENJU</div>",
            f"<div class='justified'>"
            f"Potvrđuje se da je {radnik_prikaz} bio/bila zaposlen/a kod gore navedenog Poslodavca "
            f"u razdoblju od <b>{datum_od}</b> do <b>{datum_do}</b> na poslovima: "
            f"<b>{opis_poslova}</b>.</div><br>",
            f"<div class='justified'>Potvrda se izdaje na zahtjev Radnika u svrhu predočavanja "
            f"nadležnim tijelima i trećim osobama.</div><br>",
            f"<div class='justified' style='font-size: 10pt;'>"
            f"Sukladno Zakonu o radu, potvrda o zaposlenju ne smije sadržavati podatke "
            f"koji bi mogli otežati sklapanje novog ugovora o radu.</div><br>",
            f"<div class='justified' style='text-align: right;'>{mjesto}, {datum}</div><br>",
            f'<table width="100%" border="0"><tr>'
            f'<td width="50%" align="left"></td>'
            f'<td width="50%" align="center"><b>ZA POSLODAVCA</b><br><br><br>'
            f"______________________<br><br>"
            f"<span style='font-size: 10pt;'>(pečat)</span></td>"
            f"</tr></table>",
        ]

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
