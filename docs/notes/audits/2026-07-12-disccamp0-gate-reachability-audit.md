# Audit Note — DISC-CAMP-0 pre-freeze gate-reachability audit (Q-HARV-0 obligation)

**Audit ID:** AUDIT-2026-07-12-disccamp0-gate-reachability
**Date:** 2026-07-12
**Triggered by:** scheduled pre-freeze obligation (Q-HARV-0 lesson; the "pre-run gate-reachability audit on DISC-CAMP-0" queued in the Gen-2 autonomy map)
**Authors:** Joshua (operator) + Claude (advisor; 21-agent verification workflow)
**Scope:** single pre-registration — `docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md` §3 gate table (9 gates)
**Lives in:** `docs/notes/audits/2026-07-12-disccamp0-gate-reachability-audit.md`

> **Headline disposition: FREEZE-BLOCKED.** DISC-CAMP-0 must NOT be frozen (no
> `register_search open`, no first `db_fetch pull`) as written. The Q-HARV-0
> obligation fired **before K was committed**, as designed. Four corrections are
> required first (§5); one of them (the DSR-0.95 default) requires a **superseding
> ADR**, not a pre-registration edit. DISC-CAMP-0 does **not** carry the *specific*
> Q-HARV-0 bug (placebo ⊂ conditioning) — its IS/OOS geometry is clean — but it
> carries three defects of the same family: an effectively-unreachable RESOLVED
> path, three underspecified gates, and gate code that does not exist.
>
> **ADDENDUM (2026-07-12, same session, post-audit).** Two things changed *after* this
> audit's body was written, both incorporated by the follow-on work rather than by
> editing the findings below: (1) `universe_gate.py` + `temporal_consistency.py`
> **landed mid-session** (PR #337/#339, merged into this worktree) — the §4/§5
> "code does not exist" finding is superseded (Stage 5/6 code now exists; REGIME/CUSUM
> gained numeric predicates), though the K-rule finding is confirmed **still live**
> (pre-reg K rule byte-unchanged, K still `[PENDING]`). (2) Reading the now-landed
> `universe_gate.py` surfaced a **second, independent DSR defect** not in the original
> body: its default empirical `V` (across-trial Sharpe variance) estimator is biased
> upward by the very edge it scores and collapses to vacuous at `K_SPA=1`. Both defects
> are now fixed by
> [`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md)
> (`Accepted`, operator ratified 2026-07-12, PR #341 merged: non-overlap-floor K +
> unconditional `V=1/n` pin, empirically validated against the live module; the
> `var_trials` override landed in `universe_gate.py`, 12/12 tests green). The
> Stage-2/4 runner is delegated to Cursor
> ([`2026-07-12-cursor-handoff-stage-2-4-runner.md`](../../briefs/rnd-pipeline/2026-07-12-cursor-handoff-stage-2-4-runner.md),
> dispatched 2026-07-12, not yet landed).
> **FREEZE-BLOCKED still holds** pending the runner landing + a Stage-7 realism engine;
> see `STATE.md` and `[[project_disccamp0_gate_reachability_audit]]`.

---

## §0 — Source anchors

Read via filesystem this session (2026-07-12) in worktree branch
`claude/stage-runner-gate-reachability-8569df`, `git rev-parse --short HEAD` = **`05ea80d`**.
All numerics below reproduce against the cited engine; the audit's arithmetic was
independently re-derived by adversarial verifier agents against the real module.

- `docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md` — the frozen §3 gate table (9 rows), §2 K rule (`K = 22 + 3·N_subseq`), §4 block-size rule. The artifact under audit.
- `docs/ltm/briefs/rnd-pipeline/DISC-CAMP-0-shakedown.md` — campaign narrative; §6 verdict semantics (FALSIFIED = shakedown success), §7 stages 0–8.
- `docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md` — `§Campaign-defaults` (canonical gate definitions #3 universe correction, #4 temporal battery, #5 decay monitor).
- `docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md` — ratifies the defaults as standing policy; §4 falsifier ("DSR-0.95 shown mis-calibrated for the realized trial economics" → superseding ADR).
- `lab/research_utils/deflated_sharpe.py` — DSR engine. `SR0 = √V·[(1−γ)·Φ⁻¹(1−1/K) + γ·Φ⁻¹(1−1/(K·e))]`; `DSR = Φ((SR−SR0)·√(n−1)/√denom)`. Every DSR numeric reproduces against this file (scipy backend).
- `lab/validation_selftest.py` — positive/negative synthetic controls; the positive control uses only **K=50 trials** (`generate_positive_control(n_trials=50)`).
- `lab/discovery/register_search.py` — K-ledger; `open` binds K immutably; docstring: the Bonferroni/BH floor is "the CHEAP triage… NOT the rigorous gate."
- `lab/archive/harv_0_month_end_rebalance_es_2026-07/run_harv0.py` — the only ad-hoc Stage-2/4 precedent, and the study whose placebo-⊂-conditioning bug produced the gate-reachability lesson.
- **Absence confirmed by glob** (`**/{universe_gate,temporal_consistency}.py` → zero hits): the Stage-5 universe gate and Stage-6 temporal battery **do not exist** in this worktree. `lab/discovery/` contains only `register_search.py` + `__init__.py`.

**Failure class:** Methodology failure (a discipline — the pre-freeze reachability
simulation — that the pre-registration process does not yet enforce) **caught in time**
rather than after the fact. This is the "gate we'd-never-PASS" mirror of
programme-audit's falsifier-drift, per `[[lesson_gate_reachability_preregistration]]`.

---

## §1 — Trigger

The Gen-2 autonomy map (2026-07-12) named a standing obligation before DISC-CAMP-0
locks: *"pre-run gate-reachability audit on DISC-CAMP-0 (Q-HARV-0 obligation;
universe-correction clauses proven reachable via positive control, temporal clauses
need Track B)."* The Q-HARV-0 lesson (2026-07-12) is the anchor: a frozen bundled gate
can be **structurally un-passable at registration** even after a correct
freeze-before-contact, and the obligation is to *simulate every bundled clause under
(a) the null and (b) a plausible-true-mechanism world before freezing — if a clause
cannot pass under (b), fix the geometry before K is committed.* This audit discharges
that obligation for DISC-CAMP-0's 9 pre-registered gates.

---

## §2 — What actually happened (method + reconciliation)

1. **Rule-0 reads** of the pre-registration, shakedown, template, defaults-ADR, both
   gate handoffs, and the four engine/ledger files (§0). Confirmed the campaign is
   still pre-lock: the three `[PENDING]` data-derived integers (campaign-local K,
   `block_size`, summed estimate) are unbound; no pull has run.
2. **Grounded numerics** computed against `deflated_sharpe.py`: the GC 1h IS window
   (2010–2018, ~23h/day) is ≈ 52,164 bars → `N_subseq ≈ 52k` per STUMPY window →
   `K = 22 + 3·N_subseq ≈ 156,500` (the cumulative-family K the DSR gate consumes).
3. **Per-gate reachability analysis** (one agent per gate) under the null and a
   plausible-true GC 1h edge (per-trade Sharpe ∈ [0.05, 0.20]; OOS trade count
   n ∈ [100, 1000] since matrix-profile motif/discord signals are rare), each with the
   specific Q-HARV-0 geometry check (control window ⊂ conditioning window? magnitude
   clause sign-aware?).
4. **Adversarial verification** of each finding (a second agent tasked to *refute*).
   Every load-bearing numeric reproduced exactly against the real engine. One finding
   was overturned by its verifier (DROPTOP — see §3).
5. **Cross-cutting synthesis** (bundle-conjunction, effective-K, SPA-K vs DSR-K,
   shakedown-branch coverage, code-absence) and a **runner-scope red-team** that
   verified the obvious fix to the K defect is self-contradictory (§4).

**Reconciliation note:** the mid-workflow bundle synthesis leaned "freeze with fixes,"
contingent on an effective-K patch. The final red-team (verified against the engine)
demolished that patch. This audit therefore escalates to **FREEZE-BLOCKED**: the DSR
defect is not patchable inside the pre-registration; it re-opens a ratified default.

---

## §3 — Per-gate reachability findings

**Hypothesis under audit — H:** every frozen §3 gate is *reachable* — a genuinely-true
GC 1h edge of plausible magnitude can pass it. **H is FALSIFIED for DSR** (and SPA is
near-vacuous) and **untestable as-written for REGIME/CUSUM/REALISM** (§4).

Reachability = can a **genuinely-true** edge of plausible magnitude pass this gate?
(The mirror question to "does the null correctly fail.")

| # | Gate (§3 row) | Reachability (verified) | Severity | Note |
|---|---|---|---|---|
| 1 | **SPA** (family p<0.05) | **MARGINAL** | CONCERN | Near-**vacuous** at low candidate count: a matrix profile emits ~1 motif/discord per window, so the scored-candidate set is single-digit; with M=1, SPA degenerates to a raw bootstrap p (zero multiplicity protection). The multiplicity burden collapses onto DSR. |
| 2 | StepM (superior set) | REACHABLE | CONCERN | Conditional ("if >1 survives SPA"); mechanically sound. |
| 3 | **DSR ≥ 0.95** | **MARGINAL→UNREACHABLE** | **CONCERN (load-bearing)** | Dominant erosion. At the frozen K≈156k a true edge needs per-trade Sharpe **0.28 (n=500) / 0.63 (n=100)** — above the plausible-true ceiling 0.20. See §4. |
| 4 | PBO < 0.5 | REACHABLE | CONCERN | The *inverse* of un-passable — a true edge passes easily; conditional on config selection occurring. |
| 5 | Sign consistency ≥5/7 | REACHABLE (n≥500) | CONCERN | Binomial: reachable once per-year P(year>0) ≥ ~0.70, i.e. per-year SNR is adequate; tightens for low-n signals. |
| 6 | Drop-top-year | REACHABLE | CLEAN | Verifier **refuted** the initial "underspecified" reading via Rule-0 read: "> gate" is well-defined (the same edge threshold with the best OOS year removed). A stable edge passes; a one-year artifact fails by design. |
| 7 | **Regime-slice survival** | **UNDERSPECIFIED** | CONCERN | Prose-only in all four sources ("edge positive across ruptures/HMM slices"); no slice count, no "all vs majority" rule, no engine. An unspecified conjunction cannot be reachability-tested — and if read as "all slices positive," it inherits the book's own documented reality that *nothing in this asset family has ever been regime-robust*. |
| 8 | **Own-edge CUSUM** | **UNDERSPECIFIED** | CONCERN | No pinned threshold; "null calibrated during validation" points at `temporal_consistency.py` (Track B) which **does not exist**. |
| 9 | **Native-micro realism** | **UNDERSPECIFIED** | CONCERN | The **only** §3 row with no pass predicate. Economic reachability is genuinely doubtful: cost-in-R ∝ price/stop; precedent DJ30→MYM died at OOS PF ratio 0.559 on *structural* venue costs. |

**Geometry (the specific Q-HARV-0 bug): CLEAN.** No control/placebo window sits inside
a conditioning/selection window. IS (2010–18) and OOS (2019+) are temporally disjoint;
the negative control is a separate synthetic family. The reachability risk here is
**magnitude/power and specification**, not the Q-HARV-0 selection-geometry overlap.

**Bundle (the conjunction).** RESOLVED requires SPA ∧ DSR ∧ sign ∧ drop-top ∧ regime ∧
CUSUM ∧ realism. Modeling per-gate pass-probabilities for a *genuine* edge, the non-DSR
conjunction alone multiplies to ≈ **0.165** (regime-slice ~0.55 and MGC-realism ~0.65
dominate that erosion). Joint reachability = P(pass DSR) × 0.165:
- optimistic (SR 0.20, n=1000): ≈ **0.09**
- realistic motif (SR 0.20, n=500): ≈ **0.007**
- weak (SR 0.10, n=500): ≈ **0.000**

**RESOLVED is effectively unreachable for realistic edges** → FALSIFIED is the
near-certain close *regardless of ground truth*.

---

## §4 — Root cause (why DSR ≥ 0.95 is malformed for this family)

- **Immediate cause.** `K = 22 + 3·N_subseq ≈ 156,500` treats every overlapping
  matrix-profile subsequence position as an independent trial. LdP's `SR0` assumes
  **independent** trials, so the raw count over-deflates: at V=1/n, `SR0(156k, n=500) =
  0.201` → DSR≥0.95 hurdle **0.276** vs 0.176 at K=50 (both reproduced against
  `deflated_sharpe.py`).

- **The obvious patch fails (verified).** The tempting fix is an effective count
  `Keff_MP = 3·(N_subseq/L)` where L is the return-ACF decorrelation length — reusing
  the ACF the Stage-5 block-size rule already needs. **This is self-contradictory.**
  `Keff` is *decreasing* in L, but §4 freezes `block_size` as "the smallest lag where
  the ACF first enters the white-noise band" — which for 1h *returns* is small (returns
  are near-white; long memory lives in |returns|). Small L → `Keff` in the tens of
  thousands → hurdle 0.25–0.27, still unreachable. The `Keff ≈ 200` that would make DSR
  passable needs L ≈ 780 (a ~32-day decorrelation — an invalid block size). The
  statistically correct decorrelation scale for overlapping m-bar windows is the window
  length m (windows independent once non-overlapping) → the non-overlap floor
  ≈ Σ(T/m) ≈ 3,200, at which the hurdle is **0.233 — still > 0.20**. There is **no honest
  effective-K** that makes DSR≥0.95 reachable at the plausible-true ceiling for n=500,
  and it is unreachable for the whole honest-K range at **n ≤ 250**.

- **Structural cause.** `DSR ≥ 0.95` (ratified **Campaign-default #3**, standing policy
  across all campaigns) is **mis-calibrated for a discovery family whose trial count is
  dominated by autocorrelated matrix-profile subsequences and whose OOS signals are rare
  (low n).** It is the exact "gate we'd-never-PASS" the Q-HARV-0 lesson names. Fixing it
  inside the pre-registration by choosing a convenient K would *install* the malformed
  geometry the lesson exists to prevent (best-of-K K-selection as a freeze gate). This
  trips the defaults-ADR §4 falsifier ("the DSR-0.95 threshold is shown mis-calibrated
  for the realized trial economics"), whose remedy is a **superseding ADR**, not an
  in-place edit.

- **Secondary structural cause.** The pre-registration calls both the DSR denominator
  and the SPA input "the K-column matrix," conflating two distinct selection events
  (`K_DSR` = search-magnitude *count*; `K_SPA` = the handful of *scored return series*).
  This overstates protection: at low `K_SPA`, SPA is near-vacuous, so DSR carries the
  entire multiplicity burden — at a mis-calibrated denominator.

- **Verifiability gap.** With `universe_gate.py` and `temporal_consistency.py` absent,
  **no gate can be reachability-tested end-to-end**, the campaign-K positive control
  cannot be run (the existing control is K=50 only — it does *not* certify reachability
  at K≈156k, exactly where the hurdle bites), and the shakedown's *primary* deliverable —
  the process-defect log — cannot be produced because there is no code to exhibit the
  defects. A freeze here commits thresholds against vaporware.

- **Shakedown consequence.** Because RESOLVED is effectively unreachable, the shakedown
  will close FALSIFIED whether or not a real GC edge exists, so the **promote branch**
  (Stage-8 breadth → mechanism → strategies-never-locked CANDIDATE intake, plus the
  Stage-6d decay-monitor ship) is **never exercised on real inputs**. "Pipeline
  validated" would be only half-proven — defeating the shakedown's stated purpose.

---

## §5 — Repair plan

### Immediate (before any freeze / `register_search open` / first `pull`)

- [ ] **Do not commit the freeze.** Hold DISC-CAMP-0 at pre-lock until (1)–(4) land.
- [ ] **(1) Re-open the DSR clause via a superseding ADR** to the ratified defaults.
      Options to weigh in that ADR (not in the pre-reg): (a) re-baseline `K_DSR` to a
      principled effective-independent-trial count with a **stated, non-outcome-selected
      rule** (the non-overlap floor Σ(T/m) is the defensible upper bound; the return-ACF
      reuse is invalid — do not adopt it); (b) re-baseline the DSR threshold for
      low-n/autocorrelated-search discovery families; or (c) accept that DSR≥0.95 is a
      *survival* gate this family cannot clear and route discovery survivors through a
      different admission bar. **Report the K bracket {non-overlap floor, raw 156k}
      together; bind the honest denominator, never the one that happens to pass.**
- [ ] **(2) Specify the three UNDERSPECIFIED gates** with frozen predicates: regime-slice
      (slice source, count rule, all-vs-majority, threshold), CUSUM (h/k and the
      calibration procedure), native-micro realism (the numeric pass predicate — the only
      §3 row without one). An unspecified gate cannot be frozen *or* reachability-tested.
- [ ] **(3) Disambiguate `K_SPA` (scored-candidate columns) from `K_DSR` (search size)**
      in the pre-reg; state that SPA is near-vacuous at low candidate count so DSR carries
      multiplicity — stop presenting SPA as independent protection it does not provide.
- [ ] **(4) Build the Stage-5 universe gate + Stage-6 battery** (`universe_gate.py`,
      `temporal_consistency.py`) and run a **campaign-K synthetic-positive** end-to-end
      (inject a known edge; confirm it clears the corrected gates, reaches Stage-8 breadth
      with a real N_eff delta, emits the Stage-6d monitor, and lands a CANDIDATE). This is
      the only proof of the promote branch the expected FALSIFIED close never exercises,
      **and** the reachability attestation the freeze is blocked on. Needs no market data
      (see the Stage-2/4 runner handoff, `docs/briefs/rnd-pipeline/2026-07-12-cursor-handoff-stage-2-4-runner.md`).

### Structural (prevent the next campaign from hitting this)

- [ ] **Add a "gate-reachability attestation" step to the discovery-campaign template**
      (Stage 0/Register): before freeze, every bundled clause must be shown to pass a
      campaign-K synthetic-positive under a plausible-true edge, with the effect-size and
      n assumptions recorded. Freeze-before-contact is necessary but not sufficient — a
      frozen gate can still be un-passable by construction.
- [ ] **Template: forbid raw subsequence counts as a DSR denominator** for
      matrix-profile/motif search; require an effective-independent-trial rule pinned
      pre-result, with the {effective, raw} bracket reported.
- [ ] **check_brief / campaign lint:** flag any §3 gate row lacking a numeric pass
      predicate (the REGIME/CUSUM/REALISM prose-only rows would have tripped it).

If no structural repair ships, the next discovery campaign re-hits the same
inflated-K / unspecified-gate trap.

---

## §6 — Lessons to capture

- **Candidate lesson (already covered — reinforce, do not duplicate):** a frozen
  bundled gate can be un-passable by *magnitude/power geometry*, not only by
  selection-window overlap. Q-HARV-0 was the placebo-⊂-conditioning shape; DISC-CAMP-0 is
  the **inflated-K-denominator × low-n** shape and the **conjunction-erosion** shape.
  Anchor: this audit. Cost/counterfactual: would have spent the GC/MGC family's entire
  cumulative K (banked whether the campaign resolves or is abandoned) on a campaign whose
  RESOLVED answer space was ≈1% reachable — and validated only half the pipeline.
  Registry: extend `[[lesson_gate_reachability_preregistration]]` with the two new shapes
  (a bracketed pointer, not a new entry — same lesson, wider surface).

- **Candidate lesson:** "effective independent trials, not raw search count, is the DSR
  denominator for autocorrelated search spaces (matrix profiles, overlapping windows,
  grid neighbours)." Anchor: this audit + the verified `SR0`-vs-K table. Registry:
  `docs/methodology/lessons/methodology_lessons.md`. Promotion status: Candidate (one
  firing; structural-argument approval on the LdP-independence assumption).

---

## §7 — Programme-audit signal check (cross-skill)

- [x] **Falsifier thresholds drifting toward "we'd never hit this."** DSR≥0.95 at
      K≈156k is the *inverse* — a gate a true edge would never *pass*. Same degeneration
      family (a threshold decoupled from realized economics), opposite sign. **Escalate**
      the DSR-0.95 default to programme-audit at the 2026-08-08 quarterly (it is the
      defaults-ADR §4 falisifier's named trigger).
- [ ] Belt-patches without corroboration — N/A (this audit prunes, it does not patch).
- [ ] Belt that only grows — N/A.
- [x] **Methodology invoked to rationalize a decision already made** — the *runner design*
      tried this (a convenient `Keff` to make the campaign freezable); the red-team caught
      it. Not shipped. Flag as a near-miss, not a live defect.
- [ ] SNAG pattern — N/A (first discovery campaign under the stack).
- [ ] Cross-layer contamination — N/A.
- [ ] Negative heuristic crossed without repair — N/A (caught pre-freeze).

The DSR-0.95 escalation makes this audit an **input to the 2026-08-08 quarterly
programme audit** of the ratified Campaign defaults; do not consider the structural
repair closed here.

---

## §10 — Audit hooks (forward-looking)

```bash
cd "C:/Users/joshu/multi_firm_operations"

# FREEZE-BLOCKED must hold: no open/manifest, no pull, integers still [PENDING]
ls discovery_manifests/disccamp0_gc_2010_18.json 2>/dev/null && echo "VIOLATION: campaign opened before fixes" || echo "ok: not opened"
grep -n "PENDING" docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md   # expect the 3 integers still PENDING

# (2) the three prose-only gates must gain a numeric predicate before freeze
grep -nE "Regime-slice survival|Own-edge CUSUM|Native-micro realism" docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md
# review: each row must carry a frozen threshold/engine, not prose only

# (4) the gate code must exist before the campaign-K synthetic-positive can run
ls .claude/skills/strategy-validation/scripts/universe_gate.py lab/**/temporal_consistency.py 2>/dev/null || echo "still absent — reachability untestable end-to-end"

# (1) the DSR re-open must be a superseding ADR, not a silent pre-reg edit
ls docs/adr/*discovery-campaign-defaults* docs/adr/*dsr*  2>/dev/null

# Reproduce the load-bearing DSR reachability numeric (independent of any repo state)
python - <<'PY'
import math; from scipy.stats import norm
G=0.5772156649015329; E=math.e
def sr0(K,V): 
    s=math.sqrt(V); return s*((1-G)*norm.ppf(1-1/K)+G*norm.ppf(1-1/(K*E)))
for K in (50,3200,156500):
    for n in (100,250,500,1000):
        s=sr0(K,1/n); print(f"K={K:>6} n={n:>4} DSR>=0.95 hurdle={s+1.645/math.sqrt(n-1):.3f}")
PY
# Expect: all hurdles at K in {3200,156500}, n in {100,250,500} exceed the plausible-true ceiling 0.20

# Recurrence check schedule: 2026-08-08 quarterly programme audit — re-run §7 DSR-0.95 escalation
grep -rn "AUDIT-2026-07-12-disccamp0" docs/ .claude/skills/  # expect this audit + any graduated lesson pointer
```

---

## §11 — Closure

- **Status:** `Open (immediate repair pending operator go on (1)–(4); structural repair deferred to 2026-08-08 quarterly)`
- **Disposition:** **FREEZE-BLOCKED** — DISC-CAMP-0 not to lock until §5 (1)–(4) land.
- **Immediate repair completed:** — (pending)
- **Structural repair completed:** — (deferred to 2026-08-08 quarterly programme audit of the ratified defaults)
- **Follow-up triggered:** (a) superseding ADR for Campaign-default #3 (DSR); (b) the Stage-2/4 runner + gate code (`2026-07-12-cursor-handoff-stage-2-4-runner.md`); (c) programme-audit escalation of DSR-0.95 at 2026-08-08.

---

## Verification

```bash
# Discipline check — skill-side is authoritative for the 'audit' type (repo-side maps audit->generic)
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/notes/audits/2026-07-12-disccamp0-gate-reachability-audit.md --type audit
# Expected: PASS (6/6). Repo-side `scripts/check_brief.py --type audit` also green (H: token present).

# §0 anchors resolve
git rev-parse --short HEAD                                   # 05ea80d (or descendant)
ls docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md lab/research_utils/deflated_sharpe.py

# Absence claim (Stage-5/6 gate code) still holds
ls .claude/skills/strategy-validation/scripts/universe_gate.py 2>/dev/null || echo "confirmed absent"
```
