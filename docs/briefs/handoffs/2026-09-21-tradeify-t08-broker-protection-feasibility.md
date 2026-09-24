# Handoff — Tradeify T08: broker and protection feasibility decided (CAP R2–R5 / N1(a)–(g))

**Type:** cc_handoff (source-backed capability decision; adapter code is explicitly out of scope)
**Date:** 2026-09-21
**Status:** dispatchable now under existing authority, independent of T01–T06 and of PR #448. Parent packet: [deployment checklist §T08](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md). T09 (the real adapter) is gated on this packet's verdict and on operator decision **D-broker**.
**Executor:** one capability executor (Claude Code; this is reading, tracing and deciding, not building). **Operator:** Joshua supplies the enabled external-actor and outstanding-request inventory (R5) and the platform entitlement facts; **no agent places, amends or cancels an order, and no drill runs without its own written authorization.** **Coordinator:** owns the CAP R2–R5/N1 rows and the incident-contract reconciliation.
**Authority:** read every owner below; write the return section, a dated append-only addendum to the CAP record, and (if the verdict is "amendment required") a proposal document. No adapter code, no route configuration change, no ADR status change. A `DONE` status supplies no permission.

## 0. Owners to read first (anchors at `main@abb3914`)
- `docs/briefs/phase4-preparation/2026-09-16/capability-decision.md` — **CAP-20260916**: rows R1 (QUALIFIED, local engineering only, code `7c31770`), R2–R5 UNPROVEN, N1 UNPROVEN for the whole route (:42-47); "R3 source result and N1 incompatible realizations" (:103-135) — the three retained primary pages (SHA-256 recorded there): the Tradovate API overview's positive-correlation recipe (excludes inline ATM; its absence-based resend step is **not adopted**), the execution-internals distinction between native continuous trailing and an inline OSO bracket's CrossTrade-managed triggered trail (**UNSUPPORTED for L2(g)**), and Cancel/Replace as guarded cancel-then-place (**UNSUPPORTED as an L2(c) atomic amend**); "Integration disposition and remaining work" (:182-200).
- `docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md` — **Status: Proposed**; §2's effectiveness gate: dependent behavior is recorded **AMENDMENT_REQUIRED**, never QUALIFIED under the proposed exception, until accepted and propagated. `docs/superpowers/specs/2026-09-17-attended-platform-protection-recommendation.md`.
- The governing rail and halt/resume contracts CAP cites (S1/S2/S3/H revisions; L2(a)–(g) primitive list) — read the L2 list in full and quote each primitive verbatim in the return.
- `ops/c1_rail/book_account_owner.py` @7ba7844 — `BrokerFact` :152, `BrokerResult` :179, `BrokerCommand` :191 (the owner's command/fact contract the adapter must satisfy), `SyntheticBroker` :207 (test-only), `DispatchResult` :231, intent-before-send and unresolved-reservation semantics. `docs/superpowers/specs/2026-09-16-tradeify-settlement-order-feasibility-design.md`.
- Memory-derived facts to verify, not assume: CrossTrade has no Tradovate market data (bars/quotes/WS are NT8-only); the CrossTrade→Tradovate relink needs the Tradeify-issued credential; the Tradeify support reply closed the certified-close source avenue.

## 1. Selected outcome and return boundary
**Outcome:** one exact route (named: CrossTrade webhook → Tradovate on the incumbent eval, or an explicit alternative) supports every required order semantic and **unknown-request closure**, each with source-backed evidence; or a concrete incompatibility is established per primitive. **Return boundary:** an implementation-ready capability contract for T09, or an exact route/behavior decision (including "amendment required" with the proposed contract change). **No whole-route PASS from documentation alone**; no adapter code; no drill without its own authorization.

## 2. Steps
- [x] **Early go/no-go: unknown-request resolution (R3).** — **Returned 2026-09-24: NONE** (§7). The contract requires a terminal / no-future-effect fence for the original request scope, including across session reset. Establish from primary sources (Tradovate API docs, CrossTrade docs, retained page bytes — hash each) whether any mechanism yields that fence: client-order-id correlation plus a documented terminal-state read, an order-status query with documented completeness, or none. If none exists, **stop here** and return the decision; T09 cannot be specified without it, and "resend on absence" stays rejected.
- [ ] **R5 — actor inventory.** Joshua supplies the current enabled external actors (managers, copiers, manual sessions, queued or scheduled requests) and outstanding requests on the account; the executor records it as a dated inventory (no identifiers) and derives the "all-actor delayed-effect fence" requirement from it.
- [ ] **R2/R4 — history producer.** Identify one entitled producer with complete request/order/fill/protection history and documented causal bounds (what is guaranteed present, in what order, after what delay). Obtain one original nonempty order/fill export through a working download path (Joshua exports; bytes retained privately, hashed) and show that a consumer can bind it to a runtime attempt identity. Periodic history reads and current-session reads are not, by themselves, complete causal history (CAP R4).
- [ ] **N1(a)–(g) — per-primitive map for all four legs.** For each of: entries, partial fills, adds (executed-base), native amendments (L2(c) — ordinary native modify is the remaining candidate; needs rejection/unknown-outcome and old-protection-survival evidence), trailing/OCO (L2(g) — native continuous trailing only; inline triggered-trail is UNSUPPORTED), scoped exits, takeover, cutoff/flatten: cite the primary-source semantics, name the realization, mark **SUPPORTED / UNSUPPORTED / UNKNOWN-NEEDS-DRILL**, and state exactly what account observation would close it. Do not assume economic equivalence between a native protection and the contract's protection.
- [ ] **Incident-contract reconciliation.** For every primitive whose realization depends on the Proposed platform-protection exception, record AMENDMENT_REQUIRED and route the dependency to the ADR's acceptance, not to T09.
- [ ] **Verdict.** Route contract for T09 (interfaces the adapter must satisfy against `BrokerCommand`/`BrokerFact`/`BrokerResult`, the drill list with its authorization needs, the evidence each drill must retain), or the incompatibility decision.

## 3. Verification
Source-backed semantics only: every claim cites a retained primary page (SHA-256, capture time) or an original account export (hash, private root). Unsupported route → a decision, not speculative adapter code. The CAP addendum updates R2–R5/N1 per row with evidence references.

## 4. Checkpoints
The R3 go/no-go is a hard early return. A missing normal primitive (no native amend, no native trail) returns before the map is completed. Any drill proposal returns for operator authorization before execution.

## 5. Operator inputs
R5 inventory; entitlement facts; one original order/fill export; authorization for any bounded drill; **D-broker** (the access T09 will need) is a separate decision this packet informs.

## 6. Forbidden
Any order action; account identifiers in text; adopting the docs' resend-on-absence step; treating inline triggered-trail or cancel/replace as satisfying L2(g)/L2(c); qualifying anything under the Proposed incident exception; writing adapter code; whole-route PASS from documentation.

## 7. Executor return
_Required contents:_ R3 verdict first; R5 inventory (redacted); R2/R4 producer + export hash; the N1(a)–(g) table; AMENDMENT_REQUIRED items; the T09 route contract or the incompatibility decision; retained-source hashes.

### 7.1 Step 1 return — 2026-09-24 (Claude Code, documentary pass; no account access)

**R3 = NONE.** The primary sources for the CrossTrade → Tradovate route document no terminal or no-future-effect fence for a request whose outcome was not learned. They document a positive correlation inside one trading session. They document no negative closure. Nothing survives a session reset. Per §4 this is the hard early return: R5, R2/R4, the N1 map and the incident reconciliation were **not run**. Consequences:
- **T09 cannot be specified.**
- **D-broker is void** under its ratified wording ("void if T08 returns R3 = none", [Addendum 2026-09-22](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md)).
- No access, drill or adapter follows from this return.

**What each surface gives, and why it is not the fence.** Sources are CrossTrade docs and Tradovate partner-API docs, captured 2026-09-24 16:10–16:19 UTC (hashes in §7.3).

| # | Surface | What the source says | Gap against the fence |
|---|---|---|---|
| 1 | Client-id correlation (REST `orderId`/`clOrdId`; webhook `order_id`/`cl_ord_id`) | After an ambiguous reply, scan working and session orders; each candidate's lifecycle `New` command carries the `clOrdId`; "Place again only when no order carries your id." Neither CrossTrade nor Tradovate deduplicates a plain placement. Inline ATM submits no `clOrdId`. (P1, P5) | Positive match only. No read is keyed by `clOrdId`. The closure step is absence-based resend, which stays rejected (CAP R3). |
| 2 | Session scope | Order and fill lists "reset at the daily session close (around 5:00 PM ET) and stay empty until the next open, including all weekend." (P1) | The correlation evidence is purged at reset. Across a reset, even the positive match is unavailable. |
| 3 | Durable fill history | Rows carry `executionId`/`orderId`, with no client id. Capture is periodic ("not capture deadlines or guarantees"). Earlier sessions cannot be backfilled. A null cursor is "not verified capture completeness." (P3) | Cannot bind a fill to a request after reset. Cannot prove absence. Has no rows for orders that never filled. |
| 4 | Webhook route (current rail path) | "TradingView requests are acknowledged before background processing finishes." The page promises no synchronous broker result to script senders either. "A timeout does not establish whether an order was placed." `delay=` of up to 300 s runs before any Tradovate call. Per-identity pacing is "internal … may change without notice." Alert History is a dashboard view; REST calls get no Alert History row. (P4, P2, P6, P1) | No API gives a Tradovate-route request status. No documented bound limits how late an accepted request can still take effect. |
| 5 | REST route (Pro plan) | Returns an id on success. After `tradovate_unavailable` (30 s broker timeout), `internal_error` or a client timeout, the request "may still have reached Tradovate: CrossTrade never resends it." (P1) | No resend is good. But no terminal read exists for the ambiguous request. The route's closure is item 1's absence rule. |
| 6 | Tradovate native API | The `command` entity carries `clOrdId`, a `commandStatus` (including `Pending`, `PendingExecution`, `OnHold`) and an `activationTime`. Order status includes `PendingNew` and `Unknown`. Reads are by id or full list. (P8–P10) | No lookup by `clOrdId`. No retention or completeness statement. No terminal guarantee for a request missing from the list. |
| 7 | Kill switch / closing-only | Evaluated "before any broker routing." Orders placed manually or from other platforms "never pass through CrossTrade." (P7, P1) | Blocks new intake only. Nothing documents its effect on a request already past the check. It does not fence other actors. |

**Supported, recorded for later use:** inside the current session, an ordinary placement that carries a client id can be positively matched to one observed order. Ownership can then pass to that order, whose terminal states (Filled, Canceled, Rejected, Expired) are documented. CrossTrade states that it never resends an ambiguous mutation (P1, P2). A missing match proves nothing.

**Changes since CAP-20260916 (09-17 capture).** The API-overview text is unchanged; only the page bytes differ. The execution-internals page has dropped its "Trailing protective stops" section, which matters for N1-g, not R3. Items 2–4 and 6 are new to this record.

**Limits.** This is documentary evidence only. An undocumented behavior is not proven absent. But the contract needs a source-backed guarantee, and a drill cannot create one (CAP, bounded collection procedure). No support contact was made; CAP's R3 disposition does not authorize one.

### 7.2 Decision owed to the operator (not taken here)
Choose one of three paths:
1. **Contract amendment (recommended).** Write a proposal that says how an unresolved request with no positive match may be cleared without a fence. For example: an attended clear after a stated interval, with the account flat and order-free across a session boundary; any later unexplained effect is quarantined as an incident. This is the only path that keeps the incumbent route. E3 already holds the account block, so today one ambiguous request stops admission with no way to discharge it. That is §1's "amendment required" branch; drafting it needs the operator's GO.
2. **Vendor guarantee.** Get a written CrossTrade bound on late effect and a Tradovate terminal-state guarantee. This needs support contact, which is not authorized.
3. **Route change.** The Tradovate-side gap in item 6 applies to any route that ends at Tradovate.

### 7.3 Retained sources
Original bytes are held privately in capture batch `CAP-20260916/t08-r3-20260924`. Its manifest (`a56a09cdf02dc378ed2d3ae5eab5cc69650d287373757ac0aa350648cde3fc3c`) hashes all 54 captured files. Load-bearing pages:

| Ref | Page | SHA-256 |
|---|---|---|
| P1 | [CrossTrade Tradovate API overview](https://crosstrade.io/docs/api/tradovate/overview) | `02cc37b357d65d75abdd7df5972234ed4099f9317ca032d162c9cda8dcc8d49c` |
| P2 | [Tradovate execution internals](https://crosstrade.io/docs/webhooks/tradovate-advanced) | `e98e35f5b7f248ba7adfbf807ca4fa000cc1e3bf7556031147ab08f421b0cea1` |
| P3 | [GET Fill History](https://crosstrade.io/docs/api/tradovate/get-fill-history) | `1f5f19dde4d05a311bf61442d7db77ec70e746285f227ce00210d6da3d119881` |
| P4 | [Webhook Trading](https://crosstrade.io/docs/api/webhook-trading) | `8b849fbdbf7857f04abf6dc12450a493c67bb12a349e45fd8045305252a7fa52` |
| P5 | [GET Order Lifecycle](https://crosstrade.io/docs/api/orders/get-order-lifecycle) | `e639f615eb8243a6089044a977651c2b2f5bd6e644b09838e55335780a1c210c` |
| P6 | [Delay Timer](https://crosstrade.io/docs/webhooks/advanced-options/delay-timer) | `2888339b623e275cec8a0b726384f9e9f2107b012d2f43cd110c3944f4cf7455` |
| P7 | [Kill Switch](https://crosstrade.io/docs/webhooks/advanced-options/kill-switch) | `8da36fdb18f1c2e7f8c895003aaf9bed31299077d84d95e1fe0f87c8505580ce` |
| P8 | [Tradovate Command Item](https://partner.tradovate.com/api/rest-api-endpoints/orders/command-item) | `6ccd3e79b3d53d0eeff9b9e229d25e3d1bed1a00097880974e25397dd00d3aa9` |
| P9 | [Tradovate Command List](https://partner.tradovate.com/api/rest-api-endpoints/orders/command-list) | `dc42f6b5e5679720a5477352f82a4b36f4550221d9d16dfd8de25828059629d5` |
| P10 | [Tradovate Order List](https://partner.tradovate.com/api/rest-api-endpoints/orders/order-list) | `eccb01bb332c27adfd03e0842b5a1c1ef94220a2fcc9a4757e4060e24e3ab12e` |

Publication and effective-revision times are unknown. These are documents, not account observations. The eleven pins are registered in `docs/evidence/PRIVATE_EVIDENCE.sha256`. The M-41 archive copy exists only in a local clone and was **not pushed**, for two reasons: `first-passage-archive` is archived on GitHub (the push returned 403), and `core.autocrlf` changed one committed blob's hash. `make audit` will show these pins as not archived until the archive step is fixed.
