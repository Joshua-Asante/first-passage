# Execution Lessons Registry

This file is the canonical anchor for behavioral lessons surfaced via the
live-execution-journal pipeline. New lessons use the light format in
[`methodology_lessons.md`](methodology_lessons.md): a **dated incident** (specific
trade, specific date), an imperative **rule**, and its anchor link; no dollar field
is required, and account figures stay private.

**Promotion criteria:** a lesson becomes standing guidance only when it is
high-severity or recurs independently ([AGENTS.md §Continuous improvement](../../../AGENTS.md#continuous-improvement)
item 5); there is no dollar threshold. The legacy entries below record their
original status: E1 and E2 were promoted under the retired >$3K-incident rule,
E3 was a candidate awaiting three separate firings.

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
days — through the entire macro window — and exited on 2026-04-20 with a large realized counterfactual gain (dollar figures redacted 2026-10-15).
This was the largest single winner in the strategy
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

**Output trigger:** When E1 fires, the watchlist message references this lesson
by name and dollar cost. Do NOT re-derive the rule each time — the registry is
the source.

---

## E2 — Don't decompose intended single-position holds

**Status:** PROMOTED 2026-04-29 · ⚠ DORMANT 2026-08-14 — watch-point structurally unreachable (`journal_review.py` retired 2026-07-11). Demotion clock is now measuring calendar time against a dead feeder, not live pattern survival.

**Anchor incident:** 2026-04-15 Aegis intra-trade discretion on USDJPY.

**Counterfactual:** Backtest fired one Aegis entry signal at 12:30 USDJPY for a
single position, held to 13:45 BB-mean exit, with a large realized counterfactual gain.
Live execution decomposed this into three separate entries totaling the same size
across the same window. One of the three sub-entries hit its individual stop
loss while the other two continued. Net realized: a small fraction of the counterfactual (dollar figures redacted 2026-10-15).

**Execution gap:** most of the counterfactual. Largest single-day execution leakage
in the 7-week 04-29 audit window.

**Rule:** Retired 2026-10-25 (rule consolidation D6; LESSONS-E-10): manual FIRE-alert
execution is retired ([ADR 2026-06-30](../../adr/2026-06-30-no-manual-trading-cfd-retirement.md)).
The finding stands: re-entering decomposes one trade with one stop into N trades with N
stops, asymmetrically increasing tail risk against an R-budget calibrated on single entries.

**Mechanism (why this fails on Aegis specifically):** Aegis carries 1.50%
per trade — the highest allocation in the portfolio. Splitting a single
intended position into three sub-positions doesn't change total
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

**Provisional rule:** Retired 2026-10-25 (rule consolidation D6; LESSONS-E-12): manual
signal skips ended with manual execution
([ADR 2026-06-30](../../adr/2026-06-30-no-manual-trading-cfd-retirement.md)) and the
`ops/live_journal` skip surface is gone.

**Why not yet promoted:** The dollar cost of "post-hoc rationale" is hard to
isolate from the dollar cost of the underlying skips. E1 and E2 each isolate
to a specific trade. E3 is a procedural lesson that affects rationale quality
but not directly P&L. The registry needs either a documented case where
post-hoc rationale led to a recurring failure pattern (n=3 firings of the
same masked-skip pattern), or a single incident where post-hoc rationale
produced a wrong decision with measurable cost.

---

## E4 — Entry latency from manual SL/size adjustment (feed-realign lag)

**Status:** CANDIDATE 2026-06-01 (single anchored incident below $3K (dollar figures redacted 2026-10-15); firing 1 of 3 for promotion) · ⚠ DORMANT 2026-08-14 — promotion counter structurally unreachable (`journal_review.py` retired 2026-07-11); firings cannot accrue.

**Anchor incident:** 2026-05-29 Striker DJ30 v4.5 long. The signal was running on the **Pepperstone** indicator while the execution feed is **Alchemy** (~+23pt basis; fill prices and dollar figures redacted 2026-10-15). Manually adjusting SL and lot size to the broker feed introduced fill latency: the DXTrade entry filled **+21pt above the Alchemy signal** because the bar broke up during the manual adjustment. Exited on the trail.

**Execution gap:** realized = **10.0% of the edge** in the verified Striker DJ30 v4.5 strategy backtest counterfactual (slippage=2 already baked in). Exits were ~aligned; essentially the entire gap is the +21pt late entry.

**Rule:** Retired 2026-10-25 (rule consolidation D6; LESSONS-E-14): Alchemy/DXTrade and manual SL/size entry are retired ([ADR 2026-06-30](../../adr/2026-06-30-no-manual-trading-cfd-retirement.md)); feed admission is AGENTS.md Rule 18. The finding stands: the adjustment latency, not the feed price basis, is what eats the edge on fast breakouts.

**Mechanism (why this fails):** A breakout strategy's edge front-loads into the first move after the signal. When the indicator is on a different feed than execution, the trader must translate SL/size manually at fire time; that costs seconds, and on a fast breakout each second is adverse entry slippage. The price-basis difference between feeds (~23pt) is benign if entry and SL shift together (R preserved); the **latency** it induces is the real cost. DJ30 here traveled only ~25pt signal→trail-exit, so a 21pt late entry captured ~10% of the move.

**Connection to standing doctrine:** Execution-layer instantiation of the N-2026-05-29 feed-divergence Notice (`docs/notes/notice/N-2026-05-29-pepperstone-alchemy-feed-divergence.md`) — that Notice tracks price-basis divergence; E4 tracks the execution-latency cost it induces. Reinforces fxify-challenge Core Principle 1 ("trade the system") — the system assumes a fire-time fill, not a fire-plus-manual-adjustment fill.

**Promotion criteria:** CANDIDATE → PROMOTED on EITHER (a) a single entry-latency execution gap >$3K, OR (b) the pattern firing across three separate review windows. This is firing 1 of 3.

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

---

## Versioning & change-log

- 2026-04-29: Registry seeded with E1, E2 (promoted on single-incident anchors
  >$3K). E3 added as candidate.
- 2026-05-07: Live-execution-journal skill authored; this registry becomes the
  output reference for `scripts/journal_review.py` watch-point messages.
- 2026-06-01: E4 added as candidate (entry latency from manual SL/size
  adjustment; anchor 2026-05-29 DJ30, firing 1 of 3) on the first
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
- 2026-10-25: Rule consolidation ruling D6 retired the demotion criteria and the
  E2, E3 and E4 rule statements (rows LESSONS-E-4, E-10, E-12, E-14) as tied to retired
  manual execution; anchors, costs and incident evidence are kept. Prior text at
  `91ccd984693d62c5c83ff3f428188dd47085633d`.
