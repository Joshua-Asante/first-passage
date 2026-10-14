# Q-SFCLEAR-2 run path B: verified personal replay and route evidence (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** **FROZEN 2026-10-12** by the Deployment Coordinator at the commit that adds this line (committed-handoff rule), after Joshua's rulings on [decision packet](../../notes/2026-10-12-q-sfclear-2-run-path-decision-packet.md) items 1–7 (2026-10-12: "item 1 admitted as listed"; "2 mirror, 3 b, 4 PR, 5 as proposed, 6 b (extend §60 to the FG run), 7 b"). **Not dispatched.** Dispatchable on the coordinator's dispatch record once: card A merged, card C merged, and #752 (frozen `lab/analysis/c1/sfclear_2026-10/` files) merged to main.

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
- **(E) Route (item 4 RULED: PR).** Port replay (PR) for all four legs in one `BookReplay` (pre-registration §7). RS is not used: no RS path is built for any leg.
- **(F) Instance.** The factory at `:1367` takes the resolved instance: Tradeify keeps `candidate_book_protection_policy()`; personal uses A's `PersonalP0Policy`. The startup check at `:190` compares against `account_micro_cap(resolved tier)`, not the literal.

## 1. Goal

A four-leg chronological `BookReplay` that consumes only the frozen input identities (R1 vector, P0, schedule, roll list) and emits the route output the study scores. It preserves adapter state and actual fill feedback, including refused signals. Every Tradeify path is unchanged.

**Not asked:** fees (C), live parity (D), scoring and publication (E), any real-data run.

## 2. Scope

### 2.1 The change

- New `ops/c1_rail/qualification/personal_replay.py`: the verified input envelope (§0.5 A–D), the personal factory, and the route-output writer `sfclear_route_output/v1`.
- `sfclear_route_output/v1`, per trade: leg, instrument, contract, entry and exit UTC, side, quantity, tranche index (0 at R1), entry price, initial stop level and `δ₀`, exit price, exit kind, stop-fill distance `b`, Net PnL and Commission (reference friction, as the emulator charges it), whole-trade MAE and MFE in USD. Per leg: refused signals with reason; Striker daily- and total-DD trip timestamps; Vanguard `E_p` path. Per run: every input identity, and A's P0 latch record if one occurred (item 7 RULED (b): later days are zero days; no verdict rule). No `E_0` or account figure.
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
| B12 | All four legs run in the one PR replay; there is no RS path, so a manifest requesting a per-trade rescale for any leg refuses | Any leg rescaled instead of replayed |

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
| `NEEDS_CONTEXT` | A default contradicted |
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

- **`production_source.py` single writer (A, B, C):** this card's writer only. A does not touch it (A §9). C is lab-side (item 3 RULED (b)) and never touches it. Order (item 5 RULED as proposed): A0 → A → C → B → D → E.
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

- **G-1. Joshua's code admission** for §2.2's bound files and the new module entering the trust domain (item 1), and the route ruling (item 4). **Admission RECORDED:** Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "item 1 admitted as listed" (scope confirmed: card A §2.3 files including A0 `core/firm_rules.py` and the conditional rows; card B §2.2 files including new `qualification/personal_replay.py`; accepting that the Tradeify TB-I1 fingerprint and trust-domain digests move, D8 paths change and H′ moves, with P7 re-measured on the new bytes if P7 D8 is still owed; `book_sizing_context`/`book_account_owner` excluded, with P4). **Item rulings RECORDED:** Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "2 mirror, 3 b, 4 PR, 5 as proposed, 6 b (extend §60 to the FG run), 7 b".
- **G-2. Coordinator freeze**, after A returns RESOLVED and the schedule files are on the base. **Not done.**
- **G-3. Dispatch.** **Not done.**

## 12. Open decisions (coordinator at freeze; Joshua where marked)

- **D-1 (item 4).** RULED: PR for all legs (§0.5 (E)).
- **D-2.** Confirm the route-output field list against pre-registration §3 (residual `r` needs `δ₀`, `b`, MAE) and §4 item 1.
- **D-3 (item 7).** RULED: (b), the frozen reading. Post-latch days are zero days produced by the replay through A's mechanics, with no extra code here; B carries A's latch record into the route output. No NOT CLEARED rule is added.

## Pre-mortem

- **Loop cost.** One targeted run, one `fp test-ops`, one `fp check`, plus the S2 workflow.
- **Likely failure.** §0(d): Striker's trip state or Vanguard's `E_p` not reachable without a port read. That is a stop, not a workaround.
- **What would make this moot:** none known; the route is ruled PR.
- **Evidence binding:** records at the returned head only.

[prereg]: https://github.com/Joshua-Asante/first-passage/blob/83867f0d362931c2a516a62b990bb1c209372527/docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md

## Amendment 2026-10-13 — port state via an observer hook (§0(d) stop resolved)

**Trigger:** card B's Phase 0 return (Codex, 2026-10-13, NEEDS_CONTEXT at exact base `07d90b0`): `BookStrategy.checkpoint()` has no public contract for Striker's paper equity or `ddHit` trips or Vanguard's `E_p`. The coordinator read the two ports in place (private read surface; nothing quoted): neither stores its trip state or paper equity in `checkpoint()`; both compute them per bar. B10 as written is unmeetable without a port edit (§0(d): plan-itself-wrong). **Ruling:** Joshua, 2026-10-13, directly to the Deployment Coordinator, verbatim "yes", approving the coordinator's proposal after card B's Phase 0 stop.

**Changes (all else unchanged):**
- **Observer hook.** The personal replay accepts an optional `bar_observer`. After every leg has processed a bar's close and that bar's fills have settled, it is called once per leg, in a fixed leg order, as `bar_observer(leg_id, bar_close_utc, strategy)`, where `strategy` is the leg's loaded strategy object as the replay holds it. Its return value is ignored. An exception from it aborts the run with no route output. Default `None`: behaviour and output bytes identical to no hook. Public code never reads, interprets or logs the strategy's state.
- **Route output.** `sfclear_route_output/v1` no longer carries Striker daily/total-DD trip timestamps or Vanguard's `E_p` path. Per-trade fields (D-2, confirmed 2026-10-13), refused signals with reason, verified input identities and A's latch record are unchanged.
- **B10 replaced by B10′:** a synthetic observer is called exactly once per leg per bar, in order, after fills settle, with the same strategy instance each time; route output bytes with a no-op observer equal those with none; a raising observer aborts with no output. Named mutant **M-B11:** call the observer before fills settle, or skip a leg.
- **Where trips and `E_p` come from:** the private clearance-run driver (card E amendment 2026-10-13), not this card.

### Addendum 2026-10-13 (b) — tuple schema and `E_0` resolution

On card B's question (Codex, 2026-10-13), the coordinator read `R1_TUPLE.json`'s key structure and the `E_0` file's encoding in place (no value read or printed; same scope as pre-registration §8 exposure entry 13). Public schema, names and types only:

- `schema` = `q-sfclear-1-sizing-tuple/v1`; scalars (str): `study`, `rung`, `status`, `protection`, `lifecycle_tier`, `striker_risk_basis`, `size_vector_hash_rule`, `size_vector_sha256`, `prescreen_SHA256SUMS_sha256`, `nonce`; (int): `paper_initial_capital`; `book_legs`: list of 4 str.
- `sizing` (the `validate_size_vector` input; `size_vector_sha256` = sha256 of `canonical_json_bytes(sizing)`): `aegis_6j` {`base` int, `adds` str}; `dj30_mym_p250` {`risk_multiplier` str, `cap_reserve_multiplier` str, `adds` str}; `vanguard_mgc` {`base_by_port` {`1` int, `2` int}, `adds` str}; `orb_mnq_v7` {`base` int, `adds` str}. `adds` ∈ {`OFF`, `UNCHANGED`}.
- `capital_anchor` {`file` str, `file_sha256` str (64 hex), `symbol` str}; `cap_source` {`code_source` str, `ruling` str, `shared_account_cap_micro_equivalents` int, `request_cap_micro_equivalents_each_leg` int}; `rule_max_contracts` {one int per leg id, `book_micro_equivalents` int}; `derived_from` {`R0_size_vector_sha256`, `change_from_R0`, `r3d_startup_policy_sha256`} str; `ruling` {`D4`, `date`, `source`, `text`} str.

**`E_0` resolution (replaces "file reference" in §0.5 (B)/(B′)):** `capital_anchor.file` is a descriptive label, not a path; never parse it. The run manifest supplies the `E_0` file path. B reads those bytes once and refuses unless their sha256 equals `capital_anchor.file_sha256` from the hash-verified tuple. Encoding: ASCII, no BOM, exactly one line of digits `[0-9]+` terminated by a single LF; the value must be > 0. Anything else refuses. Tests use a synthetic tuple and `E_0` file.

## Amendment 2026-10-14 (c) — 15:55 flatten start by the R1 bracket placement (Q-SFCLEAR-3)

**Takes effect only when Q-SFCLEAR-3 is frozen** (commit F₃, recorded in the parent brief as `Q-SFCLEAR-3 pre-registration commit hash`); until then it is a committed draft and changes nothing. Basis: [Q-SFCLEAR-3](../pre-registration/Q-SFCLEAR-3-verdict-preregistration.md) §S, ratified by Joshua at freeze.

- **Schedule provider.** The personal replay's `schedule_quotes` becomes `ops/c1_rail/qualification/bracket.BracketScheduleQuotes('R1')` (one fresh instance per replay). It prices grid-boundary instants from the retained source bars (cutoff 15:45, own-flat 16:00) and places each exposed leg's 15:55 instant at the ratified R1 vertex (position: adverse extreme; pending-only: close). The replay already splits only exposed legs (`replay.py`, `_split` over `exposed`); unexposed legs are not split.
- **Source bundle.** `splits` must be the empty list; any row refuses (evidence-located and other finer rows are excluded by Q-SFCLEAR-3 §S row 1). The per-day "missing finer chronology" refusal no longer applies to an edge strictly inside a bar; the requirement that the session's bars cover every edge stays.
- **Data-exclusion zero day (Q-SFCLEAR-3 §S row 1b).** The source bundle adds `data_exclusions`: a list of `{account_date, leg, reason}` (closed; `reason` = `missing_active_bar`). A PERMITTED schedule day listed there carries `bars: []` and is a zero day exactly like a DENIED row: no bars, no adapter reset, no entry or add, `net_pnl_usd` 0 and `fills` 0. A PERMITTED day with `bars: []` that is not listed, or a listed day that has bars or is DENIED, refuses. A session may begin after 18:00 ET of the prior day only on the source's first day. **Rows:** B15 listed zero day; B16 unlisted empty PERMITTED day refuses; B17 listed day with bars refuses. **Mutant:** M-B15 accept an unlisted empty PERMITTED day.
- **Contracts after the last seam.** The roll list lists only contracts whose G4 window intersects the replay window (its rule C3), so the panel's contract after the final in-window seam (6J `2026-09`, MGC `2026-12`) is absent and has no in-window G4 boundary. `parse_roll_dates` also reads `seams`; a 6J or MGC contract label is accepted if it is a listed contract (its boundary applies) or the `to_month` of a listed seam that is not itself listed (no boundary). Any other label refuses. **Row:** B18 a post-seam unlisted `to_month` is accepted with no boundary; an arbitrary unlisted label refuses. **Mutant:** M-B16 accept any unlisted label.
- **Session-boundary signal (for FG item 6).** For every zero-bar session (DENIED or §4-A), the replay calls `bar_observer(leg_id, None, strategy)` once per leg in fixed leg order at the session's position in the chronology, with no bar processed; the replay calls `adapter_factory` exactly once per run and never re-creates or resets an adapter. **Rows:** B19 one boundary call per leg per zero-bar session and no bar callback inside it; B20 `adapter_factory` called once and every observer call carries the same instance per leg. **Mutants:** M-B17 re-create an adapter across a zero-bar session; M-B18 reset an existing adapter in place across a zero-bar session (killed by a row asserting no reset path exists in the replay and the adapter's state is untouched across the session).
- **Placement record.** `BracketScheduleQuotes.placements` stays in process for the private FG driver (item 5); it is not added to `sfclear_route_output/v1`.
- **B5 replaced by B5′:** an exposed long at 15:55 is split at the low vertex, a short at the high vertex, a pending-only leg at the close vertex; an unexposed leg is not split; a non-empty `splits` list refuses. **Mutants:** M-B12 R2 placement; M-B13 split an unexposed leg; M-B14 accept an evidence row.
- **Scope:** `personal_replay.py`, `tests/ops/qualification/test_personal_replay.py`, and one `trust_domain.py` inventory entry for `c1_rail.qualification.bracket`, now a runtime dependency of the personal replay (within item 1's admission: one inventory entry per newly imported module). No `replay.py`, `bracket.py` or `production_source.py` edit.
