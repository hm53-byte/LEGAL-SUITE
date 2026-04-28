# -----------------------------------------------------------------------------
# GENERATORI: Ugovorno/Obvezno pravo
# Darovanje, Cesija, Kompenzacija, Jamstvo, Gradenje, Licencija, Posredovanje,
# Sporazumni raskid
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur, format_eur_s_rijecima, _rimski_broj, u_lokativu


def generiraj_darovanje(darovatelj, obdarenik, podaci):
    """
    Ugovor o darovanju - ZOO čl. 479-498
    ZAHTIJEVANA FORMA: ovisi o predmetu darovanja
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        predmet_tip = podaci.get("predmet_tip", "pokretnina_s_predajom")
        predmet_opis = podaci.get("predmet_opis", "")
        vrijednost = podaci.get("vrijednost", 0)
        dozivotno_uzivanje = podaci.get("dozivotno_uzivanje", False)

        # ZK podaci za nekretninu
        ko = podaci.get("ko", "")
        ulozak = podaci.get("ulozak", "")
        cestica = podaci.get("cestica", "")
        opis_nekretnine = podaci.get("opis", "")
        povrsina = podaci.get("povrsina", "")

        # Forma
        if predmet_tip == "nekretnina":
            forma_tekst = "JAVNOBILJEŽNIČKI AKT ILI SOLEMNIZACIJA"
        elif predmet_tip == "obećanje_darovanja":
            forma_tekst = "JAVNOBILJEŽNIČKI AKT"
        else:
            forma_tekst = "PISANA (nije zakonski obvezna)"

        clanak = 1
        parts = [
            "<div style='text-align: center; font-size: 10pt; font-weight: bold; "
            "border: 1px solid black; padding: 8px; margin-bottom: 20px;'>"
            f"ZAHTIJEVANA FORMA: {forma_tekst}</div>",
            "<div class='header-doc'>UGOVOR O DAROVANJU</div>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {danas} godine, između:</div><br>",
            f"<div class='party-info'><b>1. DAROVATELJ:</b><br>{darovatelj}</div>",
            f"<div class='party-info'><b>2. OBDARENIK:</b><br>{obdarenik}</div><br>",
        ]

        # Članak - Predmet darovanja
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Predmet darovanja)</div>"
            f"<div class='justified'>Darovatelj je isključivi vlasnik sljedećeg predmeta darovanja:<br><br>"
            f"<b>{format_text(predmet_opis)}</b>"
        )
        if predmet_tip == "nekretnina":
            parts.append(
                f"<br><br><b>Zemljišnoknjižni podaci:</b><br>"
                f"Katastarska općina: <b>{format_text(ko)}</b><br>"
                f"Zemljišnoknjižni uložak: <b>{format_text(ulozak)}</b><br>"
                f"Katastarska čestica: <b>{format_text(cestica)}</b><br>"
                f"Opis: {format_text(opis_nekretnine)}<br>"
                f"Površina: <b>{format_text(povrsina)}</b>"
            )
        if vrijednost:
            parts.append(f"<br><br>Procijenjena vrijednost predmeta darovanja iznosi <b>{format_eur_s_rijecima(vrijednost)}</b>.")
        parts.append("</div><br>")
        clanak += 1

        # Članak - Animus donandi
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Animus donandi)</div>"
            f"<div class='justified'>Darovatelj izjavljuje da bezuvjetno i neopozivo, iz čiste darežljivosti "
            f"(animus donandi), daruje Obdareniku predmet darovanja opisan u članku 1. ovog Ugovora, "
            f"a Obdarenik izjavljuje da dar prima.<br><br>"
            f"Darovanje se čini bez ikakve protučinidbe Obdarenika.</div><br>"
        )
        clanak += 1

        # Clausula intabulandi (za nekretninu)
        if predmet_tip == "nekretnina":
            parts.append(
                f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Clausula intabulandi)</div>"
                f"<div class='clausula'>Darovatelj ovime daje izričitu, bezuvjetnu i neopozivo "
                f"zemljišnoknjižnu dozvolu (clausula intabulandi) te dopušta da se na temelju ovog Ugovora "
                f"u zemljišnoj knjizi kod nadležnog Općinskog suda, na nekretnini opisanoj u članku 1. ovog Ugovora, "
                f"izvrši uknjižba prava vlasništva u korist Obdarenika, bez daljnjeg pitanja "
                f"i odobrenja Darovatelja.</div><br>"
            )
            clanak += 1

        # Uvjeti/nalozi
        if dozivotno_uzivanje:
            parts.append(
                f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Uvjeti i nalozi)</div>"
                f"<div class='justified'>Obdarenik prihvaća i obvezuje se da Darovatelj zadržava pravo "
                f"doživotnog uživanja (plodouživanja) na predmetu darovanja iz članka 1. ovog Ugovora. "
                f"Obdarenik dopušta uknjižbu prava plodouživanja u korist Darovatelja.<br><br>"
                f"Ovo pravo prestaje smrću Darovatelja.</div><br>"
            )
            clanak += 1

        # Opoziv darovanja
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Opoziv darovanja)</div>"
            f"<div class='justified'>Darovatelj može opozvati darovanje sukladno odredbama Zakona o "
            f"obveznim odnosima (ZOO), i to u sljedećim slučajevima:<br><br>"
            f"a) <b>zbog osiromašenja</b> — ako nakon izvršenog darovanja Darovatelj toliko osiromaši da nema "
            f"sredstava za nužno uzdržavanje (čl. 493. ZOO);<br>"
            f"b) <b>zbog grube nezahvalnosti</b> — ako se Obdarenik ponaša grubo nezahvalno prema Darovatelju "
            f"ili članovima njegove obitelji (čl. 494. ZOO).<br><br>"
            f"Pravo na opoziv zastarijeva u roku od jedne godine od dana saznanja za razlog opoziva.</div><br>"
        )
        clanak += 1

        # Troškovi i porezi
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Troškovi i porezi)</div>"
            f"<div class='justified'>Troškove solemnizacije/ovjere ovog Ugovora snosi Obdarenik, "
            f"osim ako se strane ne dogovore drugačije.<br><br>"
            f"Porez na promet nekretnina ili porez na darove plaća Obdarenik, "
            f"uz napomenu da su darovanja u pravnoj liniji (bračni drug, potomci, preci) "
            f"oslobođena poreza na promet nekretnina sukladno Zakonu o porezu na promet nekretnina.</div><br>"
        )
        clanak += 1

        # Završne odredbe
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Završne odredbe)</div>"
            f"<div class='justified'>Na sva pitanja koja nisu uređena ovim Ugovorom primjenjuju se "
            f"odredbe Zakona o obveznim odnosima (NN 35/05, 41/08, 125/11, 78/15, 29/18, 126/21, 114/22, 156/22, 155/23), "
            f"posebice odredbe o ugovoru o darovanju (čl. 479.-498.).<br><br>"
            f"Ovaj Ugovor sastavljen je u potrebnom broju primjeraka.</div><br>"
        )

        # Potpisi
        parts.append(
            "<div class='signature-row'>"
            "<div class='signature-block'><b>DAROVATELJ</b><br><br><br>______________________</div>"
            "<div class='signature-block'><b>OBDARENIK</b><br><br><br>______________________</div></div>"
        )

        # JB ovjera za nekretninu
        if predmet_tip == "nekretnina":
            parts.append(
                "<br><div style='border: 2px solid black; padding: 15px; margin-top: 30px;'>"
                "<div class='section-title' style='text-align: center;'>"
                "PROSTOR ZA JAVNOBILJEŽNIČKU OVJERU / SOLEMNIZACIJU</div>"
                "<div class='justified' style='font-size: 10pt;'>"
                "Ovaj Ugovor solemniziran je / sastavljen kao javnobilježnički akt "
                "od strane javnog bilježnika _________________________, "
                "pod brojem OV-_____/______, dana ____________.<br><br>"
                "Javni bilježnik: ______________________<br>"
                "Pečat i potpis</div></div>"
            )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_cesiju(cedent, cesionar, podaci):
    """
    Ugovor o cesiji (prijenos tražbine) - ZOO čl. 80-89
    ZAHTIJEVANA FORMA: PISANA
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        duznik_naziv = podaci.get("duznik_naziv", "")
        duznik_oib = podaci.get("duznik_oib", "")
        iznos_trazbine = podaci.get("iznos_trazbine", 0)
        temelj_trazbine = podaci.get("temelj_trazbine", "")
        datum_dospijeca = podaci.get("datum_dospijeca", "")
        naplatna = podaci.get("naplatna", True)
        naknada = podaci.get("naknada", 0)
        jamci_veritet = podaci.get("jamci_veritet", True)
        jamci_bonitet = podaci.get("jamci_bonitet", False)

        clanak = 1
        parts = [
            "<div style='text-align: center; font-size: 10pt; font-weight: bold; "
            "border: 1px solid black; padding: 8px; margin-bottom: 20px;'>"
            "ZAHTIJEVANA FORMA: PISANA</div>",
            "<div class='header-doc'>UGOVOR O CESIJI<br>"
            "<span style='font-size: 12pt; font-weight: normal;'>"
            "(Prijenos tražbine)</span></div>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {danas} godine, između:</div><br>",
            f"<div class='party-info'><b>1. CEDENT (ustupatelj tražbine):</b><br>{cedent}</div>",
            f"<div class='party-info'><b>2. CESIONAR (primatelj tražbine):</b><br>{cesionar}</div><br>",
        ]

        # Članak - Predmet cesije
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Predmet cesije)</div>"
            f"<div class='justified'>Cedent ovim Ugovorom ustupa (cedira) Cesionaru svoju tražbinu prema "
            f"dužniku (cesus):<br><br>"
            f"<b>Dužnik (cesus):</b> {format_text(duznik_naziv)}, OIB: {format_text(duznik_oib)}<br><br>"
            f"<b>Iznos tražbine:</b> {format_eur(iznos_trazbine)}<br>"
            f"<b>Temelj tražbine:</b> {format_text(temelj_trazbine)}<br>"
            f"<b>Datum dospijeća:</b> {format_text(datum_dospijeca)}</div><br>"
        )
        clanak += 1

        # Članak - Trenutak prijenosa i sporedna prava
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Trenutak prijenosa i sporedna prava)</div>"
            f"<div class='justified'>Tražbina prelazi na Cesionara danom potpisa ovog Ugovora.<br><br>"
            f"Prijenosom tražbine na Cesionara prelaze i sva sporedna prava koja su s njom povezana, "
            f"uključujući:<br><br>"
            f"a) pravo na kamate (ugovorne i zatezne);<br>"
            f"b) hipoteke i založna prava koja osiguravaju tražbinu;<br>"
            f"c) prava iz jamstava (osobnih i stvarnih);<br>"
            f"d) zadužnice i bjanko zadužnice;<br>"
            f"e) ostala sporedna prava sukladno čl. 84. ZOO.</div><br>"
        )
        clanak += 1

        # Članak - Naknada (ako je naplatna)
        if naplatna:
            parts.append(
                f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Naknada)</div>"
                f"<div class='justified'>Za ustupljenu tražbinu Cesionar se obvezuje Cedentu isplatiti "
                f"naknadu u iznosu od <b>{format_eur_s_rijecima(naknada)}</b>.<br><br>"
                f"Naknada se plaća u roku od 8 (osam) dana od dana potpisa ovog Ugovora, "
                f"na račun Cedenta.</div><br>"
            )
            clanak += 1

        # Članak - Izjave cedenta
        jamstvo_veritet_tekst = (
            "Cedent jamči za <b>veritet</b> (istinitost, pravovaljanost i naplativost) ustupljene tražbine, "
            "odnosno jamči da tražbina pravno postoji, da je nesporna i da nije zastarjela."
            if jamci_veritet
            else "Cedent <b>ne jamči</b> za veritet (istinitost) ustupljene tražbine."
        )
        jamstvo_bonitet_tekst = (
            "<br>Cedent jamči i za <b>bonitet</b> (solventnost) dužnika u trenutku sklapanja ovog Ugovora."
            if jamci_bonitet
            else "<br>Cedent <b>ne jamči</b> za bonitet (solventnost) dužnika."
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Izjave cedenta)</div>"
            f"<div class='justified'>{jamstvo_veritet_tekst}{jamstvo_bonitet_tekst}<br><br>"
            f"Cedent izjavljuje da tražbinu nije prethodno ustupio trećoj osobi niti je opteretio "
            f"zalogom ili drugim pravima trećih.</div><br>"
        )
        clanak += 1

        # Članak - Obveza notifikacije dužnika
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Obveza notifikacije dužnika)</div>"
            f"<div class='justified'><b>Cedent se obvezuje bez odgode obavijestiti dužnika "
            f"({format_text(duznik_naziv)}) o izvršenom prijenosu tražbine</b>, sukladno čl. 82. ZOO.<br><br>"
            f"Dok dužnik ne bude obaviješten o prijenosu, on se oslobađa obveze ispunjenjem Cedentu. "
            f"Nakon primitka obavijesti, dužnik je dužan ispuniti obvezu isključivo Cesionaru.<br><br>"
            f"Ugovorne strane suglasno utvrđuju da Cesionar ima pravo i sam obavijestiti dužnika "
            f"o izvršenom prijenosu, uz predočenje ovjerenog primjerka ovog Ugovora.</div><br>"
        )
        clanak += 1

        # Završne odredbe
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Završne odredbe)</div>"
            f"<div class='justified'>Na sva pitanja koja nisu uređena ovim Ugovorom primjenjuju se "
            f"odredbe Zakona o obveznim odnosima (NN 35/05, 41/08, 125/11, 78/15, 29/18, 126/21, 114/22, 156/22, 155/23), "
            f"posebice odredbe o ustupanju tražbine (čl. 80.-89.).<br><br>"
            f"Ovaj Ugovor sastavljen je u 3 (tri) istovjetna primjerka — po jedan za svaku ugovornu stranu "
            f"te jedan za dostavu dužniku.</div><br>"
        )

        # Potpisi
        parts.append(
            "<div class='signature-row'>"
            "<div class='signature-block'><b>CEDENT</b><br><br><br>______________________</div>"
            "<div class='signature-block'><b>CESIONAR</b><br><br><br>______________________</div></div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_kompenzaciju(strana_a, strana_b, podaci):
    """
    Sporazum o kompenzaciji (prijeboj) - ZOO čl. 195-202
    ZAHTIJEVANA FORMA: PISANA
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        obveze_a = podaci.get("obveze_a", [])
        obveze_b = podaci.get("obveze_b", [])
        iznos_kompenzacije = podaci.get("iznos_kompenzacije", 0)
        preostali_saldo = podaci.get("preostali_saldo", 0)
        datum_kompenzacije = podaci.get("datum_kompenzacije", danas)

        clanak = 1
        parts = [
            "<div style='text-align: center; font-size: 10pt; font-weight: bold; "
            "border: 1px solid black; padding: 8px; margin-bottom: 20px;'>"
            "ZAHTIJEVANA FORMA: PISANA</div>",
            "<div class='header-doc'>SPORAZUM O KOMPENZACIJI<br>"
            "<span style='font-size: 12pt; font-weight: normal;'>"
            "(Prijeboj)</span></div>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {danas} godine, između:</div><br>",
            f"<div class='party-info'><b>1. STRANA A:</b><br>{strana_a}</div>",
            f"<div class='party-info'><b>2. STRANA B:</b><br>{strana_b}</div><br>",
        ]

        # Članak - Utvrđenje uzajamnih obveza
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Utvrđenje uzajamnih obveza)</div>"
            f"<div class='justified'>Ugovorne strane suglasno utvrđuju sljedeće uzajamne obveze:</div><br>"
        )

        # Tablica A -> B
        ukupno_a = sum(o.get("iznos", 0) for o in obveze_a)
        parts.append(
            f"<div class='justified'><b>Obveze Strane A prema Strani B:</b></div>"
            f"<table width='100%' style='border-collapse: collapse; margin: 10px 0;'>"
            f"<tr style='background-color: #f0f0f0; font-weight: bold;'>"
            f"<td style='border: 1px solid #999; padding: 6px;' width='70%'>Opis (račun)</td>"
            f"<td style='border: 1px solid #999; padding: 6px; text-align: right;' width='30%'>Iznos</td></tr>"
        )
        for o in obveze_a:
            parts.append(
                f"<tr><td style='border: 1px solid #999; padding: 6px;'>{format_text(o.get('opis', ''))}</td>"
                f"<td style='border: 1px solid #999; padding: 6px; text-align: right;'>{format_eur(o.get('iznos', 0))}</td></tr>"
            )
        parts.append(
            f"<tr style='font-weight: bold; background-color: #f0f0f0;'>"
            f"<td style='border: 1px solid #999; padding: 6px;'>UKUPNO:</td>"
            f"<td style='border: 1px solid #999; padding: 6px; text-align: right;'>{format_eur(ukupno_a)}</td></tr>"
            f"</table><br>"
        )

        # Tablica B -> A
        ukupno_b = sum(o.get("iznos", 0) for o in obveze_b)
        parts.append(
            f"<div class='justified'><b>Obveze Strane B prema Strani A:</b></div>"
            f"<table width='100%' style='border-collapse: collapse; margin: 10px 0;'>"
            f"<tr style='background-color: #f0f0f0; font-weight: bold;'>"
            f"<td style='border: 1px solid #999; padding: 6px;' width='70%'>Opis (račun)</td>"
            f"<td style='border: 1px solid #999; padding: 6px; text-align: right;' width='30%'>Iznos</td></tr>"
        )
        for o in obveze_b:
            parts.append(
                f"<tr><td style='border: 1px solid #999; padding: 6px;'>{format_text(o.get('opis', ''))}</td>"
                f"<td style='border: 1px solid #999; padding: 6px; text-align: right;'>{format_eur(o.get('iznos', 0))}</td></tr>"
            )
        parts.append(
            f"<tr style='font-weight: bold; background-color: #f0f0f0;'>"
            f"<td style='border: 1px solid #999; padding: 6px;'>UKUPNO:</td>"
            f"<td style='border: 1px solid #999; padding: 6px; text-align: right;'>{format_eur(ukupno_b)}</td></tr>"
            f"</table><br>"
        )
        clanak += 1

        # Članak - Kompenzacija
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Kompenzacija)</div>"
            f"<div class='justified'>Ugovorne strane suglasno provode prijeboj (kompenzaciju) uzajamnih "
            f"tražbina s učinkom od <b>{format_text(datum_kompenzacije)}</b>.<br><br>"
            f"<b>Iznos kompenzacije:</b> {format_eur(iznos_kompenzacije)}<br>"
            f"<b>Preostali saldo:</b> {format_eur(preostali_saldo)}</div><br>"
        )
        clanak += 1

        # Završne odredbe
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Završne odredbe)</div>"
            f"<div class='justified'>Nakon provedene kompenzacije, strana koja duguje preostali saldo "
            f"obvezuje se isti podmiriti u roku od 8 (osam) dana od dana potpisa ovog Sporazuma.<br><br>"
            f"Na ovaj Sporazum primjenjuju se odredbe Zakona o obveznim odnosima o prijeboju "
            f"(čl. 195.-202.).<br><br>"
            f"Ovaj Sporazum sastavljen je u 2 (dva) istovjetna primjerka, po jedan za svaku stranu.</div><br>"
        )

        # Potpisi
        parts.append(
            "<div class='signature-row'>"
            "<div class='signature-block'><b>STRANA A</b><br><br><br>______________________</div>"
            "<div class='signature-block'><b>STRANA B</b><br><br><br>______________________</div></div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_jamstvo(vjerovnik, jamac, podaci):
    """
    Ugovor o jamstvu - ZOO čl. 104-126
    ZAHTIJEVANA FORMA: ovisi o vrsti jamstva
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        glavni_duznik = podaci.get("glavni_duznik", "")
        broj_ugovora_kredita = podaci.get("broj_ugovora_kredita", "")
        iznos_duga = podaci.get("iznos_duga", 0)
        valuta = podaci.get("valuta", "EUR")
        kamatna_stopa = podaci.get("kamatna_stopa", "")
        vrsta = podaci.get("vrsta", "obicno")

        if vrsta == "jamac_platac":
            forma_tekst = "SOLEMNIZACIJA S OVRŠNOM KLAUZULOM"
        else:
            forma_tekst = "PISANA"

        clanak = 1
        parts = [
            "<div style='text-align: center; font-size: 10pt; font-weight: bold; "
            "border: 1px solid black; padding: 8px; margin-bottom: 20px;'>"
            f"ZAHTIJEVANA FORMA: {forma_tekst}</div>",
            "<div class='header-doc'>UGOVOR O JAMSTVU</div>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {danas} godine, između:</div><br>",
            f"<div class='party-info'><b>1. VJEROVNIK:</b><br>{vjerovnik}</div>",
            f"<div class='party-info'><b>2. JAMAC:</b><br>{jamac}</div><br>",
        ]

        # Članak - Stranke i identifikacija glavnog duga
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Stranke i identifikacija glavnog duga)</div>"
            f"<div class='justified'>Ugovorne strane utvrđuju da između Vjerovnika i glavnog dužnika:<br><br>"
            f"<b>Glavni dužnik:</b> {format_text(glavni_duznik)}<br><br>"
            f"postoji obveza iz ugovora broj <b>{format_text(broj_ugovora_kredita)}</b> "
            f"u iznosu od <b>{format_eur_s_rijecima(iznos_duga)}</b>"
        )
        if kamatna_stopa:
            parts.append(f", uz ugovorenu kamatnu stopu od <b>{format_text(kamatna_stopa)}</b>")
        parts.append(".</div><br>")
        clanak += 1

        # Članak - Izjava o jamčenju
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Izjava o jamčenju)</div>"
            f"<div class='justified'>Jamac izjavljuje da preuzima jamstvo za ispunjenje obveze "
            f"glavnog dužnika iz članka 1. ovog Ugovora, u cijelosti, uključujući glavnicu, "
            f"kamate, troškove te eventualne naknade štete.</div><br>"
        )
        clanak += 1

        # Članak - Vrsta jamstva
        if vrsta == "jamac_platac":
            vrsta_opis = (
                "Jamac preuzima jamstvo kao <b>JAMAC PLATAC</b> (solidarni jamac) sukladno čl. 111. ZOO.<br><br>"
                "Jamac platac odgovara Vjerovniku kao glavni dužnik za cijelu obvezu i "
                "Vjerovnik može zahtijevati ispunjenje od Jamca platca i prije nego što zatraži "
                "ispunjenje od glavnog dužnika.<br><br>"
                "Jamac platac nema pravo na beneficij reda (beneficium ordinis), "
                "tj. ne može zahtijevati da se Vjerovnik najprije naplati od glavnog dužnika."
            )
        else:
            vrsta_opis = (
                "Jamac preuzima <b>OBIČNO JAMSTVO</b> (supsidijarno) sukladno čl. 104. ZOO.<br><br>"
                "Jamac ima pravo na beneficij reda (beneficium ordinis), tj. može zahtijevati "
                "da Vjerovnik najprije pokuša naplatiti svoju tražbinu od glavnog dužnika, "
                "pa tek onda od Jamca.<br><br>"
                "Jamac ima pravo na beneficij podjele (beneficium divisionis) ako postoji "
                "više jamaca za istu obvezu."
            )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Vrsta jamstva)</div>"
            f"<div class='justified'>{vrsta_opis}</div><br>"
        )
        clanak += 1

        # Ovršna klauzula (za jamca platca)
        if vrsta == "jamac_platac":
            parts.append(
                f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Ovršna klauzula)</div>"
                f"<div class='justified'>Jamac platac izričito, bezuvjetno i neopozivo pristaje i dopušta da se "
                f"radi naplate dospjele, a neplaćene tražbine iz ovog Ugovora, neposredno "
                f"na temelju ovog Ugovora kao ovršne isprave, provede prisilna ovrha na svim "
                f"njegovim računima kod banaka te na cjelokupnoj pokretnoj i nepokretnoj imovini, "
                f"uključujući pljenidbu i prijenos novčanih sredstava, zapljenu pokretnina "
                f"i prodaju nekretnina.<br><br>"
                f"Ovaj Ugovor ima snagu ovršne isprave sukladno čl. 54. Ovršnog zakona.</div><br>"
            )
            clanak += 1

        # Troškovi
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Troškovi)</div>"
            f"<div class='justified'>Troškove solemnizacije ovog Ugovora snosi Jamac.</div><br>"
        )
        clanak += 1

        # Završne odredbe
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Završne odredbe)</div>"
            f"<div class='justified'>Na sva pitanja koja nisu uređena ovim Ugovorom primjenjuju se "
            f"odredbe Zakona o obveznim odnosima (NN 35/05, 41/08, 125/11, 78/15, 29/18, 126/21, 114/22, 156/22, 155/23), "
            f"posebice odredbe o jamstvu (čl. 104.-126.).<br><br>"
            f"Ovaj Ugovor sastavljen je u 3 (tri) istovjetna primjerka.</div><br>"
        )

        # Potpisi
        parts.append(
            "<div class='signature-row'>"
            "<div class='signature-block'><b>VJEROVNIK</b><br><br><br>______________________</div>"
            "<div class='signature-block'><b>JAMAC</b><br><br><br>______________________</div></div>"
        )

        # JB ovjera za jamca platca
        if vrsta == "jamac_platac":
            parts.append(
                "<br><div style='border: 2px solid black; padding: 15px; margin-top: 30px;'>"
                "<div class='section-title' style='text-align: center;'>"
                "PROSTOR ZA JAVNOBILJEŽNIČKU SOLEMNIZACIJU</div>"
                "<div class='justified' style='font-size: 10pt;'>"
                "Ovaj Ugovor solemniziran je od strane javnog bilježnika "
                "_________________________, pod brojem OV-_____/______, dana ____________.<br><br>"
                "Potvrđuje se da je Jamac upozoren na pravne posljedice ovršne klauzule.<br><br>"
                "Javni bilježnik: ______________________<br>"
                "Pečat i potpis</div></div>"
            )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_ugovor_o_gradenju(narucitelj, izvodac, podaci):
    """
    Ugovor o građenju - ZOO čl. 620-636
    ZAHTIJEVANA FORMA: PISANA (ZOO čl. 620 - ništetnost bez pisanog oblika)
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        predmet_radova = podaci.get("predmet_radova", "")
        gradevinska_dozvola = podaci.get("gradevinska_dozvola", "")
        projekt = podaci.get("projekt", "")
        rok_uvodenja = podaci.get("rok_uvodenja", "")
        medurokovi = podaci.get("medurokovi", "")
        rok_zavrsetka = podaci.get("rok_zavrsetka", "")
        vrsta_cijene = podaci.get("vrsta_cijene", "kljuc_u_ruke")
        cijena = podaci.get("cijena", 0)
        jamstveni_rok = podaci.get("jamstveni_rok", "2 godine")
        bankarska_garancija = podaci.get("bankarska_garancija", "")

        clanak = 1
        parts = [
            "<div style='text-align: center; font-size: 10pt; font-weight: bold; "
            "border: 1px solid black; padding: 8px; margin-bottom: 20px;'>"
            "ZAHTIJEVANA FORMA: PISANA (ZOO čl. 620 — ništetnost bez pisanog oblika)</div>",
            "<div class='header-doc'>UGOVOR O GRAĐENJU</div>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {danas} godine, između:</div><br>",
            f"<div class='party-info'><b>1. NARUČITELJ (investitor):</b><br>{narucitelj}</div>",
            f"<div class='party-info'><b>2. IZVOĐAČ:</b><br>{izvodac}</div><br>",
        ]

        # Članak - Predmet
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Predmet ugovora)</div>"
            f"<div class='justified'>Izvođač se obvezuje izvesti sljedeće radove:<br><br>"
            f"<b>{format_text(predmet_radova)}</b><br><br>"
            f"Radovi se izvode temeljem:<br>"
            f"— Građevinska dozvola: <b>{format_text(gradevinska_dozvola)}</b><br>"
            f"— Glavni projekt: <b>{format_text(projekt)}</b><br><br>"
            f"Glavni projekt čini sastavni dio ovog Ugovora.</div><br>"
        )
        clanak += 1

        # Članak - Rokovi
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Rokovi)</div>"
            f"<div class='justified'>"
            f"<b>Uvođenje u posao:</b> {format_text(rok_uvodenja)}<br><br>"
        )
        if medurokovi:
            parts.append(f"<b>Međurokovi:</b><br>{format_text(medurokovi)}<br><br>")
        parts.append(
            f"<b>Rok završetka radova:</b> {format_text(rok_zavrsetka)}<br><br>"
            f"U slučaju prekoračenja roka završetka radova, Izvođač je dužan platiti Naručitelju "
            f"ugovornu kaznu u iznosu od 1‰ (jedan promil) ugovorene cijene za svaki dan zakašnjenja, "
            f"ali ne više od 5% ukupne ugovorene cijene.</div><br>"
        )
        clanak += 1

        # Članak - Cijena i obračun
        if vrsta_cijene == "kljuc_u_ruke":
            cijena_opis = (
                f"Cijena radova ugovorena je kao cijena po sustavu <b>\"ključ u ruke\"</b> "
                f"i iznosi <b>{format_eur(cijena)}</b> (bez PDV-a).<br><br>"
                f"Cijena \"ključ u ruke\" obuhvaća sve radove potrebne za potpuno dovršenje građevine "
                f"sukladno glavnom projektu, uključujući i radove koji nisu izričito navedeni u troškovniku "
                f"ali su nužni za funkcionalno dovršenje objekta.<br><br>"
                f"Izvođač snosi rizik većeg opsega radova od predviđenog."
            )
        else:
            cijena_opis = (
                f"Cijena radova obračunava se po <b>jediničnim cijenama</b> iz troškovnika "
                f"koji čini sastavni dio ovog Ugovora.<br><br>"
                f"Procijenjeni ukupni iznos radova: <b>{format_eur(cijena)}</b> (bez PDV-a).<br><br>"
                f"Konačna cijena utvrdit će se obračunom stvarno izvedenih količina "
                f"prema jediničnim cijenama iz troškovnika."
            )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Cijena i obračun)</div>"
            f"<div class='justified'>{cijena_opis}</div><br>"
        )
        clanak += 1

        # Članak - Jamstva i osiguranja
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Jamstva i osiguranja)</div>"
            f"<div class='justified'>"
            f"<b>Jamstveni rok:</b> Izvođač jamči za kvalitetu izvedenih radova u trajanju od "
            f"<b>{format_text(jamstveni_rok)}</b> od dana tehničkog pregleda i primopredaje radova.<br><br>"
        )
        if bankarska_garancija:
            parts.append(
                f"<b>Bankarska garancija:</b> {format_text(bankarska_garancija)}<br><br>"
            )
        parts.append(
            "Izvođač je dužan o svom trošku otkloniti sve nedostatke koji se pojave "
            "u jamstvenom roku, a koji su posljedica neispravne izvedbe ili neodgovarajućeg materijala."
            "</div><br>"
        )
        clanak += 1

        # Članak - Viškovi i nepredviđeni radovi
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Viškovi i nepredviđeni radovi)</div>"
            f"<div class='justified'>Nepredviđeni radovi i viškovi radova mogu se izvoditi isključivo "
            f"na temelju prethodnog pisanog naloga Naručitelja, uz suglasnost nadzornog inženjera.<br><br>"
            f"Izvođač koji izvede nepredviđene radove bez pisanog naloga nema pravo na naknadu "
            f"za te radove, osim ako su radovi bili hitno potrebni radi zaštite od štete "
            f"ili sigurnosti građevine.</div><br>"
        )
        clanak += 1

        # Članak - Solidarna odgovornost
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Solidarna odgovornost za nedostatke)</div>"
            f"<div class='justified'>Sukladno čl. 633. ZOO, za štetu nastalu na građevini u roku od "
            f"<b>10 (deset) godina</b> od predaje i preuzimanja radova, a koja je posljedica "
            f"tla ili nedostatka u konstrukciji, <b>solidarno odgovaraju</b>:<br><br>"
            f"a) izvođač radova;<br>"
            f"b) projektant;<br>"
            f"c) nadzorni inženjer.<br><br>"
            f"Ova odgovornost ne može se ugovorom isključiti niti ograničiti.</div><br>"
        )
        clanak += 1

        # Završne odredbe
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Završne odredbe)</div>"
            f"<div class='justified'>Na sva pitanja koja nisu uređena ovim Ugovorom primjenjuju se "
            f"odredbe Zakona o obveznim odnosima (NN 35/05, 41/08, 125/11, 78/15, 29/18, 126/21, 114/22, 156/22, 155/23), "
            f"posebice odredbe o ugovoru o građenju (čl. 620.-636.), te odredbe Zakona o gradnji.<br><br>"
            f"Ovaj Ugovor sastavljen je u 4 (četiri) istovjetna primjerka, po dva za svaku ugovornu stranu.</div><br>"
        )

        # Potpisi
        parts.append(
            "<div class='signature-row'>"
            "<div class='signature-block'><b>NARUČITELJ</b><br><br><br>______________________</div>"
            "<div class='signature-block'><b>IZVOĐAČ</b><br><br><br>______________________</div></div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_licenciju(davatelj, stjecatelj, podaci):
    """
    Ugovor o licenciji - ZOO čl. 699-724, Zakon o patentu, Zakon o žigu
    ZAHTIJEVANA FORMA: PISANA
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        predmet_licencije = podaci.get("predmet_licencije", "")
        vrsta_ip = podaci.get("vrsta_ip", "patent")
        registarski_broj = podaci.get("registarski_broj", "")
        vrsta_licencije = podaci.get("vrsta_licencije", "neiskljuciva")
        teritorij = podaci.get("teritorij", "Republika Hrvatska")
        trajanje = podaci.get("trajanje", "")
        naknada_tip = podaci.get("naknada_tip", "royalty")
        naknada_iznos = podaci.get("naknada_iznos", 0)
        naknada_postotak = podaci.get("naknada_postotak", "")
        sublicenciranje = podaci.get("sublicenciranje", False)

        ip_nazivi = {
            "patent": "patent",
            "žig": "žig (trademark)",
            "autorsko": "autorsko djelo",
            "softver": "softver (računalni program)",
        }
        ip_naziv = ip_nazivi.get(vrsta_ip, vrsta_ip)

        clanak = 1
        parts = [
            "<div style='text-align: center; font-size: 10pt; font-weight: bold; "
            "border: 1px solid black; padding: 8px; margin-bottom: 20px;'>"
            "ZAHTIJEVANA FORMA: PISANA</div>",
            "<div class='header-doc'>UGOVOR O LICENCIJI</div>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {danas} godine, između:</div><br>",
            f"<div class='party-info'><b>1. DAVATELJ LICENCIJE (licensor):</b><br>{davatelj}</div>",
            f"<div class='party-info'><b>2. STJECATELJ LICENCIJE (licencijat):</b><br>{stjecatelj}</div><br>",
        ]

        # Članak - Definicije
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Definicije)</div>"
            f"<div class='justified'>U smislu ovog Ugovora, sljedeći pojmovi imaju značenje kako je navedeno:<br><br>"
            f"<b>\"Predmet licencije\"</b> — {format_text(ip_naziv)} opisan u članku 2. ovog Ugovora;<br>"
            f"<b>\"Davatelj\"</b> — nositelj prava intelektualnog vlasništva koji daje licenciju;<br>"
            f"<b>\"Stjecatelj\"</b> — osoba koja stječe pravo iskorištavanja predmeta licencije;<br>"
            f"<b>\"Teritorij\"</b> — geografsko područje na kojem se licencija može koristiti;<br>"
            f"<b>\"Licencnina\"</b> — naknada koju Stjecatelj plaća Davatelju za pravo korištenja.</div><br>"
        )
        clanak += 1

        # Članak - Predmet licencije
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Predmet licencije)</div>"
            f"<div class='justified'>Davatelj je nositelj prava na sljedeći predmet intelektualnog vlasništva:<br><br>"
            f"<b>Vrsta:</b> {format_text(ip_naziv)}<br>"
            f"<b>Opis:</b> {format_text(predmet_licencije)}<br>"
        )
        if registarski_broj:
            parts.append(f"<b>Registarski broj:</b> {format_text(registarski_broj)}<br>")
        parts.append(
            "<br>Davatelj izjavljuje da je valjani nositelj navedenog prava te da je ovlašten "
            "dati licenciju za njegovo korištenje.</div><br>"
        )
        clanak += 1

        # Članak - Opseg prava
        if vrsta_licencije == "iskljuciva":
            licencija_opis = (
                "Davatelj ovim Ugovorom daje Stjecatelju <b>isključivu (ekskluzivnu) licenciju</b>. "
                "Davatelj se obvezuje da neće dati licenciju za isti predmet na istom teritoriju "
                "nijednoj trećoj osobi, niti će sam iskorištavati predmet licencije na tom teritoriju."
            )
        else:
            licencija_opis = (
                "Davatelj ovim Ugovorom daje Stjecatelju <b>neisključivu licenciju</b>. "
                "Davatelj zadržava pravo dati licenciju za isti predmet na istom teritoriju "
                "i trećim osobama, kao i sam iskorištavati predmet licencije."
            )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Opseg prava)</div>"
            f"<div class='justified'>{licencija_opis}<br><br>"
            f"<b>Teritorij:</b> {format_text(teritorij)}<br>"
            f"<b>Trajanje:</b> {format_text(trajanje) if trajanje else 'Neodređeno vrijeme'}</div><br>"
        )
        clanak += 1

        # Članak - Licencnina (naknada)
        if naknada_tip == "royalty":
            naknada_opis = (
                f"Stjecatelj se obvezuje Davatelju plaćati licencninu u obliku <b>tantijeme (royalty)</b> "
                f"u iznosu od <b>{format_text(naknada_postotak)}%</b> od neto prihoda ostvarenog "
                f"korištenjem predmeta licencije.<br><br>"
                f"Obračun i plaćanje vrši se tromjesečno (kvartalno), najkasnije do 15. u mjesecu "
                f"koji slijedi nakon isteka obračunskog razdoblja."
            )
        elif naknada_tip == "pausalni":
            naknada_opis = (
                f"Stjecatelj se obvezuje Davatelju jednokratno platiti licencninu u paušalnom iznosu "
                f"od <b>{format_eur_s_rijecima(naknada_iznos)}</b>, u roku od 15 dana od potpisa ovog Ugovora."
            )
        else:
            naknada_opis = (
                f"Stjecatelj se obvezuje Davatelju plaćati kombiniranu licencninu:<br><br>"
                f"a) jednokratni paušalni iznos od <b>{format_eur_s_rijecima(naknada_iznos)}</b> pri potpisu Ugovora;<br>"
                f"b) tekuću tantijemu (royalty) od <b>{format_text(naknada_postotak)}%</b> od neto prihoda, "
                f"s tromjesečnim obračunom."
            )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Licencnina)</div>"
            f"<div class='justified'>{naknada_opis}</div><br>"
        )
        clanak += 1

        # Članak - Sublicenciranje
        if sublicenciranje:
            sublicenciranje_tekst = (
                "Stjecatelj ima pravo dati podlicenciju (sublicenciju) trećim osobama, "
                "uz prethodnu pisanu suglasnost Davatelja. Sublicencija ne može sadržavati "
                "šira prava od onih koja su dana ovim Ugovorom."
            )
        else:
            sublicenciranje_tekst = (
                "Stjecatelj <b>nema pravo</b> dati podlicenciju (sublicenciju) trećim osobama "
                "bez prethodne pisane suglasnosti Davatelja."
            )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Sublicenciranje)</div>"
            f"<div class='justified'>{sublicenciranje_tekst}</div><br>"
        )
        clanak += 1

        # Članak - Prestanak
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Prestanak)</div>"
            f"<div class='justified'>Ovaj Ugovor prestaje:<br><br>"
            f"a) istekom ugovorenog roka trajanja;<br>"
            f"b) sporazumnim raskidom;<br>"
            f"c) otkazom s otkaznim rokom od 6 (šest) mjeseci;<br>"
            f"d) raskidom zbog neispunjenja bitne ugovorne obveze.<br><br>"
            f"Ako nijedna strana ne otkaže Ugovor najkasnije 3 (tri) mjeseca prije isteka "
            f"ugovorenog roka, Ugovor se prešutno produljuje za isto vremensko razdoblje, "
            f"sukladno čl. 717. ZOO.</div><br>"
        )
        clanak += 1

        # Završne odredbe
        zakoni = "Zakona o obveznim odnosima (čl. 699.-724.)"
        if vrsta_ip == "patent":
            zakoni += " te Zakona o patentu"
        elif vrsta_ip == "žig":
            zakoni += " te Zakona o žigu"
        elif vrsta_ip in ("autorsko", "softver"):
            zakoni += " te Zakona o autorskom pravu i srodnim pravima"
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Završne odredbe)</div>"
            f"<div class='justified'>Na sva pitanja koja nisu uređena ovim Ugovorom primjenjuju se "
            f"odredbe {zakoni}.<br><br>"
            f"Ovaj Ugovor sastavljen je u 2 (dva) istovjetna primjerka, po jedan za svaku ugovornu stranu.</div><br>"
        )

        # Potpisi
        parts.append(
            "<div class='signature-row'>"
            "<div class='signature-block'><b>DAVATELJ LICENCIJE</b><br><br><br>______________________</div>"
            "<div class='signature-block'><b>STJECATELJ LICENCIJE</b><br><br><br>______________________</div></div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_posredovanje(posrednik, nalogodavac, podaci):
    """
    Ugovor o posredovanju u prometu nekretnina - ZPPN, ZOO čl. 813+
    ZAHTIJEVANA FORMA: PISANA
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        nekretnina_opis = podaci.get("nekretnina_opis", "")
        nekretnina_adresa = podaci.get("nekretnina_adresa", "")
        nekretnina_zk = podaci.get("nekretnina_zk", "")
        cijena_nekretnine = podaci.get("cijena_nekretnine", 0)
        provizija_postotak = podaci.get("provizija_postotak", "")
        rok_trajanja = podaci.get("rok_trajanja", "")
        ekskluziva = podaci.get("ekskluziva", False)
        rjesenje_hgk = podaci.get("rjesenje_hgk", "")

        clanak = 1
        parts = [
            "<div style='text-align: center; font-size: 10pt; font-weight: bold; "
            "border: 1px solid black; padding: 8px; margin-bottom: 20px;'>"
            "ZAHTIJEVANA FORMA: PISANA (ZPPN, ZOO čl. 813)</div>",
            "<div class='header-doc'>UGOVOR O POSREDOVANJU<br>"
            "<span style='font-size: 12pt; font-weight: normal;'>"
            "u prometu nekretnina</span></div>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {danas} godine, između:</div><br>",
            f"<div class='party-info'><b>1. POSREDNIK:</b><br>{posrednik}"
        ]
        if rjesenje_hgk:
            parts.append(f"<br>Rješenje HGK br.: {format_text(rjesenje_hgk)}")
        parts.append("</div>")
        parts.append(
            f"<div class='party-info'><b>2. NALOGODAVAC:</b><br>{nalogodavac}</div><br>"
        )

        # Članak - Predmet posredovanja
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Predmet posredovanja)</div>"
            f"<div class='justified'>Nalogodavac povjerava Posredniku posredovanje u prodaji/kupnji "
            f"sljedeće nekretnine:<br><br>"
            f"<b>Opis:</b> {format_text(nekretnina_opis)}<br>"
            f"<b>Adresa:</b> {format_text(nekretnina_adresa)}<br>"
        )
        if nekretnina_zk:
            parts.append(f"<b>Zemljišnoknjižni podaci:</b> {format_text(nekretnina_zk)}<br>")
        parts.append("</div><br>")
        clanak += 1

        # Članak - Cijena i provizija
        provizija_iznos = 0
        if provizija_postotak and cijena_nekretnine:
            try:
                provizija_iznos = cijena_nekretnine * float(provizija_postotak) / 100
            except (ValueError, TypeError):
                provizija_iznos = 0
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Cijena i provizija)</div>"
            f"<div class='justified'>"
            f"<b>Tražena cijena nekretnine:</b> {format_eur(cijena_nekretnine)}<br><br>"
            f"<b>Posrednička provizija:</b> {format_text(str(provizija_postotak))}% od ostvarene kupoprodajne cijene"
        )
        if provizija_iznos:
            parts.append(f" (procijenjeno: {format_eur(provizija_iznos)})")
        parts.append(
            ".<br><br>Posrednička provizija dospijeva na naplatu danom sklapanja pravnog posla "
            "(kupoprodajnog ugovora ili predugovora) za koji je posredovano, "
            "odnosno danom sklapanja ugovora uz posredovanje Posrednika.<br><br>"
            "Na posredničku proviziju obračunava se PDV sukladno Zakonu o PDV-u.</div><br>"
        )
        clanak += 1

        # Članak - Obveze posrednika
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Obveze posrednika)</div>"
            f"<div class='justified'>Posrednik se obvezuje:<br><br>"
            f"a) nastojati naći i dovesti u vezu s Nalogodavcem osobu radi pregovaranja i "
            f"sklapanja pravnog posla;<br>"
            f"b) upoznati Nalogodavca s prosječnom tržišnom cijenom slične nekretnine;<br>"
            f"c) obaviti uvid u stanje nekretnine u zemljišnim knjigama;<br>"
            f"d) obaviti potrebne radnje radi prezentacije nekretnine na tržištu "
            f"(oglašavanje, organiziranje razgledavanja);<br>"
            f"e) posredovati u pregovorima i nastojati da dođe do sklapanja ugovora;<br>"
            f"f) čuvati podatke Nalogodavca te postupati s povećanom pažnjom "
            f"(pažnja dobrog stručnjaka).</div><br>"
        )
        clanak += 1

        # Članak - Obveze nalogodavca
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Obveze nalogodavca)</div>"
            f"<div class='justified'>Nalogodavac se obvezuje:<br><br>"
            f"a) obavijestiti Posrednika o svim okolnostima važnim za posredovanje;<br>"
            f"b) dati Posredniku na uvid originale isprava koje dokazuju vlasništvo nekretnine;<br>"
            f"c) omogućiti razgledavanje nekretnine zainteresiranim osobama;<br>"
            f"d) obavijestiti Posrednika o svim promjenama vezanim za posao za koji posreduje;<br>"
            f"e) platiti posredničku proviziju sukladno članku 2. ovog Ugovora.</div><br>"
        )
        clanak += 1

        # Članak - Ekskluziva
        if ekskluziva:
            parts.append(
                f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Ekskluzivno posredovanje)</div>"
                f"<div class='justified'>Nalogodavac se obvezuje da za vrijeme trajanja ovog Ugovora "
                f"<b>neće angažirati drugog posrednika</b> za posredovanje u prometu iste nekretnine.<br><br>"
                f"Ako Nalogodavac za vrijeme trajanja ekskluzivnog posredovanja sklopi pravni posao "
                f"za koji je posredovano putem drugog posrednika ili izravno (bez posrednika), "
                f"dužan je Posredniku platiti ugovorenu proviziju u cijelosti.</div><br>"
            )
            clanak += 1

        # Članak - Trajanje i produženje
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Trajanje i produženje)</div>"
            f"<div class='justified'>Ovaj Ugovor sklapa se na određeno vrijeme od "
            f"<b>{format_text(rok_trajanja) if rok_trajanja else '12 (dvanaest) mjeseci'}</b> "
            f"od dana potpisa.<br><br>"
            f"Po isteku ugovorenog roka, Ugovor prestaje, osim ako ga strane pisanim putem ne produže.<br><br>"
            f"Svaka strana može raskinuti Ugovor s otkaznim rokom od 30 (trideset) dana, "
            f"pisanom obavijesti drugoj strani.</div><br>"
        )
        clanak += 1

        # Završne odredbe
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Završne odredbe)</div>"
            f"<div class='justified'>Na sva pitanja koja nisu uređena ovim Ugovorom primjenjuju se "
            f"odredbe Zakona o posredovanju u prometu nekretnina (NN 107/07, 144/12, 14/14, 32/19) "
            f"te odredbe Zakona o obveznim odnosima.<br><br>"
            f"Ovaj Ugovor sastavljen je u 2 (dva) istovjetna primjerka, po jedan za svaku ugovornu stranu.</div><br>"
        )

        # Potpisi
        parts.append(
            "<div class='signature-row'>"
            "<div class='signature-block'><b>POSREDNIK</b><br><br><br>______________________<br>"
            "<small>(pečat i potpis)</small></div>"
            "<div class='signature-block'><b>NALOGODAVAC</b><br><br><br>______________________</div></div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_sporazumni_raskid(strana1, strana2, podaci):
    """
    Sporazum o raskidu ugovora - ZOO čl. 327+
    ZAHTIJEVANA FORMA: ovisi o formi izvornog ugovora (paralelizam formi)
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")
        naziv_izvornog_ugovora = podaci.get("naziv_izvornog_ugovora", "")
        datum_izvornog = podaci.get("datum_izvornog", "")
        jb_broj_izvornog = podaci.get("jb_broj_izvornog", "")
        datum_raskida = podaci.get("datum_raskida", danas)
        ucinak = podaci.get("ucinak", "ex_nunc")
        restitucija = podaci.get("restitucija", "")
        forma_izvornog = podaci.get("forma_izvornog", "pisana")

        if forma_izvornog == "jb_ovjera":
            forma_tekst = "JB OVJERA POTPISA (paralelizam formi)"
        else:
            forma_tekst = "PISANA"

        clanak = 1
        parts = [
            "<div style='text-align: center; font-size: 10pt; font-weight: bold; "
            "border: 1px solid black; padding: 8px; margin-bottom: 20px;'>"
            f"ZAHTIJEVANA FORMA: {forma_tekst}</div>",
            "<div class='header-doc'>SPORAZUM O RASKIDU UGOVORA</div>",
            f"<div class='justified'>Sklopljen u {u_lokativu(mjesto)}, dana {danas} godine, između:</div><br>",
            f"<div class='party-info'><b>1. STRANA:</b><br>{strana1}</div>",
            f"<div class='party-info'><b>2. STRANA:</b><br>{strana2}</div><br>",
        ]

        # Članak - Poziv na izvorni ugovor
        izvorni_ref = f"<b>{format_text(naziv_izvornog_ugovora)}</b>"
        if datum_izvornog:
            izvorni_ref += f" od dana <b>{format_text(datum_izvornog)}</b>"
        if jb_broj_izvornog:
            izvorni_ref += f", JB broj: <b>{format_text(jb_broj_izvornog)}</b>"
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Izvorni ugovor)</div>"
            f"<div class='justified'>Ugovorne strane konstatiraju da su dana {format_text(datum_izvornog)} "
            f"sklopile {izvorni_ref} (u daljnjem tekstu: Izvorni ugovor).</div><br>"
        )
        clanak += 1

        # Članak - Očitovanje volje
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Očitovanje volje o raskidu)</div>"
            f"<div class='justified'>Ugovorne strane suglasno i bezuvjetno izjavljuju da raskidaju "
            f"Izvorni ugovor opisan u članku 1. ovog Sporazuma.<br><br>"
            f"Raskid se vrši sporazumno, temeljem slobodne i ozbiljne volje obiju ugovornih strana, "
            f"sukladno čl. 327. Zakona o obveznim odnosima.</div><br>"
        )
        clanak += 1

        # Članak - Datum nastupa učinaka
        if ucinak == "ex_tunc":
            ucinak_opis = (
                "Raskid Izvornog ugovora ima učinak <b>ex tunc</b> (od početka), "
                "što znači da se smatra kao da Izvorni ugovor nikada nije ni bio sklopljen.<br><br>"
                "Sve činidbe koje su strane izvršile na temelju Izvornog ugovora smatraju se "
                "stečenima bez pravne osnove i podliježu restituciji (povratu)."
            )
        else:
            ucinak_opis = (
                "Raskid Izvornog ugovora ima učinak <b>ex nunc</b> (od sada nadalje), "
                f"s datumom nastupa učinaka <b>{format_text(datum_raskida)}</b>.<br><br>"
                "Sve činidbe koje su strane izvršile do dana raskida ostaju na snazi i "
                "strane nemaju obvezu povrata za do tada izvršene činidbe, osim ako ovim "
                "Sporazumom nije drugačije određeno."
            )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Datum nastupa učinaka)</div>"
            f"<div class='justified'>{ucinak_opis}</div><br>"
        )
        clanak += 1

        # Članak - Restitucija
        if restitucija:
            parts.append(
                f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Restitucija — povrat)</div>"
                f"<div class='justified'>{format_text(restitucija)}</div><br>"
            )
            clanak += 1

        # Članak - Odricanje od potraživanja
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Odricanje od potraživanja)</div>"
            f"<div class='justified'>Potpisom ovog Sporazuma obje ugovorne strane izjavljuju da "
            f"nakon provedbe restitucije (ako je primjenjivo) nemaju nikakvih međusobnih potraživanja "
            f"iz Izvornog ugovora, te se odriču bilo kakvih zahtjeva koji bi proizlazili iz "
            f"Izvornog ugovora ili u vezi s njim.</div><br>"
        )
        clanak += 1

        # Završne odredbe
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak {clanak}. (Završne odredbe)</div>"
            f"<div class='justified'>Na sva pitanja koja nisu uređena ovim Sporazumom primjenjuju se "
            f"odredbe Zakona o obveznim odnosima (NN 35/05, 41/08, 125/11, 78/15, 29/18, 126/21, 114/22, 156/22, 155/23), "
            f"posebice odredbe o raskidu ugovora (čl. 327.-332.).<br><br>"
            f"Ovaj Sporazum sastavljen je u 2 (dva) istovjetna primjerka, po jedan za svaku ugovornu stranu.</div><br>"
        )

        # Potpisi
        parts.append(
            "<div class='signature-row'>"
            "<div class='signature-block'><b>1. STRANA</b><br><br><br>______________________</div>"
            "<div class='signature-block'><b>2. STRANA</b><br><br><br>______________________</div></div>"
        )

        # JB ovjera za paralelizam formi
        if forma_izvornog == "jb_ovjera":
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


def generiraj_predugovor(strana1, strana2, podaci):
    """Predugovor — ZOO cl. 268. Predugovorom se preuzima obveza da se kasnije
    sklopi glavni ugovor. Kad se ne ispuni, druga strana ima pravo zahtijevati
    sklapanje glavnog ugovora u sudskom postupku (cl. 268 st. 4)."""
    try:
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        vrsta_glavnog = format_text(podaci.get('vrsta_glavnog_ugovora', 'kupoprodajni ugovor'))
        predmet = format_text(podaci.get('predmet', ''))
        cijena = podaci.get('cijena_eur', 0)
        cijena_str = format_eur(cijena) if cijena else ''
        kapara = podaci.get('kapara_eur', 0)
        kapara_str = format_eur(kapara) if kapara else ''
        rok_glavnog = format_text(podaci.get('rok_sklapanja_glavnog', ''))
        bitni_uvjeti = format_text(podaci.get('bitni_uvjeti', ''))
        forma_glavnog = format_text(podaci.get('forma_glavnog', 'pisana, s ovjerom potpisa kod javnog bilježnika'))

        kapara_html = ""
        if kapara_str:
            kapara_html = (
                f"<div class='section-title'>Članak 4. — KAPARA</div>"
                f"<div class='doc-body'>Strana 1 ovime predaje, a Strana 2 prima na ime kapare iznos od "
                f"<b>{kapara_str}</b>. Kapara se uračunava u kupoprodajnu cijenu prilikom sklapanja glavnog "
                f"ugovora. Ako glavni ugovor ne bude sklopljen krivnjom Strane 1, kapara ostaje Strani 2. "
                f"Ako krivnjom Strane 2 — Strana 2 vraća dvostruku kaparu Strani 1 (ZOO čl. 303).</div>"
            )

        cijena_html = ""
        if cijena_str:
            cijena_html = (
                f"<div class='section-title'>Članak 3. — CIJENA / VRIJEDNOST</div>"
                f"<div class='doc-body'>Ugovorne strane suglasno utvrđuju da će u glavnom ugovoru "
                f"cijena/vrijednost iznositi <b>{cijena_str}</b>.</div>"
            )

        return (
            f"<div class='header-doc'>PREDUGOVOR<br>"
            f"<span style='font-size: 11pt; font-weight: normal;'>(ZOO čl. 268)</span></div>"
            f"<div class='justified'>sklopljen u {u_lokativu(mjesto)} dana {datum} između:</div><br>"
            f"<div class='party-info'><b>1. STRANA (budući prodavatelj / davatelj):</b><br>{strana1}</div>"
            f"<div class='party-info'><b>2. STRANA (budući kupac / primatelj):</b><br>{strana2}</div><br>"
            f"<div class='section-title'>Članak 1. — OBVEZA SKLAPANJA GLAVNOG UGOVORA</div>"
            f"<div class='doc-body'>Ugovorne strane se ovime obvezuju u roku iz članka 5. ovog Predugovora "
            f"sklopiti glavni ugovor — <b>{vrsta_glavnog}</b> — pod uvjetima dogovorenim u ovom Predugovoru.</div>"
            f"<div class='section-title'>Članak 2. — PREDMET BUDUĆEG GLAVNOG UGOVORA</div>"
            f"<div class='doc-body'>{predmet}</div>"
            f"{cijena_html}"
            f"{kapara_html}"
            f"<div class='section-title'>Članak 5. — ROK ZA SKLAPANJE GLAVNOG UGOVORA</div>"
            f"<div class='doc-body'>Ugovorne strane se obvezuju glavni ugovor sklopiti najkasnije do "
            f"<b>{rok_glavnog}</b>. Forma glavnog ugovora bit će: {forma_glavnog}.</div>"
            f"<div class='section-title'>Članak 6. — BITNI UVJETI</div>"
            f"<div class='doc-body'>{bitni_uvjeti if bitni_uvjeti else 'Ostali uvjeti dogovorit će se u glavnom ugovoru u skladu s ovim Predugovorom.'}</div>"
            f"<div class='section-title'>Članak 7. — POSLJEDICE NEISPUNJENJA</div>"
            f"<div class='doc-body'>Ako jedna strana odbije sklopiti glavni ugovor, druga strana ima pravo "
            f"zahtijevati od suda da se glavni ugovor sklopi (ZOO čl. 268 st. 4), odnosno tražiti naknadu "
            f"štete. Pravo na sklapanje glavnog ugovora gasi se u roku od godine dana od isteka roka iz "
            f"članka 5. (ZOO čl. 268 st. 5).</div>"
            f"<div class='section-title'>Članak 8. — ZAVRŠNE ODREDBE</div>"
            f"<div class='doc-body'>Ovaj Predugovor stupa na snagu danom potpisa. Sastavljen je u "
            f"4 (četiri) primjerka, po 2 (dva) za svaku stranu. Sve eventualne sporove ugovorne strane "
            f"riješit će sporazumno, a u protivnom je nadležan sud prema općoj mjesnoj nadležnosti.</div>"
            f"<br><br>"
            f"<table width='100%'><tr>"
            f"<td width='50%' align='center'><b>1. STRANA</b><br><br>______________________</td>"
            f"<td width='50%' align='center'><b>2. STRANA</b><br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_raskid_najma(najmodavac, najmoprimac, podaci):
    """Otkaz / raskid ugovora o najmu — ZOO cl. 552-558.
    Razlikuje: jednostrani redoviti otkaz (s rokom) i izvanredni raskid (zbog
    neispunjenja, npr. neplacanje najamnine 2+ mjeseca, ZOO cl. 555)."""
    try:
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        vrsta_raskida = podaci.get('vrsta_raskida', 'redoviti')  # redoviti | izvanredni
        ugovor_datum = format_text(podaci.get('ugovor_datum', ''))
        adresa_najma = format_text(podaci.get('adresa_najma', ''))
        otkazni_rok = format_text(podaci.get('otkazni_rok', '30 dana'))
        razlog_izvanredni = format_text(podaci.get('razlog_izvanredni', ''))
        datum_iseljenja = format_text(podaci.get('datum_iseljenja', ''))
        zaostala_najamnina = podaci.get('zaostala_najamnina_eur', 0)
        zaostala_str = format_eur(zaostala_najamnina) if zaostala_najamnina else ''

        if vrsta_raskida == 'izvanredni':
            naslov = "IZVANREDNI RASKID UGOVORA O NAJMU"
            podnaslov = "(ZOO čl. 555 — zbog neispunjenja obveza najmoprimca)"
            tijelo = (
                f"<div class='doc-body'>Najmodavac ovime <b>izvanredno raskida</b> Ugovor o najmu sklopljen "
                f"dana <b>{ugovor_datum}</b> za nekretninu na adresi <b>{adresa_najma}</b>, "
                f"<b>bez otkaznog roka</b>, zbog sljedećih razloga:</div>"
                f"<div class='doc-body'>{razlog_izvanredni}</div>"
                f"<div class='doc-body'>Ovaj raskid temelji se na članku 555. Zakona o obveznim odnosima "
                f"(neispunjenje obveza najmoprimca). Najmoprimac se obvezuje napustiti i predati nekretninu "
                f"u stanju u kojem ju je preuzeo (uz uobičajeno trošenje) najkasnije do "
                f"<b>{datum_iseljenja or '8 dana od primitka ovog raskida'}</b>.</div>"
            )
            if zaostala_str:
                tijelo += (
                    f"<div class='doc-body'>Najmodavac istovremeno poziva najmoprimca da podmiri zaostalu "
                    f"najamninu i pripadajuće troškove u iznosu od <b>{zaostala_str}</b> u roku od 8 dana, "
                    f"u protivnom će se prisilno naplatiti u sudskom postupku.</div>"
                )
        else:
            naslov = "OTKAZ UGOVORA O NAJMU"
            podnaslov = f"(redoviti otkaz s otkaznim rokom od {otkazni_rok})"
            tijelo = (
                f"<div class='doc-body'>Najmodavac ovime <b>otkazuje</b> Ugovor o najmu sklopljen dana "
                f"<b>{ugovor_datum}</b> za nekretninu na adresi <b>{adresa_najma}</b>, "
                f"uz otkazni rok od <b>{otkazni_rok}</b> koji počinje teći danom primitka ovog otkaza.</div>"
                f"<div class='doc-body'>Najmoprimac se obvezuje predati nekretninu u stanju u kojem ju je "
                f"preuzeo (uz uobičajeno trošenje) najkasnije do "
                f"<b>{datum_iseljenja or 'isteka otkaznog roka'}</b>.</div>"
            )

        return (
            f"<div class='party-info'><b>NAJMODAVAC:</b><br>{najmodavac}</div>"
            f"<div class='party-info'><b>NAJMOPRIMAC:</b><br>{najmoprimac}</div><br>"
            f"<div class='header-doc'>{naslov}<br>"
            f"<span style='font-size: 11pt; font-weight: normal;'>{podnaslov}</span></div>"
            f"{tijelo}"
            f"<div class='doc-body'>Sve eventualne sporove riješit ćemo sporazumno, a u protivnom je nadležan "
            f"sud prema mjestu nekretnine.</div>"
            f"<br>"
            f"<div class='justified'>U {u_lokativu(mjesto)}, dana {datum}.</div><br>"
            f"<table width='100%'><tr>"
            f"<td width='40%'></td>"
            f"<td width='60%' align='center'><b>NAJMODAVAC</b><br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_raskid_ugovora_djelu(narucitelj, izvodac, podaci):
    """Raskid ugovora o djelu — ZOO cl. 633.
    Narucitelj uvijek moze raskinuti ugovor (cl. 633 st. 1) uz placanje
    izvrsenog rada + obeshtecenja izvodaca za izgubljenu zaradu."""
    try:
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        ugovor_datum = format_text(podaci.get('ugovor_datum', ''))
        opis_djela = format_text(podaci.get('opis_djela', ''))
        razlog = format_text(podaci.get('razlog_raskida', ''))
        izvrseno_html = format_text(podaci.get('izvrseno_dio', ''))
        ponuda_naknade = podaci.get('ponuda_naknade_eur', 0)
        ponuda_str = format_eur(ponuda_naknade) if ponuda_naknade else ''

        return (
            f"<div class='party-info'><b>NARUČITELJ:</b><br>{narucitelj}</div>"
            f"<div class='party-info'><b>IZVOĐAČ:</b><br>{izvodac}</div><br>"
            f"<div class='header-doc'>RASKID UGOVORA O DJELU<br>"
            f"<span style='font-size: 11pt; font-weight: normal;'>(ZOO čl. 633)</span></div>"
            f"<div class='doc-body'>Naručitelj ovime <b>raskida</b> Ugovor o djelu sklopljen dana "
            f"<b>{ugovor_datum}</b>, čiji je predmet bio:</div>"
            f"<div class='doc-body'>{opis_djela}</div>"
            f"<div class='section-title'>RAZLOG RASKIDA</div>"
            f"<div class='doc-body'>{razlog if razlog else 'Naručitelj koristi pravo iz članka 633. ZOO da raskine Ugovor o djelu i prije njegovog izvršenja.'}</div>"
            f"<div class='section-title'>OBRAČUN IZVRŠENOG RADA</div>"
            f"<div class='doc-body'>{izvrseno_html if izvrseno_html else 'Izvođač nije do dana raskida izvršio značajan dio djela.'}</div>"
            f"{f'<div class=\"doc-body\">Naručitelj nudi Izvođaču naknadu u iznosu od <b>{ponuda_str}</b> kojom se podmiruje vrijednost izvršenog rada i razumno obeštećenje za izgubljenu zaradu sukladno ZOO čl. 633 st. 2.</div>' if ponuda_str else ''}"
            f"<div class='doc-body'>Izvođač se obvezuje predati Naručitelju izvršeni dio djela, kao i sav "
            f"materijal koji mu je predan za izvedbu, najkasnije u roku od 8 dana od primitka ovog Raskida.</div>"
            f"<br>"
            f"<div class='justified'>U {u_lokativu(mjesto)}, dana {datum}.</div><br>"
            f"<table width='100%'><tr>"
            f"<td width='40%'></td>"
            f"<td width='60%' align='center'><b>NARUČITELJ</b><br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_raskid_kupoprodaje(prodavatelj, kupac, podaci):
    """Raskid kupoprodaje zbog neispunjenja — ZOO cl. 360-368.
    Tri tipa: zbog neplacanja cijene (kupac), zbog nepredaje stvari (prodavatelj),
    zbog materijalnih nedostataka (kupac, cl. 410)."""
    try:
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        ugovor_datum = format_text(podaci.get('ugovor_datum', ''))
        predmet = format_text(podaci.get('predmet', ''))
        razlog_tip = podaci.get('razlog_tip', 'neplacanje')  # neplacanje | nepredaja | nedostaci
        opis_neispunjenja = format_text(podaci.get('opis_neispunjenja', ''))
        cijena = podaci.get('cijena_eur', 0)
        cijena_str = format_eur(cijena) if cijena else ''
        rok_ostavljen = format_text(podaci.get('rok_ostavljen', ''))
        zahtjev_povrat = format_text(podaci.get('zahtjev_povrat', ''))

        razlog_map = {
            'neplacanje': (
                "neispunjenja obveze plaćanja kupoprodajne cijene",
                "članak 360. ZOO (raskid zbog neispunjenja)",
                "Prodavatelj"
            ),
            'nepredaja': (
                "neispunjenja obveze predaje stvari",
                "članak 360. ZOO (raskid zbog neispunjenja)",
                "Kupac"
            ),
            'nedostaci': (
                "materijalnih nedostataka stvari",
                "članci 401. — 422. ZOO (odgovornost za materijalne nedostatke)",
                "Kupac"
            ),
        }
        razlog_tekst, pravni_temelj, raskidatelj = razlog_map.get(razlog_tip, razlog_map['neplacanje'])

        rok_html = ""
        if rok_ostavljen:
            rok_html = (
                f"<div class='doc-body'>Stranci kojoj se pripisuje neispunjenje već je dana "
                f"<b>{rok_ostavljen}</b> ostavljen primjereni naknadni rok za ispunjenje, koji je istekao "
                f"bez rezultata, čime su ispunjeni uvjeti za raskid sukladno ZOO čl. 362.</div>"
            )

        povrat_html = ""
        if zahtjev_povrat:
            povrat_html = (
                f"<div class='section-title'>POSLJEDICE RASKIDA</div>"
                f"<div class='doc-body'>{zahtjev_povrat}</div>"
            )
        elif cijena_str:
            povrat_html = (
                f"<div class='section-title'>POSLJEDICE RASKIDA</div>"
                f"<div class='doc-body'>Ugovorne strane su dužne međusobno vratiti sve što su primile po "
                f"raskinutom ugovoru (ZOO čl. 368). Iznos kupoprodajne cijene od <b>{cijena_str}</b> ima se "
                f"vratiti u roku od 8 dana, uz pripadajuće zakonske zatezne kamate.</div>"
            )

        return (
            f"<div class='party-info'><b>PRODAVATELJ:</b><br>{prodavatelj}</div>"
            f"<div class='party-info'><b>KUPAC:</b><br>{kupac}</div><br>"
            f"<div class='header-doc'>IZJAVA O RASKIDU KUPOPRODAJE<br>"
            f"<span style='font-size: 11pt; font-weight: normal;'>zbog {razlog_tekst}</span></div>"
            f"<div class='doc-body'>{raskidatelj} ovime <b>raskida</b> Ugovor o kupoprodaji sklopljen dana "
            f"<b>{ugovor_datum}</b>, čiji je predmet:</div>"
            f"<div class='doc-body'>{predmet}</div>"
            f"<div class='section-title'>RAZLOG RASKIDA</div>"
            f"<div class='doc-body'>{opis_neispunjenja}</div>"
            f"{rok_html}"
            f"<div class='doc-body'>Pravni temelj raskida: {pravni_temelj}.</div>"
            f"{povrat_html}"
            f"<div class='doc-body'>Ovaj raskid stupa na snagu danom primitka od strane druge strane. "
            f"Stranka koja prima raskid ima pravo osporavati osnovanost raskida u sudskom postupku.</div>"
            f"<br>"
            f"<div class='justified'>U {u_lokativu(mjesto)}, dana {datum}.</div><br>"
            f"<table width='100%'><tr>"
            f"<td width='40%'></td>"
            f"<td width='60%' align='center'><b>{raskidatelj.upper()}</b><br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
