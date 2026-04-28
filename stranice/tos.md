# Uvjeti korištenja — LegalTechSuite Pro

**Verzija**: 1.0 (nacrt 2026-04-27)
**Status**: NACRT za pravnički pregled prije live mode aktivacije.

---

> **NAPOMENA**: Ovaj dokument je inicijalni nacrt sastavljen kao tehnički predložak. Mora biti **pregledan od strane odvjetnika** prije aktivacije Stripe live mode-a i prihvata stvarnih plaćanja. Posebno provjeriti: HR specifičnosti potrošačkog ugovora (ZZP, NN 41/14), pravo na otkazivanje pretplate (14-dnevno pravo na jednostrani raskid), porezne obaveze, jurisdikcijske klauzule.

---

## 1. Definicije

- **Aplikacija**: web servis "LegalTechSuite Pro" dostupan na `https://{{STREAMLIT_APP_ID}}.streamlit.app` i eventualnim budućim domenama.
- **Davatelj**: vlasnik i razvijatelj Aplikacije (kontakt naveden u Privacy Policy).
- **Korisnik**: bilo koja fizička ili pravna osoba koja koristi Aplikaciju, registrirana ili neregistrirana.
- **Dokument**: `.docx` datoteka generirana iz Aplikacije nakon što Korisnik popuni formu.
- **PRO pretplata**: plaćeni tier koji eliminira ograničenja iz besplatnog tier-a (vidi članak 5).

## 2. Što Aplikacija je, a što NIJE

### 2.1 Što Aplikacija je

Aplikacija je **alat za determinističko popunjavanje obrazaca**. Korisnik unosi podatke u formu, Aplikacija ih ubacuje u prethodno pripremljen Word predložak (template) i vraća `.docx` datoteku.

Aplikacija je tehnički ekvivalent Word makro funkciji, samo dostupna preko web sučelja.

### 2.2 Što Aplikacija NIJE

Aplikacija **NE pruža pravne savjete**. Konkretno, Aplikacija:

- **NE klasificira** Korisnikov problem niti predlaže koji pravni postupak treba pokrenuti.
- **NE preporučuje** strategiju vođenja postupka.
- **NE predviđa** ishod sudskog postupka.
- **NE analizira** činjenice Korisnikova slučaja.
- **NE zamjenjuje konzultaciju s odvjetnikom.**

Aplikacija ne sadrži generativni AI sloj koji bi automatski generirao klauzule ili tekstove dokumenata. Svi predlošci su ručno napisani.

### 2.3 Odgovornost Korisnika

**Korisnik je u potpunosti odgovoran za sadržaj** dokumenata generiranih kroz Aplikaciju. Korisnik:

- Sam unosi sve podatke (imena, identifikatore, iznose, opise);
- Sam odlučuje koji predložak koristi;
- Sam provjerava točnost podataka prije podnošenja dokumenta sudu, drugoj strani ili tijelu javne vlasti;
- Sam snosi posljedice grešaka u sadržaju.

**Davatelj NE jamči** da je dokument generiran iz Aplikacije pravno ispravan, pravovremen, ili prihvatljiv pred sudom u Korisnikovom konkretnom slučaju. Korisnik se savjetuje s odvjetnikom (Hrvatska odvjetnička komora — Imenik na https://www.hok-cba.hr) ako nije siguran.

## 3. Registracija i račun

### 3.1 Registracija

Registracija je besplatna i zahtijeva e-mail adresu i lozinku. Korisnik može koristiti Aplikaciju i bez registracije (gost), uz ograničenja iz članka 5.

### 3.2 Točnost podataka

Korisnik se obvezuje dati točne i ažurne podatke pri registraciji. Davatelj može zatvoriti račun u slučaju namjerno netočnih ili obmanjujućih podataka.

### 3.3 Sigurnost računa

Korisnik je odgovoran za čuvanje pristupnih podataka. Davatelj koristi PBKDF2-SHA256 za pohranu lozinki (lozinka se NIKAD ne pohranjuje u plain text-u).

### 3.4 Brisanje računa

Korisnik može u svako doba zatražiti brisanje računa slanjem e-maila na kontakt adresu navedenu u Privacy Policy. Brisanje je nepovratno i obuhvaća sve podatke o Korisniku osim onih koje Davatelj mora čuvati po zakonu (npr. fiskalni račun za platilane pretplate, vidi Privacy Policy).

## 4. Watermark i serijski broj dokumenta

### 4.1 Vidljivi watermark (free tier)

Dokumenti generirani u besplatnom tier-u sadrže u footer-u tekst:

> *Generirano iz LegalTechSuite Pro — ID: NN-NNNN-NNNNNN*

ID je jedinstveni serijski broj koji povezuje dokument s Korisnikom u internoj bazi (`download_log`).

### 4.2 Cleaner watermark (PRO tier)

PRO korisnici dobivaju samo serijski broj bez "Generirano iz" referenca:

> *ID: NN-NNNN-NNNNNN*

### 4.3 Nevidljivi metapodaci

Dokumenti svih tier-a sadrže serijski broj u `dc:identifier` polju Office Open XML metapodataka. To je standardno polje OOXML-a (ISO/IEC 29500). Forenski alati ga vide; common korisnik ne.

### 4.4 Privatnost

Serijski broj je **kriptografski sažetak** podataka (`SHA256` od user_id + tip dokumenta + vremenska oznaka + slučajni nonce). Iz serijskog broja **NIJE moguće** izvući Korisnikove osobne podatke bez pristupa Davateljovoj bazi. Vidi Privacy Policy za detalje.

### 4.5 Zašto serijski broj postoji

Serijski broj služi kao **forenzički audit trail** — ako se neki dokument pojavi u sporu i Korisnik tvrdi da nije njegov, Davatelj može povezati serijski broj s konkretnim računom i datumom generiranja. To je interes Davatelja (sprečava zlouporabu) i Korisnika (dokaz autentičnosti).

## 5. Pretplate i plaćanje

### 5.1 Tieri

| Tier | Cijena | Što uključuje |
|---|---|---|
| Besplatan | 0 EUR | Pristup svih 60+ predloška, vidljivi watermark u footer-u dokumenta, dnevni limit dokumenata (TBD) |
| PRO | 9,99 EUR/mj (cijena privremena, podložna izmjenama prije live mode aktivacije) | Neograničeni dokumenti, cleaner footer (samo serial), prioritetna podrška |

### 5.2 Plaćanje

Plaćanje se obavlja kroz **Stripe** (Stripe Inc., Irska podružnica). Davatelj **ne pohranjuje** podatke o kartici Korisnika; Stripe je registrirana institucija s PCI-DSS Level 1 certifikatom.

### 5.3 PDV

PDV (25 % HR stopa) se automatski izračunava i prikazuje pri checkout-u kroz Stripe Tax. Korisnik vidi konačnu cijenu prije potvrde plaćanja.

### 5.4 Pravo na jednostrani raskid (potrošački ugovor)

Korisnik koji je potrošač u smislu Zakona o zaštiti potrošača (NN 41/14) ima pravo na jednostrani raskid pretplate u roku od 14 dana od sklapanja ugovora **bez obrazlaganja**. Pravo se ostvaruje slanjem e-maila na kontakt adresu Davatelja.

**Iznimka**: ako je Korisnik tijekom tih 14 dana već generirao i preuzeo dokumente, smatra se da je dao izričitu suglasnost za izvršenje usluge prije isteka roka za odustanak (čl. 79. ZZP). U tom slučaju Korisnik gubi pravo na povrat novca za već iskorištene usluge, ali može otkazati buduće obnavljanje pretplate.

### 5.5 Otkazivanje obnove pretplate

Korisnik može otkazati obnovu pretplate u svako doba. Otkazom prestaje buduće obnavljanje, ali aktivni mjesec se zaračunava do kraja.

### 5.6 Refundi

Refundi se odobravaju u skladu sa zakonom (čl. 5.4 i prema Stripe-ovim pravilima). Refund obrađuje Stripe; vrijeme obrade može trajati do 10 radnih dana. Po refundu se PRO entitlement **odmah** ukida i Korisnik se vraća na besplatan tier.

### 5.7 Sporovi i charge-back

Ako Korisnik podnese charge-back kroz banku, Davatelj zadržava pravo zatvoriti račun. Davatelj će u tom slučaju kontaktirati Korisnika prije zatvaranja kako bi se nesporazum riješio izvansudski.

## 6. Dopušteno i nedopušteno korištenje

### 6.1 Dopušteno

- Generiranje dokumenata za vlastite potrebe Korisnika (fizičkih osoba) ili vlastite poslovne potrebe (pravnih osoba).
- Generiranje dokumenata u ime klijenta uz uvjet da Korisnik ima ovlaštenje (npr. odvjetnik za svoje klijente).

### 6.2 Nedopušteno

- **Nadripisarstvo**: Korisnik koji nije odvjetnik ne smije generirati dokumente u ime treće strane uz naplatu (Zakon o odvjetništvu, čl. 72 — kazneno djelo).
- **Reverse engineering** Aplikacije s namjerom kopiranja predložaka u konkurentski proizvod.
- **Automatizirano scrapanje** generiranih dokumenata iz Aplikacije van granica fer korištenja (rate limit će biti uveden).
- **Korištenje Aplikacije za generiranje dokumenata u svrhu prijevare**, lažnog predstavljanja, ili drugih protupravnih radnji.

Davatelj zadržava pravo zatvoriti račun u slučaju nedopuštenog korištenja, bez obaveze povrata novca za neiskorišten dio pretplate ako je dokazano protupravno postupanje.

## 7. Intelektualno vlasništvo

### 7.1 Predlošci

Predlošci dokumenata su autorsko djelo Davatelja. Korisnik dobiva **licencu za korištenje generiranih dokumenata** za vlastite potrebe (uključujući podnošenje sudu, drugoj strani, javnoj vlasti). Korisnik **NE dobiva pravo** redistribuirati predloške ili koristiti ih za izradu konkurentske aplikacije.

### 7.2 Generirani dokumenti

Vlasništvo nad generiranim dokumentima (sadržaj koji Korisnik unese) ostaje Korisniku. Davatelj **ne polaže pravo** na sadržaj koji Korisnik unese.

## 8. Ograničenje odgovornosti

### 8.1 Ograničenje

U najvećoj mjeri dopuštenoj važećim hrvatskim pravom, Davatelj NIJE odgovoran za:

- Posredne, posljedične ili neslučajne štete (lost profit, lost time, reputacijska šteta);
- Štete proizašle iz pogrešnog sadržaja koji je Korisnik unio;
- Štete proizašle iz odluka koje je Korisnik donio na temelju informacija u Aplikaciji;
- Privremene nedostupnosti Aplikacije (planiranog ili neplaniranog downtime-a, prirodnih nepogoda, kvarova trećih strana — Streamlit Cloud, Supabase, Cloudflare, Stripe).

### 8.2 Maksimalna odgovornost

Maksimalna ukupna odgovornost Davatelja prema bilo kojem Korisniku ograničena je na **iznos plaćen za pretplatu u zadnjih 12 mjeseci** prije nastanka štete, ali u svakom slučaju ne više od **100 EUR**.

### 8.3 Suprotnost zakonu

Ništa u ovim Uvjetima ne ograničava odgovornost Davatelja u slučajevima kad zakon to izričito zabranjuje (npr. namjerna prevara, gruba nepažnja).

## 9. Promjene Uvjeta

Davatelj može mijenjati Uvjete uz **30-dnevnu obavijest** putem e-maila ili u-aplikacijskog notifikacije. Korisnik koji nastavi koristiti Aplikaciju nakon stupanja na snagu izmjena pristaje na nove uvjete. Korisnik koji se ne slaže može otkazati pretplatu i zatražiti brisanje računa bez naknade.

## 10. Mjerodavno pravo i nadležnost

Ovi Uvjeti tumače se po pravu Republike Hrvatske. Za sporove je **stvarno nadležan sud u Zagrebu**, osim ako Korisnik (kao potrošač) ne odluči pokrenuti spor pred mjesno nadležnim sudom svog prebivališta (kako mu jamči Zakon o zaštiti potrošača).

## 11. Kontakt

Sva pitanja, primjedbe i zahtjevi (uključujući brisanje računa, otkazivanje pretplate, GDPR pravna prava) šalju se na e-mail naveden u Privacy Policy.

---

**Datum stupanja na snagu**: dan kad Korisnik prihvati ove Uvjete pri registraciji ili pri prvoj pretplati nakon ažuriranja.

**Posljednja izmjena**: 2026-04-27 (nacrt v1.0)
