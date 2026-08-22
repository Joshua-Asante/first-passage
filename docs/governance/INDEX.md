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
- [`deletion_ledger.md`](deletion_ledger.md) — C1–C4 deletion/attic criteria and
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
- Skill mirror check/copy: `make sync-skills-check` / `make sync-skills`.
- Session narrative: read the newest entry in
  [`../SESSIONS.md`](../SESSIONS.md); older entries are indexed at its end.
