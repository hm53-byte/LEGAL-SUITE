# Ideja: Hermesov sync outbox

**Status**: USPJEH 7/7 (UBOJICA 7/7 + SUDAC 7/7, delta 0)
**Datum**: 2026-04-27
**Source ciklus**: `CIKLUS_K2_2026-04-27.md`
**Pipeline modus**: P2 hibrid (Agent 2A FILOZOF + Agent 5 SUDAC odvojeni subagenti)
**Tip (Pravilo L1)**: B kompozicija (4 ortogonalna primitiva)
**Filozofski izvor**: KRISTAL 2 Hermes (granicar) + KRISTAL 3 Pascal (forsirana oklada) + KRISTAL 4 Turner (trofazni prag)

---

## Sažetak

Aplikacija postaje offline-capable kroz **client-side outbox sync s server-side audit chain link computation**. Korisnik radi u browser-u; kad mreža padne, forme se persistiraju u IndexedDB outbox-u; pri reconnect-u, sync_worker POST-a outbox payload-e na Cloudflare Worker `/api/sync` endpoint koji validira UNIQUE constraint na `client_event_id`, prosljeđuje na Streamlit za **deterministic generation**, i K1 audit chain link se računa na serveru u istoj transakciji.

**Ključna invariantna**: K1 hash chain ostaje cjelovit. Klijent NE računa parent_hash — server ga dohvati pri primanju iz aktualnog stanja.

## Inženjerska teza

Generacija docx-a ostaje 100% server-side (Python pure functions u `generatori/*.py`) jer port na JS bi razbio:
- Generator versioning hash (drugačiji bytecode = drugačiji `generator_version_hash`)
- Deterministic guarantee (suptilne razlike Python ↔ JS string handling)
- K1 reproducibility test (`git checkout <commit> && replay <serial>`)

Klijent-side sloj je čisto **infrastrukturni** (network interception + persistence + retry semantika), ne mijenja business logiku.

---

## Arhitektura — komponente

### Service Worker (`static/sw.js` ~120 LOC)

- **Cache-first** za `/static/*` (sw.js, idb_outbox.js, sync_worker.js, manifest.json, app shell HTML)
- **Network-first** za `/api/*` (uvijek fresh data od Supabase/CF Worker)
- **Offline fallback** za form submit: ako network fail → write IDB outbox, vraća offline-success status
- **Scope filter**: presreće samo `/static/*` i `/api/sync`; **NE presreće** `/_stcore/stream` (Streamlit WebSocket)
- **Versioning**: `cache_v<git_commit_sha>` — auto-cleanup starih cache-eva pri activate event

### IndexedDB (`static/idb_outbox.js` ~150 LOC)

3 object store-a:
1. `forms_drafts` — auto-save in-progress forms (key: page_module + timestamp)
2. `outbox_pending` — submitted forms čekaju sync (key: client_event_id UUID v4; payload: input_canonical + doc_type + generator_module_path + client_timestamp)
3. `documents_cached` — generirani docx za re-download (key: serial_hash; value: bytes)

### Sync worker (`static/sync_worker.js` ~80 LOC)

- Periodični poll `navigator.onLine` (event listener `online` + interval fallback 30s)
- Iz outbox FIFO order: POST `/api/sync` s payload-om
- **Exponential backoff** 1s → 2s → 4s → 8s → 16s (max 5 attempts)
- Error states: `pending` → `syncing` → `synced` (delete from IDB) ili `error_4xx`/`error_5xx`/`failed_max_retries`

### PWA manifest (`static/manifest.json` ~20 LOC)

- `name`: "LegalTechSuite Pro"
- `theme_color`: brand navy
- `start_url`: "/"
- ikona: 192x192 + 512x512 PNG
- `display`: "standalone" (instalable kao desktop app)

### Cloudflare Worker `/api/sync` (`cloud/cf_worker_sync.ts` ~180 LOC)

```
POST /api/sync
Body: {client_event_id, input_canonical, doc_type, generator_module_path, client_timestamp, user_jwt}

1. Validate JWT (Supabase token)
2. SELECT FROM client_outbox_events WHERE client_event_id = ? -- idempotency check
   IF row exists → return cached response (status 200, audit_chain_link iz row-a)
3. ELSE:
   a. INSERT INTO client_outbox_events (client_event_id, user_id, payload, received_at) -- UNIQUE catch ako concurrent
   b. Forward (input_canonical, doc_type, generator_module_path) Streamlit /_stcore/api endpoint
      ILI direktno pozvati Python generator preko Supabase Edge Function (alternativa)
   c. Receive docx_bytes + audit_payload (parent_hash dohvati u entitlements.get_last_chain_hash)
   d. INSERT INTO download_log (audit fields + client_event_id reference)
   e. UPDATE client_outbox_events SET processed_at = NOW(), result = JSON
   f. Return {audit_link, serial_hash}
```

### Supabase tablica (`cloud/0008_outbox_events.sql` ~25 LOC)

```sql
CREATE TABLE IF NOT EXISTS client_outbox_events (
    client_event_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    payload JSONB NOT NULL,
    received_at TIMESTAMPTZ DEFAULT NOW(),
    processed_at TIMESTAMPTZ,
    result JSONB,
    error_count INT DEFAULT 0,
    last_error TEXT
);

CREATE INDEX IF NOT EXISTS idx_outbox_user_received ON client_outbox_events(user_id, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_outbox_unprocessed ON client_outbox_events(received_at) WHERE processed_at IS NULL;

ALTER TABLE download_log ADD COLUMN IF NOT EXISTS client_event_id UUID REFERENCES client_outbox_events(client_event_id);
```

### Streamlit integracija (`LEGAL-SUITE.py` +25 LOC)

```python
import streamlit.components.v1 as components

def _registriraj_sw():
    """Inject Service Worker registracija u browser."""
    if not os.getenv("OFFLINE_MODE_ENABLED", "false") == "true":
        return
    components.html("""
    <script>
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js').catch(console.error);
    }
    </script>
    <link rel="manifest" href="/static/manifest.json">
    """, height=0)

# Pozvati u main()
```

### `pomocne.py` proširenje (+15 LOC)

`_prikazi_offline_save_button(input_dict, doc_type, modul)` — opcijski gumb prikazan kad `navigator.onLine === false` (preko JS feature detection); poziv u `prikazi_dokument` ako SW dostupan.

### `entitlements.py` proširenje (+10 LOC)

`record_download(client_event_id=None)` — opcijski parametar; ako proslijeđen, upiše u `download_log.client_event_id` polje (FK na outbox).

---

## ROI metrike (Pravilo L4)

| # | Metrika | Prije | Poslije | Anchor |
|---|---|---|---|---|
| 1 | Offline kontinuitet rada | 0% | 100% za 30d drafts | W3C Service Workers Spec |
| 2 | Server cost reduction (return users s ≥3 visit/tjedan) | 100% requests hit | ≥40% reduction | Google Web.dev "Offline Cookbook" |
| 3 | Audit chain integritet pod offline | N/A | 100% server-side computed | RFC 8785 JCS + audit_chain.compute_full_audit |
| 4 | MTTR za browser crash recovery | 100% rework | <5s iz IDB | MDN IDB transactions |

**Kohort definitor (per SUDAC REFRAKTOR signal #1)**: Metrika #2 mjeri se na sub-kohorti "return users s ≥3 visit/tjedan kroz zadnja 4 tjedna". Initial baseline placeholder dok se ne implementira Lighthouse audit u CI (signal #5 — measurement instrumentacija preko sw.js → analytics endpoint).

---

## SUDAC follow-up signali integrirani u implementaciju

1. **Metrika #2 kohort suženje**: u dokumentaciji za marketing ROI samo "≥40% za return ≥3 visit/tjedan", ne raspon 40-60% (potonji je placeholder).
2. **test_sync_outbox.py race condition**: dodati eksplicitan test case "two concurrent POST /api/sync s istim client_event_id" → očekuj UNIQUE constraint hit, 2. POST vraća prvotni response.
3. **Manual flush admin role + GDPR audit**: `entitlements.is_admin(user_id)` provjera; flush event upisuje u `audit_chain.flush_log` tablicu (novi minor primitive); GDPR Art 17 compliance.
4. **SW cache versioning sha**: koristit **git commit sha** (predvidljivije od content sha — manje chatty re-deploy-i); dohvati preko `gh.event.commit.sha` u GitHub Action ili lokalnog `git rev-parse HEAD`; injektira se u sw.js kao `const CACHE_VERSION = "<sha>"` template-replace pri build-u.
5. **Cache hit ratio instrumentacija**: sw.js šalje `postMessage({type: 'cache_hit', url, strategy})` na main thread; main thread agregira (last 100 events) u sessionStorage; periodic POST na `/api/analytics/sw_metrics` (free tier Cloudflare Analytics ili custom Supabase tablica `sw_metrics`).

---

## PhD-tehnička pitanja (Pravilo 16)

1. **Distribution shift (browser kvote)**: feature detection + `navigator.storage.estimate()` warning ako kvota < 100MB; graceful fallback to no-offline mod.
2. **Calibration (cache strategija)**: per-asset; static cache-first (target >70% hit), API network-first (<5% stale); measurement signal #5.
3. **Causal vs correlational**: čisto kauzal — deterministic FSM; bez ML.
4. **Failure mode taxonomy**: 5 modova s eksplicitnim handling-om (timeout, mid-flight close, 4xx, 5xx, concurrent device).

---

## 5 NAPADA + pobijanja (Pravilo 6)

Vidi `CIKLUS_K2_2026-04-27.md:Korak 2B`. Sva 5 napada pobijena, 1 akceptiran rizik (NAPAD #4 SW lifecycle edge cases prvih 1-2 mj — Lighthouse + manual QA mitigacija).

---

## Anti-AI izjava (Pravilo L6)

Ovaj kandidat ne uvodi: AI inferenciju, klasifikator, prediktivni model, generative AI sloj, recommender, personalizaciju. Sve je deterministic JS/HTTP/SQL primitive: Service Worker presretanje (W3C spec), IndexedDB transakcije (W3C spec), UUID v4 generacija (`crypto.randomUUID()`), HTTP POST s JSON payload-om, server-side UNIQUE constraint za idempotency. Ne aktivira AI Act Article 3(1) "AI system" definiciju. Ne pruža pravne savjete. Ne klasificira korisnikov slučaj. Ne predlaže content. **Generacija docx-a ostaje 100% server-side u postojećim Python pure-function generatorima** — generator_version_hash i K1 audit chain integritet nepromijenjeni.

---

## Reference (Pravilo 24)

(a) **AKADEMSKA / RFC**:
- W3C Service Workers Specification (Russell, Song et al., latest 2024)
- W3C Indexed Database API 3.0 Working Draft (2024)
- RFC 4122 (Leach, Mealling, Salz 2005) — UUID specification (v4 random)
- RFC 8785 (Rundgren, Jordan, Erdtman 2020) — JSON Canonicalization (preduvjet za K1; klijent serijalizira u istu formu)

(b) **VENDOR**:
- Google Web.dev "Offline Cookbook" (Russell 2014, ažurirano 2024)
- Stripe Idempotency Keys Documentation
- Cloudflare Workers Cron Triggers (free tier — opcijski reconciliation)

(c) **REGULATORNA / KRIPTOGRAFSKA**:
- GDPR Art 25 (Privacy by design) — IDB outbox kao opt-in lokalna pohrana
- GDPR Art 17 (Right to erasure) — manual flush outbox audit log obavezan
- W3C Web Crypto API spec (faza 2 dodatak za AES-GCM enkripciju IDB entries)
- OWASP Cryptographic Storage Cheat Sheet (PBKDF2-SHA256 ključ derivacija)

---

## LOC realnost (Pravilo 27)

- `static/sw.js` — 120
- `static/idb_outbox.js` — 150
- `static/sync_worker.js` — 80
- `static/manifest.json` — 20
- `LEGAL-SUITE.py` proširenje — +25
- `pomocne.py` proširenje — +15
- `cloud/cf_worker_sync.ts` — 180
- `cloud/0008_outbox_events.sql` — 25
- `entitlements.py` proširenje — +10
- `tests/test_sync_outbox.py` — 120

**Total**: 545 src + 120 test = **665 LOC**
**Formula**: 545/75 + 120/50 + 2 = 7.27 + 2.4 + 2 = **11.7 dana solo dev rok**

---

## Patch summary (Pravilo 23 commit-able)

| File | Status | LOC | Što |
|---|---|---|---|
| `static/sw.js` | NOVI | +120 | Service Worker (cache-first static, network-first API, offline fallback) |
| `static/idb_outbox.js` | NOVI | +150 | IDB wrapper s 3 object stores |
| `static/sync_worker.js` | NOVI | +80 | Periodic sync, exponential backoff |
| `static/manifest.json` | NOVI | +20 | PWA manifest |
| `LEGAL-SUITE.py` | proširen | +25 | SW registracija kroz st.components.v1.html |
| `pomocne.py` | proširen | +15 | `_prikazi_offline_save_button()` |
| `cloud/cf_worker_sync.ts` | NOVI | +180 | POST /api/sync, UNIQUE check, audit chain link computation |
| `cloud/0008_outbox_events.sql` | NOVI | +25 | client_outbox_events tablica + indexes |
| `entitlements.py` | proširen | +10 | `record_download(client_event_id=None)` |
| `tests/test_sync_outbox.py` | NOVI | +120 | FSM transitions, idempotency, race condition, mocked IDB |

---

## Rollback plan

- **Feature flag**: `OFFLINE_MODE_ENABLED` env var u Streamlit secrets; `False` → SW se ne registrira; aplikacija radi 100% online (postojeće ponašanje)
- **Idempotent migration**: `cloud/0008_outbox_events.sql` koristi `CREATE TABLE IF NOT EXISTS` + `CREATE UNIQUE INDEX IF NOT EXISTS`; siguran ponovni run
- **Graceful degradation**: feature detection `'serviceWorker' in navigator`; legacy IE radi normalno bez offline featurea
- **SW uninstall**: u slučaju kritičnog bug-a, korisnici mogu force-uninstall preko `chrome://serviceworker-internals` ili automatski preko `sw.js?unregister=1` query param koji unregister-a sebe
- **Manual flush outbox**: admin-only gumb (entitlements.is_admin); flush event upisuje u `audit_chain.flush_log` tablicu (GDPR Art 17 compliance)

---

## Sljedeći logički korak nakon K2 implementacije

**K4 — Generator versioning registry proširenje**: dodati `schema_in` i `schema_out` JSON Schema polja u `generators_registry.json` (postoji od K1). Per generator validacija forme prije server-side generation. Daje JSON Schema test za client-side validaciju u `static/idb_outbox.js` prije save-a u outbox.

---

## Status

**PROMOTE-an za implementaciju** — orkestrator (korisnik) odlučuje kada (vjerojatno nakon Streamlit Cloud + Supabase + CF Worker setup-a koji je preduvjet za K3/K1 testiranje na production).

**Implementacijski preduvjeti**:
1. K3 setup završen (Supabase + Stripe + Cloudflare deploy) — bez toga nema serverless `/api/sync` endpoint
2. K1 audit chain implementiran (već JEST) — `audit_chain.compute_full_audit` mora biti pozvan server-side iz CF Worker-a
3. Streamlit Cloud `OFFLINE_MODE_ENABLED=true` env var aktiviran (ili default false dok se ne testira)
