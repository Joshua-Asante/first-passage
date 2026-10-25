# Repeated agent roles: codify, fold or retire (2026-10-25)

**Status:** research and recommendations for Joshua. No role is changed by this note; each fold or retirement below needs his call (seat changes run through the surface-allocation ADR's seat table).
**Question:** which agent roles keep being rebuilt by hand across sessions, and which of them should become a skill, fold into another role, or retire?
**Method:** four independent sweeps: live and archived Claude memory, `docs/SESSIONS.md`, and the governance seats (surface-allocation ADR, `scripts/seat_authority.yml`, STATE, campaign §58). Then a merge, then an adversarial check of each row's status and recommendation. Statuses below are the checked ones as of 2026-10-25.
**Policy applied:** the operator's "boundaries only where necessary; simplify by subtraction; one home per rule". Codify only an active role, rebuilt at least twice, whose procedure no repo skill or script holds; otherwise fold or retire.

## Result

Of 30 roles found, **one** meets the codify bar: the merge-train coordinator (about ten incarnations from 2026-09-26 to 10-25). It is codified in this PR as `.claude/skills/merge-train/SKILL.md` and `scripts/merge_train.py`. Every other role is folded, retired or kept as already codified.

| Role (aliases) | Status | Recommendation |
|---|---|---|
| Merge-train coordinator (PR merge-order agent, merge session, Codex merge worker) | active | **Codify**: this PR. The procedure moves out of private handoff memory; the rules stay in AGENTS.md and ADR 2026-10-24b/10-25 |
| Coordinator seat (campaign owner → coordinator (4) → deployment coordinator → First Passage coordinator) | active | **Fold** into one coordinator seat (ADR seat table, `work-decomposition`); archive the superseded handoff memories |
| Deployment Project Manager (PM) | dormant since 10-22 (session archived) | **Retire**; the memory index still lists it as live |
| Relay coordinator (Claude, R1–R6 bundle) | dormant since 10-22 | **Retire** R2–R6 with their deliverables (into the coordinator seat); R1's recipient side folds into `relay-skill` |
| Codex Session Relay (standing hub) | standing holder dormant; relay work runs per exchange | **Retire** the standing hub; keep `relay-skill` as the one procedure, run per exchange |
| Hyper (operator-side relay origin) | active as a relay endpoint (10-24) | **Fold** into `relay-skill` as an endpoint |
| Codex PR reviewer lane | active | **Fold** its stall and CLI-fallback procedure into `merge-train` (done in this PR) |
| Claude stand-in reviewer for docs-only PRs | superseded (ADR 10-24b A, 10-25) | **Retire**; a private memory line still says a Claude review suffices for docs |
| PR fold / review-fix worker | standalone seat superseded; duty active for PR owners | **Retire** the seat; fold the owner-side duty into `babysit`, which loops "until merge-ready" with no review-limit exit |
| PR babysitter | active, codified | **Keep** `babysit`; retire the stale personal copy in `~/.claude/skills/` |
| PR merge-conflict resolver | superseded | **Retire** (`babysit` step 3 covers it) |
| Worker seat (Codex execution, computer use) | active, codified | **Keep** (ADR seat, `seat_authority.yml`, `handoff-verify`) |
| Executive seat (Codex "Astra") | dormant | **Fold**: review into the Codex reviewer lane, goal and acceptance to Joshua, at the seat-table revision the 10-24 addendum defers |
| Escalation lane / adversarial panel | dormant | **Fold** into the coordinator seat, at the same seat-table revision |
| Eligibility register / 11-08 packet owner (R6) | assigned, dormant since 10-22 | **Fold** into the coordinator; it closes at the 11-08 sitting |
| Grant A coordinator (R2) | dormant | **Fold** into the coordinator |
| NinjaTrader card / canary owner | Claude side dormant; 10-26 canary is Codex and Joshua | **Fold** into the Codex worker seat plus the frozen spec |
| Deployment-path lane and card owners | dormant | **Retire** |
| Campaign / experiment owner (per campaign) | dormant (no campaign in flight) | **Fold**: keep the generic ownership rule (campaign §58, STATE); retire the per-instance aliases |
| Portfolio Research Manager (PRM) / research desk | PRM retired 10-24; desk on hold | **Retire** the PRM; the desk stays dormant until Joshua resumes sourcing |
| STATE / SESSIONS roll keeper | active | **Fold**: STATE rolls are already gated and scripted. The SESSIONS keep-30 roll has lapsed with no gate (last entry 10-09; about 68 entries pending) |
| Memory and lessons caretaker | active | **Keep** |
| Repo hygiene / post-merge caretaker | active, codified | **Keep** `repo-hygiene`; fold its memory-only rules into it (check live readers before moving ignored paths) |
| Weekly account-preservation trade | active (Joshua's GO each week) | **Keep** |
| Codex deployment coordinator / combined acceptor | retired | done |
| GLM worker lane, Cursor surface, Ox-alpha lens, persona hierarchy, scheduled sentinel | retired | done |

## What the rows have in common

- **Handoffs live in private memory.** Seat knowledge sits in Claude memory handoff files (five for the deployment coordinator alone), which Codex can't read and which go stale silently. Several stale lines contradict the current ADR, for example "never post `@codex review`", "fast CI defers pytest" and "a Claude review suffices for docs".
- **Roles outlive their sessions.** PM, relay coordinator and Codex Session Relay are still listed as live in the memory index after their sessions went quiet or were archived.
- **The seat table lags practice.** The executive and escalation seats are named in the ADR but not staffed; the 10-24 addendum already defers a seat-table revision to the labor-division research.

## Recommended next steps (for Joshua)

1. Rule on the seat-table revision: one coordinator seat that absorbs PM, relay R2–R6, campaign owner, executive goal-setting and escalation; Codex as reviewer and executor; the merge train as a separate seat.
2. Have the memory caretaker archive the retired roles' handoff memories and fix the stale index lines.
3. Give `babysit` a review-limit exit, so a PR owner stops fixing at the limit the merge train enforces.
4. Decide whether the SESSIONS keep-30 roll still earns its place. Either run it or delete the cap; don't leave it unenforced.
