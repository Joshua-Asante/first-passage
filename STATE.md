# STATE — First Passage

**Updated:** 2026-11-06. Keep this to one page: the goal, live obligations, open
decisions. Replace stale lines instead of appending history.

## Goal

Get a native NinjaScript strategy trading the **Tradeify Select 100K evaluation**,
then scale within Tradeify. The candidate is the ORB MNQ v7 + Aegis pair.

- **Stage:** 5 of 5, Verification, on the
  [11-05 bare-bones eval path](https://github.com/Joshua-Asante/first-passage/blob/b7eaff7/docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-11-05--bare-bones-eval-path).
  Stages: 1 Ideation, 2 Validation, 3 Definition, 4 Creation, 5 Verification, then
  measure. A private build (S-PAIR) exists, and the source went to Tradeify on 11-05.
  The [design spec](docs/spec/2026-11-06-orb-aegis-eval-build-design.md) is accepted
  (11-06) and amended: tested source plus two ORB fixes. The
  [attended-session procedure](docs/spec/2026-11-07-orb-aegis-attended-session-procedure.md)
  is accepted (11-07). **Next: the F rehearsal** (procedure §10): Joshua runs it in this
  week's preservation trade (MNQ, about 16:15 ET, not 11-11) plus a Sim101 disable
  timing, then derives the hard latest trigger on the signed page. Then: a short
  Sim101 check; Joshua sends Tradeify the eval files; the signed page and pre-session
  check; then a session GO.
  The first session does not wait for Tradeify's source-review reply.
- **New candidates** are allowed again: Joshua overturned the one-candidate bar on
  2026-11-06. Whether its limits on new instruments and builder rounds also fell is
  unconfirmed. The private port is built and changed by Claude Code in Joshua's
  primary checkout.
- **Status:** Joshua accepted S-PAIR on 11-06; it is not a pass as frozen. His 11-06
  GO covers the eval build only: no order, session or spend. No sizing or deployment
  is approved, and every session needs its own GO.
  The [native plan](docs/superpowers/plans/2026-10-21-tradeify-native-ninjascript-strategy-plan-DRAFT.md)
  and the [qualification framework](docs/briefs/pre-registration/2026-10-26-tradeify-native-lane-prereg-DRAFT.md)
  are drafts that the 11-05 path does not wait on.
- **Known risk:** no configuration has an evidence case for this evaluation yet, and
  no strategy-signal fill has ever occurred on the account.
- **Ruled out:** the multi-firm program is research-only (its falsifier fired). The
  external Python rail and the personal account lane are closed.

## Live obligations

| Obligation | Next due | Notes |
|---|---|---|
| Weekly account-preservation trade | Week of 11-09 → 11-13 | One round trip per Mon–Fri week, placed natively. A missed week risks account deletion. Agents may place it under the standing GO. Done for 11-02 → 11-06 (11-04). This week it is the F rehearsal: Joshua places it himself, with the resting stop and flatten-and-cancel exit (procedure §10, within the standing GO). |
| Subscription reconfirm | 11-21 | Joshua reconfirms the [ledger](docs/pursuits/SUBSCRIPTION_LEDGER.md) rows. |
| c1 rail decommission | After the 11-08 sitting | Stages 1–2 done (hosts disarmed 11-03, both Fly apps destroyed 11-05). Rail code removed by PR; S3-4 (`book_policy`, the sizing reference) remains. |

## Open decisions (Joshua)

1. **11-08 sitting:** the remaining decisions before the first eval session.
2. **Data source:** Databento is retired and has no replacement. Research uses
   TradingView CME exports only.
