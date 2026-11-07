# ORB + Aegis native eval build: design spec

**Status:** `ACCEPTED 2026-11-06` by Joshua ("accept the spec"), then amended the same
day: he ruled "No rerun, use the tested source, no need to wait" (§7). Claude drafted it. It grants no build, GO, session or spend. It is the
behaviour contract that the private eval build is checked against at step 4 of the
[11-05 bare-bones path](https://github.com/Joshua-Asante/first-passage/blob/b7eaff7/docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-11-05--bare-bones-eval-path)
(the signed page and the pre-session check). Changes after acceptance need Joshua's
ruling.

**Why this exists.** The pair's behaviour design was spread across the
[pilot runbook](https://github.com/Joshua-Asante/first-passage/blob/b7eaff7/docs/notes/2026-10-18-native-protection-recovery-pilot-runbook.md)
(492 lines, rulings D-N1 to D-N16 and SM-1 to SM-3), the 11-05 exceptions, the
private cards, `core/firm_rules.py` and the forward stop rule. The governance cut
removed the runbook and checklist from `main`. This page states what the eval build
must do today, in one place. Links point at commit `b7eaff7`.

**Public/private split.** This page carries no parameters, cap values, prices or
account data. Each row's "confirm" column is ticked locally against the private
frozen source set (D7), in Joshua's primary checkout. The ticks go on the signed page,
not in this repo.

## 1. What is being built

- One account: the owned **Tradeify Select 100K evaluation**, through NinjaTrader 8
  on Tradovate.
- Two NinjaScript strategy instances: **ORB on MNQ** and **Aegis on full 6J**. Each
  instance owns only its own instrument (11-05 exception).
- All signal, sizing and order logic is native. There are no external calls, ATI,
  CrossTrade or bridges ([AGENTS.md](../../AGENTS.md) money control 3).
- The eval build is the frozen source set derived from S-PAIR, with the four changes in D7.

## 2. Account envelope (public venue facts)

Source: `core/firm_rules.py` (`_TRADEIFY_EVAL`, `_TRADEIFY_SELECT_EVAL`,
`Tradeify_Select_100K`).

| Fact | Value | What the build must do about it |
|---|---|---|
| Max drawdown | $3,000 trailing, ratcheting on end-of-day balance, no lock in eval, **breached intraday** | Each loss guard sits inside the floor with a margin (B6) |
| Profit target | $6,000; at least 3 trading days | Nothing. Passing is not a strategy input |
| Consistency | Best day at most 40% of total profit at pass (so at most $2,400 when the target is reached) | No daily profit cap for now (D3) |
| Size cap | 80 micro-equivalents; one 6J counts as 10 micros | The static per-leg caps sum to at most 80 (B3) |
| Session | Force-flat 16:45 ET; no weekend holds | Flat before the venue acts (B5) |
| Activity | At least one trade per Mon–Fri week | The weekly preservation trade covers this (B13) |
| Costs | $0.91 per side MNQ; $3.10 per side 6J | Fixed in the private card, not here |

## 3. Required behaviour

"Proven on" says what evidence exists or is planned. Under the 11-05 path the
runbook's U-tests are no longer gates, because Sim cannot prove them. Where
behaviour is unproven on the firm connection, the signed page names it as risk
Joshua accepts.

| ID | Behaviour | Source | Proven on | Confirm in build |
|---|---|---|---|---|
| B1 | Native only: no network calls, ATI, add-ons or external signals | AGENTS rule 3 | Source read | ☐ |
| B2 | Each instance sends orders only for its own instrument, recognises only its own orders and fills, and refuses to start unless that instrument is flat with no working orders. What it cannot correlate on its own instrument is an incident. The companion's activity on the other leg's instrument is not an incident. Activity on neither instrument, or on another account, is unexplained and a stop. Each instance keeps its own journal | Runbook §2.1, §2.6, §6.8; 11-05 "Runbook §6 for the pair" | Sim101 | ☐ |
| B3 | Static per-leg cap. Each request is admitted whole or refused, never clipped. The caps sum to ≤ 80 micro-equivalents | Runbook §2.2 as replaced 11-05 | Sim101 | ☐ |
| B4 | The strategy submits its own protective stop sized to filled quantity and resizes it on partial fills. Protection counts only once the broker reports it working. No ATM templates | Runbook §2.3 | Sim101; firm-connection residency (U-3) is accepted risk | ☐ |
| B5 | Normal scheduled exits as S-PAIR tested them; the frozen set changes only exceptional close handling (D7). No session on a day whose calendar row is not `PERMITTED`, and none on a shortened day: the exits have early-close branches, but nothing shows they meet the venue's earlier deadline (12:59 ET on 2026-11-27) end to end | D4 withdrawn | Sim101 on a normal day; the strategies' own cutoff close has not run on this host | ☐ |
| B6 | The account loss stop, account-wide incidents and stopping new risk across both legs belong to the **attending operator**, under the signed page and the stop rule. No cross-instance automation handles them. Each instance keeps its own leg's position stop (B4) and scheduled exit (B5). Any account-level threshold the operator uses is private | 11-05 "Runbook §6 for the pair"; runbook §2.4 | Attended | n/a |
| B7 | Any loss of connection halts new risk, and any connection alert from enable onward ends automation for that session, even if the connection returns and the instance looks healthy. The operator disables first, then follows the procedure. The build alone does not guarantee this: an instance that was flat when the connection dropped can resume after a reconnect. The connection-loss setting stays on the option that does not replay or recalculate into new orders | Joshua 11-06 (private sheet: any connection alert ends ORB for the session; disconnect risk accepted, attended, with Tradovate web as the second flatten path); procedure card 1 (both legs); [A11.2](https://github.com/Joshua-Asante/first-passage/blob/b7eaff7/docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md) (no same-session restart). Why it still applies: while disconnected an instance cannot see fills or confirm protection (U-3), so its own record may be wrong. No venue rule or recorded disconnect stands behind it. Inherited through runbook §2.5; U-4 | Accepted risk | ☐ |
| B8 | Disabling an instance leaves working protection in place, unmanaged: nothing trails or resizes it after that, so disabling alone is not a stop. This depends on NinjaTrader's two cancel-on-disable options being off (§5). Re-enabling is never a recovery step, and the build does not block it, so this is an operator rule (the 10-17 canary showed `WaitUntilFlat` cancelling protection) | 10-17 Sim101 canary; S-PAIR 11-06 on Sim101 (orders stayed working after disable, until the manual close). Why it still applies: step 1 of the procedure's F relies on it. Runbook §2.3 item 5 | Sim101 canary 10-17; S-PAIR 11-06. Firm connection unproven (U-6) | ☐ |
| B9 | An unknown order is never resent, and neither is a rejected entry or add. A rejected protective order is not replaced: the leg goes to its incident close (B10). A close that ends without closing the leg may be followed by another only within the limit the build carries, sized to the leg's position at that moment. Not every rejection halts the instance, so any rejected or unknown order ends the session through the operator (procedure card 2) | D-N6 (Joshua 10-19: a rejected entry is never resent and stops for review); [A12 F1](https://github.com/Joshua-Asante/first-passage/blob/b7eaff7/docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md) (no resend of an unknown outcome); D-N1, runbook §2.8 item 5, and Joshua 11-07 (private: limit on replacement closes). Why it still applies: an unknown order may be live, so a resend can double exposure, and how Tradovate reports a rejection is unknown. Runbook §2.6 | Offline tests. S-PAIR's Sim101 run had no rejected order | ☐ |
| B10 | The strategy's own incident close (D-N1) stays in the frozen set (D7) and is not relied on (11-05). On an incident the operator flattens in Tradovate. The signed page says how the two interact | Runbook §2.8; 11-05; D1 withdrawn | U-3, U-5, U-9, U-17 unproven on the firm connection | ☐ |
| B11 | Verified-flat shutdown. First read both views (NinjaTrader and Tradovate web) after the last request: both must show zero gross positions and no working orders, with no request unresolved. Then disable, and check that every request has a terminal outcome and every execution is correlated, using the journals and the platform's order and execution records together: a journal stops at disable, and one journal cannot be read while its instance runs. Empty grids, net zero, elapsed time or an acknowledgment do not count. Then disconnect, and export the journals to private custody. If flat cannot be verified, the account stays under attended recovery | NinjaTrader's order grid hides prior-day orders after rollover, so one view cannot prove no working orders (10-18 finding, U-13). S-PAIR 11-06: the journal ends at disable. Venue: the drawdown is breached intraday and no weekend holds (§2), so a false flat is costly. [Halt/resume contract](2026-09-14-tb-s3-halt-resume-contract.md) §3; runbook §2.7 items 3–7 | Attended | ☐ |
| B12 | Forward stop rule: after each session, each strategy's forward trades are scored offline (keep, drop or halt). A drop or halt disables that instance before the next session | [Stop rule registration](../briefs/pre-registration/2026-10-31-tradeify-forward-stop-rule-registration.md) | Offline, private | n/a |
| B13 | The weekly preservation trade is placed only while both instances are disabled and the account is flat. While either instance is armed, a manual trade on its instrument is an uncorrelated fill, and a trade on any other instrument is unexplained activity; both stop the session. Any other placement needs a new ruling | 11-05 "Runbook §6 for the pair"; runbook U-12; STATE | Weekly practice | n/a |
| B14 | No position held past the venue force-flat. S-PAIR's tested exits stand; the attending operator stays until each leg is flat | Venue rule; D2; D4 withdrawn | Source read; Sim101 to the drill only | ☐ |
| B15 | Journals, exports and screenshots contain account data, so they stay in private custody and never enter this repo | AGENTS data rules | n/a | n/a |

## 4. What the 11-05 path removed

Joshua accepted these as risk when he adopted the bare-bones path:

- An attended check replaces instance M1 acceptance.
- The signed page and pre-session check replace the runbook's P2 entry gate.
- U-1 to U-18 stop being gates. Protection across a disconnect on the firm
  connection (U-3) and the quantity callbacks (U-18) are unproven.
- The automatic incident close is not relied on.
- Joshua still owns: starting without Tradeify's source-review reply, CME licence
  risk, T1 (preservation trade vs ESA §6.5) and T2 (agent-operated orders).

## 5. Attended pre-session check

From the 11-05 exception, plus the build-specific items from §3:

1. Platform alert audible; connection-loss alert on; operator present.
2. Tradovate web view open; flatten path confirmed.
3. The account is flat with no working orders, in both views (B2, B11).
4. Both instances are on the eval account, not Sim101 or another account (U-16),
   and the loaded build matches the frozen source manifest on the signed page, by checksum.
   NinjaTrader's cancel-on-disable options are off (B8).
5. Today's calendar row is `PERMITTED` and is not a shortened day (B5).
6. The operator has the account loss threshold and the flatten path for both legs
   at hand (B6).
7. The per-leg caps match the private card (B3).
8. The session GO is in hand (AGENTS money control 1).

## 6. Who does what

| Stage | Owner | Hands over |
|---|---|---|
| Definition | Claude drafts this page; Joshua accepts it | The accepted spec |
| Creation | Claude Code in Joshua's primary checkout (private) | The eval build: the frozen set (D7), with the §3 confirm column ticked |
| Verification | S-PAIR Sim101 run 11-06, accepted by Joshua, then a short Sim101 check of ORB on the frozen set; Codex reviews this spec, any public harness and the private source (Joshua 11-06); Joshua signs the page | Signed page, then GO |
| Measure | Post-session export, forward stop rule scored privately | Keep, drop or halt per strategy, then STATE |

## 7. Decisions

Decided by Joshua, 2026-11-06:

- **D1 (B10).** Withdrawn 11-06: the source does not change, so the incident close stays as built.
- **D2 (B14).** Corrected 11-06: each strategy has its own tested scheduled exit, and they differ. Aegis's needs a bar close to fire, so it has no clock backstop. The signed page states both.
- **D3.** No daily profit cap for now. Revisit if a single day's profit is likely to
  exceed one third of the profit target ($2,000 of $6,000), which is below the 40%
  consistency limit ($2,400).
- **D4 (B5, B14).** Withdrawn 11-06: S-PAIR's exits stay as tested and there is no Sim101 rerun.
- **D5 (B5).** Withdrawn 11-06 with D4.
- **D6 (Tradeify source review).** Tradeify received S-PAIR's source on 11-05. Joshua sends
  them the eval files, checksums and a change list before any enable; agents never send
  private source. The first session does **not** wait for Tradeify's source-review reply.
- **D7 (the frozen set).** Joshua reopened the source on 11-06, ruled two further changes on
  11-07, then froze the set. It holds four ORB changes: no journal record per tick; an order
  id change is no longer a fault; terminal order states are handled correctly when an error
  is reported; and replacement of a normal close is bounded. Normal signal, sizing and stop
  calculations are unchanged; exceptional close handling changes on purpose. Aegis is
  unchanged. Any further source change needs Joshua's ruling and a new version-named set. A
  short Sim101 check covers ORB on the frozen set; it is not a full rerun.

Decided by Joshua, 2026-11-07 ("Approve as written", on [#1129](https://github.com/Joshua-Asante/first-passage/pull/1129)):

- **D8 (B7, B8, B9, B11).** Each row now names a reason that still applies to a native
  build. On a rejected or unknown order, the operator ends the session, because not every
  rejection halts the instance. In verified flat, disable comes before the journal check.
