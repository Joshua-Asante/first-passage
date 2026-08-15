# RUNSPEC — Q-TXG-1 cell `striker_nas100 × MYM` (operator native-TV export)

**Date authored:** 2026-08-12 · **Owner:** Joshua (TV run) → later Block-4 scoring (gated)
**Parent PREREG:** [`docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md`](lab/archive/../../../../docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md) (`FROZEN`)
**Election:** #1 · [`ELECTION.md`](lab/archive/../ELECTION.md)
**Type:** operator export contract only. **No scoring, N-SURV, manifest open, or PnL/return reads in Blocks 2–3.**
**TV login automation:** **PROHIBITED** ([S2](lab/archive/../../../../docs/adr/2026-08-07-loop-s2-signal-host-fork.md)).

---

## Configuration (defaults only — no chart overrides)

| Item | Value |
|---|---|
| Script | `striker_nas100_v1_mym_qtxg1_prototype.pine` |
| SHA256 | `19264da29a3d9a30200600689e1950931f1abfb648e9071a232ee83fdec2756c` |
| Pin | [`PORT_MANIFEST.sha256`](lab/archive/../../../../core/strategies/PORT_MANIFEST.sha256) · card [`striker_nas100_v1_mym_qtxg1_CARD.md`](lab/archive/../../../../core/strategies/nas/striker_nas100_v1_mym_qtxg1_CARD.md) |
| Symbol / TF | CBOT **`MYM1!`** · **15m** · back-adjusted ("Adjust for contract changes" **ON**) |
| Mode | TradingView **Deep Backtesting** |
| Start | script default `2022-01-01` (do not advance the start to manufacture N) |
| Inputs | **all defaults** — session/DOW filters **ON**; EOD Force-Flat **ON**; accountSize 100000; microCap 80; risk 0.37%; day soft-stop −1.5% |
| Commission / slip | already in script (`$0.91` / side, slippage 1) — do not double-count in TV properties |

---

## Operator landing path

1. Paste / load the pinned Pine on a clean `MYM1!` 15m chart.
2. Run Deep Backtesting at defaults above.
3. Export **List of Trades** CSV → `Downloads/`.
4. Copy into this cell folder as:
   `lab/archive/transfer_expression_grid_2026-08/cells/striker_nas100_mym/inputs/<export_filename>.csv`
5. Record SHA256 of the landed bytes in `inputs/SHA256SUMS` (create on land).
6. **STOP.** Do not open the CSV for Net / PF / expectancy / DD in this block.

---

## Frozen `port_must_beat` (compile — not a scoring action)

Verbatim from GRID_RESULTS / cell PREREG §2.2 — for Block-4 use only:

- cost_tax_r **0.06** · env1 **OPEN** · lifecycle **1.0** · nsurv_ceiling_pct **3.0**
- qty_at_locked_risk **9** · required_net_r **0.06** · risk_pct **0.0037** · stop_ticks **80**

---

## Hard stop

Blocks 2–3 end when this RUNSPEC is committed and the port is hash-pinned.
**Block 4** (not this file) owns `register_search open`, panel metrics, and N-SURV.
Offline fills are **not** a verdict (design §7).
