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
  Wired [`../../scripts/gates.yml`](../../scripts/gates.yml) `path-conditional`
  (Phase 5b). Script still exits 0; INDEX moves stay judgment.
- Rule 7 owner lookup: `make find-owner Q=<token>`. Not a sixth index.
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

Verdict: **CLEAN** (re-confirmed 2026-08-23). Phase 5b landed this GO.

## Named-not-opened (nav leftover)

Not a sixth root doc. Pointers only.

| Item | Disposition |
|---|---|
| Phase 5b — wire `sync_liveness` into `gates.yml` | Landed. `path-conditional` on `docs/briefs/INDEX.md` + `lab/CATALOG.md`; report-only (exit 0). Not W5 leftover C-P5-04 / H6 (CI composition). |
| Phase 7 — ADR topic view | Named. Needs a new `AdrHeader` field + `check_adr_graph.py --regenerate-index`. No miss evidence from P0–P4. |
| Phase 8 — unify `ops/` imports | Named. Dual layout is intentional ([`REPO_MAP.md`](../../REPO_MAP.md) §2.2). Architecture ADR + Fly/deploy blast; out of nav scope. |
| Phase 2b — further CATALOG stamps | This GO: `**Verdict:**` on `driftex_2026-08` + `eodadv_mnq_2026-08` (stay-hot; no `--slug`). Remaining leftovers on [`lab/analysis/README.md`](../../lab/analysis/README.md). Do not mass-stamp. `time_to_pass.py` stays C-P2-05. |
| SESSIONS keep-20 | Named. `--dry-run` 2026-08-23: keep 20 / roll 155 → `2026-Q3`. Actual roll is a separate GO. STATE diet already landed 2026-08-22e. |
| find-owner | Landed. [`../../scripts/find_owner.py`](../../scripts/find_owner.py) looks up Rule 7 + owner-surfaces. Not a sixth index. |
| Non-nav leftovers | C-P1-06 DISC-CAMP-0 prereg body · W5 CI-from-`gates.yml` (H6 **landed** 2026-08-23) · Q-PUBTRANS-1 still `Proposed` · W6 lockfile discharged (PR #92). |
