# -----------------------------------------------------------------------------
# GENERATORI: Punomoc (opca i posebna)
# Pravni temelj: ZPP cl. 89-98, ZOO cl. 308-331
# -----------------------------------------------------------------------------
from datetime import date
from pomocne import format_text, u_lokativu


def generiraj_punomoc(vrsta, vlastodavac, punomocnik, podaci):
    """
    Generira punomoć - opću ili posebnu.
    vrsta: 'opca' ili 'posebna'
    """
    try:
        danas = date.today().strftime("%d.%m.%Y.")
        mjesto = podaci.get("mjesto", "Zagreb")

        if vrsta == "opca":
            return _opca_punomoc(vlastodavac, punomocnik, podaci, mjesto, danas)
        else:
            return _posebna_punomoc(vlastodavac, punomocnik, podaci, mjesto, danas)
    except Exception as e:
        return f"<div class='doc-body'>Greška pri generiranju dokumenta: {e}</div>"


def _opca_punomoc(vlastodavac, punomocnik, podaci, mjesto, danas):
    return (
        f"<div class='header-doc'>OPĆA PUNOMOĆ</div>"
        f"<div class='justified'>Ja, dolje potpisani/a:</div><br>"
        f"<div class='party-info'><b>VLASTODAVAC (opunomoćitelj):</b><br>{vlastodavac}</div><br>"
        f"<div class='justified'>ovime dajem</div><br>"
        f"<div style='text-align: center; font-weight: bold; font-size: 14pt; margin: 20px 0;'>OPĆU PUNOMOĆ</div>"
        f"<div class='party-info'><b>PUNOMOĆNIK:</b><br>{punomocnik}</div><br>"
        f"<div class='justified'>da me zastupa u svim pravnim poslovima i pred svim sudovima, "
        f"upravnim i drugim državnim tijelima, pravnim i fizičkim osobama, "
        f"sa svim pravima koja pripadaju stranci u postupku, uključujući:</div><br>"
        f"<div class='justified'>"
        f"- podnošenje tužbi, prijedloga, žalbi i izvanrednih pravnih lijekova;<br>"
        f"- sklapanje nagodbi;<br>"
        f"- priznavanje i odricanje od tužbenog zahtjeva;<br>"
        f"- poduzimanje svih ostalih pravnih radnji u moje ime i za moj račun.</div><br>"
        f"<div class='justified'>Ova punomoć vrijedi do opoziva.</div><br>"
        f"<div class='justified'>Na temelju članka 89. - 98. Zakona o parničnom postupku (NN 53/91, 91/92, 112/99, "
        f"88/01, 117/03, 2/07, 84/08, 96/08, 123/08, 57/11, 148/11, 25/13, 89/14, 70/19, 80/22, 114/22, 155/23) "
        f"i članka 308. - 331. Zakona o obveznim odnosima.</div><br>"
        f"<br>"
        f"<div class='justified'>U {u_lokativu(mjesto)}, dana {danas}</div><br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>VLASTODAVAC</b><br>(vlastoručni potpis)</div>"
        f"</div>"
    )


def _posebna_punomoc(vlastodavac, punomocnik, podaci, mjesto, danas):
    opseg = format_text(podaci.get("opseg", ""))
    sud = podaci.get("sud", "")
    poslovni_broj = podaci.get("poslovni_broj", "")

    predmet_info = ""
    if sud:
        predmet_info += f"Pred sudom: <b>{sud}</b><br>"
    if poslovni_broj:
        predmet_info += f"Poslovni broj: <b>{poslovni_broj}</b><br>"

    return (
        f"<div class='header-doc'>POSEBNA PUNOMOĆ</div>"
        f"<div class='justified'>Ja, dolje potpisani/a:</div><br>"
        f"<div class='party-info'><b>VLASTODAVAC (opunomoćitelj):</b><br>{vlastodavac}</div><br>"
        f"<div class='justified'>ovime dajem</div><br>"
        f"<div style='text-align: center; font-weight: bold; font-size: 14pt; margin: 20px 0;'>POSEBNU PUNOMOĆ</div>"
        f"<div class='party-info'><b>PUNOMOĆNIK:</b><br>{punomocnik}</div><br>"
        f"<div class='justified'>da me zastupa u sljedećem predmetu:</div><br>"
        f"<div class='justified'>{predmet_info}{opseg}</div><br>"
        f"<div class='justified'>Punomoćnik je ovlašten poduzimati sve pravne radnje u okviru "
        f"ovog predmeta, uključujući podnošenje podnesaka, zastupanje na ročištima, "
        f"ulaganje pravnih lijekova te primanje pismena.</div><br>"
        f"<div class='justified'>Na temelju članka 89. - 98. Zakona o parničnom postupku (NN 53/91, 91/92, 112/99, "
        f"88/01, 117/03, 2/07, 84/08, 96/08, 123/08, 57/11, 148/11, 25/13, 89/14, 70/19, 80/22, 114/22, 155/23) "
        f"i članka 308. - 331. Zakona o obveznim odnosima.</div><br>"
        f"<br>"
        f"<div class='justified'>U {u_lokativu(mjesto)}, dana {danas}</div><br>"
        f"<div class='signature-row'>"
        f"<div class='signature-block'><b>VLASTODAVAC</b><br>(vlastoručni potpis)</div>"
        f"</div>"
    )
