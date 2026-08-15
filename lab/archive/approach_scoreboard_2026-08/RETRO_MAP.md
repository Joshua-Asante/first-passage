# Q-SCORE-1 — one-time lane retro-map (FROZEN)

**Status:** FROZEN · 2026-08-11 · one-time · never re-tuned
**Rule:** assign by the campaign's PRE-REGISTERED QUESTION (PREREG F5), never by outcome.
**Vocabulary:** PREREG F2 (closed set).
**Freeze SHA:** `99be1d8` (Task-2 PREREG commit)

## §Closures (`docs/briefs/closures/*.md`)

| closure file | campaign ID | pre-registered question (one line) | lane (F2) | verdict token (quoted) | machine Closed: (Y/N) | notes |
|---|---|---|---|---|---|---|
| 2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md | aegis-6j-stage1 | Aegis→6J prop reconstruction Stage-1 (H-SWEEP): do any cells clear hard filters? | reconstruction-self-funded | `FALSIFIED — H-SWEEP` | Y |  |
| 2026-07-16-aegis-6j-prop-reconstruction-stage2-hsolo-falsified.md | aegis-6j-stage2 | Aegis→6J Stage-2 H-SOLO: does winner panel clear both firms? | reconstruction-self-funded | `FALSIFIED — H-SOLO` | Y |  |
| 2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md | striker-mym-recon-1 | S-MYM-ORC-01 Striker→MYM reconstruction (session-calendar gate) | reconstruction-self-funded | `CLOSED-AMBIGUOUS` | Y |  |
| 2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md | striker-mym-recon-2 | Q-STRIKER-MYM-RECON-2 session-aware Striker→MYM reconstruction | reconstruction-self-funded | `CLOSED-FALSIFIED` | Y |  |
| 2026-07-27-hermes-agent-adoption-closure-resolved.md | hermes-agent-adoption | Hermes Agent adoption ruling (dispatch-environment falsifier) | governance-ops | `RESOLVED-NO-GO` | N | no F3 Closed: |
| GSUB-1-closure-resolved-loadbearing.md | GSUB-1 | First GRAND subtract pass — dispositions vs status quo | governance-ops | `RESOLVED-LOADBEARING` | Y |  |
| H-FBEIA-1-closure-screen-fail.md | H-FBEIA-1 | F-B: EIA CL unconditional event expression (harvest screen) | harvest-mechanism-first | `SCREEN-FAIL (informed-flow)` | Y |  |
| H-FCCARRY-1-closure-screen-fail.md | H-FCCARRY-1 | F-C: carry-timing δ on 6E/6J/CL (harvest screen) | harvest-mechanism-first | `SCREEN-FAIL (effect absent)` | Y |  |
| H-ZNAUC-1-closure-screen-fail.md | H-ZNAUC-1 | ZN post-auction unwind δ vs Req-5 cost law | harvest-mechanism-first | `SCREEN-FAIL (cost-wall)` | Y |  |
| MNQBASE-1-closure-intake-dry.md | MNQBASE-1 | Tradeify-shaped MNQ base-construct harvest — is intake well non-empty? | harvest-mechanism-first | `FALSIFIED` | N | Date: alias only; not F3 Closed: |
| MYM-3FPS-1-closure-falsified.md | MYM-3FPS-1 | Does native MYM reproduce published DJIA 3FPS effect at useful magnitude? | reconstruction-self-funded | `FALSIFIED at Phase-0` | Y |  |
| OPENPRESS-1-closure-falsified.md | OPENPRESS-1 | Opening-volume × directional-efficiency BAR EXPORT on MNQ/MYM | harvest-mechanism-first | `FALSIFIED` | Y |  |
| Q-6JCOMPOSE-1-closure-void-unexecutable.md | Q-6JCOMPOSE-1 | Can a 6J composed Class-S number be executed as frozen? | reconstruction-self-funded | `VOID` | N | no F3 Closed: |
| Q-6JCOMPOSE-2-closure-void-c2-red-gate-unreachable.md | Q-6JCOMPOSE-2 | 6J compose successor — is C2 gate reachable by construction? | reconstruction-self-funded | `VOID` | N | no F3 Closed: |
| Q-BOOKFIT-1-closure-resolved.md | Q-BOOKFIT-1 | Do three priced forks project inside the book-improving band? | governance-ops | `RESOLVED` | Y | book-geometry question, not approach exhaustion |
| Q-BUSTGATE-1-closure-falsified.md | Q-BUSTGATE-1 | Do eval-fee vs funded-upside economics ratify the 3.0% bust ceiling? | governance-ops | `FALSIFIED` | Y |  |
| Q-C1PANEL-1-closure-ambiguous.md | Q-C1PANEL-1 | c1 panel / re-MC structural premises (Phase-0) | governance-ops | `AMBIGUOUS` | Y |  |
| Q-CAPA-1-closure-resolved.md | Q-CAPA-1 | Cap seat / MNQ N14 tripwire persistence cell | governance-ops | `RESOLVED` | Y |  |
| Q-CAPALLOC-2-closure-resolved-fragile.md | Q-CAPALLOC-2 | Cap allocation geometry 51/29 vs standing 69/11 | governance-ops | `RESOLVED-FRAGILE` | Y |  |
| Q-COMPOSE-1-closure-falsified.md | Q-COMPOSE-1 | Does ORB third-leg breadth rescue Class-S book regime-fragility? | fifth-leg-domain | `FALSIFIED` | Y |  |
| Q-COSTGEO-1-closure-ambiguous.md | Q-COSTGEO-1 | Cost-geometry panel stamp / frozen-rule alignment (Phase-0) | governance-ops | `AMBIGUOUS-ALIGNMENT` | Y |  |
| Q-COSTGEO-2-closure-aborted.md | Q-COSTGEO-2 | Cost-geometry successor — verify §0 cost premise before pull | governance-ops | `ABORTED` | Y |  |
| Q-COSTGEO-3-closure-ambiguous-needs-depth.md | Q-COSTGEO-3 | Can level-1 depth bound cost of a 67-lot MYM add? | governance-ops | `AMBIGUOUS-NEEDS-DEPTH` | Y |  |
| Q-FUNNEL-1-closure-resolved.md | Q-FUNNEL-1 | Does contract-funnel EV vary materially across authorization rungs? | governance-ops | `RESOLVED` | Y |  |
| Q-GATECART-1-survivor-gate-cartography.md | Q-GATECART-1 | Is the survivor-gate realistic band non-empty at banked K? | discovery-blind-grid | `FALSIFIED — at the banked K = 3,177` | Y |  |
| Q-GEOFIT-1-closure-ambiguous-parameterization.md | Q-GEOFIT-1 | Trailing-DD funding-envelope profile family sufficiency | governance-ops | `AMBIGUOUS-PARAMETERIZATION` | Y |  |
| Q-HARV-0-month-end-rebalance-ES.md | Q-HARV-0 | Month-end ES-vs-ZN rebalance fade mechanism (HARV-2026-001) | harvest-mechanism-first | `AMBIGUOUS` | Y |  |
| Q-ICT-1-closure-moot.md | Q-ICT-1 | Is W/D-over-LTF advantage a best-of-4 selection artifact? | UNASSIGNED | `MOOT` | N | question does not fit F2 lane set |
| Q-ICT-CASCADE-1-closure-insufficient-n.md | Q-ICT-CASCADE-1 | ICT cascade end-to-end edge (binding 1M execution layer) | UNASSIGNED | `CLOSED` | Y | cascade thread not in F2 vocabulary |
| Q-INVENTORY-1-closure-falsified.md | Q-INVENTORY-1 | Zero-survivor replenishment — can one burst stage Req1–5 seeds? | harvest-mechanism-first | `FALSIFIED` | Y |  |
| Q-JOINT-TAIL-WEEKLY-closure-retired.md | Q-JOINT-TAIL-WEEKLY | Weekly joint-tail / 4-way co-failure at §9 panel-shape gate | UNASSIGNED | `RETIRED` | N | panel-shape joint-tail not in F2 |
| Q-KBUDGET-1-axis-reachability-screen.md | Q-KBUDGET-1 | Which discovery axes clear Clause-K + Clause-N reachability? | discovery-blind-grid | `RESOLVED` | N | no F3 Closed: |
| Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md | Q-KBUDGET-HARVEST-1 | Bounded literature harvest of axis rows for K-budget screen | discovery-blind-grid | `RESOLVED` | N | no F3 Closed: |
| Q-MCLTAS-1-closure-falsified.md | Q-MCLTAS-1 | TAS settlement δ-extraction probe (TNEC-ENV reopen path) | tnec-necessary-conditions | `FALSIFIED` | N | no F3 Closed: |
| Q-MNQDTL-CON-1-closure-falsified.md | Q-MNQDTL-CON-1 | Dense-1m EM construct catalogue Stage-G0 on MNQ | mnq-dense-1m-entry | `FALSIFIED` | Y | streak member |
| Q-MNQSEL-1-closure-falsified.md | Q-MNQSEL-1 | MNQ selection-value ceiling under EM1 (restart-clock universe) | mnq-dense-1m-entry | `FALSIFIED` | Y |  |
| Q-MNQSEL-2-closure-resolved.md | Q-MNQSEL-2 | Dense RTH 1m selection ceiling at G=10 | mnq-dense-1m-entry | `RESOLVED` | Y | capability-RESOLVED; does NOT reset streak (F4) |
| Q-OBJCOHERE-1-closure-falsified-coherent.md | Q-OBJCOHERE-1 | Do ratified objective instruments compose without contradiction? | governance-ops | `FALSIFIED-COHERENT` | Y |  |
| Q-OFCHAN-1-closure-void-coverage.md | Q-OFCHAN-1 | MNQ orderflow-channel Route-B Stage-G0 candidate coverage | mnq-dense-1m-entry | `VOID-COVERAGE` | Y | question is dense-1m Route-B coverage, not forced-flow census |
| Q-PYRPARITY-1-closure-falsified-nonproportional.md | Q-PYRPARITY-1 | Does WATCH-1 pyramid size scale proportionally with risk%? | governance-ops | `FALSIFIED-NONPROPORTIONAL` | Y |  |
| Q-R2AGRUN-1-closure-ambiguous-hold.md | Q-R2AGRUN-1 | MNQ aggressor-run-length Route-B Stage-G0 association | mnq-dense-1m-entry | `AMBIGUOUS-HOLD` | Y | streak member |
| Q-R2FLOW-1-closure-falsified.md | Q-R2FLOW-1 | MNQ signed-minute-flow Route-B Stage-G0 association | mnq-dense-1m-entry | `FALSIFIED` | Y | streak member |
| Q-R2VBUCK-1-closure-falsified.md | Q-R2VBUCK-1 | MNQ volume-bucket aggressor Route-B Stage-G0 association | mnq-dense-1m-entry | `FALSIFIED` | Y | streak member |
| Q-RAIL-1-closure-resolved.md | Q-RAIL-1 | c1 execution-rail GO/NO-GO decision packet (path + cost ceiling) | governance-ops | `RESOLVED` | Y |  |
| Q-TNEC-CON-2-closure-ambiguous-hold.md | Q-TNEC-CON-2 | Compression→expansion break construct on dense-1m MNQ | mnq-dense-1m-entry | `AMBIGUOUS-HOLD` | Y | streak member |
| Q-TNEC-CON-3-closure-ambiguous-hold.md | Q-TNEC-CON-3 | HTF-native compression break construct on dense-1m MNQ | mnq-dense-1m-entry | `AMBIGUOUS-HOLD` | N | Closed (explore record): non-F3; declared Lane corroborates |
| Q-TNEC-CON-4-closure-ambiguous-hold.md | Q-TNEC-CON-4 | PDH/PDL through-break construct on dense-1m MNQ | mnq-dense-1m-entry | `AMBIGUOUS-HOLD` | N | Closed (explore record): non-F3; declared Lane corroborates |
| Q-TNEC-CON-5-closure-ambiguous-hold.md | Q-TNEC-CON-5 | Impulse→pullback→VWAP-reclaim construct on dense-1m MNQ | mnq-dense-1m-entry | `AMBIGUOUS-HOLD` | N | Closed (explore record): non-F3; declared Lane corroborates |
| Q-TNEC-ENV-1-closure.md | Q-TNEC-ENV-1 | TNEC necessary-conditions envelope compile (H_B seed-grade cells) | tnec-necessary-conditions | `NULL` | N | no F3 Closed: |
| Q-TVCOV-1-closure-falsified.md | Q-TVCOV-1 | Is the 2022 TV trade-rate break a coverage artifact? | governance-ops | `CLOSED-FALSIFIED` | Y |  |
| Q-USOIL-1-closure-subtract.md | Q-USOIL-1 | USOIL/MCL instrument-lane intake (expired PARK → SUBTRACT) | governance-ops | `CLOSED` | N | Closed: PARKED… prose — not F3 date grammar |
| SLR-MYM-1-closure-falsified-stage0.md | SLR-MYM-1 | MYM liquidity sweep-and-reclaim Stage-0 scoping gates | harvest-mechanism-first | `FALSIFIED (as scoped)` | Y |  |
| ST-EH-1-closure-operator-stopped.md | ST-EH-1 | Supertrend ST(period,mult) flip-only 15m blind grid (NQ/YM/MNQ/MYM) | discovery-blind-grid | `OPERATOR-STOPPED` | N | no F3 Closed:; Status: closed YYYY-MM-DD prose |

## §Manifests (`discovery_manifests/*.json`)

| manifest | run_id | manifest.lane (raw, may be null) | mapped scoreboard lane (F2) | K executed | declared_K | status | notes |
|---|---|---|---|---|---|---|---|
| d5_nq_intraday_mom.json | d5_nq_intraday_mom | mechanism-first | harvest-mechanism-first | 1 | — | closed | raw lane mechanism-first |
| disccamp0_gc_2010_18.json | disccamp0_gc_2010_18 | — | discovery-blind-grid | 3177 | — | closed | DISC-CAMP-0 catch22/STUMPY/ruptures; no top-level lane |
| fb_eia_cl_reversal.json | fb_eia_cl_reversal | — | harvest-mechanism-first | 1 | — | closed | pairs with H-FBEIA-1; harvest screen not external-sourcing domain bar |
| fc_carry_6e6j6cl.json | fc_carry_6e6j6cl | — | harvest-mechanism-first | 1 | — | closed | pairs with H-FCCARRY-1 |
| h_od_1_es_overnight_drift.json | h_od_1_es_overnight_drift | mechanism-first | harvest-mechanism-first | 1 | — | closed | raw lane mechanism-first |
| harv2026_001_es_monthend.json | harv2026_001_es_monthend | — | harvest-mechanism-first | 1 | — | closed | pairs with Q-HARV-0 |
| mnqflow_depth_imbalance.json | mnqflow_depth_imbalance | — | forced-flow-census | 1 | — | closed | Avenue-A order-flow modality |
| mnqfvg_draw_probe.json | mnqfvg_draw_probe | — | mnq-dense-1m-entry | 1 | — | closed | MNQFVG-1 RTH entry mechanism probe |
| mnqpool_shield_probe.json | mnqpool_shield_probe | — | mnq-dense-1m-entry | 1 | — | closed | MNQPOOL-1 RTH entry mechanism probe |
| mnqsr1_structure_20260806.json | mnqsr1_structure_20260806 | — | UNASSIGNED | 14 | — | closed | S/R event study; not an F2 approach question |
| mnqsr1_structure_20260806b.json | mnqsr1_structure_20260806b | — | UNASSIGNED | 14 | — | closed | seed-fixed re-score of same 14-cell construct |
| orb_mnq_intraday_breakout.json | orb_mnq_intraday_breakout | mechanism-first | reconstruction-self-funded | 0 | 1 | closed | NAS100→MNQ ORB reconstruction; executed 0 vs declared 1 |
| st_eh_supertrend_grid.json | st_eh_supertrend_grid | — | discovery-blind-grid | 2 | 84 | closed | ST-EH: executed 2 vs declared 84 |

## §Differentials (F5 honesty)

| closure / manifest | question-based lane | outcome-based lane (counterfactual) | kept | why |
|---|---|---|---|---|
| Q-MNQSEL-2-closure-resolved.md | mnq-dense-1m-entry | leave-lane / "capability" pseudo-lane after RESOLVED | question-based | capability-RESOLVED does not reset streak (F4); same lane / yield does not reset |
| Q-OFCHAN-1 + Q-R2VBUCK/FLOW/AGRUN-1 | mnq-dense-1m-entry | forced-flow-census (orderflow words in outcome) | question-based | pre-registered questions are Route-B Stage-G0 on dense-1m MNQ entry thread |
| MNQBASE-1-closure-intake-dry.md | harvest-mechanism-first | mnq-dense-1m-entry (MNQ + later dense-1m thread) | question-based | question is Tradeify-shaped base-construct *harvest intake*, not dense-1m entry mechanism |
| Q-TNEC-ENV-1-closure.md | tnec-necessary-conditions | UNASSIGNED (NULL outcome) | question-based | envelope compile question stands; NULL is the answer, not the lane |
| Q-MCLTAS-1-closure-falsified.md | tnec-necessary-conditions | UNASSIGNED / governance-ops | question-based | TAS probe was the TNEC-ENV reopen path |
| ST-EH-1-closure-operator-stopped.md | discovery-blind-grid | governance-ops (operator stop) | question-based | question is the Supertrend blind grid; stop mode is disposition |
| Q-GATECART-1-survivor-gate-cartography.md | discovery-blind-grid | governance-ops (Cap/empty-gate residue) | question-based | question is survivor-gate cartography at banked K |
| Q-USOIL-1-closure-subtract.md | governance-ops | fifth-leg-domain (USOIL symbol) | question-based | question is instrument-lane intake / GSUB SUBTRACT, not a 5th-leg approach |
| H-FBEIA-1 / H-FCCARRY-1 / H-ZNAUC-1 | harvest-mechanism-first | fifth-leg-domain or external-sourcing (domain roll-up kin) | question-based | pre-registered as mechanism-first harvest screens |
| orb_mnq_intraday_breakout.json | reconstruction-self-funded | harvest-mechanism-first (raw manifest.lane) | question-based | prereg is NAS100→MNQ ORB reconstruction |

## §Coverage counts (link out; do not restate Task 5 arithmetic)

See BLOCK1_RESULTS.md.
