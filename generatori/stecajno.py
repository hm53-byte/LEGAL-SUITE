# -----------------------------------------------------------------------------
# GENERATORI: Stecajno pravo
# Prijedlog za stecaj, Prijava trazbine, Stecaj potrosaca (osobni bankrot)
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur, format_eur_s_rijecima, formatiraj_troskovnik, u_lokativu


def generiraj_prijedlog_stecaj(predlagatelj, duznik, podaci, troskovi_dict):
    """
    Prijedlog za otvaranje stečajnog postupka.
    Pravni temelj: Stečajni zakon (NN 71/15, 104/17, 36/22)
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        sud = podaci.get("sud", "Zagreb")
        razlog = podaci.get("razlog", "nesposobnost_za_placanje")
        blokada_dana = podaci.get("blokada_dana", 60)
        opis_trazbine = podaci.get("opis_trazbine", "")
        iznos_trazbine = podaci.get("iznos_trazbine", 0)
        predujam = podaci.get("predujam", 0)
        mjesto = podaci.get("mjesto", "Zagreb")

        tvrtka = duznik.get("tvrtka", "")
        oib_duznik = duznik.get("oib", "")
        mbs_duznik = duznik.get("mbs", "")
        sjediste_duznik = duznik.get("sjediste", "")

        if razlog == "nesposobnost_za_placanje":
            razlog_tekst = (
                f"Stečajni dužnik je nesposoban za plaćanje u smislu članka 6. stavka 2. "
                f"Stečajnog zakona (NN 71/15, 104/17, 36/22). Računi dužnika blokirani su neprekidno "
                f"<b>{blokada_dana} dana</b>, što prelazi zakonski minimum od 60 dana neprekidne "
                f"blokade. Dužnik nije u mogućnosti ispunjavati svoje dospjele novčane obveze, "
                f"čime su ispunjene pretpostavke za utvrđenje nesposobnosti za plaćanje."
            )
        else:
            razlog_tekst = (
                f"Stečajni dužnik je prezadužen u smislu članka 6. stavka 3. Stečajnog zakona "
                f"(NN 71/15, 104/17). Imovina dužnika ne pokriva postojeće obveze, odnosno "
                f"pasiva prelazi aktivu dužnika. Računi dužnika blokirani su "
                f"<b>{blokada_dana} dana</b>."
            )

        parts = [
            f'<div style="font-weight: bold; font-size: 14px; text-align: left;">'
            f'TRGOVAČKI SUD U {format_text(sud).upper()}</div><br>',

            f"<div class='party-info'>"
            f"<b>PREDLAGATELJ:</b><br>{predlagatelj}</div>",

            f"<div class='party-info'>"
            f"<b>STEČAJNI DUŽNIK:</b><br>"
            f"<b>{format_text(tvrtka)}</b><br>"
            f"Sjedište: {format_text(sjediste_duznik)}<br>"
            f"OIB: {format_text(oib_duznik)}, MBS: {format_text(mbs_duznik)}</div><br>",

            f"<div class='header-doc'>PRIJEDLOG ZA OTVARANJE STEČAJNOG POSTUPKA</div>",

            f"<div class='justified' style='text-align: center; font-weight: bold; "
            f"margin-bottom: 15px;'>NAD DUŽNIKOM: {format_text(tvrtka)}</div>",

            f"<div class='section-title'>I. PODACI O DUŽNIKU</div>",
            f"<div class='justified'>"
            f"Tvrtka: <b>{format_text(tvrtka)}</b><br>"
            f"OIB: <b>{format_text(oib_duznik)}</b><br>"
            f"MBS: <b>{format_text(mbs_duznik)}</b><br>"
            f"Sjedište: <b>{format_text(sjediste_duznik)}</b></div><br>",

            f"<div class='section-title'>II. STEČAJNI RAZLOG</div>",
            f"<div class='justified'>{razlog_tekst}</div><br>",
        ]

        if opis_trazbine:
            parts.append(
                f"<div class='section-title'>III. TRAŽBINA PREDLAGATELJA</div>"
                f"<div class='justified'>Predlagatelj ima dospjelu tražbinu prema stečajnom "
                f"dužniku kako slijedi:<br><br>"
                f"<b>Opis tražbine:</b> {format_text(opis_trazbine)}<br>"
                f"<b>Iznos tražbine:</b> {format_eur(iznos_trazbine)}<br><br>"
                f"Navedena tražbina je dospjela, a dužnik ju nije podmirio unatoč "
                f"urednim pozivima na plaćanje.</div><br>"
            )
            prijedlog_sekcija = "IV"
        else:
            prijedlog_sekcija = "III"

        parts.append(
            f"<div class='section-title'>{prijedlog_sekcija}. PRIJEDLOG</div>"
            f"<div class='justified'>Na temelju članka 109. Stečajnog zakona (NN 71/15, 104/17, 36/22), "
            f"predlagatelj predlaže da naslovni sud:</div><br>"
            f"<div class='justified'>"
            f"<b>I.</b> Otvori stečajni postupak nad dužnikom <b>{format_text(tvrtka)}</b>, "
            f"OIB: {format_text(oib_duznik)}, sa sjedištem u {format_text(sjediste_duznik)}.<br><br>"
            f"<b>II.</b> Imenuje privremenog stečajnog upravitelja koji će utvrditi imovinu "
            f"dužnika, osigurati očuvanje imovine te ispitati postoje li uvjeti za otvaranje "
            f"stečajnog postupka.<br><br>"
            f"<b>III.</b> Odredi sve mjere osiguranja potrebne za očuvanje imovine dužnika "
            f"do donošenja odluke o otvaranju stečajnog postupka.</div><br>"
        )

        parts.append(troskovnik_html)

        parts.append(
            f"<br><div class='justified' style='border: 1px solid #999; padding: 12px; "
            f"background-color: #f9f9f9; margin-top: 15px;'>"
            f"<b>NAPOMENE:</b><br>"
            f"1. Predujam za troškove stečajnog postupka u iznosu od <b>{format_eur_s_rijecima(predujam)}</b> "
            f"uplaćuje se na račun suda sukladno čl. 110. Stečajnog zakona.<br>"
            f"2. Prilaže se FINA potvrda o blokadi računa dužnika.<br>"
            f"3. Dostava i komunikacija sa sudom obavlja se putem sustava e-Komunikacija.</div>"
        )

        parts.append(
            f"<br><br>"
            f"<div class='justified'><b>PRILOZI:</b><br>"
            f"1. Dokaz o uplati predujma<br>"
            f"2. FINA potvrda o blokadi računa dužnika<br>"
            f"3. Izvadak iz sudskog registra za dužnika<br>"
            f"4. Dokaz o tražbini predlagatelja (ako je vjerovnik)</div>"
        )

        parts.append(
            f"<br><div class='justified'>U {format_text(u_lokativu(mjesto))}, dana {danas}</div><br>"
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>PREDLAGATELJ</b><br>(vlastoručni potpis)</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_prijavu_trazbine(vjerovnik, podaci):
    """
    Prijava tražbine u stečajnom postupku.
    Pravni temelj: Stečajni zakon (NN 71/15, 104/17, 36/22) čl. 173-178
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        stecajni_upravitelj = podaci.get("stecajni_upravitelj", "")
        sud = podaci.get("sud", "Zagreb")
        broj_predmeta = podaci.get("broj_predmeta", "St-___/____")
        duznik_naziv = podaci.get("duznik_naziv", "")
        glavnica = podaci.get("glavnica", 0)
        kamate = podaci.get("kamate", 0)
        troskovi_spora = podaci.get("troskovi_spora", 0)
        ukupno = glavnica + kamate + troskovi_spora
        ima_razlucno_pravo = podaci.get("ima_razlucno_pravo", False)
        razlucno_opis = podaci.get("razlucno_opis", "")
        iban = podaci.get("iban", "")
        mjesto = podaci.get("mjesto", "Zagreb")

        parts = [
            f'<div style="font-weight: bold; font-size: 14px; text-align: left;">'
            f'TRGOVAČKI SUD U {format_text(sud).upper()}</div>',
            f'<div style="text-align: left;">Stečajni upravitelj: '
            f'<b>{format_text(stecajni_upravitelj)}</b></div><br>',

            f'<div style="text-align: right; font-weight: bold; color: red;">'
            f'Broj predmeta: {format_text(broj_predmeta)}</div><br>',

            f"<div class='party-info'>"
            f"<b>VJEROVNIK (podnositelj prijave):</b><br>{vjerovnik}</div>",

            f"<div class='party-info'>"
            f"<b>STEČAJNI DUŽNIK:</b> {format_text(duznik_naziv)}</div><br>",

            f"<div class='header-doc'>PRIJAVA TRAŽBINE U STEČAJNOM POSTUPKU</div>",

            f"<div class='justified'>Na temelju članka 173. Stečajnog zakona (NN 71/15, 104/17, 36/22), "
            f"vjerovnik prijavljuje svoju tražbinu u stečajnom postupku koji se vodi nad "
            f"dužnikom <b>{format_text(duznik_naziv)}</b>, pod brojem predmeta "
            f"<b>{format_text(broj_predmeta)}</b>, kako slijedi:</div><br>",

            f"<div class='section-title'>PREGLED TRAŽBINE</div>",
            f"<table class='cost-table'>",
            f'<tr style="background-color: #f0f0f0; font-weight: bold;">'
            f'<td width="70%" style="padding: 8px;">Vrsta tražbine</td>'
            f'<td width="30%" style="padding: 8px;" align="right">Iznos</td></tr>',
            f'<tr><td style="padding: 8px;">1. Glavnica</td>'
            f'<td style="padding: 8px;" align="right">{format_eur(glavnica)}</td></tr>',
            f'<tr><td style="padding: 8px;">2. Zatezne kamate '
            f'(obračunate do dana otvaranja stečaja)</td>'
            f'<td style="padding: 8px;" align="right">{format_eur(kamate)}</td></tr>',
            f'<tr><td style="padding: 8px;">3. Troškovi spora</td>'
            f'<td style="padding: 8px;" align="right">{format_eur(troskovi_spora)}</td></tr>',
            f'<tr style="font-weight: bold; background-color: #f0f0f0;">'
            f'<td style="padding: 10px;">UKUPNO:</td>'
            f'<td style="padding: 10px;" align="right">{format_eur(ukupno)}</td></tr>',
            f"</table><br>",
        ]

        if ima_razlucno_pravo and razlucno_opis:
            parts.append(
                f"<div class='section-title'>RAZLUČNO PRAVO</div>"
                f"<div class='justified'>Vjerovnik ima razlučno pravo na imovini stečajnog "
                f"dužnika, sukladno članku 177. Stečajnog zakona. Razlučno pravo temelji se "
                f"na sljedećem:<br><br>"
                f"<b>{format_text(razlucno_opis)}</b><br><br>"
                f"Vjerovnik prijavljuje svoju tražbinu kao razlučni vjerovnik te zahtijeva "
                f"odvojeno namirenje iz predmeta na kojem postoji razlučno pravo. Ukoliko se "
                f"vjerovnik ne namiri u cijelosti iz predmeta razlučnog prava, za preostali "
                f"iznos sudjeluje u namirenju kao stečajni vjerovnik.</div><br>"
            )

        if iban:
            parts.append(
                f"<div class='justified' style='border: 1px solid #999; padding: 10px;'>"
                f"<b>IBAN za uplatu:</b> {format_text(iban)}</div><br>"
            )

        parts.append(
            f"<div class='justified' style='border: 1px solid #999; padding: 12px; "
            f"background-color: #f9f9f9;'>"
            f"<b>VAŽNE NAPOMENE:</b><br>"
            f"1. Rok za prijavu tražbine je <b>30 dana</b> od dana objave rješenja o otvaranju "
            f"stečajnog postupka na e-Oglasnoj ploči suda (čl. 173. st. 2. SZ).<br>"
            f"2. Zatezne kamate <b>prestaju teći danom otvaranja stečajnog postupka</b> "
            f"(čl. 167. SZ). Obračun kamata u ovoj prijavi izvršen je zaključno s danom "
            f"koji prethodi danu otvaranja stečajnog postupka.<br>"
            f"3. Tražbine prijavljene nakon isteka roka mogu se ispitati na <b>naknadnom "
            f"ispitnom ročištu</b>, uz obvezu snošenja dodatnih troškova postupka "
            f"(čl. 176. SZ).</div>"
        )

        parts.append(
            f"<br><br><div class='justified'><b>PRILOZI:</b><br>"
            f"1. Dokaz o osnovi tražbine (ugovor, račun, presuda)<br>"
            f"2. Obračun zateznih kamata<br>"
            f"3. Dokaz o razlučnom pravu (ako postoji)<br>"
            f"4. Izvadak iz zemljišne knjige (ako je razlučno pravo hipoteka)</div>"
        )

        parts.append(
            f"<br><div class='justified'>U {format_text(u_lokativu(mjesto))}, dana {danas}</div><br>"
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>VJEROVNIK</b><br>(vlastoručni potpis)</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_stecaj_potrosaca(podnositelj, podaci):
    """
    Prijedlog za stečaj potrošača (osobni bankrot).
    Pravni temelj: Zakon o stečaju potrošača (NN 100/15, 67/18)
    Postupak: FINA Savjetovalište -> Općinski sud
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        ukupni_dug = podaci.get("ukupni_dug", 0)
        broj_vjerovnika = podaci.get("broj_vjerovnika", 0)
        trajanje_blokade_dana = podaci.get("trajanje_blokade_dana", 90)
        popis_vjerovnika = podaci.get("popis_vjerovnika", [])
        popis_imovine = podaci.get("popis_imovine", [])
        mjesecni_prihod = podaci.get("mjesecni_prihod", 0)
        mjesecni_rashod = podaci.get("mjesecni_rashod", 0)
        plan_ispunjenja = podaci.get("plan_ispunjenja", "")
        razlika = mjesecni_prihod - mjesecni_rashod

        parts = [
            f"<div style='text-align: center; font-size: 10pt; font-weight: bold; "
            f"border: 1px solid #cc0000; padding: 8px; margin-bottom: 15px; "
            f"background-color: #fff5f5; color: #cc0000;'>"
            f"NAPOMENA: Prijedlog se najprije podnosi FINA Savjetovalištu za stečaj potrošača, "
            f"a potom Općinskom sudu</div>",

            f'<div style="font-weight: bold; font-size: 14px; text-align: left;">'
            f'FINANCIJSKA AGENCIJA (FINA)</div>'
            f'<div style="text-align: left;">Savjetovalište za stečaj potrošača</div><br>',

            f'<div style="font-weight: bold; font-size: 14px; text-align: left;">'
            f'OPĆINSKI SUD U {format_text(mjesto).upper()}</div><br>',

            f"<div class='party-info'>"
            f"<b>PODNOSITELJ PRIJEDLOGA:</b><br>{podnositelj}</div><br>",

            f"<div class='header-doc'>PRIJEDLOG ZA STEČAJ POTROŠAČA</div>",

            f"<div class='section-title'>I. PODACI O PODNOSITELJU</div>",
            f"<div class='justified'>{podnositelj}<br><br>"
            f"Ukupan iznos dugovanja: <b>{format_eur(ukupni_dug)}</b><br>"
            f"Broj vjerovnika: <b>{broj_vjerovnika}</b><br>"
            f"Trajanje blokade računa: <b>{trajanje_blokade_dana} dana</b></div><br>",
        ]

        # II. POPIS VJEROVNIKA
        parts.append(
            f"<div class='section-title'>II. POPIS VJEROVNIKA I DUGOVANJA</div>"
        )
        if popis_vjerovnika:
            parts.append(
                f"<table class='cost-table'>"
                f'<tr style="background-color: #f0f0f0; font-weight: bold;">'
                f'<td width="10%" style="padding: 8px;" align="center">R.br.</td>'
                f'<td width="55%" style="padding: 8px;">Naziv vjerovnika</td>'
                f'<td width="35%" style="padding: 8px;" align="right">Iznos dugovanja</td></tr>'
            )
            ukupno_vjerovnici = 0
            for i, v in enumerate(popis_vjerovnika, 1):
                naziv = v.get("naziv", "")
                iznos = v.get("iznos", 0)
                ukupno_vjerovnici += iznos
                parts.append(
                    f'<tr><td style="padding: 6px;" align="center">{i}.</td>'
                    f'<td style="padding: 6px;">{format_text(naziv)}</td>'
                    f'<td style="padding: 6px;" align="right">{format_eur(iznos)}</td></tr>'
                )
            parts.append(
                f'<tr style="font-weight: bold; background-color: #f0f0f0;">'
                f'<td colspan="2" style="padding: 10px;">UKUPNO:</td>'
                f'<td style="padding: 10px;" align="right">{format_eur(ukupno_vjerovnici)}</td></tr>'
                f"</table><br>"
            )
        else:
            parts.append(
                f"<div class='justified'><i>Popis vjerovnika nije unesen.</i></div><br>"
            )

        # III. POPIS IMOVINE
        parts.append(
            f"<div class='section-title'>III. POPIS IMOVINE</div>"
        )
        if popis_imovine:
            parts.append(
                f"<table class='cost-table'>"
                f'<tr style="background-color: #f0f0f0; font-weight: bold;">'
                f'<td width="10%" style="padding: 8px;" align="center">R.br.</td>'
                f'<td width="55%" style="padding: 8px;">Opis imovine</td>'
                f'<td width="35%" style="padding: 8px;" align="right">Procijenjena vrijednost</td></tr>'
            )
            ukupno_imovina = 0
            for i, im in enumerate(popis_imovine, 1):
                opis = im.get("opis", "")
                vrijednost = im.get("vrijednost", 0)
                ukupno_imovina += vrijednost
                parts.append(
                    f'<tr><td style="padding: 6px;" align="center">{i}.</td>'
                    f'<td style="padding: 6px;">{format_text(opis)}</td>'
                    f'<td style="padding: 6px;" align="right">{format_eur(vrijednost)}</td></tr>'
                )
            parts.append(
                f'<tr style="font-weight: bold; background-color: #f0f0f0;">'
                f'<td colspan="2" style="padding: 10px;">UKUPNO:</td>'
                f'<td style="padding: 10px;" align="right">{format_eur(ukupno_imovina)}</td></tr>'
                f"</table><br>"
            )
        else:
            parts.append(
                f"<div class='justified'><i>Podnositelj nema imovine.</i></div><br>"
            )

        # IV. FINANCIJSKO STANJE
        parts.append(
            f"<div class='section-title'>IV. FINANCIJSKO STANJE</div>"
            f"<table class='cost-table'>"
            f'<tr><td width="70%" style="padding: 8px;">Mjesečni prihodi:</td>'
            f'<td width="30%" style="padding: 8px;" align="right">{format_eur(mjesecni_prihod)}</td></tr>'
            f'<tr><td style="padding: 8px;">Mjesečni rashodi (nužni životni troškovi):</td>'
            f'<td style="padding: 8px;" align="right">{format_eur(mjesecni_rashod)}</td></tr>'
            f'<tr style="font-weight: bold; background-color: #f0f0f0;">'
            f'<td style="padding: 10px;">Razlika (raspoloživo za namirenje):</td>'
            f'<td style="padding: 10px;" align="right">{format_eur(razlika)}</td></tr>'
            f"</table><br>"
        )

        # V. PLAN ISPUNJENJA
        parts.append(
            f"<div class='section-title'>V. PLAN ISPUNJENJA OBVEZA</div>"
            f"<div class='justified'>Sukladno članku 18. Zakona o stečaju potrošača "
            f"(NN 100/15, 67/18), podnositelj predlaže sljedeći plan ispunjenja obveza:<br><br>"
            f"{format_text(plan_ispunjenja)}</div><br>"
        )

        # VI. IZJAVA O ISTINITOSTI
        parts.append(
            f"<div class='section-title'>VI. IZJAVA O ISTINITOSTI PODATAKA</div>"
            f"<div class='justified' style='border: 2px solid #cc0000; padding: 12px; "
            f"background-color: #fff5f5;'>"
            f"Pod kaznenom i materijalnom odgovornošću izjavljujem da su svi podaci "
            f"navedeni u ovom prijedlogu istiniti i potpuni. Svjestan/svjesna sam da "
            f"davanje lažnih podataka u postupku stečaja potrošača predstavlja kazneno "
            f"djelo sukladno članku 283. Kaznenog zakona (lažni stečaj) te da za isto "
            f"mogu kazneno odgovarati.</div><br>"
        )

        parts.append(
            f"<div class='justified' style='border: 1px solid #999; padding: 12px; "
            f"background-color: #f9f9f9;'>"
            f"<b>UVJETI ZA STEČAJ POTROŠAČA:</b><br>"
            f"1. Minimalni iznos dugovanja: <b>3.981,68 EUR</b> (protuvrijednost 30.000,00 HRK)<br>"
            f"2. Trajanje blokade računa: <b>najmanje 90 uzastopnih dana</b><br>"
            f"3. Otvaranjem stečaja potrošač <b>gubi pravo raspolaganja imovinom</b> - "
            f"upravljanje preuzima povjerenik<br>"
            f"4. Razdoblje ispunjenja obveza traje do <b>5 godina</b> od dana pravomoćnosti "
            f"rješenja o oslobođenju od preostalih obveza<br>"
            f"5. Postupak se pokreće podnošenjem prijedloga <b>FINA Savjetovalištu</b> "
            f"za stečaj potrošača</div>"
        )

        parts.append(
            f"<br><br><div class='justified'><b>PRILOZI:</b><br>"
            f"1. Potvrda FINA-e o provedenom postupku savjetovanja<br>"
            f"2. FINA potvrda o blokadi računa<br>"
            f"3. Popis svih vjerovnika s iznosima i rokovima dospijeća<br>"
            f"4. Popis imovine s procjenama vrijednosti<br>"
            f"5. Potvrda o prihodima (platna lista / rješenje HZMO-a)<br>"
            f"6. Plan ispunjenja obveza</div>"
        )

        parts.append(
            f"<br><div class='justified'>U {format_text(u_lokativu(mjesto))}, dana {danas}</div><br>"
            f"<div class='signature-row'>"
            f"<div class='signature-block'><b>PODNOSITELJ</b><br>(vlastoručni potpis)</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
