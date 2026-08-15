# Pre-Registration — 5m Granularity Prototypes (2026-06-25)

Frozen before any 5m export is observed. No metric, basis, or read-direction
below may change after the first 5m CSV is loaded.

## Strategies
guardian (XAUUSD), striker (US30/DJ30), striker_nas100 (NAS100), aegis (USDJPY).

## Comparison basis
- Dollar metrics on **static-$200K**: `static_pnl = Net P&L % / 100 × 200_000`.
  Rationale: TV CSVs compound; static-$200K is the FXIFY convention and removes
  the compounding artifact. PF/WR are count-based.
- **Matched window**: the 15m baseline is clipped to `[min(exit_ts), max(exit_ts)]`
  of the 5m export before any metric is computed. The achieved window and trade
  counts are reported in RESULTS.md.
- **Trade count = exit-row count** (every closed leg, incl. pyramid adds), applied
  identically to 15m and 5m so it is internally consistent.

## Per-strategy metrics (15m baseline vs 5m proto, matched window)
PF, Win-rate, Net (static-$), MaxDD (static-$, peak-to-trough on cumulative),
Recovery Factor (Net/MaxDD), trade count, implied 1R (via core implied_1r).

## Read-direction (declared now)
For each strategy, classify the 5m result as:
- **HELPS**: RF improves AND/OR MaxDD falls, with PF not materially worse.
- **HURTS**: PF or RF degrades, OR MaxDD rises.
- **NEUTRAL**: differences within MC/sampling noise (esp. on short windows).
"Material" = beyond a ±1 MC-bootstrap-style band noted at report time.

## Portfolio re-MC (descriptive only — NOT a lock gate)
Feed the four 5m streams through the core MC kernel at locked
ALLOCATIONS + DD_TRIGGER 0.015 / DD_SCALE 0.40. Report pass / bust / p99-DD
vs the locked anchor **99.83% / 0.17% / 4.37%**. If the matched window is shorter
than the canonical 4yr floor, the re-MC uses a window-relaxed loader and the
shortened window is disclosed — never silently passed.

## Guardrail
Exploratory. No 5m variant here can justify a lock; promotion requires the full
strategy-validation gauntlet. Locked strategies/constants are untouched.

## Caveat params (TF-sensitive, kept unchanged as first cut)
DJ30/NAS `minBodyRatio` (per-bar candle geometry) — disclosed, not scaled.
