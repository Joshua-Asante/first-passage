# Q-FIRMEOD-1 — Verdict pre-registration

**Frozen:** 2026-08-23, before Phase 1 runs. Byte-unedited from this point forward —
amendments via a fresh Q, never an in-place edit (brief-authoring Known Trap #12).
**Companion Pre-Q:** [`../Q-FIRMEOD-1-eod-breach-clock-bulenox-blusky.md`](../Q-FIRMEOD-1-eod-breach-clock-bulenox-blusky.md)
**Committed at:** commit `9bb650c` (2026-08-23), Section 0 anchors (`core/mc/simulation.py`,
`core/mc/preflight.py`, `core/firm_rules.py`) last modified `94041d9` (2026-08-23),
byte-unchanged from the brief's own Section 0 citations.

---

## Frozen gate table (verbatim from the brief's own Section 6 — not restated with any drift)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | CLOCK holds AND LOCK holds | `INTEGRATE` — record the `trailing` branch as evidence-ratified for Bulenox/BluSky bust-rate use; discharge audit finding B4. No `dd_type`/constant edits — the branch is validated, not changed. The F2 magnitude gap stays open and unquantified — this verdict does not speak to it. |
| `FALSIFIED` | CLOCK fails (seed diff flips) OR LOCK fails (lock-adjacent language found) | `STOP` — this brief's $0 check is complete; the defect is priced, not fixed. Re-proposal bar: a successor brief (named, not opened here) is owed to (i) re-run the intraday-honest fix across all 7 tiers per the W1 ADR pattern, and/or (ii) re-classify the affected firm's branch to `trailing_locking` with sourced lock terms, **before** any Bulenox/BluSky bust-rate figure is cited in a cross-firm capital-allocation comparison. |
| `AMBIGUOUS-HOLD` | either cheap check cannot execute at $0 | `ITERATE` — name (do not open) a successor to re-attempt the blocked check(s) on a re-test date; record which tier(s)/page(s) were blocked and why. |

## Frozen falsifier text (verbatim from Section 4)

**Reject H-FIRMEOD-1 → `FALSIFIED` if:** CLOCK fails (the one-seed diff on a tested Bulenox
tier shows a nonzero `bust_trailing` count change between `intraday_low` populated vs `None`)
**OR** LOCK fails (the primary-source re-read surfaces lock-adjacent language — "lock," "stop
trailing," "cease," "no longer trail," "fixed at" — for either firm that contradicts the
current `dd_type="trailing"` never-locks classification).

**Accept H-FIRMEOD-1 → `RESOLVED` if:** CLOCK holds (no flip) **AND** LOCK holds (no
lock-adjacent language found).

## Frozen method (Section 7, restated so the read is auditable, not renegotiated after seeing data)

- **Phase 1a — LOCK.** Re-open the primary Bulenox pages (`bulenox.com/help/qualification-account/`,
  `/help/master-account/`) and BluSky's cited pages (`help.blusky.pro` evaluation-rules article
  12434059, funded/sim-funded rules) and grep for lock-adjacent language, same discipline that
  originally surfaced Tradeify's verbatim FAQ denial and MFFU's article citation. If the live URLs
  are unreachable, fall back to the Wayback Machine capture nearest the code's own citation date
  (2026-07-01 through 2026-07-27) as the primary-source substitute — not a fresh live re-crawl of
  a changed site, and not a secondary/affiliate summary treated as primary.
- **Phase 1b — CLOCK.** Diff `simulate_path`'s `bust_trailing` outcome for a Bulenox
  `dd_type="trailing"` tier with `intraday_low` populated vs `None`, reusing an
  **already-committed** path array — no new market data, no new discovery trial. A pre-existing
  engine unit-test fixture (`tests/core/test_mc_intraday_barrier.py`, on disk since the
  2026-08-14 public-transition base commit, predating this brief) qualifies as "already-generated"
  under this rule if its firm-geometry parameters (starting equity, `trailing_dd_pct`,
  `daily_loss_pct`) match a real `FIRM_RULES` tier's `firm_kwargs()` output exactly — it is not a
  fresh simulation authored for this brief, only a fresh *invocation* of code and fixtures that
  already existed.
- **Phase 2 — Verdict assertion.** Apply the frozen gate table above mechanically to whatever
  Phase 1a/1b actually produce. No threshold in this file may be loosened, tightened, or reworded
  once Phase 1 has been run even once. A miss is a miss.

## Explicit non-negotiables

- LOCK's falsifier fires on **finding the language**, not on a downstream judgment about whether
  that language is reachable by the currently-simulated horizon (Qualification/eval-only, since
  `simulate_path` treats "pass" as absorbing and never simulates a funded/Master stage). That
  scope question is real and must be recorded, but it does not get to silently convert a
  found-lock-language result into a `RESOLVED` by argument after the fact — it is successor-brief
  material (re-proposal bar), not a live override of this table.
- CLOCK's falsifier is satisfied by **one** tested Bulenox tier flipping, per Section 5's explicit
  bar against substituting a full multi-tier campaign — a single reused deterministic path is
  sufficient and is not to be second-guessed as "not enough seeds" after the fact.

**Committed:** 2026-08-23, same session as the brief's own operator GO. Phase 1 has not run as of
this commit.
