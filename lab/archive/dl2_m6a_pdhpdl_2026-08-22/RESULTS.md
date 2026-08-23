# DL-2 (M6A-PDHPDL) -- TRAIN scoring RESULTS

**Status:** `AMBIGUOUS` -- ABANDONMENT (prereg roster mapping: confirm never read, nothing
was tested).

**Prereg:** [`docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md`](../../../docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md)
**Charter:** [`docs/adr/2026-08-16-deep-iteration-lane-charter.md`](../../../docs/adr/2026-08-16-deep-iteration-lane-charter.md)
**Handoff:** [`docs/briefs/rnd-pipeline/2026-08-22-cc-handoff-dl2-m6a-step2-train-scoring.md`](../../../docs/briefs/rnd-pipeline/2026-08-22-cc-handoff-dl2-m6a-step2-train-scoring.md)

## Sec6 step 2 -- TRAIN + nomination

All 10 frozen variants (Sec2) scored on 6A.FUT TRAIN (2010-06-06 -> 2019-01-01, 2,200
Globex sessions, 2,815,486 stitched 1-minute bars; 35 UTC roll days -> 35 roll sessions
excluded from entries). All 10 net-negative on TRAIN.

| V | Lookback | Drift | Style | Target | n | net annSR | trades/wk | median stop (ticks) | cost-law ratio |
|---|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | 1 | unconditional | close_confirm | 2R | 1811 | -1.6100 | 4.050 | 82.0 | 12.62 |
| 2 | 1 | unconditional | close_confirm | 3R | 1811 | -1.6104 | 4.050 | 82.0 | 12.62 |
| 3 | 1 | aligned | close_confirm | 2R | 1364 | -1.6121 | 3.050 | 84.0 | 12.92 |
| 4 | 1 | aligned | close_confirm | 3R | 1364 | -1.6220 | 3.050 | 84.0 | 12.92 |
| 5 | 2 | unconditional | close_confirm | 2R | 1500 | -1.2596 | 3.355 | 116.0 | 17.85 |
| 6 | 2 | unconditional | close_confirm | 3R | 1500 | -1.2750 | 3.355 | 116.0 | 17.85 |
| 7 | 2 | aligned | close_confirm | 3R | 1179 | -1.3654 | 2.637 | 121.0 | 18.62 |
| 8 | 1 | aligned | retest_limit | 2R | 1327 | -0.8471 | 2.968 | 80.0 | 12.31 |
| 9 | 2 | aligned | retest_limit | 3R | **1144** | **-0.6840** | 2.558 | 118.0 | 18.15 |
| 10 | 1 | unconditional | retest_limit | 2R | 1752 | -0.7580 | 3.918 | 79.0 | 12.15 |

Nominee = **V9** (2-session lookback, drift-aligned, retest-limit, 3R target) -- argmax
train net annSR, no fallback, no walk-down, per Sec6. No argmax tie (checked).

| Gate | Result |
|---|---|
| 2a cost-law (net annSR > 0 AND ratio >= 4x at realized geometry) | **FAIL** -- net annSR -0.6840; ratio 18.15x (passes alone) |
| 2b SPA (Hansen, consistent p <= 0.10, full 10-variant universe, block=20, B=10000, seed=11) | **FAIL** -- p = 0.9755 |
| 2c N-ACT cadence (>= 1 trade/week) | PASS -- 2.558/wk |
| 2d M-16 (+1 tick/side additional slip, net annSR > 0) | **FAIL** -- net annSR -0.9185 |

**Verdict:** nominee fails 3 of 4 nomination gates -> **ABANDONMENT** (dated, no strike
against the lane's 2-campaign falsification budget, per prereg Sec4 / charter Sec4(c)).
Confirm partition (M6A.FUT) never read, per Sec5 forbidden moves.

**This is DL-2's own abandonment, the 2nd consecutive after DL-1 -- charter Sec4(c)'s
audit-report duty has now tripped** (2 consecutive abandonments), owed at the next
quarterly programme audit.

**Diagnostic note (disclosed, not a code defect -- ruled out by direct inspection before
accepting this verdict).** All 10 variants show win rates in a sensible 42.6%-46.6% band,
balanced long/short splits (~50/50 every variant), and `net = gross - n * $2.60` reproduces
exactly for every variant checked -- no evidence of a sign/direction defect. The structural
driver of the uniform negativity: 85-90% of trades exit via `force_flat`, not stop or
target (e.g. nominee V9: 1091/1144 = 95.4% force-flat, only 53 stops, 0 targets). The
prior-session-derived stop/target geometry (median stop ~80-130 ticks, target 2-3x that) is
wide relative to how far price can travel in the remainder of a single Globex session
before the next day's 16:55 ET force-flat -- so almost no trade ever resolves to a real R
multiple; realized P&L is close to a small, cost-negative directional residual on the
un-resolved bars. This is a property of the frozen construction (1-session holding period
vs. a full-prior-session-range-derived stop), not a signal that the mechanism itself lacks
directional information -- disclosed per Sec2.4's own instruction ("that's a
`DONE_WITH_CONCERNS` flag for the operator, never a silent in-flight edit") rather than
silently patched.

Full per-variant table (all 10 variants' net annSR, cadence, cost-law ratio) and gate
detail: [`train_results.json`](train_results.json). Engine: `stitch.py` / `engine.py` /
`score.py` / `variants.py` / `run_train.py`; unit-tested against hand-constructed synthetic
slices ([`test_units_synthetic.py`](test_units_synthetic.py), all (a)-(e) gates pass,
including a known synthetic roll day correctly skip-back'd and a known synthetic
break-and-hold reproducing the exact hand-worked R multiple) before the full TRAIN run.
