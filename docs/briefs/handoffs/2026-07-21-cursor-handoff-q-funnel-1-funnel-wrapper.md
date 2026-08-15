# Cursor Handoff — Q-FUNNEL-1 funnel wrapper (fee/reset/funded-phase EV harness)

**Date:** 2026-07-21
**Parent session:** Claude Code operator session (Joshua + Claude) — authored the design doc, scoping brief, and FROZEN pre-registration for Q-FUNNEL-1 in the same session; this handoff builds the harness the pre-registration specifies.
**Spawn target:** Cursor
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step)
**Parent question:** Q-FUNNEL-1 (`docs/briefs/rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md`) — discharges the retry-EV objective deferred four times since 2026-07-11.
**Authority:** Joshua (CEO). No commit/merge without Joshua's go. **No `core/` edit, no `register_search open`, no live rail/account touch, no locked-parameter edit anywhere.** Build + test against the frozen pre-registration only.

---

## Routing-test self-check (per `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`, applied by the parent session before dispatch)

- **Test 0 (dispatch-environment bytes/credentials) — the load-bearing one for this task.** U1 must reuse the **same sha256-pinned CME panel** the WATCH-1 haircut ratification used: `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv` and `Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv`, both under the gitignored `core/data/tv_exports/pepperstone/` tree. **This exact panel already caused a cloud-dispatch bounce once** (ADR addendum, 2026-07-15: "Class-S C1 G0–G8 scoring — cloud run → `NEEDS_CONTEXT` — gitignored CME CSVs (`15d8b`/`beabf`) absent from the cloud checkout"). The parent session's own worktree has **zero CSVs present** (`find core/data -name "*.csv" | wc -l` → 0) — only `SHA256SUMS` manifests. **Per ADR Step 0: this defaults to LOCAL dispatch, full stop, unless Cursor's actual dispatch environment is confirmed to have these two files present before any code is written.** Phase 0 below makes this the first, blocking check.
- **Test 1 (locked/governed surface):** No. U1 imports `core/mc/simulation.py`, `run_class_s_c1_scoring.py`, `run_class_s_c1_regime_gate.py` **read-only**. No edit to any `core/` file, no ADR/pre-reg/closure authoring (all three already exist, authored by the parent session). Stays off the locked surface — Cursor-eligible.
- **Test 2 (spec frozen):** Yes. `docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md` is `FROZEN` — EV formula, rungs, retry policies, edge-scenario grid, the 25%/bootstrap-band/regime-consistency threshold, `MAX_RETRIES=5`, and the full Select Flex 100K funded-payout config (§5, pinned with dated primary-source quotes) are all fixed. No judgment call is expected mid-build.
- **Test 3 (overhead threshold):** Clears easily — new `lab/archive/q_funnel_1_2026-07/` directory, funnel wrapper, regression-pin tests, a 3-rung × 2-retry × 3-edge-scenario × 2-regime-half MC sweep (36 cells), RESULTS.md. Well above the ~1-hour / ~3-file floor.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any code)

Cursor: read each item and post a read-report in your first response **before** writing code. If repo state contradicts a §2 assumption, return `NEEDS_CONTEXT` with the discrepancy quoted.

**0.0 — Blocking dispatch-environment check (do this FIRST, before any other read):**
```bash
ls core/data/tv_exports/pepperstone/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv
ls core/data/tv_exports/pepperstone/Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv
```
If either is absent, **stop immediately and return `BLOCKED — capability-problem`** with this exact message: "Panel CSVs absent in dispatch environment; per ADR 2026-07-14 Step 0 this build requires local dispatch or manually-staged bytes — not a code problem, do not attempt a synthetic substitute." Do not proceed to any other §0 item.

If present, continue:

- [`docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md`](../pre-registration/Q-FUNNEL-1-verdict-preregistration.md) — report the full EV formula, the three rungs, the two retry policies, the three-point edge-scenario grid, the ratified §3(a)/§3(b)/§3(c) threshold (25% relative + non-overlapping bootstrap bands + cross-regime-half sign consistency), `MAX_RETRIES=5`, and the entire §5 pinned funded-payout config (split, cap, winning-day threshold, loss-recovery rule, drawdown-lock arithmetic, purchase restrictions). This is the harness's complete spec — nothing here is re-derived.
- [`docs/briefs/rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md`](../rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md) — report §6 (gate table), §7 (execution plan phases), §5 (forbidden moves).
- [`core/mc/simulation.py`](../../../core/mc/simulation.py) — report `simulate_path`'s signature and return shape (the per-path daily-equity/outcome series U1 wraps), the `trailing_locking` floor formula, and the consistency-clause semantics (soft gate, never absorbing).
- [`core/firm_rules.py`](../../../core/firm_rules.py) — report `Tradeify_Select_100K`'s exact fields (confirm `max_dd_pct=3.0`, `daily_loss_pct=None`, `dd_lock_offset_usd=100`, `profit_target_pct=6.0`, `min_trading_days=3`, `consistency_rule_pct=40.0` — this account is confirmed Select **Flex**, operator chat 2026-07-21).
- [`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/run_haircut_regime_remc.py`](../../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/run_haircut_regime_remc.py) — report the module's own docstring, the `ARMS` dict, `run_arm`, and how it imports `run_class_s_c1_scoring` (panel build) and `run_class_s_c1_regime_gate` (`full_panel_reference`, `part_b_half_panel`, `part_a_bootstrap`, `compose_verdict`) as a **sibling runner pattern, not an in-place edit**. U1 follows this exact pattern — a new sibling module, importing the same panel-build + regime-gate primitives read-only, adding a funnel-accounting layer on top.
- [`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md`](../../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md) — report the WATCH-1 0.50× numbers (full-panel bust 0.08%, H1 bust, bootstrap-95th bust, pass-5th 95.76%) that Phase 1's regression pin must reproduce at `fees=0, funded_value=0, retry=never`.
- [`lab/analysis/c1/q_rail_1_2026-07/PHASE4.md`](../../../lab/analysis/c1/q_rail_1_2026-07/PHASE4.md) — report the eval fee figures ($328 base / $258 promo / $681 worst-plus-reset) this repo already pinned from its own account purchase.
- `git log -1 --format='%h %ci' -- docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md` — report the anchor (expect `8ca20e3` or later if amended).
- [`scripts/check_boundaries.py`](../../../scripts/check_boundaries.py) — report the import contract (`lab→{core,governance,lab}`).

After Phase 0: post the read-report; proceed to §2 only once §0.5 is resolved.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Parent-recommended defaults are stated; confirm or challenge in the Phase-0 response. Set `Status: NEEDS_CONTEXT` until resolved.

- **(A) Terminal-value accounting for a "busted-post-funding" lineage.** The pre-registration's EV formula (§2) defines this case as `terminal_value = -cumulative_spend`. **Recommended default:** any realized payouts already extracted before the post-funding bust are **not** clawed back in this formula (i.e., `terminal_value = sum(realized payouts so far) - cumulative_spend`, which can be positive even if the account ultimately busts) — this matches the real Tradeify mechanic (a breach terminates the account but does not reverse prior payouts) and is the economically correct reading. Confirm this is what "busted-post-funding loss" in the pre-reg means, or flag if the pre-reg's phrasing implies full clawback.
- **(B) Funded-phase daily-return draw source.** The frozen `simulate_path` daily loop stops at `pass`. For the funded-phase continuation, the funnel wrapper needs a daily-return generating process to keep simulating *after* pass. **Recommended default:** continue drawing from the **same week-block-bootstrap panel** `simulate_path` already draws from for the pre-pass phase (same haircut multiplier applied, same regime-half split), simply not stopping the loop at the pass gate — i.e., extend `simulate_path`'s own draw mechanism via a wrapper-level continuation, not a new distribution. This is a `core/mc/simulation.py` **read-only** reuse question, not an edit — confirm the cleanest way to extend without modifying that file (e.g., call the same underlying panel-sampling function directly rather than patching `simulate_path`).
- **(C) Winning-day threshold interaction with the payout-frequency clock.** The pinned config (pre-reg §5) says payouts trigger "every 5 winning days" where a winning day requires ≥$200 profit on the 100K tier. **Recommended default:** track a separate winning-day counter within the funded-phase daily loop (increments only on days meeting the $200 floor; resets are NOT implied by the source doc — confirm whether "every 5 winning days" is a rolling/cumulative count or resets after each payout cycle; the primary source's Q&A section implies cycle-based, i.e., the counter resets after each payout is taken). Flag if the primary source's language is ambiguous on this point rather than guessing.
- **(D) Edge=0 and edge=half-panel construction.** The pre-reg specifies "bootstrap-preserving variance/autocorrelation" de-meaning. **Recommended default:** de-mean each strategy leg's daily return series independently (not the combined book series) before re-combining, so cross-leg correlation structure is preserved — confirm this is the intended unit of de-meaning, since de-meaning the already-combined `daily_100k` series vs. de-meaning per-leg before combining can give different variance/autocorrelation properties.

---

## §1 — Context

The parent session designed and froze a study answering a question the discovery apparatus's bust/pass gate cannot: does the funnel EV per dollar-day of the c1 book vary materially across sizing rungs once eval fees, resets, and the funded-phase payout structure are priced? The gap has been named four times since 2026-07-11 (`tradeify_futures3_remc`, Bulenox C5, `tradeify_selectflex_remc`, the survivor-scoring-and-ddp-reframe recommendation's §3.4) and never built. Everything needed to build it is now frozen: the EV formula, the accept/reject thresholds, the retry cap, and — resolved this session via live primary-source fetch — the complete Select Flex 100K funded-payout config.

**What Cursor is asked to produce** (all in `lab/archive/q_funnel_1_2026-07/`):
- `funnel.py` — the funnel wrapper: consumes `simulate_path` per-path output (or the same underlying panel-draw primitives, per §0.5(B)), adds eval-fee/reset-recursion accounting, funded-phase continuation with the pinned payout policy, and computes EV/day per the frozen formula.
- Regression-pin tests: with `fees=0, funded_value=0, retry=never`, `funnel.py` must reproduce the WATCH-1 0.50× ratified numbers exactly (full-panel bust 0.08%, etc.) — this is the load-bearing correctness check, since it proves the wrapper hasn't silently changed the underlying bust/pass mechanics.
- Hand-computed deterministic-path EV unit tests (a handful of scripted, non-random paths where the correct EV/day can be computed by hand and asserted).
- `run_funnel_sweep.py` — executes the full grid: 3 rungs × 2 retry policies × 3 edge-scenario points × 2 regime halves (36 cells), applying the pinned §5 payout config and the Q-RAIL-1 Phase 4 fee figures.
- `RESULTS.md` — reports every cell's EV/day with bootstrap bands, applies the frozen §6 gate table verbatim, states the verdict (RESOLVED / FALSIFIED / AMBIGUOUS-HOLD) per the pre-registered trigger conditions — **as a mechanical application of the frozen gate, not a judgment call.**

**What Cursor is NOT asked to do:** edit any `core/` file; call `register_search open` (this study is `K=0`, no manifest); touch the c1 rail, `lifecycle_state.json`, or any account/live-execution surface; author or amend the pre-registration's §3/§4 thresholds (frozen — any perceived need to change them is a `NEEDS_CONTEXT`/`BLOCKED — plan-itself-wrong`, not a silent adjustment); build or recommend the deferred policy layer (design doc §7 — out of scope, downstream of this study's verdict); author the Q-FUNNEL-1 closure record (§9 — operator/CC-side, downstream of the RESULTS the harness produces).

---

## §2 — Execution plan

TDD throughout.

### Step 2.1 — Panel + regime-gate reuse scaffold
- **Inputs:** `run_haircut_regime_remc.py`'s import pattern, `run_class_s_c1_scoring.py`, `run_class_s_c1_regime_gate.py`.
- **Action:** `funnel.py` imports the panel-build and regime-gate primitives exactly as the sibling-runner pattern does — no reimplementation of panel loading, bust/pass detection, or the bootstrap machinery.
- **Expected output:** import scaffold + a smoke test confirming the panel loads and the 1.00× reproduction control matches the frozen `REGIME_GATE.md` baseline (same tolerance as `run_haircut_regime_remc.py`'s own `_repro_check`: ≤1.0pp H1 bust, ≤2.0pp bootstrap-95th).
- **Per-step gate:** smoke test green; zero panel-loading logic duplicated from the sibling runner.

### Step 2.2 — Funnel accounting layer (fee + reset recursion)
- **Inputs:** pre-reg §2 EV formula, §4 `MAX_RETRIES=5`, Q-RAIL-1 Phase 4 fee figures.
- **Action:** wrap per-path outcomes with eval-fee/reset-recursion: on `bust_*`, apply the fee schedule and re-draw a fresh path (up to 5 resets for the retry-to-cap policy; 0 for no-retry), accumulating spend and wall-clock days across the chain.
- **Expected output:** module + tests: a fixture path sequence with known bust outcomes produces the hand-computable cumulative spend/days for both retry policies.
- **Per-step gate:** no-retry policy's cumulative spend is always exactly one eval fee; retry-to-cap's is bounded by `6 × eval_fee` (5 resets + original).

### Step 2.3 — Funded-phase continuation
- **Inputs:** pre-reg §5 pinned config, §0.5(B)/(C) resolutions.
- **Action:** on `pass`, continue the daily loop past the frozen `simulate_path` terminus using the funded-phase geometry (floor locked at $100,100, no consistency rule, the Select Flex payout policy: 90/10 split, 5-winning-day cycle at $200/day threshold, 50%-of-total-profit cap at $4,000/payout, loss-recovery-to-net-positive before next payout). Track realized payout events and terminal account state (still funded / busted-post-funding).
- **Expected output:** module + tests: a scripted funded-phase path with known winning days produces the hand-computable payout sequence and terminal value.
- **Per-step gate:** payout arithmetic matches the pre-reg §5 worked examples (e.g., the $52,500-balance/$1,250-payout example) exactly when replayed on equivalent synthetic inputs.

### Step 2.4 — EV/day computation + edge-scenario grid
- **Inputs:** 2.1–2.3, pre-reg §2 formula, the three edge-scenario constructions (§0.5(D) resolution).
- **Action:** compute `EV/day` per the frozen formula, across all 3 rungs × 2 retry policies × 3 edge scenarios × 2 regime halves.
- **Expected output:** `run_funnel_sweep.py` + tests (a small synthetic sweep with known expected EV/day values, sanity-checking the aggregation).
- **Per-step gate:** edge=0 scenario's EV/day is strictly lower than edge=panel-historical's, for every rung (a basic sanity property — more edge should never produce less EV, and a failure here indicates a wiring bug before any real numbers are trusted).

### Step 2.5 — Regression pin (load-bearing correctness check)
- **Inputs:** 2.1–2.4, `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md`.
- **Action:** with `fees=0, funded_value=0 (all payouts valued at 0), retry=never`, run the full sweep at the 0.50× rung and assert the resulting bust/pass numbers match the ratified WATCH-1 numbers within the same tolerance as Step 2.1's smoke test.
- **Expected output:** a named regression test (`test_funnel.py::test_regression_pin_matches_watch1_ratification`) — must be green before Phase 3 runs on real thresholds.
- **Per-step gate:** this is the single most important test in the build. If it fails, the funnel wrapper has silently altered the underlying bust/pass mechanics — halt and return `NEEDS_CONTEXT`, do not proceed to Step 2.6 with a known-wrong wrapper.

### Step 2.6 — Full sweep + gate application + RESULTS.md
- **Inputs:** all prior steps, pre-reg §6 gate table (verbatim).
- **Action:** run the real 36-cell sweep; apply §6's RESOLVED/FALSIFIED/AMBIGUOUS-HOLD trigger conditions mechanically; write `RESULTS.md` reporting every cell's EV/day + bootstrap band, the gate application, and the verdict.
- **Expected output:** `RESULTS.md` + the raw sweep output (JSON, one row per cell).
- **Per-step gate:** the verdict in `RESULTS.md` is a mechanical readout of §6's table against the actual numbers — no interpretation beyond what §6 specifies. If the numbers land in a genuinely ambiguous spot §6 doesn't cleanly cover, report that explicitly rather than picking a verdict.

---

## §4 — Falsifiable hypothesis (parent study's, restated as assertion targets)

No hypothesis is under test in the build itself — this handoff executes the frozen Q-FUNNEL-1 pre-registration. H-FUNNEL-1 and the §6 verdict table (owned by the pre-registration) are restated here because the harness must assert against these pre-registered conditions, never re-derived ones:

**H-FUNNEL-1 (verbatim, pre-reg):** funnel EV per dollar-day varies materially (§3(a)+(b)+(c)) across rungs/retry policies, on ≥1 edge-scenario grid point.
**Falsifier:** EV surface flat within noise / below the 25% economic floor at every grid point.
**AMBIGUOUS-HOLD:** direction reverses H1↔H2, or the funded-payout config can't be applied as pinned.

The harness implements the machinery that makes this verdict assertable; Step 2.6's `RESULTS.md` states the verdict as a mechanical gate readout, and the parent session's closure record (§9, downstream, CC-side) is the actual adjudication artifact.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Substituting a synthetic panel if the real CSVs are absent.** Genuinely tempting — "just use something representative to prove the harness works." Forbidden: the whole point of the regression pin (Step 2.5) is byte-for-byte reproduction of a *real* ratified result; a synthetic substitute would silently produce a harness that looks tested but has never actually been checked against real numbers. This is why §0.0's dispatch-environment check is a hard blocker, not a warning.
- **Amending the pre-registration's §3/§4 thresholds mid-build** because the real numbers "clearly should" use a different cutoff. Forbidden per the pre-reg's own commit-discipline clause and brief-authoring Known Trap #12 — any perceived need to change §3/§4 is `NEEDS_CONTEXT`/`BLOCKED — plan-itself-wrong`, resolved by the operator opening a fresh pre-registration, never a silent in-flight edit.
- **Building the deferred policy layer** (design doc §7) "since the funnel numbers make it obvious what the sizing policy should be." Out of scope — that is a separate, gated future study requiring its own pre-registration, `dd_geometry` instance, and B6 dry-fire re-run. This handoff produces a measurement, not a deployed behavior change.
- **Reimplementing panel-loading, bust/pass detection, or bootstrap math** instead of importing `run_class_s_c1_scoring`/`run_class_s_c1_regime_gate` read-only. Drivers wire; engines compute — any drift between a reimplementation and the real engine is a silent second implementation that would invalidate the regression pin's meaning.
- **Treating the Q-RAIL-1 Phase 4 fee figures as stale and re-deriving new ones from a checkout flow.** Out of scope for this build — the pre-reg explicitly notes this is a non-blocking data point to log-if-different, not re-verify; re-deriving would be scope creep into a different kind of data acquisition this handoff doesn't authorize.
- **The "while I was in there" refactor** of `run_class_s_c1_scoring.py` / `run_class_s_c1_regime_gate.py` / `core/mc/simulation.py`. Log observations under `DONE_WITH_CONCERNS`; touch nothing outside `lab/archive/q_funnel_1_2026-07/`.

---

## §6 — Gate + status return taxonomy

Report EXACTLY one of: `DONE` | `DONE_WITH_CONCERNS` | `NEEDS_CONTEXT` | `BLOCKED — <context-problem | capability-problem | scope-problem | plan-itself-wrong>`.

A `DONE` here means the harness is built, the regression pin passes, and the full sweep ran — it is **never** the Q-FUNNEL-1 study's own final verdict-of-record: the closure record (§9 of the parent brief) is the operator/CC-side adjudication artifact, downstream of this build's `RESULTS.md`.

Closure report format:
```
Status: <...>
§0.0 dispatch-environment check: <PASS (files present) | BLOCKED (files absent, stopped immediately)>
Per-step gates: 2.1 [pass/concern/skip], 2.2 [...], 2.3 [...], 2.4 [...], 2.5 [...], 2.6 [...]
Diffs (files touched): <list — expect only lab/archive/q_funnel_1_2026-07/**>
§0.5 resolutions applied: A=<...>, B=<...>, C=<...>, D=<...>
Regression pin (Step 2.5) result: <pass/fail with numbers>
Sweep verdict from RESULTS.md: <RESOLVED | FALSIFIED | AMBIGUOUS-HOLD | genuinely-unclear-flag>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (after Cursor returns)

**Pass 1 — Spec-compliance:** every Step 2.x output present; diff list contains ONLY `lab/archive/q_funnel_1_2026-07/**`; no `core/` file touched; regression pin (Step 2.5) actually ran and passed, not skipped.
**Pass 2 — Quality:** the frozen thresholds (25%, `MAX_RETRIES=5`) appear literally from the pre-reg, not re-derived; the §5 payout config's numbers match the pinned quotes exactly; the gate application in `RESULTS.md` is mechanical, not editorialized.
**Pass 3 — Consolidated read:** the sweep's 36 cells are internally consistent (edge=0 ≤ edge=panel-historical ≤ or ≥ edge=half-panel as expected per the de-meaning construction); the verdict stated matches what §6's table actually says for the reported numbers.

Only after all three passes does the parent recommend Joshua accept/merge, and only then does Q-FUNNEL-1's own closure record get authored.

---

## §10 — Audit hooks (runnable)

```bash
# Dispatch-environment check ran first, before any other Phase-0 read (grep the Cursor transcript / PR description)
# Expected: §0.0 result stated before any other §0 item is reported

# No core/ file touched
git diff main -- core/ | wc -l
# Expected: 0

# No register_search / ledger mutation
grep -rn "register_search" lab/archive/q_funnel_1_2026-07/
# Expected: no matches

# Regression pin actually present and named
grep -rn "test_regression_pin_matches_watch1_ratification" lab/archive/q_funnel_1_2026-07/
# Expected: at least one match, and it must be a real assertion, not a skip/xfail

# Frozen thresholds appear literally, not re-derived
grep -n "0\.25\|MAX_RETRIES\s*=\s*5" lab/archive/q_funnel_1_2026-07/*.py

# Panel-loading not reimplemented (expect these imports present, not vendored copies)
grep -rn "import run_class_s_c1_scoring\|import run_class_s_c1_regime_gate" lab/archive/q_funnel_1_2026-07/

# Tests + boundaries
pytest -q lab/archive/q_funnel_1_2026-07/
python scripts/check_boundaries.py
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
# Mechanical discipline check on this brief
python scripts/check_brief.py docs/briefs/handoffs/2026-07-21-cursor-handoff-q-funnel-1-funnel-wrapper.md --type cc_handoff

# §0 anchors resolve
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md

# Cursor's closure report uses the four-state taxonomy
grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cursor-return>
```

If Cursor returns `NEEDS_CONTEXT` or `BLOCKED`, this handoff is not complete; re-dispatch (locally, if the §0.0 dispatch-environment check is what failed) per §6.

---

## Related

- Pre-registration (FROZEN): [`Q-FUNNEL-1-verdict-preregistration.md`](../pre-registration/Q-FUNNEL-1-verdict-preregistration.md)
- Scoping brief: [`Q-FUNNEL-1-contract-funnel-ev-scoping.md`](../rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md)
- Design doc: [`2026-07-21-q-funnel-1-contract-ev-design.md`](../../superpowers/specs/2026-07-21-q-funnel-1-contract-ev-design.md)
- Sibling-runner pattern this build follows: [`run_haircut_regime_remc.py`](../../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/run_haircut_regime_remc.py)
- Routing ADR (Test 0 / dispatch-environment discipline): [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md)
