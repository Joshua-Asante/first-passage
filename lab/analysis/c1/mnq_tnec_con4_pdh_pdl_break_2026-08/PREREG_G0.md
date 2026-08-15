# Q-TNEC-CON-4 — Stage-0 PREREG (G0) — PDH/PDL RTH with-break

**Status:** `FROZEN` 2026-08-10 — ENTRY named; explore GO **paid** → [`RESULTS.md`](RESULTS.md) `AMBIGUOUS-HOLD`; Cap seat not claimed.
**Date:** 2026-08-10
**Parent brief:** [`docs/briefs/Q-TNEC-CON-4-pdh-pdl-breakout-scoping.md`](../../../../docs/briefs/Q-TNEC-CON-4-pdh-pdl-breakout-scoping.md)
**Lane:** [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../../../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
**Intake gate:** [`TNEC-1`](../../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) (`RATIFIED`)
**Mechanism id:** `pdh-pdl-breakout-rth` ([`MECHANISMS.md`](../../../../ops/instruments/MECHANISMS.md))
**Prior:** [`Q-TNEC-CON-3` AMBIGUOUS-HOLD → Branch B](../../../../docs/briefs/closures/Q-TNEC-CON-3-closure-ambiguous-hold.md)
**`K_intrinsic = 1`**. Cap 1.0 → DSR floor **0.650**.
**Cost so far:** **$0.0000** (MNQSEL-2 panel reuse).

**FROZEN ON THIS FILE'S INTRODUCING COMMIT.** Zero EXPLORATION path scores at freeze
(cheap falsifier = parent panel run only — see [`ADMISSION_FALSIFIER_LOG.md`](ADMISSION_FALSIFIER_LOG.md)).

---

## §0 — Rule-0 / cheap falsifier / domain bar (parent-side, 2026-08-10)

| Check | Result |
|---|---|
| MNQ panel | `lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet` |
| Domain bar | `python scripts/instrument_profiles.py cell MNQ pdh-pdl-breakout-rth` → BINDING BAR answered **route ①** |
| Family | `CHEAP_FALSIFIER_OK` — long −0.0048 CI [−0.042, +0.033]; short −0.0028 CI [−0.051, +0.043]; n=850/616; coverage 88.0%; mean stop ≈279 pt — [`_cheap_falsifier_pdh_pdl_break_2026-08-10_LOG.md`](../cheap_falsifiers_2026-08/_cheap_falsifier_pdh_pdl_break_2026-08-10_LOG.md) |
| Sign | **With-break** frozen; do not invert to fade / level-touch attraction |
| ENTRY | Named, causal at next 1m open after close beyond PDH/PDL; first/session |

**Verdict:** `CHEAP_FALSIFIER_OK` — licenses G0 freeze + harness scaffold; **not** SHAPE-CLEAR.

---

## §1 — Universe and trade geometry

| Element | Frozen value |
|---|---|
| Clocks | CME equity-index **RTH** Mon–Fri **09:30–15:59 ET**; signal clock = **1m** bars |
| Trade instrument | `MNQ.v.0` continuous (MNQSEL-2 panel) |
| Roll exclusion | `in_roll_window` (±4 days of 3rd Friday Mar/Jun/Sep/Dec) |
| Levels | PDH/PDL = immediately prior eligible RTH session high/low |
| Stop | **Opposite prior extreme** (long→PDL, short→PDH); same-bar stop wins |
| Exit | **Session-flat** at last in-session RTH bar close |
| Cost / R | Tradeify RT **1.41** pt; `R = (pts − 1.41) / stop_dist` |
| Independence | EM3 — one position; **first valid signal per session only** |
| Arms | Long and short **separate** for gate stats |
| K | `K_intrinsic = 1` |

---

## §2 — Catalogue cell C1 — ENTRY (causal; all constants a priori)

After each RTH **1m** bar close `t` (known at close of `t`):

| Condition | Action |
|---|---|
| close[t] > PDH | enter **LONG** at open[t+1]; stop = PDL |
| close[t] &lt; PDL | enter **SHORT** at open[t+1]; stop = PDH |
| otherwise / already traded this session | no trade |

**Frozen constants:** PDH/PDL = prior RTH H/L · first/session · structural opposite-extreme stop · with-break · session-flat · RT 1.41.

**Closed-door clearance:** ≠ CON-1 · ≠ CON-2 · ≠ CON-3 · ≠ HTF-bias→LTF · ≠ ORB · ≠ MNQPROX · ≠ N9 pool-attraction / C10 level-touch fade (through-break, not attraction).

---

## §3 — Scoring (EXPLORATION only; after operator GO)

Per arm (long / short separate):

| Limb | Definition |
|---|---|
| Primary | Mean net R; session-block bootstrap **95% CI** must exclude 0 |
| Placebo | Sign-randomized R **1000** reps; seed **20260810** (declared at explore GO if runner gap) |
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

- Retuning PDH/PDL definition / first→N / stop geometry / session window after freeze.
- Reintroducing compression-break (CON-2/3) θ; fade / level-touch attraction; ORB transplant.
- Path-scoring real bars before explore GO; oracle ranking; Cap/Pine/deploy/arming.
