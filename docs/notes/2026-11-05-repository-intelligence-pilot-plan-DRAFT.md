# First Passage — Repository Intelligence Pilot

**Status:** PROPOSED · advisory only · planning deliverable, not execution GO.

**Prepared:** 2026-11-05 UTC. **Inspected checkout:** `535494eecc32aa8f9276b999cf055bf46da91a21`.

**Decision:** Do these tools reduce context work or find consequential defects beyond the existing review workflow enough to justify their total cost?

**Planning budget:** one draft and one focused validation pass; no independent review round, paid tool run, installation or research trial ($0 new vendor spend; K=0).

**External facts:** documentation observations below; runtime compatibility, permissions, data handling and historical isolation remain unverified until the bounded qualification step. Drafting does not treat them as established guarantees.

This file owns this pilot proposal, its eventual evaluation summary and Joshua's pilot decisions. It does not own architecture, strategy, deployment, review policy or the decisions retrieved by a tool. Joshua initially requested planning, then authorized committing and publishing this draft with a local Claude handoff in the PR. Publication does not authorize spending, installation, service enablement, repository-source submission to the proposed tools or pilot execution. No repository contents were submitted to those services, and no pilot was run.

## 1. Scope and current owners

Reduce repeated context gathering and catch consequential defects or assumption conflicts missed by the existing Claude/Codex workflow. Retain only demonstrated improvements. Deployment continues under its existing owners; starting or passing this pilot is never a deployment prerequisite.

| Subject | Existing owner and pilot consequence |
|---|---|
| Priorities and operational work | [STATE](../../STATE.md) and its owning deployment checklist. Do not add this discretionary proposal to the operator queue or consume a deployment GO. |
| Authority, privacy and independent review | [AGENTS](../../AGENTS.md), [operational rules](../operational_rules.md), [surface allocation](../adr/2026-07-14-cc-cursor-surface-allocation.md), [seat registry](../../scripts/seat_authority.yml). Joshua decides scope, spend, access and retention. Claude reviews Codex work; Codex reviews Claude work. |
| Review implementation | [scripts/README: Independent review](../../scripts/README.md#independent-review), [Claude workflow](../../.github/workflows/claude.yml), existing merge controls. Tool findings do not supply the independent review or a clean-head acceptance. |
| Gate composition and CI | [gates.yml](../../scripts/gates.yml), [Tests workflow](../../.github/workflows/tests.yml). Add no gate, required status, production dependency or parallel check list. Markdown-only changes already have a docs-reader CI route. |
| Context retrieval | [REPO_MAP](../../REPO_MAP.md), [PIPELINES](../../PIPELINES.md), [find_owner.py](../../scripts/find_owner.py), [repo_retrieve.py](../../scripts/repo_retrieve.py), [recall](../../ops/recall/README.md), [archive retrieval](../ltm/README.md). These remain available to the baseline; tool-generated answers are assistive pointers. |
| Context architecture | [Cleanup programme](../superpowers/specs/2026-10-28-org-cleanup-programme-spec.md) owns its G1–G3/P2 work. [#1087](https://github.com/Joshua-Asante/first-passage/pull/1087) is a separate proposed amendment, not a prerequisite or an accepted instruction hierarchy. |
| Trustabl already present | [trustabl.yml](../../.github/workflows/trustabl.yml), introduced by [#1052](https://github.com/Joshua-Asante/first-passage/pull/1052). Audit and evaluate this integration; do not install a second CI job. |
| Agent procedures | The [.agents skill entrypoints](../../.agents/skills/) route to canonical `.claude/skills` sources. [Coordinator](../../.claude/skills/coordinator/SKILL.md) applies when Joshua assigns that role; this planning session does not assume the seat. [Agent improvement](../../.claude/skills/agent-improvement/SKILL.md) supports the bounded evaluation and retention decision. No new skill is needed. |

Observed baseline details, **derived from the linked owners at the inspected revision**:

- Claude's workflow is mention-triggered, requests `claude-sonnet-5`, and uses subscription OAuth. Codex integration is described there as account-level. Actual enabled app settings, models and billing must be inventoried before comparison; configuration text is not execution evidence.
- Trustabl runs on PRs, pushes to main and manual dispatch. Action SHA is `d97575c864814bf4965fa2c72c044224d372723a`; CLI `v0.1.15`; rules tag `v0.8.0` (workflow comment records `c4a3bc8104e4817b63c68b11792fe77b90d2cfbe`). Findings exit 1 is advisory; other scan failures can fail the job. PR comments are disabled; artifact retention is 14 days. Do not suppress execution failures to make a pilot appear successful. No CI results were fetched in this pass.
- #1087 was read at head `7ad5e5d1a861f42b0b3979f4860ea39d0ea17123`: open/draft, with [Claude's blocking review](https://github.com/Joshua-Asante/first-passage/pull/1087#pullrequestreview-5779931846). Its capacity, ownership and necessity questions are not settled here. Freeze the pilot to one context layout; if cleanup lands meanwhile, do not mix layouts within comparisons or credit its savings to Repowise.
- #1087 also has a CodeRabbit bot comment. This establishes its presence on that PR, not its review coverage or account-wide configuration. Inventory incumbent reviewers so rediscoveries are not claimed as additional value.

Dedup evidence, before authoring (case-insensitive search; only matches shown):

```text
rg -n -i 'repowise|codesea|greptile|trustabl|repository intelligence' lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md docs/notes docs/spec docs/superpowers .agents .github
.github/workflows/trustabl.yml:26:        id: trustabl
.github/workflows/trustabl.yml:27:        uses: trustabl/trustabl-action@d97575c864814bf4965fa2c72c044224d372723a # v0.4.3
.github/workflows/trustabl.yml:37:        if: ${{ always() && steps.trustabl.outcome == 'failure' }}
.github/workflows/trustabl.yml:39:          SCAN_EXIT: ${{ steps.trustabl.outputs.exit-code }}
```

This search and the related PR inspection justify one pilot owner; an empty local match would not prove absence of historical work.

## 2. Capability qualification before enabling anything

The requested roles are hypotheses about useful deployment, not automatic interoperability. Vendor documentation was read on 2026-11-05; it is evidence of advertised interfaces, not a successful First Passage probe. Pin exact releases and recheck the source before use.

| Tool / assigned role | Observed documentation | Still unknown; acceptance of qualification |
|---|---|---|
| **Repowise:** architecture, dependencies and decision provenance through a local index/MCP | The [project](https://github.com/repowise-dev/repowise) describes indexing source, history and decisions. [Configuration](https://github.com/repowise-dev/repowise/blob/main/docs/reference/CONFIG.md) describes local storage, hosted or local model providers and a separate embedder. Local storage alone does not establish local-only processing. | Exact release, Python/Markdown/YAML coverage, MCP tool schema, read-only allowlist, source citations, revision invalidation and total indexing cost. Prove both inference and embedding destinations, exclusions, session/history ingestion controls, telemetry setting and cache deletion. A generated decision summary must point back to the existing owner; do not adopt a generated wiki as another owner. |
| **CodeSea:** targeted unresolved assumptions/contracts | Its [About page](https://codesea.app/about) describes a hosted GitHub URL analysis, locations and failure modes; it says temporary clones are deleted while structural results remain. | No CLI/MCP, path-scoped scan, exact commit selection, non-public input route, model pin, output export or complete provider/retention contract was verified. The attempted `/privacy` page returned 404. Identify supported controls and inspectable evidence before any input. If the service only clones a live/default repo, it cannot satisfy this replay as specified. Mark unavailable; do not send the real repo as a workaround. |
| **Greptile:** diff defects and cross-file inconsistencies via GitHub review | [Introduction](https://www.greptile.com/docs/introduction) documents repository context and PR reviews. Its [CLI evaluation guide](https://www.greptile.com/docs/code-review/evaluate-with-cli) supports historical diffs and JSON output without PR comments; it explicitly distinguishes original heads from landed revisions and notes service/context drift. [Memory documentation](https://www.greptile.com/docs/how-greptile-works/memory-and-learning) describes learning from comments and commit changes. | GitHub permissions, model/tier and cost, input exclusion before indexing, provider retention/training terms, disabling prior organizational memory, and isolation from later commits/reviews. Fixed local SHAs alone do not prove remote context isolation. Use the CLI for evaluation only if isolated inputs can be demonstrated; validate the requested GitHub interface separately on a synthetic sandbox PR. |
| **Trustabl:** reliability/safety checks for supported agent infrastructure | The [v0.1.15 README](https://github.com/trustabl/agent-reliability-analyzer/blob/v0.1.15/README.md) documents deterministic local scanning, JSON/SARIF and cached-rule offline use; enrichment/fix functions are separate. The existing workflow pins the versions above. | Map actual repository paths to supported detectors/rules. Verify cached rules' resolved commit, input exclusions, output evidence and scan-only behavior. Zero detected supported surfaces is **not applicable**, not a clean reliability verdict. The Python dispatch scripts, skill files and YAML workflow cannot be presumed covered simply because agents use them. |

Qualification uses a tiny synthetic fixture first, after execution is authorized: one known issue, one clean case, one excluded canary and one deliberately stale revision. Inspect input manifests and outputs, denied writes and network destinations. A canary's absence from output is not proof it was never ingested: also inspect the effective configuration, file access/egress evidence and provider contract. Disable autofix, enrichment, auto-approval, generated instruction edits, publication, unattended hooks and write-capable MCP operations. Allow only index/cache writes in the isolated evaluation area and findings output. If the tool cannot enforce this mode, do not use that interface.

No new production dependency or findings database: local tool caches are disposable, outside the production environment and untracked. Do not add packages to `requirements-ops.lock`, register global MCP servers or change `.claude`/`.codex` settings for this plan. Later approved tooling remains separately versioned and removable.

## 3. Approved material and isolation

The [public-clone/data-class rules](../../AGENTS.md#public-clone-posture) still apply to public Git history. A public URL, tracked file, path exclusion or an existing integration does not itself authorize sending everything to another provider.

Before a run, Joshua approves a **positive input manifest per recipient**: source revision, exact paths/blob hashes, destination, purpose and retention. Start with selected tooling, tests and their public specifications. Exclude credentials, account data, restricted/vendor datasets, Pine, strategy ports, `effective_inputs.json`, private strategy sources, private archive content, local artifacts and derived restricted outputs. Do not collect them to redact later. A source class permitted for Claude is not thereby permitted for Codex or the new services.

The corpus curator builds standalone evaluation copies containing only those approved bytes. Shared worktrees with reachable full history are insufficient. Preserve dependency and owning-document context where approved; if exclusion removes context necessary to judge a contract, mark the case ineligible or explicitly coverage-limited before scoring. Do not replace real inputs with synthetic values and still call it a full historical-PR result.

Keep caches, session logs, usage records and findings under an isolated local evaluation root such as the already ignored `local_artifacts/repository-intelligence-pilot/<run-id>/`. Tools cannot read the curator's answer key. External materialization or a private sandbox GitHub repository is a later named access decision, not authorized here. Do not create a public fork to make a hosted tool work.

## 4. Historical sample and leakage controls

**Proposal for Joshua:** 10 distinct PRs, selected before any tool output; 8 minimum, 12 maximum only by a recorded pre-run choice. Use two reserved candidates for eligibility failures, not disappointing results. Include code, cross-file controls, agent infrastructure and ownership/documentation. Do not choose only known bug fixes. Aim for at least three genuinely supported Trustabl cases; if the frozen sample has fewer, its result is coverage-limited and cannot justify broad retention.

Candidate inventory below was obtained from local merge subjects and changed-file statistics, not a review-outcome search. It is a shortlist, not a frozen corpus. Merge IDs identify discovery evidence **only**; none is asserted to be the original review head. All original base/head/time fields remain unresolved until C0.

| Candidate | Reason for inclusion / observed changed surface | Eligibility concern |
|---|---|---|
| [#1056](https://github.com/Joshua-Asante/first-passage/pull/1056) · `9509cf1f` | Agent handoff isolation: `scripts/agent_handoff.py` and tests | A repair PR; count in a predeclared repair stratum, not as an outcome-enriched default |
| [#1052](https://github.com/Joshua-Asante/first-passage/pull/1052) · `6d8fab5d` | Trustabl CI configuration | Measures configuration/coverage; may be unsupported by Trustabl itself |
| [#1014](https://github.com/Joshua-Asante/first-passage/pull/1014) · `f710fce9` | Document budgets, gate manifest, generated map and tests | Cross-file contract; gate authoring remains outside pilot execution |
| [#1013](https://github.com/Joshua-Asante/first-passage/pull/1013) · `26a7624d` | Markdown anchor parser and tests | Large baseline file; keep the same relevant context in every arm |
| [#1059](https://github.com/Joshua-Asante/first-passage/pull/1059) · `a4dbce6c` | Tool removal, consumers and doc references | Correlated with cleanup PRs; report that cluster together |
| [#1071](https://github.com/Joshua-Asante/first-passage/pull/1071) · `3df683fc` | Skill trims and `sync_skills.py` | Verify supported skill detectors; inspect historical bytes for restricted material |
| [#1051](https://github.com/Joshua-Asante/first-passage/pull/1051) · `dfcfcb10` | Builder-round template and owning proposal | Contract/owner retrieval case; no research trial |
| [#1035](https://github.com/Joshua-Asante/first-passage/pull/1035) · `20e48e69` | AGENTS, STATE and retired-route routing | Later route decisions must not enter the historical case |
| [#1070](https://github.com/Joshua-Asante/first-passage/pull/1070) · `2fe186b1` | Calendar extension, source references and tests | Include only approved reference data; test cross-file usage, not unverified external dates |
| [#1023](https://github.com/Joshua-Asante/first-passage/pull/1023) · `4664cbd4` | `lab/builder/venue.py`, README and tests | Exclude if meaningful validation requires restricted strategy/data inputs |
| Reserve [#1040](https://github.com/Joshua-Asante/first-passage/pull/1040) · `45396758` | Cross-firm policy/assumption document | External claims need contemporaneous approved evidence; no present-day facts substituted |
| Reserve [#1033](https://github.com/Joshua-Asante/first-passage/pull/1033) · `315ea66b` | Enumeration and decision-record consistency | Documentation case; cannot stand in for missing supported agent-code coverage |

If these fail coverage, use a frozen, outcome-blind replacement rule: search earlier merged PRs for the missing path stratum; select the lowest PR number among eligible candidates in that search window. Record the window, paths, exclusions and ordering before opening outcomes. If eight comparable cases cannot be formed within budget, stop as inconclusive; no silent expansion of permissions or sample.

For every accepted case:

1. Curator resolves the first substantive independent review request time `t0` and its head from event/check/review metadata; uses the submitted review's `commit_id` only if it actually matches that request. Reconstruct the contemporaneous target-base SHA and merge base. Preserve evidence URLs and full SHAs. An ambiguous or unavailable original revision is ineligible; current `refs/pull/N/head`, a merge parent and a final fixed head are not substitutes.
2. Freeze the review diff, allowed head snapshot, relevant owning docs as of `t0`, and sanitized task intent available then. Strip later-edited PR descriptions, comments, review outcomes, CI annotations, post-`t0` tests/fixes, current STATE, issue closure messages and this plan from the evaluator packet. Present-day privacy/authority restrictions still constrain access; historical instructions supply context, not execution authority.
3. For provenance retrieval, supply only approved history ending at `t0`; otherwise declare history unavailable in **all** arms. Remove remotes, later refs, reflogs and object alternates from evaluator copies. Each arm/case gets a fresh index and clean session; no current wiki, memory, chat transcript or shared retrieval cache. Probe that a seeded later-only marker cannot be retrieved before admitting the runner.
4. Curator seals known outcomes and fix evidence separately. Evaluators and initial adjudicators receive no answer key and do not browse original PRs. Randomize arm/case order with a frozen seed. Keep repeat runs separate. Model pretraining exposure to public code cannot be eliminated; disclose it rather than claim perfect blindness.
5. Only after outputs and initial validity judgments are locked does the curator unblind later history. A subsequent fix is a lead, not ground truth: verify the claim against the original revision. A newly noticed defect introduced after `t0` is not a hit.

The present planner has read #1087's outcomes and repository history; it must not serve as a blind evaluator. Exclude #1087 and the firm-reply PR #1090 from this sample because this conversation already contains their review outcomes.

## 5. Comparable arms and workflow

Freeze one review protocol, model/version/settings, task prompt, approved source manifest, relevant existing tests, tool versions, service tiers and budgets. Preserve the same historical code/doc snapshot across arms. Disable uncontrolled web retrieval and incumbent bot output in the replay. This is a contemporary re-review of historical inputs, not a reproduction of the original models' behavior.

| Arm | Controlled comparison |
|---|---|
| **B** | Existing Claude/Codex procedure with STATE/owner orientation, `rg`, normal local navigation/retrieval and the existing relevant checks; no tools under evaluation. Preserve investigator/reviewer separation. |
| **B+R** | Same procedure plus Repowise retrieval only |
| **B+C** | Same procedure plus CodeSea on unresolved contracts identified from the task packet before outputs |
| **B+G** | Same procedure plus Greptile diff review |
| **B+T** | Same procedure plus the pinned, applicable Trustabl scan |
| **B+S** | Same procedure plus the eligible combination S, fixed from qualification/coverage before scored outputs; same total per-cell resource ceiling |

Each single-tool arm preserves raw tool-only output as well as its independently validated result; a host-agent finding must not automatically be credited to the tool. Not applicable, unavailable, failed, timed-out and completed-with-zero-findings are distinct statuses. An inapplicable B+T case still records its detection/coverage outcome but contributes no claimed clean scan. If a tool cannot meet input isolation, its scored arm is unavailable; report the incomplete four-tool comparison and let Joshua decide scope before execution continues.

**Two baseline questions must remain separate.** B isolates incremental assistance to Claude/Codex. Trustabl is already installed, so B+T is the incumbent scan comparator, not a new benefit. Also compare to the sealed original review record: Claude, Codex, applicable CI and any active CodeRabbit/other reviewers. A finding already there is a rediscovery. Missing incumbent records mean novelty is unknown, not additional. Do not claim value beyond today's complete workflow unless the C0 app inventory identifies and accounts for its active components; unmatched incumbent components limit that claim.

A single scored cell has two phases under one budget:

1. **Before implementation, simulated:** read historical STATE and owning specification, answer three curator-set retrieval questions (owner/current-at-`t0` decision, dependency/consumer, relevant test/evidence); identify unresolved contracts. Repowise supplies citations; CodeSea is invoked only for the preregistered unresolved-contract scope. No code is implemented.
2. **Before merge, simulated:** inspect the original diff; Greptile reviews it and Trustabl scans applicable agent tooling in their arms. The independent Claude/Codex reviewer assesses evidence and existing acceptance rules. The baseline receives the same orientation answers format and review task. No merge is performed.

Combination order is R → targeted C → G and applicable T → independent validation, with provenance retained at every stage. There is no assumed API interoperability or automatic contradiction detector. If outputs conflict, the reviewer reads the cited originals and records the conflict/disposition. Findings remain advisory; only a separately authorized implementation can act on them.

Keep available host models and settings identical within each pair. A vendor's hidden model or token usage is recorded **unknown**, never zero or inferred from host usage. Deterministic Trustabl uses no inference budget for its scan, but triage still counts. If a hosted model cannot be matched, present a budget-matched service comparison separately from the model-controlled evidence; no claim that the tool alone caused the difference. Treat version drift as an invalid pair or a separately labeled block, never silently pool it.

## 6. Proposed budget and stopping bounds — Joshua's decision

These are proposed caps, **not spend authorization or vendor price quotes**. Obtain actual prices before starting; if the minimum design does not fit, return a smaller explicit proposal instead of changing the thresholds after seeing output.

| Item | Proposed limit |
|---|---|
| Sample and repeats | 10 PRs × 6 arms = 60 scored cells; repeat two PRs chosen by the frozen seed across all six arms = 12 repeat cells. No other stochastic retries. At the 12-PR maximum: 84 cells total. |
| Cell effort | ≤60,000 observable total tokens across investigator, tool inference where reported, independent review and corrections; one investigative pass and one review. Count cached/replayed input and output; log hidden usage separately. ≤$4 marginal service/compute cost per cell, including failed attempts. All arms get the same ceiling, not equal forced consumption. |
| Overall tokens | ≤6M observable tokens including setup, index generation/refresh, repeats, adjudication and reporting. Stop starting new work at 5M. Hidden vendor tokens make total-token comparability incomplete. |
| Cash | ≤$500 new cash total: up to $336 cells at the 12-PR maximum, $100 qualification/index/setup, $64 closeout/reserve. No automatic paid renewal. Existing subscription allocation and runner costs are still reported. |
| Review rounds | Planning/qualification packet: one independent review plus one correction review if commissioned; replay cells as above; final retention packet: one independent review plus one correction review. Existing Rules 6/7 remain stricter where applicable. |
| Human effort and valuation | Record setup, curation, adjudication and maintenance separately; proposed 16 person-hours envelope and $75/hour valuation for the cost calculation. Combined evaluation cost target ≤$1,700 ($500 + 16 × $75), plus disclosed existing-subscription allocation. These are accounting assumptions for Joshua, not claimed labor charges. |
| Runtime failures | At most one infrastructure rerun for a diagnosed transient failure within the same caps; preserve the failed attempt. A repeated failure family stops that tool. Do not rerun because the findings are weak. |

Stop the affected arm immediately for unauthorized data access/egress, source mutation, unisolated later evidence or a wrong revision. Retain only permitted evidence of the failure and restore the sandbox. Invalid outputs remain in the cost/coverage denominator. Stop starting cells at 80% of the cash or effort envelope if the remaining paired work cannot fit; never discard the costly failed runs from the report. No extra pilot round, service or corpus expansion on silence.

## 7. Finding contract and independent adjudication

Use PR discussion entries or temporary Markdown/JSON review artifacts, not a database. One row per distinct claim, linked to raw output; duplicate root causes share an identity. Required fields:

| Field | Required content |
|---|---|
| Claim/provenance | Tool and release/rules/model where known; run/case/arm; full original revision; exact file/line or immutable document span; inspectable output/evidence reference |
| Consequence | Trigger and affected behavior, assumption or decision; severity and applicable acceptance rule; affected consumer for cross-file claims |
| Evidence class | **Unverified hypothesis**, **supported inference**, or **verified defect**. Only reproducible failures or decisive source/contract contradictions at that revision reach verified defect. |
| Disposition | **Open**, **rejected**, **resolved**, or **deferred**; reason, named reviewer, date and existing owning-record reference. Deferred includes a concrete owner/wake condition. Resolution cites verification, not a tool confidence score. |
| Evaluation labels | Root-cause/duplicate group; in original review?; in replay B?; in B+T?; marginal to S without this tool?; coverage and adjudication limits |

Initial adjudicators see randomized claims without tool labels, original verdicts or subsequent fixes. Cross-agent separation still applies: a model cannot independently validate its own produced finding. Use the other Claude/Codex agent for host-originated claims and for the plan/retention review; an author follow-up is supporting evidence only. Preserve disagreements as unresolved; Joshua decides material disputed dispositions. Do not give an implementer an answer-key-informed prompt and call that blind review.

Validate using safe focused reproductions or source-contract checks against the original snapshot, with synthetic permitted inputs. Do not run historical workflows, deployments, agent tools or strategy/backtest trials just to validate a finding. A missing external premise remains an inference. No reviewer upgrades a finding because the vendor labels it critical.

## 8. Metrics and proposed retention thresholds — Joshua's decision

Freeze definitions and thresholds **before** scored runs. Report counts and per-PR paired results, then medians/ranges; 8–12 PRs are a screening exercise, not statistical proof. Related cleanup PRs form a cluster, not independent replications. Report repeats separately rather than selecting each arm's best run.

Let V be independently verified consequential root causes, F rejected false claims, U unresolved claims and D repeated claims. A consequential defect affects behavior, evidence validity, authority/privacy or a cross-file contract; cosmetic/style suggestions do not qualify. Supported inferences and useful assumption questions are reported separately and do not inflate V.

- **Additional findings:** `V(tool arm) minus V(B)`; also compare to B+T and the complete available historical review record. Count unique mechanisms once, not each affected file. A tool's unique contribution is its validated roots not present in the other individually tested tools or baseline, supported by its raw evidence. This is attribution, not a causal full factorial ablation.
- **Noise:** precision `V / (V + F)` on resolved unique claims; unresolved fraction `U / (V + F + U)`; false-claim fraction `F / (V + F + U)`; duplicate fraction `D / all emitted claims`. Always show denominators; zero claims means precision undefined, not 100%. Correct but nonconsequential suggestions are separate overhead, not defects or false positives.
- **Context:** correct owner/dependency/evidence answers, files/bytes read, observed context tokens, elapsed lookup time and stale/incorrect authority citations. Measure cold indexing and warm retrieval separately; charge initialization to the pilot and refresh to expected ongoing use.
- **Effort/cost:** active reviewer time, latency, corrections, setup and ongoing maintenance; input/output/cache/reasoning tokens if available; vendor/API/compute charges and allocated subscriptions. Total cost includes triage of false, duplicate, unresolved and nonconsequential output. Report dollars per additional verified defect, undefined when the denominator is zero.
- **Coverage:** eligible and attempted cases, supported paths/detectors, completion rate and every skipped/invalid run. Historical-known defects found is descriptive sensitivity, not recall over all possible defects.

Proposed retention rules:

| Criterion | Threshold to recommend retention |
|---|---|
| Boundaries and evidence | No unresolved unauthorized disclosure or mutation; every counted finding has the full contract and independent validation; no contaminated case counted as evidence. |
| Defect-focused tool | ≥2 additional verified consequential roots across ≥2 PRs beyond B, including ≥1 absent from all available original review findings; ≥1 contribution beyond the other retained tools/incumbent B+T where applicable. Trustabl itself is judged against B for retention of its existing integration. |
| Retrieval-focused Repowise alternative | On ≥8 paired cases, 100% correct owner/authority answers, ≥25% median lookup-time reduction and ≥20% median context-token reduction, including refresh amortization; no loss of verified defects relative to B. This can justify retrieval-only retention even without two new defects. |
| Noise and reviewer burden | Precision ≥75%; false-claim fraction ≤20%; unresolved fraction ≤10%; duplicate fraction ≤40%. Median incremental triage ≤10 minutes/PR and 90th percentile ≤20 minutes; report effort even when outputs are unsupported. |
| Useful combination | ≥3 additional verified roots across ≥3 PRs beyond B and ≥1 beyond incumbent B+T; ≥1 absent from the complete available historical record; no baseline consequential defect lost. Retain a smaller subset if the rest add no marginal value. |
| Cost and maintenance | ≤$150 fully allocated incremental evaluation cost per additional verified consequential defect for defect tools; expected ongoing cash ≤$100/month across retained tools and maintenance ≤1 person-hour/month. Retrieval-only retention needs expected saved labor value ≥1.5× total recurring cost. Show projections at 10 and 20 PRs/month, not an assumed actual volume. |

No speculative avoided trading loss is assigned a dollar value. Price unavailable, hidden costs that cannot be bounded, insufficient supported cases, missing incumbent evidence or discordant repeats yield **inconclusive**, not retention by default. Repowise's role-specific efficiency result cannot justify retaining every scanner. A high-severity but unverified allegation does not override the thresholds. Joshua may choose a different threshold before testing; after testing a changed threshold defines a new proposal, not retroactive success. Selecting a smaller subset from these results is a recommendation: an unrun subset has not passed the combination threshold and needs separate bounded confirmation before that claim is made.

## 9. Sequence, owners and deliverables

Role assignments below are proposed and must name actual sessions before dispatch. The corpus curator is separate from blind evaluators; independent reviewer is separate from planner/implementer. No standing coordinator appointment or parallel agent dispatch is implied.

| Checkpoint | Owner / dependency | Bounded output and completion condition |
|---|---|---|
| **C0 — qualify and freeze** | Joshua chooses pilot lead/curator and budget; lead inspects existing integrations; other-agent reviewer checks packet | Resolve vendor identities, interfaces, prices, coverage and data routes; synthetic probes only after access/run GO. Freeze original revision manifest, inputs, sealed outcomes, arms, models, seeds and thresholds. Maximum two qualification/review iterations. Unknown external premises are resolved or explicitly accepted as named assumptions under Rule 0 before a formal review relies on them. |
| **C1 — assemble and smoke-check** | Curator/runner implementer; C0 complete | Minimal disposable runner/worksheet, fresh sandboxes and indexes, one synthetic positive/negative/exclusion/staleness check per eligible interface. No new framework or service. Independent reviewer verifies isolation and source-write denial. A failed boundary blocks only the affected tool; incomplete requested coverage returns for Joshua's scope decision. |
| **C2 — paired historical replay** | Fresh evaluator sessions and cross-agent validators; C1 complete | Frozen 60 primary plus 12 repeat cells for the proposed 10 cases; raw outputs, status, revision, usage/cost and claim records. Stop at the declared bounds. Lock outputs before unblinding. No changes to historical or current production code. |
| **C3 — adjudicate and decide** | Independent reviewer, curator unblinding, then Joshua | One summary table in this owner: paired counts, historical novelty, noise, coverage, total cost, role-specific result, retained subset recommendation and limitations. Link temporary inspectable evidence. Recommend retain, reject or inconclusive separately for each tool and combination. |
| **C4 — optional adoption/closeout** | Existing owning workflow implementer; only for retained tools with separate authorization | At most one small configuration/documentation PR and one necessary follow-up, using existing owners. No mandatory check. Verify scan/retrieval-only mode, failure/fallback behavior and removal. Existing independent review and merge acceptance apply unchanged. |

There is no need to finish #1087, thin AGENTS, migrate catalogs, add a glossary or reorganize code to execute this evaluation. If those owners change, the pilot lead records the new revision for a later separate comparison. Do not turn the pilot into a dependency for that work either.

After **accepted changes**, the assigned implementer refreshes a retained local index against the exact accepted revision and approved input manifest, checks its revision/citations, and records refresh cost. A stale index is bypassed in favor of canonical files. Refreshing an index grants no permission to modify decision owners. A material accepted finding is recorded at its existing specification, campaign, plan or PR; this pilot keeps only the evaluation reference. Reassess old evidence only when a relevant change or identified flaw challenges it, not on a timer or merely because a new scanner exists.

Proposed retention of temporary evaluation artifacts: 30 days after Joshua's decision, then remove caches and redundant output after preserving the minimal approved evidence needed to inspect the recommendation. The curator verifies external deletion where available; no deletion guarantee is claimed for an unverified service. Preserve only unresolved obligations and non-regenerable supporting evidence under the repository's [retention rules](../operational_rules.md#16-retention--an-artifact-must-earn-its-place-and-deletion-is-classified-by-execution-not-by-folder). No permanent findings store or duplicate decision log.

Rollback for later adoption: disable/remove only pilot-added adapters, access and schedules, delete their disposable indexes, and return to existing retrieval/review. Because Trustabl predates this plan, changing or retiring its existing CI is a separate explicit disposition of that integration, not automatic pilot cleanup. No rollback changes `gates.yml`, deployment rules or trading authority.

## 10. Decisions remaining with Joshua

These choices are prepared for the parent session; no response is needed to publish this draft, and silence authorizes no pilot execution.

1. **Scope/budget:** recommend the 10-case design, named role separation, caps and thresholds in §§4–8. Critical path: pilot execution only; no deployment impact. Alternative: keep this proposal parked with $0 new spend.
2. **Approved recipients/material:** recommend local, allowlisted synthetic qualification first, then only explicitly approved historical source manifests. Authorize each external destination separately after its retention/permissions are known. Unknown CodeSea controls and Greptile remote context isolation are concrete open dependencies, not inferred permission.
3. **Unavailable tools:** recommend returning a qualified subset proposal if any tool cannot satisfy coverage/isolation; do not silently substitute another product or call the four-tool pilot complete.
4. **Retention/adoption:** decide only on C3's evidence. Passing a pilot authorizes neither production dependency changes nor mandatory checks; C4 remains optional and bounded.

## 11. Planning validation and limits

The plan is documentation only. Relevant checks are the checkout launcher/environment validation, Markdown paths/anchors, document budgets, a focused structural audit of this file, and applicable publication hooks/CI. The authorized publication follow-up commits and pushes this plan and opens a draft PR containing the local Claude handoff. Joshua will start that local session to investigate the four capability gaps in §2 and update this owner with inspectable evidence and unresolved limits. No scanner, historical replay, installation, live settings change, repository-source submission to the proposed services, merge, deployment or trade is authorized. The proposed $500 new-cash and 6M observable-token ceilings remain unapproved. Independent review is still outstanding; a Claude session that edits the plan cannot independently review its own changes.

**Improvement — historical-context leakage:** the proposed original-review experiment can accidentally expose later fixes through full Git history or learned service context. The evidence is Greptile's documented history/memory behavior and Repowise's history indexing. This plan's isolated corpus and unblinding sequence address that mechanism within the planning request. Disposition: **proposed**, owner Joshua; actual isolation and value remain unmeasured. No standing instruction or additional registry was created.
