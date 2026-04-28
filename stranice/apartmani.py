# -----------------------------------------------------------------------------
# STRANICA: Apartmani — iznajmljivanje, MTU, kategorizacija
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import unos_stranke, prikazi_dokument, zaglavlje_sastavljaca, audit_kwargs, napuni_primjerom
from generatori.apartmani import (
    generiraj_suglasnost_obitelji,
    generiraj_suglasnost_suvlasnika,
    generiraj_zahtjev_mtu,
    generiraj_zahtjev_kategorizacija,
)


def _polja_nekretnine(prefix):
    st.subheader("Nekretnina")
    col1, col2 = st.columns(2)
    with col1:
        adresa = st.text_input("Adresa nekretnine", key=f"{prefix}_adr", placeholder="npr. Riječka 1, 51000 Rijeka")
        kat_opis = st.text_input("Opis (kat / jedinica)", key=f"{prefix}_kat", placeholder="npr. 1. kat, stan br. 4")
        povrsina = st.text_input("Površina (m²)", key=f"{prefix}_pov", placeholder="npr. 65")
    with col2:
        ko = st.text_input("Katastarska općina (k.o.)", key=f"{prefix}_ko", placeholder="opcionalno")
        cestica = st.text_input("Broj čestice (k.č.br.)", key=f"{prefix}_ces", placeholder="opcionalno")
        ulozak = st.text_input("Broj zk. uloška", key=f"{prefix}_ulo", placeholder="opcionalno")

    return {
        'adresa': adresa,
        'kat_opis': kat_opis,
        'povrsina_m2': povrsina,
        'ko': ko,
        'cestica': cestica,
        'ulozak': ulozak,
    }


def render_apartmani():
    st.header("Apartmani — iznajmljivanje turistima")
    st.caption(
        "Pravni temelj: Zakon o ugostiteljskoj djelatnosti (NN 85/15), "
        "Pravilnici NN 9/16 (MTU) i NN 56/16 (kategorizacija)."
    )

    zaglavlje_sastavljaca()

    tip = st.selectbox(
        "Vrsta dokumenta",
        [
            "Suglasnost vlasnika članu obitelji za iznajmljivanje",
            "Suglasnost suvlasnika nekretnine",
            "Zahtjev za rješenje o MTU (minimalni tehnički uvjeti)",
            "Zahtjev za kategorizaciju apartmana",
        ],
        key="ap_tip",
    )

    if tip == "Suglasnost vlasnika članu obitelji za iznajmljivanje":
        napuni_primjerom('suglasnost_obitelji', '')
        col1, col2 = st.columns(2)
        with col1:
            vlasnik, _, _ = unos_stranke("VLASNIK NEKRETNINE", "ap_so_v")
        with col2:
            korisnik, _, _ = unos_stranke("KORISNIK SUGLASNOSTI", "ap_so_k")

        podaci = _polja_nekretnine("ap_so_n")

        col_a, col_b = st.columns(2)
        with col_a:
            podaci['srodstvo'] = st.text_input(
                "Srodstvo s vlasnikom",
                "sin/kći", key="ap_so_sr",
                help="npr. sin, kći, bračni drug, roditelj, brat/sestra",
            )
            podaci['mjesto'] = st.text_input("Mjesto izdavanja", "Zagreb", key="ap_so_mj")
        with col_b:
            podaci['rok_vazenja'] = st.text_input(
                "Rok važenja",
                "do opoziva ove suglasnosti u pisanom obliku",
                key="ap_so_rok",
            )
            podaci['broj_smjestajnih_jedinica'] = st.text_input(
                "Broj smještajnih jedinica",
                key="ap_so_bj", placeholder="opcionalno",
            )

        if st.button("Generiraj suglasnost", type="primary"):
            doc = generiraj_suglasnost_obitelji(vlasnik, korisnik, podaci)
            audit_input = {"vlasnik_html": vlasnik, "korisnik_html": korisnik, "podaci": podaci}
            prikazi_dokument(doc, "Suglasnost_obitelji_apartmani.docx", "Preuzmi suglasnost",
                             **audit_kwargs("suglasnost_obitelji", audit_input, "apartmani"))

    elif tip == "Suglasnost suvlasnika nekretnine":
        napuni_primjerom('suglasnost_suvlasnika', '')
        st.markdown(
            "Unesite suvlasnike koji **daju** suglasnost (kao slobodan tekst — svaki suvlasnik s OIB-om i adresom). "
            "Predlagatelj je suvlasnik koji ishođuje rješenja u svoje ime."
        )
        suvlasnici_txt = st.text_area(
            "Suvlasnici (potpisnici suglasnosti)",
            placeholder="IVAN HORVAT, OIB: 12345678901, Riječka 1, 51000 Rijeka\n\nMARIJA HORVAT, OIB: 98765432109, Riječka 1, 51000 Rijeka",
            height=120,
            key="ap_ss_su",
        )
        suvlasnici_html = "<br>".join(
            line.strip() for line in suvlasnici_txt.split("\n") if line.strip()
        )

        st.markdown("**Predlagatelj** (suvlasnik koji ishođuje MTU/kategorizaciju):")
        predlagatelj, _, _ = unos_stranke("PREDLAGATELJ", "ap_ss_pr")

        podaci = _polja_nekretnine("ap_ss_n")
        podaci['mjesto'] = st.text_input("Mjesto izdavanja", "Zagreb", key="ap_ss_mj")

        if st.button("Generiraj suglasnost", type="primary"):
            doc = generiraj_suglasnost_suvlasnika(suvlasnici_html, predlagatelj, podaci)
            audit_input = {"suvlasnici_html": suvlasnici_html, "predlagatelj_html": predlagatelj, "podaci": podaci}
            prikazi_dokument(doc, "Suglasnost_suvlasnika.docx", "Preuzmi suglasnost",
                             **audit_kwargs("suglasnost_suvlasnika", audit_input, "apartmani"))

    elif tip == "Zahtjev za rješenje o MTU (minimalni tehnički uvjeti)":
        napuni_primjerom('zahtjev_mtu', '')
        podnositelj, _, _ = unos_stranke("PODNOSITELJ ZAHTJEVA", "ap_mtu_pn")

        podaci = _polja_nekretnine("ap_mtu_n")

        col_a, col_b = st.columns(2)
        with col_a:
            podaci['vrsta_objekta'] = st.selectbox(
                "Vrsta objekta",
                ["Apartman", "Soba u domaćinstvu", "Studio apartman", "Kuća za odmor", "Kamp u domaćinstvu"],
                key="ap_mtu_vo",
            )
            podaci['broj_smjestajnih_jedinica'] = st.text_input("Broj smještajnih jedinica", "1", key="ap_mtu_bj")
            podaci['broj_kreveta'] = st.text_input("Broj kreveta", key="ap_mtu_bk", placeholder="npr. 4")
        with col_b:
            podaci['zupanija'] = st.text_input("Županija", key="ap_mtu_zu", placeholder="npr. Primorsko-goranska")
            podaci['nadlezno_tijelo'] = st.text_input(
                "Nadležno tijelo (ako specifično)",
                key="ap_mtu_nt",
                placeholder="ostavi prazno za default",
            )
            podaci['mjesto'] = st.text_input("Mjesto", "Rijeka", key="ap_mtu_mj")

        if st.button("Generiraj zahtjev", type="primary"):
            doc = generiraj_zahtjev_mtu(podnositelj, podaci)
            audit_input = {"podnositelj_html": podnositelj, "podaci": podaci}
            prikazi_dokument(doc, "Zahtjev_MTU.docx", "Preuzmi zahtjev",
                             **audit_kwargs("zahtjev_mtu", audit_input, "apartmani"))

    elif tip == "Zahtjev za kategorizaciju apartmana":
        napuni_primjerom('zahtjev_kategorizacija', '')
        podnositelj, _, _ = unos_stranke("PODNOSITELJ ZAHTJEVA", "ap_kat_pn")

        podaci = _polja_nekretnine("ap_kat_n")

        col_a, col_b = st.columns(2)
        with col_a:
            podaci['vrsta_objekta'] = st.selectbox(
                "Vrsta objekta",
                ["Apartman", "Soba u domaćinstvu", "Studio apartman", "Kuća za odmor"],
                key="ap_kat_vo",
            )
            podaci['zatrazena_kategorija'] = st.selectbox(
                "Zatražena kategorija (zvjezdice)",
                ["", "2★", "3★", "4★", "5★"],
                key="ap_kat_kat",
                help="Konačnu kategoriju utvrđuje povjerenstvo. Ovaj unos je prijedlog.",
            )
            podaci['broj_smjestajnih_jedinica'] = st.text_input("Broj smještajnih jedinica", "1", key="ap_kat_bj")
            podaci['broj_kreveta'] = st.text_input("Broj kreveta", key="ap_kat_bk")
        with col_b:
            podaci['mtu_klasa'] = st.text_input("Broj rješenja o MTU (KLASA)", key="ap_kat_mk", placeholder="opcionalno ako MTU postoji")
            podaci['mtu_datum'] = st.text_input("Datum rješenja o MTU", key="ap_kat_md", placeholder="dd.mm.yyyy.")
            podaci['zupanija'] = st.text_input("Županija", key="ap_kat_zu", placeholder="npr. Primorsko-goranska")
            podaci['mjesto'] = st.text_input("Mjesto", "Rijeka", key="ap_kat_mj")

        podaci['opremljenost'] = st.text_area(
            "Opis opremljenosti i sadržaja",
            placeholder="kuhinja s mikrovalnom i posuđem, kupaonica s tušem, klima, TV, WiFi, terasa s pogledom na more, parking",
            height=100, key="ap_kat_op",
        )
        podaci['nadlezno_tijelo'] = st.text_input(
            "Nadležno tijelo (ako specifično)",
            key="ap_kat_nt",
            placeholder="ostavi prazno za default",
        )

        if st.button("Generiraj zahtjev", type="primary"):
            doc = generiraj_zahtjev_kategorizacija(podnositelj, podaci)
            audit_input = {"podnositelj_html": podnositelj, "podaci": podaci}
            prikazi_dokument(doc, "Zahtjev_kategorizacija.docx", "Preuzmi zahtjev",
                             **audit_kwargs("zahtjev_kategorizacija", audit_input, "apartmani"))
