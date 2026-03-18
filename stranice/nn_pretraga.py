# =============================================================================
# STRANICE/NN_PRETRAGA.PY - Pretraga Narodnih novina / baza zakona
# =============================================================================
import streamlit as st
from api_nn import KLJUCNI_ZAKONI, pretrazi_nn, generiraj_nn_link


def render_nn_pretraga():
    """Stranica za pretragu Narodnih novina i bazu kljucnih zakona."""
    # Primijeni pending upit iz popularnih gumba PRIJE renderiranja widgeta
    if "_nn_pending" in st.session_state:
        st.session_state["nn_upit"] = st.session_state.pop("_nn_pending")

    st.header("Propisi i zakoni")
    st.caption("Pretrazite Narodne novine i pristupite kljucnim hrvatskim zakonima.")

    tab_baza, tab_pretraga = st.tabs([
        "Baza kljucnih zakona",
        "Pretraga Narodnih novina",
    ])

    with tab_baza:
        st.markdown(
            "Brzi pristup najvaznijim zakonima koji se koriste u pravnim dokumentima. "
            "Kliknite na link za otvaranje teksta na Narodnim novinama."
        )

        _KATEGORIJE = {
            "Gradansko i obvezno pravo": ["ZOO", "ZPP"],
            "Trgovacko pravo": ["ZTD"],
            "Radno pravo": ["ZR"],
            "Obiteljsko pravo": ["ObZ"],
            "Upravno pravo": ["ZUP", "ZUS", "ZPPI"],
            "Kazneno pravo": ["KZ"],
            "Ovrsno i stecajno pravo": ["OZ", "SZ"],
            "Zemljisno pravo": ["ZZK"],
            "Zastita potrosaca": ["ZZP"],
        }

        for kategorija, kratice in _KATEGORIJE.items():
            st.markdown(f"##### {kategorija}")
            for kratica in kratice:
                zakon = KLJUCNI_ZAKONI.get(kratica, {})
                if zakon:
                    st.markdown(
                        f"<div style='background:#F8FAFC;padding:0.7rem 1rem;border-radius:8px;"
                        f"border-left:3px solid #1E3A5F;margin-bottom:0.4rem;'>"
                        f"<b>{kratica}</b> &mdash; {zakon['naziv']}<br>"
                        f"<span style='color:#94A3B8;font-size:0.8rem;'>{zakon['nn']}</span><br>"
                        f"<a href='{zakon['url']}' target='_blank' style='font-size:0.85rem;'>"
                        f"Otvori na Narodnim novinama &rarr;</a>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

    with tab_pretraga:
        st.markdown("Pretrazite Narodne novine po kljucnim rijecima.")

        upit = st.text_input(
            "Pojam za pretragu",
            placeholder="npr. zastara, naknada stete, otkaz ugovora o radu...",
            key="nn_upit",
        )

        if st.button("Pretrazi", type="primary", use_container_width=True, key="nn_search"):
            if not upit:
                st.error("Unesite pojam za pretragu.")
            else:
                with st.spinner("Pretrazujem Narodne novine..."):
                    rezultat = pretrazi_nn(upit)

                if "error" in rezultat:
                    st.warning(
                        f"Pretraga nije uspjela: {rezultat['error']}\n\n"
                        f"Pokusajte izravno na: [narodne-novine.nn.hr](https://narodne-novine.nn.hr/pretraga)"
                    )
                else:
                    rezultati = rezultat.get("rezultati", [])
                    if not rezultati:
                        st.info("Nema rezultata za zadani upit.")
                    else:
                        st.markdown(f"**Pronadeno:** {len(rezultati)} rezultata")
                        for r in rezultati:
                            st.markdown(
                                f"<div style='background:#F8FAFC;padding:0.7rem 1rem;border-radius:8px;"
                                f"margin-bottom:0.4rem;'>"
                                f"<a href='{r['url']}' target='_blank'><b>{r['naslov']}</b></a><br>"
                                f"<span style='color:#94A3B8;font-size:0.8rem;'>{r.get('nn_broj', '')}</span>"
                                f"</div>",
                                unsafe_allow_html=True,
                            )

        # Popularni upiti
        st.markdown("---")
        st.markdown("##### Popularni upiti")
        _popularni = [
            "zastara potrazivanja", "naknada stete", "otkaz ugovora o radu",
            "ugovor o kupoprodaji nekretnine", "ovrha na placi",
            "zalba na rjesenje", "zastita potrosaca reklamacija",
        ]
        cols = st.columns(3)
        for i, p in enumerate(_popularni):
            with cols[i % 3]:
                if st.button(p, key=f"nn_pop_{i}", use_container_width=True):
                    st.session_state["_nn_pending"] = p
                    st.rerun()
