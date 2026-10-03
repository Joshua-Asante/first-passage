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

**Selected outcome:** One existing Part A pilot produces observed selection/replay identity that is retained in its bounded capture, with outer membership independently checked and inner path structurally checked by G5 (owner-selected option (a)). Return a reviewable implementation with local evidence and a precise measurement/Linux evidence debt list. Do not execute the next campaign step.

**Prerequisites:** Read AGENTS.md, STATE.md, H9, Full-E1 spec §2.6–2.7, the [proposed B4 contract](../../notes/2026-10-02-tradeify-b4-observed-pilot-PROPOSED.md), and the current C′ card. Source review pin is `ebe5c0ba846d2d7b75227d7b8302a818945974f5`; it is not an implementation base authorization. Before dispatch, satisfy every gate in §0.5: operator C3-rule admission, option-(a) contract freeze, B4 release allocation after C′-final, the PART_A-only reader matrix, ordering after K3/RC-4, compatible base and shared-file ownership, static maximum size, and exact Linux/evidence selection. An unresolved prerequisite returns NEEDS_CONTEXT. B4 is before T06 and never an R1 prerequisite.

**Ownership:** Executor is a campaign-owner-selected worker after freeze; Codex Coordinator 3 reviews the return; Claude coordinator (3) integrates, owns ENG-2 remeasurement and accepts the combined campaign result. ENG-2 option C already places the one PART_A remeasurement on the integrated pre-S8 candidate; B4 must be named in its covered-change set and land before that candidate freezes. Joshua retains operator admission and operational authority. Coordinator 2 retains existing reviews, hyper work and monitors.

**Verification:** B4-A1–A5 below are mandatory fail-first acceptance cases. Run the affected Windows tests and repository gates through this checkout's launcher after `fp.ps1 doctor`. Retain commands, interpreter, exact revision/working-tree state and launcher record.json paths; verify completed status, zero verification exit, stable source, complete capture and valid reports. Linux evidence is separately dispatched by Claude; local tests do not discharge it or B4's pre-T06 gate.

**Checkpoint:** Before code, send Claude and Coordinator 3 a source/interface read report covering observation producer, capture envelope, G5 consumer, historical version routing and closure membership. Report a base/interface contradiction before editing. At return, supply the exact implementation revision, changed files, evidence and remaining measurement/Linux dependencies.

**Return boundary:** Return DONE_WITH_CONCERNS when the bounded implementation and local verification are ready with external acceptance debts explicitly retained; NEEDS_CONTEXT on unresolved contract/base/size/authority conflict; BLOCKED on an unavailable required environment. Stop before remeasurement, Linux dispatch, integration, T06, recovery, term 8 or C′ follow-on work. Branch publication/PR grants must be issued explicitly in the frozen dispatch if required; this low-risk draft grants neither.

## §0 Source reads and behavioral footprint

Source-read anchor: 2026-10-03, commit ebe5c0ba846d2d7b75227d7b8302a818945974f5. Read ops/c1_rail/qualification/part_a.py and the producer/consumer files below at that revision; re-anchor before implementation.

Follow proposed B4 contract items 1–7 as one observable trace: actual probe draw → replay identity checks → callback bytes → worker payload → finalized capture → G5 independent outer check plus structural inner checks → capture-bound assessment → historical reopen. No additional pilot, namespace or sample. No observer callback may grant recovery or result authority.

Starting production files (all under `ops/c1_rail/qualification/`): `part_a.py` (actual observation); `execution/compute.py` (single serialization and callback cardinality); `execution/worker.py` (transport); `execution/evidence.py` (strict versioned encoding/parsing); `evidence.py` (independent outer and structural inner G5 validation). Locate `PartACompute` and its consumers before changing the dataclass. Release pairing needs separately assigned edits to execution release-schema/allow-lists; those are an explicit pre-dispatch dependency. If capture/protocol/release code must change beyond this footprint, return the exact dependency to Claude for a revised card; do not silently expand it. Never change shared core controls, protected strategy sources, plan seeds, formulas or thresholds.

Existing producers: actual panel/path/replay objects and admitted source; existing custody: bounded worker capture and attestation; proposed interfaces: `on_pilot_observed`, `PartACompute.pilot_observation_bytes`, strict versioned nested observation. The proposed contract specifies their content. The final freeze must select the exact worker-result version and reader compatibility rule; a worker must not decide those policies mid-build.

## §4 Falsifiable outcome and acceptance cases

Hypothesis: the existing executed pilot can supply observed identity through bounded capture and G5 without an additional pilot.

Falsifier: any acceptance case below fails, or the design requires a new draw or larger allowance. Return the exact conflict; do not expand the contract.

- [ ] Read sources and return the Phase-0 interface/closure report. Confirm each planned producer exists on the frozen base.
- [ ] Add failing cases in `tests/ops/qualification/test_part_a.py`, `tests/ops/qualification/execution/test_worker.py`, `tests/ops/qualification/execution/test_campaign_part_a.py` and the owning G5 reconstruction tests. Use real engine/adapter/encoder/consumer entrypoints. Test names below are new acceptance requirements, not claims of existing tests.
- [ ] Implement one observation and its complete consumer path; preserve old exact-history inspection under its originating version.
- [ ] Run the affected tests, inspect the complete diff, and run the repository check gate. Return the implementation and closure inventory; do not run measurement or Linux without their separate dispatch.

**B4-A1 — `test_observed_pilot_uses_executed_selection_once`:** a synthetic admitted source drives the real engine and worker. Count original sampler/replay calls; enabling observation adds none. The captured order/multiplicity and complete replay triples equal the objects that crossed the provider boundary. G5 independently accepts outer membership and checks the inner path structure only. Assert the callback runs after pilot_end and the predictor refusal, before initial-panel sampling; probe_seconds and predicted_seconds retain the base timer points. Observation construction/serialization adds no RNG calls and stays outside the predictor interval while its cost remains metered. The test must fail against plan-only encoding, not pass by injecting a fabricated observation into a stub.

**B4-A2 — `test_observed_pilot_rejects_missing_or_substituted_evidence`:** through real parser/G5 paths, reject absent observation, plan-only evidence under the B4 revision, wrong outer probe selection, invalid occurrence numbering, non-whole blocks, blocks not contiguous within the observed panel, invalid applicable calendar adjacency or path-date clock, sampled/replayed disagreement, truncated replay, another work's envelope, changed digest, noncanonical bytes and extra keys. Preserve legal repeated source IDs. Recompute an attacker's inner digest where appropriate to exercise structural and envelope checks. Include a structurally valid alternate inner selection and report that exact inner RNG selection/flat-edge eligibility cannot be independently rejected under option (a); CP-6 bars verification remains separate.

**B4-A3 — `test_observed_pilot_capture_failure_never_publishes`:** missing/duplicate callback, callback exception, partial replay, oversized payload and interruption before finalized capture yield no B4-complete assessment. Exercise before and after callback, before and after frame write, and after durable capture. A complete capture may be validated/signed without recompute; a partial spool cannot. Confirm no allowance/profile enlargement and preserve the original prefix-before-expansion guarantee.

**B4-A4 — `test_observed_pilot_reopen_preserves_release_and_history`:** reopen retained capture and assessment, verify identical observation bytes and binding; inspect /v7, /v8 and C′-final plan-only historical receipts byte-for-byte under their original contracts without upgrading authority; reject plan-only evidence in the later B4 release. Test every frozen release/checkpoint/worker-result pairing, with any new worker-result schema PART_A-only and N1/N2 plus worker.py:245 unchanged. Prove a pilot observation alone never enables H9 R2 / D3 compute recovery. Do not reimplement signing recovery.

**B4-A5 — closure inventory:** compare changed modules against the accepted Stage 1c closure and installed release inputs, report every changed identity, and explain callback/serialization metering and predictor placement. `part_a.py` and `execution/compute.py` are present in retained Stage 1c measurement records. Before dispatch, changes require Joshua's C3-rule admission of all four named worker measured-closure modules (and any separately owned release_schema.py edit). ENG-2 option C requires Claude's one integrated pre-S8 remeasurement covering B4 explicitly. Freeze a static maximum-byte calculation including the expanded inventory, pilot outer panel, two horizon arrays, full envelope and framing; exercise the maximum fixture without enlarging the ceiling. Prove no edits to the T00 P7 closure and preserve production.py's optional-callback route without a B4-complete claim. Carry the complete proposed Linux cases in `tests/integration/qualification_boundary/test_campaign_part_a_linux.py`; freeze their actual node IDs at the owner's later dispatch.

## §6 Gate criteria and return

RESOLVED requires all frozen acceptance cases to pass with valid evidence. A failed case is FALSIFIED for this implementation claim; missing evidence is AMBIGUOUS and never acceptance.

Accept the contract and frozen dispatch only after every §0.5 gate is recorded at the frozen revision. Accept the implementation locally only on valid evidence for A1–A5. Accept B4 for T06 only after the required combined Linux/capture evidence and measurement/release consequences have been judged on the same identity. H9 R1 continues on its own gates. Term 8 and H9 R2 / D3 recovery remain separate.

Verdict: ACCEPT only when the named evidence and frozen contract agree; otherwise REJECT the affected outcome. Worker status is DONE only when its frozen handoff is fully discharged; DONE_WITH_CONCERNS retains the owner-controlled Linux/measurement debt; NEEDS_CONTEXT reports a missing contract decision; BLOCKED names unavailable infrastructure.

## §0.5 Clarifying decisions before dispatch

Owner-selected G5 scope is option (a): independent outer membership; structural inner checks only, under the protected-worker boundary. No flat-edge proof or exact inner selection independence is claimed. CP-6 bars verification stays separate. Record the following before dispatch:

1. Joshua's C3-rule admission for `part_a.py`, `execution/compute.py`, `execution/worker.py`, `execution/evidence.py`; a separate named owner's admission for required `execution/release_schema.py` edits. Other lanes' admissions do not extend here.
2. Claude's allocation of a B4 execution release after C′-final, with owner/footprint for release-schema and all allow-lists. `/v7`, `/v8`, C′-final retain plan-only behavior; the B4 release requires observation. Any worker-result bump is PART_A-only. Inventory nine hard-coded readers and keep N1/N2/staged-N2 payload parsing unchanged.
3. B4 follows K3/RC-4 and C′-final. Pin the resulting RNG, plan and mechanics versions and derive the outer probe accordingly. Allocate the shared `qualification/evidence.py` changes after C′ step 2.
4. Accept the concrete observation schema and compute the worst-case entire framed payload at maximum admitted identifier/date widths. No finite bound or insufficient room means NOT DISPATCHABLE, not a larger limit.
5. Pin callback invocation after source `part_a.py:182,186-187`, before :207. Retain actual pilot objects with no additional RNG/replay; construct/serialize observation rows after the predictor gate.
6. Name B4 explicitly in ENG-2 option C's one integrated pre-S8 measurement; freeze exact Linux selection and evidence responsibilities. Local implementation evidence alone cannot discharge the gate.
7. Preserve T00 P7 closure disjointness, including `regime.py`, `blocks.py`, `paths.py`, `production_source.py`, `replay.py`, `runner.py`. `ProductionExecutor.run_part_a` in `production.py:251-264` is out of scope: keep callback optional/unset there and do not label that route B4-complete.

The executor returns NEEDS_CONTEXT for any missing gate. Reject if the contract requires another draw, broader G5 trust, a P7 edit or an enlarged ceiling; return the concrete dependency to the owner. These prerequisites do not gate H9 R1.

## §5 Forbidden moves

- Do not dispatch from this draft, run production statistical work, merge, spend, deploy or arm.
- Do not change sample identity, formulas, limits, locked strategy sources, T00 P7 closure modules, production.py or private-data policy.
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
