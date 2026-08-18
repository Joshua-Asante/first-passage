# INSTRUMENT LEDGER — M6B

**Symbol:** CME Micro GBP/USD futures (M6B; Globex, Databento `GLBX.MDP3`) · **Parent:** 6B (standard GBP/USD — **un-ledgered**) · **Asset class:** FX futures (micro)
**Contract facts in committed record:** **commission only** — Bulenox Rates.pdf fee-table row groups `M6A/M6B/M6E = 0.5` ($/contract/side, all-in; unit resolution in `core/firm_rules.py` Bulenox header). **No** committed tick size, tick value, or multiplier in this repo. Do not invent them.
**Status:** **Research/discovery only — geometry-documented, no mechanism cell, no candidate.** Not in the 2026-07-27 third-leg Currencies screen (that map ran M6A + M6E only). No TV export; no `PRICE_COL_BY_INSTRUMENT` row. Not a live leg; no allocation; no K spend.
**Last updated:** 2026-08-18

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Created **2026-08-18** on first touch (ADR [`2026-07-25-instrument-profile-index.md`](../../docs/adr/2026-07-25-instrument-profile-index.md) §5 creation-on-touch) to open the consult limb and price an initial Databento census. Dedup before create: `\bM6B\b` hits only [`core/firm_rules.py`](../../core/firm_rules.py) L58; empty in `STATE.md`, `docs/rejected_candidates.md`, `docs/briefs/`, third-leg [`RESULTS`](../../lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS.md), and [`tnec_envelope RESULTS`](../../lab/archive/tnec_envelope_compile_2026-08/RESULTS.md). Sibling **M6E** *was* Stage-1 `E-COST` — that kill does **not** transfer to M6B.

## PROFILE (machine-readable)

```yaml
symbol: M6B
asset_class: fx-futures
family: []
venue_tradable: false
venue_note: "Live Tradeify Currencies micro set is M6A+M6E only (firm_rules Tradeify commission note: 'micro FX = M6A + M6E only'; product-group lists include 6B standard + M6A, not M6B). Bulenox Rates.pdf fee table does print M6B alongside M6A/M6E. Research/discovery until a live-firm product-group re-verify names M6B."
k_bank_source: "../../discovery_manifests/"
cost_hurdle:
  value: 0.50
  units: "USD/side (Bulenox all-in; Bulenox-only in-repo)"
  basis: "Single committed pricing cite: Bulenox Rates.pdf row M6A/M6B/M6E = 0.5 $/contract/side (comment at firm_rules.py ~L58). NOT priced on Tradeify / MyFundedFutures / BluSky schedules in this repo — do not claim cross-firm schedule coverage."
  source: "#B1"
structure:
  - claim: "Untouched by third-leg Currencies Stage-1 (M6A SURVIVOR / M6E E-COST only). No mechanism cell. No candidate."
    source: "#B2"
```

---

## STANDING WARNINGS (read first)

- **W1 — Parent 6B is un-ledgered.** Creating `6B.md` without a live touching session on 6B itself would be the "complete the matrix" motive ADR 2026-07-25 §5 forbids. M6B inherits **no** bars via `family`.
- **W2 — `ohlcv-1d` UTC-day bucketing → phantom weekend bars.** Drop settle-date weekday > 4. Feed-general.
- **W3 — Pricing is Bulenox-only.** The only in-repo fee cite is the Bulenox Rates.pdf line. Tradeify's published micro-FX commission set is **M6A + M6E only**. Do not paste M6A's Stage-1 `$0.91`/side Tradeify figure onto M6B.
- **W4 — Sibling M6E `E-COST` does not transfer.** M6E was killed on its own Stage-1 cost-tax vs power floor. M6B was never screened; do not inherit the kill.
- **W5 — No tick economics in committed record.** Any future cost-tax / Req-5 hurdle needs a cited tick value (definition pull or CME specs) before arithmetic — not invented here.

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **B1** | **Only in-repo pricing evidence is Bulenox-only.** `core/firm_rules.py` Bulenox header cites Rates.pdf `M6A/M6B/M6E = 0.5` ($/side). Tradeify commission research in the same file names micro FX as **M6A + M6E only** (no M6B row). | [`firm_rules.py`](../../core/firm_rules.py) ~L58 · ~L230–233 | **HIGH** (committed comment cites). |
| **B2** | **Never included in third-leg / ENV-1 instrument pools.** Stage-1 Currencies table: M6A + M6E only. TNEC envelope grid: M6A cells; M6E out-of-pool as E-COST. `\bM6B\b` absent from both RESULTS bodies. | [`third-leg RESULTS`](../../lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS.md) · [`tnec RESULTS`](../../lab/archive/tnec_envelope_compile_2026-08/RESULTS.md) | **HIGH**. |
| **B3** | **No TV panel / loader row.** `core/data/tv_exports/cme/SHA256SUMS` has no M6B filename; `PRICE_COL_BY_INSTRUMENT` has no M6B key. | SHA256SUMS · [`tv_export_loader.py`](../../core/tv_export_loader.py) | **HIGH**. |
| **B4** | **Initial census pull priced (estimate only, 2026-08-18) — not pulled.** Primary `M6B.v.0` `continuous` `ohlcv-1d` `2019-05-06`→`2026-08-18` (exclusive) → streaming estimate on the cost dry-run owner. | [`COST_DRYRUN_M6B_2026-08-18.md`](COST_DRYRUN_M6B_2026-08-18.md) | **HIGH** (metadata estimate). |

## DEAD / REJECTED (instrument-specific)

None. (Do not list M6E's `E-COST` here — wrong instrument.)

## ACTIVE / OPEN

- **Consult limb opened** by this ledger. Future intake: `python scripts/instrument_profiles.py cell M6B <mechanism-id>`.
- **Census pull electable** at the priced estimate — operator GO only; this session did not pull.
- **No candidate, no election, no K spend.**
- **Parent 6B remains un-ledgered** (W1).

## SESSION LOG

- **2026-08-18p** — **Ledger created** on first touch. Dedup clean (only firm_rules L58). Status geometry-documented / no mechanism cell / no candidate. Initial Databento census **estimate-only** ([cost dry-run](COST_DRYRUN_M6B_2026-08-18.md)); no pull, no K, no election, no `core/` / Pine / allocation / `dd_protection` / rail change. Regenerated `profiles.json` / `PROFILES.md` via `instrument_profiles.py build`.
