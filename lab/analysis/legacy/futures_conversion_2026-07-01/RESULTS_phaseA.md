**Theme:** legacy
**Status:** ACTIVE — Phase A provisional MNQ/MYM granularity floors
# Phase A results — provisional MNQ/MYM granularity floors

**PROVISIONAL:** the floors below are provisional until the ATR length (11), SL
multiple (1.20×), and risk% (NQ 0.37% / YM 0.70%) transcribed into `CONFIGS` are
re-verified against the dropped Pine source at Phase B Task B0. Treat as a
LOCK.md mirror, not an authoritative recompute.

## 1. Parsed panels (Step 0)

Ran `scripts/parse_bar_export.py` against the four raw CME-micro-pivot BAR EXPORT
v0.2 exports (operator's Downloads dir, 2026-07-01 exports). Output — gitignored,
not committed:

| Symbol | Bars parsed | Expected (spec §0) | Span |
|--------|------------:|--------------------:|------|
| NQ | 153,122 | ≈153,122 | 2020-01-02T00:00:00Z → 2026-07-02T00:00:00Z |
| YM | 153,054 | ≈153,054 | 2020-01-02T00:00:00Z → 2026-07-02T00:00:00Z |
| J7 | 125,868 | ≈125,868 | 2020-01-01T23:00:00Z → 2026-07-02T00:00:00Z |
| QO | 133,164 | ≈133,164 | 2020-01-02T00:00:00Z → 2026-07-02T00:00:00Z |

All four counts match the brief's expected §0 acceptance numbers exactly (no
material deviation). Span is 2020→2026 for all four, consistent with the rest
of the panel's canonical window. Each parse also wrote a v0.2 instrument
metadata sidecar (`<SYM>_M15.meta.json`) — not used for `$/pt` (see §5/Excluded
and the Constraints section below); price/ATR only.

## 2. Roll-seam counts (Step 3)

`roll_mask.roll_seam_dates(...)` (unique flagged calendar dates) per symbol,
over the full parsed panel:

```
NQ 27
YM 25
J7 26
QO 45
```

All four counts are modest (tens, not thousands) — consistent with rare
calendar roll events (quarterly for NQ/YM/J7, bimonthly for QO) rather than a
miscalibrated gap threshold. No threshold-calibration caveat needed. These
counts are used **only** to mask individual seam bars out of the ATR
computation (per-bar safety) — per `roll_mask.py`'s documented SCOPE (R5), they
do **not** make the unadjusted panel safe for multi-day path/drawdown
reconstruction; that is out of scope for this floor derivation, which only
consumes a median ATR statistic.

## 3. Floor table (Step 2 — verbatim stdout)

```
NQ -> micro ($2.0/pt) PROVISIONAL
  ATR(pts) median 23.62  SL(pts) 28.35  floor_balance $15,322
    $ 25,000: base 1 (ideal 1.632, rounding loss 38.7%)
    $ 50,000: base 3 (ideal 3.263, rounding loss 8.1%)
    $100,000: base 6 (ideal 6.527, rounding loss 8.1%)
    $150,000: base 9 (ideal 9.79, rounding loss 8.1%)
    $250,000: base 16 (ideal 16.317, rounding loss 1.9%)

YM -> micro ($0.5/pt) PROVISIONAL
  ATR(pts) median 38.5  SL(pts) 46.2  floor_balance $3,300
    $ 25,000: base 7 (ideal 7.575, rounding loss 7.6%)
    $ 50,000: base 15 (ideal 15.15, rounding loss 1.0%)
    $100,000: base 30 (ideal 30.3, rounding loss 1.0%)
    $150,000: base 45 (ideal 45.45, rounding loss 1.0%)
    $250,000: base 75 (ideal 75.75, rounding loss 1.0%)
```

**Reading:** MNQ's base position rounds to **9 contracts** at the $150K tier
(ideal 9.79) → **8.1% rounding loss**. MYM's base rounds to **45 contracts** at
the same tier (ideal 45.45) → **1.0% rounding loss**. MYM clears <10%
rounding-loss at every tier in the grid ($25K included, at 7.6%); MNQ only
clears <10% from the $50K tier upward, with the worst rounding loss (38.7%) at
the $25K floor tier where the base is a single contract.

**Numerical concern (flag, not a stop):** the brief's own §4/R8 sanity note
(from "2026-06-30 estimates") expected MNQ's clean (<10% rounding-loss) base
not to be reached until roughly $216K, with large rounding-loss expected
through $150K. The actual computed result clears <10% already at the **$50K**
tier (8.1%) and holds at 8.1% through $150K — better (lower rounding loss) than
that prior estimate anticipated, not worse. Neither of the brief's explicit
absurdity triggers fired: `floor_balance` is $15,322 for MNQ / $3,300 for MYM
(neither near $0), and base-contract counts across the whole $25K–$250K grid
are single/low-double-digit (1–75), not "in the thousands." Independently
hand-verified the `derive_floor()` arithmetic (floor_balance and per-tier
ideal/base/rounding-loss formulas) against the printed stdout — it is
internally consistent. Also independently recomputed the median ATR outside
`derive_floors.py` (same `flag_roll_seams` mask + Wilder EWM, `alpha=1/11`,
`min_periods=11`) and confirmed 23.62 for NQ, matching the module's own output.
ATR-to-price ratio is plausible (~23.6pt median ATR against an NQ panel-median
close of ~$16,478, max ~$30,959) — no ATR-scale error. Best explanation: the
brief's prior R8 note was a rougher pre-parse estimate, superseded here by the
actual roll-seam-masked, full 2020–2026-panel Wilder ATR; it is not evidence of
a bug in this transcription. Flagging per the brief's instruction to report
(not silently adjust) when the direction of a sanity expectation doesn't match
observed output.

**Median-vs-current-ATR caveat (deploy-optimism, added post-review):** these
floors use the **full-panel (2020–2026) median** ATR(11) as a representative
statistic (NQ 23.62 pts, YM 38.5 pts). That understates the **current**
deploy-time ATR: NQ trades near all-time highs (panel-median close ~$15,143 vs
recent-90-day median close ~$29,219, ~2×), and absolute-point ATR scales with
price level — an independent recent-90-day ATR(11) proxy is ~45–54 NQ pts,
roughly **2× the panel median**. Because `floor_balance` scales linearly with
the stop, the true current-deploy MNQ floor is plausibly **~$29K–$35K, not
$15.3K** — which pushes the $25K tier (already 38.7% rounding loss) decisively
below viable and shifts where the $50K tier lands. This is a SEPARATE source of
optimism from the PROVISIONAL banner above: the banner flags that the ATR
length / SL multiple / risk% *parameters* await Pine re-verification (B0); this
caveat flags that even with those parameters confirmed, the *statistic* (6-year
median vs current-regime ATR) is optimistic. **Phase B B0 action:** recompute
the floor using a recent-window ATR(11) that matches what the live Pine will
actually compute bar-to-bar (the locked strategies size off the current ATR(11),
a ~11-bar lookback, not a multi-year median) — or explicitly justify the
median-panel choice as the intended parity target. Do not read the $15.3K/$3.3K
figures as the operative deploy floors.

## 4. Excluded

QO (E-mini gold) and J7 (E-mini yen) are **not** ATR-derivation-grade per spec
§2.3 (stale/thin prints on those two continuous-front series) — no floor is
computed for either symbol here. Guardian (gold) and Aegis (yen) granularity
floors wait on dedicated GC1!/6J1! (full-size or gold/yen-native) re-exports.
Both panels were still parsed in Step 0 (needed for the roll-seam count table
above and to keep the four-symbol Task A3 fold complete), but neither feeds
`derive_floor()` — `CONFIGS` in `derive_floors.py` only has `NQ`/`YM` entries.

## 5. Deferred manifest note

The four parsed futures bar files (`core/data/bar_data/{NQ,YM,J7,QO}_M15.csv` +
`.meta.json` sidecars) are present on disk after Step 0 but are **gitignored
and not committed** — this task is compute-only. Their `SHA256SUMS` manifest
tracking is deliberately **DEFERRED** pending reconciliation of a pre-existing,
unrelated NAS100 bar-file manifest drift (see the vendor-data integrity gate in
`CLAUDE.md`). The bars are fully reproducible at any time via the Step 0
commands below; no data bytes from this task are lost by not committing them.

**Known transient consequence:** Task A2 added `core/data/tv_exports/cme/` to
`MANIFEST_DIRS` but deferred its `SHA256SUMS` scaffold (the empty-scaffold
commit is blocked by the same all-dirs gate + NAS100 drift). Until that scaffold
lands, a standalone `python scripts/check_data_manifests.py --check` (and
`make validate-data` / `make validate`) returns exit 1 with
`MISSING_MANIFEST core/data/tv_exports/cme/SHA256SUMS`. This is **fail-closed and
expected**, not a regression to chase: the pre-commit hook is unaffected (it runs
`--check` only when a commit stages under `core/data/…`), and the condition
self-heals the moment the deferred futures-bar data commit lands (its
`--regenerate` step creates the `cme/` scaffold). Do not "fix" it by committing an
empty scaffold in isolation — that trips the same gate.

## 6. Reproduction

Step 0 (parse; raw exports in the operator's Downloads dir):

```bash
python scripts/parse_bar_export.py --symbol NQ --in "C:/Users/joshu/Downloads/BAR_EXPORT_v0.2_CME_MINI_NQ1!_2026-07-01_833bd.csv"
python scripts/parse_bar_export.py --symbol YM --in "C:/Users/joshu/Downloads/BAR_EXPORT_v0.2_CBOT_MINI_YM1!_2026-07-01_273ea.csv"
python scripts/parse_bar_export.py --symbol J7 --in "C:/Users/joshu/Downloads/BAR_EXPORT_v0.2_CME_MINI_J71!_2026-07-01_9220b.csv"
python scripts/parse_bar_export.py --symbol QO --in "C:/Users/joshu/Downloads/BAR_EXPORT_v0.2_COMEX_MINI_QO1!_2026-07-01_bc865.csv"
```

Step 2 (floor derivation):

```bash
python lab/analysis/futures_conversion_2026-07-01/derive_floors.py
```

Step 3 (roll-seam counts):

```bash
python -c "
import sys; sys.path.insert(0,'lab/analysis/futures_conversion_2026-07-01')
import pandas as pd, roll_mask as rm
for s in ('NQ','YM','J7','QO'):
    b=pd.read_csv(f'core/data/bar_data/{s}_M15.csv')
    print(s, len(rm.roll_seam_dates(b, symbol=s)))
"
```
