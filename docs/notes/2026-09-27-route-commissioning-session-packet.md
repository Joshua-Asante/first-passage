# Route commissioning session packet: operator-run, automation disarmed (2026-09-27)

**Status:** PREPARED 2026-09-27 for coordinator review and operator checkpoints CP-2 and CP-3. Documentary only. **This packet authorizes nothing.** It places, amends or cancels no order. It does not read the account, contact a vendor, spend, arm or deploy. It sequences the rows of the [route drill plan](2026-09-26-tradeify-route-drill-plan-draft.md), which stays their **owner**. Row IDs, preconditions, pass/fail rules and consequences bind to the drill plan's text; this packet quotes only what the operator needs at the platform. Where this packet and the drill plan differ, the drill plan governs, and the difference is a defect in this packet to report. **One pending exception, named here:** §4's fresh-position sequencing for X-2 and X-3 departs from the drill plan's preconditions ("X-1's position is open", lines 241 and 256). It is routed to the drill-plan owner as a proposed amendment of those two lines, and X-2 and X-3 are not runnable on it until the owner confirms (§4, §7).

**Card:** [H2](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md) (lines 136–196), dispatch revision `521d8f2`. **Sequencing owner:** [checklist addendum 2026-09-27](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step), §0–§5 (lines 375–506). **Executor:** agent subagent (Claude Code, Opus 5.5), writing this one file only.

**Rulings applied** (read at their owners):
- **R-CLOSE (2026-09-26):** R-1/R-2 authorized after existing entitlement is confirmed; no order-producing row authorized; X-5 deferred; no automatic fallback to the live eval. Sources: [incident ADR §A11.1](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a111--operator-ruling-close-direction-2026-09-26) (lines 362–376) and the drill plan's ruling block (lines 16–42).
- **§A11.2 (2026-09-27):** no same-session restart of automation after an incident; review before another session ([incident ADR §A11.2](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27), lines 378–386).
- **§A11.3 (2026-09-27):** preservation-trade evidence as the read target ([incident ADR §A11.3](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a113--operator-ruling-preservation-trade-evidence-as-the-target-of-authorized-reads-2026-09-27), lines 388–399; drill plan lines 33–36).

**Consumed, not redone:** [#519](https://github.com/Joshua-Asante/first-passage/pull/519)'s close-semantics return, read at the pinned head `8c15f18`. It is unmerged. Its note is `8c15f18:docs/notes/2026-09-26-close-semantics-c-a.md` (cited below as **CS-note**). Its card is `8c15f18:docs/briefs/handoffs/2026-09-26-close-semantics-c-a.md` (**CS-card**), whose coordinator review, "ACCEPTED AS INPUT", is at lines 117–127.

**Result.**
- **Stage 0** (read-only; §2) can run once the CP-2 facts in §1 are supplied. It covers the host disarm check, the actor inventory, the entitlement record, the transaction identity of each read's target, R-2 and T07 R1–R3 on a completed preservation trade that qualifies, and R-1 in the session of this week's preservation trade. In Stage 0 the inventory is completed and recorded, but an actor found outside its required state does not by itself stop the reads; the drill plan's "session ends before it starts" rule applies from the first order-producing row (§2.2).
- **Stage 1** (order-producing; §3–§4) has four row cards. Each needs its **own CP-3**, and the rows run in this order:
  - **X-1:** ready on CP-3, except one documentary item: the exact `orders/place` request body for a market entry, which no owner names (§3.7).
  - **X-4:** ready on CP-3, except the same item for a resting stop entry (§3.7; drill plan line 272: "none are specified here").
  - **X-2:** waits for M2's return. No M2 dispatch or return was found; see §4.3. It also waits for the owner's confirmation of the fresh-position precondition (§4).
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
| **R-1** same-session recipe | **Only** a preservation trade the operator places anyway, observed **in that trade's own session** (before the next ~17:00 ET reset) (§A11.3; addendum §1.3, line 443). *Not covered by §A11.3 or addendum §1.3 as written:* X-1's REST-placed order, which the drill plan's known-order definition (line 156, written before §A11.3) names the best source. Whether R-1 or R-2 may target it is returned as a CP-2 decision (F-3; §7) | Its id retained privately, with original bytes, in that session | §A11.3; addendum §1.3 (line 443); drill plan line 164 | ☐ confirmed in session · time (ET) ____ |

**Candidate completed target (UNVERIFIED).** STATE records an operator-attested preservation trade in week 09-21→09-25: a filled MYM market round trip. The capture was shared in session; it shows no date and is not committed ([STATE](../../STATE.md#scheduled-forward-triggers), weekly row). It qualifies as an R-2 or T07 target **only if** the operator confirms two things: that its ids were retained in its own session with original bytes, and, for T07 R1/R2, that it filled after the rollover. Neither is established in the repository.

### 2.5 Stage 0 order of work

1. **Once, before Stage 0 (CP-2):** CP-2 recorded (§1): F-1 through the §2.3 entitlement record (needed for R-1/R-2 only), F-3 with each read's target (§2.4), and the other CP-2 facts. **Then, every session:** §2.1 host disarm → §2.2 inventory (recorded; Stage 0 consequence as in §2.2) → the reads whose gates are met (§2 intro).
2. **Completed-trade reads**, where a target qualifies (§2.4):
   - **R-2**, exactly within the R-2 table (drill plan lines 173–186). Steps in order: lifecycle read by id; status per id for the order and its known children; fills by `orderId`; a control read of working and session orders.
   - **T07 R1–R3**, per session plan §4 (lines 57–63). Collection detail belongs to [H6](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md) (lines 315–351), which owns the settlement collection. This packet only sequences the reads.
3. **R-1, only in the session of a preservation trade the operator places anyway.** R-1 runs exactly within the R-1 table (drill plan lines 158–171):
   - Read steps 1–5 in order: list working and session orders; lifecycle per candidate; children through `ocoId`/`parentId`/`linkedId` plus `ordStatus`; fills by `orderId`; fill-reconciled positions.
   - **Excluded:** the "place again when no order carries the id" step, and every `orders/place`, `change`, `cancelreplace`, `cancel` or `close` call.
   - **Partial coverage.** A preservation trade placed on the platform, not through REST, carries an unknown `clOrdId`, if any. R-1 then covers **steps 1 and 3–5 only**, and the `clOrdId` match waits for a REST-placed order: X-1's (drill plan line 171). Whether R-1 may target X-1's order is F-3's open question (§2.4).
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
- ☐ The row's exact request body recorded privately and reviewed (§3.7).
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

### 3.7 Request body (a documentary item, not a private figure)

No owner names the `orders/place` field that selects the entry order type. The REST assessment documents absolute `stopLoss`, optional `takeProfit` and the child ids (Q02, line 105), and marks both a market entry with OSO and a resting stop entry with OSO as supported (line 164), without naming the type fields. The drill plan says of X-4: "The REST return does not name the order-type fields, and none are specified here" (line 272). These are public documentation facts, so they are not an operator placeholder. Before the CP-3 of X-1, X-4, and the opening entries of X-2 and X-3:
- **Documentary step (coordinator, returned for review):** name the `orders/place` fields and non-private values for a market entry and for a resting buy stop entry, each with `stopLoss` (and `takeProfit` where used), from retained vendor documentation, citing quote IDs. UNVERIFIED which retained source carries them.
- **CP-3 field (every row that sends `orders/place`, `change`, `cancel` or `close`):** "exact request body (field names and non-private values) reviewed and recorded privately before send".

Until the documentary step returns, X-1 and X-4 are ready except for this one item.

---

## 4. Stage 1 row cards (each needs its own CP-3; in this order)

**Sequencing note (packet reading; operator confirms at CP-3).** In the drill plan's suggested session A (line 211), X-1's open position carries on into X-2 and then X-3. Under the one-row-at-a-time rule, the traces are reviewed between rows, so no position is held across a review. X-2 and X-3 therefore each **open their own fresh X-1-shaped position** as their first steps, under their own CP-3. The drill plan already anticipates this for X-3 ("X-3 later needs a fresh X-1 position", line 211). That opening entry is not a new row. Its trace is also an additional X-1-shaped observation, and X-1's abort rules apply to it.

**Pending owner confirmation.** This departs from the drill plan's preconditions for X-2 ("X-1 passed, and its position is open with the stop `Working`", line 241) and X-3 ("X-1's position is open, with both children `Working`", line 256). It is the one exception named in the Status line, routed to the drill-plan owner as a proposed amendment of lines 241 and 256. X-2 and X-3 are **also READY ON owner confirmation of the fresh-position precondition**. *Packet reading, returned with that amendment:* a failure of the opening entry inside X-2 or X-3 is treated as an X-1 failure, with X-1's full consequence (packet GC-2a, ROUTE STOPS for all legs; drill plan line 226).

### 4.1 X-1: one-contract REST OSO entry with its stop (drill plan §2.1, lines 216–227)

**State:** READY on CP-3, except the §3.7 request-body item (market entry fields).

**CP-3 authorization block (operator fills in):**

| Field | Entry |
|---|---|
| Environment | ☐ named sim/demo: ____ ☐ incumbent eval, explicitly decided for this row |
| Symbol / quantity | MYM front month, away from roll; **1** per request and in total (drill plan line 200) |
| Stop | Absolute `stopLoss` in the same request; distance ≤ `<OP: max stop distance>` |
| Take-profit | ☐ included at `<OP: take-profit distance>` (so a later X-3 exercises an OCO pair) ☐ omitted |
| Wait / time / window / cost | `<OP: stop-activation wait>` · `<OP: max time in market>` · `<OP: session window>` · `<OP: cost ceiling>` |
| Request body (§3.7) | ☐ exact request body (field names and non-private values) reviewed and recorded privately before send · SHA-256 ____ |
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
8. **Reads on X-1's order (optional; not yet available).** These are not part of CP-3. The drill plan's known-order definition (line 156, written before §A11.3) and its session A/B sequence (lines 211–212) name X-1's order as the best R-1/R-2 source. §A11.3 and addendum §1.3 (line 443), as written, confine R-1 to the session of a preservation trade the operator places anyway, and do not cover X-1's order. These reads therefore run only if the F-3 decision (§1) admits X-1's order as a target, and then under R-CLOSE once F-1 and F-3 are confirmed, exactly within the drill plan's tables:
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

**State:** READY on CP-3, except the §3.7 request-body item (resting stop entry fields). The drill plan schedules X-4 independently: "in session A after teardown, or on its own" (line 213). *Packet reading, returned for operator and coordinator decision:* whether X-4 still has value after an X-1 fail (ROUTE STOPS for all legs, GC-2a) is an operator decision; no owner bars it.

**CP-3 authorization block:** as X-1, except:
- Symbol: **MNQ** front month, one contract (ORB's leg; line 270).
- `stopLoss` and `takeProfit` both included.
- Entry: a resting **buy stop** above the market at `<OP: resting-entry distance>`, chosen so it will not trigger during the row.
- Cancel buffer: `<OP: cancel buffer>`.
- Time and cost placeholders as §3.6.
- Request body (§3.7): ☐ exact request body reviewed and recorded privately before send.

**Preconditions:** §3.2 in full.

**Actions, in order** (line 272):
1. Read the starting state.
2. Assign a fresh `clOrdId`.
3. Record the local time. Send one REST `orders/place` for the resting buy stop entry with `stopLoss` and `takeProfit`. The REST return does not name the order-type fields, and none are specified here (drill plan line 272); the body is the one recorded under §3.7.
4. Read: entry `Working`, children `Suspended`.
5. Record the local time. Send one REST `cancel` of the parent.
6. Read the lifecycle and status of the parent and both children, positions and fills.
7. Confirmation reads (recovery step 3).

**Row-specific abort** (line 275):
- If the market comes within `<OP: cancel buffer>` of the entry level, cancel at once.
- If the entry fills anyway, handle it as X-1: confirm the stop is `Working` at quantity 1 (SC-2), then run recovery.

**Pass / fail:** lines 273–274.

| Outcome | Establishes | Behavior row |
|---|---|---|
| Pass | For this symbol, environment and date: a cancel of a resting stop entry before any fill ended its Suspended children, with no fill and nothing left `Working` or `Suspended` | REST §6.11 drill map row "Cancelling a resting stop entry ends its Suspended children" (line 340), REST interface; packet GC-4; CAP N1-a/N1-cancel (proposed; CAP lines 402, 409); CAP R2 (proposed, packet reading, as X-1) |
| Fail | **OPERATOR DECISION for ORB**, with the alternatives at line 276. Not route-wide. A finding that changes ORB's intended behavior goes to its owner before CP-6 (addendum §5) | Same |

**Does NOT establish:** the expiry variant (it needs its own authorization; line 278). ORB's lifecycle was ruled L1 on 2026-09-27 (§59 Ruling 6); X-4 observes the broker's cancel behavior only (line 277).

### 4.3 X-2: rejected modify leaves the old stop working (drill plan §2.2, lines 229–249)

**State:** **READY ON M2's return**, then CP-3. M2 is a documentary step whose return is a precondition of X-2 (line 231). It needs a coordinator dispatch (authorization table, line 372). **No M2 dispatch or return was found** on this branch or at `8c15f18` (§8). X-2 therefore cannot be requested at CP-3 yet. It is **also READY ON owner confirmation of the fresh-position precondition** (§4 sequencing note) and on the §3.7 request-body item for its opening entry.

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

**State:** **ONLY as part of the operator's decision on the residual-risk statement** (CR-3, line 52). #519's M return marks M1–M9 OPEN, S CONFLICTING and elements (a)–(c) OPEN (CS-note lines 8–32; §2.1 lines 121–132 for M and S; §2.2 lines 136–142 for (a)–(e)). CP-3 for X-3 is therefore taken **within** that decision, never on its own. It is **also READY ON owner confirmation of the fresh-position precondition** (§4 sequencing note) and on the §3.7 request-body item for its opening entry.

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
| **CP-2 (F-3)** | May R-1 and R-2 target X-1's REST-placed order? The drill plan's definition (line 156) predates §A11.3, which with addendum §1.3 (line 443) confines R-1 to a preservation-trade session | §1 F-3, §2.4, §4.1 step 8 |
| **CP-2 (Stage 0 inventory)** | Keep this packet's stage split (Stage 0: inventory recorded and returned; the "session ends before it starts" rule from the first order-producing row, drill plan line 101), or adopt the stricter reading that an actor outside its required state also stops Stage 0 reads | §2.2 |
| **Coordinator (documentary)** | Name the `orders/place` request-body fields for a market entry and a resting stop entry, from retained vendor documentation with quote IDs | §3.7 |
| **CP-3 (X-1)** | Written authorization with the environment, every §3.6 placeholder fixed and the §3.7 request body recorded | §4.1 |
| **CP-3 (X-4)** | The same, after X-1's traces are reviewed. Whether X-4 still runs after an X-1 fail is an operator decision (packet reading) | §4.2 |
| **CP-3 (X-2)** | The same, after M2 returns, X-1 passes and the owner confirms the fresh-position precondition. **M2 needs a coordinator dispatch first** | §4.3 |
| **Residual-risk decision, with X-3's CP-3 inside it** | Under CR-3, on CS-note §3; also after the owner confirms the fresh-position precondition | §4.4 |
| **Drill-plan owner** | Amend X-2's and X-3's preconditions (lines 241, 256) to a fresh X-1-shaped opening position, or reject; and confirm the packet reading that an opening-entry failure carries X-1's GC-2a consequence | §4 sequencing note |
| Operator | Whether to send #519's vendor question; whether and how to use the T08 follow-up | §5 |
| Operator and coordinator | Whether a non-disableable firm-side liquidation (A-11) blocks Stage 1 sessions under GC-7 | §2.2 note |
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
1. **§3.7 request body.** Name the `orders/place` entry-type fields and non-private values for a market entry and a resting buy stop entry, citing quote IDs. The retained vendor captures (`local_artifacts/t08-rest-route-assessment-2026-09-25/`, REST §6.1) live only in the operator's primary checkout, so this step runs there: a local session, or the operator. It is documentary; it involves no account access or vendor contact.
2. **M2 dispatch** (for X-2 only). This is a documentary vendor-semantics step (drill plan §2.2, line 231). It is not yet dispatched.

**Ready for the operator now: CP-2.** The facts F-1 to F-5 and F-6 (§1); each read's target identity (§2.4); the F-3 decision on X-1's order; and the optional stricter Stage 0 reading. Once F-1 and F-3 are recorded, this week's required preservation trade (due 2026-10-02) can also serve as the R-1 target in its own session. No additional trade is authorized.

**Post-publication corrections (2026-09-27, from the cross-handoff critic).** They govern over the packet text above.
- **X-07, entitlement for T07.** §A11.3's words are "after entitlement and target confirmation" for "the authorized reads", with no restriction to REST. The session-plan row this packet relied on carried a coordinator parenthetical, "(for the REST reads)", which is not in the ruling; it has been corrected. **New CP-2 item F-3a:** does the entitlement condition apply to the T07 report exports, or only to the REST reads? **Until it is answered, T07 R1–R3 are gated on F-1 as well.** This supersedes §2 intro's "**not** on REST entitlement", §2.5's matching condition, and §2.4.
- **X-13, one scope question for the $700 ceiling.** F-4 becomes the single consolidated question for the rail GO ADR's owner: which spend classes count against the $700 ceiling? That covers drill commissions and slippage (here), production-host spend (H7) and feed deposits and fees (H8). Asked once at CP-2 and cited by all three.
- **X-08, verification.** The coordinator's acceptance commit (`74788a0`) ran the full gate suite in a clean worktree at that commit, with no other drafts present: `status: completed`, exit 0, `source_stable: true`. The same run also covered `check_handoff_authority.py --all`. The fix-round rows H2-SRC-5 and H2-R4 are superseded by the acceptance edit that pinned the halt/resume anchors to `521d8f2`.

**Not granted:** the packet's own list (§7) stands. Acceptance authorizes no read, row, trade, vendor contact or spend.
