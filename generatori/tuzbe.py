# -----------------------------------------------------------------------------
# GENERATORI: Tuzbe (parnicni postupak, brisovna tuzba)
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import _escape, format_text, formatiraj_troskovnik, format_eur, format_eur_s_rijecima


def generiraj_tuzbu_pro(sud, zastupanje, tuzitelj, tuzenik, vps, vrsta, data, troskovi_dict):
    try:
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        return f"""
        <div style="font-weight: bold; font-size: 14px;">{sud.upper()}</div>
        <div style="font-size: 12px;">{zastupanje}</div>
        <br>
        <div class='justified'>
        <b>TUŽITELJ:</b> {tuzitelj}<br>
        <b>TUŽENIK:</b> {tuzenik}
        <br><br>
        <b>Radi:</b> {_escape(vrsta)}<br>
        <b>Vrijednost predmeta spora (VPS): {format_eur(vps)}</b>
        </div>
        <br>
        <div class='header-doc'>TUŽBA</div>
        <div class='section-title'>I. ČINJENIČNI NAVODI</div>
        <div class='justified'>{format_text(data['cinjenice'])}</div>
        <div class='section-title'>II. DOKAZI</div>
        <div class='justified'>Predlaže se izvođenje sljedećih dokaza:<br>{format_text(data['dokazi'])}</div>
        <div class='section-title'>III. TUŽBENI ZAHTJEV</div>
        <div class='justified'>Slijedom navedenog, budući da Tuženik nije podmirio svoju dospjelu obvezu, Tužitelj predlaže da naslovni Sud donese sljedeću<br><br>
        <div style="text-align: center; font-weight: bold;">PRESUDU</div><br>
        <b>I. Nalaže se Tuženiku</b> da Tužitelju isplati iznos od <b>{format_eur_s_rijecima(vps)}</b> zajedno sa zakonskom zateznom kamatom koja teče od dana dospijeća {data['datum_dospijeca']} pa do isplate, po stopi određenoj zakonom.<br><br>
        <b>II. Nalaže se Tuženiku</b> da Tužitelju naknadi troškove ovog parničnog postupka, u roku od 15 dana, zajedno sa zateznom kamatom od dana donošenja presude do isplate.
        </div>
        {troskovnik_html}
        <br><br>
        <div class='signature-row'><div style='display:inline-block; width: 50%;'><b>PRILOZI:</b><br>1. Punomoć<br>2. Dokaz o uplati pristojbe<br>3. Dokazi navedeni u točki II.</div>
        <div class='signature-block'><b>TUŽITELJ</b><br>(po punomoćniku)<br><br>______________________</div></div>
        """
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def generiraj_brisovnu_tuzbu(sud, zastupanje, tuzitelj, tuzenik, nekretnina, podaci_spora, troskovi_dict):
    try:
        datum = date.today().strftime("%d.%m.%Y.")
        troskovnik_html = formatiraj_troskovnik(troskovi_dict)
        tekst_savjesnost = (
            "Tuženik je prilikom stjecanja bio nesavjestan..."
            if podaci_spora['tuzenik_znao']
            else "Tužba se podnosi u zakonskom roku..."
        )
        return (
            f'<div style="font-weight: bold; font-size: 14px; text-align: left;">{sud.upper()}</div>'
            f'<div style="font-size: 12px; text-align: left;">{zastupanje}</div><br>'
            f"<div class='party-info'><b>PRAVNA STVAR:</b><br><b>TUŽITELJ:</b> {tuzitelj}<br><b>TUŽENIK:</b> {tuzenik}</div>"
            f"<div class='party-info'><b>Radi:</b> Brisanja uknjižbe i uspostave prijašnjeg ZK stanja<br>"
            f"<b>Vrijednost predmeta spora (VPS): {format_eur(podaci_spora['vps'])}</b></div><br>"
            f"<div class='header-doc'>BRISOVNA TUŽBA</div>"
            f"<div class='section-title'>I. ČINJENIČNI NAVODI</div>"
            f"<div class='doc-body'>Tužitelj je bio isključivi vlasnik nekretnine upisane u "
            f"<b>zk.ul. {nekretnina['ulozak']}, k.o. {nekretnina['ko']}, k.č.br. {nekretnina['cestica']}</b>.<br><br>"
            f"Dana {podaci_spora['datum_uknjizbe']}, u zemljišnim knjigama naslovnog suda, pod brojem "
            f"<b>{podaci_spora['z_broj']}</b>, provedena je nevaljana uknjižba prava vlasništva u korist Tuženika "
            f"na temelju isprave: {podaci_spora['isprava']}.<br><br>"
            f"Tužitelj tvrdi da je navedena isprava ništetna iz sljedećih razloga:<br>"
            f"<i>{podaci_spora['razlog_nevaljanosti']}</i><br><br>"
            f"{tekst_savjesnost}</div>"
            f"<div class='section-title'>DOKAZI:</div>"
            f"<div class='doc-body'>1. ZK izvadak.<br>2. Uvid u ZK spis broj {podaci_spora['z_broj']}.<br>"
            f"3. {podaci_spora['isprava']}.</div>"
            f"<div class='section-title'>II. TUŽBENI ZAHTJEV</div>"
            f"<div class='doc-body'>Slijedom navedenog, Tužitelj predlaže da Sud donese sljedeću</div>"
            f'<div style="text-align: center; font-weight: bold; margin: 10px 0;">PRESUDU</div>'
            f"<div class='doc-body'><b>I. Utvrđuje se da je ništetan</b> {podaci_spora['isprava']}.<br><br>"
            f"<b>II. Utvrđuje se da je nevaljana uknjižba</b> prava vlasništva u korist tuženika, provedena pod brojem {podaci_spora['z_broj']}.<br><br>"
            f"<b>III. Nalaže se brisanje uknjižbe</b> i uspostava prijašnjeg stanja.<br><br>"
            f"<b>IV.</b> Nalaže se Tuženiku naknaditi trošak.</div>"
            f"{troskovnik_html}<br><br>"
            f'<table width="100%" border="0"><tr>'
            f'<td width="50%" align="left">U {podaci_spora["mjesto"]}, dana {datum}</td>'
            f'<td width="50%" align="center"><b>TUŽITELJ</b><br><br><br>______________________</td></tr></table>'
        )
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
