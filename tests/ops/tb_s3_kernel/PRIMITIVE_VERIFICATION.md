# Primitive verification — PR #369

Candidate: `codex/tb-s3-durable-primitives`, based on merged #368 (`ba0d4aa`).
Scope: offline rev7 consumer primitive boundary; no account/daemon or live acceptance.

## Local evidence (2026-09-13)

- `python -m pytest tests/ops/tb_s3_cases/primitives tests/ops/test_tb_s3_evidence_contract.py -q --tb=short`: **293 passed** (256 primitive + 37 producer).
- `python -m pytest tests/ops -q --tb=short`: **870 passed, 13 skipped**; two existing seaborn deprecation warnings.
- Unchanged #370 account suite, with only its kernel package lookup redirected in memory to this candidate: **156 passed**. No #370 files were modified. This checks retained behavior, not account-stage acceptance or schema migration.

The independent review exercised ownership transfer, scope expansion, request-ID
renewal, surviving FIFO owners, generation changes, external order coherence,
retained registry/history and global execution identity. Findings were reproduced
before correction. In particular, the retained external-order test initially
included restart, which independently blocked admission and hid the failure; the
final test omits restart and proves the actual disappearing-registry race.
The bounded-generation completion regression also failed before its correction.

## Acceptance limits

Schema 6 is an offline snapshot format; old snapshots are refused, not migrated.
Listener close commands implement explicit scoped market transitions only. Native
trigger evidence is supported, but #370's listener-origin close-time trigger path
requires separate integration review. Bounded leg/symbol close requests and
producer-divergent scoped closes are unsupported. See `KERNEL_CONTRACT.md`.
Passing this stage does not ratify pending policy/contract decisions, qualify a
live producer, authorize operation, or accept #370.

Independent final review accepted the documented offline primitive boundary at
`198623ca328fb3818ab5ce182b4d94bfeff9e348` plus the reviewed changes committed with
this record: no remaining blocking findings; independent **293 passed** and clean
`git diff --check`. Errors-only pylint passed with repository/ops import roots.
Remote CI and user approval remain external merge gates.
