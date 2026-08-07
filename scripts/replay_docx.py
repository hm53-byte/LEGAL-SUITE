"""K1 Dan 5: replay_docx CLI.

Za dani serial_hash, dohvati download_log red iz Supabase i ispise upute za
manualan replay (git checkout + generator poziv + hash usporedba).

Automatski replay nije podrzan jer se input ne pohranjuje (GDPR data
minimization Art 5(1)(c)) — korisnik mora dostaviti svoj originalan input.

Usage: python -m scripts.replay_docx <serial_hash>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from entitlements import _rest, _is_configured  # noqa: E402

REGISTRY_PATH = ROOT / "generators_registry.json"


def _find_generator_by_hash(generator_hash: str) -> tuple[str, dict] | None:
    if not REGISTRY_PATH.exists():
        return None
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    for name, info in reg.get("generators", {}).items():
        if info.get("hash") == generator_hash:
            return name, info
    return None


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.replay_docx <serial_hash>")
        return 1
    serial_hash = sys.argv[1].strip()

    if not _is_configured():
        print("Supabase secrets nisu postavljeni; replay nemoguc lokalno.")
        return 2

    rows = _rest("download_log", params={
        "serial_hash": f"eq.{serial_hash}",
        "limit": "1",
    })
    if not rows:
        print(f"Nema reda u download_log za serial_hash={serial_hash}")
        return 3
    row = rows[0]

    print("=" * 70)
    print(f"REPLAY UPUTE za serial_hash {serial_hash[:16]}...")
    print("=" * 70)
    print(f"  doc_type:               {row.get('doc_type')}")
    print(f"  doc_subtype:            {row.get('doc_subtype')}")
    print(f"  generated_at:           {row.get('generated_at')}")
    print(f"  plan_at_download:       {row.get('plan_at_download')}")
    print(f"  input_canonical_hash:   {row.get('input_canonical_hash')}")
    print(f"  output_sha256:          {row.get('output_sha256')}")
    print(f"  parent_hash:            {row.get('parent_hash')}")
    print(f"  current_hash:           {row.get('current_hash')}")
    print(f"  generator_version_hash: {row.get('generator_version_hash')}")
    print(f"  input_schema_version:   {row.get('input_schema_version')}")
    print()

    g_hash = row.get("generator_version_hash")
    if not g_hash:
        print("UPOZORENJE: red nema generator_version_hash (vjerojatno pre-K1 red).")
        return 4

    found = _find_generator_by_hash(g_hash)
    if not found:
        reg_path_msg = (
            f"Provjeri starije verzije generators_registry.json ili git log "
            f"za commit s hashom {g_hash[:16]}..."
        )
        print(f"Generator s hash-em {g_hash} nije u trenutnom registry-u.")
        print(reg_path_msg)
        return 5

    gen_name, gen_info = found
    print("Pronaden generator:")
    print(f"  ime:    {gen_name}")
    print(f"  modul:  {gen_info.get('module')}")
    print(f"  hash:   {gen_info.get('hash')}")
    print()

    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    git_commit = reg.get("git_commit", "unknown")

    print("KORACI ZA REPLAY:")
    print(f"  1. git checkout {git_commit}")
    print(f"  2. Ucitaj originalni input dict (korisnik mora dostaviti)")
    print(f"     - audit_chain.canonical_input_hash(input) MORA dati:")
    print(f"       {row.get('input_canonical_hash')}")
    print(f"  3. Pozovi generator iz {gen_info.get('module')}")
    print(f"  4. Pretvori HTML u docx kroz docx_export.html_u_docx(...)")
    print(f"  5. hashlib.sha256(docx_bytes).hexdigest() MORA dati:")
    print(f"     {row.get('output_sha256')}")
    print(f"  6. Ako oba hash-a match-aju → autenticnost potvrdjena.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
