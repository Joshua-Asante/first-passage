# First Passage

## Purpose

Research + operational layer for First Passage. The mission pipeline is
**generate → evaluate → deploy → measure → update**: discover, validate, and deploy automated
futures strategies at automation-friendly prop firms
(`core/firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS`).

**Documentation exists to serve that pipeline, not to be maintained by it.** Every artifact must
pass the retention test in [`docs/operational_rules.md`](docs/operational_rules.md) §16 Retention. Anything
else is deleted under a snapshot tag ([`Great Prune ADR`](docs/adr/2026-08-08-great-prune.md)).
On this public clone retrieval is `git log --follow -- <path>` — the `pre-prune-2026-08-08` tag
lives only in the private archive ([`docs/ltm/README.md`](docs/ltm/README.md)).

**ADRs are canonical for every decision.** This file carries **pointers only** — never a retelling.
Forward obligations live in [`STATE.md`](STATE.md); session narrative in
[`docs/SESSIONS.md`](docs/SESSIONS.md); prior research in [`lab/CATALOG.md`](lab/CATALOG.md) and
[`docs/briefs/INDEX.md`](docs/briefs/INDEX.md).

## Live-execution posture

**Environment:** the live incumbent `Tradeify_Select_100K` eval is the environment for **new**
strategies. The c1 rail is **built, warm, and disarmed** (`dry_run=true`) pointed at it.
**There is no live c1 book** — both Striker legs were withdrawn 2026-08-04 and stay barred.

**Safety invariants (non-negotiable):**

* `dry_run=false` may not be set while M1 is not `RESOLVED`. The gate's object is the **arm**, not
  the send.
* Disarm **before** the absolute `armed_until` expiry — a lapse-while-armed self-bricked the host
  into a crash-loop on 2026-07-31.
* Live spend needs M1 `RESOLVED` **plus** a separate operator GO. Every armed session is its own GO.
* No agent may place a trade. The weekly venue-idle token trade is **operator-placed**
  ([`STATE.md`](STATE.md) §Weekly carries the rolling deadline).
* The arming interlock validates the M1 acceptance artifact via
  `validate_c1_monitoring_acceptance.validate(require_resolved=True)`
  (`ops/c1_rail/c1_rail_arm.py`) — a forged or status-only artifact fails closed.

**Account state:** not pristine — two hand-POSTed canned-payload sessions filled (B6 dry-fire
2026-07-20; SIM `CHAIN_OK` 2026-07-27) plus the weekly token trades. Cumulative realized P&L is
small and positive; the account identifier and dollar figures are redacted from the public tree.
`order_id` idempotency is **DISPROVEN** — every payload gets a fresh tag. No strategy-signal fill
has ever occurred.

| Standing decision | Owner ADR |
|---|---|
| Environment ratified (F2+F3); no successor migration | [S1](docs/adr/2026-08-07-loop-s1-environment-ratification.md) |
| Signal host = Python daemon → listener; TV login automation prohibited | [S2](docs/adr/2026-08-07-loop-s2-signal-host-fork.md) · [build](docs/adr/2026-08-08-s2b-signal-daemon-build.md) |
| Tradeify de-scoped for the two Striker legs (eval included); F1 reversed 2026-09-01 — a Tradeify-resting discharge counts toward §4 again; hard-dates 11-08 unchanged | [de-scope](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) |
| Rail build + account registration GO; spend ceiling $700 | [rail GO](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) |
| M1 venue-native monitoring maturity (arming gate) | [M1](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) |
| Prop-portfolio program at four firms; §4 falsifier hard-dates **2026-11-08** | [four-firms](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md) · [withdrawal](docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) |
| Bounded sandbox-up promotion lane (the one exception to down-only automation) | [S5](docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md) |
| Challenge-era substrate retired; no `ACTIVE_FIRM` selector | [substrate](docs/adr/2026-07-22-challenge-era-substrate-retirement.md) |
| CFD estate + manual trading retired | [CFD estate](docs/adr/2026-07-11-ops-cfd-estate-retirement.md) |
| GRAND tier bound above STRATEGIC (Quintessentials; pursuit domain + intake rule) | [GRAND](docs/adr/2026-08-09-grand-tier-quintessentials-binding.md) |
| MYM1!/MNQ1! occupancy released for new non-Striker research (Striker legs stay barred) | [occupancy](docs/adr/2026-08-12-msl-mym-occupancy-release.md) |
| Persona-hierarchy review panel fully retired 2026-08-31 — no persona is spawnable; the generic 6-lens pre-ratification panel is unaffected | [full retirement](docs/adr/2026-08-31-persona-hierarchy-full-retirement.md) · historical: [08-19](docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md) · [08-21](docs/adr/2026-08-21-persona-hierarchy-front-office-only.md) |

## Architecture

**4-layer monorepo** ([boundaries ADR](docs/adr/2026-06-05-monorepo-layer-boundaries.md); map in
[`REPO_MAP.md`](REPO_MAP.md)): locked **`core/`** (+ backtest panels under `core/data/`),
research **`lab/`**, operational **`ops/`** (tearsheet CLI + c1 rail + sentinel), and
root-resident governance (`docs/ .claude/ .github/ scripts/`).
`scripts/check_boundaries.py` enforces the import contract (`lab↔ops` isolation; `core` imports
nothing internal).

* **`core/firm_rules.py`** — firm configs + locked `_BASE_RISK` allocations. Add new firms here.
* **`core/dd_protection.py`** — the DD rule + live-sizing authority.
* **`core/csv_parser.py`** — DXTrade CSV parser (historical).
* **`ops/cli.py tearsheet`** — the only remaining CLI command.
* **`ops/c1_rail/`** — live rail (listener leg); sizing host consumes `dd_protection` + lifecycle.
* **`ops/c1_signal_daemon/`** — S2b Python signal daemon (warm, `emit_enabled=false`).

**Lab layout:** hot bodies at `lab/analysis/<theme>/<slug>/`; closed campaigns keep
`RESULTS*` / `PREREG*` / `CARD.md` only. Open [`lab/CATALOG.md`](lab/CATALOG.md) **In flight** and
[`docs/briefs/INDEX.md`](docs/briefs/INDEX.md) before searching — **an empty Grep is not evidence
of no prior work**: pruned bodies live in git history, and `docs/ltm/` is excluded from default
`rg` (use `--no-ignore`). Hop table: [`README.md`](README.md) §Where to look.

## Load-bearing numbers

Owner: [`docs/load_bearing_numbers.md`](docs/load_bearing_numbers.md) — **read it before quoting any
prop-tier figure.** The two standing rules, in one line each:

* ⚠ **Eval bust figures are EOD-clock lower bounds** unless they cite an intraday-honest RESULTS
  path. Scope is all 7 `dd_type="trailing"` tiers, Bulenox/BluSky included.
* ⚠ **Every published bust/pass figure assumes the inactivity barrier is OFF.** The operator-placed
  weekly token trade is the mitigation, and the barrier-ON re-MC is degenerate — **do not re-open
  it as a fresh finding.**

Six figures have a second, historical value in the tree (Part A ceiling · pass floor · §4 firm set ·
venue inactivity rule · Q-RANGECOND-1 verdict · ORB-MYM headline). That doc names the live value and
its sole owner for each.

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

"LOCKED" splits into two **orthogonal** axes —
[ADR](docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md); canonical owner
[`docs/methodology/strategy_lifecycle.md`](docs/methodology/strategy_lifecycle.md). A third axis
(venue binding: BOOK → VENUE EDITION → DEPLOYMENT) is
[`Accepted`](docs/adr/2026-08-05-strategy-venue-binding-axis.md); registry
[`ops/venue_editions/Tradeify_Select_100K.md`](ops/venue_editions/Tradeify_Select_100K.md) (live set empty).

* **Parameter axis — `LOCKED`**: SL/TP/ATR/risk%/pyramid/Pine are immutable. Decay never
  authorizes editing these.
* **Authorization axis — revocable**: `CANDIDATE → AUTHORIZED → WATCH{-1,-2} → RETIRED` at
  **1.00× / 0.50× / 0.25× / 0.00×**, plus a durability tag `{MECHANISM | SURVIVAL-ONLY}`.

The lifecycle multiplier is a risk_pct-layer haircut, multiplicative with `DD_SCALE`
(`scaled_risk = BASE_RISK × DD_SCALE × lifecycle`). Decay is met by graded reversible de-risk fired
by a pre-registered trigger — **never re-optimization**. Automation moves authorization **down
only**, except the bounded sandbox-up lane ([S5](docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md));
retirement and full beta shutdown are operator GO/NO-GO.

**Current state:** all four legs `AUTHORIZED · MECHANISM @ 1.00×` (no `lifecycle_state.json` ⇒ code
default). ⚠ Historical: the c1 host ran the Striker book at **WATCH-1 0.50×** per the rail GO ADR;
that book was withdrawn 2026-08-04, so there is no live deployed sizing today — neither figure is a
current live haircut.

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

Define rules in `firm_rules.py`, then run an **engine-support pre-flight** — config alone is not
enough (falsified in production 2026-07-11 by a `daily_loss_pct: None` `TypeError`). Each firm class
needs bespoke engine branches (`bust_trailing` Bulenox, `trailing_locking` Tradeify). Every prop tier
must carry `starting_balance`. New firms need an ADR + pre-flight (+ re-MC when the run consumes that
firm's rules). A different execution feed additionally requires the feed-equivalence pre-flight
([`LOCKED spec`](docs/spec/feed_equivalence_discovery_test_LOCKED.md)).

## Methodology references

* **Rule 0 — audit-first**: [`docs/rule_0.md`](docs/rule_0.md). Read production code first when
  authoring anything touching risk controls. Extends to locked Pine.
* **INQHIORI canon** (entry point; §14 binds the three loops; §15 owns Rule 2 —
  budget before acting, ratified 2026-08-21 as an operator override ahead of its own
  evidentiary graduation gate — [Addendum](docs/adr/2026-06-16-rule-2-budget-before-acting.md)):
  [`docs/methodology/inqhiori-canon.md`](docs/methodology/inqhiori-canon.md).
* **Regime-robustness gate** (mandatory before any LOCK CANDIDATE on a `dd_protection`-class
  constant): [`docs/methodology/regime_robustness_gate.md`](docs/methodology/regime_robustness_gate.md).
* **Strategy lifecycle** · **strategy harvest** · **observation routing** · **1R estimation** ·
  **methodology lessons** · **rejected signals** — all under
  [`docs/methodology/`](docs/methodology/).
* **Operational rules** (incl. retention test + doc/code skew trigger):
  [`docs/operational_rules.md`](docs/operational_rules.md).
* **Rejected candidates** (re-proposal needs new *mechanism* evidence, not new parameters):
  [`docs/rejected_candidates.md`](docs/rejected_candidates.md).

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

**This repo is public** as of 2026-08-14
([transition ADR](docs/adr/2026-08-14-repo-public-visibility-transition.md)). Pre-transition
history (3000+ commits) lives privately in `first-passage-archive`; this repo started from a single
"Initial public release" commit after a remediation pass scrubbed the live account identifier/P&L
and redacted locked-strategy parameter/backtest detail. Three classes stay gitignored:

* **Vendor-licensed CSVs** under `core/data/tv_exports/`, `core/data/bar_data/`,
  `core/data/external/` — per-directory `SHA256SUMS` manifests are tracked.
* **Pine strategy source** (`**/*.pine`) — hashes pinned in `core/strategies/MANIFEST.sha256`.
* **Executable Python ports of locked strategy logic** — hashes in
  `core/strategies/PORT_MANIFEST.sha256`. New ports land gitignored + hash-pinned, never tracked.

Tests depending on vendor CSVs skip-if-missing. `core/data/bar_data/` is **RETAINED but FROZEN**
(CME micros only; producer pipeline dead) — panels are usable but **not regenerable**.

### Vendor-data integrity gate

Owner: [manifest integrity gate ADR](docs/adr/2026-05-10-manifest-integrity-gate.md) — it holds the
`check_data_manifests.py` flags and the per-clone hook install. Three rules to know here:

* After re-exporting any panel CSV, commit the `SHA256SUMS` delta in the **same commit** as the data
  change. The checker hashes **working-tree bytes**, so all three manifest dirs must be present.
* **Install the pre-commit hook once per clone** (`scripts/install_hooks.sh`) — CI cannot re-hash
  gitignored bytes, so this gate is local-only. ⚠ On Windows use `scripts\install_hooks.bat`:
  PowerShell `bash` is WSL, not Git Bash, and the `.sh` files are CRLF.
* `git commit --no-verify` is not the standing path.

⚠ **`main` is protected — you cannot push to it directly.** A PR is required (0 approvals) and
exactly one status check must pass: `skills (3.12)`, the
[`gate-manifest`](.github/workflows/gate-manifest.yml) job that runs
[`scripts/gates.yml`](scripts/gates.yml). `pytest` / `build` / `manifest-check` /
`validation-controls` are deliberately **not** required (path-filtered), so those staying red does
**not** block a merge. Ruleset details: the
[`Q-GATESTACK-1` closure](docs/briefs/closures/Q-GATESTACK-1-closure-falsified.md) 2026-08-19
addendum — its verdict line is stale by design (Trap #12); read the addendum, not the headline.

### Gate composition authority

[`scripts/gates.yml`](scripts/gates.yml) via [`scripts/gate_manifest.py`](scripts/gate_manifest.py)
— pre-commit and `make check` call the runner. **Do not hand-maintain a parallel list.** The
`params.toml` hub validator was [retired](docs/adr/2026-08-03-params-toml-gate-retirement.md); Pine
is canonical for strategy behavior, `dd_protection.py` / `firm_rules.py` for live-sizing constants.

```bash
make validate                              # data manifests + pine
python scripts/gate_manifest.py --list     # full hard-gate roster
python scripts/gate_manifest.py --tier pre-commit
```

## Key Principle

The portfolio is LOCKED **at the parameter axis** — this pipeline manages the *operational* layer
and never touches strategy parameters. **Capital authorization is a separate, always-revocable
axis.** "Locked" means parameters are frozen, **not** that a strategy earns capital indefinitely.
