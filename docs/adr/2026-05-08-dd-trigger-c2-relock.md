# ADR: dd_protection C2 relock — 1.0% / 0.40× → 1.5% / 0.40×

**Date:** 2026-05-08
**Status:** Accepted (with documented dissent)
**Decision date:** 2026-05-08
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Scope:** `dd_protection.py`, `tests/test_mc_anchors.py`, `tests/test_mvd_selfchecks.py`, `CLAUDE.md`, `mc_explore.py`
**Supersedes:** `2026-04-17-dd-trigger-calibration.md` in part - DD_TRIGGER only; DD_SCALE = 0.40 unchanged.

## Context

Two converging events created the conditions for this re-lock:

1. **bust_attribution_flip resolution.** The 2026-04-26 portfolio_mc canonical-OANDA migration surfaced a mirror-symmetric Aegis ↔ Guardian attribution swap between the OANDA and Pepperstone panels (~+14pp Guardian / ~−14pp Aegis), confounded between two candidate drivers (broker-feed effect vs. version-relock effect). The brief at `bust_attribution_flip.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/bust_attribution_flip.md`) was held Forward pending three gating preconditions including a same-date TradingView Pepperstone+OANDA re-export. On 2026-05-08 those preconditions cleared, and the same-date re-export resolved the flip as **broker-feed-confirmed**: OANDA mis-represents the Aegis-vs-Guardian attribution split relative to Pepperstone. Pepperstone is canonical for attribution; OANDA continues as the secondary pattern-spotting surface.

2. **Q-DDP-1 sweep verdict re-evaluation.** The Q-DDP-1 Pareto-relaxation sweep (2026-05-06, `Q-DDP-1/recommendation.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-DDP-1/recommendation.md`)) tested 5 candidate dd_protection configs against 5 acceptance criteria. C2 (1.5% / 0.40×) was the sole config to pass criteria 1–4 strictly on the full 4-strategy Pepperstone panel:
   - Pass 98.09% (vs C0 97.88%)
   - Bust 0.36% (under 0.50% ceiling, vs C0 0.22%)
   - p99 DD 4.73% (under 5.00% ceiling, vs C0 4.55%)
   - Drag savings 25% (vs C0 baseline)
   - **Median days-to-pass 22 (vs C0 23)**

   C2 **failed criterion 5 (regime-robustness gate)** decisively: bootstrap 5th-percentile pass-rate 90.82% (vs 97.5% floor), H1 (2022-01 → 2024-04) sub-panel pass-rate 86.78% (vs 97.5% floor); H2 (2024-05 → 2026-04) sub-panel passes at 99.67%. The 12.9pp half-panel pass-rate spread was decisive and the recommendation was AMBIGUOUS / default HOLD.

The combined re-evaluation: with broker-feed differential isolated and OANDA's role re-affirmed as pattern-spotting (not lock-decision substrate), the H1↔H2 partition asymmetry that drove the regime-robustness failure is partially confounded by the same broker-feed differential the same-date re-export was designed to control. The dissent on regime fragility is preserved — H1's 86.78% characterization is not erased — but the operational benefit of C2 (median days-to-pass 23 → 22, 25% drag savings, both lock criteria still cleared with margin) is concrete and broker-feed-validated.

## Decision

Re-lock dd_protection at **C2 (DD_TRIGGER = 0.015, DD_SCALE = 0.40)**. Override of the Q-DDP-1 HOLD recommendation, on the explicit grounds that:

1. **Risk controls clear.** Bust 0.36% < 1.00% lock criterion; p99 DD 4.73% < 5.00% lock criterion. Both gates pass with margin on the full 4-strategy Pepperstone panel.
2. **Median pass-time benefit.** 23 → 22 days. Operational, concrete, measured.
3. **Broker-feed resolution.** The bust_attribution_flip closure validates that broker-feed differential affects attribution; C2's H1↔H2 spread is partially read through the same lens. Not a complete invalidation of the regime-robustness signal — a partial reframe.
4. **OANDA pattern-spotting reliability preserved.** OANDA C2 anchor (96.23% / 0.69% / 4.91%) clears the same lock criteria on the secondary panel.

### Locked MC numbers (canonical reference)

Config: G 0.34% / DJ30 v4.5 1.00% / A v4.3 1.50% / NAS v1 0.40%, dd_protection C2 1.5% / 0.40× single-tier, Pepperstone panel 2022-01-04 → 2026-04-20, 10,000 sims × 3 seeds.

- **Pass: 98.09%** (sigma 0.04%)
- **Bust: 0.36%** (0.00% daily + 0.36% static, sigma 0.03%)
- **Timeout: 1.55%**
- **Median days to pass: 22**
- **p50 DD: 1.37% / p95 DD: 3.74% / p99 DD: 4.73%**
- **Bust attribution:** striker 44.4% / aegis 24.1% / guardian 21.3% / NAS 10.2%

OANDA C2 anchor (3-strategy, DJ30 still v4.4): 96.23% pass / 0.69% bust / p99 DD 4.91% / median 25 days. Both lock criteria clear with thinner margin than Pepperstone, consistent with OANDA's pattern-spotting role.

Pinned by `tests/test_mc_anchors.py` and `tests/test_mvd_selfchecks.py`.

## Alternatives considered

- **C0 = (1.0%, 0.40×) — prior lock.** Pass 97.88% / bust 0.22% / p99 DD 4.55% / median 23. Pareto-undominated under the full Q-DDP-1 criteria set (1–5). Forgoes the median-pass-time benefit and 25% drag savings. **Rejected** in favor of C2 once broker-feed-resolution shifted the load on criterion 5.
- **C1 = (1.0%, 0.50×).** Bust 0.54% — exceeds the 0.50% ceiling. **Rejected** on Q-DDP-1 criterion 2.
- **C3 = (1.5%, 0.50×).** Bust 0.74% — exceeds the 0.50% ceiling. **Rejected** on Q-DDP-1 criterion 2.
- **C4 = (2.0%, 0.50×).** Bust 1.03%, p99 DD 5.06% — fails both the bust ceiling AND the static DD ceiling. **Rejected** on Q-DDP-1 criteria 2 + 3.

The full sweep audit lives at `Q-DDP-1/sweep_results.csv` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-DDP-1/sweep_results.csv`); per-config rejection itemization at `Q-DDP-1/recommendation.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-DDP-1/recommendation.md`).

## Consequences

Positive:
- Median days-to-pass shortens from 23 to 22 on Pepperstone.
- Drag savings of 25% on the unprotected-PnL substrate (per Q-DDP-1 sweep).
- Bust attribution rebalances under the new trigger: striker 40.9% → 44.4%, guardian 25.8% → 21.3%, aegis 22.7% → 24.1%, NAS 10.6% → 10.2%. NAS remains the lowest contributor consistent with the diversification thesis.
- Both lock criteria (bust < 1%, p99 DD < 5%) continue to clear on Pepperstone and OANDA.

Negative / watched:
- **Regime-robustness dissent.** H1 sub-panel pass-rate of 86.78% under C2 remains a real characterization of the strategy under early-panel (2022-01 → 2024-04) market conditions. The 12.9pp half-panel spread is on record. If forward live-PnL or future panel updates show H1-like underperformance, **C2's regime-fragility risk has materialized** — the documented fallback is to revert to C0.
- **Reduced p99 DD headroom under the 5% static cap.** 4.55% → 4.73% (45 bp → 27 bp of headroom). Still clear, but tighter than C0.
- **Striker concentration in bust attribution.** DJ30 share grew 40.9% → 44.4%. Q-DJ30-3 closed exhausted on the SNAG-tail anchor (2025-02-07 / −5.94R) on 2026-05-06; under C2 the DJ30 path now carries marginally more bust budget. Forward live-PnL on DJ30 warrants the most attention.

> ⚠ **READER INTERCEPT — added 2026-08-08. The trigger below is UNREACHABLE; the constants it guards are NOT.**
>
> - **The constants are in force and untouched:** `DD_TRIGGER` 0.015 / `DD_SCALE` 0.40 remain live law in
>   `core/dd_protection.py`. Nothing on this page is withdrawn by this banner.
> - **The scheduled check was retired by decision, not by decay:** the quarterly C2→C0 revert check was retired
>   2026-07-22 — its criterion was challenge-denominated ([`claims-rescope §Addendum 2026-07-22`](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-07-11-challenge-era-claims-rescope.md)).
>   A *scheduled review* was retired; the control was not.
> - **Its instrument cannot run either way:** the operationalization below names `analysis/time_to_pass.py`
>   (the script lives at `lab/analysis/`) run against a *"live-extended Pepperstone panel"* — the Pepperstone feed
>   was retired 2026-08-02 and `PANELS_BY_BROKER` has been empty since substrate Phase 3. A run today reports
>   **AMBIGUOUS-no-input**, never PASS.
> - **Do not confuse this with the allocation §Falsifier** in [`2026-05-23-allocation-refresh-2.md`](2026-05-23-allocation-refresh-2.md)
>   (revert target: DJ30 0.75% / pyr 500%, NAS100 0.45%): its limb 1 is this same retired check, limbs 2–3 are dormant
>   (re-arm: live-fill route + fresh Pre-Q), and its zero forward tripwire was accepted 2026-08-15 (that ADR's addenda).
>
> Any change to the DD constants still runs the standing chain: pre-registration → re-MC → **both-halves**
> regime-robustness gate → admitting ADR.

### Forward revert trigger (load-bearing)

Per the OVERRIDE section in `Q-DDP-1/recommendation.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-DDP-1/recommendation.md`):

> If rolling 6-month MC pass-rate on the live-extended Pepperstone panel falls below 95% for two consecutive 6-month windows after this override, treat as evidence the regime-fragility risk has materialized and re-open the C0/C2 question with the new panel data.

**Operationalization (2026-05-08):** quarterly cadence; the rolling 6-month MC pass-rate check is implemented in `analysis/time_to_pass.py` (`--regime-check` mode) and reported during the next four quarter-end reviews (2026-08-08, 2026-11-08, 2027-02-08, 2027-05-08 minimum).

## Cross-references

- Notion FINAL decision page (single-tier dd_protection): https://www.notion.so/346dc0b53c11816085bbf2292be934cc
- Q-DDP-1 brief: `Q-DDP-1/recommendation.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-DDP-1/recommendation.md`) (OVERRIDE section + original AMBIGUOUS / default HOLD verdict preserved below)
- bust_attribution_flip closure: `bust_attribution_flip.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/bust_attribution_flip.md`)
- Regime-robustness gate doc (worked example + override postscript): [docs/methodology/regime_robustness_gate.md](../methodology/regime_robustness_gate.md)
- Related ADRs:
  - 2026-04-17-dd-trigger-calibration (original C0 lock; superseded for `DD_TRIGGER` only)
  - 2026-04-17-equity-tier-deletion (single-tier basis)
  - 2026-04-23-guardian-risk-relock-0.34 (concurrent risk-control work)
  - 2026-04-24-mvd-discipline (constant-change MVD gate that fired correctly on this relock)
  - 2026-04-25-mvd-retrofit (MVD self-check at import; constants pinned at two layers)
- Code: `dd_protection.py` (`DD_TRIGGER = 0.015`, `DD_SCALE = 0.40`); `tests/test_mc_anchors.py` (Pepperstone 0.9809/0.0036/0.0473, OANDA 0.9623/0.0069/0.0491); `tests/test_mvd_selfchecks.py` (duplicated pin)
- MC harness: `portfolio_mc.py` (no source change; constants imported from `dd_protection`)
- Forward-trigger instrumentation: `analysis/time_to_pass.py` (`--regime-check` mode added 2026-05-08)

---

## Addendum — 2026-05-10

- `mc_explore.py` deleted in Q-MCFP-1 (PR #63, merge 54d22858 on main).
- C2 anchor 98.09 / 0.36 / 4.73 empirically reconfirmed post-precision-fix
  (Run A identical to baseline at abs=1e-4).
- Reference: [archive/docs/briefs/Q-MCFP-1/closure.md](https://github.com/Joshua-Asante/multi_firm_operations/blob/main/archive/docs/briefs/Q-MCFP-1/closure.md)

---

<a id="lineage-2026-04-17"></a>

## Lineage — 2026-04-17 origin (consolidated 2026-10-15)

Consolidated 2026-10-15 from 2026-04-17-equity-tier-deletion and 2026-04-17-dd-trigger-calibration (removed; see [TOMBSTONES](TOMBSTONES.md#2026-10-15-adr-decay-audit-removals)).
Accepted text, quoted verbatim; history only. `core/dd_protection.py` owns the live constants and
`AGENTS.md` §Protection the rule for any second tier (the equity tier's revert triggers are LOST;
the revisit note quoted below is not one). Incident record: [Rule 0](../rule_0.md#triggering-failures).

**2026-04-17-equity-tier-deletion** (Accepted 2026-04-17; its 1.0% trigger was re-locked to 1.5% by this ADR):

> **Context.** Prior `dd_protection.py` implemented two-tier protection: a drawdown-from-peak trigger (DD tier) and an equity-level trigger (equity tier). Under the intended composition, both tiers fired independently and their scaling factors combined via `min(DD_SCALE, EQUITY_SCALE)` to produce the active risk multiplier.
>
> Phase 1 audit surfaced the issue. Under `min()` semantics with the actual parameter values in use, the equity tier cannot fire without the DD tier having already fired first. The equity threshold (3.5% equity loss) is reached through drawdown from peak, which is exactly what the DD tier (1.5% DD) is already monitoring. The equity tier was behaviorally inert — mathematically dead code contributing nothing to the protection envelope.
>
> This was verified by sweeping equity-tier parameters across plausible ranges and confirming zero behavioral difference in Monte Carlo outcomes.
>
> **Decision.** Delete the equity tier entirely. Single-tier protection: DD trigger 1.0% from peak with 0.40× risk scaling.
>
> **Alternatives considered.**
> - **3a. Keep both tiers, change combination from `min()` to `*=` (multiplicative).** Under multiplicative combination, the equity tier would provide behavioral contribution. MC at 2.0%/0.40× with multiplicative showed bust 1.66% vs 1.55% for the single-tier option. One extra line of semantic complexity for a worse result. Rejected.
> - **3b. Delete equity, single-tier DD 1.0%/0.40×.** Chosen. Bust 1.55%, pass 93.00%, p99 DD ~4.9%.
> - **Do nothing.** Keep dead code. Rejected — violates Delete step of The Algorithm, adds ongoing maintenance burden and reader confusion.
>
> **Negative.** Requires a follow-up ADR if future portfolio changes (fourth strategy, Aegis allocation above 1.5%, correlated tail additions) make a genuine equity-level floor useful. Revisit then, do not preemptively restore.

**2026-04-17-dd-trigger-calibration** (Accepted 2026-04-17; superseded in part by this ADR — `DD_TRIGGER` re-locked to C2 (1.5%); `DD_SCALE` 0.40× unchanged):

> **Context.** Calibration objective: minimize portfolio bust rate across 150-day challenge horizon while preserving enough profit capture to clear the 5% FXIFY target at acceptable pass rate.
>
> **Decision.** DD trigger: 1.0% drawdown from peak.
> Scale factor: 0.40× (i.e., active risk multiplied by 0.40 when triggered).
>
> Under this configuration and the finalized allocations (G 0.30 / S 1.00 / A 1.50):
> - Bust rate: 1.55%
> - Pass rate: 93.00%
> - p99 drawdown: ~4.9%
> - Bust attribution: Aegis ~47% / Striker ~40% / Guardian ~12%
>
> **Alternatives considered.** MC sweep across trigger × scale grid. Key points tested:
> - **1.5% / 0.40× (initial retune).** Bust rate higher than 1.0%/0.40× because the trigger fired too late to meaningfully protect the 5% static DD bound. Rejected.
> - **2.0% / 0.40× with multiplicative two-tier (3a).** Bust 1.66% — worse than single-tier 1.0%/0.40× despite additional complexity. Rejected in favor of single-tier deletion.
> - **2.0% / 0.50× (post-challenge retune proposal).** Bust rate acceptable but only under relaxed challenge constraints (no 5% static DD cap). Proposal is queued for post-challenge, NOT active. See Notion: "dd_protection recalibration to 2.0%/0.50× — post-challenge — 2026-04-17".
> - **0.50× scale (looser protection).** Preserves more upside but crosses the 5% challenge threshold with higher probability. Rejected for the challenge phase.
> - **0.30× scale (tighter protection).** Reduces bust rate marginally but compresses profit distribution enough to drop pass rate below 90%. Rejected.
