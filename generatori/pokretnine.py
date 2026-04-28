# -----------------------------------------------------------------------------
# GENERATORI: Zalog na pokretninama
# Pravni temelj:
#   - Zakon o vlasnistvu i drugim stvarnim pravima (NN 91/96 ...)
#   - Zakon o upisniku sudskih i javnobiljeznickih osiguranja trazbina
#     vjerovnika na pokretnim stvarima i pravima (NN 121/05 i izmjene)
#   - FINA Upisnik zaloznih prava na pokretninama
#   - Za vozila: Zakon o sigurnosti prometa na cestama, MUP evidencija
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, format_eur, format_eur_s_rijecima, u_lokativu


def generiraj_zalog_pokretnine(vjerovnik, zalozni_duznik, podaci):
    """Sporazum o zasnivanju zaloznog prava na pokretnini koja se upisuje
    u FINA Upisnik zaloznih prava (NN 121/05).

    Tipicni predmeti: oprema, strojevi, zalihe, umjetnine, nakit visokoj vrijednosti.
    Forma: javnobiljeznicki akt ili privatna isprava s ovjerenim potpisima.
    Upis: putem javnog biljeznika koji prosljeduje FINA-i."""
    try:
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        opis_predmeta = format_text(podaci.get('opis_predmeta', ''))
        identifikacija = format_text(podaci.get('identifikacija', ''))
        procjena_vrijednosti = podaci.get('procjena_vrijednosti_eur', 0)
        procjena_str = format_eur(procjena_vrijednosti) if procjena_vrijednosti else ''
        glavnica = podaci.get('iznos_trazbine_eur', 0)
        glavnica_str = format_eur(glavnica) if glavnica else ''
        glavnica_slovima = format_eur_s_rijecima(glavnica) if glavnica else ''
        kamata = format_text(podaci.get('kamatna_stopa', 'zakonska zatezna kamata'))
        rok_dospijeca = format_text(podaci.get('rok_dospijeca', ''))
        osnova_trazbine = format_text(podaci.get('osnova_trazbine', ''))
        mjesto_pohrane = format_text(podaci.get('mjesto_pohrane', ''))
        oblik_zaloga = podaci.get('oblik_zaloga', 'bezdrzavinski')  # bezdrzavinski | drzavinski

        slovima_html = f" (slovima: {glavnica_slovima})" if glavnica_slovima else ""

        if oblik_zaloga == 'drzavinski':
            posjed_klauzula = (
                "Ugovorne strane su suglasne da se predmet zaloga predaje u posjed Vjerovnika "
                "(držžavinski zalog — pignus). Vjerovnik je obvezan predmet brižljivo čuvati i ne koristiti ga "
                "bez izričite suglasnosti Založnog dužnika."
            )
        else:
            posjed_klauzula = (
                f"Predmet zaloga ostaje u posjedu Založnog dužnika (bezdržavinski zalog), "
                f"u sljedećem mjestu pohrane: <b>{mjesto_pohrane or 'kako je gore navedeno u Članku 1.'}</b>. "
                f"Založni dužnik je obvezan predmet brižljivo održavati, osigurati od uobičajenih rizika u korist "
                f"Vjerovnika, te omogućiti Vjerovniku pregled na njegov zahtjev."
            )

        return (
            f"<div class='header-doc'>SPORAZUM O ZASNIVANJU ZALOŽNOG PRAVA NA POKRETNINI</div>"
            f"<div class='justified'>sklopljen u {u_lokativu(mjesto)} dana {datum} između:</div><br>"
            f"<div class='party-info'><b>VJEROVNIK (založni vjerovnik):</b><br>{vjerovnik}</div>"
            f"<div class='party-info'><b>ZALOŽNI DUŽNIK (vlasnik pokretnine):</b><br>{zalozni_duznik}</div><br>"
            f"<div class='section-title'>Članak 1. — PREDMET ZALOGA</div>"
            f"<div class='doc-body'>"
            f"<b>Opis predmeta:</b> {opis_predmeta}<br>"
            f"{f'<b>Identifikacija (serijski broj, oznaka, marka):</b> {identifikacija}<br>' if identifikacija else ''}"
            f"{f'<b>Procijenjena tržišna vrijednost:</b> {procjena_str}<br>' if procjena_str else ''}"
            f"</div>"
            f"<div class='section-title'>Članak 2. — TRAŽBINA KOJA SE OSIGURAVA</div>"
            f"<div class='doc-body'>Založnim pravom osigurava se tražbina Vjerovnika prema Založnom dužniku "
            f"u iznosu od <b>{glavnica_str}</b>{slovima_html}, "
            f"s pripadajućim {kamata}, te eventualnim troškovima naplate.<br><br>"
            f"<b>Osnova tražbine:</b> {osnova_trazbine}<br>"
            f"<b>Rok dospijeća:</b> {rok_dospijeca}</div>"
            f"<div class='section-title'>Članak 3. — UPIS U FINA UPISNIK</div>"
            f"<div class='doc-body'>Založni dužnik suglasan je i izričito dopušta da se na temelju ovog Sporazuma "
            f"u <b>Upisnik založnih prava na pokretnim stvarima i pravima</b> (FINA), sukladno Zakonu o "
            f"upisniku sudskih i javnobilježničkih osiguranja tražbina vjerovnika na pokretnim stvarima i "
            f"pravima (NN 121/05 i izmjene), provede upis založnog prava u korist Vjerovnika.<br><br>"
            f"Upis se provodi putem javnog bilježnika. Trošak upisa snosi Založni dužnik.</div>"
            f"<div class='section-title'>Članak 4. — POSJED I OBLIK ZALOGA</div>"
            f"<div class='doc-body'>{posjed_klauzula}</div>"
            f"<div class='section-title'>Članak 5. — OVLASTI VJEROVNIKA U SLUČAJU NEISPUNJENJA</div>"
            f"<div class='doc-body'>Ako Založni dužnik ne ispuni osiguranu tražbinu o dospijeću, Vjerovnik je "
            f"ovlašten zahtijevati prodaju predmeta zaloga radi namirenja, sukladno Ovršnom zakonu. "
            f"Prodaja se vrši putem javnog bilježnika ili u sudskom postupku.</div>"
            f"<div class='section-title'>Članak 6. — OBVEZE ZALOŽNOG DUŽNIKA</div>"
            f"<div class='doc-body'>Založni dužnik se obvezuje:<br><br>"
            f"a) bez pisane suglasnosti Vjerovnika ne otuđivati predmet zaloga niti ga dodatno opterećivati;<br>"
            f"b) predmet zaloga osigurati od uobičajenih rizika u korist Vjerovnika;<br>"
            f"c) Vjerovniku omogućiti pregled predmeta zaloga na njegov zahtjev.</div>"
            f"<div class='section-title'>Članak 7. — PRESTANAK ZALOGA</div>"
            f"<div class='doc-body'>Založno pravo prestaje ispunjenjem osigurane tražbine u cijelosti. "
            f"Po ispunjenju, Vjerovnik se obvezuje izdati pisanu izjavu o prestanku založnog prava s ovjerenim "
            f"potpisom, kojom se izvršava brisanje upisa u FINA Upisniku.</div>"
            f"<br><br>"
            f"<table width='100%'><tr>"
            f"<td width='50%' align='center'><b>VJEROVNIK</b><br>(potpis ovjeren JB)<br><br>______________________</td>"
            f"<td width='50%' align='center'><b>ZALOŽNI DUŽNIK</b><br>(potpis ovjeren JB)<br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_zalog_vozila(vjerovnik, zalozni_duznik, podaci):
    """Sporazum o zasnivanju zaloznog prava na motornom vozilu.
    Pravni temelj: ZV cl. 297, FINA Upisnik (NN 121/05).
    Specificnost: registracijska oznaka + sasija + motor identifikacija;
    Vjerovnik se upisuje u prometnu dozvolu (rubrika 'Tereti')."""
    try:
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')
        marka = format_text(podaci.get('marka', ''))
        model = format_text(podaci.get('model', ''))
        god_proizvodnje = format_text(podaci.get('godina_proizvodnje', ''))
        registracija = format_text(podaci.get('registracijska_oznaka', ''))
        broj_sasije = format_text(podaci.get('broj_sasije_vin', ''))
        broj_motora = format_text(podaci.get('broj_motora', ''))
        boja = format_text(podaci.get('boja', ''))
        prijedeni_km = format_text(podaci.get('prijedeni_km', ''))
        procjena = podaci.get('procjena_vrijednosti_eur', 0)
        procjena_str = format_eur(procjena) if procjena else ''
        glavnica = podaci.get('iznos_trazbine_eur', 0)
        glavnica_str = format_eur(glavnica) if glavnica else ''
        glavnica_slovima = format_eur_s_rijecima(glavnica) if glavnica else ''
        kamata = format_text(podaci.get('kamatna_stopa', 'zakonska zatezna kamata'))
        rok_dospijeca = format_text(podaci.get('rok_dospijeca', ''))
        osnova_trazbine = format_text(podaci.get('osnova_trazbine', ''))

        slovima_html = f" (slovima: {glavnica_slovima})" if glavnica_slovima else ""

        identifikacija_html = []
        if marka or model:
            identifikacija_html.append(f"<b>Marka i model:</b> {marka} {model}".strip())
        if god_proizvodnje:
            identifikacija_html.append(f"<b>Godina proizvodnje:</b> {god_proizvodnje}")
        if registracija:
            identifikacija_html.append(f"<b>Registracijska oznaka:</b> {registracija}")
        if broj_sasije:
            identifikacija_html.append(f"<b>Broj šasije (VIN):</b> {broj_sasije}")
        if broj_motora:
            identifikacija_html.append(f"<b>Broj motora:</b> {broj_motora}")
        if boja:
            identifikacija_html.append(f"<b>Boja:</b> {boja}")
        if prijedeni_km:
            identifikacija_html.append(f"<b>Prijeđeni kilometri:</b> {prijedeni_km}")
        if procjena_str:
            identifikacija_html.append(f"<b>Procijenjena tržišna vrijednost:</b> {procjena_str}")
        identifikacija_full = "<br>".join(identifikacija_html)

        return (
            f"<div class='header-doc'>SPORAZUM O ZASNIVANJU ZALOŽNOG PRAVA NA MOTORNOM VOZILU</div>"
            f"<div class='justified'>sklopljen u {u_lokativu(mjesto)} dana {datum} između:</div><br>"
            f"<div class='party-info'><b>VJEROVNIK:</b><br>{vjerovnik}</div>"
            f"<div class='party-info'><b>ZALOŽNI DUŽNIK (vlasnik vozila):</b><br>{zalozni_duznik}</div><br>"
            f"<div class='section-title'>Članak 1. — PREDMET ZALOGA (motorno vozilo)</div>"
            f"<div class='doc-body'>{identifikacija_full}</div>"
            f"<div class='section-title'>Članak 2. — TRAŽBINA KOJA SE OSIGURAVA</div>"
            f"<div class='doc-body'>Založnim pravom osigurava se tražbina Vjerovnika u iznosu od "
            f"<b>{glavnica_str}</b>{slovima_html}, s pripadajućim {kamata}, te eventualnim troškovima naplate.<br><br>"
            f"<b>Osnova tražbine:</b> {osnova_trazbine}<br>"
            f"<b>Rok dospijeća:</b> {rok_dospijeca}</div>"
            f"<div class='section-title'>Članak 3. — UPIS U FINA UPISNIK I PROMETNU DOZVOLU</div>"
            f"<div class='doc-body'>Založni dužnik suglasan je i izričito dopušta da se na temelju ovog Sporazuma:<br>"
            f"a) provede upis založnog prava u <b>FINA Upisnik založnih prava na pokretnim stvarima i pravima</b> "
            f"(NN 121/05) putem javnog bilježnika;<br>"
            f"b) zabilježi teret u <b>prometnoj dozvoli</b> vozila pri nadležnoj policijskoj upravi (MUP), "
            f"u rubrici predviđenoj za terete.<br><br>"
            f"Trošak upisa snosi Založni dužnik.</div>"
            f"<div class='section-title'>Članak 4. — POSJED I KORIŠTENJE</div>"
            f"<div class='doc-body'>Vozilo ostaje u posjedu i uobičajenom korištenju Založnog dužnika. "
            f"Založni dužnik je obvezan:<br><br>"
            f"a) održavati vozilo u ispravnom stanju (redoviti tehnički pregledi, servisi);<br>"
            f"b) osigurati vozilo od uobičajenih rizika (auto kasko, autoodgovornost) — Vjerovnik se može "
            f"navesti kao korisnik osiguranja;<br>"
            f"c) bez pisane suglasnosti Vjerovnika ne prodavati, darovati niti dodatno opterećivati vozilo;<br>"
            f"d) ne prijavljivati vozilo izvan Republike Hrvatske bez pisane suglasnosti Vjerovnika.</div>"
            f"<div class='section-title'>Članak 5. — OVLASTI VJEROVNIKA U SLUČAJU NEISPUNJENJA</div>"
            f"<div class='doc-body'>Ako Založni dužnik ne ispuni osiguranu tražbinu o dospijeću, Vjerovnik je "
            f"ovlašten zahtijevati prodaju vozila radi namirenja sukladno Ovršnom zakonu. "
            f"Prodaja se vrši putem javnog bilježnika ili u sudskom postupku, a Založni dužnik je obvezan "
            f"predati Vjerovniku vozilo, prometnu dozvolu i ključeve u roku od 8 dana od pisanog poziva.</div>"
            f"<div class='section-title'>Članak 6. — PRESTANAK ZALOGA</div>"
            f"<div class='doc-body'>Založno pravo prestaje ispunjenjem osigurane tražbine u cijelosti. "
            f"Po ispunjenju, Vjerovnik se obvezuje izdati pisanu izjavu o prestanku založnog prava s ovjerenim "
            f"potpisom, kojom se izvršava brisanje upisa u FINA Upisniku i u prometnoj dozvoli vozila.</div>"
            f"<br><br>"
            f"<table width='100%'><tr>"
            f"<td width='50%' align='center'><b>VJEROVNIK</b><br>(potpis ovjeren JB)<br><br>______________________</td>"
            f"<td width='50%' align='center'><b>ZALOŽNI DUŽNIK</b><br>(potpis ovjeren JB)<br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
