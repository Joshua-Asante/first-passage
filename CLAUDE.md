# First Passage

## Purpose

Research + operational layer for First Passage. The mission pipeline is
**generate → evaluate → deploy → measure → update**: discover, validate, and deploy automated
futures strategies at automation-friendly prop firms
(`core/firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS`).

**Documentation exists to serve that pipeline, not to be maintained by it.** Every artifact must
pass the retention test in [`docs/operational_rules.md`](docs/operational_rules.md) §Retention.
Anything else is deleted, retrievable via
`git show pre-prune-2026-08-08:<path>` — [`Great Prune ADR`](docs/adr/2026-08-08-great-prune.md).

**ADRs are canonical for every decision.** This file carries **pointers only** — never a retelling.
Forward obligations live in [`STATE.md`](STATE.md); session narrative in
[`docs/SESSIONS.md`](docs/SESSIONS.md); prior research in [`lab/CATALOG.md`](lab/CATALOG.md) and
[`docs/briefs/INDEX.md`](docs/briefs/INDEX.md).

## Live-execution posture

**Environment:** the live incumbent `Tradeify_Select_100K` eval is the environment for **new**
strategies. The c1 rail is **built, warm, and disarmed** (`dry_run=true`) pointed at it.
**There is no live c1 book** — both Striker legs were withdrawn 2026-08-04 and stay barred.

**Safety invariants (non-negotiable):**

* `dry_run=false` may not be set while M1 is not `RESOLVED`. Gate trigger is **arm**, not send.
* Disarm must happen **before** the absolute `armed_until` expiry (a lapse-while-armed self-bricked
  the host into a crash-loop on 2026-07-31).
* Live spend needs M1 `RESOLVED` **plus** a separate operator GO. Every armed session is its own GO.
* No agent may place a trade. The weekly venue-idle token trade is **operator-placed**.
* M1 arming interlock validates the acceptance artifact via
  `validate_c1_monitoring_acceptance.validate(require_resolved=True)` (fixed
  2026-08-09, `ops/c1_rail/c1_rail_arm.py`) — a forged or status-only artifact
  fails closed.

**Account state:** not pristine — two hand-POSTed canned-payload sessions filled (B6 dry-fire
2026-07-20; SIM `CHAIN_OK` 2026-07-27), plus the weekly venue-idle token trade (operator-placed at
venue, 2026-08-12). Cumulative realized P&L is small and positive (platform-confirmed 2026-08-12;
exact account identifier and dollar figures redacted from the public tree — see the private
operational archive). `order_id` idempotency is **DISPROVEN** — every payload gets a fresh tag. No
strategy-signal fill has ever occurred.

| Standing decision | Owner ADR |
|---|---|
| Environment ratified (F2+F3); no successor migration | [S1](docs/adr/2026-08-07-loop-s1-environment-ratification.md) |
| Signal host = Python daemon → listener; TV login automation prohibited | [S2](docs/adr/2026-08-07-loop-s2-signal-host-fork.md) · [build](docs/adr/2026-08-08-s2b-signal-daemon-build.md) |
| Tradeify de-scoped for the two Striker legs (eval included); F1 open, hard-dates 11-08 | [de-scope](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) |
| Rail build + account registration GO; spend ceiling $700 | [rail GO](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) |
| M1 venue-native monitoring maturity (arming gate) | [M1](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) |
| Prop-portfolio program at four firms; §4 falsifier hard-dates **2026-11-08** | [four-firms](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md) · [withdrawal](docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) |
| Bounded sandbox-up promotion lane (the one exception to down-only automation) | [S5](docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md) |
| Challenge-era substrate retired; no `ACTIVE_FIRM` selector | [substrate](docs/adr/2026-07-22-challenge-era-substrate-retirement.md) |
| CFD estate + manual trading retired | [CFD estate](docs/adr/2026-07-11-ops-cfd-estate-retirement.md) |
| GRAND tier bound above STRATEGIC (Quintessentials; pursuit domain + intake rule) | [GRAND](docs/adr/2026-08-09-grand-tier-quintessentials-binding.md) |
| MYM1!/MNQ1! occupancy released for new non-Striker research (Striker legs stay barred) | [occupancy](docs/adr/2026-08-12-msl-mym-occupancy-release.md) |
| Persona-hierarchy review panel (Front-Office-only spawnable roster + CEO apex/CFO cross-office; Middle/Back-office functions run as mechanical gates, not personas) over GRAND ratifications + strict-D2 STRATEGIC-tier Deletes; advisory only, safety-invariant hard-block is a standalone deterministic code check | [persona hierarchy](docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md) · [Front-Office-only narrowing](docs/adr/2026-08-21-persona-hierarchy-front-office-only.md) |

⚠ **Eval bust figures remain EOD-clock lower bounds unless they cite an intraday-honest RESULTS
path.** Class-S 0.50× full+halves on the honest clock:
[`RESULTS_INTRADAY_W1`](lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md)
([W1 ADR](docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md) `Accepted` 2026-08-22 —
other decisions of record still pending as measurement).

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
* **`ops/c1_rail/`** — live rail; sizing host consumes `dd_protection` + lifecycle.
* **`ops/c1_signal_daemon/`** — S2b Python signal daemon (warm, `emit_enabled=false`); paired with
  `ops/c1_rail/` as the listener leg.

**Lab layout:** hot bodies at `lab/analysis/<theme>/<slug>/`. Closed campaigns keep
`RESULTS*` / `PREREG*` / `CARD.md` only — harnesses were pruned and are retrievable from the tag.
Open [`docs/briefs/INDEX.md`](docs/briefs/INDEX.md) and [`lab/CATALOG.md`](lab/CATALOG.md) before
searching; **an empty Grep is not evidence of no prior work** — archived bodies live in git history.
Layer roots carry pointer-only READMEs; hop table lives in [`README.md`](README.md) §Where to look.

## Strategy Reference (LOCKED legacy book — do not modify)

The four CFD-era locked strategies have **no live venue**. Live authority for sizing is
`dd_protection.BASE_RISK` / `firm_rules._BASE_RISK` — this table is the human-readable record.
The two Striker legs' futures editions (MYM/MNQ) *were* the c1 book until 2026-08-04; the code path
is deliberately untouched (`ops/c1_rail/c1_sizing_host_reference.py` still consumes
`BASE_RISK["Striker"]` / `["Striker NAS100"]` via `LEG_MAP`).

| Strategy | Instrument / TF | Risk/trade | Version | DXTrade contractValue |
|---|---|---|---|---|
| Guardian Gold | XAUUSD 15m | 0.34% | v5.5 LOCKED | 100 |
| Striker DJ30 | DJ30 15m | **0.70%** (pyramid 750%) | v4.5 LOCKED | **10** (critical — default 1 ⇒ ~7% risk) |
| Aegis USDJPY | USDJPY 15m | 1.50% | v4.3 LOCKED | default (1) |
| Striker NAS100 | NAS100 15m | **0.37%** (pyramid 1000%) | v1 LOCKED | 10 |

Strategy parameters (SL/TP/ATR/session/BE/trail) live in **Pine only** — never duplicated here;
risk% and pyramid are mirrored above from `firm_rules.py`/Pine as the human-readable record. Lock
lineage: [allocation refresh 2](docs/adr/2026-05-23-allocation-refresh-2.md).
Historical MC calibration — **99.83% pass / 0.17% bust, p99 DD 4.37%** — is **historical record, not a
live claim**; do not quote it as a current pass probability
([`docs/mc_anchor_history.md`](docs/mc_anchor_history.md)). ⚠ These three literals are **read by
`ops/recall/guard.py`** (regex, ~L100) to build the recall-sidecar denylist — reword them and the guard
stops rejecting the anchor as authority. Change the phrasing only alongside that parser. Engine regression is vendor-free:
`tests/core/test_mc_synthetic_engine.py`. Canonical feed = CME futures TV exports
(`core/data/tv_exports/cme/`); OANDA and Pepperstone are retired.

## Strategy Authorization Lifecycle

"LOCKED" splits into two **orthogonal** axes —
[ADR](docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md); canonical owner
[`docs/methodology/strategy_lifecycle.md`](docs/methodology/strategy_lifecycle.md).
A third axis (venue binding: BOOK → VENUE EDITION → DEPLOYMENT) is
[`Accepted`](docs/adr/2026-08-05-strategy-venue-binding-axis.md); registry: [`ops/venue_editions/Tradeify_Select_100K.md`](ops/venue_editions/Tradeify_Select_100K.md) (live set empty).

* **Parameter axis — `LOCKED`**: SL/TP/ATR/risk%/pyramid/Pine are immutable. Decay never
  authorizes editing these.
* **Authorization axis — revocable**: `CANDIDATE → AUTHORIZED → WATCH{-1,-2} → RETIRED` at
  **1.00× / 0.50× / 0.25× / 0.00×**, plus a durability tag `{MECHANISM | SURVIVAL-ONLY}`.

The lifecycle multiplier is a risk_pct-layer haircut, multiplicative with `DD_SCALE`
(`scaled_risk = BASE_RISK × DD_SCALE × lifecycle`). Decay is met by graded reversible de-risk fired
by a pre-registered trigger — **never re-optimization**. Automation moves authorization **down
only**, except the bounded sandbox-up lane ([S5](docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md));
retirement and full beta shutdown are operator GO/NO-GO.

**Current state:** all four legs `AUTHORIZED · MECHANISM @ 1.00×` (no `lifecycle_state.json` ⇒ code default). ⚠ **Historical:** the c1 host, while the Striker book was the deployment limb, ran at **WATCH-1 0.50×** per the rail GO ADR. That book was withdrawn 2026-08-04 — there is no live deployed sizing today. Do not read the 1.00× record as a current live haircut, or the 0.50× GO figure as a current book.

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

## Public-clone posture

**This repo is public** as of 2026-08-14
([transition ADR](docs/adr/2026-08-14-repo-public-visibility-transition.md)). Full pre-transition
development history (3000+ commits) lives privately in the archived `first-passage-archive` repo —
this repo started fresh from a single "Initial public release" commit, seeded from a remediation
pass that scrubbed the live account identifier/P&L and redacted locked-strategy parameter/backtest
detail across every tracked file that carried it (not just `LOCK.md`). Three classes stay
gitignored going forward, same as before the transition:

* **Vendor-licensed CSVs** under `core/data/tv_exports/`, `core/data/bar_data/`,
  `core/data/external/` — per-directory `SHA256SUMS` manifests are tracked.
* **Pine strategy source** (`**/*.pine`) — hashes pinned in `core/strategies/MANIFEST.sha256`.
* **Executable Python ports of locked strategy logic** — hashes in `PORT_MANIFEST.sha256`.
  New ports land gitignored + hash-pinned by default, never tracked.

Tests depending on vendor CSVs skip-if-missing. `core/data/bar_data/` is **RETAINED but FROZEN**
(CME micros only; producer pipeline dead) — panels are usable but **not regenerable**.

### Vendor-data integrity gate

After re-exporting any panel CSV, run the checker and commit the `SHA256SUMS` delta in the **same
commit** as the data change:

```bash
python scripts/check_data_manifests.py --regenerate --dry-run
python scripts/check_data_manifests.py --regenerate
```

All three active manifest dirs must be present locally before committing anything under `data/`.
The checker hashes **working-tree bytes**, matching what `sha256sum` sees on disk.

**Load-bearing gate — install the pre-commit hook once per clone:**

```bash
bash scripts/install_hooks.sh
```

(Windows cmd: `scripts\install_hooks.bat`. ⚠ PowerShell `bash` is WSL, not Git Bash — the `.sh`
files are CRLF; prefer the `.bat`.) GitHub Actions runs for real (live and green since the
2026-08-15 public transition — [`Q-GATESTACK-1`](docs/briefs/closures/Q-GATESTACK-1-closure-falsified.md)
Limb-D) and cannot re-hash gitignored bytes; CI composition is
[`gate-manifest.yml`](.github/workflows/gate-manifest.yml) (`python scripts/gate_manifest.py --tier check`;
[W5](docs/adr/2026-08-07-w5-governance-diet.md)). **CI passing is still not a
merge precondition** — `main` carries no branch protection or required checks
([`Q-GATESTACK-1`](docs/briefs/closures/Q-GATESTACK-1-closure-falsified.md) Limb-A; a ruleset packet
is named, not opened). Escape hatch `git commit --no-verify` is not the
standing path. See [manifest integrity gate](docs/adr/2026-05-10-manifest-integrity-gate.md).

### Gate composition authority

[`scripts/gates.yml`](scripts/gates.yml) via
[`scripts/gate_manifest.py`](scripts/gate_manifest.py) — pre-commit, `make check`, and
[`.github/workflows/gate-manifest.yml`](.github/workflows/gate-manifest.yml) call the
runner. **Do not hand-maintain a parallel list.** The `params.toml` hub validator was retired
([ADR](docs/adr/2026-08-03-params-toml-gate-retirement.md)); Pine remains canonical for strategy
behavior, `dd_protection.py` / `firm_rules.py` for live-sizing constants.

```bash
make validate                              # data manifests + pine
python scripts/gate_manifest.py --list     # full hard-gate roster
python scripts/gate_manifest.py --tier pre-commit
```

## Key Principle

The portfolio is LOCKED **at the parameter axis** — this pipeline manages the *operational* layer
and never touches strategy parameters. **Capital authorization is a separate, always-revocable
axis.** "Locked" means parameters are frozen, **not** that a strategy earns capital indefinitely.
