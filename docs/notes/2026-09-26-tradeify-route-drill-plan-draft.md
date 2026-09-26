# Tradeify route drill plan (DRAFT for authorization; nothing authorized)

**Status:** DRAFT, 2026-09-26, for operator review. Drafted by an agent session for the coordinator. **Nothing in this file is authorized, ruled or accepted.** It is the concrete plan that the operator's 2026-09-26 executive review recommends (executive review 2026-09-26; operator ruling pending) before any order-producing drill on the CrossTrade REST route is authorized ([B–D packet](2026-09-26-tradeify-bd-decision-packet.md) §2 item A-1 and §6 decision 2). It also proposes two read-only REST reads for authorization now. Every direction attributed to the executive review is *recommended (executive review 2026-09-26); operator ruling pending*. Gates B, C and D stay pending on the [T09 gate table](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t09-gate-acceptance-record). This file grants no drill, access, spend, release or GO.

**Inputs:**
- the [2026-09-25 operator session plan](2026-09-25-t08-drills-t07-reads-operator-session.md) (webhook form; its authorization table and D1–D5 rows);
- the [REST route assessment](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md): §6.2–§6.4, §6.6 and §6.9, plus the Gate A drill map and interface rule in §6.11;
- the packet's §1, as revised on 2026-09-26: the GC rows, the evidence standard, the consequence classes, and the §1.1a close-amendment outline, which that section owns;
- incident ADR [§A1 and §A6](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#addendum-2026-09-24--bounded-exposure-reservation-for-unknown-requests-proposed);
- the [rail spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md)'s `CLOSE(scope)`, S5 and R-B3 L-2;
- the [halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md) §1 and §3;
- the [CAP](../briefs/phase4-preparation/2026-09-16/capability-decision.md) bounded collection and rehearsal procedure.

Vendor facts are cited by the REST assessment's quote IDs (Q-nn). Operation names are used only as that assessment and the packet name them. No parameters are added.

## Authority (binds every row)

| Rule | Source |
|---|---|
| The operator (Joshua) performs every platform and API action, including reads. No agent places, amends or cancels an order, or reads the account. | AGENTS.md live-execution posture (no agent places a trade); CAP procedure, "Authority" row (Joshua performs separately approved platform actions); session plan Status line (no agent reads the account) |
| A row runs only under its own written operator authorization, naming environment, symbol, quantity and limits. The 2026-09-25 in-principle authorization of the session plan's webhook-form D1–D4 does not extend to any row here. | Session plan §0; Gate A drill map |
| The c1 rail stays disarmed (`dry_run=true`). Daemon emission stays off (`emit_enabled=false`). The operator confirms the actual host state before each session. | AGENTS.md |
| No manufactured lost response or transport failure. No request is resent after an unknown outcome. | CAP procedure (none proposed); session plan §0; checklist T09 verification; REST §6.4 |
| Evidence is private: original bytes go under `local_artifacts/route-drills-2026-09/` in the operator's **primary checkout**, which is gitignored (a worktree copy can be deleted with the worktree), and are hashed into `MANIFEST.tsv`. File names carry no account identifiers. Credentials and session tokens are never captured. The coordinator receives the manifest hashes and one outcome line per step, with no identifiers, figures or P&L. | Session plan §5 |

## Mapping by behavior and interface, not by D-number

The session plan and the REST return number their drills differently. Authorization and evidence bind to the **row here**, never to a D-label alone (Gate A drill map).

| Behavior to establish | This plan | Session plan (2026-09-25) | REST return §6.9 | Interface in this plan | Packet row |
|---|---|---|---|---|---|
| Same-session reconciliation recipe on a known order | **R-1** | — | D4 | REST reads | GC-6 |
| Prior-session lookup by id after the ~17:00 ET reset | **R-2** | — | D5 | REST reads | GC-6 |
| §A1: one-contract entry and bracket created in one call; stop activates on the first fill at quantity 1 | **X-1** | D1 (webhook form) | D1 | REST `orders/place` | GC-2a |
| L2(c): a rejected modify leaves the old stop working | **M2**, then **X-2** | D2 (webhook form) | D2 | Documentary first (M2); then REST `change`, command report | GC-2b, GC-3 |
| L2(d): a full close by liquidation leaves no working protective order | **M**, then **X-3** | D3 (webhook form) | D3 | Documentary first (M); then REST `close` (`liquidateposition`) | GC-1 (C-a), GC-3 |
| Cancelling a resting stop entry ends its Suspended children | **X-4** | D4 (webhook form) | D6 | REST `orders/place`, `cancel` (packet §5) | GC-4 |
| Liquidation against an in-flight protective fill (reversal) | **M**, then **X-5** | — | — | Documentary first; then REST `close` | GC-1 (new) |
| Exit-side partial fills | — | D5 ("moot") | — | — | Not drillable at one contract. The "moot" fact is withdrawn pending UB-5 (incident ADR §A8 note and §A9.1; Proposed, not accepted). A whole-leg liquidation of several lots can still fill partly (§2.5 fault cases). |

**Evidence reuse rule.**
- A trace counts only for the interface and environment it exercised (Gate A interface rule).
- Webhook-form evidence (session plan D1–D4) counts for REST only for a **downstream property that both forms demonstrably share**. For example, first-fill stop activation counts once both forms are shown to produce the same Tradovate `placeOSO` with the same observations. §6.5's same-call argument has not been accepted as that demonstration.
- Three things always need REST evidence:
  - REST request classification (the §6.3 outcome mapping);
  - correlation (`clOrdId` to lifecycle; Q05, Q20);
  - observation through the REST reads.

## §0 — Prerequisites

### 0.1 Exclusivity and actor inventory (GC-7)

Exclusivity prohibits **uncoordinated** actors on the account (recommended, executive review 2026-09-26; operator ruling pending). Before the first order-producing row of each session, the operator records privately, with no identifiers, the state of each actor class below (CAP R5; REST §6.2). If any actor is not in the required state, the session ends before it starts.

| Actor class | Source | Required state for a drill session |
|---|---|---|
| Trade Copier with this account as leader or follower | Q11, Q26 | None active |
| Account Manager: auto-close, scheduled or window flatten, Block Signals, Closing Only | Q27 | Disabled. If one stays active, record its expected effect on each row; a vendor flatten would be a second close owner (packet B-12). |
| CrossTrade managed layers (ATM strategies, trigger replay) | Q12, Q30 | None active; no `atm*` fields sent |
| CrossTrade coverage repair on bracket placements | Q15; Gate A A8 | Request shape cannot exclude it. Record it as a vendor actor. Any OCO pair it places is an unexplained effect and ends testing. |
| Scheduled or queued work (`cancel_after`, outstanding requests) | REST §6.2 | None |
| Other senders: TradingView alerts to the account's webhook, other API clients, other platforms, manual sessions other than the drill session | CAP R5; halt/resume §1 | Disabled or closed |
| The drill's own REST client, operated by the operator | This plan | The **sole permitted sender** for the session, recorded as such in the inventory |
| Our runtime (c1 rail, signal daemon) | AGENTS.md | Disarmed (`dry_run=true`) with emission off, confirmed on the host. This is the runtime's required state, not an account fence (halt/resume §1) |

**Two kinds of operator action are coordinated, not excluded.**
- **The drill sends.** Each order-producing row's REST requests come from a separately authorized, attended operator actor: the drill's own REST client, which the inventory records as the session's sole permitted sender. They are not the halt/resume §3 intervention procedure.
- **Attended intervention.** Under halt/resume §3, the operator manages positions and protection through the trading platform while the runtime is fenced; INTERVENTION permits no runtime broker mutations (halt/resume §1). This plan's recovery flatten (§2.0) is such an action.

Exclusivity accommodates both under three conditions:
1. automation is fenced before the operator acts;
2. every manual action is logged with its time and treated as a claim that still needs outcome evidence;
3. automation resumes only after reconciliation from fresh, coherent evidence (halt/resume §3) and a new operator resume (halt/resume §4).

"Fenced" here means the runtime's required state: rail disarmed and emission off, confirmed on the host. That is not an account fence. Halt/resume §1 says a `dry_run` config write "is neither an account fence nor proof of flatness", and forbids claiming that manual action is race-free without evidence. The concrete platform procedure is owed at T13.

**"Approved" (for the packet owner).** Packet GC-7 and B-12, and executive-review correction 5, call the intervention procedure "approved". Halt/resume rev9 records approval of its attended amendment for packet 0 only (contract freeze and feasibility work, not implementation or live operation), and the concrete platform procedure is owed at T13. This plan therefore does not call it approved. The coordinator routes the wording to the packet owner.

Other operator-placed trades on the four symbols, such as the weekly account-preservation trade, need one of two treatments: the same handling (automation fenced, reconciliation afterwards), or a symbol outside the four. Which one is **OPEN** for the operator (packet GC-7). A drill session with any such trade open or working does not start.

An inventory attests the state at one time; it does not prove later absence, so repeat it at the start of every session. **Consequence (packet GC-7):** ROUTE STOPS while C-a is the close candidate and an actor cannot be disabled, because D-B9's quantity-less close needs an exclusively owned symbol. Otherwise the result is a named actor to disable.

### 0.2 Entitlement and venue permission (P-1)

- **Before any REST call, reads included:** the operator confirms REST access. It needs the Pro plan; entitlement is vendor-reported and not independently checked (Q01).
- **Before any order-producing row, also:**
  - venue permission for CrossTrade-mediated automated orders on this eval (packet P-1; a firm-level classification is not enough);
  - the session plan §2 venue-rules and cost items, including whether drill costs count against the rail spend ceiling.

### 0.3 Environment (OPEN)

**OPEN:** does a non-funded demo or simulation environment exist with the same route semantics, meaning the same CrossTrade REST calls reaching the same Tradovate behavior, observed through the same reads? This plan does not assert that one exists.
- **If one exists:** a trace there counts for the eval account only under an accepted equivalence argument, as the interface rule requires.
- **If none exists:** rows run on the incumbent eval account with one micro contract. That exposure is real and counts against the account's drawdown rules.

The operator names the environment in each row's authorization.

## Part 1 — Read-only REST reads (recommended for authorization now)

Reads cannot place, change or cancel anything. They still use the operator's REST credential against the live account, so each needs its own written authorization.

**Known order (R-1 and R-2).** Proposed definition, which the operator confirms in each read's authorization: an order on this account that the operator placed, whether in an authorized drill or as an operator-placed trade such as the weekly account-preservation trade, whose order id, and caller `clOrdId` if it has one, the operator learned and retained privately with original bytes **in the order's own session**. An operator-placed order outside any drill therefore qualifies only if its id was retained that way. **Best source order:** X-1's order, which is REST-placed with a known `clOrdId`. Until X-1 is authorized, an order from an authorized session-plan drill or another qualifying operator-placed order can serve, subject to R-1's OPEN row.

### R-1 — Same-session reconciliation recipe on a known order (REST return D4; GC-6)

| Field | Content |
|---|---|
| Question | Does the documented same-session recipe locate a known order on this account and recover its children, status and fills? |
| Account scope | The one incumbent eval account, named generically. Every read targets only that account. A 401, 403 or 409 response (auth, plan, unlinked, ambiguous account; §6.3, Q06) ends the read with no inference. |
| Preconditions | (1) Written operator authorization for R-1. (2) A known order, as defined above. (3) The same session as that order: before the next ~17:00 ET reset (Q10, Q22). (4) §0.2 REST access. (5) Rail disarmed, daemon silent. |
| Read operations, in order | 1. List working orders and all session orders (Q07). 2. Read each candidate's lifecycle; the `New` command carries the `clOrdId` (Q20). 3. From the match, take the order id, the children through `ocoId`/`parentId`/`linkedId`, and `ordStatus` (Q20). 4. Read fills by `orderId` (§6.4). 5. Read fill-reconciled positions (§6.4). |
| Excluded | The recipe's last step, placing again when no order carries the id (Q08). The REST return rejects it (§6.4), and it is forbidden here. No `orders/place`, `change`, `cancelreplace`, `cancel` or `close` call. |
| Recorded | For each response: original bytes, local request time and operation name. No credentials or headers. Saved under `local_artifacts/route-drills-2026-09/reads/` and hashed into `MANIFEST.tsv`; never committed. |
| Would establish | For this order at this time: whether the `clOrdId` search locates it, and whether the link fields recover its children, status and fills. |
| Would NOT establish | Uniqueness: a repeated `clOrdId` is accepted (Q05). Anything about an absent order: there is no negative inference (§6.4). Fill completeness (Q23, Q24). A recovery rate or a recovery-time bound: one success bounds nothing. Cross-session behavior (R-2). REST placement classification (X-1). |
| Consequence (GC-6) | Not a route stop. Under preserve-and-block, unknowns stay blocking and R-1 bears on how long (packet §3). Under option B, it limits what UB-7 can resolve. |
| OPEN | If the known order was not REST-placed (webhook- or platform-placed), which `clOrdId`, if any, it carries is not established. R-1 then exercises steps 1 and 3–5 only, and the `clOrdId` match waits for a REST-placed order (X-1). |

### R-2 — Prior-session lifecycle lookup by id (REST return D5; GC-6)

| Field | Content |
|---|---|
| Question | After the ~17:00 ET reset, does a lifecycle read by id return a prior-session order, or `unknown_order` (§6.9 D5)? |
| Account scope | As R-1. |
| Preconditions | (1) Written operator authorization for R-2. (2) A known order, as defined above (id learned and retained **in its own session**); attribution survives the reset only for ids learned before it (§6.6). (3) At least one ~17:00 ET reset since that session, with the elapsed interval recorded. (4)–(5) As R-1. |
| Read operations, in order | 1. Lifecycle read by id for the known order (§6.9 D5). 2. Status per id for the order and its known children (§6.3). 3. Fills by `orderId`; that history is periodic and its completeness unverified (Q23, Q24). 4. Control read: list working and session orders (Q07). The prior-session order is expected to be absent (Q22); record the result either way. |
| Excluded | Any mutation. Also, a cross-session `clOrdId` search presented as recovery: the documented search is session-scoped (Q22). |
| Recorded | As R-1, under the same root. |
| Would establish | Whether this read returns a prior-session order by id on this account after this elapsed interval, and whether its children and fills are recoverable by id. |
| Would NOT establish | A retention limit (how many sessions or days); readability of other orders; recovery of a request whose order id was never learned (the lost-response case, §6.4); any processing bound or fence; a recovery-time bound. An `unknown_order` result shows unavailability at this interval only. A retention probe needs repeated reads at stated intervals, each separately authorized and recorded. |
| Consequence (GC-6) | If the order is readable, the packet §3 row "Establish whether and when a block can end, using D4/D5 (A-1)" can use this read for requests whose id was learned (BE-4). If it is not, cross-session recovery stays unestablished and unresolved attempts stay held (§6.4). Neither result releases a reservation or permits a resend. |
| OPEN | The REST return does not settle which identifier the read accepts: the broker order id learned in session, or the caller's tracking id, which CrossTrade remembers for seven days and forwards as `clOrdId` (Q05). R-2 uses the id the operator retained and records which one it was. If the read accepts the caller's id, R-2 would also bear on lost-response requests; that is not assumed. |

## Part 2 — Order-producing rows (NOT recommended for authorization until this plan is reviewed)

### 2.0 Rules common to X-1 … X-5

Each row supplies the CAP procedure's fields, either in its own table (action/scope, expected identity, stated result, stop/intervention) or through the common rules below (account/environment, starting state, original capture, teardown, authority). Each row's expected result is fixed **before** action.

| Field | Rule |
|---|---|
| Evidence standard | Per packet §1, a row **validates** a mechanism that vendor semantics establish; it does not establish one. So X-2 waits for its documentary step M2 (§2.2) and X-3 for M (§2.5). Where the mechanism stays undocumented after that step (for example, whether the old stop survives a rejected modify, §6.4), a pass shows only that one attempt did not fail. |
| Environment | OPEN (§0.3); named in each authorization. |
| Instrument | One micro contract of the symbol of the leg the row serves: MYM for the Striker row (X-2), MNQ for ORB's resting entry (X-4). Rows serving all legs (X-1, X-3, X-5) use one micro symbol from the book; MYM keeps X-1 → X-3 on one position. Transfer to other symbols is an argument to accept, not an assumption. Aegis trades 6J, which is not a micro contract, so any Aegis-specific trace is a separate operator decision and is not proposed here. Front month, away from roll. |
| Exposure limit | One contract per request and in total. Every entry carries its protective stop in the same request (absolute `stopLoss`, Q02). The operator fixes, in the authorization, the maximum stop distance, the maximum time in market, the window and the cost ceiling. No figures appear here or come from private sources. No `atm*` fields, no `cancel_after`, no copier or multi-account routing (§6.2). |
| Window | Attended throughout. Not within 15 minutes of a scheduled high-impact release (session plan §2). |
| Starting state | Recorded as in session plan §2: flat, no working orders, no outstanding requests, and the §0.1 inventory complete. Otherwise stop. |
| Local timing | Record the local time immediately before each send. It is the `prepared_at` analogue used for the GC-3 postdating check. |
| Abort (all rows) | The session plan §2 stop rule, plus: any §6.3 `unknown` outcome (no retry, no resend); a protective stop not `Working` at quantity 1 within the operator-fixed wait after a fill; any position other than the one expected; the time-in-market limit reached. |
| Recovery (all rows) | 1. Stop sending REST requests. 2. **If any request's outcome is unknown** (for example an unknown `close`), the operator first reads positions, working orders and that request's lifecycle and status. A platform flatten happens only if these fresh reads show exposure that needs it. It is then a second close owner whose race with the in-flight request is unresolved: record it as such and carry it to the §2.5 fault cases and residual-risk statement (rail spec `CLOSE`: an unknown outcome is reconciled from postdating evidence before resubmission; halt/resume §1: no claim that manual action is race-free). **Otherwise**, the operator flattens and cancels working orders on the symbol through the trading platform (attended intervention, not a new REST request). 3. Confirm from fresh reads taken after the last action: positions flat, no working orders, and every id involved terminal by lifecycle or status. A flat snapshot alone is insufficient (CAP teardown; halt/resume §3). 4. Reconcile each request: it has terminal evidence, or it is retained as outstanding with a named owner. 5. Record the outcome. Run no further row that session. |
| Evidence (all rows) | Original bytes of every response and read, plus local send times, hashed into `MANIFEST.tsv` under `local_artifacts/route-drills-2026-09/drills/`. A trace qualifies only the behavior it observed (session plan §5). |

**Suggested sequence, once reviewed and authorized.**
- Before session A: M2 has returned (X-2 depends on it) and M has returned (X-3 depends on it).
- Session A: §0.1 inventory → X-1 → X-2 → X-3 → teardown reads → R-1 on X-1's and X-3's orders, before the reset. A row whose documentary step has not returned is skipped. If X-3 is skipped, session A ends with the §2.0 recovery, and X-3 later needs a fresh X-1 position.
- Session B, after the reset: R-2 on the same orders.
- X-4: in session A after teardown, or on its own.
- X-5: not scheduled (§2.5).

### 2.1 X-1 — One-contract REST OSO entry with its stop (GC-2a)

| Field | Content |
|---|---|
| Behavior | §A1: entry and bracket created in one REST call; the stop activates on the entry's first fill at quantity 1. |
| Actions, in order | 1. Assign a fresh `clOrdId`, never reused, and record it privately before sending. 2. Send one REST `orders/place`: a market entry for one contract with an absolute `stopLoss`. Include `takeProfit` too, so that X-3 exercises an OCO pair; if the operator omits it, X-3 tests a single stop child only. 3. Retain the response: the entry id and the child ids `oso1Id`/`oso2Id`/`osoChildIds` (Q02). 4. Poll status and lifecycle per id for the entry and children until the entry is `Filled` or `Rejected`. REST has no Alert History row, so the poll is the only way to see a late reject (Q09; Gate A A7). 5. After the fill, read the children's status and quantity, the fills by `orderId`, and the positions. |
| Expected identity | The fresh `clOrdId` → one REST `orders/place` → the entry order id and child ids (`oso1Id`/`oso2Id`/`osoChildIds`, Q02) → the entry's fill by `orderId` → the stop child `Working` at quantity 1, linked to the entry. |
| Pass | Lifecycle shows one `New` command carrying the `clOrdId`. The entry fills one contract. The children read `Suspended` before the fill, if that state is observed. On reads after the fill, the stop child is `Working` at quantity 1 and linked to the entry. The activation interval is measured from broker timestamps if the reads carry them (OPEN). |
| Fail | The stop child is not `Working` at quantity 1 within the wait, or it is `Rejected` or ended while the position is open. Any position other than one contract. |
| Abort | Stop not `Working` within the wait: run recovery at once. More than one `New` for the `clOrdId` (an identity conflict; a repeated `clOrdId` is accepted, Q05): testing ends and recovery runs. It is recorded as GC-6 correlation evidence, not as a GC-2a failure. |
| Consequence (packet GC-2a) | **Fail: ROUTE STOPS for all legs.** The one-contract premise fails (incident ADR §A6, falsifier 4). **Pass:** the REST-form trace that the §A1 admission precondition needs. Recording it in CAP is the coordinator's job. |
| Does NOT establish | The distribution or bound of the activation interval (UB-2). Behavior on other symbols. Late-reject handling, unless a late reject actually occurs. |

### 2.2 X-2 — Rejected modify leaves the old stop working (GC-2b, GC-3)

**M2 — L2(c) semantics step.** Documentary, like M (§2.5), because packet GC-2b's validation method is "Vendor semantics, then D2". Its return is a precondition of X-2.

| Field | Content |
|---|---|
| Questions | For CrossTrade `change` → Tradovate modify: (1) After a rejected modify of a working stop, does the original order stay `Working` at its original price? (2) A version can exist for a command Tradovate later rejects (Q21): what state does the order show in that interval, and after the rejection? (3) Is an accepted modify atomic, with the old stop effective until the new one is? (4) What does a modify with an unknown outcome leave working? |
| Sources, who, output | As M (§2.5): public documentation first, captured privately; any vendor question sent only by the operator; each question marked DOCUMENTED, CONFLICTING or OPEN; nothing inferred from silence. |

| Field | Content |
|---|---|
| Behavior | L2(c): after a rejected modify, the old stop is still `Working`, unchanged. |
| Precondition | M2 has returned. X-1 passed, and its position is open with the stop `Working`. X-2 validates what M2 documents; it does not establish the mechanism. |
| Expected identity | The `change` request → the X-1 stop child's order id → the command report (Q21) → the stop's lifecycle, status and version, unchanged. |
| Actions, in order | 1. Read the stop's lifecycle and status. 2. Record the local time. Send one REST `change` moving the working stop to a level on the wrong side of the market, a price the broker should refuse. 3. Retain the response and read the command report (Q21). 4. Read the stop's lifecycle and status again: state, price, and version if one is exposed. |
| Pass | The command report shows the rejection. On reads postdating the send, the stop is `Working` at its original price. |
| Fail | After the rejection the stop has ended or moved, or its state is unknown, or the position is unprotected. |
| Abort | If the modify is accepted and executes, the position closes: record that, run recovery and skip X-3 (session plan D2). If the `change` outcome is unknown, do not retry; run recovery. |
| Consequence (packet GC-2b) | **Fail: OPERATOR DECISION for Striker and Aegis.** The question returns with alternatives, none adopted automatically: a fixed-stop edition (with pre-registration and requalification), a different amend realization under a contract change, or excluding the leg. A cancel/replace cannot satisfy L2(c) (rail spec R-B3 L-2). ORB and Vanguard are unaffected only if their successor settings make every amend a noop (packet B-4, B-5). |
| Also records (GC-3) | Whether the command report and the lifecycle reads carry broker timestamps or versions that postdate the send. |
| Does NOT establish | Whether the old stop survives an **unknown** modify, as opposed to a rejected one. Atomicity of an accepted modify, where the old stop must stay effective until the new one is. Behavior under other rejection reasons. |

### 2.3 X-3 — Full close by broker liquidation (GC-1 C-a, first candidate to investigate; GC-3)

| Field | Content |
|---|---|
| Behavior | L2(d): a full close through REST `close` (Tradovate `liquidateposition`, §6.4) leaves the position flat and the OCO children terminal. The REST return records this as documented but not verified (§6.6, partial-fill row). |
| Preconditions | **Required:** M (§2.5) has returned, with each question marked DOCUMENTED, CONFLICTING or OPEN, so the reads can check the documented order of cancel and flatten. X-3 validates the mechanism M documents; it does not establish it. X-1's position is open, with both children `Working` far from the market; this row is not a race test. |
| Expected identity | The `close` request → the liquidation order, identified from session orders → the X-1 children's ids → fills (the liquidation fill; no protective fill). Whether the `close` response carries an order id is OPEN. |
| Actions, in order | 1. Read positions, working orders, and both children's status. 2. Record the local time. Send one REST `close` for the symbol. 3. Retain the response. 4. Read positions, working orders, lifecycle and status per id for both children, the session orders (to identify the liquidation order), and fills, including any protective fill. What fields the `close` response carries is not described in the REST return (OPEN). |
| Pass | On reads postdating the send: position zero; both children terminal (`Cancelled`); no `Working` remainder on the symbol; no protective fill; and the liquidation order, identified from session orders, terminal. The reads are shown to describe one coherent state, or else the coherence limit is recorded as OPEN (GC-3) and qualifies the pass. |
| Fail | A child is `Working` after flat (an orphan). The position has reversed. |
| Fault outcome | The close is rejected with the position open, or its outcome is unknown. This is neither a pass nor, by itself, a route stop: run abort and recovery, and record it as fault-case evidence for §1.1a (b) and (e). Its consequence is decided under the packet's §1.1 failure rule and B-1, not asserted here. A partly completed close is not reachable at one contract. |
| Abort | Orphan: the operator cancels it through the platform, then recovery. Reversal: recovery at once. Rejected with the position open: no retry; recovery. Unknown outcome: no retry; recovery's unknown-outcome branch (§2.0 step 2: read first; flatten only if fresh reads show exposure; record any flatten as a second close owner). |
| Consequence (packet §1.1) | **Fail (orphan or reversal): ROUTE STOPS for all four legs**, as the packet's failure consequence states for traces that show residual orders or reversal. A residual-risk statement goes to the operator, who may choose: C-b as a separately decided expression change; a different close contract; or rejecting the route. None is automatic. **Pass:** one no-race observation of cancel-and-flatten, validating what M documents. It bears mainly on §1.1a element (d), and on (a) for the end state only (the interval itself is unobserved unless the reads carry timestamps). It settles nothing on (b), (c) or (e), and it is not evidence against reversal. |

### 2.4 X-4 — Cancel of a resting stop entry ends its Suspended children (GC-4)

| Field | Content |
|---|---|
| Behavior | Cancelling a resting stop entry before any fill ends its Suspended GTC children (REST return D6). |
| Instrument | One MNQ micro contract (ORB's leg). |
| Expected identity | The fresh `clOrdId` → one REST `orders/place` → the resting entry's order id and child ids (Q02) → the `cancel` request → the parent and both children terminal; no fill. |
| Actions, in order | 1. Assign a fresh `clOrdId`. 2. Send one REST `orders/place` for a resting buy stop entry above the market, at an operator-fixed distance chosen so it will not trigger during the row, with `stopLoss` and `takeProfit`. The REST return does not name the order-type fields, and none are specified here. 3. Read: the entry `Working`, the children `Suspended`. 4. Send one REST `cancel` of the parent. 5. Read the lifecycle and status of the parent and both children, the positions and the fills. |
| Pass | On reads after the cancel: parent `Cancelled`, both children terminal, no fill, nothing `Working` or `Suspended` left. |
| Fail | A child stays `Suspended` or `Working` after the parent is terminal. |
| Abort | If the market comes within an operator-fixed buffer of the entry level, cancel at once. If the entry fills anyway, handle the position as in X-1 (confirm the stop is `Working`), then run recovery. |
| Consequence (packet GC-4) | **Fail: OPERATOR DECISION for ORB.** The alternatives are: an attended session-end procedure; a different end-of-life rule, which is an edition change (packet B-13); or a cleanup read that closes the orphans before the next session. Not route-wide. |
| Related, not decided here | X-4 observes the broker's behavior on cancel only. It does not choose ORB's resting-entry lifecycle (packet B-13). Its reads can serve as example order-level evidence for fence states (i) and (iv) in the packet §3 four-state trace, but that repair is a source-to-consumer trace, not a drill. |
| Not covered | The expiry variant ("cancelled or expired", D6) requires the entry to rest until it expires, which lengthens exposure. It needs a separate authorization if wanted. |

### 2.5 GC-1 (D19) close: corrections, proposed amendment, mechanism step and X-5

**Executive-review corrections to the GC-1 framing.** These are recommended (executive review 2026-09-26); the operator ruling is pending. Their owner is the packet's 2026-09-26 revision (§1, §1.1, §1.1a, B-1). This table mirrors them only to show how they shape this plan; where the two differ, the packet governs.

| # | Correction | Effect on this plan |
|---|---|---|
| 1 | C-a (whole-leg broker liquidation) is only the **first candidate to investigate**. No close guarantee is accepted. | X-3 and M investigate C-a. A pass qualifies nothing beyond what it observed. |
| 2 | The earlier §1.1a "interpretation" is **withdrawn**, including its sentence that no residual protection is required once the intent is to be flat. The packet's §1.1a now carries a proposed explicit amendment to the close contract in its place, with elements (a)–(e). | This plan relies on no interpretation of L2(e). It gathers evidence for each amendment element (table below). |
| 3 | Evidence standard: a single successful race observation cannot show that reversal cannot occur. The mechanism comes first, from authoritative vendor semantics; traces and fault cases then validate it. If the guarantee remains unavailable, the output is a precise residual-risk statement returned to the operator for decision. | M returns before X-3 and X-5 (M2 before X-2). X-3 validates what M documents. X-5 is optional and never closes the question. |
| 4 | C-b (exit through the lot's own OCO) is an **unapproved alternative** that needs its own operator expression decision. It is not an automatic fallback. | No C-b drill is planned here. |
| 5 | Exclusivity (GC-7) prohibits uncoordinated actors but must accommodate the attended operator-intervention procedure, with automation fenced and reconciliation required afterwards. | §0.1 |

**Evidence this plan gathers for the proposed close amendment.** The amendment and its OPEN items belong to the packet's [§1.1a](2026-09-26-tradeify-bd-decision-packet.md) (the rail spec's R-B3 L-2 (d)/(e), `CLOSE(scope)`, S5 and I7; decided under B-1). This plan neither restates nor adopts them. It maps each element to the evidence the plan gathers and to what stays OPEN after it. No vendor semantics are assumed.

| §1.1a element | Current contract it would amend (rail spec, as read) | Evidence this plan gathers | Still OPEN after this plan |
|---|---|---|---|
| **(a)** Protection during the liquidation interval | S5: protection stays effective for any unclosed remainder and is removed only when the scope is flat | M questions 1–2. X-3 reads, which show only the end state unless the reads carry timestamps | The interval's length and bound, unless vendor semantics state them. One trace does not measure a bound. |
| **(b)** Failed, rejected or partly completed liquidation | `CLOSE`: a rejection keeps the existing protection; a partial outcome resumes the same operation for the remainder; an unknown outcome is reconciled before resubmission | M questions 4–6. Most fault cases cannot be traced live (table below) | Any outcome that neither M documents nor an offline test covers |
| **(c)** Protective-fill races and reverse exposure | `CLOSE`: "cannot over-execute into a reverse position"; L-2 (e): "without reverse exposure" | M questions 3 and 7–8, then optionally X-5 | Absence of reversal. **No observation settles it** (correction 3). Without a documented mechanism, the output is the residual-risk statement. |
| **(d)** Observations that establish completion | `CLOSE`/S5: `P` and `W` evidence postdating `prepared_at`, never HTTP acceptance | X-3's reads; X-2's GC-3 record of timestamps and versions | Account-wide coherence across separate calls (CAP R4; GC-3) |
| **(e)** Incident handling while completion is uncertain | `CLOSE`'s `unknown_order` block; halt/resume §2 row 1 and §3 | None by drill. No lost response is manufactured (not proposed in CAP; excluded by session plan §0 and checklist T09). Offline consumer tests only | The deadline after which "unconfirmed" becomes "uncertain", and the operator's T13 platform procedure |

**M — mechanism step.** Documentary. Its return, with each question marked DOCUMENTED, CONFLICTING or OPEN, is a **required** precondition of X-3 and X-5 (packet §1 evidence standard; C-a evidence row: vendor semantics, then traces). X-3 and X-5 validate what M documents; they do not establish it. The packet notes that vendor-semantics work for GC-1 needs no drill and can start now.

| Field | Content |
|---|---|
| Questions | For CrossTrade `close` → Tradovate `liquidateposition`: (1) Are working orders cancelled before the flattening order is sent? What order type is the flattening order? (2) Does any protection survive between cancellation and flat? (3) Is the flattening quantity fixed at request time, or taken from the live position at execution? (4) Is liquidation all-or-nothing? Are cancellations rolled back if it fails? (5) Can a partial flatten occur? (6) Is a failure reported synchronously or only later? (7) Can a protective fill land between the cancel and the flatten, and can both execute? If liquidation is internally a cancel followed by a market order, the C-c race exists inside C-a (packet §1.1a (c)). (8) What does liquidating an already flat position do? (9) Does coverage repair (Q15) or any other vendor watcher act after a liquidation? |
| Sources | Public Tradovate and CrossTrade documentation first, each captured with URL, time and SHA-256 into private evidence. Then a vendor question drafted by the coordinator and **sent only by the operator**. Original reply bytes are retained; a transcription does not suffice (Gate A A12). |
| Who | A documentary executor under a coordinator dispatch, with no account access. Vendor contact is the operator's alone. |
| Output | Each question is marked DOCUMENTED (bound to a source), CONFLICTING or OPEN. Nothing is inferred from silence. |
| Then | Whatever the answers: design the fault cases below for (a), (b) and (e), and X-3 becomes eligible for authorization. Only X-5 depends on questions 3 and 7: it is considered, on the operator's explicit decision, only if they document a no-reversal mechanism; if they do not, the (c) outcome is the residual-risk statement. The residual-risk statement below is returned whenever any question bearing on elements (a)–(c) stays OPEN or CONFLICTING, not only questions 3 and 7. Any observation stays optional and cannot close the question. |

**Fault cases to design.** The packet's C-a evidence row asks for REST-form traces of fault cases: rejection, partial, unknown outcome and the race. **Most cannot be traced live under this plan's limits:**
- a partial liquidation is impossible at one contract;
- a lost response is not manufactured (not proposed in CAP; excluded by session plan §0 and checklist T09);
- no safe way to induce a broker rejection is known.

They are designed as M checks plus offline consumer tests, and observed live only if they occur naturally. Whether that suffices is the operator's call (open question 8).

| Fault case | Live provocation? | How it is validated | Amendment clause |
|---|---|---|---|
| Liquidation rejected with the position open | No known safe trigger (OPEN) | M plus an offline consumer test | (b), (e) |
| Liquidation partly filled | Impossible at one contract; applies to multi-lot legs | M plus an offline test | (b) |
| Liquidation accepted but delayed | No | M plus an offline test | (a), (e) |
| Lost response to `close` | Not proposed (CAP); excluded by session plan §0 and checklist T09 | Offline test | (e) |
| Unknown `close` outcome followed by an attended platform flatten | Not provoked; arises only after a natural unknown outcome (§2.0 recovery step 2) | M (questions 3 and 8) plus an offline test; any such flatten is recorded as a second close owner whose race is unresolved | (c), (e) |
| Protective fill lands before the liquidation (liquidating a flat position) | May occur naturally in X-5 | M, then observation if it occurs | (c), (d) |
| Protective fill overlaps the liquidation | X-5's target; one observation cannot close it | M, then X-5 | (c) |
| OCO cancel fails while the flatten executes (orphan stop) | No | M; X-3's reads detect it if it occurs | (a), (c) |
| Coverage repair re-places protection after the liquidation | No | M (Q15) | (c), (d) |

**Residual-risk statement.** It is returned to the operator whenever the guarantee is unavailable: that is, whenever any M question bearing on elements (a)–(c) stays OPEN or CONFLICTING, or an item under (d) or (e) stays OPEN after this plan. It is not limited to reversal. Its figures bind at T16, like §A3, and are not written here.

| Field | Content |
|---|---|
| Mechanism status | Each M question: DOCUMENTED, CONFLICTING or OPEN, with sources. |
| Observations | The count and conditions of X-3 and X-5 traces and of any fault case that occurred naturally. A statement that none proves absence. |
| Per element | The table below, filled from M. Each worst outcome there is an inference conditional on the M questions named, not a vendor fact. |
| Affected exits | Every whole-leg exit on all four legs, plus Striker's close-time crossed-level exit when realized as a whole-leg close (packet B-7). |
| Choices returned to the operator | None is automatic (packet §1.1): accept the residual under named conditions in the amendment (B-1); C-b as a separately decided expression change; a different close contract; or reject the route. |

| Element | Worst credible outcome (conditional inference) | Detection | What bounds it |
|---|---|---|---|
| **(a)** Liquidation interval | If working orders are cancelled before the flatten executes (M questions 1–2 OPEN): the whole position open with no protective order until the flatten fills. | Only reads carrying broker timestamps show the interval (GC-3; OPEN). End-state reads do not. | Nothing documented. The interval's length and bound are OPEN. |
| **(b)** Rejected, failed or partial liquidation | If cancellations are not rolled back on failure (M questions 4 and 6 OPEN): an unprotected open position after a rejected or failed liquidation. For multi-lot legs, an unprotected partly flattened remainder (M question 5 OPEN). | Position and working-order reads postdating the send; a late failure needs polling (Gate A A7; GC-8). | Attended detection plus response (halt/resume §2 row 1, protection fault), unmeasured until T13. |
| **(c)** Protective-fill race | If the flatten quantity is fixed at request time and a protective fill can land in between (M questions 3 and 7 OPEN): a reversed, unprotected position, up to the whole-leg quantity (one contract in any drill). The size is a field M fills, not a vendor fact stated here. | Post-close position reads showing a non-zero opposite position, subject to the (d) coherence limit. | Attended detection plus response, unmeasured until T13. Incident ADR §A6 falsifier 5 requires this measurement for a failed stop activation; the same T13 measurement is needed here by analogy, not under that falsifier. |
| **(d)** Completion observations | If reads cannot be shown coherent (GC-3 OPEN): a close taken as complete while a residual order or position exists. | Re-reads only; coherence is itself the open item. | No completion without postdating, coherent evidence (packet §1.1a (d)); until then the close stays unresolved and blocking. |
| **(e)** Uncertain completion | An unresolved close that keeps its blocks indefinitely, with any remaining exposure unprotected or unknown until attended recovery completes. | The halt/resume §2 row 1 incident (uncertain order outcome). | The operator's attended response and the T13 procedure. The deadline after which "unconfirmed" becomes "uncertain" is OPEN. |

**X-5 — Protective-fill race observation.** Only after M returns and the operator makes an explicit decision.

**Warning:** deliberately liquidating near a working protective order carries **real reversal risk**. The result can be a position opposite to the intended one, with no protective order. This needs the operator's explicit decision on environment (§0.3) and limits, beyond an ordinary drill authorization.

| Field | Content |
|---|---|
| Behavior | Whether a liquidation sent while the protective stop is likely to fill leaves a reversed position. |
| Expected identity | As X-1 for the opening position; then the `close` request → the liquidation order, identified from session orders → the children's ids → fills, including any protective fill. |
| Actions, in order | 1. Open a position as in X-1, with the stop at an operator-fixed distance close to the market. 2. When the market reaches an operator-fixed trigger zone, record the local time and send one REST `close`. 3. Read everything: positions, working orders, children, fills, with broker timestamps where available. |
| Exposure limit | One contract. A reversal leaves up to one contract opposite and unprotected. The operator stays at the platform, ready to flatten, throughout. After an unknown `close` outcome, recovery's unknown-outcome branch applies (§2.0 step 2): read first, flatten only if fresh reads show exposure, and record any flatten as a second close owner whose race is unresolved. |
| Pass | **None.** A no-reversal result is recorded as consistent with a no-reversal mechanism, not as proof. Human timing cannot reliably place the send inside the in-flight window. Whether the overlap occurred can be shown only from broker timestamps, if the reads carry them (OPEN). |
| Fail | A reversed position observed. This is decisive against C-a's reversal clause. |
| Consequence (packet §1.1) | Fail: ROUTE STOPS for all four legs. The residual-risk statement goes to the operator, whose choices are those listed above; none is automatic. |

## Authorization requested

| Item | Kind | Proposed for authorization now? | Waits for |
|---|---|---|---|
| **R-1** same-session recipe | Read-only REST | **Yes** | Its preconditions: a known order (Part 1 definition) in the same session; §0.2 access. It can run only after webhook D1 (open question 2), an authorized X-1, or another qualifying operator-placed order |
| **R-2** prior-session lookup | Read-only REST | **Yes** | A known order (Part 1 definition); one reset since |
| §0.1 actor inventory (GC-7) | Operator inventory; places no order | Requested from the operator (owed as CAP R5) | — |
| M and M2 mechanism steps | Documentary; vendor contact by the operator only | Not an account action; needs a coordinator dispatch | — |
| X-1, X-2, X-3, X-4 | Order-producing | **No** | Review of this plan; §0.2 P-1; §0.3 environment decision; the §0.1 inventory; a written authorization per row. X-2 also requires M2's return, and X-3 requires M's return (§2.2, §2.5). |
| X-5 | Order-producing, with a deliberate hazard | **No** | M; the packet §1.1a amendment outline; an explicit operator decision on environment and limits |
| C-b drills | — | Not planned | An operator expression decision (correction 4) |

## Open questions for the operator

1. **Environment:** does a demo or simulation environment exist with the same route semantics (§0.3)?
2. **Webhook-form drills:** the session plan's D1–D4 remain authorized in principle as recorded on 2026-09-25, and this file does not change that. Do they run before this plan is reviewed, given the executive review's recommended direction (operator ruling pending)?
3. **R-2 identifier:** which identifier does the lifecycle read accept, the broker order id or the caller's tracking id (Q05)?
4. **R-1 on a non-REST order:** which `clOrdId`, if any, does a webhook- or platform-placed order carry? Does the Part 1 "known order" definition, which admits an operator-placed order such as the weekly account-preservation trade, stand?
5. **GC-3 reads:** do lifecycle, status and command-report reads carry broker timestamps or versions?
6. **Drill costs:** do they count against the rail spend ceiling (session plan §2)?
7. **Aegis:** is a 6J-specific trace wanted at all (§2.0)?
8. **GC-1 fault cases:** most cannot be traced live under this plan's limits (§2.5). Do M checks plus offline consumer tests suffice? The alternative, a multi-contract design, would exceed this plan's one-contract limit and need its own review.
9. **Weekly account-preservation trade:** is it handled with automation fenced and reconciliation afterwards, or moved to a symbol outside the four (§0.1; packet GC-7)?

## Owners and propagation

- **Owners.** The executive-review corrections (§2.5) belong to the packet's 2026-09-26 revision (§1, §1.1, §1.1a, B-1, A-1). This file creates no second owner. If the packet revision is not committed as drafted, the corrections in §2.5 remain owed there.
- **When traces exist.** The coordinator records outcomes in CAP (R2–R5, N1) and T08 §7, as session plan §5 describes. The drill-map rows in REST §6.11 bind by behavior, so each outcome is recorded against its behavior row with its interface.
