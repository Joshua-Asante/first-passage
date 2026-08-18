# Open-Question Roster (Q-roster)

Created 2026-06-13 as part of the Notion Phase-2 migration (`docs/adr/2026-06-12-notion-surface-retirement.md` §2.5).
The Notion Command Center previously held the live Q-roster; that surface is retired (read-only). This file is the
repo home for **open / dormant** investigation questions — one home per open Q. Closed questions live in `docs/ltm/briefs/`
(and `git log`) as their own closure briefs; they are not re-listed here.

**Convention:** each open Q has exactly one canonical repo home (the row's "Home"). When a Q closes, move it to a
closure brief in `docs/ltm/briefs/` and delete its row here.

## Open

| Q | Status | Home (canonical) | Next action |
|---|---|---|---|
| **Q-XMEM-1** — cost of per-surface agent-memory invisibility; time-boxed Mem0 sidecar pilot (prefs/pointers only) | **`OPEN`** (architecture + §6 frozen 2026-07-16; v1.2 Limb B FTS landed 2026-08-15, **re-measured `ASSISTIVE-ONLY`** same day — beats `rg` (0.500 vs 0.088) but below the 0.70 floor even after the one permitted corpus widening; T0 not started) | [`Q-XMEM-1-cross-surface-memory-sidecar-pilot.md`](Q-XMEM-1-cross-surface-memory-sidecar-pilot.md) · [pre-reg](pre-registration/Q-XMEM-1-verdict-preregistration.md) · [v3 remeasure](pre-registration/2026-08-15-fts5-delete-falsifier-prereg-v3.md) · [`RESULTS`](../../lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md) | Limb B: `scripts/repo_retrieve.py` on hot surfaces — **do not paste its output as a sub-rule 8/10 attestation**; `ASSISTIVE-ONLY` is final under the frozen v3 table (no further re-measurement without a fresh registration). Limb A Mem0 T0 unpaid — **operator GO only** (original §6). Limb C (local-embedder) is now a live question, not authorized to build. Do **not** store Rule-7 values. |
| **Q-TOM-SPX-1** — SPX500 turn-of-month existence and capturability | Layer A **RESOLVED-ABSENT** on canonical Pepperstone (2026-06-16); formal DEAD close reserved | [`docs/briefs/Q-TOM-SPX-1.md`](Q-TOM-SPX-1.md) | Run only the brief-reserved native Pine confirmation. Do not widen the window, change thresholds, or rerun Dukascopy to rescue the null. |
| **Q-SIGID-1** — measured live↔backtest signal-identity gap from mid-bar `alert()`/`strategy.entry` on c1 venue editions; architectures that close it (locked-axis, not EQ) | **`OPEN`** 2026-07-28 — cheap falsifier: 07-28 MNQ bar is a phantom (`longSignal` mid-true / close-false on `body_ok`); offline phantoms ~0.7× confirmed signals; Fri §2b clean re-measure owed | [`Q-SIGID-1-intra-bar-signal-identity.md`](Q-SIGID-1-intra-bar-signal-identity.md) · [pre-reg](pre-registration/Q-SIGID-1-verdict-preregistration.md) · [RESULTS](../../lab/analysis/c1/c1_signal_identity_2026-07-28/RESULTS.md) | **STRANDED on alert / signal-host disposition** (F2 closed via S1; Rule-11 intercept 2026-08-06) — §2b needs no fill/order/arming; offline limb MNQ 0.68 / MYM 0.70 stands. Pine edit only under separate operator GO. |
| **Q-FILLTAX-1** — TV fill-optimism gap + Pine↔Python / engine↔TV parity | **`OPEN`** — V2 Phase-0 scaffold `CODE_LANDED` 2026-08-07 ($0 under S1 incumbent); V1 disposition follows S1 (Tradeify geometry); Gate RESOLVED needs first family TV anchor | [`Q-FILLTAX-1-fill-realism-and-parity-scoping.md`](Q-FILLTAX-1-fill-realism-and-parity-scoping.md) · [`parity_gen2`](../../lab/analysis/c1/parity_gen2_2026-08/) · [`RESULTS`](../../lab/analysis/c1/parity_gen2_2026-08/RESULTS.md) | Operator: first family same-feed CME TV anchor → Gen-2 ADMIT. No post-hoc band tuning. Mutation battery (Phase 1) still owed. |

## Dormant (no current session home; resurface before assuming dead)

| Q | Status | Home | Note |
|---|---|---|---|
| ~~**Q-FUNDPOL-1** — funded-phase policy inheritance~~ → **DORMANT 2026-08-04** (§6 gate retired — eval pass converting cannot occur; Select-Flex thresholds non-transferable). §8 pre-reg (`d0200a4`, **K frozen = 4**) + P1/P2 discharges **unspent**; §1–§5 analysis retained as worked method. **Do not build** §9-C1 / `PAYOUT_MIN → 0`. | measurement / method record | [`Q-FUNDPOL-1-funded-phase-policy-inheritance.md`](Q-FUNDPOL-1-funded-phase-policy-inheritance.md) · pre-reg [`Q-FUNDPOL-1-verdict-preregistration.md`](pre-registration/Q-FUNDPOL-1-verdict-preregistration.md) | Successor venue needs a **new derivation**, not this brief rescheduled. |

## Recently closed (cross-reference; not open)

- **Q-CONDVAL-1** — does the validated CL range-state lift buy anything in R terms —
  **`FALSIFIED` 2026-08-18** — committed C−U 0.130 < frozen `L_star` 0.423 at the N-EDGE
  cell (R=$75, RT=$4.12, slate-2 center); S1b conditioner-engineering branch parked; O2
  discharged; SIGNAL-GENERIC stands. $0/K=0.
  [`closure`](closures/Q-CONDVAL-1-closure-falsified.md) ·
  [`RESULTS`](../../lab/analysis/_inbox/q_condval_1_2026-08/RESULTS.md) ·
  [`brief`](Q-CONDVAL-1-range-state-r-terms.md) ·
  [`pre-reg`](pre-registration/Q-CONDVAL-1-verdict-preregistration.md).
- **Q-POLFRONT-1** — policy-augmented seed-target frontier — **`RESOLVED-QUANTIFIED` 2026-08-16**
  (median R_max ratio policy/flat = **5.107×** ≥ 1.25× bar, 24/30 cells defined, min 1.526×, 2
  newly-admitted cells, no reversal under quantization). ⚠ **Load-bearing caveat carried
  forward, not a footnote:** the policy's bust rate is far more EOD-clock-fragile than flat
  sizing (median stress delta +55.2pp vs +1.63pp) — feeds deep-lane GO-1 **with the caveat
  named in the first campaign's prereg**; intraday-honest remeasurement fork named, not opened.
  [`closure`](closures/Q-POLFRONT-1-closure-resolved-quantified.md) ·
  [`RESULTS`](../../lab/analysis/c1/q_polfront_1_2026-08/RESULTS.md) ·
  [`brief`](Q-POLFRONT-1-policy-augmented-seed-frontier.md)
- **Q-EVALSEQ-1** — within-eval front-load schedule (frozen K=4 family) — **`FALSIFIED` 2026-08-16**
  (best lift −1.06pt vs +5pt bar; flat WATCH-1 stands; K=3 consumed). **Surviving finding:**
  cushion-proportional sizing cut bust 20.18% → 0.00% (both halves) at 1.06pt of pass — routed to
  Q-POLFRONT-1 (bust-axis reframe). No θ-retune of the family; no registry row (policy-lever, not
  mechanism). [`closure`](closures/Q-EVALSEQ-1-closure-falsified.md) ·
  [`RESULTS`](../../lab/analysis/c1/q_evalseq_1_2026-08/RESULTS.md) ·
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
  [`RESULTS`](../../lab/analysis/c1/mnq_capflow_orb_r_2026-08/RESULTS.md).
- **Q-TNEC-CON-5** — impulse→pullback→VWAP-reclaim (pullback stop; first/session) —
  **`AMBIGUOUS-HOLD` → Branch A STOP 2026-08-12** — non-promotable; CONFIRM unread forever;
  dense-1m OHLCV temporal-selectivity lane default **paused** pending new modality /
  non-route-① thesis; lane FALSIFIED counter unchanged **1/3**. Cap unclaimed.
  [`closure`](closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) ·
  [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/RESULTS.md).
- **Q-TNEC-CON-4** — PDH/PDL RTH with-break — **`AMBIGUOUS-HOLD` 2026-08-11**; successor
  CON-5 Branch A STOP paused the lane, so this row left Open. INDEX repair 2026-08-15
  (liveness sweep). CONFIRM unread; Cap unclaimed.
  [`closure`](closures/Q-TNEC-CON-4-closure-ambiguous-hold.md) ·
  [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md).
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


These had Notion tracker cards that are now retired. Closure records live in `docs/ltm/briefs/` / `git log`:

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
