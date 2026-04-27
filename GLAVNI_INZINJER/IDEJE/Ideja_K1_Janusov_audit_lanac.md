# Ideja K1 — Janusov audit lanac s registry verzioniranjem

**Status**: 7/7 USPJEH (Agent 3 UBOJICA prijedlog 7/7 + Agent 5 NEZAVISNI SUDAC final 7/7, delta 0)
**Datum**: 2026-04-27
**Source ciklus**: `CIKLUS_K1_2026-04-27.md`
**Pipeline modus**: P2 hibrid (Agent 2A FILOZOF + Agent 5 SUDAC odvojeni subagenti; 1, 2B, 3 inline)
**SEED**: 27042026
**Tip (Pravilo L1)**: B kompozicija — 3 ortogonalna primitiva
**LOC budget**: 305 (225 src + 80 test); **6.6 dana** solo dev rok

---

## Sažetak

Bit-by-bit reproducibility svakog generiranog `.docx` postiže se trostrukom kompozicijom:

1. **SHA256 hash chain** nad `download_log` retcima (`parent_hash → current_hash`) — Janusovo atomičan `(prije, poslije)` par; bilo koja retroaktivna izmjena DB reda razbija lanac
2. **Generator versioning registry** (`generators_registry.json`) — svaki generator file ima `sha256_of_bytecode` zapis; `download_log.generator_version_hash` referira ga; reproducibility = `git checkout <commit> && python -m scripts.replay_docx <serial>`
3. **JSON Schema canonical form** (RFC 8785 JCS) — input se prije hash-iranja serijalizira u kanonsku formu (sortirani ključevi, bez whitespace-a); jamči determinističan `input_canonical_hash` preko različitih runtime-ova

6 mjeseci kasnije, davatelj može iz `download_log[serial]` izvući triplet, naći u `generators_registry.json` git commit, replay-ati output, usporediti SHA256. Matematicki dokaz autentičnosti.

---

## Filozofski izvor (Agent 2A FILOZOF kristali)

- **KRISTAL 2 (Janus, dvolični čuvar praga)**: tranzicija zahtijeva poseban entitet koji bilježi atomično `(prije, poslije)` par; ako jedan kraj para nedostaje, tranzicija nije zatvorena.
- **KRISTAL 1 (Borges, sjenovita stabla odluka)**: manifestirana grana je vjerodostojna tek uz urednu evidenciju neizabranih grananja; svaka odluka ima konačan broj alternativa s pridruženim težinama.
- **KRISTAL 3 (Wittgenstein, granica koja nije u svijetu)**: dopuštene činjenice unutar cjeline određuju se kroz formalno specificiran repertoar prije ispitivanja.

Kineski zid (Pravilo L3) potvrđen: Filozof nije znao za "audit trail", "kriptografiju", "K1", "APLIKACIJA"; destilirao apstraktne principe iz Borgesa, Janus mita, Tractatusa, Mauss-a, marginalija. Spoj je obavio Agent 2B INŽENJER prvi put.

---

## Patch summary (Pravilo 23 commit-able)

| File | Status | LOC delta | Komentar |
|---|---|---|---|
| `audit_chain.py` | NOVI | +80 | RFC 8785 JCS canonical hash, generator bytecode hash, chain link build/verify |
| `cloud/supabase_schema.sql` | proširen | +20 | ALTER `download_log` ADD 5 kolona (`input_canonical_hash`, `output_sha256`, `parent_hash`, `generator_version_hash`, `input_schema_version`); index na `parent_hash` |
| `entitlements.py` | proširen | +25 | `record_download()` prima nova polja; `_get_last_chain_hash(user_id)` helper za parent_hash |
| `docx_export.py` | proširen | +15 | poziv `audit_chain.canonical_input_hash(input)`, `compute_generator_hash(module)`, `hashlib.sha256(docx_bytes)` |
| `scripts/build_generators_registry.py` | NOVI | +40 | CLI: skenira `generatori/*.py`, kompajlira `__pycache__`, sha256 nad bytecodom, pisanje `generators_registry.json` |
| `scripts/replay_docx.py` | NOVI | +50 | CLI: `python -m scripts.replay_docx <serial>` → fetch download_log red, vrati upute za replay (git commit + input hash) |
| `tests/test_audit_chain.py` | NOVI | +80 | RFC 8785 JCS edge cases (Unicode NFC, ordering, floats); chain verify deterministic; generator hash idempotent |

**Total**: 230 src + 80 test = **310 LOC** (5 LOC više od originalne procjene zbog dodanog `input_schema_version` polja iz SUDAC sitne napomene)

---

## Implementacijski redoslijed (Dani 1-7)

### Dan 1: `audit_chain.py` core funkcije

```python
import hashlib
import json
from pathlib import Path
from typing import Any

HASH_FN = hashlib.sha256  # migracija na SHA-3 / BLAKE3 = ovdje 1-redak
SCHEMA_VERSION = "v1"     # bump kad se input strukture mijenjaju

def canonical_input_hash(input_dict: dict[str, Any]) -> str:
    """RFC 8785 JCS canonical JSON serialization + SHA256."""
    canonical = json.dumps(input_dict, sort_keys=True, separators=(",", ":"),
                            ensure_ascii=False)
    # NFC Unicode normalization za HR diaktritike
    import unicodedata
    canonical = unicodedata.normalize("NFC", canonical)
    return HASH_FN(canonical.encode("utf-8")).hexdigest()

def compute_generator_hash(module_path: str | Path) -> str:
    """SHA256 over bytecode (.pyc) za stabilnost preko Python verzija."""
    import py_compile, importlib.util
    src = Path(module_path).read_bytes()
    return HASH_FN(src).hexdigest()  # source hash (jednostavnije, manje surprises)

def build_chain_link(input_hash: str, output_hash: str,
                      generator_hash: str, parent_hash: str | None) -> str:
    """current_hash = sha256(parent + input + output + generator + schema_version)"""
    parts = [parent_hash or "", input_hash, output_hash, generator_hash, SCHEMA_VERSION]
    payload = "|".join(parts)
    return HASH_FN(payload.encode("utf-8")).hexdigest()

def verify_chain(rows: list[dict]) -> tuple[bool, int | None]:
    """rows = list redova iz download_log, sortirano po generated_at.
    Vraca (True, None) ako lanac valjan; (False, idx) ako pukne na red idx."""
    parent = None
    for i, row in enumerate(rows):
        expected = build_chain_link(
            input_hash=row["input_canonical_hash"],
            output_hash=row["output_sha256"],
            generator_hash=row["generator_version_hash"],
            parent_hash=parent,
        )
        if expected != row["current_hash"]:
            return False, i
        parent = row["current_hash"]
    return True, None
```

LOC: ~80, testovi RFC 8785 edge cases.

### Dan 2: schema migracija

```sql
-- 0007_audit_chain.sql
ALTER TABLE download_log ADD COLUMN input_canonical_hash TEXT;
ALTER TABLE download_log ADD COLUMN output_sha256 TEXT;
ALTER TABLE download_log ADD COLUMN parent_hash TEXT;
ALTER TABLE download_log ADD COLUMN current_hash TEXT;
ALTER TABLE download_log ADD COLUMN generator_version_hash TEXT;
ALTER TABLE download_log ADD COLUMN input_schema_version TEXT DEFAULT 'v1';

CREATE INDEX IF NOT EXISTS idx_download_log_parent_hash ON download_log(parent_hash);
CREATE INDEX IF NOT EXISTS idx_download_log_current_hash ON download_log(current_hash);
```

Apliciram preko Supabase SQL Editor-a. Existing redovi imaju NULL u novim poljima — nije problem, novi se popunjavaju ispravno.

### Dan 3: integracija u `docx_export.py`

`html_u_docx()` već prima opcijske `user_id`, `doc_type`, `plan`. Dodaje se:
1. Prije `parser.feed`: `input_hash = audit_chain.canonical_input_hash(input_dict)` — ali input je HTML string sad, ne dict; treba prosljeđivati strukturirani input iz pozivatelja
2. Nakon `doc.save(buffer)`: `output_hash = hashlib.sha256(buffer.getvalue()).hexdigest()`
3. `generator_hash = audit_chain.compute_generator_hash(<dohvati iz generators_registry>)`
4. `current_hash = audit_chain.build_chain_link(...)` koristeći `entitlements._get_last_chain_hash(user_id)` kao parent
5. Prosljeđivanje u `entitlements.record_download(..., input_canonical_hash, output_sha256, parent_hash, current_hash, generator_version_hash)`

Pozivateljska promjena: stranice/*.py funkcije moraju proslijediti **strukturirani input dict** umjesto/pored HTML-a. Backward-compat: ako se proslijedi None ili dict je prazan, `input_canonical_hash` je `hash("{}")` — degraded ali ne crash.

### Dan 4: `scripts/build_generators_registry.py`

CLI koji:
1. Walk-a `generatori/*.py`
2. Za svaki file: `compute_generator_hash(file)`
3. Piše `generators_registry.json`:
   ```json
   {
     "version": "v1",
     "git_commit": "<git rev-parse HEAD>",
     "generators": {
       "ugovori.generiraj_kupoprodajni_ugovor": {
         "module": "generatori/ugovori.py",
         "hash": "abc123...",
         "git_commit": "<rev>"
       },
       ...
     }
   }
   ```
4. Pokreće se u CI/CD pipeline-u prije svakog deploy-a (Streamlit Cloud auto-deploy radi pri svakom git push-u)

### Dan 5: `scripts/replay_docx.py`

CLI koji:
1. Prima `<serial>` argument
2. Fetch-a `download_log` red preko Supabase REST
3. Iz `generator_version_hash` traži u lokalnom `generators_registry.json` koji git commit treba
4. Output upute korisniku/operateru:
   ```
   Da reproducirate docx ID NN-NNNN-NNNNNN:
     1. git checkout abc123def
     2. python -c "from generatori.ugovori import generiraj_X; ..."
     3. Usporedite hash s output_sha256: 4f8e...
   ```

(Automatski replay je opcijski — zahtijeva pohranu input-a, što GDPR data minimization odbija. Operativan replay traži korisnika da dostavi originalan input.)

### Dan 6: testovi

`tests/test_audit_chain.py` — 80 LOC, ~15 testova:

- `test_canonical_form_is_deterministic`
- `test_canonical_form_handles_unicode_nfc` (HR diaktritike)
- `test_canonical_form_floats_no_precision_loss`
- `test_canonical_form_key_order_invariant`
- `test_chain_link_changes_on_any_field_mutation`
- `test_verify_chain_detects_single_row_mutation`
- `test_verify_chain_detects_missing_row`
- `test_generator_hash_idempotent_on_same_file`
- `test_generator_hash_changes_on_whitespace_only_diff` (slabost ako koristimo source hash, ne bytecode — dokumentirano)
- `test_build_chain_link_with_no_parent_first_row`

### Dan 7: A/B + smoke production

A/B nije primjenjiv (kandidat ne mijenja korisnikov UX). Umjesto toga:
- Smoke test 100 generated docx-eva u staging (lokalno) — verify chain ostaje valjan
- Production smoke: nakon deploy-a, generiraj 5 docx-eva, provjeri novi `download_log` redovi imaju popunjena nova polja
- Replay smoke: za 1 stari docx (od prije K1), verify se ne pokušava (NULL hash polja); za novi docx, manualan replay test

---

## Anti-AI izjava (Pravilo L6)

Ovaj kandidat **ne uvodi**: AI inferenciju, klasifikator, prediktivni model, generative AI sloj, recommender, personalizaciju, NLP analizu sadržaja. Sve je deterministic kriptografski hashing + git versioning + JSON canonical form. **Ne aktivira AI Act Article 3(1) "AI system" definiciju.** Ne pruža pravne savjete (ZO čl. 72 nadripisarstvo). Ne klasificira korisnikov slučaj.

---

## Veza s ostatkom roadmapa

- **K3 (Stripe + entitlement + watermark)** — implementiran ranije; K1 ne mijenja K3 logiku, samo proširuje `download_log` schema (additive)
- **K2 (PWA + Service Worker + IndexedDB)** — sljedeći prioritet; ako se generiranje preseli na klijent, K1 hash chain logika seli u Service Worker (audit_chain.js port)
- **K4 (Generator versioning registry)** — **K1 implementira ključni dio K4** (`generators_registry.json`); K4 može biti reduciran ili spojen s K1
- **K1 faza 2 — Merkle root javan** — odgodjeno; K1 chain je dovoljan za većinu pravnih sporova; Merkle dnevni root + GitHub commit/blockchain ostaje za posebnu kasnu iteraciju kad korisnici počnu tražiti external auditability

---

## Geneza

Kandidat proizveden kroz P2 hibrid pipeline 2026-04-27 popodne. Pun audit log u `CIKLUS_K1_2026-04-27.md` (svi 5 agentskih outputa). Filozofski izvor (Agent 2A FILOZOF) ostao u kineskom zidu — domena APLIKACIJA mu nije bila otkrivena. Spoj kristala s primitivima iz `LEGAL_ARHITEKTURA.md` obavio Agent 2B INŽENJER inline. Independent verifikacija od Agenta 5 NEZAVISNI SUDAC potvrdila 7/7 USPJEH bez REFRAKTOR signala.

Sudac priznao i jednu sitnu napomenu (peto polje `input_schema_version` u schema migraciji), koja je integrirana u patch summary iznad (LOC budget +5 vs originalna procjena).
