# Aegis-Reversion — Changelog

Mean-reversion strategy on USDJPY 15min. Pine Script v6.

**Source of truth:** `aegis_usdjpy_v4.3.pine` holds the authoritative parameter values. This CHANGELOG records decisions, rationale, and portfolio role. If the two ever disagree, the Pine file wins — fix the CHANGELOG.

**Public summary (2026-10-09).** Parameter values and backtest figures were removed from this public copy; the original text is preserved in the private archive (`first-passage-archive`, branch `archive/preserve-exposure-2026-10-09`). Portfolio MC anchors are owned by [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md); risk% is owned by `core/historical_challenge.py`.

Versioning begins at v4.1 (2026-04-17). Prior development (v4 → v4.1, which raised net P&L and shifted the drawdown shape) is archived in Notion.

---

## [Unreleased]

_Queued changes. Move to a dated entry on commit._

_(none)_

---

## 2026-05-05 — Open queue closeout

- **BOJ April 28, 2026 meeting watch — closed.** Monitoring window from the prior Unreleased entry elapsed 2026-04-28 → 2026-05-05 with no parameter change required and no dated regime-shift entry written. No behavioral note merits backfill at this point; closing the watch.

---

## [v4.3] — 2026-04-22 (candidate) / 2026-04-23 🔒 LOCKED

**Status:** LOCKED 2026-04-23 (commit `e40802d`, jointly with Guardian v5.5 and Striker v4.4 — DJ30 later migrated v4.4 → v4.5 on 2026-05-05; Aegis v4.3 unchanged through both events). Active on FXIFY $200K challenge. Risk 1.50%. Supersedes v4.2.

### Delta from v4.2
Single change: **block the last days of every calendar month** (month-end block). All other parameters are preserved unchanged from v4.2.

### Mechanism
Month-end JPY flow impulse (Japanese exporter repatriation, WMR fix-window positioning, fund rebalancing, options expiry adjustments) overrides mean-reversion at month end. A loss-character diagnostic comparing month-end losses with the rest of the month found far more full-stop losses, larger and faster losses, and less favorable excursion before the loss at month end — the signature of a directional impulse overwhelming mean-reversion.

### OOS validation
The filter improved both net and profit factor on the 2022–2024 train split and on the 2025–2026 test split, so it transfers across the regime change (key evidence against curve-fit).

### Full-panel impact (Pepperstone 52mo)
Removing the month-end trades improved net, profit factor, win rate, maximum drawdown and return over maximum drawdown together while lowering the trade count — the signature of removing genuine negative-expectancy trades, not curve-fit noise.

### Rejected during same INQHIORI loop (do not revisit without new mechanism evidence)
- **Post-holiday Wed 10:15 filter** — failed OOS (the train-split effect reversed in test).
- **FOMC-day filter** — different mechanism (chop/BE-shaves, not impulse); near-flat aggregate.
- **BOJ-day filter** — no session overlap in 4yr panel (BOJ announces before the session opens).
- **Wed 10:15 blanket block** — redundant after EOM; residual is noise on top of EOM/FOMC correlation.

### Post-v4.3 portfolio Monte Carlo (completed 2026-04-23)
The previously-queued post-v4.3 portfolio MC re-run executed at the joint 2026-04-23 lock and the same-day Guardian risk re-lock (0.30% → 0.34%). Aegis's share of bust probability fell sharply from the 2026-04-17 MC to roughly the original expectation at the post-relock canonical config (G 0.34% / S 1.00% / A 1.50%). See `docs/adr/2026-04-23-guardian-risk-relock-0.34.md` and [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md) for the locked MC anchors.

### Cross-reference
- 2026-04-22 INQHIORI loop (candidate)
- 2026-04-23 Pepperstone directional MC re-lock vs 2026-04-20 Alchemy baseline — commit `e40802d`
- 2026-04-23 post-Guardian-risk-relock canonical MC — commit `84d3cb1`
- 2026-04-24 Mon-H10 2024 Inversion INVESTIGATE: H-A confirmed (tail-noise, not a structural issue)
- **2026-05-05** — portfolio re-anchored to 4-strategy lock (G 0.34% / DJ30 v4.5 1.00% / **A 1.50%** / NAS v1 0.40%). Aegis allocation unchanged; Aegis bust attribution fell slightly. See `strategies/striker/striker_CHANGELOG.md` v4.5 entry and `archive/docs/briefs/striker_nas100_q_nas_3_mc_addition.md`.

---

## [v4.1] — 2026-04-17 🔒 LOCKED (superseded by v4.3 on 2026-04-23)

**Status:** Historical. Active on FXIFY $200K challenge from 2026-04-17 to 2026-04-23. Risk 1.50%. Initial tracked version.

### Parameters
Authoritative parameter values (as of the v4.1 lock) lived in the then-current `strategies/aegis/aegis_usdjpy_v4.1.pine` (removed when v4.3 superseded it; .txt → .pine extension convention adopted 2026-04-28). Public fields:

| Field | Value |
|---|---|
| Instrument | USDJPY |
| Timeframe | 15min |
| Direction | Mean-reversion (both sides) |
| Risk per trade | 1.50% |

### Allocation rationale
1.50% risk chosen on per-strategy recovery factor optimization. The final portfolio Monte Carlo (2026-04-17) attributed the largest share of bust probability to Aegis. Decision stands:

1. Aegis had the highest μ/σ in the portfolio
2. Recovery-factor optimization prefers higher allocation to highest-Sharpe strategy
3. Bust attribution at correct sizing is an artifact of having a strongest edge, not a miscalibration

### MC context (final, 2026-04-17)
Run at G 0.30% / S 1.00% / A 1.50% with single-tier DD protection; Aegis was the largest bust contributor, then Striker, then Guardian. Anchors: [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md).

### Strategy role in portfolio
Yen safe-haven bid capture and BOJ/Fed divergence expression. Structurally countercyclical to Guardian and Striker:
- Iran-Israel conflict regime (Feb 28, 2026 onset, Hormuz closure Mar 2): Aegis fired consecutive winners while Guardian drew down through its worst-ever losing streak
- Debate-to-election 2024 window: Aegis/Guardian positive while Striker had its worst window
- No day across the 4yr backtest on which all three strategies lost

### Regime sensitivities
- Benefits from: violent round-trip regimes, yen safe-haven flows, BOJ/Fed rate divergence
- Threatened by: sustained USDJPY trend regime, BOJ policy shock
- BOJ April 28, 2026 meeting flagged as binary vol event

---

## Change convention

Each entry: version, date, lock status, parameters (full snapshot or delta), rationale, backtest metrics if re-run, cross-reference to Notion decision page.

Tag in git on lock: `git tag aegis-vX.Y && git push --tags`.
