# HANDOFF — Sljedeća sesija

> Nastavi u `C:\Users\{{WIN_USER}}\Documents\APLIKACIJA`
> Pročitaj CLAUDE.md za puni kontekst projekta.

## Što je gotovo (Session 11):

1. **Hrvatski znakovi popravljeni** — cijela aplikacija sada koristi čšćđž:
   - `stranice/jednostavno.py` — 785 linija prepisano (bio potpuno bez dijakritika)
   - `LEGAL-SUITE.py` — svi navigacijski ključevi (_MODULI dict), vodič, opisi
   - `stranice/epredmet.py`, `stranice/nn_pretraga.py` — reference ažurirane
2. **CSS font fix** — `@import url()` unutar `<style>` zamijenjen s `<link>` tagom (ne blokira Streamlit Cloud)
3. **Suptilni CSS redesign** primijenjen ali korisnik NIJE ZADOVOLJAN:
   - Inter Variable Font, weight 425, letter-spacing, font-feature-settings
   - Aurora sidebar (radial gradients), shadow hierarchy, focus-visible, prefers-reduced-motion
   - Ali vizualno izgleda gotovo isto — "udžbenik iz biologije" (bijela pozadina + plavi sidebar)
4. **Skill `/design:ui-architect`** obogaćen (828 linija) — OKLCH, WCAG 2.2, aurora, anti-slop
5. Svi 129 testova prolaze, pushano na GitHub

## Što treba ODMAH sljedeće — DRAMATIČAN UI redesign:

Korisnik želi vidljivo drugačiji, premium UI. Trenutni dizajn je "biologija udžbenik" — prevelik bijeli prostor, generičan flat sidebar. Treba:

### Konkretni vizualni problemi:
- **Previše bijelog prostora** — stranica izgleda prazno i generično
- **Sidebar je flat plavi blok** — aurora gradijenti su presuptilni, jedva vidljivi
- **Kartice nemaju dubinu** — flat bijele kutije s tankim borderom
- **Nema atmosfere** — solid bijela pozadina bez teksture/dubine
- **Hero sekcija je mala** — ne dominira stranicom

### Što napraviti:
1. **Pročitaj `~/.claude/commands/design/ui-architect.md`** — ima kompletne specifikacije
2. **Sidebar**: pojačaj aurora efekt — veći opacity na radial gradientima, vidljivije boje
3. **Pozadina**: zamijeni čistu bijelu s blagim gradijentom ili teksturom (`_BG` u config.py)
4. **Kartice**: dodaj vidljivije sjene, hover efekte s bojom, možda blagi gradient na pozadini
5. **Hero sekcija**: veći padding, veći font, izraženiji gradient, možda animacija
6. **Tipografija**: veći kontrast veličina (h1 dramatično veći od body texta)
7. **Sidebar gumbi**: vidljiviji hover/active efekti
8. **Sve promjene su u `config.py`** (CSS_STILOVI) i eventualno inline stilovi u `LEGAL-SUITE.py`

### Referentni dizajn: Linear, Stripe Dashboard, Vercel
- Atmospheric backgrounds (ne flat bijela)
- Colored shadows matching element color
- Asymmetric spacing (tight within groups, wide between sections)
- Dramatic type scale

### Fajlovi za editirati:
- `config.py` — CSS_STILOVI (svi stilovi)
- `LEGAL-SUITE.py` — hero sekcija, kartice, vodič (inline HTML stilovi)
- `stranice/jednostavno.py` — hero sekcija, kartice (inline HTML stilovi)

## Dugoročni plan (NAKON UI redesigna):

1. Inovacija prema `C:\Users\{{WIN_USER}}\Desktop\PRAKTIČNA PRIMJENA AI-ja U PRAVU\MD verzije\claude\PROJEKTI\LEGAL-SUITE53`
2. Analiza svakodnevnih dokumenata za neuke stranke on-the-go
3. Problemi iz PROBLEM_S_APP.md (autoscroll, input validacija, uvjeti korištenja, itd.)

## Pokretanje:
```
cd "C:\Users\{{WIN_USER}}\Documents\APLIKACIJA"
streamlit run LEGAL-SUITE.py --server.headless true
python -m pytest tests/ -x -q
```
