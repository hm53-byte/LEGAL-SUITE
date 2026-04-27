# 02 — Pravna struktura: paušalni obrt vs j.d.o.o. vs d.o.o.

> **Datum**: 2026-04-27
> **Preporuka**: **j.d.o.o.** (jednostavno društvo s ograničenom odgovornošću)
> **Trošak osnivanja**: ~150-300 € (uključujući temeljni kapital 1.250 € koji se vraća kad se konvertira u d.o.o. kasnije)

---

## SAŽETAK ODLUKE

| Forma | Trošak osnivanja | Temeljni kapital | Porezna stopa | GDPR voditelj | **Verdict** |
|---|---|---|---|---|---|
| **Paušalni obrt** | ~50 € | 0 € | 12% na 15% gornje granice razreda | Ti osobno | **NE** — SaaS je sporan kao "slobodno zanimanje", limit 60k€/god, B2B usluge problematične |
| **j.d.o.o.** | ~150-300 € + 1.250 € TK | 1.250 € (uplaćuje se odmah) | 10% (do 1M€) ili 18% | Pravna osoba | **DA — preporuka** |
| **d.o.o.** | ~150-300 € + 2.500 € TK | 2.500 € (625 € odmah, ostatak u god) | 10% (do 1M€) ili 18% | Pravna osoba | Kasnije, kad prihod > 60k€/god |

---

## 1. Zašto NE paušalni obrt

### 1.1 Limit prihoda
- **60.000 EUR/god** ukupni prihodi → preko toga obvezno PDV i prelazak na "obrt s vođenjem poslovnih knjiga" ili pretvorba u d.o.o.
- Realan plafon za LegalTech Suite Pro: 100 PRO usera × 9 €/mj × 12 mj = **10.800 €/god** (bez B2B), 50-100 B2B usera × 50 €/mj × 12 = **30-60k €/god** (s B2B)
- **Kritičan pitanje**: ako uđeš u NPL/banke segment, prihod brzo prelazi 60k → moraš migrirati u d.o.o. → migracija je **pravno-administrativni teret** (prijenos imovine, brand, ugovori s klijentima)

### 1.2 "Slobodno zanimanje" isključenje
HOK pravilnik isključuje **slobodna zanimanja** iz paušalnog režima:
> "samostalna djelatnost zdravstvenih djelatnika, veterinara, odvjetnika, javnih bilježnika, revizora, **inženjera, arhitekata**, poreznih savjetnika i druge slične djelatnosti"

**Pitanje**: je li razvoj softvera "inženjering" / "slobodno zanimanje"?
- HZZ i Porezna uprava povijesno su tolerirale **NKD 62.01 (računalno programiranje)** kao paušal
- ALI: legalan SaaS koji **automatizira pravne radnje** (generira tužbe, ovrhe) je interpretacijski blizu **odvjetničkim uslugama** → AZOP / HOK / OO bi mogli osporiti
- Tvoja memory record `feedback_nadripisarstvo` već identificira da je generiranje pravnih dokumenata za druge uz naplatu = ZO čl. 72 ilegalno

**Zaključak**: paušalni obrt je **dvostruki rizik** — porezni (NKD 62.01 vs 69.10) + odvjetnički (nadripisarstvo). Najbolji je izlaz **d.o.o./j.d.o.o.** jer:
- Pravna osoba je voditelj obrade (GDPR štit)
- Pravna osoba je porezni obveznik (porezni štit)
- Pravna osoba je odvjetničko-disciplinski **subjekt nadležnosti AZOP-a, ne HOK-a**

### 1.3 Fiskalizacija 2.0 (od 2026)
- Od **2026-01-01** svi PDV obveznici obvezni zaprimati **eRačune**
- Od **2027** očekuje se proširenje obveze izdavanja eRačuna na sve (uključujući paušaliste)
- **B2B SaaS billing** (NPL agencije, banke kao klijenti) zahtijeva eRačun infrastrukturu **odmah**
- Polar.sh kao MOR možda pokriva eRačun za digital goods, ali nije eksplicit potvrđeno za HR
- **Akcija**: pri Faza 1 setupa, integriraj eRačun rješenje (FINA, Helena, Moj eRačun ili sl.)

---

## 2. Zašto j.d.o.o. (a ne odmah d.o.o.)

### 2.1 Trošak razlike
| Stavka | j.d.o.o. | d.o.o. |
|---|---|---|
| Temeljni kapital | 1.250 € odmah | 2.500 € (625 odmah, 1.875 u 1 god) |
| Pristojbe (sud + javni bilježnik via START) | ~26-200 € | ~26-200 € |
| Knjigovodstvo godišnje | 800-2.000 € (isti) | 800-2.000 € (isti) |
| **Ukupni cash drag prva godina** | **~1.500 €** | **~2.700 €** |

**Razlika**: ~1.200 € manje na startu za j.d.o.o. → ako prihod plan rastište na ~3-5k€ u prvih 6 mj, to je značajan delta.

### 2.2 Konverzija j.d.o.o. → d.o.o.
- Kad temeljni kapital naraste do 2.500 € (iz dobiti, dokapitalizacija ili oboje), automatska promjena oblika
- **Bez nove registracije** — samo podnošenje sudu nakon godišnjeg računovodstva
- Drži taj plan u svom 12-mj horizontu

### 2.3 Praktični tijek otvaranja j.d.o.o.

**Korak 1 — Predregistracija (1-2 dana)**:
- eOsobna iskaznica (s čitačem) ili mToken (HABA, Erste, PBZ-ov certA) — jedan od ova tri
- Pristup [START platformi](https://start.gov.hr/)
- Online popunjavanje + plaćanje sudske pristojbe karticom (~26 €)

**Korak 2 — Sjednica kod javnog bilježnika** (ako START traži):
- ~120-200 € javnobilježnička naknada
- Potpis ugovora o osnivanju + izjave osnivača

**Korak 3 — Otvaranje IBAN-a** (1-3 dana):
- HRK Wallet kod banke (Erste, PBZ, Zaba, RBA, OTP)
- **Preporuka za SaaS biznis**: Erste **Mojo** business ili PBZ **Online business** — niže mjesečne naknade (~5-15 €/mj)
- Uplata temeljnog kapitala 1.250 € → potvrda banke → predaja sudu
- **Alternativa**: Wise Business ili Revolut Business — ali HR sudski registar zahtijeva **HR IBAN** za upis pa to nije zamjena za primarni račun

**Korak 4 — Upis u sudski registar** (2-3 dana):
- Sud automatski iz START platforme
- Dobiva se MBS, OIB pravne osobe, izvod iz sudskog registra

**Korak 5 — Aktivacija OIB-a**:
- Porezna uprava — eOsobna ili odlazak u poreznu
- Aktivacija HZZO + HZMO (mirovinsko + zdravstveno)
- **Ako si jedini direktor i radiš u svom d.o.o.**: obvezan minimalni obračun plaće → ~700-900 €/mj **bruto** doprinosi (čak i ako neto = 0)

**Korak 6 — Knjigovodstvo**:
- Računovodstveni servis: 100-200 €/mj (mali d.o.o.)
- Alternativa: Minimax + sam vodiš (60-80 €/mj softver) — **rizik**: HR računovodstvo i porezne prijave su komplicirane, krivu vodi i može te koštati

**Ukupno vrijeme**: **5-10 radnih dana** od početka do operativnog d.o.o.

---

## 3. Mjesečni operativni trošak j.d.o.o. (procjena)

| Stavka | Trošak/mj | Bilješka |
|---|---|---|
| Plaća direktora (obvezna minimalka) | ~700-900 € bruto | HZZO + HZMO + porez na dohodak |
| Knjigovodstvo | 100-200 € | Vanjski računovodstveni servis |
| Banka business račun | 5-15 € | Erste/PBZ/Zaba |
| eRačun servis (FINA Moj eRačun) | 5-15 € | Obvezan od 2026 |
| **Ukupno fiksno** | **~810-1.130 €/mj** | **~10-13.5k€/god** |

**Break-even prihod**: ~13.500 € godišnji prihod tek pokriva fiksne troškove pravne osobe. Ovo je **ozbiljan break-even** za solo dev SaaS — bolje je prvih 3-6 mj raditi kao **fizička osoba s ugovorom o djelu** (test market) **prije** otvaranja j.d.o.o.

### 3.1 Alternativa: faza 0 kao fizička osoba
- **Pre-d.o.o. faza**: 3-6 mj kao fizička osoba, naplata kroz **paušalni obrt s NKD 62.01** (računalno programiranje, ne pravne usluge)
- Ograničen scope: **NE prodajeti gotove pravne dokumente** (nadripisarstvo) — prodaješ **alat** (softver, knjižnicu, template)
- Marketing: "računalni alat za izradu dokumenata, ne pravna usluga" — eksplicitno disclaimer
- **Cilj te faze**: validacija — dosegnuti ~50-100 platežnih usera prije otvaranja j.d.o.o.

**Risk paušala**: i dalje ulaziš u sivu zonu nadripisarstva ako proizvod **ne ograniči korisnike na pravnike i fizičke osobe za vlastite stvari**.

### 3.2 Ipak preporuka: skipni paušal, idi direktno j.d.o.o.

Razlozi:
1. **Pravna sigurnost** > marginalna ušteda 1k€ u prvih 6 mj
2. **AZOP teret** je nepostojan: kao fizička osoba, kazna do 20M EUR / 4% globalnog prometa **ide protiv tebe osobno** — to ti uništava budući kreditni rating, kuću, plaću
3. **Polar.sh KYC** prima d.o.o. profesionalnije od fizičke osobe (Stripe Connect Express)
4. **Nadripisarstvo argument**: kao d.o.o. s licencom računalnog razvoja, jasnija je razlika od pravne usluge

---

## 4. Porezni režim za d.o.o./j.d.o.o. 2026

### 4.1 Porez na dobit
- **10% za prihode do 1.000.000 €/god**
- **18% za prihode preko 1M €/god**
- Plaća se **godišnje** (do 30. travnja sljedeće godine), **predujmovi mjesečno**

### 4.2 Porez na dohodak od kapitala (kad isplatiš dobit sebi)
- **12% jedinstveno**
- Primjer: d.o.o. ostvari 50k € dobiti → plati 5k € poreza na dobit (10%) → 45k € ostane → ti isplatiš sebi → 12% × 45k = 5.4k poreza na dividendu → **neto ti ostane 39.6k €** (efektivna stopa ~21%)

### 4.3 PDV
- **Obvezni ulazak** kad prihod prijeđe 40.000 €/god (HR prag) ili pri prvoj B2B fakturi za EU klijenta
- **Stopa**: 25% (standardna) — ali **digital services** za EU B2B = **reverse charge** (obrnut obračun PDV-a)
- **Polar.sh kao MOR**: Polar preuzima PDV obvezu za prodaje **digital goods B2C**. Za B2B (NPL agencije, banke) — provjeri eksplicit s Polar support-om.

### 4.4 Doprinosi za direktora
Ako si jedini član j.d.o.o. i radiš u njemu, obavezno se obračunavaju doprinosi i porez na minimum bruto plaću (~5.262 € od 2026, MIROVINA gornja granica). Stvarne stope:
- **HZMO**: 20% (15% I stup + 5% II stup)
- **HZZO**: 16,5%
- **Porez na dohodak**: 23% niža stopa (ispod ~5.000 €/god) — od 2026 nove stope

**Bruto-neto razlika**: ~30-40% direktor uplaćuje državi.

---

## 5. Decision gate: kad migrirati j.d.o.o. → d.o.o.

| Trigger | Akcija |
|---|---|
| Temeljni kapital naraste >= 2.500 € | Konverzija u d.o.o. (samo prijava sudu) |
| Godišnji prihod > 100.000 € | **Ozbiljno razmotri** vanjske investitore — d.o.o. status pomaže (jasniji corporate governance) |
| Godišnji prihod > 1.000.000 € | **Obavezno** — porezna stopa skače s 10% na 18%, optimizacija (npr. R&D incentive) treba ozbiljnu strukturu |
| Privlačiš strane B2B klijente (EU, US) | d.o.o. je profesionalniji "izgled", j.d.o.o. konceptualno je "starter" forma |

---

## 6. Sljedeći koraci (Faza 1 iz `06_MILESTONES.md`)

1. **Provjeri eOsobnu iskaznicu**: imaš li je s čitačem? Ako ne, alternativa je mToken HABA (HABA = HABA Online preko Erste, ako ne onda mToken kod druge banke s certA)
2. **Otvori račun na START platformi**: [start.gov.hr](https://start.gov.hr/)
3. **Naziv tvrtke**: predloženo `LegalTech Suite j.d.o.o.` ili `LST Hrvatska j.d.o.o.` ili sličan brand-konzistentan naziv
4. **NKD klasifikacija**: glavna djelatnost **62.01 (Računalno programiranje)**, sekundarna **63.99 (Ostale informacijske uslužne djelatnosti, n. d.)** — IZBJEGAVAJ 69.10 (Pravne djelatnosti) jer to traži položen pravosudni ispit
5. **Sjedište**: Zagreb (tvoja rezidencija prema memory) — adresa može biti virtualna (Coworking Office, virtual office služi ~30-60 €/mj) ako ne želiš javno otkriti kućnu adresu
6. **Direktor**: Hrvoje Matej Lešić, sole director
7. **Otvori HR IBAN business**: Erste Mojo Business ili PBZ Online — sa eOsobnom istog dana
8. **Kontakt računovodstveni servis**: 2-3 ponude (Aning, Brojevi, Aestus, lokalne male agencije Zagreb)
9. **eRačun rješenje**: FINA Moj eRačun (besplatno za male) ili Helena (paušal ~5 €/mj)

---

## 7. Reference

- [START platforma](https://start.gov.hr/)
- [Porezna uprava — Porez na dobit](https://porezna-uprava.gov.hr/hr/porez-na-dobit-3940/3940)
- [HOK — Paušalno oporezivanje](https://www.hok.hr/gospodarstvo-i-savjetovanje/obrtnicka-pocetnica/pausalno-oporezivanje-dohotka)
- [Fiskalizacija 2.0](https://expertise.hr/fiskalizacija-2-0-kljucne-promjene-rokovi-i-obveze-za-eracune-od-2026/)
- [j.d.o.o. vodič 2026](https://kako.hr/financije-pravo/kako-osnovati-jdoo-u-hrvatskoj)
- [NKD 2025 odluka](https://narodne-novine.nn.hr/clanci/sluzbeni/2024_04_47_800.html)
