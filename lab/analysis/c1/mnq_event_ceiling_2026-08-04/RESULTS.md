# MNQBASE-1 Step 1 — RESULTS: the independent-event ceiling on MNQ

**Status:** RESOLVED — frequency is NOT structurally constrained on MNQ: the ceiling is 145–1,172 disjoint events/day against a target of 3, so the base-construct bottleneck is mechanism-side, not instrumental; the incumbent book captures ~0.24% of the widest-stop ceiling

**Date:** 2026-08-04
**Pre-registration:** [`PREREG.md`](PREREG.md) — frozen at commit `1eeb35c`, **before any event count
existed**.
**Cost:** **$0.00** (MNQ 1m already on disk) · **K=0** · **no manifest** · **Cap seat untouched**.
**Runner:** [`run_ceiling.py`](run_ceiling.py) · **20 unit tests**, hand-computed and passing
**before** the runner read a real bar.

---

## 1. Verdict — `RESOLVED`, by a margin that is itself the finding

`MNQ.v.0` 1m, 2,553,405 bars → 2,453,286 in-session → **1,875 sessions**, of which **1,672** are
scored (roll-window and short sessions dropped).

| stop `s` (pt) | `G` (pt) | median events/day | p25 | p75 | mean | % of days ≥ 3 | qty @ $275 risk |
|---|---|---|---|---|---|---|---|
| 2 | 2.21 | **1,172** | 1,019 | 1,280 | 1,105 | 100.0% | 68.8 |
| 5 | 3.41 | **953** | 768 | 1,151 | 925 | 100.0% | 27.5 |
| 10 | 5.41 | **676** | 496 | 901 | 695 | 100.0% | 13.8 |
| 20 | 9.41 | **364** | 237 | 553 | 418 | 100.0% | 6.9 |
| **40** | **17.41** | **145** | 83 | 248 | 191 | **99.9%** | 3.4 |

**Max median over the grid = 1,172/day against a target of 3.** C4 fires: the target is cleared at
every cell including `G ≥ 5.41`, so this is `RESOLVED` rather than the `AMBIGUOUS` case where only
un-holdable tight stops reach it. **Even the widest stop — 40 points, the most credible for T4 (hard
stops that hold) — clears 3/day on 99.9% of sessions.**

**Parent falsifier L1 does not fire.** A single-instrument MNQ construct is *not* structurally
barred from 3–8 independent trades/day.

---

## 2. The pre-registered expectation held — and the parent brief's did not

`MNQBASE-1` §4 called **L1 firing "the single most likely outcome"**, reasoning from the incumbent
book's 0.35 trades/calendar-day. `PREREG.md` §4 **corrected that before running**, on the ground
that realized *strategy* frequency and the *instrument* ceiling are different quantities, and
recorded that a high ceiling was the more likely result and **would not be a positive finding**.

That correction is dated and committed ahead of the measurement (`1eeb35c` precedes this file), so
the outcome is a discharged prediction rather than a retrofit. **Restating it because the number is
large enough to be misread: 1,172/day is not a discovery. It is the removal of one hypothesis.**

---

## 3. What this actually establishes — and the ~0.24% that follows

The single decision-relevant quantity:

| | events/day |
|---|---|
| Ceiling at the widest stop (40 pt) | **145** |
| Target (shape spec T2) | 3–8 |
| **Incumbent c1 book, realized** | **0.35** |

**The incumbent captures roughly 0.24% of the disjoint opportunities available at its own risk
scale.** The gap between 0.35 and 145 is not an instrument limitation — it is entirely the
mechanism's inability to identify *which* windows to take. That relocates the base-construct
problem precisely:

> **We are not short of opportunities. We are short of a rule that selects profitable ones.**

Every prior MNQ campaign optimized per-trade edge and treated frequency as whatever fell out. This
says the frequency axis has enormous headroom and was never the binding constraint — so a construct
that fires 3–8×/day is *available in principle* at any stop level on the grid.

---

## 4. Scope limits — read before citing any number

1. **A range window is not a tradeable capture.** This grants perfect direction, perfect timing, and counts a *range* rather than a realized directional move from a specific entry. It is a **strict upper bound and only that** (PREREG §1, FM-5). Nothing here says a profitable construct exists.
2. **`RESOLVED` licenses no candidate** (FM-1). It removes a hypothesis; it opens nothing. The gap between this bound and any realizable strategy *is* the entire remaining problem.
3. **The tight-`G` cells are near-degenerate and should not be quoted.** At `G = 2.21` the median is 1,172 events across a ~1,320-minute session — roughly one per 1.1 minutes, i.e. close to "count the bars." **The `s = 40` row (145/day, one per ~9 minutes) is the only cell with real discriminating power**, and it is the one to cite. The verdict does not depend on this: C4 requires a `G ≥ 5.41` cell, and the 40-pt cell clears 3/day by 48×.
4. **The margin is so wide that the measurement has little resolving power.** It was designed to fire L1 cheaply if L1 were going to fire. It did not, and a bound 48× from its threshold cannot distinguish between "plenty of room" and "vastly too much room" — nor does it need to.
5. **Counting rule is marginally conservative.** Per the frozen §2, a booked event consumes its boundary bar (`restart at j+1`) rather than sharing it with the next window. At 1m granularity this is immaterial, and it errs toward *under*-counting — the safe direction for an upper bound.
6. **One instrument, one geometry.** MNQ only, sessions cut 18:00→16:00 ET. The `G` grid is derived from the 0.40R threshold and the **Tradeify $0.91/side** basis; another firm's basis shifts `G` slightly and would want a re-run (~seconds, $0).

---

## 5. Disposition (discharging the pre-registered §6 branch)

**Verdict used:** `RESOLVED` (C4)
**Model update:** the base-construct problem was framed as "can MNQ support the required
frequency?" It cannot be that — the ceiling exceeds the requirement by 48× at the most conservative
stop. The correct framing is **selection**: which of ~145 daily disjoint windows carry edge, and can
a rule identify them ex ante. The incumbent's 0.35/day is a statement about our rules, not about MNQ.

**Next: `ITERATE` → the parent brief's Step 2** — the branch §6 pre-registered for `RESOLVED`,
discharged as frozen.

**Entry packet for Step 2:** this per-`G` curve (cite the `s = 40` row, per §4.3); the ceiling-vs-
realized ratio in §3; T1–T7 unchanged; and the §2.3 pre-filters P1–P6, which are **not** loosened by
this result — in particular **P1 (edge < 0.40R) still kills on arithmetic**, and a large ceiling
makes P1 *more* important, not less, because abundant opportunities plus no edge is exactly the
§2a inversion trap (more trades at a thin edge makes the rope geometry worse).

**Stop rule:** none — `RESOLVED` routes forward. If Step 2's intake comes back dry, that is the
parent's **L2**, and it is a legitimate verdict.

**Board write:** `STATE.md` decision-index line; `SESSIONS.md` entry; MNQ ledger durable finding.

---

## 6. Reproduce

```bash
python -m pytest lab/analysis/c1/mnq_event_ceiling_2026-08-04/ -q     # 20 passed
python lab/analysis/c1/mnq_event_ceiling_2026-08-04/run_ceiling.py <mnq_1m.parquet>
```

Data (gitignored, regenerable at $0.00 — estimate first, always):

```bash
python lab/databento_fetch/db_fetch.py estimate --symbols MNQ.v.0 --stype continuous \
  --schema ohlcv-1m --start 2019-05-06 --end 2026-08-04 --phase oos
```

**One test bug caught before the runner read real data** (mine, in the test): the disjointness test
asserted that a 5-bar monotone climb yields 2 events at `G=2`, assuming adjacent windows could share
their boundary bar. The frozen §2 rule says *"restart the window at `j+1`"* — the boundary bar is
consumed by the window that closed — so the correct answer is 1 and the code was right. Fixed the
test rather than the code, and added a complementary 7-bar fixture that does yield 2, so both the
restart and the disjointness properties are pinned.
