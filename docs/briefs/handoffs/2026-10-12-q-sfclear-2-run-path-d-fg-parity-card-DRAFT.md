# Q-SFCLEAR-2 run path D: FG capability tests and the separate FG evidence run (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** **FROZEN 2026-10-12** by the Deployment Coordinator at the commit that adds this line (committed-handoff rule), after Joshua's rulings on [decision packet](../../notes/2026-10-12-q-sfclear-2-run-path-decision-packet.md) items 1–7 (2026-10-12: "item 1 admitted as listed"; "2 mirror, 3 b, 4 PR, 5 as proposed, 6 b (extend §60 to the FG run), 7 b"). **Not dispatched.** Dispatchable on the coordinator's dispatch record once: cards A and B merged, P-L2 and P-L3 merged (the live-P0 row waits for P4).

**Base:** `origin/main` `92bfca7` for every `file:line`; the build cuts from a base containing A, B, P-L2 and P-L3 (§0(a)).

**Parent scope:** [run-path scope note](../../notes/2026-10-12-q-sfclear-2-run-path-code-scope.md) §1 item 6, §2 packet D and its "separate evidence return".

**Study (governs):** the FROZEN Q-SFCLEAR-2 [pre-registration at F `83867f0`][prereg] §7 routes and FG items 1–3 (all PASS before the run; FG not PASS means the run must not start, §6 VOID), §2 "quantity law tested = the live law", §1 D8, §11 items 2 and 4.

**This card has two parts with different executors:**
- **Part 1, the build (this card's authority block):** public synthetic differential tests. Codex.
- **Part 2, the FG evidence run (§13):** a Claude-owned private executor act. It is **not part of the build**, is not granted by this card, and needs its own frozen executor card and dispatch.

**Authority (Part 1):** G-1, G-2, G-3 (§11).

**Executor (Part 1, proposed):** Codex local, single writer of `codex/sfclear2-d-fg-parity`, in a fresh worktree. Not GLM.

**Coordinator:** the Deployment Coordinator.

```yaml authority
seat: worker
parent: docs/notes/2026-10-12-q-sfclear-2-run-path-code-scope.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - not_dispatchable_until_section_11_gates_recorded
  - offline_synthetic_only
  - test_files_only
  - no_real_data_run
  - no_private_read
  - no_fg_evidence_run
  - no_production_code_edit
  - no_book_bundle_execution_edit
  - no_book_account_owner_edit
  - no_dd_protection_or_frozen_constant_edit
  - no_lab_ops_import
  - no_log_or_reason_renaming
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
  - tests/ops/test_personal_replay_live_parity.py
  - tests/ops/test_live_size_vector_sizing_context.py
  - tests/ops/test_book_bundle_execution.py
  - tests/ops/test_book_quantity_laws.py
  - tests/ops/test_book_account_owner.py
  - tests/ops/test_four_leg_runtime.py
  - tests/ops/qualification/test_replay.py
  - tests/ops/qualification/test_personal_replay.py
```

The first file is new; the rest exist (the last from B) and stay green with no edit.

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

- **(a) Base.** The cut contains A, B, [P-L2](2026-10-11-live-size-vector-p-l2-owner-binding-card-DRAFT.md) and [P-L3](2026-10-11-live-size-vector-p-l3-emulator-parity-card-DRAFT.md). Report their merge SHAs. Missing any is a **stop**.
- **(b) Three refusal layers.** Adapter execution: `ops/c1_signal_daemon/book_bundle_execution.py:159`/`:168` (laws), `:173` (`shared_sizing_zero`). Replay: `ops/c1_rail/qualification/replay.py:612`, `:628` (`zero policy quantity`). Owner: `ops/c1_rail/book_sizing_context.py:264`/`:268` (sized), `ops/c1_rail/book_account_owner.py:1575` (binding), `:1825` (`zero_size`). Report each anchor at the cut base, after P-L2/P-L3 moved them.
- **(c) Existing parity.** `ops/c1_signal_daemon/book_parity.py:289`/`:318` and `tests/ops/test_book_adapters_parity.py:75` cover historical parity and skip without private inputs (`:43`). They are not R1 acceptance and are not reused as such.
- **(d) Live P0.** Whether the owner composes P0 at the cut. If not (P4 not landed), rows needing it are marked `PENDING-P4` and the card returns `DONE_WITH_CONCERNS`, never a skip that reads as PASS.

## 0.5. Routing and clarifying questions

- **(A) Same signals, three consumers.** One synthetic signal script drives the adapter execution path, the replay and the owner. The test compares admitted quantity, fills, refusal feedback and next-signal state, not two calls to the same law.
- **(B) Named reasons stay.** Each layer's own reason is asserted at its real consumer. No reason is renamed or normalized to make layers match.
- **(C) Identities.** Each route's code identity (`git` blob of each consumer module) and input identity are bound in the test result record.

## 1. Goal

A differential test outside `lab/` follows the same synthetic signals through adapter execution, replay and the live owner at a synthetic R1-shaped vector (FG items 2 and 3).

**Not asked:** the FG evidence run (§13); any production-code change; P0 live wiring (P4).

## 2. Scope

### 2.1 Files

| File | Bound | Edit |
|---|---|---|
| `tests/ops/test_personal_replay_live_parity.py` | — (test only) | new |

**Forbidden files:** every production file, including `book_bundle_execution.py` (P-L3), `book_account_owner.py` (P-L2/P4 queue), `book_sizing_context.py`, `replay.py`, `personal_replay.py`, `production_source.py`; every `core/` and `lab/` file; every existing test or fixture; Pine, ports, `effective_inputs.json`.

## 3. Method

1. Phase 0; post findings.
2. Fresh worktree; cut `codex/sfclear2-d-fg-parity`.
3. Write §4 rows. A row that passes on first run is checked against its mutant (a differential test is green at the base by design, so the falsifier is the mutant, not a red base run).
4. Run each mutant on a scratch copy outside the branch; record that it turns its row red; discard the copy.
5. Acceptance list, `fp test-ops`, `fp check`; cite records. Stage the one file; push; return.

## 4. Acceptance checks (falsifier-first)

**Hypothesis:** `N/A`. This executes scope note §2 packet D.

| Row | Test | Fails if |
|---|---|---|
| D1 | All four legs, entry and add, at a synthetic non-identity vector with Striker and Vanguard adds OFF: equal admitted quantity on all three paths | Any path diverges |
| D2 | Partial confirmed base: an add is sized from the confirmed base, equal on all paths (adds ON in a control vector) | Sized from intended base |
| D3 | Adds OFF in NORMAL: no add on any path | An add is sent |
| D4 | Zero-base entry (Aegis base 0) and zero-port entry (Vanguard): adapter `shared_sizing_zero`, replay `zero policy quantity`, owner `zero_size`, each at its own consumer | A reason is missing or renamed |
| D5 | Refused zero quantity: no dispatch and no reservation on the owner; no fill in replay or adapter | Zero order or reservation |
| D6 | Refusal feedback reaches the adapter exactly once; the next signal's adapter state agrees on all paths | Feedback lost or doubled |
| D7 | `PENDING-P4`: after a P0 latch, all three paths refuse risk | (only once P4 lands) |

**Named mutants:** M-D1 drop `size=` on one path (D1); M-D2 submit a zero order (D5); M-D3 omit refusal feedback (D6); M-D4 size adds from intended base (D2); M-D5 rename a reason to match (D4).

**Revert trigger:** any existing suite changes outcome.

## 5. Forbidden

- No real-data run, no private read, no FG evidence run.
- No production-code edit; no renaming of logs or reasons.
- No `lab↔ops` import; no edit to frozen constants or `dd_protection`.
- A synthetic PASS is never reported as FG at R1 (scope note §2 D).
- GLM, a push to `main`, a merge, or opening a PR.

## 6. Return (status taxonomy)

| Status | When |
|---|---|
| `DONE` | All rows green; every mutant turns its row red; suites and `fp test-ops`/`fp check` completed exit 0; footprint is the one file |
| `DONE_WITH_CONCERNS` | As DONE with D7 `PENDING-P4`, or another observation |
| `NEEDS_CONTEXT` | §0(b) anchors moved so a row cannot be stated |
| `BLOCKED — context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong` | As named; `plan-itself-wrong` if a row needs a production edit |

**Gate verdict (coordinator, at review):** **RESOLVED** when `DONE` (or `DONE_WITH_CONCERNS` only for D7) and §7 reproduces it; **FALSIFIED** when a mutant survives or paths diverge; **AMBIGUOUS** otherwise.

## 7. Stop conditions and parent review

**Stop and return:** §0(a) missing a predecessor; any row needs a production edit; paths diverge (that is a finding for the owning card, not a test fix).

**Parent review:** Pass 1, the diff is one test file; Pass 2, re-run rows and mutants from a clean worktree.

## 8. Out of scope and decision unlocked

**Out of scope:** §13, P4, E.

**Unlocks:** the tested capability that §13 re-runs at the real R1 vector for FG items 2–3.

## 9. Sequencing and file collisions

- Order (item 5 RULED as proposed): A0 → A → C → B → D → E; D also needs P-L2 and P-L3 merged. D writes no production file, so it holds no slot in the `book_account_owner.py` order (GC-5-DISPLACED → TB-I3 S2 → P-L2 → P4) or the `production_source.py` single writer (B).
- D7 waits for P4.

## 10. Audit hooks (runnable)

```bash
python -I scripts/check_brief.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-run-path-d-fg-parity-card-DRAFT.md --type cc_handoff
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-run-path-d-fg-parity-card-DRAFT.md
git diff --name-only <cut>..HEAD   # expect exactly tests/ops/test_personal_replay_live_parity.py
grep -n "shared_sizing_zero\|zero policy quantity\|zero_size" tests/ops/test_personal_replay_live_parity.py
python -I scripts/fp.py python -m pytest <the authority-block acceptance list>
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
```

## 11. Gates (Part 1 is NOT DISPATCHABLE until all three hold)

- **G-1.** No bound-code admission is needed (test only); the predecessors' admissions (A, B) are recorded in their cards. **Item rulings RECORDED:** Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "2 mirror, 3 b, 4 PR, 5 as proposed, 6 b (extend §60 to the FG run), 7 b".
- **G-2. Coordinator freeze.** **Not done.**
- **G-3. Dispatch.** **Not done.**

## 12. Open decisions (coordinator at freeze; Joshua where marked)

- **D-1 (item 4).** RULED: PR for all legs; §13 shows no FG-T.
- **D-2 (item 6).** RULED: (b), the Azure VM under the §60 addendum 2026-10-12.
- **D-3.** Whether D7 must be green before the run (FG item 3 names adds OFF and zero refusal only; P0 live parity is P4's acceptance).

## 13. Part 2: the FG evidence run (Claude-owned executor act; not in this build)

Owned by Claude under its own frozen executor card, after Part 1, A, B and the predecessors return RESOLVED. This card grants nothing for it. Content the executor card must carry:

- **Executor and host (item 6 RULED: b).** An authorized Claude executor runs on the Joshua-controlled Azure VM. The accepted runtime ports and `effective_inputs.json` may be copied to that VM **for this FG run only**, under the [campaign §60 addendum 2026-10-12](../programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25) (being added by the coordinator) extending AGENTS.md "Private read surface". **Pine stays off the VM.** Nothing private is quoted, committed or sent to GLM or any other external service; any Pine read stays in place in the primary checkout.
- **Anchors at R1 on the moved emulator:** per leg, the §7 route's anchor re-shown at R1 (Striker: corrected port `efd479b6…` Step 3 contract and Step 6 replay; Vanguard: V-0 338/338; Aegis: its PR anchor), each with the F11 revalidation (T10 reconciliation R1 hold item (ii); `docs/notes/2026-09-21-t10-phase1-source-reconciliation.md:182`); FG item 1's schedule and roll list loaded by frozen sha256. RS is not used (item 4 RULED: PR), so FG-T is not part of this run.
- **FG items 2 and 3 at the real R1 vector** (pre-registration §7): Part 1's synthetic PASS does not discharge them. The executor re-runs Part 1's differential (adapter quantities equal the rail's sizing law with `LegSize` and `AddsRule.OFF`; live path equals replay for adds OFF and for refused zero-quantity entries, `shared_sizing_zero` / `zero policy quantity`) on the real signals with the frozen R1 vector, bound by the tuple hash `62d7ae19…671f`, read in place. Item 3 needs the #773 P-L1/R-SV seam carrying the frozen vector.
- **Evidence:** private, under `C:\Users\joshu\t00-step3-console\sfclear2-fg-<UTC>\` with a nonce'd `SHA256SUMS`; public output is pass/fail per item and hashes only, via `docs/evidence/PRIVATE_EVIDENCE.sha256` rows written by the coordinator.
- **Limits:** a public synthetic PASS or a private-input skip is not FG at R1. No scoring output is read or produced. FG FAIL means the run does not start (§6 VOID).

## Pre-mortem

- **Loop cost.** One targeted run plus mutants, one `fp test-ops`, one `fp check`.
- **Likely failure.** The three paths take different input shapes; a shared synthetic script needs adapters per path, built in the test file only.
- **What would make this moot:** none; FG items 2–3 are binding.
- **Evidence binding:** records at the returned head only.

[prereg]: https://github.com/Joshua-Asante/first-passage/blob/83867f0d362931c2a516a62b990bb1c209372527/docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
