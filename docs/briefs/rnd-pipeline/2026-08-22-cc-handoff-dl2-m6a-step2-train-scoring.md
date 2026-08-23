# CC Handoff — DL-2 (M6A × prior-session-breakout-continuation) §6 step 2: train scoring + nomination

**Date:** 2026-08-22
**Parent session:** Claude Code (this session, worktree `deep-lane-candidate-family-3ab825`)
**Spawn target:** Claude Code (Analyst + Tactical Ops) — not Cursor. This is first-of-its-kind
implementation against a genuinely novel frozen spec (new mechanism id, new session-boundary
logic, new roll-day rule); it is not a repeatable frozen-spec build in the sense the CC/Cursor
surface-allocation ADR routes to Cursor, and any halt-on-ambiguity below must reach a human, not
default silently.
**Repo:** `first-passage`, worktree `deep-lane-candidate-family-3ab825` (branch
`claude/deep-lane-candidate-family-3ab825`)
**Brief type:** CC handoff (multi-step)
**Parent artifact:** [DL-2 prereg](../pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md)
(`FROZEN` 2026-08-22, operator GO "GO on freeze") — the deep-lane charter's second campaign
**Authority:** Joshua (operator). This handoff executes §6 step 2 only. No commit/merge, no
confirm-partition read, no charter/prereg edit beyond what §2.4 below specifies, without a
separate operator go-ahead if anything below surfaces as ambiguous.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any §2 work)

CC: read each file below and report contents (or the specified excerpt) in your first response.
Do not write scoring code, do not run anything against the TRAIN cache, until this Phase 0
read-report is posted and any §0.5 ambiguities are resolved.

- [`docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md`](../pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md)
  — **the authoritative spec, read in full.** §1 (family + session definition + roll-day rule),
  §2 (the 10 frozen variants, closed set), §3 (partition, cost pin, scoring conventions, fill
  engine), §6 (the exact gate table you are executing). Report: confirmation you have read every
  section, and paste §2's table + §6's gate row verbatim in your response so drift is
  self-evident if the file changes later.
- [`ops/instruments/MECHANISMS.md`](../../../ops/instruments/MECHANISMS.md) — the
  `prior-session-breakout-continuation` entry (already `NEW`-registered this session; no action
  needed on this file unless a genuine construction question arises that the entry itself should
  answer and doesn't).
- `lab/archive/dl1_mgc_orc_2026-08-16/` — DL-1's own step-2 harness, the one precedent under this
  charter. Read for **structural convention only** (directory layout, how the SPA/Hansen
  bootstrap was actually implemented, how the adverse-first-same-bar fill rule was coded, how
  `train_results.json` was shaped) — DL-1's construct (`opening-range-continuation`, gold) is a
  **different mechanism on a different instrument**; do not port its session-boundary or
  roll-day logic, which do not apply here. Report: the file list and a one-paragraph summary of
  the SPA implementation you found, so §0.5 can flag if this handoff's own SPA pin (below)
  conflicts with it.
- [`lab/databento_fetch/db_fetch.py`](../../../lab/databento_fetch/db_fetch.py) — the pull tool
  already used to cache the two files below; report the reload pattern
  (`databento.DBNStore.from_file(...).to_df()`) and whatever column/schema shape `ohlcv-1m`
  produces.
- `git log -1 -- docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md` —
  report commit hash + date (anchor for this handoff's own closure artifact).

**Cached data (already pulled, $0.0000, this session — do not re-pull):**

| Partition | Cache file | Rows | Window |
|---|---|---:|---|
| TRAIN | `C:\Users\joshu\.databento_cache\ohlcv-1m_parent_628b3020421840e1.dbn` | 3,259,026 | `6A.FUT` parent, 2010-06-06 → 2019-01-01 |
| CONFIRM | `C:\Users\joshu\.databento_cache\ohlcv-1m_parent_01f8f1910c17eb9f.dbn` | 2,110,056 | `M6A.FUT` parent, 2019-01-01 → 2026-08-22 |

**This handoff uses TRAIN only. See §5 — the CONFIRM file's existence on disk is not license to
load, inspect, or score it under this task.**

---

## §0.75 — Local-only dependency check

`N/A — CC runs in the operator's own environment (this worktree), where the cache files and any
credentials are already present.` (Confirmed live this session: both pulls landed in
`C:\Users\joshu\.databento_cache\`, no Databento key needed for a cached reload.)

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY required)

CC: halt and ask rather than default-guessing on any of the following. Post your answers (or
"none found" per category) under `## §0.5 Response — ambiguities` in your first response.

- **Scope/session semantics:** the prereg's §1 Globex session boundary (18:00 ET prior day → 17:00
  ET current day) and the §2 lookback/drift-filter/entry-style/target axes are meant to be
  implemented exactly as written — if any sentence in §1–§3 is genuinely ambiguous about *how* to
  compute something (e.g., the precise tick-buffer direction on a short entry, or how a
  session-close vs session-flat-at-bar-close interacts with the last minute bar), ASK. Do not
  resolve a genuine spec gap by picking the "reasonable" reading silently — the prereg is frozen
  (Trap #12); a silent reasonable-seeming reading that turns out wrong would need a whole new
  campaign to fix, not an edit.
- **Roll-day detection:** §3's frozen stitch rule ("front month = per-UTC-day `ohlcv-1d` volume
  leader, outrights only; a roll day = the day the leader changes") requires an `ohlcv-1d`
  volume-leader signal this handoff has not separately pulled. If the TRAIN `ohlcv-1m` cache
  alone cannot support this (e.g., it's already filtered to one contract, or multiple contracts
  aren't distinguishable in it), STOP and return `NEEDS_CONTEXT` — do not approximate roll days
  by a fixed calendar (IMM dates) without flagging that as a deviation from the frozen rule.
- **SPA/Hansen implementation:** §6 step 2b pins Politis–Romano stationary bootstrap, expected
  block length 20 days, B=10,000, seed=11, benchmark = zero-return series. If DL-1's own
  implementation (read in §0) used a library or hand-rolled routine, confirm which is available
  in this environment before assuming; if neither is trivially available, return
  `NEEDS_CONTEXT` rather than substituting a different multiplicity control.
- **Termination condition:** §6's gate table requires **all four** of 2a–2d to independently
  compute and be reported, even once one has already failed (DL-1's own closure reported all
  three gates it touched, including the one that passed, gate 2c) — do not short-circuit on the
  first failure.

---

## §1 — Context

DL-2 is the second campaign under the deep-iteration lane charter. Its prereg is `FROZEN`; the
two $0 TRAIN/CONFIRM pulls already landed this session. What's missing is the actual scoring
harness: nobody has yet implemented the 10 frozen variants against real TRAIN data, computed the
argmax nominee, or run the four nomination gates. That implementation, its run, and the resulting
verdict (ABANDONMENT, or "clears step 2 — confirm-read GO owed") is this handoff's entire scope.

**Parent artifact:** [DL-2 prereg](../pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md)
§6, row 2 ("Train + nomination").

**What CC is being asked to produce:**
- A scoring harness at `lab/analysis/dl2_m6a_pdhpdl_2026-08-22/` (matches DL-1's actual layout —
  see the §0 note under Step 2.1 below; the charter's own citation of a `deep_lane/` intermediate
  directory is stale) implementing the frozen §1–§3 construct.
- `train_results.json` (or equivalent) — all 10 variants' TRAIN net annSR and trade counts, per
  the prereg's own frozen statistic definition (§3, scoring-convention item 1).
- The nominee (argmax train net annSR) and, on that nominee only, the four gate 2a–2d results
  with the actual numbers (not just pass/fail) — cost-law ratio at realized stop, SPA p-value,
  measured cadence, +1-tick-slip net annSR.
- A closure record for this step: if any gate fails, an **ABANDONMENT** entry (dated) on the DL-2
  prereg's own Change history *and* the charter's running-count line (mirroring how DL-1's own
  abandonment was recorded) — **and explicitly flag that this would be DL-2's own abandonment,
  the 2nd consecutive after DL-1, which trips the charter §4(c) audit-report duty** (report this
  loudly in your closure summary; do not bury it). If all four gates pass, do **not** proceed
  further — report the nominee and gate results and stop; the confirm read is a separate operator
  mark.

**What CC is NOT being asked to do:**
- Read, load, or score the CONFIRM cache file, under any gate outcome.
- Touch the 10-variant table, the session definition, the roll-day rule, the cost pin, or any
  other §1–§3 frozen element — if scoring reveals one of these seems wrong, that's a
  `DONE_WITH_CONCERNS` flag for the operator, never a silent in-flight edit (Trap #12).
- Author Pine, touch `core/`, or take any live-adjacent action — this is TRAIN-only research
  scoring, nothing here is deploy-adjacent.
- Fire a fresh Databento pull — both partitions are already cached.

---

## §2 — Execution plan

### Step 2.1 — Build the harness

- **Inputs:** DL-2 prereg §1–§3 (frozen spec); TRAIN cache (`ohlcv-1m_parent_628b3020421840e1.dbn`);
  DL-1's harness (`lab/archive/dl1_mgc_orc_2026-08-16/`) for structural convention only. **Note,
  verified this session:** DL-1's own harness was built at `lab/analysis/dl1_mgc_orc_2026-08-16/`
  (now pruned to a `CARD.md` stub, full body archived to `lab/archive/dl1_mgc_orc_2026-08-16/`) —
  **no `deep_lane/` intermediate directory exists in DL-1's real path**, despite the charter's own
  running-count line citing one (a stale link there, flagged as separate forward work, not fixed
  in this handoff). Land this campaign's own harness at `lab/analysis/dl2_m6a_pdhpdl_2026-08-22/`
  — matching DL-1's *actual* layout, not the charter's broken citation of it.
- **Action:** implement, as separate testable units: (a) the Globex session-boundary grouping
  (18:00 ET → 17:00 ET), (b) roll-day detection + the skip-back lookback rule (§1), (c) the 10
  variant definitions (§2 — lookback length × drift filter × entry style × target), (d) the fill
  engine (adverse-first same-bar resolution, ±1 tick, §3 scoring-convention item 4), (e) the cost
  pin ($2.60 RT, §3 item 3) and the daily-net-P&L → annSR statistic (§3 item 1, √252, flat days
  as zeros).
- **Expected output:** a harness that, given the TRAIN dataframe, returns a per-variant trade
  list and net annSR.
- **Per-step gate:** unit-test each of (a)–(e) against a small hand-constructed synthetic slice
  before running on the full 3.26M-row TRAIN set (e.g., confirm a known synthetic roll day is
  correctly skipped-back, confirm a known synthetic break-and-hold produces the expected R
  multiple). If any of (a)–(e) cannot be cleanly unit-tested with the available data shape, that
  is a `DONE_WITH_CONCERNS` flag, not a silent best-effort.

### Step 2.2 — Score all 10 variants, determine nominee

- **Inputs:** the Step 2.1 harness; full TRAIN dataframe.
- **Action:** score V1–V10 exactly as tabulated in §2; nominee = argmax train net annSR, full
  stop, no fallback (prereg §6 row 2's own language — a tie is a `NEEDS_CONTEXT` case, not a
  coin-flip).
- **Expected output:** `train_results.json` with all 10 variants' net annSR, trade count, and
  which variant is nominee.
- **Per-step gate:** all 10 variants must actually score (no silent drops); the file must be
  reproducible by re-running the harness.

### Step 2.3 — Nomination gates on the nominee only

- **Inputs:** the nominee's TRAIN trade series.
- **Action:** compute, in order, all four — **do not stop at the first failure**:
  - **2a:** train net annSR > 0 AND cost-law ratio ≥ 4× at the nominee's *realized* median stop
    width (ticks), per §4's pre-arithmetic (≥26.0 ticks at the design point, but use the
    nominee's own realized geometry, not the design-point number).
  - **2b:** SPA (Hansen) consistent p ≤ 0.10 against the full 10-variant universe — pinned
    implementation per §6 (stationary bootstrap, block length 20 days, B=10,000, seed=11).
  - **2c:** nominee's measured TRAIN cadence ≥ 1 trade/week.
  - **2d:** nominee's train net annSR stays > 0 at +1 tick/side additional slip.
- **Expected output:** all four numbers, with pass/fail against each threshold.
- **Per-step gate:** all four computed and reported regardless of outcome.

### Step 2.4 — Verdict + closure

- **If any of 2a–2d fails:** `ABANDONMENT`, dated. Deliverables:
  - A closure summary in your final response. **Verified this session: DL-1 produced no
    `docs/briefs/closures/` entry** — its closure-equivalent record is
    `lab/archive/dl1_mgc_orc_2026-08-16/RESULTS.md` plus the dated Change-history rows on its own
    prereg and on the charter. Mirror that shape (a RESULTS.md-equivalent under this campaign's
    own harness directory + the two Change-history rows below) rather than inventing a
    `docs/briefs/closures/` file DL-1 itself never used.
  - A dated Change-history row appended to the DL-2 prereg itself, mirroring DL-1's own
    abandonment-recording language (nominee, which gates failed with numbers, which passed).
  - An update to the charter's running-count line
    ([`docs/adr/2026-08-16-deep-iteration-lane-charter.md`](../../adr/2026-08-16-deep-iteration-lane-charter.md)):
    campaigns abandoned → 2, consecutive → 2/2, active campaign → none, and — **prominently, this
    is the load-bearing consequence** — a note that the §4(c) audit-report duty has now tripped
    (2 consecutive abandonments) and is owed at the next quarterly programme audit.
  - `lab/CATALOG.md` entry for `dl2_m6a_pdhpdl_2026-08-22` mirroring the DL-1 row's shape.
- **If all four gates pass:** do not read CONFIRM. Report the nominee, all four gate numbers, and
  stop with `Status: DONE` — the closure recommendation in your final response should say
  explicitly: "nominee clears §6 step 2 in full; confirm-partition read is owed as its own,
  separate operator GO, not authorized by this handoff."

---

## §4 — Falsifiable hypothesis

**Parent H, restated verbatim from the DL-2 prereg §4** (not tested by this handoff — H is a
confirm-partition assertion, and confirm is not read here): the train-nominated variant achieves
confirm net annSR ≥ 1.170 (= DSR ≥ 0.95 at K=10 on the 7.6386y confirm) AND both confirm halves
(split 2022-10-27, per-half floor SR > 0) are positive.

**This handoff's own local falsifiable claim (H-step2)**, which determines whether parent H ever
gets tested at all: *the argmax-train-annSR nominee clears all four §6 step-2 nomination gates
(2a cost-law, 2b SPA, 2c cadence, 2d slip-robustness).*

- **Accept-if (verdict: `AMBIGUOUS` — mirrors the prereg's own roster mapping, "ABANDONMENT
  closes AMBIGUOUS"):** all four of 2a–2d pass. Then H-step2 is accepted, parent H is not yet
  tested, and the confirm-read is owed as its own separate operator GO.
- **Reject-if (verdict: `FALSIFIED` at the step-2 level — recorded as `ABANDONMENT`, dated, no
  strike against the lane's own falsification budget, per charter §4(c)):** any one of 2a–2d
  fails. Then parent H is never tested this campaign, and — because this is DL-2's own
  abandonment, the 2nd consecutive after DL-1 — the charter's §4(c) audit-report duty trips.
- **Ambiguous/re-dispatch condition:** an argmax tie on train net annSR, or any §0.5 gap
  (roll-day signal, SPA implementation) that blocks even computing the four gates cleanly. Not a
  verdict — return `NEEDS_CONTEXT` per §6 below.

---

## §5 — Forbidden moves

- **Reading, loading, or computing anything from the CONFIRM cache file.** Named as the single
  most tempting move in this handoff — it's sitting on disk, already pulled, and "just peeking at
  the shape" is exactly the kind of confirm-contamination the prereg's own §5 forbids. Don't.
- **Touching the 10-variant table, session definition, roll-day rule, or cost pin** if scoring
  surfaces something that makes one of them look wrong. Flag it in `DONE_WITH_CONCERNS`; do not
  silently patch and re-run (Trap #12 — the prereg is frozen).
- **Approximating the roll-day rule** with a fixed IMM calendar if the `ohlcv-1d` volume-leader
  signal isn't cleanly derivable from the cached data — return `NEEDS_CONTEXT` instead (see §0.5).
- **Short-circuiting gate 2a–2d** at the first failure. Compute and report all four, every time.
- **Re-deriving the SPA implementation** from scratch if DL-1's own code (read in §0) already
  solves it — reuse the tested routine rather than risk a second, subtly different
  implementation of the same pinned test.
- **Amending §6 mid-execution** if a gate threshold seems off once real numbers are in — that's
  `BLOCKED — plan-itself-wrong`, escalated to the parent session, never a silent threshold change.

---

## §6 — Gate + status return taxonomy

Per §4's own H-step2: all four gates pass → verdict `AMBIGUOUS` (ABANDONMENT does not fire;
parent H untested, confirm-read owed separately); any gate fails → verdict `FALSIFIED` at the
step-2 level, recorded as `ABANDONMENT`. Neither outcome is `RESOLVED` — this handoff never reads
confirm, so parent H cannot resolve here regardless of the step-2 outcome.

Report back with exactly one of:

| Status | Meaning |
|---|---|
| `DONE` | Steps 2.1–2.4 complete; harness unit-tested; all four gates computed; verdict (ABANDONMENT or clears-step-2) recorded per §2.4's deliverables. |
| `DONE_WITH_CONCERNS` | Work completed but something surfaced that the operator should weigh before accepting — e.g., a §1–§3 element that scoring suggests is mis-specified, or a unit-test that couldn't be cleanly constructed. |
| `NEEDS_CONTEXT` | An §0.5 ambiguity, the roll-day/`ohlcv-1d` gap, a SPA-implementation gap, or any other missing input that can be supplied by the operator. |
| `BLOCKED — <sub-case>` | Structural obstruction — see the four sub-cases in the brief-authoring skill's own taxonomy (context / capability / scope / plan-itself-wrong). |

**Closure report format:**
```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Per-step gates: 2.1 [pass/concern], 2.2 [pass/concern], 2.3 [all four numbers], 2.4 [verdict]
Diffs (files touched): <list — expect: lab/analysis/dl2_m6a_pdhpdl_2026-08-22/**, and
  if ABANDONMENT: the DL-2 prereg, the charter, lab/CATALOG.md>
Nominee: <variant #, definition>
Gate 2a–2d: <all four, numbers + pass/fail>
Verdict: <ABANDONMENT (dated) | clears step 2 — confirm-read GO owed>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (after this handoff returns)

**Pass 1 — Spec-compliance.** Did the harness implement exactly §1–§3 as frozen — nothing
re-interpreted, nothing added (no FOMC exclusion, no extra axis, no widened variant set)?
**Pass 2 — Quality.** Do the reported gate numbers actually reproduce by re-running the harness?
Does the SPA p-value use the pinned seed/block-length/B? Is the cost-law check using the
nominee's *realized* stop, not the design-point number?
**Pass 3 (multi-step).** Read the full diff together — does the charter update, the prereg
Change-history row, and the `CATALOG.md` entry (if ABANDONMENT) tell a mutually consistent story?

---

## §10 — Audit hooks (runnable)

```bash
# Confirm the harness directory landed where expected
ls lab/analysis/dl2_m6a_pdhpdl_2026-08-22/

# Re-run the closure assertion (path depends on what Step 2.1 actually names the entry script)
python lab/analysis/dl2_m6a_pdhpdl_2026-08-22/run_train_scoring.py --reproduce

# Confirm CONFIRM was never touched
grep -rl "01f8f1910c17eb9f" lab/analysis/dl2_m6a_pdhpdl_2026-08-22/ 2>/dev/null || echo "clean — confirm cache never referenced"

# If ABANDONMENT: charter + prereg + CATALOG all updated together
git diff --name-only | grep -E "deep-iteration-lane-charter|dl2-m6a-pdhpdl-prereg|CATALOG.md"
```

---

## Verification (parent-side, before declaring this handoff complete)

```bash
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/rnd-pipeline/2026-08-22-cc-handoff-dl2-m6a-step2-train-scoring.md --type cc_handoff
# Expected: all 6 general checks + checks 7-10 PASS

grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cc-return-path>
```

If the spawned session returns `NEEDS_CONTEXT` or `BLOCKED`, this handoff is not complete —
supply the missing context and re-dispatch per the returned sub-case.
