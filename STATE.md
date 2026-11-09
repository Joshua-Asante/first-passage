# STATE — First Passage

**Updated:** 2026-11-09. One page: goal, method, obligations, open decisions. Replace
stale lines instead of appending history.

## Goal

Strategy research only ([rulings 2026-11-09](docs/notes/2026-11-09-rulings.md), R1):
find out with honest evidence whether any systematic futures strategy has a real edge
after costs. The prop operation is closed. No order, venue, deployment or monetisation
work until a Codex-verified CONFIRMED result exists, and that opens only a separate
deployment decision under its own contract.

## Method

[The Order](docs/framework/the-order.md), witness mode, **adoption pending** (R10): it is
adopted when Joshua's scheduled self-email records its hash (see obligations). Its
machine state, [`order-state.json`](docs/framework/order-state.json), is already shown at
every session start and enforced by the `order-gates` check.

- **Step:** aim. **No contract yet,** so there is no programme work. Stopping and
  shrinking (closure records, deletions) need none.
- **Round inputs Joshua has accepted (R2, R7),** for him to put in the contract: one
  round of at most 4 cards, ending at 4 or on 2026-12-31; 2-3 index-micro cards from
  different mechanism families, at most 1 MGC, no 6J/M6E breakout cards; banked K still
  counts; about 1 hour a week of his time; spend limited to the data line.

## Live obligations

| Obligation | Next due | Notes |
|---|---|---|
| Tradeify eval | — | Lapses (R3). No more preservation trades; agents place nothing. |
| Subscription reconfirm | 11-21 | Joshua reconfirms the [ledger](docs/pursuits/SUBSCRIPTION_LEDGER.md) and cuts spend to the data line (R7). |
| Witness record | After merging #1176 | Joshua self-emails The Order's hashes with an OpenTimestamps proof (R10). |

## Open decisions (Joshua)

1. **The round's contract** (Order step 1): objective, limiting input, budgets, outside
   questions, kill rule, caps. Agents may not draft items 1 and 2.
2. **Protect the enforcement files:** a GitHub ruleset requiring Joshua's approval for
   `scripts/check_order.py`, `scripts/gates.yml` and `.claude/settings.json`.
3. **The eight technical recommendations** at the end of the
   [2026-11-09 rulings](docs/notes/2026-11-09-rulings.md). They gate the later
   narrowing PRs (tooling, lab, ops and core removals).
4. **Data rights:** research still rests on TradingView CME exports under accepted
   terms-of-service risk (D16). A licensed data path is the long-horizon requirement to
   question.
