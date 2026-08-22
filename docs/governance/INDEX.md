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
- INDEX/CATALOG liveness census (report-only): `make sync-liveness`.
  Not in [`../../scripts/gates.yml`](../../scripts/gates.yml) — Phase 5b named.
- Session narrative: read the newest entry in
  [`../SESSIONS.md`](../SESSIONS.md); older entries are indexed at its end.

## Liveness census (2026-08-22)

Pointer, not a second owner. Re-run: `make sync-liveness`.
`--apply-index` unused (reserved-close Open rows stay Open).

| limb | count |
|---|---|
| `stale_index_open` | 0 |
| `open_with_hot_closure` | 0 |
| `archive_owed_active` | 0 |

Verdict: **CLEAN**. `scripts/gates.yml` untouched this pass.

## Named-not-opened (nav leftover)

Not a sixth root doc. Pointers only.

| Item | Disposition |
|---|---|
| Phase 5b — wire `sync_liveness` into `gates.yml` | Named. GO only if this census stays CLEAN. Candidate: `path-conditional` on `docs/briefs/INDEX.md` + `lab/CATALOG.md`. Not W5 leftover C-P5-04 / H6 (CI composition). |
| Phase 7 — ADR topic view | Named. Needs a new `AdrHeader` field + `check_adr_graph.py --regenerate-index`. No miss evidence from P0–P4. |
| Phase 8 — unify `ops/` imports | Named. Dual layout is intentional ([`REPO_MAP.md`](../../REPO_MAP.md) §2.2). Architecture ADR + Fly/deploy blast; out of nav scope. |
| Phase 2b — further CATALOG stamps | Named. Leftovers on [`lab/analysis/README.md`](../../lab/analysis/README.md). Axis split [`ADR`](../adr/2026-08-22-catalog-hot-vs-disposition.md) `Accepted`; Phase 1 landed. Do not mass-stamp `Verdict:`. `time_to_pass.py` stays C-P2-05. |
| Non-nav leftovers | C-P1-06 DISC-CAMP-0 prereg body · W5 CI-from-`gates.yml` (H6 HOLD) · Q-PUBTRANS-1 still `Proposed` · W6 lockfile discharged (PR #92). |
