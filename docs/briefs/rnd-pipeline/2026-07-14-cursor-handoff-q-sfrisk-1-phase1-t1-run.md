# Cursor Handoff — Q-SFRISK-1 Phase 1: run T1 against the decompound instrument (report-only, no verdict)

**Date:** 2026-07-14
**Parent session:** Claude Code operator session (Joshua + Claude). The Q-SFRISK-1 Phase-0 numeric freeze is canonical on `origin/main` (`9b219ab`, single triple **T1**: F1 p99 max-DD ≤10%/half + F3 ADOPT banded + F4 median-days-to-first-skim >252 bd; **F2 TUW deferred**). The F4 producing-code obligation is now discharged (`days_to_first_skim.py`, `3ee7e8f`, PR #376). **This handoff is Phase 1: run the frozen T1 metrics on the real clean-vintage panel and report the numbers — nothing else.**
**Spawn target:** Cursor (frozen-spec implementation — [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md)). Deps stdlib + `numpy`/`pandas`, already on the instrument path.
**Repo:** `multi_firm_operations` — branch off **current `origin/main`** (must contain `9b219ab` pre-reg + `3ee7e8f` F4 instrument; if your checkout predates either, `git fetch` and re-branch before starting).
**Brief type:** Cursor handoff (multi-step)
**Parent question:** [`Q-SFRISK-1`](../Q-SFRISK-1-successor-self-funded-risk-framework.md) §7 step 3 (Phase 1 — "run instrument against the frozen triple(s) only"). **§6 verdict assertion is Phase 2, reserved to CC/operator** ([surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md) §2 test 1; go-live-gating adjudication).
**Authority:** Joshua (CEO). No commit/merge without Joshua's go. **Named locked/frozen surfaces Cursor must NOT touch or re-decide:** any `core/*` file; `decompound.py` / `remc_cleanvintage.py` / `days_to_first_skim.py` bodies (imported/run read-only — call them, don't edit them); the frozen T1 numbers in the pre-reg (10% / 252 bd / banded); the F1/F4 metric definitions; Pine; the locked MC anchor. **And — the load-bearing one — do NOT assert or imply a §6 verdict (RESOLVED / FALSIFIED / AMBIGUOUS-HOLD): report numbers only.**

> **Report-only, build-behind-the-verdict (read first).** Phase 0 (freeze) and the F4 instrument are done; the pre-reg is `NUMERIC FROZEN`. This handoff **runs** the already-frozen T1 metrics against the real clean-vintage panel and **reports** F1 (per-half p99 max-DD) and F4 (per-half median days-to-first-skim + censoring). It does **not** compare any number to its bar (10% / 252 bd), does **not** emit a pass/fail boolean, and does **not** fire the Q-SFRISK-1 §6 verdict — the operator/CC apply the T1 bars in Phase 2. Cursor **may** print/commit real-panel numbers (that is the deliverable here — unlike the F4 instrument-build handoff, which was synthetic-only). It may not editorialize them into a verdict.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any code)

Cursor: read each item and post a read-report in your first response **before** writing code. If repo state contradicts a §2 assumption or the pre-reg, return `NEEDS_CONTEXT` with the discrepancy quoted — do **not** resolve it unilaterally.

- [`docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md`](../pre-registration/Q-SFRISK-1-verdict-preregistration.md) (`9b219ab`) — report the **Status** line (must read `NUMERIC FROZEN`), **Field 1** (`VALUE: p99 max-DD ≤ 10% per regime half`, form = path max-DD ceiling, binds to `regime_gate.py` p99 per half at the locked book), **Field 2** (`DEFERRED` — no TUW clause in T1), **Field 3** (`ADOPT +5%/$200K banded`), **Field 4** (`VALUE: median business-days-to-first-$210K-skim > 252 bd ⇒ IMPRACTICAL`, metric = median days-to-first-skim), and the **T1 grid row** (3-dimension: F1 + F3 + F4). **This file freezes what to compute; you transcribe no new number and redefine nothing. If Status ≠ NUMERIC FROZEN, `BLOCKED — context-problem`.**
- `lab/analysis/regime/decompound_remc_2026-06-07/days_to_first_skim.py` (`3ee7e8f`) — report `median_days_to_first_skim_by_partition(panel, n_paths, seed)` (returns `{H1, H2, pooled}`, each with `median_days_to_first_skim` / `censoring_rate` / `n_paths` / `horizon_bd` / `seed`), `build_banded_portfolio_panel()` (B_2020 construction — requires vendor CSVs under `inputs/`), `BOOT_SEED = 20260607`, `DEFAULT_N_PATHS = 1000`, and the right-censoring sentinel (`len + 1` for a path that never skims). **This is the F4 producing code — call it, do not re-implement or edit it.**
- `lab/analysis/regime/decompound_remc_2026-06-07/remc_cleanvintage.py` (report the on-disk anchor via `git log -1`) — report `NEW_FILES` (the clean 2026-06-25 vintage CSVs — the correct inputs), `build_streams()` (banded sub-dict), and **`half_panels()`**: it runs `LOCKED k=1.0` + two de-risk candidates and prints per-half `pass / bust / p99 / med`. **F1 for T1 is the `LOCKED k=1.0` row's H1 and H2 p99 only** — the C1/C2 de-risk rows are NOT part of T1 (T1 evaluates the locked book). Report the split logic (`mid = panel.index[len(panel)//2]`) and confirm it is the SAME split `days_to_first_skim.median_days_to_first_skim_by_partition` uses (it must be, for F1 and F4 to be on the same H1/H2 partition).
- `lab/analysis/regime/decompound_remc_2026-06-07/decompound.py` (`6af6ae1`) — report `ACCOUNT`, `WITHDRAW_AT`, `ALLOC`, `FIXED_1R`, `rebank(mode="banded")`, `run_mc` — the shared banded/decompound machinery both metrics consume. **Read-only.**
- `lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_cleanvintage_2026-06-25.md` — report the locked-config half-panel numbers already on record (H1 bust 13.84% / p99 **7.76%** / med 62; H2 0.21% / p99 **4.53%** / med 20). **These are your F1 reproduction target** — your Phase-1 F1 run reproduces the LOCKED row of this table (same instrument, same vintage). A material divergence is a `NEEDS_CONTEXT`, not a silent overwrite.
- `git log -1 --format='%h %ci' -- lab/analysis/regime/decompound_remc_2026-06-07/days_to_first_skim.py lab/analysis/regime/decompound_remc_2026-06-07/remc_cleanvintage.py docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md` — report all three as your build anchors.
- `scripts/check_boundaries.py` — report the import contract (`lab → {core, governance, lab}` read-only; no `ops`). This driver lives in `lab/`, imports `core/` read-only via the `portfolio_mc` facade (already how `days_to_first_skim.py` does it), never touches `ops/`.

After Phase 0: post the read-report; proceed to §2 only once §0.5 is resolved.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Parent-recommended defaults are stated; confirm or challenge each in the Phase-0 response. Set `Status: NEEDS_CONTEXT` until resolved.

- **(A) Vendor-data availability.** Both metrics require the clean 2026-06-25 vintage CSVs under `lab/analysis/regime/decompound_remc_2026-06-07/inputs/` (gitignored, local-only). **Recommended default:** confirm the four CSVs are present in your checkout before running; if absent, `BLOCKED — context-problem` (Joshua must drop them in — they cannot be committed). Do NOT substitute the stitched 2026-06-07 vintage (carries the DD-inflation stitch-seam artifact).
- **(B) F4 sample size for a reported (not smoke) number.** The instrument's `DEFAULT_N_PATHS = 1000` is documented "smoke-friendly." A number that will feed a go-live-gating verdict should be resolution-stable. **Recommended default:** run F4 at **`n_paths = 30000`** (= `SIMS_PER_SEED × len(SEEDS)` = 10 000 × 3, the instrument's own production-scale reference), `seed = BOOT_SEED` (frozen, `20260607`). Report the exact `n_paths` and `seed` in the artifact. Confirm, or propose a different production scale (do not silently keep 1000).
- **(C) F4 censoring honesty (the F1-class trap for this metric).** A high `censoring_rate` means most resampled paths never skim within the horizon, so the median is right-censored and the ">252 bd" reading may be an under-statement of true slowness. **Recommended default:** report `censoring_rate` for H1/H2/pooled **prominently alongside** each median (never the median alone), and if any partition's censoring_rate ≥ 50% add a one-line flag `⚠ median right-censored — >half of paths never skimmed` **as a fact, not a verdict**. Confirm.
- **(D) F1 config = locked book only.** **Recommended default:** F1 is the `remc_cleanvintage.half_panels()` **LOCKED k=1.0** row's H1 and H2 `p99` (report `pass`/`bust`/`med` too, as context); the C1 k=0.55 and C2 DDscale0.20 de-risk rows are **not** part of T1 and are not reported here (they belong to the separate decompound-HOLD de-risk question). Confirm you will capture only the LOCKED row.
- **(E) Artifact + driver shape.** **Recommended default:** a thin driver `lab/analysis/regime/decompound_remc_2026-06-07/run_sfrisk_t1_phase1.py` that (i) imports `remc_cleanvintage` and runs its locked half-panels for F1, (ii) imports `days_to_first_skim.median_days_to_first_skim_by_partition` for F4, and (iii) emits `RESULTS_sfrisk_t1_phase1_2026-07-14.md` — a plain numeric table (F1 H1/H2 p99 + F4 H1/H2/pooled median + censoring), each number labeled with the bar it will later be compared against **stated as context, not applied** (e.g. "F1 bar = ≤10% (applied in Phase 2)"), and **zero** RESOLVED/FALSIFIED/AMBIGUOUS language. The driver imports the two existing functions; it does **not** re-derive their internals. Confirm, or propose running the two existing entry points directly and hand-assembling the artifact.

---

## §1 — Context

The Q-SFRISK-1 pre-reg froze T1 (single triple) and was operator-confirmed 2026-07-14; the F4 instrument (median days-to-first-skim) landed via PR #376 — the one outstanding producing-code obligation. Phase 1 is now unblocked: run the two frozen metrics on the real clean-vintage panel and report the numbers so Phase 2 (CC/operator) can assert §6. Routing note: this run must happen where the vendor CSVs live (local), and Cursor correctly will not free-form a real-panel MC without a frozen spec — hence this handoff, small though the build is (the frozen no-verdict guard is the point, not the LOC count).

**What Cursor is asked to produce:**
- `lab/analysis/regime/decompound_remc_2026-06-07/run_sfrisk_t1_phase1.py` — thin driver (§0.5(E)).
- `lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_sfrisk_t1_phase1_2026-07-14.md` — the numeric report (F1 per-half p99; F4 per-half + pooled median + censoring), **no verdict**.
- If the driver contains any non-trivial glue logic, a small `test_run_sfrisk_t1_phase1.py` proving the F1-row extraction and F4-partition wiring on a synthetic panel (real-panel run needs no test — it's a report).

**What Cursor is NOT asked to do:** compare any number to 10% or 252 bd; emit a pass/fail; assert or imply a §6 verdict; compute F2/TUW (deferred, out of scope); report the C1/C2 de-risk rows; edit any `core/` file or the three existing `decompound_remc` modules; re-tune seeds/n_paths beyond §0.5(B); touch `ops/`.

---

## §2 — Execution plan

TDD for any glue logic; the real-panel run is a report, not a tested unit.

### Step 2.1 — Driver skeleton + imports (read-only)
- **Inputs:** §0.5(E) resolution; `remc_cleanvintage`, `days_to_first_skim` (imported, not edited).
- **Action:** build `run_sfrisk_t1_phase1.py` importing the two existing functions; wire the vendor-input presence check (§0.5(A)) with a clean `BLOCKED`-style message if absent.
- **Per-step gate:** `python -c "import run_sfrisk_t1_phase1"` succeeds; no edit to the three existing modules (grep the diff).

### Step 2.2 — F1: locked-config per-half p99 max-DD
- **Inputs:** `remc_cleanvintage.half_panels()` (or its underlying per-half `run_mc` at the LOCKED config), clean-vintage inputs.
- **Action:** run the locked half-panels; capture H1 and H2 `p99` (+ pass/bust/med as context). Do NOT capture C1/C2.
- **Expected output:** F1 numbers, reproducing the `RESULTS_cleanvintage_2026-06-25.md` LOCKED row (H1 p99 ≈7.76%, H2 ≈4.53%) within MC noise.
- **Per-step gate:** F1 H1/H2 p99 reproduce the on-record locked row; a material divergence bounces `NEEDS_CONTEXT`.

### Step 2.3 — F4: per-half + pooled median days-to-first-skim
- **Inputs:** `days_to_first_skim.median_days_to_first_skim_by_partition(panel, n_paths=30000, seed=BOOT_SEED)` on `build_banded_portfolio_panel()`.
- **Action:** run it; capture H1/H2/pooled median + censoring_rate.
- **Expected output:** F4 numbers at the frozen production scale, censoring reported per §0.5(C).
- **Per-step gate:** `n_paths`/`seed` recorded in the artifact; censoring reported alongside every median; the ≥50% flag present iff triggered.

### Step 2.4 — RESULTS artifact (report-only)
- **Inputs:** Steps 2.2–2.3.
- **Action:** emit `RESULTS_sfrisk_t1_phase1_2026-07-14.md` — F1 (H1/H2 p99) + F4 (H1/H2/pooled median + censoring), each with its Phase-2 bar stated as context only; a header noting `T1 = F1 + F3(banded) + F4; F2 deferred`; explicit line: `Verdict deferred to Phase 2 (CC/operator) — this file asserts no RESOLVED/FALSIFIED/AMBIGUOUS.`
- **Per-step gate:** grep the artifact for `RESOLVED|FALSIFIED|AMBIGUOUS` → zero hits.

### Step 2.5 — End-to-end + boundaries
- **Action:** driver runs clean end-to-end on the real panel; `check_boundaries.py` green; diff contains only the new driver + RESULTS (+ optional test) under `lab/analysis/regime/decompound_remc_2026-06-07/`.
- **Per-step gate:** boundaries green; no `core/`/`ops/`/existing-module diff.

### Step 2.6 — Closure report
Post the §6-format closure report. `DONE` means the numbers are reported — **never** a claim about T1's verdict.

---

## §4 — Falsifiable hypothesis (parent gate's, restated — NOT under test here)

No hypothesis is under test in this run — it produces the numbers Phase 2 will assert against **H-SFRISK-1** (verbatim from the pre-reg): T1 clears iff its declared bars hold on **both** regime halves without crossing the impracticality bar. This build makes the verdict computable from the RESULTS numbers; it does not compute or claim it. F1 bar (≤10% p99/half) and F4 bar (median >252 bd ⇒ impractical) are applied by CC/operator in Phase 2, not here.

---

## §5 — Forbidden moves (each genuinely tempting, transcribed from the pre-reg + ADR)

- **Asserting or implying a §6 verdict in the RESULTS file** ("H1 p99 8% < 10% so F1 clears…"). The single load-bearing prohibition — report the number, state the bar as context, stop. Verdict is Phase 2 / CC.
- **Applying the bar** — computing `p99 ≤ 10%` or `median > 252` as a boolean anywhere. Report the raw metric; the comparison is the operator's.
- **Reporting the median without its censoring rate** — the F4-metric analogue of the F1 headline-bust trap; a censored median alone reads optimistically.
- **Including the C1/C2 de-risk rows as if they were T1** — T1 is the locked book; de-risk candidates belong to the separate decompound-HOLD question.
- **Computing F2/TUW** — deferred, explicitly out of T1 scope; adding it is scope creep against a frozen freeze.
- **Editing `decompound.py` / `remc_cleanvintage.py` / `days_to_first_skim.py` or any `core/` file** "while I'm in there." Call them; log any concern under `DONE_WITH_CONCERNS`.
- **Silently keeping `n_paths=1000`** for the reported F4 number — that is a smoke default, not a production estimate (§0.5(B)).

---

## §6 — Gate + status return taxonomy

Report EXACTLY one of: `DONE` | `DONE_WITH_CONCERNS` | `NEEDS_CONTEXT` | `BLOCKED — <context-problem | capability-problem | scope-problem | plan-itself-wrong>`.

A `DONE` here means F1 + F4 numbers are reported faithfully in the RESULTS artifact with no verdict — it is **never** a claim about Q-SFRISK-1's §6 disposition, which is the operator/CC's Phase-2 call.

Closure report format:
```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Per-step gates: 2.1 [...], 2.2 [...], 2.3 [...], 2.4 [...], 2.5 [...]
Diffs (files touched): <list>
§0.5 resolutions applied: A=<...>, B=<...>, C=<...>, D=<...>, E=<...>
F1 (locked) H1/H2 p99: <values> (reproduces RESULTS_cleanvintage locked row? y/n)
F4 H1/H2/pooled median + censoring (n_paths, seed): <values>
No-verdict grep (RESOLVED|FALSIFIED|AMBIGUOUS in artifact): <0 expected>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (after Cursor returns)

**Pass 1 — Spec-compliance:** driver + RESULTS present; diff only under `lab/analysis/regime/decompound_remc_2026-06-07/`; no `core/`/`ops/`/existing-module edit; F2 absent; C1/C2 absent.
**Pass 2 — Quality:** F1 reproduces the on-record locked half-panel p99 (7.76% / 4.53%) within noise; F4 run at n_paths=30000/seed=BOOT_SEED with censoring reported; **artifact contains zero verdict language** (grep-confirmed); the ≥50%-censoring flag present iff triggered.
**Pass 3 — Consolidated read:** F1 and F4 are on the SAME H1/H2 split; the numbers hang together (H1 worse than H2, consistent with the known regime split); nothing in the artifact pre-empts the Phase-2 verdict.

Only after all three passes does CC proceed to Phase 2 (§6 assertion + §9 closure).

---

## §10 — Audit hooks (runnable)

```bash
# No verdict language leaked into the report
grep -in "RESOLVED\|FALSIFIED\|AMBIGUOUS" lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_sfrisk_t1_phase1_2026-07-14.md
# Expected: empty

# No edit to core/ or the three existing decompound_remc modules
git diff --stat <pre-spawn-commit> -- core/ \
  lab/analysis/regime/decompound_remc_2026-06-07/decompound.py \
  lab/analysis/regime/decompound_remc_2026-06-07/remc_cleanvintage.py \
  lab/analysis/regime/decompound_remc_2026-06-07/days_to_first_skim.py
# Expected: empty

# F4 ran at production scale, not smoke
grep -n "n_paths" lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_sfrisk_t1_phase1_2026-07-14.md
# Expected: 30000 (not 1000)

# Boundaries + any glue test
python scripts/check_boundaries.py
cd lab/analysis/regime/decompound_remc_2026-06-07 && python -m pytest test_run_sfrisk_t1_phase1.py -q  # if present
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/rnd-pipeline/2026-07-14-cursor-handoff-q-sfrisk-1-phase1-t1-run.md --type cc_handoff

git log -1 --format='%h %ci' -- lab/analysis/regime/decompound_remc_2026-06-07/days_to_first_skim.py  # expect 3ee7e8f
grep -n "NUMERIC FROZEN" docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md
grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cursor-return>
```

If Cursor returns `NEEDS_CONTEXT` or `BLOCKED`, this handoff is not complete; re-dispatch per §6.

---

## Related

- Frozen + confirmed grid: [`docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md`](../pre-registration/Q-SFRISK-1-verdict-preregistration.md) (`9b219ab`)
- Parent Pre-Q: [`docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md`](../Q-SFRISK-1-successor-self-funded-risk-framework.md)
- F4 instrument (built PR #376, this handoff runs it): `lab/analysis/regime/decompound_remc_2026-06-07/days_to_first_skim.py`
- F4 instrument handoff (prerequisite, now discharged): [`docs/briefs/rnd-pipeline/2026-07-14-cursor-handoff-sfrisk-f4-days-to-first-skim.md`](2026-07-14-cursor-handoff-sfrisk-f4-days-to-first-skim.md)
- F1 producing code + reproduction target: `lab/analysis/regime/decompound_remc_2026-06-07/remc_cleanvintage.py` + `RESULTS_cleanvintage_2026-06-25.md`
- Routing doctrine: [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md)
