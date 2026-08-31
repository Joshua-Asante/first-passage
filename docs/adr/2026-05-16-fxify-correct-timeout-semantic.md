# ADR: Replace portfolio_mc 150-bday horizon-runout with FXIFY-correct timeout semantic

**Status:** ACCEPTED
**Falsifier-status:** `FALSIFIER-UNREACHABLE` as of 2026-08-08 — all four §Falsifier limbs have lost their input (see the banner at §Falsifier). The decision itself stands and the timeout→inactivity semantic remains live in the engine; this marks the falsifier unreachable, not the ADR wrong.
**Decision date:** 2026-05-16
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Date:** 2026-05-16
**Authors:** Joshua (decision); Claude Code (execution)
**Supersedes:** No prior ADR pinned the timeout semantic — `HORIZON_DAYS = 150` was an implicit modeling choice present since the original `portfolio_mc.py` and never locked through an ADR. This ADR is the first formal decision on portfolio MC timeout semantics. It does **not** supersede `2026-05-08-dd-trigger-c2-relock` (dd_protection constants C2 unchanged) or `2026-05-14-allocation-refresh` (allocations unchanged).
**Closes:** `Q-MCTO-1-portfolio-mc-timeout-semantics.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-MCTO-1-portfolio-mc-timeout-semantics.md`) — CLOSED-RESOLVED on this ADR's adoption.

---

## §0 — Rule 0 reads (production-source verification)

Files verified before authoring this ADR. Verification anchors as of 2026-05-16 (HEAD `8028bcb` — Q-MCTO-1 PR #84 doc-cleanup merge, prior to this ADR's code change).

- [`portfolio_mc.py`](../../core/portfolio_mc.py) — anchor `8028bcb`. Verified at line 42–52: `HORIZON_DAYS = 150` with doc-cleanup comment block flagging it as a modeling artifact, not an FXIFY rule. Verified at line 200–238: `_simulate_path` returns `"timeout"` on horizon runout with no inactivity check. Verified at line 254: `outcomes = {"pass": 0, "bust_daily": 0, "bust_static": 0, "timeout": 0}` — the buckets that will change in this ADR's code edit.
- [`firm_rules.py`](../../core/firm_rules.py) — anchor `cd58bb9` (verified by Q-MCTO-1 §0 reads, unchanged on `origin/main`). Line 14: `inactivity_max_idle_days: 60`. This is the FXIFY ground-truth rule the new simulator semantic implements.
- [`dd_protection.py`](../../core/dd_protection.py) — anchor `6c7fa54`. C2 lock confirmed: `DD_TRIGGER = 0.015`, `DD_SCALE = 0.40`. **Unchanged by this ADR.**
- [`scripts/inactivity_simulator.py`](../../scripts/inactivity_simulator.py) — anchor `8028bcb` (added in PR #84). Phase 1 work-product simulator that implements the FXIFY-correct semantic: `INACTIVITY_LIMIT = 60`, `HORIZON_CAP = 1500`. Idle check is symmetric (`pnl == 0 AND no strategy had non-zero pnl`) to guard against offsetting-pnl false-idle. This is the reference implementation the production change ports into `portfolio_mc.py`.
- [`tests/test_inactivity_boundary.py`](../../tests/test_inactivity_boundary.py) — anchor `8028bcb`. 10 boundary tests pin the semantic against `scripts/inactivity_simulator.py`. Tests must be re-pointed to exercise the production path after the port.
- [`tests/test_mc_anchors.py`](../../tests/test_mc_anchors.py) — anchor `54d2285`. Current pins: Pepperstone `0.9878 / 0.0012 / 0.0417`; OANDA `0.9633 / 0.0040 / 0.0473`. **These pins move with this ADR.**
- `Q-MCTO-1-portfolio-mc-timeout-semantics.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-MCTO-1-portfolio-mc-timeout-semantics.md`) — anchor `8028bcb`. Status: OPEN. §6 gate criteria: CLOSED-RESOLVED route requires all six H-MCTO-1 clauses PASS + separate ADR before anchor-literal edits. Phase 1 evidence reproduced locally on 2026-05-16 against the merged worktree (deterministic, 0.00000pp spread across 3 reruns). Phase 2 evidence pinned at `Q-MCTO-1/regime_robustness.csv` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-MCTO-1/regime_robustness.csv`) (100 bootstrap rows + 2 half-panel rows).
- [`docs/adr/2026-05-08-dd-trigger-c2-relock.md`](2026-05-08-dd-trigger-c2-relock.md) — anchor `9268289`. Adoption template for ADR-with-documented-grounds. Forward revert trigger and quarterly cadence patterns reused here.
- [`docs/adr/2026-05-14-allocation-refresh.md`](2026-05-14-allocation-refresh.md) — anchor `a16a36b`. The immediately-prior canonical anchor (98.78 / 0.12 / 4.17 at C2 under 150-bday semantics). This ADR moves that anchor to historical.
- [`CLAUDE.md`](../../CLAUDE.md) — anchor on this worktree post-merge from `origin/main` head `8028bcb`. Strategy Reference §"2026-05-14 allocation-refresh MC anchor" reads the 98.78/0.12/4.17/1.10% timeout line that this ADR replaces.

**Cross-reference grep before authoring:**
```
$ grep -rn "HORIZON_DAYS\|timeout_rate\|1\.55%\|1\.10%" docs/ tests/ scripts/ portfolio_mc.py CLAUDE.md
```
Returns 27 hits across 9 files. The anchor-propagation surface (CLAUDE.md, tests/test_mc_anchors.py, archive/docs/briefs/Q-MCTO-1/*, docs/adr/2026-05-14-allocation-refresh.md §Locked MC, docs/analytics/mc_anchor_evolution/, references/baselines.md skill-side, portfolio_mc.py L42–52 comment, L254 outcomes dict, L391/414 aggregation, L435 horizon print). All require coordinated edits — itemized in §Implementation notes.

---

## Context

The Pepperstone 4-strategy canonical lock anchor (`98.78% pass / 0.12% bust / 4.17% p99 DD`, 2026-05-14 allocation refresh under C2) reports a `1.10%` "timeout" bucket. That bucket is a **150-bday horizon-runout cap** in `portfolio_mc.py`, not the **FXIFY 60-day inactivity rule** documented at `firm_rules.py:14`. Two different objects:

- `firm_rules.py:14` `inactivity_max_idle_days: 60` — actual FXIFY challenge-fail rule.
- `portfolio_mc.py:52` `HORIZON_DAYS = 150` — modeling artifact (simulation runs off end of array).

The mismatch was surfaced 2026-05-15 during a DJ30/NAS100 allocation MC. Q-MCTO-1 (Pre-Q brief authored 2026-05-15, PR #84) gated the question with strict §5 forbidden-moves: no silent re-anchor, no hybrid semantic, ADR required before any literal edits.

Q-MCTO-1 Phase 1 (headline shift) and Phase 2 (regime-robustness) both PASSED all six H-MCTO-1 clauses on the 2026-05-14 Pepperstone panel (1039 bdays / 207 week-blocks) under C2 dd_protection:

| Clause | Result |
|---|---|
| 1. Pass-rate shift ≥ +0.50pp | +1.100pp (98.78 → 99.88) ✓ |
| 2. p99 DD shift ≤ +0.20pp | +0.036pp (4.174 → 4.210) ✓ |
| 3. Inactivity bust rate ≤ 0.10% | 0.00% (no 60-day all-zero runs in 30K sims) ✓ |
| 4. Horizon_cap rate ≤ 0.10% | 0.00% (1500-day safety never fires) ✓ |
| 5. Lock gates (bust <1% AND p99 DD <5%) | 0.12% bust / 4.21% p99 DD ✓ |
| 6. Phase 2 regime-robustness | bootstrap p05 = 99.35% (margin +1.85pp); H1 = 99.64% / H2 = 99.95%; spread 0.31pp ✓ |

Phase 1 deterministic byte-identical reproducibility across 3 reruns: 0.00000pp spread on pass-rate, p99 DD, and median days-to-pass. Phase 2 closest-to-floor metric is H1 p99 DD = 4.84% (margin +0.16pp to 5% ceiling) — known residual, present under either timeout semantic.

The brief routes CLOSED-RESOLVED on adoption of this ADR.

---

## Decision

Replace `portfolio_mc.py`'s 150-bday horizon-runout timeout with the FXIFY-correct semantic:

- **Add** `INACTIVITY_LIMIT = 60` and `HORIZON_CAP = 1500` constants.
- **Remove** `HORIZON_DAYS = 150` (the 150-bday runout cap).
- **Add** inactivity tracking inside `_simulate_path`: a day is idle iff `pnl == 0 AND no individual strategy had a non-zero pnl` (symmetric check guards against offsetting non-zero pnls). On `consecutive_idle >= 60`, return `"bust_inactivity"` with `culprit = None` (no single-strategy attribution applies — the bust is "no one traded").
- **Replace** the `"timeout"` outcome with `"horizon_cap"` (semantic only — `horizon_cap` is a runtime-tractability safety, not an FXIFY rule). Bootstrap-of-week-blocks structure makes 60 consecutive all-zero bdays vanishingly rare and 1500-bday runout effectively impossible. Both bucket rates are expected to be ≤0.10% empirically; in Phase 1, both are 0.00%.
- **Re-pin** `tests/test_mc_anchors.py` Pepperstone anchor from `0.9878 / 0.0012 / 0.0417` to `0.9988 / 0.0012 / 0.0421`. OANDA anchor re-pin from `0.9633 / 0.0040 / 0.0473` to its FXIFY-correct value (determined by post-code-change re-run; see §Implementation notes).
- **Re-point** `tests/test_inactivity_boundary.py` to exercise `portfolio_mc._simulate_path` directly (importing from `scripts/inactivity_simulator.py` becomes redundant once the simulator is in production code).

dd_protection (C2: DD_TRIGGER=0.015, DD_SCALE=0.40), allocations (G 0.34% / DJ30 0.75% pyr 500% / A 1.50% / NAS 0.45%), and the Pepperstone 2022-05-23 → 2026-05-14 panel (1039 bdays / 207 week-blocks) are **all unchanged**.

### Locked MC numbers (canonical reference)

Config: G 0.34% / DJ30 v4.5 0.75% pyr 500% / A v4.3 1.50% / NAS v1 0.45%, dd_protection C2 1.5% / 0.40×, Pepperstone panel 2022-05-23 → 2026-05-14 (1039 bdays, 207 week-blocks), 10,000 sims × 3 seeds, FXIFY-correct timeout semantic.

- **Pass: 99.88%** (sigma 0.04%)
- **Bust: 0.12%** (0.00% daily + 0.12% static, sigma 0.01%)
- **Bust inactivity: 0.00%**
- **Horizon cap: 0.00%** (safety; bootstrap structure precludes 1500-day runouts)
- **Median days to pass: 21** (unchanged)
- **p50 DD: 1.27% / p95 DD: 3.28% / p99 DD: 4.21%**

OANDA C2 anchor under the FXIFY-correct semantic: re-computed by post-code-change verification re-run; expected directional shift mirrors Pepperstone (pass up ~1pp; static bust unchanged; p99 DD ≤ +0.20pp). The new OANDA anchor will be pinned at PR-commit time.

---

## Falsifier

This ADR is invalidated if **any** of the following observes:

> ⚠ **FALSIFIER-UNREACHABLE — added 2026-08-08. All four limbs below have lost their input; none can fire.**
> Limb 1 needs a **FXIFY rule change** — the venue was formally closed 2026-07-11/07-22. Limb 2 needs **live
> execution** — no strategy-signal-originated fill has ever occurred. Limb 3 names a *"live-extended Pepperstone
> panel"* and `analysis/time_to_pass.py` — the feed retired 2026-08-02 and the script lives at `lab/analysis/`.
> Limb 4 runs `portfolio_mc.py --panel pepperstone` — `PANELS_BY_BROKER` has been empty since substrate Phase 3.
> **What is NOT withdrawn:** the timeout→inactivity semantic this ADR installed remains live in the engine, and
> the §Decision stands. This banner marks the *falsifier* unreachable, not the decision wrong. Re-arm would
> require a successor venue with a published inactivity rule **and** a runnable panel; book it at the next
> programme audit rather than rolling the four dates forward silently.

1. **FXIFY rule change.** If FXIFY updates `inactivity_max_idle_days` from 60 (the firm-published rule this ADR models). Re-MC against the new rule.
2. **Live-PnL inactivity bust appears.** If forward live execution produces ≥3 consecutive idle bdays across the 4-strategy portfolio in any rolling 6-month window. The bootstrap-of-week-blocks structure should make this vanishingly rare; an empirical observation contradicts the modeling assumption. (Single-incident threshold: ≥30 consecutive idle bdays = immediate ADR invalidation; ≥3-instance threshold guards against ambiguous shorter clusters.)
3. **Quarterly regime-robustness drift.** At any of the four standing quarterly review dates (2026-08-08, 2026-11-08, 2027-02-08, 2027-05-08), if the rolling 6-month MC pass-rate on the live-extended Pepperstone panel falls below 95% for two consecutive 6-month windows under the FXIFY-correct semantic, treat as evidence the H1↔H2 regime-fragility risk has materialized and re-open. (Same quarterly cadence as 2026-05-08 C2 ADR — `python analysis/time_to_pass.py --regime-check`.)
4. **Anchor reproduction failure.** If `python portfolio_mc.py --panel pepperstone` produces output that deviates from `0.9988 / 0.0012 / 0.0421` by more than `abs=1e-4` after this ADR's code change lands. Indicates a code-edit error; this ADR's anchor literals do not hold.

Minimum action on falsification (any of 1–4 firing): revert `portfolio_mc.py` to the 150-bday horizon-runout semantic and restore the 2026-05-14 anchor pins (98.78 / 0.12 / 4.17). The 2026-05-14 allocation refresh ADR is the documented revert target.

---

## Consequences

### Positive

- **Canonical anchor matches FXIFY ground truth.** The "timeout" bucket no longer represents a model-only artifact; the timeout-class outcome (`bust_inactivity`) is now the FXIFY-published rule.
- **+1.10pp pass-rate headroom.** 98.78 → 99.88. The previously-reported ~1.1% "timeout" was paths that would have passed within ~7 more days (p99 unbounded days-to-pass = 156 in Phase 1 measurement).
- **Both lock gates pass with the widest margin on record.** Bust 0.12% (87% headroom below 1% ceiling); p99 DD 4.21% (79% headroom below 5% ceiling).
- **Bust rate unchanged.** 0.12% bust unchanged — the headline pass-rate shift comes entirely from timeout-bucket relabeling, not from any change in risk behavior. The lock gates are not loosened.
- **Regime-robustness gate cleared with margin.** Phase 2 bootstrap p05 = 99.35% (vs 97.5% floor, +1.85pp). H1↔H2 spread 0.31pp — well below the 5pp decisive-fail threshold and dramatically smaller than Q-DDP-1's 12.9pp H1↔H2 spread that drove the C2 dissent.
- **Doc layer matches code layer.** CLAUDE.md "timeout" prose now describes an FXIFY-modeled outcome rather than a modeling artifact.

### Negative

- **Anchor-literal propagation surface is non-trivial.** 9 files need coordinated edits (itemized in §Implementation notes). PR must land all edits together to avoid a partial-anchor-state.
- **H1 p99 DD = 4.84% remains the closest-to-floor metric.** Margin +0.16pp to the 5% lock ceiling. This is a known residual present under either timeout semantic (a panel feature, not a semantic artifact). Forward live-PnL on the H1-like regimes (2022 commodity volatility + early USDJPY weakness, partially rolled off by the 2026-05-14 strict 4yr window but not fully) warrants the same attention as under the prior semantic.
- **One-time downstream churn.** `references/baselines.md` (skill-side, last synced 2026-05-14), `docs/notion/repo_context.md`, and any Notion pages referencing the 98.78 anchor need updates. Tracked as standalone follow-ups (out of code-PR scope).
- **The `"timeout"` outcome name is retired in favor of `"horizon_cap"`.** Any external script consuming `result["timeout_rate"]` breaks. Internal grep confirms no such consumers exist in this repo; the field is renamed (not removed) to `horizon_cap_rate` to preserve the count-as-rate API shape.

### Neutral / informational

- **Bust rate identical (0.12%).** Confirms the semantic change is in the timeout bucket only; risk behavior unchanged.
- **Median days-to-pass identical (21).** The semantic change doesn't affect timing of paths that pass.
- **dd_protection constants unchanged.** This ADR is orthogonal to the C2 lock from 2026-05-08.
- **Bust attribution unchanged.** Same 4 strategies, same bust counts (35 across 30K sims), same proportional attribution.

---

## Forbidden moves

Each move below was genuinely considered or surfaced during Q-MCTO-1 authoring; not ceremonial.

- **Silent re-anchor of `CLAUDE.md` / `tests/test_mc_anchors.py` headlines without this ADR.** Q-MCTO-1 §5 explicitly forbade this. The 2026-04-17 dd_protection retune→reversal→delete-and-retune cycle is the load-bearing anchor for why silent semantic changes propagate as ceremony at the lock-decision layer. **Rejected.**
- **Hybrid semantic (60-day inactivity check ON TOP OF the 150-day horizon cap).** Tempting because it preserves backwards-compatibility with the 2026-05-14 anchor. But it would model neither the FXIFY rule cleanly nor any well-defined modeling object — ceremony at the simulator core. **Rejected** per Q-MCTO-1 §5.
- **Anchor-only edit without code change.** Tempting because Phase 1 evidence is clean (99.88/0.12/4.21 deterministic). But the anchor literal would not be reproducible from `python portfolio_mc.py` — a brittle state where `tests/test_mc_anchors.py` pins values the production simulator cannot produce. **Rejected**; the anchor must come from a deterministic re-run of new production code, not eyeballed from Phase 1 scripts.
- **One-shot PR bundling code change + brief closure + downstream Notion edits.** Q-MCTO-1 §5 named this trap. The discipline is: (1) ADR lands first (this artifact), (2) code change + anchor pins + CLAUDE.md edit land in one coordinated commit, (3) Q-MCTO-1 brief closure note + cross-link to this ADR, (4) downstream surfaces (references/baselines.md, Notion) follow as standalone work. **Adopted.**
- **Bypass Phase 2 evidence.** Tempting because Phase 1 shift is large and clean. But Q-DDP-1 (closed AMBIGUOUS-HOLD 2026-05-06, overridden 2026-05-08) is the load-bearing prior for why full-panel pass-rate improvement can be a regime-specific artifact. Phase 2 ran AND PASSED — bootstrap p05 = 99.35%, H1↔H2 spread 0.31pp. **Phase 2 evidence is load-bearing for this adoption.**
- **Wider scope drift.** Don't touch `dd_protection` constants, `ALLOCATIONS`, panel CSVs, MVD spec pins, or `firm_rules.py` while in the simulator-edit PR. The 2026-04-17 portfolio-allocations / equity-tier-deletion / dd-trigger-calibration cycle proved that bundling unrelated lock changes into one PR creates ambiguous attribution if the lock fails forward. **Strict scope: timeout outcome buckets only.**

---

## Implementation notes

Executed in the coordinated commit that shipped this ADR (constants, `_simulate_path` inactivity
tracking, and the `bust_inactivity`/`horizon_cap` outcome rename landed in `core/portfolio_mc.py`;
pins moved in `tests/test_mc_anchors.py` and `tests/test_inactivity_boundary.py`; `CLAUDE.md` and
`docs/analytics/mc_anchor_evolution/` updated same-commit). Full edit-by-edit runbook and pre-commit
verification commands: `git log --follow -- docs/adr/2026-05-16-fxify-correct-timeout-semantic.md`.

---

## Audit hooks

Runnable checks to verify this ADR still holds in future review.

```
# Verify the FXIFY-correct constants are in production code
$ grep -nE "INACTIVITY_LIMIT\s*=\s*60|HORIZON_CAP\s*=\s*1500" portfolio_mc.py
# Expected: 2 matches; HORIZON_DAYS = 150 NOT present

# Verify the canonical anchor pin
$ grep -E "0\.9988|0\.0012|0\.0421" tests/test_mc_anchors.py
# Expected: all three values present in test_pepperstone_anchor body

# Verify dd_protection constants unchanged (this ADR doesn't touch them)
$ grep -E "DD_TRIGGER\s*=\s*0\.015|DD_SCALE\s*=\s*0\.40" dd_protection.py
# Expected: both lines present

# Verify the FXIFY rule citation is current
$ grep -E "inactivity_max_idle_days:\s*60" firm_rules.py
# Expected: 1 match

# Verify Q-MCTO-1 is CLOSED-RESOLVED with back-link
$ grep -E "CLOSED-RESOLVED|2026-05-16-fxify-correct-timeout-semantic" archive/docs/briefs/Q-MCTO-1-portfolio-mc-timeout-semantics.md
# Expected: both phrases present

# Verify the falsifier hasn't fired (live-PnL inactivity check)
$ python analysis/time_to_pass.py --regime-check
# Expected (next four quarterly reviews 2026-08-08 → 2027-05-08): rolling 6mo pass-rate ≥ 95%
# Expected (live-PnL): zero ≥3-day consecutive idle windows in any rolling 6mo

# Verify no superseding ADR has shipped without back-link
$ grep -l "Supersedes:.*2026-05-16-fxify-correct-timeout-semantic" docs/adr/
# Expected: empty (or, if shipped, this ADR's status updated to SUPERSEDED-BY-NNN)
```

---

## Cross-references

- **Closes:** `Q-MCTO-1-portfolio-mc-timeout-semantics.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-MCTO-1-portfolio-mc-timeout-semantics.md`) (OPEN → CLOSED-RESOLVED)
- **Phase 2 evidence:** `Q-MCTO-1/regime_robustness.csv` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-MCTO-1/regime_robustness.csv`) (100 bootstrap + 2 half-panel rows, audit-ready)
- **Phase 1 runner:** `scripts/q_mcto_1_phase1.py` (deleted; Q-MCTO Phase scripts retired) — reproduced control + treatment anchors deterministically
- **Boundary tests:** [`tests/test_inactivity_boundary.py`](../../tests/test_inactivity_boundary.py) — 10 tests pin the semantic
- **Reference simulator:** [`scripts/inactivity_simulator.py`](../../scripts/inactivity_simulator.py) — Phase 1 work-product (production port lands in `portfolio_mc.py`)
- **Trajectory artifact:** [`docs/analytics/mc_anchor_evolution/README.md`](../analytics/mc_anchor_evolution/README.md) — A8 anchor added by this ADR
- **Standing doctrine:**
  - `docs/methodology/regime_robustness_gate.md` — Phase 2 gate worked-example here
  - `docs/rule_0.md` — §0 above is the production-source verification
  - `docs/operational_rules.md` — doc/code skew audit trigger
- **Related ADRs:**
  - [2026-05-14-allocation-refresh](2026-05-14-allocation-refresh.md) — immediately-prior canonical anchor, now historical
  - [2026-05-08-dd-trigger-c2-relock](2026-05-08-dd-trigger-c2-relock.md) — C2 lock, unchanged; this ADR is orthogonal
  - [2026-04-17-dd-trigger-calibration](2026-04-17-dd-trigger-calibration.md) — load-bearing anchor for "production reads before brief authoring" discipline
  - [2026-04-24-mvd-discipline](2026-04-24-mvd-discipline.md) — constant-change MVD gate
  - [2026-05-10-dd-protection-ulp-rounding](2026-05-10-dd-protection-ulp-rounding.md) — ULP-rounding precedent reused at L83/L89/L91 in inactivity_simulator.py and the production port

---

## Verification

One-time pre-adoption checks (brief-check PASS, pre/post-edit constant greps, Phase 1
reproducibility) ran clean before this ADR's code landed. Ongoing verification lives in
§Audit hooks above; the one-time commands themselves are recoverable via
`git log --follow -- docs/adr/2026-05-16-fxify-correct-timeout-semantic.md`.
