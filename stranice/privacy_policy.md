# Politika privatnosti — LegalTechSuite Pro

**Verzija**: 1.0 (nacrt 2026-04-27)
**Status**: NACRT za pravnički pregled prije live mode aktivacije.

---

> **NAPOMENA**: Ovaj dokument je inicijalni nacrt. Mora biti pregledan od strane odvjetnika i prilagođen Davateljevim konkretnim okolnostima (poslovnim podacima, OIB-u, sjedištu, eventualnom službeniku za zaštitu osobnih podataka — DPO) prije aktivacije Stripe live mode-a.

---

## 1. Voditelj obrade (Davatelj)

| Podatak | Vrijednost |
|---|---|
| Naziv | [POPUNITI: ime/naziv tvrtke ili obrta, ili fizičke osobe] |
| OIB | [POPUNITI] |
| Adresa | [POPUNITI] |
| E-mail za GDPR pitanja | [POPUNITI: privacy@vasdomena.com ili sl.] |
| Telefon (opcijski) | [POPUNITI ili "Ne primjenjuje se"] |
| DPO (ako primjenjivo) | [POPUNITI ili "Ne imenuje se posebno DPO; voditelj je dosegnut na e-mailu iznad"] |

## 2. Koje osobne podatke prikupljamo

### 2.1 Podaci pri registraciji

- E-mail adresa
- Lozinka (pohranjena kao PBKDF2-SHA256 hash, NIKAD u plain text-u)
- Eventualni OAuth podaci (Google sub, Apple sub) ako Korisnik koristi vanjsku autentikaciju

### 2.2 Podaci pri korištenju Aplikacije

- Tip generiranog dokumenta (npr. "tuzba", "ovrha")
- Datum i vrijeme generiranja
- Serijski broj dokumenta (kriptografski sažetak — vidi članak 4)
- Tier u trenutku generiranja (free / pro)

**Ne pohranjujemo sadržaj generiranih dokumenata.** Sav sadržaj koji Korisnik unese (imena stranaka, OIB-i, opisi, iznosi) ostaje samo u memoriji servera tijekom generiranja i odmah se odbacuje. Generirani `.docx` se Korisniku vrati direktno; mi ne čuvamo kopiju.

### 2.3 Podaci pri pretplati (samo PRO korisnici)

- Stripe customer ID (interni identifikator kod Stripe-a)
- Stripe subscription ID
- Status pretplate (active / past_due / revoked)
- Datum istjeka aktualnog perioda

**Podatke o kartici NE prikupljamo niti pohranjujemo.** Plaćanje se odvija direktno između Korisnika i Stripe-a; mi dobijemo samo potvrdu da je pretplata aktivna.

### 2.4 Tehnički podaci

- IP adresa (privremeno tijekom sesije, ne pohranjujemo dugoročno)
- User-Agent (browser identifikator) — koristi se za debug i ne pohranjuje
- Cookies za session management (vidi članak 9)

## 3. Pravni temelji obrade (GDPR čl. 6)

| Podatak | Pravni temelj | Razlog |
|---|---|---|
| E-mail, lozinka | Ugovor (čl. 6(1)(b)) | Bez registracije ne možemo pružiti uslugu PRO pretplate |
| Tip dokumenta, datum, serial | Legitiman interes (čl. 6(1)(f)) | Forenzički audit trail za sprečavanje zlouporabe; statistika korištenja u agregiranom obliku |
| Stripe customer ID | Ugovor (čl. 6(1)(b)) | Bez ovog ID-a ne možemo verificirati plaćanje |
| IP adresa (sesija) | Legitiman interes (čl. 6(1)(f)) | Zaštita od napada (rate limiting, fraud detection) |
| Cookies (session) | Legitiman interes (esencijalni cookies, čl. 6(1)(f)) | Aplikacija bez session-a ne može raditi |

## 4. Serijski broj dokumenta i forenski audit trail

Svaki generirani `.docx` ima jedinstveni serijski broj (`NN-NNNN-NNNNNN` format). Serijski broj je:

```
SHA256(user_id + tip_dokumenta + timestamp + random_nonce)[:12]
```

To znači:

- Iz samog serijskog broja **NIJE moguće rekonstruirati** Korisnikove osobne podatke (kriptografski hash).
- Forenzički chain ide preko interne tablice `download_log` u kojoj je veza `serial_hash → user_id`.
- Pristup `download_log` tablici je strogo ograničen (samo Davatelj kao voditelj obrade).

Serijski broj je vidljiv u footer-u dokumenta (free tier) i u XML metapodacima dokumenta (svi tier-i). Korisnik može tehnički ukloniti footer u Word-u, ali XML metapodaci ostaju osim ako Korisnik ne otvori `.docx` kao zip i ne uredi `core.xml` ručno.

**Cilj**: ako se netko pojavi sa "vašim" dokumentom u sporu, Davatelj može potvrditi je li dokument autentičan (generirat iz Aplikacije) i kojem računu pripada. Korisnik koji to ne želi može u Word-u ukloniti footer i metapodatke prije dijeljenja dokumenta s drugima.

## 5. Tko ima pristup vašim podacima (treće strane)

| Treća strana | Što vidi | Gdje | Razlog |
|---|---|---|---|
| **Streamlit Inc.** (San Francisco, CA, SAD) | IP adresa, User-Agent, sesijski cookies | SAD (Standard Contractual Clauses za prijenos van EU) | Hosting Aplikacije |
| **Supabase Inc.** (San Francisco, CA, SAD) | Sve iz članka 2.1, 2.2, 2.3 osim sadržaja dokumenata | EU (Frankfurt, Njemačka) | Baza podataka (registracija, entitlements, audit) |
| **Cloudflare Inc.** (San Francisco, CA, SAD) | Stripe webhook eventi (sadrže Stripe customer ID, plan, status) | EU edge | Webhook handler |
| **Stripe Payments Europe Ltd.** (Dublin, Irska) | E-mail, podaci o kartici, podaci o transakciji | EU (Irska) | Procesiranje plaćanja |

Davatelj ima sklopljene Data Processing Agreements (DPA) sa svim navedenim trećim stranama u skladu s GDPR čl. 28.

## 6. Vaša prava (GDPR)

Sukladno GDPR-u i hrvatskom Zakonu o provedbi Opće uredbe o zaštiti podataka (NN 42/18), Korisnik ima sljedeća prava:

### 6.1 Pravo na pristup (čl. 15)

Korisnik može u svako doba zatražiti kopiju svih svojih osobnih podataka koje Davatelj obrađuje. Davatelj odgovara u roku od 30 dana.

### 6.2 Pravo na ispravak (čl. 16)

Korisnik može ispraviti netočne podatke (npr. e-mail) direktno u aplikaciji ili kontaktiranjem Davatelja.

### 6.3 Pravo na brisanje ("pravo da budem zaboravljen", čl. 17)

Korisnik može zatražiti brisanje računa i svih osobnih podataka. Iznimka: podaci koje Davatelj mora čuvati po zakonu (npr. fiskalni račun za pretplate — 11 godina prema HR Zakonu o računovodstvu).

### 6.4 Pravo na prenosivost (čl. 20)

Korisnik može zatražiti svoje podatke u strojno čitljivom formatu (JSON ili CSV).

### 6.5 Pravo na prigovor (čl. 21)

Korisnik može uložiti prigovor na obradu temeljenu na legitimnom interesu (npr. forensic audit trail). Davatelj će razmotriti i odgovoriti u roku od 30 dana; ako prigovor smatra opravdanim, prestat će obrada osim ako postoje uvjerljiviji legitimni razlozi.

### 6.6 Pravo na povlačenje suglasnosti

Ne primjenjuje se na obrade temeljene na ugovoru ili legitimnom interesu (vidi članak 3). Primjenjuje se na eventualne marketinške komunikacije za koje je dana zasebna suglasnost (vidi članak 8).

### 6.7 Pravo žalbe nadzornom tijelu

Korisnik se može žaliti **Agenciji za zaštitu osobnih podataka** (AZOP), Selska cesta 136, 10000 Zagreb, www.azop.hr, ako smatra da Davatelj ne poštuje GDPR.

## 7. Razdoblje čuvanja podataka

| Podatak | Razdoblje |
|---|---|
| Račun korisnika (e-mail, lozinka) | Dok god je račun aktivan + 30 dana nakon brisanja (grace period za reaktivaciju) |
| `download_log` (serial, doc_type, datum) | **24 mjeseca** od datuma generiranja, zatim auto-brisanje (cron job) |
| Fiskalni računi za PRO pretplate | **11 godina** (Zakon o računovodstvu, NN 78/15) |
| Stripe podaci | Prema Stripe Privacy Policy (https://stripe.com/privacy) |
| IP adrese, User-Agent | Samo tijekom sesije, ne pohranjuje se trajno |

## 8. Marketing i obavijesti

Davatelj **NE šalje** marketinške e-mailove bez izričite suglasnosti Korisnika. Pri registraciji ne traži se suglasnost za marketing — registracija je čisto operativna.

Eventualni budući marketing će biti zasebno odobren (opt-in checkbox); Korisnik može u svako doba povući suglasnost (opt-out link u svakoj poruci).

**Operativne obavijesti** (npr. "vaša pretplata istječe za 7 dana", "promijenili smo Uvjete korištenja") nisu marketing i ne traže zasebnu suglasnost — temelje se na ugovoru ili legitimnom interesu.

## 9. Cookies

Aplikacija koristi sljedeće cookies:

| Cookie | Tip | Razlog | Trajanje |
|---|---|---|---|
| Streamlit session cookies | Esencijalni | Bez ovih cookies Aplikacija ne može pamtiti Korisnikove izbore tijekom sesije | Sesija (do zatvaranja browser tab-a) |
| Supabase auth JWT | Esencijalni | Pamti login (da Korisnik ne mora upisivati lozinku pri svakoj posjeti) | 30 dana, refresh-a se pri svakom logiranju |
| Stripe Checkout cookies | Esencijalni (treća strana) | Stripe ih koristi pri checkout-u | Prema Stripe Privacy Policy |

**Ne koristimo** cookies za praćenje (Google Analytics, Facebook Pixel, ad networks) bez izričite suglasnosti. Trenutno (verzija 1.0) takvih cookies nema. Ako se uvedu u budućnosti, traži se suglasnost prije postavljanja.

## 10. Sigurnost

Davatelj primjenjuje tehničke i organizacijske mjere zaštite osobnih podataka:

- **Šifriranje u tranzitu**: HTTPS (TLS 1.2+) za sav promet između Korisnika i Aplikacije, te između Aplikacije i trećih strana.
- **Šifriranje pri pohrani**: Supabase Postgres koristi at-rest šifriranje (AES-256). Lozinke se hashиraju s PBKDF2-SHA256.
- **Pristup podacima**: samo Davatelj kao voditelj obrade ima pristup `download_log` tablici i Stripe dashboard-u. Pristup je zaštićen 2FA gdje je moguće.
- **Backup**: Supabase radi automatske backup-e (point-in-time recovery 7 dana na free tier-u).
- **Incident response**: u slučaju povrede osobnih podataka koja predstavlja rizik za Korisnike, Davatelj će obavijestiti AZOP u roku od 72 sata (GDPR čl. 33) i ugrožene Korisnike bez nepotrebne odgode (čl. 34).

## 11. Maloljetnici

Aplikacija nije namijenjena osobama mlađim od 18 godina. Davatelj ne prikuplja namjerno podatke maloljetnika. Ako roditelj/zakonski zastupnik utvrdi da je dijete mlađe od 18 godina registrirano, treba kontaktirati Davatelja koji će račun brisati bez naknade.

## 12. Promjene Politike privatnosti

Davatelj može mijenjati ovu Politiku uz **30-dnevnu obavijest** putem e-maila ili u-aplikacijske notifikacije. Korisnik koji nastavi koristiti Aplikaciju nakon stupanja na snagu izmjena pristaje na nove uvjete; ako se ne slaže, može zatražiti brisanje računa bez naknade.

## 13. Kontakt

Pitanja, primjedbe i GDPR zahtjevi šalju se na: **[POPUNITI e-mail]**

Davatelj će odgovoriti u roku od 30 dana (GDPR standard).

---

**Datum stupanja na snagu**: dan kad Korisnik prihvati ovu Politiku pri registraciji ili pri prvoj pretplati nakon ažuriranja.

**Posljednja izmjena**: 2026-04-27 (nacrt v1.0)
