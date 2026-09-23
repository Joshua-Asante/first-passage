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

## Addendum 2026-09-23 — Bracket convention (PROPOSED; awaiting operator ratification)

**Status:** PROPOSED. Drafted at the operator's direction on 2026-09-23 ("I want to ratify a timing convention to unblock the replay"; the operator chose Bracket over Adverse-only and Interpolate). Nothing here is in force until the operator ratifies it below. It is the "newly ratified interpolation/model convention" route named above, not finer historical evidence, and it authorizes no build: T00 step 2 remains unratified ([T00 return §7.8](../../handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md#78-operator-rulings-on-the-return-2026-09-23)).

**Scope.** A schedule instant (entry cutoff, flatten-start, own-flat deadline) that falls strictly inside an M15 source bar, for a leg that has a position, pending orders or a capacity reservation at that instant. Instants on a bar boundary, and inactive legs, need no convention and keep the rules above: the original bar consumed once, one `on_bar`, and no extra signals, costs or extrema.

**Convention.** Every outcome-bearing path is replayed twice. Each run is a full, deterministic replay with its own labelled synthetic chronology in place of source-instant evidence:

| | Adverse run (A) | Favorable run (F) |
|---|---|---|
| Price at the instant | The bar's extreme against the open position (L for long, H for short) | The bar's extreme in its favour (H for long, L for short) |
| Before the instant | The bar's full range [L, H] is traversed: any stop, or any pending order whose trigger lies in [L, H], executes | The open-to-favourable-extreme leg only: a stop executes only if the open gaps through it |
| Legs the instant does not act on | A position the instant leaves unchanged keeps the original bar's lifetime marks (RC-6). The convention orders events only for the orders and positions the instant cancels or flattens | Same |
| `intraday_low` mark | The adverse extreme | The favourable extreme |

**Verdict.** A path's outcome (eval PASS, BUST or neither at the horizon) is taken only where A and F agree; otherwise the path is **UNDETERMINED**. UNDETERMINED is reported as its own count and never folded into PASS or BUST. The `intraday_low` series handed to `simulate_path` is always run A's, so any bust figure stays conservative.

**What it claims, and what it does not.**
- A and F are the two extreme intrabar orderings. Agreement means the outcome does not depend on the order of events inside the bar under those two orderings. It is not a proof over every possible path.
- For pending entries, filling is not always the adverse branch. A and F take both branches; they do not bound between them.
- The convention replaces one P7 blocker only, the source-instant schedule evidence. The source calendar, the startup-policy binding (`PRODUCER_GAPS`, `production_source.py:38–45`) and the private ports and panels remain open.

**Implementation boundary (for a later, separately authorized build).** Each run supplies its chronology through the existing execution-evidence provider interface as labelled synthetic segments (`A`/`F`), and the provider validates them exactly as above. Provenance must record which label produced each path. Previous-close pricing, next-bar flatten and single-path interpolation remain excluded.

**Operator ratification:** _(pending)_
