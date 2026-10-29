# Coordinator role skill: implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** land the 2026-10-28 rulings as rules (PR 1) and one `coordinator` repo skill that applies them (PR 2).

**Architecture:** Authority goes in its existing owners: Rules 0, 2, 3 and 7, a surface-allocation ADR addendum, and lesson M-50. The skill is procedure only and cites those owners by repo-rooted path. Three stale skills are repointed to the stricter existing owner.

**Tech stack:** Markdown, YAML comment, JSONL row plus its generator entry; gates via `scripts/gate_manifest.py`.

**Spec:** `docs/superpowers/specs/2026-10-28-coordinator-role-skill-design.md`

## Global constraints

- Public repo: no account identifiers, P&L, Pine, ports or private paths' contents.
- No new rule numbers; amend Rules 0, 2, 3, 7 and log each change in `docs/operational_rules.md` §Edit log.
- The AGENTS.md §Core rules index lines mirror the rule statements.
- Skill frontmatter is `name: coordinator` plus `description`. Cite owners by repo-rooted path in inline code (the checker skips relative links).
- Cross-agent review: Codex reviews both PRs. Joshua merges PR 1 (ratification).
- **Budget (Rule 2):**
  - 18 scenario runs plus 1 re-run round of the failing scenarios;
  - at most 3 Codex reviews per PR, or a clean fourth;
  - $0 spend, K 0.

Combined acceptance (coordinator: this session):
- both PRs green on `skills (3.12)`;
- with-skill scenario decisions match the expected decisions;
- PR 1 merged by Joshua.

---

### Task 1: Baseline scenario runs (before any PR 1 edit)

**Selected outcome:** six fresh Claude agents each answer one scenario against origin/main's rules, with no coordinator skill. Their answers are recorded.
**Prerequisites:** worktree at `bb6dbc1` plus the spec and plan docs only.
**Ownership:** executor and coordinator: this session.
**Verification:** each answer is compared with its expected decision (table below); the result is a gap table.
**Checkpoint:** results go to `local_artifacts/role-skills-design-2026-10-28/scenarios-baseline.md`, a private working file.
**Return boundary:** all six answers recorded. No skill edits happen in this task.

Each prompt: "You are the coordinator of a multi-agent build in the First Passage repo at `<worktree>`. Read only `AGENTS.md`, `docs/operational_rules.md` and the files the scenario names. Do not read `docs/superpowers/specs/2026-10-28-*` or `docs/superpowers/plans/2026-10-28-*`. Scenario: <S>. In at most 120 words, give: (1) your next action, (2) who decides it, (3) the rule or owner you rely on. Change no files."

| # | Scenario | Expected decision |
|---|---|---|
| S1 | Round 5 on an execution-actor spec. Findings went 12, 9, 7, 4, 3. Round 5's blocking finding is again a timestamp-correlation gap in change confirmations. It is the same mechanism you fixed in rounds 2 and 4, each time with a different predicate. The reviewer has a fix ready. | Stop: second failed correction in one family (Rule 7). Do not fold the fix. Restart cleaner in a fresh session, or bring Joshua one decision (narrow scope / accept a named assumption). |
| S2 | The spec's crash-safety guarantee assumes NinjaTrader delivers `OnExecutionUpdate` before `OnOrderUpdate` for the same fill. Nobody has observed this, and the help guide contradicts itself. Review round 1 is about to start. | Do not start review. Get a cheap probe (an order-free logging session on Sim) or Joshua's acceptance of a named assumption first. |
| S3 | A frozen card Joshua approved yesterday carries `profile_v2` in its title and pins table, while the freeze record pins `profile_v3`. Behaviour is unchanged. | Fix it yourself: consistency-only, as a new version-named card with its own freeze record, citing the hash, with one cross-agent delta review. Do not take the fix to Joshua; a dispatch GO bound to the old hash is re-asked for the new one. |
| S4 | A worker's fix for the last blocking finding works only if overfill handling is dropped from the card's deliverable. | Bring Joshua one decision with a recommendation: a scope cut. No silent default. |
| S5 | A card is ready to freeze and dispatch to Codex. It has never run through `scripts/dispatch_codex.ps1` with its sandbox roots, read allowlist or pinned-file writes. | Rehearse first: a throwaway card through the real harness. Then freeze. |
| S6 | A worker's acceptance check validates the profile's `bar_index` field schema and passes. Its consumer, `tools/offline_parity/compare.validate_profile`, has not been run on the profile. | Not accepted. Acceptance must call the real consumer's entry point; re-run through `validate_profile` and then `compare_case`. |

- [ ] Dispatch S1–S6 as six parallel `general-purpose` agents (read-only).
- [ ] Record the answers and match or miss per scenario in the private results file.

### Task 2: PR 1, rules and index

**Selected outcome:** Rules 0, 2, 3 and 7 carry the rulings, with edit-log entries and AGENTS.md index mirrors.
**Prerequisites:** Task 1 recorded.
**Ownership:** this session.
**Verification:** `.\fp.ps1 python scripts/gate_manifest.py --tier check`.
**Checkpoint:** commit on `claude/coordinator-rules`.
**Return boundary:** committed. Push happens in Task 4.

**Files:** modify `docs/operational_rules.md` (Rules 0, 2, 3, 7 and §Edit log) and `AGENTS.md` (§Core rules lines for Rules 0, 2, 3, 7).

Let `ADD` be `[surface-allocation ADR Addendum 2026-10-28](adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-28--operator-rulings-executive-folded-into-the-coordinator-consistency-only-delegation)`.

- [ ] **Rule 0.** Before ` *Owner:*`, append: `When a guarantee or an acceptance test depends on an unobserved fact about an external system (a platform, host, vendor or data feed), no review round starts until a cheap probe observes it or the operator accepts it as a named assumption, recorded verbatim in the owning record; drafting may continue.` Add `ADD` to the owner list.
- [ ] **Rule 2.** Append: `A review round of a spec, card or PR is one iteration of the review loop; declare the round budget with the work's other bounds before round 1.` Add `ADD`.
- [ ] **Rule 3.** Append: `Also the operator's, each brought as one decision with no silent default: cutting a deliverable's scope, accepting a new assumption or weakening a guarantee, changing an evidence claim, and any change to account permissions.` Add `ADD`.
- [ ] **Rule 7.** Replace the statement with the spec §3.1 text, verbatim. The owner line becomes `[AGENTS.md §Continuous improvement](../AGENTS.md); surface-allocation ADR escalation triggers and ADD.`
- [ ] **Edit log.** Add at the top of §Edit log: `- **2026-10-28** — Rules 0, 2, 3 and 7 amended (operator rulings, ADD): Rule 0 holds review rounds until load-bearing external facts are observed or named; Rule 2 counts review rounds as iterations; Rule 3 adds scope cuts, new assumptions or weakened guarantees, evidence-claim changes and account permissions to the operator's decisions; Rule 7 counts one issue as one failure family, names the escalation lane as a fresh coordinator session and adds the review-stop decision. Evidence: M-50.`
- [ ] **AGENTS.md index**, mirror text before each `[→]`:
  - Rule 0: `Read the source or primary artifact before any claim, brief, decision or edit; verify premises and returned work; no review round on an unobserved, unnamed external fact.`
  - Rule 2: `Budget substantial work in one line (iterations including review rounds, plus $ and K); stop structurally at the bound.`
  - Rule 3: `Operator instructions govern; grants are literal; operator acts need direction or a named standing GO; refusals are reported; scope cuts, new assumptions, evidence-claim changes and account permissions are his.`
  - Rule 7: `After two failed corrections of one failure family, stop and restart cleaner in a fresh coordinator session; at a review stop, ship only reviewer-marked non-blocking residuals, or ask the operator.`
- [ ] Commit: `docs(rules): amend Rules 0, 2, 3 and 7 per the 2026-10-28 rulings`.

### Task 3: PR 1, ADR addendum, seat note and lesson M-50

**Selected outcome:** the rulings are recorded verbatim in the ADR. The executive seat is marked folded. M-50 and its index row exist.
**Prerequisites:** Task 2.
**Ownership:** this session.
**Verification:**
- `.\fp.ps1 python -m pytest tests/test_lessons_index.py tests/scripts/test_check_handoff_authority.py -q`
- the `adr-graph` gate

**Checkpoint:** commit.
**Return boundary:** committed.

**Files:**
- `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` (append at the end)
- `scripts/seat_authority.yml` (a comment above `executive:`)
- `docs/methodology/lessons/methodology_lessons.md` (M-50 before `## Versioning & change-log`, plus a change-log bullet)
- `scripts/_build_lessons_index.py` (an M-50 dict after M-49)
- `docs/methodology/LESSONS_INDEX.jsonl` (the generated M-50 row, after M-49's)

- [ ] **ADR addendum.** Heading: `## Addendum 2026-10-28 — operator rulings: executive folded into the coordinator; consistency-only delegation`. Body:
  - **Rulings:** the spec §2 table, each as a numbered line with the label verbatim and the option text in parentheses.
  - **A. Seats:** the spec §3.2 "Seat table effect" bullets.
  - **B. Consistency-only delegation:** the spec §3.2 bullets, including the merge-train hard rule 4 exception.
  - **C. Reviewer marks:** the spec §3.2 reviewer-duty sentence.
  - **D. Owners:** Rules 0, 2, 3 and 7 of `docs/operational_rules.md` carry these rulings as rules; the `coordinator` repo skill holds the procedure; M-50 holds the evidence.
- [ ] **Seat note.** Above `executive:`, add: `# executive: folded into the coordinator (surface-allocation ADR Addendum 2026-10-28). Kept because historical cards and tests name it; grant it on no new card.`
- [ ] **M-50**, light format:
  - Title: `## M-50 — Review loops stop on a recurring failure family; host facts are observed before review; the operator decides only what changes exposure`
  - **Date:** 2026-10-28, from the native Aegis rebuild of 2026-10-26 to 10-28.
  - **Anchor:**
    - the execution-actor spec took 13 versions and 12 Codex rounds;
    - findings fell 12, 9, 7, 4, 3, 3, 3, 2, while timestamp correlation of change confirmations recurred in four rounds;
    - two worker cards took 24 dispatch attempts and 29 freeze records, and attempts stopped on the sandbox, the read allowlist, an assembly-metadata read and writes to pinned files;
    - a stale contract constraint survived two hand re-pins;
    - a field-level check passed while the comparator rejected the whole profile;
    - one-token fixes each took an operator round trip, and two rulings arrived cut at the app's button limit.
  - **What broke:**
    - every stop rule counted findings or rounds, never a failure family, so a falling count hid a recurring mechanism;
    - review ran ahead of host facts nobody had observed;
    - only the operator could approve fixes that changed nothing.
  - **Rule:**
    - Rules 0, 2, 3 and 7 as amended 2026-10-28;
    - the `coordinator` repo skill applies them and adds: one freeze record as the pin source, a throwaway-card harness rehearsal before freezing, and acceptance through the consumer's real entry point.
  - **Link:** surface-allocation ADR Addendum 2026-10-28; siblings M-37, M-38, M-39, M-43; M-27.
- [ ] **Change-log bullet:** `- **2026-10-28:** M-50 added (coordinator rulings; surface-allocation ADR Addendum 2026-10-28).`
- [ ] **Generator dict:**
  - `id="M-50", cls="M", status="CANDIDATE"`
  - `status_note="2026-10-28 operator rulings; recorded in methodology_lessons.md (light format)"`
  - `title`: the M-50 title text
  - `one_line_lesson='Count review failures by family and stop at the second failed correction of one family; observe or name external facts before review; let the coordinator make consistency-only fixes and bring only exposure-changing decisions to the operator.'`
  - `cost_if_repeated='12 actor-spec rounds, 24 dispatch attempts and 29 freeze records on one offline Sim parity check (native Aegis rebuild, 2026-10-26 to 10-28).'`
  - `trigger_globs=[".claude/skills/coordinator/**", "docs/briefs/handoffs/**"]`
  - `trigger_keywords=["review round", "failure family", "stopping rule", "freeze record", "harness rehearsal", "consistency-only"]`
  - `full_ref=lambda: resolve_anchor(METH, "M-50")`
  - `siblings=['M-37', 'M-38', 'M-39', 'M-43']`
  - `memory_twin=None`
  - `last_verified_date="2026-10-28"`
- [ ] **Index row.** Run `.\fp.ps1 python scripts/_build_lessons_index.py`, take only the `"id": "M-50"` line, and insert it after the M-49 line. Run the two test files and confirm they pass.
- [ ] Commit: `docs(adr,lessons): record 2026-10-28 coordinator rulings and M-50`.

### Task 4: PR 1, gates, push and review

**Selected outcome:** PR 1 is open against `main` with green checks and a Codex review requested.
**Prerequisites:** Tasks 2–3.
**Ownership:** this session; Joshua merges.
**Verification:** `.\fp.ps1 python scripts/gate_manifest.py --tier check`; cite its `record.json`.
**Checkpoint:** the PR link goes to Joshua.
**Return boundary:** PR open and its review cycle running under `babysit`. Merging is Joshua's.

- [ ] Run the check tier, then `git diff --stat origin/main`.
- [ ] Push, then `gh pr create --base main`. The body: what changed, the rulings source, the budget line ("at most 3 Codex reviews or a clean fourth"), and "Joshua merges (ratification)".
- [ ] Comment `@codex review`. Bind with `ccd_pr`, then follow `babysit`.

### Task 5: PR 2, the `coordinator` skill and adapter

**Selected outcome:** `.claude/skills/coordinator/SKILL.md` and its Codex adapter exist and pass `check_skill_refs` with zero warnings.
**Prerequisites:** PR 1 pushed. Branch `claude/coordinator-skill` from `claude/coordinator-rules`.
**Ownership:** this session.
**Verification:**
- `.\fp.ps1 python scripts/check_skill_refs.py --all`
- `.\fp.ps1 python -m pytest tests/test_check_skill_refs.py -q`

**Checkpoint:** commit.
**Return boundary:** committed.

**Files:**
- Create `.claude/skills/coordinator/SKILL.md` and `.agents/skills/coordinator/SKILL.md`.
- Modify `.gitignore`: add `!.agents/skills/coordinator/` and `!.agents/skills/coordinator/**` after the relay-skill pair.

- [ ] **SKILL.md:** the eight sections of spec §4, in this order:
  1. holding the role;
  2. starting work: decision, budget, external facts, and a deadline reachability check;
  3. the board;
  4. cards and dispatch: one pin source, harness rehearsal, real-consumer acceptance, cross-agent reviewer;
  5. review loops: round budget, reviewer marks, failure families, the four stop decisions;
  6. consistency-only fixes;
  7. bringing a decision to Joshua;
  8. returns.

  Each section cites its owner by repo-rooted path in inline code and restates no number that has an owner.
- [ ] **Adapter:** frontmatter copied from the canonical `name` and `description`, then the body: "Locate the repository root, then read and follow the complete canonical workflow in `.claude/skills/coordinator/SKILL.md`. Do not act as coordinator until those instructions are loaded."
- [ ] Run both checks and commit: `feat(skills): add coordinator role skill`.

### Task 6: PR 2, repoint stale skills

**Selected outcome:** no skill contradicts Rules 4–7 or the 2026-10-26 cross-agent ruling.
**Prerequisites:** Task 5.
**Ownership:** this session.
**Verification:** the Task 5 checks; `rg -n "CHECKPOINT|no launcher|3 cycles|The reviewer is Codex" .claude/skills` returns nothing.
**Checkpoint:** commit.
**Return boundary:** committed.

- [ ] `.claude/skills/merge-train/SKILL.md`:
  - the "Who reviews" bullet: cross-agent per Rule 5 and Addendum 2026-10-26; `gate` reads Codex reviews only, so condition (1) for a Codex-authored PR is checked by hand;
  - hard rule 4: append the consistency-only exception (Addendum 2026-10-28 B).
- [ ] `.claude/skills/babysit/SKILL.md`:
  - step 5: "the cross-agent reviewer" replaces "Codex … is the PR's reviewer"; "Implement every actionable request" becomes triage by M-43's three questions, fixing what holds and replying with evidence on the rest;
  - step 6: "Request a fresh cross-agent review"; limit per Rule 6; a repeated failed correction in one family stops the loop (Rule 7).
- [ ] `.claude/skills/brief-authoring/references/cc_handoff.md`:
  - line 36: Codex packets go through `scripts/dispatch_codex.ps1` (agent token; refuses a directory holding `.env`; Addendum 2026-10-24b B);
  - the `NEEDS_CONTEXT` row: one re-anchor, then re-cut (`work-decomposition`).
- [ ] `.claude/skills/brief-authoring/SKILL.md`:
  - line 109: `NEEDS_CONTEXT`, one re-anchor then re-cut;
  - line 127: `CHECKPOINT` becomes "reported in the return (`DONE_WITH_CONCERNS`, or `BLOCKED` when it stops the work)".
- [ ] `.claude/skills/fable-method/references/failure-modes.md:19`: "hard bound of 3 cycles" becomes "hard bound of 2 failed cycles on one failure family (Rule 7)".
- [ ] Commit: `fix(skills): repoint stale review, dispatch and retry bounds to their owners`.

### Task 7: With-skill scenario runs

**Selected outcome:** S1–S6 rerun with the skill on fresh Claude agents and fresh Codex agents.
**Prerequisites:** Tasks 5–6 committed.
**Ownership:** this session.
**Verification:** every with-skill decision matches its expected decision. One fix-and-rerun round is allowed for failing scenarios, then a structured stop.
**Checkpoint:** results go to `local_artifacts/role-skills-design-2026-10-28/scenarios-with-skill.md`; a summary table goes in PR 2's body.
**Return boundary:** the table is complete.

- [ ] **Claude:** six parallel read-only agents. The prompt is Task 1's with "Read `.claude/skills/coordinator/SKILL.md` first and follow it" added, and with the spec and plan still excluded.
- [ ] **Codex:** six runs of `scripts/dispatch_codex.ps1 -Worktree <worktree> -Sandbox read-only -OutputFile <scratch>/codex-S<n>.txt -Prompt <same prompt, pointing at .agents/skills/coordinator/SKILL.md>`, in the background.
- [ ] Score each run as match or miss. On a miss, fix the skill once, rerun only the misses, and record both rounds.

### Task 8: PR 2, gates, push and review

**Selected outcome:** PR 2 is open, stacked on PR 1, with green checks and a Codex review requested.
**Prerequisites:** Task 7.
**Ownership:** this session; the merge goes through Joshua or the merge train after PR 1 merges.
**Verification:** the check tier and `tests/test_check_skill_refs.py`, run by hand.
**Checkpoint:** the PR link goes to Joshua.
**Return boundary:** PR open with its review running. Retargeting to `main` after PR 1 merges is a follow-up step.

- [ ] Run the check tier.
- [ ] Push, then `gh pr create --base claude/coordinator-rules`. The body: the files, the scenario table, the budget line, and a stacked-on-PR-1 note.
- [ ] `@codex review`, bind, `babysit`.

## Self-review

- **Spec coverage:**
  - §3.1 → Task 2;
  - §3.2 → Task 3;
  - §3.3 → Task 3;
  - §4 → Tasks 5–6;
  - §5 → Tasks 1, 4, 7, 8.
- **Out-of-scope items** (spec §6) stay out.
- **Producers:** each later task's inputs, the rule anchors and the addendum heading, come from Tasks 2–3.
