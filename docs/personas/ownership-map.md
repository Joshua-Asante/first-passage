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

## Layer 2 — Pursuit refinement (done 2026-08-19)

All 38 `docs/pursuits/` records read in full and classified — same Workflow fan-out pattern used for
the 11 PR-53 Q-briefs, one agent per pursuit, each confirming or correcting the office it would
inherit from Layer 1's directory skeleton.

**18 of 38 diverged from their Layer-1 default** (a1, a4, b4, b5, b6, c1, c2, c3, c5, d1, d3, d11,
d12, d13, d14, d15, d16, e1) — a real signal, not noise: the directory skeleton is a decent coarse
prior, but pursuit-level content changed the answer on nearly half the cases. Divergence clusters in
two shapes: (1) an artifact's *location* (docs/pursuits/, .claude/skills/) implied Governance/Back,
but its actual subject matter was Front/Middle (a1, a4, b4, b6, c3, c5, d3); (2) GRAND-tier's own
CFO domain line ("subscription spend, d11-d16") wins the *spend-authority* question even when the
*operational* stakeholder is a different office entirely (d11-d16) — CFO as primary, the actual
day-to-day user as secondary.

**28 of 38 are flagged cross-cutting.** That's most of the registry, and it's expected: a pursuit is
by definition a "whole commitment" (design spec §5.2's framing), which routinely touches more than
one office even when it has one clear first-line owner.

| Pursuit | Title | Standing | Office (inherited → confirmed) | Primary | Secondary |
|---|---|---|---|---|---|
| **a1** | Four-firms prop-portfolio program (umbrella) | KEEP | Back → **Front** | CIO | Head of Execution, Head of Research, Head of Validation |
| **a2** | c1 rail + incumbent-eval operations | KEEP | Front | Head of Execution | Head of Validation, CFO |
| **a3** | MNQ discovery pipeline (TNEC intake · Route A/B · CapFLOW · dense-1m/instrument/W1) | KEEP | Front | Head of Research | Head of Validation |
| **a4** | Harvest / external-mechanism intake + sourcing radar | KEEP | Back → **Front** | Head of Research | — |
| **a5** | R&D tooling lane (T2/T3/T4 gated adoption · sentinel promotion) | KEEP | Back | Head of Engineering | Head of Governance, Head of Validation |
| **a6** | Cursor-fleet worker capability | KEEP | Back | Head of Engineering | Head of Research |
| **b1** | Aegis→6J transfer lane | PARK | Front | Head of Research | Head of Execution |
| **b2** | Striker MYM reconstruction (S-MYM-ORC-02, TERMINAL lane) | PARK | Front | Head of Research | Head of Execution, Head of Governance |
| **b3** | ORB-MNQ payability line (orb_mnq · eodadv) | PARK | Front | Head of Research | Head of Execution |
| **b4** | Q-USOIL-1 (+ `usoil_regime_capture` legacy harness) | SUBTRACT | Front → **Back** | Head of Governance | Head of Research |
| **b5** | Q-FUNDPOL-1 funded-phase policy inheritance | PARK | Front → **Middle** | Head of Risk & Sizing | Head of Validation, Head of Execution |
| **b6** | Q-NAS-ECR-1 NAS100 live edge-captured ratio | PARK | Back → **Front** | Head of Execution | Head of Research, Head of Governance |
| **b7** | ICT line (PREREG-1M / Q-ICTEXP-1) | PARK | Front | Head of Research | Falsifier/Pre-Registration Analyst (executes the Q-ICTEXP-1 §9 zero-K falsifier), Head of Governance (tracks the 2026-11-08 auto-convert-to-SUBTRACT deadline) |
| **b8** | Guardian→MGC transfer lane (R7) | SUBTRACT | Front | Head of Governance | Head of Research |
| **c1** | Q-XMEM-1 cross-surface memory sidecar pilot | PARK | Front → **Back** | Head of Engineering | Head of Governance |
| **c2** | Q-SIGID-1 signal-identity gap | KEEP | Front → **Cross-office** | Head of Execution | Head of Validation, Head of Research |
| **c3** | Q-TOM-SPX-1 SPX500 turn-of-month | PARK | Back → **Front** | Head of Research | Head of Governance |
| **c4** | Q-TVCOV-1 TV intraday bar-coverage census — SUBTRACT-complete | SUBTRACT | Back | Head of Governance | — |
| **c5** | Q-MSCHAN-1 microstructure sourcing-channel (blind form) | SUBTRACT | Front → **Back** | Head of Governance | Head of Research |
| **c6** | Notion estate (frozen workspace) | SUBTRACT | Back | Head of Governance | — |
| **d1** | Repo belt — 19 version-controlled skills | KEEP | Back → **Cross-office** | Head of Governance | Head of Engineering |
| **d2** | brief-authoring (user-level skill) | KEEP | Back | Head of Governance | Head of Engineering |
| **d3** | rule-0 (user-level skill) | KEEP | Back → **Middle** | Head of Risk & Sizing | Head of Validation, Head of Governance, Head of Engineering |
| **d4** | trade-csv-reconcile (user-level skill) | MERGE | Back | Head of Governance | — |
| **d5** | mql-developer (user-level skill) | SUBTRACT | Back | Head of Governance | Head of Engineering |
| **d6** | notion-mcp-api-patterns (user-level skill) | SUBTRACT | Back | Head of Governance | Head of Engineering |
| **d7** | fxify-challenge (plugin bundle) | SUBTRACT | Back | Head of Governance | — |
| **d8** | live-execution-journal (plugin bundle) | SUBTRACT | Back | Head of Governance | Head of Execution |
| **d9** | inqhiori-algorithm (plugin bundle) | SUBTRACT | Back | Head of Governance | Head of Engineering |
| **d10** | anthropic-skills plugin duplicate set (7 skills, marker-only) | MERGE | Back | Head of Governance | Head of Engineering |
| **d11** | TradingView subscription | KEEP | Back → **Cross-office** | CFO | Head of Research |
| **d12** | databento subscription | KEEP | Back → **Cross-office** | CFO | Head of Research |
| **d13** | Fly.io subscription | KEEP | Front → **Cross-office** | CFO | Head of Execution, Head of Governance |
| **d14** | CrossTrade subscription | KEEP | Back → **Front** | Head of Execution | CFO |
| **d15** | Tradeify Select 100K account | KEEP | Back → **Front** | Head of Execution | CFO |
| **d16** | Cursor subscription | KEEP | Back → **Cross-office** | CFO | Head of Engineering |
| **e1** | First Passage program (the Aim itself) | KEEP | Back → **Cross-office** | **CEO** | Head of Governance (record custodian), CRO, CIO |
| **e2** | Already-terminal register (CFD estate, manual trading, challenge-era substrate, retired feeds, Hermes NO-GO, Bulenox/futures-prop R6) | no action | Back | Head of Governance | — |

**One correction made on review**: the classification run initially assigned e1 ("the Aim itself") to
Head of Governance — the nearest spawnable AI custodian, since CEO is never spawned. But the roster's
own charter is explicit ("CEO | Joshua | Aim..."), so e1's true primary is CEO; Governance custodies
the pursuit *record*, not the Aim it describes.

**Known rough edge, not fixed in this pass**: the `confirmedOffice` field's `Cross-office` value and
the separate `crossCuttingFlag` boolean overlap conceptually — several rows above (c2, d1, d11-d13,
d16, e1) got `Cross-office` where a single-office-with-secondaries reading might have been cleaner.
Left as-is rather than re-litigated solo; worth tightening the schema before this pattern is reused
for Layer 3 classifications going forward.

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
