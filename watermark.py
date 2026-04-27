# =============================================================================
# watermark.py — K3 per-doc forensic watermark (2026-04-27)
# =============================================================================
# Generira deterministicki serial broj za svaki download i utiskuje ga u docx.
#
# 2-tier pristup (NAPAD #1 pobijanje iz BRZ_MOZAK audita):
#   - **VISIBLE footer**: "Generirano iz LegalTechSuite Pro — ID: NN-NNN-NNN"
#     Korisnik moze ga ukloniti rucno (Word footer edit), ali defaultni docx ima
#     brand awareness + serial koji povezuje docx s user_id-em u download_log.
#   - **INVISIBLE XML metadata** (paid tier only): per-doc sha256 u
#     `dc:identifier` core property. Skriven od casual user-a, ali postoji u XML
#     i forensic alati ga vide. Ako se piratski docx pojavi, alati mogu izvuci
#     metadata -> serial -> user_id.
#
# Ovo NIJE robust DRM (svaki watermark moze se ukloniti ako korisnik zna XML).
# To je **forensic** watermark u smislu Petitcolas/Anderson/Kuhn 1999 IEEE 87(7) —
# cilj je dokaz autentičnosti, ne sprjecavanje kopiranja.
#
# Reference (Pravilo 24):
#   - Petitcolas, Anderson, Kuhn 1999 — "Information Hiding: A Survey", IEEE 87(7)
#   - Microsoft Office Open XML (ISO/IEC 29500) — dc:identifier u core.xml
#   - GDPR Art 5(1)(c) — data minimization: serial je sha256(user_id+...)[:12], ne plain user_id

from __future__ import annotations

import hashlib
import os
import secrets
from datetime import datetime, timezone
from typing import Any


# =============================================================================
# Serial generator
# =============================================================================

def _format_serial(raw_hex: str) -> str:
    """Prema sha256 hex prefix-u format-a: 'AB-CDEF-GHIJ' (12 chars + dashes).
    Lakse za citanje u footer-u, lakse za korisnika da kaze adminu kad reportira issue.
    """
    raw = raw_hex.upper()[:12]  # 12 hex chars
    return f"{raw[0:2]}-{raw[2:6]}-{raw[6:10]}{raw[10:12]}"


def generate_serial(
    user_id: str,
    doc_type: str,
    timestamp_iso: str | None = None,
    nonce: str | None = None,
) -> str:
    """Deterministicki serial broj. Isti input -> isti output (idempotent test-able).
    Ako nonce=None, generira random — sluzi za production gdje svaki download dobije unique serial.

    Format: 'AB-CDEF-GHIJ' (12 hex chars dashed, ~52 bita entropije).
    """
    ts = timestamp_iso or datetime.now(timezone.utc).isoformat(timespec="seconds")
    n = nonce if nonce is not None else secrets.token_hex(8)
    raw = f"{user_id}|{doc_type}|{ts}|{n}".encode("utf-8")
    h = hashlib.sha256(raw).hexdigest()
    return _format_serial(h)


def serial_hash(serial: str) -> str:
    """Kanonski hash serial broja za pohranu u download_log.serial_hash kolonu.
    Daje sha256(serial), 64 hex chars (puni; bez truncation jer je DB column TEXT).
    """
    return hashlib.sha256(serial.encode("utf-8")).hexdigest()


# =============================================================================
# Footer HTML (visible watermark, free tier)
# =============================================================================

def footer_html(serial: str, plan: str = "free") -> str:
    """Vraca HTML fragment za footer — koristi se u generatori/* preko docx_export-a.

    free: vidljiv brand + serial (uklonjivo, ali default)
    pro: vidljiv samo serial (cleaner UX, jer placeni klijenti nisu marketing kanal)
    """
    if plan == "pro":
        return (
            f"<div class='doc-watermark' style='font-size:0.65rem;color:#94a3b8;"
            f"text-align:center;margin-top:1.5rem;letter-spacing:0.04em;'>"
            f"ID: {serial}"
            f"</div>"
        )
    # free tier — brand + serial
    return (
        f"<div class='doc-watermark' style='font-size:0.65rem;color:#94a3b8;"
        f"text-align:center;margin-top:1.5rem;letter-spacing:0.04em;'>"
        f"Generirano iz LegalTechSuite Pro &nbsp;&middot;&nbsp; ID: {serial}"
        f"</div>"
    )


# =============================================================================
# python-docx core property setter (invisible XML metadata, pro tier)
# =============================================================================

def stamp_core_properties(doc: Any, serial: str, user_id: str = "") -> None:
    """Utiskuje serial u OOXML core.xml (dc:identifier).
    Forensic alati (npr. ExifTool, Microsoft Office "Document Properties") to vide.

    Doc je python-docx Document instance. Ako lib nije dostupan ili dokument
    nije DOCX, tihi no-op.

    NAPOMENA: samo `identifier` se postavlja. user_id NE pohranjujemo u XML —
    forensic chain ide preko `download_log.serial_hash → user_id` lookup-a u DB.
    Ovo je svjesna privacy-protection odluka (GDPR Art 5(1)(c) data minimization):
    docx u rukama trece strane otkriva serial, ne identitet korisnika.
    """
    try:
        cp = doc.core_properties
        cp.identifier = serial
    except Exception:
        # Ako doc nije python-docx Document ili lib problem, ne padaj
        pass


# =============================================================================
# Convenience: jedan-poziv API koji se koristi u docx_export.py
# =============================================================================

def apply_watermark(
    doc: Any,
    user_id: str,
    doc_type: str,
    plan: str = "free",
) -> tuple[str, str]:
    """Generira serial + utiskuje invisible XML metadata. Vraca (serial, serial_hash).

    Pozivatelj (docx_export.py) treba:
      1) Pozvati ovo PRIJE save-a docx-a
      2) Dodati footer_html(serial, plan) u rendered HTML
      3) Pozvati entitlements.record_download(doc_type, doc_subtype, serial_hash, plan, user_id)

    Sva tri koraka su izolacijska — ako bilo koji fails, ostatak app-a radi (no DRM,
    ali docx generation je glavni use case).
    """
    serial = generate_serial(user_id=user_id or "guest", doc_type=doc_type)
    stamp_core_properties(doc, serial, user_id=user_id)
    return serial, serial_hash(serial)
