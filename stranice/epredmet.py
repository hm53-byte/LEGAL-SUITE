# =============================================================================
# STRANICE/EPREDMET.PY - Pracenje sudskih predmeta (e-Predmet)
# =============================================================================
import streamlit as st
from api_epredmet import dohvati_sudove, pretrazi_predmet, OZNAKE_POSTUPAKA


def render_epredmet():
    """Stranica za pracenje sudskih predmeta putem e-Predmet API-ja."""
    st.header("\U0001f50d Pracenje sudskih predmeta")
    st.caption(
        "Pretrazite status sudskog predmeta putem sustava e-Predmet "
        "(Ministarstvo pravosuđa i uprave)."
    )

    st.info(
        "\U0001f4a1 **Kako pronaci broj predmeta?** "
        "Broj predmeta je na svakom sudskom pismenu u zaglavlju, "
        "npr. **P-123/2024** (parnicni), **Ovr-456/2023** (ovrsni), "
        "**K-78/2024** (kazneni)."
    )

    # Dohvati sudove
    with st.spinner("Ucitavam listu sudova..."):
        sudovi = dohvati_sudove()

    if isinstance(sudovi, dict) and "error" in sudovi:
        st.error(f"Greska pri dohvatu sudova: {sudovi['error']}")
        st.warning(
            "e-Predmet API mozda trenutno nije dostupan. "
            "Sustav se osvjezava jednom dnevno (01:00-05:00). Pokusajte kasnije."
        )
        return

    if not sudovi:
        st.warning("Nije moguce dohvatiti listu sudova. Pokusajte kasnije.")
        return

    # Forma za pretragu
    col1, col2 = st.columns([2, 1])

    with col1:
        # Selectbox za sud
        sud_opcije = {s.get("name", s.get("id", "")): s.get("id", "") for s in sudovi if isinstance(s, dict)}
        if not sud_opcije:
            # Fallback ako je format drugaciji
            sud_opcije = {str(s): i for i, s in enumerate(sudovi)}

        odabrani_sud = st.selectbox(
            "Sud",
            options=list(sud_opcije.keys()),
            key="ep_sud",
            help="Odaberite sud na kojem se vodi predmet",
        )

    with col2:
        oznaka = st.selectbox(
            "Vrsta postupka",
            options=list(OZNAKE_POSTUPAKA.keys()),
            format_func=lambda x: f"{x} - {OZNAKE_POSTUPAKA[x]}",
            key="ep_oznaka",
        )

    col3, col4 = st.columns(2)
    with col3:
        broj = st.text_input("Broj predmeta", placeholder="123", key="ep_broj", help="Redni broj predmeta")
    with col4:
        godina = st.text_input("Godina", placeholder="2024", key="ep_godina", max_chars=4)

    if st.button("\U0001f50d Pretrazi predmet", type="primary", use_container_width=True, key="ep_search"):
        if not broj or not godina:
            st.error("Unesite broj predmeta i godinu.")
            return

        broj_predmeta = f"{oznaka}-{broj}/{godina}"
        sud_id = sud_opcije.get(odabrani_sud, 0)

        with st.spinner(f"Pretrazujem predmet {broj_predmeta}..."):
            rezultat = pretrazi_predmet(broj_predmeta, sud_id)

        if isinstance(rezultat, dict) and "error" in rezultat:
            st.error(rezultat["error"])
            return

        if not rezultat:
            st.warning(f"Predmet {broj_predmeta} nije pronaden na odabranom sudu.")
            return

        # Prikazi rezultate
        st.markdown("---")
        st.markdown(f"### \U0001f4cb Predmet: {rezultat.get('caseNumber', broj_predmeta)}")

        # Osnovni podaci
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Sud:** {rezultat.get('court', {}).get('name', odabrani_sud)}")
            st.markdown(f"**Sudac:** {rezultat.get('judge', 'N/A')}")
        with col_b:
            status = rezultat.get("status", "N/A")
            status_boja = {"aktivan": "#059669", "zavrsen": "#DC2626", "u tijeku": "#D97706"}.get(
                status.lower() if isinstance(status, str) else "", "#475569"
            )
            st.markdown(
                f"**Status:** <span style='background:{status_boja};color:white;"
                f"padding:2px 8px;border-radius:4px;font-size:0.85rem;'>{status}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**Vrsta:** {rezultat.get('caseType', 'N/A')}")

        # Stranke
        stranke = rezultat.get("parties", [])
        if stranke:
            st.markdown("#### Stranke u postupku")
            for stranka in stranke:
                uloga = stranka.get("role", "")
                ime = stranka.get("name", "")
                st.markdown(f"- **{uloga}:** {ime}")

        # Dogadaji / Rociasta
        dogadaji = rezultat.get("events", [])
        if dogadaji:
            st.markdown("#### Tijek postupka")

            # Ponudi dodavanje u kalendar za buduce dogadaje
            from datetime import datetime as dt
            for d in dogadaji:
                datum_str = d.get("date", "")
                opis = d.get("description", "")
                tip = d.get("type", "")

                # Formatiraj datum
                datum_fmt = datum_str
                try:
                    datum_obj = dt.fromisoformat(datum_str.replace("Z", "+00:00"))
                    datum_fmt = datum_obj.strftime("%d.%m.%Y. %H:%M")
                    je_buduci = datum_obj > dt.now(datum_obj.tzinfo) if datum_obj.tzinfo else datum_obj > dt.now()
                except (ValueError, AttributeError):
                    je_buduci = False

                ikona = "\U0001f534" if je_buduci else "\u2705"
                st.markdown(f"{ikona} **{datum_fmt}** — {opis} ({tip})")

                # Gumb za dodavanje u kalendar (samo buduci dogadaji)
                if je_buduci:
                    if st.button(
                        f"\U0001f4c5 Dodaj u kalendar",
                        key=f"ep_cal_{datum_str}_{opis[:20]}",
                    ):
                        st.session_state.setdefault("_kalendar_eventi", []).append({
                            "naslov": f"Rociste: {broj_predmeta}",
                            "datum": datum_str,
                            "opis": f"{opis} - {odabrani_sud}",
                            "tip": "rociste",
                            "predmet": broj_predmeta,
                        })
                        st.success("Dodano u kalendar!")

        # Ponudi relevantne dokumente
        st.markdown("---")
        st.markdown("#### \U0001f4dd Trebate dokument za ovaj predmet?")
        col_x, col_y, col_z = st.columns(3)
        with col_x:
            if st.button("\U0001f4e3 Zalba", key="ep_doc_zalba"):
                st.session_state._active_module = "Zalbe"
                st.rerun()
        with col_y:
            if st.button("\U0001f4b0 Ovrha", key="ep_doc_ovrha"):
                st.session_state._active_module = "Ovrsno pravo"
                st.rerun()
        with col_z:
            if st.button("\u2696\ufe0f Tuzba", key="ep_doc_tuzba"):
                st.session_state._active_module = "Tuzbe"
                st.rerun()
