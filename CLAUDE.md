# First Passage

## Purpose

Research and operations for automated futures strategies at
`core/firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS`. The mission is
**generate → evaluate → deploy → measure → update**.

Start with [STATE.md](STATE.md) for priorities and obligations, then the owning
campaign plan for executable steps and its record for evidence. Use
[PIPELINES.md](PIPELINES.md) for handoffs and [REPO_MAP.md](REPO_MAP.md) for code.
[SESSIONS.md](docs/SESSIONS.md) is history. Direct operator instructions govern
the current task; do not infer new work or authorization from historical dispatches.

Decisions belong with their owning specification, campaign, plan or PR. Create an
ADR only for durable architecture/governance rationale or authority that needs a
distinct record under the [admission rule](docs/adr/2026-08-08-adr-ceremony-tiering.md).
ADRs are not a universal decision log. Other documents link to the owner or label a derived mirror
([Rule 7](docs/operational_rules.md)). Documentation must serve the pipeline
and pass the [retention test](docs/operational_rules.md#16-retention--an-artifact-must-earn-its-place-and-deletion-is-classified-by-execution-not-by-folder).
Removed evidence remains retrievable through [archive guidance](docs/ltm/README.md)
and [lab/ARCHIVED.json](lab/ARCHIVED.json).

## Live-execution posture

**Recorded posture:** the incumbent `Tradeify_Select_100K` eval exists; c1 is warm and **disarmed** (`dry_run=true`), with no deployed book. Daemon `emit_enabled=false`. Confirm actual host state before operational work.

- `dry_run=false` requires M1 `RESOLVED`: the gate's object is the **arm**, not the send.
- Disarm **before** absolute `armed_until` expiry; lapse-while-armed previously caused a host crash-loop.
- Live spend requires M1 `RESOLVED` **and** separate operator GO. Every armed session needs its own GO.
- **No agent may place a trade.** Weekly account-preservation trades are operator-placed; deadline in [STATE](STATE.md#scheduled-forward-triggers).
- The arming interlock calls `validate_c1_monitoring_acceptance.validate(require_resolved=True)` in `ops/c1_rail/c1_rail_arm.py`; a forged or status-only artifact fails closed.

**Account:** used, not pristine; canned-payload and weekly token trades have filled, but no strategy-signal fill has occurred. `order_id` idempotency is **DISPROVEN**; every payload gets a fresh tag. Private account figures stay private.

| Standing consequence | Owner |
|---|---|
| Incumbent environment retained; no successor migration | [S1](docs/adr/2026-08-07-loop-s1-environment-ratification.md) |
| Python daemon → listener; TV login automation prohibited | [S2](docs/adr/2026-08-07-loop-s2-signal-host-fork.md), [daemon build](docs/adr/2026-08-08-s2b-signal-daemon-build.md) |
| Withdrawn Striker editions stay barred; separate campaign expressions have conditional eval eligibility, not funded/deployment authority | [withdrawal](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md), [readmission](docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md) |
| Rail build/account registration GO; spend ceiling $700 | [rail GO](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) |
| Licensed test strategy can discharge M1 item 5 / B7 Stage 1 independently of strategy selection; no arm | [M1 addendum](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24) |
| Four-firm program falsifier remains dated 2026-11-08; Tradeify counts again | [program](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md), [F1 reversal](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md#addendum-2026-09-01--f1-reversed-a-tradeify-resting-discharge-now-counts-toward-4) |

## Architecture

`core/` owns shared engines and frozen controls; `lab/` owns research; `ops/`
owns operational services. Governance remains at the root. `lab↔ops` imports
are forbidden; `core` imports nothing from other internal layers.
[REPO_MAP.md](REPO_MAP.md) names the code owners and enforced boundary maps.

Before opening research, read [lab/CATALOG.md](lab/CATALOG.md) **In flight**,
[docs/briefs/INDEX.md](docs/briefs/INDEX.md), and the relevant instrument ledger
and rejection bar. An empty `rg` result is not evidence of no prior work:
cold stores are search-excluded, removed bodies are in history, and private
inputs are gitignored. Use catalog paths and [retrieval guidance](docs/ltm/README.md).

## Load-bearing numbers

Read [docs/load_bearing_numbers.md](docs/load_bearing_numbers.md) before quoting
prop-tier figures. Eval bust claims are EOD-clock lower bounds unless backed by
an intraday-honest RESULTS artifact; published bust/pass claims assume the
inactivity barrier is OFF. The owner records scope, exceptions, and historical
values; do not reopen the degenerate barrier-ON re-MC as a fresh finding.

## Strategy Reference (LOCKED legacy book — do not modify)

Record moved 2026-09-04 to
[`core/strategies/CATALOG.md`](core/strategies/CATALOG.md) §Locked parameter record — risk%,
pyramid, version, `contractValue`, and the Guardian/Aegis disposition. **No live venue, not a live
book;** live sizing authority is `dd_protection.BASE_RISK` / `firm_rules._BASE_RISK`, and every
other strategy parameter lives in **Pine only**.

Historical MC calibration — **99.83% pass / 0.17% bust, p99 DD 4.37%** — is **historical record, not a
live claim** ([`docs/mc_anchor_history.md`](docs/mc_anchor_history.md)). ⚠ Those three literals stay
**here**: `ops/recall/guard.py` regex-reads them from this file to build the recall-sidecar denylist,
and the first anchor-shaped match in `mc_anchor_history.md` is a *different* triple (the Q-SWAP
figures), so moving them would silently denylist the wrong numbers. Reword only alongside that parser.
Engine regression is vendor-free (`tests/core/test_mc_synthetic_engine.py`). Canonical feed = CME
futures TV exports (`core/data/tv_exports/cme/`); OANDA and Pepperstone are retired.


## Strategy Authorization Lifecycle

Parameter lock, capital authorization, and venue deployment are separate axes.
[strategy_lifecycle.md](docs/methodology/strategy_lifecycle.md) owns the lifecycle;
[venue editions](ops/venue_editions/Tradeify_Select_100K.md) owns venue binding.
The legacy book's authorization does not imply a deployed strategy.

Locked parameters are immutable. Decay permits pre-registered de-risking, never
re-optimization. Automation moves authorization down only, except the
[bounded sandbox-up lane](docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md).
Retirement and full beta shutdown require operator GO/NO-GO. Read
`core/lifecycle.py` and its state for effective multipliers; do not infer a live
haircut from historical rail operation.

## Protection

Single rule in `dd_protection.py`, consumed by the rail's sizing path. **Unused today** — no
strategy is deployed.

* **DD tier:** if `(equity − peak) / peak ≤ −0.015`, multiply the day's sizing by **0.40×**.
  Clears automatically when equity returns to peak.
* **`DD_TRIGGER` 1.5% / `DD_SCALE` 0.40× are frozen** and guarded at import
  (`_validate_protection_rule`). Change-control runs **only** through: pre-registration → re-MC →
  **both-halves** regime-robustness gate → admitting ADR.
  Lock provenance: [C2 relock](docs/adr/2026-05-08-dd-trigger-c2-relock.md) ·
  [ULP rounding](docs/adr/2026-05-10-dd-protection-ulp-rounding.md).
* **Concept-not-constant:** the mechanism is invariant; `(trigger, scale, reference_mode)` are
  per-(portfolio, firm-tier) variables —
  [ADR](docs/adr/2026-07-13-dd-protection-concept-not-constant.md).
* ⚠ The prior equity tier was deleted 2026-04-17 and **its revert triggers are LOST**.
  Reintroducing a second tier needs **fresh pre-registration**, not a lookup.


## Firm Expansion

Define firm rules in `core/firm_rules.py`, then run the
`core/mc/preflight.py` engine-support pre-flight: configuration alone does not
prove support for a drawdown clock or firm class. Every prop tier requires
`starting_balance`. New firms require an ADR, pre-flight, and re-MC when used;
a new execution feed also requires the [feed-equivalence pre-flight](docs/spec/feed_equivalence_discovery_test_LOCKED.md).

## Methodology references

- [Rule 0](docs/rule_0.md): read production sources before authoring risk-control or locked-Pine claims.
- [INQHIORI canon](docs/methodology/inqhiori-canon.md): three-loop authority and Rule 2, budget before acting.
- [Evaluation order](docs/adr/2026-08-30-evaluation-order.md): standing candidate sequence; campaign-specific amendments remain with their owners.
- [Regime robustness](docs/methodology/regime_robustness_gate.md): mandatory gate for qualifying risk-control lock changes.
- [Methodology index](docs/methodology/README.md): lifecycle, harvest, observation routing, estimation, and lessons.
- [Operational rules](docs/operational_rules.md): instrument-ledger discipline, provenance, corrections, retention, and change control.
- [Rejected candidates](docs/rejected_candidates.md): re-proposal requires new mechanism evidence, not parameter changes.

## Continuous improvement

When a correction, failed verification, or avoidable rework reveals a reusable
failure mode:

1. Record the observable failure and evidence, not a general preference.
2. Search existing tests, hooks, skills, lessons, and history before proposing
   a new rule.
3. Propose at most one durable improvement at the cheapest reliable layer:
   test → hook → skill → CLAUDE.md → ADR/lesson, as appropriate.
4. State the behavior expected to change and how that change will be verified.
5. Promote one-off feedback only when high-severity or independently recurring.
6. Do not edit standing instructions unless the user requests it.
7. Replace or consolidate superseded wording; improvement is not measured by
   instruction count.

After two failed corrections of the same issue, stop, summarize what was
learned, and restart with a cleaner prompt and explicit verification criteria.

Where each layer lives here: tests = `tests/` · hooks = [`scripts/gates.yml`](scripts/gates.yml) +
`scripts/githooks/` + `.claude/hookify.*.local.md` · skills = `.claude/skills/` · this file ·
ADR/lesson = [`docs/adr/`](docs/adr/) + [`docs/methodology/lessons/`](docs/methodology/lessons/)
(indexed in `docs/methodology/LESSONS_INDEX.jsonl`).


## Public-clone posture

This repository is public ([transition ADR](docs/adr/2026-08-14-repo-public-visibility-transition.md)).
Private history lives in `first-passage-archive`; follow [retrieval guidance](docs/ltm/README.md).
Do not commit account identifiers/P&L, vendor-licensed CSVs, Pine source, or
executable Python ports of locked strategy logic. Private sources are pinned by
`SHA256SUMS`, `core/strategies/MANIFEST.sha256`, and
`core/strategies/PORT_MANIFEST.sha256`; new locked ports follow the same policy.
Vendor-dependent tests skip when inputs are absent. `core/data/bar_data/` is
retained but frozen: usable panels, no regenerable producer.

### Vendor-data integrity gate

[Manifest integrity ADR](docs/adr/2026-05-10-manifest-integrity-gate.md) owns the
commands. Commit each re-export's SHA256SUMS delta with the corresponding change;
the checker hashes working-tree bytes. Install hooks once per clone:
`scripts/install_hooks.sh` under Git Bash/POSIX, or `scripts\install_hooks.bat`
on Windows. CI cannot hash absent private data. `git commit --no-verify` is not
the standing path.

### Gate composition authority

[scripts/gates.yml](scripts/gates.yml) and its runner own gate composition;
[scripts/README.md](scripts/README.md) owns the command entry points.
`make check` runs blocking checks; `make audit` runs report-only diagnostics.
Do not maintain a parallel gate list. `main` requires a PR and the
`skills (3.12)` status; [Q-GATESTACK-1's addendum](docs/briefs/closures/Q-GATESTACK-1-closure-falsified.md)
records the ruleset. Other path-filtered checks are not required merge checks.

## Key Principle

**Locked artifacts retain immutable parameters; research follows its own approved
campaign contract.** Capital authorization is revocable, and venue/deployment
authority is separate. Neither a parameter lock nor a research result grants capital.
