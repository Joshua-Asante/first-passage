---
name: coordinator
description: Use when holding the coordinator role over Claude or Codex researcher and engineer agents - starting multi-agent work, keeping the board, freezing or dispatching a card, running a review loop on a spec, card or PR, deciding at a review stop ("another round?", "ship with residuals?"), fixing a stale pin, label or token, bringing a decision to Joshua, or judging a worker's return. Procedure only; authority is Rules 0, 2, 3, 4, 5, 6 and 7 of docs/operational_rules.md and the surface-allocation ADR's Addendum 2026-10-28.
---

# Coordinator

Keep several agents' work aimed at the decision it serves, at the lowest cost that can be trusted. This skill is procedure. Authority lives in `docs/operational_rules.md` (Rules 0, 2, 3, 4, 5, 6, 7) and `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` (Addendum 2026-10-28); where they differ from this skill, they win and this skill gets fixed. Evidence: M-50 in `docs/methodology/lessons/methodology_lessons.md`.

## 1. Holding the role

- Joshua assigns the role per session. Without that, you are not the coordinator; ask him.
- Your grants are the `coordinator` seat in `scripts/seat_authority.yml`, narrowed by any card.
- Joshua keeps acceptance, every Rule 3 decision and every dispatch GO.

## 2. Starting work

Before drafting or dispatching anything substantial, write three lines in the owning plan or record:

1. **Decision:** the question, the decision its answer changes, and why now (Rule 9). If that decision cannot be reached by its deadline, say so and propose scaling the work down before starting.
2. **Budget:** Rule 2's line, with review rounds per artifact.
3. **External facts:** each fact about a platform, host, vendor or feed that a guarantee or acceptance test rests on, marked observed (with the probe output) or open. No review round starts while one is open: get a cheap probe, or Joshua's acceptance of it as a named assumption (Rule 0). Drafting may continue.

## 3. The board

- Multi-agent work has one board: `work-decomposition`'s parent manifest. PRs in the merge train use `merge-train`'s table. Make no other tracker.
- Hand finished PRs to the merge-train conductor (`merge-train`), which orders and merges them; you do not merge.
- You are its single writer: one row per unit (owner, card, frozen hash or head SHA, status), reconciled each turn against the real branches and returns.

## 4. Cards and dispatch

- Author with `brief-authoring`; gate with `handoff-verify`. Before freezing and before dispatch, run them through the checkout's launcher (`.p.ps1 doctor`, then `.p.ps1 python scripts/check_handoff_authority.py <card>` and `.p.ps1 python scripts/check_brief.py --type handoff <card>`); both must be clean.
- **One pin source.** The freeze record holds every hash. Generate a card's pin tables from it and diff card against record before each review and before dispatch; never hand-copy a hash. For a Claude dispatch, also pass the record's pinned inputs as `scripts/dispatch_claude.ps1 -InputFile`, so the runner rehashes them on resume.
- **Rehearse the harness.** Before freezing a real card, run a throwaway card through the same launcher (`scripts/dispatch_codex.ps1` or `scripts/dispatch_claude.ps1`), sandbox roots, skills, read allowlist and writes near pinned files. Fix what breaks once.
- **Real-consumer acceptance.** An acceptance check calls the consumer's own entry point, never a sub-validation. Bind every exemption to an exact span and give it a negative test.
- Name the cross-agent reviewer (Rule 5).

## 5. Review loops

- Declare the round budget before round 1 (Rule 2).
- Ask the reviewer to mark each finding blocking or non-blocking. Its mark, not yours, is the blocking bar.
- Track findings by failure family: the same mechanism, whatever the wording. A second failed correction in one family stops the loop even while the count falls (Rule 7).
- At any Rule 7 stop, choose one:
  - **Ship** a spec, card or private artifact with reviewer-marked non-blocking findings, logged in it. Never with an omitted required check, never an irreversible change on a spent budget. PRs follow Rule 6.
  - **One more round**, only when the budget alone stopped the loop and Rules 6 and 7 allow it.
  - **Restart cleaner:** a card or spec defect, you rebuild it in a fresh session; an implementation defect, the PR's owner rewrites.
  - **Ask Joshua** for anything Rule 3 names, including waiving a blocking finding.

## 6. Consistency-only fixes

Without asking, fix only what Addendum 2026-10-28 B covers: pins, hashes, version labels, self-references, stale tokens, and harness or tooling fixes that change no behaviour. A file whose hash is frozen or under review gets a new version-named file and freeze record, and a dispatch GO bound to the old hash is asked again for the new one. Cite the exact file hash or head SHA, write "consistency-only (surface-allocation ADR Addendum 2026-10-28)" in the PR body or record, and get one cross-agent delta review. Frozen evidence, agreed rules, ruling text and claims are out of scope.

## 7. Bringing a decision to Joshua

- One decision per ask, recommendation first, with its critical-path status, in the decision-packet form of the surface-allocation ADR. A Rule 3 item never defaults on silence.
- Keep each reply option under 300 characters, or put the options in a file he confirms.
- Record his answer verbatim in its owner before anything cites it.

## 8. Returns

- Statuses are Rule 4's four. `NEEDS_CONTEXT` gets one re-anchor, then a re-cut (`work-decomposition`); `BLOCKED` follows its sub-case (`brief-authoring`).
- Judge a return against its artifacts (`handoff-verify` §Post-execution). Your adjudication is input; Joshua accepts on the evidence pack.
