# Notice — The Quintessentials binds above the ML-shaped pipeline, not inside it — and two of its six principles are unwired below GRAND

**Notice ID:** N-2026-08-18-quintessentials-ml-lifecycle-mapping
**Observed:** 2026-08-18
**Author:** Joshua (commission: explore how incorporating "The Quintessentials" decision framework — Aim/Measure/Anchor/Survive/Subtract/Update — may sharpen the generate→evaluate→deploy→measure→update pipeline, and test its viability in this environment) + Claude Code
**Source:** cross-session deep-dive, two verification workflows (`wf_e162d82d-6e8`; `wf_b1b3d57d-38d`) plus direct reads of `docs/adr/2026-08-09-grand-tier-quintessentials-binding.md`, `docs/briefs/GSUB-1-inventory-and-dispositions.md`, `docs/briefs/closures/GSUB-1-closure-resolved-loadbearing.md`
**Status:** `OPEN` → routed below (primary: `DROP`; two supplementary `ACTION` items spawned as background tasks)
**Lives in:** `docs/notes/notice/N-2026-08-18-quintessentials-ml-lifecycle-mapping.md`

---

## §0 — Source anchor

- **Source:** user-supplied Gemini answer mapping "The Quintessentials" onto the DS/ML lifecycle (per-stage: Aim=target definition, Anchor=baseline models, Survive=per-model stress-testing, Subtract=regularization/feature-selection, Update=drift monitoring), checked against `docs/adr/2026-08-09-grand-tier-quintessentials-binding.md` (full read) and its same-day GSUB-1 test artifacts.
- **Observed at:** 2026-08-18, this session.

---

## §1 — The observation

Gemini's mapping places the Quintessentials *inside* the ML pipeline, as governing logic at each build stage. The repo's own ratified binding places it one tier *above* the entire pipeline: **GRAND** (`docs/adr/2026-08-09-grand-tier-quintessentials-binding.md`) governs whether whole **pursuits** (campaigns, lanes, standing explorations, meta-belt items, subscriptions) exist at all, with a downward interface that is explicitly "scoping authority only... never modifies strategy code, locked parameters, allocations, dd_protection, MC calibration" (§2.2). Below GRAND, each of the six principles already has an independent, real analog implementing it inside the pipeline under a different name — four are solid and load-bearing (Aim, Measure, Survive, Update); two are real but fragmented (Anchor, Subtract).

---

## §2 — Why it stands out (the N signal)

- **Baseline:** expectation going in was either "Gemini's per-stage mapping applies cleanly" or "no repo precedent exists at all."
- **Delta:** neither holds. The repo ratified its own, different-altitude binding for the same six-word vocabulary nine days before this conversation (2026-08-09), tested it same day (GSUB-1: 19/37 pursuit dispositions differed from status quo, against a pre-registered bar of ≥1), and its own alternatives analysis (§3) already considered and rejected the exact move Gemini's table implies — folding the Quintessentials into The Algorithm's intra-pipeline operators — on domain-conflation grounds.
- **Frequency:** first instance. A repo-wide grep in the preceding research turn found zero prior hits on "MLOps" / "ML lifecycle" / "CI/CD" anywhere in-tree — no earlier notice or brief has run this external-framework comparison.

---

## §3 — Candidate mechanisms (informal)

- Gemini's answer is generic advisory content authored without repo access — it has no way to know GRAND exists, so it defaulted to the most common placement for a decision-quality framework (inside the build loop). Not a repo defect; an artifact of an outside-context answer meeting an in-repo prior decision.
- The four solid principles may be solid specifically *because* each has a single dedicated artifact driving it (Rule 2 for Measure, `dd_protection.py` for Survive, INQHIORI's Iterate-exit + add-back metric for Update, GRAND's own inheritance clause for Aim), while Anchor and Subtract are each split across ≥2 artifacts that were never designed as one system and only resemble each other in retrospect.
- Could also be noise: Anchor's and Subtract's fragmentation might be intentional non-integration (distinct tools solving distinct problems that happen to share a word) rather than a real gap. Recorded as a live possibility, not resolved here — both spawned tasks are scoped as diagnostics, not prescribed fixes.

---

## §4 — Routing decision

**Primary: DROP.** Reason: the core question — "does the Quintessentials need to be built into the intra-pipeline mechanics the way Gemini's table implies" — is already answered by standing doctrine. `docs/adr/2026-08-09-grand-tier-quintessentials-binding.md` §3 explicitly considered and rejected folding the Quintessentials into The Algorithm as additional operators, on the grounds that Subtract removes *pursuits* and Delete removes *parts within a surviving pursuit* — distinct objects the §2.4 domain guard exists to keep separate. Re-opening that question here would relitigate a ratified decision, itself a forbidden move under that same ADR's §5. No Pre-Q is warranted.

**Supplementary tags** (three-bucket vocabulary, standing as an optional supplementary tag per `docs/adr/2026-08-15-notice-log-is-the-live-observation-routing-convention.md` §2, layered on top of the primary DROP, not replacing it):

| Item | Tag | Detail |
|---|---|---|
| Anchor fragmentation — Rule 1 (`docs/methodology/archive/notion/rule-1-small-cell-variance-prior.md`) and `docs/mc_anchor_history.md` never cross-reference each other; Rule 1 has zero code enforcement (`rule1_gate.py` never landed); Rule 1's name collides with a third, unrelated meaning in `docs/methodology/regime_robustness_gate.md`, deconfliction explicitly deferred at `docs/adr/2026-06-16-rule-2-budget-before-acting.md:26` | **ACTION — discharged 2026-08-19** | Ruled by [`2026-08-19-rule-1-citation-not-three-meanings.md`](../../adr/2026-08-19-rule-1-citation-not-three-meanings.md): same Rule 1 (gate row = 2026-04-24 extension, no rename); do not build `rule1_gate.py`; do not sibling-wire `mc_anchor_history.md`. Spawned as background task `task_06830dbb` — "Resolve Anchor discipline fragmentation (Rule 1 / mc_anchor_history)" (re-spawned 2026-08-18 after original chip `task_28f5754f` was orphaned by an app restart before it could be actioned; original diagnosis unaffected by the intervening 30-commit fast-forward to origin/main) |
| Subtract cross-tier silence — the Great Prune retention test (`docs/adr/2026-08-08-great-prune.md`) and GRAND's pursuit-Subtract are asserted as the same conceptual family by the GRAND ADR's own §2.4 handoff clause ("Subtract (pursuits) → Delete (parts)"), but neither document cites the other anywhere | **ACTION** | Spawned as background task `task_73c5d74d` — "Cross-reference Great Prune retention test with GRAND's pursuit-Subtract" (re-spawned 2026-08-18 after original chip `task_97f468bb` was orphaned the same way; gap re-confirmed still open post-fast-forward — `inqhiori-canon.md` §14 gained a `strategy_lifecycle.md` pointer in the sync but still has zero mention of Great Prune) |

Both ACTION items are diagnostic-first: each spawned task is instructed to confirm the gap, then recommend whether a minimal cross-reference/rename is warranted or whether the artifacts are legitimately independent — neither is authorized to rewrite locked doctrine or silently amend an Accepted ADR.

**Addendum (2026-08-18, post-fast-forward):** this branch fast-forwarded 698c47b→4a828c7 (30 commits). Two DROP-adjacent findings from this notice's original research were independently fixed upstream in the interim, outside this notice's own routing: the dead `ConceptRecords` stage-1 citation (session `2026-08-18r`) and the stage-5 STRATEGIC-vs-WATCH ownership conflict between `systematic-trading-lifecycle.md` and `strategy_lifecycle.md` (same sync). Neither fix originated from this notice's chips — both chips (`task_d902f070`, `task_54f23e28`) were orphaned by an app restart before they could be actioned; the fixes landed via other, unrelated work. No action needed here; recorded for the audit trail.

---

## §10 — Audit hooks

```bash
# Confirm this notice does not get read later as grounds to reopen GRAND's §3 alternatives ruling
grep -rn "N-2026-08-18-quintessentials-ml-lifecycle-mapping" docs/adr/2026-08-09-grand-tier-quintessentials-binding.md
# Expected: no hit — this notice DROPS the core question, it does not reopen §3

# Anchor ACTION item discharge check
grep -n "Rule 1" docs/adr/2026-06-16-rule-2-budget-before-acting.md
# Expected (pre-fix, today): line ~26, namespace-collision flag, "deconfliction out of scope"
# Expected (post-fix): collision resolved, re-scoped, or explicitly ruled non-issue

# Subtract ACTION item discharge check
grep -l "Great Prune" docs/adr/2026-08-09-grand-tier-quintessentials-binding.md docs/methodology/inqhiori-canon.md
# Expected (pre-fix, today): no hit in either file
# Expected (post-fix): at least one cross-reference lands, or the diagnostic explicitly rules it unnecessary
```

---

## Verification

```bash
# Discipline checks (mechanical — notice type is lighter)
$ python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/notes/notice/N-2026-08-18-quintessentials-ml-lifecycle-mapping.md --type notice
# Expected: §0 source / §1 observation / §2 baseline+delta / §4 routing decision all present
```
