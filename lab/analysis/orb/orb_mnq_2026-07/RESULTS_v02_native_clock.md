# ORB MNQ v0.2 — native-harness EOD clock delta + Tradeify k-grid (no TV export)

**Date:** 2026-07-31
**Harness:** [`run_v02_native_clock_kgrid.py`](run_v02_native_clock_kgrid.py) — `orb_lib.orb_backtest` verbatim
**Data:** cached `MNQ.v.0` 15m panel (`_mnq_15m.pkl`), 2019-05-06 → 2026-07-15, $0.00 (no pull)
**Class:** structural / Notice-phase. No Pine edit, no filter, no new campaign, no K spend.

**Why:** [`RESULTS_v02_clock_kgrid.md`](RESULTS_v02_clock_kgrid.md) scored a TV export whose
full-session EOD fills printed at **15:30** instead of the documented **16:00** (the defect D5
pins shut). Its own §3 says freeze no k policy until a 16:00 re-export is scored — which needs an
operator TV paste. The native harness has **no such dependency**: `orb_lib.CLOSE_TOD_US` is 15:45
(last RTH bar-open, session ends 16:00), so it has always run the correct clock, and the defective
clock is reproducible by setting `close_tod = 15:15`. Both are therefore measurable offline today.

---

## 0. Cross-check — the harness reproduces the published Stage-2 anchor exactly

| Window | This run | [`RESULTS.md`](RESULTS.md) published | Match |
|---|---|---|:--:|
| FULL 2019-05+ net meanR (Bulenox) | **+0.0668** (n=1,846) | +0.0668 (n=1,846) | ✅ |
| 2021+ net meanR (Bulenox) | **+0.0894** (n=1,420) | +0.0894 (n=1,420) | ✅ |

Trade-day mapping is asserted elementwise against the engine's own `range` array before any
dollar conversion; a mapping that does not reproduce it aborts the run.

---

## 1. THE LOAD-BEARING FINDING — the D5 conformance fix **costs edge**

Same construct, same data, same Tradeify economics ($0.91/side + 1 tick). Only the session-end
clock differs:

| Clock | n | net meanR | net $ (k=1) | WR | stopped |
|---|---:|---:|---:|---:|---:|
| **Correct — exit 16:00** (v0.2 contract, post-D5) | 1,846 | **+0.0626** | **$17,780** | 46.37% | 38.0% |
| Defective — exit 15:30 (pre-D5 export) | 1,841 | **+0.0778** | **$23,738** | 47.58% | 35.9% |

- **61.2%** of common days (1,127 / 1,841) have a different P&L.
- Total delta at k=1: **−$5,832** (−25% of net). Mean **−$3.17/day**. Worst single-day delta
  −$388, best +$418.
- The longer session also converts **+2.1pp more days into stop-outs** (35.9% → 38.0%) — more
  time for price to reach the opposite OR extreme.

**Reading: the final 30 minutes of the RTH session are a net-negative P&L term for this
construct.** The published k-grid was not merely mis-clocked, it was **flattering** — it scored a
construct that exits before a loss-making half hour. The owed re-export will come back **worse
than the 07-30 panel, not neutral.** Anyone reading the two side by side without this note would
likely misattribute the drop to a data or Pine problem.

**This does NOT license adopting 15:30.** The frozen pre-registered construct is *flat at session
close*, and 16:00 is the correct expression of it. Choosing 15:30 *because it backtests better* is
exit-time tuning — inside the exit space already pre-killed in
[`RESULTS_tv_export_realism.md`](RESULTS_tv_export_realism.md) §2b/2c, and in any case a new
candidate at `K_eff = 3` (DSR floor 0.98, which the construct's own full-window annSR 0.890 does
not clear). D5 stands as correct. The finding is a **cost of conformance**, recorded honestly.

---

## 2. k-policy geometry on the CORRECT clock (Tradeify $0.91/side)

Trail buffer **$3,000** (Select 100K), winning-day floor **$200**, start equity $100k, one
trade/day so per-trade = per-day. `headroom = $3,000 + worst_day` (>0 ⇒ that day alone cannot bust
a fresh peak).

### FULL window 2019-05 → 2026-07 (n=1,846)

| k | net | PF | mean | maxDD | RF | worst day | headroom | single-day bust? | days ≥$200 | trail episodes |
|--:|--:|--:|--:|--:|--:|--:|--:|:--:|--:|--:|
| 1 | $17,780 | 1.109 | $9.63 | −$6,527 | 2.72 | −$784 | $2,216 | no | **17.8%** | 3 |
| 2 | $35,560 | 1.109 | $19.26 | −$13,054 | 2.72 | −$1,568 | $1,432 | no | **31.4%** | 8 |
| 3 | $53,339 | 1.109 | $28.89 | −$19,581 | 2.72 | −$2,351 | $649 | no | **36.0%** | 12 |
| 4 | $71,119 | 1.109 | $38.53 | −$26,108 | 2.72 | −$3,135 | −$135 | **YES** | 38.3% | 18 |
| 5 | $88,899 | 1.109 | $48.16 | −$32,635 | 2.72 | −$3,919 | −$919 | **YES** | 40.5% | 21 |

### Payability across windows (days clearing the $200 floor)

| Window | n | k=1 | k=2 | k=3 |
|---|--:|--:|--:|--:|
| FULL 2019-05+ | 1,846 | 17.8% | 31.4% | 36.0% |
| 2021+ (pre-reg regime window) | 1,420 | 20.8% | 34.9% | 38.6% |
| recent ~2y (2024-07-30+) | 502 | 23.3% | 36.9% | 40.6% |

Published (defective clock, ~2y): k=1 22.2% · k=2 33.1% · k=3 37.6% — the correct clock is
**slightly worse on payability too**, consistent with §1.

### Reading

- **The k ∈ {1,2,3} safe band is confirmed on the correct clock** — worst day is −$784 × k, so
  k ≤ 3 keeps a single day inside the $3,000 trail; k ≥ 4 is single-day bustable from a fresh
  peak. This reproduces the published band and the Pine tooltip.
- **k does not resolve payability, but ORB is not structurally unpayable either.** This is the
  substantive correction to the working assumption. The fade-program spec's *"one trade/day is
  structurally unpayable"* was derived for a high-WR / low-R:R construct whose best possible day
  is $107–140 — it **never** clears $200. ORB is the opposite shape: EOD winners average **$181.53
  at k=1 with a 74.8% win rate** (recent 2y), so it clears $200 on 18–23% of days at k=1 and
  31–37% at k=2. The constraint is **cadence, not impossibility.**
- **The cost of buying cadence with k is trail episodes, not single-day bust.** Going k=1→3 lifts
  payable days from 17.8%→36.0% but takes trail episodes from **3 → 12** on the full window, with
  only $649 of single-day headroom left. k=2 is the balanced cell: 31.4% payable, $1,432 headroom,
  8 episodes.

---

## 3. Exit split — recent ~2y, correct clock, Tradeify k=1

| slice | n | WR | mean | net |
|---|--:|--:|--:|--:|
| EOD (held to close) | 322 | 74.8% | $181.53 | $58,454 |
| stopped out | 180 | 0.0% | −$281.46 | −$50,663 |

The construct is low-WR / high-R at the day level: a minority of held-to-close days carry it, and
stop-outs are a fixed −1R by construction (stop = opposite OR extreme, so mean stopped ≈
−(mean OR range × $2 + RT)).

---

## 4. Caveats (each load-bearing)

1. **Trail episodes are an EOD-proxy, so every bust/episode figure here is a LOWER BOUND.** The
   2026-07-30 primary-source read established that Tradeify enforces the drawdown breach
   **in real time**, not at end of day (`STATE.md` pointer log 2026-07-30). A path that touches the
   floor intraday and closes above it is invisible to this scorecard. This bites a held-to-close
   construct harder than a bracketed one.
2. **Not a Stage-7/8 substitute.** Full-window Tradeify DSR already **FAILED** at $0.91/side
   ([`RESULTS_stage7.md`](RESULTS_stage7.md)); only 2021+ carries cushion. This is sizing geometry,
   not a confirm gate, and it re-scores no gate.
3. **Panel ends 2026-07-15**, the TV export ran to 2026-07-30 — the ~2y rows are not a
   like-for-like row match to the published table (n=502 vs 513).
4. **Engine ≠ Pine.** The harness's stop test scans `rest_tods` (the documented inherited
   approximation) and resolves same-bar both-extremes touches by the open-vs-midpoint rule, where
   Pine uses its intrabar path assumption — the 96.9% per-trade parity measured 2026-07-21. Exit
   *counts* between this table and the TV table are therefore not expected to match exactly.
5. **No k policy is frozen by this run**, and the operator TV paste + 16:00 re-export is still
   owed as the conformance confirmation. What has changed is that it is **no longer a blocker for
   reading k geometry** — and §1 predicts what it will show.

---

Reproduce:

```bash
.venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_v02_native_clock_kgrid.py
```
