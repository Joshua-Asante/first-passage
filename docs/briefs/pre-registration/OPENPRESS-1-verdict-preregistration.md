# OPENPRESS-1 verdict pre-registration

**Status:** `CLOSED — FALSIFIED 2026-07-21` ([closure](../closures/OPENPRESS-1-closure-falsified.md); [RESULTS](../../../lab/archive/opening_pressure_map_2026-07/RESULTS.md))
**Scope:** K=0 MNQ/MYM opening volume × efficiency diagnostic.
**Scoping:** [`OPENPRESS-1-opening-volume-efficiency-map.md`](../rnd-pipeline/OPENPRESS-1-opening-volume-efficiency-map.md)

## Frozen construct

| Item | Value |
|---|---|
| Inputs | `MNQ_M15.csv` SHA256 `ddb14f…e1f7e3ac`; `MYM_M15.csv` SHA256 `298ab8…f9059c` |
| Opening window | 09:30 and 09:45 ET bars |
| Exit observation | 15:45 ET bar close |
| RV | opening volume / shifted trailing-14-session median |
| Efficiency | absolute opening displacement / opening high-low range |
| Score | `max(log(RV),0) × (2×efficiency−1)` |
| Response | opening-direction-signed 10:00→16:00 log return, bp |
| Model | OLS slope with Newey-West/HAC SE, 5 lags |
| Development | through 2023-12-31 |
| Holdout | 2024 onward |
| K | 0; diagnostic only |

## Per-instrument PASS

All five must pass:

1. Development N≥800 and holdout N≥500.
2. Development slope >0 and HAC t≥2.
3. Holdout slope >0.
4. Pooled slope >0 and HAC t≥2.
5. `pooled_slope × (score_P90−score_P10) ≥ 4 × Tradeify RT cost`.

Cost model: instrument multiplier from CME/metadata; Tradeify $0.91/side plus one micro-index tick ($0.50) slippage per side.

## Overall verdict

| Verdict | Trigger |
|---|---|
| `RESOLVED` | Both MNQ and MYM PASS |
| `FALSIFIED` | Neither passes |
| `AMBIGUOUS` | Exactly one passes |
| `NEEDS_CONTEXT` | Either exact input is absent or hash-mismatched |

No threshold, time-window, instrument, or cost convention may be changed after results are visible. RESOLVED licenses a fresh candidate Pre-Q only.

## Freeze audit

The pre-registration and runner must precede `RESULTS.md` in git history.

```bash
git log --format='%h %ci %s' -- \
  docs/briefs/pre-registration/OPENPRESS-1-verdict-preregistration.md \
  lab/archive/opening_pressure_map_2026-07/run_diagnostic.py \
  lab/archive/opening_pressure_map_2026-07/RESULTS.md
```
