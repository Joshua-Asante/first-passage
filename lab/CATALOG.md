# Lab analysis catalog

Open this file first for lab decisions. Hot bodies live under
`lab/analysis/<theme>/<slug>/`; archived studies are stub-only under
`lab/analysis/<slug>/CARD.md` (body in `lab/archive/<slug>/`).

Do not glob `lab/analysis/` alone to infer what is live.

**Camp layout (pytest):** every candidate directory that carries `test_*.py`
must include an empty `__init__.py` at scaffold time (and keep it when
archived). Hyphenated slugs (`…_2026-08`) are **not** valid package names, so
the marker alone cannot uniquify shared basenames under prepend —
`validation-controls` therefore runs `pytest lab/ --import-mode=importlib`.
Sibling imports of camp-local modules (especially shared names like
`construct_lib`) must use
[`research_utils.camp_import.load_camp_sibling`](research_utils/camp_import.py).
Still ship the `__init__.py` marker: valid-identifier camps need it, and it
documents the camp boundary for humans/tools.

## Active

### c1

| slug | theme | status | hot | one-liner | body | heavy |
|---|---|---|---|---|---|---|
| a2_panel_noise_venue_bound_2026-08-24 | c1 | ACTIVE | yes | A2 uncertainty is the 520-week DGP panel, not MC path count; size-invariant eval bound leaves corpus-max annSR 2.1× short of a six-month pass | lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/ | — |
| aegis1p_3leg_rescore_2026-07-27 | c1 | ACTIVE | yes | Aegis@1.00% 3-leg corrected-geometry re-MC under Tradeify envelope | lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/ | — |
| aegis3leg_engine_param_2026-08-20 | c1 | ACTIVE | yes | Parameterized Aegis 3-leg rescore engine (default 1.00% only; J14 bars new risk-arm measurement) | lab/analysis/c1/aegis3leg_engine_param_2026-08-20/ | — |
| aegis_orbmnq_combined_book_2026-08-26 | c1 | ACTIVE | yes | naive equal-risk Aegis-6J1+ORB-MNQ-1 combined book (each leg fails Tradeify solo, §0) — headline 1.51%/0.01% bust REVISED §9/§10: 1yr fails a proper both-halves regime bootstrap and gets worse under every tested correction; 3yr — the one cell §9 found survived both halves — now ALSO fails both halves (3.29%/5.37%) once tail-consistent sizing + a genuine timestamp-sequenced intraday-honest remeasure are compounded (§10.2); no tested config on either window now survives | lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/ | — |
| band_quantization_2026-08-02 | c1 | ACTIVE | yes | MNQ zero-floors at every FRIENDLY tier below 100K under the locked-proportional split; the two published 50K clearers describe a book the integer rail cannot instantiate | lab/analysis/c1/band_quantization_2026-08-02/ | — |
| c1_band_rescore_2026-07-24 | c1 | ACTIVE | yes | two Part A clearers at 50K band; RIDER FAIL stands a fortiori | lab/analysis/c1/c1_band_rescore_2026-07-24/ | — |
| c1_cadence_coverage_2026-08-03 | c1 | ACTIVE | yes | 0.50× fails 16.0% of eval starts once overlapping pyramid holds are priced; 0.40× is clean; one incumbent-shaped leg halves the cadence gap rather than closing it | lab/analysis/c1/c1_cadence_coverage_2026-08-03/ | — |
| c1_cadence_inactivity_2026-08-02 | c1 | ACTIVE | yes | token trade owed 82/312 Mon–Fri weeks (max 4 consecutive); 0.50× haircut raises inactivity exposure | lab/analysis/c1/c1_cadence_inactivity_2026-08-02/ | — |
| c1_cost_geometry_mym_add_2026-07-24 | c1 | ACTIVE | yes | MYM add@67 TBBO cost geometry; D1 inside-sufficiency measured 0.0 | lab/analysis/c1/c1_cost_geometry_mym_add_2026-07-24/ | — |
| c1_liveness_diversification_2026-08-02 | c1 | ACTIVE | yes | how much an added leg cuts dead weeks on the c1 book | lab/analysis/c1/c1_liveness_diversification_2026-08-02/ | — |
| c1_signal_identity_2026-07-28 | c1 | ACTIVE | yes | Full-panel MEASURED (2026-07-29); Q-SIGID-1 §6 offline limb is FULL | lab/analysis/c1/c1_signal_identity_2026-07-28/ | — |
| c1_thirdleg_instrument_map_2026-07-27 | c1 | ACTIVE | yes | Stage 1 discharges the contract-specs limb; Stage 2 measured sigma + tau_max for all four (RESULTS_stage2.md) | lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/ | — |
| catalogue_k_wall_2026-08-05 | c1 | ACTIVE | yes | — | lab/analysis/c1/catalogue_k_wall_2026-08-05/ | — |
| cheap_falsifiers_2026-08 | c1 | HOLD | yes | parent-side cheap falsifiers for the TNEC/dense-1m lane (spent; stay hot while CON-* cite them) | lab/analysis/c1/cheap_falsifiers_2026-08/ | — |
| class_s_c1_haircut_regime_remc_2026-07-16 | c1 | ACTIVE | yes | lifecycle-haircut regime re-MC for Class-S candidate #1 | lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/ | — |
| class_s_candidate1_scoring_2026-07-15 | c1 | ACTIVE | yes | G0–G8 scoring for Class-S candidate #1 (locked-book MYM+MNQ) | lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/ | — |
| eval_inverse_requirements_2026-08-03 | c1 | ACTIVE | yes | Max risk/trade is ~flat in trades/day, so daily profit scales with frequency not size; 3-day archetype needs ~8 trades/day vs the c1 book's 1.6 | lab/analysis/c1/eval_inverse_requirements_2026-08-03/ | — |
| eval_shape_diagnostics_2026-07-28 | c1 | ACTIVE | yes | eval-shape diagnostics under corrected Tradeify geometry | lab/analysis/c1/eval_shape_diagnostics_2026-07-28/ | — |
| eval_slow_archetype_2026-08-04 | c1 | ACTIVE | yes | — | lab/analysis/c1/eval_slow_archetype_2026-08-04/ | — |
| f3_cadence_successor_venues_2026-08-05 | c1 | ACTIVE | yes | F3 is decidable: Bulenox and MFFU share Tradeify's inactivity-death class; BluSky's real limit is 22 idle business days | lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/ | — |
| firm_model_repair_r1_7tier_2026-08-23 | c1 | ACTIVE | yes | W1 pattern extended to all 7 Bulenox/BluSky `dd_type="trailing"` tiers (Q-FIRMEOD-1 successor); all 7 flip CLOCK on direct `simulate_path` diff; no verdict flips on the 2 tiers with a published figure on the live book but 1.00x deepens ~7.6x (Bulenox 3.51%→26.77%, BluSky 4.44%→32.26%); 0.50x WATCH-1 both 0.08%→0.59% (still PASS, 2.41pp headroom); BluSky_Premium_50K alone carries no published figure — the other 4 Bulenox tiers DO (closed/NO-GO'd archived book, §2/§4b; 2026-08-23 fix-pass corrected a false "5 tiers none" claim) | lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/ | — |
| geofit_iid_sufficiency_power_2026-08-15 | c1 | ACTIVE | yes | Scoping probe (not a Q-GEOFIT-1 reopen); stays hot because aegis3leg_engine_param imports this scoring tree; $0/K=0 | lab/analysis/c1/geofit_iid_sufficiency_power_2026-08-15/ | — |
| geofit_skewed_family_construction_2026-08-15 | c1 | ACTIVE | yes | Scoping construction of family_skewed_gamma (imported by the N-SURV magnitude probe); not a Q-GEOFIT-1 reopen; $0/K=0 | lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/ | — |
| mnq_event_ceiling_2026-08-04 | c1 | ACTIVE | yes | — | lab/analysis/c1/mnq_event_ceiling_2026-08-04/ | — |
| mnq_ofchan_routeb_2026-08 | c1 | ACTIVE | yes | — | lab/analysis/c1/mnq_ofchan_routeb_2026-08/ | — |
| mnq_orb_flow_depth_2026-08-18 | c1 | HOLD | yes | Operator HOLD 2026-08-23 — blocked at P0 twice (~$150 vs $125 ceiling); no pull run, $0 spent | lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/ | — |
| mnq_orb_flow_substrate_2026-08-05 | c1 | ACTIVE | yes | — | lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/ | — |
| mnq_orb_level_proximity_tod_2026-08-06 | c1 | ACTIVE | yes | — | lab/analysis/c1/mnq_orb_level_proximity_tod_2026-08-06/ | — |
| mnq_r2agrun_routeb_2026-08 | c1 | HOLD | yes | `AMBIGUOUS-HOLD` — empty candidate list (magnitude floor; G3 → **ITERATE**, not promote). | lab/analysis/c1/mnq_r2agrun_routeb_2026-08/ | — |
| mnq_selection_ceiling_allbars_2026-08 | c1 | ACTIVE | yes | — | lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/ | — |
| mnq_sizediv_blind_2026-08 | c1 | ACTIVE | yes | — | lab/analysis/c1/mnq_sizediv_blind_2026-08/ | — |
| mnq_stop_distribution_2026-08-02 | c1 | ACTIVE | yes | MNQ stop distribution vs qty≥1 floor — Monday window realism | lab/analysis/c1/mnq_stop_distribution_2026-08-02/ | — |
| mnq_tnec_con2_compression_break_2026-08 | c1 | HOLD | yes | `AMBIGUOUS-HOLD` — gross-positive / net-negative; halves sign-flip; non-promotable close. | lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/ | — |
| mnq_tnec_con3_htf_native_break_2026-08 | c1 | HOLD | yes | `AMBIGUOUS-HOLD` — long mean net-positive but CI straddles 0; short net-negative; aux limbs fail live-pass. | lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/ | — |
| mnq_tnec_con4_pdh_pdl_break_2026-08 | c1 | HOLD | yes | `AMBIGUOUS-HOLD` — both arms near-zero; CIs straddle 0; aux limbs fail live-pass. | lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/ | — |
| mnq_tnec_con5_impulse_pullback_vwap_2026-08 | c1 | HOLD | yes | `AMBIGUOUS-HOLD` — both arms mean-negative; CIs straddle 0; aux limbs fail live-pass. | lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/ | — |
| mnqtape1_power_check_2026-08-23 | c1 | ACTIVE | yes | — | lab/analysis/c1/mnqtape1_power_check_2026-08-23/ | — |
| msl_monsurf_1_idle_clock_2026-08 | c1 | ACTIVE | yes | `Q-MONSURF-1` M-B idle-clock monitor — `RESOLVED` 2026-08-23: 0 missed / 0 spurious across all 312 real historical weeks, mutation-verified. Registration-ready (gated on F3 only). [closure](../../../docs/briefs/closures/Q-MONSURF-1-closure-resolved.md) | lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08/ | — |
| msl_s2b_mym_2026-08 | c1 | HOLD | yes | STAGE-1 FAIL / pre-G0 kill; MSL-S2B closed, archive still owed | lab/analysis/c1/msl_s2b_mym_2026-08/ | — |
| msl_s4_mgc_2026-08 | c1 | HOLD | yes | MSL-S4 `expiry-oi-strike-convergence` (NEW) on MGC — G0 FROZEN, Pine authored CC-solo; discharges the 2026-08-14 WHO-track E1 stop rule; Explore-confirm deferred by operator override (no data access); operator TV backtest owed (⚠ stale — Explore-confirm ran 2026-08-21 → `AMBIGUOUS-HOLD` → operator `PARKED` same day, hash-pinned 2026-08-23; no TV backtest currently owed — see README Addendum in lab/analysis/c1/msl_s4_mgc_2026-08/ and core/strategies/candidates/candidates_CARD.md) | lab/analysis/c1/msl_s4_mgc_2026-08/ | — |
| orbcush_orbpos_refit_2026-08 | c1 | ACTIVE | yes | — | lab/analysis/c1/orbcush_orbpos_refit_2026-08/ | — |
| orbmnq1_cushion_sizing_probe_2026-08-20 | c1 | ACTIVE | yes | Informal $0/K=0 probe (not pre-registered) — cushion-proportional sizing eliminates ORB-MNQ-1's bust intraday-honestly (mathematically real, regime-agnostic); a real 2021-09-28 pass-rate regime break survives a thirds split but its trailing-vol mechanism is REFUTED. Formalized as [`Q-ORBCUSH-1`](../../../docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md), which itself closed `FALSIFIED` 2026-08-20 (trailing mean-R also refuted — `ops/instruments/MNQ.md` N17). | lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/ | — |
| orbmnq1_nsurv_magnitude_probe_2026-08-20 | c1 | ACTIVE | yes | N=50 magnitude-resampled skewed-gamma fit to ORB-MNQ-1's own P&L, testing whether cushion-sizing bust-elimination is robust or a lucky single-history draw. Bust axis: 50/50 robust. Pass axis: real ~50/50 proposition (sd 24pp). See [MNQ.md](../../../ops/instruments/MNQ.md) N18. | lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/ | — |
| orbmnq1_skew_sizing_probe_2026-08-20 | c1 | ACTIVE | yes | Skew-derived `pol_cushion` sizing ceiling vs the borrowed 0.75 constant — informal $0/K=0 null, neither derived candidate beats the borrowed constant on pass rate. See [MNQ.md](../../../ops/instruments/MNQ.md) N18. | lab/analysis/c1/orbmnq1_skew_sizing_probe_2026-08-20/ | — |
| parity_gen2_2026-08 | c1 | ACTIVE | yes | — | lab/analysis/c1/parity_gen2_2026-08/ | — |
| q_orbpos_1_2026-08 | c1 | ACTIVE | yes | — | lab/analysis/c1/q_orbpos_1_2026-08/ | — |
| q_polfront_1_2026-08 | c1 | ACTIVE | yes | — | lab/analysis/c1/q_polfront_1_2026-08/ | — |
| q_rail_1_2026-07 | c1 | ACTIVE | yes | c1 rail Phases 0–4 CLOSED RESOLVED; ceiling $700 operator-signed | lab/analysis/c1/q_rail_1_2026-07/ | — |
| research-analyst-mnq-atomic-facts-2026-08-19 | c1 | ACTIVE | yes | Research Analyst inaugural session — MNQ atomic-fact decomposition draft (cross-campaign synthesis, not a new backtest); routing corrected same-day 2026-08-19 (DROP D5 -- already killed twice, ledger-contradicted first GRADUATE call / HOLD temporal-selectivity / DROP weekly-bias) | lab/analysis/c1/research-analyst-mnq-atomic-facts-2026-08-19/ | — |
| shape_feasibility_map_2026-08 | c1 | ACTIVE | yes | 945-cell region published (Select/MFFU/Growth); Select≡MFFU; §4 sims_per_seed reduction accepted; screens shape, not mechanisms | lab/analysis/c1/shape_feasibility_map_2026-08/ | — |
| tradeify_book_composition_2026-07-23 | c1 | ACTIVE | yes | eval-lock fix + §2 book-composition re-derivation | lab/analysis/c1/tradeify_book_composition_2026-07-23/ | inputs gitignored |
| tradeify_eval_lock_correction_2026-07-22 | c1 | ACTIVE | yes | Tradeify/MFFU eval drawdown-lock correction re-MC | lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/ | — |
| tradeify_fade_stage0_2026-07-30 | c1 | ACTIVE | yes | Stage 0 instrumentation complete; Stage 1 region computed at 1x/2x/4x; no mechanism scored, K=0, $0 spend | lab/analysis/c1/tradeify_fade_stage0_2026-07-30/ | — |
| tradeify_futures3_bustcut_2026-07-11 | c1 | ACTIVE | yes | Tradeify Select Flex 50K bust-cut Tests 1+2 | lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/ | — |
| tradeify_futures3_remc_2026-07-11 | c1 | ACTIVE | yes | Tradeify Select Flex 3-leg futures remc panel | lab/analysis/c1/tradeify_futures3_remc_2026-07-11/ | — |
| tradeify_seed_target_spec_2026-08-04 | c1 | ACTIVE | yes | At the Part A gate the binding constraint is the weekly activity rule; a token trade swings pass from 3.0% to ~99.4% | lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/ | — |
| tvcov_2026-07 | c1 | ACTIVE | yes | TV intraday bar-coverage census (Q-TVCOV-1) | lab/analysis/c1/tvcov_2026-07/ | — |
| venuegeo_dp3_bustceiling_2026-08-05 | c1 | ACTIVE | yes | Bust-ceiling half of DP3 measured; EV/$ half not run (eval purchase prices unsourced); does not close H-VENUEGEO-1 | lab/analysis/c1/venuegeo_dp3_bustceiling_2026-08-05/ | — |
| wstruct_cost_geometry_2026-07-28 | c1 | ACTIVE | yes | corrects WSTRUCT-M2K-1 §2.2 on cost; asymmetric-payoff frontier is OPEN but harvest returns 0 seeds (modality-barred) | lab/analysis/c1/wstruct_cost_geometry_2026-07-28/ | — |

### striker

| slug | theme | status | hot | one-liner | body | heavy |
|---|---|---|---|---|---|---|
| striker_mym_reconstruction_candidate1_2026-07 | striker | ACTIVE | yes | S-MYM-ORC-02 development candidate (reconstruction TERMINAL lane) | lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/ | — |

### orb

| slug | theme | status | hot | one-liner | body | heavy |
|---|---|---|---|---|---|---|
| d5_nq_intraday_mom_2026-07 | orb | ACTIVE | yes | Baltussen H1 on NQ IS — Stage-2/4 results | lab/analysis/orb/d5_nq_intraday_mom_2026-07/ | — |
| eodadv_mnq_2026-08 | orb | FALSIFIED | yes | no pre-registered mechanism survives; 15:30 exit stays barred | lab/analysis/orb/eodadv_mnq_2026-08/ | — |
| orb_mnq_2026-07 | orb | ACTIVE | yes | NAS100-ORB-30 on native MNQ; Stage-2 cost-law PASS then T2 payability FIRED | lab/analysis/orb/orb_mnq_2026-07/ | inputs gitignored |
| orb_mnq_recon_v3_2026-08-31 | orb | ACTIVE | yes | Bust/pass rope walk on the recon-v3 DD-tuning candidate (core/strategies/candidates/orb_mnq_recon_v3.pine) — FAILS the live Tradeify gate (bust<=5.0%) at every k=1-3; k=1 20.78% intraday-honest bust, 4.2x over — real ~3.25x improvement vs frozen construct's 67.67% (T2 ADR) but not close to clearing | lab/analysis/orb/orb_mnq_recon_v3_2026-08-31/ | — |
| orb_universe_2026-06-22 | orb | ACTIVE | yes | which FXIFY CFD best suits Opening Range Breakout | lab/analysis/orb/orb_universe_2026-06-22/ | pkl gitignored |
| sessconf_mnq_2026-08 | orb | ACTIVE | yes | faithful close_tod session-truncation sweep (MNQ, Tradeify) | lab/analysis/orb/sessconf_mnq_2026-08/ | — |

### aegis

| slug | theme | status | hot | one-liner | body | heavy |
|---|---|---|---|---|---|---|
| aegis_6j_prop_reconstruction_2026-07 | aegis | ACTIVE | yes | Stage-1 FALSIFIED (operator accepted); Wave-1 sweep artifacts retained hot | lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/ | — |
| aegis_6j_trail_tradeify_2026-07-29 | aegis | ACTIVE | yes | J4 re-run at true Tradeify Select 100K geometry (Aegis→6J v0.3) | lab/analysis/aegis/aegis_6j_trail_tradeify_2026-07-29/ | — |
| aegis_6j_transfer_2026-07-05 | aegis | ACTIVE | yes | Bulenox Option-2 trail-survival MC sequence (Aegis→6J v0.3) | lab/analysis/aegis/aegis_6j_transfer_2026-07-05/ | inputs gitignored |

### regime

| slug | theme | status | hot | one-liner | body | heavy |
|---|---|---|---|---|---|---|
| decompound_remc_2026-06-07 | regime | ACTIVE | yes | decompounded full-history MC breaches both lock gates | lab/analysis/regime/decompound_remc_2026-06-07/ | inputs gitignored |
| q_ddtrig_1_2026-06-07 | regime | ACTIVE | yes | dd_protection trigger re-MC on proposed de-risk bundle | lab/analysis/regime/q_ddtrig_1_2026-06-07/ | inputs gitignored |
| regime_fit_2026-06-17 | regime | ACTIVE | yes | Q-REGIME-FIT-1 closure findings | lab/analysis/regime/regime_fit_2026-06-17/ | — |
| regime_oos_2026-06-21 | regime | ACTIVE | yes | Phase-1 gold-gate face-validity (descriptive, unscored) | lab/analysis/regime/regime_oos_2026-06-21/ | — |
| regime_postcovid_2026-06-22 | regime | ACTIVE | yes | post-COVID held-out regime probe | lab/analysis/regime/regime_postcovid_2026-06-22/ | — |
| regime_stress_2026-06-15 | regime | ACTIVE | yes | regime-stress investigation chain | lab/analysis/regime/regime_stress_2026-06-15/ | — |
| regime_time_cost_2026-06-09 | regime | ACTIVE | yes | Q-REGIME-TIME-1 RESOLVED-LARGE, but stagnation's recoverable cost is tail-risk/survivability, not speed | lab/analysis/regime/regime_time_cost_2026-06-09/ | — |

### harvest

| slug | theme | status | hot | one-liner | body | heavy |
|---|---|---|---|---|---|---|
| disccamp0_gc_2010_18 | harvest | ACTIVE | yes | DISC-CAMP-0 binding artifacts (Stage 2/3/5 staging) | lab/analysis/harvest/disccamp0_gc_2010_18/ | — |
| driftex_2026-08 | harvest | FALSIFIED | yes | drift exhaustion is not the mechanism; phenomenon is equity-index-specific | lab/analysis/harvest/driftex_2026-08/ | — |
| fts5_delete_falsifier_2026-07-27 | harvest | ACTIVE | yes | FTS5-as-Delete falsifier harness results | lab/analysis/harvest/fts5_delete_falsifier_2026-07-27/ | — |
| h_od_1_es_overnight_drift_2026-07 | harvest | ACTIVE | yes | SR917 overnight hour on ES IS — Stage-2/4 results | lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/ | — |
| harv_a4_footprint_2026-07 | harvest | ACTIVE | yes | A4 month-end footprint diagnostic (Cursor return) | lab/analysis/harvest/harv_a4_footprint_2026-07/ | — |
| harvest_mechanism_deep_search_2026-07-23 | harvest | ACTIVE | yes | harvest mechanism deep search fan-out (2026-07-23) | lab/analysis/harvest/harvest_mechanism_deep_search_2026-07-23/ | — |
| koijen_axis2_openalex_2026-08-17 | harvest | ACTIVE | yes | Koijen Carry axis-2 OpenAlex substitute traversal — 6 screen-level leads survived, none Req-1a admitted | lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/ | — |
| limb_b_remeasure_2026-08 | harvest | ACTIVE | yes | FTS5-as-Delete falsifier v3 (Limb B re-measurement) results | lab/analysis/harvest/limb_b_remeasure_2026-08/ | — |
| q_kbudget_harvest_1_2026-07 | harvest | ACTIVE | yes | Phase-1 literature fan-out + Phase-2 K-budget ratification | lab/analysis/harvest/q_kbudget_harvest_1_2026-07/ | — |
| radar_tier_a_burst_2026-07 | harvest | ACTIVE | yes | First burst executed; H-TSMOM-6J Clause-N FAIL; carry moments recovered / timing still UNSCREENABLE; not archiveable | lab/analysis/harvest/radar_tier_a_burst_2026-07/ | — |
| six_lead_cf_2026-08-17 | harvest | ACTIVE | yes | P1/P2 CF FAIL all four legs; P3 dry-run $0 then CLOSED (calendar-spread SCREEN-FAIL); L3=L6 same-paper (6→5); P4 route memo → HOLD (data-sourcing question); P5 access probe → `UNSCREENABLE`, CLOSED | lab/analysis/harvest/six_lead_cf_2026-08-17/ | — |
| st_eh_2026-07 | harvest | ACTIVE | yes | ST-EH campaign engine + fidelity harness (harvest) | lab/analysis/harvest/st_eh_2026-07/ | — |
| tnec_l2_sourcing_2026-08-10 | harvest | ACTIVE | yes | TNEC L2 sourcing pass — R8 gold-fix δ-extracted SCREEN-FAIL (informed-flow + cost-law); C2/C3/C4 closed at 0 admissible | lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/ | — |

### mc

| slug | theme | status | hot | one-liner | body | heavy |
|---|---|---|---|---|---|---|
| mc_mdd_closed_form_2026-08 | mc | ACTIVE | yes | Magdon-Ismail (2004) closed-form G_D vs `simulate_path` absolute-$ trailing bust rates | lab/analysis/mc/mc_mdd_closed_form_2026-08/ | — |

### legacy

| slug | theme | status | hot | one-liner | body | heavy |
|---|---|---|---|---|---|---|
| eurusd_pattern_enum | legacy | ACTIVE | yes | EURUSD pattern-enumeration harness | lab/analysis/legacy/eurusd_pattern_enum/ | — |
| futures_conversion_2026-07-01 | legacy | ACTIVE | yes | Phase A provisional MNQ/MYM granularity floors | lab/analysis/legacy/futures_conversion_2026-07-01/ | — |
| guardian_filter_sweep_2026-06-20 | legacy | ACTIVE | yes | Guardian XAUUSD filter-validity sweep harness | lab/analysis/legacy/guardian_filter_sweep_2026-06-20/ | — |
| guardian_parity_2026-06-23 | legacy | ACTIVE | yes | Guardian v5.5 parity port harness | lab/analysis/legacy/guardian_parity_2026-06-23/ | — |
| silver_be_off_2026-06-11 | legacy | ACTIVE | yes | Silver BE-off reconcile + remc gate harness | lab/analysis/legacy/silver_be_off_2026-06-11/ | — |
| silver_counterbalance_2026-06-13 | legacy | ACTIVE | yes | Silver counterbalance equity curve & required-hedge envelope | lab/analysis/legacy/silver_counterbalance_2026-06-13/ | — |
| silver_regime_2026-06-10 | legacy | ACTIVE | yes | Guardian Silver v1.0 allocation frontier + regime stress | lab/analysis/legacy/silver_regime_2026-06-10/ | — |
| us500_discovery_2026-06-22 | legacy | ACTIVE | yes | US500 widest-net edge discovery results | lab/analysis/legacy/us500_discovery_2026-06-22/ | — |
| xauusd_cgb_2026-06-15 | legacy | HOLD | yes | AMBIGUOUS (brief §6) / operational HOLD — build NOT triggered | lab/analysis/legacy/xauusd_cgb_2026-06-15/ | — |

### _inbox

| slug | theme | status | hot | one-liner | body | heavy |
|---|---|---|---|---|---|---|
| b2_london_fix_wake_2026-08-24 | _inbox | CLOSED | yes | B2.2 battery: 6E and 6B both DEAD via orthogonality (\|t\|<2/wrong-signed); placebo leg decisive only for 6B (rank 4.9) | lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/ | — |
| ict_1mexec_1_2026-08 | _inbox | FALSIFIED | yes | **RESOLVED (FALSIFIED at Stage 2, F1).** The frozen construct's gross edge does not | lab/analysis/_inbox/ict_1mexec_1_2026-08/ | — |
| ict_mnq_2026-08 | _inbox | ACTIVE | yes | ICT cascade on NQ/MNQ at $0/K=0: W and D confirm, pools falsified a 3rd time; no layer licenses a deployable edge | lab/analysis/_inbox/ict_mnq_2026-08/ | — |
| joint_surrogation_null_2026-08-30 | _inbox | ACTIVE | yes | Q-RANGEXFER-1/Q-VOLREGIME-1's joint-surrogation null design (D5 O1): 4 rounds, NOT RESOLVED — neither model adequacy nor size/power clears (26% empirical Type-I vs nominal 5%); hard stop fired. Closure-path plan authored (`BOUNDED_ROUND_PLAN.md`); operator ratified L5-gates-`FALSIFIED` + per-hypothesis `AMBIGUOUS-DESIGN`; Q-RANGEXFER-1 closed 2026-08-30 (see `rangexfer_presence_battery_2026-08-30`) — Q-VOLREGIME-1 remains independently assessed, not closed by inheritance | lab/analysis/_inbox/joint_surrogation_null_2026-08-30/ | — |
| mnq_dailygeom_notice_2026-08-29 | _inbox | ACTIVE | yes | MNQ 5-candidate Notice-phase geometry screen (K=5): overnight-range/gap-magnitude/volume-regime all GRADUATE at stage-1, now nested under Q-RANGEXFER-1/Q-VOLREGIME-1 pending Phase 1 | lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/ | — |
| mym_mechanism_harvest_2026-08-29 | _inbox | ACTIVE | yes | MYM 5-candidate Notice-phase Phase-2 batch (K=5), replicates MNQ's shape: overnight-range GRADUATE, gap-magnitude split by day-history stratum (bprime=0 INCREMENT / bprime=1 not established), volume-regime INCREMENT, CLV DROPPED | lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/ | — |
| q_trainkill_1_2026-08 | _inbox | HOLD | yes | AMBIGUOUS-HOLD — BOUNDED extremes disagree (MISCALIBRATED at ε vs KILLS-INFORMATIVE at 1−ε); scored core (n*=8) is MISCALIBRATED | lab/analysis/_inbox/q_trainkill_1_2026-08/ | — |
| q_trainkill_2_2026-08 | _inbox | HOLD | yes | `AMBIGUOUS-HOLD`. Limb 1 did not fire (1 promotion; extremes still disagree). Limb 2: both `NEG` and `DEP-ZERO` fit. | lab/analysis/_inbox/q_trainkill_2_2026-08/ | — |
| q_trainkill_3_2026-08 | _inbox | HOLD | yes | `AMBIGUOUS-HOLD`. Block F winner `NEG` (ratio 9.83). Block A winner `DEP` (ratio 0.246 = DEP at 4.06:1). Split. | lab/analysis/_inbox/q_trainkill_3_2026-08/ | — |
| rangecond_1_2026-08-30 | _inbox | FALSIFIED | yes | Q-RANGECOND-1: overnight-range-conditioned ORB-MNQ-1 payoff shape — CORRECTED 2026-08-31, retracting the original `RESOLVED` verdict. A look-ahead defect in data_lib.py::overnight_ohlc (Codex PR #227) inflated the original result; corrected, conditioned WR 47.98% vs unconditioned 47.22% (+0.75pp, CI includes 0), mean win -0.058R (sign-flipped, CI includes 0). `FALSIFIED`. Addendum on b3-orb-mnq-payability-line.md retracted; ORB-MNQ-1 stays PARKED, no new evidence. | lab/analysis/_inbox/rangecond_1_2026-08-30/ | — |
| rangestate_corrected_2026-08 | _inbox | ACTIVE | yes | Official corrected-null re-score: S1a (GC) NULL (L2, L4); S1b (CL) SIGNAL-GENERIC at the 69th pct of its linear-ACF band | lab/analysis/_inbox/rangestate_corrected_2026-08/ | — |
| rangestate_gc_2026-08 | _inbox | NULL | yes | `NULL`** (per the frozen §3 gate — limb `ci_lb` failed; | lab/analysis/_inbox/rangestate_gc_2026-08/ | — |
| rangestate_mcl_2026-08 | _inbox | ACTIVE | yes | SIGNAL-GENERIC under the corrected battery: canon-attributed vol clustering (69th pct); not a mechanism and no conditioner license | lab/analysis/_inbox/rangestate_mcl_2026-08/ | — |
| rangexfer_byyear_l4_2026-08-30 | _inbox | ACTIVE | yes | Q-RANGEXFER-1's L4 (by-year) presence limb, all 5 hypotheses: N_valid<7 on all five (AMBIGUOUS), confirming the pre-registration's own ex-ante prediction; corrected three times (PR #224 Codex review — qualifying-year gate fix; 2026-08-31 MNQ look-ahead fix; 2026-08-31 MYM scope-gap fix — n_valid counts shift, AMBIGUOUS routing unchanged on all five). Consumed into the presence-battery closure (`rangexfer_presence_battery_2026-08-30`) — Q-RANGEXFER-1 closed 2026-08-30 | lab/analysis/_inbox/rangexfer_byyear_l4_2026-08-30/ | — |
| rangexfer_presence_battery_2026-08-30 | _inbox | FALSIFIED | yes | MIXED — 4/5 hypotheses AMBIGUOUS-DESIGN, H-RANGEXFER-1.a-MYM FALSIFIED (presence L2 fails). | lab/analysis/_inbox/rangexfer_presence_battery_2026-08-30/ | — |
| volregime_byyear_l4_2026-08-31 | _inbox | ACTIVE | yes | L4 PASS independently on MNQ and MYM; L3 subsequently PASS on both, leaving L5 attribution open. | lab/analysis/_inbox/volregime_byyear_l4_2026-08-31/ | — |
| volregime_l3_2026-08-31 | _inbox | ACTIVE | yes | L3 PASS independently on MNQ and MYM; the presence battery is complete on both instruments and L5 attribution remains open. | lab/analysis/_inbox/volregime_l3_2026-08-31/ | — |
| volregime_l5_design_2026-08-31 | _inbox | ACTIVE | yes | L5 attribution design frozen (Packet B, B1-B5 complete): bar-native nested forward-prediction comparison replacing the retired day-level joint-surrogation adaptation; B5 ran 5 Codex review rounds, closed clean; no code executed, no real L5 statistic inspected; Packet C1 pilot GO is the next gate | lab/analysis/_inbox/volregime_l5_design_2026-08-31/ | — |
| volregime_l5_pilot_2026-08-31 | _inbox | ACTIVE | yes | Packet C1 acceptance bands frozen. Packet C2-C4 pipeline built (data prep, folds, S4.2-S4.4 null construction) and correctness-validated: identity-rotation reproduces real bias_volume exactly on both MNQ and MYM after fixing an excluded-day NaN cascade and an ungrouped-day exclusion gap; no large-scale simulation run yet, no real L5 statistic inspected; C2-C4 execution at the frozen N_outer=100/B=4000 scale and Packet D each need further separate authorization | lab/analysis/_inbox/volregime_l5_pilot_2026-08-31/ | — |
| mym_breakout_entry_2026_09 | _inbox | ACTIVE | yes | Five predeclared MYM opening-range entry families: none reaches +0.10R on validation; intended holdout was consumed and remains exploratory only | lab/analysis/mym_breakout_entry_2026_09/ | — |

## Archived

| slug | status | one-liner | card | body | heavy | closed |
|---|---|---|---|---|---|---|
| approach_scoreboard_2026-08 | CLOSED | Q-SCORE-1 Block 1 assignability under 80%; forward fields proposed; no runner | lab/analysis/approach_scoreboard_2026-08/CARD.md | lab/archive/approach_scoreboard_2026-08/ | — | 2026-08-13 |
| bulenox_futures_remc_2026-07-01 | CLOSED | R6 NO-GO — futures-prop program closed 2026-07-10 | lab/analysis/bulenox_futures_remc_2026-07-01/CARD.md | lab/archive/bulenox_futures_remc_2026-07-01/ | — | 2026-07-12 |
| c1_capalloc_2026-07-27 | CLOSED | `AMBIGUOUS (d)` — a dominating split exists under the modeled rules, but its | lab/analysis/c1_capalloc_2026-07-27/CARD.md | lab/archive/c1_capalloc_2026-07-27/ | — | 2026-08-03 |
| chop_native_leg_2026-06-30 | CLOSED | no viable candidate | lab/analysis/chop_native_leg_2026-06-30/CARD.md | lab/archive/chop_native_leg_2026-06-30/ | — | 2026-07-11 |
| class_s_aegis_solo_scoring_2026-07-16 | FALSIFIED | `FALSIFIED` | lab/analysis/class_s_aegis_solo_scoring_2026-07-16/CARD.md | lab/archive/class_s_aegis_solo_scoring_2026-07-16/ | — | 2026-07-17 |
| class_s_candidate2_scoring_2026-07-15 | FALSIFIED | `FALSIFIED — all-four-fail` | lab/analysis/class_s_candidate2_scoring_2026-07-15/CARD.md | lab/archive/class_s_candidate2_scoring_2026-07-15/ | — | 2026-07-17 |
| custodian_eurusd | CLOSED | SHELVED (probe not completed) | lab/analysis/custodian_eurusd/CARD.md | lab/archive/custodian_eurusd/ | — | 2026-07-11 |
| d5_recost_2026-07 | FALSIFIED | Stage-2 KILL (binding cause is edge decay, not cost). | lab/analysis/d5_recost_2026-07/CARD.md | lab/archive/d5_recost_2026-07/ | — | 2026-08-03 |
| decompound_ddprot_2026-06-21 | CLOSED | DONE_WITH_CONCERNS. | lab/analysis/decompound_ddprot_2026-06-21/CARD.md | lab/archive/decompound_ddprot_2026-06-21/ | — | 2026-07-12 |
| dl1_mgc_orc_2026-08-16 | CLOSED | `AMBIGUOUS` — ABANDONMENT (prereg roster mapping: confirm never read, nothing | lab/analysis/dl1_mgc_orc_2026-08-16/CARD.md | lab/archive/dl1_mgc_orc_2026-08-16/ | — | 2026-08-21 |
| dl2_m6a_pdhpdl_2026-08-22 | CLOSED | `AMBIGUOUS` -- ABANDONMENT (nominee V9 fails gates 2a/2b/2d; gate 2c passed; confirm never read) | lab/analysis/dl2_m6a_pdhpdl_2026-08-22/CARD.md | lab/archive/dl2_m6a_pdhpdl_2026-08-22/ | — | 2026-08-22 |
| dstruct_mnq_2026-08 | NULL | NULL — daily close-vs-EMA20 bias carries nothing at daily granularity (Tier-1 screen; 3 of 4 limbs failed) | lab/analysis/dstruct_mnq_2026-08/CARD.md | lab/archive/dstruct_mnq_2026-08/ | — | 2026-08-22 |
| external_sourcing_2026-06-30 | CLOSED | RESOLVED zero saved candidates (thesis-first narrow pass) | lab/analysis/external_sourcing_2026-06-30/CARD.md | lab/archive/external_sourcing_2026-06-30/ | — | 2026-07-12 |
| feed_divergence_2026-06 | CLOSED | RESOLVED-BY-RETIREMENT — Q-FEED-1 dissolved with the Dukascopy feed; byte-reading paths marked non-runnable | lab/analysis/feed_divergence_2026-06/CARD.md | lab/archive/feed_divergence_2026-06/ | — | 2026-08-03 |
| fixrev_costscreen_2026-06-22 | FALSIFIED | FAIL-COST** (best-of-grid break-even 0.277 pip vs FXIFY all-in 0.80 pip). | lab/analysis/fixrev_costscreen_2026-06-22/CARD.md | lab/archive/fixrev_costscreen_2026-06-22/ | — | 2026-07-11 |
| futures_prop_hold_compat_2026-06-30 | CLOSED | R6 NO-GO — futures-prop pivot closed | lab/analysis/futures_prop_hold_compat_2026-06-30/CARD.md | lab/archive/futures_prop_hold_compat_2026-06-30/ | — | 2026-07-12 |
| gbpusd_rank_cert | RETIRED | UNCERTIFIED — manual TV step never run; not carried (2026-07-10) | lab/analysis/gbpusd_rank_cert/CARD.md | lab/archive/gbpusd_rank_cert/ | — | 2026-07-12 |
| geofit_skew_probe_2026-07-25 | CLOSED | Scoping probe, not part of Q-GEOFIT-1 (CLOSED AMBIGUOUS-PARAMETERIZATION); no envelope, grid, or candidate claim | lab/analysis/geofit_skew_probe_2026-07-25/CARD.md | lab/archive/geofit_skew_probe_2026-07-25/ | — | 2026-08-03 |
| guardian_decay_gate_2026-06-25 | CLOSED | DP-1…DP-7 resolved and the gate built, then dormant — no live Guardian venue | lab/analysis/guardian_decay_gate_2026-06-25/CARD.md | lab/archive/guardian_decay_gate_2026-06-25/ | — | 2026-07-22 |
| guardian_silver_be_2026-06-10 | CLOSED | `DONE_WITH_CONCERNS` | lab/analysis/guardian_silver_be_2026-06-10/CARD.md | lab/archive/guardian_silver_be_2026-06-10/ | — | 2026-07-11 |
| harv_0_month_end_rebalance_es_2026-07 | CLOSED | H1 corroborated but placebo magnitude un-passable; successor pre-Q parked | lab/analysis/harv_0_month_end_rebalance_es_2026-07/CARD.md | lab/archive/harv_0_month_end_rebalance_es_2026-07/ | — | 2026-07-12 |
| ict_cascade_2026-06-18 | CLOSED | Q-ICT-CASCADE-1 CLOSED (1M insufficient N) | lab/analysis/ict_cascade_2026-06-18/CARD.md | lab/archive/ict_cascade_2026-06-18/ | — | 2026-07-12 |
| ict_revcon_2026-06-19 | CLOSED | CLOSED NOT-CONFIRMED — 1H REVCON ambiguous / insufficient N | lab/analysis/ict_revcon_2026-06-19/CARD.md | lab/archive/ict_revcon_2026-06-19/ | — | 2026-07-12 |
| ict_target_investigation_2026-08-20 | CLOSED | Zero-run distance sweep (5–300pt); mean R negative at every distance; DOL target exonerated, entries lack directional edge | lab/analysis/ict_target_investigation_2026-08-20/CARD.md | lab/archive/ict_target_investigation_2026-08-20/ | — | 2026-08-21 |
| identify_nas100_2026-06-20 | CLOSED | Identify-only incomplete; stats JSON only — closed without Question phase | lab/analysis/identify_nas100_2026-06-20/CARD.md | lab/archive/identify_nas100_2026-06-20/ | — | 2026-07-12 |
| mnq_capa_n14_tripwire_2026-08-06 | CLOSED | RESOLVED (W5) — Cap seat marked spent on this Route A cell | lab/analysis/mnq_capa_n14_tripwire_2026-08-06/CARD.md | lab/archive/mnq_capa_n14_tripwire_2026-08-06/ | — | 2026-08-13 |
| mnq_capflow_orb_r_2026-08 | FALSIFIED | `FALSIFIED` · **cap_spent:** `False` | lab/analysis/mnq_capflow_orb_r_2026-08/CARD.md | lab/archive/mnq_capflow_orb_r_2026-08/ | — | 2026-08-21 |
| mnq_con1_dense1m_stage0_2026-08 | FALSIFIED | `FALSIFIED` — ES/NQ 5m divergence explore; both arms CI&lt;0; STOP catalogue | lab/analysis/mnq_con1_dense1m_stage0_2026-08/CARD.md | lab/archive/mnq_con1_dense1m_stage0_2026-08/ | — | 2026-08-13 |
| mnq_fvg_draw_probe_2026-08-04 | CLOSED | UNDERPOWERED (n=117<150) and uniformly adverse (mean net −21.6 pt/trade); do not read as try-again-with-more-data | lab/analysis/mnq_fvg_draw_probe_2026-08-04/CARD.md | lab/archive/mnq_fvg_draw_probe_2026-08-04/ | — | 2026-08-13 |
| mnq_orb_level_proximity_2026-08-05 | CLOSED | VOID-TOD-CONFOUND (W6) — highest-precedence amended §7 gate; Δ not interpreted | lab/analysis/mnq_orb_level_proximity_2026-08-05/CARD.md | lab/archive/mnq_orb_level_proximity_2026-08-05/ | — | 2026-08-13 |
| mnq_orderflow_probe_2026-08-04 | FALSIFIED | V2 fired as pre-registered most likely: the observable book carries no | lab/analysis/mnq_orderflow_probe_2026-08-04/CARD.md | lab/archive/mnq_orderflow_probe_2026-08-04/ | — | 2026-08-13 |
| mnq_pool_shield_probe_2026-08-04 | FALSIFIED | V2 fired: mean net +0.017R/trade, CI straddles zero; shield never binds (nearest pool 572pt away) | lab/analysis/mnq_pool_shield_probe_2026-08-04/CARD.md | lab/archive/mnq_pool_shield_probe_2026-08-04/ | — | 2026-08-13 |
| mnq_r2flow_routeb_2026-08 | FALSIFIED | `FALSIFIED` — empty candidate list (G3 → **STOP** for this G0 catalogue). | lab/analysis/mnq_r2flow_routeb_2026-08/CARD.md | lab/archive/mnq_r2flow_routeb_2026-08/ | — | 2026-08-13 |
| mnq_r2vbuck_routeb_2026-08 | FALSIFIED | `FALSIFIED` — empty candidate list (G3 → **STOP** for this G0 catalogue). | lab/analysis/mnq_r2vbuck_routeb_2026-08/CARD.md | lab/archive/mnq_r2vbuck_routeb_2026-08/ | — | 2026-08-13 |
| mnq_selection_ceiling_2026-08 | FALSIFIED | `FALSIFIED` (C2) — oracle top-1/day mean net R is **below** EM1 0.40 on | lab/analysis/mnq_selection_ceiling_2026-08/CARD.md | lab/archive/mnq_selection_ceiling_2026-08/ | — | 2026-08-13 |
| mnq_sr_structure_2026-08-06 | CLOSED | 0/14 BH-FDR survivors; Phase B/C not licensed | lab/analysis/mnq_sr_structure_2026-08-06/CARD.md | lab/archive/mnq_sr_structure_2026-08-06/ | — | 2026-08-13 |
| msl_c1_mym_2026-08 | FALSIFIED | `FALSIFIED` | lab/analysis/msl_c1_mym_2026-08/CARD.md | lab/archive/msl_c1_mym_2026-08/ | — | 2026-08-13 |
| msl_c2_mgc_2026-08 | FALSIFIED | `FALSIFIED` | lab/analysis/msl_c2_mgc_2026-08/CARD.md | lab/archive/msl_c2_mgc_2026-08/ | — | 2026-08-13 |
| msl_c3_m2k_2026-08 | FALSIFIED | FALSIFIED — pdh-pdl-failed-break-reclaim both arms mean-negative (long −0.146R, short −0.196R); no axis promoted | lab/analysis/msl_c3_m2k_2026-08/CARD.md | lab/archive/msl_c3_m2k_2026-08/ | — | 2026-08-13 |
| msl_s2a_mcl_2026-08 | FALSIFIED | `FALSIFIED` (N-ACT: measured trades/week &lt; 1) | lab/analysis/msl_s2a_mcl_2026-08/CARD.md | lab/archive/msl_s2a_mcl_2026-08/ | — | 2026-08-13 |
| mym_3fps_recon_2026-07 | FALSIFIED | `FALSIFIED` | lab/analysis/mym_3fps_recon_2026-07/CARD.md | lab/archive/mym_3fps_recon_2026-07/ | — | 2026-08-03 |
| ng_eia_recon_2026-07 | FALSIFIED | FALSIFIED at Phase-0 — P0.2 power and P0.3 cost-law both fail; per-year sign alternates | lab/analysis/ng_eia_recon_2026-07/CARD.md | lab/archive/ng_eia_recon_2026-07/ | — | 2026-08-03 |
| noct_spx | FALSIFIED | FALSIFIED | lab/analysis/noct_spx/CARD.md | lab/archive/noct_spx/ | — | 2026-07-11 |
| nsurv_layer_design_2026-08-20 | CLOSED | Q-NSURV-2 RESOLVED; additive magnitude-resampling wrapper reproduces both candidates' headlines within 2.0pp | lab/analysis/nsurv_layer_design_2026-08-20/CARD.md | lab/archive/nsurv_layer_design_2026-08-20/ | — | 2026-08-21 |
| oanda_stage1 | RETIRED | OANDA retired 2026-06-24; frozen historical evidence | lab/analysis/oanda_stage1/CARD.md | lab/archive/oanda_stage1/ | — | 2026-07-12 |
| oil_carry | FALSIFIED | F1-FALSIFIED — rejected candidate | lab/analysis/oil_carry/CARD.md | lab/archive/oil_carry/ | — | 2026-07-12 |
| opening_pressure_map_2026-07 | FALSIFIED | `FALSIFIED` | lab/analysis/opening_pressure_map_2026-07/CARD.md | lab/archive/opening_pressure_map_2026-07/ | — | 2026-08-03 |
| orb_zb_recon_2026-07 | FALSIFIED | FALSIFIED at Phase-0 — P0.1 cost-law KILL on every window; ORB breakout has negative gross edge on ZB | lab/analysis/orb_zb_recon_2026-07/CARD.md | lab/archive/orb_zb_recon_2026-07/ | — | 2026-08-03 |
| orbmnq1_survivor_scoring_2026-08-20 | FALSIFIED | Full-panel k=2 misses the pass floor (41.51%<50%); post-break-only clears at both k | lab/analysis/orbmnq1_survivor_scoring_2026-08-20/CARD.md | lab/archive/orbmnq1_survivor_scoring_2026-08-20/ | — | 2026-08-21 |
| p2_replay_2026-07 | FALSIFIED | P2 FALSIFIED for this venue — both legs K2-kill | lab/analysis/p2_replay_2026-07/CARD.md | lab/archive/p2_replay_2026-07/ | — | 2026-07-12 |
| pharos_us500_sweepfvg | FALSIFIED | FALSIFIED (2026-06-17)** — directional signal is | lab/analysis/pharos_us500_sweepfvg/CARD.md | lab/archive/pharos_us500_sweepfvg/ | — | 2026-07-12 |
| q_bookfit_1_2026-07 | CLOSED | RESOLVED — 3/3 forks PASS (ρ<1.0 and n_eff_risk_delta>0 @ 0.37%) | lab/analysis/q_bookfit_1_2026-07/CARD.md | lab/archive/q_bookfit_1_2026-07/ | — | 2026-08-03 |
| q_compose_1_2026-07 | FALSIFIED | `FALSIFIED` (§6 row 2 — both limbs, every tier) | lab/analysis/q_compose_1_2026-07/CARD.md | lab/archive/q_compose_1_2026-07/ | — | 2026-07-20 |
| q_condval_1_2026-08 | FALSIFIED | `FALSIFIED` (S1b conditioner-engineering branch parked) | lab/analysis/q_condval_1_2026-08/CARD.md | lab/archive/q_condval_1_2026-08/ | — | 2026-08-21 |
| q_decay_1_2026-07-10 | CLOSED | SCOPE-SPLIT — Guardian-only coverage; rest UNCOVERED | lab/analysis/q_decay_1_2026-07-10/CARD.md | lab/archive/q_decay_1_2026-07-10/ | — | 2026-07-12 |
| q_evalseq_1_2026-08 | FALSIFIED | FALSIFIED — schedule lever spent for eval-pass lift (best −1.06pt vs +5pt bar); flat WATCH-1 stands | lab/analysis/q_evalseq_1_2026-08/CARD.md | lab/archive/q_evalseq_1_2026-08/ | — | 2026-08-21 |
| q_expr_1_2026-08 | CLOSED | H1 horizon-mismatch 4/4 models the orphaning; H2 1/5 misses; H3 cannot fire | lab/analysis/q_expr_1_2026-08/CARD.md | lab/archive/q_expr_1_2026-08/ | — | 2026-08-21 |
| q_fbeia_1_2026-07 | CLOSED | SCREEN-FAIL (informed-flow — no unconditional edge) | lab/analysis/q_fbeia_1_2026-07/CARD.md | lab/archive/q_fbeia_1_2026-07/ | — | 2026-08-03 |
| q_fccarry_1_2026-07 | CLOSED | SCREEN-FAIL (effect absent — carry-timing Sharpe ≈ 0) | lab/analysis/q_fccarry_1_2026-07/CARD.md | lab/archive/q_fccarry_1_2026-07/ | — | 2026-08-03 |
| q_funnel_1_2026-07 | CLOSED | RESOLVED — funnel-EV materially prefers 1.00× over ratified WATCH-1 0.50× on 2/4 horizon-robust trigger points | lab/analysis/q_funnel_1_2026-07/CARD.md | lab/archive/q_funnel_1_2026-07/ | — | 2026-08-03 |
| q_geofit_1_2026-07 | CLOSED | `AMBIGUOUS-PARAMETERIZATION` | lab/analysis/q_geofit_1_2026-07/CARD.md | lab/archive/q_geofit_1_2026-07/ | — | 2026-08-03 |
| q_inventory_1_2026-07 | FALSIFIED | `FALSIFIED` — the admissible band is empty at the cost of one bounded pass. | lab/analysis/q_inventory_1_2026-07/CARD.md | lab/archive/q_inventory_1_2026-07/ | — | 2026-07-20 |
| q_joint_tail_weekly_2026-07 | RETIRED | RETIRED — §9 panel-shape sanity gate failed at authoring time, before any CC handoff | lab/analysis/q_joint_tail_weekly_2026-07/CARD.md | lab/archive/q_joint_tail_weekly_2026-07/ | — | 2026-07-22 |
| q_kbudget_1_2026-07 | CLOSED | RESOLVED — ≥1 axis PASSES both frozen §D clauses; D5 (intraday-momentum footprint) ratified | lab/analysis/q_kbudget_1_2026-07/CARD.md | lab/archive/q_kbudget_1_2026-07/ | — | 2026-08-03 |
| q_nas_4_2026-06-20 | FALSIFIED | Strict gate FALSIFIED; a weak graded directional tendency survives but clears no honest correction at 0.05 | lab/analysis/q_nas_4_2026-06-20/CARD.md | lab/archive/q_nas_4_2026-06-20/ | — | 2026-07-12 |
| q_orbcush_1_2026-08 | FALSIFIED | FALSIFIED — trailing mean-R classifier vs ORB-MNQ-1's 2021-09-28 break; date-correlation clears 0/3 windows | lab/analysis/q_orbcush_1_2026-08/CARD.md | lab/archive/q_orbcush_1_2026-08/ | — | 2026-08-21 |
| q_pyrparity_1_2026-07 | FALSIFIED | `FALSIFIED-NONPROPORTIONAL` | lab/analysis/q_pyrparity_1_2026-07/CARD.md | lab/archive/q_pyrparity_1_2026-07/ | — | 2026-08-03 |
| q_znauc_1_2026-07 | CLOSED | SCREEN-FAIL (cost-wall — δ ≈ 1 bp vs 6–10 bp hurdle) | lab/analysis/q_znauc_1_2026-07/CARD.md | lab/archive/q_znauc_1_2026-07/ | — | 2026-08-03 |
| rates_ev_zf_recon_2026-07 | FALSIFIED | FALSIFIED at Phase-0 — P0.2 cost-law and P0.4 power both fail; no usable edge survives realistic cost | lab/analysis/rates_ev_zf_recon_2026-07/CARD.md | lab/archive/rates_ev_zf_recon_2026-07/ | — | 2026-08-03 |
| regime_aegis_2026-06-16 | FALSIFIED | FALSIFIED — USDJPY trend-persistence does not separate Aegis's win/loss regime at the per-trade level | lab/analysis/regime_aegis_2026-06-16/CARD.md | lab/archive/regime_aegis_2026-06-16/ | — | 2026-07-12 |
| regime_cond_2026-06-30 | FALSIFIED | Conditional regime probe falsified | lab/analysis/regime_cond_2026-06-30/CARD.md | lab/archive/regime_cond_2026-06-30/ | — | 2026-07-12 |
| regime_ratevol_2026-06-16 | FALSIFIED | FALSIFIED — exogenous US-Treasury rate volatility does not carry regime-hardness beyond the gold-anchored gate | lab/analysis/regime_ratevol_2026-06-16/CARD.md | lab/archive/regime_ratevol_2026-06-16/ | — | 2026-07-12 |
| regime_remc_2026-06-22 | FALSIFIED | FALSIFIED-T2b — primary VIX>20 / k=0.50 / lag-1 brake, stressed 43.4% of days | lab/analysis/regime_remc_2026-06-22/CARD.md | lab/archive/regime_remc_2026-06-22/ | — | 2026-07-11 |
| regime_signal_research_2026-06-25 | FALSIFIED | no candidate clears FWER with correct sign | lab/analysis/regime_signal_research_2026-06-25/CARD.md | lab/archive/regime_signal_research_2026-06-25/ | — | 2026-07-12 |
| slr_mym_phase05_2026-07-29 | FALSIFIED | FALSIFIED — Phase 0.5 event-rate bound; best S5+S3 day set 81 IS entries vs 120 floor; CLOSED at $0/0K | lab/analysis/slr_mym_phase05_2026-07-29/CARD.md | lab/archive/slr_mym_phase05_2026-07-29/ | — | 2026-08-03 |
| spx500_f09_gate_2026-06-20 | FALSIFIED | F09 gate CLOSED-FALSIFIED | lab/analysis/spx500_f09_gate_2026-06-20/CARD.md | lab/archive/spx500_f09_gate_2026-06-20/ | — | 2026-07-12 |
| striker_dj30_mym_prototype_2026-07 | FALSIFIED | Stage-1 NOT CLEARED (OOS holdout MISS) | lab/analysis/striker_dj30_mym_prototype_2026-07/CARD.md | lab/archive/striker_dj30_mym_prototype_2026-07/ | — | 2026-07-11 |
| timeframe_5m_2026-06-25 | CLOSED | NO-GO — 5m conversion degrades all four strategies; locked 15m timeframe is vindicated | lab/analysis/timeframe_5m_2026-06-25/CARD.md | lab/archive/timeframe_5m_2026-06-25/ | — | 2026-07-12 |
| tnec_envelope_compile_2026-08 | NULL | H_B = 0, STOP / NULL per PREREG F7 · closure: docs/briefs/closures/Q-TNEC-ENV-1-closure.md | lab/analysis/tnec_envelope_compile_2026-08/CARD.md | lab/archive/tnec_envelope_compile_2026-08/ | — | 2026-08-13 |
| todvol_1_2026-08-20 | FALSIFIED | D2 FAIL — mean signed gross +0.25pt vs 2.82pt bar (9% of required), n=975 | lab/analysis/todvol_1_2026-08-20/CARD.md | lab/archive/todvol_1_2026-08-20/ | — | 2026-08-21 |
| tom_spx | FALSIFIED | SPX500 turn-of-month Layer-A inference harness DEAD 2026-08-23 | lab/analysis/tom_spx/CARD.md | lab/archive/tom_spx/ | — | 2026-08-26 |
| tradeify_selectflex_remc_2026-07-10 | FALSIFIED | Tradeify Select Flex integer-micro re-MC gates fail under costs | lab/analysis/tradeify_selectflex_remc_2026-07-10/CARD.md | lab/archive/tradeify_selectflex_remc_2026-07-10/ | — | 2026-07-12 |
| transfer_expression_grid_2026-08 | FALSIFIED | FALSIFIED-at-walls — operator elected CLOSE on the H_A re-argument packet | lab/analysis/transfer_expression_grid_2026-08/CARD.md | lab/archive/transfer_expression_grid_2026-08/ | — | 2026-08-13 |
| usdcad_fade_2026-06-26 | FALSIFIED | the up-fade asymmetry is REAL but SUB-COST and REGIME-FRAGILE. | lab/analysis/usdcad_fade_2026-06-26/CARD.md | lab/archive/usdcad_fade_2026-06-26/ | — | 2026-07-11 |
| usdcad_ratemap_verify_2026-06-15 | CLOSED | DONE_WITH_CONCERNS — verification clean; one integration hazard surfaced | lab/analysis/usdcad_ratemap_verify_2026-06-15/CARD.md | lab/archive/usdcad_ratemap_verify_2026-06-15/ | — | 2026-07-11 |
| usdcad_rdm | CLOSED | PASS** — §6 return: `DONE_WITH_CONCERNS` | lab/analysis/usdcad_rdm/CARD.md | lab/archive/usdcad_rdm/ | — | 2026-07-11 |
| usdcad_reverse_2026-06-14 | FALSIFIED | no robust price-action strategy from this window. | lab/analysis/usdcad_reverse_2026-06-14/CARD.md | lab/archive/usdcad_reverse_2026-06-14/ | — | 2026-07-11 |
| usoil_rdm | FALSIFIED | edge-failure (+ venue/cost-constraint).** Falsified on all three | lab/analysis/usoil_rdm/CARD.md | lab/archive/usoil_rdm/ | — | 2026-07-12 |
| usoil_regime_capture | CLOSED | GSUB-1 SUBTRACT residual (Q-USOIL-1); Gen-1 harness NON-RUNNABLE | lab/analysis/usoil_regime_capture/CARD.md | lab/archive/usoil_regime_capture/ | — | 2026-08-09 |
| xindex_rv_recon_2026-07 | FALSIFIED | DROP (lean): selection dilutes edge; strictly dominated by incumbent ORB-MNQ. | lab/analysis/xindex_rv_recon_2026-07/CARD.md | lab/archive/xindex_rv_recon_2026-07/ | — | 2026-08-03 |
