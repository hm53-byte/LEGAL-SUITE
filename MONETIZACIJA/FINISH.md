# FINISH — Pre-launch checklist + studentska prava + doktorat

> **Datum**: 2026-04-27
> **Svrha**: Konsolidirani checklist svega što treba prije prvog plaćajućeg korisnika + pravna struktura koja štiti studentske beneficije
> **Status**: Glavni operativni dokument — referenca za sve sljedeće sesije

---

## DIO I — Pre-launch checklist

> Što mora biti gotovo prije nego prvi euro može legalno teći.

### 🔴 KRITIČNO (bez ovoga ne ide)

#### Pravna struktura
- [ ] **j.d.o.o. otvoren** preko START platforme — MBS, OIB pravne osobe (Faza 1, ~5-10 radnih dana)
- [ ] **HR IBAN business** otvoren (Erste Mojo / PBZ / Zaba) — uplata TK 1.250 €
- [ ] **Računovodstveni servis** ugovoren (~150-200 €/mj)
- [ ] **HZZO + HZMO aktivirani za direktora** — VAŽNO: direktor NIJE Hrvoje Matej dok studira (vidi Dio II)
- [ ] **DPA-ovi potpisani**: Streamlit, Supabase, Polar, Hetzner (kasnije)
- [ ] **DPIA finalizirana** — AZOP obrazac popunjen, spremljen u repo

#### Pravna dokumentacija (UI)
- [ ] **Uvjeti korištenja** (T&C) — disclaimer "alat, ne pravna usluga"
- [ ] **Politika privatnosti** — voditelj obrade, izvršitelji, razdoblje čuvanja, prava ispitanika
- [ ] **Cookie banner** + cookie politika (analytics, session)
- [ ] **Atribucija Sudski registar API** — CC-BY u footer-u
- [ ] **Anti-nadripisarstvo disclaimer** vidljiv pri svakom dokumentu (footer dokumenta)
- [ ] **AZOP konzultacija** (besplatni Help-Desk) — pisana potvrda da je obrada zakonita

#### Plaćanja (Polar.sh)
- [ ] **Polar account aktivan** (KYC submitted, account approved)
- [ ] **Stripe → Polar migracija** code (~345 LOC, vidi `GOAT/PREPORUKA_MOR.md`)
- [ ] **Sandbox testing** kompletan — webhook, refund, subscription create/cancel
- [ ] **Polar live mode** prebacen
- [ ] **Webhook secret rotacija** — security baseline
- [ ] **Cancellation flow** self-service u app-u

#### Tehnička sigurnost
- [ ] **Sve API ključeve** u Streamlit Secrets (nikad u git-u)
- [ ] **2FA** uključeno na: GitHub, Streamlit, Supabase, Polar, Hetzner, banka
- [ ] **Backup Supabase Pro** daily (25 $/mj, kad pređe 500 audit chain zapisa)
- [ ] **HTTPS** automatic (Streamlit Cloud daje, OK)
- [ ] **Supabase regija** = EU (Frankfurt/Ireland) — provjeri prije launch-a

### 🟡 VAŽNO (radi ozbiljnost)

#### Proizvod
- [ ] **Watermark logika** za FREE tier — `watermark.py` + conditional aktivacija
- [ ] **Tier limit** za FREE (5 dok/mj rolling) — `entitlements.py`
- [ ] **Pricing page** s 3 tier-a (FREE / PRO 9€ / STUDIO 29€)
- [ ] **Email verifikacija** obvezna pri signupu
- [ ] **Landing page copy** — bez "AI", bez "zamjena za odvjetnika", bez maglovitog "pravna pomoć"
- [ ] **Welcome email** — kratak, bez bait-framing-a, link na vodič
- [ ] **Pravopis + padeži review** cijele aplikacije — LanguageTool lokalno (`pip install language_tool_python`) za sve `.py` + `.md` fajlove; Hascheck (FER) kao backup za sumnjive dijelove; Word/LibreOffice spell-check na ~10 random generiranih `.docx` primjera kao final QA. Posebno provjeriti runtime padeže (`_padez_uloge`, `_padez_ime`, `u_lokativu`) s nestandardnim imenima (strana, ženska s `-ić`).

#### Brand & komunikacija
- [ ] **Vlastita domena** kupljena (`legalsuite.hr` ili sl. preko CARNet)
- [ ] **Business email** s d.o.o. domenom (Zoho Mail Free)
- [ ] **Support email** aktivan + odgovor unutar 48h SLA
- [ ] **Logo + minimum brand identity** (Figma free, ili ~500 € designer)
- [ ] **Favicon** + social card slika

#### Operativno
- [ ] **eRačun rješenje** — FINA Moj eRačun (free) ili Helena (5-15 €/mj) — obvezno od PDV obveze
- [ ] **Sentry error tracking** (free tier) — vidiš production errore u realnom vremenu
- [ ] **Better Stack uptime monitoring** (free) — alert kad app padne
- [ ] **Plausible/Umami analytics** (privacy-friendly, EU rezidentno)

#### Customer support setup
- [ ] **FAQ stranica** (10-15 najčešćih pitanja)
- [ ] **Refund policy** napisana (14 dana garancija, HR Zakon o zaštiti potrošača)
- [ ] **Cancellation message** — "što smo mogli bolje" survey

### 🟢 PREPORUČA SE (skida trenje, ne blokira launch)

- [ ] **Onboarding wizard** prvih 5 min (već imaš `_render_vodic`)
- [ ] **5-10 SEO blog članaka** spremnih za drip-objavu (Faza 1-2)
- [ ] **LinkedIn profil** updated kao Founder
- [ ] **3-5 friends&family beta** koji već koriste i daju feedback
- [ ] **Cold outreach lista** (50 odvjetnika, kasnije NPL agencija) za post-launch
- [ ] **Press kit** (one-pager + screenshoti) za eventualne medije

### ⏰ TIMELINE — što kada

| Tjedan | Faza | Aktivnost |
|---|---|---|
| **T 1-2** | Faza 0 | Cleanup (✅ done 2026-04-27), Sudreg validacija, DPIA draft, domena research |
| **T 3-4** | Faza 1 | j.d.o.o. otvaranje, IBAN, knjigovodstvo, domena |
| **T 5-7** | Faza 2 | Polar migracija + KYC + DPA + DPIA finaliziran |
| **T 8** | Faza 2 | Pravni dokumenti UI (T&C, Privacy, Cookie) |
| **T 9** | Faza 2 | Watermark, tiers, pricing page, brand polish |
| **T 10** | Faza 2 | Sandbox testing, friends&family beta |
| **T 11** | Faza 2 | Polar live, F&F u live, monitoring |
| **T 12** | LAUNCH | LinkedIn announce, prvih 5-10 platežnih usera |

**Ukupno**: **~10-12 tjedana** od 2026-04-27 do prvog naplaćenog €.

### ⚠️ Što NE PROPUSTITI

Tri stvari koje će ugristi ako ih preskočiš:

1. **DPIA + AZOP konzultacija** — prije live mode-a. Bez toga prvi AZOP upit te može potopiti.
2. **Anti-nadripisarstvo disclaimer** — u svakom dokumentu, jasan, vidljiv. HOK pristup je sustavan, jedan njihov pregled tvojeg landing page-a može pokrenuti prijavu.
3. **DPA s vendorima** — bez potpisanih DPA-a si u GDPR breach od dana 1. Većina ih ima online, samo treba klik kroz Streamlit/Supabase/Polar dashboard.

---

## DIO II — Studentska prava + d.o.o. struktura

> Pravna struktura koja štiti tvoja studentska prava dok pokreneš biznis.

### TL;DR — preporuka

**NE budi direktor dok studiraš.** Drugi netko (roditelj, član obitelji, prijatelj kojem vjeruješ) bude direktor. Ti si **100 % vlasnik**, dobit primaš kao **dividendu (12 % porez)**, studentska prava ostaju netaknuta.

### Ključna razlika: vlasnik vs direktor

| Tvoja uloga u d.o.o. | Studentska prava | SC ugovor | Doprinosi mjesečno |
|---|---|---|---|
| **Samo član društva (vlasnik), nisi direktor** | ✅ ZADRŽAVAŠ | ✅ SMIJEŠ raditi | ❌ 0 € |
| **Direktor + član društva (TI sam vodiš)** | ⚠️ Djelomično | ❌ NE SMIJEŠ | ⚠️ ~200-400 € razlika osnovice (ili ~700-900 € puna minimalka) |

### Detaljna razrada

#### 1. Vlasnik (član društva) ≠ Direktor

HR pravo razlikuje **dvije uloge**:
- **Član društva** = vlasnik udjela ("investor"). Pasivna pozicija. Bez radnog odnosa, bez obvezne registracije u HZMO/HZZO, **bez doprinosa**.
- **Direktor (član uprave)** = osoba koja vodi društvo. Aktivna funkcija. Po **Zakonu o doprinosima čl. 21**, ako nije osiguran po drugoj osnovi, postaje obvezno osiguran s minimalnom osnovicom **888,67 €/mj (2026)**.

**Možeš biti vlasnik 100 % udjela d.o.o.-a a da netko drugi bude direktor.** Legalno i uobičajeno.

#### 2. Studentsko zdravstveno osiguranje

**Redoviti student do 26 god** ima zdravstveno osiguranje preko:
- Roditelja (kao član obitelji), ili
- Statusa redovitog studenta (HZZO osiguranik)

**Gubiš to ako**: imaš drugu obveznu osnovu osiguranja (npr. zaposlen ili obvezno osiguran kao direktor).

**Ne gubiš to ako**: si samo član društva bez direktorske funkcije (pasivni investor).

#### 3. Studentski servis (SC ugovor)

SC pravila eksplicit isključuju studente koji:
- Imaju **uspostavljen radni odnos**, ili
- Obavljaju **samostalnu djelatnost** (obrt, profesija)

**Vlasništvo nad d.o.o.-om NIJE samostalna djelatnost** — d.o.o. je pravna osoba, ti si njen vlasnik (ne djelatnik).

**Direktorska funkcija JEST samostalna djelatnost** → gubiš pravo na SC.

#### 4. Dividenda kao prihod studenta

- **Dohodak od kapitala (dividenda)** = 12 % porez, jedinstvena stopa
- **NIJE u limitu od 4.800 €/god** (taj se odnosi samo na SC ugovore ako roditelj koristi povećani osobni odbitak)
- **ALI**: ako roditelj koristi povećani osobni odbitak, godišnja porezna prijava može imati implikacije — provjeri s računovodstvenim servisom prije prve isplate

### 5. Konkretna struktura

**j.d.o.o. setup**:
- **Osnivač / član društva (100 %)**: Hrvoje Matej Lešić
- **Direktor**: roditelj/sibling/pouzdani prijatelj — **bez naknade dopušteno** (volonterski direktor)
- **Operativno**: ti vodiš sav razvoj, marketing, podršku — direktor samo formalno potpisuje ugovore (preko punomoći ili specifičnih ovlasti)
- **Banka**: direktor otvara IBAN, ali ti dobijaš ovlast za upravljanje računom (joint signatory)

**Što dobijaš:**
- ✅ Studentska zdravstvena prava (do 26 god)
- ✅ SC ugovori (možeš raditi preko studentskog servisa)
- ✅ Roditelj zadržava povećani osobni odbitak (do 4.800 €/god od SC-a)
- ✅ Dividenda iz d.o.o.-a (oporeziva 12 %, ne ulazi u SC limit)
- ✅ Pravna zaštita (d.o.o. = ograničena odgovornost, GDPR voditelj obrade nije ti osobno)

**Što ne dobijaš:**
- ❌ Ne možeš sam potpisivati u ime društva (treba ti direktorov potpis)
- ❌ Ako želiš mjesečnu plaću iz d.o.o.-a, moraš biti zaposlen u d.o.o.-u → ali to ujedno pokreće doprinose i status

### 6. Kad prebaciti se u direktora

**Trigger**: nakon **diplome** (ili završetka studija). Tada studentske beneficije ionako prestaju, a direktorska funkcija postaje normalan trošak.

**Praktični savjet**: trajanje studija = horizont u kojem zadržavaš ovu strukturu.

### 7. Tri pitanja koja moraš razjasniti prije j.d.o.o.

1. **Tko će biti direktor?** Roditelj? Brat? Pouzdani prijatelj?
   - Volonterski (bez plaće) je dopušteno
   - Mora razumjeti što potpisuje (ugovori, KYC, banka)

2. **Kako ćeš operativno upravljati?**
   - Joint signatory na business IBAN
   - Punomoć od direktora za specifične akcije (Polar.sh signup, ugovori)
   - Operativa kroz tebe, formalni potpisi kroz direktora

3. **Provjera s računovođom** (Faza 0 task 0.8): pitaj eksplicit ovo pitanje. Servisi rade sa studentima-osnivačima često i znaju nijanse.

### Update plan dokumenata

`MONETIZACIJA/02_PRAVNA_STRUKTURA.md` treba ispravke u sljedećoj sesiji:
- "Direktor: Hrvoje Matej Lešić, sole director" → **"Direktor: TBD (ne korisnik dok studira)"**
- Sekcija "Mjesečni operativni trošak" → ako direktor je volonter bez plaće, fiksni mjesečni trošak je manji (~150-200 €/mj samo knjigovodstvo + banka, bez ~700-900 € direktorske plaće)

**Unit economics impact**: break-even pada s ~13.500 €/god na **~3.000 €/god** → Faza 2 puno realističnija za solo dev.

---

## DIO III — Doktorski studij — tri scenarija

> Studentska prava produžuju se ako upišeš doktorat, pod uvjetima koji ovise o tipu doktorskog studija.

### Tri tipa doktorskog studija u HR

| Tip | Zaposlen? | Plaća studij? | SC ugovor | Zdravstveno preko fakulteta |
|---|---|---|---|---|
| **A) Redoviti doktorand (bez asistenture)** | NE | Sam ili stipendija | ✅ DA | ✅ DA (do 8 god ukupno kao student) |
| **B) Doktorand-asistent (suradničko zvanje)** | DA, na fakultetu | Fakultet ili sam | ❌ NE (radni odnos) | ✅ DA (preko zaposlenja) |
| **C) Izvanredni doktorand** | Najčešće DA, drugdje | Sam | ✅ DA | ❌ NE (preko poslodavca ili sam) |

### Implikacije za d.o.o. strukturu

#### Scenarij A: redoviti doktorand bez asistenture
**Identično kao trenutno** — preporučena struktura ostaje:
- Ti si vlasnik 100 %, netko drugi je direktor
- SC ugovori i dalje mogući
- Zdravstveno preko fakulteta
- Dividenda 12 % iz d.o.o.-a

**Trajanje pokrivenosti**: 8 god ukupno kao redoviti student (preddiplomski + diplomski + doktorat zbrojeno). Provjeri svoju studentsku povijest.

#### Scenarij B: doktorand-asistent (financijski najpametniji za d.o.o.)
- Asistent = **zaposlen na fakultetu** s plaćom (~1.000-1.300 € neto/mj 2026)
- Zdravstveno + mirovinsko se plaća **kroz fakultet** kao primarna osnova osiguranja
- **MOŽEŠ biti direktor d.o.o.-a** uz dodatak: plaća se samo **razlika osnovice** (prosječna plaća × 0.65 ≈ ~570 € baza minus to što već plaća fakultet) → dodatak je **~50-150 €/mj**, ne pune ~700-900 €
- ✅ Stalan prihod od fakulteta
- ✅ Obvezno osiguranje preko zaposlenja
- ✅ D.o.o. operativno (kao direktor) financijski izvediv
- ❌ Gubiš SC (već si zaposlen)

**Rijedak scenarij gdje d.o.o. + akademska karijera idu zajedno bez velikog kompromisa.**

#### Scenarij C: izvanredni doktorand
- Imaš drugi posao izvan fakulteta
- Studij plaćaš sam (~1.000-3.000 €/god ovisno o fakultetu)
- SC ugovori i dalje formalno mogući
- Zdravstveno **NE** preko fakulteta — moraš imati svoju osnovu

**Za d.o.o.**:
- Ako imaš drugi posao → struktura slična kao Scenarij B (drugi posao = osnova osiguranja)
- Ako d.o.o. je tvoj jedini biznis i moraš biti direktor → puni doprinosi (~700-900 €/mj)

### Otvorena pitanja za korisnika

1. **U kojoj si trenutno godini studija?** (1.-5.)
2. **Planiraš li polagati pravosudni ispit** nakon diplome?
3. **Ako doktorat — A, B ili C scenarij?**

### Strateška preporuka

**Ako još razmatraš doktorat → drži strukturu fleksibilnom**: vlasnik 100 %, ne direktor.

Time čuvaš opciju oba puta (akademski i biznis):
- Ako kasnije odeš na asistenturu (Scenarij B), prebaciš se u direktora bez velikog troška
- Ako ne (Scenarij A ili C), struktura ostaje
- Ako uopće ne ideš na doktorat — direktorska konverzija nakon diplome

### Doktorat + LegalTech SaaS = sinergija

Za pravnika je doktorat strateški izbor — omogućava:
- **Akademska karijera**: asistent → docent → izvanredni profesor → redoviti profesor
- **Predavanja na fakultetu**
- **Expert witness u kompleksnim sporovima** (~150-300 €/h)
- **Specijalizacija u nišama** (npr. pravo umjetne inteligencije, GDPR — što idealno paše uz LegalTech projekt)

**Tvoj proizvod stiče kredibilitet, akademska karijera dobija realan tehnološki "field test".**

---

## DIO IV — Sljedeći koraci

### Što SAD treba napraviti (Faza 0 nedovršeni task-ovi)

Iz `06_MILESTONES.md`:
- [ ] **0.3** — Registracija na `sudreg-data.gov.hr` + credentials u Streamlit secrets (~1h)
- [ ] **0.4** — Email upit `sudski.registar@pravosudje.hr` (~15 min)
- [ ] **0.5** — Provjera Supabase regije (~5 min)
- [ ] **0.6** — DPIA template populacija (~2-3h)
- [ ] **0.7** — HR domena WHOIS check (~1h)
- [ ] **0.8** — Računovodstvene ponude (~2h) — **uključi pitanje o studentskoj strukturi**

### Što treba odlučiti prije Faza 1

1. **Tko će biti direktor j.d.o.o.-a** (roditelj? brat? prijatelj?)
2. **Doktorat — A, B ili C scenarij** (ili odluka o odgodi)
3. **Naziv tvrtke** (provjeri dostupnost u sudskom registru)
4. **Naziv domene** (`legalsuite.hr`, `legalsuite.com.hr`, drugi predlog)

### Ažuriranja u sljedećoj sesiji

- [ ] `MONETIZACIJA/02_PRAVNA_STRUKTURA.md` — direktor: TBD, ne ti
- [ ] `MONETIZACIJA/06_MILESTONES.md` — Faza 1 task 1.6 ("Direktor — TBD"), task 1.10 ("Računovodstveni servis — pitanje o studentskoj strukturi")
- [ ] `MONETIZACIJA/04_CJENOVNI_MODEL.md` — break-even revidiran (~3k€/god umjesto ~13.5k€/god)

---

## Reference

### Pravni okvir
- [Zakon o doprinosima čl. 21 (član uprave)](https://www.zakon.hr/z/365/zakon-o-doprinosima)
- [HZZO — tko su osigurane osobe](https://hzzo.hr/obvezno-zdravstveno-osiguranje-0/tko-su-osigurane-osobe-hzzo)
- [TEB — zdravstveno osiguranje redovitih studenata](https://www.teb.hr/novosti/2020/zdravstveno-osiguranje-redovnih-ucenika-i-studenata/)
- [HZZO — redovni studenti i nakon 26. godine](https://www.iusinfo.hr/aktualno/dnevne-novosti/hzzo-redovnim-studentima-zdravstveno-osiguranje-i-nakon-26-godine-17038)

### Studentski servis
- [Studentski centar Zagreb — informacije](https://www.sczg.unizg.hr/student-servis)
- [Studentski centar Zagreb — porezni limiti 2026](https://www.sczg.unizg.hr/informacije/studentske-zarade-limiti)
- [Moja Firma — student rad 2026](https://mojafirma.hr/clanci/rad-studenata-studentski-ugovor-2026)

### Status studenta
- [Sveučilište J. Dobrile Pula — FAQ status studenta](https://www.unipu.hr/studenti/faq/status_studenta)
- [Sveučilište u Zadru — poslijediplomski studiji](https://www.unizd.hr/studiji-i-studenti/studentska-referada/poslijediplomski-studiji/studiranje)

### Drugo
- `MONETIZACIJA/README.md` — orkestrator masterplana
- `MONETIZACIJA/02_PRAVNA_STRUKTURA.md` — detaljnija razrada (treba ažuriranje)
- `MONETIZACIJA/06_MILESTONES.md` — faze 0-4 s decision gate-ovima
- `GOAT/PREPORUKA_MOR.md` — Polar.sh kao MOR

---

## Audit log

| Datum | Promjena | Razlog |
|---|---|---|
| 2026-04-27 | Inicijalna izrada | Korisnik tražio finalni dokument koji konsolidira pre-launch checklist + studentska prava + doktorske scenarije |
