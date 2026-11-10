# STATE — First Passage

**Updated:** 2026-11-10. One page: goal, method, obligations, open decisions. Replace
stale lines instead of appending history.

## Goal

Strategy research only ([rulings 2026-11-09](docs/notes/2026-11-09-rulings.md), R1):
find out with honest evidence whether any systematic futures strategy has a real edge
after costs. The prop operation is closed. No order, venue, deployment or monetisation
work until a Codex-verified CONFIRMED result exists, and that opens only a separate
deployment decision under its own contract.

The coda on the owned Tradeify eval ended on 2026-11-10 before any session
([R13](docs/notes/2026-11-09-rulings.md)); the eval lapses. Joshua does not plan to reopen
the strategy or operations paths after the quarantine.

## Method

[The Order](docs/framework/the-order.md), witness mode, adopted 2026-11-09 when the
self-email recorded its hash (R10). Its
machine state, [`order-state.json`](docs/framework/order-state.json), is already shown at
every session start and enforced by the `order-gates` check. The enforcement files are
code-owned ([CODEOWNERS](.github/CODEOWNERS)); the `order-enforcement-files` ruleset
makes changing them a deliberate, logged admin bypass.

- **Step:** stop. Joshua ended the research round on 2026-11-10 ("Stop the round"), a
  discretionary stop with zero registered cards. Quarantine runs 2026-11-10 to 2026-11-24:
  only `closure:` commits on the closure paths in `order-state.json`. The closing record is
  written in the quarantine.
- **Round terms (contract §3):** at most 4 cards, ending at the fourth consumed card's
  verdict or on 2026-11-30; 2-3 index-micro cards from different mechanism families, at
  most 1 MGC, no 6J/M6E breakout cards; banked K still counts; about 1 hour a week of
  Joshua's time; spend limited to the data line.

## Live obligations

| Obligation | Next due | Notes |
|---|---|---|
| Subscription reconfirm | 11-21 | Joshua reconfirms the [ledger](docs/pursuits/SUBSCRIPTION_LEDGER.md) and cuts spend to the data line (R7). |
| Witness record | Sent 2026-11-09 | Hashes emailed to Joshua's second account with an OpenTimestamps proof (R10). Joshua runs `ots upgrade` on the proof once Bitcoin confirms it. |

## Open decisions (Joshua)

1. **Recommendations 2, 3 and 4** at the end of the
   [2026-11-09 rulings](docs/notes/2026-11-09-rulings.md). Joshua confirmed 1 and 5-8 on
   2026-11-10 (addendum there).
2. **Data rights:** research still rests on TradingView CME exports under accepted
   terms-of-service risk (D16). A licensed data path is the long-horizon requirement to
   question.
