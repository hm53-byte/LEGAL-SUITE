# 06 — KOD: PREPRAVAK `auth.py` (SUPABASE UMJESTO JSON)

> Postojeći `auth.py` koristi `.users.json` koji se briše kod restart-a. Sad ga prepravimo da koristi Supabase, uz **istu javnu API** (funkcije `provjeri_auth()`, `trenutni_korisnik()`, `odjava()`, `login_stranica()`, `prikazi_korisnika_sidebar()`) — tako da ne moraš dirati `LEGAL-SUITE.py`.

---

## 1. ZAŠTO PREPRAVKA, A NE NOVI MODUL

Već imaš `auth.py` koji se koristi iz `LEGAL-SUITE.py`:

```python
from auth import login_stranica, prikazi_korisnika_sidebar, provjeri_auth, _authenticate
```

Ako napravimo `auth_v2.py` — moraš mijenjati i `LEGAL-SUITE.py`. Bolje da prepravimo `auth.py` **iznutra** — zadržimo isti interface, promijenimo internu implementaciju.

**Backup prvo:** preimenuj postojeći `auth.py` u `auth_old.py` (za slučaj da nešto pukne, vrati se).

---

## 2. NOVI SADRŽAJ `auth.py`

Otvori `APLIKACIJA/auth.py` i **zamijeni** sav sadržaj sljedećim:

```python
# =============================================================================
# AUTH.PY — Supabase autentikacija
# Zadržava istu javnu API kao stara verzija (login_stranica, provjeri_auth, ...)
# Ali interno koristi Supabase Auth umjesto JSON datoteke.
# =============================================================================
"""
Funkcije koje su iste kao u staroj verziji (drop-in replacement):
    - provjeri_auth()           -> bool
    - trenutni_korisnik()       -> dict | None
    - odjava()
    - login_stranica()          -> bool (True ako autentificiran)
    - prikazi_korisnika_sidebar()

Internoga koristi Supabase Auth API umjesto PBKDF2 + JSON storage.
"""
import streamlit as st
from datetime import datetime
import html as _html_module

from billing import _supabase, _set_session_token


# =============================================================================
# SESSION HELPERS — javni API (kompatibilno sa starom verzijom)
# =============================================================================

def provjeri_auth() -> bool:
    """Vrati True ako je korisnik autentificiran u trenutnoj sesiji."""
    return st.session_state.get("_authenticated", False)


def trenutni_korisnik() -> dict | None:
    """Vrati dict s podacima trenutnog korisnika ili None."""
    if not provjeri_auth():
        return None
    return st.session_state.get("_user", None)


def odjava():
    """Odjavi korisnika — Supabase sign out + brisanje session_state."""
    try:
        _supabase().auth.sign_out()
    except Exception:
        # Ako poziv API-ju padne, svejedno čisti lokalnu sesiju
        pass

    for key in ["_authenticated", "_user", "_sb_access", "_sb_refresh"]:
        st.session_state.pop(key, None)


# =============================================================================
# INTERNI HELPERS
# =============================================================================

def _set_user_session(session_obj, user_obj, role="user"):
    """
    Sprema podatke korisnika u session_state nakon uspješne prijave.

    Args:
        session_obj: Supabase Session (s access_token, refresh_token)
        user_obj:    Supabase User (s id, email, user_metadata)
        role:        rola u aplikaciji (user / admin / guest)
    """
    st.session_state._authenticated = True
    st.session_state._user = {
        "id": user_obj.id,
        "email": user_obj.email,
        "name": (user_obj.user_metadata or {}).get("full_name", user_obj.email),
        "role": role,
        "provider": (user_obj.app_metadata or {}).get("provider", "email"),
        "login_time": datetime.now().isoformat(),
    }
    # Spremi tokene za reuse u sljedećim rerun-ovima
    st.session_state._sb_access = session_obj.access_token
    st.session_state._sb_refresh = session_obj.refresh_token

    # Aktiviraj sesiju u Supabase klijentu (za RLS)
    _set_session_token(session_obj.access_token, session_obj.refresh_token)


def _try_restore_session():
    """
    Pri svakom rerun-u: ako imamo spremljene tokene, vrati Supabase klijent
    u 'logged in' stanje (bez ovoga, RLS odbije query-je).
    """
    if provjeri_auth() and st.session_state.get("_sb_access"):
        try:
            _set_session_token(
                st.session_state._sb_access,
                st.session_state._sb_refresh,
            )
        except Exception:
            # Token expirao ili nevažeći — odjavi
            odjava()


# =============================================================================
# OAUTH CALLBACK — obrada povratka s Google logina
# =============================================================================

def _handle_oauth_callback():
    """
    Kad korisnik klikne 'Prijava preko Googlea', vraća se na app s
    parametrom u URL-u. Supabase potpisuje token u tom URL-u.
    """
    try:
        params = st.query_params
        access_token = params.get("access_token")
        refresh_token = params.get("refresh_token")
        if not access_token:
            return False

        sb = _supabase()
        sb.auth.set_session(access_token, refresh_token or "")
        user_resp = sb.auth.get_user()
        user = user_resp.user
        if user:
            session_obj = type("S", (), {
                "access_token": access_token,
                "refresh_token": refresh_token or "",
            })()
            _set_user_session(session_obj, user, role="user")
            st.query_params.clear()
            st.rerun()
    except Exception as e:
        st.error(f"OAuth greška: {str(e)[:100]}")
    return False


# =============================================================================
# LOGIN STRANICA
# =============================================================================

def login_stranica() -> bool:
    """
    Prikazuje login UI.
    Vraća True ako je korisnik autentificiran (npr. iz prethodne sesije).
    """
    _try_restore_session()
    if provjeri_auth():
        return True

    # OAuth callback (Google login povratak)
    _handle_oauth_callback()
    if provjeri_auth():
        return True

    sb = _supabase()

    # ---- UI ----
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Branding header
        st.markdown(
            """
            <div style='text-align:center; margin: 3rem 0 1rem;'>
                <h1 style='color:#1E3A5F; font-size:1.8rem; margin-bottom:0.2rem;
                           border:none !important; padding:0 !important; font-weight:700;'>
                    LegalTech Suite Pro
                </h1>
                <p style='color:#64748B; font-size:0.9rem; margin:0 0 0.3rem;'>
                    Generator pravnih dokumenata za Hrvatsku
                </p>
                <p style='color:#94A3B8; font-size:0.75rem; margin:0;'>
                    1 dokument besplatno · zatim pretplata od 9,99 EUR/tjedno
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_login, tab_register = st.tabs(["Prijava", "Registracija"])

        # ---------- LOGIN TAB ----------
        with tab_login:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="vas@email.com")
                password = st.text_input("Lozinka", type="password")
                submit = st.form_submit_button(
                    "Prijavi se",
                    type="primary",
                    use_container_width=True,
                )
                if submit:
                    if not email or not password:
                        st.error("Unesite email i lozinku.")
                    else:
                        try:
                            res = sb.auth.sign_in_with_password({
                                "email": email,
                                "password": password,
                            })
                            if res.session and res.user:
                                _set_user_session(res.session, res.user)
                                st.rerun()
                            else:
                                st.error("Pogrešan email ili lozinka.")
                        except Exception as e:
                            msg = str(e).lower()
                            if "invalid" in msg or "credentials" in msg:
                                st.error("Pogrešan email ili lozinka.")
                            elif "not confirmed" in msg or "email" in msg:
                                st.error("Email nije potvrđen. Provjerite inbox.")
                            else:
                                st.error(f"Greška: {str(e)[:120]}")

            # Google OAuth gumb
            st.markdown(
                "<p style='text-align:center; color:#94A3B8; font-size:0.8rem; margin:1rem 0;'>ili</p>",
                unsafe_allow_html=True,
            )
            if st.button("Prijava preko Googlea", use_container_width=True, key="google_btn"):
                try:
                    redirect_url = st.secrets.get("APP_URL", "http://localhost:8501")
                    res = sb.auth.sign_in_with_oauth({
                        "provider": "google",
                        "options": {"redirect_to": redirect_url},
                    })
                    if res.url:
                        st.markdown(
                            f"<meta http-equiv='refresh' content='0; url={res.url}'>",
                            unsafe_allow_html=True,
                        )
                        st.info("Preusmjeravamo vas na Google...")
                except Exception as e:
                    st.error(f"Google login nije konfiguriran: {str(e)[:80]}")

            # Reset lozinke
            with st.expander("Zaboravljena lozinka?"):
                reset_email = st.text_input("Email za reset", key="reset_email_input")
                if st.button("Pošalji link za reset", key="reset_btn"):
                    try:
                        sb.auth.reset_password_email(reset_email)
                        st.success("Provjerite email za daljnje upute.")
                    except Exception:
                        st.error("Greška. Provjerite email adresu.")

        # ---------- REGISTRACIJA TAB ----------
        with tab_register:
            with st.form("register_form"):
                reg_name = st.text_input("Ime i prezime", placeholder="Ivan Horvat")
                reg_email = st.text_input("Email", placeholder="ivan@email.com", key="reg_email_input")
                reg_pass = st.text_input("Lozinka", type="password", key="reg_pass_input",
                                          help="Min. 8 znakova, preporučljivo i broj/specijalni znak")
                reg_pass2 = st.text_input("Potvrdite lozinku", type="password", key="reg_pass2_input")

                # GDPR consent
                accepted = st.checkbox(
                    "Slažem se s [Uvjetima korištenja] i [Politikom privatnosti]",
                    key="gdpr_consent",
                )

                reg_submit = st.form_submit_button(
                    "Registriraj se", type="primary", use_container_width=True
                )

                if reg_submit:
                    if not reg_name or not reg_email or not reg_pass:
                        st.error("Sva polja su obavezna.")
                    elif len(reg_pass) < 8:
                        st.error("Lozinka mora imati minimalno 8 znakova.")
                    elif reg_pass != reg_pass2:
                        st.error("Lozinke se ne podudaraju.")
                    elif "@" not in reg_email or "." not in reg_email:
                        st.error("Unesite valjanu email adresu.")
                    elif not accepted:
                        st.error("Morate prihvatiti Uvjete korištenja i Politiku privatnosti.")
                    else:
                        try:
                            res = sb.auth.sign_up({
                                "email": reg_email,
                                "password": reg_pass,
                                "options": {
                                    "data": {"full_name": reg_name},
                                },
                            })
                            if res.session and res.user:
                                # Auto-login (ako email confirmation nije obavezan)
                                _set_user_session(res.session, res.user)
                                st.rerun()
                            elif res.user:
                                # Email confirmation required
                                st.success(
                                    "Registracija uspješna! Provjerite email i kliknite "
                                    "potvrdni link prije prijave."
                                )
                            else:
                                st.error("Registracija nije uspjela. Pokušajte ponovo.")
                        except Exception as e:
                            msg = str(e).lower()
                            if "already" in msg or "registered" in msg:
                                st.error("Korisnik s tom email adresom već postoji.")
                            elif "weak" in msg or "password" in msg:
                                st.error("Lozinka nije dovoljno jaka.")
                            else:
                                st.error(f"Greška: {str(e)[:120]}")

        # Footer
        st.markdown(
            """
            <div style='text-align:center; margin-top:1.5rem; color:#94A3B8; font-size:0.7rem;'>
                LegalTech Suite Pro &copy; 2026 &middot; v5.0
            </div>
            """,
            unsafe_allow_html=True,
        )

    return False


# =============================================================================
# SIDEBAR USER WIDGET
# =============================================================================

def prikazi_korisnika_sidebar():
    """Prikazuje info o korisniku + status pretplate + odjava gumb."""
    user = trenutni_korisnik()
    if not user:
        return

    # Importiraj provjeru pretplate (lazy, da izbjegnemo circular import)
    from billing import ima_aktivnu_pretplatu, broj_iskoristenih_besplatnih

    is_paid = ima_aktivnu_pretplatu(user["id"])

    if is_paid:
        badge_label, badge_color = "PRO", "#059669"
    elif user.get("role") == "admin":
        badge_label, badge_color = "ADMIN", "#DC2626"
    else:
        badge_label, badge_color = "BESPLATNI", "#64748B"

    name = _html_module.escape(user.get("name", "Korisnik"))

    # User badge
    st.sidebar.markdown(
        f"""
        <div style='background: rgba(255,255,255,0.06); padding: 0.5rem 0.7rem;
                    border-radius: 6px; margin-bottom: 0.3rem;'>
            <span style='font-size: 0.8rem; color: #CBD5E1;'>{name}</span>
            &nbsp;<span style='background: {badge_color}; color: white; padding: 1px 5px;
                              border-radius: 3px; font-size: 0.55rem; font-weight: 600;'>
                {badge_label}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Status besplatnih (ako nije plaćen)
    if not is_paid:
        try:
            used = broj_iskoristenih_besplatnih(user["id"])
            st.sidebar.caption(f"Besplatno iskorišteno: {used}/1")
        except Exception:
            pass

    # Manage subscription link (LS customer portal)
    if is_paid:
        portal_url = "https://my-customer.lemonsqueezy.com/billing"
        st.sidebar.markdown(
            f"<small><a href='{portal_url}' target='_blank' style='color:#94A3B8;'>"
            f"Upravljaj pretplatom →</a></small>",
            unsafe_allow_html=True,
        )

    # Odjava
    if st.sidebar.button("Odjava", key="_auth_logout", use_container_width=True):
        odjava()
        st.rerun()


# =============================================================================
# DEPRECATED — privremeno za kompatibilnost s _authenticate() pozivima
# =============================================================================

def _authenticate(email, name, role="user", provider="email"):
    """
    DEPRECATED — staro API za 'gost' login.
    Sad ne radi gost mode (Supabase ne dopušta anonymous insert/select pod RLS-om
    bez odvojene logike). Možeš implementirati gost mode preko 'magic link' s
    automatski generiranim emailom, ali za MVP — uklanjamo.

    Ako trebaš gost demo, kreiraj posebnog 'demo@legalsuite.hr' usera u Supabase
    Authentication, daj mu pretplatu ručno, i prijavi se s tim podacima.
    """
    st.warning(
        "Gost mode je uklonjen u novoj verziji. Molimo registrirajte se."
    )
```

---

## 3. OBJAŠNJENJE KLJUČNIH DIJELOVA

### 3.1 `provjeri_auth()`, `trenutni_korisnik()`, `odjava()`

Identično kao prije, samo internoga koriste novu strukturu.

### 3.2 `_set_user_session()`

Novo. Sprema **tokene** u `st.session_state`:
- `_sb_access` — kratkotrajni token (1 sat)
- `_sb_refresh` — dugotrajni token (mjesec dana, koristi se za obnovu)

Bez ovoga, kod svakog rerun-a Streamlita bi se Supabase klijent vratio u "logged out" stanje.

### 3.3 `_try_restore_session()`

**Najbitniji dio za razumijevanje.** Streamlit rerun-a aplikaciju kod svakog klika. Što znači:
- Klikaš gumb → cijela skripta se pokreće od početka
- `_supabase()` instancira novi klijent (ili vraća cache-ani)
- **Klijent je "logged out"** osim ako mu opet ne kažeš tko je user

`_try_restore_session()` čita tokene iz session_state i postavlja ih na klijenta. Tako Supabase zna da je user prijavljen čak i nakon rerun-a.

### 3.4 OAuth callback handler

Google OAuth radi ovako:
1. User klikne "Prijava preko Googlea"
2. App ga šalje na Google login stranicu
3. User odobri pristup
4. Google ga šalje natrag na tvoj URL s tokenima u **query parametrima** (`?access_token=...&refresh_token=...`)
5. `_handle_oauth_callback()` pročita parametre i postavi sesiju
6. `st.query_params.clear()` makne tokene iz URL-a (security best practice)

### 3.5 Reset lozinke

Pravo email reset koristi Supabase ugrađeni endpoint. Korisnik dobije email s linkom, klikne, otvori se Supabase-ov default UI za novu lozinku. Možeš urediti template-ove u Supabase **Authentication → Email Templates**.

### 3.6 GDPR checkbox u registraciji

Pravno potreban — bez eksplicitnog pristanka **ne smiješ** registrirati korisnika u EU. Linkovi u tekstu ("Uvjetima korištenja", "Politikom privatnosti") trebaju voditi na tvoje stvarne dokumente.

### 3.7 `prikazi_korisnika_sidebar()` — proširen

Novosti:
- Badge mijenja boju i tekst ovisno o pretplati (zelena PRO ili siva BESPLATNI)
- Prikaže "Besplatno iskorišteno: X/1" za free korisnike
- Prikaže "Upravljaj pretplatom →" link za plaćene
- Odjava i dalje radi

### 3.8 Lazy import `from billing import ...` unutar funkcije

Zašto unutar funkcije, ne na vrhu file-a? Da izbjegnemo **circular import**:
- `auth.py` importira `billing.py`
- `billing.py` se isto bi mogao trebati `auth.py` (npr. za check tko je user)

Lazy import (unutar funkcije) odgađa import dok se funkcija ne pozove, čime izbjegavamo zagrljaj.

---

## 4. ŠTO SE PROMIJENILO U ODNOSU NA STARU VERZIJU

| Stara | Nova |
|-------|------|
| PBKDF2-SHA256 + JSON | Supabase Auth |
| `.users.json` na disku | `auth.users` + `profiles` u Postgresu |
| Gost mode auto-auth | **Uklonjen** (vidi napomenu dolje) |
| Admin special-case | Možeš ručno postaviti `role='admin'` u SQL-u |
| Apple Sign-In stub | Uklonjen (može se dodati kasnije kroz Supabase) |
| Sve datoteke lokalne | Sve u oblaku |

### Što s "gost" modom?

Tvoja postojeća app ima `_app_mode = "jednostavno"` koji auto-authenticatea kao gost. Sad to **moraš ukloniti** iz `LEGAL-SUITE.py` jer Supabase RLS onemogućava anonymous query-je.

**Prijedlog:** zamijeni gost mode s "Try it for free" CTA na landing stranici koji vodi na **registraciju**. Konverzija registriranog usera je 10× veća od gosta jer već imaš email.

Ako baš trebaš gost mode (npr. za demo videa), kreiraš posebnog `demo@legalsuite.hr` korisnika ručno u Supabase, daš mu permanent pretplatu (manualno SQL), i staviš "Demo prijava" gumb koji koristi te credentials. Ali to je za 100% kompromis i ne preporučujem za prod.

---

## 5. MODIFIKACIJA `LEGAL-SUITE.py` (MALA)

Otvori `APLIKACIJA/LEGAL-SUITE.py` i nađi ovaj blok (oko linije 81-91):

```python
if "_app_mode" not in st.session_state:
    st.session_state._app_mode = "jednostavno"

if st.session_state._app_mode == "jednostavno":
    if not provjeri_auth():
        _authenticate("gost@legalsuite.hr", "Gost", role="guest", provider="guest")
else:
    if not login_stranica():
        st.stop()
```

**Zamijeni s:**

```python
# Auth obvezan za sve operacije
if not login_stranica():
    st.stop()
```

I obriši `_authenticate` iz import-a (više se ne koristi):

```python
# OLD:
from auth import login_stranica, prikazi_korisnika_sidebar, provjeri_auth, _authenticate

# NEW:
from auth import login_stranica, prikazi_korisnika_sidebar, provjeri_auth
```

To je sve što treba u `LEGAL-SUITE.py`. Ostatak ostaje isti.

---

## 6. KAKO TESTIRAŠ

1. Pokreni lokalno: `streamlit run LEGAL-SUITE.py`
2. Trebao bi vidjeti login ekran (umjesto direktnog ulaska kao gost)
3. Registriraj se s test emailom
4. Provjeri Supabase **Authentication → Users** — trebao bi vidjeti novi red
5. Provjeri **Table Editor → profiles** — trebao bi vidjeti red sa svojim emailom i `free_documents_used = 0`
6. Odjavi se → prijavi se ponovo s istim email/lozinkom — trebalo bi raditi
7. Generiraj dokument → trebao bi raditi (free trial)
8. Vrati se i pokušaj još jedan — trebao bi vidjeti **paywall** (jer si iskoristio 1/1)

---

## TIPIČNI PROBLEMI

**"Login uspije ali nakon rerun-a se odjavi"**
→ `_try_restore_session()` se ne poziva ili tokeni nisu spremljeni. Provjeri da `_set_user_session()` postavlja `_sb_access` i `_sb_refresh`.

**"Email confirmation traži potvrdu, korisnik ne dobiva mail"**
→ Supabase free tier šalje 4 maila/sat. Provjeri spam folder. Za prod — poveži vlastiti SMTP (Resend.com).

**"Google login: 'redirect_uri_mismatch'"**
→ Vrati se u Google Cloud Console → OAuth credentials → provjeri da Authorized redirect URI **točno** odgovara onom koji ti Supabase prikazuje (uključno s `/auth/v1/callback`).

**"`Cannot find _set_session_token`"**
→ Provjeri da je `billing.py` u istom folderu kao `auth.py`. Inače moraš podesiti `sys.path`.

**"Korisnik registriran ali profil ne postoji u `profiles`"**
→ Trigger `on_auth_user_created` nije postavljen. Vrati se u SQL Editor i pokreni `CREATE TRIGGER` blok iz `03_SUPABASE_SETUP.md`.

**"Stara `auth.py` mi je pokrila sve, gdje su hash funkcije?"**
→ Više ne trebaš `_hash_password`, `_verify_password` — Supabase to radi interno. Ako migrirate stare korisnike — vidi `09_LANSIRANJE.md`, sekcija "Migracija postojećih korisnika".

---

## SLJEDEĆI KORAK

Otvori `07_KOD_PAYWALL.md` — modifikacija `pomocne.py` da paywall radi prije svakog download-a.
