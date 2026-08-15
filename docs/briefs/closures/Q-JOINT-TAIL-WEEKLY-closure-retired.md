# Q-JOINT-TAIL-WEEKLY — closure: RETIRED (§9 panel-shape gate FAILED)

**Status:** `RETIRED` (2026-07-14, at the pre-registered §9 authoring-time sanity gate — before any CC handoff)
**Parent Pre-Q:** [`docs/briefs/2026-05-27-q-joint-tail-weekly-pre-q.md`](../2026-05-27-q-joint-tail-weekly-pre-q.md) (Pre-Q PASS, **conditional on §9**)
**Predecessor:** Q-JOINT-TAIL-1 (closed BLOCKED-RETIRED 2026-05-27 at daily resolution)
**Disposition owner:** the Pre-Q's own §7/§9 branch ("§9 fails → RETURN TO PRE-Q / RETIRE, mirror Q-JOINT-TAIL-1") + roster next-action ("else RETIRE")
**Artifact:** [`lab/archive/q_joint_tail_weekly_2026-07/sanity_check.py`](../../../lab/archive/q_joint_tail_weekly_2026-07/sanity_check.py)

---

## What was tested

The §9 authoring-time panel-shape sanity check: before locking the §2 joint-tail
hypothesis, verify that `n_active = 4` weeks (all four strategies trading in a
Monday-anchored 5-business-day block) are the **dominant** pattern — the assumption
that the weekly-resolution reframe was built on (Q-JOINT-TAIL-1 died at daily
resolution because all-four-active days were 1-in-1141; the wager was that weekly
resolution would make 4-way overlap the norm and the co-failure question
falsifiable).

Aggregation matches the MC engine exactly (`core.mc build_week_blocks`:
Mon-anchored, non-overlapping, 5 business days), over the four canonical 2026-05-24
Pepperstone panels. 227 week-blocks — matching the brief's expected ~227 (aggregation
validated).

## Result (2026-07-14) — both gate limbs FAIL

| Gate limb | Threshold | Observed | Verdict |
|---|---|---|---|
| `n_active=4` dominant overall | > 50% of weeks | **9.7%** (22 of 227) | **FAIL** |
| `n_active=4` in bottom decile of portfolio-week PnL | ≥ 15 of ~23 | **4 of 23** | **FAIL** |

Full n_active distribution over all 227 weeks: `0:5.7% · 1:27.3% · 2:29.5% · 3:27.8% · 4:9.7%`
— the modal week has **two** strategies active, not four. Within the 23 worst
portfolio-weeks the split is `1:6 · 2:9 · 3:4 · 4:4`; the worst weeks are dominated
by one or two strategies, not 4-way co-failure. Even the pre-registered fallback
subset (`n_active ≥ 3`) yields only 8 of 23 bottom-decile weeks — far below the N≥15
the brief requires and the N≥30 primary floor.

Preview (NOT the verdict — the CC investigation was never authored): mean
`n_negative` in the bottom decile = **1.91**, which itself leans toward H0
(concentration-driven, ≤2.0) rather than H1 (joint-tail-present, ≥3.0).

## Disposition — RETIRED (mirror Q-JOINT-TAIL-1)

The four-strategy book is temporally diversified at **both** daily and weekly
resolution. The joint-tail / hedge-need question is structurally non-falsifiable
for this allocation at the weekly scale for the same reason it was at the daily
scale: the worst portfolio-weeks are concentration events, and the verdict subset
(all-four-active bad weeks) is too small (N=4) to power the pre-registered test.

Per the Pre-Q's own §9 disposition, this is the **RETURN-TO-PRE-Q → RETIRE** branch,
not a license to re-pose at a third resolution. INQHIORI §6 (tail-methodology
exhaustion): Q-JOINT-TAIL-1 (daily) and Q-JOINT-TAIL-WEEKLY (weekly) are two
attempts at the same parent question ("does the book co-fail in its tail?") at two
resolutions; both find the question ill-posed for a temporally-diversified book.
No third-resolution attempt without **new mechanism evidence** — a dated incident
of actual 4-way tail co-failure the current machinery would have missed, not a
restated plausibility argument.

The §9-fix lesson (run the panel-shape sanity check at authoring time, before
threshold-locking) is **corroborated**, not spent: it caught a non-falsifiable
framing before any CC handoff was authored — the exact avoidable cycle Q-JOINT-TAIL-1
paid three revisions + a Phase-0 BLOCKED for.

## Re-open trigger

A dated observation of genuine 4-way tail co-failure (a bottom-decile portfolio
week with all four strategies net-negative) that the current temporal-diversification
belt did not anticipate. Absent that, this line stays retired.

## Reproduce

```bash
python lab/archive/q_joint_tail_weekly_2026-07/sanity_check.py
# Requires the four canonical 2026-05-24 Pepperstone panels present locally
# (gitignored vendor data; skips cleanly if absent).
# Expected: 227 blocks; n_active=4 overall 9.7%; 4 of 23 in bottom decile; FAIL.
```
