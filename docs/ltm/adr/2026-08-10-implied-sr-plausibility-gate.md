<!-- relocated from docs/adr/; relative links rewritten 2026-08-13 -->

# ADR 2026-08-10 — `implied_annualized_sr` promoted from report-only to a gate; fade design-region closes on its own arithmetic

**Status:** `Superseded`
**Decision date:** 2026-08-10
**Authors:** Joshua (ruling) + Claude Code (Fable 5, evidence trace)
**Supersedes:** none
**Superseded-by:** `2026-08-13-implied-sr-report-only-fade-reopen.md`
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [frozen rulings + Finding 2026-07-31b](../../notes/2026-07-31-fade-stage1-frozen-rulings.md) (owed disposition, now discharged as its Ruling 5) · [MCL INTAKE-DRY + killing-constants sensitivity](../../../ops/instruments/MCL.md) (the ablation evidence) · [ceremony tiering](../../adr/2026-08-08-adr-ceremony-tiering.md) (light record — doctrine limb only; $0 · K=0 · no live-risk, locked, or non-regenerable surface)

## Decision

1. **Gate, not diagnostic:** any **assumed-edge feasible-region screen** (fade-class design law or successor) must carry `implied_annualized_sr = per_trade_sharpe(p, rr) × √(n·252)` as a **freeze-time admission limb**: a cell whose implied annualized Sharpe exceeds the estate plausibility ceiling is inadmissible. Ceiling = the documented `SHARPE_CEILING` **1.83** (Aegis, CFD-era cohort — generous); the futures-native best **≈0.89** is mandatory disclosure beside any pass, and electing it as the binding ceiling is a separate, stricter ruling not taken here.
2. **Consequence, effective now:** the Tradeify-native fade program's admitted region (4× · `CONFIG-B-MCL` · rr∈{0.66, 1.0}) **empties at every `p`** — measured floor 2.98 as-ruled, **2.11 = 1.15× ceiling with every elective limb ablated**, zero cells under either ceiling. **The fade design-region is CLOSED on its own arithmetic** at $0 / K=0. Frozen Rulings 1–4 stand as history; no lab body is edited (reader-intercept convention).
3. **Scope boundary (what makes this safe):** the gate binds **assumed-edge design regions only**. Measured-edge candidates (Route B campaigns, TNEC intake, CON-2) are governed by DSR-at-K on their actual Sharpe and are untouched.

**Check:** on any new feasible-region freeze — the region artifact must print the limb and the ceiling cohort disclosure; a region published without it fires this ADR.
