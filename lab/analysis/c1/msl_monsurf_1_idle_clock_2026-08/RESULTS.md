# Q-MONSURF-1 M-B acceptance battery — RESULTS

**Verdict:** ACTIVE — `Q-MONSURF-1` M-B idle-clock monitor — `RESOLVED` 2026-08-23: 0 missed / 0 spurious across all 312 real historical weeks, mutation-verified. Registration-ready (gated on F3 only). [closure](../../../docs/briefs/closures/Q-MONSURF-1-closure-resolved.md)
`RESOLVED` (H-MONSURF-1 accepted)
**Date:** 2026-08-23
**Pre-registration:** [`Q-MONSURF-1-verdict-preregistration.md`](../../../../docs/briefs/pre-registration/Q-MONSURF-1-verdict-preregistration.md)
**Cost:** $0 — no new data pulled, no K spent. Re-reads the same committed `daily_panel.csv`
(2026-07-23 vintage) `lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md` already scored,
retrieved read-only from the `pre-prune-2026-08-08` git tag per this repo's own stated retrieval
convention.

## What ran

`acceptance_battery.py` — see [`RUN_LOG.txt`](RUN_LOG.txt) for the full, unedited terminal output.

1. **Panel parse + sanity check.** Fetched `daily_panel.csv` from the pre-prune tag, computed
   per-day activity (`combined != 0.0`), grouped into Mon-anchored business-day weeks. Reproduced
   every anchor `c1_cadence_inactivity_2026-08-02/RESULTS.md` §1 publishes, exactly:

   | Anchor | Published | This run |
   |---|---|---|
   | Business days | 1,556 | **1,556** |
   | Active days | 329 | **329** |
   | Mon–Fri weeks | 312 | **312** |
   | Zero-trade weeks | 82 (26.3%) | **82 (26.3%)** |
   | Weeks with exactly 1 trading day | 45.2% | **141 (45.2%)** |

   Parse confirmed correct before trusting anything downstream (the script `sys.exit(1)`s on any
   mismatch — none occurred).

2. **Mutation test 1 — false-positive class.** Planted a realistic off-by-one bug (`buggy_single_day_lookback`:
   checks only the immediately-preceding business day for activity, not the full week-to-date) and
   re-ran. Result: **380 spurious alerts**, 0 missed — the battery's spurious-detection is
   genuinely sensitive to this defect class, not a vacuous check.

3. **Mutation test 2 — false-negative class.** Planted the opposite defect (`buggy_always_suppressed`:
   lookback always reports "already active," so no alert ever fires) and re-ran. Result: **164
   missed alerts** — exactly 82 breached weeks × 2 checks (T-2 and T-1), confirmed against the
   expected count before accepting the mutation as caught.

4. **The real acceptance run**, frozen (unmutated) lookback rule, against all 312 real historical
   weeks:

   ```
   {'n_weeks': 312, 'n_breached': 82, 'n_missed': 0, 'n_spurious': 0, 'pass': True}
   ```

   **0 missed weeks, 0 spurious alerts, across every one of the 312 real Mon–Fri weeks measured.**
   Every one of the 82 real breached weeks fired both its T-2 and T-1 alert; no alert fired on a
   week that had already satisfied its trade requirement as of that alert's own evaluation point.

## Reading this honestly

This is a full-panel test (312 weeks), not a 13-week "quarter" sample — per the pre-registration's
own §2, this resolves an internal tension in H-MONSURF-1's wording conservatively: a full-panel
pass is a strict superset of any quarter-length slice, so it is the stronger, not the weaker, bar.
It is also, definitionally, a **logic-correctness test of the monitor against known historical
activity data**, not a live-fire test — it says the alerting rule is internally sound and
non-buggy on real data shapes, not that a live deployment will never have a data-feed problem
(e.g., a fill that silently fails to reach the monitor's input). That data-adapter question is
explicitly deferred to Phase 5 (F3 registration), when M-B is wired to the live account's actual
event stream rather than this frozen historical panel.

## What this does NOT license

- Does not wire M-B to the live account, `ops/c1_rail/`, or any M1 EventLedger schema — standalone
  by design (parent brief §5), unchanged.
- Does not rule on M-A's build-gate scope question (does "first live fill" bind a pure market-data
  observer?) — still an explicit, unanswered operator ruling per the parent brief §1/§5.
- Does not touch M-C — still correctly gated on first live fill, untouched.
- Does not re-freeze idle-clock semantics against a specific successor venue — this run uses the
  Tradeify-shaped provisional freeze (pre-reg §3) pending Q-VENUEGEO-1's DP2 sweep, exactly as the
  parent brief's intake amendment specified.
