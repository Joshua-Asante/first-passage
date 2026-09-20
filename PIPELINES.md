# PIPELINES — data-flow map (what moves where, and why)

Workflow companion to [REPO_MAP.md](REPO_MAP.md). [STATE.md](STATE.md) owns current
priorities, [AGENTS.md](AGENTS.md#live-execution-posture) owns execution safeguards,
and each campaign's implementation plan owns its executable sequence. Statuses
below describe machinery and its recorded use; they confer no authorization.

## Pipeline inventory (at a glance)

| # | Pipeline | Recorded use / next handoff | Owner layers |
|---|---|---|---|
| P1 | Discovery / research | Available; current queue #1 uses supplied strategies, not a new discovery run | `lab/discovery/`, `lab/research_utils/`, `discovery_manifests/` |
| P2 | Python → Pine codification bridge | Retired; a future crossing requires a fresh build and identity check | Historical evidence via [archive guidance](docs/ltm/README.md) |
| P3 | Legacy portfolio Monte Carlo | Legacy CLI idle; shared simulation primitives are reused by current research | `core/mc/`, `core/portfolio_mc.py` |
| P4 | Firm-specific construction / sizing | Selection closed 2026-09-10 by operator acceptance; Track B qualification of the accepted book is the current handoff (below) | `lab/analysis/c1/`, `core/mc/`, `core/firm_rules.py`, `ops/c1_rail/book_policy.py` |
| P5 | Execution rail + qualification | Built, disarmed; M1 `RESOLVED` 2026-09-14; Track B qualification, the feed decision and deployment GO precede any deployment | `ops/c1_rail/` (incl. `qualification/`), `ops/c1_signal_daemon/`, `deploy/`, `tools/qualification_verification/` |
| P6 | Monitoring | M1 `RESOLVED` (A7 attended ceremony + A8 signed acceptance); fill-gated monitors stay dormant | `ops/c1_rail/c1_rail_telemetry.py`; fill-dependent monitors below |
| X | Governance | Evidence, integrity, and authority checks across every handoff | `scripts/`, `docs/`, manifests |

### Current campaign handoff

Configuration selection closed on 2026-09-10 by operator acceptance
([record](docs/notes/2026-09-10-tradeify-protection-selection.md#operator-acceptance-and-state-item-1-closure));
the [Select implementation plan](docs/superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md)
is historical. **Track B — qualify the accepted book** (the operator's *Tradeify
portfolio*) owns the current sequence: the
[umbrella handoff](docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md)
routes packets; the [campaign record](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#55--track-b-release--d-b1d-b15-recorded-2026-09-11)
(§55–§57) owns rulings, evidence and
[ownership](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#57--astra-tradeify-contract-ownership-and-closeout-routing-2026-09-13);
the [Protected Full E1 execution-slices plan](docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md)
and its [coordinator handoff](docs/briefs/handoffs/2026-09-19-full-e1-coordinator-handoff.md)
own the qualification engineering. Consult those for prerequisites and stopping
rules; neither synthetic E1 evidence nor host readiness constitutes a qualified book.

M1 is `RESOLVED` (2026-09-14: A7 attended ceremony, A8 signed acceptance —
[record](docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md#a8--signed-acceptance-deployed-re-bake-verified-2026-09-14));
Track A left the queue. Still separate and owed: the production feed (umbrella
O-4, deferred 2026-09-11), deployment GO and the arm.

## P1 — Discovery / research pipeline (Gen-2) — available

Start with the catalog, relevant instrument ledger and rejection bar before
opening a campaign. [Evaluation order](docs/adr/2026-08-30-evaluation-order.md)
owns the standing order for contracts frozen after 2026-08-30: structural screens,
contract and reachability gates, K-bound exploration, selection freeze, confirmation,
and scoped fit. Read its exact order and each gate's scope before execution.
Channel-specific artifact migrations remain separately owed on [STATE](STATE.md);
they do not suspend the evaluation order. Campaign amendments are explicit owner decisions.

### Data flow

| Handoff | Producer / input | Consumer / output |
|---|---|---|
| Acquire research data | **Blocked** — Databento retired/unsubscribed (operator report 2026-09-10); no replacement approved. Do not run `db_fetch.py` estimate/pull | Retained historical DBN cache only; new source needs explicit operator GO ([retirement record](docs/adr/2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento)) |
| Define and bind a search | Channel intake and frozen candidate contract | `lab/discovery/register_search.py` → committed `discovery_manifests/<run_id>.json` |
| Explore | `lab/discovery/stage24_runner.py` and campaign-specific harnesses | Observations and candidate evidence, never automatic promotion |
| Evaluate | Current evaluation-order owner and [survivor-scoring preregistration](docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) | Typed verdict and evidence; `lab/discovery/prop_survivor_scoring.py` supplies scoring |
| Admit and monitor | Admitting decision and calibrated decay monitor | [Strategy lifecycle](docs/methodology/strategy_lifecycle.md), then venue/deployment gates |

### Inputs → transforms → outputs

Research data acquisition is blocked pending an approved replacement source.
The `databento-data` skill is a retirement notice that refuses estimate/pull/
batch/download despite retained scripts or keys ([owner](docs/adr/2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento)).
Candidate-generation tools remain owned by `futures-anomaly-discovery`; validation
mechanics by `strategy-validation`. Parent/micro rescaling provides realism, not
independent instrument evidence. [Campaign defaults](docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md)
own temporal evidence and budget conventions.

### Ratified rules of evidence (campaign defaults, inherited by reference)

[W4](docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md) governs dormant SPA/StepM,
PBO/CPCV, and breadth producers. Available library code is not a live promotion
gate. The discovery Stage 2–8 names are historical activity vocabulary; they do
not override evaluation-order. Detailed old flows remain retrievable in Git history.

### Two standing constraints on new campaigns

1. A wired harness does not prove its survivor path has been exercised. Read the
   campaign's actual RESULTS and skips before relying on that claim.
2. The [K-budget reachability screen](docs/briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md)
   precedes a funded campaign. Screen PASS is neither candidate admission nor
   permission to buy data. Read manifest status: open manifests do not bank K.

## P2 — Codification bridge (Python → Pine) — RETIRED 2026-08-02

The Gen-1 bridge is retired. Pine/TV remains a research/export surface;
[S2](docs/adr/2026-08-07-loop-s2-signal-host-fork.md) selects a Python live signal
host. Any future Python/Pine crossing requires a fresh build and identity check
against the then-current survivor format. Retrieve old machinery through
[archive guidance](docs/ltm/README.md).

## P3 — Portfolio construction (Monte Carlo) — legacy CLI idle

`core/mc/ingest.py` builds panels; `simulation.py` owns transitions and seeded
paths; `modes.py` owns legacy orchestration; `portfolio_mc.py` is the facade.
The current campaign reuses shared engine primitives under its own plan.
The historical anchor stays in [mc_anchor_history.md](docs/mc_anchor_history.md).

The two-leg `cme` panel is breadth-only: `python core/portfolio_mc.py --panel cme`
is not a working MC rerun because the legacy ingestion gate still applies.
Use the current campaign harness or `lab/discovery/prop_survivor_scoring.py`
according to the owning plan. Vendor-free engine regression is
`tests/core/test_mc_synthetic_engine.py`.

## P4 — Firm application / sizing

Firm rules define the objective and failure clock. `core/firm_rules.py`,
`core/mc/preflight.py`, and `core/dd_geometry.py` own rules and engine support;
the campaign owns the bound population, replay, composition policy and statistical
design. [prop_envelope_default.md](ops/prop_envelope_default.md) supplies the
standing envelope. P5 owns live quantities; `ops/cli.py` is historical tearsheet-only.

The [four-firm program](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md)
and its dated falsifier remain distinct from the bounded Select attempt.
[STATE](STATE.md) tracks that obligation; the Track B owners above govern execution.

## P5 — Live execution rail (c1) — BUILT · currently DISARMED

Python signal daemon → Python listener/sizing host → CrossTrade → Tradovate.
See [listener deployment](deploy/c1_rail/README.md),
[daemon deployment](deploy/c1_signal_daemon/README.md), and
[the AGENTS.md posture](AGENTS.md#live-execution-posture) for operating boundaries.
The account's existence, conditional candidate eligibility, and deployed-book
authorization are separate facts. `nautilus_trader` remains research-only.

**Qualification (Track B, offline).** `ops/c1_rail/qualification/` is the
fixed-book qualification machinery — contracts, panel and replay, adjudication,
evidence and seals — with no admission or live authority. Its `execution/`
subpackage is the separately installed protected service (supervisor, worker,
independent G5 verification, signing) that implements the protected execution
boundary for staged TEST_ONLY qualification on Linux; complete E1 remains under
development. `deploy/qualification/bootstrap.py` is its isolated-Python role
launcher and [`tools/qualification_verification/`](tools/qualification_verification/README.md)
the disposable Ubuntu host. The three `.github/workflows/qualification-*.yml`
workflows collect boundary, S2 supervision and host evidence for the
coordinator's acceptance; they are evidence, never acceptance, and leave the
required merge status unchanged. The [B0 decision](docs/superpowers/plans/2026-09-19-attended-batch-qualification.md#b0-decision--2026-09-19)
retained this service over an operator-launched batch. Track B's book owner,
protection, halt, settlement and takeover modules (`book_*`, `account_close_*`)
also live in `ops/c1_rail/`; they are offline until a deployment GO.

## P6 — Monitoring — CFD estate RETIRED; venue-native M1 RESOLVED (2026-09-14)

[M1 acceptance](docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json) and its
[validator](scripts/validate_c1_monitoring_acceptance.py) own monitoring maturity;
status is `RESOLVED` since the [A7/A8 record](docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md#a8--signed-acceptance-deployed-re-bake-verified-2026-09-14).
`RESOLVED` satisfies only the arming interlock's M1 condition: `dry_run=false`
still needs the separate operator GO, and no production feed is selected.

[Q-MONSURF-1](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md) distinguishes
registration-gated idle monitoring, fill-gated capture, and the elective observer.
Their actual wake conditions are on [STATE's forward board](STATE.md#scheduled-forward-triggers).
`ops/sentinel/` supplies governance diagnostics; it is not venue telemetry.
The retired DXTrade/manual-CFD monitoring estate is historical evidence.

## X — Governance / discipline cross-cut — LIVE throughout

| Concern | Authority / entry point |
|---|---|
| Import boundaries | `scripts/check_boundaries.py`; [REPO_MAP](REPO_MAP.md) |
| Source and data integrity | Hash manifests; [scripts README](scripts/README.md) |
| Decision, budget, provenance and correction rules | [Operational rules](docs/operational_rules.md), [methodology](docs/methodology/README.md) |
| Blocking checks vs report-only diagnostics | [gates.yml](scripts/gates.yml); `make check` / `make audit` |
| Recorded results and future work | Owning campaign/closure; [STATE](STATE.md) for priority and obligation pointers |

## Data stores — where bytes actually live

| Store | Use / integrity |
|---|---|
| `core/data/tv_exports/cme/` | Private CME trade exports, hash-pinned; campaign-specific binding still required |
| `core/data/bar_data/` | Frozen private panels; retained but not regenerable |
| `core/data/external/` | Exogenous research series; SHA256SUMS |
| `core/strategies/` | Catalog/CARD stubs and private archived sources; source/port manifests |
| `lab/analysis/<theme>/<slug>/` | Campaign evidence and active harnesses; [catalog](lab/CATALOG.md) owns discovery |
| `discovery_manifests/` | Committed search contracts/status; commitment is the pin |
| `ops/data/` | Retained reconciliation records |
| Private DBN cache | Historical request-keyed Databento pulls; gitignored; not a live acquisition path |
| [lab/ARCHIVED.json](lab/ARCHIVED.json) | Removed-path inventory and preservation provenance |

No canonical CFD feed remains. Historical figures keep their original provenance;
new data or a new venue does not silently inherit their claims.
