# Pine Baseline CSV Format — ECR Ingest Pipeline v0.1

**Status:** SPEC (stub) — awaiting Pine-side implementation
**Consumer:** `live_journal/ingest/pine_loader.py::load_pine_csv` (currently raises `NotImplementedError`)
**Output:** `Counterfactual` rows (see `live_journal/counterfactuals/schema.py`)
**Parent brief:** ECR Ingest Pipeline v0.1 §2 (out of scope), §3 architecture, §9.4 deterministic UUIDs
**Memory canon:** `docs/spec/` (singular) per the 2026-05-10 path convention.

---

## §1 — Purpose

A Pine baseline CSV is the output of replaying a single locked Pine strategy
over its historical bar feed and recording, for every signal that fired (per
the Pine entry logic), what the realized P&L would have been under the
counterfactual assumptions in §3 below.

The ECR pipeline joins these rows to `SignalEvent` records on `event_id` and
computes `leakage_$ = counterfactual_pnl_usd - realized_pnl_account_ccy`.

One CSV per `(strategy, methodology_version, pine_hash)` triple. Multiple
methodology versions may coexist; the ingest picks one at query time per the
`Counterfactual.methodology_version` field.

---

## §2 — Required columns

Type column is the Python type the parser produces. CSV strings are coerced
per standard `csv` + `datetime.fromisoformat` rules.

| # | Column | Type | Required | Maps to `Counterfactual` field | Notes |
|---|---|---|---|---|---|
| 1 | `event_id` | str (UUID) | ✓ | `event_id` | Must match the `SignalEvent.event_id` produced by `ingest.enum_maps.event_id_for(notion_signal_id)`. Brief §9.4 — deterministic UUID5 under `NAMESPACE_UUID`. |
| 2 | `notion_signal_id` | int | ✓ | (derive) | The Notion auto-increment integer. Use to compute `event_id` via `event_id_for(notion_signal_id)` and assert it matches column 1. |
| 3 | `strategy` | str | ✓ | (derive `source_pine_path`) | One of the Pydantic Strategy enum values: `guardian_v5_5`, `striker_dj30_v4_5`, `aegis_v4_3`, `nas100_v1_0`. |
| 4 | `instrument` | str | ✓ | (cross-check) | XAUUSD/DJ30/USDJPY/NAS100. Must agree with `STRATEGY_INSTRUMENT_MAP[strategy]`. |
| 5 | `direction` | str | ✓ | (cross-check) | LONG or SHORT (uppercase, matches Pydantic Direction enum). |
| 6 | `anticipated_ts` | datetime ISO | ✓ | (cross-check) | UTC. Should match `SignalEvent.signal.anticipated_ts` for the joined row. |
| 7 | `entry_ts` | datetime ISO | ✓ | (informational) | When Pine actually entered (may differ from `anticipated_ts` if the entry is a delayed condition). |
| 8 | `entry_price` | float | ✓ | (used for pnl reconstruction) | The fill price Pine assumes (perfect_fill=True). |
| 9 | `planned_sl` | float | ✓ | (informational) | |
| 10 | `planned_tp` | float | ✓ | (informational) | |
| 11 | `planned_size_R` | float | ✓ | (informational) | Decimal units, NOT percent. Brief §9.7. |
| 12 | `exit_ts` | datetime ISO | ✓ | `exit_ts` | UTC. |
| 13 | `exit_price` | float | ✓ | `exit_price` | |
| 14 | `exit_reason` | str | ✓ | `exit_reason` | One of: `tp_hit`, `sl_hit`, `be_hit`, `trail_hit`, `max_hold_hit`, `session_end_hit`, `manual_close`, `pyramid_reversal`. NOT `still_open` — counterfactuals are over closed trades only (schema validator rejects `still_open`). |
| 15 | `pnl_usd` | float | ✓ | `pnl_usd` | Signed; positive = profit. In account ccy (USD for FXIFY). |
| 16 | `pnl_R` | float | ✓ | `pnl_R` | Signed. R = risk amount at `equity_basis` (see §3). |
| 17 | `mfe_R` | float | ✓ (>=0) | `mfe_R` | Max favorable excursion in R, non-negative. |
| 18 | `mae_R` | float | ✓ (<=0) | `mae_R` | Max adverse excursion in R, non-positive. |
| 19 | `bars_in_trade` | int | ✓ (>=0) | `bars_in_trade` | 15m bars between entry_ts and exit_ts inclusive. |
| 20 | `notes` | str | ✗ | `notes` | Optional free text per row. |

`source_pine_hash`, `source_pine_path`, `methodology_version`, `computed_ts`,
`computed_by`, and `assumptions` are NOT per-row — they're passed as CLI
arguments to `ingest counterfactuals` and stamped onto every emitted
`Counterfactual` from that run.

---

## §3 — Assumptions (CLI-level, not per-row)

`CounterfactualAssumptions` block (from `live_journal/counterfactuals/schema.py`):

| Field | Default for v0.1 | Notes |
|---|---|---|
| `perfect_fill` | `True` | Pine baseline assumes you got the planned entry price exactly. |
| `zero_commission` | `True` | No commission/swap modeling. |
| `equity_basis` | `"at_fire"` | R is computed against equity at fire time. |
| `pyramid_handling` | `"full_resolution"` for DJ30/NAS, `"n/a"` for Guardian/Aegis | Pyramid pyramids fully resolve into a single composite trade for Striker DJ30 and NAS100. |
| `slippage_model` | `"none"` | No slippage applied. |
| `slippage_fixed_pips` | `None` | Required iff `slippage_model="fixed_pips"`. |

CLI invocation will look like:

```bash
python -m ingest.ingest counterfactuals \
    --month 2026-04 \
    --pine-hash $(git -C pine rev-parse --short HEAD) \
    --methodology-version v0.1 \
    --equity-basis at_fire \
    --slippage-model none
```

---

## §4 — Example CSV (Guardian, May 2026)

```csv
event_id,notion_signal_id,strategy,instrument,direction,anticipated_ts,entry_ts,entry_price,planned_sl,planned_tp,planned_size_R,exit_ts,exit_price,exit_reason,pnl_usd,pnl_R,mfe_R,mae_R,bars_in_trade,notes
22222222-2222-4222-8222-222222222222,87,guardian_v5_5,XAUUSD,LONG,2026-05-07T13:15:00Z,2026-05-07T13:18:00Z,2415.50,2410.30,2435.50,0.0034,2026-05-07T21:30:00Z,2435.50,tp_hit,1480.00,1.96,2.05,-0.45,82,Anticipation-only skip; full Pine-projected outcome
```

(Row deliberately matches the existing `counterfactuals_fixture.jsonl` row 2
for cross-checking — running `ingest counterfactuals` against this CSV should
produce an identical `Counterfactual` to the fixture row, modulo
`counterfactual_id` which is generated per-row.)

---

## §5 — Validation rules

`pine_loader.load_pine_csv` MUST:

1. Cross-check `event_id == event_id_for(notion_signal_id)`. Mismatch =
   sidecar row (do not emit Counterfactual).
2. Cross-check `instrument == STRATEGY_INSTRUMENT_MAP[strategy]`. Mismatch =
   sidecar.
3. Reject `exit_reason="still_open"` at row level (schema validator does this
   too, but failing early gives a clearer message).
4. Reject `mfe_R < 0` or `mae_R > 0` per the schema validators.
5. Stamp `computed_ts = now()`, `computed_by = "compute_ecr.py@v0.1"`,
   `source_pine_hash` and `source_pine_path` from CLI args.
6. Generate `counterfactual_id = uuid4()` per row.

All other validation comes from Pydantic's `Counterfactual.model_validate()`
which runs at construction time.

---

## §6 — Producing the CSV (Pine-side workflow, sketched)

This is the work that needs to happen on the Pine side to produce the CSV
this spec consumes. NOT in scope for the ECR ingest pipeline v0.1; sketched
here so the cross-team handoff is clear.

For each locked strategy (Guardian v5.5, Striker DJ30 v4.5, Aegis v4.3,
Striker NAS100 v1.0):

1. Run the Pine indicator (NOT the strategy script) on the bar feed for the
   window of interest. The indicator should output every entry signal and
   the bar-bar trajectory.
2. For each signal, simulate the trade per §3 assumptions and emit one CSV
   row per the §2 column spec.
3. Save as `live_journal/data/counterfactuals/pine_{strategy}_{YYYY-MM}.csv`. Per-file
   `SHA256SUMS` per the existing manifest discipline (see `CLAUDE.md`
   "Vendor-data integrity gate").

`event_id` for each row is `event_id_for(notion_signal_id)`. Pine doesn't
know Notion signal IDs natively — the join must be done either by:
- A pre-computed lookup table (notion_signal_id ↔ anticipated_ts), OR
- Anticipated_ts-based matching (less reliable, requires de-duplication)

The lookup-table path is cleaner; the table can be exported once-per-month
from Notion via the same MCP/REST that the ingest uses.

---

## §7 — Open questions for spec ratification

1. **MFE/MAE units.** This spec uses R. Pine may produce price-based MFE/MAE
   more naturally. Convert at CSV-write time or accept either with an R-flag
   column?
2. **Multi-pyramid handling.** For DJ30/NAS pyramids, do we emit ONE
   composite row per pyramid-sequence or one per pyramid level? §3 says
   "full_resolution" = composite; that's load-bearing for ECR but loses
   per-level detail.
3. **Cancelled-by-collision signals.** Pre-Trade Log has `Collision Tier 3`
   skip rows. Are those COUNTERFACTUAL rows (would-have-fired) or are they
   filtered out before reaching this CSV?
4. **OANDA vs Pepperstone feed.** `CLAUDE.md` says Pepperstone is canonical
   for MC; OANDA is pattern-spotting only. Pine baseline should use
   Pepperstone bars. Need an explicit pin in `source_pine_path` or in
   methodology_version notes.

These are NOT blockers for spec ratification — they're items to settle
before the first `ingest counterfactuals` run in Phase 1.

---

## §8 — Pointer back to ingest

Once this spec is ratified and a CSV in this shape exists for any month:

```bash
python -m ingest.ingest counterfactuals --month YYYY-MM \
    --pine-hash $(git -C pine rev-parse --short HEAD)
```

would replace the current `NotImplementedError` in
`live_journal/ingest/pine_loader.py::load_pine_csv` with the spec-conformant parser.

**End of spec stub.**
