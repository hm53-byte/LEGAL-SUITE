# 07 — KOD: PAYWALL INTEGRACIJA U `pomocne.py`

> Tu spajamo sve dosadašnje. Kad korisnik klikne "Generiraj", **prije** nego se prikaže download gumb — provjeravamo smije li, i ako ne — prikazujemo paywall.

---

## 1. GDJE SE TO DOGAĐA

U tvojoj postojećoj aplikaciji, **svaki** generirani dokument na kraju zove:

```python
prikazi_dokument(doc_html, "Tuzba.docx", "Preuzmi tužbu")
```

Ova funkcija je u `pomocne.py` na liniji ~707. Trenutno radi sljedeće:
1. Prikaže success banner
2. Pretvori HTML u DOCX bytes
3. Prikaže download gumb
4. Prikaže preview dokumenta

**Mi ćemo dodati** prije koraka 1: provjeru `smije_generirati()`. Ako ne smije → paywall, ako smije → kao do sad + bilježenje.

---

## 2. PROMJENA `pomocne.py`

Otvori `APLIKACIJA/pomocne.py` i nađi funkciju `prikazi_dokument` (oko linije 707).

### 2.1 Stari kod (referenca):

```python
def prikazi_dokument(doc_html, naziv_datoteke, label_preuzmi="Preuzmi"):
    """Pomocna funkcija za prikaz dokumenta i download gumb (.docx format)."""
    # Success banner
    st.markdown("...success...", unsafe_allow_html=True)

    docx_naziv = naziv_datoteke.replace('.doc', '.docx') ...
    if not docx_naziv.endswith('.docx'):
        docx_naziv += '.docx'

    watermark_tekst = "NACRT" if st.session_state.get("_docx_watermark") else None
    naslov = docx_naziv.replace('.docx', '').replace('_', ' ') if st.session_state.get("_docx_header") else None

    docx_bytes = pripremi_za_docx(doc_html, watermark=watermark_tekst, naslov_dokumenta=naslov)

    st.download_button(
        f"⬇️ {label_preuzmi} ({docx_naziv})",
        docx_bytes,
        docx_naziv,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    st.markdown(f"<div class='legal-doc'>{doc_html}</div>", unsafe_allow_html=True)
```

### 2.2 Novi kod (zamijeniti)

**Zamijeni cijelu funkciju ovim:**

```python
def prikazi_dokument(doc_html, naziv_datoteke, label_preuzmi="Preuzmi", doc_type="generic"):
    """
    Pomocna funkcija za prikaz dokumenta i download gumb (.docx format).

    NOVO U v5.0:
        - Provjerava ima li korisnik pravo (pretplata ili free trial)
        - Ako ne — prikazuje paywall umjesto dokumenta
        - Bilježi svako preuzimanje u usage_log

    Args:
        doc_html:        HTML sadržaj dokumenta
        naziv_datoteke:  npr. "Tuzba_Horvat_protiv_Maric.docx"
        label_preuzmi:   tekst download gumba
        doc_type:        kategorija dokumenta za audit log
                         (npr. "tuzba_novcana", "ovrha_jb", "ugovor_o_radu")
    """
    from auth import trenutni_korisnik
    from billing import smije_generirati, zabiljezi_koristenje, prikazi_paywall

    # ----- 1) PROVJERA AUTH -----
    user = trenutni_korisnik()
    if not user:
        st.error("Morate biti prijavljeni za preuzimanje dokumenta.")
        return

    # ----- 2) PROVJERA PRAVA -----
    smije, razlog = smije_generirati(user["id"])

    if not smije:
        # Iscrpljen besplatni trial — prikaži paywall i prekini
        prikazi_paywall(user["id"], user["email"])
        return

    # ----- 3) GENERIRAJ DOCX -----
    docx_naziv = naziv_datoteke.replace('.doc', '.docx') if naziv_datoteke.endswith('.doc') else naziv_datoteke
    if not docx_naziv.endswith('.docx'):
        docx_naziv += '.docx'

    watermark_tekst = "NACRT" if st.session_state.get("_docx_watermark") else None
    naslov = docx_naziv.replace('.docx', '').replace('_', ' ') if st.session_state.get("_docx_header") else None

    docx_bytes = pripremi_za_docx(doc_html, watermark=watermark_tekst, naslov_dokumenta=naslov)

    # ----- 4) ZABILJEŽI KORIŠTENJE -----
    # NAPOMENA: Bilježimo na trenutku generiranja (ne na klik download-a),
    # jer Streamlit download_button ne pruža pouzdan on_click callback.
    # Ovo je dovoljno za free trial brojač i analytics.
    was_paid = (razlog == "subscribed")
    zabiljezi_koristenje(user["id"], doc_type, was_paid=was_paid)

    # ----- 5) SUCCESS BANNER -----
    if razlog == "subscribed":
        banner_text = "Dokument je spreman!"
        banner_sub = "Pregledajte dokument ispod i preuzmite ga u DOCX formatu."
    else:
        banner_text = "Dokument je spreman! (besplatno)"
        banner_sub = f"Iskorišten besplatni dokument: {razlog.split('(')[1].rstrip(')')}. Sljedeći zahtjeva pretplatu."

    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, #059669 0%, #047857 100%);
                    color: white; padding: 1rem 1.5rem; border-radius: 10px;
                    margin: 1rem 0; text-align: center;'>
            <span style='font-size: 1.3rem; font-weight: 700;'>
                ✅ {banner_text}
            </span><br>
            <span style='font-size: 0.85rem; opacity: 0.9;'>
                {banner_sub}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----- 6) DOWNLOAD GUMB -----
    st.download_button(
        f"⬇️ {label_preuzmi} ({docx_naziv})",
        docx_bytes,
        docx_naziv,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    # ----- 7) PREVIEW -----
    st.markdown(f"<div class='legal-doc'>{doc_html}</div>", unsafe_allow_html=True)
```

---

## 3. KAKO ČITATI NOVU FUNKCIJU (KORAK PO KORAK)

**Krak 1: Tko je korisnik?**
- Pita `auth.trenutni_korisnik()` koji vraća dict ili None
- Ako None → "Morate biti prijavljeni" (ovo se ne bi trebalo dogoditi jer login_stranica blokira ulaz, ali sigurnosno)

**Korak 2: Smije li?**
- Pita `billing.smije_generirati(user_id)` koji vrati `(True/False, "razlog")`
- Ako False → `prikazi_paywall(user_id, email)` i `return` (prekida funkciju, dokument se ne generira)
- Ako True → nastavi

**Korak 3: Generiranje DOCX-a**
- Identično staroj logici (watermark, naslov, pretvorba HTML→DOCX)

**Korak 4: Bilježenje**
- Pozovi `zabiljezi_koristenje()` koji upiše u `usage_log` i poveća brojač ako je free
- **Bilježi se NA generiranju, ne na klik download-a** (limitacija Streamlita)

**Korak 5: Banner**
- Različit tekst za plaćene vs free korisnike (lagani upsell prompt)

**Krak 6: Download gumb**
- Identično staroj logici

**Korak 7: Preview**
- Identično staroj logici

---

## 4. ZAŠTO BILJEŽIMO NA GENERIRANJU, A NE NA KLIKU?

Streamlit-ov `st.download_button` **nema pouzdan on_click callback** koji bi se okinuo tek kad korisnik stvarno klikne preuzimanje. Pokušaji su:

1. **`on_click=callback`** — okine se kad se gumb prikaže, ne kad se klikne
2. **Provjera u sljedećem rerun-u** — Streamlit ne triggera rerun na download
3. **JavaScript hook** — kompliciranije, fragile

Najjednostavniji praktični kompromis: **bilježi na trenutku generiranja**.

**Posljedica:** ako korisnik klikne "Generiraj" i ne preuzme, brojač se svejedno poveća. Na većim brojevima — dovoljno blizu istini.

**Alternativa (kasnije):** zamijeni `st.download_button` s `st.html` koji ima `<a href="data:...">` link s JavaScriptom koji javi back-end-u na klik. Komplicirano, ostavi za v6.

---

## 5. DODAVANJE `doc_type` U SVIM `stranice/*.py`

Sad svaki poziv `prikazi_dokument(...)` u `stranice/` modulima trebaš dopuniti s `doc_type` parametrom za bolje analytics.

### 5.1 Primjer: `stranice/tuzbe.py`

Stari poziv:
```python
prikazi_dokument(doc_html, "Tuzba.docx", "Preuzmi tužbu")
```

Novi:
```python
prikazi_dokument(doc_html, "Tuzba.docx", "Preuzmi tužbu", doc_type="tuzba_novcana")
```

### 5.2 Predložene `doc_type` vrijednosti po modulima

| Modul | Tipovi dokumenata |
|-------|-------------------|
| `tuzbe.py` | `tuzba_novcana`, `tuzba_radnik`, `tuzba_alimentacija` |
| `ovrhe.py` | `ovrha_jb`, `ovrha_presuda`, `ovrha_placa`, `obustava_ovrhe` |
| `ugovori.py` | `ugovor_kupoprodaja`, `ugovor_najam`, `ugovor_o_radu`, `nda` |
| `opomene.py` | `opomena_pred_tuzbu` |
| `punomoci.py` | `punomoc_opca`, `punomoc_posebna` |
| `zalbe.py` | `zalba_presuda`, `zalba_zup` |
| `kazneno.py` | `kaznena_prijava`, `prigovor_kazneni_nalog` |
| `obiteljsko.py` | `tuzba_razvod`, `sporazum_razvod`, `alimentacija` |
| `trgovacko.py` | `drustveni_ugovor_doo`, `odluka_skupstine`, `prijenos_udjela` |
| `obvezno.py` | `ugovor_zoo_*` (po potkategoriji) |
| `zemljisne.py` | `prijedlog_uknjizba`, `prijedlog_zaloznog_prava` |
| `stecajno.py` | `prijava_trazbine`, `prijedlog_stecaj` |
| `potrosaci.py` | `reklamacija`, `tuzba_potrosac` |

**Trik za bržu implementaciju:** ako te mrzi proći kroz svih ~50 file-ova odjednom, počni samo s top 5 najpopularnijih (tuzbe, ovrhe, ugovori, opomene, punomoci). Ostali mogu raditi s defaultom `"generic"` privremeno.

### 5.3 Kako ažurirati u praksi

Otvori `APLIKACIJA/stranice/tuzbe.py`, nađi `prikazi_dokument(...)` i dodaj `doc_type=`. Spremi.

Ako koristiš VS Code / PyCharm — **find & replace u folderu** "stranice":
- Find: `prikazi_dokument(doc_html, "Tuzba.docx"`
- Replace: `prikazi_dokument(doc_html, "Tuzba.docx", doc_type="tuzba_novcana"`

Itd. po file-u.

### 5.4 Backwards compatible

Ako negdje propustiš dodati `doc_type` — **ne ruši se ništa**. Default vrijednost je `"generic"`, što znači da će u `usage_log` biti zapis s tim tipom. Samo nećeš znati koji točno dokument je bio u analytics. Dovoljno za MVP.

---

## 6. EDGE CASE: KAD KORISNIK KLIKNE "GENERIRAJ" PA SE SRUŠI POSLIJE

Što ako:
1. User klikne "Generiraj"
2. `smije_generirati()` kaže DA (free trial)
3. `zabiljezi_koristenje()` poveća brojač na 1
4. **Generacija DOCX-a padne** (greška u `pripremi_za_docx`)

Korisnik je iskoristio besplatni iako nije dobio dokument!

**Rješenje (poboljšanje za v5.1):** prebaci `zabiljezi_koristenje()` POSLIJE generiranja DOCX-a:

```python
# Generiraj DOCX prvo
docx_bytes = pripremi_za_docx(doc_html, ...)

# Zabilježi tek nakon uspjeha
zabiljezi_koristenje(user["id"], doc_type, was_paid=was_paid)
```

To rješava taj edge case. Mali rizik suprotnog slučaja (DOCX gotov, bilježenje padne) — manje bitno.

---

## 7. KAKO TESTIRAŠ

1. Pokreni lokalno: `streamlit run LEGAL-SUITE.py`
2. Registriraj se s test emailom
3. Generiraj 1 dokument — trebao bi vidjeti zeleni banner "iskorišten 1/1" + dokument
4. Generiraj još jedan — trebao bi vidjeti **paywall** umjesto dokumenta
5. Klikni "Pretplati se mjesečno" — otvara LS checkout u novom tabu
6. Plati s test karticom (`4242 4242 4242 4242`)
7. Vrati se u app, klikni opet "Generiraj"
8. **PROBLEM**: pretplata neće biti aktivna jer webhook još ne radi (to je sljedeći korak `08`)

Za test bez webhooka, **ručno upiši pretplatu u Supabase**:
- SQL Editor → `INSERT INTO subscriptions (user_id, status, ends_at) VALUES ('<tvoj-uid>', 'active', '2027-01-01');`
- Sad je tvoj user "plaćen" do 2027.
- Klikni "Generiraj" opet — trebao bi raditi neograničeno

---

## 8. DODATNI UI POBOLJŠICE (OPCIONALNO ZA KASNIJE)

### 8.1 Brojač dokumenata u sidebar

Već je u `prikazi_korisnika_sidebar()` — pokazuje "Besplatno iskorišteno: X/1" za free korisnike.

### 8.2 "Upgrade" gumb stalno vidljiv

U sidebar dodaj gumb "Pretplati se za neograničeno →" koji je vidljiv free korisnicima:

```python
# U auth.prikazi_korisnika_sidebar(), nakon brojača:
if not is_paid:
    if st.sidebar.button("Pretplati se →", use_container_width=True, type="primary"):
        st.session_state._show_paywall = True
        st.rerun()
```

### 8.3 Paywall na vrhu stranice za "limit reached"

Umjesto da paywall iskoči tek kod download-a, prikaži ga na svim stranicama čim se vidi da je limit dosegnut:

```python
# U LEGAL-SUITE.py prije renderanja modula:
from billing import smije_generirati
from auth import trenutni_korisnik
user = trenutni_korisnik()
if user:
    smije, razlog = smije_generirati(user["id"])
    if not smije and st.session_state.get("_active_module") not in ["Početna", "Vodič"]:
        from billing import prikazi_paywall
        prikazi_paywall(user["id"], user["email"])
        st.stop()
```

To je agresivnije, ali povećava konverziju.

---

## TIPIČNI PROBLEMI

**"Korisnik vidi paywall ali se brojač pokazuje 0/1"**
→ Brojač se inkrementira tek nakon `zabiljezi_koristenje()`. Provjeri da se ta funkcija stvarno zove (možeš dodati `print("DEBUG: bilježim")` privremeno).

**"Paywall se prikazuje pred plaćenom korisniku"**
→ `ima_aktivnu_pretplatu()` ne radi. Provjeri u Supabase tablici `subscriptions` — ima li red s točnim `user_id`, `status='active'`, `ends_at` u budućnosti?

**"Download gumb se ne pojavljuje uopće"**
→ Vjerojatno greška u `pripremi_za_docx`. Pogledaj Streamlit konzolu (`streamlit run` terminal) za stack trace.

**"Stranice su `generic` u audit log-u"**
→ Nisi prošao kroz `stranice/*.py` da dodaš `doc_type=`. Nije blokirajuće, samo manje detaljan analytics.

---

## SLJEDEĆI KORAK

Otvori `08_WEBHOOK.md` — Edge Function koja prima webhookove iz Lemon Squeezyja. **Ovo je najsloženiji dio**, ali nakon toga sustav radi end-to-end.
