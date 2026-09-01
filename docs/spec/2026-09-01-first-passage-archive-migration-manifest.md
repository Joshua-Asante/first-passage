# Migration manifest v2 — code-level verified

**Supersedes the original (v1) manifest**, which classified candidates by doc citation only.
Companion to [`2026-09-01-first-passage-archive-migration-spec.md`](2026-09-01-first-passage-archive-migration-spec.md).

**Why this version exists:** Codex's PR #252 review found two of v1's "safest, zero-citation"
items (`lab/analysis/legacy/`, `docs/analytics/mc_anchor_evolution/`) had live CODE dependencies
a doc-only grep completely missed. This version re-checked every candidate against four surfaces —
doc/ADR/brief citations, CODE dependencies (imports/`sys.path`/dynamic `importlib` loads/direct
file reads across `core/ ops/ lab/ tests/ scripts/`), `.claude/skills/**/*.md` references, and
`lab/CATALOG.md` status — via 21 parallel agents, 490 tool calls, verified 2026-09-01
(Workflow `wf_ce66f55a-f3a`; full per-item evidence in that run's `journal.jsonl`).

**Result: of 650 items checked, 228 (35%) are confirmed safe — 487 tracked files.** The rest split:
150 have live code dependencies, 135 have live doc citations that survived closer scrutiny, 99 are
blocked because `lab/CATALOG.md` itself still marks them `ACTIVE`/`HOLD` (not closed at all), 38 need
operator judgment (genuine ambiguity, not yet resolved either way).

**Round-3 correction (Codex PR #252, third review):** 5 items from the round-2 SAFE lists — 3
`lab/archive/` slugs (`orb_zb_recon_2026-07`, `striker_dj30_mym_prototype_2026-07`,
`usdcad_fade_2026-06-26`) and both `lab/analysis/_inbox/` items — were cited via a machine-checked
`source:` YAML field in `ops/instruments/*.md`, resolved at runtime by `scripts/instrument_profiles.py`'s
`_resolve()` (a literal filesystem `.exists()` check that HARD-fails the P1 profile gate if it doesn't
resolve) or a `discovery_manifests/*.json` path field. The 21-agent pass checked `ops/instruments/*.md`
inconsistently — it caught this exact pattern correctly in `docs/notes/notice/` and elsewhere, but
missed it here. **A follow-up sweep of all 51 then-safe `lab/archive/`+`_inbox` items against every
`ops/instruments/*.md` and `discovery_manifests/*.json` file found 25 with SOME mention — but only
these 5 hit the actual machine-checked `source:` field**; the other 20 are ordinary prose/markdown-link
citations in a DEAD-list section, the same "expected historical citation trail" pattern that
legitimately cleared 26 other `lab/archive/` items. Moved to their respective exclusion sets below.
`lab/analysis/_inbox/` is now entirely excluded (0 safe of 11).

**How to use this file:** the SAFE lists below are the current migration scope. Before opening a
deletion PR for any cluster, re-run a spot-check grep on that cluster's paths — this data is a
snapshot, not a standing guarantee; the repo keeps changing. Specifically for `ops/instruments/*.md`:
a hit only blocks migration if it's a `source: "..."` YAML field (machine-checked); a prose/markdown
citation in a DEAD/CLOSED-verdict section does not.

---

## Entirely excluded clusters (structural reasons, not per-file judgment)

These clusters returned zero or near-zero safe items, and the *reason* is structural — re-triaging
individual files won't fix it without first changing the underlying tooling or premise.

| Cluster | Checked | Safe | Why |
|---|---:|---:|---|
| `lab/analysis/c1/` (all 59 current slugs) | 59 | 0 | Every slug carries `lab/CATALOG.md` status `ACTIVE` or `HOLD` — this is live research, not a closed-campaign backlog. The v1 survey's premise that this was a ~296-file closed cluster was wrong at the cluster level, not just on individual items. Several slugs are also load-bearing to `core/firm_rules.py`, `ops/c1_rail/c1_sizing_host_reference.py` (the live sizing host), or `.claude/skills/c1-rail/SKILL.md`. |
| `lab/analysis/legacy/` (9 children) | 9 | 0 | 8 `ACTIVE` + 1 `HOLD` in `CATALOG.md`. `futures_conversion_2026-07-01` has a confirmed live `sys.path` import from `lab/analysis/c1/q_rail_1_2026-07/f2_floors.py:18` (the original Codex catch) plus a live skill citation and CI `--ignore` reference (`guardian_parity_2026-06-23`). |
| `lab/analysis/harvest/` | 13 campaigns / 55 files | 0 | The v1 "46 of 55 closed subset" framing doesn't correspond to anything on disk (55 tracked files, 13 campaigns, no 46-file subset exists). 12 of 13 campaigns are `CATALOG` `ACTIVE`. Live code deps confirmed: `tests/test_stage4_7_drivers.py` (`sys.path.insert`), `ops/instruments/profiles.json` (a `"source"` field resolved at runtime by `scripts/instrument_profiles.py`), `tests/governance/test_sentinel.py` (hardcoded fixture paths). |
| `docs/briefs/closures/` | 84 | 0 | `scripts/check_closure_disposition.py` hardcodes 3 frozensets totaling 100 exact closure filenames (lines 189-224, 254-293, 305-334) as live governance-gate input — this is the same "quoted string path literal in live code" class Codex caught before, at cluster scale. 50/84 hit those sets directly; the other 34 carry genuine doc citations (6 also fail on `CATALOG` `ACTIVE`/`HOLD`). |
| `docs/briefs/rnd-pipeline/` | 30 | 0 | `scripts/check_advisor_dedup.py:213-218` globs the entire directory as one of its 8 mandatory dedup-corpus surfaces. Not vestigial — `docs/operational_rules.md` §8 sub-rule 8 and the `brief-authoring` skill mandate running it before any new campaign; its own docstring records two real incidents this exact gap already caused. |
| `docs/analytics/`, `docs/lessons/`, `docs/methodology/archive/`, `docs/external/` | 14 | 0 | `docs/analytics/mc_anchor_evolution/{plot.py,data.csv}` is a live import in `tests/test_mc_anchor_chart.py` (the original Codex catch). The other three carry live doc citations (canonical methodology docs, dedicated ADRs, `CLAUDE.md`-linked `mc_anchor_history.md`). |
| `docs/notes/notice/` | 36 | 1 | Ratified ([`ADR`](2026-08-15-notice-log-is-the-live-observation-routing-convention.md)) as "the estate's continuous, sole practice for recording observations" — by design, almost everything in it is a permanent provenance anchor cited from ADRs, briefs, `ops/instruments/*.md`, or `STATE.md`. 6 files are cited via a literal `source:` field in `ops/instruments/*.md`/`profiles.json` that `scripts/instrument_profiles.py` hard-fails on if unresolved. |
| `lab/analysis/_inbox/` | 11 | 0 | Round-3 correction: both round-2 "safe" items (`ict_1mexec_1_2026-08`, `rangexfer_presence_battery_2026-08-30`) are cited by machine-readable path fields — `discovery_manifests/ict-1mexec-1.json`'s `reachability_attestation`/`profile_consult` fields, and `ops/instruments/MECHANISMS.md:231,401` — plus `ops/instruments/MNQ.md:136` treats the first's RESULTS.md as current verdict evidence. Combined with the other 9 (6 `CATALOG` `ACTIVE`/`HOLD`, 1 live code dep, 1 doc citation, 1 operator judgment — see the round-2 detail preserved in the workflow journal), this cluster is now 0 of 11. |

**None of these eight clusters should be batch-migrated.** If any individual file within them is
migrated later, treat it as its own judgment call with its own citation sweep, not a batch action.

---

## Partially-safe clusters — explicit SAFE lists

### `lab/archive/` — 46 of 90 safe

`approach_scoreboard_2026-08` · `c1_capalloc_2026-07-27` · `futures_prop_hold_compat_2026-06-30` ·
`gbpusd_rank_cert` · `identify_nas100_2026-06-20` · `msl_c2_mgc_2026-08` · `msl_c3_m2k_2026-08` ·
`mym_3fps_recon_2026-07` · `noct_spx` · `nsurv_layer_design_2026-08-20` · `oanda_stage1` ·
`oil_carry` · `opening_pressure_map_2026-07` ·
`orbmnq1_survivor_scoring_2026-08-20` · `p2_replay_2026-07` · `pharos_us500_sweepfvg` ·
`q_bookfit_1_2026-07` · `q_compose_1_2026-07` · `q_condval_1_2026-08` · `q_decay_1_2026-07-10` ·
`q_evalseq_1_2026-08` · `q_expr_1_2026-08` · `q_fbeia_1_2026-07` · `q_fccarry_1_2026-07` ·
`q_funnel_1_2026-07` · `q_inventory_1_2026-07` · `q_joint_tail_weekly_2026-07` ·
`q_nas_4_2026-06-20` · `q_pyrparity_1_2026-07` · `q_znauc_1_2026-07` · `regime_aegis_2026-06-16` ·
`regime_ratevol_2026-06-16` · `regime_remc_2026-06-22` · `regime_signal_research_2026-06-25` ·
`slr_mym_phase05_2026-07-29` · `spx500_f09_gate_2026-06-20` ·
`timeframe_5m_2026-06-25` · `tnec_envelope_compile_2026-08` · `todvol_1_2026-08-20` · `tom_spx` ·
`tradeify_selectflex_remc_2026-07-10` · `usdcad_ratemap_verify_2026-06-15` ·
`usdcad_rdm` · `usoil_rdm` · `usoil_regime_capture` · `xindex_rv_recon_2026-07`

305 tracked files across these 46 slugs (`git ls-files lab/archive/<slug>/` per slug, summed).

Excluded (44): 3 moved from SAFE in the round-3 correction — `orb_zb_recon_2026-07`
(`ops/instruments/ZB.md:22` `source:` field), `striker_dj30_mym_prototype_2026-07`
(`ops/instruments/MYM.md:45` + `YM.md:21`), `usdcad_fade_2026-06-26` (`ops/instruments/USDCAD.md:37`)
— all three resolve to real files today, so `scripts/instrument_profiles.py`'s P1 gate would HARD-fail
the instant the source directory is deleted. 25 fail on live doc citation
(`ops/instruments/*.md` prose, `docs/rejected_candidates.md`, or an `ACTIVE`-campaign's own RESULTS.md
citing them as "named residual, not re-run"), 9 fail on confirmed live code dependency
(`sys.path`/`importlib`/direct read from an `ACTIVE` sibling or a live script — e.g.
`q_kbudget_1_2026-07` read by `tests/test_floor_scan_htsmom_pin.py` via `importlib`;
`rates_ev_zf_recon_2026-07` dynamically imported by `scripts/diff_econ_calendar.py`), 7 flagged
`NEEDS_OPERATOR_JUDGMENT` (stale/likely-dead references that a skeptical-by-default pass didn't
self-clear — see journal for `custodian_eurusd`, `external_sourcing_2026-06-30`,
`feed_divergence_2026-06`, `guardian_decay_gate_2026-06-25`, `q_geofit_1_2026-07`,
`regime_cond_2026-06-30`, `usdcad_reverse_2026-06-14`).

**Pre-rename paths recovered** (needed for the `filter-repo` extraction per the main spec's step 4):
the MSL campaigns + `nsurv_layer_design_2026-08-20` + `orbmnq1_survivor_scoring_2026-08-20`
originated under `lab/analysis/c1/<slug>/`; `p2_replay_2026-07` under flat
`lab/analysis/p2_replay_2026-07/`; `q_condval_1_2026-08` under `lab/analysis/_inbox/q_condval_1_2026-08/`.
Most others show only the standard `lab/analysis/<slug>/CARD.md` stub pattern (flat, non-themed
origin) — `git log --follow` is uninformative repo-wide since this clone's history starts at the
single 2026-08-14 public-release squash commit.

### `docs/briefs/*.md` (root, loose) — 60 of 64 safe

Q-BOOKFIT-1, Q-BUSTGATE-1, Q-BUSTGATE-2, Q-C1PANEL-1, Q-CALLBOUND-1, Q-CAPA-1, Q-CAPBAND-1,
Q-CAPRES-2, Q-COMPOSE-1, Q-CONDVAL-1, Q-DATAFIDELITY-1, Q-DECAY-1, Q-EXPR-1, Q-FIRMEOD-1,
Q-GATECART-1, Q-GATESTACK-1, Q-GEOFIT-1, Q-INTAKEGOV-1, Q-INVENTORY-1, Q-KBUDGET-1 (both files),
Q-KBUDGET-HARVEST-1 (both files), Q-M1WIRE-1, Q-MCLTAS-1, Q-MNQDTL-CON-1, Q-NSURV-1, Q-NSURV-2,
Q-OBJCOHERE-1, Q-OFCHAN-1, Q-ORBCUSH-1, Q-ORBSURV-1, Q-PERSIST-1, Q-POLFRONT-1, Q-PUBTRANS-1,
Q-PYRPARITY-1, Q-R2AGRUN-1, Q-R2FLOW-1, Q-R2VBUCK-1, Q-RAIL-1, Q-RANGECOND-1, Q-S5CAP-1,
Q-SFRISK-1 (both files), Q-SIZECOMP-1, Q-STATVALID-1, Q-STRIKER-MYM-RECON-1, Q-STRIKER-MYM-RECON-2,
Q-TNEC-CON-2, Q-TNEC-CON-3, Q-TNEC-CON-4, Q-TNEC-CON-5, Q-TOM-SPX-1, Q-TRADECAP-1, Q-TRADECAP-2,
Q-TRAINKILL-1, Q-TRAINKILL-2, Q-TRAINKILL-3, Q-TXG-1, Q-XMEM-1 (exact filenames unchanged from v1 —
see `git ls-files docs/briefs/*.md`).

Excluded (4): Q-MONSURF-1 and Q-TVCOV-1 fail on their own `CATALOG` `ACTIVE` row
(`msl_monsurf_1_idle_clock_2026-08`, `tvcov_2026-07`); Q-RANGEXFER-1 fails on a live code citation
(`docs-runtime-inventory.md` records two un-archived `_inbox` scripts quoting its §6/§7 by section
number); Q-MSCHAN-1 is `NEEDS_OPERATOR_JUDGMENT` — self-declared `DRAFTED — NOT OPENED`, never
actually closed despite sitting in the "closed" cluster, and a 2026-08-24 Accepted ADR ratified a
live text-intercept edit into it.

### `docs/briefs/pre-registration/` — 45 of 88 safe

2026-07-16-striker-mym-reconstruction-candidate-2-prereg, 2026-08-01-drift-exhaustion-mechanism-preregistration,
2026-08-04-ict-1m-execution-mnq-preregistration, 2026-08-11-guardian-mgc-transfer-cell-prereg,
2026-08-12-q-txg-1-striker-mnq-cell-prereg, 2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg,
2026-08-16-deep-lane-dl1-mgc-orc-prereg, 2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg,
2026-08-24-grow-0-limb-c-marginal-effect-RESULTS, D5-RECOST-1, MYM-3FPS-1, OPENPRESS-1,
Q-6JCOMPOSE-1, Q-6JCOMPOSE-2, Q-BOOKFIT-1, Q-BUSTGATE-1, Q-BUSTGATE-2, Q-C1PANEL-1, Q-CALLBOUND-1,
Q-CAPALLOC-1, Q-CAPALLOC-2, Q-CAPBAND-1, Q-COMPOSE-1, Q-CONDVAL-1, Q-COSTGEO-1, Q-COSTGEO-2,
Q-COSTGEO-3, Q-DATAFIDELITY-1, Q-EXPR-1, Q-FIRMEOD-1, Q-FUNNEL-1, Q-GATESTACK-1, Q-INTAKEGOV-1,
Q-INVENTORY-1, Q-NSURV-2, Q-OBJCOHERE-1, Q-ORBSURV-1, Q-PUBTRANS-1, Q-PYRPARITY-1, Q-RANGECOND-1,
Q-S5CAP-1, Q-SIZECOMP-1, Q-STATVALID-1, Q-TRADECAP-1, Q-TRADECAP-2 (all `-verdict-preregistration.md`
unless noted; exact suffix per `git ls-files`).

Excluded (43): 24 fail on `CATALOG` `ACTIVE`/`HOLD` (the entire `aegis-6j-prop-reconstruction`
family, `class-s-c1-lifecycle-haircut-regime-remc`, `c1-band-rescore-corrected-geometry`,
`Q-TRAINKILL-1/2/3`, and 18 more — see journal), 10 have confirmed live code dependencies (most
seriously: `prop-survivor-scoring` v2 is the canonical `GATE_PREREG` path embedded in the live
production module `lab/discovery/prop_survivor_scoring.py`, imported by 20+ scripts; `Q-RAIL-1`'s
pre-reg backs `ops/c1_rail/c1_sizing_host_reference.py` — the live c1 rail sizing oracle), 2 fail on
doc citation, 7 need operator judgment. Also excluded per the original spec: the 5 pre-regs for the
still-OPEN/DORMANT Qs (Q-SIGID-1, Q-FILLTAX-1, Q-VOLREGIME-1, Q-FUNDPOL-1, Q-GATECAL-1) — reconfirmed
genuinely live, not reclassified.

### `docs/notes/audits/` + `docs/notes/research/` — 33 of 66 safe

2026-07-10-research-liveness-inventory, 2026-07-12-08-08-classA-reachability-audit,
2026-07-12-disccamp0-gate-reachability-audit, 2026-07-24_gate_composite-closure-deletion,
2026-07-29-live-docs-stale-claims-audit, 2026-07-29-methodology-90day-rebound-review,
2026-08-08-conventions-delete-phase-gap-audit, 2026-08-08-pipeline-requirements-question-closing,
2026-08-11-code-dry-audit, 2026-08-11-rule7-dry-fact-audit, 2026-08-14-requirements-backlog-ratification,
2026-08-19-governance-friction-persona-panel-audit, 2026-08-23-p10-open-roster-census,
brief-corpus/2026-08-29-brief-decay-audit, issue_54_ulp_audit.json, issue_54_ulp_audit.md,
programme-audit/2026-07-01-meta-layer-audit-completion, programme-audit/2026-07-11-core-fxify-anchoring-audit,
programme-audit/2026-08-05-claim-alignment/{01-diagnostics,02-blockers,04-misleading,06-operator-judgement,07-followups,2026-08-06-script-wiring-census,README},
programme-audit/2026-08-14-f2-adr-corpus-disposition, programme-audit/2026-08-14-msl-methodology-audit,
programme-audit/2026-08-15-governance-belt-meta-audit, programme-audit/2026-08-15-msl-wall-scope-audit,
programme-audit/2026-08-20-external-mapping-move-class-audit,
research/2026-08-19-agentic-research-team-structures, research/2026-08-23-t3-surrogate-calibration,
research/2026-08-23-tradable-anomalies-t2-t3-prego-inventory.

Excluded (33): 19 fail on doc citation (`docs/rejected_candidates.md` "Authoritative artifact:"
lines, `docs/briefs/INDEX.md` "Origin:", `STATE.md` open rows — see journal for the full list, e.g.
2026-08-23-kill-register-attribution-audit, 2026-07-01-cross-layer-synthesis,
2026-08-31-mnq/mym-overnight-window-defect audits), 12 fail on live code (e.g.
`core/firm_rules.py:49` cites `2026-08-23-bulenox-lock-scope-resolution.md` by path in a live
comment; `scripts/check_lab_path_relocation.py`'s `INTENTIONAL_STALE_DOCS` frozenset hardcodes 3
`claim-alignment/` filenames; `.claude/skills/adr-decay-audit/SKILL.md`'s output-path template names
the 2026-08-29 decay audit as its own canonical artifact class), 2 need operator judgment.

### `docs/superpowers/plans/` — 14 of 24 safe

2026-08-20-cross-campaign-mechanism-prior, 2026-08-22-grow0-harness-implementation,
2026-08-23-bind-operator-queue-implementation, 2026-08-23-coldstore-phase-b-implementation,
2026-08-23-coldstore-phase-c-implementation, 2026-08-23-grow-lane-leftovers-implementation,
2026-08-23-p2-memory-demote-implementation, 2026-08-23-p3-docs-runtime-inventory-implementation,
2026-08-23-p4-museum-rules-implementation, 2026-08-23-p5-repo-map-layers-implementation,
2026-08-23-substrate-phase-6-implementation, 2026-08-23-tradable-anomalies-t3-implementation,
2026-08-23-venue-binding-registry-implementation, 2026-08-23-w5-ci-from-gates-yml-implementation.

Excluded (10): 8 are still cited from live governance surfaces (6 named in `STATE.md`'s current
15-row decision index; `repo-pain-point-packets` is the definitional citation target for
"pain-point P0-P10" in root `README.md`; `call4-beta-cohesion-implementation` is directly quoted in
the live `docs/methodology/strategy_lifecycle.md`), 1 fails on live code (`viable-strategy-parallel-s4-firm-repair`
is a `"parent_plan"` string literal inside `lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/run_r1_bulenox_blusky_intraday.py`
— that RESULTS directory is `CLAUDE.md`-pinned canonical evidence), 1 needs operator judgment
(`futures-anomaly-discovery-skill-skew-implementation` — owning Notice's Status field literally
reads `OPEN`).

### `docs/spec/` closed retirement + build specs — 13 of 21 safe

2026-05-23-trade-capture-skill-design, 2026-06-13-codifier-breakout-longshort-trailing-extension,
2026-06-17-dukascopy-retirement-design, 2026-06-17-dukascopy-retirement-plan,
2026-06-24-nas100-orb-filters-design, 2026-06-24-nas100-orb-filters-plan,
2026-06-24-oanda-retirement-design, 2026-06-24-oanda-retirement-plan,
2026-08-02-tradeify-activity-rule-disposition-spec, 2026-08-06-mnqprox-2-tod-matched-level-proximity-spec,
CC-HANDOFF-monorepo-boundaries, issue_54_survey_brief, pine_baseline_csv_format.

Excluded (8): 4 fail on live code/doc dependency, including 2 caught only by the code-grep step
(`session-log-rolloff-design`, `wfo-runner-v0`) that a doc-only pass would have missed —
reproducing the exact failure mode Codex flagged; `PREREG-NAS-ECR-1` is additionally on an explicit
operator "do NOT move" keep-list in a prior handoff; 3 more are `NEEDS_OPERATOR_JUDGMENT` for
bundle-coherence reasons (tightly cross-linked to an unsafe sibling, not independently blocked).

### `docs/briefs/handoffs/` + `docs/historical/` — 16 of 40 safe

`docs/briefs/handoffs/`: 2026-07-13-cursor-handoff-post-batch-doc-artifacts,
2026-07-16-cc-handoff-aegis-6j-wave1-n80-adjudication, 2026-07-16-cursor-handoff-h-od-1-stage1-2-pull,
2026-07-24-cursor-handoff-c1-deploy-packaging-fix, 2026-07-24-cursor-handoff-ltm-rolloff-execution,
2026-07-24-cursor-handoff-request-received-price-capture,
2026-07-26-cursor-fleet-cost-normalization-umbrella, 2026-08-12-msl-tooling-packet-{A,B,C},
2026-08-24-cursor-handoff-harvest-shape-floor-citation,
2026-08-29-cursor-handoff-notice-grade-k-correction-audit.
`docs/historical/` (whole dir, all 4 files): README, portfolio_mc_2026-04-20_aegis_2pct_sensitivity,
portfolio_mc_2026-04-20_v5.4_v4.4_v4.2, v5_5_validation_halt_2026-04-21.

Excluded (24, all within `handoffs/`): 1 fails on live code
(`2026-07-24-cc-handoff-core-dead-code-prune.md` — `tests/test_check_brief.py:446` asserts this
exact fixture file exists), 13 fail on doc citation (mostly `CATALOG`-`ACTIVE` citing campaigns or
Accepted ADRs/live SESSIONS entries with operator-owed language), 10 need operator judgment.
`docs/historical/` is fully clean — zero citations anywhere, its own README already says "not live
doctrine."

### `docs/notes/notice/` — 1 of 36 safe

`N-2026-08-24-breadth-over-magnitude-phase-b-target-restatement.md` — the only file in this
directory with zero hits across every surface checked, verified with an unscoped repo-wide grep.
Everything else stays (see the exclusion table above).

---

## Corrected total: 228 of 650 checked (35%) — 487 tracked files

| Bucket | Items | Files | Notes |
|---|---:|---:|---|
| `lab/archive/` | 46 / 90 | 305 | |
| `lab/analysis/c1/` | 0 / 59 | 0 | entire cluster excluded |
| `lab/analysis/legacy/` | 0 / 9 | 0 | entire cluster excluded |
| `lab/analysis/harvest/` | 0 / 13 campaigns | 0 | entire cluster excluded |
| `lab/analysis/_inbox/` | 0 / 11 | 0 | entire cluster excluded (round-3 correction) |
| `docs/briefs/closures/` | 0 / 84 | 0 | entire cluster excluded |
| `docs/briefs/*.md` (root) | 60 / 64 | 60 | |
| `docs/briefs/rnd-pipeline/` | 0 / 30 | 0 | entire cluster excluded |
| `docs/briefs/pre-registration/` | 45 / 88 | 45 | |
| `docs/briefs/handoffs/` + `docs/historical/` | 16 / 40 | 16 | |
| `docs/spec/` | 13 / 21 | 13 | |
| `docs/notes/audits/` + `research/` | 33 / 66 | 33 | |
| `docs/notes/notice/` | 1 / 36 | 1 | |
| `docs/superpowers/plans/` | 14 / 24 | 14 | |
| `docs/analytics/` + `lessons/` + `methodology/archive/` + `external/` | 0 / 14 | 0 | entire cluster excluded |
| `docs/governance/notion-redirect-map.md` | 0 / 1 | 0 | cited by 3 live skills |
| **Total** | **228 / 650** | **487** | |

"Items" and "files" differ only for `lab/archive/` (46 directory-slugs expand to 305 files); every
other row is already file-granular (1 item = 1 file). The `Gate` in the main spec is defined against
the **487-file** total, not the 228-item count — an item count alone can't verify a byte-identical
deletion.

38 items across the above clusters are `NEEDS_OPERATOR_JUDGMENT` (genuine ambiguity — a stale-looking
but not-quite-dead reference, a self-contradicting status field, a bundle-coherence coupling) and are
not counted as safe above; see each cluster's exclusion note or the workflow journal for the specific
items.

---

## Provenance

21-agent parallel verification, 2026-09-01, Workflow `wf_ce66f55a-f3a` (script:
`archive-migration-survey-redo-v2`), 490 tool calls, ~3.5M tokens. Full per-item evidence (exact
`grep`/`git log` output backing every verdict) is in that run's `journal.jsonl`, not reproduced here.
Triggered by Codex's PR #252 review catching two live-dependency misses in the doc-only v1 manifest.
**Round-3 correction** (same PR, third review): a targeted sweep of the 51 then-safe `lab/archive/`+
`_inbox` items against `ops/instruments/*.md` `source:` fields and `discovery_manifests/*.json` found
5 more misses, moved to their exclusion sets; verified directly against the cited files and
`scripts/instrument_profiles.py`'s `_resolve()` function, not taken on faith.
