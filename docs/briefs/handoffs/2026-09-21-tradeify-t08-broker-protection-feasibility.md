# Handoff — Tradeify T08: broker and protection feasibility decided (CAP R2–R5 / N1(a)–(g))

**Type:** cc_handoff (source-backed capability decision; adapter code is explicitly out of scope)
**Date:** 2026-09-21
**Status:** RETURNED 2026-09-24 at the step-1 hard early return (follow-up rulings 2026-09-25 in §7.8): **R3 = NONE** (no documented terminal / no-future-effect fence for the route), §7. Steps R5, R2/R4, the N1 map and the verdict were not executed, per §2 and §4. Under the ratified D-broker wording the conditional grant is void (§7.6). Operator decision owed; recommendation in §7.7. Originally: dispatchable now under existing authority, independent of T01–T06 and of PR #448. Parent packet: [deployment checklist §T08](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md). T09 (the real adapter) is gated on this packet's verdict and on operator decision **D-broker**.
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
_Required shape (as authored):_ R3 verdict first; R5 inventory (redacted); R2/R4 producer + export hash; the N1(a)–(g) table; AMENDMENT_REQUIRED items; the T09 route contract or the incompatibility decision; retained-source hashes.

Executed 2026-09-24 by the coordinating Claude Code session at the operator's direction ("start with T08 step 1"). This is documentary work only. No login, account page, form, support contact, order action or drill took place. Vendor pages were retained as raw bytes under the primary checkout's `local_artifacts/t08-r3-2026-09-24/`, which holds 1,802 files and 72.2 MB. At capture time that root was excluded only by the clone-local `.git/info/exclude`; PR #484 adds the tracked `/local_artifacts/` ignore. Every file is hashed in `EVIDENCE_INDEX.sha256` there; that index's own SHA-256 is `974ea080aaa3dc0a3d421dea7a1dcd15af2786922b2ca8d239513a40edba065a`. The whole root is archived in `first-passage-archive` (M-41): all 1,469 distinct digests, with every committed blob verified against its name. The index and every digest cited here are registered in `docs/evidence/PRIVATE_EVIDENCE.sha256`. No vendor text is reproduced in this repository.

### 7.1 Status and verdict
**`DONE` — R3 = NONE.** No primary source documents a mechanism that yields a terminal / no-future-effect fence for an original request whose outcome is unknown on the route CrossTrade webhook → Tradovate (incumbent eval). The mechanism would also have to hold across the daily session reset and have all-actor scope. Per §2 and §4 this is the hard early return. **T09 cannot be specified**, and "resend on absence" stays rejected. The contract outcome for any unknown request therefore remains the CAP row "Not found, timeout, partial history or unsupported retention": **preserve the original attempt and its block, with no resend and no reservation release.**

### 7.2 Method
The work ran as one refute-first research workflow in four stages.

1. **Sweep.** Six independent lenses swept the sources:
   - L1: CrossTrade webhook lifecycle.
   - L2: CrossTrade's Tradovate REST API and public OpenAPI.
   - L3: Tradovate's native API, partner docs and staff forum posts.
   - L4: session reset and time boundaries.
   - L5: account-level fences and kill switches.
   - L6: vendor changelogs and help centres.

   Every claim was bound to a retained file and checked against a verbatim quote found in those bytes: 467 claims, all quote-verified. Secondary sources counted only as leads.
2. **Synthesis.** A synthesis step assembled every candidate protocol, including combinations across vendors.
3. **Voting.** Three independent lenses voted on each candidate:
   - documentary: re-hash the file and re-find the quote;
   - contract fit: the CAP R3 disposition and the self-service closure plan's outcome table;
   - counterexample: a documented-possible event sequence with a later effect.

   A candidate survived only if all three failed to refute it.
4. **Completeness critic.** A critic added four targeted follow-ups:
   - F1: every one of the 594 CrossTrade sitemap pages no lens had retained, plus the API endpoint index.
   - F2: Tradovate partner release notes, best-practices, terminology, environments and maintenance pages, plus a crawl of all 468 partner pages.
   - F3: a documentary check of the "irreversible termination" class: prop-firm revocation, archive and permanent lock.
   - F4: the JS-only Tradovate support articles, read through the site's public guest read-only record endpoint with no login.

   The candidates each follow-up produced were voted on the same way.

In total, 24 candidates were voted on, 14 in round one and 10 in round two. **None survived.** The critic rates the risk that NONE flips to an operable fence as LOW. A flip would need two independent positive findings in unread vendor text: a CrossTrade bound on **all** deferred work (or a terminal per-request state), and a Tradovate-side terminal definition (or keyed cross-reset coverage).

### 7.3 Why no fence exists: independent blockers, each sufficient
Each row cites the retained file and the first 16 hex characters of its SHA-256. Capture dates run from 2026-09-23 to 2026-09-24 UTC.

| # | Blocker | Load-bearing sources |
|---|---|---|
| 1 | **The key is a label, not a fence.** A client key exists before transport and reaches Tradovate (webhook `cl_ord_id` → `clOrdId`). Neither vendor deduplicates a plain placement, Tradovate accepts a repeated `clOrdId`, and no uniqueness rule is documented at any scope. | `L1__tradovate-webhooks.html` `adaa513e8eb096a8`; `L2__api_tradovate_overview.html` `f84d10c1aa95904a`; F2 partner-corpus negatives |
| 2 | **No lookup by key.** The Order entity carries no `clOrdId`. The key appears only on the lifecycle's New command, so matching means enumerating orders and reading each lifecycle. CrossTrade's OpenAPI and its prose contradict each other on a by-`orderId` read. | `L3__api_tradovate_main_chunk.js` `a4e4271b900e3238`; `L2__api_orders_get-order-lifecycle.html` `88cbc69010e131f5`; `L2__api_orders_get-order.html` `176375eb83477b49` vs `L2__app_v1_api_openapi.json` `816ee11fa8bef55d` |
| 3 | **No read is documented complete, and several are documented partial.** Lifecycle reads can succeed while partial. Command reports are capped at the last 10. A Command exists only once it is bound to an Order id, so requests that never became orders have no record. | `L2__api_orders_get-order-lifecycle.html` `88cbc69010e131f5`; `L3__api_tradovate_main_chunk.js` `a4e4271b900e3238` |
| 4 | **No state is defined as terminal or no-future-effect.** Acceptance is not terminal: a placement can be accepted and then rejected about a second later. A timeout does not establish placement. Tradovate's `Pending New` is an explicit unknown resolved only by contacting support. Only Filled and Cancelled carry finality wording, and that is per-order UI text, not a request-scope contract. | `L2__api_tradovate_overview.html` `f84d10c1aa95904a`; `L1__api-webhook-trading.html` `d6af1d9c9620895e`; `L6__tvzd_article_219454917.json` `f94ef16bd2568329`; F4 support-article captures |
| 5 | **CrossTrade can act after the HTTP exchange, and nothing bounds all of it.** Documented deferred work includes a delay timer of up to 300 s, durable recovery that resumes mutations, OCO coverage repair, 24 h managed-ATM retries, cancel-after watchers and copier retries. Late-request discard is documented for the NT8 path only. F1 found no bound across all deferred-work classes in 594 further pages. | `L1__adv-delay-timer.html` `411c7e629aac4c7d`; `L1__tradovate-webhooks.html` `adaa513e8eb096a8`; `L1__adv-tradovate-atm.html` `6b1ab99338b3949b`; `L1__changelog-xt-versions.html` `7d328ba342e2c824`; `F1__MANIFEST.tsv` `8191f9cf8ef8ba86` |
| 6 | **The session reset erases the lookup surface while effects cross it.** Order and fill lists are session-scoped and empty after the ~5 PM ET reset. Earlier-session orders never reappear. Tradovate staff state that a day's data is archived at close, with only current-day orders readable through the API. Webhook bracket exits are sent GTC. Suspended/time-released orders are released later. | `L2__api_tradovate_overview.html` `f84d10c1aa95904a`; `L2__api_orders_get-all-orders.html` `229669bc9760daa6`; `L3__community_t6194.json` `7124c348a48add68` (staff, 2022); `L1__tradovate-order-types-and-exits.html` `1142e6b7f340adac`; `L6__tvzd_article_219454917.json` `f94ef16bd2568329` |
| 7 | **No all-actor scope.** Every CrossTrade control (kill switch, Block Signals, Closing Only, locks, key rotation, unlink) is an ingress gate on new CrossTrade signals and does not reach manual or other-platform orders. The one broker-side all-platform lockout (Tradovate Prop manual lockout) is documented only in vendor blog posts. It is UI-only, at most 24 h long, silent on requests still pending in CrossTrade, and unverified for this account. | `L1__adv-kill-switch.html` `31f5791742ebfcb3`; `L1__tradovate-account-manager.html` `e0ebea5046fa7060`; `L5__tv_prop_manual_lockout.html` `4e7cda3ca1d8fe2a` |
| 8 | **No source-backed common causal ordering** between request preparation, dispatch and broker effects. | L1/L3/L5 negatives |
| 9 | **"Irreversible termination" is not a fence either (F3).** Revocation, admin locks and failed-eval states are documented as reversible by the org admin. The only permanent state is archival after a 10-day wait, and archival deletes the account from the API, so no terminal read or ownership transfer is possible afterwards. | F3 captures (`F3_capture_log.tsv`) |

The 24 candidates and why each fell:

| Candidates | Why they fell |
|---|---|
| C1, C2, C5, C6, C7 (the correlation and read family) | Blockers 1–4 and 6 |
| C3, C4, R2-C3, R2-C4 (intake-log search; received no-effect classes such as a 429, a p-ticket or an auth gap) | They need a received response or a classified row. Timeout and absence stay unclassified. |
| C8–C11, R2-C10, R2-C11 (CrossTrade ingress fences; Tradovate risk, admin and prop locks) | Blockers 5 and 7, and reversibility |
| C12, R2-C12 (DAY/GTD/cancel-after lifetime) | They bound only an already-identified order. GTC exits and deferred work escape them. The demo engine does not enforce GTD or scheduled cancels. |
| C13, R2-C13 (composites) | They inherit every unbounded component. |
| C14, R2-C14 (guarded resend / duplicate-`clOrdId` tombstone) | Disqualified. No duplicate-`clOrdId` reject value exists in the retained Tradovate enums, and any probe is a trade that needs an operator GO. |
| R2-N1 (end the eval), R2-N2 (Tradeify admin lookup), R2-N3 (operator UI reconciliation), R2-N4 (MCP async job) | Destructive or admin-only, not keyed or complete, or scoped to NT8 jobs only |

Positive fragments (a pre-transport key, in-session positive correlation, per-order UI finality for Filled and Cancelled, DAY session-end expiry for an identified order) remain useful to a future protocol. None of them closes the negative side.

### 7.4 Findings beyond R3 (recorded, not acted on)
- **No native API for the eval.** Tradovate's support article states that prop-firm and evaluation accounts are not eligible for API access. Its API docs and staff posts require a LIVE account with more than $1,000 plus an API subscription. So no route that reads Tradovate natively is available for the incumbent eval. Evidence: `F4__tvsf_Tradovate-API-Access__record.json` `4a91db885f44d8ce`; `L3__community_t2380_how-do-i-access-the-api.json` `dbc5eaaa70ac4c6b`.
- **The CAP pages: new bytes, mostly unchanged text** (corrected in review, 2026-09-24). All three CrossTrade pages CAP retained on 2026-09-17 have different bytes now. The API overview is `f84d10c1…` (was `dd7f839a…`), the webhook advanced/internals page is `adaa513e…` (was `ebba0572…`), and cancel-replace is `21a8e8c7…` (was `a0000d0d…`), after CrossTrade rebuilt its docs on 2026-09-21. Byte hashes change with every site build: same-day captures of the same URL differ only in the bundle file names. A text-level comparison is the meaningful check:
  - The API-overview and cancel/replace text is unchanged.
  - The internals page dropped its "Trailing protective stops" section. Its CrossTrade-managed triggered-trail wording remains on the current pages, so CAP's 09-17 statements (including the L2(g) and L2(c) incompatibilities) still stand.

  The earlier sentence about the Tradovate order-status article is withdrawn. `cedcc29c…` is the generic script shell shared by 22 different Tradovate support pages, so it shows nothing about any article's content.
- **Independent corroboration.** A separate documentary pass the same day, in closed PR #479, reached the same R3 = NONE on its own capture of 54 files. That capture is `CAP-20260916/t08-r3-20260924`, manifest `a56a09cdf02dc378ed2d3ae5eab5cc69650d287373757ac0aa350648cde3fc3c`, archived and registered. It adds two corrections to how the route is described:
  - For non-TradingView senders, a successful webhook response means Tradovate accepted the order. Only TradingView-originated requests are documented as acknowledged before processing.
  - Alert History can be read through CrossTrade's MCP signal-history tool (Elite plan). Both remain covered by candidates C3/C4 here: a timeout or absence stays unclassified.
- **Evidence hygiene.** Lens manifests were partly overwritten by a shared fetch script. Cite the lens-private manifests named in the evidence root, not the mixed `L1__MANIFEST.tsv`.

### 7.5 Not reached, and residual risk
- **Unread surfaces:**
  - `help.tradeify.co` (Cloudflare 403; not bypassed);
  - the full body of CrossTrade's 2026-09-21 release notes (the retained bytes are truncated);
  - the gate-order diagram on CrossTrade's advanced-options page (alt text only).
- **Thin but load-bearing sources:** 'repeated `clOrdId` accepted' comes from CrossTrade only; archive-at-close rests on Tradovate staff forum posts from 2021–2023; the prop lockout is blog-only.
- **The unbounded lifetime of CrossTrade deferred work** is the premise that most decides the verdict. It is backed by one sentence on durable recovery plus the absence of any bound across roughly 1,100 CrossTrade pages.
- **The preserved attempt's actual payload fields were not bound.** Which deferred-work classes apply depends on them, but durable recovery and the reset keep NONE either way.

### 7.6 Consequences and decisions this opens (none taken)
1. **D-broker.** The ratified wording reads: "granted automatically when T08 returns R3 = fence exists, and void if T08 returns R3 = none." This return is R3 = NONE, so the conditional grant is **void by its own terms**. No broker access was granted or used.
2. **T09 and the live route.** T09 stays unspecifiable, and CAP R3 stays blocked for live release. Moving forward needs an operator decision among contract or route options, for example:
   - (a) a contract amendment that defines an attended, bounded-exposure posture for unknown requests;
   - (b) a written vendor statement bounding deferred work for a narrowed request shape (support contact needs its own authorization);
   - (c) a different route (§7.4 rules out native Tradovate API for the eval);
   - (d) holding live release.

   Any contract change is an ADR-level decision. The return itself proposes none; §7.7 records the review's recommendation.
3. **CAP record.** A dated addendum records this return against row R3 (CAP-20260916, "Addendum 2026-09-24").

### 7.7 Recommendation (review, 2026-09-24; operator decision, none taken)
There is no clock pressure. The 2026-11-08 four-firm falsifier is discharged by a lab re-MC, not by a live session (deployment-checklist amendment, Addendum 2026-09-22).
1. **Hold live release** (option d) until item 2 or 3 is settled.
2. **Authorize one narrow vendor question** (option b; support contact needs its own authorization). The question: for a narrowed request shape, is there a documented upper bound on when an accepted request can still reach Tradovate, including durable recovery? The narrowed shape is a plain market or stop entry carrying its own native OSO stop, sent without `delay=`, ATM fields, `cancel_after` or copier fan-out. The answer is cheap to get, and it is the only way to source a real interval.
3. **Scope the ADR-level amendment in parallel** (option a) as a bounded-exposure posture, not a time-based clear. Flatness, elapsed time, empty reads and operator acknowledgment stay insufficient as closure evidence (halt/resume §3; incident ADR §5). The amendment would:
   - admit only the narrowed request shape;
   - give every exposure-creating entry its own native stop;
   - keep an unresolved request's reservation and block;
   - quarantine any later unexplained effect as an incident.

   It must name the owners it amends: halt/resume §3 and §4, rail E3, the CAP R3 disposition and the closure-plan outcome table. Any interval it relies on must come from item 2, and must cover documented deferred work (24-hour managed-ATM jobs, GTC bracket exits).

Option c (route change) is not recommended. Every route ends at Tradovate, and §7.4 rules out native API access for the eval.

### 7.8 Operator ruling on the return (2026-09-24)
Recorded after the return; §7.1–§7.7 are unchanged.

| Item | Ruling (operator, in session, verbatim) | Consequence |
|---|---|---|
| §7.7 recommendation | "approve item 1" (item 1 of the coordinator's 2026-09-24 decision list = this section's three-part recommendation) | All three parts adopted, as set out below. Option c (route change) was not adopted. |

1. **Hold live release (option d).** CAP R3 stays blocked, T09 stays unspecifiable and D-broker stays void, as §7.6 says. The hold ends when part 2 or part 3 settles. Engineering (S4–S8), T07, T10 and the provider-neutral T14 work continue; none of them needs the route.
2. **One narrow vendor question (option b) is authorized.** Joshua sends it from his own support account; no agent contacts a vendor. The draft text is in [the vendor-question note](../../notes/2026-09-24-t08-vendor-question-draft.md). The answer is evidence only when it is written, retained as original bytes under the private root, and hashed; a chat reply that is not retained, or a verbal answer, does not count. One question, one follow-up at most. It must not carry account identifiers.
3. **Scope the ADR-level amendment in parallel (option a).** The scope is in [the bounded-exposure scope note](../../superpowers/specs/2026-09-24-bounded-exposure-unknown-request-amendment-scope.md). Scoping grants no contract change: the governing owners (halt/resume §3–§4, rail E3, CAP R3, the closure-plan outcome table) stay in force until an amendment is accepted and propagated.

This ruling grants no broker access, route change, drill, order action, arm or spend.

**Follow-up ruling (2026-09-24, in session, verbatim):** "I accept B. You can proceed as scoped." The scope's Q1 is ruled **B** (a permanent worst-case reservation replaces the account block for narrowed-shape unknowns). The scope's §5 steps 2–4 are authorized; acceptance stays with the operator.

**Follow-up rulings (2026-09-25, in session; owner: [campaign record §59](../programs/2026-09-03-seven-strategy-select-campaign-state.md#59--route-native-expressions-for-the-accepted-book-three-operator-rulings-2026-09-25)):** (1) Vanguard MGC and Aegis 6J fit the narrowed shape — operator-attested ("yes and yes"; private ports unread by any agent). (2) The vendor question above was **sent** on 2026-09-25 by the operator; no reply is recorded. (3) The operator adopted **route-native expressions** for ORB MNQ (fixed-stop OSO bracket, no trailing) and Striker MYM (entry carrying its stop in the same OSO; one-contract requests) as a pre-registered K=1 requalification, not a search. R3 stays NONE; D-broker stays void; live release stays held; no drill, access or spend is granted. The N1 rows that remain after §59 are the K items and the §A1 admission precondition.

**Drill authorization (2026-09-25, in session, verbatim):** "I authorize the remaining T08 drills." This covers D1–D4 of the [operator session plan](../../notes/2026-09-25-t08-drills-t07-reads-operator-session.md). **Joshua performs each drill.** No agent order action is involved (CAP "Bounded collection and rehearsal procedure"). The plan's §2 scope block needs one written confirmation before the session. The residual exit-side partial-fill row is moot under the one-contract rule. D-broker stays void, and live release stays held.
