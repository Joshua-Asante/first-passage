# Jev research against recent First Passage work

Research date: 2026-09-19. Purpose: improve the Jev adoption decision for Codex capacity and operator supervision. No Jev inference was run; no software was installed or private repository material sent to a model provider.

## Finding

The evidence supports testing Jev as a source-selection and semantic-triage assistant. It does not establish that Jev can replace the engineering review that found our recent cross-component defects. The strongest initial experiment is now ranking relevant context from a deterministic shortlist, followed by evidence-packet triage. This revises the earlier failure-log-first preference in the [roadmap](../../superpowers/plans/2026-09-19-jev-integration-roadmap.md).

Three different savings mechanisms must be measured separately:

1. Ordinary code avoids repeated reads, extracts structured results and detects unchanged state.
2. Jev ranks or labels ambiguous text that code cannot cheaply resolve.
3. Codex reasons over the selected evidence and implements or reviews the actual change.

If Codex still performs the entire original sorting pass after Jev returns, Jev adds work. If a compact evidence packet removes repeated broad reads or a separate triage turn, there is a plausible capacity benefit. Neither outcome has yet been measured here.

## External evidence: what is established

### Official capability and limitations

TypeSafe documents `jev-1.13.0` as a versioned model ID and says responses identify the resolved version. Its current limits are 64k tokens per request and 32k for state plus the longest question. Inputs are text or structured text, not raw screenshots. Published limits are 1,200 requests/minute and 250,000 tokens/second, explicitly subject to change. Account access remains untested. [Models](https://docs.typesafe.ai/models)

The vendor's limitation register explicitly covers unreliable arithmetic/counting/date comparison, literal wording, multi-hop indirection, irrelevant context and adversarial inputs. It also warns that equivalent-looking Noul and Choice formulations need not produce equivalent probabilities. For our experiment, compute identities, ordering and counts locally; version the complete question definition; include uncertain and no-match answers. [Jev 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13)

The launch workflow evaluation uses frontier-model predictions as its reference, rather than independently established ground truth. It is evidence about performance on that evaluation, not a demonstrated coding-review defect-detection rate. [Vendor methodology](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

### Independent experiments worth using

| Evidence | Reported result | Interpretation for us |
|---|---|---|
| [Phishing benchmark](https://github.com/anisselbd/jev-phishing-bench), 2,000 emails, public harness/results | Direct verdict: Jev 62.6% accuracy, Haiku 81.3%. On the held-out half, a simple rule reached 91.8%; a fitted combination of five Jev signals reached 95.0%. The matched Haiku combination reached 93.2%, with no significant accuracy difference from Jev reported. | Broad verdicts can fail while narrower signals help. The strong rule baseline exposes dataset shortcuts. Question decomposition and scripts must receive fair comparisons. Its reported roughly 27x cost and 5x speed advantage for decomposed signals is task-specific. |
| [Reranking benchmark](https://github.com/anessbelbati/jev-rerank-bench), 1,617 scored queries across eight English datasets | Jev rubric nDCG@10 0.692, Cohere Pro 0.691; the difference interval crosses zero. Reported time was 422 ms versus 844 ms. Per-query weighting favored Cohere. | Most directly relevant evidence for context selection. Both started from the same 30 keyword-retrieved candidates. This measures ranking quality, not code understanding or completeness. Public scoring code and saved responses make the experiment more inspectable. |
| [Every's hands-on experiment](https://every.to/also-true-for-humans/mini-vibe-check-typesafe-s-jev-judged-everything-i-ve-written-in-0-7-seconds) | Across 12 synthetic passages, Jev caught six of seven planted defects; Fable caught seven. Jev repeatedly missed the same defect. | A promising cheap advisory check, with an observed recall limit. Repeating a judgment does not necessarily repair its blind spot. |
| [TrueStandard's grounding experiment](https://truestandard.ai/blog/jev-accuracy-tested), 108 claims | Reported Jev accuracy 96.3%, versus 94.4% and 93.5% for two small chat models; reported calibration errors were close. | Small, single-run, author-labeled evidence; the author's conclusion changed as the corpus expanded. The prose also contradicts the table's dollar-to-cent conversion. Do not use it to establish general superiority or precise cost savings. |

These are young, task-specific results. We inspected published methods and results, not independently reran them. Domain and prompt changes can outweigh headline model differences.

### Agent integration evidence

TypeSafe's own [skill-suggestion cookbook](https://docs.typesafe.ai/cookbooks/skill_suggestion) reports fewer wrong and needless skill loads across 488 requests. Suggestions fixed 37 covered cases and broke seven. Positive requests were generated from the skills themselves and each had one target skill. This is a useful pattern, but our multi-skill workflow and mandatory instructions are a different problem. Suggestions cannot suppress an explicitly required skill.

The [jev-eval-agent harness](https://github.com/vinilana/jev-eval-agent) compares six tasks with 100 mocked tools. Its Jev mode also reduces the language model's reasoning effort and exposes only a selected tool. Therefore a result would reflect multiple interventions; it cannot isolate Jev's contribution without additional controls. Mock tool completion is not evidence of real execution reliability.

[Firstmate](https://github.com/kunchenguid/firstmate) documents event-driven supervision and persistent coordination as separate features. Its README did not expose the video's Jev dispatch benchmark. We have not independently substantiated the video's 71%/90% dispatch figures. Avoid crediting all orchestration improvements to Jev.

## Comparison with our recent work

This is a retrospective workflow analysis, not a fresh correctness review of production code. Local review findings and acceptance states below apply to their recorded revisions and snapshots. No current PR status is inferred from an old assessment.

### 1. PR 415: related defects across repeated reviews

The [September 17 structural assessment](2026-09-17-pr415-structural-assessment.md) records 22 top-level findings in six submissions at reviewed head `bfad2f187e05980369dbf0e8f75801f621ba998d`. It groups them into recurring families and explains how local repairs left producer/consumer relationships incomplete.

**Potential Jev benefit:** Given a new review comment and a shortlist of prior findings, identify likely related findings, affected interface names and relevant contract passages. Codex would begin its related-case investigation with a focused packet.

**Limit:** Recognizing that comments belong to the same family is not discovering or proving the defect. The historical assessment needed source tracing, counterexamples and a judgment about whether the architecture could deliver the claimed guarantee. No retrieved Jev benchmark establishes that capability.

**Measurement:** Relevant-evidence recall at a fixed context budget; number of broad file reads avoided; repeated-review rounds and newly missed defects. Do not count a cluster label as a resolved finding.

### 2. S1: green tests followed by new counterexamples

The original S1 coordinator review, `recovery/full-e1-s1-coordinator-review/README.md` (local-only, not in this repo; archived in the private first-passage-archive, SHA-256 `14ca2223f920b885f67a48133b736e324702215b44fec822c4de444559ade79a`), reused 137 passing tests and still returned two substantive findings. The retained counterexample records show two failed recovery cases and one failed interface case, all capture-complete and source-stable. Those JSON fields were read directly during this research; tests were not rerun.

**Potential benefit:** Rank the handoff clauses, prior findings and source references needed for review. Flag that a return claims more than the attached test descriptions explicitly demonstrate.

**Limit:** The missing scenarios required constructing state sequences and testing interfaces. Asking Jev whether the whole assignment is complete would compress a difficult review into an unsupported verdict. Existing passing tests and high model confidence cannot establish coverage of an untested sequence.

### 3. S2-R1: separate packet validation from semantic interpretation

The [S2-R1 coordinator disposition](../../briefs/handoffs/2026-09-19-full-e1-s2-r1-review.md) reports verification of 254 packet entries and 2,076 source files. It accepts only the bounded local repair and explicitly withholds overall S2 acceptance.

The retained `recovery/full-e1-s2-r1-20260919/final-results.json` (local-only, not in this repo; archived in the private first-passage-archive, SHA-256 `8f71afce256fdd6e30b709345468825f560d9b120d882b92419a5cc0fb592e71`) has three records: 272 tests passed, 41 tests passed, and a failed standard check. Recorder durations are approximately 215.81, 71.36 and 62.48 seconds; they are not the pytest durations quoted in the return narrative. The first two records are source-stable and capture-complete, as is the failed check. These records overlap in time, so adding durations would misstate elapsed workflow time.

**Deterministic work:** Parse counts, exit status and identity; compare hashes; show which source files changed; retain the failed gate. Jev contributes nothing to exact comparisons.

**Potential Jev work:** Find sentences that appear to extend the bounded acceptance to the whole assignment, then show them alongside the actual disposition. Suggest relevant limitations to the coordinator, with sources.

**Limit:** Scope acceptance belongs to the coordinator. A model must not infer a successful live run from local test records.

### 4. PR 428 and the deadline failure: history matters

The PR 428 repair packet, `recovery/pr428-review-20260919/README.md` (local-only, not in this repo; archived in the private first-passage-archive, SHA-256 `c10c1d13b5870f45e8a00e89a14be851bf654358c3b728142198f6082bbcdba4`), records an initially failing deadline gate and a later successful check after an operator-supplied update. The earlier S2-R1 evidence still truthfully records its own failed check.

**Benefit:** A deterministic timeline keyed by run and revision prevents stale-result confusion. Jev can help match a new narrative failure to an existing incident, but only after code establishes identity and chronology. It must not rewrite an old result or close a new failure merely because a similar one was previously resolved.

### 5. Deployment handoffs: context selection over authority selection

Recent messages in **Confirm Tradeify deployment phases** distinguish preparation that could start immediately from dependent work requiring accepted interfaces. The local phase handoffs carry the resulting sequencing.

**Potential benefit:** Retrieve the exact prerequisite and return-boundary paragraphs when a task asks what can proceed. A short source packet could save repeated reading and operator explanations.

**Limit:** Determining that prerequisites are actually satisfied still needs current evidence. Jev may identify a relevant clause; it cannot grant missing authority or turn preparation into acceptance.

## Revised opportunity ranking

| Priority | Work | Best initial mechanism | Confidence in fit |
|---|---|---|---|
| First | Rank contract, handoff and related-finding passages | Keyword/index shortlist, then one Jev ranking batch | Moderate: supported by external reranking evidence; untested here |
| Alongside | Build compact evidence manifests and suppress unchanged input | Deterministic scripts and existing host events | High fit; this is not a Jev-specific benefit |
| Second | Match changed findings and flag possible scope overclaims | Bounded semantic questions with source excerpts | Plausible; needs retrospective labels |
| Third | Group genuinely ambiguous failure logs | Parser first, Jev only for the residual ambiguity | Volume/value in our work not yet established |
| Later | Suggest skills or dispatch profiles | Explicit allowed candidates and abstention | Host integration and multi-skill behavior need proof |
| Retain with current owners | Counterexample design, cross-component review, exact validation and final acceptance | Tests, deterministic validators and reasoning model | No evidence supports transferring these to Jev |

## A better first experiment

Use the actual retrospective examples above instead of generic email demonstrations. Freeze each task at the time a decision was needed: do not give a retrieval system a later solution as input. Keep later reviews only as label evidence. In particular, final S2-R1 results must not enter an earlier S1 task's candidate corpus.

Build 40 bounded queries from at least eight independent work items, covering related findings, requirement lookup, evidence-scope lookup and no-answer cases. The inspected material supplies seed cases, not eight independent completed items; collect the remaining work items before running the evaluation. Split by work item, not random paragraph, to reduce leakage. Reserve half for held-out evaluation and include at least ten hard negative or contradictory cases across the corpus. Treat this as screening evidence only.

Compare four arms on the same candidate pool and output budget:

1. Existing search/read workflow.
2. Deterministic indexing, exact extraction and keyword ranking.
3. The same shortlist reranked with pinned Jev questions.
4. The same shortlist ranked by a small generative model, if available within the approved evaluation setup.

Evaluate two levels. First, source selection: recall of necessary passages, irrelevant text included, correct abstention and stability under candidate-order changes. Second, downstream task outcome: Codex context consumed, additional reads, reasoning calls, elapsed time, operator interventions and missed findings. Keep downstream model and effort fixed while measuring the retrieval intervention.

Do not promise quota savings from tokens alone; task-level telemetry may be unavailable and account-wide usage is confounded by concurrent tasks. Label proxies as proxies. Operator minutes need prospective observation; historical chat length and run duration do not measure them.

A simple decision rule is to retain Jev only if its incremental savings over deterministic preprocessing justify its setup and maintenance, without reducing necessary-evidence recall. The roadmap's 20% usage / 25% supervision targets remain proposed adoption targets, not research findings. Our 30-case original pilot and this expanded screening design cannot establish a very low rare-failure rate.

## Effect on the earlier roadmap

- Resolve the model-version uncertainty: `jev-1.13.0` is now documented; actual account access is still unverified.
- Promote context ranking above generic log classification.
- Reuse structured verification records found in recent recovery packets; do not assume their producer is installed in this older main checkout.
- Add a matched small-model baseline and keep reasoning effort constant during comparisons.
- Separate deterministic evidence validation from semantic interpretation explicitly.
- Preserve substantive review. Our observed rework came partly from missing behavior and incomplete interface contracts, which faster text classification does not itself repair.

## Evidence limits and research verification

The main checkout remains at `c2e6eb2cbe159b60fdff7873b9e96aef943c46df`; newer work was inspected through retained packets and task history. The selected sample is weighted toward difficult qualification work and is not a census of all recent tasks. No reliable per-task Codex usage or operator-time totals were obtained, so no percentage of our actual spend is attributed to these activities.

Research used read-only web retrieval, task-history reads and PowerShell file/JSON inspection. The first JSON inspection command had a PowerShell pipeline syntax error; the corrected command succeeded. No project Python command, test suite or live Jev evaluation ran. Packet verification claims are attributed to their coordinator records; this research did not independently rehash all packet contents. External benchmark percentages are authors' reported results, with the limitations above.
