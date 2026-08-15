# Execution History — FXIFY manual-execution era (RETIRED 2026-06-30)

**HISTORICAL.** This file describes the FXIFY CFD manual-execution operating mode that ran 2026-04 through 2026-06-30, retired per `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` (operator executive decision after a 2-day discretionary-tilt episode lost −$4,188.85 at 100%-off-spec against flat systems). Joshua is not currently executing any live trades manually. Preserved because the underlying structure is reusable if/when a manual-execution challenge goes live again — do not treat anything below as current operational state; check CLAUDE.md's "Live-execution posture" section for what's actually active today.

## Manual execution delivery (as it worked, 2026-04 to 2026-06-30)

**Platform:** TradingView alerts → Phone/Smartwatch → Manual execution on DXTrade.

`dd_protection.py`'s sizing was computed via a morning CLI tool, run before the trading session, because DXTrade has no API — there was no way to compute or apply the day's DD-scaling programmatically against a live DXTrade account. An automated execution rail (e.g. TradersPost against a futures broker) would need its own design for where this computation happens; it should not be assumed to still be a CLI-tool-based morning ritual.

## Emergency Protocols (assumed active manual trading)

Portfolio-level DD scaling was automated via `dd_protection.py` (single-tier C2, DD 1.5% peak / 0.40× scaling, relocked 2026-05-08). These rules covered residual operational cases only:

- **3+ consecutive losses on one strategy** → Normal variance. Do NOT adjust parameters.
- **Platform issues / alert failure** → Close all positions manually. No blind entries.
- **Emotional compromise** → Close the laptop. Opportunities reset tomorrow.
- **Market holidays** → Verify before every Friday/Monday. Do NOT force alternate-day trades to compensate for a missed session.

Threshold-based halts (daily-loss-percent, total-DD-percent, VIX gates) were NOT used — they'd duplicate `dd_protection.py` semantics inconsistently and create decision conflict under stress. `dd_protection.py` remains the single source of sizing response to drawdown, whichever execution rail is eventually active.
