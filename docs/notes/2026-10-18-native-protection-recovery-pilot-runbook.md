# Native protection and recovery: bounded pilot runbook

**Status:** PROPOSAL, 2026-10-18. Planning only. It grants no build, launch, connection, arm, order, session or spend, and changes no accepted contract. Every `⟨L-…⟩` limit is unbound until the portfolio and account are selected; a pilot cannot start with any limit unbound.

**Question and decision.** Which of the accepted protection and recovery rules carry over to a firm-approved native runtime, and what must be proved before one attended pilot session? The answer decides whether a native pilot card can be frozen, and what it must test first.

**Sources adapted** (owners; they govern where this note differs, except where a §5 operator ruling records the departure):
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
| Unknown outcome → hold reservation, halt; release only on unique correlation (A12 F1–F3) | Unchanged. Correlation uses the owner's fresh `client_tag` bound to the broker order ID, plus the execution ID; never signal name or timestamp (§6.3). | No |
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

The owner enters `UNRESOLVED` (packet §12.1 states) and sends nothing when any of these holds: unknown request outcome; an uncorrelated fill, position or order; a protective order of unknown state; account P&L or position evidence missing or stale; a journal write failure; or a start with an unclosed dirty epoch. The owner sends no close for an uncertain position; that exposure waits for the operator. Exposure known exactly on any instrument outside the uncertain set (§6.5) may still be closed under §2.8 and §6.9 (D-N5). Fresh evidence alone never lifts the state: release follows A12 F2 and the halt ends only through §2.7. Under D-N8 (pending, §5) the exceptions to sending nothing are cancels of the owner's own resting entries and adds and, outside `INCIDENT`, protection for correlated fills; after a journal write failure nothing at all is sent.

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
2. A close is sent only for a position whose residual quantity is known exactly from fresh facts correlated by `client_tag`, broker order ID and execution ID (§6.3). The close is sized to that quantity.
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
| U-9 | Unknown outcome detected and correlated by broker order and execution ID, never resent | Suppress an acknowledgment, then reconnect with complete, absent and contradictory facts; show that reads A and B each return the `client_tag` on order records | O2 |
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

Pending operator rulings, amendment A1 (2026-10-20). A1 closes the gaps the coordinator's review found in §6 and §7 against the [reference-model card](../briefs/handoffs/2026-10-18-account-risk-reference-model-card-DRAFT.md). §6 and §7 are written for the recommended option of each ruling and mark the clauses it affects. The ruling selects or replaces that text before the card is reconciled and dispatched. Under the recommended options the card's text does not change, so it needs reconciliation at dispatch, not a new freeze.

- **D-N7 (pending): how a strategy withdraws its own resting entry.** Before A1, every owner cancel latched `HALT` or `INCIDENT`, so CX-1 and CX-2 could not be built.
  - **A (recommended):** a leg may send `CancelIntent` for its own resting entry or add. The owner sends the `Cancel` under `RUNNING` or `HALTED` and latches nothing (§6.3, §6.6). Strategies commonly withdraw unfilled entries; without this, every such withdrawal would halt the session.
  - **B:** strategies cannot cancel. The owner cancels a resting entry when a configured lifetime expires and latches nothing. `entry_ttl` becomes a pilot-card field and a fifth §6.5 timer, started at the entry's send; `CancelIntent` is removed and CX-1 is restated around the expiry. The card needs reconciliation only.
  - **C:** no cancel without a latch. CX-1 and CX-2 become broker-originated cancels, as CX-3 is, and §6.8 must declare a consistent cancel the owner did not request to be no incident. CX-1's incorrect variant is restated; mutant M4 is unchanged and still caught by PF-2, so the card needs reconciliation only. A strategy that withdraws its own entries is then not admissible to the pilot.
- **D-N8 (pending): cancelling the owner's own resting entries on an uncertain instrument.** Every cancel of resting entries (a `CancelIntent`, the cutoff and day-loss stop, §2.7 step 1 and §6.9 item 1) conflicted with "the owner sends nothing" on an uncertain instrument (§6.5). PF-3 and CX-3 meet the case under `INCIDENT`; after a disconnect it also arises under `HALT`.
  - **A (recommended):** a cancel of the owner's own resting entry or add is sent on any instrument, uncertain ones included, from any of those sources, each under the permissions §6 gives it (under `INCIDENT` only §6.9 item 1 cancels). Outside `INCIDENT`, protection for a correlated fill is also sent there. Nothing else is sent on an uncertain instrument. A cancel or new protection can only reduce exposure; a resting entry left working, or a fill left unprotected, can only add to it. D-N1 already departs from the [incident ADR](../adr/2026-09-17-bounded-platform-protection-incident-contract.md) for instruments known exactly: its §2 bars automatic post-incident cancellation of previously sent entries without an explicit amendment, and its §A12 F1(c) bars incident-time broker mutation. Option A extends that departure to uncertain instruments, and the ruling is the explicit amendment §2 asks for. PF-3 and CX-3 exercise it. Option A still sends no cancel for an order that has ever been `UNKNOWN`, so §A12 F1(a)'s bar on a speculative cancel of an unknown request stands.
  - **B:** nothing at all is sent on an uncertain instrument, protection for new fills included. Its resting entries keep working until the operator acts, a `CancelIntent` there is refused `uncertain`, and an unprotected fill there latches `INCIDENT` through the deficit clock.
  - Under either option, the owner cancels only an order whose `order_id` an `Ack` bound and that has never been `UNKNOWN`. An order known only from a snapshot record, or one that was ever `UNKNOWN`, goes to the operator. An order whose cancel is already sent, acknowledged or `UNKNOWN` is not cancelled again. After `JournalWriteFailed`, nothing at all is sent (§6.3).
- **D-N9 (pending): an owner restart with a clean epoch, after this session's `OperatorStart`.** rev9 keeps open whether a restart with no prior incident is itself an incident (O-4); the Phase 5 plan proposes treating an unexpected restart like one. rev9's process-restart row reads: "Halt, restore original operation identities and require reconciliation/attended intervention as needed. No automatic broker mutations or reuse of pre-restart running authorization." A `Restart` before the session's `OperatorStart` (a planned boot) latches nothing under every option.
  - **A (recommended):** the `Restart` latches `INCIDENT` (reason `restart`). Every instrument with a position or a non-terminal order enters the uncertain set until a snapshot pair taken after the restart reconciles it. Strategy intents are refused, only the §6.9 procedure runs, and `OperatorStart` is refused `latched` for the rest of the session. §6.9's cancels and closes are automatic broker mutations, but D-N1 already rules on them; nothing else is sent. This follows the Phase 5 proposal and the §3 stop rule (one session, then review).
  - **B:** the `Restart` latches `HALT`, with the same uncertain-set rule. Strategy cancels and exits and the scheduled sequence keep running under `HALT`, which departs from "No automatic broker mutations" while U-4 (no replayed or recalculated orders after a restart) is unproved.
  - **C:** nothing is latched and nothing becomes uncertain. Exposure carried across the restart stays known exactly without reconciliation, `HALTED` exits and cancels act on pre-restart state, and the session may be started again once verified flat. This departs from rev9's process-restart row and from the §3 stop rule.

Coordinator readings A1 adopts as interface completion, not rulings. Any of them can be overruled:
- Timers are strict (§6.5), matching §2.5 "outlasts" and §2.3 "above".
- Correlated `Fill`, `Terminal` and `ProtectionState` facts do not age; `fact_max_age` bounds only `Snapshot` and `AccountPnl` readings (§6.5). The stricter alternative, that a §6.9 close also needs a snapshot pair taken after the latch, would add snapshots to PF-2, IC-1 and IC-2.
- Commands withheld after a journal write failure count as never sent, keep their reservations, and leave verified flat false for the session (§6.3).
- A `Connection(down)` before `OperatorStart` latches nothing; `OperatorStart` then needs a snapshot pair taken after the reconnect (§6.5).
- A replacement close after a definitive rejection is sent on that rejection, which is a fresh fact (§6.9 item 6).
- A snapshot pair that disagrees on some instruments is still applied to those on which it agrees; only a pair that agrees everywhere is accepted (§6.3). The stricter alternative applies nothing from a disagreeing pair.
- The adapter delivers a `Fill` before the terminal that reports it (§6.3); U-9 must show the native callbacks allow this.
- The day-loss stop needs a fresh P&L reading only while exposure is open or permission is `RUNNING`, and excess policy-exit close quantity after a protective fill is cancelled under any permission (§6.6, §6.8).

## 6. Shared account-risk interface

*Added 2026-10-18, revised 2026-10-19 for D-N4 to D-N6, and amended 2026-10-20 (A1) to close the reference-model card's gaps, with D-N7 to D-N9 pending (§5); same proposal status as above.* §2 states the rules; this section states the contract every account owner implements. One contract serves three uses: the NinjaScript owner (P1, P2); a pure Python reference model, the P0 oracle ([build card](../briefs/handoffs/2026-10-18-account-risk-reference-model-card-DRAFT.md)); and the offline check of exported journals (§2.7 step 7), where replaying a session's journal through the reference model must reproduce every decision, command and latch. The reference model is an offline specification and test oracle, never a service in the live execution path; passing it proves nothing about NinjaTrader or broker behavior. It generalizes the laws of the Python book reducer (`ops/c1_rail/book_capacity.py`: reserve before send, whole or refuse, partial fills move only filled quantity, a terminal must match its fills, invalid evidence adds a block and never a release) from the fixed four-leg book to configured legs and limits.

### 6.1 Roles

| Role | May | May not |
|---|---|---|
| Strategy leg | Emit intents (§6.3) for its own leg, including a request to cancel its own resting entry or add (D-N7) | Send, modify or cancel any order itself; read another leg's state |
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
| `day_loss_stop` | `⟨L-day⟩`; the binding record states the `⟨L-day-margin⟩` used, which is not a config field | §2.4 |
| `unprotected_max` | `⟨L-unprot⟩` | §2.3 |
| `disconnect_max` | `⟨L-disc⟩` | §2.5 |
| `outcome_window` | Time after a send, resize or cancel request with no acknowledgment before the order is unknown | Pilot card |
| `fact_max_age` | Maximum age of a snapshot or P&L reading used for a decision | Pilot card |
| `barrier_timeout` | How long a bar batch waits for every leg's report, from the bar's close time | Pilot card, from timing observed in P1 |

Loading rejects the configuration, and the owner stays `HALTED`, if any field is unbound, ranks are not unique, a `micro_equiv` or `point_value` is not positive, or two legs share an instrument with opposite `entry_side` or without `same_instrument` bound.

### 6.3 Inputs

Every input carries `event_id`, a strictly increasing `sequence`, `as_of`, `account_id`, owner epoch and `config_id`. An identical replayed event is a no-op; the same `event_id` with different content is a block (§6.8).

| Input | Fields | From |
|---|---|---|
| `BarReport` | `leg_id`, `bar_time` (the bar's close on the `as_of` clock), `intents[]` (may be empty) | Strategy leg |
| `EntryIntent` | `intent_id`, `leg_id`, `bar_time`, `kind` (`BASE`/`ADD`), `side`, `quantity`, `reference_price`, `stop_price`, `base_order_id` for an add | Strategy leg, inside a `BarReport` |
| `ExitIntent` | `intent_id`, `leg_id`, `quantity` | Strategy leg |
| `CancelIntent` (D-N7) | `intent_id`, `leg_id`, `order_id` of the leg's own resting entry or add | Strategy leg |
| `Ack` | `client_tag`, `order_id`, `op` (`submit`, `resize` or `cancel`) | Broker |
| `Fill` | `execution_id`, `order_id`, `quantity`, `price` | Broker |
| `Terminal` | `order_id`, `status` (`filled`/`cancelled`/`rejected`), `cumulative_filled` | Broker |
| `ProtectionState` | `order_id` (the protective order's own ID), `entry_order_id`, `state` (`working`/`rejected`/`terminal`), `terminal_status` (`filled` or `cancelled`, with `terminal` only), `quantity`, `stop_price` | Broker |
| `Connection` | `up` or `down` | Adapter |
| `Snapshot` | `source` (`A` native, `B` firm platform); `pair_id` (the pair of reads it belongs to); `watermark` (the journal sequence of the last pair the owner accepted); `positions[]` (instrument, signed quantity); `orders[]` (`order_id`, `client_tag`, instrument, kind, status `working`/`filled`/`cancelled`/`rejected`, quantity, cumulative filled); `executions[]` (`execution_id`, `order_id`, quantity, price) since the watermark | Adapter |
| `AccountPnl` | Realized plus open P&L | Adapter |
| `Tick` | `now` | Clock |
| `OperatorStart` | Session ID, GO reference, `cutoff_at` (§1 cutoff on the `as_of` clock) | Operator |
| `Restart` | `stored_permission`, `prior_epoch`, `prior_epoch_closed` (false only when the prior epoch's dirty flag is unclosed) and `session_started` (this session's `OperatorStart` is journaled), from the persisted journal tail; the first event after an owner restart, carrying the new epoch | Adapter |
| `JournalWriteFailed` | `failed_sequence`: the journal sequence of the first record that did not persist | Adapter |

**Correlation.** Every command carries a fresh `client_tag` (§6.4). An `Ack` binds that tag to the broker `order_id`. A fact keyed by `order_id` correlates only through that binding, or through a snapshot order record that carries the same `client_tag`; any other fact is uncorrelated (§6.8). A `Terminal`, or a snapshot order record applied as one, is accepted only if its cumulative filled equals the correlated fills when it is applied; otherwise the order stays non-terminal and keeps its reservation. An accepted terminal stays terminal; a later contradicting fact latches (§6.8) and does not reopen the order. An `UNKNOWN` order becomes terminal only through one uniquely correlated, accepted terminal (A12 F2).

**Snapshot pairs.** The adapter takes reads `A` and `B` as a pair and tags both with one `pair_id`. The two reads are compared when the second arrives, never with a read from another pair. A read whose pair has not arrived neither removes an instrument from the uncertain set nor verifies flat. A pair is applied for each instrument on which its reads agree, in three phases: its order records bind `order_id`s to journal `client_tag`s; its executions the journal has not seen are applied as `Fill` facts, de-duplicated by `execution_id`; then its order records are applied as `Terminal` facts. Each read covers executions since its `watermark`. A pair is **accepted** when its reads agree on every instrument; only an accepted pair advances the watermark or counts for verified flat. A pair is **taken after** an event, or after a command or latch that an event produced, when both its reads arrive later in `sequence` than that event and carry an `as_of` no earlier than it.

**Delivery order.** The adapter delivers an order's `Fill` before the `Terminal` or `ProtectionState(terminal, filled)` that reports it.

**Write-ahead.** The adapter persists each step's journal records before it releases that step's commands. If a write fails, it releases none of that step's commands and delivers `JournalWriteFailed`. Those commands count as never sent: they have no outcome window, keep their reservations, and count as unresolved requests, so verified flat stays false. After `JournalWriteFailed` the owner sends nothing at all for the rest of the session.

**Restart and epoch.** `stored_permission` is journaled and never grants authority (§1). The owner adopts the epoch the `Restart` carries, which must differ from `prior_epoch`; without a `Restart`, it adopts the epoch of the first event. Every later event must carry that epoch (§6.8). A `Restart` continues the state folded from the persisted journal; its fields summarize that journal's tail, and a §7 row with no preamble models a prior journal that holds only what its `Restart` states. A dirty start is signalled by `initial_state(dirty_epoch=True)`, which latches on the first event, or by a `Restart` with `prior_epoch_closed` false; the §7 fixture uses the `Restart`, so a replay from a clean `initial_state` reproduces it. A `Restart` with `session_started` true latches `INCIDENT` (D-N9).

### 6.4 Outputs

Before any command the owner appends the decision and the command to its journal (write-ahead, §6.3). A failed write sets the dirty epoch and sends nothing (§2.6). Every command (`SubmitEntry`, `SubmitProtection`, `ResizeProtection`, `Cancel`, `Close`) carries a fresh `client_tag`.

| Output | Meaning |
|---|---|
| `Decision` | `intent_id` (or the `OperatorStart` session ID), `ADMITTED` or `REFUSED`, reason (§6.6) |
| `SubmitEntry` | Exactly the admitted quantity |
| `SubmitProtection`, `ResizeProtection` | Stop (and target) linked to the entry `order_id`, sized to its filled quantity |
| `Cancel` | A resting entry or add (`CancelIntent`; cutoff and day-loss stop, §6.8; §6.9 item 1; §2.7 step 1); close quantity exceeding known exposure after a protective fill (§6.6, §6.9 item 5); protection only under §6.7 item 4. Never a second cancel for an order whose cancel is sent, acknowledged or `UNKNOWN` |
| `Close` | Policy exit (§2.4, `ExitIntent`) or incident close (§6.9), sized to exactly known quantity |
| `Latch` | `HALT` or `INCIDENT`, with the §6.8 condition as reason. Emitted when the latch level rises (none < `HALT` < `INCIDENT`; an unlatched `HALTED` start is level none). A later condition at or below the current level is journaled with its reason and emits no `Latch`. One event, together with the timers that expire before it, emits at most one `Latch`, at the highest level reached. Never cleared within the session |

### 6.5 State and accounting

Per order: requested quantity, fills by `execution_id`, terminal, and state `SENT → ACKED → TERMINAL`, or `UNKNOWN` once `outcome_window` passes with no `Ack`. A resize or cancel request has its own window: `Ack(op=resize)` is not coverage (§6.7 item 2) and `Ack(op=cancel)` changes no reservation; a request with neither its `Ack` nor its outcome (a `ProtectionState` at the new quantity, or a `Terminal`) within `outcome_window` makes the order `UNKNOWN`. An order is **resting** while the owner holds it non-terminal with remaining reservation above zero. Per leg: confirmed open quantity (entry and add fills minus correlated close fills and protective-order fills) and its protection.

- **Timers.** A timer of length T started at s expires on the first event or `Tick` whose `as_of` is greater than s + T. The rule is strict, so "passes", "within", "longer than" and "beyond" all mean the same. Expired timers are applied in expiry order before that event, and their outputs carry its `as_of`. The timers are `outcome_window` (from the send, resize or cancel request), `barrier_timeout` (from `bar_time`), `unprotected_max` (from the first uncovered fill) and `disconnect_max` (from `Connection(down)`). The schedule instants `cutoff_at`, flatten start (`cutoff_at` + 10 min) and `D` (`cutoff_at` + 15 min, §1) follow the same rule.

- **Reservation** of an entry or add order: requested minus filled while it is not terminal (§2.2). An `UNKNOWN` order keeps its full remaining reservation; a terminal order reserves nothing.
- **Usage** per limit: confirmed open plus every reservation, including partial, unknown and recovery-pending ones, in the limit's unit. Micro-equivalents for `cap_micro` and `instrument_cap`; legs holding confirmed or reserved quantity for `max_legs`; Σ |quantity| × |price − stop| × `point_value` for `max_open_risk`, using the fill price for open quantity and `reference_price` for reservations.
- **Permission (D-N4):** `RUNNING`; `HALTED`, which stops new risk and continues controlled risk reduction (policy exits, §6.9); or `INCIDENT`, where ordinary strategy behavior is no longer trusted and only the §6.9 procedure runs. Every session starts `HALTED`. The operator's start moves it to `RUNNING` only with a clean epoch and a verified-flat account (§2.7). Any exit or close also needs the connection up and exposure reconciled from facts fresher than `fact_max_age`. Correlated `Fill`, `Terminal` and `ProtectionState` facts are fresh when they arrive and do not age; `fact_max_age` bounds only `Snapshot` and `AccountPnl` readings (§6.2). The connection is up from a `Connection(up)` until the next `Connection(down)`; a session starts with it not up, which latches nothing. `disconnect_max` only decides when a disconnect becomes an incident; it never pauses the protection deficit clock (§6.7).
- **Verified flat** is derived (§2.7 step 5): the connection is up; the latest accepted snapshot pair was taken after the last request, the last `Connection(up)` and any latch, and is no older than `fact_max_age`; both reads show zero gross positions and no working orders; every journal request is terminal; every execution is correlated. Otherwise it is false, and a stale or missing pair raises no latch by itself. `OperatorStart` needs it. Evaluating it sends nothing; §2.7 steps 1–2 still send their cancels and exits.
- **Uncertain set:** instruments whose exposure is not known exactly. The owner sends nothing on them except cancels of its own resting entries and adds and, outside `INCIDENT`, protection for correlated fills (D-N8); they wait for the operator (§2.6). An instrument leaves the set only when its position follows exactly from correlated executions and every order on it is terminal with a uniquely correlated outcome (A12 F2), the owner's own protective order confirmed working at a known quantity by fresh facts, or the owner's own entry or add, whose `order_id` an `Ack` bound and that has never been `UNKNOWN`, confirmed working by an accepted pair at a cumulative filled equal to its correlated fills. An instrument gained from a `Connection(down)` or a `Restart` (§6.8) leaves only on an accepted pair taken after both that event and the last `Connection(up)`; facts journaled before them do not remove it. Working protection never blocks the exit and is never cancelled to clear the set. Leaving the set permits a §6.9 close; it never lifts a latch.

### 6.6 Entry admission

A bar batch for `bar_time` closes when every configured leg has sent its `BarReport` for that bar, or when `barrier_timeout` passes, measured from `bar_time` (§6.5 timers). Intents in a later report are refused `late` and journaled as missed signals; a missed signal is never carried forward. The batch is decided in `rank` order, one intent at a time, each against usage that includes every earlier admission in the batch. Arrival order inside a batch never matters. The barrier orders entry intents only: fills, terminals, protection states, exits, cancels, connection events and latches are processed on arrival and never wait for a batch (D-N4).

An intent is admitted only if every row holds. Otherwise it is refused whole, never clipped, with the first failing reason. Evaluation stops at that row, so row 7's P&L reading is needed only when rows 1–6 hold:

| Order | Condition | Refusal |
|---|---|---|
| 1 | Permission `RUNNING` | `halted` |
| 2 | `intent_id` not seen before | `duplicate` |
| 3 | Leg configured; side equals `entry_side`; no opposite position on the instrument | `invalid_leg`, `opposing` |
| 4 | An add: `adds_allowed`, and `base_order_id` has a confirmed fill on this leg | `add_without_base` |
| 5 | `same_instrument` rule satisfied | `same_instrument` |
| 6 | `cap_micro`, `instrument_cap`, `max_legs`, `max_open_risk` each hold after the request | `cap`, `instrument`, `legs`, `risk` |
| 7 | P&L above −`day_loss_stop` (a reading older than `fact_max_age` is a block, §6.8) | `day_loss` |

A refused intent has no later effect: it is not queued, retried or resized. An `ExitIntent` is refused with the first failing reason: `incident` (permission `INCIDENT`; §6.9 governs), `disconnected` (connection down), `uncertain` (its instrument is in the uncertain set). Otherwise, while `RUNNING` or `HALTED`, it becomes a `Close` only for quantity known exactly on that leg net of closes already in flight, so it cannot reverse the position. If a protective fill leaves a working policy-exit close larger than known exposure, the excess is cancelled as §6.9 item 5 does; U-17 proves the native race.

A `CancelIntent` (D-N7) is processed on arrival and never batched. It becomes a `Cancel` only while `RUNNING` or `HALTED`, only for a resting entry or add order of that leg whose broker `order_id` an `Ack` bound and that has never been `UNKNOWN` (D-N8), and only with the connection up. It latches nothing. Otherwise it is refused with the first of `incident`, `disconnected`, `not_owned` (including an order never bound by an `Ack`, or ever `UNKNOWN`), `not_resting` (terminal, or no remaining reservation) or `cancel_pending` (a cancel already sent, acknowledged or `UNKNOWN`); under D-N8 B, `uncertain` follows `disconnected`. The order's reservation is released only by its `Terminal` (§6.5).

An `OperatorStart` is `ADMITTED` only with a clean epoch, no latch, the connection up, `as_of` before `cutoff_at` and a verified-flat account (§6.5). Otherwise it is `REFUSED` with the first of `dirty_epoch`, `latched`, `disconnected`, `after_cutoff` or `not_flat`.

### 6.7 Protection ownership

1. For each entry order, the owner keeps protection whose working quantity equals that order's confirmed open quantity. Each `Fill` produces `SubmitProtection` or `ResizeProtection` to the new filled total; each correlated close reduces it.
2. Coverage counts only on `ProtectionState(working)` at the target quantity. A deficit clock runs from the first uncovered fill until coverage is confirmed. A deficit longer than `unprotected_max`, or `ProtectionState(rejected)`, latches `INCIDENT` (§2.3 item 3).
3. Strategy logic may move a stop only toward less risk; protection is never widened. Under `INCIDENT` no protection is submitted, resized upward, tightened or moved (D-N5); it is only reduced or cancelled as §6.9 allows.
4. Protection is cancelled only after fills confirm the position it covers is flat (§2.8 item 4). The cancel counts only when `ProtectionState(terminal, cancelled)` arrives; `ProtectionState(terminal, filled)` with its `Fill` is a stop fill.
5. Disconnect, strategy disable and owner restart never cancel protection (§2.3 item 5).

### 6.8 Blocks

Each condition latches as shown. No later fact lifts a latch within the session; the session ends through §2.7.

| Condition | Latch | Uncertain set gains |
|---|---|---|
| Order `UNKNOWN` (§6.5) | `INCIDENT` | Its instrument |
| `Ack` with a `client_tag` the journal does not hold | `INCIDENT` | All instruments |
| A `Fill`, `Terminal` or `ProtectionState` whose `order_id` is not bound (§6.3); a `Fill` exceeding that order's requested quantity (for protection, its size after the last resize) minus its earlier correlated fills; any fill on an order already terminal; an `execution_id` repeated with different content | `INCIDENT` | Its instrument; all instruments when the `order_id` is not bound |
| `Terminal.cumulative_filled` differs from the sum of correlated fills (the terminal is not accepted, §6.3) | `INCIDENT` | Its instrument |
| A snapshot position, order or execution the journal cannot correlate | `INCIDENT` | Its instrument |
| The two reads of one snapshot pair disagree | `INCIDENT` | The disagreeing instruments |
| Protection deficit beyond `unprotected_max`, or protection rejected | `INCIDENT` | None while the position is known exactly |
| `Connection(down)` after `OperatorStart` | `HALT`; `INCIDENT` if it lasts beyond `disconnect_max`, occurs after `cutoff_at`, or reconnect reconciliation finds a gap | Instruments with a non-terminal order at the drop, working protection included |
| P&L or snapshot older than `fact_max_age` when an admission (row 7), an exit, a close or the day-loss stop needs it. The day-loss stop needs it only while exposure is open or permission is `RUNNING`; verified flat is not such a need | `INCIDENT` | None |
| `JournalWriteFailed`; a start or `Restart` with an unclosed dirty epoch | `INCIDENT` | All instruments |
| Event under another `config_id`, account or epoch; a `Restart` whose epoch equals `prior_epoch`; conflicting `event_id` | `INCIDENT` | None |
| `Restart` with `session_started` true (D-N9) | `INCIDENT` | Every instrument with a position or a non-terminal order |
| Entry `Terminal(rejected)` with zero fills, consistent with every fact (D-N6) | `HALT`; the unused reservation is released and nothing is resent | None |
| Entry rejection with any fill, status or protection fact that is uncertain or contradictory | `INCIDENT` | Its instrument |
| A fill that would take a leg's position through zero | `INCIDENT` | Its instrument |
| `cutoff_at` reached | `HALT`; cancel resting entries and adds at once; positions keep their protection (rev9 §2) | None |
| Flatten start (`cutoff_at` + 10 min) reached, or the day-loss stop | `HALT` (the day-loss stop also cancels resting entries and adds at once), then the policy exit of every leg (§2.4); a leg whose instrument is uncertain gets its exit once it leaves the set, before `D` | None |
| A policy-exit `Close` (an `ExitIntent`, flatten start or the day-loss stop) that ends other than filled to its quantity (rev9 §4.2) | `INCIDENT` | Its instrument when the outcome is ambiguous; none when it is definitive (then §6.9 item 6 governs the one replacement, D-N1) |
| Exposure, a working order or an unresolved request at `D` (`cutoff_at` + 15 min) | `INCIDENT` | Its instrument |

Reconnect never resumes trading. After `Connection(up)` the owner reconciles from its watermark (§2.5 item 3) and stays latched. A `Restart` never restores `RUNNING`. Before `OperatorStart`, a `Connection(down)` latches nothing, because there is no risk to stop; `OperatorStart` then needs a snapshot pair taken after the reconnect (§6.5).

### 6.9 Incident close procedure (D-N5)

Under `INCIDENT` the owner ends exposure rather than repairing it. This implements §2.8 with the D-N5 policy; U-17 must still prove the native mechanism before P2 relies on it.

1. **Stop new exposure.** At once, and again whenever an `Ack` later binds one of them, cancel every one of the owner's own resting entries and adds whose broker `order_id` an `Ack` bound and that has never been `UNKNOWN`, on every instrument, including instruments in the uncertain set (D-N8). An order whose cancel is already sent, acknowledged or `UNKNOWN` is not cancelled again. Nothing else is sent on an uncertain instrument. Each keeps its remaining reservation until its `Terminal` arrives; a fill that arrives before the terminal joins the leg's known exposure and is closed under this procedure.
2. **Protection stays.** Working protection is left in place at its current price. It is resized only downward, to match confirmed closes, and cancelled only under §6.7 item 4. No new or tightened protection is submitted.
3. **Close known exposure.** For each leg outside the uncertain set, send one `Close` for the exactly known open quantity minus closes already in flight. Exposure that appears later (item 1) gets its own close on fresh facts.
4. **Partial close fill.** Reduce known exposure and protection by the filled quantity; the remainder of the close keeps working.
5. **Protective stop fills during a close.** Reduce known exposure by the stop fill, then cancel any close quantity now exceeding known exposure. If a close fill would take the position through zero, the instrument enters the uncertain set (§6.8); the native mechanism that prevents this is U-17.
6. **Close rejected or ambiguous.** After a definitive rejection or cancellation, at most one replacement close follows. It is sent on the definitive `Terminal` itself, a fresh fact (§6.5), while the position is still known exactly (§2.8 item 5). An ambiguous outcome (`UNKNOWN`, or a terminal that disagrees with fills) puts the instrument in the uncertain set; nothing is resent.
7. **Done.** A leg is closed when correlated fills show it flat and its protection is `ProtectionState(terminal)`. The session then ends through §2.7.

## 7. Deterministic scenarios

These are the interface's acceptance fixtures. The reference model must pass each; P1 runs each on the real platform (§3); each **incorrect variant** is an implementation error the check must detect. Fixture values are test inputs, not proposals for any `⟨L-…⟩`, pilot-card field or portfolio-selection value.

**Fixture:** legs `A` (rank 1, instrument X), `B` (rank 2, Y) and `C` (rank 3, Z), each `micro_equiv` 1 and `point_value` 1, long only, adds allowed on `A`; `same_instrument` `refuse`; fixed test strings for `account_id`, `instance` and each `order_symbol`. `cap_micro` 4; `instrument_cap` 4 each; `max_legs` 2; `max_open_risk` and `day_loss_stop` 10^9 account units, so neither binds; `outcome_window` 3 s; `unprotected_max` 5 s; `disconnect_max` 10 s; `barrier_timeout` 2 s; `fact_max_age` 60 s; `cutoff_at` later than every row's last event.

**Defaults**, unless a row says otherwise:
- Preamble at t = 0: `Connection(up)`, a flat snapshot pair `A` and `B` (one `pair_id`, `watermark` 0), `AccountPnl` 0, then `OperatorStart`, so each scenario starts `RUNNING`, connected, flat and unblocked.
- Bars close every 10 s from t = 0. At each bar's close a fresh `AccountPnl` 0 arrives first, and every leg the row gives no report for in that bar sends an empty `BarReport`.
- Every command is acknowledged at its send time: `op` `submit` for `SubmitEntry`, `SubmitProtection` and `Close`, `resize` for `ResizeProtection`, and `cancel` for `Cancel`.
- Each `SubmitProtection` or `ResizeProtection` is confirmed working 0.5 s after it is sent.
- An entry or add whose fills reach its requested quantity receives `Terminal(filled)` with that cumulative at its last fill.
- Snapshots a row names come as an agreeing pair.
- A starting state a row names ("X long 2 …", "PF-2 state", `INCIDENT`) is reached by ordinary admitted, filled and protected events after the preamble. An `INCIDENT` set-up uses a `Tick` under another `config_id` (§6.8), which adds nothing to the uncertain set.

| ID | Events | Expected | Incorrect variant |
|---|---|---|---|
| **Competing entries** | | | |
| CE-1 | One bar: `B` reports entry 2, then `A` reports entry 3 | `A` admitted 3 (rank 1 decided first); `B` refused `cap` (3 + 2 > 4); one `SubmitEntry` of 3 | Arrival order decides; `B` clipped to 1 |
| CE-2 | One bar: `A` 1, `B` 1, `C` 1 | `A` and `B` admitted; `C` refused `legs` | `C` admitted because micro usage 3 ≤ 4 |
| CE-3 | Bar 1: `A` 3 admitted, 1 filled, 2 working. Bar 2: `B` 2 | `B` refused `cap` (1 confirmed + 2 reserved + 2 > 4) | Only confirmed quantity counted |
| CE-4 | Preamble at t = −20; bar 0 closes at t = −10, where `A`'s entry of 1 is admitted and left working. Bar 1 closes at t = 0: `A` reports no intent and `B` entry 1 at t = 0.5; `A`'s working entry fills 1 at t = 1; `C` reports entry 1 at t = 2.5 | Protection for `A` sent at t = 1, not at batch close; the batch deadline (t = 2, strict) is applied when `C`'s report arrives at t = 2.5, before that report, and `B` is admitted; `C` refused `late` and journaled as a missed signal, never carried to bar 2 | Fill or protection held until the batch closes; batch reopened for `C`; `C` decided against stale usage |
| CE-5 | `A` add 1 whose `base_order_id` is acknowledged but unfilled | Refused `add_without_base` | Acknowledgment treated as an executed base |
| **Partial fills** | | | |
| PF-1 | `A` 3 admitted; fill 1 at t = 1; working (1) at 1.5; fill 2 at t = 2; working (3) at 2.5 | Usage 3 throughout; protection commands sized 1, then 3; no deficit beyond 0.5 s; no latch | Protection sized to the requested 3 before fills; reservation released at the first fill |
| PF-2 | `A` 3 admitted; fill 1 at t = 1; protection acknowledged, never working | `INCIDENT` at the first event or `Tick` after t = 6; new intents refused `halted`; the resting 2 are cancelled and keep their reservation until `Terminal`; no new protection is sent; one §6.9 close of exactly 1 | Acknowledged protection counted as coverage; the resting 2 left working or forgotten |
| PF-3 | `A` 3 admitted; fill `e1` of 1; then `e1` again with quantity 2 | `INCIDENT`; `X` uncertain; the resting 2 are cancelled (D-N8) and nothing else is sent on `X` | The second report replaces the first; a close or protection change sent on `X` |
| **Cancellations** | | | |
| CX-1 | `A` 3 admitted; fill 1; `A` sends `CancelIntent` for the rest (D-N7); owner sends `Cancel`; `Ack(op=cancel)`, no `Terminal` yet; next bar `B` 2 | Permission stays `RUNNING`; `A` still reserves 2; `B` refused `cap` | Cancel acknowledgment releases the reservation |
| CX-2 | CX-1, then `Terminal(cancelled, cumulative 1)`; next bar `B` 2 | Reservation 0, confirmed 1, protection stays at 1; `B` admitted (1 + 2 ≤ 4) | Protection cancelled with the entry |
| CX-3 | `A` 3 admitted; fill 1; `Terminal(cancelled, cumulative 2)` | `INCIDENT`; `X` uncertain; reservation 2 held; the order, not accepted as terminal, is cancelled (D-N8) and nothing else is sent on `X` | Terminal accepted and the missing fill assumed |
| CX-4 | `A` 3 admitted; `Terminal(rejected, cumulative 0)`; next bar `B` 1 | Reservation released; nothing resent; `HALT` (D-N6); `B` refused `halted` | Rejected order resent; rejection treated as harmless and trading continues |
| CX-5 | `A` 3 admitted; `Terminal(rejected, cumulative 0)`; then a `Fill` of 1 on that order | `HALT` on the rejection, then `INCIDENT` on the fill; `X` uncertain; the rejected order stays terminal, so no cancel is sent and nothing is sent on `X` | The late fill ignored because the order was terminal |
| **Reconnects** | | | |
| RC-1 | `A` 2 sent at t = 0, no `Ack`; `Connection(down)` at t = 1; `Tick` at t = 3.5; `up` at t = 4; snapshots `A` and `B` agree: `X` long 2, the order's record (with its `client_tag`) `filled` with cumulative 2, one execution of 2 | `HALT` at t = 1; `INCIDENT` at the t = 3.5 `Tick` (`UNKNOWN`; the window expires strictly after t = 3); after reconnect `X` leaves the uncertain set with 2 known exactly; permission stays `INCIDENT`; one §6.9 close of 2, with no protection submitted first (D-N5); no entry or resend | Reconnect restores `RUNNING`; the order is resent |
| RC-2 | As RC-1, but the snapshot pair shows `X` long 2, no record of the order and no execution since the watermark | `X` stays uncertain; the owner holds no `order_id` for the unacknowledged order, so it sends nothing on `X`; operator recovery | Owner closes 2 on the position read alone |
| RC-3 | Flat, nothing in flight; down at t = 1; `Tick` at t = 11; `Tick` at t = 11.5; up at t = 12; a flat snapshot pair at t = 12 | `HALT` at t = 1; still `HALT` at the t = 11 `Tick` (10 s, not beyond `disconnect_max`); `INCIDENT` at the t = 11.5 `Tick`; §2.7 runs and no command is sent; verified flat is false until the t = 12 pair arrives, then true | No incident because nothing was in flight; `INCIDENT` already at t = 11 |
| RC-4 | `Connection(down)` at t = 1, `up` at t = 4; then a pair whose read `A` shows no working orders and whose read `B` shows a working order on `Y` absent from the journal | `HALT` at t = 1; `INCIDENT`; `Y` uncertain; no command is sent; flat not verified (§2.7 step 5) | Snapshot `A` alone accepted |
| RC-5 | No preamble. (a) A new session boots: `Restart` carries a stored `RUNNING` from the prior session, `session_started` false and a clean epoch; then `A` reports entry 1. (b) `Restart` carries a stored `RUNNING`, `session_started` false and `prior_epoch_closed` false; then `OperatorStart`. (c) `Restart` carries `session_started` true and a clean epoch; then `OperatorStart` | (a) Permission stays `HALTED`; `A` refused `halted`. (b) `INCIDENT` on the `Restart`, every instrument uncertain; `OperatorStart` refused `dirty_epoch`. (c) `INCIDENT` latched (reason `restart`, D-N9); `OperatorStart` refused `latched` | Stored `RUNNING` honoured; (c) a restart after the start latches nothing or only `HALT` |
| RC-6 | `X` long 2 with protection working at 2; `Connection(down)` at t = 1; `A` `ExitIntent` 2 at t = 2; `up` at t = 4; `A` `ExitIntent` 2 at t = 4.5; a snapshot pair at t = 5 agrees: position 2 correlated, protection working at 2, no other orders | `HALT` only (3 s, not beyond `disconnect_max`); the exit at t = 2 refused `disconnected`; the exit at t = 4.5 refused `uncertain` (no pair yet after the reconnect); after the pair `X` is known exactly despite its working stop; protection untouched; a new `ExitIntent` after reconciliation becomes a `Close` of 2; no entries | `X` held uncertain because its stop is not terminal; protection cancelled to clear it; exit sent while down or after the reconnect before the pair; `RUNNING` restored |
| **Incident close (§6.9)** | | | |
| IC-1 | PF-2 state: close of 1 working, cancel of the resting 2 sent; one of the 2 fills before `Terminal(cancelled, cumulative 2)` (cumulative counts both fills) | Known exposure becomes 2; a second close of 1 follows on that fill; reservation 0 after the terminal; protection never resized upward | The late entry fill dropped, or protected instead of closed |
| IC-2 | `X` long 2, protection working at 2, `INCIDENT`; close of 2 sent; the stop's `Fill` of 2, then its `ProtectionState(terminal, filled)`, before the close fills; then a close fill of 1 arrives | Known exposure 0; the close is cancelled; the late close fill takes `X` through zero, so `X` enters the uncertain set and nothing more is sent on `X` | Close left working; a fill through zero treated as normal |
| IC-3 | `X` long 1, `INCIDENT`; close of 1 rejected definitively; replacement also rejected; then a fresh snapshot pair still shows long 1 | Exactly one replacement close, sent on the first rejection; after the second rejection nothing is sent, on the later snapshot pair included, and `X` waits for the operator, outside the uncertain set because both outcomes were definitive; protection stays working | A third close; protection cancelled |
| IC-4 | `X` long 1, `INCIDENT`; close of 1 sent at t = s with no `Ack`; `Tick` at s + 3.5 | `X` enters the uncertain set; nothing resent; protection stays working | Close resent |

Every scenario also asserts that each command follows its journal record, and that replaying the journal through the model reproduces the same decisions, commands and latches.
