# Close semantics for C-a (whole-leg broker liquidation): documentary determination (2026-09-26)

**Status:** RETURNED for coordinator review; **revised 2026-09-26 in a fix pass** on the coordinator's review findings (scope question S reclassed `CONFLICTING`; the REST→liquidate step labelled as an inference; M8 carried into (c); D-2 added; residual-risk choices completed). Documentary only. This is **not** a trace, a qualification, an acceptance of the close-contract amendment or an acceptance of residual risk. It accepts, authorizes, qualifies or releases nothing.
**Card:** [close-semantics handoff](../briefs/handoffs/2026-09-26-close-semantics-c-a.md). **Dispatch revision:** `62c956f538dfa53f31eaec5951efc3ffa1dce53b` (the worktree `HEAD` was verified to descend from it). **Executor:** assessor subagent (Claude Code, Opus 5.5), worktree `.claude/worktrees/close-semantics`, branch `claude/close-semantics-c-a`.
**Route examined:** our client → CrossTrade REST `POST /v1/api/tv/accounts/{account}/positions/close` with no `qty` or `percent` → Tradovate `liquidateposition`, on an exclusively owned symbol (rail spec D-B9). The last hop is documented for the webhook `closeposition` command; for the REST close it is an **inference** (F1; §4.2 D-2).
**Authority:** operator ruling 2026-09-26, R-CLOSE ([incident ADR §A11.1](../adr/2026-09-17-bounded-platform-protection-incident-contract.md)): C-a is the first candidate **to investigate**; investigation only.
**Addendum 2026-09-27:** public-source and browser research is recorded in the [dated addendum](#addendum-2026-09-27--public-source-and-browser-research-governs-where-it-narrows-statuses-unchanged-unless-stated) at the end of this note. It governs where it narrows the text above. No class in §2 changes, nothing in it is a trace, and C-a stays investigation only: no amendment or residual risk is accepted.

**Result.**
- **Vendor documentation settles none of the nine M questions** ([drill plan §2.5](2026-09-26-tradeify-route-drill-plan-draft.md)). All nine are `OPEN`; none is `CONFLICTING`. The supplementary scope question (S: which working orders a full close cancels) is `CONFLICTING`. Elements (a)–(e) of the [packet's §1.1a](2026-09-26-tradeify-bd-decision-packet.md) are all `OPEN`.
- **What is documented:**
  - For the **webhook** `closeposition` command, CrossTrade's documented typical sequence is a contract lookup and one Tradovate `liquidateposition` request, with no cancel sent by CrossTrade itself. That the **REST** full close follows the same sequence is an **inference** (F1): the REST page names a shared dispatcher and labels its example response `liquidate_position`, but does not document its broker requests.
  - Tradovate describes that request as cancelling orders for a specific contract and closing the position, and says it is "not a guarantee".
  - The request carries no quantity.
  - The response has an optional failure reason and an optional order id.
  - Bracket orders are not tied to the position, so a bracket order left working can open new exposure.
  - Several other actors can liquidate the same symbol.
- **What is not documented:**
  - the broker requests the REST close sends (F1 is an inference);
  - which working orders a full close cancels: CrossTrade's documents disagree between the contract and the account (S, `CONFLICTING`);
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
- **Contradictions:** no trace exists, so there is no trace contradiction. Two documentary inconsistencies are reported: the scope of cancellation within CrossTrade's documents (§4.2, D-1; S is `CONFLICTING`), and the REST page's `liquidate_position` label on a partial-close example (§4.2, D-2). Neither stops C-a.

Under the packet's rule (§1.1, first failure bullet; drill plan CR-3), (a)–(c) are still `OPEN` after M. X-3 may therefore be authorized only as part of the operator's decision on the residual-risk statement. That rule is recorded in the packet; this note only applies it. Whether that bullet's condition ("C-a's mechanism cannot be established from vendor semantics") is met now, or is pending the vendor question, is stated in §3 ("Choices").

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

**Direct file:line citations (fix pass).** The fix pass did not edit the evidence directory, so the following are cited by file and line instead of by quote-index ID:
- **CMD:n** = NEW `ct_webhooks_commands_close-position.html.txt`, line n. CMD:20 is the generic text's first sentence, which is instrument-scoped. CMD:19 and CMD:48 name NinjaTrader instruments. CMD:50 is the Tradovate note: it opens with a "full parity" claim, and CS20 quotes its close.
- **REST:n** = NEW `ct_api_positions_post-close-position.html.txt`, line n, in its Tradovate tab. REST:125 is the "same validation and controls" sentence. REST:140, :151 and :168 are the request examples, each a `percent: 0.5` close. REST:180 is the "shared dispatcher" sentence.
- **DEST:63** = R25 `crosstrade_io_docs_webhooks_destinations.raw.txt:63`. It says a shared name is "not an identical broker request sequence", which refers to the NT8 and Tradovate destinations.
- **OSO:47** = R24 `F2__corpus__api_rest-api-endpoints_orders_place-oso.md` (SHA-256 `6e263dc983e2eba7…`), line 47. Tradovate's `placeOSO` note says that when both brackets are specified they are linked as an OCO, so a fill of one cancels the other.

Two annotations in `QUOTE_INDEX.txt` are the executor's inference labels, not vendor text: "(generic, NT8-oriented text)" on CS18 and CS19. See §4.2 D-1.

**Rules applied.**
- NinjaTrader (NT8) semantics are never read as Tradovate semantics. Where a CrossTrade page has NT8 and Tradovate tabs, the HTML tab boundary was checked (CS12).
- CrossTrade-managed behavior (Account Manager, coverage repair, flat-place barriers) is kept apart from broker-native Tradovate behavior.
- Tradovate's own endpoint text owns `liquidateposition` semantics. CrossTrade's text owns only what CrossTrade sends.
- CrossTrade's statement that its command rows and Tradovate field notes are authoritative (CR03) applies to "this page" only, the webhook destinations page. It is not used to rank CrossTrade's other pages against each other.
- Where CrossTrade's documents disagree about what CrossTrade sends, the question is classed `CONFLICTING`. It is not resolved by an argument about which text takes precedence.
- Silence is recorded as `OPEN`, never as a negative or positive finding.

### 1.3 Documented facts used

| # | Fact | Whose behavior | Sources |
|---|---|---|---|
| F1 | **Webhook (documented):** a full `closeposition` is a contract lookup, then one `POST /order/liquidateposition` (two requests). CrossTrade sends no cancel of its own. CrossTrade calls the table a "typical" sequence: durable recovery and similar processes can add, skip or resume steps.<br>**REST (inference):** the REST full close is inferred to follow the same webhook request table. The basis:<br>• The REST page says the request runs through "the same validation and controls" as a webhook signal (REST:125; also Q01).<br>• It says Account Manager and Trade Copier behavior is applied by "the shared dispatcher" (REST:180).<br>• It labels its abbreviated example response `liquidate_position` (CS11).<br>None of these states the REST path's broker requests. The response example follows only partial-close request examples (REST:168), and for webhooks a partial close is sent as a `placeorder`, not a liquidation (CS06; §4.2 D-2).<br>CrossTrade also disclaims identical broker sequencing for shared names and fields (CS13; DEST:63). Those disclaimers compare the NT8 and Tradovate destinations, not REST with webhooks. They are cited only to show that CrossTrade does not treat a shared name as a statement about sequencing | CrossTrade (its dispatch); the REST part is an inference | CS06, CR02, Q17; REST:125, REST:180, CS11, Q01 |
| F2 | A full close via liquidate "also cancels that contract's working orders". A partial close is an opposing market order that leaves working orders in place. Which orders a full close cancels is disputed within CrossTrade's documents (S, `CONFLICTING`; §4.2 D-1) | CrossTrade's description of Tradovate | CS08, CS20; REST §6.4 |
| F3 | Tradovate: `liquidateposition` is a request to cancel orders for a specific contract and close that position. It "initiates the cancellation process" of open orders for an existing position, and it is "not a guarantee": it can fail for reasons from exchange rejection to parameterization. Tradovate's architecture overview summarizes it as cancelling all orders for a position | Tradovate native | CS01–CS03, CT14 (same text in the legacy API doc bundle), CT01 |
| F4 | The request body is account, contract and an `admin` flag (plus optional tags). It has **no quantity** | Tradovate native | CS04 |
| F5 | The result is `PlaceOrderResult`: a `failureReason` enum (including `Success`, `AnotherCommandPending`, `NotEnoughLiquidity`, `SessionClosed`, `TooLate`, `TradingLocked`, `RiskCheckTimeout`, `UnknownReason`), `failureText` and an optional `orderId`. Each reason has a one-line definition and none is specific to liquidation | Tradovate native | CS05, CT11 |
| F6 | CrossTrade shows its Tradovate close response only in abbreviated form. The full response "includes dispatcher context and the close result", but its fields are not documented. CrossTrade's documented mutation-safety guarantees cover cancel-replace, change, cancel-and-bracket and flat-place, not close. Error classes: 400 `tradovate_rejected` carries the broker reason; a mutation that gets 502 `tradovate_unavailable` may have reached Tradovate and is never resent; after a 500, reconcile first | CrossTrade | CS11, CS14, Q06, Q29, Q18 |
| F7 | **NT8 only:** the REST close page's `pending`/`verified`/`remainingQuantity` fields, join-in-progress, `close_in_progress`, `close_needs_reconciliation` and "400 when nothing is open" sit in the NT8 tab. They are not Tradovate evidence | NT8 add-on | CS12 |
| F8 | Bracket exits are GTC and activate on the entry's first fill. They are not tied to the position: "exit orders can outlive the position they protect". Tradovate documents cases where protective orders left working after a close filled later and opened an unintended position.<br>**OCO sibling cancel:** CrossTrade sends a bracketed REST placement as one `placeOSO` call (Q02). For a `placeOSO` with both brackets, Tradovate documents an OCO link: when one bracket fills, the other is cancelled (OSO:47). CT03 says the same about ATM strategy orders on the Tradovate platform. That is a different context, so CT03 is a transfer to the API brackets and serves as corroboration only | Tradovate native; CrossTrade description | Q14, CS09, CT02, Q02, OSO:47; CT03 (platform ATM context) |
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
| M1 | Are working orders cancelled before the flattening order is sent? What order type is the flattening order? | **OPEN** | Liquidation cancels orders and closes the position in one request (F2, F3). The one-request sequence is documented for the webhook command; for REST it is inferred (F1). Which orders are cancelled is `CONFLICTING` (S) | The order of cancel and flatten, and the flattening order's type. **Leads, not evidence:** Tradovate's text names cancellation first and says the request "initiates the cancellation process" (CS02). CrossTrade's Account Manager flatten, a different operation, cancels first (CR01). Neither states how `liquidateposition` sequences its steps at the broker |
| M2 | Does any protection survive between cancellation and flat? | **OPEN** | No source says any protective order survives. The documented effect cancels all of the contract's working orders, including the bracket children (F2, F3) | Whether cancellation completes before the flatten fills; the length of that interval and any bound on it |
| M3 | Is the flattening quantity fixed at request time or taken from the live position at execution? | **OPEN** | The request has no quantity field, so no client-side quantity can be stale (F4) | When Tradovate computes the quantity |
| M4 | Is liquidation all-or-nothing? Are cancellations rolled back if it fails? | **OPEN** | It is a request that can fail (F3); failure reasons exist (F5) | Whether cancels are rolled back; whether cancels can take effect while the close fails. The endpoint's example response shows a failure reason together with an order id (CS05); an example is not semantics |
| M5 | Can a partial flatten occur? | **OPEN** | Execution reports carry cumulative and last quantity (CT06), so a partial fill would be observable | Whether a liquidation can fill partly, and what happens to the remainder |
| M6 | Is failure reported synchronously or later? | **OPEN** | Both channels exist: a synchronous failure reason in the result (F5), surfaced by CrossTrade as a 400 with the broker reason (F6); and later command reports with reject reasons (CT05). Late rejection is documented for placements (F13) | Which channel a liquidation failure uses; whether a `Success` result can be followed by a failure |
| M7 | Can a protective fill land between the cancel and the flatten, and can both execute? | **OPEN** | Mechanism facts only: bracket children are not tied to the position, and one that survives can open new exposure (F8). When one bracket of the API OSO fills, Tradovate cancels the other (OSO:47; F8). The request is quantity-less (F4) | Any no-reversal mechanism; whether both can execute |
| M8 | What does liquidating an already flat position do? | **OPEN** | **Tradovate:** nothing on the flat case. Its endpoint text refers to "an existing position" (CS02).<br>**CrossTrade, generic command text:** open or pending orders "will not be canceled unless a position already exists" (CS19). The same page's Tradovate note opens by claiming "full parity" with the Tradovate destination (CMD:50). Read literally, that carries CS19 over to Tradovate. The note itself does not repeat CS19.<br>CS19 is therefore the evidence on the disputed side of S (`CONFLICTING`). It is neither adopted nor dismissed. No source states the opposite, that orders are cancelled when the position is flat, so M8 stays `OPEN` rather than `CONFLICTING`.<br>**Flat-place:** CrossTrade's flat-place row tolerates a "no position" result (CS07). Reading that as Tradovate's response to liquidating a flat position is an **inference**: the result could be CrossTrade's own determination | The response class, and whether working orders are cancelled when the position is flat. The REST "400 when nothing is open" is NT8 only (F7). Vendor items 5 and 6 (§6) |
| M9 | Does coverage repair (Q15), or any other vendor watcher, act after a liquidation? | **OPEN** | The repair triggers and quantity rule (F9); other actors that liquidate (F10) | Whether the repair watch ends once a finished entry's position is liquidated, and whether it can act on a stale position read. No source says it acts, or does not act, after a full close |
| S | *Supplementary (not an M question):* which working orders does a full close cancel? | **CONFLICTING** | **Contract scope:**<br>• Tradovate's endpoint covers orders for a specific contract (CS01).<br>• CrossTrade's Tradovate notes say "the contract's working orders" (CS08, CS20).<br>• The generic text's first sentence is instrument-scoped (CMD:20).<br>**Account scope:**<br>• The generic command text cancels "account-level" working or pending orders (CS18), and does not cancel when flat (CS19).<br>• The Tradovate note's "full parity" opening (CMD:50) carries that text over when read literally | Which reading governs what CrossTrade sends on Tradovate. Precedence does not settle it (CR03 covers the destinations page only), and neither does an inference. Pending vendor item 6 (§6). See §4.2 D-1 |

### 2.2 §1.1a elements (a)–(e): the four things the card asks for

| Element | Class | What the vendors document | Does it cover liquidation while a protective order is working or in flight? | Does it bound reversal? | Completion evidence the documents make available (postdating and coherent, GC-3) |
|---|---|---|---|---|---|
| **(a)** Protection during the liquidation interval | **OPEN** | One request that cancels orders and closes the position; "not a guarantee" (F2, F3). The one-request sequence is inferred for REST (F1). No survival, ordering or interval is stated (M1, M2). Whether the cancel reaches other symbols' orders is `CONFLICTING` (S) | No. The liquidation is described only as a whole | No | End state only: position and working-order reads that postdate the send. The interval is visible for one instance at most, and only if the children's `Cancel` commands and the liquidation fill are read with broker timestamps (CT04, CT09). CrossTrade's lifecycle composes those entities but does not list its fields |
| **(b)** Failed, rejected or partial liquidation | **OPEN** | It can fail (F3); the failure reasons and CrossTrade error classes are listed (F5, F6). All-or-nothing, rollback and partial semantics are not documented (M4–M6) | No | No | The liquidation order's status and command reports, if its id is learned: the CrossTrade response fields are undocumented (F6), but the session order list can identify it (drill plan X-3). Position and working-order reads that postdate the send. A partial lifecycle read is not evidence of absence (CR05) |
| **(c)** Protective-fill races and reverse exposure | **OPEN** | The request is quantity-less (F4); children are not tied to the position (F8); when one bracket of the API OSO fills, Tradovate cancels the other (OSO:47). No no-reversal mechanism is documented (M3, M7). Nothing documents what liquidating an already flat position does, as happens when the stop fills first; the one statement on it (CS19) is on the disputed side of S (M8). Other actors can liquidate the same symbol (F10) | No | **No** | A reversal would show in a fill-reconciled position read and in fills by order id with broker timestamps (F11). An order left working after a close on a flat position would show in working-order reads that postdate the send. **No read can show that reversal cannot occur** |
| **(d)** Observations that establish completion | **OPEN** | Per-entity reads exist, and several carry broker timestamps (F11). But order rows carry the creation time only; the status timestamp's meaning is not stated; raw position rows can lag by tens of seconds; the fill-reconciled read is CrossTrade-derived; lists reset at the session boundary; the close response's fields are undocumented (F6). No read is documented as coherent with another (CAP R4) | Not applicable | Detection only | **Postdating:** available for fills and for commands and reports (they carry timestamps). Not available for order rows (creation time) or status (meaning not stated). **Coherence across calls:** not documented. So GC-3 stays OPEN, and a coherence-qualified X-3 pass cannot discharge (d) (CR-5) |
| **(e)** Incident handling while completion is uncertain | **OPEN** | There is no processing bound (support reply, webhook-scoped; T08 §7.9). CrossTrade never resends an ambiguous mutation (Q06, Q18). No join-in-progress behavior is documented for a Tradovate close (F7 is NT8 only). `AnotherCommandPending` exists as a reason with no defined scope (CT11). Lists reset at about 5 PM ET (Q10, Q22). Platform exits and other actors can close the same symbol (F10), and a plain exit ticket leaves brackets working (F8) | No | No. A second close owner adds reversal risk (inference) | As for (d). After the session reset, the documented same-session lookup no longer covers the liquidation order (Q22); a cross-session read by id is R-2's question |

---

## 3. Residual-risk statement (returned for operator decision; not accepted)

| Field | Content |
|---|---|
| Mechanism status | M1–M9: all `OPEN`, with sources in §2.1. No M question is `CONFLICTING`. Supplementary S (which orders are cancelled): `CONFLICTING`, contract scope against account scope (§4.2 D-1). The REST→`liquidateposition` step is an inference (F1; D-2) |
| Observations | **None.** No X-3 or X-5 trace exists, and no fault case has occurred. No observation could prove absence |
| Affected exits | Every whole-leg exit on all four legs (allocation map C11). Also: Striker's close-time crossed-level exit, if realized as a whole-leg close (packet B-7; STR-5 OPEN); scheduled and end-of-session flattens and recovery `CLOSE(leg/symbol)` that use the same primitive; and the displaced-leg close inside the Aegis takeover (GC-5). Under the account-scope reading of S, the working protection of every **other** leg is affected by any of these closes (row "S" below) |
| Figures | None here. Sizes and allowances bind at T16, like §A3 |
| Choices | None is automatic, and the decision is the operator's under R-CLOSE. The packet (§1.1, first failure bullet) and the drill plan's template (§2.5) list these choices; they are recorded here, not adopted:<br>• accept the stated residual under named conditions in the §1.1a amendment (B-1);<br>• C-b, as a separately decided expression change;<br>• a different close contract;<br>• reject the route.<br>**Constraint (drill plan CR-4; packet CC-2, §1.1 second failure bullet):** these choices apply only while the mechanism is unestablished. If a trace contradicts the mechanism (an orphan or reversal in X-3, or a reversal in X-5), residual-risk acceptance is not available for C-a, and any earlier acceptance lapses. The operator may then choose C-b (its own expression decision) or reject the route.<br>**Status of §1.1's first failure condition** ("C-a's mechanism cannot be established from vendor semantics"): **pending**, not yet met on this note's evidence. Public documentation does not establish the mechanism. M's second source, the vendor question (§6), has not been sent. The condition therefore waits on the operator's decision about that question and on any reply. This note owns no route-stop determination and declares none.<br>This statement is returned for decision. It is not an acceptance, and it creates no default |

Each worst outcome below is a **conditional inference**, not a vendor fact. It names the open questions it depends on.

| Element | Worst credible outcome (conditional inference) | How it would be detected | What bounds it |
|---|---|---|---|
| **(a)** | If cancellation completes before the flattening order fills (M1, M2 OPEN), the whole leg is open with **no protective order** until the flatten fills. Exposure: the leg's whole quantity. Duration: not documented. CrossTrade calls its own server-side flatten latency "seconds" in another context (F14); that is not a bound | Only broker-timestamped command and fill reads show the interval, one instance at a time (F11). End-state reads cannot | Nothing documented. If the interval ends in (b) or (c), attended detection and response |
| **(b)** | If cancellations are not rolled back when the liquidation is rejected or fails (M4 OPEN), the whole leg is left **open and unprotected**. Named failure reasons include `SessionClosed` and `TooLate` (CT11), so an end-of-session flatten is one situation where this could arise (conditional). For multi-lot legs, if a liquidation can fill partly (M5 OPEN), an **unprotected remainder** is left. If failure is reported only later (M6 OPEN), the runtime treats the close as pending while the position is unprotected | Position and working-order reads that postdate the send; the liquidation order's status and reports, if its id is learned (F6). A late failure needs polling (Gate A A7; GC-8) | Attended detection and response (halt/resume §2 protection fault), not measured until T13 |
| **(c)** | If Tradovate fixes the flatten quantity before a protective fill lands, or a protective fill lands between the cancel and the flatten (M3, M7 OPEN; for the stop-fills-first case, M8, see the next row), the result is a **reversed, unprotected position** of up to the leg's whole quantity. Three variants end in the same state:<br>(i) a child whose cancel fails while the flatten executes, and which fills later (the documented orphan mechanism after a close, F8);<br>(ii) a second liquidation or platform exit by another actor while the first is in flight, with no documented join or refusal for a Tradovate close (F7, F10, CT11);<br>(iii) coverage repair placing an OCO pair after flat (M9 OPEN), which could later fill | A non-zero opposite position on a fill-reconciled read, or an unexpected fill by order id, subject to the (d) limits. A working order left on the symbol after flat | Attended detection and response, not measured until T13. Exclusive ownership (D-B9; GC-7) removes variant (ii) only for actors the inventory can disable. It does not remove a firm-side automatic liquidation, if one is configured (F10). No observation proves absence |
| **(c)/(d): close on a flat position (M8)** | Suppose the protective stop fills before the liquidation arrives, or a close is sent on a symbol that is already flat. If liquidating a flat position then cancels nothing (the CS19 reading; M8 OPEN; S `CONFLICTING`), any order still working on the contract survives a close whose response may look successful. The response class is undocumented (M8). On an exclusively owned symbol the candidates are:<br>• a remaining entry quantity;<br>• an OCO sibling whose cancel lagged or failed (OSO:47 documents the cancel, not its timing);<br>• a pair placed by coverage repair (M9).<br>A later fill of any of them opens new exposure, possibly unprotected | Working-order reads for the symbol that postdate the send, and lifecycle reads of each child and of any entry (F11), subject to the (d) limits. The close response alone cannot show it (M8) | Attended detection and response, not measured until T13. Nothing documented |
| **(a)/(c): cancellation scope (S)** | If a full close cancels account-level working orders (the CS18 reading, carried over by CMD:50's "full parity"; S `CONFLICTING`), then a whole-leg close on one symbol cancels the working protection of every other leg on the account. Those legs stay open with no protective order until the loss is detected and protection is restored. Exclusive ownership (D-B9) does not reduce this: the other legs belong to this runtime | Working-order reads across all four symbols that postdate the close, and lifecycle reads of each other leg's children (F11). X-3 as designed (one symbol, no other working orders) cannot observe it (§4.2 D-1) | Nothing documented. Attended detection and response only, not measured until T13 |
| **(d)** | If reads cannot be shown to describe one state (GC-3 OPEN), a close could be taken as complete while an order or position remains, or a close could never be completable. Relying on a raw position row (which can lag by tens of seconds, F11), or on a position-only read, would produce the first. A close on a flat position has an undocumented response class (M8), so its response cannot establish completion | Re-reads. Coherence is itself the open item | The rail's evidence-currency rule: no completion without postdating, coherent evidence. Until then the close stays unresolved and blocking, at a cost in availability. *Context only, not an acceptance of this residual:* R-POSTURE (first release) adopted preserve-and-block "for one attended session", followed by explicit review before extension. Within that scope the operator accepted that one unresolved request may suspend automation indefinitely. That existing posture ruling does not accept the C-a (d) residual |
| **(e)** | If the liquidation's outcome stays uncertain (there is no processing bound, and nothing is resent), an unresolved close keeps its blocks indefinitely, with any exposure unprotected or unknown until attended recovery. After the ~5 PM ET reset, the documented same-session lookup no longer finds the liquidation order (Q22). An attended platform flatten during this state is a second close owner (variant (c)(ii)) | The halt/resume §2 row 1 incident (uncertain order outcome) | The attended response and the T13 procedure. When "unconfirmed" becomes "uncertain" is a contract choice; no vendor bound exists to anchor it |

---

## 4. Contradictions found

**4.1 Trace contradictions: none.** No trace exists, so the ruling's stop condition ("a contradicting trace stops C-a") is not triggered.

**4.2 Documentary: two inconsistencies, D-1 and D-2 (reported for the operator; neither stops C-a).**

**D-1: scope of cancellation (S is `CONFLICTING`).**
- **What disagrees.** The disagreement is within CrossTrade's documents, which own what CrossTrade sends.
  - **Account side.** CrossTrade's generic `closeposition` text says a close cancels "account-level" working or pending orders (CS18). It also says orders are not cancelled unless a position exists (CS19). The same page's Tradovate note opens by saying CLOSEPOSITION "has full parity" with the Tradovate destination (CMD:50). Read literally, that carries the generic text over to Tradovate.
  - **Contract side.** The same Tradovate note goes on to say that the full close's liquidation "also cancels the contract's working orders" (CS20). CrossTrade's Tradovate order-types page says the same (CS08). The generic text's own first sentence is instrument-scoped (CMD:20). Tradovate's endpoint text is contract-specific (CS01). The documented typical webhook sequence (CS06) contains no account-level cancel, but CrossTrade calls it "typical", and extra steps can be added (Q17).
- **Why it matters.** If account scope applied, a whole-leg close on one symbol would cancel other legs' working protection: a cross-leg protection gap. It now has its own residual-risk row (§3, "(a)/(c): cancellation scope (S)").
- **Correction (fix pass).** The first return settled this by precedence, citing CR03, and classed S `DOCUMENTED` (contract scope). That settlement is withdrawn. CR03 says the command rows and Tradovate field notes "on this page" are authoritative, and that page is the webhook destinations page (R25 `…destinations.raw.txt:82`). Its `closeposition` row (CR02) says nothing about which orders are cancelled, so CR03 cannot rank CS20 or CS08 above CS18 and CS19.
- **Labelled inferences (not vendor statements).**
  - (i) The generic text is NT8-oriented. The basis is that it names NinjaTrader instruments (CMD:19, CMD:48). The QUOTE_INDEX annotations on CS18 and CS19 record this inference.
  - (ii) "Full parity" may refer to the command's parameters, since the sentence goes on to scaling out, and not to the scope of cancellation.
  - (iii) Tradovate's own endpoint is contract-scoped (CS01). Account scope would therefore require CrossTrade to send further cancels, which its typical sequence does not show but does not exclude.

  None of these settles S.
- **What would settle it.** Vendor question item 6 (§6). X-3 as designed (one symbol, no other working orders) cannot observe it.

**D-2: the REST page labels a partial-close example `liquidate_position`.**
- **What disagrees.** Every request example on the REST close page is a `percent: 0.5` partial close (REST:140, :151, :168). The abbreviated response example that follows is labelled `"api": "liquidate_position"` (CS11). The webhook sequence table sends a partial close as an opposing `placeorder`, not a liquidation (CS06), and the command page's Tradovate note says the same (CS20).
- **Readings.** If the response example belongs to that request, then one of two things is true:
  - the REST partial close uses liquidation, contradicting CS06 and CS20; or
  - the label names CrossTrade's operation rather than the broker call. In that case it is not evidence that the REST **full** close calls `liquidateposition` either.
- **Effect.** The REST page states no broker sequence and says nothing about cancellation in its Tradovate tab. F1's REST step stays an inference under either reading, and no class changes.
- **What would settle it.** Vendor question item 9 (§6).

**4.3 Transfer hazards, not contradictions.** Each could be misread as settling an M question.
- The NT8-tab close semantics (F7), including join-in-progress and `close_in_progress`, are not Tradovate semantics.
- CrossTrade calls flat-place "the atomic version" (CS24). That is a CrossTrade composite with a settlement barrier, not broker atomicity in the rail spec's sense (`CLOSE(scope)`: two requests in one software step are not atomic at the broker).
- The Account Manager's cancel-first flatten (CR01) and Tradovate's risk-limit liquidation text (T08 captures) describe other operations. They do not state how `liquidateposition` sequences its steps.
- Tradovate's architecture-overview summary (CT01) mentions cancellation only. The endpoint page (CS01) is the specific source. This is a gap in the summary, not a conflict.
- CT03's OCO sibling cancel describes ATM strategy orders on the Tradovate platform, linked by Strategy Root ID. The route's brackets are an API `placeOSO` (Q02), for which OSO:47 is the source. Treating CT03 as if it described API brackets would be a transfer.
- The webhook `closeposition` request table (CS06) describes the webhook command. Treating it as the REST close's broker sequence is the inference labelled in F1, not a documented fact.

**4.4 Wording precision (routed to the coordinator; nothing edited).** Packet §1.1's C-a row says the route documents that liquidation cancels "the OCO children". The sources say it cancels **at least all of the contract's working orders**, and Tradovate adds "not a guarantee" (F2, F3). On an exclusively owned symbol, the difference within the contract is small: the working orders are the bracket children plus any working entry on that symbol. On the account-scope reading (S, `CONFLICTING`; D-1), the cancellation would also reach other symbols' orders.

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

*Operator ruling 2026-09-26 (in session): finalized for the operator to send, keeping the nine questions below and adding one request as item 10. The final text, the reply-handling rules and where the reply is retained are in the [vendor-question note](2026-09-26-crosstrade-close-semantics-vendor-question.md). The draft below is kept as drafted.*

*Operator ruling 2026-09-27 (in session):* the text to send is now the revised message in the [vendor-question note](2026-09-26-crosstrade-close-semantics-vendor-question.md) §1, built on the research in the [2026-09-27 addendum](#addendum-2026-09-27--public-source-and-browser-research-governs-where-it-narrows-statuses-unchanged-unless-stated); the 2026-09-26 text is kept there, superseded for sending. It has not been sent. The draft below is still kept as drafted.

**To:** CrossTrade support. The evaluation account has no native Tradovate API access (T08 §7.4), so CrossTrade is the party that makes the `liquidateposition` call. The question asks CrossTrade to name any answer that depends on Tradovate. **Constraints:** no account identifiers. Retain the written reply as original bytes (Gate A A12). Sending needs the operator's own decision; no agent contacts a vendor.

> **Subject:** Full close (liquidate) behavior on a Tradovate account via the REST close endpoint
>
> We call `POST /v1/api/tv/accounts/{account}/positions/close` with no `qty` or `percent` on a Tradovate prop-firm evaluation account (Demo environment). Your webhook docs say a full `closeposition` uses Tradovate's liquidate endpoint, which also cancels the contract's working orders. The position was opened with `orders/place` carrying `stopLoss` and `takeProfit` (one OSO; the exits are OCO). Please answer in writing, for this endpoint and account type:
> 1. **Order of steps.** Are the contract's working orders cancelled before the closing order is sent, at the same time, or after it fills? What order type is the closing order?
> 2. **Quantity.** Is the closing quantity taken from the position when the closing order executes, or fixed when the request is accepted? If the bracket stop fills while the liquidation is in progress, can the closing order still execute and leave an opposite position?
> 3. **Failure.** If the liquidation is rejected or fails, are the cancelled bracket orders restored, or can the position be left open without its stop? Is a failure always in the immediate response, or can it arrive later?
> 4. **Partial.** For a multi-contract position, can the closing order fill partly? What happens to the rest?
> 5. **Already flat.** If the position is already flat, what does the endpoint return? Are working orders on that contract cancelled?
> 6. **Scope.** Does a full close cancel only that contract's working orders, or all working orders on the account? (Your generic `closeposition` text says "account-level" orders; its Tradovate note says the contract's working orders.)
> 7. **Identity and overlap.** Does the response include the closing order's Tradovate id? If a second close for the same account and contract (from the API, or from the Tradovate platform) arrives while the first is in progress, what happens?
> 8. **After the close.** Can bracket coverage repair, or any other CrossTrade process, place or change orders on that contract after a full close?
> 9. **REST path.** Does the REST close endpoint, with no `qty` or `percent`, send the same broker requests as the webhook `closeposition` (a contract lookup, then one `liquidateposition`, with no separate cancel)? Your REST page's example response for a `percent` close is labelled `liquidate_position`. Does a REST partial close use liquidation or an opposing market order?
>
> If any answer depends on Tradovate rather than CrossTrade, please say so, and say whether you can obtain Tradovate's statement.

A written answer would be a vendor statement, subject to coordinator acceptance. It would be evidence for M1–M9, S (D-1), D-2 and the F1 inference. It would not be a trace.

---

## 7. Limitations

- **Documentary only.** No account access, trace, drill or vendor contact took place. Public documents describe intended behavior; they are not execution evidence.
- **Currency.** Checked on 2026-09-26 for the six load-bearing pages only (§1.2). CrossTrade rebuilds its docs (T08 §7.4), so text needs a re-check at binding time. Tradovate entity pages (CT04–CT13) come from the 2026-09-24 capture and were not re-fetched.
- **Which vendor owns what.** The eval reaches Tradovate only through CrossTrade (native API ineligible, T08 §7.4). Tradovate's endpoint semantics apply as far as CrossTrade actually calls that endpoint, and CrossTrade calls its request table "typical" (Q17). For the REST close, even the call itself is inferred rather than documented (F1; D-2). Which orders CrossTrade's close cancels is disputed within CrossTrade's own documents (S; D-1). What CrossTrade sends in the `admin` flag, and what that flag does, are not documented.
- **Environment.** The documents are silent on whether liquidation behaves differently on Demo, where this account runs (F12).
- **Not searched:**
  - the Tradovate community forum (staff posts are not official documentation; T08 treated them as thin);
  - the Tradeify help centre (Cloudflare 403 in T08; not bypassed);
  - CrossTrade's Discord.

  Only three help-centre searches were run, and their results cover platform UI features, not API semantics.
- **Scope of the inferences.** The (a)–(e) mapping is the packet's. Every worst outcome in §3 is a conditional inference. No figures are given; sizes bind at T16.
- **Account configuration.** Whether the other actors in F10 (Account Manager functions, the platform timed exit, firm-side automatic liquidation) are configured on this account is not established. That belongs to the operator's GC-7 inventory.
- **Lifecycle fields.** CrossTrade's lifecycle read is described as a composition of Tradovate entities; its field pass-through (including timestamps) is not listed field by field.
- **Evidence index (fix pass).** The fix pass cited four files directly by file and line (CMD, REST, DEST, OSO; §1.2) and did not add them to `QUOTE_INDEX.txt`. It also left the index's inference annotations on CS18 and CS19 unchanged. Both are for the coordinator at relocation.

---

## Addendum 2026-09-27 — public-source and browser research (governs where it narrows; statuses unchanged unless stated)

**Standing.** Documentary research on public pages only. **Nothing here is a trace.** No class in §2 changes: M1–M9 stay `OPEN`, S stays `CONFLICTING`, and elements (a)–(e) stay `OPEN`. **C-a's status is unchanged:** investigation only under R-CLOSE; neither the close-contract amendment nor any residual risk is accepted. Nothing here authorizes a drill (X-3, X-5), an order action or account access, and nothing here means the vendor question was sent. Where this addendum narrows the text above (A.4), it governs; everywhere else the text above stands. It is recorded under the operator's ruling of 2026-09-27 (in session), which approved preserving the research captures in the primary checkout and recording the findings here.

**A.1 Method and limits.**
- **Scope.** Public pages only, retrieved 2026-09-26/27 UTC by fetch and in an in-app browser. There was no sign-in, account access, form submission or vendor contact. The first (fetch) pass met Cloudflare challenges or 403 responses (help.tradeify.co, support.apextraderfunding.com, the apextraderfunding.com help centre and reddit) and a Vercel bot checkpoint (grep.app, HTTP 429). The browser pass met no CAPTCHA or bot check; one cookie banner (Apex) was answered "Reject All". No block, challenge or checkpoint was bypassed.
- **Two passes.** A public-source pass read CrossTrade's documentation and OpenAPI, Tradovate's partner API reference, the Tradovate community forum and third-party code. A browser pass then read the help-centre pages the first pass could not reach (Tradovate help centre, Tradeify help, Apex help centre). Proposed upgrades went to verifiers; in the first pass, Q1 and Q4 were recorded `OPEN` without going to verifiers ("not sent to verifiers", REPORT.md §2), and in the browser pass Q1 was the only item proposed for an upgrade. Q1, Q2, Q5 and Q8 were proposed higher and are recorded downgraded: Q2 by both verifiers, Q1 by the browser-pass verifier, and Q5 and Q8 on a split vote, with the conservative reading used.
- **Source types.** OC = official CrossTrade; OT = official Tradovate API reference; OT-help = Tradovate help centre (platform UI and policy, not API semantics); PFH = prop-firm help (Tradeify is this account's firm; Apex is another firm, corroboration only); COM = community; TPC = third-party code. Only OC and OT count as documentation of this route. COM and TPC are observations or designs, mostly of direct Tradovate use rather than use through CrossTrade. OT-help and PFH describe platform or firm behavior, not what CrossTrade sends or what `liquidateposition` does. NT8-destination text stays excluded (§1.2 rules).
- **Limits.** Tradovate's text applies only as far as CrossTrade calls that endpoint. Both specs are undated, so the capture hashes pin what was read. Some captures were abridged by their capturers (marked in each file). The hashes pin the captures, not the live pages; one Tradeify article (Exit at Mkt & Cxl) now returns "page doesn't exist". Silence is still recorded as `OPEN` (§1.2 rules).

**A.2 Per-question status.** Q1–Q10 are the items of the vendor message, in its numbering. `PARTLY_DOCUMENTED` is this research's label: at least one part of the item is documented for this route and at least one part is not. It is not this note's `DOCUMENTED`, and it moves no M question.

| Q | Final status | This note | What public sources establish (source type; applies to this route?) | Unresolved |
|---|---|---|---|---|
| **Q1** Order of steps / order type | **OPEN** (a browser-pass proposal of PARTLY_DOCUMENTED was downgraded by the verifier) | M1, M2; (a) | • OT: liquidation "initiates the cancellation process" and closes the position; it is "not a guarantee". No step order and no order type.<br>• OC (applies through the Q9 inference): the flatten_first Tradovate note attributes cancel-and-offset to Tradovate's server-side liquidation, not to a CrossTrade sequence.<br>• OT-help (`f2b1d1c7`, `a31a978e`): the platform's Exit at Mkt & Cxl button cancels working orders and submits **market** orders, for one instrument. This is platform UI only. It reaches this route only through 2022 staff community posts tying the platform flatten to liquidatePosition (COM t/4458, t/4569; the latter may describe the account-wide exit), plus the Q9 inference. A market-order type is therefore community-reported at best for this route.<br>• Does not apply: NT8 sequences; third-party bridge designs | Cancel before, with or after the close; whether the API's closing order is a market order; whether a protective leg can be working while the close is live, and for how long |
| **Q2** Quantity / reversal | **OPEN** (both verifiers downgraded a PARTLY_DOCUMENTED proposal) | M3, M7; (c) | • OT: the LiquidatePosition body has **no quantity field** (account, contract and `admin` are required), so no sent quantity can be stale. This reaches the route only through the Q9 inference; it confirms F4.<br>• OC (webhook-framed): a full `closeposition` is not among the commands that compute the live position from fills. That CrossTrade computes no quantity, and that this carries over to REST, are two inferences.<br>• OT: `placeOSO` exits are OCO (as OSO:47).<br>• COM: a second-hand support quote that a fill wins over a pending cancel; both OCO legs of one bracket filled 34 ms apart (not a liquidation).<br>• Does not apply: reversal examples framed on NinjaTrader (`8579f3d7`) or on another firm's fixed-quantity group flatten (`bdf13b75`) | Whether Tradovate fixes the quantity at acceptance or at execution; whether a stop fill during the liquidation can still leave an opposite position |
| **Q3** Failure | **PARTLY_DOCUMENTED** | M4, M6; (b), (e) | • OC (applies; REST Tradovate overview): 400 `tradovate_rejected` carries the broker reason; 502 `tradovate_unavailable` may have reached Tradovate and is never resent; reconcile after a 500; REST requests create no Alert History entry; the late-rejection re-read is documented for placements only (as F13).<br>• OC OpenAPI: the close lists only 200/400/401/403/429, so it is not an exhaustive failure contract.<br>• OT: the result carries `failureReason` inside an HTTP 200, and later reject channels exist (command-report statuses RiskRejected and ExecutionRejected).<br>• OT-help: liquidation-only mode still allows exits, and eval-account rejections are the provider's to answer (`531c206f`, `c3671420`); "Pending New" means the outcome is not yet known (`9c3f2c99`).<br>• COM: liquidation fails outside market hours; exits and cancels failed during platform incidents.<br>• No official text restores cancelled brackets | Whether cancelled brackets are restored after a failed liquidation; whether cancels can take effect while the close fails; whether a success can fail later; how CrossTrade maps a 200 with a non-`Success` reason; whether the late-rejection re-read covers the close |
| **Q4** Partial fill | **OPEN** | M5; (b) | • No official statement for liquidation.<br>• OT: risk-system auto-liquidation (AutoLiqTransaction, a different operation) tracks exit filled quantity.<br>• OT (platform release notes, `08f2c6c2`): an order that fills partly and is then cancelled can display as "Filled". OT-help (`9c3f2c99`): the order statuses include no "partially filled" value. Read `cumQty`/`lastQty`, not the status alone (an observability hazard).<br>• Demo fills are simulated | Whether the liquidation can fill partly; what happens to the remainder, and whether it stays protected. A one-contract X-3 cannot test this |
| **Q5** Already flat | **OPEN** (one verifier downgraded a community-reported proposal) | M8; S (the CS19 reading) | • COM (broker-native, not through CrossTrade): one Demo API probe got HTTP 200 `{}` when liquidating a flat contract. Working orders were not checked, and `{}` also appeared on a real liquidation, so it does not show a no-op.<br>• OT: the endpoint text refers to "an existing position".<br>• OT-help (`948a6c7e`): the scheduled Flatten Today feature leaves working orders on flat contracts. That is a different feature, not shown to call liquidatePosition.<br>• The REST page's "400 when nothing is open" stays NT8-only (F7) | What the REST close returns when flat, and whose "no position" that is; whether working orders are cancelled. No source of any kind tested the flat case with working orders present |
| **Q6** Cancel scope | **CONFLICTING**; D-1 stands | S (D-1) | • Contract side: OC Tradovate-specific pages (the close-position Tradovate note, order-types-and-exits, the indicator-automation guide, the trade-copier page); OT's endpoint is one contract; COM staff: one call per contract; OT-help and PFH (`f2b1d1c7`, `3542a877`): the platform button touches only the module's instrument (platform UI, reaching the route only through the community link).<br>• Account side: OC's generic `closeposition` text ("account-level", CS18), which reaches Tradovate only through a literal reading of "full parity" (CMD:50). The verifiers struck two further account-side items: the flatten_first "in the account" warning (a different feature) and an NT8-framed, unscoped info box.<br>• The OpenAPI binding (Q9) makes the command pages apply to REST. Precedence still does not settle the conflict | Whether a Tradovate full close sends any cancel beyond the contract-scoped liquidation, reaching other symbols. Only CrossTrade, or a test with working orders on two symbols, can settle it; X-3 as designed cannot |
| **Q7** Identity / overlap | **PARTLY_DOCUMENTED** | F6; (c)(ii), (d), (e) | • OC (applies): REST requests get no per-account/instrument webhook lock and no webhook rate bucket. Idempotency keys cover only `cancelreplace` and copier fan-out; reading this as excluding CLOSEPOSITION rests on the word "only". The request body allows only `instrument`, `qty` and `percent`, so no client tag can be sent. The response envelope differs between the OpenAPI (`data`) and the page (`response`), and neither documents an order id.<br>• OT: the result's `orderId` is optional; `AnotherCommandPending` appears only as an enum value.<br>• COM: liquidate "never returns an orderId" (2025); an order strategy sent about 63 ms after a liquidate acknowledgement was closed out.<br>• OT-help (`29e43cc7`): the Orders module shows an order-details timeline (platform UI; useful for after-the-fact checks) | Whether the close response carries the closing order's id, and in which field; what Tradovate does with a second liquidation or platform exit while the first is in flight; any unlisted REST-side guard |
| **Q8** After the close | **OPEN** (one verifier downgraded a PARTLY_DOCUMENTED proposal) | M9; (c)(iii) | • OC: coverage-repair mechanisms only (as F9); none is documented as acting, or as not acting, after a full close. The Sep 5, 2026 release note says CrossTrade tracks every bracket family it places, re-checks it on socket resync and background sweep, and raises a critical alert for uncovered quantity. The docs were rebuilt on Sep 21, and nothing says whether alert-only or rebuild is current. That REST OSOs are watched, and that a liquidation fill is not an "exit fill", are inferences.<br>• Other actors: OC Account Manager functions; copier sync only if the account is a leader or follower; PFH Tradeify end-of-session auto-close, drawdown-breach auto-liquidation and Manual Lockout (candidates in the [drill plan §0.1](2026-09-26-tradeify-route-drill-plan-draft.md) addition of 2026-09-27) | Whether tracking ends at a full close; whether a sweep or resync can act between the cancel and the fill, or on a stale read; alert-only versus rebuild; which processes are configured on this account (GC-7). Nothing documents any actor placing or changing orders after a successful full close |
| **Q9** REST path | **PARTLY_DOCUMENTED** | F1; D-2 | • OC (applies): the OpenAPI (`7d78fb0a`) maps the REST close to `x-tv-command: CLOSEPOSITION`, which "runs through the shared webhook parser and dispatcher". The `_endpoints` list, the REST page and the overview say the same.<br>• OC execution table (`cb0ef0ba`): a full close is `GET /contract/find` then `POST /order/liquidateposition`, two requests with no cancel step; a partial close is a lookup, live reads and an opposing market `placeorder`, five requests. The table is labelled a "typical broker sequence, not an exact request transcript", and recovery, settlement and copier logic can add or skip steps.<br>• OT-help (`6638dae9`, updated 9/16/2026): prop and evaluation accounts are not eligible for Tradovate's retail API add-on, so CrossTrade reaches this account through another integration | CrossTrade's direct statement of the broker requests a REST full close sends; what "typical" can add (ties to Q6); whether a REST `qty`/`percent` close uses liquidation or an opposing market order (D-2); which Tradovate integration CrossTrade uses |
| **Q10** Guarantees / version / Demo | **PARTLY_DOCUMENTED** | F12; §7 (the `admin` flag; currency) | • Guarantees: OT calls liquidation a request, "not a guarantee" (the text dates from 2022 or earlier, per TPC). OC calls its broker table "typical", and its mutation-safety guarantees name CANCELREPLACE, partial CHANGE, CANCELANDBRACKET and FLATPLACE, not CLOSEPOSITION.<br>• Versions: OC OpenAPI 3.1.0, API 1.0.0; OT partner OpenAPI 3.1.0, info.version 1.0.0. Against a 2026-08-21 third-party copy of the OT spec (TPC), the field set is unchanged.<br>• Demo: OC says firm accounts are Demo simulation accounts and documents only scheduled-cancel and GTD-expiry differences (F12). OT-help (`022409b7`, updated 9/10/2026): prop and eval accounts always run in Simulation mode, and Tradovate Support does not resolve their rejections or disputes. OT-help (`1e2dd8ca`): partner prop simulation accounts are a separate class from retail Demo.<br>• `admin`: OT marks it required, with no description. COM: `admin:true` was refused and `admin:false` worked on Demo. What CrossTrade sends is undocumented | Which close behaviors CrossTrade guarantees; the endpoint version, integration and `admin` value; whether liquidation or fills on the prop simulation differ from Live |

**A.3 Key new facts.**
1. **The REST close is bound to `CLOSEPOSITION`.** CrossTrade's OpenAPI binds the REST close to `CLOSEPOSITION` through the shared webhook parser and dispatcher. CrossTrade's execution table gives a full close as `contract/find` then one `liquidateposition`, labelled "typical". F1's REST step now rests on these two documented links. Joining them is still an inference, and "typical" still allows added steps.
2. **No quantity is sent.** Tradovate's LiquidatePosition body has no quantity field (this confirms F4 against the partner OpenAPI). It reaches this route only through the inference in item 1.
3. **"Market orders" is platform-UI text.** Tradovate's help centre says the platform's Exit at Mkt & Cxl button cancels working orders and submits market orders. That is platform UI. It reaches this route only through 2022 staff community posts plus the item-1 inference, so it does not document the API's order type.
4. **No ordering and no no-reversal mechanism.** No source of any type gives the order of cancel and close for a liquidation, or documents a mechanism that prevents reversal. The residual-risk statement (§3) therefore still applies to every element, unchanged.
5. **Recovery runs through the firm.** Tradovate's Emergency Trade Desk does not flatten or manage evaluation accounts, and Tradovate Support does not resolve eval rejections (`18133cfa`, `057d0e3d`, `022409b7`). An attended recovery that cannot use the platform therefore runs through Tradeify, not Tradovate. This bears on the T13 attended procedure. The question belongs to Tradeify, not CrossTrade, and it is not in the vendor message.

**A.4 Where this narrows the text above.** The earlier text is kept; this governs where they differ.
- **F1, and the header's "Route examined" line:** the REST→`liquidateposition` step is still an **inference**, now a narrow one: two documented links (A.3 item 1) joined by one inference, under a "typical" label. REST:125, REST:180 and CS11 remain supporting context.
- **D-2:** unresolved. The REST page's `api` labels (`flatten_filtered`, `liquidate_position` and others) look like CrossTrade operation names rather than broker calls. That is a pattern inference. It leans toward D-2's second reading without settling it.
- **F10:** Tradeify's end-of-session auto-close, its drawdown-breach auto-liquidation and the Manual Lockout join the actors that can close the same symbol, as published firm and platform policy. Whether and how they act on this account is not established. They are listed as candidates in the drill plan's §0.1 addition of 2026-09-27.
- **F12:** Tradovate's help centre says prop and eval accounts always run in Simulation mode, and treats partner prop simulation accounts as a separate class from retail Demo. Nothing documents whether liquidation behaves differently there, so F12's conclusion stands.
- **§3, status of §1.1's first failure condition:** still **pending**. Public documentation still does not establish the mechanism, and the vendor question (text revised 2026-09-27) has not been sent.
- **§4.3 transfer hazards, added:**
  - platform button text (Exit at Mkt & Cxl, Reverse & Cxl, Flatten Today) is not API semantics;
  - Tradeify policy text describes the firm, not `liquidateposition`;
  - Tradovate's close-first text on market conditions concerns margin liquidation on brokerage accounts (`939c8ad1`) and does not apply;
  - NinjaTrader-framed pages (Risks of Electronic Trading, Sim+) are excluded.
- **§7, "Not searched":** the Tradovate community forum and the Tradeify help centre have now been read (public pages; the Tradeify help centre no longer blocks). CrossTrade's Discord was not searched. The limits in A.1 apply.

**A.5 Evidence.** The research captures are preserved in the operator's primary checkout at `local_artifacts/crosstrade-close-research-2026-09-27/` (gitignored). `SHA256SUMS.all` lists 637 files, and its own SHA-256 is `8dd20292daa98f0fee17f3c0e0c9f2585696eee7303791dc61bf8a883b70dbe6`.
- Each capture folder also has its own `SHA256SUMS` or manifest. The first line of each capture gives its URL and retrieval time (UTC).
- The two reports are `REPORT.md` (the public-source pass) and `BROWSER-DELTA.md` (the browser pass). The session scratchpad paths inside them are superseded by this location.
- Hash prefixes in this addendum are the SHA-256 of the capture relied on. Community thread captures carry dynamic fields, so a re-capture of the same thread hashes differently.
- The earlier captures under `local_artifacts/close-semantics-2026-09-26/` (§1.2) were read only.

**A.6 Still blocked** (none bypassed):
- support.apextraderfunding.com: in the first (fetch) pass, blocked by Cloudflare or 403; in the browser pass, it redirects to a helpdesk sign-in page. No sign-in was attempted.
- reddit.com: in the first (fetch) pass, the r/Tradovate search was blocked (Cloudflare or 403) and old.reddit returned only an interstitial. In the browser pass, reddit.com and old.reddit.com were refused by the in-app browser's safety restriction before any request was sent. No mirror was used.

Not used: GitHub code search (it needs sign-in), CrossTrade's Discord, logged-in CrossTrade pages and the API Playground. Previously blocked and now read: the Tradovate help-centre articles, help.tradeify.co and the apextraderfunding.com help centre.

**A.7 Vendor question.** Every item still has an unanswered part, so none is dropped. By the operator's ruling of 2026-09-27 (in session), the revised message is the text to send. It is in the [vendor-question note](2026-09-26-crosstrade-close-semantics-vendor-question.md) §1, with the 2026-09-26 text preserved there as superseded for sending. It has not been sent. The operator sends it himself, and the reply-handling rules are unchanged. §6 above stays as drafted.

## Addendum 2026-10-02 — C-a selection register (prerequisites before C-a is selected as the first-release close form)

**Why this exists.** On 2026-10-01 the operator directed that the first release close every leg by C-a. Exceptions: attended incident recovery stays on the attended-platform path, and entries stay one-contract-per-request (deployment checklist, first-session addendum item 7). Successive reviews kept finding one more prerequisite at a time, so this register lists them **all in one place**. C-a stays **investigation-only and is not selected** until every row below is discharged. **Technical rows** (B, C, D and E, plus F4, F7 and F8) are discharged only by the named owner's amendment, code, test or evidence. Missing evidence cannot be waived (halt/resume :67). **Policy and residual-risk rows** (A3, A4, F1, F2, F5, F6, and any A2 answer left OPEN, except that Q6 also needs A5's owner amendment) may be discharged by an explicit operator ruling. Item 7 points here; this register is the owner.

The register comes from one read-only pass, made by a coordinator-dispatched reader on 2026-10-02 (main `3cbaa04`, PR #590 `3ec7bb3`, §A12 from PR #584). It covered this note, the vendor question, the B–D packet, the rail spec, halt/resume, the incident ADR, the drill plan, both production handoffs and both pre-registrations.

Abbreviations:
- **VQ**: vendor question (revised §1).
- **BD**: B–D packet.
- **RS**: multi-leg rail spec.
- **HR**: halt/resume contract.
- **DP**: drill plan.
- **BAO**: `ops/c1_rail/book_account_owner.py`.

**A. Vendor semantics** (owner: the operator sends; the reply is an authoritative vendor statement).
- A1. Send VQ revised §1. **Not yet sent** (VQ :3).
- A2. Load-bearing answers, needed for selection: Q1 (order of steps), Q2, Q3 (failure classes), Q4, Q5, **Q6 (scope, which decides S; a trace cannot substitute; discharge rule in A5)**, Q7 (identity and second close owner), Q8 (coverage repair), **Q9 (whether the REST full close maps to `liquidateposition`; today this is an inference, CS §3 and the A.2 addendum)**. The D-2 part of Q9 only corroborates. **Q10** (Demo and prop-simulation integration: the admin value, simulation-specific liquidation) needs **authoritative coverage or an explicit operator residual-risk decision**.
- A3. If any of (a)–(c) stays OPEN, or Q6 is answered account-wide (A5), the operator must make a **residual-risk decision** on §3. X-3 can be authorized only inside that decision (§3 :155; BD :112; DP :248).
- A4. Accept the BD §1.1a amendment, elements (a)–(e) (BD :85, :95–105). Owner: the operator, then the rail spec.
- A5. **Q6 discharge rule (safety-critical).** An authoritative answer to Q6 is **not by itself a discharge**. Only an authoritative **contract-scoped** answer (a full close sends no cancel beyond the contract-scoped liquidation) discharges Q6. If the answer is **account-wide**, or Q6 stays OPEN or CONFLICTING (so account scope is not excluded), a whole-leg close may strip every other open leg's working protection (§3, scope row (a)/(c)), so C-a is not selectable unless the operator makes an explicit residual-risk decision on that outcome **and** the owners amend for it: the rail spec and halt/resume must say how the other legs' protection is re-established or how a close is barred while another leg is open. That decision cannot discharge the owner amendment, which is technical.

**B. X-3 trace coverage** (owner: the X-3 drill; the operator for authorization).
- B1. **X-3 cannot show a partial remainder or no-reversal** (DP :318, :320, :370). Those come from vendor semantics or an accepted residual risk, not from X-3.
- B2. A multi-lot leg (N OSO pairs) is untraced, because X-3 is one contract (DP :251, :446; OQ8).
- B3. Transfer to other symbols and environments: MNQ and MGC need an argument, and 6J is a separate decision (DP :250, :439, :445).
- B4. A coherence-qualified pass discharges neither GC-3 nor (d). GC-3 for close completion is ROUTE STOPS (DP :316; BD :122).
- B5. Lifecycle reads, with timestamps, of the liquidation order and both former children (§ :220).
- B6. CP-3, P-1 and a fresh X-1 position (DP :268, :553).
- B7. A trace with other legs' working orders present **corroborates S only**.

**C. Outcome classes** (owners: the rail-spec amendment, halt/resume, T09 code). **No automatic retry of any attempted non-success outcome.** A close that was **never sent** (queued as `close_pending` behind attachment or another serialized operation) keeps its automatic **first** dispatch (BAO :1434–1453; `test_unresolved_attachment_queues_close_until_confirmation`); otherwise a strategy exit is stranded and the leg stays open.
- C1. **Success.** Completion requires postdating, coherent P/W/K1 reads covering the former children, the liquidation's own terminal status, and **every symbol's** working orders while S is CONFLICTING. Late failures are polled (BD :104; §A12 :473; RS :58).
- C2. **Partial (known).** An incident, with no resend. It needs a carrier: HR :34 (protection fault) or the rail spec. That carrier replaces RS :63 "resumes… remainder only".
- C3. **Unknown.** An incident under §A12 F1/F4, with no resend. The outcome window is one bar, but a scheduled flatten reaches deadline D first (HR :119; BD :105, OPEN).
- C4. **Rejected.** An incident, with **no automatic resubmission**. This replaces RS :63 "resubmitted at most once per bar", which rests on M4 (OPEN). A refusal may be remote and uncertain (Gate A A3(ii)), and C-a sends no client tag (§ :292). HR §4.1 :93 must classify it.
- C5. **Failed or refused.** That covers HTTP 200 with failureReason, 400, **401, 403, 409, both 429 forms** (including the ambiguous `broker_rate_limited`), 500 and 502. The CrossTrade REST assessment gives none of these a no-send guarantee (:123–125, :133). **Every documented route error class is an incident until it is authoritatively mapped**, with no retry.
- C6. **Flat at send** (no position, children still working). Send no C-a. Use the S4 orphan cancel or treat it as an incident (RS :63, :77; § :164).

**D. Owner amendments.**
- D1. **Rail spec**:
  - :63 and :79 (scoped `CLOSE(fill scope)`; resume-for-remainder; auto-resubmit);
  - S1(5) L2(c)(d)(e) for every leg (:71);
  - I7 (:67), S3(d) (:75), S7 "preserve protective orders" (:83), S10 (:89);
  - L-2 and its test list (:149), R-D (:152).
- D2. **Halt/resume**: classes 13–15; §1 :28, provider-side actors; §7 :145, required tests.
- D3. **Incident ADR**: §A11.1 is investigation-only (:368, :376), so selection needs a dated addendum. UB-5 is EVIDENCE-PENDING and resolves through gate-C evidence (the primitive choice waits for gate C, D3 / L2(d); :302): its discharge is the accepted gate-C UB-5 evidence plus the dated addendum recording it, not an approval.
- D4. **Successor pre-registrations** (PR #591): ORB-6, STR-7 and VAN-8 answered; VAN-8's close "replay treatment" (PRv :63); §6; **Vanguard §3a's exit-split dependency** (PRv :82) replaced by the same C-a answer, so the successor holds one execution contract.
- D5. **Production handoffs**:
  - G1/G2 still require the §6 sequential-exit replay model;
  - G3/G4 bind the closed originals' "no replay output" gate;
  - both must retarget to the successors (HO :27, :31; HV :25, :29).
- D6. **Sequencing.** BD :144 rewrites the exit rows "once a close realization is accepted". A successor cannot be amended after any replay output (PRo :98), so the rows are answered before any successor replay.

**E. T09 code.**
- E1. A quantity-less REST close producer. `_flatten_action` builds a flat intent that carries a quantity (BAO :1917), and the route is absent (:1866).
- E2. Remove the `:remainder:N` auto-remainder (BAO :1909) and halt instead.
- E3. Broker rejection becomes an incident, not a terminal outcome (BAO :1875).
- E4. A close past its one-bar timeout must halt. Today the fence covers entries and adds only (:827–830), and an open close only refuses risk-adds (`close_unreconciled`, :1792).
- E5. Close completion is scoped to `scope_legs` (:1407). The liquidation order must be identified without a response id.
- E6. `resume_closes` (:1434) must not automatically **re-dispatch** a close that was already sent with a non-success outcome. It keeps the first dispatch of a never-sent queued close, and the rail-spec amendment (D1) states the same split.
- E7. Reverse the rail-spec tests `test_close_partial_fill_preserves_residual_protection` and `…restart_resumes_same_operation` (:149).
- E8. Refuse any sub-whole-leg close on the C-a transport (first-session addendum 7.6.2).

**F. Other** (operator rulings unless stated).
- F1. **GC-7 exclusivity.** Without it, C-a is ROUTE STOPS. The firm-liquidation exception currently covers X-1 only (BD :126; DP :553).
- F2. **OQ9.** A liquidation also closes any preservation trade on a book symbol (DP :447).
- F3. **GC-5 Aegis takeover through C-a** (BD :124, :153). It is **not** a selection prerequisite, because that would be circular: GC-5's takeover trace needs an accepted close realization (BD :124; DP :433). It is a **post-selection release condition**. C-a may be used for GC-5 qualification once every other row is discharged, and the first release still requires GC-5 to pass before it starts.
- F4. **The T13 attended-platform procedure**, including the firm fallback (§ :302). **Technical, not a ruling row:** the B–D owner records the procedure, including the second-close race (§3 (e); (c)(ii)), as OPEN. It is discharged only by the accepted T13 procedure and its evidence.
- F5. **The B07 gate-D condition** (BD :231).
- F6. **OQ8.** Whether the M step plus offline tests suffice for the fault cases (DP :446).
- F7. **Striker's triggered-protection transition** is qualified at gate C. STR-5's whole-leg intent does not settle it (§1.1a; BD :107–109).
- F8. **The Rule-0 whole-leg source check** (first-session addendum 7.5 and 7.6), including the per-fill trailing items, which clear only when the editions freeze trailing-free.

**If any row cannot be discharged,** the close form returns to the operator before the first release (first-session addendum 7.4).
