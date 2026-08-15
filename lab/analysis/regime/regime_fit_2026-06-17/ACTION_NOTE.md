# Execution-discipline action note — FIX-EXECUTION (Q-REGIME-FIT-1, 2026-06-17)

Disposition from [`RESULTS.md`](RESULTS.md): the strategies are healthy (+17.12% signal-level, INSIDE
the envelope); the live account is −$1,272. **The work is execution capture, not strategy.** This note
distills the measured leaks into pre-trade rules. Each rule is anchored to a dated, dollar-quantified
in-window failure — not a plausibility argument.

## The four leaks, ranked by cost

| # | leak | dated incident | cost (static $200K) | rule |
|---|---|---|---:|---|
| 1 | **Decomposing a single-position hold** | Aegis 04-15: one 12:30 signal (held to +$6,086) executed as three fills (19+11+2 lots), one stopped, others continued → +$362 | **−$5.7K** | When a FIRE alert specifies ONE entry of size N, execute ONE entry of size N. No re-entering on BB touches. (= documented lesson **E2**, fired again.) |
| 2 | **Oversizing + discretionary early exit** | Aegis 05-19: flat +$47 signal taken at 25 lots, exited 7 min later → −$2,300 | **−$2.3K** | Size to the multiplier card, not conviction. Hold to the system's exit; do not hand-close a live position the strategy still holds. |
| 3 | **Skipping a fired signal (deployed leg)** | DJ30 04-17: +$3,144 backtest winner, DJ30 was live, no fill | **−$2.8K** | Take every signal a deployed strategy fires. Skips need a *written* rationale at skip-time (lesson E3); 13 of 13 in-window skips had rationale = MISSING. |
| 4 | **Off-spec discretionary trades** | 04-16 Guardian (−$2.4K) and others with no backtest signal | net +$1.8K but high-variance | Trade only fired signals. Off-system trades are the account's largest variance source even when net-positive. |

## Deployment-completeness (operational, not behavioral)

The single biggest miss — the **04-13/04-14 NAS100 pyramid, +$27.7K = 81% of the window's edge** — was
**un-capturable**: NAS100 v1 wasn't operationally deployed until ~2026-05-07 (first live USTEC fill 05-11).
Not a skip. The lesson is operational: **a locked strategy earns nothing until it is armed live.** Before
the next challenge window, confirm all four legs are armed and alerting (the NAS100 contractValue=10
broker-verify was the gating step that delayed it).

## Pre-trade checklist (derived)

1. All four strategies armed and alerting? (deployment-completeness)
2. Each fired signal → one entry, system size, system exit. No splits, no oversize, no hand-close.
3. Every skip gets a one-line written rationale at skip-time (≤60s; if that's intolerable, the rationale is post-hoc).
4. Zero off-system trades.

## Measurement cadence

The canonical pipeline now parses current exports (the schema-drift fix landed this session), so the
rolling-6-week ECR is runnable weekly:
```
python -m live_journal.scripts.ecr_rolling --asof <date> --dxtrade <fills.csv> \
  --backtest guardian:<g> striker_dj30:<d> striker_nas:<n> aegis:<a>
```
Re-check the edge-captured ratio at the next weekly review. Target: ≥0.70 on a clean (post-deployment,
single-version) window. This window read **negative** — the floor before any new strategy work is a
positive ECR.
