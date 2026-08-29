# Q-RANGEXFER-1 — Verdict pre-registration (H-RANGEXFER-1 / H-RANGEXFER-1.a)

**Frozen:** 2026-08-29, before Phase 1 (the joint-surrogation null design) has been written,
reviewed, or run. Parent brief:
[`Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md`](../Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md).
Operator GO for Phase 1 design work: **owed, not yet granted** — this freeze does not authorize
Phase 1; it only pins the classification thresholds so Phase 1, once GO'd and reviewed, cannot be
tuned to its own result.

A verdict computed after moving any threshold below, the window/quantile constants, or the
by-year N_valid floor is void.

**Forbidden regardless of outcome:** no threshold moves after Phase 1 results exist. If the
joint-surrogation design (once written) cannot be scored against these frozen limbs without
modification, that is a new design decision requiring a fresh freeze — not an edit to this one.

---

## §A — Frozen constants (carried from the frozen corrected-null-battery spec's own D2 table,
`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`, adapted to the
cross-series case; not re-derived, not re-tuned)

- `WINDOW = 60` (trailing valid-observation count for both bias and reference thresholds)
- `Q_BIAS = 0.80` (top-quintile bias threshold)
- `Q_REF = 0.50` (median outcome-reference threshold)
- `alpha = 0.05`
- `N_FLOOR_POP = 400`, `N_FLOOR_COND = 100` (L1 analogue, population and conditional-cell floors)
- `YEAR_MIN_NCOND = 20`, `N_valid >= 7` else AMBIGUOUS (L4 analogue — **known risk, disclosed
  ex-ante**: this MNQ panel (2020-07 to 2026-07) produced only 6 qualifying full calendar years
  for candidate 1's identical by-year structure, landing AMBIGUOUS there; the same wall may fire
  here, and is not evidence against H-RANGEXFER-1 if it does)
- CI block-bootstrap: `block = 20` trading days, `draws = 4000`, `seed = 42` (day-level; distinct
  from the frozen spec's own `block = 60` since this construct's bias/outcome pairing is denser —
  one observation per trading day, not one per bar)

---

## §B — Presence limbs (L1–L4 analogues; GATE, verbatim carry from whichever Phase-1 script
computes them — no re-derivation at verdict time)

| Limb | Content | Role |
|---|---|---|
| L1 | n-floor: n_scored ≥ 400 AND n_cond ≥ 100, both parent and (for H-RANGEXFER-1.a) the overnight-calm-restricted sub-panel | GATES |
| L2 | Block-bootstrap CI lower bound on the minimum stratified incremental lift > 0 | GATES |
| L3 | Both halves (chronological split) of the conditional cases show lift > 0 | GATES |
| L4 | By-year floor: incremental lift > 0 in ≥ N_valid−2 of N_valid qualifying years (n≥20/year); AMBIGUOUS if N_valid < 7 | GATES |

## §C — Attribution limb (L5 analogue; NEVER GATES on its own — TYPES the verdict between
RESOLVED-strength and a weaker survival-only reading, exactly as the frozen battery's SIGNAL-EXCESS
vs SIGNAL-GENERIC split)

- Whatever joint-surrogation design Phase 1 produces (post-review), its two-sided p_upper against
  the observed minimum stratified lift is the L5 analogue. `p_upper ≤ 0.05` → attribution clears;
  `SUB-LINEAR` / `ATTRIBUTION-FRAGILE` / `BORDERLINE` flags carry the same definitions and the
  same never-re-roll discipline as the frozen spec's §2.

---

## §D — Verdict map (mirrors the parent brief's §6 table exactly; restated here as the
frozen, pre-Phase-1 form)

| Verdict | Trigger | Applies to |
|---|---|---|
| `RESOLVED` | L1–L4 all pass AND L5 clears (p_upper ≤ 0.05) | H-RANGEXFER-1 and/or H-RANGEXFER-1.a, scored independently |
| `FALSIFIED` | Any of L1–L3 fails outright, OR L4 fails outright (not AMBIGUOUS — i.e. N_valid ≥ 7 but fewer than N_valid−2 years clear), OR L5's diagnostic gate VOIDs after the full escalation ladder (iter=500 → Schreiber end-matching trim, same ladder candidate 1 exhausted) | as above |
| `AMBIGUOUS-HOLD` | L1–L3 pass but L4 cannot resolve (N_valid < 7) | as above |

---

## §E — Pinned ex-ante expectation

**Predicted for H-RANGEXFER-1: presence limbs (L1–L3) PASS, L4 lands AMBIGUOUS** — same
structural wall candidate 1 hit on this identical panel span (only 6 of the required 7 full
calendar years qualify at `n_cond >= 20`). This is a panel-length prediction, not a comment on
whether the underlying effect is real; the stage-1 result's own by-year table has not been
computed and may behave differently in year-count terms than candidate 1's daily-TR object, since
the conditioning event (top-quintile overnight range) may distribute across years differently
than top-quintile daily TR does. **Predicted for H-RANGEXFER-1.a: FALSIFIED or AMBIGUOUS on
power grounds** — the overnight-calm-restricted sub-panel (973 scored days, 175 gap-positive) is
meaningfully smaller than the parent's full 1487, and splitting further by year for an L4 read on
a sub-stratum is likely underpowered before any joint-surrogation null is even applied.

Substituting real Phase-1 numbers to confirm or refute this prediction is the compute step, not
this freeze.

---

**Freeze note:** this file exists on disk, committed in the same commit as the parent brief, before
Phase 1 has been designed, reviewed, or run — same discipline as `Q-CONDVAL-1` / `Q-TRAINKILL-1`
(freeze-then-score, verified via the parent brief's own `git log` audit hook).
