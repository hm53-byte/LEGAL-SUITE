# =============================================================================
# API_NN.PY - Narodne novine ELI/JSON-LD klijent
# URL: https://narodne-novine.nn.hr/
# ELI format: https://narodne-novine.nn.hr/eli/sluzbeni/{god}/{broj}/{id}
# Rate limit: 3 req/s
# Auth: Nema
# =============================================================================
import streamlit as st
import time
import re
from datetime import datetime

_NN_BASE = "https://narodne-novine.nn.hr"
_RATE_LIMIT_INTERVAL = 0.34  # ~3 req/s
_last_request_time = 0.0


def _rate_limited_get(url, **kwargs):
    """HTTP GET s rate limitingom (max 3 req/s)."""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < _RATE_LIMIT_INTERVAL:
        time.sleep(_RATE_LIMIT_INTERVAL - elapsed)

    import requests
    _last_request_time = time.time()
    return requests.get(url, timeout=15, **kwargs)


@st.cache_data(ttl=86400, show_spinner=False)
def dohvati_zakon_jsonld(godina, broj, id_akta):
    """Dohvati zakonski tekst u JSON-LD formatu putem ELI URL-a."""
    url = f"{_NN_BASE}/eli/sluzbeni/{godina}/{broj}/{id_akta}/json-ld"
    try:
        resp = _rate_limited_get(url, headers={"Accept": "application/ld+json"})
        if resp.status_code == 200:
            return resp.json()
        return {"error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@st.cache_data(ttl=3600, show_spinner=False)
def pretrazi_nn(upit, stranica=1):
    """Pretrazi Narodne novine po tekstu."""
    try:
        resp = _rate_limited_get(
            f"{_NN_BASE}/pretraga",
            params={"q": upit, "page": stranica},
            headers={"Accept": "text/html"},
        )
        if resp.status_code == 200:
            return _parsiraj_rezultate_pretrage(resp.text)
        return {"error": f"HTTP {resp.status_code}", "rezultati": []}
    except Exception as e:
        return {"error": str(e), "rezultati": []}


def _parsiraj_rezultate_pretrage(html_text):
    """Parsiraj HTML rezultate pretrage u strukturirane podatke."""
    rezultati = []
    # Jednostavan regex parser za NN rezultate pretrage
    # Trazi <a> linkove s /clanci/sluzbeni/ patternima
    pattern = r'href="(/clanci/sluzbeni/\d+_\d+_\d+\.html)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html_text)

    for url, naslov in matches[:20]:
        # Izvuci NN broj iz URL-a
        nn_match = re.search(r'(\d+)_(\d+)_(\d+)', url)
        if nn_match:
            godina, broj, redni = nn_match.groups()
            rezultati.append({
                "naslov": naslov.strip(),
                "url": f"{_NN_BASE}{url}",
                "nn_broj": f"NN {broj}/{godina}",
                "godina": godina,
                "broj": broj,
            })

    return {"rezultati": rezultati, "ukupno": len(rezultati)}


# =============================================================================
# BAZA KLJUCNIH ZAKONA (za brzi pristup bez API poziva)
# =============================================================================

KLJUCNI_ZAKONI = {
    "ZOO": {
        "naziv": "Zakon o obveznim odnosima",
        "nn": "NN 35/05, 41/08, 125/11, 78/15, 29/18, 126/21, 114/22, 156/22, 155/23",
        "url": f"{_NN_BASE}/clanci/sluzbeni/2005_03_35_707.html",
    },
    "ZPP": {
        "naziv": "Zakon o parnicnom postupku",
        "nn": "NN 53/91, 91/92, ..., 80/22, 114/22, 155/23",
        "url": f"{_NN_BASE}/clanci/sluzbeni/1991_10_53_1383.html",
    },
    "OZ": {
        "naziv": "Ovrsni zakon",
        "nn": "NN 112/12, 25/13, 93/14, 55/16, 73/17, 131/20",
        "url": f"{_NN_BASE}/clanci/sluzbeni/2012_10_112_2421.html",
    },
    "ZTD": {
        "naziv": "Zakon o trgovackim drustvima",
        "nn": "NN 111/93, ..., 40/19, 34/22, 114/22, 18/23, 130/23",
        "url": f"{_NN_BASE}/clanci/sluzbeni/1993_12_111_2084.html",
    },
    "ZR": {
        "naziv": "Zakon o radu",
        "nn": "NN 93/14, 127/17, 98/19, 151/22, 64/23",
        "url": f"{_NN_BASE}/clanci/sluzbeni/2014_07_93_1872.html",
    },
    "ObZ": {
        "naziv": "Obiteljski zakon",
        "nn": "NN 103/15, 98/19, 47/20, 49/23, 156/23",
        "url": f"{_NN_BASE}/clanci/sluzbeni/2015_09_103_1992.html",
    },
    "ZUP": {
        "naziv": "Zakon o opcem upravnom postupku",
        "nn": "NN 47/09, 110/21",
        "url": f"{_NN_BASE}/clanci/sluzbeni/2009_04_47_1065.html",
    },
    "ZUS": {
        "naziv": "Zakon o upravnim sporovima",
        "nn": "NN 20/10, 143/12, 152/14, 94/16, 29/17, 110/21",
        "url": f"{_NN_BASE}/clanci/sluzbeni/2010_02_20_483.html",
    },
    "KZ": {
        "naziv": "Kazneni zakon",
        "nn": "NN 125/11, 144/12, 56/15, 61/15, 101/17, 118/18, 126/19, 84/21, 114/22, 114/23",
        "url": f"{_NN_BASE}/clanci/sluzbeni/2011_11_125_2498.html",
    },
    "ZZK": {
        "naziv": "Zakon o zemljisnim knjigama",
        "nn": "NN 63/19, 128/22",
        "url": f"{_NN_BASE}/clanci/sluzbeni/2019_06_63_1216.html",
    },
    "SZ": {
        "naziv": "Stecajni zakon",
        "nn": "NN 71/15, 104/17, 36/22",
        "url": f"{_NN_BASE}/clanci/sluzbeni/2015_06_71_1358.html",
    },
    "ZZP": {
        "naziv": "Zakon o zastiti potrosaca",
        "nn": "NN 19/22, 59/23",
        "url": f"{_NN_BASE}/clanci/sluzbeni/2022_02_19_211.html",
    },
    "ZPPI": {
        "naziv": "Zakon o pravu na pristup informacijama",
        "nn": "NN 25/13, 85/15, 69/22",
        "url": f"{_NN_BASE}/clanci/sluzbeni/2013_02_25_419.html",
    },
}


# =============================================================================
# DEMO / FALLBACK PODACI - prikazuju se kad API ne odgovara
# =============================================================================

_DEMO_REZULTATI = {
    "rezultati": [
        {
            "naslov": "Zakon o obveznim odnosima (procisceni tekst)",
            "url": f"{_NN_BASE}/clanci/sluzbeni/2005_03_35_707.html",
            "nn_broj": "NN 35/2005",
            "godina": "2005",
            "broj": "35",
        },
        {
            "naslov": "Zakon o parnicnom postupku (procisceni tekst)",
            "url": f"{_NN_BASE}/clanci/sluzbeni/1991_10_53_1383.html",
            "nn_broj": "NN 53/1991",
            "godina": "1991",
            "broj": "53",
        },
        {
            "naslov": "Ovrsni zakon (procisceni tekst)",
            "url": f"{_NN_BASE}/clanci/sluzbeni/2012_10_112_2421.html",
            "nn_broj": "NN 112/2012",
            "godina": "2012",
            "broj": "112",
        },
    ],
    "ukupno": 3,
    "_demo": True,
}


def generiraj_nn_link(kratica, clanak=None):
    """Generiraj link na NN za dani zakon i opcionalno clanak."""
    zakon = KLJUCNI_ZAKONI.get(kratica)
    if not zakon:
        return None
    url = zakon["url"]
    tekst = f"{zakon['naziv']} ({zakon['nn']})"
    if clanak:
        tekst = f"cl. {clanak}. {zakon['naziv']}"
    return {"url": url, "tekst": tekst, "naziv": zakon["naziv"], "nn": zakon["nn"]}
