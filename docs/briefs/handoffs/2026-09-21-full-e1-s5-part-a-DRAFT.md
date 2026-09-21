# GLM handoff — Protected Full E1 / S5 (T04): genuine Part A, preserved expansion prefix and committed G5 decision — DRAFT for the operator's rulings

**Type:** cc_handoff (frozen-spec implementation; one executor owns the engine adaptation, prefix capture and reconstruction)
**Date:** 2026-09-21 (DRAFT — **the three decisions in §0.5 were ruled by the operator on 2026-09-21 (all recommended options)**; becomes FROZEN when S4 has merged and the anchors are re-taken at the S4 merge head)
**Status:** not dispatchable yet. Predecessor: **S4 accepted and merged** (joint N2/Part B green on Linux, `PART_A_READY` reached, the coordinator's acceptance entry in the ledger). Branch `claude/s5-part-a` off the S4 merge head; push; no PR until the coordinator says so.
**Executor:** GLM (single writer for every file in §2). **Coordinator:** Claude (rulings, checkpoint C3, integration, acceptance; **T05 integration follows S5's acceptance** per the amendment). **Operator:** Joshua (the three decisions below; any further versioned change is a `CHECKPOINT`).
**Parent:** [execution-slices plan §S5 + the S3/S4 acceptance entries](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md) · [governing spec](../../superpowers/specs/2026-09-17-protected-full-e1-campaign.md) §2.3 (PART_A_READY → FULL_PASS_READY), §2.4 (statistical/RNG preservation), E04/E05/E06/E08/E09 · [S4 packet](2026-09-21-full-e1-s4-joint-n2-part-b-DRAFT.md) (the widened custody and the checkpoint-keyed family this extends) · [T05 packet §0.5 F3](2026-09-21-full-e1-t05-result-and-seal.md) (`PART_A_FAILED` / `FULL_PASS_READY` are the only names S5 may write; T05's `checkpoint_receipts` row shape must keep working for PART_A rows).
**Authority:** the files in §2. Engine edits are limited to necessary store-free integration; **a numerical behavior discrepancy returns to the coordinator before any accepted formula changes**; no tolerance relaxed; no allowance/ceiling change; no S6+ work; no activation; no self-acceptance. A `DONE` status supplies no permission.

## 0. Rule 0 reads (Phase 0 — report anchors in §7; line numbers pinned at the S4 merge head)
- The engine, read before any edit: `qualification/part_a.py` (`_run_part_a` — the sampling/append loop, its request/provider/proof inputs, the pilot addresses, outer panel seeds, path addresses and source-occurrence order), `regime.py`, `provider.py`, `replay.py`, the adjudicators (`adjudication.py`, `result_adjudication.py` — the exact-Decimal side), `benchmark_part_a.py`; `execution/compute.py` (`run_n1_compute`, S4's `run_n2_compute`, `stage_request`, `_ReplayProvider`, `_run_stage`, `initial_state`).
- S4's generalized checkpoint route (every `{'N1','N2'}` closed set becomes `{'N1','N2','PART_A'}` — list each site in §7): `derive_checkpoint_plan`, `build_checkpoint_evidence` + parsers, `_checkpoint_projection`, `parse_checkpoint_snapshot`, work-phase sets (`PART_A`, `PART_A_CAPTURE`, `PART_A_G5` already exist in `campaign_budget.PHASES`), `g5.validate_campaign_checkpoint`, `campaign_protocol`, `campaign_funding` roles, `campaign_supervisor` role branches, `worker.main`, `release_schema`/`profile`.
- Custody: S4's widened tables already admit `checkpoint='PART_A'` (S4-D1) — **no layout change in S5**; the family's checkpoint-keyed field sets gain the PART_A set (§1).
- Budget: `part_a_initial_paths` / `part_a_expanded_paths` in the frozen budget binding (the fixture's 4 / 8) — reduced TEST_ONLY depths, to be reported distinctly from reference-depth qualification.
- Harness: `test_campaign_n2_linux.py` helpers; the selector (S4's placement rule: before the S2 OOM case); subset iteration; `s2_run_evidence.py --expect-head`.
- Repo constraints: no module-level mutable state (frozen-adjudicator walk); line 3 on committed bytes only.

## 0.5. Design decisions (ruled by the operator 2026-09-21 — constraints, not options)

**S5-D1 — Prefix custody: two durable artifacts from one run.** The single Part A worker writes the **initial-prefix result** to the output mount (fsynced, then read-only by convention) *before* deciding expansion, and the **final result** (initial prefix + appended panels, or initial alone when no expansion is prescribed) after. The guardian archives both byte-for-byte; the checkpoint family's PART_A capture carries both digests, `initial_panels`, `final_panels`, `expansion_required` and the inclusive-tolerance comparison inputs. The byte-identical prefix assertion holds on the archived bytes of one run. A crash after the initial file but before the final file → `IN_DOUBT`, saved bytes retained for inspection only — no panel resume, no replacement pilot, no checkpoint rerun. *Alternative rejected:* reconstructing the prefix by a second replay (the slice forbids it: "capture the prefix from that computation rather than reconstructing it by another replay").

**S5-D2 — N2 FULL baseline transport.** The guardian stages the committed N2 capture bytes (from S4 custody, read-only) into the worker's input mount; the worker derives the N2 FULL pass rate from those captured outcomes (`n2_full_outcomes`), and G5 independently derives the same baseline from the custody rows through S4's parsers — never from the worker's stated value. A mismatch between the two derivations refuses the assessment (`mismatched N2 FULL baseline`). *Alternative rejected:* passing the baseline as a number in the plan (an unobserved input the worker could be handed wrongly).

**S5-D3 — Release/profile.** One new literal `qualification_execution_release/v7` + profile `/v7` with `supported_checkpoints = dispatch_checkpoints = ['N1','N2','PART_A']` (all three compute checkpoints; the result/seal route is still not enabled — that flag is T06/S8's, added with T05's integration); v6 stays exactly `['N1','N2']`; fresh attempts only. Snapshot `/v8` = `/v7` with the PART_A checkpoint entry (prefix digests, panel counts, expansion decision); budget-profile v3 pairs v5–v8. *Alternative rejected:* enabling finalization in the same literal (would let an S5 attempt claim a route that does not exist yet).

## 1. Interfaces (produce together)
- `compute.run_part_a_compute(contract, source, budget, *, n2_full_outcomes)` — adapts the existing `_run_part_a` loop and its request/provider/proof inputs; preserves the disjoint pilot addresses, outer panel seeds, path addresses and source-occurrence order including legitimate duplicates; returns the initial-prefix document and the final document as separate byte strings from one computation.
- `derive_checkpoint_plan(campaign_plan_bytes, 'PART_A', predecessor_receipt_bytes)` — binds the exact joint (N2) checkpoint receipt and the N2 capture digest.
- `g5.validate_campaign_checkpoint(..., checkpoint='PART_A', ...)` — reconstructs the panel-major source-session occurrence inventory, path outcomes, the initial-prefix artifact and the expansion decision with the canonical installed adjudicators (exact Decimal); applies the final floor and the FULL sanity comparison after required expansion; decision `CONTINUE` → `FULL_PASS_READY`, `FAILURE` → `PART_A_FAILED`.
- Worker result: `qualification_worker_result/v1` records gain `stage='PART_A'` with panel index, path index and source-occurrence address; the PART_A checkpoint-keyed assessment field set adds `initial_panels`, `final_panels`, `expansion_required`, `tolerance_comparison`, `floor_comparison`, `full_sanity_comparison`.
- Roles `part_a_worker` (phase `PART_A`) and `part_a_g5` (phase `PART_A_G5`), admitted only on `/v7` with the campaign at `PART_A_READY`/`VALID`.
- **Checkpoint C3** (before the first acceptance-grade Linux run): the PART_A field sets, the `/v8` snapshot diff, the two-artifact capture contract and its crash semantics, the baseline-transport contract, the float-vs-Decimal parity results on the supported frozen boundary configurations, and the E-case ownership for E04/E05 and the PART_A halves of E06/E08/E09.

## 2. Files (single writer)
`execution/{compute.py, worker.py, evidence.py, g5.py, service.py, campaign_store.py, campaign_supervisor.py, campaign_funding.py, campaign_protocol.py, release_schema.py, profile.py, release.py}`; `qualification/{checkpoint_plan.py, evidence.py, journal_snapshot.py}`; `qualification/part_a.py` **only** for store-free integration seams (report every line); installed fixtures; tests: new `tests/ops/qualification/execution/test_campaign_part_a.py`, extensions to `test_campaign_n2.py`, `test_campaign_recovery.py`, `test_worker.py`, `test_release.py`, `test_profile.py`, `test_journal_snapshot.py`, `tests/ops/qualification/{test_part_a.py, test_regime.py, test_evidence_reconstruction.py, test_result_adjudication.py}`; new Linux file `tests/integration/qualification_boundary/test_campaign_part_a_linux.py` registered per S4's placement rule. **Forbidden:** T05's modules and tests; `qualification/seal.py`; accepted formulas and tolerances; any S2/S3/S4 Linux assertion.

## 3. Behavior (binding)
After the joint PASS receipt (`PART_A_READY`), one Part A operation produces the initial panels and, exactly when prescribed, the appended panels `[initial_panels, expanded_panels)`; the final prefix is byte-identical to the initial; conditional expansion uses inclusive tolerance equality; the final floor and the FULL sanity comparison apply after required expansion. Reject omitted or unnecessary expansion, a substituted or reordered prefix, altered source occurrences, a missing pilot identity, and a mismatched N2 FULL baseline. Interruption during expansion cannot relaunch; remaining-budget exhaustion blocks completion without inventing a statistical failure. Required assertions from the slice, verbatim in the adapter/capture test:

```python
assert final_panel_bytes[:len(initial_panel_bytes)] == initial_panel_bytes
assert actual_panel_count == (expanded_panels if expansion_required else initial_panels)
assert part_a_worker_launch_count == 1
```

- [ ] Engine-adapter boundary tests before wiring: no expansion, required expansion, exact tolerance equality, below-floor failure, above-FULL failure, unchanged initial prefix.
- [ ] Trace the actual `_run_part_a` inputs and reuse its loop; capture the prefix from that computation.
- [ ] One metered worker invocation through the S3/S4 route; independent G5 reconstruction; the five rejections.
- [ ] Float compute vs exact-Decimal G5 on the supported frozen boundary configurations — a disagreement is an engine-contract conflict returned to the coordinator, never a relaxed tolerance.
- [ ] Interruption during expansion → IN_DOUBT, no relaunch; budget exhaustion → no completion, no fabricated FAIL.

## 4. Verification
- Windows (`./fp.ps1`, frozen bytes): the S4 line-1 selection + `test_campaign_part_a.py` + the §2 extensions (`--workers 2`, zero skips); line 2; line 3 on the committed final tree; `check`; `git diff --check`. Fail-on-base (S4 merge head): `part_a_worker` refused on `/v6`; `validate_campaign_checkpoint('PART_A')` refused by the S4 builder. Pure boundary tests may use exact outcome vectors.
- Linux: subset iteration first, then acceptance-grade: the full S4 file set **plus** the Part A file. Required: genuine Part A without expansion → `FULL_PASS_READY`; with prescribed expansion (if a synthetic source can produce it economically; otherwise the arithmetic boundary test stands separately and is **not** called a full-route witness — disclose); a genuine below-floor or above-FULL failure → `PART_A_FAILED`; crash during expansion → IN_DOUBT with the initial prefix retained; g5 death + exact retry. Actual synthetic market/session sources for the Linux campaigns.
- Return: heads, record IDs with counts, run IDs with record hashes, the `/v7` release/profile digests, the initial/final prefix identities per Linux campaign, the parity results, and the reduced TEST_ONLY depths stated distinctly.

## 5. Checkpoint C3
Push and return: head + `git diff --stat <S4 merge head>...HEAD`; the line-1 record; the §1 freeze as a table; the fixture ledger; fail-on-base; the parity results; anything S5-D1–D3 did not anticipate. Wait for GO.

## 6. Forbidden
A second replay to reconstruct the prefix; a panel resume, replacement pilot or checkpoint rerun after interruption; a relaxed tolerance or a worker/G5 disagreement tolerated; a baseline passed as an unobserved number; changing an accepted formula without the coordinator's ruling; enabling the result/seal route in the v7 literal; writing any progression name outside F3; module-level mutable state; `git stash`; commits without `git diff --stat`; pushing while a Linux run is in flight; claiming acceptance.

## 7. Executor return
_Pending._
