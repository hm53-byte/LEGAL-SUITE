# -----------------------------------------------------------------------------
# GENERATORI: Nautika (brodice, jahte, plovila)
# Pravni temelj: Pomorski zakonik (NN 181/04, 76/07, 146/08, 61/11, 56/13,
#   26/15, 17/19), Zakon o vlasnistvu i drugim stvarnim pravima (NN 91/96 ...)
# Upisnik brodica vodi lucka kapetanija (PZ cl. 213).
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur, format_eur_s_rijecima, u_lokativu


def _identifikacija_brodice(podaci):
    """Vraca HTML blok s identifikacijom brodice koja se ponavlja u svim dokumentima."""
    naziv = format_text(podaci.get('naziv_brodice', ''))
    oznaka = format_text(podaci.get('registracijska_oznaka', ''))
    luka = format_text(podaci.get('luka_upisa', ''))
    kapetanija = format_text(podaci.get('lucka_kapetanija', ''))
    proizvodjac = format_text(podaci.get('proizvodjac', ''))
    model = format_text(podaci.get('model', ''))
    god_proizvodnje = format_text(podaci.get('godina_proizvodnje', ''))
    duljina = format_text(podaci.get('duljina_m', ''))
    motor = format_text(podaci.get('motor', ''))
    snaga_kw = format_text(podaci.get('snaga_kw', ''))
    serijski = format_text(podaci.get('serijski_broj_trupa', ''))

    rows = []
    if naziv:
        rows.append(f"<b>Naziv plovila:</b> {naziv}")
    if oznaka:
        rows.append(f"<b>Registracijska oznaka:</b> {oznaka}")
    if luka:
        rows.append(f"<b>Luka upisa:</b> {luka}")
    if kapetanija:
        rows.append(f"<b>Lučka kapetanija:</b> {kapetanija}")
    if proizvodjac or model:
        rows.append(f"<b>Proizvođač / model:</b> {proizvodjac} {model}".strip())
    if god_proizvodnje:
        rows.append(f"<b>Godina proizvodnje:</b> {god_proizvodnje}")
    if duljina:
        rows.append(f"<b>Duljina (m):</b> {duljina}")
    if motor:
        rows.append(f"<b>Motor:</b> {motor}{' (' + snaga_kw + ' kW)' if snaga_kw else ''}")
    if serijski:
        rows.append(f"<b>Serijski broj trupa (HIN):</b> {serijski}")

    return "<br>".join(rows)


def generiraj_kupoprodaju_brodice(prodavatelj, kupac, podaci):
    """Ugovor o kupoprodaji brodice. Pomorski zakonik + ZOO."""
    try:
        cijena = podaci.get('cijena_eur', 0)
        cijena_str = format_eur(cijena)
        cijena_slovima = format_eur_s_rijecima(cijena) if cijena else ''
        nacin_placanja = format_text(podaci.get('nacin_placanja', 'jednokratno na transakcijski racun prodavatelja'))
        rok_predaje = format_text(podaci.get('rok_predaje', '8 dana od potpisa Ugovora'))
        mjesto_predaje = format_text(podaci.get('mjesto_predaje', ''))
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        tereti = format_text(podaci.get('tereti', 'bez tereta i prava trecih osoba'))

        identifikacija = _identifikacija_brodice(podaci)
        cijena_slovima_html = f" (slovima: {cijena_slovima})" if cijena_slovima else ""

        return (
            f"<div class='header-doc'>UGOVOR O KUPOPRODAJI BRODICE</div>"
            f"<div class='justified'>sklopljen u {u_lokativu(mjesto)} dana {datum} između:</div><br>"
            f"<div class='party-info'><b>PRODAVATELJ:</b><br>{prodavatelj}</div>"
            f"<div class='party-info'><b>KUPAC:</b><br>{kupac}</div><br>"
            f"<div class='section-title'>Članak 1. — PREDMET UGOVORA</div>"
            f"<div class='doc-body'>Predmet ovog Ugovora je kupoprodaja brodice sa sljedećim identifikacijskim podacima:<br><br>"
            f"{identifikacija}</div>"
            f"<div class='section-title'>Članak 2. — KUPOPRODAJNA CIJENA</div>"
            f"<div class='doc-body'>Ugovorne strane suglasno utvrđuju kupoprodajnu cijenu u iznosu od "
            f"<b>{cijena_str}</b>{cijena_slovima_html}. Kupac se obvezuje cijenu platiti {nacin_placanja}.</div>"
            f"<div class='section-title'>Članak 3. — PRAVNO STANJE</div>"
            f"<div class='doc-body'>Prodavatelj jamči da je isključivi vlasnik brodice, da je brodica {tereti}, "
            f"te da na brodici ne postoje sudski sporovi, ovrhe, niti ograničenja prava raspolaganja. "
            f"Prodavatelj jamči da je brodica uredno upisana u Upisnik brodica koji se vodi pri Lučkoj kapetaniji "
            f"navedenoj u članku 1. ovog Ugovora.</div>"
            f"<div class='section-title'>Članak 4. — PREDAJA U POSJED</div>"
            f"<div class='doc-body'>Prodavatelj se obvezuje predati brodicu Kupcu u posjed u roku od {rok_predaje}, "
            f"u stanju u kojem se nalazila u trenutku potpisa ovog Ugovora, sa svim pripadnostima i ispravama "
            f"(Plovidbena dozvola, Knjiga brodice, ovjereni izvadak iz Upisnika, jamstveni listovi proizvođača "
            f"u dijelu u kojem postoje)."
            f"{f'<br><br>Mjesto predaje: <b>{mjesto_predaje}</b>.' if mjesto_predaje else ''}</div>"
            f"<div class='section-title'>Članak 5. — PRIJENOS VLASNIŠTVA</div>"
            f"<div class='doc-body'>Pravo vlasništva na brodici prelazi s Prodavatelja na Kupca upisom u "
            f"Upisnik brodica pri Lučkoj kapetaniji (Pomorski zakonik). Prodavatelj će istovremeno s potpisom "
            f"ovog Ugovora izdati Kupcu posebnu izjavu (clausula intabulandi) kojom dopušta upis prava vlasništva "
            f"u Upisnik brodica u korist Kupca.</div>"
            f"<div class='section-title'>Članak 6. — TROŠKOVI</div>"
            f"<div class='doc-body'>Troškove ovjere potpisa kod javnog bilježnika, eventualnog poreza na promet "
            f"plovila i upisa promjene vlasništva u Upisnik brodica snosi Kupac, ako se ugovorne strane drugačije "
            f"ne dogovore.</div>"
            f"<div class='section-title'>Članak 7. — ZAVRŠNE ODREDBE</div>"
            f"<div class='doc-body'>Ovaj Ugovor stupa na snagu danom potpisa obiju ugovornih strana. "
            f"Sve sporove iz ovog Ugovora ugovorne strane će rješavati sporazumno, a u protivnom je nadležan "
            f"sud prema mjestu upisa brodice.<br><br>"
            f"Ugovor je sastavljen u 4 (četiri) primjerka, od kojih svaka ugovorna strana zadržava po jedan, "
            f"a 2 (dva) primjerka su namijenjena za potrebe Lučke kapetanije i javnog bilježnika.</div>"
            f"<br><br>"
            f"<table width='100%'><tr>"
            f"<td width='50%' align='center'><b>PRODAVATELJ</b><br>(potpis ovjeren JB)<br><br>______________________</td>"
            f"<td width='50%' align='center'><b>KUPAC</b><br>(potpis ovjeren JB)<br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_tabularnu_brodice(prodavatelj, kupac, podaci):
    """Tabularna izjava (clausula intabulandi) za upis vlasnistva brodice u Upisnik brodica."""
    try:
        datum_ugovora = format_text(podaci.get('datum_ugovora', ''))
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        kapetanija = format_text(podaci.get('lucka_kapetanija', ''))

        identifikacija = _identifikacija_brodice(podaci)

        return (
            f"<div class='header-doc'>TABULARNA IZJAVA<br>"
            f"<span style='font-size: 11pt; font-weight: normal;'>(Clausula Intabulandi za Upisnik brodica)</span></div>"
            f"<div class='party-info'><b>PRODAVATELJ:</b><br>{prodavatelj}</div>"
            f"<div class='party-info'><b>KUPAC:</b><br>{kupac}</div><br>"
            f"<div class='doc-body'>Temeljem Ugovora o kupoprodaji brodice od {datum_ugovora}, "
            f"za brodicu sljedećih identifikacijskih podataka:<br><br>"
            f"{identifikacija}</div>"
            f"<div class='doc-body clausula'>"
            f"Ja, PRODAVATELJ, ovime izričito i bezuvjetno <b>dopuštam</b> Lučkoj kapetaniji "
            f"{f'<b>{kapetanija}</b> ' if kapetanija else ''}da, na temelju ove Tabularne izjave i Ugovora o "
            f"kupoprodaji, izvrši upis prava vlasništva na gore opisanoj brodici "
            f"u <b>cijelosti (1/1 dijela)</b> u korist KUPCA — bez moje daljnje suglasnosti i bez moje prisutnosti."
            f"</div>"
            f"<div class='doc-body'>Izjavljujem da je brodica slobodna od svih tereta, sudskih sporova, ovrha "
            f"i prava trećih osoba, te da nemam nikakvih daljnjih potraživanja prema Kupcu po osnovi ove kupoprodaje.</div>"
            f"<br>"
            f"<div class='justified'>U {u_lokativu(mjesto)}, dana {datum}.</div><br>"
            f"<table width='100%'><tr>"
            f"<td width='40%'></td>"
            f"<td width='60%' align='center'><b>PRODAVATELJ</b><br>(ovjera potpisa kod javnog bilježnika)<br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_punomoc_prodaje_brodice(vlastodavac, punomocnik, podaci):
    """Specijalna punomoc za prodaju brodice (ZOO cl. 308-331 + Pomorski zakonik)."""
    try:
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        min_cijena = podaci.get('minimalna_cijena_eur', 0)
        min_cijena_str = format_eur(min_cijena) if min_cijena else ''
        rok_vazenja = format_text(podaci.get('rok_vazenja', '12 (dvanaest) mjeseci od datuma ovjere'))

        identifikacija = _identifikacija_brodice(podaci)
        cijena_klauzula = (
            f"<li>pregovarati o kupoprodajnoj cijeni, ali ne ispod iznosa od <b>{min_cijena_str}</b>;</li>"
            if min_cijena_str else
            "<li>pregovarati o kupoprodajnoj cijeni i prihvatiti onu koju smatra najpovoljnijom;</li>"
        )

        return (
            f"<div class='header-doc'>SPECIJALNA PUNOMOĆ<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>za prodaju brodice</span></div>"
            f"<div class='justified'>Ja, dolje potpisani/a:</div><br>"
            f"<div class='party-info'><b>VLASTODAVAC (vlasnik brodice):</b><br>{vlastodavac}</div><br>"
            f"<div class='justified'>kao isključivi vlasnik niže opisane brodice, ovime dajem</div><br>"
            f"<div style='text-align: center; font-weight: bold; font-size: 14pt; margin: 20px 0;'>SPECIJALNU PUNOMOĆ</div>"
            f"<div class='party-info'><b>PUNOMOĆNIKU:</b><br>{punomocnik}</div><br>"
            f"<div class='justified'>za prodaju sljedećeg plovila:</div><br>"
            f"<div class='doc-body'>{identifikacija}</div>"
            f"<div class='justified'>Punomoćnik je ovlašten u moje ime i za moj račun:</div>"
            f"<div class='doc-body'><ol>"
            f"<li>oglasiti i ponuditi brodicu na prodaju;</li>"
            f"{cijena_klauzula}"
            f"<li>sklopiti i potpisati Ugovor o kupoprodaji brodice s kupcem po izboru punomoćnika;</li>"
            f"<li>potpisati i ovjeriti Tabularnu izjavu (clausulu intabulandi) za upis vlasništva u Upisnik brodica;</li>"
            f"<li>preuzeti kupoprodajnu cijenu i izdati potvrdu o primitku;</li>"
            f"<li>predati brodicu kupcu u posjed sa svim pripadnostima i ispravama;</li>"
            f"<li>obavljati sve poslove pri Lučkoj kapetaniji potrebne za prijenos vlasništva u Upisnik brodica, "
            f"uključujući podnošenje zahtjeva za brisanje vlasništva vlastodavca i upis novog vlasnika;</li>"
            f"<li>poduzimati sve ostale pravne radnje potrebne za uspješan dovršetak kupoprodaje.</ol></div>"
            f"<div class='justified'>Ova specijalna punomoć vrijedi {rok_vazenja}, ako prije ne bude opozvana "
            f"u pisanom obliku s ovjerenim potpisom.</div><br>"
            f"<div class='justified'>Pravni temelj: članci 308. — 331. Zakona o obveznim odnosima "
            f"i odredbe Pomorskog zakonika o pravnom prometu brodicama.</div><br>"
            f"<div class='justified'>U {u_lokativu(mjesto)}, dana {datum}.</div><br>"
            f"<table width='100%'><tr>"
            f"<td width='40%'></td>"
            f"<td width='60%' align='center'><b>VLASTODAVAC</b><br>(potpis ovjeren kod javnog bilježnika)<br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_zalog_brodice(vjerovnik, zalozni_duznik, podaci):
    """Sporazum o zasnivanju zaloznog prava na brodici (PZ + ZV).
    Sluzi kao osnova za upis u Upisnik brodica."""
    try:
        glavnica = podaci.get('iznos_trazbine_eur', 0)
        glavnica_str = format_eur(glavnica)
        glavnica_slovima = format_eur_s_rijecima(glavnica) if glavnica else ''
        kamata = format_text(podaci.get('kamatna_stopa', 'zakonska zatezna kamata'))
        rok_dospijeca = format_text(podaci.get('rok_dospijeca', ''))
        osnova_trazbine = format_text(podaci.get('osnova_trazbine', ''))
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')

        identifikacija = _identifikacija_brodice(podaci)
        slovima_html = f" (slovima: {glavnica_slovima})" if glavnica_slovima else ""

        return (
            f"<div class='header-doc'>SPORAZUM O ZASNIVANJU ZALOŽNOG PRAVA NA BRODICI</div>"
            f"<div class='justified'>sklopljen u {u_lokativu(mjesto)} dana {datum} između:</div><br>"
            f"<div class='party-info'><b>VJEROVNIK (založni vjerovnik):</b><br>{vjerovnik}</div>"
            f"<div class='party-info'><b>ZALOŽNI DUŽNIK (vlasnik brodice):</b><br>{zalozni_duznik}</div><br>"
            f"<div class='section-title'>Članak 1. — PREDMET ZALOGA</div>"
            f"<div class='doc-body'>Predmet zaloga je brodica u vlasništvu Založnog dužnika, sljedećih identifikacijskih podataka:<br><br>"
            f"{identifikacija}</div>"
            f"<div class='section-title'>Članak 2. — TRAŽBINA KOJA SE OSIGURAVA</div>"
            f"<div class='doc-body'>Založnim pravom osigurava se tražbina Vjerovnika prema Založnom dužniku "
            f"u iznosu od <b>{glavnica_str}</b>{slovima_html}, "
            f"s pripadajućim {kamata}, te eventualnim troškovima naplate.<br><br>"
            f"<b>Osnova tražbine:</b> {osnova_trazbine}<br>"
            f"<b>Rok dospijeća:</b> {rok_dospijeca}</div>"
            f"<div class='section-title'>Članak 3. — UPIS U UPISNIK BRODICA</div>"
            f"<div class='doc-body'>Založni dužnik suglasan je da se na temelju ovog Sporazuma u Upisnik brodica "
            f"pri nadležnoj Lučkoj kapetaniji provede upis založnog prava u korist Vjerovnika, u iznosu i "
            f"pod uvjetima iz članka 2. ovog Sporazuma. Založni dužnik ovime daje izričito dopuštenje za upis "
            f"(intabulacijska klauzula).</div>"
            f"<div class='section-title'>Članak 4. — OVLASTI VJEROVNIKA</div>"
            f"<div class='doc-body'>Ako Založni dužnik ne ispuni osiguranu tražbinu o dospijeću, Vjerovnik je "
            f"ovlašten zahtijevati prodaju brodice radi namirenja iz dobivene cijene, sukladno odredbama Ovršnog "
            f"zakona i Pomorskog zakonika. Brodica se prodaje putem javnog bilježnika ili u sudskom postupku.</div>"
            f"<div class='section-title'>Članak 5. — OBVEZE ZALOŽNOG DUŽNIKA</div>"
            f"<div class='doc-body'>Založni dužnik se obvezuje:<br><br>"
            f"a) brodicu uredno održavati i osigurati od svih uobičajenih rizika u korist Vjerovnika;<br>"
            f"b) brodicu ne otuđiti, ne opteretiti dodatnim založnim pravima niti dati u zakup bez pisane "
            f"suglasnosti Vjerovnika;<br>"
            f"c) Vjerovniku omogućiti pregled brodice na njegov zahtjev.</div>"
            f"<div class='section-title'>Članak 6. — PRESTANAK ZALOGA</div>"
            f"<div class='doc-body'>Založno pravo prestaje ispunjenjem osigurane tražbine u cijelosti. "
            f"Po ispunjenju Vjerovnik se obvezuje izdati pisanu izjavu o prestanku založnog prava (brisovno "
            f"očitovanje) s ovjerenim potpisom, kojom će se izvršiti brisanje upisa u Upisniku brodica.</div>"
            f"<br><br>"
            f"<table width='100%'><tr>"
            f"<td width='50%' align='center'><b>VJEROVNIK</b><br>(potpis ovjeren JB)<br><br>______________________</td>"
            f"<td width='50%' align='center'><b>ZALOŽNI DUŽNIK</b><br>(potpis ovjeren JB)<br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
