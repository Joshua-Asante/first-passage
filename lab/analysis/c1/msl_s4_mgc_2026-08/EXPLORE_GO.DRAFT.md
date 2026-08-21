# MSL-S4 — Explore-confirm GO draft (UNPAID)

**Status:** `DRAFT` — operator explore GO **unpaid**. Promote = copy this file to
`EXPLORE_GO.md` (gitignored) and add a first-line stamp `ISSUED YYYY-MM-DD`.
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`STAGE1.md`](STAGE1.md)
**Supersedes-in-design (not in freeze):** the informal 2026-08-21 cheap falsifier's naive
fixed-offset control window — [`LOG.md`](_cheap_falsifier_expiry_oi_strike_convergence_2026-08-21_LOG.md)'s
own addendum found that control trend-confounded (same cycles converged/diverged in both arm and
control). This document is the corrected, pre-registered design; the cheap falsifier itself stays
frozen and unedited as the historical record it is.
**Harness:** [`explore_confirm_lib.py`](explore_confirm_lib.py) (statistical core, unit-testable
without vendor data) · [`test_explore_confirm_lib.py`](test_explore_confirm_lib.py) (23/23 passing
on synthetic fixtures, including a power check against an injected synthetic convergence signal
and a false-positive check against pure autocorrelated noise). **No pull-and-run driver script
exists yet** — this environment has no `DATABENTO_API_KEY`; a local session with data access
writes the driver (extending `_cheap_falsifier_expiry_oi_strike_convergence_2026-08-21.py`'s
proven cycle-discovery pattern to weeklies + the partitions below) as its first step under this
token, not before.
**Cost / K at draft:** $0 · K=0. Nothing scored until `--explore-go` after promote and a driver
exists. A Databento cost `estimate` is still owed before any full pull — the schemas involved
(`definition`/`statistics`/`ohlcv-1d`) have priced at $0 in every precedent this repo has run
(including the cheap falsifier itself), but "estimate first" is this program's standing rule, not
optional because of precedent.

---

## Promote rule (operator)

1. Confirm `DATABENTO_API_KEY` is set in the executing environment.
2. `cp EXPLORE_GO.DRAFT.md EXPLORE_GO.md` and stamp `ISSUED <date>` on line 1.
3. Write the driver script (cycle discovery + pull, per §Universe below) — not yet written; this
   token authorizes writing it, not a pre-existing script.
4. Run the pilot phase (§Diagnostic gate) on live data **before** drawing the official IAAFT seed
   block. No parameter movement after the pilot without a fresh addendum, append-only, mirroring
   `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`'s own D6 ordering.
5. Do **not** author a second Pine version / re-TV / touch survivor MC until the explore gate is
   `SHAPE-CLEAR` (or operator kill).

---

## Partitions — corrected for what's already been viewed

**What's already been looked at, and why it can't be blind CONFIRM anymore:**

| Source | Window touched |
|---|---|
| Operator TV backtest (screenshot, this session) | Chart date range set to **2025-09-30 → 2026-08-21** |
| Cheap falsifier (`_cheap_falsifier_..._2026-08-21.py`) | 7 monthly OG cycles, arm/control windows spanning roughly **2026-01-08 → 2026-07-28** |

Both sit inside the wider TV range. **The entire 2025-09-30 → 2026-08-21 window is excluded from
both IS and CONFIRM below** — not reused for IS (an informally-viewed window is not blind, but
IS was never blind to begin with, so reuse there isn't the harm; excluding it anyway keeps the
accounting simple and avoids ever citing "IS included the window the cheap falsifier read" as a
future ambiguity) and obviously excluded from CONFIRM (a peeked window cannot be a holdout).

| Partition | Window | Note |
|---|---|---|
| **IS** | **2024-01-01 → 2025-03-31** | Starts at the CME weekly-options-expansion era (2024) so weeklies are dense throughout, not just for a partial window — see §Universe |
| **CONFIRM** | **2025-04-01 → 2025-09-29** | **RESERVED UNREAD** through step 8. Ends the day before the already-viewed window starts — genuinely untouched by either the TV backtest or the cheap falsifier |
| Excluded (already viewed) | 2025-09-30 → 2026-08-21 | Neither IS nor CONFIRM. Not reused for scoring under any framing |
| Live / forward | after 2026-08-21 | Out of scope for this token — a future OOS check, not this Explore-confirm |

Any CONFIRM peek voids the holdout, same as every other MSL card.

---

## Universe — weeklies now included, discovered live (not hardcoded)

The cheap falsifier used monthly OG cycles only (n=7, explicitly disclosed as underpowered).
CME's 2024 weekly-options expansion means Gold options now list expiries most business days —
including weeklies is not optional if this test is to have real power, and n=7 cannot support a
significance test regardless of which null is used.

- **Discover, don't hardcode**: pull `OG.OPT` `definition` snapshots (free schema, exact
  real strikes/expirations) across the IS+CONFIRM span and enumerate every distinct listed
  expiry — monthly and weekly alike — mirroring `find_cycles()`'s proven pattern in the cheap
  falsifier, not a guessed ticker list.
- **n-floor**: 20 completed cycles minimum in IS before any score is trusted
  (`explore_confirm_lib.explore_verdict`'s `n_floor` — VOIDs below it). Expected actual count
  given weekly density: on the order of 60-90 cycles over the 15-month IS window — an order of
  magnitude past the floor, not a near-miss.
- Reference level, arm window, displacement threshold: unchanged from `PREREG_G0.md` §1
  (highest-OI strike ~3 sessions before expiry; final 3 sessions armed; MGC proxy via GC parent
  price per §6).

---

## The corrected null — IAAFT-surrogate significance test (PRIMARY gate)

**Why not just fix the control window's offset:** the cheap falsifier's control (same-length
window, fixed 10 sessions earlier) turned out to move with whatever multi-week trend the cycle
sat in — the *same* cycles converged and diverged in both windows. Any single fixed-offset
control inherits this: there is no offset that reliably decorrelates from a multi-week trend
without also discarding real information. A surrogate-based null sidesteps the problem entirely
by asking a sharper question directly: does the real series, against its *own* strikes and *own*
expiry dates, converge more than a large ensemble of price paths that share its exact
autocorrelation and marginal structure but have no expiry-specific mechanism baked in?

**Method** (adapted from the corrected-null-battery's own proven IAAFT approach — same generation
discipline, different statistic): IAAFT (Schreiber–Schmitz) surrogates of the real GC daily
log-return series over IS, generated in the **normal-scores domain by default**
(`explore_confirm_lib.generate_surrogate_returns`) — matching the battery's own finding that raw-
domain IAAFT is empirically disqualified for skew/spike-inflated series; returns are less skewed
than the battery's True-Range series, but normal-scores is adopted as the safe default rather
than re-deriving the raw-vs-normal-scores question from scratch on a series this repo has never
run the comparison on. Each surrogate return series is exponentiated into a surrogate GC price
path (`start_price * exp(cumsum(surrogate_returns))`), and the **same real strikes and real
expiry-relative window indices** are scored against it — only the price *path* is surrogated,
strikes/dates are held fixed, which isolates exactly the variable in question (see
`explore_confirm_lib.iaaft_significance_test`).

**Statistic:** `mean_displacement_reduction` (primary) — mean across IS cycles of
`(disp_start − disp_end)`, positive = net convergence. `convergence_rate` disclosed alongside,
never gating (a rate can be pulled by outlier magnitude the way the mean can be pulled by a
skewed count — report both, gate on the mean).

**M = 1000, seed block `[20260821, i]` for i=0..999** (disjoint from the pilot-verification block
`[20260821, 990000+i]` — mirrors the battery's own disjoint-seed-provenance convention exactly,
same rationale: the official draw must be provably unaffected by whatever seeds were used to
verify the implementation).

**p_upper = (1 + #{null ≥ real}) / (M+1)** — tests whether real convergence exceeds generic
autocorrelated price dynamics. **No M escalation on a near-miss** — report, never re-roll, same
rule as the battery.

### Diagnostic gate — what's frozen here, what's pilot-calibration-owed

Frozen now: the **structure** of the gate (rank-ACF fidelity check must pass on the pilot draw
*before* any official hit rate is computed; convergence diagnostic written to disk first;
escalation ladder on failure: `n_iter=100` default → `n_iter=500` → Schreiber end-matching trim
→ **VOID**). This mirrors `explore_confirm_lib.IAAFT_ITER_DEFAULT` /
`IAAFT_ITER_ESCALATED` and the battery's own §1 escalation ladder exactly.

**Not frozen, and deliberately not invented here:** the exact numeric tolerance (the battery's own
0.04 median / 0.07 p95 rank-ACF-delta thresholds were calibrated *for its own True-Range series*
via a 4-lens design panel with live experiments — reusing those numbers for a differently-shaped
series without the same calibration would be exactly the kind of borrowed-number error this
program's own culture treats as a real defect, not a shortcut). **The pilot phase's first job is
running `explore_confirm_lib.surrogate_diagnostic` on real GC returns and freezing a tolerance
before drawing the official seed block** — an explicit, named, owed step, not an oversight.

---

## Req 1a — Delete / Flip (distinct from the IAAFT null)

The IAAFT null answers "is this real, vs. generic price dynamics." Delete/Flip answers "does the
*specific* mechanism claim (OI-derived strike selection; convergence not divergence) matter" —
both owed, neither substitutes for the other.

### DELETE

Same window/threshold/geometry, but the reference level is the **60-session trailing median
price** at each cycle's arm-window open (a generic technical level, uncorrelated with published
OI) instead of the real highest-OI strike.

- `delete_pass(constrained_stat, sham_stat)` — **PASS** iff the true-strike statistic beats the
  sham-reference statistic (strict inequality; NaN ⇒ not PASS). Mirrors MSL-C2's own convention
  exactly (`construct_lib.delete_pass`).
- **FAIL** ⇒ not SHAPE-CLEAR — the OI-derived selection isn't doing real work if a generic level
  converges just as well.

### FLIP

Same displaced-cycle population, but bet on **divergence** (short below the strike, long above)
instead of convergence.

- `flip_pass(converge_stat, diverge_stat)` — **PASS** iff convergence beats divergence (strict).
- **FAIL** ⇒ not SHAPE-CLEAR — the construct's own worked distinction from its dead directional
  sibling (§Rejected nearest classes, `MECHANISMS.md`) was that convergence and divergence are
  *distinguishable* hypotheses here, unlike the sibling's unobservable sign. FLIP-FAIL means that
  distinction didn't cash out empirically.

---

## Primary / aux limbs

| Limb | Definition |
|---|---|
| Primary | IAAFT `p_upper` on `mean_displacement_reduction` (§The corrected null) |
| Delete | `delete_pass` vs. 60-session trailing median sham (§Req 1a) |
| Flip | `flip_pass` vs. divergence arm (§Req 1a) |
| DSR | ≥ **0.650** at `K_intrinsic=1` (disclosure floor, unchanged from `PREREG_G0.md`) |
| Cost-law | Gross/trade vs **$16.48** (4× RT $4.12) at realized stop distances, unchanged |
| Disclose (non-gating) | `convergence_rate` alongside the mean; naive fixed-offset control comparison (the cheap falsifier's own check, re-run on the full IS universe) *for continuity with the informal result*, explicitly labeled non-gating; per-cycle correlation check (does the trend-confound the cheap falsifier found on n=7 persist at full n — a genuine disclosure item, not assumed away) |

### Gate vocabulary (`explore_confirm_lib.explore_verdict`)

- **VOID** — diagnostic gate fails (after the full escalation ladder), or n_cycles_is < 20.
- **FALSIFIED** — `p_upper > 0.95` (real convergence sits below almost the entire surrogate null —
  no better, or worse, than generic autocorrelated price dynamics).
- **SHAPE-CLEAR** — `p_upper ≤ 0.05` **and** DELETE PASS **and** FLIP PASS.
- **AMBIGUOUS-HOLD** — otherwise (incl. significant primary with delete/flip fail, or a p_upper
  that clears neither the FALSIFIED nor SHAPE-CLEAR line).

CONFIRM unread. Cap not claimed. Pine (already authored once, see `RUNBOOK.md`) is not
re-authored until SHAPE-CLEAR + operator, per the same rule every other MSL card has followed.

---

## Forbidden moves

- Path-scoring CONFIRM before step-8 survivor protocol; any CONFIRM peek voids the holdout.
- Treating the cheap falsifier's informal `NOT DECISIVE` result, or its own addendum's trend-
  correlation finding, as a scored verdict — informative only, per its own LOG.
- Reusing the corrected-null-battery's calibrated tolerance NUMBERS without running this
  construct's own pilot calibration first (§Diagnostic gate).
- M escalation on a near-miss p — report, never re-roll.
- θ-retune (arm-window width, displacement threshold, stop/target) after seeing IS results — new
  K, new G0.
- Instrument hop (MCL) under this token — a second instrument is a new K spend per `PREREG_G0.md`
  §3, not a same-card widening.
- Self-authorizing an explore score without this token present as `EXPLORE_GO.md` (ISSUED-stamped).
- `dry_run=false` / arming / any live order — unaffected by anything in this document.

---

## Audit hooks

```text
test -f lab/analysis/c1/msl_s4_mgc_2026-08/EXPLORE_GO.md
PYTHONPATH=lab python3 -m pytest lab/analysis/c1/msl_s4_mgc_2026-08/test_explore_confirm_lib.py -q --import-mode=importlib
# expect: 23 passed (statistical core verified before any live pull)
rg -n "2024-01-01|2025-03-31|2025-04-01|2025-09-29|IAAFT|SHAPE-CLEAR" lab/analysis/c1/msl_s4_mgc_2026-08/EXPLORE_GO.DRAFT.md
PYTHONPATH=lab python3 -c "
from research_utils.camp_import import load_camp_sibling
lib = load_camp_sibling('explore_confirm_lib', 'lab/analysis/c1/msl_s4_mgc_2026-08/_audit.py')
assert lib.K_INTRINSIC == 1 and lib.DSR_FLOOR == 0.650 and lib.IAAFT_M == 1000
print('frozen constants OK')
"
```
