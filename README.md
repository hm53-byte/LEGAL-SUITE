# LEGAL-SUITE

Streamlit aplikacija koja iz web forme popuni unaprijed napisani predložak
hrvatskog pravnog podneska ili ugovora i vrati ga kao `.docx` datoteku.

Namijenjena je osobi koja već zna koji dokument treba i želi uredno formatiran
nacrt koji će sama provjeriti ili dati odvjetniku na pregled. Nastala je kao
vlastiti alat autora, studenta prava.

## Odricanje od odgovornosti

**Ovo nije pravni savjet.** Aplikacija ne tumači propise, ne analizira konkretnu
situaciju i ne procjenjuje izglede u postupku. Umeće unesene podatke u
predložak.

**Svaki generirani dokument mora prije upotrebe pregledati čovjek.** Predlošci su
pisani ručno prema propisima koji su vrijedili u vrijeme pisanja. Repozitorij
nema mehanizam koji prati izmjene propisa, pa tekst može biti zastario ili
neprikladan za konkretan slučaj.

**Aplikacija ne prati rokove.** Rok za žalbu, prigovor ili tužbu nije ugrađen,
ne prikazuje se i ne provjerava. Rokovi u hrvatskom postupovnom pravu su u
pravilu prekluzivni, a propušteni rok se ne može popraviti. Provjera roka je
isključivo na korisniku.

Za pravni savjet: imenik Hrvatske odvjetničke komore, https://www.hok-cba.hr

## Što radi

U `generatori/` je 82 funkcije s prefiksom `generiraj_`, raspoređene u 18
modula. Svaka prima `dict` s podacima iz forme i vraća HTML koji
`docx_export.py` pretvara u `.docx`. Sve su dosežne iz sučelja (provjereno
usporedbom definicija i poziva).

Raspodjela po modulima:

| Skupina | Moduli (broj funkcija) |
|---|---|
| Ugovori i izjave | `obvezno` 12, `ugovori` 10, `trgovacko` 7, `punomoci` 1, `opomene` 1 |
| Nekretnine i pokretnine | `zemljisne` 10, `apartmani` 4, `nautika` 4, `pokretnine` 2, `posrednik_najam` 2 |
| Sudski postupci | `ovrhe` 7, `obiteljsko` 5, `potrosaci` 4, `upravno` 4, `kazneno` 3, `stecajno` 3, `tuzbe` 2, `zalbe` 1 |

Jedna funkcija ne odgovara nužno jednom tipu dokumenta: dio funkcija ima
parametar vrste koji mijenja tekst, a dio srodnih podnesaka dijeli istu
funkciju. Zato je 82 broj funkcija, ne broj dokumenata.

Uz generatore, sučelje ima šest pomoćnih modula: pretragu Narodnih novina,
kalkulator zakonskih zateznih kamata, kalkulator sudskih pristojbi, kalendar
ročišta, poveznicu na e-Oglasnu ploču i stranicu s uvjetima korištenja.
Bočna navigacija sadrži 24 modula uz početnu stranicu.

### Formatiranje izlaznog dokumenta

Definirano u `docx_export.py`: Times New Roman (redak 19), 12 pt osnovni tekst
(redak 20), margine 2,5 cm sa sve četiri strane (redak 25, primjena 528-533),
obostrano poravnanje odlomaka (redak 46), datumi u obliku `dd.mm.yyyy.`

### Provjere unosa i ugrađeni podaci

- OIB se provjerava po ISO 7064 MOD 11,10 (`pomocne._validiraj_oib()`, redci
  47-63). Provjerava se kontrolna znamenka, ne postojanje osobe u registru.
- `sudovi.SUDOVI` sadrži 74 suda: 40 općinskih, 16 županijskih, 9 trgovačkih,
  5 upravnih, 3 visoka i Vrhovni sud.
- `klauzule.KLAUZULE` sadrži 17 ugovornih klauzula u 10 kategorija.
- `pristojbe.py` računa prema Zakonu o sudskim pristojbama (NN 118/18) i Uredbi
  o tarifi (NN 129/19). Iznosi su preračunati iz kuna i treba ih provjeriti
  prema važećoj tarifi prije uplate.

Aplikacija ne koristi generativni AI. Predlošci su Python f-stringovi, nema
poziva prema jezičnom modelu (vidi `generatori/tuzbe.py`).

## Što NE radi i koja su ograničenja

Namjerno izostavljeno:

- **Ne daje pravni savjet** i ne tumači propis za konkretnu situaciju.
- **Ne klasificira korisnikov problem.** Nema tijeka "opišite problem, mi ćemo
  vam reći koji dokument treba".
- **Ne prati rokove.** Odluka je obrazložena u kodu (`LEGAL-SUITE.py:468-473`).
- **Ne predviđa ishod postupka.**
- **Ne podnosi ništa sudu.** Nema integracije s e-Komunikacijom ni s bilo kojim
  sustavom za predaju podnesaka.

Ograničenja implementacije:

- **Deklinacija imena je približna.** `pomocne._padez_ime()` u vlastitom
  docstringu navodi da za nejasne slučajeve (nepostojano a, složenice) vraća
  nominativ. Lokativ grada (`pomocne.u_lokativu()`) radi preko rječnika s
  ograničenim popisom; nepoznat grad vraća se nepromijenjen.
- **Prijava korisnika nije trajna.** `auth.py` piše u lokalni `.users.json`
  (PBKDF2-SHA256). Na Streamlit Community Cloudu disk je efemeran, pa se
  korisnici gube pri restartu. Isto vrijedi za `_data/kalendar.json`.
- **Postoji ugrađena zadana admin lozinka.** `auth.py:247` prihvaća zadanu
  lozinku ako u secrets nije postavljen `admin_password_hash`. Taj secret mora
  biti postavljen prije bilo kakvog javnog deploya. Otvoren zadatak je ukloniti
  fallback iz koda.
- **Pretraga Narodnih novina je krhka.** `api_nn.py` parsira HTML regularnim
  izrazom i pri grešci pada na ugrađene demo rezultate (`_DEMO_REZULTATI`,
  redak 160), koji nisu živi podatak.
- **Sudski registar traži vlastite OAuth2 vjerodajnice** (`sudreg_client_id`,
  `sudreg_client_secret`). Bez njih modul vraća poruku da nije konfiguriran
  (`api_sudreg.py:59`).
- **e-Oglasna ploča nije integrirana.** `stranice/eoglasna.py` je poveznica na
  službeni portal. Raniji klijenti za e-Oglasnu i e-Predmet uklonjeni su iz
  koda (commit `6ca39ee`) jer su vraćali izmišljene podatke.
- **Naplata nije u pogonu.** `entitlements.py` i `cloud/` sadrže kod za Supabase
  i Polar.sh, ali bez postavljenih secrets sve je neaktivno
  (`entitlements._is_configured()`). Uvjeti korištenja i politika privatnosti u
  `stranice/pravila.py` su nacrti bez pravničkog pregleda.
- **Odricanje nije na prvom zaslonu.** Zadani mod je jednostavni
  (`LEGAL-SUITE.py:119`), a u njemu napomena stoji na dnu stranice, ispod
  kataloga (`stranice/jednostavno.py:1077`). Trebala bi stajati iznad kataloga,
  prije prvog klika. Otvoren zadatak.
- **Jednostavni mod prijavljuje korisnika kao gosta bez koraka potvrde**
  (`LEGAL-SUITE.py:122-124`).
- **Predlošci nisu pravnički recenzirani** ni sudski testirani.

## Pokretanje

Traži se Python 3.10 ili noviji. `runtime.txt` za deploy fiksira Python 3.12.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run LEGAL-SUITE.py
```

Aplikacija se otvara na `http://localhost:8501` i radi bez ikakve
konfiguracije. `.env` i Streamlit secrets potrebni su samo za neobavezne
module: Sudski registar, Supabase i Polar.

Ovisnosti u `requirements.txt`: `streamlit`, `python-docx`, `lxml`, `requests`.

### Testovi

`pytest` nije u `requirements.txt` i treba ga instalirati zasebno:

```bash
pip install pytest
python -m pytest tests/ -q
```

U `tests/` je 13 datoteka; `pytest tests` daje 382 prošla i 5 preskočenih.
Pokrivaju provjeru OIB-a, formatiranje iznosa, generatore, pretvorbu u DOCX,
kalkulator pristojbi, watermark, lanac revizije, retenciju zapisa o preuzimanjima
i obavijest o obradi po GDPR čl. 13.

Pet preskočenih su stranice bez ijednog polja za unos, pa se na njima obavijest o
obradi i ne očekuje.

Pokreće se `pytest tests`, ne `pytest` iz korijena: `scripts/load_test.py` uvozi
`playwright`, kojeg u okolini nema, pa prikupljanje testova iz korijena pukne
prije nego išta krene.

Česte greške pri pokretanju: [`docs/troubleshooting.md`](docs/troubleshooting.md).

## Struktura repozitorija

```
LEGAL-SUITE.py        Ulazna točka, navigacija, katalog pravnih područja
config.py             CSS i vizualni tokeni
auth.py               Prijava (lokalni .users.json, PBKDF2-SHA256)
pomocne.py            Provjera OIB-a, formatiranje, deklinacija, dijeljeni UI
docx_export.py        Pretvorba HTML u .docx (python-docx)
sudovi.py             Popis 74 suda s adresama
pristojbe.py          Kalkulator sudskih pristojbi
klauzule.py           Biblioteka od 17 ugovornih klauzula
watermark.py          Serijski broj po dokumentu
audit_chain.py        SHA256 lanac nad zapisima o preuzimanju
entitlements.py       Klijent za Supabase (neaktivan bez secrets)
api_nn.py             Pretraga Narodnih novina
api_sudreg.py         Sudski registar (traži OAuth2 vjerodajnice)
generatori/           18 modula, 82 funkcije koje vraćaju HTML
stranice/             Streamlit forme po pravnom području
tests/                pytest
cloud/                SQL shema i Cloudflare Worker za naplatu (nije u pogonu)
scripts/              Registar generatora, replay dokumenta, load test
docs/                 Dokumentacija
```

Tok podataka: `stranice/*.py` prikuplja unos i slaže `dict`, funkcija u
`generatori/` vraća HTML kao string (bez stanja i sporednih učinaka),
`docx_export.py` gradi dokument, korisnik ga preuzima.

## Zaštita podataka

Podaci iz forme obrađuju se u memoriji i vraćaju u `.docx`. U zadanoj
konfiguraciji ne spremaju se u bazu. Ako se uključi Supabase, u `download_log`
upisuju se serijski broj dokumenta, identifikator korisnika, vrijeme i razina
pretplate, ali ne i sadržaj dokumenta.

Svaki generirani `.docx` dobiva serijski broj u vidljivom podnožju i u polju
`dc:identifier` OOXML metapodataka (`watermark.py:100-114`). Korisnik ga može
ukloniti. Svrha je utvrđivanje podrijetla dokumenta, ne sprječavanje kopiranja.

## Pravna granica

Aplikacija je držana izvan dvije zone: neovlaštenog pružanja pravne pomoći po
Zakonu o odvjetništvu i pojačanih obveza koje Uredba EU 2024/1689 (AI Act)
predviđa za sustave koji se koriste u primjeni prava na konkretne slučajeve.
Način na koji se to postiže je da aplikacija ne zaključuje ništa o korisnikovoj
situaciji: ne bira dokument umjesto korisnika, ne tumači propis i ne daje
procjenu.

Ovo je autorova prosudba o tome gdje granica stoji, nije pravna analiza i nije
zamjena za pravno mišljenje. Aplikacija nije prošla pravnu reviziju.

Gdje odricanje stoji u sučelju: `LEGAL-SUITE.py:575-586` (početna stranica
naprednog moda), `stranice/jednostavno.py:1077` (dno stranice jednostavnog
moda), `stranice/pravila.py:38-48` (nacrti uvjeta, s oznakom da nisu pravnički
pregledani).

## Status

Osobni projekt u razvoju. Nije proizvod, nema podršku ni jamstvo dostupnosti i
ispravnosti. Autor ne odgovara za štetu nastalu korištenjem aplikacije ili
generiranih dokumenata, uključujući propuštene rokove, odbačene podneske i
troškove postupka.

## Licenca

Apache-2.0, vidi [`LICENSE`](LICENSE). Odnosi se na kod, predloške i tekstove
klauzula u ovom repozitoriju.

Do 15. 8. 2026. repozitorij je nosio vlasničku licenciju uz otvoren izvor, što
je bilo proturječno: kod je bio javan, a upotreba zabranjena. Razriješeno je u
korist otvorene licencije.

Ono što licencija ne mijenja stoji u odjeljku iznad: izlaz aplikacije nije
pravni savjet, a odgovornost za upotrebu dokumenta nosi onaj tko ga podnosi.
