**Theme:** legacy
**Status:** ACTIVE — EURUSD pattern-enumeration harness
# EURUSD Pattern-Enumeration Harness

Reality-check harness for the EURUSD mechanical pattern-enumeration
investigation. Components A–H per the Reality-Check Harness ADR.
**Phase 3 LOCKED 2026-05-23** (`harness_lock.json`); subsequent
modifications to load-bearing lock fields require a new ADR.

| Phase | Status | Date | Anchor |
|---|---|---|---|
| 1 — skeleton + sanity tests | LOCKED | 2026-05-22 | PR #104 (`aac72c2`) |
| 2 — `avg_block_length=21` | LOCKED | 2026-05-22 | `9487106` (DONE_WITH_CONCERNS §C2/§C3) |
| 3 — `feature_space` + K=450 + lock_hash | LOCKED | 2026-05-23 | this commit |
| 4 — enumeration | not started | — | runs under `EURUSD_HARNESS_PHASE=phase4` |
| 5 — MTC | not started | — | — |
| 6 — OOS evaluation | not started | — | runs under `EURUSD_HARNESS_PHASE=oos` |
| 7 — verdict | not started | — | — |

## Parent artifacts

- Pre-Q: `preq_eurusd_pattern_enumeration.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/preq_eurusd_pattern_enumeration.md`)
- ADR: [`docs/adr/2026-05-22-reality-check-harness.md`](../../../docs/adr/2026-05-22-reality-check-harness.md)
- Phase 2 justification: [`avg_block_length_justification.md`](avg_block_length_justification.md)
- Phase 3 justification: [`feature_space_justification.md`](feature_space_justification.md)

## Running the sanity tests

From within this directory (so the local `pyproject.toml` is picked up):

```
cd analysis/eurusd_pattern_enum
pytest tests/ -v --tb=short
```

The full suite includes the slow Test 2 (`-m "slow"` only or default-all).
For development iterations: `pytest tests/ -v -m "not slow"`.

## Phase-flag mechanism

Two components are gated by `EURUSD_HARNESS_PHASE`:

| Component | Module | Guard form | Allowed phase |
|---|---|---|---|
| A (data loader) — OANDA path | `harness/data_loader.py` `fetch_oanda_eurusd` | function raises `RuntimeError` | `phase2` or later |
| G (OOS evaluator) | `harness/oos_evaluator.py` | **module-level** `ImportError` at import | `oos` only |

Default value when the env var is unset: `'phase1'`. The OOS module's
import-time guard is the strong structural form — Phase 1-4 code paths
that accidentally import `harness.oos_evaluator` fail at the import statement,
not later at function call.

Test 4 (`test_sanity_partition_leakage.py`) covers both guards via
subprocess invocations that toggle the env var per case.

## OOS-access discipline

OOS data (2024-01-01 onward) is reachable only through the OOS evaluator,
which itself requires `EURUSD_HARNESS_PHASE='oos'`. All other code paths
treat OOS dates as forbidden via `assert_in_sample()` in `data_loader.py`.

The IS/OOS boundary is locked in `harness_lock.json`:
- IS: 2018-01-01 → 2023-12-31
- OOS: 2024-01-01 → data-end

Per ADR §2.1 — no third "validation" split, ever.

## Components

| Component | File | Phase 1 status |
|---|---|---|
| A — Data loader | `harness/data_loader.py` | Synthetic-only path active; OANDA path import-guarded |
| B — Pattern registry | `harness/pattern_registry.py` | Trivial registry, append-only, freeze-able |
| C — Pattern executor | `harness/pattern_executor.py` | Pure function (pattern_fn, bars, tx_cost) → trade list |
| D — Metrics | `harness/metrics.py` | PF, N, MaxDD, Sharpe, DSR (Bailey-LdP 2014) |
| E — Bootstrap | `harness/bootstrap.py` | Politis-Romano stationary block bootstrap |
| F — MTC | `harness/mtc.py` | Bonferroni; alpha=0.05 |
| G — OOS evaluator | `harness/oos_evaluator.py` | Stub — module-level ImportError under non-OOS phase |
| H — Audit logger | `harness/audit_logger.py` | Append-only JSONL with in-process tamper detection |

## Lock file

`harness_lock.json` carries the locked harness contract. All fields populated
as of 2026-05-23:

| Field | Value | Locked at |
|---|---|---|
| `instrument` / `timeframe` | EURUSD / 4H | ADR-author (Phase 0) |
| `avg_block_length` | 21 | Phase 2 (`avg_block_length_justification.md`) |
| `feature_space` | structured spec, 15 triggers × 2 dir × 5 hold × 3 stop | Phase 3 (`feature_space_justification.md`) |
| `K_total` | 450 | Phase 3 |
| `evaluation_metrics`, `gate_thresholds`, `multiple_testing_method`, `bootstrap_method`, `tx_cost_model`, `position_sizing`, `is_window`, `oos_window_start` | per ADR §2.2 | ADR-author |
| `lock_hash`, `lock_timestamp` | canonical-form SHA-256 + ISO-8601 | Phase 3 |

### Lock-hash protocol

`lock_hash` is the **self-excluding** SHA-256 of the JSON's canonical form
(`lock_hash` + `lock_timestamp` zeroed, `json.dumps` with `sort_keys=True`
and `indent=2`, trailing newline, UTF-8). The protocol is documented in
the `_meta.lock_hash_protocol` field of the file itself and implemented
by [`scripts/verify_lock.py`](scripts/verify_lock.py).

ADR §4 audit hook #1 is satisfied by:

```
cd analysis/eurusd_pattern_enum
python scripts/verify_lock.py verify       # exit 0 on match, 1 on mismatch
```

`tests/test_sanity_lock_integrity.py` pins this against the committed file.
Any semantic edit (feature_space, K_total, gate_thresholds, etc.) without a
re-run of `python scripts/verify_lock.py compute --write --timestamp ...`
will trip the audit test.

**Do not edit `harness_lock.json` outside the explicit lock-amendment
workflow.** Changes invalidate the gate per ADR §4.

## Forbidden moves (excerpt — full list in CC handoff §5)

1. No touching real EURUSD data in Phase 1.
2. No populating `block_length`, `K_total`, `feature_space`, `lock_hash`, or
   `lock_timestamp` in `harness_lock.json` outside their phase windows.
3. No adding metrics beyond [PF, N, MaxDD, Sharpe, DSR].
4. No i.i.d. resampling anywhere; stationary block bootstrap only.
5. No modifying any file outside this directory.

## Phase 4 prerequisites (next)

Before Phase 4 enumeration work:

1. `EURUSD_HARNESS_PHASE=phase4` set for the spawn session.
2. `python scripts/verify_lock.py verify` passes (ADR §4 audit hook #1).
3. All sanity tests green: `pytest tests/ -v` from this directory.
4. Pattern registry populated by deterministic generation from
   `feature_space` (450 patterns enrolled before the executor runs).
5. `logs/enumeration.jsonl` empty or absent at start; audit logger
   appends one entry per pattern, denominator-matching K=450.
