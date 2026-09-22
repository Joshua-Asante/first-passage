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
- [ ] **Early go/no-go: unknown-request resolution (R3).** The contract requires a terminal / no-future-effect fence for the original request scope, including across session reset. Establish from primary sources (Tradovate API docs, CrossTrade docs, retained page bytes — hash each) whether any mechanism yields that fence: client-order-id correlation plus a documented terminal-state read, an order-status query with documented completeness, or none. If none exists, **stop here** and return the decision; T09 cannot be specified without it, and "resend on absence" stays rejected.
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
_Pending._ R3 verdict first; R5 inventory (redacted); R2/R4 producer + export hash; the N1(a)–(g) table; AMENDMENT_REQUIRED items; the T09 route contract or the incompatibility decision; retained-source hashes.
