# DL-1 (MGC-ORC) — TRAIN scoring RESULTS

**Status:** `AMBIGUOUS` — ABANDONMENT (prereg roster mapping: confirm never read, nothing
was tested).

**Prereg:** [`docs/briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md`](../../../docs/briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md)
**Charter:** [`docs/adr/2026-08-16-deep-iteration-lane-charter.md`](../../../docs/adr/2026-08-16-deep-iteration-lane-charter.md)

## Sec6 step 2 — TRAIN + nomination

All 10 frozen variants (Sec2) scored on GC.FUT TRAIN (2010-06-06 -> 2019-01-01, 2,168 CME
trading sessions, 2,947,410 stitched 1-minute bars). All 10 net-negative on TRAIN.

Nominee = **V7** (60-min OR, drift-aligned, breakout, 3R target) — argmax train net annSR,
no fallback, no walk-down, per Sec6.

| Gate | Result |
|---|---|
| 2a cost-law (net annSR > 0 AND ratio >= 4x) | **FAIL** — net annSR -0.4203; ratio 5.05x (passes alone) |
| 2b SPA (Hansen, consistent p <= 0.10, full 10-variant universe) | **FAIL** — p = 0.9386 |
| 2c N-ACT cadence (>= 1 trade/week) | PASS — 2.99/wk |
| 2d M-16 (+1 tick/side additional slip, net annSR > 0) | **FAIL** — net annSR -0.6567 |

**Verdict:** nominee fails 3 of 4 nomination gates -> **ABANDONMENT** (dated, no strike
against the lane's 2-campaign falsification budget, per Sec4). Confirm partition (MGC.FUT)
never read, per Sec5 forbidden moves.

Full per-variant table (all 10 variants' net annSR, cadence, cost-law ratio) and gate
detail: [`train_results.json`](train_results.json). Engine: `stitch.py` / `engine.py` /
`score.py` / `variants.py` / `run_train.py` — adversarially verified against the frozen
prereg text (5-agent workflow) before this run.
