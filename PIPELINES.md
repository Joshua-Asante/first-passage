# PIPELINES — data-flow map (what moves where, and why)

Workflow companion to [REPO_MAP.md](REPO_MAP.md). [STATE.md](STATE.md) owns current
priorities, [CLAUDE.md](CLAUDE.md#live-execution-posture) owns execution safeguards,
and each campaign's implementation plan owns its executable sequence. Statuses
below describe machinery and its recorded use; they confer no authorization.

## Pipeline inventory (at a glance)

| # | Pipeline | Recorded use / next handoff | Owner layers |
|---|---|---|---|
| P1 | Discovery / research | Available; current queue #1 uses supplied strategies, not a new discovery run | `lab/discovery/`, `lab/research_utils/`, `discovery_manifests/` |
| P2 | Python → Pine codification bridge | Retired; a future crossing requires a fresh build and identity check | Historical evidence via [archive guidance](docs/ltm/README.md) |
| P3 | Legacy portfolio Monte Carlo | Legacy CLI idle; shared simulation primitives are reused by current research | `core/mc/`, `core/portfolio_mc.py` |
| P4 | Firm-specific construction / sizing | Select configuration campaign; follow the [STATE queue](STATE.md) and current plan below | `lab/analysis/c1/`, `core/mc/`, `core/firm_rules.py` |
| P5 | Execution rail | Built, disarmed; winner implementation/parity precedes deployment | `ops/c1_rail/`, `ops/c1_signal_daemon/`, `deploy/` |
| P6 | Monitoring | M1 code landed; licensed test-strategy Stage 1 is independent of P4 selection | `ops/c1_rail/c1_rail_telemetry.py`; fill-dependent monitors below |
| X | Governance | Evidence, integrity, and authority checks across every handoff | `scripts/`, `docs/`, manifests |

### Current campaign handoff

The [Select implementation plan](docs/superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md)
owns the current sequence. Its [campaign record](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#52--completed-capture-intake-and-export-provenance-2026-09-05)
owns evidence, gate dispositions, and operator decisions. Historical phase numbers
and dispatches in that record are not competing work instructions.

The plan routes bound sources through faithful sizing, shared-symbol replay and
used-account simulation, then a statistical freeze, selection, executable-winner
parity, the sole final validation, and an operator deployment decision. Consult
the plan for its precise prerequisites and stopping rules; neither complete
capture coverage nor synthetic engine tests constitute a qualified book.
Scanner work is separated from campaign delivery by the same owner.

In parallel, M1 item 5 / B7 Stage 1 can use the
[licensed test strategy](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24).
This does not discharge winner-specific parity or authorize arming.

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
| Acquire research data | `lab/databento_fetch/db_fetch.py estimate`, then cost-gated `pull` | Private local DBN cache; free estimate precedes paid pull |
| Define and bind a search | Channel intake and frozen candidate contract | `lab/discovery/register_search.py` → committed `discovery_manifests/<run_id>.json` |
| Explore | `lab/discovery/stage24_runner.py` and campaign-specific harnesses | Observations and candidate evidence, never automatic promotion |
| Evaluate | Current evaluation-order owner and [survivor-scoring preregistration](docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) | Typed verdict and evidence; `lab/discovery/prop_survivor_scoring.py` supplies scoring |
| Admit and monitor | Admitting decision and calibrated decay monitor | [Strategy lifecycle](docs/methodology/strategy_lifecycle.md), then venue/deployment gates |

### Inputs → transforms → outputs

Databento data and proxy discipline are owned by the `databento-data` skill;
candidate-generation tools by `futures-anomaly-discovery`; validation mechanics
by `strategy-validation`. Parent/micro rescaling provides realism, not independent
instrument evidence. [Campaign defaults](docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md)
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
[STATE](STATE.md) tracks that obligation; the current plan above governs execution.

## P5 — Live execution rail (c1) — BUILT · currently DISARMED

Python signal daemon → Python listener/sizing host → CrossTrade → Tradovate.
See [listener deployment](deploy/c1_rail/README.md),
[daemon deployment](deploy/c1_signal_daemon/README.md), and
[CLAUDE's posture](CLAUDE.md#live-execution-posture) for operating boundaries.
The account's existence, conditional candidate eligibility, and deployed-book
authorization are separate facts. `nautilus_trader` remains research-only.

## P6 — Monitoring — CFD estate RETIRED; venue-native M1 CODE_LANDED

[M1 acceptance](docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json) and its
[validator](scripts/validate_c1_monitoring_acceptance.py) own monitoring maturity.
Code landed does not mean RESOLVED. The licensed test strategy can supply item 5
without a selected book; operator signoff and subsequent arm GO remain separate.

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
| Private DBN cache | Request-keyed Databento pulls; gitignored |
| [lab/ARCHIVED.json](lab/ARCHIVED.json) | Removed-path inventory and preservation provenance |

No canonical CFD feed remains. Historical figures keep their original provenance;
new data or a new venue does not silently inherit their claims.
