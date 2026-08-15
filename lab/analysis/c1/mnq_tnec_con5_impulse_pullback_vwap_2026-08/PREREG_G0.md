# Q-TNEC-CON-5 — Stage-0 PREREG (G0) — impulse→pullback→VWAP-reclaim

**Status:** `FROZEN` 2026-08-11 — ENTRY named; explore GO **paid** → [`RESULTS.md`](RESULTS.md) `AMBIGUOUS-HOLD`; Cap seat not claimed.
**Date:** 2026-08-11
**Parent brief:** [`docs/briefs/Q-TNEC-CON-5-impulse-pullback-vwap-reclaim-scoping.md`](../../../../docs/briefs/Q-TNEC-CON-5-impulse-pullback-vwap-reclaim-scoping.md)
**Lane:** [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../../../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
**Intake gate:** [`TNEC-1`](../../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) (`RATIFIED`)
**Mechanism id:** `impulse-pullback-vwap-reclaim` ([`MECHANISMS.md`](../../../../ops/instruments/MECHANISMS.md))
**Prior:** [`Q-TNEC-CON-4` AMBIGUOUS-HOLD → Branch B](../../../../docs/briefs/closures/Q-TNEC-CON-4-closure-ambiguous-hold.md)
**`K_intrinsic = 1`**. Cap 1.0 → DSR floor **0.650**.
**Cost so far:** **$0.0000** (MNQSEL-2 panel reuse).

**FROZEN ON THIS FILE'S INTRODUCING COMMIT.** Zero EXPLORATION path scores at freeze
(cheap falsifier = parent panel run only — see [`ADMISSION_FALSIFIER_LOG.md`](ADMISSION_FALSIFIER_LOG.md)).

---

## §0 — Rule-0 / cheap falsifier / domain bar (parent-side, 2026-08-11)

| Check | Result |
|---|---|
| MNQ panel | `lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet` |
| Domain bar | `python scripts/instrument_profiles.py cell MNQ impulse-pullback-vwap-reclaim` → BINDING BAR answered **route ①** |
| Family | `CHEAP_FALSIFIER_OK` — long +0.0061 CI [−0.284, +0.327]; short −0.4268 CI [−0.709, −0.095]; n=784/723; coverage 90.3%; mean stop ≈19.1 pt — [`_cheap_falsifier_impulse_pullback_vwap_2026-08-11_LOG.md`](../cheap_falsifiers_2026-08/_cheap_falsifier_impulse_pullback_vwap_2026-08-11_LOG.md) |
| Sign | **With-bias reclaim** frozen; do not invert to fade-to-VWAP |
| ENTRY | Named, causal at next 1m open after reclaim close; first/session |

**Verdict:** `CHEAP_FALSIFIER_OK` — licenses G0 freeze + harness scaffold; **not** SHAPE-CLEAR. Short arm already CI-entirely-negative on full panel (formal both-arm kill did not fire).

---

## §1 — Universe and trade geometry

| Element | Frozen value |
|---|---|
| Clocks | CME equity-index **RTH** Mon–Fri **09:30–15:59 ET**; signal clock = **1m** bars |
| Trade instrument | `MNQ.v.0` continuous (MNQSEL-2 panel) |
| Roll exclusion | `in_roll_window` (±4 days of 3rd Friday Mar/Jun/Sep/Dec) |
| Bias | First 30 RTH minutes; long iff close@09:59 > open@09:30; short iff &lt;; equal → skip |
| VWAP | Session cumulative typical-price VWAP from RTH open |
| Stop | **Pullback extreme** (tag→reclaim; long→min low; short→max high); same-bar stop wins |
| Exit | **Session-flat** at last in-session RTH bar close |
| Cost / R | Tradeify RT **1.41** pt; `R = (pts − 1.41) / stop_dist` |
| Independence | EM3 — one position; **first valid signal per session only** |
| Arms | Long and short **separate** for gate stats |
| K | `K_intrinsic = 1` |

---

## §2 — Catalogue cell C1 — ENTRY (causal; all constants a priori)

After bias window ends (10:00 ET):

| Condition | Action |
|---|---|
| Bias long · cleared (close > VWAP) · tag (low ≤ VWAP) · reclaim (close > VWAP) | enter **LONG** at open[t+1]; stop = min low tag→reclaim |
| Bias short · cleared (close &lt; VWAP) · tag (high ≥ VWAP) · reclaim (close &lt; VWAP) | enter **SHORT** at open[t+1]; stop = max high tag→reclaim |
| otherwise / already traded this session | no trade |

**Frozen constants:** 30m bias · session VWAP · first/session · pullback-extreme stop · with-bias reclaim · session-flat · RT 1.41.

**Closed-door clearance:** ≠ CON-1–4 through-break / compression · ≠ fade-to-VWAP · ≠ ORB · ≠ PDH/PDL · ≠ HTF-bias→LTF. Cost-geometry distinction: pullback-depth stop vs day-range / compression stops.

---

## §3 — Scoring (EXPLORATION only; after operator GO)

Per arm (long / short separate):

| Limb | Definition |
|---|---|
| Primary | Mean net R; session-block bootstrap **95% CI** must exclude 0 |
| Placebo | Sign-randomized R **1000** reps; seed **20260811** (declared at explore GO if runner gap) |
| Halves | Older/newer EXPLORATION session-date halves; sign disagree → VOID / AMBIGUOUS-HOLD |
| DSR | ≥ **0.650** at `K_intrinsic=1` |
| Disclose | WR · stop_dist · trades/session · coverage · gross pts vs 4×RT · EM six-char |

**Gate:** `SHAPE-CLEAR` / `FALSIFIED` / `VOID` as specified at explore GO.
At G0 freeze: all five N-* limbs **U**.

**Deferred:** confirm GO · Cap · Pine/rail · retune θ · sign invert · multi-signal/session.

---

## §4 — Explore path

1. Stage-0 freeze (**this file**) — DONE when committed (Rule 8.7).
2. Operator **explore GO** — unpaid at freeze; cache reuse only.
3. `run_construct_g0.py` refuses real-panel path PnL unless `EXPLORE_GO.md` exists **and** `--explore-go` is passed.
4. First scored run = EXPLORATION only. CONFIRM unread.

---

## §5 — Forbidden moves

- Retuning bias window / VWAP definition / first→N / stop geometry / session window after freeze.
- Reintroducing through-break (CON-1–4) θ; fade-to-VWAP; compression transplant; ORB transplant.
- Path-scoring real bars before explore GO; oracle ranking; Cap/Pine/deploy/arming.
