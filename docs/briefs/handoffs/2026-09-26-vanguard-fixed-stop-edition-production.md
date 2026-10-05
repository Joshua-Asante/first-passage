# Vanguard MGC fixed-stop edition — produce the private edition files (bounded local handoff)

**Status:** DRAFT. **Not dispatchable** until every §0 gate holds. It runs only on the operator's primary checkout, because the private Pine, port and effective inputs exist nowhere else. Commit this packet before dispatch and record the dispatch revision in §6.

**Selected outcome:** the private files that realize [`vanguard_mgc_fixed_stop_oso@Tradeify_Select_100K`](../pre-registration/2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md), exactly as the pre-registration's answered rules state *[Retargeted 2026-10-02 ([PR #590](https://github.com/Joshua-Asante/first-passage/pull/590) item 7.6.1): the original pre-registration is CLOSED — replay-output exposure; this points to its successor. Ratification and disclosure completeness were recorded on 2026-10-03 in successor §7; the successor is still NOT FROZEN.]*:
- retain the accepted Pine and port bytes and identities (A1, override-only);
- realize the ruled settings through the one book-wide successor effective-settings file shared with ORB;
- return the retained identities and the shared settings source/runtime digests. The coordinator binds one path, one writer and sibling sequencing before dispatch; an unset binding blocks production.

This is step 3 of the pre-registration's §8 freeze procedure. The edition implements answered rules and designs nothing new.

**Ownership:**
- One local executor, named at dispatch.
- The operator authorizes file creation (§0 G3), answers every rule and freezes the pre-registration.
- The coordinator accepts the return.
- Pin registration in `book_adapters.py`, `ops/c1_rail/book_policy.py`, `BOOK_SOURCES.sha256` or the ledger is a **separate reviewed change**, not this packet.

**Return boundary:** the single authorized successor settings file (or its identity when the sibling writer supplies it), retained Pine/port identities and §6 only. No replay, E1, screen, backtest, TradingView run, account access, alert, drill or spend. No edits to any existing Pine, port, manifest, registry, pre-registration or campaign record.

## 0. Dispatch gates (all must hold; otherwise return `BLOCKED — <gate>`)

| Gate | Condition | Where it is recorded |
|---|---|---|
| G1 | Operator ruled **option A** (fixed-stop edition), not B (reject the leg) | Campaign record §59, or a dated operator ruling linked from it |
| G2 | Pre-registration VAN-2 to VAN-6, the §4 effective-inputs row, the §6 replay choice and the §6 sequential-exit replay model are answered in words. No `OWED` remains in §3, §4 or §6, apart from the pin rows this packet fills. *2026-10-02: on the successor, the §6 sequential-exit replay model is moot for the first release under C-a (successor §6 and its exit-split row, ratified 2026-10-02 (sitting 2); [PR #590](https://github.com/Joshua-Asante/first-passage/pull/590) item 7.2). Successor §7 records ratification and disclosure completeness on 2026-10-03; those settled decisions are not outstanding gates. All other freeze requirements remain.* | The pre-registration file at a named commit |
| G2a | Realization and identity-binding scheme are specified (reused pins fixed; new output digests supplied by this packet) under pre-registration §4, including compatibility of the port-embedded Pine identity with the registry. Any required identity-contract change is separately reviewed before dispatch. *2026-10-02: scheme ruled (operator ruling 2026-10-02 (sitting 2)): Vanguard A1 (input-only, shared successor settings file with ORB), leg_id kept. Use R1 below; no new Pine or port. The coordinator records the shared settings path, single writer and sequential sibling execution before dispatch.* | Pre-registration at G2 commit; separate identity review if needed |
| G3 | Operator explicitly authorizes an agent to **create** new private edition files under the paths in §2. §60 grants read access only. | Dispatch message or campaign record |
| G3b | **Allocation gate (operator ruling 2026-09-26: "Yes, gate on allocation").** Producing the edition files waits until the TradingView/CrossTrade [capability allocation and deletion map](2026-09-25-tradeify-capability-allocation-deletion-map.md) is **ACCEPTED** under gate D of the checklist's [T09 gate acceptance record](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t09-gate-acceptance-record), and the accepted map keeps Vanguard's runtime port as the controller boundary. A committed or merged map is not acceptance. If the accepted allocation delegates this behavior, this packet is withdrawn, not run. | Checklist T09 gate D acceptance record (named revision); allocation map disposition |
| G4 | The pre-registration is **not frozen**, and no replay or E1 output exists for the edition *2026-10-02: this gate now binds the successor and is scoped in time. It means no replay or E1 output on the edition produced after the successor's first commit (`e85d321`). Output produced before that commit is disclosed in successor §D and governed there and by its ratified §7 successor-validity reading; it does not fail this gate. The successor's standing rule §R forbids any candidate-configurable replay before freeze.* | Pre-registration Status line; campaign record |

Record the pre-registration commit the executor builds against, and the sibling ORB/Striker pre-registration commit whose ruled ORB settings the shared successor settings carry. If either changes after its recorded commit, stop and return; do not reconcile.

## 1. Read first

- The [pre-registration](../pre-registration/2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md) at the G2 commit. It is the **only** specification.
- [Trailing determination §5](2026-09-26-vanguard-mgc-trailing-determination.md#5-executor-return), for the port and Pine locations of the trailing, breakeven and grace branches. It recorded `file:line` anchors only; re-read the source, don't trust those anchors blindly.
- Campaign record §59 and §60, and AGENTS.md "Public-clone posture": the handling rules.
- The sibling [ORB/Striker pre-registration](../pre-registration/2026-10-02-tradeify-route-native-editions-successor-prereg.md), for the file and pin conventions its editions use. The ORB and Vanguard handoffs consume one shared settings identity. One named writer produces it and the other executor returns its static proof against that same digest; execute sequentially with one pinning convention.

## 2. Inputs, outputs and handling

**Inputs (read in place, verify first):** the accepted Vanguard Pine `af26899c…`, port `e6a03d04…` and `effective_inputs.json` `66406dee…`, at the paths pinned in `core/strategies/BOOK_SOURCES.sha256` and `ops/c1_signal_daemon/book_adapters.py:51-55`. Hash each file before use. A mismatch stops the work.

**Outputs:** Vanguard A1 retains the accepted Pine and port; no new Pine or port is produced. Only the named shared settings writer may create the successor effective-settings file at the private path explicitly authorized under G3. The sibling executor consumes that same identity. Never overwrite the accepted effective settings or create an independent per-leg settings file.

Before writing anything, confirm with `git check-ignore -v` that every output path is ignored. If a path is not ignored, stop: a tracked private file would be published.

**Handling:**
- Never modify, rename or overwrite the accepted Pine, port or effective inputs.
- Never copy any private file outside the primary checkout's private roots: no worktree, scratch directory, clone or external service (§60).
- Nothing private enters a tracked file, PR, comment or this packet. §6 records behavior as shapes, plus hashes and `file:line` references into the new files.

## 3. Steps

- [ ] **Environment and baseline.** Run `.\fp.ps1 doctor`. Record the checkout revision, tree state, the G2 pre-registration commit and the sibling ORB/Striker pre-registration commit. Hash the three inputs.
- [ ] **Use the ruled A1 / R1 override-only realization.** Retain the compatible Pine and port identities. Apply only the answered settings to the one shared successor file; if the sibling writer supplies it, verify its identity instead of creating another file. A changed Pine cannot satisfy the unchanged port's embedded identity: return BLOCKED for a separately ruled code edition or reviewed identity contract. Never disable the loader checks.
- [ ] **Apply exactly the answered rules, and nothing else:**
  - **VAN-1:** no trailing fields on any bracket, whether entry, scale-in or amend.
  - **VAN-2:** the stop level at entry, as ruled.
  - **VAN-3:** the existing exit named. No new exit logic.
  - **VAN-4:** amend behaviour after entry, as ruled.
  - **VAN-5:** the port keeps emitting **one** intent per signal, which the rail admits and sizes once (`BookLegExecution.admit`, `ops/c1_signal_daemon/book_bundle_execution.py:142-182`, which refuses a second entry on a non-empty leg). The split into one-contract requests is a post-admission rail dependency (T09 / TB-I3, campaign §59 Ruling 5 and the UB-4 freeze; the T09 acceptance case must prevent child k+1 after transport loss on child k), **not port work**. Do not make the port emit N requests. The ruled maximum is the admitted-quantity bound, and the port applies no split logic.
  - **VAN-6:** partial-acknowledgement and counter behaviour, as ruled.
  - **VAN-7:** breakeven and grace stay inactive.

  Every changed line must trace to one of these rules or to the accepted §4 identity binding. The signal, setup, entry and add-eligibility logic is byte-identical to the original.
- [ ] **Static verification (no execution):**
  1. Verify the retained Pine/port hashes are unchanged. Diff the shared successor settings against the accepted settings in place, and classify every hunk by its ruled ORB/VAN setting or accepted identity binding. Inspect diffs in place without retained source extracts. Unclassified hunks fail.
  2. Under the exact pinned effective configuration, show that every reachable port bracket construction yields null trailing fields and every reachable Pine exit omits active trailing arguments. Cover entry, scale-in and managed-bar amendments. Retained unreachable trailing code is permitted for R1; an unconditional claim that the source contains no trailing path is not required. Missing or different effective settings invalidate this proof.
  3. Verify the identity tuple against the current loader contract without importing the private port: embedded Pine identity equals the proposed registration Pine identity, and port digest and leg identity match the proposed binding, and effective inputs bind the inspected configuration. Unresolved compatibility fails. For any successor effective inputs, show that only the ruled keys change and bind both Pine and port settings to the same declared behavior. Recompute the runtime digest through `.\fp.ps1 python` with the registry's derivation, exactly as the determination did. Do not import or execute the port.
  4. There is no new port to syntax-check under A1. Classify each reachable amend as a broker mutation or a rail no-op under the ruled settings; retain the production protection-read and tick-rounded equality obligations. Static evidence does not discharge route or E1 acceptance.
- [ ] **Hash.** Return the retained Pine/port identities and the shared successor settings source/runtime digests.
- [ ] **Stop.** Do not update pins, the manifest, the ledger or the pre-registration. List those as owed follow-ups.

## 4. Forbidden

- Running, importing or backtesting any edition or original, in Python or TradingView.
- Any change not traceable to an answered VAN rule or the accepted identity-binding scheme. This includes "cleanup", refactoring, renames inside the file, and changes to comments that alter behaviour.
- Adding a CrossTrade-managed trail, a new exit, a new filter or any parameter change beyond the explicitly ruled edition settings.
- Editing the accepted files, the pre-registration or any governance document.
- Freezing the pre-registration, or treating the edition as qualified.

## 5. Owed follow-ups (not this packet)

1. A separately reviewed registration change retaining the Pine/port pins and binding the shared successor settings identity (`book_adapters.py` and `ops/c1_rail/book_policy.py`, which must carry the same Pine pin as the port's embedded identity (`tests/ops/test_book_adapters_parity.py:69`), and `BOOK_SOURCES.sha256` or `PORT_MANIFEST.sha256` per convention). The shared successor settings require reviewed source and runtime digest constants; override-only does not mean registration is code-free.
2. Filling the pre-registration §4 pin rows with this return's hashes, then the operator freeze (pre-registration §8 steps 4–5). *[2026-10-02, on the successor: the steps after production are the successor-validity ruling (§8 step 4), the §10 audit with §4 filled (step 5), the trailing-removal confirmation and operator freeze (step 6), and the full §10 re-audit in the freeze commit (step 7).]*
3. Adding a venue-edition ledger row `vanguard_mgc_fixed_stop_oso` as `CANDIDATE`.
4. Requalification through the book's production E1 (pre-registration §6).

## 6. Executor return

**Status:** not dispatched.

| Field | Value |
|---|---|
| Executor / dispatch revision | |
| Gates G1–G4, including G2a and G3b (evidence link each) | |
| Pre-registration commit built against (and the sibling ORB/Striker pre-registration commit for the shared settings) | |
| Checkout revision, tree state, `doctor` result | |
| Input hashes (3 rows, match/mismatch) | |
| Realization and governing rule | A1 / R1; successor §4 |
| `git check-ignore` result for each output path | |
| Retained identities and shared settings writer/path/digest | |
| Effective-input source and runtime digests (reused or successor) | |
| Hunk classification (rule → `file:line` in new files) | |
| Identity tuple and loader compatibility (static evidence) | |
| No-trailing proof under pinned effective configuration (port and Pine, file:line) | |
| Syntax check (run / skipped and why) | |
| Deviations or stops | |
| Follow-ups owed (§5) | |

**Coordinator disposition:** pending.
