# Q-NSURV-1 — CLOSURE: `RESOLVED` (single-history magnitude blindspot confirmed general, not idiosyncratic to c1 — mechanism differs by sizing shape)

**Verdict:** `RESOLVED`
**Closed:** 2026-08-20
**Lane:** `UNASSIGNED`
**Pre-registration:** none filed — see brief §8 honesty note (retrospective synthesis of two already-verified measurements, not a fresh blind test)
**Successor:** none named — the deferred fix-design question is explicitly not opened here (operator direction, 2026-08-20: address in a future session)
**Spend / K:** $0.00 · K consumed: 0 (methodology-layer synthesis, not a strategy-candidate proposal)
**Live effect:** none — no `dd_protection`/allocation/Pine/rail surface touched; no closed N-SURV verdict re-opened or re-scored (§5, frozen)
**Artifacts:** [`characterize.json`](../../../lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/characterize.json) (candidate 1) · [`orbmnq1_nsurv_magnitude_probe_2026-08-20/`](../../../lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/) (candidate 2)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | second candidate shows material spread (resampled sd ≥5pp OR combined-gate clear rate ≤80%) on ≥1 gate-relevant axis | ORB-MNQ-1 pass-axis sd **24.17pp** (≫5pp); combined-gate clear rate **50.0%** (≪80%) | ✓ |
| `FALSIFIED` | second candidate shows no material spread on any axis | did not fire | — |
| `AMBIGUOUS-HOLD` | second candidate's fit-quality control fails | fit-quality PASS on the load-bearing axis (worst-day tail: real −$783.82 vs synthetic median −$786.94, real value at the 52nd percentile of 50 synthetic worst-days) — did not fire. Skew itself under-fit (all 50 draws undershoot real +2.09; independently re-derived analytically as a structural method-of-moments property, not sampling luck) — disclosed, does not invalidate the tail-driven gate result | — |

Two candidates, two different axes carrying the uncertainty:

| Candidate | Sizing mechanism | Axis with material spread | Resampled sd | Single-history read vs. distribution |
|---|---|---|---|---|
| c1 book (2026-08-15) | flat/constant-risk | bust% | 7.07pp | single-history bust (4.74%) at ~44th percentile; 30% of realizations clear the gate |
| ORB-MNQ-1 (2026-08-20) | cushion-proportional | pass% (bust saturated at 0.00%, sd=0) | 24.17pp | single-history pass (52.27%) at ~52nd percentile; 50% of realizations clear the combined gate |

## 2. What the pre-registration predicted vs what happened

No pre-registration was filed (brief §8) — this section instead records what the parent Notice's own §5 anticipated vs what actually happened. The Notice named three candidate mechanisms (A: general gap, B: small-sample estimation noise, C: idiosyncratic to c1) and explicitly said only C could be ruled out by a second candidate showing "a comparably wide gap ... even without skew" — the Notice's own drop-trigger was written for the *opposite* finding (a symmetric candidate also showing the gap, which would broaden the finding beyond skew-heavy books). What actually happened is different from both the Notice's main scenario and its drop-trigger: the second candidate (ORB-MNQ-1, also skew-heavy, +2.09) showed the gap, but on a *different axis* than the first candidate, because its sizing mechanism (cushion-proportional) structurally eliminates bust-axis variance that flat sizing doesn't. This is a genuine surprise the Notice's own three-mechanism framing didn't anticipate: the gap's *existence* generalizes, but its *location* (which axis) is mechanism-dependent, not book-dependent. Mechanism B (small-sample estimation noise) also gains a data point against it being the *sole* explanation — two independently-fitted families, different underlying data, both show real spread on their respective load-bearing axis, which is harder to explain by estimation noise in one fit alone.

## 3. What this closure does NOT license

- Does not re-open, invalidate, or re-score any specific closed N-SURV verdict (Q-TXG-1, Guardian→MGC, Q-COMPOSE-1, ORB-MNQ-1's own prior verdicts, c1's historical record) — carried forward from the parent Notice's own forbidden-moves list, unchanged.
- Does not license building a fix (a second uncertainty layer in `run_partition_mc`, magnitude-resampling wired into the live gate) — explicitly deferred to a future session per operator direction (2026-08-20), not opened here.
- Does not establish the *magnitude* of the blindspot as a fixed number applicable estate-wide — two data points show it's real and material, not what its size is for any third candidate not yet tested.
- Does not close G5 envelope rule E3's missing level (`docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md` §5.4) — sharpens why it matters, same as the parent Notice already said, still open.

## 4. Defects found in the frozen brief (recorded, not repaired)

None — no frozen artifact predates this closure to carry a defect (§8, no separate pre-registration filed).

## 5. Lesson candidates

Below the two-incident bar — watch, but a strong candidate: the estate's entire N-SURV survival-scoring convention has now shown a real, non-trivial single-history-vs-magnitude-resampled gap on 2 of 2 candidates tested, on two structurally different sizing mechanisms. If a third candidate (a future N-SURV-gated book, tested the same way) also shows it, this graduates from "candidate" to load-bearing with a real counterfactual: every closed N-SURV verdict in this estate — a meaningful count — would need this caveat attached, or the gate itself would need a second uncertainty layer. Watch for a third data point before either escalating or letting this quietly stop being watched.

## Iterate — loop exit

- **Verdict used:** `RESOLVED`
- **Model update:** The single-history magnitude blindspot is confirmed general (Mechanism A supported over C), not idiosyncratic to the one book that first surfaced it — but its *location* is mechanism-dependent (bust-axis for flat sizing, pass-axis for cushion-proportional sizing), a nuance neither the original Notice nor this Q's own §4 hypothesis anticipated in that specific form. The parent Notice's three-way mechanism split (A/B/C) undersold how the finding could generalize in shape while still needing case-by-case axis identification.
- **Next:** `INTEGRATE`
- **Routing:** Parent Notice `N-2026-08-15-nsurv-single-history-magnitude-blindspot.md` graduates `HOLD` → `GRADUATED (via Q-NSURV-1)` — status updated in the same commit as this closure. The deferred question this unblocks — does the estate's N-SURV gate need a second uncertainty layer, and if so on which axis per candidate — is named explicitly as a forward obligation for a future session (operator direction, 2026-08-20), not opened as a successor Q here.
- **Entry packet:** n/a for this closure directly (INTEGRATE, not ITERATE) — but the named forward obligation above should carry, when opened: both candidates' full data (this closure's §1 table), the axis-dependency finding (§2), and the forbidden-move against treating either candidate's specific clear-rate as a general correction factor (§3, first bullet's spirit extended).
- **Stop rule / re-proposal bar:** n/a — integrated. The *forward* question (fix design) has its own bar when opened: needs a third candidate or a principled reason to act on 2, given axis-dependency was already a surprise once.
- **Board write:** `STATE.md` decision index (2026-08-20 entry) + `OPERATOR QUEUE` item #3 (N-SURV fix-design + ORB-MNQ-1 re-PARK scope question, deferred to next session per operator direction). Owner: this closure.
- **Registry:** n/a — methodology-layer confirmation, not a strategy-mechanism rejection (no `docs/rejected_candidates.md` row)

## §10 audit-hook discharge

```bash
$ git log -1 --format='%h' -- lab/discovery/prop_survivor_scoring.py
027a729
$ git log -1 --format='%h' -- docs/notes/notice/N-2026-08-15-nsurv-single-history-magnitude-blindspot.md
19139a7
$ python -c "import json; d=json.load(open('lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/characterize.json', encoding='utf-8')); print(d['bust_mean'], d['bust_sd'])"
[reproduces 0.0746 0.0707 -- candidate 1, unchanged from 2026-08-15]
$ grep -n "Status" docs/notes/notice/N-2026-08-15-nsurv-single-history-magnitude-blindspot.md
[confirms GRADUATED, updated same commit as this closure]
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-20 | Brief and closure authored same day, retrospectively synthesizing two already-independently-verified measurements. RESOLVED recorded. Parent Notice graduated. | Claude Code (Sonnet 5), operator direction ("graduate N-SURV") |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-NSURV-1-closure-resolved.md
grep -c "Fired?" docs/briefs/closures/Q-NSURV-1-closure-resolved.md
```
