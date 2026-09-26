# Tradeify route: integrated B–D decision packet

**Status:** DRAFT for operator review (2026-09-26). Coordinator-authored. It accepts no gate, changes no contract or behavior, and grants no drill, access, spend or GO. Gates B–D stay pending until the operator rules and the coordinator records integrated acceptance on the [T09 gate table](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t09-gate-acceptance-record).
**Inputs:** Gate A ([REST §6.11](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#611-gate-a-factual-disposition)); the [allocation map](2026-09-25-tradeify-capability-allocation-deletion-map.md) (read its coordinator-corrected section first); incident ADR [§A9–§A10](../adr/2026-09-17-bounded-platform-protection-incident-contract.md); the rail spec's [R-B3 / L-2, `CLOSE(scope)`, S2, S5](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md); the [halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md); campaign §59 Rulings 3–4; the three edition pre-registrations. Parallel drafts: [dispatch card](../briefs/handoffs/2026-09-26-bd-packet-parallel-drafts.md) (UB-8 comparison; S5 decision draft, [PR #517](https://github.com/Joshua-Asante/first-passage/pull/517)); the route drill-plan draft, [`docs/notes/2026-09-26-tradeify-route-drill-plan-draft.md`](2026-09-26-tradeify-route-drill-plan-draft.md) (written in parallel).
**Route assumed:** the ruled Python signal host → our account owner → CrossTrade-mediated Tradovate REST. TradingView's exclusion is the standing 2026-09-11 ruling. Account entitlement and venue permission remain evidence owed (§2 A-1, P-1).

**Revision 2026-09-26 (executive review).** The executive review of 2026-09-26 recommended the changes below. They revise draft recommendations in place. None is an operator ruling: every direction is **recommended (executive review 2026-09-26); operator ruling pending**. No gate is accepted, the qualification S5 freeze (execution-slices plan; PR #517) is not released and no drill is authorized. "Rail S5" below means the rail spec's S5 (scoped exit/flat), a different item.
- **§1.1 (GC-1 / D19):** C-a is only the **first candidate to investigate**; no close guarantee is accepted. The earlier §1.1a L2(e) interpretation is **withdrawn** and replaced by a **proposed explicit amendment** to the rail close contract, with five required elements and every unknown marked OPEN. An evidence standard is added. C-b is an **unapproved alternative**, not a fallback. GC-7 exclusivity now accommodates the attended operator-intervention procedure.
- **§1.2:** failures that previously named a fixed-stop or other edition now **return to the operator with alternatives**. GC-3 records that ORB and Vanguard noop amends also need its postdating read. The operator performs every order-producing trace; the coordinator designs and records. GC-6 and GC-8 are labelled NO ROUTE STOP.
- **§2:** B-1 to B-12 revised; B-13 added (ORB resting-entry lifecycle). A-1 no longer asks approval of a race check. It asks for two REST reads, the actor inventory and permission evidence, and the concrete order-producing drill plan **before** any execution is authorized.
- **§3:** preserve-and-block recommended with suggested ruling text; one attended session, then review; the operator records acceptance of a concrete consequence instead of setting ε; "band" and break-even wording qualified; the resting-order fence is a **required correctness repair** with a four-state trace, and the spec's own reading of a resting order still working after one bar is OPEN; the ORB lifecycle conflict is resolved separately.
- **§4:** consistency only (B16 deferred with B; close and fence rows restated; B07 conditioned on the close amendment; vendor savings conditions).
- **§5:** close and fence rows updated; HELD kept.
- **§6:** restated as recommended directions pending ruling. **The immediate route blocker is safe closing.** Pointer to the qualification S5 freeze decision (PR #517) added.

| § | Content | State |
|---|---|---|
| 1 | Gate C: decisive capabilities, validation and failure consequences | Drafted; revised 2026-09-26 |
| 2 | Gate B: remaining behavior decisions | Drafted; revised 2026-09-26 |
| 3 | Unknown-request posture and option-B rules, with unresolved assumptions | Drafted; revised 2026-09-26 |
| 4 | Allocation and component reductions (gate D) | Drafted; consistency edits 2026-09-26 |
| 5 | T09 handoff (held until B–D acceptance) | Drafted; revised 2026-09-26 |
| 6 | Decisions required from the operator | Drafted; revised 2026-09-26 |

---

## 1. Gate C — decisive capabilities

**Rule applied.** The rail spec's L-2 applies: "every item a port uses must be `supported` … missing evidence or an unsupported item makes the live packet `BLOCKED — capability-problem`". A cancel/replace cannot satisfy L2(c), and a concurrent cancel plus close cannot satisfy L2(d). Every row below that can block states its failure consequence as one of two classes:
- **ROUTE STOPS:** the live packet is BLOCKED for the affected legs until a contract change is accepted.
- **OPERATOR DECISION:** the affected legs are BLOCKED on this route, and the question returns to the operator with stated alternatives (for example an edition change with pre-registration and requalification, a contract change, or excluding the leg). **No alternative is adopted automatically.**

Rows whose failure costs availability or design work only (GC-6, GC-8) are marked **NO ROUTE STOP**.

**Evidence labels** follow the allocation map: `DOCUMENTED`, `OBSERVED FOR EXACT SCOPE`, `CONTRADICTED`, `UNVERIFIED`. No row is observed yet. The drill references use the Gate A drill map, which is keyed by behavior. D-numbers in this packet are the REST return's (§6.9); the 2026-09-25 session plan numbers the same order-producing rows D1–D4, and the drill-plan draft names them R-1 and R-2 (reads) and X-1 to X-5 (order-producing). Authorization binds to the row, not to a label.

**Interface rule.** A trace counts only for the interface it exercised. Webhook-form evidence may be reused for REST only for a **demonstrated common downstream property** (for example, the same Tradovate call with the same observations, once that equivalence is accepted). REST request classification, correlation and observation still need REST-form evidence.

**Evidence standard.** For each capability, establish the mechanism from **authoritative vendor semantics first**, then validate it with traces and fault cases. A trace validates a mechanism; it does not establish one. A single successful observation shows that one attempt did not fail; it cannot show that a race or reversal cannot occur. If the guarantee remains unavailable, the output is a **precise residual-risk statement** returned to the operator for decision. Every order-producing trace is performed by the operator (Joshua) only.

### 1.1 GC-1 (D19): close and protection cleanup — first-order blocker

**Why it blocks.** Every inspected port exit is a whole-leg flat (allocation map C11). Striker also needs the close-time crossed-level exit, which is a triggered-protection close (C11b; rail S3(d)). The contract's `CLOSE` needs **L2(d)**: an atomic scoped close with attached-order removal, including a quantity-less close on an exclusively owned symbol. It also needs **L2(e)**: atomic protection adjustment to the residual on every partial fill, with no reverse exposure. L2(e) is contradicted on this route (Gate A A5), and partial or scoped close leaves working orders behind (A5). One-contract **entries** do not settle close semantics:
- a close of N lots can finish partly;
- a protective fill can race the close;
- a close sent after a protective fill can reverse the position.

UB-8 cannot make an unqualified close route viable. **The immediate route blocker is safe closing.**

**Candidate realizations.** None is qualified and no close guarantee is accepted. The operator chooses what to investigate.

| Option | Mechanism | L2 fit | Main risk | Evidence needed | Assessment |
|---|---|---|---|---|---|
| **C-a. Broker liquidate for whole-leg exits** | CrossTrade `close` → Tradovate `liquidateposition` on the exclusively owned symbol. It is quantity-less. The route documents that it cancels the OCO children and closes the position, but that is **not verified** (K; REST §6.6 partial-fill row; A4) | L2(d) as written **only if** authoritative vendor semantics establish that the cancel and the flatten are **atomic**, with no interval between them (`CLOSE(scope)`: two requests in one software step are not atomic at the broker). No residual working order afterwards is necessary but not sufficient. Otherwise L2(d), like L2(e), rail S5 and I7, falls under the **proposed explicit amendment** below (§1.1a (a), (c)). L2(e), rail S5 and I7 as written would **not** be met if the brackets are cancelled before the position is flat (the ordering is OPEN) | A protective stop may fill while the liquidation is in flight, so a flatten on stale quantity could reverse the position (`UNVERIFIED`). Full `close` is `liquidateposition`, a request rather than a guarantee (REST §6.4; Gate A A4 records L2(d) as K). Rejection, partial completion and unknown outcomes are unread | (1) Authoritative vendor semantics for §1.1a (a)–(c); (2) REST-form traces of the normal case (D3) and of fault cases (rejection, partial, unknown outcome, a protective fill racing the liquidation), under an approved drill plan; (3) the R5 exclusivity inventory (GC-7; D-B9 needs an exclusively owned symbol) | **First candidate to investigate** (recommended direction; operator ruling pending). It matches every whole-leg exit. It is usable only if the §1.1a amendment is accepted and its OPEN items are settled, or their residual risk is accepted by the operator |
| C-b. Exit through the lot's own OCO | Amend each lot's target to a marketable level so that the broker-native OCO fills and cancels its sibling stop | L2(d) per lot by the broker's own OCO. L2(e) is moot at one contract | Needs L2(c) (K; D2) for every lot. A modify through the market may be refused or behave differently. A leg without a target has no carrier. A whole-leg exit becomes N per-lot modifies that can complete partly (UB-5). It changes the exit order type and price path, which is a behavior change | D2 plus a marketable-limit amend trace, after vendor semantics | **Unapproved alternative.** It is not an automatic fallback: it needs its own operator expression decision, then pre-registration and requalification |
| C-c. Market exit per lot, then cancel its bracket | Two requests | **Fails** L2(d) as written ("concurrent cancel/close cannot satisfy (d)") | Orphan protection, and a reverse position if the stop fills between the two requests | — | **Not recommended.** It needs a contract change that accepts the known race |

**§1.1a — proposed explicit amendment to the close contract (for gate B; not adopted).**

*Withdrawn 2026-09-26 (executive review):* the earlier draft proposed an **interpretation** of L2(e) for whole-scope liquidation: that the broker's own flatten order satisfies L2(e) by owning the residual, and that no residual protection is required once the intent is to be flat. That interpretation is withdrawn. It is replaced by the outline below.

**What would be amended.** The rail spec's close contract: R-B3 L-2 items (d) and (e); the §1 `CLOSE(scope)` primitive (including "Rejection retains the existing protection"); rail S5, scoped exit/flat ("protection remains effective for any unclosed remainder … removed only when that scope is flat"); and I7 ("`CLOSE` reduces position and protection together"), which a cancel-first liquidation would not meet as written. Owner text is written into the rail spec only after an operator ruling. **Scope:** whole-leg or full-symbol closes on an exclusively owned symbol (D-B9). Subset or scoped closes stay U and are outside it.

The amendment must specify each element below. Nothing here states vendor behavior that the route documents do not; every unknown is **OPEN**.

| # | The amendment must specify | Known today | OPEN |
|---|---|---|---|
| (a) | **Protection during the liquidation interval.** What protects the position between cancellation of its protective orders and confirmed flatness, or an explicit statement that nothing does; a bound on that interval; and the consequence when the bound is exceeded | The route documents that liquidate cancels the OCO children and closes the position (unverified) | Whether cancellation precedes the flatten; the flatten's order type; the interval's length; whether any protection survives it |
| (b) | **Failed, rejected or partially completed liquidation.** For each outcome: what the rail owns, which block it sets, and what the operator sees. It must replace `CLOSE`'s premise that rejection retains the existing protection wherever that premise cannot hold, for example a rejection or failure after the brackets were cancelled, which leaves an unprotected position (a protection fault under halt/resume §2) | `CLOSE` defines `close_rejected`, remainder-only resumption and reconciliation before any resubmission; late rejects need polling (A7; GC-8) | Whether liquidation is all-or-nothing; whether cancels are rolled back on failure; how failure is reported (synchronously or later); whether a partial flatten can occur |
| (c) | **Protective-fill races and reverse exposure.** Reverse exposure stays forbidden (`CLOSE`: "cannot over-execute into a reverse position"; R-C). The amendment names the mechanism that prevents reversal. If that mechanism cannot be established from vendor semantics, it states the residual precisely (the conditions under which reversal can occur, and its detection and attended handling) for operator decision | Nothing; the race is `UNVERIFIED` | Whether the broker computes the flatten quantity from the live position at execution or fixes it at request time; whether a protective fill can land between the cancel and the flatten; whether both can execute. If liquidation is internally a cancel followed by a market order, the C-c race exists inside C-a, and the amendment must say so rather than rely on it being one request |
| (d) | **Observations that establish completion.** Only broker-sourced evidence that **postdates** `prepared_at` (rail evidence-currency rule) and is **coherent** for the symbol (E1): zero net position and no gross open lot (K1), no working order on the symbol, including the former bracket children and any flatten remainder, and the liquidation request's own terminal status. HTTP acceptance, cached flatness and position-only reads never complete it | Per-order lifecycle reads `DOCUMENTED`; account-wide causal order `UNVERIFIED` (CAP R4) | Which REST reads carry broker timestamps or versions that postdate preparation, and whether several reads can be shown to describe one state (GC-3) |
| (e) | **Incident handling while completion is uncertain.** When "not yet confirmed" becomes "uncertain"; that rev9 governs from then on (halt/resume §2 row 1, "uncertain transport/order outcome": halt into INTERVENTION, no runtime resend or second close, attended recovery under §3); that the unresolved close keeps its blocks; and that no acknowledgment, reset or elapsed time completes it. The blocks have different sources: `unknown_order` for an unresolved close is required by the rail spec's `CLOSE(scope)`, but today's production fence does not produce it, because it scans entries and adds only (`book_account_owner.py:787-789`); `close_unreconciled` is the code's risk-add refusal while any exit or flat is non-terminal (`:1610-1612`). The §3 fence trace therefore includes close operations. `CLOSE(scope)`'s own reconcile-then-resubmit text must be reconciled with rev9 for this case | Rev9 §2–§3 and the own-flat deadline rule (§5) | The deadline after which an unconfirmed liquidation is uncertain; how a scheduled-flatten liquidation that turns uncertain interacts with the §5 own-flat deadline |

**Striker's crossed-level exit (S3(d)).** Decide STR-5 only after a source check establishes whether the crossed-level condition can apply to a **subset** of lots. A subset exit is never silently widened into a whole-leg liquidation.
- If the condition cannot apply to a subset (every lot is crossed together), the amendment must also state whether one whole-leg liquidation may realize the S3(d) `triggered_protection` transition for every protection owner. `CLOSE(scope)` forbids substituting one transition kind for another. **OPEN.**
- If it can apply to a subset, the subset case is a scoped close (U on this route) and returns to the operator with alternatives (STR-5, gate B).

**Failure consequence.**
- **C-a's mechanism cannot be established from vendor semantics:** **ROUTE STOPS for all four legs until the operator decides.** There is no admissible exit meanwhile, and C-c is excluded. The output is a precise residual-risk statement to the operator, who may choose among: accepting the stated residual risk under the §1.1a amendment; C-b as a separately decided expression change; a different close contract; or rejecting the route. None is automatic.
- **C-a's traces show residual orders or an actual reversal:** **ROUTE STOPS for all four legs** on C-a. The trace contradicts the mechanism, so it reopens any earlier residual-risk acceptance, and the question returns to the operator with the trace. None of the choices above is automatic.
- **The subset crossed-level case is unsupported:** **OPERATOR DECISION** for Striker (STR-5).

### 1.2 Other decisive capabilities

| ID | Capability (rail item) | Legs | Current evidence | Validation method · owner | Pass criterion | If it fails |
|---|---|---|---|---|---|---|
| GC-2a | Stop activation on the entry's first fill at quantity 1 (§A1; L2(b)) | All | Creation `DOCUMENTED`; activation at qty 1 `UNVERIFIED`. Creation is not protection in force | D1 (REST form) · operator performs, coordinator records | The child stop is `Working` at qty 1 after the fill, linked to the entry; activation interval measured | **ROUTE STOPS for all legs.** The one-contract premise fails, and no entry is protected from fill |
| GC-2b | Rejected modify keeps the old stop (L2(c)) | Striker (per-bar ratchet), Aegis (breakeven/re-pin); C-b if pursued | `UNVERIFIED` (K) | Vendor semantics, then D2 (REST `change`, command report) · coordinator (vendor semantics); operator performs the trace, coordinator records | The old stop stays `Working` at its old price after the rejection; an unknown modify is reconciled before any retry | **OPERATOR DECISION** for Striker and Aegis, with alternatives, e.g. a fixed-stop edition (a strategy change needing pre-registration and requalification), a different amend realization under a contract change, or excluding the leg. A cancel/replace cannot satisfy L2(c). ORB and Vanguard are unaffected only if their successor settings make every amend a noop (B-4, B-5) |
| GC-3 | Evidence freshness and coherence for amend, noop and close completion (rail evidence-currency rule; C18) | Striker, Aegis (amend); ORB and Vanguard (noop determination); all (close completion) | Per-order lifecycle reads `DOCUMENTED`; account-wide causal order `UNVERIFIED` (CAP R4). A poller sequence orders **our** observations only. Every re-issued bracket, including one that resolves to noop, is prepared with a protection deadline and needs a protection read that postdates preparation before the noop is decided (`book_protection_owner.py:554-563`, `:583-586`, `:602-605`); a missing read reaches the protection-deadline fault (`:177-182`) | Design, then trace: show that post-preparation lifecycle and status reads carry broker timestamps or versions that postdate `prepared_at`, and that the reads used for one decision describe one coherent state (for example a re-read bracket, or version equality) · coordinator (design), operator (trace) | Each completion or no-op determination rests on broker-sourced evidence proven to postdate preparation and to be coherent for the targeted scope | Amend: **OPERATOR DECISION** (as GC-2b). ORB/Vanguard per-bar noop path: **OPERATOR DECISION**, with alternatives, e.g. a contract change on when an unchanged re-issue needs a postdating read, an edition change that stops the per-bar re-issue (pre-registration and replay), or excluding the leg. Close completion: **ROUTE STOPS**, because a close could never be completed |
| GC-4 | Cancel of a resting stop entry ends its Suspended children | ORB | `UNVERIFIED` (drill-map row 4; session plan D4 / REST return D6) | Trace · operator | Parent and both children terminal; no fill | **OPERATOR DECISION** for ORB, with alternatives, e.g. an attended session-end procedure, a different end-of-life rule (an edition change entering the ORB pre-registration and replay; see B-13), or a cleanup read that closes the orphans before the next session. Not route-wide |
| GC-5 | Takeover composite (cancel plus close for the displaced leg, then admission) | Aegis | `UNVERIFIED` (K) | Documentary sequence under the accepted close realization (none yet), then a trace · coordinator (documentary sequence); operator performs the trace, coordinator records | The displaced leg is flat with no residual orders before the Aegis entry is admitted | **OPERATOR DECISION** for the takeover rule, with alternatives, e.g. no takeover (the Aegis intent queues or is skipped) |
| GC-6 | REST reconciliation: same-session recipe (D4) and prior-session lookup (D5) | All | Same-session `DOCUMENTED`; cross-session `UNVERIFIED` | Operator-performed reads, **not yet authorized** (D12); recommended for authorization under A-1 | D4 locates by `clOrdId` and recovers children and fills; D5 shows whether a prior-session order is readable by id | **NO ROUTE STOP** under preserve-and-block. Unknowns stay blocking, and their cost is availability (UB-8). Cross-session recovery is **UNKNOWN** until D5, not an observed zero rate. Under B, it limits what UB-7 can resolve |
| GC-7 | Account actor inventory and exclusivity (CAP R5; D-B9) | All | `UNVERIFIED` (A10) | Operator inventory of copier, Account Manager, other platforms and manual sessions · operator | No actor other than this runtime places, modifies or closes on the four symbols **except under the approved attended operator-intervention procedure** (halt/resume §1, §3). During intervention the runtime is fenced (INTERVENTION: no runtime broker mutation); afterwards, recovery requires fresh coherent evidence covering the operator's actions (§3 ¶2), and resumption requires a fresh operator resume (§4). Every other actor is documented and disabled. Other operator-placed trades, such as the weekly account-preservation trade, need the same treatment (automation fenced, reconciliation afterwards) or a symbol outside the four: **OPEN** (operator). Still owed by route qualification (halt/resume §1, last paragraph): the inventory of provider-side actors, the supported intervention/quiescence procedure and residual request accounting (**OPEN**). This exception does not assert that manual action is race-free | **ROUTE STOPS** while C-a is the close candidate, because D-B9's quantity-less close needs exclusive ownership. Otherwise the result is a named actor to disable |
| GC-8 | Late-reject detection by polling (A7) | All | `DOCUMENTED` (no Alert History) | T09 design, then trace · coordinator (design); operator performs the trace, coordinator records | A rejected child or bracket is detected within the protection deadline | **NO ROUTE STOP**; design work. The protection deadline (`PROTECTION_PERIOD`, `book_protection_owner.py:24`, enforced at `:177-182`) bounds it; a missed deadline is a protection fault, which halts under halt/resume §2 |

**Priority order.** GC-1 first (it decides whether any safe exit exists), then GC-2a, GC-7, GC-3, GC-2b, GC-4 and GC-5, with GC-6 and GC-8 in parallel. Vendor-semantics work for GC-1 needs no drill and can start now. The drill-map rows D1–D3 and D6 (REST-return labels; session plan D1–D4) are authorized in principle (2026-09-25) in **webhook form only**. Whether that in-principle authorization permits execution before the concrete drill plan is reviewed is **OPEN** for the operator (drill-plan draft, open question 2); this packet does not treat it as execution authority. REST-form traces for GC-1, GC-2a, GC-2b, GC-3 and GC-4 (drill-plan X-1 to X-5) are order-producing: A-1 requests their concrete drill plan, and this packet asks no approval to execute any of them, including any GC-1 fault or race case. The D4/D5 reads (drill-plan R-1, R-2) are requested separately under A-1.

---

## 2. Gate B — remaining behavior decisions

Each row is the operator's to rule, in words and without parameter values, in its owner. "Recommendation" is the coordinator's, revised under the executive review of 2026-09-26: each is a **recommended direction, operator ruling pending**. The source-grounded suggestions come from the allocation map §D; private reads were in place only. Nothing is adopted here.

| ID | Decision (owner) | Recommendation | Depends on | Blocks |
|---|---|---|---|---|
| B-1 | **Close realization (D19).** Which GC-1 candidate to investigate first, and whether to commission the §1.1a amendment to the rail close contract (rail spec R-B3, `CLOSE(scope)`, S5, I7; incident ADR UB-5) | Investigate **C-a** first; no close guarantee is accepted. Commission the §1.1a amendment with elements (a)–(e); its OPEN items are settled by vendor semantics, then traces. If the guarantee stays unavailable, a residual-risk statement returns to the operator. C-b is an **unapproved alternative** needing its own expression decision, not a fallback. Reject C-c | Vendor semantics; GC-1 traces; GC-3; GC-7 | Every exit; T09 |
| B-2 | **Exit-split rows** ORB-6, STR-7, VAN-8 (pre-registrations) | Rewrite them to follow B-1 once a close realization is accepted (none is yet). If the C-a amendment is accepted, a whole-leg exit would be **one broker liquidation**, not N one-contract closes. The "must become one-contract closes" premise is withdrawn with UB-5 (Proposed). Subset exits are not covered (B-7) | B-1 | Edition freeze |
| B-3 | **Striker initial stop, STR-2** (D04) | Pursue option (a), the level the port computes on the signal bar, as a **pre-registered behavior change**. The source shows the level is computable at entry. The first attached level can differ from the declared one-bar-later stop, so STR-2 enters the pre-registration and replay, and E1 measures its effect | — | Striker freeze |
| B-4 | **ORB fixed-stop rules**, ORB-2/3/4 | ORB-2: the **existing** fixed-stop component, unchanged. ORB-3: only **existing** exits (fixed stop, target, max hold when enabled, EOD flat) close what the trail used to close; **no invented replacement exit**; a case no existing exit covers returns to the operator (prereg §7). The pre-registration accounts for the changed holding periods, overlap and capacity. ORB-4: "none", **subject to verification** that the successor settings make every per-bar re-issue a noop (trail and breakeven off in the resolved effective behavior; Gate A A6 criterion). The noop itself still needs GC-3's postdating read | GC-3 (noop read) | ORB freeze |
| B-5 | **Vanguard fixed-stop rules**, VAN-2/3/4 | As B-4, per the pre-registration §3a findings: the existing fixed stop and the existing remaining exits (target, stale exit after max hold, EOD flat); no invented replacement exit. VAN-4 "none" is **subject to the mandatory successor-binding check** (Gate A A6) showing trailing, breakeven and grace resolve off, so every amend is a noop. VAN-3 needs the full account of remaining exits that §59 Ruling 4 requires | GC-3 (noop read); A6 check | Vanguard freeze |
| B-6 | **Split size and partial acknowledgement**: STR-3/4, VAN-5/6 | Adopt the UB-4 first-release rule: **whole-intent capacity reservation**; **sequential submission**, each child after a defined acknowledgment; on a refusal, unknown outcome, cutoff, takeover or flatten, **abandon the unsent remainder**; **never retry or top up** an unknown child or a short fill; a base supports adds only after its sequence closes and the approved rule holds. Abandonment is a behavior change: it enters the pre-registrations and replay, and qualification covers the resulting execution and pricing rules. The VAN-6 counter wording states whether the add counter advances at proposal (as declared) | — | Freezes; replay |
| B-7 | **Striker close-time crossed-level exit**, STR-5 (D07) | Decide **only after** the source check establishes whether the condition can apply to a subset of lots. If it cannot, realize it as declared through the accepted close realization, subject to the §1.1a OPEN item on the `triggered_protection` transition. If it can, the subset case is a scoped close (U) and returns to the operator with alternatives. A subset exit is **never** turned into a whole-leg liquidation | Source check; B-1 | Striker freeze |
| B-8 | **Striker per-bar stop modify**, STR-6, and Aegis breakeven/re-pin | Keep them as declared, dependent on GC-2b and GC-3. If either fails, the leg **returns to the operator with alternatives**, e.g. a fixed-stop edition (with pre-registration and requalification), a contract change, or excluding the leg. No fixed-stop edition is created automatically | GC-2b, GC-3 | Striker and Aegis |
| B-9 | **Split sequencing and replay pricing** (D10; §A8 rule 10; each pre-registration's §6) | Sequential one-contract entry requests, with a stated per-request delay and price rule in the replay. Qualification covers the resulting execution and pricing rules. Exits follow B-1 | B-1 | Freezes; E1 |
| B-10 | **Option B for the first release** (D11; incident ADR UB-8 and §A10 acceptance condition) | Preserve-and-block for the first release; **defer B's implementation**; B stays Proposed (§3, with suggested ruling text). Deferral is consistent with the ruled UB-8 row (incident ADR §A9.1): B remains the development direction and stays Proposed under §A10's acceptance condition; deferral concerns first-release implementation only | UB-8 (accepted as input) | §3 rules; T09 scope |
| B-11 | **Takeover under the route** (GC-5) | Keep as declared, realized through the accepted close realization (none yet) for the displaced leg, followed by admission. If GC-5 fails, it returns to the operator with alternatives (e.g. no takeover) | B-1; GC-5 | Aegis |
| B-12 | **Account actors and backstop** (D13; GC-7) | Inventory first. Exclusivity accommodates the approved attended intervention procedure (GC-7). No vendor scheduled flatten as a backstop until qualified, since it would be a second close owner | — | C-a; UB-7 |
| B-13 | **ORB resting-entry end of life** (D18; GC-4) | Resolve the conflict between the rail's one-bar cancel (S2: a resting entry older than one bar is cancelled unless re-issued, citing replay RC-9) and the ORB port's session-end cancel (allocation map C08). Establish from source which lifecycle the qualified strategy and replay implement (I8), then rule it in the ORB edition. **Not chosen to make the fence stop blocking**; the fence is repaired separately (§3). Any change to ORB's intended lifecycle enters the ORB edition pre-registration and replay | Source check (in place, §60); GC-4; §3 fence trace | ORB freeze |

**Authorizations and evidence requested (operator authority, not behavior):**
- **A-1. Reads, evidence and a drill plan.** Recommended (executive review 2026-09-26; operator ruling pending):
  1. **Authorize two narrowly scoped REST reads**, performed by the operator: same-session reconciliation of a **known** order (drill-map row "same-session REST reconciliation recipe on a known order", REST-return D4, drill-plan R-1) and prior-session lifecycle lookup of a **known** order (row "prior-session lifecycle read by id", REST-return D5, drill-plan R-2). Each is bound to its exact read operations and the account scope, as the [drill-plan draft](2026-09-26-tradeify-route-drill-plan-draft.md) names them; authorization binds to those operations, not to a label. Reads only: no order is placed, amended or cancelled.
  2. **Complete the actor inventory** (GC-7) and **supply the entitlement and venue-permission evidence** (P-1).
  3. **Request the concrete order-producing drill plan before any execution is authorized:** environment, exact actions, exposure limits, and abort and recovery. The draft is [`docs/notes/2026-09-26-tradeify-route-drill-plan-draft.md`](2026-09-26-tradeify-route-drill-plan-draft.md). It is to cover REST-form D1–D3 and D6 (REST-return labels; drill-plan X-1 to X-4) and the GC-1 mechanism step and fault cases (drill-plan M and X-5). This packet requests the plan only. It asks no approval to execute any drill, including any race case, and every drill is performed by the operator. Webhook-form evidence may be reused only for a demonstrated common downstream property (§1 interface rule).
- **P-1.** Evidence of account entitlement (CrossTrade Pro REST) and of venue permission for CrossTrade-mediated automated orders on this eval. A firm-level "automation-friendly" classification is insufficient.

---

## 3. Unknown-request posture and option-B rules

**Input:** the [UB-8 comparison](2026-09-26-ub8-availability-comparison.md) (accepted as input; its coordinator review records the source checks on Q1–Q3).

**Recommended direction (executive review 2026-09-26; operator ruling pending): preserve-and-block for the first release** (the current rule, `book_account_owner.py:1608`). **Defer B's implementation. B stays Proposed**, which §A10's acceptance condition already provides for. This is consistent with the ruled UB-8 row (incident ADR §A9.1): B remains the development direction; the deferral concerns first-release implementation only. Suggested ruling text:

> "The first release uses preserve-and-block. An unresolved request stops further automated risk-adds until admissible evidence resolves it. No acknowledgment, reset or elapsed time clears the obligation. Reconsider B after actual reconciliation and operating evidence."

**Horizon.** Recommended: **one attended session, followed by explicit review before extending.** No probability tolerance (ε) is requested. Instead, the operator records whether they accept the concrete consequence that **one unresolved request may suspend automation on this account indefinitely**. Automated trading as a whole stays halted, not only risk-adds: an uncertain outcome halts the account into INTERVENTION (halt/resume §2 row 1), recovery cannot complete and resume is refused while a request is unresolved (halt/resume §3–§4). The owner code's risk-add fence (`book_account_owner.py:1608`) is the part implemented today (UB-8 Corr. 5).

**This is a scope decision under uncertainty.** UB-8 did not show that B is unnecessary, or that unresolved responses are rare. Reasons for the direction:
- **B's continuity, as the texts stand, is limited.** An unknown still triggers the halt/resume §2 halt and the §3 return to flat, so B buys *resume after an attended return to flat*, not uninterrupted trading (UB-8 Q1; BE-5).
- **B's value cannot be sized today.** λ is unmeasured, the room figures (UB-2 and UB-6) are unbound, and cross-session recovery is **UNKNOWN** until D5 (the comparison's ρₓ = 0 is a placeholder, not an observed rate). UB-8's break-even conditions (BE-1 to BE-6) illustrate the trade-off under a simple arrival model. They are not logically necessary conditions. B can have value outside the ε < λH < n\* band: it can postpone exhaustion, or shorten a block that would later prove recoverable.
- **B's build is the largest discretionary item** (allocation rows C06b, C15b, B16). Deferring it cuts T09 scope without touching any accepted behavior.

**What preserve-and-block still requires for the first release** (these are not optional):

| Item | Why | Owner |
|---|---|---|
| **Resting-order fence: required correctness repair** (not a policy choice; UB-8 Q2). The production fence counts an accepted entry or add as unresolved once one bar passes without an accepted terminal (`book_account_owner.py:787-797`). The rail spec's S1 cut keys on the **absence of order-level evidence** within a bar, but its `pending` row reaches `UNKNOWN` "after the one-bar outcome timeout", and S2 cancels a resting entry older than one bar unless re-issued. How the spec classifies a resting order still working after one bar is **OPEN** (state (i) below), so the spec side of the divergence is not established. Repair through a source-to-consumer trace of the four states in the table below that settles the spec reading (with a spec clarification if needed) as well as the code classification | As read, a known resting ORB stop entry with fresh evidence would refuse risk-adds on every leg after one bar. Consumers to trace: admission (`:1608`), close operations (§1.1a (e): the fence scans entries and adds only) and every other consumer the trace finds (capacity release, takeover; rule 4′ if B is later accepted). **Must be resolved before the ORB freeze** | Coordinator (trace; T09 repair) |
| **ORB resting-entry lifecycle** (B-13), resolved separately: the rail's one-bar cancel (S2; RC-9) versus the port's session-end cancel (C08) | Neither behavior may be chosen merely to make the fence stop blocking. Any change to ORB's intended lifecycle enters the ORB edition pre-registration and replay. Before the ORB freeze | Operator (ruling); coordinator (source trace) |
| **Establish whether and when a block can end**, using D4/D5 (A-1) | BE-4: if a prior-session lookup can locate the order, the block for that order can end then rather than lasting for the rest of the account. A located order settles facts about that order only (Gate A A1): one D5 success shows neither coverage of every kind of unknown nor a time bound. Until D5, cross-session recovery is UNKNOWN | Operator (reads) |
| **An attended recovery procedure for an unresolved request** (halt/resume §3) | The only exit from the block | T13 |
| **Horizon and consequence acceptance** (replaces "H and ε", UB-8 Q4) | One attended session, then review; the operator records whether they accept that one unresolved request may suspend automation on this account indefinitely | Operator |

**Four-state trace for the fence repair** (spec and code columns are *as read*, not traced; the trace confirms or corrects them):

| State | Defined by | Production fence today (`:768-798`) | Rail spec | The trace must show |
|---|---|---|---|---|
| (i) Known working order, fresh evidence | Accepted request with order-level evidence of `Working` within the freshness window | Unresolved once one bar passes with no accepted terminal (`:793-797`), so `unknown_order` refuses every risk-add | **OPEN; the texts pull both ways.** §1 `pending` row: `UNKNOWN` "after the one-bar outcome timeout or a crash between send and outcome", resolved only by a terminal event or a postdating `W` absence plus consistent `P`; a `W` showing the order working is not listed. S1 cut: "no evidence within one bar → `pending=UNKNOWN`" (AC-5: an entry sent and `accepted` with no evidence for one bar becomes `UNKNOWN` and HALTED). S2 holds the reservation while the entry rests, but cancels a resting entry older than one bar unless re-issued (RC-9). E3: completion hands ownership to observed working orders. A literal reading may agree with the production fence | First the spec reading, with a spec clarification if needed. Then which producer supplies and refreshes the evidence, and the repaired classification for each consumer |
| (ii) Evidence gone stale | A previously evidenced order with no fresh order-level evidence | As (i): the fence has no evidence-age input | `W` older than one bar degrades to `UNKNOWN` (§1 `W` row); risk-add admission refuses (consistency matrix; I1) | That staleness, not order age, blocks, and which fresh evidence clears it |
| (iii) Genuinely unknown dispatch outcome | Attempt `UNKNOWN`: transport exception, no response, or a crash between send and outcome | Unresolved at once: the one-bar grace applies only to non-`UNKNOWN` outcomes (`:793`) | §1 `pending` row: `UNKNOWN` "after the one-bar outcome timeout or a crash between send and outcome"; reservation held and account-wide `unknown_order` (S1 cut). Rev9 halts on an "uncertain transport/order outcome" (halt/resume §2 row 1) | The timing difference: the code classifies at once (the attempt is journaled `UNKNOWN` before send and kept on a transport exception, `:1674`, `:1685-1688`), while the spec's `pending` waits for the one-bar timeout except on a crash; confirm the rev9 halt covers that interval. Resolution only by order-level evidence (Gate A A1, A3) |
| (iv) Terminal order | Accepted terminal (fill, cancel, reject) postdating preparation | Resolved (`:795`); a `REJECTED` attempt is skipped (`:791-792`) | Resolved by the terminal event, or by postdating `W` absence plus consistent `P` | That a rejection counts as terminal only where Gate A A3 admits it (a local pre-dispatch refusal; a remote refusal only with request-specific closure) |

**If the operator still wants B for the first release, rule these first** (each is added to the incident ADR's open list; none is adopted):
1. **B-B1: continuous or resume-after-flat?** Amend the halt/resume §2 row for narrowed-shape unknowns too, which gives continuous admission and changes a live-risk contract, or accept B as resume-after-flat. Rule 4′'s wording must match the choice.
2. **B-B2: exceptional-mode trigger.** Rule 4′ defines the mode by the account fence, so the fence repair (four-state trace) decides when the mode begins.
3. **B-B3: Aegis under a held reservation.** Accept or reject that any held reservation may block a full-size Aegis entry, and that a takeover cannot complete while a displaced leg holds a reservation (`book_capacity.py:277-278`).
4. **B-B4: split with an unknown child** (UB-8 Q5). Does it count as "closed" for add eligibility? UB-4's rule implies not, because an unknown child keeps the sequence open.

**Effect on the incident ADR (proposed; not applied here):** record the first-release posture as preserve-and-block under the §A10 acceptance condition. Add B-B1 to B-B4 to §A10's OPEN list. Rule 4′'s "exceptional mode" stays defined by the fence as repaired under the four-state trace.

---

## 4. Allocation and component reductions (gate D)

**Source:** the [allocation map](2026-09-25-tradeify-capability-allocation-deletion-map.md), as corrected. Recommended boundary: **one durable account owner** plus the barrier, the private ports and the watchdogs, and a thin CrossTrade REST adapter. The vendors own execution only. That is:
- **Tradovate:** matching, the resting stop entry, one-contract OSO creation and first-fill activation, and fixed stop/target execution between bars;
- **CrossTrade:** transport and ids;
- **TradingView:** research and export only, under the standing ruling.

| Disposition | Items | Condition |
|---|---|---|
| **Avoid building** | TradingView webhook ingress and alert manifest (B01); Pine market-input publisher (B02); intrabar trail manager and protection feed (B03); automatic incident dispatch (B04); partial-fill residual cover (B07) | The standing TradingView ruling; the edition freezes. For B07, "avoid building" applies to one-contract requests only; for a whole-leg liquidation it is subject to the accepted close amendment (§1.1a (a)–(b)) |
| **Defer** | Option-B machinery (B16), deferred with B, which stays Proposed | The §3 direction: reconsider B after actual reconciliation and operating evidence |
| **Reduce after freeze** | ATTACH path (B05); live use of trailing fields, via a live-sender guard (B06) | The Striker, ORB and Vanguard editions freeze and requalify. Code stays in place for replay parity, and the E1 inventory rebinds if code changes |
| **Retain** | Ports, emulator, parity and bundles (B08); feed (B09, funding deferred); runtime and loop (B10); account-owner core (B11); protection amend path (B12, dependent on GC-2b/GC-3); settlement (B19); legacy M1 path, guarded (B17) | — |
| **Introduce (required by the route)** | One-contract split and sequencing (B13); close realization per the accepted close amendment (none accepted yet; C-a is the first candidate, §1.1); Striker crossed-level exit (B14, as B-7 rules); REST producer with post-placement poll and same-session recipe (B15); **resting-order fence repair (§3)** | T09 scope (§5) |
| **Delete** | **None established.** No removal candidate has met its conditions | — |

**Conditional savings** (the corrected note's rule):
- Bracket creation is not protection. Vendor protection counts only once the stop is **Working** (GC-2a).
- Splits and multi-order closes can still complete partly (UB-4; UB-5). A whole-leg liquidation, if accepted, is itself a request that can fail or complete partly (§1.1a (b)).
- Moving work to a vendor adds local reconciliation: the late-reject poll (GC-8), the coverage-repair actor (A8) and postdating, coherent reads (GC-3).

**Freeze impact:** the qualification trust domain binds the account owner, protection owner, capacity, takeover, protocol, feed and the ports. Every T09 change to those modules changes the E1 freeze inventory (allocation map §B).

---

## 5. T09 handoff — HELD until B–D acceptance

**Status: HELD. Not dispatchable.** It becomes dispatchable only when:
- gates B, C (for the bounded design) and D are accepted on the T09 gate table;
- a close realization and its close-contract amendment are accepted (B-1; the §1.1a amendment if C-a is pursued), none yet;
- the edition rules it depends on, including the ORB resting-entry lifecycle (B-13), are frozen or explicitly held;
- it is re-committed as its own handoff under the committed-handoff rule.

The draft below fixes scope and boundaries only.

**Selected outcome:** a disarmed CrossTrade REST adapter and reconciliation path behind the existing account owner. It realizes the recommended boundary (§4) under **preserve-and-block** (§3), with every route-dependent step held behind its gate-C trace.

| In scope | Interface / evidence | Held behind |
|---|---|---|
| REST producer: `orders/place` (one-contract OSO with a per-attempt `clOrdId`), `change`, `cancel`, `close`; lifecycle, status and fill reads mapped to `BrokerFact` and `ProtectionSnapshot` | Gate A A1, A3 (i)–(iii), A7; REST-form traces (webhook evidence only for a demonstrated common downstream property) | GC-2a, GC-2b, GC-3 |
| Outcome classifier: local pre-dispatch refusal, remote refusal after dispatch, positive lookup (facts it establishes only) | Gate A A3 | — (design); traces for the evidence |
| Post-placement status poll within the protection deadline | GC-8 | — |
| One-contract split, per-symbol sequencing, whole-intent capacity reservation, abandon-remainder rule | B-6, B-9; UB-4 | Edition freezes |
| Close realization per the accepted close amendment (none accepted yet); completion on postdating, coherent evidence | B-1; the accepted close-contract amendment (the §1.1a amendment if C-a is pursued), with its OPEN items settled or their residual risk accepted by the operator | Vendor semantics; GC-1 traces; GC-3; GC-7 |
| Striker close-time crossed-level exit, as B-7 rules (whole-leg only if the condition cannot apply to a subset of lots) | B-7 | Source check; GC-1; STR-5 |
| Resting-order fence repair (§3): the four-state trace (fresh working, stale evidence, unknown dispatch, terminal), the settled spec reading and the repaired classification per consumer, including close operations; ORB resting-entry lifecycle per its ruled edition | §3 row 1; B-13 | Trace; ORB freeze |
| Live-sender guard refusing trailing fields and ATTACH on edition legs | B06, B05 | Edition freezes |

**Out of scope:** option B (B16); TradingView paths; any deletion; the feed provider (T14); settlement changes (T07); notifications (T13); drills, account access, arming, activation and spend.

**Verification:** fault-injected consumer cases for every GC failure consequence (the route stops or refuses, as §1 states), for each §1.1a element (a)–(e), and for each of the four fence states; retained REST-form traces for each delegated capability; `.\fp.ps1 test-ops` and `check` records. No live manufactured lost response or unmanaged exposure (checklist T09).

**Return boundary:** the adapter and reconciliation evidence, disarmed. It must not arm or activate, and it must not change anything outside the scope table.

---

## 6. Decisions required from the operator

Grouped by what each one unblocks. Every entry is a **recommended direction (executive review 2026-09-26); operator ruling pending**. Nothing here is a ruling. **The immediate route blocker is safe closing.**

**First: these decide whether the route can exit safely at all.**

| # | Decision | Recommended direction | § |
|---|---|---|---|
| 1 | Close realization, and the close-contract amendment | Investigate C-a first; accept no close guarantee yet. Commission the §1.1a amendment (a)–(e), unknowns OPEN; if the guarantee stays unavailable, a residual-risk statement returns to you. C-b is an unapproved alternative needing its own expression decision. Reject C-c | B-1, §1.1 |
| 2 | Reads, evidence and the drill plan | Authorize the two REST reads (known order, same session; known order, prior session), bound to exact read operations and account scope. Request the concrete order-producing drill plan (environment, exact actions, exposure limits, abort and recovery) before any execution is authorized | A-1 |
| 3 | Account actor inventory (exclusivity) | Complete it; exclusivity accommodates the attended intervention procedure, whose route-specific intervention/quiescence procedure and residual request accounting are still owed (halt/resume §1; OPEN); enable no vendor backstop | B-12, GC-7 |
| 4 | Entitlement and venue-permission evidence | Required before any live use | P-1 |

**Second: unknown-request posture.**

| # | Decision | Recommended direction | § |
|---|---|---|---|
| 5 | First-release posture | Preserve-and-block; defer B's implementation; B stays Proposed. Suggested ruling text in §3 | §3, B-10 |
| 6 | Horizon and consequence | One attended session, then explicit review before extending. Record whether you accept that one unresolved request may suspend automation on this account indefinitely (the account stays halted: recovery cannot complete and resume is refused, halt/resume §3–§4). No ε is requested | §3 |
| 7 | *Only if B is wanted for the first release:* B-B1 to B-B4 | — | §3 |

**Third: edition rules, frozen with the pre-registrations.**

| # | Decision | Recommended direction | § |
|---|---|---|---|
| 8 | ORB-2/3/4 and Vanguard VAN-2/3/4 | Existing fixed-stop component and existing remaining exits; no invented replacement exit; verify that the successor settings make every amend a noop | B-4, B-5 |
| 9 | Striker initial stop, STR-2 | The signal-bar-computable level, as a pre-registered behavior change | B-3 |
| 10 | Split size and partial acknowledgement: STR-3/4, VAN-5/6, and the VAN-6 counter wording | Whole-intent capacity reservation; sequential submission; abandon the unsent remainder on an exceptional outcome; no retry or top-up of an unknown child | B-6 |
| 11 | Exit-split rows (ORB-6, STR-7, VAN-8) | Follow the accepted close realization (none accepted yet) | B-2 |
| 12 | Striker crossed-level exit, STR-5 | Decide only after establishing whether the condition can apply to a subset of lots; never widen a subset exit into a whole-leg liquidation | B-7 |
| 13 | Split sequencing and replay pricing | Sequential one-contract requests with stated delay and price rules; qualification covers them | B-9 |
| 14 | ORB resting-entry end of life (one-bar cancel versus session-end cancel) | Resolve from source before the ORB freeze; not chosen to make the fence stop blocking; any change enters the ORB edition and replay | B-13 |

**Required correctness repair (not a decision):** the resting-order fence (§3, four-state trace). It is listed so that decision 14 is not made to stop the fence blocking.

**If a capability fails,** the affected question returns to you with alternatives; none is adopted automatically: Striker or Aegis amends (GC-2b/GC-3; e.g. a fixed-stop edition); ORB and Vanguard noop reads (GC-3); the Aegis takeover (GC-5; e.g. no takeover); ORB resting-entry end of life (GC-4); the close (GC-1; a residual-risk statement).

**Not requested here:** freeze, T09 dispatch, the execution of any drill (decision 2 requests reads and a plan only), deployment, arming or spend. **The qualification S5 freeze** (execution-slices plan) is decided separately through its decision draft, [PR #517](https://github.com/Joshua-Asante/first-passage/pull/517) (`docs/notes/2026-09-26-s5-decision-draft.md`, branch `claude/s5-decision-draft`). Its release conditions are in that draft, and the freeze remains held. It is unrelated to rail S5 (scoped exit/flat), which the §1.1a amendment would change.
