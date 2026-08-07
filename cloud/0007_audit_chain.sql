-- 0007_audit_chain.sql — K1 Janusov audit lanac
-- Idempotent ALTER (Postgres podržava IF NOT EXISTS na ADD COLUMN od v9.6+).
-- Apliciraj u Supabase Dashboard → SQL Editor nakon 0006 (supabase_schema.sql).

ALTER TABLE download_log ADD COLUMN IF NOT EXISTS input_canonical_hash    TEXT;
ALTER TABLE download_log ADD COLUMN IF NOT EXISTS output_sha256            TEXT;
ALTER TABLE download_log ADD COLUMN IF NOT EXISTS parent_hash              TEXT;
ALTER TABLE download_log ADD COLUMN IF NOT EXISTS current_hash             TEXT;
ALTER TABLE download_log ADD COLUMN IF NOT EXISTS generator_version_hash   TEXT;
ALTER TABLE download_log ADD COLUMN IF NOT EXISTS input_schema_version     TEXT DEFAULT 'v1';

CREATE INDEX IF NOT EXISTS idx_download_log_parent_hash  ON download_log(parent_hash);
CREATE INDEX IF NOT EXISTS idx_download_log_current_hash ON download_log(current_hash);

-- Postojeci redovi (od prije K1) imaju NULL u novim poljima — to je OK,
-- audit chain se gradi od trenutka aktivacije unaprijed. Stari redovi se
-- ne mogu replay-ati (input nije pohranjen po data minimization principu).
