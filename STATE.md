# STATE — First Passage

**Updated:** 2026-11-07. Keep this to one page: the goal, live obligations, open
decisions. Replace stale lines instead of appending history.

## Goal

Get a native NinjaScript strategy trading the **Tradeify Select 100K evaluation**,
then scale within Tradeify. The candidate is the ORB MNQ v7 + Aegis pair.

- **By role** (owners per [AGENTS.md Roles](AGENTS.md#roles)). Replace a line when its
  objective changes.
  - **Joshua (director, operations):** run the F rehearsal (Tue 11-10), derive the hard
    latest trigger, send Tradeify the eval files, sign the page, then give the session 1 GO.
  - **Research (Claude):** the evidence read on the live pair: re-run the August
    combined-book gate on ORB v7 + Aegis A-0. New candidates only under the priority rule below.
  - **Design (Claude):** keep the spec and procedure current. Next: any change that
    the readback's B10 answer or the evidence read forces.
  - **Engineering (Claude Code, primary checkout):** the S-PAIR readback, including
    B10, before the rehearsal; the c1 untangle, `.gitignore` guard first.
  - **Verification (Codex):** review every head; audit the evidence read; review the
    rehearsal and Sim101 records.
  - **Measure (Claude Code, for Joshua's sign-off):** ready to score session 1 under the
    forward stop rule.
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
  2026-11-06, and on 11-07 confirmed that this covers new instruments and builder
  rounds too. The private port is built and changed by Claude Code in Joshua's
  primary checkout.
- **Priority for new candidates** (Joshua, 2026-11-07): new-candidate ideation and
  research may run only if it uses none of Joshua's attention, no writes or exclusive
  work in his primary checkout, no spend, and nothing that delays the pair's next
  steps. Joshua's time covers discussion, decisions, anything only he can do (eval
  actions, private exports), troubleshooting and private-checkout builds; it excludes
  public reading, public experiments on separate branches, and deferrable decision
  notes. This holds until the pair's first attended eval session has completed under
  the procedure, its evidence is captured, and any incident is dealt with well enough
  to name the next action, unless Joshua reprioritises.
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
