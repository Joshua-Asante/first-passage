# Parallel Leg — §4 Firm-Model Repair (Bulenox/BluSky trust restoration + survivor scoring)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development or
> superpowers:executing-plans. Checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION:** R1+R2 GO executed 2026-08-23 (R1 ratified `RESOLVED — WITH NAMED RESIDUAL`;
R2 `RESOLVED` at `65dc17b`). R3 remains gated on a Phase-C survivor. The
[Q-FIRMEOD-1 closure](../../briefs/closures/Q-FIRMEOD-1-closure-falsified.md) named this
successor but, per its own convention, did not open ("naming ≠ opening") — that sentence is
history; the fresh-Q + operator-GO condition it named was met the same day. Runs in
parallel with Phases A/B; R1+R2 must have landed **before** any Phase-C survivor is scored for §4.
**Cost:** $0 / K=0 — reuses committed engine fixtures and free primary-source reads.
**Parent:** [`sequence overview`](2026-08-23-viable-strategy-sequence-overview.md)

**Why this is on the §4 critical path:** post-F1, §4 discharge requires ≥1 pre-registered
candidate clearing the frozen gate on **≥2 of {Bulenox, MFFU, BluSky}** by 2026-11-08. Q-FIRMEOD-1
proved the engine models for two of those three cannot currently be trusted (Bulenox CLOCK flip
demonstrated; Bulenox LOCK language unexamined; BluSky CLOCK never diffed), and its closure bars
citing any Bulenox/BluSky bust figure in cross-firm comparison until this repair lands. Without
it, a Phase-C survivor could reach 2026-11-08 unable to be scored on 2 of the 3 firms that count.

**Entry packet (frozen by the closure — carried, not re-derived):** (i) the CLOCK evidence — the
exact `firm_kwargs('Bulenox_100K')` parametrization and the 0→1 `bust_trailing` flip, reproducible
via `tests/core/test_mc_intraday_barrier.py`; (ii) the LOCK evidence — the verbatim Bulenox Master
Account quote ("stops moving... starting balance +100") + both Wayback capture URLs/timestamps;
(iii) the explicit note that BluSky's CLOCK was only textually suggestive, never engine-diffed.

---

## Task R1 — 7-tier intraday-honest re-run (the W1 pattern, applied)

- [x] Enumerate the 7 `dd_type="trailing"` tiers (Bulenox ×5, BluSky ×2) from `core/firm_rules.py`
  — the closure's own grep pins them.
- [x] Re-run every published bust/pass figure that exists for those tiers with `intraday_low`
  populated, per the W1 ADR's pattern (frozen seeds/sims/horizon via `load_scoring_thresholds()`;
  no re-picking). Where a tier has no published figure, record "none to re-measure" rather than
  manufacturing one.
- [x] Report per-tier: EOD-clock figure → honest-clock figure → flipped verdicts, in a RESULTS
  doc under `lab/analysis/c1/` with a CATALOG row. Every prior figure that moved gets a
  reader-intercept note at the surface where it is read (Rule 14), not just here.
- [x] BluSky CLOCK specifically: run its tier(s) through the same direct `simulate_path` diff
  Bulenox got — the closure explicitly declined to assume BluSky is clean by analogy.

**Gate (R1):** `RESOLVED — WITH NAMED RESIDUAL` — the two tiers carrying a published figure on the
live candidate book (Bulenox_100K, BluSky_Premium_100K, both published arms) carry a MEASURED
honest-clock figure with no verdict flip; BluSky_Premium_50K carries an explicit
none-to-re-measure line. **Correction (2026-08-23 fix-pass, reviewer-flagged):** the original text
here claimed "an explicit none-to-re-measure line (the other 5)" — false for 4 of them. A separate,
closed/NO-GO'd, Pepperstone-sourced archived campaign (`lab/archive/bulenox_futures_remc_2026-07-01/`)
publishes EOD-clock figures for Bulenox_25K/50K/100K/150K/250K; most cells are monotonicity-disposed
(already FAIL), a small PASS-side residual is explicitly named and not re-run (3 stated reasons —
retired vendor feed, a verified-broken entry-point import, a dead/NO-GO'd program). Full accounting:
RESULTS.md §2/§4b. The CLAUDE.md caveat line ("EOD-clock lower bounds unless intraday-honest") now
extends its scope from Tradeify/Class-S to these firms, landed in the same commit —
[`RESULTS`](../../../lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md) ·
[`audit note`](../../notes/audits/2026-08-23-r1-bulenox-blusky-clock-repair.md).

**Operator ratification (2026-08-23, real-time GO in chat):** the implementer's self-authored
three-way disposition — the task reviewer's own phrasing was "done for what's live, openly
incomplete for what isn't" — is ratified as-is. `Bulenox_100K`/`BluSky_Premium_100K` (the tiers
R3 actually consumes; the 50K band is diagnostic-only per R3's own scope and the other archived
tiers aren't named there at all) are genuinely, fully re-measured. The named residual
(`Bulenox_25K/50K/150K/250K` PASS-side cells in the closed/NO-GO'd archived campaign) stays
un-re-run for the three stated reasons; reviving it is not authorized by this ratification and
would need its own case if ever raised. This closes the one item the task reviewer flagged as
needing explicit sign-off rather than implementer self-authorization.

## Task R2 — Bulenox lock-scope resolution (primary source, then classification) — `RESOLVED`

- [x] Answer with primary-source grounding: does the Master-account "stops moving at initial
  balance +100" lock reach the **currently-simulated horizon** (Qualification-only,
  absorbing-at-pass), yes or no? The closure left this genuinely open — a successor must
  investigate, not assume either way. **Answer: NO** — confirmed two independent ways (textual
  scope on both re-fetched primary sources; `simulate_path`'s absorbing-at-pass structure never
  threads a post-pass stage). [`audit note`](../../notes/audits/2026-08-23-bulenox-lock-scope-resolution.md).
- [x] If the lock does **not** bite the modeled horizon: record the finding + fix the
  `firm_rules.py` sourcing comment's completeness gap (the "silence read as completeness"
  defect the closure documented) — comment-only change, no constant moves. Landed at
  [`65dc17b`](https://github.com/Joshua-Asante/first-passage/commit/65dc17bdc969f562a952951cb5273e7913384864).
- [ ] If the lock **does** bite: re-classifying Bulenox to `trailing_locking` with sourced lock
  terms is a **separate change-control action** — its own pre-registration → re-derivation →
  admitting ADR, never an in-place edit riding on this plan (the closure's own bar). **Did not
  fire** — the answer above is NO, so this branch is correctly untaken.

## Task R3 — Survivor §4 scoring (blocks on R1; consumes a Phase-C survivor)

- [ ] Score the survivor on `Bulenox_100K` / `MFFU_Rapid_100K` / `BluSky_Premium_100K` honest-clock
  models under the frozen survivor-scoring prereg (2026-07-13, unedited: bust ≤3.0% ∧ P(pass)
  ≥50%, frozen $100K cross-section — the 50K band stays diagnostic-only).
- [ ] **F1-ruling discipline:** Tradeify's own clearance, if any, is reported with the mandatory
  disclosure (F1 ruled: counts zero toward §4) — the count that matters is over the three firms.
- [ ] **Disposition table (pre-stated):** ≥2 of 3 clear → §4 H fires; discharge per the four-firms
  ADR. Exactly 1 clears → the `PARTIAL` addendum is still `Proposed`/deferred-to-trigger-time —
  surface it to the operator **at that moment** with the scoreboard in hand; do not pre-ratify
  it here. 0 clear → the revert trigger's designed path (research-only demotion) governs at
  2026-11-08, per the standing base case.

## Sequencing note

R1+R2 are a few sessions of work with no dependency on Phases A/B — start any time after GO.
R3 cannot run before a Phase-C survivor exists; if none exists by 2026-11-08, R1/R2 still stand
on their own (they repair a confirmed model-trust defect regardless of the strategy search's
outcome, and the closure's citation bar lifts only when they land).

## Forbidden moves

Editing `dd_type`/`trailing_dd_pct`/any constant under this plan (R2's change-control path is the
only door) · citing any pre-repair Bulenox/BluSky figure in a cross-firm comparison · treating
BluSky as CLOCK-clean by analogy · re-deriving frozen scoring thresholds · reading this plan as
ruling the exactly-one-tier `PARTIAL` question (operator's, at trigger time).

## Exit criteria

R1 honest-clock table published + caveat-scope extended · R2 lock-scope answered with primary
grounding (and any re-classification routed to its own ADR) · the Q-FIRMEOD-1 citation bar
formally lifted by those artifacts · R3 executed if and when a survivor exists.
