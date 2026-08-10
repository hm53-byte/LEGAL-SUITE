# Politika privatnosti - LEGAL-SUITE

**Verzija**: 1.3 (nacrt 2026-08-10)
**Status**: NACRT. Nije spreman za objavu kao završen dokument, ali je točniji od
inačice 1.0 koja je trenutno javna.

---

> ## Zašto ovaj dokument još nije spreman za objavu
>
> **1. Sedam polja nije popunjeno.** U dokumentu se na sedam mjesta nalazi
> oznaka `<<< VLASNIK UPISUJE: ... >>>` (šest u članku 1, jedno u članku 13; ova
> napomena nije jedno od tih polja).
> Dok su ta polja prazna, dokument ne imenuje voditelja obrade i ne daje
> kontaktnu adresu za ostvarivanje prava. Takav tekst ne smije se prikazati
> korisniku ni predati nadzornom tijelu: politika privatnosti bez identiteta
> voditelja obrade i bez kontakta ne ispunjava GDPR čl. 13(1)(a) i (b).
>
> **2. Dokument nije pravnički pregledan.** Nacrt treba proći kroz odvjetnika i
> prilagoditi se stvarnim okolnostima Davatelja prije aktivacije naplate.
>
> **3. Dio tvrdnji čeka potvrdu Davatelja.** Vidi objašnjenje oznaka niže.
>
> **4. Prethodna inačica je već javna i sadrži tvrdnju koja nije točna.**
> Inačica 1.0 objavljena je u javnom repozitoriju i u njoj stoji da se zapisi u
> `download_log` nakon 24 mjeseca automatski brišu cron poslom. Takav posao ne
> postoji. Dok ta inačica stoji vani, javno objavljena politika obećava brisanje
> koje se ne provodi. Ovo je zasebna vrsta rizika od nepopunjenih polja i ne
> uklanja se čekanjem: uklanja se objavom ispravljenog teksta.

### Kako čitati ovaj dokument

Dokument opisuje dva stanja i razlikuje ih izričito:

- ono što Aplikacija radi **sada**, u konfiguraciji u kojoj naplata i
  zapisivanje preuzimanja nisu uključeni;
- ono što će raditi kad Davatelj te dijelove uključi.

Gdje god se ta dva stanja razlikuju, razlika je označena oznakom
**[NIJE AKTIVNO]** i objašnjena je u istom odlomku. Tvrdnja bez te oznake opisuje
sadašnje stanje.

### Oznake u tekstu

| Oznaka | Značenje |
|---|---|
| **[VLASNIK POTVRĐUJE]** | Tvrdnja se ne može provjeriti iz izvornog koda aplikacije. Ovisi o ugovorima, postavkama vanjskih računa ili odlukama Davatelja. Prije objave Davatelj mora provjeriti je li točna, i ako nije, ispraviti je ili izbrisati. |
| **[NIJE AKTIVNO]** | Mehanizam postoji u kodu ili u pripremljenim skriptama, ali u trenutnoj konfiguraciji ne radi. Opisano je i što je potrebno da proradi. |

Oznake su namijenjene Davatelju i moraju nestati iz objavljene verzije: ili tako
da se tvrdnja potvrdi, ili tako da se preoblikuje u ono što je stvarno točno.

---

## 1. Voditelj obrade (Davatelj)

| Podatak | Vrijednost |
|---|---|
| Naziv | <<< VLASNIK UPISUJE: ime/naziv tvrtke ili obrta, ili fizičke osobe >>> |
| OIB | <<< VLASNIK UPISUJE: OIB >>> |
| Adresa | <<< VLASNIK UPISUJE: adresa sjedišta >>> |
| E-mail za GDPR pitanja | <<< VLASNIK UPISUJE: kontakt e-mail za GDPR >>> |
| Telefon (opcijski) | <<< VLASNIK UPISUJE: telefon ili "Ne primjenjuje se" >>> |
| DPO (ako primjenjivo) | <<< VLASNIK UPISUJE: DPO ili "Ne imenuje se posebno DPO; voditelj je dosegnut na e-mailu iznad" >>> |

## 2. Koje osobne podatke prikupljamo

### 2.1 Pristup bez registracije (gost)

Aplikacija ima dva načina rada i u oba se do rada dolazi bez registracije.

U **jednostavnom načinu**, koji je zadani, prijavna se stranica uopće ne
prikazuje: sesija pod zajedničkom internom oznakom `gost@legalsuite.hr` otvara se
sama, pri prvom otvaranju Aplikacije. Korisnik pritom ne prolazi kroz nijedan
korak u kojem bi mu bila ponuđena ova Politika.

U **naprednom načinu** prikazuje se prijavna stranica s gumbom "Isprobaj
besplatno"; klikom se otvara ista gostujuća sesija.

Ta oznaka nije adresa korisnika i ne stvara se korisnički zapis: o gostu se ne
pohranjuje ništa što bi ga identificiralo.

**Puni dokument se ne prikazuje sam od sebe, kratka obavijest se prikazuje.**
Od 10.8.2026. Aplikacija na svakom mjestu gdje se unose osobni podaci prikazuje
kratku obavijest o obradi: tko obrađuje, u koju svrhu, na kojoj osnovi, koliko
se čuva i koja prava Korisnik ima, uz poveznicu na ovaj dokument. To vrijedi i
za prijavu i za registraciju, prije ijednog polja.

Ovaj puni dokument se i dalje ne prikazuje sam od sebe niti se traži njegovo
prihvaćanje; dostupan je preko poveznice iz obavijesti ili preko stranice
"Pravila i privatnost". Kratka obavijest ne pokriva sve iz članka 13. (primatelji,
prijenos izvan EGP-a, kolačići) nego za to upućuje ovamo.

### 2.2 Podaci pri registraciji

Ako se Korisnik odluči registrirati, pohranjuju se:

- Ime i prezime, onako kako ih Korisnik upiše
- E-mail adresa
- Lozinka, i to isključivo kao PBKDF2-SHA256 sažetak sa slučajnom soli. Lozinka
  se nikad ne pohranjuje u čitljivom obliku.
- Datum registracije
- Oznaka uloge u Aplikaciji (`user`; postoje i `admin` i `guest`), koja određuje
  samo što se Korisniku prikazuje

**Gdje se to nalazi.** Ovi podaci upisuju se u datoteku `.users.json` na
poslužitelju na kojem aplikacija radi, a ne u bazu podataka. Datoteka nije
dio javnog repozitorija. Ako aplikacija radi na Streamlit Community Cloudu,
datotečni sustav je privremen: pri ponovnom pokretanju ili novoj objavi
aplikacije sadržaj datoteke se gubi, pa s njim i registrirani računi.
Korisnik zbog toga ne smije računati da će mu račun trajati.

**Datum zadnje prijave se ne pohranjuje.** Vrijeme prijave postoji samo u
memoriji tekuće sesije i nestaje s njom.

**Upozorenje uz prelazak računa u bazu.** Pripremljena shema baze
(`cloud/supabase_schema.sql`) ima za račune stupce `last_login_at` i
`oauth_subject`. Čim Davatelj tu shemu primijeni i prijavu poveže s bazom, obje
niječne tvrdnje iz ovog i sljedećeg članka prestaju biti točne. Tada se ovaj
članak mora prepisati prije nego što se ta izmjena objavi, a ne poslije.

### 2.3 Prijava preko Googlea

Ako Korisnik odabere prijavu Googleom, Davatelj od Googlea prima e-mail adresu i
ime s Googleova profila. Ti podaci žive samo u tekućoj sesiji i ne upisuju se
ni u jednu datoteku ni bazu. Trajni identifikator Google računa (`sub`) se
ne prima i ne pohranjuje. Vrijedi i ovdje upozorenje s kraja članka 2.2: shema
baze predviđa stupac za taj identifikator.

Prijava Apple računom nije dovršena: gumb se pojavljuje samo ako Davatelj upiše
Apple podatke u postavke, ali obrada Appleova odgovora nije implementirana, pa
prijava tim putem ne završava uspješno. **[NIJE AKTIVNO]**

### 2.4 Podaci pri generiranju dokumenata

Za svaki preuzeti dokument predviđen je jedan zapis u internoj tablici
`download_log`, sa sljedećim sadržajem:

- Tip dokumenta (npr. "tuzba", "ovrha") i naziv generatora unutar tipa
- Datum i vrijeme generiranja
- Sažetak serijskog broja dokumenta (vidi članak 4)
- Tier u trenutku generiranja (free / pro)
- Oznaka korisnika koji je dokument generirao
- Kriptografski sažeci (SHA-256) unesenih podataka, gotove datoteke i izvornog
  koda generatora, te lančani sažetak prethodnog zapisa (audit lanac). Iz
  sažetka se ne može rekonstruirati uneseni sadržaj. Može se, međutim, potvrditi
  pogodak: tko već ima dokument i podatke koji su u njega uneseni, usporedbom
  sažetaka provjerava je li riječ o tom dokumentu. Zato se ti sažeci u članku
  7.1 tretiraju kao pseudonimizirani, a ne anonimni podatak.

**U trenutnoj konfiguraciji ta tablica ostaje prazna. [NIJE AKTIVNO]** Upis
zapisa vezan je uz oznaku korisnika koju bi trebala postaviti prijava, a
trenutna prijava je ne stvara. Zbog toga upis tiho izostaje i o generiranim
dokumentima se ne bilježi ništa. Isto vrijedi za serijski broj: on se i dalje
utiskuje u dokument, ali se ne veže ni uz koji račun (vidi članak 4).

Zapisi počinju nastajati tek kad Davatelj poveže prijavu s bazom podataka. Od
tog trenutka vrijedi sve što je gore navedeno, uključujući rok čuvanja iz
članka 7.

**Ne pohranjujemo sadržaj generiranih dokumenata.** Sav sadržaj koji Korisnik
unese (imena stranaka, OIB-i, opisi, iznosi) ostaje samo u memoriji poslužitelja
tijekom generiranja i odmah se odbacuje. Gotova datoteka gradi se u memoriji i
predaje Korisniku na preuzimanje; na disk se ne zapisuje i kopija se ne čuva.

**Što se s tim unosom ne radi.** Dok je u memoriji, uneseni sadržaj služi
isključivo popunjavanju predloška koji je Korisnik odabrao. Ne koristi se ni za
jednu drugu svrhu: nema profiliranja, nema oglašavanja, nema analize ponašanja,
nema ustupanja trećima i ne koristi se za učenje ili podešavanje bilo kakvog
modela. Aplikacija nema ugrađen jezični model ni drugi oblik strojnog učenja
(vidi članak 3.1).

**Uneseni sadržaj može biti osjetljiv.** Predlošci pokrivaju i obiteljske,
nasljedne, kaznene i ovršne stvari, pa Korisnik u obrazac može upisati podatke
koji su za njega ili za treću osobu osjetljivi. Zbog toga vrijedi pravilo iz
prethodnog odlomka: takav sadržaj ne izlazi iz memorije. Jedini trag koji od
njega ostaje, i to tek kad se zapisivanje uključi, jest kriptografski sažetak
opisan gore u ovom članku, koji se u članku 7.1 tretira kao pseudonimiziran
podatak i briše se po roku iz članka 7.

### 2.5 Kalendar rokova i ročišta

Modul "Kalendar" sprema unesene događaje u datoteku `_data/kalendar.json` na
poslužitelju. Zapis sadrži naslov događaja, datum, opis, tip (ročište, rok,
dražba, ostalo), oznaku predmeta i, ako je Korisnik upiše, e-mail adresu na koju
se šalje podsjetnik.

Dvije stvari koje Korisnik mora znati prije nego išta upiše:

1. **Unosi nisu odvojeni po korisniku.** Svi koji koriste istu instancu
   aplikacije vide isti popis događaja. Ne upisujte podatke koji ne smiju biti
   vidljivi drugim korisnicima iste instance, osobito ne podatke o strankama i
   ne tuđe e-mail adrese.
2. **Datoteka je privremena** na Streamlit Community Cloudu, jednako kao i
   `.users.json` iz članka 2.2: pri ponovnom pokretanju unosi se gube.

Podsjetnici se šalju e-mailom preko SMTP poslužitelja koji konfigurira Davatelj.
Ako SMTP nije konfiguriran, podsjetnik se ne šalje i aplikacija to javi.
Davatelj mora navesti kojeg SMTP pružatelja koristi i uvrstiti ga u popis u
članku 5. **[VLASNIK POTVRĐUJE]**

3. **Adresa primatelja podsjetnika može biti tuđa.** Polje "Email za podsjetnik"
   prima bilo koju adresu. Ako Korisnik upiše tuđu, ta osoba postaje ispitanik
   čije podatke Davatelj obrađuje, a od Davatelja ne dobiva nikakvu obavijest:
   Aplikacija joj ovu Politiku ne šalje niti je na nju upućuje. Zbog toga
   upozorenje iz točke 1 vrijedi i ovdje: ne upisujte tuđu adresu. Tko je za
   takav unos voditelj obrade, a tko izvršitelj, ovim dokumentom nije uređeno i
   Davatelj to mora riješiti prije objave. **[VLASNIK POTVRĐUJE]**

### 2.6 Podaci pri pretplati (samo PRO korisnici)

Ovaj članak opisuje što se obrađuje kad je naplata aktivirana. **U trenutnoj
konfiguraciji naplata nije aktivna [NIJE AKTIVNO]**: pokretanje kupnje traži i
oznaku korisnika iz članka 2.4 i objavljen webhook servis, pa se PRO pretplata
ne može kupiti kroz aplikaciju.

Kad je naplata aktivna, u bazi se nalaze:

- Identifikator kupca kod pružatelja naplate Polar.sh (u bazi u polju
  naslijeđenog naziva `stripe_customer_id`)
- Identifikator pretplate ili narudžbe kod pružatelja naplate
- Status pretplate (active / past_due / revoked) i datum isteka aktualnog perioda
- Cjeloviti zapis webhook događaja pružatelja naplate (tablica `stripe_events`,
  polje `payload_json`). Taj zapis nije samo tehnička oznaka događaja: sprema se
  onakav kakav stigne, a sadrži i e-mail adresu kupca, iznos, valutu i
  identifikator proizvoda. Služi za to da se isti događaj ne obradi dvaput.

**Podatke o kartici ne prikupljamo niti pohranjujemo.** Broj kartice, datum
isteka i sigurnosni kod ne prolaze kroz Aplikaciju: plaćanje se odvija izravno
između Korisnika i pružatelja naplate (Polar.sh, koji nastupa kao Merchant of
Record). U kodu postoji i naslijeđena Stripe integracija; ako je aktivirana, za
karticu vrijedi isto.

Davatelj pritom ne dobiva samo potvrdu da je pretplata aktivna. Prima cjelovitu
obavijest o događaju plaćanja i sprema je onakvu kakva stigne, sa sadržajem
navedenim u zadnjoj točki gornjeg popisa, uključujući e-mail adresu kupca. Ova
je rečenica dodana zato što je raniji tekst govorio "samo potvrdu", što je
manje nego što se stvarno prima.

### 2.7 Tehnički podaci

**Aplikacija ne čita, ne koristi i ne pohranjuje IP adresu ni User-Agent.** U
kodu nema takve obrade, pa nema ni ograničavanja broja zahtjeva ni otkrivanja
prijevara na temelju IP adrese.

Pružatelji infrastrukture (Streamlit, Cloudflare, Supabase) svejedno vode
vlastite zapise prometa, koji tipično uključuju IP adresu i User-Agent, prema
svojim uvjetima. Davatelj na te zapise ne utječe i ne pristupa im kroz
aplikaciju. Koji su to zapisi i koliko se čuvaju, Davatelj mora provjeriti kod
svakog pružatelja i navesti ovdje. **[VLASNIK POTVRĐUJE]**

## 3. Pravni temelji obrade (GDPR čl. 6)

| Podatak | Pravni temelj | Razlog |
|---|---|---|
| E-mail, ime, sažetak lozinke | Ugovor (čl. 6(1)(b)) | Bez računa nije moguće razlikovati korisnike ni pružiti PRO pretplatu |
| Zapis o generiranom dokumentu (tip, datum, serial, sažeci) | Legitiman interes (čl. 6(1)(f)) | Dokazivanje autentičnosti dokumenta u sporu i sprečavanje zlouporabe |
| Unosi u kalendar i e-mail za podsjetnik | Ugovor (čl. 6(1)(b)) | Bez tih podataka funkcija podsjetnika ne postoji |
| Identifikator kupca kod pružatelja naplate i zapis o plaćanju | Ugovor (čl. 6(1)(b)) | Bez toga nije moguće provjeriti plaćanje ni izvršiti povrat |
| Cookies nužni za rad sesije | Izuzeće od privole po čl. 43. st. 4. Zakona o elektroničkim komunikacijama (NN 76/22); vidi napomenu ispod tablice | Pohrana je nužna za pružanje usluge koju je Korisnik izričito zatražio: Aplikacija bez sesije ne može raditi |

Obrada IP adrese ne navodi se u ovoj tablici jer je aplikacija ne obavlja (vidi
članak 2.7).

**Napomena uz nužne kolačiće.** Čl. 43. st. 4. Zakona o elektroničkim
komunikacijama (NN 76/22) dopušta pohranu podataka u terminalnoj opremi bez
privole kad je nužna za pružanje usluge informacijskog društva na izričit zahtjev
korisnika. Raniji tekst ove Politike za te je kolačiće navodio legitimni interes
iz čl. 6. st. 1. t. (f) GDPR-a. Nije poznato je li AZOP zauzeo stav o tome koji
je od ta dva okvira mjerodavan za nužne kolačiće sesije: u javno objavljenim
rješenjima i mišljenjima takvo izjašnjenje nije nađeno. Ovdje se navodi izuzeće
iz Zakona o elektroničkim komunikacijama jer je to propis koji izravno uređuje
pohranu u terminalnoj opremi. To je ocjena Davatelja, a ne utvrđena praksa.

### 3.1 Automatizirano donošenje odluka i profiliranje

**Nema ga.** Aplikacija ne donosi nijednu odluku o Korisniku automatiziranom
obradom, uključujući izradu profila, u smislu GDPR čl. 22. Konkretno:

- ne ocjenjuje Korisnika ni njegov predmet i ne dodjeljuje mu bodove, razrede ni
  rizične oznake;
- ne predviđa ishod postupka, ne preporučuje koji dokument treba i ne bira
  predložak umjesto Korisnika; predložak bira Korisnik;
- ne prilagođava sadržaj, cijenu ni ponudu na temelju ponašanja Korisnika;
- ne sadrži jezični model, klasifikator ni drugi oblik strojnog učenja. Popuna
  predloška je determinističko uvrštavanje unesenih vrijednosti u unaprijed
  napisan tekst: isti unos uvijek daje isti izlaz.

Jedina automatska radnja koja se veže uz Korisnika jest provjera ima li aktivnu
PRO pretplatu, i to je provjera zapisa o plaćanju, a ne ocjena osobe.

### 3.2 Je li davanje podataka obvezno i što ako se ne daju

| Podatak | Je li obvezan | Što ako se ne da |
|---|---|---|
| Ništa, za rad kao gost | Nije. Registracija nije uvjet korištenja | Aplikacija radi u punom opsegu predložaka |
| E-mail, ime i lozinka pri registraciji | Ugovorni uvjet, i to samo ako Korisnik želi račun | Bez njih se račun ne može otvoriti. Aplikacija se i dalje može koristiti kao gost |
| Podaci koje Korisnik upiše u obrazac dokumenta | Nisu obveza prema Davatelju, nego uvjet da dokument bude upotrebljiv | Dokument se generira i s nepotpunim unosom, ali takav dokument najčešće nije upotrebljiv pred sudom ili tijelom |
| Unosi u kalendar i adresa za podsjetnik | Nisu obvezni | Bez njih funkcija kalendara i podsjetnika ne radi. Ostatak Aplikacije radi |
| Podaci pri pretplati | Ugovorni uvjet za PRO | Bez njih se pretplata ne može sklopiti; besplatni tier ostaje dostupan |

Zakonske obveze davanja podataka Davatelju nema ni za jedan od gornjih podataka.

## 4. Serijski broj dokumenta i forenzički trag

Svaki generirani `.docx` dobiva serijski broj u obliku `NN-NNNN-NNNNNN`,
izračunat ovako:

```
SHA256(oznaka_korisnika + tip_dokumenta + vrijeme + slučajna_vrijednost)[:12]
```

Iz samog serijskog broja nije moguće rekonstruirati Korisnikove osobne podatke,
jer je riječ o kriptografskom sažetku.

**Gdje je serijski broj vidljiv.** U podnožju dokumenta nalazi se u oba tiera:
u free tieru uz oznaku "Generirano iz LEGAL-SUITE", u PRO tieru sam. Uz to se
upisuje u XML metapodatke dokumenta (`dc:identifier`) u oba tiera. Korisnik može
ukloniti podnožje u uređivaču teksta, ali metapodaci ostaju dok ne otvori
`.docx` kao zip arhivu i ne uredi `core.xml`.

**Čemu služi.** Ako se u sporu pojavi dokument, serijski broj iz podnožja ili iz
metapodataka vodi na zapis u tablici `download_log`, iz kojeg se vidi je li
dokument doista generiran u Aplikaciji i kojem računu pripada.

**Ograničenje u trenutnoj konfiguraciji. [NIJE AKTIVNO]** Kako zapisi iz članka
2.4 ne nastaju, serijski broj trenutno ne vodi nikamo. Uz to se računa s
oznakom `guest` umjesto oznake korisnika, pa se iz njega ne može utvrditi ni tko
je dokument generirao. Praktično: serijski broj sada dokazuje samo da je
dokument nastao u ovom obliku, a ne i tko ga je izradio.

**Tko može čitati tablicu.** Na tablici je uključena zaštita na razini retka.
Pravila su napisana tako da vežu redak uz identitet korisnika koji izdaje baza
(`auth.uid()`): tko je tako prijavljen, čita i unosi samo vlastite retke, a
cjeloviti uvid ima jedino Davatelj preko servisnog ključa baze. Za brisanje i
izmjenu retka ne postoji nijedno pravilo, pa se iz Aplikacije redak ne može ni
obrisati ni promijeniti; to je moguće samo servisnim ključem.

**Što to znači sada. [NIJE AKTIVNO]** Aplikacija se ne prijavljuje na bazu
korisničkim identitetom: prijava iz članka 2.2 s bazom nije povezana. Zbog toga
je `auth.uid()` prazan i nijedno od navedenih pravila nikome ne odobrava ni
čitanje ni upis. Posljedica je ista kao u članku 2.4: kroz Aplikaciju u tu
tablicu ne ulazi ni jedan redak i iz nje se ništa ne čita. Opis iznad opisuje
stanje koje nastupa tek kad Davatelj prijavu poveže s bazom.

## 5. Tko ima pristup vašim podacima (treće strane)

| Treća strana | Što vidi | Gdje | Razlog |
|---|---|---|---|
| **Streamlit Community Cloud**, pravna osoba koja pruža uslugu nije potvrđena **[VLASNIK POTVRĐUJE]** | Promet prema aplikaciji, uključujući IP adresu i User-Agent u vlastitim zapisima; datoteke `.users.json` i `_data/kalendar.json` nalaze se na njihovom poslužitelju | SAD | Hosting Aplikacije |
| **Supabase Inc.** (San Francisco, CA, SAD) | Podaci iz članaka 2.4 i 2.6 kad su te funkcije aktivirane; ne vidi sadržaj dokumenata | Regija u kojoj je projekt otvoren nije navedena u ovom dokumentu, pa Korisnik iz njega ne može znati gdje se podaci nalaze **[VLASNIK POTVRĐUJE]** | Baza podataka |
| **Cloudflare Inc.** (San Francisco, CA, SAD) | Webhook događaji pružatelja naplate (identifikator i e-mail kupca, plan, status) | Cloudflareova globalna mreža, koja ima poslužitelje i izvan EGP-a | Obrada webhookova o plaćanju |
| **Polar.sh**, točan naziv pravne osobe nije potvrđen **[VLASNIK POTVRĐUJE]** | E-mail, podaci o kartici, podaci o transakciji | Prema Polarovoj politici privatnosti | Procesiranje plaćanja (Merchant of Record) |
| **Stripe**, ugovorna strana za korisnike iz EGP-a je društvo sa sjedištem u Irskoj **[VLASNIK POTVRĐUJE]** | E-mail, podaci o kartici, podaci o transakciji | Prema Stripeovoj politici privatnosti; ovaj dokument ne tvrdi da obrada ostaje unutar EU | Procesiranje plaćanja (naslijeđena integracija; vrijedi samo ako je Stripe checkout aktiviran) |
| **SMTP pružatelj za podsjetnike** | E-mail adresa primatelja i sadržaj podsjetnika (naslov, datum, opis, oznaka predmeta) | Prema uvjetima pružatelja **[VLASNIK POTVRĐUJE]** | Slanje podsjetnika iz kalendara |
| **Google LLC** | E-mail i ime s Google profila, ako Korisnik odabere prijavu Googleom | Prema Googleovoj politici privatnosti | Prijava vanjskim računom |

**Puni podaci o primateljima nedostaju.** Tablica imenuje pružatelje, ali ne
navodi adresu sjedišta ni registracijski broj nijednoga od njih, a za dva
pružatelja ni točan naziv pravne osobe. Dok to nije popunjeno, Korisnik ne može
provjeriti s kim njegovi podaci stvarno završe. **[VLASNIK POTVRĐUJE]**

**Prijenos izvan EGP-a: da, odvija se.** Pružatelj hostinga Aplikacije i
Cloudflare Inc. posluju iz SAD-a, Davatelj im obradu nije ograničio na Europski
gospodarski prostor, i Aplikacija nema postavku kojom bi to učinio. Korisnik zato
mora računati s time da se njegovi podaci obrađuju i izvan EGP-a.

Ova je rečenica namjerno bez ograde. Raniji tekst je govorio da se obrada "može"
odvijati izvan EU. AZOP je takvo izražavanje ("možda", "u pravilu unutar EU, a
iznimno izvan") ocijenio protivnim čl. 12. st. 1. GDPR-a u rješenju protiv
teleoperatora, uz kaznu od 4.500.000 eura, upravo zato što ispitanik iz takve
formulacije ne može zaključiti prenose li se njegovi podaci ili ne
(https://azop.hr/teleoperatoru-upravna-novcana-kazna-u-ukupnom-iznosu-od-45-milijuna-eura/,
pročitano 9.8.2026.; rješenje prema podacima AZOP-a nije pravomoćno).

Za takav prijenos potreban je valjan mehanizam iz GDPR poglavlja V (standardne
ugovorne klauzule ili odluka o primjerenosti). Koji mehanizam vrijedi za svakog
pružatelja i je li prihvaćen, Davatelj mora utvrditi i ovdje navesti prije
objave; do tada ovaj dokument ne tvrdi da takav mehanizam postoji.
**[VLASNIK POTVRĐUJE]**

**Ugovori o obradi (GDPR čl. 28).** Postojanje potpisanog ugovora o obradi s
pojedinim pružateljem ne vidi se iz aplikacije ni iz repozitorija. Prije objave
Davatelj mora za svakog pružatelja iz tablice provjeriti je li ugovor o obradi
sklopljen (kod većine se prihvaća u administracijskom sučelju računa) i tek onda
ovdje napisati da postoji. **[VLASNIK POTVRĐUJE]**

## 6. Vaša prava (GDPR)

Sukladno GDPR-u i Zakonu o provedbi Opće uredbe o zaštiti podataka (NN 42/18),
Korisnik ima sljedeća prava. Sva se ostvaruju slanjem zahtjeva na kontakt adresu
iz članka 13. **U Aplikaciji ne postoji samoposlužno sučelje za ta prava**, pa
ih Davatelj obrađuje ručno.

**Rok.** Davatelj odgovara bez nepotrebnog odgađanja, a najkasnije u roku od
mjesec dana od primitka zahtjeva. Taj se rok može produljiti za najviše dodatna
dva mjeseca ako je zahtjev složen ili ih je više; u tom slučaju Davatelj o
produljenju i o razlozima obavještava Korisnika unutar prvog mjeseca (GDPR čl.
12. st. 3.). Davatelj se obvezuje na taj rok bez obzira na to koliko dugo traje
tehnička provedba brisanja, koja je opisana u članku 6.3.

**Provjera identiteta.** Ako Davatelj ima osnovanu sumnju u identitet osobe koja
podnosi zahtjev, zatražit će dodatne podatke nužne za potvrdu identiteta prije
nego što po zahtjevu postupi (GDPR čl. 12. st. 6.). Zatražit će samo ono što je
za to nužno i te podatke neće koristiti ni u koju drugu svrhu. Razlog je zaštita
samog Korisnika: bez te provjere zahtjev za presliku podataka ili za brisanje
mogla bi podnijeti bilo koja osoba koja zna Korisnikovu adresu e-pošte.

### 6.1 Pravo na pristup (čl. 15)

Korisnik može zatražiti presliku svojih osobnih podataka koje Davatelj obrađuje.

### 6.2 Pravo na ispravak (čl. 16)

Netočne podatke (npr. ime ili e-mail) ispravlja Davatelj na zahtjev. Aplikacija
trenutno nema ekran za izmjenu vlastitih podataka.

### 6.3 Pravo na brisanje ("pravo da budem zaboravljen", čl. 17)

Korisnik može zatražiti brisanje računa i osobnih podataka. Na zahtjev se briše:

- zapis o računu u `.users.json` (ime, e-mail, sažetak lozinke, datum registracije),
- unosi u kalendaru koje Korisnik označi kao svoje.

Iz zapisa o generiranim dokumentima (`download_log`) redak se ne briše, nego mu
se prazne osobni stupci. Razlog i posljedice objašnjeni su u članku 7.

Podaci kod pružatelja naplate brišu se prema njegovim rokovima, a ne prema
odluci Davatelja. Podaci koje Davatelj mora čuvati po zakonu (npr. dokumentacija
o plaćanju prema Zakonu o računovodstvu) ostaju do isteka zakonskog roka.

Brisanje ne djeluje trenutačno na sigurnosne kopije baze: iz njih podatak nestaje
tek kad istekne rok čuvanja kopija (vidi članak 10).

### 6.4 Pravo na prenosivost (čl. 20)

Korisnik može zatražiti svoje podatke u strojno čitljivom obliku. Davatelj ih
priprema ručno i dostavlja kao JSON.

### 6.5 Pravo na prigovor (čl. 21)

Korisnik može uložiti prigovor na obradu utemeljenu na legitimnom interesu (npr.
zapis o generiranim dokumentima). Davatelj odgovara u roku iz uvoda ovog članka;
ako prigovor smatra opravdanim, prestaje s tom obradom osim ako postoje
uvjerljiviji legitimni razlozi.

### 6.6 Pravo na povlačenje privole

Ne primjenjuje se na obrade utemeljene na ugovoru ili legitimnom interesu (vidi
članak 3). Primjenjuje se na eventualne marketinške poruke za koje je dana
zasebna privola (vidi članak 8).

Ako Korisnik privolu povuče, povlačenje vrijedi unaprijed: ne utječe na
zakonitost obrade koja se na temelju te privole provodila prije povlačenja (GDPR
čl. 7. st. 3.). Povlačenje je jednako jednostavno kao davanje privole i ne
povlači nikakvu naknadu ni posljedicu za korištenje Aplikacije.

### 6.7 Pravo žalbe nadzornom tijelu

Korisnik se može žaliti **Agenciji za zaštitu osobnih podataka** (AZOP),
www.azop.hr, ako smatra da Davatelj ne poštuje GDPR. Prije objave ovdje treba
stajati i adresa sjedišta AZOP-a, njegova adresa e-pošte i telefon: to traži
AZOP-ov vlastiti obrazac politike privatnosti
(https://azop.hr/wp-content/uploads/2024/03/2-politika-privatnosti_obrazac.docx,
obrazac objavljen 03/2024, preuzet 9.8.2026.). Te podatke Davatelj mora provjeriti
na izvoru na dan objave dokumenta, jer se u ovom nacrtu ne navode napamet.
**[VLASNIK POTVRĐUJE]**

## 7. Razdoblje čuvanja podataka

| Podatak | Razdoblje |
|---|---|
| Račun (ime, e-mail, sažetak lozinke) | Dok postoji račun. Briše se na zahtjev. Automatskog brisanja neaktivnih računa nema. Na privremenom datotečnom sustavu račun može nestati i ranije (članak 2.2). |
| Unosi u kalendaru | Dok ih Korisnik ne obriše. Automatskog brisanja nema. |
| `download_log` (zapis o generiranom dokumentu) | **24 mjeseca** od generiranja. Nakon toga se zapis prazni: ostaju interna oznaka retka, vrijeme generiranja, dva lančana sažetka i oznaka trenutka pražnjenja; svi ostali stupci se brišu. Zašto ne cijeli redak, vidi točku 7.1. |
| `entitlements` (plan, status, period) | Dok postoji račun; briše se zajedno s računom. |
| `stripe_events` (sirovi zapisi o plaćanju s e-mailom kupca) | Rok nije određen i automatskog brisanja nema. Davatelj mora odrediti rok i uvrstiti ga ovdje. **[VLASNIK POTVRĐUJE]** |
| Dokumentacija o plaćanju za PRO pretplate | Prema Zakonu o računovodstvu (NN 78/15); Davatelj mora provjeriti koji rok se primjenjuje na njegov oblik poslovanja i upisati ga ovdje. **[VLASNIK POTVRĐUJE]** |
| Podaci kod pružatelja naplate | Prema politici privatnosti pružatelja (Polar.sh; Stripe za naslijeđenu integraciju) |
| Zapisi prometa kod pružatelja infrastrukture | Prema njihovim uvjetima; Davatelj na njih ne utječe (članak 2.7) **[VLASNIK POTVRĐUJE]** |

**Koji redci ove tablice još ne zadovoljavaju.** Smjernice o transparentnosti
(WP260 rev.01, str. 38, koje je AZOP objavio na hrvatskom na
https://azop.hr/wp-content/uploads/2020/12/smjernice-o-transparentnosti.pdf)
traže da rok ili kriterij budu takvi da ispitanik na temelju vlastite situacije
može procijeniti koliko će se njegovi podaci čuvati. Tome udovoljava samo redak
za `download_log`, koji ima brojku. Ostali retci daju kriterij vezan uz radnju
Korisnika ili uz odluku trećega, a redak za `stripe_events` ne daje ni to.

Neodređen rok za `stripe_events` nije formalni propust. To je stanje koje je AZOP
sankcionirao u dva objavljena predmeta: protiv specijalne bolnice, gdje je
utvrđeno da rokovi čuvanja nisu propisani internim aktima (rješenje KLASA
UP/I-034-01/24-01/23 od 21.8.2024., ukupno 190.000 eura), i protiv Hrvatskog
ureda za osiguranje, gdje maksimalni rokovi nisu bili zasebno propisani
(101.000 eura, prema Godišnjem izvješću AZOP-a za 2025.). Taj zapis sadrži
e-mail adresu kupca (članak 2.6), pa nije riječ o tehničkom dnevniku bez osobnog
podatka.

**Zašto ovdje nema pravila o neaktivnom računu.** Uobičajeno rješenje kod sličnih
usluga jest brisanje ili pseudonimizacija nakon određenog broja mjeseci bez
prijave. Takvo se pravilo ovdje ne može postaviti jer Aplikacija ne bilježi datum
zadnje prijave (članak 2.2), pa nema podatka na kojem bi se rok mjerio. Davatelj
ima dvije mogućnosti i mora izabrati jednu prije objave: ili ostaviti račun bez
roka i to ovako reći, ili početi bilježiti datum zadnje prijave, čime se članak
2.2 mijenja. Treće mogućnosti, da se rok obeća a ne mjeri, nema.

### 7.1 Zašto se zapis o dokumentu ne briše, nego se prazni

Zapisi u `download_log` povezani su u lanac kriptografskih sažetaka: svaki zapis
nosi sažetak izračunat i iz sažetka prethodnog zapisa. Zbog toga se lanac može
provjeriti: ako netko naknadno izmijeni jedan stari zapis, a ne preračuna
sažetke tog i svih kasnijih zapisa, provjera to otkrije. Protiv onoga tko ima
pravo pisanja u bazu i preračuna cijeli niz, lanac sam po sebi ne štiti; za to
bi trebalo povremeno pohranjivati zadnji sažetak izvan baze, što nije
uspostavljeno.

Brisanje cijelog retka imalo bi nuspojavu koju Korisnik mora znati. Provjera
lanca ne razlikuje redak koji je uklonjen zato što je istekao rok čuvanja od
retka koji je uklonjen zato da bi se nešto sakrilo. Oba slučaja izgledaju
jednako. Kad bi se stari zapisi brisali, forenzička vrijednost lanca bi nestala,
i to upravo za korisnike koji Aplikaciju koriste najduže.

Zato se nakon 24 mjeseca radi ovo:

**Prazni se** (postavlja se na praznu vrijednost):

- oznaka korisnika koji je dokument generirao,
- tip dokumenta i naziv generatora unutar tipa,
- sažetak serijskog broja dokumenta,
- tier u trenutku generiranja,
- sažetak unesenih podataka, sažetak gotove datoteke, sažetak izvornog koda
  generatora i oznaka verzije sheme.

Prazne se i ta tri sažetka, iako na prvi pogled ne izgledaju kao osobni podatak.
Sažetak unesenih podataka izračunat je nad sadržajem koji uključuje ime, OIB i
adresu stranke. Takav sažetak je pseudonimiziran podatak, a ne anoniman (GDPR
čl. 4 t. 5 i uvodna izjava 26): tko zna sadržaj, može provjerom pogoditi je li
određeni dokument bio taj. Da ostanu u tablici, obećani rok čuvanja ne bi bio
ispoštovan.

**Ostaje trajno**:

- interna oznaka retka (nasumičan broj koji baza dodjeljuje pri upisu i koji ne
  sadrži nikakav podatak o Korisniku),
- vrijeme generiranja,
- dva lančana sažetka: onaj koji pokazuje na prethodni zapis i onaj koji
  predstavlja sam zapis u lancu,
- oznaka trenutka kad je zapis ispražnjen, koja služi kao dokaz da je rok
  proveden.

**Što to znači za Korisnika.** Nakon 24 mjeseca Davatelj iz tog retka ne može
doći ni do osobe ni do sadržaja dokumenta: veza serijski broj prema računu je
prekinuta, tip dokumenta se ne vidi, i nijedan podatak koji je Davatelj zadržao
ne vodi natrag do Korisnika. Ostaje samo karika koja drži lanac na okupu.

**Što ostaje mogućim, i to se ovdje ne prešućuje.** Lančani sažetak zapisa
izračunat je iz pet vrijednosti. Tri od njih nisu tajne: sažetak prethodnog
zapisa ostaje u istom retku, oznaka verzije sheme je kratka tehnička vrijednost,
a sažetak izvornog koda generatora se može ponovno izračunati za svakoga tko ima
izvorni kod Aplikacije. Nedostaju samo sažetak unesenih podataka i sažetak gotove
datoteke, a oboje se dobiva iz istog dokumenta. Praktična posljedica: tko već
ima i gotovi dokument i podatke koji su u njega uneseni, može sam izračunati
lančani sažetak i usporediti ga s onim u tablici. Ako se poklope, saznaje da je
taj dokument generiran u Aplikaciji i u kojem trenutku. Ne saznaje tko ga je
generirao, jer taj podatak u tablici više ne postoji, i ne može iz sažetka
izvesti sadržaj koji nema.

Davatelj tu mogućnost nema, jer nikad ne pohranjuje ni sadržaj dokumenta ni
unesene podatke (članak 2.4). Zbog toga Davatelj drži da ispražnjeni redak za
njega više nije osobni podatak u smislu GDPR čl. 4 t. 1 i uvodne izjave 26, koja
traži da se u obzir uzmu sredstva kojima se razumno može poslužiti voditelj
obrade ili druga osoba, te se poziva i na čl. 11 st. 1, po kojem voditelj obrade
nije dužan pribavljati dodatne podatke samo zato da bi mogao identificirati
osobu. To je pravna ocjena Davatelja, a ne utvrđena praksa: AZOP se o zadržavanju
lančanog sažetka nakon isteka roka nije izjašnjavao. Ako nadzorno tijelo zauzme
stroži stav, Davatelj se za tri preostala polja poziva na legitimni interes
dokazivanja autentičnosti dokumenta (čl. 6 st. 1 t. (f)) i na iznimku od prava
na brisanje radi postavljanja, ostvarivanja ili obrane pravnih zahtjeva (čl. 17
st. 3 t. (e)).

Isti postupak primjenjuje se i kad Korisnik zatraži brisanje računa prije isteka
24 mjeseca: prvo se isprazne njegovi zapisi, pa se briše račun. U tom slučaju
vrijedi jedna dodatna ograda: zapisi prometa kod pružatelja infrastrukture
(članak 2.7) mogu u tom trenutku još postojati i sadržavati vrijeme prijave, pa
teoretski dopuštaju povezivanje s vremenom generiranja iz ispražnjenog retka. Ti
se zapisi brišu prema rokovima pružatelja, na koje Davatelj ne utječe, i redovito
su kraći od 24 mjeseca; kod redovnog isteka roka iz ove tablice takvih zapisa
više nema.

### 7.2 Status ovog roka

**Pražnjenje se ne izvodi automatski. [NIJE AKTIVNO]** Aplikacija ne može sama
mijenjati zapise u `download_log`, jer je pravilima baze u tome spriječena
(članak 4). Posao mora biti postavljen u samoj bazi, servisnim ovlaštenjem, i to
je zahvat koji Davatelj izvodi jednokratno; upute su u datoteci
`docs/brisanje_podataka.md` u repozitoriju.

Dok Davatelj taj posao ne postavi, rok od 24 mjeseca iz ove tablice ne teče i
osobni stupci ostaju popunjeni. U trenutnoj konfiguraciji tablica je ionako
prazna (članak 2.4), pa nema podataka koje bi trebalo prazniti, ali obje stvari
treba riješiti prije objave: prvo se aktivira zapisivanje, pa tek onda smije
stajati tvrdnja da se zapisi čiste.

## 8. Marketing i obavijesti

Davatelj **ne šalje** marketinške e-mailove. Aplikacija nema popis primatelja ni
mehanizam za slanje takvih poruka. Pri registraciji se privola za marketing ne
traži jer registracija služi samo radu Aplikacije.

Podsjetnici iz kalendara nisu marketing: šalju se samo na adresu koju Korisnik
sam upiše uz pojedini događaj i samo za taj događaj.

Ako se marketing uvede, tražit će se zasebna privola (kućica koju Korisnik sam
označi), a svaka poruka će sadržavati poveznicu za odjavu.

**Operativne obavijesti** (npr. izmjena Uvjeta korištenja) objavljuju se u
Aplikaciji, na stranici "Pravila i privatnost". Automatsko slanje takvih
obavijesti e-mailom nije uspostavljeno.

## 9. Cookies

| Cookie | Tip | Razlog | Trajanje |
|---|---|---|---|
| Streamlit kolačići sesije | Nužni | Bez njih Aplikacija ne može zadržati Korisnikove izbore tijekom sesije | Sesija (do zatvaranja kartice preglednika) |
| Kolačići koje postavlja Google pri prijavi Google računom | Nužni (treća strana) | Postavlja ih Google na svojim stranicama tijekom prijave | Prema Googleovoj politici |
| Kolačići pružatelja naplate pri kupnji | Nužni (treća strana) | Polar.sh (odnosno Stripe u naslijeđenoj integraciji) postavlja ih na svojoj stranici za plaćanje. Relevantno samo kad je naplata aktivirana. | Prema politici pružatelja naplate |

Aplikacija ne postavlja vlastiti kolačić za pamćenje prijave: prijava vrijedi
samo dok traje sesija.

**Ne koriste se** kolačići za praćenje (Google Analytics, Facebook Pixel,
oglasne mreže). U kodu Aplikacije nema takvog koda. Ako se uvedu, tražit će se
privola prije postavljanja.

## 10. Sigurnost

Davatelj primjenjuje sljedeće mjere:

- **Šifriranje u prijenosu**: HTTPS (TLS) za promet između Korisnika i
  Aplikacije te između Aplikacije i vanjskih servisa. Osiguravaju ga pružatelji
  infrastrukture.
- **Lozinke**: PBKDF2-SHA256 sa slučajnom soli i 100.000 iteracija.
- **Ograničenja prijave**: aplikacija ne ograničava broj neuspjelih pokušaja
  prijave i traži lozinku od najmanje šest znakova. Preporučuje se dugačka
  lozinka koja se ne koristi nigdje drugdje.
- **Pristup podacima u bazi**: na tablicama s korisničkim podacima (`users`,
  `entitlements`, `download_log`) uključena je zaštita na razini retka, uz
  ograničenje iz članka 4. Tablica `stripe_events` nema zaštitu na razini retka:
  do nje se dolazi isključivo servisnim ključem, koji drži Davatelj i koji nije
  ni u Aplikaciji ni u repozitoriju. Cjeloviti pristup svim tablicama ima samo
  Davatelj, tim ključem.
- **Šifriranje pohranjenih podataka i sigurnosne kopije**: obavlja ih pružatelj
  baze. Koji je opseg šifriranja, postoje li sigurnosne kopije na odabranom
  planu i koliko se dugo čuvaju, Davatelj mora provjeriti u svojim postavkama i
  upisati ovdje. To je bitno jer određuje i koliko dugo obrisani podatak još
  postoji u kopijama (članak 6.3). **[VLASNIK POTVRĐUJE]**
- **Dvofaktorska prijava na račune Davatelja** kod pružatelja usluga: Davatelj
  mora potvrditi da je uključena. **[VLASNIK POTVRĐUJE]**
- **Postupanje pri povredi podataka**: u slučaju povrede koja predstavlja rizik
  za Korisnike, Davatelj obavještava AZOP u roku od 72 sata (GDPR čl. 33) i
  ugrožene Korisnike bez nepotrebne odgode (čl. 34).

## 11. Maloljetnici

Aplikacija nije namijenjena osobama mlađima od 18 godina. Davatelj ne prikuplja
namjerno podatke maloljetnika. Ako roditelj ili zakonski zastupnik utvrdi da je
dijete mlađe od 18 godina registrirano, neka kontaktira Davatelja koji će račun
obrisati bez naknade.

## 12. Promjene Politike privatnosti

Davatelj može mijenjati ovu Politiku. Izmijenjeni tekst objavljuje se u
Aplikaciji, na stranici "Pravila i privatnost", uz navođenje datuma izmjene, i
primjenjuje se 30 dana nakon objave.

**Nastavak korištenja nije prihvaćanje bitne izmjene.** Ranija inačica ovog
članka govorila je suprotno. Smjernice o transparentnosti (WP260 rev.01, t. 29
do 31, str. 16 do 18) uputu ispitaniku da sam prati promjene ocjenjuju ne samo
nedostatnom nego i nepoštenom u odnosu na načelo poštenosti iz čl. 5. st. 1. t.
(a) GDPR-a, i traže da se bitne izmjene priopće načinom kojim će ih većina
primatelja stvarno primijetiti, zasebno od drugog sadržaja i znatno prije nego
što počnu proizvoditi učinke.

Bitnima se smatraju barem ove izmjene, i one se priopćuju pojedinačno:

- promjena svrhe obrade ili uvođenje nove svrhe;
- promjena identiteta voditelja obrade;
- promjena načina na koji Korisnik ostvaruje svoja prava;
- skraćenje ili produljenje roka čuvanja iz članka 7.;
- uvođenje novog primatelja podataka ili novog prijenosa izvan EGP-a.

**Kako se to sada provodi. [NIJE AKTIVNO]** Automatsko slanje obavijesti
e-mailom nije uspostavljeno (vidi članak 8.). Dok se ne uspostavi, Davatelj je
dužan takvu obavijest poslati ručno, na adresu iz računa Korisnika, prije nego
izmjena počne vrijediti. Za korisnike koji rade kao gosti Davatelj nema adresu i
ne može ih obavijestiti; o gostima se ne pohranjuje nikakav podatak (članak 2.1),
pa se na njih izmjena odnosi tek od trenutka objave u Aplikaciji.

Korisnik koji se s izmjenom ne slaže može zatražiti brisanje računa bez naknade.

## 13. Kontakt

Pitanja, primjedbe i GDPR zahtjevi šalju se na: **<<< VLASNIK UPISUJE: kontakt e-mail za GDPR >>>**

Davatelj odgovara u roku iz uvoda članka 6.: bez nepotrebnog odgađanja, a
najkasnije u roku od mjesec dana, uz mogućnost produljenja za najviše dodatna dva
mjeseca uz obavijest o razlogu.

---

**Datum stupanja na snagu**: danom objave u Aplikaciji, na stranici "Pravila i
privatnost".

> **Napomena o prihvaćanju. [NIJE AKTIVNO]** Raniji tekst je ovdje govorio da
> Politika stupa na snagu danom kad je Korisnik prihvati pri registraciji ili pri
> prvoj pretplati. Takav korak u Aplikaciji ne postoji: obrazac za registraciju
> nema kućicu za prihvaćanje, prijavna se stranica u zadanom načinu rada uopće ne
> prikazuje (članak 2.1), a naplata nije aktivna (članak 2.6). Zato se ovdje ne
> tvrdi prihvaćanje kojeg nema.
>
> **Dopuna 10.8.2026.** Raniji tekst je ovdje stajao da registracija podatke
> prikuplja bez da se ovaj dokument ikad prikaže i da to Davatelj mora riješiti
> izmjenom Aplikacije. Izmjena je napravljena: na svakom mjestu unosa, uključujući
> prijavu i registraciju, stoji kratka obavijest o obradi s poveznicom na ovaj
> dokument. Prihvaćanje se i dalje ne traži, a kratka obavijest ne pokriva sve
> stavke članka 13. nego za ostalo upućuje ovamo.
>
> Ono što i dalje nedostaje: voditelj obrade i njegov kontakt nisu upisani, pa
> obavijest ne ispunjava članak 13. stavak 1. točke (a) i (b) dok se ne popune.
> Bez kontakta zahtjev za ostvarivanje prava nema kamo.

**Posljednja izmjena**: 2026-08-10 (nacrt v1.3)

### Što je izmijenjeno u v1.3

- **Obavijest u trenutku prikupljanja** (članak 2.1 i napomena uz datum stupanja
  na snagu). Raniji tekst je tvrdio da Aplikacija ovu Politiku ne prikazuje ni u
  jednom načinu rada, ni pri registraciji, i da to Davatelj mora riješiti izmjenom
  Aplikacije. Izmjena je napravljena, pa je ta tvrdnja postala netočna i
  ispravljena je: na svakom mjestu unosa osobnih podataka, uključujući prijavu i
  registraciju, stoji kratka obavijest o obradi s poveznicom na ovaj dokument.
- Zadržano je i izrijekom rečeno što obavijest **ne** rješava: prihvaćanje se ne
  traži, primatelji i prijenos izvan EGP-a i kolačići nisu u kratkoj obavijesti
  nego samo ovdje, a voditelj obrade i kontakt i dalje nisu upisani, pa obavijest
  ne ispunjava članak 13. stavak 1. točke (a) i (b).


### Što je izmijenjeno u v1.2 (isti dan, nakon usporedbe s praksom AZOP-a)

Popis je zaveden i u `docs/politika_usporedba.md`, zajedno s onim što nije
promijenjeno jer traži vlasnikovu odluku.

- **Prijenos izvan EGP-a** (članak 5.): "obrada se može odvijati izvan EU"
  zamijenjeno je jednoznačnom tvrdnjom da se prijenos odvija. Ograđena
  formulacija te vrste izričito je sankcionirana u rješenju AZOP-a protiv
  teleoperatora.
- **Automatizirano donošenje odluka i profiliranje** (novi članak 3.1): ranije
  nije bilo spomenuto ni potvrdno ni niječno, a riječ je o obveznom elementu iz
  GDPR čl. 13. st. 2. t. (f).
- **Je li davanje podataka obvezno** (novi članak 3.2): obvezni element iz GDPR
  čl. 13. st. 2. t. (e), ranije je nedostajao.
- **Rok za odgovor na zahtjev** (članak 6., 6.5, 13.): umjesto ravnih 30 dana
  sada stoji zakonski rok od mjesec dana uz mogućnost produljenja za dva mjeseca
  (GDPR čl. 12. st. 3.).
- **Provjera identiteta podnositelja zahtjeva** (članak 6.): dodana, po GDPR čl.
  12. st. 6. i po AZOP-ovu obrascu politike privatnosti.
- **Učinak povlačenja privole** (članak 6.6): dodano da povlačenje ne dira
  zakonitost ranije obrade (GDPR čl. 7. st. 3.).
- **Obavijest o izmjenama** (članak 12.): uklonjena je konstrukcija po kojoj
  nastavak korištenja znači prihvaćanje izmjene, uz popis izmjena koje se
  priopćuju pojedinačno. Smjernice o transparentnosti takvu konstrukciju
  ocjenjuju nepoštenom.
- **Zaštita na razini retka** (članci 4. i 10.): ranije je stajala kao činjenica.
  Sada je odvojeno pravilo koje je zapisano u bazi od stanja u kojem to pravilo
  nikome ništa ne odobrava, jer Aplikacija korisnika ne prijavljuje na bazu.
  Dodano je i da tablica `stripe_events` nema zaštitu na razini retka.
- **Ulaz u Aplikaciju** (članak 2.1): dodan je zadani način rada, u kojem se
  prijavna stranica uopće ne prikazuje, i činjenica da se ova Politika nigdje ne
  prikazuje sama od sebe.
- **Datum stupanja na snagu**: uklonjena tvrdnja o prihvaćanju pri registraciji,
  jer takav korak u Aplikaciji ne postoji.
- **Nepohranjivanje sadržaja** (članak 2.4): dodana izjava o zabrani sekundarne
  uporabe (nema profiliranja, oglašavanja ni učenja modela) i upozorenje da
  uneseni sadržaj može biti osjetljiv.
- **Tuđa adresa za podsjetnik** (članak 2.5): dodana točka 3, jer osoba čiju
  adresu Korisnik upiše od Davatelja ne dobiva nikakvu obavijest.
- **Kolačići** (članak 3.): pravni okvir za nužne kolačiće promijenjen je s
  legitimnog interesa na izuzeće iz čl. 43. st. 4. Zakona o elektroničkim
  komunikacijama, uz napomenu da izjašnjenje AZOP-a o tom pitanju nije nađeno.
- **Rokovi čuvanja** (članak 7.): dodano je koji redci tablice ne zadovoljavaju
  mjerilo iz Smjernica o transparentnosti i zašto se pravilo o neaktivnom računu
  ne može postaviti dok se ne bilježi datum zadnje prijave.
- **Prelazak računa u bazu** (članci 2.2 i 2.3): dodano upozorenje da pripremljena
  shema ima stupce za datum zadnje prijave i za trajni identifikator OAuth računa,
  pa niječne tvrdnje iz tih članaka prestaju vrijediti onog dana kad se shema
  primijeni.
- **Što se prima pri plaćanju** (članak 2.6): rečenica "Davatelj dobiva samo
  potvrdu da je pretplata aktivna" bila je u proturječju s popisom tri retka
  iznad, koji kaže da se sprema cjelovit zapis događaja s e-mailom kupca.
  Ispravljeno u korist popisa.
- **Identitet primatelja** (članak 5.): za pružatelja hostinga i za Polar naziv
  pravne osobe više se ne navodi kao utvrđen, jer iz repozitorija nije provjerljiv.
  Za Stripe je uklonjena tvrdnja da se obrada odvija u EU (Irskoj), koja je bila
  tvrdnja o lokaciji obrade, a ne o sjedištu ugovorne strane. Dodana je napomena
  da tablici nedostaju adrese i registracijski brojevi.

### Što je izmijenjeno u odnosu na v1.0

- Rok čuvanja zapisa o dokumentima: raniji tekst je tvrdio automatsko brisanje
  koje ne postoji. Sada je opisano pražnjenje osobnih stupaca uz zadržavanje
  sažetaka, s razlogom, i označeno je da posao još nije postavljen.
- Dodano je da se registracija sprema u datoteku na poslužitelju, a ne u bazu, i
  da ti podaci mogu nestati pri ponovnom pokretanju.
- Dodan je članak o kalendaru, koji ranije nije bio spomenut, uključujući
  upozorenje da unosi nisu odvojeni po korisniku.
- Uklonjena je tvrdnja da se pohranjuju trajni identifikatori Google i Apple
  računa i datum zadnje prijave; to se ne pohranjuje.
- Uklonjena je tvrdnja o obradi IP adrese radi ograničavanja zahtjeva i
  otkrivanja prijevara; aplikacija IP adresu ne obrađuje.
- Uklonjen je kolačić "Supabase auth JWT, 30 dana"; aplikacija ga ne postavlja.
- Tvrdnja o sklopljenim ugovorima o obradi, regiji baze i mehanizmu prijenosa
  izvan EU pretvorena je u stavku koju Davatelj mora potvrditi.
- Dodani su `stripe_events` i sadržaj koji zapis nosi, te je označeno da za njih
  rok čuvanja nije određen.
- Ispravljen je opis vidljivosti serijskog broja: podnožje i XML metapodaci
  postoje u oba tiera.
- Označeno je što u trenutnoj konfiguraciji ne radi: zapisivanje preuzimanja,
  naplata, prijava Appleom.

Ispravljeno nakon provjere unutar iste inačice v1.1:

- Tvrdnja da se lančani sažetak ispražnjenog zapisa "ne može ponovno izračunati"
  bila je netočna i proturječila je popisu dva reda iznad: sažetak prethodnog
  zapisa, koji je jedan od ulaza u račun, ostaje u istom retku. Članak 7.1 sada
  navodi koliko je ulaza poznato i što se time stvarno može, a što ne.
- Popisu onoga što ostaje u ispražnjenom retku dodana je interna oznaka retka;
  raniji tekst je tvrdio da se briše "sve ostalo".
- Tvrdnja da provjera lanca otkriva naknadnu izmjenu dopunjena je ogradom: ne
  otkriva izmjenu koju je pratio preračun cijelog niza.
- Članak 2.4 sada kaže i da se iz sažetka može potvrditi pogodak, ne samo da se
  ne može rekonstruirati sadržaj.
- Pravna ocjena o statusu ispražnjenog retka dopunjena je pozivom na GDPR čl. 11
  st. 1 i izričitom napomenom da AZOP o tome nije zauzeo stav.
- Uvjeti korištenja (`stranice/tos.md`, članak 3.4) tvrdili su da brisanje
  računa obuhvaća sve podatke; usklađeni su s člankom 7.1.
