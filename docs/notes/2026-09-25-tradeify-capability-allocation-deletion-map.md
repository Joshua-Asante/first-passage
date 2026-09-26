# TradingView / CrossTrade capability allocation and deletion map — 2026-09-26

**Status:** RETURNED for coordinator review (checklist [T09 gate D](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t09-gate-acceptance-record)). Documentary assessment only. It approves no design, deletes nothing, changes no behavior or contract, and grants no drill, access, spend or GO.
**Packet:** [allocation handoff](../briefs/handoffs/2026-09-25-tradeify-capability-allocation-deletion-map.md) §0–§5 as amended by §5a (dispatch refresh 2026-09-26, which governs on conflict).
**Executor:** assessor subagent (Claude Code, Opus 5.5) of the coordinating session, worktree branch `claude/tradeify-allocation-map`. **Coordinator:** the coordinating Claude Code session. **Dispatch revision:** `d5effe5fbeb9df84de39dbcf1933a1ee91e303e3` (HEAD at start; verified). **Retrieval/inspection date:** 2026-09-26.

## Coordinator-corrected recommendation and decision list (2026-09-26) — read this first

**Status:** coordinator review, with the operator's executive corrections of 2026-09-26. Where this section conflicts with the assessor's text below, **this section governs**. The assessor's return is preserved unchanged as the historical record. Review record: [handoff §6](../briefs/handoffs/2026-09-25-tradeify-capability-allocation-deletion-map.md#6-executor-return). This is **not** gate-D acceptance.

**Corrected recommendation.**
- **Route.** The recommended route stays the ruled Python signal host → our account owner → CrossTrade-mediated Tradovate REST.
- **TradingView.** Its exclusion from any live role is the **standing project ruling** (2026-09-11), not a fresh legal conclusion. Reopening permission would be a separate investigation (D01).
- **Permission gap on the chosen route.** It still needs evidence of account entitlement (CrossTrade Pro REST is only vendor-reported, Q01) and of venue permission for CrossTrade-mediated automated orders on this eval. A firm's general "automation-friendly" classification is insufficient on its own.

**Vendor savings are conditional.** Read the §C boundary and rows C09–C11 with these limits:
- Tradovate *creates* the one-contract bracket with the entry (`DOCUMENTED`). Protection is **not in force until its stop is Working**, after the first-fill activation interval (`UNVERIFIED` until D1; incident ADR §A1 residual).
- Removing multi-contract entry coverage repair does **not** remove partial completion **across a split or a multi-order close**. A split can stop midway (UB-4), and sequential closes can leave an intent partly closed (UB-5).

**Corrected decision list.** It supersedes the matching §D rows; rows not listed stand as written.

| # | Correction |
|---|---|
| D09 → **GC-3** (gate C, not a contract change for now) | A poller-assigned per-stream sequence (`_apply_protection_snapshot_db`, stream-order check) orders **our observations only**. It does not show that several reads describe **one coherent broker state**, or that their underlying broker data **postdates** amend preparation. Gate C must establish both separately. If they can't be established, amend admission is unimplementable on this route, and the fallback is a contract change or an operator-owned expression change (Striker ratchet, Aegis re-pin). |
| **D19 (new; first-order blocker)** | The rail spec's `CLOSE(scope)` and S5 require **verified L2(d) and L2(e)**, and forbid a cancel-plus-market fallback. L2(e) is contradicted on this route (Gate A A5). One-contract entries do **not** automatically satisfy that contract, and they don't remove races between a close and a protective fill. Resolve early: define a route-native close and protection cleanup, or amend or interpret the close contract, then qualify it. **Until resolved, no close route is viable**, whatever option B's value. UB-8 cannot substitute for this. |
| D17 | **Resolved** by the owner record ([protection selection](2026-09-10-tradeify-protection-selection.md), mode table): ORB adds are normal in NORMAL mode and off under protection. |
| All K primitives | Each carries a failure consequence in the gate-C matrix: stop activation at quantity 1 (D1), rejected-modify survival (D2), full close (D3), cancel of Suspended children (D6), and the takeover composite. For each, the matrix states whether **the route stops** or **an operator-owned expression change is needed**. |

**Corrected next action:** the integrated B–D packet. It contains D19 and the gate-C decisive capabilities (close and protection cleanup; stop activation and rejected modify; evidence freshness and coherence; REST reconciliation and actor inventory), the UB-8 bounded comparison run in parallel, the remaining gate-B decisions, the revised option-B rules and a T09 handoff held until B–D acceptance.

---

**Operator objective (checklist addendum 2026-09-26):** TradingView and CrossTrade own what they can reliably do on the exact route; our controller fills only evidenced gaps.

**Headline.** On the ruled route (Python signal host → our account owner → CrossTrade-mediated Tradovate REST), the controller cannot shrink to a thin relay. The reason is not prior build effort. The vendors own no portfolio-level function: no admission, capacity, priority, fill-confirmed strategy state, unknown-request accounting, settlement or schedule owner. TradingView has **no permitted live role**: the standing 2026-09-11 ruling holds its Terms of Use §3 applicable to machine use of alerts. What the vendors do own after the three route-native editions is substantial. Tradovate holds the per-contract fixed stop/target from entry, and brokers every execution between bars. No leg then needs an intrabar trailing owner, a continuous protection feed, an ATTACH path or partial-fill coverage repair. Those are the real reductions, and they are **AVOID BUILDING** rows, not deletions.

---

## §0 Read report and checkpoint

### Read report (Phase 0)

| Item | Result |
|---|---|
| Inspected revision | Worktree `d5effe5` (main `24e3843` + gate-B branch `7fe2891`, per §5a item 1). Code read at that revision (hashes in §E). |
| Governing reads | All §0 items: STATE; deployment checklist incl. 2026-09-26 addendum and gate table; umbrella (ownership routing); route note (partition, three state kinds, between-alert map); REST assessment incl. §6.11 Gate A (A1–A14, drill map); T08 §7.8–§7.9; CAP (R1–R5, N1); campaign §59 Rulings 1–4 and §60; both edition pre-registrations (DRAFT); S2 signal-host ADR; rail extension spec (E1–E3, S2–S10, R-B3, I8); halt/resume rev9; incident ADR §A1–§A9.1; bounded-exposure scope. Also read, because they decided allocation facts: S2b build ADR addendum 2026-09-11 (Q3 terms ruling), `ops/c1_rail/qualification/trust_domain.py` and `prepare_compute.py` (qualification consumers). |
| Private identities | All eight `core/strategies/BOOK_SOURCES.sha256` pins **match** (`sha256sum -c` in the primary checkout, 2026-09-26), including Striker's corrected generation `efd479b6…`. The default Striker port hashes to `c81aa59c…`. It was not used. Read in place: ORB port `b1f4e573…`, Striker corrected port `efd479b6…` and Aegis port `11763740…` (action/exit/amend branches only). Vanguard behavior is taken from its pre-registration §3a and the accepted A6 disposition, not re-read (§5a item 3). No private body, value or path content was copied, committed or sent anywhere. |
| Missing / not read | The private effective-inputs files (`66406dee…` source, `9d4d4e1d…` runtime) are **outside the §60 list** and were not read. Every claim resting on an effective binding (e.g. ORB breakeven off, Striker's non-backtest branches on) is attributed to the route note or the Vanguard return. The retained vendor captures (`local_artifacts/t08-rest-route-assessment-2026-09-25/`) were not re-read; Gate A accepted them after the operator's spot-check. No new vendor retrieval was made. The Tradeify automation-compliance owner note named in `core/firm_rules.py` is not in this checkout. |
| Current vs proposed authority | **Current:** S2 Python-native signal host; TradingView research/export only. Halt/resume rev9 (incident = attended; no automatic incident dispatch). E3 preserve-and-block (`book_account_owner.py:1608`). Rail spec L2 requirements. Declared expressions remain the accepted book until the editions freeze. **Direction, not effective:** route-native editions for ORB/Striker/Vanguard (§59 Rulings 3–4; pre-registrations DRAFT with OWED rows); option B (Proposed), whose UB-1/3/8/9 are ruled as direction only. |

### Checkpoint (recorded per §0; delivered in the §6 return)

- **Provisional boundary:** retain one durable account owner with an intent-before-send journal, a completed-bar four-leg barrier, the private ports, capacity/sizing/mode, takeover, schedule, settlement, unknown-request accounting and a thin REST adapter. Delegate order matching, resting stop entries, per-contract OSO protection and between-bar stop/target execution to Tradovate. Delegate transport and IDs to CrossTrade.
- **Likely reductions:** no live TradingView ingress, alert manifest or Pine publisher; no intrabar trail manager or protection feed; ATTACH and live trailing-field paths become unreachable after freeze; no partial-fill cover logic.
- **Material conflicts:** (1) no documented REST read supplies the `complete`/`sequence` protection snapshot the owner's amend admission requires (C18); (2) Striker's close-time crossed-level exit exists only in the offline emulator, not the owner (C11b); (3) T08 §7.8 still says the exit-side partial-fill row is moot, which UB-5 withdrew (stale restatement).
- **Missing evidence:** every K primitive (L2(c)/(d), cancel of Suspended children, takeover composite); stop activation at quantity 1 (D1); REST reads D4/D5 (unauthorized); R5 actor inventory; production feed (O-4); T13 channels.

---

## A. Capability allocation matrix

Labels: `DOCUMENTED`, `OBSERVED FOR EXACT SCOPE`, `CONTRADICTED`, `UNVERIFIED`. No route capability is `OBSERVED FOR EXACT SCOPE`: no trace exists (Gate A drill map, all rows "Not demonstrated"). Local code behavior below is inspected source, not route evidence. *PROVISIONAL-B* marks a responsibility that exists only if option B is accepted. "Decision?" names the D-queue item.

### A1. Signal, strategy and portfolio decisions

| ID | Required behavior · governing owner | Current local implementation | Proposed owner: decision / execution / recovery | Vendor alternative · evidence | Inputs → authoritative state | Gap · residual work · Decision? |
|---|---|---|---|---|---|---|
| C01 | Market calculations and history (indicators, ranges, warm-up), per leg · D-B4 book; ports pinned by `book_adapters.py` | Private ports `on_bar` on completed 15-minute bars; `pine_ta.py` | Local ports / — / local retained barriers | TradingView Pine computes the same on its chart: technically `DOCUMENTED`. Machine use of alerts: `CONTRADICTED` for permission, Terms §3 ruled applicable 2026-09-11 ([S2b ADR Q3](../adr/2026-08-08-s2b-signal-daemon-build.md)) | Completed bars → port state (checkpointed through the owner) | TV route needs permission plus an S2 ADR amendment. Ports are required regardless by offline qualification (`trust_domain.py` port roles; replay uses `tv_broker_emulator`). **D01, D02** |
| C02 | Source continuity, session and contract mapping for 4 symbols · S2b; halt/resume §2 timeouts | `BarSource` protocol only; no provider (O-4 deferred); `book_session_calendar.py`; barrier and staleness checks in `book_runtime.py` / `book_evaluate_loop.py` | Local feed adapter (T14) / — / local halt on silence | CrossTrade: no Tradovate market data, `DOCUMENTED` (S2b ADR Q5 "CrossTrade market-data exclusion"). TV: as C01 | Feed bars → retained partial bars and barriers | Provider unselected and unfunded. The feed is irreducible on the ruled host. **D15** |
| C03 | Eligibility and decision counters (daily counts, once-per-session arming, add counters advancing at proposal) · accepted ports | Ports. Refusals are retained by the owner and not rolled back (route note "three kinds of state") | Local ports / — / owner feedback replay | TV Pine: `CONTRADICTED` for unchanged forwarding (route note §3: simulated state diverges after refusal) | Proposal-time state in port checkpoint | None beyond retention. VAN-6 counter wording is OWED. **D05** |
| C04 | Fill-dependent adds and exits (position, average price, lots from confirmed fills only) · `book_protocol.py` feedback contract | Owner commits facts; `FourLegRuntime._deliver_events` → `on_execution`; ports hold lots | Local / Tradovate fills / owner journal | TV emulator fills: `CONTRADICTED` as a substitute. CrossTrade: none | Broker fills → owner `broker_facts` → port lots | Needs a real fill producer (T09). **D16** |
| C05 | Sizing, protection mode, lifecycle · `book_policy.py`, `book_sizing_context.py`, frozen `dd_protection` | `size_book_request` inside `_dispatch_action_locked`; mode from settlement binding | Local / — / settlement-bound | None (portfolio policy) | Settlement equity/peak (T07) → mode | Settlement inputs are UNPROVEN (CAP S1–S5); T07 |
| C06 | Combined capacity and reservations (80-micro cap; reserve before send; release only on evidence) · rail R-E, E3 | `book_capacity.py` `Reserve`/`apply_event`; `CapacityLedger` | Local / — / local | CrossTrade Account Manager limits act after the fact (Q27, `DOCUMENTED` as actors). Not a pre-send reservation | Intents and facts → capacity events | Retain. Whole-intent **capacity** reservation per split applies in every mode (UB-1, ruled direction) |
| C06b | *PROVISIONAL-B:* account-wide loss check in exceptional mode · incident ADR §A2 rule 4 as scoped by UB-1 | Absent | Local / — / local | Venue trailing drawdown is enforced by Tradeify, not a pre-admission gate. Account Manager auto-close acts after loss (Q27) | Held unknowns + open positions + working entries + new request → loss room | New engineering. Figures owed at T16 (UB-6); UB-8 runs first. **D11** |
| C07 | Same-bar priority and Aegis takeover · rail S10, D-B8 | `FourLegRuntime` completed-bar barrier, `LEG_ORDER`; `book_takeover_owner.py` | Local / Tradovate cancel+close / local | Direct TV webhooks arrive in network order (route note §5): `CONTRADICTED` for priority. Takeover composite on the route: `UNVERIFIED` (K, A4) | Four bars → one ordered batch | Retain. Composite trace owed (gate C) |
| C08 | ORB resting stop entry: placement and cancellation · S2, L2(a) | Port emits a stop entry carrying its bracket at range completion. Its only own cancel is at the session-end bar. PROTECTED mode cancels pending adds. The owner validates the cancel target | Local / Tradovate resting stop via CrossTrade place / local | Creation `DOCUMENTED` (A4 S). `cancel_after` exists but is excluded by §A1. Day-order expiry: `UNVERIFIED`. Fate of Suspended children on cancel: `UNVERIFIED` (drill-map row 4) | Pending entry id → operation `reserved/attempted` | Local cancel stays required. **D18** |

### A2. Order execution and protection

| ID | Required behavior · governing owner | Current local implementation | Proposed owner: decision / execution / recovery | Vendor alternative · evidence | Inputs → authoritative state | Gap · residual work · Decision? |
|---|---|---|---|---|---|---|
| C09 | Per-fill protection from entry; no uncovered partial fills · R-B3 L2(b)/(e); §59 editions | Owner reserves full quantity, one command per intent. **No splitting code exists** (Vanguard prereg §3a) | Local split / Tradovate OSO, first-fill activation / local | OSO creation plus first-fill-sized activation: `DOCUMENTED` (A4; Q14/Q19). Activation at quantity 1: `UNVERIFIED` (D1). Residual cover L2(e): `CONTRADICTED` (A5), so one-contract requests are needed on this route whatever the posture. CrossTrade coverage repair: third-party actor, expected inert at quantity 1 (A8) | Intent qty → N child requests → per-child obligation | Build the split (T09). Sequencing (rule 10) and replay pricing are OWED. **D10**; UB-10 record **D11** |
| C10a | ORB exits after trail removal · ORB edition | Port re-issues its bracket every bar. With trailing removed and breakeven off (route note, effective binding), stop and target are fixed at range completion. The owner turns an unchanged amend into `noop` with no broker command (`book_protection_owner.py:595-617`) | Local (noop) / Tradovate fixed OCO / — | No trailing owner needed | Protection owner rows | ORB-2/3/4 OWED; the source supports ORB-4 "none". **D05** |
| C10b | Vanguard exits after trail removal · Vanguard edition | As C10a (prereg §3a VAN-4) | Local (noop) / Tradovate / — | As C10a | — | VAN-2..6/8 OWED. **D05** |
| C10c | Striker breakeven and bar-close trail ratchet · declared port | Port recomputes its stop from completed-bar close and emits `BracketAmend` every managed bar | **Local decision** / Tradovate modify via CrossTrade `change` / local | L2(c) atomic modify: `UNVERIFIED` (K; A4, drill D2). CrossTrade-managed trail is price-driven and its docs conflict (A9), so it is `CONTRADICTED` as a bar-close substitute | Signal-time references + latches → stop level per 1-lot child | Retained local duty. N modifies per bar per split. If D2 fails, a behavior decision follows. **D08** |
| C10d | Aegis one-time breakeven and target re-pin · declared port | Port emits one `BracketAmend` when its trigger is crossed | Local / Tradovate modify / local | L2(c) `UNVERIFIED` (K) | As C10c | **D08** |
| C11 | Whole-leg exits (EOD, max hold, stale, DD/daily limit) · S5, S7 | Every inspected port exit is a whole-position flat. `_reserve_close` scopes it to confirmed open fills | Local / CrossTrade `close` (liquidate) or N one-contract market exits / local | Full close L2(d): `UNVERIFIED` (K; D3). Partial or scoped close: `CONTRADICTED` (A5; leaves working orders). Each leg owns a distinct symbol, so a whole-leg exit is a full-symbol exit, provided the account is exclusive (A10) | Open fills → close reservation | Exit primitive choice is UB-5 (EVIDENCE-PENDING). **D06** |
| C11b | Close-time crossed-level exit (S3(d)): a re-issued stop already crossed at close exits at market · rail S3(d), AC-2 | Modeled only in `tv_broker_emulator.py:198-204`. No owner or rail realization found by name search in `ops/c1_rail` (absence `UNVERIFIED`) | Local / market exit / local | None: the broker would reject or immediately trigger a stop placed through the market (behavior `UNVERIFIED`) | Amend level vs bar close | Unbuilt, required for Striker. STR-5 OWED. **D07** |
| C12 | Scheduled cutoff and flatten; own-flat deadline · halt/resume §2, §5; S7 | `book_schedule.py`, `_advance_schedule_locked` driven by the loop's wall-clock `step` (independent of bars) | Local / CrossTrade close / attended on breach | Account Manager scheduled or window flatten exists as an actor (Q27, `DOCUMENTED` existence); semantics `UNVERIFIED`. As a backstop it would be a second close owner (incident ADR §2) | Session calendar → phase | Retain local as primary. A vendor backstop is optional and not recommended until qualified. **D13** |
| C13 | Order transport and identity; freshness; no duplicate dispatch · E3, rail R-B1 | Owner journals `UNKNOWN` before send (`:1674`). Occurrence identity and conflict halt. No production sender (`production_route_unavailable`, `:1684`) | Local / CrossTrade REST `orders/place` / local | `orderId`→`clOrdId` is a label, not an idempotency key (A1/Q05). REST returns child IDs synchronously (§6.5) | Attempt journal (one `clOrdId` per attempt) | Build the REST producer (T09). Interface rule: webhook-form traces do not qualify REST. **D16** |
| C14 | Late-reject detection · A7 | None (no route) | Local poll timer / CrossTrade status read / local | REST has no Alert History; the owner must poll (A7, `DOCUMENTED`) | Order status reads → terminal facts | New timer (T09) |

### A3. Recovery, reconciliation and operations

| ID | Required behavior · governing owner | Current local implementation | Proposed owner: decision / execution / recovery | Vendor alternative · evidence | Inputs → authoritative state | Gap · residual work · Decision? |
|---|---|---|---|---|---|---|
| C15 | Unknown request, **current posture**: preserve and block · E3; halt/resume §3–4 | `_ordinary_unknown_orders_db` → `unknown_order` refusal (`:768-798`, `:1608`) | Local / — / attended plus positive lookup | Same-session positive reconciliation `DOCUMENTED`; cross-session `UNVERIFIED` (D5); no fence (A1). A received HTTP status is no no-send guarantee (A3) | Attempt state `UNKNOWN` until an accepted terminal | Outcome classifier must follow A3 (i)–(iii). REST reads D4/D5 unauthorized. **D12** |
| C15b | *PROVISIONAL-B:* reservation-held unknowns; one obligation record per child (UB-10); re-evaluation on revoking events (UB-9); stop on stale monitoring (UB-3) | Absent; UB-10 extends `attempts` (`:764`, `:791`, `:1674`) | Local / — / local | No vendor obligation ledger. CrossTrade's 7-day `orderId` memory is a label (Q05) | Per-child state: unsent → submitted-unknown → acknowledged-working → filled / protection-unresolved / terminal | New engineering after UB-8. **D11** |
| C16 | Settlement and E1–E3 reconciliation · CAP S1–S5, rail E1–E3 | `book_settlement.py`, `account_close_*`; manual report exports (T07) | Local / — / operator exports | Complete causal history: `UNVERIFIED` (CAP R4); REST fill history has no `clOrdId` and unverified completeness (Q23/Q24) | Original report bytes → settlement chain | Retain. T07 |
| C17 | Restart recovery · halt/resume §2 "Process restart" | `FourLegRuntime.recover`, retained barriers and feedback; restart halts | Local / — / attended | Session-scoped reads; GTC children survive; the 7-day ID map survives (REST §6.6) | Durable journal | Cross-session lookup D5 unauthorized |
| C18 | Protection observation before any amend (fresh `W`) · rail E1, `AMEND` | Amend admission requires evidence after preparation (`book_protection_owner.py:584-587`). `ProtectionSnapshot` needs `stream_id`/`sequence`/`complete` (`book_protection.py:56-67`) | Local / CrossTrade reads / local | No documented REST read gives a complete, sequenced snapshot (REST §6.6). Per-order lifecycle reads: `DOCUMENTED` | Snapshot → protection owners | **Contract conflict:** the producer is unsourceable as specified. **D09** |
| C19 | Alert and configuration release identity · route note §5 (TV path); adapter pins (Python path) | `book_adapters.py` pins; `register_runtime_actor` with effective-inputs digest | Local / — / — | TV alert snapshots: not used on the recommended path | Pins → runtime actor | Nothing new on the recommended path |
| C20 | Liveness, source silence, barrier expiry, protection deadlines, heartbeat · halt/resume §2–3; T13 | `check_source_silence`, `expire_barrier`, `check_protection_deadlines`, daemon heartbeat | Local / — / attended | None monitors our process | Wall clock → halt | Channels and heartbeat provider unselected (T13). **D14** |
| C21 | Attended intervention and account exclusivity · halt/resume §3; UB-3; CAP R5 | Local fence and console model; the operator acts on the platform | Operator / Tradovate UI / operator | Copier and Account Manager actors are possible and uninventoried (A10) | Operator inventory | R5 inventory owed. **D13** |

**Orphan and owner check.** Every capability named in the handoff §3 A list maps to a row: calculations C01; continuity C02; counters C03; fill-dependent C04; sizing/mode C05; capacity C06/C06b; priority/takeover C07; stop entry C08; per-fill brackets C09; breakeven/trailing C10a–d; scoped closes C11/C11b; scheduled flatten C12; delivery identity C13; unknown requests C15/C15b; settlement C16; restart C17; releases C19; liveness C20; attended intervention C21. C14 and C18 are added execution sub-rows. Each row has one decision owner; no row has two execution owners, except C12 if a vendor backstop were enabled (D13).

---

## B. Deletion / reduction matrix

No file is deleted by this map. "Remaining consumers" come from import search at `d5effe5`. Key fact: the production qualification closure names `c1_rail.book_account_owner` as the `listener_account_owner` role, and lists `book_protection_owner`, `book_capacity`, `book_takeover_owner`, the ports, `book_protocol`, `feed` and `pine_ta` as bound code (`trust_domain.py:139-175`; `prepare_compute.py:78-87`). **Changing any of those modules changes the E1 freeze inventory.**

| ID | Component (exact) | Serves | Disposition | Replacement owner | Remaining consumers | Evidence / decisions to meet | Migration / rollback | Net burden |
|---|---|---|---|---|---|---|---|---|
| B01 | Live TradingView webhook ingress: durable intake queue, event-identity store, alert manifest, release admission (route note §4–5) | C13, C19 | **AVOID BUILDING** | Python host + owner occurrences | None (unbuilt) | Stands while the S2 ADR and Terms ruling stand | None | Removes a whole ingress subsystem |
| B02 | Pine market-input publisher (route note option B partition) and new publisher Pine expressions | C01, C02 | **AVOID BUILDING** (reopen only on D01) | Private ports | — | Terms permission, S2 amendment, cadence decision (D02) | — | Avoids new Pine identities and a second parity surface |
| B03 | Intrabar trailing manager; continuous protection price feed; CrossTrade-managed trail integration | C10a/b | **AVOID BUILDING** | Tradovate fixed OCO (editions) | — | Edition freezes (ORB-3, VAN-3). If an edition fails, the leg is rejected; no trail manager is built (prereg §6) | — | Avoids the largest custom subsystem the route note flagged |
| B04 | Automatic incident CLOSE/AMEND/ATTACH dispatch; programmatic vendor pause | — | **AVOID BUILDING** (already deferred by rev9) | Attended intervention | — | None | — | Keeps the status quo |
| B05 | ATTACH primitive path (`book_protection_owner.py` `primitive='attach'` for `ever_protected=False`) and L2(f) admission | C09 | **REDUCE** (live unreachable after the Striker edition) | Entry-carried OSO stop | Protection owner; qualification closure; tests | Striker edition frozen and requalified (STR-1) | Rebind the qualification closure if code changes; simplest is to leave the code and refuse live | Small; no deletion before freeze |
| B06 | Live use of trailing-bracket fields (`Bracket.trail_*`, B1 optional fields, L2(g) gating) | C10a/b | **REDUCE** (live sender refuses trailing fields per §A1) | Fixed OCO | `book_protocol.Bracket`, emulator and replay (historical parity needs them) | Edition freezes | Keep the protocol unchanged; add a live-sender guard | Adds one guard, removes a whole L2(g) path |
| B07 | Partial-fill residual-cover logic (L2(e) realization) | C09 | **AVOID BUILDING** | One-contract requests | — | A5 direction discharged at freeze | — | Removed |
| B08 | Private ports, `tv_broker_emulator.py`, `pine_ta.py`, `book_parity.py`, `book_bundle_*` | C01, C03, C04; qualification | **RETAIN** | — | Qualification replay, source admission, benchmark, trust domain | Not removable because live signal hosting stays in Python, and offline qualification needs them anyway | — | — |
| B09 | Production bar feed (`BarSource` provider, T14) | C02 | **RETAIN** (funding **DEFER**, O-4) | — | `book_evaluate_loop` sources | No permitted vendor alternative (C02) | — | Irreducible on the ruled host |
| B10 | `FourLegRuntime`, `FourLegEvaluateLoop` (no CLI or config yet) | C03, C04, C07, C17, C20 | **RETAIN** | — | `daemon.py` import, listener handlers | — | Production wiring is T09/TB-I3 scope | — |
| B11 | `BookAccountOwner` core (occurrences, attempts, capacity, sizing, schedule, takeover, halt) | C05–C07, C12, C13, C15–C17 | **RETAIN** | — | Qualification role `listener_account_owner` | — | Any change re-enters the freeze inventory | — |
| B12 | Protection owner amend path | C10c/d, C18 | **RETAIN**; **REDUCE** the observation contract | — | Qualification closure | D09 contract decision; D2 L2(c) trace | Contract amendment before the T09 producer | Striker/Aegis need it; ORB/Vanguard reduce to noop |
| B13 | One-contract split, per-symbol sequencing, whole-intent capacity reservation | C06, C09 | **RETAIN (requirement; unbuilt)**. Sequencing is *PROVISIONAL-B* (rule 10) | — | — | UB-4 freezes with the editions; replay pricing OWED | New owner code (T09) | Introduced |
| B14 | Close-time crossed-level exit realization (S3(d)) | C11b | **RETAIN (requirement; unbuilt)** | — | Emulator already models it | STR-5 | New owner code | Introduced |
| B15 | REST producer: place, status/lifecycle/fill reads, post-placement poll, same-session recipe | C13–C15, C18 | **RETAIN (requirement; unbuilt)** | CrossTrade REST | — | Drill map; REST-form traces; D4/D5 authorization | New adapter (T09) | Introduced, replacing `SyntheticBroker` in production |
| B16 | *PROVISIONAL-B:* UB-10 per-child obligation record; UB-1 loss model; UB-9 re-evaluation triggers | C06b, C15b | **DEFER** until UB-8 and B acceptance | — | — | UB-8 availability assessment; §A8 step-4 reviews | Extend `attempts`; no parallel ledger | Introduced only if B is needed for first release |
| B17 | Legacy single-strategy B1 path: `c1_rail_listener.handle_signal`, `crosstrade_payload.py`, `c1_sizing_host_reference.py`, `c1_rail_http_server.py` POST route, fixed-book guard | M1 test identity | **RETAIN** (guard must stay); any wider change **DEFER** | — | `c1_rail_arm`, `m1_stage1_control`, http server | Out of this route's scope | — | `crosstrade_payload` is not reusable as the book sender (B1 schema, 10 s synchronous send) |
| B18 | M1 stage-1 machinery (`daemon.py` single-strategy loop, `operator_input_source`, `m1_stage1*`) | M1 (completed) | **DEFER** | — | Arming interlock via acceptance validation | Separate owner decision | — | None here |
| B19 | Settlement modules and the manual export procedure | C16 | **RETAIN** | — | Owner, qualification closure | No vendor producer (CAP R4) | — | — |
| B20 | Vendor-side actors (copier, Account Manager auto-close/flatten, Block Signals) | C12, C21 | **AVOID** enabling any not inventoried; **RETAIN** the attended inventory | Operator | — | R5 inventory | — | Avoids unowned second actors |

**Deletion readiness:** no REMOVE CANDIDATE row has met its conditions. The reductions (B05–B07) wait on edition freezes and requalification. The largest savings (B01–B04) are avoided builds, which need no deletion.

---

## C. Minimal-controller boundary (assessment boundary, not a specification)

```
 T14 feed (UNSELECTED, O-4) ── completed 15m bars ×4 ──┐
                                                        ▼
                ┌──────────── OUR CONTROLLER (one host, one durable writer) ─────────────┐
                │ FourLegRuntime barrier ─► private ports (decision state, counters)       │
                │        │ ordered actions (LEG_ORDER, takeover)                            │
                │        ▼                                                                  │
                │ BookAccountOwner: occurrence identity → sizing/mode → capacity reserve    │
                │   → [PROPOSED] 1-lot split + per-symbol sequencing (B13)                  │
                │   → attempt journal UNKNOWN-before-send → REST adapter [PROPOSED, B15]    │
                │   facts in: fills / terminals / protection reads → port feedback          │
                │   unknowns: preserve-and-block (current) | reservation + UB-10 (PROV-B)   │
                │ timers: schedule cutoff/flatten · source silence · barrier expiry ·       │
                │         protection deadline · post-placement poll [PROPOSED] ·            │
                │         heartbeat/notify [T13] · UB-9 re-evaluation [PROV-B]              │
                └──────┬──────────────────────────────────────▲──────────────────────────────┘
          place OSO 1-lot · change · cancel · close           │ ids, errors, status, lifecycle, fills
                       ▼                                      │ (session-scoped; no complete snapshot)
              CrossTrade REST (transport, id map; coverage-repair actor, inert at 1 lot)
                       ▼                                      ▲
              Tradovate: matching, resting stop entry, OSO first-fill activation,
                         fixed stop/target execution between bars, OCO sibling cancel
 Operator: attendance, platform intervention, R5 inventory, settlement exports, alert creation (none live)
 TradingView: research/export only (no live role; Terms §3 ruled applicable)
```

**Why each surviving local responsibility survives the vendor comparison**

| Local responsibility | Substantiated vendor gap |
|---|---|
| Signal computation and decision state (ports) | The TV live role is not permitted (C01). CrossTrade has no strategy logic. Qualification needs the ports anyway. |
| Completed-bar barrier, priority, takeover | Vendors see independent requests; network arrival order cannot supply portfolio priority (C07). |
| Sizing, mode, capacity, loss check (PROV-B) | No vendor holds portfolio policy or pre-send reservations (C05, C06, C06b). |
| Intent-before-send journal, identity, unknown accounting | `clOrdId` is a label; there is no fence; A3 forbids treating a status as no-send (C13, C15). |
| Split and sequencing | L2(e) is contradicted, and the stop activates at first-fill size (C09). |
| Striker/Aegis amend decisions | Bar-close ratchet and one-time re-pin are strategy decisions; the vendor trail is not equivalent (C10c/d). |
| Close-time crossed-level exit | The broker has no "exit if the close crossed the new level" primitive (C11b). |
| Schedule and own-flat deadline | Vendor flatten semantics are unverified, and a vendor flatten would be a second owner (C12). |
| Settlement and reconciliation | No complete causal history producer (C16). |
| Watchdogs and post-placement poll | No vendor monitors our host; REST lacks Alert History (C14, C20). |

**Unknown producers:** the feed provider (C02); the fill/terminal/protection read producer (C04, C18); the notification channel (C20); the R5 inventory (C21).

---

## D. Decision and evidence queue

**GB** = gate-B behavior/contract item (operator; fed back, not adopted). **GC** = gate-C evidence. **P** = permission.

| # | Class | Question | Rows | Current rule | Proposed alternative | Benefit | Behavior change | Evidence / requalification owed | Owner |
|---|---|---|---|---|---|---|---|---|---|
| D01 | P | May any TradingView-hosted live path be evaluated? | C01, C02, B01, B02 | Terms §3 ruled applicable (2026-09-11); S2 Python host | Keep as is (recommended); or obtain written TradingView permission for the exact non-display use, then amend S2 | Removes the feed and live-port burden only if permitted | Yes, if TV hosts signals (route note §3) | Written licence evidence; no vendor contact by agents | Operator |
| D02 | P/GB | Striker and Vanguard Pine declare per-tick calculation. Which realtime semantics apply? | C01 | Accepted definition = completed-bar ports matching historical exports | Moot on the recommended path; decide only if D01 opens TV hosting | — | Only on a TV path | — | Operator (conditional) |
| D03 | GB (resolved by direction) | Who owns intrabar trailing? | C10a/b, B03 | Declared ORB and Vanguard need L2(g) (A5, A6) | None, via the three editions; an edition NO-GO rejects that leg | No trail manager or feed | Yes, already ruled (§59 Rulings 3–4) | Freeze ORB-3 and VAN-3; E1 requalification | Operator |
| D04 | GB | Striker initial bracket timing: which stop rides the entry (STR-2)? | C09, C10c | Declared: bare entry, first stop issued one bar later | Option (a). Source finding: the port computes its stop level on the signal bar, so it is computable at entry. The declared first-attached level can differ, because the next bar's breakeven/ratchet update may move it | Protection from entry; removes ATTACH | Yes | Freeze STR-2; E1 | Operator |
| D05 | GB | Remaining OWED edition rules: ORB-2/3/4/6, STR-3/4/6/7, VAN-2..6/8 | C09–C11 | DRAFT pre-registrations | Source-grounded suggestions: ORB-4 = "none" (the per-bar re-issue is a noop once trail and breakeven are off; breakeven-off rests on the route note's effective binding, not re-read here); ORB-3 = existing fixed stop, target, max hold when enabled, EOD flat; STR-6 = modifies every bar (L2(c) dependency, D08); VAN rows per prereg §3a | Freezes the editions | Yes | Pre-registration freeze; E1 | Operator |
| D06 | GB/GC | UB-5: which exit primitive? | C11, B13 | UB-5 EVIDENCE-PENDING; §A8 "moot" withdrawn | Whole-leg exits as a full-symbol close (each leg owns a distinct symbol), if D3 passes and R5 shows exclusivity; otherwise N sequential one-contract closes with replay pricing | One close per exit; fewer races | None for a qualified full close; price path changes for split closes | D3 trace; R5; exit replay model (OWED) | Operator; coordinator for evidence |
| D07 | GB | STR-5: realize the close-time crossed-level exit as a market exit of scope, as declared? | C11b, B14 | Rail S3(d); emulator only; no owner code | Build in T09 as declared | Preserves accepted behavior | None if as declared | E1; owner test | Operator (rule), coordinator (build scope) |
| D08 | GC → GB on failure | Does L2(c) hold: the old stop survives a rejected modify, for per-child modifies at Striker cadence? | C10c/d | K | D2 trace (webhook form; REST form separately) | — | If it fails: a non-atomic cancel/replace (CAP-rejected) or a fixed-stop Striker (strategy change) | D2; REST-form equivalence | Coordinator; operator on failure |
| D09 | Contract (GC) | The amend admission needs a complete, sequenced protection snapshot that no documented REST read supplies. Change the contract? | C18, B12 | `ProtectionSnapshot` `complete`/`sequence` (rail E1) | Per-order fresh lifecycle/status read after preparation as the evidence for the targeted order, with E1 whole-account coherence kept for recovery only | Makes the amend path implementable | No strategy change; contract change | Rail spec E1 owner review; REST read trace | Coordinator → operator ratification |
| D10 | GB | Split sequencing and replay pricing (rule 10, UB-4, prereg §6 entry and exit models) | C09, B13 | OWED; blocks freeze | Sequential one-contract requests with a stated per-request price/delay rule, applied to exits too | Bounds held unknowns to one per symbol | Yes (fill prices; abandoned remainders) | Replay model in both pre-registrations | Operator + coordinator |
| D11 | GB | Is option B needed for the first release, and with what controller scope? | C06b, C15b, B16 | Preserve-and-block governs | UB-8 assessment first. If B is needed: UB-1 loss model, UB-10 per-child record extending `attempts`, UB-9 revocation events, UB-3 stops | Continuity after an unknown | Yes (admission in exceptional mode) | UB-2/6 figures; §A8 step-4 reviews; replay | Operator |
| D12 | GC | Authorize REST reads D4 (same-session recipe) and D5 (prior-session lookup)? | C15, C17 | Unauthorized | Add them to an operator session plan | Establishes what reconciliation can resolve (UB-7) | None | Operator-performed traces | Operator |
| D13 | GB/P | R5 actor inventory and exclusivity; should a vendor scheduled flatten act as a backstop? | C12, C21, B20 | Uninventoried | Inventory first. No backstop until qualified, because it would be a second close owner | Enables D06 and UB-7 | A backstop would be one | R5 inventory; backstop qualification if wanted | Operator |
| D14 | GC | Notification channel and heartbeat provider (UB-3 thresholds) | C20 | Unselected (T13) | Select in T13 | Enables UB-3 | None | T13 traces | Coordinator/operator |
| D15 | P (funding) | Production feed provider (O-4) | C02, B09 | Deferred | Fund at the source-independent checkpoint | Required on the recommended path | None | T14 | Operator |
| D16 | GC | T09 interface: REST or webhook form? | C04, C13, C14 | Undecided; interface rule (Gate A) | REST (positive recovery, A1) plus a post-placement poll (A7) | Better recovery | None | REST-form traces, or an accepted equivalence argument | Coordinator |
| D17 | Evidence | Are ORB adds enabled in NORMAL mode under the accepted binding? The route note says "adds-off binding"; the selection note says up to two adds, off under protection | C06, C09 | Effective inputs not read (outside §60) | Coordinator confirms from the owner record | Correct split and capacity inputs | None | Record check | Coordinator |
| D18 | GC | ORB resting-entry end of life: local session-end cancel (the only mechanism in the narrowed shape), and what happens to Suspended children | C08 | K (drill-map row 4) | Keep the local cancel; D6 trace | — | None | D6 | Coordinator |

---

## E. Evidence and return

### Source inventory and hashes (SHA-256 prefix at `d5effe5`)

| File | Hash |
|---|---|
| `ops/c1_rail/book_account_owner.py` | `724667a250ed6998…` |
| `ops/c1_rail/book_protection_owner.py` | `b4da2884c68b438c…` |
| `ops/c1_rail/book_protection.py` | `ff883056478b9b9c…` |
| `ops/c1_rail/book_policy.py` | `ffcd3aab3e74235e…` |
| `ops/c1_rail/book_capacity.py` | `95381097d2799175…` |
| `ops/c1_rail/c1_rail_listener.py` | `a9cba7f0d97e8a28…` |
| `ops/c1_rail/crosstrade_payload.py` | `4ac29b306b08b125…` |
| `ops/c1_rail/qualification/trust_domain.py` | `c4b669383b300689…` |
| `ops/c1_signal_daemon/book_protocol.py` | `743117ea79af2a83…` |
| `ops/c1_signal_daemon/book_runtime.py` | `def3790310cba563…` |
| `ops/c1_signal_daemon/book_adapters.py` | `c6ad40bd54d11545…` |
| `ops/c1_signal_daemon/book_evaluate_loop.py` | `9dbc7ace4e173bea…` |
| `ops/c1_signal_daemon/feed.py` | `b94e43c0e3410a82…` |
| `ops/c1_signal_daemon/tv_broker_emulator.py` | `2be77babd618995d…` |
| REST assessment (Gate A text) | `17d35023403e0d1a…` |
| Route note | `ef8bd9175df24203…` |
| Incident ADR (incl. §A9.1) | `b31390f490a8a2d3…` |
| Allocation handoff at dispatch | `c24c1ff00a4cfcd8…` |
| Private sources | The eight `BOOK_SOURCES.sha256` pins, all OK in place (2026-09-26) |

Vendor evidence is reused from Gate A (Q-index, `MANIFEST.tsv` `d069ae7e…`); no fresh retrieval. TradingView terms evidence: S2b ADR addendum 2026-09-11 (page read on 2026-09-11; not re-read).

### §4 acceptance-case traces (recommended path)

| Case | Trace and outcome | Minimum later observation |
|---|---|---|
| Two legs near shared capacity, opposite arrival order | Both bars enter one barrier; the batch is ordered by `LEG_ORDER`, then admitted serially under the account lock. Arrival order is irrelevant. Takeover runs through S10 before any displaced dispatch | Takeover composite trace (K) |
| Simulated base; the actual entry is refused, partial or unknown; an add follows | No simulation: ports see only owner facts. A refusal is retained, and counters are not refunded (C03). Partial fills are impossible at 1 lot. An unknown blocks adds (current) or is held (PROV-B). An add needs a closed submission sequence (UB-4) | D1; UB-4 freeze |
| ORB stop placed, cancelled or triggered, then an exit | Placement is a resting Tradovate stop with OSO. A fill is a broker fact, not the emulator. The session-end cancel is local. A trigger activates the stop/target; EOD flat closes the leg | D1, D6 |
| Striker initial bracket; Vanguard/ORB trails | Striker's stop rides the entry (STR-2). No trail activates on any leg under the editions. Striker's ratchet is a bar-close modify (L2(c) K); an intrabar path is never reconstructed | D2; edition freezes |
| Native protection fills before the strategy exit; takeover or flatten overlaps | The protective fill becomes a fact that consumes the protection owner row. A later port flat finds no open fills and is refused, or reserves only the remainder. `close_unreconciled` blocks risk-adds while any close is non-terminal | D3; per-child close ordering (UB-5) |
| Webhook duplicated, lost, late or stale | Not applicable (no inbound webhook). Bars: a duplicate is a no-op, a conflict halts, and a stale or noncontiguous bar halts (`book_runtime.py`) | Feed qualification (T14) |
| Entry/cancel/amend/close response lost | Attempt stays `UNKNOWN`; same-session lookup only for located facts (A3 (iii)); no resend. An unknown non-entry follows the protection-uncertain row (attended) | D4/D5 (unauthorized) |
| Restart, source silence, session/contract roll | Restart halts and restores durable state with no automatic mutation. Silence halts on the wall-clock watchdog, independent of bars. The schedule deadline runs on its own timer. Roll mapping is owed by T14 | T13/T14 traces |
| Delete a feed, daemon, module or state store | No deletion recommended. B05/B06 wait on freeze and a qualification-closure rebind. The feed and daemon are retained (no permitted alternative) | — |
| Delegate to a vendor | Only Tradovate-native OSO/stop/target and CrossTrade transport are delegated, each tied to its A-row evidence and a named drill. No NinjaTrader or ATM capability is claimed | D1–D3, D6 |

### Limitations

- Documentary only. No capability here is route-qualified. Every vendor allocation still needs its drill-map trace in the selected interface form.
- Private reads were limited to action and exit branches. Effective bindings were not read (outside §60), so edition suggestions resting on them are attributed.
- The absence claims (no split code; no close-time exit realization) come from name search plus reading the dispatch path. They are `UNVERIFIED` absence, not proof.
- Import search covers `ops`, `core`, `lab`, `scripts` and `tools`. Test consumers were counted but not traced.

### Verdicts (assessment verdicts, not deployment approval)

- **Technical allocation: CONDITIONAL MINIMAL BOUNDARY IDENTIFIED.** The boundary is §C. It is conditional on: the three editions freezing with D04–D07 and D10 answered; K primitives L2(c), L2(d), Suspended-child cancel and the takeover composite passing their traces; D09's contract change; the posture choice D11. No leg needs an unsupported primitive once the editions freeze.
- **Permission readiness: UNRESOLVED.** TradingView live use is ruled impermissible under Terms §3 (so the recommended path gives TradingView no live role). CrossTrade Pro REST entitlement is vendor-reported, not account-verified (Q01). Venue acceptance of CrossTrade-mediated automated orders on this eval rests on the automation-friendly firm listing; its compliance owner note is not in this checkout and was not re-verified.
- **Deletion readiness: NONE ESTABLISHED.**

### One next action

Coordinator reviews this map for gate D, then authors the **integrated gate-B/C decision packet** for the operator. It covers D04–D08, D10 and D11, with the UB-8 availability assessment as its first sub-deliverable, and D09 as a contract proposal. **Acceptance criterion:** each gate-B item has an operator answer in words, recorded in its owner (the pre-registrations or incident ADR §A2/§A8), or an explicit hold. The gate-C per-leg requirement-to-route map then has no required U primitive without an accepted resolution, and names the trace owner for every K primitive. After that, a bounded T09 handoff can be drafted against §C.
