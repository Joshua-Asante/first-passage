# Q-SFCLEAR-2 FG evidence run: private executor card (card D, Part 2)

**Type:** cc_handoff (private executor card)

**Status:** **FROZEN 2026-10-12** by the Deployment Coordinator (single writer of this card, by Joshua's 2026-10-12 "you own #808, keep writing it") at the commit that adds this line, after §13's resolutions and Joshua's rulings (D-5/D-6 "as recommended"; E_0 transfer and the FG seam "yes to both"). **Not dispatched.** Dispatchable only when §0 and §11 hold: cards A, B, D Part 1 merged, P-L2/P-L3 merged (done), the driver reviewed and its hash bound, D-4 measurements recorded, the digest-only run manifest built, and Joshua's per-run VM access opened.

**Base:** `origin/main` `158bf2a` for every `file:line`. The run head is a later clean `main` commit that holds every §0(a) predecessor.

**Parent:** the FROZEN [Q-SFCLEAR-2 pre-registration at F `83867f0`][prereg] (governs): §7 routes, FG items 1–3 and the run-record rules; §6 (VOID when FG is not PASS: the run must not start; nonce rule); §5; §10 hooks 1, 4 and 6. The parent card is [run-path card D](2026-10-12-q-sfclear-2-run-path-d-fg-parity-card-DRAFT.md) §13 (FROZEN). Item rulings come from the [decision packet](../../notes/2026-10-12-q-sfclear-2-run-path-decision-packet.md) (2 mirror; 3 b; 4 PR for all legs, so RS and FG-T are not used; 6 b, VM; 7 b). The host exception is the [campaign §60 addendum 2026-10-12][s60].

**Executor:** an authorized Claude executor, a single session, attended. Not GLM, not Codex, and no other external service.

**Coordinator:** the Deployment Coordinator. It owns the freeze, the dispatch, review, the `PRIVATE_EVIDENCE.sha256` row and every public line.

```yaml authority
seat: worker
parent: docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
max_risk: low
capabilities: [repository.read, tests.run]
constraints:
  - not_dispatchable_until_section_11_gates_recorded
  - fg_items_1_to_3_only_no_scoring
  - no_g1_g3_b2_drawdown_growth_or_margin_computation
  - no_pnl_equity_drawdown_or_trip_value_written_printed_or_returned
  - no_read_of_t00_replay_screen_or_mc_output
  - no_read_of_e0_private_txt_contents
  - private_root_outputs_only_never_under_repo
  - vm_inputs_limited_to_section3_list
  - direct_transfer_identical_absolute_paths_only
  - joshua_opened_vm_access_only_no_credential_handling
  - no_pine_on_vm_or_any_copy
  - no_copy_outside_primary_checkout_and_vm
  - interpreter_and_venv_read_only_during_run
  - no_edit_to_frozen_files_anchors_or_tolerances
  - no_code_or_test_edit_in_repo
  - no_rail_arm_deploy_or_account_traffic
  - no_private_evidence_or_state_write
  - no_commit_push_pr_or_merge
  - no_glm_or_external_service
  - single_session
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_personal_replay_live_parity.py
  - tests/ops/test_book_adapters_parity.py
  - tests/ops/test_book_quantity_laws.py
  - tests/ops/test_book_bundle_execution.py
```

The acceptance files run green at the run head before any real-input step (§3 step H5). They are public and synthetic, or they skip without private inputs. A green run is not FG evidence (§5).

## 0. Phase 0: premise, prerequisites and Rule-0 reads (all must hold before dispatch)

- **(a) Predecessors merged on `main`. Report each merge SHA.**
  - Cards A and B, each RESOLVED.
  - Card D Part 1 (`tests/ops/test_personal_replay_live_parity.py`), RESOLVED.
  - P-L1 (#794, `a8769f8`).
  - P-L2 (#805; **open** at `158bf2a`).
  - P-L3 (#797, `911a369`).
  - If any is missing, **stop**.
- **(b) Frozen tuple re-verified by hash.** In the primary checkout, `sha256sum C:/Users/joshu/t00-step3-console/personal-prescreen-20261011/R1_TUPLE.json` equals `62d7ae196059b7d98fd814c7b07a911558e8e5891dd2a669170393583b6c671f` (§10 hook 1). The executor reads the key structure only. It reads the tuple's `size_vector_sha256` field into memory for the seam check (§4 item 3) and prints no value.
- **(c) Chronology.** §10 hook 4 prints nothing at the run head. The run head descends from F, and the pre-registration, `schedule/` and `build_historical_schedule.py` are unchanged from F.
- **(d) Joshua's per-run VM access is opened.** Joshua says in chat that the VM is up and access is open for this run. The executor never asks for, reads or stores a credential.
- **(e) Rule-0 reads at the run head. Report anchors and do not quote values.**
  - `ops/c1_signal_daemon/book_parity.py`: `bar_data_dir` `:46`, `export_dir` `:51`, `load_effective_inputs` `:265`, `parity_for` `:318`.
  - `ops/c1_signal_daemon/book_adapters.py`: `port_root` `:98`, `load_port` `:115` (it refuses non-pinned bytes).
  - `EFFECTIVE_INPUTS_SHA256` `:66` versus `RUNTIME_EFFECTIVE_INPUTS_SHA256` `:72`. Report which one the R1 route checks.
  - The three refusal layers (card D §0(b), re-anchored at the run head).
  - The P-L1/P-L2/P-L3 seam that carries a sizing FILE source (live-wiring packet §3, J-3).
- **(f) Port root.** All four accepted runtime ports must resolve under one `FP_PORT_ROOT`, each at its `core/strategies/BOOK_SOURCES.sha256` pin, with `effective_inputs.json` beside them. Striker's pin is the corrected port `efd479b6…11f4` in the corrected-ports folder; the other three pins are in `ops/c1_signal_daemon/ports/`. Report how one root serves all four (the folder's composition was not read in drafting). If it cannot, return `NEEDS_CONTEXT`. Never assemble a new folder of copies.
- **(g) Anchor artifacts located by hash.** Striker Step 3 contract `acfa7920…6e6d`, acceptance `ebcb2efb…4f1e`, and the Step 6 replay record ([packet-1 Step 3 acceptance](../../notes/2026-09-15-packet1-step3-acceptance.md)). V-0 and A-0 rows are in the [scaling-faithfulness read](../../notes/2026-09-12-track-b-scaling-faithfulness-read.md) (`:100`, `:101`). Report the private path and hash of each. Do not read their bodies beyond what the re-show executes.
- **(h) Card D's D-3** (whether D7 must be green) is ruled.

## 0.5. Routing and clarifying questions

- **(A) Why Claude, why private.** The run reads accepted ports, `effective_inputs.json`, vendor exports and the R1 tuple. That routes it to a Claude private executor under AGENTS.md "Private read surface" and §60, never to Codex or GLM.
- **(B) The driver.** FG items 2–3 need a real-input driver. Part 1 is a synthetic test, and this card writes no repo code. The driver is a private script, prepared and reviewed **before dispatch**, and its sha256 is bound in the dispatch record. H4 copies it into the private root and verifies those exact bytes; nothing is written or edited on the VM (decision D-2, §13). It imports the run head's production modules unchanged and the Part 1 differential's logic by reference. It reimplements no law.
- **(C) The vector on the live path.** The R1 vector reaches the P-L1/P-L2/P-L3 seam as a sizing FILE source (J-3). The FILE is exactly `canonical_json_bytes(tuple["sizing"])`, with no reformatting. Its sha256 must equal the tuple's frozen `size_vector_sha256`, and `validate_size_vector` must accept it. Three identities stay distinct: the tuple file hash (`62d7ae19…671f`), the canonical size-vector hash, and the owner's binding identity (decision D-3, §13).

## 1. Goal

Produce private, hash-bound evidence of FG items 1–3 at R1 (pre-registration §7), with one public pass/fail per item, before any Q-SFCLEAR-2 scoring run.

**Not asked, and not part of this card:** any G1, G3, G1-D, G3-D, B2, drawdown, growth, margin or residual computation; the scoring run; the run record under `run_records/`; the closure; FG-T and RS (item 4 RULED: PR).

## 2. Scope: FG items at R1, with PASS/FAIL rules fixed ex ante

**Legs:** `aegis_6j`, `dj30_mym_p250` (Striker) and `vanguard_mgc` are ON. `orb_mnq_v7` is OFF: its signals are generated and refused. The route is PR for every leg: the four-leg `BookReplay` with the R1 vector under P0, the bound schedule (`ab44fada…d473`) and the bound roll-date list (`72677d25…134c`). The window is 2022-09-01..2026-09-02.

| Item | What is shown | PASS (all must hold) | FAIL |
|---|---|---|---|
| **1a. F11 revalidation** (T10 reconciliation R1 hold item (ii), [`:182`](../../notes/2026-09-21-t10-phase1-source-reconciliation.md)) | Each ON leg's anchor reproduced on the run head's (moved) emulator, at captured settings. Aegis: A-0 (121/121). Vanguard: V-0 (338/338). Striker: the corrected port `efd479b6…` replayed under the Step 3 contract `acfa7920…`/`ebcb2efb…` domain, plus the Step 6 replay | Matched count equals the anchor's count, with zero divergences and zero exclusions beyond the anchor's own. The port, panel and export triple matches every pin | Any count short, any divergence, or any pin mismatch |
| **1b. Route identity at R1** | The PR route at R1 loads the schedule and the roll-date list by their frozen sha256 | Both hashes equal the §3-bound values. A byte-perturbed copy of each, inside the private root, is refused before execution | Either loads without a hash check, or a perturbed copy runs |
| **1c. Re-show at R1** (meaning: decision D-1) | Each ON leg's anchor property carried to R1 quantity | As D-1 fixes it before freeze. Proposed: Aegis's entry and exit bars and prices equal its captured-size run at R1's fixed quantity (A-0's timing-invariance basis). Vanguard's and Striker's PR runs complete at R1 on the 1a-identical pins, with item 2 holding | Per D-1 |
| **2. Quantity law** | On the full R1 PR replay, each adapter-emitted entry's quantity against the rail's sizing law (`LegSize`, `AddsRule.OFF`) on the same signal | 100% equality per ON leg, with ≥ 1 entry per ON leg. Zero adds on Striker and Vanguard. Aegis is fixed at the R1 base. Every Vanguard zero-port entry and every ORB entry is refused | Any inequality, any add sent, or a zero-quantity order |
| **3. D8 seam** | The same real signal stream through the live path (P-L1 sizing context, P-L2 owner binding with the frozen vector FILE, P-L3 bundle execution), run in-process with no account, against the replay | Per signal: equal admitted quantity. Adds OFF on both paths. Each refused zero-quantity entry is refused on both, with its own reason at its own consumer (`shared_sizing_zero` adapter, `zero policy quantity` replay, `zero_size` owner), and with no dispatch, reservation or fill. The live binding's vector hash equals the tuple's `size_vector_sha256` | Any divergence, a missing or renamed reason, a zero order or reservation, or a hash mismatch |

**Tolerances:** exact equality everywhere: integer quantities, bar timestamps and reason strings. No tolerance can be introduced or widened after any output exists (§5).

**FG verdict:** PASS only if 1a, 1b, 1c, 2 and 3 all PASS. Anything else is FG not PASS, so the study run must not start (pre-registration §6 VOID).

## 3. Host procedure (the VM, under §60 addendum 2026-10-12)

**Host:** the Joshua-controlled Windows VM admitted on 2026-10-07 and extended on 2026-10-12. No hostname, address or credential appears in this card or its return. The 2026-10-07 T00 route A (a path-identical mirror; [T00 card §8](2026-10-03-t00-screen-authority-build-card-DRAFT.md)) was withdrawn before use, so this run is the first use of the admission (risk, §Pre-mortem).

**H1. Direct transfer, identical absolute paths.** Copy from the primary checkout `C:\Users\joshu\multi_firm_operations` (and `C:\Users\joshu\t00-step3-console`) straight to the VM, with no intermediate copy. Only these items are copied:

| Input | Path (identical on the VM) | Pin |
|---|---|---|
| Repo clone at the run head | `C:\Users\joshu\multi_firm_operations` (clean, `core.autocrlf=false`) | `git rev-parse HEAD` = run head |
| Four accepted runtime ports | the paths in `core/strategies/BOOK_SOURCES.sha256` (ports section) | that manifest's four port rows |
| `effective_inputs.json` | `ops/c1_signal_daemon/ports/effective_inputs.json` (or the §0(f) root) | the constant §0(e) names |
| Bar panels 6J, MYM, MGC, MNQ | `core/data/bar_data/{6J,MYM,MGC,MNQ}_M15.csv` | `core/data/bar_data/SHA256SUMS` |
| Captured exports the anchors bind | `local_artifacts\recovery-2026-09-24\surviving-inputs\` (the named files only) | `phase1_config.json` sha256 (checked by `book_parity.load_export`) |
| Frozen tuple | `C:\Users\joshu\t00-step3-console\personal-prescreen-20261011\R1_TUPLE.json` | `62d7ae19…671f` |
| Anchor artifacts (§0(g)) | their private paths | `acfa7920…`, `ebcb2efb…`, the Step 6 record hash |
| Interpreter and operations venv | `C:\Program Files\Python313` and the launcher's venv path | the launcher's `doctor` identity |
| `E_0` file (machine-consumed only, §13 D-7) | `C:\Users\joshu\t00-step3-console\personal-prescreen-20261011\e0_private.txt` | the tuple's reference and the freeze record's `input_sha256` digest, both via the run manifest |
| Digest-only run manifest (§13 D-7) | built by the coordinator in the private root before dispatch | its sha256 in the dispatch record |

**Never copied:** Pine (`core/strategies/book/*.pine`); the freeze, rulings, fold or fact-finding folders (but see §13 input scope for the `E_0` file and the digest-only run manifest); any T00, screen, replay or MC output; any other private file.

**H2. Verify.** On the VM, before any run, compare every copied file by sha256 against its pin. Run `sha256sum -c core/strategies/BOOK_SOURCES.sha256` on the four port rows only (Pine is absent by design), and check the panel `SHA256SUMS`.

**H3. Read-only interpreter and venv.** Set `C:\Program Files\Python313` and the venv read-only for the run's duration (attended-host threat model, T00 card §8). `fp doctor` passes. Use `sys.executable` for any child process.

**H4. Private root.** Create `C:\Users\joshu\t00-step3-console\sfclear2-fg-<UTC>\`, outside the repo, on the VM. Write `nonce.txt` first (≥ 128 random bits, §6 nonce rule). Copy in the reviewed driver (§0.5 B) and verify its sha256 equals the dispatch-record value; derive the sizing FILE (§0.5 C) and verify it; hash both into `SHA256SUMS` before any real-input step.

**H5. Run, attended.** Run the acceptance list green at the run head. Then set `FP_PORT_ROOT`, `FP_BAR_DATA_DIR` and `FP_TV_EXPORT_DIR` to the §H1 paths and run items 1a → 1b → 1c → 2 → 3, each under the §7 timeout. Outputs are per-item pass/fail plus counts, refusal reasons and divergence locations (bar time, leg, field). No P&L, equity, drawdown, MAE/MFE or trip column is written, printed or returned.

**H6. Seal and return.** Write `SHA256SUMS` over every output and `nonce.txt`, then hash it. Transfer the private root directly back to the identical path on the primary host and re-verify it with `sha256sum -c`.

**H7. Teardown.** List every path copied in H1 and H4 for removal from the VM. Joshua removes them and deallocates the VM, or directs the executor in chat to remove the copies. The executor then confirms they are absent with a listing. Restore the interpreter and venv permissions. Copies never leave the VM or the primary checkout.

## 4. Hypothesis and evidence

**Hypothesis (H-FG):** if the R1 PR route and the live P-L1/P-L2/P-L3 seam are faithful to the frozen design, then items 1a–3 all PASS under §2's ex-ante rules. **Reject (FG FAIL) if** any item FAILs. **Revert trigger:** none, since the executor changes no repo state; a FAIL is returned, not reverted.

- **Private:** only `C:\Users\joshu\t00-step3-console\sfclear2-fg-<UTC>\`, with `nonce.txt` and `SHA256SUMS` listing it. Nothing goes under the repo (pre-registration §7).
- **Public, written by the coordinator (not the executor):**
  - the FG verdict, with pass/fail for each of 1a, 1b, 1c, 2 and 3;
  - the `SHA256SUMS` sha256;
  - one `docs/evidence/PRIVATE_EVIDENCE.sha256` row, `<sha256>  t00-step3-console/sfclear2-fg-<UTC>/SHA256SUMS`.
- **E_0:** nothing public pins `E_0` (pre-registration §5, last item). The return carries no per-leg quantity, count that pins a quantity, or money value.
- **e0 leak scan:** before returning, the executor writes its return text to a file inside the private root. In the primary checkout, it verifies the fold-4 folder (`d4e358f8…a45c`, §10 hook 1) and runs `bash C:/Users/joshu/t00-step3-console/sfclear2-fold4-20261012T001816Z/e0_leak_scan.sh <that file>` (hook 6). The expected result is `CLEAN`. The coordinator re-runs it on the public commit text before pushing.

## 5. Forbidden moves

- Editing any frozen file: the pre-registration, cards A–E, P-L1–P-L3, the schedule, the roll-date list, generators, the calculator, `R1_TUPLE.json`, ports, `effective_inputs.json` or `STATE.md`.
- Changing an anchor, a count, a tolerance, the driver or the derived sizing FILE after any item output exists.
- Retrying a FAIL by changing anything frozen. A FAIL is returned, not repaired.
- Reading T00, screen, trial-9 replay or MC outputs, or `e0_private.txt` contents.
- Running the clearance scoring, or computing G1, G3, G1-D, G3-D, B2, drawdown, growth, margin, residuals, Striker trip dates or any P&L summary. FG outputs never feed the scoring run.
- Reporting Part 1's synthetic PASS, or a private-input skip, as FG at R1.
- Pine on the VM, any copy outside the primary checkout and the VM, or any handling of a credential.
- Arming, deploying, contacting a listener or broker, or sending any account traffic.
- Committing, pushing, opening a PR, or writing `PRIVATE_EVIDENCE.sha256`. GLM or any other external service.

## 6. Return (status taxonomy)

| Status | When |
|---|---|
| `DONE — FG PASS` | §0 holds; H2 verified; every §2 item PASS; `SHA256SUMS` re-verified on the primary host; leak scan CLEAN; teardown confirmed |
| `DONE — FG FAIL` | The run completed and at least one item FAILs. The study run must not start (§6 VOID). The return names the failing item(s) and a structural divergence class only |
| `DONE_WITH_CONCERNS` | FG PASS with an observation (for example, D7 still `PENDING-P4` if D-3 allows it) |
| `NEEDS_CONTEXT` | §0(e)–(g) cannot be stated (for example, no single port root, or an anchor artifact cannot be found by hash) |
| `BLOCKED — context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong` | As named. `capability-problem` covers VM access not opened, a credential prompt, or a power, disk or timeout stop (§7). `plan-itself-wrong` covers an item that needs a code or frozen-file change |

The return carries: the run head; predecessor merge SHAs; the `SHA256SUMS` sha256; pass/fail per item; the driver and sizing-FILE hashes; an exposure attestation (what the executor saw, as classes, not values); and the leak-scan result. It carries no G1/G3 or scoring value, because none is computed.

**Gate verdict (coordinator, at review):** **RESOLVED** (FG PASS) when `DONE — FG PASS` and the coordinator re-verifies `SHA256SUMS` and the leak scan. **FALSIFIED** (FG FAIL) on `DONE — FG FAIL`: recorded, and the study does not run. **AMBIGUOUS** on any other status: no FG standing, so the study does not run.

## 7. Stop conditions

Stop and return at once, writing nothing further:
- any input hash mismatch (H2, §0(b), §0(f), §0(g));
- any FG item FAIL. Finish sealing the outputs, then return `DONE — FG FAIL`. No retry by any change;
- VM access not opened, or any credential, login or MFA prompt;
- **power and disk:** the VM is stopped, preempted or deallocated mid-run; free disk below twice the copied-input size before H4; or a write error;
- **timeout:** any single item exceeds its per-item wall-clock limit (decision D-4, §13). An interrupted root is sealed as `INCOMPLETE` (the only writes allowed after interruption are the `INCOMPLETE` marker and `SHA256SUMS`; no further output), kept, never reused, and carries no PASS standing. A rerun uses a new `<UTC>` root on the same frozen inputs, only on a coordinator dispatch, and the interrupted root is disclosed;
- the VM is unavailable. Falling back to the laptop needs a new coordinator ruling, because item 6 ruled (b) and the laptop has hit timeouts.

## 8. Out of scope and decision unlocked

**Out of scope:** the scoring run, its run record and the closure (card E §13); P4 and D7 unless D-3 requires it; the Tradeify lane.

**Unlocks:** on FG PASS, the pre-registration §6 FG condition holds, and the coordinator may dispatch the scoring run under card E §13. On FAIL, nothing is unlocked.

## 9. Sequencing and collisions

- Runs after A0 → A → C → B → D (Part 1), with P-L1, P-L2 and P-L3 merged, and before E's scoring run.
- It writes no repo file, so it holds no slot in the `book_account_owner.py` or `production_source.py` writer queues.
- One executor session at a time on the VM. No concurrent T00 or other use of the admission.

## 10. Audit hooks (runnable)

```bash
python -I scripts/check_brief.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-fg-private-executor-card-DRAFT.md --type cc_handoff
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-12-q-sfclear-2-fg-private-executor-card-DRAFT.md
# Pre-dispatch (primary checkout): tuple, chronology, predecessors
sha256sum C:/Users/joshu/t00-step3-console/personal-prescreen-20261011/R1_TUPLE.json   # expect 62d7ae19…671f
git log --oneline origin/main | grep -E "#794|#797|#805"   # expect all three merged
# At return (primary checkout)
( cd "C:/Users/joshu/t00-step3-console/sfclear2-fg-<UTC>" && sha256sum SHA256SUMS && sha256sum -c SHA256SUMS )
bash C:/Users/joshu/t00-step3-console/sfclear2-fold4-20261012T001816Z/e0_leak_scan.sh <return-text-file>   # expect CLEAN
git status --porcelain   # expect empty: no repo write by the executor
```

## 11. Gates (NOT DISPATCHABLE until all hold)

- **G-1. Prerequisites:** §0(a)–(d) and (h) hold, and the §12 decisions are recorded.
- **G-2. Coordinator freeze** of this card under the committed-handoff rule. **Not done.**
- **G-3. Dispatch record** naming the run head, the driver sha256 and the executor session. **Not done.**

## 12. Open decisions (coordinator at freeze; Joshua where marked)

- **D-1.** What "anchor re-shown at R1" means per leg (item 1c). The pre-registration names no Aegis anchor under PR (A-0 is the RS anchor), and Striker's size-dependent halts rule out timing identity at R1. The proposal is in §2.
- **D-2.** Driver custody: a private driver hashed before the run (proposed), or a public, real-input mode added to Part 1 (a new build card).
- **D-3.** How the frozen vector enters the live path: a sizing FILE derived from `R1_TUPLE.json` in the private root (proposed). This also confirms live-wiring §4 condition 2 (the tuple's hash formula equals `sha256(canonical_json_bytes(sizing))`).
- **D-4.** Per-item timeout values, and whether an `INCOMPLETE` rerun needs Joshua or only the coordinator.
- **D-5 (Joshua).** Whether "the frozen study's run inputs" in §60 2026-10-12 covers `R1_TUPLE.json`, the Step 3/Step 6 anchor artifacts and the interpreter/venv mirror on the VM.
  - **RULED 2026-10-12 (Joshua, to the Deployment Coordinator, verbatim "D-5 and D-6 as recommended"):** yes; the §60 2026-10-12 run inputs cover `R1_TUPLE.json`, the Step 3/Step 6 anchor artifacts and the interpreter/venv mirror. Pine stays off the VM.
- **D-6 (Joshua).** Teardown: who removes the VM copies, and whether deallocation is enough or disk deletion is required.
  - **RULED 2026-10-12 (same words):** Joshua removes the H1/H4 copies, the executor confirms their absence with a listing, then Joshua deallocates the VM. Disk deletion is not required once absence is confirmed.
- **D-7.** Exposure: the R1 PR replay inside items 2–3 runs the same path the scoring run will. Confirm that §5's output restriction (no P&L, equity or trip data) is sufficient, or require a separate executor for scoring.

## 13. Coordinator resolutions before freeze (2026-10-12)

Prepared on Joshua's 2026-10-12 instruction to resolve #808's contradictions using the fidelity review (main `6cf684a`, #808 `ae689ff`). They govern §§0.5, 2, 3, 7 and 12 where they differ. D-5 and D-6 stay as ruled. Items marked **(Joshua)** need his words before freeze. Card D's open D-3 (whether D7 must be green) is read from card D's own verdict rule (`:137`: RESOLVED allows `DONE_WITH_CONCERNS` only for D7 `PENDING-P4`), so D7 need not be green before this run; P0 live parity stays P4's acceptance.

**D-1. What item 1 demonstrates, per leg.** Item 1 has two separate parts, and passing one does not imply the other.
- **1(i) Captured-setting F11 revalidation.** On the moved emulator, at the captured sizing, each anchor reproduces exactly as recorded: Vanguard V-0 338/338; Striker Step 3 contract `acfa7920…`/`ebcb2efb…` and the Step 6 replay record; Aegis's captured-size PR run against its retained reference. Reference: the recorded anchor. Permitted difference: none.
- **1(ii) Transfer to R1 sizing.** Reference: the 1(i) run of the same leg on the same pins.
  - *Aegis* (fixed quantity): in the isolated-leg run, every trade's entry/exit bar and price equal the reference, with only quantity scaled. This does not imply unchanged whole-book timing, so 1(ii) also runs the four-leg PR under the bound schedule and P0. Every whole-book difference from the isolated run must carry a named control record (G0 denial, G4 window, P0 refusal or latch, cap). Any unexplained difference fails.
  - *Vanguard* and *Striker* (size-dependent state: port paper equity, port map, `ddHit` and soft-stop): all trades up to the first divergence equal the reference, apart from quantity, which item 2 checks against the law. The first divergence must be attributable to a recorded size-dependent state change (paper-equity path, or a trip with its date). After it, differences are permitted only through that state. The divergence point and its cause are recorded privately, with pass/fail public. "The replay completes and quantities match" alone is not a 1(ii) PASS.
- None of this weakens the frozen §7 item 1: each anchor is re-shown at R1, with F11.

**D-2. Driver custody.** The coordinator prepares the private driver before dispatch. A Claude reviewer reads it in place: it imports the run head's production modules unchanged, uses production feedback (fills and refusals reach the adapters exactly as in replay), reimplements no strategy or sizing law, and follows the output allowlist below. Its sha256 is then bound in the dispatch record. H4 copies and verifies; it never writes the driver.

**D-3. Vector identities and the FG seam.** The FILE is exactly `canonical_json_bytes(tuple["sizing"])`, verified against the frozen `size_vector_sha256` and accepted by `validate_size_vector`. The typed consumers exist (P-L1, P-L2 and P-L3 are merged). The production FILE loader (R-SV) does not exist yet and stays with its owner. **RULED (Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "yes to both"):** the reviewed in-process seam satisfies FG item 3; the R-SV production loader stays a separate gate before any live activation. *As put:* Decide whether the reviewed in-process seam satisfies FG item 3. In that seam, the driver reads the FILE bytes, validates them into a `SizeVector`, and builds the owner binding through P-L2's typed path. Recommended: yes for FG, with the R-SV production loader kept as a separate gate before any live activation. Otherwise FG waits for the R-SV loader build.

**D-4. Timeouts.** No VM runtime is assumed. Each item's limit is 4× a measurement, recorded in the dispatch record:
- items 1(i) and 1(ii): the laptop's recorded parity run at the run head (the coordinator's #797 run: 29 tests in 43 s), re-measured at the run head before dispatch;
- items 2 and 3: Part 1's own synthetic full-calendar replay duration at its merged head.

An interrupted root is sealed `INCOMPLETE`: only its marker and `SHA256SUMS` are written after interruption, it has no PASS standing, and it is kept. A rerun needs a coordinator dispatch, a new root and unchanged frozen inputs. A rerun that would change any input needs Joshua.

**D-7. Exposure and input scope.** Under frozen card B, the replay must verify a starting-equity file and its digest from the freeze record. This card excluded both, which is the contradiction.
- **Smallest amendment.** Add two machine-consumed inputs to H1, both never opened or printed by any person or agent process outside the replay's verified envelope:
  - (a) the `E_0` file (`e0_private.txt`), checked against the tuple's reference and the freeze record's `input_sha256` digest;
  - (b) a **digest-only run manifest** built by the coordinator from F and the freeze record. It holds only the expected digests that card B's envelope consumes. It holds no G1/G3, drift or other values, so the freeze record itself is not copied.
- **No bypass.** No substitute equity, no skipped verification, and no edit to frozen card B.
- **RULED (Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "yes to both"):** `e0_private.txt` may be transferred to the VM for this FG run only, consumed by the replay's verified envelope and never opened or printed by any person or agent process; it is listed in H1 and removed at H7 teardown under D-6. Recorded at the §60 owner as well. *As put:* D-5 covered the tuple, anchors and interpreter, not the `E_0` file.
- **Output allowlist** (unchanged scope: no separate scoring executor is required). The replay keeps its normal internal equity and P&L arithmetic; nothing derived from it leaves the process except:
  - per item, PASS/FAIL;
  - per trade, leg, timestamps, quantity and reason codes;
  - divergence points and causes (private);
  - hashes.

  Denied in output: P&L, equity, drawdown, trip dates, `E_0` and any cell value.
  - Exceptions are logged as class and code location only, with no message text or locals.
  - Pytest runs use `--tb=line -p no:cacheprovider`, with no captured-variable dumps.
  - No route-output file is kept beyond the allowlisted fields.
  - The leak scan runs on everything returned.

## Pre-mortem

- **Loop cost.** One VM session: transfer, five items, seal and teardown.
- **Likely failure.**
  - No single `FP_PORT_ROOT` serves the corrected Striker port and the other three (§0(f)).
  - The VM was never provisioned, because route A was withdrawn on quota. *Cleared 2026-10-12: Joshua confirms the VM exists.*
- **What would make this moot:** none. FG PASS is a precondition of the study run.
- **Evidence binding:** the private `SHA256SUMS` at the returned UTC root, the run head and the driver hash only.

[prereg]: https://github.com/Joshua-Asante/first-passage/blob/83867f0d362931c2a516a62b990bb1c209372527/docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
[s60]: ../programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25
