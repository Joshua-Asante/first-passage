# PIPELINES — data-flow map

Companion to [REPO_MAP.md](REPO_MAP.md). [STATE.md](STATE.md) owns priorities and obligations;
[AGENTS.md](AGENTS.md#live-execution-posture) owns execution safeguards.

## Pipeline inventory

| # | Pipeline | Recorded use / next handoff | Owner layers |
|---|---|---|---|
| P1 | Discovery / research | Available; Track B uses supplied strategies, not a new run | `lab/discovery/`, `lab/research_utils/`, `discovery_manifests/` |
| P2 | Python → Pine codification bridge | Retired | [Archive guidance](docs/ltm/README.md) |
| P3 | Legacy portfolio Monte Carlo | CLI idle; current research reuses its primitives | `core/mc/`, `core/portfolio_mc.py` |
| P4 | Firm-specific construction / sizing | Selection closed 2026-09-10 by operator [acceptance](docs/notes/2026-09-10-tradeify-protection-selection.md#operator-acceptance-and-state-item-1-closure); Track B qualification is the handoff | `lab/analysis/c1/`, `core/mc/`, `core/firm_rules.py`, `ops/c1_rail/book_policy.py` |
| P5 | Execution rail + qualification | Built, disarmed; Track B qualification, feed decision and deployment GO precede deployment | `ops/c1_rail/` (incl. `qualification/`), `ops/c1_signal_daemon/`, `deploy/`, `tools/qualification_verification/` |
| P6 | Monitoring | M1 `RESOLVED` 2026-09-14; fill-gated monitors dormant | `ops/c1_rail/c1_rail_telemetry.py` |
| X | Governance | Evidence, integrity and authority checks on every handoff | `scripts/`, `docs/`, manifests |

### Current campaign handoff

Track B — qualify the accepted book (the [STATE](STATE.md) queue item). Owners:
[umbrella](docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) (scope, authority, gates),
[deployment checklist](docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) (cross-workstream sequence),
[execution-slices plan](docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md) (qualification engineering requirements;
[acceptance ledger](docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#progress-ledger-and-present-disposition)),
bounded handoffs (assignments),
[campaign record](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#55--track-b-release--d-b1d-b15-recorded-2026-09-11)
§55–§60 (rulings, evidence,
[ownership](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#58--campaign-ownership-the-current-coordinating-task-2026-09-20)).
Synthetic E1 evidence and host readiness are not a qualified book. Separate from M1
`RESOLVED` and still owed: production feed (umbrella O-4, deferred 2026-09-11; none
selected), deployment GO, the arm.

## P1 — Discovery / research pipeline (Gen-2) — available

[Evaluation order](docs/adr/2026-08-30-evaluation-order.md) owns the gate sequence for
contracts frozen after 2026-08-30; read it before execution. Channel artifact migrations owed
on [STATE](STATE.md) do not suspend it; campaign amendments are explicit owner decisions.

| Handoff | Producer / input | Consumer / output |
|---|---|---|
| Acquire data | **Blocked**: Databento retired/unsubscribed (operator report 2026-09-10), no replacement approved; do not run `db_fetch.py` estimate/pull | Historical DBN cache only; a new source needs explicit operator GO ([retirement record](docs/adr/2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento)) |
| Bind a search | Channel intake, frozen candidate contract | `lab/discovery/register_search.py` → committed `discovery_manifests/<run_id>.json` |
| Explore | `lab/discovery/stage24_runner.py`, campaign harnesses | Observations and candidate evidence; never automatic promotion |
| Evaluate | Evaluation order, [survivor-scoring prereg](docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) | Typed verdict and evidence; scoring by `lab/discovery/prop_survivor_scoring.py` |
| Admit and monitor | Admitting decision, calibrated decay monitor | [Strategy lifecycle](docs/methodology/strategy_lifecycle.md), then venue/deployment gates |

The `databento-data` skill refuses estimate/pull/batch/download even with retained scripts
or keys. Skill owners: `futures-anomaly-discovery` (candidate generation), `strategy-validation`
(validation mechanics). [Campaign defaults](docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md)
own temporal evidence and budget conventions; [W4](docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md)
governs dormant SPA/StepM, PBO/CPCV and breadth producers.

### Two standing constraints on new campaigns

1. A wired harness does not prove its survivor path ran; read the campaign's RESULTS and
   skips first.
2. The [K-budget reachability screen](docs/briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md)
   precedes a funded campaign. Read manifest status: open manifests do not bank K.

## P2 — Codification bridge (Python → Pine) — RETIRED 2026-08-02

Pine/TV stays research/export; [S2](docs/adr/2026-08-07-loop-s2-signal-host-fork.md) selects
a Python live signal host. A future crossing needs a fresh build and identity check against
the then-current survivor format.

## P3 — Portfolio construction (Monte Carlo) — legacy CLI idle

Modules, facade and engine regression: [core/mc README](core/mc/README.md). The two-leg `cme`
panel is breadth-only: `python core/portfolio_mc.py --panel cme` is not a working MC rerun,
because the legacy ingestion gate still applies. Use the campaign harness or
`lab/discovery/prop_survivor_scoring.py` per the owning plan.

## P4 — Firm application / sizing

`core/firm_rules.py` (objective, failure clock), `core/mc/preflight.py` and
`core/dd_geometry.py` own firm rules and engine support; the campaign owns the bound
population, replay, composition policy and statistical design.
[prop_envelope_default.md](ops/prop_envelope_default.md) is the standing envelope; P5 owns
live quantities. The [four-firm program](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md)
and its dated falsifier, tracked on [STATE](STATE.md), are distinct from the bounded Select
attempt.

## P5 — Live execution rail (c1) — BUILT · currently DISARMED

Python signal daemon → Python listener/sizing host → CrossTrade → Tradovate; see the
[listener](deploy/c1_rail/README.md) and [daemon](deploy/c1_signal_daemon/README.md) deployment
READMEs. Track B's book modules (`book_*`, `account_close_*`) stay offline until a deployment
GO. [`nautilus_trader`](docs/adr/2026-07-10-databento-research-stack.md) remains research-only.

**Qualification (Track B, offline).** `ops/c1_rail/qualification/` is the fixed-book
qualification machinery: contracts, panel and replay, adjudication, evidence and seals. Its
`execution/` subpackage is the separately installed protected service for staged TEST_ONLY
qualification on Linux; complete E1 is still in development.
`deploy/qualification/bootstrap.py` is its isolated-Python role launcher;
[`tools/qualification_verification/`](tools/qualification_verification/README.md) the
disposable Ubuntu host. `.github/workflows/qualification-*.yml` collect boundary, S2
supervision, host and dispatch-only S5 Part A evidence for coordinator acceptance and run the
platform-independent suite on Windows; none is a required check. The [B0 decision](docs/superpowers/plans/2026-09-19-attended-batch-qualification.md#b0-decision--2026-09-19)
kept this service over an operator-launched batch.

## P6 — Monitoring — CFD estate RETIRED; venue-native M1 RESOLVED (2026-09-14)

[M1 acceptance](docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json) and its
[validator](scripts/validate_c1_monitoring_acceptance.py) own monitoring maturity; evidence:
[A7/A8 record](docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md#a8--signed-acceptance-deployed-re-bake-verified-2026-09-14).
[Q-MONSURF-1](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md) separates
registration-gated idle monitoring, fill-gated capture and the elective observer; wake
conditions are on [STATE's forward board](STATE.md#scheduled-forward-triggers).

## X — Governance / discipline cross-cut — LIVE throughout

Entry points: `scripts/check_boundaries.py` (import boundaries), hash manifests
([scripts README](scripts/README.md)), [gates.yml](scripts/gates.yml) (`make check`,
`make audit`), [operational rules](docs/operational_rules.md) and
[methodology](docs/methodology/README.md) (decision, budget, provenance, corrections).

## Data stores

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
