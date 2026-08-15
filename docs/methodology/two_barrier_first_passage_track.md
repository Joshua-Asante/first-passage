# Track: two-barrier first-passage theory for stop/target win-rate achievability

**Status:** ACTIVE — Session 0 (this doc) only. No theory session has run yet.
**Started:** 2026-08-13, on operator direction ("let's start a research track... this
may be a multi session research track to fill in the gaps of our internal knowledge
that can help with passing the Tradeify eval").
**Scope:** $0 / K=0. Doc + charter only — no candidate scored, no gate moved, no
capital or account action, no MSL card touched.

## Why this track exists

Session 2026-08-13 closes the account-level half of "first-passage theory" as a
standing knowledge gap — but not by building it fresh. `lab/analysis/mc/mc_mdd_closed_form_2026-08/`
(merged via PR #790, earlier the same day) already implements Magdon-Ismail et al.
(2004)'s closed-form continuous-time drawdown distribution and validates it against
the paper's own Appendix B table and against `simulate_path` in the fine-discretization
limit. This session's own independent attempt at the same closed form was caught as a
near-duplicate by the `lab/CATALOG.md` freshness gate and reworked rather than landed —
a second dedup-sweep miss in this same session (after the eval-passing battery near-miss
below), which prompted a separate repo-wide investigation into why this keeps recurring
(2026-08-13, not yet landed as of this doc's writing — check `docs/adr/` and
`docs/operational_rules.md` for a dated follow-up before assuming this paragraph is
current). What this session actually added, folded into that existing study rather than
a competing directory: [`intraday_realistic_grid.py`](../../lab/analysis/mc/mc_mdd_closed_form_2026-08/intraday_realistic_grid.py),
which tests `simulate_path`'s `intraday_low` mechanism at realistic ~20-60 *business-day*
granularity (the existing study only tested fine 2000-5000-substep convergence) —
finding the repo's EOD-only bust-rate convention captures only ~74-86% of Tradeify's
own documented-rule bust probability. See
[`RESULTS.md` §Realistic-granularity extension](../../lab/analysis/mc/mc_mdd_closed_form_2026-08/RESULTS.md).

The same session surfaced a sharper, currently-unresolved question one level down, at
the *trade* level. MSL's population-data note
([`docs/notes/notice/N-2026-08-13-external-eval-population-data.md`](../notes/notice/N-2026-08-13-external-eval-population-data.md)
§7.5, §9-10) found that observed real-world Tradeify/Topstep passers cluster
bimodally — low-win-rate/2-3R-with-a-hard-stop, or high-win-rate/tiny-target/**no
stop** — with **zero observed passers in the high-win-rate-with-a-hard-stop region**,
which is exactly where the frozen MSL candidate C1 (MYM PDH/PDL failed-break reclaim,
`rr=1`, hard stop, break-even WR ≈ 50.9% per the sprint-lane note's own arithmetic)
sits. The operator ruled the hard stop stays regardless (a tail-risk preference, not a
data dispute — see the population note §10 ruling #3) — but *why* that region is
empty, and whether a hard-stop construct can be designed to clear break-even anyway,
is flagged in that note as "worth stating... not established." This track exists to
turn that from a flagged hypothesis into an analytically-grounded answer, using the
same class of mathematics (first-passage theory for a drifted diffusion) already
proven out at the account level, applied one level down at the single-trade level.

**⚠ Update 2026-08-13, same day, later.** C1 explored and closed **FALSIFIED**
([`closure`](../briefs/closures/MSL-C1-closure-falsified.md), both arms CI entirely
< 0, ≈ −0.18R/−0.11R). The failure mode was **outright negative edge**, not a
close-run break-even-WR-vs-hard-stop margin — simpler and more mundane than the
theoretical question this track was chartered to answer, and this track's math was
not needed to explain it. C2, the C3 dual-axis revival, and S2A explored the same
day and also closed FALSIFIED (C2/C3-K2 on negative-edge CI; S2A on a different axis,
construction-level trade frequency below its own N-ACT bar). **This track's
motivating candidate no longer exists** — but its purpose doesn't evaporate with it;
it *sharpens*. Five explore-GOs were just spent to learn "negative edge" the
expensive way, one per candidate. The standing value of Session 1's two-barrier math
is exactly this: a **pre-screen** that could rule an obviously-doomed hard-stop
geometry out (or in) for a fraction of an explore-GO's cost, before the next slate's
cards are authored — post-mortem-for-C1 was never really the point. Session 1's
scope (§ below) is unchanged; only the "why now" framing is corrected.

## Scope decisions (already made, don't re-litigate without a reason)

- **Narrow, not broad.** Two-barrier (stop-vs-target) hit-probability theory, scoped
  tightly to the win-rate-achievability question above. The wider curriculum this
  connects to (optional stopping theorem, Wald's identity, sequential probability
  ratio tests, barrier-option-pricing parallels) is explicitly deferred — worth
  returning to if this narrow track proves valuable, not a prerequisite for it.
- **Independent of MSL's governance.** This track does not route through MSL's plan
  §6 claim manifest or its orchestrator-only-writes discipline — it is theory-building
  that produces evidence MSL can cite, not a candidate-scoring activity MSL owns.
  Findings that bear on C1 specifically should be handed to MSL as a citation, not
  written into MSL's own artifacts by this track.
- **Theory-then-artifact, every session.** Each session builds genuine understanding
  of a piece of the math *and* immediately operationalizes it into a repo-native,
  falsifiable artifact — neither half skipped, per session-start's explicit
  direction.
- **Synthetic/validated-first, real data later.** Follows the pattern that worked for
  the account-level track: validate the closed form against a known/independent
  reference before touching anything real. Real price data (MNQ around C1's PDH/PDL
  trigger) is Session 3+, gated on Sessions 1-2 actually producing something useful.

## Session plan

| # | Target | Status |
|---|---|---|
| 1 | Build and validate the two-barrier (stop-vs-target) first-passage hit-probability formula for a drifted diffusion. Apply it two ways: (a) given a hypothesized entry-signal edge, what win rate is achievable at C1's `rr=1` hard-stop geometry, against the measured ~50.9% break-even; (b) same formula with the stop pushed far out, to test the "does removing the stop mechanically inflate win rate" hypothesis directly, and by how much, as a function of edge. | **Not started** |
| 2 | Feed Session 1's trade-level output (win rate, payoff ratio, implied skew of the resulting P&L stream) into `lab/analysis/mc/mc_mdd_closed_form_2026-08/closed_form.py`'s `g_d` (the repo's existing, PR #790 account-level closed form — do not reimplement), producing an end-to-end pipeline: *given a hypothesized signal edge and a stop/target choice, predict account-level survival* — usable on C1 MYM or any future candidate before spending an explore-GO. | Not started, blocked on 1 |
| 3+ | Apply the validated Session 1-2 machinery to real price data around C1's actual PDH/PDL trigger (or another candidate's real trigger), replacing synthetic drift/vol assumptions with measured local values. Needs real market data (databento/TV exports) — cost-gated, bigger lift, only worth it once 1-2 prove the approach useful. | Not started, gated on 1-2 |

## Known adjacent infrastructure (read before rebuilding anything)

Surfaced by a repo sweep before this doc was written — read before treating any of
this as a fresh problem:

- [`docs/methodology/1r_estimation.md`](1r_estimation.md) — existing convention for
  estimating "1R" (typical loss size) from realized CSV backtests, including an
  MAE-based estimator for strategies with active exit management. Adjacent to but
  distinct from this track's question (that doc estimates realized risk for MC
  *normalization*; this track predicts achievable win rate *before* a backtest
  exists) — read it before designing a new MAE-based estimator here, the pattern may
  transfer.
- [`lab/analysis/c1/mnq_stop_distribution_2026-08-02/RESULTS.md`](../../lab/analysis/c1/mnq_stop_distribution_2026-08-02/RESULTS.md) —
  a real stop-distance measurement study on the (withdrawn) MNQ book, and its own
  hard-won methodology lesson: *"I built an estimator from realized outcomes when a
  direct computation of the governing formula already existed in the repo... Search
  for the oracle before constructing a proxy."* Apply this directly to Session 3+ —
  check whether a direct computation of C1's PDH/PDL trigger's expected excursion
  already exists (e.g. in `lab/analysis/c1/mnq_tnec_con*_2026-08/` construct-G0
  harnesses) before building a fresh empirical estimator.
- [`lab/analysis/mc/mc_mdd_closed_form_2026-08/`](../../lab/analysis/mc/mc_mdd_closed_form_2026-08/) —
  the repo's existing account-level closed form (`closed_form.py::g_d`) and validation
  methodology (Appendix B cross-check, `simulate_path` fine-grid convergence test),
  extended this session by [`intraday_realistic_grid.py`](../../lab/analysis/mc/mc_mdd_closed_form_2026-08/intraday_realistic_grid.py)
  (exact Brownian-bridge intraday sampling at realistic business-day granularity).
  Their `g_d` implementation does **not** use series acceleration (plain truncated sum,
  200-term cap) and was validated against a small toy-scale grid (`sigma≈1, h≈2-3`);
  this session's cross-check ran it directly at real Tradeify-dollar scale
  (`h=$3,000, sigma=$400`) and it agreed closely with an independently-built,
  Euler-accelerated implementation at that scale — reassuring, but if a future session
  needs `g_d` at a very different (extreme small-x, or very large-|mu|) parameter
  region, check for the same slow-convergence/overflow failure modes this session's own
  (now-deleted) `magdon_ismail_drawdown.py` had to solve — deleted pre-commit
  during this session, so it never entered git history and is not retrievable
  via `git log`; see this track's Session 1 for a fresh derivation if needed. The
  two-barrier problem is a different, more classical closed form, but the same
  validation discipline (check against an independent published/derived reference
  before trusting the engine, watch for numerical-precision walls at extreme
  parameters) applies directly.

## Session log

- **2026-08-13** — Track chartered. No theory session run yet.
