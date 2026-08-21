# Subscription / venue-account ledger — CFO-owned

One row per `docs/pursuits/d11-d17` cost-carrying record. Canonical source for every $/mo
figure — the pursuit records themselves link here rather than restating the number (Rule 7,
one canonical owner). Built per
[`docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md`](../adr/2026-08-21-cfo-subscription-ledger-consolidation.md),
closing GSUB-1's concern C-1 (subscription $ figures not discoverable in-repo, open
2026-08-09 → 2026-08-21).

**Reconfirm cadence:** monthly — see `STATE.md` § Scheduled forward triggers, "Monthly —
recurring." Each reconfirm updates the "Last confirmed" column below; a figure that goes
un-reconfirmed for >60 days should be treated as stale, not silently trusted.

| Subscription | Pursuit | $/mo | Billing model | Last confirmed | Status |
|---|---|---|---|---|---|
| TradingView | [d11](d11-tradingview-subscription.md) | $70 | flat | 2026-08-21 | confirmed |
| Databento | [d12](d12-databento-subscription.md) | $200 | **flagged** — record describes usage-billed/per-pull-gated; operator's figure reads flat. Tension open, not reconciled. | 2026-08-21 | confirmed (billing-model question open) |
| Fly.io | [d13](d13-flyio-subscription.md) | — | — | asked 2026-08-21, not supplied | **still open** |
| CrossTrade | [d14](d14-crosstrade-subscription.md) | $50 | flat | 2026-08-21 | confirmed |
| Tradeify | [d15](d15-tradeify-account.md) | — | account-carrying cost, not a subscription fee | asked 2026-08-21, not supplied | **still open** |
| Cursor Ultra | [d16](d16-cursor-subscription.md) | $200 | flat | 2026-08-21 | confirmed |
| Claude Max | [d17](d17-claude-max-subscription.md) | $200 | flat | 2026-08-21 | confirmed |

**Confirmed monthly total:** $720/mo (five confirmed rows; Fly.io and Tradeify excluded from
this sum since their figures are still unverified, not zero — do not read $720 as the true
total).

**Change log**

| Date | Change |
|---|---|
| 2026-08-21 | Ledger created — five figures operator-confirmed, one flagged (Databento billing-model tension), two still open (Fly.io, Tradeify). Closes GSUB-1 C-1. |
