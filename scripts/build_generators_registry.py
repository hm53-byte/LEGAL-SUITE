"""K1 Dan 4: skenira generatori/*.py, izracuna SHA256 nad source bytes, pise
generators_registry.json u root projekta. Pokrenuti pre-deploy (CI/CD ili lokalno
prije git push-a) tako da je registry u repu konzistentan s commit-om.

Usage: python -m scripts.build_generators_registry
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from audit_chain import compute_generator_hash  # noqa: E402

GENERATORI_DIR = ROOT / "generatori"
OUT_PATH = ROOT / "generators_registry.json"


def _git_commit() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
        return out
    except Exception:
        return "unknown"


def main() -> int:
    if not GENERATORI_DIR.exists():
        print(f"Folder ne postoji: {GENERATORI_DIR}")
        return 1

    git_commit = _git_commit()
    generators: dict[str, dict[str, str]] = {}

    for py_file in sorted(GENERATORI_DIR.glob("*.py")):
        if py_file.name.startswith("_"):
            continue
        rel = py_file.relative_to(ROOT).as_posix()
        h = compute_generator_hash(py_file)
        generators[py_file.stem] = {
            "module": rel,
            "hash": h,
        }

    registry = {
        "version": "v1",
        "git_commit": git_commit,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generators": generators,
    }

    OUT_PATH.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"OK: {len(generators)} generatora -> {OUT_PATH}")
    print(f"Git commit: {git_commit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
