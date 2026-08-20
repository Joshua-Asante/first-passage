# Claude Code / Cursor handoff — parameterize the Aegis→6J 3-leg composed engine's risk allocation (engineering-only, no new measurement)

**Status:** ready to dispatch
**Authority:** operator direction 2026-08-20 ("hand off the engineering fix... to Cursor"), scoped by operator election ("Engineering-only, no new number") after a J14 conflict was surfaced and flagged before any spec was written.
**Layer:** `lab/analysis/` research engineering only. **No `core/`, Pine, allocation, `dd_protection`, rail, K ledger, or live-risk surface touched. $0. Nothing armed.**

---

## §0 — Rule 0 reads (this session, verified before this handoff was written)

- [`ops/instruments/6J.md`](../../../ops/instruments/6J.md) J13/J14 — read in full (**correction, post-dispatch**: an earlier draft of this document mis-cited the risk-bracket closure as "J15" throughout; the verbatim text "THE RISK BRACKET IS CLOSED" lives in **J14**, not J15 — J15 is the unrelated "trade Aegis more frequently" blending-bound closure; caught by Cursor's own plan-mode Phase-0 check, verified and corrected here). J14: a separate, already-validated 3-leg composed harness (`aegis1p_3leg_rescore_2026-07-27`) exists, distinct from the Trap #11-constrained Q-COMPOSE-1 breadth engine; controls reproduce published 2-leg pins to 0.00pp; gating result at Aegis risk=1.00%: `Tradeify_Select_100K` **10.96% FAIL**, `Tradeify_Select_50K` **3.78% FAIL**, `MFFU_Rapid_50K` **3.54% FAIL**. J14: the Aegis risk-bracket question is **explicitly closed** — *"no further risk-arm measurement is owed; any future re-open requires new mechanism evidence, not a new parameter."* This is why this packet is scoped engineering-only — see §5.
- `lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/RESULTS.md` — read in full. Runner script `run_aegis1p_rescore.py` is referenced but **absent from the working tree** — pruned by the Great Prune (`git log -- <dir>` shows commit `283d1de`, "drop closed-campaign harnesses/panels from lab/analysis; keep RESULTS*/PREREG*/CARD"). Retrieved this session via `git show pre-prune-2026-08-08:lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/run_aegis1p_rescore.py` — confirmed readable, full source below informs §2.
- The retrieved script itself, read in full this session. Load-bearing lines: `AEGIS_RISK = 0.0100` (module constant, hardcoded); `AEGIS_EXPECT_1R = {"dollars": 2163.57, "n": 7, "scale": 0.924398}`; `ALLOCS_3 = {"striker": 0.0070, "striker_nas100": 0.0037, AEGIS_LEG: AEGIS_RISK}`; `CONTROL_PINS`/`CONTROL_TOL = 0.0015`.
- **The `scale`-coupling question is already resolved — do not re-derive, just implement as specified.** Read `build_scaled_panel` in `lab/analysis/c1/geofit_iid_sufficiency_power_2026-08-15/run_class_s_c1_scoring.py:269-301` directly. `scale` is **always freshly computed** as `allocations[strat] * ACCOUNT / r_dollars`, where `r_dollars` is derived independently from the CSV panel itself (`pin_r_basis`) — it does **not** come from `AEGIS_EXPECT_1R["scale"]`. That field is used only as a drift **guard**: if `expect_1r[strat]["scale"]` is present, the freshly-computed `scale` must match it within `SCALE_TOL = 0.0005` or the call raises `NeedsContext` (line 296-300). Consequence: `scale` is already a correct linear function of `AEGIS_RISK` with zero code changes needed to that math — the parameterization work is purely about making `AEGIS_RISK` settable and threading it into `ALLOCS_3`. The only thing to get right: since this packet's validation run **only ever executes at the default `0.0100`** (§3, forbidden to run at any other value), the `expect3[AEGIS_LEG]` dict's `"scale": 0.924398` guard pin stays byte-identical to the original at that default — do not touch it, do not generalize it, do not add logic to recompute it for other risk levels (there is no code path in this packet that would ever need that).
- [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md) — this packet's routing: `lab/analysis/` is not a locked surface (test 1 clear); spec is freezable without mid-build judgment calls (test 2 — see §2's explicit fallback for the one genuine ambiguity); estimated build > 1hr / >3 files plausible (test 3). Standard single-Cursor-handoff routing, not a fleet (only one packet).
- Vendor-data note: the 6J CSV panels this script reads (`Aegis_6J1_CME_6J1!_2026-07-27_ac331.csv` + the Striker MYM/MNQ byte-pinned exports `15d8b`/`beabf`) are gitignored and **absent from this worktree** (confirmed via `find`). Located this session at: `C:/Users/joshu/Downloads/Aegis_6J1_CME_6J1!_2026-07-27_ac331.csv`, `C:/Users/joshu/multi_firm_operations/core/data/tv_exports/cme/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv`, `C:/Users/joshu/multi_firm_operations/core/data/tv_exports/cme/Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv`. **This packet must run from a LOCAL worktree with access to these files, not a cloud environment** (`cursor-fleet` skill Test-0: vendor bytes → local, never cloud) — the orchestrator stages them into this packet's own `inputs/` directory (via `dispatch_cursor.ps1 -Copy`) before dispatch; Cursor's job is only to have the parameterized script read from `inputs/` relative to its own directory, matching the original script's `_HERE / "inputs" / <filename>` convention.

---

## §0.9 — Phase-0 staleness check (run these before touching anything)

```bash
ls lab/analysis/c1/aegis3leg_engine_param_2026-08-20/run_aegis1p_rescore_parameterized.py 2>/dev/null && echo "ALREADY EXISTS -- STOP, return DONE with the commit that added it"
git log --oneline -- ops/instruments/6J.md | head -1   # confirm J13/J14 haven't been superseded since this packet was authored
grep -n "THE RISK BRACKET IS CLOSED" ops/instruments/6J.md || echo "J14's closure language has changed or moved -- STOP, return NEEDS_CONTEXT, this packet's whole scope rationale depends on it still reading this way"
git log --oneline -- "lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/*" | head -3   # confirm no newer composed-gate work has landed on this campaign since 2026-08-20
```

If any staleness check fails its expected condition, stop and return the state noted above rather than proceeding on stale premises.

## §1 — Context

`ops/instruments/6J.md` J13 named two admissible routes to test Aegis→6J's composed-book behavior at the deployed WATCH-1 (0.50×) lifecycle scale, distinct from the Trap #11-constrained Q-COMPOSE-1 breadth engine. Investigation this session found the cleaner of the two isn't "extend a 2-leg engine to 3 legs" (J13's route (a)) — it's that a **separate, already-correct, already-validated 3-leg harness already exists** (`aegis1p_3leg_rescore_2026-07-27`), just hardcoded to one risk level (1.00%) it was pre-registered to test. But a **separate standing ruling** (J14) explicitly closed the risk-bracket question and bars re-measuring at a new risk% without new mechanism evidence — a bar this packet does not attempt to clear. Operator election: build the engineering *capability* now (so a future, evidence-backed reopening can fire fast), without producing any new measurement today.

## §2 — Frozen scope

**Do:**
1. Retrieve the pruned runner: `git show pre-prune-2026-08-08:lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/run_aegis1p_rescore.py` and land it, **unmodified**, at a **new** path: `lab/analysis/c1/aegis3leg_engine_param_2026-08-20/run_aegis1p_rescore_ORIGINAL.py` (reference copy — do not edit this file; it is provenance, never executed on its own).
2. **Import-path resolution (pre-resolved, post-dispatch correction — verified directly, not guessed).** The retrieved original's `_SCORING = _ROOT / "lab" / "analysis" / "c1" / "class_s_candidate1_scoring_2026-07-15"` path is **dead**: confirmed this session that directory holds only `.gitignore` + three `.md` files, zero `.py` — the Great Prune removed the harness. The live successor is `lab/analysis/c1/geofit_iid_sufficiency_power_2026-08-15/run_class_s_c1_scoring.py` (same `build_scaled_panel`/`C1_ALLOCS`/`C1_STRATS` code, relocated post-prune — already the file §0's scale-coupling verification read directly). The **parameterized fork** (step 3 below) retargets `_SCORING` to the live path so it can actually import and run; the **ORIGINAL** reference copy keeps its dead import untouched, since it is provenance only and is never executed.
3. Create `lab/analysis/c1/aegis3leg_engine_param_2026-08-20/run_aegis1p_rescore_parameterized.py` — a fork of the original with exactly two changes: (a) the `_SCORING` import-path retarget from step 2, (b) `AEGIS_RISK` becomes a function/CLI parameter (default value `0.0100`, preserving current behavior byte-for-byte when unset) instead of a module-level constant. Everything else — panel loading, `ALLOCS_3` construction (now built from the parameter), tier list, control pins, cost-true delta, cap-feasibility note — stays **structurally identical** to the original.
4. **The scale-coupling question is pre-resolved — see §0.** No code change to `build_scaled_panel` or the `expect3` dict's `"scale"` guard is needed or wanted; `AEGIS_RISK` parameterization is orthogonal to it.
5. **Validation run (the only execution this packet performs):** run the parameterized script with `AEGIS_RISK` at its default (0.0100) — i.e., byte-identical inputs to the original — and confirm it reproduces, to the **same tolerance the original script already uses** (`CONTROL_TOL = 0.0015` for controls; exact match expected for the gating cells since this is the same seeds/inputs, not a fresh MC draw): controls `4.74%/1.06%/0.96%`, gating `10.96% / 3.78% / 3.54%` (Tradeify_Select_100K / Tradeify_Select_50K / MFFU_Rapid_50K). Write the validation output to `VALIDATION.md` in the same directory — numbers only, no narrative framing beyond "reproduces / does not reproduce."
6. Update `lab/CATALOG.md` with one new row for `aegis3leg_engine_param_2026-08-20` (theme `c1`, status `ACTIVE`), following the existing slug-sorted, one-liner convention in that file — **do not** run `--regenerate-catalog` (known to clobber unrelated hand-curated rows from a worktree; hand-insert only).

**Do NOT:**
- Run the parameterized script at any `AEGIS_RISK` value other than the default `0.0100`. Not 0.0075, not 0.0050, not a sweep, not "just to see." This is the load-bearing constraint of the whole packet — J14 bars it, and this packet's entire purpose is to stay clear of that bar while building the capability. If you find yourself wanting to run it at a different value "to test the parameterization works" — it doesn't need to; reproducing the default value **is** the test.
- Touch `run_class_s_c1_scoring.py`, `run_class_s_c1_regime_gate.py`, or anything under `Q-COMPOSE-1`'s own engine path (read them, per step 2's cited file; do not edit them) — this packet builds on the separate, already-correct harness, not the Trap #11-constrained one. The **only** import-path change licensed is the `_SCORING` retarget in the **parameterized fork** (step 2/3) — the ORIGINAL reference copy's imports stay untouched (dead, unexecuted, provenance only).
- Touch `docs/rejected_candidates.md`, `STATE.md`, `docs/SESSIONS.md`, or any ADR/pre-registration/closure file — this is a research-engineering packet, not a decision artifact; those stay with the orchestrator.
- Edit or delete `lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/RESULTS.md` (the closed campaign's own record) — leave it exactly as-is.

## §0.5 — Ambiguity surfacing (read before executing)

If the three input CSVs (§0.9-adjacent — check `inputs/` relative to this packet's own new directory first) are not present when you start, **stop and return `NEEDS_CONTEXT`** — do not substitute a different export or synthesize data; the orchestrator stages vendor bytes at dispatch time and their absence means the staging step didn't happen, not that you should work around it. If the retrieved original script's behavior at default parameters doesn't reproduce the published numbers within tolerance on your first validation run, **stop and return `BLOCKED` (context-problem)** with the actual numbers you got — do not adjust the script to force a match; that would mean something about the retrieval or environment is wrong, not the target numbers.

## §3 — Forbidden moves

- Running the parameterized engine at any risk level besides the validated default (J14; see §2).
- Reading this packet as license to also test the composed gate under any *other* changed input (cap, commission, panel export) — scope is the risk-allocation parameter only.
- Treating a successful validation run as itself a new measurement worth reporting to `ops/instruments/6J.md` as a finding — it reproduces an already-published number; it is not new information. The orchestrator (not this packet) will decide whether/how to record the engineering capability in the ledger.
- Committing anything under `lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/` itself — all new work lands in the new `aegis3leg_engine_param_2026-08-20/` directory.

## §6 — Return contract

Branch: `cursor/aegis-3leg-risk-param`. One PR. Four-state status:
- **`DONE`** — parameterized script exists, validation run reproduces all 6 published numbers within tolerance, `VALIDATION.md` + `CATALOG.md` row committed, no forbidden move touched.
- **`DONE_WITH_CONCERNS`** — validated, but something in the parameterization felt like a judgment call — flag exactly what and why so the orchestrator can adjudicate before trust.
- **`NEEDS_CONTEXT`** — the staged input CSVs are missing, or another genuine blocker not resolvable from source; state the exact gap.
- **`BLOCKED`** — validation doesn't reproduce; state which numbers diverged and by how much, unmodified.

---

## Orchestrator staging note (not part of Cursor's own instructions — dispatch-time only)

Verified this session (sha256 matched against `PANEL_FILES`/`AEGIS_SHA` in `run_class_s_c1_scoring.py`): the original script needs `ac331.csv` in **two** places (`resolve_panel_path`'s `CME_DIR` lookup for the main panel build, and `_HERE/inputs/` for the separate COST-TRUE diagnostic panel), and the two Striker exports only in `CME_DIR`. `-Copy` staging for `dispatch_cursor.ps1`:
```
-Copy "C:/Users/joshu/Downloads/Aegis_6J1_CME_6J1!_2026-07-27_ac331.csv::core/data/tv_exports/cme/Aegis_6J1_CME_6J1!_2026-07-27_ac331.csv",
      "C:/Users/joshu/Downloads/Aegis_6J1_CME_6J1!_2026-07-27_ac331.csv::lab/analysis/c1/aegis3leg_engine_param_2026-08-20/inputs/Aegis_6J1_CME_6J1!_2026-07-27_ac331.csv",
      "C:/Users/joshu/multi_firm_operations/core/data/tv_exports/cme/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv::core/data/tv_exports/cme/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv",
      "C:/Users/joshu/multi_firm_operations/core/data/tv_exports/cme/Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv::core/data/tv_exports/cme/Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv"
```

## Verification (orchestrator, post-return)

```bash
git log -1 --format='%h' -- lab/analysis/c1/aegis3leg_engine_param_2026-08-20/run_aegis1p_rescore_parameterized.py
diff <(git show pre-prune-2026-08-08:lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/run_aegis1p_rescore.py) lab/analysis/c1/aegis3leg_engine_param_2026-08-20/run_aegis1p_rescore_ORIGINAL.py
# Expected: empty (byte-identical reference copy)
grep -n "AEGIS_RISK" lab/analysis/c1/aegis3leg_engine_param_2026-08-20/run_aegis1p_rescore_parameterized.py
# Expected: a parameter/default, not a bare module constant
cat lab/analysis/c1/aegis3leg_engine_param_2026-08-20/VALIDATION.md
# Expected: 10.96% / 3.78% / 3.54% gating, 4.74% / 1.06% / 0.96% controls, within tolerance
```
