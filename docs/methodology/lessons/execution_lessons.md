# Execution Lessons Registry

This file is the canonical anchor for behavioral lessons surfaced via the
live-execution-journal pipeline. Each lesson must be tied to:

1. A **dated incident** (specific trade, specific date)
2. A **dollar cost or counterfactual gain** (so the lesson is load-bearing, not ceremonial)
3. A **rule statement** in imperative form (do X, never do Y)
4. A **watch-point** (which Step 6 pattern check fires for this lesson)

**Promotion criteria:** A pattern graduates from candidate to promoted lesson
when EITHER (a) a single incident with dollar cost >$3K surfaces, OR (b) the
same pattern fires across three separate review windows. E1 and E2 promoted
on (a); E3 currently candidate awaiting (b).

**Demotion criteria:** A promoted lesson demotes if 12+ months pass without
the watch-point firing AND the structural condition that produced the lesson
no longer exists (e.g., strategy code changed in a way that eliminates the
pattern). Demotion is rare; lessons mostly accumulate.

> ⚠ **2026-08-14 — E1–E4 promotion/demotion frozen.** Watch-point source
> (`scripts/journal_review.py`) retired 2026-07-11, so firings cannot accrue.
> The 12-month demotion clock for E1/E2 (dated from the 2026-04-29 promotion)
> now measures calendar time against a dead feeder, not live pattern survival;
> an auto-demotion ~2027-04 would record venue retirement as pattern death.

---

## E1 — Trust the design through macro

**Status:** PROMOTED 2026-04-29 · ⚠ DORMANT 2026-08-14 — watch-point structurally unreachable (`journal_review.py` retired 2026-07-11). Demotion clock is now measuring calendar time against a dead feeder, not live pattern survival.

**Anchor incident:** 2026-04-07 Guardian skip during US-Iran macro-stress window.

**Counterfactual:** Backtest fired a valid Guardian XAUUSD long entry on Tue
2026-04-07. The trader skipped it on the basis that the Iran-Hormuz macro
escalation made the position too risky. The strategy held the position 13
days — through the entire macro window — and exited on 2026-04-20 at +$3,752
realized counterfactual. This was the largest single winner in the strategy
CSV for the surrounding window. The skip "to protect against macro" cost the
biggest gain.

**Rule:** Never skip a valid system signal based on a macro-volatility forecast.
The strategy's filter stack (EMA slope, BB position, ATR expansion, hour blocks,
day-of-week filters) already handles volatility regime. Discretionary overrides
on macro thesis are systematically wrong over the panel.

**Mechanism (why this fails):** The strategies were calibrated against a 52-month
Pepperstone panel that includes the 2022 hostile gold regime, the 2023 disinflation
regime, the 2024 election regime, and the 2025-2026 geopolitical regime. The
filter parameters that survived this calibration are *already adapted* to
macro-volatility periods — that's what "regime-adaptive via base signal logic"
means. Adding a discretionary macro filter on top double-adjusts what's already
captured, and the discretionary judgment systematically penalizes the right tail
(macro-volatile periods are when the strongest trends form).

**Connection to standing doctrine:** Reinforces the "no regime overlays" principle
locked 2026-04-23 (Hormuz overlay deactivated). Discretionary skips on macro
thesis are operationally equivalent to a regime overlay applied at execution
time. Same failure mode, different layer.

**Watch-point:** `check_macro_skip` in `scripts/journal_review.py`. Fires when
skip rate on tier-1 macro days (CPI/FOMC/NFP/BOJ) exceeds baseline by 1.5×
with at least 2 macro-day skips in the window.

**Output trigger:** When E1 fires, the watchlist message references this lesson
by name and dollar cost. Do NOT re-derive the rule each time — the registry is
the source.

---

## E2 — Don't decompose intended single-position holds

**Status:** PROMOTED 2026-04-29 · ⚠ DORMANT 2026-08-14 — watch-point structurally unreachable (`journal_review.py` retired 2026-07-11). Demotion clock is now measuring calendar time against a dead feeder, not live pattern survival.

**Anchor incident:** 2026-04-15 Aegis intra-trade discretion on USDJPY.

**Counterfactual:** Backtest fired one Aegis entry signal at 12:30 USDJPY for a
35-lot position, held to 13:45 BB-mean exit, +$6,467 realized counterfactual.
Live execution decomposed this into three separate entries totaling ~35 lots
across the same window. One of the three sub-entries hit its individual stop
loss while the other two continued. Net realized: +$362.

**Execution gap:** $6,105 ($6,467 − $362). Largest single-day execution leakage
in the 7-week 04-29 audit window.

**Rule:** When a FIRE alert specifies a single entry size, execute it as a
single entry. Do not re-enter on each minor BB-touch within the held position.
Re-entering decomposes one trade with one stop into N trades with N stops,
asymmetrically increasing tail risk. The strategy's R-budget is calibrated
against single-entry execution.

**Mechanism (why this fails on Aegis specifically):** Aegis carries 1.50%
per trade — the highest allocation in the portfolio. Splitting a single
intended 35-lot position into three sub-positions doesn't change total
exposure, but it does change DD geometry: each sub-position has its own
1R worst-case loss. The aggregate worst case for three split sub-positions
is ~3R if they all hit stops near-simultaneously, vs 1R for the single
intended position. On Aegis at 1.50% per trade, that's the difference
between -1.50% and -4.50% on a single coordinated mean-reversion failure
— directly contesting the FXIFY 5% daily DD cap.

**Connection to standing doctrine:** Aegis's BE logic IS the edge — 41% of
winners are BE-manufactured. Splitting an entry undermines the BE-manufactured
winner mechanism, because the BE trigger fires on the original entry price;
sub-entries at later prices have different effective BE points and degrade the
BE conversion rate.

**Watch-point:** `check_discretion_on_largest` in `scripts/journal_review.py`.
Fires when TAKEN-DISCRETIONARY events concentrate on the highest-allocation
strategy with at least 2 events and >50% concentration. Aegis-specifically,
the multi-fill-on-single-signal pattern (which the pairing logic flags
automatically for non-pyramid arch).

**Output trigger:** When E2 fires, the watchlist message references this
lesson by name. The discretionary detail line shows the multi-fill count
and aggregate gap, anchoring the abstract pattern to concrete dollar cost.

---

## E3 — Capture rationale at skip time, not retrospectively

**Status:** CANDIDATE (not yet promoted; awaiting either single >$3K incident
or three firings across separate windows) · ⚠ DORMANT 2026-08-14 — promotion
counter structurally unreachable (`journal_review.py` retired 2026-07-11);
firings cannot accrue.

**Observation:** When skipped signals are reviewed weeks after the fact, the
recall of "why I skipped" tends toward reconstruction rather than recall.
Reconstructed rationales are systematically more flattering than the
as-experienced ones — they tend to invoke risk management, market structure,
or strategy concerns that may not have been present in the moment of decision.

**Provisional rule:** One-line skip-log entry at the
moment of skip — date, strategy, alert tag, one-sentence reason. If under
60 seconds of effort isn't tolerable in the moment, that itself is a signal
that the rationale being constructed is post-hoc.

**Why not yet promoted:** The dollar cost of "post-hoc rationale" is hard to
isolate from the dollar cost of the underlying skips. E1 and E2 each isolate
to a specific trade. E3 is a procedural lesson that affects rationale quality
but not directly P&L. The registry needs either a documented case where
post-hoc rationale led to a recurring failure pattern (n=3 firings of the
same masked-skip pattern), or a single incident where post-hoc rationale
produced a wrong decision with measurable cost.

**Watch-point:** Indirect — when MISSING rationale appears for ≥3 skips in a
single review window, that's evidence the discipline isn't operationalized.
Three consecutive review windows with ≥3 MISSING rationales each would
trigger promotion.

---

## E4 — Entry latency from manual SL/size adjustment (feed-realign lag)

**Status:** CANDIDATE 2026-06-01 (single anchored incident −$270.82, below $3K; firing 1 of 3 for promotion) · ⚠ DORMANT 2026-08-14 — promotion counter structurally unreachable (`journal_review.py` retired 2026-07-11); firings cannot accrue.

**Anchor incident:** 2026-05-29 Striker DJ30 v4.5 long. The signal was running on the **Pepperstone** indicator (entry 51004) while the execution feed is **Alchemy** (entry 51027, ~+23pt basis). Manually adjusting SL and lot size to the broker feed introduced fill latency: the DXTrade entry filled at 51048.05 — **+21pt above the Alchemy signal** — because the bar broke up during the manual adjustment. Exited at 51050.05 (trail), realized +$30.

**Execution gap:** **−$270.82.** Verified Striker DJ30 v4.5 strategy backtest counterfactual = +$300.82 (slippage=2 already baked in); realized = +$30 = **10.0% edge captured**. Exits were ~aligned (~51050); essentially the entire gap is the +21pt late entry.

**Rule:** Keep the live indicator on the **execution feed (Alchemy)** at all times, so there is nothing to hand-translate at fire time. Never re-derive SL/size manually from a different-feed indicator during the fire window — the adjustment latency, not the feed price basis, is what eats the edge on fast breakouts.

**Mechanism (why this fails):** A breakout strategy's edge front-loads into the first move after the signal. When the indicator is on a different feed than execution, the trader must translate SL/size manually at fire time; that costs seconds, and on a fast breakout each second is adverse entry slippage. The price-basis difference between feeds (~23pt) is benign if entry and SL shift together (R preserved); the **latency** it induces is the real cost. DJ30 here traveled only ~25pt signal→trail-exit, so a 21pt late entry captured ~10% of the move.

**Connection to standing doctrine:** Execution-layer instantiation of the N-2026-05-29 feed-divergence Notice (`docs/notes/notice/N-2026-05-29-pepperstone-alchemy-feed-divergence.md`) — that Notice tracks price-basis divergence; E4 tracks the execution-latency cost it induces. Reinforces fxify-challenge Core Principle 1 ("trade the system") — the system assumes a fire-time fill, not a fire-plus-manual-adjustment fill.

**Watch-point:** Entry-slippage on TAKEN-ON-SPEC fills (Step 4 per-trade gap) — a cluster of adverse entry slippage on the same broker feed. Surfaces in the weekly deviation table, not one of the four named Step-6 checks. Flag when ≥2 trades in a window show material adverse entry slippage attributable to feed-realign latency.

**Promotion criteria:** CANDIDATE → PROMOTED on EITHER (a) a single entry-latency execution gap >$3K, OR (b) the pattern firing across three separate review windows. This is firing 1 of 3.

---

## Candidate watch-list (insufficient firings, not yet candidates)

These are observations that *might* graduate to candidates if the pattern
recurs. Do NOT cite as lessons; do NOT add to the registry until a clear
incident anchors them.

- **Size-cutting bias.** Hypothesis: when uncertain, the trader executes at
  smaller size than the alert specifies, capping upside without proportionally
  reducing downside. No anchored incident yet. Watch via the size-deviation
  field in TAKEN-DISCRETIONARY classification.

- **Early-exit-on-winner bias.** Hypothesis: closing winners before TP triggers
  a regret-avoidance pattern. No anchored incident yet. Watch via exit-time
  deviation in TAKEN-DISCRETIONARY classification (close_time materially
  earlier than backtest exit_time).

- **First-trade-of-day-skip bias.** Hypothesis: the first FIRE alert of any
  trading day has a higher skip rate than subsequent alerts within the same
  day. No anchored incident; would need pattern detection across dozens of
  trading days.

---

## Doctrine cross-references

These lessons interlock with standing doctrine in `fxify-challenge`:

- **fxify-challenge Core Principle 1:** "Trade the system, not your opinion."
  E1 is the operational instantiation: macro-volatility opinions are a
  specific case of "your opinion" that fail systematically.

- **fxify-challenge Core Principle 2:** "No discretionary overrides."
  E1 (skip override) and E2 (size/timing override) are both discretionary
  overrides. The registered February override on a Guardian long is the
  pre-2026-04 anchor; E1 and E2 are the post-04-23-lock anchors.

- **fxify-challenge Lesson — headlines drive markets, not physical ground-truth.**
  E1 is the execution-layer manifestation. The Hormuz overlay was rejected
  at the strategy layer; E1 catches the same logic re-entering at the
  execution layer.

The execution-lesson registry should therefore be read with `fxify-challenge`'s
Core Principles section nearby — they are the same doctrine at different
abstraction layers.

---

## Versioning & change-log

- 2026-04-29: Registry seeded with E1, E2 (promoted on single-incident anchors
  >$3K). E3 added as candidate.
- 2026-05-07: Live-execution-journal skill authored; this registry becomes the
  output reference for `scripts/journal_review.py` watch-point messages.
- 2026-06-01: E4 added as candidate (entry latency from manual SL/size
  adjustment; anchor 2026-05-29 DJ30, −$270.82, firing 1 of 3) on the first
  weekly execution review run against verified strategy-tester counterfactuals.
- 2026-07-11: **Relocated** from `ops/live_journal/references/` to
  `docs/methodology/lessons/` and **preserved** as a KEEP under the ops CFD-estate
  retirement (ADR [`2026-07-11-ops-cfd-estate-retirement`](../../adr/2026-07-11-ops-cfd-estate-retirement.md)).
  The `live-execution-journal` pipeline (`scripts/journal_review.py`, ECR engine)
  was **retired** in that pass — the E1–E4 watch-point references to
  `journal_review.py` above are now **historical** (the lessons themselves stand;
  the tool that surfaced them is gone with manual trading). This registry survives
  because it is $-anchored methodology, not execution machinery.
- 2026-08-14: E1–E4 Status fields marked DORMANT — watch-points structurally
  unreachable after `journal_review.py` retirement; E1/E2 demotion clock flagged
  as measuring calendar time against a dead feeder, not live pattern survival.
  Lesson bodies unedited.
