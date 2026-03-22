# =============================================================================
# STRANICE/EOGLASNA.PY - e-Oglasna ploca sudova
# =============================================================================
import streamlit as st
from datetime import datetime, timedelta
from api_eoglasna import pretrazi_objave, TIPOVI_OBJAVA, formatiraj_objavu, _DEMO_OBJAVE


def render_eoglasna():
    """Stranica za pretragu e-Oglasne ploce sudova."""
    # Primijeni pending vrijednosti iz brzih pretraga PRIJE renderiranja widgeta
    for _pk in ("_eo_pending_tip", "_eo_pending_tekst"):
        _target = _pk.replace("_eo_pending_", "eo_")
        if _pk in st.session_state:
            st.session_state[_target] = st.session_state.pop(_pk)

    st.header("Sudske objave (e-Oglasna ploca)")
    st.caption(
        "Pretrazite elektronicke oglasne ploce svih sudova u Hrvatskoj. "
        "Dostave pismena, drazbe, stecajni postupci, ovrhe."
    )

    # Filteri
    with st.expander("Filteri pretrage", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            tip = st.selectbox(
                "Tip objave",
                options=[""] + list(TIPOVI_OBJAVA.keys()),
                format_func=lambda x: TIPOVI_OBJAVA.get(x, "Sve objave") if x else "Sve objave",
                key="eo_tip",
            )
            tekst = st.text_input(
                "Pretraga po tekstu",
                placeholder="Unesite pojam za pretragu...",
                key="eo_tekst",
                max_chars=200,
            )
        with col2:
            datum_od = st.date_input(
                "Datum od",
                value=datetime.now() - timedelta(days=30),
                key="eo_datum_od",
            )
            datum_do = st.date_input(
                "Datum do",
                value=datetime.now(),
                key="eo_datum_do",
            )

        sud = st.text_input(
            "Sud (opcionalno)",
            placeholder="npr. Opcinski sud u Zagrebu",
            key="eo_sud",
            help="Unesite naziv suda ili ostavite prazno za sve sudove",
            max_chars=100,
        )

    if st.button("Pretrazi", type="primary", use_container_width=True, key="eo_search"):
        with st.spinner("Pretrazujem e-Oglasnu plocu..."):
            rezultat = pretrazi_objave(
                sud=sud,
                tip=tip,
                datum_od=datum_od.strftime("%Y-%m-%d") if datum_od else "",
                datum_do=datum_do.strftime("%Y-%m-%d") if datum_do else "",
                tekst=tekst,
            )

        je_demo = False
        if "error" in rezultat:
            # Fallback na demo podatke
            je_demo = True
            rezultat = _DEMO_OBJAVE
            st.warning(
                "e-Oglasna ploca API trenutno nije dostupan. "
                "Prikazujemo demonstracijske podatke. "
                "Za stvarne podatke posjetite: "
                "[e-oglasna.pravosudje.hr](https://e-oglasna.pravosudje.hr/)"
            )

        objave = rezultat.get("objave", [])
        ukupno = rezultat.get("ukupno", 0)

        if not objave:
            st.info("Nema rezultata za zadane kriterije.")
            return

        if je_demo:
            st.markdown(f"**Demonstracijski podaci** ({ukupno} primjera)")
        else:
            st.markdown(f"**Pronadeno:** {ukupno} objava")
        st.markdown("---")

        for objava in objave:
            fmt = formatiraj_objavu(objava)
            tip_boja = {
                "dostava": "#1E3A5F", "drazba": "#DC2626", "stecaj": "#D97706",
                "ovrha": "#059669", "oglas": "#475569",
            }.get(fmt["tip"], "#475569")

            st.markdown(
                f"<div style='background:#F8FAFC;padding:1rem;border-radius:8px;"
                f"border-left:4px solid {tip_boja};margin-bottom:0.8rem;'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
                f"<b>{fmt['naslov']}</b>"
                f"<span style='background:{tip_boja};color:white;padding:2px 8px;"
                f"border-radius:4px;font-size:0.7rem;'>{TIPOVI_OBJAVA.get(fmt['tip'], fmt['tip'])}</span>"
                f"</div>"
                f"<div style='color:#475569;font-size:0.85rem;margin-top:0.3rem;'>"
                f"{fmt['sud']} &middot; {fmt['datum']}"
                f"</div>"
                f"{'<div style=\"color:#0F172A;font-size:0.85rem;margin-top:0.5rem;\">' + fmt['sadrzaj'] + '</div>' if fmt['sadrzaj'] else ''}"
                f"</div>",
                unsafe_allow_html=True,
            )

            # Gumb za dodavanje u kalendar (za drazbe i rocista)
            if fmt["tip"] in ("drazba", "rociste") and not je_demo:
                if st.button(
                    f"Dodaj u kalendar",
                    key=f"eo_cal_{hash(fmt['naslov'] + fmt['datum'])}",
                ):
                    st.session_state.setdefault("_kalendar_eventi", []).append({
                        "naslov": fmt["naslov"],
                        "datum": fmt["datum"],
                        "opis": f"{fmt['sud']} - {fmt['sadrzaj'][:100]}",
                        "tip": fmt["tip"],
                    })
                    st.success("Dodano u kalendar!")

    # Brze pretrage
    st.markdown("---")
    st.markdown("##### Brze pretrage")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("Drazbe nekretnina", key="eo_brza_drazbe", use_container_width=True):
            st.session_state["_eo_pending_tip"] = "drazba"
            st.session_state["_eo_pending_tekst"] = "nekretnina"
            st.rerun()
    with col_b:
        if st.button("Stecajevi", key="eo_brza_stecaj", use_container_width=True):
            st.session_state["_eo_pending_tip"] = "stecaj"
            st.session_state["_eo_pending_tekst"] = ""
            st.rerun()
    with col_c:
        if st.button("Ovrhe", key="eo_brza_ovrhe", use_container_width=True):
            st.session_state["_eo_pending_tip"] = "ovrha"
            st.session_state["_eo_pending_tekst"] = ""
            st.rerun()
