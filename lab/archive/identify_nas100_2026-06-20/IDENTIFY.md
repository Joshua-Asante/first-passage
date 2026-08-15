# Identify phase — NAS100 bar feed vs Striker NAS100 v1 trades (prev 2 years)

**Date:** 2026-06-20 · **Loop:** INQHIORI `I` (Identify) only — corpus assembly + characterization.
**Discipline:** SURFACE and characterize what is in the corpus. No Question, no Hypothesis, no Action. Strategy is LOCKED.
**Method:** ground truth computed once (`identify_nas100.py`) → 5-facet multi-modal Identify sweep → adversarial re-check of every observation (41 agents) → synthesis + completeness critic.

## Corpus (verified)

- **Bar feed:** 47,199 M15 bars, **2024-06-19 → 2026-06-19 UTC** (730.7d), via canonical `core/bar_export_loader` (two pages deduped; `Signal=epoch_ms|OHLCV`, epoch is bar-open UTC). Clean CME-hours grid (46,679/47,199 spacings exactly 15m; 393 daily ~75-min CME maintenance breaks; 95 weekend gaps). No data holes.
- **Trades:** 96 legs = **81 base + 15 pyramid_add** (the most-recent-2y subset of the locked 4y/196-leg panel). Trade CSV TZ resolved **empirically = ET** (96/96 price cross-check vs 0/96 as-UTC). **96/96 legs bar-matched.** Net reconciles to file's final cumulative (no double-count).
- **Source-of-truth caveats** that color every figure: (a) `atr11/atr_ratio` = descriptive Wilder-RMA(11), **not** the exact Pine filter; (b) export is **TV-COMPOUNDED** → dollar headlines are not live numbers; (c) 1R cohort **n=1** noisy; (d) 2y subset — do not reconcile counts to the 4y panel.

## Confirmed observations (held + not an artifact)

### Trade anatomy
1. **P&L is hyper-concentrated in the pyramid/rider mechanism.** Adds (15.6% of legs) carry **91.56% of net** (+$115,430, WR 86.7%) vs base +$10,641 (WR 54.3%). The 10 Max-Hold add legs alone = **83.2% of net**.
2. **Not a compounding artifact.** Static-$200k decompounding gives pyramid share **0.9233** (slightly higher than the 0.9156 dollar figure) — mechanism-driven (locked 1000% pyramid; add qty ~10× base), not late-window equity inflation.
3. **Base layer near-breakeven by design**, net-positive ONLY via its own 12 Max-Hold trend-runners (+$24,790); routine 69 `Exit Long` base legs net **−$14,149** (WR 46.4%). Decompounded, base net collapses +$10,641 → **+$460** (corroborates "near-breakeven" *more* strongly than the compounded figure).
4. **All winners exit via Max Hold (15-bar timeout)** — both Max-Hold buckets 100% WR (TP=9×ATR effectively unreachable). This is **survivorship, not a mechanical tautology**: all 22 went adverse (mean MAE −$953); a losing-but-unstopped Max Hold is structurally possible — the closest leg timed out **within 0.32 price points of its SL**.
5. **Position size tracks ATR vol-sizing, not equity growth.** qty vs 1/ATR dominant (base pearson +0.946); `qty = 0.0037·equity_pre/(1.20·ATR·10)` fits r=1.0. Compounding is second-order (partial corr qty~equity|logATR = +0.555).

### Opportunity surface
6. **Reachable surface is thin:** base entries can fire on only **5.73% of all bars** (47,199 → 18,975 Mon/Tue → 3,328 session-hrs → 2,704 post-warmup). Mon/Tue DOW filter is the largest absolute thinner; the hour filter is more aggressive conditionally (cuts 82.5% of DOW survivors).
7. **…but the window is action-DENSE, not dead time:** Mon/Tue 13–17 UTC = 7.05% of bars but **11.80% of total range (1.67× concentration)** — it sits on the highest-volatility US-open hours (~1.7–1.8× off-session mean bar range).
8. **Silent ~2 of 3 eligible days:** 69/208 eligible Mon/Tue sessions fire a base entry (**33.2% density**, 139 idle). Max-2/day cap binds only 12/208 days (5.8%, zero exceedances); within-day slot occupancy ~3% (1 entry / ~33 slots).
9. **TZ axis reconciles cleanly:** all 81 base entries in UTC session-hrs 13–16; all 69 traded dates inside the 208-date eligible set → 33.2% density is **not** a TZ artifact.

### Bar regime (the index itself)
10. **Window dominated by a single ~26% bear-and-recovery cycle:** peak 22,221 (2025-02-18) → bottom **16,375 (2025-04-07, −26.31%, Apr-2025 selloff)** → reclaim ~79d later, inside an overall **+52.29%** uptrend. 1.62× the second-deepest drawdown.
11. **2025Q2 = vol-regime peak (annvol 36.9%) yet 2nd-largest positive quarter (+18.43%):** bullish RALLY vol, not crash vol — deleting the 4-day April crash, the rally-only leg still annualizes to 34.1% (highest of any quarter).
12. **`atr11_median` overstates late-window "expansion":** absolute ATR drifts 17→41 pts tracking the +52% price level, but **ATR-as-%-of-price COMPRESSED H1→H2 (0.142%→0.123%)**; true price-normalized intrabar-range peak is 2025Q2 (0.166%), not the 2026 quarters.
13. **Quarters alternate sharply** between drawdown and trend (lag-1 autocorr −0.481, 4 sign flips/8 quarters); at most ONE sustained low-vol drift stretch (2025Q3, ~2 months) that immediately re-flips.

### Juxtaposition / capture
14. **Harvests intraday bursts, not the index trend:** 15-bar (≤3.75h) maxHold binds on all 96 legs, **100% same-calendar-day**; the 10 add monsters captured a mean **+0.26% intraday** index move; per-leg captured index moves sum to ~+3.04% while the index rose +52.3%.
15. **2026Q2 (+27%): captured the LAUNCH not the run.** Both Q2 add monsters fired Apr 13–14 (~82–84% of ATH) for +$35.6K; then all May–Jun legs were small base legs (−$1,215 to +$1,464) while the index ran another **~18%** to 30,352. Mechanism real (May–Jun base legs never reached the 6-bars-in-profit add trigger). *(only facet-flagged `anomaly`)*
16. **Monsters span 6 of 8 quarters** (every positive quarter incl. modest +2.90% 2025Q4), absent only in the two negative quarters — co-gated by index sign but not magnitude. *(medium confidence; n=8)*
17. **Bent, did not break, through the worst index event:** strat max equity DD co-located in time with the index −26.31% bottom (strat trough 2025-04-07 10:15 UTC, ~3.5h after) but **~5.9× shallower** (frame-sensitive 5.7×–7.4×).
18. **Worst single leg in the 2y panel is a failed pyramid_add** (−$3,865.50, 2025-02-11) — the edge mechanism mis-firing in a non-persistent regime; also the lone n=1 full-stop cohort leg (so "= the 1R figure" is self-referential). *(medium confidence)*

## Rejected as artifacts (adversarial pass) — do NOT read these as findings
- "Max Hold carries +$129,638" → **compounding**: dominance survives decompounding, but the *magnitude* is ~7× inflated vs static-$200k (~$17,840).
- "88% of index movement is untradeable" → **tautology + sign-inverted**: window is 7.05% of bars; strategy captures **1.67× its fair share** and sits on the MOST active hours.
- "Captures cluster mid-range (64–84% ATH)" → **window-subset tautology**: index first hit ≥90% ATH only in the final ~5 weeks; 75.4% of all bars sat in that band; monster %ATH indistinguishable from the full exit population. Also hand-curated (omits T63).
- "Quarterly P&L sign-agrees 8/8" → **compounding**: decompounds to 5/8; correlation collapses 0.792→0.175.
- Magnitude "asymmetric AND convex" → asymmetry **holds** (6.4×, survives decompounding); **convexity is a small-sample cherry-pick** (within-up-quarter rank-corr ≈ 0).
- "Decouples / sat out the March crash" → **window-subset + long-only tautology**: across 24 months it positively couples (+0.517); March silence is a long-only breakout system in a downtrend, and 5.78/6.3pp of March's drop fell on untradeable Wed–Fri.
- "Signal density regime-invariant ~9–13%/qtr" → **denominator error**: true per-quarter density is 28–38%; the deepest down quarter (2025Q1) is the *lowest* (28%, rank 8/8).
- "1R cohort n=1" warning → itself **compounding + leg-classifier**: the fixed-$2,000 threshold admits one compounded pyramid leg (loss/SL ratio 0.38, not a clean stop) and excludes all **16 genuine base full-stops** (avg ~$1,020) → reported 1R ~3.79× inflated.
- "Edge gated by trend persistence" / "long-only filter caps bleed via the ATR gate" → **tautology + mis-attribution**: down-quarter flatness is 0.37% risk-capping + breakeven-long base design; the gate does NOT reduce exposure in selloffs.
- Weekend/Easter-gap narrative → count structure holds; 3 decorations fail (4/13 are mid-week holidays; cited prices ~10–18pt off; "10 days before the bottom" is **time-inverted** — the Easter gap is *after* the 2025-04-07 bottom).

## Notice candidates (FORWARD — for a downstream Notice/gate; NOT investigated, NOT actioned here)
1. **2026Q2 launch-vs-run capture gap:** the edge fired both monsters in the first 2 days then zero adds across the subsequent ~18% multi-week run. Characterize across the full 196-leg panel before treating as structural vs window-specific.
2. **Monster presence co-gated by index sign** (clean 6-vs-2 split) — small-sample (only 2 down quarters); test against the full panel.
3. **Tail shape:** the panel's worst single leg is a failed pyramid_add. Surface for downstream R-multiple / tail-risk gating (n=1 here).
4. **R-multiple normalization is unreliable on this subset** (cohort n=1 by a dollar-threshold artifact). Any metric dividing by 1R should be gated; the SL-distance cohort (n=16, ~$1,020) or full panel (n=18, $3,940) is the defensible basis.

## Scope caveats & completeness gaps
- **Compounded export**: net $126,071 → ~$6,000 static-$200k. Directional/structural conclusions survive decompounding; **no dollar headline is a live number**.
- **2y subset** of the 4y/196 panel — counts, 1R cohort, quarter splits are subset-specific.
- **Descriptive ATR** (RMA-reconstructed from OHLCV), not the exact Pine filter.
- **Not covered:** live/forward execution (edge-captured ratio, slippage, fills); exact-Pine validation of triggers; portfolio/cross-strategy context (corr w/ DJ30/Guardian/Aegis, the 99.83/0.17/4.37 MC anchor, dd_protection); proper R-distribution; any significance/overfit test; bar-level conditions at the fork between a base leg that earns an add vs one that exits fast (the natural Notice follow-on, deliberately not formed here).

## Artifacts on disk
`lab/analysis/identify_nas100_2026-06-20/`: `identify_nas100.py` (producer), `nas100_bars_utc.csv`, `nas100_trades_paired.csv`, `nas100_identify_stats.json`, this `IDENTIFY.md`.
