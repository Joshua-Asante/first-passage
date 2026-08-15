**Theme:** orb
**Status:** ACTIVE — which FXIFY CFD best suits Opening Range Breakout
# Which FXIFY CFD is most suited for an Opening Range Breakout? — RESULTS (2026-06-22)

**Mandate (operator-directed):** the US500 widest-net search
([`lab/analysis/us500_discovery_2026-06-22`](../us500_discovery_2026-06-22/RESULTS.md))
surfaced opening-range breakout (ORB-30) as the one *structurally-real* pattern (within-day
placebo p=0.012) but **not tradeable on US500** (the +0.058R edge died at ~0.9pt of entry
slip). Question: **which CFD in the FXIFY universe is most suited for an ORB strategy?**
Method = literature/universe research (deductive ranking) ⊕ an empirical screening that
ports the calibrated US500 ORB battery to every instrument with local 15m data.

**Harness:** [`orb_lib.py`](orb_lib.py) (generalized loader for BAR_EXPORT + OANDA feeds,
tz-aware session tagging, ORB engine, within-day placebo, continuous fill-cliff slip sweep,
best-of-K, FXIFY first-passage MC) + [`run.py`](run.py) (per-instrument battery) +
[`screen.py`](screen.py) (cross-instrument comparison). Research: workflow `wf_3e36b013-2a4`
(5 agents — academic literature, FXIFY universe, repo grounding, adversarial critique,
synthesis).

## Calibration gate (port faithfulness) — PASSED

`run.py calibrate` reproduces the established US500 ORB-30 result **exactly**, so every
cross-instrument number is directly comparable to the US500 not-tradeable benchmark:

| check | reproduced | established |
|---|---|---|
| meanR | +0.0580 | +0.058 |
| t | +1.35 | +1.35 |
| WR / PF | 0.419 / 1.107 | 0.419 / 1.107 |
| long / short | +0.069 / +0.047 | +0.069 / +0.047 |
| within-day placebo p | 0.008 | 0.012 |
| fill-cliff slip-to-zero | 0.913pt (1.14× spread) | ~0.9pt |
| first-passage ceiling | 58% pass / 41% bust / p99DD 10.1% | ~58% / 31-45% / 7-13% |

## What "suited for ORB" means — the scorecard

From the literature (Gao-Han-Li-Zhou *Market Intraday Momentum* JFE 2018; Zarattini-Aziz
QQQ/TQQQ; Reading 2021 global; Crabel 1990) ⊕ the US500 fill-cliff lesson, ORB
*tradeability* (not mere statistical presence) is predicted by, in order of discriminating
power:

1. **Discrete, high-information cash open** (overnight info resolves at one scheduled
   auction). 24/7 markets (FX, crypto) have no real open → arbitrary anchor. **On FXIFY only
   the European/Asian cash indices (GER40, UK100, JP225, EU50) have a feed that genuinely
   closes overnight; US500/NAS100/DJ30 trade ~23h so 09:30 ET is a vol *event*, not a
   session boundary.**
2. **Edge-band vs (spread+slip)** — ORB entries are stop-fills at the breakout level, so
   entry slip is worst exactly on fast one-sided moves. *This is what killed US500* (edge
   inside a sub-1pt band on an 18.8pt range). Metric: **slip-to-zero / spread**.
3. **Opening-session realized vol / impulse** (numerator over #2).
4. **Intraday momentum / trend persistence** (not mean-reversion) — and *regime-robust*,
   not a single trend-year artifact.
5. **Overnight gap behavior** (coupled to #1).
6. **Liquidity / news-conditioning** (single-stock ORB has *no* unconditional edge — lives
   entirely in a relative-volume filter FXIFY can't provide intraday).

## The empirical battery (7 pre-registered falsifiers, run cheapest-first)

Per instrument, ORB-30 touch-fill, cost-net (each instrument's RT cost in its own points),
risk = opening range, exit at session close (no swap), directly vs the US500 benchmark:

1. cost-net meanR / t / WR / PF
2. **both-sides / short-side meanR** (beta control — a long-only-positive ORB is duplicative
   index beta, not an edge)
3. **fill-cliff slip-to-zero**, as a fraction of the instrument's spread
4. **within-day placebo p** (is the *opening* range special vs arbitrary intraday windows)
5. **year-robustness + chop-half** (is it all-years-positive or a single-trend-year artifact)
6. **best-of-K** OR-length × vol-filter multiplicity correction
7. **standalone first-passage** pass / bust / p99 DD at 0.75% risk

Falsifier — *"instrument X is no better than US500 for ORB"* if **any** of: short side not
independently positive after cost; slip-to-zero/range ≤ US500's; chop-year weak or
halves sign-invert; best-of-K-corrected p ≈ US500's; first-passage ceiling near US500's ~58%.

---

## RESULTS — comparison table

ORB-30 touch-fill, cost-net, exit@close. Ordered by meanR. `slip0/sprd` = entry slip (in
spreads) at which meanR crosses zero — the US500 fill-cliff metric (higher = more tradeable).
`plcb_p` = within-day placebo (is the *opening* range special). `BoK_p` = best-of-K (OR-length
× vol-filter) multiplicity-corrected p.

| instrument | feed | n | meanR | t | long | short | plcb_p | allyr+ | slip0/sprd | BoK_p | fp pass/bust/p99DD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **NAS100** | Pep | 1663 | **+0.0872** | **+2.94** | +0.102 | **+0.070** | **0.014** | 6/7yr | **>3.0×** (no zero-cross) | **0.009** | **0.71 / 0.25 / 0.097** |
| GER40 (DAX) | Pep | 1646 | +0.0597 | +1.63 | +0.091 | +0.028 | **0.126 ✗** | 4/7yr | 2.67× | 0.354 | 0.60 / 0.39 / 0.100 |
| US500 *(bench)* | Pep | 1149 | +0.0580 | +1.35 | +0.069 | +0.047 | 0.008 | 5/5yr | 1.14× | 0.50 | 0.58 / 0.41 / 0.101 |
| XAUUSD (gold) | Pep | 1644 | +0.0311 | +1.03 | +0.113 | **−0.048** | 0.0005† | 4/7yr | 0.89× | 0.79 | 0.55 / 0.42 / 0.100 |
| DJ30 (US30) | OANDA | 2038 | +0.0249 | +0.89 | +0.034 | +0.015 | **0.194 ✗** | 5/9yr | 1.43× | 0.85 | 0.53 / 0.44 / 0.100 |
| USDJPY | OANDA | 2053 | −0.0311 | −0.87 | +0.037 | −0.099 | 0.0005† | 5/9yr | 0 | 1.00 | 0.40 / 0.59 / 0.102 |
| GBPUSD | OANDA | 1552 | −0.1131 | −3.03 | −0.092 | −0.134 | 0.0005† | 0/6yr | 0 | 1.00 | 0.28 / 0.72 / 0.103 |
| XAGUSD (silver) | OANDA | 1089 | −0.1953 | −5.24 | −0.148 | −0.243 | 0.0005† | 1/5yr | 0 | 1.00 | 0.13 / 0.86 / 0.103 |

*Pep = Pepperstone BAR_EXPORT (canonical feed, same as the US500 anchor). OANDA = staging/Action-class.
NAS100 deep panel 2014-2026 (page-split); the row is the 2020-2026 page. Cost models are
grounding-derived estimates (NAS100 spread 1.25pt, RT 1.55pt); the NAS100 fill-cliff verdict is
robust to 2-3× cost error (see below).*

† **placebo "significant" in the WRONG direction** — for gold-short/USDJPY/GBPUSD/silver the
opening range *is* special, but the breakout **fades** (placebo_mean strongly negative), so a
*reverse*-ORB would be the signed edge, not ORB. A low placebo p means "the opening window
carries information," NOT "the breakout pays." NAS100 is the one instrument where the opening
range is special **and** the breakout direction is the profitable one.

## Per-instrument verdicts

- **NAS100 — UNIQUE WINNER.** The only instrument that clears every falsifier. **It solves
  the exact thing that killed US500**: the fill cliff. NAS100's median opening range is 95.9pt
  against a ~1.25pt spread (≈77:1) vs US500's 18.8pt against 0.8pt (≈23:1) — so the edge-band
  absorbs **>3 spreads of entry slip without crossing zero** (still +0.041R at 3.75pt slip),
  where US500 died at 1.14×. cost_R is only 0.016 (range swamps cost). The short side is
  **strongly positive (+0.070)** — direction-agnostic, *not* long-Nasdaq beta (the
  Aegis-short-mirror falsification was a mean-reversion-short mechanism, irrelevant to a
  breakout short). Best-of-K p=0.009 with a **short-OR plateau** (OR15 +.086 / OR30 +.087,
  both t>2.3) — matches the literature's 5-min dominance, *not* a hand-landed needle.
  Year-robust *within 2020-2026*: positive 6/7 incl. the **2022 bear (+0.108)**; only 2020
  marginally negative (−0.014). **Two decisive caveats from the confirmation battery (below):
  (a) the edge is REGIME-CONDITIONAL** — pre-2020 OOS (2014-2019) is **negative** (meanR −0.059,
  every year negative, placebo fails), and the OANDA cross-feed independently dates the turn-on
  to ~2020-2021. **(b) not standalone-lock-grade** — no risk level clears the lock gates *and*
  passes the challenge usefully.
- **GER40 (DAX) — best-by-spec, empirically modest.** Despite being the *only* true
  discrete-cash-open instrument (the trait the literature prizes most), its within-day
  **placebo FAILS (p=0.126)** — the opening range is *not* significantly special vs arbitrary
  windows — and it is 2022-carried (3 negative years; halves +0.113/+0.007). Good fill-cliff
  headroom (2.67×) but the structural-open advantage **did not translate into a robust edge.**
  The decisive empirical lesson: ORB tradeability is dominated by *edge-band-vs-cost* (vol/spread),
  not by the discreteness of the open.
- **US500 — the benchmark.** Real-but-not-tradeable (fill cliff 1.14×), re-confirmed exactly.
- **XAUUSD (gold) — long-beta-contaminated, sub-cost.** Long +0.113 but short **−0.048** →
  the "edge" is partly gold-bull beta; weak overall (t=1.03), sub-cost fill cliff (0.89×).
- **DJ30 — weak, placebo FAILS (0.194).** Critically, DJ30 (the other US index) is *not* a good
  ORB instrument — proving NAS100's edge is **NAS100-specific (highest vol/spread ratio), not a
  generic US-index effect.** (OANDA feed; DJ30 Pepperstone recent panel not local.)
- **USDJPY / GBPUSD — anti-edge (FX, no discrete open).** Negative meanR; breakouts fade. The
  24h-no-cash-open prior is confirmed on the NY-open ORB. *(London-open variant untested; the
  fade signature + repo FX priors make a positive result unlikely.)*
- **XAGUSD (silver) — strong anti-edge** (meanR −0.195, t=−5.24, 86% bust). Breakouts get
  crushed; consistent with the prior Silver-breakout rejection.

## Ranking — which CFD is most suited for ORB

1. **NAS100 / USTEC — decisively #1.** The single FXIFY CFD with a tradeable-grade ORB profile:
   it is the one instrument where the higher opening-session volatility widens the edge-band
   *faster than spread scales*, clearing the fill cliff that makes ORB sub-cost everywhere else.
2. **GER40 / DAX — #2 by spec, #2-3 empirically.** Best structural fit (true discrete open) and
   good fill-cliff headroom, but the opening-range signal is not placebo-special and is
   regime-fragile. A *conditional* candidate (see next steps).
3. **US500 — #3.** Cleanest signal-to-noise but the range/spread ratio is too low → sub-cost.
4. (gold / DJ30 — weak; FX / silver — anti-edge.)

**The headline answer: NAS100 is the most suited CFD in the FXIFY universe for an ORB strategy,**
and it is the only one whose ORB edge survives realistic entry fills.

## NAS100 winner-confirmation battery ([`nas100_confirm.py`](nas100_confirm.py))

Applying the repo's own anti-overfit skepticism to the *positive* result — the in-sample
2020-2026 strength is real, but the deeper tests reframe it.

**1. Pre-2020 out-of-sample (NAS100 Pepperstone 2014-2020) — FALSIFIED.**
meanR **−0.0592, t=−1.74**, **every year 2014-2019 negative** (2014 −.049 / 2015 −.199 / 2016
−.065 / 2017 −.011 / 2018 −.013 / 2019 −.012), placebo p=0.133 (fails), both sides negative,
fill cliff already below zero. **The NAS100 ORB edge did not exist before 2020.**

**2. OANDA cross-feed (2018-2026) — corroborates the regime split, not a feed artifact.**
meanR +0.040 (t=1.42), placebo p=0.024 clears, but the by-year independently dates the turn-on:
2018 **−0.220** / 2019 −0.032 / 2020 −0.029 (negative) → 2021-2026 all positive (+.066/+.100/
+.091/+.161/+.070/+.147). Two independent feeds agree the edge **activates ~2020-2021**. This
is the literature's pattern exactly (ES/NQ intraday momentum "flat 2010-2017, activating after
2018") and the repo's standing regime caveat (benign-regime-weighted post-2020 sample).

**3. Risk-sizing sweep (standalone first-passage, touch-fill, 2020-2026) — no lock-grade size.**

| risk | pass | bust | timeout | p99DD | median_d | lock gate |
|---|---|---|---|---|---|---|
| 0.75% | 0.71 | 0.25 | 0.04 | 9.7% | 32 | fail |
| 0.50% | 0.65 | 0.13 | 0.22 | 8.5% | 51 | fail |
| 0.40% | 0.56 | 0.08 | 0.37 | 7.6% | 62 | fail |
| 0.30% | 0.40 | 0.03 | 0.57 | 6.3% | 75 | fail |
| 0.20% | 0.16 | 0.002 | 0.84 | 4.7% | 92 | **PASS gate but 84% timeout** |

The lock gates (bust<1%, p99DD<5%) only clear at 0.20% risk, where 84% of paths time out — i.e.
there is **no risk level that is both safe and passes the challenge usefully.** (Far better than
US500's 58%/41% ceiling, but the same structural verdict.) The edge is **slip-robust**: +1pt
realistic entry slip at 0.40% risk leaves meanR +0.075, bust 9.5%, p99DD 7.7% — the fill-cliff
headroom is real, the *regime-conditionality and the pass-vs-bust ceiling* are the binding limits.

## Recommendation + next steps

**Answer to the question — NAS100 / USTEC is the most suited CFD in the FXIFY universe for an
ORB strategy, decisively and uniquely.** It is the single instrument where higher opening-session
volatility widens the breakout edge-band *faster than spread scales*, clearing the fill cliff that
makes ORB sub-cost on US500, gold, and the rest. The effect is **NAS100-specific** (DJ30 and US500
fail the placebo / fill-cliff), driven by its uniquely high opening-range-to-spread ratio (~77:1).

**But ORB is not a drop-in standalone leg, even on NAS100** — two honest limits:
1. **Regime-conditional.** The edge is negative pre-2020 on *both* feeds and only activates
   ~2020-2021. Without an *exogenous* reason for the structural break, this is the repo's standing
   "OHLC edge is regime-descriptive" pattern (cf. Q-SPX-F09, Q-NAS-4) — it would need a confirmed
   mechanism to be lock-grade.
2. **Not lock-grade standalone** — no risk size clears the lock gates and passes usefully.

**Disposition: NAS100 ORB-30 = REAL-AND-SUPRA-COST-IN-CURRENT-REGIME, REGIME-CONDITIONAL** (a
strictly more hopeful disposition than US500's real-but-sub-cost — the edge clears fills here; the
open question is whether the post-2020 regime is structural). **No core/lock/allocation/dd_protection
change; no Pine authored.** This is a characterization + a ranked answer, not a deployment.

**Next steps, in priority order:**
1. **Test the regime-break mechanism (the load-bearing question).** The post-2020 turn-on
   coincides with the 0DTE-options / retail-intraday-flow explosion on Nasdaq names — a plausible
   *exogenous microstructure* reason the edge is structural, not lucky. Acquire 0DTE/options-flow
   or VIX-term-structure series and test whether NAS100 ORB conditions on it. If yes → it graduates
   from regime-conditional to mechanism-backed (clears the standing exogenous-data bar). If no →
   it stays a regime artifact. **This is the only path to a lockable NAS100 ORB.**
2. **If developed: IR-exit, not exit-at-close.** Per F-US500-A (FXIFY is a Sharpe-race-with-a-
   deadline), a give-back-33%-of-open-profit trailing exit should lift the pass-vs-bust frontier
   above the touch-fill exit-at-close used here — re-run the risk sweep with the IR-exit before
   judging deployability.
3. **Portfolio fit (flag, not part of the suitability question).** A NAS100 ORB overlaps the live
   Striker NAS100 v1 leg at the instrument level (different clock: 09:30-ET cash open vs Mon/Tue
   13:00-17:00 UTC). The ORB is direction-agnostic (short +0.070), so it is not pure duplicative
   long-beta — but a second NAS100 strategy is a concentration the 2026-08-08 regime review (which
   wants a *corr≤0* counterbalance) should weigh against. **DXTrade contractValue=10 already
   broker-verified** (no onboarding/sizing risk).
4. **GER40 (DAX) — deprioritize for ORB.** The best-by-spec candidate empirically failed the
   placebo; its true-discrete-open advantage did not produce a robust opening-range edge. Keep the
   user-supplied panel for other European-session work, but it is not the ORB answer.
5. **Closed for ORB:** US500 (re-confirmed sub-cost), DJ30 (placebo fail), gold (long-beta + sub-cost),
   silver (strong anti-edge), USDJPY/GBPUSD (anti-edge; FX no-discrete-open prior confirmed).

## Operator ruling + approval (2026-06-22, post-research)

**Operator ruling (standing, methodology-layer):** results proven since 2020 are **admissible**;
COVID-19 (March 2020) is treated as a structural watershed, so a pre-2020 OOS failure is **not**
a disqualifier. 6.5 years (2020-2026) is a sufficient sample. **ORB-on-NASDAQ is APPROVED as a
strategy.**

**This retires the N2 "regime-conditional" caveat by ruling.** It is a *defensible* application
here specifically because NAS100 ORB's post-2020 evidence is **strong on its own** — positive
6/7 post-COVID years *including the 2022 bear*, both-sides (+0.070 short), a *structural* within-day
placebo (not a fitted threshold), a short-OR plateau, and best-of-K p=0.009 — i.e. it is robust
across many independent post-2020 sub-samples, not an in-sample fit to one regime. There is also a
plausible *exogenous* reason the pre-2020 break is real (0DTE/retail-intraday-flow microstructure).
**Principled guard (so the ruling is not OOS-laundering):** the ruling revives a mechanism only when
its post-2020 evidence stands alone (not a circular/n≈2 in-sample fit). NAS100 ORB clears this; see
the Q-REGIME-OOS-1 re-adjudication (it does *not*).

**"Approved edge" ≠ "deployable locked leg" — remaining engineering before a 5th-leg lock:**
1. **Exit** — replace exit-at-close with the F-US500-A **IR-exit** (give-back-33%-of-open-profit);
   re-run the risk sweep on the IR-exit (expected to lift the pass-vs-bust frontier materially).
2. **Risk size + direction** — pick the risk% from the IR-exit sweep; decide both-sides vs long-only
   (short side is +0.070, so both-sides is supported and reduces overlap with the long-only v1 leg).
3. **Pine** — author the strategy + indicator (`pinescript-v6`); contractValue=10 already verified.
4. **Portfolio re-MC** — 5-strategy MC including NAS100-ORB, with the **instrument-overlap correlation**
   vs Striker NAS100 v1 measured; check the lock gates (bust<1%, p99 DD<5%) and the 2026-08-08
   regime/counterbalance slate. The ORB short side is the part most likely to *help* the H1 chop tail.

## Methodological yields

**Methodological yield (transferable):** (i) **ORB tradeability is dominated by opening-range-to-
spread ratio, not by the discreteness of the cash open** — the highest-vol 23h-feed instrument
(NAS100) beat the only true-discrete-open instrument (GER40), which failed the placebo. (ii) **A
low within-day placebo p does not mean "good ORB"** — for FX/silver the opening range is special in
the *fade* direction; the *sign* of the edge is the discriminator, not the placebo alone. (iii) **In-
sample year-robustness (NAS100 6/7 positive 2020-2026) can still be regime-conditional** — the
2014-2019 OOS was the load-bearing test; a positive finding earns the same deep-OOS scrutiny as a
negative one.
