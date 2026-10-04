# S5 Q9: closing a never-retried, retry-eligible IN_DOUBT, and when the salt is revealed (decision note, 2026-10-02)

**Status:** PROPOSED. This note is input for the coordinator to put to the operator. It decides nothing and applies no owner text.

**Why now.** The C3 ruling of 2026-10-01 reassigned Q9 "to the RC-4 slice, before F1" ([execution-slices ledger `:1914`](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01)). The checklist's CP-6 row lists it as an F1 freeze input (`2026-09-20-tradeify-deployment-checklist.md:492`). The [K3/RC-4 card draft](../briefs/handoffs/2026-10-02-k3-rc4-service-salt-client-view-DRAFT.md) §3.1 needs it before freeze.

**Base:** `main@bd30646`. Code citations are at that commit.

## 1. The question

S5 decision draft §6 Q9 (`docs/notes/2026-09-26-s5-decision-draft.md:409`): "Closure of a retry-eligible IN_DOUBT that is never retried: is the campaign closed (and the salt revealed) once no retry can fit the original deadline, or only by an operator VOID?"

It has two parts:
- **(a) Closure.** When does a retry-eligible IN_DOUBT that is never re-executed stop holding the campaign open?
- **(b) Reveal timing.** Once the campaign is closed, when and how does the client receive the salt?

## 2. What the owner text already fixes

| # | Fixed point | Owner (cited) |
|---|---|---|
| F-1 | No salt or seed value reaches the client before the campaign is "irrevocably closed to further computation and recovery" | Full-E1 spec §2.2a (`docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:84`) and §2.4 (`:113`) |
| F-2 | "the salt is not disclosed to the client while a re-execution remains possible" | Spec §2.6 bounded rule (`:157`) |
| F-3 | Eligibility: a compute checkpoint IN_DOUBT from interruption on the same boot, with no finalized capture; once per interruption and at most twice per campaign; "under the campaign's original deadline and allowance, charged on top of the interrupted work's charge" | Spec §2.6 (`:157`) |
| F-4 | "Until that slice is accepted, no release performs a re-execution and every IN_DOUBT stays terminal." So the Q9 state cannot arise before the D3 recovery slice (H9 R2) lands | Spec §2.6 (`:157`); [H9 R2](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h9--resultseal-integration-and-bounded-same-sample-recovery-two-checkpoints) |
| F-5 | The campaign deadline is an absolute BOOTTIME value fixed when the budget is bound. A reboot or clock fault makes the campaign BUDGET_UNCERTAIN, which is never eligible | `campaign_store.py:2941-2943`; S5 draft R1 (`:311`) |
| F-6 | VOID belongs to the operator alone (`'operator': {'STATUS', 'VOID'}`), and VOID is a closed state | `campaign_protocol.py:94`; S5 draft §1.4 public-reveal row (`:121`) |
| F-7 | A pending recovery barrier keeps the campaign open | S5 draft `:121`, citing `campaign_budget.recovery_pending` (`:166-168`) |

Draft text, accepted as input but not applied as owner text:
- R4 (`:314`): "If it does not fit, the campaign ends exhausted."
- The abandonment row (`:122`) lists "deadline lapse" and "an interruption that is no longer re-execution-eligible" among the closed states.

## 3. When the state arises

Recovery leaves a work IN_DOUBT with an absence proof (R2, `:312`). The re-execution is reserved afterwards, and only by the service's recovery path, with no client operation (R1, `:311`). In normal operation the retry follows at once, so a durable "eligible but not re-executed" state survives only when:
1. the service does not return on the same boot until after a retry could still fit (R4); or
2. the service returns, and it reaches the retry only after the original deadline or allowance can no longer cover the phase's installed limits.

A reboot ends eligibility (F-5). If zero records are retained and no reproducibility evidence exists, the work is terminal rather than eligible (R7, `:317`). An interruption of the second re-execution is terminal (R9, `:319`). Those cases are closed already. Q9 covers cases 1 and 2.

## 4. Options

**A. Feasibility closure (automatic).** The campaign closes once no re-execution can fit. That happens when:
- R4's check fails for the eligible work: the remaining wall time to the original BOOTTIME deadline, or the remaining allowance, is below the phase's installed limits (an unknown charge counts as the full reservation);
- R9's limits are spent; or
- eligibility is lost (BUDGET_UNCERTAIN).

The service commits this as a durable terminal transition. Infeasibility uses the existing `BUDGET_EXHAUSTED` reason, as R4 states, so no new state name is needed. The recovery path evaluates it on each start and recovery pass, and the existing deadline timer does too. A STATUS read never evaluates it lazily. The operator can still VOID earlier.
- *Variant A′ (an implementation shape for D3, not a separate policy):* recovery completion either reserves the re-execution or records the work as not eligible, in one commit, so the eligible-but-not-reserved state is never durable. Case 1 then becomes a recovery barrier that stays pending until the service returns (F-7), and A's rule decides at that point.

**B. VOID-only closure.** A retry-eligible IN_DOUBT keeps the campaign open until either a re-execution runs or the operator VOIDs. Nothing closes it automatically.

## 5. Reveal timing (part b; the same under A and B)

- **Trigger.** The salt becomes client-visible from the commit that closes the campaign irrevocably, meaning all four conditions of S5 draft §1.4 (`:121`) hold:
  - no work of any phase can still be reserved, dispatched, re-executed or recovered;
  - every work is settled;
  - no recovery barrier is pending;
  - the state is terminal.

  Before that commit, no surface carries it (F-1).
- **Mechanism.** The reveal is a projection of that durable state into the client's STATUS. It is not a separate act, and it is not an operator step. The admission receipt is immutable, so it keeps only the commitment. At reveal the service checks that the salt is canonical 64 lowercase hex and matches the commitment (S5 draft §1.6, `:153-154`).
- **Irreversibility.** Every closing state is terminal and absorbing. The BOOTTIME deadline is monotone within one boot, and a reboot makes the campaign BUDGET_UNCERTAIN. So no path can reopen eligibility after a reveal, and a preview after reveal is harmless (delta K3 residual, `docs/notes/audits/2026-09-25-qualification-assurance-contract-delta.md:245-246`).
- **Admission crash.** The crash-after-binding case already follows this rule: "the salt is revealed once recovery completes" (S5 draft §1.6, `:161`), because the pending recovery barrier keeps the campaign open until then (F-7).
- **Before D3 lands.** The eligibility term is empty (F-4). The predicate reduces to "terminal, settled, no recovery barrier pending", so K3/RC-4 can implement and test it without D3. D3 adds the eligibility term.

## 6. Recommendation: A (with A′ where D3's design allows), and the §5 reveal timing

Reasons:
1. **It fits the text already written.** R4 ends a non-fitting retry as exhausted, and the abandonment row counts deadline lapse as closed (`:314`, `:122`). B would need an owner sentence that contradicts both.
2. **No unbounded open state.** Generating the salt consumes the attempt (`:122`). Under B, a campaign whose retry never happens stays open, unrevealed and unresolved until an operator acts. Because a successor needs a new authorization citing the predecessor's record (`:122`), B adds a mandatory VOID to that ops path, and it has no owner today.
3. **Custody is equal.** Under A, closure happens only when no computation or recovery remains possible, which is exactly the condition F-1 and F-2 attach to disclosure.
4. **Machine-checkable, with existing parts.** It reuses the bound deadline (`campaign_store.py:2941-2943`), the existing exhaustion terminal and the trusted campaign clock. R4 needs the same "fit" computation in any case.
5. **What B offers, and why it is weaker.** B adds an explicit human decision before reveal and avoids defining "fit". But R4 defines fit anyway, and reveal after closure carries no custody risk.

**Risk under A, with its guard.** An error in the feasibility computation goes one of two ways:
- If it closes the campaign while a retry could still fit, a retry is lost. That is an operational loss, not a custody breach.
- If it keeps the campaign open too long, the reveal is delayed. That is custody-safe.

So the rule should close only when infeasibility is certain: compare against the installed phase limits and the charge-on-top accounting, and close nothing on an estimate.

## 7. What each option unblocks

| | A (recommended) | B |
|---|---|---|
| K3/RC-4 slice | Implements the reveal predicate (§5) and its tests now: "the same campaign reveals once it is closed" (S5 draft §1.6, `:157`). The "retry-eligible IN_DOUBT does not reveal" half lands with D3 against the same predicate | Implements reveal for VOID and the other terminals. The predicate must also exclude eligible IN_DOUBT indefinitely |
| D3 slice (H9 R2) | Gets a closure rule: R4 infeasibility → `BUDGET_EXHAUSTED`, committed by recovery or the timer | Must keep an eligible IN_DOUBT open until a retry or a VOID. Owes no closure transition |
| Operator procedure | None new | An abandonment VOID procedure, owed before F1 (no owner today) |
| Owner text | One added sentence in spec §2.6 (below) | A correction of the draft abandonment row's "deadline lapse", plus a §2.6 sentence making VOID the only closure |
| CP-6 Q9 item (checklist `:492`) | Closes when the ruling is recorded and the slice lands | Closes when the procedure and the owner correction land |
| CQ-3 / OF-7 (host-obligations note §D.1) | Unaffected. CQ-3 concerns the pre-admission read | Unaffected |

## 8. Proposed owner text (PROPOSED; not applied; it lands through the operator-accepted owner-text route)

In full-E1 spec §2.6, after "…and the salt is not disclosed to the client while a re-execution remains possible.", add:

> "A re-execution-eligible IN_DOUBT that is not re-executed closes the campaign once no re-execution can fit the campaign's original deadline and allowance (the campaign ends BUDGET_EXHAUSTED), once the per-campaign limit is spent, or once eligibility is lost (BUDGET_UNCERTAIN). The service commits that transition; it is never inferred by a status read; the operator may VOID earlier. From the commit that irrevocably closes the campaign, the client's status carries the salt, validated against the admission commitment; before it, no client surface does."

## 9. Decision requested

The operator chooses **A** or **B** for part (a) and accepts or amends §5 for part (b). The coordinator then records the ruling in the execution-slices ledger, under the RC-4 entry (`:895`). It routes the §8 text, or B's corrections, through the owner-text route, and freezes card §3.1 item Q9 to match.

**Not decided here:** the D3 implementation (H9 R2); the G5 private salt route (S5 draft Q8, `:408`); any cryptographic encoding (card §3.1); CQ-1..CQ-3.
