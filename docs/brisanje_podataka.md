# Brisanje podataka: što vlasnik mora napraviti

Ovaj dokument opisuje jedan konkretan posao: čišćenje tablice `download_log`
nakon 24 mjeseca, onako kako to obećava politika privatnosti
(`stranice/privacy_policy.md`, članak 7).

Tri stvari koje treba znati prije nego išta pokreneš:

1. **Aplikacija to ne može napraviti sama.** Tablica ima zaštitu na razini retka
   bez pravila za `UPDATE` i `DELETE`, pa iz aplikacije nitko ne može mijenjati
   ni brisati retke. Posao se postavlja u samoj bazi, servisnim ovlaštenjem.
2. **Ništa se ne izvodi dok ti to ne postaviš.** Migracija je napisana i leži u
   repozitoriju, ali datoteka u repozitoriju ne mijenja tvoju bazu.
3. **Redak se ne briše, nego prazni.** Objašnjenje je u odjeljku "Zašto se ne
   briše cijeli redak".

Ništa u ovom dokumentu nije isprobano na tvojoj bazi. Nemamo pristup tvom
Supabase projektu i nismo ga tražili. Sve je napisano iz shema koje se nalaze u
repozitoriju (`cloud/supabase_schema.sql`, `cloud/0007_audit_chain.sql`,
`cloud/0008_retencija_download_log.sql`). Zato svaki korak ima i provjeru: ne
oslanjaj se na to da je nešto uspjelo, nego pogledaj.

---

## Stanje prije početka

`download_log` je danas prazan i ostat će prazan dok ne povežeš prijavu s bazom.
Upis zapisa traži oznaku korisnika koju postavlja prijava, a trenutna prijava
(`auth.py`) je ne stvara: korisnici žive u lokalnoj datoteci `.users.json`, a ne
u Supabase tablici `users`.

To ne znači da ovaj posao treba odgoditi. Znači obrnuto: postavi ga sada, dok je
tablica prazna i dok migracija ne može ništa pokvariti, pa kad prvi zapis
nastane, rok već teče. Redoslijed je bitan i u tekstu politike privatnosti:
tvrdnja da se zapisi čiste smije stajati tek kad ovaj posao radi.

Provjeri prvo da su prethodne migracije primijenjene. U Supabase Dashboardu,
**SQL Editor**, pokreni:

```sql
SELECT column_name
  FROM information_schema.columns
 WHERE table_name = 'download_log'
 ORDER BY ordinal_position;
```

Očekuje se 13 stupaca: `id`, `user_id`, `doc_type`, `doc_subtype`,
`serial_hash`, `plan_at_download`, `generated_at`, pa šest stupaca lanca
(`input_canonical_hash`, `output_sha256`, `parent_hash`, `current_hash`,
`generator_version_hash`, `input_schema_version`).

Ako stupaca lanca nema, prvo primijeni `cloud/0007_audit_chain.sql`. Ako nema ni
tablice, kreni od `cloud/supabase_schema.sql`.

---

## Korak 1: primijeni migraciju

1. Otvori **https://supabase.com/dashboard**, odaberi svoj projekt.
2. U lijevom izborniku klikni **SQL Editor**, pa **New query**.
3. Otvori datoteku `cloud/0008_retencija_download_log.sql` iz repozitorija,
   označi cijeli sadržaj i zalijepi ga u prozor upita.
4. Klikni **Run** (dolje desno, ili Cmd+Enter).

Skripta je idempotentna: ponovno pokretanje ne kvari ništa i ne stvara duplikate.
Ako nešto zapne na pola, popravi uzrok i pokreni je cijelu ponovno.

**Što očekivati u odgovoru.** Zadnja naredba u datoteci je `SELECT`, pa rezultat
nije "Success. No rows returned" nego jedan redak sa četiri stupca. Gledaj
stupac `raspored`:

| Početak vrijednosti | Značenje | Kamo dalje |
|---|---|---|
| `POSTAVLJEN:` | pg_cron posao je prijavljen | korak 3 |
| `NEMA: pg_cron nije ukljucen` | ekstenzija nije uključena | korak 2 |
| `NEMA: <poruka o grešci>` | ostatak migracije je primijenjen (funkcije, ograničenje, indeks), nedostaje samo raspored | pročitaj poruku, riješi uzrok, pokreni skriptu ponovno; ili korak 4 |
| `NEPOZNATO:` | blok koji postavlja raspored nije došao do kraja | provjeri upitom iz koraka 3 |

Taj redak postoji zato što Supabaseovo sučelje ne prikazuje pouzdano poruke
razine `NOTICE`. Da se ishod javljao samo njima, migracija bi mogla završiti s
"Success" i bez postavljenog rasporeda, a to je jedini korak koji tvrdnju iz
politike privatnosti čini istinitom. Poruke `NOTICE` se i dalje ispisuju, ako ih
sučelje pokaže; redak iz rezultata je mjerodavan.

**`POSTAVLJEN` znači da posao postoji, ne da se izvršio.** Prvo izvršavanje je
tek iduće noći. Potvrda je u koraku 3.

---

## Korak 2: uključi pg_cron ako nije uključen

1. U lijevom izborniku **Database**, pa **Extensions**.
2. U tražilicu upiši `pg_cron`.
3. Uključi prekidač. Supabase će tražiti potvrdu sheme u koju se ekstenzija
   instalira; ostavi predloženu.
4. Vrati se u **SQL Editor** i pokreni `cloud/0008_retencija_download_log.sql`
   još jednom, cijelu. Sad bi trebala doći obavijest da je posao postavljen.

Ako `pg_cron` nema na popisu ekstenzija ili se ne da uključiti, tvoj plan ga ne
podržava. To nije prepreka: idi na korak 4, pričuvna skripta radi isti posao
izvana. Je li `pg_cron` dostupan na tvom planu, ne može se utvrditi iz
repozitorija.

---

## Korak 3: provjeri da je raspored živ

"Raspored postoji" i "raspored radi" nisu isto. Provjeri oboje.

**Postoji li posao i je li uključen:**

```sql
SELECT jobid, jobname, schedule, active, command
  FROM cron.job
 WHERE jobname = 'download_log_retencija';
```

Očekuje se jedan redak, `schedule` = `17 3 * * *`, `active` = `true`. Nula
redaka znači da raspored nije postavljen. O tome u kojoj se zoni raspored tumači
vidi odjeljak "Rub roka: 29. veljače i vremenska zona".

**Je li se doista izvršio:**

```sql
SELECT d.status, d.return_message, d.start_time, d.end_time
  FROM cron.job_run_details d
  JOIN cron.job j ON j.jobid = d.jobid
 WHERE j.jobname = 'download_log_retencija'
 ORDER BY d.start_time DESC
 LIMIT 10;
```

Očekuje se barem jedan redak sa `status` = `succeeded`, a `return_message`
sadrži broj obrađenih redaka. Prazna lista odmah nakon postavljanja je uredna:
prvo izvršavanje je tek sljedeće noći. Vrati se na ovaj upit sutradan.

Ako sutradan i dalje nema retka, ili `status` nije `succeeded`, posao ne radi.
Pročitaj `return_message`, i dok se to ne riješi, koristi pričuvnu skriptu.

**Ne moraš čekati noć da vidiš radi li funkcija.** Pozovi je ručno:

```sql
SELECT download_log_anonimiziraj(24);
```

Vraća broj obrađenih redaka. Na praznoj tablici vraća `0`, i to je uredan
odgovor: znači da je funkcija tu i da je prošla bez greške. To je i jedina
provjera koja se na praznoj tablici može napraviti bez izmišljenih podataka.

---

## Korak 4: pričuvna skripta, ako pg_cron nije dostupan

Skripta `scripts/retencija_download_log.py` radi isti posao izvana, preko REST
sučelja baze. Koristi je kad `pg_cron` nije dostupan ili kad raspored ne radi.

**Što joj treba.** Servisni ključ baze (`service_role`), jer se anonimizacija
izvodi zaobilaženjem zaštite na razini retka. Anon ključ ovdje ne radi i to nije
propust nego namjera.

Servisni ključ nikad ne ide u Streamlit secrets, u repozitorij, ni u chat.
Nalazi se u Supabase Dashboardu pod **Settings**, pa **API**, kao `service_role`.

**Pokretanje** (iz korijena repozitorija). Bez zastavice `--izvrsi` skripta radi
suhi hod: ispiše koliko bi redaka dirnula i ne mijenja ništa. To je zadano stanje
i s njim uvijek počni.

```bash
export SUPABASE_URL="https://<tvoj-projekt>.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="<service_role kljuc>"

# 1) suhi hod, nista se ne mijenja
python -m scripts.retencija_download_log

# 2) stvarno izvrsenje
python -m scripts.retencija_download_log --izvrsi
```

U suhom hodu skripta ispiše granicu (`generated_at <= ...`), broj pogođenih
redaka i najviše deset najstarijih, s datumom, tipom dokumenta i početkom oznake
retka. Oznaku korisnika i sažetak serijskog broja ne ispisuje namjerno: taj ispis
završi u dnevniku, koji je slabije zaštićen od baze.

Ostale zastavice: `--mjeseci` mijenja rok (zadano 24), `--uzorak` mijenja koliko
se redaka ispisuje, `--suhi-hod` izričito traži suhi hod. Ako navedeš i
`--izvrsi` i `--suhi-hod`, pobjeđuje suhi hod.

**Kako znaš je li prošlo.** Po izlaznom kodu procesa (`echo $?` odmah nakon
pokretanja):

| Kod | Značenje |
|---|---|
| 0 | Gotovo. Vrijedi i za suhi hod i za slučaj kad nema redaka za obradu. |
| 2 | Nije podešeno: nedostaje varijabla okoline ili ključ nije `service_role`. Ništa nije dirano. |
| 3 | Greška u komunikaciji sa Supabaseom, uključujući prekid mreže i istek vremena. Vidi "Kod 3 ne znači da ništa nije obrisano". |
| 4 | Neispravan argument (rok izvan raspona 1 do 1200 mjeseci, ili nije cijeli broj). |
| 1 | Nepredviđena greška. Ne bi se smjelo dogoditi; ako se dogodi, u dnevniku je trag stoga. To je kvar skripte, a ne stanje baze. |

Kod 2 je čest i koristan: skripta odbija raditi s anon ključem umjesto da tiho
obradi nula redaka i ostavi dojam da je posao odrađen.

**Kod 3 ne znači da ništa nije obrisano.** Pisanje je jedan `PATCH`, dakle jedna
`UPDATE` naredba u jednoj transakciji: ili prođu svi pogođeni retci ili nijedan.
Djelomično ispražnjena tablica nije moguća, čak ni ako se veza prekine usred
posla. Ali ako se prekine **nakon** što je baza već izvršila naredbu, a prije
nego što je odgovor stigao natrag, skripta prijavljuje grešku, a retci su
ispražnjeni. Obrnuto se ne događa: uspješan izlaz nikad ne znači da nije
zapisano.

Zato kod 3 čitaj kao "ne znam je li prošlo", ne kao "nije prošlo". Provjeri
upitom iz koraka 5. Ponovno pokretanje je bezopasno: uvjet `anonymized_at IS
NULL` preskoči već obrađene retke.

Najvjerojatniji uzrok koda 3 na velikoj tablici je istek vremena. Skripta čeka
odgovor 15 sekundi, a prvi prolaz nakon uvođenja retencije može dirati sve retke
starije od 24 mjeseca odjednom. Skripta nema obradu u serijama. Ako se to
dogodi, provjeri upitom iz koraka 5 je li posao ipak prošao, pa po potrebi
pokreni ponovno.

**Koliko često.** Jednom dnevno je dovoljno. Rok je 24 mjeseca, pa dan
zakašnjenja nije problem; tjedni razmak već znači da zapis može ostati do sedam
dana duže nego što politika privatnosti obećava.

**Ako je pokrećeš s vlastitog računala**, znaj što si dobio: posao se izvodi samo
kad je računalo upaljeno. To je slabija garancija od rasporeda u bazi i nije
dobro trajno rješenje. Ako mora tako, na Linuxu ide u `crontab -e`, na macOS-u u
`launchd` (datoteka u `~/Library/LaunchAgents/`). Primjer retka za obični cron,
svaki dan u 03:17, s dnevnikom:

```
17 3 * * * cd /put/do/LEGAL-SUITE && SUPABASE_URL=... \
  SUPABASE_SERVICE_ROLE_KEY=... /put/do/python \
  -m scripts.retencija_download_log --izvrsi >> /var/log/retencija.log 2>&1
```

Povremeno pogledaj taj dnevnik. Posao koji tiho ne radi izgleda isto kao posao
koji radi.

---

## Korak 5: kako provjeriti da je nešto stvarno obrisano

Ne vjeruj poruci "Success". Pogledaj podatke.

**Stanje tablice:**

```sql
SELECT count(*)                                            AS ukupno,
       count(*) FILTER (WHERE anonymized_at IS NULL)       AS zivi,
       count(*) FILTER (WHERE anonymized_at IS NOT NULL)   AS ocisceni,
       min(generated_at) FILTER (WHERE anonymized_at IS NULL) AS najstariji_zivi
  FROM download_log;
```

Ključan je `najstariji_zivi`. Ako je stariji od 24 mjeseca, posao ne radi kako
treba, bez obzira na to što piše u dnevnicima.

**Koliko bi posao obradio da se pokrene sada** (ne mijenja ništa):

```sql
SELECT count(*)
  FROM download_log
 WHERE anonymized_at IS NULL
   AND generated_at <= now() - make_interval(months => 24);
```

Ako ovo vrati broj veći od nule, a raspored je navodno živ, nešto je puklo
između rasporeda i funkcije.

**Kako izgleda očišćen redak:**

```sql
SELECT id, generated_at, anonymized_at,
       user_id, doc_type, doc_subtype, serial_hash, plan_at_download,
       input_canonical_hash, output_sha256, generator_version_hash,
       parent_hash, current_hash
  FROM download_log
 WHERE anonymized_at IS NOT NULL
 ORDER BY anonymized_at DESC
 LIMIT 5;
```

Ispravan rezultat: `generated_at`, `anonymized_at`, `parent_hash` i
`current_hash` imaju vrijednost, svi ostali stupci su prazni. Ako je bilo koji
osobni stupac popunjen, a `anonymized_at` postavljen, ograničenje u bazi je
zaobiđeno i to treba istražiti odmah.

Suprotan smjer provjere, prebrojavanje onoga što je ostalo gdje ne bi smjelo:

```sql
SELECT count(*)
  FROM download_log
 WHERE anonymized_at IS NOT NULL
   AND (user_id IS NOT NULL OR serial_hash IS NOT NULL OR doc_type IS NOT NULL);
```

Očekivani odgovor je `0`. Bilo koji drugi broj znači da posao nije napravio ono
što politika privatnosti tvrdi.

**Provjera na praznoj tablici.** Dok zapisa nema, gore navedeni upiti vraćaju
nule i ne dokazuju da čišćenje radi, samo da ne pada. Ako želiš vidjeti postupak
na djelu prije nego što nastanu stvarni zapisi, umetni jedan testni redak sa
starim datumom, pokreni funkciju i pogledaj rezultat. Testni redak traži
postojećeg korisnika u tablici `users`, jer stupac `user_id` ima stranu vezu na
nju:

```sql
-- 1) uzmi bilo koji postojeci user_id
SELECT id FROM users LIMIT 1;

-- 2) umetni testni redak star 25 mjeseci (zamijeni <UUID> gornjim id-em)
INSERT INTO download_log
    (user_id, doc_type, doc_subtype, serial_hash, plan_at_download, generated_at,
     input_canonical_hash, output_sha256, parent_hash, current_hash,
     generator_version_hash, input_schema_version)
VALUES
    ('<UUID>', 'test', 'test', repeat('a', 64), 'free',
     now() - interval '25 months',
     repeat('b', 64), repeat('c', 64), NULL, repeat('d', 64),
     repeat('e', 64), 'v1');

-- 3) pokreni posao i pogledaj sto se dogodilo
SELECT download_log_anonimiziraj(24);
SELECT * FROM download_log WHERE current_hash = repeat('d', 64);

-- 4) ukloni testni redak
DELETE FROM download_log WHERE current_hash = repeat('d', 64);
```

Korak 4 je bezopasan samo dok je redak testni i dok nijedan drugi redak ne
pokazuje na njegov `current_hash`. Testni redak ima izmišljene sažetke koji ne
odgovaraju nijednom stvarnom dokumentu, pa nikad ne postane karika stvarnog
lanca. Nikad ne briši stvarni redak istim postupkom.

---

## Brisanje računa na zahtjev korisnika (GDPR čl. 17)

Ovdje je redoslijed bitan i lako ga je pogriješiti. Tablica `download_log` ima
stranu vezu na `users` s pravilom `ON DELETE CASCADE`: ako obrišeš korisnika,
baza sama ukloni sve njegove retke iz `download_loga`. To je upravo ono što se
ne smije dogoditi, jer uklonjeni redak lomi lanac.

Ispravan redoslijed:

```sql
-- 1) prvo isprazni retke korisnika
SELECT download_log_anonimiziraj_korisnika('<UUID korisnika>');

-- 2) provjeri da mu nije ostao nijedan zivi redak (mora vratiti 0)
SELECT count(*) FROM download_log
 WHERE user_id = '<UUID korisnika>' AND anonymized_at IS NULL;

-- 3) tek sad obrisi korisnika
DELETE FROM users WHERE id = '<UUID korisnika>';
```

Nakon koraka 1 retci više nemaju `user_id`, pa ih `CASCADE` u koraku 3 ne dira.

Uz to, u današnjoj konfiguraciji korisnici zapravo žive u datoteci `.users.json`
na poslužitelju aplikacije, a ne u bazi. Brisanje računa na zahtjev znači i:

- ukloniti unos za tu e-mail adresu iz `.users.json`,
- ukloniti unose te osobe iz `_data/kalendar.json` ako ih ima, uključujući
  e-mail adrese upisane za podsjetnike.

Sve to je danas ručan posao. Za njega ne postoji sučelje ni skripta.

---

## Zašto se ne briše cijeli redak

Svaki zapis u `download_logu` nosi `current_hash` izračunat i iz `current_hash`
prethodnog zapisa. Tako nastaje lanac u kojem naknadna izmjena starog zapisa
razbije sve što dolazi poslije, što je i svrha.

Brisanje starog retka razbija isti lanac, samo na način koji se ne razlikuje od
zlonamjernog. Provjera vidi da veza vodi u prazno, ali ne može reći je li redak
nestao zato što je istekao rok ili zato što ga je netko uklonio. Kod retencije po
datumu reže se s najstarije strane, dakle upravo s one koja lomi lanac. Nekoliko
mjeseci nakon uključenja automatskog brisanja, lanac svakog dugogodišnjeg
korisnika izgledao bi kao krivotvorina.

Zato migracija stari redak prazni. Ostaju `generated_at`, `parent_hash` i
`current_hash`, plus oznaka `anonymized_at` koja kaže da je redak ispražnjen
zakonito. Veza u lancu ostaje cijela, jer sljedeći redak i dalje pokazuje na
postojeći `current_hash`.

Prazne se i `input_canonical_hash`, `output_sha256` i `generator_version_hash`,
iako nisu očit osobni podatak. Prva dva su sažeci sadržaja u kojem su ime, OIB i
adresa stranke. Sažetak je pseudonimizacija, ne anonimizacija: tko zna sadržaj,
može provjerom potvrditi da je riječ o tom dokumentu. Da ostanu, rok čuvanja iz
politike privatnosti ne bi bio ispoštovan.

Posljedica za provjeru lanca: ispražnjeni redak ne može se provjeriti sam za
sebe, jer podataka iz kojih se `current_hash` računao više nema. On je samo
nosač veze. Za provjeru koja to razumije služi
`audit_chain.verify_chain_retention_aware`.

**Tu provjeru pokreći samo servisnim ključem.** Zaštita na razini retka je
`user_id = auth.uid()`, a ispražnjeni redak nema `user_id`, pa je korisničkom
ključu nevidljiv. Provjera koja preko korisničkog ključa traži prethodnika neće
ga naći i prijavit će prekinutu vezu, dakle upravo lažnu uzbunu zbog koje
ispražnjeni redak i postoji.

**Što ta provjera ne može.** Tri stvari, sve tri stvarne i sve tri zapisane u
opisu funkcije:

1. Sadržaj ispražnjenog retka se ne provjerava, nego mu se vjeruje. Drukčije ne
   može, jer su ulazi obrisani. Tko ima pravo pisanja u bazu može bilo kojem
   retku obrisati sadržaj, postaviti oznaku ispražnjenosti i proći provjeru.
   Za razliku od brisanja retka, taj zahvat izgleda isto kao zakonita
   retencija. Neobavezni parametar `mjeseci_retencije` prijavljuje redak
   ispražnjen prije roka, ali hvata samo nemarnu izvedbu: oznaka trenutka
   pražnjenja nije ni u jednom sažetku, pa je onaj tko mijenja podatke može
   postaviti na vrijednost koja izgleda uredno.
2. Ispražnjeni redci na koje više ništa ne pokazuje nemaju nikakvu zaštitu.
   Nastaju kad Korisnik 24 mjeseca ne generira dokument: tada su svi njegovi
   redci ispražnjeni, sljedeći redak kreće kao novi korijen, a stari ostaju bez
   ijednog potomka. Mogu se izmijeniti ili ukloniti a da provjera to ne
   primijeti.
3. Tko prilikom izmjene retka preračuna sažetke i za taj redak i za sve
   sljedeće, prolazi i staru i novu provjeru. Obrana od toga traži vanjsko
   sidro, na primjer povremeni zapis zadnjeg sažetka izvan baze. Toga nema.

Ovo nisu razlozi da se lanac ne vodi. Lanac i dalje hvata izmjenu pojedinog
retka koju nitko nije popratio preračunom, i to je ono što se od njega tvrdi u
članku 7.1 politike privatnosti. Više od toga se ne smije tvrditi.

## Rub roka: 29. veljače i vremenska zona

**Prijestupni dan.** Redak od 29.02.2024. neće biti obrađen 28.02.2026., nego
tek 01.03.2026. Razlog je podrezivanje kalendarskog računa: 28.02.2026. minus 24
mjeseca daje 28.02.2024., a redak je stariji od te granice tek dan poslije.
Ispada 731 dan umjesto 730. To je jedini dan u četiri godine u kojem se rok
probija umjesto da se skrati. Alternativa (uspoređivati `generated_at + 24
mjeseca <= now()`) daje 28.02.2026., ali onda uvjet ne može koristiti indeks i
posao čita cijelu tablicu. Isto vrijedi za pričuvnu skriptu, pa se dva puta ne
razilaze.

**Vremenska zona.** Račun granice u bazi radi se u vremenskoj zoni sesije, a u
pričuvnoj skripti u UTC-u. Supabaseova zadana zona je UTC, pa se poklapaju.
Provjeri s `SHOW TimeZone;` ako mijenjaš zonu ili ako rok mijenjaš na broj
mjeseci koji nije višekratnik dvanaest; kod roka od 6 ili 18 mjeseci u zoni s
ljetnim računanjem vremena granice se razilaze za sat vremena.

**Raspored `17 3 * * *`** tumači se prema postavci `cron.timezone`, koja je
zadano GMT. Uz tu zadanu vrijednost posao se po hrvatskom vremenu izvodi u 04:17
zimi i 05:17 ljeti.

Starija `audit_chain.verify_chain` to ne zna. Na ispražnjenom retku ne vrati ni
uredan negativan odgovor, nego digne `TypeError`, jer pokuša spojiti prazne
sažetke u niz znakova. Provjereno pokretanjem, pokriveno testom
`test_stara_verify_chain_puca_na_nadgrobnom_retku`. Ostavljena je nepromijenjena
zbog zatečenih poziva, ali je nemoj koristiti na tablici na kojoj je čišćenje
uključeno.

Nova provjera preskače i zapise nastale prije uvođenja lanca
(`cloud/0007_audit_chain.sql`), koji nemaju nijedan sažetak. Oni nikad nisu ni
bili u lancu, pa bi inače svaki stariji račun javljao lažnu uzbunu.

---

## Što se događa ako ne napraviš ništa

**Dok je tablica prazna**, praktične štete nema. Politika privatnosti u sadašnjem
tekstu ne tvrdi da čišćenje radi: u članku 7.2 stoji oznaka `[NIJE AKTIVNO]` i
objašnjenje da posao treba postaviti. Dokle god ta oznaka ostane u tekstu,
dokument je istinit.

**Ako ukloniš tu oznaku, a posao ne postaviš**, politika privatnosti tvrdi
korisniku i nadzornom tijelu nešto što se ne događa. To je stanje od kojeg je
ovaj posao i krenuo.

**Kad zapisivanje profunkcionira, a čišćenje ne**, redom:

- Zapisi se gomilaju bez roka. Veza serijski broj prema korisniku ostaje trajno,
  pa se i pet godina star dokument može vezati uz osobu. To je povreda načela
  ograničenja pohrane (GDPR čl. 5 st. 1 t. (e)) i izravno proturječi roku od 24
  mjeseca iz vlastite politike privatnosti.
- Korisnik koji zatraži uvid dobiva popis svega što je ikad generirao, umjesto
  zadnje dvije godine.
- Prijava AZOP-u u toj situaciji ne traži vještačenje: dovoljno je usporediti
  tekst politike privatnosti s jednim upitom nad tablicom.
- Baza raste. Na besplatnom Supabase planu granica je 500 MB za cijelu bazu.

**Ako umjesto ovoga uvedeš obično brisanje redaka**, izgubit ćeš forenzičku
vrijednost lanca, i to najprije kod korisnika koje najdulje imaš. Vidi prethodni
odjeljak.

---

## Što ostaje neprovjereno

Ovo su stvari koje se ne mogu utvrditi iz repozitorija i koje mora provjeriti
vlasnik:

- **Je li `pg_cron` dostupan** na tvom Supabase planu i u tvojoj regiji.
- **U kojoj je regiji tvoj Supabase projekt.** Upute u `cloud/SETUP.md`
  predlažu Frankfurt, ali to je preporuka u dokumentu, a ne dokaz o tome što je
  odabrano. Vidi se u Dashboardu, **Settings**, pa **General**.
- **Jesu li ugovori o obradi sklopljeni** s Supabaseom, Streamlitom,
  Cloudflareom, Polarom i SMTP pružateljem. Iz koda se to ne vidi ni u naznakama.
- **Postoje li sigurnosne kopije i koliko se čuvaju.** Bitno je jer čišćenje ne
  dopire do postojećih kopija: podatak iz njih nestaje tek kad kopija istekne.
  Dok se to ne zna, ne može se korisniku reći kad je podatak stvarno nestao.
- **Radi li čišćenje na tvojoj bazi.** Migracija je pisana prema shemi iz
  repozitorija i nije pokrenuta ni na jednoj stvarnoj bazi. Prvi pokretač si ti,
  i zato korak 3 i korak 5 postoje.

---

## Kontrolna lista

| | Korak | Provjera da je gotovo |
|---|---|---|
| [ ] | Primijenjena `cloud/0008_retencija_download_log.sql` | `SELECT download_log_anonimiziraj(24);` vraća broj, ne grešku |
| [ ] | `pg_cron` uključen | redak u `cron.job` s `jobname = 'download_log_retencija'`, `active = true` |
| [ ] | Raspored se doista izvršava | redak sa `status = 'succeeded'` u `cron.job_run_details`, provjereno dan poslije |
| [ ] | Ili: pričuvna skripta postavljena | dnevnik zadnjeg pokretanja ima današnji datum |
| [ ] | Najstariji neočišćeni zapis mlađi od 24 mjeseca | upit `najstariji_zivi` iz koraka 5 |
| [ ] | Nijedan očišćeni redak nema osobne stupce | kontrolni upit iz koraka 5 vraća `0` |
| [ ] | Postupak brisanja računa poznat i zapisan | anonimizacija prije `DELETE FROM users` |
| [ ] | Politika privatnosti usklađena | oznaka `[NIJE AKTIVNO]` u članku 7.2 uklonjena tek kad su gornji redci potvrđeni |
