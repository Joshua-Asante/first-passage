# STATE-POLICY — CLOSURE: `RESOLVED` (P2 RUN + COMMISSION-FRONTIER)

**Verdict:** `RESOLVED` (P2) — Q-EVALSEQ-1 un-dormed for scoring at the incumbent; frozen K=4 run licensed; policy-frontier measurement commissioned (named, not opened)
**Closed:** 2026-08-16
**Lane:** UNASSIGNED
**Pre-registration:** [packet §6/§8](../programs/2026-08-16-state-policy-scoring-review.md) — §6 table frozen at the packet's commit; no separate pre-reg file
**Spend / K:** $0 at close · the licensed run consumes Q-EVALSEQ-1's own frozen K (K_intrinsic = 3 non-control policies, banked in its prereg §6) when it fires · no Pine / TV / arming
**Live effect:** none — scoring is simulation; no deployment surface touched
**Artifacts:** [packet](../programs/2026-08-16-state-policy-scoring-review.md) · [Q-EVALSEQ-1 prereg](../pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md) · [b5](../../pursuits/b5-q-fundpol-1.md)

---

## 1. Verdict (§6 asserted)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` (P0 KEEP-DORMANT) | Operator marks **P0** | not marked | — |
| `RESOLVED` (P1 RUN-AS-FROZEN) | Operator marks **P1** | subsumed by P2 | — |
| `RESOLVED` (P2 RUN + COMMISSION-FRONTIER) | Operator marks **P2** | Operator: "P2 + GO" 2026-08-16 | ✓ |
| `FALSIFIED` | MC fired pre-mark / family edited / schedule recommended / read as deployment | none | — |
| `AMBIGUOUS-HOLD` | Dated deferral | not deferred | — |

Quoted frozen row: *Operator marks **P2** → `INTEGRATE` — P1, **plus** commissions (names, does not open) a fresh measurement-only campaign extending the seed-target frontier with the same four policy shapes.*

## 2. What the mark licenses, exactly

1. **Un-dorm stamp** on the Q-EVALSEQ-1 prereg header (amendment-first; frozen §6 body byte-untouched) — landed alongside this closure.
2. **The frozen run:** recover the `gap_stage*` harness from tag `pre-prune-2026-08-08`, verify it against its own `assert_anchors.py` / RESULTS anchors **before** extending, add the four frozen policies with no grid and no fifth policy, run the bounded MC on the incumbent geometry, apply DSR/placebo to best-of-K and the both-halves split at read, and close Q-EVALSEQ-1 under **its own frozen §6** (RESOLVED adopt-eligible / FALSIFIED lever-spent / AMBIGUOUS power-short). A faithfulness gate precedes the frozen read: if the recovered harness does not reproduce its recorded anchors, stop and repair before any policy number is looked at.
3. **The commissioned frontier campaign:** named `Q-POLFRONT-1` — policy-augmented extension of the [seed-target frontier](../../lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/RESULTS.md) over synthetic `(w, b, r, k, d)` cells with the same four policy shapes; measurement-only, $0, no manifest; **a fresh brief is owed before any run** — this closure names it and opens nothing.
4. **b5 renewal (elected with the mark, per the packet's §7 conditional):** Q-FUNDPOL-1's PARK renews once; wake condition corrected to "Q-POLFRONT-1 positive on funded-relevant cells OR a candidate reaches funded-phase modeling"; new expiry 2027-02-08.

## 3. What this closure does NOT license

- Deploying, arming, or Striker re-entry in any form — scoring is simulation on a panel.
- Editing the frozen K=4 family, adding policies, or recommending a schedule before the run's own gate reads.
- Reading a policy PASS as an N-SURV admission for any candidate, or as clearing the FTA "consistent trading sizes" live-compliance surface.
- Opening Q-POLFRONT-1 without its own brief.
- Loosening bust ≤ 3.0% / P(pass) ≥ 50%, or reopening the declined eval-sprint lane.

## 4. Defects found in the frozen packet

None found at mark time.

## 5. Lesson candidates

Below the bar — watch: a Board packet whose §7 carries a conditional sibling election (b5) needs the mark to state whether the conditional fired; "P2 + GO" accepting the written recommendation did, and this closure records it explicitly rather than by inference.

## Iterate — loop exit

- **Verdict used:** `RESOLVED` (P2)
- **Model update:** the dormancy ground was venue-scoped and lapsed with S1; the scheduling lever is now measurable under the estate's own frozen instrument; constant-policy N-SURV numbers stop being the unexamined ceiling the moment the run reads.
- **Next:** INTEGRATE
- **Routing:** (i) un-dorm stamp + frozen run (this session's licensed work, faithfulness gate first); (ii) Q-POLFRONT-1 brief authored before any frontier run; (iii) b5 renewal stamp; (iv) deep-iteration charter GO recorded on its own ADR (sibling election, same session)
- **Entry packet:** Q-EVALSEQ-1's own frozen prereg is the entry packet — nothing re-derived here
- **Stop rule / re-proposal bar:** n/a — integrated; the run closes under Q-EVALSEQ-1's frozen §6, and a FALSIFIED there spends the schedule lever (flat WATCH-1 stands) with no θ-retune of the four shapes
- **Board write:** STATE decision index: P2 mark + charter GO lines; briefs INDEX row for Q-EVALSEQ-1 (OPEN, un-dormed). Owner: this closure · [packet](../programs/2026-08-16-state-policy-scoring-review.md)
- **Registry:** n/a — RESOLVED / governance / not a strategy-grounds kill

## §10 audit-hook discharge

```
grep -n "DORMANT 2026-08-04" docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md
# still present (historical stamp) — now followed by the 2026-08-16 un-dorm stamp

grep -n "UN-DORMED 2026-08-16" docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md
# one header hit

grep -n "Q-POLFRONT-1" docs/briefs/INDEX.md
# named (commissioned, not opened)
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-16 | P2 marked; closure recorded; b5 conditional elected | JA · Claude Code |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/STATE-POLICY-closure-resolved-p2.md
python scripts/check_brief.py docs/briefs/programs/2026-08-16-state-policy-scoring-review.md --type inquire
```
