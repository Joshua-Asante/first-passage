# Scope — bounded-exposure amendment for unknown requests (T08 option a)

**Status:** SCOPE, not an amendment. Authorized by the operator's 2026-09-24 ruling ([T08 §7.8](../../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md#78-operator-ruling-on-the-return-2026-09-24), part 3). It changes no contract; every owner named in §3 stays in force until an amendment is accepted and propagated. Live release is held meanwhile (§7.8 part 1).
**Date:** 2026-09-24 · **Author:** Claude (coordinating session) · **Operator:** Joshua.

## 1. The problem the amendment must solve

The accepted contracts treat an unknown request (sent, no response, outcome unknown) like this:

- Rail E3: "Each unresolved request owns an account block."
- Halt/resume §3: recovery is complete only when there are "no unresolved requests". Elapsed time, empty reads, flatness and operator acknowledgment are insufficient.
- Halt/resume §4: "A still-active fault or unresolved owner cannot be overridden."
- CAP R3 and the closure plan's Step 2 outcome table, row "Not found, timeout, partial history or unsupported retention": preserve the attempt and its block. No resend, no reservation release.

All four assume that some fence can eventually resolve the request. T08 found none on this route (R3 = NONE). **As written, one timed-out request blocks automated trading on the account permanently.** Manual trading still works: the weekly preservation trade is unaffected. The only other exits are an account end or a new account.

Halt/resume §4 already anticipates this: "a different evidence/route protocol requires a concrete separately reviewed amendment, never an operator waiver checkbox." This note scopes that amendment.

## 2. The questions the operator has to rule

**Q1: What can end or contain an unknown request's block? This is the question the whole amendment depends on.**

| Option | Mechanism | What it depends on | Assessment |
|---|---|---|---|
| **A. Vendor-bounded fence** | For the narrowed shape only, an unknown request is treated as having no future effect once a vendor-stated bound plus a margin has elapsed, and only if no effect was observed in that window. | A written CrossTrade bound covering durable recovery and OCO repair ([vendor question](../../notes/2026-09-24-t08-vendor-question-draft.md)). | The only source-backed clear. Elapsed time is evidence here only because the vendor bound makes it so, which §3's "elapsed time is insufficient" must be amended to say. Unavailable if the vendor declines. |
| **B. Bounded-exposure reservation** | Replace the account block with a permanent worst-case reservation. The unknown request's possible exposure (quantity × distance to its attached native stop, plus a gap/slippage allowance) is charged against the account's remaining drawdown room and never released without evidence. Admission continues with the reduced room. Any later effect that can't be explained is quarantined as an incident (halt, attended recovery). | That the native OSO stop attaches atomically with the entry, so an entry cannot exist without its stop (source evidence still owed: T08's N1 map was not reached). A gap allowance the operator accepts. | Contains risk rather than resolving it. Each unknown permanently narrows the account; after a few, trading stops by arithmetic, not by ruling. Works with no vendor answer. |
| **C. Operator-attested residual risk** | The operator reconciles on the platform and signs acceptance of the residual risk. | Nothing external. | **Not recommended.** It is the "operator waiver checkbox" §4 forbids, and §3's acknowledgment exclusion exists for the case where the platform shows flat while a request is still in flight. |
| **D. No amendment** | Live release stays held. | — | The default if nothing is ruled. |

**Recommendation:** adopt **B** as the base posture, with **A** as an optional release of B's reservation if and when a vendor bound arrives. B works without any vendor answer, and A later returns capacity without changing B's invariants.

**Operator ruling (2026-09-24, in session, verbatim):** "I accept B. You can proceed as scoped." **Q1 = B.** The amendment is authored on the bounded-exposure reservation. A stays available only as the optional release the recommendation describes; C and D are not adopted. Proceeding as scoped means §5 steps 2–4: the N1 map, the addendum text with its propagation diffs, and the refute-first review. Acceptance (step 5) remains the operator's. This ruling changes no owner text and grants no implementation, route work, drill or spend.

**Q2: Unknown non-entry requests.** Closes, cancels, amendments and flatten are requests too. An unknown close leaves exposure possibly unreduced. An unknown cancel or amend leaves protection in an unknown state. B's reservation is defined for entries. For the rest, the recommended rule is that any unknown non-entry request triggers the incident-ADR "protection uncertain" row: immediate attended intervention, with no autonomous protection claimed. The amendment has to state this per request type.

**Q3: Is the narrowed shape enough for the book?** T08 §7.7 admits only "a plain market or stop entry carrying its own native OSO stop, sent without `delay=`, ATM fields, `cancel_after` or copier fan-out." The four legs also use adds, native amendments, trailing (native continuous only; the inline triggered-trail is already UNSUPPORTED for L2(g)), scoped exits, the Aegis takeover and the scheduled flatten. Which of these fit the narrowed shape is T08's N1(a)–(g) map, never run because R3 returned early. **The amendment can't be accepted until that map exists.** If a leg can't be expressed in the narrowed shape, the choice is to drop it from the automated scope or requalify the book. That choice goes to the operator; the amendment doesn't make it.

**Q4: Sizing the reservation against the venue rules.** The gap allowance and the cap on concurrent unknowns have to be sized against the account's trailing drawdown room, enforced intraday (`lesson_tradeify_trail_enforced_intraday`). The numbers belong with the load-bearing-numbers owner, not here. The amendment names the rule; the figures come from that owner at binding time.

**Q3 outcome (N1 map, 2026-09-24):** no leg is shown to fit as publicly declared. ORB fails on L2(g) (trailing); Striker fails on L2(f) (bare entry, then attach) and multi-contract cover; Vanguard and Aegis are undetermined because their protection cases are private. Most of this comes from the route's normal-path gaps (L2(e)/(f)/(g) unsupported), not from option B. B adds a one-contract-per-request rule, because the broker sizes the stop to the entry's first fill. The detail is in the addendum's §A4. Whether to requalify changed expressions or reject the route is a new operator decision, outside the amendment. **Ruled 2026-09-25:** requalify — route-native editions of ORB (fixed-stop bracket, no trailing) and Striker (entry carrying its stop; one-contract requests), K=1 pre-registered; Vanguard and Aegis attested to fit. Owner: [campaign record §59](../../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#59--route-native-expressions-for-the-accepted-book-three-operator-rulings-2026-09-25). The amendment now covers only the residual "timeout and no observed effect" class.

## 3. Owners the amendment must change (exact places)

| Owner | Place | Change needed |
|---|---|---|
| [Halt/resume contract](../../spec/2026-09-14-tb-s3-halt-resume-contract.md) | §3 paragraph 2 ("no unresolved requests"; elapsed-time exclusion) | Recovery may complete with unknown requests held under a reservation (B), or cleared by a vendor-bounded fence (A). Every other exclusion stays. |
| same | §4 ("unresolved owner cannot be overridden"; producer requirement) | Resume is allowed while reservation-held unknowns remain, if the remaining room passes admission. Name the amendment as the "concrete separately reviewed amendment". |
| [Rail extension spec](../../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) | E3 row and its acceptance case ("completing one cannot unblock admission") | "Owns an account block" becomes "owns a permanent worst-case reservation" for the narrowed shape. Other request shapes keep the block. |
| [CAP-20260916](../../briefs/phase4-preparation/2026-09-16/capability-decision.md) | R3 row; standing consumer outcome | Dated addendum: R3 disposition under the amendment. R3 stays NONE as a fence finding. |
| [Self-service closure plan](../../superpowers/plans/2026-09-16-self-service-capability-closure.md) | Step 2 outcome table, row "Not found, timeout…" | Add the reservation outcome beside "preserve and block". |
| [Bounded platform-protection incident ADR](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md) (Proposed) | §2 table, row "Unknown entry, add, cancel, close or modification" | This is the row the amendment rewrites. |

**Recommended vehicle:** a dated addendum to the Proposed incident ADR, not a new ADR. It rewrites that ADR's own row and needs the same propagation to the same owners, so one acceptance carries both.

## 4. Invariants the amendment must keep

- No resend on absence. No speculative cancel or repair of an unknown request.
- Flatness, empty reads and operator acknowledgment never close an unknown request. Elapsed time closes one only under option A's vendor bound.
- A reservation is never released without evidence (a uniquely correlated outcome, or A's bound).
- Any unexplained later effect is an incident: halt, attended recovery, quarantine through the existing owner.
- No new command permission. Only the narrowed shape is admitted; other shapes keep today's block.
- No agent places, amends or cancels an order. Drills need their own written authorization.

## 5. Next steps and order

1. **Operator rules Q1** (recommended: B, with A as an optional release).
2. **Finish T08's N1(a)–(g) map** against the narrowed shape. This is documentary; it answers Q3 and supplies the OSO-atomicity evidence B needs.
3. **Author the addendum** to the incident ADR plus the propagation diffs for the §3 owners, with Q2 and Q4 written as rules.
4. **Review:** a separate-session refute-first panel (D-codex (a)); a cross-vendor review before acceptance, because this changes a live-risk contract.
5. **Operator acceptance**, then propagation. Only then can T09 be specified against the amended E3.

The vendor answer (option A) can arrive at any point. It changes step 3's text, not the order of the steps.

## 6. Forbidden while scoping

Editing any §3 owner's text; recording anything QUALIFIED under this scope; implementing reservation logic; sizing figures in this file; treating this note as acceptance of option A or B.
