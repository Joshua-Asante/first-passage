# ADR 2026-07-12 — DSR K-rule and variance-floor supersession (Campaign-default #3)

**Status:** Accepted (operator ratified 2026-07-12; supersedes Campaign-default #3's DSR K/V inputs only)
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0 body condensed, §6 downstream list, §7, part of §10 (the local `cd` line, the three DISC-CAMP-0 greps, the trigger reminder) and Verification removed; currency note added. Pre-trim text at blob `3b62deabcbc8d8abc2aa0d6983338555556c5dfc` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).
**Decision date:** 2026-07-12
**Authors:** Joshua (operator, ratified) + Claude (advisor; drafted from a 21-agent gate-reachability audit + direct code verification)
**Supersedes:** `2026-07-11-discovery-campaign-defaults-ratified.md` in part - Section 2 Campaign-default #3 ("Universe correction" row only - SPA/StepM/PBO mechanics and thresholds are untouched; only the DSR K and V inputs are re-baselined).
**Related:** `docs/notes/audits/2026-07-12-disccamp0-gate-reachability-audit.md` (the evidentiary base); `docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md` (the campaign this unblocks, amended in the same landing); `STATE.md` lines 143-153 (the pre-existing "pre-run obligation" this ADR discharges); `docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md` (the sibling gate-reachability precedent — same failure class, different mechanism)
**Layer:** methodology (research rules-of-evidence only). **No** strategy/risk-control parameter, allocation, `dd_protection` constant, `portfolio_mc.py`, or Pine source is touched. Locked MC anchor 99.83/0.17/4.37 untouched.

> **2026-10-15 currency note.** The `K_DSR` input semantics are amended in part by [`2026-08-04-family-k-bank-disclosure-not-gate.md`](2026-08-04-family-k-bank-disclosure-not-gate.md) (`K_eff = K_intrinsic`; family bank disclosure-only); the non-overlap floor and `V = 1/n` pin stand. `universe_gate.py`'s default has been `V = 1/n` since 2026-08-15 (Change history). The DISC-CAMP-0 pre-registration and shakedown paths cited below were removed from the tree; DISC-CAMP-0 closed FALSIFIED 2026-07-13 without reaching DSR.

---

## §0 — Rule 0 reads (production-source verification)

Read 2026-07-12 at `2a15c0e`: the defaults ADR (§2 default #3, §4 remedy path); the DISC-CAMP-0 pre-registration (raw K ≈ 156,500); `deflated_sharpe.py` `expected_max_sharpe`; `universe_gate.py` (empirical V, no override at the time); the [gate-reachability audit](../notes/audits/2026-07-12-disccamp0-gate-reachability-audit.md); and direct `.venv-research` runs showing the empirical-V bias (DSR 0.58 vs 0.65 at K_SPA=100) and the K_SPA=1 collapse. Full reads: [prior revision](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md).

---

## §1 — Context

Campaign-default #3 (universe correction, incl. `DSR ≥ 0.95`) was ratified 2026-07-11 as one of six standing rules of evidence for all discovery campaigns, explicitly **without** a reachability stress-test — the ratifying ADR's own §6 concedes it locked "reasoned defaults, not empirically-tuned ones," with §4 pre-committing the exact remedy path (a superseding ADR) if a closed campaign — or, as here, a **pre-freeze reachability audit** — showed mis-calibration.

The 2026-07-12 gate-reachability audit (the standing Q-HARV-0 pre-freeze obligation, `STATE.md:151-153`) found: DISC-CAMP-0's frozen K rule — `K = 22 + 3·N_subseq(GC 1h, 2010–2018) ≈ 156,500` — treats every **overlapping** matrix-profile subsequence position as an independent trial. LdP's `SR0` formula assumes independence, so this over-deflates: a genuinely-true GC 1h edge (plausible per-trade Sharpe ≤ 0.20, the top of a tradeable-edge range) needs Sharpe **0.28 at n=500 OOS trades / 0.63 at n=100** to clear DSR ≥ 0.95 — unreachable. The audit's red-team further verified that the natural patch (an effective-K reusing the Stage-5 block-size ACF) is **self-contradictory**: the effective count is *decreasing* in the ACF decorrelation length `L`, but the frozen block-size rule forces `L` **small** (the smallest lag where the return-ACF re-enters the white-noise band) — so reusing that same `L` drives the effective K back up into the tens of thousands, not down. There is no honest ACF-reuse fix.

Reading the now-landed `universe_gate.py` (which did not exist at audit time — it landed via PR #337/#339 mid-session) surfaced a **second, independent defect in the same gate**: the production `V` (across-trial Sharpe variance) is computed empirically from the Stage-4 returns-matrix columns, `Var(col_sr, ddof=1)`. At `K_SPA = 1` (a single triage survivor — the plausible outcome of Stage 4's own cost-law 4× hurdle, per the shakedown's own tool ladder), this collapses to `var_trials = 0.0` → `√V ≈ 0` → `SR0 ≈ 0` → **DSR passes almost trivially, regardless of `cumulative_k`.** This is the mirror-image failure to the first: not over-strict, but **vacuous exactly when Stage 4's aggressive triage does its job** — decoupling the K_DSR search-magnitude correction from the campaign's actual candidate economics.

**Direct empirical testing against the live module (this session, §0) showed the two defects compound rather than being independently fixable by the K-rule alone**: at a realistic `K_SPA=5`, fixing only `K_DSR` (to the non-overlap floor, below) left DSR still ≈0 for a true `SR=0.20`/`n=500` edge, because the empirical `V` estimator — contaminated by the very edge it scores — inflated `SR0` far more than the K-fix alone could compensate. Testing confirmed the bias does not resolve even at `K_SPA=100` (DSR 0.58 vs the unbiased-V value 0.65 for the same edge). **The V-estimator defect is therefore the dominant driver of unreachability at realistic candidate counts, not a secondary refinement of the K-fix** — both must be fixed together, and a conditional "trust empirical V once K_SPA≥30" rule (an earlier draft of this ADR) is **not supported by the data** and has been dropped in favor of an unconditional pin (§2.3). Both defects are properties of the **standing default**, not just DISC-CAMP-0 — every future matrix-profile campaign inherits them unless the default is fixed here.

**Decision driver (one sentence):** the ratified DSR default has two independent, code-verified calibration defects — an over-counted K denominator and a degenerate V estimator — that must be re-baselined before any campaign relying on matrix-profile discovery can freeze, per the remedy path the ratifying ADR itself pre-committed to.

---

## §2 — Decision

**Decision:** Campaign-default #3 ("Universe correction") is amended as follows. SPA, StepM, and PBO/CPCV mechanics and thresholds (`p<0.05`, `PBO<0.5`) are **unchanged**. Only the DSR **K** and **V** inputs are re-baselined:

1. **K_DSR — non-overlap floor, not raw subsequence count.** For any tool contributing an overlapping-window search term (matrix-profile / STUMPY-class), the K_DSR contribution is the **non-overlapping tiling count** Σ over windows of `⌊T / m⌋` (T = IS bar count, m = window length) — the largest count that does not require assuming independence between adjacent, (m−1)-bar-sharing start positions. Tools with a genuinely discrete, non-overlapping search space (catch22's 22 features; a single fixed-penalty `ruptures` run) are counted at **face value**, unchanged. For DISC-CAMP-0 (GC 1h, 2010-01-01:2018-12-31, m∈{30,60,90}): K_DSR = 22 (catch22) + 1 (ruptures) + Σ⌊T/m⌋ ≈ **3,200** — computed and bound at `register_search open` exactly as before, only the formula changes. The pre-registration must report the **bracket** `{non-overlap floor (BINDING), raw overlapping count}` together, so the discarded, larger number stays visible for review — never report only the value that happens to pass.
2. **K_SPA recorded distinct from K_DSR.** The Stage-4 returns-matrix column count (post-triage scored candidates) is a **different selection event** from the search-magnitude count DSR consumes. Campaign manifests and pre-registrations must name both separately (`K_SPA`, `K_DSR`) and never call both "the K-column matrix."
3. **V — unconditional pin to the theoretical null-sampling variance, `V = 1/n`.** `universe_gate.py`'s empirical `var_trials = Var(col_sr, ddof=1)` is **never** trusted for this default — direct testing (§0) showed it remains materially biased even at `K_SPA=100`, so no conditional "trust it once K_SPA≥N" threshold is adopted (an earlier draft's `K_SPA≥30` conditional is dropped as unsupported by the data). Every matrix-profile-family campaign pins `V = 1/n` (n = the selected candidate's OOS trade count), bound at the same Stage-4 step as K_SPA. **Landed this session** (not deferred): `lab/research_utils/universe_gate.py::run_universe_gate` gained an explicit `var_trials: float | None = None` keyword (`None` preserves the prior empirical default for backward compatibility with existing self-tests; campaigns with a frozen V-rule pass it explicitly) — plus a `--var-trials` CLI flag mirroring `deflated_sharpe.py`'s existing one, and `self_test()` forwards it for campaign-specific calibration. Three new tests (`test_var_trials_override_changes_dsr_from_default`, `test_var_trials_pin_guards_the_ksp1_degenerate_case`, `test_self_test_var_trials_forwarded`) verify the override is actually used and guards the K_SPA=1 degeneracy; full suite (12/12) + `check_boundaries` pass.
4. **Standing power-disclosure requirement (template-level, applies to all future campaigns).** Every campaign pre-registration must report, alongside its K/V rule, the **minimum detectable per-trade Sharpe** its bound `(K_DSR, V=1/n, plausible-n)` requires for DSR to clear the frozen threshold — operationalizing the Q-HARV-0 gate-reachability lesson as a structural pre-freeze step rather than a one-off audit. For DISC-CAMP-0, the validated power table (§6) shows: **at n≥500 the fix roughly doubles detection power** for a plausible-true edge relative to the unfixed default (e.g. `SR=0.20`: power 3%→21% at n=500, 63%→89% at n=1000), but **n≤250 stays near-zero power across the entire plausible-true range regardless of the fix** — rare/discord-class candidates with few OOS occurrences remain structurally excluded from DSR promotion by construction, not by a fixable calibration error. A campaign whose disclosed minimum exceeds a stated plausible-edge ceiling is malformed and must not freeze as written; DISC-CAMP-0 specifically must triage or explicitly flag low-n (≤250-trade) candidates as DSR-unreachable rather than let them silently fail at Stage 5.
5. **DSR ≥ 0.95 itself is retained, unchanged.** A graded/provisional-admission alternative (partial credit below 0.95) is explicitly **out of scope** here — forked to a separate, not-yet-authored Pre-Q (§3).

**Effective:** immediately upon operator ratification (accepted 2026-07-12; see Change history). **Scope:** all discovery campaigns using an overlapping-window/matrix-profile search term, retroactive to any campaign (DISC-CAMP-0 is the only one) still pre-freeze. Does not retroactively reopen closed campaigns (none exist for this family — cumulative K prior to DISC-CAMP-0 is 0).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep raw `3·N_subseq`, lower the DSR threshold to compensate | Arbitrarily softening the threshold to fit a known-flawed K is p-hacking-adjacent — it launders the over-count rather than fixing it, and does nothing about the independent V-degeneracy defect. |
| Adopt `Keff = 3·(N_subseq/L)` reusing the Stage-5 block-size ACF (the originally-proposed patch) | Red-team-verified self-contradictory: `Keff` decreases in `L`, but §4's frozen block-size rule forces `L` small — the two uses of the same ACF pull in opposite directions. Installs the exact "gate we'd-never-pass, evaded by a convenient K" error the audit exists to catch. |
| Drop DSR entirely for this family, rely on SPA/PBO/temporal battery only | DSR is the only mechanism-agnostic protection against best-of-K search inflation independent of the temporal battery; removing it defeats the multiplicity-control purpose of the Gen-2 stack (Campaign-default #2, two-level K). |
| Leave the default as-is; let DISC-CAMP-0 close FALSIFIED by construction (its own declared "shakedown success") | Wastes the campaign's banked K on a foregone conclusion and — more importantly — never exercises the promote branch (Stage-8 breadth, lifecycle admission, the Stage-6d decay-monitor ship), which is the primary operational risk the shakedown exists to retire per the audit's §4 (`shakedown_branch_coverage`). |
| Fix K only, ignore the V-degeneracy (treat it as a Phase-4 fast-follow) | **Directly tested and rejected mid-draft (§0/§1):** the K-fix alone does essentially nothing at realistic K_SPA — DSR stayed ≈0 for a true SR=0.20 edge at K_DSR=3200 with the default empirical V. The V-fix is not a refinement of the K-fix, it is the dominant lever; deferring it would ship an ADR that doesn't actually restore reachability. |
| Adopt a conditional "trust empirical V once K_SPA ≥ 30" threshold (an earlier draft of this ADR) | **Directly tested and rejected**: at K_SPA=100, empirical-V DSR (0.58) still had not converged to the unbiased V=1/n value (0.65) for the same edge — 30 is nowhere near a safe threshold, and no tested K_SPA reached convergence. An untested numeric threshold would have been exactly the kind of unverified pre-registration this whole audit exists to prevent. |

---

## §4 — Falsifier (revert / re-baseline trigger)

**H:** the non-overlap K_DSR floor + the unconditional `V=1/n` pin are the correct standing re-baseline for matrix-profile-family discovery campaigns.

**Falsifier:** this ADR is falsified if (a) a closed campaign under the new rule shows DSR still un-passable for an edge independently corroborated at high confidence by ≥2 other gates (SPA + temporal-consistency battery), indicating the non-overlap floor is still too conservative; or (b) a closed campaign's DSR-promoted candidate fails out-of-sample replication at a rate inconsistent with DSR≥0.95's intended false-positive control, indicating the floor is now too permissive. Either direction triggers a re-baseline via a further superseding ADR citing the closed-campaign evidence — never an in-place edit of this ADR or the template.

**Revert action:** supersede this ADR with a new one stating which value moves and why, citing the specific closed-campaign manifest.

**Trigger check schedule:** rides the standing quarterly programme audit — next **2026-08-08** (same cadence as the parent ratifying ADR), then 2026-11-08. Check: has DISC-CAMP-0 (or any successor matrix-profile campaign) closed, and does its closure record flag either K_DSR or the `V=1/n` rule as mis-gating?

---

## §5 — Forbidden moves (under this ADR)

- **Amending K_DSR or the `V=1/n` rule again after DISC-CAMP-0 sees a result.** The freeze contract's Known-Trap #12 still applies from the moment the amended pre-registration is committed — this ADR is a **pre-result** fix, not a license for further mid-campaign tuning.
- **Patching `universe_gate.py` beyond the minimal, additive `var_trials` override.** The landed patch (§2.3) is deliberately narrow: one new optional keyword, defaulting to the prior behavior, plus the matching CLI flag and `self_test()` forwarding — no change to SPA/StepM/PBO, no re-implementation of any vetted primitive, full existing test suite (9/9 prior tests) verified still green before adding 3 new ones (12/12 total). Any broader change to this module (e.g. changing the default itself, touching block-size logic) is out of scope here and requires its own review.
- **Lowering the DSR ≥ 0.95 threshold to compensate for either defect.** Ruled out in §3; the threshold itself is not what's miscalibrated.
- **Applying this K-rule to non-matrix-profile search terms** (e.g. a future campaign using only catch22 or only a fixed-penalty segmentation) — the non-overlap floor is specific to overlapping-window search; other tools keep face-value counting as the ratified default already specifies.
- **Retroactively reopening Q-HARV-0** (K=1, a wholly different tool/mechanism, already closed AMBIGUOUS) — this ADR is scoped to future/pre-freeze matrix-profile-family campaigns only.

---

## §6 — Consequences

**Positive consequences:**
- DSR becomes materially more reachable for a genuinely-true GC edge at realistic OOS trade counts (n≥500), unblocking DISC-CAMP-0's freeze. **Validated power table** (`run_dsr_gate` over 200 draws/cell, K_DSR=3200, V=1/n, vs the unfixed K=156,500/V=1/n baseline — both use the corrected V, isolating the K-fix's own contribution):

  | true SR | n=100 | n=250 | n=500 | n=1000 | n=2000 |
  |---|---|---|---|---|---|
  | 0.20 (NEW / OLD) | 0.00 / 0.00 | 0.01 / 0.00 | **0.21 / 0.03** | **0.89 / 0.63** | 1.00 / 0.99 |
  | 0.25 (NEW / OLD) | 0.00 / 0.00 | 0.14 / 0.01 | **0.67 / 0.23** | 1.00 / 0.97 | 1.00 / 1.00 |
  | 0.30 (NEW / OLD) | 0.01 / 0.01 | 0.29 / 0.09 | **0.92 / 0.65** | 1.00 / 1.00 | 1.00 / 1.00 |

  The K-fix alone (holding V fixed at the corrected 1/n) roughly **doubles** detection power at n=500–1000 across the plausible-true range. **Honest limit:** n≤250 stays near-zero power under either K rule — the fix does not and cannot rescue rare/low-n candidates; that is a structural property of DSR at this α, not a further calibration bug.
- The V-degeneracy fix protects every future matrix-profile campaign inheriting this default, not just DISC-CAMP-0 — catching a defect that would otherwise silently vitiate DSR whenever Stage-4 triage is aggressive (its intended behavior), and that a K-only fix would have left live.
- The standing power-disclosure requirement (§2.4) makes the next Q-HARV-0-class gate-reachability failure catchable by template discipline, not dependent on an ad-hoc audit being run.

**Negative consequences (real cost):**
- DISC-CAMP-0's campaign-local K_DSR drops from the frozen ~156,500 to ~3,200 — a genuinely **weaker** search-magnitude correction than originally committed. Some noise candidates that the (unreachable) 156k K would have blocked can now clear DSR. This is an explicit, accepted tradeoff: the alternative — a gate that is undetectably unreachable by construction — provides zero real protection while looking rigorous.
- The validated power table above is honest, not flattering: even fixed, DSR provides real protection against a plausible-true edge only at n≥500, and only reaches high power (≥0.9) at n≥1000. A campaign whose surviving candidates are all low-n (discord-class) will still close FALSIFIED at Stage 5 regardless of this fix — which is a correct outcome (per §2.4), not a remaining defect, but it means this ADR does not guarantee DISC-CAMP-0 reaches RESOLVED.

**Risks (probabilistic):**
- The non-overlap floor is itself a modeling choice, not a proven-correct effective-independence count for autocorrelated subsequences — true effective K could sit anywhere between the non-overlap floor and 1 (fully redundant). Mitigated by §2.1's bracket-reporting requirement (both floor and raw count travel together for review) and the §4 falsifier.
- `universe_gate.py`'s **default** behavior (no `var_trials` passed) still uses the biased empirical estimator, unchanged — the fix is opt-in via the new keyword/CLI flag, not a default-behavior change (deliberately, to avoid silently altering the module's existing self-test calibration). Any caller of `run_universe_gate`/the CLI that omits `--var-trials` inherits the known-biased default; this campaign's Stage-2/4 runner must always pass it explicitly.

---

## §10 — Audit hooks (runnable)

```bash
# No locked constant / allocation / dd_protection / MC anchor touched (expect empty)
git diff --stat HEAD -- core/config/params.toml core/dd_protection.py core/portfolio_mc.py

# Reproduce the validated power table (K_DSR=3200 vs 156500, V=1/n pinned, both cases)
PYTHONPATH=lab .venv-research/Scripts/python - <<'PY'
import numpy as np
from research_utils.universe_gate import run_dsr_gate
def power(true_sr, n, K, seed0, reps=200):
    rng = np.random.default_rng(seed0); passes = 0
    for _ in range(reps):
        rets = rng.normal(true_sr*0.01, 0.01, n)
        passes += run_dsr_gate(rets, cumulative_k=K, var_trials=1.0/n, dsr_min=0.95)["passed"]
    return passes/reps
for K in (3200, 156500):
    print(f"K_DSR={K}: SR=0.20,n=500 power={power(0.20,500,K,1):.2f}  SR=0.20,n=1000 power={power(0.20,1000,K,2):.2f}")
PY
# Expect: K=3200 power roughly double K=156500's at each cell (see ADR §6 table)

# var_trials override landed and is exercised by tests (Phase 1, DONE — not deferred)
grep -n "var_trials: float | None = None" lab/research_utils/universe_gate.py   # confirm the override parameter exists
PYTHONPATH=lab .venv-research/Scripts/python -m pytest tests/test_universe_gate.py -k var_trials -q
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-12 | Initial drafting (operator "Go" on the gate-reachability audit's fix path); status `Proposed`, pending explicit ratification | Claude (advisor) |
| 2026-07-12 | **Operator ratified** — status `Proposed` → `Accepted`. K/V fix becomes standing policy for matrix-profile-family campaigns | Joshua |
| 2026-08-15 | Module default flipped: `run_universe_gate(var_trials=None)` now uses `1/n` on the selected candidate's finite OOS trade count (gate-stack audit R5). The empirical `Var(col_sr)` default is retired. §6 risk line "omitting `--var-trials` inherits the known-biased default" is **discharged** by this addendum — not a silent §2 rewrite. Explicit pin still overrides. | Cursor (R5 execution; winning V already ratified 2026-07-12) |
| 2026-10-15 | §0 body, §6 downstream, §7, part of §10, Verification removed; currency note; prior body pinned | ADR decay audit |
