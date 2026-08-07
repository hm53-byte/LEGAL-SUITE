# -----------------------------------------------------------------------------
# GENERATORI: Iznajmljivanje apartmana (suglasnosti, MTU, kategorizacija)
# Pravni temelj:
#   - Zakon o ugostiteljskoj djelatnosti (NN 85/15 i izmjene)
#   - Pravilnik o razvrstavanju i kategorizaciji ugostiteljskih objekata iz
#     skupine OSTALO (NN 56/16) — kategorizacija apartmana
#   - Pravilnik o razvrstavanju i kategorizaciji objekata u kojima se pruzaju
#     ugostiteljske usluge u domacinstvu (NN 9/16) — MTU za sobe/apartmane
#   - Zakon o vlasnistvu i drugim stvarnim pravima (NN 91/96 ...)
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, u_lokativu


def _opis_nekretnine(podaci):
    adresa = format_text(podaci.get('adresa', ''))
    kat_opis = format_text(podaci.get('kat_opis', ''))
    ko = format_text(podaci.get('ko', ''))
    cestica = format_text(podaci.get('cestica', ''))
    ulozak = format_text(podaci.get('ulozak', ''))
    povrsina = format_text(podaci.get('povrsina_m2', ''))
    broj_smjestaja = format_text(podaci.get('broj_smjestajnih_jedinica', ''))

    rows = []
    if adresa:
        rows.append(f"<b>Adresa:</b> {adresa}")
    if kat_opis:
        rows.append(f"<b>Opis (kat/jedinica):</b> {kat_opis}")
    if ko or cestica or ulozak:
        rows.append(f"<b>K.O. / k.č.br. / zk.ul.:</b> {ko} / {cestica} / {ulozak}")
    if povrsina:
        rows.append(f"<b>Površina (m²):</b> {povrsina}")
    if broj_smjestaja:
        rows.append(f"<b>Broj smještajnih jedinica:</b> {broj_smjestaja}")
    return "<br>".join(rows)


def generiraj_suglasnost_obitelji(vlasnik, korisnik, podaci):
    """Suglasnost vlasnika nekretnine clanu obitelji za iznajmljivanje turistima.

    Tipican use-case: roditelj vlasnik kuce daje suglasnost djetetu da na svoje ime
    ishodi MTU rjesenje i kategorizaciju, te iznajmljuje turistima.
    """
    try:
        srodstvo = format_text(podaci.get('srodstvo', 'član obitelji'))
        rok = format_text(podaci.get('rok_vazenja', 'do opoziva ove suglasnosti u pisanom obliku'))
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        opis = _opis_nekretnine(podaci)

        return (
            f"<div class='header-doc'>SUGLASNOST<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>vlasnika nekretnine za pružanje ugostiteljskih usluga</span></div>"
            f"<div class='justified'>Ja, dolje potpisani/a:</div><br>"
            f"<div class='party-info'><b>VLASNIK NEKRETNINE:</b><br>{vlasnik}</div><br>"
            f"<div class='justified'>kao vlasnik (ili suvlasnik) niže opisane nekretnine, ovime dajem</div><br>"
            f"<div style='text-align: center; font-weight: bold; font-size: 14pt; margin: 20px 0;'>SUGLASNOST</div>"
            f"<div class='party-info'><b>KORISNIKU SUGLASNOSTI:</b><br>{korisnik}<br>(srodstvo: {srodstvo})</div><br>"
            f"<div class='justified'>za korištenje sljedeće nekretnine:</div><br>"
            f"<div class='doc-body'>{opis}</div>"
            f"<div class='section-title'>OPSEG SUGLASNOSTI</div>"
            f"<div class='doc-body'>Korisnik suglasnosti ovlašten je u svoje ime i za svoj račun:<br><br>"
            f"<ol>"
            f"<li>iznajmljivati gore opisanu nekretninu (ili njezine smještajne jedinice) turistima i drugim "
            f"gostima radi pružanja usluge smještaja;</li>"
            f"<li>kod nadležnog ureda državne uprave u županiji (turistička inspekcija / ured za gospodarstvo) "
            f"podnositi zahtjeve i obavljati sve radnje radi ishođenja rješenja o ispunjavanju minimalnih "
            f"tehničkih uvjeta (MTU) i rješenja o razvrstavanju i kategorizaciji ugostiteljskog objekta;</li>"
            f"<li>prijaviti pružanje ugostiteljske djelatnosti u domaćinstvu / iznajmljivanje turistima u svoje ime;</li>"
            f"<li>sklapati ugovore s posrednicima (Booking, Airbnb, agencije) i s gostima;</li>"
            f"<li>obavljati sve administrativne i porezne radnje vezane uz iznajmljivanje (paušalni porez, boravišna "
            f"pristojba, prijava gostiju u eVisitor i sl.);</li>"
            f"<li>poduzimati uobičajene radnje održavanja i opremanja nekretnine za turističku namjenu, bez prava "
            f"prodaje, opterećenja ili drugih oblika raspolaganja vlasništvom.</ol></div>"
            f"<div class='section-title'>VAŽENJE</div>"
            f"<div class='doc-body'>Ova Suglasnost vrijedi {rok}. Vlasnik zadržava pravo opozvati Suglasnost "
            f"u pisanom obliku, uz razumni rok obavještavanja koji ne ograničava već preuzete obveze prema "
            f"trećim osobama (gosti, posrednici).</div>"
            f"<div class='section-title'>NAPOMENA</div>"
            f"<div class='doc-body'>Ovom Suglasnosti se <b>ne prenosi</b> pravo vlasništva niti se ono mijenja. "
            f"Suglasnost služi isključivo kao pravna osnova za korištenje nekretnine u svrhu obavljanja "
            f"ugostiteljske djelatnosti od strane Korisnika suglasnosti.</div>"
            f"<br>"
            f"<div class='justified'>U {u_lokativu(mjesto)}, dana {datum}.</div><br>"
            f"<table width='100%'><tr>"
            f"<td width='40%'></td>"
            f"<td width='60%' align='center'><b>VLASNIK NEKRETNINE</b><br>(potpis ovjeren kod javnog bilježnika)<br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_suglasnost_suvlasnika(suvlasnici, predlagatelj, podaci):
    """Suglasnost suvlasnika nekretnine za pruzanje ugostiteljskih usluga (kad je suvlasnistvo)."""
    try:
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        opis = _opis_nekretnine(podaci)
        suvl_html = suvlasnici if isinstance(suvlasnici, str) else "<br><br>".join(suvlasnici)

        return (
            f"<div class='header-doc'>SUGLASNOST SUVLASNIKA<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>za pružanje ugostiteljskih usluga u nekretnini</span></div>"
            f"<div class='party-info'><b>SUVLASNICI (potpisnici suglasnosti):</b><br>{suvl_html}</div><br>"
            f"<div class='party-info'><b>PREDLAGATELJ (suvlasnik koji ishođuje rješenja):</b><br>{predlagatelj}</div><br>"
            f"<div class='justified'>Mi, suvlasnici niže opisane nekretnine, ovime izričito i bezuvjetno dajemo</div><br>"
            f"<div style='text-align: center; font-weight: bold; font-size: 14pt; margin: 20px 0;'>SUGLASNOST</div>"
            f"<div class='justified'>da Predlagatelj, u svoje ime, podnese nadležnom uredu državne uprave "
            f"zahtjev i ishodi:</div>"
            f"<div class='doc-body'><ol>"
            f"<li>rješenje o ispunjavanju minimalnih tehničkih uvjeta (MTU) za pružanje ugostiteljskih usluga "
            f"u domaćinstvu;</li>"
            f"<li>rješenje o razvrstavanju i kategorizaciji ugostiteljskog objekta;</li>"
            f"<li>obavi sve daljnje radnje potrebne za otpočinjanje pružanja ugostiteljskih usluga "
            f"(prijava djelatnosti, evidencije, porezne prijave).</ol></div>"
            f"<div class='justified'>Suglasnost se daje za sljedeću nekretninu:</div><br>"
            f"<div class='doc-body'>{opis}</div>"
            f"<div class='doc-body'>Suvlasnici su suglasni da se nekretnina koristi za turističko iznajmljivanje "
            f"i da su upoznati sa svim posljedicama te djelatnosti, uključujući porezne i komunalne obveze. "
            f"Međusobni odnosi suvlasnika u pogledu prihoda od iznajmljivanja uredit će se posebnim sporazumom.</div>"
            f"<br>"
            f"<div class='justified'>U {u_lokativu(mjesto)}, dana {datum}.</div><br>"
            f"<div class='doc-body'><b>POTPISI SUVLASNIKA</b><br><br>"
            f"_______________________________ &nbsp; &nbsp; (ime i prezime, OIB)<br><br>"
            f"_______________________________ &nbsp; &nbsp; (ime i prezime, OIB)<br><br>"
            f"_______________________________ &nbsp; &nbsp; (ime i prezime, OIB)<br><br>"
            f"<i>Potpisi se ovjeravaju kod javnog bilježnika.</i></div>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_zahtjev_mtu(podnositelj, podaci):
    """Zahtjev za izdavanje rjesenja o ispunjavanju minimalnih tehnickih uvjeta (MTU).

    Pravilnik NN 9/16 — pruzanje ugostiteljskih usluga u domacinstvu.
    Podnosi se uredu drzavne uprave / upravnom odjelu zupanije za gospodarstvo.
    """
    try:
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        zupanija = format_text(podaci.get('zupanija', ''))
        nadlezno = format_text(podaci.get('nadlezno_tijelo', ''))
        vrsta_objekta = format_text(podaci.get('vrsta_objekta', 'Apartman'))
        broj_jedinica = format_text(podaci.get('broj_smjestajnih_jedinica', '1'))
        broj_kreveta = format_text(podaci.get('broj_kreveta', ''))
        opis = _opis_nekretnine(podaci)

        primatelj = nadlezno or (
            f"Upravni odjel za gospodarstvo, poljoprivredu i turizam<br>"
            f"{zupanija + ' županija' if zupanija else '(nadležna županija)'}"
        )

        return (
            f"<div style='font-weight: bold; font-size: 14px;'>{primatelj}</div><br><br>"
            f"<div class='party-info'><b>PODNOSITELJ ZAHTJEVA:</b><br>{podnositelj}</div><br>"
            f"<div class='header-doc'>ZAHTJEV<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>za izdavanje rješenja o ispunjavanju minimalnih tehničkih uvjeta (MTU)</span></div>"
            f"<div class='doc-body'>Na temelju Zakona o ugostiteljskoj djelatnosti (NN 85/15 i izmjene) i "
            f"Pravilnika o razvrstavanju i kategorizaciji objekata u kojima se pružaju ugostiteljske usluge "
            f"u domaćinstvu (NN 9/16), podnosim ovaj Zahtjev za izdavanje rješenja kojim se utvrđuje da "
            f"objekt opisan u nastavku ispunjava minimalne tehničke uvjete za pružanje ugostiteljskih usluga.</div>"
            f"<div class='section-title'>I. OPIS OBJEKTA</div>"
            f"<div class='doc-body'>"
            f"<b>Vrsta ugostiteljskog objekta:</b> {vrsta_objekta}<br>"
            f"<b>Broj smještajnih jedinica:</b> {broj_jedinica}<br>"
            f"{'<b>Broj kreveta:</b> ' + broj_kreveta + '<br>' if broj_kreveta else ''}"
            f"{opis}</div>"
            f"<div class='section-title'>II. PRAVNA OSNOVA KORIŠTENJA</div>"
            f"<div class='doc-body'>Podnositelj zahtjeva ima pravo korištenja objekta kao:<br>"
            f"<ul><li>vlasnik / suvlasnik — temeljem izvatka iz zemljišne knjige (prilog), ili</li>"
            f"<li>nositelj suglasnosti vlasnika — temeljem ovjerene Suglasnosti vlasnika nekretnine (prilog).</li></ul></div>"
            f"<div class='section-title'>III. PETIT — ŠTO SE TRAŽI</div>"
            f"<div class='doc-body'>Predlažem da naslovni Upravni odjel <b>donese rješenje</b> kojim se utvrđuje da "
            f"gore opisani objekt ispunjava minimalne tehničke uvjete za pružanje ugostiteljskih usluga u domaćinstvu, "
            f"sukladno Pravilniku NN 9/16, te se podnositelju omogućuje upis u registar pružatelja usluga.</div>"
            f"<div class='section-title'>IV. POPIS PRILOGA</div>"
            f"<div class='doc-body'><ol>"
            f"<li>Izvadak iz zemljišne knjige za predmetnu nekretninu</li>"
            f"<li>Suglasnost vlasnika nekretnine (ako podnositelj nije vlasnik)</li>"
            f"<li>Tlocrt objekta s označenim smještajnim jedinicama</li>"
            f"<li>Preslika osobne iskaznice / OIB podnositelja</li>"
            f"<li>Dokaz o uplati upravne pristojbe</li>"
            f"</ol></div>"
            f"<br>"
            f"<div class='justified'>U {u_lokativu(mjesto)}, dana {datum}.</div><br>"
            f"<table width='100%'><tr>"
            f"<td width='40%'></td>"
            f"<td width='60%' align='center'><b>PODNOSITELJ ZAHTJEVA</b><br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_zahtjev_kategorizacija(podnositelj, podaci):
    """Zahtjev za rjesenje o razvrstavanju i kategorizaciji apartmana/sobe.

    Pravilnik NN 56/16 — kategorizacija ugostiteljskih objekata u skupini OSTALO.
    """
    try:
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        zupanija = format_text(podaci.get('zupanija', ''))
        nadlezno = format_text(podaci.get('nadlezno_tijelo', ''))
        vrsta = format_text(podaci.get('vrsta_objekta', 'Apartman'))
        zatrazena_kat = format_text(podaci.get('zatrazena_kategorija', ''))
        broj_jedinica = format_text(podaci.get('broj_smjestajnih_jedinica', '1'))
        broj_kreveta = format_text(podaci.get('broj_kreveta', ''))
        opremljenost = format_text(podaci.get('opremljenost', ''))
        opis = _opis_nekretnine(podaci)
        mtu_broj = format_text(podaci.get('mtu_klasa', ''))
        mtu_datum = format_text(podaci.get('mtu_datum', ''))

        primatelj = nadlezno or (
            f"Upravni odjel za gospodarstvo, poljoprivredu i turizam<br>"
            f"{zupanija + ' županija' if zupanija else '(nadležna županija)'}"
        )

        kat_html = (
            f"<b>Zatražena kategorija:</b> {zatrazena_kat}<br>"
            if zatrazena_kat else
            "<b>Zatražena kategorija:</b> sukladno utvrđenom činjeničnom stanju<br>"
        )

        mtu_html = ""
        if mtu_broj or mtu_datum:
            mtu_html = (
                f"<div class='doc-body'>Podnositelj se poziva na već izdano rješenje o ispunjavanju "
                f"minimalnih tehničkih uvjeta (MTU) — KLASA/UR.BR.: {mtu_broj}, datum: {mtu_datum}.</div>"
            )

        return (
            f"<div style='font-weight: bold; font-size: 14px;'>{primatelj}</div><br><br>"
            f"<div class='party-info'><b>PODNOSITELJ ZAHTJEVA:</b><br>{podnositelj}</div><br>"
            f"<div class='header-doc'>ZAHTJEV<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>za izdavanje rješenja o razvrstavanju i kategorizaciji ugostiteljskog objekta</span></div>"
            f"<div class='doc-body'>Na temelju Zakona o ugostiteljskoj djelatnosti (NN 85/15) i Pravilnika "
            f"o razvrstavanju i kategorizaciji ugostiteljskih objekata iz skupine OSTALO (NN 56/16), "
            f"podnosim ovaj Zahtjev za donošenje rješenja kojim se objekt razvrstava i kategorizira.</div>"
            f"<div class='section-title'>I. PODACI O OBJEKTU</div>"
            f"<div class='doc-body'>"
            f"<b>Vrsta objekta:</b> {vrsta}<br>"
            f"{kat_html}"
            f"<b>Broj smještajnih jedinica:</b> {broj_jedinica}<br>"
            f"{'<b>Broj kreveta:</b> ' + broj_kreveta + '<br>' if broj_kreveta else ''}"
            f"{opis}"
            f"{f'<br><br><b>Opis opremljenosti i sadržaja:</b><br>{opremljenost}' if opremljenost else ''}"
            f"</div>"
            f"{mtu_html}"
            f"<div class='section-title'>II. PETIT — ŠTO SE TRAŽI</div>"
            f"<div class='doc-body'>Predlažem da naslovni Upravni odjel <b>donese rješenje</b> kojim se objekt "
            f"opisan u točki I. razvrstava u vrstu <b>{vrsta}</b>"
            f"{f' i kategorizira oznakom <b>{zatrazena_kat}</b>' if zatrazena_kat else ' i kategorizira sukladno utvrđenom činjeničnom stanju'}, "
            f"sukladno Pravilniku NN 56/16, te se podnositelju omogućuje upis u registar i otpočinjanje "
            f"pružanja ugostiteljskih usluga.</div>"
            f"<div class='section-title'>III. POPIS PRILOGA</div>"
            f"<div class='doc-body'><ol>"
            f"<li>Rješenje o ispunjavanju minimalnih tehničkih uvjeta (MTU)</li>"
            f"<li>Izvadak iz zemljišne knjige</li>"
            f"<li>Suglasnost vlasnika (ako podnositelj nije vlasnik)</li>"
            f"<li>Tlocrt objekta i fotografije smještajnih jedinica</li>"
            f"<li>Preslika osobne iskaznice / OIB podnositelja</li>"
            f"<li>Dokaz o uplati upravne pristojbe</li>"
            f"</ol></div>"
            f"<br>"
            f"<div class='justified'>U {u_lokativu(mjesto)}, dana {datum}.</div><br>"
            f"<table width='100%'><tr>"
            f"<td width='40%'></td>"
            f"<td width='60%' align='center'><b>PODNOSITELJ ZAHTJEVA</b><br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
