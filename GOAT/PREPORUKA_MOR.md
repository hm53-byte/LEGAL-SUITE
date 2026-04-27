# Preporuka: Polar.sh kao Merchant of Record

**Status**: ODLUKA (GOAT Ciklus 1, 2026-04-27)
**Score**: 4.20 / 5 (vs Paddle 3.90, LemonSqueezy 2.45)
**Source**: `GOAT/CIKLUS_1_2026-04-27.md`

---

## Zašto Polar.sh

1. **Najjeftiniji efektivno za HR EUR sellera**: ~6% + $0.40 + Stripe pass-through fees ≈ **~6.5% all-in**, vs Paddle ~7-8% (s FX spread-om) i LMSQZY ~7%+.

2. **Eksplicit Croatia supported** preko Stripe Connect Express. EUR payout direktno na HR IBAN d.o.o. accounta.

3. **Cash flow fleksibilnost**: konfigurabilan min payout (Polar default €1 base unit, ne fixed); on-demand payouts (vs Paddle samo mjesečno s $100 min).

4. **MOR pokriva HR PDV obveze**: Polar je registrirani MOR — preuzima VAT MOSS handling, eIDAS compliance, refund handling, dispute fees. HR seller (d.o.o.) ne vodi PDV za digital goods sales.

5. **Open-source platforma** s aktivnim development-om. Browser SDK je serverless-friendly (`validateEvent` iz `@polar-sh/sdk/webhooks` eksplicit dizajniran za edge runtimes).

## Glavni rizik i mitigacija

| Rizik | Mitigacija |
|---|---|
| API versioning policy nije publicly dokumentirana | Pin SDK verziju u `cloud/package.json` (npr. `@polar-sh/sdk@^X.Y.Z`); integration test pri svakoj nadogradnji |
| Cloudflare Bot Fight Mode može blokirati webhook delivery | Whitelist Polar webhook source IPs ili isključiti Bot Fight za `/api/polar-webhook` route |
| Polar je novija platforma (manje history vs Paddle) | Sekundarni fallback plan: Paddle migracija dokumentirana ako Polar postane unstable |

## Eliminirani izbori

- **LemonSqueezy**: Stripe akvizicija (srpanj 2024) + roadmap Stripe Managed Payments → tim u siječnju 2026 priznao "slower support and fewer product updates". Build-on-LMSQZY 2026+ nosi materijalni migration risk.
- **Paddle**: 2-3% FX margin spread eliminira fee prednost za HR EUR sellera; min ticket <$10 traži custom pricing (problem za niskotarifne planove).

## Integracijski plan (dva paralelna toka)

### Tok A: Cloud (zamjena Stripe → Polar)

| Fajl | Izmjena | LOC |
|---|---|---|
| `cloud/cf_worker_stripe.ts` | Rename → `cloud/cf_worker_polar.ts`; zamijeni Stripe SDK s `@polar-sh/sdk` | ~180 (re-write) |
| `cloud/wrangler.toml` | Update env var imena (`POLAR_API_KEY`, `POLAR_WEBHOOK_SECRET`) | +5 |
| `cloud/package.json` | `npm uninstall stripe && npm install @polar-sh/sdk` | -1 / +1 |
| `cloud/SETUP.md` | Polar account setup, product setup, webhook URL | re-write ~80 LOC |
| `cloud/supabase_schema.sql` | Tablica `stripe_events` → `polar_events` (rename + payload schema) | ~20 LOC izmjena |

### Tok B: Python klijent

| Fajl | Izmjena | LOC |
|---|---|---|
| `entitlements.py` | `STRIPE_CHECKOUT_URL_BASE` env → `POLAR_CHECKOUT_URL_BASE`; `get_checkout_url()` koristi Polar Checkout link format | ~30 LOC |
| `stranice/pravila.py` | Update merchant-of-record disclosure (Polar.sh kao MOR umjesto "Stripe + manual VAT") | ~10 LOC |

### Migration risk procjena

- **Backwards compat**: Polar webhook payload schema **različit** od Stripe-a. Postojeća tablica `stripe_events` se ne koristi za nove eventove (ostaje za audit history). Nova tablica `polar_events`.
- **Test environment**: Polar ima sandbox mode (`POLAR_API_KEY` test-mode prefiks). Lokalni dev koristi sandbox prije live mode-a.
- **Rollback plan**: feature flag `MOR_PROVIDER=polar|stripe` u Streamlit secrets; ako Polar bug → switch nazad na Stripe (cf_worker_stripe.ts ostaje u repo-u).

## Total LOC procjena za migration

- Cloud: ~285 LOC izmjena
- Python: ~40 LOC
- SQL migracija: ~20 LOC
- **Total**: ~345 LOC, **~5-7 dana solo dev rok**

## Ne implementirati prije

1. **Live test integracije s Polar sandbox**: webhook signature, subscription create flow, payout konfiguracija.
2. **Verify HR d.o.o. KYC zahtjevi**: kontaktirati Polar support za točnu listu dokumenata (Polar nije publicly objavio).
3. **Rolling reserve check**: Stripe Connect Express može aplicirati reserves nezavisno; provjera prije ozbiljnog volumena.

## Sljedeći korak

K3 cloud setup koji je trenutno čekao **stop**. Sav cloud kod treba migraciju Stripe → Polar prije live deploy-a. K3 status reset: "čeka Polar integraciju" umjesto "čeka Stripe credentials".

Implementacija je sljedeća sesija (s čistim kontekstom).
