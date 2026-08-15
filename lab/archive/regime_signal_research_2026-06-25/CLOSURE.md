# Regime-signal battery — CLOSURE (NULL, power-limited) — 2026-06-25

**Disposition:** CLOSED — NULL — no candidate clears FWER with correct sign

**Question (the "expensive" one):** is there a FREE / TradingView-exportable **exogenous** signal that
flags the book's H1 **co-drawdown** regime — to drive regime-adaptive sizing (and maybe seed a 5th leg)?

**Method:** pre-registered episode-level permutation battery, frozen after **3 adversarial review rounds**
(v1 single-asset-ER, v2 daily-rolling regression — both rejected fix-fatal-first; v3.1 converged).
[PREREG v3.1](lab/archive/../../docs/ltm/briefs/pre-registration/PREREG-REGIME-CHOP-ORTHOGONALITY-2026-06-25.md);
harness `run_battery.py`; `battery_result.json`. N=34 raw co-drawdown episodes (33 used; 1 early-2020
dropped for <21d vol window). Partial-Spearman of each signal **at the pre-drawdown peak** vs static-$
episode severity, residualized on **realized vol + calendar**, 20k-permutation, max-|ρ| FWER, seed 20260625.

## Result — NULL
| candidate | class | reg.sign | ρ_partial | raw ρ | p_FWER | verdict |
|---|---|--:|--:|--:|--:|---|
| RCORR | within-equity | + | **−0.276** | +0.067 | 0.46 | fail (wrong sign) |
| NFCI | cross-asset | + | −0.157 | +0.025 | 0.90 | fail (wrong sign) |
| S5FI | within-equity | − | +0.097 | +0.153 | 0.99 | fail (wrong sign) |
| RDISP | within-equity | − | +0.037 | +0.217 | 1.00 | fail (wrong sign) |
| COR3M | within-equity | + | −0.033 | **+0.328** | 1.00 | fail (confound) |

**No candidate clears FWER<0.05 with the correct sign.** Premise confirmed: realized vol does NOT rank
severity (Spearman +0.159, p=0.378) → the episodes are a real beyond-vol target; calendar does (−0.459,
p=0.007) → controlled.

**Load-bearing catch (rigor paid off):** COR3M raw ρ **+0.328** (a tempting "signal") → **−0.033** after
removing the calendar/secular-decline confound. Without the calendar control it would have been a false
positive — exactly the v3-review F1 trap. The mechanistically-right cross-asset NFCI is also null.

**Untestable (logged, pre-result):** ICORR (4-instrument corr) + HURST (4-leg 15m) need full-history DJ30
+ USDJPY 15m bars, absent on disk (only NAS100/gold full); both are the pre-reg's endogenous/redundant
candidates. Family run at M=5 (the exogenous + within-equity set — the actual question).

## Disposition — HOLD; scoped closure
- **No FREE exogenous signal in the tested family discriminates the book's co-drawdown episodes beyond
  vol+calendar, at N=33 (power-limited to |ρ|≈0.36).** NOT "no exogenous signal exists" — a weaker-but-real
  effect is not excluded; re-opening needs MORE ACCRUED EPISODES or a NEW signal family, not a re-tune.
- **Combined with the prior H1-fix closures** — static de-risk (2026-06-07), dd-trigger (Q-DDTRIG-1),
  VIX-brake (Q-REGIME-ADAPT-1.T2b), 5th-leg (target-spec) — the H1 chop tail has **no free, detectable,
  static-or-simple-adaptive fix at current data resolution.** The only remaining theoretical levers are
  **PAID** exogenous data (options-flow / dealer-gamma with orthogonal separation — operator excluded by
  the free-only constraint) or **more accrued co-drawdown episodes** over time. Both deferred.
- **Lock HELD** (99.83 / 0.17 / 4.37); H1 tail managed operationally + quarterly regime trigger 2026-08-08.

## Durable methodology lesson
A handful (~34) of co-drawdown episodes + highly-persistent free signals is **intrinsically low-power**;
mechanism + confound-control must lead, not backtest payoff (Dacco-Satchell). The **calendar/secular-trend
confound nearly manufactured a COR3M positive** — any regime-signal regression on these persistent series
MUST residualize on calendar, or it re-discovers the trend. Three adversarial rounds were necessary to
reach a design whose NULL is trustworthy (and which refused a tempting false positive).
