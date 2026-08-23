# Q-ORBSURV-1 — Does cushion-proportional sizing clear the frozen survivor-scoring gate on the ORB-MNQ-1/Tradeify configurations today's informal probes didn't already check?

**Status:** `CLOSED-FALSIFIED 2026-08-20` — full-panel k=2 misses the pass floor (41.51% < 50%); cushion sizing's gate-clear is k-dependent, not a robust property. Closure: [`closures/Q-ORBSURV-1-closure-falsified.md`](closures/Q-ORBSURV-1-closure-falsified.md).
**Authored:** 2026-08-20
**Closed:** 2026-08-20
**Authors:** Joshua (operator election: "go bigger — open formal Pre-Qs") + Claude Code (Sonnet 5)
**Parent question:** `N/A` — forks from the deferred re-PARK-scope half of `Q-NSURV-1`'s named forward obligation, but is its own, narrower question (see §2)
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gates whether cushion-sizing's gate-clear is a robust property across configurations, or configuration-dependent
**Artifact path:** `docs/briefs/Q-ORBSURV-1-cushion-sizing-gate-configurations.md`

---

## §0 — Rule 0 reads (production-source verification)

- `docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md` §4/§5 — anchor `027a729` (verified `git log -1` 2026-08-20). §4's falsifier H′ is scoped to "k∈{1,2,3}" under the flat-sizing engine `run_t2_intraday_bust.py` measured; §5 explicitly separates "falsifying ORB-MNQ as a mechanism" (not done) from "falsifying one target" (done); none of R1/R2/R3 name a sizing-mechanism change.
- `lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py` (`pol_cushion`, L289–292; `day_loop_intraday`, L295–358) — anchor `b84544a` (2026-08-20). Confirms `pol_cushion` is a dynamic, state-dependent multiplier (`0.75 * min(1, max(bal-(peak-DD),0)/DD)`), recomputed per step from live balance/peak — categorically different from a static risk% haircut, and confirms the fidelity control reproduces the ADR's own flat-sizing 67.67%/77.01% figures before any policy read (i.e., the ADR's baseline measurement was flat sizing).
- `lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/evalseq_orb_intraday_results.json` — anchor `b84544a` (2026-08-20). Contains the already-measured halves-split cushion results at both k=1 AND k=2 — the full-panel k=2 gate check and the isolated post-break sub-window are NOT in this artifact (halves only, not the full-panel single-history read, and not a post-break-only isolation).
- `lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/nsurv_magnitude_probe_results.json` §"real_single_history_cushion" — anchor `bf81496` (2026-08-20). The only full-panel, single-history gate check performed so far is at **k=1**: bust 0.0000% / pass 52.2700%, `floor_ok=True`.
- `docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md` — anchor `bcef3e0` (2026-08-20). Confirms the 2021-09-28 regime break is real, triple-verified, and its mechanism is `STOP`ped (tail-methodology-exhaustion) — this Q treats the break as a given boundary, not a reopened mechanism question.
- `git log --diff-filter=A -- "lab/analysis/c1/q_evalseq_1_2026-08/*"` confirms `pol_cushion`'s first commit is `a7c6f7b`, dated 2026-08-16 — 13 days after the 2026-08-03 re-PARK ADR, confirming the ADR's falsifier could not have contemplated this sizing mechanism.
- `docs/pursuits/b3-orb-mnq-payability-line.md` — anchor (file content read 2026-08-20; unversioned single-page pursuit record). Re-entry criterion: "new payability / cost-geometry evidence at an admissible venue"; expiry 2026-11-08.

---

## §1 — Context & motivation

Today's informal, adversarially-verified probes (`orbmnq1_cushion_sizing_probe_2026-08-20`, `orbmnq1_nsurv_magnitude_probe_2026-08-20`, `orbmnq1_skew_sizing_probe_2026-08-20`) found that cushion-proportional sizing eliminates ORB-MNQ-1's Tradeify bust entirely and clears the frozen survivor-scoring gate at k=1 on the full real-history panel (bust 0.00%, pass 52.27%). But the informal probes only ever checked the FULL panel at k=1, and the halves/thirds split at k=1 and k=2 separately — never the full-panel gate check at k=2, and never the post-2021-09-28 sub-window in isolation against the frozen gate (the thirds-split numbers imply what it would show, but that implication has not itself been gated). The re-PARK ADR's own §5 forbidden moves and unedited §4 falsifier confirm cushion sizing was never in scope for that ADR — it postdates it by 13 days (`Q-EVALSEQ-1`, first committed 2026-08-16). Separately, `docs/pursuits/b3-orb-mnq-payability-line.md` PARKs ORB-MNQ under a 2026-11-08 auto-`SUBTRACT` clock with a re-entry bar of "new payability / cost-geometry evidence" — today's finding is a candidate for that bar, but only once measured completely, not partially.

## §2 — Prior art / lineage

- `docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md` (`Accepted`) — falsifies the flat-sizing Tradeify target only; this Q tests whether cushion sizing clears where flat sizing didn't, on the configurations not yet checked.
- `docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md` (`FALSIFIED`, `STOP`) — the regime break this Q treats as a fixed, unexplained boundary; not reopened here.
- `docs/briefs/closures/Q-NSURV-1-closure-resolved.md` (`RESOLVED`) — the pass-axis uncertainty finding this Q's own gate-clear reads must carry forward as a disclosure (§5).
- `docs/pursuits/b3-orb-mnq-payability-line.md` — the GSUB-1 PARK record whose re-entry criterion this Q's `RESOLVED` verdict would (partially) speak to, without itself triggering renewal.

## §3 — Question (Q-ORBSURV-1)

**Q-ORBSURV-1:** Across the specific gate-check configurations today's informal probes left unmeasured — full-panel k=2, and the post-2021-09-28 sub-window in isolation at k=1 and k=2 — does cushion-proportional sizing clear the frozen survivor-scoring gate (bust≤3.0% ∧ pass≥50%), or is the gate-clear found at k=1/full-panel a configuration-specific result rather than a robust property of the mechanism?

## §4 — Falsifiable hypothesis (H-ORBSURV-1)

**H-ORBSURV-1:** If cushion-proportional sizing (`pol_cushion`, ceiling 0.75, unedited — the skew-sizing null probe already found no beatable alternative) clears the frozen gate at full-panel k=2, AND clears it on the post-2021-09-28-only sub-window in isolation at both k=1 and k=2, then cushion-sized ORB-MNQ-1 has now cleared the gate on every configuration this thread (today's probes plus this Q) has measured — which is the evidentiary floor `docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md`'s own R3 doctrine requires *before* any re-entry proposal. This Q's `RESOLVED` verdict records that floor as measured; it does **not** itself authorize unparking (§5). Otherwise — any of the three checks misses the gate — cushion sizing's gate-clear is configuration-dependent, which caps what any future re-entry proposal can honestly claim and is recorded as a negative finding.

**Reject H-ORBSURV-1 if:** ANY of the three checks (full-panel k=2; post-break-only k=1; post-break-only k=2) misses bust≤3.0% OR pass≥50%.
**Accept H-ORBSURV-1 if:** ALL THREE clear both limbs.
**Ambiguous-hold if:** the post-2021-09-28 sub-window forms fewer than 20 Mon-anchored 5-day blocks (mirroring `Q-ORBCUSH-1`'s own sparsity-floor logic, translated from trade-count to block-count) — re-test as the panel extends past that floor.

---

## §5 — Forbidden moves

- **Treating a `RESOLVED` verdict here as authorization to unpark ORB-MNQ-1, open a re-entry ADR, or renew GSUB-1's `b3` PARK.** Genuinely tempting — a full-clear result reads like a green light. Ruled out because this Q answers a narrower "has the evidentiary floor been measured" question; the re-PARK ADR's own R3 doctrine requires a survivor-scoring pass **before** unparking, but does not say a passing Q auto-executes the unpark — that stays a fresh, separate operator GO.
- **Citing this Q's pass% numbers without the N-SURV pass-axis caveat.** Any pass-rate this Q reports must carry the same "coin-flip-adjacent, not a comfortable margin" disclosure `ops/instruments/MNQ.md` N18 already established for the k=1/full-panel read — the same magnitude-resampling uncertainty applies to every configuration this Q measures, not just the one already checked.
- **Re-opening `Q-ORBCUSH-1` (regime-break mechanism), `STOP`ped under tail-methodology-exhaustion.** This Q does not propose a third mechanism candidate; it treats the 2021-09-28 break as a given, unexplained boundary and only asks whether the gate clears on each side of it.
- **Re-deriving the already-measured k=1 full-panel number.** Reuse `nsurv_magnitude_probe_results.json`'s `real_single_history_cushion` verbatim; re-running it is not a fresh test and would misrepresent this Q's own scope (Trap #12-adjacent).
- **Adjusting the 0.75 ceiling constant.** The skew-sizing null probe already checked and rejected both a looser (1.00) and tighter (0.50) ceiling on pass-rate grounds; this Q inherits 0.75 unedited, no mid-test renegotiation.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | All three unmeasured configurations clear bust≤3.0% ∧ pass≥50% | `INTEGRATE — record as an ADR addendum to the 2026-08-03 re-PARK ADR (scope-only: cushion sizing measured outside its falsifier, evidentiary floor met); no unpark, no b3 renewal executed here` |
| `FALSIFIED` | Any of the three configurations misses either limb | `STOP — cushion sizing's gate-clear is configuration-dependent, not a robust mechanism property; re-proposal bar: a genuinely different sizing mechanism, not a re-tuned ceiling or a re-picked configuration` |
| `AMBIGUOUS-HOLD` | Post-break sub-window has < 20 Mon-anchored 5-day blocks | `ITERATE — re-test once the panel extends past the block-count floor; no re-test date set (panel-growth-triggered, not calendar-triggered)` |

---

## §7 — Execution plan

Self-executing — extends the already-verified, adversarially-checked harness (`run_evalseq_orb_intraday.py`) without modifying it.

- **Phase 0 — Rule-0 reads.** §0 above, already done.
- **Phase 1 — Full-panel k=2 gate check.** New script under `lab/analysis/c1/orbmnq1_survivor_scoring_2026-08-20/`, importing `pol_cushion`/`build_paths_orb`/`day_loop_intraday`/`build_k_panel`/`blocks_from_panel` unchanged from the cushion probe; run on the FULL panel (not halved) at k=2, frozen seeds/thresholds from `load_scoring_thresholds()`.
- **Phase 2 — Post-break sub-window isolation.** Same imports, panel sliced to dates ≥ 2021-09-28 (the `Q-ORBCUSH-1`-established break date), at both k=1 and k=2; block-count check against the Ambiguous-hold floor before trusting the result.
- **Phase 3 — Verdict assertion.** Run the §6 gate against all three results; produce closure artifact per §9, carrying the N-SURV pass-axis caveat (§5) into every pass% citation.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

`docs/briefs/pre-registration/Q-ORBSURV-1-verdict-preregistration.md` — frozen before Phase 1 runs.

Pre-registration commit hash: `<populated at pre-registration commit>`
Pre-registration date: 2026-08-20

---

## §9 — Closure record format

Per `references/closure_record.md`. `RESOLVED` → `docs/briefs/closures/Q-ORBSURV-1-closure-resolved.md`; `FALSIFIED` → `...-closure-falsified.md`; `AMBIGUOUS-HOLD` → `...-closure-ambiguous.md`.

---

## §10 — Audit hooks (runnable)

```bash
# Confirm §0 anchors still resolve
git log -1 --format='%h' -- docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md   # expect 027a729
git log -1 --format='%h' -- lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py  # expect b84544a

# Confirm pol_cushion first-commit date (the "postdates the ADR" claim)
git log --diff-filter=A --format='%ad %h' --date=short -- "lab/analysis/c1/q_evalseq_1_2026-08/*"
# Expected: 2026-08-16, after the 2026-08-03 ADR

# Confirm the k=1 full-panel number this Q reuses (not re-derives)
python -c "import json; d=json.load(open('lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/nsurv_magnitude_probe_results.json', encoding='utf-8')); print(d['real_single_history_cushion'])"
# Expected: bust 0.0, pass 52.27, equivalence_ok True

# Re-run Phase 1/2 (once scripts land)
python lab/analysis/c1/orbmnq1_survivor_scoring_2026-08-20/run_full_k2_and_postbreak_gate.py
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-ORBSURV-1-cushion-sizing-gate-configurations.md --type inquire

git log -1 --format='%h %ci' -- docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md
git log -1 --format='%h %ci' -- docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md

git log --oneline docs/briefs/pre-registration/Q-ORBSURV-1-verdict-preregistration.md
# Expected: pre-registration commit predates first Phase 1 script run
```

## Pre-Lock Checklist (DRAFT briefs only)

- [x] All §0 paths read and anchored with commit hash
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 hypothesis is genuinely falsifiable (binary triggers in §6)
- [x] §5 forbidden moves are genuinely tempting, not strawmen
- [x] §6 gates have specific numerical triggers
- [x] §8 pre-registration committed BEFORE Phase 1 runs — frozen at `97f301f`, same day as Phase 1/2 execution, operator GO ("execute them now")
- [x] §10 audit hooks are runnable commands
- [x] Verification block executed and passing — see [`closures/Q-ORBSURV-1-closure-falsified.md`](closures/Q-ORBSURV-1-closure-falsified.md) §10 audit-hook discharge
