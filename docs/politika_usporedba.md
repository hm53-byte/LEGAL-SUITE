# Politika privatnosti: presuda o spremnosti za objavu

**Datum ocjene**: 9. kolovoza 2026.
**Ocijenjeni dokument**: `stranice/privacy_policy.md`, zatečeno stanje v1.1,
nakon ove ocjene v1.2.
**Popratni dokument**: `stranice/tos.md`, v1.0 od 27. travnja 2026.

## Kako je ocjena napravljena

Svaka tvrdnja iz politike uspoređena je s izvornim kodom u repozitoriju, a ne s
namjerom ili s dokumentacijom. Gdje se tvrdnja i kod razilaze, mjerodavan je kod.
Uz to je politika uspoređena s tri vanjska mjerila:

1. **Obvezni elementi** koje AZOP nabraja na svojoj stranici o informiranju
   ispitanika i u svom obrascu politike privatnosti (obrazac 03/2024).
2. **Objavljena rješenja AZOP-a** u kojima je politika privatnosti bila jedna od
   utvrđenih povreda.
3. **Politike privatnosti konkurentskih generatora dokumenata**, domaćih i
   stranih, kao mjerilo tržišne prakse.

Rečeno je i što se nije moglo utvrditi. Popis je na kraju dokumenta.

---

## 1. Presuda

**Dokument ne smije van kao završena politika privatnosti, jer bez imena
voditelja obrade i bez kontaktne adrese ne obavlja svoju funkciju. Ali inačica
koja je već javna gora je od ove, pa je objava ovog teksta popravak, a
zadržavanje starog je nastavak štete.**

Te dvije rečenice nisu u suprotnosti i razlika je važna za redoslijed poteza.
Vidi odjeljak 7.

---

## 2. Što nedostaje, poredano po cijeni

Poredak je po tome što se dogodi ako stavka ostane kakva jest, ne po tome koliko
teksta treba napisati.

### 2.1 Identitet voditelja obrade i kontaktna adresa

**Gdje**: članak 1. (šest polja) i članak 13. (jedno polje).

Bez toga dokument ne ispunjava GDPR čl. 13. st. 1. t. (a) i (b), i nijedno pravo
iz članka 6. nije ostvarivo, jer nema adrese na koju bi se zahtjev poslao. Ovo je
jedini nedostatak koji sam po sebi znači da tekst nije politika privatnosti nego
predložak politike privatnosti.

**Cijena**: dokument ne funkcionira. Sve ostalo u njemu je bespredmetno dok ovo
stoji prazno.

### 2.2 Politika se korisniku nikad ne prikazuje

**Gdje**: u aplikaciji, ne u dokumentu. Zabilježeno je u članku 2.1 i u napomeni
uz datum stupanja na snagu.

Provjereno u kodu: u zadanom načinu rada (`LEGAL-SUITE.py`, redci 119 do 124)
korisnik se automatski prijavljuje kao gost i prijavna se stranica uopće ne
prikazuje. Obrazac za registraciju (`auth.py`, redci 290 do 319) nema kućicu za
prihvaćanje uvjeta ni poveznicu na ovaj dokument. Pretraga cijelog koda za bilo
kakvim korakom prihvaćanja nije vratila nijedan pogodak. Dokument je dostupan
samo ako korisnik sam otvori stranicu "Pravila i privatnost".

GDPR čl. 13. st. 1. traži da se informacije daju **u trenutku prikupljanja**
podataka. Registracija prikuplja ime, adresu e-pošte i lozinku, a da dokument ni
ne spomene.

**Cijena**: obveza informiranja nije ispunjena ni za jednog korisnika, uključujući
one koji su se već registrirali. Ovo se ne popravlja pisanjem, nego izmjenom
aplikacije.

**Riješeno 10.8.2026., djelomično.** Aplikacija je izmijenjena: novi modul
`privatnost.py` daje jednu kratku obavijest o obradi koja se prikazuje na svakom
mjestu unosa osobnih podataka, uključujući prijavu i registraciju, prije ijednog
polja. Obuhvaćena je 21 datoteka; mjesta su utvrđena čitanjem koda, a ne popisom
koji bi netko održavao rukom.

Test to drži tako da AST-om skenira `stranice/*.py` i `auth.py`, prepozna svaku
datoteku s poljem za slobodan unos i traži poziv obavijesti. Nova stranica s
unosom pada bez ijedne izmjene testa. Da test nije tautologija dokazano je
dodavanjem sintetičke stranice: test pada, pa se stranica ukloni.

**Što time nije riješeno:** prihvaćanje se i dalje ne traži; kratka obavijest ne
pokriva primatelje, prijenos izvan EGP-a ni kolačiće nego za to upućuje na
politiku; a voditelj obrade i kontakt i dalje nisu upisani, pa obavijest ne
ispunjava čl. 13. st. 1. t. (a) i (b) dok se ta polja ne popune. Uz to, u kalendar
se može upisati tuđa adresa e-pošte, a ta osoba i dalje ne dobiva obavijest po
čl. 14.; obavijest od takvog unosa sada odvraća, što nije isto što i obavijestiti
tu osobu.

### 2.3 Rok čuvanja za `stripe_events` nije određen

**Gdje**: članak 7., tablica, redak `stripe_events`.

Tablica sadrži cjelovit zapis događaja plaćanja s adresom e-pošte kupca
(članak 2.6). Politika za nju kaže da rok nije određen i da automatskog brisanja
nema.

To je točno ono stanje koje je AZOP sankcionirao u dva objavljena predmeta:

| Predmet | Utvrđeno | Kazna |
|---|---|---|
| Specijalna bolnica, KLASA UP/I-034-01/24-01/23, 21.8.2024. | "Specijalna bolnica nije propisala internim aktima rokove čuvanja takvih osobnih podataka", povreda čl. 5. st. 1. t. (e) | 190.000 EUR ukupno, za sedam povreda |
| Hrvatski ured za osiguranje, prema Godišnjem izvješću AZOP-a za 2025. | "HUO nije zasebno propisao maksimalne rokove čuvanja osobnih podataka" | 101.000 EUR |

**Cijena**: jedina stavka u dokumentu koja se doslovno poklapa s izrekom objavljene
odluke. Traži broj, a broj može dati samo vlasnik.

### 2.4 Mehanizam za prijenos izvan EGP-a nije naveden

**Gdje**: članak 5., odlomak "Prijenos izvan EGP-a".

U ovoj je ocjeni sama činjenica prijenosa napisana jednoznačno (bilo je "može se
odvijati", vidi odjeljak 5). Ono što i dalje nedostaje jest odgovor na pitanje po
kojem se pravnom mehanizmu iz poglavlja V GDPR-a prijenos odvija: standardne
ugovorne klauzule, odluka o primjerenosti, ili nešto treće.

GDPR čl. 13. st. 1. t. (f) traži da se navede i mehanizam i način na koji
ispitanik može doći do primjerka zaštitnih mjera.

**Cijena**: polovica obveznog elementa. Sama izjava o prijenosu bez mehanizma
priznaje prijenos i ne opravdava ga.

### 2.5 Ugovori o obradi po čl. 28 nisu potvrđeni

**Gdje**: članak 5., odlomak "Ugovori o obradi".

Iz repozitorija se ne vidi je li s ijednim pružateljem sklopljen ugovor o obradi.
Za usporedbu, domaći konkurent Pravomat (QMind d.o.o.) u svojoj politici imenuje
svakog izvršitelja punim nazivom i adresom i za Google izričito navodi da je
ugovor o obradi sklopljen.

U rješenju protiv B2 Kapitala AZOP je uz povredu čl. 13. st. 1. utvrdio i povredu
čl. 28. st. 3., u istom postupku, uz ukupnu kaznu od 2.265.000 eura.

**Cijena**: nije samo dokumentacijska. Ako ugovori ne postoje, obrada preko tih
pružatelja nema uređenu osnovu, neovisno o tome što piše u politici.

### 2.6 Puni podaci o primateljima

**Gdje**: članak 5., tablica.

Tablica imenuje pružatelje, ali nema adrese, registracijske brojeve, a za dva
pružatelja ni pouzdan naziv pravne osobe (vidi odjeljak 4.3). Pravomatova
politika za svakog izvršitelja navodi puni naziv i adresu.

**Cijena**: srednja sama po sebi, ali se zbraja s 2.5: bez naziva pravne osobe ne
može se ni provjeriti s kim bi ugovor o obradi trebao biti sklopljen.

### 2.7 Podjela uloga voditelj/izvršitelj za odvjetnika koji radi za klijenta

**Gdje**: nedostaje u cijelom dokumentu. Povod je `tos.md`, članak 6.1.

Uvjeti korištenja izričito dopuštaju "generiranje dokumenata u ime klijenta uz
uvjet da Korisnik ima ovlaštenje (npr. odvjetnik za svoje klijente)". To je
klasičan odnos u kojem je korisnik voditelj obrade, a Davatelj izvršitelj, barem
za dio podataka. Politika Davatelja tretira kao voditelja obrade za sve
(članak 1.).

Pravomat isto pitanje rješava izričitom podjelom u čl. 5. svoje politike i
zasebnim Ugovorom o obradi podataka koji korisnik mora prihvatiti.

**Cijena**: veliko ako se članak 6.1 Uvjeta zadrži, jer pogađa upravo skupinu
korisnika koju Uvjeti izričito predviđaju. Malo ako se ta odredba ukloni.
Neizbježno je odabrati jedno.

### 2.8 Obavještavanje treće osobe čija adresa uđe u kalendar

**Gdje**: članak 2.5, sada dodana točka 3.

Polje "Email za podsjetnik" (`stranice/kalendar.py`, redci 226 do 227) prima bilo
koju adresu. Ako korisnik upiše tuđu, ta osoba postaje ispitanik, a od Davatelja
ne dobiva nikakvu obavijest. GDPR čl. 14. uređuje upravo taj slučaj.

Zatečeni tekst je istovremeno upozoravao da se tuđe adrese ne upisuju i opisivao
polje koje ih prima. Upozorenje ne uklanja obvezu.

**Cijena**: mala dok kalendar koristi malo ljudi, ali obveza postoji od prvog
unosa.

### 2.9 Rok vezan uz prestanak odnosa

**Gdje**: članak 7., tablica, redci za račun i za dokumentaciju o plaćanju.

Tablica nema nijedan rok koji teče od prestanka odnosa. Juro (Juro Online
Limited) taj rok ima i obrazlaže ga: šest godina nakon prestanka svojstva
korisnika, "in case there are any legal claims relating to your time as a
customer".

**Cijena**: srednja. Bez toga se ne zna kad podaci bivšeg korisnika prestaju
postojati.

### 2.10 Elementi koji su ovom ocjenom dodani

Sljedeće je nedostajalo i sada je upisano. Navedeno je radi zapisa, ne kao
otvorena stavka:

| Element | Osnova | Gdje je sada |
|---|---|---|
| Automatizirano donošenje odluka i profiliranje | GDPR čl. 13. st. 2. t. (f), obvezni element po popisu AZOP-a | novi članak 3.1 |
| Je li davanje podataka obveza i posljedice nedavanja | GDPR čl. 13. st. 2. t. (e), obvezni element po popisu AZOP-a | novi članak 3.2 |
| Rok od mjesec dana uz produljenje do dva mjeseca | GDPR čl. 12. st. 3., traži i AZOP-ov obrazac | članak 6., uvod |
| Provjera identiteta podnositelja zahtjeva | GDPR čl. 12. st. 6., traži i AZOP-ov obrazac | članak 6., uvod |
| Povlačenje privole ne dira raniju obradu | GDPR čl. 7. st. 3., traži i AZOP-ov obrazac | članak 6.6 |
| Način priopćavanja bitnih izmjena | Smjernice o transparentnosti, t. 29 do 31 | članak 12. |

Prije ovoga u dokumentu nije postojala **nijedna rečenica** o automatiziranom
donošenju odluka, ni potvrdna ni niječna. To je provjereno pretragom: pojmovi
"automatiz" i "profil" u zatečenoj datoteci nisu se pojavljivali.

### 2.11 Kontakt AZOP-a i podaci o službeniku za zaštitu podataka

**Gdje**: članak 6.7 i članak 1., redak DPO.

AZOP-ov obrazac traži da se navedu adresa sjedišta, e-pošta i telefon AZOP-a te
poveznica na www.azop.hr. U dokumentu stoji samo poveznica.

U rješenju protiv specijalne bolnice AZOP je kao zasebnu povredu (čl. 38. st. 1.)
utvrdio da službenica za zaštitu podataka nije bila uključena u izradu politike
privatnosti ni u propisivanje rokova čuvanja. Kod nas se iz praznog polja ne može
utvrditi ni postoji li službenik.

**Cijena**: mala pojedinačno, ali su oba obvezni elementi.

---

## 3. Što je viška: obećanja koja mehanizam ne pokriva

Ovo je vrsta greške koja je već jednom popravljana (obećano brisanje nakon 24
mjeseca bez posla koji bi ga izvodio). Pretraženo je ostalo li još takvih mjesta.

### 3.1 Ostalo je, i ovo su

| Obećanje | Gdje | Što stvarno postoji |
|---|---|---|
| Zahtjev za presliku podataka (čl. 15) obrađuje se ručno | članak 6.1 | Nema postupka, nema skripte, nema zapisa tko prima zahtjev. Podaci su raspoređeni u `.users.json`, `_data/kalendar.json` i, kad proradi, u bazi; nema ničega što ih spaja |
| Prenosivost, isporuka kao JSON (čl. 20) | članak 6.4 | Isto. Nema izvoza ni u kodu ni u skriptama |
| Ispravak podataka na zahtjev (čl. 16) | članak 6.2 | Ručna izmjena datoteke na poslužitelju koji se pri ponovnom pokretanju vraća na početno stanje. Politika sama kaže da ekrana za izmjenu nema |
| Obavijest AZOP-u o povredi u roku od 72 sata | članak 10. | Nema evidencije pristupa, nema praćenja, nema postupka. Aplikacija ne bilježi ni IP ni User-Agent (članak 2.7), pa Davatelj nema iz čega utvrditi da je do povrede došlo |
| Brisanje računa na zahtjev roditelja | članak 11. | Isti ručni kanal, uz istu prazna kontaktnu adresu |

Nijedno od tih obećanja nije neistinito kao izjava o namjeri. Sva su neprovjerljiva
kao izjava o postojećem mehanizmu. Razlika prema kažnjenom slučaju FAVBET-a
(175.000 eura) je u tome što je ondje politika obećavala pravo na zaborav dok je
brisanje bilo tehnički nemoguće. Ovdje je ručno brisanje moguće, samo nije
uređeno.

**Što s tim**: za brisanje postupak postoji i opisan je u
`docs/brisanje_podataka.md`. Za pristup, ispravak i prenosivost ne postoji.
Najjeftiniji popravak nije mijenjati politiku nego napisati te tri stranice
uputa, kao što je već napravljeno za brisanje.

### 3.2 Popravljeno u ovoj ocjeni

- **"Davatelj dobiva samo potvrdu da je pretplata aktivna"** (članak 2.6) bilo je
  u izravnom proturječju s popisom tri retka iznad, koji kaže da se sprema
  cjelovit zapis događaja s adresom e-pošte kupca. To je manja inačica greške za
  koju je sportska kladionica dobila 380.000 eura: u politici je pisalo da se
  brojevi kartica ne pohranjuju, a pohranjivali su se. Ovdje kartica doista ne
  ulazi, ali "samo potvrdu" je govorilo manje nego što se prima. Ispravljeno.
- **"Stripe ... EU (Irska)"** (članak 5.) bila je tvrdnja o mjestu obrade koju
  repozitorij ne potkrepljuje. Sjedište ugovorne strane i mjesto obrade nisu isto.
  Ispravljeno.
- **Zaštita na razini retka** (članci 4. i 10.) bila je napisana kao činjenica o
  sadašnjem stanju. Vidi odjeljak 4.1.

---

## 4. Što je netočno: provjera tvrdnji uz kod

### 4.1 Nalazi koji ranije nisu bili zabilježeni

**(a) Zaštita na razini retka ne štiti nikoga, jer se nitko ne prijavljuje na
bazu.**

Pravila u `cloud/supabase_schema.sql` (redci 125 do 138) glase
`USING (user_id = auth.uid())`. `auth.uid()` popunjava Supabaseova prijava.
Aplikacija Supabaseovu prijavu ne koristi: `entitlements.py` čita
`st.session_state["_supabase_jwt"]` i `st.session_state["_user_id"]`, a pretraga
cijelog koda pokazuje da te dvije vrijednosti **nitko nigdje ne postavlja**.
Posljedica je da je `auth.uid()` prazan, pa nijedno pravilo nikome ne odobrava ni
čitanje ni upis.

Zatečeni tekst članka 4. tvrdio je: "prijavljeni Korisnik može čitati i unositi
samo vlastite retke". Takvog korisnika nema. Ispravljeno: pravilo je odvojeno od
stanja u kojem to pravilo nikome ništa ne odobrava.

**(b) Tablica `stripe_events` nema zaštitu na razini retka.**

`cloud/supabase_schema.sql`, redak 115: "stripe_events NEMA RLS". Članak 10.
tvrdio je bez ograde da je zaštita na razini retka mjera zaštite podataka u bazi.
Za tu tablicu, koja sadrži adrese e-pošte kupaca, to ne vrijedi; do nje se dolazi
samo servisnim ključem. Ispravljeno.

**(c) Shema baze predviđa upravo ono što politika izričito niječe.**

Politika u članku 2.2 tvrdi da se datum zadnje prijave ne pohranjuje, a u članku
2.3 da se trajni identifikator Google računa (`sub`) ne prima i ne pohranjuje.
Obje su tvrdnje **danas točne**. Ali `cloud/supabase_schema.sql` za tablicu
računa definira stupce `last_login_at` (redak 31) i `oauth_subject` (redak 28).

Ista ta shema je preduvjet za sve što politika opisuje kao buduće stanje:
zapisivanje preuzimanja (članak 2.4) ne može proraditi dok se prijava ne poveže s
bazom. Drugim riječima, dokument upućuje vlasnika na korak nakon kojeg dvije
njegove apsolutne niječne tvrdnje prestaju biti točne.

To je obrazac iz predmeta EOS Matrix, gdje je politika tvrdila da se zdravstveni
podaci ne obrađuju, a bilježili su se u bazu (ukupno 5.470.000 eura, najviši
iznos u hrvatskoj praksi). Dodano upozorenje u oba članka.

**(d) Zadani način rada zaobilazi prijavnu stranicu.**

Politika je u članku 2.1 opisivala gumb "Isprobaj besplatno" kao ulaz. U zadanom
načinu rada (`LEGAL-SUITE.py`, redci 119 do 124) tog gumba nema, jer se prijavna
stranica ne prikazuje. Ispravljeno.

**(e) Aplikacija u sučelju tvrdi da je politika starija nego što jest.**

`stranice/pravila.py`, redci 39 do 48, ispisuje traku: "Status: nacrt v1.0
(2026-04-27)". Dokument ispod te trake je v1.2 od 9.8.2026. Korisniku se
istovremeno prikazuje kriv datum i kriva inačica. Ovo je izmjena u kodu i nije
napravljena u ovoj ocjeni jer je izvan zadanog opsega. **Traži se popravak.**

**(f) Komentar u migraciji proturječi ispravku iz članka 7.1.**

`cloud/0008_retencija_download_log.sql`, redci 26 do 27, i dalje tvrdi:
"current_hash je sazetak nad sazetcima i bez ta tri ulazna polja se ne moze
ponovno izracunati". Politika je tu tvrdnju već ispravila u v1.1: od pet ulaza tri
nisu tajna, a preostala dva dobiva svatko tko ima i dokument i podatke koji su u
njega uneseni. Komentar u SQL-u treba uskladiti s člankom 7.1.

### 4.2 Provjera trinaest ranije nađenih neispravnosti

Sve su provjerene uz kod. Nijedna nije ostala neispravljena u politici. Popis
provjera, s izvorom:

| Tvrdnja politike | Provjereno u | Ishod |
|---|---|---|
| Računi u `.users.json`, ne u bazi | `auth.py`:14, 43 do 60 | Točno |
| Pohranjuju se ime, e-pošta, sažetak lozinke, datum, uloga | `auth.py`:311 do 316 | Točno |
| Datum zadnje prijave se ne pohranjuje | `auth.py`:177, samo `session_state` | Točno danas, vidi 4.1(c) |
| Google `sub` se ne prima | `auth.py`:120, uzima se samo `email` i `name` | Točno danas, vidi 4.1(c) |
| Prijava Appleom ne završava uspješno | `auth.py`:130 do 143, postoji URL, nema obrade odgovora | Točno |
| `download_log` ostaje prazan | `entitlements.py`:246 do 248, `current_user_id()` je uvijek `None` | Točno |
| Serijski broj se računa s oznakom `guest` | `watermark.py`:140, `docx_export.py`:571 | Točno |
| Serijski broj u podnožju i u metapodacima, u oba tiera | `watermark.py`:141 poziva se uvijek | Točno |
| Sadržaj dokumenta se ne pohranjuje | `docx_export.py`:588 do 592, gradi se u `BytesIO`, na disk se ne piše | Točno |
| IP i User-Agent se ne obrađuju | pretraga cijelog koda za `user-agent`, `remote_ip`, `x-forwarded`, `st.context` bez pogotka | Točno |
| Nema kolačića za praćenje | pretraga za `gtag`, `google-analytics`, `pixel`, `matomo`, `plausible`, `posthog` bez pogotka | Točno |
| Kalendar je zajednički, datoteka je privremena | `stranice/kalendar.py`:19 do 55 | Točno |
| Pražnjenje `download_loga` nije aktivno | `cloud/0008_...sql` postoji, ali `pg_cron` posao nije potvrđen ni na jednoj bazi | Točno, i dalje označeno |

Uz to je provjereno da opis pražnjenja u članku 7.1 odgovara migraciji do stupca:
`0008_retencija_download_log.sql`, redci 147 do 159, prazni točno onih devet
stupaca koje politika nabraja i ostavlja `generated_at`, `parent_hash`,
`current_hash`, uz `anonymized_at` i internu oznaku retka. Poklapa se.

### 4.3 Tvrdnje koje se iz repozitorija ne mogu provjeriti

- **Naziv pravne osobe koja pruža hosting.** Politika je navodila "Streamlit Inc.".
  Streamlit je 2022. preuzet od strane Snowflakea, pa je pitanje tko je ugovorna
  strana za Streamlit Community Cloud otvoreno. U ovoj je ocjeni tvrdnja o nazivu
  uklonjena, a ne zamijenjena drugom, jer točan naziv nije provjeren na izvoru.
- **Naziv pravne osobe iza Polar.sh.** Politika je navodila "Polar Software Inc.".
  Nije provjereno.
- **Regija Supabase projekta.** Nije poznata. `cloud/SETUP.md` predlaže Frankfurt,
  ali prijedlog u uputama nije dokaz o odabiru.
- **Postoje li sigurnosne kopije i koliko se čuvaju.** Nije poznato. Bitno je jer
  o tome ovisi kad obrisani podatak stvarno nestane (članak 6.3).
- **Koji SMTP pružatelj se koristi.** Kod ga čita iz postavki
  (`stranice/kalendar.py`:62 do 65) i ne otkriva ga.

---

## 5. Jezik

### 5.1 Mjerilo

Smjernice o transparentnosti (WP260 rev.01, t. 12 i 13, str. 8 do 10) traže
izbjegavanje kvalifikatora "može", "možda", "neki", "često", "moguće", i nalažu
da voditelj obrade, ako nejasan jezik ipak koristi, mora moći dokazati zašto ga
nije mogao izbjeći.

AZOP je to primijenio dvaput s izrečenom kaznom:

- Specijalna bolnica: "intencija navedene odredbe je da se izbjegnu nejasne
  rečenične formulacije (npr. može) koje mogu ispitanicima ostaviti prostora za
  razna tumačenja". Formulacija "ovaj razgovor može biti sniman" umjesto "ovaj
  razgovor se snima" ocijenjena je povredom čl. 12. st. 1.
- Teleoperator: ograde tipa "možda će se osobni podaci dijeliti u treće zemlje"
  i "u pravilu unutar EU, a samo iznimno izvan" ocijenjene povredom čl. 12. st. 1.,
  uz ukupnu kaznu od 4.500.000 eura.

### 5.2 Ocjena razumljivosti

Dokument je razumljiv. Pisan je kratkim rečenicama, u drugom licu prema
korisniku, s objašnjenjima uz svaki tehnički pojam, i nema pravničkih fraza koje
bi laik morao prevoditi. Članak 7.1, koji objašnjava zašto se zapis ne briše nego
prazni, napisan je s primjerom i s posljedicom za korisnika. To je iznad razine
koju ima većina uspoređenih politika.

**Razumljivost nije zamjerka.** Zamjerka je bila u ogradama.

### 5.3 Ograde: koje su uklonjene, a koje ostaju s razlogom

Uklonjeno u ovoj ocjeni:

| Bilo | Sada | Zašto |
|---|---|---|
| "obrada se može odvijati izvan EU" (članak 5.) | "Prijenos izvan EGP-a: da, odvija se" | Doslovno konstrukcija koju je AZOP kaznio kod teleoperatora |
| "obrada se ne odvija nužno unutar EU" (Cloudflare, članak 5.) | "Cloudflareova globalna mreža, koja ima poslužitelje i izvan EGP-a" | Isto |
| "Korisnik koji nastavi koristiti Aplikaciju prihvaća izmjene" (članak 12.) | Izričito se navodi da nastavak korištenja nije prihvaćanje bitne izmjene | Smjernice, t. 29 do 31 |

Ostaje, i to je obrazloženo u samom dokumentu:

| Ograda | Gdje | Zašto se ne može ukloniti |
|---|---|---|
| "račun može nestati" pri ponovnom pokretanju | članak 2.2 | Stvarna neizvjesnost. Ponovno pokretanje ovisi o pružatelju hostinga i ne događa se po rasporedu. Rečenica koja bi tvrdila "račun nestaje" bila bi netočna, jer ne nestaje uvijek |
| "brisanje ne djeluje trenutačno na sigurnosne kopije" | članak 6.3 | Rok čuvanja kopija nije poznat (odjeljak 4.3). Ograda je posljedica nepoznanice koju vlasnik može ukloniti |
| "zapisi prometa mogu još postojati" | članak 7.1 | Rokovi pružatelja nisu poznati i Davatelj na njih ne utječe |

Prve dvije ograde nestaju kad vlasnik popuni podatke. Treća je stvarna i za nju
Smjernice t. 13 traže upravo ovo: dokumentiran razlog zašto se ne može izbjeći.
Razlog je u dokumentu naveden.

### 5.4 Jedna stilska primjedba koja nije pravna

`stranice/tos.md` koristi crticu em na četiri mjesta, `privacy_policy.md` ni na
jednom. Dva dokumenta prikazuju se jedan pored drugoga, u dvije kartice iste
stranice. Nije zamjerka po GDPR-u.

---

## 6. Sedam praznih polja `<<< VLASNIK UPISUJE: ... >>>`

### 6.1 Što se točno događa pri objavi

Prvo činjenično stanje, jer mijenja pitanje:

- Repozitorij `https://github.com/hm53-byte/LEGAL-SUITE` **je već javan**
  (provjereno 9.8.2026., odgovor 200).
- `stranice/privacy_policy.md` **je već u njemu**, u inačici 1.0 od 27.4.2026.
- Inačica 1.1 postoji samo lokalno: grana `main` je ispred `origin/main` za jedan
  commit.
- `stranice/pravila.py` prikazuje **cijelu datoteku** korisniku, uključujući
  oznake i uvodnu napomenu. Prazna polja nisu skrivena od korisnika ni sada.

Pitanje dakle nije hoće li prazna polja postati javna. Pitanje je hoće li ostati
javna uz stari tekst ili uz novi.

### 6.2 Prazna polja nasuprot izmišljenim vrijednostima

**Prazna polja su bolja i nije blizu.**

Prazno polje govori istinu: podatak nije upisan. Čitatelj vidi da dokument nije
dovršen i ne izvodi iz njega zaključak koji bi bio netočan. Nedostaje mu obvezni
element iz čl. 13. st. 1. t. (a) i (b), što je propust.

Izmišljena vrijednost stvara **drugu** vrstu problema, tešku:

1. Netočan naziv ili OIB znači da dokument imenuje krivu osobu kao voditelja
   obrade. Ispitanik koji na temelju toga podnese zahtjev ili pritužbu obraća se
   krivoj adresi.
2. Izmišljena adresa e-pošte za GDPR zahtjeve je adresa koja ne prima poštu.
   Politika tada obećava kanal koji ne postoji, što je isti obrazac zbog kojeg je
   ova ocjena i napravljena.
3. Upisati "Ne imenuje se DPO" bez provjere je izjava o pravnoj obvezi koja se
   nije ispitala.

Kod EOS Matrixa i kod sportske kladionice AZOP nije kaznio prazninu, nego
**netočnu tvrdnju**. U oba je predmeta politika govorila nešto što nije bilo
istina. Prazno polje ne govori ništa; izmišljeno polje govori neistinu.

**Zaključak**: polja se popunjavaju točnim podacima ili ostaju prazna. Trećeg
puta nema.

### 6.3 Zašto se šest od sedam polja može popuniti odmah

Ista javna riznica u datoteci `LICENSE` navodi: "Copyright (c) 2026 Hrvoje Matej.
Sva prava pridržana." Nositelj prava na softveru nije nužno isto što i voditelj
obrade, ali podatak o tome tko stoji iza aplikacije **već je javan u istom
repozitoriju**. Razlog za nepopunjavanje polja "Naziv" zato nije zaštita
identiteta, jer identitet nije zaštićen.

Preostaje stvarno pitanje, i ono nije tehničko: nastupa li vlasnik kao fizička
osoba, obrt ili trgovačko društvo. O tome ovisi i OIB, i adresa sjedišta, i to
je odluka koju ova ocjena ne može donijeti.

---

## 7. Usporedba: gdje smo bolji, gdje slabiji

### 7.1 Bolji

| Stavka | Kod nas | Kod usporedivih |
|---|---|---|
| Pohrana sadržaja dokumenta | Ne pohranjuje se. Datoteka se gradi u memoriji i predaje korisniku (provjereno u kodu) | Rocket Lawyer izričito pohranjuje i podatke unesene u obrazac i uređene dokumente, bez navedenog roka: "we collect and store the information you enter in the course of generating or editing your document ... as well as your edited documents" |
| Brisanje korisničkih podataka | Na zahtjev | Rocket Lawyer: "Rocket Lawyer will not delete customer information other than upon customer request. However, Rocket Lawyer reserves the right to delete customer information for members with a free account status at any time" |
| Priznavanje onoga što ne radi | Pet mjesta označeno oznakom [NIJE AKTIVNO], uz objašnjenje što treba da proradi | Nije nađeno ni kod jednog uspoređenog pružatelja |
| Objašnjenje što se iz zadržanog sažetka još može saznati | Članak 7.1 to izlaže s posljedicom za korisnika | Nije nađeno ni kod jednog uspoređenog pružatelja |

Prva stavka nije standard tržišta nego stvarna razlika, i najveći konkurent u
istoj kategoriji radi suprotno. To se u dokumentu sada izričito kaže (članak 2.4).

### 7.2 Slabiji

| Stavka | Kod nas | Kod usporedivih |
|---|---|---|
| Raspored čuvanja po vrsti podatka | Jedna brojka (24 mjeseca za `download_log`), ostalo bez roka ili s kriterijem vezanim uz radnju korisnika | Legal Templates ima zaseban članak 18 s rokom za svaku kategoriju: račun bez plaćanja 6 mjeseci, plaćeni 24 mjeseca uz obavijest i 30 dana za reaktivaciju, financijski zapisi 7 godina, podrška 3 godine, analitika 36 mjeseci |
| Rok od zahtjeva do brisanja | Nema ga zasebno; vrijedi opći rok od mjesec dana | Gavel: sedam dana nakon otkaza računa, uz izričite iznimke |
| Rok vezan uz prestanak odnosa | Nema | Juro: šest godina nakon prestanka svojstva korisnika, s obrazloženjem |
| Podaci o izvršiteljima | Nazivi bez adresa; za dva pružatelja ni naziv nije potvrđen | Pravomat: puni naziv i adresa za svakog, uz tvrdnju o sklopljenom ugovoru o obradi |
| Ugovor o obradi za poslovne korisnike | Nema ga | Pravomat ima zaseban Ugovor o obradi s rokovima (14 dana za prigovor na podizvršitelja, 90 dana za preuzimanje podataka nakon prestanka) |
| Rezidentnost podataka | Prijenos izvan EGP-a se odvija, mehanizam nije naveden | Pravomat tvrdi poslužitelje u RH, EU ili EGP-u. Clio ima zasebnu datiranu stranicu podizvršitelja s lokacijom po dobavljaču |
| Naziv i trajanje pojedinog kolačića | Tri skupine, bez naziva i bez konkretnog trajanja kolačića trećih strana | AZOP je u rješenju o kolačićima (20.000 eura) izričito tražio skupine, vrste, funkciju i svrhu svakog kolačića te razdoblje pohrane |

Zanimljiva podudarnost: Legal Templates za plaćene račune koristi **isti postupak
i istu brojku** kao naša politika: "After 24 months without logging in, your
personal information is pseudonymized and your document content is deleted".
Kod nas je isti izbor obrazložen iznutra, lancem sažetaka. Da je tržišno uobičajen,
dosad se nije znalo.

---

## 8. Redoslijed poteza

Presuda iz odjeljka 1 razlaže se ovako.

### Odmah, prije svega ostalog

1. **Objaviti ovu inačicu.** Javna inačica 1.0 tvrdi da se zapisi u `download_log`
   nakon 24 mjeseca brišu cron poslom. Takav posao nikad nije postojao. Dok taj
   tekst stoji vani, javno objavljena politika obećava brisanje koje se ne
   provodi. U rješenju protiv B2 Kapitala AZOP je kao otegotnu okolnost izričito
   naveo da "politika privatnosti ostala je nepromijenjena te povreda još nije
   otklonjena". Trajanje je otegotno, a ono se broji od danas.

   Ovo nije objava završenog dokumenta. To je zamjena neistinite tvrdnje
   označenim nacrtom. Oznake [NIJE AKTIVNO] i [VLASNIK POTVRĐUJE] i uvodna
   napomena moraju ostati, jer one su ono što tekst čini poštenim.

### Prije nego se uključi bilo koja neaktivna funkcija

2. Popuniti sedam polja iz članka 1. i 13.
3. Odrediti rok za `stripe_events`.
4. Utvrditi i upisati mehanizam prijenosa izvan EGP-a.
5. Provjeriti i upisati stanje ugovora o obradi za svakog pružatelja.
6. Riješiti prikaz politike pri registraciji (odjeljak 2.2).

### Prije aktivacije naplate

7. Pravnički pregled cijelog dokumenta.
8. Odluka o članku 6.1 Uvjeta i o odnosu voditelj/izvršitelj (odjeljak 2.7).
9. Uskladiti `stranice/tos.md`, koji je i dalje v1.0 od 27.4.2026. i sadrži
   tvrdnje koje politika više ne podupire: članak 4.1 tvrdi da serijski broj
   povezuje dokument s korisnikom u bazi, članak 4.5 da Davatelj može povezati
   serijski broj s računom, a članak 9. da se izmjene javljaju e-poštom. Nijedno
   od toga u trenutnoj konfiguraciji ne stoji.

### Popravci u kodu, neovisni o dokumentu

10. `stranice/pravila.py`: traka i dalje kaže "nacrt v1.0 (2026-04-27)".
11. `cloud/0008_retencija_download_log.sql`, redci 26 do 27: komentar proturječi
    članku 7.1.
12. **Lozinke.** `auth.py`:300 traži najmanje šest znakova, a ograničenja broja
    neuspjelih pokušaja prijave nema. Politika to u članku 10. pošteno navodi, i
    zato ovo nije zamjerka dokumentu. Ali u rješenju protiv FAVBET-a AZOP je pod
    čl. 32. utvrdio da lozinke od tri, četiri, šest i devet znakova nisu dovoljno
    snažna mjera zaštite. Poštena objava slabe mjere ne čini mjeru jačom.

---

## 9. Što traži vlasnikovu odluku

Nijedna od ovih stavki nije popravljena u ovoj ocjeni, jer nijedna nema
jednoznačno točan odgovor koji bi se dao izvesti iz koda.

| # | Odluka | Bez nje | Gdje se upisuje |
|---|---|---|---|
| 1 | Nastupa li vlasnik kao fizička osoba, obrt ili društvo | Nema naziva, OIB-a ni adrese | članak 1. |
| 2 | Kontaktna adresa e-pošte za GDPR zahtjeve | Nijedno pravo iz članka 6. nije ostvarivo | članci 1. i 13. |
| 3 | Imenuje li se službenik za zaštitu podataka | Obvezni element nije popunjen | članak 1. |
| 4 | Rok čuvanja za `stripe_events` | Stanje koje je AZOP dvaput sankcionirao | članak 7., tablica |
| 5 | Rok za računovodstvenu dokumentaciju, prema obliku poslovanja | Prazno polje u tablici rokova | članak 7., tablica |
| 6 | Pravilo za neaktivan račun: ili bez roka, ili početi bilježiti datum zadnje prijave | Nema kriterija koji bi ispitanik mogao primijeniti na sebe | članci 2.2 i 7. |
| 7 | Mehanizam prijenosa izvan EGP-a po svakom pružatelju | Polovica obveznog elementa nedostaje | članak 5. |
| 8 | Jesu li ugovori o obradi sklopljeni, i s kim | Nepoznato stanje po čl. 28 | članak 5. |
| 9 | Točan naziv i adresa svakog pružatelja | Korisnik ne može provjeriti s kim podaci završe | članak 5., tablica |
| 10 | Regija Supabase projekta | Ne zna se gdje podaci fizički jesu | članak 5., tablica |
| 11 | Postoje li sigurnosne kopije i koliko traju | Ne može se reći kad obrisani podatak stvarno nestane | članci 6.3 i 10. |
| 12 | Koji SMTP pružatelj se koristi | Primatelj podataka nije imenovan | članci 2.5 i 5. |
| 13 | Zadržava li se članak 6.1 Uvjeta (odvjetnik za klijenta) | Bez ugovora o obradi i klauzule o ulogama | politika, članak 1.; `tos.md`, članak 6.1 |
| 14 | Tko je voditelj obrade za tuđu adresu upisanu u kalendar | Obveza po čl. 14. neriješena | članak 2.5 |
| 15 | Adresa, e-pošta i telefon AZOP-a, provjereni na izvoru na dan objave | Obvezni element po AZOP-ovu obrascu | članak 6.7 |
| 16 | Nazivi i trajanja pojedinih kolačića | Zamjerka iz rješenja o kolačićima ostaje otvorena | članak 9. |
| 17 | Postupak za zahtjeve po čl. 15, 16 i 20 | Obećanja iz odjeljka 3.1 nemaju mehanizam | novi dokument u `docs/`, po uzoru na `brisanje_podataka.md` |

---

## 10. Što ostaje neprovjereno u ovoj ocjeni

Navedeno da se ne bi zamijenilo s provjerenim:

- **Politike privatnosti pružatelja usluga.** Rokovi čuvanja kod Polara, Stripea,
  Supabasea, Cloudflarea, Googlea i pružatelja hostinga nisu čitani na izvoru u
  ovoj ocjeni. Sve što politika o njima kaže i dalje nosi oznaku [VLASNIK
  POTVRĐUJE].
- **Ponaša li se Polar.sh doista kao Merchant of Record za ovaj račun.** Iz koda
  se vidi namjera integracije, ne i stanje računa kod pružatelja.
- **Radi li migracija `0008` na stvarnoj bazi.** Nije pokrenuta ni na jednoj, što
  je zabilježeno i u `docs/brisanje_podataka.md`.
- **Je li AZOP zauzeo stav o pravnom temelju za nužne kolačiće sesije**, to jest
  vrijedi li izuzeće po čl. 43. st. 4. Zakona o elektroničkim komunikacijama ili
  legitimni interes po GDPR-u. Takvo izjašnjenje nije nađeno. U članku 3. sada
  stoji izuzeće iz Zakona o elektroničkim komunikacijama, uz izričitu napomenu da
  je to ocjena Davatelja.
- **Je li AZOP zauzeo stav o zadržavanju lančanog sažetka nakon isteka roka
  čuvanja.** Nije nađeno nijedno rješenje ni mišljenje. Ograda u članku 7.1 da se
  AZOP o tome nije izjašnjavao ostaje točna.
- **Kolika bi kazna bila za samostalnu grešku u politici.** Nije nađen nijedan
  hrvatski predmet u kojem je politika privatnosti bila jedina utvrđena povreda.
  U svim nađenim odlukama zamjerka politici dolazi uz najmanje još jednu povredu.
  Zbog toga se iznosi navedeni u ovom dokumentu **ne smiju** čitati kao procjena
  izloženosti; navedeni su zato što pokazuju koje je konkretne formulacije i koja
  konkretna stanja AZOP ocijenio povredom.
- **Nije nađen predmet** u kojem je zamjerka bila da je u politici naveden rok
  čuvanja kraći od stvarne prakse, što je bila zatečena greška ovog projekta.
  Najbliži su FAVBET i specijalna bolnica, ali nijedan nije ista kombinacija.

---

## 11. Sažetak u jednom retku

Politika je poštenija i razumljivija od većine uspoređenih, ali bez imena
voditelja obrade i bez kontaktne adrese nije politika privatnosti nego njezin
predložak; objaviti je svejedno treba odmah, jer je tekst koji je trenutno javan
netočan, a ovaj je označen kao nedovršen.
