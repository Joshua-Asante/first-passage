# Q-NSURV-2 — CLOSURE: `RESOLVED` (additive wrapper reproduces both candidates' headlines within tolerance, zero core internals touched)

**Verdict:** `RESOLVED`
**Closed:** 2026-08-20
**Lane:** `UNASSIGNED`
**Pre-registration:** [`Q-NSURV-2-verdict-preregistration.md`](../pre-registration/Q-NSURV-2-verdict-preregistration.md) — frozen at `97f301f`, corrected pre-Phase-1 (see pre-reg's own Correction note)
**Successor:** [`docs/adr/2026-08-20-nsurv-magnitude-resampling-disclosure.md`](../../adr/2026-08-20-nsurv-magnitude-resampling-disclosure.md) (`Proposed`, ratification owed)
**Spend / K:** $0.00 · K consumed: 0 (design/reproduction check on already-committed artifacts, not a strategy-candidate proposal)
**Live effect:** none — no `dd_protection`/allocation/Pine/rail surface touched; no closed N-SURV verdict re-scored
**Artifacts:** [`run_wrapper_reproduction_check.py`](../../../lab/analysis/c1/nsurv_layer_design_2026-08-20/run_wrapper_reproduction_check.py) · [`wrapper_reproduction_results.json`](../../../lab/analysis/c1/nsurv_layer_design_2026-08-20/wrapper_reproduction_results.json)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | Both candidates reproduce within 2.0pp, zero `run_partition_mc`/`blocks_from_daily_pnl` internals touched, resampled bands additively emitted | Both reproduced (see below); grep audit hook confirms zero matches for `run_partition_mc`/`blocks_from_daily_pnl`/`simulate_path` in the wrapper script | ✓ |
| `FALSIFIED` | Either candidate fails to reproduce within 2.0pp without touching internals | Did not fire | — |
| `AMBIGUOUS-HOLD` | One candidate reproduces, the other does not | Did not fire — both reproduced | — |

Per-candidate reproduction results:

| Candidate | (A) single-history headline echoed | (B) recomputed vs stored — deltas |
|---|---|---|
| c1 book | bust 4.7433% (exact echo) | mean +0.0000pp, sd −0.0710pp (well within 2.0pp) |
| ORB-MNQ-1 | bust 0.0000% / pass 52.2700% (exact echo) | bust_mean +0.0000pp, pass_mean +0.0000pp, pass_sd −0.2429pp (well within 2.0pp) |

The small non-zero sd deltas (−0.07pp, −0.24pp) are population-vs-stored-summary computation nuances (this wrapper uses `statistics.pstdev`; the original artifacts may have used a slightly different percentile/stdev convention), not evidence of a reproduction failure — both are an order of magnitude inside the 2.0pp tolerance.

## 2. What the pre-registration predicted vs what happened

The pre-registration's first draft conflated two different numbers for c1 (labeled `bust_mean`, the resampled-distribution mean, as if it were the "single-history" headline) — caught and corrected before Phase 1 ran (see the pre-registration's own Correction section). Once corrected, the wrapper cleanly separated (A) the fixed single-history reference (echoed, not computed) from (B) the resampled-distribution statistics (independently recomputed from each candidate's `runs[]` array and checked against the artifact's own stored summary). Both candidates passed cleanly, with no surprises in the numbers themselves — the only surprise was in this Q's own first-draft design, not in the underlying data.

## 3. What this closure does NOT license

- Does not re-score, re-open, or invalidate any closed N-SURV verdict's point estimate — both candidates' (A) headlines were echoed exactly, never recomputed.
- Does not authorize wiring the wrapper (or any magnitude-resampling layer) into the live gate's PASS/FAIL logic — this closure's `RESOLVED` verdict licenses only the disclosure-only ADR named as successor above, not a gate-behavior change.
- Does not establish that a third candidate's fitted-family artifact would reproduce equally cleanly — this Q tested exactly the two candidates that exist today.
- Does not claim `Q-NSURV-1`'s own "need a 3rd candidate" bar was met — this closure took the alternate, "principled reason to act on 2" branch explicitly (bounded, additive scope), per `Q-NSURV-2` §5.

## 4. Defects found in the frozen brief (recorded, not repaired)

The pre-registration's original c1 reproduction-target row was corrected pre-Phase-1 (§2 above) — recorded in the pre-registration file itself as a "Correction (pre-Phase-1)" section rather than a silent edit, since it was caught before any result was seen (not a Known-Trap-#12 amendment).

## 5. Lesson candidates

Below the two-incident bar — watch: distinguishing "the fixed real-history reference" from "the resampled-distribution's own summary statistic" is easy to conflate in prose (both are commonly called "the headline") even when the underlying JSON artifacts keep them in clearly separate fields. Worth a second look if a future N-SURV-adjacent artifact shows the same ambiguity.

## Iterate — loop exit

- **Verdict used:** `RESOLVED`
- **Model update:** An additive, headline-preserving magnitude-resampling layer is buildable today, on the two candidates that exist, without touching `run_partition_mc`/`blocks_from_daily_pnl` — confirming H-NSURV-2's affirmative branch. The design cost was near-zero (pure JSON consumption, no simulation code); the actual work was catching and fixing an internal labeling error in the pre-registration itself before it drove a wrong check.
- **Next:** `INTEGRATE`
- **Routing:** the commit is the disclosure-only ADR named above (`docs/adr/2026-08-20-nsurv-magnitude-resampling-disclosure.md`), mirroring the 2026-08-04/08-18 K-bank precedent — authored `Proposed` this session, ratification owed to the operator. No `run_partition_mc`/`blocks_from_daily_pnl` code change; the wrapper script itself stays a reusable reference implementation under `lab/analysis/c1/nsurv_layer_design_2026-08-20/`, not wired into any production path.
- **Entry packet:** n/a for this closure directly (`INTEGRATE`, not `ITERATE`) — the ADR carries its own forward obligations.
- **Stop rule / re-proposal bar:** n/a — integrated.
- **Board write:** `STATE.md` decision index (2026-08-20 entry) + `docs/briefs/INDEX.md` — this Q moves from Open to Recently closed. Owner: this closure.
- **Registry:** n/a — methodology-layer design confirmation, not a strategy-mechanism rejection (no `docs/rejected_candidates.md` row).

## §10 audit-hook discharge

```bash
$ python -c "import json; d=json.load(open('lab/analysis/c1/nsurv_layer_design_2026-08-20/wrapper_reproduction_results.json', encoding='utf-8')); print(d['verdict'], d['overall_reproduction_ok'])"
RESOLVED True

$ grep -n "run_partition_mc\|blocks_from_daily_pnl\|simulate_path" lab/analysis/c1/nsurv_layer_design_2026-08-20/run_wrapper_reproduction_check.py
[no matches -- confirms pure JSON-artifact consumption]

$ git log -1 --format='%h' -- docs/briefs/pre-registration/Q-NSURV-2-verdict-preregistration.md
97f301f
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-20 | Closure authored. Phase 1 executed same day as pre-registration (with a pre-Phase-1 correction to the pre-registration itself), under operator GO ("execute them now"). `RESOLVED` recorded. | Claude Code (Sonnet 5), operator GO |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-NSURV-2-closure-resolved.md
grep -c "Fired?" docs/briefs/closures/Q-NSURV-2-closure-resolved.md
```
