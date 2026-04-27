# 04 — Cjenovni model

> **Datum**: 2026-04-27
> **Status**: PRELIMINARAN — finalna struktura ide kroz **GOAT C5** (vidi `07_BUDUCI_GOAT_CIKLUSI.md`)
> **Polazna pretpostavka**: Polar.sh kao MOR (B2C), ručna B2B fakturacija (početak)

---

## 1. Cjenovni model — three-tier ladder

### 1.1 Tier struktura (preliminarno)

| Tier | Cijena/mj | Cijena/god (-15%) | Limit | Cilj segment |
|---|---|---|---|---|
| **FREE / GUEST** | 0 € | — | 5 dokumenata/mj, watermark, bez audit chaina | Lead generation, lurkers |
| **PRO** | **9 €/mj** | **92 €/god** | Neograničeno dokumenata, audit chain, sve napomenute značajke | Mali odvjetnici, javni bilježnici, građanski korisnici |
| **STUDIO** | **29 €/mj** | **295 €/god** | + multi-user (do 5), customizable templates, prioritetna podrška | Mala odvjetnička društva (2-5 odvj.) |
| **PRO+ / B2B** | **150-500 €/mj** | individualno | + e-pravnik review, SLA, dedicated support, on-prem option, custom integracije | NPL agencije, banke, kreditni osiguravatelji |

### 1.2 Razlozi za ovu strukturu

**Memory `feedback_trzisni_segment_legaltech`** kaže:
> Mali odvjetnici plafon 49-69 EUR/mj; pravi platežni segmenti su NPL agencije, investitori, kreditni osiguravatelji, banke (300-3000 EUR/mj)

Ovo je **ključan input**. Postojeći Polar plan (~9 €/mj) je dobar **ulazni** tier, ali **nije dovoljan za break-even** — vidi `02_PRAVNA_STRUKTURA.md` (~10-13.5k €/god fiksni trošak d.o.o.). 100 PRO usera × 9 €/mj × 12 = 10.8k €/god — **tek pokriva fiksne**.

**Plan**:
- PRO tier (9€) **drži kao current**, validira market
- **STUDIO tier (29€)** — *novi*, gađa multi-user mali law firm. Koraci do toga: dodati team management u app (Faza 3)
- **B2B tier (150-500€)** — *kritičan break-even fix*. 5-10 B2B klijenata = 9-50k€/god + scale potential

### 1.3 Što FREE tier mora imati (ulaz)

**Cilj FREE tier-a**: korisnik napravi prvi dokument, vidi vrijednost, pretvori se u PRO.

**Što FREE smije**:
- 5 dokumenata mjesečno (rolling window)
- Watermark u dokumentima ("Generirano LegalTech Suite Pro — pretplata na...")
- Sve module dostupne (ne ograničavaš na 1-2)
- Vodič wizard, tooltipovi, primjeri
- Basic OIB validacija + Sudreg lookup

**Što FREE NE smije**:
- Audit chain (forenzički hash) — to je premium značajka
- Bulk export
- Custom branded watermark
- Team sharing
- API pristup

### 1.4 Watermark logika

Watermark je **lateralan retention tool** — svaki put kad FREE user pošalje dokument klijentu, klijent vidi "LegalTech Suite Pro" — virusna distribucija.

**Implementacija**: već postoji `watermark.py` u repo-u. Treba samo conditionally aktivirati za FREE tier:
```python
if user_tier == "FREE":
    add_watermark(doc, "Generirano LegalTech Suite Pro — pretplata na legalsuite.hr")
```

---

## 2. Pretplata vs jednokratna kupnja vs credits

### 2.1 Tri modela
| Model | Plus | Minus | Verdict |
|---|---|---|---|
| **Pretplata mjesečna** | Predvidljiv prihod, niska ulazna barijera | Crkvena lojalnost (churn) | **DA — primarni model** |
| **Pretplata godišnja (-15%)** | Cash flow + lojalnost | Veća ulazna barijera | **DA — sekundarno** |
| **Jednokratna kupnja po dokumentu** | "Pravnik nije profesionalan, samo trebam jedan dokument" | Loš LTV, kompleksnije billing | NE u Faza 0-2 |
| **Credits / pay-as-you-go** | Fleksibilnost | Kompleksnost UI + naplata | NE |
| **One-time pro license (LTD lifetime)** | Cash burst za marketing pricing | Bez recurring revenue | **NE** — anti-pattern za SaaS |

### 2.2 Free trial
**Preporuka**: 14-dnevni PRO trial **bez kreditne kartice** za prva 100 usera — onda požuri na "potrebna kartica".

**Razlog**: HR korisnici su **kartično skeptični** (visok ratio cash transactions). Trial bez kartice znatno povećava conversion.

**Risk mitigation**: ograniči trial na **5 dokumenata** (isti limit kao FREE), ali otključa audit chain + premium značajke.

---

## 3. Pricing test plan

### 3.1 Faza 2 (do 50 platežnih) — fixed price 9€/mj
Ne testiraj pricing još. Cilj: **product-market fit**, ne profit optimization.

### 3.2 Faza 3 (50-200 platežnih) — A/B testovi
- **Test 1**: Cijena 9€ vs 12€ (split 50/50 nove signupse)
- **Test 2**: Free trial 7 dana vs 14 dana
- **Test 3**: Annual discount 15% vs 20%

**Tooling**: GrowthBook ili Statsig free tier; ako ne želiš dodavati infrastrukturu, ručno se može (snapshot conversion ratio po datumu signup-a).

### 3.3 Faza 4 (B2B negotiated)
B2B price discovery = **sales call**, ne A/B test.
- Anchor pri 500 €/mj
- Spustiš na 300 €/mj ako klijent traži
- Ne ispod 150 €/mj — to je tvoj **walk-away point**

---

## 4. Cohort i unit economics (procjena)

### 4.1 Pretpostavke
- **CAC** (cost of acquisition): 0 € u Faza 0-2 (organic), ~30 €/user u Faza 3 (paid ads)
- **Churn**: 5%/mj (tipičan SaaS B2C, viši za pravne tools)
- **LTV** (lifetime value): 9 €/mj × (1/0.05) = **180 €** po PRO useru
- **LTV:CAC** ratio: 180/30 = **6x** (zdravo, > 3x je standard)

### 4.2 Rast scenariji (12 mj iz Faze 2)

| Scenario | Mj 0 | Mj 3 | Mj 6 | Mj 9 | Mj 12 | Total revenue |
|---|---|---|---|---|---|---|
| **Pesimistic** | 5 | 15 | 25 | 35 | 50 | ~3.5k € |
| **Realistic** | 5 | 25 | 60 | 90 | 130 | ~9k € |
| **Optimistic** | 10 | 50 | 120 | 200 | 350 | ~22k € |

→ **Realistic 12-mj** = ~9k € / god → **NE pokriva** d.o.o. fiksne troškove (10-13k). 
→ **Implication**: B2B tier je **obvezno** za break-even unutar 12 mj. **Plan**: do mj 6 stiže prvi B2B klijent.

### 4.3 B2B unit economics
- **CAC B2B**: 200-1000 € (sales effort, demo, ugovaranje) — **veće**
- **LTV B2B**: 300 €/mj × 24 mj (manji churn) = **7.200 €**
- **LTV:CAC**: 7.2k/500 = **14x** — **highly profitable** segment

---

## 5. Free tier abuse mitigacija

### 5.1 Riziki
- Multi-account abuse (jedan korisnik → 10 free računa)
- Bot signups za scrapanje vrijednosti
- "Forever free" usera koji crawlaju

### 5.2 Mjere
**Faza 1**:
- Email verifikacija obvezna
- Phone verifikacija opcionalna (Faza 3+)
- IP rate limit (max 3 signups/IP/24h)

**Faza 3**:
- ML-free fingerprinting (Memory: BezAI policy) — server-side, ne browser fingerprint:
  - User-Agent header
  - Geo IP (Cloudflare CF-IPCountry)
  - Account creation pattern
- Manualni review accounts s `pravo.hr` domenom (sumnja na konkurenciju)

---

## 6. Cancellation i refund policy

### 6.1 Cancellation
- Self-service cancel u app-u (PRO settings)
- Cancellation = "downgrade na FREE od sljedećeg billing cycle-a"
- Bez pitanja, bez retention emaila u Faza 0-2 (priority je proizvod, ne retention growth hacks)

### 6.2 Refund policy
- 14-dnevni money-back guarantee (HR Zakon o zaštiti potrošača čl. 79 — pravo otkaza ugovora sklopljenog na daljinu)
- **Polar.sh handle-a refundove** (jedan od razloga MOR je dobar) — ti samo daješ "yes/no" odluku
- Anti-abuse: max 1 refund per user lifetime

---

## 7. Pricing page copy (preliminarno)

### 7.1 Tone
- **Direktan**, bez bullshit-a
- HR formalni ali ne-distantan
- **No fake urgency** ("⏰ samo danas!" = ne)
- **No bait framing** (per memory `feedback_no_bait_framing`)

### 7.2 Struktura
```
🎯 BESPLATNO              💼 PRO                   🏢 STUDIO
0 €/mj                     9 €/mj                   29 €/mj
                          ili 92 €/god (-15%)       ili 295 €/god (-15%)

5 dokumenata/mj            Neograničeno dok./mj      Sve iz PRO
Watermark                  Bez watermarka           +
Osnovni vodič              Audit chain               Multi-user (do 5)
                          Sve module                 Custom templates
[Probaj besplatno]         Standardna podrška         Prioritetna podrška
                          [Pretplati se]            [Pretplati se]
```

### 7.3 Što NE pisati u pricing page
- "AI powered" — per AI Act 2026 + nadripisarstvo policy
- "Zamjena za odvjetnika" — nikad
- "Pravni savjet" — nikad
- Garanciju uspjeha pravne radnje
- Bilo što što HOK može tumačiti kao reklamu pravnih usluga

### 7.4 Što DA pisati
- "Alat za izradu dokumenata"
- "Templates za sudske dokumente"
- "Računalna podrška u izradi pravnih akata"
- "Korisnik je odgovoran za sadržaj — dokument provjerava odvjetnik prije podnošenja"

---

## 8. Decision gate: kad uvesti svaki tier

| Tier | Trigger | Implementacijski rad |
|---|---|---|
| FREE | Faza 2 (sa Polar setup-om) | watermark logika + 5 dok/mj limit u entitlements.py |
| PRO 9€ | Faza 2 (osnovni MVP s plaćanjem) | Polar webhook + entitlement aktivacija |
| STUDIO 29€ | Faza 3 (50+ PRO usera, signal za multi-user) | team management UI, multi-tenant data isolation |
| PRO+ B2B | Faza 4 (prvi cold lead iz NPL/banke) | manual entitlement, custom plan |

---

## 9. Što ide u GOAT C5 (final pricing)

**Pitanja koja zaslužuju formalan GOAT ciklus prije Faze 2 launch-a**:

1. **Currency** — €9 vs $10 vs HRK ekvivalent? Polar je $-bazirana platforma, ali HR usere očekuje EUR billing.
2. **Annual discount** — 15% vs 20% vs 25%? (15% je standardan SaaS, 20%+ stimulira cash flow ali pojeftinjuje LTV)
3. **Trial duration** — 7 dana vs 14 dana vs 30 dana?
4. **Free tier limit** — 5 dok/mj vs 10 vs 3? (5 je preliminarna kalibrracija)
5. **Watermark text/design** — fiksni tekst vs personalizirani link? (per memory: ne bait)

**GOAT C5 treba dati**: decision matrix s 3 opcije za svaki kriterij, score, ROI procjenu. Procjena: ~10-15k tokena.

---

## 10. Reference

- Memory `feedback_trzisni_segment_legaltech` — segmenti i price ceilings
- `GOAT/PREPORUKA_MOR.md` — Polar.sh fees i ROI scenariji
- HR Zakon o zaštiti potrošača NN 41/14, 110/15, 14/19, 76/22 — refund policy
- Polar.sh pricing: 6% + $0.40 + Stripe pass-through (~6.5% all-in)
