# PREREG — proposed new input for ORB-MYM-1 v0.4 (P50 build): OR-range risk budget

**Frozen:** 2026-09-02, before any scoring of this rule. Construct under test = the P50 export
`ORB-MYM-1_v0.4_CBOT_MINI_MYM1!_2026-09-02_49508.csv` (Pine SHA-256 `9292bd4e…`, 385 traded days,
qty 2/leg, up to 2 adds, SL 2.5×ORR, Mon/Thu/Fri). Informal Downloads lane; K disclosed.

## Mechanism (from the Pine + the trade list, not from P&L-by-feature)
- Stop distance = 2.5 × ORR; add steps = k × 0.07 × ORR; all legs share the base stop. So the
  planned worst-case loss of a full day ≈ **3 legs × 2.5 × ORR × $0.50 × qty** — it scales with
  the opening range; the Tradeify rope ($3,000 Select / $3,500 Growth) does not.
- Trade list: 63% of days carry 3 legs; the 8 worst and 5 best days are 2–3-leg days; 5 of the 8
  worst are Hot (P80 overnight range ⇒ wide OR, P(wide|Hot)=0.76 yesterday). The realized path
  busts Select on day 42 = **2020-02-28** (COVID week: −$384, −$775/contract on 02-24/02-27,
  intraday MAE through the trail). Worst day 2020-03-20: −$1,424/contract, MAE −$1,440.
- The Pine already documents the arithmetic in the `qty` tooltip ("SL 2.5x ORR ≈ $220/contract at
  median ORR") but sizes in fixed contracts. Fixed-contract sizing on an ORR-scaled stop is the
  same defect class as the CFD-era `contractValue` trap: the $ risk per trade is not what the
  input implies.

## Proposed input
`riskBudgetUsd` (default frozen here at **$1,500 = 50% of the Select rope**), evaluated at the OR
close (09:45 ET, before the entry order is armed — ex-ante, no lookahead):

    plannedRiskPerContract = (1 + maxScaleIns) * stopLossMult * orRangeToday * syminfo.pointvalue
    qtyToday = min(qty, floor(riskBudgetUsd / plannedRiskPerContract))   // 0 ⇒ skip the day

Direction fixed by construction (risk parity on the stop). Not reactive: it never cuts an open
position, so it does not touch the right tail the `skewed-strategy risk overlays backfire`
lesson protects.

## Counterfactual (exact)
Every leg shares `qty`; commission is per contract ⇒ day P&L and MAE at qtyToday =
(qtyToday/2) × the export's day values; qtyToday=0 ⇒ flat. ORR from the 09:15 and 09:30 ET bars
(union range) of the long BAR EXPORT (`…_2026-09-01_1b59b.csv`, 2019-05→2026-07-31) so Jan–Jun
2020 is covered; days after 2026-07-31 unscored.

## Cells (canonical engine: `core/mc/simulation.py`, seeds 1-3 × 4,000, intraday-honest, 5-day
blocks, protection off, Select consistency 0.40 / Growth none; common window = days with ORR)
- base q1-flat, base q2-flat (reference)
- **primary:** budget $1,500
- disclosed neighbors: budget $1,000, budget $2,000
- disclosed variant: hard cap only (keep qty 2, skip if plannedRisk(q2) > $1,500) — isolates the
  skip component from the downsizing component
- disclosed: budget $1,500 with base qty 1 (i.e. the rule at half scale)
K_this_test = 5 looks (1 primary + 4 disclosed). Cumulative on this construct family ≈ 35.

## Decision rule (frozen)
Recommend for a TV-native A/B iff the primary cell is **not dominated** by q1-flat or q2-flat on
(bust%, pass%) on **both** tiers, and median days-to-pass is not worse than q1-flat by more than
25%. Otherwise: report, no recommendation. Neighbors are never promoted over the primary.

## Limits
In-sample on a fully seen panel; MAE proxy is trade-level; Mon/Thu/Fri schedule inherited;
Off/P80 comparison cells remain screenshot-only (not re-derived here).
