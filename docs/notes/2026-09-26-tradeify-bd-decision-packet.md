# Tradeify route: integrated B–D decision packet

**Status:** DRAFT, in progress (2026-09-26). Coordinator-authored. It accepts no gate, changes no contract or behavior, and grants no drill, access, spend or GO. Gates B–D stay pending until the operator rules and the coordinator records integrated acceptance on the [T09 gate table](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t09-gate-acceptance-record).
**Inputs:** Gate A ([REST §6.11](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#611-gate-a-factual-disposition)); the [allocation map](2026-09-25-tradeify-capability-allocation-deletion-map.md) (read its coordinator-corrected section first); incident ADR [§A9–§A10](../adr/2026-09-17-bounded-platform-protection-incident-contract.md); the rail spec's [R-B3 / L-2](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md); campaign §59 Rulings 3–4; the three edition pre-registrations. Parallel drafts: [dispatch card](../briefs/handoffs/2026-09-26-bd-packet-parallel-drafts.md) (UB-8 comparison; S5 decision draft).
**Route assumed:** the ruled Python signal host → our account owner → CrossTrade-mediated Tradovate REST. TradingView's exclusion is the standing 2026-09-11 ruling. Account entitlement and venue permission remain evidence owed (§4, P-1).

| § | Content | State |
|---|---|---|
| 1 | Gate C: decisive capabilities, validation and failure consequences | Drafted below |
| 2 | Gate B: remaining behavior decisions | Pending |
| 3 | Revised option-B rules, with unresolved assumptions | Pending (UB-8 return) |
| 4 | Allocation and component reductions (gate D) | Pending |
| 5 | T09 handoff (held until B–D acceptance) | Pending |
| 6 | Decisions required from the operator | Pending |

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
