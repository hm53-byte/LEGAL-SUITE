# -----------------------------------------------------------------------------
# GENERATORI: Zemljisne knjige (tabularna, ZK prijedlog)
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import formatiraj_troskovnik, format_text, format_eur, format_eur_s_rijecima, u_lokativu


def generiraj_tabularnu_doc(prod, kup, ko, cest, ul, opis, dat):
    try:
        return (
            f"<div class='header-doc'>TABULARNA IZJAVA<br>"
            f"<span style='font-size: 11pt; font-weight: normal;'>(Clausula Intabulandi)</span></div>"
            f"<div class='party-info'><b>PRODAVATELJ:</b><br>{prod}</div>"
            f"<div class='party-info'><b>KUPAC:</b><br>{kup}</div>"
            f"<div class='doc-body'>Temeljem Ugovora od {dat} za nekretninu u K.O. {ko}, k.č.br {cest}."
            f"{'<br>Opis u naravi: ' + opis if opis else ''}</div>"
            f"<div class='doc-body clausula'>Ja, PRODAVATELJ, ovime izričito ovlašćujem KUPCA da zatraži uknjižbu prava vlasništva.</div>"
            f'<br><br><table width="100%"><tr><td width="40%"></td>'
            f'<td width="60%" align="center"><b>PRODAVATELJ</b><br>(Ovjera JB)<br><br>_________________</td></tr></table>'
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_zk_prijedlog(sud, predlagatelj, protustranka, nekretnina, dokumenti, troskovi_dict):
    try:
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        return (
            f'<div style="font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f'<div style="font-size: 12px;">Zemljišnoknjižni odjel</div><br><br>'
            f"<div class='party-info'><b>PREDLAGATELJ:</b><br>{predlagatelj}</div>"
            f"<div class='party-info'><b>PROTUSTRANKA:</b><br>{protustranka}</div><br>"
            f"<div class='header-doc'>ZEMLJIŠNOKNJIŽNI PRIJEDLOG<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>za uknjižbu prava vlasništva</span></div>"
            f"<div class='doc-body'>Predlagatelj predlaže da naslovni sud, na temelju priloženih isprava, "
            f"u zemljišnim knjigama za nekretninu upisanu kao:<br><br>"
            f"<b>Katastarska općina (k.o.):</b> {nekretnina['ko']}<br>"
            f"<b>Broj zk. uloška:</b> {nekretnina['ulozak']}<br>"
            f"<b>Broj čestice (k.č.br.):</b> {nekretnina['cestica']}"
            f"{', u naravi ' + nekretnina['opis'] if nekretnina['opis'] else ''}<br><br>"
            f"provede upis, odnosno dozvoli:</div>"
            f"<div class='section-title' style='text-align: center; border: 1px solid black; padding: 10px; margin: 20px 0;'>"
            f"UKNJIŽBU PRAVA VLASNIŠTVA<br>u korist Predlagatelja (u cijelosti / 1/1 dijela).</div>"
            f"<div class='doc-body'>Predlagatelj prilaže izvornike/ovjerene preslike isprava koje su temelj za upis.</div>"
            f"<div class='section-title'>POPIS PRILOGA:</div>"
            f"<div class='doc-body'><ol>"
            f"<li>{dokumenti['ugovor']}</li>"
            f"<li>{dokumenti['tabularna']}</li>"
            f"<li>Dokaz o uplati sudske pristojbe</li>"
            f"<li>Dokaz o državljanstvu / OIB (preslika osobne iskaznice)</li>"
            f"</ol></div>"
            f"{troskovnik_html}<br><br>"
            f'<table width="100%" border="0"><tr><td width="50%"></td>'
            f'<td width="50%" align="center"><b>PREDLAGATELJ</b><br>(potpis nije nužno ovjeravati)<br><br>______________________</td></tr></table>'
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_zabilježbu(sud, predlagatelj, podaci):
    try:
        ko = podaci.get('ko', '')
        ulozak = podaci.get('ulozak', '')
        cestica = podaci.get('cestica', '')
        vrsta_zabilježbe = podaci.get('vrsta_zabilježbe', 'spora')
        opis_cinjenice = podaci.get('opis_cinjenice', '')
        pravni_temelj = podaci.get('pravni_temelj', '')
        mjesto = podaci.get('mjesto', '')
        datum = date.today().strftime('%d.%m.%Y.')

        vrsta_map = {
            'spora': 'spora',
            'ovrhe': 'ovrhe',
            'stečaja': 'stečaja',
            'maloljetnosti': 'maloljetnosti',
            'oduzimanje_pos_sposobnosti': 'oduzimanja poslovne sposobnosti',
        }
        vrsta_tekst = vrsta_map.get(vrsta_zabilježbe, vrsta_zabilježbe)

        return (
            f'<div style="font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f'<div style="font-size: 12px;">Zemljišnoknjižni odjel</div><br><br>'
            f"<div class='party-info'><b>PREDLAGATELJ:</b><br>{predlagatelj}</div><br>"
            f"<div class='header-doc'>PRIJEDLOG ZA ZABILJEŽBU<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>zabilježba {vrsta_tekst}</span></div>"
            f"<div class='doc-body'><b>I. PREDLAGATELJ</b><br><br>"
            f"{predlagatelj}</div>"
            f"<div class='doc-body'><b>II. NEKRETNINA</b><br><br>"
            f"<b>Katastarska općina (k.o.):</b> {format_text(ko)}<br>"
            f"<b>Broj zk. uloška:</b> {format_text(ulozak)}<br>"
            f"<b>Broj čestice (k.č.br.):</b> {format_text(cestica)}</div>"
            f"<div class='doc-body'><b>III. SADRŽAJ ZABILJEŽBE</b><br><br>"
            f"Predlagatelj predlaže da se u zemljišnoj knjizi, za nekretninu označenu kao k.č.br. {format_text(cestica)}, "
            f"upisanu u zk.ul. {format_text(ulozak)}, K.O. {format_text(ko)}, provede zabilježba {vrsta_tekst}.<br><br>"
            f"<b>Činjenica koja se zabilježava:</b><br>"
            f"{format_text(opis_cinjenice)}<br><br>"
            f"<b>Pravni temelj:</b><br>"
            f"{format_text(pravni_temelj)}<br><br>"
            f"<i>Napomena: Zabilježba ne prenosi pravo vlasništva niti ga mijenja, već osigurava publicitet "
            f"određene pravno relevantne činjenice u zemljišnoj knjizi.</i></div>"
            f"<div class='doc-body'><b>IV. PETITUM</b><br><br>"
            f"Predlaže se da naslovni sud u zemljišnoj knjizi za nekretninu upisanu u zk.ul. {format_text(ulozak)}, "
            f"K.O. {format_text(ko)}, k.č.br. {format_text(cestica)}, dozvoli i provede:<br><br>"
            f"<div style='text-align: center; border: 1px solid black; padding: 10px; margin: 20px 0;'>"
            f"ZABILJEŽBU {vrsta_tekst.upper()}</div></div>"
            f"<div class='section-title'>POPIS PRILOGA:</div>"
            f"<div class='doc-body'><ol>"
            f"<li>Isprava koja je temelj za zabilježbu (presuda / rješenje / ugovor)</li>"
            f"<li>Izvadak iz zemljišne knjige</li>"
            f"<li>Dokaz o uplati sudske pristojbe</li>"
            f"</ol></div>"
            f"<div class='doc-body justified'>"
            f"U {format_text(u_lokativu(mjesto))}, {datum}</div><br><br>"
            f'<table width="100%" border="0"><tr><td width="50%"></td>'
            f'<td width="50%" align="center"><b>PREDLAGATELJ</b><br><br>______________________</td></tr></table>'
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_predbiježbu(sud, predlagatelj, protustranka, podaci):
    try:
        ko = podaci.get('ko', '')
        ulozak = podaci.get('ulozak', '')
        cestica = podaci.get('cestica', '')
        vrsta_prava = podaci.get('vrsta_prava', 'vlasništvo')
        nedostatak_isprave = podaci.get('nedostatak_isprave', '')
        pravni_temelj = podaci.get('pravni_temelj', '')
        mjesto = podaci.get('mjesto', '')
        datum = date.today().strftime('%d.%m.%Y.')

        vrsta_tekst = 'prava vlasništva' if vrsta_prava == 'vlasništvo' else 'založnog prava'

        return (
            f'<div style="font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f'<div style="font-size: 12px;">Zemljišnoknjižni odjel</div><br><br>'
            f"<div class='party-info'><b>PREDLAGATELJ:</b><br>{predlagatelj}</div>"
            f"<div class='party-info'><b>PROTUSTRANKA:</b><br>{protustranka}</div><br>"
            f"<div class='header-doc'>PRIJEDLOG ZA PREDBILJEŽBU<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>{vrsta_tekst}</span></div>"
            f"<div class='doc-body'><b>I. STRANKE</b><br><br>"
            f"<b>Predlagatelj:</b> {predlagatelj}<br>"
            f"<b>Protustranka:</b> {protustranka}</div>"
            f"<div class='doc-body'><b>II. NEKRETNINA</b><br><br>"
            f"<b>Katastarska općina (k.o.):</b> {format_text(ko)}<br>"
            f"<b>Broj zk. uloška:</b> {format_text(ulozak)}<br>"
            f"<b>Broj čestice (k.č.br.):</b> {format_text(cestica)}</div>"
            f"<div class='doc-body'><b>III. NEDOSTATAK U ISPRAVI</b><br><br>"
            f"Predlagatelj raspolaže ispravom koja bi bila temelj za uknjižbu {vrsta_tekst}, "
            f"no isprava sadrži sljedeći nedostatak:<br><br>"
            f"{format_text(nedostatak_isprave)}<br><br>"
            f"<b>Pravni temelj:</b><br>"
            f"{format_text(pravni_temelj)}</div>"
            f"<div class='doc-body'><b>IV. PETITUM</b><br><br>"
            f"Predlaže se da naslovni sud u zemljišnoj knjizi za nekretninu upisanu u zk.ul. {format_text(ulozak)}, "
            f"K.O. {format_text(ko)}, k.č.br. {format_text(cestica)}, dozvoli i provede:<br><br>"
            f"<div style='text-align: center; border: 1px solid black; padding: 10px; margin: 20px 0;'>"
            f"PREDBILJEŽBU {vrsta_tekst.upper()}<br>"
            f"u korist Predlagatelja (uvjetni upis)</div><br>"
            f"<i>Napomena: Predbilježba se opravdava dostavom valjane izjave (clausula intabulandi) "
            f"ili presude u zakonskom roku. Ukoliko se predbilježba ne opravda, brisat će se na prijedlog protustranke.</i></div>"
            f"<div class='section-title'>POPIS PRILOGA:</div>"
            f"<div class='doc-body'><ol>"
            f"<li>Isprava koja je temelj za predbilježbu (ugovor / presuda)</li>"
            f"<li>Izvadak iz zemljišne knjige</li>"
            f"<li>Dokaz o uplati sudske pristojbe</li>"
            f"<li>Dokaz o državljanstvu / OIB (preslika osobne iskaznice)</li>"
            f"</ol></div>"
            f"<div class='doc-body justified'>"
            f"U {format_text(u_lokativu(mjesto))}, {datum}</div><br><br>"
            f'<table width="100%" border="0"><tr><td width="50%"></td>'
            f'<td width="50%" align="center"><b>PREDLAGATELJ</b><br><br>______________________</td></tr></table>'
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_upis_hipoteke(sud, vjerovnik, zalozni_duznik, podaci, troskovi_dict):
    try:
        ko = podaci.get('ko', '')
        ulozak = podaci.get('ulozak', '')
        cestica = podaci.get('cestica', '')
        opis_nekretnine = podaci.get('opis_nekretnine', '')
        iznos_trazbine = podaci.get('iznos_trazbine', 0)
        kamatna_stopa = podaci.get('kamatna_stopa', '')
        broj_ugovora_kredita = podaci.get('broj_ugovora_kredita', '')
        mjesto = podaci.get('mjesto', '')
        datum = date.today().strftime('%d.%m.%Y.')

        troskovnik_html = formatiraj_troskovnik(troskovi_dict)

        return (
            f'<div style="font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f'<div style="font-size: 12px;">Zemljišnoknjižni odjel</div><br><br>'
            f"<div class='party-info'><b>VJEROVNIK (PREDLAGATELJ):</b><br>{vjerovnik}</div>"
            f"<div class='party-info'><b>ZALOŽNI DUŽNIK:</b><br>{zalozni_duznik}</div><br>"
            f"<div class='header-doc'>PRIJEDLOG ZA UKNJIŽBU ZALOŽNOG PRAVA (HIPOTEKE)</div>"
            f"<div class='doc-body'><b>I. STRANKE</b><br><br>"
            f"<b>Vjerovnik (predlagatelj):</b> {vjerovnik}<br>"
            f"<b>Založni dužnik (vlasnik nekretnine):</b> {zalozni_duznik}</div>"
            f"<div class='doc-body'><b>II. NEKRETNINA</b><br><br>"
            f"<b>Katastarska općina (k.o.):</b> {format_text(ko)}<br>"
            f"<b>Broj zk. uloška:</b> {format_text(ulozak)}<br>"
            f"<b>Broj čestice (k.č.br.):</b> {format_text(cestica)}"
            f"{'<br><b>Opis u naravi:</b> ' + format_text(opis_nekretnine) if opis_nekretnine else ''}</div>"
            f"<div class='doc-body'><b>III. TRAŽBINA</b><br><br>"
            f"<b>Iznos tražbine:</b> {format_eur(iznos_trazbine)}<br>"
            f"<b>Kamatna stopa:</b> {format_text(kamatna_stopa)}<br>"
            f"<b>Broj ugovora o kreditu:</b> {format_text(broj_ugovora_kredita)}</div>"
            f"<div class='doc-body'><b>IV. PETITUM</b><br><br>"
            f"Predlaže se da naslovni sud u zemljišnoj knjizi za nekretninu upisanu u zk.ul. {format_text(ulozak)}, "
            f"K.O. {format_text(ko)}, k.č.br. {format_text(cestica)}, dozvoli i provede:<br><br>"
            f"<div style='text-align: center; border: 1px solid black; padding: 10px; margin: 20px 0;'>"
            f"UKNJIŽBU ZALOŽNOG PRAVA (HIPOTEKE)<br>"
            f"u C list (Teretovnicu)<br>"
            f"u korist Vjerovnika, radi osiguranja tražbine u iznosu od {format_eur_s_rijecima(iznos_trazbine)}<br>"
            f"s pripadajućim kamatama i troškovima</div><br>"
            f"<i>Napomena: Upis založnog prava je konstitutivan – hipoteka nastaje tek upisom u zemljišnu knjigu. "
            f"Založno pravo djeluje erga omnes (pravo slijeđenja) te se može ostvariti prema svakom kasnijem vlasniku nekretnine.</i></div>"
            f"<div class='section-title'>POPIS PRILOGA:</div>"
            f"<div class='doc-body'><ol>"
            f"<li>Solemnizirani ugovor o kreditu br. {format_text(broj_ugovora_kredita)}</li>"
            f"<li>Založna izjava s clausulom intabulandi</li>"
            f"<li>Izvadak iz zemljišne knjige</li>"
            f"<li>Dokaz o uplati sudske pristojbe</li>"
            f"</ol></div>"
            f"{troskovnik_html}<br>"
            f"<div class='doc-body justified'>"
            f"U {format_text(u_lokativu(mjesto))}, {datum}</div><br><br>"
            f'<table width="100%" border="0"><tr><td width="50%"></td>'
            f'<td width="50%" align="center"><b>VJEROVNIK (PREDLAGATELJ)</b><br><br>______________________</td></tr></table>'
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_brisanje_hipoteke(sud, vlasnik, podaci):
    try:
        ko = podaci.get('ko', '')
        ulozak = podaci.get('ulozak', '')
        cestica = podaci.get('cestica', '')
        z_broj = podaci.get('z_broj', '')
        vjerovnik_naziv = podaci.get('vjerovnik_naziv', '')
        mjesto = podaci.get('mjesto', '')
        razlog_brisanja = podaci.get('razlog_brisanja', 'otplata_kredita')
        dodatni_razlozi = podaci.get('dodatni_razlozi', [])
        datum = date.today().strftime('%d.%m.%Y.')

        # Temelj brisanja ovisno o razlogu
        razlog_map = {
            'otplata_kredita': (
                f"Predlagatelj, kao vlasnik nekretnine, predlaže brisanje založnog prava (hipoteke) "
                f"upisanog u korist vjerovnika <b>{format_text(vjerovnik_naziv)}</b>, "
                f"temeljem brisovnog očitovanja izdanog od strane vjerovnika nakon otplate kredita u cijelosti."
            ),
            'sudska_odluka': (
                f"Predlagatelj predlaže brisanje založnog prava (hipoteke) upisanog u korist "
                f"<b>{format_text(vjerovnik_naziv)}</b>, temeljem pravomoćne sudske odluke "
                f"kojom je utvrđeno da založno pravo ne postoji, odnosno da je prestalo."
            ),
            'zastara': (
                f"Predlagatelj predlaže brisanje založnog prava (hipoteke) upisanog u korist "
                f"<b>{format_text(vjerovnik_naziv)}</b>, jer je tražbina osigurana hipotekom "
                f"zastarjela sukladno odredbama Zakona o obveznim odnosima, a time je prestalo i "
                f"založno pravo kao akcesorni pravni odnos (čl. 336. ZV)."
            ),
            'nagodba': (
                f"Predlagatelj predlaže brisanje založnog prava (hipoteke) upisanog u korist "
                f"<b>{format_text(vjerovnik_naziv)}</b>, temeljem nagodbe sklopljene između "
                f"predlagatelja i vjerovnika, kojom je uređen prestanak založnog prava."
            ),
            'kompenzacija': (
                f"Predlagatelj predlaže brisanje založnog prava (hipoteke) upisanog u korist "
                f"<b>{format_text(vjerovnik_naziv)}</b>, jer je tražbina osigurana hipotekom "
                f"prestala kompenzacijom (prijebojem) s protutražbinom predlagatelja."
            ),
            'zakonska_hipoteka_prestanak': (
                f"Predlagatelj predlaže brisanje zakonske hipoteke upisane u korist "
                f"<b>{format_text(vjerovnik_naziv)}</b>, jer su prestali uvjeti koji su bili "
                f"temelj za nastanak zakonskog založnog prava."
            ),
        }
        temelj_tekst = razlog_map.get(razlog_brisanja, razlog_map['otplata_kredita'])

        # Dodatni razlozi/obrazloženje
        dodatni_html = ""
        if dodatni_razlozi:
            dodatni_items = "".join(f"<li>{format_text(r)}</li>" for r in dodatni_razlozi)
            dodatni_html = (
                f"<br><b>Dodatno obrazloženje:</b><ol>{dodatni_items}</ol>"
            )

        # Prilagodeni prilozi ovisno o razlogu
        prilog_map = {
            'otplata_kredita': f"<li>Brisovno očitovanje s ovjerenim potpisom {format_text(vjerovnik_naziv)} i clausulom intabulandi za brisanje</li>",
            'sudska_odluka': "<li>Pravomoćna sudska presuda/rješenje s potvrdom pravomoćnosti</li>",
            'zastara': "<li>Dokaz o zastari tražbine (presuda, izjava, ostalo)</li><li>Brisovno očitovanje (ako postoji)</li>",
            'nagodba': "<li>Nagodba (sudska ili izvansudska) s ovjerenim potpisima</li>",
            'kompenzacija': "<li>Izjava o kompenzaciji s dokazom uručenja vjerovniku</li><li>Brisovno očitovanje (ako postoji)</li>",
            'zakonska_hipoteka_prestanak': "<li>Dokaz o prestanku uvjeta za zakonsku hipoteku</li><li>Brisovno očitovanje ili sudska odluka</li>",
        }
        prilog_specifican = prilog_map.get(razlog_brisanja, prilog_map['otplata_kredita'])

        # Napomena ovisno o razlogu
        napomena_map = {
            'otplata_kredita': (
                "Otplata kredita ne dovodi do automatskog brisanja hipoteke iz zemljišne knjige. "
                "Vlasnik nekretnine mora proaktivno zatražiti brisanje podnošenjem prijedloga uz brisovno očitovanje."
            ),
            'sudska_odluka': (
                "Brisanje temeljem sudske odluke provodi se po službenoj dužnosti ili na prijedlog stranke "
                "uz dostavu pravomoćne presude s potvrdom pravomoćnosti."
            ),
            'zastara': (
                "Založno pravo je akcesorno pravo - prestaje prestankom tražbine koju osigurava. "
                "Zastara tražbine dovodi do prestanka hipoteke (čl. 336. ZV). Ukoliko vjerovnik "
                "ne izda brisovno očitovanje, vlasnik može pokrenuti postupak za brisanje."
            ),
            'zakonska_hipoteka_prestanak': (
                "Zakonska hipoteka nastaje ex lege (po samom zakonu) bez upisa u zemljišnu knjigu, "
                "ali za brisanje iz zemljišne knjige potreban je formalni prijedlog s dokazom prestanka uvjeta."
            ),
        }
        napomena = napomena_map.get(razlog_brisanja,
            "Brisanje založnog prava provodi se na prijedlog vlasnika nekretnine uz odgovarajuću dokumentaciju.")

        return (
            f'<div style="font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f'<div style="font-size: 12px;">Zemljišnoknjižni odjel</div><br><br>'
            f"<div class='party-info'><b>VLASNIK (PREDLAGATELJ):</b><br>{vlasnik}</div><br>"
            f"<div class='header-doc'>PRIJEDLOG ZA BRISANJE ZALOŽNOG PRAVA</div>"
            f"<div class='doc-body'><b>I. TEMELJ BRISANJA</b><br><br>"
            f"{temelj_tekst}{dodatni_html}</div>"
            f"<div class='doc-body'><b>II. NEKRETNINA I UPIS</b><br><br>"
            f"<b>Katastarska općina (k.o.):</b> {format_text(ko)}<br>"
            f"<b>Broj zk. uloška:</b> {format_text(ulozak)}<br>"
            f"<b>Broj čestice (k.č.br.):</b> {format_text(cestica)}<br>"
            f"<b>Z-broj upisa založnog prava:</b> {format_text(z_broj)}</div>"
            f"<div class='doc-body'><b>III. PETITUM</b><br><br>"
            f"Predlaže se da naslovni sud u zemljišnoj knjizi za nekretninu upisanu u zk.ul. {format_text(ulozak)}, "
            f"K.O. {format_text(ko)}, k.č.br. {format_text(cestica)}, dozvoli i provede:<br><br>"
            f"<div style='text-align: center; border: 1px solid black; padding: 10px; margin: 20px 0;'>"
            f"BRISANJE ZALOŽNOG PRAVA<br>"
            f"upisanog pod Z-{format_text(z_broj)} u C listu (Teretovnici)<br>"
            f"u korist {format_text(vjerovnik_naziv)}</div><br>"
            f"<i>Napomena: {napomena}</i></div>"
            f"<div class='section-title'>POPIS PRILOGA:</div>"
            f"<div class='doc-body'><ol>"
            f"{prilog_specifican}"
            f"<li>Izvadak iz zemljišne knjige</li>"
            f"<li>Dokaz o uplati sudske pristojbe</li>"
            f"</ol></div>"
            f"<div class='doc-body justified'>"
            f"U {format_text(u_lokativu(mjesto))}, {datum}</div><br><br>"
            f'<table width="100%" border="0"><tr><td width="50%"></td>'
            f'<td width="50%" align="center"><b>VLASNIK (PREDLAGATELJ)</b><br><br>______________________</td></tr></table>'
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_upis_sluznosti(sud, predlagatelj, podaci, troskovi_dict):
    try:
        ko_posluzno = podaci.get('ko_posluzno', '')
        ulozak_posluzno = podaci.get('ulozak_posluzno', '')
        cestica_posluzno = podaci.get('cestica_posluzno', '')
        ko_povlasno = podaci.get('ko_povlasno', '')
        ulozak_povlasno = podaci.get('ulozak_povlasno', '')
        cestica_povlasno = podaci.get('cestica_povlasno', '')
        vrsta_sluznosti = podaci.get('vrsta_sluznosti', 'stvarna')
        sadrzaj_sluznosti = podaci.get('sadrzaj_sluznosti', '')
        pravni_temelj = podaci.get('pravni_temelj', '')
        mjesto = podaci.get('mjesto', '')
        datum = date.today().strftime('%d.%m.%Y.')

        troskovnik_html = formatiraj_troskovnik(troskovi_dict)

        je_stvarna = vrsta_sluznosti == 'stvarna'
        vrsta_tekst = 'stvarne služnosti' if je_stvarna else 'osobne služnosti'

        povlasno_html = ''
        if je_stvarna and ko_povlasno:
            povlasno_html = (
                f"<div class='doc-body'><b>III. POVLASNO DOBRO</b><br><br>"
                f"<b>Katastarska općina (k.o.):</b> {format_text(ko_povlasno)}<br>"
                f"<b>Broj zk. uloška:</b> {format_text(ulozak_povlasno)}<br>"
                f"<b>Broj čestice (k.č.br.):</b> {format_text(cestica_povlasno)}</div>"
            )
        elif not je_stvarna:
            povlasno_html = (
                f"<div class='doc-body'><b>III. OVLAŠTENIK OSOBNE SLUŽNOSTI</b><br><br>"
                f"{predlagatelj}</div>"
            )

        petitum_upis = (
            f"u C list (Teretovnicu) poslužnog dobra"
        )
        if je_stvarna and ko_povlasno:
            petitum_upis += f"<br>te u A list povlasnog dobra (zk.ul. {format_text(ulozak_povlasno)}, K.O. {format_text(ko_povlasno)})"

        napomena = (
            "Stvarna služnost veže se uz nekretninu i prenosi se zajedno s vlasništvom povlasnog dobra."
            if je_stvarna else
            "Osobna služnost prestaje smrću ovlaštenika i ne može se prenositi na druge osobe."
        )

        geodetski_prilog = ''
        if sadrzaj_sluznosti and any(w in sadrzaj_sluznosti.lower() for w in ['vod', 'infrastruktur', 'komunal', 'cijev', 'kabel']):
            geodetski_prilog = f"<li>Geodetski elaborat (infrastrukturni objekt)</li>"

        return (
            f'<div style="font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f'<div style="font-size: 12px;">Zemljišnoknjižni odjel</div><br><br>'
            f"<div class='party-info'><b>PREDLAGATELJ:</b><br>{predlagatelj}</div><br>"
            f"<div class='header-doc'>PRIJEDLOG ZA UKNJIŽBU PRAVA SLUŽNOSTI<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>({vrsta_tekst})</span></div>"
            f"<div class='doc-body'><b>I. SUBJEKTI I OBJEKTI</b><br><br>"
            f"<b>Predlagatelj:</b> {predlagatelj}<br>"
            f"<b>Vrsta služnosti:</b> {vrsta_tekst}<br>"
            f"<b>Sadržaj služnosti:</b> {format_text(sadrzaj_sluznosti)}<br>"
            f"<b>Pravni temelj:</b> {format_text(pravni_temelj)}</div>"
            f"<div class='doc-body'><b>II. POSLUŽNO DOBRO</b><br><br>"
            f"<b>Katastarska općina (k.o.):</b> {format_text(ko_posluzno)}<br>"
            f"<b>Broj zk. uloška:</b> {format_text(ulozak_posluzno)}<br>"
            f"<b>Broj čestice (k.č.br.):</b> {format_text(cestica_posluzno)}</div>"
            f"{povlasno_html}"
            f"<div class='doc-body'><b>IV. SADRŽAJ SLUŽNOSTI</b><br><br>"
            f"{format_text(sadrzaj_sluznosti)}</div>"
            f"<div class='doc-body'><b>V. PETITUM</b><br><br>"
            f"Predlaže se da naslovni sud u zemljišnoj knjizi dozvoli i provede:<br><br>"
            f"<div style='text-align: center; border: 1px solid black; padding: 10px; margin: 20px 0;'>"
            f"UKNJIŽBU PRAVA SLUŽNOSTI<br>"
            f"({vrsta_tekst})<br>"
            f"{petitum_upis}</div><br>"
            f"<i>Napomena: {napomena}</i></div>"
            f"<div class='section-title'>POPIS PRILOGA:</div>"
            f"<div class='doc-body'><ol>"
            f"<li>Isprava koja je temelj za uknjižbu služnosti ({format_text(pravni_temelj)})</li>"
            f"{geodetski_prilog}"
            f"<li>Izvadak iz zemljišne knjige (poslužno dobro)</li>"
            f"{'<li>Izvadak iz zemljišne knjige (povlasno dobro)</li>' if je_stvarna and ko_povlasno else ''}"
            f"<li>Dokaz o uplati sudske pristojbe</li>"
            f"</ol></div>"
            f"{troskovnik_html}<br>"
            f"<div class='doc-body justified'>"
            f"U {format_text(u_lokativu(mjesto))}, {datum}</div><br><br>"
            f'<table width="100%" border="0"><tr><td width="50%"></td>'
            f'<td width="50%" align="center"><b>PREDLAGATELJ</b><br><br>______________________</td></tr></table>'
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_brisovno_ocitovanje(vjerovnik, vlasnik, podaci):
    """Brisovno ocitovanje (Loschungserklarung) — samostalan dokument vjerovnika
    s clausulom intabulandi za brisanje zaloznog prava (hipoteke) iz zk."""
    try:
        ko = format_text(podaci.get('ko', ''))
        ulozak = format_text(podaci.get('ulozak', ''))
        cestica = format_text(podaci.get('cestica', ''))
        opis_nekretnine = format_text(podaci.get('opis_nekretnine', ''))
        z_broj = format_text(podaci.get('z_broj', ''))
        datum_upisa = format_text(podaci.get('datum_upisa', ''))
        iznos_trazbine = format_text(podaci.get('iznos_trazbine', ''))
        razlog_prestanka = format_text(podaci.get('razlog_prestanka', 'isplate cjelokupne tražbine'))
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')

        upis_info = []
        if z_broj:
            upis_info.append(f"<b>Pod brojem upisa (Z):</b> {z_broj}")
        if datum_upisa:
            upis_info.append(f"<b>Datum upisa:</b> {datum_upisa}")
        if iznos_trazbine:
            upis_info.append(f"<b>Osigurana tražbina:</b> {iznos_trazbine}")
        upis_html = "<br>".join(upis_info)

        upis_default = f"Založno pravo upisano u C list (Teretovnicu) zk.ul. {ulozak}, K.O. {ko}."

        return (
            f"<div class='header-doc'>BRISOVNO OČITOVANJE<br>"
            f"<span style='font-size: 11pt; font-weight: normal;'>(Clausula Intabulandi za brisanje založnog prava)</span></div>"
            f"<div class='party-info'><b>VJEROVNIK (izdavatelj očitovanja):</b><br>{vjerovnik}</div><br>"
            f"<div class='party-info'><b>VLASNIK NEKRETNINE:</b><br>{vlasnik}</div><br>"
            f"<div class='doc-body'>Vjerovnik ovime potvrđuje da je njegova tražbina osigurana založnim pravom "
            f"(hipotekom) na nižeopisanoj nekretnini <b>prestala</b> uslijed {razlog_prestanka}, "
            f"te da Vjerovnik nema više nikakvih potraživanja koja bi bila osigurana navedenim založnim pravom.</div>"
            f"<div class='section-title'>I. NEKRETNINA</div>"
            f"<div class='doc-body'>"
            f"<b>Katastarska općina (k.o.):</b> {ko}<br>"
            f"<b>Broj zk. uloška:</b> {ulozak}<br>"
            f"<b>Broj čestice (k.č.br.):</b> {cestica}<br>"
            f"{f'<b>Opis u naravi:</b> {opis_nekretnine}<br>' if opis_nekretnine else ''}"
            f"</div>"
            f"<div class='section-title'>II. UPIS KOJI SE BRIŠE</div>"
            f"<div class='doc-body'>{upis_html if upis_html else upis_default}</div>"
            f"<div class='section-title'>III. CLAUSULA INTABULANDI</div>"
            f"<div class='doc-body clausula'>"
            f"Vjerovnik ovime <b>izričito i bezuvjetno dopušta</b> da se na temelju ovog Brisovnog očitovanja "
            f"u zemljišnim knjigama provede <b>brisanje</b> založnog prava (hipoteke) upisanog u korist Vjerovnika "
            f"na gore opisanoj nekretnini, bez daljnje suglasnosti i bez prisutnosti Vjerovnika.<br><br>"
            f"Ovo Brisovno očitovanje predstavlja samostalnu i potpunu ispravu temeljem koje vlasnik nekretnine "
            f"može podnijeti zemljišnoknjižni prijedlog za brisanje upisa."
            f"</div>"
            f"<br>"
            f"<div class='justified'>U {u_lokativu(mjesto)}, dana {datum}.</div><br>"
            f"<table width='100%'><tr>"
            f"<td width='40%'></td>"
            f"<td width='60%' align='center'><b>VJEROVNIK</b><br>(potpis ovjeren kod javnog bilježnika)<br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_upis_plodouzivanja(sud, vlasnik, plodouzivatelj, podaci, troskovi_dict):
    """Prijedlog za uknjizbu prava plodouzivanja (uzufrukta) — osobne sluznosti.
    Pravni temelj: ZV cl. 199-219."""
    try:
        ko = format_text(podaci.get('ko', ''))
        ulozak = format_text(podaci.get('ulozak', ''))
        cestica = format_text(podaci.get('cestica', ''))
        opis_nekretnine = format_text(podaci.get('opis_nekretnine', ''))
        opseg = format_text(podaci.get('opseg', 'puno plodouživanje (uživanje stvari u cijelosti)'))
        ogranicenja = format_text(podaci.get('ogranicenja', ''))
        pravni_temelj = format_text(podaci.get('pravni_temelj', ''))
        naknada = format_text(podaci.get('naknada', 'bez naknade'))
        trajanje = format_text(podaci.get('trajanje', 'doživotno (do smrti plodouživatelja)'))
        mjesto = podaci.get('mjesto', '')
        datum = date.today().strftime('%d.%m.%Y.')

        troskovnik_html = formatiraj_troskovnik(troskovi_dict)

        return (
            f'<div style="font-weight: bold; font-size: 14px;">{sud.upper()}</div>'
            f'<div style="font-size: 12px;">Zemljišnoknjižni odjel</div><br><br>'
            f"<div class='party-info'><b>PREDLAGATELJ (vlasnik):</b><br>{vlasnik}</div>"
            f"<div class='party-info'><b>PLODOUŽIVATELJ (ovlaštenik osobne služnosti):</b><br>{plodouzivatelj}</div><br>"
            f"<div class='header-doc'>PRIJEDLOG ZA UKNJIŽBU<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>prava plodouživanja (uzufrukta) — osobne služnosti</span></div>"
            f"<div class='doc-body'><b>I. NEKRETNINA</b><br><br>"
            f"<b>Katastarska općina (k.o.):</b> {ko}<br>"
            f"<b>Broj zk. uloška:</b> {ulozak}<br>"
            f"<b>Broj čestice (k.č.br.):</b> {cestica}<br>"
            f"{f'<b>Opis u naravi:</b> {opis_nekretnine}' if opis_nekretnine else ''}</div>"
            f"<div class='doc-body'><b>II. PRAVO KOJE SE UPISUJE</b><br><br>"
            f"<b>Vrsta prava:</b> Pravo plodouživanja (uzufrukt) — osobna služnost<br>"
            f"<b>Opseg:</b> {opseg}<br>"
            f"{f'<b>Ograničenja / izuzeća:</b> {ogranicenja}<br>' if ogranicenja else ''}"
            f"<b>Naknada:</b> {naknada}<br>"
            f"<b>Trajanje:</b> {trajanje}</div>"
            f"<div class='doc-body'><b>III. PRAVNI TEMELJ</b><br><br>"
            f"{pravni_temelj}<br><br>"
            f"<i>Pozivajući se na članke 199. — 213. Zakona o vlasništvu i drugim stvarnim pravima "
            f"(NN 91/96 i izmjene) o osobnim služnostima.</i></div>"
            f"<div class='doc-body'><b>IV. PETITUM</b><br><br>"
            f"Predlaže se da naslovni sud u zemljišnoj knjizi dozvoli i provede:<br><br>"
            f"<div style='text-align: center; border: 1px solid black; padding: 10px; margin: 20px 0;'>"
            f"UKNJIŽBU PRAVA PLODOUŽIVANJA<br>(uzufrukt — osobna služnost)<br>"
            f"u korist plodouživatelja, u C list (Teretovnicu) zk.ul. {ulozak}, K.O. {ko}</div><br>"
            f"<i>Napomena: Pravo plodouživanja je strogo osobno pravo. Ne prenosi se nasljeđivanjem, "
            f"darovanjem niti prodajom. Prestaje smrću plodouživatelja, odricanjem, propadanjem stvari "
            f"ili istekom roka (ako je ugovoreno na rok).</i></div>"
            f"<div class='section-title'>POPIS PRILOGA:</div>"
            f"<div class='doc-body'><ol>"
            f"<li>Isprava koja je temelj za uknjižbu plodouživanja ({pravni_temelj})</li>"
            f"<li>Izvadak iz zemljišne knjige</li>"
            f"<li>Dokaz o uplati sudske pristojbe</li>"
            f"</ol></div>"
            f"{troskovnik_html}<br>"
            f"<div class='doc-body justified'>"
            f"U {u_lokativu(mjesto) if mjesto else format_text(mjesto)}, {datum}</div><br><br>"
            f'<table width="100%"><tr><td width="50%"></td>'
            f'<td width="50%" align="center"><b>PREDLAGATELJ</b><br><br>______________________</td></tr></table>'
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_punomoc_prodaje_nekretnine(vlastodavac, punomocnik, podaci):
    """Specijalna punomoc za prodaju nekretnine — strukturirani template."""
    try:
        ko = format_text(podaci.get('ko', ''))
        ulozak = format_text(podaci.get('ulozak', ''))
        cestica = format_text(podaci.get('cestica', ''))
        opis_nekretnine = format_text(podaci.get('opis_nekretnine', ''))
        adresa = format_text(podaci.get('adresa', ''))
        povrsina = format_text(podaci.get('povrsina_m2', ''))
        min_cijena = podaci.get('minimalna_cijena_eur', 0)
        min_cijena_str = format_eur(min_cijena) if min_cijena else ''
        rok_vazenja = format_text(podaci.get('rok_vazenja', '12 (dvanaest) mjeseci od datuma ovjere'))
        mjesto = podaci.get('mjesto', 'Zagreb')
        datum = date.today().strftime('%d.%m.%Y.')

        nekretnina_rows = []
        if ko:
            nekretnina_rows.append(f"<b>Katastarska općina (k.o.):</b> {ko}")
        if ulozak:
            nekretnina_rows.append(f"<b>Broj zk. uloška:</b> {ulozak}")
        if cestica:
            nekretnina_rows.append(f"<b>Broj čestice (k.č.br.):</b> {cestica}")
        if opis_nekretnine:
            nekretnina_rows.append(f"<b>Opis u naravi:</b> {opis_nekretnine}")
        if adresa:
            nekretnina_rows.append(f"<b>Adresa:</b> {adresa}")
        if povrsina:
            nekretnina_rows.append(f"<b>Površina (m²):</b> {povrsina}")
        nekretnina_html = "<br>".join(nekretnina_rows)

        cijena_klauzula = (
            f"<li>pregovarati o kupoprodajnoj cijeni, ali ne ispod iznosa od <b>{min_cijena_str}</b>;</li>"
            if min_cijena_str else
            "<li>pregovarati o kupoprodajnoj cijeni i prihvatiti onu koju smatra najpovoljnijom;</li>"
        )

        return (
            f"<div class='header-doc'>SPECIJALNA PUNOMOĆ<br>"
            f"<span style='font-size: 12pt; font-weight: normal;'>za prodaju nekretnine</span></div>"
            f"<div class='justified'>Ja, dolje potpisani/a:</div><br>"
            f"<div class='party-info'><b>VLASTODAVAC (vlasnik nekretnine):</b><br>{vlastodavac}</div><br>"
            f"<div class='justified'>kao isključivi vlasnik nižeopisane nekretnine, ovime dajem</div><br>"
            f"<div style='text-align: center; font-weight: bold; font-size: 14pt; margin: 20px 0;'>SPECIJALNU PUNOMOĆ</div>"
            f"<div class='party-info'><b>PUNOMOĆNIKU:</b><br>{punomocnik}</div><br>"
            f"<div class='justified'>za prodaju sljedeće nekretnine:</div><br>"
            f"<div class='doc-body'>{nekretnina_html}</div>"
            f"<div class='justified'>Punomoćnik je ovlašten u moje ime i za moj račun:</div>"
            f"<div class='doc-body'><ol>"
            f"<li>oglasiti i ponuditi nekretninu na prodaju (uključujući angažiranje agencije za posredovanje);</li>"
            f"{cijena_klauzula}"
            f"<li>sklopiti i potpisati Predugovor i Ugovor o kupoprodaji nekretnine s kupcem po izboru punomoćnika;</li>"
            f"<li>potpisati i ovjeriti Tabularnu izjavu (clausulu intabulandi) za upis prava vlasništva u korist kupca;</li>"
            f"<li>preuzeti kupoprodajnu cijenu (ili dio cijene kao kaparu/predujam) i izdati potvrdu o primitku;</li>"
            f"<li>predati nekretninu kupcu u posjed sa svim pripadnostima i ispravama (energetski certifikat, "
            f"povijesni izvadak iz zk., dokaz o plaćenim režijama i komunalnim naknadama);</li>"
            f"<li>obavljati sve poslove pri zemljišnoknjižnom odjelu, poreznoj upravi, javnom bilježniku i "
            f"drugim tijelima potrebne za prijenos prava vlasništva i prijavu poreza na promet nekretnina;</li>"
            f"<li>poduzimati sve ostale pravne i faktične radnje potrebne za uspješan dovršetak kupoprodaje.</ol></div>"
            f"<div class='justified'>Ova specijalna punomoć vrijedi {rok_vazenja}, ako prije ne bude opozvana "
            f"u pisanom obliku s ovjerenim potpisom.</div><br>"
            f"<div class='justified'>Pravni temelj: članci 308. — 331. Zakona o obveznim odnosima "
            f"i odredbe Zakona o zemljišnim knjigama o uknjižbi na temelju ovjerenih isprava.</div><br>"
            f"<div class='justified'>U {u_lokativu(mjesto)}, dana {datum}.</div><br>"
            f"<table width='100%'><tr>"
            f"<td width='40%'></td>"
            f"<td width='60%' align='center'><b>VLASTODAVAC</b><br>(potpis ovjeren kod javnog bilježnika)<br><br>______________________</td>"
            f"</tr></table>"
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
