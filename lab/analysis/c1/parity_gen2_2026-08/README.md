# Gen-2 parity gate (SPEC S3 / Q-FILLTAX-1 V2)

**Status:** `CODE_LANDED` scaffold 2026-08-07 — **Gate RESOLVED still needs first
family TV anchor (operator).** No parity numbers fabricated; unit tests use
synthetic series only.
**Spend:** $0 · K=0 · nothing armed.

Python engine research authority is **per strategy family**: one manual TV
anchor run that clears the frozen bands in [`PREREG.md`](PREREG.md) grants the
engine authority inside that family's envelope. Fail keeps the family native-only.

## How to run

From repo root (bands load from `PREREG.md` constants mirrored in `parity_gate.py`):

```bash
# Synthetic unit tests (no vendor CSV)
python -m pytest lab/analysis/c1/parity_gen2_2026-08/test_parity_gate.py -q

# Family anchor (operator supplies both CSVs; same-feed CME TV exports)
python lab/analysis/c1/parity_gen2_2026-08/parity_gate.py \
  --engine path/to/engine_trades.csv \
  --tv-anchor path/to/tv_anchor_trades.csv
```

CSV columns (minimal): `pnl` (required). Optional: `trade_id`, `entry_time`.
Exit `0` = `ADMIT`, `1` = `FAIL`. JSON summary prints to stdout.

## Gen-1 retired

The Gen-1 `lab/validation` harness is **retired** (ADR
`docs/adr/2026-07-11-gen1-pipeline-retirement.md`). Do not resurrect it.
Bands here are **refrozen** (`FROZEN-PRE-RUN` in [`PREREG.md`](PREREG.md)), not
inherited. Methodology shape:
[`docs/methodology/prefilter_rank_correlation_gate.md`](../../../docs/methodology/prefilter_rank_correlation_gate.md).

## Same-feed rule

Both series must come from the **same CME futures TV export feed**
(`core/data/tv_exports/cme/`). Mixing Pepperstone/CFD-era panels, offline
fill-ports, or cross-feed splices voids the run. One manual TV anchor per
family is the sole grant of engine research authority (S3 Step 3).

## Deployment-truth path (read-only; do not arm)

Deployment truth is **not** the backtester. When M1 is `RESOLVED` and a separate
per-session operator GO arms the rail, micro-size eval fills are the ground truth:

```
micro-size eval fills
  → ops/c1_rail/c1_rail_telemetry.py   (structured events + evidence)
  → S4 ledger                          (SPEC S4 sensor layer)
  → ops/c1_rail/c1_rail_slippage.py    (read-only join / cohort analysis)
```

This scaffold **does not** arm the rail, set `dry_run=false`, POST orders, or
run Stage-1/Stage-2 live capture. `c1_rail_slippage.py` remains read-only
(RUNBOOK §B7 Stage 2b). Fill capture waits on M1 `RESOLVED` + per-session GO
(Addendum 2026-07-31b).

## Related

- Brief: [`docs/briefs/Q-FILLTAX-1-fill-realism-and-parity-scoping.md`](../../../docs/briefs/Q-FILLTAX-1-fill-realism-and-parity-scoping.md)
- Spec: [`docs/spec/2026-08-07-loop-s3-arbiter-two-tier-spec.md`](../../../docs/spec/2026-08-07-loop-s3-arbiter-two-tier-spec.md)
- Phase-0 note: [`RESULTS.md`](RESULTS.md)
