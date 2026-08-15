# PIPELINES — data-flow map (what moves where, and why)

> **Status:** runtime **data-flow** companion to [`REPO_MAP.md`](REPO_MAP.md). REPO_MAP is the *static* layer/import contract (`core / lab / ops / governance`); this file is the *dynamic* view — how bytes actually move. **Posture lives in [`CLAUDE.md`](CLAUDE.md) §Live-execution posture (canonical) and [`STATE.md`](STATE.md) (dated obligations).** This file may carry **at most a one-line disposition per pipeline row**, each stating its own disqualifier and its owning fork/ADR. Anything longer — arming gates, spend ceilings, rung numbers, fill history, park reasons — belongs in CLAUDE.md and is a defect here.

---

## Pipeline inventory (at a glance)

| # | Pipeline | Substrate (data in) | Status | Owner layers |
|---|---|---|---|---|
| **P1** | **Discovery / research (Gen-2)** | Databento GLBX.MDP3 CME futures (parents 2010+, micros 2019+) | **ACTIVE** (research) | `.claude/skills/*`, `lab/`, `discovery_manifests/` |
| **P2** | **Codification bridge (Python→Pine)** | — | **RETIRED 2026-08-02** (retrieve via git) | ~~`lab/codification/`~~ |
| **P3** | **Portfolio construction (MC)** | Locked-strategy TV trade-lists | **IDLE** (anchor frozen; CLI not runnable) | `core/mc/`, `core/{dd_protection,firm_rules,portfolio_mc}` |
| **P4** | **Firm application / sizing** | Portfolio + prop-firm rule set | **IDLE** — legacy book has no venue; the c1 eval deployment was withdrawn 2026-08-04 | `core/{firm_rules,lifecycle}`, `ops/cli.py` |
| **P5** | **Live execution rail (c1)** | Strategy alerts → broker fills | **BUILT · DISARMED** — venue de-scoped 2026-08-04; nothing deployed; disposition = fork **F2** (2026-08-08) | `ops/c1_rail_*.py`, `ops/c1_rail/c1_sizing_host_reference.py`, `ops/c1_rail/crosstrade_payload.py`, `deploy/c1_rail/` |
| **P6** | **Monitoring (edge / decay / tail / execution)** | Live fills vs backtest counterfactual | **CFD estate RETIRED; venue-native M1 spine CODE_LANDED** | `ops/c1_rail/c1_rail_telemetry.py`, `ops/sentinel/` |
| **X** | **Governance / discipline** | Every artifact the other six emit | **LIVE throughout** | `scripts/check_*`, `docs/`, hash-pinned manifests |

The essential function of the repo is not "research → deploy" but **"research → deploy *without self-deception*."** P1–P6 are the object pipeline; **X** is the anti-degeneration layer that decides what counts as a survivor — it rides on top of all six.

**Generational note:** Gen-1 (the CFD-era `concept_intake → codification → sweep → hand-rolled validation` chain) was **retired 2026-07-11** ([ADR](docs/adr/2026-07-11-gen1-pipeline-retirement.md)); retirement removed *machinery*, never *evidence* (every `lab/analysis/**` closure dir, pre-registration, and banked K stays). Gen-2 (P1 below) exists because futures edge must be **discovered natively**, not ported — the edge-transfer gate was falsified.

---

## P1 — Discovery / research pipeline (Gen-2) — ACTIVE

The one turning pipeline. A **campaign** is one bounded run of discovery→validation→admission against a pre-registered search universe on one instrument family. Stage numbering is canonical (``discovery-campaign-template.md`` (pruned; `git show pre-prune-2026-08-08:docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`)); rules of evidence are operator-ratified ([`…discovery-campaign-defaults-ratified`](docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md)).

### Data flow

```text
DATABENTO_API_KEY (env only — never committed)
      │
      ▼  db_fetch.py estimate (free, metadata) ──▶ db_fetch.py pull (cost-gated, --max-cost ceiling)
GLBX.MDP3 ───────────────────────────────────────────────────────────────▶ local DBN cache (research venv, gitignored)
 (parents ES/NQ/YM/GC for deep 2010+ discovery;                              re-pulls hit cache, no re-bill
  native micros MES/MNQ/MYM/MGC 2019+ reserved as OOS)
      │
      ▼  Stage 2 MINE  — catch22 → STUMPY → ruptures (least-overfit tool first); outputs are OBSERVATIONS
      ▼  Stage 3 BIND K — register_search.py open  ──▶  discovery_manifests/<run_id>.json  (K frozen BEFORE any p-value)
      ▼  Stage 4 SCORE (IS)   — per-candidate edge/return series on IS window only
      ▼  Stage 5 BLOCK SIZE   — block_size from IS-return ACF (never sqrt(T)), bound before any SPA p-value
      ▼  Stage 6 CONFIRM (OOS) — §8 universe gate + temporal-consistency battery, on native-micro OOS era
      │        SPA/StepM/MCS (arch.bootstrap) · DSR≥0.95 (deflated_sharpe.py) · PBO<0.5 via CPCV (skfolio)
      │        + sign-consistency ≥5/7 · drop-top-year · regime-slice-as-test-condition · own-edge CUSUM
      ▼  Stage 7 REALISM      — GC→MGC 1:10 re-scale + native-micro fill re-parameterization (realism, NOT independence)
      ▼  Stage 8 BREADTH      — ENB / cross-leg-correlation delta vs the existing frame
      ▼  ADMIT                — strategies-never-locked lifecycle intake at CANDIDATE; ships its calibrated
                                Stage-6d CUSUM decay-monitor as its "death certificate"
```

### Inputs → transforms → outputs

| Element | What | Where |
|---|---|---|
| **Data source** | Single venue GLBX.MDP3 (CME/CBOT/NYMEX/COMEX), history to 2010-06-06; schema ladder `ohlcv → tbbo → mbp → mbo` (coarsest-that-answers first) | `.claude/skills/databento-data/` |
| **Cost gate** | Mandatory free `estimate` before every `pull`; `pull` aborts above `--max-cost` | `db_fetch.py` (`estimate`/`pull` verbs) |
| **Proxy discipline** | Parents = deep-history **discovery only**; micros (2019+) = OOS realism gate; 1:10 tick/margin re-scale mandatory before P&L; **JPY micro (M6J vs MJY + quote inversion) is UNRESOLVED — resolve before building the FX lane** | `reference/proxy-discipline.md` |
| **Candidate generation** | STUMPY (motif/discord), ruptures (change-point), tsfresh/catch22 (features), hmmlearn (regime), PySR/gplearn (symbolic) — each manufactures multiplicity at scale | `.claude/skills/futures-anomaly-discovery/` |
| **Trial-count ledger (K)** | `open` binds K + hypothesis + window **before** results (pre-registration-as-a-file); `close` records survivor p-values; **verdict is always a hand-off to the gate, never a promotion** | `register_search.py` → **`discovery_manifests/<run_id>.json`** (committed) |
| **Universe gate** | Rigorous correction consuming K + the K return-set: SPA/StepM/MCS via `arch`, DSR via `deflated_sharpe.py`, PBO/CPCV via `skfolio`. **"Do not reimplement — subtle correctness lives in the vetted library."** | `.claude/skills/strategy-validation/SKILL.md` §8 |
| **Realism** | Fast bar-level triage in `vectorbt`; fill-realism in `nautilus_trader` (**research-only — no Rithmic adapter, cannot execute**) | research venv (`requirements-research.txt`) |
| **Admission** | Survivor enters the revocable `strategies-never-locked` lifecycle at CANDIDATE, carrying a decay monitor calibrated *at admission* | [`docs/methodology/strategy_lifecycle.md`](docs/methodology/strategy_lifecycle.md), `core/lifecycle.py` |

### Ratified rules of evidence (campaign defaults, inherited by reference)

Temporal-**not**-instrument OOS axis (IS `2010–2018` parent / OOS `2019-05-06+` native micro — same order book ⇒ instrument is not an independent axis) · two-level K (campaign-local feeds SPA/StepM, program-cumulative-per-family feeds DSR; abandoned campaigns still bank K) · SPA p<0.05 + DSR≥0.95 + PBO<0.5 · temporal-consistency battery (≥⌈0.7·Y⌉ sign, drop-top-year, regime-slice-as-test, CUSUM) · decay-monitor-at-admission · per-campaign `--max-cost`. A campaign overrides a single default **only** with a stated reason in its §8 pre-registration.

### Two standing constraints on new campaigns

1. **The §8 gate is real code, but unexercised on a live survivor.** [`lab/research_utils/universe_gate.py`](lab/research_utils/universe_gate.py) wraps `arch` SPA/StepM/MCS + DSR + `skfolio` PBO/CPCV against the frozen thresholds, and [`lab/discovery/stage24_runner.py`](lab/discovery/stage24_runner.py) is the generic Stage-2/4 runner. **Caveat:** DISC-CAMP-0 (the shakedown campaign, [CLOSED FALSIFIED 2026-07-13](docs/briefs/DISC-CAMP-0-closure-falsified.md)) found 0 candidates, so Stages 5–7 exited `SKIPPED` without ever calling the gate on real data — the *wiring* is exercised, the *gate logic on a live survivor* is not.
2. **A K-budget reachability screen gates new campaigns.** Q-GATECART-1 closed FALSIFIED at Phase 0.5 (the DSR selection floor at K=3,177 sits above even the best in-house validated edge); its fork [Q-KBUDGET-1](docs/briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md) closed `RESOLVED` (2026-07-15); **D5** (NQ/MNQ intraday-momentum footprint) may proceed to campaign scoping. Standing HARD gates: HARV §R reachability attestation before `register_search open`; net-of-cost Sharpe vs the Clause-K floor at K_eff ≤ 3. **Every OTHER axis remains unfunded for the 2026-11-08 falsifier.** Screen PASS never blesses a candidate and never authorizes a Databento pull. This screen sits *before* Stage 2.

**Manifest ledger:** `discovery_manifests/` is committed (committed = the pin). Read the per-manifest `status` field, not the file count — **open manifests do not bank K** (2026-07-31 ORB-MNQ ruling).

---

## P2 — Codification bridge (Python → Pine) — RETIRED 2026-08-02

**Was:** the only Python→Pine translator (survivor spec → scaffold → emitted `.pine` → identity-checked against the Python reference → hand to P5).

**Status:** **RETIRED** by operator ruling 2026-08-02, superseding the 2026-07-11 do-not-delete park. Bytes retrieve via git history. Pine remains the execution language of the P5 rail, so a future survivor still needs a Python→Pine crossing with an identity check (the Aegis→6J 129/129 pattern) — but that is a **fresh build against the then-current survivor format**, not a revival of this bridge.

---

## P3 — Portfolio construction (Monte Carlo) — IDLE (anchor frozen)

**Purpose:** turn survivor trade-lists into an allocation and a bust-probability estimate. This is the legacy locked-portfolio MC; its anchor is frozen as a historical record.

**Data flow:**

```text
core/data/tv_exports/cme/*.csv                 (backtest trade-lists, hash-pinned)
      │  csv_parser.py / tv_export_loader.py / tv_schema.py   (parse → internal trade objects)
      ▼
core/mc/ingest.py     (TV ingestion + panel construction — week-block panels)
core/mc/simulation.py (deterministic paths + seeded joint week-block bootstrap)
core/mc/modes.py      (configs, reporting, orchestration, CLI)  ── portfolio_mc.py is a thin facade
      │   consumes:  core/firm_rules.py    (prop-firm bust lines / targets — defines "bust")
      │              core/dd_protection.py (drawdown control — literals owned there / CLAUDE.md §Protection; consumed by c1)
      │              core/lib/{correlation,regime_bootstrap,nonlinear,mvd,tearsheet}.py
      ▼
MC anchor (pass% / bust% / p99 DD%) + bust-probability distribution
```

⚠ **Not runnable on demand.** The executable anchor was retired 2026-07-24 (substrate Phase 3); `PANELS_BY_BROKER` is empty by code, so `portfolio_mc.py` and `lab/analysis/time_to_pass.py --regime-check` exit 1 with *"No registered broker panel"* on any machine. Engine correctness now lives in `tests/core/test_mc_synthetic_engine.py` (vendor-free). Anchor numbers + provenance: [`docs/mc_anchor_history.md`](docs/mc_anchor_history.md).

**Note:** tail risk here is largely a *construction-time* property (the shared-mechanism common-mode tail, Q-DECAY-1) — not something P6 can detect at runtime.

---

## P4 — Firm application / sizing

**Purpose:** map a portfolio onto a specific prop firm's rule set and produce position sizing + a GO/NO-GO. "Bust" is *defined* by the firm rules, so this is part of the objective function, not a thin deployment target.

**Data flow:** `core/firm_rules.py` (firm constants) + `core/lifecycle.py` (authorization ladder → `get_effective_multipliers`) + `core/dd_protection.py` (risk_pct layer) → firm-gate / sizing law. The continuous-lot `ops/accounts.py` + `cli.py lots` surface was **retired** (substrate Phase 2); the live quantity path is **P5**.

**Two tracks, one surface:**

- **Legacy book — IDLE.** No live account; the CFD/challenge era is closed. Lifecycle Phase-2 remains open on the Call-4 beta-cohesion diagnostic.
- **Prop-portfolio program — the live track.** A greenfield construction+application flow for candidates targeting `core/firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS` ([ADR](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md)). Its scoring harness (`lab/discovery/prop_survivor_scoring.py`, G0–G8) is **built ahead of any candidate**, and the survivor-scoring gate is **frozen** ([pre-registration](docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) — bust ≤3.0% at the $100K common band; discharge = ≥2 of 4 firms). Inputs landed: [`ops/prop_envelope_default.md`](ops/prop_envelope_default.md) + `core/dd_geometry.py` (venue-agnostic drawdown-mechanism registry). Rail build + account registration landed under the c1 GO (P5); the deployment limb was **superseded 2026-08-04** and no live-spend path exists — $208 of the $700 ceiling is sunk against a venue de-scoped as a deployment target, and whether the programme regains an execution surface is fork **F3** (08-08). Program demotes to research-only if no candidate clears any tier by **2026-11-08**.

---

## P5 — Live execution rail (c1) — BUILT · currently DISARMED

**Built path** (GO 2026-07-17; deployment limb superseded 2026-08-04): ruled **Python signal daemon** (S2 / S2b; warm, `emit_enabled=false`) → always-on Python listener (Option C) → CrossTrade Cloud → Tradovate on one `Tradeify_Select_100K` eval; historical TV→listener path remains on record. Attended-only; spend ceiling $700 ($208 sunk). **No strategy is deployed** — both Striker legs were withdrawn from the c1 eval deployment 2026-08-04 ([ADR](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md)); the rail is retained warm/disarmed at the incumbent eval ([`S1 ADR`](docs/adr/2026-08-07-loop-s1-environment-ratification.md); F2+F3 ruled). The GO ADR's rail build, account registration, attended-only posture, $700 ceiling and arm gate are untouched and stand. Daemon: [`deploy/c1_signal_daemon/`](deploy/c1_signal_daemon/README.md) · [build ADR](docs/adr/2026-08-08-s2b-signal-daemon-build.md).

**Status and safety invariants are owned by [`CLAUDE.md`](CLAUDE.md) §Live-execution posture** — including the fill history, the arm-gating on M1 `RESOLVED`, and the disarm-before-`armed_until` rule. Operating procedure: private archive (`docs/notes/rail_build/` excluded from the public seed); public owners are the [GO ADR](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) and [`deploy/c1_rail/README.md`](deploy/c1_rail/README.md). M1 gate owner: [`M1 ADR`](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md).

**Repo touchpoints:** `ops/c1_rail/c1_rail_listener.py`, `ops/c1_rail/c1_rail_http_server.py`, `ops/c1_rail/c1_sizing_host_reference.py`, `ops/c1_rail/crosstrade_payload.py` (the payload contract), `ops/c1_rail/c1_rail_telemetry.py` (M1 EventLedger), `ops/c1_rail/c1_rail_arm.py`, `deploy/c1_rail/`. `nautilus_trader` remains **research-only**.

**Historical alternative (never built):** `TradingView → CrossTrade → NinjaTrader 8 → Bulenox (via Rithmic)` — dormant under R6 NO-GO; not the c1 path.

---

## P6 — Monitoring — CFD estate RETIRED; venue-native M1 CODE_LANDED

**Purpose:** watch live execution for fill quality, edge-captured ratio, edge decay, and tail.

**Disposition:** the DXTrade/manual-CFD estate is **RETIRED** ([ADR](docs/adr/2026-07-11-ops-cfd-estate-retirement.md)) — `ops/live_journal/`, `ops/regime_gate/`, `scripts/run_ecr.py`, and `make ecr` are gone (retrieve via `git show`). Provenance kept under `ops/data/reconciles/` and `docs/notes/audits/` (issue #54 ULP survey relocated from `ops/data/audits/` 2026-08-03). Surviving adjacent governance monitor: `ops/sentinel/` (`make sentinel`).

**Venue-native rebuild (c1):** [ADR](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) `Accepted` 2026-07-23. **M1 spine CODE_LANDED** in `ops/c1_rail/c1_rail_telemetry.py` — structured events, honest transport, attested evidence reconcile, confirmed-base interlock. M1 `RESOLVED` gates arming (see CLAUDE.md); M2/M3 remain fill/data-dependent. **Do not restore the DXTrade-shaped engine.** Q-NAS-ECR-1 stays PARKED-DORMANT; its release condition (first live fill) is **unreachable** — ADR [2026-08-04](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) §6 records that the first live fill never happens and names the Q-NAS-ECR successor among five threads stranded with no live source anywhere in the estate. Any re-triage depends on fork **F3** (successor venue, 2026-08-08) / `Q-MONSURF-1`, and per the thread's own dormancy flag a re-point to a different venue is **not type-preserving** and needs a fresh Pre-Q, not an edit.

---

## X — Governance / discipline cross-cut — LIVE throughout

Rides every pipeline; this is the "without self-deception" layer, and it is demonstrably load-bearing.

| Function | Mechanism |
|---|---|
| **Layer/import contract** | `scripts/check_boundaries.py` (source of truth: [`REPO_MAP.md`](REPO_MAP.md)) |
| **Reproducibility / hash-pinning** | `core/**/SHA256SUMS`, `core/strategies/{MANIFEST,PORT_MANIFEST}.sha256`, `scripts/check_data_manifests.py` + `scripts/check_pine_manifest.py` (note the plural on the first), `scripts/parse_bar_export.py` |
| **Locked-constant integrity** | `scripts/verify_lock_anchors.py` (plus `scripts/check_pine_manifest.py` for Pine) — (`ast.Constant` RHS; `scripts/verify_lock_anchors.py` requires that shape — the `validate_params` hub retired 2026-08-03 with `params.toml`, ADR `2026-08-03-params-toml-gate-retirement`) |
| **Decision artifacts** | `docs/adr/`, `docs/briefs/` (+ `check_brief.py`), `docs/methodology/`, `docs/spec/`, registers ([`operational_rules.md`](docs/operational_rules.md), [`rejected_candidates.md`](docs/rejected_candidates.md), [`mc_anchor_history.md`](docs/mc_anchor_history.md), [`rule_0.md`](docs/rule_0.md), [`SESSIONS.md`](docs/SESSIONS.md)) |
| **Path / skill liveness** | `scripts/check_path_liveness.py`, `scripts/check_skill_refs.py`, `scripts/check_root_doc_liveness.py`, `scripts/check_lab_path_relocation.py` (WARN — docs cite relocated `lab/…` tails; `make lab-path-relocation`; not in `gates.yml`), `scripts/sync_skills.py` |
| **Pine pre-flight** | `scripts/pine_check.py`, `scripts/pine_lint.py` |
| **Three-loop authority** | OODA (tactical) / INQHIORI (structural) / The Algorithm (strategic) — subsystem/track/tier Deletes require STRATEGIC-LoR (operator) |
| **Build entry points** | `make check` — the aggregate gate; read the `check:` target in `Makefile` for its current member list, which is authoritative and is deliberately not mirrored here. Also: `make test` / `make test-ops`; `make sentinel` |

---

## Data stores — where bytes actually live

| Store | Content | Pinned? |
|---|---|---|
| `core/data/tv_exports/cme/` | **The live canonical feed** — CME futures backtest trade-lists (the P3 inputs; 6J/MGC/MYM/MNQ) | per-dir `SHA256SUMS` |
| `core/data/bar_data/` | Frozen CME micros only (`6J_M15`, `MNQ_M15`, `MYM_M15`). ⚠ **FROZEN — usable but not regenerable** (Pepperstone producer retired 2026-08-02). CFD-era panels + `tv_exports/candidates/` deleted 2026-08-03 ([ADR](docs/adr/2026-08-03-bar-data-cfd-and-candidates-retirement.md) · `tombstone` (pruned; `git show pre-prune-2026-08-08:docs/ltm/notes/2026-08-03-bar-data-cfd-candidates-tombstone.md`)). Micros restore path: same offline copy family as the `Pepperstone tombstone` (pruned; `git show pre-prune-2026-08-08:docs/ltm/notes/2026-08-02-pepperstone-data-tombstone.md`) + the 2026-08-03 CFD backup | `SHA256SUMS` |
| `core/data/external/` | Exogenous series for mechanism/decay research (COT gold, COR3M, DSPX, S5FI, sector SPDR) | `SHA256SUMS` |
| `core/strategies/` | Hot: `CATALOG.md` + `*_CARD.md` stubs; cold Pine + LOCK/CHANGELOG/CANDIDATE under `_archive/` | `MANIFEST.sha256` / `PORT_MANIFEST.sha256` (archive paths) |
| **`discovery_manifests/`** | Gen-2 pre-registration manifests (`<run_id>.json`) — **committed** for auditability | committed = the pin |
| `ops/data/` | `audits/`, `reconciles/` | — |
| DBN cache | Databento pulls, keyed by request params | **gitignored** (research venv) |

**Retired feeds:** OANDA + Dukascopy left the active manifest contract in substrate Phase 5 (`tombstone` (pruned; `git show pre-prune-2026-08-08:docs/ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md`)); **Pepperstone left it 2026-08-02 with the feed itself** ([ADR](docs/adr/2026-08-02-pepperstone-feed-retirement.md) · `tombstone` (pruned; `git show pre-prune-2026-08-08:docs/ltm/notes/2026-08-02-pepperstone-data-tombstone.md`)); **CFD-era `bar_data` panels + `tv_exports/candidates/` deleted 2026-08-03** ([ADR](docs/adr/2026-08-03-bar-data-cfd-and-candidates-retirement.md) · `tombstone` (pruned; `git show pre-prune-2026-08-08:docs/ltm/notes/2026-08-03-bar-data-cfd-candidates-tombstone.md`)). There is **no canonical CFD feed** — historical CFD-era numbers keep their provenance labels and gain no successor.
