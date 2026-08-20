# Governance friction audit — persona-hierarchy review panel — 2026-08-19

**Trigger:** operator request — repo flagged as preregistration-heavy / ADR-heavy / heavily gated,
specifically re: the "Agentic research team structures" session (persona-hierarchy review panel,
ratified `docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md`).
**Domain (INQHIORI §2):** meta-process — D-S-A applied to the framework itself, not to research data.
**Method:** 4 parallel read agents (persona-panel construction + usage logs; prior self-diet ADRs;
standing ADR/gate checklist; commit-churn quantification) + 1 synthesis pass. Full per-agent evidence
in workflow run `wf_235d4f63-f76`, journal preserved at
`C:\Users\joshu\.claude\projects\C--Users-joshu-multi-firm-operations--claude-worktrees-pr-40-adversarial-review-dc3f72\da9c18ec-1857-4662-be61-ad668bdae2eb\subagents\workflows\wf_235d4f63-f76\journal.jsonl`
(62 KB + 5 per-agent transcripts) — logged here specifically so this artifact doesn't repeat the
evidentiary gap it describes below. Reviewed by a fresh-spawned Head of Governance pass (independence
rule honored — read only this artifact + its own, previously-empty log); see
`docs/personas/head-of-governance-log.md` for that review's findings, including two corrections
folded into this document (the 13-of-18 figure and the same-day PR #59 timeline above) and its own
verdict on whether this spawn met its literal trigger condition.

---

## Headline numbers

- 62 commits in the episode (85fde96 → 3c480b4, under 20 hours wall-clock across 2026-08-18/19,
  6 PRs). **11.3% net-new**, 25.8% rework (the panel finding BLOCKERs in its own design, twice),
  **62.9% pure ceremony** (ADR/ratification, charter versioning, pre-mortem procedure text, merges).
  Process (rework+ceremony) = 88.7% of commits.
- 19 personas built (1, `ceo.md`, marked non-spawnable); **13 of the 18 spawnable ones have never
  fired once** (only cfo/cio/coo/cro/head-of-execution have any log entry).
- Exactly **one real (non-rehearsal) use to date**: GSUB-2, reclassifying two already-parked,
  already-dormant pursuits from PARK to SUBTRACT ~80 days early. 1/3 banked toward the design spec's
  own N=3 falsifier.
- **One deterministic, load-bearing control exists**: the CRO safety-invariant hard-block
  (`.claude/workflows/pre-ratification-adversarial-panel.js` L297-394) — fails closed, real fixed
  defect at commit `84a941a`. Everything else audited below is prose describing a mechanism with no
  runtime footprint yet.
- The panel's own ratifying ADR's self-review scale claims (32-agent, then 44-agent, then 46-agent
  passes) are **unconfirmed by any artifact in the repo** — no `journal.jsonl`, no workflow-run ID,
  for most of them — discovered and downgraded to "editorial pass, unconfirmed scale" only after
  ratification, by a separate parallel branch (PR #59) the same calendar day (~3h48m after the ADR's
  own ratification commit `66410ed`, per PR #59's merge commit `711e4c2`).
- The same day this ADR ratified, a sibling ADR
  (`docs/adr/2026-08-19-great-prune-is-not-grand-subtract.md`) was written solely because the repo's
  governance vocabulary was already colliding with itself. The persona ADR never asks whether it is
  the next collision.

## What's genuinely load-bearing — keep

- CRO safety-invariant hard-block (fails closed, wired into the pipeline that runs).
- The underlying CLAUDE.md safety invariants it restates (dry_run gate, M1-RESOLVED+GO, arm-not-send).
- The GRAND tier itself (CFO/CIO/COO/CRO) — real logged output tied to GSUB-2.
- Ownership map Layers 1–2 (actually consulted; caught the c3 routing gap in GSUB-2).
- `adr-ceremony-tiering.md`'s full/light test — self-applied correctly by this very ADR (landed
  full-tier honestly on a genuine limb-4 fire, not padded, not dodged) and clears its own falsifier
  at 36% light-tier adoption.
- Dedup-first / Rule 0 sub-rules — tier-independent, cheap, and this episode's own backfilled-
  attestation gap (Rule 8 sub-rule 10 was skipped at authoring, caught 4 days later by a separate PR)
  is itself proof they catch real omissions when actually checked.

## Ranked candidates for deletion/simplification (most ceremonial first)

1. **Cross-examination round (design spec §6.6).** Zero implementing code, zero executions, no
   `*-cross-exam-log.md` file exists anywhere. Consumed two adversarial-review cycles (one BLOCKED
   with 6 confirmed BLOCKERs, a recheck that found the fix "visibility-only") reviewing a feature
   never built. **D-test:** unbuilt and self-admitted as such (Great Prune R5 — an obligation whose
   check cannot fire is deletable even when signed).
2. **MAST pre-mortem procedure (§14).** 50-line taxonomy imported from an unrelated paper, needed two
   rounds of self-correction to its own citation arithmetic before ever running once. **D-test:**
   duplicated by a higher-fidelity source already in the corpus (the existing adversarial panel
   already does pre-mortem-style failure enumeration).
3. **Charter versioning / governance-gated self-refinement (§6.4.1).** Trigger needs 2 consecutive
   divergent ratifications; the only real review (GSUB-2) produced zero divergence. **D-test:**
   outside current temporal scope — build when the second divergence is imminent, not before the
   first (mirrors operational_rules.md's "rules earn their place by being paid for").
4. **Preference-anchoring (§10.1) and self-consistency (§10.2) checkpoints.** Sourced from research on
   a different system class (durable personal-agent memory, not review panels). §10.1's trigger (5th
   log entry) is unreachable at current max depth (3 entries, CRO). §10.2's trigger fired at GSUB-2
   and was never executed. **D-test:** source doesn't transfer to this mechanism's actual usage
   pattern.
5. **Citation-diff / independent-dissent flag (§6.3).** Self-labeled "drafted, not wired in,"
   explicitly held until N=3 real data (currently 1/3). **D-test:** enforce its own stated hold —
   remove from standing spec text until the hold clears.
6. **Evidence-Cited / Deviation-from-Precedent log fields (§12).** `check_personas.py`'s required-
   field list was never updated to enforce them; zero real log entries use either field. **D-test:**
   unfalsifiable per Great Prune R5 — a field no gate checks is ceremony regardless of intent.
7. **The 8-persona STAFF tier** (falsifier-analyst, tca-analyst, etc.). Never spawned; trigger
   (strict-D2 STRATEGIC-tier deletes) has never fired. **D-test:** zero pipeline consumption to date
   (Great Prune R1) — collapse to a one-paragraph future-expansion note rather than 8 standing files
   with their own schema/INDEX maintenance surface.

## Structural recommendation

Extend `adr-ceremony-tiering.md`'s logic from document *structure* to apparatus *construction*: no new
checkpoint, companion diagnostic, or persona tier should be drafted into a ratified spec unless it is
either (a) needed by a limb that has already fired, or (b) built when its own trigger is one cycle
from firing — never preemptively, per operational_rules.md's existing "paid for by incident"
discipline. Pair this with a hard cap on self-review recursion for governance-of-governance artifacts:
no more than one automated adversarial pass on a meta-process ADR without a preserved
`journal.jsonl`/workflow-run-ID; a second pass requires operator sign-off rather than another
automated run. That targets the review-*effort* axis specifically, which — unlike document structure —
has no existing stakes-scaling rule anywhere in the repo.

## Disposition

**Authorized and executed, 2026-08-19, with one scope amendment.** Operator authorized items 1–7 in
chat ("cut them and keep them as archived ideas in case they are referenced in future"), with an
explicit carve-out: **"don't delete the front office staff, i am using my front office in a parallel
chat."** Item 7 (originally "the 8-persona STAFF tier") was executed narrowed to the 5 Middle/Back-
office analysts only — Risk Analyst (Intraday), Model Validation Analyst, Robustness Analyst,
Documentation Analyst, Research Registry Analyst. The 3 Front-office Staff (Falsifier Analyst,
Pre-Registration Analyst, TCA Analyst) were left untouched, per operator instruction, regardless of
this audit's original framing — a live concurrent use overrides a paper argument for symmetry.

**What actually moved:**
- Items 1–6 (§6.3 dissent-flag addendum, §6.4.1, §6.6, §10.1, §10.2, §12's extended log fields, §14)
  archived verbatim to
  `docs/superpowers/specs/archive/2026-08-19-persona-hierarchy-archived-sections.md`; live spec left
  with short stub pointers at each original section number.
- 5 Middle/Back-office STAFF personas moved via `git mv` to `docs/personas/archive/`, retired per
  the design spec's own §6.7 procedure; `docs/personas/INDEX.md` updated.
- `scripts/check_personas.py`'s `EXPECTED_COUNT` updated 19 → 14.
- A short addendum added to `docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md` (ratified
  body left byte-unedited, per this repo's own convention) noting the roster/spec counts are now
  stale by design, not drift.

Nothing above has been committed to git yet — working-tree edits only, pending an explicit commit
instruction.

## Iterate

**Next:** none outstanding on this artifact's own scope — executed. Two smaller items surfaced by
the Head of Governance review remain open for a future session, not blocking: (1) the "Structural
recommendation"'s claim of "no existing stakes-scaling rule" for review-panel effort should be
checked against `docs/adr/2026-06-16-rule-2-budget-before-acting.md` before anyone builds the
proposed automated-pass cap; (2) cite full paths, not just workflow-run IDs, when a future audit
references a `journal.jsonl` for its own evidentiary trail — this one now does (see Method above),
matching the sibling convention at `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`.
