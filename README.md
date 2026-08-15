# First Passage

Research + operational layer for a futures prop-trading program: discover,
validate, and deploy automated futures strategies at four automation-friendly
prop firms. There is currently **no live execution surface** — the c1 rail
(ruled host→listener→CrossTrade→Tradovate; Python-native signal host per S2;
daemon Fly app warm with `emit_enabled=false` per S2b build GO) is built and
**disarmed** at the incumbent eval (S1).
Live-execution posture is owned by [`CLAUDE.md`](CLAUDE.md) §Live-execution
posture and is deliberately NOT restated here (Rule 7). What is actually turning
today: [`PIPELINES.md`](PIPELINES.md).

## Source of truth

This repo is the source of truth for locked parameters, risk controls,
methodology, governance, and operational records. The former Notion surface is
retired/read-only; its durable content was migrated in-repo. Per Rule 0
([`docs/rule_0.md`](docs/rule_0.md)), when prior docs or a retired mirror
disagrees with production code, the code wins — flag the skew and resync.

Start here — five root docs, each with one job (no fact is restated across
more than one; see [`docs/operational_rules.md`](docs/operational_rules.md)
Rule 7 for the canonical-owner table):

- [`CLAUDE.md`](CLAUDE.md) — architecture, CLI usage, Strategy Reference table,
  Protection spec, and the Key Principle (Pine Script is source of truth for
  strategy parameters)
- [`REPO_MAP.md`](REPO_MAP.md) — the static layer map: which of `core / lab /
  ops` (+ root-resident governance) owns a given path, and the import-boundary
  contract `scripts/check_boundaries.py` enforces
- [`PIPELINES.md`](PIPELINES.md) — the dynamic companion to REPO_MAP: what is
  actually turning right now (one active research pipeline; the portfolio /
  firm / execution pipelines are locked-idle or retired)
- [`STATE.md`](STATE.md) — the open-threads + forward-obligation register:
  dormant cross-session investigations and the forward-trigger board (next
  dated review 2026-08-08)
- [`docs/SESSIONS.md`](docs/SESSIONS.md) — the session-by-session narrative;
  its top entry carries the live Open/next

Governance and decision records:

- [`docs/operational_rules.md`](docs/operational_rules.md) — the canonical-owner
  table (which doc owns which fact) and the doc/code skew-audit discipline
- [`docs/governance/INDEX.md`](docs/governance/INDEX.md) — compact governance
  and routine-workflow entry point
- [`docs/adr/`](docs/adr/) — immutable architecture decision records
- [`docs/briefs/INDEX.md`](docs/briefs/INDEX.md) — open/dormant question roster;
  individual briefs include both open and retained closure records

The former Notion surface was **retired 2026-06-12** and its pages are dead
(404). Do not chase the old URLs — every page ID resolves through one map, which
records where each was archived in-repo and which file is now canonical:
[`docs/governance/notion-redirect-map.md`](docs/governance/notion-redirect-map.md).
The five pages this README used to link (Command Center, Portfolio MC Lock
Details, Strategy Lock Reference, Per-Firm Broker Matrix, Operating Procedures)
are all covered there, archived under `docs/ltm/notes/archive/notion/`.

## Locked strategy book (legacy — CFD/challenge era, no live venue)

Guardian Gold, Striker DJ30, Aegis USDJPY, and Striker NAS100 are **LOCKED on
the parameter axis**, but the CFD/challenge era they were built for is
**closed** — see [`CLAUDE.md`](CLAUDE.md)'s Live-execution posture. The table below is the **human-readable record** of locked sizing cells; live
authority is `core/dd_protection.py` (`BASE_RISK`) and `core/firm_rules.py`
(`_BASE_RISK`), with Pine canonical for strategy behavior — there is **no
mechanical parameter-mirror gate** (the `params.toml` hub and
`scripts/validate_params.py` were retired 2026-08-03,
[ADR](docs/adr/2026-08-03-params-toml-gate-retirement.md)). The two Striker legs'
futures editions (MYM/MNQ) **were** the c1 book until 2026-08-04, when both were
withdrawn from the eval deployment
([ADR](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md)); their code
path is deliberately untouched (`ops/c1_rail/c1_sizing_host_reference.py` still
consumes `BASE_RISK["Striker"]` / `BASE_RISK["Striker NAS100"]` via `LEG_MAP`),
lifecycle stays `AUTHORIZED · MECHANISM @ 1.00×` (venue-fit is not decay), and the
rail is retained warm and **disarmed** at the incumbent eval ([`S1 ADR`](docs/adr/2026-08-07-loop-s1-environment-ratification.md)). Capital *authorization* is a
separate, revocable lifecycle —
[`docs/methodology/strategy_lifecycle.md`](docs/methodology/strategy_lifecycle.md).
Versions, risk %, contractValue, and lock dates live in one gated place: the
[`CLAUDE.md`](CLAUDE.md) Strategy Reference table and the per-strategy
[`core/strategies/*/LOCK.md`](core/strategies/) files.

DD protection (the live rule, consumed by c1) and the historical MC anchor
are **not** restated here — see the gated CLAUDE.md "Protection" block and
[`docs/mc_anchor_history.md`](docs/mc_anchor_history.md).

## Portfolio MC (historical — CLI retired)

> **The `portfolio_mc` CLI no longer runs.** Substrate Phase 3 retired the
> Pepperstone executable anchor (2026-07-24); `PANELS_BY_BROKER` is empty by
> code, so every former invocation exits 1 with *"no registered broker
> panel"* on any machine. The MC anchor survives as a **historical record**,
> not a re-runnable command — see [`docs/mc_anchor_history.md`](docs/mc_anchor_history.md).

Engine correctness is checked vendor-free, against synthetic fixtures and
planted defects:

```bash
python -m pytest tests/core/test_mc_synthetic_engine.py tests/core/test_planted_defects.py
```

**There is no canonical CFD feed** — Pepperstone (the last one) was retired
2026-08-02 along with its `core/data/tv_exports/` bytes; both OANDA and
Pepperstone are tombstoned, not superseded. The live canonical feed is
**CME futures TV exports** (`core/data/tv_exports/cme/`) — see CLAUDE.md's
vendor-data integrity gate for the manifest/hash discipline.

## Public-clone note

Vendor-licensed data, Pine strategy source, and executable ports of locked
strategy logic are deliberately **not committed** (each hash-pinned by a tracked
manifest; data-dependent tests skip cleanly when they are absent) — the canonical
statement and integrity gates live in [`CLAUDE.md`](CLAUDE.md) §Public-clone posture.
