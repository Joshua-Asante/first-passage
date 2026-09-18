# Phase 3 qualification tooling implementation

Goal: implement reviewable, synthetic-tested G3/G4 and integrate G1/G2/G5 without freezing or running qualification.

Architecture: single-process continuous four-adapter replay; immutable source metadata and independent path occurrences; shared production sizing, capacity, emulator and kernel. No recorded-trade reweighting. Package is `ops/c1_rail/qualification/`: this corrects the proposed lab placement because the accepted monorepo boundary prohibits lab importing ops. No boundary exception.

Tech Stack: Python 3.12, dataclasses, NumPy/SciPy existing kernel, pytest, existing TV emulator.

Spec: TB-S2 rev3 plus September 15 RC-8 amendment; TB-P1 draft; TB-P2 accepted first ratification; preparation requirements matrix.

Global Constraints: synthetic only; no F1/E1/n1/n2/PartA/n3 actual-source runs, registry admission, live state, purchase, PR, merge or deployment. Depths/configuration stay explicit proposals. Existing historical evidence is immutable. External coverage/settings acceptance blocks only consuming gates. Base d107ebdfaec194ac4b4448d1d121331ff7128e1a; isolated branch codex/phase3-qualification-tooling, worktree .worktrees/phase3-f1-preparation; pre-existing untracked preparation packet retained.

## Ownership and interfaces

Phase3 integrates; programme coordinator accepts. Phase2 owns contract.py, attempt.py, seal.py, qualification_cli.py and matching tests; Phase3 owns remaining package files and initializer. Phase1 owns independent provenance document and tests/ops/test_phase3_provenance_acceptance.py. Phase2 owns fixes to pre-existing runtime. Each writer uses exclusive files; integrator alone commits this branch.

`model.py` exports frozen source/path/session records. `SourceSession(session_id, source_session_date, bars, schedule)` contains `SourceBar(source_bar_time, bars)` where bars is tuple[(leg_id, Bar)] and schedule is `SessionSchedule(cutoff, flatten_start, own_flat_deadline)` of aware source datetimes. All source bars remain immutable. `PathSession(occurrence, path_session_date, source, bars, block_start, block_end)` contains `PathBar(path_time, source_bar_time, source_session_date, source_time_et, bars)`; bars retain source timestamps for adapters. Path identity keys replay dedupe/clock; feedback is translated to source time for adapters. Source clock drives strategy/calendar only. `EdgeState(positions, working_orders, reservations)` provides explicit four-leg zero proofs. `SessionRecord(occurrence, path_session_date, source_session_id, pnl, intraday_low, fills, flat_before_deadline, start_edge, end_edge)` is simulated, never live settlement. `PathOutcome(status, sessions_to_pass, failure_reason, diagnostics)` uses PASS/FAILURE/UNRESOLVED and immutable tuple diagnostics. `ReplayResult(sessions, events)` is engine output.

`JointFlatBlocks` consumes ordered source sessions and ledger edge proofs; no position-only shortcut. `PathAssembler` samples whole blocks and maps occurrences onto increasing UTC 15-minute path timestamps, preserving source metadata and boundaries. No indicator resets at splices. `regime.py` samples contiguous six-calendar-month source ranges with replacement to exact N, truncating only final outer range, rebuilding inner candidates on every resulting occurrence panel. RNG domains include stage/population/panel/path; speed reuses FULL.

`BookReplay` receives fresh four-adapter registry, explicit policy, EvaluationState, venue-cost instrument configuration and risk sizing provider; it runs continuously, outputs confirmed execution facts/edges and lifetime-scoped adverse marks. Source active-window coverage is established before sampling. Coverage exclusions differ from own-flat path failures. Scheduler requires source-instant price evidence at non-bar instants; no next-bar flatten or invented price. `runner.py` supplies explicit synthetic runner, kernel call with dd_scale=1 and inactivity OFF, budget preflight from a distinct synthetic probe, and stage population inventory. Production runner accepts Phase2 validated immutable contract and a claimed reservation only; source provider must meet identities and acceptance, not caller labels.

## Tasks and acceptance

1. Model, coverage and clock: failing tests for active-window gaps, chronology/DST, missing schedule prices/coverage; immutable records, source/path separation. Owner integrator.
2. Blocks/path/PartA: failing repeated/reverse mapping, nonflat working-order edge, ceil-half partition, six-month ranges, per-panel inner rebuild and seed-domain isolation tests. Bounded delegate; only blocks.py, paths.py, regime.py and matching tests.
3. Continuous replay: failing synthetic RC-1..9 cases including lifetime marking, confirmed sizing, cap/takeover, stale orders, source filters and schedule. Bounded delegate; only replay.py and test_replay.py. Shared policy functions are authorities; no substitute risk law.
4. Session/kernel/stage runner: explicit initial state, no double scaling, failure and unresolved outcomes, exact inventory, budget before batch, PartA-only-n2 constraints. Owner integrator.
5. Integrate Phase2 and Phase1 committed contributions, independently review, fix findings, run combined synthetic acceptance and representative single-process benchmark. Preserve distinct synthetic seeds and compute observations; optimize only with equivalence evidence. Local reviewable commit and coordinator handback, listing source/settings/coverage/freeze dependencies.

Each implementation task uses meaningful failing tests before production code. Review full integration, not only happy-path unit checks. Any accepted-boundary conflict is recorded and the affected gate fails closed while independent work continues.
