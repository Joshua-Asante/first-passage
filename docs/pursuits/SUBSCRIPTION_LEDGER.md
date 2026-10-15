# Subscription / venue-account ledger

One row per `docs/pursuits/d11-d19` cost-carrying record. Canonical source for every $/mo
figure — the pursuit records themselves link here rather than restating the number (Rule 7,
one canonical owner). Created 2026-08-21, closing GSUB-1's concern C-1 (subscription $ figures
not discoverable in-repo, open 2026-08-09 → 2026-08-21), under the operator-ratified
[rules](#rules) below.

**Reconfirmation owner:** the operator.

**Reconfirm cadence:** monthly — see `STATE.md` § Scheduled forward triggers, "Monthly —
recurring." Each reconfirm updates the "Last confirmed" column below; a figure that goes
un-reconfirmed for >60 days should be treated as stale, not silently trusted.

## Rules

Consolidated 2026-10-15 from 2026-08-21-cfo-subscription-ledger-consolidation (removed; see
[TOMBSTONES](../adr/TOMBSTONES.md#2026-10-15-adr-decay-audit-removals)). The operator ratified the
ledger, checks and monthly cadence on 2026-08-21; the 2026-09-08 revision removed the retired role's
hooks with ledger terms unchanged. Two stale details are corrected on the move: the ledger covers
d11–d19 (the ADR said d11–d17), and the checker is run manually (unwired from every gate tier since
2026-08-24, [pursuits README](README.md)).

- **One ledger.** This file owns the cost figures for d11–d19. Pursuit records link to it rather
  than repeat numbers. Missing figures remain unknown, not zero.
- **Ledger pointer.** [`check_pursuit_records.py`](../../scripts/check_pursuit_records.py) requires
  a ledger pointer on KEEP records of class `(d) meta-belt (subscription)` or
  `(d) meta-belt (venue account)`. It reports WARN and exits zero on a completed scan; no severity
  escalation or class widening is authorized. Reverify the actual corpus before any separately
  approved widening. This remains a scoped check, not a general required-field mandate for every
  pursuit.
- **Monthly reconfirmation.** The operator confirms the ledger figures monthly, rolling the
  `STATE.md` deadline after each occurrence. Confirm even when unchanged; silence is not evidence
  of currency. No replacement role, hook or scheduled service is commissioned; STATE holds the
  forward reminder, not a claim about external scheduling.
- **Update at disclosure.** A cost supplied in-session updates its ledger row in that session. This
  is a practice, not a telemetry subsystem. Additional automation needs evidence that the practice
  is insufficient and its own decision.

**Trigger check schedule:** every monthly reconfirm (2026-09-21, then rolled forward) — carried verbatim from ADR 2026-08-21-cfo-subscription-ledger-consolidation; the live date is `STATE.md`'s Monthly row.

At each reconfirm, check whether the pointer rule gave a false-positive WARN for a record with no
meaningful cost, or the ledger missed a stale/wrong figure that the former per-pursuit text would
have caught. Either finding requires a decision to narrow/redesign the affected mechanism, with the
miss recorded. Three consecutive reconfirms with no figure changes and no staleness found warrant
proposing a quarterly cadence; they do not authorize changing it silently. The original verdict
distinction remains: RESOLVED when the mechanism runs without those failures, FALSIFIED for a
confirmed mechanism failure, AMBIGUOUS for that cadence signal pending a proposal.

*Grounds:* scattered cost tags left a known information gap open for twelve days. One owner plus a
creation-time pointer check makes the figures discoverable; operator reconfirmation checks their
truth. HARD-gating, a parallel monthly cron and new telemetry were rejected as extra machinery
without evidence. Monthly was the operator's chosen interval, so its suitability remains reviewable
under the rule above.

## Ledger

| Subscription | Pursuit | $/mo | Billing model | Last confirmed | Status |
|---|---|---|---|---|---|
| TradingView | [d11](d11-tradingview-subscription.md) | $70 | flat | 2026-08-21 | confirmed |
| Databento | [d12](d12-databento-subscription.md) | $0 recurring after retirement | unsubscribed; final invoice/usage charges unverified | 2026-09-10 (operator report) | retired; excluded from active recurring total |
| Fly.io | [d13](d13-flyio-subscription.md) | — | — | asked 2026-08-21, not supplied | **still open** |
| CrossTrade | [d14](d14-crosstrade-subscription.md) | $50 | flat | 2026-08-21 | confirmed |
| Tradeify | [d15](d15-tradeify-account.md) | — | account-carrying cost, not a subscription fee | asked 2026-08-21, not supplied | **still open** |
| Cursor Ultra | [d16](d16-cursor-subscription.md) | excluded | removed from recurring spend by operator; **surface retired outright 2026-09-15** ([worker-surface allocation](../adr/2026-07-14-cc-cursor-surface-allocation.md), Revision 2026-09-15); **fully terminated, no final or prorated charge** (operator, 2026-09-15); cancellation date **still not supplied** | 2026-09-10 (spend), 2026-09-15 (surface; terminated / no final charge) | removed from active recurring total; terminated |
| Claude Max | [d17](d17-claude-max-subscription.md) | $100 | flat | 2026-09-10 | confirmed |
| Codex | [d18](d18-codex-subscription.md) | $200 | monthly amount supplied; plan details unspecified | 2026-09-10 | operator-confirmed |
| GLM Max 5x | [d19](d19-glm-subscription.md) | $80 | monthly amount and plan name supplied; billing date unspecified | 2026-09-23 | operator-confirmed |

**Confirmed active recurring monthly total:** $500/mo (five confirmed active rows:
TradingView, CrossTrade, Claude Max, Codex and GLM Max 5x).
Databento is retired and excluded; its effective cancellation date and final invoice
were not supplied. Cursor is removed from recurring spend by operator instruction and the surface
itself was retired on 2026-09-15; the operator confirmed on 2026-09-15 that the subscription
is fully terminated and that no final or prorated charge landed, but the cancellation date
itself was not to hand and remains open. Fly.io and Tradeify remain
unverified, not zero. Do not read $500 as total spend or as settlement of outstanding
charges.

**Change log**

| Date | Change |
|---|---|
| 2026-10-12 | Operator keeps CrossTrade (d14, $50/month) while Tradeify-route work is deferred (verbatim "5 keep"). No amount changes; the d11–d18 reconfirm stays owed. |
| 2026-09-23 | Operator reports GLM Max 5x at $80/month, replacing the retired Cursor subscription (d16, already excluded). Added as [d19](d19-glm-subscription.md). Active recurring total: $420 + $80 = $500. The report does not reconfirm rows d11–d18; that 2026-09-21 reconfirm remains owed (STATE Monthly trigger). |
| 2026-09-15 | Operator settles two of the three outstanding Cursor items, asked directly: subscription **fully terminated**; **no final or prorated charge** landed after cancellation. The cancellation date was not to hand and **remains open** — 2026-09-10 stays a report date, not a cancellation date. Ledger effect: **none** ($420 unchanged; the row was already excluded). |
| 2026-09-15 | Cursor retired as a worker surface repo-wide (operator instruction; [ADR revision](../adr/2026-07-14-cc-cursor-surface-allocation.md)). Ledger effect: **none** — the row was already excluded from the active recurring total on 2026-09-10. Cancellation date and final charges remain outstanding operator items; this row records the surface retirement, not a settlement. |
| 2026-09-10 | Operator removes Cursor from recurring spend, revises Claude Max from $200 to $100/month, and adds Codex at $200/month. Active recurring total: $520 - $200 - $100 + $200 = $420. Claude remains active. Cursor cancellation date/final charges and Codex plan details not supplied. |
| 2026-09-10 | Operator reports Databento retired/unsubscribed, no replacement approved. Removed prior $200 from active recurring total: $720 to $520. Report date is not an asserted cancellation date; final invoice and historical billing-model tension remain unverified. |
| 2026-08-21 | Ledger created — five figures operator-confirmed, one flagged (Databento billing-model tension), two still open (Fly.io, Tradeify). Closes GSUB-1 C-1. |
