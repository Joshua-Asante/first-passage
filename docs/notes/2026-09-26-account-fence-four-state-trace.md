# Account fence: four-state correctness trace (2026-09-26)

**Status:** RETURNED for coordinator review. Deliverable 2 of the [ORB lifecycle and fence-trace card](../briefs/handoffs/2026-09-26-orb-lifecycle-and-fence-trace.md), answering the "resting-order fence" row of the [B–D packet §3](2026-09-26-tradeify-bd-decision-packet.md#3-unknown-request-posture-and-option-b-rules). That row's four-state table was marked "as read, not traced"; this note traces it and confirms or corrects it. The fence is treated as a **required correctness repair, not a policy choice** (operator ruling 2026-09-26). This note changes no code, contract or owner record, and accepts, authorizes or qualifies nothing. The repair in §6 is a proposal.
**Executor:** assessor subagent (Claude Code, Opus 5.5), branch `claude/orb-fence-trace`. **Dispatch revision:** `62c956f538dfa53f31eaec5951efc3ffa1dce53b` (HEAD equals it; verified). Line numbers are at that revision. File names without a directory refer to `ops/c1_rail/book_account_owner.py`.
**Separation:** nothing here relies on the ORB lifecycle ruling ([Deliverable 1](2026-09-26-orb-lifecycle-evidence.md)). Where the repair depends on that ruling, §6.6 says so and leaves it open.

## Answer in brief

1. **The production fence cannot tell a working order from a stale one.** Its only resolving input is an accepted terminal (fill, cancel or reject). The owner has no way to learn that an entry or add is still working. So once one bar has passed since the order was prepared, it treats a **known working order with fresh evidence (i)** exactly like an order whose **evidence has gone stale (ii)**. Both refuse every leg's risk-adds and loosening amends (`:793-797`, `:1608`, `book_protection_owner.py:492`).
2. **The spec's own wording is ambiguous for (i), but every other row points one way.** The §1 `pending` row, read literally, agrees with the code. The S1 cut, the `W` freshness row, E3, AC-3, AC-5, AC-8, the §5 cutoff rule and the incident ADR's UB-7 direction all read an order that fresh order-level evidence shows working as **not unknown** (§2). Under that reading the code has a defect in state (i) for admission, loosening amends and takeover.
3. **Takeover over-blocks further.** It has a second, stricter check (`book_takeover_owner.py:621`) that treats any entry or add not yet terminal, on any leg, as "not quiescent" from the moment it is sent. S10 requires quiescence only of the displaced legs.
4. **Genuinely unknown outcomes (iii) are fenced correctly, but not halted.** They are counted at once and cleared only by an accepted, postdating terminal. That is the conservative reading and is consistent with Gate A A1. Rev9 also requires a halt into INTERVENTION for an "uncertain transport/order outcome". The owner raises that halt for protection and takeover-child unknowns, but not for ordinary entries, adds, closes or cancels. This gap is already recorded (packet CC-3: the risk-add fence "is the part implemented today").
5. **Terminal orders (iv) resolve correctly.** One caveat: the transport-`REJECTED` shortcut (`:791-792`) is safe for the synthetic seam only. Gate A A3 constrains it for any real route.
6. **Close, cancel, recovery, the resume gate and capacity do not read the fence.** Their behavior is correct in all four states, or fail-closed where not built, with one spec ambiguity. A close is refused while its own leg holds any unresolved entry or add (`:1296-1301`), whatever that order's state.
7. **The repair needs a producer that does not exist yet.** Classifying state (i) needs fresh, request-correlated, order-level evidence. The accepted production producer is T09, which is **not built**. Only a synthetic inventory reader, used by takeover and bootstrap, exists today.

## 1. The four states, and what the owner can see

| State | Definition used in this trace | What the owner records | How `_ordinary_unknown_orders_db` (`:768-798`) classifies it |
|---|---|---|---|
| (i) Known working, fresh evidence | Transport accepted the request. The latest complete order-level acquisition for its symbol postdates preparation, is at most one bar old and shows the order working (or partially filled with a remainder) under its own identity | Attempt `ACCEPTED` (`:1700-1702`); operation `attempted` (`:1676`). No evidence field exists: broker facts are only `fill` and `terminal` (`:150-176`), and any other fact kind halts (`:2055-2057`) | Not counted for one bar after preparation (`:793`). Counted from then on, with the boundary inclusive, until an accepted terminal that postdates preparation (`:795-797`) |
| (ii) Evidence gone stale | As (i), but no qualifying acquisition within the last bar (including an order never evidenced at all) | Same as (i) | Same as (i). The clock runs from preparation (`created_at`, `:790`), not from the last evidence |
| (iii) Unknown dispatch outcome | The attempt outcome is unknown: a transport exception, no response, or a crash between the attempt journal and the outcome record | Attempt written `UNKNOWN` before send (`:1674-1677`) and left `UNKNOWN` on an exception (`:1685-1688`) or an unknown result (`:1700-1702`) | Counted at once, with no grace (`:793`), until an accepted terminal postdating preparation (`:795`) |
| (iv) Terminal | A fill-complete, cancelled or rejected terminal, accepted by the capacity reducer (`book_capacity.py:212-224`) | The terminal fact is journaled with the same `as_of` as its capacity event (`:778-786`); operation `terminal` (`:2047`) | Resolved if the terminal strictly postdates preparation (`:795`). A transport-`REJECTED` attempt is skipped outright (`:791-792`) |

The fence scans **entries and adds only** (`:787-789`). Close orders are gated separately (§3.8).

**Two further observations:**

- **A never-sent request is classified as unknown.** With no transport configured, the attempt is journaled `UNKNOWN` and the method returns `production_route_unavailable` without sending (`:1682-1684`). The request is demonstrably unsent (Gate A A3 (i)) but is classified (iii). This fails closed and is reachable only without a route, but T09 must not inherit it (§6.7).
- **The boundary differs from the kernel.** The code counts an accepted order at exactly one bar after preparation (`now < prepared + BAR_PERIOD` is false at equality). The test reference kernel times out strictly after one bar (`tests/ops/tb_s3_kernel/kernel.py:1326`). The spec says "within one bar" and "older than one bar". Minor; §6.3 asks for it to be pinned.

## 2. Settling the spec reading of state (i)

**The spec text is ambiguous.** Rows that support the literal reading, under which (i) becomes unknown after one bar:
- §1 `pending` row (rail spec `:27`): "`UNKNOWN` after the one-bar outcome timeout or a crash between send and outcome". It lists resolution only by a terminal event, or by a postdating `W` absence plus a consistent `P`. A `W` showing the order working is not listed, and the state list has no "working" value.
- Consistency matrix (`:78`): "`pending = UNKNOWN`" → "refuse (account-wide, `unknown_order`)".

Rows that support reading (i) as **not unknown**:
- **S1 cut** (`:54`): "no evidence within one bar → `pending=UNKNOWN` … until order-level postdating evidence … resolves it". The trigger is the *absence of evidence*, not the order's age.
- **`W` row** (`:26`): a working-order snapshot is `CONFIRMED` until it is older than one bar. So a fresh snapshot that lists the order is confirmed evidence of it.
- **S2** (`:56`): the entry "rests" while "`W[MNQ]` gains the order on evidence", and the reservation is held "while it rests". Resting is treated as a normal state.
- **E3** (`:111`): "Completion hands responsibility to observed working orders, gross lots or quarantine before releasing the request owner". An observed working order discharges the request.
- **AC-5** (`:94`): the unknown case is qualified: "accepted, **no evidence** for one bar".
- **AC-3, AC-8, §5**: AC-3 (`:92`) has a resting add live until the next session open. AC-8 (`:97`) has an ORB entry filling at the cutoff. Halt/resume §5 (`:67`) cancels "resting risk-add orders" at the cutoff. Each assumes orders that rest for many bars under RUNNING without an incident.
- **Incident ADR UB-7 direction** (`docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md:302`, EVIDENCE-PENDING): "a correlated working entry becomes a known working-order reservation".
- **The test reference kernel** implements this reading, though it is an unaccepted reference (rail spec `:103`). It refreshes `last_evidence_at` on each order-level read that mentions the order (`kernel.py:562-563`), times out only from the last evidence (`:1319-1329`), and returns an unknown order to `accepted` when `W` shows it working (`:577-578`, `:1095-1112`).

**Settled reading (proposed clarification; the rail-spec owner must adopt it; not applied here).** A request whose latest qualifying order-level evidence (§4) is at most one bar old and shows it working or partially filled is a **known working order**, not `UNKNOWN`. It keeps its reservation. It is subject to cancellation at the cutoff and on mode or takeover transitions. It counts as a working order for recovery and deadline checks. It does **not** create an `unknown_order` block. The one-bar outcome timeout runs from the latest such evidence, not from the send.

**Verdict for (i):** *spec-ambiguous on its face; the code is a defect under the settled reading.* The `pending` row needs a sentence to remove the ambiguity (§6.1).

## 3. Four-state × consumer matrix

Consumers 3.1 to 3.5 are the ones the card names. Consumers 3.6 to 3.8 were found by the trace. Each consumer has a table with one row per state: the code's behavior today, the spec's behavior, a verdict and the tests that cover it.

### 3.1 Admission (entry and add; rail S1 (5) `:54`; consistency matrix `:78`; I1/I6 `:50`)

| State | Code today | Spec | Verdict | Tests |
|---|---|---|---|---|
| (i) | Not counted for one bar (`:793`). From then on every leg's risk-add is refused `unknown_order` (`:1608-1609`) until the order is terminal | Settled reading (§2): no block; admission proceeds, with the reservation counted in capacity | **Spec-ambiguous; defect under the settled reading** | Production: none (there is no working-evidence input). `test_pr409_review4.py:51-66` (`accepted-901`) and `:69-88` pin refusal for an accepted order **with no evidence**. Kernel reference only: `tests/ops/tb_s3_cases/primitives/test_tb_s3_kernel_review.py:56-66` |
| (ii) | As (i): refused from one bar after preparation; cleared only by a terminal | `W` older than one bar → `UNKNOWN` (`:26`); S1 cut → `unknown_order` (`:54`); refuse (`:78`) | **Correct.** The clock starts at preparation, never later than the spec's. Clearing when fresh working evidence returns is spec-ambiguous (E3 `:111` yes; `pending` row `:27` silent) and impossible in code | `test_pr409_review4.py:51-66`, `:69-88`, `:127-140`; `test_book_feedback_journal.py:42-55` (`accepted`). Clearing by fresh evidence: kernel only (`test_tb_s3_kernel_review.py:40-53`) |
| (iii) | Refused at once (`:793`, `:1608`) until an accepted, postdating terminal (`:795`). No halt | Rail: `UNKNOWN`, reservation held, account-wide `unknown_order` (`:27`, `:54`). Rev9: "uncertain transport/order outcome" → durable halt into INTERVENTION (halt/resume `:26`; rev9 replaces the incident portions, rail spec `:3`). Resolution by a terminal; the absence path (`:27`, AC-5) does not apply on this route, because absence proves nothing (Gate A A1) | **Classification correct. Consequence incomplete:** no halt is a defect against rev9 §2, already recorded as not implemented (packet CC-3) | `test_pr409_review4.py:51-66` (`unknown-1`), `:91-101`; `test_book_feedback_journal.py:42-69`. Halt on an ordinary unknown: none |
| (iv) | Resolved (`:795`); a transport-`REJECTED` attempt is skipped (`:791-792`) | Resolved by the terminal event (`:27`), strictly postdating (`:41`). Gate A A3: only a local pre-dispatch refusal is demonstrably unsent; a remote refusal keeps its uncertainty without request-specific closure | **Correct** for fill and cancel terminals. The `REJECTED` skip is correct for the synthetic seam; for a real route it is constrained by A3 and owed to the T09 outcome classifier | `test_book_close_reconciliation.py:24-37`; `test_book_feedback_journal.py:42-69`; `test_pr409_review4.py:51-88`, `:127-140`; `REJECTED`: `test_pr409_review2.py:236-252` |

### 3.2 Protection amend and attach (rail S3 `:58`; AMEND/ATTACH `:47-48`; action classes `:39`; consistency matrix `:80`)

Tightening amends and first attaches are never gated by the fence. They are checked only for intervention, scheduled authority and the settlement binding (`book_protection_owner.py:475-483`). A **loosening** amend (`:595`) is refused if the fence is non-empty (`:492`), or if any non-terminal operation has an `UNKNOWN` attempt (`:493-494`).

| State | Code today | Spec | Verdict | Tests |
|---|---|---|---|---|
| (i) | Tightening and attach proceed. Loosening is refused after one bar (`:492`) | Tightening and attach are risk-reducing and admitted under blocks (`:39`, I1 `:50`). Loosening is refused only under a block; under the settled reading there is none | Tightening and attach **correct**. Loosening **spec-ambiguous; defect under the settled reading** | None for fence states. `test_book_protection_evidence.py:143-182` covers binding, window, intervention and capacity gaps. Kernel: `test_tb_s3_kernel_findings.py:244-255` (an EOD block, not `unknown_order`) |
| (ii) | Loosening refused; tightening and attach proceed | Same | **Correct** | None |
| (iii) | Loosening refused at once (`:492`, `:493-494`). Tightening and attach are still sent, because no halt is raised | Rail: as the code. Rev9: the halt puts the account in INTERVENTION, which permits no runtime mutation, including tightening (halt/resume `:16`, `:41`) | Loosening **correct**. Tightening and attach follow from the missing halt (the same defect as 3.1 (iii)) | None |
| (iv) | Not refused | Not refused | **Correct** | Covered indirectly by the amend tests |

### 3.3 Close (rail S5 `:62`; CLOSE `:46`; consistency matrix `:79`; K1 `:112`) and cancel (S4 `:60`)

The close path does not read the fence. `_reserve_close` refuses a close for a leg that holds any reservation, that is, any non-terminal entry or add on the same leg (`entry_remainder_pending`, `:1296-1301`). Other legs' closes are unaffected.

| State | Code today | Spec | Verdict | Tests |
|---|---|---|---|---|
| (i)–(iii), same leg | Close refused until the order is terminal. The reason is the reservation, so it is identical in all three states | Exits and flats are risk-reducing and "admitted under every block" (`:62`). For `pending = UNKNOWN`: "admit; reconcile the overlapping operation before resending" (`:79`). But the schedule (§5), takeover (S10 `:72`) and K1 ("A fill exit owns its originating entry remainder") all order cancellation to a terminal state before the close | **Spec-ambiguous.** It is not a fence-classification question, so it stays out of the fence repair (§6.7) | `test_pr409_related_cases.py:21-45`, `:88-105` |
| (i)–(iii), other legs | Not refused | Admitted | **Correct** | `test_pr409_related_cases.py:107-119` |
| (iv) | Not refused | Admitted | **Correct** | `test_pr409_related_cases.py:78-86` |
| Cancel (i), (ii) | Sent when the target is a non-terminal entry or add (`:1573-1584`); not fenced | Risk-reducing; send; the acknowledgement releases the reservation (`:60`) | **Correct** | `test_pr409_owner_lifecycle.py:92-107` (invalid targets); scheduled cancel `test_book_account_owner.py:296-308` |
| Cancel (iii) | Sent | S4: "the cancel is still sent" (`:60`). Rev9: after the halt, INTERVENTION fences it and recovery is attended (halt/resume `:41`) | **Correct under S4.** Under rev9 it follows from the missing halt | None specific |
| Cancel (iv) | Refused `invalid_cancel_target` (`:1584`) | Nothing to cancel | **Correct** | `test_pr409_owner_lifecycle.py:92-107` (`terminal`) |

### 3.4 Recovery (halt/resume §3 `:41-45`; own-flat deadline §5 `:67`)

The owner has no incident-recovery completion check. INTERVENTION stops runtime mutations (`:1544-1545`, `:1257-1258`, `:1743-1744`; `book_protection_owner.py:477-478`). The only completion check is at the scheduled own-flat deadline (`:1789-1797`). It halts if any attempt row is unresolved (`:760-766`: an `UNKNOWN` attempt on a non-terminal operation, or an operation still `reserved`, `attempted`, `takeover_pending` or `awaiting_protection`) or if any leg holds confirmed or reserved capacity.

| State | Code today | Spec | Verdict | Tests |
|---|---|---|---|---|
| (i) | Counted (operation `attempted`, reservation held) → deadline breach | At D "any exposure, working order or unconfirmed state is a deadline breach" (`:67`); recovery needs "no working orders" (`:43`) | **Correct** | `test_book_account_owner.py:296-308` |
| (ii) | Counted → breach | Same | **Correct** | as (i) |
| (iii) | Counted → breach | Same; also "no unresolved requests" (`:43`) | **Correct** | `test_book_account_owner.py:200-213`; `test_pr409_review4.py:103-111` |
| (iv) | Not counted (operation `terminal`, `:2047`; reservation released) | Recovery is complete only on fresh coherent E1–E3/K1 evidence (`:43`) | **Correct as far as it goes.** The owner decides from its own accounting, not from a fresh coherent acquisition; that producer is T09 (not built) | Indirect only |

### 3.5 Resume gate (halt/resume §4 `:57-59`)

There is no resume path in the code. The only HALTED→RUNNING transition is the one-use bootstrap activation (`book_bootstrap.py:106-175`, `:174`). It refuses when any history table is non-empty (`:136-140`), so an owner that has ever prepared an order cannot run again. `book_halt.py:1-5` is halt-only.

| State | Code today | Spec | Verdict | Tests |
|---|---|---|---|---|
| (i)–(iii) | No resume | No resume while any working order or unresolved request exists (`:43`, `:57`) | **Correct** | `test_book_bootstrap_migration.py:127` (a complete, empty inventory is required); `test_book_halt.py:65-72` (an injected RUNNING never grants permission) |
| (iv) | No resume | Allowed only with every other condition met, and "No production resume implementation is released until a named accepted producer supplies each retained E1/E2/E3 fact" (`:59`) | **Correct (fails closed); not built** | as above |

### 3.6 Takeover (rail S10 `:72`), found by the trace

Revalidation refuses when the fence is non-empty (`book_takeover_owner.py:558-559`). It also refuses when any unresolved attempt row exists anywhere in the account (`:621-622`, `takeover_account_not_quiescent`, using `_unresolved_attempt_rows`, `:760-766`). The capacity reducer additionally requires every displaced operation to be terminal (`book_capacity.py:277-281`).

| State | Code today | Spec | Verdict | Tests |
|---|---|---|---|---|
| (i), displaced leg | The plan cancels it; the takeover completes only after a terminal | "cancel every displaced resting or partially filled entry/add, counting a cancel only when evidence shows the order terminal" (`:72`) | **Correct** | `test_book_account_owner.py:359`; `test_book_capacity.py:110` |
| (i), non-displaced leg | Refused **from the send onward**, not after one bar (`:621`, operation `attempted`); after one bar also by the fence (`:558`) | "Under RUNNING with valid authorization and `blocks = ∅`" plus "fresh displaced-scope quiescence" (`:72`). Under the settled reading a known working order on another leg is neither a block nor in scope | **Defect under the settled reading.** It is also inconsistent with ordinary admission, which allows (i) for its first bar | None |
| (ii) | Refused | Refused (a block) | **Correct** | None specific |
| (iii) | Refused; an unknown **takeover child** halts (`book_takeover_owner.py:539-541`) | Refused; rev9 halt | **Correct** | None specific for an ordinary unknown during takeover |
| (iv) | Not refused | Not refused | **Correct** | as displaced above |

### 3.7 Capacity reservation (rail §1 ledger row `:28`; S2 `:56`), found by the trace

The reservation is the requested quantity minus credited fills while the operation is active and non-terminal (`book_capacity.py:137-140`). It is released only when the reducer accepts a terminal (`:212-224`), never by elapsed time and never by the fence.

| State | Code today | Spec | Verdict | Tests |
|---|---|---|---|---|
| (i)–(iii) | Held | Held "while it rests" (`:56`) and while the outcome is unknown (`:54`); "never elapsed time" (`:28`) | **Correct** | `test_pr409_review4.py:51-66` (held exposure); `test_book_capacity.py` |
| (iv) | Remainder released; fills converted | Released by confirmed terminal evidence. The never-dispatched proof path (`:28`) is not implemented; Gate A A1 limits it on this route | **Correct** | `test_book_capacity.py`; `test_pr409_review2.py:236-252` |

### 3.8 Close orders themselves in the four states (packet row (e)), found by the trace

The fence never counts closes (`:787-789`). Risk-adds are instead refused `close_unreconciled` while **any** exit or flat is non-terminal (`:1610-1612`). That is broader than the spec's "`unknown_order` block while a close is unresolved" (CLOSE `:46`), so it is correct for admission.

Loosening amends are refused only when a close's attempt is `UNKNOWN` (`book_protection_owner.py:493-494`). An **accepted but not yet terminal** close on another leg does not refuse a loosening amend. On the close's own leg the amend is deferred (`:546-549`). Takeover counts any attempted close as not quiescent (`:621`).

**Verdict:** admission and takeover are **correct**. Cross-leg loosening during an accepted, unresolved close is **spec-ambiguous**. The CLOSE bullet does not define "unresolved". If it means "not yet complete on evidence", the loosening gate is a defect. There are no tests for this case.

## 4. Evidence inputs and producers

| Input | What it must be to count | Consumed by | Producer today | Built? |
|---|---|---|---|---|
| Terminal fact (`BrokerFact.terminal`) | Observed no more than `MAX_FACT_AGE` (30 s, `:70`) after its `as_of`, or the owner halts (`:1918-1921`). Accepted by the capacity reducer (`book_capacity.py:212-224`). `as_of` strictly after preparation (`:795`) | Fence (iv); capacity release | `SyntheticBroker` (labeled test seam, `:207-228`) | Real producer **not built (T09)** |
| Fill fact (`BrokerFact.fill`) | Same age rule; identity and leg match the operation (`:1936-1943`) | Capacity conversion; adapter feedback | Synthetic seam | **Not built (T09)** |
| **Working-order evidence for entries and adds** — needed for (i) and (ii) | One complete, request-fenced, order-level acquisition of the symbol's working orders, order status and position, taken together (E1 `:109`). `as_of` strictly after preparation and after any later dispatch touching the order (evidence currency `:41`). At most one bar old (`W` row `:26`). Correlated to the request's own identity with quantities consistent with credited fills (E2 `:110`, E3 `:111`). A position-only read never counts (`:41`) | Nothing in the ordinary fence path. The shape exists as `AccountInventory.working_orders` and `requests` (`book_takeover.py:15-67`), consumed only by takeover (`book_takeover_owner.py:245-330`) and by bootstrap, which requires it empty | Synthetic `read_inventory` (`book_synthetic_protection.py:199-202`). `c1_rail_telemetry.BrokerEvidence` is operator-attested and does not supply this acquisition (rail spec producer obligations `:117`) | **Not built (T09).** On the REST route: a positive same-session lookup is established (Gate A A1), polling is a design obligation (A7), and cross-session reads are not demonstrated (D5) |
| Protection snapshot | Complete, fresh (`PROTECTION_PERIOD`, one bar) and postdating the pending operation | The protection owner's per-owner `evidence_at` and `evidence_fact` (`book_protection_owner.py:471`, `:583-586`, `:634-635`) | Synthetic `read_protection` | **Not built (T09).** It is also the in-code precedent for the evidence-freshness rule the fence needs |

## 5. Test coverage summary

| Consumer | (i) | (ii) | (iii) | (iv) |
|---|---|---|---|---|
| Admission | **None** (kernel only) | Covered, no evidence at all; return to working on fresh evidence **none** | Covered; the halt **none** | Covered |
| Loosening amend | **None** | **None** | **None** | Indirect |
| Tightening amend / attach | Indirect | Indirect | **None** (the halt interaction) | Indirect |
| Close (same leg / other leg) | Covered (via reservation) | Covered | Covered | Covered |
| Cancel | Covered | Covered | **None** specific | Covered |
| Recovery / deadline | Covered | Covered | Covered | Indirect |
| Resume gate | Covered (bootstrap, halt store) | same | same | same |
| Takeover | Displaced covered; non-displaced **none** | **None** specific | Child unknown covered; ordinary **none** | Covered |
| Capacity | Covered | Covered | Covered | Covered |
| Close orders (3.8) | Admission covered (`test_book_close_reconciliation.py:62-77`); loosening **none** | same | same | Covered |

The owner's tests pin today's classification of an accepted order with no evidence (`test_pr409_review4.py:51-88`). Those tests stay valid as state-(ii) tests under the repair below.

## 6. Proposed repair specification (behavior, not code)

### 6.1 Spec clarification (owner: the rail spec; proposed, not applied)

Add to the §1 `pending` row: an `accepted` or `partial` order that fresh, qualifying order-level evidence (§4) shows working is a **known working order**. The one-bar outcome timeout runs from the latest such evidence. A known working order holds its reservation and is not `UNKNOWN`. Add an acceptance case: a resting entry evidenced on every bar for several bars leaves other legs' risk-adds admitted. The kernel already has it: `test_tb_s3_kernel_review.py:56-66`.

### 6.2 Classification (the account owner)

For each entry or add request:
- **(iv) Terminal:** unchanged. When the real outcome classifier exists, derive the `REJECTED` shortcut (`:791-792`) again under Gate A A3: only a local pre-dispatch refusal, or a remote refusal with request-specific closure, is terminal.
- **(i) Known working:** the attempt is accepted, and the latest qualifying acquisition for the order's symbol (§4) shows the order working or partially filled under its own identity, strictly postdates preparation, and is at most one bar old at evaluation. It is **not** an unresolved request.
- **(ii) Stale:** accepted, not terminal, and not (i) once one bar has passed since preparation or since the last qualifying acquisition. It is **unresolved**, as today. It moves to (i) on a new qualifying acquisition and to (iv) on a terminal.
- **(iii) Unknown dispatch:** unresolved at once, as today, and resolved only by an accepted, postdating terminal. Whether a positive, correlated lookup may move (iii) to (i) stays **OPEN** (UB-7 is EVIDENCE-PENDING; Gate A A1 and A3 (iii)). The repair must not weaken (iii).
- **Never dispatched:** journal the attempt so that a request refused locally before any send (A3 (i)) is distinguishable from `UNKNOWN`, including the no-route path at `:1682-1684`.

### 6.3 Consumers after the repair

- **Admission** (`:1608`), **loosening amends** (`book_protection_owner.py:492`) and the **takeover fence** (`book_takeover_owner.py:558`): count states (ii) and (iii) only.
- **Takeover quiescence** (`:621`): count unresolved requests ((ii), (iii)) and non-terminal orders of **displaced** legs. Do not count a known working order (i) on a non-displaced leg.
- **Unchanged:** the close gate (`:1296-1301`), cancel (`:1573-1584`), cutoff, flatten and deadline (`:1768-1797`), and capacity. Under the repair a known working order still blocks recovery and deadline completion and is still cancelled at the cutoff.
- **Boundary:** choose "older than one bar" (strict) or inclusive, state it in the spec, and pin it with a test. Today the code is inclusive (`:793`) and the kernel strict (`kernel.py:1326`).

### 6.4 Fault cases and tests the repair needs

1. A resting entry evidenced on every bar for more than one bar: other legs' risk-adds, loosening amends and a non-displaced takeover are admitted, and the reservation is held.
2. Evidence stops: fenced from the moment the last qualifying acquisition is more than one bar old. Fresh working evidence returns the order to (i); a terminal resolves it.
3. An accepted order never evidenced: fenced after one bar. The existing tests `test_pr409_review4.py:51-88` stay as the pin.
4. Evidence that must **not** refresh (i):
   - a position-only read;
   - an incomplete or unfenced acquisition;
   - an acquisition at the same instant as preparation or earlier;
   - a read older than one bar;
   - a read observed later than the fact-age limit;
   - an order listed under another identity or on another symbol, or with a remainder inconsistent with credited fills (these quarantine or halt, as E2 and E3 require).
5. A partial fill whose remainder is still working, evidenced fresh: (i). Kernel analogue: `test_tb_s3_kernel_review_followups.py:44-58`.
6. An unknown dispatch (iii): fenced at once. Working evidence for a different order, a position-only read, or an equal-time terminal does not clear it. It is cleared only by an accepted, postdating terminal.
7. Two unresolved requests: resolving one does not unblock (E3; the existing `test_pr409_review4.py:69-88` as analogue).
8. Takeover: a non-displaced known working order does not block. A non-displaced stale order blocks. A displaced order must reach a terminal state.
9. Restart: evidence taken before the restart never makes an order (i) after it (S9 `:70`); the owner boots HALTED.
10. Cutoff with an order in (i): the cancel is sent. At D with any order in (i), (ii) or (iii): a breach (existing behavior, re-pinned).
11. The one-bar boundary, exactly at the edge.
12. Replay and reorder: a newer position-only read followed by an older full read cannot restore (i) (E1 `:109`).

### 6.5 Effect on the E1 freeze inventory

The production qualification closure binds `c1_rail.book_account_owner` as the `listener_account_owner` role (`ops/c1_rail/qualification/trust_domain.py:146`). It lists `book_protection_owner`, `book_takeover_owner`, `book_takeover`, `book_capacity`, `book_migration` and `book_migration_schema` as runtime dependencies (`:158-163`). The repair touches at least the account owner, the protection owner's loosening gate and the takeover owner's two checks. A new evidence ingress would likely also touch the evidence data classes, and if persisted, the schema and migration. **Each is an E1 freeze-inventory change** (allocation map `:131`, row B11 `:145`: "Any change re-enters the freeze inventory"). The packet requires the repair to be resolved before the ORB freeze. It should land before the inventory is frozen, not after, or the freeze would be re-entered.

### 6.6 Dependence on the ORB lifecycle ruling (stated; not resolved)

- **The repair is required under every lifecycle.** State (i) occurs without ORB's long-resting entry:
  - an order still working at the first barrier after placement: the code fences at exactly one bar, before a one-bar cancel's terminal can arrive;
  - a partially filled remainder;
  - a resting add, as in AC-3;
  - a market order whose terminal arrives late.
- **What the lifecycle ruling changes:**
  - **How long (i) must be sustained by evidence:** up to the span from range completion to the cutoff under a session-end lifecycle, and at most about one bar under a one-bar lifecycle.
  - **The required refresh cadence,** and so the producer's polling load (Gate A A7).
  - **Which fault cases are representative:** case 1 with a multi-bar ORB entry is realistic only if the entry rests for many bars.
  - **Request count, if re-issue is chosen:** each re-issued order is a new request, so there are more opportunities for state (iii).
- None of this is resolved here, and the lifecycle choice must not be made from it (operator ruling 2026-09-26).

### 6.7 Separate items, outside the fence repair

- **The rev9 halt** on an uncertain outcome for ordinary entries, adds, closes and cancels. It is already recorded as not implemented (packet CC-3); the protection path and takeover children already halt. Owner: TB-I3/T09.
- **The T09 outcome classifier** under Gate A A3, including the `REJECTED` shortcut and the never-dispatched journal (§6.2).
- **Same-leg close refusal** while an entry or add is unresolved (§3.3). This is a spec ambiguity between S5 and the consistency matrix on one side, and K1, S10 and §5 on the other. Owner: the rail spec.
- **Whether an accepted, unresolved close must block cross-leg loosening amends** (§3.8). Owner: the rail spec, CLOSE bullet.

## 7. Method, verification and limits

- **Read at `62c956f`:**
  - owner code: `book_account_owner.py` (fence, admission, dispatch and attempt journal, observation, close reservation, schedule), `book_protection_owner.py` (admission and evidence rows), `book_capacity.py`, `book_takeover_owner.py`, `book_takeover.py`, `book_bootstrap.py`, `book_halt.py`;
  - specs and records: rail spec §1, S1–S5, S9–S10, the consistency matrix, AC-3/5/8 and §2e; halt/resume §1–§5; incident ADR UB-7; the Gate A disposition A1, A3 and A7; allocation map C15, B11 and §B; packet §3;
  - tests: the test reference kernel (`tests/ops/tb_s3_kernel/kernel.py`) and the fence tests named in the card, plus `test_pr409_review4.py`, `test_pr409_related_cases.py`, `test_pr409_owner_lifecycle.py` and `test_book_protection_evidence.py`.
- **Tests run:** existing tests only, no code change.
  - `.\fp.ps1 python -m pytest tests/ops/qualification/test_replay.py tests/ops/test_pr409_review4.py tests/ops/test_book_feedback_journal.py tests/ops/test_book_close_reconciliation.py` plus the four kernel files under `tests/ops/tb_s3_cases/primitives/` (review, model, review_followups, findings): **139 passed**. Record: `.cache/fp-verification/20260926T232158Z-591119cf168f/record.json` (`status: completed`, exit 0, `source_stable: true`).
  - `test_pr409_related_cases.py`, `test_book_protection_evidence.py`, `test_book_account_owner.py`, `test_book_capacity.py` and `test_book_halt.py`: **170 passed**. Record: `.cache/fp-verification/20260926T232629Z-44105170d04d/record.json`.
  - Interpreter: `tmp/ops-env` Python 3.13.2 (launcher doctor passed).
- **Not done:**
  - No probe or new test was written: the card allows running existing tests only. The state-(i) defect is therefore shown by code reading and by the absence of any working-evidence input, not by a failing test.
  - No private port or Pine was read for this deliverable.
- **Kernel status:** the kernel is an unaccepted development reference (rail spec `:103`). Its behavior is cited as evidence, not authority.
