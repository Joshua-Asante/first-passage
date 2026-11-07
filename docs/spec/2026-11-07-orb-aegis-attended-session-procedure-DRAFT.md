# ORB + Aegis attended session: operator procedure (DRAFT)

**Status:** DRAFT, 2026-11-07. Claude drafts, Joshua accepts or edits. It grants no
GO, order, session or spend. It is the operator's half of the
[eval build design spec](2026-11-06-orb-aegis-eval-build-design.md): the spec says what
the build does, and this page says what the attending operator does. Where they
differ, the accepted spec governs until Joshua rules.

**Why this exists.** On the 11-05 bare-bones path, several safety duties sit with the
operator, not the build: the account loss stop and account-wide incidents (B6),
flattening on an incident (B10), verified flat (B11), the preservation trade (B13),
and the backstop for Aegis's exit, which needs a bar close to fire (B14, D2). Until
now no page has said how the operator carries them out.

**Public/private split.** This page carries no thresholds, times specific to a
strategy, prices or account data. Values marked *(signed page)* are set on Joshua's
private signed page. Journals, exports and screenshots stay in private custody (B15).

## 1. Roles

- **Operator:** Joshua. He enables both instances himself (11-05 path, step 5) and
  stays at the screen until the session ends (§5).
- **Agents and Codex** act on the eval only on his direction (AGENTS.md money control
  1). Codex may see account data on screen while it acts; it writes none of it down.

## 2. The one manual action: F (flatten a leg)

Every incident card below ends in **F**. F applies to a leg that has a position, a
working order or an unresolved request. A leg with none of these only needs disabling.
F runs in this order:

1. **Disable** the leg's instance in NinjaTrader. The strategy's own incident close
   stays in the build (B10). Disabling stops the strategy from sending more orders,
   and it leaves the leg's protective orders working (B8). It does not withdraw a
   close the strategy has already sent, and whether disable stops the incident close
   is not proven: confirm both in S-PAIR, and the signed page names the rest as risk.
   **If NinjaTrader is unavailable** (crashed, frozen or disconnected), skip this step
   and go straight to step 2 in Tradovate web. Do not wait for NinjaTrader.
2. **Flatten and cancel** in the Tradovate web view. Use the action that exits that
   contract's position at market and cancels its working orders. The pre-session check
   confirms which button this is ("flatten path confirmed"). On a leg with no position,
   this cancels its working orders.
3. **Verify** with B11's conditions, not the grids alone. In both views, read after the
   last request: no position and no working orders on that instrument. Every request
   the leg sent has a terminal outcome, and every execution is accounted for. While
   any request is still unresolved, F is not complete. Keep watching, and if a late
   fill opens or reverses a position, repeat step 2 for it.

**F on both legs** runs each step across both legs before the next: disable both
instances, then flatten and cancel both legs, then verify both. Never wait on one
leg's verification while the other instance is still enabled; B6 gives no automation
that would stop it. If NinjaTrader is unavailable, the step 1 bypass applies to both.
The general rule: step 2 covers everything that needs flattening or cancelling,
including exposure on any other instrument (card 5), before any step 3 wait begins.

A leg that has had F is not re-enabled in the same session. Re-enabling is never a
recovery step (B8), and an incident ends automation for that session. If NinjaTrader
restarts, make sure neither instance is enabled from the saved workspace and the
connection is set not to connect on startup before it reconnects
([runbook](https://github.com/Joshua-Asante/first-passage/blob/b7eaff7/docs/notes/2026-10-18-native-protection-recovery-pilot-runbook.md) §3, A11.2).

## 3. Before the session

1. Run the spec's [pre-session check](2026-11-06-orb-aegis-eval-build-design.md#5-attended-pre-session-check)
   (items 1–8).
2. Have these values at hand *(signed page)*:
   - today's trailing floor (highest end-of-day balance minus $3,000; the eval has no
     lock, and Tradeify enforces the floor intraday);
   - the account loss threshold, set above that floor (B6);
   - the protection limit: how long after a fill a leg may go without a broker-reported
     working stop covering its whole open quantity before the operator acts (§4);
   - the freshness limit: how long the Tradovate account view may go without updating
     before the operator treats account evidence as lost (§4, card 8);
   - the operator flatten time, before 16:45 ET (§5, C2).
3. Plan the attended window. It must cover the session from enable until verified
   flat. If it cannot, do not start.

## 4. During the session

| Watch | Where | When it trips | Do |
|---|---|---|---|
| A leg fills | Tradovate web, that contract's orders | The broker-reported working stop quantity is below the leg's whole open quantity (missing or short) for longer than the protection limit (B4; U-3 and U-7 are unproven) | Card 3 |
| Account equity | Tradovate web account view | At or below the account loss threshold (B6) | Card 6 |
| Account evidence | Tradovate web account view | The view stops updating or is unavailable for longer than the freshness limit (runbook §2.4) | Card 8 |
| Connection | NinjaTrader connection-loss alert | Any loss of connection (B7) | Incident card 1 |
| Each instance's state | NinjaTrader strategies tab | An instance halts or reports a fault | Incident cards 2–4 |
| The operator | — | The operator must leave the screen | F on both legs; the session ends |

## 5. Incident cards

| # | Situation | What the operator sees | Do | Session after |
|---|---|---|---|---|
| 1 | Connection lost (NinjaTrader, or the platform crashes or restarts) | Connection-loss alert; positions and orders in Tradovate web may still be live | F on both legs, flattening from Tradovate web (F step 1's bypass if NinjaTrader is down). Do not reconnect to resume: reconnecting never resumes trading (B7). Protection across a disconnect is unproven (U-3), so an open leg is treated as unprotected | Ends for both legs |
| 2 | Rejected or unknown order on a leg (B9) | The instance halts | F on both legs (C1). A leg with no position, working order or unresolved request (an unknown order counts as unresolved) only needs disabling | Both legs end (C1) |
| 3 | Missing or short protection (§4) | A filled leg whose broker-reported working stop is missing or covers less than its open quantity | F on both legs (C1) | Both legs end (C1) |
| 4 | Unexplained activity on a leg's own instrument (a fill or order the instance did not send) | The instance halts with an incident (B2) | F on both legs (C1) | Both legs end (C1) |
| 5 | Activity on neither instrument, or on another account (B2) | A position or order the pair did not send | F on both legs, with the unexplained position and orders included in step 2: disable both instances, then flatten and cancel both legs and the unexplained exposure in Tradovate web, then verify all of them | Ends for both legs |
| 6 | Account loss threshold reached (B6) | §4 | F on both legs | Ends for both legs |
| 7 | A leg is still open at the operator flatten time (B14, D2) | A position after the strategy's own scheduled exit should have run; most likely Aegis, whose exit needs a bar close | F that leg | Ends normally after §6 |
| 8 | Account evidence lost (runbook §2.4) | The Tradovate account view is stale or unavailable beyond the freshness limit, so the loss threshold cannot be watched | F on both legs, using whatever view still works | Ends for both legs |

## 6. End of session

1. From each strategy's own scheduled exit until the leg is flat, watch it close.
   Any leg still open at the operator flatten time gets F (card 7).
2. **Verified flat (B11).** Both views read after the last request show zero positions
   and no working orders; no request is unresolved; every journal request has a
   terminal outcome; every execution is correlated. Empty grids, net zero, elapsed
   time or an acknowledgment do not count.
3. Then: disable both instances, disconnect, set the connection not to connect on
   startup, and check the saved workspace (runbook §2.7 step 6).
4. Export both journals and both views' records to private custody (B15).
5. If flat cannot be verified, stay. The account remains under attended recovery,
   flattening and cancelling in Tradovate web, until both views show flat.

## 7. After the session

1. A private session record: what happened against each B-row and each incident card,
   with the evidence from §6 step 4.
2. Score each strategy's forward trades under the
   [forward stop rule](../briefs/pre-registration/2026-10-31-tradeify-forward-stop-rule-registration.md)
   (keep, drop or halt). A drop or halt disables that instance before the next session
   (B12).
3. A recorded review before the next session (runbook §3).
4. STATE gets the public line only: the session was held, and whether an incident
   occurred. No balances or P&L (AGENTS.md data rules).

## 8. Weekly preservation trade

Placed only outside an armed session, with both instances disabled and the account
flat (B13). After it, run §6 steps 2–3 before the next session.

## 9. Choices for Joshua

- **C1. Scope of a leg incident (cards 2–4).** Recommendation: for the first
  sessions, any incident ends both legs, through F on both legs (§2). That matches
  A11.2 as written ("an incident ends automated trading for that session") and keeps a
  lone operator's job simple. Once sessions have run cleanly, a leg incident could end
  that leg only, because each instance owns only its own instrument (11-05 path).
- **C2. Operator flatten time.** It must fall before 16:45 ET and after both strategies'
  own scheduled exits. If a strategy's tested exit is at or after a workable flatten
  time, the operator's F pre-empts it every session. That changes behaviour against
  the tested source, and the signed page names it. Recommendation: 16:40 ET at the
  latest.
- **C3. Protection limit (§4).** Set on the signed page, from how long the Sim101 runs
  took to show a working stop after a fill.
