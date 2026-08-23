# Q-MONSURF-1 — Verdict pre-registration (M-B acceptance battery)

**Frozen:** 2026-08-23, before Phase 3 runs (operator GO given in chat: *"GO on Q-MONSURF-1"*).
Byte-unedited from this point forward — amendments via a fresh Q, never an in-place edit
(brief-authoring Known Trap #12).

This freezes the design choices Phase 2 (§7) calls for that the parent brief itself left as
implementation detail — the parent brief's own H-MONSURF-1 (§4) and §6 gate table govern; this
document only pins down what "simulated quarter," "T-2/T-1," "missed," and "spurious" mean in a
way an acceptance script can actually execute.

---

## 1. Data source (the "already-measured Tradeify cadence distribution")

`lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md` cites
`lab/analysis/c1/tradeify_book_composition_2026-07-23/out/daily_panel.csv` (2026-07-23 vintage,
2020-08-04 → 2026-07-21, 1,556 business days) as the panel behind every §1 statistic. That panel
and the `gap_cadence.py` script that reads it were pruned from the working tree at the 2026-08-08
Great Prune — both retrieved read-only via `git show pre-prune-2026-08-08:<path>`, matching this
repo's own stated retrieval convention (`CLAUDE.md` §Purpose). **No new data pulled, no K spent** —
this is the same committed panel the cited RESULTS already scored, read a second time.

**Active-day definition** (matching RESULTS.md's own methodology, "Active days... corr(daily P&L
on those days)"): a business day is active iff the panel's `combined` column is non-zero that day.

## 2. "Simulated quarter" — resolved to the full frozen panel, not a bootstrap draw

H-MONSURF-1's own text is in tension with itself: "a simulated quarter" (13 weeks) vs. "the full
frozen distribution draw" (implying the whole measured panel). Rather than invent an unspecified
bootstrap scheme (block size, seed, draw count — none of which the parent brief names, and its own
§5 forbids "inventing thresholds the design doesn't specify"), this freeze resolves the tension
conservatively: **run the monitor against every one of the 312 real Mon–Fri weeks in the panel**,
not a synthetic sample. A full-panel pass is a strict superset of a 13-week-quarter pass — if the
monitor clears every real week ever measured, it clears any quarter-length slice of them by
construction — so this is the stronger, not the weaker, bar. If the operator wants a narrower
bootstrap-quarter test instead, that is a distinct, separately-scoped request.

## 3. Week / business-day semantics

- **Week boundary:** Monday-anchored, business days only (weekends already excluded from the
  panel). A week with fewer than 5 business days (a holiday week) is scored on the business days
  it actually has — "T-2" and "T-1" are defined relative to that week's own last business day, not
  to calendar Friday specifically.
- **Breach:** a week where zero of its business days are active (matches RESULTS §1's own
  "zero-trade Mon–Fri weeks" definition, reproduced as 82/312 = 26.3%).

## 4. Alert timing (T-2 / T-1) — frozen operational definition

For each week, on each of its business days in order, the monitor evaluates two checks **using
only information available as of that day's start** (no look-ahead):

- **T-2 alert:** fires if the current day is the week's second-to-last business day **and** no
  active day has occurred yet that week (days 1..current-1, using positions before evaluation).
- **T-1 alert:** fires if the current day is the week's last business day **and** no active day
  has occurred yet that week (days 1..current-1).

A week with only 1 business day (should never occur in this panel, named for completeness) fires
neither check (no T-2 position exists) — this is a design limitation of the T-2/T-1 scheme itself,
not a monitor defect, and is disclosed rather than silently handled.

## 5. "Missed" and "spurious" — frozen definitions

- **Missed week:** a week that breaches (zero active days, §3) for which the monitor did not fire
  **both** its T-2 and T-1 alert. By construction (§4), a fully-inactive week has no active day
  before either check position, so both checks should fire on every breaching week — this is
  asserted, not assumed, by the acceptance battery.
- **Spurious alert:** an alert whose own stated premise is false at evaluation time — i.e., the
  monitor reports "no active day yet this week" on a day when an active day **did** already occur
  on or before that day. This is a pure read-correctness invariant (does the monitor see the data
  correctly), not a business-judgment threshold — an alert firing on a week that later turns out to
  clear (a trade lands on the alert-triggering day itself, or the day after a T-2 alert) is **not**
  spurious under this definition; it is the alert doing its job as a leading indicator. Reading
  "spurious" any more broadly (e.g. "any alert on a week that ultimately clears") would make the
  T-2 check spurious on every one of the 45.2% one-trade-days weeks whose single trade lands
  Thu/Fri — collapsing the leading-indicator design into a lagging one, which nothing in the parent
  brief asks for.

## 6. Gate criteria (verbatim from parent brief §6; restated here as the frozen artifact of record)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | M-B acceptance passes (0 missed / 0 spurious over all 312 real weeks, per §5 above) **and** the triage (M-B/M-C/M-A at their three true gates) is written to the board | `INTEGRATE` — M-B registration-ready; M-C recorded first-live-fill-gated; M-A recorded elective |
| `FALSIFIED` | any missed week or spurious alert, per §5's frozen definitions | `ITERATE` — repair the monitor, never the rule; re-run the frozen draw |
| `AMBIGUOUS-HOLD` | idle-clock semantics unpinnable from DP2's verified facts | `ITERATE` — return to Q-VENUEGEO-1 DP2 sweep |
| `MOOT` | F3 rules "no admissible successor" | `STOP` — not applicable today; F3 has not ruled |

## 7. Explicit non-negotiables

- No re-definition of "missed" or "spurious" once the battery has run, for any outcome.
- All 312 weeks scored and reported regardless of individual outcome — no cherry-picked subset.
- Monitor built and tested as a standalone module — no hard import against
  `ops/c1_rail/c1_rail_telemetry.py`'s live EventLedger schema (parent brief §5, intake amendment).
- Per the repo's own M1-acceptance precedent (`docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json`
  drill methodology), the battery is **mutation-tested**, not merely observed green: a planted
  defect must be caught and reverted before the clean run is trusted.

**Committed:** 2026-08-23. Phase 3 has not run as of this commit.
