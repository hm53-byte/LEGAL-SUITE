# Upute za deploy na Streamlit Community Cloud

## Preduvjeti

1. **GitHub racun** - besplatan na https://github.com
2. **Streamlit Community Cloud racun** - besplatan na https://share.streamlit.io (prijava s GitHub racunom)

## Koraci

### 1. Stavi kod na GitHub

Kod je vec na GitHubu: https://github.com/{{GITHUB_KORISNIK}}/LEGAL-SUITE

Za buduce promjene:
```bash
cd "C:\Users\{{WIN_USER}}\Documents\APLIKACIJA"
git add -A
git commit -m "Opis promjene"
git push
```

### 2. Deploy na Streamlit Community Cloud

1. Idi na https://share.streamlit.io
2. Klikni **"New app"**
3. Ispuni formu:
   - **Repository**: odaberi `{{GITHUB_KORISNIK}}/LEGAL-SUITE`
   - **Branch**: `main`
   - **Main file path**: `LEGAL-SUITE.py`
4. Klikni **"Deploy!"**

Streamlit ce automatski:
- Instalirati dependencies iz `requirements.txt`
- Pokrenuti aplikaciju
- Dati ti public URL (npr. `https://legaltech-suite-pro.streamlit.app`)

### 3. Pristupi aplikaciji

Nakon deploya (1-2 minute), dobit ces link oblika:
```
https://tvoj-app-name.streamlit.app
```

Taj link mozes otvoriti s bilo kojeg uredaja (mobitel, tablet, racunalo).

## Azuriranje aplikacije

Kad napravis promjene lokalno:
```bash
git add -A
git commit -m "Opis promjene"
git push
```

Streamlit Cloud automatski detektira push i redeploya aplikaciju (obicno unutar 1-2 minute).

## Napomene

- **Besplatno**: Streamlit Community Cloud je potpuno besplatan za public repoe
- **Private repo**: Takoder besplatan, ali ima limit na 1 privatnu app
- **Sleep mode**: Besplatne appove Streamlit uspava nakon neaktivnosti - prvi pristup nakon spavanja traje ~30 sekundi
- **Nema baze**: Aplikacija je stateless - nema perzistencije podataka. Svaki korisnik radi sa svjezim formama.
- **requirements.txt**: Mora biti u root folderu repoa. Vec postoji s `streamlit` i `python-docx`.

## Troubleshooting

| Problem | Rjesenje |
|---------|----------|
| "Module not found" | Provjeri da su svi importi u `requirements.txt` |
| App se ne pokrece | Provjeri logove na Streamlit Cloud dashboardu |
| Spor deploy | Normalno - prvi deploy moze trajati do 5 min |
| "Resource limits" | Besplatni tier ima 1GB RAM limit - ova app koristi ~100MB |
