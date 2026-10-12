# Q-SFCLEAR-2 run path B: verified personal replay and route evidence (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** **DRAFT, not frozen, not dispatchable.** Drafted 2026-10-12 for the Deployment Coordinator. Freezing is the coordinator's act, and only after Joshua's admissions and rulings ([decision packet](../../notes/2026-10-12-q-sfclear-2-run-path-decision-packet.md) items 1, 4, 5, 7).

**Base:** `origin/main` `92bfca7` for every `file:line`; the build cuts from a base that contains A's merge and #752's frozen schedule files (§0(a)).

**Parent scope:** [run-path scope note](../../notes/2026-10-12-q-sfclear-2-run-path-code-scope.md) §1 items 2 and 4, cross-component constraints (schedule, roll facts, trade output, layer boundary), §2 packet B.

**Study (governs):** the FROZEN Q-SFCLEAR-2 [pre-registration at F `83867f0`][prereg]: §2 (R1 labels; binding by tuple hash `62d7ae19…671f`), §3 G0 (schedule sha256 `ab44fada…d473`) and G4 (roll-date list sha256 `72677d25…134c`), §4 items 1, 3, 7, 8, §6 VOID row, §7 routes, FG item 1 and the PR definition.

**Authority:** G-1 code admission, G-2 freeze, G-3 dispatch (§11).

**Executor (proposed):** Codex local, single writer of `codex/sfclear2-b-personal-replay`, in a fresh worktree. Not GLM. **This writer is the only writer of `production_source.py` across A, B and C** (§9).

**Coordinator:** the Deployment Coordinator.

```yaml authority
seat: worker
parent: docs/notes/2026-10-12-q-sfclear-2-run-path-code-scope.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - not_dispatchable_until_section_11_gates_recorded
  - offline_synthetic_only
  - no_real_data_run
  - no_private_read
  - card_section2_files_only
  - no_core_edit
  - no_book_sizing_context_or_book_account_owner_edit
  - no_book_bundle_execution_edit
  - no_adapter_port_or_emulator_edit
  - no_dd_protection_or_frozen_constant_edit
  - no_lab_ops_import
  - no_schedule_or_roll_list_or_generator_edit
  - no_expected_hash_derived_from_checked_file
  - no_existing_test_or_fixture_edit
  - no_pine_or_port_access
  - no_rail_arm
  - no_rail_deploy
  - no_account_traffic
  - no_main_write
  - no_merge
  - no_pr_open
  - no_glm
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/qualification/test_personal_replay.py
  - tests/ops/qualification/test_personal_route_output.py
  - tests/ops/qualification/test_personal_p0_replay.py
  - tests/ops/qualification/test_production_source.py
  - tests/ops/qualification/test_replay.py
  - tests/ops/qualification/test_trust_domain.py
  - tests/ops/qualification/test_runtime_inventory.py
  - tests/ops/qualification/test_seal.py
  - tests/ops/qualification/test_composition_fixture.py
  - tests/ops/qualification/test_composition_route.py
  - tests/ops/test_book_policy.py
  - tests/ops/test_book_quantity_laws.py
  - tests/ops/test_book_adapters_parity.py
  - tests/ops/test_c1_rail_image_manifest.py
  - tests/ops/test_c1_signal_daemon_image_manifest.py
```

The first two files are new; `test_personal_p0_replay.py` comes from A. The rest exist and stay green with no edit.

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

Report before any test. A contradiction is a **stop** (§7).

- **(a) Base.** The cut base contains A's merge, and `lab/analysis/c1/sfclear_2026-10/schedule/historical_schedule_2022-09-01_2026-09-02.json` and `roll_dates_6J_MGC_2022-09-01_2026-09-02.json` byte-equal to F (`git diff --quiet 83867f0 HEAD -- lab/analysis/c1/sfclear_2026-10/schedule`). Their schemas are `sfclear_historical_schedule/v1` and `sfclear_roll_dates/v1`.
- **(b) Replay.** `ops/c1_rail/qualification/replay.py:46` (`AttributionSidecar`), `:200` (`lifetime_adverse_mark`), `:245`, `:612`, `:628`. Report what per-trade fields exist today against §2.1's route-output schema.
- **(c) Production source.** `ops/c1_rail/qualification/production_source.py:175` (`parse_startup_policy`), `:190` (literal 80), `:230` (`parse_source_calendar`, `qualification-source-calendar/v1`), `:1138` (`_build_from_prepared`), `:1344` (`_engine`), `:1367` (`candidate_book_protection_policy()` hardcoded).
- **(d) Adapter state.** Without reading any port body, report whether `ops/c1_signal_daemon/book_adapters.py` exposes Striker's paper equity and `ddHit` trip state, and Vanguard's paper equity `E_p`, through its public adapter surface. If either needs a port or adapter edit, **stop** (`plan-itself-wrong`).
- **(e) Inventories.** `trust_domain.py:140`/`:156`; whether a new `qualification/` module must be listed there and in the image manifests (`tests/ops/test_c1_rail_image_manifest.py`).
- **(f) P7 D8 closure.** `production_source.py` and `replay.py` are D8 paths ([C′ card](2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md)). As A §0(f).

## 0.5. Routing and clarifying questions

Synthetic only. Defaults apply unless Phase 0 contradicts them (`NEEDS_CONTEXT`).

- **(A) Read once.** Each input is read as bytes once, hashed, parsed from the same bytes and retained. No hash-then-reopen.
- **(B) Expected hashes.** Public pins (schedule, roll list) are module constants equal to the pre-registration's values. Private identities (tuple, source bundle with its reference-friction capture) arrive as expected digests in a run manifest that E builds from the frozen pre-registration at F and the private freeze record. The `E_0` file reference comes from `R1_TUPLE.json`, itself verified against the frozen tuple sha256 `62d7ae19…671f` (pre-registration §2: the tuple carries the `E_0` file reference). The `E_0` file's bytes are also checked against the `E_0` file hash in the private freeze record's `input_sha256` map; the coordinator confirms at freeze that the map includes that file. Both must match. No expected hash is read from the file it checks.
- **(B′) Halt start.** The replay's starting account equity, and so the P0 halt's initial peak, is `E_0` read from the private `E_0` file inside the verified envelope: bytes read once, hashed and checked as in (B), parsed as one finite positive value. There is no default, no constructor fallback and no value from any other file. The value is never logged or written to public output. Tests use a synthetic file and digest.
- **(C) Schedule bridge.** A closed parser for `sfclear_historical_schedule/v1` maps each row to the replay's session facts: DENIED rows refuse entries and adds and stay zero days; PERMITTED rows carry cutoff 15:45, flatten start 15:55 and own-flat 16:00 ET from the row's UTC fields. It is a separate parser, not a feed into `parse_source_calendar`.
- **(D) Roll list.** A closed parser for `sfclear_roll_dates/v1`. For 6J and MGC, no entry or held position at or after `g4_start_open_utc` of the held contract. Roll dates are never inferred from a price discontinuity.
- **(E) Route.** **Pending decision packet item 4.** Recommended: PR for all four legs. RS for Aegis is built only if Joshua rules it, and then every D9 condition and FG-T is a refusing check.
- **(F) Instance.** The factory at `:1367` takes the resolved instance: Tradeify keeps `candidate_book_protection_policy()`; personal uses A's `PersonalP0Policy`. The startup check at `:190` compares against `account_micro_cap(resolved tier)`, not the literal.

## 1. Goal

A four-leg chronological `BookReplay` that consumes only the frozen input identities (R1 vector, P0, schedule, roll list) and emits the route output the study scores. It preserves adapter state and actual fill feedback, including refused signals. Every Tradeify path is unchanged.

**Not asked:** fees (C), live parity (D), scoring and publication (E), any real-data run.

## 2. Scope

### 2.1 The change

- New `ops/c1_rail/qualification/personal_replay.py`: the verified input envelope (§0.5 A–D), the personal factory, and the route-output writer `sfclear_route_output/v1`.
- `sfclear_route_output/v1`, per trade: leg, instrument, contract, entry and exit UTC, side, quantity, tranche index (0 at R1), entry price, initial stop level and `δ₀`, exit price, exit kind, stop-fill distance `b`, Net PnL and Commission (reference friction, as the emulator charges it), whole-trade MAE and MFE in USD. Per leg: refused signals with reason; Striker daily- and total-DD trip timestamps; Vanguard `E_p` path. Per run: every input identity, and A's P0 latch record if one occurred (its consequence is decision packet item 7). No `E_0` or account figure.
- `production_source.py`: §0.5 (F); nothing else.
- `replay.py`: G4 enforcement and the per-trade fields above, from the actual fill lifecycle.
- `trust_domain.py`: list `c1_rail.qualification.personal_replay` if §0(e) requires it.

### 2.2 Files

| File | Bound | Edit |
|---|---|---|
| `ops/c1_rail/qualification/personal_replay.py` | new; T once listed | new |
| `ops/c1_rail/qualification/production_source.py` | T | §0.5 (F) |
| `ops/c1_rail/qualification/replay.py` | T | §2.1 |
| `ops/c1_rail/qualification/trust_domain.py` | T | one entry, conditional |
| `tests/ops/qualification/test_personal_replay.py` | — | new |
| `tests/ops/qualification/test_personal_route_output.py` | — | new |

**Forbidden files:** every `core/` file; `book_policy.py`, `book_capacity.py`, `book_sizing_context.py`, `book_account_owner.py`, `personal_drawdown_halt.py`; `ops/c1_signal_daemon/book_adapters.py`, `tv_broker_emulator.py`, `book_bundle_execution.py`; `policy_fingerprint.py`; every `lab/` file, including the schedule, roll list and their generators; any existing test or fixture; Pine, ports, `effective_inputs.json`.

## 3. Method

1. Phase 0; post findings.
2. Cut `codex/sfclear2-b-personal-replay` in a fresh worktree from the §0(a) base.
3. Write §4 rows; record **red**.
4. Build §2.1; record **green**, then the acceptance list, then `fp test-ops` and `fp check` (cite `record.json`).
5. Stage only §2.2; push; return. The coordinator runs the S2 supervision workflow on the PR.

## 4. Acceptance checks (falsifier-first)

**Hypothesis:** `N/A`. This executes scope note §2 packet B.

| Row | Test | Fails if |
|---|---|---|
| B1 | Independently mutate each identity (tuple, size vector, source bundle, schedule, generator, calendar, reference-friction capture, roll list, `E_0` file; the Tradovate fee and margin snapshots are E's inputs, not the replay's): each refuses before adapter construction or outcome access. With a valid envelope, the replay's starting equity and the halt's initial peak equal the synthetic `E_0`; a missing `E_0` file refuses | Any mismatch reaches execution, or the halt starts from anything but the bound `E_0` |
| B2 | Wrong four-leg set; non-canonical size vector; adds ON for Striker or Vanguard; ORB with nonzero base | Accepted |
| B3 | Entry on a DENIED row refused; the row is a zero day in output | Entry or removed day |
| B4 | Entry or add at exactly the cutoff refused; one second before admitted; flatten at flatten start; flat by own-flat | Off-by-one at a boundary |
| B5 | Missing finer chronology inside a session refuses | Silent gap |
| B6 | 6J and MGC: entry, add or carried position at or after `g4_start_open_utc` refused or closed; a price jump with no listed roll changes nothing | G4 breach or inferred roll |
| B7 | Zero-base entry (Aegis base 0, Vanguard zero port, ORB) refuses `zero policy quantity` with no fill and exactly one refusal record; next signal sees unchanged adapter state | Zero order or lost feedback |
| B8 | Per-trade money fields, quantity, tranche, `δ₀`, `b`, MAE and MFE reconcile to the emulator's fills on synthetic bars | Output disagrees with fills |
| B9 | Output without MAE or MFE fails the schema validator | VOID not enforced |
| B10 | Synthetic Striker trip and Vanguard `E_p` path come from the adapter's state, not recomputed | Provenance faked |
| B11 | Tradeify factory output and startup v1/v2 parsing byte-equal at the cut base | Tradeify changed |
| B12 | Aegis RS requested without ruling (or any D9 condition false) refuses; PR is the default | RS approximates timing |

**Named mutants:** M-B1 skip one identity check (B1); M-B2 accept DENIED rows (B3); M-B3 `<=` for `<` at cutoff (B4); M-B4 infer a roll from a price gap (B6); M-B5 submit a zero order (B7); M-B6 drop a refusal record (B7); M-B7 omit MFE (B9); M-B8 hash then reopen the file (A); M-B9 start the replay and halt from a default or constructor equity instead of the bound `E_0` (B1); M-B10 start from a wrong value (a different synthetic `E_0` than the hashed file holds) (B1).

**Revert trigger:** any existing suite changes outcome, or B11 diffs.

## 5. Forbidden

- No real-data run, no private read, no `E_0`, no real tuple or fee bytes in fixtures (fixtures invent identities and rates).
- No edit to frozen constants, `dd_protection`, locked parameters, adapters, ports or the emulator.
- No `lab↔ops` import; the schedule and roll list are read as bytes by path.
- No Pine-native sizing, capital-scaled export or RS for Striker or Vanguard; no toggling of native guards or reference slippage (pre-registration §5).
- GLM, a push to `main`, a merge, or opening a PR.

## 6. Return (status taxonomy)

| Status | When |
|---|---|
| `DONE` | Rows red then green; mutants killed; suites green; `fp test-ops` and `fp check` completed exit 0; footprint equals §2.2 |
| `DONE_WITH_CONCERNS` | As DONE, with an observation |
| `NEEDS_CONTEXT` | A default contradicted; item 4 unruled |
| `BLOCKED — context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong` | As named; `plan-itself-wrong` covers §0(d) |

**Gate verdict (coordinator, at review):** **RESOLVED** when `DONE` and both §7 passes reproduce it; **FALSIFIED** when a row cannot be made red, a mutant survives or the revert trigger fires; **AMBIGUOUS** on `DONE_WITH_CONCERNS`.

**Report:** status, records, `git diff --name-only <cut>..HEAD`, the route-output schema as built, concerns.

## 7. Stop conditions and parent review

**Stop and return:** §0(a) base lacks A or the frozen schedule files; §0(d) needs an adapter or port change; §0(f) open without H′ in G-1; green needs a file outside §2.2; a route-output field cannot come from the actual fill lifecycle.

**Parent review:** Pass 1, footprint and schema against pre-registration §4 item 1 and §7; Pass 2, re-run rows and mutants from a clean worktree.

## 8. Out of scope and decision unlocked

**Out of scope:** C, D, E; the private run.

**Unlocks:** D's differential tests and E's route-output consumer.

## 9. Sequencing and file collisions

- **`production_source.py` single writer (A, B, C):** this card's writer only. A does not touch it (A §9). C's parser lives outside it under either fee option (C §9); if Joshua picks the ops-side option, any wiring of C's parser into the production source is done by this writer, in this card, after C merges. Order: A → C → B.
- `replay.py`: A then B, serial; B cuts after A merges.
- No `book_account_owner.py` edit; that queue (GC-5-DISPLACED → TB-I3 S2 → P-L2 → P4) is untouched.

## 10. Audit hooks (runnable)

```bash
python -I scripts/check_brief.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-run-path-b-personal-replay-card-DRAFT.md --type cc_handoff
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-run-path-b-personal-replay-card-DRAFT.md
git diff --quiet 83867f0 HEAD -- lab/analysis/c1/sfclear_2026-10/schedule && echo SCHEDULE_FROZEN
git diff --name-only <cut>..HEAD   # expect a subset of §2.2
python -I scripts/fp.py python -m pytest <the authority-block acceptance list>
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
```

## 11. Gates (the card is NOT DISPATCHABLE until all three hold)

- **G-1. Joshua's code admission** for §2.2's bound files and the new module entering the trust domain (item 1), and the route ruling (item 4). **Not recorded.**
- **G-2. Coordinator freeze**, after A returns RESOLVED and the schedule files are on the base. **Not done.**
- **G-3. Dispatch.** **Not done.**

## 12. Open decisions (coordinator at freeze; Joshua where marked)

- **D-1 (Joshua, item 4).** Aegis route.
- **D-2.** Confirm the route-output field list against pre-registration §3 (residual `r` needs `δ₀`, `b`, MAE) and §4 item 1.
- **D-3 (Joshua, item 7).** Joshua confirms the frozen reading (b), or rules (a) or (c). Under (b) the post-latch zero days come from A's mechanics with no extra code here. B carries A's latch record into the route output under every option; the card is not frozen until item 7 is settled.

## Pre-mortem

- **Loop cost.** One targeted run, one `fp test-ops`, one `fp check`, plus the S2 workflow.
- **Likely failure.** §0(d): Striker's trip state or Vanguard's `E_p` not reachable without a port read. That is a stop, not a workaround.
- **What would make this moot:** an Aegis RS ruling with cheap D9 proof changes only B12 and the Aegis route.
- **Evidence binding:** records at the returned head only.

[prereg]: https://github.com/Joshua-Asante/first-passage/blob/83867f0d362931c2a516a62b990bb1c209372527/docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
