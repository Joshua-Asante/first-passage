# Proposal: a shorter path for deploying a new strategy on the owned Select 100K (2026-11-08)

**Status: Proposed. Decides nothing until Joshua rules on each item.**

**Question.** If research admits a new strategy (a third leg, or a replacement for ORB or Aegis), what
must it pass before its first attended eval session? No standing checklist exists: the
[11-05 bare-bones path](https://github.com/Joshua-Asante/first-passage/blob/b7eaff7/docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-11-05--bare-bones-eval-path)
and the [11-08 sitting rulings](2026-11-08-sitting-rulings.md) D1, D3 and D6 were ruled for ORB + Aegis only.

**Decision it changes.** Which steps the next strategy repeats, and in what form. Nothing here
applies before the pair's first session completes ([STATE](../../STATE.md) priority rule, 11-07).

**Method.** The coordinator listed the steps the pair actually went through. Codex reviewed them
read-only on 11-08 against the [design spec](../spec/2026-11-06-orb-aegis-eval-build-design.md), the
[attended-session procedure](../spec/2026-11-07-orb-aegis-attended-session-procedure.md), the
[stop-rule registration](../briefs/pre-registration/2026-10-31-tradeify-forward-stop-rule-registration.md)
and the private eval-build records. Each item keeps a requirement only where it names a failure that
happened, or a rule that requires it. The coordinator checked Codex's citations.

## The proposed path

1. **Admission (research).** One frozen research verdict from pre-registered gates with honest K;
   in-sample evidence admits. Venue fit in one check against existing facts (flat by 16:45 ET, no
   weekend hold, drawdown, instrument allowed, native logic only). Contribution to the book's
   per-session Sharpe, with correlation, reported beside the verdict, not as a new threshold.
2. **Native port.** Claude Code, privately in the primary checkout. One offline parity comparison
   against the research version.
3. **Spec delta, not a new spec.** Inherit spec rows B6–B15 and the account-level procedure unchanged.
   Review only the new leg's B2–B5: own instrument and start-flat, cap share with the whole active set
   at most 80 micros, protection sized to fill including partial fills, scheduled exit and calendar.
   A replacement on an instrument another leg already trades must resolve B2 explicitly. The procedure
   names an active-leg list instead of the two legs, and keeps "disable all first".
4. **One combined Sim101 run.** The new leg runs with the live legs once, exercising its exit, its
   protection and the operator fallback. A solo run only to diagnose a failure. Joshua accepts it.
5. **One release packet.** Source review and freeze, Tradeify send, eval build, H0–H3, stop-rule
   registration, account binding and the signed page are one packet with one readback. Each distinct
   check stays; repeated captures go. The pre-session check reads the packet.
6. **Session GO.** One GO per session; Joshua attends and enables.
7. **Measure.** Score under the stop rule before the next session.

## Rulings asked

| # | Proposal | What it replaces | Why |
|---|---|---|---|
| P1 | One combined Sim101 run; solo only to diagnose | Solo run, then a combined run | Largest saving. S-PAIR was a combined run and surfaced the pair's run-time misses (the P-3 exit, the connection readback); the rejected-stop stall came from source review, which stays |
| P2 | One release packet for steps 4, 6, 7, 8 | Separate freeze, send, build, registration and page rounds | Second-largest saving; same checks, one readback |
| P3 | Spec and procedure delta: review only new-leg behaviour | Re-deriving B1–B15 per leg | B6–B15 are account rules that do not change with the leg |
| P4 | Delete the general no-trade rehearsal; rehearse only runtime paths existing evidence has not run | A no-trade rehearsal per leg | The pair's rehearsal exists because H2 stops at Aegis's permit check (eval sheet item 9), a blind spot specific to Aegis |
| P5 | Contribution and correlation reported beside the verdict, no extra threshold | An implied deployment threshold | No ruling owns a per-leg threshold; the 0.25 book target gates more accounts, not this eval |
| P6 | Add: the response to a close wait with no timeout goes in the existing incident procedure | Nothing (gap) | Codex's final review: a close can wait indefinitely while the watcher shows `RUNNING`. No new gate |

## What still applies to a new strategy, unchanged

- Its own evidence case or a named waiver (sitting D1 waived it for the pair's first attempt only).
- A new account binding signed with build hashes (D3 binds only Aegis and ORB), and a new stop-rule
  registration, since a composition change after session 1 needs one (D6).
- Re-send to Tradeify on any eval-build change (D6). No agent places eval orders while D8 holds.
- DD-tier admission (re-MC, regime gate, admitting ADR) before any scaling (D3).
- Rules 10–15, the money controls, Tradeify and venue terms. P1–P6 share checks and records but do
  not weaken any of them.
- More accounts only at in-sample book per-session Sharpe of at least 0.25, each with its own GO
  (scaling ruling 10-30, addendum 3, private; confirm locally).

## Correction to the review

Codex reported the 0.25 target as having no owner. It has one: Joshua's 11-02 ruling, "Yes, in-sample
0.25", in the private addendum 3 to the 10-30 scaling ruling.
