# Q-MONSURF-1 — CLOSURE: `RESOLVED` (M-B acceptance battery passes; triage written to the board)

**Verdict:** `RESOLVED`
**Closed:** 2026-08-23
**Lane:** `UNASSIGNED`
**Pre-registration:** [`Q-MONSURF-1-verdict-preregistration.md`](../pre-registration/Q-MONSURF-1-verdict-preregistration.md) — frozen 2026-08-23, before Phase 3 ran
**Spend / K:** $0.00 · K consumed: 0 — re-reads the already-committed `daily_panel.csv` (2026-07-23
vintage), retrieved read-only from the `pre-prune-2026-08-08` tag; no new data pulled
**Live effect:** none directly — a standalone module built and tested, not wired to
`ops/c1_rail/` or any live account; STATE.md board triage updated (Phase 1 deliverable)
**Artifacts:** [`idle_clock_monitor.py`](../../../lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08/idle_clock_monitor.py) · [`acceptance_battery.py`](../../../lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08/acceptance_battery.py) · [`RESULTS.md`](../../../lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08/RESULTS.md) · [`RUN_LOG.txt`](../../../lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08/RUN_LOG.txt)

---

## 1. Verdict (§6 asserted against actual results)

| §6 route | Trigger condition | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | M-B acceptance passes (0 missed / 0 spurious) **and** triage written to the board | Both true (below) | ✓ |
| `FALSIFIED` | any missed week or spurious alert | Neither occurred | — |
| `AMBIGUOUS-HOLD` | idle-clock semantics unpinnable from DP2 | Not applicable — Tradeify-shaped provisional freeze used, as the parent brief's own intake amendment specifies | — |
| `MOOT` | F3 rules "no admissible successor" | F3 has not ruled | — |

## 2. What ran (Phase 0–4 of the parent brief's §7)

**Phase 0 — Rule-0 reads.** Completed the five `[§0-pending content read before lock]` items the
parent brief left unread at intake: `2026-08-02-venue-native-regime-monitor-design.md`,
`PREREG-NAS-ECR-1-live-edge-capture.md`, `2026-06-07-decompound-remc-hold.md` §Addendum,
`c1_cadence_inactivity_2026-08-02/RESULTS.md` (in full, not just the cited headline numbers),
`2026-08-02-tradeify-activity-rule-disposition-spec.md`, and
`M1_MONITORING_ACCEPTANCE.json`. (`2026-08-02-idle-clock-tracking-spec.md`, cited from the activity
spec, was not found at that path in the current tree — not load-bearing for this closure, since
M-B's own frozen design is self-contained in the pre-registration; flagged as a possible stale
cross-reference in that other spec, not chased further here.)

**Phase 1 — Triage written to the board.** `STATE.md`'s "No fixed date / gated" section's single
"five threads stranded on first live fill" blockquote is replaced with the corrected three-gate-depth
read: **M-B** now registration-ready, gated on F3 only (not first live fill) — this closure's own
result. **M-C** (per-fill add-slippage + the ECR discharge vehicle) stays correctly fill-gated.
**M-A** stays elective, not scheduled, its own build-gate scope question still explicitly unruled.
The two genuinely unrelated threads that shared the same blockquote (lifecycle Call-1, ORB decay
re-scope) are kept, now clearly separated from the monitoring triage.

**Phase 2 — Freeze.** See the pre-registration: data source (real historical panel via the prune
tag), the "simulated quarter" ambiguity resolved to the full 312-week panel (a strictly stronger
test than any 13-week draw), week/business-day semantics, and frozen operational definitions of
T-2/T-1, missed, and spurious.

**Phase 3 — Build + run.** `idle_clock_monitor.py` (standalone, no `ops/c1_rail` import) +
`acceptance_battery.py`. Panel parse reproduced every RESULTS.md §1 anchor exactly (1,556 days /
329 active / 312 weeks / 82 zero-trade weeks / 141 one-day weeks) before trusting anything
downstream. Two independent mutation classes planted and caught (false-positive: 380 spurious
alerts surfaced from a single-day-lookback bug; false-negative: exactly 164 = 82×2 missed alerts
surfaced from an always-suppressed lookback), confirming the battery is sensitive to real defects
before trusting its clean result — matching this repo's own M1-acceptance mutation-testing
precedent (`M1_MONITORING_ACCEPTANCE.json` drill methodology). The real, unmutated run against all
312 historical weeks: **0 missed, 0 spurious.**

**Phase 4 — Verdict.** `RESOLVED` per §6.

## 3. What this closure does NOT license

- Does not wire M-B to the live account or `ops/c1_rail/` — Phase 5 (at F3 registration), not now.
- Does not rule M-A's build-gate scope question — still an open, explicit operator ruling request.
- Does not touch M-C, `PREREG-NAS-ECR-1`, or any of their existing thresholds.
- Does not re-freeze idle-clock semantics against a specific successor venue — uses the
  Tradeify-shaped provisional freeze pending Q-VENUEGEO-1's DP2 sweep, per the parent brief's own
  intake amendment.
- Is a logic-correctness test on historical data, not a live-fire test — disclosed explicitly in
  `RESULTS.md` ("Reading this honestly").

## 4. Defects found in the frozen brief

One stale cross-reference noted, not repaired under this closure (out of scope — a different
document): the activity-rule disposition spec cites
`docs/superpowers/specs/2026-08-02-idle-clock-tracking-spec.md`, which does not resolve at that
path in the current tree. Recorded here per Rule 0 discipline rather than silently worked around;
does not affect this closure's own verdict since M-B's design is self-contained in its own
pre-registration.

## 5. Lesson candidates

Below the two-incident bar — watch: this is the second time this session a monitor/acceptance-style
verification benefited from mutation-testing the test harness itself before trusting a clean run
(the first being the repo's own pre-existing M1 `REQUIRED_DRILLS` precedent, cited and followed
here, not re-derived). Not yet load-bearing as a new rule; flagged for whoever next builds an
acceptance battery in this program to consider doing the same.

## Iterate — loop exit

- **Verdict used:** `RESOLVED`
- **Model update:** the estate's monitoring obligations were genuinely conflated into one class
  when they sit at three distinct gate depths; M-B specifically was blocked on nothing but design
  work, not on a venue or a fill, and that design work is now complete and verified.
- **Next:** `ITERATE` (deployment) — Phase 5 (wire to the live account) is named but not opened;
  it fires automatically at F3 registration, not by a fresh Q.
- **Routing:** F3 (successor-venue registration), an existing fork owned elsewhere
  ([`ADR 2026-08-04`](../adr/2026-08-04-tradeify-venue-descope-eval-included.md) §7).
- **Entry packet:** Phase 5 as specified in the parent brief §7 — re-freeze idle-clock semantics
  against the actual successor's DP2-verified rules if they differ from the Tradeify-shaped
  provisional freeze, then wire to the live account via the M1 event schema (if F2 retained it),
  alert-only.
- **Stop rule / re-proposal bar:** N/A for this closure (discharges cleanly). M-A's own build-gate
  scope question is a separate, standing operator-ruling request, not a re-proposal bar on M-B.
- **Board write:** `STATE.md` "No fixed date / gated" section (Phase 1, above) + decision index;
  `docs/briefs/INDEX.md` — this Q moves from Open to Recently closed. Owner: this closure.
- **Registry:** no `docs/rejected_candidates.md` row — this confirms a monitor design works, not a
  strategy/mechanism kill.

## §10 audit-hook discharge

```bash
$ cd lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08 && python acceptance_battery.py
... VERDICT: PASS (RESOLVED)

$ rg -ln "crosstrade|payload|order" lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08/*.py
(no output — no order-send capability in the monitor package)

$ rg -n "c1_rail_telemetry|EventLedger" lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08/*.py
(no output — no hard M1-schema import)
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Closure authored. Pre-registration committed, Phases 0–4 executed same session under operator GO ("GO on Q-MONSURF-1"). `RESOLVED` recorded. | Claude Code (Sonnet 5), operator GO |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-MONSURF-1-closure-resolved.md
```
