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

Every incident card below ends in **F**. It always runs in this order:

1. **Disable** the leg's instance in NinjaTrader. The strategy's own incident close
   stays in the build (B10). A manual flatten while the instance is enabled can race
   that close, and if both fill, the position reverses. Disabling leaves the leg's
   protective orders working (B8), so the position stays protected until step 2.
2. **Flatten and cancel** in the Tradovate web view. Use the action that exits that
   contract's position at market and cancels its working orders. The pre-session check
   confirms which button this is ("flatten path confirmed").
3. **Verify** in both views (NinjaTrader and Tradovate web): no position and no working
   orders on that instrument. If the position reversed (a strategy close or stop
   filled at the same moment), repeat step 2 for the reversed quantity.

A leg that has had F is not re-enabled in the same session. Re-enabling is never a
recovery step (B8), and an incident ends automation for that session
([runbook](https://github.com/Joshua-Asante/first-passage/blob/b7eaff7/docs/notes/2026-10-18-native-protection-recovery-pilot-runbook.md) §3, A11.2).

## 3. Before the session

1. Run the spec's [pre-session check](2026-11-06-orb-aegis-eval-build-design.md#5-attended-pre-session-check)
   (items 1–8).
2. Have these values at hand *(signed page)*:
   - today's trailing floor (highest end-of-day balance minus $3,000; the eval has no
     lock, and Tradeify enforces the floor intraday);
   - the account loss threshold, set above that floor (B6);
   - the protection limit: how long after a fill a leg may go without a working stop
     before the operator acts (§4);
   - the operator flatten time, before 16:45 ET (§5, C2).
3. Plan the attended window. It must cover the session from enable until verified
   flat. If it cannot, do not start.

## 4. During the session

| Watch | Where | When it trips | Do |
|---|---|---|---|
| A leg fills | Tradovate web, that contract's orders | No working protective stop within the protection limit (B4; U-3 and U-7 are unproven) | F that leg |
| Account equity | Tradovate web account view | At or below the account loss threshold (B6) | F both legs; the session ends |
| Connection | NinjaTrader connection-loss alert | Any loss of connection (B7) | Incident card 1 |
| Each instance's state | NinjaTrader strategies tab | An instance halts or reports a fault | Incident cards 2–4 |
| The operator | — | The operator must leave the screen | F both legs; the session ends |

## 5. Incident cards

| # | Situation | What the operator sees | Do | Session after |
|---|---|---|---|---|
| 1 | Connection lost (NinjaTrader, or the platform crashes or restarts) | Connection-loss alert; positions in Tradovate web may still be open | For each leg with a position, F, using Tradovate web for step 2. Disable flat legs. Do not reconnect to resume: reconnecting never resumes trading (B7). Protection across a disconnect is unproven (U-3), so an open leg is treated as unprotected | Ends for both legs |
| 2 | Rejected or unknown order on a leg (B9) | The instance halts | Check both views. If the leg has a position or a working order, F. If flat with none, disable | Both legs end (C1) |
| 3 | Missing protection (§4) | A filled leg with no working stop | F | Both legs end (C1) |
| 4 | Unexplained activity on a leg's own instrument (a fill or order the instance did not send) | The instance halts with an incident (B2) | F that leg | Both legs end (C1) |
| 5 | Activity on neither instrument, or on another account (B2) | A position or order the pair did not send | F both legs, then close the unexplained position and cancel its orders in Tradovate web | Ends for both legs |
| 6 | Account loss threshold reached (B6) | §4 | F both legs | Ends for both legs |
| 7 | A leg is still open at the operator flatten time (B14, D2) | A position after the strategy's own scheduled exit should have run; most likely Aegis, whose exit needs a bar close | F that leg | Ends normally after §6 |

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
  sessions, any incident ends both legs; run F on the other leg too. That matches
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
