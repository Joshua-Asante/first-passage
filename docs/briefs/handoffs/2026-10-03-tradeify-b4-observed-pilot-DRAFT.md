# B4 observed-pilot implementation handoff — DRAFT

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
max_risk: low
capabilities:
  - repository.read
  - tests.run
  - worktree.write
constraints:
  - Draft only; no dispatch until campaign-owner acceptance and revision freeze.
  - No merge, spend, deployment, arming, research or production statistical execution.
  - No monitors or work owned by Coordinator 2; no term-8 or C-prime implementation.
  - No destructive commands even for scratch; use a fresh unique scratch directory.
  - Foreground work only; no private values in returns or commits.
acceptance:
  - B4-A1 observed existing pilot
  - B4-A2 rejects fabricated or altered evidence
  - B4-A3 bounded durable capture and failure ordering
  - B4-A4 historical reopen and release binding
  - B4-A5 measured-closure impact inventory
```

**Status:** NOT DISPATCHABLE. Prepared 2026-10-03 under Joshua's assignment to Codex Coordinator 3; Claude coordinator (3) confirmed scope in the campaign chat. This draft grants no action until the owner accepts and freezes it. It returns one implementation outcome; the campaign roadmap and combined acceptance remain with Claude.

## §1 Context and execution contract

**Selected outcome:** One existing Part A pilot produces observed selection/replay identity that is retained in its bounded capture and independently checked by G5. Return a reviewable implementation with local evidence and a precise measurement/Linux evidence debt list. Do not execute the next campaign step.

**Prerequisites:** Read AGENTS.md, STATE.md, H9, Full-E1 spec §2.6–2.7, the [proposed B4 contract](../../notes/2026-10-02-tradeify-b4-observed-pilot-PROPOSED.md), and the current C′ card. Source review pin is `ebe5c0ba846d2d7b75227d7b8302a818945974f5`; it is not an implementation base authorization. Before dispatch, Claude must commit acceptance of the proposed schema and exact worker-result version/field shape, select and pin the compatible C′/H9 base, allocate the shared G5 file, and freeze the named Linux selection and measurement ownership. An unresolved prerequisite returns NEEDS_CONTEXT. B4 is before T06 and never an R1 prerequisite.

**Ownership:** Executor is a campaign-owner-selected worker after freeze; Codex Coordinator 3 reviews the return; Claude coordinator (3) integrates, owns ENG-2 remeasurement and accepts the combined campaign result. Joshua controls measurement timing and any operational authority. Coordinator 2 retains existing reviews, hyper work and monitors.

**Verification:** B4-A1–A5 below are mandatory fail-first acceptance cases. Run the affected Windows tests and repository gates through this checkout's launcher after `fp.ps1 doctor`. Retain commands, interpreter, exact revision/working-tree state and launcher record.json paths; verify completed status, zero verification exit, stable source, complete capture and valid reports. Linux evidence is separately dispatched by Claude; local tests do not discharge it or B4's pre-T06 gate.

**Checkpoint:** Before code, send Claude and Coordinator 3 a source/interface read report covering observation producer, capture envelope, G5 consumer, historical version routing and closure membership. Report a base/interface contradiction before editing. At return, supply the exact implementation revision, changed files, evidence and remaining measurement/Linux dependencies.

**Return boundary:** Return DONE_WITH_CONCERNS when the bounded implementation and local verification are ready with external acceptance debts explicitly retained; NEEDS_CONTEXT on unresolved contract/base/size/authority conflict; BLOCKED on an unavailable required environment. Stop before remeasurement, Linux dispatch, integration, T06, recovery, term 8 or C′ follow-on work. Branch publication/PR grants must be issued explicitly in the frozen dispatch if required; this low-risk draft grants neither.

## §0 Source reads and behavioral footprint

Source-read anchor: 2026-10-03, commit ebe5c0ba846d2d7b75227d7b8302a818945974f5. Read ops/c1_rail/qualification/part_a.py and the producer/consumer files below at that revision; re-anchor before implementation.

Follow proposed B4 contract items 1–7 as one observable trace: actual probe draw → replay identity checks → callback bytes → worker payload → finalized capture → G5 reconstruction → capture-bound assessment → historical reopen. No additional pilot, namespace or sample. No observer callback may grant recovery or result authority.

Starting production files (all under `ops/c1_rail/qualification/`): `part_a.py` (actual observation); `execution/compute.py` (single serialization and callback cardinality); `execution/worker.py` (transport); `execution/evidence.py` (strict versioned encoding/parsing); `evidence.py` (independent G5 validation). Locate `PartACompute` and its consumers before changing the dataclass. If capture/protocol/release code must change beyond this footprint, return the exact dependency to Claude for a revised card; do not silently expand it. Never change shared core controls, protected strategy sources, plan seeds, formulas or thresholds.

Existing producers: actual panel/path/replay objects and admitted source; existing custody: bounded worker capture and attestation; proposed interfaces: `on_pilot_observed`, `PartACompute.pilot_observation_bytes`, strict versioned nested observation. The proposed contract specifies their content. The final freeze must select the exact worker-result version and reader compatibility rule; a worker must not decide those policies mid-build.

## §4 Falsifiable outcome and acceptance cases

Hypothesis: the existing executed pilot can supply observed identity through bounded capture and G5 without an additional pilot.

Falsifier: any acceptance case below fails, or the design requires a new draw or larger allowance. Return the exact conflict; do not expand the contract.

- [ ] Read sources and return the Phase-0 interface/closure report. Confirm each planned producer exists on the frozen base.
- [ ] Add failing cases in `tests/ops/qualification/test_part_a.py`, `tests/ops/qualification/execution/test_worker.py`, `tests/ops/qualification/execution/test_campaign_part_a.py` and the owning G5 reconstruction tests. Use real engine/adapter/encoder/consumer entrypoints. Test names below are new acceptance requirements, not claims of existing tests.
- [ ] Implement one observation and its complete consumer path; preserve old exact-history inspection under its originating version.
- [ ] Run the affected tests, inspect the complete diff, and run the repository check gate. Return the implementation and closure inventory; do not run measurement or Linux without their separate dispatch.

**B4-A1 — `test_observed_pilot_uses_executed_selection_once`:** a synthetic admitted source drives the real engine and worker. Count original sampler/replay calls; enabling observation adds none. The captured order/multiplicity and complete replay triples equal the objects that actually crossed the provider boundary; G5 independently accepts them. The test must fail against plan-only encoding, not pass by injecting a fabricated observation into a stub.

**B4-A2 — `test_observed_pilot_rejects_missing_or_substituted_evidence`:** through real parser/G5 paths, reject absent observation, plan-only digests, wrong seed selection, reordered/duplicated/substituted occurrence rows, truncated replay, another work's envelope, changed digest, noncanonical bytes and extra schema keys. Recompute an attacker's inner digest where appropriate so the test exercises expected-selection and envelope checks, not only checksum rejection.

**B4-A3 — `test_observed_pilot_capture_failure_never_publishes`:** missing/duplicate callback, callback exception, partial replay, oversized payload and interruption before finalized capture yield no B4-complete assessment. Exercise before and after callback, before and after frame write, and after durable capture. A complete capture may be validated/signed without recompute; a partial spool cannot. Confirm no allowance/profile enlargement and preserve the original prefix-before-expansion guarantee.

**B4-A4 — `test_observed_pilot_reopen_preserves_release_and_history`:** reopen retained capture and assessment, verify identical observation bytes and binding; inspect an old plan-only historical receipt byte-for-byte without upgrading its authority; reject old evidence in a B4-required new release. Prove a pilot observation alone never enables H9 R2 / D3 compute recovery. Do not reimplement signing recovery.

**B4-A5 — closure inventory:** compare changed modules against the accepted Stage 1c closure and installed release inputs, report every changed identity, and explain callback/serialization metering and predictor placement. `part_a.py` and `execution/compute.py` are present in retained Stage 1c measurement records. Changes require Claude's ENG-2 remeasurement, with timing owned by Joshua. Carry the complete proposed Linux cases in `tests/integration/qualification_boundary/test_campaign_part_a_linux.py`; freeze their actual node IDs at the owner's later dispatch.

## §6 Gate criteria and return

RESOLVED requires all frozen acceptance cases to pass with valid evidence. A failed case is FALSIFIED for this implementation claim; missing evidence is AMBIGUOUS and never acceptance.

Accept the contract and frozen dispatch only after schema/version/base and C′ file ownership are explicit. Accept the implementation locally only on valid evidence for A1–A5. Accept B4 for T06 only after the required combined Linux/capture evidence and measurement/release consequences have been judged on the same identity. H9 R1 continues on its own gates. Term 8 and H9 R2 / D3 recovery remain separate.

Verdict: ACCEPT only when the named evidence and frozen contract agree; otherwise REJECT the affected outcome. Worker status is DONE only when its frozen handoff is fully discharged; DONE_WITH_CONCERNS retains the owner-controlled Linux/measurement debt; NEEDS_CONTEXT reports a missing contract decision; BLOCKED names unavailable infrastructure.

## §0.5 Clarifying decisions before dispatch

Claude must accept or revise the proposed observation schema, freeze the worker-result version and historical-reader rule, select the compatible implementation base and allocate the C′ shared G5 file. These named decisions remain open; the executor returns NEEDS_CONTEXT rather than choosing them. Hypothesis: the real pilot can supply observed identity within the existing bounded capture. Reject if doing so requires another pilot or an enlarged ceiling; return that conflict to the owner.

## §5 Forbidden moves

- Do not dispatch from this draft, run production statistical work, merge, spend, deploy or arm.
- Do not change sample identity, formulas, limits, locked strategy sources or private-data policy.
- Do not create monitors, absorb term 8/C′/H9 R2, or make B4 a prerequisite of R1.
- Do not destroy scratch, run background work, or publish private values.

## §10 Audit hooks

Run from the frozen implementation checkout. The direct artifact checks precede the complete gate run, so malformed handoff text is caught cheaply.

```powershell
.\fp.ps1 doctor
.\fp.ps1 python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-tradeify-b4-observed-pilot-DRAFT.md
.\fp.ps1 python scripts/check_brief.py docs/briefs/handoffs/2026-10-03-tradeify-b4-observed-pilot-DRAFT.md --type handoff
.\fp.ps1 --workers 2 python -m pytest tests/ops/qualification/test_part_a.py tests/ops/qualification/execution/test_worker.py tests/ops/qualification/execution/test_campaign_part_a.py
.\fp.ps1 check
git diff --check
```

The new G5 cases must be included in the exact test command frozen at dispatch after locating their owner on that base. Linux node IDs and measurement runs remain the campaign owner's separate dispatch. Current documentary verification and its limitations travel in Coordinator 3's revision-bound return, not as a claim that these future implementation cases passed.
