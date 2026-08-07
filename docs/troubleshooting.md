# Otklanjanje grešaka

## `ModuleNotFoundError: No module named 'docx'`

```bash
pip install python-docx
```

Paket se instalira kao `python-docx`, a uvozi kao `docx`. `pip install docx` je
drugi, nepovezan paket.

## `ModuleNotFoundError: No module named 'pytest'`

`pytest` nije naveden u `requirements.txt` jer nije potreban za pokretanje
aplikacije. Za testove ga treba instalirati zasebno:

```bash
pip install pytest
python -m pytest tests/ -q
```

## Aplikacija na Streamlit Cloudu javlja grešku nakon push-a

Streamlit Cloud gradi novo virtualno okruženje pri svakom push-u, pa uvoz koji
lokalno radi može ondje pasti ako paket nije u `requirements.txt`. Provjera:

```bash
streamlit run LEGAL-SUITE.py     # radi li lokalno
python -m pytest tests/ -q       # prolaze li testovi
```

## Hrvatski znakovi (č, ć, ž, š, đ) u ispisu terminala na Windowsu

```powershell
$env:PYTHONIOENCODING = "utf-8"
```

Ili unutar skripte:

```python
import sys
sys.stdout.reconfigure(encoding="utf-8")
```

## Modul Sudskog registra javlja da nije konfiguriran

`api_sudreg.py` traži OAuth2 vjerodajnice u Streamlit secrets
(`sudreg_client_id`, `sudreg_client_secret`). Bez njih `pretrazi_subjekt()`
vraća poruku o nedostajućoj konfiguraciji. Vjerodajnice se traže kod
Ministarstva pravosuđa i uprave.

## Prijavljeni korisnici nestanu nakon restarta

`auth.py` sprema korisnike u lokalnu datoteku `.users.json`. Na Streamlit
Community Cloudu je disk efemeran, pa se datoteka gubi pri svakom ponovnom
pokretanju. Isto vrijedi za `_data/kalendar.json`. Trajna pohrana traži vanjsku
bazu i nije implementirana.
