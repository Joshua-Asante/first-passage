# Q-VOLREGIME-1 — Packet C1: pilot acceptance bands (frozen before simulation)

**Status:** `FROZEN, NOT YET EXECUTED` — this document declares C1's own required bands, counts, and
disposition rules. **No simulation has been run.** No real L5 statistic, on either instrument, has
been inspected. Nothing here executes anything; it exists so C2–C5 (the actual pilot studies) have
nothing left to decide once real data is touched.

**Operator GO:** received for Packet C1 specifically — 2026-08-31. Per the plan doc's own gate
table, this GO authorizes *freezing* the pilot's own acceptance criteria; it does **not** authorize
running C2 (null-size study), C3 (power study), or C4 (adequacy checks) — those each still need
their own execution to actually happen, and Packet D (real execution) needs a further, separate
GO plus a K declaration on top of a passing C5.

**Entry gate satisfied:** Packet B (B1–B5) is complete —
[`volregime_l5_design_2026-08-31/DESIGN.md`](../volregime_l5_design_2026-08-31/DESIGN.md), frozen
2026-08-31, five Codex review rounds, the fifth returning no findings.

---

## 1. Replicate counts and seeds

**Two distinct replicate counts, for two distinct purposes — not one number reused.**

- **`B = 4000`** — the frozen inner null-replicate count for the real L5 attribution statistic
  itself (`DESIGN.md` §4.1), unchanged. This is what Packet D would eventually use, and what C3's
  own power study also uses per synthetic panel (below) — the pilot must exercise the exact
  machinery Packet D would run, not a scaled-down version of it, or the pilot proves nothing about
  the real thing.
- **`N_outer = 100`** (new, frozen here) — the number of independent synthetic null panels
  generated per instrument, per comparison, for C2's own null-size study. Each synthetic panel is
  scored by the **full** `B=4000`-replicate pipeline (`DESIGN.md` §4.2–§4.4), so C2 alone requires
  `100 × 4000 = 400,000` full-pipeline replicate-equivalent computations per (instrument,
  comparison) — a disclosed, deliberate computational-budget choice, not a number chosen for
  convenience without consequence: under a true 5% Type-I rate, 100 outer draws gives a binomial
  standard error of `sqrt(0.05 × 0.95 / 100) ≈ 2.2 percentage points`, which resolves a true rate
  of 5% from `Q-RANGEXFER-1`'s own measured failure magnitude (5% → 25%) with high confidence, but
  is **not** sized to detect a smaller, subtler miscalibration (e.g. 5% → 8%) — a limitation
  disclosed here, not hidden, and the reason C4's own absolute-adequacy checks exist as an
  independent line of defense rather than relying on C2's own power alone.
- **Seeds — frozen per instrument, per comparison, per study, not drawn ad hoc at execution
  time:** `seed_base = 20260831` (matching this design's own freeze date, following
  `c3_stratified_rerun.py`'s own precedent of a dated seed rather than an arbitrary one). Each of
  the four (instrument × comparison) cells uses `seed_base` offset by a fixed, disclosed integer
  (MNQ Comparison 1: `+0`; MNQ Comparison 2: `+1`; MYM Comparison 1: `+2`; MYM Comparison 2: `+3`),
  so every cell's own random draws are reproducible and distinct, and no cell's own seed is chosen
  after seeing that cell's own results.

## 2. Empirical Type-I acceptance band (C2's own pass rule)

**Frozen method, not a single point estimate, and not a number picked after seeing the count.**
Across `N_outer = 100` synthetic null panels (§1) for a given (instrument, comparison) cell, count
the number of panels whose own `p_upper ≤ 0.05`. This observed count must fall inside the **exact
two-sided 95% Clopper–Pearson confidence interval for `Binomial(100, 0.05)`** — computed exactly,
not via a normal approximation (`n=100, p=0.05` is small enough that a normal approximation can
misstate the tail) — for the cell to individually clear. **All four cells** (MNQ × Comparison 1,
MNQ × Comparison 2, MYM × Comparison 1, MYM × Comparison 2) must clear independently; one cell's
own pass does not carry another's, matching this design's own per-instrument, per-comparison
independence throughout (`DESIGN.md` §2).

## 3. Minimum useful power at a planted effect (C3's own pass rule)

**Planted-effect magnitude — calibrated to each instrument's own already-observed minimum
stratified lift, not a shared or invented number.** Per the parent brief's own H-VOLREGIME text:
MNQ's own minimum within-stratum lift is **+22.3pp** (the low-range stratum, the smaller of its
own two strata); MYM's own is **+16.5pp** (the block-bootstrap mean minimum stratified lift). Each
instrument's own power study plants an incremental probability shift **no larger than its own
already-observed minimum** — using each instrument's own real number, not the smaller of the two
applied to both, consistent with this design's own no-pooling principle.

- **Primary planted effect:** exactly each instrument's own minimum stratified lift above (MNQ
  +22.3pp, MYM +16.5pp).
- **Secondary, stricter planted effect (disclosed as an additional check, not a required
  minimum):** half of the primary — MNQ +11.15pp, MYM +8.25pp — to see whether power degrades
  gracefully or falls off a cliff.
- **Minimum useful power: 80%** at the primary planted effect, per (instrument, comparison) cell,
  measured across `N_outer = 100` synthetic planted-effect panels (same count and seeding
  convention as §1, offset by a further fixed, disclosed integer per cell so planted-effect draws
  never reuse the null-study's own seeds) each scored by the full `B=4000` pipeline: the fraction
  of these 100 panels whose own `p_upper ≤ 0.05` must be `≥ 0.80`. No minimum power requirement is
  frozen for the secondary (half-magnitude) effect — it is diagnostic, reported but not gating.

## 4. Absolute calibration / adequacy diagnostics and pass rules (C4)

**Two layers, not one — `DESIGN.md` §4.6's own confound-preservation diagnostics, plus C4's own,
broader model-calibration battery this document adds.**

- **Layer 1 (already frozen, unchanged):** `DESIGN.md` §4.6's own per-replicate adequacy gate
  (same-bar Spearman correlation, conditional volume distribution across range quantiles, volume
  and range autocorrelation, cross-correlation at lags −4 through +4, time-of-day distribution),
  each checked per replicate against a 90% day-blocked bootstrap CI, requiring ≥95% of sampled
  replicates to individually clear. This layer checks whether the *null* is well-constructed; it
  does not check whether the *fitted model* is well-calibrated, which is C4's own distinct concern.
- **Layer 2 (new, frozen here) — model calibration, stratified.** For each of `baseline_1` and
  `augmented_1`'s own real-data (not null-replicate) OOS predictions, pooled across folds
  (`DESIGN.md` §4.1): bin predicted probabilities into deciles, and within each of the following
  strata independently — time-of-day (four buckets: the four calendar quarters of the ToD cycle,
  a coarser split than the raw slot, frozen now to avoid a sparse-bin problem at 96 slots), own-range
  stratum (`bias_range ∈ {0,1}`), calendar year, chronological half (matching L3's own midpoint
  split, `volregime_l3_2026-08-31/RESULTS.md`), and instrument — compute the maximum absolute gap
  between each decile bin's own mean predicted probability and its own observed outcome rate.
  **Pass rule: the maximum absolute calibration gap, across every decile bin within every stratum
  independently, must not exceed 5 percentage points.** A stratum with fewer than 30 scored bars in
  a given decile bin is excluded from that specific check and disclosed as excluded, not silently
  passed or failed. This is an **absolute** criterion (§ per the plan doc's own C4 language,
  "being relatively best among candidate models is insufficient") — `augmented_1` failing this gate
  is a design failure regardless of how it compares to `baseline_1`.

## 5. Bounded escalation and terminal failure disposition (C5's own gate, operationalized)

**Exactly one permitted escalation, narrowly scoped — not an open-ended retry.** If, and only if,
§2's own Type-I acceptance band is the gate that fails (power, §3, or calibration, §4, failing has
no escalation — see below): the **sole** permitted adjustment is widening `DESIGN.md` §3.4's own
frozen embargo from 4 to **8 trading days**, then re-running C2 (§2) **once** with that single
change and no other. If the widened-embargo re-run also fails §2's own band, or if the *original*
run failed §3 (power) or §4 (calibration) in the first place, the pilot **terminates immediately** —
no further escalation, no parameter search, no repeated tuning against the observed pilot result
(this design's own D8: "a pilot failure is a designed outcome").

**Terminal disposition on failure:** the affected (instrument, comparison) cell is marked
`AMBIGUOUS-PARKED`, per the plan doc's own C5 disposition table. This is recorded as a **design
failure**, not a negative empirical verdict on volume itself — the parent brief's own H-VOLREGIME
hypothesis is not falsified by a pilot failure; it remains open, with the machinery that would have
tested it disclosed as not yet trustworthy enough to run. No retune of §§1–4 above is permitted
after seeing which cell failed, beyond the one named embargo-widening escalation.

**Terminal disposition on success:** if all four (instrument × comparison) cells clear §§2–4, C5's
own joint pilot gate passes, and a frozen L5 execution packet is produced — Packet D still requires
its own separate operator GO and K declaration before the real, one-shot L5 statistic is ever
computed.

---

## 6. Amendment log

| Date | Change | By |
|---|---|---|
| 2026-08-31 | Initial freeze — Packet C1, following operator GO. No simulation run, no real data touched beyond citing already-published L1–L4/H-VOLREGIME figures from the parent brief. | Claude Code |
