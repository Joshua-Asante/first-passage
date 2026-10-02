# T08 drills and T07 account reads: one attended operator session (plan, 2026-09-25)

**Trade-authority clarification (2026-10-01).** Categorical statements below that agents may not place trades, exit positions or cancel orders are **historical, superseded** by [ADR Addendum 2026-09-30b](../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-30b): Agents may place orders, exit positions and cancel orders only at the operator's direction for the specific act; `trade.submit` is an operator act at risk `high`, never grantable in a card. Arming, live-spend and per-session GO requirements are unchanged. This artifact grants no order action; its task-specific exclusions, named performers and separate drill approvals remain in force. It does not supply direction for a specific trade.

**Status:** PLAN. Authorized in principle by the operator on 2026-09-25 (verbatim below). *Pointer 2026-09-26: see the §0 addendum; D1–D4 are not treated as cleared for execution and each returns as an individual decision.* **Joshua performs every platform action; no agent places, amends or cancels an order or reads the account** (AGENTS.md live-execution posture; CAP-20260916 "Bounded collection and rehearsal procedure": "Joshua performs separately approved platform actions"; T07 §5–§6). Before the session, the operator confirms the **scope block** in §2 with one written "approve drill scope"; the CAP requires exact symbol, quantity and limits to be approved per test, and this block is that approval.
**Owners:** [T08](../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md) (drills, CAP R2–R5/N1), [T07](../briefs/handoffs/2026-09-21-tradeify-t07-manual-settlement-procedure.md) (reads, CAP S2), [incident ADR Addendum 2026-09-24](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#addendum-2026-09-24--bounded-exposure-reservation-for-unknown-requests-proposed) §A1 (admission precondition).

## §0 — Operator authorizations (2026-09-25, in session, verbatim)

| Item | Ruling | Scope granted |
|---|---|---|
| T08 drills | "I authorize the remaining T08 drills" | D1–D4 below, performed by Joshua, under the §2 scope once confirmed. No agent order action; no manufactured lost response or transport failure (CAP); no drill beyond this list. |
| T07 reads | "I authorize the account-side reads" | R1–R3 below, performed by Joshua; original bytes retained privately and hashed. No agent account access. |

Neither grants broker access to an agent, arming, a route change, deployment, D-broker (still void under T08 R3 = NONE) or spend beyond the session's own commissions (§2).

**§0 addendum (dated rows; the 2026-09-25 rows above are unchanged):**

| Date | Ruling | Scope |
|---|---|---|
| 2026-09-26 | REST reads R-1 and R-2 only, authorized after existing entitlement is confirmed. Operator ruling and coordination, 2026-09-26, relayed in session, with the operator's structured-question answer the same day (R-CLOSE) | Scope and steps in the [drill-plan draft](2026-09-26-tradeify-route-drill-plan-draft.md#operator-ruling-2026-09-26-recorded): operator-performed R-1 and R-2 only, within the draft's exact read-only scope, after confirming existing CrossTrade REST entitlement (the drill plan proposes how the confirmation is recorded; that procedure is not part of the ruling). R-1 and R-2 are the drill-plan draft's REST reads, not this plan's T07 reads R1–R3. No purchase, new access, route change or order mutation is authorized |
| 2026-09-26 | D1–D4 not treated as cleared for execution; each returns as an individual decision. Same source (R-CLOSE) | The ruling directs that normal-case drill decisions be prepared individually after their documentary prerequisites are met, with the exact environment, actions, exposure limits and abort/recovery procedure returned before execution approval is requested, and with no automatic fallback to the live evaluation environment; the deliberate protective-fill race drill is deferred. The 2026-09-25 in-principle authorization of D1–D4 above was not formally revoked, but it is superseded in practice by that requirement: D1–D4 are not treated as cleared for execution, and each returns as an individual decision naming its environment (the §2 scope block's incumbent-eval environment is not a default). No order-producing drill is authorized. The T07 reads R1–R3 read the D1 transaction, so they cannot run before D1 is individually decided; the ruling does not address them otherwise. The 2026-09-25 rows above are unchanged |
| 2026-09-27 | Read target: a completed operator-placed preservation trade may be the target of the T07 reads R1–R3 (and of R-2) where it meets the required evidence conditions; R-1 must observe a same-session trade the operator places anyway. Operator ruling adopted in session by structured answer ([incident ADR §A11.3](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a113--operator-ruling-preservation-trade-evidence-as-the-target-of-authorized-reads-2026-09-27)) | Changes the target of reads already authorized; it adds no read. It lifts, for a qualifying preservation trade, the §0 addendum's dependence of R1–R3 on D1. The ruling's words are "after entitlement and target confirmation", for the authorized reads. Whether the entitlement condition also applies to the T07 report exports is returned as a CP-2 question (commissioning packet F-3a); until it is answered, T07 R1–R3 are gated on entitlement too. The transaction identity is confirmed by the operator first. *(Corrected 2026-09-27 by the coordinator: this row first read "Entitlement (for the REST reads)", a parenthetical not in the ruling.)* No new trade, purchase, account reset or agent account access |

## §1 — Why one session covers both

A one-contract MYM entry sent through the route with its own stop, placed after the 18:00 ET reopen, is:
- the narrowed-shape request the incident ADR's §A1 admission precondition needs a trace of (single-call entry+bracket creation, first-fill activation sized to the fill);
- the position the remaining K rows need (modify, close, cancel);
- a **post-rollover** transaction, which is what T07 needs to discriminate the Cash History `Date` meaning and the export query bounds;
- the week's account-preservation trade, if placed Monday–Thursday evening. A Friday-evening trade belongs to the next week's session and does **not** cover the current week.

## §2 — Scope block (operator confirms before the session)

| Field | Proposed | Confirm |
|---|---|---|
| Account / environment | Incumbent Tradeify Select eval, Tradovate, via the operator's own CrossTrade webhook (not the rail; the rail stays disarmed, `dry_run=true`). Account identifiers never written in any repo, task or chat text. | ☐ |
| Symbol / quantity | MYM front month, **1 contract** per request, never more | ☐ |
| Protective stop | A fixed distance the operator chooses for safety (not a strategy parameter), sent as CrossTrade `stop_loss` on the same `place` request | ☐ |
| Window | Mon–Thu, 18:00–23:00 ET, attended throughout; not within 15 minutes of a scheduled high-impact release | ☐ |
| Request shape | No `delay=`, no ATM fields, no trailing fields, no `cancel_after`, no copier / multi-account fan-out | ☐ |
| Cost | A few MYM one-lot round trips' commissions and slippage. Operator states whether this counts against the $700 rail spend ceiling | ☐ |
| Venue rules | Operator confirms Tradeify permits evening-session trading on this account type | ☐ |

**Starting state (R5, before any action):** record privately, with no identifiers, the enabled external actors (managers, copiers, other platforms, open manual sessions), the open positions, the working orders and any outstanding requests. The starting state must be flat, with no working orders. If it isn't, stop.

**Stop rule (every step):** any identity conflict, any effect you can't explain, a partial or unknown outcome, missing capture or uncertain protection **ends testing**. Flatten attended, record what happened, and go no further.

## §3 — Drills (T08 residual rows)

| Drill | Action (Joshua) | Question it closes | Evidence to retain (private, hashed) |
|---|---|---|---|
| **D1** | Send one narrowed-shape market buy for 1 MYM with `stop_loss` | §A1 precondition: is the entry created together with its bracket in one call, and does the stop activate on the first fill at the filled quantity? | The CrossTrade response bytes; a Tradovate order-history export showing the entry and the linked stop, with the stop's quantity (1) and state (Working) after the fill; the fill export |
| **D2** | With D1's position open, submit **one** modify of the working stop to a level on the wrong side of the market (a price Tradovate should refuse) | L2(c): after a rejected modify, is the old stop still working, unchanged? | The rejection bytes; an order export after the rejection showing the original stop still Working at its original level. If the modify is **accepted and executes**, the position closes; record that and skip D3 |
| **D3** | Close the D1 position with the route's full-position close | L2(d): does a full close leave no orphaned protective order? | Exports showing position 0 and the D1 stop in a terminal state (Cancelled), with no Working remainder |
| **D4** | Place a resting buy **stop entry** far enough above the market that it won't trigger during the session, with `stop_loss`; then cancel the parent | Does cancelling the parent end the suspended bracket leg? | Exports showing the parent and its child both terminal; no fill |
| ~~D5~~ | none | Exit-side partial fills | **Moot by construction:** under the one-contract rule, an exit is for one contract and can't partially fill. Recorded, not drilled. |

## §4 — Account reads (T07 S2)

| Read | Action (Joshua) | Question it closes | Evidence |
|---|---|---|---|
| **R1** `Date` meaning | The day after the session, export Cash History and Account Balance History covering **both** the calendar date of the D1 fill and the next date | Does the D1 row's `Date` carry the calendar date or the session date? (The fill is after the 17:00 ET rollover, so the two differ.) | Original export bytes, each hashed |
| **R2** Query bounds | Export Cash History twice: range = the calendar date only, then range = the session date only | Which single-day range includes the D1 row: is the query bound calendar-dated or session-dated? | Both original exports, hashed; note the exact range entered |
| **R3** `Timestamp` offset | Find a **zone-explicit** source instant for the same D1 transaction: (a) the CrossTrade response or alert-history timestamp, if it carries an explicit zone or `Z`; or (b) a browser network capture of the Tradovate web platform's own response for that transaction, if it carries zone-explicit times. **Scrub session tokens and cookies before retaining a capture.** Compare the result with the Cash History `Timestamp` for the same transaction ID | The Cash History `Timestamp` offset in the current (daylight-saving) regime | The zone-explicit source bytes plus the export row. **Repeat once after 2026-11-01** (DST ends) for the second regime. A UI display is not a source (T07 §6). Whether (b) is admissible is the coordinator's ruling under T07 |

## §5 — Retention and return

- Private roots only: `local_artifacts/t08-drills-2026-09/` and `local_artifacts/t07-reads-2026-09/` (gitignored). File names carry no account identifiers.
- Hash every file and write a `MANIFEST.tsv` (path, SHA-256, capture time UTC, step id).
- Give the coordinating session the two manifest SHA-256s plus a one-line outcome per step (for example "D2: rejected; old stop Working, unchanged"). No figures, identifiers or P&L.
- The coordinator records outcomes in CAP (R2–R5/N1 and S2 rows, dated addendum), T08 §7 and T07 §7. **Documentation-only rows stay UNPROVEN until these traces exist.** A drill trace qualifies only the behavior it observed.
