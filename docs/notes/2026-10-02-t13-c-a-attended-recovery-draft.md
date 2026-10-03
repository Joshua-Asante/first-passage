# Draft: attended recovery after a C-a close incident (T13 preparation, register row S-X3) — 2026-10-02

**Status: DRAFT. PROPOSED as T13 owner text.** It discharges nothing until the coordinator accepts it as owner text **and** the owner disposes of the §7 step-3 GAP; together those are S-X3's discharge evidence. It authorizes no drill, read, order action, vendor or firm contact, arm or GO. The operator performs every step. The runtime performs none.

**Traces to.** C-a selection register row **S-X3** ([`docs/notes/2026-09-26-close-semantics-c-a.md`](2026-09-26-close-semantics-c-a.md#addendum-2026-10-02--c-a-selection-register-proposed-for-operator-acceptance) on main, as merged from PR #593 at `550bc74`, §R.4 *Actors and attended recovery*; accepted as written by operator ruling 2026-10-02 (sitting 2)). S-X3 asks for a written procedure for an incident during or after a C-a close, covering:
- quiescence and residual request accounting (§3, §4 below);
- the second-close race against an unresolved liquidation (§6);
- the firm fallback when the platform cannot be used (§7).

S-X3's sources are HR :28; CS :161–167, :302; DP :256; CL :263, :265. This draft is not release row R-5, T13's final acceptance through the actual consumers.

**Base.** Line numbers are on origin/main `bd30646`; register rows are on main (the register as merged at `550bc74`, unchanged on main `1a350ec`). *Citations refreshed 2026-10-02 from PR #593 `8d253c9` and PR #584 `e57bd98` to main (operator ruling 2026-10-02 (sitting 2), A12-D1).* Abbreviations follow the register:
- HR: the [halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md);
- CS: the [close-semantics note](2026-09-26-close-semantics-c-a.md);
- DP: the [drill plan](2026-09-26-tradeify-route-drill-plan-draft.md);
- CL: the [deployment checklist](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md);
- ADR: the [incident ADR](../adr/2026-09-17-bounded-platform-protection-incident-contract.md); §A12 is PROPOSED (on main, as merged from PR #584 at `368f366`);
- REST: the [REST route assessment](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md);
- BAO: [`ops/c1_rail/book_account_owner.py`](../../ops/c1_rail/book_account_owner.py);
- REG: the C-a selection register addendum in CS (on main).

## 1. When this applies

- The first release, after any incident during or after a C-a close. That covers REG §R.3's outcomes O0 and O1 after a restart, O2b, O3 at the own-flat deadline D, O5, O6, O7 and O8, and R-T9's finding (a missing stop on another open leg, or a working order left on the closed symbol).
- The account is HALTED in INTERVENTION. The runtime sends nothing: no close, amend, attach or cancel (HR :24, :49).
- No REST C-a is sent in recovery (CL item 7.2, "Attended incident recovery is excluded"; REG O9). The operator manages exposure on the trading platform, per symbol (CL item 7.2).
- No restart of automation follows in that session (HR :71; ADR §A11.2).

## 2. Preconditions, before any session that could produce one

CL :482 requires this procedure before any session that could produce an unresolved request.

| # | Precondition | Source |
|---|---|---|
| P1 | Platform access and alert channels verified before arming (channels: the [D-MON options packet](2026-10-02-d-mon-channel-options-packet.md)) | HR :57 |
| P2 | The GC-7 inventory is taken at session start. Actors that cannot be disabled are listed with their action times: Tradeify's end-of-session auto-close (4:45 PM ET; 12:59 PM ET on early-close days) and its drawdown-breach auto-liquidation | DP :139, :145–146; REG S-X1 |
| P3 | **Recovery read authority.** The §4 reads use the operator's REST credential, and each read needs written authorization. Proposal: authorize one recovery read set at session GO. Otherwise the platform screen is the only read path, and no original bytes are captured (OQ-2)<br>*Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-2:* one recovery read set is authorized at each session GO. It uses R-1's read operations (positions, working orders, session orders, order status, fills), is read-only and is performed by Joshua. No purchase, new access or order action is included. Each session's GO carries it; this record authorizes no read by itself. | DP :174 |
| P4 | **Firm contact path.** How to reach Tradeify to flatten an evaluation position, its hours, and how it identifies the account. Not documented anywhere<br>*Superseded 2026-10-03 (operator, D-MON-3 follow-up, recorded in #615 RH7/§7 G4):* Joshua flattens an evaluation position **directly on Tradovate himself**; no Tradeify contact question is sent, and the Tradeify contact path is not used. Manual Lockout scope stays assumed username-wide (D-MON-4). **Still open (GAP, owner disposition):** the technical fallback when Tradovate is unavailable, login fails or actions are blocked; S-X3 stays held until the owner disposes of it. *Earlier ruling text, kept as the record:* *Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-3:* Joshua asks Tradeify now, in writing, for the flatten contact path, its hours and how it identifies the account. The same message asks Manual Lockout's scope (username or account). Sending is his act. The reply stays private (hash only). P4 stays undocumented until the reply arrives. | CS :302; DP :149 |
| P5 | The session's own-flat deadline D and the ~17:00 ET order-list reset are known | HR :119; CS :167 (Q22) |

## 3. Step 1 — Quiescence

Purpose: stop every actor that can still change the account, as far as possible, and record what cannot be stopped. Quiescence is **asserted with its basis, never claimed as proven**: no claim that manual action is race-free is allowed without evidence (HR :28).

1. **Confirm the halt.** Read HALTED, INTERVENTION, the generation and the local fence status. A hung sender leaves the fence **unconfirmed**: record that and continue (HR :26).
2. **Do not treat a config write as the fence.** A `dry_run` write "is neither an account fence nor proof of flatness" (HR :24). Disarm comes last (§8).
3. **Provider-side actors** (HR :28). From the session-start inventory, confirm that CrossTrade Account Manager automations, the copier and any scheduled cancels are disabled. Do not turn protective services off blindly (HR :28). CrossTrade's coverage repair may place an OCO pair for uncovered quantity (CS F9, :109; Q8, :293); record it as live unless the inventory shows it disabled.
4. **Firm-side actors that cannot be disabled** (DP :145–146). Record each one's next action time against the current time. If recovery will run past 4:45 PM ET, the firm's auto-close is a second close owner (§6).
5. **Manual (Trader) Lockout** flattens everything, cancels all working orders and blocks trading; once enabled it cannot be cancelled, and its scope (username or account) is unverified (DP :148). It is not a default step. Using it is an operator decision, recorded as a close owner on every account in its scope (OQ-4).
   *Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-4:* Manual (Trader) Lockout is a last resort only, used at the operator's call when exposure is unprotected and normal exits fail. It is recorded as a close owner on every account in its scope. Until Tradeify or Tradovate confirms its scope (D-MON-3), it is assumed to cover every account under the username.
6. **Record** the time, the fence status, each actor with its state, and the basis for each ("inventory at session start", "not disableable"). This is the quiescence record.

## 4. Step 2 — Residual request accounting

Purpose: one ledger of every request that could still take effect. Each entry ends either terminal with evidence, or retained with a named owner (DP :256, step 4). Absence never releases (ADR §A12 F2; closure plan row 3).

**Ledger entries:**
- every runtime request of the session from the attempt journal, including attempts journaled `UNKNOWN` before the send (BAO :1856; REG O0);
- each C-a close, and its liquidation order if it can be identified;
- each leg's bracket children (stop and target), on every symbol;
- provider-side effects (coverage repair) and any firm-side action observed;
- every operator platform action, entered as a claim awaiting outcome evidence (HR :51).

**First reads, before any manual action.** They are fresh, with the local time of each read recorded for the postdating check (DP :254):
1. fill-reconciled positions on all symbols (raw position rows can lag by tens of seconds: CS F11, :111);
2. working orders on all symbols (cancel scope S is treated as account-wide until S-V2 is discharged, and R-T9 stays after it);
3. session orders, to identify the liquidation order, because the close response may carry no order id (Q7, CS :292). Do this before the ~17:00 ET reset, after which the same-session lookup no longer finds it (CS :167);
4. the lifecycle and status of the liquidation order and of each former child;
5. fills by `orderId` for each identified order.

The reads follow R-1's read operations (DP :178–190) under P3's authority. R-1 located one order at one time (DP :208–222). It establishes no uniqueness and nothing about an absent order. Cross-session lookup is UNESTABLISHED (R-2 closure, DP :224–236).

**Classify each entry** as either:
- **terminal**: Filled, Canceled or Rejected by lifecycle or status, with fills reconciled; or
- **retained**: unknown, not terminal, or not identifiable, with its owner named.

A retained request keeps its reservation (ADR §A12 F1(b), PROPOSED; CL item 1). If it outlives the session, the held-request watch starts ([F3 watch draft](2026-10-02-t13-a12-f3-held-request-watch-draft.md)).

## 5. Step 3 — Exposure, by outcome

Act only on what the fresh reads show (DP :256, step 2). Each action is a platform action on one symbol, entered in the ledger as a claim. When more than one leg is exposed, an unprotected leg comes first.

| Outcome (REG §R.3) | Presumed while unresolved | First action |
|---|---|---|
| O5 unknown; O3 at D | Position unreduced, partly reduced, flat or reversed; protection may already be cancelled (ADR §A12 F4, full-close row) | Reads first. If exposure remains, handle the race (§6) |
| O6 partial | A remainder, perhaps unprotected | §6, then flatten the remainder on the platform |
| O7 rejected | The leg is open; its brackets may already be cancelled (M4 OPEN) | If unprotected: flatten, or place protection, on the platform (operator's choice). If protected: hold for the operator's decision. The session is over either way |
| O8 refused | Unchanged if nothing was sent; still an incident | Confirm by reads that position and protection are unchanged |
| O2b already flat | The symbol is flat; an order may still be working (M8 OPEN) | Confirm no working order on the symbol; cancel any survivor on the platform |
| R-T9 cross-symbol | Another open leg has lost its stop | Flatten or re-protect that leg on the platform first: it is open and unprotected |
| Reversal found | An opposite position | Flatten on the platform. A reversal beside an opposite position in the same product group can be a prohibited hedge under Tradeify's rules (DP :147, inference) |
| O0 or O1 after a restart | The close was never sent; exposure and protection are as they were | Confirm protection by reads. Flatten or hold is the operator's choice. No runtime dispatch |

## 6. Step 4 — The second-close race

A platform flatten while a liquidation is unresolved is a second close owner racing it. The race can close twice and reverse the leg (CS (c)(ii), :163; (e), :167). Nothing documented prevents it (DP :256; HR :28).

Proposed order:
1. Never send a second REST C-a (REG O9).
2. If the liquidation order is identified and still working, cancel it on the platform. Then read its status until it is terminal: Canceled, or Filled.
3. Re-read the position. Flatten on the platform only if exposure remains.
4. If the liquidation order cannot be identified, or its cancel stays non-terminal, the race cannot be removed. The operator chooses between flattening now (accepting the reversal risk, then re-reading at once) and waiting while the position is still protected. An unprotected leg weighs toward flattening now. Record the choice and its time (OQ-3).
5. After any flatten, re-read positions, working orders and fills on all symbols. Flatten any reversal, and record the race as a fault-case observation (DP :256).
6. Close per symbol only. The platform's single-instrument exit cancels that instrument's working orders and submits market orders (CS :286, platform help text, not API semantics). An account-wide exit also touches the other legs.

The firm's 4:45 PM ET auto-close and its drawdown liquidation are further close owners. If either acts during recovery, record it in the ledger.

## 7. Step 5 — Firm fallback when the platform cannot be used

**Triggers:** the platform is unavailable; login fails; Tradovate's request limit blocks order actions ("Too Many Requests", until a 60-minute cool-down or a support reset; DP :150); or the account is liquidation-only after a drawdown breach (DP :146).

1. **Tradovate is not a fallback.** Its Emergency Trade Desk does not act on evaluation accounts, and Tradovate Support does not resolve evaluation rejections (CS :302; DP :149).
2. **CrossTrade is not a closing fallback.** REST C-a is excluded in an incident (CL item 7.2).
3. **GAP: technical fallback when Tradovate itself is unavailable, login fails or actions are blocked.** The Tradeify contact path is not used (D-MON-3, superseded 2026-10-03: Joshua flattens directly on Tradovate; #615 RH7, §7 G4/G5). No fallback for a Tradovate outage is defined; **S-X3 stays held** until the owner disposes of this GAP. *Earlier text, kept as the record:* "Contact Tradeify through the P4 path … Contacting Tradeify is a message, so it is the operator's act."
4. **Keep reading** if reads work (read-only collection continues: HR :49). Record every contact and its time.
5. A liquidation-only account still allows exits on the platform (CS :288, platform help text).

## 8. Step 6 — Completion and hand-off

- **Recovery completes only on fresh, coherent evidence:** zero gross positions, no working orders or protective orphans, no unresolved requests, and every location accounted for (HR :51). Cached flatness, empty reads, elapsed time and acknowledgment do not count.
- **Then disarm** through the config owner and read it back (`dry_run=true`, `armed_until=null`), and stay HALTED (HR :53). No restart in the session (HR :71).
- **If any request is still retained,** recovery cannot complete (ADR §A12 F3). The account stays HALTED. The operator still disarms before leaving (HR :57), and the held-request watch takes over ([F3 watch draft](2026-10-02-t13-a12-f3-held-request-watch-draft.md), W1).
- **Evidence:** original bytes of every read, local read times, the quiescence record, the ledger and the claims, kept privately on the drill-evidence pattern (DP :257) and never committed.

## 9. Open questions

- **OQ-1** (coordinator). Accept this as S-X3 owner text, or return changes. Name its home: the T13 attended procedure, or the Track B incident sequence in [ARMING_PROCEDURE](rail_build/ARMING_PROCEDURE.md) :5–13.
- **OQ-2** (operator). Authorize a recovery read set (§4) at session GO, or rely on platform-screen reads with no original bytes.
  *Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-2:* one recovery read set is authorized at each session GO. It uses R-1's read operations (positions, working orders, session orders, order status, fills), is read-only and is performed by Joshua. No purchase, new access or order action is included. Each session's GO carries it; this record authorizes no read by itself.
- **OQ-3** (operator). The §6 step 4 choice when the liquidation cannot be identified. This draft names the factors and sets no default.
- **OQ-4** (operator). Whether Manual Lockout is ever a recovery tool.
  *Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-4:* Manual (Trader) Lockout is a last resort only, used at the operator's call when exposure is unprotected and normal exits fail. It is recorded as a close owner on every account in its scope. Until Tradeify or Tradovate confirms its scope (D-MON-3), it is assumed to cover every account under the username.
- **OQ-5** (operator). Tradeify's contact path (P4). Asking Tradeify is a message the operator sends.
  *Superseded 2026-10-03 (operator, D-MON-3 follow-up, recorded in #615 RH7/§7 G4):* Joshua flattens an evaluation position **directly on Tradovate himself**; no Tradeify contact question is sent, and the Tradeify contact path is not used. Manual Lockout scope stays assumed username-wide (D-MON-4). **Still open (GAP, owner disposition):** the technical fallback when Tradovate is unavailable, login fails or actions are blocked; S-X3 stays held until the owner disposes of it. *Earlier ruling text, kept as the record:* *Ruled, operator ruling 2026-10-02 (sitting 2), D-MON-3:* Joshua asks Tradeify now, in writing, for the flatten contact path, its hours and how it identifies the account. The same message asks Manual Lockout's scope (username or account). Sending is his act. The reply stays private (hash only). P4 stays undocumented until the reply arrives.
- **OQ-6.** §6 step 6 and §7 step 5 rest on platform help text, not on a trace.
