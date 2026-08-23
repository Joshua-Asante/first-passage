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

## Iterate — loop exit (canon `docs/methodology/inqhiori-canon.md` §16; mandatory per
`docs/adr/2026-08-04-iterate-closure-exit-mandatory.md`; added retroactively 2026-08-22 — the
disposition-enforcement gap this closure had sat behind was named and fixed the same session
as DL-2's own closure, see that file's Change history)

- **Verdict used:** `AMBIGUOUS` — ABANDONMENT (prereg roster mapping; confirm never read,
  nothing tested).
- **Model update:** Reconciled 2026-08-22 (prompted by a sanitized ox-alpha second
  opinion sought on DL-2's own closure, per `docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md`,
  which raised the question of whether DL-1's and DL-2's abandonments share one root cause).
  Re-ran this archived harness and computed the exit-reason mix for all 10 variants: 40–70% of
  trades resolve to a genuine stop or target (nominee V7: 35% stop, 5.7% target, 59%
  force-flat) — a materially different resolution profile than DL-2's own 85–95% force-flat
  dominance. **Confirmed: this is a candidate-level failure** (an adverse stop:target
  hit-rate ratio at the frozen 3R target — win rates 34–40% against what a 3R payout needs to
  break even), not a construction/holding-period mismatch. This decouples DL-1 from DL-2: they
  are two independent abandonments, not two symptoms of one shared deep-iteration-lane
  template defect, contrary to a hypothesis raised (and refuted) while reflecting on the pair.
- **Next:** `STOP`
- **Routing:** the `opening-range-continuation` construct on GC/MGC is dead on its own
  candidate-level merits, confirmed above — not a template flaw a construction fix could
  rescue. No successor is named.
- **Entry packet:** n/a (`Next` = `STOP`).
- **Stop rule / re-proposal bar:** re-opening `opening-range-continuation` (this mechanism id,
  any instrument) needs new *mechanism* evidence — a stated reason to expect the realized
  win-rate/target-ratio mismatch resolves — not a retuned OR-window/target parameter within the
  same 10-variant family shape (`docs/rejected_candidates.md`'s standing convention).
- **Board write:** none — `STOP`, nothing owed. (The live forward obligation from this
  reconciliation lives on DL-2's own Iterate block and its `STATE.md` pointer, since DL-2's
  construction — not DL-1's — is the one carrying an open, untested-for-generality risk.)

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-16 | RESULTS.md authored; §6 step 2 closed ABANDONMENT | Claude Code (train-scoring session) |
| 2026-08-22 | Iterate block added retroactively (canon §16); exit-reason mix re-computed and reconciled against an ox-alpha hypothesis raised on DL-2's own closure — confirmed candidate-level, not shared-template | Claude Code (DL-2 train-scoring session) |
