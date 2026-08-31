# Regime-robustness gate

**Status:** canonical
**Version:** 1.0
**Authored:** 2026-05-06 (post Q-DDP-1 closure)
**Origin:** worked example in Q-DDP-1 (`archive/docs/briefs/Q-DDP-1/`)
**D-S-A domain at authoring:** meta-process (framework codification)
**Applies during:** INQHIORI loops on system-domain questions involving risk-constant Pareto sweeps

---

## What this gate is

A two-part panel-resampling test that any candidate configuration must pass before being recommended as a LOCK CANDIDATE in a Pareto-relaxation brief on a risk-control constant. Specifically: **6-month-block bootstrap** + **half-panel time split**, both pinned to the brief's full-panel pass-rate floor.

This gate exists because of one structural asymmetry: in any Pareto-relaxation question on `dd_protection` or analogous risk constants, **drag is fully measurable on the panel; tail-protection benefit is only partially measurable**. The realized panel is one trajectory through regime-space. A relaxation that wins on the realized panel may lose under regimes the panel didn't sample. This gate is the conservative haircut that lets the brief surface that distinction.

---

## When this gate fires

**Mandatory** for:
- Any brief proposing a change to constants in `core/dd_protection.py` (or a new `dd_geometry` POLICY_REGISTRY instance)
- Any brief proposing a Pareto-relaxation on (pass-rate, drag) or analogous (safety, performance) plane for a risk constant
- Any brief comparing MC configurations on a single panel where regime distribution materially affects the result

**Not required** for:
- Strategy parameter changes (governed by strategy-specific gates: pyramid-conditional WR, MFE/MAE direction-symmetry, etc.)
- Allocation changes (governed by variance-contribution + MC re-balance methodology)
- Adding / removing strategies (full re-MC at locked `dd_protection` — no Pareto sweep)
- Operational decisions (OODA / c1-rail layer, not INQHIORI)
- ORB-MNQ / venue-native research that does not change locked risk constants
- Any decision routed to OODA per the loop-selection canon

If a brief is uncertain whether this gate applies **and** a risk-constant LOCK CANDIDATE is in play: default to running it. Do not fire it as ceremony on tooling or research CSVs with no risk-constant change. The false-positive LOCK CANDIDATE failure mode is expensive; calendar-forced re-runs without a candidate are not.

**Do not import this gate as a per-candidate rider outside the scope above.** A candidate
pre-registration whose subject matter sits in the "Not required" list (a book/strategy addition,
an operational decision, ORB-MNQ/venue-native research) may cite this gate as informational
context, but must not import a specific item from another frozen gate document as a rider whose
consequence is fixed **before the gate runs** — see the worked non-example below. If a
pre-registration wants this gate's verdict to be load-bearing, it must sit inside this gate's own
declared scope, with a FAIL treated as a real falsifier, not pre-negotiated to non-blocking.

---

## Procedure

### Part A — Block bootstrap on the locked panel

1. Take the locked panel (e.g. 52-month Pepperstone — ⚠ retired 2026-08-02, bytes deleted, kept below only as the worked-example panel; there is no canonical CFD feed and the live feed is CME futures, see [pepperstone-feed-retirement ADR](../adr/2026-08-02-pepperstone-feed-retirement.md); check `core/mc/modes.py::PANELS_BY_BROKER` for the panel currently registered). Treat as a daily DataFrame with one row per business day.
2. Define **6-month contiguous blocks** over the panel timeline. With a 52-month panel, this yields ~9 candidate blocks; bootstrap variance scales accordingly.
3. **Resample with replacement** to construct 100 alternate-history panels of the same total length as the original.
4. For each alternate panel, rebuild the inner MC week-blocks (the existing harness's 5-day resampling unit) and run the full MC sweep at the candidate config — same seed count as the parent brief (e.g. 30K paths × 3 seeds).
5. Record per-(config, alt_panel_id) tuple: `pass_rate, bust_rate, p99_dd`.
6. Compute the **5th percentile** of the 100-panel pass-rate distribution per candidate.

### Part B — Half-panel time split

1. Split the locked panel at its temporal midpoint:
   - (Historical figures from the retired Pepperstone panel, kept for the worked example below — not a live split point; see the retirement ADR above.) For 52mo Pepperstone (2022-01 → 2026-04): H1 = 2022-01 → 2024-04, H2 = 2024-05 → 2026-04.
   - Unequal-length halves are acceptable; document the split point.
2. Run full MC at the candidate config on each half independently — same seed count as the parent brief.
3. Record per-(config, half) tuple: `pass_rate, bust_rate, p99_dd`.

### Part C — Acceptance test

A candidate config C* passes the gate **if and only if all three** hold:

1. **Bootstrap 5th-percentile pass-rate ≥ floor** (where floor = the brief's full-panel pass-rate floor)
2. **H1 pass-rate ≥ floor**
3. **H2 pass-rate ≥ floor**

Failure on any one criterion rejects the candidate as **regime-fragile**, even if it strictly Pareto-dominates on the full panel under criteria 1-4 of the brief's acceptance set.

The bootstrap and half-panel parts are complementary. Bootstrap captures **block-level regime variance**; half-panel captures **temporally-coherent regime asymmetry**. A candidate can fail one and pass the other; both must clear.

---

## What this gate catches

- **Partition-specific dominance** masquerading as full-panel dominance (Q-DDP-1's C2 result).
- **Panel-regime artifacts** where the candidate's win is concentrated in one sub-period.
- **Sensitivity to block-resampling order** that wouldn't generalize forward.

## What this gate does NOT catch

- **Out-of-distribution regimes the panel never sampled.** A 52mo Pepperstone panel from 2022-01 → 2026-04 contains no 2008-style crisis sample. No bootstrap or split can manufacture data the panel doesn't have. This is the residual uncertainty that justifies keeping the locked config conservative even after the gate clears — there are regimes outside both H1 and H2 that the panel doesn't reach.
- **Continuous non-stationarity** as opposed to block-coherent regimes. Block bootstrap preserves intra-block correlation structure but destroys inter-block ordering; if the actual regime evolves smoothly, the bootstrap distribution will be unrepresentative.
- **Strategy-specific tail risks** that aren't expressed in the panel's MC trajectories (e.g. a strategy that has a structural binary-event tail not represented in its 4yr trade history).

The gate is necessary but not sufficient. A passing candidate still requires the brief author's judgment on the residual uncertainty haircut.

---

## Relationship to other gates

| Gate | Layer | Operates on | When |
|---|---|---|---|
| Rule 0 (audit-first) | Pre-loop | Production source | Before INQHIORI begins |
| Pre-Q gate (D-S-A on data) | Inside INQHIORI | The I/N corpus | Before Q is asked |
| **Regime-robustness gate** | **Inside INQHIORI** | **Candidate configs** | **Before LOCK recommendation** |
| Rule 1 extension (partition-hypothesis permutation) | Post-observation | Specific partition hypotheses | When partition-specific dominance is asserted |
| Observation routing gate | Post-pre-Q | Observations | After Q produces evidence |

These compose; they don't compete. A brief running this gate may also need to run Rule 1 if the gate's failure surfaces a specific partition hypothesis worth formal screening (e.g. "C2 wins in H2 but not H1 — is this stochastic or systematic?"). When in doubt, run both.

---

## Worked example: Q-DDP-1 (2026-05-06)

The first formal application of this gate. Brief asked whether a Pareto-dominant relaxation of `(DD_TRIGGER=1.0%, DD_SCALE=0.40×)` exists under 4-strategy diversification.

Sweep over 5-config grid produced one candidate that passed full-panel acceptance criteria 1-4: **C2 = (1.5%, 0.40×)** with full-panel pass-rate 98.09%, drag savings 25%.

This gate's verdict on C2:

| Test | Result | Floor | Pass? |
|---|---:|---:|:---:|
| Bootstrap 5th-percentile pass-rate | 90.82% | 97.5% | ❌ |
| H1 (2022-01 → 2024-04) pass-rate | 86.78% | 97.5% | ❌ |
| H2 (2024-05 → 2026-04) pass-rate | 99.67% | 97.5% | ✅ |

C2 rejected as **regime-fragile** by the gate. The H1↔H2 spread of 12.9pp is decisive — C2's apparent full-panel dominance was an H2-driven artifact. Brief verdict: AMBIGUOUS / default HOLD.

Without this gate, the sweep would have produced a LOCK CANDIDATE recommendation on C2 with no dissenting evidence. **This gate is the specific reason the regime fragility entered the record.**

**Postscript — 2026-05-08 OVERRIDE.** Joshua subsequently adopted C2 anyway, on broker-feed-resolution + median-pass-time grounds (see `archive/docs/briefs/Q-DDP-1/recommendation.md` OVERRIDE section + `archive/docs/briefs/bust_attribution_flip.md` closure). The gate's regime-fragility signal was preserved as dissent, with a forward revert trigger (rolling 6-month MC pass-rate <95% for two consecutive windows → revert to C0). The methodology value of this worked example is unchanged — the gate **correctly surfaced** fragility evidence; whether to act on that evidence is a separate decision Joshua made on broader information.

---

## Worked non-example: candidate-1 rider (2026-07-15/16)

Documented in [`2026-08-24 ADR — regime-gate scope worked non-example and F1 discharge`](../adr/2026-08-24-regime-gate-scope-worked-nonexample-f1-discharge.md);
summarized here per Rule 14 (corrections land where the error is read).

The `FROZEN` prop-survivor-scoring pre-registration
([G1](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) in the gate-stack
audit's own shorthand) carries, in its §7 freeze list, item 7: *"Regime-robustness caveat — run
the regime gate on the deployable expression before trusting the ceiling result."* That item's own
subject — prop-tier book scoring, not a `dd_protection` Pareto sweep — sits inside this gate's
"Not required" list above. A downstream `FROZEN` pre-registration (the Class-S existing-strategy
book candidate #1 chain, frozen 2026-07-15) imported that item as a per-candidate rider and
pre-declared, **before the gate ran**, that a FAIL would not overturn the candidate's discharge —
only ride into the next gate as a standing caveat.

The rider then ran (2026-07-16) and returned `GATE FAIL (regime-fragile)` on both discharge tiers
(H1 bust ≈4.37%, bootstrap bust 95th-percentile ≈10.4% — both against a 3.0% ceiling). Per the
pre-declared posture, the FAIL did not block anything: the candidate was recorded
`discharges_falsifier: true` and admitted onward with the FAIL noted only as a caveat.

This is not a hard-core violation of the gate's own acceptance criteria — computed honestly, and
the gate-stack programme audit's own theory-comparison pass found the rider's criteria were
*stricter* than this gate's canonical Part C (whose three limbs are pass-rate tests only; the
rider's FAIL was driven partly by a bust limb Part C does not contain) while its *consequence* was
relaxed to non-blocking. The defect is narrower and more specific: importing this gate outside its
own scope, as a rider, with the outcome fixed in advance — bindingness theater, not a broken test.
**Both source documents stay `FROZEN` and byte-unedited** (Trap #12); this section is the
upstream-of-the-claim correction Rule 14 requires, not an edit to either.

---

## Edge cases and boundary conditions

**Panel length.** Block bootstrap requires the panel to have ≥4 candidate blocks at the chosen block size. For 6-month blocks, that means ≥24-month panel minimum. Shorter panels: either reduce block size to 3 months (with documented justification) or reject the brief as unable to clear regime stress.

**Unequal half-panels.** Acceptable. Document the split point. The split should reflect a meaningful regime boundary if one is identifiable; absent that, midpoint is the default.

**Bootstrap n.** Default n=100. For close calls (5th-percentile within 1pp of floor), upgrade to n=200 to reduce 5th-percentile estimator variance.

**All candidates rejected.** That IS the answer. The brief closes with HOLD verdict and the locked config is confirmed. This is not a methodology failure — it's the gate working correctly to surface regime fragility across the entire grid.

**Pre-registered floor.** The gate's pass-rate floor must equal the brief's full-panel pass-rate floor (criterion 1 in standard Pareto sweep). No separate "regime floor" is permitted — that would be a hidden parameter through which post-hoc fitting could enter.

**Sanity checks during execution.**
- Bootstrap 5th-percentile must be ≤ full-panel pass-rate (regime stress is a haircut, not a boost). Violation = bootstrap implementation bug.
- Bootstrap p95 should typically be ≥ full-panel pass-rate. If not, the panel itself is regime-anomalous.
- H1 + H2 path counts should sum approximately to full-panel path count. Material gaps suggest a panel-construction error.

---

## Implementation notes

The procedure above is implementation-agnostic. **Rewritten 2026-08-08:** the two paragraphs that stood here
directed the next author to a template in the evicted `archive/` tree, a `docs/briefs/Q-XXX/` convention that no
longer exists, and a graduation target (`multi_firm_operations/regime_robustness_gate.py`) that predates both the
repo rename and the 2026-06-05 four-layer boundary contract. **The graduation they described has already
happened** — it landed in `core/mc/`, and the doc was never told.

Use, in this order:

1. **Canonical implementation — `core/mc/modes.py::_run_half_panel`.** Its own docstring names the Q-DDP-1 and
   Q-SWAP-3 half-panel patterns as what it mirrors. This is the library the "graduate when a second brief invokes
   it" clause was waiting for; treat the clause as **discharged**, not pending.
2. **Live on-disk reference script — `docs/ltm/briefs/Q-SWAP-3/_run_regime_robustness.py`.** A readable file beats
   a `git show` pointer. ⚠ `docs/ltm/` is excluded from default agent search, so `rg` will not surface it — Read
   the path directly.
3. **Historical original**, if you need the first form:
   `git show pre-prune-2026-06-05:archive/docs/briefs/Q-DDP-1/_run_regime_robustness.py`.
4. **Live templates for the surrounding harness:** `lab/analysis/regime/` and
   `lab/discovery/prop_survivor_scoring.py`.
5. **Before reusing any candidate script, read its own `CANDIDATES` / `CONFIGS` list.** Two of the three
   regime-gate-family scripts contain no unmodified-LOCKED candidate, so a naive re-run silently scores something
   other than the locked config.

A brief invoking this gate writes its script under its own `lab/analysis/<theme>/<slug>/` directory (the 2026-08-03
theme nest), not under a `docs/briefs/` path.

---

## Re-MC trigger registration

A brief that **invokes this gate AND produces a LOCK CANDIDATE** has, by construction, changed a risk constant. That constant change is itself the canonical re-MC trigger. The order of operations:

1. Brief gates clear (including this gate)
2. LOCK CANDIDATE recommendation surfaced to Joshua
3. Joshua approves → constant change committed to production
4. Re-MC fires immediately at the new config (full 4-strategy MC, all locked seeds)
5. ADR drafted documenting the lock decision and re-MC results

Steps 4–5 are not part of the brief that ran this gate — they are downstream consequences. A brief that bundles them is a Rule-0-violating brief and should be rejected.

---

## Provenance

- **2026-05-06 — Q-DDP-1 closure**: gate worked example produced; H1↔H2 spread of 12.9pp on C2 surfaced regime fragility that full-panel sweep missed.
- **2026-05-06 — methodology canonization**: this doc authored.
- **Future calibration**: the bootstrap n=100 and 5th-percentile floor are calibrated to the current panel size and seed count. If the locked panel grows substantially (e.g. to 8+ years post-2030) or seed count changes, re-evaluate whether n and the percentile threshold remain appropriate.

---

## Cross-references

- **INQHIORI canon**: `docs/methodology/inqhiori-canon.md` (§14 three-loop binding); skill `.claude/skills/inqhiori/SKILL.md`
- **Rule 0**: `docs/rule_0.md`
- **Rule 1 extension (partition-hypothesis permutation):** same INQHIORI Rule 1 as canon §12, not a third numeral. Owner [`rule-1-small-cell-variance-prior.md`](archive/notion/rule-1-small-cell-variance-prior.md) (core top-k + 2026-04-24 partition extension). No `rule1_gate.py` exists; the archive gated that script on CFD-era USDJPY OHLC panel ingestion that never landed — implementation is **not pending**. Build only if a live n≤10 / partition investigation needs it ([citation ADR](../adr/2026-08-19-rule-1-citation-not-three-meanings.md)).
- **Observation routing gate**: `docs/methodology/observation_routing.md`
- **Q-DDP-1 worked example**: retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-DDP-1/recommendation.md`
- **Locked dd_protection config**: `core/dd_protection.py` (literals owned there; human summary [`CLAUDE.md`](../../CLAUDE.md) §Protection; C2 relock + concept-not-constant ADRs)
- **MC harness**: `core/portfolio_mc.py` (+ `core/mc/`)
- **Historical MC anchor record**: [`docs/mc_anchor_history.md`](../mc_anchor_history.md) (executable panel pin retired substrate Phase 3; tombstone via `git show pre-prune-2026-08-08:docs/ltm/notes/2026-07-24-pepperstone-executable-anchor-tombstone.md`). **Engine regression (vendor-free):** `tests/core/test_mc_synthetic_engine.py`. Do **not** cite deleted `tests/core/test_mc_anchors.py`. Allocation-refresh-2 override of this gate: [`docs/adr/2026-05-23-allocation-refresh-2.md`](../adr/2026-05-23-allocation-refresh-2.md) §Override.

---

## What this doc does NOT change

- Any locked strategy parameter / version — Pine + [`CLAUDE.md`](../../CLAUDE.md) §Strategy Reference
- Any locked allocation — [`allocation-refresh-2`](../adr/2026-05-23-allocation-refresh-2.md) · `core/firm_rules.py` `_BASE_RISK`
- The locked `dd_protection` config — `core/dd_protection.py` / CLAUDE §Protection
- The MC harness logic
- The full-panel acceptance criteria template for Pareto sweeps (this doc adds a layer on top, doesn't replace)

This is a methodology layer addition. Production state is unaffected. The next time a Pareto-relaxation question on a risk constant gets authored, this gate becomes mandatory criterion 5 (or analogous numbering) in that brief's acceptance set.
