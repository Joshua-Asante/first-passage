# STATE — First Passage

**Updated:** 2026-11-08. Keep this to one page: the goal, live obligations, open
decisions. Replace stale lines instead of appending history.

## Goal

Get a native NinjaScript strategy trading the **Tradeify Select 100K evaluation**,
then scale within Tradeify. The candidate is the ORB MNQ v7 + Aegis pair.

- **Status:** the 11-05 bare-bones eval path governs, as ruled at the
  [11-08 sitting](docs/notes/2026-11-08-sitting-rulings.md). The legs are Aegis A-0
  and ORB O-0. The 10-31 stop rule is the pair's gate, with no pre-session evidence
  case. The draft native plan and qualification framework do not gate it. Next steps:
  S-PAIR rerun, then the eval build installed disabled, the signed page, and a session
  GO no earlier than the Tradeify notice deadline (D6, 11-19 if sent by 11-10).
- **Known risk:** no configuration has an evidence case for this evaluation, and no
  strategy-signal fill has ever occurred on the account. Both are accepted as risk
  for the first attempt (D1).
- **Ruled out:** the multi-firm program is research-only (its falsifier fired). The
  external Python rail and the personal account lane are closed.

## Live obligations

| Obligation | Next due | Notes |
|---|---|---|
| Weekly account-preservation trade | Week of 11-09 → 11-13 | One genuine minimal trade per Mon–Fri week (D9: 1 micro, held minutes, protective stop, RTH, no instance enabled). Joshua places it by hand; agents remind and verify read-only only (D8). A missed week risks deletion after an email warning. Done for 11-02 → 11-06 (11-04). |
| Subscription reconfirm | 11-21 | Joshua reconfirms the [ledger](docs/pursuits/SUBSCRIPTION_LEDGER.md) rows. |
| c1 rail decommission | Open | Stages 1–2 done (hosts disarmed 11-03, both Fly apps destroyed 11-05). Agents remove the rail code by PR. |

## Open decisions (Joshua)

1. **T1** (whether Tradeify accepts the weekly trade's shape) and **T2** (whether an
   agent may operate the account) stay open. Joshua asks Tradeify in writing after
   the first minimal trade (D10). T2 governs the D8 suspension.
2. **Local confirmations for the 11-08 rulings:** the private build ruling (D5), the
   subscriber agreement (D7), the spend ceiling's scope (D11), the 11-05 cadence
   covering eval sessions (D12), and the c1 archive contents (D19).

Data source is settled: TradingView CME exports only, with the terms-of-service risk
accepted (D16).
