# Route commissioning session packet: operator-run, automation disarmed (2026-09-27)

**Trade-authority clarification (2026-10-01).** Categorical statements below that agents may not place trades, exit positions or cancel orders are **historical, superseded** by [ADR Addendum 2026-09-30b](../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-30b): Agents may place orders, exit positions and cancel orders only at the operator's direction for the specific act; `trade.submit` is an operator act at risk `high`, never grantable in a card. Arming, live-spend and per-session GO requirements are unchanged. This artifact grants no order action; its task-specific exclusions, named performers and separate drill approvals remain in force. It does not supply direction for a specific trade.

**Status:** PREPARED 2026-09-27 for coordinator review and operator checkpoints CP-2 and CP-3. Documentary only. **This packet authorizes nothing.** It places, amends or cancels no order. It does not read the account, contact a vendor, spend, arm or deploy. It sequences the rows of the [route drill plan](2026-09-26-tradeify-route-drill-plan-draft.md), which stays their **owner**. Row IDs, preconditions, pass/fail rules and consequences bind to the drill plan's text; this packet quotes only what the operator needs at the platform. Where this packet and the drill plan differ, the drill plan governs, and the difference is a defect in this packet to report. **One pending exception, named here:** §4's fresh-position sequencing for X-2 and X-3 departs from the drill plan's preconditions ("X-1's position is open", lines 241 and 256). It is routed to the drill-plan owner as a proposed amendment of those two lines, and X-2 and X-3 are not runnable on it until the owner confirms (§4, §7).

**Card:** [H2](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md) (lines 136–196), dispatch revision `521d8f2`. **Sequencing owner:** [checklist addendum 2026-09-27](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step), §0–§5 (lines 375–506). **Executor:** agent subagent (Claude Code, Opus 5.5), writing this one file only.

**R-2 disposition (2026-09-29):** the operator closed the preservation-trade investigation **with limits / inconclusive**. Both collector runs remain `STOPPED(HTTP_FAILURE)`; the prescribed sequence was not completed. Cross-session recovery remains unestablished and unresolved attempts stay held. This closes only the investigation's administrative HOLD and grants no Stage 1, trading or release authority. Decision and private-evidence pins: [drill-plan R-2 closure](2026-09-26-tradeify-route-drill-plan-draft.md#r-2-closure-with-limits--operator-decision-2026-09-29).

**Rulings applied** (read at their owners):
- **R-CLOSE (2026-09-26):** R-1/R-2 authorized after existing entitlement is confirmed; no order-producing row authorized; X-5 deferred; no automatic fallback to the live eval. Sources: [incident ADR §A11.1](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a111--operator-ruling-close-direction-2026-09-26) (lines 362–376) and the drill plan's ruling block (lines 16–42).
- **§A11.2 (2026-09-27):** no same-session restart of automation after an incident; review before another session ([incident ADR §A11.2](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27), lines 378–386).
- **§A11.3 (2026-09-27):** preservation-trade evidence as the read target ([incident ADR §A11.3](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a113--operator-ruling-preservation-trade-evidence-as-the-target-of-authorized-reads-2026-09-27), lines 388–399; drill plan lines 33–36).

**Consumed, not redone:** [#519](https://github.com/Joshua-Asante/first-passage/pull/519)'s close-semantics return, read at the pinned head `8c15f18`. It is unmerged. Its note is `8c15f18:docs/notes/2026-09-26-close-semantics-c-a.md` (cited below as **CS-note**). Its card is `8c15f18:docs/briefs/handoffs/2026-09-26-close-semantics-c-a.md` (**CS-card**), whose coordinator review, "ACCEPTED AS INPUT", is at lines 117–127.

**Result.**
- **Stage 0** (read-only; §2) can run once the CP-2 facts in §1 are supplied. *(2026-09-28: CP-2 facts and operator rulings recorded in [§1.1](#11-cp-2-record-2026-09-28); F-6(a) is answered conditionally; each Stage 1 row still requires its own CP-3, the operator's attestation of Tradeify's conditions, and the remaining prerequisites.)* It covers the host disarm check, the actor inventory, the entitlement record, the transaction identity of each read's target, R-2 and T07 R1–R3 on a completed preservation trade that qualifies, and R-1 in the session of this week's preservation trade. In Stage 0 the inventory is completed and recorded, but an actor found outside its required state does not by itself stop the reads; the drill plan's "session ends before it starts" rule applies from the first order-producing row (§2.2).
- **Stage 1** (order-producing; §3–§4) has four row cards. Each needs its **own CP-3**, and the rows run in this order. *(Updated 2026-09-28: the §3.7 documentary item is discharged for all four rows by the [§3.7 closure](#37-closure-2026-09-28--request-shapes-from-the-current-public-crosstrade-documentation); the per-row bullets below are otherwise unchanged.)*
  - **X-1:** ready on CP-3, except one documentary item: the exact `orders/place` request body for a market entry, which no owner names (§3.7). *(Closed 2026-09-28; X-1 now waits on the CP-2 facts (F-1, F-4, F-6), the §3.2 session preconditions and its own CP-3.)*
  - **X-4:** ready on CP-3, except the same item for a resting stop entry (§3.7; drill plan line 272: "none are specified here"). *(Closed 2026-09-28; X-4 now waits on the CP-2 facts (F-1, F-4, F-6), the §3.2 session preconditions and its own CP-3.)*
  - **X-2:** waits for M2's return. No M2 dispatch or return was found; see §4.3. *(Corrected 2026-09-28: M2 was carded later on 2026-09-27 and is DISPATCH-READY, [M2 card](../briefs/handoffs/2026-09-27-m2-modify-semantics.md); no return exists. See [§3.7 closure C.6](#c6-m2-x-2s-documentary-precondition-the-exact-remaining-dependency).)* *(Later 2026-09-28: M2 has returned, [#541](https://github.com/Joshua-Asante/first-passage/pull/541) (`DONE_WITH_CONCERNS`), with Q1–Q4 all `OPEN`. The coordinator's review of the return is not yet recorded. No documented read shows a working order's effective price after a refused modify, so an X-2 pass can show the refusal and a `Working` status, but "at its original price" rests on inference. Under M2 card §8, the GC-2b decision for Striker and Aegis may go to the operator now.)* It also waits for the owner's confirmation of the fresh-position precondition (§4).
  - **X-3:** runs only as part of the operator's residual-risk decision. CS-note left every M question and every element (a)–(e) OPEN, and S is CONFLICTING (CS-note lines 8–32). It also waits for the owner's confirmation of the fresh-position precondition (§4).
- **Excluded:** X-5, C-b rows and the GC-5 takeover composite (§6).

---

## 0. Rules for every session under this packet

| Rule | Source |
|---|---|
| The operator performs every platform and API action, reads included. No agent places, amends or cancels an order, reads the account or contacts a vendor | [AGENTS.md](../../AGENTS.md) live-execution posture; drill plan Authority table (lines 63–71) |
| The c1 rail stays **disarmed** (`dry_run=true`) and daemon emission stays **off** (`emit_enabled=false`) throughout. The operator confirms both on the host before each session (§2.1) | AGENTS.md; drill plan line 69 |
| **One row at a time.** A row's traces return to the coordinator and are **reviewed before the next row is authorized**. No CP-3 is requested for a row until the previous row's review is recorded | H2 card, "Session rule"; addendum §4 CP-3 (line 491) |
| One micro contract per request and **one in total**. Every entry carries its protective stop in the same request. No `atm*` fields, `cancel_after`, copier or multi-account routing | Drill plan §2.0 (lines 200–201) |
| No manufactured lost response or transport failure. **No request is resent after an unknown outcome** | Drill plan line 70 |
| No automatic fallback to the live evaluation account. The environment is named per row at CP-3 | R-CLOSE; drill plan §0.3 (lines 144–150) |
| A drill (Stage 1, order-producing) session does not start while any operator-placed trade (for example the weekly preservation trade) is open or working on the account. Stage 0's R-1 session is not a drill session: it reads the preservation trade in its own session (§2.5) | Drill plan §0.1 (line 133); §A11.3 |
| **Evidence labels.** Every commissioning result is labelled `COMMISSIONING_OBSERVATION` and states its scope: behavior, interface, environment and date. After review it may support capability acceptance for that scope only. It is never production E1/n3, portfolio admission or whole-route acceptance | Addendum §2 (lines 451–459) |
| A finding that would change intended behavior goes to its owner decision before CP-6 | Addendum §5 (lines 499–506) |

**§A11.2 in a disarmed commissioning session (packet reading, for coordinator and operator confirmation).** §A11.2 says an incident "ends automated trading for that session. Continue operator recovery and evidence collection; review before another session." In these sessions the runtime is disarmed from start to finish, so there is no automated trading for the ruling to end. The drill plan's own recovery step 5 already says "Run no further row that session" (line 206). This packet applies both as follows. An **incident** is any stop condition (§3.3) or any row abort or fault outcome. It ends that session's commissioning activity:
1. **Stop further rows.** Send no further REST order request of any kind (`orders/place`, `change`, `cancel`, `close`). There is no retry and no resend, and no other row runs that session, even one already authorized.
2. **Recover.** Run the five-step recovery (§3.4) to completion. Read-only REST reads and the attended platform flatten or cancel that recovery calls for are part of recovery, not new rows.
3. **Return traces.** Collect and hash the evidence (§3.5) and return the manifest hash and outcome lines.
4. **Review first.** The coordinator records a review before any further CP-3 is requested or another session starts. The rail stays disarmed, and nothing is armed or resumed.

§A11.2 excludes "ordinary, correctly handled signal or capacity refusals". By the same logic, a refusal that is a row's **designed** outcome (X-2's rejected modify) is not an incident. An unexpected refusal, or any effect that cannot be explained, **ends testing** (session plan §2 stop rule, line 45); this packet treats it as an incident for §A11.2 purposes (packet reading).

**Concurrent owner text.** Handoff H5 step (a) is preparing a dated halt/resume §4 amendment that applies §A11.2 and classifies incidents by the contract's §2 trigger rows. It was not published at this packet's acceptance revision and is not relied on here. This packet's incident reading (any stop condition, abort or fault) is its own and is conservative: it arms nothing and additionally stops further rows. H5's acceptance must reconcile the two (§7).

---

## 1. CP-2 fact list (the operator fills this in; nothing private is written here)

Decided once, against this packet (addendum §4 CP-2, line 490). The operator writes **no identifiers, figures, account numbers or billing details** in this table. Anything private goes to the private manifest, and only its SHA-256 appears here.

| # | Fact | Why it is needed | Owner / status today | Operator entry |
|---|---|---|---|---|
| F-1 | **Existing CrossTrade REST entitlement.** The account's existing plan includes REST access. This is vendor-reported; no purchase or plan change is authorized | Condition of R-1 and R-2 (R-CLOSE). Needed before **any** REST call, reads included (drill plan §0.2, line 139) | Drill plan ruling block. Proposed recording procedure at line 40 (step id `P-1-entitlement`). Record today: "none yet" (line 42). The drill plan leaves OPEN whether the reads wait for the coordinator's dated line or only for the confirmation | ☐ confirmed · date ____ · manifest SHA-256 ____ · ☐ reads wait for the dated line ☐ confirmation alone suffices |
| F-2 | **Sim/demo availability.** Does a non-funded environment exist with the same route semantics: the same REST calls reaching the same Tradovate behavior, seen through the same reads? | Each row's environment (§0.3). A trace elsewhere counts for the eval only under an accepted equivalence argument | Drill plan open question 1, **OPEN**. *Context:* CrossTrade describes prop-firm eval accounts as running on Tradovate's **Demo** environment, with documented Demo/Live differences (CS-note F12, line 111). That is not a separate sandbox, and exposure on the eval counts against its drawdown rules (drill plan line 148) | ☐ exists: ____ (no identifiers) ☐ none known ☐ unknown |
| F-3 | **Known-order definition and each read's transaction identity.** Is the drill plan's Part 1 definition (line 156) confirmed? Which transaction is the target of R-1, R-2 and T07 R1–R3? | Precondition (2) of R-1 and R-2 (lines 164, 179). §A11.3 requires "Entitlement and transaction identity" to be confirmed | Definition **OPEN**, partly resolved by §A11.3: an operator-placed preservation trade may be the known order where it qualifies (drill plan line 34). Each target is confirmed here, one per read (§2.4). **Also returned here:** may R-1 and R-2 target X-1's REST-placed order once X-1 has run? The drill plan's definition (line 156, which predates §A11.3) names it the best source, but §A11.3 and addendum §1.3 (line 443) say R-1 runs only in the session of a preservation trade the operator places anyway, and do not mention X-1's order | ☐ definition confirmed as written ☐ amended (text): ____ · targets: see §2.4 table · X-1's order as an R-1/R-2 target: ☐ yes ☐ no ☐ undecided |
| F-4 | **Do drill costs count against the $700 ceiling?** Does each row's commissions and slippage count against the rail spend ceiling? | The cost-ceiling placeholder on every row card | Drill plan open question 6; session plan §2 "Cost" row (line 40). Ceiling: [rail GO ADR](../adr/2026-07-17-c1-rail-build-account-registration-go.md) (AGENTS.md standing-consequence table). **OPEN** | ☐ counts ☐ does not count ☐ other: ____ |
| F-5 | **Preservation-trade treatment in operation.** Is it handled with automation fenced and reconciliation afterwards, or moved to a symbol outside the book's four? | Exclusivity (GC-7). Reusing preservation trades as read targets (§A11.3) does **not** settle this (§A11.3 Scope, third bullet) | Drill plan open question 9, **OPEN**; §A11 item 4 | ☐ fenced + reconciled ☐ outside the four symbols ☐ still open |
| F-6 | *Also required before any Stage 1 row (not a card item for CP-2, listed so it is not missed):* (a) **venue permission (P-1)** for CrossTrade-mediated automated orders on this eval. A firm-level classification is not enough. (b) The **session plan §2 venue-rules item**: "Operator confirms Tradeify permits evening-session trading on this account type" (session plan line 41). The §2 cost item is F-4 | Drill plan §0.2 (lines 140–142) | OPEN | (a) ☐ confirmed · source SHA-256 ____ · (b) ☐ confirmed ☐ not permitted ☐ unknown |

### 1.1 CP-2 record (2026-09-28)

**Source:** facts supplied to the operator on 2026-09-28 from the operator's CrossTrade account page and the vendors' published pages; **operator rulings 2026-09-28 (in session): the six proposed rulings below were adopted as written.** *(Source, added 2026-09-28: the rulings were adopted in the operator's Codex conversation and relayed to this record; the relayed text matches the table below.)* Nothing private is written here. This record authorizes no read, row or trade by itself: Stage 0 still needs §2.1 and §2.2 on the day, and each read its own preconditions. No agent places a trade.

**Facts.**

| # | Recorded | Status |
|---|---|---|
| F-1 | **REST entitlement confirmed.** The operator's CrossTrade account shows the Pro plan, active; CrossTrade states that Pro includes REST access. No upgrade or purchase | **Confirmed** (vendor-reported). The §2.3 capture (`P-1-entitlement`) is owed; under drill plan line 40 the recording procedure "does not add to the ruling's condition", so it is not a gate on the reads |
| F-2 | **No separate equivalent sandbox verified.** The linked account runs on Tradovate Demo, which is how Tradeify evaluation accounts run; that label does not identify a separate test account. Any other sim would need an accepted equivalence argument | Each order-producing row's environment is therefore the incumbent eval, **explicitly decided at that row's CP-3**; no automatic fallback |
| F-6(b) | **Evening sessions permitted** under Tradeify's published evaluation rule: sessions open 6 p.m. ET Sunday–Thursday, positions closed by 4:45 p.m. ET the following trading day; holiday restrictions apply | Confirmed as reported; a capture of the rule is owed with the first Stage 1 row |
| F-6(a) | ~~**Venue permission for this route: still unconfirmed.**~~ **Answered 2026-09-28 by Tradeify support, in writing, to the operator's question about this CrossTrade-mediated setup: conditional permission.** A personal, low-frequency automated strategy is allowed. A third-party API or router such as CrossTrade is not explicitly prohibited but is not supported, is used at the operator's own risk, and "approval by a third-party provider does not guarantee approval by Tradeify". The conditions are: **ownership** (the strategy is the operator's and not shared with other traders or firms); **exclusive use** (only the operator's own accounts, "not be used across multiple firms"); **not HFT**; **full responsibility** for all activity the automation generates; **no rule circumvention** (not designed to bypass risk controls or exploit platform behavior) | **ANSWERED, CONDITIONAL.** Stage 1 no longer waits on an answer. Each Stage 1 row's CP-3 carries the operator's attestation that the five conditions are met (X-1's CP-3 table). ~~**Open for the operator:** whether "not be used across multiple firms" conflicts with running the same strategies at the other firms of the [four-firm program](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md); a clarifying question to Tradeify may be needed before that program deploys elsewhere.~~ **Operator ruling 2026-09-28 (in session):** no clarification with Tradeify is needed. Portfolios adapted to each firm's rules are treated as distinct strategies for the exclusive-use condition. Any per-firm variant of a locked strategy still follows the edition and pre-registration path ([strategy lifecycle](../methodology/strategy_lifecycle.md)), and the attestation at each CP-3 remains the operator's. The original reply is retained privately under `local_artifacts/route-drills-2026-09/` (step `P-1-venue`), owed |

**Operator rulings (adopted as proposed).**

| # | Ruling |
|---|---|
| F-3a | The entitlement condition applies to the **REST reads only**. T07 uses Tradovate's native report exports. The confirmed entitlement satisfies the condition regardless |
| F-3 | The drill plan's known-order definition is **confirmed**. This week's required preservation trade is **R-1's target, in its own session**; its original ids and timestamps are retained so it can become **R-2's target** after a session reset. An independently approved X-1 order may supply R-1/R-2 evidence when it meets their conditions. **This authorizes no extra trade** |
| T07 target | A **completed** transaction with the required post-rollover timing and a zone-explicit timestamp. No qualifying historical transaction has been verified; if this week's preservation trade meets those conditions, it is reused. The target's transaction identity is still confirmed before the T07 reads run (§2.4) |
| F-4 | Drill commissions and adverse slippage **count against the $700 ceiling**, without double-counting costs already included in recorded losses |
| F-5 | Preservation trades on the book's symbols: **automation fenced, then reconciled.** Moving to another symbol does not remove account-wide effects or establish exclusive control |
| Stage 0 | **Keep this packet's stage split.** Unexpected actors are recorded and eligible reads are allowed; the host-disarm (§2.1) and read-specific preconditions stay. The full actor conditions (§2.2) are required before any order-producing row |

**What this unlocks, and what it does not.**
- **Stage 0** can run in the session of this week's preservation trade (due by 2026-10-02): §2.1 host disarm read, §2.2 inventory, then R-1 on that trade, operator-performed. R-2 on the same trade after a reset. T07 reads once a qualifying completed target is confirmed.
- **Stage 1:** F-6(a) is answered, conditionally (above). Each row still needs its own CP-3, which now includes the operator's attestation of Tradeify's conditions. A-11 (firm-side automatic liquidation) remains a Stage 1 question under GC-7.
- **Owed:** the `P-1-entitlement` capture and its manifest SHA-256 (§2.3 step 4); a capture of the F-6(b) rule; the original Tradeify reply (`P-1-venue`). *(2026-09-28: the public F-6(b) rule is now captured; the other two are still owed. See §1.2.)*

### 1.2 Next attended session: checklist (2026-09-28)

This checklist gathers the steps this packet already requires, in dependency order. It adds no condition and authorizes nothing: preparing the session is not permission to run its reads or place its trade. **CP-2 is not complete:** each read's target binding (§2.4) is still missing. The entitlement capture and the venue reply are owed but gate nothing (§1.1).

**CrossTrade observations, 2026-09-28 (Codex, in the operator's authenticated browser; conversation only, not retained evidence).**
- Membership: Pro, monthly, active.
- One linked Tradovate identity, on Demo. No separate test account.
- The connection was first shown as expired. The operator re-authenticated, and CrossTrade then showed the connection Connected, the same Demo identity linked, and the account active.
- Earlier expired-auth alerts were still visible.

These observations are not an entitlement package, and they do not show that the host is disarmed or that the account is flat. They do show that the link can lapse, so it is checked again on the day (step B1).

**Retained so far** (private, gitignored; hashes only here). Five public pages were captured 2026-09-28 under step `P-1-public`: CrossTrade's API page ("included with every Pro subscription"), CrossTrade's Tradovate linking page (prop-firm accounts link as Demo), Tradovate's native-report article, and Tradeify's permitted-times and trader-guidelines articles (text via browser; plain fetch returned 403). The folder is `route-drills-2026-09/public-2026-09-28/`, `SHA256SUMS` `b8fcdcbd1bbc620d470463297a54a2e0fee9d055a041c8c449397ba60536fdef`. It was written in a worktree. The operator then copied it into the primary checkout's `local_artifacts/route-drills-2026-09/` and appended its five rows to that `MANIFEST.tsv`. There, `sha256sum -c` gives 6/6 OK (2026-09-28). Public pages confirm what the vendor says; they do not show this account's plan.

**A. Before the session (once).**
1. **Entitlement capture (`P-1-entitlement`, §2.3).** The operator captures the CrossTrade account page that shows the plan (Pro) and its status (Active). Before saving, remove or crop the email, name, account and user ids, billing and card details, and the Tradovate username. Save it under `local_artifacts/route-drills-2026-09/entitlement/`, append a `MANIFEST.tsv` row, and give the coordinator the SHA-256 and the §2.3 outcome line. This is owed but does not gate the reads (§1.1 F-1).
2. **Tradeify's reply (`P-1-venue`).** Save the original reply privately under the same root. Nothing in the repository or the local captures holds it today. It does not gate Stage 0.
3. **Bind each read to its target** (§2.4). Write one private binding record per read and give the coordinator its hash only:

| Read | Target | Bound when | Runs with existing evidence? |
|---|---|---|---|
| R-1 | This week's preservation trade, in its own session | In that session, from ids captured there | No; it waits for the trade |
| R-2 | The same trade, after at least one ~17:00 ET reset. The 09-21→09-25 trade qualifies only if the operator confirms its ids were retained in its own session | After the reset, with the retained-id manifest hash and the reset count | **No.** No retained ids for any earlier trade are established |
| T07 R1–R2 | A completed trade filled after the 17:00 ET rollover | After the fill, with its post-rollover time confirmed | **No.** No qualifying earlier trade is verified. This week's trade qualifies only if it fills Mon–Thu after the 18:00 ET reopen |
| T07 R3 | The same trade | Only if a zone-explicit source time exists: (a) a CrossTrade time with an explicit zone, or (b) a scrubbed browser capture, if the coordinator rules (b) admissible | No. If neither exists, R3 does not run |

**B. The session of this week's preservation trade (due by 2026-10-02).** Timing is the operator's choice. A Mon–Thu evening trade after 18:00 ET can serve R-1, R-2 and T07. A Friday-evening trade does not cover this week (§2.5). Positions close by 4:45 PM ET; Tradeify closes any position still open (captured rule).
1. **Link check** *(a practical step drawn from the 2026-09-28 observation; not a packet requirement)*. CrossTrade shows the Tradovate connection Connected and the account linked. This is an operator look at the page, not a REST call. If the link has expired, re-authenticate first. Any read that returns 401, 403 or 409 ends with no inference (§2.6).
2. **Host disarm** (§2.1), read on the host: `dry_run=true` and `emit_enabled=false` (an ordinary disarm also writes `armed_until=null`). Record the time and a capture hash. If either required value cannot be confirmed, the session does not start.
3. **Actor inventory** (§2.2), A-1 to A-13, recorded privately. In the A-9 row, record the preservation trade's platform session. Record the known firm-side close owners (drill plan's candidate table: end-of-session auto-close, drawdown-breach liquidation) against A-11. In Stage 0, an actor outside its required state is recorded and returned, and does not stop the reads (§1.1 Stage 0).
4. **The preservation trade** (placed by the operator because the account requires it; not authorized by this packet). Automation stays fenced and the trade is reconciled afterwards (F-5). **In the same session**, retain the original bytes and a hash for:
   - the order and fill ids;
   - the original timestamps, with their zone;
   - a note of whether the fill came after the 17:00 ET rollover.
5. **R-1**, before the next reset: steps 1 and 3–5 only, because a platform-placed trade has no known `clOrdId` (§2.5 item 3). Reads only.
6. **Flat and reconciled**, confirmed from R-1 steps 1 and 5 (the F-5 reconciliation).

**C. After at least one reset.** R-2 on the same trade, then T07 R1–R2 if the fill was post-rollover, and T07 R3 only with a zone-explicit source. Every read waits for its own binding (A3).

**D. Before X-1 (a separate drill session, never while the preservation trade is open or working).**
- ~~**Decision still open:** whether a non-disableable firm-side liquidation (A-11) blocks Stage 1 under GC-7 (§7).~~ *Decided 2026-09-29 for X-1 only (§2.2 ruling note): an identified mandatory firm control need not be disabled; the rest of this bullet is context.* Tradeify's end-of-session auto-close is published; the published captures give no way to disable it, and this is not verified on this account. Under §2.2, A-11 reading "configured, not disableable" means no Stage 1 session starts until the operator and coordinator decide.
- **Permission:** Tradeify answered conditionally, and the operator ruled no clarification is needed (§1.1 F-6(a)). What remains is the operator's attestation of the five conditions in X-1's CP-3. *Observation from the `P-1-public` capture, not a CP-3 item:* Tradeify's published guideline also says it may require "a live video of you enabling the code on your own PC".
- **X-1's own CP-3** (§4.1): the environment named explicitly (the incumbent eval, F-2); every placeholder fixed, including `tif` and the quote source; the request body recorded privately with its hash; the cost ceiling (F-4); written authorization.
- **On the day:** §3.2 in full. That means host disarm, the full inventory with every actor in its required state, a flat start with nothing working, and no scheduled high-impact release within 15 minutes.
- X-1 and X-4 do not wait on M2. X-2 does: see §4.3.

---

## 2. Stage 0: read-only (before it: CP-2)

Stage 0 places, changes and cancels nothing. **No new trade is authorized.** Two kinds of read run in it, with different gates:
- **R-1 and R-2 are CrossTrade REST reads.** They use the operator's credential against the live account, run under R-CLOSE, and are gated on existing REST entitlement (F-1) and on the known-order confirmation and target identity (F-3) (drill plan lines 164, 179).
- **T07 R1–R3 are Tradovate report exports** (Cash History, Account Balance History; session plan lines 61–63), run under the 2026-09-25 read authorization. They are gated on the target's transaction identity (F-3) and on CP-2 as a whole (addendum §4 CP-2, line 490), **not** on REST entitlement: the session plan's 2026-09-27 row confines the entitlement condition to "the REST reads" (session plan line 21).

§A11.3 rules the target of both kinds.

### 2.1 Host disarm confirmation (every session, before any read or row)

| Check | Required | Operator entry |
|---|---|---|
| Rail config on the host, read by the operator | `dry_run=true`. The ordinary disarm is written as `dry_run=true`, `armed_until=null` (halt/resume §3, line 45 at `521d8f2`) | ☐ confirmed on host · time (ET) ____ |
| Signal daemon | `emit_enabled=false` | ☐ confirmed on host · time (ET) ____ |
| How it was confirmed | Read on the host itself, not assumed from a recorded posture (AGENTS.md: "Confirm actual host state before operational work") | ☐ host read · capture SHA-256 ____ |

A `dry_run` config write "is neither an account fence nor proof of flatness" (halt/resume §1, line 16 at `521d8f2`). This check establishes the **runtime's** required state only. It does not show that the account is quiet; the inventory (§2.2) and the starting-state reads do that. **If either value cannot be confirmed, the session does not start.**

### 2.2 Actor inventory (GC-7; drill plan §0.1 with CR-12; the operator fills in privately)

Repeat this at the start of **every** session: an inventory attests one moment only (drill plan line 135). It is the CAP R5 inventory (drill plan lines 101, 371; CAP line 48). The consequence of an actor outside its required state depends on the stage:
- **Stage 0 (reads only).** The addendum requires the inventory before Stage 0 (§3 broker-route row, "[1] Before stage 0"), so it is completed and recorded. An actor outside its required state is recorded privately and returned; it does not by itself stop the reads. The reads are gated by §2.1 and their own preconditions (drill plan lines 164, 179, which do not include the inventory; §2 intro for T07).
- **Stage 1 (from the first order-producing row).** If any actor is not in its required state, **the session does not start** (drill plan line 101: "Before the first order-producing row of each session … the session ends before it starts"). While C-a is the close candidate, any actor that cannot be disabled means **ROUTE STOPS** (packet GC-7; drill plan line 135). A-10 and A-11 are the rows where that is most likely (packet reading), and it bears first on X-3 (C-a).
- If the coordinator prefers the stricter reading (the Stage 1 rule also gating Stage 0), it is returned as a CP-2 decision (§7).

| # | Actor | Required state | Source | State observed |
|---|---|---|---|---|
| A-1 | Trade Copier with this account as leader or follower | None active | Drill plan line 105; Q11, Q26 | ☐ none ☐ active |
| A-2 | Account Manager **auto-close** | Disabled | CR-12 (drill plan line 61) | ☐ disabled ☐ active |
| A-3 | Account Manager **scheduled or window flatten** | Disabled | CR-12 | ☐ disabled ☐ active |
| A-4 | Account Manager **Block Signals** | Disabled (it can refuse the drill's requests) | CR-12; REST §6.2, Q27 | ☐ disabled ☐ active |
| A-5 | Account Manager **Closing Only** | Disabled (it can refuse the drill's requests) | CR-12 | ☐ disabled ☐ active |
| A-6 | CrossTrade managed layers (ATM strategies, trigger replay) | None active; no `atm*` fields sent | Drill plan line 107 | ☐ none ☐ active |
| A-7 | CrossTrade coverage repair on bracket placements | **Cannot be excluded** by request shape. Record it as a vendor actor. Any OCO pair it places is an unexplained effect and **ends testing** | Drill plan line 108; Gate A A8 | ☐ recorded as vendor actor |
| A-8 | Scheduled or queued work (`cancel_after`, outstanding requests) | None | Drill plan line 109 | ☐ none ☐ present |
| A-9 | Other senders: TradingView alerts to the account's webhook, other API clients, other platforms, manual sessions other than this one | Disabled or closed. **In the R-1 session**, the operator's platform session that places the preservation trade is recorded here as the operator-placed preservation trade (drill plan line 133), not as an uncoordinated sender; its treatment in operation is F-5 (open question 9, OPEN) | Drill plan line 110; halt/resume §1 | ☐ disabled/closed ☐ present · R-1 session: ☐ preservation-trade platform session recorded |
| A-10 | **Tradovate platform timed exit-and-cancel** (#519 candidate) | Not configured, or disabled | Drill plan §0.1 lead-in (line 101) and packet GC-7 ("Every other actor is documented and disabled") as quoted in CR-12 (line 61). Applying that rule to a platform timed exit is this packet's reading of #519's candidate (CS-card line 91, CS22; CS-note F10, line 109) | ☐ not configured ☐ disabled ☐ active ☐ unknown |
| A-11 | **Firm-side Tradovate automatic liquidation** at a threshold or configured time (#519 candidate) | Record whether configured, and whether the operator can disable it. **See the note below** | CS-card line 92 (CT12, CT13); CS-note F10, §3 (c) row (line 162) | ☐ not configured ☐ configured, disableable ☐ configured, not disableable ☐ unknown |
| A-12 | The drill's own REST client, operated by the operator | The **sole permitted REST sender** for the session (drill plan line 111; "sole permitted sender" there, read here as REST sender so that the R-1 session's platform-placed preservation trade, A-9, is not excluded). In Stage 0 it sends reads only | Drill plan lines 111, 127 | ☐ recorded as sole REST sender |
| A-13 | Our runtime (c1 rail, signal daemon) | Disarmed with emission off, per §2.1 | Drill plan line 112 | ☐ per §2.1 |

**Note on A-11 (returned for decision; UNVERIFIED).** A firm's risk settings may not be the operator's to disable. CS-note says exclusive ownership "does not remove a firm-side automatic liquidation, if one is configured" (line 162). Under the drill plan's §0.1 consequence (line 135), an actor that cannot be disabled while C-a is the close candidate means **ROUTE STOPS** (packet GC-7). This packet does not decide whether a firm-side liquidation on a drawdown threshold counts as an uncoordinated actor under GC-7. If A-11 reads "configured, not disableable", no Stage 1 session starts, and the question returns to the operator and coordinator. In Stage 0 it is recorded and returned; the reads are not stopped by it (see the stage split above).

*Operator ruling 2026-09-29 (A-11 exception, X-1 only). Mirror; canonical text is the [B–D packet GC-7 row](2026-09-26-tradeify-bd-decision-packet.md); decision record: [X-1 decision packet §2](2026-09-29-x1-decision-packet.md#2-a-11--gc-7-decision):* identified, non-disableable firm risk liquidation is recorded as an external risk-control actor and need not be disabled **for an X-1 session to start**. All operator-configurable competing senders remain disabled. Any firm-side intervention ends X-1 with no PASS. The ROUTE STOPS consequence for C-a and X-3 is unchanged. This ruling grants no CP-3, row, send or spend.

**Recovery flatten (from #519).** A plain exit order leaves brackets working (CS-card line 94; CS09, CT02). Any attended flatten must therefore also cancel working orders, as drill plan recovery step 2 already requires (§3.4).

### 2.3 Entitlement record

Follow the drill plan's **proposed** recording procedure (line 40); it is not part of the ruling:
1. **Evidence.** Vendor-reported evidence that the **existing** plan includes REST access. Examples: a capture of the plan shown in the operator's CrossTrade account, or a written vendor statement.
2. **What does not count.** A REST call does not count as evidence (drill plan §0.2, line 139: entitlement is confirmed before any REST call). Nor does a purchase or a plan change. Whether the reads wait for this record, or only for the confirmation, is F-1's open choice (drill plan line 40: the procedure "does not add to the ruling's condition").
3. **Storage.** Original bytes go under `local_artifacts/route-drills-2026-09/` in the **primary checkout**, hashed into `MANIFEST.tsv` with step id `P-1-entitlement`. Include no account identifiers, credentials or billing details.
4. **Hand-off.** The operator gives the coordinator the manifest SHA-256 and one outcome line. The coordinator then adds the dated line under the drill plan's "Entitlement confirmation record".
5. **This record is the CP-2 F-1 entry** (§1).

Outcome line: `P-1-entitlement · REST entitlement confirmed (existing plan) · <date> · manifest <SHA-256>`.

### 2.4 Read targets and transaction identity (confirm one per read before it runs)

| Read | Target class allowed | Evidence condition the target must meet | Source | Operator confirms (privately; hash only) |
|---|---|---|---|---|
| **R-2** prior-session lookup by id | A **completed** operator-placed preservation trade (§A11.3), or another known order | Its order id, and caller `clOrdId` if any, were **learned and retained privately with original bytes in the order's own session**. At least one ~17:00 ET reset since that session, with the elapsed interval recorded | Drill plan lines 156, 179; §A11.3 | ☐ target confirmed · retained-id manifest SHA-256 ____ · reset(s) since: ____ |
| **T07 R1** `Date` meaning | A completed preservation trade | A fill **after the 17:00 ET rollover**, so that calendar date and session date differ. Exports cover both dates | Session plan §4 (line 61); addendum §1.3 | ☐ target confirmed · ☐ post-rollover fill |
| **T07 R2** query bounds | Same transaction as R1 | As R1 | Session plan line 62 | ☐ |
| **T07 R3** `Timestamp` offset | Same transaction as R1 | A **zone-explicit** source instant for that transaction exists: (a) a CrossTrade response or alert-history time with an explicit zone; or (b) a browser network capture with session tokens and cookies scrubbed. Whether (b) is admissible is the coordinator's ruling under T07. Repeat once after 2026-11-01 | Session plan line 63 | ☐ source (a) ☐ (b) ☐ none (R3 does not run) |
| **R-1** same-session recipe | **Only** a preservation trade the operator places anyway, observed **in that trade's own session** (before the next ~17:00 ET reset) (§A11.3; addendum §1.3, line 443). *Not covered by §A11.3 or addendum §1.3 as written:* X-1's REST-placed order, which the drill plan's known-order definition (line 156, written before §A11.3) names the best source. Whether R-1 or R-2 may target it is returned as a CP-2 decision (F-3; §7). *(Decided 2026-09-28, §1.1 F-3: an independently approved X-1 order may supply R-1/R-2 evidence when it meets their conditions. That grants no extra trade and no X-1 approval.)* | Its id retained privately, with original bytes, in that session | §A11.3; addendum §1.3 (line 443); drill plan line 164 | ☐ confirmed in session · time (ET) ____ |

**Candidate completed target (UNVERIFIED).** STATE records an operator-attested preservation trade in week 09-21→09-25: a filled MYM market round trip. The capture was shared in session; it shows no date and is not committed ([STATE](../../STATE.md#scheduled-forward-triggers), weekly row). It qualifies as an R-2 or T07 target **only if** the operator confirms two things: that its ids were retained in its own session with original bytes, and, for T07 R1/R2, that it filled after the rollover. Neither is established in the repository.

### 2.5 Stage 0 order of work

1. **Once, before Stage 0 (CP-2):** CP-2 recorded (§1): F-1 through the §2.3 entitlement record (needed for R-1/R-2 only), F-3 with each read's target (§2.4), and the other CP-2 facts. **Then, every session:** §2.1 host disarm → §2.2 inventory (recorded; Stage 0 consequence as in §2.2) → the reads whose gates are met (§2 intro).
2. **Completed-trade reads**, where a target qualifies (§2.4):
   - **R-2**, exactly within the R-2 table (drill plan lines 173–186). Steps in order: lifecycle read by id; status per id for the order and its known children; fills by `orderId`; a control read of working and session orders.
   - **T07 R1–R3**, per session plan §4 (lines 57–63). Collection detail belongs to [H6](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md) (lines 315–351), which owns the settlement collection. This packet only sequences the reads.
3. **R-1, only in the session of a preservation trade the operator places anyway.** R-1 runs exactly within the R-1 table (drill plan lines 158–171):
   - Read steps 1–5 in order: list working and session orders; lifecycle per candidate; children through `ocoId`/`parentId`/`linkedId` plus `ordStatus`; fills by `orderId`; fill-reconciled positions.
   - **Excluded:** the "place again when no order carries the id" step, and every `orders/place`, `change`, `cancelreplace`, `cancel` or `close` call.
   - **Partial coverage.** A preservation trade placed on the platform, not through REST, carries an unknown `clOrdId`, if any. R-1 then covers **steps 1 and 3–5 only**, and the `clOrdId` match waits for a REST-placed order: X-1's (drill plan line 171). Whether R-1 may target X-1's order is F-3's open question (§2.4). *(Decided 2026-09-28, §1.1 F-3.)*
4. After a reset, R-2 may be run on the R-1 target as its known order, under the R-2 table. Repeated R-2 reads of one order at stated intervals are a retention probe, which needs separate authorization for each read (drill plan line 184).

**This week's preservation trade: the natural R-1 opportunity.**
- **Obligation.** At least one operator-placed trade per Mon–Fri week. The current bucket is **2026-09-28 → 2026-10-02, deadline 2026-10-02** (STATE, weekly row). No agent places it, and the rail stays disarmed.
- **Timing.** The session plan (§1, line 29) notes that a Friday-evening trade "belongs to the next week's session and does **not** cover the current week". It also notes that a Monday–Thursday evening trade after the 18:00 ET reopen is a post-rollover transaction. The evening option applies only if the session plan §2 venue-rules item is confirmed ("Tradeify permits evening-session trading on this account type", session plan line 41; F-6(b)), and the trade's timing remains the operator's choice for a trade placed anyway.
- **What one trade can serve** (sequencing arithmetic from those two facts, not a new authorization). One Monday–Thursday evening trade this week could serve as:
  - the week's obligation;
  - the R-1 target in its own session, once F-1 and F-3 are confirmed;
  - after a reset, a completed R-2 target, once F-1 and F-3 are confirmed;
  - a T07 R1–R3 target, once F-3 (its transaction identity) and CP-2 are confirmed and the §2.4 conditions hold. REST entitlement is not a condition of these report exports (§2 intro).
- **Exposure.** The trade is placed because the account requires it, **not** because of this packet. It is **not exposure-free**. It is subject to F-5 (open question 9, OPEN), and **no additional trade is authorized** (§A11.3). No Stage 1 row may run while it is open or working (§0).

### 2.6 Stage 0 stop conditions

- A read returns 401, 403 or 409 (auth, plan, unlinked or ambiguous account): the read ends with **no inference** (drill plan line 163).
- The target's identity cannot be confirmed: that read does not run.
- §2.1 fails: the session does not start. §2.2 in Stage 0: the inventory must be completed and recorded; an actor outside its required state is recorded and returned, and does not by itself stop the reads (§2.2).
- Any unexplained position, order or fill seen by a read: stop, and treat it as an incident (§0). No read result releases a reservation or permits a resend (drill plan line 185).

**Evidence.** Original response bytes, the local request time and the operation name. No credentials or headers. Store them under `local_artifacts/route-drills-2026-09/reads/` (R-1, R-2) and `local_artifacts/t07-reads-2026-09/` (T07), hashed into each `MANIFEST.tsv` (path, SHA-256, capture time UTC, step id) (drill plan line 167; session plan §5). **What each read establishes and does not establish** is in the R-1 and R-2 tables (lines 168–170, 183–185) and CR-11 (line 60). A readable prior-session order is a readability fact about that order only.

**Outcome lines for Stage 0** use the §3.5 format, one per read step and one for the inventory. Behavior rows (proposed; the coordinator records):
- **R-1:** REST §6.11 drill-map row "Same-session REST reconciliation recipe on a known order" (line 341); CAP R3 (REST assessment line 264: "CAP R3 row: POSITIVE RECONCILIATION ONLY on REST; session-scoped recipe").
- **R-2:** drill-map row "Prior-session lifecycle read by id" (line 342); CAP R3 (same line: "cross-session recovery unestablished").
- **§2.2 inventory:** CAP R5 (CAP line 48; drill plan lines 101, 371).
- **T07 R1–R3:** interface "Tradovate report export". The CAP settlement rows are H6's to name; CAP S2 (line 40, report-offset and date mapping) is this packet's proposed reading only.

---

## 3. Stage 1 common frame (applies to every row card in §4)

### 3.1 Environment (named per row at CP-3)

- **Sim or demo,** if F-2 shows one with the same route semantics. A trace there counts for the eval account only under an accepted equivalence argument (drill plan line 147).
- **Otherwise,** an explicit operator decision naming the environment for that row. If the incumbent eval is named, the row uses one micro contract, and its exposure is real and counts against the account's drawdown rules (drill plan line 148).
- There is **no default and no automatic fallback** to the live eval (R-CLOSE).

### 3.2 Preconditions common to every row (checklist)

- ☐ This row's **own CP-3** written authorization, completing the row's authorization block (§4).
- ☐ The previous row's traces returned and their review recorded (§0).
- ☐ CP-2 facts F-1 (entitlement), F-4 (cost treatment) and F-6 (venue permission P-1 and the session plan §2 venue-rules item) recorded.
- ☐ The row's exact request body recorded privately and reviewed (§3.7). *(2026-09-30, X-1: under the accepted derivation-rule CP-3 ([X-1 packet §4](2026-09-29-x1-decision-packet.md#4-request-and-evidence-binding)), CP-3 approves the rule and the tool version first. The bytes are generated afterwards, and their validation and request hashes are recorded at generation and compared before launch. This item is satisfied by that record, not by bytes reviewed before CP-3.)*
- ☐ §2.1 host disarm confirmed **this session**.
- ☐ §2.2 inventory complete **this session**, every row in its required state.
- ☐ Starting state read and recorded: **flat, no working orders, no outstanding requests**, account-wide. No preservation or other operator trade open or working (drill plan line 203; §0.1 line 133).
- ☐ Window: attended throughout, inside the operator-fixed session window, and not within 15 minutes of a scheduled high-impact release (drill plan line 202).
- ☐ Evidence roots ready. Nothing will be captured in any repo, task or chat text.

### 3.3 Stop conditions (every row, every step)

If any of these occurs, stop sending at once and run the §3.4 recovery. It is an incident under §0.

| # | Condition | Required response |
|---|---|---|
| SC-1 | **Any `unknown` outcome** (REST §6.3 class) for any request | **No resend.** Read first: recovery step 2, unknown branch |
| SC-2 | **Stop not `Working` at quantity 1** within the operator-fixed wait after a fill, or the stop `Rejected` or ended while the position is open | Recovery at once |
| SC-3 | **Unexpected position or working order** on any symbol: any position other than the one expected, or a quantity above one | Recovery at once |
| SC-4 | **Competing-actor activity**: any order, fill or position change not sent by the drill's REST client, including a coverage-repair OCO pair | Recovery. Record the actor |
| SC-5 | **Rail not disarmed**: §2.1 cannot be re-confirmed, or the host state changes | Recovery. No further REST order requests |
| SC-6 | **Time limit reached**: the operator-fixed maximum time in market, or the end of the session window | Recovery |
| SC-7 | An identity conflict (more than one `New` for one `clOrdId`), an effect that cannot be explained, a partial outcome, missing capture or uncertain protection | Recovery (session plan §2 stop rule, line 45; drill plan X-1 abort, line 225) |

### 3.4 Recovery (the drill plan's five steps, §2.0 line 206; restated, the drill plan governs)

1. **Stop sending** REST requests.
2. **If any request's outcome is unknown:**
   - First read positions, working orders, and that request's lifecycle and status.
   - Flatten on the platform **only if these fresh reads show exposure that needs it**.
   - Record any such flatten as a **second close owner**, whose race with the in-flight request is unresolved.

   **Otherwise:** flatten and cancel working orders on the symbol through the trading platform. This is attended intervention, not a new REST request. A plain exit leaves brackets working, so cancel them too (§2.2 note).
3. **Confirm** from fresh reads taken after the last action: positions flat, no working orders, and every id involved terminal by lifecycle or status. A flat snapshot alone is insufficient.
4. **Reconcile each request:** it has terminal evidence, or it is retained as outstanding with a named owner.
5. **Record the outcome.** Run no further row that session (§0, §A11.2 reading).

*Added 2026-09-28 (applied in the drill plan's §2.0 addendum too):* every position read in steps 2–3, and for SC-3, is the account-scoped fill-reconciled `GET …/accounts/{account}/positions`. The singular `…/position` and unscoped `…/positions` can show the pre-fill state for tens of seconds after a fill ([§3.7 closure F-c](#c5-findings-that-bear-on-rows-and-reads-other-than-37)), so a flat result from them does not confirm step 3.

### 3.5 Evidence entries (every row)

- **Original bytes** of every response and read, plus the local time recorded immediately before each send. Store them under `local_artifacts/route-drills-2026-09/drills/` in the **primary checkout**, hashed into `MANIFEST.tsv` (drill plan lines 71, 207).
- **Excluded from capture:** credentials, session tokens and account identifiers, including in file names.
- **Repo side:** hashes only. The coordinator receives the manifest SHA-256 and **one outcome line per step**, with no identifiers, figures or P&L.
- **Outcome line (proposed format):**
  `COMMISSIONING_OBSERVATION · <row>.<step> · behavior: <drill-map behavior row; CAP row> · interface: CrossTrade REST <operation> · environment: <as named at CP-3> · date: <YYYY-MM-DD ET> · outcome: <one line> · manifest: <SHA-256>`
- **Recording.** The coordinator records reviewed outcomes in CAP and T08 §7 against the behavior row, with its interface and environment (drill plan line 396; REST §6.11 drill map, lines 333–345). A trace qualifies only the behavior it observed, on the interface and in the environment it exercised.

### 3.6 Operator-fixed placeholders (no figures appear in the repo)

Every row card uses these. The operator fixes each in that row's CP-3 authorization. Figures do not come from private sources and are not written here (drill plan line 201).

`<OP: max stop distance>` · `<OP: take-profit distance, if used>` · `<OP: stop-activation wait after fill>` · `<OP: max time in market>` · `<OP: session window (ET)>` · `<OP: cost ceiling for this row>` · row-specific: `<OP: rejected-modify level>` (X-2), `<OP: resting-entry distance>` and `<OP: cancel buffer>` (X-4).

*Added 2026-09-28:* `<OP: tif for this row>` and `<OP: quote source>` (the reference price for the distance-to-level conversion, [C.2](#c2-the-tradovate-ordersplace-body-ct-pl-ct-ov)), on every row that sends `orders/place`. The time-in-force field is `tif` and its default when omitted is undocumented, so no row may rely on one ([§3.7 closure C.3](#c3-time-in-force--x-12-answered-in-part-and-the-part-that-stays-open)).

### 3.7 Request body (a documentary item, not a private figure)

No owner names the `orders/place` field that selects the entry order type. The REST assessment documents absolute `stopLoss`, optional `takeProfit` and the child ids (Q02, line 105), and marks both a market entry with OSO and a resting stop entry with OSO as supported (line 164), without naming the type fields. The drill plan says of X-4: "The REST return does not name the order-type fields, and none are specified here" (line 272). These are public documentation facts, so they are not an operator placeholder. Before the CP-3 of X-1, X-4, and the opening entries of X-2 and X-3:
- **Documentary step (coordinator, returned for review):** name the `orders/place` fields and non-private values for a market entry and for a resting buy stop entry, each with `stopLoss` (and `takeProfit` where used), from retained vendor documentation, citing quote IDs. UNVERIFIED which retained source carries them.
- **CP-3 field (every row that sends `orders/place`, `change`, `cancel` or `close`):** "exact request body (field names and non-private values) reviewed and recorded privately before send".

Until the documentary step returns, X-1 and X-4 are ready except for this one item.

> **Discharged 2026-09-28 — see [§3.7 closure](#37-closure-2026-09-28--request-shapes-from-the-current-public-crosstrade-documentation).** The step was closed from the current **public** CrossTrade documentation rather than the retained captures (the closure states why, and carries no quote IDs). `orderType` is the entry-type field; `takeProfit` / `stopLoss` are absolute prices; the time-in-force field is `tif`, whose **default when omitted is still undocumented**, so every row now sends it explicitly under a new `<OP: tif for this row>` placeholder. The `change` and `cancel` shapes are named there too. Two residuals stand: the retained-capture cross-check (R-3.7a) and the `tif` default (R-3.7b).

---

## 4. Stage 1 row cards (each needs its own CP-3; in this order)

**Sequencing note (packet reading; operator confirms at CP-3).** In the drill plan's suggested session A (line 211), X-1's open position carries on into X-2 and then X-3. Under the one-row-at-a-time rule, the traces are reviewed between rows, so no position is held across a review. X-2 and X-3 therefore each **open their own fresh X-1-shaped position** as their first steps, under their own CP-3. The drill plan already anticipates this for X-3 ("X-3 later needs a fresh X-1 position", line 211). That opening entry is not a new row. Its trace is also an additional X-1-shaped observation, and X-1's abort rules apply to it.

**Pending owner confirmation.** This departs from the drill plan's preconditions for X-2 ("X-1 passed, and its position is open with the stop `Working`", line 241) and X-3 ("X-1's position is open, with both children `Working`", line 256). It is the one exception named in the Status line, routed to the drill-plan owner as a proposed amendment of lines 241 and 256. X-2 and X-3 are **also READY ON owner confirmation of the fresh-position precondition**. *Packet reading, returned with that amendment:* a failure of the opening entry inside X-2 or X-3 is treated as an X-1 failure, with X-1's full consequence (packet GC-2a, ROUTE STOPS for all legs; drill plan line 226).

### 4.1 X-1: one-contract REST OSO entry with its stop (drill plan §2.1, lines 216–227)

**State:** READY on CP-3, except the §3.7 request-body item (market entry fields). *(2026-09-28: §3.7 discharged, [closure](#37-closure-2026-09-28--request-shapes-from-the-current-public-crosstrade-documentation); the §3.2 checklist, including the CP-2 facts, still applies.)*

**CP-3 authorization block (operator fills in):**

| Field | Entry |
|---|---|
| Environment | ☐ named sim/demo: ____ ☐ incumbent eval, explicitly decided for this row |
| Symbol / quantity | MYM front month, away from roll; **1** per request and in total (drill plan line 200) |
| Stop | Absolute `stopLoss` in the same request; distance ≤ `<OP: max stop distance>` |
| Take-profit | ☐ included at `<OP: take-profit distance>` (so a later X-3 exercises an OCO pair) ☐ omitted |
| Wait / time / window / cost | `<OP: stop-activation wait>` · `<OP: max time in market>` · `<OP: session window>` · `<OP: cost ceiling>` |
| Request body (§3.7) | ☐ exact request body (field names and non-private values) reviewed and recorded privately before send · SHA-256 ____ *(2026-09-30, X-1: the derivation-rule CP-3 governs. The SHA-256 is the request hash recorded at generation, after CP-3, together with the validation hash; see the X-1 packet §4 and §8.)* |
| Venue conditions (F-6(a), added 2026-09-28) | ☐ operator attests Tradeify's five conditions are met (§1.1: ownership, exclusive use, not HFT, full responsibility, no rule circumvention) |
| Written authorization | Date ____ · text reference (private) SHA-256 ____ |

**Preconditions:** §3.2 in full.

**Actions, in order** (drill plan line 221):
1. Read the starting state: positions, working orders, session orders. Confirm flat with nothing working.
2. Assign a **fresh** `clOrdId`, never reused, and record it privately before sending.
3. Record the local time. Send **one** REST `orders/place`: a market entry for one contract with absolute `stopLoss`, and `takeProfit` if authorized.
4. Retain the response: the entry id and the child ids `oso1Id`/`oso2Id`/`osoChildIds` (Q02).
5. Poll status and lifecycle per id, for the entry and the children, until the entry is `Filled` or `Rejected`. REST has no Alert History row, so polling is the only way to see a late reject (Q09; Gate A A7).
6. After the fill, read the children's status and quantity, fills by `orderId`, and positions.
7. **Teardown.** Recovery steps 2 (otherwise branch) to 5: attended platform flatten and cancel, then confirmation reads. No further row runs this session.
8. **Reads on X-1's order (required after terminal teardown under the option (b) ruling; see the 2026-09-30 note below).** *(2026-09-30: under the option (b) ruling ([X-1 packet §2](2026-09-29-x1-decision-packet.md#2-a-11--gc-7-decision)), R-1 on X-1's order is **required**. It runs after terminal teardown and before the next ~17:00 ET reset, and as a read-only reconciliation it is exempt from the no-further-row rule. For X-1 on 2026-09-30 it is **not discharged** (retained evidence and Codex's #572; operator ruling 2026-10-01; X-1 packet §8), so R-1 stays owed *(historical: discharged later on 2026-10-01, see the end of this note)*. 2026-10-01 ruling: option A, read by Joshua after local-Codex acceptance. Start-by rule: start by 16:30 ET or C; started reads run to the ~17:00 gate. If not started by then, for any reason, C (rehome); see the [X-1 packet §8 start-by rule](2026-09-29-x1-decision-packet.md#8-post-execution-record-and-corrections--2026-09-30). **2026-10-01 08:59Z: discharged** for X-1's order, `LOCATED_WITH_CLORDID` ([drill plan R-1 result](2026-09-26-tradeify-route-drill-plan-draft.md#r-1-result-on-x-1s-order--2026-10-01)).)* These are not part of CP-3. The drill plan's known-order definition (line 156, written before §A11.3) and its session A/B sequence (lines 211–212) name X-1's order as the best R-1/R-2 source. §A11.3 and addendum §1.3 (line 443), as written, confine R-1 to the session of a preservation trade the operator places anyway, and do not cover X-1's order. These reads therefore run only if the F-3 decision (§1) admits X-1's order as a target *(Decided 2026-09-28, §1.1 F-3: an independently approved X-1 order may supply R-1/R-2 evidence when it meets their conditions. That grants no extra trade and no X-1 approval)*, and then under R-CLOSE once F-1 and F-3 are confirmed, exactly within the drill plan's tables:
   - **R-1** on X-1's order in the same session, before the ~17:00 ET reset. This is the `clOrdId` match that a platform-placed trade cannot supply (drill plan line 171).
   - **R-2** on the same order after a reset, in a later session (drill plan lines 211–212).
   - Whether they may run in a session that an incident has ended is not settled here; the fresh reads that recovery itself calls for (§3.4) are part of recovery.

**Expected identity:** fresh `clOrdId` → one `orders/place` → entry id and child ids → the entry's fill by `orderId` → stop child `Working` at quantity 1, linked to the entry (line 222).

**Pass / fail / abort:** as drill plan lines 223–225. The row-specific abort: more than one `New` for the `clOrdId` ends testing. That is recorded as GC-6 correlation evidence, not as a GC-2a failure.

**What pass/fail establishes:**

| Outcome | Establishes | Behavior row it is recorded against (coordinator records; mapping as the owners name it) |
|---|---|---|
| Pass | The REST-form trace that §A1's admission precondition needs: single-call creation and first-fill activation at quantity 1, for this symbol, environment and date (lines 220, 226) | REST §6.11 drill map row "§A1: one-contract entry and bracket…" (line 337), REST interface; packet GC-2a; CAP N1 subrows N1-entry/N1-b (proposed; CAP lines 401–403); CAP R2 (proposed, packet reading: original order and fill bytes linked to the attempt and its protection; CAP line 45) |
| Fail | **ROUTE STOPS for all legs** (packet GC-2a). The incident-ADR basis depends on the failure mode (CR-10, line 59) | Same rows |

**Does NOT establish:** the activation-interval distribution or bound (UB-2); behavior on other symbols; late-reject handling unless one occurs (line 227).

### 4.2 X-4: cancel of a resting stop entry ends its Suspended children (drill plan §2.4, lines 265–278)

**State:** READY on CP-3, except the §3.7 request-body item (resting stop entry fields). *(2026-09-28: §3.7 discharged; the §3.2 checklist still applies.)* The drill plan schedules X-4 independently: "in session A after teardown, or on its own" (line 213). *Packet reading, returned for operator and coordinator decision:* whether X-4 still has value after an X-1 fail (ROUTE STOPS for all legs, GC-2a) is an operator decision; no owner bars it.

**CP-3 authorization block:** as X-1, except:
- Symbol: **MNQ** front month, one contract (ORB's leg; line 270).
- `stopLoss` and `takeProfit` both included.
- Entry: a resting **buy stop** above the market at `<OP: resting-entry distance>`, chosen so it will not trigger during the row.
- Levels *(added 2026-09-28; [C.2](#c2-the-tradovate-ordersplace-body-ct-pl-ct-ov) conversion)*: entry level E = R + `<OP: resting-entry distance>`, with R read from `<OP: quote source>`; `stopLoss` = E − the stop distance (≤ `<OP: max stop distance>`); `takeProfit` = E + `<OP: take-profit distance>`. R, its time, E and both bracket levels are recorded before the send. `<OP: resting-entry distance>` must exceed `<OP: cancel buffer>`, or the row-specific abort fires at once.
- Cancel buffer: `<OP: cancel buffer>`.
- Time and cost placeholders as §3.6.
- Request body (§3.7): ☐ exact request body reviewed and recorded privately before send.

**Preconditions:** §3.2 in full.

**Actions, in order** (line 272):
1. Read the starting state.
2. Assign a fresh `clOrdId`.
3. Record the local time. Send one REST `orders/place` for the resting buy stop entry with `stopLoss` and `takeProfit`. The REST return does not name the order-type fields, and none are specified here (drill plan line 272); the body is the one recorded under §3.7. *(2026-09-28: `"orderType": "stop"`, `stopPrice` = the entry level E, `stopLoss` and `takeProfit` anchored on E, explicit `tif`; closure C.2–C.3.)*
4. Read: entry `Working`, children `Suspended`.
5. Record the local time. Send one REST `cancel` of the parent.
6. Read the lifecycle and status of the parent and both children, positions and fills.
7. Confirmation reads (recovery step 3).

**Row-specific abort** (line 275):
- If the market comes within `<OP: cancel buffer>` of the entry level, cancel at once.
- If the entry fills anyway, handle it as X-1: confirm the stop is `Working` at quantity 1 (SC-2), then run recovery. *(Added 2026-09-28:* if the realized stop distance, from the fill price to `stopLoss`, exceeds `<OP: max stop distance>`, recovery runs at once; C.2.)

**Pass / fail:** lines 273–274.

| Outcome | Establishes | Behavior row |
|---|---|---|
| Pass | For this symbol, environment and date: a cancel of a resting stop entry before any fill ended its Suspended children, with no fill and nothing left `Working` or `Suspended` | REST §6.11 drill map row "Cancelling a resting stop entry ends its Suspended children" (line 340), REST interface; packet GC-4; CAP N1-a/N1-cancel (proposed; CAP lines 402, 409); CAP R2 (proposed, packet reading, as X-1) |
| Fail | **OPERATOR DECISION for ORB**, with the alternatives at line 276. Not route-wide. A finding that changes ORB's intended behavior goes to its owner before CP-6 (addendum §5) | Same |

**Does NOT establish:** the expiry variant (it needs its own authorization; line 278). ORB's lifecycle was ruled L1 on 2026-09-27 (§59 Ruling 7); X-4 observes the broker's cancel behavior only (line 277).

### 4.3 X-2: rejected modify leaves the old stop working (drill plan §2.2, lines 229–249)

**State:** **READY ON M2's return**, then CP-3. M2 is a documentary step whose return is a precondition of X-2 (line 231). It needs a coordinator dispatch (authorization table, line 372). **No M2 dispatch or return was found** on this branch or at `8c15f18` (§8). X-2 therefore cannot be requested at CP-3 yet. *(Corrected 2026-09-28: M2 was carded later on 2026-09-27 and is DISPATCH-READY; it has not run. It runs in a primary-checkout session the operator starts ([closure C.6](#c6-m2-x-2s-documentary-precondition-the-exact-remaining-dependency)). The §3.7 item named below is discharged.)* *(Later 2026-09-28: M2 has returned, [#541](https://github.com/Joshua-Asante/first-passage/pull/541) (`DONE_WITH_CONCERNS`), with Q1–Q4 all `OPEN`. The coordinator's review of the return is not yet recorded. No documented read shows a working order's effective price after a refused modify, so an X-2 pass can show the refusal and a `Working` status, but "at its original price" rests on inference. Under M2 card §8, the GC-2b decision for Striker and Aegis may go to the operator now.)* It is **also READY ON owner confirmation of the fresh-position precondition** (§4 sequencing note) and on the §3.7 request-body item for its opening entry.

**CP-3 authorization block:** as X-1, plus `<OP: rejected-modify level>`: a stop level on the wrong side of the market, which the broker should refuse (line 243).

**Preconditions:**
- §3.2 in full.
- ☐ M2 returned and reviewed, each question marked DOCUMENTED, CONFLICTING or OPEN (line 236).
- ☐ X-1 **passed** and its review is recorded.

**Actions, in order:**
1. **Opening position.** X-1 steps 1–6. Every X-1 abort rule applies.
2. Read the stop's lifecycle and status (line 243, step 1).
3. Record the local time. Send **one** REST `change` moving the working stop to `<OP: rejected-modify level>`.
4. Retain the response and read the command report (Q21).
5. Read the stop's lifecycle and status again: state, price, and version if one is exposed.
6. **Teardown.** Recovery steps 2 (otherwise branch) to 5.

**Designed outcome.** A rejected modify is the row's **designed** outcome, not an incident (§0).

**Row-specific abort** (line 246):
- If the modify is **accepted and executes**, the position closes. Record that and run recovery.
- If the `change` outcome is **unknown**, do not retry; run recovery (SC-1).

**Pass / fail:** lines 244–245.

| Outcome | Establishes | Behavior row |
|---|---|---|
| Pass | For this symbol, environment and date: one rejected modify left the old stop `Working` at its original price. It validates what M2 documents and does not establish the mechanism; if M2 leaves the mechanism undocumented, a pass shows only that one attempt did not fail (line 198). It also records whether the command report and lifecycle reads carry broker timestamps or versions that postdate the send (GC-3, line 248) | REST §6.11 drill map row "L2(c)" (line 338), REST interface; packet GC-2b, GC-3; CAP N1-c (proposed; CAP line 404); CAP R4 for the GC-3 record (proposed; GC-3's coherence gap is CAP R4 per the B–D packet line 120 and drill plan line 299) |
| Fail | **OPERATOR DECISION for Striker and Aegis**, with the alternatives at line 247. None is adopted automatically | Same |

**Does NOT establish:** survival after an **unknown** modify; atomicity of an accepted modify; other rejection reasons (line 249).

### 4.4 X-3: full close by broker liquidation (C-a normal case; drill plan §2.3, lines 251–263)

**State:** **ONLY as part of the operator's decision on the residual-risk statement** (CR-3, line 52). #519's M return marks M1–M9 OPEN, S CONFLICTING and elements (a)–(c) OPEN (CS-note lines 8–32; §2.1 lines 121–132 for M and S; §2.2 lines 136–142 for (a)–(e)). CP-3 for X-3 is therefore taken **within** that decision, never on its own. It is **also READY ON owner confirmation of the fresh-position precondition** (§4 sequencing note) and on the §3.7 request-body item for its opening entry. *(2026-09-28: §3.7 is discharged for X-3's opening entry too, closure C.2; the other holds above stand.)*

The residual-risk statement returned for decision is CS-note §3 (lines 146–166). Its choices are listed at line 154:
- accept the residual under named conditions in the §1.1a amendment;
- C-b as a separately decided expression change;
- a different close contract;
- reject the route.

None is automatic. CS-note records the §1.1 first failure condition as **pending** on the vendor question (§5.1), not met (line 154). The operator may choose to send that question before deciding.

**CP-3 authorization block:** as X-1, with **both** `stopLoss` and `takeProfit` included at far-from-market distances. The row is not a race test (line 256). Also record:
- the residual-risk decision reference: date ____;
- ☐ this X-3 authorization is part of it.

**Preconditions:**
- §3.2 in full.
- ☐ M returned (#519, ACCEPTED AS INPUT; CS-card lines 117–121).
- ☐ The residual-risk decision taken, with X-3 authorized as part of it.
- ☐ X-1 **passed** and its review is recorded.
- ☐ Starting state with **no working orders on any other symbol**. That is already required by §3.2.

**Actions, in order:**
1. **Opening position.** X-1 steps 1–6, with both children. Every X-1 abort rule applies.
2. Read positions, working orders, and both children's status (line 258, step 1).
3. Record the local time. Send **one** REST `close` for the symbol, with no `qty` or `percent`.
4. Retain the response. Its fields are undocumented for Tradovate (line 258; CS-note F6, line 105).
5. Read, postdating the send: positions; working orders; lifecycle and status per id for both children; session orders, to identify the liquidation order; fills, including any protective fill.
6. **#519's X-3 read addition** (CS-note §5, line 219; CS-card line 95):
   - Read the **lifecycle of the liquidation order and of both children** after the close.
   - Record **whether their command and report rows carry timestamps**.
   - It costs no extra order action.
7. Confirmation reads (recovery step 3). The session ends.

**Wording (from #519, routed to the packet owner; the owner is not edited here).** The sources document that liquidation cancels **at least all of the contract's working orders**, not only "the OCO children". Tradovate adds that it is "not a guarantee". The documents **conflict** on account-level scope (S, CONFLICTING; CS-note §4.4, line 206; D-1, lines 176–188).

**Row-specific abort** (line 262):
- **Orphan:** cancel it on the platform, then recovery.
- **Reversal:** recovery at once.
- **Rejected with the position open:** no retry; recovery.
- **Unknown outcome:** no retry; recovery's unknown branch. Read first; flatten only if fresh reads show exposure; record any flatten as a second close owner.

**Pass / fail / fault:** lines 259–261.

| Outcome | Establishes | Behavior row |
|---|---|---|
| Pass | One no-race observation of cancel-and-flatten, for this symbol, environment and date. It validates what M documents, bears mainly on §1.1a (d), and bears on (a) for the end state only (line 263). It is **necessary, not sufficient, for L2(d)** (CR-7). A pass qualified by an OPEN coherence limit **cannot discharge GC-3 or (d)** (CR-5). With the read addition, it also gives at most one observation of the order of the children's cancels and the liquidation's fill (CS-note §5, line 216) | REST §6.11 drill map row "L2(d)" (line 339), REST interface; packet GC-1 (C-a), GC-3; CAP N1-d (proposed; CAP line 405); CAP R4 for coherence across reads (proposed; drill plan line 299, element (d): "Account-wide coherence across separate calls (CAP R4; GC-3)") |
| Fail (orphan or reversal) | **A contradicting trace stops C-a** (§A11.1 item 2). ROUTE STOPS for C-a on all four legs' whole-leg exits. Residual-risk acceptance is no longer available for C-a, and any earlier acceptance lapses. The operator may choose C-b (its own expression decision) or reject the route. None is automatic (CR-4; CS-note line 154) | Same |
| Fault (rejected or unknown) | Neither a pass nor, by itself, a route stop. It is fault-case evidence for §1.1a (b) and (e), decided under the packet's §1.1 failure rule (line 261) | Same |

**Does NOT establish** (CS-note §5, lines 217 and 221):
- absence of reversal;
- rollback (M4);
- a partial flatten (impossible at one contract);
- a bound on the interval;
- coherence across reads, unless shown;
- behavior with a second close owner;
- behavior on a flat position (M8);
- the account-level cancellation scope (D-1). X-3 as designed cannot observe it: one symbol, no other working orders;
- behavior in another environment without an accepted equivalence argument.

---

## 5. Operator-sent text (vendor contact is the operator's alone)

### 5.1 #519's draft vendor question (by reference)

The text is CS-note §6 (lines 225–244), addressed to CrossTrade support. Its subject is "Full close (liquidate) behavior on a Tradovate account via the REST close endpoint". It has nine numbered items:
1. order of steps;
2. quantity;
3. failure;
4. partial fills;
5. an already-flat position;
6. scope;
7. identity and overlap;
8. after the close;
9. the REST path.

It closes by asking CrossTrade to say which answers depend on Tradovate.

**Constraints** (line 227):
- No account identifiers.
- Retain the written reply as **original bytes** (Gate A A12); a transcription is not enough.
- Sending needs the operator's own decision; nothing has been sent.

A written answer would be a vendor statement, subject to coordinator acceptance. It is evidence for M1–M9, S (D-1), D-2 and the F1 inference, not a trace (line 244). This packet does not restate the question's wording, so that it does not become a second copy of it.

### 5.2 The one permitted T08 follow-up

The T08 ruling authorized "One question, one follow-up at most", operator-sent, with the answer counting only as retained original bytes and carrying no account identifiers ([T08 §7.8](../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md), line 159). The question was sent on 2026-09-25, and a reply was supplied as a hashed transcription. **Original email bytes are still owed** (T08 §7.9, line 174; Gate A A12).

- **Whether the follow-up has been used: UNVERIFIED.** No use is recorded in the files read.
- **Content.** This packet drafts none.
- **Scope.** Whether #519's close question may be sent as that follow-up, or needs its own decision under R-CLOSE, is the operator's call. This packet does not merge the two.

---

## 6. Excluded from this packet

| Item | Why | Source |
|---|---|---|
| X-5, the protective-fill race drill | DEFERRED by R-CLOSE | Drill plan line 28; §A11.1 item 5 |
| C-b rows | Not planned. They need an operator expression decision and qualification; never automatic | Drill plan line 375; §A11.1 item 3 |
| GC-5 takeover composite (Aegis) | Not planned (CR-8). It waits on an accepted close realization | Drill plan lines 57, 376 |
| Any Aegis/6J trace, multi-contract design, or row wider than one contract | Outside the one-contract limit; separate decisions | Drill plan lines 200, 388–389 |
| Webhook-form D1–D4 | Not treated as cleared; each is an individual decision | Session plan §0 addendum (line 20) |

---

## 7. What this packet does not authorize, and the decisions it returns

**Not granted.** This packet grants no:
- read, row, drill or trade, including any additional preservation trade;
- purchase, new access, route change or order mutation;
- vendor contact;
- spend, or any change to the $700 ceiling;
- account reset;
- gate B, C or D acceptance;
- close-contract amendment, close guarantee or residual-risk acceptance;
- T09 dispatch, qualification S5 release, production qualification, arming, deployment or GO;
- merge.

It does not settle drill plan open questions 1, 3–9 or the known-order definition. It creates no second owner of any drill-plan row. No agent performs any step in it.

**Decisions returned:**

| Checkpoint | Decision | Where |
|---|---|---|
| **CP-2** | Facts F-1 to F-5, plus F-6 (P-1 and the session plan §2 venue-rules item) before Stage 1. Each read's target identity (§2.4). The §2.1 and §2.2 records for each session | §1, §2 |
| **CP-2 (F-3)** | *(Decided 2026-09-28, §1.1 F-3.)* May R-1 and R-2 target X-1's REST-placed order? The drill plan's definition (line 156) predates §A11.3, which with addendum §1.3 (line 443) confines R-1 to a preservation-trade session | §1 F-3, §2.4, §4.1 step 8 |
| **CP-2 (Stage 0 inventory)** | Keep this packet's stage split (Stage 0: inventory recorded and returned; the "session ends before it starts" rule from the first order-producing row, drill plan line 101), or adopt the stricter reading that an actor outside its required state also stops Stage 0 reads | §2.2 |
| **Coordinator (documentary)** | Name the `orders/place` request-body fields for a market entry and a resting stop entry, from retained vendor documentation with quote IDs. **Discharged 2026-09-28 from public documentation** ([closure](#37-closure-2026-09-28--request-shapes-from-the-current-public-crosstrade-documentation)); residuals R-3.7a (retained-capture cross-check) and R-3.7b (`tif` default) remain, neither blocking a CP-3 request | §3.7 |
| **Operator (2026-09-28)** | *(Done: M2 returned 2026-09-28, [#541](https://github.com/Joshua-Asante/first-passage/pull/541), Q1 `OPEN`; the vendor-question and GC-2b decisions below remain the operator's.)* Start the carded M2 in a local session of the primary checkout, on a frozen revision descending from #532's merge `6da1b2b` (M2 card §9). If M2 returns Q1 OPEN or CONFLICTING, whether to send its draft vendor question, and whether that uses the one permitted T08 follow-up | [closure C.6](#c6-m2-x-2s-documentary-precondition-the-exact-remaining-dependency), §4.3, §5.2 |
| **CP-3 (X-1)** | Written authorization with the environment, every §3.6 placeholder fixed and the §3.7 request body recorded | §4.1 |
| **CP-3 (X-4)** | The same, after X-1's traces are reviewed. Whether X-4 still runs after an X-1 fail is an operator decision (packet reading) | §4.2 |
| **CP-3 (X-2)** | *(Later 2026-09-28: M2 returned, [#541](https://github.com/Joshua-Asante/first-passage/pull/541); the coordinator's review is owed.)* The same, after M2 returns, X-1 passes and the owner confirms the fresh-position precondition. **M2 needs a coordinator dispatch first** *(2026-09-28: carded and DISPATCH-READY; it waits on the operator starting the primary-checkout session, C.6)* | §4.3 |
| **Residual-risk decision, with X-3's CP-3 inside it** | Under CR-3, on CS-note §3; also after the owner confirms the fresh-position precondition | §4.4 |
| **Drill-plan owner** | Amend X-2's and X-3's preconditions (lines 241, 256) to a fresh X-1-shaped opening position, or reject; and confirm the packet reading that an opening-entry failure carries X-1's GC-2a consequence | §4 sequencing note |
| Operator | Whether to send #519's vendor question; whether and how to use the T08 follow-up | §5 |
| Operator and coordinator | Whether a non-disableable firm-side liquidation (A-11) blocks Stage 1 sessions under GC-7. *Decided 2026-09-29 for X-1 only; other rows still open* | §2.2 note |
| Coordinator | Confirmed at acceptance (below). Reconcile it with H5's halt/resume §4 amendment when H5 is accepted | §0 |

---

## 8. Verification of this note

Run in `/home/user/first-passage` at `HEAD` `521d8f2` when drafted; the fix round re-ran the items marked below at `HEAD` `c991d2dd` with the working tree as it then stood. All read-only.

- `git log --oneline -1`: showed `521d8f2d docs(tradeify): record 2026-09-27 operator rulings; add H1 acceptance conditions`.
- `sed -n` and `grep -n` over:
  - the handoff set (lines 1–57 and 136–196, plus H6 at lines 315–351);
  - the drill plan (read in full, lines 1–396);
  - the session plan (in full);
  - the incident ADR (§A1, §A6, §A11–§A11.3);
  - the checklist addendum (lines 375–514);
  - REST §6.11 (lines 298–354);
  - the halt/resume contract (in full);
  - STATE (lines 40–100);
  - CAP (lines 37–49 and 396–412);
  - T08 (§7, §7.8, §7.9).
- `git show 8c15f18:docs/notes/2026-09-26-close-semantics-c-a.md` (read in full) and `git show 8c15f18:docs/briefs/handoffs/2026-09-26-close-semantics-c-a.md` (read in full).
- `git ls-tree -r --name-only 8c15f18 docs/briefs/handoffs docs/notes` and `ls docs/briefs/handoffs/`, plus `grep -n "M2"` over the handoff set, the drill plan and the B–D packet. These found **no M2 dispatch card or return**. M2 is referenced only as a precondition.
- `grep -n -i "follow-up"` over T08 and the 2026-09-24 vendor-question draft. These found no drafted T08 follow-up and no record that one was used.
- `git diff --stat HEAD` on the input files: empty at drafting. **Re-run in the fix round (below):** the input files are unchanged between `521d8f2` and the current `HEAD` `c991d2dd` (which changed only `.claude/skills/task-routing/SKILL.md`), but the working tree now carries an uncommitted concurrent H5 amendment to the halt/resume contract (`42 +++++++++++++++++++++-`: a dated top callout, a §4 marker and §4.1). It shifts the lines cited in §2.1; at coordinator acceptance those citations were pinned to `521d8f2`, and the H5 draft is no longer quoted (§0).
- `python3 scripts/check_handoff_authority.py --all`: at drafting, "0 card(s) with an authority block, 0 violation(s)"; re-run in the fix round against the current working tree, "2 card(s) with an authority block, 0 violation(s)", exit 0 (the two cards are other agents' concurrent files). This packet carries no authority block, so the check does not exercise it.
- A local Python check resolved every relative link in this file, and every `#anchor` against the target file's headings (GitHub-style slugs): 0 unresolved (re-run in the fix round: 11 links, 0 unresolved). The full gate suite (`make check`) was **not** run (card instruction), so there is no gate-pass claim.

**Not verified:**
- the host state;
- account configuration, entitlement and sim/demo availability;
- whether the 09-21→09-25 preservation trade's ids were retained;
- whether the T08 follow-up has been used.

These are CP-2 facts or UNVERIFIED items, as marked above.

---

## Review and fix round (2026-09-27)

Each finding was re-checked against its cited source before it was applied. Additional commands run in this round, all read-only: `git log --oneline -1` (now `c991d2dd`) and `git log --oneline 521d8f2..HEAD` (one skill-file commit); `git diff --stat` and `git diff` on the halt/resume contract; `sed -n`/`grep -n` over the drill plan (lines 33–42, 61, 101–142, 156, 164, 171, 179, 184, 211–213, 226, 241, 256, 272, 299), the session plan (lines 20–21, 29, 40–41, 45, 61–63), the addendum (lines 436–495), incident ADR §A11.2–§A11.3, CAP (lines 37–49, 396–412), REST assessment (lines 105, 164, 264, 333–345), the B–D packet (line 120) and the H2/H6 cards; `git show 8c15f18:` of the CS-note (lines 105–142) and CS-card (lines 89–95); `python3 scripts/check_handoff_authority.py --all`; the link check above.

| Finding | Disposition | What changed, and why |
|---|---|---|
| H2-SRC-1 | Applied | Verified: addendum line 443 and §A11.3 confine R-1 to a preservation-trade session; drill plan line 156 predates the ruling. §2.4 no longer cites addendum §1.3 for X-1's order and labels it not covered; §4.1 step 8 is conditional on a new F-3 decision; the "may run after an incident" sentence is removed (recovery's own reads stay part of recovery, §3.4). Returned in §1 F-3 and §7 |
| H2-SRC-2 | Applied | Verified drill plan line 40. §2.3 step 2 reworded to the finding's text; the record is marked as the CP-2 F-1 entry (step 5) |
| H2-SRC-3 | Applied | Verified drill plan line 213 ("or on its own"). The "no row runs" sentence is replaced by a labelled packet reading returned for operator decision (§4.2, §7) |
| H2-SRC-4 | Applied | Verified session plan lines 21, 61–63 and H6 card limits. §2 intro now separates REST reads (F-1, F-3) from T07 report exports (F-3 and CP-2, not REST entitlement); §2.5 conditions changed to match |
| H2-SRC-5 | Applied | Verified: anchors correct at `521d8f2`; H5's uncommitted amendment shifts them to 22 and 51. §2.1 gives both; §8 restated against the current tree, with H5's amendment named as an input that changed after reading |
| H2-SRC-6 | Applied | Verified session plan line 45 ("ends testing") and H5's §4.1 text. §0 now says "ends testing … treats it as an incident (packet reading)"; a concurrent-owner paragraph and a §7 coordinator row return the reconciliation with H5 §4.1 |
| H2-SRC-7 | Applied | Verified CS-note §2.1 at lines 119–132 and §2.2 at lines 134–142. §4.4 citation corrected |
| H2-SRC-8 | Applied | Verified CR-12 (line 61) is scoped to four Account Manager functions and line 101 is §0.1's lead-in. A-10's source cell recited as proposed |
| H2-R1 | Applied | Verified drill plan line 101 ("Before the first order-producing row …"), line 135 (C-a scope), R-1/R-2 preconditions (lines 164, 179) and addendum §3 ("Before stage 0: … actor inventory"). §2.2 now splits the consequence by stage; A-9 records the R-1 session's platform-placed preservation trade (drill plan line 133; F-5 OPEN) rather than the finding's "coordinated operator actor", because §0.1's two coordinated kinds (lines 114–116) are drill sends and attended intervention, not preservation trades; A-12 reads "sole permitted REST sender". Result line and §2.6 updated; the stricter reading is returned as a CP-2 decision (§7) |
| H2-R2 | Applied (second alternative, plus a documentary step) | Verified drill plan line 272 and REST assessment lines 105 and 164: entry-type fields are not named. New §3.7 adds a coordinator documentary step and a mandatory CP-3 request-body field; X-1 and X-4 are labelled ready except that item. The finding's "R25 captures" source was not found in the files read and is not cited |
| H2-R3 | Applied | Verified drill plan lines 241 and 256. The Status line names the one pending exception; X-2 and X-3 are also READY ON owner confirmation; the opening-entry failure consequence is stated as a packet reading returned to the drill-plan owner (§7) rather than as a rule |
| H2-R4 | Applied in part | Its line numbers (22, 51) are correct only for the working tree after H5's amendment; at `521d8f2` the original 16 and 45 point at the quoted text (verified with `git show 521d8f2:`). Both are now given (with H2-SRC-5) |
| H2-R5 | Applied | CAP R-row mappings added, sourced where an owner makes them (R5: drill plan lines 101, 371; R3: REST assessment line 264; R4 for GC-3: B–D packet line 120, drill plan line 299) and labelled packet reading where not (R2 for X-1/X-4; S2 for T07). The finding's "CAP lines 43–47" was corrected to lines 45–48 (R2–R5). Stage 0 outcome lines reuse the §3.5 format; §3.5's format gains a CAP-row field |
| H2-R6 | Applied | §2.5 step 1 now puts CP-2 first (F-1 via the §2.3 record, F-3 with targets), then per-session §2.1 → §2.2 → reads |
| H2-R7 | Applied | Verified drill plan line 142 and session plan line 41. F-6 now carries the venue-rules item as (b); §2.5 conditions the evening option on it and leaves timing to the operator |
| H2-R8 | Applied | Verified drill plan lines 164, 179 (precondition 2) and 184. §4.1 step 8 now requires F-1 and F-3; §2.5 step 4 reworded, with the retention-probe authorization rule |

**Not granted:** this round grants nothing; §7's list stands. No owner document was edited.

---

## Coordinator acceptance (2026-09-27)

**ACCEPTED as the CP-2/CP-3 packet.** Reviewer: the coordinating session. The artifact was the executor draft plus the fix round, which applied all 16 findings of two refute-first reviews. The coordinator read the whole packet and spot-checked drill plan lines 101, 133, 156, 171, 211–213, 241, 256 and 272, and §A11.3.

Coordinator edits at acceptance:
- The paragraph and §7 row that quoted H5's uncommitted halt/resume draft were replaced by a pointer. The halt/resume line anchors are pinned to `521d8f2`. The packet cites no unpublished text.

Dispositions:
- **§A11.2 reading (§0): confirmed.** In a disarmed commissioning session an incident ends that session's commissioning activity: no further rows, recovery completed, traces returned, review before another session. It is stricter than, and consistent with, §A11.2. H5's owner text is reconciled with it when H5 is accepted.
- **Stage 0 inventory split (§2.2): accepted as the default.** The drill plan scopes "the session ends before it starts" to the first order-producing row (line 101). The inventory is still completed and recorded before Stage 0, as the addendum requires. The operator may choose the stricter reading at CP-2.
- **X-1's order as an R-1/R-2 target: returned to the operator at CP-2 (F-3).** §A11.3 does not cover it, and the coordinator does not widen it.
- **Fresh-position sequencing for X-2 and X-3: the coordinator supports the amendment.** One-row-at-a-time review cannot hold X-1's position across a review. The drill-plan owner text is amended when X-2 or X-3 is next prepared for CP-3, not in this packet.

**Coordinator items owed before any CP-3 can be requested:**
1. **§3.7 request body.** Name the `orders/place` entry-type fields and non-private values for a market entry and a resting buy stop entry, citing quote IDs. The retained vendor captures (`local_artifacts/t08-rest-route-assessment-2026-09-25/`, REST §6.1) live only in the operator's primary checkout, so this step runs there: a local session, or the operator. It is documentary; it involves no account access or vendor contact. **DISCHARGED 2026-09-28** from the current public documentation instead, with the substitution and its two residuals stated in the [§3.7 closure](#37-closure-2026-09-28--request-shapes-from-the-current-public-crosstrade-documentation). The retained-capture cross-check (R-3.7a) still runs in the primary checkout, but it no longer blocks a CP-3 request.
2. **M2 dispatch** (for X-2 only). This is a documentary vendor-semantics step (drill plan §2.2, line 231). It is not yet dispatched. **Status 2026-09-28:** carded later on 2026-09-27 and DISPATCH-READY ([M2 card](../briefs/handoffs/2026-09-27-m2-modify-semantics.md); #532 merged at `6da1b2b`). Not executed and no return. It reads the retained captures in place, so it runs only in a local session of the primary checkout, which the operator starts (card §0.5, §9). The public-page findings relevant to it are in [§3.7 closure C.6](#c6-m2-x-2s-documentary-precondition-the-exact-remaining-dependency); they do not replace it.

**Ready for the operator now: CP-2.** *(Recorded 2026-09-28 in [§1.1](#11-cp-2-record-2026-09-28).)* The facts F-1 to F-5 and F-6 (§1); each read's target identity (§2.4); the F-3 decision on X-1's order; and the optional stricter Stage 0 reading. Once F-1 and F-3 are recorded, this week's required preservation trade (due 2026-10-02) can also serve as the R-1 target in its own session. No additional trade is authorized.

**Post-publication corrections (2026-09-27, from the cross-handoff critic).** They govern over the packet text above.
- **X-07, entitlement for T07.** §A11.3's words are "after entitlement and target confirmation" for "the authorized reads", with no restriction to REST. The session-plan row this packet relied on carried a coordinator parenthetical, "(for the REST reads)", which is not in the ruling; it has been corrected. **New CP-2 item F-3a:** does the entitlement condition apply to the T07 report exports, or only to the REST reads? **Until it is answered, T07 R1–R3 are gated on F-1 as well.** This supersedes §2 intro's "**not** on REST entitlement", §2.5's matching condition, and §2.4.
- **X-13, one scope question for the $700 ceiling.** F-4 becomes the single consolidated question for the rail GO ADR's owner: which spend classes count against the $700 ceiling? That covers drill commissions and slippage (here), production-host spend (H7) and feed deposits and fees (H8). Asked once at CP-2 and cited by all three.
- **X-12, broker day-order expiry.** Under ORB's L1 lifecycle (§59 Ruling 7(a)) the base entry rests for hours, so the route's default time-in-force matters. The coordinator assigns it here:
  - the §3.7 documentary step also names the `orders/place` time-in-force field and its default, from the same retained vendor captures;
  - X-4's step 4 read records the resting entry's time-in-force.

  The allocation map's C08 "Day-order expiry: `UNVERIFIED`" is answered by those two items.
- **X-08, verification.** The coordinator's acceptance commit (`74788a0`) ran the full gate suite in a clean worktree at that commit, with no other drafts present: `status: completed`, exit 0, `source_stable: true`. The same run also covered `check_handoff_authority.py --all`. The fix-round rows H2-SRC-5 and H2-R4 are superseded by the acceptance edit that pinned the halt/resume anchors to `521d8f2`.

**Not granted:** the packet's own list (§7) stands. Acceptance authorizes no read, row, trade, vendor contact or spend.

---

## §3.7 closure (2026-09-28) — request shapes from the current public CrossTrade documentation

**Status: the §3.7 documentary item is CLOSED for X-1, X-4 and the opening entries of X-2 and X-3, with two named residuals** (the `tif` default, and the retained-capture cross-check). This closes coordinator owed item 1 under "Coordinator items owed before any CP-3 can be requested" and the X-12 time-in-force assignment. It **authorizes nothing**: §7's list stands, no CP-3 is requested or granted, no request is sent, no account is read and no vendor is contacted.

### C.0 Source substitution, and why

§3.7 as written asked for the fields "from retained vendor documentation, citing quote IDs", and the coordinator acceptance routed that step to the primary checkout because the retained captures (`local_artifacts/t08-rest-route-assessment-2026-09-25/`) live only there. This session is a worktree under the standing no-private-source-read constraint, so it could not read those captures. Under the 2026-09-28 executive direction it closed the item from the **current official public CrossTrade documentation** instead, fetched read-only over HTTPS. That is a documentation read, not vendor contact, not an API call and not an account access.

**Consequence, stated rather than hidden:** the fields below are sourced to dated public pages, not to the retained Gate A captures, so they carry **no quote IDs**. The retained captures and these pages have **not** been diffed. Two things follow:
- **Residual R-3.7a (cross-check, owed to a primary-checkout session or the operator):** confirm that the retained 2026-09-25 captures do not contradict the field structure below. A contradiction is a finding for Gate A, not a defect in the row.
- Where a repo owner already records a fact as `DOCUMENTED` with a quote ID, that owner's citation governs; this section adds the **field-level request shape** the owners did not name, and flags where the public pages now say more.

### C.1 Sources read (2026-09-28 UTC)

Retrieved with `curl` over HTTPS on 2026-09-28. **Preserved 2026-09-28** in the operator's primary checkout under `local_artifacts/route-drills-2026-09/vendor-docs/` (gitignored). The folder holds the original bytes, a `SHA256SUMS`, and a `SOURCES.tsv` listing file, ref, URL, bytes, SHA-256 and capture UTC. Each of the six captures also has a row in `local_artifacts/route-drills-2026-09/MANIFEST.tsv` under step id `P-3.7-docs`. The sixth, `https://crosstrade.io/docs/api/overview` (SHA-256 `8fd7368ba42ad4fc9e94fefc384a50f8d11ee6c2c3e995506ed671f6ef5c3156`), is preserved in the same primary-checkout folder but cited nowhere in this section. The copies were re-hashed against the session originals and match. The session copy under `.cache/tradeify-next-steps/vendor-docs/` dies with the worktree. Nothing from these pages is private; the hashes below pin **what was read**.

| Ref | Page | SHA-256 of retrieved bytes |
|---|---|---|
| **CT-OV** | `https://crosstrade.io/docs/api/tradovate/overview` | `461115ce8d2215b7452312dff53a0bccddf0137ffbf892c2a1c4417320d51658` |
| **CT-PL** | `https://crosstrade.io/docs/api/orders/post-place-order` | `ff2f02d394490ff3a6971313d5d6d64f2ab1620fee3d1b387fdde44904eddb6b` |
| **CT-CH** | `https://crosstrade.io/docs/api/orders/put-change-order` | `0dff1c8806633cb60c82b9792e5a2820ebb87c7dc5a7fae1c3804d60b1b2cb5d` |
| **CT-CX** | `https://crosstrade.io/docs/api/orders/post-cancel-order` | `eb7ce58c6c98c362856dab1d1997c72c002a459c4d2d871c6a8179fb5346c12e` |
| **CT-OT** | `https://crosstrade.io/docs/getting-started/tradovate-guides/tradovate-order-types-and-exits` (retrieval URL; the page declares its canonical URL as `https://crosstrade.io/docs/tradovate/order-types-and-exits`) | `5ed93386d28c9c8a6e199e2b1e80a5e4c124a099c12ae09aa3dd2d7de991ec1c` |

Pages are living documents. A capture is evidence of the page on 2026-09-28, not a vendor commitment.

### C.2 The Tradovate `orders/place` body (CT-PL, CT-OV)

`POST /v1/api/tv/accounts/{account}/orders/place`, `Content-Type: application/json`, `Authorization: Bearer <token>`. `{account}` is the Tradovate account name; it is an **account identifier and never appears in this repository** — it is an operator binding.

Required for every row here: `instrument` (string; continuous `MYM1!`, NT8 `MYM 12-26` or Tradovate `MYMZ6` forms are all accepted), `action` (`buy` or `sell`, lowercase), `qty` (int), `orderType` (string). Enum values are **lowercase** on the Tradovate surface, unlike the NT8 surface's `BUY` / `MARKET` (CT-PL, "Platform nuances").

**The field §3.7 said no owner names — `orderType`** — takes `market`, `limit`, `stop`, `stoplimit`, `mit`, `trailingstop` or `trailingstoplimit` (CT-PL body table). That resolves both rows:

| Row | Entry shape | Type field and its price field |
|---|---|---|
| **X-1**, and the opening entries of X-2 and X-3 | market entry, one contract, bracket attached | `"orderType": "market"`. No `limitPrice`, no `stopPrice` |
| **X-4** | resting **buy stop** entry above the market, one contract, bracket attached | `"orderType": "stop"` with `"stopPrice"` = the entry level E, fixed first from `<OP: resting-entry distance>`; the bracket is then anchored on E (conversion below). `stopPrice` is "Required for stop orders" (CT-OV request-field table) |

**Bracket fields.** `takeProfit` and `stopLoss` are **absolute prices**, both optional, and setting either attaches one native Tradovate OSO; setting both OCO-links the two legs. `REST does not run webhook relative-price preprocessing` (CT-OV), so tick/point offsets that work on the webhook path are **not** available here: every level is an absolute price. **Distance-to-level conversion (binding for every row; corrected 2026-09-28 after the executive review of #540).** CP-3 fixes *distances* (§3.6), and the REST surface serves no quotes (CT-OV: bring your own market data). So the absolute levels are computed immediately before each send from a reference price R read from `<OP: quote source>`, and R, its time and every computed level are recorded before the send. What the bracket is anchored on depends on the entry type:
- **Market entry** (X-1; the opening entries of X-2 and X-3). The bracket is anchored on R, the estimate of the fill: `stopLoss` sits the stop distance from R on the protective side, and `takeProfit` sits the take-profit distance from R on the target side.
- **Resting buy-stop entry** (X-4). First fix the entry level E = R + `<OP: resting-entry distance>`, sent as `stopPrice`. Then anchor the bracket on **E, not R**: `stopLoss` = E − the stop distance and `takeProfit` = E + the take-profit distance. Anchoring on R would widen the intended entry-to-stop distance by the resting distance, and it would put the target below the entry whenever the take-profit distance is smaller than the resting distance.
- **Price grid (a recording rule, not a vendor claim).** Every level is recorded on the contract's price increment. Rounding never makes the entry-to-stop distance exceed `<OP: max stop distance>`.

Bracket prices are fixed at submission and are not recalculated from the fill (CT-PL). So after **any** entry fill (a market entry, or an X-4 entry that fills despite its buffer) the row reads the realized stop distance, from the fill price to `stopLoss`. **If it exceeds `<OP: max stop distance>`, recovery runs**; that is an SC-2-class exposure fault, not a pass. `<OP: quote source>` joins §3.6's placeholders. This confirms, at field level, REST §6.11 Q02 and the drill plan's "absolute `stopLoss`".

**Do not send** (packet allow-list, extending drill plan §2.0's `atm*` / `cancel_after` / copier / multi-account bar; **applied to the drill-plan owner** in its §2.0 addendum 2026-09-28):

| Field | Why it is barred for these rows |
|---|---|
| `atmTargets`, `atmStops`, `atmQtys`, `atmTrail`, `atmTrailTrigger`, `atmTrailOffset`, `atmBreakeven`, `atmBreakevenOffset` | Drill plan §2.0. CT-OT independently notes `atm_*` cannot be combined with `take_profit` / `stop_loss` at all, and an inline ATM placement returns `orderStrategyId` **instead of** `orderId` with no child-order map and no `clOrdId` submitted (CT-OV) — it would destroy the row's identity chain |
| `cancelAfter` | Excluded by incident ADR §A1 (allocation map C08). CT-PL scopes it to "an unfilled **limit** entry" anyway, so it would not reach X-4's stop entry |
| `flattenFirst` | Per CT-PL it flattens the position and cancels working orders on the instrument before entering. That is an unrequested close inside an entry row |
| `requireMarketPosition`, `maxPositions` | Position gates: when unmet, CrossTrade returns a 400 and places nothing (CT-PL), so the row would observe a CrossTrade gate rather than the broker behavior it exists to test |
| `syncStrategy`, `marketPosition`, `prevMarketPosition`, `outOfSync`, `targetQuantity`, `strategyExitBlock` | Strategy Sync. `outOfSync=wait` "withholds this request's entry and returns" (CT-OV) — a silent no-op |
| `maxShow`, `trailOffset`, `pegDifference`, `expireTime` | Iceberg / native trailing / GTD. None is in any row's design; trailing fields are also barred from edition legs (allocation map B06) |
| `text` | Free-form note forwarded to the broker and visible in Tradovate reports (CT-PL, CT-OT). Nothing that could carry an identifier goes in it |

**Identity fields — `orderId` and `clOrdId` are two different fields (CT-OV request-field table).** This is sharper than the packet's current wording:
- `orderId` is an "optional tracking id you choose (up to 64 characters)", remembered by CrossTrade for **seven days** so later `cancel`, `change` and `replace` calls can reference it, **and forwarded as `clOrdId` unless you supply `clOrdId` separately**.
- `clOrdId` is the client order id actually sent to Tradovate (up to 64 characters).
- "Tradovate does not reject a repeated `clOrdId`; it is a label for reconciliation, not an idempotency key" (CT-OV) — the public page now states directly what the repo holds as A1/Q05 and as the standing `order_id` idempotency disproof.

**Binding for every row:** the fresh, never-reused per-attempt id of drill plan step 1 is sent as `orderId`, and `clOrdId` is **not** sent separately, so one value carries both roles and the `clOrdId` that appears in the lifecycle `New` command is the one the operator recorded. The id is chosen so it carries no account identifier. *(If the operator prefers to send both, they must be set to the same value, or the R-1 `clOrdId` match reads an id the operator did not record.)*

**Response.** The dispatcher envelope; a bracketed placement sets `api: "place_with_brackets"` and `response` carries `orderId` (entry) plus `oso1Id` and `oso2Id` "in the order the legs were sent (take-profit, then stop-loss)" and `osoChildIds` as an array (CT-PL, CT-OV). **A single-leg bracket has only `oso1Id`** (CT-OV) — so on a row where the operator omits `takeProfit` (X-1's optional take-profit box, §4.1), the stop child arrives as `oso1Id`, not `oso2Id`. Failure is `{"success": false, "error": "<message>"}`.

### C.3 Time in force — X-12 answered in part, and the part that stays OPEN

The field is **`tif`** on the Tradovate surface (string, optional; CT-PL, CT-CH body tables). Documented values: `day`, `gtc`, `ioc`, `fok`, `gtd` (CT-OT shows IOC/FOK/GTD in the webhook's uppercase form; the lowercase REST casing is inferred from CT-PL's lowercase-enum rule) (`gtd` requires `expireTime` in ISO-8601) (CT-OT "Extra TIFs"; CT-PL `expireTime` row).

**What the public pages establish:**
- The bracket children are **not** governed by the entry's `tif`: "The exits are sent GTC whatever `tif` the entry carries, so they outlive the entry's session" (CT-OT); CT-PL says the same. So a day entry's exits are GTC, and the ORB resting entry's Suspended children would outlive the session even if the entry did not.
- On this account class the deadline machinery is **not** the broker's: "Tradovate's demo environment, which also hosts most prop-firm evaluation accounts, records GTD expirations and scheduled cancels but never executes them. CrossTrade watches those deadlines server-side and cancels the order itself shortly after they pass … On demo accounts the cancel typically lands within half a minute of the deadline" (CT-OT). CT-OT's own hosting split puts "the deadline enforcement that replaces scheduled cancels and GTD on demo and prop-firm accounts" in the **needs-CrossTrade-reachable** column.

**What stays OPEN (residual R-3.7b):** the **default when `tif` is omitted**. CT-OT says only "on Tradovate entries, `tif` is optional entirely"; no page names the resulting time in force. Because ORB's ruled **L1** lifecycle rests the base entry for hours, this is decision-bearing, so:
- **Binding for every row here:** send `tif` **explicitly**. Rows whose entry is designed to rest (X-4) send the value the operator fixes at CP-3; rows whose entry is designed to fill immediately (X-1 and the opening entries of X-2 and X-3) send it too, so no row depends on an unnamed default.
- **New CP-3 placeholder:** `<OP: tif for this row>`, added to §3.6's list for rows that send `orders/place`.
- **X-4's step-4 read** still records the resting entry's observed time in force, as the X-12 assignment requires; it is now a check against a value the operator chose, not a discovery of a default.

**Allocation map C08 ("Day-order expiry: `UNVERIFIED`"):** reduced, not closed. The **field and its accepted values are now documented**, and the demo/prop-firm deadline-enforcement owner is documented; the **default** is not, and no observation exists. C08 should read `DOCUMENTED (field, values, enforcement owner on this account class); default-when-omitted UNVERIFIED; expiry behavior unobserved` — applied to the allocation map in its documentation addendum 2026-09-28.

### C.4 `change` (X-2) and `cancel` (X-4) request shapes

Both rows send an operation whose shape no owner named either.

**`change` — X-2 step 3.** `PUT /v1/api/tv/accounts/{account}/orders/{id}/change` (CT-CH). Three facts that change how the row is written:
1. **`PUT` is canonical**; `POST` on the same path "remains accepted as a backward-compatibility alias" (CT-CH). The row must fix the verb, because a `POST` that silently routes through a compatibility alias is a different observation.
2. **`{id}` accepts the "Tradovate order id or an `orderId` assigned on an earlier place call"** (CT-CH path table) — so the row can address the stop child by its `oso*Id` from the placement response. The `orderId` route is the seven-day memory in C.2.
3. **A partial change is completed server-side from the live order.** "When omitted, CrossTrade reads and restores quantity, order type, the limit and/or stop price required by the final order type, and the trailing offset required by trailing orders" (CT-OV "Mutation safety"; CT-CH "Platform nuances"). **This is a GC-3 finding, not a convenience:** the request the broker receives is composed from a version of the order that *CrossTrade* read, at a moment we do not observe, and that read is not in our evidence chain. It bears directly on §1.1a (d) coherence and on the packet's GC-3 record.

**Body for X-2** — send only the field that changes: `{"stopPrice": <OP: rejected-modify level>}`. `stopPrice` is the field for a stop-market child; `limitPrice` "is applied only to limit and stop-limit orders" (CT-CH). Do not send `qty`, `orderType`, `tif`, `text`, `expireTime`, `maxShow`, `trailOffset` or `pegDifference`. Response: the envelope with `api: "modify_order"` and an **empty `response` object** — so the row's evidence is the lifecycle read (below), not the response body. Failure is `{"success": false, "error": "<message>"}`.

**`cancel` — X-4 step 5.** `POST /v1/api/tv/accounts/{account}/orders/{id}/cancel`, **no body fields; send `{}`** (CT-CX). `{id}` again accepts the broker id or the caller-supplied `orderId`. Response envelope carries `api: "cancel_order"` with an empty `response`. The row cancels the **parent entry** only; the children are addressed by reads, never by a second cancel.

**What is still not documented, and therefore still the reason X-2 and X-4 exist:**
- **X-4 / GC-4.** No page says what becomes of the `Suspended` OSO children when the parent entry is cancelled before any fill. CT-CX is silent; CT-OT describes creation and first-fill activation and stops there. The allocation map's C08 "Fate of Suspended children on cancel: `UNVERIFIED`" **stands unchanged**.
- **X-2 / GC-2b.** No page says whether a rejected `change` leaves the original order `Working` at its original price. CT-CH's Tradovate tab states no rule on which orders can be changed and nothing about a broker refusal; it has only a generic failure envelope. *(Corrected 2026-09-28, [M2 return, PR #541](https://github.com/Joshua-Asante/first-passage/pull/541), D-1: the sentence "Only nonterminal orders can be changed. A terminal order returns an error", cited here earlier as CT-CH's statement, is **NT8-tab** text in both the 2026-09-25 and 2026-09-28 captures.)* **The mechanism is not established from public documentation** — see C.6.

### C.5 Findings that bear on rows and reads other than §3.7

Each is a documentation fact with a named consumer. Their disposition, including those applied to other owners, is in C.7.

| # | Documented fact (source) | Consumer, and what it changes |
|---|---|---|
| F-a | Error table: `401 invalid_bearer`, `401 inactive_subscription`, **`401 api_requires_pro`** ("your plan does not include API access"), **`403 tradovate_not_linked`**, `403 endpoint_not_available`, **`409 account_ambiguous`** ("the account name exists on more than one linked identity"), `400 tradovate_rejected`, `429 rate_limited` / `broker_rate_limited` / `snapshot_refresh_pending` / `egress_limited`, `500 internal_error`, `502 tradovate_session_expired`, `502 tradovate_unavailable`, `503 temporarily_disabled` (CT-OV) | **§2.6 Stage 0 stop conditions.** "A read returns 401, 403 or 409 … the read ends with **no inference**" keeps its rule, and each code now has a named meaning to record. Note that a `401 api_requires_pro` is itself the negative answer to F-1 |
| F-b | "**The REST surface requires the Pro plan.** The webhook `destination=tradovate` route is available on every plan" (CT-OV, Limitations and Prerequisites) | **CP-2 F-1 (entitlement).** The entitlement in question is a **named plan tier**, so the F-1 evidence the operator captures is a plan record, and the failure mode is a specific error string. It remains vendor-reported and is **not** confirmed by a REST call (drill plan §0.2 is unchanged) |
| F-c | "`GET /v1/api/tv/accounts/{account}/positions` derives the live net from the fill stream. `GET /v1/api/tv/positions` and the singular `GET /v1/api/tv/accounts/{account}/position` return Tradovate's raw position rows, **which can report the pre-fill state for tens of seconds after a fill**" (CT-OV, Freshness) | **§3.4 recovery step 2 and step 3, and SC-3.** A recovery decision taken from the singular/raw position read could see a stale flat. Every position read in a row or a recovery uses the account `/positions` (fill-reconciled) form. This is a safety-bearing correction |
| F-d | Orders and fills reads "are live but session-scoped … Both lists reset at the daily close"; `GET /v1/api/tv/fills/history` is "CrossTrade's durable capture of the same fills, written periodically rather than in real time" (CT-OV) | **R-2 (prior-session lookup).** R-2's "fills by `orderId`" step targets a session-scoped endpoint. On a prior-session target it will not answer, and `fills/history` — a CrossTrade capture, not Tradovate's — is the only documented durable source. Routed to the drill-plan owner. It does **not** make cross-session recovery established: CAP R3 stands |
| F-e | `GET .../orders/{id}/lifecycle` is the "order audit trail: order, **version**, commands, and command reports (**with reject reasons**)" (CT-OV read table) | **X-2 step 5** ("state, price, and version if one is exposed") and **GC-3**. A `version` is documented as exposed. It does not by itself establish that a version postdates `prepared_at`; that is still what the trace must show |
| F-f | Coverage repair: CrossTrade "watches every bracketed entry that requested a stop-loss and repairs" uncovered quantity, "**cancelling the remaining entry when a leg completes early**, rebuilding an OCO pair for uncovered quantity, and alerting you either way" (CT-OT) | **A-7** ("cannot be excluded by request shape; record it as a vendor actor"). Confirmed, and one behavior is now named: the repair can **cancel the entry**, not only add orders. At one contract there is no uncovered quantity, so the repair should not fire; if it does, it is SC-4 |
| F-g | Late rejections: Tradovate can accept a placement (2xx with an id) and reject it "at its risk layer about a second later"; "REST and MCP placements have no Alert History row, so a REST integration that needs the outcome synchronously should read `GET .../orders/{id}/status` (or the lifecycle) itself a few seconds after placing" (CT-OV, CT-OT) | **X-1 step 5 / GC-8.** Confirms the poll is the only REST-side detector, and names the common cause (`InvalidPrice`, a price outside the product's exchange bands). **Bears on X-2's design:** if `<OP: rejected-modify level>` is chosen outside the exchange price bands rather than merely on the wrong side of the market, the refusal may arrive as a *late* rejection rather than a synchronous one, which is a different observation. Returned as a CP-3 note for X-2 |
| F-h | "Orders placed manually in the Tradovate app, or from any other platform, never pass through CrossTrade, so Account Manager kill and closing-only locks cannot intercept them … **Account Manager rules evaluate the whole account's broker state, so a rule can still flatten after the fact**" (CT-OV, Limitations) | **§2.2 actors A-2/A-3 and A-9**, and the R-1 session. It is the documented mechanism behind requiring Account Manager auto-close and scheduled flatten to be **disabled**, including in the session where the operator places a preservation trade on the platform |
| F-i | "Tradovate's API does not expose a prop firm's trailing drawdown figure, and CrossTrade has no endpoint that returns one" (CT-OV, Limitations) | **Allocation map / CAP.** Any allocation option that would delegate trailing-drawdown observation to the vendor is documented as unavailable on this interface. Routed, not applied |
| F-j | "`CANCELREPLACE` is owner-fenced and durable … If a cancel or placement outcome is ambiguous, CrossTrade does not resend it and returns `reconciliation_required`" (CT-OV, Mutation safety) | Informational for gate C only. It does **not** change the standing finding that a cancel/replace cannot satisfy L2(c) (B–D packet §1, rail spec L-2). No row in this packet sends `replace` |

### C.6 M2 (X-2's documentary precondition): the exact remaining dependency

M2 is the vendor-semantics step for GC-2b, and X-2 cannot be requested at CP-3 without its return (§4.3). **M2 is carded and DISPATCH-READY** ([M2 card](../briefs/handoffs/2026-09-27-m2-modify-semantics.md), carded 2026-09-27 on the operator's instruction "dispatch the M2", after this packet's §8 inventory at `8c15f18`; its restructure #532 merged at `6da1b2b`). **It has not executed and no return exists** (no `docs/notes/2026-09-27-m2-modify-semantics.md` at this head). *(Later 2026-09-28: M2 has returned, [#541](https://github.com/Joshua-Asante/first-passage/pull/541) (`DONE_WITH_CONCERNS`), with Q1–Q4 all `OPEN`. The coordinator's review of the return is not yet recorded. No documented read shows a working order's effective price after a refused modify, so an X-2 pass can show the refusal and a `Working` status, but "at its original price" rests on inference. Under M2 card §8, the GC-2b decision for Striker and Aegis may go to the operator now.)* This closure neither re-cards nor edits it: its §9 premise check compares the card at the dispatch revision with its own text.

**Why this session did not execute it.** The card reads the retained captures in place (`local_artifacts/t08-rest-route-assessment-2026-09-25/`, `local_artifacts/crosstrade-close-research-2026-09-27/`) and stops if they are missing (card §0.5, §7). This worktree has neither, and runs under a no-private-source-read constraint. So the card runs only where its §0.5 routes it: a local session in the primary checkout, started by the operator on a frozen revision that descends from `6da1b2b`.

**What the public pages add for that executor** (card §3 item 2 permits public retrieval for a named gap; these are inputs, not an M2 return):
- the `change` request shape and verb (C.4), so Q1–Q4 can be asked about the exact REST operation;
- Q1 (rejected modify leaves the old stop `Working`): **no public statement found.** The change surface's Tradovate tab has no rejection sentence at all (the terminal-order sentence cited here earlier is NT8-tab text; corrected 2026-09-28, [M2 return, PR #541](https://github.com/Joshua-Asante/first-passage/pull/541), D-1);
- Q2 and the GC-3 record: the lifecycle read exposes a `version` and command reports with reject reasons (F-e); a late risk-layer rejection pattern is documented for placements (F-g), not stated for `change`;
- Q3 and Q4: no public statement found. The partial-change server-side restore (C.4 item 3) states what the broker **receives**, not what survives a refusal or an unknown outcome, and is itself a new GC-3 gap.

Every M2 classification remains the executor's to make against the retained captures. **The exact remaining dependency is an operator action:** start the carded M2 in the primary checkout. If its return leaves Q1 `OPEN` or `CONFLICTING`, its note carries a draft vendor question (card §6 item 5); whether to send it, and whether it uses the one permitted T08 follow-up (§5.2; **whether that follow-up has been used is UNVERIFIED** at this head), is then the operator's. Declining to ask is viable: X-2's own text governs that case ("a pass shows only that one attempt did not fail", §4.3; drill plan line 198), and the card's §8 lets the GC-2b consequence be put to the operator on the documentary result before any trace.

**One stale premise in the frozen card, noted, not edited:** its §8 lists "the §3.7 request-body item for its opening entry" among X-2's remaining needs. That item is closed by this section; the card is left unchanged to keep its premise check valid.

### C.7 What this closure changes, and what it routes

**Applied in this packet (it is the owner):**
- §3.7's documentary step is discharged as described, with residuals R-3.7a and R-3.7b named.
- The CP-3 request-body field (§3.2, §4.1, §4.2) is now checkable against a concrete shape.
- A new placeholder `<OP: tif for this row>` joins §3.6 for rows that send `orders/place`.
- X-1, X-4 and the opening entries of X-2 and X-3 are **no longer blocked on §3.7**. Their other holds are unchanged: X-1 and X-4 wait on the CP-2 facts, the §3.2 session preconditions and their own CP-3; X-2 waits on M2 (C.6), X-1's pass and the fresh-position confirmation; X-3 waits on the residual-risk decision and the same confirmation.

**Applied in the other owners, 2026-09-28.** The coordinator card of 2026-09-28 grants `governance.author` over the route and allocation documents. The items below were first drafted as routes, then written into their owners as dated addenda. Each is a documentary correction within accepted behavior; none changes an allocation or a row's pass/fail rule.

| Item | Owner | Disposition |
|---|---|---|
| Field allow-list (C.2 "Do not send") | Drill plan §2.0 | **Applied**: §2.0 addendum 2026-09-28 extends the `atm*` / `cancel_after` bar |
| Identity and `tif` bindings (C.2, C.3) | Drill plan §2.0 | **Applied**: same addendum |
| X-4 order-type and `cancel` shape | Drill plan X-4 action 2 | **Applied**: dated inline note |
| R-2's fills step on a prior-session target (F-d) | Drill plan R-2 table | **Applied**: step 3 names `fills/history` and records which endpoint answered |
| Position-read form in recovery and SC-3 (F-c) | Drill plan §2.0; this packet §3.4 | **Applied** in both (safety-bearing) |
| Distance-to-level conversion, including X-4's entry-anchored bracket (C.2; corrected 2026-09-28 after the executive review of #540) | Drill plan §2.0; this packet §4.2 | **Applied**: the "Absolute levels" bullet of the §2.0 addendum, the X-4 action-2 note, and §4.2's Levels line and abort |
| C08 wording (C.3); trailing-drawdown unavailability (F-i); C14; C18 | Allocation map | **Applied**: documentation addendum 2026-09-28 under the coordinator note |
| Partial-change server-side restore (C.4 item 3) | B–D packet GC-3 | **Applied**: B–D packet continuation 2026-09-28 |
| X-2 level selection and late rejection (F-g) | CP-3 for X-2 | Stays a CP-3 note: the level must be chosen for a synchronous refusal, or the row observes something else |
| Retained-capture cross-check (R-3.7a) | Primary-checkout session or operator | Owed; does not block a CP-3 request |

**Not granted by this closure.** No CP-2 or CP-3 decision; no read, row, drill or trade; no additional preservation trade; no vendor contact; no purchase, plan change or new access; no spend; no gate B, C or D acceptance; no close-contract amendment or residual-risk acceptance; no T09 dispatch, S5 release, arming, deployment, GO or merge. §7's list stands in full.

## X-1 decision preparation — 2026-09-29

The [bounded X-1 decision packet](2026-09-29-x1-decision-packet.md) carries the A-11 disposition (accepted 2026-09-29 for X-1 only), the row binding and the remaining operator inputs. It is prepared for decision and grants no CP-3. The drill plan and this packet keep their ownership. R-2's limited closure does not establish cross-session recovery.
