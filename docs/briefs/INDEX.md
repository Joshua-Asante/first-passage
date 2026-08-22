# Open-Question Roster (Q-roster)

Created 2026-06-13 as part of the Notion Phase-2 migration (`docs/adr/2026-06-12-notion-surface-retirement.md` §2.5).
The Notion Command Center previously held the live Q-roster; that surface is retired (read-only). This file is the
repo home for **open / dormant** investigation questions — one home per open Q. Closed questions live in
[`docs/briefs/closures/`](closures/) (hot) and, for pre-prune / restored history, `docs/ltm/briefs/` + `git log`.
They are not re-listed in Open.

**Convention:** each open Q has exactly one canonical repo home (the row's "Home"). When a Q closes, file the
closure under `docs/briefs/closures/` and delete its Open row (Recently-closed may keep a one-line pointer).

## Open

| Q | Status | Home (canonical) | Next action |
|---|---|---|---|
| **Q-TOM-SPX-1** — SPX500 turn-of-month existence and capturability | Layer A **RESOLVED-ABSENT** on canonical Pepperstone (2026-06-16); formal DEAD close reserved | [`docs/briefs/Q-TOM-SPX-1.md`](Q-TOM-SPX-1.md) | Run only the brief-reserved native Pine confirmation. Do not widen the window, change thresholds, or rerun Dukascopy to rescue the null. |
| **Q-SIGID-1** — measured live↔backtest signal-identity gap from mid-bar `alert()`/`strategy.entry` on c1 venue editions; architectures that close it (locked-axis, not EQ) | **`OPEN`** 2026-07-28 — cheap falsifier: 07-28 MNQ bar is a phantom (`longSignal` mid-true / close-false on `body_ok`); offline phantoms ~0.7× confirmed signals; Fri §2b clean re-measure owed | [`Q-SIGID-1-intra-bar-signal-identity.md`](Q-SIGID-1-intra-bar-signal-identity.md) · [pre-reg](pre-registration/Q-SIGID-1-verdict-preregistration.md) · [RESULTS](../../lab/analysis/c1/c1_signal_identity_2026-07-28/RESULTS.md) | Ruled host is **built** (S2b, `emit_enabled=false`). Offline limb MNQ 0.68 / MYM 0.70 stands. §2b re-measure needs no fill/order/arming. Pine edit only under separate operator GO. |
| **Q-FILLTAX-1** — TV fill-optimism gap + Pine↔Python / engine↔TV parity | **`OPEN`** — V2 Phase-0 scaffold `CODE_LANDED` 2026-08-07 ($0 under S1 incumbent); V1 disposition follows S1 (Tradeify geometry); Gate RESOLVED needs first family TV anchor | [`Q-FILLTAX-1-fill-realism-and-parity-scoping.md`](Q-FILLTAX-1-fill-realism-and-parity-scoping.md) · [`parity_gen2`](../../lab/analysis/c1/parity_gen2_2026-08/) · [`RESULTS`](../../lab/analysis/c1/parity_gen2_2026-08/RESULTS.md) | Operator: first family same-feed CME TV anchor → Gen-2 ADMIT. No post-hoc band tuning. Mutation battery (Phase 1) still owed. |
| **Q-SIZECOMP-1** — does live c1 sizing actually compose lifecycle × DD × beta-death the way doctrine says (A3+D4) | **`OPEN — DRAFT (pre-lock)`** 2026-08-18 | [`Q-SIZECOMP-1-sizing-composition.md`](Q-SIZECOMP-1-sizing-composition.md) | Named, not opened. Operator GO → Phase 1 (grep + local pytest snippet, $0/K=0). |
| **Q-TRADECAP-1** — is there any per-trade dollar-loss bound anywhere in the sizing/arming path on the intraday-enforced Tradeify geometry (A6, orphaned `1r_estimation.md` Forward question) | **`OPEN — DRAFT (pre-lock)`** 2026-08-18 | [`Q-TRADECAP-1-per-trade-loss-bound.md`](Q-TRADECAP-1-per-trade-loss-bound.md) | Named, not opened. Operator GO → Phase 1 (grep + read, $0/K=0). |
| **Q-STATVALID-1** — has the repo's own DSR/multiplicity rigor ever been pointed at the MC engine's resampling unit or the risk-control constants' own calibration search (B1+C1) | **`OPEN — DRAFT (pre-lock)`** 2026-08-18 | [`Q-STATVALID-1-mc-resampling-and-constant-multiplicity.md`](Q-STATVALID-1-mc-resampling-and-constant-multiplicity.md) | Named, not opened. Operator GO → Phase 1 (Ljung-Box on existing panel + arithmetic on logged grid scores, $0/K=0). |
| **Q-INTAKEGOV-1** — does discovery-intake/rejected-registry governance tooling (K_intrinsic self-report, dedup corpus, re-proposal cadence) cover what it's relied on to cover (B2+D2+C4) | **`OPEN — DRAFT (pre-lock)`** 2026-08-18 | [`Q-INTAKEGOV-1-intake-registry-governance-coverage.md`](Q-INTAKEGOV-1-intake-registry-governance-coverage.md) | Named, not opened. Operator GO → Phase 1 (ledger read + grep, $0/K=0). |
| **Q-S5CAP-1** — does S5's "capped concurrency" hold at the system level or only as a per-packet self-report (B3) | **`OPEN — DRAFT (pre-lock)`** 2026-08-18 | [`Q-S5CAP-1-capped-concurrency-invariant.md`](Q-S5CAP-1-capped-concurrency-invariant.md) | Named, not opened. Operator GO → Phase 1 (3 synthetic packets through the local validators, $0/K=0). |
| **Q-FIRMEOD-1** — does the Tradeify-proven EOD-vs-intraday breach-clock defect apply to Bulenox/BluSky, never checked (B4) | **`OPEN — DRAFT (pre-lock)`** 2026-08-18 | [`Q-FIRMEOD-1-eod-breach-clock-bulenox-blusky.md`](Q-FIRMEOD-1-eod-breach-clock-bulenox-blusky.md) | Named, not opened. Operator GO → Phase 1 (primary-source re-read + seed/path re-diff, $0/K=0). |
| **Q-DATAFIDELITY-1** — do the stated data-integrity safety nets (TV price fidelity, feed-equivalence pre-flight, manifest gate scope) cover what they're trusted to cover (C2+C3) | **`OPEN — DRAFT (pre-lock)`** 2026-08-18 | [`Q-DATAFIDELITY-1-tv-price-fidelity-and-integrity-gate-scope.md`](Q-DATAFIDELITY-1-tv-price-fidelity-and-integrity-gate-scope.md) | Named, not opened. Operator GO → Phase 1 (~10-row OHLC diff vs CME settlement + doc grep, $0/K=0). |
| **Q-PUBTRANS-1** — did the 2026-08-14 public-visibility transition complete cleanly (ADR Status stale, residual-disclosure risk untested, sentinel queue orphaned; B5+D8+D9) | **`OPEN — DRAFT (pre-lock)`** 2026-08-18 | [`Q-PUBTRANS-1-public-transition-completeness.md`](Q-PUBTRANS-1-public-transition-completeness.md) | Named, not opened. **Operator-only limb (B5) needs withheld literal account/$ values** — rest is agent-doable at $0/K=0. |
| **Q-CALLBOUND-1** — are the lifecycle Call-system's automation-authority boundaries symmetric and complete (Call-1 no promote-back path; Call-5 zero-contract reachable via a side door; D3+D6) | **`OPEN — DRAFT (pre-lock)`** 2026-08-18 | [`Q-CALLBOUND-1-automation-boundary-symmetry.md`](Q-CALLBOUND-1-automation-boundary-symmetry.md) | Named, not opened. Operator GO → Phase 1 (grep/diff sweep, $0/K=0). |

Ten of the eleven 2026-08-18 assumption-sweep Qs remain Open (Q-M1WIRE-1 closed `FALSIFIED` 2026-08-21). Origin: [`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`](../notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md) (25 verified-unexamined findings; these Qs combine 22 of them — 3 stay audit-note-resident: D1 MEMORY.md governance reach, D5 Notice-phase 5-tool coverage, D10 D-S-A canon staleness routed to the next quarterly methodology audit instead).

## Dormant (no current session home; resurface before assuming dead)

| Q | Status | Home | Note |
|---|---|---|---|
| ~~**Q-FUNDPOL-1** — funded-phase policy inheritance~~ → **DORMANT 2026-08-04** (§6 gate retired — eval pass converting cannot occur; Select-Flex thresholds non-transferable). §8 pre-reg (`d0200a4`, **K frozen = 4**) + P1/P2 discharges **unspent**; §1–§5 analysis retained as worked method. **Do not build** §9-C1 / `PAYOUT_MIN → 0`. | measurement / method record | [`Q-FUNDPOL-1-funded-phase-policy-inheritance.md`](Q-FUNDPOL-1-funded-phase-policy-inheritance.md) · pre-reg [`Q-FUNDPOL-1-verdict-preregistration.md`](pre-registration/Q-FUNDPOL-1-verdict-preregistration.md) | Successor venue needs a **new derivation**, not this brief rescheduled. |

## Recently closed (cross-reference; not open)

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


These had Notion tracker cards that are now retired. Hot closures live in `docs/briefs/closures/`; older restored records may still sit in `docs/ltm/briefs/` / `git log`:

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
- **Q-JOINT-TAIL-1** — cross-strategy daily co-failure — closed **BLOCKED-RETIRED 2026-05-27** (portfolio temporally diversified at day-of-week level; 1 of 1141 bdays all-four-active). Succeeded by Q-JOINT-TAIL-WEEKLY (now also retired, below). Closure: [`../ltm/briefs/Q-JOINT-TAIL-1-closure.md`](../ltm/briefs/Q-JOINT-TAIL-1-closure.md) (restored 2026-08-11 from `pre-prune-2026-06-05:archive/docs/briefs/`).
- **Q-JOINT-TAIL-WEEKLY** — cross-strategy joint-tail at week-block resolution — **RETIRED 2026-07-14** at the pre-registered §9 authoring-time sanity gate (before any CC handoff). Panel-shape assumption failed: `n_active=4` weeks are 9.7% overall (needed >50%) and 4 of 23 in the bottom decile (needed ≥15) — the book is temporally diversified at weekly resolution too, so the joint-tail question is non-falsifiable for this allocation (as at the daily scale). Closure: [`closures/Q-JOINT-TAIL-WEEKLY-closure-retired.md`](closures/Q-JOINT-TAIL-WEEKLY-closure-retired.md); script `lab/archive/q_joint_tail_weekly_2026-07/sanity_check.py`.
- **Q-PRECOND-1** — mechanism preconditions — closed **FALSIFIED 2026-05-21** (precondition-as-retirement-rule too sensitive on the 2018-2022 long-DD window; HOLD-through-DD remains default). Notion data-quality sub-log `367dc0b53c11811a8944f4159ee32e11`. Closure: [`../ltm/briefs/Q-PRECOND-1-closure-falsified.md`](../ltm/briefs/Q-PRECOND-1-closure-falsified.md) (restored 2026-08-11 from `pre-prune-2026-06-05:archive/docs/briefs/Q-PRECOND-closure.md`).
- **Q-REGIME-RATEVOL-1** — exogenous rate-vol as participation-gate blind-spot complement — closed **FALSIFIED 2026-06-16** (rate-vol anti-aligned with the regime: hostile era was ZIRP low-bond-vol gold-chop; marginal AUC ≈0.50, conditional-on-gold 0.582 < 0.70 bar). Gold shadow gate stands alone; blind spot remains uncovered. Closure: [`../ltm/briefs/Q-REGIME-RATEVOL-1-closure-falsified.md`](../ltm/briefs/Q-REGIME-RATEVOL-1-closure-falsified.md). Parent Q-REGIME-STRESS-1.
- **Q-REGIME-AEGIS-1** — does USDJPY trend-persistence separate Aegis's own win/loss regime — closed **FALSIFIED 2026-06-16** (per-trade AUC 0.499 = chance; the logged `aegis_flag` is a non-signal — period-level coincidence, not per-trade predictiveness). Recommend demoting `aegis_flag` from the shadow gate. **2nd consecutive FALSIFIED on the blind-spot-detector thread → INQHIORI §6 tail-exhaustion: no 3rd same-level detector.** Closure: [`../ltm/briefs/Q-REGIME-AEGIS-1-closure-falsified.md`](../ltm/briefs/Q-REGIME-AEGIS-1-closure-falsified.md). Parent Q-REGIME-STRESS-1.
- **Q-ICT-SWEEPFVG-1** — PHAROS sweep→FVG→draw on US500 15m — closed **FALSIFIED 2026-06-17** (point +0.316R cleared the 0.2883R hurdle and direction is real, permutation p=0.014, but `drop-top-3 −0.152R` + back-loaded thirds → ~3-trade-concentrated, not a robust edge). First US500 loop; pre-reg locked then run same session. Closure [`Q-ICT-SWEEPFVG-1-closure-falsified.md`](../ltm/briefs/Q-ICT-SWEEPFVG-1-closure-falsified.md); consolidated ledger [`ops/instruments/SPX500.md`](../../ops/instruments/SPX500.md) (directional-signal belt finding retained).
- Q-SWAP-1/2/3/4, Q-REGIME-1/2, Q-REGIME-TIME-1, Q-DDTRIG-1, Q-FEED-1, Q-PARITY-1 — see their closure briefs in `docs/ltm/briefs/` (Q-FEED-1 restored 2026-08-11: [`Q-FEED-1-dukascopy-tv-feed-divergence.md`](../ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md)).
- **Q-ICT-CASCADE-1** — five-layer ICT cascade on US500 — **CLOSED 2026-06-19** (1M `INSUFFICIENT-N`; no deployable end-to-end edge). Closure stub: [`closures/Q-ICT-CASCADE-1-closure-insufficient-n.md`](closures/Q-ICT-CASCADE-1-closure-insufficient-n.md); layer bodies in [`lab/archive/ict_cascade_2026-06-18/`](../../lab/archive/ict_cascade_2026-06-18/).
- **Q-USOIL-1** — USOIL regime-capture / Silver §9 counterbalance — **CLOSED / SUBTRACT 2026-08-09** (GSUB-1 b4; expired PARK). Closure: [`closures/Q-USOIL-1-closure-subtract.md`](closures/Q-USOIL-1-closure-subtract.md) · [`b4`](../pursuits/b4-q-usoil-1.md).

> Forward triggers (methodology 90-day review 2026-07-29; 08-08 packet — C2→C0 revert check **retired** 2026-07-22 per rescope ADR D2 addendum) live in `STATE.md` §Scheduled forward triggers / pointer log, not here. Full living-board sync of retired lines is a deferred doc-drift session.
