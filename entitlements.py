# =============================================================================
# entitlements.py — K3 monetizacija (cloud-native, 24/7 stack)
# =============================================================================
# Cita/upravlja entitlement state preko Supabase REST API (PostgREST).
# NIKAD ne pisi entitlements direktno s klijenta — to radi Cloudflare Worker
# (cloud/cf_worker_polar.ts) preko Polar.sh webhook-a + service_role kljuca.
#
# Payment gateway: Polar.sh (Merchant of Record). Polar automatski rjesava EU
# PDV za sve jurisdikcije bez registracije po zemlji.
#
# Streamlit klijent ima samo:
#   - SUPABASE_URL  (public, OK u secrets.toml)
#   - SUPABASE_ANON_KEY  (public, RLS stiti retke; OK u secrets.toml)
#   - CHECKOUT_URL_BASE  (CF Worker base URL — public, samo endpoint adresa)
#   - JWT u session_state["_supabase_jwt"] nakon auth (Supabase auth.signIn)
#
# Cloudflare Worker ima:
#   - SUPABASE_SERVICE_ROLE_KEY  (secret, NIKAD u Streamlit-u — bypass-a RLS)
#   - POLAR_WEBHOOK_SECRET, POLAR_ACCESS_TOKEN, POLAR_PRODUCT_ID_PRO
#
# BRZ_MOZAK reference:
#   - Pravilo 14B (tehnoloska sprancara): Supabase je infra-vendor (Postgres + auth + REST),
#     ne no-code platforma; integracija preko HTTP REST je transparentna i auditable.
#   - Pravilo 36 (ROI): TTL cache 30s reducira REST trosak ~95% (1 ping per 30s vs per render).
#   - Pravilo 38 (anti-business drift): NEMA segment names, pricing, TAM u kodu — samo
#     mehanika "user_id -> plan -> bool".

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

import requests
import streamlit as st


# =============================================================================
# Konfiguracija (citana iz Streamlit secrets ili env)
# =============================================================================

def _secret(key: str, default: str = "") -> str:
    """Citaj iz st.secrets ako postoji, inace iz env. Ne baca exception ako nedostaje
    — vraca default (npr. prazan string). Pozivatelj odluci je li prisutan."""
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.environ.get(key, default)


SUPABASE_URL = _secret("SUPABASE_URL")           # https://xxx.supabase.co
SUPABASE_ANON_KEY = _secret("SUPABASE_ANON_KEY") # public anon key (RLS-protected)
# Payment-gateway-neutral: Streamlit klijent vidi samo CF Worker base URL.
# Aktivni gateway iza Worker-a: Polar.sh (od 2026-04-28). Backward-compat:
# ako stari secret STRIPE_CHECKOUT_URL_BASE postoji, koristimo ga kao fallback.
CHECKOUT_URL_BASE = _secret("CHECKOUT_URL_BASE") or _secret("STRIPE_CHECKOUT_URL_BASE")


def _is_configured() -> bool:
    """True ako Supabase secrets postoje. False u dev mode-u (npr. lokalan run bez secrets.toml)."""
    return bool(SUPABASE_URL) and bool(SUPABASE_ANON_KEY)


# =============================================================================
# TTL cache za REST pozive (Pravilo 36: ROI cache hit rate)
# =============================================================================

_TTL_SECONDS = 30
_cache: dict[str, tuple[float, Any]] = {}


def _cache_get(key: str) -> Any | None:
    if key not in _cache:
        return None
    ts, val = _cache[key]
    if time.time() - ts > _TTL_SECONDS:
        del _cache[key]
        return None
    return val


def _cache_set(key: str, value: Any) -> None:
    _cache[key] = (time.time(), value)


def invalidate_cache(user_id: str | None = None) -> None:
    """Pozovi nakon uspjesnog Stripe checkout-a ili manualnog refresh-a."""
    if user_id is None:
        _cache.clear()
    else:
        for k in list(_cache.keys()):
            if user_id in k:
                del _cache[k]


# =============================================================================
# Supabase REST helper
# =============================================================================

def _rest(path: str, params: dict | None = None, jwt: str | None = None) -> list[dict]:
    """GET na PostgREST endpoint. Vraca prazna lista ako nije konfigurirano ili HTTP fail.
    Pozivatelj je odgovoran za graceful degradation — npr. tretiraj kao 'free' tier ako fails.
    """
    if not _is_configured():
        return []
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {jwt or SUPABASE_ANON_KEY}",
        "Accept": "application/json",
    }
    try:
        r = requests.get(url, headers=headers, params=params or {}, timeout=5.0)
        if r.status_code != 200:
            return []
        data = r.json()
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _rest_post(path: str, payload: dict, jwt: str | None = None) -> bool:
    """POST u PostgREST tablicu (insert). Vraca True ako 201."""
    if not _is_configured():
        return False
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {jwt or SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=5.0)
        return r.status_code in (200, 201, 204)
    except Exception:
        return False


# =============================================================================
# Public API
# =============================================================================

@dataclass(frozen=True)
class Entitlement:
    user_id: str
    plan: str            # 'free','pro'
    status: str          # 'active','past_due','revoked'
    period_end_iso: str | None  # ISO datum ili None za free


def current_user_id() -> str | None:
    """Cita user_id iz st.session_state (postavlja ga auth.py nakon login-a).
    Vraca None za guest/unauthenticated."""
    return st.session_state.get("_user_id")


def current_jwt() -> str | None:
    """Supabase JWT za RLS-aware queries (vidi samo svoje retke)."""
    return st.session_state.get("_supabase_jwt")


def get_entitlement(user_id: str | None = None) -> Entitlement:
    """Vraca trenutni entitlement za user-a. Default 'free/active' ako nije
    konfigurirano ili user nepoznat — graceful degradation (legacy app radi).
    """
    user_id = user_id or current_user_id()
    if not user_id:
        return Entitlement(user_id="", plan="free", status="active", period_end_iso=None)
    cache_key = f"ent::{user_id}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached
    rows = _rest(
        "entitlements",
        params={
            "user_id": f"eq.{user_id}",
            "status": "eq.active",
            "order": "plan.desc",  # 'pro' > 'free' alphabetical
            "limit": "1",
        },
        jwt=current_jwt(),
    )
    if rows:
        r = rows[0]
        ent = Entitlement(
            user_id=user_id,
            plan=r.get("plan", "free"),
            status=r.get("status", "active"),
            period_end_iso=r.get("period_end"),
        )
    else:
        ent = Entitlement(user_id=user_id, plan="free", status="active", period_end_iso=None)
    _cache_set(cache_key, ent)
    return ent


def is_pro(user_id: str | None = None) -> bool:
    """True ako user ima active 'pro' entitlement. Glavni gate za UNLIMITED downloads /
    invisible serial / cleaner watermark."""
    ent = get_entitlement(user_id)
    return ent.plan == "pro" and ent.status == "active"


def get_checkout_url(user_id: str | None = None, plan: str = "pro") -> str | None:
    """Vraca payment Checkout URL za upgrade (Polar.sh hosted checkout).
    Pravi POST na CF Worker (`/create-checkout-session`) koji generira Polar
    Checkout session s metadata={user_id, plan}. CF Worker vraca URL.

    Vraca None ako nije konfigurirano ili user_id nedostaje (UI ce sakriti gumb).
    """
    user_id = user_id or current_user_id()
    if not user_id or not CHECKOUT_URL_BASE:
        return None
    try:
        r = requests.post(
            f"{CHECKOUT_URL_BASE}/create-checkout-session",
            json={"user_id": user_id, "plan": plan},
            timeout=10.0,
        )
        if r.status_code == 200:
            return r.json().get("checkout_url")
    except Exception:
        pass
    return None


def record_download(
    doc_type: str,
    doc_subtype: str,
    serial_hash: str,
    plan: str,
    user_id: str | None = None,
    audit: dict[str, Any] | None = None,
) -> bool:
    """Upisuje download_log red. Pozovi iz prikazi_dokument() / docx_export.
    Tihi fail — ako Supabase ne odgovara, generiranje docx-a se ne smije blokirati.

    K1 audit chain: ako je `audit` dict proslijeden, dodaju se polja
    input_canonical_hash, output_sha256, parent_hash, current_hash,
    generator_version_hash, input_schema_version (vidi audit_chain.compute_full_audit).
    """
    user_id = user_id or current_user_id()
    if not user_id or not _is_configured():
        return False
    payload = {
        "user_id": user_id,
        "doc_type": doc_type,
        "doc_subtype": doc_subtype,
        "serial_hash": serial_hash,
        "plan_at_download": plan,
    }
    if audit:
        payload.update({
            "input_canonical_hash": audit.get("input_canonical_hash"),
            "output_sha256": audit.get("output_sha256"),
            "parent_hash": audit.get("parent_hash"),
            "current_hash": audit.get("current_hash"),
            "generator_version_hash": audit.get("generator_version_hash"),
            "input_schema_version": audit.get("input_schema_version", "v1"),
        })
    return _rest_post("download_log", payload, jwt=current_jwt())


def get_last_chain_hash(user_id: str | None = None) -> str | None:
    """K1: dohvati current_hash zadnjeg download_log reda (parent_hash za novi red).
    Vraca None za prvi red u lancu (genesis) ili kad Supabase nije konfiguriran."""
    user_id = user_id or current_user_id()
    if not user_id or not _is_configured():
        return None
    rows = _rest(
        "download_log",
        params={
            "user_id": f"eq.{user_id}",
            "current_hash": "not.is.null",
            "order": "generated_at.desc",
            "limit": "1",
            "select": "current_hash",
        },
        jwt=current_jwt(),
    )
    return rows[0].get("current_hash") if rows else None


# =============================================================================
# Streamlit UI helper — gumb za pretplatu
# =============================================================================

def render_subscribe_cta(label: str = "Pretplati se na PRO", key: str = "_pro_cta") -> None:
    """Prikazuje "Pretplati se" gumb ako user nije PRO. Klik -> Stripe Checkout.
    No-op ako je vec PRO ili nije konfigurirano."""
    if not _is_configured():
        return
    user_id = current_user_id()
    if not user_id:
        return
    if is_pro(user_id):
        return
    if st.button(label, key=key, type="primary"):
        url = get_checkout_url(user_id, plan="pro")
        if url:
            st.markdown(f"[Otvori Polar Checkout]({url})")
            st.info("Nakon uspjesne pretplate, vrati se u app i kliknite refresh.")
        else:
            st.error("Trenutno nije moguce pokrenuti pretplatu. Pokusajte kasnije.")
