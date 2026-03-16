# LegalTech Suite Pro - Plan poboljsanja

## Zavrseno (prethodne sesije)
- [x] OIB ISO 7064 mod-11-10 checksum validacija
- [x] Baza hrvatskih sudova (74 suda) + selectbox helper
- [x] Podrska za vise stranaka (dinamicko dodavanje/uklanjanje)
- [x] Integracija court selectbox u sve stranice (11 modula)
- [x] Kalkulator sudskih pristojbi (pristojbe.py + stranica + integracija)
- [x] Predlosci standardnih klauzula (klauzule.py + ugovori.py)
- [x] Smart navodnici - „hrvatske" navodnike s italikom
- [x] DOCX footer/hr/potpis poboljsanja
- [x] Uklonjen legacy kod (pripremi_za_word, _rimski kopija)
- [x] Validacija unosa + date_input popravke
- [x] 87 unit testova
- [x] zaglavlje_sastavljaca() u svim stranicama (7 modula)
- [x] Standardizacija signature-block u svim generatorima
- [x] Kamate kalkulator s HNB stopama + DOCX export
- [x] CLAUDE.md azuriranje
- [x] Help tooltips na kljucnim form poljima (tuzbe, ovrhe, zemljisne, obvezno, trgovacko)
- [x] 112 unit testova (25 novih edge case testova)
- [x] XSS fix: _escape(vrsta) u tuzbe generatoru
- [x] format_eur() robustnost (string/invalid input handling)
- [x] Informativna pocetna stranica s pregledom mogucnosti
- [x] upute.md - deploy na Streamlit Community Cloud
- [x] DOCX watermark opcija ("NACRT") - VML shape u headeru
- [x] DOCX header s imenom dokumenta (sivi italic tekst + linija)
- [x] DOCX opcije expander na svim stranicama (watermark + header checkbox)
- [x] 116 unit testova (4 nova za watermark/header)

## Buduci taskovi (sljedece sesije)

### Faza 20 - Predlozak sesije (session state persistence)
- [ ] 20.1 Dodati st.session_state cache za unos stranaka (da se ne gube podaci)
- [ ] 20.2 Dodati "Ocisti formu" gumb u svaku stranicu

### Faza 22 - Poboljsanje DOCX exporta (preostalo)
- [ ] 22.1 Popraviti colspan/rowspan u tablicama (cost-table)
