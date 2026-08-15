# Cursor Handoff — Stage-4→7 real-data drivers (OOS eval → matrix → gates → realism, incl. the 0-survivor path)

**Date:** 2026-07-13
**Parent session:** Claude Code operator session (Joshua + Claude) — the same session that executed the DISC-CAMP-0 first pull, bound K_DSR = 3,177 / block_size = 3, and ran Stage-3 mining to its all-null result. **Cursor builds the Stage-4→7 real-data drivers** (the plumbing between the frozen Stage-3 candidates and the landed Stage-5/6/7 engines, which today have only synthetic callers).
**Spawn target:** Cursor (research venv — `.venv-research`; `stumpy`/`ruptures`/`pycatch22`/`arch`/`skfolio`/`databento` live there, not in `pyproject.toml`)
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step)
**Parent question:** DISC-CAMP-0 §7 Stages 4–7 traversal (campaign `disccamp0_gc_2010_18`) + general Gen-2 pipeline completion — every future discovery campaign reuses these drivers.
**Authority:** Joshua (CEO). No commit/merge without Joshua's go. **NO `db_fetch pull` / `db_fetch estimate`, NO `register_search open`/`close`, NO Databento client construction anywhere in new code** — data acquisition and ledger mutations are operator-side only. Build + test on synthetic fixtures; real-data paths must be structurally gated (see §2.3).

**Workspace pin (load-bearing):** build on branch **`claude/disc-camp-0-first-pull-ce9c73`** (pushed; PR #360), at or after commit **`c783533`** (2026-07-13, "DISC-CAMP-0 Stage-3 mining executed"). Everything §0 lists exists at that commit. Do NOT build on `main` — the Stage-3 artifacts and the miner stage-flags are not there yet.

> **Binding context (read first — this changes what "Stage 4" means for THIS campaign).**
> Stage-3 mining executed 2026-07-13 and closed **all-null**: 6 candidates mined
> (motif+discord × m∈{30,60,90}), **0/6 cleared the IS cost-law** (mean net trade
> −0.4…−2.2 bp vs the +9.56 bp 4× MGC hurdle; permutation p = 1.0 for all six), and the
> `register_search` manifest is **CLOSED with 0 survivors** at every tier. Per pre-reg §2,
> **K_SPA will bind 0** — no candidate reaches the Stage-4 OOS matrix. Consequences for
> this build: (a) the drivers' **0-survivor path is the one DISC-CAMP-0 will actually
> exercise** (a clean, artifact-producing "empty traversal" is a first-class deliverable,
> not an edge case); (b) the with-survivors path is built for the NEXT campaign and proven
> on synthetic fixtures; (c) whether DISC-CAMP-0 runs the formal 0-column traversal at all
> (vs a direct §6 FALSIFIED close) is an **operator disposition owed at closure — not
> Cursor's call and not this build's blocker.**

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any code)

Cursor: read each item and post a read-report in your first response **before** writing code. If repo state contradicts a §2 assumption, return `NEEDS_CONTEXT` with the discrepancy quoted.

- [`docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md`](../pre-registration/DISC-CAMP-0-preregistration.md) — report §2 (bound K_DSR = 3,177; K_SPA status note; **V = 1/n unconditional pin**; power disclosure), §3 (gate table + the **operator-CONFIRMED de-drift + zero-edge SPA benchmark rule**), §4 (**bound `block_size` = 3** + the recorded lag-7–13 ACF re-exceedance), §5 ($0.00 summed estimate), §1 era split (IS 2010-06-06:2018-12-31; OOS 2019-05-06:2026-07-01, `--end` exclusive ⇒ last OOS bar 2026-06-30).
- [`docs/ltm/briefs/rnd-pipeline/DISC-CAMP-0-shakedown.md`](DISC-CAMP-0-shakedown.md) — report the Status line, §7 Stages 4–8 verbatim, and the §8 Stage-3 execution record.
- `lab/analysis/harvest/disccamp0_gc_2010_18/stage3_frozen_rules.json` — report: candidate count (expect 6), the per-rule fields (`candidate_id, kind, m, shape, trigger, direction, horizon, shape_hash, source_index`). **These serialized rules are the ONLY candidate source for Stage 4 — shapes are data, never re-mined or re-fit.**
- `lab/analysis/harvest/disccamp0_gc_2010_18/stage3_report.json` — report `frozen_inputs` (incl. `cost_price_input_is_mean_close` = 1355.12 — the IS cost-price convention §0.5(B) mirrors) and the per-candidate `cost_law_pass` values (expect all false).
- `discovery_manifests/disccamp0_gc_2010_18.json` — report `status` (expect `closed`), `K` (expect 3177), `results.n_pass_bh` (expect 0).
- `lab/analysis/harvest/disccamp0_gc_2010_18/series.py` — report `cached_df` signature (symbols/start/end/phase/outright_re parameters), `volume_lead_stitch`, `within_contract_log_returns`. **The MGC OOS loader extends THIS module's conventions — same stitch, same return adjustment.**
- `lab/analysis/harvest/disccamp0_gc_2010_18/run_stage3.py` — report the integrity-gate pattern (recomputed T → bracket must equal manifest K) and the frozen-inputs block. Stage-4+ drivers mirror this shape.
- `lab/discovery/stage24_runner.py` — report `run_gate_on_survivors` (the V=1/n wiring pattern) and `run_synthetic_stage24`'s `bind_real_k` refusal — the gating pattern §2.3 mirrors. **Do not modify this module's synthetic path; `test_bind_real_k_refused` pins it.**
- `lab/discovery/matrix_emit.py` — report `emit_stage4` signature (esp. `dedrift`, `underlying_ret`, `zero_benchmark`, `era_bounds`) and `_align_bar_matrix`'s de-drift transform (subtract exposure-matched mean of `underlying_ret` on active bars). **The real campaign runs `dedrift=True` per the confirmed benchmark rule.** Also report `trade_matrix_for_gate`.
- `lab/discovery/motif_rules.py` — report `FrozenRule` fields + `evaluate_rule` semantics (returns-series input, trailing z-distance < trigger ⇒ enter next bar, hold `horizon` bars, net of `cost_frac_per_rt`, no re-entry overlap). The Stage-4 OOS evaluation calls exactly this — no reimplementation.
- `lab/discovery/miner.py` — report the NEW `run_stumpy`/`run_ruptures` flags (landed `c783533`) — §0.5(A)'s OOS-labels option (i) uses `run_stumpy=False`.
- `lab/discovery/realism_mgc.py` + `tests/` for it — report the public API: `ratio_clause` (net-MGC ≥ 0.8× GC-gross), `hurdle_clause`, `rt_cost_frac`, `reconstruct_gross_gc` (bit-exact RT-cost add-back — **this is the pinned GC-gross semantics**), `mgc_oos_returns`/`oos_timestamps` (grid alignment), `verify_rule_provenance`. The Stage-7 driver WIRES this engine; it does not reinterpret the predicate.
- `lab/research_utils/universe_gate.py` — report `run_universe_gate` full signature (esp. `var_trials`, `cumulative_k`, how block size enters SPA — if it is derived internally via `acf_block_size`, report that and see §0.5(D)), `load_returns_matrix` contract, `load_thresholds_from_prereg` (parses the pre-reg §3 summary line — confirm it still parses the amended file).
- `lab/research_utils/temporal_consistency.py` — report `run_temporal_battery` signature (edge series + calendar stamps + thresholds + optional labels; SKIPPED-not-silent-pass semantics for 6c).
- `lab/databento_fetch/db_fetch.py` — report `_cache_path` mechanics (campaign/phase era-tagging) ONLY. **New drivers may import `_cache_path` to LOCATE caches; they must never construct `db.Historical` or call any metadata/timeseries endpoint.**
- `scripts/check_boundaries.py` — report the import contract (lab→{core,governance,lab}; `lab↔ops` isolation).
- `git log -1 --format='%h %ci' -- lab/analysis/harvest/disccamp0_gc_2010_18/stage3_frozen_rules.json` — report the anchor (expect `c783533`).

After Phase 0: post the read-report; proceed to §2 only once §0.5 is resolved.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Parent-recommended defaults are stated; confirm or challenge in the Phase-0 response. Set `Status: NEEDS_CONTEXT` until resolved.

- **(A) OOS regime labels for Stage-6c.** The pre-reg §3 6c row takes *externally-supplied* ruptures/HMM slices as test conditions, `SKIPPED` (not silent pass) if none supplied. The IS-fit daily PELT found **1 segment / no breaks** (frozen penalty 10.0), so broadcasting IS labels gives a degenerate single slice. **Recommended default (i):** run ruptures PELT (same frozen penalty 10.0, `run_stumpy=False`) fresh on the stitched **OOS daily** returns — candidate-blind conditioning, legal under Q-REGIME-COND-1 (labels never filter). If OOS also yields 1 segment, 6c reports `SKIPPED`/degenerate honestly. Alternative (ii): supply no labels ⇒ `SKIPPED`. **Do NOT retune the penalty in either case** — the 1-segment outcome is a defect-log observation, not a knob.
- **(B) Stage-4 OOS cost-price input.** Stage-3 used the IS-mean stitched close ($1,355.12) for the MGC hurdle fraction. **Recommended default:** mean stitched **MGC OOS** close (same exposure-matched convention, OOS era), recorded in the emitted meta. Confirm.
- **(C) Stage-7 GC-gross semantics.** `realism_mgc.reconstruct_gross_gc` pins gross = net + frozen RT-cost add-back (bit-exact). Report the engine's semantics at Phase 0 and wire them as-is; ASK only if the engine leaves something genuinely open. Do not invent an alternative gross definition.
- **(D) SPA block size wiring.** The pre-reg §4 **bound `block_size` = 3**. Report how `run_universe_gate` sources its bootstrap block size (internal `acf_block_size` recomputation vs a parameter). If internal-only, the driver must record BOTH the bound 3 and the gate's internally-derived value in its report artifact and flag any mismatch — **do not silently let either win**; surface to operator.
- **(E) 0-survivor artifact shape.** `load_returns_matrix` requires candidate columns, so a 0-column matrix cannot round-trip. **Recommended default:** the Stage-4 driver, on 0 survivors, emits `<run_id>__stage4_matrix.meta.json` (with `k_spa: 0`, provenance of the kill: 6 candidates, all `cost_law_pass: false`) + a `<run_id>__stage45_skipped.json` marker recording that Stage-5/6 are structurally empty — and the Stage-5/6 driver, seeing that marker, writes a `SKIPPED (0 candidates)` gate report rather than crashing or fabricating columns. Propose the exact shape in the Phase-0 report.

---

## §0.5 — Answers (parent-resolved, 2026-07-13; supersedes the NEEDS_CONTEXT hold)

Cursor's Phase-0 read-report was accepted: artifacts and bound integers match the pin. All forks resolved; proceed to §2.

**Workspace / build root (resolved — do NOT build inside the session worktree).** Cursor's root workspace on `main` is pre-`c783533`, correct observation — but `.claude/worktrees/disc-camp-0-first-pull-ce9c73` is the operator session's LIVE worktree (Windows file-lock + collision risk; repo-hygiene scar). Instead: `git fetch origin && git checkout -b cursor/stage4-7-drivers origin/claude/disc-camp-0-first-pull-ce9c73` in Cursor's own workspace — branch off the pushed branch at or after `6094a43`. Do **not** push commits onto `claude/disc-camp-0-first-pull-ce9c73` itself (PR #361 stays reviewable as-is); deliver on the new branch.

**(A) OOS regime labels = option (i), CONFIRMED, with one derivation pin.** Fresh ruptures PELT (frozen penalty 10.0, `run_stumpy=False`) on the stitched MGC OOS **daily** returns, candidate-blind; a 1-segment outcome ⇒ 6c reports `SKIPPED`/degenerate honestly; the penalty is never retuned. **Derivation pin:** the frozen §5 estimate list contains NO MGC `ohlcv-1d` pull — the OOS daily leader AND the daily return series are **derived from the MGC 1h cache by per-UTC-day aggregation** (leader = max summed hourly volume per day per outright; daily series = within-contract log-diff of the leader's last hourly close per day). No new pull, no new estimate — stays inside the frozen budget.

**(B) Stage-4 cost price = mean stitched MGC OOS close (from the 1h stitched series), CONFIRMED.** Recorded in the emitted meta, mirroring Stage-3's IS-mean convention (`cost_price_input_is_mean_close: 1355.12`).

**(C) Stage-7 gross semantics = `reconstruct_gross_gc` as-is, CONFIRMED.** Gross = net + bit-exact frozen RT-cost add-back; the driver wires, never reinterprets.

**(D) Block size, CONFIRMED with precedence + expectation pins.** `run_universe_gate` accepts `block_size: int | None` (verified at `universe_gate.py:325-352`; `None` ⇒ internal `acf_block_size` on the pooled candidate mean series). **Pass the bound `block_size=3` explicitly — the pre-reg §4 binding governs.** ALSO compute the gate's internal `acf_block_size(...)` value and record both in the gate report. **A mismatch is EXPECTED, not an error** — the bound 3 comes from the IS GC 1h stitched-return ACF; the internal value would come from a different series (pooled OOS candidate returns). Record + surface; never substitute.

**(E) 0-survivor artifact shape, CONFIRMED.** `<run_id>__stage4_matrix.meta.json` with `k_spa: 0`, `k_dsr: 3177`, `v_rule: "1/n"`, era bounds, and full kill provenance (all 6 candidates with `cost_law_pass: false` + IS p-values) so the closure note cites one artifact; plus `<run_id>__stage45_skipped.json` marker; Stage-5/6/7 drivers detect the marker, write `SKIPPED (0 candidates)` reports, and exit 0 (a crash on this path is the §4 AMBIGUOUS-HOLD trigger — first-class, tested).

Standing walls unchanged: no pulls/estimates, no ledger calls, no frozen-artifact or engine edits, no threshold literals.

---

## §1 — Context

All engine pieces are landed and tested: Stage-5 (`universe_gate.py`), Stage-6 (`temporal_consistency.py`), Stage-7 (`realism_mgc.py`, PR #350, 16/16), the Stage-2/4 synthetic runner (PR #344), and — as of `c783533` — the real Stage-3 driver with its frozen-rule artifacts. **What does not exist is the real-data path from a frozen candidate set to those engines:** nothing loads `stage3_frozen_rules.json`, nothing builds the MGC OOS stitched series, nothing emits a real Stage-4 matrix (with the operator-confirmed de-drift), nothing wires the bound integers (K=3,177, V=1/n, block_size=3) into a real gate run, and nothing exercises Stage 7 on real candidates. DISC-CAMP-0's all-null result means the first real consumer is the **0-survivor traversal**; the with-survivors path is proven on synthetic fixtures and inherited by every future campaign (the stack-ADR's whole point).

**What Cursor is asked to produce** (general machinery in `lab/discovery/`, campaign glue in `lab/analysis/harvest/disccamp0_gc_2010_18/`):
- A frozen-rule loader (`stage3_frozen_rules.json` → `FrozenRule` objects, `shape_hash` re-verified).
- MGC OOS series support extending `series.py` conventions (MGC outright regex, OOS window, `phase="oos"`).
- `run_stage4.py` — cache-gated real OOS evaluation of frozen rules → K_SPA bind → `emit_stage4(dedrift=True, ...)` bundle; first-class 0-survivor path per §0.5(E).
- `run_stage5_6.py` — matrix → `run_universe_gate` (cumulative_k=3,177, `var_trials=1/n`) + `run_temporal_battery` (labels per §0.5(A)); SKIPPED path on the 0-survivor marker.
- `run_stage7.py` — survivors → `realism_mgc` predicate; report artifact.
- Synthetic-fixture tests for every driver (with-survivors AND 0-survivor cases), boundary-clean, research-venv-only.

**What Cursor is NOT asked to do:** pull or estimate ANY data (no Databento client construction — grep-audited, §10); call `register_search open`/`close`; re-run or modify Stage-3 mining; alter any frozen rule, bound integer, threshold, or pre-reg text; modify `universe_gate.py` / `temporal_consistency.py` / `realism_mgc.py` / `stage24_runner.py`'s synthetic path / `dd_protection` / `portfolio_mc` / anything in `core/`; add research deps to `pyproject.toml`; decide the DISC-CAMP-0 closure disposition; wire anything toward live execution (R6 = NO-GO).

---

## §2 — Execution plan

TDD throughout; every step's tests run offline on synthetic fixtures (no cache, no network).

### Step 2.1 — MGC OOS series support
- **Inputs:** `series.py` (conventions), pre-reg §1 OOS window.
- **Action:** extend the campaign series module with `MGC_OUTRIGHT_RE = ^MGC[FGHJKMNQUVXZ]\d{1,2}$`, OOS constants (`2019-05-06` → `2026-07-01`, end-exclusive), and an OOS loader (`cached_df(schema, symbols="MGC.FUT", phase="oos", ...)` + stitch + within-contract returns). Fixture-injectable: the stitch/returns functions must accept pre-built frames so tests never need a cache.
- **Expected output:** extended module + tests (synthetic hourly/daily frames with a known leader schedule and one roll; assert stitch membership + roll-boundary return correctness).
- **Per-step gate:** tests green offline; zero Databento client references.

### Step 2.2 — Frozen-rule loader
- **Inputs:** `stage3_frozen_rules.json`, `motif_rules.FrozenRule`, `realism_mgc.verify_rule_provenance` (pattern).
- **Action:** loader that reconstructs `FrozenRule` objects and **re-verifies each `shape_hash` against the deserialized shape bytes** (refuse on mismatch — a mutated shape is a corrupted candidate, not a warning).
- **Expected output:** loader + round-trip test (serialize a synthetic rule → load → hash match; corrupted-shape fixture → hard error).
- **Per-step gate:** hash tamper-test fails loudly.

### Step 2.3 — `run_stage4.py` (real OOS eval → K_SPA → emit; 0-survivor first-class)
- **Inputs:** 2.1 + 2.2, `evaluate_rule`, `emit_stage4`, §0.5(B) cost price, §0.5(E) shape.
- **Action:** gated like `bind_real_k` — refuses unless the MGC OOS cache exists AND an explicit operator flag is passed (absent cache or flag ⇒ clean refusal message, exit non-zero). With the gate open: evaluate ONLY IS-cost-law survivors on the MGC OOS series (net of the §0.5(B) hurdle), bind `k_spa = len(survivors)`, emit via `emit_stage4(dedrift=True, underlying_ret=<OOS stitched returns>, zero_benchmark=True, era_bounds=<real>, ...)`. For DISC-CAMP-0's actual state (0 survivors) emit the §0.5(E) bundle.
- **Expected output:** driver + tests: synthetic with-survivors fixture round-trips through `load_returns_matrix`; 0-survivor fixture emits meta + skipped-marker; gate-refusal test (no cache/flag ⇒ refuse).
- **Per-step gate:** `load_returns_matrix(<emitted csv>)` loads the with-survivors fixture; meta records `k_spa ≠ k_dsr`, `v_rule="1/n"`, `dedrift=true`.

### Step 2.4 — `run_stage5_6.py` (gates + battery on the emitted bundle)
- **Inputs:** 2.3 bundle, `load_thresholds_from_prereg`, `run_universe_gate`, `run_temporal_battery`, §0.5(A)/(D).
- **Action:** load thresholds from the pre-reg file (never hardcode); run the gate with `cumulative_k=3177`, `var_trials=1/n_selected`; record the §0.5(D) block-size cross-check; run the battery with OOS calendar stamps + §0.5(A) labels. On the 0-survivor marker: write the `SKIPPED (0 candidates)` report artifact and exit 0.
- **Expected output:** driver + tests (synthetic bundle promotes/rejects correctly through the REAL gate; 0-survivor marker ⇒ SKIPPED report).
- **Per-step gate:** no threshold literal appears in the driver (grep); gate detail records `cumulative_k` and `var_trials` matching the bound values.

### Step 2.5 — `run_stage7.py` (realism predicate on survivors)
- **Inputs:** 2.3 trades sidecar, `realism_mgc` engine, §0.5(C).
- **Action:** wire survivor per-trade nets into `reconstruct_gross_gc` → `ratio_clause` + `hurdle_clause`; emit a per-survivor pass/fail report incl. `identity_fill_coincidence_note` and `effective_bar_disclosure_bp`. 0-survivor ⇒ `SKIPPED` report.
- **Expected output:** driver + tests (fixture survivor above/below the 0.8×/4× predicates resolves correctly).
- **Per-step gate:** engine functions called as-is; no reimplemented predicate arithmetic in the driver.

### Step 2.6 — End-to-end fixture proof + boundaries
- **Inputs:** all prior steps.
- **Action:** one synthetic end-to-end test: fixture OOS bars + a planted surviving rule → 2.3 emit → 2.4 gate (real `universe_gate`) → 2.5 realism — plumbing asserted (artifact chain, bound-integer propagation), promotion not required. Plus the 0-survivor end-to-end (emit → SKIPPED → SKIPPED). `check_boundaries` green; full `pytest tests/` green in `.venv-research`.
- **Per-step gate:** both e2e paths green offline; no `ops` import; no Databento client construction (grep).

### Step 2.7 — Closure report
Post the §6-format closure report. **Do not** author the DISC-CAMP-0 closure note — that is the operator's §9 artifact, downstream of the disposition call.

---

## §4 — Falsifiable hypothesis (parent campaign's, restated as assertion targets)

No hypothesis is under test in the build itself — this handoff executes frozen campaign plumbing. The parent campaign's H-CAMP-0 and verdict table (owned by [`DISC-CAMP-0-shakedown.md`](DISC-CAMP-0-shakedown.md) §4/§6) are restated here because the drivers must assert against these pre-registered conditions (via `load_thresholds_from_prereg`), never re-derived ones:

**H-CAMP-0 (verbatim):** if every pipeline stage executes to a recorded artifact AND ≥1 mined candidate clears the §6 gate on the 2019+ OOS era, the pipeline is validated *and* a candidate found; otherwise the pipeline is validated by the clean traversal and the candidate hypothesis is **FALSIFIED** (banked K, null close).
**Falsifier / Reject (FALSIFIED):** pipeline traverses clean AND zero candidates clear on the OOS era — **the expected outcome, and a shakedown SUCCESS**; with the Stage-3 all-null (0/6 past cost-law, K_SPA→0) this is the live trajectory.
**Accept (RESOLVED):** ≥1 candidate clears SPA + DSR ≥ 0.95 + consistency + MGC realism — structurally unreachable for THIS campaign (empty candidate set), preserved for future campaigns reusing these drivers.
**AMBIGUOUS-HOLD:** a pipeline stage fails to execute (genuine process bug blocks traversal) — a driver crash on the 0-survivor path lands HERE, which is why §0.5(E)/§2.3–2.4 make that path first-class.

The drivers implement the machinery that makes these verdicts assertable; the verdict itself is the operator's closure call.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Running the MGC pull "since it's estimated $0.00."** The estimate being free does not make the pull Cursor's to fire — freeze-ordering attestations and the closure disposition are operator-side. Build the gate; never open it.
- **Re-tuning after seeing the all-null.** Six dead candidates make `trigger_quantile=0.05` / `horizon=3` / `PELT penalty=10.0` scream to be "fixed." Post-result parameter movement is exactly what voids a campaign (brief-authoring Known-Trap #12; campaign §5). The all-null IS the expected shakedown outcome. Any re-parameterization is a fresh pre-registered campaign, full stop.
- **Padding the 0-survivor matrix with the cost-law-killed candidates** "so Stage 5 has something to test." K_SPA's definition (post-kill columns) is frozen in pre-reg §2; the kill is a kill.
- **Reimplementing engine math in drivers** (SPA/DSR/PBO/battery/realism predicates). Drivers wire; engines compute. Any drift between a driver's arithmetic and the engine's is a silent second implementation.
- **Silently resolving the §0.5(D) block-size question** by picking whichever value is easier to wire. Record both, flag mismatch, surface.
- **Amending §6/§2 gates mid-build.** If the plan is structurally wrong, return `BLOCKED — plan-itself-wrong`.
- **The "while I was in there" refactor** of `stage24_runner.py`/`miner.py`/`matrix_emit.py`. Log observations under `DONE_WITH_CONCERNS`; touch nothing outside §2 scope.

---

## §6 — Gate + status return taxonomy

Report EXACTLY one of: `DONE` | `DONE_WITH_CONCERNS` | `NEEDS_CONTEXT` | `BLOCKED — <context-problem | capability-problem | scope-problem | plan-itself-wrong>`.

A `DONE` here means the drivers are built and fixture-proven — it is **never** a campaign verdict: RESOLVED / FALSIFIED / AMBIGUOUS-HOLD belong to the operator's §4-conditioned closure call, downstream of this build.

Closure report format:
```
Status: <...>
Per-step gates: 2.1 [pass/concern/skip], 2.2 [...], 2.3 [...], 2.4 [...], 2.5 [...], 2.6 [...]
Diffs (files touched): <list>
§0.5 resolutions applied: A=<i|ii>, B=<...>, C=<...>, D=<...>, E=<shape>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (after Cursor returns)

**Pass 1 — Spec-compliance:** every Step 2.x output present; diff list contains ONLY §2-scoped files; no engine modules touched; no pyproject change; gate-refusal paths present in 2.3.
**Pass 2 — Quality:** bound integers (3,177 / 1/n / 3) propagate literally from the pre-reg/manifest, not from re-derivation; hash tamper-test genuinely fails; de-drift ON in the real path and OFF nowhere it should be on; 0-survivor artifacts match §0.5(E) as resolved.
**Pass 3 — Consolidated read** across all diffs (multi-step handoff): the driver chain's artifact names/paths agree end-to-end; the same stitch feeds every stage.

Only after all three passes does the parent recommend Joshua accept/merge — and the real 0-column traversal (if the operator disposition picks it) runs operator-side, never in Cursor's session.

---

## §10 — Audit hooks (runnable)

```bash
# No data acquisition anywhere in new code (expect: no matches in new drivers)
grep -rn "Historical(\|get_range\|get_cost\|metadata\." lab/analysis/harvest/disccamp0_gc_2010_18/run_stage4.py lab/analysis/harvest/disccamp0_gc_2010_18/run_stage5_6.py lab/analysis/harvest/disccamp0_gc_2010_18/run_stage7.py

# No ledger mutation (expect: no matches)
grep -rn "register_search" lab/analysis/harvest/disccamp0_gc_2010_18/run_stage4.py lab/analysis/harvest/disccamp0_gc_2010_18/run_stage5_6.py lab/analysis/harvest/disccamp0_gc_2010_18/run_stage7.py

# Frozen artifacts untouched (expect: empty)
git diff c783533 -- lab/analysis/harvest/disccamp0_gc_2010_18/stage3_frozen_rules.json lab/analysis/harvest/disccamp0_gc_2010_18/stage3_report.json discovery_manifests/disccamp0_gc_2010_18.json docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md

# Engines untouched (expect: empty)
git diff c783533 -- lab/research_utils/universe_gate.py lab/research_utils/temporal_consistency.py lab/discovery/realism_mgc.py

# Locked core untouched (expect: empty)
git diff c783533 -- core/config/params.toml core/dd_protection.py core/portfolio_mc.py

# Thresholds come from the pre-reg file, not literals (expect: no matches)
grep -n "0\.95\|0\.05\|0\.5" lab/analysis/harvest/disccamp0_gc_2010_18/run_stage5_6.py | grep -v load_thresholds

# Tests + boundaries
PYTHONPATH=lab python -m pytest tests/ -q   # .venv-research
python scripts/check_boundaries.py
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
# Mechanical discipline check on this brief
python scripts/check_brief.py docs/briefs/rnd-pipeline/2026-07-13-cursor-handoff-stage-4-7-drivers.md --type cc_handoff

# §0 anchors resolve at the pinned commit
git log -1 --format='%h %ci' -- lab/analysis/harvest/disccamp0_gc_2010_18/stage3_frozen_rules.json   # expect c783533
git show c783533:discovery_manifests/disccamp0_gc_2010_18.json | grep '"status"'             # expect "closed"

# Cursor's closure report uses the four-state taxonomy
grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cursor-return>
```

If Cursor returns `NEEDS_CONTEXT` or `BLOCKED`, this handoff is not complete; re-dispatch per §6.

---

## Related

- Prior handoff in this lineage (structure + §0.5 conventions): [`2026-07-12-cursor-handoff-stage-2-4-runner.md`](2026-07-12-cursor-handoff-stage-2-4-runner.md) (delivered PR #344)
- Campaign narrative: [`DISC-CAMP-0-shakedown.md`](DISC-CAMP-0-shakedown.md) · Binding freeze: [`DISC-CAMP-0-preregistration.md`](../pre-registration/DISC-CAMP-0-preregistration.md)
- DSR K/V rule: [`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) (`Accepted`)
- Stage-7 engine landing: PR #350 (`lab/discovery/realism_mgc.py`)
