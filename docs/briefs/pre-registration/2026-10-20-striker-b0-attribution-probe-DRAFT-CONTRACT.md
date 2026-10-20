# Striker MYM p250 base-only (B0): attribution probe — draft-contract stub

**Status:** `DRAFT CONTRACT — probe only`. Not frozen; no candidate status; no Explore.
**Authority:** Joshua, 2026-10-20: "Approve option (b) with a 12-month forward window" (relayed by the coordinator) and "yes, (b) with 12 months" (direct, in the probe session).
**Must run locally:** the probe reads a gitignored vendor export.

This stub exists to satisfy [evaluation order](../../adr/2026-08-30-evaluation-order.md) step 2 and the
[candidate contract](../../adr/2026-08-30-candidate-contract.md) probe rule: reserve Confirm by an
append-only commitment before any pre-freeze probe reads data.

## Confirm reservation (append-only)

- **Instrument:** MYM (CBOT Micro E-mini Dow), continuous `MYM1!`, 15m.
- **Window:** forward only — every MYM session opening after this commit's timestamp, for 12 months (through 2027-10-20). No session in the window has been read by this probe or by any record it relies on.
- **Rule:** no B0 or Striker p250 read of any bar inside the window before a founding freeze names it as Confirm.

## Probe envelope

| Field | Value |
|---|---|
| Spend | $0 (no data purchase, no export request, no simulation) |
| K | 0 for this probe. Any later B0 test is a separate trial on the pyramid axis, whose prior lineage (500% → 750% → 250%) is unreconciled and disclosed, never reset. |
| Input | Existing Phase-1 export `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-09-03_9d7ea.csv`, sha256 `5a5006588fa5c87628df7b1c15c8af8d8ae2250be0abb0371ea4d93665ef998e`, 2022-09-01..2026-09-02, already fully exposed (Phase 1, T00 lineage K=12). Outside the window above. |
| Statistics (exact) | Per episode (base trade plus any add): base-lot and add-lot net P&L, commission, and embedded slippage (1 tick/side on market and stop fills, limits unslipped); add-lot P&L in R of the base's initial risk; worst stacked-stop episode loss in R; add-lot depth break-even (extra ticks/side on add fills at which total add net reaches 0); count and dates of halt-divergent sessions (day soft-stop or DD-Limit state could differ without the add) and whether each DD-Limit exit fell on an add episode. |
| Not computed | No ΔSharpe, bust, or pass inference; no re-cut, partition or parameter variation. |
| Cost basis | The export's captured basis ($0.91/side, 1 tick/side) — a labelled scenario, not an established venue cost. |

## Close

If no campaign freezes, this probe closes on the mechanism record as stand-alone spend ($0, K=0).
