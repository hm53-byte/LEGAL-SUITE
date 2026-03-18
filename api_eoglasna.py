# =============================================================================
# API_EOGLASNA.PY - e-Oglasna ploca sudova REST klijent
# URL: https://e-oglasna.pravosudje.hr/
# Auth: Nema (javni pristup, open data)
# =============================================================================
import streamlit as st
from datetime import datetime

_API_BASE = "https://e-oglasna.pravosudje.hr/api"


@st.cache_data(ttl=1800, show_spinner=False)
def pretrazi_objave(sud="", tip="", datum_od="", datum_do="", tekst="", stranica=1, po_stranici=20):
    """Pretrazi objave na e-Oglasnoj ploci.

    Args:
        sud: Naziv ili ID suda
        tip: Tip objave (dostava, drazba, stecaj, ovrha, ostalo)
        datum_od: Datum od (YYYY-MM-DD)
        datum_do: Datum do (YYYY-MM-DD)
        tekst: Slobodni tekst za pretragu
        stranica: Broj stranice
        po_stranici: Broj rezultata po stranici
    """
    params = {"page": stranica, "pageSize": po_stranici}
    if sud:
        params["court"] = sud
    if tip:
        params["type"] = tip
    if datum_od:
        params["dateFrom"] = datum_od
    if datum_do:
        params["dateTo"] = datum_do
    if tekst:
        params["search"] = tekst

    try:
        import requests
        resp = requests.get(
            f"{_API_BASE}/announcements",
            params=params,
            headers={"Accept": "application/json"},
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            return {
                "objave": data.get("items", data.get("results", [])),
                "ukupno": data.get("totalCount", data.get("total", 0)),
                "stranica": stranica,
                "ukupno_stranica": data.get("totalPages", 1),
            }
        else:
            return {"error": f"HTTP {resp.status_code}", "objave": [], "ukupno": 0}
    except Exception as e:
        return {"error": str(e), "objave": [], "ukupno": 0}


@st.cache_data(ttl=86400, show_spinner=False)
def dohvati_sudove_eoglasna():
    """Dohvati listu sudova dostupnih na e-Oglasnoj ploci."""
    try:
        import requests
        resp = requests.get(f"{_API_BASE}/courts", headers={"Accept": "application/json"}, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception:
        return []


# Tipovi objava na e-Oglasnoj ploci
TIPOVI_OBJAVA = {
    "dostava": "Dostava pismena",
    "drazba": "Drazbe i prodaje",
    "stecaj": "Stecajni postupci",
    "ovrha": "Ovrsni postupci",
    "oglas": "Oglasi",
    "ostalo": "Ostale objave",
}


def formatiraj_objavu(objava):
    """Formatiraj jednu objavu za prikaz."""
    naslov = objava.get("title", objava.get("naslov", "Bez naslova"))
    sud = objava.get("court", objava.get("sud", ""))
    datum = objava.get("date", objava.get("datum", ""))
    tip = objava.get("type", objava.get("tip", ""))
    sadrzaj = objava.get("content", objava.get("sadrzaj", ""))

    # Formatiraj datum
    if datum:
        try:
            dt = datetime.fromisoformat(datum.replace("Z", "+00:00"))
            datum = dt.strftime("%d.%m.%Y.")
        except (ValueError, AttributeError):
            pass

    return {
        "naslov": naslov,
        "sud": sud,
        "datum": datum,
        "tip": tip,
        "sadrzaj": sadrzaj[:500] + "..." if len(sadrzaj) > 500 else sadrzaj,
    }
