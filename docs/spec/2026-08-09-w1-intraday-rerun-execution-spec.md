# SPEC: W1 execution — build + run the intraday-honest both-halves re-run (GO already given)

Status: PROPOSED · 2026-08-09 · authorizes nothing new — **operator GO given 2026-08-04** on the frozen contract; this spec is the Cursor execution packet · depends: [W1 ADR](../adr/2026-08-07-w1-intraday-honest-engine-remeasure.md) · [frozen Phase-4 spec](2026-08-04-phase4-both-halves-intraday-rerun-spec.md) `FROZEN`
Objective: build the `intraday_low` channel into `lab/discovery/prop_survivor_scoring.py` per the frozen 2026-08-04 contract and publish honest-clock both-halves RESULTS — every eval bust figure in the repo is an **EOD-clock LOWER BOUND** until this lands, and the 2026-11-08 §4 verdict should read honest numbers.

Steps:

1. **Rule 0.** Read in full before any design: the frozen Phase-4 spec · `lab/discovery/prop_survivor_scoring.py` · the class_s harness (`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/`) · the [2026-07-13 survivor-scoring prereg](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) (thresholds 3.0% / 50% — frozen, unedited).
2. **RED-first tests, before the build:** (a) the pairing INVARIANT — `intraday_low` sliced with the **same indices** through both resamplings; (b) the **non-vacuity guard** — a silently dropped channel must FAIL loudly, never reproduce the flattering 2026-07-17 EOD numbers (the named M-23-shaped failure the frozen spec exists to prevent). Watch both fail, then build.
3. Build per the frozen contract. No threshold motion, no engine change beyond the channel (frozen-engine Trap #11), `dd_lock_offset_usd` stays unreachable.
4. Run both regime halves; publish RESULTS in the class_s dir with per-half and full-panel rows against the frozen 3.0%/50% gate.
5. **Supersession sweep (blast-radius in the same PR):** the DP3 bust-ceiling RESULTS, the §4-withdrawal restore-trigger rows, and CLAUDE.md's "every bust figure is a LOWER BOUND" warning each get their W1-successor pointer — reader-intercept form, frozen bodies unedited.
6. **Full `pytest` + gate battery before the PR** — the battery does not run tests and is not sufficient evidence (operational rule 16).

Gate: RESOLVED if `rg -c "intraday_low" lab/discovery/prop_survivor_scoring.py` > 0 ∧ both RED-first tests green ∧ both-halves RESULTS published ∧ supersession pointers landed ∧ full suite green. FALSIFIED — n/a (measurement); adverse numbers are a *result*, never a reason to touch the gate.
Boundary: thresholds frozen (3.0% / 50%, prereg unedited) · no rung / lifecycle / allocation motion from the numbers — disposition is the operator's at the results, not Cursor's in the PR · no re-cut of windows or halves after seeing output (Trap #12) · engine frozen.
Reads: [W1 ADR](../adr/2026-08-07-w1-intraday-honest-engine-remeasure.md) · [frozen Phase-4 spec](2026-08-04-phase4-both-halves-intraday-rerun-spec.md) · [survivor-scoring prereg](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) · [CORRECTED_FULLPANEL](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md)
Verify (Phase-0, Cursor runs before building): `rg -c "intraday_low" lab/discovery/prop_survivor_scoring.py` (expect 0 — unbuilt) · `rg -n "GO given 2026-08-04" docs/spec/2026-08-04-phase4-both-halves-intraday-rerun-spec.md` · `ls lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/`
Owner: [W1 ADR](../adr/2026-08-07-w1-intraday-honest-engine-remeasure.md); RESULTS dock in the class_s dir; supersession pointers per Rule 14 (corrections land where read).
