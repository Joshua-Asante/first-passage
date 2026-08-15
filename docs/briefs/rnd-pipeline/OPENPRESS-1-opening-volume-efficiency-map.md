# OPENPRESS-1 — opening volume × directional-efficiency mechanism map

**Status:** `CLOSED — FALSIFIED 2026-07-21` ([closure](../closures/OPENPRESS-1-closure-falsified.md))
**Authored:** 2026-07-22
**Authors:** Joshua + Cursor
**Loop:** Inquire-phase K=0 diagnostic
**Pre-registration:** [`OPENPRESS-1-verdict-preregistration.md`](../pre-registration/OPENPRESS-1-verdict-preregistration.md)

## §0 — Rule 0 reads

- [`core/bar_export_loader.py`](../../../core/bar_export_loader.py) @ `d11abdb`: BAR EXPORT provides exact M15 OHLCV bar-open UTC timestamps and v0.2 session/instrument metadata; it does not provide quotes or order flow.
- [`core/data/bar_data/SHA256SUMS`](../../../core/data/bar_data/SHA256SUMS): MNQ hash `ddb14f…e1f7e3ac`; MYM hash `298ab8…f9059c`. Both CSV bytes are absent in this cloud checkout.
- [`lab/archive/xindex_rv_recon_2026-07/run_probe.py`](../../../lab/archive/xindex_rv_recon_2026-07/run_probe.py) @ `82e338e`: prior 14-session shifted-median relative-volume definition; no-lookahead implementation reused.
- [`lab/archive/xindex_rv_recon_2026-07/RESULTS.md`](../../../lab/archive/xindex_rv_recon_2026-07/RESULTS.md): relative-volume ranking alone failed because higher volume predicted larger movement but not better ORB edge. This diagnostic asks a different mechanism question: whether volume becomes informative only after conditioning on directional efficiency.
- [`docs/rejected_candidates.md`](../../rejected_candidates.md) @ `910dbe3`: new index-OHLCV work must use a mechanism outside the exhausted price/instrument/hold-time lever set or a different modality. Volume-conditioned absorption versus information is the declared mechanism; no threshold/window sweep is allowed.

## §1 — Context and Pre-Q gate

BAR EXPORT cannot identify true order flow, but it can measure the price response to observed volume. The hypothesis is that high opening volume is continuation-bearing when the opening range is directionally efficient and reversal-bearing when similar activity is absorbed into a low-efficiency range.

Pre-Q gate:

- **D:** Delete thresholds, quartile selection, individual weekdays, alternate opening windows, and entry/exit rules. They turn a mechanism diagnostic into a search.
- **S:** One continuous pressure-alignment score per session and one signed post-opening response.
- **A:** Hash-pinned inputs, deterministic era split, JSON output, and a reproducible Markdown gate return.

## §2 — Frozen measurements

For each instrument and RTH date:

1. Opening window = 09:30 and 09:45 ET M15 bars.
2. `RV = opening_volume / trailing_14_session_median(opening_volume).shift(1)`.
3. `efficiency = abs(close_10:00 - open_09:30) / (OR_high - OR_low)`.
4. `pressure_alignment = max(log(RV), 0) × (2×efficiency - 1)`.
5. `response = sign(close_10:00 - open_09:30) × log(close_16:00 / close_10:00) × 10,000`.

Positive score means above-normal volume plus one-sided price discovery; negative score means above-normal volume absorbed into a low-efficiency range. Positive response means continuation in the opening direction.

Regression: `response ~ intercept + pressure_alignment`, Newey-West/HAC standard error with five lags. Run separately on MNQ and MYM; development ends 2023-12-31 and 2024+ is untouched holdout.

## §3 — Question

**Q-OPENPRESS-1:** Does opening volume become directionally informative when measured jointly with price efficiency, with the same mechanism surviving independently on MNQ and MYM?

## §4 — Falsifiable hypothesis

**H-OPENPRESS-1:** If both instruments have positive development slopes with HAC t≥2, positive holdout slopes, positive pooled slopes with HAC t≥2, and the predicted P90→P10 response spread clears 4× Tradeify round-trip cost, then the mechanism is RESOLVED and may generate one separately pre-registered candidate. If neither instrument passes, it is FALSIFIED. If exactly one passes, it is AMBIGUOUS and no instrument may be selected post hoc.

## §5 — Forbidden moves

- No threshold grid, buckets, or “best” high-volume cut.
- No alternate opening or exit windows.
- No interpreting BAR EXPORT volume as signed order flow.
- No choosing MNQ after seeing MYM fail, or vice versa.
- No strategy/Pine/rail construction from this diagnostic.
- No Databento substitution: feed-specific BAR EXPORT hashes are part of the question.
- No nearest-file or stale-export substitution when either hash is missing.

## §6 — Gate criteria

Per instrument, PASS requires:

- development N≥800 and holdout N≥500;
- development slope >0 and HAC t≥2;
- holdout slope >0;
- pooled slope >0 and HAC t≥2;
- predicted score P90→P10 spread ≥4× Tradeify RT cost.

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | MNQ and MYM both PASS | Author one fresh candidate Pre-Q; no automatic strategy |
| `FALSIFIED` | Neither passes | Close the mechanism; no threshold rescue |
| `AMBIGUOUS` | Exactly one passes | No post-hoc instrument selection; require independent mechanism evidence |
| `NEEDS_CONTEXT` | Either hash-pinned CSV is absent or mismatched | Supply exact vendor bytes; do not substitute feeds |

## §7 — Execution

The harness and pre-registration are frozen before reading outcome data. Execution command:

```bash
PYTHONPATH=lab .venv-research/bin/python \
  lab/archive/opening_pressure_map_2026-07/run_diagnostic.py \
  --mnq core/data/bar_data/MNQ_M15.csv \
  --mym core/data/bar_data/MYM_M15.csv
```

Current cloud state: both vendor CSVs are absent; manifests prove the expected files and hashes. The run therefore returns `NEEDS_CONTEXT` until the exact bytes are supplied.

## §8 — Operator GO

```
GO: 2026-07-22 / Joshua ("let's run that recommended first test")
Authorizes: K=0 hash-pinned BAR EXPORT diagnostic and closure.
Does not authorize: threshold search, K spend, strategy code, Pine, rail, sizing,
                    allocation, lifecycle, or live trading.
```

## §10 — Audit hooks

```bash
sha256sum core/data/bar_data/{MNQ,MYM}_M15.csv
PYTHONPATH=lab .venv-research/bin/python -m pytest -q \
  lab/archive/opening_pressure_map_2026-07/test_run_diagnostic.py
python3 scripts/check_brief.py \
  docs/briefs/rnd-pipeline/OPENPRESS-1-opening-volume-efficiency-map.md \
  --type inquire
```

## Verification

```bash
git log --format='%h %ci %s' -- \
  docs/briefs/pre-registration/OPENPRESS-1-verdict-preregistration.md \
  lab/archive/opening_pressure_map_2026-07/run_diagnostic.py \
  lab/archive/opening_pressure_map_2026-07/RESULTS.md
```
