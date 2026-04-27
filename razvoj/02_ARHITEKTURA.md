# 02 — ARHITEKTURA (KAKO SVE TEHNIČKI FUNKCIONIRA ZAJEDNO)

> Prije nego dotakneš ijedan redak koda, moraš **razumjeti cjelinu**. Inače ćeš se izgubiti u detaljima.
>
> Ova datoteka opisuje sve dijelove sustava, kao dijelove automobila — što je motor, što su kočnice, što spremnik, kako zajedno voze.

---

## 1. PROBLEM KOJI RJEŠAVAMO

Tvoja aplikacija sad radi ovako:

```
┌─────────────────────────┐
│  Korisnik otvori URL    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Streamlit Cloud učita app  │
│  Svi su gosti, svi mogu sve │
│  .users.json datoteka       │
│  (BRIŠE SE kod restart-a!)  │
└─────────────────────────────┘
```

**Problemi:**
1. Nema pravog pamćenja korisnika (JSON se briše)
2. Nema naplate
3. Nema načina razlikovanja besplatnog od plaćenog korisnika

---

## 2. CILJANO STANJE

Nakon ove implementacije aplikacija radi ovako:

```
┌─────────────────────────┐
│   KORISNIK              │
│   (web preglednik)      │
└─────┬───────────────────┘
      │
      │ (1) Otvori URL, registracija/prijava
      ▼
┌────────────────────────────────────┐
│   STREAMLIT CLOUD                  │
│   (tvoja aplikacija — već imaš)    │
│                                    │
│   Pita Supabase: "Tko je ovaj user?" ──┐
│   Pita Supabase: "Ima li pretplatu?" ──┤
│                                        │
└────────────────────────────────────────┘
                                         │
                                         ▼
┌────────────────────────────────────────────────┐
│   SUPABASE (baza + auth — nova stvar)          │
│                                                │
│   auth.users    ← lista svih registriranih     │
│   profiles      ← imena, brojač besplatnih     │
│   subscriptions ← aktivne pretplate            │
│   usage_log     ← tko je kada što generirao   │
│                                                │
└────────────────────────────────────────────────┘
                     ▲
                     │ (3) "User X je upravo platio!"
                     │
┌────────────────────┴────────────────────┐
│   SUPABASE EDGE FUNCTION                │
│   (mini-servis koji prima poruke od LS) │
└────────────────────▲────────────────────┘
                     │
                     │ (2) Webhook poruka
                     │
┌────────────────────┴────────────────────┐
│   LEMON SQUEEZY                         │
│   (naplata — nova stvar)                │
│                                         │
│   Checkout stranice                     │
│   Kartice, SEPA, PayPal                 │
│   Automatski PDV                        │
│   Mjesečne isplate tebi                 │
└─────────────────────────────────────────┘
```

---

## 3. TOK DOGAĐAJA — PRIMJER "NOVI KORISNIK"

Neka **Ana** po prvi put otvori tvoju aplikaciju:

**Korak 1: Dolazak**
- Ana upiše tvoj URL u preglednik
- Streamlit Cloud učita aplikaciju
- Aplikacija vidi: "Nema session, nije ulogirana" → prikaže login ekran

**Korak 2: Registracija**
- Ana upiše email + lozinku
- Streamlit pošalje taj email + lozinku Supabaseu
- Supabase: "OK, registriran je korisnik." Sprema u `auth.users`.
- Automatski se pokrene **trigger** koji kreira redak u `profiles` tablici s `free_documents_used = 0`
- Streamlit dobije "access token" — dokaz da je Ana prijavljena

**Korak 3: Generiranje prvog (besplatnog) dokumenta**
- Ana odabere "Generiraj tužbu", popuni formu, klikne "Generiraj"
- Streamlit napravi DOCX u memoriji
- Prije prikaza download gumba, **pita Supabase**: "Ana ima li pretplatu ili koliko je iskoristila besplatnih?"
- Supabase: "Pretplate nema, iskorištenih 0, limit je 1, smije."
- Streamlit prikaže download gumb + dokument
- Istovremeno zabilježi u `usage_log`: "Ana, tip=tužba, was_paid=false, datum=..."
- I poveća `profiles.free_documents_used` s 0 na 1

**Korak 4: Pokušaj drugog dokumenta**
- Ana ponovno generira nešto
- Streamlit pita Supabase — "iskorišteno 1, limit 1 → NE SMIJE"
- Umjesto download gumba, prikazuje **paywall**: tri gumba za pretplatu

**Korak 5: Ana klikne "Mjesečno 19,99 EUR"**
- Streamlit preusmjeri Anu na Lemon Squeezy checkout URL
- **Bitno:** u URL se "uvuče" Anin `user_id` kao `custom_data`. Ovo je ključ — bez toga Lemon Squeezy ne zna kome treba pripisati pretplatu.
- Ana popuni podatke kartice, plati

**Korak 6: Webhook (najsloženiji dio — pozorno čitaj)**
- Lemon Squeezy primi plaćanje
- **Lemon Squeezy pošalje automatsku poruku** ("webhook") na URL tvoje Supabase Edge Function
- Poruka sadrži: "subscription_created, user_id=<Anin id>, amount=19.99, renews_at=..."
- Edge Function najprije **provjeri potpis** (HMAC signature) da ne bi netko lažirao da je Ana platila
- Ako je validno → upiše u `subscriptions` tablicu: `user_id=Ana, status=active, renews_at=...`

**Korak 7: Ana se vraća na aplikaciju**
- Lemon Squeezy redirektira Anu natrag na tvoj URL
- Streamlit ponovo pita Supabase: "Ima li pretplatu?"
- Supabase: "Da, status=active do X datuma."
- Streamlit dopusti download

**Korak 8: Mjesec dana kasnije**
- Lemon Squeezy automatski naplati Aninu karticu
- Pošalje webhook: "subscription_payment_success"
- Edge Function ažurira `renews_at` u bazi
- Ana nikad ništa ne primijeti — sve radi automatski

**Korak 9: Ana otkaže**
- Ana klikne "Otkaži pretplatu" (bilo u tvojoj app ili direktno u LS emailu)
- Lemon Squeezy primi otkaz
- Pošalje webhook: "subscription_cancelled" + datum do kad je plaćeno
- Edge Function ažurira `status=cancelled`, `ends_at=...`
- Ana i dalje može koristiti do kraja plaćenog razdoblja
- Kad prođe `ends_at` → Streamlit pita Supabase, vidi da je prošlo → paywall

---

## 4. ZAŠTO WEBHOOK?

**Webhook = "automatska poruka koju servis pošalje tebi kad se nešto dogodi."**

Alternativa bi bila: Streamlit **svakih 5 minuta pita** Lemon Squeezy "Je li netko nešto platio?" Ali:
- Kašnjenje (korisnik plati → 5 min čeka)
- Trošak API poziva
- Nepouzdano (ako Streamlit spava, propusti)

Webhook je **push umjesto pull** — LS sam javi kad se dogodi.

---

## 5. ZAŠTO MORA EDGE FUNCTION UMJESTO DIREKTNO U STREAMLIT?

Dobro pitanje. Zato što:

1. **Streamlit nema "endpoint" koji prima POST zahtjev.** Streamlit je dizajniran kao interaktivna aplikacija s korisnikom pred ekranom — ne može sjediti i čekati da ga netko pozove.
2. **Streamlit Cloud spava** nakon 7 dana bez prometa. Ako LS pošalje webhook u tom trenutku — propustiš.
3. **Webhook mora biti brz** (< 10 sekundi) — Streamlit zna biti spor na cold start-u.

Supabase **Edge Function** je mali TypeScript kod koji:
- Živi u Supabase-ovom cloud-u
- Uvijek je spreman
- Kad dobije poruku od LS, provjeri potpis, upiše u bazu, odgovori "OK"
- Besplatno do 500.000 poziva mjesečno (što je ogromno)

**Ti napišeš ~30 linija TypeScript koda jednom i zaboraviš.**

---

## 6. KAKO APLIKACIJA PROVJERAVA PRETPLATU

Ovo je **tehnički najvažniji koncept** — kako app zna da li je user plaćen:

Svaki put kad Ana klikne "Preuzmi dokument", Streamlit napravi nešto poput:

```
1. Dohvati Anin user_id iz session-a
2. Upit u bazu: "SELECT status, ends_at FROM subscriptions WHERE user_id = Ana AND status = 'active'"
3. Ako postoji red s ends_at > sada → SMIJE
4. Inače → provjeri profiles.free_documents_used
5. Ako < 1 → SMIJE (besplatni trial)
6. Inače → paywall
```

Ovo je **super brzo** (~50ms) i **uvijek točno** jer baza je "jedini izvor istine".

---

## 7. "SUBSCRIPTION STATUS" — ŠTO SVE POSTOJI

Lemon Squeezy šalje više vrsta statusa:

| Status | Što znači | Smije li downloadati? |
|--------|-----------|----------------------|
| `active` | Aktivna, naplaćena | DA |
| `on_trial` | Probni period | DA |
| `paused` | Korisnik pauzirao | NE |
| `past_due` | Kartica odbijena, pokušavamo opet | DA (3 dana grace period) |
| `cancelled` | Otkazana ali još traje | DA dok `ends_at > now` |
| `expired` | Istekla, ne obnavlja se | NE |
| `unpaid` | Kartica odbijena definitivno | NE |

Kod u `billing.py` ima logiku za sve ovo.

---

## 8. BESPLATNI TRIAL — KAKO SE RAČUNA

Ne koristiš se kolačićima ni IP-om (pouzdano zaobiđeno). Koristiš **email = identitet**:

- Svaki korisnik ima `profiles.free_documents_used` (broj)
- Limit je `1` (ili koliko želiš)
- Kad netko generira dokument bez aktivne pretplate → brojač +1
- Kad brojač dosegne limit → paywall zauvijek (za tog emaila)

**Može li netko zaobići?** Da, s više mail adresa. Ali:
- Košta im vremena (novi email za svaki dokument)
- Kad vidiš da neko od jedne IP adrese stvara puno mailova → banovanje IP-a
- Dovoljno da 80%+ ljudi plati

**Alternativa — platiti i za besplatni** (nula besplatno, samo demo dokumenti koji imaju watermark "DEMO"). Ovo je agresivnije ali konverzija je bolja. Razmisli za kasnije.

---

## 9. ŠTO SE DOGAĐA AKO STREAMLIT "SPAVA" ILI SE SRUŠI

Scenarij: Ana platila, LS poslao webhook Edge Functionu, u bazu je upisano `status=active`. **Streamlit u tom trenutku spavao.**

Kad Streamlit "probudi" (Ana opet uđe) — pita bazu, vidi `status=active`, sve radi.

**Dakle:** webhook i Streamlit su potpuno neovisni. To je snaga ove arhitekture.

---

## 10. TROŠKOVI — KAD POČINJEŠ PLAĆATI

Free tier limiti (2026., provjeri aktualne):

| Servis | Free limit | Kad prijeđeš |
|--------|-----------|--------------|
| Supabase | 50.000 MAU, 500 MB baze, 500k Edge calls/mj | 25 USD/mj za Pro |
| Lemon Squeezy | Nema limit | 5% + 0,50 EUR po transakciji (uvijek) |
| Streamlit Cloud | 1 GB RAM po app-u | 20 USD/mj (Community → Team) |

Realistično: za prvih **500 aktivnih korisnika mjesečno** si u 0 EUR infrastrukture. Plaćaš samo LS fee iz naplate (što je u % od prihoda).

---

## 11. ŠTO MOŽEŠ UPRAVLJATI BEZ KODA

Supabase ima web UI gdje možeš:
- Vidjeti sve korisnike
- Ručno uključiti / isključiti nečiju pretplatu (za troubleshooting)
- Brisati korisnike (GDPR zahtjevi)
- Raditi SQL query-je za analitiku

Lemon Squeezy ima web UI gdje možeš:
- Vidjeti sve transakcije
- Izdati refund
- Promijeniti cijene
- Kreirati coupone

**Ovo znači da 95% operativnog rada radiš kroz web sučelja, ne kroz kod.**

---

## 12. VIZUALNI PREGLED FAJLOVA KOJE ĆEŠ IMATI NA KRAJU

```
APLIKACIJA/
│
├── LEGAL-SUITE.py              ← postojeći, minimalna izmjena
├── auth.py                     ← PREPRAVLJEN (Supabase umjesto JSON)
├── billing.py                  ← NOVI modul (provjera pretplate)
├── pomocne.py                  ← modificirana prikazi_dokument()
├── config.py                   ← isti
├── requirements.txt            ← dodan "supabase" paket
├── .streamlit/
│   └── secrets.toml            ← API ključevi (ne commitati na git!)
│
├── generatori/                 ← isto, ne diramo
├── stranice/                   ← gotovo isto, dodamo doc_type parametar
│
├── razvoj/                     ← ovi dokumenti, plan
│
└── supabase/                   ← NOVI folder
    └── functions/
        └── lemonsqueezy-webhook/
            └── index.ts         ← Edge Function (30 linija)
```

---

## 13. ŠTO OVO NIJE

- **Nije "enterprise grade"** — za 10.000+ korisnika ćeš trebati bolje.
- **Nije "zero-maintenance"** — morat ćeš ponekad ručno riješiti edge case-ove (kartica odbijena, korisnik tvrdi da je platio a nije...).
- **Nije "fail-proof"** — ako Supabase padne, tvoja app ne radi. Ali Supabase ima 99.9% uptime, što je OK.
- **Nije "pretjerano složeno"** — za ono što dobivaš, ovo je minimum.

---

## SLJEDEĆI KORAK

Sad kad razumiješ kako sve sjedi zajedno — kreni na `03_SUPABASE_SETUP.md`.

**NEMOJ** preskočiti na kod prije nego što razumiješ što radiš. Inače ćeš bugove debugirati bez ideje gdje su.
