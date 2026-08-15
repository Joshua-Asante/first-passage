# ORB-ZB-1 Phase-0 RESULTS — native ZB, frozen NAS100-ORB-30 construct

**Verdict: CLOSED — FALSIFIED at Phase-0 (P0.1 cost-law KILL on every window; the ORB breakout has NEGATIVE gross edge on ZB).**

**Scoping brief:** [`docs/briefs/rnd-pipeline/ORB-ZB-1-risk-off-decorrelated-breakout-scoping.md`](lab/archive/../../docs/briefs/rnd-pipeline/ORB-ZB-1-risk-off-decorrelated-breakout-scoping.md)
**Run:** 2026-07-20 · `run_phase0.py` (K=0 δ-extraction, not a registered search) · operator GO recorded (§8).
**Engine:** `orb_universe_2026-06-22/orb_lib.py` `orb_backtest` / `placebo_within_day` **verbatim** (calibration-pinned by `orb_lib_test.py`); only the loader (databento ZB.v.0 1m → 15m ET) and the ZB `Instrument` economics are new.
**Data:** native `ZB.v.0` continuous 1m (Databento GLBX.MDP3, pull `$0.00`, `ohlcv-1m_continuous_d2f56c0dc86e92c5.dbn`, 2,237,060 rows), resampled 15m ET. 169,703 session bars, 2,241 days, span 2019-05-05 → 2026-07-14. Median close **131.06** (valid 30Y-bond price ⇒ correct decode). 3 degraded-quality days (2020-02-27/28, 2020-06-30) — observation-only.

---

## P0.1 — cost-law reachability (Req 5): KILL on every window

ZB economics: point $1,000; tick 1/32 pt = $31.25; RT headline `0.06372 pt` = 2 × ($0.61 Bulenox + 1-tick $31.25 slip); RT 0-slip lower bound `0.00122 pt` (commission only).

| Window | n | median OR range | mean **gross** edge_R (t) | headline ratio | 0-slip ratio | net meanR (t) / PF |
|---|---|---|---|---|---|---|
| FULL 2019-05→present | 1,853 | 0.3125 pt (10 ticks) | **−0.0480** (−1.61) | −0.20× | −10.66× | −0.2830 (−9.42) / 0.593 |
| 2021+ | 1,426 | 0.3125 pt | −0.0293 (−0.87) | −0.12× | −6.49× | −0.2654 (−7.80) / 0.610 |
| 2019 | 170 | 0.2812 pt | −0.0686 (−0.68) | −0.27× | −14.12× | −0.3225 / 0.555 |
| 2020 | 257 | 0.3125 pt | −0.1379 (−1.69) | −0.64× | −33.26× | −0.3545 / 0.531 |

**The gross edge is negative in every window.** This is a *stronger* failure than D5/H-OD-1 (which had real positive edges killed by cost): ORB-ZB has no edge to cost-kill — the opening-range breakout **loses gross** on ZB. No cost level rescues it (the 0-slip lower bound is still −10.66× because the numerator is negative). The cost geometry is also independently hostile (median OR range 10 ticks; RT headline ~2 ticks ⇒ cost_R 0.235 R, 4× hurdle 0.94 R — a break-even breakout would need +0.94 R gross), but that is moot given the negative sign.

## Structural placebo (within-day OR window, 2021+) — confirms no opening-range momentum

`obs meanR −0.2654 · placebo p = 0.0010 · placebo_mean −0.5451 · p95 −0.4975 · parity_ok True`

The opening range **is** structurally "special" (p=0.001) — but in the wrong direction: the real 09:30 OR breakout (−0.265) is merely **less loss-making** than breakouts on arbitrary intraday windows (−0.545). Breakouts lose everywhere on ZB; the opening range is the least-catastrophic place to lose. **ZB fades its opening range — it does not continue it.** This is the opposite of MNQ (N1/ORB-MNQ: gross +0.082 R, both sides positive).

## P0.3 — tail-timing (informational; moot under the P0.1 kill)

Per-year net meanR: 2019 −0.32 · 2020 −0.35 · 2021 −0.26 · 2022 −0.23 · 2023 −0.05 · 2024 −0.35 · 2025 −0.37 · 2026 −0.39. Every year negative; no decorrelation value to assess.

## P0.2 — decorrelation pre-flight (informational; moot)

ORB R std 1.293 ⇒ at 0.37%/$100K, ZB-ORB daily-$std **$478** ⇒ **ρ = 1.75** (≥1.0 presumptive-reject); ρ=1.0 weight = 0.211%. As predicted, ρ at a fixed weight is ~instrument-invariant (R is OR-normalized) — a **weight lever, not the ZB-vs-MNQ discriminator**. The binding Stage-8 statistic `n_eff_risk_delta` was never reached (needs the aligned MYM/MNQ leg series; data-gated — the same Stage-8 owe ORB-MNQ-1 carries).

---

## The load-bearing finding (mechanism, not just cost)

**Opening-range momentum is an equity-index property; it does not transfer to Treasuries — ZB shows opening-range *mean-reversion* at the 09:30 anchor.** The Baltussen-class intraday-momentum / dealer-hedging mechanism is equity-index-cohort-specific (flagged as the Req-1 grounding caveat in the seed manifest); the ZB δ-extraction confirms the mechanism is absent — indeed sign-reversed — on the 30Y bond.

This **tightens the vise** the whole graveyard describes: the one cost-viable mechanism class (large-δ index intraday breakout) is mechanistically *tied to the equity-index book* — the same thing the locked/c1 book already harvests. Cost-survival and decorrelation are in tension not just empirically (Q-COMPOSE-1) but mechanistically: the mechanism that beats cost is the mechanism the book already owns.

## Honest scope / what this does NOT foreclose

- **Construct-specific.** The pre-committed anchor is **09:30 ET** (US equity cash open — the faithful ORB-MNQ transplant), *not* the bond-native **08:30 ET** data window. An 08:30-anchored construct is a **different mechanism requiring its own fresh pre-reg** (brief §5 forbids sweeping the anchor here), NOT a Phase-0 rescue — and it inherits a **low prior** (ZB's intraday character is mean-reverting; the negative sign is unlikely to be purely an anchor artifact given breakouts lose on *every* within-day window, placebo above).
- **Mechanism-class-specific.** This falsifies *breakout/continuation* on ZB, not every ZB mechanism. A ZB **mean-reversion/fade** construct is the sign-consistent direction — but note the nearest dead class (rates-intraday-MR on MICRO10Y/2YY, `rejected_candidates.md`) and the cost geometry (10-tick OR vs 2-tick RT) both weigh against a fade clearing cost either. Not pursued; a fade is a distinct mechanism with its own intake.

## Disposition

- **CLOSED — FALSIFIED** (P0.1 KILL every window; negative gross edge). K = 0 consumed; ZB family bank stays **0**. Databento spend **$0.00**.
- Append to [`docs/rejected_candidates.md`](lab/archive/../../docs/rejected_candidates.md) — `orb-breakout on ZB`, class edge-failure (negative gross edge) + venue/cost-geometry (secondary). Re-proposal bar: a genuinely different ZB mechanism (e.g. a fade) with its own cohort-δ + cost clearance, NOT an anchor/param re-tune of this breakout.
- No `core/` / allocation / `dd_protection` / `ACTIVE_FIRM` / Pine touch. Lock HELD.

## Reproduce

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=lab .venv-research/Scripts/python.exe lab/archive/orb_zb_recon_2026-07/run_phase0.py
```
