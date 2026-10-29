# PIPELINES — data-flow map

Companion to [REPO_MAP.md](REPO_MAP.md). [STATE.md](STATE.md) owns priorities and obligations;
[AGENTS.md](AGENTS.md#live-execution-posture) owns execution safeguards.

## Current path — Tradeify native (read first)

ORB+Aegis, one candidate under branch (b) ([STATE item 1](STATE.md#operator-queue--strictly-ordered-5-live-items); [routing](docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#current-routing--2026-10-29-derived-mirror)). Boundaries:

- read-only stage 1 assessment granted, nothing more ([branch (b)](docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-28--branch-b-ruled-ahead-of-the-11-08-sitting));
- qualification framework DRAFT ([Q-TFYNATIVE-1](docs/briefs/pre-registration/2026-10-26-tradeify-native-lane-prereg-DRAFT.md)); the [native plan](docs/superpowers/plans/2026-10-21-tradeify-native-ninjascript-strategy-plan-DRAFT.md#reading-limits--2026-10-29-consistency-note) is DRAFT;
- the pair's evidence case and exclusivity owed; workshop ORB, O-N and O-0 share no evidence ([boundary](docs/superpowers/specs/2026-10-28-orb-aegis-workshop-design.md#evidence-and-ownership-boundary));
- forward-test route ruled privately (D6; [held privately](docs/notes/2026-10-24-assumption-challenge-rulings-proposal.md));
- per-session operator GO.

Execution logic stays in NinjaTrader; Python only receives exported records after the session ([runbook](docs/notes/2026-10-18-native-protection-recovery-pilot-runbook.md) native premise). The Python signal daemon, listener/sizing host, CrossTrade route and Fly hosts are **not** native dependencies. Monitoring: P6.

## Pipeline inventory

| # | Pipeline | Recorded use / next handoff | Owner layers |
|---|---|---|---|
| P1 | Discovery / research | Available on TV CME exports; vendor acquisition blocked (below); idle lines dormant 2026-10-15 ([INDEX](docs/briefs/INDEX.md)); the personal lane uses supplied strategies | `lab/discovery/`, `lab/research_utils/`, `discovery_manifests/` |
| P2 | Python → Pine codification bridge | Retired | [Archive guidance](docs/ltm/README.md) |
| P3 | Legacy portfolio Monte Carlo | CLI idle; current research reuses its primitives | `core/mc/`, `core/portfolio_mc.py` |
| P4 | Firm-specific construction / sizing | Selection closed 2026-09-10 by operator [acceptance](docs/notes/2026-09-10-tradeify-protection-selection.md#operator-acceptance-and-state-item-1-closure); Track B and personal lane below | `lab/analysis/c1/`, `core/mc/`, `core/firm_rules.py`, `ops/c1_rail/book_policy.py` |
| P5 | Python execution rail (c1) + qualification | Built, disarmed; serves the personal lane; not in the native path | `ops/c1_rail/` (incl. `qualification/`), `ops/c1_signal_daemon/`, `deploy/`, `tools/qualification_verification/` |
| P6 | Monitoring | M1 `RESOLVED` 2026-09-14, incumbent rail Stage 1 only; fill-gated monitors dormant | `ops/c1_rail/c1_rail_telemetry.py` |
| X | Governance | Evidence, integrity and authority checks on every handoff | `scripts/`, `docs/`, manifests |

### Other routes (not current)

**Personal lane:** [Q-SFCLEAR-3](docs/briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md) frozen; dispatch paused under the [10-19 ruling](docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-19--no-book-lineage-configuration-has-an-evidence-case-for-the-tradeify-evaluation); [ADR](docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md#grounds) items 1–8 owed ([STATE](STATE.md#scheduled-forward-triggers)). P5 updates when its owner's pending Python-route record lands.

**Track B:** superseded for Tradeify 2026-10-16 ([addendum](docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-16--track-b-superseded-for-tradeify)).

## P1 — Discovery / research pipeline (Gen-2) — available

[Evaluation order](docs/adr/2026-08-30-evaluation-order.md) owns the gate sequence for
contracts frozen after 2026-08-30; read it before execution.

| Handoff | Producer / input | Consumer / output |
|---|---|---|
| Acquire data | **Blocked**: Databento retired, no replacement; never run `db_fetch.py` | Historical DBN cache; a new source needs operator GO ([record](docs/adr/2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento)) |
| Bind a search | Channel intake, frozen candidate contract | `lab/discovery/register_search.py` → committed `discovery_manifests/<run_id>.json` |
| Explore | `lab/discovery/stage24_runner.py`, campaign harnesses | Observations and candidate evidence; never automatic promotion |
| Evaluate | Evaluation order, [survivor-scoring prereg](docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) | Typed verdict and evidence; scoring by `lab/discovery/prop_survivor_scoring.py` |
| Admit and monitor | Admitting decision, calibrated decay monitor | [Strategy lifecycle](docs/methodology/strategy_lifecycle.md), then venue/deployment gates |

Skill owners: `futures-anomaly-discovery` (candidate generation), `strategy-validation`
(validation mechanics). [Campaign defaults](docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md)
own temporal evidence and budget conventions; [W4](docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md)
governs dormant SPA/StepM, PBO/CPCV and breadth producers.

New campaigns: a wired harness does not prove its survivor path ran (read RESULTS and skips
first); the [K-budget reachability screen](docs/briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md)
precedes a funded one; open manifests do not bank K.

## P2 — Codification bridge (Python → Pine) — RETIRED 2026-08-02

Pine/TV stays research/export. A future crossing needs a fresh build and identity check.

## P3 — Portfolio construction (Monte Carlo) — legacy CLI idle

[core/mc README](core/mc/README.md). The `cme` panel is breadth-only, not a working MC
rerun (legacy ingestion gate); use the owning plan's harness or `prop_survivor_scoring.py`.

## P4 — Firm application / sizing

`core/firm_rules.py`, `core/mc/preflight.py` and `core/dd_geometry.py` own firm rules and
engine support; the campaign owns population, replay and design;
[prop_envelope_default.md](ops/prop_envelope_default.md) is the standing envelope. The
[four-firm program](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md) falsifier is
tracked on [STATE](STATE.md).

## P5 — Python execution rail (c1), personal lane — BUILT · DISARMED

Not a native dependency. Python signal daemon → listener/sizing host → CrossTrade → Tradovate
([listener](deploy/c1_rail/README.md), [daemon](deploy/c1_signal_daemon/README.md)). Track B's book modules (`book_*`, `account_close_*`) stay offline until a deployment
GO. [`nautilus_trader`](docs/adr/2026-07-10-databento-research-stack.md) remains research-only.

**Qualification (offline).** `ops/c1_rail/qualification/` is the fixed-book machinery
(`personal_replay.py` serves the personal lane); its `execution/` subpackage is the protected
TEST_ONLY service ([B0](docs/superpowers/plans/2026-09-19-attended-batch-qualification.md#b0-decision--2026-09-19)),
launched by `deploy/qualification/bootstrap.py` on the
[disposable host](tools/qualification_verification/README.md). The
`.github/workflows/qualification-*.yml` evidence workflows are not required checks.

## P6 — Monitoring — M1 RESOLVED (2026-09-14), incumbent rail Stage 1 only

A native instance needs its own M1 ([runbook §3](docs/notes/2026-10-18-native-protection-recovery-pilot-runbook.md#3-pilot-sequence-and-stop-rules)); no acceptance or test evidence transfers between instances.

[M1 acceptance](docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json) and its
[validator](scripts/validate_c1_monitoring_acceptance.py) own monitoring maturity; evidence:
[A7/A8 record](docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md#a8--signed-acceptance-deployed-re-bake-verified-2026-09-14).
[Q-MONSURF-1](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md) separates idle monitoring,
fill-gated capture and the observer; wakes are on [STATE](STATE.md#scheduled-forward-triggers).

## X — Governance / discipline cross-cut — LIVE throughout

Entry points: `scripts/check_boundaries.py`, hash manifests ([scripts README](scripts/README.md)),
[gates.yml](scripts/gates.yml), [operational rules](docs/operational_rules.md) and
[methodology](docs/methodology/README.md).

## Data stores

- Research: CME TV exports (below); Databento retired (P1).
- c1 live feed: none approved; daemon emission off.
- Native execution: platform data via NinjaTrader/Tradovate under the firm's arrangement; CME licensing open ([native plan §2 item 2](docs/superpowers/plans/2026-10-21-tradeify-native-ninjascript-strategy-plan-DRAFT.md#2-prerequisites-by-what-they-gate)).

- `core/data/tv_exports/cme/`: private CME trade exports, hash-pinned; bind per campaign.
- `core/data/bar_data/`: frozen private panels; not regenerable.
- `core/data/external/`: exogenous research series; SHA256SUMS.
- `core/strategies/`: catalog/CARD stubs, private archived sources; source/port manifests.
- `lab/analysis/<theme>/<slug>/`: campaign evidence, harnesses; indexed in [catalog](lab/CATALOG.md).
- `discovery_manifests/`: committed search contracts/status; commitment is the pin.
- `ops/data/`: retained reconciliation records.
- Private DBN cache: historical request-keyed Databento pulls; gitignored.
- [lab/ARCHIVED.json](lab/ARCHIVED.json): removed-path inventory, preservation provenance.

Historical figures keep their provenance; new data or venues do not silently inherit their
claims.
