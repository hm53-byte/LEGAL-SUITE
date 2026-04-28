# -----------------------------------------------------------------------------
# STRANICA: Pokretnine — zalog na pokretnoj imovini
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, prikazi_dokument, zaglavlje_sastavljaca, audit_kwargs, napuni_primjerom
from generatori.pokretnine import generiraj_zalog_pokretnine, generiraj_zalog_vozila


def render_pokretnine():
    st.header("Pokretnine — zalog na pokretnoj imovini")
    st.caption("Pravni temelj: ZV čl. 297, FINA Upisnik (NN 121/05). Forma: javnobilježnička ovjera.")

    zaglavlje_sastavljaca()

    tip = st.selectbox(
        "Vrsta predmeta zaloga",
        [
            "Zalog na općoj pokretnini (oprema, strojevi, zalihe, umjetnine)",
            "Zalog na motornom vozilu",
        ],
        key="pkr_tip",
    )

    col1, col2 = st.columns(2)
    with col1:
        vjerovnik, _, _ = unos_stranke("VJEROVNIK", "pkr_vj")
    with col2:
        duznik, _, _ = unos_stranke("ZALOŽNI DUŽNIK (vlasnik)", "pkr_zd")

    if tip == "Zalog na općoj pokretnini (oprema, strojevi, zalihe, umjetnine)":
        napuni_primjerom('zalog_pokretnine', '')
        st.subheader("Predmet zaloga")
        opis = st.text_area(
            "Opis predmeta",
            placeholder="npr. CNC stroj XYZ Model A1, građevinska oprema (popis u Prilogu), zalihe robe u skladištu...",
            height=100, key="pkr_op_opis",
        )
        c1, c2 = st.columns(2)
        with c1:
            identifikacija = st.text_input("Identifikacija (serijski broj, oznaka)", key="pkr_op_id")
            procjena = st.number_input("Procijenjena vrijednost (EUR)", 0.0, step=100.0, key="pkr_op_pro")
        with c2:
            oblik = st.radio(
                "Oblik zaloga",
                ["bezdrzavinski", "drzavinski"],
                format_func=lambda x: "Bezdržavinski (predmet ostaje kod dužnika)" if x == "bezdrzavinski" else "Državinski (predaje se vjerovniku)",
                key="pkr_op_obl",
            )
            mjesto_pohrane = st.text_input("Mjesto pohrane (ako bezdržavinski)", key="pkr_op_mp", placeholder="npr. Skladište d.d., Vukovarska 1, Zagreb")

        st.subheader("Tražbina koja se osigurava")
        c1, c2 = st.columns(2)
        with c1:
            glavnica = st.number_input("Iznos tražbine (EUR)", 0.0, step=100.0, key="pkr_op_gl")
            kamata = st.text_input("Kamata", "zakonska zatezna kamata", key="pkr_op_kam")
            mjesto = st.text_input("Mjesto sklapanja", "Zagreb", key="pkr_op_mj")
        with c2:
            rok_d = st.text_input("Rok dospijeća tražbine", key="pkr_op_rd", placeholder="npr. 31.12.2027.")
            osnova = st.text_area("Osnova tražbine", placeholder="npr. Ugovor o zajmu od ...", height=80, key="pkr_op_os")

        if st.button("Generiraj sporazum", type="primary"):
            podaci = {
                'opis_predmeta': opis, 'identifikacija': identifikacija,
                'procjena_vrijednosti_eur': procjena,
                'iznos_trazbine_eur': glavnica, 'kamatna_stopa': kamata,
                'rok_dospijeca': rok_d, 'osnova_trazbine': osnova,
                'mjesto_pohrane': mjesto_pohrane, 'oblik_zaloga': oblik,
                'mjesto': mjesto,
            }
            doc = generiraj_zalog_pokretnine(vjerovnik, duznik, podaci)
            audit_input = {"vjerovnik_html": vjerovnik, "duznik_html": duznik, "podaci": podaci}
            prikazi_dokument(doc, "Zalog_pokretnine.docx", "Preuzmi sporazum",
                             **audit_kwargs("zalog_pokretnine", audit_input, "pokretnine"))

    elif tip == "Zalog na motornom vozilu":
        napuni_primjerom('zalog_vozila', '')
        st.subheader("Identifikacija vozila")
        c1, c2 = st.columns(2)
        with c1:
            marka = st.text_input("Marka", key="pkr_v_mar", placeholder="npr. Volkswagen")
            model = st.text_input("Model", key="pkr_v_mod", placeholder="npr. Golf")
            god_p = st.text_input("Godina proizvodnje", key="pkr_v_god")
            registracija = st.text_input("Registracijska oznaka", key="pkr_v_reg", placeholder="npr. ZG-1234-AB")
        with c2:
            broj_sasije = st.text_input("Broj šasije (VIN)", key="pkr_v_vin")
            broj_motora = st.text_input("Broj motora", key="pkr_v_mot")
            boja = st.text_input("Boja", key="pkr_v_boja")
            prijedeni_km = st.text_input("Prijeđeni kilometri", key="pkr_v_km")
        procjena_v = st.number_input("Procijenjena tržišna vrijednost (EUR)", 0.0, step=100.0, key="pkr_v_pro")

        st.subheader("Tražbina koja se osigurava")
        c1, c2 = st.columns(2)
        with c1:
            glavnica_v = st.number_input("Iznos tražbine (EUR)", 0.0, step=100.0, key="pkr_v_gl")
            kamata_v = st.text_input("Kamata", "zakonska zatezna kamata", key="pkr_v_kam")
            mjesto_v = st.text_input("Mjesto sklapanja", "Zagreb", key="pkr_v_mj")
        with c2:
            rok_v = st.text_input("Rok dospijeća tražbine", key="pkr_v_rd", placeholder="npr. 31.12.2027.")
            osnova_v = st.text_area("Osnova tražbine", placeholder="npr. Ugovor o zajmu od ...", height=80, key="pkr_v_os")

        if st.button("Generiraj sporazum", type="primary"):
            podaci = {
                'marka': marka, 'model': model, 'godina_proizvodnje': god_p,
                'registracijska_oznaka': registracija, 'broj_sasije_vin': broj_sasije,
                'broj_motora': broj_motora, 'boja': boja, 'prijedeni_km': prijedeni_km,
                'procjena_vrijednosti_eur': procjena_v,
                'iznos_trazbine_eur': glavnica_v, 'kamatna_stopa': kamata_v,
                'rok_dospijeca': rok_v, 'osnova_trazbine': osnova_v,
                'mjesto': mjesto_v,
            }
            doc = generiraj_zalog_vozila(vjerovnik, duznik, podaci)
            audit_input = {"vjerovnik_html": vjerovnik, "duznik_html": duznik, "podaci": podaci}
            prikazi_dokument(doc, "Zalog_vozila.docx", "Preuzmi sporazum",
                             **audit_kwargs("zalog_vozila", audit_input, "pokretnine"))
