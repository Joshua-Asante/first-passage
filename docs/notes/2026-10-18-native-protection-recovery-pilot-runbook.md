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
| Incident → durable halt, intervention, no runtime close/cancel/amend (rev9 §1, §3; A12 F1(c)) | Kept for the pilot. On an incident the owner latches HALT and sends nothing more; the operator recovers in the platform. Platform auto-close on error is not admitted (D-N1). | No (pilot) |
| Policy exits: scheduled cutoff and own-flat deadline under SCHEDULED_EXIT (rev9 §1, §5) | Kept, and the account loss stop joins them as a policy exit (§2.4). Any incident revokes this authority. | Adds the loss stop |
| Unknown outcome → hold reservation, halt; release only on unique correlation (A12 F1–F3) | Unchanged. Correlation uses broker order ID and execution ID, never signal name or timestamp. | No |
| Unexplained position, order or fill is an incident (A12 F5) | Unchanged, on every instrument in the account, including fills the owner did not request. | No |
| No same-session restart after an incident (A11.2) | Unchanged for the pilot: one session, then review. | No |
| Recovery complete only on fresh, coherent, postdating evidence (rev9 §3) | Two independent reads are required: the native account view and the firm platform's own view (§2.7). | Adds a second source |
| Schedule `D = min(16:00 ET, V − 15 min)` (rev9 §5) | `D = min(16:00 ET, V − 15 min, W_end − ⟨L-attend⟩)`, where `W` is the operator's attended window. Cutoff `D − 15 min`, flatten start `D − 5 min`, as before. | Adds the attendance bound |

## 2. Rules for the pilot

### 2.1 Simultaneous strategy entries

1. One account owner hosts every selected leg for that account, with a fixed leg priority. Separate strategy instances sharing one account are not admitted: their positions are tracked separately, so the account can net flat or reverse while each instance still holds protective orders.
2. Signals that complete on the same bar are admitted in priority order, one at a time. Each admission sees every earlier reservation from that bar.
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
5. A disconnect that outlasts `⟨L-disc⟩`, or that occurs after cutoff, goes to attended recovery: the operator acts in the firm platform.

### 2.6 Uncertain account state

The owner enters `UNRESOLVED` (packet §12.1 states) and sends nothing when any of these holds: unknown request outcome; an uncorrelated fill, position or order; a protective order of unknown state; account P&L or position evidence missing or stale; a journal write failure; or a start with an unclosed dirty epoch. Exits wait for the operator. Fresh evidence alone never lifts the state: release follows A12 F2 and the halt ends only through §2.7.

### 2.7 Verified flat shutdown

Run at the planned end, after an incident, or at `D`, whichever comes first:

1. Owner latches HALT; resting entries are cancelled at cutoff (policy) or left for the operator (incident).
2. Policy exits, or the operator's platform flatten, bring every leg flat.
3. **Read A (native):** account positions, working orders and executions for every instrument on the account, postdating the last request.
4. **Read B (independent):** the firm platform's web view of the same account. The native order grid hides prior-day orders after rollover, so read A alone cannot prove no working orders.
5. Flat is verified only when both reads show zero gross positions, no working orders, and no unresolved request; every journal request has a terminal outcome; and every execution is correlated. Net zero, an empty grid, elapsed time or acknowledgment does not count (rev9 §3).
6. Then: disable the strategy, disconnect, set the connection not to connect on startup, and check the platform's saved workspace (it is rewritten on exit). Record each step's evidence.
7. Export the journal and both reads to authorized custody. Python compares offline.

If step 5 fails, HALT stays and the account stays under attended recovery past the planned end (rev9 §3, attendance).

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
| U-5 | Error-handling setting causes no automatic close or cancel on a rejection (D-N1) | Reject an entry, an add and a protective amend | O1 |
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

## 5. Open decisions

- **D-N1 (operator):** keep rev9's no-runtime-incident-mutation posture for the pilot (recommended: the auto-close path is unproved, U-5), or admit a native bounded risk-reducing exit as packet §12.1 proposes, after U-3, U-5 and U-9 pass.
- **D-N2 (portfolio selection):** leg priority, same-instrument handling, and every `⟨L-…⟩` value.
- **D-N3 (firm admission):** whether one owner hosting several strategies is permitted on the selected firm's account, and whether its hedging and news rules constrain §2.1.
