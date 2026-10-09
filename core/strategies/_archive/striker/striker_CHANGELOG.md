# Striker DJ30 — Changelog

Long breakout strategy on DJ30 (US30) 15min. Pine Script v6.

**Source of truth:** `striker_dj30_v4.5.pine` holds the authoritative parameter values. This CHANGELOG records decisions, rationale, and known concerns. If the two ever disagree, the Pine file wins — fix the CHANGELOG. Prior locked versions are in `archive/`.

**Public summary (2026-10-09).** Parameter values and backtest figures were removed from this public copy; the original text is preserved in the private archive (`first-passage-archive`, branch `archive/preserve-exposure-2026-10-09`). Portfolio MC anchors are owned by [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md); risk%, pyramid and `contractValue` are owned by [`core/strategies/CATALOG.md`](../../CATALOG.md) §Locked parameter record.

This file covers Striker DJ30 only. Striker NAS100 (architecture-family sibling — separate risk/DOW/pyramid tuning) was split out to `strategies/nas/striker_nas100_v1.pine` on 2026-05-08; see `strategies/nas/striker_nas100_CHANGELOG.md`.

Versioning begins at v4.3 (2026-04-17). Prior development history (v3.1 → v4.1 → v4.2 rejected → v4.3) is archived in Notion.

---

## [Unreleased]

_Queued changes. Move to a dated entry on commit._

- **v5 architectural rebuild** — priority #1 post-challenge pass. Hypothesis: strip BE/trail/T1 management following the Guardian v4 → v5.1 pattern, lift μ/σ toward the portfolio average. See Notion: "Striker v5 architectural rebuild — priority #1 post-challenge — 2026-04-17".

---

## 2026-05-08 — NAS100 split-out + dd_protection C2 relock (cross-ref)

- **`striker_nas100_v1.pine` moved `strategies/striker/` → `strategies/nas/`.** No DJ30 parameter change; DJ30 v4.5 stays in this folder. The split codifies the architecture-family-but-instrument-tuned distinction (NAS: 0.40% / 1000% pyramid / its own DOW set; DJ30: 1.00% / 350% pyramid / its own DOW set). Cross-references repaired in `REPO_MAP.md`, `archive/docs/briefs/striker_nas100_q_nas_1_results.md`, and `archive/docs/briefs/striker_nas100_q_nas_3_mc_addition.md`.
- **dd_protection C2 relock — 4-strategy MC re-anchored.** Same-day relock from C0 (1.0%/0.40×) → C2 (1.5%/0.40×) after `bust_attribution_flip` closed broker-feed-confirmed (Pepperstone+OANDA TV re-export) and Q-DDP-1's C2 sweep showed risk-controls-met + median-pass-time benefit. The new canonical 4-strategy Pepperstone MC cleared both lock criteria with margin and passed slightly faster than under C0. **DJ30 remained the largest bust contributor**, with its share up from C0 (consistent with C2's wider DD-trigger letting more DJ30-driven static DD episodes through to closure rather than truncating early). Q-DDP-1's regime-robustness gate failed for C2; the 2026-05-08 override accepts that risk on broker-feed + median-pass-time grounds. Forward C2→C0 revert trigger: rolling 6-month pass-rate <95% for two consecutive 6-month windows. See `docs/adr/2026-05-08-dd-trigger-c2-relock.md` (canonical ADR), [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md), `archive/docs/briefs/Q-DDP-1/recommendation.md` override note, and `archive/docs/briefs/bust_attribution_flip.md` closure.

---

## [v4.5] — 2026-05-05 🔒 LOCKED

**Status:** Active on FXIFY $200K challenge. Risk 1.00% (unchanged). Supersedes v4.4. v4.4 moved to `archive/`.

### Delta from v4.4
Multi-parameter tuning — five inputs adjusted: a stricter minimum-body filter (screens out more weak bars), a slightly tighter stop, a slightly wider take-profit, a tighter trail in the tight phase, and an earlier switch to the tight trail. The pyramid-size input range was widened; its default was unchanged.

Risk per trade, daily DD cap, max trades/day, lookback, ATR length, BE trigger, pyramid default size and trigger, maxHold, minBars all preserved from v4.4.

### Rationale
The migration thesis was that in a portfolio where the FXIFY DD cap is the binding constraint, giving up some net profit for about a point of max-DD compression is the right swap — that compression shows up directly in MC bust-rate. The 4-strategy re-MC bore that out (anchor figures superseded same-day after the Guardian 87e73 → 33781 phantom-signal correction — see `data/reconciles/2026-05-05_guardian_n_reconcile.md`).

### Portfolio MC anchors (2026-05-05)
- 4-strategy Pepperstone lock (G 0.34% / DJ30 v4.5 1.00% / A 1.50% / NAS v1 0.40%): both lock gates (bust < 1%, p99 DD < 5%) pass with comfortable margin. DJ30 remained the largest bust contributor, with its share down from the 3-strategy 04-26 anchor. Figures: [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md).

### Cross-reference
- `archive/docs/briefs/striker_nas100_q_nas_3_mc_addition.md` — joint v4.5 + NAS100 add MC results.
- `archive/striker_dj30_v4.4.pine` — preserved for reproducibility.

---

## [v4.4] — 2026-04-23 🔒 LOCKED (superseded by v4.5 on 2026-05-05; archived)

**Status:** Historical. Was active on FXIFY $200K challenge 2026-04-23 → 2026-05-05. Risk 1.00%. Pine file moved to `archive/striker_dj30_v4.4.pine`.

### Delta from v4.3
- **Stop loss tightened.** Sole parameter change; all other v4.3 parameters preserved.
- The `stopAtr` tooltip still shows the v4.3 value as a historical annotation.

### Rationale
Joint lock with Guardian v5.5 and Aegis v4.3 on 2026-04-23. Tighter SL reduces the single-trade tail on pyramid-reversal days and feeds into the portfolio-level MC: bust contribution held roughly flat while pass rate ticked up modestly on the Pepperstone 52-month panel.

### Portfolio MC anchors (2026-04-23)
- 2026-04-20 Alchemy baseline (Striker v4.4 + Aegis v4.2 era).
- 2026-04-23 Pepperstone directional (all three at candidate versions): failed the bust gate raw, passed after the Aegis 1R correction.
- Post-Guardian-risk-relock (G 0.34% / S 1.00% / A 1.50%): cleared both gates.
- Figures: [`docs/mc_anchor_history.md`](../../../../docs/mc_anchor_history.md).

### Cross-reference
- 2026-04-23 joint version lock (commit `e40802d`)
- `docs/adr/2026-04-17-striker-v4.3-pyramid.md` (pyramid architecture — still load-bearing; v4.4 does not change pyramid)

---

## [v4.3] — 2026-04-17 🔒 LOCKED (superseded by v4.4 on 2026-04-23)

**Status:** Historical. Was active on FXIFY $200K challenge 2026-04-17 → 2026-04-23. Risk 1.00%. Saved in TradingView as "Striker v4.3". Initial tracked version.

### Parameters
| Field | Value |
|---|---|
| Instrument | DJ30 (US30) |
| Timeframe | 15min |
| Direction | Long breakout |
| Risk per trade | 1.00% |
| Pyramid size | 350% |
| T1 partial | removed |
| Exits | ATR stop and take-profit, breakeven, two-phase trail, max hold |
| Limits | daily DD cap, max trades per day |
| **DXTrade `contractValue`** | **10** (default of 1 produces ~7% per-trade risk — critical) |

### Design intent
Capture pyramid-cohort profit concentration. An MFE/MAE diagnostic on the prior version showed the pyramid cohort produced nearly all of the profit; v4.3 removes T1 and raises pyramid size to 350% to fully exploit that pattern.

### Backtest (4yr)
Profitable over the 4yr panel with a high win rate; μ/σ was the lowest in the portfolio.

### Known concerns
- **Very long max DD duration (N=1)** — single occurrence in 4yr window. No statistical basis for expectation. Monitor live.
- **μ/σ is lowest in portfolio.** v5 rebuild queued post-challenge.

---

## Change convention

Each entry: version, date, lock status, parameters (full snapshot or delta), rationale, backtest metrics if re-run, cross-reference to Notion decision page.

Tag in git on lock: `git tag striker-vX.Y && git push --tags`.
