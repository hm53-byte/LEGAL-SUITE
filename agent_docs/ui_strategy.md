# LegalTech Suite Pro - UI/UX Strategija

## Stil: Trust-Centric Svicarski Minimalizam

### Ciljna publika
- **Laici**: Anksiozni korisnici kojima su odvjetnici preskupi. Trebaju jednostavnost i povjerenje.
- **Odvjetnicki uredi**: Profesionalci bez spranci. Trebaju brzinu i efikasnost.

### Principi dizajna
1. **Autoritet kroz jednostavnost** - maksimiziraj omjer signala i suma
2. **Progresivno otkrivanje** - prikazuj samo informacije nuzne u tom trenutku
3. **WCAG 2.1 AA** - minimalno 4.5:1 kontrast za tekst
4. **Smirenost** - nikakvi agresivni elementi, animacije ili vizualni sum

### Design Tokeni

```
--brand:          #1E3A5F   (Navy - autoritet, profesionalnost)
--brand-light:    #2D4A6F   (Navy hover)
--brand-surface:  #EFF3F8   (Svijetla plava pozadina)
--accent:         #B8860B   (Tamno zlato - vazna isticanja)
--accent-light:   #D4A843   (Zlato hover)
--surface:        #F8FAFC   (Pozadina stranice)
--card:           #FFFFFF   (Pozadina kartica)
--text-primary:   #0F172A   (Gotovo crna - 15.4:1 na bijeloj)
--text-secondary: #475569   (Siva - 5.9:1 na bijeloj)
--text-muted:     #94A3B8   (Utisana - koristiti samo za dekor, NE za tekst)
--border:         #E2E8F0   (Mekana siva granica)
--success:        #059669   (Smaragdna - download gumbi)
--warning:        #D97706   (Amber - upozorenja)
--sidebar-bg:     #0F1B2D   (Tamna navy pozadina)
--sidebar-text:   #CBD5E1   (Svijetla siva na tamnoj)
--sidebar-hover:  rgba(255,255,255,0.08)
```

### Tipografija (Modular Scale - Major Third 1.250)
- Display: 2.44rem / 700 / line-height 1.1
- H1: 1.95rem / 700 / line-height 1.2
- H2: 1.56rem / 600 / line-height 1.3
- H3: 1.25rem / 600 / line-height 1.4
- Body: 1rem / 400 / line-height 1.6
- Label: 0.875rem / 500 / line-height 1.4
- Caption: 0.75rem / 400 / line-height 1.5

### Streamlit ogranicenja
- Koristiti config.toml za baznu temu (eliminira FOUC)
- CSS injektirati kroz config.py za specijalizacije
- NE lomiti Streamlit React stablo agresivnim CSS-om
- Generirani dokumenti (.legal-doc) zadrzavaju Times New Roman - pravni standard

### Gated Workflow
1. Plan Mode - analiza zahtjeva vs postojeca arhitektura
2. Prijedlog dizajna - tekstualni plan s obrazlozenjem
3. Implementacija - tek nakon odobrenja
4. Verifikacija - screenshot analiza ako je dostupna
