# -----------------------------------------------------------------------------
# GENERATORI: Posrednik u najmu (A-B-C arhitektura)
# A = Stanodavac, B = Posrednik, C = Narucitelj (Poslodavac)
# Dva ugovora: Najam stanova (A-B) i Upravljanje kapacitetom (B-C)
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur, format_eur_s_rijecima, _escape


def generiraj_ugovor_najam_ab(najmodavac, najmoprimac, nekretnina, podaci):
    """Generira Ugovor o najmu stanova (A-B).
    najmodavac: HTML string (stranka A)
    najmoprimac: HTML string (stranka B)
    nekretnina: dict s podacima o nekretnini
    podaci: dict s ostalim podacima
    """
    try:
        datum_str = podaci.get('datum', date.today()).strftime("%d.%m.%Y.")
        mjesto = _escape(podaci.get('mjesto', ''))
        trajanje_mj = _escape(str(podaci.get('trajanje_mjeseci', '')))
        datum_pocetka = podaci.get('datum_pocetka')
        datum_pocetka_str = datum_pocetka.strftime("%d.%m.%Y.") if datum_pocetka else '__________'
        najamnina = format_eur(podaci.get('najamnina', 0))
        najamnina_slovima = _escape(podaci.get('najamnina_slovima', ''))
        tereti = _escape(podaci.get('tereti', 'nema'))

        adr = _escape(nekretnina.get('adresa', ''))
        kc = _escape(nekretnina.get('katastarska_cestica', ''))
        povrsina = _escape(str(nekretnina.get('povrsina', '')))
        sobe_kreveti = _escape(str(nekretnina.get('sobe_kreveti', '')))

        parts = []
        parts.append(
            f"<div class='header-doc'>UGOVOR O NAJMU STANOVA</div>"
        )
        parts.append(
            f"<div class='justified'>"
            f"Sklopljen dana {datum_str} u <b>{mjesto}</b>"
            f"</div><br>"
        )
        # -- Strane --
        parts.append(
            f"<div class='section-title' style='text-align: center;'>UGOVORNE STRANE</div>"
        )
        parts.append(
            f"<div class='party-info'>"
            f"<b>1. NAJMODAVAC (A):</b><br>{najmodavac}<br>"
            f"(u daljnjem tekstu: \u201ENajmodavac\u201C)"
            f"</div>"
        )
        parts.append(
            f"<div class='party-info'>"
            f"<b>2. NAJMOPRIMAC (B):</b><br>{najmoprimac}<br>"
            f"(u daljnjem tekstu: \u201ENajmoprimac\u201C)"
            f"</div><br>"
        )

        # -- I. PREDMET UGOVORA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"I. PREDMET UGOVORA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 1.</div>"
            f"<div class='justified'>"
            f"(1) Najmodavac je vlasnik/suvlasnik sljedećih nekretnina:<br>"
            f"&nbsp;&nbsp;- Adresa: <b>{adr}</b><br>"
            f"&nbsp;&nbsp;- Katastarska čestica: <b>{kc}</b><br>"
            f"&nbsp;&nbsp;- Površina: <b>{povrsina} m\u00B2</b><br>"
            f"&nbsp;&nbsp;- Broj soba/kreveta: <b>{sobe_kreveti}</b><br>"
            f"(u daljnjem tekstu: \u201EPredmetne nekretnine\u201C)<br><br>"
            f"(2) Najmodavac daje Najmoprimcu Predmetne nekretnine u najam za "
            f"potrebe smještaja radnika trećih osoba (korporativni smještaj), "
            f"a Najmoprimac ih prima u najam pod uvjetima iz ovog Ugovora."
            f"</div>"
        )

        # -- II. NAMJENA I PRAVO PODNAJMA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"II. NAMJENA I PRAVO PODNAJMA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 2.</div>"
            f"<div class='justified'>"
            f"(1) Predmetne nekretnine koristit će se isključivo za stambene "
            f"potrebe \u2014 smještaj radnika pravnih osoba s kojima Najmoprimac ima "
            f"sklopljene ugovore o upravljanju smještajnim kapacitetom.<br><br>"
            f"(2) Najmodavac daje Najmoprimcu IZRIČITU, BEZUVJETNU I UNAPRIJED "
            f"DANU SUGLASNOST da:<br>"
            f"&nbsp;&nbsp;a) daje Predmetne nekretnine u podnajam pravnim i fizičkim osobama,<br>"
            f"&nbsp;&nbsp;b) daje Predmetne nekretnine na korištenje trećim osobama u svrhu "
            f"korporativnog smještaja radnika,<br>"
            f"&nbsp;&nbsp;c) u slučaju smanjene popunjenosti, privremeno plasira slobodni "
            f"kapacitet na tržište kratkoročnog smještaja (turistički, poslovni ili tranzitni smještaj)<br>"
            f"bez potrebe za zasebnom pisanom suglasnošću Najmodavca za svaki pojedinačni slučaj.<br><br>"
            f"(3) Suglasnost iz stavka (2) ovog članka sastavni je dio ovog "
            f"Ugovora i ne može se jednostrano opozvati za vrijeme trajanja najma."
            f"</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 3.</div>"
            f"<div class='justified'>"
            f"Najmodavac izjavljuje da nad Predmetnim nekretninama ne postoje "
            f"prava trećih osoba niti tereti koji bi ograničavali ili onemogućavali "
            f"korištenje sukladno ovom Ugovoru, osim sljedećih: <b>{tereti}</b>."
            f"</div>"
        )

        # -- III. TRAJANJE NAJMA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"III. TRAJANJE NAJMA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 4.</div>"
            f"<div class='justified'>"
            f"(1) Ovaj Ugovor sklapa se na određeno vrijeme u trajanju od "
            f"<b>{trajanje_mj}</b> mjeseci, počevši od <b>{datum_pocetka_str}</b>.<br><br>"
            f"(2) Ugovor se automatski produljuje za daljnjih 12 mjeseci, osim "
            f"ako bilo koja strana dostavi pisani otkaz najmanje 90 (devedeset) "
            f"dana prije isteka ugovorenog ili produljenog razdoblja.<br><br>"
            f"(3) Ugovor se ne može raskinuti prije isteka ugovorenog razdoblja, "
            f"osim u slučajevima predviđenim člankom 10. ovog Ugovora."
            f"</div>"
        )

        # -- IV. NAJAMNINA I NACIN PLACANJA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"IV. NAJAMNINA I NAČIN PLAĆANJA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 5.</div>"
            f"<div class='justified'>"
            f"(1) Mjesečna najamnina iznosi <b>{najamnina}</b> "
            f"(slovima: {najamnina_slovima}).<br><br>"
            f"(2) Najamnina se plaća unaprijed, najkasnije do 5. (petog) dana "
            f"u mjesecu za tekući mjesec, na IBAN račun Najmodavca naveden u "
            f"zaglavlju ovog Ugovora.<br><br>"
            f"(3) Najamnina uključuje korištenje Predmetnih nekretnina s postojećim "
            f"namještajem i opremom, popis kojih se nalazi u Prilogu 1 ovog Ugovora.<br><br>"
            f"(4) U najamninu NISU uključeni troškovi komunalnih usluga (električna "
            f"energija, voda, plin, internet, odvoz otpada), koje snosi Najmoprimac "
            f"izravno prema davateljima usluga."
            f"</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 6.</div>"
            f"<div class='justified'>"
            f"(1) Najamnina se godišnje usklađuje s indeksom potrošačkih cijena "
            f"(CPI) koji objavljuje Državni zavod za statistiku Republike Hrvatske.<br><br>"
            f"(2) Usklađivanje se primjenjuje od 1. siječnja svake kalendarske "
            f"godine, počevši od godine koja slijedi godinu sklapanja ovog Ugovora.<br><br>"
            f"(3) Usklađivanje ne može rezultirati smanjenjem najamnine ispod "
            f"iznosa ugovorenog u članku 5. stavak (1)."
            f"</div>"
        )

        # -- V. OBVEZE NAJMODAVCA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"V. OBVEZE NAJMODAVCA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 7.</div>"
            f"<div class='justified'>"
            f"Najmodavac se obvezuje:<br>"
            f"&nbsp;&nbsp;a) predati Predmetne nekretnine Najmoprimcu u stanju prikladnom za "
            f"ugovorenu namjenu na datum početka najma,<br>"
            f"&nbsp;&nbsp;b) održavati Predmetne nekretnine u stanju pogodnom za ugovorenu "
            f"uporabu, uključujući održavanje nosive konstrukcije, krova, fasade i zajedničkih instalacija,<br>"
            f"&nbsp;&nbsp;c) izvršiti nužne popravke koji su nastali uslijed dotrajalosti ili "
            f"više sile, u roku od 15 dana od pisane obavijesti Najmoprimca,<br>"
            f"&nbsp;&nbsp;d) ne ometati Najmoprimca u korištenju Predmetnih nekretnina,<br>"
            f"&nbsp;&nbsp;e) obavijestiti Najmoprimca najmanje 90 dana unaprijed o namjeri "
            f"prodaje, opterećenja ili bilo kakve raspolaganja Predmetnim nekretninama."
            f"</div>"
        )

        # -- VI. OBVEZE NAJMOPRIMCA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"VI. OBVEZE NAJMOPRIMCA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 8.</div>"
            f"<div class='justified'>"
            f"Najmoprimac se obvezuje:<br>"
            f"&nbsp;&nbsp;a) koristiti Predmetne nekretnine pažnjom dobrog gospodarstvenika,<br>"
            f"&nbsp;&nbsp;b) uredno i pravovremeno plaćati najamninu i komunalne troškove,<br>"
            f"&nbsp;&nbsp;c) ne vršiti preinake na Predmetnim nekretninama bez prethodne "
            f"pisane suglasnosti Najmodavca, osim postavljanja pokretnog namještaja i opreme "
            f"za smještaj koji se mogu ukloniti bez oštećenja nekretnine,<br>"
            f"&nbsp;&nbsp;d) obavijestiti Najmodavca o svakom većem kvaru ili oštećenju "
            f"u roku od 48 sati,<br>"
            f"&nbsp;&nbsp;e) pri prestanku najma, vratiti Predmetne nekretnine u stanju "
            f"u kakvom su primljene, uzimajući u obzir uobičajenu amortizaciju nastalu redovnom uporabom,<br>"
            f"&nbsp;&nbsp;f) ugovoriti i održavati policu osiguranja pokretne imovine i "
            f"odgovornosti prema trećima za sve vrijeme trajanja najma."
            f"</div>"
        )

        # -- VII. PRAVO NA MINORNE ADAPTACIJE --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"VII. PRAVO NA MINORNE ADAPTACIJE</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 9.</div>"
            f"<div class='justified'>"
            f"(1) Najmoprimac ima pravo, bez dodatne suglasnosti Najmodavca:<br>"
            f"&nbsp;&nbsp;a) postavljati i mijenjati pokretni namještaj (krevete, ormare, stolove, stolice),<br>"
            f"&nbsp;&nbsp;b) postavljati opremu za smještaj (posteljinu, kućanske aparate, sigurnosne brave),<br>"
            f"&nbsp;&nbsp;c) vršiti tekuće održavanje (krpanje zidova, zamjena žarulja, održavanje instalacija).<br><br>"
            f"(2) Za sve preinake koje zadiru u supstancu nekretnine (mijenjanje pregradnih zidova, "
            f"električnih instalacija, vodovodnih cijevi), Najmoprimac mora pribaviti prethodnu pisanu "
            f"suglasnost Najmodavca."
            f"</div>"
        )

        # -- VIII. RASKID UGOVORA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"VIII. RASKID UGOVORA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 10.</div>"
            f"<div class='justified'>"
            f"(1) Svaka strana može raskinuti Ugovor prije isteka ugovorenog "
            f"razdoblja samo u sljedećim slučajevima:<br>"
            f"&nbsp;&nbsp;a) ako druga strana ne ispunjava svoje bitne obveze iz ovog Ugovora "
            f"niti u naknadnom roku od 30 dana od pisane opomene,<br>"
            f"&nbsp;&nbsp;b) ako nastanu okolnosti koje bitno otežavaju ispunjenje ugovora, "
            f"a koje se nisu mogle predvidjeti u trenutku sklapanja (čl. 369. Zakona o obveznim "
            f"odnosima), uz prethodni pokušaj mirnog rješavanja,<br>"
            f"&nbsp;&nbsp;c) sporazumom obiju strana.<br><br>"
            f"(2) U slučaju raskida od strane Najmoprimca prije isteka ugovorenog "
            f"razdoblja iz razloga koji nisu navedeni u stavku (1) točki a) ovog "
            f"članka, Najmoprimac je dužan Najmodavcu isplatiti najamninu za "
            f"preostalo ugovoreno razdoblje, umanjenu za prihod koji Najmodavac "
            f"ostvari ponovnim iznajmljivanjem u razumnom roku."
            f"</div>"
        )

        # -- IX. PRIMOPREDAJA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"IX. PRIMOPREDAJA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 11.</div>"
            f"<div class='justified'>"
            f"(1) Primopredaja Predmetnih nekretnina izvršit će se na dan početka "
            f"najma uz sastavljanje zapisnika o primopredaji.<br><br>"
            f"(2) Zapisnik će sadržavati popis namještaja i opreme (Prilog 1), "
            f"stanje brojila komunalnih usluga, fotografsku dokumentaciju, i "
            f"popis eventualnih nedostataka."
            f"</div>"
        )

        # -- X. RJESAVANJE SPOROVA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"X. RJEŠAVANJE SPOROVA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 12.</div>"
            f"<div class='justified'>"
            f"Za sporove iz ovog Ugovora nadležan je stvarno nadležni sud prema "
            f"mjestu nalaženja Predmetnih nekretnina."
            f"</div>"
        )

        # -- XI. ZAVRSNE ODREDBE --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"XI. ZAVRŠNE ODREDBE</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 13.</div>"
            f"<div class='justified'>"
            f"(1) Ovaj Ugovor sastavljen je u 4 (četiri) istovjetna primjerka, "
            f"po 2 (dva) za svaku ugovornu stranu.<br><br>"
            f"(2) Na sve što ovim Ugovorom nije uređeno, primjenjuju se odredbe "
            f"Zakona o obveznim odnosima i Zakona o najmu stanova.<br><br>"
            f"(3) Izmjene i dopune ovog Ugovora valjane su samo u pisanom obliku "
            f"potpisanom od obiju ugovornih strana.<br><br>"
            f"(4) Ništavost pojedine odredbe ovog Ugovora ne utječe na valjanost "
            f"ostalih odredbi."
            f"</div>"
        )

        # -- PRILOG 1 napomena --
        parts.append(
            f"<div class='justified' style='margin-top: 20px; font-style: italic;'>"
            f"<b>PRILOG 1:</b> Popis namještaja i opreme (sastavlja se pri primopredaji)"
            f"</div>"
        )

        # -- Potpisi --
        parts.append(
            f"<div class='signature-row'>"
            f"<div class='signature-block'>"
            f"<b>NAJMODAVAC (A)</b><br><br><br>________________________"
            f"</div>"
            f"<div class='signature-block'>"
            f"<b>NAJMOPRIMAC (B)</b><br><br><br>________________________"
            f"</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_ugovor_upravljanje_bc(davatelj, narucitelj, kapacitet, podaci):
    """Generira Ugovor o upravljanju i osiguranju smjestajnog kapaciteta (B-C).
    davatelj: HTML string (stranka B)
    narucitelj: HTML string (stranka C)
    kapacitet: dict s podacima o kapacitetu
    podaci: dict s ostalim podacima
    """
    try:
        datum_str = podaci.get('datum', date.today()).strftime("%d.%m.%Y.")
        mjesto = _escape(podaci.get('mjesto', ''))
        podrucje = _escape(podaci.get('podrucje_djelovanja', ''))

        bazni_kap = _escape(str(kapacitet.get('bazni_kapacitet', '')))
        min_kap = _escape(str(kapacitet.get('minimalni_kapacitet', '')))

        fiksna_naknada = format_eur(podaci.get('fiksna_naknada', 0))
        fiksna_slovima = _escape(podaci.get('fiksna_slovima', ''))
        varijabilna = format_eur(podaci.get('varijabilna_naknada', 0))
        varijabilna_slovima = _escape(podaci.get('varijabilna_slovima', ''))

        trajanje_mj = _escape(str(podaci.get('trajanje_mjeseci', '')))
        datum_pocetka = podaci.get('datum_pocetka')
        datum_pocetka_str = datum_pocetka.strftime("%d.%m.%Y.") if datum_pocetka else '__________'

        sla_hitni = format_eur(podaci.get('sla_hitni', 0))
        sla_checkin = format_eur(podaci.get('sla_checkin', 0))
        kazna_kontakt = format_eur(podaci.get('kazna_kontakt', 0))
        max_mgmt_fee = _escape(str(podaci.get('max_mgmt_fee_pct', '')))
        sud_mjesto = _escape(podaci.get('sud_mjesto', ''))

        # Specifikacija kapaciteta (tablica)
        spec_rows = kapacitet.get('specifikacija', [])

        parts = []
        parts.append(
            f"<div class='header-doc'>UGOVOR O UPRAVLJANJU I OSIGURANJU<br>SMJEŠTAJNOG KAPACITETA</div>"
        )
        parts.append(
            f"<div class='justified'>"
            f"Sklopljen dana {datum_str} u <b>{mjesto}</b>"
            f"</div><br>"
        )

        # -- Strane --
        parts.append(
            f"<div class='section-title' style='text-align: center;'>UGOVORNE STRANE</div>"
        )
        parts.append(
            f"<div class='party-info'>"
            f"<b>1. DAVATELJ USLUGE (B):</b><br>{davatelj}<br>"
            f"(u daljnjem tekstu: \u201EDavatelj\u201C)"
            f"</div>"
        )
        parts.append(
            f"<div class='party-info'>"
            f"<b>2. NARUČITELJ (C):</b><br>{narucitelj}<br>"
            f"(u daljnjem tekstu: \u201ENaručitelj\u201C)"
            f"</div><br>"
        )

        # -- I. PREAMBULA I SVRHA UGOVORA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"I. PREAMBULA I SVRHA UGOVORA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 1.</div>"
            f"<div class='justified'>"
            f"(1) Ugovorne strane suglasno utvrđuju da se Naručitelj bavi "
            f"djelatnošću koja zahtijeva angažman većeg broja radnika kojima "
            f"je potreban organizirani smještaj na području <b>{podrucje}</b> "
            f"(u daljnjem tekstu: \u201EPodručje djelovanja\u201C).<br><br>"
            f"(2) Davatelj je specijaliziran za upravljanje smještajnim "
            f"kapacitetima i raspolaže mrežom najamnih nekretnina na Području "
            f"djelovanja, za čije održavanje i upravljanje snosi stalne fiksne "
            f"troškove neovisno o popunjenosti.<br><br>"
            f"(3) Ovim Ugovorom Naručitelj povjerava Davatelju cjelokupno "
            f"operativno upravljanje smještajnom infrastrukturom za svoje radnike, "
            f"a Davatelj se obvezuje osigurati raspoloživost i upravljanje "
            f"smještajnim kapacitetom pod uvjetima iz ovog Ugovora.<br><br>"
            f"(4) Ugovorne strane izričito utvrđuju da ovaj Ugovor po svojoj "
            f"pravnoj prirodi NIJE ugovor o najmu niti podnajmu nekretnina, već "
            f"predstavlja inominatni ugovor o pružanju usluga upravljanja "
            f"smještajnom infrastrukturom, sklopljen sukladno načelu slobode "
            f"ugovaranja iz članka 2. Zakona o obveznim odnosima (NN 35/05, 41/08, "
            f"125/11, 78/15, 29/18, 126/21, 114/22, 156/22, 155/23), s elementima "
            f"ugovora o djelu (čl. 590. ZOO) i ugovora o nalogu (čl. 764. ZOO)."
            f"</div>"
        )

        # -- II. DEFINICIJE --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"II. DEFINICIJE</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 2.</div>"
            f"<div class='justified'>"
            f"U smislu ovog Ugovora, sljedeći pojmovi imaju značenje:<br><br>"
            f"(1) <b>Smještajni kapacitet</b> \u2014 skup stambenih jedinica (stanova, "
            f"soba, kreveta) kojima Davatelj upravlja i koje su namijenjene "
            f"smještaju Naručiteljevih radnika.<br><br>"
            f"(2) <b>Bazni kapacitet</b> \u2014 minimalni broj smještajnih jedinica / "
            f"kreveta koje Davatelj drži na raspolaganju isključivo za Naručitelja. "
            f"Bazni kapacitet iznosi <b>{bazni_kap}</b> kreveta / stambenih jedinica.<br><br>"
            f"(3) <b>Naknada za upravljanje kapacitetom</b> \u2014 fiksni mjesečni iznos "
            f"koji Naručitelj plaća Davatelju za osiguranje raspoloživosti i "
            f"upravljanje Baznim kapacitetom, neovisno o stupnju korištenja.<br><br>"
            f"(4) <b>Naknada za korištenje</b> \u2014 varijabilni iznos koji Naručitelj "
            f"plaća Davatelju po ostvarenom noćenju, a koji pokriva troškove "
            f"nastale stvarnim korištenjem smještajnih jedinica (komunalije po "
            f"potrošnji, dnevno čišćenje, potrošni materijal).<br><br>"
            f"(5) <b>Radnici</b> \u2014 fizičke osobe u radnom odnosu s Naručiteljem ili "
            f"s njime povezanim društvima, koje Naručitelj upućuje na smještaj.<br><br>"
            f"(6) <b>Izvještaj o strukturi troškova</b> \u2014 periodični dokument u kojem "
            f"Davatelj Naručitelju transparentno prikazuje strukturu fiksnih "
            f"troškova koji čine osnovu Naknade za upravljanje kapacitetom.<br><br>"
            f"(7) <b>Re-monetizacija</b> \u2014 privremeno plasiranje neiskorištenog "
            f"smještajnog kapaciteta na tržište kratkoročnog smještaja, u skladu "
            f"s člankom 11. ovog Ugovora."
            f"</div>"
        )

        # -- III. OBVEZE DAVATELJA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"III. OBVEZE DAVATELJA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 3.</div>"
            f"<div class='justified'>"
            f"Davatelj se obvezuje:<br><br>"
            f"&nbsp;&nbsp;a) osigurati Bazni kapacitet na Području djelovanja za smještaj "
            f"Naručiteljevih Radnika za cijelo vrijeme trajanja ovog Ugovora,<br><br>"
            f"&nbsp;&nbsp;b) održavati sve smještajne jedinice u urednom, funkcionalnom i "
            f"higijenski prikladnom stanju, uključujući razdoblja kada jedinice nisu popunjene,<br><br>"
            f"&nbsp;&nbsp;c) organizirati check-in i check-out Radnika u roku od 24 sata "
            f"od primitka Naručiteljeve pisane najave (elektronička pošta ili drugi dogovoreni kanal),<br><br>"
            f"&nbsp;&nbsp;d) osigurati tjednu inspekciju i čišćenje svih smještajnih "
            f"jedinica, uključujući prazne,<br><br>"
            f"&nbsp;&nbsp;e) organizirati tekuće održavanje i hitne popravke u skladu s "
            f"rokovima iz članka 9. (SLA),<br><br>"
            f"&nbsp;&nbsp;f) voditi evidenciju popunjenosti i troškova te dostavljati "
            f"Naručitelju mjesečni izvještaj najkasnije do 10. u mjesecu za prethodni mjesec,<br><br>"
            f"&nbsp;&nbsp;g) dostavljati Naručitelju Izvještaj o strukturi troškova "
            f"kvartalno (svaka 3 mjeseca),<br><br>"
            f"&nbsp;&nbsp;h) pridržavati se svih važećih propisa Republike Hrvatske koji se "
            f"odnose na smještaj, sigurnost, zaštitu na radu i zaštitu osobnih podataka."
            f"</div>"
        )

        # -- IV. OBVEZE NARUCITELJA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"IV. OBVEZE NARUČITELJA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 4.</div>"
            f"<div class='justified'>"
            f"Naručitelj se obvezuje:<br><br>"
            f"&nbsp;&nbsp;a) uredno i pravovremeno plaćati Naknadu za upravljanje kapacitetom "
            f"i Naknadu za korištenje sukladno člancima 5. i 7. ovog Ugovora,<br><br>"
            f"&nbsp;&nbsp;b) pisanim putem obavijestiti Davatelja o dolasku ili odlasku "
            f"Radnika najmanje 48 sati unaprijed (osim u hitnim slučajevima kada je "
            f"dopuštena najava u roku od 12 sati),<br><br>"
            f"&nbsp;&nbsp;c) osigurati da se Radnici pridržavaju kućnog reda smještajnih "
            f"jedinica, čija pravila utvrđuje Davatelj i koji se nalaze u Prilogu 2 ovog Ugovora,<br><br>"
            f"&nbsp;&nbsp;d) snositi odgovornost za štetu koju Radnici uzrokuju na "
            f"smještajnim jedinicama i opremi, iznad uobičajene amortizacije,<br><br>"
            f"&nbsp;&nbsp;e) ne kontaktirati izravno vlasnike nekretnina (stanodavce) niti "
            f"pokušavati sklopiti zasebne aranžmane s njima mimo Davatelja."
            f"</div>"
        )

        # -- V. NAKNADA ZA UPRAVLJANJE KAPACITETOM (FIKSNI DIO) --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"V. NAKNADA ZA UPRAVLJANJE KAPACITETOM (FIKSNI DIO)</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 5.</div>"
            f"<div class='justified'>"
            f"(1) Naručitelj plaća Davatelju Naknadu za upravljanje kapacitetom "
            f"u iznosu od <b>{fiksna_naknada}</b> (slovima: {fiksna_slovima}) mjesečno.<br><br>"
            f"(2) Naknada iz stavka (1) pokriva sljedeće troškove, kako je "
            f"detaljno prikazano u Izvještaju o strukturi troškova:<br>"
            f"&nbsp;&nbsp;a) najamnine koje Davatelj plaća vlasnicima nekretnina,<br>"
            f"&nbsp;&nbsp;b) osnovne komunalne troškove praznih jedinica (grijanje u zimskom "
            f"razdoblju, minimalne režije),<br>"
            f"&nbsp;&nbsp;c) osiguranje nekretnina i opreme,<br>"
            f"&nbsp;&nbsp;d) tjednu inspekciju i održavanje praznih jedinica,<br>"
            f"&nbsp;&nbsp;e) operativnu naknadu Davatelja za upravljanje (management fee).<br><br>"
            f"(3) Naknada se plaća unaprijed, najkasnije do 5. (petog) dana u "
            f"mjesecu za tekući mjesec, na IBAN račun Davatelja naveden u zaglavlju "
            f"ovog Ugovora.<br><br>"
            f"(4) Naknada se plaća NEOVISNO o stupnju popunjenosti smještajnog "
            f"kapaciteta. Okolnost da Naručitelj u pojedinom mjesecu ne koristi "
            f"cjelokupni ili bilo koji dio Baznog kapaciteta ne utječe na obvezu "
            f"plaćanja i ne predstavlja razlog za umanjenje Naknade, jer Davatelj "
            f"za cijelo to vrijeme snosi fiksne troškove održavanja Baznog "
            f"kapaciteta u stanju spremnosti isključivo za Naručitelja.<br><br>"
            f"(5) Ugovorne strane izričito utvrđuju da su bile svjesne mogućnosti "
            f"fluktuacija u broju Radnika kojima je potreban smještaj, te da su "
            f"pri određivanju Naknade iz stavka (1) tu okolnost uzele u obzir. "
            f"Promjene u broju Radnika smatraju se uobičajenim poslovnim rizikom "
            f"i NE predstavljaju promijenjene okolnosti u smislu članka 369. "
            f"Zakona o obveznim odnosima."
            f"</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 6.</div>"
            f"<div class='justified'>"
            f"(1) Naknada iz članka 5. stavka (1) godišnje se usklađuje s indeksom "
            f"potrošačkih cijena (CPI) koji objavljuje Državni zavod za statistiku.<br><br>"
            f"(2) Usklađivanje se primjenjuje od 1. siječnja svake kalendarske "
            f"godine, počevši od godine koja slijedi godinu sklapanja ovog Ugovora.<br><br>"
            f"(3) Usklađivanje ne može rezultirati smanjenjem Naknade ispod "
            f"prvotno ugovorenog iznosa.<br><br>"
            f"(4) Neovisno o CPI usklađivanju, ukoliko se troškovi najamnina "
            f"koje Davatelj plaća vlasnicima nekretnina promijene za više od 10% "
            f"u odnosu na troškove važeće na dan sklapanja ovog Ugovora, Davatelj "
            f"može zatražiti preispitivanje Naknade. Naručitelj ne može neopravdano "
            f"odbiti takav zahtjev. U slučaju nesporazuma, strane će pristupiti "
            f"postupku mirenja iz članka 19. ovog Ugovora.<br><br>"
            f"(5) Uštede u strukturi troškova koje Davatelj ostvari operativnom "
            f"optimizacijom ne mogu služiti kao osnova za umanjenje Naknade za "
            f"upravljanje kapacitetom. Bazna razina troškova revidira se jednom "
            f"godišnje zajedničkom odlukom stranaka, uzimajući u obzir isključivo "
            f"promjene tržišnih uvjeta i indeks potrošačkih cijena."
            f"</div>"
        )

        # -- VI. NAKNADA ZA KORISTENJE (VARIJABILNI DIO) --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"VI. NAKNADA ZA KORIŠTENJE (VARIJABILNI DIO)</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 7.</div>"
            f"<div class='justified'>"
            f"(1) Za svako ostvareno noćenje Radnika u smještajnoj jedinici, "
            f"Naručitelj plaća Davatelju Naknadu za korištenje u iznosu od "
            f"<b>{varijabilna}</b> (slovima: {varijabilna_slovima}) po noćenju po osobi.<br><br>"
            f"(2) Naknada iz stavka (1) pokriva:<br>"
            f"&nbsp;&nbsp;a) komunalne troškove nastale stvarnim korištenjem (voda, struja, "
            f"plin iznad baznog minimuma),<br>"
            f"&nbsp;&nbsp;b) dnevno čišćenje u razdoblju korištenja,<br>"
            f"&nbsp;&nbsp;c) potrošni materijal (posteljina, higijenski proizvodi, osnovna kućna kemija),<br>"
            f"&nbsp;&nbsp;d) troškove habanja opreme nastale redovnom uporabom.<br><br>"
            f"(3) Naknada za korištenje obračunava se mjesečno na temelju evidencije "
            f"popunjenosti koju vodi Davatelj. Račun se ispostavlja najkasnije do "
            f"10. u mjesecu za prethodni mjesec, s rokom plaćanja od 15 dana od "
            f"primitka računa.<br><br>"
            f"(4) Naručitelj ima pravo uvida u evidenciju popunjenosti u bilo "
            f"kojem trenutku."
            f"</div>"
        )

        # -- VII. TRANSPARENTNOST I IZVJESTAVANJE (OPEN-BOOK) --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"VII. TRANSPARENTNOST I IZVJEŠTAVANJE (OPEN-BOOK)</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 8.</div>"
            f"<div class='justified'>"
            f"(1) Davatelj se obvezuje Naručitelju kvartalno dostavljati "
            f"Izvještaj o strukturi troškova koji na transparentan način prikazuje:<br>"
            f"&nbsp;&nbsp;a) ukupne najamnine plaćene vlasnicima nekretnina,<br>"
            f"&nbsp;&nbsp;b) troškove komunalnih usluga (po kategorijama),<br>"
            f"&nbsp;&nbsp;c) troškove održavanja i čišćenja,<br>"
            f"&nbsp;&nbsp;d) troškove osiguranja,<br>"
            f"&nbsp;&nbsp;e) operativnu naknadu Davatelja (management fee).<br><br>"
            f"(2) Naručitelj ima pravo jednom godišnje, o svom trošku, angažirati "
            f"neovisnog ovlaštenog revizora radi provjere točnosti Izvještaja "
            f"o strukturi troškova. Davatelj se obvezuje pružiti revizoru "
            f"potpun pristup relevantnoj dokumentaciji u roku od 15 radnih dana "
            f"od zahtjeva.<br><br>"
            f"(2a) Ukoliko tri uzastopna kvartalna izvještaja pokažu odstupanje "
            f"troškova manje od 5% od projiciranih, frekvencija izvještavanja "
            f"prelazi na polugodišnju. Ukoliko bilo koji izvještaj pokaže "
            f"odstupanje veće od 15%, frekvencija izvještavanja prelazi na "
            f"mjesečnu za sljedeća dva kvartala.<br><br>"
            f"(2b) Prijelazi iz stavka (2a) nastupaju automatski, bez potrebe "
            f"za suglasnošću bilo koje strane.<br><br>"
            f"(3) Ukoliko revizija utvrdi odstupanje veće od 5% u korist "
            f"Davatelja, Davatelj se obvezuje Naručitelju vratiti razliku "
            f"uvećanu za zakonsku zateznu kamatu, te snositi troškove revizije."
            f"</div>"
        )

        # -- VIII. STANDARDI KVALITETE USLUGE (SLA) --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"VIII. STANDARDI KVALITETE USLUGE (SLA)</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 9.</div>"
            f"<div class='justified'>"
            f"(1) Davatelj se obvezuje na sljedeće standarde kvalitete:</div>"
            f"<table class='cost-table'>"
            f"<tr style='font-weight:bold;background:#f0f0f0;'>"
            f"<td>Parametar</td><td>Standard</td><td>Mjerenje</td></tr>"
            f"<tr><td>Spremnost smještaja za check-in</td><td>24 sata od pisane najave</td><td>Po incidentu</td></tr>"
            f"<tr><td>Hitni popravak (curenje, kvar grijanja, brave)</td><td>Početak radova unutar 4 sata</td><td>Po incidentu</td></tr>"
            f"<tr><td>Redovni popravak (ostalo)</td><td>Unutar 48 sati od prijave</td><td>Po incidentu</td></tr>"
            f"<tr><td>Inspekcija i čišćenje praznih jedinica</td><td>Jednom tjedno</td><td>Mjesečni izvještaj</td></tr>"
            f"<tr><td>Odgovor na upit Naručitelja</td><td>Unutar 4 radna sata</td><td>Po upitu</td></tr>"
            f"<tr><td>Mjesečni izvještaj</td><td>Do 10. u mjesecu za prethodni</td><td>Mjesečno</td></tr>"
            f"</table>"
            f"<div class='justified'>"
            f"(2) U slučaju neispunjenja standarda iz stavka (1), Naručitelj ima "
            f"pravo na umanjenje Naknade za upravljanje kapacitetom:<br>"
            f"&nbsp;&nbsp;a) za svaki propust u kategoriji \u201EHitni popravak\u201C \u2014 umanjenje od "
            f"<b>{sla_hitni}</b> po incidentu,<br>"
            f"&nbsp;&nbsp;b) za propust u kategoriji \u201ESpremnost za check-in\u201C \u2014 umanjenje od "
            f"<b>{sla_checkin}</b> po incidentu, ukoliko je Naručitelj morao "
            f"organizirati alternativni smještaj za Radnike,<br>"
            f"&nbsp;&nbsp;c) za sustavno neispunjavanje (3 ili više propusta u jednom "
            f"kalendarskom mjesecu) \u2014 pravo na umanjenje Naknade za tekući mjesec za 10%.<br><br>"
            f"(3) Umanjenja iz stavka (2) NE predstavljaju ugovornu kaznu, već "
            f"kompenzaciju za neisporučenu uslugu, i kao takva ne podliježu "
            f"ograničenjima iz članka 354. Zakona o obveznim odnosima.<br><br>"
            f"(4) Svaki SLA parametar iz stavka (1) podložan je godišnjoj "
            f"rekalibraciji na temelju stvarnih operativnih podataka prethodne "
            f"godine. Prijedlog rekalibracije podnosi Davatelj, obrazložen "
            f"statističkom analizom ostvarenih performansi. Naručitelj odobrava "
            f"ili obrazloženo odbija u roku od 60 (šezdeset) dana.<br><br>"
            f"(5) Parametri koji su u prethodnoj godini ispunjeni u više od 95% "
            f"slučajeva smatraju se kandidatima za pooštravanje. Parametri "
            f"ispunjeni u manje od 70% slučajeva smatraju se kandidatima za "
            f"reviziju metodologije mjerenja.<br><br>"
            f"(6) Ukoliko pojačani režim izvještavanja iz članka 8. stavka (2a) "
            f"traje dulje od 6 (šest) uzastopnih mjeseci, stranke su dužne u roku "
            f"od 30 dana pokrenuti zajedničku reviziju samog mehanizma izvještavanja "
            f"i mjerenja, uključujući mogućnost promjene metrika, pragova ili "
            f"metodologije. Predmet revizije nisu obveze Strana, nego sustav "
            f"njihova mjerenja."
            f"</div>"
        )

        # -- IX. FLEKSIBILNOST KAPACITETA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"IX. FLEKSIBILNOST KAPACITETA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 10.</div>"
            f"<div class='justified'>"
            f"(1) <b>Povećanje kapaciteta:</b> Naručitelj može u bilo kojem trenutku "
            f"pisanim putem zatražiti povećanje Baznog kapaciteta. Davatelj će "
            f"učiniti razumne napore da udovolji zahtjevu u roku od 30 dana, "
            f"koristeći raspoložive kapacitete u svom portfelju. Cijena dodatnog "
            f"kapaciteta utvrđuje se aneksom ovom Ugovoru, po uvjetima razmjernima postojećima.<br><br>"
            f"(2) <b>Smanjenje kapaciteta:</b> Naručitelj može jednom godišnje, "
            f"pisanom obaviješću s rokom od 90 (devedeset) dana, zatražiti smanjenje "
            f"Baznog kapaciteta za najviše 20% ukupnog broja. Smanjeni Bazni kapacitet "
            f"postaje novi referentni kapacitet za izračun Naknade za upravljanje "
            f"kapacitetom počev od prvog dana mjeseca koji slijedi isteku roka od 90 dana.<br><br>"
            f"(3) Bazni kapacitet ne može se smanjiti ispod <b>{min_kap}</b> kreveta "
            f"/ smještajnih jedinica (u daljnjem tekstu: \u201EMinimalni kapacitet\u201C), "
            f"što predstavlja prag ispod kojeg Davatelj ne može održati operativnu "
            f"i financijsku održivost sustava.<br><br>"
            f"(4) Ukoliko Naručitelj želi smanjenje ispod Minimalnog kapaciteta, "
            f"to se tretira kao prijevremeni raskid Ugovora u smislu članka 14."
            f"</div>"
        )

        # -- X. RE-MONETIZACIJA NEISKORISTENOG KAPACITETA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"X. RE-MONETIZACIJA NEISKORIŠTENOG KAPACITETA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 11.</div>"
            f"<div class='justified'>"
            f"(1) Naručitelj ima isključivo pravo određivanja kapaciteta koji "
            f"se stavlja u aktivan režim te prioriteta popunjavanja. Davatelj "
            f"ima isključivo pravo operativnog upravljanja, odabira gostiju i "
            f"formiranja cijene za Re-monetizaciju neiskorištenog kapaciteta.<br><br>"
            f"(1a) Prava iz stavka (1) neprenosiva su i neotuđiva za vrijeme "
            f"trajanja Ugovora, osim prijenosa na povezano društvo u smislu "
            f"Zakona o trgovačkim društvima.<br><br>"
            f"(1b) Ukoliko prosječna mjesečna popunjenost Baznog kapaciteta "
            f"Radnicima Naručitelja padne ispod 50% (pedeset posto) u razdoblju "
            f"duljem od 60 (šezdeset) uzastopnih dana, Davatelj stječe pravo na "
            f"Re-monetizaciju slobodnog kapaciteta.<br><br>"
            f"(2) Re-monetizacija znači privremeno plasiranje neiskorištenih "
            f"smještajnih jedinica na tržište kratkoročnog smještaja (turistički, "
            f"poslovni ili tranzitni), bez prenošenja bilo kakvih vlasničkih ili "
            f"korisničkih prava na treće osobe koja bi ograničavala prava Naručitelja.<br><br>"
            f"(3) Naručiteljevi Radnici u svakom trenutku imaju PREDNOST pri "
            f"alokaciji kapaciteta. Davatelj je dužan osigurati da se Re-monetizacija "
            f"ne vrši na način koji bi ugrozio mogućnost smještaja Radnika "
            f"Naručitelja, uz obvezu oslobađanja re-monetiziranih jedinica u "
            f"roku od 72 sata od Naručiteljeve pisane najave potrebe za dodatnim kapacitetom.<br><br>"
            f"(4) Prihod ostvaren Re-monetizacijom raspodjeljuje se kako slijedi:<br>"
            f"&nbsp;&nbsp;a) 70% neto prihoda uračunava se (odobrava) Naručitelju kao "
            f"umanjenje sljedeće mjesečne Naknade za upravljanje kapacitetom,<br>"
            f"&nbsp;&nbsp;b) 30% neto prihoda zadržava Davatelj kao naknadu za operativni "
            f"rad organizacije kratkoročnog smještaja.<br><br>"
            f"(4a) Ukoliko Naručitelj smanji kapacitet za više od 10% u kvartalu "
            f"bez prethodne najave od 60 (šezdeset) dana, omjer Re-monetizacije "
            f"preostalog kapaciteta prelazi na 50:50 za taj kvartal.<br><br>"
            f"(5) Davatelj je dužan Naručitelju mjesečno dostavljati izvještaj "
            f"o Re-monetizaciji koji sadrži: broj re-monetiziranih jedinica, "
            f"broj noćenja, ostvareni prihod, i izračun odobrenja za Naručitelja.<br><br>"
            f"(6) Svrha Re-monetizacije je SMANJITI efektivni trošak Naručitelja "
            f"u razdobljima smanjene potrebe za kapacitetom. Ugovorne strane "
            f"izričito utvrđuju da Re-monetizacija predstavlja ugrađeni "
            f"mehanizam prilagodbe koji zamjenjuje potrebu za pregovorima o "
            f"umanjenju Naknade u slučaju smanjene popunjenosti."
            f"</div>"
        )

        # -- XI. TRAJANJE UGOVORA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"XI. TRAJANJE UGOVORA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 12.</div>"
            f"<div class='justified'>"
            f"(1) Ovaj Ugovor sklapa se na određeno vrijeme u trajanju od "
            f"<b>{trajanje_mj}</b> mjeseci, počev od <b>{datum_pocetka_str}</b> "
            f"(u daljnjem tekstu: \u201EUgovorno razdoblje\u201C).<br><br>"
            f"(2) Ugovor se automatski produljuje za daljnjih 12 (dvanaest) "
            f"mjeseci, osim ako bilo koja strana dostavi drugoj pisani otkaz "
            f"najmanje 120 (sto dvadeset) dana prije isteka Ugovornog razdoblja "
            f"ili bilo kojeg produljenog razdoblja.<br><br>"
            f"(3) Pisani otkaz dostavlja se preporučenom poštom s povratnicom "
            f"na adresu sjedišta druge strane navedenu u zaglavlju ovog Ugovora, "
            f"ili na drugu adresu koju strana pisano priopći."
            f"</div>"
        )

        # -- XII. PRIJEVREMENI RASKID --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"XII. PRIJEVREMENI RASKID</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 13.</div>"
            f"<div class='justified'>"
            f"(1) Svaka strana može raskinuti Ugovor prije isteka Ugovornog "
            f"razdoblja ako:<br>"
            f"&nbsp;&nbsp;a) druga strana bitno povrijedi svoje obveze iz ovog Ugovora i "
            f"ne otkloni povredu u roku od 30 dana od primitka pisane opomene,<br>"
            f"&nbsp;&nbsp;b) nad drugom stranom je otvoren stečajni ili predstečajni postupak,<br>"
            f"&nbsp;&nbsp;c) druga strana izgubi pravnu sposobnost ili poslovnu dozvolu "
            f"nužnu za ispunjenje ovog Ugovora.<br><br>"
            f"(2) Kao bitna povreda od strane Naručitelja smatra se osobito:<br>"
            f"&nbsp;&nbsp;a) kašnjenje s plaćanjem Naknade za upravljanje kapacitetom za "
            f"više od 30 dana,<br>"
            f"&nbsp;&nbsp;b) opetovano kašnjenje s plaćanjem (3 ili više puta u 12 mjeseci).<br><br>"
            f"(3) Kao bitna povreda od strane Davatelja smatra se osobito:<br>"
            f"&nbsp;&nbsp;a) nemogućnost osiguranja Baznog kapaciteta u trajanju duljem od 15 dana,<br>"
            f"&nbsp;&nbsp;b) sustavno neispunjavanje SLA standarda iz članka 9. (5 ili više "
            f"propusta u 2 uzastopna mjeseca)."
            f"</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 14.</div>"
            f"<div class='justified'>"
            f"(1) Ukoliko Naručitelj želi raskinuti Ugovor prije isteka Ugovornog "
            f"razdoblja, a razlog raskida NIJE bitna povreda Davatelja iz članka "
            f"13. stavka (1) točke a), Naručitelj se obvezuje Davatelju naknaditi "
            f"stvarnu štetu nastalu prijevremenim raskidom.<br><br>"
            f"(2) Stvarna šteta iz stavka (1) obuhvaća:<br>"
            f"&nbsp;&nbsp;a) najamnine koje Davatelj ostaje dužan platiti vlasnicima "
            f"nekretnina za preostalo ugovoreno razdoblje najma, umanjene za prihode "
            f"koje Davatelj ostvari ili bi mogao ostvariti razumnim nastojanjima "
            f"(re-monetizacijom ili pronalaženjem novog klijenta),<br>"
            f"&nbsp;&nbsp;b) troškove prijevremenog raskida ugovora s dobavljačima usluga "
            f"(čišćenje, održavanje) koji su sklopljeni radi ispunjenja ovog Ugovora.<br><br>"
            f"(3) Iznos naknade iz stavka (2) izračunava se temeljem:<br>"
            f"&nbsp;&nbsp;a) ugovora o najmu s vlasnicima nekretnina (prikazanih u "
            f"Izvještaju o strukturi troškova),<br>"
            f"&nbsp;&nbsp;b) razumnog roka potrebnog Davatelju da pronađe zamjenu ili "
            f"izvrši Re-monetizaciju (ali ne dulji od 6 mjeseci),<br>"
            f"&nbsp;&nbsp;c) stvarnih troškova prijevremenog raskida s dobavljačima.<br><br>"
            f"(4) Davatelj se obvezuje poduzeti razumne napore da umanji štetu "
            f"(čl. 346. ZOO) te će Naručitelju predočiti dokumentaciju o "
            f"poduzetim mjerama i ostvarenim ili propuštenim prihodima.<br><br>"
            f"(5) Ugovorne strane izričito utvrđuju da naknada iz ovog članka "
            f"predstavlja naknadu STVARNE ŠTETE u smislu članka 346. Zakona o "
            f"obveznim odnosima, a NE ugovornu kaznu u smislu članka 350. istog "
            f"Zakona, te stoga NE podliježe sudskom smanjenju iz članka 354. ZOO."
            f"</div>"
        )

        # -- XIII. ZASTITA OD KONTAKTIRANJA STANODAVACA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"XIII. ZAŠTITA OD KONTAKTIRANJA STANODAVACA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 15.</div>"
            f"<div class='justified'>"
            f"(1) Naručitelj se obvezuje da za vrijeme trajanja ovog Ugovora "
            f"i 12 (dvanaest) mjeseci nakon njegovog prestanka neće izravno "
            f"ili neizravno kontaktirati vlasnike nekretnina iz Davateljevog "
            f"portfelja u svrhu sklapanja zasebnih ugovora o najmu ili bilo "
            f"kakvog poslovnog aranžmana vezanog uz smještajne kapacitete.<br><br>"
            f"(2) U slučaju povrede obveze iz stavka (1), Naručitelj je dužan "
            f"Davatelju platiti ugovornu kaznu u iznosu od <b>{kazna_kontakt}</b>, "
            f"što ne isključuje pravo Davatelja na naknadu štete koja prelazi "
            f"iznos ugovorne kazne."
            f"</div>"
        )

        # -- XIV. BANKOVNA GARANCIJA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"XIV. BANKOVNA GARANCIJA / OSIGURANJE PLAĆANJA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 16.</div>"
            f"<div class='justified'>"
            f"(1) Naručitelj se obvezuje najkasnije u roku od 15 dana od "
            f"potpisa ovog Ugovora dostaviti Davatelju bezuvjetnu i neopozivu "
            f"bankovnu garanciju / bjanko zadužnicom u iznosu koji odgovara "
            f"trima (3) mjesečnim Naknadama za upravljanje kapacitetom, kao "
            f"osiguranje urednog ispunjavanja novčanih obveza.<br><br>"
            f"(2) Bankovna garancija / bjanko zadužnica važi za cijelo "
            f"Ugovorno razdoblje i vraća se Naručitelju u roku od 30 dana od "
            f"urednog okončanja Ugovora.<br><br>"
            f"(3) Davatelj ima pravo aktivirati garanciju / zadužnicu ako "
            f"Naručitelj kasni s plaćanjem više od 30 dana i nije otklonio "
            f"kašnjenje u dodatnom roku od 15 dana od pisane opomene."
            f"</div>"
        )

        # -- XV. ODGOVORNOST ZA STETE --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"XV. ODGOVORNOST ZA ŠTETE</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 17.</div>"
            f"<div class='justified'>"
            f"(1) Davatelj odgovara za štetu na imovini Naručitelja ili "
            f"Radnika koja nastane zbog dokazanog nemara ili propusta Davatelja "
            f"u održavanju smještajnih jedinica.<br><br>"
            f"(2) Naručitelj odgovara za štetu na smještajnim jedinicama i "
            f"opremi koju uzrokuju Radnici, iznad uobičajene amortizacije. "
            f"Šteta se utvrđuje na temelju fotografske dokumentacije pri "
            f"primopredaji i inspekcijskih izvještaja.<br><br>"
            f"(3) Odgovornost svake strane za štetu ograničena je na iznos "
            f"ukupne godišnje Naknade za upravljanje kapacitetom, osim u "
            f"slučajevima namjere ili krajnje nepažnje."
            f"</div>"
        )

        # -- XVI. POVJERLJIVOST --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"XVI. POVJERLJIVOST</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 18.</div>"
            f"<div class='justified'>"
            f"(1) Sve informacije koje strane razmijene u vezi s ovim Ugovorom, "
            f"uključujući financijske podatke, uvjete ugovora, Izvještaje o "
            f"strukturi troškova i poslovne tajne, smatraju se povjerljivima.<br><br>"
            f"(2) Strane se obvezuju te informacije ne otkrivati trećim osobama "
            f"bez prethodne pisane suglasnosti druge strane, osim:<br>"
            f"&nbsp;&nbsp;a) ako je otkrivanje potrebno radi ispunjenja zakonskih obveza,<br>"
            f"&nbsp;&nbsp;b) prema zahtjevu suda ili drugog nadležnog tijela,<br>"
            f"&nbsp;&nbsp;c) profesionalnim savjetnicima (odvjetnicima, revizorima) koji "
            f"su vezani vlastitom obvezom povjerljivosti.<br><br>"
            f"(3) Obveza povjerljivosti traje za cijelo vrijeme trajanja ovog "
            f"Ugovora i 24 (dvadeset četiri) mjeseca nakon njegovog prestanka."
            f"</div>"
        )

        # -- XVII. RJESAVANJE SPOROVA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"XVII. RJEŠAVANJE SPOROVA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 19.</div>"
            f"<div class='justified'>"
            f"(1) Ugovorne strane će svaki spor iz ovog Ugovora nastojati "
            f"riješiti mirnim putem.<br><br>"
            f"(2) Ukoliko spor nije moguće riješiti mirnim putem u roku od 30 "
            f"dana od dana kada je jedna strana pisano obavijestila drugu o "
            f"postojanju spora, strane će pokrenuti postupak mirenja pri "
            f"Stalnom izabranom sudištu Hrvatske gospodarske komore (HGK).<br><br>"
            f"(3) Ukoliko se spor ne riješi mirenjem u roku od 60 dana od "
            f"pokretanja postupka, za rješavanje spora bit će nadležan stvarno "
            f"nadležni sud u <b>{sud_mjesto}</b>."
            f"</div>"
        )

        # -- XVIII. VISA SILA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"XVIII. VIŠA SILA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 20.</div>"
            f"<div class='justified'>"
            f"(1) Nijedna strana neće odgovarati za neispunjenje ili zakašnjelo "
            f"ispunjenje obveza iz ovog Ugovora koje je uzrokovano okolnostima "
            f"više sile (elementarne nepogode, rat, epidemija, vladine mjere "
            f"koje onemogućuju ispunjenje, i sl.).<br><br>"
            f"(2) Strana koja se poziva na višu silu dužna je o tome bez "
            f"odgađanja obavijestiti drugu stranu i poduzeti razumne mjere "
            f"za ublažavanje posljedica.<br><br>"
            f"(3) Ukoliko viša sila traje dulje od 90 (devedeset) uzastopnih "
            f"dana, svaka strana može raskinuti Ugovor pisanom izjavom, uz "
            f"obvezu pokrića samo već nastalih, dospjelih obveza do dana raskida."
            f"</div>"
        )

        # -- XIX. ZASTITA OSOBNIH PODATAKA --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"XIX. ZAŠTITA OSOBNIH PODATAKA</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 21.</div>"
            f"<div class='justified'>"
            f"(1) Ukoliko Davatelj u okviru izvršavanja ovog Ugovora obrađuje "
            f"osobne podatke Radnika Naručitelja, strane će sklopiti zaseban "
            f"Ugovor o obradi osobnih podataka sukladno Uredbi (EU) 2016/679 "
            f"(Opća uredba o zaštiti podataka \u2014 GDPR) i Zakonu o provedbi "
            f"Opće uredbe o zaštiti podataka (NN 42/18).<br><br>"
            f"(2) Davatelj se obvezuje obrađivati osobne podatke Radnika "
            f"isključivo u mjeri nužnoj za ispunjenje obveza iz ovog Ugovora "
            f"(check-in/check-out, alokacija kapaciteta, evidencija)."
            f"</div>"
        )

        # -- XX. ZAVRSNE ODREDBE --
        parts.append(
            f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
            f"XX. ZAVRŠNE ODREDBE</div>"
        )
        parts.append(
            f"<div class='section-title' style='text-align: center;'>Članak 22.</div>"
            f"<div class='justified'>"
            f"(1) Ovaj Ugovor sastavljen je u 4 (četiri) istovjetna primjerka, "
            f"po 2 (dva) za svaku ugovornu stranu.<br><br>"
            f"(2) Na sve što ovim Ugovorom nije uređeno, primjenjuju se odredbe "
            f"Zakona o obveznim odnosima (NN 35/05, 41/08, 125/11, 78/15, 29/18, "
            f"126/21, 114/22, 156/22, 155/23).<br><br>"
            f"(3) Izmjene i dopune ovog Ugovora valjane su samo u pisanom obliku "
            f"(aneks), potpisanom od obiju ugovornih strana.<br><br>"
            f"(4) Ništavost pojedine odredbe ovog Ugovora ne utječe na valjanost "
            f"ostalih odredbi, a strane će ništavnu odredbu zamijeniti valjanom "
            f"koja najbliže odgovara ekonomskom cilju ništavne odredbe.<br><br>"
            f"(5) Prilozi ovog Ugovora čine njegov sastavni dio:<br>"
            f"&nbsp;&nbsp;- <b>Prilog 1:</b> Specifikacija smještajnog kapaciteta (adrese, "
            f"broj jedinica/kreveta, opremljenost)<br>"
            f"&nbsp;&nbsp;- <b>Prilog 2:</b> Kućni red<br>"
            f"&nbsp;&nbsp;- <b>Prilog 3:</b> Izvještaj o strukturi troškova (inicijalni)<br><br>"
            f"(6) Ovaj Ugovor stupa na snagu danom potpisa obiju ugovornih strana."
            f"</div>"
        )

        # -- PRILOG 1: Specifikacija --
        if spec_rows:
            parts.append(
                f"<div class='header-doc' style='font-size: 12pt; margin-top: 30px;'>"
                f"PRILOG 1: Specifikacija smještajnog kapaciteta</div>"
            )
            parts.append(
                f"<table class='cost-table'>"
                f"<tr style='font-weight:bold;background:#f0f0f0;'>"
                f"<td>R.br.</td><td>Adresa nekretnine</td><td>Br. soba</td>"
                f"<td>Br. kreveta</td><td>Opremljenost</td><td>Napomena</td></tr>"
            )
            for idx, row in enumerate(spec_rows, 1):
                parts.append(
                    f"<tr><td>{idx}.</td>"
                    f"<td>{_escape(row.get('adresa', ''))}</td>"
                    f"<td>{_escape(str(row.get('sobe', '')))}</td>"
                    f"<td>{_escape(str(row.get('kreveti', '')))}</td>"
                    f"<td>{_escape(row.get('opremljenost', ''))}</td>"
                    f"<td>{_escape(row.get('napomena', ''))}</td></tr>"
                )
            parts.append(f"</table>")

        # -- PRILOG 3: Struktura troskova napomena --
        parts.append(
            f"<div class='justified' style='margin-top: 20px; font-style: italic;'>"
            f"<b>PRILOG 2:</b> Kućni red (utvrđuje Davatelj)<br>"
            f"<b>PRILOG 3:</b> Izvještaj o strukturi troškova (inicijalni)"
        )
        if max_mgmt_fee:
            parts.append(
                f"<br>Davatelj se obvezuje da operativna naknada Davatelja ne prelazi "
                f"<b>{max_mgmt_fee}%</b> ukupne Naknade za upravljanje kapacitetom."
            )
        parts.append(f"</div>")

        # -- Potpisi --
        parts.append(
            f"<div class='signature-row'>"
            f"<div class='signature-block'>"
            f"<b>DAVATELJ (B)</b><br><br><br>________________________"
            f"</div>"
            f"<div class='signature-block'>"
            f"<b>NARUČITELJ (C)</b><br><br><br>________________________"
            f"</div>"
            f"</div>"
        )

        return "".join(parts)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
