# -----------------------------------------------------------------------------
# GENERATORI: Kazneno pravo (kaznena prijava, privatna tuzba, zalba na presudu)
# Kazneni zakon (NN 125/11, 144/12, 56/15, 61/15, 101/17, 118/18, 126/19, 84/21, 114/22, 114/23, 36/24)
# Zakon o kaznenom postupku (NN 152/08, 76/09, 80/11, 91/12, 143/12, 56/13, 145/13, 152/14, 70/17, 126/19)
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur, formatiraj_troskovnik, _rimski_broj as _rimski


def generiraj_kaznenu_prijavu(prijavitelj, podaci):
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        parts = []

        # Nadlezno tijelo
        parts.append(
            f'<div style="font-weight: bold; font-size: 14px; text-align: left;">'
            f'{podaci["nadlezno_tijelo"].upper()}</div><br>'
        )

        # Naslov
        parts.append("<div class='header-doc'>KAZNENA PRIJAVA</div>")

        # Protiv / Zbog
        parts.append(
            f"<div class='justified'>"
            f"<b>PROTIV:</b> {podaci['osumnjicenik_tekst']}<br>"
            f"<b>ZBOG:</b> osnovane sumnje na počinjenje kaznenog djela iz {podaci['clanak_kz']}"
            f"</div><br>"
        )

        # I. Podaci o prijavitelju
        parts.append("<div class='section-title'>I. PODACI O PRIJAVITELJU</div>")
        parts.append(f"<div class='justified'>{prijavitelj}</div>")

        # II. Podaci o osumnjiceniku
        parts.append("<div class='section-title'>II. PODACI O OSUMNJIČENIKU</div>")
        parts.append(f"<div class='justified'>{podaci['osumnjicenik_tekst']}</div>")

        # III. Cinjenicni opis
        parts.append("<div class='section-title'>III. ČINJENIČNI OPIS</div>")
        parts.append(
            f"<div class='justified'>"
            f"Prijavitelj podnosi ovu kaznenu prijavu iz sljedećih razloga:<br><br>"
            f"{format_text(podaci['opis_djela'])}<br><br>"
            f"Navedenim postupanjem osumnjičenik je ostvario obilježja kaznenog djela iz "
            f"{podaci['clanak_kz']}."
            f"</div>"
        )

        # IV. Dokazi
        parts.append("<div class='section-title'>IV. DOKAZI</div>")
        parts.append("<div class='justified'>")
        parts.append("Uz ovu kaznenu prijavu predlažu se sljedeći dokazi:<br>")
        for i, dokaz in enumerate(podaci.get("dokazi", []), 1):
            parts.append(f"{i}. {dokaz}<br>")
        parts.append("</div>")

        # V. Prijedlog
        parts.append("<div class='section-title'>V. PRIJEDLOG</div>")
        parts.append(
            "<div class='justified'>"
            "Slijedom svega navedenog, prijavitelj predlaže da naslovni državni odvjetnik poduzme "
            "potrebne izvide, provede dokazne radnje te, ukoliko rezultati potvrde osnovanu sumnju, "
            "pokrene kazneni postupak protiv osumnjičenika."
            "</div><br>"
        )

        # Upozorenja
        parts.append(
            "<div class='justified' style='font-style: italic; font-size: 11px;'>"
            "<b>Napomena:</b> Lažno prijavljivanje kaznenog djela je kazneno djelo iz čl. 304. KZ-a. "
            "Prijavitelj je svjestan posljedica lažnog prijavljivanja.<br><br>"
            "Ukoliko državni odvjetnik odbaci kaznenu prijavu, oštećenik ima pravo preuzeti kazneni "
            "progon kao supsidijarni tužitelj sukladno čl. 55. ZKP-a, u roku od 8 dana od primitka "
            "obavijesti o odbačaju."
            "</div><br>"
        )

        # Potpis
        parts.append(
            f"<div class='justified'>U {podaci.get('mjesto', '___________')}, dana {danas}</div>"
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>PRIJAVITELJ</b></div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_privatnu_tuzbu(tuzitelj, okrivljenik, podaci, troskovi_dict):
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        parts = []

        # Sud
        parts.append(
            f'<div style="font-weight: bold; font-size: 14px; text-align: left;">'
            f'{podaci["sud"].upper()}</div>'
            f'<div style="font-size: 12px; text-align: left;">Kazneni odjel</div><br>'
        )

        # Stranke
        parts.append(
            f"<div class='party-info'>"
            f"<b>PRIVATNI TUŽITELJ:</b><br>{tuzitelj}"
            f"</div>"
        )
        parts.append(
            f"<div class='party-info'>"
            f"<b>OKRIVLJENIK:</b><br>{okrivljenik}"
            f"</div><br>"
        )

        # Naslov
        parts.append("<div class='header-doc'>PRIVATNA TUŽBA</div>")
        parts.append(
            f"<div style='text-align: center;'>zbog kaznenog djela iz {podaci['clanak_kz']}</div><br>"
        )

        # I. Cinjenicni opis djela
        parts.append("<div class='section-title'>I. ČINJENIČNI OPIS DJELA</div>")
        parts.append(
            f"<div class='justified'>"
            f"Dana {podaci['datum_djela']}, u mjestu {podaci['mjesto_djela']}, "
            f"okrivljenik je počinio sljedeće:<br><br>"
            f"{format_text(podaci['opis_djela'])}<br><br>"
            f"Navedenim postupanjem okrivljenik je ostvario sva zakonska obilježja kaznenog djela iz "
            f"{podaci['clanak_kz']}."
            f"</div>"
        )

        # II. Pravna kvalifikacija
        parts.append("<div class='section-title'>II. PRAVNA KVALIFIKACIJA</div>")
        parts.append(
            f"<div class='justified'>"
            f"Opisano djelo predstavlja kazneno djelo iz {podaci['clanak_kz']}, "
            f"koje se progoni po privatnoj tužbi sukladno odredbama Kaznenog zakona."
            f"</div>"
        )

        # III. Dokazi
        parts.append("<div class='section-title'>III. DOKAZI</div>")
        parts.append("<div class='justified'>Predlažu se sljedeći dokazi:<br>")
        for i, dokaz in enumerate(podaci.get("dokazi", []), 1):
            parts.append(f"{i}. {dokaz}<br>")
        parts.append("</div>")

        # IV. Kazneni zahtjev
        parts.append("<div class='section-title'>IV. KAZNENI ZAHTJEV</div>")
        parts.append(
            f"<div class='justified'>"
            f"Slijedom svega navedenog, privatni tužitelj zahtijeva da naslovni sud donese sljedeću<br><br>"
            f"<div style='text-align: center; font-weight: bold;'>OSUĐUJUĆU PRESUDU</div><br>"
            f"{format_text(podaci['kazneni_zahtjev'])}"
            f"</div>"
        )

        # Troskovnik
        parts.append(troskovnik_html)

        # Upozorenja
        parts.append(
            "<br><div class='justified' style='font-style: italic; font-size: 11px;'>"
            "<b>Napomena:</b> Privatna tužba mora se podnijeti u roku od <b>3 mjeseca</b> od dana "
            "kad je oštećenik saznao za kazneno djelo i počinitelja (prekluzivni rok, čl. 61. KZ-a). "
            "Protekom roka gubi se pravo na kazneni progon.<br><br>"
            "Privatni tužitelj je dužan uplatiti sudsku pristojbu te snosi rizik naknade troškova "
            "okrivljenikove obrane u slučaju oslobađajuće presude."
            "</div><br>"
        )

        # Potpis
        parts.append(
            f"<div class='justified'>U {podaci.get('mjesto', '___________')}, dana {danas}</div>"
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>PRIVATNI TUŽITELJ</b></div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_zalbu_kaznena_presuda(zalitelj, podaci, troskovi_dict):
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        parts = []

        # Naslovni sud (drugostupanjski putem prvostupanjskog)
        parts.append(
            f'<div style="font-weight: bold; font-size: 14px;">'
            f'{podaci["sud_drugostupanjski"].upper()}</div>'
            f'<div>(kao drugostupanjskom sudu)</div><br>'
            f'<div>putem</div><br>'
            f'<div style="font-weight: bold;">'
            f'{podaci["sud_prvostupanjski"].upper()}</div>'
            f'<div>(kao prvostupanjskog suda)</div><br>'
        )

        # Poslovni broj (desno poravnato)
        parts.append(
            f'<div style="text-align: right;"><b>Broj predmeta: {podaci["poslovni_broj"]}</b></div><br>'
        )

        # Zalitelj
        parts.append(
            f"<div class='party-info'><b>ŽALITELJ:</b><br>{zalitelj}</div><br>"
        )

        # Naslov
        parts.append("<div class='header-doc'>ŽALBA PROTIV PRESUDE</div>")
        parts.append(
            f"<div style='text-align: center;'>protiv presude {podaci['sud_prvostupanjski']} "
            f"poslovni broj {podaci['poslovni_broj']} od dana {podaci['datum_presude']}</div><br>"
        )

        # Uvod
        parts.append(
            f"<div class='justified'>"
            f"Žalitelj ovime pravovremeno, u zakonskom roku od 15 dana, podnosi žalbu protiv "
            f"presude {podaci['sud_prvostupanjski']}, poslovni broj {podaci['poslovni_broj']} "
            f"od {podaci['datum_presude']}, čija izreka glasi:<br><br>"
            f"<i>\"{format_text(podaci['izreka_presude'])}\"</i><br><br>"
            f"Žalba se podnosi iz sljedećih razloga (čl. 464. ZKP-a):"
            f"</div><br>"
        )

        # Razlozi zalbe - samo oni koji su popunjeni
        razlozi = podaci.get("razlozi", {})
        redni_broj = 1

        if razlozi.get("bitna_povreda"):
            parts.append(
                f"<div class='section-title'>{_rimski(redni_broj)}. "
                f"BITNA POVREDA ODREDABA KAZNENOG POSTUPKA</div>"
            )
            parts.append(
                f"<div class='justified'>"
                f"Prvostupanjska presuda je donesena uz bitnu povredu odredaba kaznenog postupka "
                f"iz čl. 468. ZKP-a:<br><br>"
                f"{format_text(razlozi['bitna_povreda'])}"
                f"</div>"
            )
            redni_broj += 1

        if razlozi.get("materijalni_zakon"):
            parts.append(
                f"<div class='section-title'>{_rimski(redni_broj)}. "
                f"POVREDA KAZNENOG ZAKONA</div>"
            )
            parts.append(
                f"<div class='justified'>"
                f"Prvostupanjskom presudom povrijeđen je kazneni zakon (čl. 469. ZKP-a):<br><br>"
                f"{format_text(razlozi['materijalni_zakon'])}"
                f"</div>"
            )
            redni_broj += 1

        if razlozi.get("cinjenicno_stanje"):
            parts.append(
                f"<div class='section-title'>{_rimski(redni_broj)}. "
                f"POGREŠNO ILI NEPOTPUNO UTVRĐENO ČINJENIČNO STANJE</div>"
            )
            parts.append(
                f"<div class='justified'>"
                f"Činjenično stanje je pogrešno ili nepotpuno utvrđeno (čl. 470. ZKP-a):<br><br>"
                f"{format_text(razlozi['cinjenicno_stanje'])}"
                f"</div>"
            )
            redni_broj += 1

        if razlozi.get("odluka_o_kazni"):
            parts.append(
                f"<div class='section-title'>{_rimski(redni_broj)}. "
                f"ODLUKA O KAZNI</div>"
            )
            parts.append(
                f"<div class='justified'>"
                f"Odluka o kaznenoj sankciji je nepravilna (čl. 471. ZKP-a):<br><br>"
                f"{format_text(razlozi['odluka_o_kazni'])}"
                f"</div>"
            )
            redni_broj += 1

        # Zalbeni prijedlog
        parts.append(f"<div class='section-title'>{_rimski(redni_broj)}. ŽALBENI PRIJEDLOG</div>")

        if podaci.get("zalbeni_prijedlog") == "preinači":
            prijedlog_tekst = (
                "Slijedom svega navedenog, žalitelj predlaže da drugostupanjski sud ovu žalbu uvaži te "
                "pobijanu presudu <b>preinači</b> i donese pravilnu i zakonitu odluku."
            )
        else:
            prijedlog_tekst = (
                "Slijedom svega navedenog, žalitelj predlaže da drugostupanjski sud ovu žalbu uvaži, "
                "pobijanu presudu <b>ukine</b> i predmet vrati prvostupanjskom sudu na ponovno suđenje."
            )
        parts.append(f"<div class='justified'>{prijedlog_tekst}</div>")

        # Troskovnik
        parts.append(troskovnik_html)

        # Napomene
        parts.append(
            "<br><div class='justified' style='font-style: italic; font-size: 11px;'>"
            "<b>Napomena:</b> Rok za žalbu protiv kaznene presude iznosi <b>15 dana</b> od dostave "
            "presude (čl. 464. st. 1. ZKP-a). Žalba ima suspenzivni učinak - presuda ne postaje "
            "pravomoćna do odluke drugostupanjskog suda.<br><br>"
            "Drugostupanjski sud ispituje presudu u granicama žalbe (čl. 476. ZKP-a), osim u slučaju "
            "najteže povrede odredaba kaznenog postupka iz čl. 468. st. 1. t. 1.-6. ZKP-a "
            "na koje pazi po službenoj dužnosti (ex officio)."
            "</div><br>"
        )

        # Potpis
        parts.append(
            f"<div class='justified'>U {podaci.get('mjesto', '___________')}, dana {danas}</div>"
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>ŽALITELJ</b></div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


