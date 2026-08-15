# Strategy Reference — mechanics, not baselines

Strategy parameters live in Pine Script (gitignored); this file is reference only, Pine files
are source of truth. **PF/WR/Net/DD baseline figures and locked entry/exit parameters are NOT
restated here** — redacted 2026-08-14 from the public tree, same pass that redacted
`core/strategies/_archive/*/LOCK.md` and `trade-csv-reconcile/references/baselines.md`
(see `docs/adr/2026-08-14-repo-public-visibility-transition.md`). See the private operational
archive for the canonical per-strategy numbers.

## Guardian Gold v5.5 🔒 LOCKED (2026-04-23)

Pure trend-rider (no BE, no trail). DXTrade contractValue: **100**. Pine v6 —
`margin_long/short = 0`.

## Striker DJ30 v4.5 🔒 LOCKED (2026-05-05; allocation-refresh-2 2026-05-23: risk 0.75%→0.70%, pyramid 500%→750%)

Heavy pyramid architecture. **Day soft-stop: −1.15% live (TV override of Pine default
−2.00%)** — halts new Striker entries when realized day P&L hits threshold. **CRITICAL
safety rule.**

**Cross-feed $ deltas are contract-spec, not signal drift.** OANDA US30.pro is $5/pt (E-mini
DJIA futures) vs Pepperstone US30 CFD $1/pt — Pine `calcSize` doesn't account for per-point
value, so dollar figures differ ~5× on the same trade selection even though signal counts
match. Don't diagnose a dollar mismatch across feeds as a signal bug.

**Primary bust risk: solo gap-fill on non-pyramid breakouts** (1–7 bar holds, 15min close
2.5–6× past intended stop). Pyramid-reversal is a secondary tail. The day-stop catches
cascade.

DXTrade contractValue: **10** (CRITICAL — default of 1 is 10× wrong). Pine v6 —
`margin_long/short = 0`.

## Aegis-Reversion USDJPY v4.3 🔒 LOCKED (2026-04-22)

**EOM Filter (v4.3 defining feature):** month-end JPY flow impulse (Japanese exporter
repatriation, WMR fix-window positioning, fund rebalancing, options expiry) overrides the
typical lower-BB reversion character — the exact calendar window is a locked parameter, see
the private archive.

**Identical trade count across feeds (Pepperstone vs OANDA) confirms USDJPY is
broker-uniform** — only spread/slippage differs between feeds, not signal generation.

Long-only (short side eliminated in v3 → v4 rebuild — no edge). **BE logic IS the edge.
Do not remove.**

**Regime risk:** USDJPY range-regime sensitive; 2022 was a materially weaker year than
2023–2025. **Passive diagnostic:** rolling 40-trade PF — track in weekly review only. NOT a
halt trigger. If it degrades meaningfully, apply The Algorithm consciously, do not
reflexively halt.

**Binary-event pause rule applies** (see SKILL.md "Portfolio Configuration → Aegis pause
rule"). Aegis's live instrument is venue-dependent — see SKILL.md's note on the non-canonical
CME 6J prototype for futures venues.

DXTrade contractValue: **default (1)** — USDJPY direct match. Pine v6 —
`margin_long/short = 0`.

## Striker NAS100 v1 🔒 LOCKED (2026-05-05; allocation-refresh-2 2026-05-23: risk 0.45%→0.37%, pyramid 1000% unchanged)

**Long-only breakout + pyramid** (SHORT mirror falsified 2026-05-05 — direction-asymmetric by
structure — do NOT re-test without new mechanism evidence). The pyramid pathway IS the
strategy — base-only performance is materially weaker than the full pyramided book
(load-bearing). Do not overlay base-entry filters.

**Day soft-stop: −1.50%** (native Pine default — NOT a TV override, unlike DJ30's −1.15%) —
halts new NAS100 entries when realized day P&L hits threshold.

**Cross-feed validated 2026-05-24** (OANDA reached 4-strategy parity) — dollar-Net delta vs
Pepperstone is contract-spec, not signal drift.

DXTrade contractValue: **10** (CONFIRMED 2026-05-05 — same critical 10× scaling as DJ30;
default of 1 is 10× wrong). Pine v6 — `margin_long/short = 0`.
