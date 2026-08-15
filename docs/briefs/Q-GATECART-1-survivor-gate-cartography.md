# Q-GATECART-1 — Survivor-gate cartography: is the frozen Part-A gate reachable, and by what profiles?

**Status:** `CLOSED-FALSIFIED` (2026-07-14, at **Phase 0.5 — ahead of the grid**). §8 formula operator-confirmed 2026-07-14; the realistic-and-demonstrable band is **empty at the banked K=3,177** (S_floor 2.05 > every admissible Cap ≤ 2.0), so H-CART's "otherwise" branch fired without the grid. Closure: [`docs/briefs/closures/Q-GATECART-1-survivor-gate-cartography.md`](closures/Q-GATECART-1-survivor-gate-cartography.md). Phase-1 grid **DEFERRED** (moot at the banked K; Cursor handoff held per operator). Lesson **M-19**.
**Authored:** 2026-07-14
**Closed:** 2026-07-14 (CLOSED-FALSIFIED at Phase 0.5; verdict K-conditional — see closure)
**Authors:** Joshua + Claude Code (Fable 5)
**Parent question:** N/A (feeds the four-firms ADR §4 falsifier runway and the 08-08 axis-selection decision; owns neither)
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q (STRATEGIC) — closure gated on the §6 verdict computed from the pre-registered grid at the frozen scoring posture
**Artifact path:** `docs/briefs/Q-GATECART-1-survivor-gate-cartography.md`

**Pre-Q gate:**
  D: nothing deleted from the I/N corpus — the corpus is four production artifacts (§0), all load-bearing; no market data enters this question at all
  S: candidate space compressed to the 3-axis daily-P&L parameterization (edge/vol ratio × vol level × tail shape) that `run_seed` week-block resampling actually consumes — per-trade texture folds into the daily aggregate by construction (`blocks_from_daily_pnl`)
  A: grid pre-registration (§7 Phase 1) makes every subsequent "can profile X pass tier Y?" query one dictionary lookup in the emitted map

**D-S-A domain:** data (synthetic-profile corpus design only; no framework or system change — the frozen gate and harness are consumed read-only)

---

## §0 — Rule 0 reads (production-source verification)

All read in full this session (2026-07-14), working tree = `claude/progress-summary-candidate-axis-f78ee0` off `main` @ `3af5f87`:

- `lab/discovery/prop_survivor_scoring.py` — anchor: `97011c1` (2026-07-13). G0–G8 harness. Load-bearing facts used below: thresholds are **parsed from the pre-registration, never hardcoded** (`load_scoring_thresholds`, refuses to guess); scoring posture = dd_protection OFF (`NO_PROTECTION_TRIGGER = 10.0`), `strats=("candidate",)`, single-leg week-blocks via `blocks_from_daily_pnl` (Mon-anchored `bdate_range` from 2020-01-06, ≥5 bdays); `run_tier_remc` = `assert_engine_ready` → `firm_kwargs(inactivity_off=True, consistency=…)` → `run_seed` per seed → `summarize_outcomes`; Run-1/Run-2 pattern with `gated_on="run1_degenerate"` when a tier has no `consistency_rule_pct`; `n_sims` override is explicitly test-sanctioned, `tiers=` override is "never for a live scoring claim"; `score_candidate` emits `discharges_falsifier` (a field this brief must never populate from synthetic input — §5).
- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` — anchor: `be6dda6` (2026-07-13). **FROZEN.** Part A = headline bust ≤ 3.0% AND P(pass) ≥ 50%, Run-2, $100K band; Part B = bust ≤ 1.0% funded (diagnostic, does not gate §4); discharge = ≥2 distinct firms incl. ≥1 `trailing_locking`; seeds **42/123/2026**, **10k sims/seed**, horizon **1500**, inactivity disabled; §7(9) owes a **pre-registered non-candidate calibration reference** feeding the §6 AMBIGUOUS ceiling-mis-set clause; §7(8) all-null close is success-eligible.
- `core/mc/preflight.py` — anchor: `a53ee99` (2026-07-13). `summarize_outcomes` headline_bust = mean(daily+static+trailing) with the per-seed bucket-sum==n_sims assertion; `firm_kwargs` dispatches `dd_type` static/trailing/trailing_locking (trailing_locking requires `dd_lock_offset_usd`); F2 caveat verbatim: `trailing` firms' %-of-peak modeling is an optimistic lower bound vs their fixed-$ real rules — "callers must still label Bulenox/BluSky results optimistic-lower-bounds".
- `core/firm_rules.py` — anchor: `a53ee99` (2026-07-13). Frozen four confirmed present with the geometry split the map isolates: `Bulenox_100K`/`BluSky_Premium_100K` `dd_type="trailing"`, `Tradeify_Select_100K`/`MFFU_Rapid_100K` `dd_type="trailing_locking"`; `consistency_rule_pct` = none / 34.0 / 40.0 / 50.0 respectively (Bulenox none → Run-2 degenerates to Run-1 per harness); `cost_per_side_usd` present all four families ($0.61 / $0.95 / $0.91 / $0.95, index micros; MGC higher per-file comments).
- `docs/adr/2026-07-13-harv-discovery-lane-ratification.md` — anchor: `b6e604a` (2026-07-14). §2.2 mandates pre-freeze gate-reachability simulation of every bundled clause (HARD, blocks `register_search open` for mechanism-first campaigns). This brief is the same discipline pointed at the **program's terminal gate** instead of one campaign's clause bundle.
- `docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md` — anchor: `0e26a7b` (2026-07-11). §4 falsifier: ≥1 pre-registered candidate clears on ≥2 of 4 FRIENDLY tiers by **2026-11-08**, else demote to research-only; 08-08 is a progress check.

Architecture-truth note (edit-prescription scope): this brief prescribes **new files only** (`lab/analysis/gatecart_2026-07/`); zero edits to any file above. The driver's import surface (`load_scoring_thresholds`, `run_tier_remc`, `score_part_a`, `score_funded`) was verified against the harness source, not assumed.

---

## §1 — Context & motivation

The 07-06→07-14 batch left the prop-portfolio program with a complete, frozen verdict machine and an empty candidate pipe: DISC-CAMP-0 closed FALSIFIED (0 survivors) and Q-HARV-0 closed AMBIGUOUS, so every path to the 2026-11-08 §4 falsifier now runs through a **new discovery axis chosen in the next few weeks** — and that choice is currently being made on qualitative judgment, with no knowledge of whether the frozen Part-A gate is reachable by *any* realistic candidate, or what return-profile a candidate would need to reach it. The program has already paid twice for freezing gates without a reachability read: Q-HARV-0's placebo clause was structurally un-passable at registration (five review layers missed it), and DISC-CAMP-0's original DSR K-rule was found effectively unreachable only by a dedicated pre-run audit (2026-07-12, fixed by ADR supersession before the pull). The HARV lane ADR converted that lesson into HARD doctrine for campaign clause bundles; the terminal survivor gate deserves the same simulation before it silently prices four months of discovery work.

## §2 — Prior art / lineage

- **`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`** (FROZEN) — owns the gate this brief maps. This brief changes nothing in it and adjudicates nothing under it; it additionally discharges that document's §7(9) obligation by designating one grid point as the calibration reference (§7 Phase 0 here).
- **`docs/notes/audits/2026-07-12-disccamp0-gate-reachability-audit.md`** — direct precedent: a frozen gate audited for reachability *before* first use, defect found, fixed via ADR before any budget burned.
- **`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`** (`Accepted`) — reachability-simulation-as-HARD-gate doctrine this brief generalizes.
- **Q-HARV-0 closure** (`docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md`, AMBIGUOUS) — the dated incident behind the doctrine.
- **`lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md`** — the falsified locked-book transfer (17.70% bust) the ceiling was calibrated to exclude; source for the §7(9) reference profile's daily stats.
- **Memory lesson `lesson_gate_reachability_preregistration`** — "sim bundled clauses under a plausible-true world."

## §3 — Question (Q-GATECART-1)

Symptom-only form (no fix baked in): axis selection for the 11-08 window is happening blind to the frozen gate's geometry.

**Q-GATECART-1:** Which regions of candidate daily-P&L-profile space — (edge/vol ratio, vol level, tail shape) at the $100K band — clear the frozen Part-A survivor gate on ≥2 of the four frozen tiers (≥1 `trailing_locking`), and is that region non-empty within realistic single-strategy profiles?

## §4 — Falsifiable hypothesis (H-CART)

**Realism band (data-anchored, frozen as a formula in §8 before any anchor is measured — not a felt number).** A profile is "realistic" iff **S_floor ≤ annualized Sharpe ≤ Cap**, both computed *after* the §8 freeze from data that exists independently of this cartography run (annualization factor 252; SR 2.0 ⇔ daily μ/σ 0.126):

- **Cap (ceiling; the binding constraint for FALSIFIED)** = smallest grid rung ≥ **max(S_A, S_B)**. **S_A** (Anchor A) = the maximum standalone annualized Sharpe among the four locked legs on the canonical Pepperstone panel — the best single edge this programme has validated, on a *friendlier* venue than the prop envelope (no E1 forfeiture / no consistency drag / pyramiding intact) and gross-of-swap, so it is inflated in the **conservative** direction for a ceiling. **S_B** (Anchor B) = the top-decile net-of-cost annualized Sharpe from the multiple-testing-corrected published anomaly / intraday-futures / CTA distribution. **Divergence branch:** if |S_A − S_B| > 0.5, `max()` is not taken silently — both surface to the operator, who sets the Cap before Phase 1 (a pre-registered branch, so not a Trap-12 amendment).
- **S_floor (lower edge; reported, sharpens the map, expected non-binding)** = the minimum annualized Sharpe clearing DSR ≥ 0.95 at K = 3,177 / V = 1/n given the micro-era OOS trade count at a frozen frequency set (Anchor C — pure arithmetic, no prior). A clearing region entirely below S_floor is flagged "reachable-but-undemonstrable," not silently counted RESOLVED.

The full method + aggregation/divergence rule freeze in §8 **before** Anchor A or B is computed. This replaces the initial felt cap of SR ≤ 2.0; the operator confirms the *formula*, then the anchors set the number mechanically.

**H-CART:** If ≥1 realism-band-compliant grid point (S_floor ≤ SR ≤ Cap) clears Part A (pooled 3-seed headline bust ≤ 3.0% AND pass ≥ 50%, Run-2 posture) on ≥2 frozen tiers including ≥1 `trailing_locking` at 10k × 3 seeds, then the feasible region is non-empty and the deliverable is the frontier map + minimum-viable-profile table per tier; otherwise the frozen §4 falsifier is unreachable by any realistic candidate and the program's 11-08 outcome is already determined up to gate arithmetic — an operator-level finding, not a license to touch the gate.

**Accept H-CART (RESOLVED)** if: the RESOLVED row of §6 fires.
**Reject H-CART (FALSIFIED)** if: the FALSIFIED row of §6 fires.
**Ambiguous-hold** if: the AMBIGUOUS row of §6 fires (seed-instability at every deciding point).

## §5 — Forbidden moves (each genuinely tempting here)

- **Amending any frozen pre-registration number if the region comes back empty or thin.** The 11-08 deadline makes this the single most tempting move in the program. Ruled out: Trap #12; the survivor pre-reg's only amendment route is its own close-and-re-derive, triggered by *its* clauses (ceiling-mis-set via the §7(9) reference), never by this map.
- **Treating a synthetic grid point that "passes" as §4-falsifier evidence, a scored candidate, or a lifecycle admission.** Tempting because the harness's end-to-end path emits `discharges_falsifier` and the program badly wants a green number before 08-08. Ruled out structurally: the driver calls `run_tier_remc`/`score_part_a`/`score_funded` directly and never `score_candidate` — no report object with that field is ever produced from synthetic input (§10 hook 2 enforces mechanically).
- **Raising the realism cap or extending the grid after seeing near-misses to rescue RESOLVED.** Grid and cap freeze at lock (§8). Refinement inside the pre-registered bounds is permitted for map *resolution*; the §6 verdict is computed on the pre-registered grid only.
- **Substituting friendlier tiers via the harness's `tiers=` override for the headline map.** The harness's own docstring restricts that override to geometry-isolating unit tests; the headline map runs the frozen four verbatim.
- **Reading `compute_default_config()['bust_rate']` anywhere in the driver** (F1 trap — reports ~0% on trailing geometry). Inherited verbatim from the survivor pre-reg §5.
- **Presenting the map as validating any discovery axis's *edge*.** Tempting because axis selection wants a "go" signal. The map bounds risk-geometry feasibility only; edge existence stays owned by Stage 3–7 (cost-law, DSR/SPA, temporal battery).

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition (computed on the pre-registered grid, frozen four tiers, Run-2, pooled 10k × 3 seeds 42/123/2026, horizon 1500, inactivity off, dd_protection off) | Disposition |
|---|---|---|
| `RESOLVED` (region non-empty) | ≥1 grid point with annualized SR ≤ cap clears headline bust ≤ 3.0% AND pass ≥ 50% on ≥2 frozen tiers incl. ≥1 `trailing_locking` | Publish `RESULTS.md` frontier map + minimum-viable-profile table (+ Part-B funded overlay, iso-frequency cost-law overlay, F2 optimism labels on Bulenox/BluSky columns); register as pre-assembled input to the 08-08 packet's axis-selection work; route the §7(9) reference outcome to the survivor pre-reg owner |
| `FALSIFIED` (region empty) | Zero cap-compliant grid points clear that geometry | Surface to operator immediately (before any new campaign pre-registers): the 11-08 §4 falsifier is unreachable for realistic candidates. Any ceiling re-derivation proceeds under the survivor pre-reg's own close-and-reopen — explicitly not under this brief |
| `AMBIGUOUS-HOLD` (frontier unstable) | At every grid point whose clearing status decides between the two rows above, the pooled verdict disagrees with ≥2 of 3 individual seeds, and one pre-registered escalation to 20k sims/seed does not resolve it | Close AMBIGUOUS-HOLD; re-open with a re-specified sims/grid budget in a fresh brief |

Side outcome (routed, not adjudicated here): if the §7(9) calibration reference clears 3.0% on ≥2 tiers, that fires the survivor pre-reg's own AMBIGUOUS ceiling-mis-set clause — report it to the operator under that document's rules.

## §7 — Execution plan (self-executing, single session, CPU-only, $0 data)

- **Phase 0 — freeze (before any measurement).** Re-verify §0 anchors at execution; **operator confirms the §8 realism-band *formula*** (aggregation rule, 0.5 divergence threshold, S_floor frequency set — a formula, not a number); pre-register the §7(9) calibration reference as a Gaussian matched to the falsified locked-book transfer's deployable daily P&L stats (mean, σ from `lab/analysis/c1/tradeify_futures3_remc_2026-07-11/`; fallback SR 0.5 / σ_d $400 / Gaussian, recorded either way); commit §8 — **this commit is the freeze**.
- **Phase 0.5 — compute the anchors (after the freeze commit, before the grid verdict).** Anchor A: `breadth.load_baseline_panel("pepperstone")` (N_eff self-test 3.98/3.09 must PASS first) → per-leg annualized Sharpe via `_sharpe_cols × √252` → S_A = max. Anchor B: the adversarially-verified research note → S_B. Anchor C: scan the production `deflated_sharpe` for S_floor. Apply the §8 formula → (Cap, S_floor); if the divergence branch fires, surface to the operator now. Record all three in the pre-registration §F results annex **before** Phase 1 runs the grid.
- **Phase 1 — generator + driver** at `lab/analysis/gatecart_2026-07/` (new files only). Generator: 2,600 synthetic business days (520 Mon-anchored weeks) of daily P&L in dollars on $100K, generator seed **7**, over the pre-registered grid — annualized SR ∈ {0.25, 0.5, 1.0, 1.5, 2.0} (base rungs; if the Phase-0.5 Cap > 2.0, extend upward in 0.5 steps to the smallest rung ≥ Cap — rule frozen, top data-set); σ_d ∈ {$100, $200, $400, $800, $1,200, $1,600}; shape ∈ {Gaussian; Student-t(df=4) scaled to σ_d; negative-skew two-component Gaussian mixture solved to mean 0/var 1/skew −1.0}. Driver: `load_scoring_thresholds()` → per tier `run_tier_remc` Run-1 and (where `consistency_rule_pct` present) Run-2 → `score_part_a`/`score_funded`; coarse pass at 2,000 sims/seed (harness-sanctioned override).
- **Phase 2 — frontier confirmation.** Re-run every grid point adjacent to a Part-A status change, plus all deciding points, at the frozen 10k × 3; record per-seed spread; apply the §6 escalation (20k) only where the AMBIGUOUS test requires.
- **Phase 3 — report.** `RESULTS.md`: per-tier Run-2 frontier in (SR, σ_d, shape) space; Part-B funded overlay; analytic iso-frequency cost-law overlay (per-trade gross ≥ 4 × 2 × `cost_per_side_usd` at k trades/day, diagnostic only — G2 semantics belong to real candidates); minimum-viable-profile table; Bulenox/BluSky columns labeled optimistic-lower-bound (F2); §7(9) reference outcome.
- **Phase 4 — verdict.** Fire §6 against the numbers; closure record per §9.

Compute envelope: ≤ ~2,200 coarse `run_seed` invocations at 2k sims + frontier set at 10k; no Databento, no vendor CSVs, no `core/` edits, no `ACTIVE_FIRM` touch. **K accounting: zero** — no market data is examined, nothing is mined or selected; no `register_search` opens (the K ledger is untouched; a grep guard in §10 hook 5 keeps this claim honest).

## §8 — Verdict pre-registration (mandatory before Phase 1)

Companion file [`docs/ltm/briefs/pre-registration/Q-GATECART-1-verdict-preregistration.md`](pre-registration/Q-GATECART-1-verdict-preregistration.md) — the §6 table verbatim plus the **frozen realism-band formula** (S_A / S_B / S_floor methods, max() aggregation, 0.5 divergence branch, grid-extension rule), the generator seed, and the §7(9) reference profile — committed at lock, **before Anchor A/B/C or any driver run**. Its §F results annex stays empty at freeze and is filled at Phase 0.5.

Pre-registration commit hash: `<populated at lock>`
Pre-registration date: `<populated at lock>`

## §9 — Closure record format

- RESOLVED → `docs/briefs/closures/Q-GATECART-1-closure-resolved.md` + the RESULTS.md map (the map is the deliverable; no recommendation.md — axis selection stays an operator decision at the 08-08 packet).
- FALSIFIED → `docs/briefs/closures/Q-GATECART-1-closure-falsified.md` + immediate operator surfacing per §6.
- AMBIGUOUS-HOLD → `docs/briefs/closures/Q-GATECART-1-closure-ambiguous.md` with the re-spec budget.

Each records: verdict vs pre-registered triggers, the deciding grid points with pooled + per-seed numbers, §7(9) reference outcome, and any lesson candidate with its dated anchor.

## §10 — Audit hooks (runnable)

```bash
# 1. §0 anchors still resolve to the versions this brief read
git log -1 --format='%h' -- lab/discovery/prop_survivor_scoring.py                       # expect 97011c1 (or a reviewed successor)
git log -1 --format='%h' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md  # expect be6dda6 — FROZEN means unchanged

# 2. Driver never touches the candidate-scoring path or the F1 trap (forbidden-move guards)
grep -rn "score_candidate\|discharges_falsifier\|compute_default_config\|bust_rate" lab/analysis/gatecart_2026-07/ && echo "VIOLATION" || echo "clean"

# 3. Headline map ran the frozen four tiers verbatim
grep -rn "Bulenox_100K\|Tradeify_Select_100K\|MFFU_Rapid_100K\|BluSky_Premium_100K" lab/analysis/gatecart_2026-07/  # expect all four in the driver

# 4. The frozen ceilings were not re-decided anywhere in this workstream
grep -n "3.0%\|1.0%\|≥ 50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md   # unchanged

# 5. Zero-K claim holds — no discovery manifest was opened for this run
ls discovery_manifests/ | grep -i "gatecart" && echo "VIOLATION: K was consumed" || echo "clean"

# 6. The map actually fed the 08-08 packet (Trap #10 — artifacts nobody re-reads)
grep -rn "Q-GATECART-1" docs/SESSIONS.md docs/briefs/2026-07-12-08-08-packet-pretriage.md  # the 08-08 session must cite it
```

## Verification

```bash
# Discipline checks (mechanical)
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/Q-GATECART-1-survivor-gate-cartography.md --type inquire

# Production-source verification (Rule 0 confirmation)
git log -1 --format='%h %ci' -- lab/discovery/prop_survivor_scoring.py                    # 97011c1
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md  # be6dda6
git log -1 --format='%h %ci' -- core/mc/preflight.py core/firm_rules.py                   # a53ee99

# Cross-reference verification (cited facts match canonical sources)
grep -n "bust ≤ 3.0%\|P(pass) ≥ 50%\|42/123/2026\|horizon \*\*1500\*\*" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md
grep -n "NO_PROTECTION_TRIGGER = 10.0" lab/discovery/prop_survivor_scoring.py
grep -n "17.70\|17.7" lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md           # ceiling-calibration anchor
grep -n "HARD gate" docs/adr/2026-07-13-harv-discovery-lane-ratification.md

# Pre-registration commit verification (at lock)
git log --oneline docs/ltm/briefs/pre-registration/Q-GATECART-1-verdict-preregistration.md    # must predate first driver run
```

---

## Lock / closure record (was the pre-lock checklist)

- [x] All §0 paths read and anchored with commit hashes (this session, 2026-07-14)
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 hypothesis binary via §6 triggers
- [x] §5 forbidden moves genuinely tempting (deadline-pressure gate-softening is the live one)
- [x] §6 gates numerically specific
- [x] **Operator confirmed the §8 realism-band FORMULA 2026-07-14** (aggregation + 0.5 divergence + S_floor frequency set) — the divergence branch then fired as designed
- [x] §8 companion pre-registration committed (freeze **453148a**) BEFORE all three anchors — verified (§B byte-stable post-freeze)
- [x] **CLOSED-FALSIFIED at Phase 0.5** — the realism band came back empty at K=3,177; the Phase-1 grid was never run (moot at the banked K). Follow-on K-budget-as-axis-gate question forked to the STATE forward board, not this brief.
- [ ] §10 hooks re-run at closure
- [ ] Verification block executed at lock
