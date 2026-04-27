"""Tests za K1 audit_chain — RFC 8785 JCS canonical hash, generator hash, chain verify."""
import hashlib
from pathlib import Path

import pytest


def test_canonical_form_is_deterministic():
    import audit_chain as ac
    d = {"b": 2, "a": 1, "c": [3, 1, 2]}
    assert ac.canonical_input_hash(d) == ac.canonical_input_hash(d)


def test_canonical_form_key_order_invariant():
    """Sortirani kljucevi → identican hash bez obzira na input redoslijed."""
    import audit_chain as ac
    a = {"x": 1, "y": 2, "z": 3}
    b = {"z": 3, "y": 2, "x": 1}
    assert ac.canonical_input_hash(a) == ac.canonical_input_hash(b)


def test_canonical_form_handles_unicode_nfc():
    """HR diakritike normalizirane (NFC) → predvidiv hash."""
    import audit_chain as ac
    d_nfc = {"naziv": "Čakovec"}      # č kao NFC
    d_nfd = {"naziv": "Čakovec"}     # C + combining caron (NFD)
    assert ac.canonical_input_hash(d_nfc) == ac.canonical_input_hash(d_nfd)


def test_canonical_form_changes_on_value_diff():
    import audit_chain as ac
    a = ac.canonical_input_hash({"k": "v1"})
    b = ac.canonical_input_hash({"k": "v2"})
    assert a != b


def test_canonical_form_returns_64_hex_chars():
    import audit_chain as ac
    h = ac.canonical_input_hash({"a": 1})
    assert len(h) == 64
    assert all(c in "0123456789abcdef" for c in h)


def test_compute_generator_hash_is_idempotent(tmp_path):
    import audit_chain as ac
    f = tmp_path / "gen.py"
    f.write_text("def x(): return 1\n", encoding="utf-8")
    h1 = ac.compute_generator_hash(f)
    h2 = ac.compute_generator_hash(f)
    assert h1 == h2


def test_compute_generator_hash_changes_on_source_diff(tmp_path):
    import audit_chain as ac
    f1 = tmp_path / "g1.py"
    f2 = tmp_path / "g2.py"
    f1.write_text("def x(): return 1\n", encoding="utf-8")
    f2.write_text("def x(): return 2\n", encoding="utf-8")
    assert ac.compute_generator_hash(f1) != ac.compute_generator_hash(f2)


def test_build_chain_link_changes_on_any_field():
    import audit_chain as ac
    base = {
        "input_hash": "a" * 64,
        "output_hash": "b" * 64,
        "generator_hash": "c" * 64,
        "parent_hash": "d" * 64,
    }
    h_base = ac.build_chain_link(**base)
    for field in base:
        mut = dict(base)
        mut[field] = "f" * 64
        assert ac.build_chain_link(**mut) != h_base


def test_build_chain_link_genesis_with_no_parent():
    """parent_hash=None za prvi red → ne pada, vraca valjan hash."""
    import audit_chain as ac
    h = ac.build_chain_link(
        input_hash="a" * 64,
        output_hash="b" * 64,
        generator_hash="c" * 64,
        parent_hash=None,
    )
    assert len(h) == 64


def test_verify_chain_pass_on_valid_sequence():
    import audit_chain as ac
    rows = []
    parent = None
    for i in range(3):
        in_h = f"{'a'*60}{i:04d}"
        out_h = f"{'b'*60}{i:04d}"
        gen_h = "c" * 64
        cur = ac.build_chain_link(in_h, out_h, gen_h, parent)
        rows.append({
            "input_canonical_hash": in_h,
            "output_sha256": out_h,
            "generator_version_hash": gen_h,
            "parent_hash": parent,
            "current_hash": cur,
            "input_schema_version": "v1",
        })
        parent = cur
    ok, idx = ac.verify_chain(rows)
    assert ok is True
    assert idx is None


def test_verify_chain_detects_single_row_mutation():
    import audit_chain as ac
    rows = []
    parent = None
    for i in range(3):
        in_h = f"{'a'*60}{i:04d}"
        out_h = f"{'b'*60}{i:04d}"
        gen_h = "c" * 64
        cur = ac.build_chain_link(in_h, out_h, gen_h, parent)
        rows.append({
            "input_canonical_hash": in_h,
            "output_sha256": out_h,
            "generator_version_hash": gen_h,
            "parent_hash": parent,
            "current_hash": cur,
            "input_schema_version": "v1",
        })
        parent = cur
    rows[1]["output_sha256"] = "f" * 64
    ok, idx = ac.verify_chain(rows)
    assert ok is False
    assert idx == 1


def test_compute_full_audit_returns_all_fields(tmp_path):
    import audit_chain as ac
    f = tmp_path / "g.py"
    f.write_text("def x(): return 1\n", encoding="utf-8")
    res = ac.compute_full_audit(
        input_dict={"a": 1, "b": 2},
        output_bytes=b"docx-content",
        generator_module_path=f,
        parent_hash=None,
    )
    for k in ("input_canonical_hash", "output_sha256", "generator_version_hash",
              "parent_hash", "current_hash", "input_schema_version"):
        assert k in res
    assert res["input_schema_version"] == "v1"
    assert res["parent_hash"] is None
    assert len(res["current_hash"]) == 64


def test_compute_full_audit_chain_consistency(tmp_path):
    """Output current_hash mora se moci verify-ati u novoj generaciji kao parent."""
    import audit_chain as ac
    f = tmp_path / "g.py"
    f.write_text("def x(): return 1\n", encoding="utf-8")
    a1 = ac.compute_full_audit({"i": 1}, b"out1", f, None)
    a2 = ac.compute_full_audit({"i": 2}, b"out2", f, a1["current_hash"])
    rows = [
        {
            "input_canonical_hash": a1["input_canonical_hash"],
            "output_sha256": a1["output_sha256"],
            "generator_version_hash": a1["generator_version_hash"],
            "parent_hash": a1["parent_hash"],
            "current_hash": a1["current_hash"],
            "input_schema_version": "v1",
        },
        {
            "input_canonical_hash": a2["input_canonical_hash"],
            "output_sha256": a2["output_sha256"],
            "generator_version_hash": a2["generator_version_hash"],
            "parent_hash": a2["parent_hash"],
            "current_hash": a2["current_hash"],
            "input_schema_version": "v1",
        },
    ]
    ok, idx = ac.verify_chain(rows)
    assert ok is True


def test_canonical_form_handles_empty_dict():
    import audit_chain as ac
    h = ac.canonical_input_hash({})
    assert len(h) == 64


def test_canonical_form_separators_no_whitespace():
    """JSON dump koristi separators=(',',':') — bez razmaka."""
    import audit_chain as ac, json, unicodedata
    d = {"a": 1, "b": "txt"}
    canonical = json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    canonical = unicodedata.normalize("NFC", canonical)
    expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert ac.canonical_input_hash(d) == expected
    assert " " not in canonical
