# Q-REGIME-RATEVOL-1 — rate-vol participation-gate screen (2026-06-16)

**Verdict: FALSIFIED.** Exogenous US-Treasury rate volatility does **not** carry regime-hardness
information beyond the gold-anchored participation gate — and barely separates this portfolio's regime
at all. Pre-registration `c30b287` (committed before analysis). Brief:
[`docs/ltm/briefs/Q-REGIME-RATEVOL-1.md`](lab/archive/../../docs/ltm/briefs/Q-REGIME-RATEVOL-1.md); closure:
[`Q-REGIME-RATEVOL-1-closure-falsified.md`](lab/archive/../../docs/ltm/briefs/Q-REGIME-RATEVOL-1-closure-falsified.md).

## Headline numbers

- **Marginal AUC ≈ 0.50** (dgs10_63 0.498; dgs2_63 **inverted** 0.418) — rate-vol does not separate the regime.
- **Conditional AUC on gold-DEPLOY subset: 0.582** (bar 0.70; inside the [0.40,0.60] FALSIFIED band), 0.563 ex-2022, LOYO-min 0.538 — fails every floor.
- Blind spot is real (gold DEPLOYs on 187 hostile-ahead starts) but rate-vol flags them at ≈chance.

## Mechanism — rate-vol is anti-aligned with the regime

| Year | Hostile-ahead % | 63-bd DGS10 rate-vol |
|---|---:|---:|
| 2021 | **83%** (deepest hostile) | **0.644** (lowest) |
| 2023 | **22%** (benign) | **1.189** (highest) |

The hostile regime was a ZIRP-era **low-bond-vol** gold chop; rate-vol spiked on the *exit* (2022 hiking).
The "rate-vol → chop" intuition is empirically backwards here. MOVE (implied) was the gated Stage-2 upgrade,
not reached — the falsification is mechanism-level and would apply to it too (bond vol was suppressed under
ZIRP/QE in the hostile period).

## Reproduce

```
PYTHONPATH=core python lab/analysis/regime_ratevol_2026-06-16/ratevol_screen.py
```

Reuses the locked MC primitives (`core/portfolio_mc`) + the PR #157 decompound preprocessor +
`participation_check`'s forward-start sweep recipe. Needs the gitignored Pepperstone decompound `inputs/`
+ an OANDA key (XAUUSD daily, for the gold gate). FRED DGS10/DGS2 fetched freely (public-domain).
Raw fetched series are cached local-only (`.gitignore`d); the `.json` result + this `RESULTS.md` are tracked.
No `core/` / locked-config change anywhere — research only; the gold shadow gate is unchanged.
