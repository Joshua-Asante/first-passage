# Q-GEOFIT-1 — Closure: `AMBIGUOUS-PARAMETERIZATION` (the profile family omits skew; the grid was never interpretable)

**Verdict:** `AMBIGUOUS-PARAMETERIZATION` — §6's third row, fired mechanically. The engine-reproduction anchor **passed exactly on both arms**; the profile-sufficiency anchor **missed by 23.63pp at an exact parameter match**. Per §6 that admits **no envelope claim from any cell**, so the 288-cell surface carries no conclusion and none may be inferred from it.
**Closed:** 2026-07-25
**Brief / pre-registration:** [`Q-GEOFIT-1-trailing-dd-funding-envelope.md`](../Q-GEOFIT-1-trailing-dd-funding-envelope.md) — `SIGNED / FROZEN: 2026-07-25 / JA` (signed and executed same day)
**Spend:** **$0.00.** Synthetic series plus already-pinned panel bytes only; no databento pull, no external data (§5 honoured).
**K consumed:** **zero.** No candidate return data was consulted in constructing or reading the grid; `docs/discovery_manifests/` untouched.
**Live effect:** **none.** c1 rung stays WATCH-1 0.50× / disarmed; no firm rule, floor, allocation, or `dd_protection` constant changed; locked book untouched.
**Artifacts:** [`lab/archive/q_geofit_1_2026-07/RESULTS.md`](../../../lab/archive/q_geofit_1_2026-07/RESULTS.md) · [`anchors.json`](../../../lab/archive/q_geofit_1_2026-07/anchors.json) · [`profile_positions.json`](../../../lab/archive/q_geofit_1_2026-07/profile_positions.json) · [`envelope.json`](../../../lab/archive/q_geofit_1_2026-07/envelope.json) · runner [`run_envelope_map.py`](../../../lab/archive/q_geofit_1_2026-07/run_envelope_map.py)

---

## 1. What ran

| Stage | Result |
|---|---|
| §0 Rule-0 re-verification | All **7** cited file anchors match their commits exactly (`f8f8db1`, `fd95c72`, `163b0b5`, `be6dda6`, `59c2282`, `13ad9a1`, `268851b`) |
| **A1 — engine reproduction, 1.00×** | **4.74%** vs published pin 4.74% — **MATCH** (Δ 0.003pp) |
| **A1 — engine reproduction, 0.50×** | **0.11%** vs published pin 0.11% — **MATCH** (Δ 0.003pp) |
| **A2 — profile sufficiency, nearest declared cell** | 35.89% vs real 4.74% — **MISS by 31.15pp** (tolerance 0.5pp) |
| **A2 — off-grid exact fit** (diagnostic) | 28.38% vs real 4.74% — **miss by 23.63pp** |
| 288-cell grid | **not executed** — operator election, see §5 |

A1 passing on both arms is what makes the A2 failure interpretable: the harness reproduces the corrected-geometry figures of record to three decimal places, so the A2 residual is a property of the **profile family**, not of the engine, the geometry patch, or the adapter.

---

## 2. The finding — the 4-tuple omits skew

A2 was designed to ask whether `(σ_d, μ/σ, shape, z)` is a sufficient summary of a real daily-P&L series. It is not, and the failure survives an **exact** parameter match — so this is not a range-coverage problem that a wider grid would fix.

Re-drawing the fitted 4-tuple and comparing the moments the family does *not* parameterize:

| moment | real c1 (active days) | synthetic at identical (σ_d, μ/σ, shape, z) |
|---|---|---|
| skewness | **+3.633** | **−0.345** |
| excess kurtosis | 17.92 | 3.85 |
| win fraction | 0.4286 | 0.6143 |
| worst single day | **−$744** | **−$3,067** |

The real book is a positively-skewed trend-rider: frequent small losses, rare very large wins, and a worst day of −$744 that never approaches the $3,000 EOD trail. The declared shape axis cannot express that. `student_t4` is **symmetric**, so at c1's own σ it returns single days of −$3,067 — enough to exhaust the entire drawdown allowance on their own — and the two-point mixtures have bounded kurtosis by construction and cannot reach 17.9 at all.

**For a path-dependent fixed-$ trailing barrier, survival is governed by the loss-side shape of the daily distribution.** Matching the first two moments plus a symmetric tail class is demonstrably insufficient: 23.63pp of bust error at exact fit. This sharpens the standing lesson `lesson_prop_archetype_drawdown_survival` ("prop firms fund SURVIVAL not edge") into something mechanical — *which* distributional property the DD mechanism selects on.

---

## 3. Second, independent finding — the declared ranges contain neither real book

Deliverable (iii), computed on both readings of §2's moment definitions (active-day, which the runner declares, and all-day, the competing reading):

| book | reading | σ_d (% acct) | μ/σ | z | inside grid? |
|---|---|---|---|---|---|
| c1 | active-day | 0.5907 ❌ | +0.2162 ❌ | 0.7931 ❌ | **no** |
| c1 | all-day | 0.2733 ✅ | +0.0967 ✅ | 0.7931 ❌ | **no** |
| CFD (4 locked legs) | active-day | 2.1961 ❌ | +0.2404 ❌ | 0.6111 ❌ | **no** |
| CFD | all-day | 1.3928 ❌ | +0.1474 ✅ | 0.6111 ❌ | **no** |

Declared ranges: σ_d ∈ [0.05, 0.45]%, μ/σ ∈ [0.0, 0.15], **z ∈ [0.0, 0.40]**.

**Under both readings, both real books fall outside the grid on `z`.** They trade on 21% and 39% of business days; the grid's sparsest cell trades 60%. This is not an artifact of the active-day reading and not a c1 quirk — the frozen grid models books that trade most days, and this programme has none. The CFD book is additionally 3–5× outside the σ_d ceiling under either reading.

---

## 4. Verdict routing (§6, mechanical)

- `RESOLVED-ENVELOPE-NONEMPTY` requires "anchors hold **and** ≥1 practical cell clears" — **fails at the first conjunct.**
- `FALSIFIED-ENVELOPE-EMPTY` requires "anchors hold **and** 0 of the practical cells clear" — **fails at the first conjunct.**
- **`AMBIGUOUS-PARAMETERIZATION` requires any validation anchor to miss — FIRES** (profile-sufficiency residual 23.63pp ≫ ±0.5pp).

Clean single verdict. Note both accept/reject branches of §4 are gated on the anchors holding, so **H-GEOFIT is neither accepted nor rejected** — it returns to the successor brief intact.

---

## 5. Why the 288-cell grid was not executed

§8 step 2 halts interpretation, not execution, on an anchor miss — so the grid *could* have run. It was launched and stopped after the anchors resolved, on operator election (2026-07-25), for the reason §6 states directly: an anchor miss admits **no envelope claim**, so the ~8h sweep could not have produced the deliverable it exists for. Scoring it anyway would have created a boundary table that §5 forbids citing ("counting an envelope cell as candidate evidence") while sitting in the repo inviting exactly that citation.

**The grid remains declared and unrun.** Re-running it is a matter of executing the same frozen runner (`--mode all`, checkpointed), not of re-deciding the grid. RESULTS.md marks deliverables (i) and (ii) `NOT EXECUTED` and states explicitly that this is *not* a finding of "nothing clears" — the two claims are different and must not be conflated.

---

## 6. Defects found in the frozen brief (recorded, not repaired here)

1. **§4's cell counts are wrong.** The declared predicate `μ/σ ≤ 0.10` partitions the 288 cells as **240 practical / 48 diagnostic**; the stated "192 / 96" requires a strict `< 0.10`. §2's prose ("a persistent daily edge ratio **above** 0.10 …") settles it in favour of `≤`, which the runner executes. The accept rule (≥1 clears) is unaffected unless every clearer sits exactly on the boundary; the runner detects and escalates that case rather than resolving it silently.
2. **§8's runtime estimate is ~8× low.** "≈30–60 min wall at frozen sims" assumed early termination; low-edge cells run the full 1500-day horizon. Measured ≈8h at `n_jobs=7`. Sims are frozen by the gate pre-registration, so parallelism and checkpointing are the only admissible levers.
3. **An interpretive reading the brief left undeclared (R4 — zero-day *placement*).** §2 fixes the zero-day *fraction* `z` but not where the zeros fall. `build_week_blocks` takes fixed Mon-anchored 5-day slices, so placement sets the within-block active count. The runner places zeros uniformly at random; a real sparse book clusters its idleness (a quiet week is five consecutive zeros). Temporal clustering of inactivity is therefore a *second* unparameterized dimension alongside skew, and a successor must declare a placement law.

   > **Correction 2026-07-25 (direction withdrawn).** This entry originally asserted that uniform placement is "the lower-dispersion, higher-bust, **anti-clearing** choice — so it is conservative for accepting H-GEOFIT." **That directional claim is withdrawn.** It rested on a 2,000-sim proxy at non-c1 parameters, surfaced during the adversarial audit and carried into this closure without its provenance being marked. Measured directly at frozen sims and the real book's own parameters, the placement effect is **−0.29pp** (clustered minus uniform) with a combined SE ≈1.37pp — **0.21σ, indistinguishable from zero**. R4 remains a genuine undeclared reading; its **direction and magnitude are unmeasured**, and no conservatism may be claimed from it. Source: [`lab/archive/geofit_skew_probe_2026-07-25/README.md`](../../../lab/archive/geofit_skew_probe_2026-07-25/README.md).

None of these are repaired in the frozen artifact — per §5 and brief-authoring Trap #12, gate criteria are not amended mid-investigation. They are inputs to the successor brief.

---

## 7. What this closure does **not** license

- **It is not a Striker MYM/MNQ reconstruction re-open and cannot be cited as one.** That lane is TERMINAL / ORB-MNQ PARKED by operator ruling (ADR `13ad9a1` Addendum 2026-07-24); re-open needs a fresh operator GO plus pre-registration, and neither exists.
- **No candidate claim.** No cell was scored, so no "the mechanism matches cell X" argument is available even in principle.
- **No floor change.** bust ≤ 3.0% / P(pass) ≥ 50% is untouched and remains parsed from the gate pre-registration, never hardcoded.
- **The prop-portfolio §4 falsifier is unaffected** — still undischarged, hard date **2026-11-08** unchanged. Q-GEOFIT-1 was gate *calibration*, not a discharge route.
- **No re-scoring claim** attaches to the book profile positions in §3; they are context, as §2 specifies.

---

## 8. Forward — what a successor brief must carry

A re-scope is warranted (§6's own disposition: "re-scope with a richer profile family in a fresh brief"). Requirements this closure hands it:

1. **An explicit skew / loss-tail dimension.** The measured insufficiency is 23.63pp at exact fit on the first two moments plus a symmetric tail class. A successor family that does not separate loss-side from win-side shape will fail the same anchor.
2. **Ranges that contain the programme's real books** — in particular `z` up to ≈0.80, since both real books exceed the current 0.40 ceiling under every reading. Widening ranges alone is *not* sufficient (see 1), but it is necessary.
3. **A declared zero-day placement law** (clustered vs uniform), per §6-defect 3.
4. **The same A1/A2 anchor discipline.** The anchors are what made this run informative rather than confidently wrong — A1 proved the harness, A2 killed the family. Keep both, and keep A2's exact-fit arm, which is what distinguished "wrong ranges" from "wrong family."
5. **Consistent predicate/count arithmetic** for the practicality ceiling.
6. A realistic wall-clock estimate, or a pre-declared reduced-sim exploratory tier that is explicitly non-gating.
7. **≥N synthetic realizations per cell, averaged.** §2 pins one series per cell (`seed = 20260724 + cell_index`) and the MC then resamples only *block indices* from that single 1692-day draw. Series-realization noise measured at **≈0.55–1.09pp sd** across seeds — roughly **6–11× the 0.098pp binomial SE** at 30k sims, and irreducible under the frozen 10k × 3-seed protocol. Harmless here (no cell was scored, and the effect is two orders of magnitude short of moving `anchors_hold`), but **a published boundary table drawn from single realizations is not reproducible** — adjacent cells would swap clearing status on reseed alone. This is a limitation of the frozen spec, not of the runner.
8. **Fix `median_days` in the caller, not the shared primitive.** §2 lists `median_days` as a recorded per-cell diagnostic, but `run_partition_mc` does not return `run_tier_remc`'s `summary`, so the value is structurally `None` for every cell. No gate or deliverable reads it. If the successor wants it, thread the already-computed summary through the adapter — do **not** modify the frozen shared primitive.

**Cheapest next probe, if one is wanted before a full re-scope:** fit c1 with a skewed family (e.g. a two-sided distribution matched on win-rate + separate win/loss scales) and re-run A2 only. That is two MC calls, no grid, and it would confirm or refute the skew diagnosis directly before anyone commits to a 288-cell successor.

---

## 9. The brief's own §10 hooks — three are defective (M-AHF)

All six §10 hooks were executed. **Every substantive claim they test holds**, but three of the hooks are mis-written and would mislead a future reader — a textbook [M-AHF](../../methodology/lessons/methodology_lessons.md) instance ("audit hooks tested against the author's mental form, not the artifact's storage form"):

| Hook | Stated expectation | Actual | Diagnosis |
|---|---|---|---|
| **§10-1** no prior envelope | no hits outside GEOFIT | 5 hits | Grep is too broad: it matches `envelope.json` from **Q-GUARDIAN-DECAY-1**, a Guardian-solo MC envelope — a different artifact that happens to share a filename. Restricting to `"funding envelope"` returns none, so the *intent* (no prior funding-envelope map) holds. |
| **§10-2** grid immutability | `expect 1` | 2 | **The hook counts its own line.** The axis string appears once in §2 (line 110) and once inside the §10 code fence (line 237). Excluding the hook's own line gives **1** — immutability holds. |
| **§10-6** zero-K | `git log … docs/discovery_manifests/` | dir does not exist | Wrong path — the manifests live at **repo-root `discovery_manifests/`**, not under `docs/`. At the correct path the tree is **clean and untouched**, so the zero-K claim holds. |

Corrected forms are given below and should be carried into the successor brief instead of the originals.

## 10. Audit hooks (runnable — corrected)

```bash
# 1. Verdict of record.
python -c "import json;print(json.load(open('lab/archive/q_geofit_1_2026-07/envelope.json'))['adjudication']['verdict'])"   # AMBIGUOUS-PARAMETERIZATION

# 2. A1 passed both arms; A2 missed — the whole basis of the closure.
python -c "import json;d=json.load(open('lab/archive/q_geofit_1_2026-07/anchors.json'));print({k:v['ok'] for k,v in d['A1'].items()}, d['A2']['nearest_ok'], d['A2']['offgrid_exact_residual_pp'])"

# 3. Grid genuinely unrun (not 'ran and found nothing').
python -c "import json;d=json.load(open('lab/archive/q_geofit_1_2026-07/envelope.json'));print(d['grid_executed'], len(d.get('cells',[])))"   # False 0

# 4. Zero K — manifests are at REPO ROOT, not under docs/ (§9 hook defect). Expect empty.
git status --porcelain discovery_manifests/

# 4b. Grid immutability — exclude the hook's own line, then expect exactly 1 (§9 hook defect).
grep -n "0.05, 0.10, 0.15, 0.20, 0.30, 0.45" docs/briefs/Q-GEOFIT-1-trailing-dd-funding-envelope.md \
  | grep -v "grep -c" | wc -l   # expect 1

# 4c. No prior FUNDING-envelope map — the bare "envelope.json" grep collides with
#     Q-GUARDIAN-DECAY-1's unrelated Guardian-solo envelope (§9 hook defect).
grep -rn "funding envelope" docs/ lab/ --include="*.md" | grep -vi geofit   # expect none

# 5. TERMINAL guard still standing (this closure must never become a re-open route).
grep -n "TERMINAL" docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md | head -3

# 6. Floor never restated locally — must come from the pre-registration.
grep -n "eval_bust_ceiling\|load_scoring_thresholds" lab/archive/q_geofit_1_2026-07/run_envelope_map.py | head -5
```

---

## 11. Independent adversarial audit of the runner (2026-07-25)

A 25-agent adversarial review ran five independent lenses over the runner and the frozen spec — synthetic-generation math, the interpretive readings, the out-of-grid claim, §5/frozen-spec compliance, and engine/`z` interaction — each finding then handed to a separate agent instructed to **refute** it.

**19 findings raised, 0 survived refutation.** Verdict: the runner is a faithful execution of the frozen §2 spec (*"yes-with-caveats"*), with the caveats being precisely the R1–R4 readings and the `192/96` slip that RESULTS.md already publishes rather than buries. The audit independently confirmed that the §6 disposition is robust: `anchors_hold = false` is deterministic, the A2 miss (47–62× tolerance) is driven by an unparameterized moment rather than sim noise (MC SE ≈ 2pp at these rates) or range clamping (the unclamped arm also misses), and **even a fully executed, defect-free 288-cell grid returns `AMBIGUOUS-PARAMETERIZATION`.**

Two real mechanisms it surfaced are carried into §8 above as successor requirements 7 and 8 (single-realization noise; `median_days`). One genuine code defect was found and **fixed**: the final progress line referenced a dict key renamed during the census correction, which would have raised `KeyError` on any `--mode grid` run *after* `envelope.json` was already written — a correct artifact with a traceback and a non-zero exit, i.e. a completed 8h run that looks failed. Repaired and re-verified (exit 0); it touches a print statement only and changes no number, no verdict, and no frozen constant.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-25 | §9 signed; §0 re-verified; runner built; A1 PASS both arms; A2 MISS 23.63pp at exact fit; grid stopped by operator election; closed `AMBIGUOUS-PARAMETERIZATION` | Joshua (signature + grid disposition) + Claude Code (Opus 5) |
| 2026-07-25 | 25-agent adversarial audit: 19 findings, **0 survived refutation**; §6 disposition independently confirmed robust. Fixed a `KeyError` on the grid progress line (print-only, §5-neutral); added successor requirements 7–8 (per-cell realization noise ≈6–11× binomial SE; `median_days` structurally `None`) | Claude Code (Opus 5) |
