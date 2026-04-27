"""Tests za K3 entitlements — graceful degradation kad Supabase nije konfiguriran,
TTL cache, fallback na 'free' plan."""
import time

import pytest


@pytest.fixture(autouse=True)
def reset_cache():
    """Pre-svaki test, isprazni in-memory cache da testovi ne dijele state."""
    import entitlements as ent
    ent.invalidate_cache()
    yield
    ent.invalidate_cache()


def test_get_entitlement_falls_back_to_free_when_no_user_id():
    """Bez user_id-a, vraca 'free/active' default — guest experience."""
    import entitlements as ent
    e = ent.get_entitlement(user_id=None)
    assert e.plan == "free"
    assert e.status == "active"
    assert e.user_id == ""


def test_get_entitlement_falls_back_when_supabase_unconfigured(monkeypatch):
    """Kad SUPABASE_URL nije postavljen, vraca 'free/active' (graceful)."""
    import entitlements as ent
    monkeypatch.setattr(ent, "SUPABASE_URL", "")
    monkeypatch.setattr(ent, "SUPABASE_ANON_KEY", "")
    e = ent.get_entitlement(user_id="some-user")
    assert e.plan == "free"
    assert e.status == "active"


def test_is_pro_returns_false_when_unconfigured():
    """is_pro graceful-degrade: bez Supabase, svi su free."""
    import entitlements as ent
    assert ent.is_pro(user_id="anyone") is False


def test_get_checkout_url_returns_none_when_unconfigured():
    """Bez STRIPE_CHECKOUT_URL_BASE, vraca None (UI sakrije gumb)."""
    import entitlements as ent
    assert ent.get_checkout_url(user_id="user-1") is None


def test_record_download_returns_false_when_unconfigured():
    """Tihi fail (vraca False) kad Supabase ne dohvatljiv."""
    import entitlements as ent
    ok = ent.record_download(
        doc_type="tuzba",
        doc_subtype="parnicna",
        serial_hash="abc123",
        plan="free",
        user_id="user-1",
    )
    assert ok is False


def test_ttl_cache_avoids_double_fetch(monkeypatch):
    """Drugi poziv unutar TTL prozora (30s) ne ide na Supabase."""
    import entitlements as ent
    call_count = {"n": 0}

    def fake_rest(path, params=None, jwt=None):
        call_count["n"] += 1
        return [{"plan": "pro", "status": "active", "period_end": "2027-01-01"}]

    monkeypatch.setattr(ent, "_rest", fake_rest)
    monkeypatch.setattr(ent, "_is_configured", lambda: True)
    e1 = ent.get_entitlement(user_id="u-cache-1")
    e2 = ent.get_entitlement(user_id="u-cache-1")
    assert e1.plan == "pro" and e2.plan == "pro"
    assert call_count["n"] == 1, "TTL cache nije sprijecio drugi pingu"


def test_ttl_cache_per_user_isolation(monkeypatch):
    """Cache je per-user_id; razliciti useri ne dijele red."""
    import entitlements as ent
    plans = {"u-a": "free", "u-b": "pro"}

    def fake_rest(path, params=None, jwt=None):
        # Izvuci user_id iz params['user_id']='eq.UUID'
        uid = params.get("user_id", "").replace("eq.", "")
        return [{"plan": plans.get(uid, "free"), "status": "active", "period_end": None}]

    monkeypatch.setattr(ent, "_rest", fake_rest)
    monkeypatch.setattr(ent, "_is_configured", lambda: True)
    a = ent.get_entitlement(user_id="u-a")
    b = ent.get_entitlement(user_id="u-b")
    assert a.plan == "free"
    assert b.plan == "pro"


def test_invalidate_cache_for_specific_user(monkeypatch):
    """invalidate_cache(user_id) skida samo taj user-ov red, ostali ostaju."""
    import entitlements as ent
    monkeypatch.setattr(ent, "_rest", lambda *a, **kw: [{"plan": "pro", "status": "active", "period_end": None}])
    monkeypatch.setattr(ent, "_is_configured", lambda: True)
    ent.get_entitlement(user_id="u-keep")
    ent.get_entitlement(user_id="u-evict")
    assert ent._cache_get("ent::u-keep") is not None
    assert ent._cache_get("ent::u-evict") is not None
    ent.invalidate_cache(user_id="u-evict")
    assert ent._cache_get("ent::u-keep") is not None
    assert ent._cache_get("ent::u-evict") is None
