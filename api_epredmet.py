# =============================================================================
# API_EPREDMET.PY - e-Predmet GraphQL klijent
# Endpoint: https://e-predmet.pravosudje.hr/api/
# Auth: Nema (javni pristup)
# =============================================================================
import streamlit as st
import json

_ENDPOINT = "https://e-predmet.pravosudje.hr/api/"


def _graphql_query(query, variables=None):
    """Izvrsi GraphQL upit prema e-Predmet API-ju."""
    try:
        import requests
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        resp = requests.post(
            _ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            if "errors" in data:
                return {"error": data["errors"][0].get("message", "GraphQL greska")}
            return data.get("data", {})
        else:
            return {"error": f"HTTP {resp.status_code}: {resp.text[:200]}"}
    except Exception as e:
        return {"error": f"Greska pri dohvatu: {str(e)}"}


@st.cache_data(ttl=86400, show_spinner=False)
def dohvati_sudove():
    """Dohvati listu svih sudova iz e-Predmet sustava."""
    query = """
    query {
        Courts {
            id
            name
            type
        }
    }
    """
    result = _graphql_query(query)
    if "error" in result:
        return result
    return result.get("Courts", [])


@st.cache_data(ttl=3600, show_spinner=False)
def pretrazi_predmet(broj_predmeta, sud_id):
    """Pretrazi predmet po broju i sudu. Vraca dict s detaljima."""
    query = """
    query($caseNumber: String!, $courtId: Int!) {
        Case(caseNumber: $caseNumber, courtId: $courtId) {
            caseNumber
            court {
                name
                type
            }
            judge
            status
            caseType
            parties {
                name
                role
            }
            events {
                date
                description
                type
            }
        }
    }
    """
    variables = {"caseNumber": broj_predmeta, "courtId": int(sud_id)}
    result = _graphql_query(query, variables)
    if "error" in result:
        return result
    return result.get("Case", {})


def formatiraj_broj_predmeta(oznaka, broj, godina):
    """Formatiraj broj predmeta u standardni format (npr. P-123/2024)."""
    return f"{oznaka}-{broj}/{godina}"


# =============================================================================
# DEMO / FALLBACK PODACI - prikazuju se kad API ne odgovara
# =============================================================================

_DEMO_SUDOVI = [
    {"id": 1, "name": "Opcinski gradanski sud u Zagrebu", "type": "opcinski"},
    {"id": 2, "name": "Opcinski sud u Splitu", "type": "opcinski"},
    {"id": 3, "name": "Opcinski sud u Rijeci", "type": "opcinski"},
    {"id": 4, "name": "Opcinski sud u Osijeku", "type": "opcinski"},
    {"id": 5, "name": "Trgovacki sud u Zagrebu", "type": "trgovacki"},
    {"id": 6, "name": "Trgovacki sud u Splitu", "type": "trgovacki"},
    {"id": 7, "name": "Zupanijski sud u Zagrebu", "type": "zupanijski"},
    {"id": 8, "name": "Zupanijski sud u Splitu", "type": "zupanijski"},
    {"id": 9, "name": "Upravni sud u Zagrebu", "type": "upravni"},
    {"id": 10, "name": "Upravni sud u Splitu", "type": "upravni"},
    {"id": 11, "name": "Upravni sud u Rijeci", "type": "upravni"},
    {"id": 12, "name": "Upravni sud u Osijeku", "type": "upravni"},
    {"id": 13, "name": "Visoki upravni sud Republike Hrvatske", "type": "upravni"},
    {"id": 14, "name": "Vrhovni sud Republike Hrvatske", "type": "vrhovni"},
]

_DEMO_PREDMET = {
    "caseNumber": "P-123/2024",
    "court": {"name": "Opcinski gradanski sud u Zagrebu", "type": "opcinski"},
    "judge": "(Demo podatak)",
    "status": "U tijeku",
    "caseType": "Parnicni",
    "parties": [
        {"name": "Ivan Horvat (demo)", "role": "Tuzitelj"},
        {"name": "Marko Novak (demo)", "role": "Tuzenik"},
    ],
    "events": [],
    "_demo": True,
}


def je_demo_rezultat(rezultat):
    """Provjeri je li rezultat demo podatak."""
    if isinstance(rezultat, dict):
        return rezultat.get("_demo", False)
    if isinstance(rezultat, list) and rezultat:
        return isinstance(rezultat[0], dict) and rezultat[0].get("_demo", False)
    return False


# Vrste postupaka - oznake
OZNAKE_POSTUPAKA = {
    "P": "Parnični",
    "Povrv": "Parnični (VPS)",
    "R1": "Izvanparnični",
    "Ovr": "Ovršni",
    "St": "Stečajni",
    "Kzm": "Kazneni - maloljetnici",
    "K": "Kazneni",
    "Kov": "Kazneni - ovršni",
    "Gzp": "Građanski - drugostupanjski",
    "Us": "Upravni spor",
    "UsI": "Upravni spor - prvostupanjski",
    "UsII": "Upravni spor - drugostupanjski",
    "Pn": "Parnični - naknada štete",
    "Ob": "Obiteljskopravni",
    "R2": "Registarski",
    "Z": "Zemljišnoknjižni",
}
