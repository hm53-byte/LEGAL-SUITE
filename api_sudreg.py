# =============================================================================
# API_SUDREG.PY - Sudski registar API klijent (OAuth2 + REST)
# URL: https://sudreg-data.gov.hr/
# Auth: OAuth2 client_credentials (besplatna registracija)
# =============================================================================
import streamlit as st
from datetime import datetime, timedelta

_TOKEN_URL = "https://sudreg-data.gov.hr/connect/token"
_API_BASE = "https://sudreg-data.gov.hr/api/javni"


def _get_credentials():
    """Dohvati OAuth2 credentials iz st.secrets."""
    try:
        return st.secrets.get("sudreg_client_id", ""), st.secrets.get("sudreg_client_secret", "")
    except Exception:
        return "", ""


def _get_token():
    """Dohvati ili refreshaj OAuth2 token."""
    # Provjeri cache
    if "_sudreg_token" in st.session_state:
        token_data = st.session_state._sudreg_token
        if datetime.now() < token_data.get("expires_at", datetime.min):
            return token_data["access_token"]

    client_id, client_secret = _get_credentials()
    if not client_id or not client_secret:
        return None

    try:
        import requests
        resp = requests.post(_TOKEN_URL, data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "javni",
        }, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            st.session_state._sudreg_token = {
                "access_token": data["access_token"],
                "expires_at": datetime.now() + timedelta(seconds=data.get("expires_in", 21600) - 60),
            }
            return data["access_token"]
    except Exception:
        pass
    return None


@st.cache_data(ttl=3600, show_spinner=False)
def pretrazi_subjekt(oib="", mbs=""):
    """Pretrazi subjekt po OIB-u ili MBS-u. Vraca dict s podacima ili None."""
    token = _get_token()
    if not token:
        return {"error": "Sudski registar API nije konfiguriran. Dodajte sudreg_client_id i sudreg_client_secret u Streamlit Secrets."}

    params = {}
    if oib:
        params["oib"] = oib
    elif mbs:
        params["mbs"] = mbs
    else:
        return {"error": "Unesite OIB ili MBS."}

    try:
        import requests
        resp = requests.get(
            f"{_API_BASE}/detalji_subjekta",
            params=params,
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            return {
                "naziv": data.get("tvrtka", data.get("naziv", "")),
                "oib": data.get("oib", oib),
                "mbs": data.get("mbs", mbs),
                "sjediste": data.get("sjediste", ""),
                "adresa": data.get("adresa", ""),
                "zastupnik": data.get("zastupnik", ""),
                "status": data.get("status", ""),
                "oblik": data.get("pravniOblik", ""),
            }
        elif resp.status_code == 404:
            return {"error": f"Subjekt s {'OIB-om ' + oib if oib else 'MBS-om ' + mbs} nije pronaden."}
        else:
            return {"error": f"Greska API-ja: HTTP {resp.status_code}"}
    except Exception as e:
        return {"error": f"Greska pri dohvatu: {str(e)}"}


def je_konfiguriran():
    """Provjeri jesu li API credentials konfigurirani."""
    client_id, client_secret = _get_credentials()
    return bool(client_id and client_secret)


def render_sudreg_lookup(prefix="sr"):
    """Renderira mini-formu za pretragu sudskog registra unutar unos_stranke."""
    with st.expander("\U0001f50d Pretrazi tvrtku po OIB-u (Sudski registar)", expanded=False):
        if not je_konfiguriran():
            st.info(
                "Sudski registar API nije konfiguriran. "
                "Registrirajte se na [sudreg-data.gov.hr](https://sudreg-data.gov.hr/) "
                "i dodajte credentials u Streamlit Secrets."
            )
            return

        oib_input = st.text_input("OIB tvrtke", key=f"{prefix}_sudreg_oib", max_chars=11)
        if st.button("Pretrazi", key=f"{prefix}_sudreg_btn", type="primary"):
            if not oib_input or len(oib_input) != 11:
                st.error("OIB mora imati tocno 11 znamenki.")
            else:
                with st.spinner("Pretrazujem sudski registar..."):
                    result = pretrazi_subjekt(oib=oib_input)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(f"Pronadeno: **{result['naziv']}**")
                    st.markdown(
                        f"- **OIB:** {result['oib']}\n"
                        f"- **MBS:** {result['mbs']}\n"
                        f"- **Sjediste:** {result['sjediste']}\n"
                        f"- **Pravni oblik:** {result['oblik']}\n"
                        f"- **Zastupnik:** {result['zastupnik']}"
                    )
                    # Ponudi auto-popunjavanje
                    if st.button("Popuni podatke u obrazac", key=f"{prefix}_sudreg_fill"):
                        st.session_state[f"{prefix}_naziv"] = result["naziv"]
                        st.session_state[f"{prefix}_adresa"] = result.get("adresa", result.get("sjediste", ""))
                        st.session_state[f"{prefix}_oib"] = result["oib"]
                        st.rerun()
