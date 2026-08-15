# Cursor Handoff — Q-SFRISK-1 F4 instrument: median days-to-first-skim MC metric (Design C)

**Date:** 2026-07-14
**Parent session:** Claude Code operator session (Joshua + Claude) — the session that froze the Q-SFRISK-1 Phase-0 numeric amendment (`9b219ab`, single triple **T1**: F1 max-DD ≤10%/half + F3 ADOPT decompound withdrawal model + F4 impracticality >252 bd; F2 TUW deferred). **Cursor builds the F4 instrument add** — a self-contained `lab/` metric that computes median business-days-to-first-$210K-skim across MC-resampled paths of the banded decompounded streams — which has zero code today (the pre-reg's own §note flags it as the one outstanding producing-code obligation before Phase 1 can score F4).
**Spawn target:** Cursor (frozen-spec implementation — `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`; this handoff uses the §0.5 Cursor variant). Deps are stdlib + `numpy`/`pandas`, already on the instrument path — no new deps.
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step)
**Parent question:** Q-SFRISK-1 (successor self-funded risk framework) — the F4 impracticality bar frozen in [`docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md`](../pre-registration/Q-SFRISK-1-verdict-preregistration.md) (`9b219ab`, `NUMERIC FROZEN`): *median business-days-to-first-$210K-skim > 252 bd ⇒ IMPRACTICAL*. This handoff builds the **metric** that measures days-to-first-skim; it does **not** apply the >252 comparison, run the real panel, or fire the Q-SFRISK-1 verdict.
**Authority:** Joshua (CEO). No commit/merge without Joshua's go. **Named locked surfaces Cursor must NOT touch:** `core/mc/simulation.py`, `core/mc/ingest.py`, `core/portfolio_mc.py`, `core/dd_protection.py`, `core/firm_rules.py`, or **any** `core/*` file (`build_week_blocks` is imported **read-only** via the `portfolio_mc` facade); the frozen F4 definition in the Q-SFRISK-1 pre-registration; the `decompound.py` `WITHDRAW_AT` / `ACCOUNT` constants and the T1 withdrawal model (F3 = ADOPT +5%/$200K banded); Pine; the locked MC anchor.

> **Build-ahead-of-verdict (read first).** This build produces the **measuring instrument** for F4, not the F4 result. The Q-SFRISK-1 pre-reg is `NUMERIC FROZEN` and Phase 1 (running the decompound instrument against T1 and firing the §6 verdict) is a **separate, not-yet-taken** step reserved to CC/operator (Q-SFRISK-1 §6 is a go-live-gating adjudication; ADR `2026-07-14-cc-cursor-surface-allocation.md`). Cursor builds + unit-tests the days-to-first-skim computation entirely on **synthetic / hand-constructed deterministic fixtures with a known first-skim day**. Do **not** run it against the real locked-book panel for a verdict, and do **not** compare any median to 252 bd as a pass/fail — the metric **reports** the median; the operator/CC apply the comparison later. This mirrors how the decompound instrument itself was built (research `lab/`, never touching `core/` or the anchor).

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any code)

Cursor: read each item and post a read-report in your first response **before** writing a single line of code. If repo state contradicts a §1/§2 assumption or the pre-reg, return `NEEDS_CONTEXT` with the discrepancy quoted — do **not** resolve it unilaterally (ADR `2026-07-14-cc-cursor-surface-allocation.md` §2 test 2).

- [`docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md`](../pre-registration/Q-SFRISK-1-verdict-preregistration.md) (`9b219ab`) — report the **Status** line (must read `NUMERIC FROZEN`), the **Field 4** block (`VALUE: median business-days-to-first-$210K-skim > 252 bd ⇒ IMPRACTICAL`; metric chosen = `median days-to-first-skim`) and its ⚠ open-instrument-obligation note ("days-to-first-skim is not emitted by `decompound.py`/`remc.py` today — a small add to the banded-equity path … Must land **before** Phase 1 can score F4"), and the **T1 grid row** (3-dimension: F1 + F3 + F4, F2 deferred). **This file freezes what the metric must implement; the metric transcribes no new number and redefines nothing.**
- [`lab/analysis/regime/decompound_remc_2026-06-07/decompound.py`](../../../lab/analysis/regime/decompound_remc_2026-06-07/decompound.py) (`6af6ae1`) — report the constants `ACCOUNT = 200_000.0` and `WITHDRAW_AT = 210_000.0` (the +5% skim threshold), the `ALLOC` dict + `FIXED_1R = {s: a * ACCOUNT}`, the **`rebank(trades, mode="banded")`** body (the sequential skim loop: `eq = ACCOUNT`; per trade `p = r * eq`; `eq += p`; `if eq >= WITHDRAW_AT: eq = ACCOUNT`) and its return shape `DataFrame[exit_date, pnl]`, and **`banded_reset_count(trades)`** (the existing reset-counting reference — same walk, counting resets instead of dating the first). Report also `stitch(strategy)` (per-strategy roe frame the banded logic consumes). **These constants and the banded reset semantics are the metric's source of truth — imported read-only, never re-typed, never edited.**
- [`lab/analysis/regime/decompound_remc_2026-06-07/remc.py`](../../../lab/analysis/regime/decompound_remc_2026-06-07/remc.py) (`6af6ae1`) — report `build_streams()` (returns `{mode: {strat: DataFrame[exit_date, pnl]}}` for compounded/static/banded), `_window(tbs, cutoff)`, and how the banded streams feed `D.run_mc(...)` (the `B_2020` HEADLINE cell). **The metric consumes the `"banded"` sub-dict of `build_streams()` — the same banded streams the HEADLINE MC uses.**
- [`lab/analysis/regime/decompound_remc_2026-06-07/regime_gate.py`](../../../lab/analysis/regime/decompound_remc_2026-06-07/regime_gate.py) (`6af6ae1`) — report `BOOT_SEED = 20260607`, `BLOCK_SIZE = 126`, the `build_week_blocks(panel)` usage inside `run_panel`, the **half-panel split** (`mid = panel.index[len(panel) // 2]`; `h1 = panel[index < mid]`, `h2 = panel[index >= mid]`) run through the SAME block machinery per half, and the median sentinel idiom (`median = int(np.median(all_days)) if all_days else 9999`). **The days-to-first-skim metric must be computable per regime half using this exact H1/H2 split, and its seed/bootstrap convention should mirror `BOOT_SEED` / block-bootstrap here (see §0.5(A),(E)).**
- [`core/mc/ingest.py`](../../../core/mc/ingest.py) (`e9be4ec`) — report the **`build_week_blocks(panel: pd.DataFrame) -> np.ndarray`** signature + body (Mon-anchored, non-overlapping, five-business-day blocks: `for index, day in enumerate(panel.index): if day.weekday()==0 and index+5<=len(panel): blocks.append(values[index:index+5])`) and `build_daily_panel(...)` (how the banded per-strategy streams become one portfolio daily-P&L panel with `fixed_1r_reference`). **`build_week_blocks` and `build_daily_panel` are imported READ-ONLY via the `portfolio_mc` facade (they are re-exported there — verified by the parent). Cursor imports them; it does NOT edit `core/mc/ingest.py` or copy their bodies into `lab/`.**
- [`docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md`](../Q-SFRISK-1-successor-self-funded-risk-framework.md) — report **§7 step 3** (Phase 1: "run instrument against the frozen triple(s) only" — the F4 instrument add is the stated prerequisite carried into Phase 1) and **§5 forbidden moves** (esp. "Running decompound / successor MC before that Phase-0 numeric amendment is committed" and "Inventing numeric max-DD / TUW / withdrawal thresholds"). **Confirms: build the instrument now; the Phase-1 real run is out of scope.**
- `git log -1 --format='%h %ci' -- lab/analysis/regime/decompound_remc_2026-06-07/decompound.py` (expect `6af6ae1`, 2026-06-07) and the same for `core/mc/ingest.py` (expect `e9be4ec`, 2026-07-11) and the pre-reg (expect `9b219ab`, 2026-07-14) — report all three as your build anchors.
- `scripts/check_boundaries.py` — report the import contract (`lab → {core, governance, lab}` read-only; `lab ↔ ops` isolation). **This metric lives in `lab/`, imports `core/` read-only via the facade, never touches `ops/`.**

After Phase 0: post the read-report; proceed to §2 only once §0.5 is resolved.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Parent-recommended defaults are stated; **confirm or challenge each in the Phase-0 response.** Set `Status: NEEDS_CONTEXT` until resolved. If any Phase-0 read contradicts a default, bounce `NEEDS_CONTEXT` with the conflict quoted rather than resolving it.

- **(A) Where does the skim walk happen — parallel to the core sim, not inside it?** `core/mc/simulation.py`'s path simulator computes `equity`/`peak` internally but **returns only** `outcome / day / max_dd / culprit` per path — it **exposes no equity-path or skim concept in its outputs**, and Cursor may not edit it (§5). So days-to-first-skim cannot be extracted from the existing MC outputs; it must be computed by a **self-contained resampler in `lab/`** that (i) reuses `build_week_blocks` (read-only) to cut the banded portfolio daily panel into Mon-anchored 5-bday blocks, (ii) resamples those blocks into MC paths under a fixed seed, and (iii) walks cumulative equity from `ACCOUNT` per path to date the first `>= WITHDRAW_AT` crossing. **Recommended default:** build exactly this parallel walk — reuse `build_week_blocks` + `build_daily_panel` (facade, read-only) + the `decompound.py` banded constants, and do the block-resample + equity-walk in the new `lab/` module. Do NOT attempt to thread a skim tracker into `core/mc/simulation.py`. Confirm this matches what Phase 0 revealed about `simulation.py`'s tracked fields, or propose the correct locus.
- **(B) Censoring: how are paths that never skim within the path counted?** A resampled path may run its full length without cumulative equity reaching $210K. Dropping such paths (as `regime_gate.py`'s `if all_days else 9999` idiom drops non-passers) would bias the median **downward** (survivorship) and make an impractical book read fast — the exact failure F4 exists to catch. **Recommended default:** a non-skimming path contributes a **right-censored** value equal to `path_length_bd + 1` (i.e. "> the observed horizon"), so it counts as *slower than any skim* in the median rather than being dropped. Report the censoring rate (fraction of paths that never skimmed) alongside the median. Confirm, or specify an alternative censoring convention (e.g. explicit `np.inf` + a documented median rule).
- **(C) Per regime half, pooled, or both?** T1 requires **both regime halves to clear** (H-SFRISK-1), and F1 is frozen "per regime half." F4's VALUE line states the bar without an explicit per-half qualifier. **Recommended default:** the metric **reports the median (and censoring rate) for H1, H2, AND the full pooled panel**, using the exact `regime_gate.py` split (`mid = panel.index[len(panel)//2]`), and does **not** itself apply the >252 comparison or decide which of the three the verdict keys on — that selection is the operator/CC Phase-1 act. Confirm reporting all three; flag if the pre-reg implies the metric should emit a single per-half verdict.
- **(D) Path length / horizon for the walk.** The censoring rate depends entirely on how long each resampled path runs. **Recommended default:** set each MC path's length to the **business-day length of the panel being resampled** (H1 paths ~ len(H1), H2 ~ len(H2), pooled ~ len(panel)) — i.e. resample enough whole 5-bday blocks to reach ≥ that many bdays, then truncate — and report the exact horizon used per partition. This keeps the horizon a stated, reproducible property rather than a buried magic number, and avoids importing the core sim's pass/bust/`horizon_cap` termination (which the skim metric does not use). Confirm, or state a fixed horizon (e.g. 252 bd, matching the F4 bar) if you prefer the walk bounded at the impracticality line.
- **(E) Seed / resample convention.** **Recommended default:** mirror `regime_gate.py` — a single `numpy` `default_rng(BOOT_SEED)` (`BOOT_SEED = 20260607`) driving block draws, with the path count exposed as a CLI/kwarg (default a smoke-friendly value, e.g. 1000, overridable to the instrument's `SIMS_PER_SEED × len(SEEDS)` scale). Report the exact seed + path count in the output artifact so a run is byte-reproducible. Confirm, or propose reusing the instrument's `SEEDS`/`SIMS_PER_SEED` directly.
- **(F) Output artifact shape.** **Recommended default:** the module exposes a pure function returning a dict `{partition: {median_days_to_first_skim, censoring_rate, n_paths, horizon_bd, seed}}` for `partition ∈ {H1, H2, pooled}`, plus a `__main__` self-check that prints a table (mirroring `decompound.py`'s `__main__` self-check style) — **no** JSON verdict, **no** `> 252` boolean, **no** write to any canonical path. Confirm or propose an alternative shape.

---

## §1 — Context

Q-SFRISK-1's Phase-0 numeric freeze (`9b219ab`) locked triple **T1** with an F4 impracticality bar — *median business-days-to-first-$210K-skim > 252 bd ⇒ IMPRACTICAL* — but the pre-reg's Field 4 note records that **days-to-first-skim is not emitted by the decompound instrument today**, and explicitly carries that producing-code obligation into whoever authors the Phase-1 handoff. The decompound instrument tracks reset **counts** (`banded_reset_count`) and MC path **outcomes** (pass/bust/max_dd), but nothing dates the **first** skim across MC-resampled paths. This build closes that gap so Phase 1 (an operator/CC act) can score F4 — it is the F4 analogue of the already-existing F1 metric (`p99_dd`, emitted by `run_mc` today).

**What Cursor is asked to produce:**
- `lab/analysis/regime/decompound_remc_2026-06-07/days_to_first_skim.py` — a self-contained metric module that: imports `decompound as D` (for `ACCOUNT`, `WITHDRAW_AT`, `ALLOC`, `FIXED_1R`, `stitch`, `rebank`) and `build_week_blocks` + `build_daily_panel` **read-only** via the `portfolio_mc` facade; builds the banded portfolio daily panel; block-resamples it under `BOOT_SEED`; walks cumulative equity from `ACCOUNT` per path to date the first `>= WITHDRAW_AT` crossing (with censoring per §0.5(B)); and returns median days-to-first-skim + censoring rate **per regime half and pooled** (§0.5(C)). A `__main__` self-check prints the table (§0.5(F)).
- `lab/analysis/regime/decompound_remc_2026-06-07/test_days_to_first_skim.py` — synthetic-fixture unit tests. These must run **without vendor data** (unlike the `requires_inputs`-gated tests in the co-located `test_decompound.py`): construct deterministic daily-P&L streams with a **hand-computed known first-skim day** and assert the walk returns it exactly; a stream that never reaches $210K asserts the censoring sentinel; a per-half fixture asserts H1/H2 are measured independently.

**What Cursor is NOT asked to do:** run the metric against the real locked-book panel or the vendor CSVs for a verdict; compare any median to 252 bd or emit a pass/fail/IMPRACTICAL boolean; run `remc.py`/decompound MC for headline numbers; fire the Q-SFRISK-1 §6 verdict or touch its pre-registration; edit `core/mc/simulation.py`, `core/mc/ingest.py`, `core/portfolio_mc.py`, or any `core/*` file; change `decompound.py`'s `WITHDRAW_AT`/`ACCOUNT`/`ALLOC` or the banded model; touch Pine, `ops/`, or the MC anchor.

---

## §2 — Execution plan

TDD throughout; every step's tests run offline on synthetic fixtures (no vendor CSV, no real panel).

### Step 2.1 — Constant + primitive import surface (no re-typing)
- **Inputs:** `decompound.py` (`ACCOUNT`, `WITHDRAW_AT`, `ALLOC`, `FIXED_1R`, `stitch`, `rebank`); `portfolio_mc` facade (`build_week_blocks`, `build_daily_panel`).
- **Action:** in `days_to_first_skim.py`, import `decompound as D` and pull `build_week_blocks` / `build_daily_panel` from the facade (mirror `decompound.py`'s own `_CORE` sys.path insert + `from portfolio_mc import …` idiom). Reference `D.WITHDRAW_AT` / `D.ACCOUNT` — do **not** define local `210_000` / `200_000` literals.
- **Expected output:** module skeleton + an import test asserting `days_to_first_skim` reads `D.WITHDRAW_AT == 210_000.0` and `D.ACCOUNT == 200_000.0` from `decompound`, not local constants.
- **Per-step gate:** grep the module — zero `210_000` / `200_000` / `210000` / `200000` literal anywhere outside a comment; all reference `D.*`.

### Step 2.2 — Single-path equity walk (`days_to_first_skim_on_path`)
- **Inputs:** §0.5(B) censoring resolution; the `banded_reset_count` walk as the semantic reference (same loop, dating the first reset instead of counting all).
- **Action:** a pure function `days_to_first_skim_on_path(daily_pnl: np.ndarray, account=D.ACCOUNT, withdraw_at=D.WITHDRAW_AT) -> float` that walks `eq = account`; for business day `i`, `eq += daily_pnl[i]`; returns `i+1` (1-based business-day count) at the first `eq >= withdraw_at`; returns the §0.5(B) censoring sentinel (`len(daily_pnl)+1`) if never crossed.
- **Expected output:** function + tests on **hand-constructed** arrays: a stream that crosses $210K on exactly business day 7 returns `7.0`; a stream summing to < $10K over its length returns the sentinel; a stream that crosses on day 1 returns `1.0`.
- **Per-step gate:** the known-first-skim-day fixture asserts the exact integer; the never-skims fixture asserts the sentinel (not a dropped/NaN value).

### Step 2.3 — Banded portfolio panel builder (reuse, don't fork)
- **Inputs:** `D.stitch`, `D.rebank(..., "banded")`, `build_daily_panel` (facade), `D.FIXED_1R`.
- **Action:** a function that builds the banded per-strategy streams (`{s: D.rebank(D.stitch(s), "banded")}`) and aggregates to one portfolio daily-P&L panel via `build_daily_panel(streams, D.ALLOC, fixed_1r_reference=D.FIXED_1R)` — identical construction to the `B_2020` HEADLINE cell in `remc.py`. **This step is `requires_inputs`-gated** (needs vendor CSVs) and is exercised only in the `__main__` self-check, not the unit tests.
- **Expected output:** builder function; a `requires_inputs`-skipped test asserting the panel is a `DataFrame` with the four `ALLOC` columns.
- **Per-step gate:** no reimplementation of `build_daily_panel` or `rebank` in `lab/` — both are called; `scale_info` scales are ~1.000 (fixed-1R decompounded cell, per `remc.py`'s own sanity note).

### Step 2.4 — Block-resample + per-partition median (`median_days_to_first_skim`)
- **Inputs:** `build_week_blocks` (facade), `BOOT_SEED = 20260607`, §0.5(A),(C),(D),(E) resolutions.
- **Action:** for a given panel partition, cut it with `build_week_blocks`, resample whole blocks under `default_rng(BOOT_SEED)` to reach the §0.5(D) horizon, sum each path's per-day portfolio P&L to a 1-D daily array, apply `days_to_first_skim_on_path`, and return `{median_days_to_first_skim, censoring_rate, n_paths, horizon_bd, seed}`. Wrap it to run over `{H1, H2, pooled}` using the exact `regime_gate.py` split (`mid = panel.index[len(panel)//2]`).
- **Expected output:** function + tests on a **synthetic panel** (no vendor data): a hand-built panel whose blocks force a deterministic first-skim distribution returns the expected median and a censoring rate matching the fixture; H1 and H2 built from deliberately different halves return **different** medians (proving per-half independence).
- **Per-step gate:** grep proves `build_week_blocks` is called (not reimplemented); the H1≠H2 fixture test passes; the median uses censored values (a fixture where >half of paths never skim yields a median at the sentinel, not a small number).

### Step 2.5 — `__main__` self-check + closure report
- **Inputs:** all prior steps.
- **Action:** a `__main__` that (behind `requires_inputs` in spirit — degrade gracefully if vendor CSVs absent) builds the real banded panel and prints the `{H1, H2, pooled}` median / censoring table in `decompound.py`'s self-check style. **No** `>252` comparison, **no** verdict boolean, **no** write to any canonical/pre-reg path. Then post the §6 closure report.
- **Expected output:** self-check runs (or cleanly reports "vendor inputs absent" on a fresh clone); full offline `pytest test_days_to_first_skim.py -q` green; `check_boundaries` green.
- **Per-step gate:** e2e synthetic tests green with zero vendor data; no `core/`/`ops/`/Pine/pre-reg diff; the printed output contains a median and a censoring rate but no pass/fail token.

---

## §4 — Falsifiable hypothesis

**N/A — build task, no hypothesis under test.** This handoff builds the F4 **measuring instrument**; the hypothesis it feeds is the parent's, restated here as the gate this metric's output will later be scored against (by the operator/CC, not this build):

**F4 bar (verbatim from the Q-SFRISK-1 pre-reg, `9b219ab`):** the lane is IMPRACTICAL iff `median business-days-to-first-$210K-skim > 252 bd`, evaluated within the T1 triple where **both regime halves must clear** (H-SFRISK-1). This build makes that median **computable**; it does not apply the `> 252` comparison, does not decide per-half-vs-pooled, and asserts **no** verdict.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Threading a skim/equity tracker into `core/mc/simulation.py`.** The natural "just add a `first_skim_day` field to the path sim" — forbidden: `simulation.py` is a named locked surface, tracks only `outcome/day/max_dd/culprit`, and editing it breaks the MC anchor's byte-reproducibility. The skim walk lives entirely in the new `lab/` module (§0.5(A)).
- **Editing `core/mc/ingest.py` or copying `build_week_blocks`/`build_daily_panel` into `lab/`.** Import them read-only via the `portfolio_mc` facade. A local copy silently drifts from the Mon-anchored 5-bday contract.
- **Redefining `WITHDRAW_AT` / `ACCOUNT` or "tuning" the $210K / $200K numbers**, or altering the banded skim-to-base semantics. These are F3 (ADOPT +5%/$200K banded), frozen in T1. Reference `D.WITHDRAW_AT` / `D.ACCOUNT`; never re-type the literals.
- **Applying the `> 252 bd` comparison or emitting an IMPRACTICAL / pass / fail boolean.** The metric reports the median; the F4 verdict comparison is the operator/CC Phase-1 act. Emitting a verdict here pre-empts Q-SFRISK-1 §6 (a go-live-gating adjudication reserved by ADR `2026-07-14`).
- **Running `remc.py` / the decompound MC against the real panel for a headline number**, or quoting any real-panel median. Q-SFRISK-1 §5 forbids running successor MC as part of instrument-building; this build is synthetic-fixture-only. (A `__main__` self-check that *prints* a real-panel table for the operator's later use is fine — but it is not a verdict and Cursor does not act on it.)
- **Dropping non-skimming paths from the median** (the `if all_days else 9999` survivorship trap). Censor them per §0.5(B); a book that rarely skims must read *slow*, not *absent*.
- **Editing the Q-SFRISK-1 pre-registration or its §6 table** to "clarify" F4. If the frozen definition seems ambiguous, bounce `NEEDS_CONTEXT` — do not resolve a spec ambiguity unilaterally (Known Trap #12; ADR §2 test 2).
- **The "while I was in there" refactor** of `decompound.py` / `remc.py` / `regime_gate.py`. Log any observation under `DONE_WITH_CONCERNS`; do not silently fix.
- **Re-deriving §0 facts.** If a §0 anchor (commit hash, constant value, function signature) disagrees with disk, return `NEEDS_CONTEXT` with the discrepancy quoted; do not proceed on the inconsistent value.

---

## §6 — Gate + status return taxonomy

Report EXACTLY one of: `DONE` | `DONE_WITH_CONCERNS` | `NEEDS_CONTEXT` | `BLOCKED — <context-problem | capability-problem | scope-problem | plan-itself-wrong>`.

| Status | Meaning | Parent action |
|---|---|---|
| `DONE` | All §2 steps built + fixture-proven; every per-step gate green; no `core/`/`ops`/Pine/pre-reg diff; no scope creep. | Parent runs §7; recommends accept/merge. |
| `DONE_WITH_CONCERNS` | Built and green, but Cursor flags a correctness/scope/methodology doubt (e.g. a censoring-convention edge case, a horizon sensitivity worth operator review). | Parent reviews concerns; accept or re-dispatch. |
| `NEEDS_CONTEXT` | Cannot proceed without missing input — a §0.5 ambiguity unresolved, a §0 anchor contradicting disk, or the pre-reg's F4 wording under-determining the walk. | Parent supplies context; re-dispatch same plan. |
| `BLOCKED — <sub-case>` | Structural obstruction. `context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong`. | Parent escalates/decomposes/re-spawns. |

A `DONE` here means the days-to-first-skim metric is built and synthetic-fixture-proven. It is **never** a claim that F4 has been scored, that any median crosses or clears 252 bd, or that Q-SFRISK-1 has a verdict — those require the real-panel Phase-1 run, an operator/CC act downstream of this build.

**Closure report format:**
```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Per-step gates: 2.1 [...], 2.2 [...], 2.3 [...], 2.4 [...], 2.5 [...]
Diffs (files touched): <list — expect only the two new lab/ files>
§0.5 resolutions applied: A=<...>, B=<...>, C=<...>, D=<...>, E=<...>, F=<...>
Known-first-skim-day fixture test: <pass/fail — the load-bearing assertion>
Non-skim censoring test: <pass/fail>
H1≠H2 per-half independence test: <pass/fail>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (after Cursor returns)

**Pass 1 — Spec-compliance.** Every Step 2.x output present; diff list contains ONLY the two named `lab/analysis/regime/decompound_remc_2026-06-07/` files; zero `core/`/`ops/`/Pine/pre-reg touch; no new dep. The module emits **no** `>252` comparison and **no** verdict boolean.

**Pass 2 — Quality.** The known-first-skim-day fixture genuinely pins the walk (hand-verify the fixture's arithmetic independently). The censoring test genuinely fails if non-skimming paths were dropped (temporarily switch to drop-and-median, confirm the test would then wrongly change — a "does this test test anything" check). No `210_000`/`200_000` literal outside a `D.*` reference. `build_week_blocks`/`build_daily_panel`/`rebank` are called, not reimplemented.

**Pass 3 — Consolidated read** (multi-step): the H1/H2/pooled reporting flows end-to-end on a synthetic panel; the per-half split matches `regime_gate.py`'s `mid = panel.index[len//2]` exactly; the median at Step 2.4 consumes the censored single-path values from Step 2.2 (no silent NaN-drop between them).

Only after all three passes does the parent recommend Joshua accept/merge.

---

## §10 — Audit hooks (runnable)

```bash
# The metric never hardcodes the skim/base thresholds (expect: no matches outside comments)
grep -nE "21[0]?[_]?000|20[0]?[_]?000" lab/analysis/regime/decompound_remc_2026-06-07/days_to_first_skim.py | grep -v "#"

# The metric emits no verdict / no >252 comparison (expect: no matches)
grep -nE "252|IMPRACTICAL|discharges|verdict" lab/analysis/regime/decompound_remc_2026-06-07/days_to_first_skim.py

# Core primitives are imported, not reimplemented (expect: import lines only, no def)
grep -nE "def (build_week_blocks|build_daily_panel|rebank)\b" lab/analysis/regime/decompound_remc_2026-06-07/days_to_first_skim.py   # expect: empty

# No core/ / ops / Pine / pre-reg edit (expect: only the two new lab/ files)
git diff --stat <pre-spawn-commit> -- core/ ops/ '**/*.pine' docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md   # expect: empty

# Synthetic tests run WITHOUT vendor data + boundaries green
cd lab/analysis/regime/decompound_remc_2026-06-07 && python -m pytest test_days_to_first_skim.py -q
python scripts/check_boundaries.py

# §0 anchors still resolve
git log -1 --format='%h' -- lab/analysis/regime/decompound_remc_2026-06-07/decompound.py   # expect 6af6ae1
git log -1 --format='%h' -- core/mc/ingest.py                                        # expect e9be4ec
git log -1 --format='%h' -- docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md  # expect 9b219ab
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/rnd-pipeline/2026-07-14-cursor-handoff-sfrisk-f4-days-to-first-skim.md --type cc_handoff
# Expected: all checks PASS

grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cursor-return>
```

If Cursor returns `NEEDS_CONTEXT` or `BLOCKED`, this handoff is not complete; re-dispatch per §6.

---

## Related

- Parent Pre-Q: [`docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md`](../Q-SFRISK-1-successor-self-funded-risk-framework.md)
- Frozen F4 definition: [`docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md`](../pre-registration/Q-SFRISK-1-verdict-preregistration.md) (`9b219ab`)
- Reference instrument: [`lab/analysis/regime/decompound_remc_2026-06-07/`](../../../lab/analysis/regime/decompound_remc_2026-06-07/) + [`docs/adr/2026-06-07-decompound-remc-hold.md`](../../adr/2026-06-07-decompound-remc-hold.md)
- Surface-allocation governance: [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md)
- Owning ADR (completion falsifier, hard date 2026-11-08): [`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](../../adr/2026-07-11-challenge-era-claims-rescope.md)
