# Vanguard MGC fixed-stop edition — produce the private edition files (bounded local handoff)

**Status:** DRAFT. **Not dispatchable** until every §0 gate holds. It runs only on the operator's primary checkout, because the private Pine, port and effective inputs exist nowhere else. Commit this packet before dispatch and record the dispatch revision in §6.

**Selected outcome:** the private files that realize [`vanguard_mgc_fixed_stop_oso@Tradeify_Select_100K`](../pre-registration/2026-09-26-tradeify-vanguard-fixed-stop-edition-prereg.md), exactly as the pre-registration's answered rules state:
- a new edition Pine for a code edition, or the explicitly retained compatible Pine identity for an override-only edition;
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
| G2a | Realization and identity-binding scheme are specified (reused pins fixed; new output digests supplied by this packet) under pre-registration §4, including compatibility of the port-embedded Pine identity with the registry. Any required identity-contract change is separately reviewed before dispatch. | Pre-registration at G2 commit; separate identity review if needed |
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

**Outputs:** new files only where the ruled realization requires them, in the same private roots as the originals, with names that carry the edition id. R1 retains the existing compatible Pine and port; R2 produces a new matching pair:
- `core/strategies/book/Vanguard_Gold_MGC_v0.4_fixed_stop_oso.pine` for R2 only;
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
  - **(R1) Override-only.** The pre-registration §4 row says trailing is removed by an effective-input override. The edition keeps the existing compatible Pine and port identities and changes only a successor effective-inputs binding. No new Pine or port file. If a changed Pine is required, the unchanged port cannot satisfy the current loader: choose the operator-ruled R2 realization or return BLOCKED pending a separately reviewed identity contract. Never disable the embedded PINE_SHA256 check.
  - **(R2) Code edition.** Trailing and any other ruled changes live in new private Pine and port files. The new port embeds the new Pine digest; any leg identity must match the ruled registry binding. Classify identity-only changes separately from VAN behavior changes.

  If the pre-registration doesn't make the choice unambiguous, stop and return.
- [ ] **Apply exactly the answered rules, and nothing else:**
  - **VAN-1:** no trailing fields on any bracket, whether entry, scale-in or amend.
  - **VAN-2:** the stop level at entry, as ruled.
  - **VAN-3:** the existing exit named. No new exit logic.
  - **VAN-4:** amend behaviour after entry, as ruled.
  - **VAN-5:** the port keeps emitting **one** intent per signal, which the rail admits and sizes once (`BookLegExecution.admit`, `ops/c1_signal_daemon/book_bundle_execution.py:142-182`, which refuses a second entry on a non-empty leg). The split into one-contract requests is a post-admission rail dependency (T09 / TB-I3, incident ADR §A8 rules 9–10), **not port work**. Do not make the port emit N requests. The ruled maximum is the admitted-quantity bound, and the port applies no split logic.
  - **VAN-6:** partial-acknowledgement and counter behaviour, as ruled.
  - **VAN-7:** breakeven and grace stay inactive.

  Every changed line must trace to one of these rules or to the accepted §4 identity binding. The signal, setup, entry and add-eligibility logic is byte-identical to the original.
- [ ] **Static verification (no execution):**
  1. Produce a line diff of each new file against its original, and classify every hunk by the VAN rule or accepted identity binding it implements. Inspect diffs in place without retained source extracts. Unclassified hunks fail.
  2. Under the exact pinned effective configuration, show that every reachable port bracket construction yields null trailing fields and every reachable Pine exit omits active trailing arguments. Cover entry, scale-in and managed-bar amendments. Retained unreachable trailing code is permitted for R1; an unconditional claim that the source contains no trailing path is not required. Missing or different effective settings invalidate this proof.
  3. Verify the identity tuple against the current loader contract without importing the private port: embedded Pine identity equals the proposed registration Pine identity, and port digest and leg identity match the proposed binding, and effective inputs bind the inspected configuration. Unresolved compatibility fails. For any successor effective inputs, show that only the ruled keys change and bind both Pine and port settings to the same declared behavior. Recompute the runtime digest through `.\fp.ps1 python` with the registry's derivation, exactly as the determination did. Do not import or execute the port.
  4. A Python syntax check of the new port (`py_compile`) is allowed **only if** the G3 authorization permits it. Otherwise skip it and say so.
- [ ] **Hash.** SHA-256 each new file, plus any successor effective inputs and runtime digest in either realization.
- [ ] **Stop.** Do not update pins, the manifest, the ledger or the pre-registration. List those as owed follow-ups.

## 4. Forbidden

- Running, importing or backtesting any edition or original, in Python or TradingView.
- Any change not traceable to an answered VAN rule or the accepted identity-binding scheme. This includes "cleanup", refactoring, renames inside the file, and changes to comments that alter behaviour.
- Adding a CrossTrade-managed trail, a new exit, a new filter or any parameter change beyond the explicitly ruled edition settings.
- Editing the accepted files, the pre-registration or any governance document.
- Freezing the pre-registration, or treating the edition as qualified.

## 5. Owed follow-ups (not this packet)

1. A reviewed change adding the edition pins beside the existing ones (`book_adapters.py`, and `BOOK_SOURCES.sha256` or `PORT_MANIFEST.sha256` per convention). For any successor effective inputs, it also adds the source and runtime digests.
2. Filling the pre-registration §4 pin rows with this return's hashes, then the operator freeze (pre-registration §8 steps 4–5).
3. Adding a venue-edition ledger row `vanguard_mgc_fixed_stop_oso` as `CANDIDATE`.
4. Requalification through the book's production E1 (pre-registration §6).

## 6. Executor return

**Status:** not dispatched.

| Field | Value |
|---|---|
| Executor / dispatch revision | |
| Gates G1–G4, including G2a (evidence link each) | |
| Pre-registration commit built against | |
| Checkout revision, tree state, `doctor` result | |
| Input hashes (3 rows, match/mismatch) | |
| Realization (R1 / R2) and where the pre-registration rules it | |
| `git check-ignore` result for each output path | |
| New file paths and SHA-256 | |
| Effective-input source and runtime digests (reused or successor) | |
| Hunk classification (rule → `file:line` in new files) | |
| Identity tuple and loader compatibility (static evidence) | |
| No-trailing proof under pinned effective configuration (port and Pine, file:line) | |
| Syntax check (run / skipped and why) | |
| Deviations or stops | |
| Follow-ups owed (§5) | |

**Coordinator disposition:** pending.
