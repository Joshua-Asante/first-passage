# First Passage

Research + operational layer for a futures prop-trading program: discover,
validate, and deploy automated futures strategies at four automation-friendly
prop firms. The incumbent eval is live (S1); there is **no deployed book** —
the c1 rail (ruled host→listener→CrossTrade→Tradovate; Python-native signal
host per S2; daemon Fly app warm with `emit_enabled=false` per S2b build GO)
is built and **disarmed** there.
Live-execution posture is owned by [`CLAUDE.md`](CLAUDE.md) §Live-execution
posture and is deliberately NOT restated here (Rule 7). What is actually turning
today: [`PIPELINES.md`](PIPELINES.md).

## Source of truth

This repo is the source of truth for locked parameters, risk controls,
methodology, governance, and operational records. Per Rule 0
([`docs/rule_0.md`](docs/rule_0.md)), when prior docs disagree with production
code, the code wins — flag the skew and resync.

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
  dormant cross-session investigations and the forward-trigger board
- [`docs/SESSIONS.md`](docs/SESSIONS.md) — the session-by-session narrative;
  its top entry carries the live Open/next

Layer roots (`core/`, `lab/`, `ops/`, `docs/`, `scripts/`, `tests/`, `deploy/`)
carry pointer-only READMEs. Open the catalog named there — do not glob a
directory to infer what is live.

## Where to look

| Need | Open first |
|---|---|
| Layer / import contract | [`REPO_MAP.md`](REPO_MAP.md) |
| What is turning | [`PIPELINES.md`](PIPELINES.md) |
| Open threads + dated obligations | [`STATE.md`](STATE.md) |
| Lab campaigns (hot vs archived) | [`lab/CATALOG.md`](lab/CATALOG.md) |
| Locked / withdrawn strategies | [`core/strategies/CATALOG.md`](core/strategies/CATALOG.md) |
| Instrument × mechanism verdicts | [`ops/instruments/PROFILES.md`](ops/instruments/PROFILES.md) · [`ops/instruments/MECHANISMS.md`](ops/instruments/MECHANISMS.md) |
| Open / dormant questions | [`docs/briefs/INDEX.md`](docs/briefs/INDEX.md) |
| Decision status | [`docs/adr/INDEX.md`](docs/adr/INDEX.md) (derived; do not hand-edit) |
| Kill / re-proposal bar | [`docs/rejected_candidates.md`](docs/rejected_candidates.md) |
| GRAND-tier pursuits | [`docs/pursuits/`](docs/pursuits/) · [`docs/personas/INDEX.md`](docs/personas/INDEX.md) |
| Gates / `make` targets | [`scripts/gates.yml`](scripts/gates.yml) · `python scripts/gate_manifest.py --list` |
| Closed-loop specs S1–S7 | [`docs/spec/2026-08-07-loop-spec-index.md`](docs/spec/2026-08-07-loop-spec-index.md) |

Governance and decision records:

- [`docs/operational_rules.md`](docs/operational_rules.md) — the canonical-owner
  table (which doc owns which fact) and the doc/code skew-audit discipline
- [`docs/governance/INDEX.md`](docs/governance/INDEX.md) — compact governance
  and routine-workflow entry point
- [`docs/adr/INDEX.md`](docs/adr/INDEX.md) — derived ADR lifecycle index
- [`docs/briefs/INDEX.md`](docs/briefs/INDEX.md) — open/dormant question roster;
  individual briefs include both open and retained closure records

## Public-clone note

Vendor-licensed data, Pine strategy source, and executable ports of locked
strategy logic are deliberately **not committed** (each hash-pinned by a tracked
manifest; data-dependent tests skip cleanly when they are absent) — the canonical
statement and integrity gates live in [`CLAUDE.md`](CLAUDE.md) §Public-clone posture.
