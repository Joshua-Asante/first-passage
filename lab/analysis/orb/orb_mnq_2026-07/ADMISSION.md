# ORB-MNQ-1 — lifecycle admission note

**Date:** 2026-07-16 · **Decision:** operator ("admit it", full-pipeline evidence in hand)
**Governance:** [`docs/methodology/strategy_lifecycle.md`](../../../docs/methodology/strategy_lifecycle.md) · ADR [`docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md`](../../../docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md)
**Precedent:** Class-S candidate #1 G8-intake ([`../class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md`](../class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md)) — book-level CANDIDATE @1.00× with a standing caveat; **no `core/lifecycle.py` write.** This note follows that pattern.

## Verdict

**Admit ORB-MNQ-1 to lifecycle `CANDIDATE @ 1.00×`** — a genuinely new mechanism (opening-range
breakout on native MNQ), **not** one of the four locked legs (`core/lifecycle.py::STRATEGY_KEYS`)
and **not** a Class-S expression of a locked leg. Admission is recorded here as a research-lifecycle
disposition; it is **not** wired into `lifecycle_state.json` (that file is gitignored/local-only and
scoped to the four locked legs' demotion tracking — an absent entry already means 1.00×).

**Standing caveats (admitted WITH these, not upgraded past them):**

1. **Regime-conditional** (dominant risk). Edge is post-2020/trend-regime — dead 2019–2020 (N2),
   strong 2021–2025, 2026-partial −0.012 (the live early-fade tripwire). Not a structural,
   all-regime edge.
2. **Cost-marginal on the full window.** The Stage-6 full-window confirm holds only at Bulenox
   ($0.61/side) + ≤1-tick slip; the three costlier FRIENDLY firms fail the full window (2021+ has
   cushion at all four — RESULTS_stage7).
3. **Breadth** (Stage-8, **revised by realized N_eff** — [`RESULTS_stage8_neff.md`](RESULTS_stage8_neff.md)).
   The pre-data "instrument-concentration" read was **corrected**: realized weekly corr with the
   same-instrument MNQ-Striker leg is only **+0.15**, and dependence N_eff rises **1.99→2.95** (a
   near-independent bet — the belt finding confirmed). So ORB **adds correlation/direction breadth.**
   The concentration is narrower than first stated: **regime-common-mode** (both dead in 2020 / the
   chop the book busts in — average correlation doesn't capture the tail) **+ high-variance/risk-dominant**
   (weekly $ vol ~2× each book leg; sizing must stay conservative). Net: a real, near-independent edge,
   NOT a clean risk/regime diversifier.
4. **Confirmation of a pre-selected construct** (Default #1 realism axis), not a blind OOS
   discovery; DSR K_eff=2 deflates the MNQ-family K, not the original CFD search.

## Pipeline basis (all gates cleared; Stage-8 = concentration flag, not a kill)

| Stage | Verdict |
|---|---|
| 2 cost-law | PASS (5.31× full / 8.10× 2021+) — first pass in the pipeline |
| 5/6 DSR + temporal + placebo | RESOLVED (DSR full 0.9754 / annSR +0.890; temporal 2021+ PASS; placebo p=0.0040) |
| 7 firm × slip realism | survives all four FRIENDLY firms on 2021+; full-window Bulenox-and-≤1-tick-specific |
| 8 breadth (vs prop book) | concentrates instrument + regime; direction-agnostic the one breadth positive; realized N_eff data-gated |

## Still gated (admission authorizes NONE of these)

- ~~**Realized-N_eff completion** (Stage-8 owed)~~ — **DONE**, same-day as this note's own
  caveat 3 above (realized weekly corr +0.15, dependence N_eff 1.99→2.95;
  [`RESULTS_stage8_neff.md`](RESULTS_stage8_neff.md)), and re-confirmed 2026-07-17 by
  [`Q-COMPOSE-1`](../../../docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md). This
  bullet was never updated when caveat 3 landed — a same-commit internal inconsistency,
  corrected 2026-07-24, not a later staleness.
- ~~**Pine authoring**~~ — **DONE 2026-07-21** (operator GO: "create the pine for the nas
  orb strategy that survived"). `orb_mnq_v0_1.pine`, hash-pinned, compile-checked, and
  per-trade parity-reconciled against a real TV export (96.9% exact match) —
  [`orb_mnq_v0_1_CANDIDATE.md`](../../../core/strategies/orb/orb_mnq_v0_1_CANDIDATE.md).
  **Active working edition:** `orb_mnq_v0_2.pine` (D1–D4 calendar conformance + D5
  full-session clock pin, landed 2026-07-31) —
  [`orb_mnq_v0_2_CANDIDATE.md`](../../../core/strategies/orb/orb_mnq_v0_2_CANDIDATE.md).
  Post-D5 re-export + clock/k-grid re-score still owed before any k policy freeze.
- **Rail build, account registration, live spend** — separately gated (prop-portfolio program
  unchanged; no live automated execution anywhere).
- ~~**Decay monitor** (lifecycle Call-1)~~ — **calibrated (SEED) 2026-07-24**: Tradeify
  economics, 2021+ window, baseline_pf 1.1691 / pf_sigma 0.0836 / floor 1.0855, block_size=2
  (ACF, reproduces the Stage-6d spec) — [`RESULTS_decay_monitor.md`](RESULTS_decay_monitor.md).
  Tagged `SURVIVAL-ONLY` (surveillance tightness only; does not revisit this note's own
  `CANDIDATE @ 1.00×` starting-multiplier decision). A seed, not a fired monitor — no live
  venue exists yet. Call-1 action-on-breach at `CANDIDATE`:
  [`ADR 2026-08-06-candidate-call1-action-on-breach`](../../../docs/adr/2026-08-06-candidate-call1-action-on-breach.md)
  (**`Proposed`** — operator review flag only; no autonomous demotion; awaiting Accept).
  **Backtest-replay harness wired 2026-08-06** (calendar quarters vs frozen floor;
  `OPERATOR_REVIEW_FLAG` only — aligns with that Proposed rule; not demotion-wired /
  not live-fired) —
  [`RESULTS_decay_monitor_replay.md`](RESULTS_decay_monitor_replay.md).
- ~~**Cap tripwire companion (pre-P&L)**~~ — **registered 2026-08-06 (docs-only; not live-wired)**
  per [`ADR 2026-08-06`](../../../docs/adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md)
  (`Accepted` 2026-08-06): Cap-spend forward L1 `A` on `[t, t+60s)` beside this PF-CUSUM
  seed. Evidence: Cap [`RESULTS`](../../c1/mnq_capa_n14_tripwire_2026-08-06/RESULTS.md) /
  [`closure`](../../../docs/briefs/closures/Q-CAPA-1-closure-resolved.md). Fire thresholds
  deferred; no runner / lifecycle / entry-filter authority.

## Manifest / axis-separation

- Discovery manifest [`discovery_manifests/orb_mnq_intraday_breakout.json`](../../../discovery_manifests/orb_mnq_intraday_breakout.json)
  stays **open** (realized-N_eff completion owed). K_intrinsic=1 banked to the MNQ family.
- **No locked-parameter axis touch:** no `core/`, no allocation, no `dd_protection`, no `ACTIVE_FIRM`,
  no Pine. Lock **HELD** (99.83/0.17/4.37). This admission is an authorization-axis research
  disposition at the neutral 1.00× multiplier.
