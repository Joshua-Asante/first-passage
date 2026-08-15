# MSL-S2A — EXPLORATION RESULTS (G0)

**Status:** `FALSIFIED` (N-ACT: measured trades/week &lt; 1)
**Date:** 2026-08-13 · **Cost:** $0.00 · **K:** disclosure only (`K_intrinsic=1`).
**Explore GO:** ISSUED 2026-08-13 (gitignored `EXPLORE_GO.md`; draft
[`EXPLORE_GO.DRAFT.md`](EXPLORE_GO.DRAFT.md)).
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [closure](../../../docs/briefs/closures/MSL-S2A-closure-falsified.md)
**Machine record:** [`RESULTS.json`](RESULTS.json)
**Panel:** `core/data/bar_data/MCL_M15.csv` sha256 `5aa504567b943ff68506b8b5c21df293c5a553543fdf1ac606adeb0f5bfbbd23`

## Headline (EXPLORATION = sessions ≤ 2025-06-30; CONFIRM reserved unread)

| Arm | n | mean net R | WR | session-block 95% CI | annSR | halves (older/newer) |
|---|---|---|---|---|---|---|
| Long | 31 | **−0.1749** | 0.355 | [−0.4639, 0.1438] | −0.64 | −0.172 / −0.177 |
| Short | 46 | **−0.0769** | 0.435 | [−0.2867, 0.1455] | −0.40 | −0.164 / +0.026 |

753 IS sessions scored · 77 with a trade · **trades/week 0.511** (N-ACT solo fail) ·
mean stop ≈ 0.813 / 0.793 pt · gross vs 4×RT (disclose) ≈ 4.93× / 4.81× at mean stop
(1R USD vs $16.48). Placebo p_emp 0.263 / 0.489. Qty=2 disclose-only.
**TNEC:** `F U U U U | U | U | L-0.1749/S-0.0769`.

## Gate walk

- **FALSIFIED?** Yes — measured trades/week **0.511 &lt; 1** (N-ACT). Both-arms CI-upper&lt;0
  did **not** fire (n 31/46 &lt; 100; both CI hi &gt; 0).
- DELETE: **PASS** both arms (sham mean more negative: long −0.643 vs −0.175; short −0.312 vs −0.077).
- FLIP: **FAIL** long (join-pullback +0.047 &gt; resume −0.175); **PASS** short (−0.077 vs −0.081).
  Long FLIP-FAIL ⇒ that arm is not SHAPE-CLEAR; co-fires with N-ACT (not cadence-only).
- Aux live-pass: neither arm (placebo p ≥ 0.05; annSR &lt; 0.650; short halves disagree).
- → **`FALSIFIED`**. CONFIRM unread; Cap unclaimed; Pine unpaid.

## What this run does NOT license

Reading CONFIRM · Cap claim · Pine/TV/B5 · θ retune (impulse/pullback/stop buffer/rr/k/window) ·
instrument hop · treating DELETE PASS as a surviving continuation edge · `BOOK-CONDITIONAL(cadence)`
(FLIP FAIL + negative means co-fire) · arming.
