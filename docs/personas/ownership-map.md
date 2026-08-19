# Persona Ownership Map

Maps the repo's own contents onto the persona hierarchy (`docs/personas/INDEX.md`), so any future
decision, investigation, or new artifact has a clear first-line owner without re-deriving one from
scratch. Three layers, filled in incrementally — see
[the phased plan](../superpowers/plans/2026-08-19-ownership-map-plan.md) for what's done vs. deferred.

**"Owner" here means first-line reviewer/delegate, not modification authority.** A locked file
(`core/dd_protection.py`'s constants, Pine source) still has an owner in this map — that owner is
who investigates and routes questions about it, not who is allowed to edit it. Locked-parameter
authority stays exactly where the existing doctrine puts it (CLAUDE.md §Key Principle,
`docs/methodology/strategy_lifecycle.md`).

## Layer 1 — Directory skeleton (this file, Phase 1)

One row per top-level directory/subdirectory, primary + secondary persona, and the one-line reason.
Built from the repo's own already-enforced 4-layer boundary (`scripts/check_boundaries.py`) — this is
scaffolding that already existed, not an invented structure.

### `core/` — locked risk/sizing/firm-rules (Middle office home)

| Path | Primary | Secondary | Why |
|---|---|---|---|
| `dd_protection.py`, `firm_rules.py`, `dd_geometry.py`, `lifecycle.py` | Head of Risk & Sizing | — | Exact charter match: "dd_protection, the lifecycle axis, DD tier" |
| `mc/`, `portfolio_mc.py` | Head of Validation | Head of Risk & Sizing | MC calibration is a statistical-validity object (see Q-STATVALID-1), consumed by sizing |
| `bar_export_loader.py`, `csv_parser.py`, `tv_export_loader.py`, `tv_schema.py` | Head of Research | Head of Validation | Data-ingestion tooling for research; fidelity is Validation's stake (Q-DATAFIDELITY-1) |
| `data/` (vendor CSVs, frozen `bar_data/`) | Head of Research | Head of Validation | Raw research material; integrity is Validation's concern, not custody |
| `strategies/` (locked Pine + `_archive/`, MANIFEST.sha256) | Head of Research | Head of Risk & Sizing | Strategy *content* originates in discovery; authorization/lifecycle status is Risk & Sizing's |
| `historical_challenge.py` | Head of Governance | — | Challenge-era substrate, retired (terminal register, `e2`) — custodian of dead things |
| `lib/` | Head of Engineering | *(per-consumer)* | Generic shared infra; Phase 2 may split by actual import graph |

### `lab/` — research (Front office home)

| Path | Primary | Secondary | Why |
|---|---|---|---|
| `analysis/` | Head of Research | *(refined per-pursuit, Phase 2)* | The bulk of discovery/harvest campaign bodies live here |
| `CATALOG.md` | Head of Research | — | The registry of what's in `analysis/` |
| `discovery/` | Head of Research | — | S5 promotion-lane code (Q-S5CAP-1) |
| `databento_fetch/` | Head of Research | CFO | Data acquisition tooling; CFO stake is the cost-gated spend discipline |
| `research_utils/`, `tools/` | Head of Research / Head of Engineering | — | Split by content: research-specific helpers vs. generic tooling |
| `validation_selftest.py`, `conftest.py` | Head of Validation | Head of Engineering | Named for validating the lab pipeline's own correctness |
| `archive/` | Head of Governance | Head of Research | Retention/pruning custodianship, per Governance's charter |
| `data/` | Head of Research | — | Lab-local research data |

### `ops/` — operational (Front + Back split)

| Path | Primary | Secondary | Why |
|---|---|---|---|
| `c1_rail/`, `c1_signal_daemon/` | Head of Execution | CRO | Live rail; CRO visibility per the mandatory-review rule wherever live-safety is implicated |
| `sentinel/` | Head of Governance | Head of Validation | Quarterly methodology/skill-drift probe — 3rd-line-of-defense territory |
| `cli.py` (tearsheet) | Head of Engineering | Head of Execution | A reporting tool, not a decision surface |
| `instruments/` (per-instrument ledger) | Head of Governance | Head of Execution | Ledger/registry discipline; content feeds live sizing |
| `recall/` (locked-anchor recital guard) | Head of Governance | CRO | Doctrine-protection mechanism, guards against misquoting the locked MC anchor as a live claim |
| `prop_envelope_default.md` | Head of Risk & Sizing | — | Firm-rules-adjacent risk documentation |
| `data/` | Head of Execution | — | Operational (not research) data |

### `docs/` — root-resident governance (Back office home, with per-topic stakeholders)

| Path | Primary | Secondary | Why |
|---|---|---|---|
| `adr/` | Head of Governance | — | ADR discipline is the literal charter line |
| `briefs/` (Q-roster) | Head of Governance owns the index | *(per-Q, already demonstrated on 11 Qs)* | Registry custody vs. content routing are different questions |
| `pursuits/` | Head of Governance owns the registry | *(per-pursuit, Phase 2)* | Same split as briefs |
| `methodology/`, `governance/` | Head of Governance | CRO (regime-robustness-gate-class doctrine) | Doctrine/methodology-layer custodian |
| `spec/`, `superpowers/` | Head of Governance | Head of Engineering (build-planning docs) | Decision-artifact discipline |
| `notes/audits/`, `notes/sentinel/` | Head of Governance | — | Audit/sentinel-adjacent registries |
| `historical/`, `ltm/` | Head of Governance | — | Archive/retention |
| `lessons/` | Head of Governance | — | Methodology-lesson custody |
| `templates/` | Head of Governance | — | Brief-authoring discipline artifacts |
| `analytics/` | Head of Validation | — | *(unconfirmed — flagged for Phase 2 content check)* |
| `external/` | Head of Research | — | External reference material feeding harvest/discovery |
| Root: `operational_rules.md`, `rule_0.md`, `rejected_candidates.md`, `mc_anchor_history.md` | Head of Governance (registry custody) | Head of Research / Head of Validation (content) | Rules/registry custodian; content ties are strong but distinct from custody |

### `.claude/` — meta-belt (Back office, Head of Engineering home)

| Path | Primary | Secondary | Why |
|---|---|---|---|
| `skills/`, `workflows/`, `commands/` | Head of Engineering | — | The meta-belt itself; `workflows/pre-ratification-adversarial-panel.js` — the panel mechanism this whole hierarchy runs on — lives here |
| `hookify.*.md` rules | Head of Engineering | Head of Governance | Tooling artifacts that encode governance rules; the safety-adjacent ones (`locked-pine`, `locked-sizing-const`, `destructive-git`) additionally want CRO visibility |
| `settings.json`, `settings.local.json` | Head of Engineering | Head of Governance | Config, but permissions/access-control has a governance dimension |

### `scripts/` — gates + tooling (split by function, not location)

| Path | Primary | Secondary | Why |
|---|---|---|---|
| `check_*.py` gate scripts, `gates.yml`, `gate_manifest.py`, `gate_fire_log.py`, `githooks/` | Head of Governance | — | Gate-stack enforcement is the literal Q-GATESTACK-1 finding's territory |
| `dispatch_cursor.ps1`, `install_hooks.*`, `layer_bootstrap.py` | Head of Engineering | — | Cursor dispatch + repo tooling |
| `lock_event_hook.py` | Head of Governance | Head of Risk & Sizing | A gate/hook mechanism whose subject matter is locked-strategy edits |
| `cost_geometry_pregate.py` | Head of Execution | — | Cost-law pre-screen territory (TCA Analyst's staff-level charter) |
| `instrument_profiles.py` | Head of Risk & Sizing | — | Instrument-level risk config |
| `archive_lab_analysis.py`, `archive_strategy.py` | Head of Governance | — | Retention/archival tooling |
| `diff_econ_calendar.py` | Head of Research | — | Research-input tooling |
| `check_data_manifests.py` | Head of Governance (gate script) | Head of Validation (data-integrity domain) | Same custody-vs-content split as the rest of the gate cluster |

### Root files

| Path | Primary | Secondary | Why |
|---|---|---|---|
| `CLAUDE.md` | Head of Governance | CRO (the §Live-execution posture / safety invariants section is CRO's charter verbatim) | Master governance doc; custodian ≠ sole stakeholder |
| `STATE.md` | Head of Governance | — | Forward-obligation register |
| `PIPELINES.md`, `REPO_MAP.md`, `README.md` | Head of Governance | — | Repo-map/reference docs |
| `Makefile`, `pyproject.toml`, `requirements-*` | Head of Engineering | — | Build/dependency tooling |

## Layer 2 — Pursuit refinement (Phase 2, not yet run)

Fan out over all 38 `docs/pursuits/` records the same way Phase 1 of the persona-roster work fanned
out over the 11 Q-briefs from PR #53 — read each record, confirm or correct the office/persona it
inherits from the Layer-1 skeleton above, flag genuinely cross-cutting ones rather than forcing a
single owner. Most should inherit cleanly (e.g., `a3-mnq-discovery-pipeline.md` → Head of Research
via `lab/discovery/` + `lab/analysis/`; `a2-c1-rail-incumbent-eval-operations.md` → Head of Execution
via `ops/c1_rail/`) — this layer exists to catch the ones that don't, and to give every pursuit an
explicit row rather than an inherited default.

**Not run yet.** See the phased plan for scope and sequencing.

## Layer 3 — Standing classification procedure (for anything new)

New Qs, ADRs, and pursuits get created continuously — this layer is a repeatable rule, not a
one-time pass. When a new artifact doesn't cleanly inherit from Layers 1-2:

1. Read the artifact's actual content (its stated H/Aim/falsifiable question) — never classify from
   the filename or title alone.
2. Determine office: Front (discovery/execution) / Middle (risk/validation) / Back
   (governance/engineering) / Cross-office (genuinely GRAND-tier).
3. Determine the single primary Senior Manager whose charter line most directly matches the core
   question; name real secondary stakeholders only where they have actual work to do, not everyone
   tangentially related.
4. Flag `liveSafetyRelevant: true` if the artifact touches a CLAUDE.md non-negotiable safety
   invariant (`dry_run`/M1/`armed_until`) or the live c1 sizing/arming path — this earns CRO
   informational visibility, not a formal panel review, unless the artifact is itself a GRAND
   ratification or a strict-D2 STRATEGIC-tier Delete (design spec §4).

This is exactly the procedure already run once, for real, against the 11 Q-briefs opened in PR #53 —
formalized here so it doesn't need re-deriving next time.

## Change log

| Date | Change |
|---|---|
| 2026-08-19 | Layer 1 (directory skeleton) drafted. Layers 2-3 scoped, not yet executed. |
