# SPEC 2026-08-04 — Phase-4 both-halves regime re-run on the venue's honest clock

**Status:** `FROZEN` — operator **GO given 2026-08-04**. Build + run **NOT executed**; this spec is the frozen contract for executing it.
**Owner artifact for the GO:** [`ADR 2026-08-03-lifecycle-ladder-intermediate-rung`](../adr/2026-08-03-lifecycle-ladder-intermediate-rung.md) §7 Phase 4 (which requires exactly this operator GO before the run).
**Repo anchor:** `289535d`, worktree clean, verified 2026-08-04.

---

## §0 — Why this spec exists rather than a completed run

The ADR's Phase 4 reads *"re-run the `class_s_c1_haircut_regime_remc` both-halves regime gate … with `intraday_low` fed from 15m bars and `dd_lock_offset_usd` set unreachable."* Read against production, **that is not a flag on an existing runner — it is new capability with a correctness-critical invariant**, and it is gated on data absent from this worktree. All four findings below were verified, not assumed:

| # | Finding | Verified by |
|---|---|---|
| 1 | **`intraday_low` is not threaded anywhere in the scoring chain.** | `rg -c intraday_low lab/discovery/prop_survivor_scoring.py` → **0** (confirms gate-stack audit R2) |
| 2 | **The existing runner applies only a uniform daily haircut.** `run_haircut_regime_remc.py` multiplies `daily_100k` by the rung and calls the frozen regime primitives; there is no second channel. | `run_haircut_regime_remc.py::run_arm` |
| 3 | **The pairing must survive TWO independent resamplings** — see §1. Getting it wrong yields a plausible-looking wrong number. | `run_class_s_c1_regime_gate.py::_make_alt_panel` (126-bday block bootstrap) + `prop_survivor_scoring.py::blocks_from_daily_pnl` → `(n_weeks, 5, 1)` week-blocks resampled inside `run_tier_remc` |
| 4 | **Cost is ~3.2h per arm.** The 2026-07-17 0.50× arm ran **11,499 s** at n=100 panels / 10k×3 sims on 8 cores. | `class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md:6` |

**Blocking preconditions, both currently unmet:**

- **Panels absent from this worktree.** `core/data/bar_data/` here holds only `README.md` + `SHA256SUMS`; the CSVs (`MYM_M15.csv`, `MNQ_M15.csv`) are gitignored and live in the primary checkout. The run must execute where the bytes are.
- **Panel provenance defect unrepaired.** The 2026-08-03 panels are outside the manifest tree — `rg -c "2026-08-03" core/data/tv_exports/cme/SHA256SUMS` → **0**. The ADR calls its Phase 1 *"Blocking for lock-grade use."* **A Phase-4 result produced before this repair is not lock-grade** and may not be read as superseding the 2026-07-17 record.

**Freeze-integrity check, executed 2026-08-04 (and it corrected a live audit claim).** The frozen survivor-scoring pre-reg now has **2** commits and blob `25c7803`, where the gate-stack audit recorded 1 commit and `86e9038`. `git diff be6dda6 HEAD` on that file is **exactly one line** — a path repair inside its own §10 hook, from the lab theme-nest. **Thresholds are byte-identical (3.0% / 50% / 1.0%).** The freeze holds in substance; the audit's phrasing was stale and a dated correction was appended at the grep where it is re-run.

---

## §1 — The load-bearing invariant (get this wrong and the run is worse than not running)

`intraday_low` is a **per-day channel paired to `daily_100k` by index**. It is consumed at the end of a chain that resamples days **twice**:

```
daily_100k (1-D, n_days)
  └─ _make_alt_panel()        126-bday CONTIGUOUS blocks, offsets `st` drawn per panel   ← resample #1
      └─ blocks_from_daily_pnl()   → (n_weeks, 5, 1) Mon-anchored week-blocks
          └─ run_tier_remc() → run_seed()   resamples WEEK-BLOCKS per simulated path      ← resample #2
              └─ simulate_path(path=..., intraday_low=...)   <- core/mc/simulation.py:52 (kwarg L68)
```

> **INVARIANT — `intraday_low` must be carried as a parallel channel through BOTH resamplings, sliced/sampled with the SAME indices as the P&L, never re-derived or re-drawn independently.**

Concretely, the build must:

1. Add a paired `(n_weeks, 5, 1)` intraday channel alongside `blocks_from_daily_pnl`'s output, built from the **same** `pd.bdate_range("2020-01-06", …)` index so week-anchoring is identical.
2. Make `_make_alt_panel` slice **both** arrays at the same `st : st + block_size` offsets (one RNG draw, two slices — not two draws).
3. Make `run_seed` / `run_tier_remc` sample week-block **indices once** and apply them to both channels.
4. Pass the assembled per-path intraday array into **`core/mc/simulation.py::simulate_path(intraday_low=…)`** (defined L52, kwarg L68; called by `run_seed` at L233).

⚠ **Naming correction, recorded not silently fixed.** This spec's first draft called the sink `run_one`. **No such function exists in the MC chain** — the three `run_one` definitions in the repo (`lab/analysis/_inbox/ict_mnq_2026-08/run_w_layer.py:32`, `run_d_layer.py:144`, `lab/analysis/legacy/guardian_parity_2026-06-23/run_parity.py:129`) are unrelated bar/panel harnesses that accept no `path`, `intraday_low`, or `dd_scale`. The described *behaviour* was correct throughout; only the call-site name was wrong. Caught by this branch's pre-merge verification pass — `lesson_verify_content_not_path_or_id`.

**Sign and scale convention (from the `simulate_path` docstring, `core/mc/simulation.py` L72–76, verbatim):** per-day minimum equity **excursion in dollars measured from that day's OPENING equity**, so entries are **≤ 0.0 and UNSCALED** — *"this function applies `dd_scale` to them exactly as it does to `path`"* (i.e. `simulate_path` itself; the first draft rewrote "this function" to "`run_one`" inside what it labelled a verbatim quote). **Do not pre-scale by the rung**; the rung haircut is applied to the daily series and the engine mirrors it onto the excursions.

**Derivation source:** real 15m bars. ADR §4 is explicit that per-trade MAE is **not** an acceptable substitute for this limb.

**Mandatory non-vacuity guard.** Before trusting any arm, assert the threaded channel actually changes the answer: a run with `intraday_low` all-zeros **must** reproduce the close-only figures byte-for-byte, and a run with the real channel **must** differ. An `intraday_low` silently dropped on the floor would produce exactly the 2026-07-17 numbers and look like a clean re-PASS — the most dangerous available failure mode, and the shape of M-23 (defective geometry through a process pool, optimistic, undetected four days).

---

## §2 — What to run, in order

| Phase | Action | Stop condition |
|---|---|---|
| **P0** | Re-verify anchors; confirm `core/lifecycle.py` still 4-rung at `4441c72`; confirm the frozen pre-reg's thresholds still 3.0/50/1.0. | Any threshold moved → **STOP**, this is a governance event, not a re-run. |
| **P1** | **Repair panel provenance** — land the 2026-08-03 panels into `core/data/tv_exports/cme/`, `python scripts/check_data_manifests.py --regenerate --dry-run` then `--regenerate`, commit the `SHA256SUMS` delta in the **same commit**. | Manifest check red → **STOP**. Not lock-grade without this. |
| **P2** | Build the paired channel per §1 + the non-vacuity guard. **Zeros-channel reproduction must be byte-exact against `haircut_remc_report.json` before any real-channel arm runs.** | Reproduction not byte-exact → **STOP**; the threading is wrong. |
| **P3** | **Score 0.50× first** — the admissibility question. Same partitions (full / H1 2020-23 / H2 2023-26 / bootstrap-95th), same thresholds, `n_panels=100`, `10k×3` sims, seeds 42/123/2026, `dd_lock_offset_usd` **unreachable**. ~3.2h. | — |
| **P4** | **Score 0.40× ONLY IF 0.50× fails.** If 0.50× PASSes all four partitions, stop — and see §3. | — |
| **P5** | Land `lab/analysis/c1/class_s_c1_haircut_regime_remc_intraday_2026-08/RESULTS.md`; report the deltas against the 2026-07-17 figures. | — |

**Reference figures the re-run is measured against** (2026-07-17, close-only, under `dd_lock_offset_usd: 100`):

| Arm | H1 bust | boot-95th | Verdict then |
|---|---|---|---|
| 1.00× | 4.37% | 10.37% | **GATE FAIL** |
| 0.50× | 0.14% | 0.77% | **GATE PASS** (pass-5th 95.76%) |

---

## §3 — How to read the result (both directions are consequential)

**If 0.50× re-PASSes all four partitions:** the WATCH-1H ADR's own §4 admissibility limb fires — *"this ADR's premise dissolves, and `WATCH-1H` should be **withdrawn** rather than left as an unused rung inviting future selection-by-availability."* The correct action is to withdraw it, **not** to land the rung anyway.

**If 0.50× FAILS:** 0.50× loses admissibility under the ratified EV objective, and 0.40× becomes selectable — *if* `WATCH-1H` is landed. Note this now decides a **counterfactual** rung, not a live one (§4).

**Either way, this is a measurement, not an authorization.** It does not arm anything, does not re-tier anything, and does not by itself supersede the 2026-07-17 operator-signed record — the ADR is explicit that re-running a frozen operator-signed gate on corrected inputs *"needs an operator GO before it runs, and its result may not be read as superseding the 07-17 record without one."* The GO covers the run. Superseding the record is a separate ruling.

---

## §4 — What the 2026-08-04 venue de-scope changed about this run

The GO was given in the same session as [`ADR 2026-08-04`](../adr/2026-08-04-tradeify-venue-descope-eval-included.md), which de-scopes Tradeify in both phases. That **re-frames Phase 4's purpose and the change is recorded rather than left implicit**:

| | Before the de-scope | After |
|---|---|---|
| **Purpose** | Decide the **live** c1 rung | Price the **measurement-fidelity defect** |
| **Urgency** | First armed send pending | None — no armed send, no live rung |
| **Consumer** | The rung-selection objective | Prop-portfolio **§4** at 2026-11-08, and audit §5.4 item 4 |

**It retains real value.** The gate-stack audit names this exact measurement its single highest-value available item (§5.4 item 4: *"re-running the four decisions of record with `intraday_low` threaded and the corrected `dd_lock_offset_usd`, and publishing the deltas"*), and Tradeify remains in §4's frozen $100K×4 simulation set regardless of being de-scoped as a deployment target — so the honesty of its bust geometry still load-bears on the 11-08 falsifier.

**It also removes the WATCH-1H ADR's decision driver.** That ADR's §1 justified urgency as closing a granularity gap *"before the re-measurement lands rather than under its pressure,"* with a first armed send pending. There is now no armed send and no live rung to protect. **Recommendation (operator's call, not this spec's):** hold `WATCH-1H` at `Proposed` pending this run rather than landing Phases 1–3 for optionality — the ADR itself says landing them without Phase 4 *"is not grounds to re-tier c1,"* and with no live rung the optionality has no near-term consumer.

---

## §5 — Forbidden moves

- **Running the arms before the zeros-channel reproduction is byte-exact.** The whole point is that a dropped channel reproduces the flattering 2026-07-17 numbers.
- **Substituting per-trade MAE for a bar-derived excursion.** ADR §4 names it out explicitly.
- **Pre-scaling `intraday_low` by the rung.** `simulate_path` applies `dd_scale` itself; double-scaling silently deepens every excursion.
- **Re-drawing the intraday channel independently at either resampling.** §1's invariant; the failure is invisible in the output.
- **Scoring 0.40× before 0.50×.** The admissibility question is 0.50×; scoring the fallback first invites reading a pass-rate comparison as licence, which the governing EV objective forbids and the WATCH-1H ADR's own first draft got wrong.
- **Reading a PASS as authorization to arm, or a FAIL as authorization to re-tier.** Neither follows; both need their own operator action, and with the venue de-scoped there is nothing to arm.
- **Treating this result as superseding the 2026-07-17 record without a separate operator ruling.**
- **Quietly widening scope to re-score the other three decisions of record** (07-15 discharge, 07-22 withdrawal, 07-24 band re-score). They are the audit's §5.4 item 4 and are worth doing — as their own dated pass, not smuggled into this one.

---

## §6 — Audit hooks (runnable)

```bash
# 1. Has the build happened? (intraday_low threaded into the scoring chain)
rg -c "intraday_low" lab/discovery/prop_survivor_scoring.py   # 0 = not built yet

# 2. Has the run happened?
ls lab/analysis/c1/class_s_c1_haircut_regime_remc_intraday_2026-08/ 2>/dev/null \
  || echo "Phase 4 NOT run -> WATCH-1H ADR stays Proposed"

# 3. Blocking precondition: panel provenance repaired?
rg -c "2026-08-03" core/data/tv_exports/cme/SHA256SUMS 2>/dev/null \
  || echo "VIOLATION: panels still outside the manifest tree -> result is not lock-grade"

# 4. Freeze integrity: thresholds unmoved (the ONLY drift that matters here).
git diff be6dda6 HEAD -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md --stat
# Expected: exactly 1 line changed (the 91137fb path repair). Anything touching
# 3.0% / 50% / 1.0% is a governance event -> STOP.
rg -n "bust ≤ 3\.0%|P\(pass\) ≥ 50%|bust ≤ 1\.0%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md

# 5. The ladder is still 4-rung (WATCH-1H not landed).
python -c "import sys; sys.path.insert(0,'core'); import lifecycle; print(lifecycle.TIER_MULTIPLIER)"
# Expected: {'AUTHORIZED': 1.0, 'WATCH-1': 0.5, 'WATCH-2': 0.25, 'RETIRED': 0.0}

# 6. Panels present wherever this is executed (they are gitignored; absent in worktrees).
ls core/data/bar_data/*.csv 2>/dev/null || echo "no panels here -> run from the primary checkout"
```

## Verification

```bash
git log -1 --format='%h %cs' -- core/mc/simulation.py    # fc14682 (owns the intraday_low arg)
git log -1 --format='%h %cs' -- core/lifecycle.py        # 4441c72 (pre-implementation, 4-rung)
git rev-parse HEAD:docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md  # 25c7803

# The reference figures this run is measured against
rg -n "4\.37|10\.37|0\.14|0\.77|95\.76" lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md

# The ~3.2h/arm cost basis
rg -n "11,499|11499" lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md
```
