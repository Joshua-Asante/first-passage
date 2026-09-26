# Tradeify route: integrated B–D decision packet

**Status:** DRAFT for operator review (2026-09-26). Coordinator-authored. It accepts no gate, changes no contract or behavior, and grants no drill, access, spend or GO. Gates B–D stay pending until the operator rules and the coordinator records integrated acceptance on the [T09 gate table](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t09-gate-acceptance-record).
**Inputs:** Gate A ([REST §6.11](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#611-gate-a-factual-disposition)); the [allocation map](2026-09-25-tradeify-capability-allocation-deletion-map.md) (read its coordinator-corrected section first); incident ADR [§A9–§A10](../adr/2026-09-17-bounded-platform-protection-incident-contract.md); the rail spec's [R-B3 / L-2](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md); campaign §59 Rulings 3–4; the three edition pre-registrations. Parallel drafts: [dispatch card](../briefs/handoffs/2026-09-26-bd-packet-parallel-drafts.md) (UB-8 comparison; S5 decision draft).
**Route assumed:** the ruled Python signal host → our account owner → CrossTrade-mediated Tradovate REST. TradingView's exclusion is the standing 2026-09-11 ruling. Account entitlement and venue permission remain evidence owed (§4, P-1).

| § | Content | State |
|---|---|---|
| 1 | Gate C: decisive capabilities, validation and failure consequences | Drafted below |
| 2 | Gate B: remaining behavior decisions | Drafted below |
| 3 | Unknown-request posture and option-B rules, with unresolved assumptions | Drafted below |
| 4 | Allocation and component reductions (gate D) | Drafted below |
| 5 | T09 handoff (held until B–D acceptance) | Drafted below |
| 6 | Decisions required from the operator | Drafted below |

---

## 1. Gate C — decisive capabilities

**Rule applied.** The rail spec's L-2 applies: "every item a port uses must be `supported` … missing evidence or an unsupported item makes the live packet `BLOCKED — capability-problem`". A cancel/replace cannot satisfy L2(c), and a concurrent cancel plus close cannot satisfy L2(d). Every row below states its failure consequence as either **ROUTE STOPS**, meaning the live packet is BLOCKED for the affected legs until a contract change is accepted, or **OPERATOR EXPRESSION CHANGE**, meaning an operator-owned edition change plus requalification.

**Evidence labels** follow the allocation map: `DOCUMENTED`, `OBSERVED FOR EXACT SCOPE`, `CONTRADICTED`, `UNVERIFIED`. No row is observed yet. The drill references use the Gate A drill map, which is keyed by behavior. **A trace counts only for the interface it exercised:** webhook-form traces do not qualify REST unless an equivalence argument is accepted.

### 1.1 GC-1 (D19): close and protection cleanup — first-order blocker

**Why it blocks.** Every inspected port exit is a whole-leg flat (allocation map C11). Striker also needs the close-time crossed-level exit, which is a triggered-protection close (C11b; rail S3(d)). The contract's `CLOSE` needs **L2(d)**: an atomic scoped close with attached-order removal, including a quantity-less close on an exclusively owned symbol. It also needs **L2(e)**: atomic protection adjustment to the residual on every partial fill, with no reverse exposure. L2(e) is contradicted on this route (Gate A A5), and partial or scoped close leaves working orders behind (A5). One-contract **entries** do not settle close semantics:
- a close of N lots can finish partly;
- a protective fill can race the close;
- a close sent after a protective fill can reverse the position.

UB-8 cannot make an unqualified close route viable.

**Candidate realizations.** None is qualified; the operator chooses which one to pursue.

| Option | Mechanism | L2 fit | Main risk | Evidence needed | Assessment |
|---|---|---|---|---|---|
| **C-a. Broker liquidate for whole-leg exits** | CrossTrade `close` → Tradovate `liquidateposition` on the exclusively owned symbol. It is quantity-less. The route documents that it cancels the OCO children and closes the position, but that is **not verified** (K; REST §6.6 partial-fill row; A4) | L2(d) as written, **if** D3 shows cancel-and-flatten with no residual working order. L2(e): an interpretation is needed for the transient in which the brackets are gone and the liquidation remainder is still working | Race: a protective stop fills while the liquidation is in flight, so a flatten computed on stale quantity could reverse the position (`UNVERIFIED`). Liquidate is documented as a request, not a guarantee (A4) | D3 in REST form, plus a **race observation**: liquidate while a protective order is working near the market, and show no reverse position. Also the R5 exclusivity inventory (D-B9 needs an exclusively owned symbol) | **Recommended to pursue first.** It matches every whole-leg exit. It needs one contract interpretation (§1.1a) and the race evidence |
| C-b. Exit through the lot's own OCO | Amend each lot's target to a marketable level so that the broker-native OCO fills and cancels its sibling stop | L2(d) per lot by the broker's own OCO. L2(e) is moot at one contract | Needs L2(c) (K; D2) for every lot. A modify through the market may be refused or behave differently. A leg without a target has no carrier. It changes the exit order type and price path, which is a behavior change | D2 plus a marketable-limit amend trace | Fallback if C-a fails. It is an **operator expression change** |
| C-c. Market exit per lot, then cancel its bracket | Two requests | **Fails** L2(d) as written ("concurrent cancel/close cannot satisfy (d)") | Orphan protection, and a reverse position if the stop fills between the two requests | — | **Not recommended.** It needs a contract change that accepts the known race |

**§1.1a — the contract interpretation that C-a needs (for gate B; not adopted).** L2(e) exists so that a *partial* reduction never leaves the residual unprotected or reversed. For a **whole-scope** close by broker liquidation on an exclusively owned symbol, the proposed reading is:
- L2(e) is satisfied when the broker's own flatten order owns the residual until it is flat;
- no residual protection is required once the intent is to be flat;
- **reverse exposure remains forbidden**, and D3 plus the race observation must show it cannot occur.

The crossed-level exit (S3(d)) is realized as the same whole-leg liquidation when every lot's newly issued level is crossed. If only some lots are crossed, that is a **scoped close**, which is U on this route. Striker's edition must then either (i) confirm that its lots share one level, so a crossed close is whole-leg, or (ii) accept a behavior change. That goes to STR-5 (gate B).

**Failure consequence.**
- **C-a fails** (liquidate leaves residual orders, or reverses under the race): **ROUTE STOPS for all four legs.** There is no admissible exit, and C-c is excluded. Try C-b as an operator expression change, or reject the route.
- **The partial-lot crossed-level case is unsupported:** **OPERATOR EXPRESSION CHANGE** for Striker (STR-5).

### 1.2 Other decisive capabilities

| ID | Capability (rail item) | Legs | Current evidence | Validation method · owner | Pass criterion | If it fails |
|---|---|---|---|---|---|---|
| GC-2a | Stop activation on the entry's first fill at quantity 1 (§A1; L2(b)) | All | Creation `DOCUMENTED`; activation at qty 1 `UNVERIFIED` | D1 (REST form) · operator performs, coordinator records | The child stop is `Working` at qty 1 after the fill, linked to the entry; activation interval measured | **ROUTE STOPS for all legs.** The one-contract premise fails, and no entry is protected from fill |
| GC-2b | Rejected modify keeps the old stop (L2(c)) | Striker (per-bar ratchet), Aegis (breakeven/re-pin); C-b if used | `UNVERIFIED` (K) | D2 (REST `change`, command report) · operator/coordinator | The old stop stays `Working` at its old price after the rejection; an unknown modify is reconciled before any retry | **OPERATOR EXPRESSION CHANGE** for Striker and Aegis: a fixed-stop edition, with no per-bar or once-only amend. A cancel/replace cannot substitute. ORB and Vanguard are unaffected (noop amends) |
| GC-3 | Evidence freshness and coherence for amend and close completion (rail evidence-currency rule; C18) | Striker, Aegis (amend); all (close completion) | Per-order lifecycle reads `DOCUMENTED`; account-wide causal order `UNVERIFIED` (CAP R4). A poller sequence orders **our** observations only | Design, then trace: show that post-preparation lifecycle and status reads carry broker timestamps or versions that postdate `prepared_at`, and that the reads used for one decision describe one coherent state (for example a re-read bracket, or version equality) · coordinator (design), operator (trace) | Each completion or no-op determination rests on broker-sourced evidence proven to postdate preparation and to be coherent for the targeted scope | Amend: **OPERATOR EXPRESSION CHANGE** (as GC-2b). Close completion: **ROUTE STOPS**, because a close could never be completed |
| GC-4 | Cancel of a resting stop entry ends its Suspended children | ORB | `UNVERIFIED` (drill-map row 4; session plan D4 / REST return D6) | Trace · operator | Parent and both children terminal; no fill | **OPERATOR EXPRESSION CHANGE** for ORB (for example an attended session-end procedure or a different end-of-life rule), or accept a cleanup read that closes the orphans before the next session. Not route-wide |
| GC-5 | Takeover composite (cancel plus close for the displaced leg, then admission) | Aegis | `UNVERIFIED` (K) | Documentary sequence under GC-1 C-a, then a trace · coordinator/operator | The displaced leg is flat with no residual orders before the Aegis entry is admitted | **OPERATOR EXPRESSION CHANGE** for the takeover rule (for example no takeover, which queues or skips) |
| GC-6 | REST reconciliation: same-session recipe (D4) and prior-session lookup (D5) | All | Same-session `DOCUMENTED`; cross-session `UNVERIFIED` | Operator-performed reads, **not yet authorized** (D12) | D4 locates by `clOrdId` and recovers children and fills; D5 shows whether a prior-session order is readable by id | This does not stop the route under preserve-and-block. Unknowns stay blocking, and the cost shows up in UB-8. Under B, it limits what UB-7 can resolve |
| GC-7 | Account actor inventory and exclusivity (CAP R5; D-B9) | All | `UNVERIFIED` (A10) | Operator inventory of copier, Account Manager, other platforms and manual sessions · operator | No actor other than this runtime can place, modify or close on the four symbols; any exception is documented and disabled | **ROUTE STOPS** while C-a is the close realization, because D-B9's quantity-less close needs exclusive ownership. Otherwise the result is a named actor to disable |
| GC-8 | Late-reject detection by polling (A7) | All | `DOCUMENTED` (no Alert History) | T09 design, then trace · coordinator | A rejected child or bracket is detected within the protection deadline | This is design work, not a route stop. The protection deadline (halt/resume §2) bounds it |

**Priority order.** GC-1 first (it decides whether any exit exists), then GC-2a, GC-7, GC-3, GC-2b, GC-4 and GC-5, with GC-6 and GC-8 in parallel. D1–D3 and D6 are authorized in principle in webhook form only. **REST-form traces for GC-1, GC-2a, GC-2b, GC-3 and GC-4, and the D4/D5 reads, need a revised operator session plan.** The race observation in GC-1 is new and needs its own written authorization.

---

## 2. Gate B — remaining behavior decisions

Each row is the operator's to rule, in words and without parameter values, in its owner. "Recommendation" is the coordinator's. The source-grounded suggestions come from the allocation map §D; private reads were in place only. Nothing is adopted here.

| ID | Decision (owner) | Recommendation | Depends on | Blocks |
|---|---|---|---|---|
| B-1 | **Close realization (D19).** Which GC-1 option to pursue, and whether to accept the §1.1a L2(e) interpretation for whole-scope broker liquidation (rail spec R-B3; incident ADR UB-5) | Pursue **C-a**, and accept §1.1a subject to the D3 plus race evidence. Keep C-b as the fallback expression change. Reject C-c | GC-1 traces; GC-7 | Every exit; T09 |
| B-2 | **Exit-split rows** ORB-6, STR-7, VAN-8 (pre-registrations) | Rewrite them to follow B-1. Under C-a, a whole-leg exit is **one broker liquidation**, not N one-contract closes. The "must become one-contract closes" premise is withdrawn with UB-5 | B-1 | Edition freeze |
| B-3 | **Striker initial stop, STR-2** (D04) | Option (a). The source shows the port computes the stop level on the signal bar, so it is computable at entry. The first attached level can differ from the declared one-bar-later stop, so treat this as a qualified behavior change in E1 | — | Striker freeze |
| B-4 | **ORB fixed-stop rules**, ORB-2/3/4 | ORB-2: the existing fixed-stop component, unchanged. ORB-3: the trail's former exits now close through the existing fixed stop, target, max hold (when enabled) or EOD flat; the pre-registration must account for the changed holding periods, overlap and capacity. ORB-4: **none**, since the per-bar re-issue becomes a noop once trail and breakeven are off. The breakeven-off fact rests on the recorded effective binding; confirm it in the owner | — | ORB freeze |
| B-5 | **Vanguard fixed-stop rules**, VAN-2/3/4 | As B-4, per the pre-registration §3a findings. VAN-3 needs the full account of remaining exits that §59 Ruling 4 requires | — | Vanguard freeze |
| B-6 | **Split size and partial acknowledgement**: STR-3/4, VAN-5/6 | Adopt the UB-4 first-release rule. Reserve the whole intent; send sequentially after a defined acknowledgment; on refusal, unknown, cutoff, takeover or flatten, abandon the unsent remainder; never retry or top up; a base supports adds only after its sequence closes and the approved rule holds. The VAN-6 counter wording states whether the add counter advances at proposal (as declared) | — | Freezes; replay |
| B-7 | **Striker close-time crossed-level exit**, STR-5 (D07) | As declared **when every lot is crossed**, realized as the B-1 whole-leg close. If lots can have different levels, a partly crossed case is a scoped close (U), so either the edition confirms a shared level or a behavior change is ruled | B-1; source check | Striker freeze |
| B-8 | **Striker per-bar stop modify**, STR-6, and Aegis breakeven/re-pin | Keep them as declared, dependent on GC-2b. If GC-2b fails, a fixed-stop edition for the affected leg (operator expression change) | GC-2b, GC-3 | Striker and Aegis |
| B-9 | **Split sequencing and replay pricing** (D10; §A8 rule 10; each pre-registration's §6) | Sequential one-contract entry requests, with a stated per-request delay and price rule in the replay. Exits follow B-1 | B-1 | Freezes; E1 |
| B-10 | **Option B for the first release** (D11; incident ADR UB-8 and §A10 acceptance condition) | Pending the UB-8 comparison (§3) | UB-8 | §3 rules; T09 scope |
| B-11 | **Takeover under the route** (GC-5) | Keep as declared, realized as the B-1 close of the displaced leg followed by admission. If GC-5 fails, a takeover behavior change | B-1; GC-5 | Aegis |
| B-12 | **Account actors and backstop** (D13; GC-7) | Inventory first. No vendor scheduled flatten as a backstop until qualified, since it would be a second close owner | — | C-a; UB-7 |

**Authorizations needed (operator authority, not behavior):**
- **A-1.** A revised operator session plan covering: REST-form D1–D3 and D6; the REST reads D4/D5 (D12); and the new GC-1 race observation. Each is bound to exact operations and account scope. The reads are separate from order-producing drills.
- **P-1.** Evidence of account entitlement (CrossTrade Pro REST) and of venue permission for CrossTrade-mediated automated orders on this eval. A firm-level "automation-friendly" classification is insufficient.

---

## 3. Unknown-request posture and option-B rules

**Input:** the [UB-8 comparison](2026-09-26-ub8-availability-comparison.md) (accepted as input; its coordinator review records the source checks on Q1–Q3).

**Recommended first-release posture: preserve-and-block** (the current rule, `book_account_owner.py:1608`). **Option B stays Proposed** for a later release; §A10's acceptance condition already provides for this. Reasons:
- **B's continuity, as the texts stand, is limited.** An unknown still triggers the halt/resume §2 halt and the §3 return to flat, so B buys *resume after an attended return to flat*, not uninterrupted trading (UB-8 Q1; BE-5).
- **None of the conditions under which B pays can be shown today.** B pays only in a band: when the expected number of unresolved requests over the first-release horizon, λH, is above the operator's tolerance ε but below the number of held reservations the room can absorb, n\*. That band is empty if the room absorbs fewer than one reservation (n\* < 1), or if D5 makes unresolved requests recoverable (BE-1 to BE-4). λ is unmeasured, and the room figures (UB-2 and UB-6) are unbound.
- **B's build is the largest discretionary item** (allocation rows C06b, C15b, B16). Deferring it cuts T09 scope without touching any accepted behavior.

**What preserve-and-block still requires for the first release** (these are not optional):

| Item | Why | Owner |
|---|---|---|
| **Reconcile the fence semantics with the spec** (UB-8 Q2). Production counts an accepted entry or add with no accepted terminal after one bar. Spec S1 counts the absence of order-level evidence. Rail S2/RC-9 cancels a resting entry older than one bar unless it is re-issued, while the ORB port cancels only at session end (map C08) | As read, a resting ORB stop entry could block risk-adds on every leg after one bar. ORB's resting-entry lifecycle (GC-4) and this fence must be settled and traced before the ORB freeze | Coordinator (trace); operator if ORB behavior changes |
| **Bound how long a block lasts**, using D4/D5 (A-1) | BE-4: if a prior-session lookup can locate the order, the block lasts until then rather than for the rest of the account | Operator (reads) |
| **An attended recovery procedure for an unresolved request** (halt/resume §3) | The only exit from the block | T13 |
| **H and ε** (UB-8 Q4) | Without them the operator cannot judge whether a block-ends-automation risk is tolerable | Operator |

**If the operator still wants B for the first release, rule these first** (each is added to the incident ADR's open list; none is adopted):
1. **B-B1: continuous or resume-after-flat?** Amend the halt/resume §2 row for narrowed-shape unknowns too, which gives continuous admission and changes a live-risk contract, or accept B as resume-after-flat. Rule 4′'s wording must match the choice.
2. **B-B2: exceptional-mode trigger.** Rule 4′ defines the mode by the account fence, so the Q2 reconciliation decides when the mode begins.
3. **B-B3: Aegis under a held reservation.** Accept or reject that any held reservation may block a full-size Aegis entry, and that a takeover cannot complete while a displaced leg holds a reservation (`book_capacity.py:277-278`).
4. **B-B4: split with an unknown child** (UB-8 Q5). Does it count as "closed" for add eligibility? UB-4's rule implies not, because an unknown child keeps the sequence open.

**Effect on the incident ADR (proposed; not applied here):** record the first-release posture as preserve-and-block under the §A10 acceptance condition. Add B-B1 to B-B4 to §A10's OPEN list. Rule 4′'s "exceptional mode" stays defined by the fence as reconciled under Q2.

---

## 4. Allocation and component reductions (gate D)

**Source:** the [allocation map](2026-09-25-tradeify-capability-allocation-deletion-map.md), as corrected. Recommended boundary: **one durable account owner** plus the barrier, the private ports and the watchdogs, and a thin CrossTrade REST adapter. The vendors own execution only. That is:
- **Tradovate:** matching, the resting stop entry, one-contract OSO creation and first-fill activation, and fixed stop/target execution between bars;
- **CrossTrade:** transport and ids;
- **TradingView:** research and export only, under the standing ruling.

| Disposition | Items | Condition |
|---|---|---|
| **Avoid building** | TradingView webhook ingress and alert manifest (B01); Pine market-input publisher (B02); intrabar trail manager and protection feed (B03); automatic incident dispatch (B04); partial-fill residual cover (B07); **option-B machinery (B16), under the §3 recommendation** | The standing TradingView ruling; the edition freezes; the §3 posture |
| **Reduce after freeze** | ATTACH path (B05); live use of trailing fields, via a live-sender guard (B06) | The Striker, ORB and Vanguard editions freeze and requalify. Code stays in place for replay parity, and the E1 inventory rebinds if code changes |
| **Retain** | Ports, emulator, parity and bundles (B08); feed (B09, funding deferred); runtime and loop (B10); account-owner core (B11); protection amend path (B12, dependent on GC-2b/GC-3); settlement (B19); legacy M1 path, guarded (B17) | — |
| **Introduce (required by the route)** | One-contract split and sequencing (B13); close realization per B-1 (GC-1 C-a); Striker crossed-level exit (B14); REST producer with post-placement poll and same-session recipe (B15); **fence reconciliation (§3)** | T09 scope (§5) |
| **Delete** | **None established.** No removal candidate has met its conditions | — |

**Conditional savings** (the corrected note's rule): vendor protection counts only once the stop is **Working** (GC-2a). Splits and multi-order closes can still complete partly (UB-4; GC-1). Moving work to a vendor adds local reconciliation: the late-reject poll (GC-8) and the coverage-repair actor (A8).

**Freeze impact:** the qualification trust domain binds the account owner, protection owner, capacity, takeover, protocol, feed and the ports. Every T09 change to those modules changes the E1 freeze inventory (allocation map §B).

---

## 5. T09 handoff — HELD until B–D acceptance

**Status: HELD. Not dispatchable.** It becomes dispatchable only when:
- gates B, C (for the bounded design) and D are accepted on the T09 gate table;
- B-1 (the close realization) is ruled;
- the edition rules it depends on are frozen or explicitly held;
- it is re-committed as its own handoff under the committed-handoff rule.

The draft below fixes scope and boundaries only.

**Selected outcome:** a disarmed CrossTrade REST adapter and reconciliation path behind the existing account owner. It realizes the recommended boundary (§4) under **preserve-and-block** (§3), with every route-dependent step held behind its gate-C trace.

| In scope | Interface / evidence | Held behind |
|---|---|---|
| REST producer: `orders/place` (one-contract OSO with a per-attempt `clOrdId`), `change`, `cancel`, `close`; lifecycle, status and fill reads mapped to `BrokerFact` and `ProtectionSnapshot` | Gate A A1, A3 (i)–(iii), A7; REST-form traces only (interface rule) | GC-2a, GC-2b, GC-3 |
| Outcome classifier: local pre-dispatch refusal, remote refusal after dispatch, positive lookup (facts it establishes only) | Gate A A3 | — (design); traces for the evidence |
| Post-placement status poll within the protection deadline | GC-8 | — |
| One-contract split, per-symbol sequencing, whole-intent capacity reservation, abandon-remainder rule | B-6, B-9; UB-4 | Edition freezes |
| Whole-leg close via broker liquidation on the exclusively owned symbol; close completion on postdating coherent evidence | B-1 (C-a); §1.1a interpretation accepted | GC-1 traces, GC-3, GC-7 |
| Striker close-time crossed-level exit as a whole-leg close | B-7 | GC-1; STR-5 |
| Fence reconciliation (§3): resting-entry lifecycle versus the one-bar cut | §3 row 1 | Trace; ORB freeze |
| Live-sender guard refusing trailing fields and ATTACH on edition legs | B06, B05 | Edition freezes |

**Out of scope:** option B (B16); TradingView paths; any deletion; the feed provider (T14); settlement changes (T07); notifications (T13); drills, account access, arming, activation and spend.

**Verification:** fault-injected consumer cases for every GC failure consequence (the route stops or refuses, as §1 states); retained REST-form traces for each delegated capability; `.\fp.ps1 test-ops` and `check` records. No live manufactured lost response or unmanaged exposure (checklist T09).

**Return boundary:** the adapter and reconciliation evidence, disarmed. It must not arm or activate, and it must not change anything outside the scope table.

---

## 6. Decisions required from the operator

Grouped by what each one unblocks. Where a coordinator recommendation exists, it is in the cited section.

**First: these decide whether the route can exit at all.**

| # | Decision | Recommendation | § |
|---|---|---|---|
| 1 | Close realization, and the L2(e) interpretation for whole-scope liquidation | Pursue C-a and accept §1.1a subject to evidence; keep C-b as the fallback | B-1, §1.1 |
| 2 | Authorize a revised operator session plan: REST-form D1–D3 and D6, the REST reads D4/D5, and the new GC-1 race observation | Authorize, bound to exact operations and account scope | A-1 |
| 3 | Complete the account actor inventory (exclusivity) | Inventory, and enable no vendor backstop | B-12, GC-7 |
| 4 | Supply entitlement and venue-permission evidence | Required before any live use | P-1 |

**Second: unknown-request posture.**

| # | Decision | Recommendation | § |
|---|---|---|---|
| 5 | First-release posture | Preserve-and-block; B stays Proposed | §3 |
| 6 | Set H (first-release horizon) and ε (tolerance for a block that ends automation) | Operator's values | §3 |
| 7 | *Only if B is wanted for the first release:* B-B1 to B-B4 | — | §3 |

**Third: edition rules, frozen with the pre-registrations.**

| # | Decision | § |
|---|---|---|
| 8 | ORB-2/3/4 and Vanguard VAN-2/3/4 (fixed stop; the exits that replace the trail; no amend) | B-4, B-5 |
| 9 | Striker initial stop, STR-2 (option (a), a qualified behavior change) | B-3 |
| 10 | Split size and partial acknowledgement: STR-3/4, VAN-5/6, and the VAN-6 counter wording | B-6 |
| 11 | Exit-split rows follow the close choice (ORB-6, STR-7, VAN-8) | B-2 |
| 12 | Striker crossed-level exit, STR-5 (whole-leg as declared; partial-lot case) | B-7 |
| 13 | Split sequencing and replay pricing | B-9 |

**Only if a capability fails:** a fixed-stop Striker or Aegis (GC-2b/GC-3); an Aegis takeover change (GC-5); an ORB resting-entry end-of-life change (GC-4 and the §3 fence item).

**Not requested here:** freeze, T09 dispatch, drills beyond decision 2, deployment, arming or spend. **S5** is decided separately through its own decision draft and remains held.
