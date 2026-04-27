-- =============================================================================
-- LegalTechSuite Pro — Supabase Postgres schema (K3, 2026-04-27)
-- =============================================================================
-- Copy-paste ovo u Supabase Dashboard → SQL Editor → New query → Run.
-- Idempotent (CREATE TABLE IF NOT EXISTS); siguran ponovni run.
--
-- Što radi:
--   1) Migrira `.users.json` (lokalni file, ephemeral na Streamlit Cloud) na Postgres
--   2) Dodaje `entitlements` (plan, period_end, status) — driver za K3 monetizaciju
--   3) Dodaje `download_log` (per-doc serial → user_id forenzički audit)
--   4) Dodaje `stripe_events` (idempotency anchor za webhook handler)
--   5) Row-Level Security (RLS): user vidi samo svoje retke (Supabase pattern)
--
-- BRZ_MOZAK reference (Pravilo 24):
--   - Stripe Webhooks Idempotency: stripe.com/docs/webhooks#handle-duplicate-events
--   - Supabase RLS: supabase.com/docs/guides/database/postgres/row-level-security
--   - GDPR Art 5(1)(c): data minimization — DB drži samo metadata, ne sadrzaj docx-a

-- =============================================================================
-- 1) USERS — zamjena za .users.json
-- =============================================================================

CREATE TABLE IF NOT EXISTS users (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    email               TEXT            NOT NULL UNIQUE,
    password_hash       TEXT,                                       -- PBKDF2-SHA256 'salt$hex'; NULL za OAuth-only
    oauth_provider      TEXT,                                       -- 'google','apple', NULL za email/lozinka
    oauth_subject       TEXT,                                       -- provider-side user id
    stripe_customer_id  TEXT            UNIQUE,                     -- popuni se na prvi checkout
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    last_login_at       TIMESTAMPTZ,
    UNIQUE(oauth_provider, oauth_subject)
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_stripe_customer ON users(stripe_customer_id);

-- =============================================================================
-- 2) ENTITLEMENTS — driver za K3 monetizaciju
-- =============================================================================
-- plan='free' je default (svaki user dobije besplatan tier pri registraciji).
-- plan='pro' aktivira se kad Stripe webhook UPSERTa nakon checkout.session.completed.
-- period_end = NULL za free (perpetual), datum za pro (subscription period).
-- status:
--   'active'  — entitlement vrijedi
--   'past_due'— Stripe naplata fail-ala, grace period 24h prije revoke
--   'revoked' — refund/dispute → manualan ili webhook revoke

CREATE TABLE IF NOT EXISTS entitlements (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID            NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan                TEXT            NOT NULL DEFAULT 'free',    -- 'free','pro'
    status              TEXT            NOT NULL DEFAULT 'active',  -- 'active','past_due','revoked'
    period_start        TIMESTAMPTZ,                                 -- NULL za free
    period_end          TIMESTAMPTZ,                                 -- NULL za free, datum za pro
    stripe_subscription_id TEXT         UNIQUE,                      -- Stripe sub_xxx
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    UNIQUE(user_id, plan)                                            -- jedan red po (user, plan)
);

CREATE INDEX IF NOT EXISTS idx_entitlements_user ON entitlements(user_id, status);
CREATE INDEX IF NOT EXISTS idx_entitlements_period ON entitlements(period_end) WHERE status = 'active';

-- =============================================================================
-- 3) DOWNLOAD_LOG — per-doc serial forenzicki trail
-- =============================================================================
-- Spaja generirani docx s user_id-em preko per-doc serial broja koji je utisnut
-- u (a) visible footer "ID: NN-NNN-NNN", (b) invisible XML metadata dc:identifier.
-- Ako se piratska kopija pojavi: serial_hash → user_id.
--
-- Data minimization (GDPR Art 5(1)(c)): NE pohranjuje sadrzaj docx-a, samo
-- (kategorija, generator naziv, timestamp, serial). Retencija 24 mjeseca.

CREATE TABLE IF NOT EXISTS download_log (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID            NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    doc_type            TEXT            NOT NULL,                   -- 'tuzba','ovrha','opomena',...
    doc_subtype         TEXT,                                       -- generator naziv unutar tipa, npr. 'kupoprodajni_ugovor'
    serial_hash         TEXT            NOT NULL,                   -- sha256(user_id+doc_type+ts+nonce)[:12]
    plan_at_download    TEXT            NOT NULL,                   -- 'free','pro' (da znamo koji watermark)
    generated_at        TIMESTAMPTZ     NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_download_log_serial ON download_log(serial_hash);
CREATE INDEX IF NOT EXISTS idx_download_log_user_ts ON download_log(user_id, generated_at);

-- =============================================================================
-- 4) STRIPE_EVENTS — idempotency anchor za webhook handler
-- =============================================================================
-- Stripe može poslati isti event >1 puta (network retry). Bez UNIQUE-a, svaki
-- retry bi UPSERTat entitlement. UNIQUE(stripe_event_id) garantira da se isti
-- event obradi samo jednom (NAPAD #2 pobijanje).

CREATE TABLE IF NOT EXISTS stripe_events (
    stripe_event_id     TEXT            PRIMARY KEY,
    event_type          TEXT            NOT NULL,                   -- 'checkout.session.completed', 'charge.refunded', ...
    received_at         TIMESTAMPTZ     NOT NULL DEFAULT now(),
    processed_at        TIMESTAMPTZ,                                -- NULL = u tijeku; vrijednost = obraden
    payload_json        JSONB                                       -- raw event za debug (Stripe API >= 2024-08 sluzbeno preporuca pohranu)
);

CREATE INDEX IF NOT EXISTS idx_stripe_events_unprocessed
    ON stripe_events(received_at)
    WHERE processed_at IS NULL;

-- =============================================================================
-- 5) ROW-LEVEL SECURITY (RLS) — Supabase pattern
-- =============================================================================
-- User mora vidjeti SAMO svoje retke. Streamlit klijent koristi Supabase JWT s
-- claim `sub = users.id`. RLS policy-i implementiraju "user vidi svoje".

ALTER TABLE users           ENABLE ROW LEVEL SECURITY;
ALTER TABLE entitlements    ENABLE ROW LEVEL SECURITY;
ALTER TABLE download_log    ENABLE ROW LEVEL SECURITY;
-- stripe_events NEMA RLS — pristup samo service_role (webhook handler), nikad client.

-- Drop ako postoje (idempotent re-run)
DROP POLICY IF EXISTS users_self_select       ON users;
DROP POLICY IF EXISTS users_self_update       ON users;
DROP POLICY IF EXISTS entitlements_self_read  ON entitlements;
DROP POLICY IF EXISTS download_log_self_read  ON download_log;
DROP POLICY IF EXISTS download_log_self_insert ON download_log;

-- Users: vidi/uredi samo svoj red
CREATE POLICY users_self_select ON users
    FOR SELECT USING (id = auth.uid());
CREATE POLICY users_self_update ON users
    FOR UPDATE USING (id = auth.uid());

-- Entitlements: vidi samo svoje (NIKAD ne uređuje s klijenta — samo webhook preko service_role)
CREATE POLICY entitlements_self_read ON entitlements
    FOR SELECT USING (user_id = auth.uid());

-- Download log: vidi svoje + insertira svoje
CREATE POLICY download_log_self_read ON download_log
    FOR SELECT USING (user_id = auth.uid());
CREATE POLICY download_log_self_insert ON download_log
    FOR INSERT WITH CHECK (user_id = auth.uid());

-- =============================================================================
-- Smoke seed (samo za dev — ukloni u produkciji)
-- =============================================================================
-- INSERT INTO users (email, password_hash) VALUES
--   ('test@example.com', '<pbkdf2_hash>')
-- ON CONFLICT (email) DO NOTHING;
