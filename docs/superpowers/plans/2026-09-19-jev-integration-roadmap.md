# Jev integration roadmap and pilot proposal

Date: 2026-09-19. Status: planning proposal; no installation, credentials, external data transfer, or workflow activation performed.

**Experiment update (later September 19):** The user subsequently authorized installation and a small live experiment, then explicitly approved its sanitized corpus transfer to OpenRouter. The official skill is installed and Jev access verified. The [frozen experiment result](../../../recovery/jev-retrieval-pilot-20260919/RESULTS.md) falsified the 20% context-savings prediction on its small corpus: 6.4% improvement, equal top-3 coverage, correct abstention on two cases. No default integration or production workflow was activated. The original planning-only status above describes this document at creation.

**Research update:** The [follow-up investigation](../../notes/audits/2026-09-19-jev-research-workflow-fit.md) revises the proposed pilot priority to context ranking, followed by evidence triage. It documents `jev-1.13.0`, compares primary benchmark reports with recent S1/S2/PR review evidence, and adds matched deterministic and small-model baselines. The original proposal below remains for context; its failure-triage-first preference and unresolved model-ID statement are superseded by that research. No pilot has been activated.

**Goal:** Reduce Codex usage pressure and the operator's supervision time per accepted task. API spending is secondary, per the operator's explicit preference.

**Architecture:** Deterministic collection and change detection produce bounded evidence packets. Jev labels or ranks supplied evidence; ordinary code applies policy and returns compact source-linked results. Codex retains implementation, investigation, substantive review and combined acceptance.

**Scope:** Development workflow only. This proposal introduces no changes to trading behavior or production decision authority.

This is a roadmap and first evaluation handoff, not a ready-to-execute implementation specification. After design acceptance, use `superpowers:writing-plans` for the selected implementation slice and `superpowers:executing-plans` for execution. Access to this roadmap does not authorize later phases.

## What the video establishes

Reviewed the auto-generated transcript of [I Paired Jev With Astra. Here’s What Changed.](https://www.youtube.com/watch?v=2XFXe-oGnrI), not its underlying benchmark artifacts.

- At [1:00–2:24](https://www.youtube.com/watch?v=2XFXe-oGnrI&t=60s), the presenter distinguishes valid output structure from correct judgment.
- At [6:52–8:38](https://www.youtube.com/watch?v=2XFXe-oGnrI&t=412s), a third-party dispatch experiment reports 71% lower cost and 90% less time for routing work. This does not establish equivalent savings on complete coding tasks.
- At [9:08–10:18](https://www.youtube.com/watch?v=2XFXe-oGnrI&t=548s), the presenter reports roughly 50% reductions in coding/email experiments, with uncertainty fallback, and separate browser figures of 2.5x speed and 77% lower cost. Sample size, scoring methodology and reproducible artifacts were not established by the transcript.
- At [11:15–11:35](https://www.youtube.com/watch?v=2XFXe-oGnrI&t=675s), the actionable principle is avoiding an expensive model call altogether.

Recommendation: adopt that principle; test the savings locally. Replacing broad code review is not justified by these demonstrations.

## Verified capability and integration boundary

Jev supports bounded Choice, Score and Noul questions; application code composes the results. It does not supply free-form diagnosis or patches. [TypeSafe introduction](https://docs.typesafe.ai/introduction)

TypeSafe advertises $0.042 per million input tokens and free output, with workload-specific speed comparisons. These are provider claims, not measurements on this repository. [Launch explanation](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

Choice and Score confidence is derived from their distributions, not a guarantee that a decision is correct; Noul has no separate confidence field. Select thresholds from held-out local cases rather than treating 0.95 confidence as 95% measured accuracy. [Confidence documentation](https://docs.typesafe.ai/confidence)

The documented direct endpoint is `POST https://api.typesafe.ai/v1/systemone`; the official skill and SDK are integration aids. Actual account access, available immutable model IDs and rate limits remain unverified. [Quick start](https://docs.typesafe.ai/introduction/quickstart)

Codex supports external MCP tools. This supports a tool integration; it does not establish a facility for replacing every internal routing or reasoning step. Model dispatch outside the current task would be a separate integration. [Official MCP documentation](https://developers.openai.com/es-419/docs/extend/mcp?surface=cli)

## Repository grounding

Inspected working tree at HEAD `c2e6eb2cbe159b60fdff7873b9e96aef943c46df`, with existing unrelated modifications and untracked work. No implementation tests run for this planning task.

- `README.md`, `PIPELINES.md` and `REPO_MAP.md` provide existing entry points; use their routing instead of repeatedly inventorying the whole repository.
- `scripts/gates.yml` and `scripts/gate_manifest.py` own gate composition. Jev must not maintain a competing gate list or choose to omit required checks.
- `scripts/fp.py` and `scripts/README.md` own operations environment selection and commands.
- `.claude/skills/babysit/SKILL.md` requires complete review/check inspection and a per-item ledger. Jev can group and prioritize items, but cannot silently discard comments or declare merge readiness.
- `scripts/README.md` assigns independent review to the existing pre-ratification workflow. Jev scoring cannot confer its authority.
- The September 17 testing-workflow plan is a proposal, not proof of installed capability. Its referenced `tools/local_verification/README.md` is absent in this checkout. The pilot must discover actual evidence producers rather than assume the proposed recorder exists.

## Where savings are most plausible

| Priority | Candidate | Work Jev could remove | Boundary |
|---|---|---|---|
| 0 | Deterministic change detection and exact deduplication | Repeated polling/re-reading unchanged checks and identical errors | No Jev call for unchanged input or exact matches |
| 1 | Test-failure triage | Initial sorting of long logs into related failure groups | Keep all failures, exact excerpts and source locations; no inferred pass |
| 2 | Context selection | Repeated broad search and reading unrelated files | Rank candidates from `rg` and indexes; always include required instructions and explicit user references |
| 3 | Review-comment grouping | Repeated classification and duplicate investigation | Retain every comment ID and trusted-author rules; coordinator adjudicates each |
| 4 | Task/model routing | Expensive dispatch reasoning for routine work | Separate host-capability check and explicit permitted-model policy |
| Later | Narrow requirement checks | Repeated small yes/no checks against supplied evidence | Advisory; never substitutes for cross-component review or tests |

Start with failure triage if the baseline shows enough repeated cases. Context selection becomes first if it dominates observed usage. Do not build five tools at once.

## Approach selection

1. **Recommended: small repository-owned adapter using the official API.** Begin as a CLI for offline replay; add one MCP tool only after benefit is demonstrated. It offers explicit inputs, narrow data exposure and one configuration owner, at the cost of maintaining a small adapter.
2. **Existing community tooling.** Evaluate before adopting, without installing during planning. `jev-code` covers discovery/check/triage, but its README currently says npm 0.0.1 is a nonfunctional placeholder and Windows is untested. `jev-review` supplies quality scores and expects the coding model to interpret them. Neither is proven to reduce our supervisory workload. [jev-code](https://github.com/devagrawal09/jev-code), [jev-review](https://github.com/NiazMorshed2007/jev-review)
3. **External dispatch harness.** Potentially saves entire model invocations, but adds orchestration and recovery work. Defer until measured routing volume justifies it.

Installing a skill alone is not a savings mechanism. Every adopted use must name the reasoning turn, repeated read or manual intervention it removes.

## Proposed behavioral contract

Proposed components live under `tools/jev_workflow/`; these do not exist yet. Keep the first adapter outside production packages. Proposed tests live under `tests/test_jev_workflow.py`; dependency and launcher compatibility must be resolved in the implementation spec.

**Input producer:** A local collector reads an explicitly selected completed test run or supplied log, its command, exit code, revision and working-tree fingerprint. It extracts error blocks with stable IDs and line ranges. For subsequent modes, existing Git/GitHub interfaces provide changed paths or comment IDs; Jev does not fetch those itself.

**Request:** Operation, original task, bounded evidence items, source identity, question-schema version and resolved policy hash. Begin with public or synthetic fixtures. Any private corpus needs a separate explicit data-scope decision before transmission; omit account data, credentials, vendor datasets and private strategy sources from this pilot.

**Jev output:** Per-item fixed labels such as `environment`, `assertion`, `collection`, `infrastructure`, `unknown`, plus distributions and supported confidence fields. Labels are candidate classifications, not proven root causes. Jev may propose grouping only among supplied item IDs.

**Local output:** Compact groups with all member IDs, literal evidence excerpts, source locations, classification and uncertainty. The wrapper verifies ID membership and coverage. Explanatory text comes from source excerpts and deterministic templates, not invented Jev prose.

**Consumer:** Codex opens the relevant evidence and investigates. A successful pilot lets it skip the initial broad sorting pass, while retaining responsibility for diagnosis and every unresolved failure.

**Failure behavior:** Missing key, timeout, service error, invalid response, unknown label, incomplete coverage or ambiguity returns an explicit incomplete/fallback result and the deterministic evidence index. Never convert missing data into an empty successful report. No background retries that repeatedly wake Codex.

**State:** Cache by operation + exact content hashes + schema + policy + model identity. A changed log, revision, dirty-tree fingerprint or policy invalidates reuse. Atomically persist only completed results; interrupted requests cannot appear complete after restart. Deduplicate concurrent identical requests; count all actual billed attempts. If only a mutable model alias is available, record it honestly, disable cross-run cache reuse, and re-evaluate after provider changes.

**Configuration:** One versioned canonical policy object supplies limits, enabled operations, candidate labels, thresholds, endpoint and schema versions. Host bindings reference it. Credentials come from an environment reference. Default mode is shadow; proposed pilot ceiling is $1, not authorization to spend it. An off switch restores the existing workflow.

**Concrete cases:**

- Twenty failures sharing one missing import: show one group with all twenty IDs and the original import errors; Codex validates the diagnosis once.
- Similar-looking failures with different exceptions: preserve separate evidence; uncertain grouping falls back rather than hiding the distinction.
- A secret-bearing log: the collector refuses remote submission; local handling continues.
- A new commit or edited log after a cached result: reject the stale result and rebuild the packet.
- Jev outage: return the same deterministic index the control arm uses; no workflow dead end.

## Evaluation and economics

Use three arms on identical frozen inputs: current workflow; deterministic preprocessing only; deterministic preprocessing plus Jev. This isolates Jev's contribution from savings ordinary scripts could deliver.

Begin with 30 representative completed cases: 10 for schema development and 20 held out. Include ambiguous mixed failures and service failure fixtures. Freeze labels before held-out scoring and adjudicate disagreements from raw evidence. Follow with 10 bounded live tasks if offline results justify it. These are screening samples, not proof of rare-error reliability.

Record per accepted task: observable Codex calls and input/output usage where available, context volume, tool round trips, wall time, operator intervention minutes, rework, fallback frequency, actual Jev usage and cost, model/settings, revision and policy hash. Separate operator active time from unattended waiting. Use isolated matched sessions or label concurrent account usage as confounded; do not attribute account-wide usage changes to one task.

Suggested promotion targets, not predictions:

- At least 20% lower observable Codex usage per accepted task against the deterministic arm. Where task-level usage is unavailable, report calls/context as proxies and do not claim exact quota savings.
- At least 25% less operator intervention time across comparable live tasks, without increased rework.
- Zero lost failure/comment IDs and zero missed must-escalate cases in the evaluated corpus.
- No omitted required checks or displaced required reviews; no worsening of p95 task time beyond 10%.
- Measurable savings after including preparation, retries, fallback, final review and ongoing maintenance.

At the advertised input rate, 1,000 decisions of 5,000 total billed input tokens each cost about $0.21, excluding any gateway differences. Request overhead and question text must be included in actual billing measurements. Cheap inference is not the main constraint: useful integration and avoided reasoning are.

Illustrative time ceiling: if eligible decisions consume 30% of a task and the new path removes 80% of that work, gross whole-task savings are 24%, before integration overhead. The video's 50% is not our forecast.

Subscription capacity and cash are separate outcomes. Avoiding reasoning may extend useful Codex capacity; it does not imply a proportional reduction in a fixed subscription bill. Count actual avoided reset purchases or subscription changes only if they occur.

## Roadmap

| Phase | Reviewable outcome | Acceptance and return boundary |
|---|---|---|
| A: baseline and design | Frozen corpus, three-arm protocol, selected first operation | Identify a repeated eligible bottleneck; return before adapter implementation |
| B: shadow adapter | Bounded packets and valid advisory reports on the corpus | Coverage/fallback/cache tests and held-out comparison; return before host activation |
| C: one live integration | One tool used on 10 bounded tasks | End-to-end evidence meets promotion targets; return before more operations |
| D: measured expansion | Add the next highest-value operation only | Independently demonstrate benefit over scripts and existing workflow |

Timebox the initial baseline/design effort to one working session and adapter feasibility to two further sessions. These are effort caps, not delivery promises. Stop expansion when savings cannot plausibly repay setup and maintenance within a month at observed task volume.

Combined acceptance belongs to the coordinating agent, with the operator owning adoption. Component tests alone do not establish workflow savings.

## First bounded handoff: evaluation-ready pilot design

**Selected outcome:** One chosen operation, a frozen representative corpus manifest, an agreed measurement protocol and a concrete implementation spec. Completion means a reviewer can trace each input to its expected report and fallback.

**Prerequisites:** Operator accepts the proposed scope. Actual TypeSafe access and safe corpus availability must be established; no key values belong in chat or the repository. Historical usage evidence may be absent; if so, collect a prospective baseline instead of inventing it.

**Ownership:** Executor is the coordinating agent working inline. The coordinator retains combined acceptance. Operator owns adoption and any new spending/data scope. No delegation is commissioned by this handoff.

**Verification:** Record current revision/dirty state, corpus item identities and hashes, label provenance, input coverage, measurement availability, and the exact reasoning step expected to disappear. Confirm actual supported host interfaces. A provider smoke test, if subsequently authorized, uses synthetic data only. No runtime validation is claimed by this document.

**Checkpoint:** Report after corpus inspection if failure triage is not frequent enough, required telemetry is unavailable, or access/Windows compatibility changes the approach. Record evidence in a dated `docs/notes/audits/` pilot report; retain raw private evidence outside versioned documents.

**Return boundary:** Return to the coordinator when the pilot spec and evaluation manifest are reviewable, or when missing evidence/access prevents a defensible design. Excluded follow-on work: installation, paid calls, automatic hooks, standing-instruction edits, model dispatch, CI activation and production changes. These require the next bounded handoff within user authorization.

## Verification required in the subsequent implementation plan

Before project Python work run `./fp.ps1 doctor` from the implementation checkout. Use its `./fp.ps1 python -m pytest` route for focused tests and `./fp.ps1 check` for required gates; report the actual interpreter, command, revision and results. Do not add an SDK outside the locked-environment process or bypass a failed doctor.

Cover real collector-to-report behavior with success, mixed failures, missing evidence, unknown IDs, incomplete responses, timeout, interrupted writes, concurrent requests, revision/content changes and disabled mode. Mock transport tests prove wrapper behavior only; live synthetic testing is separately needed to establish provider compatibility. After enabling MCP, exercise one actual host call. Preserve raw evidence and compare accepted outcomes with the control arm.

No code, packages, standing instructions, hooks or account settings were changed during this analysis.
