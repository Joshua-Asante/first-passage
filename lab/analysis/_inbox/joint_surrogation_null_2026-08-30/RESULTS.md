# RESULTS — Phase 1 joint-surrogation null design exploration (Q-RANGEXFER-1 / Q-VOLREGIME-1)

**Status (updated, Round 3 below): NOT RESOLVED to a certifiable standard, and materially further
from resolved than Round 2's own headline claimed.** Seven total joint-surrogation constructions
have now been tried across three rounds (Round 1: linked-residual IAAFT, VAR(p), shared-start
IAAFT; Round 2: CCC-GARCH/MEM, DCC-GARCH/MEM, ARFIMA long-memory+copula, nonparametric
regime-block-bootstrap; Round 3: a Codex review pass that found and fixed 4 real code bugs and
ran the refit-per-replicate check Round 2's own positive control had skipped). **Round 2's own
headline claim — "the surrogate-testing machinery is sound, confirmed by an independent
80-replicate re-run" — is corrected here: that re-run, like the original, validated the machinery
only under KNOWN-TRUE model parameters. When parameters are instead RE-ESTIMATED per replicate
(the only way the procedure could ever actually run on real, previously-unseen data), the null
false-positive rate empirically jumps from the nominal 5% to 25% (2/8 replicates, admittedly a
coarse/small-N check — see Round 3) — a real, non-trivial inflation, not a theoretical concern.**
What remains genuinely unresolved is now BOTH model adequacy (Round 2's own finding: no diagnostic
tried can reliably tell whether the fitted ARFIMA-copula model represents the real data well
enough to trust) AND, newly, whether the estimation step itself preserves Type-I control at all.
See "Round 2" and "Round 3" below for the full account. Nothing in Round 1 or Round 2's own
empirical numbers is deleted — only the CONCLUSION drawn from them is corrected.

## Round 1 (superseded in part by Round 2, not deleted)

Three candidate designs were built and empirically tested against a positive control (synthetic
data with a known ground truth) and/or directly against the real cached `on_range`/`rth_range`
joint frame. All three fail their own diagnostic gate, in two precisely opposite ways. This was a
genuine, evidenced negative finding, not a completed design — Phase 2 adversarial review had
nothing ready to review yet on this specific sub-problem. Written up in full because the evidence
itself (which constructions fail, and exactly how) is the load-bearing output of that attempt and
materially narrowed what Round 2 tried next.

## The problem, restated precisely

D5's own O1 item (`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` §4) names
a joint/coupled surrogation null "UNRESOLVED-NEEDS-DESIGN": a null that preserves (a) each series'
own linear ACF and (b) the real lag-0 cross-correlation between the two series, while randomizing
any dependence beyond that. `Q-RANGEXFER-1`'s own §7 sketch framed this as "a coupled/joint IAAFT
variant." This session tried to build exactly that.

## What was tried, and what happened

**1. Linked-residual IAAFT** (`joint_iaaft.py`'s original version, since rewritten in place —
see that file's own "SUPERSEDED DESIGN NOTE" for the full text): normal-score both channels,
IAAFT channel 1 directly (reusing the existing, already-validated univariate routine unchanged),
decompose channel 2 into `resid = z2 - rho0*z1` (an exact lag-0 OLS decomposition) and IAAFT the
residual separately, then recombine `z2_lin = rho0*z1_surr + sqrt(1-rho0^2)*resid_surr`.

- **Positive control** (`positive_control.py`, synthetic shared-AR(1)-regime data, N=20
  replicates each): diagnostic gate FAILED on **every single replicate**, both the null (no
  genuine transmission) and alternative (genuine transmission injected) scenarios. Channel 2's
  own ACF mismatch: med ≈ 0.14 vs a 0.04 tolerance. Reject rate: 0/20 in both scenarios (the null
  never rejects — not because it correctly fails to reject a true null, but because the surrogate
  distribution is miscalibrated, sitting at p_upper ≈ 0.9–1.0 essentially always).
- **Diagnosis:** the lag-0-only residual does not remove the shared regime's own serial dependence
  from what gets treated as "channel 2's own residual dynamics." The real data's cross-covariance
  between channel 1 and channel 2's residual at NONZERO lags is not forced to zero by a lag-0
  regression, and that un-removed persistence leaks into the reconstructed channel 2, badly
  distorting its own ACF whenever the shared regime is materially persistent (true both of the
  synthetic AR(1)-sum test and of the real MNQ range data — see below).

**2. Bivariate VAR(p) residual bootstrap** (current `joint_iaaft.py`): fit a bivariate VAR(p) on
the two normal-scored channels (captures each channel's own linear dynamics AND the full
cross-lag structure by construction of a single fitted model, not an assembled approximation),
bootstrap the fitted residual pairs IID, simulate forward, rank-remap onto each channel's own raw
values.

- **Direct diagnostic check on the REAL cached MNQ joint frame**
  (`candidate24_joint_frame.csv`, n=1487, real cross-correlation 0.772): at `p=20`, channel-1 ACF
  mismatch med=0.105/p95=0.169, channel-2 med=0.125/p95=0.178 (both FAIL vs 0.04/0.07 tolerance);
  cross-correlation mismatch p95=0.049 (PASSES). At `p=40`, own-ACF mismatch does not materially
  improve (med 0.09–0.10) and cross-correlation mismatch WORSENS to FAIL (p95=0.054, estimation
  noise from more parameters relative to n=1487 outweighing any gain). Residual-whitening
  diagnostic PASSES cleanly at every `p` tested (max |ACF(residual)| ≤ 0.006), confirming the VAR
  order is not the bottleneck — the own-channel ACF gap does not close with a longer
  autoregression.
- **Diagnosis:** a finite-order VAR is a parametric LINEAR approximation. Range-type series
  (already known in this exact repo to be hard to surrogate — candidate 1's own
  `daily-range-state-persistence` VOIDed on the univariate IAAFT battery for MNQ's own TR series,
  same class of series) have an autocorrelation shape a moderate-order VAR does not capture well,
  independent of the joint/bivariate complication. Confirmed directly: plain univariate IAAFT
  (unchanged, already-validated code) on `rth_range` alone is itself only BORDERLINE
  (med=0.0403, just over the 0.04 tolerance — a near-miss, not a clean pass) and on `on_range`
  alone passes narrowly (med=0.034). The VAR(p) construction's own-ACF mismatch (med 0.09–0.13) is
  materially worse than even this borderline univariate baseline, confirming the degradation is a
  real property of the VAR method on this data, not merely "the data is hard so any method
  struggles equally."

**3. Shared-starting-permutation coupled IAAFT** (tested standalone, not committed as the
module's implementation): apply the EXISTING univariate IAAFT to each channel independently, but
seed both from the SAME random starting permutation (so the very first iterate is an exact,
time-scrambled real joint pairing) rather than two independent permutations.

- **Direct diagnostic check, real data:** own-channel ACF reproduction is excellent — channel-1
  med=0.032/p95=0.056, channel-2 med=0.043/p95=0.059 (both close to or within tolerance, tracking
  the standalone univariate IAAFT quality almost exactly). But cross-correlation decays sharply
  and immediately: realized cross-correlation lands around 0.61–0.62 against a target of 0.772
  (mismatch ≈0.16, over 3× the 0.05 tolerance) — and does **not** improve with fewer iterations
  (swept n_iter = 1, 3, 5, 10, 20, 50, 100: cross-correlation mismatch is already ≈0.158 at
  n_iter=1 and stays flat thereafter). The very first amplitude/phase reconstruction step already
  does most of the decorrelating; more iterations barely change it either direction.
- **Diagnosis:** the mirror-image failure of the VAR approach — excellent at (a), poor at (b).

## Why this triangulation matters (not just three failures)

The three attempts fail in two *exactly opposite* directions: VAR(p) trades own-ACF fidelity for
cross-correlation fidelity; shared-start IAAFT trades the reverse. Linked-residual IAAFT tried a
one-shot compromise and landed worse than either pure approach on the property it wasn't
explicitly targeting (channel 2's ACF). This is reasonably strong evidence that a **simple
"generate a well-behaved marginal surrogate per channel, then combine" family of constructions
cannot jointly satisfy both properties on this specific data** (MNQ's own overnight/RTH range
pair, cross-correlation ≈0.77, individual series already borderline-IAAFT-viable on their own) —
not merely that this session picked the wrong specific recipe within that family.

## Round 2 — GARCH/long-memory judge panel (4 lenses) + gate-redesign attempt + adversarial verification

Following Round 1's own recommendation, a 4-lens design panel (independent agents, each building
and empirically testing its own construction against the real cached frame) tried the "different
surrogate class" remedy the frozen spec names. All 4 failed their own-ACF gate too, but with a
sharper, more mechanistic diagnosis than Round 1 had:

**4. CCC-GARCH / Multiplicative Error Model** (`ccc_garch.py`): literal Bollerslev CCC-GARCH on
normal-scored channels is *provably* wrong (mean-zero GARCH shocks give the simulated series zero
own-autocorrelation by construction, confirmed empirically: simulated ACF collapsed to ~0 vs real
~0.41 at lag 1) — the file documents this rejected sub-attempt, then delivers a corrected
Multiplicative Error Model (MEM/CARR) fit directly on the raw positive range level, coupled via a
Cholesky-correlated copula whose correlation parameter is bisection-calibrated to hit the real
cross-correlation. **Cross-correlation passes cleanly** (mean mismatch 0.019, p95 0.043, both under
tolerance) — own-ACF **fails** (med 0.15/0.21 across channels) because MEM(1,1)'s single-exponential
persistence cannot reproduce the real data's "fast decay then long plateau" shape (0.41 at lag 1 →
~0.24 by lag 10 → *flat* ~0.24–0.25 out to lag 30). A second lag (MEM(1,2)) and a two-component
(Engle-Lee) extension were both tried in-lens; the former degenerated to MEM(1,1), the latter failed
to converge.

**5. DCC-GARCH** (`dcc_garch.py`): the literal Engle (2002) mean-zero-GARCH DCC spec fails for the
same provable structural reason as CCC's rejected sub-attempt (worse: own-ACF mismatch ~0.43–0.46).
The delivered fix, MEM(1,1)+DCC(1,1), independently reproduces CCC's own finding — cross-correlation
passes after calibration (mean mismatch 0.023, p95 0.049), own-ACF still fails (med 0.15/0.20) for
the identical plateau-shape reason. The fitted DCC dynamic parameters came out essentially
degenerate (a≈1.3e-8, b≈0.067) — i.e., no evidence of correlation *clustering* beyond a constant
level on this pair, so DCC collapses to CCC in practice here; this itself is a disclosed finding,
not an assumption.

**6. Long-memory ARFIMA(1,d,0) + Gaussian copula** (`longmemory_copula.py`): the most informative
lens. Fits a fractionally-integrated AR(1,d,0) process per channel (d≈0.40–0.46, close to the
d=0.5 nonstationarity boundary), directly targeting the observed plateau shape, calibrated via
simulated-method-of-moments (not the naive theoretical ACF, which has known finite-sample bias for
near-nonstationary processes at this n). Two linking variants: `rank_reorder` (literal
Iman-Conover, destroys own-ACF the same way Round 1's shared-start IAAFT did — worse, in fact,
med 0.43/0.46) and `innovation_link` (correlated innovations filtered through each channel's own
fractional filter, no post-hoc reordering) — materially better but still fails the *original*
fixed-tolerance gate (med 0.13/0.14). Crucially, this lens found the SMM-calibrated model's *mean*
surrogate ACF across many draws tracks the real ACF within ~0.02–0.07 at every lag — i.e., it looks
correctly specified on average — and diagnosed the per-draw gate failure as ordinary sampling
variance in a single realization of a near-nonstationary process at n=1487, not misspecification.
This is a materially different failure mode from every other lens: not "wrong functional form,"
not "linking destroys memory," but "the diagnostic itself may be the wrong yardstick for a
genuinely stochastic (non-spectrum-locked) generator."

**7. Nonparametric regime-binned joint block bootstrap** (`regime_block_bootstrap.py`): bins days
by a causal trailing regime proxy, reuses real contiguous (on_range, rth_range) blocks from
within-bin days to build surrogates (preserving cross-dependence almost by construction, since real
pairs are copied verbatim). Cross-correlation passes robustly across a 40+ point grid sweep
(mean mismatch 0.010–0.016). Own-ACF fails at every tested block length (10–300 days) — mechanism
is explicit and disclosed, not mysterious: a block bootstrap can only carry own-autocorrelation up
to roughly its own block length, and pushing the block length long enough to approach the real
data's persistence (which stays elevated to at least lag 30) leaves only ~6 blocks spanning the
whole 1487-day series, degrading both the surrogation itself and inflating cross-surrogate
sampling variance.

**Aggregate finding across all 7 constructions:** cross-correlation preservation is comparatively
*easy* — five different mechanisms (VAR, CCC/MEM-copula, DCC/MEM-copula, block-bootstrap, and
partially the ARFIMA copula) all hit it. Own-channel ACF reproduction is *hard*, and fails for a
consistent, well-triangulated reason: MNQ's `on_range`/`rth_range` exhibit a long-memory-like
"plateau" persistence shape that no short-memory (AR/GARCH/VAR/block-length-bounded) model
reproduces — exactly the class of series the frozen spec's own precedent anticipated
("ARFIMA/FGN... as a fresh design decision") when it named this remedy.

### The gate-redesign attempt, and why it doesn't rescue the ARFIMA lens

Lens 6's own finding (sampling variance, not misspecification) suggested the FIXED per-draw ACF
tolerance (median≤0.04/p95≤0.07, borrowed wholesale from the IAAFT context where surrogates are
spectrum-locked and nearly deterministic) might simply be the wrong diagnostic for a genuinely
stochastic generative model. A follow-up build-and-verify pass tested this directly:

- **Built** (`ensemble_gate_and_positive_control.py`): replaced the fixed tolerance with an
  ensemble/percentile check — for M=120 surrogate draws, take each lag's own [2.5,97.5] percentile
  band across draws and check whether the real ACF falls inside it, with a pre-committed pass bar
  of ≥80% of lags in-band per channel. Result: **100% of lags in-band on both channels, cross-corr
  in-band — gate PASSED.**
- **Adversarially reviewed** (independent agent, byte-level re-derivation of the bands): **CONFIRMED
  FLAWED.** The percentile-band arithmetic itself is correct, but the bands are far too wide to be a
  meaningful specification test — 0.21–0.28 wide for channel 1, 0.27–0.41 for channel 2 at
  representative lags (3–6× the width of the original, already-too-strict fixed tolerance). The
  decisive test: **applying the identical ensemble-gate methodology to the already-rejected VAR(20)
  construction (Round 1) also clears it (100% in-band, passing cross-corr band).** A gate that
  cannot tell a known-inadequate model from the proposed one is not discriminating anything — it is
  wide enough, at n=1487 for this near-nonstationary process class, to admit almost any plausibly-
  shaped model. The docstring's own claim that the surrogate mean tracks the real ACF within
  0.02–0.07 at every lag was independently re-checked and found false on direct recomputation
  (systematic bias up to −0.127 at channel 1 lag 30). **Verdict: the ensemble-gate fix does not
  work as a legitimate own-ACF specification test at this sample size — this is itself a genuine,
  useful negative finding, not merely "back to square one."**
- **Separately, the positive control was ALSO independently adversarially reviewed** (a different
  agent, re-running the same test with 4× the replicates — 80 vs 20 — and fresh seeds never used in
  the original run): **CONFIRMED SOUND.** Null false-positive rate on the larger re-run: 1/80=1.3%
  (mildly conservative, safe direction — the original 20-rep estimate of exactly 5% was "luck of a
  small sample," not wrong in direction). Power at the original effect size: 36/80=45% (vs the
  original 20-rep 50%); power at a smaller, more subtle effect: 25/80=31% — power scales sensibly
  and monotonically with injected effect size, which the reviewer specifically checked as evidence
  against a "too-wide-to-reject-anything" null (the exact failure mode of this repo's own retired
  block-shuffle placebo). Null p-values pass a formal KS-uniformity check (stat=0.158, p=0.0325 —
  a real, mild, conservative departure, not gross miscalibration); null and alternative p-value
  distributions are clearly separated (means ≈0.58–0.60 vs ≈0.10–0.15), ruling out a degenerate
  null that never rejects in either scenario.

**Net result at Round 2 (CORRECTED by Round 3 below — do not stop reading here): the
surrogate-generation-and-testing MACHINERY (Step 2, the positive control) is independently
verified sound UNDER KNOWN-TRUE MODEL PARAMETERS. The MODEL-ADEQUACY diagnostic (Step 1, the ACF
gate — in either its original fixed-tolerance or its redesigned ensemble-percentile form) is
independently verified inadequate at this sample size for this process class.** Round 3 found
that the "known-true parameters" caveat is load-bearing, not incidental — see below.

### A suggestive, EXPLORATORY-ONLY, NOT-CERTIFIED finding worth an operator's attention

As a disclosed illustration (not a scored Phase 3 result — the model-adequacy caveat above applies
in full), the ARFIMA-copula construction was run once against the real `candidate24_joint_frame.csv`
data: observed stage-1 statistic = +0.3798, surrogate null-lift mean = +0.408 (sd 0.038),
**p_upper = 0.785**. The real observed effect sits comfortably *inside*, in fact slightly below the
mean of, this null's own distribution — i.e., under a null that accounts for shared long-memory
regime dynamics plus a constant same-day linear correlation, the observed "incremental lift" H-
RANGEXFER-1's stage-1 test found does **not** look unusual. This is directionally consistent with
(does not newly establish) a possibility worth naming explicitly for whoever picks up Phase 3: the
day-history-only stage-1 filter may not be controlling for the *right* confound, and the eventual
Phase 3 verdict could plausibly land FALSIFIED rather than the stage-1-suggested GRADUATE, once a
properly-specified joint null is actually certified and run for real. **This is a lead, not a
verdict — the model behind it has not cleared model-adequacy per the section above.**

## Recommendation for a future session (updated after Round 2)

1. **Do not keep trying more parametric models hoping one clears an ACF-based gate** — Round 2's
   own finding is that ACF-based specification testing appears to lack the power to discriminate
   models at n=1487 for this near-nonstationary process class, independent of which model is tried.
   Chasing a "passing" ACF diagnostic here is very plausibly a dead end.
2. **Live option A — theory-first model acceptance + cross-model robustness, not curve-fitting
   certification:** accept the ARFIMA-copula (or another mechanistically-motivated) construction on
   theoretical grounds (long-memory volatility clustering is a well-established stylized fact for
   realized-range-type series — not novel to this data), and instead of certifying model adequacy
   via an ACF gate, check whether the eventual Phase 3 verdict is ROBUST across several plausible
   model specifications (e.g., ARFIMA-copula, MEM-copula, and a longer VAR, all of which are now
   built and available in this directory) rather than resting on any single model being "proven
   correct."
3. **Live option B — a fundamentally different model-adequacy check:** out-of-sample forecast
   evaluation (does the fitted model predict held-out range values better than a naive benchmark?)
   or a formal information-criterion-based comparison between candidate models, rather than an
   absolute ACF-percentile check, which Round 2 showed cannot discriminate at this n.
4. Either way, before any Phase 3 execution, the exploratory p_upper=0.785 finding above deserves a
   properly-certified re-run (not a repeat of this session's disclosed compute-budget
   simplifications — fixed φ/d rather than per-replicate recalibration) — it is the single most
   concrete, actionable number this entire two-round exploration produced, and if it holds up under
   a certified re-run, it would materially change Q-RANGEXFER-1's own eventual verdict.

## What this means for Q-RANGEXFER-1 / Q-VOLREGIME-1's own Phase 1/2/3 sequencing

Phase 1 (design) is **not complete to a certifiable standard** — the surrogate-testing machinery is
validated only under known-true parameters (Round 3 found real, meaningful Type-I inflation once
parameters are estimated, the only way the procedure could ever actually run), and model adequacy
is separately not established either. Phase 2 (adversarial review) has been informally discharged
for the machinery's mechanics (the generate → score → p_upper pipeline is bug-free and correctly
implements its own stated design) but NOT for the machinery's actual operating characteristics
under estimation (Round 3) or for model adequacy (Round 2) — a future session owes both a
from-scratch model-adequacy strategy AND an estimation-aware size/power re-certification per the
recommendations above before Phase 3 can proceed.
Phase 3 (K declaration + operator GO + execution) cannot proceed on either brief's
H-RANGEXFER-1-class or H-VOLREGIME-class hypotheses until model adequacy is certified. This does
**not** affect Q-VOLREGIME-1's own Phase 0.5 precondition (already cleared, separately, earlier this
session — see that brief's own §4/§7) or either brief's already-scored stage-1 results, which stand
as measured and are unaffected by this unresolved stage-2 design question.

## Runnable artifacts (for a future session to pick up from)

Round 1: `joint_iaaft.py` (VAR(p), current implementation; own docstring documents the superseded
linked-residual version) · `positive_control.py` (size/power harness, reusable against any
`generate_joint_surrogates`).

Round 2: `ccc_garch.py` · `dcc_garch.py` · `longmemory_copula.py` (both `rank_reorder` and
`innovation_link` variants; **the most promising lens** — see Round 2 above) ·
`regime_block_bootstrap.py` · `_fit_real_params.py` / `_real_fit_cache.json` (the SMM-calibrated
ARFIMA parameters: channel1 on_range phi=-0.225/d=0.397, channel2 rth_range phi=-0.225/d=0.458,
rho_innov=0.800 — cached so a future session does not need to re-fit) ·
`ensemble_gate_and_positive_control.py` + its own `_results.json` (the gate-redesign attempt and
the independently-verified positive control — **this is the file a future session should start
from**: its Step 2 machinery is validated, only its Step 1 gate needs replacing per the
recommendations above) · `_adversarial_rerun.py` + `_results.json` (the independent 80-rep
re-verification).

```bash
# Reproduce the VAR(p) diagnostic-gate FAIL on real data (Round 1)
python -c "
import pandas as pd
from joint_iaaft import generate_joint_surrogates
df = pd.read_csv('../mnq_dailygeom_notice_2026-08-29/candidate24_joint_frame.csv')
pairs, diag = generate_joint_surrogates(df['on_range'].to_numpy(), df['rth_range'].to_numpy(), M=30, seed_base=1, code=0, p=20)
print(diag['gate'], diag['channel1_acf'], diag['channel2_acf'])
"
# Expected: gate=FAIL, channel1/2 med mismatch ~0.10-0.13 (>> 0.04 tolerance)

# Reproduce the univariate IAAFT borderline baseline on rth_range alone (Round 1)
python -c "
import pandas as pd, sys
sys.path.insert(0, '../mym_mechanism_harvest_2026-08-29')
from iaaft_battery import generate_surrogates
df = pd.read_csv('../mnq_dailygeom_notice_2026-08-29/candidate24_joint_frame.csv')
_, diag = generate_surrogates(df['rth_range'].to_numpy(), M=30, seed_base=1, code=1, acf_lags=30, n_iter=100)
print(diag)
"
# Expected: gate=FAIL, med~0.040 (just over the 0.04 tolerance -- a near-miss, not a clean pass)

# Reproduce the ensemble gate PASS + the smoking-gun VAR(20) also-passes finding (Round 2)
python ensemble_gate_and_positive_control.py
# Expected: gate_passed=true (100% lags in-band both channels), positive-control null_rate=0.05,
# alt_rate=0.5, exploratory real p_upper=0.7851 -- see ensemble_gate_and_positive_control_results.json

# Reproduce the independent 80-rep re-verification (Round 2 adversarial check)
python _adversarial_rerun.py
# Expected: null false-positive rate close to 1-3% (mildly conservative), power ~31-45% depending
# on injected effect size, KS-uniformity check on null p-values does not show gross miscalibration
```

## Round 3 — Codex review (PR #219): 4 real code bugs found and fixed, 1 major conclusion corrected

An external (Codex) review pass on the PR carrying this file's Round 1/2 work found 6 substantive
issues. Each was independently re-verified against the actual code (not taken on faith) before
fixing. Four were confirmed real bugs with quantified impact; one was a confirmed but
already-partially-disclosed methodological gap that this round closed with an actual empirical
check rather than more disclosure text; one was a confirmed doc-staleness issue (fixed, see the
brief/notice/ledger updates in this PR, not detailed further here).

**1. Positive control validates machinery only under known-true parameters (the big one).**
Round 2's own positive control (`ensemble_gate_and_positive_control.py`, and its own independent
80-rep re-verification, `_adversarial_rerun.py`) passed the SAME cached real-panel-fitted
`(phi,d,rho_innov)` into every synthetic replicate as both ground truth AND surrogate-generation
parameters. This validates the generate→score→p_upper PIPELINE's mechanics, but not the actual
procedure that would run on real, previously-unseen data, which must ESTIMATE `(phi,d)` first.
Built `_refit_per_replicate_positive_control.py`: for each replicate, `(phi,d,rho_innov)` is
RE-ESTIMATED from that replicate's own synthetic data (not read from cache) via the same
simulated-method-of-moments approach `longmemory_copula.py` already implements, at a deliberately
coarse grid (phi_grid 7pts × d_grid 8pts × n_reps_calib=2 × J/burn=300, vs the production
21-31pts × 25-50pts × 5-6 × J/burn=1200-2000 — a disclosed compute-budget simplification, N=8
replicates per scenario vs the original 20/80). **Result: null false-positive rate 2/8 = 25% (vs
the fixed-parameter run's 5%) — a real, meaningful Type-I inflation, not a rounding artifact.**
Power held roughly steady (4/8 = 50% vs the fixed-parameter run's 50%). The coarse grid likely
overstates the true production-grade inflation (a finer grid should estimate `(phi,d)` more
precisely, reducing estimation noise) — but the QUALITATIVE finding, that fixed-parameter
validation materially understates the real false-positive rate, is now empirically demonstrated,
not merely a theoretical possibility. **This corrects Round 2's own "machinery CONFIRMED SOUND"
headline** — see the corrected "Net result" line above. The exploratory real-data p_upper=0.785
finding itself used the production-grade (not coarse) SMM fit from `_fit_real_params.py`, run once
directly on the real data — it is not undermined by this finding in the same way the SYNTHETIC
positive control's own size/power claim is, but its own single-fit `(phi,d)` estimate now carries
a disclosed extra layer of estimation uncertainty (per this section's own finding, plausible
alternative fits within the same uncertainty band could shift the exact 0.785 figure, though a
modest shift is very unlikely to flip a result this far from the 0.05 boundary into significance).

**2. CLV cost-screen block-bootstrap destroyed event chronology (both MNQ and MYM).**
`candidate5_clv_cost_screen.py` / `c5_clv_cost_screen.py` built their block-bootstrap input by
`np.concatenate([top_trade_bp, bot_trade_bp])` — ALL top-decile events (in their own time order)
followed by ALL bottom-decile events (in their own time order). For serially dependent M15 range
data, a block=96 window drawn from either half no longer approximates any real time span (most of
a block shares one signal type; at ~20% event frequency, neighboring elements in a decile-only
sub-array can be years apart in real time). **Fixed:** build one chronologically-ordered signed
event series via a single combined boolean mask (`event_mask = top_mask | bot_mask`; boolean
masking preserves original array order), then block-bootstrap that. This is a real semantic shift,
disclosed rather than silently kept: block=96 now means "96 consecutive QUALIFYING EVENTS in their
real occurrence order" (≈480 real bars, ≈5 sessions at this event frequency), not "~1 session of
raw bars." **Re-run, both instruments: the mean edge is UNCHANGED (concatenation vs. chronological
ordering doesn't change the mean of the same set of values), only the CI shifts slightly** — MNQ
[−0.0358,+0.3154] → [−0.0381,+0.3244] (same qualitative FAIL, straddles 0 either way); MYM
[+0.2328,+0.4835] → [+0.2436,+0.4822] (same qualitative FAIL against the 6.57bp hurdle, though the
rounded 2-decimal lower bound moves from 0.23 to 0.24 — both notices/`MECHANISMS.md`/`MYM.md`
updated to the corrected figures). **No disposition changed** (both CLV notices' DROP stands).

**3. MNQ bar-volume-regime outcome silently converted a missing threshold to a false "not
elevated" reading.** `candidate3_volume_regime.py` (pre-existing, not authored this session) and
this session's own `candidate3_stratified_rerun.py` both built `y[:-1] = (rng_bar[1:] >
rng_thresh_tod[1:]).astype(float)`. When a next bar's own ToD-slot threshold is NaN (early-panel
bars whose slot hasn't yet reached `TRAIL_N=60` prior occurrences), `rng_bar[1:] > NaN` evaluates
to `False` (numpy: any comparison against NaN is False) and `.astype(float)` silently produced
`0.0` instead of `NaN` — those rows passed the `scored` mask with a FABRICATED "not elevated"
outcome instead of being excluded, exactly the class of defect the MYM sibling script's own
`np.where` guard already prevented. **Fixed in both files** with the same `np.where(~np.isnan(...),
..., np.nan)` guard MYM already used. **Re-run, both scripts: numbers move negligibly** (the
affected fraction is a small, early-panel slice) — marginal ToD-matched range lift +19.1pp → +19.1pp
(0.69557 vs 0.69529, same to the precision already cited); stratified lift +22.3pp/+27.4pp →
+22.3pp/+27.4pp (0.2234/0.2739 vs 0.2232/0.2740), both strata still p=0.00025. **No disposition
changed.**

**4. `longmemory_copula.py` hardcoded the author's absolute Windows worktree path** in its
`__main__` block instead of resolving `candidate24_joint_frame.csv` relative to the module's own
location — would raise `FileNotFoundError` on any other checkout even though the CSV is tracked in
the adjacent analysis directory. **Fixed** with `Path(__file__).resolve().parent.parent / ...`,
matching the convention `_fit_real_params.py` and `ensemble_gate_and_positive_control.py` already
used.

**5. Ordinal (not average-rank) tie-breaking in `normal_scores`.** `joint_iaaft.py`,
`ccc_garch.py`, and `longmemory_copula.py` all defined `normal_scores` using
`np.argsort(x, kind="stable")`, which assigns DISTINCT sequential ranks to exactly-tied values in
original (temporal) array order — inventing a spurious within-tie time ordering before any
downstream fit sees the data. The real `on_range`/`rth_range` panel is materially discrete (455 /
495 duplicate rows respectively, per the review), and every diagnostic in these modules already
uses `rankdata`'s average-tie convention, creating a real internal inconsistency. **Fixed** in all
three files to use `rankdata(x, method="average")`. **Checked impact directly** (not assumed
negligible): `ccc_garch.py` and `longmemory_copula.py` define this function but never actually
CALL it anywhere in their real generation pipelines (confirmed by exhaustive grep for call sites,
not just the definition) — the fix there is correct hygiene with zero numeric impact on any
reported figure. `joint_iaaft.py`'s VAR(p) construction DOES call it; re-ran its own audit hook
post-fix: channel1/channel2 ACF mismatch and cross-correlation mismatch move by <0.001 at the
4th decimal place, no qualitative change to the FAIL verdict or the smoking-gun comparator result
Round 2's own gate-legitimacy review relied on.

**6. Stale precondition-status restatements after Q-VOLREGIME-1's precondition cleared.** Three
locations still stated or implied "neither instrument's within-stratum significance is
null-calibrated" / "UNRESOLVED, vendor-blocked" after the actual precondition-clearing work (this
same session, prior commit) had already updated the brief's own §4/§7: `Q-VOLREGIME-1`'s own §3
Sub-questions text, `N-2026-08-29-mym-bar-volume-regime.md`'s Pre-Q summary line, and — the most
stale of the three — `ops/instruments/MYM.md`'s entire `intraday-bar-volume-regime` bullet, which
had never been touched by the precondition-clearing edit at all and still read the ORIGINAL
UNRESOLVED disposition in full. **Fixed all three** to state the current (cleared) status,
consistent with the ledger cell, `MECHANISMS.md`, and the notice's own Status header, which were
already correct.

**Net effect of Round 3 on prior conclusions:** items 2, 3, 5, and the doc-staleness item are
confirmed real defects with negligible-to-no numeric impact on any disposition already recorded —
DROP/INCREMENT verdicts for CLV and bar-volume-regime are UNCHANGED, only exact CI/precision
figures were corrected where they moved. Item 1 is the substantive one: it downgrades Round 2's
own claim that the joint-surrogation null's testing machinery is "confirmed sound" to "confirmed
sound only under an assumption (known-true parameters) that does not hold for the actual use case,
and relaxing that assumption produces a real, measured Type-I inflation." Phase 1 is further from
resolved than Round 2's own headline stated, not closer.

```bash
# Reproduce the refit-per-replicate Type-I inflation finding
python _refit_per_replicate_positive_control.py
# Expected: null reject rate 2/8=0.25 (vs the fixed-parameter run's 0.05), alt reject rate 4/8=0.50

# Reproduce the corrected CLV cost-screen CIs (mean edge unchanged)
python ../mnq_dailygeom_notice_2026-08-29/candidate5_clv_cost_screen.py
# Expected: mean=+0.1402 bp/event, CI=[-0.0381,+0.3244]
python ../mym_mechanism_harvest_2026-08-29/c5_clv_cost_screen.py
# Expected: mean=+0.3609 bp/event, CI=[+0.2436,+0.4822]

# Reproduce the corrected MNQ bar-volume-regime figures (NaN-handling fix)
python ../mnq_dailygeom_notice_2026-08-29/candidate3_volume_regime.py
# Expected: ToD-matched range lift ~0.1911 (n_scored=135958, down slightly from 136020 pre-fix)
python ../mnq_dailygeom_notice_2026-08-29/candidate3_stratified_rerun.py
# Expected: strata lifts 0.2234/0.2739, both null-calibrated p=0.00025
```
