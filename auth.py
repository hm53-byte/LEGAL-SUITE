# =============================================================================
# AUTH.PY - Autentikacija korisnika
# Podrzava: email/lozinka, Google OAuth, Apple OAuth, gost pristup
# =============================================================================
import streamlit as st
import hashlib
import secrets
import json
import os
import html as _html_module
import urllib.parse
from datetime import datetime

_USERS_FILE = os.path.join(os.path.dirname(__file__), ".users.json")


# =============================================================================
# HASHING LOZINKI (PBKDF2-SHA256, bez vanjskih ovisnosti)
# =============================================================================

def _hash_password(password, salt=None):
    """PBKDF2-SHA256 hash lozinke s random saltom."""
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return f"{salt}${h.hex()}"


def _verify_password(password, stored):
    """Verificiraj lozinku protiv pohranjenog hasha."""
    try:
        salt, hash_hex = stored.split("$", 1)
        h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
        return h.hex() == hash_hex
    except (ValueError, AttributeError):
        return False


# =============================================================================
# UPRAVLJANJE KORISNICIMA (JSON storage)
# =============================================================================

def _load_users():
    """Ucitaj korisnike iz datoteke."""
    if os.path.exists(_USERS_FILE):
        try:
            with open(_USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def _save_users(users):
    """Spremi korisnike u datoteku."""
    try:
        with open(_USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except IOError:
        pass


def _get_secrets_value(key, default=""):
    """Sigurno dohvati vrijednost iz st.secrets."""
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default


# =============================================================================
# GOOGLE OAUTH
# =============================================================================

def _google_auth_url():
    """Generiraj Google OAuth URL za login."""
    client_id = _get_secrets_value("google_client_id")
    if not client_id:
        return None
    redirect_uri = _get_secrets_value("app_url", "http://localhost:8501")
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"


def _handle_google_callback():
    """Obradi Google OAuth callback (code u query params)."""
    try:
        params = st.query_params
        code = params.get("code")
        if not code:
            return None
        import requests as req
        client_id = _get_secrets_value("google_client_id")
        client_secret = _get_secrets_value("google_client_secret")
        redirect_uri = _get_secrets_value("app_url", "http://localhost:8501")
        if not client_id or not client_secret:
            return None
        token_resp = req.post("https://oauth2.googleapis.com/token", data={
            "code": code, "client_id": client_id, "client_secret": client_secret,
            "redirect_uri": redirect_uri, "grant_type": "authorization_code",
        }, timeout=10)
        if token_resp.status_code != 200:
            return None
        token_data = token_resp.json()
        user_resp = req.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token_data.get('access_token')}"},
            timeout=10,
        )
        if user_resp.status_code == 200:
            info = user_resp.json()
            st.query_params.clear()
            return {"email": info.get("email"), "name": info.get("name", ""), "provider": "google"}
    except Exception:
        pass
    return None


# =============================================================================
# APPLE SIGN-IN (priprema - treba Apple Developer Account)
# =============================================================================

def _apple_auth_url():
    """Generiraj Apple Sign-In URL."""
    client_id = _get_secrets_value("apple_client_id")
    if not client_id:
        return None
    redirect_uri = _get_secrets_value("app_url", "http://localhost:8501")
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "name email",
        "response_mode": "query",
    }
    return f"https://appleid.apple.com/auth/authorize?{urllib.parse.urlencode(params)}"


# =============================================================================
# SESSION HELPERS
# =============================================================================

def provjeri_auth():
    """Provjeri je li korisnik autentificiran."""
    return st.session_state.get("_authenticated", False)


def trenutni_korisnik():
    """Vrati podatke o trenutnom korisniku ili None."""
    if not provjeri_auth():
        return None
    return st.session_state.get("_user", None)


def odjava():
    """Odjavi korisnika."""
    for key in ["_authenticated", "_user"]:
        if key in st.session_state:
            del st.session_state[key]


def _authenticate(email, name, role="user", provider="email"):
    """Postavi korisnika kao autentificiranog."""
    st.session_state._authenticated = True
    st.session_state._user = {
        "email": email,
        "name": name,
        "role": role,
        "provider": provider,
        "login_time": datetime.now().isoformat(),
    }


# =============================================================================
# LOGIN STRANICA — Redizajnirana za bolji UX
# =============================================================================

def login_stranica():
    """Prikazuje login stranicu. Vraca True ako je korisnik autentificiran."""
    if provjeri_auth():
        return True

    # Provjeri Google OAuth callback
    google_user = _handle_google_callback()
    if google_user:
        _authenticate(google_user["email"], google_user["name"], provider="google")
        st.rerun()

    # --- LOGIN UI ---
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Branding
        st.markdown(
            "<div style='text-align:center;margin:3rem 0 1rem;'>"
            "<div style='font-size:3rem;margin-bottom:0.5rem;'>&#9878;&#65039;</div>"
            "<h1 style='color:#1E3A5F;font-size:1.8rem;margin-bottom:0.2rem;"
            "border:none !important;padding:0 !important;font-weight:700;'>"
            "LegalTech Suite Pro</h1>"
            "<p style='color:#64748B;font-size:0.9rem;margin:0 0 0.3rem;'>"
            "Generator pravnih dokumenata za Hrvatsku</p>"
            "<p style='color:#94A3B8;font-size:0.75rem;margin:0;'>"
            "60+ dokumenata &middot; 15 pravnih podrucja &middot; DOCX format</p>"
            "</div>",
            unsafe_allow_html=True,
        )

        # --- GOST PRISTUP (najprominentniji) ---
        st.markdown("")
        if st.button(
            "Isprobaj besplatno",
            type="primary",
            use_container_width=True,
            key="guest_hero_btn",
        ):
            _authenticate("gost@legalsuite.hr", "Gost", role="guest", provider="guest")
            st.rerun()

        st.caption("Bez registracije. Sve funkcije dostupne odmah.")

        st.markdown("---")

        # --- PRIJAVA / REGISTRACIJA (za korisnike koji zele account) ---
        tab_login, tab_register = st.tabs(["Prijava", "Registracija"])

        with tab_login:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="vas@email.com")
                password = st.text_input("Lozinka", type="password")
                submit = st.form_submit_button("Prijavi se", type="primary", use_container_width=True)
                if submit:
                    if not email or not password:
                        st.error("Unesite email i lozinku.")
                    else:
                        admin_email = _get_secrets_value("admin_email", "admin@legalsuite.hr")
                        admin_pw_hash = _get_secrets_value("admin_password_hash", "")
                        if email == admin_email:
                            ok = (
                                (_verify_password(password, admin_pw_hash) if admin_pw_hash else False)
                                or (password == "admin123" and not admin_pw_hash)
                            )
                            if ok:
                                _authenticate(email, "Administrator", role="admin", provider="email")
                                st.rerun()
                            else:
                                st.error("Pogresna lozinka.")
                        else:
                            users = _load_users()
                            if email in users and _verify_password(password, users[email].get("password", "")):
                                _authenticate(email, users[email].get("name", email), provider="email")
                                st.rerun()
                            else:
                                st.error("Pogresan email ili lozinka.")

            # OAuth gumbi ispod login forme
            google_url = _google_auth_url()
            apple_url = _apple_auth_url()
            if google_url or apple_url:
                st.markdown(
                    "<p style='text-align:center;color:#94A3B8;font-size:0.8rem;"
                    "margin:0.5rem 0;'>ili</p>",
                    unsafe_allow_html=True,
                )
                c_google, c_apple = st.columns(2)
                with c_google:
                    if google_url:
                        st.link_button("Google prijava", google_url, use_container_width=True)
                with c_apple:
                    if apple_url:
                        st.link_button("Apple prijava", apple_url, use_container_width=True)

        with tab_register:
            with st.form("register_form"):
                reg_name = st.text_input("Ime i prezime", placeholder="Ivan Horvat")
                reg_email = st.text_input("Email", placeholder="ivan@email.com", key="reg_email")
                reg_pass = st.text_input("Lozinka", type="password", key="reg_pass", help="Min. 6 znakova")
                reg_pass2 = st.text_input("Potvrdite lozinku", type="password", key="reg_pass2")
                reg_submit = st.form_submit_button("Registriraj se", type="primary", use_container_width=True)
                if reg_submit:
                    if not reg_name or not reg_email or not reg_pass:
                        st.error("Sva polja su obavezna.")
                    elif len(reg_pass) < 6:
                        st.error("Lozinka mora imati minimalno 6 znakova.")
                    elif reg_pass != reg_pass2:
                        st.error("Lozinke se ne podudaraju.")
                    elif "@" not in reg_email:
                        st.error("Unesite valjanu email adresu.")
                    else:
                        users = _load_users()
                        if reg_email in users:
                            st.error("Korisnik s tom email adresom vec postoji.")
                        else:
                            users[reg_email] = {
                                "name": reg_name,
                                "password": _hash_password(reg_pass),
                                "created": datetime.now().isoformat(),
                                "role": "user",
                            }
                            _save_users(users)
                            _authenticate(reg_email, reg_name, provider="email")
                            st.rerun()

        st.markdown(
            "<div style='text-align:center;margin-top:1.5rem;color:#94A3B8;font-size:0.7rem;'>"
            "LegalTech Suite Pro &copy; 2026 &middot; v4.1"
            "</div>",
            unsafe_allow_html=True,
        )

    return False


def prikazi_korisnika_sidebar():
    """Prikazi info o korisniku u sidebaru + gumb za odjavu."""
    user = trenutni_korisnik()
    if not user:
        return

    role_labels = {
        "admin": ("Admin", "#DC2626"),
        "user": ("Korisnik", "#1E3A5F"),
        "guest": ("Gost", "#64748B"),
    }
    role = user.get("role", "user")
    label, color = role_labels.get(role, ("Korisnik", "#1E3A5F"))
    name = _html_module.escape(user.get("name", "Korisnik"))

    st.sidebar.markdown(
        f"<div style='background:rgba(255,255,255,0.06);padding:0.5rem 0.7rem;"
        f"border-radius:6px;margin-bottom:0.3rem;'>"
        f"<span style='font-size:0.8rem;color:#CBD5E1;'>{name}</span>"
        f"&nbsp;<span style='background:{color};color:white;padding:1px 5px;border-radius:3px;"
        f"font-size:0.55rem;font-weight:600;'>{label}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    if st.sidebar.button("Odjava", key="_auth_logout", use_container_width=True):
        odjava()
        st.rerun()
