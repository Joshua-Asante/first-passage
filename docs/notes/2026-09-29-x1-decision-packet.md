# X-1 decision packet: one attended REST entry and native stop

**Date:** 2026-09-29.
**Status:** PREPARED FOR DECISION; NOT CLEARED TO EXECUTE. *2026-09-29:* A-11 exception accepted and the evening window withdrawn (§2 decision record); still not cleared to execute.
**Selected outcome:** A reviewable decision packet and preparation checklist for one attended X-1 entry-and-stop observation. Execution remains a separate CP-3 decision.
**Dispatch scope:** Preparation only. Prepare the observer procedure and decision materials; Joshua performs the offline platform rehearsal. This dispatch authorizes no order-producing action or execution of §5. Proposed limits remain proposals until explicitly accepted.
**Execution prerequisites:** The A-11 ruling below, reviewed observer procedure and rehearsal evidence, operator-fixed limits and private request binding, then X-1's own written CP-3. All fresh session checks remain owed.
**Ownership:** Joshua performs every platform/API action and owns CP-3; the deployment coordinator reviews the trace and retains combined route acceptance. This session prepares the packet only.
**Verification:** Original request/response/read bytes, local send times, identity chain, teardown evidence and manifest hashes, assessed against the drill plan's X-1 criteria.
**Checkpoint:** Return the preparation package for coordinator review. The exact session-time request binding must return for written CP-3 before any send. After separately authorized execution, return immediately on any stop condition and after teardown.
**Preparation return boundary:** Reviewed observer procedure, operator rehearsal evidence (or explicitly outstanding rehearsal), A-11 disposition (or pending ruling), and the private authorization worksheet with every unresolved field identified. Stop at this return; Joshua retains the separate execution decision and every order-producing action.
**Later execution return boundary:** Only after written CP-3, one row and its evidence. No next row, repeat entry, route acceptance or deployment follows from this packet.

## 1. Owners and source identity

The [deployment checklist](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) remains the roadmap.
The [drill plan](2026-09-26-tradeify-route-drill-plan-draft.md), including its 2026-09-28 corrections, owns row semantics.
The [commissioning packet](2026-09-27-route-commissioning-session-packet.md) §§2, 3 and 4.1 owns the attended procedure and CP-3 fields.
This packet narrows the next decision; it does not replace those owners.

Prepared against main `1ca4233b5f486f2946b4bbad3b2d13b427370ecb`; reviewed and revised against main `3ce500e` (PR #550 merged).
PR #550 at `924dd8ca2bcf76d102aae33ed948165ead94cd8e` records the operator's R-2 closure with limits.
The private closure and its evidence were reviewed locally: 89 sealed files and both adjudications match their pins.
Both runs remain STOPPED(HTTP_FAILURE). Recovery across sessions is unestablished.
The investigation is closed for that target; there is no scheduled repeat or support follow-up.
An X-1 decision does not reopen R-2.

Already decided: existing REST entitlement; no equivalent sandbox reported; drill costs count against the standing ceiling; Tradeify permission is conditional; each row needs its own approval.
The exact account binding stays private. Proposing the incumbent evaluation environment below is not approval to use it.
No current host/account condition is inferred from earlier captures.

## 2. A-11 / GC-7 decision

**Conflict:** the current Stage 1 procedure stops if a competing actor cannot be disabled. Firm-side risk liquidation may be configured and outside operator control.
The existing actor inventory explicitly returns this case for operator/coordinator decision.
Merely scheduling away from a timed liquidation does not eliminate threshold liquidation or its race with protection.

**Recommended disposition for decision:** allow X-1 preparation to reach CP-3 under a narrowly documented exception for identified, non-disableable firm risk controls.
The exception must be accepted before a Stage 1 session starts. It does not claim exclusive close ownership or make manual intervention race-free.

Proposed owner amendment, to be adopted in the drill plan and mirrored in commissioning §2.2 only if accepted:

> For X-1 only, identified non-disableable firm risk liquidation is recorded as an external risk-control actor and need not be disabled. All operator-configurable competing senders remain disabled. The operator records the applicable timed and threshold controls privately, confirms the proposed window avoids known scheduled liquidation, and expressly accepts that threshold liquidation may still occur. Any firm-side intervention ends X-1 immediately: retain the actor and outcome, perform the existing attended recovery, and return without a PASS claim for an uncontaminated X-1 trace. An unknown request remains held; a flat snapshot does not resolve it. This exception grants no X-3/C-a exclusivity, close guarantee, other-row permission or live-release acceptance.

**Alternative:** retain the current Stage 1 hold until a compatible environment or different accepted actor contract exists.
Do not attempt to disable a firm's mandatory risk controls.
If the configured controls cannot be identified adequately for the decision, return that missing fact and keep X-1 held.

**Review notes (2026-09-29; for the decision, not part of the amendment text):**
- **Scope of ROUTE STOPS.** Drill plan §0.1 makes a non-disableable actor a route-level consequence: "ROUTE STOPS while C-a is the close candidate". The exception above changes only whether an X-1 session may start. It leaves that consequence standing for C-a and X-3, and the ruling should say so explicitly.
- **Owner.** GC-7 itself is owned by the [B–D packet](2026-09-26-tradeify-bd-decision-packet.md). An accepted exception is mirrored in its GC-7 row, as well as in the drill plan and commissioning §2.2.
- **Threshold exposure.** Before CP-3, the operator privately confirms that the account's headroom to its trailing-drawdown floor is a large multiple of the row's planned cost allowance. That makes threshold liquidation during X-1 implausible, although not impossible. No figure appears here.

**Decision record:** ~~no ruling supplied in this authoring session. The recommendation is PROPOSED.~~ **Operator ruling 2026-09-29, in session ("proceed as recommended"):**
1. **A-11:** the narrow exception quoted above is **ACCEPTED**, for X-1 only.
   - The review notes are part of the ruling. The drill plan §0.1 ROUTE STOPS consequence for C-a and X-3 stands unchanged.
   - The drawdown-headroom check is a CP-3 item.
   - It is mirrored in drill plan §0.1, commissioning §2.2 and B–D packet GC-7.
   - It is an exception to the session-start rule only. It grants no CP-3, row, send or spend.
2. **Sequencing:** the 2026-09-29 evening window is **withdrawn**. X-1's CP-3 is not requested until R-1 has run on this week's preservation trade, in that trade's own session. That R-1 is the same-session per-order read check (§6 gap 2).
   - **Open sequencing item (recorded 2026-09-29; for Joshua, not resolved here).** This week's preservation trade was placed on Monday 2026-09-28 and became R-2's target (closed with limits, #550). No R-1 read is recorded in that trade's own session. The earliest retained read (`reads/R2prep-20260929T003518Z…`, 2026-09-29 00:35 UTC) falls after the reset. The condition above therefore cannot be met this week without an extra trade, and no extra trade is authorized. Joshua's options:
     - (a) run R-1 on next week's preservation trade (due 2026-10-09), in its own session;
     - (b) rule, under CP-2 F-3, that X-1's own REST-placed order may supply the same-session read, which would remove the separate R-1 prerequisite for X-1.
     - Neither is chosen.
   - If its per-order reads fail, X-1 stays held.
   - The observer review, the offline tool and the operator rehearsal remain owed.

## 3. Proposed row and missing operator inputs

| Item | Proposal or required input |
|---|---|
| Environment | Incumbent eval, explicitly named by Joshua in this row's CP-3; no automatic fallback |
| Instrument and size | MYM front month, away from roll, one contract per request and in total; resolve the dated contract privately before approval |
| Direction | Propose buy for this isolated observation; direction is part of the final CP-3 |
| Entry | One market order carrying absolute stopLoss in the same request |
| Take-profit | Propose omitted for X-1; X-3 is a separate decision and later position |
| Entry time in force | Propose explicit day; never rely on an undocumented default. Native exits remain GTC under the retained documentation |
| Quote and manual recovery | **Tradovate web confirmed by Joshua.** Retain quote price and timestamp immediately before send; rehearse locating position, working orders, flatten and cancel controls before the row |
| Stop distance | **Proposed:** absolute stop 30 index points below reference quote; abort if actual fill-to-stop distance exceeds 40 points (40 is `<OP: max stop distance>`, commissioning §3.6) |
| Reference quote side | **Proposed:** the ask for a buy, the price a market buy is expected to fill near. Record which side was used |
| Stop-activation wait | **Proposed:** 10 seconds after first observed fill; known rejection or unknown request triggers recovery immediately. Delayed fill observation is not a measured activation bound |
| Time in market | **Proposed:** teardown as soon as evidence is obtained; initiate teardown no later than 120 seconds after first observed fill. This is not a guarantee of flatness by that time |
| Session window (ET) | ~~**Availability confirmed:** 2026-09-29, 19:00-19:30 EDT (23:00-23:30 UTC).~~ **Withdrawn 2026-09-29 (operator ruling, §2).** Next available evening after the preservation-trade R-1 and the other prerequisites; named at CP-3. Session checks and CP-3 remain owed |
| Planned cost allowance | **Proposed:** $30 total including fees and adverse execution; one entry attempt. This is a planning allowance, not a guaranteed maximum loss; no repeat attempt. It counts against the $700 ceiling (CP-2 F-4), whose remaining headroom is confirmed privately at CP-3 |

Only availability and platform are confirmed. Numerical limits and row selections remain proposals, not executable defaults.
The final private binding must record explicit acceptance of the proposed limits or their agreed replacements.
The exact contract, quote source, selected direction, take-profit choice and tif are also confirmed in the final private binding.
No entry is approved while any field remains unresolved.

## 4. Request and evidence binding

Use the retained commissioning §3.7 C.2/C.3 schema. This is a field contract, not an executable payload:
`instrument` = exact approved contract; `action` = approved lowercase direction;
`qty` = 1; `orderType` = market; `tif` = explicitly approved value;
`orderId` = fresh per-attempt identifier; `stopLoss` = tick-valid absolute level derived from the retained reference quote and approved distance.
For the proposed buy, stopLoss is below the reference quote.
Do not send clOrdId separately: the documented orderId forwarding supplies it.
No limitPrice or stopPrice for a market entry. Omit takeProfit under the proposed selection. With no takeProfit, the stop child arrives as `oso1Id` and there is no `oso2Id` (commissioning §3.7 C.2).

Apply the drill plan's extended excluded-field list unchanged: no ATM, trailing, strategy-sync, flatten-first, cancel-after or routing additions.
A price move can make the realized stop distance exceed the authorized distance; that is an abort after fill, not permission to widen the allowance.

Before CP-3, retain privately:
- exact serialized request body and SHA-256, without authentication material;
- authorization record with all selected limits, session and environment identity;
- operator attestation of Tradeify's five conditions, using commissioning §1.1's wording;
- the A-11 decision and privately identified controls;
- evidence destination and designated owner for any outstanding request.

Account identifiers, figures and originals remain in the approved private evidence root. Public return contains hashes and a scoped outcome only.
At dispatch the coordinator rechecks the retained request schema for drift; changed vendor semantics return for review.

Before CP-3, the private binding must also name the approved quote-freshness interval and quote-movement condition that require returning for approval; neither has an executable default here. Prepare and hash the exact quote-bound request first, then obtain written CP-3 for those bytes and limits. Immediately before sending, recheck the approved freshness and movement conditions and all session gates. A failed recheck, expired session window, or any change to the serialized request (including contract, direction, quantity, stop, tif or orderId) requires a refreshed binding and renewed CP-3 before sending. Do not silently reprice or rehash an approved request. A new quote alone does not authorize new request bytes.

*Review note (2026-09-29):* the paragraph above requires byte-specific CP-3 within the quote-freshness interval. Codex (the author) agrees that is unnecessarily restrictive and recommends the amendment below.

**Amendment (derivation-rule CP-3): ACCEPTED by the operator 2026-09-29. It replaces the byte-specific CP-3 paragraph above.** Source: Joshua's statement "I accept the derivation-rule", made in the coordinating session on 2026-09-29 and confirmed by Joshua directly in this session the same day ("I accept the derivation rule"). The paragraph above is superseded wherever it requires byte-specific approval; its recheck and no-silent-repricing duties continue through items 2–3 below.

1. **Scope.** CP-3 approves a deterministic derivation rule and a reviewed generator/checker version, instead of quote-bound bytes. The rule binds:
   - the account/environment, the exact dated contract, the direction, `qty` = 1, `orderType` = market, `tif`, and the excluded-field list;
   - the quote source and side (the ask, for a buy), the freshness interval, the permitted quote movement and the session window;
   - the stop rule. For a buy: `stopLoss` = the tick-grid value obtained by subtracting the approved distance from the recorded ask and **rounding up** to the contract's tick. Rounding up never increases the quote-to-stop distance. The result must also pass the approved validity checks;
   - how the fresh per-attempt `orderId` is constructed, with exactly one entry attempt;
   - every recovery limit (the wait, the time in market, the realized-distance maximum and the cost allowance).
2. **Before the send.** The operator runs the approved generator/checker. It retains the quote (price, side and timestamp), the derived level, the exact serialized bytes and their SHA-256, and the mechanical validation result.
3. **Stop and renewal rules.**
   - A failed check stops the attempt; nothing is repriced by hand.
   - A new quote may produce new bytes only through the approved rule, with a new validation record. That record is retained, so no repricing is silent.
   - Any change to the rule, the limits, the generator/checker version, the contract, the direction or the environment requires a renewed CP-3.
4. **Unchanged.** Joshua still performs the send. Everything else in this section stands.

~~Until the operator accepts this amendment, the paragraph above governs.~~ Accepted 2026-09-29. CP-3 approves the rule and the generator/checker version; that tool is not yet built or reviewed.

## 5. Single-row sequence and verification

This sequence belongs to the later operator-executed row, not to the preparation dispatch.

1. Confirm the A-11 disposition, reviewed observer procedure and completed operator rehearsal. Read actual host disarm/emission state this session; inventory every actor.
2. Read account-wide flatness, working orders and outstanding requests. All must meet commissioning §3.2 before sending.
3. Record the quote and timestamp, tick-valid level, fresh orderId, exact serialized request and hash in the private binding. Obtain written CP-3 for that binding. Immediately before send, recheck §4's freshness/movement conditions and the session gates; return for renewed CP-3 if required. Record local send time as Joshua sends the approved bytes once.
4. Retain response, entry/child identifiers, lifecycle/status reads, fill identities and quantities. Read account-scoped fill-reconciled positions; do not substitute raw singular-position reads.
5. Apply the drill plan's X-1 pass/fail/abort criteria, including quantity, first-fill stop activation, identity correlation, partial outcomes and realized stop distance. HTTP acceptance alone is not PASS.
6. Teardown using commissioning §3.4. On a known outcome, attended platform flatten plus cancel; on an unknown outcome, read first and intervene only as that procedure permits. Never resend an unknown request.
7. Retain fresh post-action flatness, no working orders and terminal evidence for every involved id. Missing terminal evidence leaves a named outstanding obligation even if flat.
8. Seal originals and return one scoped outcome. No further row runs in the session.

All SC-1 through SC-7 remain binding, as do the time limit and the A-11 exception's additional stop.
An unknown outcome may suspend automation indefinitely under the accepted preserve-and-block posture.
Recovery/evidence collection continues; automation does not restart that session.
An R-2 failure after reset cannot be replaced by a flat snapshot or durable-fill lookup.
X-1 does not manufacture a lost response or protective-fill race.

**Interpretation:** an uncontaminated PASS supports only the observed MYM/REST/environment/date entry-and-stop behavior.
It establishes no activation-time distribution, cross-symbol equivalence, negative closure, accepted-modify behavior or C-a close guarantee.
A GC-2a failure retains the route-wide stop consequence; a correlation abort is classified separately under GC-6.

## 6. Evening preparation and unresolved checks

Public sources checked on 2026-09-29:

- [Tradeify commission schedule](https://help.tradeify.co/en/articles/10468315-trading-commission-fees) lists MYM at **$1.82 per contract round trip**, including exchange, NFA, clearing and commissions, based on its free membership structure. Use this as the published estimate; confirm applicability to the bound account. Fees may change.
- [Tradeify permitted times](https://help.tradeify.co/en/articles/10495876-rules-permitted-times-to-trade) allows the evening session after 18:00 ET and requires flatness by 16:45 ET the following trading day. Holiday exceptions still require a current check. The selected evening window falls within ordinary hours; this does not identify all configured liquidation controls.
- [Japan's official release calendar](https://www.e-stat.go.jp/release-calendar/detail/00550300/202609300850) schedules industrial production for September 30 at 08:50 JST, September 29 at **19:50 EDT**. Its 15-minute exclusion would start at 19:35. This single check does not establish an all-market news clearance. Retain a fresh complete calendar before CP-3; do not extend the session on the strength of this observation.

At MYM's $0.50 per index point, the proposed 30-point distance represents $15 before costs; 40 points represents $20. Adding the published round-trip fee gives $16.82 and $21.82 respectively, before adverse execution. These are arithmetic illustrations, not loss guarantees. Contract-value source: [CME MYM introduction](https://www.cmegroup.com/content/dam/cmegroup/notices/ser/2019/04/SER-8360.pdf).

**Readiness gaps discovered in retained evidence:**

1. The September 29 Stage 0 inventory leaves ATM/trigger replay (A6), scheduled requests (A8), platform timed exits/cancels (A10), and firm liquidation controls (A11) unresolved. Earlier disarm samples do not establish tonight's state. Joshua must identify these and disable configurable competing senders before Stage 1; the proposed A-11 exception covers only identified mandatory firm controls.
2. R-1 v3.1 collects completed orders and treats Working/Suspended as an unexplained effect. It cannot be reused as X-1's live protective-stop observer. No tested X-1 observer or completed operator rehearsal is claimed here. Before CP-3, establish a read/capture procedure that can correlate the returned parent and child identities and show the stop's working quantity and price within the selected wait. Tradovate web alone does not establish the REST identity chain. The preparation deliverable must name the read surfaces/endpoints and fields used to correlate parent/child ids, working stop quantity and price, fills and account-scoped positions; retain original responses/screens and local observation timestamps; define polling and the selected wait; and map missing/rejected-stop and unknown-response outcomes to commissioning §3.4. The coordinator reviews the procedure against retained documentation and available examples. Record unavailable fields or untested steps as blockers rather than inferring them. Complete and retain the operator's no-send rehearsal before CP-3; no live order is authorized to validate the observer during preparation.
   *Prepared 2026-09-29:* the observer procedure v0 is in the private worksheet folder as `X1_OBSERVER_PROCEDURE.md` (SHA-256 `da22ea177786b1bd0823c43456be0a6c331b88adaf8b298c20ec485ed14dead6`). It is **PROPOSED and UNTESTED**. *Codex reviewed v0 on 2026-09-29 and returned corrections. Revised as v1, `X1_OBSERVER_PROCEDURE_V1.md` (SHA-256 `49ab29ec04bc197e50e7ead6fd2d350dc5ba0f65d441ff7e82f72c4fb48cfaf1`). v1 adds an enforced request budget, bounded concurrency, timeouts, 429 handling, a no-fill deadline, triggers checked as each response arrives, error-specific triage, explicit version paths, identity-validated status reads, a scheduled entry-lifecycle read, SC-5/SC-6 and the A-11 stop, and an outstanding-request record. Codex re-review of v1 is owed.* The procedure names the read surfaces and fields, the capture rules and the outcome-to-§3.4 mapping. It records these blockers:
   - **No successful REST per-order read is established in retained evidence for this account.** Browser-rendered lifecycle displays exist, but they are not REST responses. The R-2 closure records the lifecycle, order and status reads by id all failing with HTTP 400 for historical orders, cause unconfirmed. Same-session behavior is unestablished.
   - Stop quantity and price are observable only in the lifecycle `version`. The status read carries neither, and a `partial` lifecycle reply means not observed.
   - No offline observer tool or tests exist yet.
4. **Recommended sequencing (from gap 2):** run R-1 on this week's preservation trade, in its own session, before X-1. It checks same-session per-order reads with no added exposure. If those reads fail, X-1 can yield no PASS and should stay held. The 2026-09-29 evening window is therefore premature unless R-1 has completed first. *(2026-09-29: this week's trade cannot serve; see the open sequencing item in §2.)*
5. The exact account, contract, fresh quote, absolute stop level, fresh orderId and serialized request hash remain private session-time bindings. No executable request has been prepared from a stale quote.

**Offline rehearsal checklist (not yet performed by the operator):** with no send action, locate Tradovate web's position and working-order views and the required flatten/cancel controls; walk through accepted entry, missing/rejected stop, unknown response, and already-flat cases. For each, identify the evidence to retain and the governing recovery branch in commissioning section 3.4. An unknown response never leads to a retry. A flat display never substitutes for terminal order evidence. Do not test these controls against an exposed account as part of preparation.

The private session worksheet is `local_artifacts/route-drills-2026-09/x1-prep-2026-09-29/SESSION_BINDING.md` in the primary checkout. It records missing fields explicitly. Preparation is ready for review; execution readiness remains open on the items above and the decisions below.

## 7. Decision and return

The preparation executor returns the observer procedure and its review status, rehearsal evidence or outstanding rehearsal, A-11 ruling or pending decision, and the private worksheet with unresolved fields. Preparation may complete as a reviewable return while execution remains held; unresolved execution prerequisites must be explicit.
The next operator decision is the A-11 proposal plus the completed X-1 row binding.
The coordinator presents the exact final packet for CP-3 after the missing limits and private request are supplied.
Approval of this document's preparation is not CP-3.
Preparation used retained files and public documentation. No new account/host read, trade, drill, host change, vendor contact or spend occurred.
