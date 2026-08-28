---
name: trade-csv-reconcile
description: Use this skill whenever Joshua uploads or references a TradingView (or broker) trade CSV and any analysis follows — Pepperstone/CME research panels, locked-book TV exports, or c1/Tradovate fill CSVs. Triggers on "analyze the CSV", "reconcile against baseline", "compute PF/WR/DD", "what does the data show", "verify the lock", "monthly analysis", "missed alpha", "panel-thirds", "re-MC pre-reconcile", or pasting/uploading a strategy backtest CSV. Also fires when portfolio-level analysis depends on per-strategy CSV metrics. Covers parsing, Entry/Exit pairing by Trade #, R-pinning per strategy archetype, headline metrics (PF/WR/DD/RF/Net), and Pine-header baseline reconciliation when a locked-book baseline applies. Required before accepting CSV metrics as canonical for a lock/MC decision; not required as ceremony before every ORB/payability research glance. Hand off to prop-firm-challenge for MC / dd_protection / c1 sizing; to c1-rail for live rail fill questions.
---

# Trade CSV Reconcile

Canonical pipeline for parsing TradingView (and related) trade CSVs, computing headline metrics, and — when a locked-book baseline applies — reconciling against Pine-header backtest anchors. Exists because sessions were re-deriving Entry/Exit pairing, R-pinning, and metric math, and drift surfaced as anchor disagreements (n=209 vs 201, Net P&L 2× from Entry+Exit double-count).

**Mission framing:** live posture is owned by `CLAUDE.md` §Purpose / §Live-execution posture — read it there, not from this line. Incumbent eval is live (S1); no book is deployed. Pepperstone TV exports were the locked-book historical panel and the feed is retired (2026-08-02); OANDA/Alchemy/DXTrade paths are **historical challenge-era** — keep the traps below so old CSVs do not corrupt analysis, but do **not** route every CSV session through FXIFY/$200K/DXTrade ceremony.

**Source-of-truth hierarchy:** Pine source on disk (authoritative for locked strategies) → Pine-header backtest panel (lock-of-record) → `references/baselines.md` (cached anchors) → memory (lossy). When this skill's baselines disagree with a fresh Pine read, the Pine read wins and `references/baselines.md` needs updating.

**Boundary with prop-firm-challenge / c1-rail:** prop-firm-challenge covers MC, dd_protection, firm tiers; c1-rail covers live rail fills/arming. This skill stops at verified per-strategy CSV metrics (R-pinned; scaled only when portfolio MC needs it). Do NOT duplicate dd_protection, MC, or rail logic here.

**When the full reconcile-before-MC pipeline is mandatory:** before portfolio MC, before a version lock, or before treating an uploaded CSV as a lock/MC canonical input. **When it is not:** ORB/payability native-harness remeasures, Tradovate fill dumps for rail forensics, and one-off research CSVs with no lock claim — run Steps 1–4 (parse + metrics); skip baseline reconcile / $200K challenge scaling unless the task asks for them.

---

## Rule 0 — File paths are not data provenance

A CSV at `data/tv_exports/pepperstone/aegis.csv` (retired) is not necessarily Pepperstone data. The 2026-04-23 morning Aegis arm corrupted the entire portfolio MC run because Alchemy data sat in the Pepperstone directory under a Pepperstone filename — produced Pass 84.37% / Bust 1.03% (invalidated). When a baseline reconcile is in scope: **halt if any leg fails; do not proceed to portfolio scaling, MC, or any decision artefact.**

**Sub-rule — broker contract spec verification.** Per-feed dollar P&L differs from per-feed trade selection. Historical: DJ30 OANDA $5/pt vs DJ30 Pepperstone $1/pt produced a 5× dollar delta on identical trade selection; USDJPY trade selection was broker-uniform (123t, 2026-04-23); XAUUSD had ~16-29% stop-proximity haircut across feeds. Futures micros (MYM/MNQ): use the venue point values (`$0.50` / `$2.00`), not CFD contractValue. Any cross-feed comparison must distinguish trade-selection drift from contract-spec drift.

**Sub-rule — TradingView <30-day backtests on JPY pairs are unreliable.** P&L inflation up to ~153× from JPY→USD conversion hook failing to initialize on short windows. Do not accept short-window TV exports for JPY-pair strategies; validate via Python recompute: `qty × (exit − entry) ÷ exit − 0.00006 × qty`.

**Sub-rule — last exit << chart last bar on a `1!` / Deep export is a warehouse claim.** After the July 2026 Strategy Report rewrite, the price pane and the report can be different series. If a List-of-Trades (or Overview) ends weeks/months before the chart’s last candle — especially on `MNQ1!` / `NQ1!` / `ES1!`, or when buy-and-hold on the **report** dies the same day — do **not** treat the CSV as “the strategy stopped” or as a full-window backtest. Inventory the testing period (Deep / Available chart range / Last-N vs Reset-to-chart-session), then read [`docs/notes/research/2026-08-28-tradingview-strategy-report-july-2026.md`](../../../docs/notes/research/2026-08-28-tradingview-strategy-report-july-2026.md) before computing PF/WR or reconciling a lock. A prior export of the same construct through a later date beats the short pane.

**Sub-rule — DXTrade `contractValue` (HISTORICAL / DORMANT).** FXIFY/DXTrade execution is retired. If an old DXTrade CSV appears: XAUUSD=100, USDJPY=default(1), DJ30=10 (CRITICAL), NAS100=10. Not a live sizing check — see operational Rule 3.

---

## Canonical pipeline

These steps run for every CSV reconciliation task, in this order. Skipping a step or running them out of order is what produces anchor drift.

### Step 1 — Inventory

```bash
ls -la /mnt/user-data/uploads/
```

For each CSV: filename, row count, first 3 rows, last row. Confirm consistent column structure across files in the batch.

Standard TradingView export columns (BOM-prefixed on first column, strip with `encoding='utf-8-sig'`):

```
Trade #, Type, Signal, Date and time, Price USD, Size (qty),
Net P&L USD, Net P&L %, Cumulative P&L USD, Cumulative P&L %,
Favorable excursion USD, Adverse excursion USD
```

**Schema migration (2026 current export):** TradingView renamed columns —
`Trade #`→`Trade number`, `Net P&L USD`→`Net PnL USD`, `Cumulative P&L *`→
`Cumulative PnL *`, plus a new `Size (value)` column and split excursion
USD/% columns. `load_csv` carries a `COLUMN_ALIASES` map that normalizes the
current schema back to the canonical internal names, so **both** legacy and
current exports parse. If you hit `ValueError: CSV missing required columns`,
the alias map needs a new entry — do not hand-rename the CSV.

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

**Fallback rule (corrected 2026-04-23, commit `bf32aa3`):** if `n == 0` full stops, fall back to median. Do NOT use the earlier `n < 5` fallback — it swapped to a systematically-wrong estimator under the regime it was designed to protect. Pathological scale inflation on short panels traces to the old fallback.

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
- `pyramid_pnl_share` — sum of P&L from pyramid-add legs / total P&L. Verified per-strategy: **Striker DJ30 ~42.7%** (Q-DJ30-2 Phase B, 2026-05-06, v4.5 panel — base entries are themselves edge-bearing, base-only PF 2.33, so a sub-half share is structural; the 2026-05-23 pyramid bump to 750% likely raises it); **Striker NAS100 81–99%/yr** (Q-NAS-1, 2026-05-05 — base-only PF ~0.31, the pyramid *is* the strategy). The earlier "DJ30 ~94%" was a cross-strategy misattribution of NAS100's share (Q-DJ30-2 diagnosis). Red-flag is strategy-specific: for a NAS100-class arch (base PF < 1) a share sustained below ~70% is the escalation tripwire (NAS CHANGELOG); DJ30's lower share is expected, not a defect.

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
4. **Fourth suspect: the Pine-header reproduction itself is stale.** Lesson #6 (2026-05-05): Pine source pasted at session-N is not necessarily Pine source at lock-time-T. The lock anchor reproduces only when current Pine, run on canonical feed, regenerates the headline metrics. If user pasted Pine mid-edit, neither side is canonical until a fresh backtest reconciles them.

### Step 6 — Scale to locked allocations (portfolio-level work only)

When the task is portfolio-level (monthly P&L aggregation, MC pre-reconciliation, missed-alpha discovery), apply the per-strategy scale factor:

```
scale_factor = target_risk_pct / implied_risk_pct
implied_risk_pct = (1R_dollars / 200_000) × 100
scaled_pnl_per_trade = raw_pnl × scale_factor
```

Use locked allocations from [`CLAUDE.md`](../../../CLAUDE.md) §Strategy Reference / `core/firm_rules.py` `_BASE_RISK` (not restated here; `references/baselines.md` is PF/WR/Net/DD cache only). **Skip this step** for ORB-MNQ / venue-native research CSVs and for c1 fill dumps — those are not the locked four-strategy challenge book.

For historical static-equity challenge measurement, sizing was against initial $200K, NOT compounded equity. TradingView's `strategy.equity` is compounded by default. Live c1 sizing is the rail (`BASE_RISK × DD_SCALE × lifecycle` + integer qty) — never re-derive challenge `$200K` multipliers for Tradovate fills.

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

**1. CSV mislabel (file paths ≠ data provenance).** 2026-04-23 Alchemy data in `pepperstone/` directory corrupted morning MC. Always reconcile before accepting metrics. The CSV symbol header is the cheapest first check.

**2. R-basis confusion.** Using median when full-stop mean is correct (or vice versa) silently inflates/deflates scale factor by 2-3×. Always pin explicitly per strategy archetype per the Step 3 table.

**3. Net P&L 2× from Entry+Exit double-count.** Q-A1-c (2026-04-29) burned a session on this. If both Entry and Exit rows are summed (instead of Exit only), every trade is counted twice. The canonical loader filters to `Type.startswith('Exit')` for P&L attribution.

**4. Pair-by-Trade# not by row sequence.** Pyramid architectures (Striker, NAS) have multi-row Entry/Exit per Trade #. Iterating row-by-row instead of grouping by Trade # double-counts pyramid legs.

**5. <30-day TV JPY exports have ~153× P&L inflation.** JPY→USD conversion hook fails to initialize on short windows. NEVER use <30-day TV exports for JPY-pair P&L; recompute via Python: `qty × (exit − entry) ÷ exit − 0.00006 × qty`.

**6. DJ30 contractValue=1 instead of 10 (HISTORICAL).** TradingView without explicit `contractValue` defaults to 1; retired DXTrade DJ30 was 10. Still bites on old CFD CSVs; irrelevant to MYM/MNQ micros (`$0.50`/`$2.00` point values).

**7. Encoding/BOM on first column.** TradingView exports have a BOM (`\ufeff`) on the `Trade #` header. Use `encoding='utf-8-sig'` and strip column whitespace, or `df['Trade #']` lookups silently fail.

**8. Cross-feed dollar deltas mistaken for trade-selection drift.** Historical CFD: DJ30 OANDA $5/pt vs Pepperstone $1/pt → 5× P&L on identical trades. Compare trade count and WR before suspecting strategy divergence. OANDA panel retired from the active manifest (substrate Phase 5, 2026-08-02) — still relevant if an offline OANDA CSV is re-introduced.

**9. Compounded vs static sizing.** TradingView strategy-tester uses `strategy.equity` (compounded) by default. Historical DXTrade challenge execution used static $200K. Normalize only when the task is challenge-era measurement; do not force $200K static framing onto c1/Tradovate or ORB research CSVs.

**10. Stale anchor in `references/baselines.md`.** When the user re-locks a strategy, the Pine-header baseline updates. If the references file lags, reconciliation fails on the new (correct) CSV — looks like a CSV problem but is a skill problem. Sync on every re-lock.

**11. Indicator vs strategy file confusion.** The indicator file's display logic does not produce a backtest. Only the `strategy.pine` file's `strategy(...)` call generates the CSV. If a user pastes "the locked Pine" but it's the indicator file, no CSV reconciliation is possible from it.

**12. Hurst R/S / autocorrelation on log prices not log returns.** If a user asks for instrument characterization off CSV-derived bars, run R/S and ACF on log RETURNS (`np.diff(np.log(close))`), not log prices. Log prices give H≈1 (artifactual non-stationarity, AUDNZD 2026-04-04 incident).

**13. TV export schema migration (2026-06-27).** The current TV schema renamed `Trade #`→`Trade number`, `Net P&L USD`→`Net PnL USD`, `Cumulative P&L *`→`Cumulative PnL *`. The pre-migration `load_csv` hard-failed (`CSV missing required columns`) on every current-format export — including the committed canonical baselines. Fixed via a `COLUMN_ALIASES` normalization layer (handles both schemas). Regression guard: `tests/test_reconcile_skill_schema.py`.

**14. Pyramid share — per-leg vs qty-apportioned.** Under the current schema each pyramid leg is its OWN `Trade number` with Signal `Long Add` / `Exit Long Add`, and P&L is realized per-leg. `compute_pyramid_share` detects this (any `Add` in exit Signal) and uses direct add-leg attribution; the legacy multi-entry-per-Trade# path still uses qty-apportionment. These two definitions are NOT comparable, and neither equals the counterfactual "pyramid is the edge" framing (net-with-pyramid vs base-only). The `expected_pyramid_share` anchors (DJ30 ~43%, NAS ~88%) predate the per-leg schema — the sub-50% output flag is now **advisory**, not a hard RED FLAG, until those anchors are re-measured.

---

## When NOT to use this skill

- **No CSV in scope.** Pure methodology questions, framework discussions, brief authoring without data — route to `inqhiori` or `ooda-loop`.
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
