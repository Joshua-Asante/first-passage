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
