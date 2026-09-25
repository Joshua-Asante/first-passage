# TradingView signal route evaluation — 2026-09-25

Status: documentary and source-code evaluation, not a route approval or implementation design. Requested by Joshua in the T08 vendor-question task. No account access, alert creation, webhook transmission, strategy change, qualification draw or deployment was performed.

## Verdict

**TradingView is a credible alternative signal host, but the unmodified four-strategy book is not a drop-in webhook deployment.** It could remove live Pine-to-Python signal translation and the separate signal-feed daemon. It does not remove the portfolio account owner, execution reconciliation, broker protection requirements, or portfolio qualification.

The strongest new blocker is the mismatch between Pine's simulated position and the account owner's confirmed position. Resolve that before building a TradingView ingress adapter. The August signal-host ADR states reasons for preferring Python but does not supply a measured comparison sufficient to dismiss this alternative today.

The route worth assessing further is:

`Pinned Pine alerts → durable TradingView ingress → existing typed book account owner → qualified CrossTrade adapter → Tradovate`

“Existing listener” means retaining our control boundary, not sending the book through the current legacy B1 handler. That handler explicitly refuses fixed-book mutations.

## Evidence and limits

Local baseline: `1c5c08213f7edad9b7480fceddc075f2252bea22`. Read the current HTTP handler, listener, payload sender, book policy, adapter registry, book protocol and runtime. Under Rule 0, read production controls before making control-boundary claims. No sizing constants are proposed here.

All four private Pine sources in the operator's Downloads directory were SHA-256 checked against `ops/c1_signal_daemon/book_adapters.py`; all four match. Relevant order, alert and position-management sections were inspected. Source bodies and parameter values are not reproduced here.

| Source file | SHA-256 |
|---|---|
| `aegis_6J1_venue_bound.pine` | `db78ecba95ae78aca14501a5eaccfda2a42164d83cac12321cb7f293a9adca7c` |
| `striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` | `712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7` |
| `Vanguard_Gold_MGC_v0.4_venue_bound.pine` | `af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15` |
| `orb_mnq_7_reconstruction_venue_bound.pine` | `176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3` |

The private reconstructed historical effective-input file hashes to `66406dee955fa69f237fde60eacdd24259a08d5320352d98e59889acaa18158d`. It is historical parity evidence, not a current alert manifest. Current TradingView UI settings, subscription, data entitlements and running alerts were not inspected. No live latency or delivery reliability was measured. This evaluation proves neither economic equivalence nor production readiness.

The brainstorming skill was consulted; its read-only feasibility exclusion applies. This note is an evaluation, not an approved design. Verification follows the verification-before-completion skill: source inspection and document checks only, with no runtime-test claim.

## What improves and what remains

| Concern | TradingView through our account owner | Python signal host |
|---|---|---|
| Live signal implementation | Pine runs on TradingView; removes one live port boundary | Private ports need maintained parity |
| Signal data and hosting | TradingView supplies the chart runtime; entitlements, continuous-contract mapping and data equivalence still need evidence | We supply the feed adapter, warm-up, continuity and daemon operations |
| Broker execution feedback | Critical unresolved interface: Pine simulates its own fills | Existing strategy protocol explicitly consumes confirmed outcomes |
| Portfolio policy and shared capacity | Account owner still required; four independent chart quantities cannot replace it | Already modeled in shared owner/policy modules |
| Protection and unknown requests | Same downstream CrossTrade/Tradovate limitations | Same limitations |
| Qualification | Historical exports help; path-dependent portfolio replay and final account-bound checks remain | Existing qualification/replay work remains relevant |
| Operations | Alert snapshots, replacement, expiry/runtime failures and delivery monitoring | Feed failures, daemon restart and state restoration |

No defensible calendar-time or dollar saving can be quoted yet. Avoid treating sunk implementation effort as a reason to retain Python, or treating existing TradingView research access as proof that live entitlements are free and ready.

## The decisive distinctions

### 1. A simulated fill is not a broker order instruction

TradingView distinguishes explicit `alert()` events from strategy order-fill events. Fill events come from its broker emulator; they do not certify actual Tradovate execution. Alerts operate in realtime and use a saved script/input/chart snapshot. Existing snapshots must be recreated to pick up relevant changes. [TradingView alerts documentation](https://www.tradingview.com/pine-script-docs/concepts/alerts/)

For ORB, waiting for a simulated stop-entry fill and then sending a market order changes the resting-stop execution path. Likewise, waiting for a simulated trailing exit and then sending a close does not provide the native protective order the current contract requires. Those alternatives may be evaluated as changed expressions, but cannot be declared equivalent by connecting webhooks.

### 2. The source files have different alert interfaces

| Leg | Direct source observation | Consequence |
|---|---|---|
| Striker | Explicit B1 entry/add/flat alerts; legacy leg identity; realtime tick recalculation enabled in the source declaration; protection updates are separate strategy operations | Needs identity/schema work and timing review. The emitted stream is not a complete typed protection lifecycle. |
| ORB | Stop-entry placement, cancellation and trailing bracket operations; no explicit `alert()` or custom `alert_message` in the inspected file | Generic fill alerts are available, but do not communicate all order creation/cancellation/amendment intent. |
| Vanguard | Entry/add and evolving bracket operations; no explicit `alert()` or custom `alert_message` in the inspected file | Same interface gap; active trailing/grace settings must be bound to the approved effective configuration. |
| Aegis | Custom fill messages use a different vendor-style template; bracket/breakeven updates; some close-all paths have no custom message | Existing payloads cannot simply be pointed at our typed owner; every exit path needs explicit coverage. |

Source edits are not authorized by this evaluation. A separately pinned alert-capable expression would need a review showing whether changes are instrumentation-only or change the strategy. Keep the locked originals unchanged.

Striker's tick setting is a specific parity risk, not a proven live defect. TradingView documents that realtime tick execution can differ from historical execution and repaint after reload. The actual saved alert properties must be inspected; silently switching to bar-close operation would change behavior. [TradingView strategy calculation documentation](https://www.tradingview.com/pine-script-docs/concepts/strategies/)

### 3. Account policy changes the state Pine thinks it is trading

`book_protocol.py` requires position-dependent adapter state to advance from confirmed outcomes. `book_runtime.py` delivers and persists that feedback. Pine sources instead inspect their simulated position, fills and average price.

Concrete counterexample: Pine simulates a base entry, but our account owner refuses it for capacity. Pine later emits an add or exit for that simulated trade. We can suppress an orphan command, but that alone does not restore the strategy's future entry timing, counters or state. Similar divergence follows partial fills, a broker-native stop firing before Pine's simulated stop, an Aegis takeover, scheduled flatten or manual recovery.

No supported way to inject our arbitrary broker feedback into these running Pine strategy instances was established in this evaluation. Do not assume one. The next design must either prove that shadow Pine state produces an equivalent accepted strategy after every such divergence, or define and qualify changed semantics. Manual alert recreation after every divergence may be an operating option, but its frequency and correctness are unmeasured.

The following source-level counterexamples establish why unchanged forwarding fails. These are static traces, not executed trading tests:

| Leg | Source state after its own simulated trade | Divergence if the account did something different |
|---|---|---|
| Striker | Entry sets local entry/stop/base-size state; later add logic uses that state and the simulated position | A refused base does not undo those assignments. Suppressing its later add protects the account but does not recreate the accepted feedback-driven strategy state. |
| ORB | Stop order can fill in the emulator; later management uses simulated position and average price | A broker miss or earlier broker stop leaves Pine managing a different trade. Forwarding an eventual simulated exit requires real residual-position ownership to avoid an unrelated action. |
| Vanguard | Entry assigns base quantity and trade state; simulated average price drives adds; the grace-stop clock advances locally | A refused or partial base changes the real eligible add and protection state without changing those Pine variables. |
| Aegis | Entry requires a simulated flat position; entry state and daily count advance locally; breakeven and timed exit use that state | A refused entry can consume the Pine opportunity and leave it simulated-open. Account-side takeover or an early close cannot itself reset the running Pine instance. |

For the shared cases: changing admitted size can be translated at execution, but does not prove that later Pine decisions remain identical; a rejected add can change real versus simulated average price; scheduled/manual close leaves a stale Pine position; a lost entry alert permits the emulator to advance with no account entry. None is repaired merely by putting a native stop on the eventual broker order. Therefore **unchanged Pine forwarding fails the current confirmed-feedback contract at the interface level**. What remains undecided is whether a deliberately different shadow-signal contract is economically acceptable and cheaper to qualify.

### 4. HTTP compatibility is necessary but insufficient

The legacy `c1_rail_listener.py` fixed-book guard rejects all four book IDs, including exits. Its legacy payload builder and sizing path are not a substitute for the typed durable owner. That guard must not be removed as a shortcut.

The HTTP handler waits for `handle_signal`; the CrossTrade sender has a ten-second timeout. TradingView cancels requests that take more than three seconds and acknowledges that deliveries can fail. Thus a quick, durable intake acknowledgment needs evaluation; the current synchronous handler cannot be assumed suitable. [TradingView webhook constraints](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/)

TradingView documents up to three resends at five-second intervals on 5xx responses other than 504. It does not thereby promise retries for every timeout or loss. Intake needs stable event identities, durable duplicate suppression, payload-conflict rejection, freshness checks and crash recovery before any broker dispatch. A received acknowledgment would mean durable intake only. [TradingView resubmission rules](https://www.tradingview.com/support/solutions/43000735201-webhook-resubmission/)

A future ingress queue must also have a locally enforced dispatch deadline: adding our own queue must not create another indefinite deferred-entry source. Local expiry cannot cancel a request already sent downstream.

### 5. Hosting moves; responsibility does not disappear

A proposed alert manifest should bind source digest, effective inputs/properties, symbol, timeframe, session/roll conventions, alert event mode and release identity. The receiver should admit only the active release and reject old alert versions. Creation/replacement remains operator-driven under the current prohibition on TradingView login/actuation automation.

The documented script-alert frequency halt and runtime-error behavior require a traffic budget and detection procedure. Trade silence is not proof of a healthy alert. Per-bar completion/no-signal messages may support the book's common decision boundary, but need explicit instrumentation and cannot bypass alert limits or manufacture missing bars. [TradingView alert FAQ](https://www.tradingview.com/pine-script-docs/faq/alerts/)

In particular, preserving same-bar portfolio priority cannot mean processing whichever of four independent webhooks arrives first. Missing, late and conflicting leg messages need a defined outcome. Scheduled flatten should retain an independently monitored account-side owner; it cannot rely solely on the arrival of another Pine tick.

### 6. CrossTrade's capabilities do not change with the sender

Current CrossTrade documentation still describes first-fill-sized native brackets with later-fill coverage repair, and separates native continuous trailing from CrossTrade-managed triggered trailing. These distinctions remain relevant to T08. [CrossTrade destination matrix](https://crosstrade.io/docs/webhooks/destinations)

Direct TradingView requests to CrossTrade are acknowledged before background processing finishes; that success is not fill confirmation. In the evaluated route, our own listener remains CrossTrade's HTTP client, so the vendor question already sent still addresses the relevant downstream uncertainty. [CrossTrade webhook documentation](https://crosstrade.io/docs/api/webhook-trading)

Keep [T08](../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md) and the [proposed incident amendment](../adr/2026-09-17-bounded-platform-protection-incident-contract.md) as the owners of downstream findings. This evaluation does not promote their documentation-only findings to qualified capability.

## Alternatives and recommendation

1. **TradingView → CrossTrade directly:** not recommended for this accepted portfolio. It bypasses our shared admission, confirmed-position ownership and reservation controls. Simpler single-strategy examples do not demonstrate equivalent portfolio behavior.
2. **TradingView → typed account owner → CrossTrade:** strongest alternative worth pursuing. Retains the portfolio controls while potentially eliminating live signal-port/feed work. Conditional on event completeness and the simulated-versus-confirmed-state problem.
3. **Python host → typed account owner → CrossTrade:** remains the approved baseline. Better aligned with confirmed feedback and deterministic replay, but carries feed and port operational work. It also remains blocked by downstream capability questions.

Recommendation: **do not approve a production cutover of the unchanged book.** Option 2 is worth a bounded design comparison only if the operator is willing to consider a different shadow-signal/feedback contract and its requalification burden. This is not a conclusion that Python wins. The source check rejects the easy-swap hypothesis and identifies the exact question on which the comparison turns.

## Next evidence boundary

The documentary evaluation above returns **requires a specifically identified contract/requalification decision** for option 2; **not viable as an unchanged drop-in**. A follow-on design would compare a shadow-Pine signal contract against retaining confirmed-feedback Python execution, with one reviewable outcome: an explicit event/state contract and its qualification cost. This is a proposed next assignment, not a new authorization for implementation, broker drills or alert activation.

Required cases:

1. Entry placed versus emulator-filled: stop entry, bracket creation, cancellation, amendments, trailing activation and every forced exit all have an explicit event meaning.
2. Refused entry, changed admitted quantity, partial fill, rejected add, broker-first exit, takeover and scheduled flatten: subsequent Pine behavior either matches the accepted state machine or the exact economic change is identified.
3. Simultaneous four-leg boundary: same priority and missing-leg behavior regardless of webhook arrival order.
4. Duplicate, late, conflicting and lost messages, receiver crash after durable intake and before dispatch, and stale alert revision: no duplicate or stale broker action; retained unresolved outcomes.
5. Frozen historical configuration versus actual realtime settings: original source identity and effective properties reproduced; historical-only parity is not passed off as forward evidence.

Return **viable for design**, **requires a specifically identified contract/requalification decision**, or **not viable for the unchanged book**. If no credible answer exists for case 2, stop before investing in an ingress adapter. If the documentary cases pass, propose an operator-created, capture-only forward comparison with no broker sender; real account/drill actions remain separately gated.

The vendor answer can arrive independently. A favorable answer does not discharge this event/state boundary. A route change would require an explicit amendment to the S2 signal-host decision, relevant feedback/source contracts and the qualification freeze inventory; it does not erase completed historical M1 evidence.

## Follow-up investigation — the retained account-owner route

Requested in the same task on 2026-09-25. This section records interface findings and candidate semantics for discussion, not an approved implementation specification.

### What the existing owner actually provides

Read `book_account_owner.py` methods `make_occurrence`, `dispatch`, `_dispatch_locked`, `record_local_refusal`, `commit_feedback`, and `_context`; `book_runtime.py` completed-bar dispatch and feedback delivery; `book_protection.py` occurrence validation; and each private port's execution handler.

- An occurrence binds account, account epoch, session, producer, event ID and ordinal. Repeated occurrences with different action bodies trigger a conflict; retained outcomes and attempts govern repetition. Reuse this mechanism rather than inventing broker idempotency from a webhook label.
- Supported producer values are currently `runtime`, `schedule`, `takeover`, `mode`, and `direct`. There is no registered TradingView producer. A future bridge must define its provenance explicitly, not disguise alerts as runtime output without a reviewed mapping.
- The owner constructs sizing context from confirmed base evidence and account bindings. Incoming Pine quantities cannot silently replace that context.
- The runtime collects all four leg bars, records the boundary and ordered actions, dispatches them, then delivers retained fills/refusals and checkpoints local adapter state. An HTTP call to `dispatch` alone does not replace that whole lifecycle.
- The private ports maintain fill-derived lots, position and, where used, average-price/equity calculations. Some other strategy counters and variables advance while generating intents. Thus the comparison must preserve the actual state transitions; neither “all state is fill-driven” nor “just update position size” accurately describes them.

These are code capabilities, not evidence that a real broker adapter is qualified. T09 remains a separate dependency.

### Two possible meanings of Pine as the signal source

**A. Follow Pine trade cycles.** Pine retains its complete simulated strategy. A local bridge maps each simulated trade cycle to admitted real operations and residual fills. A rejected base marks the whole cycle skipped; its later adds/amendments/exits cannot create or affect unrelated exposure. Once a real position has closed, the bridge must not reopen it merely to match Pine's still-open simulation. Broker unknowns remain unresolved incidents, not skipped cycles. A new cycle is eligible only after its identity and prior-cycle disposition are established.

This is a coherent proposal, not equivalence to the accepted book. It can deliberately miss later opportunities while Pine waits for its simulated trade to end. Partial fills and rejected adds can make later Pine thresholds depend on the wrong average price. CrossTrade's native-protection limitations still apply. Requalification must model the cycle-following rule and the resulting opportunity set explicitly.

**B. Pine supplies market conditions; a local strategy-state component uses actual execution.** Pine emits eligible market setups, required indicator values and complete decision-boundary messages without withholding them because its simulator thinks it has a position. Local strategy-state code handles fill-dependent entry eligibility, adds, protection and exits using the owner's confirmed outcomes. The owner retains account-wide admission and dispatch.

This better preserves the existing feedback direction but retains part of the Python strategy implementation. It is not just a generic ingress adapter, and it does not guarantee elimination of a separate data source: every value required between alerts, for protection, restoration and missing-input recovery must be accounted for. The exact partition needs a per-leg dependency map and parity evidence. Original Pine files remain immutable; any publisher expression gets its own identity and review.

**Assessment:** A maximizes removal of local strategy logic at the cost of an explicit behavior change. B is the better candidate when preserving the accepted portfolio is the priority. Neither is presently a proven cheaper route. A magic two-way webhook that synchronizes Pine with broker fills is not an established third option.

### Minimum transport boundary under either interpretation

The proposal requires authenticated, release-bound intake, durable storage before a quick acknowledgment, stable event identity across resends, and separate receipt versus execution status. The configured endpoint binds the account; a payload's claimed source hash is metadata, not authentication. Credentials and payloads must be redacted from public evidence.

Retain raw events and canonical typed actions separately. Identity needs enough scope to distinguish multiple legitimate actions in one bar; `{leg, bar_time}` alone is insufficient. Missing sequence members, conflicting duplicates, old source generations and expired intents have explicit refusal/recovery outcomes. Do not automatically execute a backlog after receiver recovery.

Pine must supply enough events to distinguish a no-signal bar from a missing leg, and enough order intent to distinguish placement, modification, cancellation and a simulated fill. Four-leg priority needs a completed-boundary rule. Intrabar events cannot simply be delayed to a bar-close batch without a timing-equivalence decision. Broker facts continue entering through the observation path, never through a Pine assertion of a fill.

### Concrete traces the comparison must resolve

| Event | A: follow Pine cycle | B: market conditions plus local strategy state |
|---|---|---|
| Base refused | Suppress the remaining cycle; accept altered opportunity timing | Local strategy handles its recorded refusal; future eligibility follows reviewed local rules |
| Base partially filled | Map only confirmed lots; define treatment of later shadow-based thresholds | Use confirmed quantities/prices, subject to qualified protection and partial-fill rules |
| Add refused | Never compensate with an extra order; shadow thresholds may diverge | Preserve the accepted add-refusal state transition |
| Real stop or scheduled close precedes Pine exit | Retire real exposure; suppress stale cycle commands, without reopening | Apply confirmed close to local state; subsequent proposals use that state |
| Downstream request unknown | Preserve reservation/block and incident obligations | Same |
| Alert missing or receiver restarts | No inferred flatness and no stale catch-up orders | Same; local state restoration also requires the missing input/feedback policy |

### Recommended decision boundary

If the objective remains this accepted portfolio, prefer investigating B's exact per-leg partition before implementing ingress. If minimizing local strategy code takes precedence, A must be treated as a changed execution expression and receive an explicit qualification decision. An inexpensive capture-only comparison can measure delivery and event coverage later, but cannot by itself prove either behavior under real fills or qualify native protection. No implementation, new alert, broker action or contract amendment was made by this follow-up.

## Per-leg partition — source inspection follow-up

Static feasibility analysis at revision `1c5c08213f7edad9b7480fceddc075f2252bea22`; this is a candidate partition, not an approved event schema or equivalence finding.

**Initial identity limitation, resolved in the follow-up below:** fresh SHA-256 checks matched all four Pine pins and the Aegis, Vanguard and ORB runtime pins. The default local `ports/dj30_mym_p250.py` instead hashes to `c81aa59c811dd2f318bf2f6b51e9df32fca20315ffab0885ec1d4ec6a2ab5379`, the preserved original explicitly rejected by the registry. The accepted Striker runtime pin is `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4`. The subsequent protection-map investigation located and inspected matching bytes in retained private evidence; the default port remains unchanged.

| Leg | Candidate Pine responsibility | Retained local responsibility | Required market information |
|---|---|---|---|
| Striker | Breakout, volatility expansion, candle and session filters, independent of simulated holdings | Entry eligibility and counters; signal-time entry/ATR references; add, breakeven, trailing and holding-duration state; actual exposure and realized outcomes. Accepted bytes inspected in the follow-up below. | Raw eligible setup, close, ATR and decision time, including observations while a real position is open; realtime versus completed-bar cadence remains unresolved. |
| Vanguard | Trend/recovery setup and ATR under the effective configuration | Actual position and average price for adds; signal-time entry/stop/target references; base-size reference, add count, grace-stop clock, protection and timed exits | Raw setup, high, close, ATR and boundary/session identity on every relevant bar, not only entry bars |
| ORB | Opening-range bounds, volume participation and market/session boundaries | Once-per-session placement state; pending stop-entry identity and cancellation; actual holdings; bracket lifecycle and holding clock. Preserve the accepted adds-off binding rather than copying source defaults. | Range bounds, range-completion event, eligibility, high/low/close and session identity; continuing boundaries for management and expiry |
| Aegis | Reciprocal-price series, band/volatility calculations and market filters | Daily opportunity count; signal-time synthetic entry/ATR reference; actual holdings; breakeven latch, target re-pin and holding clock | Raw setup, synthetic close/high, ATR, current band basis or target candidate, and boundary identity throughout the trade |

Evidence anchors: pinned Pine Striker signal/management blocks (lines 162–183 and 285–365), Vanguard (282–297 and 441–526), Aegis (647–707), and ORB opening-range/entry/management blocks; matching private ports' `on_bar` and `on_execution`; public `book_account_owner.py::_context`. Values and executable strategy bodies are intentionally not copied into this public note. Optional Pine branches are not assumed active merely because they exist in the source.

### Preserve three different kinds of state

1. **Market state:** rolling indicators, ranges and raw setups can be computed in Pine without its simulated position gating publication.
2. **Decision state:** some entry references and counters advance when the local strategy proposes an order. In the matching Aegis and Vanguard ports, non-fill execution events return without undoing those assignments. A refused base therefore does not imply a refunded daily opportunity. Vanguard's add counter likewise advances during proposal generation. Changing these to fill-time transitions would change the strategy.
3. **Execution state:** confirmed lots and, where referenced, their average price come from broker outcomes through the owner. Preserve signal-time references separately: replacing every entry price with a broker fill price is not a neutral correction.

This narrows the earlier phrase “local strategy handles its recorded refusal”: the owner retains refusals, but these inspected strategy handlers do not generically roll decision state back on refusal. A publisher must continue reporting market conditions; local eligibility can still intentionally suppress a later entry because its existing counter was consumed.

### What this can remove, and what remains unproved

The partition can move rolling indicator computation and chart-history warm-up to Pine. It retains strategy-specific management code, decision-state persistence, execution reconciliation and shared account policy. It also replaces a direct market-data input with an alert-delivered market-data input; it does not eliminate data continuity requirements.

The decisive remaining feed question is protection between messages. Completed-bar highs/lows do not establish the intrabar order of stop, target and trail events. Either the qualified broker route implements the required protection semantics, or another timely observation mechanism remains necessary. Source inspection alone cannot establish that TradingView alerts eliminate a separate feed.

Before treating this as an implementable split, compare identical market observations plus identical execution/refusal histories against the accepted adapters. Required comparisons include consumed opportunity counters after refusal, signal-price versus fill-price references, rejected adds, partial fills, broker-first closes, ORB pending-order cancellation and restart. Separately establish protection timing and missing-message recovery. Striker byte recovery is completed below; behavioral comparison remains owed. This comparison is the next evidence boundary, not implementation or activation authority.

Verification here used PowerShell source reads and `Get-FileHash`, plus registry comparison. No Python, runtime tests, live interfaces or delivery measurements were run. The result supports a candidate dependency partition only; it does not establish full partial-fill/restart correctness of the existing ports or the proposed split.

## Between-alert protection map — 2026-09-25

Operator-directed follow-up: identify protection inputs and their owners between alerts, and recover the accepted Striker source. The route remains a candidate. This map targets the accepted completed-bar Python interface; it separately flags where realtime Pine has a different calculation cadence.

### Striker source recovered and verified

The retrieval pointer already exists in [T10 source reconciliation](2026-09-21-t10-phase1-source-reconciliation.md) and [T00 P7 closure](../briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md). Read the retained file at:

`lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/step3-coverage/corrected-ports/dj30_mym_p250.py`

`Get-FileHash -Algorithm SHA256` returned `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4`, exactly the registry pin. Read `on_bar`, `on_execution`, `_equity` and the state helpers in these bytes. No copy, overwrite, import or execution was needed. The historical effective-input file also freshly matches its registry digest. This closes source availability for this analysis; it is not a new parity acceptance or verification of a running host.

### Dependency map

“Between alerts” below means between complete market-input boundary messages. Broker observations and local timers must operate independently of those messages.

| Decision / operation | Inputs and exact timing dependency | Candidate owner; remaining evidence |
|---|---|---|
| Striker base protection starts | Accepted `on_bar` emits its base with `bracket=None`. Position is sampled before dispatch; the later position-management branch emits the bracket only when a subsequent evaluation sees exposure. The emulator's `_amend` explicitly documents this delayed attachment. | Local strategy plus broker protection lifecycle. An immediate entry stop is a behavior/timing change requiring reconciliation with the live contract; do not silently derive and attach one from sizing stop distance. This is a structural gap, not proof of an exposed live account. |
| Striker breakeven, trail tightening and ratchet | Signal-time entry price/ATR, current completed-bar close, stored latches and actual position; branch ordering matters, including selecting trail distance before updating the tightening latch. | Local strategy computes amendments at the accepted bar boundary. No additional tick input is needed for these calculations under that interface. Once installed, the stop/target must execute between messages at the broker. |
| Striker DD and daily halt behavior | Confirmed realized outcomes, mark-to-market using the current bar close, daily/session anchors and decision counters. The effective override enables its non-backtest rail branches. | Local strategy retains this clock and accounting; broker fills arrive independently. Turning these into continuous quote-driven limits changes the accepted evaluation cadence. Shared account policy remains separately owned. |
| Vanguard fixed stop/target and adds | Signal-time entry/stop/target references; completed-bar high and confirmed average price for add eligibility; each new fill needs the applicable bracket. | Local decisions plus broker order/fill observation and per-fill protection. Current effective defaults enable trailing; breakeven is off and the grace delay is zero, so those optional branches are not active dependencies in this binding. |
| Vanguard triggered trailing | Each fill's price, activation distance, subsequent favorable price path and ratcheting extreme; state survives repeated bracket amendments. | Intrabar execution engine, ideally qualified native protection. A completed-bar alert cannot reproduce a trail activation and reversal that already happened. Pine's simulated fill price cannot substitute for the real fill reference. |
| ORB resting entry and fixed protection | Opening-range completion places a pending stop entry; the market can reach it between alerts. Trigger/fill, attached stop/target and cancellation outcome must be observed independently. | Broker trigger and protection engine plus local pending-order owner. A Pine simulated-fill alert is too late to represent original stop placement. |
| ORB triggered trailing | Per-fill entry reference and ordered favorable/adverse price movement, including activation followed by reversal within a bar. | Same unresolved intrabar owner as Vanguard. Adds-off does not remove the base position's trail. Under adds-off, the port's stall-exit condition is also disabled; do not invent a stall action from source defaults. Breakeven is off in the inspected effective binding. |
| Aegis breakeven and target re-pin | Completed-bar synthetic high, stored signal-time synthetic entry/ATR, and current band basis/ATR for the target re-pin; actual exposure gates management. | Local strategy at the completed-bar boundary. This is not a generic tick-triggered broker breakeven rule. The existing bracket executes between alerts; the updated stop and target require a qualified amendment. |
| All legs: fill, partial fill, add fill, stop/target execution | Execution identity, quantity, price, affected fill/order, remaining exposure and actual working protection; these can change before another market alert. | Broker observation path and typed owner, independent of Pine. Protection coverage and residual-order reconciliation cannot wait for the next bar or rely only on aggregate position reads. No correctness claim for every existing partial-fill path is made here. |
| Holding clocks, session cutoff, pending-entry expiry, source silence | Retained bar sequence for strategy bar-count clocks; bound calendar and independent wall clock for operational cutoff/deadlines; pending orders and confirmed exposure. | Local strategy plus independently scheduled account controls. Missing bars must not be fabricated to advance strategy time. An operational deadline can still require action when Pine is silent. |
| Receiver restart / lost market message | Retained decision state, broker facts, input sequence and active protection identities; trail extremes if managed outside the broker. | Local recovery plus the actual protection owner. A latest-price snapshot cannot recover an unobserved activation/reversal. No stale backlog dispatch or inferred flatness. |

Source anchors: accepted private ports' `on_bar`/`on_execution` and Vanguard/ORB `_bracket`; `book_protocol.py::BookStrategy` and `Bracket`; `book_runtime.py` boundary collection, feedback delivery and `advance_schedule`; `tv_broker_emulator.py::_amend` and its trail activation/extreme evaluation. The emulator establishes modeled semantics, not live broker capability.

### Two unresolved execution choices

**Calculation cadence:** both Striker and Vanguard Pine declarations set `calc_on_every_tick=true`; Aegis and ORB do not declare that setting. Actual saved properties were not inspected. The local protocol calls for completed bars. TradingView documents that the tick setting changes realtime execution and can produce behavior not reproduced after reload. A publisher gated to completed bars therefore needs an explicit target-semantics decision for both Striker and Vanguard; neither tick alerts nor bar-close alerts are automatically equivalent. [TradingView calculation settings](https://www.tradingview.com/pine-script-docs/concepts/strategies/#calc_on_every_tick).

**Intrabar trailing owner:** CrossTrade's destination documentation, checked 2026-09-25, distinguishes native continuous trailing from CrossTrade-managed profit-triggered trailing. It also describes first-fill-sized native brackets with later-fill coverage repair. These are dependencies on the vendor's pricing and observation service, not evidence that our per-fill triggered trails and coverage contract are qualified. [CrossTrade destination semantics](https://crosstrade.io/docs/webhooks/destinations). The existing [T08](../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md) / CAP disposition still owns qualification: managed triggered trailing was not accepted as satisfying L2(g), and unknown-request closure remains separate.

### Deployment simplification verdict

For the accepted completed-bar state machines, Pine could replace rolling market calculations and bar-input production while local code keeps decision state. Fixed resting stops do not inherently require our own continuous quote feed once correctly installed. However, Vanguard/ORB triggered trailing needs an intrabar price-and-state owner, and all legs need an independent broker-observation/control path. Striker's initial protection timing also needs explicit reconciliation.

Therefore **feed savings are conditional, not disproven**: if an admissible execution service supplies the exact intrabar protection semantics, the local system may avoid its own continuous protection feed. If local code must manage those trails, it needs timely ordered market observations; final OHLC messages are insufficient. More Pine alerts alone do not solve actual-fill references, missing path history or the current native-protection requirement. The next route decision must name that owner, settle the two-leg calculation cadence and reconcile Striker's initial bracket timing before ingress implementation is justified.

Verification: source inspection and SHA-256 comparison in the existing working tree at `1c5c08213f7edad9b7480fceddc075f2252bea22`; current official documentation read as linked. No strategy source or active configuration changed, no Python ran, and no replay, broker drill or live capability test was performed.
