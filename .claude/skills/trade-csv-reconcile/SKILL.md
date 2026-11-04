---
name: trade-csv-reconcile
description: Use this skill whenever Joshua uploads or references a TradingView (or broker) trade CSV and any analysis follows — Pepperstone/CME research panels, locked-book TV exports, or c1/Tradovate fill CSVs. Triggers on "analyze the CSV", "reconcile against baseline", "compute PF/WR/DD", "what does the data show", "verify the lock", "monthly analysis", "missed alpha", "panel-thirds", "re-MC pre-reconcile", or pasting/uploading a strategy backtest CSV. Also fires when portfolio-level analysis depends on per-strategy CSV metrics. Covers parsing, Entry/Exit pairing by Trade #, R-pinning per strategy archetype, headline metrics (PF/WR/DD/RF/Net), and Pine-header baseline reconciliation when a locked-book baseline applies. Required before accepting CSV metrics as canonical for a lock/MC decision; not required as ceremony before every ORB/payability research glance. Hand off to prop-firm-challenge for MC / dd_protection / c1 sizing; to c1-rail for live rail fill questions.
---

# Trade CSV Reconcile

Canonical pipeline for parsing TradingView (and related) trade CSVs, computing headline metrics, and — when a locked-book baseline applies — reconciling against Pine-header backtest anchors. Exists because re-derived pairing, R-pinning and metric math drifted (n=209 vs 201, Net P&L 2× from Entry+Exit double-count).

**Mission framing:** live posture is owned by `AGENTS.md` §Purpose / §Live-execution posture. Pepperstone TV exports were the locked-book historical panel; the feed is retired (2026-08-02). Do **not** route CSV sessions through $200K challenge-era ceremony.

**Source-of-truth hierarchy:** Pine source on disk (authoritative for locked strategies) → Pine-header backtest panel (lock-of-record) → `references/baselines.md` (cached anchors) → memory (lossy). If baselines disagree with a fresh Pine read, the Pine read wins; update `references/baselines.md`.

**Boundary:** `prop-firm-challenge` covers MC, dd_protection, firm tiers; `c1-rail` covers live rail fills/arming. This skill stops at verified per-strategy CSV metrics (R-pinned; scaled only when portfolio MC needs it). Do NOT duplicate dd_protection, MC, or rail logic here.

**Full reconcile pipeline is mandatory** before portfolio MC, before a version lock, or before treating a CSV as a lock/MC canonical input. **It is not** for ORB/payability native-harness remeasures, Tradovate fill dumps for rail forensics, or one-off research CSVs with no lock claim: run Steps 1–4 and skip baseline reconcile and $200K scaling unless asked.

---

## Reconcile check 0 — File paths are not data provenance

**Label is not data.** A path, filename or directory does not prove a CSV's feed: on 2026-04-23 Alchemy data under a Pepperstone filename corrupted a whole portfolio MC run (invalidated). Check the CSV symbol header first. When a baseline reconcile is in scope: **halt if any leg fails; do not proceed to portfolio scaling, MC, or any decision artefact.**

**Sub-rule — contract spec vs trade selection.** Dollar P&L can differ across feeds on identical trades. Any cross-feed comparison must distinguish trade-selection drift from contract-spec drift. Futures micros (MYM/MNQ): use the venue point values (`$0.50` / `$2.00`), not CFD contractValue. Historical CFD cross-feed notes: `references/baselines.md`.

**Sub-rule — TradingView <30-day backtests on JPY pairs are unreliable.** P&L inflates up to ~153× when the JPY→USD conversion hook fails to initialize on short windows. Do not accept them for JPY-pair P&L; recompute in Python: `qty × (exit − entry) ÷ exit − 0.00006 × qty`.

**Sub-rule — last exit << chart last bar is a pane claim, not automatically “the strategy died.”** Last-N Deep and entire-history Deep are different requests: flip that chip on the same script before treating the CSV as a full-window backtest. It can also be session-edge adjacency on gapped bars; a dated front month dying the same week does not by itself prove a warehouse hole, and Last-N emptiness on `MNQ1!` does not by itself prove adjacency. Inventory the testing period (Deep / Available chart range / Last-N vs entire-history), then read [`docs/notes/research/2026-08-28-tradingview-strategy-report-july-2026.md`](../../../docs/notes/research/2026-08-28-tradingview-strategy-report-july-2026.md) before computing PF/WR or reconciling a lock. A prior export of the same construct through a later date beats the short pane.

---

## Canonical pipeline

These steps run in this order for every CSV reconciliation task; skipping or reordering them produces anchor drift.

### Step 1 — Inventory

For each CSV: filename, row count, first 3 rows, last row. Confirm consistent column structure across files in the batch.

Standard TradingView export columns (BOM-prefixed on first column, strip with `encoding='utf-8-sig'`):

```
Trade #, Type, Signal, Date and time, Price USD, Size (qty),
Net P&L USD, Net P&L %, Cumulative P&L USD, Cumulative P&L %,
Favorable excursion USD, Adverse excursion USD
```

**Schema migration (2026 current export):** TradingView renamed `Trade #`→`Trade number`, `Net P&L USD`→`Net PnL USD`, `Cumulative P&L *`→`Cumulative PnL *`, and added `Size (value)` and split excursion USD/% columns. `load_csv`'s `COLUMN_ALIASES` map normalizes current exports to the canonical internal names, so **both** schemas parse. On `ValueError: CSV missing required columns`, add an alias entry; do not hand-rename the CSV. Regression guard: `tests/test_reconcile_skill_schema.py`.

### Step 2 — Pair Entry/Exit by Trade #

Each Trade # appears as both an Entry row (`Type ∈ {"Entry long", "Entry short"}`) and one or more Exit rows (`Type ∈ {"Exit long", "Exit short"}`). Realized P&L lives on Exit rows only.

For pyramid architectures (Striker DJ30, Striker NAS100), multiple Entry rows per Trade # represent pyramid adds — preserve them as separate position legs but attribute realized P&L only at the final Exit. Compute `pyramid_pnl_share` separately (sum of P&L from pyramid-add legs / total P&L).

Use `scripts/reconcile.py` — do NOT re-derive the parser inline. The parser handles BOM, multi-leg pyramid pairing, and the Q-A1-c double-count trap (2026-04-29) where summing both Entry and Exit Net P&L rows double-counted every trade.

### Step 3 — R-pinning per strategy archetype

Most error-prone step. The 1R basis differs by strategy architecture:

| Strategy | Architecture | 1R basis |
|---|---|---|
| Guardian Gold (v5.x) | Pure trend-rider (no BE, no trail) | **Median loss** |
| Striker DJ30 (v4.x) | Breakout + pyramid + BE | **Mean of |losses| > 1% of account** (full-stop cohort) |
| Striker NAS100 (v1.x) | Breakout + pyramid + BE | **Mean of |losses| > 1% of account** (full-stop cohort) |
| Aegis USDJPY (v4.x) | Mean-revert + BE | **Mean of |losses| > 1% of account** (full-stop cohort) |

**Fallback rule (corrected 2026-04-23, commit `bf32aa3`):** if `n == 0` full stops, fall back to median. Do NOT use the earlier `n < 5` fallback: it swapped to a systematically wrong estimator and caused scale inflation on short panels.

**Thin-cohort warning:** when `1 ≤ n < 5` full stops, the full-stop mean is used but flagged as noisy. Surface in output as `cohort_warning=True`; do not silently accept.

### Step 4 — Compute headline metrics

Per strategy:

- `N` — closed trades (count of Exit rows, paired by Trade #)
- `wins` / `losses` — sign-partition of Net P&L USD (>0 vs ≤0)
- `WR` — wins / N (percent)
- `gross_win` / `gross_loss`
- `PF` — gross_win / |gross_loss|
- `Net` — sum of Net P&L USD on Exit rows (NOT sum of all rows)
- `avg_win` / `avg_loss`
- `max_DD` ($) — peak-to-trough on cumulative equity reconstruction (append each trade's Net P&L, track running peak). **Initial capital:** use the panel's stated `strategy.initial_capital` when present; for locked-book Pepperstone challenge-era panels the historical default was **$200K** — do not invent a $200K base for Tradovate/c1 or micro-futures research CSVs
- `max_DD %` — `max_DD / running_peak * 100` at trough
- `RF` — `Net / max_DD` ($-basis)

Pyramid architectures get one additional metric:
- `pyramid_pnl_share` — sum of P&L from pyramid-add legs / total P&L. Verified: **Striker DJ30 ~42.7%** (Q-DJ30-2 Phase B, 2026-05-06, v4.5 panel; base-only PF 2.33, so a sub-half share is structural; the 2026-05-23 pyramid bump to 750% likely raises it); **Striker NAS100 81–99%/yr** (Q-NAS-1, 2026-05-05; base-only PF ~0.31, the pyramid *is* the strategy). The earlier "DJ30 ~94%" misattributed NAS100's share. Red flag is strategy-specific: for a NAS100-class arch (base PF < 1), a share sustained below ~70% is the escalation tripwire (NAS CHANGELOG); DJ30's lower share is expected.

### Step 5 — Reconcile against Pine-header baseline

Compare computed metrics to the Pine-header lock-of-record values in `references/baselines.md`.

| Metric | Tolerance |
|---|---|
| Trade count | **Exact** |
| PF | ±0.5% |
| Net | ±0.5% |
| Max DD % | ±1.0% (DD is noisiest — TV uses intrabar peak/trough; CSV reconstruction uses bar-close) |
| WR | ±0.5pp |

**If reconciliation fails — halt.** Do not proceed to portfolio scaling, MC, or any decision artefact. Triage in this order:

1. **First suspect: filename/feed mislabel.** Check that the CSV symbol header (e.g., `PEPPERSTONE:XAUUSD`) matches the directory and filename. The 2026-04-23 incident is the canonical failure shape.
2. **Second suspect: stale anchor in `references/baselines.md`.** Re-read Pine source headers and update the cached anchor if needed. State what changed and when.
3. **Third suspect: genuine version drift.** If the user is mid-parameter-sweep, current Pine may not reproduce the locked anchor. Confirm with user before treating the new CSV as canonical. NEVER silently update the anchor without confirmation.
4. **Fourth suspect: the Pine-header reproduction itself is stale.** Lesson #6 (2026-05-05): Pine pasted at session-N is not necessarily Pine at lock-time-T. The anchor reproduces only when current Pine, run on the canonical feed, regenerates the headline metrics. If the user pasted Pine mid-edit, neither side is canonical until a fresh backtest reconciles them.

### Step 6 — Scale to locked allocations (portfolio-level work only)

When the task is portfolio-level (monthly P&L aggregation, MC pre-reconciliation, missed-alpha discovery), apply the per-strategy scale factor:

```
scale_factor = target_risk_pct / implied_risk_pct
implied_risk_pct = (1R_dollars / 200_000) × 100
scaled_pnl_per_trade = raw_pnl × scale_factor
```

Use locked allocations from [`AGENTS.md`](../../../AGENTS.md) §Strategy Reference / `core/firm_rules.py` `_BASE_RISK` (not restated here; `references/baselines.md` is PF/WR/Net/DD cache only). **Skip this step** for ORB-MNQ / venue-native research CSVs and for c1 fill dumps — those are not the locked four-strategy challenge book.

Historical static-equity challenge sizing was against initial $200K, NOT compounded equity. Live c1 sizing is the rail (`BASE_RISK × DD_SCALE × lifecycle` + integer qty): never re-derive challenge `$200K` multipliers for Tradovate fills.

### Step 7 — Output

Standard format (every reconciliation produces this):

```
=== {Strategy} {version} — {feed} ===
N        : {count}              [reconcile: {OK | DRIFT n_baseline-n_actual}]
PF       : {pf:.3f}              [reconcile: {OK | DRIFT pct}]
WR       : {wr:.2f}%
Net      : ${net:,.2f}            [reconcile: {OK | DRIFT pct}]
DD       : {dd_pct:.2f}%          [reconcile: {OK | DRIFT pct}]
RF       : {rf:.2f}
1R basis : {method}, n={n}        [{cohort_warning if 1 ≤ n < 5}]
1R       : ${r_dollars:,.2f}
{pyramid line if applicable}: {pct}%
```

For portfolio-scaled output: include `scaled_net`, `scaled_dd`, `scale_factor` per strategy.

If any leg shows DRIFT, the output ends with **HALT — DRIFT DETECTED** and the suspected cause from Step 5 triage. Do not produce a "best guess" combined panel from a partially-failing reconciliation.

---

## Known traps

Failure modes that have actually happened, ranked by frequency:

**1. CSV mislabel.** See Reconcile check 0. Always reconcile before accepting metrics.

**2. R-basis confusion.** Using median when full-stop mean is correct (or vice versa) silently inflates/deflates scale factor by 2-3×. Always pin explicitly per strategy archetype per the Step 3 table.

**3. Net P&L 2× from Entry+Exit double-count.** Q-A1-c (2026-04-29). The canonical loader filters to `Type.startswith('Exit')` for P&L attribution.

**4. Pair-by-Trade# not by row sequence.** Pyramid architectures (Striker, NAS) have multi-row Entry/Exit per Trade #. Iterating row-by-row instead of grouping by Trade # double-counts pyramid legs.

**5. <30-day TV JPY exports.** See Reconcile check 0.

**6. contractValue on old CFD CSVs (HISTORICAL).** TradingView without explicit `contractValue` defaults to 1; see [operational_rules §3](../../../docs/operational_rules.md). Irrelevant to MYM/MNQ micros.

**7. Encoding/BOM on first column.** TradingView exports have a BOM (`\ufeff`) on the first header. Use `encoding='utf-8-sig'` and strip column whitespace, or `df['Trade #']` lookups silently fail.

**8. Cross-feed dollar deltas mistaken for trade-selection drift.** Compare trade count and WR before suspecting strategy divergence.

**9. Compounded vs static sizing.** TradingView strategy-tester uses `strategy.equity` (compounded) by default. Normalize to static $200K only for challenge-era measurement; never force it onto c1/Tradovate or ORB research CSVs.

**10. Stale anchor in `references/baselines.md`.** When the user re-locks a strategy, the Pine-header baseline updates. If the references file lags, reconciliation fails on the new (correct) CSV — looks like a CSV problem but is a skill problem. Sync on every re-lock.

**11. Indicator vs strategy file confusion.** The indicator file's display logic does not produce a backtest. Only the `strategy.pine` file's `strategy(...)` call generates the CSV. If a user pastes "the locked Pine" but it's the indicator file, no CSV reconciliation is possible from it.

**12. Hurst R/S / autocorrelation on log prices not log returns.** If a user asks for instrument characterization off CSV-derived bars, run R/S and ACF on log RETURNS (`np.diff(np.log(close))`), not log prices. Log prices give H≈1 (artifactual non-stationarity, AUDNZD 2026-04-04 incident).

**13. TV export schema migration (2026-06-27).** See Step 1.

**14. Pyramid share — per-leg vs qty-apportioned.** Under the current schema each pyramid leg is its OWN `Trade number` with Signal `Long Add` / `Exit Long Add`, P&L realized per-leg. `compute_pyramid_share` detects this (any `Add` in exit Signal) and uses direct add-leg attribution; the legacy multi-entry-per-Trade# path uses qty-apportionment. These definitions are NOT comparable, and neither equals the counterfactual net-with-pyramid vs base-only. The `expected_pyramid_share` anchors (DJ30 ~43%, NAS ~88%) predate the per-leg schema, so the sub-50% output flag is **advisory**, not a hard RED FLAG, until re-measured.

---

## When NOT to use this skill

- **No CSV in scope.** Pure methodology questions, framework discussions, brief authoring without data — route to `inqhiori`.
- **Pine code authoring/audit.** Hand off to `pinescript-v6`. This skill consumes CSV outputs of Pine; it doesn't write Pine.
- **MC simulation, dd_protection decisions, allocation locks, c1 arming.** Hand off to `prop-firm-challenge` / `c1-rail`. This skill produces verified metrics; those skills own the decisions.
- **Bar data rather than trade data.** 15-min OHLCV / tick exports use a different parser. This skill is trade-CSV-specific.
- **Ceremony on research glances.** Do not run the full lock/MC reconcile pipeline solely because a CSV was mentioned — match depth to whether a lock or MC claim is at stake.

---

## Reference files

- `scripts/reconcile.py` — canonical loader + metrics + reconciliation pipeline. Run as:
  ```
  python scripts/reconcile.py <csv_path> --strategy <guardian|striker_dj30|striker_nas|aegis> [--baseline] [--scale]
  ```
- `references/baselines.md` — Pine-header lock-of-record per strategy/version. Updated on every re-lock.

Related skills:
- `prop-firm-challenge` — MC simulation, dd_protection, live ops, broker position sizing (downstream consumer of this skill's output)
- `pinescript-v6` — Pine source authoring/auditing (upstream producer of CSVs this skill parses)
- `inqhiori` — methodology framing for any reconciliation that opens a structural question (e.g., DRIFT detected → INQHIORI loop, not silent re-baseline)
