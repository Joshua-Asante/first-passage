# Extraction evidence — 2026-09-13

Source: PR365 published head `23cf0e1` plus preserved, unaccepted round7 changes.
Base: actual `origin/main` at `2e8cf9e`. Stages are review candidates, not production references.

- Producer-only suite: **6 passed**, independently repeated by the reviewer.
- Primitive stage without account/daemon modules: **237 passed** (231 inherited + 6 producer).
- Exact collected test identifiers and parametrization compared with preserved source:
  **all 385 inherited cases present, none missing or duplicated**.
- Integrated candidate: **393 cases** (385 inherited + 6 producer + 2 snapshot boundary).
- Full `tests/ops`: **970 passed, 13 skipped**; two existing seaborn deprecation warnings.
- Focused model pylint: **9.66/10** (repository threshold 8).
- Five isolated semantic mutations were detected with a passing 393-case control:
  owner overwrite 82 failures; ignored remainder 3; timestamp without causality 1;
  ignored protection parameters 3; omitted completion disarm 12.
- Commit hooks run on each candidate; public-worktree Pine checks report their normal
  source-unavailable warning rather than claim verification of absent private inputs.

These results apply to the extracted code with account schema5 and primitive schema4.
They demonstrate preservation and selected fault detection, not completeness.
Known consumer acceptance blockers remain in `KERNEL_CONTRACT.md`. Hosting CI,
independent model acceptance, operator ratification and live qualification are separate.

## Subsequent rev7 integration (#370)

The counts and schema numbers above are historical extraction evidence. Current
account acceptance is recorded in `ACCOUNT_VERIFICATION.md`. Inherited expectations
were corrected where rev7 requires an ongoing outage to retain its rollover latch
and requires post-restart proof before dispatching a planned disarm. New independent
sequence cases live in `account/test_rev7_integration.py`.
