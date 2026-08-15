# USDCAD 15m strategy reverse-engineering — RESULTS

**Date:** 2026-06-14 · **Operator:** Joshua · **Engine:** Claude (Opus 4.8), INQHIORI loop
**Data:** `BAR_EXPORT_v0.1_PEPPERSTONE_USDCAD_2026-06-14_506df.csv` — 15m USDCAD, Pepperstone/TV, 11,048 bars, 2026-01-01→06-12 (**single ~5.4-month regime, zero true OOS**).
**Endpoint:** exploratory candidate + caveats. **Approach:** disciplined pre-registered pattern-search.

## Verdict: NULL — no robust price-action strategy from this window.

Two pre-registered loops, both NULL. The deflation discipline did its job: it blocked an overfit and produced verifiable results.

| Loop | Mechanism | Pre-reg | Outcome |
|---|---|---|---|
| 1 | Volatility breakout (Donchian + ORB), long-short | `PREREG-USDCAD-BREAKOUT-2026-06-14.md` | **NULL** — falsified, convention-robust |
| 2 | Trend-pullback (`ema_recovery`), long-short | `PREREG-USDCAD-PULLBACK-2026-06-14.md` | **NULL** — fails cost gate AND selection gate (DSR) |

## Loop 0 — Notice-phase characterization (TZ-corrected)

- **Step-0 integrity:** clean (0 decode/cross-check/OHLC/dup failures; 15m confirmed; 99.8% contiguous).
- **Timezone finding (load-bearing):** the file clock is **UTC, not ET** despite the filename. Weekend gap tracks DST (Fri 21:45→Sun 22:00 winter; −1h after 2026-03-08). TV chart was ET; the strategy-tester export emits the bar epoch in UTC. **All session logic uses UTC→ET (DST-aware) conversion.** Uncaught, every session gate would be 4–5h wrong.
- **Structure:** mean-reverting (VR<1 at every horizon 0.96→0.76; ACF lag1 −0.037; Hurst 0.56). **No** directional momentum at any TF. **Strong vol clustering** (|ret| ACF +0.248). **NY-morning concentration** (ET 08–11 range ~3× overnight; peak ET 10:00 11.3p; Wed 10:00 EIA spike). **Intra-window vol compression** −28% (Jan→Jun).
- **Cost law (durable finding #1 reproduced):** median ATR 5.2p; tight stops crippling, k≥2 needed.

## Loop 1 — Breakout: NULL (falsified)

960 configs, 734 eligible (n≥100). **0 positive net; 0 clear the cost hurdle.** Negative even **gross** (mean −0.10R; only 3.7–5.9% positive). Robust to **both** fill conventions (next-open AND intrabar stop-level/turtle). NY-morning was the **worst** session — vol concentration does not become breakout edge; **breakouts fade**, asymmetrically (up-breakouts fade −0.43R/24bar; down-breakouts flat).

**Independent verification:** 3-agent adversarial audit (`workflow wf_6f3dce37`) — TRUSTWORTHY, no finding-flipping bug. Found only 2 minor symmetric defects (STOP-FIRST ~0.018R bias, ATR seed); from-scratch reimplementation matched; honest random-walk null floor ~−0.04R.

## Loop 2 — Trend-pullback: NULL (real-looking, selection artifact)

960 configs, 916 eligible. **20.9% positive**, best +0.148R (fast20/slow200, NY-morning, k1.5, tp1.5). Passed every **parameter-conditional** check — but **failed the two gates that matter:**

- **Cost-hurdle gate: FAIL** — best +0.148R vs required 4×-hurdle 0.39R; `pass_hurdle = 0/916`.
- **Selection gate (DSR, pre-registered gate 4): FAIL — DSR = 0.144 (need >0.95).** Best per-trade Sharpe 0.12 is **below** E[max Sharpe | null over 916 trials] = 0.21. Corroborated by an independent **random-entry best-of-N null** (asymmetry-preserving): null best averages +0.247R vs observed +0.148R, **P(null ≥ obs) = 1.00.** The "edge" is within (below) selection noise — confirmed by two independent nulls.
- Passed-but-conditional: plateau 6/6 dome; H1/H2 both +0.13/+0.16; entry-timing permutation p=0.027; anti-control −0.16. **All conditional on the selection that DSR rejects** — textbook "plateau ≠ validity."

## Durable findings (→ ledger)

1. **USDCAD 15m mean-reverts / breakouts fade** (fresh 2026-H1 corroboration of VR<1; reproduces ledger #2). Up-spikes fade hard, down-moves flat — directional asymmetry.
2. **The raw reversion edge is sub-cost** (mean +0.07R gross → +0.01R @0.8p → −0.05R @1.6p; 0.9% clear hurdle) — corroborates the closed `raw-inverse` null, not new evidence to reopen it.
3. **Trend-pullback edge is a selection artifact** (DSR 0.14). Parameter-robustness + stationarity tests pass conditionally but fail multiplicity — worked example of selection-tests-outrank-parameter-tests.
4. The binding constraint throughout is the **cost law**; the price-action mechanism space (breakout falsified, reversion closed+sub-cost, pullback selection-artifact) is **exhausted for 15m on this window.**

## Caveats / what would change the verdict

Single 5.4-month regime, zero true OOS — every NULL is "failed to reject, bounded by power." The one legitimate continuation is a **multi-year, multi-regime USDCAD panel** (esp. a CAD-strength regime to test the up-fade asymmetry out-of-sample). Higher-TF re-test of pullback is **not** motivated — the 15m edge is selection noise, not a real-but-sub-cost edge to rescue.

## Artifacts (this directory)

`characterize.py` · `usdcad_harness.py` (+`test_sim.py` 14/14) · `run_grid.py` · `robustness.py` · `compare_fill.py` · `run_pullback.py` · `deflation.py` · `dsr.py` · `best_of_n.py` · `grid_results.csv` · `pullback_results.csv`. Pre-regs in `docs/briefs/pre-registration/PREREG-USDCAD-{BREAKOUT,PULLBACK}-2026-06-14.md`.

**Forbidden-move audit:** no §3 grid / §5 metric / §6 gate was moved after data arrived (one cost-default bug in the robustness *wrapper* was caught and fixed; the unit-tested core simulator and the frozen grid were unaffected). Answer to the pre-reg audit hook: **no criterion moved.**
