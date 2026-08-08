-- =============================================================================
-- 0008_retencija_download_log.sql
-- Retencija download_loga: 24 mjeseca, zatim anonimizacija u mjestu.
-- =============================================================================
-- Apliciraj u Supabase Dashboard -> SQL Editor -> New query -> Run,
-- nakon 0006 (supabase_schema.sql) i 0007 (0007_audit_chain.sql).
-- Cijela skripta je idempotentna i ne pada ako je tablica prazna.
--
-- ODLUKA: stari se redak NE brise, nego se prazni. Ostaju samo tri polja:
--   generated_at, parent_hash, current_hash.
-- Sve ostalo (user_id, doc_type, doc_subtype, serial_hash, plan_at_download,
-- input_canonical_hash, output_sha256, generator_version_hash,
-- input_schema_version) postavlja se na NULL. Takav ostatak zovemo nadgrobni
-- redak.
--
-- ZASTO ne brisanje cijelog retka: parent_hash sljedecega retka pokazuje na
-- current_hash prethodnoga. Ako se prethodni redak fizicki ukloni, veza vodi u
-- prazno i provjera lanca vraca neuspjeh koji izgleda jednako kao krivotvorina.
-- Kod retencije po datumu rezanje ide s najstarije strane, dakle upravo one
-- koja lomi lanac. Nadgrobni redak cuva current_hash pa veza ostaje cjelovita.
--
-- ZASTO se brisu i input_canonical_hash i output_sha256, iako nisu ocit osobni
-- podatak: to su SHA-256 sazetci sadrzaja koji ukljucuje ime, OIB i adresu
-- stranke. Sazetak je pseudonimizacija, ne anonimizacija (GDPR cl. 4 t. 5,
-- uvodna izjava 26). Ako bi ostali, obecani rok cuvanja ne bi bio ispostovan.
-- current_hash je sazetak nad sazetcima i bez ta tri ulazna polja se ne moze
-- ponovno izracunati, pa vise ne opisuje sadrzaj nego samo poziciju u lancu.
--
-- POSLJEDICA ZA PROVJERU: nadgrobni redak se ne moze provjeriti sam za sebe,
-- on je samo nosac veze. Provjeru radi audit_chain.verify_chain_retention_aware,
-- koja nadgrobni redak prepoznaje po anonymized_at IS NOT NULL i ne pokusava mu
-- prerecunati hes. Stara audit_chain.verify_chain ovo ne zna i na nadgrobnom
-- retku javlja neuspjeh; ostavljena je nepromijenjena zbog zatecenih poziva.

-- =============================================================================
-- 1) Nova kolona: oznaka da je redak anonimiziran
-- =============================================================================
-- anonymized_at je istovremeno oznaka stanja i dokaz da je posao radio
-- (GDPR cl. 5 st. 2, pouzdanost). NULL znaci zivi redak.

ALTER TABLE download_log
    ADD COLUMN IF NOT EXISTS anonymized_at TIMESTAMPTZ;

COMMENT ON COLUMN download_log.anonymized_at IS
    'NULL = zivi redak. Vrijednost = trenutak anonimizacije po retenciji; '
    'redak tada nosi samo generated_at, parent_hash i current_hash.';

-- =============================================================================
-- 2) Skidanje NOT NULL s kolona koje se prazne
-- =============================================================================
-- Bez ovoga se anonimizacija ne moze izvesti. Da praznjenje ne bi postalo
-- rupa kroz koju prolaze neispravni novi upisi, u koraku 3 dolazi CHECK koji
-- dopusta samo dva oblika retka: potpuno popunjen zivi ili potpuno ispraznjen
-- nadgrobni.

ALTER TABLE download_log ALTER COLUMN user_id          DROP NOT NULL;
ALTER TABLE download_log ALTER COLUMN doc_type         DROP NOT NULL;
ALTER TABLE download_log ALTER COLUMN serial_hash      DROP NOT NULL;
ALTER TABLE download_log ALTER COLUMN plan_at_download DROP NOT NULL;

-- =============================================================================
-- 3) CHECK: redak je ili zivi ili nadgrobni, treceg oblika nema
-- =============================================================================
-- DROP pa ADD jer Postgres nema ADD CONSTRAINT IF NOT EXISTS. Na praznoj
-- tablici prolazi bez posla; na punoj tablici zateceni redci zadovoljavaju
-- prvu granu jer su im sve cetiri kolone bile NOT NULL.

ALTER TABLE download_log
    DROP CONSTRAINT IF EXISTS download_log_zivi_ili_nadgrobni;

ALTER TABLE download_log
    ADD CONSTRAINT download_log_zivi_ili_nadgrobni CHECK (
        (
            anonymized_at IS NULL
            AND user_id          IS NOT NULL
            AND doc_type         IS NOT NULL
            AND serial_hash      IS NOT NULL
            AND plan_at_download IS NOT NULL
        )
        OR
        (
            anonymized_at IS NOT NULL
            AND user_id                IS NULL
            AND doc_type               IS NULL
            AND doc_subtype            IS NULL
            AND serial_hash            IS NULL
            AND plan_at_download       IS NULL
            AND input_canonical_hash   IS NULL
            AND output_sha256          IS NULL
            AND generator_version_hash IS NULL
            AND input_schema_version   IS NULL
        )
    );

-- Posao trazi najstarije jos neanonimizirane retke; djelomicni indeks se s
-- vremenom smanjuje jer anonimizirani redci ispadaju iz njega.
CREATE INDEX IF NOT EXISTS idx_download_log_retencija
    ON download_log(generated_at)
    WHERE anonymized_at IS NULL;

-- =============================================================================
-- 4) Funkcija koja provodi pravilo
-- =============================================================================
-- Vraca broj obradjenih redaka. Ponovno pokretanje ne radi nista jer uvjet
-- anonymized_at IS NULL vise ne vrijedi za vec obradjene retke.
--
-- Granica je ukljuciva: redak star tocno p_mjeseci se anonimizira. Obecani rok
-- je gornja granica cuvanja, pa se dvojba rjesava u korist ranijeg brisanja
-- (GDPR cl. 5 st. 1 t. (e)).
--
-- make_interval(months => p_mjeseci) racuna kalendarski, uz podrezivanje dana
-- na zadnji dan mjeseca. Pricuvna skripta u Pythonu radi isti racun.
--
-- IZNIMKA OD PRAVILA "RANIJE": redak od 29.02.2024. ne uhvati se 28.02.2026.,
-- jer podrezivanje daje granicu 28.02.2024., nego tek 01.03.2026. Dakle 731
-- dan umjesto 730. To je jedini dan u cetiri godine kad se rok probija umjesto
-- da se skrati, i posljedica je toga sto se granica racuna oduzimanjem od now()
-- umjesto zbrajanjem na generated_at. Zbrajanje bi dalo 28.02.2026., ali onda
-- uvjet ne bi mogao koristiti indeks idx_download_log_retencija i posao bi
-- citao cijelu tablicu. Jedan dan na 730 kod 1 od 1461 retka ne opravdava tu
-- cijenu; ako AZOP zatrazi strogo tumacenje, promijeni uvjet u
--   generated_at + make_interval(months => p_mjeseci) <= now()
-- i racunaj sa sekvencijalnim citanjem.
--
-- VREMENSKA ZONA: Postgres racuna `timestamptz - interval` s mjesecima u
-- lokalnom vremenu sesije (TimeZone GUC), a pricuvna skripta racuna u UTC-u.
-- Supabaseov zadani TimeZone je UTC, pa se poklapaju. Kod roka koji je
-- visekratnik 12 mjeseci razlike nema ni u zoni s ljetnim racunanjem vremena,
-- jer su obje tocke iste godisnje dobe; kod roka od 6 ili 18 mjeseci u zoni
-- tipa Europe/Zagreb granice se razilaze za sat vremena. Provjeri s
-- `SHOW TimeZone;` prije nego rok promijenis na broj koji nije visekratnik 12.

CREATE OR REPLACE FUNCTION download_log_anonimiziraj(p_mjeseci integer DEFAULT 24)
RETURNS integer
LANGUAGE plpgsql
AS $fn$
DECLARE
    v_granica timestamptz;
    v_broj    integer;
BEGIN
    IF p_mjeseci IS NULL OR p_mjeseci < 1 THEN
        RAISE EXCEPTION 'p_mjeseci mora biti cijeli broj >= 1 (dobiveno: %)', p_mjeseci;
    END IF;

    v_granica := now() - make_interval(months => p_mjeseci);

    UPDATE download_log
       SET user_id                = NULL,
           doc_type               = NULL,
           doc_subtype            = NULL,
           serial_hash            = NULL,
           plan_at_download       = NULL,
           input_canonical_hash   = NULL,
           output_sha256          = NULL,
           generator_version_hash = NULL,
           input_schema_version   = NULL,
           anonymized_at          = now()
     WHERE anonymized_at IS NULL
       AND generated_at  <= v_granica;

    GET DIAGNOSTICS v_broj = ROW_COUNT;
    RETURN v_broj;
END
$fn$;

COMMENT ON FUNCTION download_log_anonimiziraj(integer) IS
    'Retencija download_loga: prazni osobne stupce redaka starijih od '
    'p_mjeseci, cuva generated_at, parent_hash i current_hash radi lanca. '
    'Idempotentna; vraca broj obradjenih redaka.';

-- Brisanje racuna po GDPR cl. 17 ide kroz isti put, da CASCADE ne odnese
-- retke zajedno s vezom u lancu. Pozovi ovo PRIJE brisanja retka iz users.
CREATE OR REPLACE FUNCTION download_log_anonimiziraj_korisnika(p_user_id uuid)
RETURNS integer
LANGUAGE plpgsql
AS $fn$
DECLARE
    v_broj integer;
BEGIN
    IF p_user_id IS NULL THEN
        RAISE EXCEPTION 'p_user_id ne smije biti NULL';
    END IF;

    UPDATE download_log
       SET user_id                = NULL,
           doc_type               = NULL,
           doc_subtype            = NULL,
           serial_hash            = NULL,
           plan_at_download       = NULL,
           input_canonical_hash   = NULL,
           output_sha256          = NULL,
           generator_version_hash = NULL,
           input_schema_version   = NULL,
           anonymized_at          = now()
     WHERE anonymized_at IS NULL
       AND user_id = p_user_id;

    GET DIAGNOSTICS v_broj = ROW_COUNT;
    RETURN v_broj;
END
$fn$;

COMMENT ON FUNCTION download_log_anonimiziraj_korisnika(uuid) IS
    'GDPR cl. 17: prazni sve retke jednog korisnika bez obzira na starost. '
    'Pozovi prije DELETE FROM users, inace ON DELETE CASCADE ukloni retke '
    'zajedno s vezama u lancu.';

-- =============================================================================
-- 5) Prava: obicni klijent ne smije pokretati posao
-- =============================================================================
-- download_log ima RLS bez politike za UPDATE i DELETE, pa anon i authenticated
-- ionako ne mogu mijenjati retke. Ovo je druga brava: bez EXECUTE ne mogu ni
-- pozvati funkciju preko PostgREST RPC-a. Uloge se provjeravaju jer u lokalnom
-- Postgresu bez Supabasea ne postoje.

DO $prava$
BEGIN
    REVOKE ALL ON FUNCTION download_log_anonimiziraj(integer) FROM PUBLIC;
    REVOKE ALL ON FUNCTION download_log_anonimiziraj_korisnika(uuid) FROM PUBLIC;

    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
        REVOKE ALL ON FUNCTION download_log_anonimiziraj(integer) FROM anon;
        REVOKE ALL ON FUNCTION download_log_anonimiziraj_korisnika(uuid) FROM anon;
    END IF;

    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated') THEN
        REVOKE ALL ON FUNCTION download_log_anonimiziraj(integer) FROM authenticated;
        REVOKE ALL ON FUNCTION download_log_anonimiziraj_korisnika(uuid) FROM authenticated;
    END IF;
END
$prava$;

-- =============================================================================
-- 6) pg_cron raspored
-- =============================================================================
-- Posao ide jednom dnevno u 03:17 UTC. Neokrugla minuta smanjuje sudar s
-- ostalim poslovima koje ljudi tipicno stavljaju na punu uru.
--
-- Cijeli blok je u EXCEPTION omotu: ako pg_cron nije ukljucen ili trenutna
-- uloga nema prava na shemu cron, migracija ispise obavijest i nastavi, umjesto
-- da padne. U tom slucaju koristi pricuvnu skriptu
-- scripts/retencija_download_log.py.
--
-- RAISE NOTICE NIJE DOVOLJAN. Supabaseov SQL Editor ne prikazuje pouzdano
-- poruke razine NOTICE; migracija tada zavrsi s "Success. No rows returned" i
-- vlasnik nema nacin vidjeti da raspored nije postavljen. Zato korak 7 na kraju
-- ove datoteke vraca redak s ishodom, koji se u mrezi rezultata uvijek vidi.
-- Bez toga bi jedini korak koji tvrdnju iz politike privatnosti cini istinitom
-- mogao tiho izostati.
--
-- pg_cron se u Supabaseu ukljucuje u Dashboard -> Database -> Extensions
-- (trazi "pg_cron"), ili ovdje sljedecim retkom ako uloga to smije:
--     CREATE EXTENSION IF NOT EXISTS pg_cron;

DO $raspored$
DECLARE
    v_naziv text := 'download_log_retencija';
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_cron') THEN
        RAISE NOTICE
            'pg_cron nije ukljucen. Raspored nije postavljen. Ukljuci ekstenziju '
            'pa ponovno pokreni ovu skriptu, ili koristi '
            'scripts/retencija_download_log.py.';
        PERFORM set_config(
            'legalsuite.raspored',
            'NEMA: pg_cron nije ukljucen. Dashboard -> Database -> Extensions -> '
            'pg_cron, pa ovu skriptu ponovno; ili koristi '
            'scripts/retencija_download_log.py.',
            false
        );
        RETURN;
    END IF;

    -- Odjava prije prijave: cron.schedule po imenu radi upsert tek od pg_cron
    -- 1.4, a ovako je ponovno pokretanje sigurno i na starijima.
    PERFORM cron.unschedule(jobid) FROM cron.job WHERE jobname = v_naziv;

    PERFORM cron.schedule(
        v_naziv,
        '17 3 * * *',
        $posao$SELECT download_log_anonimiziraj(24);$posao$
    );

    RAISE NOTICE 'pg_cron posao "%" postavljen na 03:17 UTC svaki dan.', v_naziv;
    PERFORM set_config(
        'legalsuite.raspored',
        'POSTAVLJEN: pg_cron posao "' || v_naziv || '", svaki dan u 03:17 UTC. '
        'Potvrdi to sutradan upitom nad cron.job_run_details (korak 3 u '
        'docs/brisanje_podataka.md); postavljen raspored jos nije izvrsen posao.',
        false
    );
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE
        'Raspored nije postavljen (%). Ostatak migracije je primijenjen. '
        'Koristi scripts/retencija_download_log.py dok se ovo ne rijesi.',
        SQLERRM;
    PERFORM set_config(
        'legalsuite.raspored',
        'NEMA: ' || SQLERRM || '. Ostatak migracije je primijenjen; nedostaje '
        'samo raspored. Koristi scripts/retencija_download_log.py.',
        false
    );
END
$raspored$;

-- =============================================================================
-- 7) Ishod, u obliku koji se vidi u mrezi rezultata
-- =============================================================================
-- Zadnja naredba u datoteci namjerno je SELECT: SQL Editor prikaze redak i onda
-- kad NOTICE poruke iz koraka 6 ne prikaze. Procitaj stupac `raspored`.
--
-- Ishod se cita iz varijable sesije koju je postavio korak 6, a ne izravno iz
-- sheme cron: uloga koja nema prava na tu shemu dobila bi gresku, a greska u
-- zadnjoj naredbi bi u SQL Editoru, koji cijelu skriptu vrti u jednoj
-- transakciji, ponistila i sve prije nje. current_setting s drugim argumentom
-- true vraca NULL umjesto greske ako varijabla nije postavljena.

SELECT
    'download_log_anonimiziraj(24)'                                  AS funkcija,
    coalesce(
        current_setting('legalsuite.raspored', true),
        'NEPOZNATO: korak 6 nije dosao do kraja.'
    )                                                                AS raspored,
    (SELECT count(*) FROM download_log WHERE anonymized_at IS NULL)     AS zivi_redci,
    (SELECT count(*) FROM download_log WHERE anonymized_at IS NOT NULL) AS nadgrobni_redci;

-- =============================================================================
-- 8) Rucne provjere (odkomentiraj po potrebi)
-- =============================================================================
-- Stanje retencije:
--   SELECT count(*) FILTER (WHERE anonymized_at IS NULL)     AS zivi,
--          count(*) FILTER (WHERE anonymized_at IS NOT NULL) AS nadgrobni,
--          min(generated_at) FILTER (WHERE anonymized_at IS NULL) AS najstariji_zivi
--     FROM download_log;
--
-- Koliko bi posao obradio da se pokrene sada (bez pisanja):
--   SELECT count(*) FROM download_log
--    WHERE anonymized_at IS NULL
--      AND generated_at <= now() - make_interval(months => 24);
--
-- Rucno pokretanje:
--   SELECT download_log_anonimiziraj(24);
--
-- Zadnja izvrsavanja pg_cron posla:
--   SELECT status, return_message, start_time, end_time
--     FROM cron.job_run_details d
--     JOIN cron.job j ON j.jobid = d.jobid
--    WHERE j.jobname = 'download_log_retencija'
--    ORDER BY start_time DESC LIMIT 10;
