# RESULTS — Phase 1 joint-surrogation null design exploration (Q-RANGEXFER-1 / Q-VOLREGIME-1)

**Status: NOT RESOLVED.** Three candidate designs were built and empirically tested against a
positive control (synthetic data with a known ground truth) and/or directly against the real
cached `on_range`/`rth_range` joint frame. All three fail their own diagnostic gate, in two
precisely opposite ways. This is a genuine, evidenced negative finding, not a completed design —
Phase 2 adversarial review has nothing ready to review yet on this specific sub-problem. Written
up in full because the evidence itself (which constructions fail, and exactly how) is the
load-bearing output of this session's Phase 1 attempt and materially narrows what a future
session should try next.

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

## Recommendation for a future session (not executed here)

Per the frozen spec's own precedent for exactly this class of failure (diagnostic-gate FAIL after
a reasonable escalation attempt → CASE V VOID → "pre-named remedy is a different surrogate class
(ARFIMA/FGN or GARCH-fitted) as a fresh design decision with its own review"), the two candidates
worth trying next are:

1. **A shared-latent-GARCH joint model**: model both channels as driven by a common GARCH-type
   latent volatility process (explicitly built for exactly the kind of persistent, non-Gaussian
   volatility clustering that both a finite VAR and, marginally, plain IAAFT struggle with on this
   data), with channel-specific idiosyncratic innovations. This is a materially larger design
   effort — a fresh design decision with its own review, not a quick fix.
2. **Accept the VAR(p) approximation explicitly, with its own-ACF shortfall disclosed as a named
   limitation** and used only for a conservative sensitivity check (e.g., "even under a
   deliberately imperfect joint null that undersells each channel's own persistence, does the
   stage-1 lift still look unremarkable?") rather than a precise Type-I-controlled test — a much
   weaker claim than Phase 3 execution is supposed to support, and probably not sufficient on its
   own to certify RESOLVED/FALSIFIED under either brief's own §6 gate criteria.

Neither of these was built or evaluated this session — named here as the two live options, not
implemented.

## What this means for Q-RANGEXFER-1 / Q-VOLREGIME-1's own Phase 1/2/3 sequencing

Phase 1 (design) is **not complete** — the joint-surrogation null does not yet exist in a form
that passes its own positive control. Phase 2 (adversarial review) has nothing ready to review on
this specific sub-problem. Phase 3 (K declaration + operator GO + execution) cannot proceed on
either brief's H-RANGEXFER-1-class or H-VOLREGIME-class hypotheses until a design clears Phase 1.
This does **not** affect Q-VOLREGIME-1's own Phase 0.5 precondition (already cleared, separately,
this session — see that brief's own §4/§7) or either brief's already-scored stage-1 results, which
stand as measured and are unaffected by this unresolved stage-2 design question.

## Runnable artifacts (for a future session to pick up from)

- `joint_iaaft.py` — current implementation is the VAR(p) approach (its own module docstring
  documents the superseded linked-residual version in full and the "what this null actually
  tests" framing, which remains a correct and relevant conceptual note for whichever construction
  eventually succeeds).
- `positive_control.py` — the size/power self-check harness; re-runnable against whatever
  `generate_joint_surrogates` implementation lands in `joint_iaaft.py`. Its own two synthetic
  scenarios (shared-regime-only null; shared-regime-plus-genuine-transmission alternative) are
  reusable without modification for validating a future design.

```bash
# Reproduce the VAR(p) diagnostic-gate FAIL on real data
python -c "
import pandas as pd
from joint_iaaft import generate_joint_surrogates
df = pd.read_csv('../mnq_dailygeom_notice_2026-08-29/candidate24_joint_frame.csv')
pairs, diag = generate_joint_surrogates(df['on_range'].to_numpy(), df['rth_range'].to_numpy(), M=30, seed_base=1, code=0, p=20)
print(diag['gate'], diag['channel1_acf'], diag['channel2_acf'])
"
# Expected: gate=FAIL, channel1/2 med mismatch ~0.10-0.13 (>> 0.04 tolerance)

# Reproduce the univariate IAAFT borderline baseline on rth_range alone
python -c "
import pandas as pd, sys
sys.path.insert(0, '../mym_mechanism_harvest_2026-08-29')
from iaaft_battery import generate_surrogates
df = pd.read_csv('../mnq_dailygeom_notice_2026-08-29/candidate24_joint_frame.csv')
_, diag = generate_surrogates(df['rth_range'].to_numpy(), M=30, seed_base=1, code=1, acf_lags=30, n_iter=100)
print(diag)
"
# Expected: gate=FAIL, med~0.040 (just over the 0.04 tolerance -- a near-miss, not a clean pass)
```
