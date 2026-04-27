# 05 — KOD: NOVI MODUL `billing.py`

> Sad pišeš **prvi novi Python modul** koji će biti most između tvoje aplikacije, Supabase baze i Lemon Squeezy.
>
> Ovaj modul ne diraš puno nakon što ga jednom napišeš — on samo "živi" pored ostalih modula.

---

## 1. ŠTO ĆE OVAJ MODUL RADITI

Tri glavne funkcije:

1. **`smije_generirati(user_id)`** — vraća True/False može li korisnik napraviti dokument
2. **`zabiljezi_koristenje(user_id, doc_type, was_paid)`** — upiše u audit log + povisi brojač free trial-a
3. **`prikazi_paywall(user_id, email)`** — prikaže ekran s tri pretplate i checkout linkovima

Pomoćne funkcije:
- Singleton Supabase klijent
- Provjera aktivne pretplate
- Generiranje LS checkout URL-a s `user_id` u `custom_data`

---

## 2. PRVA STVAR — DODAJ SUPABASE U `requirements.txt`

Otvori `APLIKACIJA/requirements.txt` i dodaj na kraj `supabase>=2.0.0`. Cijeli file treba izgledati:

```
streamlit>=1.28.0,<2.0.0
python-docx>=1.0.0
lxml>=4.9.0
requests>=2.28.0
supabase>=2.0.0
```

Lokalno instaliraj (ako razvijaš lokalno):

```
pip install supabase
```

---

## 3. NAPRAVI FILE `billing.py` U KORIJENU APLIKACIJE

Dakle: `APLIKACIJA/billing.py` (na istoj razini kao `auth.py`).

Cijeli sadržaj kopiraš ispod. Nakon koda slijedi **objašnjenje svake sekcije**.

```python
# =============================================================================
# BILLING.PY — Provjera pretplate i naplata (Supabase + Lemon Squeezy)
# =============================================================================
"""
Modul koji povezuje Streamlit aplikaciju s:
- Supabase bazom (provjera korisnika, pretplata, brojač besplatnih)
- Lemon Squeezy checkout-om (generiranje URL-a za naplatu)

Centralna funkcija je `smije_generirati(user_id)` — koristi se prije svakog
prikaza download gumba.
"""
import streamlit as st
import urllib.parse
import hashlib
from datetime import datetime, timezone
from supabase import create_client, Client


# =============================================================================
# KONSTANTE
# =============================================================================

_FREE_DOCUMENTS_LIMIT = 1   # Koliko dokumenata može korisnik napraviti besplatno


# =============================================================================
# SUPABASE KLIJENT — singleton, jedan po sesiji
# =============================================================================

@st.cache_resource
def _supabase() -> Client:
    """
    Vraća jedan zajednički Supabase klijent kroz cijelu aplikaciju.
    `@st.cache_resource` osigurava da se instancira samo jednom.
    """
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)


def _set_session_token(access_token: str, refresh_token: str):
    """
    Postavi auth tokene na klijenta nakon prijave.
    Bez ovoga, RLS pravila ne znaju 'tko si' i sve query-je odbije.
    """
    _supabase().auth.set_session(access_token, refresh_token)


# =============================================================================
# PROVJERA AKTIVNE PRETPLATE
# =============================================================================

def ima_aktivnu_pretplatu(user_id: str) -> bool:
    """
    Vrati True ako korisnik ima aktivnu (active / on_trial / past_due) pretplatu
    koja još nije istekla.
    """
    if not user_id:
        return False

    sb = _supabase()
    res = (sb.table("subscriptions")
             .select("status, ends_at")
             .eq("user_id", user_id)
             .in_("status", ["active", "on_trial", "past_due"])
             .execute())

    if not res.data:
        return False

    now = datetime.now(timezone.utc)
    for sub in res.data:
        ends_at = sub.get("ends_at")
        if ends_at is None:
            # Nema kraja — aktivna pretplata bez ograničenja
            return True
        # Parse ISO string u datetime
        ends_dt = datetime.fromisoformat(ends_at.replace("Z", "+00:00"))
        if ends_dt > now:
            return True

    return False


# =============================================================================
# BROJAČ BESPLATNIH DOKUMENATA
# =============================================================================

def broj_iskoristenih_besplatnih(user_id: str) -> int:
    """Koliko je korisnik već generirao besplatnih dokumenata."""
    if not user_id:
        return 0

    sb = _supabase()
    res = (sb.table("profiles")
             .select("free_documents_used")
             .eq("id", user_id)
             .single()
             .execute())

    return res.data.get("free_documents_used", 0) if res.data else 0


# =============================================================================
# GLAVNA FUNKCIJA — SMIJE LI KORISNIK GENERIRATI DOKUMENT
# =============================================================================

def smije_generirati(user_id: str) -> tuple[bool, str]:
    """
    Centralna provjera prava na generiranje dokumenta.

    Returns:
        (smije: bool, razlog: str)
        razlog može biti: 'subscribed', 'free_trial (1/1)', 'limit_reached'
    """
    if not user_id:
        return False, "not_authenticated"

    if ima_aktivnu_pretplatu(user_id):
        return True, "subscribed"

    used = broj_iskoristenih_besplatnih(user_id)
    if used < _FREE_DOCUMENTS_LIMIT:
        return True, f"free_trial ({used + 1}/{_FREE_DOCUMENTS_LIMIT})"

    return False, "limit_reached"


# =============================================================================
# BILJEŽENJE KORIŠTENJA — audit log + povećanje brojača
# =============================================================================

def zabiljezi_koristenje(user_id: str, doc_type: str, was_paid: bool, ip: str = ""):
    """
    Zapisuje generaciju u usage_log.
    Ako je was_paid=False, povećava i profiles.free_documents_used za 1.
    """
    if not user_id:
        return

    sb = _supabase()

    # Hash IP-a (GDPR — ne spremamo sirov IP)
    ip_hash = hashlib.sha256(ip.encode("utf-8")).hexdigest()[:16] if ip else None

    # 1) Audit log
    try:
        sb.table("usage_log").insert({
            "user_id": user_id,
            "document_type": doc_type,
            "was_paid": was_paid,
            "ip_hash": ip_hash,
        }).execute()
    except Exception as e:
        # Ako audit ne radi, NE blokirati korisnika
        st.warning(f"Greška u zapisu audit log-a (nije blokirajuća).")

    # 2) Inkrement brojača besplatnih (samo ako nije plaćeno)
    if not was_paid:
        try:
            current = broj_iskoristenih_besplatnih(user_id)
            sb.table("profiles").update({
                "free_documents_used": current + 1
            }).eq("id", user_id).execute()
        except Exception:
            pass


# =============================================================================
# GENERIRANJE LEMON SQUEEZY CHECKOUT URL-A
# =============================================================================

def _ls_checkout_url(plan: str, user_id: str, email: str) -> str:
    """
    Vraća Lemon Squeezy checkout URL s pre-popunjenim podacima.

    Bitno: u 'custom' parametar uvlačimo user_id da Edge Function zna
    kome treba pripisati pretplatu kad webhook dođe.
    """
    base_urls = {
        "weekly":  st.secrets.get("LS_CHECKOUT_WEEKLY", ""),
        "monthly": st.secrets.get("LS_CHECKOUT_MONTHLY", ""),
        "yearly":  st.secrets.get("LS_CHECKOUT_YEARLY", ""),
    }
    base = base_urls.get(plan, "")
    if not base:
        return ""

    params = {
        "checkout[email]": email,
        "checkout[custom][user_id]": user_id,
    }
    separator = "&" if "?" in base else "?"
    return f"{base}{separator}{urllib.parse.urlencode(params)}"


# =============================================================================
# UI — PAYWALL EKRAN
# =============================================================================

def prikazi_paywall(user_id: str, email: str):
    """Prikazuje paywall s tri opcije pretplate."""

    # Glavni banner
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #1E3A5F 0%, #0F2847 100%);
                    color: white; padding: 2rem; border-radius: 12px;
                    margin: 1rem 0; text-align: center;'>
            <h2 style='color: white; margin: 0 0 0.5rem;'>Iskoristili ste besplatni dokument</h2>
            <p style='opacity: 0.85; margin: 0;'>
                Odaberite plan za neograničeno generiranje. Otkaz u bilo kojem trenutku.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    # ----- TJEDNO -----
    with c1:
        st.markdown(
            """
            <div style='border: 1px solid #E2E8F0; border-radius: 10px;
                        padding: 1.5rem; text-align: center; height: 100%;'>
                <h3 style='margin: 0;'>Tjedno</h3>
                <p style='font-size: 2rem; font-weight: 700; color: #1E3A5F; margin: 0.5rem 0;'>
                    9,99 €
                </p>
                <p style='color: #64748B; font-size: 0.85rem;'>Tjedno · obnova svakih 7 dana</p>
                <ul style='text-align: left; font-size: 0.85rem; color: #475569; padding-left: 1.2rem;'>
                    <li>Neograničeno dokumenata</li>
                    <li>DOCX, watermark, header</li>
                    <li>Otkaz bilo kada</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        url = _ls_checkout_url("weekly", user_id, email)
        if url:
            st.link_button("Pretplati se", url, use_container_width=True)

    # ----- MJESEČNO (preporučeno) -----
    with c2:
        st.markdown(
            """
            <div style='border: 2px solid #1E3A5F; border-radius: 10px;
                        padding: 1.5rem; text-align: center; height: 100%;
                        background: #F8FAFC; position: relative;'>
                <span style='position: absolute; top: -12px; left: 50%;
                             transform: translateX(-50%); background: #1E3A5F;
                             color: white; padding: 3px 12px; border-radius: 12px;
                             font-size: 0.7rem; font-weight: 700;'>
                    NAJPOPULARNIJE
                </span>
                <h3 style='margin: 0;'>Mjesečno</h3>
                <p style='font-size: 2rem; font-weight: 700; color: #1E3A5F; margin: 0.5rem 0;'>
                    19,99 €
                </p>
                <p style='color: #64748B; font-size: 0.85rem;'>Mjesečno · obnova svakih 30 dana</p>
                <ul style='text-align: left; font-size: 0.85rem; color: #475569; padding-left: 1.2rem;'>
                    <li>Neograničeno dokumenata</li>
                    <li>DOCX, watermark, header</li>
                    <li>Email podrška</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        url = _ls_checkout_url("monthly", user_id, email)
        if url:
            st.link_button("Pretplati se", url, use_container_width=True, type="primary")

    # ----- GODIŠNJE (najpovoljnije) -----
    with c3:
        st.markdown(
            """
            <div style='border: 1px solid #E2E8F0; border-radius: 10px;
                        padding: 1.5rem; text-align: center; height: 100%;'>
                <h3 style='margin: 0;'>Godišnje</h3>
                <p style='font-size: 2rem; font-weight: 700; color: #059669; margin: 0.5rem 0;'>
                    149 €
                </p>
                <p style='color: #64748B; font-size: 0.85rem;'>Godišnje · ušteda 38%</p>
                <ul style='text-align: left; font-size: 0.85rem; color: #475569; padding-left: 1.2rem;'>
                    <li>Neograničeno dokumenata</li>
                    <li>Prioritetna podrška</li>
                    <li>Najpovoljnije po danu</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        url = _ls_checkout_url("yearly", user_id, email)
        if url:
            st.link_button("Pretplati se", url, use_container_width=True)

    st.caption(
        "Plaćanje obrađuje Lemon Squeezy (Merchant of Record). "
        "Računi i potvrde stižu automatski na email. "
        "PDV je uračunat. Otkaz u bilo kojem trenutku iz email-a ili customer portala."
    )
```

---

## 4. OBJAŠNJENJE SVAKE SEKCIJE (LAIČKI)

### 4.1 `_FREE_DOCUMENTS_LIMIT = 1`

**Što:** koliko dokumenata smije napraviti netko bez pretplate.
**Zašto:** centralizirano u jednoj konstanti — promijeniš na 2 ili 3 i sve se odmah ažurira.
**Kad mijenjati:** ako ti konverzija u plaćeno bude preniska, smanji na 0 (samo demo) ili obrnuto, povećaj na 3 da privučeš više korisnika.

### 4.2 `_supabase()`

**Što:** otvara vezu s Supabase bazom.
**Zašto `@st.cache_resource`:** Streamlit po defaultu **rerun-a cijelu aplikaciju** kod svakog klika. Bez cachiranja, otvarali bismo novu vezu kod svakog klika — sporo i skupo. Ovaj decorator kaže "drži ovu vezu u memoriji, vrati istu sljedeći put".

### 4.3 `_set_session_token()`

**Što:** govori Supabase klijentu "ovo je auth token od korisnika koji je trenutno prijavljen".
**Zašto je važno:** Supabase RLS (Row-Level Security) provjerava `auth.uid()` u SQL-u. Bez tokena, RLS misli da nije nitko prijavljen i odbije sve query-je. Token = "iskaznica".

### 4.4 `ima_aktivnu_pretplatu()`

**Što radi:** pita bazu "ima li ovaj user reda u `subscriptions` s aktivnim statusom i nije istekao?"
**Statusi koji se broje kao aktivni:**
- `active` — uredna naplata
- `on_trial` — trial period
- `past_due` — kartica odbijena, pokušavamo opet (3-dnevni grace period)

**Zašto datetime parse:** Supabase vraća datume kao ISO stringove (`"2026-05-23T15:30:00Z"`), Python ih treba pretvoriti u `datetime` objekte za usporedbu.

### 4.5 `broj_iskoristenih_besplatnih()`

**Što radi:** dohvati polje `free_documents_used` iz tablice `profiles` za zadanog usera.
**Zašto `.single()`:** govori klijentu "očekujem točno 1 red, vrati ga kao dictionary, ne kao listu". Ako profil ne postoji, vraća `None`.

### 4.6 `smije_generirati()` — GLAVNA FUNKCIJA

Tri scenarija:
1. **Nije prijavljen** → ne smije
2. **Ima aktivnu pretplatu** → smije, razlog `subscribed`
3. **Nema pretplatu, ali nije iscrpio besplatne** → smije, razlog `free_trial (X/Y)`
4. **Nema pretplatu i iscrpio besplatne** → ne smije, razlog `limit_reached`

**Vraća tuple `(bool, str)`** — vrijednost + razlog. Razlog koristiš za prikaz info poruke ("Ovo je vaš 1/1 besplatni dokument").

### 4.7 `zabiljezi_koristenje()`

**Što radi:** dva poziva u bazu:
1. INSERT u `usage_log` — zapis "user X je generirao tip Y u trenutku Z"
2. UPDATE `profiles.free_documents_used += 1` (samo ako nije plaćeno)

**Zašto `try/except`:** ako audit log iz nekog razloga ne uspije, **ne** želimo blokirati korisnika. Bolje da generira dokument bez audit-a, nego da padne aplikacija.

**Zašto hash IP-a:** GDPR. IP adresa je osobni podatak. Ako spremiš sirov IP, treba ti pravna podloga. Hash je jednosmjeran (`SHA256`), ne može se vratiti u IP, ali možeš detektirati "isti IP" za abuse detection.

### 4.8 `_ls_checkout_url()`

**Što radi:** sastavi URL koji vodi na Lemon Squeezy stranicu naplate.

**KRITIČNI DIO — `custom_data`:**

Lemon Squeezy podržava `checkout[custom][polje]=vrijednost` parametre koji se prosljeđuju u webhook payload. Ovo je **jedini način** da Edge Function kasnije zna kome pripisati pretplatu.

Kad korisnik plati:
- LS pošalje webhook: `{ ..., meta: { custom_data: { user_id: "abc-123" } } }`
- Edge Function pročita `user_id` i upiše u bazu

Bez `custom_data` — webhook stiže, ali ne znaš kome.

### 4.9 `prikazi_paywall()`

**Što radi:** prikazuje tri kartice s cijenama, gumb "Pretplati se" vodi na LS checkout.

**Dizajn:**
- Mjesečna je u sredini i istaknuta ("NAJPOPULARNIJE") — psihološki, srednja opcija najviše konvertira
- Godišnja u zelenoj boji s "ušteda 38%" — povlači price-sensitive korisnike
- Tjedna kao escape hatch — netko trebao samo jedan dokument, ne želi gnjavažu

**Zašto `st.link_button`:** otvara LS checkout u novom tabu (default Streamlit ponašanje), ne navigira off tvoje aplikacije. Korisnik može plaćati u jednom tabu, vratiti se u drugi.

---

## 5. ŠTO OVAJ MODUL **NE** RADI (i kako bi proširio)

- **Ne provjerava expiraciju kartice** prije naplate (LS to radi sam)
- **Ne šalje email** korisniku kad pretplati ili otkaže (LS šalje sve emailove sam)
- **Ne podržava promo kodove u UI** — korisnik ih unosi direktno u LS checkout
- **Ne ima admin panel** za ručno odobravanje pretplate (ako ti treba, dodaj funkciju koja UPDATE-a `subscriptions` tablicu — ali bolje koristi Supabase web UI za to)

---

## 6. KAKO TESTIRAŠ DA RADI

Trenutno još ne možeš testirati u potpunosti jer treba:
- `auth.py` (sljedeći korak — `06`)
- Edge Function za webhook (korak `08`)

Ali možeš testirati pojedine funkcije lokalno:

```python
# Test skripta (test_billing.py u korijenu)
import streamlit as st
from billing import smije_generirati, ima_aktivnu_pretplatu

# Postavi test user_id (ručno kreiran u Supabase Authentication → Users)
test_uid = "ovdje-uuid-test-usera"

print("Aktivna pretplata?", ima_aktivnu_pretplatu(test_uid))
print("Smije generirati?", smije_generirati(test_uid))
```

Pokreni s `streamlit run test_billing.py` (jer koristi `st.secrets`).

---

## TIPIČNI PROBLEMI

**"`No module named 'supabase'`"**
→ `pip install supabase` lokalno, i provjeri da je u `requirements.txt` na Streamlit Cloudu (deploy nakon pusha).

**"`KeyError: 'SUPABASE_URL'`"**
→ Nisi popunio `.streamlit/secrets.toml`. To radimo u koraku 09.

**"RLS blocks all queries — empty results"**
→ Nisi pozvao `_set_session_token()` nakon prijave. Auth token mora biti postavljen prije bilo kojeg query-ja.

**"Vidi se cijena u EUR ali korisnik plaća više"**
→ To je PDV (vidi `04_LEMON_SQUEEZY_SETUP.md`). Možeš podesiti u LS Tax behaviour: Inclusive da bude jasnije.

**"Nakon plaćanja, paywall se i dalje prikazuje"**
→ Webhook nije stigao do baze. Provjeri Edge Function logs (korak 08), provjeri `subscriptions` tablicu ručno.

---

## SLJEDEĆI KORAK

Otvori `06_KOD_AUTH.md` — refaktoriranje postojećeg `auth.py` da koristi Supabase.
