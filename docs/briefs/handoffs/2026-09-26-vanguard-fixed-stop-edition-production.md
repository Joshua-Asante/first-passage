# Vanguard MGC fixed-stop edition — produce the private edition files (bounded local handoff)

**Status:** DRAFT. **Not dispatchable** until every §0 gate holds. It runs only on the operator's primary checkout, because the private Pine, port and effective inputs exist nowhere else. Commit this packet before dispatch and record the dispatch revision in §6.

**Selected outcome:** the private files that realize [`vanguard_mgc_fixed_stop_oso@Tradeify_Select_100K`](../pre-registration/2026-09-26-tradeify-vanguard-fixed-stop-edition-prereg.md), exactly as the pre-registration's answered rules state:
- a new edition Pine;
- a new edition runtime port, or an effective-input successor if the ruled realization is override-only;
- their SHA-256 digests.

This is step 3 of the pre-registration's §8 freeze procedure. The edition implements answered rules and designs nothing new.

**Ownership:**
- One local executor, named at dispatch.
- The operator authorizes file creation (§0 G3), answers every rule and freezes the pre-registration.
- The coordinator accepts the return.
- Pin registration in `book_adapters.py`, `BOOK_SOURCES.sha256` or the ledger is a **separate reviewed change**, not this packet.

**Return boundary:** new private files plus §6 only. No replay, E1, screen, backtest, TradingView run, account access, alert, drill or spend. No edits to any existing Pine, port, manifest, registry, pre-registration or campaign record.

## 0. Dispatch gates (all must hold; otherwise return `BLOCKED — <gate>`)

| Gate | Condition | Where it is recorded |
|---|---|---|
| G1 | Operator ruled **option A** (fixed-stop edition), not B (reject the leg) | Campaign record §59, or a dated operator ruling linked from it |
| G2 | Pre-registration VAN-2 to VAN-6, the §4 effective-inputs row and the §6 replay choice are answered in words. No `OWED` remains in §3 or §4, apart from the pin rows this packet fills. | The pre-registration file at a named commit |
| G3 | Operator explicitly authorizes an agent to **create** new private edition files under the paths in §2. §60 grants read access only. | Dispatch message or campaign record |
| G4 | The pre-registration is **not frozen**, and no replay or E1 output exists for the edition | Pre-registration Status line; campaign record |

Record the pre-registration commit the executor builds against. If the pre-registration changes after that commit, stop and return; do not reconcile the two.

## 1. Read first

- The [pre-registration](../pre-registration/2026-09-26-tradeify-vanguard-fixed-stop-edition-prereg.md) at the G2 commit. It is the **only** specification.
- [Trailing determination §5](2026-09-26-vanguard-mgc-trailing-determination.md#5-executor-return), for the port and Pine locations of the trailing, breakeven and grace branches. It recorded `file:line` anchors only; re-read the source, don't trust those anchors blindly.
- Campaign record §59 and §60, and AGENTS.md "Public-clone posture": the handling rules.
- The sibling [ORB/Striker pre-registration](../pre-registration/2026-09-25-tradeify-route-native-editions-prereg.md), for the file and pin conventions its editions use. If both are being produced, use the same convention.

## 2. Inputs, outputs and handling

**Inputs (read in place, verify first):** the accepted Vanguard Pine `af26899c…`, port `e6a03d04…` and `effective_inputs.json` `66406dee…`, at the paths pinned in `core/strategies/BOOK_SOURCES.sha256` and `ops/c1_signal_daemon/book_adapters.py:51-55`. Hash each file before use. A mismatch stops the work.

**Outputs:** new files only, in the same private roots as the originals, with names that carry the edition id:
- `core/strategies/book/Vanguard_Gold_MGC_v0.4_fixed_stop_oso.pine`;
- `ops/c1_signal_daemon/ports/vanguard_mgc_fixed_stop_oso.py`, or no new port if the ruled realization is override-only (see §3);
- where the pre-registration §4 row calls for it, a successor effective-inputs file beside the original.

Before writing anything, confirm with `git check-ignore -v` that every output path is ignored. If a path is not ignored, stop: a tracked private file would be published.

**Handling:**
- Never modify, rename or overwrite the accepted Pine, port or effective inputs.
- Never copy any private file outside the primary checkout's private roots: no worktree, scratch directory, clone or external service (§60).
- Nothing private enters a tracked file, PR, comment or this packet. §6 records behavior as shapes, plus hashes and `file:line` references into the new files.

## 3. Steps

- [ ] **Environment and baseline.** Run `.\fp.ps1 doctor`. Record the checkout revision, tree state and the G2 pre-registration commit. Hash the three inputs.
- [ ] **Choose the realization the pre-registration ruled, not one you prefer:**
  - **(R1) Override-only.** The pre-registration §4 row says trailing is removed by an effective-input override. The edition then keeps the existing port code (`e6a03d04…`) and changes only a successor effective-inputs file. The edition Pine sets the matching input. No new port file.
  - **(R2) Code edition.** Trailing and any other ruled changes live in new copies of the Pine and port.

  If the pre-registration doesn't make the choice unambiguous, stop and return.
- [ ] **Apply exactly the answered rules, and nothing else:**
  - **VAN-1:** no trailing fields on any bracket, whether entry, scale-in or amend.
  - **VAN-2:** the stop level at entry, as ruled.
  - **VAN-3:** the existing exit named. No new exit logic.
  - **VAN-4:** amend behaviour after entry, as ruled.
  - **VAN-5:** the split, as ruled.
  - **VAN-6:** partial-acknowledgement and counter behaviour, as ruled.
  - **VAN-7:** breakeven and grace stay inactive.

  Every changed line must trace to one of these rules. The signal, setup, entry and add-eligibility logic is byte-identical to the original.
- [ ] **Static verification (no execution):**
  1. Produce a line diff of each new file against its original, and classify every hunk by the VAN rule it implements. Unclassified hunks fail.
  2. Show that no path in the new port can build a `Bracket` with non-null `trail_activation_ticks` or `trail_offset_ticks`. Show that no new-Pine `strategy.exit` passes `trail_points`, `trail_price` or `trail_offset` reachable under the edition's effective inputs.
  3. If R1, show that the successor effective inputs change only the ruled key(s). Recompute the runtime digest through `.\fp.ps1 python` with the registry's derivation, exactly as the determination did. Do not import or execute the port.
  4. A Python syntax check of the new port (`py_compile`) is allowed **only if** the G3 authorization permits it. Otherwise skip it and say so.
- [ ] **Hash.** SHA-256 each new file, plus the successor effective inputs and runtime digest if R1.
- [ ] **Stop.** Do not update pins, the manifest, the ledger or the pre-registration. List those as owed follow-ups.

## 4. Forbidden

- Running, importing or backtesting any edition or original, in Python or TradingView.
- Any change not traceable to an answered VAN rule. This includes "cleanup", refactoring, renames inside the file, and changes to comments that alter behaviour.
- Adding a CrossTrade-managed trail, a new exit, a new filter or any parameter change.
- Editing the accepted files, the pre-registration or any governance document.
- Freezing the pre-registration, or treating the edition as qualified.

## 5. Owed follow-ups (not this packet)

1. A reviewed change adding the edition pins beside the existing ones (`book_adapters.py`, and `BOOK_SOURCES.sha256` or `PORT_MANIFEST.sha256` per convention). If R1, it also adds the successor effective-inputs digest.
2. Filling the pre-registration §4 pin rows with this return's hashes, then the operator freeze (pre-registration §8 steps 4–5).
3. Adding a venue-edition ledger row `vanguard_mgc_fixed_stop_oso` as `CANDIDATE`.
4. Requalification through the book's production E1 (pre-registration §6).

## 6. Executor return

**Status:** not dispatched.

| Field | Value |
|---|---|
| Executor / dispatch revision | |
| Gates G1–G4 (evidence link each) | |
| Pre-registration commit built against | |
| Checkout revision, tree state, `doctor` result | |
| Input hashes (3 rows, match/mismatch) | |
| Realization (R1 / R2) and where the pre-registration rules it | |
| `git check-ignore` result for each output path | |
| New file paths and SHA-256 | |
| Successor effective-inputs SHA-256 and runtime digest (R1 only) | |
| Hunk classification (rule → `file:line` in new files) | |
| No-trailing proof (port and Pine, `file:line`) | |
| Syntax check (run / skipped and why) | |
| Deviations or stops | |
| Follow-ups owed (§5) | |

**Coordinator disposition:** pending.
