# 01 — PRAVNI OKVIR

> **Pročitaj ovo prvo.** Bez ispravnog pravnog statusa ne možeš zakonito naplaćivati, niti će ti Lemon Squeezy isplatiti novac.
>
> Ovaj dokument **nije pravni savjet** — to je orijentacijski sažetak. Za konkretnu situaciju, idi knjigovođi (paušalni obrt = oko 30-50 EUR/mj knjigovođe).

---

## 1. ZAŠTO TI UOPĆE TREBA POSEBNI STATUS

U Hrvatskoj **fizička osoba ne smije primati ponavljajuće prihode iz djelatnosti** bez registriranog statusa (obrt, slobodno zanimanje, ili tvrtka). Jednokratno može — npr. prodaš vlastiti rabljeni laptop. Ali kad **redovito** primaš novac za uslugu, to je djelatnost.

Ako primaš novac na svoj osobni račun bez registracije, dvije stvari mogu poći krivo:
1. **Porezna te otkrije** preko bankovnih izvoda → kazna + plaćanje svih neuplaćenih doprinosa unatrag.
2. **Lemon Squeezy zatraži dokaze o pravnom statusu** prije isplate. Bez registracije — tvoj novac ostaje kod njih i nikad ti ga ne pošalju.

---

## 2. ŠTO REGISTRIRATI — TRI OPCIJE

### Opcija A: PAUŠALNI OBRT (preporučeno za početak)

**Što je to:** najjednostavniji oblik registrirane samostalne djelatnosti. Ne vodiš knjigovodstvo prihoda i rashoda — porez plaćaš **paušalno** (fiksni iznos po razredu prihoda), bez obzira što si stvarno potrošio.

**Trošak mjesečno (2026.):**
- Doprinosi (mirovinsko + zdravstveno): **oko 220-280 EUR/mj**
- Paušalni porez: **oko 25-100 EUR/mj** ovisno o godišnjem prihodu
- Knjigovođa (opcionalno ali preporučeno): **30-50 EUR/mj**
- **Ukupno: oko 280-430 EUR mjesečno**

**Razredi prihoda (paušalni porez ovisi o tome u kojem si):**
| Razred | Godišnji prihod (EUR) | Paušalni godišnji porez |
|--------|----------------------|-------------------------|
| 1 | do 11.945 | 1.218 EUR |
| 2 | 11.945 - 17.918 | 1.827 EUR |
| 3 | 17.918 - 23.890 | 2.435 EUR |
| 4 | 23.890 - 47.780 | 4.870 EUR |

(Iznosi orijentacijski, u 2026. mogu biti malo drukčiji — provjeri kod knjigovođe.)

**Maksimalni prihod kao paušalist:** oko 47.780 EUR/godinu. Ako prijeđeš to → moraš preći na "obrt s knjigovodstvom" (opcija B).

**Kako registrirati:**
1. **Online preko e-Građani / e-Obrt** (https://e-obrt.gov.hr) — možeš sve riješiti od kuće
2. Ili u Gradskom uredu za gospodarstvo (po mjestu prebivališta)
3. Treba ti: OIB, osobna iskaznica, **šifra djelatnosti** (za tebe je relevantna **62.01 — Računalno programiranje** ili **63.11 — Obrada podataka**)
4. Naziv obrta: nešto poput "**LegalTech Suite, obrt za računalno programiranje, vl. Hrvoje Matej**"
5. Otvaraš **poslovni račun u banci** (NE smiješ koristiti osobni za prihode iz obrta). Najjeftinije: **Erste Direkt** ili **Revolut Business** (free tier postoji)

**Vrijeme:** registracija 1-3 radna dana. PDV identifikacijski broj (ako ti zatreba) još tjedan dana.

### Opcija B: OBRT S KNJIGOVODSTVOM (kasnije, kad rasteš)

Ako prijeđeš 47k EUR/god. ili želiš odbijati troškove (kupnja računala, internet, edukacije...) — prelaziš na ovo. Skuplje za knjigovodstvo (80-150 EUR/mj) ali plaćaš porez **stvarno** prema dobiti, a ne paušalno.

### Opcija C: J.D.O.O. (jednostavno društvo s ograničenom odgovornošću)

**Trošak osnivanja:** ~150 EUR (kapital 10 HRK = ~1,33 EUR + javnobilježničke pristojbe)
**Mjesečni trošak:** sličan obrtu, ali knjigovodstvo je obavezno (~80-150 EUR/mj)
**Prednost:** ako tužitelj dođe — odgovaraš samo imovinom firme, ne osobnom.
**Mana:** veća birokracija, kompliciranije isplaćivanje sebi (dividenda + porez na dividendu).

**Preporuka:** počni s **paušalnim obrtom**. Ako za godinu dana imaš stabilno 3-4k EUR/mj prihoda i počneš zapošljavati nekoga ili surađivati s većim klijentima → razmisli o j.d.o.o.

---

## 3. PDV (POREZ NA DODANU VRIJEDNOST)

Ovo je **najveći hedache** za solo programere koji prodaju u EU.

### Kratko objašnjenje

PDV je porez koji se zaračunava krajnjem kupcu. U Hrvatskoj je 25%. **Ali** — kada prodaješ **digitalnu uslugu** (a aplikacija je digitalna usluga) **fizičkoj osobi u drugoj EU zemlji**, mora se naplatiti **PDV te zemlje** (njemački 19%, austrijski 20%, francuski 20%, švedski 25%...).

Postoje **dva sustava** za to:

#### Sustav 1: OSS (One-Stop-Shop)
Registriraš se u **Hrvatskoj** za OSS. Skupljaš PDV po stopama svih EU zemalja. Kvartalno popunjavaš jedinstvenu prijavu i šalješ Poreznoj. Oni dalje raspodjeljuju.

**Problem:** moraš znati koja zemlja je kupac, pratiti sve cijene s PDV-om po zemlji, izdavati račune po njihovim pravilima, čuvati 10 godina dokumentaciju. **Solo developer to ne može sam.**

#### Sustav 2: MERCHANT OF RECORD (rješenje)

**Lemon Squeezy postaje pravno prodavač krajnjem korisniku.** Korisnik plaća Lemon Squeezyju, ne tebi. Lemon Squeezy se brine za PDV u svakoj zemlji. Ti **prodaješ Lemon Squeezyju** (B2B unutar EU = 0% PDV-a, samo prijaviš na PDV prijavi kao "isporuka unutar EU").

**Što ti to znači praktično:**
- Krajnji kupac dobiva račun od **Lemon Squeezy** (s logom Lemon Squeezy + svojim podacima kao "prodavač")
- Ti dobivaš **mjesečnu isplatu** od Lemon Squeezy (npr. "ukupno 1.247,30 EUR za travanj 2026.")
- Lemon Squeezy ti šalje **summary račun** koji ti predaješ knjigovođi
- Ti samo prijavljuješ jednu B2B transakciju mjesečno = puno jednostavnije

**Trošak:** 5% + 0,50 EUR po transakciji. Ako naplatiš 19,99 EUR mjesečnu pretplatu → Lemon Squeezy zadrži 1,50 EUR (5% = 1 EUR + 0,50 EUR fee), tebi dolazi 18,49 EUR.

**Isplati li se:** **DA, apsolutno.** Računaj koliko vrijedi tvojih 50 sati godišnje + glavobolja s OSS-om. Tih 5% je puno jeftinije.

### Hrvatski PDV prag

Ako je tvoj **godišnji promet u Hrvatskoj** ispod **40.000 EUR**, ne moraš biti u sustavu PDV-a u HR. Ali za prodaju u EU preko OSS-a — OSS pragovi su drugi, počinju od 10.000 EUR ukupno EU prodaje.

**S Lemon Squeezyjem ovo te ne tiče** jer LS je MoR — ti si njihov dobavljač, ne kupcima direktno.

---

## 4. GDPR (ZAŠTITA OSOBNIH PODATAKA)

GDPR je EU regulativa koja kaže: ako sakupljaš osobne podatke (email, ime, IP adresu) građana EU, **moraš poštovati pravila**. Kazne su ogromne (do 4% godišnjeg prometa ili 20 milijuna EUR), ali za solo developera realno: kazne se uglavnom dogode kad ima ozbiljan curenje podataka i netko prijavi.

### Što minimalno moraš imati

#### A) Privacy Policy (Politika privatnosti)

Stranica na tvojoj aplikaciji koja jasno kaže:
- **Koje podatke** sakupljaš (email, ime, sadržaj generiranih dokumenata?)
- **Zašto** ih sakupljaš (za prijavu, naplatu, slanje računa)
- **Tko ima pristup** (Supabase, Lemon Squeezy)
- **Koliko dugo ih čuvaš** (npr. 7 godina za račune zbog zakona o računovodstvu, ostalo dok korisnik ne traži brisanje)
- **Kako korisnik može tražiti brisanje** (email s "želim biti obrisan/a" → ti to napraviš u Supabase u 1 minuti)

**Kako napraviti:** koristi besplatni generator **termly.io** ili **freeprivacypolicy.com**. Popuniš formu, generira ti tekst, ti ga zalijepiš u app.

#### B) Terms of Service (Uvjeti korištenja)

Slično, ali za pravila igre:
- "Aplikacija ne predstavlja pravni savjet"
- "Generirani dokumenti su predlošci, korisnik ih koristi na vlastiti rizik"
- "Pretplata se obnavlja automatski osim ako se ne otkaže 24h prije obnove"
- "U slučaju spora nadležan je sud u Zagrebu"

**Ovo je BITNO za tebe** — bez disclamer-a "nije pravni savjet" izlažeš se tužbi ako netko tvojom tužbom izgubi spor jer si negdje stavio krivi članak zakona.

#### C) Cookie banner

Ako koristiš kolačiće (a Streamlit ih koristi za session) — moraš pitati za pristanak. Najlakše: **Cookiebot** ima besplatnu razinu za male sajtove, ili napraviš jednostavan banner u Streamlit aplikaciji ("Slažem se" gumb).

#### D) Data Processing Agreements (DPA)

Supabase i Lemon Squeezy automatski potpisuju DPA s tobom kad otvoriš račun (uvjet je u njihovim ToS). Treba ih pohraniti. **Nije tvoja briga aktivno.**

---

## 5. SPECIFIČNO ZA TVOJU APLIKACIJU — RIZIK NADRIPISARSTVA

Ovo je **kritično za tebe**, jer aplikacija generira pravne dokumente.

**Zakon o odvjetništvu, čl. 72.** zabranjuje "nadripisarstvo" — pružanje pravnih usluga ako nisi odvjetnik. Kazna: do **9.300 EUR** + zatvor do 1 godine za teže slučajeve.

### Što SMIJEŠ
- Ponuditi **alat za izradu predložaka** koje korisnik **sam popunjava** ✅
- Imati biblioteku obrazaca, kao što imaju knjižare ✅
- Naplaćivati pristup softveru (kao Microsoft Office) ✅

### Što NE SMIJEŠ
- Pisati dokumente **za** druge ljude uz naplatu ❌
- Davati pravne savjete ("u tvom slučaju trebaš podnijeti tužbu") ❌
- Pozicionirati se kao "zamjena za odvjetnika" ❌
- Tvrditi "garantirano dobiješ spor" ili sl. ❌

### Praktično — što napiši na sajtu

U Footer / Privacy Policy / Terms:

> **LegalTech Suite Pro je softverski alat za izradu pravnih dokumenata. Aplikacija ne pruža pravnu pomoć niti pravne savjete u smislu Zakona o odvjetništvu. Generirani dokumenti su predlošci koje korisnik samostalno popunjava i koristi na vlastiti rizik. Za konkretne pravne situacije preporučujemo savjetovanje s odvjetnikom.**

To te štiti od nadripisarstva i od tužbi krajnjih korisnika ("Vaš predložak nije bio dobar pa sam izgubio spor").

---

## 6. RAČUNOVODSTVENE OBVEZE PAUŠALNOG OBRTA

Iako je "paušalni" — i dalje moraš:

1. **Voditi knjigu prometa** (KPI obrazac) — jednostavna evidencija svake naplate. Knjigovođa ti to radi za 30-50 EUR/mj.
2. **Izdavati račune** — za digitalne usluge preko Lemon Squeezy ovo radi LS umjesto tebe (oni izdaju kupcima). Ti samo izdaješ **JEDAN račun mjesečno LEMON SQUEEZYJU** za njihov payout. Knjigovođa ti to napravi.
3. **Godišnja prijava (DOH)** — do 28. veljače sljedeće godine za prošlu. Knjigovođa.
4. **Mjesečna PDV prijava** — ako si u sustavu PDV-a (vidi gore). Inače ne.

**Zaključak:** sve sa solidnim knjigovođom = **30-50 EUR/mj**. Ne pokušavaj sam. Greška u prijavi = kazna.

---

## 7. PREPORUČENI REDOSLIJED (PRIJE TEHNIKE)

```
TJEDAN 1: Razgovor s knjigovođom (besplatno, prvi sastanak je orijentacija)
          → odluči: paušalni obrt vs j.d.o.o.

TJEDAN 2: Online registracija obrta na e-Obrt portalu
          → otvori poslovni bankovni račun (paralelno)

TJEDAN 3: Dođe rješenje, dobiješ OIB obrta i poslovni IBAN
          → otvori Lemon Squeezy račun s tim podacima
          → naruči pečat (legalna obveza za obrte)

TJEDAN 4: Pripremi Privacy Policy + Terms (preko termly.io)
          → otvori Supabase
          → krene tehnička implementacija (sljedeći dokumenti)
```

---

## TIPIČNI PROBLEMI

**"Nemam pojma koju šifru djelatnosti odabrati"**
→ **62.01 (Računalno programiranje)** kao glavna. Možeš dodati i **63.11 (Obrada podataka)** i **70.22 (Savjetovanje u vezi s poslovanjem)** kao dodatne. Knjigovođa pomaže.

**"Trebam li biti u sustavu PDV-a?"**
→ Ako ostaješ ispod 40k EUR/god. domaćeg prometa **i** koristiš Lemon Squeezy (MoR) → ne moraš. Provjeri s knjigovođom.

**"Lemon Squeezy traži W-8BEN ili sličan obrazac"**
→ To je za američke porezne svrhe. Popuniš da nisi američki porezni rezident, slobodno bez američkog poreza. Standardno.

**"Mogu li raditi obrt uz redovni posao?"**
→ Da, **dopunska djelatnost**. Doprinosi su tada manji jer ih dijelom već plaćaš preko poslodavca. Posebna kategorija paušalca, javi knjigovođi.

**"Što ako ne želim otvoriti obrt nikad — ima alternativa?"**
→ Možeš prodati cijelu aplikaciju (vidi razgovor o asset-sale i royalty modelu) i pustiti da netko drugi nosi pravni status. To je razlog zašto sam u prošlom razgovoru i predložio prodaju kao plan B.

---

## SLJEDEĆI KORAK

Otvori `02_ARHITEKTURA.md` da vidiš **kako sve dijelovi tehnički zajedno funkcioniraju**, prije nego ulaziš u praktičnu izradu.
