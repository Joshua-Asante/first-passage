**Verdict:** NULL — daily close-vs-EMA20 bias carries nothing at daily granularity (Tier-1 screen, 3 of 4 limbs failed; K=1 disclosed)
**Theme:** _inbox
**Status:** ACTIVE — NULL: daily close-vs-EMA20 bias carries nothing at daily granularity (Tier-1 screen, 3 of 4 limbs failed; K=1 disclosed)
# `H-DSTRUCT-MNQ-1` — RESULTS: daily structural bias carries nothing at its own granularity

**Date:** 2026-08-18 · **Verdict: `NULL`** (per the frozen §4 gate — limbs 2, 3 AND 4 all failed)
**Pre-registration:** [`PREREG_DSTRUCT.md`](PREREG_DSTRUCT.md), written before any number existed.
**Spend:** $0.00 · K=1 (disclosed, one frozen object) · no manifest · no pull · no candidate.
**Panel:** `_mnq_15m.pkl` sha256 `81c05e9a…` (matches Q-SESSCONF-1 pin), session-days
2019-05-06 → 2026-07-15 (already-read boundary; reserved windows untouched).
**Runner:** [`run_dstruct.py`](run_dstruct.py) · full JSON: [`dstruct_results.json`](dstruct_results.json).

## 1. Headline

Object: `b_d = sign(close_{d−1} − EMA20)` on daily session bars → day *d* direction.

| | verdict: RTH open→close | disclosure: close-to-close |
|---|---|---|
| scored days | 1,833 | 1,836 |
| `gateHit` | **0.5183** | 0.5185 |
| block-CI 95% | [**0.4954**, 0.5412] — straddles 0.50 | [0.4973, 0.5414] |
| halves | (**0.4978**, 0.5387) — h1 below 0.50 | (0.5185, 0.5185) |
| placebo mean / p95 / p | 0.5152 / 0.5325 / **p=0.40** | 0.5211 / 0.5392 / p=0.62 |
| closed-form base rate | 0.5160 | 0.5201 |
| limbs passed | **1 of 4** (n-floor only) | 2 of 4 |

The measured 51.8% sits *inside* its own base-rate arithmetic (51.6% from the marginals:
f(+1)=0.682 × P(up)=0.544). Unlike leg (b) — which passed every naive limb and needed the
placebo — this doesn't even clear the CI or halves limbs. **The daily bias is weaker than the
weekly bias was, exactly as the noise-scaling expectation predicts.**

## 2. The load-bearing decomposition: the bearish arm has ZERO information at daily scale

| Prior-day bias | n | up-rate (O→C) | vs unconditional 0.5439 |
|---|---|---|---|
| +1 | 1,250 | 0.5456 | +0.17 pp |
| **−1** | 583 | **0.5403** | **−0.36 pp** |

The weekly bias at least had a real bearish arm (−3.16 pp, a "be less long" license).
The daily bias has **nothing on either side** — after a below-EMA close, the next day is up at
essentially the unconditional rate. Close-to-close, the bearish arm is even fractionally
*more* up (0.5575 vs 0.5550). There is no "less long" license here, let alone a short one.

## 3. Prediction check (frozen §5)

- Expected NULL → **held**. f(+1)=0.682 → inside the frozen 0.60–0.80 band.
- One miss, disclosed: O→C up-rate came in 0.5439, above the frozen 0.49–0.53 guess — modern
  MNQ carries more *intraday* drift than assumed. Doesn't touch the verdict (the placebo and
  closed form both condition on the measured marginals, not the guess).

## 4. Disposition

**`NULL` → STOP** (the §5 frozen branch). No second `emaLen`/horizon/lag/instrument — that
sweep is the K this declaration excluded, and the §6 forbidden moves bar it.
**Model update:** structure-persistence of the close-vs-EMA form exists at the **weekly** close
(leg (a), three panels) and degrades monotonically downward: weekly→daily transfer null
(Q-WLEGB-1), daily-native null (this), with the per-side information vanishing entirely at
daily scale. The regularity is a weekly-bar fact, full stop.
**Routing:** the Step-0 mechanism slate proceeds with **geometry/level-class daily structure
on the non-index triad** (range/level regularities, not direction prediction) — direction-type
daily structure on index micros now has four independent kills against it (N5 intraday
momentum, Q-WLEGB-1, SIZEDIV-F3 relabel, this).
**Re-proposal bar:** a daily-structure *direction* screen on MNQ re-opens only with a named
mechanism (who is constrained to trade the wrong way at daily horizon and why) — not another
indicator functional over the same daily OHLCV.

## 5. Scope limits

MNQ only; one frozen `emaLen=20`; O→C convention uses `orb_lib.session_panel` RTH bounds
(holiday half-days close at their actual last bar); measurement-only — no outcome here
promotes or blocks anything outside the daily-EMA-direction family.
