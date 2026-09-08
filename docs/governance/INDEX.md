# Governance and workflow index

Compact entry point for repository governance and routine workflows. Canonical
facts remain with the linked owners; this page does not restate locked values.

## Governance

- [`../../REPO_MAP.md`](../../REPO_MAP.md) — layer ownership and import contract.
- [`../operational_rules.md`](../operational_rules.md) — earned operational rules
  and canonical-owner table.
- [`../rule_0.md`](../rule_0.md) — audit production sources before decisions.
- [`../methodology/README.md`](../methodology/README.md) — standing method files
  (canon, lifecycle, harvest, both-halves, …).
- [`../methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) —
  parameter lock versus revocable capital authorization.
- [`systematic-trading-lifecycle.md`](systematic-trading-lifecycle.md) —
  end-to-end research, execution, telemetry, and feedback map.
- [`deletion_ledger.md`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/governance/deletion_ledger.md) — C1–C4 deletion/attic criteria and
  restore provenance.
- [`../briefs/INDEX.md`](../briefs/INDEX.md) — open/dormant question roster.
- [`../../lab/CATALOG.md`](../../lab/CATALOG.md) — lab campaign registry (open first).
- [`../../core/strategies/CATALOG.md`](../../core/strategies/CATALOG.md) — strategy dispositions.
- [`../../ops/instruments/PROFILES.md`](../../ops/instruments/PROFILES.md) — mechanism × instrument matrix.
- [`../adr/INDEX.md`](../adr/INDEX.md) — derived ADR lifecycle index.
- [`../../STATE.md`](../../STATE.md) — cross-session open threads and forward
  obligations.

## Workflows

- Deterministic repository gates: `make check`.
- Focused tests: `make test`, `make test-ops`. (No `test-validation` — it was dropped with the Gen-1 `lab/validation/` tree, 2026-07-11.)
- Session-log preview: `make roll-sessions-dry`.
- Session-log roll: `make roll-sessions` (design:
  [`../spec/2026-06-27-session-log-rolloff-design.md`](../spec/2026-06-27-session-log-rolloff-design.md)).
- Hygiene sentinel: `make sentinel`.
- Skill deploy diagnostic (read-only, any checkout): `make sync-skills-check`.
  Explicit publication from primary `main` after review requires both
  revision and target: `make sync-skills REVISION=<reviewed-sha>
  TARGET=<explicit-destination>` (no implied home/AppData default). Being
  on `main` does not prove review.
- INDEX/CATALOG liveness census (report-only): `make sync-liveness` (or
  `make audit`). Wired [`../../scripts/gates.yml`](../../scripts/gates.yml)
  `tier: audit` — not pre-commit/`make check`/required CI. Script still exits
  0; INDEX moves stay judgment.
- Rule 7 owner lookup: `make find-owner Q=<token>`. Not a sixth index.
- Current priorities: [`../../STATE.md`](../../STATE.md), then the linked campaign
  implementation plan. Session history: [`../SESSIONS.md`](../SESSIONS.md).

## Liveness census (2026-08-22)

Pointer, not a second owner. Re-run: `make sync-liveness`.
`--apply-index` unused (reserved-close Open rows stay Open).

| limb | count |
|---|---|
| `stale_index_open` | 0 |
| `open_with_hot_closure` | 0 |
| `archive_owed_active` | 0 |

Verdict: **CLEAN** (re-confirmed 2026-08-23). Phase 5b landed this GO.

## Named-not-opened (nav leftover)

Not a sixth root doc, and not a STATE.md forward obligation — low-priority nav polish with no forcing
date. `find-owner` and Phase 5b (`sync_liveness` wired into `gates.yml`) have landed and are dropped
from this list; Phase 8 (unify `ops/` imports) was considered and correctly not done — the dual layout
is intentional ([`REPO_MAP.md`](../../REPO_MAP.md) §2.2).

- Phase 7 — ADR topic view (needs a new `AdrHeader` field + `check_adr_graph.py --regenerate-index`).
- Phase 2b — remaining CATALOG `**Verdict:**` stamps; see [`lab/analysis/README.md`](../../lab/analysis/README.md). Do not mass-stamp.
- SESSIONS keep-20 roll — `--dry-run` confirmed 2026-08-23 (keep 20 / roll 155 → `2026-Q3`); the actual roll is a separate GO.

## Identifier glossary

Prefixes name different historical series; a matching number does not establish a dependency. Current priorities remain in [STATE.md](../../STATE.md).

| Prefix | Means | Does not mean | Owner |
|---|---|---|---|
| pipeline `P1–P6` | Object pipelines in [`PIPELINES.md`](../../PIPELINES.md) | Pain-point packets P0–P10, or viable-strategy Phase A–D | [`PIPELINES.md`](../../PIPELINES.md) |
| pain-point `P0–P10` | Repo-hygiene packets | Pipeline-P or phase-letter | [`pain-point charter`](../../docs/superpowers/plans/2026-08-23-repo-pain-point-packets.md) |
| Phase A–D | Viable-strategy sequence phases | Pipeline-P or pain-point-P | [`sequence overview`](../../docs/superpowers/plans/2026-08-23-viable-strategy-sequence-overview.md) |
| `S1–S7` | Closed-loop specs | S2b daemon, or the Survive queue | [`loop-spec index`](../../docs/spec/2026-08-07-loop-spec-index.md) |
| `F1/F2/F3` | S1 environment forks | Pain-point-F or firm-class F | [`S1 ADR`](../../docs/adr/2026-08-07-loop-s1-environment-ratification.md) |
| `B6/B7` | c1 rail stages | Pipeline-P or pain-point-P | [`rail GO ADR`](../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) |
| `M1` | Venue-native monitoring maturity | Q-MONSURF M-A / M-B / M-C | [`M1 ADR`](../../docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) |
| `G0–G8` | Survivor-scoring gates | GRAND-tier G or generation-G | [`strategy-validation`](../../.claude/skills/strategy-validation/SKILL.md) |
| `Q-*` | Brief roster | Queue rows | [`docs/briefs/INDEX.md`](../../docs/briefs/INDEX.md) |
