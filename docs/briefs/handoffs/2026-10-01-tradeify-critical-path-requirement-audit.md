# Tradeify critical-path requirement audit — bounded handoff (rescoped §7.4)

**Status:** DRAFT 2026-10-01, for the operator's decision. Not dispatched. Drafted at the operator's request ("draft the rescoped audit card") after the critical-path review of [#570](https://github.com/Joshua-Asante/first-passage/pull/570) ([review comment](https://github.com/Joshua-Asante/first-passage/pull/570#issuecomment-5933674378)). It rescopes that packet's §7.4 requirement audit so it starts with the two external blockers on the path to a first full-portfolio session, and takes up the packet's D-MON, D-GO, D-REC and D-HIST comparisons last.

**What this is.** One documentary audit with one return. It reads owner records and source and returns findings and decisions owed. It changes no owner text, gate, statistical criterion, authority or checkpoint, and dispatches no other work.

## §0 — Production reads

Read these first, on `origin/main` at the dispatch revision, and report the dispatch revision and each file's last-modified commit before any analysis:

- [STATE.md](../../../STATE.md) queue item 1 and the decision index (newest 15).
- [Deployment checklist](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md): the dependency summary, the 2026-09-27 staged-acceptance addendum (§0 gates, §3 workstreams, §4 checkpoints CP-1a..CP-9), and the 2026-09-28 and 2026-10-01 continuation addenda.
- [T00 step-1 return and rulings](2026-09-22-tradeify-t00-step1-producer-inventory.md) (§7.8 condition 4) and the [T00 P7 closure](2026-09-24-tradeify-t00-p7-closure.md).
- The [T00 → T10 → CP-7 note](../../notes/2026-09-29-t00-t10-cp7-sequence.md) (the 2026-09-29 D-feed correction), if present at the dispatch revision. Otherwise, the corrected 2026-09-24 decision-index entry in STATE.
- [T10 packet](2026-09-21-tradeify-t10-source-and-freeze-packet.md) and the [provider-neutral feed preparation note](../../notes/2026-09-27-feed-provider-neutral-preparation.md).
- [T08 packet](2026-09-21-tradeify-t08-broker-protection-feasibility.md) §7.6–§7.10, including the 2026-10-01 route-path ruling (§7.10, Reading 1: halt and attended reconciliation; an unknown request closes only on a uniquely correlated outcome).
- The [bounded-exposure amendment scope](../../superpowers/specs/2026-09-24-bounded-exposure-unknown-request-amendment-scope.md) and the incident ADR's §A8 addendum ([incident ADR](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md)).
- [CrossTrade REST route assessment](2026-09-25-crosstrade-rest-route-assessment.md).
- [Execution-slices ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md): the S5 entries from 2026-09-27 on, and the T12/n3 requirements.
- [Protected campaign specification](../../superpowers/specs/2026-09-17-protected-full-e1-campaign.md): the E1 and final-n3 decision rules.
- The [four-firm program ADR](../../adr/2026-07-12-prop-portfolio-four-friendly-firms.md) §4 falsifier (due 2026-11-08) and the [S4 discharge withdrawal](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md).
- The #570 simplification packet (`docs/notes/2026-09-30-tradeify-simplification-decision-packet.md`, at its merged revision if merged, otherwise PR head `9ff9318`), §2–§5 and §7–§8.

If a cited path is absent at the dispatch revision, report it and use the owner that superseded it. Do not reconstruct it from this card.

## §0.5 — Clarifications and recommended defaults

- **The scope is the first full-portfolio attended session.** That means all four strategies with their full behavior (operator constraint in #570 §7). An item that matters only to later sessions is classified "defer" or "later-event", not removed.
- **Recommended default for an unknown cost:** report it as unknown, with what would measure it. Never estimate hours or claim a saving without the comparison in §2 step 4.
- **The route path is ruled** (T08 §7.10). The audit schedules accepting the amendment. It does not reopen options A–D.
- **E1 and the final n3 stay required** throughout. Step 3 assesses decision value only. Any removal needs a separate operator admission decision under existing change control.

## §0.75 — Local dependency check

`Routing: cloud-capable.` Every input is a committed document or source file. No private Pine, vendor capture, account artifact or `local_artifacts/` read is needed. If a step seems to need one, stop and return `NEEDS_CONTEXT` rather than reading around it.

## §1 — Context and observed defect

The 2026-10-01 critical-path inventory (in session, relayed in the #570 review) found that the qualification engineering spine (S5 → S6/S7 → S8 → T11 → T12) is moving, but T15 cannot start while two inputs are blocked from outside the engineering work:

1. **Feed.** D-feed requires a T00 verdict that is actual GO-evidence (the 2026-09-29 correction). T00 is INSUFFICIENT on P7(b), so CP-7 funding, T14 and T15 cannot proceed. No owner record says what evidence would change T00's verdict, who produces it, or whether the gate itself should change.
2. **Route.** T08 R3 = NONE, and the 2026-09-25 CrossTrade reply rules out a time-based fence. The operator ruled the amendment path on 2026-10-01 (T08 §7.10). Steps 3–5 of the amendment scope (addendum text with propagation diffs, refute-first review, operator acceptance) have no schedule, and T09 cannot be specified until they finish.

**The defect being fixed:** #570 ranks D-MON, D-GO, D-REC and D-HIST as priorities 1–3. Those affect T13, T16/T17 and pre-S8 work, not the two blockers. Its §7.4 audit is the right tool, but it is aimed at the wrong items first. A separate deadline is also exposed: the four-firm §4 falsifier falls due 2026-11-08, needs its own dated re-MC (ruled 2026-09-23), and has no producer scheduled.

## §2 — Execution steps and allowed files

Work in this order. Each step's findings go into the single return file.

1. **Feed: the T00 path.** Using the T00 return and closure, state exactly what P7(b) lacks and the cheapest evidence that would move T00 to GO-evidence: inputs, producer, data access, K/trial accounting, spend, and whether it needs a provider decision first. Then state the alternative: changing the D-feed gate itself. Give its owner, the change-control route, and what it would leave unproven. Return both as options for the operator, with the decision owed. Flag a circular dependency if one exists, for example if T00 evidence needs a feed that needs CP-7, which needs T00.
2. **Route: the amendment schedule.** From the scope note (§5), the §A8 addendum state and T08 §7.10, list the remaining steps to amendment acceptance and propagation. For each step give the inputs, owner, seat, reviewer (D-codex refute-first, plus the cross-vendor review the scope requires), and blocking dependencies (the N1 map residuals for Vanguard and Aegis, Q2 non-entry rules, Q4 sizing from the load-bearing-numbers owner). Name the earliest point at which T09 becomes specifiable. Then state whether the REST route comparison must finish before acceptance, or can run alongside it.
3. **E1 and n3 decision value.** For each production-E1 stage and the sole final n3, give the uncertainty it resolves, the acceptance claim it supports, the decision that would change on each outcome, and whether accepted evidence already covers that claim. Keep portfolio/protection-policy evidence, account-state evidence and implementation parity separate. Return candidates for replacement or removal, each with what it would leave unproven. Recommend nothing that waives qualification.
4. **Remaining T07–T17 prerequisites.** For each, give: the first-session failure it prevents; current evidence; a retain/defer/remove/resequence recommendation; containment and residual exposure; the owner; remaining engineering and operator steps; the decision needed; and the later event that would require a deferred capability. Fold #570's D-MON, D-GO, D-REC and D-HIST into this step as rows. Specifically resolve whether any channel today meets the halt/resume contract's under-60-second acknowledgment and 60-second alternate escalation, which decides whether D-MON is a saving or a gap.
5. **The 2026-11-08 §4 falsifier.** Name the re-MC required to discharge or demote it, its inputs, the producer, and the latest start date that still meets 2026-11-08. Do not run it.
6. **Ordering.** Using steps 1–5, return one dependency-ordered list of operator decisions and work items from now to T15. Mark the critical path and the items that can run alongside it.

**Allowed files:** create exactly one return file, `docs/notes/2026-10-NN-tradeify-critical-path-requirement-audit-return.md` (dated on the day of return), and open one PR containing only that file. Edit no other file.

## §3 — State and interface contract

The return is a decision aid. It does not change any owner. Each finding cites its owner record by path and anchor, and evidence by commit or run ID. Every row in steps 1, 2 and 4 carries the fields listed for its step. A field the executor cannot fill is written `UNKNOWN — <what would establish it>`, never left blank or estimated. The step 6 list names an owner and a decision-or-work type for every entry.

## §4 — Hypothesis and falsifier

**H:** feed and route are the binding constraints on the first full-portfolio session. Clearing them sooner shortens time-to-T15 more than any of the D-MON, D-GO, D-REC or D-HIST simplifications.

**Falsifier:** H is refuted if step 6's ordering shows one of the following:

- the engineering spine (S5 → T12), not feed or route, finishes last before T15 under realistic estimates of when each blocker clears; or
- a D-MON, D-GO, D-REC or D-HIST item sits on the critical path ahead of both blockers.

Report the result either way. A refutation is a valid return.

## §5 — Constraints

- Read-only analysis. Change no owner record, gate, checkpoint, statistical criterion, protection constant, sizing, allocation or strategy parameter.
- No provider, vendor or Tradeify contact. No account or host access. No order action, drill, deploy, arm or spend.
- No private reads (Pine, ports, `local_artifacts/`, account data). No account figures or vendor-licensed content in the return.
- Do not run E1, n3, the re-MC or any measurement. Do not dispatch or card follow-on work. Proposals go in the return.
- Do not reopen ruled decisions: the route path (T08 §7.10), Q1 = B, CP-1a/CP-1b, the S5 rulings and the four-strategy constraint. Report a contradiction found in an owner as `NEEDS_CONTEXT`. Do not resolve it.
- Do not restate current status from mirrors when an owner is available (Rule 7). A conflict between mirror and owner is a finding.

## §6 — Acceptance and return taxonomy

**Return states:**
- `DONE`: all six steps returned, with every row field filled or marked `UNKNOWN — …`.
- `DONE_WITH_LIMITS`: one or more steps partial, each limit named.
- `DONE_WITH_CONCERNS`: all steps returned, but the executor found an owner conflict, stale mirror or risk worth the coordinator's attention. Each concern is named.
- `NEEDS_CONTEXT`: a premise of this card is false at the dispatch revision, or an owner contradiction blocks a step.
- `BLOCKED`: a required input is unreadable or private.

**Verdict on §4's H:** RESOLVED (H holds), FALSIFIED (refuted by the §4 falsifier) or AMBIGUOUS (the ordering depends on an UNKNOWN; name it).

**Acceptance (coordinator, then operator):**
- Every claim cites an owner.
- Step 1 returns both feed options with the decision owed.
- Step 2 names the earliest point at which T09 becomes specifiable.
- Step 4 resolves the D-MON gap-versus-saving question.
- Step 5 gives a latest start date.
- Step 6 is internally consistent with steps 1–5.
- The PR touches only the return file, and the required `skills (3.12)` check is green.

## §7 — Coordinator acceptance / executor return

*(Empty until return. The executor appends the return summary and PR link; the coordinator records acceptance or CHANGES REQUIRED here.)*

```yaml authority
seat: worker
parent: docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md
max_risk: medium
capabilities: [repository.read, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - single_return_file_only
  - no_owner_record_edit
  - no_private_reads
  - no_account_traffic
  - no_broker_or_vendor_contact
  - no_rail_deploy
  - no_rail_arm
  - no_measurement_or_remc_run
acceptance:
  - check_brief passes on the return file (python scripts/check_brief.py <return file>)
  - PR diff is exactly one added file under docs/notes/
  - required skills (3.12) status green on the return PR head
  - every §2 step 1, 2 and 4 row carries its listed fields or UNKNOWN with the establishing evidence named
```

## §10 — Audit hooks

Run from the checkout under test before the return PR is opened:

```bash
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-01-tradeify-critical-path-requirement-audit.md
python scripts/check_md_relative_links.py | grep critical-path-requirement-audit || true
git diff --name-status origin/main...HEAD   # expect exactly one A docs/notes/... line
git diff --check
```

- **Premise drift:** if the 2026-10-01 continuation addendum or STATE queue item 1 has changed since this draft, re-read before step 6 and note the delta.
- **Scope creep:** the PR diff must be exactly one added file under `docs/notes/`.
- **Savings claims:** any "saves", "faster" or "removes" in the return must point to a step 4 row with both paths' remaining work enumerated. Otherwise the coordinator strikes it.
- **Reading 1 preserved:** no route row may treat flatness, empty reads or operator acknowledgment as closing an unknown request.
