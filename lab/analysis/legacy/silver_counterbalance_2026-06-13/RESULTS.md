**Theme:** legacy
**Status:** ACTIVE — Silver counterbalance equity curve & required-hedge envelope
# Silver counterbalance — equity curve & required-hedge envelope (2026-06-13)

**Question (Joshua):** build the 2020–2026 equity curve for the available strategies
*including* Guardian Silver, and from it deduce the **range of equity curves** a
counterbalancing 6th leg would need to offset Silver's H1 (2020–2023 chop)
underperformance — i.e. to clear the §9 H1-neutrality gate in
`docs/ltm/briefs/2026-06-11-guardian-silver-v1-admission-override.md`.

**Status:** EXPLORATORY (lab/). No `core/` mutation, no lock. Reuses the locked MC
primitives and the 2026-06-07 decompound preprocessor verbatim.

## Basis (forced by the question)
Decompounded **static $200K**, path-independent (`decompound.rebank(..., "static")`).
This is the *only* basis on which Silver's H1 underperformance exists — the compounded
canonical view shows Silver Pareto-positive (99.90/0.10/4.31). Panel = 1672 bdays,
2020-01-06 → 2026-06-02; gate midpoint split: **H1** 2020-01-06→2023-03-20 (836 bd,
chop), **H2** 2023-03-21→2026-06-02 (836 bd, trend). Silver = decompounded `11d4b`
(BE-on H1-faithful proxy, per §3.1 of the brief), 0.15%.

## 1. Equity curve (deterministic, static $200K)

| Window | 4-strat | +Silver 0.15% | Silver Δ |
|---|---|---|---|
| Full net | +$716,810 | +$788,274 | +$71,464 |
| Full maxDD | 9.84% | 10.81% | **+0.96pp** |
| H1 net | +$84,559 | +$77,396 | **−$7,163** |
| H1 maxDD | 9.84% | 10.81% | +0.96pp |
| H2 net | +$632,251 | +$710,878 | +$78,627 |

**Why Silver hurts H1:** in H1 it loses **−$15,395 while the book is already
underwater** (+$8,232 while at peak); daily **corr(Silver, book) = +0.177** — it
bleeds *with* the book. That drawdown-coincident bleed is what turns the bootstrap
H1 bust 24.54% → 29.82% (a +0.96pp deterministic DD amplifying to +5.28pp bust
under week-block resampling). In H2 Silver nets +$78.6K — it pays in the trend.

## 2. Gate reproduced (validates the construction)

| | H1 bust | H1 p99 | H2 bust | H2 p99 |
|---|---|---|---|---|
| 4-strat baseline | 24.54% | 8.57% | 0.54% | 4.87% |
| +Silver 0.15% | 29.82% | 8.85% | 0.40% | 4.80% |

Matches `silver_regime_gate_full_2026-06-10.py` / §9 exactly. Gate: 6-strat **H1 bust
≤ 24.54% AND H1 p99 ≤ 8.57%**, and H2 must stay bust<1% / p99<5%.

## 3. Deduced counterbalance envelope (gate-validated)

Synthetic 6th leg X swept against the locked MC on the H1/H2 half-panels.

**(a) H1 magnitude — the floor.** X must supply **≈ +$22–24K of *drawdown-coincident*
PnL** across H1. The **binding** constraint is **H1 p99 DD ≤ 8.57%**, stricter than
H1 bust ≤ 24.54%:
- H1 bust clears at ~$12K underwater (α≈0.20); H1 p99 not until ~$21–24K (α≈0.36).
- Realistic "smart" hedge (gains only on book down-days, ~zero premium): **net +$24K → PASS** (H1 bust 20.6%, p99 8.49%); +$20K → FAIL (p99 8.57%).

**(b) H1 shape — the binding qualitative constraint.** corr(X, book) **≤ 0** in H1.
Same +$24K earned on book **UP-days** (corr>0) → H1 bust **46.4%** — catastrophically
worse than +Silver's 29.82%. **Timing dominates magnitude.** "Regime-complementary,
not instrument-decorrelated" (§9) is the literal requirement.

**(c) H2 ceiling.** X may bleed at most **≈ $45K net across H2** (2023–2026). Binding
= H2 p99 < 5% (crosses at ~$48–50K); H2 bust stays <1% well past. Beyond ~$45K the
trend-regime cost breaks H2.

### Equity-curve statement of the range
X's curve must **rise ~$22–24K through 2020–2023, concentrated in the book's drawdown
windows** (esp. the 2022 selloff), then **drift down by no more than ~$45K through
2023–2026**. Full-period net may sit anywhere from ~+$24K (premium-free hedge) down to
~−$20K (continuous-premium hedge), provided the H1 shape (corr≤0) and H2 ceiling hold.
See `silver_counterbalance.png` panel C.

## 4. Realism
A leg that gains in 2020–2023 chop and only mildly bleeds in the 2023–2026 trend is
structurally counter-trend / mean-reversion / vol — the opposite of the ~4.5/5
trend-long book. The envelope is narrow (H2 headroom only ~$45K; H1 timing near-perfect),
and the rejected-candidates registry (ORATS short-vol, Aegis SHORT v0.1) is the
graveyard of prior swings. Consistent with §9's "honest base rate is low."

## Reproduce
```
# inputs/ must hold the six 2026-06-07 Pepperstone exports (gitignored; see ../decompound_remc_2026-06-07/inputs/README.md)
python equity_curves.py            # deterministic curves + H1 decomposition -> curves.csv
python counterbalance_envelope.py  # gate reproduction + (alpha, H2-drag) sweep -> envelope_sweep.csv
python refine_boundaries.py        # pinned boundaries + realistic smart-hedge test
python plot_curves.py 24000 45000  # 3-panel figure -> silver_counterbalance.png
```
