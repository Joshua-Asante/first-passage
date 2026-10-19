# Native protection and recovery: bounded pilot runbook

**Status:** PROPOSAL, 2026-10-18. Planning only. It grants no build, launch, connection, arm, order, session or spend, and changes no accepted contract. Every `⟨L-…⟩` limit is unbound until the portfolio and account are selected; a pilot cannot start with any limit unbound.

**Question and decision.** Which of the accepted protection and recovery rules carry over to a firm-approved native runtime, and what must be proved before one attended pilot session? The answer decides whether a native pilot card can be frozen, and what it must test first.

**Sources adapted** (owners; they govern where this note differs):
- [Halt/resume contract rev9](../spec/2026-09-14-tb-s3-halt-resume-contract.md) §1–§5, with §4.1–§4.3 (incident classes, C-a close outcomes, resume owner).
- [Incident ADR §A12](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a12--first-release-text-narrow-2026-10-01--accepted-2026-10-05-d1) F1–F6 (accepted first-release text), §2 qualification of continuing protection, §A11.2 (no same-session restart).
- [Protection and capacity contract](../spec/2026-09-12-tradeify-book-protection-capacity-spec.md) §2–§4 (quantity law, settled-close mode, reserve-before-send capacity).
- [DD protection concept-not-constant ADR](../adr/2026-07-13-dd-protection-concept-not-constant.md): mechanism invariant; trigger, scale and reference mode bind per portfolio and firm tier.
- Native experiment admission packet §4, §5 and §12.1 (`docs/superpowers/plans/2026-10-16-native-experiment-admission-PACKET.md`, primary checkout, unpublished): safety states, assertion register S1–C3.

**Native premise.** The native reassessment proposal (`docs/superpowers/plans/2026-10-16-native-deployment-reassessment-PROPOSAL.md`, primary checkout, unpublished) keeps signals, sizing, risk decisions, order management and recovery inside the firm-approved runtime (candidate: NinjaScript in NinjaTrader Desktop). So the rev9 listener, daemon and REST route have no native counterpart. Their duties move to one native **account owner** per account instance. Python receives exported records after the session and sends nothing back.

## 1. Contract carry map

| Accepted rule | Native adaptation | Changed? |
|---|---|---|
| One durable `HALTED`/`RUNNING` owner; every start is HALTED (rev9 §1) | The account owner's append-only journal holds the permission state, generation and a dirty epoch. A stored `RUNNING` never grants authority at start. | Owner moves into the native runtime |
| Every mutation passes one serializer (rev9 §1) | All orders for the account go through the account owner. No second strategy instance, ATM template or chart-trader action may hold orders on the account during a pilot session. | Stricter: one owner per account |
| Reserve before send; whole or refuse; unresolved reservations count (capacity §4) | Unchanged. Reserve in the journal before submit; partial fills move only filled quantity; an unknown request keeps its full reservation. | No |
| Settled-close mode selected once per session; never resize carried positions (capacity §3) | Unchanged. Mode is read from the journal's last accepted settled close, not from intraday account values. | No; trigger/scale unbound |
| Incident → durable halt, intervention, no runtime close/cancel/amend (rev9 §1, §3; A12 F1(c)) | Replaced by D-N1: on an incident the owner latches HALT, then may close only exposure it knows exactly (§2.8). Anything uncertain still goes to the operator. | **Yes** (D-N1) |
| Policy exits: scheduled cutoff and own-flat deadline under SCHEDULED_EXIT (rev9 §1, §5) | Kept, and the account loss stop joins them as a policy exit (§2.4). Any incident revokes this authority. | Adds the loss stop |
| Unknown outcome → hold reservation, halt; release only on unique correlation (A12 F1–F3) | Unchanged. Correlation uses broker order ID and execution ID, never signal name or timestamp. | No |
| Unexplained position, order or fill is an incident (A12 F5) | Unchanged, on every instrument in the account, including fills the owner did not request. | No |
| No same-session restart after an incident (A11.2) | Unchanged for the pilot: one session, then review. | No |
| Recovery complete only on fresh, coherent, postdating evidence (rev9 §3) | Two independent reads are required: the native account view and the firm platform's own view (§2.7). | Adds a second source |
| Schedule `D = min(16:00 ET, V − 15 min)` (rev9 §5) | `D = min(16:00 ET, V − 15 min, W_end − ⟨L-attend⟩)`, where `W` is the operator's attended window. Cutoff `D − 15 min`, flatten start `D − 5 min`, as before. | Adds the attendance bound |

## 2. Rules for the pilot

### 2.1 Simultaneous strategy entries

1. One account owner hosts every selected leg for that account, with a fixed leg priority. Several strategies may run on one account wherever the firm's rules allow it (D-N3). Separate strategy instances sharing one account are not admitted: their positions are tracked separately, so the account can net flat or reverse while each instance still holds protective orders.
2. Priority is the strategies' expected-value rank, highest first (D-N2). The rank is a fixed, strictly ordered list bound at portfolio selection and unchanged during a session. Signals that complete on the same bar are admitted in that order, one at a time. Each admission sees every earlier reservation from that bar, so a lower-ranked signal is refused, never clipped, when a higher-ranked one has used the room.
3. One leg per instrument per account. If the selected portfolio has two legs on one instrument, the selection must state whether they are serialized or refused. Opposing positions in one instrument are refused; firms commonly prohibit hedging (bind per firm).
4. Adds count as entries. They need a confirmed executed base, never an accepted order (capacity §2).

### 2.2 Shared exposure limits

Accounted usage = confirmed open quantity + every outstanding entry and add reservation, including partial, unknown and recovery-pending ones. Admit only if every limit holds after the request:

| Limit | Value | Source when bound |
|---|---|---|
| Account cap, micro-equivalents | `⟨L-cap⟩` | min(firm max contracts, portfolio allocation) |
| Per-instrument cap | `⟨L-inst⟩` | portfolio selection |
| Maximum concurrent legs | `⟨L-legs⟩` | portfolio selection |
| Worst-case open loss of all positions at their stops, plus reservations at their intended stops | `⟨L-risk⟩` | below `⟨L-day⟩` headroom (§2.4) |

Never clip a request to fit. A mode change never creates headroom. A takeover, like Aegis's in capacity §4, exists only if the selected portfolio defines one.

### 2.3 Protective-order ownership

1. The account owner submits each protective stop and target itself, linked to the entry by broker order ID, sized to the **filled** quantity, and resized on each partial fill. ATM templates are not used.
2. Protection counts as established only after the broker reports the protective order working. An entry acknowledgment, or a local OCO object, is not protection (incident ADR §2 qualification).
3. The interval between an entry fill and protection becoming working is measured. Above `⟨L-unprot⟩`, or if protection is rejected, it is an incident: the position is unprotected.
4. Where the protection lives (broker server, platform simulated stop, or local OCO) is recorded per order type for the firm's connection. Only server-resident protection may be relied on across a disconnect (U-3).
5. Disabling the strategy must not cancel working protection, and enabling it must not cancel protection on an existing position. On the operator's laptop on 2026-10-17, disabling left protective orders working, and re-enabling with `WaitUntilFlat` cancelled them and left the position unprotected (Sim101 canary). Strategy re-enable is therefore not a recovery step.

### 2.4 Loss stops

| Layer | Trigger | Action | Authority |
|---|---|---|---|
| Position stop | Price | Broker-resident protective stop (§2.3) | Established before the incident |
| DD sizing tier | Prior settled close ≤ peak × (1 − `⟨L-dd-trigger⟩`) | Next session's sizing × `⟨L-dd-scale⟩`; ORB-style adds refused | Mode set once per session (capacity §3) |
| Account day-loss stop | Realized + open P&L ≤ −`⟨L-day⟩`, set below the firm's daily or trailing limit by `⟨L-day-margin⟩` | Halt new risk, cancel resting entries, then policy-exit all legs | Policy exit, like the scheduled flatten; any incident revokes it |
| Firm liquidation | Firm's own rule | Firm acts | External actor; never relied on, never raced (rev9 §1) |

If the account P&L reading is stale or unavailable, that is an incident (rev9 §2, loss of required account evidence), not a pass.

### 2.5 Disconnects

1. Any loss of the broker or data connection halts new risk at once. Reconnecting never resumes trading.
2. Orders sent but not acknowledged before the disconnect become unknown when their outcome window expires. A12 F1 applies: hold the reservation, halt, no resend.
3. On reconnect the owner reconciles positions, working orders and executions since its last journal watermark. Any gap, or any fill or order it cannot correlate, is an incident (F5).
4. The platform's connection-loss setting must not recalculate or replay strategy state into new orders after reconnect (U-4).
5. A disconnect that outlasts `⟨L-disc⟩`, or that occurs after cutoff, is an incident. After reconnect, §2.8 applies: the owner closes exposure it knows exactly, and the operator handles the rest in the firm platform.

### 2.6 Uncertain account state

The owner enters `UNRESOLVED` (packet §12.1 states) and sends nothing when any of these holds: unknown request outcome; an uncorrelated fill, position or order; a protective order of unknown state; account P&L or position evidence missing or stale; a journal write failure; or a start with an unclosed dirty epoch. The owner sends no close for an uncertain position; that exposure waits for the operator. Exposure known exactly on other instruments may still be closed under §2.8. Fresh evidence alone never lifts the state: release follows A12 F2 and the halt ends only through §2.7.

### 2.7 Verified flat shutdown

Run at the planned end, after an incident, or at `D`, whichever comes first:

1. Owner latches HALT and cancels resting entries and adds.
2. Policy exits and §2.8 incident closes bring known legs flat; the operator flattens anything uncertain in the platform.
3. **Read A (native):** account positions, working orders and executions for every instrument on the account, postdating the last request.
4. **Read B (independent):** the firm platform's web view of the same account. The native order grid hides prior-day orders after rollover, so read A alone cannot prove no working orders.
5. Flat is verified only when both reads show zero gross positions, no working orders, and no unresolved request; every journal request has a terminal outcome; and every execution is correlated. Net zero, an empty grid, elapsed time or acknowledgment does not count (rev9 §3).
6. Then: disable the strategy, disconnect, set the connection not to connect on startup, and check the platform's saved workspace (it is rewritten on exit). Record each step's evidence.
7. Export the journal and both reads to authorized custody. Python compares offline.

If step 5 fails, HALT stays and the account stays under attended recovery past the planned end (rev9 §3, attendance).

### 2.8 Native incident close (D-N1)

On an incident the owner may close positions itself, within these bounds (adapted from packet §12.1):

1. Only risk-reducing commands: cancel resting entries and adds, and close open positions. No entry, add, reversal, re-entry, or loosening or widening of protection.
2. A close is sent only for a position whose residual quantity is known exactly from fresh facts correlated by broker order and execution ID. The close is sized to that quantity.
3. A close must not be able to reverse the position if a protective order fills at the same time. The pilot card binds the mechanism; U-17 must prove it. Until then, the incident close is not admitted for P2.
4. Protection stays working until the close is confirmed filled; then the owner cancels that position's protective orders and confirms them terminal.
5. No retry when an outcome is ambiguous. At most one replacement close follows a definitive rejection or cancellation, and only on fresh facts. A cancel acknowledgment does not prove the position is flat.
6. Unknown, partial, rejected or unexplained outcomes, and any position the owner cannot attribute, go to `UNRESOLVED` and the operator. The owner never sends an order against a position it does not own.
7. The incident still ends automation for the session (A11.2), and the session still ends with §2.7.

## 3. Pilot sequence and stop rules

| Stage | Environment | Entry gate | Pass |
|---|---|---|---|
| P0 | Synthetic native experiment (packet §5) | Packet custody grants | Assertions S1–C3 run with no unexplained divergence |
| P1 | Isolated local simulation account, no firm connection | P0 accepted; the host isolation steps from the 10-17 canary | Every case in §4 run on the real platform, with its incorrect variant detected |
| P2 | One attended session on the admitted firm account | Below | §2.7 verified flat; review recorded |

**P2 entry gate:** portfolio and account selected; every `⟨L-…⟩` bound by the owning record; firm admission for native automation on that account; this instance's own M1 acceptance (it cannot inherit the incumbent's); P1 accepted; per-session operator GO and attendance; `D` within `W`.

**Stop rules:** any incident ends automation for the session (A11.2). One session, then a recorded review before another. Two failed corrections of the same control stop the pilot track for redesign.

## 4. Native controls that remain unproved

None of these has native evidence today. Each is INCONCLUSIVE until its named test passes on the real platform and connection; simulation results do not prove broker behavior.

| ID | Control | Proving test | Packet ID |
|---|---|---|---|
| U-1 | One owner per account excludes every other order source (other strategies, ATM, chart trader, add-ons such as CrossTrade, ATI) | Inject an order from each source; owner detects and halts | I1 (partial) |
| U-2 | Same-bar multi-leg admission in priority order with reservations visible to later legs | Two legs signal on one bar at the cap edge | Z1 (partial) |
| U-3 | Protection residency per order type on the firm's connection (server vs local OCO/simulated stop) | Place, disconnect, move price through the stop, reconnect | R3 |
| U-4 | Connection-loss and restart settings cause no replayed or recalculated orders | Disconnect and restart mid-position under each setting | R1, R3 |
| U-5 | The platform's error-handling setting either stays out of the way or behaves exactly as §2.8 requires: no reversal, and no retry after an ambiguous outcome | Reject an entry, an add and a protective amend | O1 |
| U-6 | Disable and enable never cancel working protection on an open position | Repeat the 10-17 canary under the pilot settings | none |
| U-7 | Fill-to-protection interval measurable and bounded by `⟨L-unprot⟩` | Timed entry fills, including partials | Z2 (partial) |
| U-8 | Journal dirty epoch blocks entry after a failed write at every cut | Fault cuts before write, before replace, after replace | R2 |
| U-9 | Unknown outcome detected and correlated by broker order and execution ID, never resent | Suppress an acknowledgment, then reconnect with complete, absent and contradictory facts | O2 |
| U-10 | Account P&L reading fresh and accurate enough for the day-loss stop | Compare native readings with firm statements over a session | none |
| U-11 | Day-loss policy exit completes before the firm's own liquidation | Synthetic loss path to `⟨L-day⟩` | none |
| U-12 | Uncorrelated fill or order on any account instrument raises an incident | Operator places a manual order mid-session | I1 (partial) |
| U-13 | Two-source flat verification (§2.7) catches a working order hidden from the native grid after rollover | Leave a prior-day order working; run §2.7 | none |
| U-14 | Scheduled cutoff and flatten derive from source-backed calendar rows, including early closes and DST | Calendar fixtures at each boundary | S1 |
| U-15 | Firm-side external actors (auto-liquidation, server-side risk rules) inventoried and raced safely | Firm documentation plus one observed event | none |
| U-16 | Wrong-account and profile-swap refusal on the real loader, key and outbound destination | Packet I1 and I2 on the platform, not a fixture | I1, I2 |
| U-17 | §2.8 incident close cannot reverse a position when a protective order fills at the same time, and sends nothing for uncertain exposure | Trigger the stop while the close is in flight; close with exposure known exactly, partially known and unknown | R3 (partial) |

## 5. Decisions

Operator rulings, 2026-10-18 (Joshua, in session):

- **D-N1:** "the NinjaTrader strategy be allowed to close positions itself". Adopted as the bounded incident close in §2.8. Before P2 can rely on it, U-3, U-5, U-9 and U-17 must pass.
- **D-N2:** "strategies are ranked by expected value, the higher ranked strategy gets priority. this can be done simply". Adopted in §2.1 item 2. The rank values come from portfolio selection. How two strategies on one instrument are handled, and every `⟨L-…⟩` value, also wait for portfolio selection.
- **D-N3:** "running several strategies should not be a problem as long as it doesn't violate their rules". Adopted in §2.1 item 1. The selected firm's hedging, news and automation terms are checked at its admission.

Operator rulings, 2026-10-19 (Joshua, in session, "yes" to the review disposition of §6–§7: yes to the two-level latch, the entry barrier and the reference-model package; revise the uncertain-set exit; close-first incident behavior; halt by default on entry rejection):

- **D-N4:** `HALT` stops new risk and continues controlled risk reduction; `INCIDENT` withdraws trust in ordinary strategy behavior and allows only the restricted recovery procedure (§6.5, §6.9). The bar barrier orders entries only; safety events never wait behind it (§6.6).
- **D-N5:** Close first under `INCIDENT`. Known exposure is ended, not repaired: the owner submits no new or tightened protection under `INCIDENT` and closes exactly known positions by the §6.9 procedure. This is a policy choice for the first pilot, not a reading of §2.8's wording.
- **D-N6:** A definitive, zero-fill entry rejection releases the unused reservation, is never resent, and latches `HALT` for review; contradictory fills, status or protection make it `INCIDENT` (§6.8). Specific benign rejection reasons may be allowed later by ruling.

## 6. Shared account-risk interface

*Added 2026-10-18 and revised 2026-10-19 for D-N4 to D-N6 (§5); same proposal status as above.* §2 states the rules; this section states the contract every account owner implements. One contract serves three uses: the NinjaScript owner (P1, P2); a pure Python reference model, the P0 oracle ([build card](../briefs/handoffs/2026-10-18-account-risk-reference-model-card-DRAFT.md)); and the offline check of exported journals (§2.7 step 7), where replaying a session's journal through the reference model must reproduce every decision, command and latch. The reference model is an offline specification and test oracle, never a service in the live execution path; passing it proves nothing about NinjaTrader or broker behavior. It generalizes the laws of the Python book reducer (`ops/c1_rail/book_capacity.py`: reserve before send, whole or refuse, partial fills move only filled quantity, a terminal must match its fills, invalid evidence adds a block and never a release) from the fixed four-leg book to configured legs and limits.

### 6.1 Roles

| Role | May | May not |
|---|---|---|
| Strategy leg | Emit intents (§6.3) for its own leg | Send, modify or cancel any order; read another leg's state |
| Account owner (one per account) | Decide intents; send every order; own protection; latch | Unlatch within the session (A11.2); clip a request |
| Broker adapter | Deliver facts with broker order and execution IDs | Synthesize a fact the broker did not report |
| Operator | Start the session; give GO; recover uncertain exposure | — |

### 6.2 Configuration

One `AccountRiskConfig` per account instance, bound by the portfolio-selection record. Its canonical hash, `config_id`, is written on every journal record. Every limit is a field, never a constant.

| Field | Meaning | Bound by |
|---|---|---|
| `account_id`, `instance` | The only account the owner may touch | Account admission |
| `legs[]` | `leg_id`, `instrument`, `order_symbol`, `micro_equiv`, `point_value`, `entry_side`, `rank`, `adds_allowed` | Portfolio selection |
| `same_instrument` | `refuse` or `serialize` (§2.1 item 3) | Portfolio selection |
| `cap_micro` | `⟨L-cap⟩` | §2.2 |
| `instrument_cap{}` | `⟨L-inst⟩` per instrument | §2.2 |
| `max_legs` | `⟨L-legs⟩` | §2.2 |
| `max_open_risk` | `⟨L-risk⟩`, account currency | §2.2 |
| `day_loss_stop` | `⟨L-day⟩`, recorded with `⟨L-day-margin⟩` | §2.4 |
| `unprotected_max` | `⟨L-unprot⟩` | §2.3 |
| `disconnect_max` | `⟨L-disc⟩` | §2.5 |
| `outcome_window` | Time after a send with no acknowledgment before the order is unknown | Pilot card |
| `fact_max_age` | Maximum age of a snapshot or P&L reading used for a decision | Pilot card |
| `barrier_timeout` | How long a bar batch waits for every leg's report, from the bar's close time | Pilot card, from timing observed in P1 |

Loading rejects the configuration, and the owner stays `HALTED`, if any field is unbound, ranks are not unique, a `micro_equiv` or `point_value` is not positive, or two legs share an instrument with opposite `entry_side` or without `same_instrument` bound.

### 6.3 Inputs

Every input carries `event_id`, a strictly increasing `sequence`, `as_of`, `account_id`, owner epoch and `config_id`. An identical replayed event is a no-op; the same `event_id` with different content is a block (§6.8).

| Input | Fields | From |
|---|---|---|
| `BarReport` | `leg_id`, `bar_time`, `intents[]` (may be empty) | Strategy leg |
| `EntryIntent` | `intent_id`, `leg_id`, `bar_time`, `kind` (`BASE`/`ADD`), `quantity`, `reference_price`, `stop_price`, `base_order_id` for an add | Strategy leg, inside a `BarReport` |
| `ExitIntent` | `intent_id`, `leg_id`, `quantity` | Strategy leg |
| `Ack` | `order_id`, `client_tag` | Broker |
| `Fill` | `execution_id`, `order_id`, `quantity`, `price` | Broker |
| `Terminal` | `order_id`, `status` (`filled`/`cancelled`/`rejected`), `cumulative_filled` | Broker |
| `ProtectionState` | `order_id`, `state` (`working`/`rejected`/`terminal`), `quantity`, `stop_price` | Broker |
| `Connection` | `up` or `down` | Adapter |
| `Snapshot` | `source` (`A` native, `B` firm platform), positions, working orders, executions since the journal watermark | Adapter |
| `AccountPnl` | Realized plus open P&L | Adapter |
| `Tick` | `now` | Clock |
| `OperatorStart` | Session ID and GO reference | Operator |

### 6.4 Outputs

Before any command the owner appends the decision and the command to its journal (write-ahead). A failed write sets the dirty epoch and sends nothing (§2.6).

| Output | Meaning |
|---|---|
| `Decision` | `intent_id`, `ADMITTED` or `REFUSED`, reason (§6.6) |
| `SubmitEntry` | Exactly the admitted quantity; a fresh `client_tag` per payload |
| `SubmitProtection`, `ResizeProtection` | Stop (and target) linked to the entry `order_id`, sized to its filled quantity |
| `Cancel` | A resting entry or add; protection only under §6.7 item 4 |
| `Close` | Policy exit (§2.4, `ExitIntent`) or incident close (§6.9), sized to exactly known quantity |
| `Latch` | `HALT` or `INCIDENT`, with reason; never cleared within the session |

### 6.5 State and accounting

Per order: requested quantity, fills by `execution_id`, terminal, and state `SENT → ACKED → TERMINAL`, or `UNKNOWN` once `outcome_window` passes with no `Ack`. Per leg: confirmed open quantity (fills minus correlated closes) and its protection.

- **Reservation** of an order: requested minus filled while it is not terminal. An `UNKNOWN` order keeps its full remaining reservation; a terminal order reserves nothing.
- **Usage** per limit: confirmed open plus every reservation, including partial, unknown and recovery-pending ones, in the limit's unit. Micro-equivalents for `cap_micro` and `instrument_cap`; legs holding confirmed or reserved quantity for `max_legs`; Σ |quantity| × |price − stop| × `point_value` for `max_open_risk`, using the fill price for open quantity and `reference_price` for reservations.
- **Permission (D-N4):** `RUNNING`; `HALTED`, which stops new risk and continues controlled risk reduction (policy exits, §6.9); or `INCIDENT`, where ordinary strategy behavior is no longer trusted and only the §6.9 procedure runs. Every session starts `HALTED`. The operator's start moves it to `RUNNING` only with a clean epoch and a verified-flat account (§2.7). Any exit or close also needs the connection up and exposure reconciled from facts fresher than `fact_max_age`. `disconnect_max` only decides when a disconnect becomes an incident; it never pauses the protection deficit clock (§6.7).
- **Uncertain set:** instruments whose exposure is not known exactly. The owner sends nothing on them; they wait for the operator (§2.6). An instrument leaves the set only when its position follows exactly from correlated executions and every order on it is either terminal with a uniquely correlated outcome (A12 F2) or the owner's own protective order, confirmed working at a known quantity by fresh facts. Working protection never blocks the exit and is never cancelled to clear the set. Leaving the set permits a §6.9 close; it never lifts a latch.

### 6.6 Entry admission

A bar batch for `bar_time` closes when every configured leg has sent its `BarReport` for that bar, or when `barrier_timeout` passes, measured from the bar's close time. Intents in a later report are refused `late` and journaled as missed signals; a missed signal is never carried forward. The batch is decided in `rank` order, one intent at a time, each against usage that includes every earlier admission in the batch. Arrival order inside a batch never matters. The barrier orders entry intents only: fills, terminals, protection states, exits, cancels, connection events and latches are processed on arrival and never wait for a batch (D-N4).

An intent is admitted only if every row holds. Otherwise it is refused whole, never clipped, with the first failing reason:

| Order | Condition | Refusal |
|---|---|---|
| 1 | Permission `RUNNING` | `halted` |
| 2 | `intent_id` not seen before | `duplicate` |
| 3 | Leg configured; side equals `entry_side`; no opposite position on the instrument | `invalid_leg`, `opposing` |
| 4 | An add: `adds_allowed`, and `base_order_id` has a confirmed fill on this leg | `add_without_base` |
| 5 | `same_instrument` rule satisfied | `same_instrument` |
| 6 | `cap_micro`, `instrument_cap`, `max_legs`, `max_open_risk` each hold after the request | `cap`, `instrument`, `legs`, `risk` |
| 7 | P&L above −`day_loss_stop` (a reading older than `fact_max_age` is a block, §6.8) | `day_loss` |

A refused intent has no later effect: it is not queued, retried or resized. An `ExitIntent` becomes a `Close` only while `RUNNING` or `HALTED`, only for quantity known exactly on that leg net of closes already in flight, so it cannot reverse the position; with the connection down it is refused `disconnected`; under `INCIDENT` it is refused and §6.9 governs.

### 6.7 Protection ownership

1. For each entry order, the owner keeps protection whose working quantity equals that order's confirmed open quantity. Each `Fill` produces `SubmitProtection` or `ResizeProtection` to the new filled total; each correlated close reduces it.
2. Coverage counts only on `ProtectionState(working)` at the target quantity. A deficit clock runs from the first uncovered fill until coverage is confirmed. A deficit longer than `unprotected_max`, or `ProtectionState(rejected)`, latches `INCIDENT` (§2.3 item 3).
3. Strategy logic may move a stop only toward less risk; protection is never widened. Under `INCIDENT` no protection is submitted, resized upward, tightened or moved (D-N5); it is only reduced or cancelled as §6.9 allows.
4. Protection is cancelled only after fills confirm the position it covers is flat (§2.8 item 4). The cancel counts only when `ProtectionState(terminal)` arrives.
5. Disconnect, strategy disable and owner restart never cancel protection (§2.3 item 5).

### 6.8 Blocks

Each condition latches as shown. No later fact lifts a latch within the session; the session ends through §2.7.

| Condition | Latch | Uncertain set gains |
|---|---|---|
| Order `UNKNOWN` (no `Ack` within `outcome_window`) | `INCIDENT` | Its instrument |
| `Fill` for an order not in the journal, or exceeding its reservation; an `execution_id` repeated with different content | `INCIDENT` | Its instrument |
| `Terminal.cumulative_filled` differs from the sum of correlated fills | `INCIDENT` | Its instrument |
| A snapshot position, order or execution the journal cannot correlate | `INCIDENT` | Its instrument |
| Snapshots `A` and `B` disagree | `INCIDENT` | The disagreeing instruments |
| Protection deficit beyond `unprotected_max`, or protection rejected | `INCIDENT` | None while the position is known exactly |
| `Connection(down)` | `HALT`; `INCIDENT` if it lasts beyond `disconnect_max`, occurs after cutoff, or reconnect reconciliation finds a gap | Instruments with orders in flight at the drop |
| P&L or snapshot older than `fact_max_age` when a decision needs it | `INCIDENT` | None |
| Journal write failure; start with an unclosed dirty epoch | `INCIDENT` | All instruments |
| Event under another `config_id`, account or epoch; conflicting `event_id` | `INCIDENT` | None |
| Entry `Terminal(rejected)` with zero fills, consistent with every fact (D-N6) | `HALT`; the unused reservation is released and nothing is resent | None |
| Entry rejection with any fill, status or protection fact that is uncertain or contradictory | `INCIDENT` | Its instrument |
| A fill that would take a leg's position through zero | `INCIDENT` | Its instrument |
| Scheduled cutoff or day-loss stop reached | `HALT`, then policy exit (§2.4) | None |

Reconnect never resumes trading. After `Connection(up)` the owner reconciles from its watermark (§2.5 item 3) and stays latched.

### 6.9 Incident close procedure (D-N5)

Under `INCIDENT` the owner ends exposure rather than repairing it. This implements §2.8 with the D-N5 policy; U-17 must still prove the native mechanism before P2 relies on it.

1. **Stop new exposure.** Cancel every resting entry and add at once. Each keeps its remaining reservation until its `Terminal` arrives; a fill that arrives before the terminal joins the leg's known exposure and is closed under this procedure.
2. **Protection stays.** Working protection is left in place at its current price. It is resized only downward, to match confirmed closes, and cancelled only under §6.7 item 4. No new or tightened protection is submitted.
3. **Close known exposure.** For each leg outside the uncertain set, send one `Close` for the exactly known open quantity minus closes already in flight. Exposure that appears later (item 1) gets its own close on fresh facts.
4. **Partial close fill.** Reduce known exposure and protection by the filled quantity; the remainder of the close keeps working.
5. **Protective stop fills during a close.** Reduce known exposure by the stop fill, then cancel any close quantity now exceeding known exposure. If a close fill would take the position through zero, the instrument enters the uncertain set (§6.8); the native mechanism that prevents this is U-17.
6. **Close rejected or ambiguous.** After a definitive rejection or cancellation, at most one replacement close follows, on fresh facts (§2.8 item 5). An ambiguous outcome (`UNKNOWN`, or a terminal that disagrees with fills) puts the instrument in the uncertain set; nothing is resent.
7. **Done.** A leg is closed when correlated fills show it flat and its protection is `ProtectionState(terminal)`. The session then ends through §2.7.

## 7. Deterministic scenarios

These are the interface's acceptance fixtures. The reference model must pass each; P1 runs each on the real platform (§3); each **incorrect variant** is an implementation error the check must detect. Fixture values are test inputs, not proposals for any `⟨L-…⟩`.

**Fixture:** legs `A` (rank 1, instrument X), `B` (rank 2, Y) and `C` (rank 3, Z), each `micro_equiv` 1, long only, adds allowed on `A`. `cap_micro` 4; `instrument_cap` 4 each; `max_legs` 2; `max_open_risk` and `day_loss_stop` non-binding; `outcome_window` 3 s; `unprotected_max` 5 s; `disconnect_max` 10 s; `barrier_timeout` 2 s. Each scenario starts `RUNNING`, flat and unblocked at t = 0; protection confirms working 0.5 s after each fill unless the row says otherwise.

| ID | Events | Expected | Incorrect variant |
|---|---|---|---|
| **Competing entries** | | | |
| CE-1 | One bar: `B` reports entry 2, then `A` reports entry 3 | `A` admitted 3 (rank 1 decided first); `B` refused `cap` (3 + 2 > 4); one `SubmitEntry` of 3 | Arrival order decides; `B` clipped to 1 |
| CE-2 | One bar: `A` 1, `B` 1, `C` 1 | `A` and `B` admitted; `C` refused `legs` | `C` admitted because micro usage 3 ≤ 4 |
| CE-3 | Bar 1: `A` 3 admitted, 1 filled, 2 working. Bar 2: `B` 2 | `B` refused `cap` (1 confirmed + 2 reserved + 2 > 4) | Only confirmed quantity counted |
| CE-4 | `A` holds a working entry of 1 from bar 0. Bar 1 closes at t = 0: `A` reports no intent and `B` entry 1 at t = 0.5; `A`'s working entry fills 1 at t = 1; `C` reports entry 1 at t = 2.5 | Protection for `A` sent at t = 1, not at batch close; batch closes at t = 2 and `B` is admitted; `C` refused `late` and journaled as a missed signal, never carried to bar 2 | Fill or protection held until the batch closes; batch reopened for `C`; `C` decided against stale usage |
| CE-5 | `A` add 1 whose `base_order_id` is acknowledged but unfilled | Refused `add_without_base` | Acknowledgment treated as an executed base |
| **Partial fills** | | | |
| PF-1 | `A` 3 admitted; fill 1 at t = 1; working (1) at 1.5; fill 2 at t = 2; working (3) at 2.5 | Usage 3 throughout; protection commands sized 1, then 3; no deficit beyond 0.5 s; no latch | Protection sized to the requested 3 before fills; reservation released at the first fill |
| PF-2 | `A` 3 admitted; fill 1 at t = 1; protection acknowledged, never working | `INCIDENT` at the first `Tick` after t = 6; new intents refused `halted`; the resting 2 are cancelled and keep their reservation until `Terminal`; no new protection is sent; one §6.9 close of exactly 1 | Acknowledged protection counted as coverage; the resting 2 left working or forgotten |
| PF-3 | `A` 3 admitted; fill `e1` of 1; then `e1` again with quantity 2 | `INCIDENT`; `X` uncertain; no close sent on `X` | The second report replaces the first |
| **Cancellations** | | | |
| CX-1 | `A` 3 admitted; fill 1; owner cancels the rest; cancel acknowledged, no `Terminal` yet; next bar `B` 2 | `A` still reserves 2; `B` refused `cap` | Cancel acknowledgment releases the reservation |
| CX-2 | CX-1, then `Terminal(cancelled, cumulative 1)`; next bar `B` 2 | Reservation 0, confirmed 1, protection stays at 1; `B` admitted (1 + 2 ≤ 4) | Protection cancelled with the entry |
| CX-3 | `A` 3 admitted; fill 1; `Terminal(cancelled, cumulative 2)` | `INCIDENT`; `X` uncertain; reservation held | Terminal accepted and the missing fill assumed |
| CX-4 | `A` 3 admitted; `Terminal(rejected, cumulative 0)`; next bar `B` 1 | Reservation released; nothing resent; `HALT` (D-N6); `B` refused `halted` | Rejected order resent; rejection treated as harmless and trading continues |
| CX-5 | `A` 3 admitted; `Terminal(rejected, cumulative 0)`; then a `Fill` of 1 on that order | `INCIDENT`; `X` uncertain; nothing sent on `X` | The late fill ignored because the order was terminal |
| **Reconnects** | | | |
| RC-1 | `A` 2 sent at t = 0, no `Ack`; `Connection(down)` at t = 1, `up` at t = 4; snapshots `A` and `B` agree: `X` long 2 from one correlated execution of 2, order terminal filled | `HALT` at t = 1; `INCIDENT` at t = 3 (`UNKNOWN`); after reconnect `X` leaves the uncertain set with 2 known exactly; permission stays `INCIDENT`; one §6.9 close of 2, with no protection submitted first (D-N5); no entry or resend | Reconnect restores `RUNNING`; the order is resent |
| RC-2 | As RC-1, but the snapshots show `X` long 2 and no execution since the watermark | `X` stays uncertain; the owner sends nothing on `X`; operator recovery | Owner closes 2 on the position read alone |
| RC-3 | Flat, nothing in flight; down at t = 1, up at t = 12 | `HALT` at t = 1; `INCIDENT` at t = 11 (> `disconnect_max`); §2.7 runs | No incident because nothing was in flight |
| RC-4 | After reconnect, snapshot `A` shows no working orders; snapshot `B` shows a working order on `Y` absent from the journal | `INCIDENT`; `Y` uncertain; flat not verified (§2.7 step 5) | Snapshot `A` alone accepted |
| RC-5 | Owner restarts with an unclosed dirty epoch and a stored `RUNNING` | `INCIDENT`; operator start refused | Stored `RUNNING` honoured |
| RC-6 | `X` long 2 with protection working at 2; `Connection(down)` at t = 1; `A` `ExitIntent` 2 at t = 2; `up` at t = 4; snapshots agree: position 2 correlated, protection working at 2, no other orders | `HALT` only (4 s < `disconnect_max`); the exit at t = 2 refused `disconnected`; `X` known exactly despite its working stop; protection untouched; a new `ExitIntent` after reconciliation becomes a `Close` of 2; no entries | `X` held uncertain because its stop is not terminal; protection cancelled to clear it; exit sent while down; `RUNNING` restored |
| **Incident close (§6.9)** | | | |
| IC-1 | PF-2 state: close of 1 working, cancel of the resting 2 sent; one of the 2 fills before `Terminal(cancelled, cumulative 2)` (cumulative counts both fills) | Known exposure becomes 2; a second close of 1 follows on that fill; reservation 0 after the terminal; protection never resized upward | The late entry fill dropped, or protected instead of closed |
| IC-2 | `X` long 2, protection working at 2, `INCIDENT`; close of 2 sent; stop fills 2 before the close fills | Known exposure 0; the close is cancelled; if a close fill still arrives, `X` enters the uncertain set and nothing more is sent on `X` | Close left working; a fill through zero treated as normal |
| IC-3 | `X` long 1, `INCIDENT`; close of 1 rejected definitively; fresh snapshot still shows long 1; replacement also rejected | Exactly one replacement close; after the second rejection nothing is sent and `X` waits for the operator; protection stays working | A third close; protection cancelled |
| IC-4 | `X` long 1, `INCIDENT`; close of 1 sent; no `Ack` within `outcome_window` | `X` enters the uncertain set; nothing resent; protection stays working | Close resent |

Every scenario also asserts that each command follows its journal record, and that replaying the journal through the model reproduces the same decisions, commands and latches.
