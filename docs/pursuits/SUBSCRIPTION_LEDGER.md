# Subscription / venue-account ledger

One row per `docs/pursuits/d11-d18` cost-carrying record. Canonical source for every $/mo
figure — the pursuit records themselves link here rather than restating the number (Rule 7,
one canonical owner). Built per
[`docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md`](../adr/2026-08-21-cfo-subscription-ledger-consolidation.md),
closing GSUB-1's concern C-1 (subscription $ figures not discoverable in-repo, open
2026-08-09 → 2026-08-21).

**Reconfirmation owner:** the operator.

**Reconfirm cadence:** monthly — see `STATE.md` § Scheduled forward triggers, "Monthly —
recurring." Each reconfirm updates the "Last confirmed" column below; a figure that goes
un-reconfirmed for >60 days should be treated as stale, not silently trusted.

| Subscription | Pursuit | $/mo | Billing model | Last confirmed | Status |
|---|---|---|---|---|---|
| TradingView | [d11](d11-tradingview-subscription.md) | $70 | flat | 2026-08-21 | confirmed |
| Databento | [d12](d12-databento-subscription.md) | $0 recurring after retirement | unsubscribed; final invoice/usage charges unverified | 2026-09-10 (operator report) | retired; excluded from active recurring total |
| Fly.io | [d13](d13-flyio-subscription.md) | — | — | asked 2026-08-21, not supplied | **still open** |
| CrossTrade | [d14](d14-crosstrade-subscription.md) | $50 | flat | 2026-08-21 | confirmed |
| Tradeify | [d15](d15-tradeify-account.md) | — | account-carrying cost, not a subscription fee | asked 2026-08-21, not supplied | **still open** |
| Cursor Ultra | [d16](d16-cursor-subscription.md) | excluded | removed from recurring spend by operator; final charges unverified | 2026-09-10 (operator instruction) | removed from active recurring total |
| Claude Max | [d17](d17-claude-max-subscription.md) | $100 | flat | 2026-09-10 | confirmed |
| Codex | [d18](d18-codex-subscription.md) | $200 | monthly amount supplied; plan details unspecified | 2026-09-10 | operator-confirmed |

**Confirmed active recurring monthly total:** $420/mo (four confirmed active rows:
TradingView, CrossTrade, Claude Max and Codex).
Databento is retired and excluded; its effective cancellation date and final invoice
were not supplied. Cursor is removed from recurring spend by operator instruction;
no cancellation date or final invoice was supplied. Fly.io and Tradeify remain
unverified, not zero. Do not read $420 as total spend or as settlement of outstanding
charges.

**Change log**

| Date | Change |
|---|---|
| 2026-09-10 | Operator removes Cursor from recurring spend, revises Claude Max from $200 to $100/month, and adds Codex at $200/month. Active recurring total: $520 - $200 - $100 + $200 = $420. Claude remains active. Cursor cancellation date/final charges and Codex plan details not supplied. |
| 2026-09-10 | Operator reports Databento retired/unsubscribed, no replacement approved. Removed prior $200 from active recurring total: $720 to $520. Report date is not an asserted cancellation date; final invoice and historical billing-model tension remain unverified. |
| 2026-08-21 | Ledger created — five figures operator-confirmed, one flagged (Databento billing-model tension), two still open (Fly.io, Tradeify). Closes GSUB-1 C-1. |
