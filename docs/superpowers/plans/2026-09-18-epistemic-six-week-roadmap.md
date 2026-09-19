# Epistemic decision framework: six-week sprint roadmap

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Status:** Draft for review; scope brief, not a code-level implementation plan or authority to begin the full build.
**Goal:** Demonstrate one reproducible, governable trading decision-and-learning loop using existing evidence and infrastructure.
**Architecture:** Evolve First Passage incrementally into an epistemic decision-making framework with trading as its first domain. Reuse the advisory evidence foundation; connect domain adapters through explicit contracts without treating today's trading-heavy `core/` directory as the proposed general core.
**Tech Stack:** Existing Python, repository evidence, evidence-store journal and derived indexes; storage/package changes require findings from week 1.
**Spec:** [Foundation](../specs/2026-09-18-epistemic-foundation-brief.md), [governed learning](../specs/2026-09-18-governed-learning-brief.md), [evaluation](../specs/2026-09-18-learning-evaluation-brief.md).

## 0. Sources and current-state grounding

Inspected on 2026-09-18 against `1c2472dffdc5719d4dfa89507f93f5e2f8e31cdd`. These are entry-point findings, not the completed week-1 assessment.

| Source | Established premise |
|---|---|
| [REPO_MAP](../../../REPO_MAP.md), [PIPELINES](../../../PIPELINES.md) | Existing core/lab/ops/governance ownership and import boundaries. |
| [Evidence foundation](../../../scripts/evidence_store/README.md), [belief implementation](../../../scripts/evidence_store/beliefs.py), [journal validation](../../../scripts/evidence_store/model.py) | Advisory source capture, belief assessments, applicability, historical retrieval and decision-use review already exist. These do not grant execution authority. |
| [INQHIORI](../../methodology/inqhiori-canon.md), [evaluation order](../../adr/2026-08-30-evaluation-order.md) | Existing research doctrine must be reconciled with new contracts, not silently replaced. |
| [Lab catalog](../../../lab/CATALOG.md), [question roster](../../briefs/INDEX.md), [rejection registry](../../rejected_candidates.md) | Research and failed-candidate records exist; completeness and prospective comparability remain audit questions. |
| [Production protection](../../../core/dd_protection.py), [lifecycle](../../../core/lifecycle.py), [arm gate](../../../ops/c1_rail/c1_rail_arm.py), [operating instructions](../../../CLAUDE.md) | Existing control owners remain authoritative. Reading them establishes the preservation boundary, not a recalibration proposal. |

The user reports repeated prospective revision evaluations, including failures. Use that history as the seed corpus; do not claim it already proves improving learning. Check availability, timestamps, comparators and maturity record by record. Private or archived evidence is not absent merely because a public checkout lacks it.

## Global constraints

- One existing strategy/workflow, one bounded revision family and one frozen baseline.
- Preserve existing import rules and source ownership until explicitly replaced.
- Keep goals and policies distinct from beliefs. Learning grants no authority to change objectives, risk controls, allocation behavior or execution permissions.
- Simulation is the default. Paper/shadow operation depends on verified inputs and existing permissions; no live trading, arming, data purchase or deployment is authorized here.
- Reusable configuration has one canonical definition, explicit variants/bindings, consumption-boundary validation and a pinned resolved identity. Credentials remain external.
- Use the checkout's operations launcher and recorded verification requirements. Preserve valid evidence; rerun checks when relevant inputs change.
- No universal platform, second domain, strategy optimizer, major storage migration or broad autonomous self-modification.
- The coordinator writes concrete implementation handoffs after week 1 resolves placement and interfaces.

## Phases and return points

Weeks are relative to an agreed start. Six weeks assumes consistent engineering capacity and accessible existing inputs.

| Phase | Time | Reviewable outcome |
|---|---|---|
| Establish evidence and scope | Week 1 | Current-state/gap assessment, revision-history audit, selected workflow, frozen evaluation design and bounded foundation handoff. |
| Reconstruct decisions | Weeks 2-3 | Contextual retrieval and versioned decision records connected to separate goals/constraints; auditable action or abstention. |
| Close governed learning loop | Weeks 4-5 | Persistent inquiry, outcome evaluation and proposals; rejection, authorized sandbox activation and rollback exercised. |
| Integrated acceptance | Week 6 | Reproducible comparison and separate epistemic, decision and portfolio verdicts, with remaining uncertainties. |

Evaluation starts in week 1 and runs throughout. The sprint coordinator owns combined acceptance; Joshua owns objective and policy choices outside delegated authority.

## Shared behavioral contract

These are proposed integration records, not claims of existing APIs. Week 1 maps each to a current representation or justified extension.

| Record | Producer/authority | Consumer |
|---|---|---|
| Evidence/belief snapshot | Source owners and evidence foundation; exact versions, context and knowledge cutoff | Decision workflow and evaluator |
| Objective/constraint binding | User-approved policy owner; resolved immutable version | Domain adapter and decision workflow |
| Decision | Workflow; snapshot references, alternatives, action/abstention, rationale and permission result | Simulator and evaluator |
| Outcome | Simulator/domain adapter; decision ID, event times, costs, completion state and data identity | Evaluator |
| Evaluation | Deterministic runner; pinned protocol, baseline, cohort, result and uncertainty | Inquiry and proposal workflow |
| Revision proposal | Inquiry owner; scope, evidence, expected benefit and predecessor | Authorized reviewer/promotion boundary |
| Activation/rollback receipt | Authorized promotion owner; validated revision and prior active identity | Future decisions and audit |

Trace: opportunity -> applicable evidence as known then -> decision under bound constraints -> simulated outcome -> frozen evaluation -> evidence-backed proposal -> authorized sandbox activation for later decisions. Earlier decisions remain pinned.

Missing evidence or policy needed to establish permission produces explicit blocked/abstain behavior. Delayed outcomes stay incomplete. Duplicate deliveries cannot duplicate decisions or evaluation contributions. Restart preserves durable state. Concurrent proposals against the same predecessor require conflict detection, not last-writer-wins activation. These are owed acceptance cases.

## First bounded handoff: week-1 assessment

**Selected outcome:** Evidence-backed assessment and one selected workflow with a frozen evaluation design, or an explicit dependency-blocked finding.
**Prerequisites:** The three specs and source anchors are available. Private corpus access, candidate feasibility and measurement completeness remain unverified.
**Ownership:** Assigned assessment executor produces the packet; sprint coordinator accepts it and owns combined acceptance; Joshua resolves new objective/policy authority decisions.
**Verification:** Inventory source versions, availability and timestamps; classify all revisions in the selected cohort including failures; trace one prior revision; map existing/missing interfaces; pin workflow, baseline and protocol. Report commands, interpreter, source state, results and gaps.
**Checkpoint:** Return findings after the first complete historical trace or missing producer. Record evidence in the sprint assessment packet and notify the coordinator; this does not automatically require user approval.
**Return boundary:** Return after assessment and the next bounded handoff, or a blocking scope/dependency conflict. No implementation, promotion, control changes or live operation belongs to this handoff.

- [ ] Classify capabilities as implemented, documented-only, missing or unverified.
- [ ] Inventory evaluation coverage, failed revisions and missing denominators.
- [ ] Select an accessible workflow/revision family; record rejected alternatives.
- [ ] Freeze Spec 3's measurement contract; resolve conflicts with existing authorities.
- [ ] Return an executable foundation handoff with exact placement, interfaces and checks.

## Combined acceptance and failure rule

Functional acceptance requires the specs' applicable cases, one reproducible integrated run, a declined/inconclusive proposal and a sandbox rollback. Synthetic fixtures prove mechanics only. At least one real historical revision must be traced; unavailable real inputs remain an acceptance gap.

Report separately: functional PASS/FAIL; epistemic improvement, decision improvement and portfolio benefit each supported/unsupported/inconclusive. Reliable portfolio improvement is not guaranteed within six weeks.

If week 1 cannot identify an accessible workflow and credible baseline, return revised scope and dependencies instead of building generic infrastructure. Failed integrated cases mean incomplete functional acceptance. Insufficient statistical evidence means retain the baseline and disclose uncertainty, not move thresholds.

## Document verification

Check relative links and source anchors, run `git diff --check` and applicable repository gates through `.\fp.ps1`. This PR validates planning artifacts only; future implementation handoffs require revision-bound executable evidence.
