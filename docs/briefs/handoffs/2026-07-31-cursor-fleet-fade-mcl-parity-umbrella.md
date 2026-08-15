# CC/Cursor fleet handoff — fade Stage-0 parity on the RULED instrument (umbrella)

**Fleet slug:** `fade-mcl-parity` · **Date:** 2026-07-31 · **Type:** handoff (umbrella, 2 packets)
**Orchestrator:** Claude Code (this session) — owns decomposition, spec freeze, review, integration.
**Workers:** 2 Cursor packets (A, B). Both are **LOCAL-only** (see §0.5 q5).
A third packet (C — vendor-manifest hygiene) was **withdrawn at the pre-dispatch gate**; see §2.
**Base ref:** `origin/main` @ `87cb8c5` (PR #584 merged 2026-07-31).
**Governing:** [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md) (every clause binds per packet) ·
[`docs/superpowers/specs/2026-07-30-tradeify-native-fade-program-design.md`](../../superpowers/specs/2026-07-30-tradeify-native-fade-program-design.md) (the program) ·
[`docs/notes/2026-07-31-fade-stage1-frozen-rulings.md`](../../notes/2026-07-31-fade-stage1-frozen-rulings.md) (the four frozen rulings).

**Nothing in this fleet spends money, opens K, proposes a mechanism, scores a candidate, or
touches the rail.** All three packets are measurement and hygiene.

---

## §0 — Rule 0 reads (production source, verified this session at `87cb8c5`)

Read directly, post-merge. Path first, then the facts, per the `check_brief` fence-parity
convention: `lab/analysis/c1/tradeify_fade_stage0_2026-07-30/design_law.py`.

```
design_law.py:43-49        SESSION_SIGMA_USD = {MYM 119.44 (360min@10:30), M2K 115.58
                           (360min@09:30), MCL 112.70 (240min@12:00), M6A 30.91
                           (360min@09:30)}. HARDCODED, sourced by comment to
                           c1_thirdleg_instrument_map_2026-07-27/RESULTS_stage2.md joint
                           table, "taking the max is deliberate ... most generous reading".
design_law.py:182          df["expressible"] = resolution_barrier_usd <= session_sigma_usd
                           -- NaN compares False, so an unmeasured instrument is not
                           expressible. That fail-safe is load-bearing; do not weaken it.
design_law.py:51-58        resolution_barrier_usd = min(target_pts, stop_pts) * point_value
                           -- the NEARER leg, not the stop.
integrity_1m.py:18-22      RTH_OPEN_MIN = 09:30 ET, RTH_CLOSE_MIN = 16:00 ET (390 min),
                           HALT_SLOT 16:15-16:30. These are EQUITY-INDEX constants applied
                           unconditionally; the module has no product-group awareness.
integrity_1m.py:17         SESSION_ROLL_HOUR = 18 (bars >= 18:00 ET -> next trade date).
roll_windows.py:29         LEAD_SESSIONS_DEFAULT = 2 ("TV leads Databento by 1-2 sessions;
                           take the worst case").
stage1_screen.py:88-90     power_floor(n) = 1.96 / sqrt(n)  -- Clause-N minimum detectable
                           d/s at power 0.50.
cost_pins.py               SPECS["MCL"] = point_value 100.00, tick_value 1.00, group Energy;
                           cost_per_side 1.06 for Energy/Metals => rt_cost $4.12.
c1_thirdleg_instrument_map_2026-07-27/stage2_sigma.py:59
                           windowed_sigma(panel, point_val, start_et, ...) -- the CANONICAL
                           sigma computation. Packet B reuses it; it does not reimplement it.
core/data/tv_exports/cme/SHA256SUMS
                           CLEAN as of 87cb8c5 -- Stage-0 item 7 is DISCHARGED (both ST-EH
                           CSVs on disk, landed by a8f80c2). The "still owed" line naming it
                           is stale; the orchestrator corrects that at integration, not a worker.
```

**Measured by the orchestrator this session** (the finding that motivates packets A and B),
by running the existing Stage-0 modules against the ruled instrument:

```
                     MYM (published)          MCL (RULED, never run)
panel span           2019-05-05 -> 2026-07-29  2023-01-02 -> 2023-12-29
trade dates          1,871                     257
rolls detected       29  (quarterly)           12  (MONTHLY)
sessions excluded    87  (4.65%)               36  (14.01%)
usable after ROLL-EXCLUDE-2026-07-31           221
power_floor          0.0464 (n=1,784)          0.1318 (n=221)   -- 2.84x harder
M2K: 330,032 bars, 2023-only.  MNQ: 2,549,265 bars, 2019-05-05 -> 2026-07-29 (full span).
```

---

## §0.5 — Clarifying questions and pre-answered defaults

**Workers must NOT resolve ambiguity.** Anything not answered here halts to `CURSOR_RETURN.md`
as `NEEDS_CONTEXT`. Pre-answered:

1. **New files or edits to existing modules?** A and B create **new** modules only. Neither may
   modify `integrity_1m.py`, `roll_windows.py`, `cost_pins.py`, `design_law.py`,
   `stage1_screen.py`, `render_results.py`, `RESULTS.md` or `CARD.md` — those carry **published
   MYM figures and a frozen ruling set**; changing them silently moves numbers that four rulings
   were taken against.
2. **If a packet's measurement contradicts a published number, may it fix the source?** **NO.**
   Report the contradiction in your RESULTS file and in `CURSOR_RETURN.md` as
   `DONE_WITH_CONCERNS`. Adjudicating a contradiction against a frozen ruling is an operator
   decision, not a worker's.
3. **May any packet pull data?** **NO.** `$0 spend, K=0` is a program-level constraint. If a
   measurement appears to need data that is not already cached, that is a **finding** — record
   it and stop. Never call `db_fetch pull`. Never call `register_search open`.
4. **May a packet pick a session window / a σ cell / an instrument?** **NO.** Report every
   option side by side. Selection after seeing numbers is the selection effect the whole
   program's ruling discipline exists to prevent.
5. **Cloud or local?** **LOCAL, all three.** A and B read gitignored machine-local parquet;
   C reads gitignored vendor CSV trees. A cloud worktree sees none of them and would
   silently measure an empty directory (ADR Step-0 addendum).
6. **Data root?** Set `FP_DATA_ROOT=C:/Users/joshu/multi_firm_operations/lab/analysis/c1/c1_signal_identity_2026-07-28/data`.
   `dataroot.py` defaults to the primary checkout, but a worktree run must set it explicitly.
7. **Python?** Plain `python` (3.14.3 on PATH, with pandas/numpy/pyarrow/tabulate). Fresh
   worktrees have no `.venv`.
8. **Commit / push / PR?** Commit to your own branch only. Do NOT push, do NOT open a PR, do
   NOT merge. The orchestrator reviews and integrates.

---

## §1 — Context

Four rulings were frozen 2026-07-31 before any mechanism existed —
`ROLL-EXCLUDE-2026-07-31`, `COST-MULT-4X-2026-07-31`, `CONFIG-B-MCL-2026-07-31`,
`SIZING-BASIS-BOTH-2026-07-31`. They resolve the fade program to a **two-sided MCL** construct
at the **4×** cost multiple, with roll-exposed sessions dropped from IS and OOS.

**Stage 0 was never run on that instrument.** Every published Stage-0 number — the integrity
battery, the roll exposure, the declared cost of `ROLL-EXCLUDE` — was measured on **MYM**, which
the same ruling set eliminated. The orchestrator's measurement above shows the two instruments
are not interchangeable on any of the three axes: MCL rolls monthly rather than quarterly (3×
the declared exclusion cost), and its panel is one calendar year rather than seven.

Separately, the only limb MCL currently clears — `expressible` — rests on a **borrowed** σ of
$112.70 lifted as the single largest cell of a 72-cell surface. The repo's own standing lesson
is that a borrowed metric must be bound to its cohort. Nobody has asked whether MCL's σ clears
the $54.93 barrier at a hold horizon the ruled configuration can actually use.

**`make validate` is currently red, and it does not block this fleet.** 11 manifest rows for two
ADR-retired feeds (OANDA, Dukascopy) fail the data gate. That is **un-executed substrate
retirement Phase 5**, not loose debris — see §2 for why it left the fleet. The data gate fires
in the pre-commit hook only for commits that stage something under `core/data/`; packets A and B
touch `lab/` only, so both commit and merge normally against a red `make validate`. Do not
attempt to fix it to get green.

---

## §2 — Claim manifest (dispatch table; orchestrator-owned)

| Packet | Branch | File footprint (DISJOINT) | Status |
|---|---|---|---|
| A — MCL/M2K Stage-0 parity | `cursor/fade-mcl-parity-pA` | `lab/analysis/c1/tradeify_fade_stage0_2026-07-30/instrument_parity.py` (new) · `test_instrument_parity.py` (new) · `RESULTS_parity.md` (new) | **MERGED** PR #590 `a7e5acb` · `DONE` / H-A **RESOLVED** |
| B — MCL native σ cohort check | `cursor/fade-mcl-parity-pB` | `lab/analysis/c1/tradeify_fade_stage0_2026-07-30/sigma_native.py` (new) · `test_sigma_native.py` (new) · `RESULTS_sigma_native.md` (new) | **MERGED** PR #591 `68dda82` · `DONE_WITH_CONCERNS` / H-B **FALSIFIED (limb 1 only)** |
| ~~C — retire stale manifest rows~~ | — | — | **WITHDRAWN at the pre-dispatch gate** |

**Both dispatched 2026-07-31** off `origin/main` @ `df89193`, via
`scripts/dispatch_cursor.ps1`, into `.worktrees/fade-mcl-parity-p{A,B}`. Pre-dispatch gate run
at dispatch time (not authoring time): `origin/main` re-fetched, **no open PRs**, and **neither
target module exists** — so both packets' Phase-0 no-op conditions were false and both were
cleared to proceed. Workers returned via `CURSOR_RETURN.md`; neither pushed, PR'd or merged.

**Both MERGED 2026-07-31, fleet CLOSED.** Footprint discipline held on both: three new files
each, **zero deletions**, no protected file touched, pointer and return files left untracked.
Every worker claim was re-verified by the orchestrator rather than accepted — A's suite re-run
from scratch (20 passed) and its acceptance pins confirmed to be hard literals compared against
computed output; B's borrowed published figures checked line-by-line against
`RESULTS_stage2.md:361/365`, its reuse of `stage2_sigma.windowed_sigma` confirmed by the absence
of any `.std(`/`np.std` call, and its absence tests confirmed adversarial rather than vacuous.

**One concern adjudicated at integration** (B's item 3): the falsifier test was correctly left
**red** by the worker and is now `xfail(strict=True)` with the cohort reason inline. A red test
on `main` reads as "broken" and gets greenwashed; deleting or widening it would destroy the
finding, which the spec forbade. `strict` is the tripwire — if the missing 2021-08 → 2022-12
history is ever pulled, the test XPASSes and strict converts that to a failure, reopening the
cohort question deliberately. Directory suite after integration: **107 passed, 1 xfailed**.

**Fleet-level falsifier (§7 of the skill): not tripped.** Integration cost was well under the
estimated solo-build cost, and neither worker landed a spec-interpretation judgment defect —
B's `DONE_WITH_CONCERNS` was an escalation of a judgment call it correctly declined to make,
which is the contract working, not a defect.

**Why C was withdrawn — recorded so it is not re-proposed.** It was scoped as free hygiene:
delete 11 `SHA256SUMS` rows whose files are absent and whose feeds are ADR-retired. The
pre-dispatch check falsified that framing twice over.

1. **It is a gated destructive phase, not hygiene.**
   [`docs/adr/2026-07-22-challenge-era-substrate-retirement.md`](../../adr/2026-07-22-challenge-era-substrate-retirement.md)
   §Phase 5 *is* this work — "delete OANDA and Dukascopy bytes; remove OANDA from
   `MANIFEST_DIRS`; regenerate affected manifests; update manifest tests and living restore
   instructions" — and `CLAUDE.md` records destructive Phases 5–6 as **separately gated**. The
   packet would have executed half a gated phase, and the wrong half: it forbade `--regenerate`
   and never touched `MANIFEST_DIRS`, so it would have left Phase 5 harder to finish than it
   found it, while turning the gate green and removing the signal that Phase 5 is owed.
2. **The work already exists, stashed.** `stash@{0}` (`WIP on chore/substrate-phase-5-oanda-duka`)
   carries both manifest edits **plus** `docs/ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md`
   and updates to `CLAUDE.md`, `README.md`, `REPO_MAP.md`, `PIPELINES.md`, the substrate ADR,
   `docs/adr/INDEX.md`, `lab/CATALOG.md` and `lab/archive/feed_divergence_2026-06/`. Most of
   that footprint is orchestrator-reserved by §2, so no worker could land it.

**Disposition:** Phase 5 resumes from `stash@{0}` under its own operator gate, with CC, as its
own PR. It is not fleet work and must not be re-cut as a packet.

**Reserved to the orchestrator — no worker writes these:** `docs/SESSIONS.md`, `STATE.md`,
`CLAUDE.md`, `lab/CATALOG.md`, `docs/briefs/INDEX.md`, `docs/adr/**`, `docs/notes/**`
(both ruling notes especially), `docs/superpowers/**`, and every existing file inside
`lab/analysis/c1/tradeify_fade_stage0_2026-07-30/`.

Footprints are disjoint by construction: A and B each create three new files with distinct
names, and neither reads or writes the other's.

---

## §3 — Packet A: Stage-0 parity on the ruled instrument

**Phase-0 staleness check (run FIRST; if already satisfied, return DONE and cite the commit):**

```bash
git log --oneline -5 origin/main
ls lab/analysis/c1/tradeify_fade_stage0_2026-07-30/instrument_parity.py 2>/dev/null && echo "ALREADY EXISTS -- STOP, return DONE with the commit that added it"
grep -n "MCL" lab/analysis/c1/tradeify_fade_stage0_2026-07-30/RESULTS.md || echo "RESULTS.md still MYM-only -- proceed"
```

**Frozen scope.** Create `instrument_parity.py` that runs the **existing, unmodified** Stage-0
modules across `{MCL, M2K, MYM, MNQ}` and renders `RESULTS_parity.md`. Required behaviour:

- Reuse `dataroot.load_1m`, `integrity_1m.*`, `roll_windows.*`, `stage1_screen.power_floor`.
  Import them; do not copy or reimplement.
- **Session windows: report three columns, choose none.** `integrity_1m.is_rth` hardcodes the
  equity-index 09:30–16:00 ET window and has no product-group awareness, so applying it to an
  Energy contract is a category error you must expose rather than silently inherit. Report per
  trade date: (i) **all** bars, (ii) bars inside 09:30–16:00 ET (the published equity-RTH
  convention, for comparability with the MYM row), (iii) bars inside 09:00–14:30 ET, labelled
  **provisional — NYMEX WTI open-outcry equivalent, not verified against a venue source**.
  Do not add a fourth. Do not pick one. Do not edit `integrity_1m.py` to add them.
- Per symbol report: bar count, trade dates, span, zero-bar business days, short sessions,
  rolls detected, exposure windows, sessions exposed (count and %), max absolute roll offset,
  usable sessions after `ROLL-EXCLUDE-2026-07-31`, and `power_floor(usable)`.
- Render a **declared-cost delta table** making explicit that `ROLL-EXCLUDE-2026-07-31` declares
  its cost as 4.65% from MYM while the instrument it governs pays a different figure. State the
  ratio. Do not propose a remedy — the ruling is frozen and revisiting it is operator work.
- Run `cache_coverage.coverage()` from `c1_thirdleg_instrument_map_2026-07-27/cache_coverage.py`
  for MCL and M2K and report whether history beyond 2023 is **already cached** (therefore free).
  **Do not pull under any circumstance**, even if coverage shows a gap. A gap is the finding.

**Acceptance test (this is packet A's falsifier, see §4).** `test_instrument_parity.py` must pin
the orchestrator's measured values as literals. If your run disagrees with any of them, the
panel changed under us — return `NEEDS_CONTEXT` with both numbers, do not edit the pin:

```
MCL   bars 338,735   trade_dates 257     rolls 12   exposed 36  (14.01%)
MYM   bars 2,480,324 trade_dates 1,871   rolls 29   exposed 87  ( 4.65%)
M2K   bars 330,032   span 2023-01-02 -> 2023-12-29
MNQ   bars 2,549,265 span 2019-05-05 -> 2026-07-29
power_floor(221) == 0.1318 (4dp)   power_floor(1784) == 0.0464 (4dp)
```

Plus pure-function tests that run without the parquet, and data-dependent tests that
`pytest.skip` when it is absent (public-clone posture).

**Forbidden moves (A).** No edits to any existing file in the analysis directory. No pull. No
choosing a session window. No editing `SESSION_SIGMA_USD`. No writes outside your three files.

---

## §3b — Packet B: is MCL's σ measured on the cohort the ruling can use?

**Phase-0 staleness check (run FIRST; if already satisfied, return DONE and cite the commit):**

```bash
git log --oneline -5 origin/main
ls lab/analysis/c1/tradeify_fade_stage0_2026-07-30/sigma_native.py 2>/dev/null && echo "ALREADY EXISTS -- STOP, return DONE with the commit that added it"
sed -n '38,50p' lab/analysis/c1/tradeify_fade_stage0_2026-07-30/design_law.py
```

**Frozen scope.** Create `sigma_native.py` that recomputes MCL's session σ **from the 1m panel**
and reports it against the expressibility barrier, cell by cell. Required behaviour:

- **Reuse `c1_thirdleg_instrument_map_2026-07-27/stage2_sigma.windowed_sigma`.** Do not
  reimplement a σ. The whole point is comparability with the borrowed figure; a second
  implementation makes any difference uninterpretable.
- Emit the **full (start_et × duration) σ surface** for MCL at `point_value_usd = 100.0`, on the
  same grid the Stage-2 harness uses. Do not report only the max.
- For each cell, report whether it clears the ruled configuration's barrier
  **$54.93** (`resolution_barrier_usd` at R:R 1.0, stop = target = 0.5 pts — the value already
  in `RESULTS.md`'s expressibility table), and the `subperiod_ratio` `barrier·√n/σ` at n ∈ {4,5,6}.
- **Reproduce or contradict the pinned $112.70.** `SESSION_SIGMA_USD["MCL"]` is commented
  `240min @ 12:00`. Report the value your run gives at that exact cell. Agreement is a PASS;
  disagreement is a `DONE_WITH_CONCERNS` finding, not a fix.
- Report the **cohort question explicitly**: `CONFIG-B-MCL-2026-07-31` records that MCL "pays
  τ_max for the FOMC exclusion (180→120min @09:30)". State whether the 120min@09:30 cell clears
  $54.93, and whether the cells that do clear it are reachable before the **16:45 ET** flat
  deadline. **Report; do not rule.**
- Say plainly, in `RESULTS_sigma_native.md`, what the answer implies for the three surviving
  MCL cells — without changing them: if the config-legal σ is below the barrier, MCL fails the
  expressibility limb the same way M6A did, and the ruled configuration has no feasible cell.

**Acceptance test (this is packet B's falsifier, see §4).** `test_sigma_native.py` must include:

- A pure-function test that the barrier arithmetic reproduces **$54.93** from `stop_pts = 0.5`,
  `target_pts = 0.5`, `point_value_usd = 100.0` via `design_law.resolution_barrier_usd`.
- A test that an **absent** σ cell yields a non-clearing verdict, never a silent pass — mirroring
  the `NaN ⇒ False` fail-safe at `design_law.py:182`. Assert on a genuinely absent cell, not on
  an empty frame (an assertion that passes vacuously is not a guard).
- A data-dependent test pinning the recomputed 240min@12:00 value to **112.70 ± 0.50**, skipped
  when the parquet is absent. If it fails, that is packet B's headline result — report it, do
  not retune the tolerance.

**Forbidden moves (B).** No edits to `design_law.py`, `SESSION_SIGMA_USD`, or anything under
`c1_thirdleg_instrument_map_2026-07-27/`. No new σ implementation. No pull. No instrument
comparison to "pick a better one" — that is the §7 K-multiplying selection the spec forbids.
No writes outside your three files.

---

## §4 — Falsifiable hypotheses

**H-A:** the ruled instrument's Stage-0 profile can be produced by the existing modules without
modifying them, and it differs materially from the published MYM profile. **FALSIFIED** if the
existing modules cannot run on MCL without edits — which would mean Stage-0 is structurally
equity-index-only and the parity work is a redesign, not a re-run. Halt `NEEDS_CONTEXT`.

**H-B:** MCL's borrowed σ of $112.70 reproduces from the panel at its stated cell, and the
expressibility verdict for the three surviving cells is stable under a config-legal hold
horizon. **FALSIFIED** if either the value does not reproduce, or the config-legal cells sit
below the $54.93 barrier — in which case MCL fails expressibility exactly as M6A did and the
ruled configuration has **no feasible cell**. That is a first-class result of this packet, not
an error: report it, do not force agreement.

---

## §5 — Forbidden moves (fleet-wide, in addition to per-packet)

- No writes to any orchestrator-reserved file listed in §2.
- No writes outside your declared file footprint, for any reason.
- No commit to `main`, no push, no PR, no merge.
- No resolving ambiguity: halt to `CURSOR_RETURN.md` as `NEEDS_CONTEXT` instead.
- No touching another packet's files, even to fix an obvious defect — report it instead.
- **No data purchase, no `db_fetch pull`, no `register_search open`.** `$0 / K=0` is absolute.
- **No mechanism.** Nothing in this fleet proposes, scores, or hints at a trading rule. The
  catalog's failed-ORB-fade seed is a recorded harvest Stage-0 kill and must not be revived.
- **No edit to `core/` at all**, and specifically no `SHA256SUMS` edit and no
  `check_data_manifests.py --regenerate` — that is gated Phase-5 work (§2). No Pine, no `ops/`,
  no rail, no lifecycle state, no allocation, no `dd_protection`.
- No `--no-verify`, no skipping gates, no disabling a failing test to go green.
- No editing a frozen ruling, a pinned constant, or a published figure to make a result agree.

---

## §6 — Gate criteria and status taxonomy

**Binary verdict per packet.** The packet's §4 hypothesis returns exactly one of:
**RESOLVED** (spec met, gates green — the normal PASS), **FALSIFIED** (the §4 falsifier fired —
a real result; report it, do not force a pass), or **AMBIGUOUS** (the premise could not be
established either way — return `NEEDS_CONTEXT`, never a guess).

RESOLVED requires all of: (a) the diff touches ONLY the declared footprint; (b) the packet's
acceptance tests are present and green; (c) `python -m pytest` in the analysis directory shows
no new failures; (d) `python scripts/check_boundaries.py` is clean; (e) no forbidden-move
violation. Otherwise FAIL.

**Return contract.** Write `CURSOR_RETURN.md` at the worktree root with exactly one status:

- `DONE` — spec met, gates green.
- `DONE_WITH_CONCERNS` — spec met, but something the orchestrator must adjudicate. State it.
- `NEEDS_CONTEXT` — the spec is ambiguous or its premise is false. State what you need. Do not guess.
- `BLOCKED` — cannot proceed. State why.

Include: files changed, test command run, its output tail, and any deviation from spec. One
`NEEDS_CONTEXT` bounce gets a re-anchor and re-dispatch; a second means the spec was not
freezable and the packet falls back to CC solo.

---

## §7 — Merge order (orchestrator)

A then B, re-running the fast gates between merges. They are independent; B's headline result
reads better once A's panel pins have landed, but neither blocks the other, and either may land
alone. `make validate` stays red throughout — that is the un-executed Phase 5 (§2), not a
regression, and neither packet may touch it.

The single integration commit — SESSIONS entry, manifest statuses → MERGED, board updates, and
the correction of the stale "Stage-0 item 7" owed-line in
[`docs/notes/2026-07-31-fade-stage1-frozen-rulings.md`](../../notes/2026-07-31-fade-stage1-frozen-rulings.md)
— is written **after** all merges, by the orchestrator only.

---

## §10 — Audit hooks (runnable)

```bash
# Packet A landed, reuses rather than reimplements, and did not touch published figures
test -f lab/analysis/c1/tradeify_fade_stage0_2026-07-30/instrument_parity.py && echo "A: present"
grep -n "import integrity_1m\|import roll_windows\|power_floor" lab/analysis/c1/tradeify_fade_stage0_2026-07-30/instrument_parity.py | head
git diff --name-only origin/main...HEAD -- lab/analysis/c1/tradeify_fade_stage0_2026-07-30/integrity_1m.py lab/analysis/c1/tradeify_fade_stage0_2026-07-30/RESULTS.md
# ^ MUST be empty

# Packet B reuses the canonical sigma and left the pinned dict alone
grep -n "windowed_sigma" lab/analysis/c1/tradeify_fade_stage0_2026-07-30/sigma_native.py | head
git diff --name-only origin/main...HEAD -- lab/analysis/c1/tradeify_fade_stage0_2026-07-30/design_law.py
# ^ MUST be empty

# Withdrawn packet C stayed withdrawn: gated Phase-5 surfaces untouched by the fleet
git diff --name-only origin/main...HEAD -- core/
# ^ MUST be empty

# Fleet-wide: footprint discipline, and no spend
git diff --name-only origin/main...HEAD
grep -rn "db_fetch\|register_search" lab/analysis/c1/tradeify_fade_stage0_2026-07-30/instrument_parity.py lab/analysis/c1/tradeify_fade_stage0_2026-07-30/sigma_native.py || echo "OK: no pull, no K"
```
