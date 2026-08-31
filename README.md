# First Passage

Research + a built, **disarmed** rail; **no book is deployed**. Four
automation-friendly firms are the program target, not current activity. The
incumbent eval is live (S1). The c1 rail (ruled host→listener→CrossTrade→Tradovate;
Python-native signal host per S2; daemon Fly app warm with `emit_enabled=false`
per S2b build GO) is built and disarmed there.
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
| GRAND-tier pursuits | [`docs/pursuits/`](docs/pursuits/) (persona-hierarchy review routing retired 2026-08-31 — see [retirement ADR](docs/adr/2026-08-31-persona-hierarchy-full-retirement.md)) |
| Gates / `make` targets | [`scripts/gates.yml`](scripts/gates.yml) · `python scripts/gate_manifest.py --list` |
| Closed-loop specs S1–S7 | [`docs/spec/2026-08-07-loop-spec-index.md`](docs/spec/2026-08-07-loop-spec-index.md) |

**Status words** — these tokens do not mean English. Owners below; do not restate their values here.

| Token | Means | Does not mean | Owner |
|---|---|---|---|
| `LOCKED` | Parameter axis is frozen (SL/TP/ATR/risk%/pyramid/Pine) | Capital is authorized indefinitely | [`strategy_lifecycle.md`](docs/methodology/strategy_lifecycle.md) |
| `CANDIDATE` → `AUTHORIZED` → `WATCH` → `RETIRED` | Capital-authorization ladder (revocable; down-only plus S5 sandbox-up) | A parameter edit | same |
| `AUTHORIZED @ 1.00×` | Code default when `lifecycle_state.json` is absent | A live deployed haircut | [`CLAUDE.md`](CLAUDE.md) §Strategy Authorization Lifecycle |
| eval is live | The incumbent Tradeify eval account exists | A book is trading, or the rail is armed | [`CLAUDE.md`](CLAUDE.md) §Live-execution posture |
| four-layer | `core/` · `lab/` · `ops/` plus **root-resident** governance | A physical `governance/` directory | [`boundaries ADR`](docs/adr/2026-06-05-monorepo-layer-boundaries.md) · [`REPO_MAP.md`](REPO_MAP.md) |
| CATALOG `hot` | Body still lives under `lab/analysis/<theme>/<slug>/` | The campaign is in-flight | [`catalog-hot ADR`](docs/adr/2026-08-22-catalog-hot-vs-disposition.md) |
| CATALOG `status` | Disposition word (`ACTIVE` / `HOLD` / `FALSIFIED` / …) | A work queue | same · [`lab/CATALOG.md`](lab/CATALOG.md) |
| `ACTIVE` | Often the `status` token on a stay-hot card | In-flight / undecided / “do this next” | same |
| Survive queue | The numbered `STATE.md` rows (cap ≤5) | Every leftover name in SESSIONS | [`STATE.md`](STATE.md) · [`Survive-bound ADR`](docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md) |
| `Open / next` | Queue-led pointer on the newest SESSIONS entry | The prior leftover cluster is the work list | [`SESSIONS.md`](docs/SESSIONS.md) header |
| pipeline `P1–P6` | Object pipelines in [`PIPELINES.md`](PIPELINES.md) | Pain-point packets P0–P10, or viable-strategy Phase A–D | [`PIPELINES.md`](PIPELINES.md) |
| pain-point `P0–P10` | Repo-hygiene packets | Pipeline-P or phase-letter | [`pain-point charter`](docs/superpowers/plans/2026-08-23-repo-pain-point-packets.md) |
| Phase A–D | Viable-strategy sequence phases | Pipeline-P or pain-point-P | [`sequence overview`](docs/superpowers/plans/2026-08-23-viable-strategy-sequence-overview.md) |
| `S1–S7` | Closed-loop specs | S2b daemon, or the Survive queue | [`loop-spec index`](docs/spec/2026-08-07-loop-spec-index.md) |
| `F1/F2/F3` | S1 environment forks | Pain-point-F or firm-class F | [`S1 ADR`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) |
| `B6/B7` | c1 rail stages | Pipeline-P or pain-point-P | [`rail GO ADR`](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) |
| `M1` | Venue-native monitoring maturity | Q-MONSURF M-A / M-B / M-C | [`M1 ADR`](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) |
| `G0–G8` | Survivor-scoring gates | GRAND-tier G or generation-G | [`strategy-validation`](.claude/skills/strategy-validation/SKILL.md) |
| `Q-*` | Brief roster | Queue rows | [`docs/briefs/INDEX.md`](docs/briefs/INDEX.md) |

An empty default-grep of `lab/archive/`, `docs/ltm/`, or `core/strategies/_archive/` is not evidence the work is absent — those trees are excluded from the default index; open the catalog and Read by path ([`.cursor/rules/search-ltm.mdc`](.cursor/rules/search-ltm.mdc)). Pine sources and vendor CSVs are gitignored; CARD/LOCK stubs plus the tracked manifests are the public surface ([`CLAUDE.md`](CLAUDE.md) §Public-clone posture).

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
