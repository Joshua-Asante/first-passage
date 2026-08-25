# Phase B Lane B1 — 20-session forward paper-log tracker

**Purpose:** the real-time observation instrument licensed by B1.3's `ADMIT` ruling
(2026-08-24). Task B1.5's "on admit" branch — B1.1 found no historical δ, so the historical-test
alternative does not apply; this is the forward-only path.
**Plan owner:** [`Phase B mechanism supply`](../../superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md)
§Lane B1, Task B1.5.
**Falsifier findings owner:** [`B1.0-B1.4 results`](2026-08-23-phase-b-lane-b1-falsifier-results.md).

**This file is scaffolding, not data.** No session has been logged yet — it was created
2026-08-24 to have the tracking structure ready the moment the first real session lands, not to
imply any observation has already happened. Every row below is filled in only from a real,
same-day (or next available session) observation — never backfilled from memory, never
estimated, never fabricated to fill a gap.

---

## Protocol (frozen before any row is logged)

1. **Each trading session, ~15:50–15:55 ET:** check Financial Juice
   (financialjuice.com/News/.../MOC-Imbalance.aspx, or its public X/Telegram mirror) for a
   same-day signed imbalance figure (S&P 500 / Nasdaq 100 / Dow 30 / Mag 7). Record whichever
   index figure is present; if none is posted that day, log the session as
   `NO-SOURCE-THAT-DAY` — this is itself a data point (measures the source's actual coverage
   rate, one of the open caveats B1.2 named) and must not be silently skipped.
2. **Sign convention:** a positive (buy-side) imbalance is faded short in MES for the
   16:01–16:45 ET wake window (per the plan's mechanism line); a negative (sell-side) imbalance
   is faded long. Record the raw signed figure, not just the direction, so the log can later be
   cut by magnitude if a threshold effect appears.
3. **Outcome measurement:** MES price action across the 16:01–16:45 ET wake window (real CME
   hours — see the B1.0 correction: this window is continuous on every session except the
   last trading day of the month, which still carries the narrower 16:15–16:30 ET pause).
   Record entry-equivalent price, exit-equivalent price (or a fixed hold-to-close proxy if no
   real position is taken — this is a **paper** log, zero capital, per the plan's own framing),
   and the realized move in the faded direction.
4. **Win/loss tag:** win = price moved in the faded direction by the session's end of the wake
   window; loss = it did not. Record the raw move too — a near-miss and a clean loss both count
   as losses for the win-rate tally, but the raw numbers matter for later cost-hurdle scoring
   (this lane's own B1.0 recompute: ≈3.46 MES/ES points needed net of the 4x cost-law hurdle).
5. **No mid-log changes to the protocol.** If a flaw in this protocol is found mid-run, log the
   finding and keep going under the frozen rule (or stop and re-freeze explicitly, dated) — do
   not silently adjust the sign convention, window, or source partway through the 20 sessions.

## Target the log is read against (from B1.4, already scored — not re-derived here)

Per [`shape_feasibility_map_2026-08/RESULTS.md`](../../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md)
§6.2 (`bounded_clustered`, risk=$275): cadence 2/week needs **win_rate ≥65%** (clean `FEASIBLE`);
cadence 3/week needs **≥65%** clean or **60%** (`MARGINAL`, not a pass). B1's mechanism is
predicted at ~2-4 events/week — the log should track actual weekly event count alongside the
win-rate tally, since a lower realized cadence than predicted changes which target column
applies.

## Kill criterion (frozen, from the plan — verbatim)

> "Paper-log mean net capture below the recomputed hurdle at 20 sessions → dead, registry row,
> no card ever authored."

At 20 logged sessions (not 20 calendar days — a `NO-SOURCE-THAT-DAY` session still counts toward
the 20, since source coverage is part of what's being measured), compute mean net capture (raw
move minus the ≈3.46-point cost hurdle from B1.0) and compare against both the hurdle itself and
the B1.4 win-rate target. If it fails either, the lane is dead and this file's own final entry
should record that disposition with a `docs/rejected_candidates.md` row, per this task's own
self-clearing kill-criterion license (no operator judgment needed for a numeric threshold miss).

---

## Log

| # | Date | Source status | Signed imbalance | Fade direction | MES realized move | Win/loss | Notes |
|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | *(no sessions logged yet — first row lands on the first real trading session after this file's creation)* |

---

## Running tally (updated as rows are added)

- Sessions logged: 0 / 20
- `NO-SOURCE-THAT-DAY` count: 0
- Win rate so far: n/a
- Mean net capture so far: n/a
- Disposition: **not yet evaluable** (needs ≥1 logged session)
