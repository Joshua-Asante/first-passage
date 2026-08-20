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

**Sub-rule 10 attestation (amendment-first — backfilled 2026-08-19, found missing by a Research
Registry Analyst test spawn, see §Disposition below).** Executed: `ls docs/notes/audits/` and
`ls docs/notes/audits/programme-audit/` — nearest existing owner is
[`docs/notes/audits/programme-audit/2026-08-15-governance-belt-meta-audit.md`](programme-audit/2026-08-15-governance-belt-meta-audit.md),
a formal programme-audit-protocol run over the meta/governance layer 4 days prior, itself noting the
local convention: "the protocol and the local precedent... file triggered audits as new artifacts."
**New file is correct** — this is a lighter, operator-triggered note (not a programme-audit-protocol
run: no ablation, no degeneration-signal intake, no consecutive-tally count), on a narrower scope
(one specific review-panel episode, not the whole meta/governance belt) — but should have named that
sibling explicitly at authoring time instead of omitting the attestation step entirely, which is
exactly the failure sub-rule 10 exists to prevent regardless of whether the eventual judgment call
turns out right.

---

## Headline numbers

- **Commit-count correction (2026-08-19, found by a Documentation Analyst test spawn — see
  §Disposition):** the original "62 commits (85fde96 → 3c480b4)" framing cited two endpoint SHAs as
  if they made the count reproducible; they don't — a plain `git log --oneline 85fde96..3c480b4`
  returns 72 commits (includes 4 concurrent, unrelated PRs), not 62. The actual methodology was a
  content filter, not a range: `git log --oneline --all --grep="persona" -i 3c480b4` (bounded at
  the original HEAD, before this session's own later commits) returns **61** commits mentioning
  "persona" anywhere in the message, reachable from that point. The original "62" (stated as "59
  grep-matched + 3 path-matched misses") is close but not exactly reproducible from this rerun —
  likely a minor difference in which "personal"-substring false positives were excluded or in exact
  path-matched additions; both figures support the same substantive point (a large majority of the
  episode's commits are process, not decision), and the qualitative ratios below are not sensitive
  to a ~1-commit discrepancy. Treat "~60 commits" as the honest precision level, not "62" as a fact.
  Under 20 hours wall-clock across 2026-08-18/19, 6 PRs. **11.3% net-new**, 25.8% rework (the panel
  finding BLOCKERs in its own design, twice), **62.9% pure ceremony** (ADR/ratification, charter
  versioning, pre-mortem procedure text, merges). Process (rework+ceremony) = 88.7% of commits —
  these ratios were computed by the original commit-churn agent against its own classified sample
  and are not re-derived here; treat them as directionally reliable, not to the same decimal
  precision as the corrected headline count above.
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

## Ranked candidates for deletion/simplification — ORIGINAL PASS (superseded, see §Disposition)

This section is kept verbatim as the original, pre-test proposal — several items below were
corrected after actually testing them against real repo evidence (operator pushback, 2026-08-19).
**Read the Disposition section below for what's actually true now; treat this list as historical.**

1. ~~**Cross-examination round (design spec §6.6).**~~ Tested 2026-08-19: confirmed no disputed
   Stage-1 finding has ever occurred in real panel history. Stays archived — genuinely blocked on
   data, not just "unbuilt."
2. ~~**MAST pre-mortem procedure (§14).**~~ **Corrected 2026-08-19 — restored, not cut.** Run for
   real against GSUB-2's preserved journal; produced 2 genuine findings the existing panel mechanism
   had not caught. The "duplicated by a higher-fidelity source" D-test was wrong.
3. **Charter versioning / governance-gated self-refinement (§6.4.1).** Confirmed blocked on data
   (0 divergence events exist) — stays archived, same disposition as originally proposed.
4. **Preference-anchoring (§10.1).** Confirmed blocked on data (max log depth 3, trigger needs 5) —
   stays archived, same disposition as originally proposed. **Self-consistency (§10.2)** — tested
   2026-08-19 (3 blinded CRO resamples against the frozen GSUB-2 artifact, majority `clean:true`,
   matched the real panel verdict); discharged as the bounded 1-2-use side experiment it was
   designed to be — result logged at `docs/personas/cro-log.md`, spec text stays archived since
   nothing about it was meant to be standing.
5. **Citation-diff / independent-dissent flag (§6.3).** **Stronger evidence now, not just "held":**
   tested 2026-08-19 against GSUB-2's real findings — the severity+location heuristic produced a
   false positive (flagged two unrelated findings as "independently-sourced dissent"). Needs a
   same-item/same-nomination constraint before re-proposing, not just N=3 data.
6. **Evidence-Cited / Deviation-from-Precedent log fields (§12).** Untested — cheap either way, no
   real deviation event exists yet to show whether the field would ever carry signal. Operator's
   call; not restored, not further argued against.
7. ~~**The 8-persona STAFF tier.**~~ **Corrected 2026-08-19 — narrowed.** Tested by spawning all 5
   archived Middle/Back-office analysts against real repo artifacts. 2 of 5 (Documentation Analyst,
   Research Registry Analyst) found genuine, previously-uncaught defects on first use — restored,
   see their new log entries. 3 of 5 (Risk Analyst Intraday, Model Validation Analyst, Robustness
   Analyst) came back clean against the one target tried (a CME data-panel ADR) — but that target
   turned out not to touch any of their three domains (dd_protection/DSR/regime-robustness), so this
   is an inconclusive test, not a negative one. Stay archived pending a better-fitting real target,
   not because they were shown not to add value.

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

That first pass was committed (`dd23588`, `72f8332`) and pushed to PR #63. **Before merge, operator
pushback (2026-08-19, same day): "push back on archiving all of the spec extensions and STAFF
personas, because they are brand new and haven't had a chance to be used yet... test them to see if
they would earn their keep based on existing evidence we have in the repo."** This is a materially
different, correct standard — "never fired because 5 days old" is not the same claim as "tested and
found not to earn its keep." Re-tested every archived item against real, already-existing repo
evidence (no new decisions manufactured to generate fodder):

- **§14 MAST pre-mortem — restored.** Run for real against GSUB-2's preserved journal
  (`wf_e016a5d9-3f6`, still on disk). Found 2 genuine issues the panel's existing verify stage had
  not caught (synthesis ignoring CRO's clean rationale; a trimmed/misleading quote in the original
  CIO-lens BLOCKER, itself caught by the verify stage but evidence the citation-integrity gap is
  real). Falsifies the original archival rationale. Moved back into the live spec at §14.
- **§10.2 self-consistency checkpoint — discharged, not restored.** Ran the actual side-experiment:
  3 fresh, blinded CRO samples against the frozen GSUB-2 brief, majority `clean:true`, matching the
  real panel's verdict (one sample independently found the same NIT the real CIO lens raised).
  Result logged at `docs/personas/cro-log.md`. Spec text stays archived — it was designed as a
  bounded 1-2-use diagnostic, not a standing mechanism, and it has now been used.
- **§6.3 citation-diff flag — stays archived, on stronger evidence.** Ran the actual deterministic
  rule against GSUB-2's real findings: it produced a false positive (flagged CIO's BLOCKER and
  COO's unrelated CONCERN as "independently-sourced dissent" purely on severity+location
  mismatch — the two findings aren't about the same question). Needs redesign before re-proposing.
- **§6.6 cross-exam round, §6.4.1 self-refinement, §10.1 preference-anchoring — stay archived,
  confirmed genuinely blocked on data**, not deprioritized: checked real panel history for each
  trigger precondition (a disputed finding; 2 consecutive divergent ratifications; a 5th real log
  entry) and none has occurred. No amount of testing changes this — the world hasn't produced the
  event yet.
- **STAFF tier — narrowed from 5 archived to 3.** Spawned all 5 archived Middle/Back-office
  analysts against real artifacts. **Documentation Analyst** and **Research Registry Analyst**
  found genuine, previously-uncaught defects in this very audit note on first use (see their new
  log entries, and the two corrections above) — restored to `docs/personas/`. Risk Analyst
  (Intraday), Model Validation Analyst, and Robustness Analyst came back clean against the one
  target tried (a CME data-panel ADR outside all three of their domains) — inconclusive, not
  negative; stay archived pending a naturally-occurring, better-fitting target.
- **§12 extended log fields** — untested, left as originally proposed (archived); cheap either way.

**Net effect on the original commit's scope:** of the original 7 candidates, 1 fully reversed
(§14), 1 discharged-not-restored (§10.2), 1 strengthened (§6.3), 3 confirmed unchanged (§6.4.1,
§6.6, §10.1), 1 left as a toss-up (§12). Of 5 archived STAFF personas, 2 restored. Front-office
Staff were never in scope for any of this (excluded from the original cut per operator instruction;
untouched throughout).

This correction round is committed as a separate commit on the same PR #63 branch, not a rewrite of
history — the original archival commit stands, this one partially reverses it with cited evidence.

## Iterate

**Next:** none outstanding on this artifact's own scope — executed, tested, corrected. Two smaller
items remain open for a future session, not blocking: (1) the "Structural recommendation"'s claim
of "no existing stakes-scaling rule" for review-panel effort should be checked against
`docs/adr/2026-06-16-rule-2-budget-before-acting.md` before anyone builds the proposed
automated-pass cap (Head of Governance's own flag, still unchecked); (2) Risk Analyst (Intraday),
Model Validation Analyst, and Robustness Analyst should be re-tested against a naturally-occurring
artifact in their actual domain (a `dd_protection` change, a backtest/DSR claim, a regime-robustness
gate application) rather than forced against one that doesn't fit — not urgent, opportunistic.
