# Q-SFCLEAR-2 run path A: P0 and personal instance identity (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** **DRAFT, not frozen, not dispatchable.** Drafted 2026-10-12 for the Deployment Coordinator. Freezing is the coordinator's act, and only after Joshua's admissions and rulings ([decision packet](../../notes/2026-10-12-q-sfclear-2-run-path-decision-packet.md) items 1, 2, 5, 7).

**Base:** `origin/main` `92bfca7`. Every `file:line` below is at that commit. `ops/`, `core/`, `lab/` and `tests/` are unchanged from the scope note's snapshot `a8769f8`, so its anchors carry.

**Parent scope:** [run-path scope note](../../notes/2026-10-12-q-sfclear-2-run-path-code-scope.md) §1 items 1 and 4, cross-component constraints, §2 packet A.

**Study (governs):** the FROZEN Q-SFCLEAR-2 [pre-registration at F `83867f0`][prereg] (not on main): §2 (R1, P0), §3 G0, §4 item 4, §6, §11 items 1 and 10. Where this card and the pre-registration differ, the pre-registration governs; a worker returns the conflict.

**Authority:** three separate acts (§11): G-1 Joshua's code admission, G-2 coordinator freeze, G-3 dispatch.

**Executor (proposed):** Codex local, single writer of `codex/sfclear2-a-p0-instance`, in a fresh worktree. Not GLM. **Exception, routing test 1:** the `core/firm_rules.py` edit (§2.2, step A0) is a `core/` anchor-path edit ([surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md) routing test 1), so it is the coordinator's commit, cut before the worker's branch. The worker never edits `core/`.

**Coordinator:** the Deployment Coordinator: freeze, A0, diff review, integration, PR, ledger.

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
  - no_production_source_edit
  - no_book_sizing_context_or_book_account_owner_edit
  - no_dd_protection_or_frozen_constant_edit
  - no_require_policy_loosening
  - no_lab_ops_import
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
  - tests/ops/test_personal_p0_policy.py
  - tests/ops/qualification/test_personal_p0_replay.py
  - tests/core/test_personal_tier_cap.py
  - tests/core/test_personal_tier.py
  - tests/ops/test_personal_drawdown_halt.py
  - tests/ops/test_book_policy.py
  - tests/ops/test_book_quantity_laws.py
  - tests/ops/test_book_capacity.py
  - tests/ops/test_policy_fingerprint.py
  - tests/ops/test_live_size_vector_sizing_context.py
  - tests/ops/test_tradeify_sizing_integration.py
  - tests/ops/qualification/test_replay.py
  - tests/ops/qualification/test_trust_domain.py
  - tests/ops/qualification/test_runtime_inventory.py
  - tests/ops/qualification/test_seal.py
  - tests/ops/qualification/test_composition_fixture.py
  - tests/ops/qualification/test_composition_route.py
  - tests/ops/test_c1_rail_image_manifest.py
  - tests/ops/test_c1_signal_daemon_image_manifest.py
```

The first three files are new. The rest exist and must stay green with no edit.

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

Read and report before any test. A contradiction is a **stop** (§7).

- **(a) Policy gate.** `ops/c1_rail/book_policy.py:101` `require_policy` admits only the fixed trailing instance; `:686` `settle` and `:703` `mode_for` derive next-session mode from settled equity; `:65` `ACCOUNT_MICRO_CAP` reads the Tradeify row (`TIER` at `:64`).
- **(b) Replay.** `ops/c1_rail/qualification/replay.py:245` (`BookReplay.__init__`), `:254` (`require_policy`), `:260` (`BookProtectionClock`), `:612` (size per leg), `:628` (`zero policy quantity`).
- **(c) Halt.** `ops/c1_rail/personal_drawdown_halt.py:46` (`_threshold` from `FIRM_RULES[tier]["max_dd_pct"]`), `:171` (`_breached`, rounded to 6 places), `:174` (`observe`, latch), `:189` (`flatten`, confirmation evidence). It is file-backed and is not in either inventory today.
- **(d) Cap.** `core/firm_rules.py:571` (`Personal_Tradovate`), `:580` (`micro_contract_cap: None`); `ops/c1_rail/book_capacity.py:178` (imported constant).
- **(e) Inventories.** `ops/c1_rail/qualification/trust_domain.py:140` (primary roles), `:156` (runtime dependencies; `book_policy`, `book_capacity`, `firm_rules`, `dd_protection` listed); `ops/c1_rail/policy_fingerprint.py:29` (`REQUIRED_COMPONENTS`: `firm_rules`, `book_policy`, `book_capacity`, `book_sizing_context`).
- **(f) P7 D8 closure.** The [C′ card](2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md) D8 list names `firm_rules.py`, `book_policy.py`, `replay.py` and `trust_domain.py` ("none may change"). Report whether that obligation is still open at the cut base. If it is open and G-1 does not name the H′ movement, **stop**.
- **(g) Callers.** `git grep -n "require_policy\|ACCOUNT_MICRO_CAP\|BookProtectionClock("` across `ops/` and `tests/`. Report every caller.

## 0.5. Routing and clarifying questions

Synthetic only; nothing gitignored is read, so a local Codex checkout suffices. Apply each default unless Phase 0 contradicts it; on a contradiction return `NEEDS_CONTEXT`.

- **(A) P0 is a named contract.** Add a distinct personal policy type (for example `PersonalP0Policy(tier="Personal_Tradovate")`) and a `require_personal_p0` validator in `book_policy.py`. `require_policy` and the Tradeify instance stay byte-equivalent in behaviour. No huge trigger, no fabricated `ProtectionPolicy` tuple.
- **(B) Mode.** Under P0 the replay's mode source returns NORMAL for every session at every equity. It never constructs `BookProtectionClock`.
- **(C) Halt boundary.** **Pending decision packet item 2.** Recommended: the replay calls the live halt's breach predicate. Extract `_breached`'s body into one pure module-level function in `personal_drawdown_halt.py` that `_breached` then calls, so live behaviour is unchanged. The replay imports that function. If Joshua rules the exact scorer predicate instead, the replay implements `20*(peak-trough) >= 3*peak` in ops (no lab import) and `personal_drawdown_halt.py` is not touched.
- **(D) Observed equity.** The replay observes account equity (realized plus open marks on the same bar marks the replay already uses) at each bar close. It does not observe any adapter's paper equity. The card names this sequence; the worker does not choose another one.
- **(E) Latch mechanics, not consequence.** This card builds only the live halt contract the replay mirrors: on a latch every entry and add is refused with a named reason (`personal_halt`), open positions flatten at the next bar under the existing cost model, a flatten counts as confirmed only when the replay's own position book is flat with no working order, and the replay emits one latch record (timestamp, peak, observed equity) in its output. Under the frozen reading (decision packet item 7, option (b)), these mechanics are the whole consequence: after a latch the replay adds no risk, so the remaining days come out as zero days and the §4 scorer scores the series as it stands. This card adds no verdict rule. If Joshua instead rules (a), E adds it; if (c), the card waits for the new pre-registration. The card is not frozen until item 7 is settled (Joshua confirms (b), or rules (a) or (c)).
- **(F) Cap.** Add `account_micro_cap(tier)` in `book_policy.py`. It reads the resolved tier row and refuses `None` or a non-positive int. `ACCOUNT_MICRO_CAP` stays the Tradeify value. `book_capacity.py` takes the cap from the resolved instance when one is passed; otherwise it uses today's constant.

## 1. Goal

A synthetic `BookReplay` can explicitly select the personal tier, its cap and P0. It stays NORMAL at every equity level, composes the admitted halt semantics and refuses risk after a latch. Every Tradeify output is unchanged.

**Not asked:**
- the live P0 consumer (`book_sizing_context.py`, `book_account_owner.py`; P4's queued outcome);
- the production factory (`production_source.py:1367`) and the startup cap literal (`:190`): card B, the single `production_source.py` writer (§9);
- the schedule, roll list and route output (B), fees (C).

## 2. Scope

### 2.1 Worker edits

- `book_policy.py`: §0.5 (A), (B), (F).
- `book_capacity.py`: §0.5 (F).
- `qualification/replay.py`: accept a `PersonalP0Policy`; select the P0 mode source; observe the halt per (C)–(E); refuse with `personal_halt`. The Tradeify path is unchanged.
- `personal_drawdown_halt.py`: only the (C) extraction, and only if item 2 is ruled "mirror live".
- `qualification/trust_domain.py`: add `c1_rail.personal_drawdown_halt` to the runtime-dependency tuple at `:156`, only if the replay imports it.

### 2.2 Step A0 (coordinator commit, before the worker cuts)

`core/firm_rules.py:580`: `micro_contract_cap` = `80` for `Personal_Tradovate` (D6, "keep the existing 80-micro cap source"; the study's D6 source, not a Tradovate venue maximum). Test: new `tests/core/test_personal_tier_cap.py`. `tests/core/test_personal_tier.py` must stay green unchanged.

### 2.3 Files

| File | Bound (§0(e)) | Edit |
|---|---|---|
| `core/firm_rules.py` | T+F | A0 only (coordinator) |
| `ops/c1_rail/book_policy.py` | T+F | §2.1 |
| `ops/c1_rail/book_capacity.py` | T+F | §2.1 |
| `ops/c1_rail/qualification/replay.py` | T | §2.1 |
| `ops/c1_rail/qualification/trust_domain.py` | T | one tuple entry, conditional |
| `ops/c1_rail/personal_drawdown_halt.py` | becomes T if imported | (C) extraction, conditional |
| `tests/core/test_personal_tier_cap.py` | — | new (A0) |
| `tests/ops/test_personal_p0_policy.py` | — | new |
| `tests/ops/qualification/test_personal_p0_replay.py` | — | new |

**Forbidden files:** `core/dd_protection.py`, `core/lifecycle.py`, `core/dd_geometry.py`, any other `core/` file; `ops/c1_rail/qualification/production_source.py`; `ops/c1_rail/book_sizing_context.py`; `ops/c1_rail/book_account_owner.py`; `ops/c1_signal_daemon/book_bundle_execution.py`; `ops/c1_rail/policy_fingerprint.py`; every `lab/` file; every existing test or fixture; Pine, ports, `effective_inputs.json`.

## 3. Method

1. Phase 0 (§0); post findings.
2. Coordinator lands A0; the worker cuts `codex/sfclear2-a-p0-instance` from it in a fresh worktree.
3. Write the §4 rows. Record the **red** run at the cut.
4. Make §2.1. Record **green**, then the acceptance list.
5. `python -I scripts/fp.py test-ops` and `python -I scripts/fp.py check`; cite each `record.json`.
6. Stage only §2.3 files; check the commit message against `git diff --cached`; push; return (§6).

A PR touching `ops/c1_rail/qualification/**` or `book_policy.py` triggers the Qualification S2 supervision workflow (`.github/workflows/qualification-s2-supervision.yml:33-55`). The coordinator owns that run.

## 4. Acceptance checks (falsifier-first)

**Hypothesis:** `N/A`. This executes scope note §2 packet A.

| Row | Test | Fails if |
|---|---|---|
| P1 | Exact threshold: equity at exactly 15% below peak latches. Clear of the boundary: a drawdown of `0.15 − 1e-5` does not latch and `0.15 + 1e-5` does, a margin ten times the 6-place rounding grain (`1e-6`) of `personal_drawdown_halt.py:171`, so the result does not depend on item 2. The within-grain cases are P2's | The boundary is wrong in either direction |
| P2 | Boundary predicate is the ruled one (item 2): a case where rounding and exact differ (drawdown `0.1499996`) latches under "mirror live" and does not under "exact" | The replay uses the other predicate |
| P3 | New peak, then breach measured from the new peak; recovery above peak before breach never latches | Peak tracking is wrong |
| P4 | At every synthetic equity level, including below 1.5% of peak, mode is NORMAL; `BookProtectionClock` is never constructed under P0 | Any PROTECTED transition |
| P5 | After a latch every entry and add refuses `personal_halt`; positions flatten at the next bar; zero authorization for the rest of the run | Risk added after a latch |
| P6 | A working order or unconfirmed flat at latch keeps the flatten owed and blocks risk | Uncertain flatten treated as confirmed |
| P7 | Tradeify replay outputs (quantities, modes, rejections) on the existing fixtures are byte-equal to the cut base | Tradeify behaviour changed |
| P8 | `account_micro_cap("Personal_Tradovate") == 80`; `None`, `0`, `-1`, `True` refuse; capacity refuses above the resolved cap | The resolved cap is ignored |
| P9 | `core/mc/preflight.py:249` on a synthetic fixture behaves as `tests/core/test_personal_tier.py` expects (refusal is not clearance) | Preflight treated as clearance |

**Named mutants (each must turn a row red):** M-A1 force the old clock under P0 (P4); M-A2 omit halt observation (P1, P5); M-A3 substitute the Tradeify instance for the personal one (P4, P8); M-A4 ignore the resolved cap (P8); M-A5 swap the boundary predicate (P2).

**Revert trigger:** any listed existing suite changes outcome, or P7 diffs.

## 5. Forbidden

- No real-data run; no private read (no `t00-step3-console`, Pine, ports, `effective_inputs.json`, `E_0`).
- No edit to `dd_protection`, `DD_TRIGGER`/`DD_SCALE`, `CANDIDATE_SCALE`, `BASE_RISK`, lifecycle multipliers or the Tradeify policy instance; no loosening of `require_policy`.
- No `lab↔ops` import.
- No edit outside §2.3; no "while I was in there" refactor.
- GLM, a push to `main`, a merge, or opening a PR.

## 6. Return (status taxonomy)

| Status | When |
|---|---|
| `DONE` | §4 red at the cut, green on the build; mutants killed; suites green; `fp test-ops` and `fp check` records completed exit 0; footprint equals §2.3 |
| `DONE_WITH_CONCERNS` | As DONE, with an off-pattern observation |
| `NEEDS_CONTEXT` | A §0.5 default contradicted, or item 2 or item 7 not settled at dispatch |
| `BLOCKED — context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong` | As named; `plan-itself-wrong` covers §0(f) |

**Gate verdict (coordinator, at review):** **RESOLVED** when `DONE` and both §7 passes reproduce it; **FALSIFIED** when a row cannot be made red at the cut, a mutant survives, or the revert trigger fires; **AMBIGUOUS** (held) on `DONE_WITH_CONCERNS`.

**Report:** status; red/green and mutant records; suite records; `git diff --name-only <cut>..HEAD`; concerns.

## 7. Stop conditions and parent review

**Stop and return:** §0(f) open without H′ in G-1; a listed suite fails at the cut; a row cannot be made red; green needs a file outside §2.3; any edit would touch `production_source.py`.

**Parent review (coordinator):** Pass 1, the diff equals §2.3 and Tradeify paths are untouched; Pass 2, re-run §4 and the mutants from a clean worktree at the returned head.

## 8. Out of scope and decision unlocked

**Out of scope:** live P0 (P4), the production factory (B), B–E.

**Unlocks:** B can bind the personal instance, cap and P0 in the production source.

## 9. Sequencing and file collisions

- **`production_source.py` single writer:** card B's writer is the only writer of `production_source.py` across A, B and C. A does not edit it; C does not edit it under either fee option (C card §9). Order: A merges → (C merges, independent of the file) → B cuts from a base containing A.
- `book_account_owner.py` order stays GC-5-DISPLACED → TB-I3 S2 → P-L2 → P4; A does not enter that queue.
- `book_policy.py` and `firm_rules.py` are P7 D8 paths and TB-I1 components: A moves the Tradeify fingerprint and trust-domain digests (decision packet item 1).

## 10. Audit hooks (runnable)

```bash
python -I scripts/check_brief.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-run-path-a-p0-instance-card-DRAFT.md --type cc_handoff
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-run-path-a-p0-instance-card-DRAFT.md
git diff --name-only <cut>..HEAD   # expect a subset of §2.3, no core/ file
git diff <cut>..HEAD -- ops/c1_rail/book_policy.py | grep -n "def require_policy"   # expect no hunk
python -I scripts/fp.py python -m pytest <the authority-block acceptance list>
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
```

## 11. Gates (the card is NOT DISPATCHABLE until all three hold)

- **G-1. Joshua's code admission.** He names the §2.3 bound files, knowing they move TB-I1 and trust-domain digests and touch P7 D8 paths (decision packet item 1), and rules items 2 and 7. **Not recorded.**
- **G-2. Coordinator freeze.** Answers §12; commits the frozen revision; records its SHA. **Not done.**
- **G-3. Dispatch.** The coordinator's dispatch record, after A0 lands. **Not done.**

## 12. Open decisions (coordinator at freeze; Joshua where marked)

- **D-1 (Joshua, item 2).** Replay halt boundary.
- **D-2 (Joshua, item 1).** Admission of the §2.3 footprint, including the conditional rows.
- **D-3 (Joshua, item 7).** Joshua confirms the frozen reading (b), or rules (a) or (c). This card's mechanics implement (b) and emit the latch record under every option.
- **D-4.** Confirm (D) observed equity against pre-registration §2.

## Pre-mortem

- **Loop cost.** One targeted run, one `fp test-ops`, one `fp check`, plus the S2 workflow. A third full run is a checkpoint.
- **Likely failure.** The trust-domain runtime collector refuses a new import not listed in `:156`; that is the conditional row, not a workaround.
- **What would make this moot:** Joshua ruling P0 into the live owner first (P4), so A follows P4's contract.
- **Evidence binding:** records at the returned head only; a push after green voids them.

[prereg]: https://github.com/Joshua-Asante/first-passage/blob/83867f0d362931c2a516a62b990bb1c209372527/docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
