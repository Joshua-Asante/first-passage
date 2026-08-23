# Open-Question Roster (Q-roster)

Created 2026-06-13 as part of the Notion Phase-2 migration (`docs/adr/2026-06-12-notion-surface-retirement.md` §2.5).
The Notion Command Center previously held the live Q-roster; that surface is retired (read-only). This file is the
repo home for **open / dormant** investigation questions — one home per open Q. Closed questions live in
[`docs/briefs/closures/`](closures/) (hot). Pre-prune / restored bodies are mostly
**absent on this public clone** — retrieve via `git show pre-prune-2026-08-08:docs/ltm/briefs/…`
or the private archive / `git log --follow` ([`docs/ltm/README.md`](../ltm/README.md)).
They are not re-listed in Open.

**Convention:** each open Q has exactly one canonical repo home (the row's "Home"). When a Q closes, file the
closure under `docs/briefs/closures/` and delete its Open row (Recently-closed may keep a one-line pointer).

## Open

| Q | Status | Home (canonical) | Next action |
|---|---|---|---|
| **Q-TOM-SPX-1** — SPX500 turn-of-month existence and capturability | Layer A **RESOLVED-ABSENT** on canonical Pepperstone (2026-06-16); formal DEAD close reserved | [`docs/briefs/Q-TOM-SPX-1.md`](Q-TOM-SPX-1.md) | Run only the brief-reserved native Pine confirmation. Do not widen the window, change thresholds, or rerun Dukascopy to rescue the null. |
| **Q-SIGID-1** — measured live↔backtest signal-identity gap from mid-bar `alert()`/`strategy.entry` on c1 venue editions; architectures that close it (locked-axis, not EQ) | **`OPEN`** 2026-07-28 — cheap falsifier: 07-28 MNQ bar is a phantom (`longSignal` mid-true / close-false on `body_ok`); offline phantoms ~0.7× confirmed signals; Fri §2b clean re-measure owed | [`Q-SIGID-1-intra-bar-signal-identity.md`](Q-SIGID-1-intra-bar-signal-identity.md) · [pre-reg](pre-registration/Q-SIGID-1-verdict-preregistration.md) · [RESULTS](../../lab/analysis/c1/c1_signal_identity_2026-07-28/RESULTS.md) | Ruled host is **built** (S2b, `emit_enabled=false`). Offline limb MNQ 0.68 / MYM 0.70 stands. §2b re-measure needs no fill/order/arming. Pine edit only under separate operator GO. |
| **Q-FILLTAX-1** — TV fill-optimism gap + Pine↔Python / engine↔TV parity | **`OPEN`** — V2 Phase-0 scaffold `CODE_LANDED` 2026-08-07 ($0 under S1 incumbent); V1 disposition follows S1 (Tradeify geometry); Gate RESOLVED needs first family TV anchor | [`Q-FILLTAX-1-fill-realism-and-parity-scoping.md`](Q-FILLTAX-1-fill-realism-and-parity-scoping.md) · [`parity_gen2`](../../lab/analysis/c1/parity_gen2_2026-08/) · [`RESULTS`](../../lab/analysis/c1/parity_gen2_2026-08/RESULTS.md) | Operator: first family same-feed CME TV anchor → Gen-2 ADMIT. No post-hoc band tuning. Mutation battery (Phase 1) still owed. |

Ten of the eleven 2026-08-18 assumption-sweep Qs are now closed (Q-M1WIRE-1 `FALSIFIED` 2026-08-21; Q-TRADECAP-1 `RESOLVED`, Q-SIZECOMP-1 `RESOLVED`, Q-STATVALID-1 `FALSIFIED`, Q-INTAKEGOV-1 `AMBIGUOUS-HOLD`, Q-S5CAP-1 `RESOLVED`, Q-FIRMEOD-1 `FALSIFIED`, Q-DATAFIDELITY-1 `FALSIFIED`, Q-PUBTRANS-1 `FALSIFIED`, Q-CALLBOUND-1 `AMBIGUOUS-HOLD`, the latter nine all 2026-08-23) — see `## Recently closed` below for each. Origin: [`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`](../notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md) (25 verified-unexamined findings; these Qs combine 22 of them — 2 stay audit-note-resident: D5 Notice-phase 5-tool coverage, D10 D-S-A canon staleness routed to the next quarterly methodology audit instead (D1 MEMORY reach closed 2026-08-23, P2 Approach A)).

## Dormant (no current session home; resurface before assuming dead)

| Q | Status | Home | Note |
|---|---|---|---|
| ~~**Q-FUNDPOL-1** — funded-phase policy inheritance~~ → **DORMANT 2026-08-04** (§6 gate retired — eval pass converting cannot occur; Select-Flex thresholds non-transferable). §8 pre-reg (`d0200a4`, **K frozen = 4**) + P1/P2 discharges **unspent**; §1–§5 analysis retained as worked method. **Do not build** §9-C1 / `PAYOUT_MIN → 0`. | measurement / method record | [`Q-FUNDPOL-1-funded-phase-policy-inheritance.md`](Q-FUNDPOL-1-funded-phase-policy-inheritance.md) · pre-reg [`Q-FUNDPOL-1-verdict-preregistration.md`](pre-registration/Q-FUNDPOL-1-verdict-preregistration.md) | Successor venue needs a **new derivation**, not this brief rescheduled. |

## Recently closed (cross-reference; not open)

- **Q-MONSURF-1** — which monitoring surfaces are buildable venue-free now, and on what acceptance
  evidence (M-A/M-B/M-C triage) — **`RESOLVED` 2026-08-23** — M-B (idle-clock monitor) acceptance
  battery passes 0 missed / 0 spurious across all 312 real historical weeks, mutation-verified;
  registration-ready, gated on F3 only (not first live fill, as previously recorded). M-C stays
  fill-gated; M-A stays elective with its own build-gate scope ruling still owed. Triage written to
  STATE.md's board. $0/K=0. [`closure`](closures/Q-MONSURF-1-closure-resolved.md) ·
  [`brief`](Q-MONSURF-1-monitoring-surface-triage-scoping.md) ·
  [`pre-reg`](pre-registration/Q-MONSURF-1-verdict-preregistration.md) ·
  [`results`](../../lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08/RESULTS.md).
- **Q-TRADECAP-1** — is there any per-trade dollar-loss bound anywhere in the sizing/arming path on
  the intraday-enforced Tradeify geometry (A6, orphaned `1r_estimation.md` Forward question) —
  **`RESOLVED` 2026-08-23** — confirmed absent on all four checked limbs (sizing law, arming
  interlock, EM2, disaster-stop). Successor decision packet (per-trade hard-cap vs. live tripwire,
  from `1r_estimation.md`) named on STATE.md for operator election. $0/K=0.
  [`closure`](closures/Q-TRADECAP-1-closure-resolved.md) ·
  [`brief`](Q-TRADECAP-1-per-trade-loss-bound.md) ·
  [`pre-reg`](pre-registration/Q-TRADECAP-1-verdict-preregistration.md).
- **Q-STATVALID-1** — has the repo's own DSR/multiplicity rigor ever been pointed at the MC
  engine's resampling unit or the risk-control constants' own calibration search (B1+C1) —
  **`FALSIFIED` 2026-08-23** — Limb C fires on both grids (DD-trigger grid: 3/5 losing-candidate
  scores never retained; both grids: winner margin collapses to z≈0.8–1.2 vs the 2-sigma SE
  noise floor at N=30,000 paths). Limb B independently AMBIGUOUS — locked Pepperstone 4-strategy
  panel unrecoverable at $0 (retired 2026-08-03, no rollback copy). Successor named, not opened:
  a DSR/PBO correction-pass packet on both grids; separate re-test trigger for Limb B on next
  4-leg panel availability.
  [`closure`](closures/Q-STATVALID-1-closure-falsified.md) ·
  [`brief`](Q-STATVALID-1-mc-resampling-and-constant-multiplicity.md) ·
  [`pre-reg`](pre-registration/Q-STATVALID-1-verdict-preregistration.md).
- **Q-SIZECOMP-1** — does the live c1 sizing host's `r_eff` computation and the diagnostic
  CLI's own production call chain compose lifecycle × `DD_SCALE` × Call-4 beta-death the way
  `strategy_lifecycle.md` doctrine claims (A3+D4) — **`RESOLVED` 2026-08-23** — the rail never
  composes beta-death at all (0 `ops/` hits; imports `TIER_MULTIPLIER` only); the CLI's own
  triple-compound arithmetic checks out exactly against a hand computation; no 3-way test exists
  in `tests/test_lifecycle.py`. No code change under this brief — test-coverage gap and rail
  beta-wiring both named as an operator decision, not opened.
  [`closure`](closures/Q-SIZECOMP-1-closure-resolved.md) ·
  [`brief`](Q-SIZECOMP-1-sizing-composition.md) ·
  [`pre-reg`](pre-registration/Q-SIZECOMP-1-verdict-preregistration.md).
- **Q-S5CAP-1** — does S5's "capped concurrency" hold at the system level or only as a
  per-packet self-report (B3) — **`RESOLVED` 2026-08-23** — both `validate_promotion_packet()`
  and `refute_promotion_packet()` pass all 3 cloned synthetic packets sequentially (cumulative
  `concurrency_slots`=3 > `max_concurrency`=2, zero rejections); code inspection confirms neither
  function reads or writes state external to the single packet under evaluation. Mechanism gap,
  not a realized incident (zero real S5 promotions on record). Successor `Q-S5CAP-2` (wire a
  real counter, or decide not to) named, not opened, gated on M1 `RESOLVED`.
  [`closure`](closures/Q-S5CAP-1-closure-resolved.md) ·
  [`brief`](Q-S5CAP-1-capped-concurrency-invariant.md) ·
  [`pre-reg`](pre-registration/Q-S5CAP-1-verdict-preregistration.md).
- **Q-FIRMEOD-1** — does the Tradeify-proven EOD-vs-intraday breach-clock defect and
  lock/no-lock branch misclassification also apply to the 7 Bulenox/BluSky trailing tiers (B4)
  — **`FALSIFIED` 2026-08-23** — CLOCK fails: a CI-stable engine fixture parametrized to
  `Bulenox_100K`'s own `firm_kwargs()` shows `bust_trailing` flips 0→1 between
  `intraday_low=None` and populated. LOCK fails for Bulenox: its own Master Account primary
  source carries lock-adjacent language never captured in `firm_rules.py`'s sourcing comment —
  a new, separately-scoped finding. LOCK holds for BluSky (no lock language found on either
  stage's primary page). No live surface touched (neither firm has a c1 book). Every
  Bulenox/BluSky bust figure stays an EOD-clock lower bound until a successor re-runs the
  W1-pattern intraday fix.
  [`closure`](closures/Q-FIRMEOD-1-closure-falsified.md) ·
  [`brief`](Q-FIRMEOD-1-eod-breach-clock-bulenox-blusky.md) ·
  [`pre-reg`](pre-registration/Q-FIRMEOD-1-verdict-preregistration.md).
- **Q-DATAFIDELITY-1** — do the stated data-integrity safety nets (TV price fidelity,
  feed-equivalence pre-flight, manifest gate scope) cover what they're trusted to cover (C2+C3)
  — **`FALSIFIED` 2026-08-23** — both limbs fire: Limb C2 (MGC, 9 sampled trade dates) shows
  7/9 exact-match vs an independent Databento reference, 2/9 exceeding 1-tick tolerance on
  High/Low (one at a confirmed continuous-contract roll, one on a Databento-flagged
  degraded-quality date); Limb C3 confirms 0 documented manifest-gate scope caveat and 0
  CME-era feed-equivalence successor.
  [`closure`](closures/Q-DATAFIDELITY-1-closure-falsified.md) ·
  [`brief`](Q-DATAFIDELITY-1-tv-price-fidelity-and-integrity-gate-scope.md) ·
  [`pre-reg`](pre-registration/Q-DATAFIDELITY-1-verdict-preregistration.md).
- **Q-INTAKEGOV-1** — does discovery-intake/rejected-registry governance tooling
  (K_intrinsic self-report, dedup corpus, re-proposal cadence) cover what it's relied on to
  cover (B2+D2+C4) — **`AMBIGUOUS-HOLD` 2026-08-23`** (split verdict, not averaged) — B2 holds
  (no live `K_intrinsic` undercount found across 14 ledgered runs; 0 have any automated K
  cross-check); D2 confirms a real gap (mechanism-level dedup query misses `MNQ-ANALOGUE-1`
  entirely — returns noise, not the real hit — while `docs/adr/` sits outside the corpus); C4
  confirms no scheduled/symmetric re-examination mechanism exists for a standing REJECTED
  verdict. B2 re-tests at next discovery-run close; D2/C4 remediation named, not opened.
  [`closure`](closures/Q-INTAKEGOV-1-closure-ambiguous-hold.md) ·
  [`brief`](Q-INTAKEGOV-1-intake-registry-governance-coverage.md) ·
  [`pre-reg`](pre-registration/Q-INTAKEGOV-1-verdict-preregistration.md).
- **Q-CALLBOUND-1** — are the lifecycle Call-system's automation-authority boundaries
  symmetric and complete (Call-1 no promote-back path; Call-5 zero-contract reachable via a
  side door; D3+D6) — **`AMBIGUOUS-HOLD` 2026-08-23** — D3 (symmetry) CONFIRMED clean, no
  reverse path beyond the two already-named exceptions; D6 (completeness) inconclusive — one
  topically-adjacent, non-conclusive hit at `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md`
  (M1's own sign-off, not Call-5's). Dormant; re-test only if a leg floors to zero live or a
  session needs the D3 reverse path.
  [`closure`](closures/Q-CALLBOUND-1-closure-ambiguous-hold.md) ·
  [`brief`](Q-CALLBOUND-1-automation-boundary-symmetry.md) ·
  [`pre-reg`](pre-registration/Q-CALLBOUND-1-verdict-preregistration.md).
- **Q-PUBTRANS-1** — did the 2026-08-14 public-visibility transition complete cleanly (ADR
  Status stale, residual-disclosure risk untested, sentinel queue orphaned; B5+D8+D9) —
  **`FALSIFIED` 2026-08-23** — H-PUBTRANS rejected outright: Limb D8 concretely fails —
  Guardian Gold's ATR multiplier (1.55×), grace-stop multiplier (2.0×), and grace-bar window
  are stated in cleartext at `docs/methodology/1r_estimation.md:77,379`, a file absent from the
  admitting ADR's own downstream-artifact inventory and missed by the 2026-08-14 sweep — a live
  leak of Pine-only-locked strategy detail on the now-public repo, still present. ⚠ **Not
  remediated by this closure — flagged for immediate operator attention, see chat.** Limb B5
  (withheld literal account/$ grep) and Limb D9 (pre-transition sentinel-queue disposition —
  corrected count 12, not 11) remain individually open pending operator input; D9's own premise
  that it "needs private-archive access" is shown to be wrong (the archive is an already-fetched
  local git remote).
  [`closure`](closures/Q-PUBTRANS-1-closure-falsified.md) ·
  [`brief`](Q-PUBTRANS-1-public-transition-completeness.md) ·
  [`pre-reg`](pre-registration/Q-PUBTRANS-1-verdict-preregistration.md).
- **Q-M1WIRE-1** — does the M1 arming interlock verify everything its acceptance package claims — **`FALSIFIED` 2026-08-21** — A2 (no production confirmed-base write path) and A5 (fixture-hash drift not wired into arm/`gates.yml`) both confirmed; A4 untested and not required for the verdict. Rail stays disarmed; M1 stays not-`RESOLVED`. [`closure`](closures/Q-M1WIRE-1-closure-falsified.md).
- **Q-GATESTACK-1** — does anything on GitHub actually require the gate stack to pass before `main`, and is CI-status doc current — **`FALSIFIED` 2026-08-19** — `main` unprotected (404/`[]`/`push:true`); Actions live + green since 2026-08-15. Branch-protection packet named-not-opened; doc-correction packet executed same turn. [`closure`](closures/Q-GATESTACK-1-closure-falsified.md).
- **Q-NSURV-2** — can a magnitude-resampling second-uncertainty-layer be added to N-SURV
  reporting as a pure, headline-preserving addition — **`RESOLVED` 2026-08-20** — a wrapper
  reproduces both known candidates' (c1, ORB-MNQ-1) headline point estimates within 2.0pp,
  zero `run_partition_mc`/`blocks_from_daily_pnl` internals touched (grep-audited). Successor:
  light disclosure-only ADR drafted `Proposed`, ratification owed. $0/K=0.
  [`closure`](closures/Q-NSURV-2-closure-resolved.md) ·
  [`brief`](Q-NSURV-2-second-uncertainty-layer-design.md) ·
  [`pre-reg`](pre-registration/Q-NSURV-2-verdict-preregistration.md) ·
  [`ADR`](../adr/2026-08-20-nsurv-magnitude-resampling-disclosure.md).
- **Q-ORBSURV-1** — does cushion-proportional sizing clear the frozen survivor-scoring gate
  at the configurations the 08-20 informal probes never checked (full-panel k=2; post-break-only
  k=1/k=2) — **`FALSIFIED` 2026-08-20** — full-panel k=2 misses the pass floor (41.51% < 50%,
  bust still 0.00%); both post-break-only configurations clear comfortably (81.35%/64.11% pass).
  Cushion sizing's gate-clear is k-dependent, not a robust mechanism property; the k=1 full-panel
  clear measured earlier the same day held by only a 2.27pp margin. Does not license unpark. $0/K=0.
  [`closure`](closures/Q-ORBSURV-1-closure-falsified.md) ·
  [`brief`](Q-ORBSURV-1-cushion-sizing-gate-configurations.md) ·
  [`pre-reg`](pre-registration/Q-ORBSURV-1-verdict-preregistration.md) ·
  [`results`](../../lab/archive/orbmnq1_survivor_scoring_2026-08-20/full_k2_and_postbreak_results.json).
- **Q-NSURV-1** — is the N-SURV single-history magnitude blindspot (parent Notice
  `N-2026-08-15-nsurv-single-history-magnitude-blindspot`) general or idiosyncratic to c1 —
  **`RESOLVED` 2026-08-20** — confirmed general on a second candidate (ORB-MNQ-1): both books show a
  material single-history-vs-magnitude-resampled gap, but on *different* axes (bust for c1's flat
  sizing, pass for ORB-MNQ-1's cushion-proportional sizing) — a nuance the parent Notice didn't
  anticipate. No closed N-SURV verdict re-opened. Fix-design question explicitly deferred to a future
  session (`STATE.md` queue #3). Parent Notice graduated HOLD→RESOLVED same day. $0/K=0.
  [`closure`](closures/Q-NSURV-1-closure-resolved.md) ·
  [`brief`](Q-NSURV-1-single-history-magnitude-blindspot.md) ·
  [`parent Notice`](../notes/notice/N-2026-08-15-nsurv-single-history-magnitude-blindspot.md).
- **Q-ORBCUSH-1** — does a trailing edge/cost-fraction classifier explain ORB-MNQ-1's 2021-09-28
  cushion-proportional-sizing regime break — **`FALSIFIED` 2026-08-20** — trailing mean-R
  date-correlation clears 0 of 3 pre-registered windows (lower-edge bucket's ≤40% ceiling missed
  by 11–25pp at every window); direction stable but irrelevant once date-correlation fails. Second
  classifier refuted under the same discipline that already refuted trailing volatility — the
  2021-09-28 break stays real, triple-verified, and mechanistically unexplained
  (`ops/instruments/MNQ.md` N17). Bust-elimination itself is unaffected (regime-agnostic,
  independently verified). $0/K=0.
  [`closure`](closures/Q-ORBCUSH-1-closure-falsified.md) ·
  [`RESULTS`](../../lab/archive/q_orbcush_1_2026-08/RESULTS_meanr_regime_gate.md) ·
  [`brief`](Q-ORBCUSH-1-regime-break-mechanism.md) ·
  [`pre-reg`](pre-registration/Q-ORBCUSH-1-verdict-preregistration.md) ·
  [`probe`](../../lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/).
- **Q-XMEM-1** — cost of per-surface agent-memory invisibility; time-boxed Mem0 sidecar pilot —
  **`CLOSED` / GRAND-tier `SUBTRACT` 2026-08-19** (GSUB-2 c1, pursuit-level; not a re-verdict of
  the 2026-08-15 `ASSISTIVE-ONLY` Limb B measurement, which stands unchanged). Re-entry armor: a
  genuine dated cross-surface-memory-invisibility incident, per GRAND ADR §2.3.
  [`closure`](closures/Q-XMEM-1-closure-subtract.md) · [`pursuit c1`](../pursuits/c1-q-xmem-1.md) ·
  [`GSUB-2`](GSUB-2-park-cohort-early-review.md).
- **Q-TRAINKILL-3** — do Block F (FALSIFIED) and Block A (AMBIGUOUS) name the same
  2:1 winner between NEG and DEP — **`AMBIGUOUS-HOLD` 2026-08-18** (F=`NEG`
  9.83:1; A=`DEP` 4.06:1; split). Census STOP. No Q-TRAINKILL-4. No singleton
  power finding. $0/K=0.
  [`closure`](closures/Q-TRAINKILL-3-closure-ambiguous-hold.md) ·
  [`RESULTS`](../../lab/analysis/_inbox/q_trainkill_3_2026-08/RESULTS.md) ·
  [`brief`](Q-TRAINKILL-3-neg-vs-dep-discriminator.md) ·
  [`pre-reg`](pre-registration/Q-TRAINKILL-3-verdict-preregistration.md).
- **Q-TRAINKILL-2** — after recovery of committed mean-R CIs on the seven TK1-BOUNDED
  rows, does {0, +0.10} resolve, or does a pre-declared −0.10R or Fréchet-hi-zero
  DGP fit the scored core — **`AMBIGUOUS-HOLD` 2026-08-18** (MSL-S2A promoted;
  Limb 1 extremes still disagree; both `NEG` and `DEP-ZERO` fit). No singleton
  power finding. No gate number moves. $0/K=0.
  [`closure`](closures/Q-TRAINKILL-2-closure-ambiguous-hold.md) ·
  [`RESULTS`](../../lab/analysis/_inbox/q_trainkill_2_2026-08/RESULTS.md) ·
  [`brief`](Q-TRAINKILL-2-bounded-recovery-alt-dgp.md) ·
  [`pre-reg`](pre-registration/Q-TRAINKILL-2-verdict-preregistration.md).
- **Q-TRAINKILL-1** — is the explore/train kill record consistent with zero edge, with
  true +0.10R@$75 edges the designs are underpowered to pass, or with neither —
  **`AMBIGUOUS-HOLD` 2026-08-18** (BOUNDED extremes disagree: `MISCALIBRATED` at ε vs
  `KILLS-INFORMATIVE` at 1−ε; scored core n*=8 `MISCALIBRATED`, g(0)=0.024 < 0.05).
  No named power finding. No gate number moves. $0/K=0.
  [`closure`](closures/Q-TRAINKILL-1-closure-ambiguous-hold.md) ·
  [`RESULTS`](../../lab/analysis/_inbox/q_trainkill_1_2026-08/RESULTS.md) ·
  [`brief`](Q-TRAINKILL-1-train-gate-power.md) ·
  [`pre-reg`](pre-registration/Q-TRAINKILL-1-verdict-preregistration.md).
- **Q-EXPR-1** — what measurable property of the regularity→expression conversion accounts
  for the orphaning — **`RESOLVED` 2026-08-18** (H1 horizon-mismatch 4/4; H2 1/5 misses;
  H3 cannot fire — weekly+daily share 2026-06-19). Next slate admission screens claim
  horizon vs the E1 flat-by-16:00 envelope. $0/K=0.
  [`closure`](closures/Q-EXPR-1-closure-resolved.md) ·
  [`RESULTS`](../../lab/archive/q_expr_1_2026-08/RESULTS.md) ·
  [`brief`](Q-EXPR-1-regularity-expression-conversion.md) ·
  [`pre-reg`](pre-registration/Q-EXPR-1-verdict-preregistration.md).
- **Q-CONDVAL-1** — does the validated CL range-state lift buy anything in R terms —
  **`FALSIFIED` 2026-08-18** — committed C−U 0.130 < frozen `L_star` 0.423 at the N-EDGE
  cell (R=$75, RT=$4.12, slate-2 center); S1b conditioner-engineering branch parked; O2
  discharged; SIGNAL-GENERIC stands. $0/K=0.
  [`closure`](closures/Q-CONDVAL-1-closure-falsified.md) ·
  [`RESULTS`](../../lab/archive/q_condval_1_2026-08/RESULTS.md) ·
  [`brief`](Q-CONDVAL-1-range-state-r-terms.md) ·
  [`pre-reg`](pre-registration/Q-CONDVAL-1-verdict-preregistration.md).
- **Q-POLFRONT-1** — policy-augmented seed-target frontier — **`RESOLVED-QUANTIFIED` 2026-08-16**
  (median R_max ratio policy/flat = **5.107×** ≥ 1.25× bar, 24/30 cells defined, min 1.526×, 2
  newly-admitted cells, no reversal under quantization). ⚠ **Load-bearing caveat carried
  forward, not a footnote:** the policy's bust rate is far more EOD-clock-fragile than flat
  sizing (median stress delta +55.2pp vs +1.63pp) — feeds deep-lane GO-1 **with the caveat
  named in the first campaign's prereg**. **Fork executed 2026-08-17 (operator GO, corrected
  2026-08-20 — a stale copy of this row previously said the fork was still unopened):** the 5.1×
  headline does NOT survive intraday-honest remeasurement — policy-arm median bust delta +98.1pp,
  only 1/26 cells still clear 3.0%; `SAFE_WITH_CAVEATS` on independent adversarial re-verification.
  [`closure`](closures/Q-POLFRONT-1-closure-resolved-quantified.md) ·
  [`RESULTS`](../../lab/analysis/c1/q_polfront_1_2026-08/RESULTS.md) ·
  [`brief`](Q-POLFRONT-1-policy-augmented-seed-frontier.md)
- **Q-EVALSEQ-1** — within-eval front-load schedule (frozen K=4 family) — **`FALSIFIED` 2026-08-16**
  (best lift −1.06pt vs +5pt bar; flat WATCH-1 stands; K=3 consumed). **Surviving finding:**
  cushion-proportional sizing cut bust 20.18% → 0.00% (both halves) at 1.06pt of pass — routed to
  Q-POLFRONT-1 (bust-axis reframe). No θ-retune of the family; no registry row (policy-lever, not
  mechanism). [`closure`](closures/Q-EVALSEQ-1-closure-falsified.md) ·
  [`RESULTS`](../../lab/archive/q_evalseq_1_2026-08/RESULTS.md) ·
  [`pre-reg`](pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md)

- **Q-CAPBAND-1** — has `CAP = 1.0` ever excluded an axis that would otherwise have survived —
  **`RESOLVED` 2026-08-15** — both band axes fail a non-Cap gate: **D6** venue-dead (EURUSD
  `NOT TRADABLE`, CFD venue closed 2026-07-10) and **D2-low** bar-bound (ES/NQ/YM all return the
  machine-wired `index-intraday-ohlcv-directional-timing-2026-07-21`). Cap cost nothing **on the
  named axes**; 2026-08-03 audit §5.4 item 3 discharged. `CAP` byte-unedited. Gates 1–2 stayed
  `unevaluable` — the verdict rests on gates 3–4 only. $0/K=0.
  [`closure`](closures/Q-CAPBAND-1-closure-resolved.md) · [`brief`](Q-CAPBAND-1-cap-band-counterfactual.md) ·
  [`pre-reg`](pre-registration/Q-CAPBAND-1-verdict-preregistration.md).
- **Q-BUSTGATE-2** — does the 2026-08-13 external population data / updated Tradeify fee schedule
  move the Part-A eval bust ceiling — **`RESOLVED` 2026-08-15** — sole regime-admissible rung (0.50×)
  intraday-honest bust 0.72% ≤ 3.0%; ceiling reconfirmed byte-unedited; unconstrained-EV thread still
  points looser (narrowed 31.2:1→23.4:1, not reversed) but is non-decision-governing; no third
  re-derivation absent a structural-change ruling. $0/K=0.
  [`closure`](closures/Q-BUSTGATE-2-closure-resolved.md) ·
  [`brief`](Q-BUSTGATE-2-bust-gate-re-derivation-2026-08.md) ·
  [`pre-reg`](pre-registration/Q-BUSTGATE-2-verdict-preregistration.md).
- **Q-CAPFLOW-1** — OR-window net signed aggressor → ORB trade R (Cap-spend) —
  **`FALSIFIED` 2026-08-14** — coverage 255/255; ρ +0.020012; CI95 includes 0;
  Cap **held**; C11 stands. Reservation [`Q-CAPRES-2`](Q-CAPRES-2-mnq-cap-seat-reservation.md)
  unpaid-score obligation discharged. [`closure`](closures/Q-CAPFLOW-1-closure-falsified.md) ·
  [`RESULTS`](../../lab/archive/mnq_capflow_orb_r_2026-08/RESULTS.md).
- **Q-TNEC-CON-5** — impulse→pullback→VWAP-reclaim (pullback stop; first/session) —
  **`AMBIGUOUS-HOLD` → Branch A STOP 2026-08-12** — non-promotable; CONFIRM unread forever;
  dense-1m OHLCV temporal-selectivity lane default **paused** pending new modality /
  non-route-① thesis; lane FALSIFIED counter unchanged **1/3**. Cap unclaimed.
  [`closure`](closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) ·
  [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/RESULTS.md).
- **Q-TNEC-CON-4** — PDH/PDL RTH with-break — **`AMBIGUOUS-HOLD` 2026-08-11**; successor
  CON-5 Branch A STOP paused the lane, so this row left Open. INDEX repair 2026-08-15
  (liveness sweep). **U1 exception granted and spent same day, 2026-08-20** (operator
  override [`ADR`](../adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md)) —
  CONFIRM scored `AMBIGUOUS-HOLD` (short arm mean −0.0611R); cell **reverted to `U0`
  (paused)**, same as CON-1/2/3/5. Cap unclaimed.
  [`closure`](closures/Q-TNEC-CON-4-closure-ambiguous-hold.md) ·
  [`EXPLORE RESULTS`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md) ·
  [`CONFIRM RESULTS`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS_CONFIRM.md).
- **Q-TNEC-CON-3** — HTF-native 5m compression→expansion break — **`AMBIGUOUS-HOLD`
  2026-08-10**; successor CON-4/CON-5 lane paused (same repair). CONFIRM unread; Cap
  unclaimed. [`closure`](closures/Q-TNEC-CON-3-closure-ambiguous-hold.md) ·
  [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/RESULTS.md).
- **Q-TNEC-CON-2** — dense-1m compression→expansion with-break @ G=10 — **`AMBIGUOUS-HOLD`
  non-promotable 2026-08-10** — gross +0.90/+0.97 pt eaten by RT 1.41; halves flip; CONFIRM
  unread; Cap unclaimed. Successor = fresh G0 aimed at cost geometry (not θ-retune / not
  sign-invert). Master-Pattern-shaped HTF-5m→LTF-1m directed with-break died at parent cheap
  falsifier same day ($0 / **no Q-ID**) — [`falsifier LOG`](../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_htf_bias_break_2026-08-10_LOG.md).
  [`closure`](closures/Q-TNEC-CON-2-closure-ambiguous-hold.md) ·
  [`RESULTS_g2`](../../lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/RESULTS_g2.md).
- **GSUB-1** — first GRAND-Subtract pass over the pursuit portfolio — **`RESOLVED-LOADBEARING`
  2026-08-09** — 37-row inventory; **19 ratified dispositions** (8 PARK fielded to 2026-11-08 ·
  9 SUBTRACT · 2 MERGE); 37 records at [`docs/pursuits/`](../pursuits/); GRAND ADR §4 satisfied
  (tier load-bearing, sunset did not arm); $0 / K=0. [`closure`](closures/GSUB-1-closure-resolved-loadbearing.md) ·
  [`inventory`](GSUB-1-inventory-and-dispositions.md) · [`spec`](GSUB-1-first-grand-subtract-pass.md).
- **Q-TVCOV-1** — TV intraday bar-coverage census — verdicts landed **2026-07-13** (H FALSIFIED
  for 6J + MNQ; MYM AMBIGUOUS on a one-day TV hole); roster row closed **2026-08-09** under GSUB-1
  (bookkeeping only — no re-verdict). Residuals assigned: MYM AMBIGUOUS operator call → operator;
  roll-rule pin (`.v.0` not `.c.0`) — ⚠️ **already discharged** at
  `.claude/skills/databento-data/reference/schemas-and-symbology.md:37-44` since 2026-07-13; the
  "open item" text above it was stale (see [`c4 record`](../pursuits/c4-q-tvcov-1.md)).
  Closure: [`closures/Q-TVCOV-1-closure-falsified.md`](closures/Q-TVCOV-1-closure-falsified.md)
  (records stub 2026-08-11; disposition from RESULTS + c4). [`RESULTS`](../../lab/analysis/c1/tvcov_2026-07/RESULTS.md) ·
  [`brief`](Q-TVCOV-1-tv-bar-coverage-census.md) · [`pursuit record`](../pursuits/c4-q-tvcov-1.md)
- **Q-OFCHAN-1** — flicker-filtered TBBO L1 imbalance → 60 s mid (RTH grid) — **Stage-G VOID-COVERAGE 2026-08-07** — coverage 7.36% (3,558/48,360); empty candidates; STOP this G0 catalogue; CONFIRM unread — [closure](closures/Q-OFCHAN-1-closure-void-coverage.md) · [RESULTS_g2](../../lab/analysis/c1/mnq_ofchan_routeb_2026-08/RESULTS_g2.md).
- **Q-TXG-1** — transfer/expression lane — **CLOSED — FALSIFIED-at-walls 2026-08-12** (operator elected A on H_A re-argument) — re-proposal = different loss-side shape or different venue-class survival geometry — [packet](Q-TXG-1-ha-reargument.md) · [lane closure](closures/Q-TXG-1-closure-falsified-at-walls.md).
- **Q-TXG-1 cell striker_nas100×MYM** — sibling-swap transfer cell — **DEAD(cost) 2026-08-12** — mean_net_r 0.0129 < required_net_r 0.06; N-SURV not reached — [closure](closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md) · [PANEL_SCORE](../../lab/archive/transfer_expression_grid_2026-08/cells/striker_nas100_mym/PANEL_SCORE.json).
- **Q-TXG-1 cell striker×MNQ** — sibling-swap transfer cell — **DEAD(N-SURV) 2026-08-12** — cost PASS; N-SURV FAIL ~98% bust all partitions — [closure](closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md) · [PANEL_SCORE](../../lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/PANEL_SCORE.json).
- **Q-MNQSEL-1** — selection-value ceiling on causal restart clocks (s=40) — **CLOSED-FALSIFIED 2026-08-07** — S3 long 0.3998 / short 0.3984 both &lt; 0.40; S1 ≈ −0.036 both arms; STOP this universe — [closure](closures/Q-MNQSEL-1-closure-falsified.md) · [RESULTS](../../lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md).
- **Q-R2VBUCK-1** — volume-bucket aggressor imbalance → 60 s mid — **Stage-G FALSIFIED 2026-08-08** — n 77,656 / coverage 100%; ρ −0.005478 · CI includes 0; empty candidates; CONFIRM unread — [closure](closures/Q-R2VBUCK-1-closure-falsified.md) · [RESULTS_g2](../../lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md).
- **Q-MNQDTL-CON-1** — EM construct on dense RTH 1m opens (G=10) — **CLOSED FALSIFIED 2026-08-09** — ES/NQ 5m divergence explore STOP; both arms CI entirely &lt; 0 — [closure](closures/Q-MNQDTL-CON-1-closure-falsified.md) · [RESULTS](../../lab/archive/mnq_con1_dense1m_stage0_2026-08/RESULTS.md).


These had Notion tracker cards that are now retired. Hot closures live in `docs/briefs/closures/`. Older restored records are **not** on this public clone — retrieve via `git show` / private archive ([`docs/ltm/README.md`](../ltm/README.md)):

- **Q-R2FLOW-1** — clock-minute net signed aggressor → 60 s mid — **Stage-G FALSIFIED 2026-08-08** — n 48,360 / coverage 100% / CI includes 0; empty candidates; CONFIRM unread — [`closure`](closures/Q-R2FLOW-1-closure-falsified.md) · [`RESULTS_g2`](../../lab/archive/mnq_r2flow_routeb_2026-08/RESULTS_g2.md).
- **Q-MNQSEL-2** — dense RTH 1m selection ceiling at G=10 — **RESOLVED (C4) 2026-08-08** — S3 long 0.8584 / short 0.8566; S1 negative; construct ITERATE — [`closure`](closures/Q-MNQSEL-2-closure-resolved.md) · [`RESULTS`](../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/RESULTS.md).
- **Q-R2AGRUN-1** — aggressor-run trade-count → 60 s mid — **AMBIGUOUS-HOLD (magnitude) 2026-08-08; operator non-promotable STOP** — n 22.3M / coverage 100% / CI+placebo PASS / \|ρ\| < 0.02; CONFIRM unread; Cap not claimed — [`closure`](closures/Q-R2AGRUN-1-closure-ambiguous-hold.md) · [`RESULTS_g2`](../../lab/analysis/c1/mnq_r2agrun_routeb_2026-08/RESULTS_g2.md).
- **Q-CAPA-1** — Cap-seat Route A after N14: forward tripwire vs hold Cap — **RESOLVED 2026-08-06** — Cap seat **spent**; Δ **−0.022928**, CI excludes 0, placebo dead; tripwire **registered companion** (docs-only; not live-wired) — [`ADR 2026-08-06`](../adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md); §6 Cap-held expectation **wrong**. Closure: [`closures/Q-CAPA-1-closure-resolved.md`](closures/Q-CAPA-1-closure-resolved.md) · [`RESULTS`](../../lab/archive/mnq_capa_n14_tripwire_2026-08-06/RESULTS.md).
- **Q-RAIL-1** — c1 execution-path scoping (rail, account, fidelity preconditions F1–F5, GO/NO-GO packet) — priority-series rank 1/4 — **RESOLVED 2026-07-17** — F1–F5 all PASS; packet emitted; **§8 ceiling $700 signed** (clears both tiers + one reset); Tradeify Select recommended. ⚠ the brief body's §1 "discharged the four-firms ADR §4" claim was WITHDRAWN 2026-07-22 — see [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md); brief left frozen as historical record. Closure: [`closures/Q-RAIL-1-closure-resolved.md`](closures/Q-RAIL-1-closure-resolved.md) · [PHASE4 packet](../../lab/analysis/c1/q_rail_1_2026-07/PHASE4.md) · [RESULTS](../../lab/analysis/c1/q_rail_1_2026-07/RESULTS.md).
- **Q-PYRPARITY-1** — WATCH-1 pyramid-proportionality on TV — **FALSIFIED-NONPROPORTIONAL 2026-07-17** (MYM qty ceiling; fallback = account-multiplier layer). Closure: [`closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md`](closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md).
- **Q-INVENTORY-1** — fundable-inventory zero: bounded burst-2 vs accept-idle — **FALSIFIED 2026-07-17** — ratified + frozen + burst executed same day; 0 admissible seeds (≈90 citing works + 22 searches); accept-idle recorded; 3 UNSCREENABLE probe forks priced. Closure: [`closures/Q-INVENTORY-1-closure-falsified.md`](closures/Q-INVENTORY-1-closure-falsified.md) · [RESULTS](../../lab/archive/q_inventory_1_2026-07/RESULTS.md).
- **Q-BUSTGATE-1** — Part-A eval bust ceiling basis (08-08 packet A0/P0) — **FALSIFIED 2026-07-23** — EV-optimal admissible rung (1.00×) busts 4.37% > 3.0%; operator elected fork B (EV/dollar-day objective), ratified; A0b NO-GO on 1.00× (PASSES 0.50× → EV selects 0.50×). Live rung stays WATCH-1 0.50×. Closure: [`closures/Q-BUSTGATE-1-closure-falsified.md`](closures/Q-BUSTGATE-1-closure-falsified.md) · [fork-B ADR](../adr/2026-07-23-c1-rung-selection-ev-objective.md).
- **Q-KBUDGET-HARVEST-1** — bounded Tier-1/Tier-2 literature harvest — **RESOLVED 2026-07-16** (Phase-3 fired §6; 3 PASS = D5+H1+H2). Fundable discovery inventory 1→3, scoping only, does not block D5. Closure: [`closures/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md`](closures/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md) · [Phase-3 RESULTS](../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE3_RESULTS.md).
- **Q-GEOFIT-1** — trailing-DD funding-envelope map — **AMBIGUOUS-PARAMETERIZATION 2026-07-25** — A1 engine repro PASS both arms; A2 profile sufficiency MISS 23.63pp at exact fit (the `(σ_d, μ/σ, shape, z)` family omits skew). 288-cell grid left unrun; §5 hard-guard holds (not a Striker-reconstruction re-open route). Closure: [`closures/Q-GEOFIT-1-closure-ambiguous-parameterization.md`](closures/Q-GEOFIT-1-closure-ambiguous-parameterization.md) · [RESULTS](../../lab/archive/q_geofit_1_2026-07/RESULTS.md).
- **Q-JOINT-TAIL-1** — cross-strategy daily co-failure — closed **BLOCKED-RETIRED 2026-05-27** (portfolio temporally diversified at day-of-week level; 1 of 1141 bdays all-four-active). Succeeded by Q-JOINT-TAIL-WEEKLY (now also retired, below). Closure: retrieve `git show pre-prune-2026-08-08:docs/ltm/briefs/Q-JOINT-TAIL-1-closure.md` (absent here; restored 2026-08-11 from `pre-prune-2026-06-05:archive/docs/briefs/`).
- **Q-JOINT-TAIL-WEEKLY** — cross-strategy joint-tail at week-block resolution — **RETIRED 2026-07-14** at the pre-registered §9 authoring-time sanity gate (before any CC handoff). Panel-shape assumption failed: `n_active=4` weeks are 9.7% overall (needed >50%) and 4 of 23 in the bottom decile (needed ≥15) — the book is temporally diversified at weekly resolution too, so the joint-tail question is non-falsifiable for this allocation (as at the daily scale). Closure: [`closures/Q-JOINT-TAIL-WEEKLY-closure-retired.md`](closures/Q-JOINT-TAIL-WEEKLY-closure-retired.md); script `lab/archive/q_joint_tail_weekly_2026-07/sanity_check.py`.
- **Q-PRECOND-1** — mechanism preconditions — closed **FALSIFIED 2026-05-21** (precondition-as-retirement-rule too sensitive on the 2018-2022 long-DD window; HOLD-through-DD remains default). Notion data-quality sub-log `367dc0b53c11811a8944f4159ee32e11`. Closure: retrieve `git show pre-prune-2026-08-08:docs/ltm/briefs/Q-PRECOND-1-closure-falsified.md` (absent here; restored 2026-08-11 from `pre-prune-2026-06-05:archive/docs/briefs/Q-PRECOND-closure.md`).
- **Q-REGIME-RATEVOL-1** — exogenous rate-vol as participation-gate blind-spot complement — closed **FALSIFIED 2026-06-16** (rate-vol anti-aligned with the regime: hostile era was ZIRP low-bond-vol gold-chop; marginal AUC ≈0.50, conditional-on-gold 0.582 < 0.70 bar). Gold shadow gate stands alone; blind spot remains uncovered. Closure: retrieve `git show pre-prune-2026-08-08:docs/ltm/briefs/Q-REGIME-RATEVOL-1-closure-falsified.md` (absent here). Parent Q-REGIME-STRESS-1.
- **Q-REGIME-AEGIS-1** — does USDJPY trend-persistence separate Aegis's own win/loss regime — closed **FALSIFIED 2026-06-16** (per-trade AUC 0.499 = chance; the logged `aegis_flag` is a non-signal — period-level coincidence, not per-trade predictiveness). Recommend demoting `aegis_flag` from the shadow gate. **2nd consecutive FALSIFIED on the blind-spot-detector thread → INQHIORI §6 tail-exhaustion: no 3rd same-level detector.** Closure: retrieve `git show pre-prune-2026-08-08:docs/ltm/briefs/Q-REGIME-AEGIS-1-closure-falsified.md` (absent here). Parent Q-REGIME-STRESS-1.
- **Q-ICT-SWEEPFVG-1** — PHAROS sweep→FVG→draw on US500 15m — closed **FALSIFIED 2026-06-17** (point +0.316R cleared the 0.2883R hurdle and direction is real, permutation p=0.014, but `drop-top-3 −0.152R` + back-loaded thirds → ~3-trade-concentrated, not a robust edge). First US500 loop; pre-reg locked then run same session. Closure: retrieve `git show pre-prune-2026-08-08:docs/ltm/briefs/Q-ICT-SWEEPFVG-1-closure-falsified.md` (absent here); consolidated ledger [`ops/instruments/SPX500.md`](../../ops/instruments/SPX500.md) (directional-signal belt finding retained).
- Q-SWAP-1/2/3/4, Q-REGIME-1/2, Q-REGIME-TIME-1, Q-DDTRIG-1, Q-FEED-1, Q-PARITY-1 — retrieve under `docs/ltm/briefs/` via `git show pre-prune-2026-08-08:docs/ltm/briefs/…` (absent here; Q-FEED-1 restored 2026-08-11 as `Q-FEED-1-dukascopy-tv-feed-divergence.md`).
- **Q-ICT-CASCADE-1** — five-layer ICT cascade on US500 — **CLOSED 2026-06-19** (1M `INSUFFICIENT-N`; no deployable end-to-end edge). Closure stub: [`closures/Q-ICT-CASCADE-1-closure-insufficient-n.md`](closures/Q-ICT-CASCADE-1-closure-insufficient-n.md); layer bodies in [`lab/archive/ict_cascade_2026-06-18/`](../../lab/archive/ict_cascade_2026-06-18/).
- **Q-USOIL-1** — USOIL regime-capture / Silver §9 counterbalance — **CLOSED / SUBTRACT 2026-08-09** (GSUB-1 b4; expired PARK). Closure: [`closures/Q-USOIL-1-closure-subtract.md`](closures/Q-USOIL-1-closure-subtract.md) · [`b4`](../pursuits/b4-q-usoil-1.md).

> Forward triggers (methodology 90-day review 2026-07-29; 08-08 packet — C2→C0 revert check **retired** 2026-07-22 per rescope ADR D2 addendum) live in `STATE.md` §Scheduled forward triggers / pointer log, not here. Full living-board sync of retired lines is a deferred doc-drift session.
