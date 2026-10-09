# Striker NAS100 — Changelog

Long breakout strategy on NAS100 (NASDAQ 100) 15min. Pine Script v6. Architecture-family sibling of Striker DJ30 v4.5 — shares entry filters, exit logic, and adaptive trail, but instrument-tuned (0.37% risk per 2026-05-23 allocation-refresh-2, 1000% pyramid, a narrower day-of-week set).

**Source of truth:** `striker_nas100_v1.pine` holds the authoritative parameter values. This CHANGELOG records decisions, rationale, and known concerns. If the two ever disagree, the Pine file wins — fix the CHANGELOG.

**Public summary (2026-10-09).** Parameter values and backtest figures were removed from this public copy; the original text is preserved in the private archive (`first-passage-archive`, branch `archive/preserve-exposure-2026-10-09`). Portfolio MC anchors are owned by [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md); risk%, pyramid and `contractValue` are owned by [`core/strategies/CATALOG.md`](../../CATALOG.md) §Locked parameter record.

Versioning begins at v1.0 (released 2026-05-04, locked 2026-05-05). Pre-release lineage (v0.1 dev / B_15 label / v4.5-test branch) is archived under `archive/strategies/striker/striker_nas100_v1_research.pine` and Notion.

---

## [Unreleased]

_Queued changes. Move to a dated entry on commit._

_(none)_

---

## 2026-05-08 — Folder split + 4-strategy MC re-anchor (C2)

- **Strategy file moved `strategies/striker/` → `strategies/nas/`.** No parameter change. Codifies the architecture-family-but-instrument-tuned distinction from DJ30 (separate risk %, separate DOW set, separate pyramid size). DJ30 family stays in `strategies/striker/`. Cross-references in `REPO_MAP.md`, `archive/docs/briefs/striker_nas100_q_nas_1_results.md`, and `archive/docs/briefs/striker_nas100_q_nas_3_mc_addition.md` repaired in the same commit.
- **OANDA NAS100 panel landed.** An OANDA NAS100 TV export was added as a secondary feed (Pepperstone remains canonical), and `data/bar_data/NAS100USD.csv` was fetched from OANDA M15 over the same window as the other three instruments. `scripts/fetch_oanda_bars.py` now includes NAS100USD permanently.
- **dd_protection C2 relock (cross-ref).** Same-day relock from C0 (1.0%/0.40×) → C2 (1.5%/0.40×) re-anchored the 4-strategy Pepperstone MC. NAS100 had the **lowest bust attribution** of the four strategies, consistent with the diversification thesis at lock. See `docs/adr/2026-05-08-dd-trigger-c2-relock.md`, [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md) and `strategies/striker/striker_CHANGELOG.md` for the full ADR + DJ30 anchor record.

---

## [v1.0] — 2026-05-04 RELEASED · 2026-05-05 🔒 LOCKED

**Status:** Locked, integrated into FXIFY operational tooling 2026-05-07 after DXTrade `contractValue=10` broker-verified. Risk **0.40%** (FXIFY-deployable). Released 2026-05-04 after Phase 4C + Phase 6 closure and FINAL_LOCK verification; v1 is the first production version (predecessor v0.1 dev / B_15 archived).

### Parameters
| Field | Value |
|---|---|
| Instrument | NAS100 (NASDAQ 100) |
| Timeframe | 15min |
| Direction | Long breakout |
| Risk per trade | 0.40% (rolling-equity; compounds) |
| Pyramid size | 1000% (vs DJ30 v4.5 350%) |
| Limits | daily DD cap, internal total-DD kill set inside the firm's limit, max trades per day, day soft-stop |
| Entry | breakout with ATR-expansion and bar-body filters |
| Exits | ATR stop and take-profit, breakeven with pad, adaptive trail, max hold |
| Pyramid | adds after a profit threshold and minimum bars in the trade |
| Session / days | a US-session window on a narrow weekday set (narrower than DJ30 v4.5) |
| **DXTrade `contractValue`** | **10** (default of 1 understates risk — same gotcha as DJ30) |

### Design intent
**Pyramid is the load-bearing edge.** Base entry is a qualifier; the pyramid add (after the trade has moved in profit for a minimum number of bars) is where the structural edge lives. Q-NAS-1 (2026-05-05) confirms the pattern at the trade-log level:
- Base-only cohort on non-pyramid days: loss-making by design.
- Pyramid contribution to total profit: the large majority in every year (2022–2026).
- Pyramid-conditional cohort: high win rate and profit factor.

The 1000% pyramid size on NAS100 (vs 350% on DJ30) is intentional: NAS100's trend-continuation autocorrelation is high enough that a validated continuation deserves heavy leverage. Smaller base risk (0.40% vs DJ30's 1.00%) balances the pyramid amplification — effective peak-stack risk is similar on both instruments via inverse-scaled levers.

**Implication:** do not overlay base-entry filters intended to "improve" base PF. The base is supposed to be near-breakeven; the pyramid is the strategy. (See `project_pyramid_is_strategy_for_nas100.md` memory.)

### Backtest (Pepperstone NAS100 15m, 2022-01-01 → 2026-04-20, 4y4m)
Profitable in every year, with drawdown inside the FXIFY static limit and the strategy still profitable with 2024 excluded.

The internal total-DD cap sat ahead of FXIFY's 5% static rule, leaving a buffer at the lock backtest.

### Portfolio MC anchors

**2026-05-08 (C2 relock, current canonical):**
4-strategy Pepperstone (G 0.34% / DJ30 v4.5 1.00% / A 1.50% / NAS v1 0.40%, dd_protection C2 1.5%/0.40×). **NAS100 had the lowest bust attribution of the four**, consistent with the diversification thesis at addition. An OANDA pattern-spotting run (3-strategy still v4.4) was also recorded. Reproducible under `python portfolio_mc.py --panel pepperstone`. Figures: [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md).

**2026-05-05 (C0 baseline at addition, historical):**
Same 4-strategy stack at C0 (1.0%/0.40×). Bust attribution order: DJ30, Guardian, Aegis, NAS100. See `archive/docs/briefs/striker_nas100_q_nas_3_mc_addition.md` for the addition decision audit.

### Known concerns
- **Pyramid-load fragility (live).** Pyramid-conditional cohort carries the strategy. A regime where continuation autocorrelation breaks (or where the continuation filter stops firing) collapses edge to the loss-making base-only cohort. Forward live-PnL tripwire applies; if pyramid contribution drops sustainably below a pre-set share, escalate.
- **Narrow day-of-week footprint.** Narrow by design (validated empirically) but reduces the panel's regime coverage at the trade level vs broader-DOW strategies.
- **Moderate panel size.** 4-year backtest sample is moderate; permutation/bootstrap CI is wide on tails. Q-NAS-1 confirmatory tests (2026-05-05) clear the design-intent claim, but tail estimates remain MC-bounded.

### Cross-reference
- `archive/docs/briefs/striker_nas100_q_nas_1_results.md` — Q-NAS-1 pyramid-dependence confirmatory tests (2026-05-05)
- `archive/docs/briefs/striker_nas100_q_nas_3_mc_addition.md` — joint v4.5 + NAS100 add MC results (2026-05-05)
- `archive/docs/striker_nas100/q_nas_2_capture_plan.md` — Q-NAS-2 capture plan (closed/archived 2026-05-08)
- `archive/strategies/striker/striker_nas100_v1_research.pine` — post-lock research file (archived 2026-05-07)
- `archive/analysis/striker_nas100/q_nas_1_pyramid_hypothesis.py` — Q-NAS-1 source (archived 2026-05-08)
- `strategies/striker/striker_CHANGELOG.md` v4.5 entry — sibling DJ30 lock and joint MC anchor

### FXIFY operational integration (2026-05-07)
NAS100 v1 added to `firm_rules.py` / `dd_protection.py` / `accounts.py` / `cli.py lots` after DXTrade `contractValue=10` broker-verified. `portfolio_mc.py` already covered NAS100 from the 2026-05-05 lock anchor. See `CLAUDE.md` Strategy Reference table for the operational scope.

---

## Change convention

Each entry: version, date, lock status, parameters (full snapshot or delta), rationale, backtest metrics if re-run, cross-reference to Notion decision page.

Tag in git on lock: `git tag striker-nas-vX.Y && git push --tags`.
