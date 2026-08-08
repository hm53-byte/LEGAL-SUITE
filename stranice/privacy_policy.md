# Politika privatnosti - LEGAL-SUITE

**Verzija**: 1.1 (nacrt 2026-08-09)
**Status**: NACRT. Nije spreman za objavu.

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

Aplikacija nudi gumb "Isprobaj besplatno". Klikom se otvara sesija pod
zajedničkom internom oznakom `gost@legalsuite.hr`. Ta oznaka nije adresa
korisnika i ne stvara se korisnički zapis: o gostu se ne pohranjuje ništa što bi
ga identificiralo.

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

### 2.3 Prijava preko Googlea

Ako Korisnik odabere prijavu Googleom, Davatelj od Googlea prima e-mail adresu i
ime s Googleova profila. Ti podaci žive samo u tekućoj sesiji i ne upisuju se
ni u jednu datoteku ni bazu. Trajni identifikator Google računa (`sub`) se
ne prima i ne pohranjuje.

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
tijekom generiranja i odmah se odbacuje. Generirani `.docx` vraća se Korisniku
izravno; kopija se ne čuva.

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

**Podatke o kartici ne prikupljamo niti pohranjujemo.** Plaćanje se odvija
izravno između Korisnika i pružatelja naplate (Polar.sh, koji nastupa kao
Merchant of Record); Davatelj dobiva samo potvrdu da je pretplata aktivna. U
kodu postoji i naslijeđena Stripe integracija; ako je aktivirana, isto vrijedi
za Stripe.

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
| Cookies nužni za rad sesije | Legitiman interes (čl. 6(1)(f)) | Aplikacija bez sesije ne može raditi |

Obrada IP adrese ne navodi se u ovoj tablici jer je aplikacija ne obavlja (vidi
članak 2.7).

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

**Tko može čitati tablicu.** Na tablici je uključena zaštita na razini retka:
prijavljeni Korisnik može čitati i unositi samo vlastite retke, a cjeloviti uvid
ima jedino Davatelj preko servisnog ključa baze. Za brisanje i izmjenu retka ne
postoji nijedno pravilo, što znači da se iz aplikacije redak ne može ni obrisati
ni promijeniti; to je moguće samo servisnim ključem.

## 5. Tko ima pristup vašim podacima (treće strane)

| Treća strana | Što vidi | Gdje | Razlog |
|---|---|---|---|
| **Streamlit Inc.** (San Francisco, CA, SAD) | Promet prema aplikaciji, uključujući IP adresu i User-Agent u vlastitim zapisima; datoteke `.users.json` i `_data/kalendar.json` nalaze se na njihovom poslužitelju | SAD | Hosting Aplikacije |
| **Supabase Inc.** (San Francisco, CA, SAD) | Podaci iz članaka 2.4 i 2.6 kad su te funkcije aktivirane; ne vidi sadržaj dokumenata | Regija koju je Davatelj odabrao pri otvaranju projekta **[VLASNIK POTVRĐUJE]** | Baza podataka |
| **Cloudflare Inc.** (San Francisco, CA, SAD) | Webhook događaji pružatelja naplate (identifikator i e-mail kupca, plan, status) | Cloudflareova globalna mreža; obrada se ne odvija nužno unutar EU **[VLASNIK POTVRĐUJE]** | Obrada webhookova o plaćanju |
| **Polar.sh** (Polar Software Inc.) | E-mail, podaci o kartici, podaci o transakciji | Prema Polarovoj politici privatnosti | Procesiranje plaćanja (Merchant of Record) |
| **Stripe Payments Europe Ltd.** (Dublin, Irska) | E-mail, podaci o kartici, podaci o transakciji | EU (Irska) | Procesiranje plaćanja (naslijeđena integracija; vrijedi samo ako je Stripe checkout aktiviran) |
| **SMTP pružatelj za podsjetnike** | E-mail adresa primatelja i sadržaj podsjetnika (naslov, datum, opis, oznaka predmeta) | Prema uvjetima pružatelja **[VLASNIK POTVRĐUJE]** | Slanje podsjetnika iz kalendara |
| **Google LLC** | E-mail i ime s Google profila, ako Korisnik odabere prijavu Googleom | Prema Googleovoj politici privatnosti | Prijava vanjskim računom |

**Prijenos izvan EU.** Streamlit i Cloudflare imaju sjedište u SAD-u i obrada se
može odvijati izvan EU. Za takav prijenos potreban je valjan mehanizam iz GDPR
poglavlja V (standardne ugovorne klauzule ili odluka o primjerenosti). Koji
mehanizam vrijedi za svakog pružatelja i je li prihvaćen, Davatelj mora
utvrditi i ovdje navesti. **[VLASNIK POTVRĐUJE]**

**Ugovori o obradi (GDPR čl. 28).** Postojanje potpisanog ugovora o obradi s
pojedinim pružateljem ne vidi se iz aplikacije ni iz repozitorija. Prije objave
Davatelj mora za svakog pružatelja iz tablice provjeriti je li ugovor o obradi
sklopljen (kod većine se prihvaća u administracijskom sučelju računa) i tek onda
ovdje napisati da postoji. **[VLASNIK POTVRĐUJE]**

## 6. Vaša prava (GDPR)

Sukladno GDPR-u i Zakonu o provedbi Opće uredbe o zaštiti podataka (NN 42/18),
Korisnik ima sljedeća prava. Sva se ostvaruju slanjem zahtjeva na kontakt adresu
iz članka 13. **U Aplikaciji ne postoji samoposlužno sučelje za ta prava**, pa
ih Davatelj obrađuje ručno, u roku od 30 dana.

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
zapis o generiranim dokumentima). Davatelj odgovara u roku od 30 dana; ako
prigovor smatra opravdanim, prestaje s tom obradom osim ako postoje uvjerljiviji
legitimni razlozi.

### 6.6 Pravo na povlačenje privole

Ne primjenjuje se na obrade utemeljene na ugovoru ili legitimnom interesu (vidi
članak 3). Primjenjuje se na eventualne marketinške poruke za koje je dana
zasebna privola (vidi članak 8).

### 6.7 Pravo žalbe nadzornom tijelu

Korisnik se može žaliti **Agenciji za zaštitu osobnih podataka** (AZOP),
www.azop.hr, ako smatra da Davatelj ne poštuje GDPR. Adresu i kontakt AZOP-a
Davatelj treba provjeriti na dan objave dokumenta i upisati ovdje.
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
- **Pristup podacima u bazi**: zaštita na razini retka (Korisnik vidi samo svoje
  retke), a cjeloviti pristup ima samo Davatelj preko servisnog ključa.
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
primjenjuje se 30 dana nakon objave. Korisnik koji nastavi koristiti Aplikaciju
nakon toga prihvaća izmjene; ako se ne slaže, može zatražiti brisanje računa bez
naknade.

Automatsko slanje obavijesti o izmjenama e-mailom nije uspostavljeno (vidi
članak 8). Ako Davatelj takvu obavijest bude slao, slat će je na adresu iz
računa Korisnika.

## 13. Kontakt

Pitanja, primjedbe i GDPR zahtjevi šalju se na: **<<< VLASNIK UPISUJE: kontakt e-mail za GDPR >>>**

Davatelj odgovara u roku od 30 dana.

---

**Datum stupanja na snagu**: dan kad Korisnik prihvati ovu Politiku pri
registraciji ili pri prvoj pretplati nakon ažuriranja.

**Posljednja izmjena**: 2026-08-09 (nacrt v1.1)

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
