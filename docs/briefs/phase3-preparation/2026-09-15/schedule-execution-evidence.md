# Scheduled execution inside an M15 source bar

Status: bounded tooling design accepted by programme coordinator on 2026-09-15; no historical fill-model ratification or F1 freeze.

TB-S2 RC-8 requires cancellation at cutoff, market flatten at flatten-start, and confirmed flat by the own-flat deadline. RC-4 preserves the TV fill model; RC-6 requires lifetime-scoped marks. Regular flatten-start 15:55 lies inside the 15:45–16:00 source bar. Consuming the entire bar before flatten may execute stops or apply extremes that occurred after the position should be closed. A quote at 15:55 alone does not establish the earlier event sequence.

The implementation therefore accepts an explicit execution-evidence provider for source-instant quotes and chronological segments at schedule boundaries. It validates their source/path bindings, nonoverlap, coverage and aggregate consistency. Those checks detect malformed input; they do not certify historical provenance. Missing or ambiguous chronology while positions or working orders are relevant returns NEEDS_CONTEXT. Synthetic tests supply labeled planted chronology; they do not demonstrate actual provider availability.

Evidence requirements follow consumption. The source factory validates supplied
rows against their retained source bars, including contradictory quotes or split
segments. Replay requests splits only for legs with positions, pending orders or
capacity reservations. Inactive legs retain their original bar, and every adapter
still receives that original M15 bar once. A flat deadline check consumes no
price. These rules do not require unused all-leg quotes or change schedule
chronology, source-session coverage, or RC7's observed-union rule.

Original M15 indicator updates and on_bar calls remain once per completed source bar. Execution segments must not create extra strategy signals, duplicate costs or extrema, shift entry eligibility or forget pending orders. Actual runtime executions continue to use broker-confirmed facts. The shared pure schedule determines instants for both normal runtime and path replay; path identity is separate from the immutable source schedule.

Alternatives requiring separate acceptance include a newly ratified interpolation/model convention or finer historical execution evidence. Previous-close pricing, full-bar-derived invented segments and next-bar flatten would change accepted semantics and are not implicit fallbacks. No feed purchase is authorized. Historical outcome-bearing paths consuming this evidence remain blocked until provenance and any required model amendment are accepted; independent tooling and synthetic tests continue.

## Addendum 2026-09-23 — Path-position bracket convention (RATIFIED 2026-09-23)

**Status:** RATIFIED 2026-09-23 (revision 2; operator ruling below). Drafted at the operator's direction on 2026-09-23 ("I want to ratify a timing convention to unblock the replay"; the operator chose a bracket over adverse-only and interpolation). It is the "newly ratified interpolation/model convention" route named above, not finer historical evidence, and it authorizes no build: T00 step 2 remains unratified ([T00 return §7.8](../../handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md#78-operator-rulings-on-the-return-2026-09-23)).

*Revision 2 (PR #469 review, four P2 findings):* revision 1 re-ordered the bar's extremes, which `BookReplay._split` rejects because it changes the accepted emulator path. It fed run A's lows to both evaluations, which can manufacture agreement. It left pending-only legs undefined. This revision keeps the accepted path, evaluates each run on its own, and defines the pending-only chronologies.

**Scope.** A schedule instant (entry cutoff, flatten-start, own-flat deadline) that falls strictly inside an M15 source bar, for a leg that has a position, pending orders or a capacity reservation at that instant. Instants on a bar boundary, and inactive legs, keep the rules above: the original bar consumed once, one `on_bar`, and no extra signals, costs or extrema.

**The path is fixed; only the instant's place on it is unknown.** The accepted emulator path of a bar is fixed by `BookReplay._split` (`replay.py:257`): the open, then the extreme nearer the open, then the far extreme, then the close (`vertices`, reduced by `turns`). For O=100, H=120, L=90 that path is 100→90→120→close. The convention never re-orders it. Each run places the schedule instant at one **vertex** of that path. The prefix segment is the path up to the vertex and the suffix is the rest, so the split aggregates to the source bar and preserves its turning points. **No validator or model amendment is required.** This was checked mechanically against `_split`'s aggregate and `turns` rules: 76,626 vertex splits over 20,000 random bars plus the tie cases (`H−O = O−L`, flat opens and closes) all pass.

**Two runs, per leg, by what the instant acts on:**

| Leg at the instant | Run R1 | Run R2 |
|---|---|---|
| Holds a position (flatten-start, own-flat deadline) | Instant at the path vertex that is the position's **adverse** extreme (L long, H short) | Instant at the path vertex that is its **favourable** extreme (H long, L short) |
| Pending orders only (entry cutoff) | Instant at the **close** vertex: the whole path runs before the cancellation, so every trigger in [L, H] fills (the **fill** chronology) | Instant at the **open** vertex: nothing on the path runs first; every pending order is cancelled at the open price (the **cancel** chronology) |
| Both | The position rule; pending orders execute exactly as the path prefix reaches them | Same |

Everything the accepted path reaches before the chosen vertex executes in that run: stops, targets, fills. A position the instant leaves unchanged keeps the original bar's lifetime marks (RC-6). Direction is never assumed for a pending-only leg: the two chronologies are the path's endpoints.

**Verdict.** Each run is a complete replay and is **evaluated on its own**, with its own daily P&L and its own `intraday_low` series passed to `simulate_path`. A path's outcome (eval PASS, BUST or neither at the horizon) is taken only where R1's and R2's own evaluations agree. Otherwise the path is **UNDETERMINED**, reported as its own count and never folded into PASS or BUST. A conservative hybrid (R2's P&L with R1's lows) may be reported, labelled as a hybrid, but it never contributes to the verdict.

**What it claims, and what it does not.**
- R1 and R2 are extreme **vertex placements** on the accepted path. They are not proven bounds: the true instant can fall between vertices. For a position, the adverse vertex is reached only after whatever the path visits first, which can include a favourable target fill. Agreement means the outcome does not depend on the instant's place among the path's vertices.
- For pending-only legs, the fill/cancel pair is explicit, but neither run is labelled adverse.
- Legs are placed independently, so a run's cross-leg combination is not asserted to be one real historical chronology.
- The convention replaces one P7 blocker only, the source-instant schedule evidence. The source calendar, the startup-policy binding (`PRODUCER_GAPS`, `production_source.py:38–45`) and the private ports and panels remain open.

**Implementation boundary (for a later, separately authorized build).** Each run supplies its vertex splits through the existing `schedule_quotes` provider (`split_bar` / `split_interval`), with `prefix.close` equal to the chosen vertex's price. `_split` validates them unchanged. Provenance records R1 or R2 for every path. Previous-close pricing, next-bar flatten, re-ordered extremes and single-path interpolation remain excluded.

**Operator ratification:** RATIFIED — operator, 2026-09-23, in session, verbatim: "ratify the convention and merge 469". Revision 2 is in force as the accepted convention for schedule instants inside an M15 source bar. It authorizes no build; implementation needs its own GO (T00 step 2 remains unratified).
