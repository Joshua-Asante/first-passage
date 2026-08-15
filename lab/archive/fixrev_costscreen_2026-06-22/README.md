# Fixing-reversal cost pre-screen — EURUSD London 16:00 fix (2026-06-22)

**Status:** DONE — verdict **FAIL-COST**. Scope: research (`lab/`), **zero `core/` touch**.

## Why this exists

The 2026-06-21 deep-research run (Q-5LEG-DATA.T1) surfaced the **FX intraday
fixing-reversal** (Krohn, Mueller & Whelan, *Journal of Finance* 2024) as the best
*new-mechanism* scouting hypothesis for a 5th portfolio leg — genuinely distinct
from the two owned mechanisms (Bollinger+BE mean-reversion, breakout+pyramid), a
structural FX session-microstructure regularity. But the paper's own headline is
that the swings are *"not easy to exploit once transaction costs are accounted
for"* — surviving at half-spread, **negative at full retail spread**.

This is the **cheapest falsifier**: measure, on the canonical Pepperstone 5m
EURUSD feed, whether a London-fix fade clears FXIFY-realistic cost — *before* any
full build. It is the same **cost-law** screen that killed the USDCAD MR transfer
(`ops/instruments/USDCAD.md` durable #1: 0.097R round-trip at a 1.42×ATR stop) and
the USOIL spike-fader, applied up front.

## What it measures (claims NO edge)

- **Rule (fixed, representative, NOT optimized):** at the WM/Reuters 4pm London
  fix, enter **long EURUSD** at the fix bar's close (fade the pre-fix USD strength
  → capture the post-fix reversal), protective stop at `S` pips, time-exit `H`
  minutes later. One trade per fix-day, `side=+1`.
- **DST-aware fix resolution:** 16:00 *Europe/London* → 16:00 UTC (winter) / 15:00
  UTC (summer), resolved via the zone, not a hardcoded UTC hour (the recurring TZ
  trap). The BAR_EXPORT epoch is itself UTC and authoritative.
- **Dual frame:** per `(hold × stop)` cell — mean **gross R**, win rate, stop-out
  share, and the **break-even all-in cost** = `mean_gross_R × stop` (the gross
  edge expressed as the pips of cost it can absorb). Then **net R** across an
  all-in-cost grid (0.0 → 1.0 pip). `cost_R = (spread+commission)/stop` — the
  cost law.
- **Verdict gate (pre-stated):** `FAIL-COST` if even the best-of-grid break-even
  ≤ FXIFY's all-in EURUSD cost (`--fxify-cost`, default 0.8 pip); `PASS-PROVISIONAL`
  if it clears (→ a *separate, pre-registered* edge validation, not a deploy);
  `INSUFFICIENT-DATA` if n < 100.

## Result (full 2020-06-22 → 2026-06-12, 1550 fix-days)

**FAIL-COST.** Best-of-grid break-even **0.277 pip** ≪ FXIFY ~0.8 pip. Gross edge
is real but tiny (best cell +0.0455R ≈ **~2 bps** mean post-fix move — reproduces
the paper's magnitude, a validity cross-check) and **robust-direction** (long
EURUSD post-fix is net-positive across the grid, matching the paper's USD-reverses-
after-fix), but it cannot survive retail cost: net R is negative in every cell at
≥0.4 pip all-in, and the most favorable cell only breaks even at 0.277 pip. The
verdict is **robust to the exact FXIFY spread** — even at *zero* cost the gross
edge is ≤0.055R. See [`RESULTS.md`](RESULTS.md).

**Disposition:** the fixing-reversal mechanism does not clear cost on EURUSD →
5th-leg slot stays empty on this mechanism. Pivot effort to **T2 (regime-adaptive
sizing)** — the only lever that addresses the H1 tail. This confirms, on our own
canonical feed, the paper's after-cost conclusion.

## Files

| file | role |
|---|---|
| `fixrev_costscreen.py` | library — DST fix resolution, BAR_EXPORT loader (reuses core `decode_bar_signal`), fade-trade P&L, screen, verdict |
| `test_fixrev_costscreen.py` | 15 self-tests (synthetic; no vendor data) |
| `run_costscreen.py` | driver — locate Downloads pages (skip-if-missing), decode, screen, write `RESULTS.md` |
| `RESULTS.md` | aggregate output (committed; no vendor rows) |

## Data contract & provenance

Input: BAR_EXPORT v0.1 List-of-Trades CSVs, 5m EURUSD, `Signal = epoch_ms|O|H|L|C|V`
(epoch UTC), price column `Price USD`. Three contiguous Pepperstone pages
(2020-06→2022-06, 2022-06→2024-06, 2024-06→2026-06) deduped on bar-open `time`
(keep=last). **Vendor-licensed → read in place from `~/Downloads`, never copied
into the repo; only `RESULTS.md` is committed.** EURUSD is intentionally **not**
registered in the core price-column map (zero `core/` touch — promotion happens
only at admission).

## Reproduce

```bash
cd lab/analysis/fixrev_costscreen_2026-06-22
python -m pytest test_fixrev_costscreen.py -q          # 15 passed (no data needed)
python run_costscreen.py --fxify-cost 0.8              # needs the 3 EURUSD pages in ~/Downloads
```

## Caveats / honest limits

- **Scouting-only** until re-confirmed under a feed-equivalence pre-flight — a
  fix-*timestamp* signal is acutely feed-sensitive.
- `--fxify-cost` is a parameter; set it from the real FXIFY/DXTrade EURUSD
  round-trip cost. The break-even column is the robust read.
- The rule is one representative, non-optimized fade; the `(hold × stop)` grid is
  reported in full to avoid best-cell selection. A `PASS-PROVISIONAL` would NOT
  establish an edge — it would only license a pre-registered validation.
