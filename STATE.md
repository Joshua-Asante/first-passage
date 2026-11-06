# STATE — First Passage

**Updated:** 2026-11-06. Keep this to one page: the goal, live obligations, open
decisions. Replace stale lines instead of appending history.

## Goal

Get a native NinjaScript strategy trading the **Tradeify Select 100K evaluation**,
then scale within Tradeify. The candidate is the ORB MNQ v7 + Aegis pair.

- **Status:** on the
  [11-05 bare-bones eval path](https://github.com/Joshua-Asante/first-passage/blob/a31aabc/docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-11-05--bare-bones-eval-path).
  Joshua accepted S-PAIR on 11-06; it is not a pass as frozen. His 11-06 GO covers
  the eval build only: no order, session or spend. No sizing or deployment is
  approved, and every session needs its own GO. The
  [native plan](docs/superpowers/plans/2026-10-21-tradeify-native-ninjascript-strategy-plan-DRAFT.md)
  and the [qualification framework](docs/briefs/pre-registration/2026-10-26-tradeify-native-lane-prereg-DRAFT.md)
  are drafts the path does not wait on.
- **Known risk:** no configuration has an evidence case for this evaluation yet, and
  no strategy-signal fill has ever occurred on the account.
- **Ruled out:** the multi-firm program is research-only (its falsifier fired). The
  external Python rail and the personal account lane are closed.

## Live obligations

| Obligation | Next due | Notes |
|---|---|---|
| Weekly account-preservation trade | Week of 11-09 → 11-13 | One round trip per Mon–Fri week, placed natively. A missed week risks account deletion. Agents may place it under the standing GO. Done for 11-02 → 11-06 (11-04). |
| Subscription reconfirm | 11-21 | Joshua reconfirms the [ledger](docs/pursuits/SUBSCRIPTION_LEDGER.md) rows. |
| c1 rail decommission | Open | Stages 1–2 done (hosts disarmed 11-03, both Fly apps destroyed 11-05). Agents remove the rail code by PR. |

## Open decisions (Joshua)

1. **11-08 sitting:** the remaining decisions before the first eval session.
2. **Data source:** Databento is retired and has no replacement. Research uses
   TradingView CME exports only.
