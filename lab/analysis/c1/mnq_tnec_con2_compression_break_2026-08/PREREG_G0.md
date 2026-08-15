# Q-TNEC-CON-2 — Stage-0 PREREG (G0) — dense 1m compression→expansion break

**Status:** `FROZEN` 2026-08-09 — ENTRY named; explore GO unpaid; Cap seat not claimed.
**Date:** 2026-08-09
**Parent brief:** [`docs/briefs/Q-TNEC-CON-2-compression-expansion-break-scoping.md`](../../../../docs/briefs/Q-TNEC-CON-2-compression-expansion-break-scoping.md)
**Lane:** [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../../../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
**Intake gate:** [`TNEC-1`](../../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) (`RATIFIED`) — N-ACT…N-SIZE
**Universe unlock:** [`Q-MNQSEL-2` RESOLVED](../mnq_selection_ceiling_allbars_2026-08/RESULTS.md) — dense RTH 1m @ G=10
**Prior campaign:** [`Q-MNQDTL-CON-1` FALSIFIED STOP](../../../../docs/briefs/closures/Q-MNQDTL-CON-1-closure-falsified.md) (ES/NQ divergence)
**`K_intrinsic = 1`**. Cap 1.0 → DSR floor **0.650**.
**Cost so far:** **$0.0000** (MNQSEL-2 `_mnq_1m.parquet` reuse).

**FROZEN ON THIS FILE'S INTRODUCING COMMIT.** Zero EXPLORATION path scores at freeze
(cheap falsifier = parent panel run only — see [`ADMISSION_FALSIFIER_LOG.md`](ADMISSION_FALSIFIER_LOG.md)).

---

## §0 — Rule-0 / cheap falsifier (parent-side, 2026-08-09)

| Check | Result |
|---|---|
| MNQ panel | `lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet` |
| Family A (displacement fade) | `FALSIFIED` at $0 / no Q-ID — [`_cheap_falsifier_displacement_fade_2026-08-09_LOG.md`](../cheap_falsifiers_2026-08/_cheap_falsifier_displacement_fade_2026-08-09_LOG.md) |
| Family B (this cell) | `CHEAP_FALSIFIER_OK` — long mean R −0.053 CI [−0.148, +0.044]; short −0.078 CI [−0.189, +0.039]; n≈5k/arm — [`_cheap_falsifier_compression_break_2026-08-09_LOG.md`](../cheap_falsifiers_2026-08/_cheap_falsifier_compression_break_2026-08-09_LOG.md) |
| EM1 / N-EDGE arithmetic | Pred. move ≥ **5.41** / **1.41** pt; WR bars **0.7705** / **0.5705** (disclosure) |
| Sign | **With-break** frozen; do not invert to fade (would collide with killed Family A) |
| ENTRY | Named, causal at bar open, ≠ oracle |

**Verdict:** `CHEAP_FALSIFIER_OK` — licenses G0 freeze + harness scaffold; **not** SHAPE-CLEAR.
Point estimates are negative; CIs straddle 0 so the generous kill did not fire. Explore remains GO-gated.

---

## §1 — Universe and trade geometry

| Element | Frozen value |
|---|---|
| Clocks | CME equity-index **RTH** Mon–Fri **09:30–15:59 ET** 1m bar opens |
| Trade instrument | `MNQ.v.0` continuous (MNQSEL-2 panel) |
| Roll exclusion | `in_roll_window` (±4 days of 3rd Friday Mar/Jun/Sep/Dec) |
| Stop | **G = 10.0 pt** hard adverse; same-bar stop wins |
| Exit | **Session-flat** at last in-session RTH bar close |
| Cost | Tradeify RT **1.41 pt**; `R = (pts − 1.41) / 10` |
| Independence | EM3 — one position at a time; no pyramid/scale-in |
| Arms | Long and short **separate** for gate stats |
| K | `K_intrinsic = 1` — one named cell |

---

## §2 — Catalogue cell C1 — ENTRY (causal; all constants a priori)

Inputs at each RTH 1m bar open `t` (known at `t`, no path foresight):

```
med_rng(session) = median(bar ranges) over trailing 20 completed RTH sessions
narrow(i)        = (high[i]-low[i]) > 0 and (high[i]-low[i]) <= 1.0 * med_rng
compression      = narrow(t-3) and narrow(t-2)     # K_NARROW=2 bars ending at t-2
quiet_hi/lo      = max/min high/low over those two bars
break_bar        = bar t-1
```

Signal at open of `t`:

| Condition | Action |
|---|---|
| compression ∧ close[t-1] > quiet_hi (and not also &lt; quiet_lo) | enter **LONG** MNQ at open[t] |
| compression ∧ close[t-1] &lt; quiet_lo (and not also &gt; quiet_hi) | enter **SHORT** MNQ at open[t] |
| otherwise | no trade |

While in a position, further signals ignored until session-flat or stop (EM3).

**Frozen constants (do not retune on scored data):** `K_NARROW=2` · `NARROW_MULT=1.0` ·
median window **20** sessions · break = **close** beyond quiet range · sign = **with-break**.

**Mechanism (disclosure):** short-horizon volatility compression concentrates resting
interest; the first close outside the quiet range is treated as expansion initiation.
Not ES/NQ residual (CON-1). Not ORB (not opening-range). Not Family A fade.

**Closed-door clearance (class, not a re-score):**
- ≠ CON-1 ES/NQ divergence
- ≠ ICT C1–C4 · ≠ C5 Baltussen momentum catalogue · ≠ C6 opening-pressure
- ≠ ORB / ORB gates C7 · ≠ ORB exit redesign C8
- ≠ L1/depth C9/C11
- ≠ C10 level-attraction/reaction screen (`prior_rth` / pivots / fib / camarilla / ATR bands / VWAP — MNQSR-1). This cell is a **compression-then-break entry**, not a level-touch attraction test. Adjacency disclosed; not a C10 parameter reopen.

---

## §3 — Scoring (EXPLORATION only; after operator GO)

Per arm (long / short separate):

| Limb | Definition |
|---|---|
| Primary | Mean net R; session-block bootstrap **95% CI** must exclude 0 (trade-weighted: resample sessions → concat trades → mean) |
| Placebo | Within-session R-shuffle **1000** reps; seed **20260809** |
| Halves | Older/newer EXPLORATION session-date halves; sign disagree → `VOID` / AMBIGUOUS-HOLD |
| DSR | ≥ **0.650** at `K_intrinsic=1` |
| Disclose | WR · max adverse/favorable excursion · trades/session · coverage · EM six-char |

**Gate:** `SHAPE-CLEAR` / `FALSIFIED` / `VOID` as specified at explore GO.
**TNEC verdict string** (unscored limbs typed **U** until their GO):

```
N-ACT N-SURV N-EDGE N-SHAPE N-SIZE | bust | P(pass) | μ(disclosed)
```

At G0 freeze (pre-explore): all five N-* limbs are **U**; bust / P(pass) / μ are `U`.

**Deferred:** full N-SURV MC · Cap claim · ORB unpark · Pine/rail · elevating D1/D2 ·
retuning K_NARROW / NARROW_MULT / G · sign invert to fade.

---

## §4 — Explore path

1. Stage-0 freeze (**this file**) — DONE when committed (Rule 8.7).
2. Operator **explore GO** — unpaid at freeze; cache reuse only.
3. `run_construct_g0.py` refuses real-panel path PnL unless `EXPLORE_GO.md` exists
   **and** `--explore-go` is passed.
4. First scored run = EXPLORATION only. CONFIRM unread.

---

## §5 — Forbidden moves

- Retuning `K_NARROW` / `NARROW_MULT` / median window / G / exit after freeze.
- Inverting to fade-the-break (Family A killed; also C5-adjacent if re-cast as momentum fade games).
- Path-scoring real bars before explore GO.
- Oracle / completed-window ranking; OF ρ as substitute entry; ORB filter laundering (F2).
- Claiming Cap from this packet alone; Pine/deploy/arming; C10 reopen via level-family retune.
