# 05 — Go-to-Market strategija

> **Datum**: 2026-04-27
> **Polazna teza**: organic-first, B2B nakon validacije
> **Cilj 12 mj**: 100-200 PRO usera + 1-3 B2B klijenta

---

## 1. Tržišni segmenti — primarni vs sekundarni

Per memory `feedback_trzisni_segment_legaltech`:

| Segment | Veličina HR | Plafon plaćanja/mj | Težina prodaje | **Prioritet** |
|---|---|---|---|---|
| **Mali odvjetnici / javni bilježnici** | ~5.000 | 49-69 € | Niska (organic) | **Faza 1-2** (širina) |
| **Studenti prava (FINIO modul JARVIS LEX)** | ~10-15k aktivnih | 0-9 € | Niska (FREE konverzija) | **Faza 1-2** (top-of-funnel) |
| **Građani (DIY pravni dokumenti)** | ~milijun aktivnih | 5-15 € | Niska | **Faza 2-3** (volumen, niski LTV) |
| **NPL agencije** | ~30-50 | 300-1.000 € | Srednja | **Faza 3-4** (high LTV) |
| **Kreditni osiguravatelji** | ~10-15 | 500-2.000 € | Visoka | **Faza 4** |
| **Banke (compliance / collection)** | ~25 | 1.000-3.000 € | Vrlo visoka (sales cycle 3-9 mj) | **Faza 4** (anchor klijent) |
| **Računovodstveni servisi** | ~3.000 | 19-49 € | Srednja | **Faza 3** (ako prisutni dokumenti potrebni) |

### 1.1 Strategija segmentne sekvence

**Faza 1-2**: B2C širina + studenti FREE → validacija product-market fita. **Ne ulaziš u B2B prodaju** prije nego MVP s plaćanjem ima prvih 20-30 paying users.

**Faza 3**: NPL agencije — niska barijera ulaska (0-3 mj sales cycle), tržište već vjerojatno koristi competitor (BarbeQ, Rotaa, IT Sustav d.o.o.), tvoja diferencijacija = forenzički audit chain + open architecture.

**Faza 4**: Banke → ako Faza 3 NPL pokrene flywheel, Banke su "logičan next step" jer klijenti referenciraju.

---

## 2. Diferencijacija (zašto bi te netko izabrao)

### 2.1 Konkurenti u HR
| Player | Pozicija | Cijena | Slabosti |
|---|---|---|---|
| **Pronaut.hr** (ako još radi) | DIY pravni dokumenti za građane | ~10 €/dok | Bez audit chaina, dated UI |
| **JuriPro / Optimum / lokalni dev tools** | B2B legal automation | 200-1000 €/mj | Closed source, vendor lock-in |
| **MS Word + templates** | DIY za odvjetnike | (već plaćaju Office) | Ručno, error-prone, bez OIB validacije |
| **Excel kalkulatori** | Pristojbe, kamate | 0 € | Nepouzdano, nije pravna osnova |
| **IUS-INFO** | Pravna baza | ~50-100 €/mj | NIJE generator dokumenata, već pretraga |

### 2.2 Tvoja diferencijacija
1. **Forenzički audit chain** (K1 hash chain) — **NIKO drugi nema** u HR
2. **Open architecture** — ako klijent traži custom integracije, ne moraš ih čekati
3. **HR-specific** — sudovi.py, OIB validacija ISO 7064, NN ELI integracija, padezi imena
4. **Cijena** — €9 PRO je **dramatically jeftiniji** od JuriPro-a (+95% cheaper)
5. **AI-free** (per Pravilo L6) — paradoksalno **prednost u 2026**:
   - AI Act 2026 + nadripisarstvo prevent ulaze za AI legal SaaS-ove
   - Tvoj proizvod je **regulator-friendly by design**
   - "No AI in critical legal output" je marketabilan claim

### 2.3 Što NIJE diferencijacija (i ne reklamiraj):
- "Brži od pisanja ručno" — competitors imaju isto
- "Lijep UI" — subjektivno
- "Sve module" — kvaliteta > kvantiteta

---

## 3. Akvizicija — kanali

### 3.1 Faza 1-2 (organic, low CAC)

**Kanal 1: SEO content marketing**
- Blog na `legalsuite.hr/blog` — 2-3 članka/mj
- Teme:
  - "Kako napisati tužbu — 2026 vodič" (long-tail keyword)
  - "Sudski pristojbenik 2026" (kompleti članak + interactive widget)
  - "OIB validacija — kako provjeriti je li ispravan"
  - "Nadripisarstvo — što pravnici smiju, što ne smiju" (etika + relevantno)
  - "Audit chain za pravne dokumente — što je i zašto trebate"
- **Distribucija**: organic Google search, dijeli u FB grupama (Pravnici Hrvatska, Pravna pomoć HR), LinkedIn

**Kanal 2: HR Pravni forumi i Reddit**
- `/r/croatia` — povremeno (ne spam) odgovaraj na pitanja, link na alat samo kad relevantno
- Forum.hr (legal sub) — slično
- LinkedIn HR Pravo grupe

**Kanal 3: Studentska distribucija (JARVIS LEX modul leverage)**
- Memory ti potvrđuje da imaš JARVIS LEX modul (Silent Adversary Mode za studenta prava)
- Studenti prava na Pravnom fakultetu Zagreb, Rijeka, Split, Osijek = ~10-15k aktivnih
- **Plan**: FREE tier permanent za `*@student.pravo.hr` email domene → top-of-funnel

**Kanal 4: Cold partnerstva**
- Pravni fakultet Zagreb — predavanja, workshopi
- Hrvatska udruga mladih pravnika — sponzorstvo eventa (~200 €)
- Coworking spaces s legal-tech tenants

### 3.2 Faza 3 (paid, validacija ROI)

**Kanal 5: Google Ads**
- Keywords: "izrada tužbe", "sudski pristojbenik", "ovrha generator", "templejt punomoći"
- Budget: 100 €/mj test → eskalira ako CAC < 30 €
- Landing pages per keyword (ne single homepage)

**Kanal 6: LinkedIn Ads (B2B)**
- Targeting: HR users, jobs *Lawyer*, *Legal Counsel*, *Compliance Officer*, *Collection Specialist*
- Budget: 300 €/mj test
- Format: lead-gen forms (ne web traffic) — uhvati email za drip kampanju

### 3.3 Faza 4 (B2B sales)

**Kanal 7: Outbound sales**
- Lista 30-50 NPL agencija + banaka (LinkedIn Sales Navigator $80/mj 1 mj, otkaz)
- Personalized cold outreach (NIJE generic template) — referenciraj specifični problem
- 5-10 demo calls/tj cilj
- Conversion: ~10-15% demo → trial → paid

**Kanal 8: Industry conferences**
- HRBARLEX (HR Bar Conference)
- Banking Croatia Day
- Stand vs sponsorstvo (sponsorstvo budget: ~3-5k €/event, samo Faza 4)

---

## 4. Retention

### 4.1 Onboarding (per memory: no bait, no AI)
1. Email verifikacija → odmah u app
2. **Vodič wizard** (već imaš `_render_vodic`) → "Koji dokument želite napraviti?"
3. Prva tužba/dokument za 5 minuta — **success metric** = first document in <10 min
4. Email 24h kasnije: "Trebate li pomoć s drugim dokumentom?" → link na vodič

**Što NE radim**: drip kampanje, "Hi {{first_name}}, did you know..." manipulacija, sales nagging.

### 4.2 Engagement
- **Mjesečni newsletter** (2-3 članka iz blog-a + 1 product update) — opcionalan opt-in pri signupu
- **Promjene u zakonima koje utječu na tvoje dokumente** → automatski email kad nova NN objavi (Faza 3)
  - To bi koristilo `api_nn.py` za fetch i `cron job` (Hetzner only) → idi na Faza 3
- **Power user spotlight** (Faza 4) — interview HR odvjetnika koji koristi proizvod, blog post, social

### 4.3 Win-back
- 30 dana nakon cancellation: email "Što smo mogli bolje?" (1 klik survey)
- 90 dana: posebna ponuda "30% off prvih 3 mj povratka"
- 180 dana: STOP — ne salji više

---

## 5. Branding i pozicija

### 5.1 Tagline kandidati
- "Pravni alati koji odvjetnici koriste"
- "HR pravni dokumenti, profesionalna razina"
- "Forenzički provjerivi pravni alati"
- "AI-free pravna automatizacija — usklađen s AI Act 2026"

**Preporuka**: A/B test kroz početne PostmagPostmark Postmag emails (Faza 2-3).

### 5.2 Voice & tone
- **Profesionalan**, ne corporate-formal
- Hrvatski jezik **standardni** (ne kroatizmi tipa "kompjuter", "imejl")
- **Konkretan** (ne maglovit) — npr. "Generira tužbu za novčanu tražbinu" ne "Pomaže ti s pravnim stvarima"
- **Disclaimer** transparent: "Korisnik je odgovoran za pravnu valjanost — preporuka konzultacija s odvjetnikom"

### 5.3 Vizualni identitet
**Faza 1**: minimal brand (logo + 2 boje) — DIY u Figma free
**Faza 3**: brand designer (~500-1500 € za logo + style guide)
**Faza 4**: marketing materials (one-pagers, sales decks, demo videos)

---

## 6. Mjerenje uspjeha — north star metric

### 6.1 Primary metric
**Mjesečni broj generiranih dokumenata po platežnom useru** (DocsPerUser/mo).

Razlozi:
- Direktno odražava **stvarnu uporabu** (ne vanity signup count)
- Korelira s churn (low usage → high churn)
- Mjerljivo bez extra tooling-a (audit_chain ima record svakog dokumenta)
- B2B klijenti pri renewal će tražiti ove brojke kao opravdanje

**Targets**:
- Faza 2 baseline: 5 dok/mj/PRO user
- Faza 3 cilj: 8 dok/mj/PRO user
- Faza 4 cilj: 15 dok/mj/PRO user (više usage = sticky)

### 6.2 Secondary metrics
- MRR (Monthly Recurring Revenue) — financijski
- Churn rate — health
- CAC payback period — paid acquisition zdravlje
- Trial → paid conversion — funnel zdravlje
- NPS — kvalitativni

---

## 7. Sales process za B2B (Faza 4)

### 7.1 Funnel stages
1. **Cold outreach** (LinkedIn DM, email)
2. **Discovery call** (30 min, free)
3. **Demo** (45 min, scenarios specific to klijent)
4. **Trial** (14 dana, dedicated support)
5. **Proposal** (custom price, contract draft)
6. **Negotiation** (1-3 iteracije)
7. **Close** (signed contract + first invoice)

### 7.2 Sales materials potrebni
- One-pager (PDF, 1 stranica) — trebao bi raditi sam
- Demo video (3-5 min, screencast)
- Customer reference (Faza 4: prvi B2B klijent kao reference)
- Security/compliance Q&A doc (česta pitanja: where data hosted, GDPR, SOC2)

### 7.3 Pravni materijali za B2B
- **Master Service Agreement** template (~500-1000 € odvjetnik)
- **Data Processing Agreement** (DPA)
- **NDA** template (besplatan iz online izvora, prilagodi)

---

## 8. Konkurentske misli

### 8.1 Što se događa ako veliki igrač uđe
- **Microsoft Copilot for Legal** ulazi u HR? → tvoj diferencijator je AI-free + lokalna HR specifičnost
- **WoltersKluwer / LexisNexis** lansira HR alat? → tvoja prednost je cijena (10x jeftiniji)
- **Domaći konkurent na BarbeQ ili sl. lansira tier ispod tvog**? → nemaš zaštitu osim brzine inovacije i forenzičkog audit chaina

### 8.2 Što se događa ako AZOP udari
**Risk**: AZOP rješenje prema komercijalnom legaltech-u koji koristi javne registre.
**Mitigacija**: dokumentirana DPIA + atribucija + konzultacija odvjetnika prije Faze 2 launch-a.
**Worst case**: rebrand + pivot na "alat za odvjetnike, ne građane".

### 8.3 Što se događa ako HOK udari (nadripisarstvo)
**Risk**: HOK proglasi proizvod nadripisarstvo, prijava državnom odvjetništvu.
**Mitigacija**:
- Faza 0-1: explicitan disclaimer "alat, ne pravna usluga"
- Faza 2-3: target *odvjetnici* primarno, građani sekundarno (više vide alat kao pomoć profesionalcima)
- Faza 4: HOK partnership pokušaj (sponzorstvo eventa, daj im custom verziju za članove)

---

## 9. Sljedeći koraci

**Faza 1**:
- Postavi `legalsuite.hr/blog` (statisticki Hugo/Astro, hostiran na CF Pages free)
- Napiši prvih 3 članka (HR pravni vodiči, SEO-targeted)
- Setup Google Search Console + Plausible Analytics (privacy-friendly, EU rezidentno)

**Faza 2**:
- Aktiviraj **`*@student.pravo.hr` permanent FREE** (memory note: imamo confirmation)
- Postavi LinkedIn HR profilu **Hrvoje Matej Lešić** kao "Founder, LegalTech Suite Pro" (kasnije, kad d.o.o. radi)
- Pokreni mjesečni newsletter (~50 subskribera initial)

**Faza 3**:
- Lista 50 NPL agencija + zaračunaj ekonomiju cold outreach-a
- Test Google Ads s 100 €/mj budget
- Mjeri CAC i adjust

**Faza 4**:
- 5-10 B2B klijenata za 12 mj
- Sponzorstvo HRBARLEX-a
- SOC 2 priprema ako enterprise traži
