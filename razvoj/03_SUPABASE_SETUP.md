# 03 — POSTAVLJANJE SUPABASE (BAZA + PRIJAVA KORISNIKA)

> Ovaj korak je **praktičan** — sjedneš za računalo i napraviš sve do kraja. Vrijeme: 30-45 minuta.
>
> Ako nisi nikad koristio bazu podataka — bez brige, sve ide kroz web sučelje. Nema instalacija na računalu.

---

## 1. ŠTO JE SUPABASE (10-sekundno objašnjenje)

Zamisli **gotov backend u oblaku**:
- Pravu bazu podataka (PostgreSQL, ozbiljnu, koju koriste banke)
- Sustav prijave korisnika (email/lozinka, Google, Facebook, Apple — sve gotovo)
- Mali server-bez-servera za webhookove (Edge Functions)
- Sve administrirano kroz lijepi web UI

**Free tier:** dovoljan za prvih ~50.000 korisnika mjesečno. Pravi pravcati free, bez kreditne kartice za početak.

---

## 2. KORAK PO KORAK

### 2.1 Otvaranje računa

1. Idi na **https://supabase.com**
2. Klikni **"Start your project"** (gornji desni kut)
3. **Sign up with GitHub** je najlakše (ili email)
4. Potvrdi email

### 2.2 Kreiranje projekta

1. Klikni **"New project"**
2. **Organization:** ostavi tvoj default (ili kreiraj novu, npr. "LegalTech")
3. **Project name:** `legaltech-suite-pro`
4. **Database password:** **ovo je važno** — generiraj random lozinku **i spremi je u password manager**. Ovo je root pristup bazi, ne smiješ je izgubiti niti dijeliti. (Možeš resetirati kasnije ako trebaš, ali bolje da je čuvaš.)
5. **Region: Frankfurt (eu-central-1)** — najbliže Hrvatskoj, najbrže za tvoje korisnike
6. **Pricing plan:** Free
7. Klikni **"Create new project"**

Pričekaj 2-3 minute dok se baza pripremi.

### 2.3 Dohvaćanje API ključeva (sad, da ne zaboraviš)

Kad projekt bude spreman:

1. Lijevo dolje klikni **gear ikonu** (Settings)
2. **API** tab
3. Vidjet ćeš:
   - **Project URL** — npr. `https://abcdefghijkl.supabase.co`
   - **API Keys** s dva ključa:
     - **anon (public)** — sigurno za frontend, daje se klijentskoj aplikaciji
     - **service_role (secret)** — **NIKAD** ne ide u frontend, samo na server. Ima full pristup.

**Otvori prazan `notes.txt` lokalno i kopiraj sve troje.** Trebat će za `.streamlit/secrets.toml`.

⚠️ **service_role ključ je kao master ključ.** Ako ga netko dobije, ima pristup cijeloj bazi. Ne commitaj ga na GitHub. Ne dijeli ga. Ne lijepi ga u Slack/Discord. Samo u Edge Function secrets i secrets.toml na privatnom Streamlit Cloudu.

---

## 3. KREIRANJE TABLICA (DATABASE SCHEMA)

Sad napraviš strukturu baze. Sve odjednom, kopiraš SQL i pokreneš.

### 3.1 Otvaranje SQL editora

1. Lijevo izborniku → **SQL Editor** (ikona `>_`)
2. Klikni **"New query"**
3. Otvorit će se prazni tekstualni editor

### 3.2 SQL koji kopiraš i pokreneš

Cijeli ovaj blok zalijepi u SQL editor i klikni **"Run"** (ili Ctrl+Enter):

```sql
-- ======================================================================
-- LegalTech Suite Pro — Database Schema
-- Kreira tablice: profiles, subscriptions, usage_log
-- Postavlja Row-Level Security (RLS) — kritično za sigurnost!
-- ======================================================================

-- ----------------------------------------------------------------------
-- 1) PROFILES — proširenje auth.users s našim podacima
-- ----------------------------------------------------------------------
-- Napomena: Supabase već ima auth.users tablicu (kreirana automatski)
--          Mi dodajemo profiles s dodatnim poljima (free trial brojač)
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  free_documents_used INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE public.profiles IS 'Korisnički profili — proširenje auth.users';
COMMENT ON COLUMN public.profiles.free_documents_used IS 'Brojač iskorištenih besplatnih dokumenata';

-- ----------------------------------------------------------------------
-- 2) SUBSCRIPTIONS — sinkronizirano iz Lemon Squeezy webhooka
-- ----------------------------------------------------------------------
CREATE TABLE public.subscriptions (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  ls_subscription_id TEXT UNIQUE,        -- Lemon Squeezy interni ID
  ls_customer_id TEXT,                   -- Lemon Squeezy customer ID
  variant_id TEXT,                       -- weekly/monthly/yearly
  status TEXT NOT NULL,                  -- active, paused, cancelled, expired, on_trial, past_due
  renews_at TIMESTAMPTZ,                 -- kad se sljedeći put naplaćuje
  ends_at TIMESTAMPTZ,                   -- ako je otkazano, do kad vrijedi
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_subs_user ON public.subscriptions(user_id);
CREATE INDEX idx_subs_status ON public.subscriptions(status);

COMMENT ON TABLE public.subscriptions IS 'Pretplate sinkronizirane iz Lemon Squeezy';

-- ----------------------------------------------------------------------
-- 3) USAGE_LOG — audit log svake generacije dokumenta
-- ----------------------------------------------------------------------
-- Korisno za: GDPR (dokaz tko je što radio), analytics, abuse detection
CREATE TABLE public.usage_log (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  document_type TEXT NOT NULL,           -- npr. 'tuzba_novcana', 'ovrha_jb'
  was_paid BOOLEAN NOT NULL,             -- true ako iz pretplate, false ako besplatni
  ip_hash TEXT,                          -- SHA256 hash IP-a (GDPR friendly, ne sprema sirov IP)
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_log_user_time ON public.usage_log(user_id, created_at DESC);
CREATE INDEX idx_log_doc_type ON public.usage_log(document_type);

COMMENT ON TABLE public.usage_log IS 'Audit log generacija dokumenata';

-- ----------------------------------------------------------------------
-- 4) ROW-LEVEL SECURITY (RLS) — KRITIČNO!
-- ----------------------------------------------------------------------
-- Bez RLS, ANYONE s anon key-om može čitati sve tablice!
-- RLS osigurava da svaki user vidi SAMO svoje podatke.

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.usage_log ENABLE ROW LEVEL SECURITY;

-- Profile: korisnik može SELECT i UPDATE samo svoj profil
CREATE POLICY profile_select_self ON public.profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY profile_update_self ON public.profiles
  FOR UPDATE USING (auth.uid() = id) WITH CHECK (auth.uid() = id);

-- Subscriptions: korisnik može SELECT samo svoje pretplate (insert/update radi service_role iz Edge Function)
CREATE POLICY sub_select_self ON public.subscriptions
  FOR SELECT USING (auth.uid() = user_id);

-- Usage log: korisnik može INSERT vlastiti zapis i SELECT vlastite zapise
CREATE POLICY log_insert_self ON public.usage_log
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY log_select_self ON public.usage_log
  FOR SELECT USING (auth.uid() = user_id);

-- ----------------------------------------------------------------------
-- 5) TRIGGER — auto-kreiranje profila kod registracije
-- ----------------------------------------------------------------------
-- Kad god se kreira novi auth.users zapis (registracija),
-- automatski se kreira odgovarajući profiles zapis.
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1))
  );
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();

-- ----------------------------------------------------------------------
-- 6) HELPER FUNKCIJA — provjeri ima li user aktivnu pretplatu
-- ----------------------------------------------------------------------
-- Koristi se iz Python koda (preko RPC-a) ili iz drugih SQL upita
CREATE OR REPLACE FUNCTION public.has_active_subscription(uid UUID)
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.subscriptions
    WHERE user_id = uid
      AND status IN ('active', 'on_trial', 'past_due')
      AND (ends_at IS NULL OR ends_at > now())
  );
$$;

-- ======================================================================
-- KRAJ SCHEMA — pokreni 'Run' i provjeri da nema grešaka
-- ======================================================================
```

### 3.3 Provjera

Kad pokreneš Run, vidjet ćeš dolje "Success. No rows returned." To je dobro.

Sad lijevo:
1. **Table Editor** (ikona tablice)
2. Vidiš tri tablice: `profiles`, `subscriptions`, `usage_log`
3. Sve prazne. To je super.

---

## 4. POSTAVLJANJE EMAIL AUTENTIKACIJE

### 4.1 Osnovne postavke

1. Lijevo izborniku → **Authentication** (ikona ključa)
2. **Providers** tab
3. **Email** je već uključen po defaultu — to je dobro
4. Klikni na njega da otvoriš opcije:
   - **Enable email confirmations** — preporučujem **ON** (smanjuje fake registracije)
   - **Secure email change** — ON
   - **Confirm email change** — ON
5. Spremi (Save)

### 4.2 Email templates (opcionalno za sad)

Lijevo → **Authentication** → **Email Templates** — tu možeš urediti email koji korisnik dobije za potvrdu registracije, reset lozinke itd. Možeš to ostaviti za kasnije, default je OK.

### 4.3 SMTP postavke (NEMOJ za sad mijenjati)

Supabase ima vlastiti SMTP server koji šalje 4 emaila/sat besplatno. Za testiranje to je dovoljno. Kad budeš stvarno krenuo s korisnicima → poveži vlastiti SMTP (Resend.com je free do 3.000 mailova/mj, super za to).

---

## 5. POSTAVLJANJE GOOGLE OAUTH (OPCIONALNO ALI PREPORUČENO)

Korisnici puno radije kliknu "Prijava preko Googlea" nego da pamte novu lozinku.

### 5.1 Google Cloud setup

1. Idi na **https://console.cloud.google.com**
2. Klikni **"New Project"** → naziv: `legaltech-suite` → Create
3. Lijevo izbornik → **APIs & Services** → **OAuth consent screen**
4. **External** → Create
5. Popuni:
   - App name: **LegalTech Suite Pro**
   - User support email: tvoj email
   - Developer contact: tvoj email
6. Save and Continue
7. **Scopes** → Add scopes → odaberi **email** i **profile** (osnovne)
8. Continue → na "Test users" preskočiš → Save

### 5.2 Kreiranje OAuth credentials

1. Lijevo → **APIs & Services** → **Credentials**
2. **Create Credentials** → **OAuth Client ID**
3. **Application type:** Web application
4. **Name:** Supabase OAuth
5. **Authorized redirect URIs:** dodaj URL koji ti Supabase da:
   - Vrati se u Supabase → **Authentication** → **Providers** → **Google**
   - Tu vidiš "Callback URL (for OAuth)" — npr. `https://abcdef.supabase.co/auth/v1/callback`
   - Kopiraj taj URL i zalijepi u Google "Authorized redirect URIs"
6. Create
7. Pojavi se modal s **Client ID** i **Client Secret** — kopiraj oboje

### 5.3 Spajanje s Supabaseom

1. Vrati se u Supabase → **Authentication** → **Providers** → **Google**
2. Toggle **Enable Sign in with Google** ON
3. Zalijepi **Client ID** i **Client Secret**
4. Save

### 5.4 Provjera

Možeš testirati: idi na **Authentication** → **Users** → **Add user** → trebao bi vidjeti "Magic link" i "Google" kao opcije.

---

## 6. PROVJERA DA SVE RADI

### 6.1 Ručno dodaj test korisnika

1. **Authentication** → **Users** → **Add user** → **Create new user**
2. Email: `test@example.com`, Password: `Test1234!`
3. Kreiraj

### 6.2 Provjeri da je trigger radio

1. **Table Editor** → **profiles**
2. Trebao bi vidjeti red s `email = test@example.com` i `free_documents_used = 0`
3. Ako vidiš → trigger radi savršeno

Ako ne vidiš → trigger nije pokrenut, ponovo pokreni SQL od bloka `CREATE OR REPLACE FUNCTION` nadalje.

---

## 7. ZAPISI ZA `secrets.toml`

U svoj `notes.txt` napiši:

```
SUPABASE_URL = "https://<TVOJ_ID>.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGc..."         (anon key, public)
SUPABASE_SERVICE_KEY = "eyJhbGc..."      (service_role, SECRET — samo za webhook)
```

Ove ćeš kasnije zalijepiti u `.streamlit/secrets.toml` (vidi `09_LANSIRANJE.md`).

---

## 8. ŠTO SI UPRAVO POSTIGAO

✅ Imaš pravu PostgreSQL bazu u oblaku, besplatno
✅ Imaš sustav prijave email/lozinka (i Google ako si htio)
✅ Imaš tablice za profile, pretplate i audit log
✅ Imaš Row-Level Security — niti jedan korisnik ne može vidjeti tuđe podatke
✅ Imaš automatski trigger koji kreira profil pri registraciji
✅ Imaš helper funkciju `has_active_subscription()` za brze provjere

**Sve ovo košta tebe 0 EUR i radit će za prvih 50.000 korisnika.**

---

## TIPIČNI PROBLEMI

**"SQL je javio grešku 'relation auth.users does not exist'"**
→ Pokrenuo si SQL na pogrešnom projektu ili prije nego što je projekt bio do kraja inicijaliziran. Pričekaj minutu, pokušaj ponovo.

**"Trigger ne radi (profil se ne kreira)"**
→ Provjeri u **Database** → **Triggers** da li `on_auth_user_created` postoji. Ako ne, ponovo pokreni dio SQL-a od `CREATE OR REPLACE FUNCTION` do `EXECUTE FUNCTION ...`.

**"Google OAuth javlja 'redirect_uri_mismatch'"**
→ Pogrešan callback URL u Google Cloud Console. Mora biti **točno** isti kao onaj u Supabase. Includa `https://`, port (ako postoji), i završava s `/auth/v1/callback`.

**"Mogu li imati više okruženja (dev, staging, prod)?"**
→ Da, kreiraj odvojene Supabase projekte. Free plan dopušta do 2 projekta, plaćeni više. Za sad — jedan projekt je OK.

**"Što ako želim vidjeti sve registrirane korisnike?"**
→ Authentication → Users. Ili SQL Editor: `SELECT * FROM auth.users;`

**"Mogu li ručno dati nekome pretplatu (npr. prijatelju, beta testeru)?"**
→ Da, SQL Editor:
```sql
INSERT INTO public.subscriptions (user_id, status, ends_at)
VALUES ('<uuid-korisnika>', 'active', '2027-01-01');
```
UUID korisnika nađeš u Authentication → Users → klikneš → kopiraš ID.

**"Strašno mi je dijelti SQL svoju bazu — što ako greška?"**
→ Supabase ima **Database Backups** (Settings → Database → Backups). Free plan = dnevni backup automatski. Možeš restore-ati ako pretukneš nešto. Ne brini.

---

## SLJEDEĆI KORAK

Otvori `04_LEMON_SQUEEZY_SETUP.md` i postavi naplatu. Tek nakon toga ide kod.
