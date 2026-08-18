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

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| aegis1p_3leg_rescore_2026-07-27 | c1 | ACTIVE | Aegis@1.00% 3-leg corrected-geometry re-MC under Tradeify envelope | lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/ | — |
| band_quantization_2026-08-02 | c1 | ACTIVE | MNQ zero-floors at every FRIENDLY tier below 100K under the locked-proportional split; the two published 50K clearers... | lab/analysis/c1/band_quantization_2026-08-02/ | — |
| c1_band_rescore_2026-07-24 | c1 | ACTIVE | two Part A clearers at 50K band; RIDER FAIL stands a fortiori | lab/analysis/c1/c1_band_rescore_2026-07-24/ | — |
| c1_cadence_coverage_2026-08-03 | c1 | ACTIVE | 0.50× fails 16.0% of eval starts once overlapping pyramid holds are priced (critical scale 0.441×; 0.40× clean under ... | lab/analysis/c1/c1_cadence_coverage_2026-08-03/ | — |
| c1_cadence_inactivity_2026-08-02 | c1 | ACTIVE | token trade owed 82/312 Mon–Fri weeks (max 4 consecutive); 0.50× haircut raises inactivity exposure | lab/analysis/c1/c1_cadence_inactivity_2026-08-02/ | — |
| c1_cost_geometry_mym_add_2026-07-24 | c1 | ACTIVE | MYM add@67 TBBO cost geometry; D1 inside-sufficiency measured 0.0 | lab/analysis/c1/c1_cost_geometry_mym_add_2026-07-24/ | — |
| c1_liveness_diversification_2026-08-02 | c1 | ACTIVE | how much an added leg cuts dead weeks on the c1 book | lab/analysis/c1/c1_liveness_diversification_2026-08-02/ | — |
| c1_signal_identity_2026-07-28 | c1 | ACTIVE | full-panel MEASURED** (2026-07-29); Q-SIGID-1 §6 offline limb = **FULL** (plan `docs/superpowers/plans/2026-07-29-c1-... | lab/analysis/c1/c1_signal_identity_2026-07-28/ | — |
| c1_thirdleg_instrument_map_2026-07-27 | c1 | ACTIVE | Stage 1 discharges the contract-specs limb; Stage 2 measured sigma + tau_max for all four (RESULTS_stage2.md) | lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/ | — |
| catalogue_k_wall_2026-08-05 | c1 | ACTIVE | — | lab/analysis/c1/catalogue_k_wall_2026-08-05/ | — |
| cheap_falsifiers_2026-08 | c1 | HOLD | parent-side cheap falsifiers for the TNEC/dense-1m lane (spent; stay hot while CON-* cite them) | lab/analysis/c1/cheap_falsifiers_2026-08/ | — |
| class_s_c1_haircut_regime_remc_2026-07-16 | c1 | ACTIVE | lifecycle-haircut regime re-MC for Class-S candidate #1 | lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/ | — |
| class_s_candidate1_scoring_2026-07-15 | c1 | ACTIVE | G0–G8 scoring for Class-S candidate #1 (locked-book MYM+MNQ) | lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/ | — |
| eval_inverse_requirements_2026-08-03 | c1 | ACTIVE | max risk/trade is ~flat in trades/day ($275 at a 0.65R edge, k=1 through 4), so daily profit scales linearly with FRE... | lab/analysis/c1/eval_inverse_requirements_2026-08-03/ | — |
| eval_shape_diagnostics_2026-07-28 | c1 | ACTIVE | eval-shape diagnostics under corrected Tradeify geometry | lab/analysis/c1/eval_shape_diagnostics_2026-07-28/ | — |
| eval_slow_archetype_2026-08-04 | c1 | ACTIVE | — | lab/analysis/c1/eval_slow_archetype_2026-08-04/ | — |
| f3_cadence_successor_venues_2026-08-05 | c1 | ACTIVE | the cadence axis F3 required is measured, and **F3 is not decidable on it.** Bulenox and MFFU sit in the same inactiv... | lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/ | — |
| geofit_iid_sufficiency_power_2026-08-15 | c1 | HOLD | archive owed (CLOSED): scoping probe, follow-up to [`geofit_skew_probe_2026-07-25`](../../../archive/geofit_skew_prob... | lab/analysis/c1/geofit_iid_sufficiency_power_2026-08-15/ | — |
| geofit_skewed_family_construction_2026-08-15 | c1 | HOLD | archive owed (CLOSED): scoping construction, follow-up to [`geofit_skew_probe_2026-07-25`](../../../archive/geofit_sk... | lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/ | — |
| mnq_capflow_orb_r_2026-08 | c1 | HOLD | archive owed (FALSIFIED): `FALSIFIED` · **cap_spent:** `False` | lab/analysis/c1/mnq_capflow_orb_r_2026-08/ | — |
| mnq_event_ceiling_2026-08-04 | c1 | ACTIVE | — | lab/analysis/c1/mnq_event_ceiling_2026-08-04/ | — |
| mnq_ofchan_routeb_2026-08 | c1 | ACTIVE | — | lab/analysis/c1/mnq_ofchan_routeb_2026-08/ | — |
| mnq_orb_flow_substrate_2026-08-05 | c1 | ACTIVE | — | lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/ | — |
| mnq_orb_level_proximity_tod_2026-08-06 | c1 | ACTIVE | — | lab/analysis/c1/mnq_orb_level_proximity_tod_2026-08-06/ | — |
| mnq_r2agrun_routeb_2026-08 | c1 | HOLD | `AMBIGUOUS-HOLD` — empty candidate list (magnitude floor; G3 → **ITERATE**, not promote). | lab/analysis/c1/mnq_r2agrun_routeb_2026-08/ | — |
| mnq_selection_ceiling_allbars_2026-08 | c1 | ACTIVE | — | lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/ | — |
| mnq_sizediv_blind_2026-08 | c1 | ACTIVE | — | lab/analysis/c1/mnq_sizediv_blind_2026-08/ | — |
| mnq_stop_distribution_2026-08-02 | c1 | ACTIVE | MNQ stop distribution vs qty≥1 floor — Monday window realism | lab/analysis/c1/mnq_stop_distribution_2026-08-02/ | — |
| mnq_tnec_con2_compression_break_2026-08 | c1 | HOLD | `AMBIGUOUS-HOLD` — gross-positive / net-negative; halves sign-flip; non-promotable close. | lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/ | — |
| mnq_tnec_con3_htf_native_break_2026-08 | c1 | HOLD | `AMBIGUOUS-HOLD` — long mean net-positive but CI straddles 0; short net-negative; aux limbs fail live-pass. | lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/ | — |
| mnq_tnec_con4_pdh_pdl_break_2026-08 | c1 | HOLD | `AMBIGUOUS-HOLD` — both arms near-zero; CIs straddle 0; aux limbs fail live-pass. | lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/ | — |
| mnq_tnec_con5_impulse_pullback_vwap_2026-08 | c1 | HOLD | `AMBIGUOUS-HOLD` — both arms mean-negative; CIs straddle 0; aux limbs fail live-pass. | lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/ | — |
| msl_s2b_mym_2026-08 | c1 | HOLD | archive owed (STAGE-1 FAIL route): pre-G0 kill — [closure](../../../../docs/briefs/closures/MSL-S2B-closure-stage1-fa... | lab/analysis/c1/msl_s2b_mym_2026-08/ | — |
| parity_gen2_2026-08 | c1 | ACTIVE | — | lab/analysis/c1/parity_gen2_2026-08/ | — |
| q_evalseq_1_2026-08 | c1 | HOLD | archive owed (FALSIFIED): `FALSIFIED` — schedule lever spent for eval-pass lift (best −1.06pt vs +5pt bar); flat WATC... | lab/analysis/c1/q_evalseq_1_2026-08/ | — |
| q_polfront_1_2026-08 | c1 | ACTIVE | — | lab/analysis/c1/q_polfront_1_2026-08/ | — |
| q_rail_1_2026-07 | c1 | ACTIVE | c1 rail Phases 0–4 CLOSED RESOLVED; ceiling $700 operator-signed | lab/analysis/c1/q_rail_1_2026-07/ | — |
| tradeify_book_composition_2026-07-23 | c1 | ACTIVE | eval-lock fix + §2 book-composition re-derivation | lab/analysis/c1/tradeify_book_composition_2026-07-23/ | inputs gitignored |
| tradeify_eval_lock_correction_2026-07-22 | c1 | ACTIVE | Tradeify/MFFU eval drawdown-lock correction re-MC | lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/ | — |
| tradeify_fade_stage0_2026-07-30 | c1 | ACTIVE | Stage 0 instrumentation complete; Stage 1 region computed at 1x/2x/4x; no mechanism scored, K=0, $0 spend | lab/analysis/c1/tradeify_fade_stage0_2026-07-30/ | — |
| tradeify_futures3_bustcut_2026-07-11 | c1 | ACTIVE | Tradeify Select Flex 50K bust-cut Tests 1+2 | lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/ | — |
| tradeify_futures3_remc_2026-07-11 | c1 | ACTIVE | Tradeify Select Flex 3-leg futures remc panel | lab/analysis/c1/tradeify_futures3_remc_2026-07-11/ | — |
| tradeify_seed_target_spec_2026-08-04 | c1 | ACTIVE | at the ratified Part A gate the eval's binding constraint for a seed construct is the **weekly activity rule and noth... | lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/ | — |
| tvcov_2026-07 | c1 | ACTIVE | TV intraday bar-coverage census (Q-TVCOV-1) | lab/analysis/c1/tvcov_2026-07/ | — |
| venuegeo_dp3_bustceiling_2026-08-05 | c1 | ACTIVE | bust-ceiling half of DP3 measured; EV/$ half (pass-EV per eval-dollar) NOT run — each firm's evaluation-purchase pric... | lab/analysis/c1/venuegeo_dp3_bustceiling_2026-08-05/ | — |
| wstruct_cost_geometry_2026-07-28 | c1 | ACTIVE | corrects WSTRUCT-M2K-1 §2.2 on cost; asymmetric-payoff frontier is OPEN but harvest returns 0 seeds (modality-barred) | lab/analysis/c1/wstruct_cost_geometry_2026-07-28/ | — |

### striker

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| striker_mym_reconstruction_candidate1_2026-07 | striker | ACTIVE | S-MYM-ORC-02 development candidate (reconstruction TERMINAL lane) | lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/ | — |

### orb

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| d5_nq_intraday_mom_2026-07 | orb | ACTIVE | Baltussen H1 on NQ IS — Stage-2/4 results | lab/analysis/orb/d5_nq_intraday_mom_2026-07/ | — |
| eodadv_mnq_2026-08 | orb | ACTIVE | no pre-registered mechanism survives; 15:30 exit stays barred | lab/analysis/orb/eodadv_mnq_2026-08/ | — |
| orb_mnq_2026-07 | orb | ACTIVE | NAS100-ORB-30 on native MNQ; Stage-2 cost-law PASS then T2 payability FIRED | lab/analysis/orb/orb_mnq_2026-07/ | inputs gitignored |
| orb_universe_2026-06-22 | orb | ACTIVE | which FXIFY CFD best suits Opening Range Breakout | lab/analysis/orb/orb_universe_2026-06-22/ | pkl gitignored |
| sessconf_mnq_2026-08 | orb | ACTIVE | faithful close_tod session-truncation sweep (MNQ, Tradeify) | lab/analysis/orb/sessconf_mnq_2026-08/ | — |

### aegis

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| aegis_6j_prop_reconstruction_2026-07 | aegis | ACTIVE | Stage-1 FALSIFIED (operator accepted); Wave-1 sweep artifacts retained hot | lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/ | — |
| aegis_6j_trail_tradeify_2026-07-29 | aegis | ACTIVE | J4 re-run at true Tradeify Select 100K geometry (Aegis→6J v0.3) | lab/analysis/aegis/aegis_6j_trail_tradeify_2026-07-29/ | — |
| aegis_6j_transfer_2026-07-05 | aegis | ACTIVE | Bulenox Option-2 trail-survival MC sequence (Aegis→6J v0.3) | lab/analysis/aegis/aegis_6j_transfer_2026-07-05/ | inputs gitignored |

### regime

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| decompound_remc_2026-06-07 | regime | ACTIVE | decompounded full-history MC breaches both lock gates | lab/analysis/regime/decompound_remc_2026-06-07/ | inputs gitignored |
| q_ddtrig_1_2026-06-07 | regime | ACTIVE | dd_protection trigger re-MC on proposed de-risk bundle | lab/analysis/regime/q_ddtrig_1_2026-06-07/ | inputs gitignored |
| regime_fit_2026-06-17 | regime | ACTIVE | Q-REGIME-FIT-1 closure findings | lab/analysis/regime/regime_fit_2026-06-17/ | — |
| regime_oos_2026-06-21 | regime | ACTIVE | Phase-1 gold-gate face-validity (descriptive, unscored) | lab/analysis/regime/regime_oos_2026-06-21/ | — |
| regime_postcovid_2026-06-22 | regime | ACTIVE | post-COVID held-out regime probe | lab/analysis/regime/regime_postcovid_2026-06-22/ | — |
| regime_stress_2026-06-15 | regime | ACTIVE | regime-stress investigation chain | lab/analysis/regime/regime_stress_2026-06-15/ | — |
| regime_time_cost_2026-06-09 | regime | ACTIVE | Q-REGIME-TIME-1 RESOLVED-LARGE, but stagnation's recoverable cost is tail-risk/survivability, NOT speed; both LARGE c... | lab/analysis/regime/regime_time_cost_2026-06-09/ | — |

### harvest

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| disccamp0_gc_2010_18 | harvest | ACTIVE | DISC-CAMP-0 binding artifacts (Stage 2/3/5 staging) | lab/analysis/harvest/disccamp0_gc_2010_18/ | — |
| driftex_2026-08 | harvest | ACTIVE | drift exhaustion falsified; phenomenon is equity-index-specific | lab/analysis/harvest/driftex_2026-08/ | — |
| fts5_delete_falsifier_2026-07-27 | harvest | ACTIVE | FTS5-as-Delete falsifier harness results | lab/analysis/harvest/fts5_delete_falsifier_2026-07-27/ | — |
| h_od_1_es_overnight_drift_2026-07 | harvest | ACTIVE | SR917 overnight hour on ES IS — Stage-2/4 results | lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/ | — |
| harv_a4_footprint_2026-07 | harvest | ACTIVE | A4 month-end footprint diagnostic (Cursor return) | lab/analysis/harvest/harv_a4_footprint_2026-07/ | — |
| harvest_mechanism_deep_search_2026-07-23 | harvest | ACTIVE | harvest mechanism deep search fan-out (2026-07-23) | lab/analysis/harvest/harvest_mechanism_deep_search_2026-07-23/ | — |
| koijen_axis2_openalex_2026-08-17 | harvest | ACTIVE | Koijen Carry axis-2 OpenAlex substitute traversal — 6 screen-level leads survived, none Req-1a admitted | lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/ | — |
| limb_b_remeasure_2026-08 | harvest | ACTIVE | FTS5-as-Delete falsifier v3 (Limb B re-measurement) results | lab/analysis/harvest/limb_b_remeasure_2026-08/ | — |
| q_kbudget_harvest_1_2026-07 | harvest | ACTIVE | Phase-1 literature fan-out + Phase-2 K-budget ratification | lab/analysis/harvest/q_kbudget_harvest_1_2026-07/ | — |
| radar_tier_a_burst_2026-07 | harvest | ACTIVE | first burst EXECUTED; proceed items 1–3 complete (`H-TSMOM-6J` Clause-N FAIL; carry Table-1 moments recovered / timin... | lab/analysis/harvest/radar_tier_a_burst_2026-07/ | — |
| six_lead_cf_2026-08-17 | harvest | ACTIVE | P1/P2 CF FAIL all four legs; P3 dry-run $0 then CLOSED (calendar-spread SCREEN-FAIL); L3=L6 same-paper (6→5) | lab/analysis/harvest/six_lead_cf_2026-08-17/ | — |
| st_eh_2026-07 | harvest | ACTIVE | ST-EH campaign engine + fidelity harness (harvest) | lab/analysis/harvest/st_eh_2026-07/ | — |
| tnec_l2_sourcing_2026-08-10 | harvest | ACTIVE | TNEC L2 sourcing pass — R8 gold-fix δ-extracted SCREEN-FAIL (informed-flow + cost-law); C2/C3/C4 closed at 0 admissible | lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/ | — |

### mc

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| mc_mdd_closed_form_2026-08 | mc | ACTIVE | Magdon-Ismail (2004) closed-form G_D vs `simulate_path` absolute-$ trailing bust rates | lab/analysis/mc/mc_mdd_closed_form_2026-08/ | — |

### legacy

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| eurusd_pattern_enum | legacy | ACTIVE | EURUSD pattern-enumeration harness | lab/analysis/legacy/eurusd_pattern_enum/ | — |
| futures_conversion_2026-07-01 | legacy | ACTIVE | Phase A provisional MNQ/MYM granularity floors | lab/analysis/legacy/futures_conversion_2026-07-01/ | — |
| guardian_filter_sweep_2026-06-20 | legacy | ACTIVE | Guardian XAUUSD filter-validity sweep harness | lab/analysis/legacy/guardian_filter_sweep_2026-06-20/ | — |
| guardian_parity_2026-06-23 | legacy | ACTIVE | Guardian v5.5 parity port harness | lab/analysis/legacy/guardian_parity_2026-06-23/ | — |
| silver_be_off_2026-06-11 | legacy | ACTIVE | Silver BE-off reconcile + remc gate harness | lab/analysis/legacy/silver_be_off_2026-06-11/ | — |
| silver_counterbalance_2026-06-13 | legacy | ACTIVE | Silver counterbalance equity curve & required-hedge envelope | lab/analysis/legacy/silver_counterbalance_2026-06-13/ | — |
| silver_regime_2026-06-10 | legacy | ACTIVE | Guardian Silver v1.0 allocation frontier + regime stress | lab/analysis/legacy/silver_regime_2026-06-10/ | — |
| tom_spx | legacy | ACTIVE | SPX500 turn-of-month Layer-A inference harness | lab/analysis/legacy/tom_spx/ | — |
| us500_discovery_2026-06-22 | legacy | ACTIVE | US500 widest-net edge discovery results | lab/analysis/legacy/us500_discovery_2026-06-22/ | — |
| xauusd_cgb_2026-06-15 | legacy | HOLD | AMBIGUOUS (brief §6) / operational HOLD — build NOT triggered | lab/analysis/legacy/xauusd_cgb_2026-06-15/ | — |

### deep_lane

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| dl1_mgc_orc_2026-08-16 | deep_lane | HOLD | archive owed (CLOSED): `AMBIGUOUS` — ABANDONMENT (prereg roster mapping: confirm never read, nothing | lab/analysis/deep_lane/dl1_mgc_orc_2026-08-16/ | — |

### _inbox

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| dstruct_mnq_2026-08 | _inbox | ACTIVE | NULL: daily close-vs-EMA20 bias carries nothing at daily granularity (Tier-1 screen, 3 of 4 limbs failed; K=1 disclosed) | lab/analysis/_inbox/dstruct_mnq_2026-08/ | — |
| ict_mnq_2026-08 | _inbox | ACTIVE | ICT cascade re-run on NQ/MNQ at $0/K=0/Cap seat unspent: W and D confirm on independent instruments, pools falsified ... | lab/analysis/_inbox/ict_mnq_2026-08/ | — |
| q_condval_1_2026-08 | _inbox | HOLD | archive owed (FALSIFIED): `FALSIFIED` (S1b conditioner-engineering branch parked) | lab/analysis/_inbox/q_condval_1_2026-08/ | — |
| q_expr_1_2026-08 | _inbox | HOLD | archive owed (CLOSED): H1 horizon-mismatch 4/4 models the orphaning; H2 1/5 misses; H3 cannot fire | lab/analysis/_inbox/q_expr_1_2026-08/ | — |
| q_trainkill_1_2026-08 | _inbox | HOLD | BOUNDED extremes disagree; scored core MISCALIBRATED | lab/analysis/_inbox/q_trainkill_1_2026-08/ | — |
| q_trainkill_2_2026-08 | _inbox | HOLD | both named alternates fit (NEG and DEP-ZERO) | lab/analysis/_inbox/q_trainkill_2_2026-08/ | — |
| rangestate_corrected_2026-08 | _inbox | ACTIVE | OFFICIAL corrected-null re-score complete: S1a (GC) NULL (driving L2,L4; obs at 8.4th pct of its own linear-ACF band ... | lab/analysis/_inbox/rangestate_corrected_2026-08/ | — |
| rangestate_gc_2026-08 | _inbox | ACTIVE | NULL, now official under the corrected battery (driving L2+L4; obs at 8.4th pct of GC's own linear-ACF band — near-mi... | lab/analysis/_inbox/rangestate_gc_2026-08/ | — |
| rangestate_mcl_2026-08 | _inbox | ACTIVE | SIGNAL-GENERIC under the corrected battery (official 2026-08-18): canon-attributed volatility clustering (69th pct of... | lab/analysis/_inbox/rangestate_mcl_2026-08/ | — |

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
| external_sourcing_2026-06-30 | CLOSED | RESOLVED zero saved candidates (thesis-first narrow pass) | lab/analysis/external_sourcing_2026-06-30/CARD.md | lab/archive/external_sourcing_2026-06-30/ | — | 2026-07-12 |
| feed_divergence_2026-06 | CLOSED | RESOLVED-BY-RETIREMENT. Q-FEED-1's cross-feed transfer-validity question diss... | lab/analysis/feed_divergence_2026-06/CARD.md | lab/archive/feed_divergence_2026-06/ | — | 2026-08-03 |
| fixrev_costscreen_2026-06-22 | FALSIFIED | FAIL-COST** (best-of-grid break-even 0.277 pip vs FXIFY all-in 0.80 pip). | lab/analysis/fixrev_costscreen_2026-06-22/CARD.md | lab/archive/fixrev_costscreen_2026-06-22/ | — | 2026-07-11 |
| futures_prop_hold_compat_2026-06-30 | CLOSED | R6 NO-GO — futures-prop pivot closed | lab/analysis/futures_prop_hold_compat_2026-06-30/CARD.md | lab/archive/futures_prop_hold_compat_2026-06-30/ | — | 2026-07-12 |
| gbpusd_rank_cert | RETIRED | UNCERTIFIED — manual TV step never run; not carried (2026-07-10) | lab/analysis/gbpusd_rank_cert/CARD.md | lab/archive/gbpusd_rank_cert/ | — | 2026-07-12 |
| geofit_skew_probe_2026-07-25 | CLOSED | scoping probe. **Not** part of Q-GEOFIT-1, which is CLOSED `AMBIGUOUS-PARAMET... | lab/analysis/geofit_skew_probe_2026-07-25/CARD.md | lab/archive/geofit_skew_probe_2026-07-25/ | — | 2026-08-03 |
| guardian_decay_gate_2026-06-25 | CLOSED | DP-1…DP-7 resolved and the gate built, then dormant: no live Guardian venue, ... | lab/analysis/guardian_decay_gate_2026-06-25/CARD.md | lab/archive/guardian_decay_gate_2026-06-25/ | — | 2026-07-22 |
| guardian_silver_be_2026-06-10 | CLOSED | `DONE_WITH_CONCERNS` | lab/analysis/guardian_silver_be_2026-06-10/CARD.md | lab/archive/guardian_silver_be_2026-06-10/ | — | 2026-07-11 |
| harv_0_month_end_rebalance_es_2026-07 | CLOSED | H1 corroborated but placebo magnitude un-passable; successor pre-... | lab/analysis/harv_0_month_end_rebalance_es_2026-07/CARD.md | lab/archive/harv_0_month_end_rebalance_es_2026-07/ | — | 2026-07-12 |
| ict_cascade_2026-06-18 | CLOSED | Q-ICT-CASCADE-1 CLOSED (1M insufficient N) | lab/analysis/ict_cascade_2026-06-18/CARD.md | lab/archive/ict_cascade_2026-06-18/ | — | 2026-07-12 |
| ict_revcon_2026-06-19 | CLOSED | CLOSED NOT-CONFIRMED — 1H REVCON ambiguous / insufficient N | lab/analysis/ict_revcon_2026-06-19/CARD.md | lab/archive/ict_revcon_2026-06-19/ | — | 2026-07-12 |
| identify_nas100_2026-06-20 | CLOSED | Identify-only incomplete; stats JSON only — closed without Question phase | lab/analysis/identify_nas100_2026-06-20/CARD.md | lab/archive/identify_nas100_2026-06-20/ | — | 2026-07-12 |
| mnq_capa_n14_tripwire_2026-08-06 | CLOSED | `RESOLVED` (W5) — Cap seat **marked spent** on this Route A cell; companion r... | lab/analysis/mnq_capa_n14_tripwire_2026-08-06/CARD.md | lab/archive/mnq_capa_n14_tripwire_2026-08-06/ | — | 2026-08-13 |
| mnq_con1_dense1m_stage0_2026-08 | FALSIFIED | `FALSIFIED` — ES/NQ 5m divergence explore; both arms CI&lt;0; STOP catalogue | lab/analysis/mnq_con1_dense1m_stage0_2026-08/CARD.md | lab/archive/mnq_con1_dense1m_stage0_2026-08/ | — | 2026-08-13 |
| mnq_fvg_draw_probe_2026-08-04 | CLOSED | UNDERPOWERED — V5 fired (n=117 < 150), and the disclosure beneath the power f... | lab/analysis/mnq_fvg_draw_probe_2026-08-04/CARD.md | lab/archive/mnq_fvg_draw_probe_2026-08-04/ | — | 2026-08-13 |
| mnq_orb_level_proximity_2026-08-05 | CLOSED | VOID-TOD-CONFOUND (W6) — highest-precedence amended §7 gate; Δ not interprete... | lab/analysis/mnq_orb_level_proximity_2026-08-05/CARD.md | lab/archive/mnq_orb_level_proximity_2026-08-05/ | — | 2026-08-13 |
| mnq_orderflow_probe_2026-08-04 | FALSIFIED | V2 fired as pre-registered most likely: the observable book carries no | lab/analysis/mnq_orderflow_probe_2026-08-04/CARD.md | lab/archive/mnq_orderflow_probe_2026-08-04/ | — | 2026-08-13 |
| mnq_pool_shield_probe_2026-08-04 | FALSIFIED | V2 fired exactly as pre-registered most likely: mean net +0.017R/trade with t... | lab/analysis/mnq_pool_shield_probe_2026-08-04/CARD.md | lab/archive/mnq_pool_shield_probe_2026-08-04/ | — | 2026-08-13 |
| mnq_r2flow_routeb_2026-08 | FALSIFIED | `FALSIFIED` — empty candidate list (G3 → **STOP** for this G0 catalogue). | lab/analysis/mnq_r2flow_routeb_2026-08/CARD.md | lab/archive/mnq_r2flow_routeb_2026-08/ | — | 2026-08-13 |
| mnq_r2vbuck_routeb_2026-08 | FALSIFIED | `FALSIFIED` — empty candidate list (G3 → **STOP** for this G0 catalogue). | lab/analysis/mnq_r2vbuck_routeb_2026-08/CARD.md | lab/archive/mnq_r2vbuck_routeb_2026-08/ | — | 2026-08-13 |
| mnq_selection_ceiling_2026-08 | FALSIFIED | `FALSIFIED` (C2) — oracle top-1/day mean net R is **below** EM1 0.40 on | lab/analysis/mnq_selection_ceiling_2026-08/CARD.md | lab/archive/mnq_selection_ceiling_2026-08/ | — | 2026-08-13 |
| mnq_sr_structure_2026-08-06 | CLOSED | 0/14 BH-FDR survivors; Phase B/C not licensed. (Catalog stamp CLOSED = archiv... | lab/analysis/mnq_sr_structure_2026-08-06/CARD.md | lab/archive/mnq_sr_structure_2026-08-06/ | — | 2026-08-13 |
| msl_c1_mym_2026-08 | FALSIFIED | `FALSIFIED` | lab/analysis/msl_c1_mym_2026-08/CARD.md | lab/archive/msl_c1_mym_2026-08/ | — | 2026-08-13 |
| msl_c2_mgc_2026-08 | FALSIFIED | `FALSIFIED` | lab/analysis/msl_c2_mgc_2026-08/CARD.md | lab/archive/msl_c2_mgc_2026-08/ | — | 2026-08-13 |
| msl_c3_m2k_2026-08 | FALSIFIED | `FALSIFIED` — [closure](../../../../docs/briefs/closures/MSL-C3-K2-closure-fa... | lab/analysis/msl_c3_m2k_2026-08/CARD.md | lab/archive/msl_c3_m2k_2026-08/ | — | 2026-08-13 |
| msl_s2a_mcl_2026-08 | FALSIFIED | `FALSIFIED` (N-ACT: measured trades/week &lt; 1) | lab/analysis/msl_s2a_mcl_2026-08/CARD.md | lab/archive/msl_s2a_mcl_2026-08/ | — | 2026-08-13 |
| mym_3fps_recon_2026-07 | FALSIFIED | `FALSIFIED` | lab/analysis/mym_3fps_recon_2026-07/CARD.md | lab/archive/mym_3fps_recon_2026-07/ | — | 2026-08-03 |
| ng_eia_recon_2026-07 | FALSIFIED | FALSIFIED at Phase-0 (both P0.2 power and P0.3 cost-law fail decisively; per-... | lab/analysis/ng_eia_recon_2026-07/CARD.md | lab/archive/ng_eia_recon_2026-07/ | — | 2026-08-03 |
| noct_spx | FALSIFIED | FALSIFIED | lab/analysis/noct_spx/CARD.md | lab/archive/noct_spx/ | — | 2026-07-11 |
| oanda_stage1 | RETIRED | OANDA retired 2026-06-24; frozen historical evidence | lab/analysis/oanda_stage1/CARD.md | lab/archive/oanda_stage1/ | — | 2026-07-12 |
| oil_carry | FALSIFIED | F1-FALSIFIED — rejected candidate | lab/analysis/oil_carry/CARD.md | lab/archive/oil_carry/ | — | 2026-07-12 |
| opening_pressure_map_2026-07 | FALSIFIED | `FALSIFIED` | lab/analysis/opening_pressure_map_2026-07/CARD.md | lab/archive/opening_pressure_map_2026-07/ | — | 2026-08-03 |
| orb_zb_recon_2026-07 | FALSIFIED | FALSIFIED at Phase-0 (P0.1 cost-law KILL on every window; the ORB breakout ha... | lab/analysis/orb_zb_recon_2026-07/CARD.md | lab/archive/orb_zb_recon_2026-07/ | — | 2026-08-03 |
| p2_replay_2026-07 | FALSIFIED | P2 FALSIFIED for this venue — both legs K2-kill | lab/analysis/p2_replay_2026-07/CARD.md | lab/archive/p2_replay_2026-07/ | — | 2026-07-12 |
| pharos_us500_sweepfvg | FALSIFIED | FALSIFIED (2026-06-17)** — directional signal is | lab/analysis/pharos_us500_sweepfvg/CARD.md | lab/archive/pharos_us500_sweepfvg/ | — | 2026-07-12 |
| q_bookfit_1_2026-07 | CLOSED | RESOLVED (3/3 forks PASS: `ρ < 1.0` AND `n_eff_risk_delta > 0` @ 0.37%). Cano... | lab/analysis/q_bookfit_1_2026-07/CARD.md | lab/archive/q_bookfit_1_2026-07/ | — | 2026-08-03 |
| q_compose_1_2026-07 | FALSIFIED | `FALSIFIED` (§6 row 2 — both limbs, every tier) | lab/analysis/q_compose_1_2026-07/CARD.md | lab/archive/q_compose_1_2026-07/ | — | 2026-07-20 |
| q_decay_1_2026-07-10 | CLOSED | SCOPE-SPLIT — Guardian-only coverage; rest UNCOVERED | lab/analysis/q_decay_1_2026-07-10/CARD.md | lab/archive/q_decay_1_2026-07-10/ | — | 2026-07-12 |
| q_fbeia_1_2026-07 | CLOSED | SCREEN-FAIL (informed-flow — no unconditional edge). Canonical closure: [`doc... | lab/analysis/q_fbeia_1_2026-07/CARD.md | lab/archive/q_fbeia_1_2026-07/ | — | 2026-08-03 |
| q_fccarry_1_2026-07 | CLOSED | SCREEN-FAIL (effect absent — carry-timing Sharpe ≈ 0). Canonical closure: [`d... | lab/analysis/q_fccarry_1_2026-07/CARD.md | lab/archive/q_fccarry_1_2026-07/ | — | 2026-08-03 |
| q_funnel_1_2026-07 | CLOSED | RESOLVED (funnel-EV materially prefers 1.00x over ratified WATCH-1 0.50x on 2... | lab/analysis/q_funnel_1_2026-07/CARD.md | lab/archive/q_funnel_1_2026-07/ | — | 2026-08-03 |
| q_geofit_1_2026-07 | CLOSED | `AMBIGUOUS-PARAMETERIZATION` | lab/analysis/q_geofit_1_2026-07/CARD.md | lab/archive/q_geofit_1_2026-07/ | — | 2026-08-03 |
| q_inventory_1_2026-07 | FALSIFIED | `FALSIFIED` — the admissible band is empty at the cost of one bounded pass. | lab/analysis/q_inventory_1_2026-07/CARD.md | lab/archive/q_inventory_1_2026-07/ | — | 2026-07-20 |
| q_joint_tail_weekly_2026-07 | RETIRED | §9 panel-shape sanity gate FAILED at authoring time, before any CC handoff. C... | lab/analysis/q_joint_tail_weekly_2026-07/CARD.md | lab/archive/q_joint_tail_weekly_2026-07/ | — | 2026-07-22 |
| q_kbudget_1_2026-07 | CLOSED | `RESOLVED`** (frozen pre-reg §D: ≥1 axis PASSES both clauses) — flipped 2026-... | lab/analysis/q_kbudget_1_2026-07/CARD.md | lab/archive/q_kbudget_1_2026-07/ | — | 2026-08-03 |
| q_nas_4_2026-06-20 | FALSIFIED | PARTIAL** — strict gate **FALSIFIED**; a weak graded directional tendency s... | lab/analysis/q_nas_4_2026-06-20/CARD.md | lab/archive/q_nas_4_2026-06-20/ | — | 2026-07-12 |
| q_pyrparity_1_2026-07 | FALSIFIED | `FALSIFIED-NONPROPORTIONAL` | lab/analysis/q_pyrparity_1_2026-07/CARD.md | lab/archive/q_pyrparity_1_2026-07/ | — | 2026-08-03 |
| q_znauc_1_2026-07 | CLOSED | SCREEN-FAIL (cost-wall — δ ≈ 1 bp vs 6–10 bp hurdle). Canonical closure: [`do... | lab/analysis/q_znauc_1_2026-07/CARD.md | lab/archive/q_znauc_1_2026-07/ | — | 2026-08-03 |
| rates_ev_zf_recon_2026-07 | FALSIFIED | FALSIFIED at Phase-0 (P0.2 cost-law + P0.4 power both fail; the instrument-ch... | lab/analysis/rates_ev_zf_recon_2026-07/CARD.md | lab/archive/rates_ev_zf_recon_2026-07/ | — | 2026-08-03 |
| regime_aegis_2026-06-16 | FALSIFIED | FALSIFIED.** USDJPY trend-persistence does not separate Aegis's win/loss regi... | lab/analysis/regime_aegis_2026-06-16/CARD.md | lab/archive/regime_aegis_2026-06-16/ | — | 2026-07-12 |
| regime_cond_2026-06-30 | FALSIFIED | Conditional regime probe falsified | lab/analysis/regime_cond_2026-06-30/CARD.md | lab/archive/regime_cond_2026-06-30/ | — | 2026-07-12 |
| regime_ratevol_2026-06-16 | FALSIFIED | FALSIFIED.** Exogenous US-Treasury rate volatility does **not** carry regime-... | lab/analysis/regime_ratevol_2026-06-16/CARD.md | lab/archive/regime_ratevol_2026-06-16/ | — | 2026-07-12 |
| regime_remc_2026-06-22 | FALSIFIED | T2b** — primary VIX>20 / k=0.50 / lag-1 brake, stressed 43.4% of days. Pre-re... | lab/analysis/regime_remc_2026-06-22/CARD.md | lab/archive/regime_remc_2026-06-22/ | — | 2026-07-11 |
| regime_signal_research_2026-06-25 | FALSIFIED | no candidate clears FWER with correct sign | lab/analysis/regime_signal_research_2026-06-25/CARD.md | lab/archive/regime_signal_research_2026-06-25/ | — | 2026-07-12 |
| slr_mym_phase05_2026-07-29 | FALSIFIED | SLR-MYM-1 Phase 0.5 free event-rate bound (15m upper-bound proxy) — entry 17.... | lab/analysis/slr_mym_phase05_2026-07-29/CARD.md | lab/archive/slr_mym_phase05_2026-07-29/ | — | 2026-08-03 |
| spx500_f09_gate_2026-06-20 | FALSIFIED | F09 gate CLOSED-FALSIFIED | lab/analysis/spx500_f09_gate_2026-06-20/CARD.md | lab/archive/spx500_f09_gate_2026-06-20/ | — | 2026-07-12 |
| striker_dj30_mym_prototype_2026-07 | FALSIFIED | Stage-1 NOT CLEARED (OOS holdout MISS) | lab/analysis/striker_dj30_mym_prototype_2026-07/CARD.md | lab/archive/striker_dj30_mym_prototype_2026-07/ | — | 2026-07-11 |
| timeframe_5m_2026-06-25 | CLOSED | NO-GO — 5m conversion degrades all four strategies. Original: NO-GO. The 5m c... | lab/analysis/timeframe_5m_2026-06-25/CARD.md | lab/archive/timeframe_5m_2026-06-25/ | — | 2026-07-12 |
| tnec_envelope_compile_2026-08 | NULL | H_B = 0, STOP / NULL per PREREG F7 · closure: docs/briefs/closures/Q-TNEC-ENV-1-closure.md | lab/analysis/tnec_envelope_compile_2026-08/CARD.md | lab/archive/tnec_envelope_compile_2026-08/ | — | 2026-08-13 |
| tradeify_selectflex_remc_2026-07-10 | FALSIFIED | Tradeify Select Flex integer-micro re-MC gates fail under costs | lab/analysis/tradeify_selectflex_remc_2026-07-10/CARD.md | lab/archive/tradeify_selectflex_remc_2026-07-10/ | — | 2026-07-12 |
| transfer_expression_grid_2026-08 | FALSIFIED | `CLOSED — FALSIFIED-at-walls` · operator elected **(A) CLOSE** on the H_A re-... | lab/analysis/transfer_expression_grid_2026-08/CARD.md | lab/archive/transfer_expression_grid_2026-08/ | — | 2026-08-13 |
| usdcad_fade_2026-06-26 | FALSIFIED | the up-fade asymmetry is REAL but SUB-COST and REGIME-FRAGILE. | lab/analysis/usdcad_fade_2026-06-26/CARD.md | lab/archive/usdcad_fade_2026-06-26/ | — | 2026-07-11 |
| usdcad_ratemap_verify_2026-06-15 | CLOSED | `DONE_WITH_CONCERNS` (verification clean; one integration hazard surfaced — s... | lab/analysis/usdcad_ratemap_verify_2026-06-15/CARD.md | lab/archive/usdcad_ratemap_verify_2026-06-15/ | — | 2026-07-11 |
| usdcad_rdm | CLOSED | PASS** — §6 return: `DONE_WITH_CONCERNS` | lab/analysis/usdcad_rdm/CARD.md | lab/archive/usdcad_rdm/ | — | 2026-07-11 |
| usdcad_reverse_2026-06-14 | FALSIFIED | no robust price-action strategy from this window. | lab/analysis/usdcad_reverse_2026-06-14/CARD.md | lab/archive/usdcad_reverse_2026-06-14/ | — | 2026-07-11 |
| usoil_rdm | FALSIFIED | edge-failure (+ venue/cost-constraint).** Falsified on all three | lab/analysis/usoil_rdm/CARD.md | lab/archive/usoil_rdm/ | — | 2026-07-12 |
| usoil_regime_capture | CLOSED | GSUB-1 SUBTRACT residual (Q-USOIL-1); Gen-1 harness NON-RUNNABLE | lab/analysis/usoil_regime_capture/CARD.md | lab/archive/usoil_regime_capture/ | — | 2026-08-09 |
| xindex_rv_recon_2026-07 | FALSIFIED | DROP (lean): selection dilutes edge; strictly dominated by incumbent ORB-MNQ. | lab/analysis/xindex_rv_recon_2026-07/CARD.md | lab/archive/xindex_rv_recon_2026-07/ | — | 2026-08-03 |
