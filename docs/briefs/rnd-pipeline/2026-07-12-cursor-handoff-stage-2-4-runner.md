# Cursor Handoff — Stage-2/4 campaign runner (the Mine → Bind-K → Score → emit-matrix middle)

**Date:** 2026-07-12
**Parent session:** claude.ai advisor (Joshua + Claude) — delegated split: **advisor** ran the gate-reachability audit, drafted + empirically validated the DSR K/V fix (ADR below), landed the `var_trials` override in `universe_gate.py`, and amended the pre-reg/template; **Cursor builds this Stage-2/4 runner** (the mining + scoring + matrix-emission middle that has no code yet).
**Spawn target:** Cursor (research venv — `.venv-research`; `stumpy`/`ruptures`/`pycatch22`/`vectorbt`/`arch` live there, not in `pyproject.toml`)
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step)
**Parent question:** DISC-CAMP-0 shakedown traversal (Stage 2 Mine + Stage 3 Bind-K + Stage 4 Score); unblocks the gate-orchestrator §0.5(B) input contract that the **already-landed** `universe_gate.py` consumes.
**Authority:** Joshua (CEO). No commit/merge, and **no `db_fetch pull` / no real `register_search open`**, without Joshua's go. Run in `.venv-research`.

**Relocation note (2026-07-12):** Gen-2 research modules live in **`lab/`** (the `.claude/skills/*/scripts/*.py` are thin launchers). Build the runner in **`lab/discovery/`** (joining `register_search.py`, its Bind-K dependency). Import siblings as `from research_utils.universe_gate import run_universe_gate, load_thresholds_from_prereg, acf_block_size` and `from discovery.register_search import ...` (lab→lab, legal). Run via `PYTHONPATH=lab python -m discovery.stage24_runner`.

> **Binding dependency (read first — CHANGED from the earlier CC-handoff draft).** The
> pre-freeze gate-reachability audit
> ([`docs/notes/audits/2026-07-12-disccamp0-gate-reachability-audit.md`](../../notes/audits/2026-07-12-disccamp0-gate-reachability-audit.md))
> found the pre-reg's DSR K rule (`22 + 3·N_subseq ≈ 156,500`) effectively unreachable,
> and — reading the code once it landed mid-audit — a second, independent defect (the
> default empirical V estimator is biased upward by the very edge it scores). **Both are
> now fixed by a drafted, empirically-validated ADR**
> ([`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md),
> `Accepted`, operator ratified 2026-07-12): K_DSR = the **non-overlap tiling floor**
> `22 + 1 + Σ⌊T/m⌋` (≈3,200 for DISC-CAMP-0), and an **unconditional `V = 1/n` pin**.
> The `var_trials` override this needs **already landed** in `universe_gate.py` (additive
> keyword + `--var-trials` flag, 12/12 tests green). So the K/V **rule is no longer
> ambiguous** — Cursor implements against the concrete formula in §2.1. **The ADR is now `Accepted`, so the K rule is
> final — BUT the real `register_search open` binding + any `db_fetch pull` remain gated
> on the Stage-2/4 runner landing and a separate operator go for the campaign run**:
> build + test everything on **synthetic data only**; do not open the real campaign or
> pull data in this handoff.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any code)

Cursor: read each file and post a read-report in your first response **before** writing code. If repo state contradicts a §2 assumption, return `NEEDS_CONTEXT` with the discrepancy quoted.

- [`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) — report §2 (the K_DSR non-overlap floor + K_SPA split + unconditional V=1/n) and §6 (the validated power table: n≤250 near-zero power, n≥500 workable). **This is the load-bearing input — the K/V rule the runner binds against.**
- [`docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md`](../pre-registration/DISC-CAMP-0-preregistration.md) — report §1 (universe/tool ladder), the AMENDED §2 (K_DSR/K_SPA/V rules + power-disclosure), §3 (gate table), §4 (block-size ACF rule).
- [`docs/ltm/briefs/rnd-pipeline/DISC-CAMP-0-shakedown.md`](DISC-CAMP-0-shakedown.md) — report §7 stages 2–4 (Mine/Triage/Score) verbatim.
- [`docs/ltm/briefs/rnd-pipeline/2026-07-11-cc-handoff-gate-orchestrator.md`](2026-07-11-cc-handoff-gate-orchestrator.md) — report §0.5(B) (the approved option-(i) matrix contract = the runner's output contract).
- `lab/research_utils/universe_gate.py` — **ALREADY LANDED (Stage 5).** Report: the `run_universe_gate(...)` signature — specifically the new `var_trials: float | None` keyword (pass `1/n` to pin V, per the ADR; `None` = the biased default the runner must NOT use), the module-docstring "Stage-4 return-matrix contract" block, and `load_returns_matrix`'s expected CSV/parquet shape (timestamp index + candidate columns + exactly one `benchmark`). **The runner emits exactly what this consumes; do NOT rebuild the gate.**
- `lab/research_utils/temporal_consistency.py` — **ALREADY LANDED (Stage 6).** Report `run_temporal_battery` (or equivalent) signature + what per-candidate edge-series shape it consumes — the runner's per-trade / per-year artifact must feed it.
- `lab/discovery/register_search.py` — report the `open`/`close` manifest JSON schema (keys carrying K, alpha, window, hypothesis, candidates/pvalues). The runner is the CALLER.
- `lab/archive/harv_0_month_end_rebalance_es_2026-07/run_harv0.py` + `build_panel.py` + `cost_hurdle.py` — report `load_symbol_frame` (ts_event handling + weekday/weekend-bar filter) and the cost-hurdle shape. **The precedent to generalize — note it is DAILY logic; the OOS matrix needs a 1h intraday grid (new work, NOT reuse).**
- `lab/validation_selftest.py` — report `ControlData(trial_returns, entry_times, exit_times, best_index, label)` (the synthetic per-trade family shape the matrix-emit path can reuse for a fast unit test; note it is K=50, not campaign-K).
- `scripts/check_boundaries.py` — report the import contract (lab→{core,governance,lab}; `lab↔ops` isolation is load-bearing).
- `git log -1 --format='%h %ci' -- lab/research_utils/universe_gate.py` — report the sibling anchor you build against.

After Phase 0: post the read-report; proceed to §2 only once §0.5 is resolved.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Cursor: halt and ask rather than guess. The K/V rule is **resolved** (§2.1 — no longer a fork); the open forks are:

- **(A) catch22 → columns?** catch22 features are covariates, not strategies (tool-discipline Rule 3). **Default = zero scored columns** (covariate-only; catch22 contributes its 22 to the K_DSR count but produces 0 matrix columns / regime-annotations only). Implement this default; do NOT invent a feature→rule mapping (that would be a silent researcher DoF). Confirm, or ASK if the operator wants a pre-registered mapping first.
- **(B) Benchmark column.** The audit + `strategy-validation` §5 warn a zero-drift null lets a net-directional rule beat it by rediscovering drift; on trending gold a directional motif rule flatters a flat benchmark. **HALT:** is `benchmark` GC-flat/zero-edge (matching `universe_gate.load_returns_matrix`'s "zero-edge / buy-hold series" doc), drift-inclusive (buy-hold), or are motif rules made direction-neutral? Pick one, state it, and if unsure ASK — this changes what SPA actually tests.
- **(C) Low-n candidate handling.** The ADR §6 power table shows candidates with ≤250 OOS trades are DSR-unreachable by construction (near-zero power across the whole plausible-edge range). **Confirm the contract:** the scorer must **flag** such candidates (record `dsr_unreachable_low_n: true` in the matrix meta) rather than silently carry them to Stage 5 where they will fail regardless — so the closure can distinguish "failed DSR on evidence" from "structurally excluded by trade-count." Confirm this is the intended handling.

Post under `## §0.5 Response`; set `Status: NEEDS_CONTEXT` until resolved.

## §0.5 — Answers (parent-resolved, 2026-07-12; supersedes the NEEDS_CONTEXT hold)

Cursor's Phase-0 read-report was accepted; all forks resolved below. It also caught a real ADR §4 internal inconsistency (the "30-candidate V-floor" text vs the ratified unconditional `V=1/n`) — **fixed** in the ADR this same commit. Proceed to §2 on the branch named below.

**Workspace / checkout (load-bearing — resolved).** All inputs (ADR, amended pre-reg, the `var_trials` override, `temporal_consistency.py`) are on the pushed branch **`claude/stage-runner-gate-reachability-8569df`** (origin, commit `514499a` or later) = `2a15c0e` (origin/main incl. PR #337/#339) + this session's audit/ADR/code. **Build on that branch** (`git fetch origin && git checkout claude/stage-runner-gate-reachability-8569df`). Do NOT build at `af51179` — it is stale (pre-`temporal_consistency`, pre-`var_trials`). The `var_trials` override is **committed** there, not working-tree-only.

**Stage terminology (resolved — use the TEMPLATE numbering).** Canonical = `discovery-campaign-template.md` pipeline table: **Stage 2 = Mine, Stage 3 = Bind-K, Stage 4 = Score (IS)**; Stage 1 = Pull. The shakedown §7's "Stage 2 = Acquire / 3 = Mine / 4 = Triage" predates the template and is the stale numbering (a doc-reconciliation follow-on, not your concern). This runner = template Stages 2–4; **data acquisition (Stage 1 Pull) is NOT in scope** (synthetic only).

**(A) catch22 → columns — CONFIRMED.** Covariate-only: catch22 contributes **22 to K_DSR** and **0 scored matrix columns** (regime-annotation / diagnostic only). No feature→rule mapping (a silent DoF); a scored mapping would be a fresh pre-registered amendment, not this build.

**(B) Benchmark — RESOLVED with a synthetic-vs-real split** (both naive choices fail on real data, so this is deliberate):
- **Synthetic e2e test (THIS build): `benchmark ≡ 0` (zero-edge).** Correct and unambiguous — the synthetic GC-like bars are a driftless random walk + a planted *timing* motif, so there is no drift to rediscover; SPA-vs-zero tests exactly the planted edge.
- **Real campaign (deferred, post-freeze): zero-benchmark flatters** a directional rule on trending gold (§5 drift-rediscovery), and **always-on buy-hold structurally rejects** an intermittent rule (exposure mismatch — it can't beat always-long on per-bar mean, a NEW reachability trap in the other direction). **Pre-registered rule (provisional, operator-confirm-at-freeze; recorded in pre-reg §3): de-drift each candidate's returns** (subtract its exposure-matched unconditional GC drift — mean GC 1h return over the candidate's active bars) and use `benchmark ≡ 0` → tests *timing skill net of drift* (§5 "detrend, or claim only timing"; serves the "new leg must be uncorrelated to the long-continuation beta" requirement). **This does not block your build** — implement de-drift as an off-by-default transform the real run enables; keep the synthetic path zero-benchmark.

**(C) Low-n — CONFIRMED.** Candidates with ≤250 OOS trades get `dsr_unreachable_low_n: true` in the matrix meta, **still emitted/visible**, never silently dropped — so the closure separates structural exclusion (trade-count) from evidential DSR failure. Your Step 2.6 low-n variant (n≈150) is the expected-FAIL demonstration.

---

## §1 — Context

`lab/discovery/` contains only `register_search.py` + `__init__.py`. The **campaign-local Stage-2/4 runner does not exist** — the "missing middle" between a pulled dataset and the (already-built) universe gate. Stage 5 (`universe_gate.py`) and Stage 6 (`temporal_consistency.py`) landed 2026-07-12 and consume a Stage-4 return matrix that nothing currently emits. This runner produces it. It also provides the **synthetic-bar generator** that lets the full pipeline (Stage 2 → 5 → 6) be exercised end-to-end offline — the promote-branch proof the gate-reachability audit requires before DISC-CAMP-0 freezes. `run_harv0.py` is the only precedent (ad-hoc, single-study, hand-rolled stats — generalize its data-loading/cost shape, not its statistics).

**What Cursor is asked to produce:**
- `lab/discovery/stage24_runner.py` (or a `lab/discovery/campaign_runner/` package) — Mine + Bind-K + Score + emit-matrix, research-venv-only.
- The Stage-4 output bundle: aligned OOS return matrix (parquet, the option-(i) contract `universe_gate.load_returns_matrix` reads) + a per-trade sidecar (the DSR n/V source; K_SPA + `v_rule=1/n` recorded in meta) + a regime-labels side channel (`temporal_consistency` 6c test-conditions).
- A **synthetic GC-like 1h bar generator with an injectable known motif edge** + a **campaign-K end-to-end pos/neg test** that runs the runner's matrix through the REAL `universe_gate.run_universe_gate(..., var_trials=1/n)` + `temporal_consistency` and asserts promote/reject. This is the promote-branch proof.
- A thin skill launcher under `.claude/skills/futures-anomaly-discovery/scripts/`.

**What Cursor is NOT asked to do:** touch any locked parameter / allocation / `dd_protection` / `portfolio_mc.py` / Pine; **rebuild or modify `universe_gate.py` / `temporal_consistency.py`** (they are landed inputs — the `var_trials` fix is already done, do not re-touch it); reimplement any `arch`/`skfolio`/`stumpy` primitive; add research deps to `pyproject.toml`; **hardcode K, or bind K to a real campaign / run any `db_fetch pull`** (synthetic only until ADR ratified + operator go); build Stage 7 (native-micro realism — a separate later follow-on, needs $-gated MGC data); wire anything toward live execution (R6 = NO-GO).

---

## §2 — Execution plan

TDD throughout: write the failing synthetic-series test first, watch it fail, implement minimally, watch it pass (mirror how `tests/test_universe_gate.py` drove its module).

### Step 2.1 — K-count module (concrete rule, bound integer parameterized)
- **Action:** implement the ADR's K rule as a pure function: `K_DSR = 22 (catch22, face) + 1 (ruptures, face) + Σ_{m∈{30,60,90}} ⌊T/m⌋` where `T` = GC 1h IS bar count. Also compute the **raw** overlapping count `22 + 3·N_subseq` as a *reported diagnostic* (the bracket the pre-reg §2 requires: `{floor (binding), raw}`). The bound integer is **read from the pre-reg/ADR at `register_search open` time**, never hardcoded in the runner. Reuse `universe_gate.acf_block_size` for the shared Stage-5 block size.
- **Per-step gate:** unit test: for a synthetic T, `K_DSR` equals the hand-computed non-overlap sum; the raw diagnostic is also emitted; grep the diff — **no bare `3*N_subseq` bound as K, no `Keff_MP` patch**.

### Step 2.2 — Miner (research venv)
- **Action:** STUMPY matrix profile at m∈{30,60,90} (motif argmin + discord argmax per window); pycatch22 (covariate-only per §0.5(A)); ruptures PELT at the fixed penalty → regime labels to the side channel (test conditions, never filters — Q-REGIME-COND-1 scar). Pre-mining hygiene: intraday vol-U-shape normalization; correct GC continuous-contract adjustment (ratio/return, not difference-adjusted, or motif shapes mine phantom price levels).
- **Per-step gate:** deterministic given a seed + the frozen windows; on the synthetic-edge series (2.6) the miner surfaces the injected motif.

### Step 2.3 — Motif→rule templates (the candidate→return-series interface)
- **Action:** one scored candidate = one **frozen IS-derived rule** = one matrix column. Template: on the eval era, at each bar compute z-normalized Euclidean distance of the trailing m-bar window to the **frozen** motif/discord shape; when distance < frozen trigger, enter in the **frozen** direction (IS-realized forward-return sign — never re-fit on OOS) for a frozen horizon h; exit at h/stop.
- **Per-step gate:** no OOS re-optimization anywhere in the diff (grep the rule params — all frozen from IS).

### Step 2.4 — Scorer (IS triage + OOS matrix + low-n flag)
- **Action:** evaluate each frozen rule on **IS** (cost-law 4× MGC-hurdle kill per `strategy-validation` §2 — generalize `cost_hurdle.py` to MGC tick value $1.00 — + an IS permutation/bootstrap p per candidate for `register_search close`) and on **OOS** (the matrix). **Per §0.5(C): flag any candidate with ≤250 OOS trades `dsr_unreachable_low_n: true`** in the meta (DSR-excluded by construction per ADR §6), rather than silently carrying it.
- **Per-step gate:** IS-only selection (holdout unseen); `close` p-values are per-candidate IS p in [0,1], not the cost hurdle; low-n flag set correctly on a synthetic ≤250-trade candidate.

### Step 2.5 — Matrix emitter + manifest close (the option-(i) contract)
- **Action:** emit beside the manifest at `discovery_manifests/<run_id>__stage4_*`:
  - `__stage4_matrix.parquet` / `.csv` — the shape `universe_gate.load_returns_matrix` reads: a `timestamp` index (tz-aware UTC, OOS 1h grid — define the maintenance-break hour, holidays/half-sessions, pinned index source; **new intraday-grid work, not `run_harv0` daily reuse**), one float64 column per scored candidate, exactly one `benchmark` column (§0.5(B)); cell = frozen rule per-bar return **net of the frozen MGC cost model**, simple-return units identical across all columns.
  - `__stage4_matrix.meta.json` — era bounds, tz=UTC, cost constants, per-column provenance (motif-shape hash, m, trigger, horizon), `k_spa`, `k_dsr` + the `{floor,raw}` bracket, `v_rule="1/n"`, per-candidate `n_trades` + `dsr_unreachable_low_n`.
  - `__stage4_trades.json` — per-candidate ordered per-trade returns (the DSR n/V source; `n` = per-trade count, `V = 1/n`).
  - `__regime_labels.parquet` — ruptures labels (IS-fit, forward-only) for `temporal_consistency` 6c.
  Then call `register_search open` (bind K_DSR **only when not in synthetic mode + operator go**) → `close --pvalues <IS survivors>`; record `k_spa` distinct from `k_dsr`.
- **Per-step gate:** `universe_gate.load_returns_matrix(<emitted file>)` loads it without error; all columns + benchmark share one DatetimeIndex; meta records k_spa≠k_dsr and the v_rule.

### Step 2.6 — Synthetic-bar generator + campaign-K end-to-end pos/neg test (LOAD-BEARING)
- **Action:** a GC-like 1h series (random-walk + intraday vol-U-shape, 2010–2026 span) with an **injectable known motif edge**. Per the ADR §6 validated power table, spec the **positive** control's injected edge at **per-trade SR ≈ 0.30 with n ≥ 750 OOS trades** (a regime where the fixed gate has ≥0.9 power — NOT SR=0.20/n=500, which is only ~21% power and would make the test flaky). Also inject a **low-n variant (n≈150)** as an **expected-FAIL** case, demonstrating the ADR §6 low-n exclusion is real. Run the full miner→rule→score→emit→`universe_gate.run_universe_gate(var_trials=1/n)`→`temporal_consistency` path:
  - positive (SR≈0.30, n≥750): promotes (clears SPA + DSR + PBO + battery);
  - low-n positive (SR≈0.30, n≈150): flagged `dsr_unreachable_low_n`, does NOT promote (DSR fails) — and this is a *correct* outcome, asserted as such;
  - negative (pure noise): rejected.
- **Per-step gate:** all three cases resolve as above at the campaign K_DSR (~3,200); runs fully offline (no databento, no $).

### Step 2.7 — Wire + boundary gates
- **Action:** thin skill launcher (stdlib-only subprocess forward); `check_boundaries` green (lab→lab only, **no `ops` import**); imports resolve **only** in `.venv-research`; §-hooks in `discovery-campaign-template` Stage-4 and the `futures-anomaly-discovery` SKILL pointing at the runner.
- **Per-step gate:** `check_boundaries` green; grep proves no `ops` import; research-venv-only.

### Step 2.N — Closure
Return per §6. State explicitly: **no `db_fetch pull` ran**, **no real campaign opened** (synthetic only), whether the low-n expected-FAIL case behaved as designed, and the file list.

---

## §4 — Falsifiable hypothesis

**N/A — this handoff builds infrastructure, it does not test a market Pre-Q.** The build's own success predicate lives in the §2 per-step gates (esp. 2.6).

**Falsifier (build-design, not market):** if the miner→rule→matrix→gate path cannot recover the planted SR≈0.30/n≥750 edge at campaign K_DSR — i.e. Step 2.6's positive is **falsified** (planted edge not promoted) or the negative is promoted — then the candidate→return-series design is wrong (not merely its implementation); return `BLOCKED — plan-itself-wrong`, change withheld. (Note: the *low-n* case NOT promoting is a PASS, not a falsifier — it is the ADR §6 exclusion working as designed.)

---

## §5 — Forbidden moves

- **Hardcoding K, or binding K to a real campaign / running `db_fetch pull`.** K comes from the pre-reg/ADR at `open` time; the runner is synthetic-only until the ADR is `Accepted` + operator go. Adopting a convenient K to make the campaign freezable is the exact Q-HARV-0 error the audit caught.
- **Re-touching `universe_gate.py` / `temporal_consistency.py`** (incl. the just-landed `var_trials` fix). They are landed inputs; the runner *feeds* them. A "while I was in there" edit fails Pass-1 spec-compliance even if it runs.
- **OOS re-optimization** — any rule parameter re-fit on the 2019+ era. Rules are frozen from IS; OOS bars are only *evaluated*. Categorically forbidden.
- **Reimplementing `arch`/`skfolio`/`stumpy`** or building a hand-rolled matrix profile / bootstrap.
- **Regime labels as filters** — labels go to the side channel as `temporal_consistency` test-conditions; never subset the series to a favorable regime (Q-REGIME-COND-1 scar).
- **Importing `ops`** from the runner — `lab↔ops` isolation is the load-bearing boundary invariant.
- **Presenting `run_harv0`'s daily grid as the intraday matrix grid** — the 1h OOS grid is new work.
- **Silently dropping low-n candidates instead of flagging them** — the flag is what lets the closure distinguish structural exclusion from evidential failure (§0.5(C)).

---

## §6 — Gate + status return taxonomy

Return EXACTLY one of `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED` (`BLOCKED` carries its sub-case: `context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong`).

Mapping: all §2 per-step gates green + the 2.6 three-case end-to-end discriminates (positive promotes, low-n expected-fails, noise rejects) + no real pull + no hardcoded K → `DONE`; green with a flagged doubt → `DONE_WITH_CONCERNS`; a §0.5 fork unresolved → `NEEDS_CONTEXT`; unresolvable obstruction → `BLOCKED — <sub-case>`. Program-level: **RESOLVED** on `DONE`/`DONE_WITH_CONCERNS` + accepted diff + the synthetic-positive traverses; **AMBIGUOUS** if held at a §0.5 fork; **FALSIFIED** if the miner→rule→matrix design cannot recover a planted edge (design wrong, not just implementation).

```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Per-step gates: 2.1 [..], 2.2 [..], ... 2.7 [..]
2.6 end-to-end: positive [promote?], low-n [expected-fail?], noise [reject?]
Diffs (files touched): <list — expect only lab/discovery/*, the skill launcher, tests/, and the two doc §-hooks>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (two passes, then consolidated)

**Pass 1 — Spec-compliance.** Built EXACTLY §2 — a Stage-2/4 runner on vetted libs + the synthetic generator; a re-touch of `universe_gate.py`/`temporal_consistency.py`, a hardcoded K, or a real pull **fails Pass 1 even if it runs**. Diff list contains only the §1 deliverable paths.

**Pass 2 — Quality.** Rules frozen from IS (no OOS re-fit); matrix loads via `universe_gate.load_returns_matrix`; per-trade sidecar drives DSR with V=1/n; low-n flag set; cost model applied; k_spa recorded distinct from k_dsr; the 2.6 end-to-end genuinely discriminates all three cases at campaign K.

**Pass 3 — Consolidated read.** The hot spot: the emitted matrix contract must match `universe_gate.load_returns_matrix` **and** the ADR's K_SPA/K_DSR split **and** the v_rule=1/n the gate is invoked with — a drift among these is exactly what per-step gates miss. Confirm the runner passes `var_trials=1/n` to the gate in 2.6 (not the biased default).

---

## §10 — Audit hooks (runnable)

```bash
cd "C:/Users/joshu/multi_firm_operations"

# Runner exists in the discovery package, research-venv-only, no ops import
ls lab/discovery/stage24_runner.py lab/discovery/campaign_runner/ 2>/dev/null
grep -rnE "import ops|from ops" lab/discovery/ 2>/dev/null   # expect EMPTY
python scripts/check_boundaries.py

# K is NOT hardcoded to the raw rule or the invalid Keff patch
grep -rnE "3 ?\* ?N_subseq|Keff_MP" lab/discovery/ 2>/dev/null   # expect EMPTY (K = non-overlap floor, read from pre-reg)

# The gate modules were NOT re-touched by this runner build
git diff --name-only | grep -E "universe_gate|temporal_consistency"   # expect EMPTY

# No real pull ran; campaign not opened
ls discovery_manifests/disccamp0_gc_2010_18.json 2>/dev/null && echo "VIOLATION" || echo "ok: synthetic only"

# The 2.6 end-to-end discriminates at campaign K (positive/low-n/noise), invoking the REAL gate with V=1/n
PYTHONPATH=lab .venv-research/Scripts/python -m pytest tests/ -k "stage24 or campaign_runner" -q

# Emitted matrix is loadable by the landed gate + carries the k_spa/v_rule meta
PYTHONPATH=lab .venv-research/Scripts/python - <<'PY'
import glob, json
from research_utils.universe_gate import load_returns_matrix
for p in glob.glob("discovery_manifests/*__stage4_matrix.parquet"):
    rm = load_returns_matrix(p); assert rm.benchmark is not None
    meta = json.load(open(p.replace("matrix.parquet","matrix.meta.json")))
    assert meta["v_rule"] == "1/n" and meta["k_spa"] != meta["k_dsr"]
    print(p, rm.returns.shape, "ok")
PY

# Doc §-hooks landed
grep -rn "stage24_runner" docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md .claude/skills/futures-anomaly-discovery/SKILL.md
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/rnd-pipeline/2026-07-12-cursor-handoff-stage-2-4-runner.md --type cc_handoff
# Expected: no HARD violations (§0/§0.5/§4/§5/§6 four-state/§7 two-pass/§10 present)

# The K/V rule the runner binds against is the ratified one, not the superseded raw count
grep -n "non-overlap" docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md
```
