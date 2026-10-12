# Q-SFCLEAR-2 run path C: Tradovate scoring costs (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** **DRAFT, not frozen, not dispatchable.** Drafted 2026-10-12 for the Deployment Coordinator. Freezing is the coordinator's act, and only after Joshua's rulings ([decision packet](../../notes/2026-10-12-q-sfclear-2-run-path-decision-packet.md) items 1, 3, 5).

**Base:** `origin/main` `92bfca7`; every `file:line` is at that commit.

**Parent scope:** [run-path scope note](../../notes/2026-10-12-q-sfclear-2-run-path-code-scope.md) §1 item 3, cross-component constraint "fee identities stay separate", §2 packet C.

**Study (governs):** the FROZEN Q-SFCLEAR-2 [pre-registration at F `83867f0`][prereg] §4 items 1 (`g = Net PnL + Commission` once) and 2 (dated per-side all-in Tradovate rate per instrument: Free-plan commission + exchange + clearing + NFA; 6J at the standard rate; snapshot re-taken and hashed at freeze if older than 30 days, then used by hash; `c ∈ {1, 1.5}` multiplies only these fees; the replay keeps reference friction), §1 D7, §6 VOID (fee snapshot missing or mismatched).

**Authority:** G-1, G-2, G-3 (§11).

**Executor (proposed):** Codex local, single writer of `codex/sfclear2-c-tradovate-costs`, in a fresh worktree. Not GLM.

**Coordinator:** the Deployment Coordinator. Converting the private snapshot into this card's schema is a coordinator act outside the build.

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
  - no_real_fee_value_in_fixtures
  - card_section2_files_only
  - no_core_edit
  - no_production_source_edit
  - no_replay_or_emulator_edit
  - no_reference_friction_replacement
  - no_dd_protection_or_frozen_constant_edit
  - no_lab_ops_import
  - no_existing_test_or_fixture_edit
  - no_pine_or_port_access
  - no_main_write
  - no_merge
  - no_pr_open
  - no_glm
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/lab/test_sfclear_tradovate_fees.py
  - tests/lab/test_sfgrowth_acceptance.py
  - tests/ops/qualification/test_production_source.py
  - tests/ops/qualification/test_cost_schedule_validation.py
```

The first file is new; the rest exist and stay green with no edit. Under option (a) (§0.5) the new test is `tests/ops/qualification/test_personal_cost_terms.py` instead, and the ops trust-domain suites join the list.

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

Every anchor is at `origin/main` `92bfca7`. Report findings before any test; a contradiction is a **stop** (§7).

- **(a) Existing parser.** `ops/c1_rail/qualification/production_source.py:127` `_cost_terms`: Tradeify URL, closed four-symbol rows, `round_trip_usd` divided by two at `:156`. It stays exactly as is.
- **(b) Scorer consumer.** `lab/discovery/sfgrowth_acceptance.py:192` `daily_series(trades, calendar, fees, cost)`: `fees` is **one** component mapping `{commission, exchange, clearing, NFA}` (`:194`), summed and applied as `cost × trade.sides × rate` (`:206`). It takes no instrument key, so a per-instrument snapshot is applied by calling it once per leg with that leg's instrument rate. Confirm.
- **(c) Sides.** `lab/discovery/remc_series_builder.py:210` (`sides` = one entry and one exit per contract). So the rate is per side per contract, and no divide-by-two applies.
- **(d) Firm row.** `core/firm_rules.py` `Personal_Tradovate` has `cost_per_side_usd: None`: one undated scalar, not this snapshot. It is not used (decision packet item 3).
- **(e) Inventories.** `lab/` is outside `trust_domain.py:140`/`:156` and `policy_fingerprint.py:29`.

## 0.5. Routing and clarifying questions

- **(A) Placement.** **Pending decision packet item 3.** Recommended option (b): a lab-side closed parser, `lab/discovery/sfclear_tradovate_fees.py`, consuming a serialized snapshot. Option (a): a separate closed ops parser, `ops/c1_rail/qualification/personal_cost_terms.py`, with an explicit venue discriminator; `_cost_terms` is untouched and `production_source.py` is never edited by this card.
- **(B) Schema `sfclear_tradovate_fees/v1`, closed.** Fields: `venue = "Tradovate"`, `plan = "Free"`, `unit = "USD_per_side_per_contract"`, `captured_utc` (aware ISO), `source_sha256` (64 hex, the retained private capture), `rows`: exactly one per instrument in {`6J`, `MYM`, `MGC`, `MNQ`}, each with decimal strings `commission`, `exchange`, `clearing`, `NFA`.
- **(C) Identity, not freshness.** The 30-day re-take in pre-registration §4 item 2 applies **at freeze only**; the coordinator does it before the freeze record is sealed. At run time the parser takes the expected digest from the private freeze record and refuses any snapshot whose hash differs (§6 VOID). It applies no age test at run time.
- **(D) Output.** `rates_for(instrument)` returns the four-component mapping `daily_series` already accepts. One unit conversion, at parse.

## 1. Goal

One closed, dated, per-instrument per-side all-in Tradovate capture feeds scoring. Reference replay friction stays separately identified and unchanged.

**Not asked:** taking or converting the real snapshot; wiring into replay; the run wrapper (E).

## 2. Scope

### 2.1 Files (option (b), recommended)

| File | Bound | Edit |
|---|---|---|
| `lab/discovery/sfclear_tradovate_fees.py` | not in either inventory | new |
| `tests/lab/test_sfclear_tradovate_fees.py` | — | new |

### 2.2 Files (option (a), if ruled)

| File | Bound | Edit |
|---|---|---|
| `ops/c1_rail/qualification/personal_cost_terms.py` | T once imported by a bound module | new |
| `tests/ops/qualification/test_personal_cost_terms.py` | — | new |

**Forbidden files (either option):** `production_source.py` (B's single writer); `replay.py`; `tv_broker_emulator.py`; `lab/discovery/sfgrowth_acceptance.py` and `lab/research_utils/sfgrowth_margin.py` (reused, not edited); every `core/` file; any existing test; Pine, ports, private files.

## 3. Method

1. Phase 0; post findings.
2. Fresh worktree; cut `codex/sfclear2-c-tradovate-costs`.
3. §4 rows red; build; green; acceptance list; `fp test` (option (b)) or `fp test-ops` (option (a)); `fp check`; cite records.
4. Stage only the option's files; push; return. Return this input contract to the coordinator before B or E integration.

## 4. Acceptance checks (falsifier-first)

**Hypothesis:** `N/A`. This executes scope note §2 packet C.

| Row | Test | Fails if |
|---|---|---|
| C1 | Each instrument's rate is independent: changing one row changes only that instrument's output | Rates cross |
| C2 | A row labelled round-trip, or `unit` other than per-side, refuses; a per-side value is never halved | Per-side and round-trip conflated |
| C3 | Missing component, extra component, duplicate instrument, missing or extra instrument refuse | Partial all-in accepted |
| C4 | Wrong `venue` or `plan`, or naive or unparsable `captured_utc`, refuses. A snapshot whose hash matches the freeze-record digest is accepted whatever its age at run time; any other snapshot refuses (VOID) | Mislabelled or swapped snapshot accepted, or a frozen snapshot refused for age |
| C5 | `source_sha256` mismatch against the expected digest refuses; a rate lookup without a new capture does not change identity | Silent snapshot swap |
| C6 | NaN, infinity, negative, non-decimal-string, or positive value that underflows to 0.0 refuse | Bad number accepted |
| C7 | Through `daily_series` on synthetic trades: `g = Net PnL + Commission` adds the reference commission back exactly once; the Tradovate fee is then deducted exactly once per side at each multiplier `c = 1` and `c = 1.5`. Assert the day total equals `Σ(Net PnL + Commission) − c × sides × rate` exactly, so neither commission is deducted twice | Double deduction, a missing add-back, or a missing fee |
| C8 | `_cost_terms` on its existing fixtures is byte-equal at the cut base | Tradeify contract changed |

**Named mutants:** M-C1 divide per-side by two (C2, C7); M-C2 replace reference friction with the Tradovate rate (C7); M-C3 accept a missing instrument (C3); M-C4 refuse a snapshot older than 30 days at run time (C4: the frozen snapshot must still be accepted, so this mutant is a defect the row catches); M-C6 accept a snapshot whose hash differs from the freeze record (C4, C5); M-C5 apply `c` to reference commission (C7).

**Revert trigger:** any listed existing suite changes outcome.

## 5. Forbidden

- No real fee value in fixtures; fixtures invent rates.
- No private read; no real-data run.
- No edit to `_cost_terms`, the emulator or reference friction.
- No `lab↔ops` import under either option.
- No edit to frozen constants or `dd_protection`.
- GLM, a push to `main`, a merge, or opening a PR.

## 6. Return (status taxonomy)

| Status | When |
|---|---|
| `DONE` | Rows red then green; mutants killed; suites and `fp check` completed exit 0; footprint equals the option's table |
| `DONE_WITH_CONCERNS` | As DONE, with an observation |
| `NEEDS_CONTEXT` | Item 3 unruled; §0(b) contradicted |
| `BLOCKED — context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong` | As named |

**Gate verdict (coordinator, at review):** **RESOLVED** when `DONE` and both §7 passes reproduce it; **FALSIFIED** when a row cannot be made red or a mutant survives; **AMBIGUOUS** on `DONE_WITH_CONCERNS`.

## 7. Stop conditions and parent review

**Stop and return:** §0(b) shows `daily_series` cannot take a per-instrument rate without an edit; any need to edit `production_source.py`, `sfgrowth_acceptance.py` or the emulator.

**Parent review:** Pass 1, footprint and schema against pre-registration §4 item 2; Pass 2, re-run rows and mutants from a clean worktree.

## 8. Out of scope and decision unlocked

**Out of scope:** the private snapshot conversion (coordinator), B, D, E.

**Unlocks:** E's scoring composition.

## 9. Sequencing and file collisions

- **`production_source.py` single writer:** B's writer. C never edits it. Under option (a), any import of `personal_cost_terms.py` into a bound module is B's edit, after C merges. Order: A → C → B.
- No collision with the calculator branch, P-L2/P-L3 or the owner queue.

## 10. Audit hooks (runnable)

```bash
python -I scripts/check_brief.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-run-path-c-tradovate-costs-card-DRAFT.md --type cc_handoff
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-run-path-c-tradovate-costs-card-DRAFT.md
git diff --name-only <cut>..HEAD   # expect the option's two files
git diff <cut>..HEAD -- ops/c1_rail/qualification/production_source.py   # expect empty
python -I scripts/fp.py python -m pytest <the authority-block acceptance list>
python -I scripts/fp.py check
```

## 11. Gates (the card is NOT DISPATCHABLE until all three hold)

- **G-1. Joshua's ruling on item 3**, and admission if option (a). **Not recorded.**
- **G-2. Coordinator freeze.** **Not done.**
- **G-3. Dispatch.** **Not done.**

## 12. Open decisions (coordinator at freeze; Joshua where marked)

- **D-1 (Joshua, item 3).** Placement.
- **D-2.** Confirm the instrument key set and that 6J's "standard rate" is a row value, not a parser rule.

## Pre-mortem

- **Loop cost.** One targeted run, one suite run, one `fp check`.
- **Likely failure.** C7 exposes that `daily_series` sums the fee before multiplying by `sides`; that is correct per side, and the test must assert it, not change it.
- **What would make this moot:** none known; the study requires a dated Tradovate rate.
- **Evidence binding:** records at the returned head only.

[prereg]: https://github.com/Joshua-Asante/first-passage/blob/83867f0d362931c2a516a62b990bb1c209372527/docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
