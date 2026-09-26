# Close semantics for C-a (whole-leg broker liquidation): documentary determination (2026-09-26)

**Status:** RETURNED for coordinator review. Documentary only. This is **not** a trace, a qualification, an acceptance of the close-contract amendment or an acceptance of residual risk. It accepts, authorizes, qualifies or releases nothing.
**Card:** [close-semantics handoff](../briefs/handoffs/2026-09-26-close-semantics-c-a.md). **Dispatch revision:** `62c956f538dfa53f31eaec5951efc3ffa1dce53b` (the worktree `HEAD` was verified to descend from it). **Executor:** assessor subagent (Claude Code, Opus 5.5), worktree `.claude/worktrees/close-semantics`, branch `claude/close-semantics-c-a`.
**Route examined:** our client → CrossTrade REST `POST /v1/api/tv/accounts/{account}/positions/close` with no `qty` or `percent` → Tradovate `liquidateposition`, on an exclusively owned symbol (rail spec D-B9).
**Authority:** operator ruling 2026-09-26, R-CLOSE ([incident ADR §A11.1](../adr/2026-09-17-bounded-platform-protection-incident-contract.md)): C-a is the first candidate **to investigate**; investigation only.

**Result.**
- **Vendor documentation settles none of the nine M questions** ([drill plan §2.5](2026-09-26-tradeify-route-drill-plan-draft.md)). All nine are `OPEN`; none is `CONFLICTING`. Elements (a)–(e) of the [packet's §1.1a](2026-09-26-tradeify-bd-decision-packet.md) are all `OPEN`.
- **What is documented:**
  - In CrossTrade's documented typical sequence, a full close is one Tradovate `liquidateposition` request, with no cancel sent by CrossTrade itself.
  - Tradovate describes that request as cancelling the contract's orders and closing the position, and says it is "not a guarantee".
  - The request carries no quantity.
  - The response has an optional failure reason and an optional order id.
  - Bracket orders are not tied to the position, so a bracket order left working can open new exposure.
  - Several other actors can liquidate the same symbol.
- **What is not documented:**
  - the order of the cancel and the flatten;
  - whether any protection survives that interval;
  - when the flatten quantity is fixed;
  - whether cancels are rolled back on failure;
  - whether a flatten can fill partly;
  - when failures are reported;
  - whether a protective fill can race the flatten;
  - what liquidating a flat position does;
  - whether any vendor watcher acts afterwards.
- **Consequence:** no no-reversal mechanism is documented, so the residual-risk statement (§3) applies to every element.
- **Contradictions:** no trace exists, so there is no trace contradiction. One documentary inconsistency, the scope of cancellation in CrossTrade's generic command text (§4, D-1), is reported. It does not stop C-a.

Under the packet's rule (§1.1, first failure bullet; drill plan CR-3), (a)–(c) are still `OPEN` after M. X-3 may therefore be authorized only as part of the operator's decision on the residual-risk statement. That rule is recorded in the packet; this note only applies it.

---

## 1. Read report

### 1.1 Inputs read

| Input | Used for |
|---|---|
| Card (in full); [B–D packet](2026-09-26-tradeify-bd-decision-packet.md) rulings table, §1.1, §1.1a, §1.2 (GC-3, GC-7), CC-1/CC-2 | The questions, the element mapping, the evidence standard and the failure rules |
| [Drill plan draft](2026-09-26-tradeify-route-drill-plan-draft.md): ruling block, CR-1–CR-12, §0.1, §2.0, §2.3 (X-3), §2.5 (M, fault cases, residual-risk template, X-5) | M questions 1–9; X-3/X-5 design; the residual-risk format |
| [REST assessment](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md) §6 (incl. §6.3, §6.4, §6.6) and §6.11 (Gate A A1–A14) | Q-IDs; outcome classes; accepted Gate A findings (A4 L2(d) `K`; A7; A8; A12) |
| [T08 handoff](../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md) §7 (incl. §7.3, §7.4, §7.9) | No processing bound; native API unavailable to evals; support reply scope |
| [CAP-20260916](../briefs/phase4-preparation/2026-09-16/capability-decision.md) N1-d (L2(d)) and N1-e (L2(e)); R4 | What L2(d)/(e) qualification needs; the coherence gap |
| [Rail spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md): evidence currency, `CLOSE(scope)`, I7, S5 (scoped exit/flat), R-B3 L-2 (d)/(e) | The contract text the amendment would change |
| [Incident ADR](../adr/2026-09-17-bounded-platform-protection-incident-contract.md) §A1, §A2 rule 7, §A4, §A6, §A11, §A11.1 | Ruling scope; per-primitive `K`/`U` record |
| T08 N1 map (private, `local_artifacts/t08-r3-2026-09-24/n1-map-2026-09-24/N1_MAP.md`) | Earlier source of "liquidate cancels the contract's working orders" (its LQ key) |

### 1.2 Evidence and method

**Reuse first.** The following were read in place in the primary checkout:
- **R25:** `local_artifacts/t08-rest-route-assessment-2026-09-25/`, cited by its Q01–Q30 (`MANIFEST.tsv` `d069ae7e…`).
- **R24:** `local_artifacts/t08-r3-2026-09-24/pages/`, the T08 root. It holds the complete Tradovate partner-API corpus of 468 pages, captured 2026-09-24. Files are cited by name and SHA-256 prefix.

Facts used from these roots that carry no Q-ID are given new IDs (CR-, CT-) in this determination's quote index.

**Targeted retrieval, only for named gaps.** Nine public URLs were fetched on 2026-09-26 at 23:18–23:19 UTC, all HTTP 200, with no login and no account access.

| Named gap | Fetched |
|---|---|
| Currency check of the main sources behind M1–M8 | The Tradovate partner `liquidate-position` page; CrossTrade's REST close-position page, Tradovate API overview, order-types-and-exits page and execution-internals page |
| M8, and the scope of cancellation | The CrossTrade webhook `close-position` command page |
| (e): the attended platform flatten as a second close owner; M1 leads | Three Tradovate help-centre searches: "liquidate", "exit at mkt" and "flatten" |

Currency results:
- The Tradovate page is **byte-identical** to its 2026-09-24 capture (`41eadfe9ff705e85…`).
- The four CrossTrade REST and Tradovate pages are **text-identical** to their 2026-09-25 captures. Their byte hashes differ because the HTML is regenerated.
- The webhook command page is text-identical to its T08 capture.
- The help-centre results cover platform UI features only; none states API liquidation semantics.

**Evidence directory.** `local_artifacts/close-semantics-2026-09-26/` in this worktree, which is gitignored (`.gitignore:291`). It holds:
- `MANIFEST.tsv` (file, URL, capture UTC, HTTP code, bytes, SHA-256), SHA-256 `74721db0f4223329c97a9e4ede2f03e0173fa20236f6b800b48617ae024d1d29`;
- `QUOTE_INDEX.txt` (CS01–CS24 for new captures; CR01–CR08 for R25; CT01–CT14 for R24);
- `SHA256SUMS` over every file.

The coordinator relocates the directory to the primary checkout. The HTML-to-text helpers ran through `.\fp.ps1 python` (doctor: ops-env 3.13.2, 62 locked packages matched).

**Rules applied.**
- NinjaTrader (NT8) semantics are never read as Tradovate semantics. Where a CrossTrade page has NT8 and Tradovate tabs, the HTML tab boundary was checked (CS12).
- CrossTrade-managed behavior (Account Manager, coverage repair, flat-place barriers) is kept apart from broker-native Tradovate behavior.
- Tradovate's own endpoint text owns `liquidateposition` semantics. CrossTrade's text owns only what CrossTrade sends.
- Silence is recorded as `OPEN`, never as a negative or positive finding.

### 1.3 Documented facts used

| # | Fact | Whose behavior | Sources |
|---|---|---|---|
| F1 | A full `closeposition` is a contract lookup, then one `POST /order/liquidateposition` (two requests). CrossTrade issues no cancel of its own. CrossTrade calls the table a "typical" sequence: durable recovery and similar can add, skip or resume steps. REST `close` uses the same dispatcher as webhooks | CrossTrade (its dispatch) | CS06, CR02, Q17, Q01 |
| F2 | A full close via liquidate "also cancels that contract's working orders". A partial close is an opposing market order that leaves working orders in place | CrossTrade's description of Tradovate | CS08, CS20; REST §6.4 |
| F3 | Tradovate: `liquidateposition` is a request to cancel orders for a specific contract and close that position. It "initiates the cancellation process" of open orders for an existing position, and it is "not a guarantee": it can fail for reasons from exchange rejection to parameterization. Tradovate's architecture overview summarizes it as cancelling all orders for a position | Tradovate native | CS01–CS03, CT14 (same text in the legacy API doc bundle), CT01 |
| F4 | The request body is account, contract and an `admin` flag (plus optional tags). It has **no quantity** | Tradovate native | CS04 |
| F5 | The result is `PlaceOrderResult`: a `failureReason` enum (including `Success`, `AnotherCommandPending`, `NotEnoughLiquidity`, `SessionClosed`, `TooLate`, `TradingLocked`, `RiskCheckTimeout`, `UnknownReason`), `failureText` and an optional `orderId`. Each reason has a one-line definition and none is specific to liquidation | Tradovate native | CS05, CT11 |
| F6 | CrossTrade shows its Tradovate close response only in abbreviated form. The full response "includes dispatcher context and the close result", but its fields are not documented. CrossTrade's documented mutation-safety guarantees cover cancel-replace, change, cancel-and-bracket and flat-place, not close. Error classes: 400 `tradovate_rejected` carries the broker reason; a mutation that gets 502 `tradovate_unavailable` may have reached Tradovate and is never resent; after a 500, reconcile first | CrossTrade | CS11, CS14, Q06, Q29, Q18 |
| F7 | **NT8 only:** the REST close page's `pending`/`verified`/`remainingQuantity` fields, join-in-progress, `close_in_progress`, `close_needs_reconciliation` and "400 when nothing is open" sit in the NT8 tab. They are not Tradovate evidence | NT8 add-on | CS12 |
| F8 | Bracket exits are GTC and activate on the entry's first fill. They are not tied to the position: "exit orders can outlive the position they protect". Tradovate documents working protective orders left after a close filling later and opening an unintended position. An OCO fill cancels its sibling | Tradovate native; CrossTrade description | Q14, CS09, CT02, CT03 |
| F9 | Coverage repair (CrossTrade-managed) watches bracketed entries from the placement response onward. It cancels a remaining entry quantity, or places a new OCO pair for uncovered quantity. Uncovered quantity is entry fills minus exit fills minus working stop quantity, clamped to the live position. It runs when the entry finishes, after its own cancels, and on periodic re-checks. Support's "never opens or adds to a position" was scoped to the webhook shape | CrossTrade-managed | Q15 and the execution-internals page lines 105–109; T08 §7.9; Gate A A8 |
| F10 | Other actors can liquidate the same symbol:<br>• CrossTrade Account Manager: auto-close through the Tradovate API; manual, scheduled and window flatten. Its flatten cancels working orders **before** liquidation and reports success only when the account is confirmed order-free and flat. That is a CrossTrade-managed composite, not `closeposition`<br>• Tradovate platform: a timed exit that exits positions and cancels orders; the "Exit at Mkt & Cancel All" button; a plain exit ticket<br>• The prop firm's Tradovate risk settings, which can automatically liquidate on a threshold or at a configured time<br>Whether any of these is configured on this account is not established here | Mixed; see text | Q27, CR01, CS21–CS23, CT12, CT13 |
| F11 | **Reads.**<br>• The lifecycle read returns the order, its highest version (quantity, type, prices), its commands and its reports. It can be partial, and "an empty section marked unavailable is not evidence that no data exists". Report reads cover only the last 10 commands.<br>• Order and fill list rows carry Tradovate server timestamps.<br>• Tradovate's Command, CommandReport, ExecutionReport, Fill and Position entities each carry a required timestamp. `Order.timestamp` is the **creation** time. OrderVersion carries `orderQty` and `orderType`.<br>• The status read carries a timestamp whose meaning is not stated.<br>• Raw position rows can lag a fill by tens of seconds. The fill-reconciled position read is derived by CrossTrade.<br>• Order and fill lists reset at about 5 PM ET | CrossTrade reads of Tradovate entities | CR05, CR06, CS16, CT04–CT10, CR07, CS15, Q10, Q22 |
| F12 | Prop-firm evaluation accounts run on Tradovate's **Demo** environment. CrossTrade documents points where Demo differs from Live: Demo records scheduled cancels and GTD expiry but does not execute them. Nothing documented says whether liquidation behaves differently on Demo | CrossTrade's description of Tradovate | CR04, CS10 |
| F13 | Late rejection, about a second after acceptance, is documented for **placements**. It is not stated for liquidation | Tradovate, per CrossTrade | CR08, Q03 |
| F14 | CrossTrade says the flatten and lock latency of its Account Manager enforcement is "measured in seconds". This is a lead only, not a bound for `closeposition` | CrossTrade-managed | CS17 |

---

## 2. Classification

### 2.1 Drill-plan M questions

| # | Question (drill plan §2.5) | Class | Documented (source) | Not documented |
|---|---|---|---|---|
| M1 | Are working orders cancelled before the flattening order is sent? What order type is the flattening order? | **OPEN** | Liquidation cancels the contract's working orders and closes the position, as one request (F1–F3) | The order of cancel and flatten, and the flattening order's type. **Leads, not evidence:** Tradovate's text names cancellation first and says the request "initiates the cancellation process" (CS02). CrossTrade's Account Manager flatten, a different operation, cancels first (CR01). Neither states how `liquidateposition` sequences its steps at the broker |
| M2 | Does any protection survive between cancellation and flat? | **OPEN** | No source says any protective order survives. The documented effect cancels all of the contract's working orders, including the bracket children (F2, F3) | Whether cancellation completes before the flatten fills; the length of that interval and any bound on it |
| M3 | Is the flattening quantity fixed at request time or taken from the live position at execution? | **OPEN** | The request has no quantity field, so no client-side quantity can be stale (F4) | When Tradovate computes the quantity |
| M4 | Is liquidation all-or-nothing? Are cancellations rolled back if it fails? | **OPEN** | It is a request that can fail (F3); failure reasons exist (F5) | Whether cancels are rolled back; whether cancels can take effect while the close fails. The endpoint's example response shows a failure reason together with an order id (CS05); an example is not semantics |
| M5 | Can a partial flatten occur? | **OPEN** | Execution reports carry cumulative and last quantity (CT06), so a partial fill would be observable | Whether a liquidation can fill partly, and what happens to the remainder |
| M6 | Is failure reported synchronously or later? | **OPEN** | Both channels exist: a synchronous failure reason in the result (F5), surfaced by CrossTrade as a 400 with the broker reason (F6); and later command reports with reject reasons (CT05). Late rejection is documented for placements (F13) | Which channel a liquidation failure uses; whether a `Success` result can be followed by a failure |
| M7 | Can a protective fill land between the cancel and the flatten, and can both execute? | **OPEN** | Mechanism facts only: bracket children are not tied to the position, and one that survives can open new exposure (F8). An OCO fill cancels its sibling (CT03). The request is quantity-less (F4) | Any no-reversal mechanism; whether both can execute |
| M8 | What does liquidating an already flat position do? | **OPEN** | For Tradovate, nothing. CrossTrade's flat-place row tolerates a "no position" liquidation result (CS07) | The response class, and whether working orders are cancelled when the position is flat. CrossTrade's generic command text says orders are not cancelled unless a position exists (CS19), but that text is NT8-oriented and its Tradovate note does not repeat it. The REST "400 when nothing is open" is NT8 only (F7) |
| M9 | Does coverage repair (Q15), or any other vendor watcher, act after a liquidation? | **OPEN** | The repair triggers and quantity rule (F9); other actors that liquidate (F10) | Whether the repair watch ends once a finished entry's position is liquidated, and whether it can act on a stale position read. No source says it acts, or does not act, after a full close |
| S | *Supplementary (not an M question):* which working orders does a full close cancel? | **DOCUMENTED** (contract scope) | Tradovate: orders for a specific contract (CS01). CrossTrade's Tradovate notes: that contract's working orders (CS08, CS20) | CrossTrade's generic command text says "account-level" (CS18); see §4, D-1 |

### 2.2 §1.1a elements (a)–(e): the four things the card asks for

| Element | Class | What the vendors document | Does it cover liquidation while a protective order is working or in flight? | Does it bound reversal? | Completion evidence the documents make available (postdating and coherent, GC-3) |
|---|---|---|---|---|---|
| **(a)** Protection during the liquidation interval | **OPEN** | One request that cancels the contract's orders and closes the position; "not a guarantee" (F1–F3). No survival, ordering or interval is stated (M1, M2) | No. The liquidation is described only as a whole | No | End state only: position and working-order reads that postdate the send. The interval is visible for one instance at most, and only if the children's `Cancel` commands and the liquidation fill are read with broker timestamps (CT04, CT09). CrossTrade's lifecycle composes those entities but does not list its fields |
| **(b)** Failed, rejected or partial liquidation | **OPEN** | It can fail (F3); the failure reasons and CrossTrade error classes are listed (F5, F6). All-or-nothing, rollback and partial semantics are not documented (M4–M6) | No | No | The liquidation order's status and command reports, if its id is learned: the CrossTrade response fields are undocumented (F6), but the session order list can identify it (drill plan X-3). Position and working-order reads that postdate the send. A partial lifecycle read is not evidence of absence (CR05) |
| **(c)** Protective-fill races and reverse exposure | **OPEN** | The request is quantity-less (F4); children are not tied to the position (F8); an OCO fill cancels its sibling (CT03). No no-reversal mechanism is documented (M3, M7). Other actors can liquidate the same symbol (F10) | No | **No** | A reversal would show in a fill-reconciled position read and in fills by order id with broker timestamps (F11). **No read can show that reversal cannot occur** |
| **(d)** Observations that establish completion | **OPEN** | Per-entity reads exist, and several carry broker timestamps (F11). But order rows carry the creation time only; the status timestamp's meaning is not stated; raw position rows can lag by tens of seconds; the fill-reconciled read is CrossTrade-derived; lists reset at the session boundary; the close response's fields are undocumented (F6). No read is documented as coherent with another (CAP R4) | Not applicable | Detection only | **Postdating:** available for fills and for commands and reports (they carry timestamps). Not available for order rows (creation time) or status (meaning not stated). **Coherence across calls:** not documented. So GC-3 stays OPEN, and a coherence-qualified X-3 pass cannot discharge (d) (CR-5) |
| **(e)** Incident handling while completion is uncertain | **OPEN** | There is no processing bound (support reply, webhook-scoped; T08 §7.9). CrossTrade never resends an ambiguous mutation (Q06, Q18). No join-in-progress behavior is documented for a Tradovate close (F7 is NT8 only). `AnotherCommandPending` exists as a reason with no defined scope (CT11). Lists reset at about 5 PM ET (Q10, Q22). Platform exits and other actors can close the same symbol (F10), and a plain exit ticket leaves brackets working (F8) | No | No. A second close owner adds reversal risk (inference) | As for (d). After the session reset, the documented same-session lookup no longer covers the liquidation order (Q22); a cross-session read by id is R-2's question |

---

## 3. Residual-risk statement (returned for operator decision; not accepted)

| Field | Content |
|---|---|
| Mechanism status | M1–M9: all `OPEN`, sources in §2.1. Supplementary S: `DOCUMENTED` (contract scope). No mechanism row is `CONFLICTING` |
| Observations | **None.** No X-3 or X-5 trace exists, and no fault case has occurred. No observation could prove absence |
| Affected exits | Every whole-leg exit on all four legs (allocation map C11). Also: Striker's close-time crossed-level exit, if realized as a whole-leg close (packet B-7; STR-5 OPEN); scheduled and end-of-session flattens and recovery `CLOSE(leg/symbol)` that use the same primitive; and the displaced-leg close inside the Aegis takeover (GC-5) |
| Figures | None here. Sizes and allowances bind at T16, like §A3 |
| Choices | The operator's, under R-CLOSE; none is automatic. This statement is returned for decision. It is not an acceptance, and it creates no default |

Each worst outcome below is a **conditional inference**, not a vendor fact. It names the open questions it depends on.

| Element | Worst credible outcome (conditional inference) | How it would be detected | What bounds it |
|---|---|---|---|
| **(a)** | If cancellation completes before the flattening order fills (M1, M2 OPEN), the whole leg is open with **no protective order** until the flatten fills. Exposure: the leg's whole quantity. Duration: not documented. CrossTrade calls its own server-side flatten latency "seconds" in another context (F14); that is not a bound | Only broker-timestamped command and fill reads show the interval, one instance at a time (F11). End-state reads cannot | Nothing documented. If the interval ends in (b) or (c), attended detection and response |
| **(b)** | If cancellations are not rolled back when the liquidation is rejected or fails (M4 OPEN), the whole leg is left **open and unprotected**. Named failure reasons include `SessionClosed` and `TooLate` (CT11), so an end-of-session flatten is one situation where this could arise (conditional). For multi-lot legs, if a liquidation can fill partly (M5 OPEN), an **unprotected remainder** is left. If failure is reported only later (M6 OPEN), the runtime treats the close as pending while the position is unprotected | Position and working-order reads that postdate the send; the liquidation order's status and reports, if its id is learned (F6). A late failure needs polling (Gate A A7; GC-8) | Attended detection and response (halt/resume §2 protection fault), not measured until T13 |
| **(c)** | If Tradovate fixes the flatten quantity before a protective fill lands, or a protective fill lands between the cancel and the flatten (M3, M7 OPEN), the result is a **reversed, unprotected position** of up to the leg's whole quantity. Three variants end in the same state:<br>(i) a child whose cancel fails while the flatten executes, and which fills later (the documented orphan mechanism after a close, F8);<br>(ii) a second liquidation or platform exit by another actor while the first is in flight, with no documented join or refusal for a Tradovate close (F7, F10, CT11);<br>(iii) coverage repair placing an OCO pair after flat (M9 OPEN), which could later fill | A non-zero opposite position on a fill-reconciled read, or an unexpected fill by order id, subject to the (d) limits. A working order left on the symbol after flat | Attended detection and response, not measured until T13. Exclusive ownership (D-B9; GC-7) removes variant (ii) only for actors the inventory can disable. It does not remove a firm-side automatic liquidation, if one is configured (F10). No observation proves absence |
| **(d)** | If reads cannot be shown to describe one state (GC-3 OPEN), a close could be taken as complete while an order or position remains; or a close could never be completable. Using a raw position row (can lag by tens of seconds, F11) or a position-only read would produce the first | Re-reads. Coherence is itself the open item | The rail's evidence-currency rule: no completion without postdating, coherent evidence. Until then the close stays unresolved and blocking. That costs availability, which the operator accepted for unresolved requests under R-POSTURE |
| **(e)** | If the liquidation's outcome stays uncertain (there is no processing bound, and nothing is resent), an unresolved close keeps its blocks indefinitely, with any exposure unprotected or unknown until attended recovery. After the ~5 PM ET reset, the documented same-session lookup no longer finds the liquidation order (Q22). An attended platform flatten during this state is a second close owner (variant (c)(ii)) | The halt/resume §2 row 1 incident (uncertain order outcome) | The attended response and the T13 procedure. When "unconfirmed" becomes "uncertain" is a contract choice; no vendor bound exists to anchor it |

---

## 4. Contradictions found

**4.1 Trace contradictions: none.** No trace exists, so the ruling's stop condition ("a contradicting trace stops C-a") is not triggered.

**4.2 Documentary: one inconsistency, D-1 (reported for the operator; does not stop C-a).**
- **What disagrees.** CrossTrade's generic `closeposition` command text says a close cancels "account-level" working or pending orders, and that orders are not cancelled unless a position exists (CS18, CS19). The same page's Tradovate note, CrossTrade's Tradovate rows and Tradovate's own endpoint text all scope the cancellation to the **contract** (CS20, CS08, CS01).
- **Why it matters.** If account scope applied, a whole-leg close on one symbol would cancel other legs' working protection: a cross-leg protection gap.
- **How this determination resolves it.** CrossTrade says its Tradovate command rows and field notes are authoritative for destination differences (CR03), and Tradovate's own text is contract-scoped. The scope is therefore classed `DOCUMENTED` (contract), with the inconsistency reported.
- **What would settle it.** Vendor question item 6 (§6). X-3 as designed (one symbol, no other working orders) cannot observe it.

**4.3 Transfer hazards, not contradictions.** Each could be misread as settling an M question.
- The NT8-tab close semantics (F7), including join-in-progress and `close_in_progress`, are not Tradovate semantics.
- CrossTrade calls flat-place "the atomic version" (CS24). That is a CrossTrade composite with a settlement barrier, not broker atomicity in the rail spec's sense (`CLOSE(scope)`: two requests in one software step are not atomic at the broker).
- The Account Manager's cancel-first flatten (CR01) and Tradovate's risk-limit liquidation text (T08 captures) describe other operations. They do not state how `liquidateposition` sequences its steps.
- Tradovate's architecture-overview summary (CT01) mentions cancellation only. The endpoint page (CS01) is the specific source. This is a gap in the summary, not a conflict.

**4.4 Wording precision (routed to the coordinator; nothing edited).** Packet §1.1's C-a row says the route documents that liquidation cancels "the OCO children". The sources say it cancels **all of the contract's working orders**, and Tradovate adds "not a guarantee" (F2, F3). On an exclusively owned symbol the difference is small: the working orders are the bracket children plus any working entry on that symbol.

---

## 5. What order-producing drills could and could not add

The ruling defers X-5, and no drill is authorized. This section describes value only; it proposes nothing.

| | X-3: normal-case full close, one contract, no race | X-5: protective-fill race (DEFERRED) |
|---|---|---|
| **Could add** (one instance, on the environment where it runs) | • The end state: flat; children terminal; no working order left; the liquidation order terminal. This validates F2/F3 for one instance without a race<br>• The liquidation order's type and quantity, from session orders and then its lifecycle version (CT08). This is one observation for M1 (type) and for M3 (quantity equals the position when nothing changed; it cannot separate request-time from execution-time)<br>• **If lifecycle rows carry broker timestamps:** the relative order of the children's `Cancel` commands and the liquidation's `New` command and fill. That gives one observation for M1's ordering and one sample of the (a) interval, not a bound<br>• Whether the close response carries the liquidation order id (F6)<br>• Which reads carry timestamps that postdate the send (GC-3; drill plan open question 5)<br>• Whether any repair placement appears after flat, in that instance (M9) | • One near-race outcome. **A reversal observed contradicts the mechanism and stops C-a** (ruling). No reversal is only *consistent* with a no-reversal mechanism<br>• Whether an overlap actually happened, shown only from broker timestamps, if the reads carry them |
| **Could not add** | • Absence of reversal (c)<br>• Rollback (M4)<br>• A partial flatten (M5; impossible at one contract)<br>• A late failure, unless one occurs naturally<br>• A bound on the interval<br>• Coherence across reads (GC-3, (d)), unless shown<br>• Behavior with a second close owner<br>• Behavior on a flat position (M8)<br>• Behavior in another environment without an accepted equivalence argument (Demo versus Live, F12; interface rule)<br>A pass is necessary but not sufficient for L2(d) (CR-7), and a coherence-qualified pass cannot discharge (d) or GC-3 (CR-5) | • The mechanism for M3 or M7, unless a reversal occurs<br>• Any bound. Human timing cannot place the send reliably inside the window<br>• X-5 also carries real reversal exposure |

**Suggested read additions for the coordinator's X-3 decision (not adopted).** Read the lifecycle of the liquidation order and of both children after the close. Record whether their command and report rows carry timestamps. This costs no extra order action.

**Not covered by either drill.** M8 (flat-position behavior) and the D-1 scope would each need their own design or a vendor answer.

---

## 6. Draft vendor question (for the operator to send; not sent)

**To:** CrossTrade support. The evaluation account has no native Tradovate API access (T08 §7.4), so CrossTrade is the party that makes the `liquidateposition` call. The question asks CrossTrade to name any answer that depends on Tradovate. **Constraints:** no account identifiers. Retain the written reply as original bytes (Gate A A12). Sending needs the operator's own decision; no agent contacts a vendor.

> **Subject:** Full close (liquidate) behavior on a Tradovate account via the REST close endpoint
>
> We call `POST /v1/api/tv/accounts/{account}/positions/close` with no `qty` or `percent` on a Tradovate prop-firm evaluation account (Demo environment). Your docs say a full close uses Tradovate's liquidate endpoint, which also cancels the contract's working orders. The position was opened with `orders/place` carrying `stopLoss` and `takeProfit` (one OSO; the exits are OCO). Please answer in writing, for this endpoint and account type:
> 1. **Order of steps.** Are the contract's working orders cancelled before the closing order is sent, at the same time, or after it fills? What order type is the closing order?
> 2. **Quantity.** Is the closing quantity taken from the position when the closing order executes, or fixed when the request is accepted? If the bracket stop fills while the liquidation is in progress, can the closing order still execute and leave an opposite position?
> 3. **Failure.** If the liquidation is rejected or fails, are the cancelled bracket orders restored, or can the position be left open without its stop? Is a failure always in the immediate response, or can it arrive later?
> 4. **Partial.** For a multi-contract position, can the closing order fill partly? What happens to the rest?
> 5. **Already flat.** If the position is already flat, what does the endpoint return? Are working orders on that contract cancelled?
> 6. **Scope.** Does a full close cancel only that contract's working orders, or all working orders on the account?
> 7. **Identity and overlap.** Does the response include the closing order's Tradovate id? If a second close for the same account and contract (from the API, or from the Tradovate platform) arrives while the first is in progress, what happens?
> 8. **After the close.** Can bracket coverage repair, or any other CrossTrade process, place or change orders on that contract after a full close?
>
> If any answer depends on Tradovate rather than CrossTrade, please say so, and say whether you can obtain Tradovate's statement.

A written answer would be a vendor statement: evidence for M1–M9 and D-1, subject to coordinator acceptance. It would not be a trace.

---

## 7. Limitations

- **Documentary only.** No account access, trace, drill or vendor contact took place. Public documents describe intended behavior; they are not execution evidence.
- **Currency.** Checked on 2026-09-26 for the six load-bearing pages only (§1.2). CrossTrade rebuilds its docs (T08 §7.4), so text needs a re-check at binding time. Tradovate entity pages (CT04–CT13) come from the 2026-09-24 capture and were not re-fetched.
- **Which vendor owns what.** The eval reaches Tradovate only through CrossTrade (native API ineligible, T08 §7.4). Tradovate's endpoint semantics apply as far as CrossTrade actually calls that endpoint, and CrossTrade calls its request table "typical" (Q17). What CrossTrade sends in the `admin` flag, and what that flag does, are not documented.
- **Environment.** The documents are silent on whether liquidation behaves differently on Demo, where this account runs (F12).
- **Not searched:**
  - the Tradovate community forum (staff posts are not official documentation; T08 treated them as thin);
  - the Tradeify help centre (Cloudflare 403 in T08; not bypassed);
  - CrossTrade's Discord.

  Only three help-centre searches were run, and their results cover platform UI features, not API semantics.
- **Scope of the inferences.** The (a)–(e) mapping is the packet's. Every worst outcome in §3 is a conditional inference. No figures are given; sizes bind at T16.
- **Account configuration.** Whether the other actors in F10 (Account Manager functions, the platform timed exit, firm-side automatic liquidation) are configured on this account is not established. That belongs to the operator's GC-7 inventory.
- **Lifecycle fields.** CrossTrade's lifecycle read is described as a composition of Tradovate entities; its field pass-through (including timestamps) is not listed field by field.
