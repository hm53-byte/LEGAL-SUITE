# -----------------------------------------------------------------------------
# GENERATORI: Upravno pravo
# Pravni temelj: ZUP, ZUS, ZPPI, Ustav RH
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur


def generiraj_zalbu_zup(zalitelj, podaci):
    """
    Generira žalbu u upravnom postupku.
    Pravni temelj: Zakon o općem upravnom postupku (NN 47/09, 110/21, 104/25).
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        drugostupanjsko = podaci.get("drugostupanjsko_tijelo", "")
        prvostupanjsko = podaci.get("prvostupanjsko_tijelo", "")
        klasa = podaci.get("klasa", "")
        urbroj = podaci.get("urbroj", "")
        datum_rjesenja = podaci.get("datum_rjesenja", "")
        razlozi = format_text(podaci.get("razlozi", ""))
        zalbeni_prijedlog = podaci.get("zalbeni_prijedlog", "poništi i vrati")

        if zalbeni_prijedlog == "poništi i vrati":
            prijedlog_tekst = (
                "da žalbu uvaži, pobijano rješenje <b>poništi</b> i predmet "
                "vrati prvostupanjskom tijelu na ponovni postupak i odlučivanje"
            )
        else:
            prijedlog_tekst = (
                "da žalbu uvaži te pobijano rješenje <b>izmijeni</b> tako da "
                "usvoji zahtjev žalitelja u cijelosti"
            )

        parts = []

        # Adresiranje - drugostupanjsko putem prvostupanjskog
        parts.append(
            f"<div style='font-weight: bold; font-size: 14px;'>{drugostupanjsko.upper()}</div>"
            f"<div>(kao drugostupanjskom tijelu)</div><br>"
            f"<div>putem</div><br>"
            f"<div style='font-weight: bold;'>{prvostupanjsko.upper()}</div>"
            f"<div>(kao prvostupanjskog tijela)</div><br><br>"
        )

        # Žalitelj info - desna strana
        parts.append(
            f"<div class='party-info'><b>ŽALITELJ:</b><br>{zalitelj}</div><br>"
        )

        # Naslov
        parts.append("<div class='header-doc'>ŽALBA</div>")

        # Identifikacija pobijanog akta
        parts.append(
            f"<div class='justified'>Žalitelj ovime pravovremeno, u zakonskom roku od 15 dana, "
            f"podnosi žalbu protiv rješenja {prvostupanjsko}, "
            f"KLASA: <b>{klasa}</b>, URBROJ: <b>{urbroj}</b>, "
            f"od dana <b>{datum_rjesenja}</b>, koje je žalitelju dostavljeno dana ________.</div><br>"
        )

        # Razlozi žalbe
        parts.append("<div class='section-title'>I. RAZLOZI ŽALBE</div>")
        parts.append(
            "<div class='justified'>Žalitelj pobija prvostupanjsko rješenje zbog sljedećih razloga "
            "(članak 105. stavak 2. Zakona o općem upravnom postupku):</div><br>"
            "<div class='justified'>"
            "<b>a) Povreda pravila postupka</b> – prvostupanjsko tijelo nije provelo postupak "
            "sukladno odredbama ZUP-a, čime je povrijeđeno pravo stranke na pravično postupanje.<br><br>"
            "<b>b) Pogrešno ili nepotpuno utvrđeno činjenično stanje</b> – činjenice na kojima se "
            "temelji pobijano rješenje nisu pravilno utvrđene.<br><br>"
            "<b>c) Pogrešna primjena materijalnog zakona</b> – materijalni propis je pogrešno "
            "primijenjen ili uopće nije primijenjen na utvrđeno činjenično stanje.</div><br>"
        )

        # Obrazloženje razloga
        parts.append("<div class='section-title'>II. OBRAZLOŽENJE</div>")
        parts.append(f"<div class='justified'>{razlozi}</div><br>")

        # Žalbeni prijedlog
        parts.append("<div class='section-title'>III. ŽALBENI PRIJEDLOG</div>")
        parts.append(
            f"<div class='justified'>Slijedom svega navedenog, žalitelj predlaže da drugostupanjsko tijelo "
            f"{prijedlog_tekst}.</div><br>"
        )

        # Napomena o roku i odgodnom učinku
        parts.append(
            "<div class='justified'><small><b>Napomena:</b> Žalba se podnosi u roku od 15 dana "
            "od dana dostave prvostupanjskog rješenja (prekluzivni rok). Pravovremeno izjavljena "
            "žalba u pravilu ima odgodni (suspenzivni) učinak, osim kad je zakonom isključen "
            "(članak 112. ZUP-a).</small></div>"
        )

        # Potpis
        parts.append(
            f"<br><div class='justified'>U {mjesto}, dana {danas}</div><br>"
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>ŽALITELJ</b><br>(vlastoručni potpis)</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_tuzbu_zus(tuzitelj, tuzenik_tijelo, podaci):
    """
    Generira tužbu u upravnom sporu.
    Pravni temelj: Zakon o upravnim sporovima (NN 20/10, 143/12, 152/14, 94/16, 29/17, 110/21, 36/24, 104/25).
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        sud = podaci.get("sud", "Upravni sud u Zagrebu")
        klasa = podaci.get("klasa", "")
        urbroj = podaci.get("urbroj", "")
        datum_rjesenja = podaci.get("datum_rjesenja", "")
        razlozi_nezakonitosti = format_text(podaci.get("razlozi_nezakonitosti", ""))
        zahtjev_rasprava = podaci.get("zahtjev_rasprava", False)
        zahtjev_privremena_mjera = podaci.get("zahtjev_privremena_mjera", False)
        privremena_mjera_razlog = format_text(podaci.get("privremena_mjera_razlog", ""))
        tuzbeni_zahtjev = podaci.get("tuzbeni_zahtjev", "poništenje")

        parts = []

        # Naslovni sud
        parts.append(
            f"<div style='font-weight: bold; font-size: 14px;'>{sud.upper()}</div><br><br>"
        )

        # Naslov
        parts.append("<div class='header-doc'>TUŽBA U UPRAVNOM SPORU</div>")

        # Tužitelj
        parts.append(
            f"<div class='party-info'><b>TUŽITELJ:</b><br>{tuzitelj}</div>"
        )

        # Tuženik (javnopravno tijelo)
        parts.append(
            f"<div class='party-info'><b>TUŽENIK (javnopravno tijelo):</b><br>{tuzenik_tijelo}</div><br>"
        )

        # I. Pobijani akt
        parts.append("<div class='section-title'>I. POBIJANI AKT</div>")
        parts.append(
            f"<div class='justified'>Tužitelj podnosi tužbu protiv rješenja tuženika, "
            f"KLASA: <b>{klasa}</b>, URBROJ: <b>{urbroj}</b>, od dana <b>{datum_rjesenja}</b>, "
            f"koje je tužitelju dostavljeno dana ________.</div><br>"
        )

        # II. Razlozi nezakonitosti
        parts.append("<div class='section-title'>II. RAZLOZI NEZAKONITOSTI</div>")
        parts.append(
            "<div class='justified'>Pobijano rješenje je nezakonito iz sljedećih razloga "
            "(članak 36. stavak 2. ZUS-a):</div><br>"
            f"<div class='justified'>{razlozi_nezakonitosti}</div><br>"
        )

        # III. Izjava o usmenoj raspravi
        parts.append("<div class='section-title'>III. IZJAVA O USMENOJ RASPRAVI</div>")
        if zahtjev_rasprava:
            parts.append(
                "<div class='justified'>Tužitelj izričito zahtijeva zakazivanje usmene rasprave "
                "sukladno članku 36. stavku 4. Zakona o upravnim sporovima, budući da smatra "
                "da je potrebno neposredno izvesti dokaze radi pravilnog utvrđenja činjeničnog stanja.</div><br>"
            )
        else:
            parts.append(
                "<div class='justified'>Tužitelj ne zahtijeva održavanje usmene rasprave te "
                "pristaje da sud odluči na nejavnoj sjednici.</div><br>"
            )

        # IV. Privremena mjera (ako je zatražena)
        if zahtjev_privremena_mjera:
            parts.append("<div class='section-title'>IV. PRIJEDLOG ZA PRIVREMENU MJERU</div>")
            parts.append(
                "<div class='justified'>Na temelju članka 47. Zakona o upravnim sporovima, "
                "tužitelj predlaže da sud donese privremenu mjeru odgode izvršenja pobijanog rješenja "
                "iz sljedećih razloga:</div><br>"
                f"<div class='justified'>{privremena_mjera_razlog}</div><br>"
                "<div class='justified'>Izvršenjem pobijanog rješenja tužitelju bi nastala šteta "
                "koja bi se teško mogla popraviti, a odgoda nije protivna javnom interesu.</div><br>"
            )

        # V. Tužbeni zahtjev
        section_num = "V" if zahtjev_privremena_mjera else "IV"
        parts.append(f"<div class='section-title'>{section_num}. TUŽBENI ZAHTJEV</div>")

        if tuzbeni_zahtjev == "poništenje":
            parts.append(
                "<div class='justified'>Slijedom navedenog, tužitelj predlaže da Sud donese sljedeću</div>"
                '<div style="text-align: center; font-weight: bold; margin: 10px 0;">PRESUDU</div>'
                "<div class='justified'>"
                f"<b>I.</b> Poništava se rješenje tuženika KLASA: {klasa}, URBROJ: {urbroj} "
                f"od dana {datum_rjesenja}.<br><br>"
                "<b>II.</b> Predmet se vraća tuženiku na ponovni postupak.</div><br>"
            )
        else:
            parts.append(
                "<div class='justified'>Slijedom navedenog, tužitelj predlaže da Sud, u sporu pune jurisdikcije "
                "(članak 58. ZUS-a), donese sljedeću</div>"
                '<div style="text-align: center; font-weight: bold; margin: 10px 0;">PRESUDU</div>'
                "<div class='justified'>"
                f"<b>I.</b> Poništava se rješenje tuženika KLASA: {klasa}, URBROJ: {urbroj} "
                f"od dana {datum_rjesenja}.<br><br>"
                "<b>II.</b> Usvaja se zahtjev tužitelja te se nalaže tuženiku da odluči "
                "sukladno pravnom shvaćanju suda.</div><br>"
            )

        # Napomena
        parts.append(
            "<div class='justified'><small><b>Napomena:</b> Tužba u upravnom sporu podnosi se u roku od "
            "30 dana od dostave pobijanog rješenja (članak 24. ZUS-a). Za razliku od žalbe u upravnom "
            "postupku, tužba nema suspenzivni učinak - pobijano rješenje se izvršava bez obzira na "
            "podnesenu tužbu, osim ako sud ne odredi privremenu mjeru odgode izvršenja.</small></div>"
        )

        # Potpis
        parts.append(
            f"<br><div class='justified'>U {mjesto}, dana {danas}</div><br>"
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>TUŽITELJ</b><br>(vlastoručni potpis)</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_zahtjev_informacije(podnositelj, podaci):
    """
    Generira zahtjev za pristup informacijama.
    Pravni temelj: Zakon o pravu na pristup informacijama (NN 25/13, 85/15, 69/22, 104/25).
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        tijelo_javne_vlasti = podaci.get("tijelo_javne_vlasti", "")
        opis_informacije = format_text(podaci.get("opis_informacije", ""))
        nacin_pristupa = podaci.get("nacin_pristupa", "pisana dostava")

        nacin_map = {
            "neposredan uvid": "neposrednim uvidom u informaciju u prostorijama tijela javne vlasti",
            "pisana dostava": "dostavom pisane informacije poštom na adresu podnositelja",
            "preslika": "dostavom preslike dokumenta koji sadrži traženu informaciju",
            "elektronička pošta": "dostavom informacije elektroničkom poštom",
        }
        nacin_tekst = nacin_map.get(nacin_pristupa, nacin_pristupa)

        parts = []

        # Adresiranje
        parts.append(
            f"<div style='font-weight: bold; font-size: 14px;'>{tijelo_javne_vlasti.upper()}</div>"
            f"<div><i>- tijelo javne vlasti -</i></div><br><br>"
        )

        # Naslov
        parts.append("<div class='header-doc'>ZAHTJEV ZA PRISTUP INFORMACIJAMA</div>")

        # Pravni temelj
        parts.append(
            "<div class='justified'>Na temelju članka 18. stavka 1. Zakona o pravu na pristup informacijama "
            "(NN 25/13, 85/15, 69/22, 104/25), podnosim zahtjev za pristup informacijama kako slijedi:</div><br>"
        )

        # 1. Tijelo javne vlasti
        parts.append("<div class='section-title'>1. TIJELO JAVNE VLASTI KOJEM SE ZAHTJEV PODNOSI</div>")
        parts.append(
            f"<div class='justified'>{tijelo_javne_vlasti}</div><br>"
        )

        # 2. Podaci o podnositelju
        parts.append("<div class='section-title'>2. PODACI O PODNOSITELJU ZAHTJEVA</div>")
        parts.append(
            f"<div class='justified'>{podnositelj}</div><br>"
        )

        # 3. Informacija koja se traži
        parts.append("<div class='section-title'>3. INFORMACIJA KOJA SE TRAŽI</div>")
        parts.append(
            f"<div class='justified'>{opis_informacije}</div><br>"
        )

        # 4. Način pristupa
        parts.append("<div class='section-title'>4. NAČIN NA KOJI SE ŽELI OSTVARITI PRISTUP INFORMACIJI</div>")
        parts.append(
            f"<div class='justified'>Podnositelj zahtjeva traži ostvarivanje pristupa informaciji "
            f"<b>{nacin_tekst}</b>.</div><br>"
        )

        # Napomena
        parts.append(
            "<div class='justified'><small><b>Napomena:</b> Sukladno članku 20. ZPPI-ja, tijelo javne vlasti "
            "dužno je odlučiti o zahtjevu u roku od <b>15 dana</b> od dana podnošenja zahtjeva. "
            "Ako tijelo javne vlasti ne odluči u propisanom roku (šutnja administracije), podnositelj "
            "ima pravo izjaviti žalbu Povjereniku za informiranje (članak 25. stavak 2. ZPPI-ja). "
            "Tijelo javne vlasti može naplatiti stvarne materijalne troškove pružanja informacije "
            "(članak 19. stavak 2. ZPPI-ja).</small></div>"
        )

        # Potpis
        parts.append(
            f"<br><div class='justified'>U {mjesto}, dana {danas}</div><br>"
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>PODNOSITELJ ZAHTJEVA</b><br>(vlastoručni potpis)</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_prigovor_predstavku(podnositelj, podaci):
    """
    Generira prigovor ili predstavku na rad tijela državne uprave.
    Pravni temelj: Ustav RH čl. 46., ZUP čl. 122., Zakon o sustavu državne uprave.
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        tijelo = podaci.get("tijelo", "")
        celnik_tijela = podaci.get("celnik_tijela", "")
        opis_problema = format_text(podaci.get("opis_problema", ""))
        sluzbenici = format_text(podaci.get("sluzbenici", ""))
        klasa_predmeta = podaci.get("klasa_predmeta", "")
        tip = podaci.get("tip", "predstavka")

        if tip == "prigovor":
            naslov = "PRIGOVOR NA POSTUPANJE"
            uvodni_tekst = (
                "Na temelju članka 122. Zakona o općem upravnom postupku (NN 47/09, 110/21, 104/25), "
                "podnosim prigovor na postupanje službenika tijela državne uprave kako slijedi:"
            )
        else:
            naslov = "PREDSTAVKA NA RAD SLUŽBENIKA"
            uvodni_tekst = (
                "Na temelju članka 46. Ustava Republike Hrvatske, kojim je zajamčeno pravo "
                "na podnošenje predstavki i pritužbi, podnosim predstavku na rad službenika "
                "kako slijedi:"
            )

        parts = []

        # Adresiranje - čelniku tijela
        parts.append(
            f"<div style='font-weight: bold; font-size: 14px;'>{tijelo.upper()}</div>"
            f"<div><b>{celnik_tijela}</b></div>"
            f"<div><i>- čelnik tijela -</i></div><br><br>"
        )

        # Podnositelj - desna strana
        parts.append(
            f"<div class='party-info'><b>PODNOSITELJ:</b><br>{podnositelj}</div><br>"
        )

        # Naslov
        parts.append(f"<div class='header-doc'>{naslov}</div>")

        # Uvod
        parts.append(f"<div class='justified'>{uvodni_tekst}</div><br>")

        # Predmet na koji se odnosi
        if klasa_predmeta:
            parts.append(
                f"<div class='justified'><b>Predmet na koji se odnosi:</b> "
                f"KLASA: {klasa_predmeta}</div><br>"
            )

        # Službenici na čiji se rad odnosi
        if sluzbenici:
            parts.append("<div class='section-title'>SLUŽBENICI NA ČIJI SE RAD ODNOSI</div>")
            parts.append(f"<div class='justified'>{sluzbenici}</div><br>")

        # Kronološki opis problema
        parts.append("<div class='section-title'>OPIS PROBLEMA</div>")
        parts.append(f"<div class='justified'>{opis_problema}</div><br>")

        # Zahtjev
        parts.append("<div class='section-title'>ZAHTJEV</div>")
        parts.append(
            "<div class='justified'>Ovime zahtijevam da čelnik tijela ispita navode iz ove "
            f"{'predstavke' if tip == 'predstavka' else 'prigovora'}, poduzme odgovarajuće "
            "mjere te me u zakonskom roku obavijesti o poduzetom.</div><br>"
        )

        # Napomena
        parts.append(
            "<div class='justified'><small><b>Napomena:</b> Pravo na podnošenje predstavki i pritužbi "
            "zajamčeno je člankom 46. Ustava Republike Hrvatske. Čelnik tijela dužan je odgovoriti "
            "podnositelju u roku od <b>30 dana</b> od primitka predstavke/prigovora. "
            "Podnošenje predstavke ili prigovora <b>NE odgađa</b> prekluzivne rokove za izjavljivanje "
            "žalbe ili podnošenje tužbe u upravnom sporu - stranka je dužna paralelno koristiti "
            "redovne pravne lijekove ako želi zaštititi svoja prava.</small></div>"
        )

        # Potpis
        parts.append(
            f"<br><div class='justified'>U {mjesto}, dana {danas}</div><br>"
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>PODNOSITELJ</b><br>(vlastoručni potpis)</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
