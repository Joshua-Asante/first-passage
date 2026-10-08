# CC handoff — T00 step-12 diagnostic, Tier 1: reproduce and explain (session level)

**Date:** 2026-10-08.
**Status:** Tier 1 ADMITTED. Execution starts only after this card and the driver PR (#728) are both merged, each on Joshua's "merge".
**Authority:**
- **Admission:** Joshua, 2026-10-08, about 03:30Z, directly to the step-12 owner session: "I'll admit tier 1".
- **Driver:** "Admit a reviewed driver", Joshua, 2026-10-08, directly to coordinator (4), on the P1 of #727's review `6051698989`.

These are the authority for this one use of the r3c receipt; §0.6 gives the reasoning.
**Brief type:** CC handoff, executor packet (diagnostic, non-decision-bearing).
**Seats:**
- **Executor:** the step-12 owner session, named by Joshua to coordinator (4) on 2026-10-08.
- **Acceptor of the Tier-1 report:** coordinator (4), as T00 card owner.
- The deployment coordinator keeps combined acceptance. Joshua keeps every investment decision.

**Subject:** the step-12 result recorded in #724: `NO-GO-evidence-robust`, `VERIFIED`; results `a5b985d0…42dc`, attestation `f627e805…1ed5`, REPORT `bebceb93…9984`; H `5d25f9cfc1e8ff00bacda45478322f9858176e8b`.
**Return boundary:** a private report, plus a public return of hashes and labels only, or BLOCKED / NEEDS_CONTEXT exactly where §6 says.

## §0 — Production reads

Read at H `5d25f9c` on 2026-10-08. Re-read at dispatch.

| Surface (H `5d25f9c`) | Use |
|---|---|
| `production_source.py:926-936` `_seal`; `:1232-1254` `replay_bracket` (H `5d25f9c`) | For a source-only contract (r3c), `replay_bracket` returns `SourceOnlyBracket`. Per session it carries `pnl`, `intraday_low`, `fills`, `flat_before_deadline`, `start_flat` and `end_flat`; per run it carries `events_sha256`, the consumed-split placements and `deadline_failure`. **It never returns the event stream.** |
| `production_source.py:1183-1199`, `:1210-1214` (H `5d25f9c`) | Every `replay_bracket` call re-runs the full integrity check (about 71 s, design §6.2), including `require_validated_source_contract(now=_now())`, so the approval window is code-enforced per call. |
| `p7_driver.py:39-48` (H `5d25f9c`) | The source construction the driver copies: `validate_source_contract` → `ProductionSource.build(receipt, artifact_root=…)` → `replay_bracket(path)`. Only the construction is copied; P7's bootstrap is not used (§0.5). |
| `t00_screen/worker.py:162-182`, `:340-360`; `plan.py:42` `seed`, `:120` `rebuild_candidates` (H `5d25f9c`) | The retained identities and the path re-assembly the driver repeats. `worker` imported under any name other than `__main__` installs nothing and runs nothing (its docstring), so the driver reuses `worker.path_sha256` directly. |
| `replay.py:164-631`; `book_policy.py:65-114` (H `5d25f9c`) | The raw event kinds and the replay's protection policy (`candidate_book_protection_policy()`: trailing, trigger `0.01`, scale `0.40`). Both are **Tier 2 only** (§2). |

## §0.5 — The driver and the prerequisites (each must hold before the first replay; otherwise BLOCKED)

1. **Driver.** The driver is `scripts/t00_tier1_diagnostic.py` from #728. It is reviewed in its own code PR and pinned at **SHA-256 `94c8eeab7b51360401f792e097cd013d89e6edd56ec57e05a7cb141e911a7508`** (#728 head `f6ef6c6`). The executor re-hashes it before each mode, and a mismatch is BLOCKED. A fold of #728 that changes the file re-pins it here before execution.
   - It runs under the operations venv with no bootstrap.
   - Every module it uses is imported from `--code-root`, the clean detached H checkout; the driver refuses any other HEAD or a dirty tree.
   - The imported modules are `contract`, `paths`, `production_source`, `p7_evidence`, and `t00_screen.journal`, `plan`, `verdict` and `worker`.
   - Nothing under `ops/` or `core/` changes, so H is unaffected.
   - #728 passes the A10b scan, which lists the driver and allowlists its one `replay_bracket` owner.
2. **Self-tests before any replay.**
   - **(a) Fixture test, with no real source** (#728 `test_sealed_identity_equals_worker_projection`). On the same synthetic run, the identities the driver computes from `_seal`'s output equal `worker.run_projection`'s, with and without a deadline failure.
   - **(b) `selftest` mode, with no replay.** It builds the source, rebuilds every selected path, and checks each path's seed and `path_sha256` against its retained PATH record.
3. **Window.** Every replay must finish before **2026-10-14T02:08Z**, when the r3c source approval `2cc7195e…` expires. No renewal is requested here.
4. **Environment.** The worktree must be clean before and after, and the interpreter and venv unchanged during the run. The inputs (r3c contract, source approval, registry, authority) are checked against their pins by the driver.
5. **Host.** No overlap with a heavy run booked by the deployment coordinator (#651). The diagnostic is one process of about 0.6 GiB.
6. **Entry points.** Only `ProductionSource.build` and `replay_bracket`. **Forbidden:** `screen_bracket`, `screen_epoch`, `_engine`, `_replay_raw` and `replay`; any access to unsealed results; any code edit. If the report needs more than the sealed output gives, return NEEDS_CONTEXT naming Tier 2.

## §0.6 — Why this use fits the r3c receipt

The r3c receipt's purpose is `T00_P7_SOURCE_VERIFICATION`. Its refusals include `SCREEN`, `MONTE_CARLO` and `DECISION_RULES` (`contract.py:963-968`).

- **Reproduction is source verification in kind.** Tier 1 replays already-scored paths and checks that they reproduce their retained identities, exactly as P7 checks its own path.
- **Not SCREEN:** no screen authority, verdict, label or tally is computed, and no new path is sampled.
- **Not MONTE_CARLO:** no draw is made. The 18 paths are fixed, previously drawn keys, and no rate or distribution is estimated (§1).
- **Not DECISION_RULES:** no rule or threshold is evaluated. Floor crossings are descriptive, the kernel status stays the retained one, and the §6 recommendation is advice to Joshua, not a gate.

Joshua's admission is the authority for this third use of approval `2cc7195e…`, beyond steps 7–12 and `verify`.

## §1 — Purpose, non-goals and no back door

**Purpose:** determine, from at most 18 already-scored paths, whether the step-12 failures show a credible portfolio-construction mechanism worth a controlled test. The output is an attribution report. It is not a bust-rate estimate, a replacement book or qualification evidence; selected cases cannot estimate population rates or prove that changing a mechanism helps.

**No back door.** No Tier-1 output changes, re-tests or re-opens the step-3 verdict (`NO-GO-evidence-robust`, `VERIFIED`, #724) or #581 (#581 A6; design §4.5). A non-reproduction (§6) is an **integrity incident**, reported to Joshua. It is never a verdict change, a re-run trigger or grounds for re-opening #581.

## §2 — Evidence: Tier 1 versus Tier 2

| Draft evidence item | Tier 1 (sealed) | Needs Tier 2 (raw events) |
|---|---|---|
| Equity against the drawdown floor, per session | Yes: cumulative `pnl` and `intraday_low`. Floor crossings are **descriptive**; the kernel status stays the retained one, because `evaluate_replay` refuses sealed input | — |
| Bust timing, and shock versus grind | Yes: the first session the descriptive floor is crossed; the `intraday_low` gap at that session | — |
| Recovery on passing paths | Yes: depth and duration of drawdowns before the pass day | — |
| Activity | Yes: `fills` per session | — |
| Each strategy's contribution | — | Yes |
| Protection state and its changes (`session_mode`) | — | Yes |
| Requested and filled base and add quantities | — | Yes |
| Capacity refusals, takeovers, forced closes, costs | — | Yes |

Tier 2 needs a reviewed capability that returns raw events for a diagnostic evidence class. That is a code change, so it means a new H, review, a P7 re-run at that H and new signatures. Scope it only if Tier 1 shows a mechanism worth attributing.

## §3 — Sample

- **Record of truth:** the step-12 **segment journals** (`journal/s*.jsonl`), chain-verified by `journal.read`.
  - `freeze` checks them against `results.json` (`a5b985d0…`): the plan digest must match, and the verdict re-derived through `verdict.evaluate` must equal the finalized one.
  - They are bound to the pinned `attestation.json` (`f627e805…`). Each segment journal's head must equal its attested head. The ledger must be the attested chain up to its REPORTED head, then the FINAL naming this attestation, then only `verify`'s records. A difference is BLOCKED.
  - The `verify` journals (`v*`), which duplicate 9 keys, are not read.
- **Strata:** population (FULL, H1, H2) × retained class (agreed `FAILURE`, agreed `PASS`, `UNDETERMINED`, from `bracket_status`), in that order. FULL / agreed FAILURE comes first, so it holds the checkpoint. Any other `bracket_status` is not sampled.
- **Rule:** within each stratum, sort the keys by `sha256(canonical_json_bytes(key))` ascending and take the first two. A stratum with fewer than two paths contributes all it has, and nothing is substituted from another stratum. The `UNDETERMINED` stratum's R1/R2 mix is taken as drawn.
- **Freeze.** `freeze` writes `keys.json` once and prints its SHA-256. The executor **publishes that hash on #727 before `selftest`**. The key list and the per-stratum counts stay private.

## §4 — Hypothesis and falsifier

**H (reproduction):** a sealed `replay_bracket` re-execution at H of each selected path reproduces its retained record byte for byte. Per run, that is `digest`, `sessions`, `fills`, `events_sha256`, `deadline_failure`, and the consumed-split count and SHA-256.

**Falsifier:** any one mismatch after the path's seed and `path_sha256` have matched in `selftest`, or any exception raised by replay execution proper. Every retained PATH record came from a bracket that returned normally. A host fault (`MemoryError`, `OSError`) inside a replay is also a NON_REPRODUCTION.
- **REFUSED, not FALSIFIED, by origin:** a `ContractValidationError`, or any exception raised inside `ProductionSource._check_path`, whatever its message. That frame runs `_verify_integrity`, and with it `_resolve_domain` and `_qualification_snapshots` (the `book_adapters` checks), before any engine is built. The driver reads it from the traceback.
- Every run stop's exception type and detail are recorded in `summary.json` and on `stderr`, so a host fault can be told apart from a real non-reproduction.

The run stops at that path, with no replacement and no retry.

The mechanism reading (shock versus grind, recovery depth) is descriptive and conditional on H holding. It is not a gate and does not test a mechanism.

## §5 — Launch, sequence and stops

1. **Hash the driver** against §0.5 item 1. The file that is hashed and run is exactly `C:\Users\joshu\multi_firm_operations\.claude\worktrees\t00-tier1-driver-merged\scripts\t00_tier1_diagnostic.py`, in a new detached worktree at #728's merge commit, clean with `--untracked-files=all`. It is re-hashed immediately before each mode, and the public return names that merge commit.
2. **`freeze`**, then publish the key-list hash on #727.
   - **Pre-merge smoke run.** One read-only `freeze` ran on 2026-10-08 at 03:50Z, before #728 was opened, by the executor session, to its session scratchpad. It built no source and replayed nothing. Its `keys.json` SHA-256 was `60c128a7e5ba9f030b90312b2c7792e1a55fd4c9077b42566fcb99d2971d329e`, and that `keys.json` stays private.
   - This smoke run is exempt from item 5's "never re-run a mode". The official `freeze`'s `keys.json` must have this same SHA-256. A different hash is `DRIVER_DEFECT`: stop, and run no `selftest`.
3. **`selftest`** (no replay). A seed or `path_sha256` mismatch is `DRIVER_DEFECT`, and nothing is replayed.
4. **`run`, detached:**
   - Launch with PowerShell `Start-Process -PassThru` from the H checkout, with stdout and stderr to files under the private output directory (§6).
   - Watch the PID, and kill it with `Stop-Process` at **3 h 10 min wall** from launch. This is a backstop behind the driver's own 3 h wall stop, timed so the two do not race.
   - The driver's watchdog hard-stops only while a replay is in progress, using a guard flag under a lock. Outside a replay, the main thread's own checks stop the run. So a detected mismatch is never reported as BUDGET, and no record is cut mid-write.
   - Every output is written create-once and atomically (a synced temporary file, then `os.replace`).
   - The driver itself refuses to start path N+1 if that would cross **2 CPU-hours** or 3 h of wall time, measured from its own start plus the last path's cost (`BUDGET`).
   - It stops after the checkpoint path if that path costs more than **225 CPU-seconds** (1.5 × the 150 s estimate).
5. **Never** replace a path, change a comparison criterion, re-run a mode (item 2's smoke run aside), or retry after a stop. A stop returns partial evidence.

## §6 — Return and verdict

**Verdict on H:**
- **RESOLVED:** every selected path replayed and matched, and the report is delivered.
- **FALSIFIED:** a `NON_REPRODUCTION`: an identity mismatch, or a non-gate replay exception (§4).
- **`EVIDENCE_WRITE_FAILED`** (AMBIGUOUS, exit 3): a run that would be RESOLVED could not write `summary.json`. This is a host or evidence fault, not a driver defect. A run that had already stopped keeps its verdict and code, and the write failure goes to `stderr`. The reservation still blocks any retry, and an AMBIGUOUS result goes to Joshua.
- **AMBIGUOUS:** any other stop (`PREREQUISITE`, `DRIVER_DEFECT`, `REFUSED`, `BUDGET`) before every path is replayed, with no mismatch.

A `DRIVER_DEFECT` is a fault in the driver, not evidence about the run: it goes back to #728 for a fix and re-review. It covers the pre-replay faults (seed or `path_sha256` mismatch, an unclassified setup exception) and any driver fault after a replay has returned, for example a failed write of a path record. Any re-attempt needs a fresh ruling from Joshua; this card grants none.

**Status (exactly one):**
- **DONE:** H RESOLVED and the report delivered.
- **DONE_WITH_CONCERNS:** all of DONE, plus a named concern. A mismatch is never this.
- **NEEDS_CONTEXT:** a missing fact or ruling, including evidence only Tier 2 can supply. Name it.
- **BLOCKED:** a §0.5 prerequisite fails, H is FALSIFIED (an integrity incident to Joshua, §1), a refusal, a driver defect, or the budget stops the run. State the exact obstruction.

**Private output:** `C:\Users\joshu\multi_firm_operations\t00-step3\tier1-diagnostic-2026-10\`. It is in the private root, outside every worktree and outside the step-12 run directory, and it is git-ignored (#719 and the primary checkout's exclude). It holds `keys.json`, the per-path sealed series and identities, the run summary, stdout and stderr, all costs and timings, and the report.

**Public return** (to coordinator (4), and the hash on #727): the key-list SHA-256, the driver SHA-256, the §6 verdict and code, the status, and the report SHA-256. No counts, ordinals, rates, values, timings or keys.

**Report contents:**
1. Reproduction results and evidence identities.
2. Session-level explanations of failures, and contrasting recoveries.
3. Supporting and contradicting session-level evidence for a shock or grind mechanism. Any claim that would need Tier 2 data is marked as such.
4. One recommendation: Tier 2 scoping, a controlled repair comparison, fresh research, or a precisely stated remaining uncertainty.

## §7 — Budget

The step-12 run took about 80 s of wall time per path per worker, with integrity hoisted. `replay_bracket` adds about 71 s of integrity per call, so expect about 150 s per path, plus about 3 min to build the source.

- Estimate: about 50 min in total.
- **Ceiling: 2 CPU-hours and 3 h of wall time; at most 18 paths and 36 bracket runs.**
- Enforced as in §5 item 4.

## §8 — Exposure

The diagnostic reads per-session detail for scored step-12 paths, beyond the verdict. The reader log opens with the §5 item 2 smoke run's operator: the executor session, 2026-10-08. It saw the selected keys and the per-stratum counts, and no series or report. The second entry is the same session, 2026-10-08, about 04:57Z: a read-only real-evidence check of #728's `prerequisites` attestation pin and `retained()` on the finalized run directory. It wrote nothing, built no source and replayed nothing. It saw that the binding held, and the in-memory key-list hash, which equals the smoke hash. The executor logs every reader (name, date, and what they saw: series, report or neither) with the private report. Any successor pre-registration, for example of an adjusted book, must carry an exposure statement that names these readers (design §4.5).

### Addendum 2026-10-08 — Tier-1 return and acceptance (Deployment Coordinator, card owner)

Public return: hashes and labels only (§6).
- **Run:** `T00_TIER1 run RESOLVED OK`, exit 0. Driver `scripts/t00_tier1_diagnostic.py` from #728 merge `a3a91f3`, SHA-256 `94c8eeab…7508`; keys `60c128a7…329e`, published on #727 (comment 6053992089) before `selftest`.
- **Verdict on H:** RESOLVED. **Status:** DONE. Every selected path reproduced its retained identities, and the kernel re-evaluation agreed with every retained outcome.
- **Private artifacts** (`t00-step3/tier1-diagnostic-2026-10/` in the primary checkout; hashes re-computed in place by the card owner): `run/summary.json` `d21badda…e245`; `REPORT-tier1.final.md` `7ef4d7c7…f013`; `report-data.json` `b22a9f3a…8936`; `consistency-check.json` `52dce654…629d`.
- **Report recommendation (label):** Tier 2 scoping before any repair comparison. Tier 2 is scoped in the [Tier-2 scoping card](2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md) (#729, merged `afaca99`). Its admission is Joshua's.
- **Acceptance:** accepted by the card owner on 2026-10-08, after reading the report. It changes no verdict (§1).

**Reader log, continued.**
3. The executor session, 2026-10-08, about 07:10Z: the per-path sealed series and the report.
4. Joshua, 2026-10-08, about 07:12Z: the executor's findings summary in chat (no series, no keys).
5. The Deployment Coordinator, 2026-10-08, about 07:40Z: the same summary, in the executor's exposure message. Then, at about 08:10Z, the report (no series), read after the Tier-2 thresholds were fixed at `34c31c4`.

Any successor pre-registration names these readers (§8). The Tier-2 card records how they bear on its pattern table (§2.1, row 5 provenance).

## §9 — Forbidden moves

- Any change to the book, the ports, the parameters or protection; any alternative or repair run; beginning qualification.
- Any entry point other than §0.5 item 6; any code change outside #728; GLM or any external service.
- New simulations, resampling, threshold changes or resizing.
- Any private value (counts, rates, P&L, keys, timings, Pine or port bodies) in a public surface.
- Treating `NO-GO-evidence-robust` as statistical confidence or out-of-sample validation, or using any Tier-1 output to re-open it (§1).
- Writing to, or changing, the step-12 run directory.

## §10 — Audit hooks

```bash
# Card form (expect RESULT: well-formed).
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-08-t00-step12-diagnostic-tier1-card.md

# The pinned driver (expect 94c8eeab...7508).
sha256sum scripts/t00_tier1_diagnostic.py

# The sealed boundary and the admitted construction.
git show 5d25f9c:ops/c1_rail/qualification/production_source.py | sed -n '1232,1254p'
git show 5d25f9c:ops/c1_rail/qualification/p7_driver.py | sed -n '39,48p'

# The receipt's purpose and refusals (§0.6).
git show 5d25f9c:ops/c1_rail/qualification/contract.py | sed -n '963,968p'

# No private value in this card (expect no output).
rg -n "P&L =|\\$[0-9]{2,}|account [0-9]" docs/briefs/handoffs/2026-10-08-t00-step12-diagnostic-tier1-card.md | grep -v 'rg -n'
```
