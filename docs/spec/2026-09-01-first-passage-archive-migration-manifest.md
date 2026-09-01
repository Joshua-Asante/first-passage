# Migration manifest — first-passage-archive Levels 1–3

Companion to [`2026-09-01-first-passage-archive-migration-spec.md`](2026-09-01-first-passage-archive-migration-spec.md).
Codex review on PR #252 (finding: "Check in the complete migration manifest") — the spec
referenced a survey that was never committed. This is that survey, persisted, at cluster
granularity: every row below is a directory/glob whose files share one migration fate, not a
hand-typed 1,500-line list that would go stale the moment anything in the tree changes.

**How to use this file:** before opening any deletion PR for a cluster, re-run that cluster's
verification command. A cluster whose command returns non-empty output (a live citer) is NOT
safe to move as originally classified — stop and re-triage that specific cluster, do not
override the check. This file is authoritative for *what* to move; the commands are
authoritative for *whether it's still true*.

---

## Level 1 — zero citations, move first (~213 files)

| Cluster | Files | Verify-clean command |
|---|---:|---|
| `lab/analysis/legacy/` (whole dir) | 20 | `git grep -l "legacy/" -- ':!lab/analysis/legacy/' ':!docs/**'` (expect: no hits naming a specific slug under it as a live dependency) |
| `lab/archive/{approach_scoreboard_2026-08,external_sourcing_2026-06-30,futures_prop_hold_compat_2026-06-30,gbpusd_rank_cert,geofit_skew_probe_2026-07-25,guardian_decay_gate_2026-06-25,guardian_silver_be_2026-06-10,identify_nas100_2026-06-20,orbmnq1_survivor_scoring_2026-08-20,p2_replay_2026-07,q_bookfit_1_2026-07,q_decay_1_2026-07-10,q_evalseq_1_2026-08,q_expr_1_2026-08,q_geofit_1_2026-07,q_joint_tail_weekly_2026-07,regime_cond_2026-06-30,regime_remc_2026-06-22,regime_signal_research_2026-06-25,timeframe_5m_2026-06-25}` (20 campaigns) | 130 | per-slug: `git grep -l "<slug>" -- ':!lab/archive/<slug>/' ':!lab/CATALOG.md'` (expect: empty) |
| `docs/briefs/handoffs/` (whole dir) | 33 | `git grep -rl "docs/briefs/handoffs/" -- ':!docs/briefs/handoffs/'` (expect: empty or only "template lineage" mentions) |
| `docs/historical/` (whole dir) | 4 | README self-declares "Not live doctrine" — `git grep -l "docs/historical/" -- ':!docs/historical/'` (expect: empty) |
| `docs/analytics/` (whole dir, incl. PNGs) | 7 | README self-declares "Historical record only" — live owner is `docs/mc_anchor_history.md`, unaffected |
| `docs/lessons/` (whole dir) | 3 | README redirects to `docs/methodology/lessons/`; both content files still `Status: CANDIDATE` |
| `docs/methodology/archive/` (whole dir) | 5 | README self-declares "frozen Notion ports... not a second methodology roster" |
| `docs/ltm/notes/archive/sessions/SESSIONS-2026-Q3.md`, `docs/ltm/notes/archive/state/STATE-decision-index-pre-2026-08-23.md` | 2 | Already-rolled, already search-excluded snapshots per `docs/ltm/README.md` |
| `docs/external/fxify_swap_rates_2026-05-25.md` | 1 | CFD estate confirmed retired (CLAUDE.md decision table) |

## Level 2 — closed-decision graveyard, per-cluster spot-check before deletion (~687 files)

| Cluster | Files | Excludes (do NOT move) | Verify command |
|---|---:|---|---|
| `docs/briefs/closures/` | 84 | 18 files cited from `docs/rejected_candidates.md` by Q-ID: Q-BOOKFIT-1, Q-CAPFLOW-1, Q-COMPOSE-1, Q-GATECART-1, Q-INVENTORY-1, Q-MCLTAS-1, Q-MNQDTL-CON-1, Q-MNQSEL-1, Q-MNQSEL-2, Q-ORBPOS-1, Q-PYRPARITY-1, Q-R2FLOW-1, Q-R2VBUCK-1, Q-RAIL-1, Q-TNEC-CON-5, Q-TOM-SPX-1, Q-TVCOV-1, Q-TXG-1 | `for f in docs/briefs/closures/*.md; do id=$(basename "$f" | grep -oE 'Q-[A-Z0-9-]+-[0-9]+'); grep -q "$id" docs/rejected_candidates.md && echo "EXCLUDE: $f"; done` |
| `docs/briefs/*.md` (loose root, closed subset) | 64 | Q-SIGID-1 (OPEN), Q-FILLTAX-1 (OPEN), Q-VOLREGIME-1 (OPEN), Q-FUNDPOL-1 (DORMANT-renewed), Q-GATECAL-1 (self-declared OPEN, post-08-29), Q-VENUEGEO-1 (self-declared OPEN) | `grep -A2 "^| Q-" docs/briefs/INDEX.md` — cross-check every candidate against the Open/Dormant tables before moving |
| `docs/briefs/rnd-pipeline/` (scoping + handoff subset) | 30 | Q-SESSCONF-1 (only OPEN item), `closures/Q-FVGFLOW-1-closure-ambiguous.md` (is itself the stub, stays) | Per-file `**Status:**` header check |
| `docs/spec/` closed retirement + build specs (21 named files — dukascopy×2, oanda×2, nas100-orb-filters×2, session-log-rolloff-design, trade-capture-skill-design, codifier-breakout-longshort-trailing-extension, CC-HANDOFF-monorepo-boundaries, wfo-runner-v0×4, third-leg-target-spec, tradeify-activity-rule-disposition-spec, mnq-daily-cadence-tight-daily-loss-target-spec, mnqprox-2-tod-matched-level-proximity-spec, PREREG-NAS-ECR-1-live-edge-capture, issue_54_survey_brief, pine_baseline_csv_format) | 21 | none identified | Each carries an explicit terminal status line — grep `RETIRED\|CLOSED\|SCOPE DEAD\|PARKED` per file |
| `docs/notes/audits/` (root 28 + `programme-audit/` 27 + adr-corpus/brief-corpus decay audits 2) | 57 | `rule-2-trip-log.md` (live falsifier-of-record), `sentinel-gate-audit.md` (live), `docs-runtime-inventory.md` (script-regenerated), `README.md` (nav) | `grep -l "live falsifier\|do not hand-edit\|do not write here except quarterly" docs/notes/audits/*.md` → those 3 stay |
| `docs/notes/research/` (8 of 9) | 8 | `2026-08-24-phase-b-lane-b1-paper-log-tracker.md` (live, still-appended) | Filename check |
| `docs/superpowers/plans/` shipped bulk | 24 | 8 AWAITING-GO / DRAFT / in-progress files (2026-08-23-disaster-stop-*, viable-strategy-phase-{a,b,c,d}/sequence-overview, macro-regime-barometer-campaign-overview, 2026-08-31-q-volregime-next-step, 2026-09-01-mnq-pine-vet-*, 2026-08-23-tradable-anomalies-t4) | `grep -l "AWAITING GO\|DRAFT ·\|Status: DRAFT" docs/superpowers/plans/*.md` |
| `lab/analysis/harvest/` closed subset | 46 of 55 | `driftex_2026-08/` (R1-cited by `rejected_candidates.md`), `radar_tier_a_burst_2026-07/` ("not an archiveable close" per its own README), `harv_a4_footprint_2026-07/` (unclear terminal status — low confidence, needs a closer read, do not move on this pass) | `grep -l "driftex_2026-08\|radar_tier_a_burst" docs/rejected_candidates.md docs/notes/**/*.md` |
| `lab/analysis/_inbox/` closed subset (`ict_1mexec_1_2026-08`, `ict_mnq_2026-08`, `q_trainkill_{1,2,3}_2026-08`, `rangestate_{corrected,gc,mcl}_2026-08`, `rangecond_1_2026-08-30`, `rangexfer_{byyear_l4,presence_battery}_2026-08-30`) | ~65 | `b2_london_fix_wake_2026-08-24/` (R1, cited by `rejected_candidates.md`), `joint_surrogation_null_2026-08-30/`, `mnq_dailygeom_notice_2026-08-29/`, `mym_mechanism_harvest_2026-08-29/`, `volregime_byyear_l4_2026-08-31/`, `volregime_l3_2026-08-31/`, `volregime_l5_design_2026-08-31/`, `volregime_l5_pilot_2026-08-31/` — all feed the OPEN Q-VOLREGIME-1 | `grep -rn "harness_disposition_ref\|BOUNDED_ROUND_PLAN" docs/rejected_candidates.md docs/briefs/INDEX.md` |
| `lab/analysis/c1/` closed clusters (19 named tradeify/eval-geometry dirs + 8 TNEC/dense-1m dirs + 9 MNQ selection/orb-flow dirs + 6 ORB-MNQ-1 cushion/skew dirs + `aegis1p_3leg_rescore_2026-07-27` + `aegis_orbmnq_combined_book_2026-08-26` + `msl_s2b_mym_2026-08` + `msl_s4_mgc_2026-08` + `tvcov_2026-07` + `q_rail_1_2026-07`) | ~296 of 381 | Q-SIGID-1's dir (`c1_signal_identity_2026-07-28/`), Q-FILLTAX-1's dir (`parity_gen2_2026-08/`), `msl_monsurf_1_idle_clock_2026-08/` (live monitoring code), `class_s_c1_haircut_regime_remc_2026-07-16/` + `firm_model_repair_r1_7tier_2026-08-23/` (CLAUDE.md-cited canonical figures), `geofit_iid_sufficiency_power_2026-08-15/` + `geofit_skewed_family_construction_2026-08-15/` + `aegis3leg_engine_param_2026-08-20/` + `class_s_candidate1_scoring_2026-07-15/` (code dependency chain of the above two), `shape_feasibility_map_2026-08/` + `a2_panel_noise_venue_bound_2026-08-24/` (STATE.md-cited open decision basis) | Full per-slug re-check against `docs/briefs/INDEX.md` + `STATE.md` — this cluster has the highest exclusion density of the survey, re-verify every slug, do not batch-assume |

## Level 3 — needs engineering before it can move (~607 files)

| Cluster | Files | Precondition | Verify command |
|---|---:|---|---|
| `docs/briefs/pre-registration/` spent pairs | 82 | Excludes: `Q-SIGID-1-`, `Q-FILLTAX-1-`, `Q-VOLREGIME-1-`, `Q-FUNDPOL-1-`, `Q-GATECAL-1-verdict-preregistration.md` (4-5 files). Each remaining pre-reg must be paired 1:1 against a `closures/` file or a `lab/CATALOG.md` CLOSED row before moving — not individually re-verified by the original survey, sampling only. | `for f in docs/briefs/pre-registration/*.md; do slug=$(basename "$f" -verdict-preregistration.md); ls docs/briefs/closures/*"$slug"* 2>/dev/null || echo "UNPAIRED: $f"; done` |
| `docs/notes/notice/` | 36 | Medium confidence — 11 of 37 files dated 2026-08-29, feeding the still-open regime-awareness forward item. Re-read `docs/briefs/INDEX.md`'s Q-VOLREGIME-1 row immediately before moving any 08-29-dated file. | `grep -l "2026-08-29" docs/notes/notice/*.md` — re-triage each hit individually |
| The 56 cited `lab/archive/` campaigns (the remainder of `lab/archive/`'s 91 total, excluding the 20 already in Level 1) | 488 | **Blocked on Phase 3 of the spec** (link-rewrite pass) — every citer in `ops/instruments/*.md` and `docs/rejected_candidates.md` must be enumerated and repointed in the same PR as the deletion, not after. | `for slug in lab/archive/*/; do s=$(basename "$slug"); git grep -l "$s" -- 'ops/instruments/*.md' 'docs/rejected_candidates.md'; done` — this command IS the enumeration Codex asked for; run it fresh, do not reuse survey-era counts |
| `docs/governance/notion-redirect-map.md` | 1 | Low confidence — self-declares "the read authority" for dereferencing old `[LEGACY-NOTION]` tags that may still appear in memory/briefs. Confirm nothing currently resolves through it before moving. | `grep -rl "LEGACY-NOTION" --include=*.md .` |

---

## What stays public regardless of level (do not move under any circumstance)

`docs/adr/` (audited 3× independently, near-zero dormant — see `docs/notes/audits/programme-audit/2026-08-31-adr-corpus-audit.md`); `docs/pursuits/` (the GRAND-tier register itself); `docs/methodology/` (minus `archive/`); `docs/templates/`; `lab/analysis/{orb,regime,aegis,mc,striker}/`; `lab/analysis/c1/`'s excluded slugs above; `docs/notes/rail_build/`, `sentinel/`, `autonomy_staging/`; the live intake-gate spec family in `docs/spec/` (TNEC-1, dense-1m, MSL charter, loop-s* index); `ops/ core/ tests/ scripts/ discovery_manifests/ deploy/ .claude/ .cursor/`.

---

## Provenance

Derived from a 9-agent parallel survey run 2026-09-01 (Workflow `wf_056c1b94-efd`) plus a follow-up
citation-chain audit (`wf_a084527c-900` covers ADR-corpus overlap only, not this manifest). Counts are
survey-era; **the verify commands in each row are the source of truth going forward, not the counts.**
