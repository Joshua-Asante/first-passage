# `core/data/external/` — exogenous / reference panels

External (non-broker-feed) reference panels used by `lab/` research. The CSV
**bytes are gitignored** (vendor / third-party TOS: personal export OK,
redistribution not); only `SHA256SUMS` is tracked. Regen / integrity gate is the
standard vendor-data flow — see CLAUDE.md **Vendor-data integrity gate**
(`python scripts/check_data_manifests.py --regenerate --dry-run` → `--regenerate`,
commit the `SHA256SUMS` delta in the same commit). `check_data_manifests.py` only
hashes `*.csv` here, so this README does not affect the gate.

## Panel disposition (annotated 2026-07-02, R7c of the 2026-07-01 programme audit)

All five panels were filed for the **regime-signal / co-drawdown-orthogonality
battery** (`lab/analysis/regime_signal_research_2026-06-25/`), which **closed NULL
(power-limited)** — no free exogenous signal in the tested family discriminates the
book's H1 co-drawdown episodes beyond vol+calendar at N≈33. See
[`CLOSURE.md`](../../../lab/analysis/regime_signal_research_2026-06-25/CLOSURE.md).
The closure's only remaining theoretical levers are **PAID exogenous data**
(options-flow / dealer-gamma) or **more accrued co-drawdown episodes over time** —
both deferred, not excluded.

| File | Provenance | Role | Disposition |
|---|---|---|---|
| `COR3M_M15_cboe.csv` | commit `9c75d86` | CBOE 3M implied-correlation, 15m (starts 2021-05, misses 2020) | **RETAINED** — orphan add (R7c) |
| `DSPX_M15_cboe.csv` | commit `9c75d86` | CBOE dispersion index, 15m (starts 2023-09, H2-only) | **RETAINED** — orphan add (R7c) |
| `S5FI_D1_index.csv` | commit `403576d` | S&P 500 % > 50-DMA breadth, daily, full 2020→ history | **RETAINED** — orphan add (R7c) |
| `COR3M_D1_cboe.csv` | commit `4f467a5` (pre-reg v3.1 FREEZE) | CBOE 3M implied-correlation daily (CBOE CDN 2006→, full H1) | RETAINED — frozen battery-run evidentiary input |
| `SECTOR_SPDR_D1_yahoo.csv` | commit `4f467a5` (pre-reg v3.1 FREEZE) | Sector-SPDR ETF closes (Yahoo); source for realized RCORR/RDISP | RETAINED — frozen battery-run evidentiary input |

**R7c decision — annotate-retain (not remove).** The three orphan adds
(`COR3M_M15`, `DSPX_M15`, `S5FI_D1`) are **retained for a future exogenous
regime-signal probe** — specifically a *paid*-exogenous or *more-accrued-episodes*
re-open per the CLOSURE's stated levers. Retention is near-zero cost (hashes only,
bytes gitignored) and these panels may seed that probe without a re-download.
Removing would be a vendor-data-manifest operation with no space/cleanliness
benefit here.

The last two rows (`COR3M_D1`, `SECTOR_SPDR`) are **not** orphans — they were the
data pinned by the pre-registration FREEZE (`4f467a5`) as the battery's actual
evidentiary inputs, and are retained as that frozen record.

No locked config, allocation, `dd_protection`, MC anchor, or Pine touched by this
annotation.
