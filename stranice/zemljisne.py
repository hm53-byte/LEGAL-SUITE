# -----------------------------------------------------------------------------
# STRANICA: Zemljisne knjige
# -----------------------------------------------------------------------------
import streamlit as st
from pomocne import (
    unos_stranke,
    zaglavlje_sastavljaca,
    prikazi_dokument,
    odabir_suda,
    unos_tocaka,
    doc_selectbox,
    audit_kwargs,
    napuni_primjerom,
)
from generatori.zemljisne import (
    generiraj_tabularnu_doc,
    generiraj_zk_prijedlog,
    generiraj_zabilježbu,
    generiraj_predbiježbu,
    generiraj_upis_hipoteke,
    generiraj_brisanje_hipoteke,
    generiraj_upis_sluznosti,
    generiraj_brisovno_ocitovanje,
    generiraj_upis_plodouzivanja,
    generiraj_punomoc_prodaje_nekretnine,
)
from generatori.tuzbe import generiraj_brisovnu_tuzbu
from pristojbe import pristojba_zk_prijedlog


def render_zemljisne():
    st.header("Zemljišne knjige")
    zk_usluga = doc_selectbox(
        "Odaberite ZK uslugu",
        ["Tabularna isprava", "ZK Prijedlog (Uknjižba)", "Brisovna tužba",
         "Zabilježba", "Predbilježba", "Upis hipoteke", "Brisanje hipoteke", "Upis služnosti",
         "Brisovno očitovanje", "Upis plodouživanja (uzufrukt)", "Punomoć za prodaju nekretnine"],
    )

    if zk_usluga == "Tabularna isprava":
        c1, c2 = st.columns(2)
        prod, _, _ = unos_stranke("PRODAVATELJ", "tp")
        kup, _, _ = unos_stranke("KUPAC", "tk")
        c1, c2, c3 = st.columns(3)
        ko = c1.text_input("K.O.", help="Katastarska općina u kojoj se nalazi nekretnina.")
        cest = c2.text_input("Čestica", help="Broj katastarske čestice (k.č.br.).")
        ul = c3.text_input("Uložak", help="Broj zemljišnoknjižnog uloška (ZK ul.).")
        opis = st.text_area("Opis u naravi", help="Opis nekretnine (npr. 'kuća i dvorište', 'oranica').")
        dat = st.date_input("Datum ugovora")
        if st.button("Generiraj tabularnu ispravu", type="primary"):
            datum_str = dat.strftime('%d.%m.%Y.')
            doc = generiraj_tabularnu_doc(prod, kup, ko, cest, ul, opis, datum_str)
            audit_input = {
                "prodavatelj_html": prod, "kupac_html": kup,
                "ko": ko, "cestica": cest, "ulozak": ul,
                "opis": opis, "datum": datum_str,
            }
            prikazi_dokument(doc, "Tabularna.docx", "Preuzmi dokument",
                             **audit_kwargs("tabularna_isprava", audit_input, "zemljisne"))

    elif zk_usluga == "ZK Prijedlog (Uknjižba)":
        st.warning(
            "**Upozorenje — obvezno angažiranje odvjetnika ili javnog bilježnika:** "
            "Sukladno Zakonu o zemljišnim knjigama (NN 63/19, čl. 109.) i Zakonu o javnom bilježništvu, "
            "isprava koja je temelj za uknjižbu prava vlasništva (tabularna isprava / clausula intabulandi) "
            "mora biti sastavljena ili ovjerena pred javnim bilježnikom ili odvjetnikom. "
            "Prijedlog za uknjižbu možete podnijeti osobno, ali bez valjane solemnizacije/ovjere "
            "isprava neće biti prihvaćena. **Preporučujemo konzultaciju s odvjetnikom ili javnim bilježnikom.**"
        )
        sud = odabir_suda("Sud", vrsta="opcinski", key="zk_sud")
        c1, c2, c3 = st.columns(3)
        ko = c1.text_input("K.O.", "Centar")
        ulozak = c2.text_input("ZK uložak")
        cestica = c3.text_input("Čestica")
        opis = st.text_area("Opis u naravi")
        c1, c2 = st.columns(2)
        pred, _, _ = unos_stranke("PREDLAGATELJ", "zk_p")
        prot, _, _ = unos_stranke("PROTUSTRANKA", "zk_pr")
        ug = st.text_input("Ugovor info")
        tab = st.text_input("Tabularna info")
        st.info(f"ZK pristojba (Tbr. 20): **{pristojba_zk_prijedlog():,.2f} EUR**")
        pristojba = st.number_input("ZK pristojba", value=pristojba_zk_prijedlog())
        if st.button("Generiraj prijedlog", type="primary"):
            nekretnina = {'ko': ko, 'ulozak': ulozak, 'cestica': cestica, 'opis': opis}
            isprave = {'ugovor': ug, 'tabularna': tab}
            troskovi = {'pristojba': pristojba}
            doc = generiraj_zk_prijedlog(sud, pred, prot, nekretnina, isprave, troskovi)
            audit_input = {
                "sud": sud,
                "predlagatelj_html": pred,
                "protustranka_html": prot,
                "nekretnina": nekretnina,
                "isprave": isprave,
                "troskovi": troskovi,
            }
            prikazi_dokument(doc, "ZK_Prijedlog.docx", "Preuzmi dokument",
                             **audit_kwargs("zk_prijedlog", audit_input, "zemljisne"))

    elif zk_usluga == "Brisovna tužba":
        zastupanje = zaglavlje_sastavljaca()
        sud = odabir_suda("Nadležni sud", vrsta="opcinski", key="bt_sud")
        c1, c2 = st.columns(2)
        tuzitelj, _, _ = unos_stranke("TUŽITELJ", "bt_t")
        tuzenik, _, _ = unos_stranke("TUŽENIK", "bt_tu")
        c1, c2, c3 = st.columns(3)
        ko = c1.text_input("K.O.")
        ulozak = c2.text_input("Uložak")
        cestica = c3.text_input("Čestica")
        opis = st.text_area("Opis u naravi")
        c1, c2 = st.columns(2)
        z_broj = c1.text_input("Z-broj")
        dat_uknj = c2.date_input("Datum uknjižbe")
        vrsta_nevaljanosti = st.selectbox(
            "Vrsta nevaljanosti isprave",
            [
                "Ugovor je ništetan (čl. 322. ZOO)",
                "Isprava je falsificirana / krivotvorena",
                "Nedostaje valjana clausula intabulandi",
                "Ugovor je sklopljen pod prisilom ili prijevarom",
                "Ugovor je sklopljen od neovlaštene osobe",
                "Ostalo (ručni unos)",
            ],
            key="bt_vrsta_neval",
            help="Odaberite pravni temelj nevaljanosti isprave na kojoj se zasniva brisovna tužba.",
        )
        if vrsta_nevaljanosti == "Ostalo (ručni unos)":
            razlog_tekst = st.text_area("Razlog nevaljanosti", key="bt_razlog_rucni")
        else:
            razlog_tekst = vrsta_nevaljanosti

        st.markdown("**Obrazloženje** *(detaljniji opis činjenica)*")
        razlog_tocke = unos_tocaka(
            "Obrazloženje", "bt_razlozi",
            placeholder="Npr. Prodavatelj nikada nije potpisao navedeni ugovor...",
            min_tocaka=1, max_tocaka=10, height=80,
        )
        if razlog_tocke:
            razlog = razlog_tekst + "\n\n" + "\n\n".join(f"{i+1}. {t}" for i, t in enumerate(razlog_tocke))
        else:
            razlog = razlog_tekst

        tuzenik_znao = st.radio("Je li tuženik znao za nevaljanost?", ["DA", "NE"],
                                help="Utječe na tekst tužbe - savjesnost/nesavjesnost stjecatelja.")
        vps = st.number_input("VPS", 10000.0)
        sastav = st.number_input("Cijena sastava", 0.0)
        pdv = sastav * 0.25
        pristojba = st.number_input("Pristojba", 0.0)
        if st.button("Generiraj brisovnu tužbu", type="primary"):
            nekretnina = {'ko': ko, 'ulozak': ulozak, 'cestica': cestica, 'opis': opis}
            podaci = {
                'vps': vps,
                'z_broj': z_broj,
                'datum_uknjizbe': dat_uknj.strftime('%d.%m.%Y.'),
                'isprava': "Ugovor",
                'datum_isprave': "...",
                'razlog_nevaljanosti': razlog,
                'tuzenik_znao': "DA" in tuzenik_znao,
                'mjesto': "Zagreb",
            }
            troskovnik = {'stavka': sastav, 'pdv': pdv, 'pristojba': pristojba}
            doc = generiraj_brisovnu_tuzbu(sud, zastupanje, tuzitelj, tuzenik,
                                            nekretnina, podaci, troskovnik)
            audit_input = {
                "sud": sud,
                "zastupanje": zastupanje,
                "tuzitelj_html": tuzitelj,
                "tuzenik_html": tuzenik,
                "nekretnina": nekretnina,
                "podaci": podaci,
                "troskovnik": troskovnik,
            }
            prikazi_dokument(doc, "Brisovna.docx", "Preuzmi dokument",
                             **audit_kwargs("brisovna_tuzba", audit_input, "zemljisne"))

    elif zk_usluga == "Zabilježba":
        sud = odabir_suda("Sud", vrsta="opcinski", key="zab_sud")
        pred, _, _ = unos_stranke("PREDLAGATELJ", "zab_")
        c1, c2, c3 = st.columns(3)
        ko = c1.text_input("K.O.", key="zab_ko")
        ulozak = c2.text_input("Uložak", key="zab_ulozak")
        cestica = c3.text_input("Čestica", key="zab_cestica")
        vrsta_zabilježbe = st.selectbox(
            "Vrsta zabilježbe",
            ["spora", "ovrhe", "stečaja", "maloljetnosti", "oduzimanje_pos_sposobnosti"],
            key="zab_vrsta",
        )
        opis_cinjenice = st.text_area("Opis činjenice", key="zab_opis")
        pravni_temelj = st.text_input("Pravni temelj", key="zab_pravni")
        mjesto = st.text_input("Mjesto", key="zab_mjesto")
        if st.button("Generiraj zabilježbu", type="primary"):
            podaci = {
                'ko': ko, 'ulozak': ulozak, 'cestica': cestica,
                'vrsta_zabilježbe': vrsta_zabilježbe,
                'opis_cinjenice': opis_cinjenice,
                'pravni_temelj': pravni_temelj,
                'mjesto': mjesto,
            }
            doc = generiraj_zabilježbu(sud, pred, podaci)
            audit_input = {"sud": sud, "predlagatelj_html": pred, "podaci": podaci}
            prikazi_dokument(doc, "Zabilježba.docx", "Preuzmi dokument",
                             **audit_kwargs(f"zabiljezba_{vrsta_zabilježbe}", audit_input, "zemljisne"))

    elif zk_usluga == "Predbilježba":
        sud = odabir_suda("Sud", vrsta="opcinski", key="pred_sud")
        pred, _, _ = unos_stranke("PREDLAGATELJ", "pred_")
        prot, _, _ = unos_stranke("PROTUSTRANKA", "pred_pr_")
        c1, c2, c3 = st.columns(3)
        ko = c1.text_input("K.O.", key="pred_ko")
        ulozak = c2.text_input("Uložak", key="pred_ulozak")
        cestica = c3.text_input("Čestica", key="pred_cestica")
        vrsta_prava = st.selectbox(
            "Vrsta prava",
            ["vlasništvo", "založno_pravo"],
            key="pred_vrsta",
        )
        nedostatak_isprave = st.text_area("Nedostatak isprave", key="pred_nedostatak")
        pravni_temelj = st.text_input("Pravni temelj", key="pred_pravni")
        mjesto = st.text_input("Mjesto", key="pred_mjesto")
        if st.button("Generiraj predbilježbu", type="primary"):
            podaci = {
                'ko': ko, 'ulozak': ulozak, 'cestica': cestica,
                'vrsta_prava': vrsta_prava,
                'nedostatak_isprave': nedostatak_isprave,
                'pravni_temelj': pravni_temelj,
                'mjesto': mjesto,
            }
            doc = generiraj_predbiježbu(sud, pred, prot, podaci)
            audit_input = {
                "sud": sud,
                "predlagatelj_html": pred,
                "protustranka_html": prot,
                "podaci": podaci,
            }
            prikazi_dokument(doc, "Predbilježba.docx", "Preuzmi dokument",
                             **audit_kwargs("predbiljezba", audit_input, "zemljisne"))

    elif zk_usluga == "Upis hipoteke":
        sud = odabir_suda("Sud", vrsta="opcinski", key="hip_sud")
        vjerovnik, _, _ = unos_stranke("VJEROVNIK", "hip_v_")
        zalozni_duznik, _, _ = unos_stranke("ZALOŽNI DUŽNIK", "hip_zd_")
        c1, c2, c3 = st.columns(3)
        ko = c1.text_input("K.O.", key="hip_ko")
        ulozak = c2.text_input("Uložak", key="hip_ulozak")
        cestica = c3.text_input("Čestica", key="hip_cestica")
        opis_nekretnine = st.text_area("Opis nekretnine", key="hip_opis")
        iznos_trazbine = st.number_input("Iznos tražbine (EUR)", 0.0, key="hip_iznos")
        kamatna_stopa = st.text_input("Kamatna stopa", key="hip_kamata")
        broj_ugovora_kredita = st.text_input("Broj ugovora/kredita", key="hip_ugovor")
        pristojba = st.number_input("Pristojba", 0.0, key="hip_pristojba")
        mjesto = st.text_input("Mjesto", key="hip_mjesto")
        if st.button("Generiraj upis hipoteke", type="primary"):
            podaci = {
                'ko': ko, 'ulozak': ulozak, 'cestica': cestica,
                'opis_nekretnine': opis_nekretnine,
                'iznos_trazbine': iznos_trazbine,
                'kamatna_stopa': kamatna_stopa,
                'broj_ugovora_kredita': broj_ugovora_kredita,
                'mjesto': mjesto,
            }
            troskovi = {'pristojba': pristojba}
            doc = generiraj_upis_hipoteke(sud, vjerovnik, zalozni_duznik, podaci, troskovi)
            audit_input = {
                "sud": sud,
                "vjerovnik_html": vjerovnik,
                "zalozni_duznik_html": zalozni_duznik,
                "podaci": podaci,
                "troskovi": troskovi,
            }
            prikazi_dokument(doc, "Upis_hipoteke.docx", "Preuzmi dokument",
                             **audit_kwargs("upis_hipoteke", audit_input, "zemljisne"))

    elif zk_usluga == "Brisanje hipoteke":
        sud = odabir_suda("Sud", vrsta="opcinski", key="bh_sud")
        vlasnik, _, _ = unos_stranke("VLASNIK", "bh_")
        c1, c2, c3 = st.columns(3)
        ko = c1.text_input("K.O.", key="bh_ko", help="Katastarska općina u kojoj se nalazi nekretnina.")
        ulozak = c2.text_input("Uložak", key="bh_ulozak")
        cestica = c3.text_input("Čestica", key="bh_cestica")
        z_broj = st.text_input("Z-broj upisa hipoteke", key="bh_z_broj",
                               help="Z-broj pod kojim je hipoteka upisana u C list (Teretovnicu).")
        vjerovnik_naziv = st.text_input("Naziv vjerovnika (hipotekarni)", key="bh_vjerovnik",
                                        help="Banka, fizička ili pravna osoba u čiju korist je upisana hipoteka.")

        razlog_brisanja = st.selectbox(
            "Razlog / temelj brisanja",
            [
                ("otplata_kredita", "Otplata kredita (brisovno očitovanje)"),
                ("sudska_odluka", "Pravomoćna sudska odluka"),
                ("zastara", "Zastara tražbine"),
                ("nagodba", "Nagodba (sudska ili izvansudska)"),
                ("kompenzacija", "Kompenzacija (prijeboj)"),
                ("zakonska_hipoteka_prestanak", "Prestanak zakonske hipoteke"),
            ],
            format_func=lambda x: x[1],
            key="bh_razlog",
            help="Odaberite pravni temelj na kojem se zasniva zahtjev za brisanje hipoteke.",
        )

        st.markdown("**Dodatno obrazloženje** *(opcionalno - razlozi zašto se traži brisanje)*")
        dodatni_razlozi = unos_tocaka(
            "Obrazloženje", "bh_razlozi",
            placeholder="Npr. Kredit je otplaćen dana 01.01.2025., što potvrđuje brisovno očitovanje banke...",
            min_tocaka=0, max_tocaka=5, height=80,
        )

        mjesto = st.text_input("Mjesto", key="bh_mjesto")
        if st.button("Generiraj brisanje hipoteke", type="primary"):
            podaci = {
                'ko': ko, 'ulozak': ulozak, 'cestica': cestica,
                'z_broj': z_broj,
                'vjerovnik_naziv': vjerovnik_naziv,
                'razlog_brisanja': razlog_brisanja[0],
                'dodatni_razlozi': dodatni_razlozi,
                'mjesto': mjesto,
            }
            doc = generiraj_brisanje_hipoteke(sud, vlasnik, podaci)
            audit_input = {"sud": sud, "vlasnik_html": vlasnik, "podaci": podaci}
            prikazi_dokument(doc, "Brisanje_hipoteke.docx", "Preuzmi dokument",
                             **audit_kwargs(f"brisanje_hipoteke_{razlog_brisanja[0]}", audit_input, "zemljisne"))

    elif zk_usluga == "Upis služnosti":
        sud = odabir_suda("Sud", vrsta="opcinski", key="sluz_sud")
        pred, _, _ = unos_stranke("PREDLAGATELJ", "sluz_")
        vrsta_sluznosti = st.radio("Vrsta služnosti", ["stvarna", "osobna"], key="sluz_vrsta")
        st.subheader("Poslužno dobro")
        c1, c2, c3 = st.columns(3)
        ko_posluzno = c1.text_input("K.O. (poslužno)", key="sluz_ko_posluzno")
        ulozak_posluzno = c2.text_input("Uložak (poslužno)", key="sluz_ulozak_posluzno")
        cestica_posluzno = c3.text_input("Čestica (poslužno)", key="sluz_cestica_posluzno")
        if vrsta_sluznosti == "stvarna":
            st.subheader("Povlasno dobro")
            c1, c2, c3 = st.columns(3)
            ko_povlasno = c1.text_input("K.O. (povlasno)", key="sluz_ko_povlasno")
            ulozak_povlasno = c2.text_input("Uložak (povlasno)", key="sluz_ulozak_povlasno")
            cestica_povlasno = c3.text_input("Čestica (povlasno)", key="sluz_cestica_povlasno")
        else:
            ko_povlasno = ""
            ulozak_povlasno = ""
            cestica_povlasno = ""
        sadrzaj_sluznosti = st.text_area("Sadržaj služnosti", key="sluz_sadrzaj")
        pravni_temelj = st.text_input("Pravni temelj", key="sluz_pravni")
        pristojba = st.number_input("Pristojba", 0.0, key="sluz_pristojba")
        mjesto = st.text_input("Mjesto", key="sluz_mjesto")
        if st.button("Generiraj upis služnosti", type="primary"):
            podaci = {
                'vrsta_sluznosti': vrsta_sluznosti,
                'ko_posluzno': ko_posluzno, 'ulozak_posluzno': ulozak_posluzno, 'cestica_posluzno': cestica_posluzno,
                'ko_povlasno': ko_povlasno, 'ulozak_povlasno': ulozak_povlasno, 'cestica_povlasno': cestica_povlasno,
                'sadrzaj_sluznosti': sadrzaj_sluznosti,
                'pravni_temelj': pravni_temelj,
                'mjesto': mjesto,
            }
            troskovi = {'pristojba': pristojba}
            doc = generiraj_upis_sluznosti(sud, pred, podaci, troskovi)
            audit_input = {
                "sud": sud,
                "predlagatelj_html": pred,
                "podaci": podaci,
                "troskovi": troskovi,
            }
            prikazi_dokument(doc, "Upis_sluznosti.docx", "Preuzmi dokument",
                             **audit_kwargs(f"upis_sluznosti_{vrsta_sluznosti}", audit_input, "zemljisne"))

    elif zk_usluga == "Brisovno očitovanje":
        st.caption("Vjerovnik izdaje (ovjereno kod JB) — vlasnik nekretnine s ovim očitovanjem podnosi prijedlog za brisanje hipoteke.")
        napuni_primjerom('brisovno_ocitovanje', '')
        c1, c2 = st.columns(2)
        with c1:
            vjerovnik, _, _ = unos_stranke("VJEROVNIK (banka / pojedinac)", "bo_vj")
        with c2:
            vlasnik, _, _ = unos_stranke("VLASNIK NEKRETNINE", "bo_vl")
        st.subheader("Nekretnina")
        c1, c2, c3 = st.columns(3)
        ko_b = c1.text_input("K.O.", key="bo_ko")
        ulozak_b = c2.text_input("ZK uložak", key="bo_ul")
        cestica_b = c3.text_input("Čestica (k.č.br.)", key="bo_ces")
        opis_b = st.text_input("Opis u naravi (opcionalno)", key="bo_op")
        st.subheader("Upis koji se briše")
        c1, c2, c3 = st.columns(3)
        z_broj = c1.text_input("Broj upisa (Z)", key="bo_z", placeholder="npr. Z-1234/2018")
        datum_upisa = c2.text_input("Datum upisa", key="bo_du", placeholder="dd.mm.yyyy.")
        iznos = c3.text_input("Osigurana tražbina", key="bo_iz", placeholder="npr. 100.000,00 EUR")
        razlog = st.selectbox(
            "Razlog prestanka tražbine",
            ["isplate cjelokupne tražbine", "kompenzacije s protutražbinom",
             "nagodbe između stranaka", "zastare tražbine", "drugog razloga prestanka"],
            key="bo_raz",
        )
        mjesto_b = st.text_input("Mjesto izdavanja", "Zagreb", key="bo_mj")
        if st.button("Generiraj brisovno očitovanje", type="primary"):
            podaci = {
                'ko': ko_b, 'ulozak': ulozak_b, 'cestica': cestica_b,
                'opis_nekretnine': opis_b, 'z_broj': z_broj, 'datum_upisa': datum_upisa,
                'iznos_trazbine': iznos, 'razlog_prestanka': razlog, 'mjesto': mjesto_b,
            }
            doc = generiraj_brisovno_ocitovanje(vjerovnik, vlasnik, podaci)
            audit_input = {"vjerovnik_html": vjerovnik, "vlasnik_html": vlasnik, "podaci": podaci}
            prikazi_dokument(doc, "Brisovno_ocitovanje.docx", "Preuzmi očitovanje",
                             **audit_kwargs("brisovno_ocitovanje", audit_input, "zemljisne"))

    elif zk_usluga == "Upis plodouživanja (uzufrukt)":
        st.caption("Pravni temelj: ZV čl. 199-213 (osobne služnosti). Pravo prestaje smrću plodouživatelja, neprenosivo.")
        napuni_primjerom('upis_plodouzivanja', '')
        sud_p = odabir_suda("Sud", vrsta="opcinski", key="plod_sud")
        c1, c2 = st.columns(2)
        with c1:
            vlasnik_p, _, _ = unos_stranke("VLASNIK NEKRETNINE", "plod_vl")
        with c2:
            plodouz, _, _ = unos_stranke("PLODOUŽIVATELJ", "plod_pu")
        st.subheader("Nekretnina")
        c1, c2, c3 = st.columns(3)
        ko_p = c1.text_input("K.O.", key="plod_ko")
        ulozak_p = c2.text_input("ZK uložak", key="plod_ul")
        cestica_p = c3.text_input("Čestica", key="plod_ces")
        opis_p = st.text_input("Opis u naravi", key="plod_op")
        st.subheader("Opseg i uvjeti")
        c1, c2 = st.columns(2)
        opseg_p = c1.selectbox(
            "Opseg plodouživanja",
            ["puno plodouživanje (uživanje stvari u cijelosti)",
             "djelomično plodouživanje (samo dio nekretnine)",
             "plodouživanje samo prihoda (najamnine, plodova)"],
            key="plod_opseg",
        )
        trajanje_p = c2.selectbox(
            "Trajanje",
            ["doživotno (do smrti plodouživatelja)",
             "na određeno vrijeme",
             "do nastupa nekog uvjeta"],
            key="plod_traj",
        )
        ogranicenja_p = st.text_area(
            "Ograničenja / izuzeća (opcionalno)",
            placeholder="npr. plodouživatelj ne smije bez suglasnosti vlasnika davati nekretninu u zakup",
            height=80, key="plod_ogr",
        )
        naknada_p = st.text_input("Naknada", "bez naknade", key="plod_nak")
        pravni_temelj_p = st.text_input(
            "Pravni temelj",
            placeholder="npr. Ugovor o osnivanju plodouživanja od 01.05.2026.",
            key="plod_pt",
        )
        c1, c2 = st.columns(2)
        pristojba_p = c1.number_input("Sudska pristojba", 0.0, key="plod_pri")
        mjesto_p = c2.text_input("Mjesto", "Zagreb", key="plod_mj")
        if st.button("Generiraj prijedlog uknjižbe", type="primary"):
            podaci = {
                'ko': ko_p, 'ulozak': ulozak_p, 'cestica': cestica_p, 'opis_nekretnine': opis_p,
                'opseg': opseg_p, 'ogranicenja': ogranicenja_p, 'pravni_temelj': pravni_temelj_p,
                'naknada': naknada_p, 'trajanje': trajanje_p, 'mjesto': mjesto_p,
            }
            troskovi = {'pristojba': pristojba_p}
            doc = generiraj_upis_plodouzivanja(sud_p, vlasnik_p, plodouz, podaci, troskovi)
            audit_input = {
                "sud": sud_p, "vlasnik_html": vlasnik_p, "plodouzivatelj_html": plodouz,
                "podaci": podaci, "troskovi": troskovi,
            }
            prikazi_dokument(doc, "Upis_plodouzivanja.docx", "Preuzmi prijedlog",
                             **audit_kwargs("upis_plodouzivanja", audit_input, "zemljisne"))

    elif zk_usluga == "Punomoć za prodaju nekretnine":
        st.caption("Specijalna punomoć (ZOO čl. 308-331) sa autopopulacijom k.č.br./zk.ul. Potpis se ovjerava kod JB.")
        napuni_primjerom('punomoc_prodaje_nekretnine', '')
        c1, c2 = st.columns(2)
        with c1:
            vlastodavac, _, _ = unos_stranke("VLASTODAVAC (vlasnik)", "pun_vl")
        with c2:
            punomocnik_n, _, _ = unos_stranke("PUNOMOĆNIK", "pun_pu")
        st.subheader("Nekretnina")
        c1, c2, c3 = st.columns(3)
        ko_n = c1.text_input("K.O.", key="pun_ko")
        ulozak_n = c2.text_input("ZK uložak", key="pun_ul")
        cestica_n = c3.text_input("Čestica", key="pun_ces")
        opis_n = st.text_input("Opis u naravi", key="pun_op", placeholder="npr. stan, kuća s dvorištem")
        c1, c2 = st.columns(2)
        adresa_n = c1.text_input("Adresa", key="pun_adr", placeholder="npr. Ilica 100, 10000 Zagreb")
        povrsina_n = c2.text_input("Površina (m²)", key="pun_pov", placeholder="opcionalno")
        st.subheader("Uvjeti punomoći")
        c1, c2 = st.columns(2)
        min_cijena = c1.number_input(
            "Minimalna prihvatljiva cijena (EUR, opcionalno)",
            min_value=0.0, step=1000.0, key="pun_min",
            help="Ako 0 — punomoćnik može pregovarati slobodno.",
        )
        rok_pun = c2.text_input("Rok važenja", "12 (dvanaest) mjeseci od datuma ovjere", key="pun_rok")
        mjesto_n = st.text_input("Mjesto izdavanja", "Zagreb", key="pun_mj")
        if st.button("Generiraj punomoć", type="primary"):
            podaci = {
                'ko': ko_n, 'ulozak': ulozak_n, 'cestica': cestica_n,
                'opis_nekretnine': opis_n, 'adresa': adresa_n, 'povrsina_m2': povrsina_n,
                'minimalna_cijena_eur': min_cijena, 'rok_vazenja': rok_pun, 'mjesto': mjesto_n,
            }
            doc = generiraj_punomoc_prodaje_nekretnine(vlastodavac, punomocnik_n, podaci)
            audit_input = {"vlastodavac_html": vlastodavac, "punomocnik_html": punomocnik_n, "podaci": podaci}
            prikazi_dokument(doc, "Punomoc_prodaja_nekretnine.docx", "Preuzmi punomoć",
                             **audit_kwargs("punomoc_prodaja_nekretnine", audit_input, "zemljisne"))
