# =============================================================================
# stranice/pravila.py — Uvjeti korištenja + Politika privatnosti (K3, 2026-04-27)
# =============================================================================
# Render-a tos.md i privacy_policy.md iz stranice/ direktorija u dvije st.tabs
# kartice. Markdown se ucitava pri svakom render-u (lazy load), pa izmjene u
# .md fajlovima odmah dolaze u app bez restart-a.
#
# Lokacija .md fajlova mora ostati u stranice/ jer __init__.py ne traje import
# za .md (samo za .py). Streamlit Cloud auto-deploya .md uz Python kod jer su
# u istom direktoriju i u repo-u.

import os
import streamlit as st


_DIR = os.path.dirname(os.path.abspath(__file__))
_TOS_PATH = os.path.join(_DIR, "tos.md")
_PRIVACY_PATH = os.path.join(_DIR, "privacy_policy.md")


def _ucitaj_md(path: str) -> str:
    """Ucitaj .md fajl. Vraca placeholder ako fajl nedostaje (graceful)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"_(Dokument privremeno nedostupan: {os.path.basename(path)})_"
    except Exception as e:
        return f"_(Greska pri ucitavanju: {e})_"


def render_pravila():
    """Glavna funkcija. Pozvana iz LEGAL-SUITE.py routing-a kad je
    `st.session_state._active_module == "Pravila i privatnost"`.
    """
    st.markdown("### Pravila i privatnost")

    # Disclaimer banner: dokumenti su nacrti
    st.markdown(
        "<div style='background:#FEF3C7;border-left:3px solid #D97706;"
        "padding:0.7rem 1rem;margin:0.4rem 0 1rem 0;border-radius:6px;font-size:0.82rem;"
        "color:#451A03;line-height:1.5;'>"
        "<b>Status:</b> nacrt v1.0 (2026-04-27). Dokumenti nisu pravnicki pregledani "
        "i moraju proci kroz odvjetnika prije aktivacije placenih pretplata. "
        "Aktivacija PRO tier-a je trenutno u test mode-u; ne primaju se stvarne uplate."
        "</div>",
        unsafe_allow_html=True,
    )

    tab_tos, tab_pp = st.tabs(["Uvjeti korištenja", "Politika privatnosti"])
    with tab_tos:
        st.markdown(_ucitaj_md(_TOS_PATH))
    with tab_pp:
        st.markdown(_ucitaj_md(_PRIVACY_PATH))
