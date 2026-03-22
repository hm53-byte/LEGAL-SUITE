# =============================================================================
# STRANICE/KALENDAR.PY - Kalendar s podsjetnicima za rocista
# Persistencija: JSON datoteka (_data/kalendar.json)
# =============================================================================
import streamlit as st
from datetime import datetime, timedelta
import json
import os
import html as _html_module
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def _esc(text):
    """Escape HTML entiteta u korisnickom unosu."""
    return _html_module.escape(str(text)) if text else ""

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "_data")
_KALENDAR_PATH = os.path.join(_DATA_DIR, "kalendar.json")


def _ucitaj_iz_datoteke():
    """Ucitaj eventi iz JSON datoteke."""
    try:
        if os.path.exists(_KALENDAR_PATH):
            with open(_KALENDAR_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError, OSError):
        pass
    return []


def _spremi_u_datoteku(eventi):
    """Spremi eventi u JSON datoteku."""
    try:
        os.makedirs(_DATA_DIR, exist_ok=True)
        with open(_KALENDAR_PATH, "w", encoding="utf-8") as f:
            json.dump(eventi, f, ensure_ascii=False, indent=2)
    except (IOError, OSError):
        pass  # Tiho zanemari ako ne moze pisati (npr. read-only filesystem)


def _dohvati_eventi():
    """Dohvati listu eventi - sinkroniziraj session_state i datoteku."""
    if "_kalendar_eventi" not in st.session_state:
        # Prvo ucitavanje - pokusaj iz datoteke
        st.session_state._kalendar_eventi = _ucitaj_iz_datoteke()
    return st.session_state.get("_kalendar_eventi", [])


def _spremi_eventi(eventi):
    """Spremi listu eventi u session_state i datoteku."""
    st.session_state._kalendar_eventi = eventi
    _spremi_u_datoteku(eventi)


def _posalji_podsjetnik(email, event):
    """Posalji email podsjetnik za event."""
    try:
        try:
            smtp_host = st.secrets.get("smtp_host", "")
            smtp_port = int(st.secrets.get("smtp_port", "587"))
            smtp_user = st.secrets.get("smtp_user", "")
            smtp_pass = st.secrets.get("smtp_pass", "")
        except Exception:
            return False, "SMTP nije konfiguriran."

        if not smtp_host or not smtp_user:
            return False, "SMTP nije konfiguriran u Streamlit Secrets."

        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = email
        msg["Subject"] = f"Podsjetnik: {event['naslov']}"

        body = (
            f"Podsjetnik za dogadaj:\n\n"
            f"Naslov: {event['naslov']}\n"
            f"Datum: {event.get('datum', 'N/A')}\n"
            f"Opis: {event.get('opis', '')}\n"
            f"Predmet: {event.get('predmet', '')}\n\n"
            f"---\n"
            f"LegalTech Suite Pro - Automatski podsjetnik"
        )
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        return True, "Podsjetnik poslan!"
    except Exception as e:
        return False, str(e)


def _provjeri_podsjetnike():
    """Provjeri je li vrijeme za poslati podsjetnik za neki event."""
    eventi = _dohvati_eventi()
    sada = datetime.now()
    promjena = False

    for event in eventi:
        if event.get("_podsjetnik_poslan"):
            continue

        podsjetnik_email = event.get("podsjetnik_email")
        podsjetnik_sati = event.get("podsjetnik_sati", 24)

        if not podsjetnik_email:
            continue

        try:
            datum_str = event.get("datum", "")
            if "T" in datum_str:
                datum_obj = datetime.fromisoformat(datum_str.replace("Z", "+00:00")).replace(tzinfo=None)
            else:
                datum_obj = datetime.strptime(datum_str.rstrip("."), "%d.%m.%Y")

            razlika = datum_obj - sada
            if timedelta(0) < razlika <= timedelta(hours=podsjetnik_sati):
                ok, msg = _posalji_podsjetnik(podsjetnik_email, event)
                if ok:
                    event["_podsjetnik_poslan"] = True
                    promjena = True
        except (ValueError, TypeError):
            pass

    if promjena:
        _spremi_eventi(eventi)


def render_kalendar():
    """Stranica za kalendar s dogadajima i podsjetnicima."""
    st.header("Kalendar")
    st.caption("Pratite rocista, rokove i dogadaje. Postavite podsjetnik putem emaila.")

    # Provjeri podsjetnike pri svakom ucitavanju
    _provjeri_podsjetnike()

    eventi = _dohvati_eventi()

    # Success poruka koja prezivi rerun
    if st.session_state.get("_kalendar_success"):
        st.success(st.session_state._kalendar_success)
        del st.session_state._kalendar_success

    # Tab: pregled i dodavanje
    tab_pregled, tab_dodaj = st.tabs(["Moji dogadaji", "Dodaj dogadaj"])

    with tab_pregled:
        if not eventi:
            st.info(
                "Nemate spremljenih dogadaja. Dodajte dogadaj rucno ili "
                "pretrazite predmet na e-Predmetu i dodajte rociste u kalendar."
            )
        else:
            # Sortiraj po datumu
            sada = datetime.now()

            for i, event in enumerate(eventi):
                naslov = event.get("naslov", "Bez naslova")
                datum_str = event.get("datum", "")
                opis = event.get("opis", "")
                tip = event.get("tip", "ostalo")
                predmet = event.get("predmet", "")

                # Pokusaj parsirati datum
                je_prosao = False
                datum_fmt = datum_str
                try:
                    if "T" in datum_str:
                        datum_obj = datetime.fromisoformat(datum_str.replace("Z", "+00:00")).replace(tzinfo=None)
                    elif "." in datum_str and len(datum_str) >= 8:
                        datum_obj = datetime.strptime(datum_str.rstrip("."), "%d.%m.%Y")
                    else:
                        datum_obj = None

                    if datum_obj:
                        datum_fmt = datum_obj.strftime("%d.%m.%Y.")
                        je_prosao = datum_obj < sada
                        dana_do = (datum_obj - sada).days
                except (ValueError, TypeError):
                    datum_obj = None
                    dana_do = None

                # Boja po tipu
                tip_boje = {
                    "rociste": "#DC2626", "rok": "#D97706", "drazba": "#059669", "ostalo": "#1E3A5F",
                }
                boja = tip_boje.get(tip, "#475569")
                opacity = "0.5" if je_prosao else "1"

                st.markdown(
                    f"<div style='background:#F8FAFC;padding:1rem;border-radius:8px;"
                    f"border-left:4px solid {boja};margin-bottom:0.6rem;opacity:{opacity};'>"
                    f"<div style='display:flex;justify-content:space-between;'>"
                    f"<b>{_esc(naslov)}</b>"
                    f"<span style='font-size:0.85rem;color:{boja};font-weight:600;'>"
                    f"{_esc(datum_fmt)}"
                    f"{'  (' + str(dana_do) + ' dana)' if dana_do is not None and dana_do > 0 else ''}"
                    f"{'  (PROSLO)' if je_prosao else ''}"
                    f"</span></div>"
                    f"{'<div style=\"color:#475569;font-size:0.85rem;margin-top:0.3rem;\">' + _esc(opis) + '</div>' if opis else ''}"
                    f"{'<div style=\"color:#94A3B8;font-size:0.8rem;margin-top:0.2rem;\">Predmet: ' + _esc(predmet) + '</div>' if predmet else ''}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                # Podsjetnik i brisanje
                col_pod, col_brisi = st.columns([3, 1])
                with col_pod:
                    if not je_prosao and not event.get("podsjetnik_email"):
                        pod_email = st.text_input(
                            "Email za podsjetnik",
                            placeholder="vas@email.com",
                            key=f"kal_email_{i}",
                            label_visibility="collapsed",
                            max_chars=100,
                        )
                        pod_sati = st.selectbox(
                            "Koliko sati prije",
                            options=[1, 2, 6, 12, 24, 48, 72],
                            format_func=lambda x: f"{x}h prije" if x < 24 else f"{x // 24} dan(a) prije",
                            key=f"kal_sati_{i}",
                            label_visibility="collapsed",
                        )
                        if st.button("Postavi podsjetnik", key=f"kal_pod_{i}"):
                            if pod_email and "@" in pod_email:
                                event["podsjetnik_email"] = pod_email
                                event["podsjetnik_sati"] = pod_sati
                                _spremi_eventi(eventi)
                                st.success(f"Podsjetnik postavljen ({pod_sati}h prije) na {pod_email}")
                                st.rerun()
                            else:
                                st.error("Unesite valjanu email adresu.")
                    elif event.get("podsjetnik_email"):
                        st.markdown(
                            f"Podsjetnik: **{event['podsjetnik_email']}** "
                            f"({event.get('podsjetnik_sati', 24)}h prije)"
                        )

                with col_brisi:
                    if st.button("Ukloni", key=f"kal_del_{i}"):
                        eventi.pop(i)
                        _spremi_eventi(eventi)
                        st.rerun()

    with tab_dodaj:
        st.markdown("#### Rucno dodavanje dogadaja")

        with st.form("novi_event_form"):
            naslov = st.text_input("Naslov", placeholder="npr. Rociste - P-123/2024", max_chars=200)
            datum = st.date_input("Datum", value=datetime.now() + timedelta(days=7))
            from datetime import time as _time
            vrijeme = st.time_input("Vrijeme (09:00 ako nema)", value=_time(9, 0), key="kal_vrijeme")
            opis = st.text_area("Opis (opcionalno)", placeholder="Dodatne biljeske...", max_chars=500)
            tip = st.selectbox("Tip", options=["rociste", "rok", "drazba", "ostalo"],
                               format_func=lambda x: {"rociste": "Rociste", "rok": "Rok", "drazba": "Drazba", "ostalo": "Ostalo"}[x])
            predmet = st.text_input("Broj predmeta (opcionalno)", placeholder="P-123/2024", max_chars=50)
            submitted = st.form_submit_button("Dodaj u kalendar", type="primary", use_container_width=True)

            if submitted:
                if not naslov:
                    st.error("Unesite naslov dogadaja.")
                else:
                    datum_str = datum.strftime("%d.%m.%Y.")
                    datum_iso = datetime.combine(datum, vrijeme).isoformat()

                    # Duplikat detekcija - sprijecava uzastopno dodavanje istog dogadaja
                    duplikat = any(
                        e.get("naslov") == naslov and e.get("datum") == datum_iso
                        for e in eventi
                    )
                    if duplikat:
                        st.warning(f"Dogadaj '{naslov}' za {datum_str} vec postoji u kalendaru.")
                    else:
                        novi_event = {
                            "naslov": naslov,
                            "datum": datum_iso,
                            "datum_fmt": datum_str,
                            "opis": opis,
                            "tip": tip,
                            "predmet": predmet,
                        }
                        eventi.append(novi_event)
                        _spremi_eventi(eventi)
                        st.session_state._kalendar_success = f"Dogadaj '{naslov}' dodan za {datum_str}!"
                        st.rerun()

    # SMTP konfiguracija info
    with st.expander("Konfiguracija email podsjetnika"):
        try:
            smtp_ok = bool(st.secrets.get("smtp_host", ""))
        except Exception:
            smtp_ok = False
        if smtp_ok:
            st.success("SMTP je konfiguriran. Email podsjetnici ce se slati automatski.")
        else:
            st.warning(
                "Za slanje email podsjetnika, dodajte SMTP podatke u Streamlit Secrets:\n\n"
                "```toml\n"
                "smtp_host = \"smtp.gmail.com\"\n"
                "smtp_port = \"587\"\n"
                "smtp_user = \"vas@gmail.com\"\n"
                "smtp_pass = \"vasa_app_password\"\n"
                "```\n\n"
                "Za Gmail: koristite [App Password](https://support.google.com/accounts/answer/185833)."
            )
