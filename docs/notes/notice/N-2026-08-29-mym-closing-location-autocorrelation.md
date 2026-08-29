# Notice — MYM M15 bar closing-location autocorrelation (unconditional, SIGNAL-EXCESS)

**Notice ID:** N-2026-08-29-mym-closing-location-autocorrelation
**Observed:** 2026-08-29
**Author:** Joshua | claude.ai
**Source:** backtest CSV (bar panel) — atheoretical mechanism harvest, MYM Phase 2
**Status:** `HELD until 2026-11-08`
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

**HOLD until 2026-11-08.**

Reason: the underlying statistic is real and worth taking seriously (not a DROP-worthy
non-finding, unlike candidates 2–4), but — **exactly as flagged before this candidate was
run** — its admission-route status under the 2026-07-21 single-instrument index-futures
directional-timing raised bar (`docs/rejected_candidates.md`) is genuinely unresolved,
not something this session is positioned to rule on its own authority. The finding is a
bar-SHAPE statistic (distinct from every level/breakout/continuation construct in the
raised bar's own mapped-lever taxonomy), but a NEGATIVE, sign-stable persistence
("bars that close strong tend to be followed by bars that close weak, relatively")
carries an inherent mean-reversion/fade flavor adjacent to the existing
`mean-reversion-fade` class, not a neutral conditioner the way candidate 1's magnitude
claim was. Neither GRADUATE (presuming an admission route I am not authorized to assume
clears) nor DROP (discarding the strongest statistical result in the batch) is the
honest call — this needs a scope ruling first, the same kind of ruling the 2026-08-10
ADR gave "within-instrument temporal selectivity."

---

## §5 — If HOLD: re-check trigger

- **Re-check date:** 2026-11-08 (rides the standing §4 falsifier hard-date already on
  the calendar for other programme items, per `CLAUDE.md`'s prop-portfolio §4 line — not
  a new date invented for this notice).
- **Trigger condition:** an operator or governance-layer ruling on whether this
  construct's admission route is (a) Route 1 (a-priori-named within-instrument
  selectivity — arguable, since it's unconditional on any window, not clearly a
  "selectivity" claim at all), (b) outside the raised bar's scope entirely (a pure
  shape/microstructure statistic, not a "directional intraday timing" construct in the
  bar's own sense), or (c) requires Route 2/3 like any other directional candidate. Once
  ruled, either GRADUATE to a Pre-Q (if a route clears) or DROP (if none does, or if a
  quick cost-law pre-screen — see §3 — kills it first at $0).
- **Drop trigger:** a $0 cost-law pre-screen (mean |gross edge implied by ρ≈−0.037| vs.
  the MYM cost hurdle, `MYM.md` #M6) run before the re-check date and failing cleanly.
- **Calendar entry:** none set; operator to set if desired.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c5_closing_location.py
# Expected: observed lag-1 Spearman rho = -0.0370, CI=[-0.0422,-0.0319], VERDICT: SIGNAL-EXCESS

# Re-check due: 2026-11-08 -- verify in Calendar / Todoist if the operator sets one
```

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md --type notice
# Expected: RESULT: well-formed
```
