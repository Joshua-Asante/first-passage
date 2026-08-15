# Phase-0 verdict pre-registration — MYM-3FPS-1

**Status:** `FROZEN — operator GO 2026-07-21`
**Freeze scope:** Native-MYM third-Friday settlement-reversal K=0 extraction.
**Scoping:** [`MYM-3FPS-1-third-friday-settlement-reversal-scoping.md`](../rnd-pipeline/MYM-3FPS-1-third-friday-settlement-reversal-scoping.md)
**Result:** `FALSIFIED` without gate amendment; [`RESULTS.md`](../../../lab/archive/mym_3fps_recon_2026-07/RESULTS.md).

## §0 — Verified inputs

- `docs/rejected_candidates.md` @ `910dbe3`: exact construct absent.
- `docs/methodology/strategy_harvest.md` @ `268851b`: Requirements 1–5 and K=0 delta-extraction precedent bind.
- `ops/prop_envelope_default.md` @ `7af4224`: intraday-flat deployment requirement.
- `core/firm_rules.py` @ `a53ee99`: Tradeify $0.91/side primary; MFFU $0.95/side sensitivity.
- Baltussen, Terstegge, and Whelan, *The Derivative Payoff Bias*: target prior approximately +12 bp DJIA overnight and comparable open-to-noon reversal; target sigma unavailable.

## §1 — Frozen construct

| Field | Frozen value |
|---|---|
| Instrument | `MYM.v.0`, native micro continuous series |
| Panel | 2019-05-06 inclusive → 2026-07-21 exclusive (pre-pull metadata-range correction from July 22; event set unchanged) |
| Events | Every calendar third Friday; no quarterly or other subtype selection |
| Mechanism anchor | Thursday 15:59 ET bar close → Friday 09:30 ET bar open |
| Trade | Short Friday 09:30 ET bar open → cover Friday 12:00 ET bar open |
| Missing checkpoints | Drop event; never nearest-bar substitute |
| K | 0 for Phase 0; no discovery manifest |
| Cost model | MYM $0.50/point; one tick slippage/side; Tradeify $0.91/side primary; MFFU $0.95/side sensitivity |
| Outputs | Event CSV, JSON metrics, Markdown RESULTS |

## §2 — Frozen gates

Let `N` be events with all three exact checkpoints and `f = 1.96/sqrt(N)`.

| Gate | PASS condition |
|---|---|
| P0.0 coverage | `N / calendar_events ≥ 0.90` |
| P0.1 mechanism faithfulness | Overnight-spike mean `> 0` and `delta/sigma ≥ f` |
| P0.2 tradable reversal | Open-to-noon short mean `> 0` and `delta/sigma ≥ f` |
| P0.3 cost law | Open-to-noon short mean bp `≥ 4 × Tradeify round-trip bp` |

The power calculation is the harvest intake’s frozen `power = Φ(sqrt(N) × |delta/sigma| − 1.96)` rule; `delta/sigma ≥ f` is exactly the `power ≥ 0.50` boundary. Because the source predicts a sign, the gate additionally requires positive signed means and ratios.

## §3 — Verdict

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | P0.0–P0.3 all PASS | Stop; author a fresh K=1 confirmation pre-registration and obtain a fresh operator GO |
| `FALSIFIED` | P0.0 PASS and any of P0.1–P0.3 FAIL | Close construct; append rejection with measured numbers; K bank unchanged |
| `AMBIGUOUS` | P0.0 FAIL | Diagnose data coverage only; no return verdict and no in-place gate edit |

## §4 — Forbidden interpretations

- MFFU PASS cannot rescue a Tradeify failure.
- A wrong-sign but statistically large move fails.
- A quarterly-only, MNQ, different-clock, overnight, or pooled variant is a new hypothesis.
- Phase-0 RESOLVED is not lifecycle admission or deployment authorization.

## §5 — Freeze-before-result audit

This file and `lab/archive/mym_3fps_recon_2026-07/run_phase0.py` must be committed before the data pull is consumed by the runner. `RESULTS.md` must land in a later commit.

```bash
git log --format='%h %ci %s' -- \
  docs/briefs/pre-registration/MYM-3FPS-1-verdict-preregistration.md \
  lab/archive/mym_3fps_recon_2026-07/run_phase0.py \
  lab/archive/mym_3fps_recon_2026-07/RESULTS.md
```
