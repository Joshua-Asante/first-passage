# CC Handoff — [Short task name]

**Date:** YYYY-MM-DD
**Parent session:** claude.ai advisor (Joshua + Claude)
**Spawn target:** Claude Code (Analyst + Tactical Ops) | Cursor (frozen-spec implementation — see `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`; use the §0.5 Cursor variant)
**Repo:** `first-passage` (or specific repo path)
**Brief type:** CC handoff (single-step | multi-step)
**Parent question:** Q-X (if executing a Pre-Q) | ADR-NNN (if executing a locked decision) | `N/A`
**Authority:** Joshua (CEO). claude.ai authored this brief; CC executes. No commit/merge without Joshua's go.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any §2 work)

CC: read each file below and report contents in your first response. Do not propose changes, do not write code, do not run analysis scripts until this Phase 0 read-report has been delivered and Joshua has confirmed any ambiguities surfaced in §0.5.

Per SKILL.md: when production isn't directly accessible from the authoring environment, §0 lives in the CC handoff brief, not in the parent brief. This is that case.

- `path/to/file.py` — report: full file contents OR specific line range [a:b] for [reason]
- `path/to/config.yaml` — report: full contents
- `docs/adr/NNN-prior-decision.md` — report: §Decision section + §Consequences section
- `Notion: <page_title>` (page ID `<id>`) — report: read-only confirmation of current state of [specific table/field]
- `<git log -1 -- path/to/file.py>` — report: commit hash + date (anchor for §0 of any closure record this spawn produces)

After Phase 0: post the read-report. Wait for Joshua's go-ahead OR for §0.5 resolution before proceeding to §2.

---

## §0.75 — Local-only dependency check (required when Spawn target is Cursor)

**(Added 2026-07-16, per `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §2 Step 0 — RATIFIED 2026-07-16.)** Three cloud→local bounces in one 48h window (Class-S C1 scoring, Class-S C1 regime rider, H-OD-1 Stage-1/2 — all in `docs/SESSIONS.md` 2026-07-15/16) shared one root cause: the dispatch environment didn't have bytes or a credential the §0 reads assumed were there. Answer explicitly before dispatch:

- **Gitignored vendor data:** does any §0 read or §2 step touch a path under `core/data/tv_exports/**`, `core/data/bar_data/**`, or `core/data/external/**`? These are gitignored by standing policy (personal export OK, redistribution not) — a cloud checkout has them **only** if manually staged there for this session.
  - If yes: `Confirmed present — <how you verified it for THIS dispatch, e.g. "sha256-matched against SHA256SUMS in this checkout on <date>">` OR `NOT confirmed — route local.`
- **Secrets/API keys:** does any step need a credential (e.g. the databento key)?
  - If yes: `Confirmed present — <the check you ran in THIS environment, e.g. a command output>` OR `NOT confirmed — route local.`

A general belief that the bytes or key exist "somewhere" (a prior session, a different project) does not clear this gate — confirm for the dispatch you are about to make. If either line is `NOT confirmed`, do not dispatch to Cursor cloud: either run locally (CC or a local Cursor session) or stage the dependency into this specific cloud workspace first and re-confirm.

If Spawn target is CC (not Cursor), this section reads `N/A — CC runs in the operator's own environment, where these bytes/keys are already present.`

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY required)

CC: this section is your explicit license to halt and ask. Do NOT default to a guess if any of the following are ambiguous to you after Phase 0 reads.

Anchor: a CC session that ran the wrong analysis because the brief was ambiguous and the spawn defaulted instead of asking wastes the entire session. The cost of asking is one round-trip; the cost of guessing wrong is a full re-spawn (Discipline Check #7).

Surface ambiguities in these categories:
- **Scope:** does "[specific term in §1/§2]" mean [interpretation A] or [interpretation B]? If A and B would produce different artifacts, ASK.
- **Data:** which CSV / which date range / which strategy version is the source for [Phase X]? If multiple candidates exist on disk, ASK.
- **Methodology:** is [analysis choice] pre-registered or open? If §8 of the parent Pre-Q doesn't pin it, ASK rather than picking.
- **Termination:** does [phase] gate require both [condition A] and [condition B], or either? Default to AND only if §6 explicitly says AND.

Post ambiguities under `## §0.5 Response — ambiguities` in your first response. Set `Status: NEEDS_CONTEXT` until resolved (see §6).

**Cursor variant — parent-recommended defaults (use when Spawn target is Cursor, not CC).** Under the CC/Cursor surface-allocation rule (`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`), frozen-spec implementation routes to Cursor. For a Cursor handoff, do NOT leave §0.5 as bare open questions — for each ambiguity state a bolded **Recommended default:** that Cursor *applies* unless its Phase-0 read contradicts it, in which case it bounces `Status: NEEDS_CONTEXT` with the conflict quoted. Enumerate them `(A) … (B) … (C) …`. Reference implementation (retired; public seed excludes `docs/ltm/`) — retrieve via `git show pre-prune-2026-08-08:docs/ltm/briefs/rnd-pipeline/2026-07-13-cursor-handoff-prop-survivor-scoring-harness.md` §0.5. Rationale: Cursor executes frozen specs and never resolves a spec ambiguity unilaterally (ADR §2 test 2); a stated default keeps a spec-frozen build moving without a round-trip while preserving the halt-on-*conflict* guarantee. The pure halt-and-ask form above stays the default when the spawn target is CC.

---

## §1 — Context

[2–4 sentences. What is this task and why is it being run NOW?]

**Parent Pre-Q (if applicable):** Q-X — [one-sentence statement of what gates closure]
**Decision being executed (if ADR):** ADR-NNN — [one-sentence summary of the locked decision this implements]

**What CC is being asked to produce:**
- [Deliverable 1 — specific file path or report format]
- [Deliverable 2]
- [Closure artifact per §9 of parent Pre-Q if applicable]

**What CC is NOT being asked to do:** [Explicit scope-creep guard. The "while I was in there" refactor is forbidden — see §5.]

---

## §2 — Execution plan

Multi-step plans have Step 2.x sub-blocks. Single-step plans have one block. If §2 has >1 step, §7 requires final consolidated read across ALL diffs (Discipline Check #10).

### Step 2.1 — [Step name]

- **Inputs:** [files / params / prior step outputs]
- **Action:** [specific command or analysis]
- **Expected output:** [file / report / number]
- **Per-step gate:** [what passes this step; what surfaces as DONE_WITH_CONCERNS]

### Step 2.2 — [Step name]

- **Inputs:**
- **Action:**
- **Expected output:**
- **Per-step gate:**

### Step 2.N — Closure artifact

Produce the closure record per parent Pre-Q §9 format (or ADR amendment if executing a locked decision). Sentinel convention: no `recommendation.md` for non-PROMOTE verdicts.

---

## §4 — Falsifiable hypothesis (if executing a Pre-Q analysis)

Restate the parent Pre-Q §4 H-X verbatim here, with the §6 reject/accept/ambiguous-hold thresholds. CC must assert against these thresholds in Step 2.N, not against re-derived ones.

**H-X:** [verbatim from parent Pre-Q]
**Reject if:** [verbatim from parent §6]
**Accept if:** [verbatim from parent §6]
**Ambiguous-hold if:** [verbatim from parent §6]

If this handoff executes a locked decision (ADR) rather than a Pre-Q investigation, this section reads `N/A — executing ADR-NNN, no hypothesis under test`.

---

## §5 — Forbidden moves

Per SKILL.md Discipline Check #3: list moves the author genuinely considered or was tempted by, not theatrical refusals.

- **Scope creep — the "while I was in there" refactor.** If CC notices an unrelated issue, it logs the observation in §6 `DONE_WITH_CONCERNS` and surfaces it to Joshua. It does NOT silently fix it. (Anchor: Discipline Check #9 — spec-compliance is a separate audit pass from quality.)
- **Outcome-conditional D-tests.** Filtering data based on the outcome being studied is forbidden categorically. If §2 has an apparent need for one, return `NEEDS_CONTEXT` to the parent rather than proceed.
- **Amending §6 mid-execution.** If gate criteria appear wrong after data is seen, do NOT amend them silently. Return `BLOCKED — plan-itself-wrong` and escalate (Known Trap #12).
- **Re-deriving §0 facts.** If a §0 anchor seems inconsistent with what CC reads on disk, do NOT proceed with the inconsistent number. Return `NEEDS_CONTEXT` with the discrepancy surfaced.
- **[Task-specific forbidden move]** — [reason].

---

## §6 — Gate + status return taxonomy

CC reports back with EXACTLY one of these four statuses (Discipline Check #8). Two-state success/failure collapses distinct epistemic states.

| Status | Meaning | Parent action |
|---|---|---|
| `DONE` | All §2 steps passed; all per-step gates green; no scope creep; no off-pattern observations. | Accept, merge, close. |
| `DONE_WITH_CONCERNS` | Work completed but CC flags correctness, scope, or methodology doubts the parent should resolve before accepting. Every gate passed but CC noticed something off-pattern. | Parent reviews concerns; accept or re-dispatch with clarification. |
| `NEEDS_CONTEXT` | Cannot proceed without missing input that can be supplied. (§0.5 ambiguity unresolved, file referenced but not on disk, parameter underspecified.) | Parent supplies context; CC re-dispatches the same plan with added input. |
| `BLOCKED` | Cannot proceed; structural obstruction. Sub-case required (see below). | Parent escalates, decomposes, or re-spawns with stronger model. |

**`BLOCKED` sub-cases (mandatory):**
- `BLOCKED — context-problem`: re-dispatch with more context.
- `BLOCKED — capability-problem`: re-dispatch with stronger model or escalate to human.
- `BLOCKED — scope-problem`: decompose into smaller tasks.
- `BLOCKED — plan-itself-wrong`: escalate to parent session; the §2 plan is structurally broken.

**Closure report format:**
```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Per-step gates: 2.1 [pass/concern/skip], 2.2 [...], 2.N [...]
Diffs (files touched): <list>
Closure artifact path: <path>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (after CC returns)

Two passes, not one (Discipline Check #9). Do not collapse them.

**Pass 1 — Spec-compliance audit.** Did CC build EXACTLY what §1/§2 specified — nothing missing, nothing added?
- [ ] Every Step 2.x produced its expected output
- [ ] No "while I was in there" refactors slipped in
- [ ] No silent scope additions ("just to be safe" extra checks)
- [ ] Closure artifact matches §9 format of parent Pre-Q (if applicable)
- [ ] Diff list contains ONLY files §2 named; flag any unexpected paths

**Pass 2 — Quality audit.** Is what CC built methodologically and structurally sound?
- [ ] §6 verdict assertion matches §4 pre-registered thresholds
- [ ] Numbers in closure artifact reproduce when audit hooks re-run
- [ ] No outcome-conditional D-tests in the analysis path
- [ ] §0 anchors in closure artifact match Phase 0 read-report

**Pass 3 (only if §2 had >1 step) — Final consolidated read.** Read across ALL diffs together. Per-step gates catch local correctness; they do not catch integration issues — two correct steps producing an inconsistent combined state (Discipline Check #10).

Only after all three passes complete does claude.ai recommend Joshua accept/merge.

---

## §10 — Audit hooks (runnable)

```bash
# Re-run the closure assertion
python scripts/<analysis_script>.py --reproduce-<task-id>

# Verify §0 anchors still resolve
git log -1 -- path/to/file.py | grep <commit_hash>

# Cross-reference diffs against §2 scope
git diff <pre-spawn-commit>..<post-spawn-commit> --name-only
# Expected: matches §2 file list exactly

# Verdict-vs-pre-registration cross-check (if Pre-Q)
diff <(grep -A5 "thresholds" docs/briefs/pre-registration/Q-X-verdict-preregistration.md) \
     <(grep -A5 "thresholds" <closure-artifact-path>)
# Expected: identical
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
# Mechanical discipline check on this handoff brief
$ python scripts/check_brief.py <this-file>.md --type cc_handoff
# Expected: RESULT: well-formed  (applicable 1–6 + spawn extras this subset models)

# Confirm CC's closure report uses the four-state taxonomy
$ grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cc-return-path>

# Confirm spec-compliance pass and quality pass were both performed
$ grep -A2 "Pass 1 — Spec-compliance" <review-notes-path>
$ grep -A2 "Pass 2 — Quality" <review-notes-path>
```

If CC returned `NEEDS_CONTEXT` or `BLOCKED`, this handoff is not complete; re-dispatch per §6 disposition guide.
