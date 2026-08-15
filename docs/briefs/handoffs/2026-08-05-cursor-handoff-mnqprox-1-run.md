# Cursor Handoff — `MNQPROX-1` (level-proximity discriminator) → single run, one §7 branch

**Date:** 2026-08-05
**Parent session:** Claude Code (Sonnet 5) + Joshua
**Spawn target:** Cursor (execution lane — CC/Cursor surface-allocation ADR 2026-07-14: CC specifies, Cursor implements the frozen spec)
**Repo:** `multi_firm_operations`
**Brief type:** CC/Cursor handoff (single build)
**Parent pre-reg:** [`lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md`](../../../lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md) — **FROZEN, three amendments landed, OPERATOR GO GRANTED**, committed through `64bd8a4` on `analysis/mnqprox-1-level-proximity-prereg`.
**Authority:** Joshua (operator), in session: *"I am giving it the GO."* GO covers the construct **including** the S4c/W6 time-of-day guard and the S4 implementation-precision pin (both landed before the GO). Cursor executes the frozen spec **exactly as amended** — no threshold, window, construct, or definition change; the amendment log is the single source of truth for what "frozen" means here, not just §§1–9 in isolation.

---

## §0 — Phase-0 reads (execute BEFORE any §2 work; post a read-report first)

Cursor: read each file and report back what it says before running anything. Do **not** build or pull until this read-report is posted and any §0.5 ambiguity is resolved. Verification anchors are `git log -1` (hash + commit-date) at authoring; re-confirm each resolves before relying on it.

- **`lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md`** (`64bd8a4` 2026-08-05) — the frozen spec, **read the whole file including the Amendment log** (the log carries three load-bearing amendments not in §§1–9: S4c/W6 time-of-day guard, the operator GO scope, and the S4 implementation-precision pin — S2 PDH/PDL session boundary, bar-mid definition, first-bar exclusion). Report back: §2 (S1–S7 as written), §7 (gate table, now six rows W6→W1), and all three Amendment-log entries dated 2026-08-05.
- **`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/flow_lib.py`** (in `f06e9db`, now on `main`) — the parent's pure-function statistic core. Report: `asym`/`signed_asym`/`window_mean_A`, `assemble_sessions` (and **why** it filters on finiteness, not `is not None` — the None→NaN coercion trap), `_pad`/`_stat_from_choice`, `session_block_bootstrap`, `within_session_placebo`, `verdict`. **You are adapting this file's shape for a paired two-arm (ORB vs level) statistic, not the single-arm (trigger vs control) statistic it currently computes** — see §2.3 for exactly what differs.
- **`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/build_events.py`** (in `f06e9db`) — the parent's S2/S4 event construction. Report: `trade_days` (day-inclusion predicate replay), `localize_touch` (first 1m bar crossing OR hi/lo, touch = that bar's **open**), the FM-1 outcome-column ban assertion. **You will reuse this file's `events.parquet` output for the ORB arm verbatim — do not recompute it via a fresh engine call** (PREREG S2: "Reuse parent `events` where byte-identical; do not re-cut"). ⚠ **`events.parquet` and `quotes.parquet` are gitignored** (`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/.gitignore` — vendor-derived, redistribution-restricted) — check whether they exist on disk in your actual execution environment **before** assuming reuse is free. See the next bullet for what to do if they're absent.
- **`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/pull_windows.py`** (in `f06e9db`) — the parent's windowed TBBO transport (checkpointed, `event_id`-keyed, atomic write, hard S1-boundary guard). Report: `_assert_inside_s1`, the checkpoint/resume logic, the "zero-quote window → null row, never silently dropped" discipline. **Reuse policy for the ORB arm, precisely:** if `events.parquet`/`quotes.parquet` already exist on disk in your environment, reuse them byte-for-byte (do not touch). **If either is absent** (likely — they're gitignored, so a fresh Cursor checkout/worktree will not have them), rebuild `events.parquet` for `$0.00` via `build_events.py` unmodified (deterministic from the free 1m panel — this is a *rebuild*, not a re-cut, per the file's own `.gitignore` comment: "rebuildable from the free on-disk 1m panel"), and rebuild `quotes.parquet` via `pull_windows.py` unmodified. **This is not a forbidden re-pull** — it reproduces the identical, already-authorized, already-`$0.0000`-estimated S1 request; the forbidden move (§5) is pulling anything *beyond* that window or re-estimating a wider one, not reproducing the same bytes in an environment that doesn't already have them cached.
- **`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/test_flow_lib.py`** (in `f06e9db`) — the parent's 27-test suite (hand-computed statistic checks, ragged-session handling, bootstrap/placebo determinism, verdict precedence). Report: the test list (names only is fine) and confirm the hand-computed arithmetic pattern used in `test_asym_hand_computed`/`test_observed_stat_hand_computed`/`test_placebo_j_zero_reproduces_observed` — your new tests for the paired statistic and for S4c/W6 must follow the same hand-computed-not-tautological pattern.
- **`lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py`** L1–320ish — Report: `Instrument`, `session_panel`, `orb_backtest` signatures (already used unmodified by `build_events.py`; you call `session_panel`/`orb_backtest` the same way for the PDH/PDL panel — no reimplementation).
- **`ops/instruments/MNQ.md`** F2 GUARD + N14 — Report: the guard text and N14's exact numbers (you will add **N15** on completion; N14's numbers must not be touched).
- **`.claude/skills/databento-data/SKILL.md`** (or `db_fetch --help`) — Report: the mandatory cost dry-run before every pull. **This run needs zero new `estimate`/`pull` gate beyond what §4 of the PREREG already reproduced** ($0.0000 for the full S1 window) — the level-touch pull is a strict subset of that same window, exactly as the parent's `pull_windows.py` comment reasons for the trigger pull.

After Phase 0: post the read-report and **stop**. Proceed to §2 only after posting.

---

## §0.5 — HALT-on-ambiguity

Ask (set `Status: NEEDS_CONTEXT`) rather than guess if any of these are unclear after Phase 0:

- **`events.parquet` schema drift:** whether reused-from-disk or rebuilt via `build_events.py`, if it does not carry `trigger_id`, `date`, `side`, `entry_tod_15m`, `ts_et`, `tod_min` as documented, ASK — do not hand-patch the schema or reconstruct it a different way (that would risk silent drift from the panel-refresh-ratified window).
- **`quotes.parquet` reuse vs. rebuild:** if present on disk but cannot be joined back to `events.parquet` by `event_id` (e.g., a prior partial checkpoint), rebuilding via `pull_windows.py` unmodified is the documented recovery path (previous bullet) — this is fine and not a forbidden re-pull. ASK only if `pull_windows.py` itself needs modification to complete the rebuild, or if the rebuilt file's coverage doesn't reproduce the parent's reported 100% (255/255) — that would indicate an environment or panel discrepancy, not a simple missing-cache situation.
- **Prior-session gap (`prev_session` undefined):** the panel's first calendar day has no prior session (S4a exclusion iii already covers this — drop, don't error). If ANY session in the paired-session-eligible set (has ≥1 ORB trigger) lacks a resolvable `prev_session` for a reason other than being the panel's first day, ASK.
- **Degraded days:** the parent's four Databento `degraded`-flagged sessions (2025-09-24, 2025-11-28, 2026-03-16, 2026-04-10) are retained, not dropped (PREREG limitation 2 analog, FM-4/FM-6). If your level-touch pull surfaces additional degraded-flag sessions beyond those four, retain and disclose them the same way — do not drop and do not silently ask; log in `PULL_LOG.md` and proceed.

---

## §1 — Context

`MNQFLOW-1` (parent, `RESOLVED` W1) found ORB-MNQ-1's own trigger boundary carries an L1 book-asymmetry signature, but its own largest caveat (limitation 1) is that the parent's controls only matched time-of-day, not level-type — so the signature might be generic approached-level microstructure, not anything ORB-specific. `MNQPROX-1` is the gated re-proposal the parent itself named to resolve that caveat, contrasting the ORB arm against non-ORB approached levels (prior-day high/low first touches) in the same sessions.

Pre-GO review (this session) found the originally-drafted S4 lacked a time-of-day match between the two arms — reintroducing the exact confound the parent's own design controlled for — and closed it via amendment (S4c disclosure + W6 gate). A second review pass found S4's prose under-specified three implementation choices; those are now pinned in the amendment log too. **The PREREG you are building against is the frozen §§1–9 text PLUS all three 2026-08-05 amendment-log entries — treat the amendment log as load-bearing, not a changelog to skim.**

**What Cursor produces:**
- Level-touch (PDH/PDL) event construction, reusing the ORB arm from parent's `events.parquet`/`quotes.parquet` verbatim.
- A paired two-arm statistic module (S5/S6/S7/S4c/W6) adapted from `flow_lib.py`.
- A single authorized TBBO pull for the level-touch windows only (subset of S1; $0.0000).
- Hand-computed unit tests covering the new construction, statistic, and gate logic (S4/S4a/S4c/W6 predicates) — must pass before the runner reads a real quote (§9 step 3).
- One run. `RESULTS.md` discharging exactly one §7 branch (now six rows, W6 highest precedence).
- Board writes: `STATE.md`, `ops/instruments/MNQ.md` (new **N15**), `docs/SESSIONS.md`, `lab/CATALOG.md`, PREREG amendment log pointer (all mirroring the parent's own board-write shape in `f06e9db`).

**What Cursor is NOT asked to do:** any MBP-10 pull (FM-4/§5); any second cell, alternate level class, τ sweep, or second instrument (FM-4); any conversion of a result into a gate or filter (§6 — a fresh K-bound axis, out of scope entirely); touch `core/`, allocations, `dd_protection`, lifecycle, Pine, or the rail.

---

## §2 — Execution plan (gated; stop at the §7 verdict)

### Step 2.1 — Level-touch (PDH/PDL) event construction

- **Inputs:** the same free 1m OHLCV panel `build_events.py` loads (`CACHE_1M`, S1 window `2025-08-06`→`2026-08-04`), the parent's `events.parquet` (for the paired-session filter and the S4a(ii) 15-min exclusion), `orb_lib.session_panel`/`orb_backtest` (unmodified).
- **Action:** for each session that has ≥1 ORB trigger (from parent `events.parquet`, `kind=="trigger"`):
  1. PDH = `piv["high"].loc[prev_session].max()`, PDL = `piv["low"].loc[prev_session].min()` — `prev_session` is the immediately preceding entry in the **same session index** `orb_lib.session_panel` produces (amendment-log pin). Skip (S4a-iii) if no prior session exists.
  2. Scan that session's 1m bars **starting at the second bar** (amendment-log pin: first bar never eligible). Bar mid = `(bar_high + bar_low) / 2` (amendment-log pin, free-panel bars, not TBBO). A **first touch** of PDH (or PDL) is the first bar where `abs(mid - level) <= 0.25` (1 tick) **and** the immediately preceding intra-session bar had `abs(mid - level) > 0.25`. Touch timestamp = that bar's **open** (ET) — same convention as the ORB trigger touch.
  3. Approach side: PDH touch → `long`; PDL touch → `short` (S2/S3 signing convention — mirrors parent, do not invent a new sign rule).
  4. Apply S4a exclusions **in order**: (i) drop if `abs(level - session_OR_high) <= 4*0.25` or `abs(level - session_OR_low) <= 4*0.25` (ORB/near-ORB coincidence — 4 ticks = 1.0 pt); (ii) drop if the touch is within 15 min of that session's own ORB trigger timestamp (reuse the trigger's `ts_et` from parent `events.parquet`); (iii) already handled in step 1 (no prior session); (iv) drop if the retained touch's `[t-60s, t)` window later turns out to carry zero usable TBBO quotes (this is a post-pull filter, applied after Step 2.3 — do not pre-filter on an assumption).
  5. A session may retain PDH and/or PDL touches, or neither, after exclusions. Emit one row per retained touch: `trigger_id` (borrow parent's session-linked id so pairing is unambiguous), `date`, `level_kind` (`PDH`/`PDL`), `side`, `ts_et`, `tod_min`.
- **Output:** `level_events.parquet` in `lab/archive/mnq_orb_level_proximity_2026-08-05/`.
- **Faithfulness assertion (mirrors `build_events.py`'s day-mapping proof):** assert every emitted touch's session appears in parent `events.parquet`'s trigger set (paired-session precondition); assert no touch's `abs(mid-level)` exceeds 0.25 at its own timestamp (sanity on the detector).
- **Per-step gate:** `level_events.parquet` written; coverage counts printed (candidate touches found / retained after each S4a exclusion, matching PREREG S7(b)).

### Step 2.2 — Paired session assembly + S4c disclosure

- **Action:** join parent trigger rows (one per paired session — a session may appear once, since S2 is one trigger per session by construction) with `level_events.parquet` rows on session/date. A session enters the **paired set** only if it has ≥1 ORB trigger **and** ≥1 retained level-touch (S5). Sessions with only one side are counted in the coverage ledger (S7(c)/(d)), not in `Δ`.
- **S4c:** for the paired set, compute `median`/`IQR` of `tod_min` separately for the ORB-trigger rows and the level-touch rows (if a session contributes both a PDH and a PDL touch, both enter the level-arm distribution — do not average them into one).
- **Per-step gate:** paired-session count `n_paired` printed; S4c medians/IQRs printed; **evaluate W6 here, before any TBBO is pulled for the level arm** — if W6 fires (IQRs don't overlap, or `|median diff| > 60` min), **STOP**, do not proceed to Step 2.3, report `VOID-TOD-CONFOUND` with the coverage ledger and S4c numbers only (mirrors the S7 VOID-POWER stop-rule: not re-cut to chase a passing split).

### Step 2.3 — Level-arm TBBO pull (subset of S1; reuse ORB-arm quotes)

- **Action:** adapt `pull_windows.py` for the **retained, paired-set level-touch rows only** (not all candidate touches from Step 2.1 — only those that survived Step 2.2's pairing). Same `[t-60s, t)` window, same `MNQ.v.0`/`continuous`/`tbbo`, same hard `_assert_inside_s1` guard, same checkpoint/resume/atomic-write discipline. **Do not re-pull the ORB arm** — join parent's `quotes.parquet` by the trigger's original `event_id` (or re-derive the mapping from parent `events.parquet` if `event_id` was positional — confirm this in Phase 0, §0.5 if unclear).
- **Now apply S4a(iv):** any level-touch window with zero usable TBBO quotes is dropped from the paired set (log the count; this is the final numerator/denominator for S7).
- **Per-step gate:** `level_quotes.parquet` written; coverage fraction (S7a for ORB arm — should reproduce parent's 100%, S7b for level arm) printed.

### Step 2.4 — Statistic module (adapt `flow_lib.py` for the paired two-arm design)

- **Action:** build `proximity_lib.py` with:
  - `signed_asym`/`window_mean_A`/`asym` — reuse `flow_lib.py`'s functions verbatim (identical S3 feature).
  - A session-row assembler analogous to `assemble_sessions`, but each session's row is `[mean_A_ORB, mean_A_level]` (paired, not trigger-vs-k-controls) — one ORB value and one level value per session (if a session has both PDH and PDL touches, mean them into a single per-session level value **before** row assembly — declare this explicitly in the module docstring since it's a step not literally spelled out in S5's "mean(A_ORB) − mean(A_level)" wording but is the only way to keep one row per session for the block bootstrap).
  - `Δ = mean(A_ORB) − mean(A_level)` — session-block bootstrap 95% CI, seed **20260805b** (not the parent's `20260805` — S5 amendment note), 10,000 reps.
  - Placebo: within-paired-session label permutation (ORB vs level, not trigger vs control), 1,000 reps, same seed, two-sided (`|observed|` vs p95 of `|placebo|`) — mirror `flow_lib.py`'s two-sidedness discipline exactly.
  - `verdict()`: **six-row precedence, W6 → W5 → W4 → W3 → W2 → W1**, per the amended §7 table. W6 is already evaluated in Step 2.2 and short-circuits before this module is even invoked on real TBBO — but `verdict()` should still accept a `tod_confound: bool` argument and re-assert the W6 short-circuit defensively (belt-and-braces; do not rely solely on Step 2.2's control flow).
- **CRITICAL — copy the None→NaN coercion fix.** `flow_lib.py`'s `assemble_sessions` docstring explains why filtering on `is not None` is insufficient (pandas `.map()` coerces `None`→`NaN`, which then survives an `is not None` check and manufactures a difference via `nansum`). Your assembler must filter on `np.isfinite`, not `is not None`, from the start — this is not optional hardening, it is the exact defect the parent caught with a synthetic dry-run before its real run.

### Step 2.5 — Unit tests (before the runner reads a real quote)

- **Action:** `test_proximity_lib.py`, following `test_flow_lib.py`'s hand-computed-not-tautological pattern. Minimum coverage:
  - Touch detector: hand-computed first-touch on a synthetic 5-bar session (confirm first-bar exclusion, confirm the >1-tick→≤1-tick transition trigger, confirm the S4a(i)/(ii) exclusions fire on synthetic near-ORB and near-trigger cases).
  - PDH/PDL session-boundary: confirm `prev_session` resolves to the correct entry in a synthetic 3-session panel, and confirm the panel's first session is excluded.
  - Statistic core: hand-computed `Δ` on a small synthetic paired-session set; bootstrap determinism under seed; placebo `j=0` reproduces the observed statistic (mirrors `test_placebo_j_zero_reproduces_observed`); the None→NaN coercion regression (synthetic session with a `None` window, assert it is dropped not zeroed).
  - S4c/W6: hand-computed median/IQR on a synthetic paired set; W6 fires on a synthetic non-overlapping-IQR case and on a synthetic >60-min-median-gap case; W6 does NOT fire on a synthetic overlapping/close case; verdict precedence test confirms W6 pre-empts W5–W1 even when the other four would resolve differently.
- **Per-step gate:** all new tests green, reported alongside a re-run of the parent's 27 (to confirm nothing in the reused `flow_lib.py`/`events.parquet`/`quotes.parquet` path broke).

### Step 2.6 — The single run

- **Action:** `run_proximity.py`, mirroring `run_flow_substrate.py`'s shape — reads `level_events.parquet` + `level_quotes.parquet` + parent's `events.parquet`/`quotes.parquet`, emits **only** the §2 closed output list (n_paired, coverage ledger, means, `Δ` with CI, placebo p95/p_emp, by-half split, S4c medians/IQRs) plus the W6 disposition. No per-trade table, no win/loss, no MFE/MAE (FM-1/FM-2 — the event sets carry no outcome column by construction; add the same `banned` column assertion `build_events.py` uses).
- **Per-step gate:** exactly one §7 branch discharged. `RESULTS.md` + `RESULTS.json` written (mirror parent's `RESULTS.md` structure: verdict table, headline numbers, "what this does NOT say," limitations, process disclosures, iterate, audit hooks).

### Step 2.7 — Closure artifacts (board writes)

- `ops/instruments/MNQ.md` — new **N15** row (do not edit N14's numbers), mirroring N14's density/disclosure style; if the verdict is `RESOLVED` (W1) or `FALSIFIED` (W3), state the disposition plainly per §7's own language; if `VOID-TOD-CONFOUND` or `VOID-POWER`/`VOID-COVERAGE`, N15 records the void and what would need to change (more sessions, not a re-cut).
- `STATE.md` — one line under the executed-decisions index (not the ≤5-item OPERATOR QUEUE), mirroring the parent's single-line-with-full-numbers style.
- `docs/SESSIONS.md` — top entry.
- `lab/CATALOG.md` — status column update for the `mnq_orb_level_proximity_2026-08-05` row (currently `ACTIVE`/`—`).
- PREREG amendment log — final entry recording the run's completion and pointing to `RESULTS.md` (append-only, do not touch §§1–9 or the prior three amendment entries).

---

## §4 — Falsifiable hypothesis (verbatim from PREREG §1)

**H-MNQPROX-1.** At ORB-MNQ-1's own frozen trigger moments, mean signed L1 asymmetry `A` differs from mean `A` at non-ORB approached levels in the same sessions (prior-day high/low first touches), under the same feature window and inference stack as `MNQFLOW-1`.

- **Accept (ORB-specific):** CI on `Δ` excludes 0 **and** |effect| exceeds the placebo p95.
- **Reject (generic level microstructure):** CI includes 0, **or** effect ≤ placebo p95.
- **New precondition (this session's amendment):** the accept/reject branches are only interpretable if **W6 does not fire** — a confounded time-of-day split voids interpretation entirely, it does not fall back to accept or reject.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Recomputing the ORB arm from the engine instead of reusing `events.parquet`/`quotes.parquet`.** S2 says reuse where byte-identical; a fresh engine call risks silent drift from the panel-refresh-ratified window and burns a redundant TBBO pull.
- **Averaging PDH and PDL touches into the ORB arm's own statistic, or otherwise blending arms.** They are always compared, never pooled.
- **Skipping the W6 check, or computing it AFTER the level-arm TBBO pull.** Step 2.2 evaluates W6 **before** Step 2.3's pull specifically so a confounded design doesn't burn TBBO reads on data that can't be interpreted — moving W6 later defeats that ordering's purpose even though the $ cost is the same either way.
- **"Fixing" a borderline W6 result by adjusting the 60-minute threshold or the touch-detection tick tolerance.** Both are frozen (amendment log, FM-6 extension). A borderline case is `VOID-TOD-CONFOUND`, not a prompt to retune.
- **Treating a `RESOLVED` (W1) verdict as license to build a filter or gate.** §6: any such conversion is a fresh K-bound axis, entirely out of this handoff's scope.
- **Pulling anything outside the S1 window, or widening/re-estimating the window "while you're at it."** The `_assert_inside_s1` guard from `pull_windows.py` must be reused, not weakened. (Rebuilding the ORB arm's `events.parquet`/`quotes.parquet` via the unmodified parent scripts, when those gitignored files are absent from your environment, is expected and not a forbidden move — see §0.)
- **Silent scope creep into `core/` / allocations / `dd_protection` / Pine / the rail.** Log off-pattern observations under `DONE_WITH_CONCERNS`; do not fix.
- **Amending the PREREG's frozen §§1–9 or the existing three amendment entries.** Only append a fourth, closure-only entry (Step 2.7).

---

## §6 — Status return taxonomy

Return EXACTLY one: `DONE` (all of §2 ran; one §7 branch discharged including a `VOID-TOD-CONFOUND` outcome; artifacts + boards written) · `DONE_WITH_CONCERNS` (ran but flags something off-pattern you resolved but want reviewed) · `NEEDS_CONTEXT` (schema drift, unresolvable `prev_session`, or any §0.5 item) · `BLOCKED — <sub-case>`.

**`BLOCKED` sub-cases (mandatory):**
- `BLOCKED — context-problem`: a needed input (parent's `events.parquet`/`quotes.parquet`, orb_lib) is missing/unreadable.
- `BLOCKED — capability-problem`: Databento auth / research-venv / API limit blocks the level-arm pull.
- `BLOCKED — scope-problem`: the construction→pull→statistic→run span is too large for one pass → decompose (e.g., construction+pairing+W6-check first, pull+run second) and report the split.
- `BLOCKED — plan-itself-wrong`: a frozen value in §2 (this handoff) is internally inconsistent with the PREREG's amendment log → escalate to CC; do not proceed on a guess.

**On a `VOID-TOD-CONFOUND` outcome specifically:** return `DONE` (the gate firing is itself a valid, informative, pre-registered outcome, not a failure) with the S4c numbers front and center in the closure report — this is not a case to soften into `DONE_WITH_CONCERNS`.

Closure report format:
```
Status: <...>
Per-step gates: 2.1 [..], 2.2 [..], 2.3 [..], 2.4 [..], 2.5 [..], 2.6 [..], 2.7 [..]
§7 verdict: <W6 VOID-TOD-CONFOUND | W5 VOID-POWER | W4 VOID-COVERAGE | W3 FALSIFIED | W2 AMBIGUOUS-CONFOUND | W1 RESOLVED>
Headline numbers: n_paired=<x>, Δ=<x>, CI=[<x>,<x>], placebo p95=<x>, S4c ORB tod median/IQR=<x>, level tod median/IQR=<x>
Diffs (files touched): <list>
Closure artifacts: level_events.parquet, level_quotes.parquet, proximity_lib.py, test_proximity_lib.py, run_proximity.py, RESULTS.md, RESULTS.json, board updates
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (CC, after Cursor returns)

**Pass 1 — Spec compliance:** `level_events.parquet` built from the free 1m panel only (no TBBO burned on detection); ORB arm is a verbatim join to parent artifacts (diff the trigger rows byte-for-byte against parent `events.parquet`); S4a exclusions applied in the frozen order; W6 evaluated before the level-arm pull (check the commit/log ordering, not just the final artifact).
**Pass 2 — Quality:** re-run `test_proximity_lib.py`; spot-check the touch detector against 2–3 hand-picked sessions in the raw panel; confirm the None→NaN coercion fix is present in the new assembler (grep for `np.isfinite`, not `is not None`); confirm seed `20260805b` (not the parent's `20260805`) is actually used.
**Pass 3 — Consolidated:** the §7 verdict, the N15 board entry, and STATE.md/SESSIONS.md tell a consistent story; if `RESOLVED`/`FALSIFIED`, confirm the disposition language matches §7's frozen "opens nothing"/"any filter use is a fresh K-bound axis" posture — no accidental overclaim.

---

## §10 — Audit hooks (runnable)

```bash
# Amendment log fully present and dated before any Cursor commit
rg -n "S4 TIME-OF-DAY GUARD ADDED|OPERATOR GO GRANTED|S4 IMPLEMENTATION-PRECISION PIN" \
  lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md
# expect: 3 hits, all dated 2026-08-05

# ORB arm reused-or-rebuilt, not recomputed via a fresh engine call (row count matches
# parent exactly either way). If events.parquet is absent (gitignored), rebuild first:
#   .venv-research/Scripts/python.exe lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/build_events.py
python -c "import pandas as pd; \
  p=pd.read_parquet('lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/events.parquet'); \
  print((p['kind']=='trigger').sum())"
# expect: 255

# W6 evaluated before the level-arm pull (commit/log ordering)
git log --oneline -- lab/archive/mnq_orb_level_proximity_2026-08-05/level_quotes.parquet | tail -1
git log --oneline -- lab/archive/mnq_orb_level_proximity_2026-08-05/level_events.parquet | tail -1
# expect: level_events.parquet's first commit predates (or is same-commit-earlier-diff-order
# than) level_quotes.parquet's first commit

# None -> NaN coercion fix present in the new assembler
grep -n "np.isfinite" lab/archive/mnq_orb_level_proximity_2026-08-05/proximity_lib.py
grep -c "is not None" lab/archive/mnq_orb_level_proximity_2026-08-05/proximity_lib.py
# expect: isfinite present; any "is not None" hits are NOT the sole filter condition

# Seed is the amended one, not the parent's
grep -n "20260805b" lab/archive/mnq_orb_level_proximity_2026-08-05/proximity_lib.py

# Full test suite green
.venv-research/Scripts/python.exe -m pytest \
  lab/archive/mnq_orb_level_proximity_2026-08-05/test_proximity_lib.py -q

# Verdict reproduces from the run script
.venv-research/Scripts/python.exe lab/archive/mnq_orb_level_proximity_2026-08-05/run_proximity.py
```

---

## Verification (parent-side, before dispatch)

```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/handoffs/2026-08-05-cursor-handoff-mnqprox-1-run.md --type cc_handoff

# PREREG state this handoff depends on is present
git log --oneline -1 -- lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md
# expect: 64bd8a4 or later, with all three 2026-08-05 amendments intact
```
