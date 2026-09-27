# B–D packet: two parallel drafts (UB-8 comparison; S5 decision draft) — dispatch card

**Status:** DISPATCHED 2026-09-26. Operator direction, in session, relayed through the Chief of Staff's return: "Proceed with the integrated B–D packet and the UB-8 scenarios. Also authorize a bounded S5 decision draft in parallel. Neither should begin implementation."
**Coordinator:** the coordinating Claude Code session (Opus 5.5). It accepts or corrects each return and owns the integrated B–D packet.
**Executors:** one assessor subagent per task, each in its own git worktree and branch named below.
**Dispatch revision:** the commit that adds this card. The Task 1 executor verifies that its `HEAD` descends from it. The Task 2 executor branches from `main` and reads this card at that revision with `git show <revision>:<path>`.

**Common rules**
- Read `AGENTS.md` first.
- Write only the result file named for your task. Commit it locally; do not push.
- Do not change code, contracts, STATE, plans or ADRs. Proposed owner text goes *inside* the result file, quoted as proposed.
- No private source, account figure, P&L, credential or vendor contact. No `.env`. No GLM or external service.
- Run `.\fp.ps1 check` (PowerShell 7) before committing, and report its `record.json` path.
- Return: status (`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`), commit SHA, `git diff --stat`, check result, and open questions.

## Task 1 — UB-8 bounded availability comparison

**Branch / worktree:** `claude/ub8-availability`, from this revision.
**Result:** `docs/notes/2026-09-26-ub8-availability-comparison.md`.

**Question:** is continuity after an unresolved request needed for the first attended release? In other words, does option B earn its implementation and operating burden over preserve-and-block under credible scenarios? This answers [incident ADR §A9.1](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md) UB-8 and the §A10 acceptance condition. It does **not** decide close or protection feasibility (D19 / gate C), and it must not delay that work.

**Method**

1. **Compare the two postures under identical scenarios and assumptions:**
   - preserve-and-block, the current rule (`book_account_owner.py:1608`);
   - Proposed B, as §A10 writes it: rules 4′, 4a–4c, 9′, 11, 12 and rule 8 exhaustion.
2. **Scenarios (all six):**
   1. no unresolved requests;
   2. one unknown that stays unresolved;
   3. several symbols hit by one outage;
   4. an unknown just before the session reset;
   5. a partial split followed by lost monitoring;
   6. repeated unknowns across days.
3. **Compare, per scenario:**
   - trading opportunities lost under preserve-and-block;
   - additional opportunities B admits;
   - reservation accumulation and exhaustion;
   - operator interventions and unresolved obligations;
   - implementation and verification work each posture requires.

   For the work comparison, use the allocation map's rows C06b, C15, C15b and B16 and the §A10 OPEN items.
4. **No failure-rate estimate.** Data is sparse, so express frequency as explicit scenario parameters with stated uncertainty. Show where the conclusion flips, as break-even conditions.
5. **Figures stay symbolic.** B's allowance, room and figures are unbound (UB-2 and UB-6 are open), so use symbols. Request and trade counts may come only from **tracked public documents**, cited. No account balance, P&L or private export.
6. **Don't claim what isn't established.** In particular, never claim that trading stops "after a few unknowns"; derive exhaustion only from the stated symbols.

**Output:** a recommendation to the operator, in one of three forms: B needed for the first release; B not needed (the first release runs preserve-and-block); or it depends on named conditions. Give the decisive assumptions.

## Task 2 — S5 decision draft (bounded; S5 stays held)

**Branch / worktree:** `claude/s5-decision-draft`, from `main` (independent of the controller architecture).
**Result:** `docs/notes/2026-09-26-s5-decision-draft.md`.

**Question:** the three open decisions in the [contract-delta audit](../../notes/audits/2026-09-25-qualification-assurance-contract-delta.md): the §5.1 assurance boundary, N1 resource accounting and N2 deterministic recovery. Answer them as **proposed owner amendments** that the operator can rule on. The S5 hold stays in place ([ledger entry](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-freeze-held-2026-09-25)).

**Must cover**

1. **Boundary B-1..B-5.** Make the credential, administrator, signing-key and Docker-socket assumptions explicit, as operational facts to verify rather than assume. Add seed custody for K3: who generates the salt and when; when configuration is irrevocably committed; who can see the salt before reveal; and how abandonment after reveal stays visible and consumes the authorized attempt.
2. **N1 accounting**
   - An **enforceable cumulative** resource limit. A cgroup CPU quota limits rate, not cumulative consumption, so state the cumulative mechanism and a deadline that survives restart. Ground it in the current supervisor code: `ops/c1_rail/qualification/` and its campaign supervisor, budget and funding modules.
   - A **comparison of the proposed mixed model** (per-phase for N1/N2; campaign-scope for Part A, result and seal) **with a uniform campaign model**, on forward complexity, migration risk against accepted S2 evidence, and cost.
   - The rule for a valid stage result when the campaign is exhausted: retain the result as evidence, stop further work, and withhold whole-campaign completion unless its required evidence already exists.
3. **N2 recovery.** Bounded same-sample re-execution, with:
   - the original worker terminated or fenced first;
   - sample identities committed before execution;
   - the original resource envelope and deadline retained;
   - retained attempt history;
   - an explicit rule for the zero-retained-records case (rely on demonstrated determinism plus pinned identities, or return unresolved);
   - the existing limits: one retry per interruption and two per campaign.
4. **Owners.** For each amendment, name the owner document and exact place, and quote the proposed text.

**Output:** a reviewable decision packet with a recommended ruling per decision and the evidence behind it. No code, no owner edits and no S5 release.
