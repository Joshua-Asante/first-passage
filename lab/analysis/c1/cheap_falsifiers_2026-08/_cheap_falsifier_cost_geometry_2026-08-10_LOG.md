# Cheap falsifier — dense-1m lane cell #3 "cost geometry" · `FALSIFIED (exit-geometry lever)` + a blocking governance finding

**Date:** 2026-08-10 · **$0.00 · K=0 · no Q-ID spent · no G0 authored** · EXPLORATION only (sessions ≤ 2025-08-31; CONFIRM unread)
**Trigger:** operator "cell #3 fresh G0 aimed at cost geometry", per the [CON-2 closure](../../../docs/briefs/closures/Q-TNEC-CON-2-closure-ambiguous-hold.md) Iterate routing.
**Discipline:** [lane spec](../../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) **step 2** — parent-side cheap falsifier BEFORE authoring; *"a failed cheap falsifier kills the proposal at $0 with no Q-ID spent."*

## Pre-committed reading (written before the run)

> KILL if no stop width in the ratified 5–20 pt band, and not even the perfect-foresight once-per-session
> ORACLE, produces gross pts/trade ≥ the 4× cost bar (4 × 1.41 = **5.64 pt**). A "some G clears" result is
> **not** a candidate — it is disclosure requiring a fresh mechanism argument and its own G0.

## Result 1 — the exit/stop-width lever is DEAD (kill fires)

CON-2's frozen entry, exit geometry swept across the whole ratified band. The 4× bar is **G-independent in
points** (cost_R = RT/G and the bar is 4·cost_R, so both scale together ⇒ gross_pts ≥ 4·RT always):

| G (pt) | n signals | gross pt/trade | net R | vs 5.64 pt bar |
|---|---|---|---|---|
| 5 | 79,620 | 0.112 | −0.2596 | **0.02×** |
| 10 | 79,620 | 0.377 | −0.1033 | **0.07×** |
| 15 | 79,620 | 0.419 | −0.0661 | **0.07×** |
| 20 | 79,620 | 0.542 | −0.0434 | **0.10×** |

⚠ **Cohort note (this basis is STRICTER than CON-2's, not generous):** this probe scores **every** signal
(79,620), while CON-2's harness enforces one-position-at-a-time blocking (8,429 non-overlapping trades). The
blocking incidentally selects better fills, so CON-2's own gross is **+0.90/+0.97 pt = 0.16–0.17× the bar**.
Read the sweep for its **shape** (monotone in G, plateauing) and CON-2's number for the level. Both readings
are 6–10× short, and widening the stop to the top of the ratified band closes ~none of that gap.
**Verdict: widening the stop cannot rescue this family. Kill fires on the exit-geometry design.**

## Result 2 — trade-count headroom is real (the lever that survives)

Perfect-foresight best single entry per session (upper bound on **any** selectivity rule):

| G (pt) | oracle gross pt/session | vs bar | % of oracle needed to clear 4× |
|---|---|---|---|
| 5 | 166.86 | 29.6× | **3.4%** |
| 10 | 170.47 | 30.2× | **3.3%** |
| 15 | 171.29 | 30.4× | **3.3%** |
| 20 | 171.41 | 30.4× | **3.3%** |

**The cost-geometry lever is trade COUNT, not stop width.** One trade/session needs 3.3% of the oracle;
CON-2's ~6 trades/session/day needs ~20%. This is the EM1 frequency-inversion arithmetic from the other side,
and it is consistent with the venue needing only **weekly** activity (N-ACT), not daily. ⚠ 3.3% is not
"easy" — it is a fraction of a max-order-statistic, and random entry captures ≈0 or negative (MNQSEL-2 S1
≈ −0.036). It is *headroom*, not a candidate.

## Result 3 — BLOCKING: the lane never consulted a live, machine-enforced domain bar

`python scripts/instrument_profiles.py cell MNQ compression-gated-breakout` prints:

```
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
```

That bar (tier=always, machine-consulted) admits a *new* single-instrument index-futures intraday **OHLCV
directional-timing** candidate only via: ① a mechanism **outside the mapped cost-ratio levers {price ·
instrument-selection · hold-time}**; ② a different **modality** (order-flow/microstructure) or a venue
relaxing a binding wall; ③ evidence it **beats incumbent ORB-MNQ net-of-cost**.

**Executed check — the bar appears NOWHERE in the lane:**

```
rg -niE "raised bar|domain bar|index-intraday|2026-07-21|mapped lever|hold-time" \
   docs/briefs/Q-TNEC-CON-2-...md lab/.../PREREG_G0.md docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md
→ (no matches)
```

The lane spec's per-campaign door check is scoped to **C1–C11 + the MNQ DEAD list** and never reaches the
domain-level bar. So **CON-1 and CON-2 both ran unbound by a gate that was live and machine-consulted the
whole time.** This is `lesson_gate_reachability_preregistration` in its *unbinding* form — the **5th recorded
firing** (memory notes 4 at the 2026-08-08 sweep, "overdue for promotion").

**Why it blocks cell #3 specifically:** the surviving lever (Result 2) is temporal selectivity on OHLCV bars.
Any OHLCV-derived selection rule is a **price** mechanism ⇒ fails route ①. Route ② is the order-flow modality,
which [ADR 2026-08-08 §2-C **L1**](../../../docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md)
**PAUSED**. Route ③ is a *results* bar — unclearable ex ante, by construction. **A dense-1m OHLCV cell #3
cannot clear the domain bar as written.**

## Disposition

**No G0 authored. No Q-ID spent.** Per lane-spec step 2 the proposal dies here at $0 — and independently, the
domain bar blocks the only surviving design. Two things are now owed to the operator and neither is
self-authorizable:

1. **A domain-bar ruling** — does within-instrument *temporal* selectivity count as the mapped
   "instrument-selection" lever (⇒ barred), or as a mechanism outside the mapped set (⇒ route ① open)? The
   mapped entry was derived from **cross-index** RV ranking, so the reading is genuinely open — and it is an
   operator ruling, not a brief's to take.
2. **The unbinding-gate repair** — the lane spec's door check must reach domain-level bars, and the
   `lesson_gate_reachability_preregistration` promotion question is now at 5 firings.

**Not claimed:** no lever is declared universally dead; Result 2 preserves the selectivity direction pending
(1). No retune of any frozen CON-2 constant is licensed by anything above.
