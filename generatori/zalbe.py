# -----------------------------------------------------------------------------
# GENERATORI: Zalbe
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, formatiraj_troskovnik


def generiraj_zalbu_pro(sud_prvi, sud_drugi, stranke, podaci_o_presudi, razlozi, tekst_obrazlozenja, troskovnik):
    try:
        troskovnik_html = formatiraj_troskovnik(troskovnik)
        danas = date.today().strftime("%d.%m.%Y.")
        razlozi_html = "<ul>" + "".join([f"<li>{r}</li>" for r in razlozi]) + "</ul>"
        return f"""
        <div style="font-weight: bold; font-size: 14px;">{sud_drugi.upper()}</div><div>(kao drugostupanjskom sudu)</div><br><div>putem</div><br><div style="font-weight: bold;">{sud_prvi.upper()}</div><div>(kao prvostupanjskog suda)</div><br><br>
        <div class='justified'><b>PRAVNA STVAR:</b><br><b>TUŽITELJ:</b> {stranke['tuzitelj']}<br><b>TUŽENIK:</b> {stranke['tuzenik']}<br><b>Poslovni broj: {podaci_o_presudi['broj']}</b></div><br>
        <div class='header-doc'>ŽALBA</div><div style="text-align: center;">protiv presude {sud_prvi} poslovni broj {podaci_o_presudi['broj']} od dana {podaci_o_presudi['datum']}</div><br>
        <div class='justified'>Žalitelj ovime pravovremeno, u otvorenom zakonskom roku, podnosi žalbu protiv navedene presude {podaci_o_presudi['opseg']} zbog sljedećih zakonskih razloga (čl. 353. ZPP):</div>
        {razlozi_html}
        <div class='section-title'>I. OBRAZLOŽENJE</div><div class='justified'>{format_text(tekst_obrazlozenja)}</div>
        <div class='section-title'>II. PRIJEDLOG</div><div class='justified'>Slijedom navedenog, predlaže se da naslovni drugostupanjski sud ovu žalbu uvaži, pobijanu presudu ukine i predmet vrati prvostupanjskom sudu na ponovno suđenje.</div>
        {troskovnik_html}
        <br><div class='justified'>U {podaci_o_presudi['mjesto']}, dana {danas}</div>
        <div class='signature-row'>
        <div class='signature-block'><b>ŽALITELJ</b><br>(po punomoćniku)</div>
        </div>
        """
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"
