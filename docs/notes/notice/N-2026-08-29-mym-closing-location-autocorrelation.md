# Notice — MYM M15 bar closing-location autocorrelation (unconditional, SIGNAL-EXCESS; cost-law pre-screen run — DROP)

**Notice ID:** N-2026-08-29-mym-closing-location-autocorrelation
**Observed:** 2026-08-29; **cost-law pre-screen run 2026-08-30**
**Author:** Joshua | claude.ai
**Source:** backtest CSV (bar panel) — atheoretical mechanism harvest, MYM Phase 2
**Status:** `DROP` (2026-08-30 — $0 cost-law pre-screen fails the floor cleanly against a provisional basis; see §4/§5)
**Lives in:** `docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md`

---

## §0 — Source anchor

- **Source:** `core/data/bar_data/MYM_M15.csv` (sha256
  `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58`), all 141,467 bars
  (RTH + overnight; last truncated session dropped; further trimmed 347 bars, 0.25%,
  from the front for a fast-FFT-friendly length — disclosed methodology detail, not a
  selection choice). Script:
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c5_closing_location.py`. Results:
  `.../c5_results.json`.
- **Observed at:** 2026-08-29 (this session).

---

## §1 — The observation

CLV_t = (close_t − low_t) / (high_t − low_t) — where within its own H–L range each M15
bar closed. Lag-1 Spearman autocorrelation of CLV, unconditional on level, session
anchor, or vol regime: **obs = −0.0370** (n_pairs = 141,119). 95% circular
block-bootstrap CI **[−0.0422, −0.0319]** (entirely negative, does not straddle 0);
halves both negative (older −0.0482, newer −0.0263 — same sign, roughly halved in
magnitude); by-year table negative in **all 7 years** (2020 −0.073 → 2021 −0.053 → 2022
−0.039 → 2023 −0.034 → 2024 −0.029 → 2025 −0.020 → 2026 −0.027) — sign never flips, but
magnitude has been shrinking over the panel's life.

Run through the same independent-series IAAFT normal-scores battery used for candidate 1
(diagnostic gate PASS, rank-ACF mismatch med=0.0034/p95=0.0044, well inside tolerance),
the zero-excess-mechanism surrogate band itself sits at **mean −0.0346** (not centered on
0 — CLV's own marginal + linear-ACF structure already implies *some* negative serial
correlation, plausibly from the ordinary OHLC-construction fact that close_t and the
next bar's open/low are mechanically related). The observed −0.0370 sits at the **0th
percentile** of that band (p_two_sided = 0.0050) — the real effect is reliably *more*
negative than what linear-ACF reproduction alone predicts. **This is the strongest
statistical finding of the five-candidate batch: SIGNAL-EXCESS**, not SIGNAL-GENERIC.

**Verdict-logic correction, mid-session:** the script's presence gates were first written
assuming a *positive*-persistence claim (mirroring candidate 1's framing) and initially
mis-scored this negative result as NULL; caught and fixed to be sign-agnostic (every
limb must agree with obs's own sign, not a hardcoded positive) before any verdict was
recorded. A separate JSON-serialization bug (numpy bool vs. Python bool) was also fixed.
Both fixes are in the script as committed; the numbers above are unaffected — the bugs
were in verdict bookkeeping and the record step, not the computation itself.

## §2 — Why it stands out (the N signal)

- **Baseline:** an unconditional shape statistic with no prior score anywhere on any
  instrument in this repo.
- **Delta:** real, sign-stable across 7 years and both halves, and statistically in
  excess of what the series' own linear ACF explains (p=0.005) — the only SIGNAL-EXCESS
  result in this batch, versus candidate 1's SIGNAL-GENERIC and candidates 2–4's
  DROP/HOLD non-findings.
- **Frequency check:** first instance; no prior work on `bar-closing-location-autocorrelation`
  anywhere in the repo.

## §3 — Candidate mechanisms (informal)

- Ordinary intrabar microstructure bounce (Roll 1984-style bid-ask bounce reasoning,
  applied to within-bar shape rather than close-to-close returns) — plausible but not
  verified here; would need order-flow data to confirm, which this Notice-phase screen
  does not reach for per the discovery skill's "explanation is deferred" rule.
  Consistent with the magnitude shrinking over the panel (spreads/tick-relative-noise
  have compressed on many CME micros over 2020→2026 as liquidity matured).
  Could also be noise dissolving over time and the earlier years are simply noisier
  (also consistent with the by-year shrinkage) — the two readings are not distinguished
  by anything measured here.
- If real and exploitable rather than a pure microstructure artifact, the natural next
  cheap check (not run this session) is whether ρ≈−0.037 clears any plausible cost
  hurdle at M15 hold times before anything else — per this program's own standing
  lesson (`lesson_cost_law_pre_screen_mr_fade`), a correlation this small at this
  granularity is a strong prior toward failing a cost-law pre-screen even where the
  statistical signal itself is genuine.

## §4 — Routing decision

**DROP (2026-08-30, superseding the original HOLD below — the $0 cost-law pre-screen this notice's own §3/§5 named has now run).** Script: [`c5_clv_cost_screen.py`](../../../lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c5_clv_cost_screen.py). Same design as MNQ's sibling screen: unconditional whole-sample CLV_t deciles (P10=0.0909, P90=0.9189); forward 1-bar real return close_t→close_{t+1} in bp; fade direction set by the data's own sign. Result: top-decile lift −0.3245bp, bottom-decile lift +0.3968bp, combined implied gross edge **+0.3609 bp/event**, 95% block-bootstrap CI **[+0.2328, +0.4835]** (n_events=28,668) — real and statistically distinguishable from 0 (unlike MNQ's sibling result), but still roughly **18× below** MYM's own #M6 hurdle (**6.57 bp/event, provisional** — Tradeify de-scoped, pending F3 re-pricing). Even reading the hurdle at its last-known, pre-de-scope basis, the implied edge does not come close. **This clears ADR §4 D2** (pre-screen fails cleanly on both instruments): DROP per that ADR, no Pre-Q authored. If a future re-priced #M6 hurdle ever falls below ~0.4bp (implausible for any live venue), this specific disposition would need revisiting — flagged, not expected.

~~**HOLD until $0 cost-law pre-screen runs.** (original, struck 2026-08-30 by the pre-screen result above)

Reason: the underlying statistic is real and worth taking seriously (not a DROP-worthy
non-finding, unlike candidates 2–4), but neither GRADUATE nor DROP is the honest call
until the cheap pre-screen this notice's own §3 already named has actually run.~~

**Admission-route status — resolved by [`docs/adr/2026-08-29-clv-autocorrelation-admission-route-scope.md`](../../adr/2026-08-29-clv-autocorrelation-admission-route-scope.md) (`Proposed`, pending re-ratification after a same-day correction — see that ADR's Change history).** Of the three readings §5 originally sketched, the ruling lands closest to (b): a bar-shape statistic with no entry rule attached does not trigger the raised bar's admission gate — that gate fires at Pre-Q admission for an actual directional-timing *candidate*, which this is not yet, so no route decision is owed to keep recording it in a Notice-log. The ADR goes further than "outside scope" alone, though: it also pre-rules the routes for *if* this becomes a candidate. Reading (a) (Route 1) is **plausibly open, corrected from this notice's own original "weak" read**: CLV's mechanism (bar-shape mean-reversion) sits outside the raised bar's three specifically-mapped cost-re-derivation axes (price / instrument-selection / hold-time), independent of and in addition to Route 3 — the ADR's own initial draft made the same "weak" mistake this notice did, by testing only against the 2026-08-10 ADR's one temporal-selectivity worked example rather than the mapped-lever definition itself, and was corrected after ratification was withdrawn. Route 2 does not apply (same OHLCV modality). **Route 3 (beat `ORB-MNQ-1` net-of-cost, not merely clear the cost floor) remains separately available** if this is ever converted into an entry construct. Route 1 eligibility still requires full G0 discipline (adversarial review, `K_intrinsic`, the F2 guard) — it is a scope reading, not a clearance. The mean-reversion/fade flavor this notice flagged is exactly why the ADR leans on the standing `lesson_cost_law_pre_screen_mr_fade` discipline for the concrete next step — see the updated §5 below.

---

## §5 — DROP disposition (was: "If HOLD: re-check trigger")

**N/A — superseded 2026-08-30, ahead of the 2026-11-08 outer bound.** The drop trigger below fired; there is no re-check.

~~- **Re-check date:** 2026-11-08 as an outer bound (rides the standing §4 falsifier
  hard-date already on the calendar for other programme items, per `CLAUDE.md`'s
  prop-portfolio §4 line — not a new date invented for this notice); the pre-screen
  below is the preferred, earlier trigger and does not need to wait for that date.
- **Trigger condition:** the admission-route question itself is resolved (see §4 above;
  Route 1 is also plausibly open, independent of Route 3) — the remaining gate is the $0
  cost-law pre-screen: convert ρ≈−0.037 into a decile-conditioned expected-value read and
  check it against MYM's own cost hurdle (`MYM.md` #M6, ≈6.57 bp/event — **provisional
  only**, pending F3 re-pricing since Tradeify was de-scoped; a pass/fail here is against
  the last-known basis, not a final MYM verdict). This is a necessary-condition-only floor
  check, per the admission-route ADR's corrected 2-C — it does **not** by itself graduate
  this to a Pre-Q. The full Route 3 comparison against `ORB-MNQ-1`'s own net-of-cost edge
  (+0.0626R/trade) needs an actual entry/exit construct to compute a comparable R-figure
  (bp/event and R-per-trade are not the same unit), which does not exist yet for CLV —
  that comparison is deferred until such a construct is built.
- **Drop trigger:** the $0 cost-law pre-screen (mean |gross edge implied by ρ≈−0.037| vs.
  the MYM cost hurdle, `MYM.md` #M6, read as provisional per above) run before the
  re-check date and failing cleanly.~~ — **fired**: +0.36 bp/event vs a 6.57bp hurdle,
  ~18× short even at the provisional (possibly overstated) basis.
- **Calendar entry:** none set; operator to set if desired.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c5_closing_location.py
# Expected: observed lag-1 Spearman rho = -0.0370, CI=[-0.0422,-0.0319], VERDICT: SIGNAL-EXCESS

# Reproduce the $0 cost-law pre-screen (2026-08-30 DROP disposition)
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c5_clv_cost_screen.py
# Expected: implied gross edge +0.3609 bp/event, CI=[+0.2328,+0.4835], vs M6 hurdle 6.57bp -- CLEARS=False

# Confirm no Pre-Q was opened for this DROP (per ADR §4 D2)
grep -rln "N-2026-08-29-mym-closing-location-autocorrelation" docs/briefs/Q-*.md
# Expected: empty
```

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md --type notice
# Expected: RESULT: well-formed
```
