# PLAN MONETIZACIJE — LegalTech Suite Pro

> Ovaj folder sadrži kompletan plan kako napraviti naplatu i pretplatu na tvojoj aplikaciji, **bez vlastitog servera**, uz najmanji mogući trošak.
>
> **Napisano za laika** — svaki tehnički pojam je objašnjen. Možeš čitati redom, korak po korak.
>
> **Datum izrade:** 23.04.2026.

---

## ŠTO ĆEŠ DOBITI NA KRAJU

Aplikaciju koja:

1. Ima **stvarnu prijavu korisnika** (email + lozinka, ili Google login)
2. Pamti korisnike **trajno** (ne briše se kao sad)
3. Daje **1 besplatni dokument** svakom novom korisniku
4. Nakon toga **traži pretplatu** (tjedna, mjesečna, godišnja)
5. **Naplaćuje karticom** preko legalno čistog kanala (s računima, EU PDV-om, sve uredno)
6. **Sama ažurira status pretplate** kad korisnik plati / otkaže

**Trošak za pokretanje:** 0 EUR (sve free tier servisi). Tek kad zaradiš preko određenog praga, počinju mjesečni troškovi.

---

## REDOSLIJED ČITANJA

| # | Datoteka | Što sadrži | Vrijeme čitanja |
|---|----------|------------|-----------------|
| 01 | `01_PRAVNI_OKVIR.md` | Obrt, PDV, GDPR — što moraš imati prije nego krene novac | 15 min |
| 02 | `02_ARHITEKTURA.md` | Pregled svih komada koji čine cijeli sustav | 10 min |
| 03 | `03_SUPABASE_SETUP.md` | Postavljanje baze i prijave (gdje se pamte korisnici) | 30 min praktično |
| 04 | `04_LEMON_SQUEEZY_SETUP.md` | Postavljanje naplate (gdje korisnik plaća) | 30 min praktično |
| 05 | `05_KOD_BILLING.md` | Novi modul `billing.py` s objašnjenjima | 20 min |
| 06 | `06_KOD_AUTH.md` | Prepravak `auth.py` modula | 20 min |
| 07 | `07_KOD_PAYWALL.md` | Integracija "zid plaćanja" u download | 15 min |
| 08 | `08_WEBHOOK.md` | "Most" između naplate i tvoje baze | 30 min praktično |
| 09 | `09_LANSIRANJE.md` | Checklist prije nego pustiš ljude unutra | 10 min |
| 10 | `10_NAKON_LANSIRANJA.md` | Što pratiti, kad skalirati, kad mijenjati cijene | 15 min |

**Ukupno aktivnog rada:** otprilike 8-12 sati ako sve ide po planu. Možeš to raspodijeliti na 3-4 vikenda.

---

## VAŽNI POJMOVI (kratki rječnik)

Prije nego kreneš, evo prevodilačkog rječnika za pojmove koji će se ponavljati:

- **Backend** = strana aplikacije koju korisnik ne vidi (baza, server). Ti **nemaš** vlastiti backend i to je u redu.
- **Frontend** = strana koju korisnik vidi. Tvoj Streamlit je frontend.
- **Baza podataka (database)** = gdje se trajno pamte korisnici, pretplate, transakcije. **Trenutačno koristiš JSON datoteku — to je krivo, briše se sama.**
- **Auth (autentikacija)** = sustav prijave: tko si ti, dokaži.
- **Webhook** = automatska poruka koju jedan servis pošalje drugome ("Korisnik je upravo platio, ažuriraj status"). Glavni tehnički koncept koji moraš shvatiti.
- **API** = način na koji programi razgovaraju jedan s drugim.
- **MoR (Merchant of Record)** = "trgovac upisan u registar". Servis koji pravno postaje prodavač krajnjem korisniku umjesto tebe — riješava poreze i račune. **Ovo ti štedi godinu dana glavobolje.**
- **Free tier** = besplatna razina servisa, dovoljna dok si mali.
- **Subscription / Pretplata** = ponavljajuće naplaćivanje (svaki tjedan ili mjesec automatski).
- **Paywall** = "zid plaćanja". Ekran koji se pojavi kad korisnik želi nešto što je iza pretplate.

---

## TRI SERVISA KOJE ĆEŠ KORISTITI

1. **Supabase** (supabase.com) — baza podataka i prijava korisnika
   - Što je to: gotov backend s Postgres bazom + sustavom za login
   - Cijena: **besplatno** dok ne dobiješ 50.000 mjesečnih korisnika
   - Zašto: jer nemaš vlastiti server, a Supabase ti ga zamjenjuje

2. **Lemon Squeezy** (lemonsqueezy.com) — naplata
   - Što je to: Stripe-ov konkurent, ali s automatskim PDV-om za EU
   - Cijena: **5% + 0,50 EUR po transakciji** (skuplji od Stripea, ali rješava PDV mjesto tebe)
   - Zašto: jer kao solo programer ne želiš kvartalno popunjavati PDV prijave za 27 EU zemalja

3. **Streamlit Community Cloud** (streamlit.io/cloud) — već koristiš
   - Cijena: **besplatno**
   - Ostaje gdje jest, samo dodajemo gornje gore

---

## ŠTO AKO ZAPNEŠ

Svaka datoteka ima na kraju sekciju "**Tipični problemi**" gdje su nabrojane greške koje će ti se vjerojatno dogoditi i kako ih riješiti.

Ako nešto baš ne valja, pošalji mi:
1. Točan korak na kojem si zapeo
2. Točnu poruku greške (copy-paste)
3. Što si pokušao prije nego što si pitao

Onda ti mogu odgovoriti precizno.

---

## SLJEDEĆI KORAK

Otvori `01_PRAVNI_OKVIR.md` i pročitaj. **Ne preskačeš taj dio** — bez urednog pravnog statusa ne smiješ ni primiti prvi euro, a Lemon Squeezy ti neće isplatiti zaradu ako nemaš IBAN i status poreznog obveznika.
