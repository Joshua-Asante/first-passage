# First Passage agent instructions

## Purpose

Research and operations for automated futures strategies at
`core/firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS`. Mission:
**generate → evaluate → deploy → measure → update**.

Start with [STATE.md](STATE.md) for priorities and obligations, then the owning
campaign plan (steps) and record (evidence); [PIPELINES.md](PIPELINES.md) covers
handoffs, [REPO_MAP.md](REPO_MAP.md) code, [SESSIONS.md](docs/SESSIONS.md) history.
Direct operator instructions govern the current task; do not infer new work or
authorization from historical dispatches.

This is the only agent instruction file; a dated record's `CLAUDE.md §X` means
`AGENTS.md §X` ([charter addendum](docs/adr/2026-07-16-root-doc-charter-dedup.md#addendum-2026-09-20--the-agent-constraints-root-is-agentsmd-claudemd-retired)).
The [surface-allocation ADR](docs/adr/2026-07-14-cc-cursor-surface-allocation.md) owns
seats, the committed-handoff rule and escalation-lane triggers
([M-26 … M-48](docs/methodology/lessons/methodology_lessons.md) hold the evidence).

Decisions live with their owning specification, campaign, plan or PR; ADRs follow the
[admission rule](docs/adr/2026-08-08-adr-ceremony-tiering.md); other documents link the
owner or label a derived mirror ([Rule 7](docs/operational_rules.md)). Documents must
serve the pipeline and pass the [retention test](docs/operational_rules.md#16-retention--an-artifact-must-earn-its-place-and-deletion-is-classified-by-execution-not-by-folder);
removed evidence is retrievable via [archive guidance](docs/ltm/README.md) and
[lab/ARCHIVED.json](lab/ARCHIVED.json).

## Output efficiency

Use the fewest words that meet the objective in text, code, tool calls and records.
No preamble, recap, filler or restated context; link the owner instead. Never trade
away correctness, required confirmations or honest verification reporting.

A ruling, GO, acceptance or record grants only what it states; anything unstated is
not granted. Do not append "no X granted" disclaimers. This does not cover limits on
how a verdict may be read (e.g. a closure's negative-scope section); keep those.
Operator direction 2026-10-02.

## Live-execution posture

**Recorded posture:** the incumbent `Tradeify_Select_100K` eval exists; c1 is warm and **disarmed** (`dry_run=true`) with no deployed book; daemon `emit_enabled=false`. Confirm actual host state before operational work.

**Data source (operator report 2026-09-10):** Databento is [retired](docs/adr/2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento) and unsubscribed; no replacement is approved; daemon emission stays blocked.

- `dry_run=false` requires M1 `RESOLVED`: the gate's object is the **arm**, not the send.
- Disarm **before** absolute `armed_until` expiry; lapse-while-armed previously caused a host crash-loop.
- Live spend requires M1 `RESOLVED` **and** separate operator GO; every armed session needs its own GO.
- **Agents may place orders, exit positions and cancel orders when directed by the operator**, including through computer use ([operator amendment 2026-09-30](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-30b)); arming, live-spend and per-session operator GO requirements still apply. Weekly account-preservation trades may be operator- or agent-placed at the operator's direction; deadline in [STATE](STATE.md#scheduled-forward-triggers).
- The arming interlock (`ops/c1_rail/c1_rail_arm.py` calling `validate_c1_monitoring_acceptance.validate(require_resolved=True)`) gates only the arm helper. It checks structure, `RESOLVED` status and `operator_signoff` presence, not a signature: a status-only file fails; a complete forged `RESOLVED` file passes. The rail host's boot gate (`c1_rail_http_server.load_config`) does not check M1, so editing the `/data` config bypasses it; the host-side activation gate is owed at TB-I3 ([admission](docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md)). `--acknowledge-m1-unresolved` overrides a structurally valid unresolved artifact (operator-ratified discretion; writes an `arming_deviation` record); agents may invoke it only through the operator-act prompt ([ruling 2026-09-26](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-26)).

**Account:** used, not pristine; canned-payload and weekly token trades have filled, but no strategy-signal fill has occurred. `order_id` idempotency is **DISPROVEN**; every payload gets a fresh tag. Private account figures stay private.

| Standing consequence | Owner |
|---|---|
| Incumbent environment retained; no successor migration | [S1](docs/adr/2026-08-07-loop-s1-environment-ratification.md) |
| Python daemon → listener; TV login automation prohibited | [S2](docs/adr/2026-08-07-loop-s2-signal-host-fork.md), [daemon build](docs/adr/2026-08-08-s2b-signal-daemon-build.md) |
| Withdrawn Striker editions stay barred; separate campaign expressions are conditionally eval-eligible | [withdrawal](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md), [readmission](docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md) |
| Rail build/account registration GO; spend ceiling $700 | [rail GO](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) |
| Licensed test strategy can discharge M1 item 5 / B7 Stage 1 independently of strategy selection | [M1 addendum](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24) |
| Four-firm program falsifier remains dated 2026-11-08; Tradeify counts again | [program](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md), [F1 reversal](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md#addendum-2026-09-01--f1-reversed-a-tradeify-resting-discharge-now-counts-toward-4) |

## Architecture

`core/` owns shared engines and frozen controls, `lab/` research, `ops/` operational
services; governance stays at the root. `lab↔ops` imports are forbidden; `core`
imports no other internal layer. [REPO_MAP.md](REPO_MAP.md) maps code owners and
enforced boundaries.

Before opening research, read [lab/CATALOG.md](lab/CATALOG.md) **In flight**,
[docs/briefs/INDEX.md](docs/briefs/INDEX.md), and the relevant instrument ledger and
rejection bar. An empty `rg` result is not evidence of no prior work: cold stores are
search-excluded, removed bodies are in history, private inputs are gitignored. Use
catalog paths and [retrieval guidance](docs/ltm/README.md).

## Load-bearing numbers

Read [docs/load_bearing_numbers.md](docs/load_bearing_numbers.md) before quoting prop-tier figures.
Eval bust claims are EOD-clock lower bounds unless backed by an intraday-honest RESULTS artifact.
Published bust/pass claims assume the inactivity barrier is OFF. The owner records scope,
exceptions and historical values; do not reopen the degenerate barrier-ON re-MC as a fresh finding.

## Strategy Reference (LOCKED legacy book — do not modify)

Locked parameters: [`core/strategies/CATALOG.md`](core/strategies/CATALOG.md) §Locked
parameter record. **No live venue, not a live book;** live sizing authority is
`dd_protection.BASE_RISK` / `firm_rules._BASE_RISK`; every other strategy parameter
lives in **Pine only**.

MC calibration — **99.83% pass / 0.17% bust, p99 DD 4.37%** — is **historical record, not a
live claim** ([`docs/mc_anchor_history.md`](docs/mc_anchor_history.md)). ⚠ Keep these literals **here**:
`ops/recall/guard.py` regex-reads them from this file for its denylist; `mc_anchor_history.md`'s
first match is a *different* (Q-SWAP) triple, so moving them denylists the wrong numbers.
Reword only alongside that parser.
Engine regression is vendor-free (`tests/core/test_mc_synthetic_engine.py`). Canonical feed: CME
futures TV exports (`core/data/tv_exports/cme/`); OANDA and Pepperstone are retired.

## Strategy Authorization Lifecycle

Parameter lock, capital authorization and venue deployment are separate axes;
[strategy_lifecycle.md](docs/methodology/strategy_lifecycle.md) owns the lifecycle,
[venue editions](ops/venue_editions/Tradeify_Select_100K.md) the venue binding.

Locked parameters are immutable. Decay permits pre-registered de-risking, never
re-optimization. Automation moves authorization down only, except the
[bounded sandbox-up lane](docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md).
Retirement and full beta shutdown require operator GO/NO-GO. Read effective
multipliers from `core/lifecycle.py` and its state; do not infer a live haircut from
historical rail operation.

## Protection

Single rule in `dd_protection.py`, consumed by the rail's sizing path. **Unused today**: no
strategy is deployed.

* **DD tier:** if `(equity − peak) / peak ≤ −0.015`, multiply the day's sizing by **0.40×**.
  Clears automatically when equity returns to peak.
* **`DD_TRIGGER` 1.5% / `DD_SCALE` 0.40× are frozen** and guarded at import
  (`_validate_protection_rule`). Change-control runs **only** through: pre-registration → re-MC →
  **both-halves** regime-robustness gate → admitting ADR.
  Lock provenance: [C2 relock](docs/adr/2026-05-08-dd-trigger-c2-relock.md) ·
  [ULP rounding](docs/adr/2026-05-10-dd-protection-ulp-rounding.md).
* **Concept-not-constant:** the mechanism is invariant; `(trigger, scale, reference_mode)` are
  per-(portfolio, firm-tier) variables ([ADR](docs/adr/2026-07-13-dd-protection-concept-not-constant.md)).
* ⚠ The prior equity tier was deleted 2026-04-17 and **its revert triggers are LOST**.
  Reintroducing a second tier needs **fresh pre-registration**, not a lookup.

## Firm Expansion

Define firm rules in `core/firm_rules.py`, then run the `core/mc/preflight.py`
engine-support pre-flight: configuration alone does not prove support for a drawdown
clock or firm class. Every prop tier requires `starting_balance`. New firms require an
ADR, pre-flight, and re-MC when used; a new execution feed also requires the
[feed-equivalence pre-flight](docs/spec/feed_equivalence_discovery_test_LOCKED.md).

## Methodology references

[Rule 0](docs/rule_0.md): read production sources before risk-control or locked-Pine
claims. [Rejected candidates](docs/rejected_candidates.md): re-proposal needs new
mechanism evidence, not parameter changes. Also: [INQHIORI canon](docs/methodology/inqhiori-canon.md)
(three-loop authority; Rule 2, budget before acting) · [evaluation order](docs/adr/2026-08-30-evaluation-order.md)
(standing sequence; campaign-specific amendments stay with their owners) ·
[regime robustness gate](docs/methodology/regime_robustness_gate.md) (mandatory for
qualifying risk-control lock changes) · [methodology index](docs/methodology/README.md) · [operational rules](docs/operational_rules.md).

## Continuous improvement

During authorized work, actively notice concrete plan flaws, preventable mistakes,
recurring failures and evidenced waste; at planning, correction and completion moments
use [agent-improvement](.claude/skills/agent-improvement/SKILL.md) when such an
opportunity appears (read its source if the harness does not list it); no opportunity
means no extra reflection artifact or task. Implement and verify a local, reversible,
evidence-supported improvement that fits the current task and seat without changing
outcome or acceptance criteria; existing authorization carries forward, so do not ask
again merely because it is an improvement. This includes repairing an agent-owned
execution sequence before it fails. Bounds:

1. Authority is the task's existing authorization, bounded by the seat's grants in
   [`scripts/seat_authority.yml`](scripts/seat_authority.yml) and any authority block on
   the current card, under the surface-allocation ADR's
   [action classes](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#action-classes-and-the-authority-block).
   An improvement is never an operator act or a forbidden capability.
2. A frozen worker card stays frozen: a worker returns contradictions, scope changes
   and improvement evidence to its coordinator; other seats route out-of-scope changes
   by seat under that ADR.
3. At most one durable intervention per failure mechanism, at the cheapest reliable layer:
   source fix or test (`tests/`) → hook ([`scripts/gates.yml`](scripts/gates.yml),
   `scripts/githooks/`, `.claude/hookify.*.local.md`, harness hooks in
   [`.claude/settings.json`](.claude/settings.json)) → skill (`.claude/skills/`) →
   AGENTS.md → ADR/lesson ([`docs/adr/`](docs/adr/),
   [`docs/methodology/lessons/`](docs/methodology/lessons/), indexed in
   `docs/methodology/LESSONS_INDEX.jsonl`).
4. Retain evidence with the existing task/plan/PR/campaign owner, writing into an owner
   record only when the current card's authority block grants `governance.author` (no
   card: only an owner the direct operator instruction puts in scope); otherwise route
   evidence through the task return.
5. Promote one-off feedback into standing guidance only when high-severity or
   independently recurring.
6. Do not edit standing instructions unless the user requests it. Registering or
   changing a harness hook in `.claude/settings.json` counts: unasked, propose it;
   requested, implement it within item 1's authority.

After two failed corrections of the same issue, stop, summarize what was learned,
and restart with a cleaner prompt and explicit verification criteria — on the
escalation lane the surface-allocation ADR names, not as a third retry.

## Public-clone posture

This repository is public ([transition ADR](docs/adr/2026-08-14-repo-public-visibility-transition.md));
private history is in `first-passage-archive` ([retrieval guidance](docs/ltm/README.md)).
Do not commit account identifiers/P&L, vendor-licensed CSVs, Pine source, or
executable Python ports of locked strategy logic. `SHA256SUMS`,
`core/strategies/MANIFEST.sha256` and `core/strategies/PORT_MANIFEST.sha256` pin
private sources; new locked ports follow the same policy. Vendor-dependent tests skip
when inputs are absent. `core/data/bar_data/` is retained but frozen: usable panels,
no regenerable producer.

**Private read surface.** Agents may read the accepted book's four Pine sources and
accepted runtime ports listed in `core/strategies/BOOK_SOURCES.sha256`, in place in
the operator's primary checkout (from a worktree, by that checkout's absolute path).
Never copy them into a worktree, commit or quote their bodies or values, edit them,
or pass them to `glm_agent` or any external service
([campaign §60](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25)).

### Vendor-data integrity gate

The [manifest integrity ADR](docs/adr/2026-05-10-manifest-integrity-gate.md) owns the
commands. Commit each re-export's SHA256SUMS delta with its change; the checker hashes
working-tree bytes. Install hooks once per clone: `scripts/install_hooks.sh`
(Git Bash/POSIX) or `scripts\install_hooks.bat` (Windows). `git commit --no-verify` is
not the standing path.

### Gate composition authority

[scripts/gates.yml](scripts/gates.yml) and its runner own gate composition,
[scripts/README.md](scripts/README.md) the command entry points; do not maintain a
parallel gate list. `main` requires a PR and the `skills (3.12)` status ([Q-GATESTACK-1's addendum](docs/briefs/closures/Q-GATESTACK-1-closure-falsified.md)
records the ruleset); other path-filtered checks are not required merge checks.

## Python environment and local checks

- Use the launcher of the checkout being tested: `.\fp.ps1 doctor` before project Python work; `.\fp.ps1 python ...` for operations Python; `.\fp.ps1 test`, `test-ops` and `check` for the standard suites and gates; `.\fp.ps1 python -m pytest <paths>` for selected tests. Without PowerShell 7.3+: `python -I scripts/fp.py <command>`.
- If validation fails, diagnose it ([launcher setup](scripts/README.md#local-operations-launcher)); never silently fall back to system Python or bypass validation. Keep the separately pinned research environment separate.
- When project Python starts another Python process, use `sys.executable`, not bare `python`.
- Report the command, interpreter, tested revision or working-tree state, and actual results. Disclose any pre-existing gate failure; do not describe the complete gate suite as passing.
- Cite the printed `record.json` and keep source and Git state unchanged while a recorded check runs. A verification claim needs `status: completed`, exit zero, stable source, complete capture, valid expected reports and, where applicable, successful Docker cleanup ([record format](scripts/README.md#automatic-verification-evidence)); `not_started`, `running`, `failed` and `interrupted` are not acceptance. Never infer a pass from a record merely existing.
- For independent pytest cases, select the affected tests first, then add workers: `.\fp.ps1 --workers 2 python -m pytest <paths>`; worker count does not replace related-case coverage. Docker sequence checks use `tools/local_verification/run.ps1` and are recorded too.

## Configuration as code

Default to configuration as code for new or changed configuration, especially when
reused; apply it only to configuration the work already touches, preserving accepted
policy behavior. Define reusable objects once in a canonical source that consumers reference or
compose, never copy. Separate shared configuration, product/environment variants and
instance bindings; make overrides explicit; validate the resolved configuration where it
is consumed. Reference credentials; never embed secrets in versioned configuration.
Deployments preserve the resolved configuration's identity/version so validation and
activation refer to the same configuration.

## Key Principle

**Locked artifacts retain immutable parameters; research follows its own approved
campaign contract.** Capital authorization is revocable. Neither a parameter lock nor a
research result grants capital.
