# Q-TNEC-CON-2 — cheap falsifier + admission log (parent-side, pre G0 score)

**Date:** 2026-08-09  
**Cell:** 2 narrow bars (≤1.0× med20 range) → close-break → with-break MNQ session-flat @ G=10  
**K_intrinsic:** 1 · **Cost:** $0.00 (MNQSEL-2 parquet reuse)

## Panels

| Symbol | Path | Notes |
|---|---|---|
| `MNQ.v.0` | `../mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet` | same panel as MNQSEL-2 / CON-1 |

No new Databento pull.

## Arithmetic bars (G=10, RT=1.41)

| Bar | Value |
|---|---|
| EM1 pred move (0.40R) | **5.41 pt** |
| N-EDGE pred move | **1.41 pt** |
| EM1 WR (±G binary) | **0.7705** |
| N-EDGE WR (±G binary) | **0.5705** |

## Parent panel falsifier (Family B)

See [`../cheap_falsifiers_2026-08/_cheap_falsifier_compression_break_2026-08-09_LOG.md`](../cheap_falsifiers_2026-08/_cheap_falsifier_compression_break_2026-08-09_LOG.md).

| Arm | n | mean R | session-block 95% CI |
|---|---:|---:|---|
| long | 5,187 | −0.053 | [−0.148, +0.044] |
| short | 4,992 | −0.078 | [−0.189, +0.039] |

**Verdict:** `CHEAP_FALSIFIER_OK` (CI straddles 0 both arms — generous kill did not fire).

## Prior Family A (no Q-ID)

[`../cheap_falsifiers_2026-08/_cheap_falsifier_displacement_fade_2026-08-09_LOG.md`](../cheap_falsifiers_2026-08/_cheap_falsifier_displacement_fade_2026-08-09_LOG.md) — `FALSIFIED` both arms CI &lt; 0.

## S6 admission

[`ADMISSION.md`](ADMISSION.md) — **ADMIT** at `catalogue_k=1`.

## Explore

**Blocked** until `EXPLORE_GO.md` + `--explore-go`. CONFIRM unread.
