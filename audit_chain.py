"""
audit_chain.py — K1 Janusov audit lanac (deterministic forensic primitive)

Tri ortogonalna primitiva (Tip B kompozicija prema Pravilu L1):

  1. SHA256 hash chain nad download_log retcima (`parent_hash → current_hash`)
     Janusovo atomično (prije, poslije) bilježenje — bilo koja retroaktivna
     izmjena DB reda razbija lanac.

  2. Generator bytecode versioning — SHA256 nad svakim generator file-om
     (`generators_registry.json`); bez versioning-a ne mozemo reproducirati
     output 6 mjeseci kasnije.

  3. JSON Schema canonical form (RFC 8785 JCS) — input se serijalizira u
     kanonsku formu (sortirani kljucevi, bez whitespace-a, NFC Unicode normalizacija)
     prije hash-iranja. Jamci determinizam preko razlicitih runtime-ova.

Reference (Pravilo 24, K1 ciklus):
  (a) RFC 8785 (Rundgren, Jordan, Erdtman 2020) — JSON Canonicalization Scheme
  (b) NIST FIPS 180-4 — SHA-2 family (SHA-256 specifikacija)
  (c) Schneier 1996, "Applied Cryptography" ch. 18.7 — hash chains

Anti-AI izjava (Pravilo L6): ovaj modul ne uvodi AI inferenciju, klasifikator,
prediktivni model, generative AI, recommender niti personalizaciju. Sve su
deterministicki kriptografske operacije. Ne aktivira AI Act Article 3(1).

Migracija na drugi hash algoritam (npr. SHA-3 ili BLAKE3 u slucaju kvantnog
napada na SHA-256) je 1-redak izmjena `HASH_FN` konstante; preostali kod ostaje.
"""
from __future__ import annotations

import hashlib
import json
import unicodedata
from pathlib import Path
from typing import Any, Callable


# =============================================================================
# Konstante
# =============================================================================

HASH_FN: Callable[[bytes], "hashlib._Hash"] = hashlib.sha256
"""Aktualan hash algoritam. Migracija na SHA-3 / BLAKE3 = ovdje 1 redak."""

SCHEMA_VERSION: str = "v1"
"""Verzija input schema-e. Bump pri breaking change-u u canonical form-u
(npr. promjena u tretmanu floats, Unicode normalizacije). Pohranjuje se u
download_log.input_schema_version radi forward-compat verifikacije."""


# =============================================================================
# 1. JSON canonical form (RFC 8785 JCS)
# =============================================================================


def canonical_input_hash(input_dict: dict[str, Any]) -> str:
    """SHA-256 hash kanonske JSON serijalizacije input dict-a.

    Slijedi RFC 8785 JCS pristup za reproducibilnu serijalizaciju:
      - Sortirani kljucevi (sort_keys=True)
      - Bez nepotrebnog whitespace-a (separators=(',',':'))
      - UTF-8 encoding bez BOM
      - NFC Unicode normalizacija (kriticno za HR diaktritike c/c/dj/s/z)
      - ensure_ascii=False — UTF-8 prirodno dopusta non-ASCII

    Vraca hex string (64 chars za SHA-256).
    """
    canonical = json.dumps(
        input_dict,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    canonical = unicodedata.normalize("NFC", canonical)
    return HASH_FN(canonical.encode("utf-8")).hexdigest()


# =============================================================================
# 2. Generator bytecode versioning
# =============================================================================


def compute_generator_hash(module_path: str | Path) -> str:
    """SHA-256 nad source bytes generator file-a.

    Source hash (ne bytecode .pyc) je odabran iz dva razloga:
      - Stabilan preko razlicitih Python verzija (.pyc se mijenja medu 3.10/3.11/3.12)
      - Reproducibilan iz git checkout-a (nema build artefakata)

    Slabost: whitespace-only diff promijenit ce hash. To je akceptirano —
    `generators_registry.json` se rebuildea pri svakom commit-u, pa hash
    odgovara trenutnom git commit-u. Reproducibility zahtijeva isti commit.
    """
    return HASH_FN(Path(module_path).read_bytes()).hexdigest()


# =============================================================================
# 3. Hash chain link build / verify
# =============================================================================


def build_chain_link(
    input_hash: str,
    output_hash: str,
    generator_hash: str,
    parent_hash: str | None,
    schema_version: str = SCHEMA_VERSION,
) -> str:
    """Izracun current_hash za novi audit log red.

    current_hash = SHA256( parent_hash | input_hash | output_hash | generator_hash | schema_version )

    Pipe ('|') separator je odabran jer:
      - SHA-256 hex nikad ne sadrzi pipe (samo [0-9a-f])
      - SCHEMA_VERSION je control string ('v1', 'v2'), NEMA pipe
      - eliminira concat-ambiguity attack (npr. ('a','bc') vs ('ab','c'))

    parent_hash=None za prvi red u lancu (genesis). Tada se ulazi prazna string.
    """
    parts = [
        parent_hash or "",
        input_hash,
        output_hash,
        generator_hash,
        schema_version,
    ]
    payload = "|".join(parts)
    return HASH_FN(payload.encode("utf-8")).hexdigest()


def verify_chain(rows: list[dict[str, Any]]) -> tuple[bool, int | None]:
    """Provjeri integritet hash chain-a nad sortiranim listom redova.

    `rows` mora biti sortirano kronologijski (po `generated_at` ASC); svaki red
    ima polja: `input_canonical_hash`, `output_sha256`, `parent_hash`,
    `current_hash`, `generator_version_hash`, `input_schema_version`.

    Vraca (True, None) ako je lanac valjan; (False, idx) ako pukne na redu idx.

    Algoritam: prolazi redove; za svaki racuna `expected_current` na temelju
    `parent_hash` (proslijedjen iz prethodnog reda ili None za prvi); usporedba
    s pohranjenim `current_hash`; ako se razlikuju → mutacija detektirana.
    """
    parent: str | None = None
    for i, row in enumerate(rows):
        expected = build_chain_link(
            input_hash=row.get("input_canonical_hash", ""),
            output_hash=row.get("output_sha256", ""),
            generator_hash=row.get("generator_version_hash", ""),
            parent_hash=parent,
            schema_version=row.get("input_schema_version", SCHEMA_VERSION),
        )
        if expected != row.get("current_hash"):
            return False, i
        parent = row.get("current_hash")
    return True, None


# =============================================================================
# Convenience: jedan-poziv API
# =============================================================================


def compute_full_audit(
    input_dict: dict[str, Any],
    output_bytes: bytes,
    generator_module_path: str | Path,
    parent_hash: str | None,
) -> dict[str, str]:
    """Glavni entry point. Racuna sve hash-eve potrebne za novi download_log red.

    Vraca dict spreman za upis u Supabase:
      {
        "input_canonical_hash": "<sha256>",
        "output_sha256": "<sha256>",
        "generator_version_hash": "<sha256>",
        "parent_hash": <parent or None>,
        "current_hash": "<sha256>",
        "input_schema_version": "v1",
      }

    Pozivatelj (docx_export.py) prosljedjuje to u entitlements.record_download().
    """
    input_h = canonical_input_hash(input_dict)
    output_h = HASH_FN(output_bytes).hexdigest()
    generator_h = compute_generator_hash(generator_module_path)
    current_h = build_chain_link(
        input_hash=input_h,
        output_hash=output_h,
        generator_hash=generator_h,
        parent_hash=parent_hash,
    )
    return {
        "input_canonical_hash": input_h,
        "output_sha256": output_h,
        "generator_version_hash": generator_h,
        "parent_hash": parent_hash,
        "current_hash": current_h,
        "input_schema_version": SCHEMA_VERSION,
    }
