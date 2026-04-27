# -----------------------------------------------------------------------------
# STRANICA: Posrednik u najmu (A-B-C paket)
# Jedno sučelje, tri stranke, dva ugovora
# -----------------------------------------------------------------------------
import streamlit as st
from datetime import date
from pomocne import unos_stranke, prikazi_dokument, _escape, audit_kwargs
from generatori.posrednik_najam import (
    generiraj_ugovor_najam_ab,
    generiraj_ugovor_upravljanje_bc,
)


def render_posrednik_najam():
    """Paketno generiranje ugovora za posrednika u najmu (A-B-C)."""
    st.header("Posrednik u najmu")
    st.markdown(
        "<div style='background:rgba(22,45,80,0.06);padding:1rem 1.2rem;"
        "border-radius:10px;margin-bottom:1.5rem;border-left:3px solid #162D50;'>"
        "<b style='color:#162D50;'>A-B-C model korporativnog smještaja</b><br>"
        "<span style='color:#3D4A5C;font-size:0.85rem;line-height:1.6;'>"
        "Ovaj modul generira <b>dva ugovora kao paket</b>:<br>"
        "1. <b>Ugovor o najmu stanova (A-B)</b> \u2014 stanodavac iznajmljuje posredniku<br>"
        "2. <b>Ugovor o upravljanju kapacitetom (B-C)</b> \u2014 posrednik pruža uslugu poslodavcu<br><br>"
        "Poslodavac (C) traži stanove za radnike i ugovara s posrednikom (B), "
        "bez izravnog kontakta sa stanodavcima (A).</span></div>",
        unsafe_allow_html=True,
    )

    # =========================================================================
    # 1. STRANKE
    # =========================================================================
    st.subheader("1. Ugovorne strane")

    tab_a, tab_b, tab_c = st.tabs([
        "A \u2014 Stanodavac (najmodavac)",
        "B \u2014 Posrednik (najmoprimac / davatelj)",
        "C \u2014 Poslodavac (naručitelj)",
    ])

    with tab_a:
        st.markdown(
            "<span style='color:#64748B;font-size:0.8rem;'>"
            "Vlasnik nekretnine koji daje stan u najam posredniku.</span>",
            unsafe_allow_html=True,
        )
        a_html, a_tip, a_valid = unos_stranke("NAJMODAVAC (A)", "pn_a")
        a_iban = st.text_input("IBAN (Najmodavac)", key="pn_a_iban",
                               placeholder="npr. HR1234567890123456789")

        # Dodaj IBAN u HTML ako postoji
        if a_iban and a_iban.strip():
            a_html = a_html + f"<br>IBAN: {_escape(a_iban)}"

    with tab_b:
        st.markdown(
            "<span style='color:#64748B;font-size:0.8rem;'>"
            "Posrednička tvrtka koja upravlja smještajem. "
            "Pojavljuje se u OBA ugovora.</span>",
            unsafe_allow_html=True,
        )
        b_html, b_tip, b_valid = unos_stranke("POSREDNIK (B)", "pn_b")
        b_iban = st.text_input("IBAN (Posrednik)", key="pn_b_iban",
                               placeholder="npr. HR1234567890123456789")
        if b_iban and b_iban.strip():
            b_html = b_html + f"<br>IBAN: {_escape(b_iban)}"

    with tab_c:
        st.markdown(
            "<span style='color:#64748B;font-size:0.8rem;'>"
            "Poslodavac čiji radnici trebaju smještaj. "
            "Ne kontaktira stanodavce izravno.</span>",
            unsafe_allow_html=True,
        )
        c_html, c_tip, c_valid = unos_stranke("NARUČITELJ (C)", "pn_c")
        c_iban = st.text_input("IBAN (Naručitelj)", key="pn_c_iban",
                               placeholder="npr. HR1234567890123456789")
        if c_iban and c_iban.strip():
            c_html = c_html + f"<br>IBAN: {_escape(c_iban)}"

    st.markdown("---")

    # =========================================================================
    # 2. NEKRETNINA (za A-B ugovor)
    # =========================================================================
    st.subheader("2. Podaci o nekretnini")
    st.markdown(
        "<span style='color:#64748B;font-size:0.8rem;'>"
        "Nekretnina koju stanodavac (A) daje u najam posredniku (B).</span>",
        unsafe_allow_html=True,
    )

    col_nek1, col_nek2 = st.columns(2)
    nek_adresa = col_nek1.text_input("Adresa nekretnine", key="pn_nek_adr",
                                     placeholder="npr. Vukovarska 15, Zagreb")
    nek_kc = col_nek2.text_input("Katastarska čestica", key="pn_nek_kc",
                                  placeholder="npr. k.č. 1234/1, k.o. Trnje")
    col_nek3, col_nek4 = st.columns(2)
    nek_povrsina = col_nek3.number_input("Površina (m\u00B2)", min_value=0.0,
                                         step=1.0, key="pn_nek_pov")
    nek_sobe = col_nek4.text_input("Broj soba / kreveta", key="pn_nek_sob",
                                    placeholder="npr. 3 sobe, 6 kreveta")
    nek_tereti = st.text_input(
        "Postojeći tereti na nekretnini (ako nema, ostavite 'nema')",
        value="nema", key="pn_nek_tereti",
    )

    st.markdown("---")

    # =========================================================================
    # 3. UVJETI A-B UGOVORA (Najam)
    # =========================================================================
    st.subheader("3. Uvjeti najma (A-B)")

    col_ab1, col_ab2 = st.columns(2)
    ab_mjesto = col_ab1.text_input("Mjesto sklapanja", value="Zagreb", key="pn_ab_mj")
    ab_datum = col_ab2.date_input("Datum sklapanja", key="pn_ab_dat")

    col_ab3, col_ab4 = st.columns(2)
    ab_trajanje = col_ab3.number_input("Trajanje najma (mjeseci)", min_value=1,
                                        value=36, step=1, key="pn_ab_traj")
    ab_pocetak = col_ab4.date_input("Datum početka najma", key="pn_ab_poc")

    col_ab5, col_ab6 = st.columns(2)
    ab_najamnina = col_ab5.number_input("Mjesečna najamnina (EUR)", min_value=0.0,
                                         step=50.0, key="pn_ab_najam")
    ab_najamnina_sl = col_ab6.text_input("Najamnina slovima", key="pn_ab_najam_sl",
                                          placeholder="npr. petsto eura")

    st.markdown("---")

    # =========================================================================
    # 4. UVJETI B-C UGOVORA (Upravljanje)
    # =========================================================================
    st.subheader("4. Uvjeti upravljanja kapacitetom (B-C)")

    col_bc1, col_bc2 = st.columns(2)
    bc_podrucje = col_bc1.text_input("Područje djelovanja", key="pn_bc_podr",
                                      placeholder="npr. grada Zagreba i okolice")
    bc_trajanje = col_bc2.number_input("Trajanje ugovora (mjeseci)", min_value=1,
                                        value=36, step=1, key="pn_bc_traj")

    col_bc3, col_bc4 = st.columns(2)
    bc_bazni = col_bc3.number_input("Bazni kapacitet (kreveta/jedinica)",
                                     min_value=1, value=10, step=1, key="pn_bc_bazni")
    bc_min = col_bc4.number_input("Minimalni kapacitet (prag raskida)",
                                   min_value=1, value=5, step=1, key="pn_bc_min")

    st.markdown("**Naknade**")
    col_bc5, col_bc6 = st.columns(2)
    bc_fiksna = col_bc5.number_input("Fiksna mjesečna naknada (EUR)", min_value=0.0,
                                      step=100.0, key="pn_bc_fiksna")
    bc_fiksna_sl = col_bc6.text_input("Fiksna naknada slovima", key="pn_bc_fiks_sl",
                                       placeholder="npr. tri tisuće eura")

    col_bc7, col_bc8 = st.columns(2)
    bc_var = col_bc7.number_input("Varijabilna naknada po noćenju/osobi (EUR)",
                                   min_value=0.0, step=1.0, key="pn_bc_var")
    bc_var_sl = col_bc8.text_input("Varijabilna naknada slovima", key="pn_bc_var_sl",
                                    placeholder="npr. petnaest eura")

    with st.expander("SLA penali i dodatni uvjeti", expanded=False):
        col_sla1, col_sla2 = st.columns(2)
        sla_hitni = col_sla1.number_input("Penal za propust hitnog popravka (EUR)",
                                           min_value=0.0, step=50.0, key="pn_sla_h")
        sla_checkin = col_sla2.number_input("Penal za propust check-in (EUR)",
                                             min_value=0.0, step=50.0, key="pn_sla_ci")
        col_sla3, col_sla4 = st.columns(2)
        kazna_kontakt = col_sla3.number_input(
            "Kazna za kontaktiranje stanodavaca (EUR)",
            min_value=0.0, step=500.0, key="pn_kazna"
        )
        max_mgmt_pct = col_sla4.number_input(
            "Max % operativne naknade Davatelja",
            min_value=0.0, max_value=100.0, step=1.0, value=0.0, key="pn_mgmt_pct",
            help="Ograničenje udjela management fee-a u ukupnoj naknadi. 0 = bez ograničenja.",
        )
        sud_mjesto = st.text_input("Sud nadležan za sporove (B-C)", key="pn_sud",
                                    placeholder="npr. Zagrebu")

    # =========================================================================
    # 5. SPECIFIKACIJA KAPACITETA (Prilog 1 za B-C)
    # =========================================================================
    with st.expander("Specifikacija smještajnog kapaciteta (Prilog 1)", expanded=False):
        st.markdown(
            "<span style='color:#64748B;font-size:0.8rem;'>"
            "Popis svih nekretnina u portfelju posrednika za ovog naručitelja.</span>",
            unsafe_allow_html=True,
        )
        spec_count_key = "pn_spec_count"
        if spec_count_key not in st.session_state:
            st.session_state[spec_count_key] = 1

        spec_rows = []
        for i in range(st.session_state[spec_count_key]):
            st.markdown(f"**Nekretnina {i+1}**")
            sc1, sc2 = st.columns(2)
            s_adr = sc1.text_input(f"Adresa", key=f"pn_sp_adr_{i}",
                                    placeholder="Adresa nekretnine")
            s_sobe = sc2.text_input(f"Br. soba", key=f"pn_sp_sob_{i}")
            sc3, sc4 = st.columns(2)
            s_kreveti = sc3.text_input(f"Br. kreveta", key=f"pn_sp_kre_{i}")
            s_opr = sc4.text_input(f"Opremljenost", key=f"pn_sp_opr_{i}",
                                    placeholder="npr. potpuno opremljen")
            s_nap = st.text_input(f"Napomena", key=f"pn_sp_nap_{i}",
                                   placeholder="opcionalno")
            if s_adr and s_adr.strip():
                spec_rows.append({
                    'adresa': s_adr, 'sobe': s_sobe, 'kreveti': s_kreveti,
                    'opremljenost': s_opr, 'napomena': s_nap,
                })
            if i < st.session_state[spec_count_key] - 1:
                st.markdown("---")

        col_sp_add, col_sp_rem = st.columns(2)
        with col_sp_add:
            if st.session_state[spec_count_key] < 20:
                if st.button("+ Dodaj nekretninu", key="pn_sp_add"):
                    st.session_state[spec_count_key] += 1
                    st.rerun()
        with col_sp_rem:
            if st.session_state[spec_count_key] > 1:
                if st.button("- Ukloni zadnju", key="pn_sp_rem"):
                    st.session_state[spec_count_key] -= 1
                    st.rerun()

    st.markdown("---")

    # =========================================================================
    # 6. GENERIRANJE PAKETA
    # =========================================================================
    if st.button("Generiraj paket ugovora", type="primary", use_container_width=True):

        # --- A-B Ugovor ---
        nekretnina = {
            'adresa': nek_adresa,
            'katastarska_cestica': nek_kc,
            'povrsina': nek_povrsina,
            'sobe_kreveti': nek_sobe,
        }
        podaci_ab = {
            'datum': ab_datum,
            'mjesto': ab_mjesto,
            'trajanje_mjeseci': ab_trajanje,
            'datum_pocetka': ab_pocetak,
            'najamnina': ab_najamnina,
            'najamnina_slovima': ab_najamnina_sl,
            'tereti': nek_tereti,
        }
        doc_ab = generiraj_ugovor_najam_ab(a_html, b_html, nekretnina, podaci_ab)

        # --- B-C Ugovor ---
        kapacitet = {
            'bazni_kapacitet': bc_bazni,
            'minimalni_kapacitet': bc_min,
            'specifikacija': spec_rows,
        }
        podaci_bc = {
            'datum': ab_datum,
            'mjesto': ab_mjesto,
            'podrucje_djelovanja': bc_podrucje,
            'trajanje_mjeseci': bc_trajanje,
            'datum_pocetka': ab_pocetak,
            'fiksna_naknada': bc_fiksna,
            'fiksna_slovima': bc_fiksna_sl,
            'varijabilna_naknada': bc_var,
            'varijabilna_slovima': bc_var_sl,
            'sla_hitni': sla_hitni,
            'sla_checkin': sla_checkin,
            'kazna_kontakt': kazna_kontakt,
            'max_mgmt_fee_pct': max_mgmt_pct if max_mgmt_pct > 0 else '',
            'sud_mjesto': sud_mjesto,
        }
        doc_bc = generiraj_ugovor_upravljanje_bc(b_html, c_html, kapacitet, podaci_bc)

        # --- Prikaz oba ugovora ---
        st.markdown(
            "<div style='background:linear-gradient(135deg,#059669 0%,#047857 100%);color:white;"
            "padding:1rem 1.5rem;border-radius:10px;margin:1rem 0;text-align:center;'>"
            "<span style='font-size:1.3rem;font-weight:700;'>"
            "\u2705 Paket ugovora je spreman!</span><br>"
            "<span style='font-size:0.85rem;opacity:0.9;'>"
            "Oba ugovora su generirana. Preuzmite ih zasebno ispod.</span>"
            "</div>",
            unsafe_allow_html=True,
        )

        tab_dok_ab, tab_dok_bc = st.tabs([
            "Ugovor o najmu (A-B)",
            "Ugovor o upravljanju (B-C)",
        ])

        audit_input_ab = {
            "stanodavac_html": a_html,
            "posrednik_html": b_html,
            "nekretnina": nekretnina,
            "podaci": podaci_ab,
        }
        audit_input_bc = {
            "posrednik_html": b_html,
            "narucitelj_html": c_html,
            "kapacitet": kapacitet,
            "podaci": podaci_bc,
        }

        with tab_dok_ab:
            prikazi_dokument(doc_ab, "Ugovor_o_najmu_AB.docx", "Preuzmi ugovor A-B",
                             **audit_kwargs("ugovor_najam_ab", audit_input_ab, "posrednik_najam"))

        with tab_dok_bc:
            prikazi_dokument(doc_bc, "Ugovor_o_upravljanju_BC.docx", "Preuzmi ugovor B-C",
                             **audit_kwargs("ugovor_upravljanje_bc", audit_input_bc, "posrednik_najam"))
