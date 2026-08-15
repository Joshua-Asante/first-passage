<!--
REPO-FACING PREFACE (Claude Code, 2026-07-11) — not part of the source document.

Provenance: an external field guide commissioned for this operation (it references
this program's own artifacts — Q-DECAY-1, the rejected-candidates registry, the
joint week-block MC, the accept-beta fork — so it is bespoke, not generic). Adopted
into the repo 2026-07-11.

Status: REFERENCE, not canonical and not gating. Pine source + `docs/adr/` remain
canonical for strategy behavior and decisions (Rule 0); `dd_protection.py` /
`firm_rules.py` remain canonical for live-sizing constants. Nothing here overrides a
locked parameter or a landed ADR. It is the statistical *rationale* layer the
methodology skills and the discovery-campaign pipeline cite.

Where it maps in-repo:
  - Part II (staged pipeline, Stage 0–7) ≈ `docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`
    stage pipeline; the Domain columns are the "why" behind `§Campaign-defaults`.
  - Domain 4 (multiplicity) ≈ `strategy-validation` §8 + `futures-anomaly-discovery`
    register_search K-ledger.
  - Adoption decision, the 8-domain → repo gap map, and the deliberate NON-adoptions
    (Kelly / SPRT / Ledoit-Wolf / numeric-π) are recorded in
    `docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md`.

The body below is verbatim.
-->

# The Statistics of Tradable Anomalies

*A field guide to the inference machinery behind anomaly discovery, from detection through strategy admission. Organized by statistical domain (Part I), then mapped onto a staged discovery pipeline (Part II).*

---

## Framing: what you are actually claiming

A tradable anomaly is a claim of the form: **E[r | condition] ≠ fair value, net of costs, and the gap is stable enough to survive the lag between discovery and execution at size.** Every word in that sentence is a separate statistical burden, and your phrasing — *structural, statistically significant, and consistent* — decomposes it exactly:

- **Significant** — the conditional expectation is distinguishable from sampling noise given how hard you searched. This is the domain of hypothesis testing, resampling, and multiplicity control (Domains 2–4).
- **Consistent** — the effect is stable across time, regimes, parameter neighborhoods, and related instruments, and you can detect its death. This is stability analysis, decay modeling, and sequential monitoring (Domain 5).
- **Structural** — something causes it, and that something has a reason to persist. Statistics cannot establish this directly; it can only discipline the mechanism story and quantify how much a mechanism prior is worth (Domain 8).

Two framing facts govern everything downstream.

First, the **joint hypothesis problem** (Fama): "anomalous" is always relative to a model of fair returns. A test never rejects "the market is efficient"; it rejects "the market is efficient *and* my null model of returns is right." Choosing the null model is not a technicality — it is the definition of the anomaly. A long-only signal tested against a zero-drift null on an instrument that trended for three years will show a spectacular "edge" that is actually just the drift. Name the null explicitly, every time.

Second, the **law of large numbers is the business model**. A per-trade edge of θ = μ/σ (mean over standard deviation of per-trade P&L) compounds as n·μ while noise grows as √n·σ, so the t-statistic of your track record grows as √n·θ. "Executed many times" is not a flourish — it is the entire mechanism by which a small conditional expectation becomes a reliable income stream. This immediately implies that trade frequency, capacity, and cost per execution are first-class statistical quantities, not operational afterthoughts: they set n and they set the floor μ must clear.

---

# Part I — Statistical domains

## Domain 1: Null models and the baseline texture of price data

**What "no edge" means.** The weakest interesting null is not the i.i.d. random walk but the **martingale difference hypothesis**: E[r_{t+1} | information at t] = 0 after costs and risk compensation. Prices can have fat tails, volatility clustering, and time-varying distributions and still be a martingale — unpredictable in mean. Most real anomaly claims are rejections of the martingale property *conditional on something*: a calendar date, a positioning state, an order-flow state, a prior price pattern.

**Stylized facts are the baseline, not anomalies.** Any null generator you simulate from, and any test statistic you compute, must respect the well-documented texture of returns (Cont 2001):

- Heavy tails: excess kurtosis at every frequency; daily equity-index returns have tail indices around 3–5, meaning sample means are dominated by a handful of observations.
- Volatility clustering: |r| and r² are strongly autocorrelated for weeks to months even when r itself shows near-zero linear autocorrelation.
- Aggregational Gaussianity: returns look more normal at longer horizons.
- Leverage effect (equities): negative returns raise future volatility more than positive ones.
- Intraday seasonality: volatility and volume follow a U-shape within the session.

The practical consequences are severe. Naive i.i.d.-Gaussian t-statistics on strategy returns are **anti-conservative** — vol clustering means your effective sample is smaller than your nominal sample, and fat tails mean the CLT converges slowly. A test that ignores this will "discover" the stylized facts themselves and report them as edges (e.g., "volatility breakout works" is often just vol clustering wearing a costume). Rule of thumb: if your null simulation produces i.i.d. Gaussian bars, every result it blesses is suspect.

**Effect size before significance.** Define the edge in tradable units first: expectancy per trade in R or ticks, per-trade information ratio θ, and only then annualized Sharpe as the aggregation. Two anchors worth internalizing:

- The standard error of an estimated Sharpe ratio is approximately √((1 + SR²/2)/T) with T in years (Lo 2002, i.i.d. case; dependence makes it worse). An observed SR of 1.0 over 3 years carries a standard error of ±0.71. Over 10 years, ±0.39. Most backtests cannot statistically distinguish SR 1.0 from SR 0.3. This single formula explains most of the industry's replication failures.
- Statistical significance without economic significance is common and useless: a 0.5-tick conditional edge on a 1-tick spread instrument is a real anomaly and a guaranteed loss. Economic significance means clearing the full cost distribution (Domain 7) with margin — your existing convention of expectancy ≥ 4× the round-trip cost hurdle is exactly this, stated as a floor.

## Domain 2: Classical inference that survives market data

**Dependence-robust errors.** The workhorse fix for autocorrelated, heteroskedastic returns is HAC standard errors (Newey–West 1987), with lag length at least the dependence horizon (for overlapping event windows, at least the overlap length — the Hansen–Hodrick setting). When observations cluster naturally (by day, by announcement, by regime), cluster the errors at that level. The underlying idea is **effective sample size**: with autocorrelation ρ_k, n_eff ≈ n / (1 + 2·Σρ_k). A thousand overlapping 20-bar returns might carry the information of fifty independent ones. Compute n_eff before celebrating any t-statistic.

**First-line detectors.** A small kit covers most scanning needs:

- **Variance-ratio tests** (Lo–MacKinlay 1988): VR(q) = Var(q-period return)/(q·Var(1-period return)). Equals 1 under a random walk; >1 indicates positive autocorrelation (momentum) at horizon q, <1 indicates mean reversion. Use the heteroskedasticity-robust z-statistic. This is the cleanest single test for "is there *any* linear predictability at this horizon."
- **Ljung–Box** on returns versus on |returns|: significant on |r| but not r means vol clustering, not predictability. Running both prevents the most common false discovery in the genre.
- **Runs tests and the BDS test** for dependence that autocorrelation misses (nonlinear structure). BDS rejecting while linear tests pass is the signature of regime-switching or nonlinear dynamics — interesting, but a much harder anomaly class to monetize.
- **Event-study framework** for calendar and announcement effects: abnormal return = realized minus a conditional benchmark, aggregated across events, with errors robust to overlap and event-time clustering. This is the right harness for month-end, expiry, FOMC-window, and roll-date hypotheses.

**Structural breaks and era risk.** An "edge" can be a single break in disguise. Bai–Perron multiple-break tests, CUSUM of recursive residuals, and simple era-dummy interactions answer the question: *is the effect a property of the process, or a property of one period?* The 2023–26 trend era is the live example in your book — a family of strategies sharing long-continuation exposure will all test "significant" against any null that doesn't hold the era fixed. The minimum discipline: estimate the effect within eras and demand sign consistency (Domain 5); the stronger discipline: include era as an explicit conditioning variable in the null.

**The regression trap.** The claim "my strategy has an edge" is a claim about the **intercept** of a regression of strategy returns on tradable benchmarks — not about the mean return. Regress on buy-and-hold, on generic time-series momentum, on carry; use HAC errors. A strategy whose alpha vanishes when a trend factor enters the regression is a trend-following implementation, not an anomaly. That's not worthless — but it must be admitted as beta (with beta's crowding and correlation properties), not as an independent bet. This regression is the statistical form of your accept-beta fork.

## Domain 3: Resampling, permutation, and surrogate data

Analytic null distributions rarely exist for the statistics you actually care about — profit factor, max drawdown, best-of-search Sharpe. Simulation-based inference fills the gap, and the entire craft lies in **what you hold fixed and what you destroy**.

**Permutation tests and exchangeability.** A permutation test is valid only if, under the null, the things you shuffle are exchangeable. The design choices:

- **Shuffle signals against returns** (or equivalently, relabel entry dates): nulls the claim "this signal times entries better than random entries with the same frequency and holding profile." Critically, if signals cluster in time (they almost always do), naive shuffling destroys that clustering and overstates significance — block-shuffle the signals, or regenerate signals from the same rule on surrogate prices.
- **Bar permutation** (Masters): permute the sequence of bar-to-bar changes while preserving each bar's internal open-high-low-close geometry, then re-run the full strategy on the permuted series. This nulls "the rule extracts sequence information" while preserving the marginal distribution and intrabar structure.
- **Drift handling is the crux.** If you detrend before permuting, you test timing skill net of drift; if you leave drift in, a long-only rule beats its permutations trivially by being long. For a long-only strategy on a trending instrument, the honest null *includes* the unconditional drift — you are claiming timing skill, not the equity premium. Getting this wrong is the single most common way permutation tests flatter a strategy.
- **Know what each permutation kills.** Your own validation canon already states it: permutation kills random-labeling nulls, not path-overfit. A rule tuned to the one realized path can pass label permutation forever. The complementary nulls (fresh path, fresh period, fresh instrument) come from Domain 5's replication logic — keep the "which nulls remain alive" ledger.

**Bootstrap under dependence.** The i.i.d. bootstrap is wrong for returns; block bootstraps are the fix. Moving blocks, circular blocks, and the stationary bootstrap (Politis–Romano 1994, geometric block lengths) all preserve dependence up to the block horizon. Two decisions matter:

- **Block length** must exceed the dependence horizon you care about. Vol clustering persists for weeks; weekly-to-monthly blocks for daily-bar strategies are defensible, and Politis–White (2004) gives an automatic selector when you'd rather not argue. Your portfolio MC's joint week-block design is this machinery — and the "joint" part is the important half: resampling all strategies' weeks *together* preserves cross-strategy dependence, which is exactly what a portfolio-level tail estimate needs.
- **What the bootstrap cannot do:** it resamples the sample. A block bootstrap of 2023–26 quantifies sampling error *within* the 2023–26 regime; it says nothing about regimes not in the data. This is why a bootstrap-based MC and an era-risk analysis are complements, not substitutes — the adverse futures-constrained re-MC result and the era question are two different failure axes.

**Surrogate data.** Phase randomization and IAAFT generate series with the same linear autocorrelation spectrum (and, for IAAFT, the same marginal distribution) but destroyed nonlinear structure. They are the natural null for "my edge is nonlinear dependence" claims and a useful second opinion when bar permutation and signal shuffling disagree.

**Monte Carlo of the fitted null.** Sometimes the cleanest null is parametric: fit a GARCH-family process (which reproduces vol clustering and fat tails), simulate long histories, and run the full discovery pipeline on synthetic data that contains *no* conditional mean structure by construction. The distribution of "best anomaly found" on synthetic noise is the sharpest possible calibration of your scanner — it measures the scanner, not the market. Expensive, and worth it once per pipeline version.

## Domain 4: Multiplicity — the central problem of anomaly mining

If you remember one number from this entire document, make it this one: **the expected maximum of N independent standard-normal draws is approximately √(2 ln N).**

| Configurations tried (N) | Expected best t-stat on pure noise |
|---|---|
| 10 | 2.1 |
| 100 | 3.0 |
| 1,000 | 3.7 |
| 10,000 | 4.3 |

Run a thousand variants — instruments × sessions × entry rules × parameter cells — on data with zero edge, and your best result is *expected* to have a t-statistic of 3.7. Not might: expected. Every threshold, haircut, and registry discipline downstream exists because of this arithmetic. And N is combinatorial: three instruments × four sessions × five entry variants × ten parameter cells is already 600 implicit tests, whether or not you ran them as an explicit grid.

**Family-wise error control (FWER)** — Bonferroni (test at α/m) and Holm's stepdown — guarantees P(any false positive) ≤ α. Appropriately brutal for small confirmatory families (the final three candidates before admission), needlessly destructive for scans.

**False discovery rate control (FDR)** — Benjamini–Hochberg (valid under independence and positive dependence), Benjamini–Yekutieli (arbitrary dependence, at a cost) — controls the expected *fraction* of discoveries that are false. This is the right frame for a scan stage: you are not trying to be right about every lead, you are trying to keep the lead pool clean enough that Stage-2 confirmation isn't swamped. A scan-stage FDR of 10–20% feeding a confirmation stage on fresh data is a coherent design; a scan at per-test α = 0.05 with no correction is a false-discovery factory.

**Data-snooping tests for rule universes.** When the claim is "the best rule in my universe beats the benchmark," the null distribution is the distribution of the *maximum* over the universe:

- **White's Reality Check** (2000): bootstrap the joint distribution of all rules' performance under the null, compare the observed max to the bootstrapped max distribution.
- **Hansen's SPA test** (2005): a studentized version, much less sensitive to padding the universe with garbage rules (which mechanically inflates RC p-values).
- **Romano–Wolf stepdown** (2005): identifies *which* rules survive, with FWER control, rather than just testing the best one.

The operational requirement dwarfs the mathematical one: **the universe must include everything tried, including abandoned branches, informal peeks, and the variants you rejected by eye.** Sullivan–Timmermann–White (1999, 2001) showed that decades of published technical-rule and calendar-effect results dissolve under Reality Check accounting once the full search space is honestly represented. Your rejected-candidates registry is precisely this accounting — its value is that it makes N auditable.

**Sharpe-specific corrections.**

- **Harvey–Liu–Zhu (2016)**: given the volume of factor research, newly claimed effects should clear t ≈ 3.0, not 2.0. The exact hurdle matters less than the logic: the hurdle is a function of the field's cumulative N, not just yours.
- **Deflated Sharpe Ratio** (Bailey–López de Prado 2014): replaces the null benchmark SR = 0 with SR₀ = the expected maximum Sharpe of N trials on noise (given the variance across your trials), and corrects the test for skewness and kurtosis of returns. DSR ≈ P(true SR > 0 | observed SR, N trials, non-normality). It is the single most practical "one number" for a mined strategy.
- **Minimum backtest length**: inverting √(2 ln N), you need roughly T ≥ 2 ln N / SR² years of data for a true Sharpe SR to reliably beat the noise-max of N trials. Testing 1,000 configs hunting a Sharpe-1 strategy wants ~14 years of data. On a 2019-launch micro contract, that bound is unmeetable — which is an argument for researching on the parent's longer history and reserving the micro era as out-of-sample, i.e., the parent→micro discipline you already run.
- **Probability of Backtest Overfitting** (CSCV; Bailey et al. 2017): partition the sample into S blocks, form all combinations of half-train/half-test, rank all candidate configs in-sample in each combination, and record the out-of-sample rank of each in-sample winner. PBO = fraction of combinations where the IS winner lands below median OOS. PBO near 0.5 means your in-sample ranking carries no information — the selection process, not any single backtest, is what's being measured. That is its unique value: it audits the *procedure*.

**Design-level control: pre-registration.** All the corrections above are repairs. The prevention is fixing the hypothesis, test statistic, sample, and thresholds *before* looking — which converts a mining exercise (π low, Domain 8) into a confirmatory test (π high) and makes N = 1 true by construction. Two disciplines make it real rather than ceremonial: an append-only audit trail (any criterion moved after data arrived voids the checkpoint — your template's clause), and **alpha-spending** across a research program (Foster–Stine's alpha-investing formalizes how a sequence of tests over months can maintain a global error budget: each discovery earns back budget, each failure spends it).

**Selection effects beyond parameter grids.** Multiplicity hides in choices that don't look like tests: picking *which instrument* to study because it trended (selection on outcome), picking *which period* to emphasize, picking *which metric* to report (PF vs Sharpe vs expectancy — trying three metrics is three tests), and survivorship in your own idea flow. The corrective habit is to write the sampling frame down first: "I will scan these instruments over this period with this metric" is a registered family; "I noticed gold looked clean" is an unregistered one, and its p-values are fiction until re-derived on fresh data.

## Domain 5: Consistency — stability, robustness, and decay

Significance says the effect wasn't noise *in the sample you tested*. Consistency is the evidence that it's a property of the process rather than of one slice of history — and the machinery for noticing when it stops being one.

**Sub-period structure.** Split-half and rolling-window estimates, era dummies, and expanding-window t-statistics all answer versions of the same question. The right demand is **sign stability, not magnitude stability**: a real effect can halve across regimes; an artifact of one era changes sign or vanishes. Halves/thirds stationarity checks (already in your selection-tests battery) are the compact version. For anything calendar- or event-based, also check *count* stability — an "effect" carried by four fat observations in one quarter fails drop-top-k concentration analysis regardless of its t-stat.

**Parameter plateaus, correctly ranked.** Smoothness of the performance surface in parameter space — neighborhood mean rather than peak value — is necessary but weak evidence. Your test-ordering principle already encodes the reason: *a plateau validates parameters conditional on the selection.* Perturbing around a lucky selection (a lucky day-of-week, a lucky instrument, a lucky direction) reproduces the luck at every neighboring parameter value. Selection-level tests (placebos on the conditioning variable, label permutation, cross-instrument transplant) carry more information per run and should be spent first. The plateau's real job is narrower: distinguishing dome (well-placed), flat (insensitive — consider deleting the parameter), and cliff (needle — presumptive overfit).

**Replication across instruments, weighted by independence.** The same mechanism should appear wherever the mechanism operates: a month-end FX-hedge-rebalancing effect found in JPY has a natural out-of-sample test in the other majors *before* touching new data in time. But replication evidence must be discounted by correlation — confirming an ES finding on NQ (ρ ≈ 0.9+) is close to re-testing the same path, which is the Jaccard-0.96 lesson from your own records generalized: **a different data source is not a different path, and a correlated instrument is only a fractionally different path.** Confirming an index finding in gold or bonds is worth multiples more. Mentally, weight each replication by (1 − ρ²) against what you've already tested and demand that the *effective* number of independent confirmations, not the raw count, clears your bar.

**Triangulation across test designs.** A robust effect shows up under multiple non-identical harnesses — variance ratio at the relevant horizon, an event study on the conditioning variable, and the full strategy simulation should agree in direction. Each design has different failure modes (VR is blind to nonlinearity, event studies are sensitive to window choice, strategy sims entangle the effect with exit logic), so agreement is informative in a way that repetition of one design is not.

**Regime conditioning without lookahead.** Any regime label used to condition a test must be computable in real time. Fitting an HMM on the full sample and testing "within the high-vol state" uses smoothed (future-informed) state probabilities — a subtle but fatal leak; use filtered probabilities or trailing realized-vol buckets. The same applies to trend-era labels: "the 2023–26 trend era" is a valid *descriptive* stratification for break analysis, but a trading rule conditioned on "being in a trend era" must define the era from trailing data only.

**Decay is the base case.** McLean–Pontiff (2016) measured it across 97 published anomalies: returns roughly a quarter lower out-of-sample (pure overfitting share) and more than half lower post-publication (crowding share). The prior this installs: **edges are wasting assets with unknown half-lives**, part sampling illusion, part arbitraged-away. Two practical corollaries. First, expected live performance should be shrunk from backtest performance *before* sizing — a shrinkage weight rising with trade count and falling with search intensity; expecting 30–70% of backtest Sharpe is the honest range, and your own live-vs-projection reconciliation exists to estimate where in that range you sit. Second, capacity protects: effects too small for institutional size to harvest (micro-scale, short-horizon, high-friction) decay slower post-discovery because the marginal arbitrageur isn't paid enough to come — one of the few structural advantages of trading small.

**Detecting death: sequential monitoring.** The tools are CUSUM control charts on standardized trade outcomes (cumulative sum of (observed − expected)/σ, signal when the sum crosses a boundary) and Wald's SPRT between H₁: "edge as underwritten" and H₀: "edge = 0," which gives explicit expected-sample-to-decision at chosen error rates. Two hard truths come with them:

- **The peeking problem**: monitoring continuously against a fixed threshold without sequential correction inflates the false-kill rate enormously (checking a 2σ line weekly for a year is ~50 looks). Boundaries must be designed as sequential boundaries — SPRT thresholds or spending-function equivalents — and pre-registered, exactly like the forward-test checkpoints in your template.
- **The power reality**: at per-trade θ ≈ 0.1 and ~20 trades/month, distinguishing "edge as claimed" from "edge = 0" at conventional error rates takes on the order of *years*, not weeks (Domain 4's n ≈ 6.2/θ² ≈ 620 trades, ≈ 2.5 years). This is the statistical content of your Q-DECAY-1 finding — a common-mode failure busts the firm line long before any per-strategy detector can fire, *and no detector with acceptable false-alarm rates can be built that fires faster at these trade counts.* The implication is architectural, not instrumental: sizing and portfolio-level kill rules must carry the risk that per-strategy decay detection is slow by mathematical necessity. Where a mechanism monitor exists (Domain 8), it can fire faster than the P&L statistics; where none exists, the P&L arithmetic above is the binding constraint and the size must respect it.

## Domain 6: Dependence and portfolio-level admission statistics

A candidate anomaly is never admitted in isolation; it's admitted *into a book*. The statistics change accordingly — the question is marginal, and the enemy is hidden common structure.

**Correlation is not tail dependence.** Two strategies can show ρ ≈ 0.2 on daily returns and still draw down together, because dependence concentrates in stress: trend systems that are pairwise-quiet in calm markets go jointly flat-to-wrong in whipsaw regimes. Measure what you actually fear: downside correlation (correlation conditional on one leg being in its worst decile), drawdown coincidence in the joint MC, and copula-style tail dependence if you want a formal statistic. The joint block bootstrap already gives you the honest version — resampling all strategies' weeks together preserves whatever stress-dependence the sample contains, and the portfolio drawdown distribution it produces *is* the tail-dependence measurement.

**Effective number of bets.** PCA- or entropy-based ENB compresses the correlation matrix into "how many independent bets is this book, really." Four strategies at realized ENB ≈ 3.1–4.0 is a genuinely diversified small book *by that metric* — but ENB is estimated from the sample covariance, and the sample is one regime. The family-synthesis finding (shared long-continuation exposure, shared entry window, shared era) is the caution: a common factor that hasn't yet had its bad quarter is invisible to sample ENB. The admission statistic that matters is **marginal ENB and marginal tail delta**: run the joint MC with and without the candidate at proposed size, and read the change in ENB, in p5/p1 drawdown, and in bust probability. A candidate that improves mean while thickening the common-mode tail is a reload of an existing bet wearing new parameters.

**Covariance estimation error.** With 4–10 strategies and 1–3 years of weekly returns, the sample covariance matrix is noise-dominated (random-matrix territory), and anything downstream that inverts it — optimizers especially — amplifies the noise into confident nonsense. Ledoit–Wolf shrinkage helps; better still is refusing precision you don't have: coarse allocation buckets, capped weights, and MC-verified tails beat optimized weights at these sample sizes, essentially always.

**Drawdown mathematics.** Expected maximum drawdown grows with observation length even when the edge is constant and real — on the order of σ√T for zero drift, logarithmically in T for positive drift (Magdon-Ismail–Atiya 2004). Two consequences: a fixed dollar kill-line is implicitly a *time-declining* significance threshold (the longer you run, the more likely a healthy system trips it); and the only honest way to set kill thresholds is to simulate the claimed-edge process and the zero-edge process and read off, at each horizon, P(threshold hit | healthy) and P(not hit | dead). A kill line has a false-kill rate and a detection lag whether or not you computed them; computing them is the difference between a risk control and a mood.

**Sizing under estimation error.** Full Kelly maximizes growth *if the edge estimate is exact*; it is catastrophically asymmetric to overestimation (betting 2× Kelly has zero long-run growth). Since every backtest edge is an upper-biased estimate (Domains 4–5), the correct object to size on is a **shrunk, lower-confidence-bound edge**, and the standard practice is fractional Kelly — one-half Kelly retains ~75% of maximal growth at half the variance, and its real virtue is robustness to the estimation error you know you have. A ramp schedule (fractional sizing that steps up as live trade count accumulates and the posterior tightens) is the sequential version of the same logic.

## Domain 7: Microstructure, costs, and futures-specific texture

**Costs are part of the null model.** The tradable null is not E[r] = 0 but E[r] = −cost, and cost is a distribution, not a number: commission (fixed, knowable) plus spread crossing plus slippage (fat-tailed, state-dependent — worst exactly when signals cluster, i.e., in fast markets and thin sessions). Your cost-law pre-flight captures the sizing interaction that most people miss: under risk-based sizing, cost in R scales with price/stop-distance, so tight-stop designs face structurally higher hurdles before a single parameter is chosen. The admission-grade practice is to bracket fills — model the pessimistic assumption (market orders crossing the spread, stops filled with adverse slippage from the empirical tail) and the optimistic one, and require the edge to survive the pessimistic bracket. For limit-order entries, add adverse selection: you are disproportionately filled when the market is moving through you, so raw "touch = fill" backtests overstate limit-entry edges systematically.

**Micros specifically.** Micro contracts share the parent's tick grid, so spread as a fraction of notional is identical — but commission per notional runs roughly 5–10× the parent, books are thinner (especially overnight), and the history is short (2019 launches for the equity micros). Three consequences: the expectancy floor is higher on micros than the parent for the same strategy; research belongs on the parent's longer, cleaner history with tick values re-scaled (the parent→micro proxy discipline, with the micro era reserved as an out-of-sample gate); and any anomaly whose margin over costs is thin on the parent should be presumed dead on the micro until shown otherwise.

**Continuous-contract artifacts.** Back-adjustment is a choice that manufactures or destroys patterns. Difference-adjustment preserves point moves but distorts (and can make negative) price *levels* — percentage returns computed on a difference-adjusted series are wrong, and any level-based signal (round numbers, prior highs) is testing phantom levels. Ratio-adjustment preserves returns but distorts point values. Roll-date conventions inject jumps whose timing is your choice, not the market's. The discipline: indicators may run on adjusted series for continuity, but *entries, exits, and P&L must be evaluated on the actual tradeable contract's prices*, and any calendar-adjacent anomaly must be checked against the roll schedule to ensure you haven't discovered your own back-adjustment.

**Session structure and clock hygiene.** Exchange time vs local time vs UTC, DST transitions that silently shift a "9:30 open" filter by an hour twice a year, holiday half-sessions, and the RTH/ETH distinction are the leading generators of fake time-of-day anomalies — your Step-0 battery's entry-minute census and DST-aware hour mapping exist because these defects are machine-detectable and were caught in the wild. Additionally, intraday vol seasonality (the U-shape) means raw returns at different times of day are not comparable: any time-of-day effect must survive normalization by the time-of-day vol curve, or it's the U-shape in a costume.

**A taxonomy of futures-relevant anomaly families**, ordered roughly by persistence prior (Domain 8 explains why):

- **Constraint/flow effects** — month-end and quarter-end rebalancing (equity/bond flows, FX hedge rebalance: the named mechanism behind your JPY month-end finding), index reconstitution, leveraged-ETF close rebalancing, option-expiry pinning and OPEX cycles, futures roll windows, window dressing. Caused by mandated or mechanical flows from agents who are not paid to hide them; persist while the mandate persists; often calendar-forecastable, which is why they're detectable at retail scale.
- **Risk-premium effects** — time-series momentum (Moskowitz–Ooi–Pedersen 2012: 12-month persistence, partial long-horizon reversal, across ~58 futures), carry/roll yield from term-structure slope (Koijen et al. 2018), hedging-pressure premia readable in CFTC COT positioning (Bessembinder 1992; De Roon et al. 2000 — the family your swap-dealer COT lead belongs to), volatility risk premium. Compensation for bearing something; persistent but regime-dependent and increasingly crowded; these are *betas* in Domain 2's regression sense, and admitting one means admitting its factor exposure.
- **Announcement effects** — pre-FOMC announcement drift (Lucca–Moench 2015: a striking share of equity excess returns earned in the 24h pre-announcement window over 1994–2011, notably weaker post-publication — a live decay exhibit), post-CPI/NFP momentum-reversal structure, scheduled-vs-realized vol patterns around events. Mechanisms are contested (risk-premium vs attention), which lowers the persistence prior despite strong historical stats.
- **Session/temporal effects** — overnight vs intraday return decomposition (index returns historically concentrated overnight), turn-of-month, first-hour vs last-hour momentum, day-of-week (largely dead — the Monday effect is the canonical decay corpse; Sullivan–Timmermann–White 2001 showed most calendar effects fail data-snooping accounting), commodity seasonals (mostly folklore; test under Reality Check before believing).
- **Microstructure effects** — short-horizon order-flow-imbalance predictability (your MBO data's home turf), stop clustering at round numbers, liquidity gaps at session transitions. Real but small, capacity-constrained, cost-dominated — the family where the cost-distribution null does most of the killing. Note the artifact cousin: bid-ask bounce induces spurious negative autocorrelation in trade-price series; at bar granularity, use midpoints or you will "discover" mean reversion that is the spread itself.

## Domain 8: Mechanism, priors, and the Bayesian frame

**Every edge is someone's cost — name the payer.** The mechanism question isn't philosophical decoration; it sets the prior on persistence and defines what to monitor. The useful taxonomy of payers: agents *paid to transfer risk* (premium harvesting — persistent while risk exists), agents *constrained or mandated* (flow effects — persistent while the mandate exists, and monitorable via the mandate), agents *behaving predictably against their interest* (behavioral — persistent while the marginal participant stays undisciplined, eroded by arbitrage), and *structural latency/plumbing* (persistent until the plumbing changes, often abruptly). If no payer can be cast, the default hypothesis is that the pattern is sampling error and the payer-to-be is you.

**Priors, quantified.** The Ioannidis (2005) arithmetic transfers exactly. If π is the prior probability a candidate effect is real, the post-test probability (positive predictive value) at significance α and power (1−β) is PPV = (1−β)·π / [(1−β)·π + α·(1−π)]. Two worked points at α = 0.05, power = 0.5:

- Blind-mined pattern, π ≈ 0.01: PPV ≈ **9%**. A significant result from an uncontrolled scan is *probably false* — not "possibly," probably.
- Mechanism-first hypothesis, π ≈ 0.2: PPV ≈ **71%**.

Same test, same p-value, an order of magnitude apart — the entire case for hypothesis-first discovery, pre-registration, and mechanism naming in three lines of algebra. This is also why the Q-MECH-1-style verdict structure (mechanism named vs NO-MECH) is doing statistical work, not paperwork: it's assigning π, and π propagates through everything downstream including size.

**Mechanism gives you a second, faster detector.** Domain 5 established that P&L-based decay detection is slow by arithmetic necessity at realistic trade counts. A named mechanism offers an alternative channel: monitor the *cause*, not the consequence. If the effect is month-end hedge rebalancing, the monitors are the calendar and any observable of hedging practice; if it's COT positioning pressure, the positioning report is the monitor; if it's an expiry-pinning effect, open interest structure is. A mechanism monitor can fire on a structural change *before* enough losing trades accumulate to move a CUSUM. Conversely, the zero-free-external-monitors outcome of your family synthesis is the statistically uncomfortable case: admission without a cause-channel means the slow P&L channel is the only channel, which is a sizing input — the uninsured common-mode tail is uninsured precisely in this sense.

**Bayesian updating as the admission-to-live bridge.** The frequentist toolkit dominates discovery; the live phase is naturally Bayesian. Carry a posterior over the per-trade edge θ (start from the shrunk, search-penalized estimate; update as fills arrive), and let size track a lower quantile of that posterior. This unifies three things that otherwise live in separate documents: the initial haircut (prior), the ramp schedule (posterior tightening), and the retirement rule (posterior mass at θ ≤ 0 crossing a pre-registered line). Sequential Bayes and SPRT are near-relatives — SPRT is the likelihood-ratio special case — so the pre-registered SPRT boundaries and the posterior view can be built from the same object without double bookkeeping.

---

# Part II — The staged pipeline

The domains above are a toolbox; a discovery campaign is a sequence of gates. What follows is the generic pipeline with each stage's statistical content named. The stage boundaries are conventions — wherever your own campaign spec draws the lines, the domain-to-stage mapping transfers unchanged.

**Stage 0 — Data integrity and universe registration** *(Domain 7).* Before any statistic: back-adjustment method chosen and documented, tradeable-contract prices available for P&L, session definitions DST-proofed, tick-size and contract-spec history checked, micro launch dates noted, panel-integrity battery run. Equally statistical: **register the universe** — instruments, period, bar sizes, and the metric — before scanning, because this fixes the sampling frame and the N that every Domain-4 correction will need. An unregistered universe makes every downstream p-value unauditable.

**Stage 1 — Hypothesis generation** *(Domains 8, 1, 2).* Two lanes with different priors. The mechanism-first lane: enumerate payers and flows (the Domain 7 taxonomy is a checklist), write each candidate as a falsifiable conditional-expectation claim with its null model named — these carry π ≈ 0.1–0.3. The scan lane: cheap detectors (variance ratios by horizon, event studies on calendar/positioning conditions, conditional-mean tables) run across the registered grid with FDR control at 10–20% and an **effect-size floor in cost multiples** (a lead below ~2–3× round-trip cost is dead on arrival regardless of p) — survivors carry π ≈ 0.01–0.05 and must be treated accordingly downstream. Record everything tried, including the eyeballed-and-abandoned: that count is N.

**Stage 2 — Statistical confirmation** *(Domains 2, 3, 4).* On data not used in Stage 1 — a held-out period, or instruments where the mechanism should operate but wasn't scanned (weighted by independence, Domain 5). HAC t-statistics; permutation with the exchangeability design matched to the claim and drift handled honestly; era-split sign consistency; SPA/Reality Check against the registered universe if the candidate came from the scan lane. Exit hurdle in the spirit of DSR > 0.95, or t ≥ 3 given honest N — with the hurdle itself pre-registered.

**Stage 3 — Strategy formation** *(Domains 5, 7).* Translate the anomaly into rules with the *minimum* parameter count — every knob multiplies Stage-2's N retroactively if you iterate. Cost-law pre-flight on the intended stop geometry before building. Before any re-run of a variant (direction flip, exit redesign, added filter): the excursion-bounded counterfactual, which frequently answers the question for zero runs and — crucially for multiplicity — for zero new tests. Any filter that survives into the design re-enters the multiplicity ledger as a tested hypothesis, not a free choice.

**Stage 4 — Overfitting audit** *(Domains 4, 5).* CSCV/PBO on the full config set that was actually explored; deflated Sharpe with the ledger's N; minimum-backtest-length sanity check against available history; plateau protocol with pre-registered pass criteria, read *after* selection-level tests per the test-ordering principle; drop-top-k concentration and halves/thirds stationarity. The output artifact is a "which nulls remain alive" statement — the honest residual risk list, not a verdict of purity.

**Stage 5 — Out-of-sample and incubation** *(Domains 5, 3).* True OOS is one-shot: each look burns it, so the look is scheduled, not casual. Forward/paper/small-live incubation with the trade count set by power analysis in advance — n ≈ 6.2/θ² for 80% power at 5% one-sided, so at θ = 0.1 the honest checkpoint is hundreds of trades, and the pre-registration must disclose that intermediate checkpoints are expectation-based stop rules, not significance tests (your template's power-disclosure clause is exactly this). Sequential boundaries (SPRT or spending-function) fixed before the first trade; no post-hoc adjustment.

**Stage 6 — Admission** *(Domain 6).* The question changes from "is it real?" to "what does it do to the book?" Joint MC with and without the candidate at proposed size: marginal ENB, marginal p5/p1 drawdown, marginal bust probability, common-mode audit against the known family exposures (does it share the continuation beta, the entry window, the era?). Size from the shrunk lower-bound edge at a Kelly fraction, with a ramp schedule tied to live trade count. And the Domain-5 lesson made structural: **the retirement rule is written at admission** — CUSUM/SPRT boundaries, the mechanism monitor if one exists, and the acknowledgment of detection lag as a sizing input where one doesn't. A strategy without a death certificate template isn't admitted; it's adopted.

**Stage 7 — Live monitoring and retirement** *(Domains 5, 8).* The pre-registered detectors run; the mechanism monitors run where they exist; scheduled re-underwriting (quarterly is a natural cadence) re-estimates the posterior edge and re-checks the admission deltas at current correlations. Retirement or size-down triggers execute mechanically — the entire point of pre-registering them was to remove the negotiation. Post-mortems feed the registry either way: a retired strategy's autopsy is Stage-1 fuel and a data point on your own π calibration.

## Stage-by-domain map

| Stage | Question | Primary domains | Core tools | Gate artifact |
|---|---|---|---|---|
| 0 Integrity | Is the data real and the frame fixed? | 7 | Step-0 battery, back-adjust audit, universe registration | Registered universe + clean panel |
| 1 Generation | What might be true, and at what prior? | 8, 1, 2 | Mechanism taxonomy, VR/event scans, FDR, cost floor | Hypothesis registry with π lane |
| 2 Confirmation | Is it distinguishable from noise, given the search? | 2, 3, 4 | HAC t, permutation (drift-honest), SPA/RC, DSR | Pre-registered hurdle pass |
| 3 Formation | Can it be traded without re-mining? | 5, 7 | Cost pre-flight, excursion counterfactual, min-parameter design | Rule spec + updated N ledger |
| 4 Overfit audit | Is the *procedure* informative? | 4, 5 | PBO/CSCV, plateau-after-selection, drop-top-k | "Nulls remaining alive" statement |
| 5 OOS/incubation | Does it survive contact with new data? | 5, 3 | One-shot OOS, powered forward test, SPRT boundaries | Pre-registered checkpoint results |
| 6 Admission | What does it do to the book? | 6 | Joint MC deltas, marginal ENB, shrunk-Kelly sizing | Admission doc incl. retirement rule |
| 7 Live | Is it still alive, and at what size? | 5, 8 | CUSUM/SPRT, mechanism monitors, re-underwriting | Quarterly verdict + autopsy on exit |

## Numbers worth memorizing

- **Expected best t-stat mining N configs of noise: √(2 ln N)** → 2.1 / 3.0 / 3.7 / 4.3 at N = 10 / 100 / 1,000 / 10,000.
- **Trades for 80% power at 5% (one-sided): n ≈ 6.2/θ²** → ≈155 at θ=0.2, ≈620 at θ=0.1, ≈2,470 at θ=0.05.
- **SE of an estimated Sharpe ≈ √((1+SR²/2)/T years)** → SR 1.0 over 3y: ±0.71.
- **Minimum backtest length ≈ 2 ln N / SR² years** → 1,000 trials hunting SR 1: ~14 years.
- **PPV at α=0.05, power 0.5:** π=0.01 → ~9% real; π=0.2 → ~71% real. Mechanism is worth ~8× in posterior odds.
- **Half-Kelly: ~75% of maximum growth at half the variance;** 2× Kelly: zero long-run growth.
- **Published-anomaly decay (McLean–Pontiff): ~−26% out-of-sample, ~−58% post-publication.**

## Reading list

- **Cont (2001), "Empirical Properties of Asset Returns"** — the stylized-facts baseline every null must reproduce.
- **Lo & MacKinlay (1988)** — variance-ratio tests; *A Non-Random Walk Down Wall Street* collects the program.
- **Lo (2002), "The Statistics of Sharpe Ratios"** — the SE formula and its dependence corrections.
- **White (2000), "A Reality Check for Data Snooping"; Hansen (2005), SPA; Romano & Wolf (2005)** — inference on the best of a searched universe.
- **Sullivan, Timmermann & White (1999; 2001)** — technical rules and calendar effects under honest search accounting.
- **Benjamini & Hochberg (1995); Benjamini & Yekutieli (2001)** — FDR control, the scan-stage workhorse.
- **Harvey, Liu & Zhu (2016), "…and the Cross-Section of Expected Returns"** — the t ≥ 3 argument from field-level multiplicity.
- **Bailey & López de Prado (2014), "The Deflated Sharpe Ratio"; Bailey et al. (2017), "The Probability of Backtest Overfitting"** — the mined-Sharpe corrections; López de Prado, *Advances in Financial Machine Learning* (2018) for the assembled pipeline view.
- **McLean & Pontiff (2016)** — post-publication decay, measured.
- **Hou, Xue & Zhang (2020), "Replicating Anomalies"** — roughly two-thirds of the published zoo fails honest replication; the base-rate paper.
- **Moskowitz, Ooi & Pedersen (2012), "Time Series Momentum"; Koijen et al. (2018), "Carry"** — the two big futures risk-premium families.
- **Lucca & Moench (2015), "The Pre-FOMC Announcement Drift"** — announcement-family exemplar and live decay exhibit.
- **Politis & Romano (1994); Politis & White (2004)** — stationary bootstrap and automatic block-length selection.
- **Masters, *Permutation and Randomization Tests for Trading System Development*** — the applied permutation designs, including bar permutation.
- **Aronson, *Evidence-Based Technical Analysis* (2006)** — dated in places, but the best book-length treatment of selection bias aimed squarely at rule-based trading.
- **Ioannidis (2005), "Why Most Published Research Findings Are False"** — the PPV arithmetic; read it substituting "backtest" for "study."
