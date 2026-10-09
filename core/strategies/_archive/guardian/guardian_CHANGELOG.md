# Guardian Gold — Changelog

Long-only XAUUSD 15min trend strategy. Pine Script v6.

**Source of truth:** `guardian_gold_v5.5.pine` holds the authoritative parameter values. This CHANGELOG records decisions, rationale, and active overlays. If the two ever disagree, the Pine file wins — fix the CHANGELOG.

**Public summary (2026-10-09).** Parameter values and backtest figures were removed from this public copy; the original text is preserved in the private archive (`first-passage-archive`, branch `archive/preserve-exposure-2026-10-09`). Portfolio MC anchors are owned by [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md); risk% is owned by `core/historical_challenge.py`.

Versioning begins at v5.1 (2026-04-17). Prior development history (v3.7 → v3.8 → v3.9 → v4 → v5.1) is archived in Notion under the FXIFY Command Center.

---

## [Unreleased]

_Queued changes. Move to a dated entry on commit._

_(none)_

---

## 2026-05-05 — Open queue closeout

- **v5.4 Pepperstone re-MC for feed-vs-filter isolation — closed without execution.** Question was framed against the 3-strategy MC anchor and aimed at isolating Pepperstone feed-level drag from v5.5's added filters. Under the 2026-05-05 4-strategy lock (see `strategies/striker/striker_CHANGELOG.md` v4.5 entry) the v5.4-vs-v5.5 isolation no longer informs any pending decision. Re-open only if a future v5.5-attributed regression in live PnL surfaces.

---

## [v5.5 + risk 0.34%] — 2026-04-23 🔒 LOCKED

**Status:** Active on FXIFY $200K challenge. Cold-start risk **0.34%** (re-locked from 0.30% same day on expanded 52-month Pepperstone panel). Supersedes v5.4.

### Delta from v5.4
- Added several hour-of-day entry blocks and a same-day latch: when a blocked hour would have produced a valid trend-recovery signal, all later entries that day are blocked.
- One legacy hour block from v5.4 retained (small, positive cohort; kept locked on, with a test input exposed for an isolated unblock experiment).
- Grace mechanic shortened and tightened relative to v5.1.

### Risk re-lock 0.30% → 0.34% (same-day)
Pepperstone-sourced CSVs (2022→2026) expanded the MC panel from ~14 months to 52 months of regime coverage, revealing headroom under the 1% bust target and 5% static DD cap. The post-relock portfolio MC (G 0.34% / S 1.00% / A 1.50%) cleared both gates. Iran-Israel / Hormuz conflict overlay deactivated same day — revert triggers met. See `docs/adr/2026-04-23-guardian-risk-relock-0.34.md`, [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md) and `docs/overlays/guardian_conflict_risk.md` (historical record).

### Lock MC anchors (2026-04-23, pre-risk-relock)
- Alchemy reference (2026-04-20, Striker v4.4 + Aegis v4.2 era).
- Pepperstone directional: failed the bust gate raw, then passed after correcting Aegis 1R for an n=1 full-stop thin-cohort artifact (median fallback inflated the Aegis scale). Pass-rate gap vs Alchemy attributed to feed-level drag + v5.5 added filters. Locked under brief-authorized directional read, not anchor-grade MC. Re-MC with v5.4 Pepperstone pending.

### Cross-reference
- 2026-04-23 joint version lock (commit `e40802d`, Guardian v5.5 / Striker v4.4 / Aegis v4.3)
- 2026-04-23 Guardian risk re-lock (commit `84d3cb1`)
- `docs/adr/2026-04-23-guardian-risk-relock-0.34.md`
- **2026-05-05** — portfolio re-anchored to 4-strategy lock (**G 0.34%** / DJ30 v4.5 1.00% / A 1.50% / NAS v1 0.40%). Guardian risk unchanged; Guardian bust attribution fell. The Pepperstone Guardian export was re-fetched same day (`87e73 → 33781`) after a reconcile flagged phantom v5.5 signals — see `data/reconciles/2026-05-05_guardian_n_reconcile.md`. See also `strategies/striker/striker_CHANGELOG.md` v4.5 entry.

---

## [v5.4] — 2026-04-20 (interim, superseded by v5.5)

**Status:** Interim candidate; superseded within 3 days by v5.5. No risk/allocation change at v5.4.

### Notes
Pepperstone panel integration run (Alchemy → Pepperstone feed migration). Adjusted filter set produced the baseline 2026-04-20 Alchemy MC reference against which v5.5 was later anchored. Retained `data/tv_exports/pepperstone/guardian_v5.4.csv` as a re-MC input for feed-effect isolation (see v5.5 Unreleased queue).

---

## [v5.1] — 2026-04-17 🔒 LOCKED (superseded by v5.5 on 2026-04-23)

**Status:** Historical. Was active on FXIFY $200K challenge 2026-04-17 → 2026-04-23. Cold-start risk 0.30%. Initial tracked version.

### Parameters
| Field | Value |
|---|---|
| Instrument | XAUUSD |
| Timeframe | 15min |
| Direction | Long only |
| Entry | EMA trend filter |
| Exits | ATR stop, distant ATR take-profit, grace stop, max hold |
| Breakeven / trailing stop / MFE-BE | none |
| Session / days | A daytime session on selected weekdays, with hour blocks |
| Risk (cold-start) | 0.30% |

### Design intent
Pure trend-rider. No exit management beyond SL / TP / grace / maxHold. Captures full ATR-extension moves without BE or trail truncation.

### Backtest (4yr full period)
Strongly profitable over the full period, with the highest recovery factor in the portfolio at the time and no static drawdown.

### Funded-account risk ramp
Per-trade risk was planned to step up in stages as funded-account equity rose above the challenge balance.

### Active overlays
- **Conflict risk overlay (2026-04-16):** per-trade risk reduced pending Iran-Israel / Hormuz resolution. Revert triggers (BOTH, sustained 5 sessions): gold implied volatility back to normal AND Hormuz transit recovered to most of baseline. If signals don't fire in 8–12 weeks, extend — do not revert on calendar. See Notion: "Guardian conflict risk overlay — 2026-04-16".

### Known concerns
- Mar 2–30, 2026: worst losing streak on record, coincident with Iran conflict onset and Hormuz closure. Prompted the conflict risk overlay. Monitoring continues.

---

## Change convention

Each entry: version, date, lock status, parameters (full snapshot or delta), rationale, backtest metrics if re-run, cross-reference to Notion decision page.

Tag in git on lock: `git tag guardian-vX.Y && git push --tags`.
