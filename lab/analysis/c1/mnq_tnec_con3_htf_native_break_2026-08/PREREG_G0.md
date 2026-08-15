# Q-TNEC-CON-3 — Stage-0 PREREG (G0) — HTF-native 5m compression break

**Status:** `FROZEN` 2026-08-10 — ENTRY named; explore GO **paid** → [`RESULTS.md`](RESULTS.md) `AMBIGUOUS-HOLD`; Cap seat not claimed.
**Date:** 2026-08-10
**Parent brief:** [`docs/briefs/Q-TNEC-CON-3-htf-native-compression-break-scoping.md`](../../../../docs/briefs/Q-TNEC-CON-3-htf-native-compression-break-scoping.md)
**Lane:** [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../../../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
**Intake gate:** [`TNEC-1`](../../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) (`RATIFIED`)
**Mechanism id:** `htf-compression-breakout-5m` ([`MECHANISMS.md`](../../../../ops/instruments/MECHANISMS.md))
**Prior:** [`Q-TNEC-CON-2` AMBIGUOUS-HOLD](../../../../docs/briefs/closures/Q-TNEC-CON-2-closure-ambiguous-hold.md) · HTF-bias→LTF filter `FALSIFIED` (no Q-ID)
**`K_intrinsic = 1`**. Cap 1.0 → DSR floor **0.650**.
**Cost so far:** **$0.0000** (MNQSEL-2 panel reuse).

**FROZEN ON THIS FILE'S INTRODUCING COMMIT.** Zero EXPLORATION path scores at freeze
(cheap falsifier = parent panel run only — see [`ADMISSION_FALSIFIER_LOG.md`](ADMISSION_FALSIFIER_LOG.md)).

---

## §0 — Rule-0 / cheap falsifier / domain bar (parent-side, 2026-08-10)

| Check | Result |
|---|---|
| MNQ panel | `lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet` |
| Domain bar | `python scripts/instrument_profiles.py cell MNQ htf-compression-breakout-5m` → BINDING BAR `index-intraday-ohlcv-directional-timing-2026-07-21`; **route ①** temporal selectivity ([ADR 2026-08-10](../../../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)) |
| Family | `CHEAP_FALSIFIER_OK` — long mean R +0.063 CI [−0.079, +0.203]; short −0.035 CI [−0.216, +0.151]; n=794/716; coverage 91.6% — [`_cheap_falsifier_htf_native_break_2026-08-10_LOG.md`](../cheap_falsifiers_2026-08/_cheap_falsifier_htf_native_break_2026-08-10_LOG.md) |
| Sign | **With-break** frozen; do not invert to fade |
| ENTRY | Named, causal at 5m open, ≠ oracle; first/session |

**Verdict:** `CHEAP_FALSIFIER_OK` — licenses G0 freeze + harness scaffold; **not** SHAPE-CLEAR.

---

## §1 — Universe and trade geometry

| Element | Frozen value |
|---|---|
| Clocks | CME equity-index **RTH** Mon–Fri **09:30–15:59 ET**; signal clock = **5m** bars (resampled from 1m panel) |
| Trade instrument | `MNQ.v.0` continuous (MNQSEL-2 panel) |
| Roll exclusion | `in_roll_window` (±4 days of 3rd Friday Mar/Jun/Sep/Dec) |
| Stop | **Opposite quiet extreme** (structural); same-bar stop wins |
| Exit | **Session-flat** at last in-session RTH bar close |
| Cost / R | Tradeify RT **1.41** pt; `R = (pts − 1.41) / stop_dist` |
| Independence | EM3 — one position; **first valid signal per session only** |
| Arms | Long and short **separate** for gate stats |
| K | `K_intrinsic = 1` |

---

## §2 — Catalogue cell C1 — ENTRY (causal; all constants a priori)

Inputs at each RTH **5m** bar close `t` (known at close of `t`):

```
med_rng(session) = median(5m bar ranges) over trailing 20 completed RTH sessions
narrow(i)        = (high[i]-low[i]) > 0 and (high[i]-low[i]) <= 1.0 * med_rng
compression      = narrow(t-K_NARROW) … narrow(t-1)   # K_NARROW=2
quiet_hi/lo      = max/min high/low over those bars
midline          = (quiet_hi + quiet_lo) / 2
```

Signal after close of `t`; enter at **open of t+1**:

| Condition | Action |
|---|---|
| compression ∧ close[t] > quiet_hi ∧ close[t] > midline | enter **LONG** at open[t+1]; stop = quiet_lo |
| compression ∧ close[t] &lt; quiet_lo ∧ close[t] &lt; midline | enter **SHORT** at open[t+1]; stop = quiet_hi |
| otherwise / already traded this session | no trade |

**Frozen constants:** `K_NARROW=2` · `NARROW_MULT=1.0` · median window **20** · HTF=**5m** · first/session · structural stop · with-break.

**Closed-door clearance:** ≠ CON-1 · ≠ CON-2 (1m / fixed G=10) · ≠ HTF-bias→LTF filter · ≠ Family A fade · ≠ C1–C11 / T-IMB / SWING-1. C10 adjacency: not a level-touch attraction test.

---

## §3 — Scoring (EXPLORATION only; after operator GO)

Per arm (long / short separate):

| Limb | Definition |
|---|---|
| Primary | Mean net R; session-block bootstrap **95% CI** must exclude 0 |
| Placebo | Within-session R-shuffle **1000** reps; seed **20260810** (declared at explore GO if runner gap) |
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

- Retuning `K_NARROW` / `NARROW_MULT` / median window / HTF minutes / first→N per session after freeze.
- Reintroducing 1m entry or HTF-as-bias-only layer; fixed G=10 CON-2 retune; fade.
- Path-scoring real bars before explore GO; oracle ranking; Cap/Pine/deploy/arming.
