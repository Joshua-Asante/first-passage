# Design — NAS100 ORB: toggleable day-of-week + hour-block filters

**Date:** 2026-06-24 · **Status:** APPROVED (design) · **Author:** Joshua + CC
**Scope class:** research-tooling (NO core/lock/allocation/dd_protection change)
**Target:** the NAS100 ORB **research candidate** (disposition NO-GO/HOLD per
[`ops/instruments/NAS100.md`](../../ops/instruments/NAS100.md) N5/N7), not the
locked Striker NAS100 v1 pyramid strategy.

## Problem

The NAS100 ORB candidate exists only as the Python research harness
([`lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py`](../../lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py));
there is no ORB `.pine` on disk. Joshua wants **day-of-week** and **session
(hour-block)** filters he can toggle on/off, in both the harness and a Pine
strategy file, kept in parity.

These are exactly the *reliable-offline* class of change per the ledger's N5/N7
fill-fragility lesson ("day-level selection that keeps the touch-fill"), unlike
the exit/entry-point transforms that collapsed on native fills.

## Decisions

1. **Base engine = exit-at-close.** Build the toggles on `orb_backtest` (stop at
   the opposite OR extreme, else flat at session close) — the engine that
   reconciles offline. NOT the give-back/trailing engine (N5/N7: not
   offline-simulable). The Pine mirrors `orb_backtest`.
2. **Hour-block entry semantics = C1 (scan-next-eligible).** When scanning for
   the breakout, ignore bars whose ET hour is blocked; entry = first breakout on
   a non-blocked bar. Matches the house "eligible = session − blocks" pattern and
   keeps a real touch-fill. OR construction is **never** affected by blocks.
3. **DOW filter** = master switch + per-day membership, applied at day level.
4. **Pine = strategy file only** (`core/strategies/candidates/nas100_orb_v0_1.pine`,
   gitignored / live-edge, main-tree only). No indicator file.
5. **All filters default OFF** ⇒ harness and Pine reproduce current ORB behavior
   exactly. This is the headline acceptance test.

## Changes

### Harness — `orb_lib.py` `orb_backtest`
- New kwargs (defaults preserve current behavior):
  - `allowed_dows: frozenset[int] | None = None` — `None` ⇒ all weekdays; else
    only trade days where `meta["dow"] ∈ allowed_dows` (skip at day level, before
    building the OR).
  - `blocked_hours: frozenset[int] | None = None` — `None`/empty ⇒ no block; else
    skip any candidate breakout bar whose ET hour `(tod // 60) ∈ blocked_hours`
    (C1). OR window unaffected.
- Add `entry_tod` to the returned dict (additive) so the hour-block is testable
  and inspectable.
- The inherited stop/exit approximation (min/max over all `rest_tods`) is left
  unchanged; only entry-bar selection + day inclusion are gated.

### Runner — `nas100_orb_filtered.py` (new)
Thin CLI: `--dow mon,tue,...` and `--block-hours 12,13` flags; loads
`NAS100_pep`, prints `summ()` metrics + a `first_passage_mc` line. No flags ⇒
current numbers.

### Pine — `core/strategies/candidates/nas100_orb_v0_1.pine` (new)
v6 strategy port of exit-at-close ORB. Inputs:
- `useDowFilter` (default false) + `tradeMon..tradeFri` (default true).
- `useHourBlock` (default false) + per-hour `blkH09..blkH15` (default false).
- All gating in ET via `hour(time, "America/New_York")` (DST-aware) to match the
  harness. Defaults ⇒ parity with `orb_backtest(or_bars=2, both sides, slip=0)`.
- Note: at `orBars=2` the first entry bar is 10:00 ET, so `blkH09` is a no-op at
  the default OR (kept for completeness / other OR lengths).

### Tests — `test_orb_filters.py` (new)
1. **Parity:** `orb_backtest(allowed_dows=None, blocked_hours=None)` output is
   array-identical to a baseline run (filters-off == current).
2. **DOW:** `allowed_dows={0}` ⇒ every trade is a Monday; count ≤ unfiltered.
3. **Hour-block:** `blocked_hours={10}` ⇒ no entry on a 10:xx ET bar; count ≤
   unfiltered.

## Verification
- Run the new pytest (parity + filter behavior).
- Run `scripts/pine_check.py` on the new Pine (zero-auth compile gate).
- **Honest limit:** true *numeric* harness↔Pine parity requires a TV export from
  Joshua (the ledger's native-export arbiter). This work guarantees structural
  parity + clean compile, not TV numbers.

## Governance
- Append a dated disposition to `ops/instruments/NAS100.md` SESSION LOG: tooling
  change, default-off, parity-preserving, **no validation claim**, no
  core/lock/allocation change.
- **No** CLAUDE.md / LOCK / allocation / dd_protection edits.

## Parity reconcile (2026-06-24, post-merge of first TV export)
First native TV export reconciled via the new `nas100_orb_tv_reconcile.py`. **Trade-day
selection faithful** — real (non-margin-call) trade-days **1663 = harness exact**. Two Pine
config bugs found + fixed: (1) `default_qty_type=percent_of_equity`/100 → 556 margin-call
fragments + compounding → **fixed 1-contract sizing** (R reconstructed offline); (2)
`orReady = orCount > orBars` submitted the resting orders one bar late → **+15m entry lag on
60% of days** → fixed to **`>= orBars`** (submit at OR-completion; first fillable bar = first
post-OR bar under `process_orders_on_close=false`). **Re-export CONFIRMED** (`…_4e1c2.csv`): 0 margin calls,
entry-tod **0.9994**, side **0.9832**, n 1667 (≈1663), meanR **+0.0978** vs harness +0.0872 —
**parity confirmed, faithful port.** Accepted residuals (~2% of trades): same-bar both-break
double-entries + EOD exit one bar after `rth_close`.

## Out of scope (YAGNI)
Indicator Pine; give-back exit; side-filter; any sweep/validation claim that a
DOW/hour combo *improves* the edge (that needs pre-registration + multiplicity
correction — the N6 best-of-K trap); anything touching locked Striker NAS100 v1,
firm_rules, dd_protection, or allocations.
