# -----------------------------------------------------------------------------
# GENERATORI: Ovrsni prijedlog + Prigovor protiv rjesenja o ovrsi JB
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import formatiraj_troskovnik, format_eur, format_eur_s_rijecima, format_text


def generiraj_ovrhu_pro(jb, ovrhovoditelj, ovrsenik, trazbina, isprava, troskovi_dict):
    try:
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        ukupno_trosak = (
            troskovi_dict.get('stavka', 0)
            + troskovi_dict.get('pdv', 0)
            + troskovi_dict.get('materijalni', 0)
            + troskovi_dict.get('pristojba', 0)
        )
        return f"""
        <div style="font-weight: bold;">JAVNOM BILJEŽNIKU {jb.upper()}</div>
        <br>
        <div class='justified'><b>OVRHOVODITELJ:</b> {ovrhovoditelj}<br><b>OVRŠENIK:</b> {ovrsenik}<br><br><b>Radi:</b> Ovrhe na temelju vjerodostojne isprave<br><b>Vrijednost tražbine: {format_eur(trazbina['glavnica'])}</b></div>
        <br><div class='header-doc'>PRIJEDLOG ZA OVRHU<br><span style='font-size:11pt; font-weight:normal'>na temelju vjerodostojne isprave</span></div>
        <div class='justified'>Na temelju vjerodostojne isprave – <b>{isprava}</b> od dana {trazbina['datum_racuna']}, iz koje proizlazi dospjela tražbina Ovrhovoditelja prema Ovršeniku, Ovrhovoditelj predlaže da Javni bilježnik donese sljedeće:</div>
        <div style='border: 2px solid black; padding: 15px; margin: 20px 0;'><div class='header-doc' style='margin:0;'>RJEŠENJE O OVRSI</div><div style='text-align:center; font-size:10pt;'>(na temelju vjerodostojne isprave)</div><br>
        <div class='justified'><b>I. NALAŽE SE Ovršeniku</b> da Ovrhovoditelju u roku od osam dana od dana dostave ovog rješenja namiri tražbinu u iznosu od <b>{format_eur_s_rijecima(trazbina['glavnica'])}</b>, zajedno sa zakonskim zateznim kamatama koje teku od dana dospijeća <b>{trazbina['dospjece']}</b> pa do isplate, kao i da mu naknadi troškove ovog postupka u iznosu od <b>{format_eur_s_rijecima(ukupno_trosak)}</b>.<br><br>
        <b>II. ODREĐUJE SE OVRHA</b> radi naplate tražbine iz točke I. ovog rješenja i troškova postupka. Ovrha će se provesti na novčanim sredstvima Ovršenika po svim računima kod banaka, te na cjelokupnoj imovini Ovršenika.</div></div>
        {troskovnik_html}
        <br><br><div class='signature-row'><div style='display:inline-block; width: 50%;'></div><div class='signature-block'><b>OVRHOVODITELJ</b><br><br><br>______________________</div></div>
        """
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_prigovor_ovrhe(sud, ovrsenik, ovrhovoditelj, podaci, troskovi_dict):
    """
    Generira prigovor protiv rješenja o ovrsi na temelju vjerodostojne isprave.
    Rok: 8 dana od dostave. Pretvara postupak u parnicu.
    Pravni temelj: Ovršni zakon čl. 41-42
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        razlozi_tekst = format_text(podaci.get("razlozi", ""))
        poslovni_broj = podaci.get("poslovni_broj", "________")
        datum_rjesenja = podaci.get("datum_rjesenja", "________")
        jb = podaci.get("javni_bilježnik", "________")
        mjesto = podaci.get("mjesto", "Zagreb")

        return (
            f'<div style="font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f"<br>"
            f"<div class='justified'>"
            f"<b>OVRŠENIK (predlagatelj prigovora):</b><br>{ovrsenik}<br><br>"
            f"<b>OVRHOVODITELJ (protivna strana):</b><br>{ovrhovoditelj}<br><br>"
            f"<b>Poslovni broj rješenja o ovrsi:</b> {poslovni_broj}<br>"
            f"<b>Radi:</b> Prigovora protiv rješenja o ovrsi na temelju vjerodostojne isprave"
            f"</div><br>"
            f"<div class='header-doc'>PRIGOVOR<br>"
            f"<span style='font-size: 11pt; font-weight: normal;'>protiv rješenja o ovrsi "
            f"na temelju vjerodostojne isprave</span></div>"
            f"<div class='justified'>Ovršenik ovime, pravovremeno i u zakonskom roku od 8 dana "
            f"od dana primitka rješenja o ovrsi, podnosi <b>prigovor</b> protiv rješenja o ovrsi "
            f"na temelju vjerodostojne isprave javnog bilježnika {jb}, "
            f"poslovni broj {poslovni_broj} od {datum_rjesenja}.</div><br>"
            f"<div class='section-title'>I. RAZLOZI PRIGOVORA</div>"
            f"<div class='justified'>{razlozi_tekst}</div><br>"
            f"<div class='section-title'>II. PRIJEDLOG</div>"
            f"<div class='justified'>Na temelju članka 41. i 42. Ovršnog zakona (NN 112/12, 25/13, "
            f"93/14, 55/16, 73/17, 131/20), predlaže se da naslovni sud:</div><br>"
            f"<div class='justified'>"
            f"<b>I.</b> Uvaži prigovor Ovršenika.<br><br>"
            f"<b>II.</b> Stavi izvan snage rješenje o ovrsi javnog bilježnika {jb}, "
            f"poslovni broj {poslovni_broj} od {datum_rjesenja}, u dijelu kojim je "
            f"određena ovrha (kondemnatorni dio).<br><br>"
            f"<b>III.</b> Postupak nastavi kao u povodu prigovora protiv platnog naloga, "
            f"sukladno članku 42. stavku 2. Ovršnog zakona.<br><br>"
            f"<b>IV.</b> Naloži Ovrhovoditelju naknaditi Ovršeniku troškove ovog postupka."
            f"</div>"
            f"{troskovnik_html}"
            f"<br><br>"
            f'<table width="100%" border="0"><tr>'
            f'<td width="50%" align="left">U {mjesto}, dana {danas}</td>'
            f'<td width="50%" align="center"><b>OVRŠENIK</b><br><br><br>______________________</td>'
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_ovrhu_ovrsna_isprava(sud, ovrhovoditelj, ovrsenik, podaci, troskovi_dict):
    """
    Generira prijedlog za ovrhu na temelju ovršne isprave (presuda, nagodba, javnobilježnički akt).
    Pravni temelj: Ovršni zakon čl. 21-26
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        ukupno_trosak = (
            troskovi_dict.get('stavka', 0)
            + troskovi_dict.get('pdv', 0)
            + troskovi_dict.get('materijalni', 0)
            + troskovi_dict.get('pristojba', 0)
        )
        ovrsna_isprava = format_text(podaci.get("ovrsna_isprava", ""))
        poslovni_broj_isprave = podaci.get("poslovni_broj_isprave", "________")
        datum_isprave = podaci.get("datum_isprave", "________")
        glavnica = podaci.get("glavnica", 0)
        kamate_od = podaci.get("kamate_od", "________")
        sredstvo_ovrhe = podaci.get("sredstvo_ovrhe", "novčana sredstva")
        mjesto = podaci.get("mjesto", "Zagreb")

        if sredstvo_ovrhe.lower() in ("novčana sredstva", "novčana"):
            sredstvo_tekst = (
                "na novčanim sredstvima Ovršenika po svim računima kod banaka, "
                "te na cjelokupnoj imovini Ovršenika"
            )
        elif sredstvo_ovrhe.lower() in ("nekretnina", "nekretnine"):
            sredstvo_tekst = (
                "na nekretnini Ovršenika, sukladno odredbama Ovršnog zakona o ovrsi na nekretnini"
            )
        elif sredstvo_ovrhe.lower() in ("plaća", "placa", "plaći"):
            sredstvo_tekst = (
                "na plaći i drugim stalnim novčanim primanjima Ovršenika"
            )
        else:
            sredstvo_tekst = format_text(sredstvo_ovrhe)

        return (
            f'<div style="text-align: right; font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f"<br>"
            f"<div style='text-align: center; font-size: 11pt; font-weight: bold;'>OVRŠNI PREDMET</div>"
            f"<br>"
            f"<div class='justified'>"
            f"<b>OVRHOVODITELJ:</b><br>{ovrhovoditelj}<br><br>"
            f"<b>OVRŠENIK:</b><br>{ovrsenik}<br><br>"
            f"<b>Radi:</b> Ovrhe na temelju ovršne isprave<br>"
            f"<b>Vrijednost tražbine:</b> {format_eur(glavnica)}"
            f"</div><br>"
            f"<div class='header-doc'>PRIJEDLOG ZA OVRHU<br>"
            f"<span style='font-size: 11pt; font-weight: normal;'>na temelju ovršne isprave</span></div>"
            f"<div class='justified'>Na temelju ovršne isprave – <b>{ovrsna_isprava}</b>, "
            f"poslovni broj {poslovni_broj_isprave} od {datum_isprave}, koja je postala pravomoćna "
            f"i ovršna, iz koje proizlazi dospjela tražbina Ovrhovoditelja prema Ovršeniku, "
            f"Ovrhovoditelj predlaže da naslovni sud donese sljedeće:</div><br>"
            f"<div style='border: 2px solid black; padding: 15px; margin: 20px 0;'>"
            f"<div class='header-doc' style='margin:0;'>RJEŠENJE O OVRSI</div>"
            f"<div style='text-align:center; font-size:10pt;'>(na temelju ovršne isprave)</div><br>"
            f"<div class='justified'>"
            f"<b>I. NALAŽE SE Ovršeniku</b> da Ovrhovoditelju u roku od osam (8) dana od dana "
            f"dostave ovog rješenja namiri tražbinu u iznosu od <b>{format_eur_s_rijecima(glavnica)}</b>, "
            f"zajedno sa zakonskim zateznim kamatama koje teku od dana <b>{kamate_od}</b> pa do isplate, "
            f"kao i da mu naknadi troškove ovog postupka u iznosu od <b>{format_eur_s_rijecima(ukupno_trosak)}</b>.<br><br>"
            f"<b>II. ODREĐUJE SE OVRHA</b> radi naplate tražbine iz točke I. ovog rješenja i troškova "
            f"postupka, i to {sredstvo_tekst}."
            f"</div></div>"
            f"{troskovnik_html}"
            f"<br><br>"
            f'<table width="100%" border="0"><tr>'
            f'<td width="50%" align="left">U {mjesto}, dana {danas}</td>'
            f'<td width="50%" align="center"><b>OVRHOVODITELJ</b><br><br><br>______________________</td>'
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_ovrhu_na_nekretnini(sud, ovrhovoditelj, ovrsenik, podaci, troskovi_dict):
    """
    Generira prijedlog za ovrhu na nekretnini (forum rei sitae).
    Postupak: zabilježba → procjena → e-Dražba (FINA) → namirenje.
    Pravni temelj: Ovršni zakon čl. 75-137
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        ukupno_trosak = (
            troskovi_dict.get('stavka', 0)
            + troskovi_dict.get('pdv', 0)
            + troskovi_dict.get('materijalni', 0)
            + troskovi_dict.get('pristojba', 0)
        )
        ovrsna_isprava = format_text(podaci.get("ovrsna_isprava", ""))
        poslovni_broj_isprave = podaci.get("poslovni_broj_isprave", "________")
        datum_isprave = podaci.get("datum_isprave", "________")
        glavnica = podaci.get("glavnica", 0)
        kamate_od = podaci.get("kamate_od", "________")
        ko = podaci.get("ko", "________")
        ulozak = podaci.get("ulozak", "________")
        cestica = podaci.get("cestica", "________")
        opis_nekretnine = format_text(podaci.get("opis_nekretnine", ""))
        mjesto = podaci.get("mjesto", "Zagreb")

        return (
            f'<div style="text-align: right; font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f"<div style='text-align: right; font-size: 10pt;'>(forum rei sitae – sud prema mjestu "
            f"gdje se nekretnina nalazi)</div>"
            f"<br>"
            f"<div class='justified'>"
            f"<b>OVRHOVODITELJ:</b><br>{ovrhovoditelj}<br><br>"
            f"<b>OVRŠENIK:</b><br>{ovrsenik}<br><br>"
            f"<b>Radi:</b> Ovrhe na nekretnini<br>"
            f"<b>Vrijednost tražbine:</b> {format_eur(glavnica)}"
            f"</div><br>"
            f"<div class='header-doc'>PRIJEDLOG ZA OVRHU NA NEKRETNINI</div>"
            f"<div class='justified'>Na temelju ovršne isprave – <b>{ovrsna_isprava}</b>, "
            f"poslovni broj {poslovni_broj_isprave} od {datum_isprave}, Ovrhovoditelj predlaže "
            f"da naslovni sud donese rješenje o ovrsi na nekretnini Ovršenika.</div><br>"
            f"<div class='section-title'>NEKRETNINA – PREDMET OVRHE</div>"
            f"<div class='justified'>"
            f"<b>Katastarska općina:</b> {ko}<br>"
            f"<b>Zemljišnoknjižni uložak:</b> {ulozak}<br>"
            f"<b>Katastarska čestica:</b> {cestica}<br>"
            f"<b>Opis:</b> {opis_nekretnine}"
            f"</div><br>"
            f"<div style='border: 2px solid black; padding: 15px; margin: 20px 0;'>"
            f"<div class='header-doc' style='margin:0;'>RJEŠENJE O OVRSI NA NEKRETNINI</div><br>"
            f"<div class='justified'>"
            f"<b>I. NALAŽE SE Ovršeniku</b> da Ovrhovoditelju namiri tražbinu u iznosu od "
            f"<b>{format_eur_s_rijecima(glavnica)}</b>, zajedno sa zakonskim zateznim kamatama od "
            f"<b>{kamate_od}</b> do isplate, te troškove postupka u iznosu od "
            f"<b>{format_eur(ukupno_trosak)}</b>.<br><br>"
            f"<b>II. ODREĐUJE SE zabilježba ovrhe</b> u zemljišnoj knjizi Općinskog suda, "
            f"k.o. {ko}, z.k.ul. {ulozak}, k.č.br. {cestica}, "
            f"u korist Ovrhovoditelja.<br><br>"
            f"<b>III. ODREĐUJE SE utvrđivanje vrijednosti nekretnine</b> vještačenjem "
            f"po stalnom sudskom vještaku za graditeljstvo i procjenu nekretnina.<br><br>"
            f"<b>IV. ODREĐUJE SE prisilna prodaja nekretnine</b> putem elektroničke javne dražbe "
            f"(e-Dražba) koju provodi Financijska agencija (FINA), sukladno Ovršnom zakonu.<br><br>"
            f"<b>V. ODREĐUJE SE namirenje Ovrhovoditelja</b> iz kupovnine ostvarene prodajom "
            f"nekretnine, prema redu prvenstva utvrđenom u skladu sa zakonom."
            f"</div></div>"
            f"<div style='background-color: #fff3cd; border: 1px solid #ffc107; padding: 10px; "
            f"margin: 15px 0; font-size: 10pt;'>"
            f"<b>Napomena (čl. 75.a Ovršnog zakona):</b> Ako je predmetna nekretnina jedina "
            f"nekretnina Ovršenika u kojoj stanuje i koja je nužna za zadovoljenje osnovnih "
            f"stambenih potreba, ovrha se ne može provesti ako glavnica tražbine ne prelazi "
            f"iznos od <b>5.308,91 EUR</b>.</div>"
            f"{troskovnik_html}"
            f"<br>"
            f"<div class='section-title'>PRILOZI</div>"
            f"<div class='justified'>"
            f"1. Izvadak iz zemljišne knjige (k.o. {ko}, z.k.ul. {ulozak})<br>"
            f"2. Ovršna isprava – {ovrsna_isprava}, poslovni broj {poslovni_broj_isprave} od {datum_isprave}"
            f"</div>"
            f"<br><br>"
            f'<table width="100%" border="0"><tr>'
            f'<td width="50%" align="left">U {mjesto}, dana {danas}</td>'
            f'<td width="50%" align="center"><b>OVRHOVODITELJ</b><br><br><br>______________________</td>'
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_ovrhu_na_placi(sud, ovrhovoditelj, ovrsenik, podaci, troskovi_dict):
    """
    Generira prijedlog za ovrhu na plaći i stalnim novčanim primanjima.
    Nalog poslodavcu za zapljenu dijela plaće.
    Pravni temelj: Ovršni zakon čl. 149-157
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        ukupno_trosak = (
            troskovi_dict.get('stavka', 0)
            + troskovi_dict.get('pdv', 0)
            + troskovi_dict.get('materijalni', 0)
            + troskovi_dict.get('pristojba', 0)
        )
        ovrsna_isprava = format_text(podaci.get("ovrsna_isprava", ""))
        poslovni_broj_isprave = podaci.get("poslovni_broj_isprave", "________")
        datum_isprave = podaci.get("datum_isprave", "________")
        glavnica = podaci.get("glavnica", 0)
        kamate_od = podaci.get("kamate_od", "________")
        poslodavac_ovrs = format_text(podaci.get("poslodavac_ovrs", ""))
        mjesto = podaci.get("mjesto", "Zagreb")

        return (
            f'<div style="text-align: right; font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f"<br>"
            f"<div class='justified'>"
            f"<b>OVRHOVODITELJ:</b><br>{ovrhovoditelj}<br><br>"
            f"<b>OVRŠENIK:</b><br>{ovrsenik}<br><br>"
            f"<b>POSLODAVAC OVRŠENIKA:</b><br>{poslodavac_ovrs}<br><br>"
            f"<b>Radi:</b> Ovrhe na plaći<br>"
            f"<b>Vrijednost tražbine:</b> {format_eur(glavnica)}"
            f"</div><br>"
            f"<div class='header-doc'>PRIJEDLOG ZA OVRHU NA PLAĆI</div>"
            f"<div class='justified'>Na temelju ovršne isprave – <b>{ovrsna_isprava}</b>, "
            f"poslovni broj {poslovni_broj_isprave} od {datum_isprave}, Ovrhovoditelj predlaže "
            f"da naslovni sud donese rješenje o ovrsi na plaći Ovršenika te naloži poslodavcu "
            f"Ovršenika zapljenu dijela plaće.</div><br>"
            f"<div style='border: 2px solid black; padding: 15px; margin: 20px 0;'>"
            f"<div class='header-doc' style='margin:0;'>RJEŠENJE O OVRSI NA PLAĆI</div><br>"
            f"<div class='justified'>"
            f"<b>I. NALAŽE SE Ovršeniku</b> da Ovrhovoditelju namiri tražbinu u iznosu od "
            f"<b>{format_eur(glavnica)}</b>, zajedno sa zakonskim zateznim kamatama od "
            f"<b>{kamate_od}</b> do isplate, te troškove postupka u iznosu od "
            f"<b>{format_eur(ukupno_trosak)}</b>.<br><br>"
            f"<b>II. NALAŽE SE POSLODAVCU</b> – {poslodavac_ovrs} – da od plaće i svih stalnih "
            f"novčanih primanja Ovršenika zaplijeni odgovarajući dio te da zaplijenjene iznose "
            f"mjesečno isplaćuje izravno Ovrhovoditelju, sve do potpunog namirenja tražbine "
            f"iz točke I. ovog rješenja, uključujući kamate i troškove postupka.<br><br>"
            f"<b>III.</b> Ovrha na plaći provodi se neprekidno dok tražbina ne bude u cijelosti "
            f"namirena, uključujući i u slučaju promjene poslodavca Ovršenika."
            f"</div></div>"
            f"<div style='background-color: #d4edda; border: 1px solid #28a745; padding: 10px; "
            f"margin: 15px 0; font-size: 10pt;'>"
            f"<b>Zaštićeni dio plaće (čl. 153-154 OZ):</b><br>"
            f"• Ako neto plaća Ovršenika ne prelazi prosječnu neto plaću u RH – od ovrhe je "
            f"izuzeta <b>3/4 plaće</b>, a ovrha se provodi na <b>1/4 plaće</b>.<br>"
            f"• Ako neto plaća prelazi prosječnu – od ovrhe je izuzet iznos u visini <b>2/3 "
            f"prosječne neto plaće</b>, a ovrha se provodi na ostatku.<br>"
            f"• Za tražbine po osnovi zakonskog uzdržavanja – od ovrhe je izuzeta <b>1/2 plaće</b>.<br>"
            f"• Ovršenik ima pravo zatražiti otvaranje <b>zaštićenog računa</b> na koji se "
            f"uplaćuju primanja izuzeta od ovrhe.</div>"
            f"{troskovnik_html}"
            f"<br><br>"
            f'<table width="100%" border="0"><tr>'
            f'<td width="50%" align="left">U {mjesto}, dana {danas}</td>'
            f'<td width="50%" align="center"><b>OVRHOVODITELJ</b><br><br><br>______________________</td>'
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_obustavu_ovrhe(sud, podaci):
    """
    Generira prijedlog za obustavu ovršnog postupka.
    Razlozi: namirenje, nagodba, ostalo.
    Pravni temelj: Ovršni zakon čl. 67-72
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        poslovni_broj_spisa = podaci.get("poslovni_broj_spisa", "OVR-________")
        ovrhovoditelj_tekst = format_text(podaci.get("ovrhovoditelj_tekst", ""))
        ovrsenik_tekst = format_text(podaci.get("ovrsenik_tekst", ""))
        razlog = podaci.get("razlog", "namirenje")
        ima_zabilježbu = podaci.get("ima_zabilježbu", False)
        mjesto = podaci.get("mjesto", "Zagreb")

        if razlog.lower() == "namirenje":
            razlog_opis = (
                "Ovrhovoditelj izjavljuje da je tražbina koja je bila predmet ovršnog postupka "
                "u cijelosti namirena, te da nema daljnjih potraživanja prema Ovršeniku po osnovi "
                "ovog postupka."
            )
        elif razlog.lower() == "nagodba":
            razlog_opis = (
                "Stranke su sklopile izvansudsku nagodbu kojom su uredile svoja međusobna prava "
                "i obveze, te Ovrhovoditelj predlaže obustavu ovršnog postupka temeljem postignute nagodbe."
            )
        else:
            razlog_opis = format_text(razlog)

        zabilježba_tekst = ""
        if ima_zabilježbu:
            zabilježba_tekst = (
                f"<br><br><b>III. NALAŽE SE brisanje zabilježbe ovrhe</b> u zemljišnoj knjizi "
                f"koja je provedena u ovom ovršnom postupku, poslovni broj {poslovni_broj_spisa}, "
                f"te se nalaže zemljišnoknjižnom sudu da provede brisanje po pravomoćnosti ovog rješenja."
            )

        return (
            f'<div style="text-align: right; font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f"<br>"
            f"<div class='justified'>"
            f"<b>Poslovni broj:</b> <span style='font-size: 16px; font-weight: bold; "
            f"color: #c0392b;'>{poslovni_broj_spisa}</span><br><br>"
            f"<b>OVRHOVODITELJ:</b><br>{ovrhovoditelj_tekst}<br><br>"
            f"<b>OVRŠENIK:</b><br>{ovrsenik_tekst}<br><br>"
            f"<b>Radi:</b> Obustave ovršnog postupka"
            f"</div><br>"
            f"<div class='header-doc'>PRIJEDLOG ZA OBUSTAVU OVRŠNOG POSTUPKA</div>"
            f"<div class='justified'>U ovršnom predmetu koji se vodi pred naslovnim sudom pod "
            f"poslovnim brojem <b>{poslovni_broj_spisa}</b>, Ovrhovoditelj podnosi prijedlog za "
            f"obustavu ovršnog postupka.</div><br>"
            f"<div class='section-title'>IZJAVA O NAMIRENJU</div>"
            f"<div class='justified'>{razlog_opis}</div><br>"
            f"<div class='section-title'>PRIJEDLOG</div>"
            f"<div class='justified'>Na temelju iznesenog, Ovrhovoditelj predlaže da naslovni sud donese:<br><br>"
            f"<b>I.</b> Obustavlja se ovršni postupak koji se vodi pod poslovnim brojem "
            f"<b>{poslovni_broj_spisa}</b>.<br><br>"
            f"<b>II.</b> Ukidaju se sve provedene ovršne radnje u ovom postupku."
            f"{zabilježba_tekst}"
            f"</div>"
            f"<br><br>"
            f'<table width="100%" border="0"><tr>'
            f'<td width="50%" align="left">U {mjesto}, dana {danas}</td>'
            f'<td width="50%" align="center"><b>OVRHOVODITELJ</b><br><br><br>______________________</td>'
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_privremenu_mjeru(sud, predlagatelj, protivnik, podaci, troskovi_dict):
    """
    Generira prijedlog za određivanje privremene mjere (osiguranje tražbine).
    Pretpostavke: fumus boni iuris + periculum in mora.
    Pravni temelj: Ovršni zakon čl. 340-360
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        vrsta_trazbine = podaci.get("vrsta_trazbine", "novčana")
        fumus = format_text(podaci.get("fumus_boni_iuris", ""))
        periculum = format_text(podaci.get("periculum_in_mora", ""))
        mjera = podaci.get("mjera", "zabrana_raspolaganja")
        poslovni_broj_parnice = podaci.get("poslovni_broj_parnice", "")
        mjesto = podaci.get("mjesto", "Zagreb")

        if mjera == "zabrana_raspolaganja":
            mjera_tekst = (
                "ZABRANJUJE SE Protivniku osiguranja raspolaganje imovinom, uključujući "
                "otuđenje, opterećenje, davanje u zakup ili najam, ili bilo kakvo drugo "
                "raspolaganje koje bi moglo umanjiti vrijednost imovine ili onemogućiti "
                "namirenje tražbine Predlagatelja osiguranja."
            )
        elif mjera == "blokada_racuna":
            mjera_tekst = (
                "ZABRANJUJE SE bankama i drugim financijskim institucijama isplata s računa "
                "Protivnika osiguranja do iznosa tražbine Predlagatelja osiguranja, "
                "te se nalaže blokada sredstava na svim računima Protivnika osiguranja."
            )
        elif mjera == "zabrana_otudenja":
            mjera_tekst = (
                "ZABRANJUJE SE Protivniku osiguranja otuđenje i opterećenje nekretnina "
                "i pokretnina koje su predmet osiguranja, te se ODREĐUJE zabilježba zabrane "
                "otuđenja i opterećenja u zemljišnoj knjizi."
            )
        else:
            mjera_tekst = format_text(mjera)

        parnica_ref = ""
        if poslovni_broj_parnice:
            parnica_ref = (
                f"<br><b>Poslovni broj parnice:</b> {poslovni_broj_parnice}"
            )

        return (
            f'<div style="text-align: right; font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f"<br>"
            f"<div class='justified'>"
            f"<b>PREDLAGATELJ OSIGURANJA:</b><br>{predlagatelj}<br><br>"
            f"<b>PROTIVNIK OSIGURANJA:</b><br>{protivnik}<br><br>"
            f"<b>Radi:</b> Određivanja privremene mjere osiguranja ({vrsta_trazbine} tražbina)"
            f"{parnica_ref}"
            f"</div><br>"
            f"<div class='header-doc' style='color: red;'>"
            f"HITNO – PRIJEDLOG ZA ODREĐIVANJE PRIVREMENE MJERE</div>"
            f"<div class='justified'>Predlagatelj osiguranja podnosi ovaj prijedlog za određivanje "
            f"privremene mjere radi osiguranja {vrsta_trazbine} tražbine, sukladno člancima "
            f"340.-360. Ovršnog zakona.</div><br>"
            f"<div class='section-title'>I. FUMUS BONI IURIS – VJEROJATNOST TRAŽBINE</div>"
            f"<div class='justified'>{fumus}</div><br>"
            f"<div class='section-title'>II. PERICULUM IN MORA – OPASNOST ZA OSTVARENJE TRAŽBINE</div>"
            f"<div class='justified'>{periculum}</div><br>"
            f"<div class='section-title'>III. PRIJEDLOG – PRIVREMENA MJERA</div>"
            f"<div class='justified'>Na temelju iznesenih činjenica i dokaza, Predlagatelj osiguranja "
            f"predlaže da naslovni sud donese sljedeću:</div><br>"
            f"<div style='border: 2px solid #c0392b; padding: 15px; margin: 20px 0;'>"
            f"<div class='header-doc' style='margin:0; color: #c0392b;'>PRIVREMENA MJERA</div><br>"
            f"<div class='justified'>{mjera_tekst}</div></div>"
            f"<div style='background-color: #f8d7da; border: 1px solid #c0392b; padding: 10px; "
            f"margin: 15px 0; font-size: 10pt;'>"
            f"<b>Napomena:</b> Sukladno Ovršnom zakonu, sud može odrediti privremenu mjeru "
            f"<b>inaudita altera parte</b> (bez saslušanja protivne strane) ako Predlagatelj "
            f"osiguranja učini vjerojatnim da bi obavještavanje Protivnika osiguranja ugrozilo "
            f"provedbu mjere. Žalba protiv rješenja o privremenoj mjeri <b>ne odgađa provedbu "
            f"mjere</b>.</div>"
            f"{troskovnik_html}"
            f"<br><br>"
            f'<table width="100%" border="0"><tr>'
            f'<td width="50%" align="left">U {mjesto}, dana {danas}</td>'
            f'<td width="50%" align="center"><b>PREDLAGATELJ OSIGURANJA</b><br><br><br>______________________</td>'
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
