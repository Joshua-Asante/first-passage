# ORB + Aegis attended session: operator procedure

**Status:** `ACCEPTED 2026-11-07` by Joshua ("accept the procedure"), with the §9
decisions. Claude drafted it; Codex reviewed it. Changes need Joshua's ruling. It grants no
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

1. **Disable** the leg's instance in NinjaTrader, even if it is disconnected, and
   confirm it shows disabled. The strategy's own incident close stays in the build
   (B10). Once disable takes effect the strategy sends no more orders, including that
   close, and the leg's protective orders stay working, unmanaged (B8). Disable does
   not withdraw a close already sent. The signed page names what is unproven on the
   firm connection.
   **If NinjaTrader is frozen and disable cannot be confirmed,** end the NinjaTrader
   process and confirm it has exited before step 2. A frozen window does not prove the
   strategies have stopped, and cancelling a running strategy's stop in Tradovate can
   trigger its own close, which can open an opposite position. A process that has
   exited needs no disable: go to step 2, and keep it from restarting or reconnecting.
   Orders already sent stay live or unresolved until reconciled. If sending cannot be
   stopped promptly, use the emergency route on the signed page.
2. **Flatten and cancel** in the Tradovate web view. Use the action that exits that
   contract's position at market and cancels its working orders. The pre-session check
   confirms which button this is ("flatten path confirmed"). On a leg with no position,
   this cancels its working orders.
3. **Verify** with B11's conditions, not the grids alone. In both views, read after the
   last request: no position and no working orders on that instrument. Reconcile every
   request and execution the leg sent, using its journal together with the platform's
   order and execution records: a journal stops at disable, so it cannot account for
   later activity. While any request is unresolved or a view is unavailable, F is not
   complete. Keep automation disabled and keep watching, and if a late
   fill opens or reverses a position, repeat step 2 for it.

**F on both legs** runs each step across both legs before the next: disable both
instances, then flatten and cancel both legs, then verify both. Never wait on one
leg's verification while the other instance is still enabled; B6 gives no automation
that would stop it. If NinjaTrader is frozen or has exited, step 1's rule applies to both.
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
   - the observation cycle: how often a fresh broker read is taken after a fill, the
     one cycle a stop gets to appear before the operator acts (§4, C3);
   - the freshness limit: how long the Tradovate account view may go without updating
     before the operator treats account evidence as lost (§4, card 8);
   - the hard latest trigger: the time by which F starts on any leg still open,
     derived under C2 from a rehearsed worst-case F duration plus margin.
3. Plan the attended window. It must cover the session from enable until verified
   flat. If it cannot, do not start.
4. Do not start until the hard latest trigger has been derived from a rehearsal (C2).
5. Confirm the watcher is the version on the signed page, and check directly that each
   instance's refusal folder exists: the watcher does not flag a missing one.

## 4. During the session

| Watch | Where | When it trips | Do |
|---|---|---|---|
| A leg fills or part-fills | Tradovate web, that contract's orders | After one observation cycle, a fresh broker read still shows the working stop below the leg's whole open quantity, missing or short (B4, C3). A rejected or unknown protective order, a disconnect or lost broker evidence is an incident at once, not a reason to wait | Card 3; or cards 2, 1 or 8 |
| Working exit quantity | Tradovate web, that contract's orders | After one observation cycle, a fresh broker read shows a stop or target larger than the leg's open quantity, with no explanation. It can open an opposite position | Card 3 |
| Account equity | Tradovate web account view | At or below the account loss threshold (B6) | Card 6 |
| Account evidence | Tradovate web account view | The view stops updating or is unavailable for longer than the freshness limit (runbook §2.4) | Card 8 |
| Connection | NinjaTrader connection-loss alert | Any loss of connection (B7) | Incident card 1 |
| Broker activity | NinjaTrader Orders, Executions and Positions; Tradovate web | Any rejected or unknown request, or any order, fill or position change the pair did not send. Do not wait for an instance to halt: not every rejection halts it, ORB does not see a manual fill on its own instrument, and Aegis can stop managing a leg while its row still shows enabled | Incident cards 2, 4 or 5 |
| Instance diagnostics | NinjaTrader log, NinjaScript Output and the watcher | Any halt, refusal, incident or close-wait flag *(signed page)*. A close-wait flag is a late alarm: an incident above never waits for it | F on both legs; the session ends |
| The watcher | Its own display | It stops updating or cannot read its evidence while either instance is enabled | F on both legs; the session ends |
| The operator | — | The operator must leave the screen | F on both legs; the session ends |

## 5. Incident cards

| # | Situation | What the operator sees | Do | Session after |
|---|---|---|---|---|
| 1 | Connection lost (NinjaTrader, or the platform crashes or restarts) | Connection-loss alert; positions and orders in Tradovate web may still be live | F on both legs, flattening from Tradovate web (F step 1 covers a NinjaTrader that is frozen or has exited). Do not reconnect to resume: reconnecting never resumes trading (B7). Protection across a disconnect is unproven (U-3), so an open leg is treated as unprotected | Ends for both legs |
| 2 | Rejected or unknown order on a leg (B9) | A rejected or unknown order in the NinjaTrader log or Orders view; the instance may keep running | F on both legs (C1). A leg with no position, working order or unresolved request (an unknown order counts as unresolved) only needs disabling | Both legs end (C1) |
| 3 | Missing, short or oversized protection (§4) | A filled leg whose broker-reported working stop is missing or covers less than its open quantity, or a stop or target larger than it | F on both legs (C1) | Both legs end (C1) |
| 4 | Unexplained activity on a leg's own instrument (a fill or order the instance did not send) | A fill or order in the Orders, Executions or Positions view that the instance did not send; the instance may not notice (B2) | F on both legs (C1) | Both legs end (C1) |
| 5 | Activity on neither instrument, or on another account (B2) | A position or order the pair did not send | F on both legs, with the unexplained position and orders included in step 2: disable both instances, then flatten and cancel both legs and the unexplained exposure in Tradovate web, then verify all of them | Ends for both legs |
| 6 | Account loss threshold reached (B6) | §4 | F on both legs | Ends for both legs |
| 7 | A leg is still open at the hard latest trigger (B14, D2, C2) | A position after the strategy's own scheduled exit should have run; most likely Aegis, whose exit needs a bar close | F that leg | Ends normally after §6 |
| 8 | Account evidence lost (runbook §2.4) | The Tradovate account view is stale or unavailable beyond the freshness limit, so the loss threshold cannot be watched | F on both legs, using whatever view still works | Ends for both legs |

## 6. End of session

1. From each strategy's own scheduled exit until the leg is flat, watch it close.
   Any leg still open at the hard latest trigger gets F (card 7).
2. **Verified flat (B11).** Both views read after the last request show zero positions
   and no working orders, and no request is unresolved. Empty grids, net zero, elapsed
   time or an acknowledgment do not count.
3. Disable both instances. Reconcile every request and execution, using the journals
   together with the platform's order and execution records, including any activity
   after disable; if there was any, re-read both views. Then disconnect, set the
   connection not to connect on startup, and check the saved workspace (runbook §2.7
   step 6).
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

## 9. Decisions

Joshua adopted Codex's recommendations on all three choices, 2026-11-07
([Codex's answer](https://github.com/Joshua-Asante/first-passage/pull/1118#issuecomment-6700011227)).

Joshua ruled again on 2026-11-07 ("Keep one cycle" and "Approve as written", on
[#1130](https://github.com/Joshua-Asante/first-passage/pull/1130)). If NinjaTrader is
frozen, its process is ended before flattening (F step 1). Oversized protection is an
incident after one observation cycle (§4, card 3). Watcher failure ends the session, even
when flat (§4). The operator watches broker activity, not instance halts (§4, cards 2 and 4).

- **C1. Incident scope.** Whether something is an incident is judged per leg: the
  companion's normal activity on its own instrument is not one (B2, 11-05 path). Once
  an incident is declared on either leg, automation ends for the whole session, through
  F on both legs (§2), as A11.2 says ("an incident ends automated trading for that
  session"). Ending only the affected leg would need an explicit ruling by Joshua; clean
  sessions alone do not authorise it.
- **C2. Exit backstop: two triggers.**
  1. *Normal:* each strategy gets its tested scheduled exit, including the bar close
     Aegis's exit needs (D2).
  2. *Hard latest:* whether or not that exit has fired, F starts early enough that a
     full F, measured at its worst case in a rehearsal (submission, fills,
     cancellation, verification and an adverse-path allowance), finishes before
     16:45 ET, plus an explicit margin. The time is derived backwards from 16:45 ET,
     not chosen as a round number, and is checked against both tested exits
     *(signed page)*.

  If no time both gives the tested exits a real chance and leaves that recovery time,
  either the signed page records that the hard trigger pre-empts the tested exit and
  Joshua accepts that difference, or the session does not run.
- **C3. Protection check.** For the first firm sessions: after every fill or partial
  fill, take a fresh broker read. Allow one observation cycle for a working stop
  covering the whole open quantity to appear. If the next fresh read still shows any
  shortfall, run F (card 3). A rejected or unknown protective order, a disconnect or
  lost broker evidence is an incident at once (cards 2, 1, 8). Sim101 timings can
  inform the observation cycle but cannot set the firm-connection bound (U-7). A
  broker-reported `Working` stop does not prove it survives a disconnect (U-3). The
  bound may be relaxed later only by a ruling Joshua registers in advance, set from the
  slow tail of firm observations plus margin, never the average.
