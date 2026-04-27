# 01 — Pravna analiza scrapera + AZOP DPIA

> **Datum**: 2026-04-27
> **Izvor istraživanja**: WebFetch e-oglasna.pravosudje.hr (robots.txt, politika-privatnosti, o-e-oglasnoj), AZOP DPIA portal, sudreg-data.gov.hr, data.gov.hr open license

---

## SAŽETAK ODLUKA

| Izvor | Tehnički | ToS | Sui generis | GDPR | **Verdict** |
|---|---|---|---|---|---|
| **e-Oglasna** | robots.txt prazan | Politika privatnosti **eksplicit navodi tehničke zaštite** | Visok | DPIA obvezan | **STOP — ne porting** |
| **e-Predmet** (web only) | Bez API-ja | Nema "uvjeti korištenja" | Visok ako se indeksira | DPIA obvezan | **STOP — ne scraping** |
| **Sudski registar** (`sudreg-data.gov.hr`) | OAuth2 REST API | **CC-BY licenca** | N/A (otvoreni podaci) | Niski (samo pravni subjekti) | **GO — već implementirano** |
| **Narodne novine** (`api_nn.py`) | ELI/JSON-LD | Otvoreni podaci | N/A (službeni tekstovi nisu zaštićeni) | Bez osobnih podataka | **GO — zadrži** |

**Glavni nalaz dana**: e-Oglasna politika privatnosti citira:
> "Ugrađene su zaštite od prikupljanja podataka Internet pretraživača s e-oglasne ploče."

Ovo je **namjerna tehnička barijera**. Iako nije eksplicit pravna zabrana, zaobilaženje takve barijere ulazi u zonu KZ čl. 266 (neovlašteni pristup računalnom sustavu) — jer si svjesno zaobišao protective measure. **Ne idi tamo.**

---

## 1. e-Oglasna — zašto STOP

### 1.1 Tehnička dimenzija
- **robots.txt**: `User-agent: *` bez Disallow → permisivan, ali nije autoritativan (samo signal)
- **Politika privatnosti**: eksplicit navedena **tehnička zaštita protiv scraping-a**
- **Praktične zaštite koje vjerojatno postoje** (ne nužno verifikabilno): cloudflare anti-bot, JavaScript challenges, IP rate limiting, captcha pri sumnjivom volumenu

### 1.2 Pravna dimenzija
- **KZ čl. 266** (neovlašteni pristup): zaobilaženje *protective measure* je element kaznenog djela
  - Argument "podaci su javni" ne pomaže ako svjesno zaobiđeš protection
  - Doktrina: *protected target* + *circumvention* + *intent* = sve tri komponente prisutne ako programski scrape-ash protected stranicu
- **GDPR** (čl. 6): tvoja svrha (komercijalni SaaS) ≠ izvorna svrha (procesna fikcija dostave) → **promjena svrhe** zahtijeva novu zakonitu osnovu
- **Sui generis** (ZAPSP čl. 149-156): MP "značajno ulaganje" → systematic extraction = povreda
- **Razdoblje čuvanja**: politika privatnosti navodi **8 dana (čl. 145 ZPP-a) ili 60 dana (Zakon o stečaju potrošača čl. 25)** → podaci se **ionako brišu**, indeksiranje besmisleno

### 1.3 AZOP perspektiva
Iz AZOP-ovog popisa obveznih DPIA tipova obrade:
- "Prikupljanje podataka s javnih društvenih medija za izradu profila" → analogija za sudske objave
- "Velike baze podataka koje se spajaju iz više izvora (data matching)" → tvoj proizvod kombinira NN + Sudreg + (potencijalno) e-Oglasna

**Zaključak**: tvoja arhitektura (kombinacija javnih registara + sustavna obrada s OIB-om kao pivot) **direktno ulazi u AZOP DPIA obveznu zonu**.

### 1.4 Operativna posljedica
**Akcija za sljedeću sesiju:**
1. **Ne vrši C2 (port iz RIJEKA_PRATILAC)** — RIJEKA_PRATILAC sam je u kategoriji "tihi pratilac" projekta i tamo se rizik može pravno bolje opravdati (osobna uporaba), ali u **komercijalnom proizvodu na Polar-u** to ne ide.
2. **Ukloni `api_eoglasna.py`** zajedno s C1 (`api_epredmet.py`) — oba modula su **jurisdikcijski rizik** i fiktivni → brisanje je čisto.
3. **Refaktor `stranice/eoglasna.py`**: postavi pristojan placeholder *"Pristup e-Oglasnoj nije podržan u proizvodu zbog politike privatnosti tijela. Korisnici mogu izravno posjetiti https://e-oglasna.pravosudje.hr/ za vlastiti uvid."* + outbound link.

---

## 2. e-Predmet — zašto STOP

### 2.1 Stanje
- **Postoji** (suprotno od HANDOFF tvrdnje): `https://e-predmet.pravosudje.hr/`
- **Javna i besplatna usluga** prema MPUDT objavi 2013
- **NEMA javnog API-ja** — samo web sučelje (search by court + case number)

### 2.2 Pravna dimenzija
- Ista logika kao e-Oglasna — sudski podaci s identitetima fizičkih osoba
- Razdoblje čuvanja: **prekršajni od 2021-01-01, upravni od 2021-07-01** (dakle, prošireno) → **dugotrajna dostupnost** povećava GDPR rizik (suprotno od e-Oglasne)
- Bez API-ja → scraping = jedina opcija → tehnički otporno na user-driven model jer treba sesijski cookies, JS rendering, captcha

### 2.3 Operativna posljedica
- Drži C1 odluku iz handoff-a (`api_epredmet.py` brisanje) — **proširi** odlukom **da se nikad ne vraća**
- U `MONETIZACIJA/04_CJENOVNI_MODEL.md` ne planiraj značajke koje se oslanjaju na e-Predmet podatke

---

## 3. Sudski registar — POSTOJEĆA prilika

### 3.1 Stanje
**`api_sudreg.py` već postoji** u repo-u (provjereno 2026-04-27, 138 LOC):
- OAuth2 client_credentials grant
- REST API base: `https://sudreg-data.gov.hr/api/javni`
- Token caching u `st.session_state`
- TTL cache 1h (`@st.cache_data(ttl=3600)`)
- `pretrazi_subjekt(oib, mbs)` već radi
- `render_sudreg_lookup(prefix)` UI helper

### 3.2 Licencni status
- **Otvoreni podaci** preko `data.gov.hr` portala
- **CC-BY licenca** (Open License HR ekvivalent)
- **Komercijalna uporaba dozvoljena** uz atribuciju izvora
- **Besplatna registracija** za API ključ (`sudreg-data.gov.hr`)

### 3.3 GDPR perspektiva
Sudski registar sadrži:
- Pravne osobe (d.o.o., j.d.o.o., dionice, zaklade) — **nisu osobni podaci u smislu GDPR**
- Zastupnici i vlasnici su navedeni kao "organi pravne osobe" — granični GDPR slučaj
  - GDPR čl. 4(1) — *physical person identifiable* — ima
  - ALI: kontekst je javno službeno objavljivanje radi pravne sigurnosti (analogno UK Companies House) → zakonita osnova **legitimni interes javnosti** + tijelo već publicira

**Praktična procjena**: Sudski registar je **najsigurniji izvor** podataka za HR legal SaaS. AZOP do danas (2026-04) nema rješenja koja kažnjavaju komercijalnu uporabu Sudskog registra.

### 3.4 Operativna posljedica
1. **Registriraj se na `sudreg-data.gov.hr`** — besplatno, treba e-mail
2. **Dodaj credentials u Streamlit secrets**: `sudreg_client_id` + `sudreg_client_secret`
3. **Verifikaciju komercijalne uporabe**: pošalji email na `sudski.registar@pravosudje.hr` s upitom **"je li komercijalni SaaS korištenje API-ja podlježe posebnoj licenci ili registraciji"** — dobiti pisano potvrdu prije launch-a
4. **Atribucija u UI-u**: footer pravila "Podaci o subjektima Sudskog registra dohvaćeni preko `sudreg-data.gov.hr` (CC-BY licenca, Ministarstvo pravosuđa, uprave i digitalne transformacije RH)"

---

## 4. Narodne novine — STATUS QUO

`api_nn.py` koristi ELI/JSON-LD endpoint. NN su:
- Službeni tekstovi (zakoni, odluke) — **nisu predmet autorskog prava** (ZAPSP čl. 8)
- Otvoreni podaci, dokumentirani API
- Nema osobnih podataka u zakonima

**Akcija**: nikakva. Modul radi i pravno je čist.

---

## 5. AZOP DPIA — što treba učiniti

### 5.1 Pravna podloga
GDPR čl. 35 + AZOP-ov objavljen popis tipova obrade za koje je DPIA obvezna ([AZOP](https://azop.hr/odluka-o-uspostavi-i-javnoj-objavi-popisa-vrsta-postupaka-obrade-koje-podlijezu-zahtjevu-za-procjenu-ucinka-na-zastitu-podataka/)).

### 5.2 Procjena za LegalTech Suite Pro

| Kriterij | Primjenjivost | Razlog |
|---|---|---|
| Velika obrada osobnih podataka | **DA** | OIB-ovi korisnika (kao stranke u dokumentima) + suprotnih strana + zastupnika |
| Sustavni nadzor javno dostupnih područja | NE | Nema video/lokacijski tracking |
| Profiliranje s pravnim učinkom | **GRANIČNO** | Bez automatskog odlučivanja, ALI generirani dokumenti imaju pravni učinak (tužba, ovrha) |
| Cross-referencing baza | **DA** | NN + Sudreg + interni korisnik podaci u jednom dokumentu |
| Automatizirano odlučivanje | NE | Korisnik ručno odabire + uređuje |
| Posebne kategorije podataka | **GRANIČNO** | Kazneni postupci kazneno (kategorija čl. 10 GDPR) — generator `kazneno.py` |

**Verdict**: DPIA je **obvezan** prije profesionalne komercijalne uporabe. Nije obvezan za solo dev fazu jer obrada nije "u značajnom volumenu", ali ulaskom u plaćeni model (Faza 2) postaje obvezan.

### 5.3 Praktični DPIA workflow

**Faza 0 (sada — sljedeća sesija)**: pripremi DPIA template
1. Skini AZOP službeni obrazac s [azop.hr/dpia](https://azop.hr/procjena-ucinka-na-zastitu-podataka-eng-data-protection-impact-assessment-dpia/)
2. Popuni:
   - Voditelj obrade: TI (kao d.o.o. nakon Faze 1) ili kao fizička osoba dotad
   - Izvršitelj obrade: Streamlit Cloud + Polar.sh + Supabase + Hetzner (kasnije)
   - Kategorije podataka: identifikacijski (OIB, ime), kontaktni (email), pravni (predmet, pristojba)
   - Kategorije ispitanika: korisnici proizvoda + suprotne strane u dokumentima
   - Svrhe: izrada pravnih dokumenata, audit chain za forenziku, billing
   - Razdoblje čuvanja: zakonski (10 god za računovodstvo, 5 god za audit chain prema procesnom zakonu)
3. Risk assessment + measures (već imaš dosta — entitlements, audit_chain, hash chain)

**Faza 2**: registriraj u AZOP-u (DPIA prijava obvezna ako risk score "high")

### 5.4 Voditelj obrade — kritičan trenutak

**Sada**: si fizička osoba (Hrvoje Matej Lešić) — pravna odgovornost je **na tebi osobno**.

**Nakon Faze 1**: prebaci sve na **j.d.o.o.** kao voditelja obrade. To te štiti od osobne odgovornosti za AZOP kazne (do 20M EUR ili 4% globalnog prometa).

**Streamlit Cloud + Polar.sh + Supabase = izvršitelji obrade** — treba:
- DPA (Data Processing Agreement) potpisan s svakim
- Streamlit Cloud DPA: dostupan na [streamlit.io/legal](https://streamlit.io/legal)
- Polar.sh DPA: dostupan u onboarding flow-u
- Supabase DPA: dostupan na [supabase.com/legal/dpa](https://supabase.com/legal/dpa)

---

## 6. Konsolidirana akcija za sljedeću sesiju

```bash
# 1. Ukloni e-Oglasna scraper iz roadmap-a (otkazi C2)
git rm api_eoglasna.py stranice/eoglasna.py
# ili refaktor stranice/eoglasna.py u outbound-link placeholder

# 2. Verificiraj api_sudreg.py kao primarni HR pravni izvor
#   - Registriraj se na sudreg-data.gov.hr
#   - Pošalji email sudski.registar@pravosudje.hr za komercijalnu licencu
#   - Dodaj atribuciju u footer

# 3. Pokreni AZOP DPIA template
#   - Download s azop.hr
#   - Popuni za fazu 0/1
#   - Drži kao .pdf u MONETIZACIJA/dpia/
```

**LOC dirne**: -300 (api_eoglasna.py + stranice/eoglasna.py refaktor) + 0 (api_sudreg.py već radi)
**Vrijeme**: ~2-3 sata (vs ~4-6h za neispravan C2 port)
**Pravni rizik**: čisto.

---

## 7. Reference

- e-Oglasna robots.txt: dohvaćeno 2026-04-27 — `User-agent: *` permisivan
- e-Oglasna politika privatnosti: dohvaćeno 2026-04-27 — citat o tehničkim zaštitama
- e-Oglasna "O e-Oglasnoj": MPUDT je voditelj, sudovi nadležni
- Sudski registar API: [sudreg-data.gov.hr](https://sudreg-data.gov.hr/) + [data.gov.hr CC-BY](https://www.data.gov.hr/cesto-postavljana-pitanja)
- AZOP DPIA: [azop.hr/dpia](https://azop.hr/procjena-ucinka-na-zastitu-podataka-eng-data-protection-impact-assessment-dpia/)
- e-Predmet: [mpudt.gov.hr](https://mpudt.gov.hr/vijesti/e-predmet-javni-i-besplatni-pristup-osnovnim-podacima-sudskih-predmeta/158) (samo web)
- KZ čl. 266 (neovlašteni pristup): NN 125/11, 144/12, 56/15, 61/15, 101/17, 118/18, 126/19, 84/21, 114/22, 114/23, 36/24
- ZAPSP čl. 149-156 (sui generis): NN 111/21
- CJEU Ryanair v PR Aviation (C-30/14)
- CJEU Innoweb v Wegener (C-202/12)
- CJEU Manni (C-398/15)
