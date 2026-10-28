# Coordinator role skill and its rules (design, 2026-10-28)

**Status:** approved design (Joshua, in session, 2026-10-28: "approved, go for it").

**Delivery:** PR 1 carries the rules and rulings; PR 2 carries the skill. Joshua ratifies PR 1 by merging it.

**Goal:** keep work spread across several researcher and engineer agents (Claude and Codex) on track. One repo skill, `coordinator`, holds the repeated practices that the native Aegis rebuild of 2026-10-26 to 10-28 failed to carry out. The project-manager duties are folded into it.

## 1. Why

The native Aegis rebuild produced the evidence for this design:

- the execution-actor spec took 12 Codex rounds;
- the two worker cards took 24 dispatch attempts and 29 freeze records between them.

The causes, in order of cost:

1. **Review loops had no stop tied to value.** Finding counts fell (12, 9, 7, 4, 3, 3, 3, 2), so no count-based rule fired. Yet the same failure family kept returning: timestamp correlation of change confirmations came back in four rounds. Rule 7 should have stopped the loop at the second failed correction. Because each finding read as a new variant, it was never counted as the same issue.
2. **Design ran ahead of cheap evidence.** Most actor-spec rounds defended against host behaviour nobody had observed: callback order, the stamping clock, overfill handling, unknown order states. One order-free logging session on the host would have answered those questions.
3. **The operator was the bottleneck for mechanical decisions.** One-token fixes, version labels and self-references each needed a ruling round trip, and some rulings arrived cut at the app's 300-character button limit.
4. **Pins were copied by hand.** A stale contract constraint survived two re-pins.
5. **Procedural failures cost as much as design failures.** Dispatch attempts stopped on the sandbox, the read allowlist and writes to pinned files.
6. **Checks were narrower than their consumer.** A field-level validation passed while the comparator rejected the whole profile, and a check's exemption was bound to a line rather than to the exact token.

The 2026-10-25 roles research (`docs/notes/2026-10-25-repeated-agent-roles.md`) recommended folding the executive seat into the operator and the coordinator. This design follows that recommendation for the project-manager duties.

## 2. Rulings (Joshua, verbatim, in the escalation-lane session, 2026-10-28)

| # | Question | Answer |
|---|---|---|
| 1 | Seats | "Fold into coordinator". Confirmed unprompted: "after considering it, having the project manager role folded into the coordinator makes the most sense, less coordination work" |
| 2 | Delegation | "Consistency-only (Recommended)": pins, hashes, version labels, self-references, stale tokens, harness or tooling fixes that change no behaviour, plus one delta review per fix. Joshua keeps behaviour, scope, spend, risk, governance text and every dispatch GO |
| 3 | Review stops | The coordinator decides between shipping with logged residuals and one more bounded round. Cutting scope, accepting a new assumption or weakening a guarantee, spending money, or changing an evidence claim goes to Joshua as one decision. (He answered this while the PM seat still existed; ruling 1 moved the decision to the coordinator.) |
| 4 | Residuals on the coordinator's own artifacts | "Reviewer classifies (Recommended)": the cross-agent reviewer marks each finding blocking or non-blocking. The coordinator ships only with findings the reviewer marked non-blocking, logged in the artifact. Waiving a blocking finding goes to Joshua |
| 5 | Evidence gate | "No reviews until settled (Recommended)": drafting may continue, but no review round starts until each such fact is observed by a cheap probe or accepted by Joshua as a named assumption |
| 6 | Rule 7 | "Yes, the family": "one issue" means one failure family, the same mechanism |
| 7 | Rule 3 | "Amend Rule 3 (Recommended)": add the classes above, with no silent default |
| 8 | Rule 2 | "go with your recommendation for the review rounds": each review round is one iteration, budgeted before round 1 |
| 9 | Scope | Practices 1–6 of §1, including "add 4-6 too" |

## 3. PR 1: rules, rulings, lesson

### 3.1 `docs/operational_rules.md`

Amend existing rules, because the Rule 0–41 list is fixed. Log each change in §Edit log. Mirror each change in AGENTS.md §Core rules, whose index lines are mirrors of these statements.

- **Rule 0**, append: "When a guarantee or an acceptance test depends on an unobserved fact about an external system (a platform, host, vendor or data feed), no review round starts until a cheap probe observes the fact or the operator accepts it as a named assumption, recorded verbatim in the owning record; drafting may continue."
- **Rule 2**, append: "A review round of a spec, card or PR is one iteration of the review loop; declare the round budget with the work's other bounds before round 1."
- **Rule 3**, append: "Also the operator's, each brought as one decision with no silent default: cutting a deliverable's scope, accepting a new assumption or weakening a guarantee, changing an evidence claim, and any change to account permissions."
- **Rule 7**, restated:

  > After two failed corrections of one issue — one failure family (the same mechanism, counted across instances even while the finding count falls); this count overrides any per-skill bound — stop, summarize and restart cleaner in a fresh coordinator session (the escalation lane). At any review stop (this rule, a spent round budget, a count that fails to fall for two rounds, or a fix round that grows the artifact) the coordinator may ship a spec, card or private artifact only with findings the cross-agent reviewer marked non-blocking, logged in the artifact, and never with an omitted required check or on an irreversible change at a spent budget; or it may run one more round when the budget was the only stop and the round stays within Rule 6 and this rule; anything else goes to the operator under Rule 3. A PR whose cross-agent reviews found issues three times returns to its owner for a rewrite unless a fourth review is clean.

  The owner line adds the new addendum. "Codex reviews" becomes "cross-agent reviews", matching Rules 5 and 6. The class limits keep their own owners under this override: M-37 (documents), M-38 (contract code), M-39 (state-model specs) and Rule 6 (PRs).
- Each amended rule's owner line adds the new addendum.

### 3.2 Addendum to the surface-allocation ADR: "Addendum 2026-10-28 — operator rulings: executive folded into the coordinator; consistency-only delegation"

- **Rulings:** the §2 table, verbatim.
- **Seat table effect:**
  - The executive seat is folded. Goal-setting, value checks and review-stop decisions move to the coordinator. Acceptance moves to the operator, and goal review to the cross-agent reviewer.
  - The executive row stays in the table as history, marked folded. Its `scripts/seat_authority.yml` entry stays too, with a comment, because historical cards and tests name it.
  - The escalation lane is the coordinator's fresh-session rebuild; it already was not a seat.
  - Merges stay with the merge-train seat under Addendum 2026-10-24b A.
  - Who holds the coordinator role is assigned by the operator, per session.
- **Consistency-only delegation:**
  - **Scope:** an act changes only pins, hashes, version labels, self-references or stale tokens, or fixes harness or tooling without changing behaviour.
  - **Object binding:** each act cites the exact file hash or head SHA it changes.
  - **Review:** each fix gets one cross-agent delta review.
  - **Exclusions:** frozen evidence bodies, any agreed rule, any ruling text, and any change to what is claimed.
  - **Not a ratification:** a consistency-only edit changes no ruling text, so merging it is not a ratification.
  - **merge-train exception:** merge-train hard rule 4 does not require the operator's direct confirmation for a PR whose body declares "consistency-only (surface-allocation ADR Addendum 2026-10-28)" and whose reviewer confirms that its diff changes no ruling or rule text.
- **Reviewer duty:** in a coordinator-run review loop, the cross-agent reviewer marks each finding blocking or non-blocking. Only the reviewer's mark makes a finding a shippable residual.
- **Procedure owner:** `.claude/skills/coordinator/SKILL.md` holds the procedure; this addendum and Rules 0, 2, 3 and 7 hold the authority.

### 3.3 Lesson M-50

- `docs/methodology/lessons/methodology_lessons.md`, in the light format, titled "Review loops stop on a recurring failure family; host facts are observed before review; the operator decides only what changes exposure".
- Anchors: the §1 counts. Rule: §3.1. Links: M-37, M-38, M-39, M-43, M-49.
- A matching row in `docs/methodology/LESSONS_INDEX.jsonl`.

## 4. PR 2: the `coordinator` skill

**`.claude/skills/coordinator/SKILL.md`.** Frontmatter is `name` and `description`. The skill points to its owners and restates no rule or number, citing each owner by a repo-rooted path in inline code so `check_skill_refs` checks it. Sections:

1. **Holding the role.** The operator assigns it per session; never assume it. Seat grants are in `scripts/seat_authority.yml`.
2. **Starting work (project-manager duties):**
   - name the decision the work changes and why it is worth doing now (Rule 9);
   - declare the Rule 2 budget, including review rounds;
   - list every load-bearing external fact, and get a probe or a named assumption for each before any review (Rule 0).
3. **The board.** `work-decomposition`'s parent manifest is the only board for multi-agent work; `merge-train`'s table covers PRs. The coordinator is the single writer: one row per agent (owner, card, frozen SHA, status), reconciled every turn. No new store.
4. **Cards and dispatch:**
   - author with `brief-authoring` and gate with `handoff-verify`;
   - the freeze record is the single pin source: generate card pin tables from it and check card against record before every review;
   - rehearse the real dispatch harness (launcher, sandbox roots, read allowlist, writes near pinned files) with a throwaway card before freezing;
   - acceptance calls the real consumer's entry point, and every exemption is bound to an exact span with a negative test;
   - assign the cross-agent reviewer (Rule 5).
5. **Review loops:**
   - the round budget is declared up front;
   - the blocking bar is the reviewer's mark;
   - Rule 7's family stop applies;
   - stop decisions follow Rule 7, and the decisions Rule 3 names go to the operator.
6. **Delegation.** Act only within Addendum 2026-10-28. Cite the object, declare it in the PR body, and get one delta review.
7. **Bringing decisions to the operator:**
   - the Rule 3 classes, one decision at a time;
   - recommendation first;
   - reply buttons under 300 characters;
   - record the ruling verbatim in its owner before anything cites it.
8. **Returns:**
   - the four statuses (Rule 4);
   - `NEEDS_CONTEXT` gets one re-anchor, then a re-cut (`work-decomposition`);
   - the coordinator's adjudication is input; the operator accepts on the evidence pack.

**Codex adapter.** `.agents/skills/coordinator/SKILL.md` is a thin pointer to the canonical skill, plus the `.gitignore` pair `!.agents/skills/coordinator/` and `!.agents/skills/coordinator/**`.

**Mechanical fixes in other owners**, each resolving a conflict the overlap map found by pointing to the stricter existing owner:

- `merge-train/SKILL.md` line 13: the stale "the reviewer is Codex" points to Rules 5 and 6.
- `babysit/SKILL.md`:
  - add a review-limit exit pointing to Rules 6 and 7;
  - "implement every actionable request" becomes triage per M-43;
  - the reviewer becomes the cross-agent reviewer.
- `brief-authoring`:
  - the stale "no Codex launcher" note points to `scripts/dispatch_codex.ps1`;
  - the undeclared `CHECKPOINT` status is resolved against the four statuses;
  - unlimited re-dispatch points to `work-decomposition`'s one re-anchor.
- `fable-method`: its references' three-cycle limit points to Rule 7.

## 5. Verification

- **Gates:**
  - `scripts/gate_manifest.py --tier check`, the `skills (3.12)` job;
  - `scripts/check_skill_refs.py --all` with zero warnings;
  - `adr-graph` and `governance-prose-control-chars`;
  - the live skill tests (`tests/test_check_skill_refs.py`), run by hand, because skills-only PRs skip them.
- **Behaviour, before PR 2 opens:** six scenarios replayed from §1. The baseline runs on fresh Claude agents against origin/main, before any PR 1 edit, to show the gap. The with-skill runs use fresh Claude agents and fresh Codex agents (through the adapter) on PR 2's tree. The scenarios:
  1. a third round brings back the clock family after two fixes;
  2. a spec rests on an unobserved callback order;
  3. a stale token is found after approval;
  4. a fix needs a scope cut;
  5. a card is about to freeze with no harness rehearsal;
  6. a field check passes while the consumer rejects the profile.

  A pass means each scenario's decision matches the expected one with the skill. The runs, prompts and outcomes go in PR 2's body.
- **Review:** a cross-agent Codex review on each PR, with the round budget declared in the PR body.

## 6. Out of scope (follow-ups)

- The `pr.review` grant for reviewer cards (worker grants lack it).
- `governance.author` is granted to more seats than the ADR's action-class table says.
- `check_skill_refs` leaves relative links, anchors and frontmatter unchecked.
- The SESSIONS keep-30 roll.
- Memory updates (routing lines, retired role handoffs), after PR 2 merges.
