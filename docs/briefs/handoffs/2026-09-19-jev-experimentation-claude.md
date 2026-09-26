# Jev experimentation handoff to Claude

Prepared September 19, 2026. The user is moving this investigation from Codex to Claude. Both completed experiments and their evidence are retained locally. No further inference or integration is currently running.

## Start here

**User objective:** Reduce frontier-agent usage limits and the user's time supervising development tasks. API dollars are secondary. The original inspiration was [this Jev/Astra video](https://www.youtube.com/watch?v=2XFXe-oGnrI).

**Current judgment:** Jev is promising for selecting relevant evidence before a reasoning agent reads it. We have not demonstrated actual Codex/Claude quota savings, reduced supervision, better code review, or faster task completion. Improve ordinary keyword retrieval before attributing savings to Jev. Keep substantive engineering reasoning with the main agent and exact checks with deterministic code.

**Most important qualification:** Jev passed our second experiment against its frozen baseline, but a subsequent local check recovered most of its unique advantage simply by indexing document headings and paths. Do not report “65% lower Codex usage” or “Jev replaced engineering review.” Neither was measured.

Repository: `C:/Users/joshu/multi_firm_operations`.

## What we researched

Read the existing research note rather than repeat broad discovery:

- [Research and fit to recent work](../../notes/audits/2026-09-19-jev-research-workflow-fit.md).
- [Integration roadmap and dated experiment updates](../../superpowers/plans/2026-09-19-jev-integration-roadmap.md).

The video described substantial dispatch savings, but we did not independently substantiate its headline 71%/90% figures. Published reranking work was more directly relevant than routing demos to our actual workflow. Other reviewed evaluations showed that task decomposition and a strong deterministic baseline can matter more than the model's headline accuracy. These were inspected reports, not replications.

Recent workflow examples motivating the investigation:

- PR415's retained structural assessment grouped 22 top-level findings across six review submissions into recurring defect families. Retrieval could surface related findings and governing clauses; recognizing a family is not finding or proving a defect.
- An S1 coordinator review reused 137 passing tests yet produced three failing counterexamples. Good test results and a clean evidence packet did not replace substantive review.
- S2-R1's local review accepted a bounded repair while overall S2 remained incomplete and S3 blocked. Its record reconciled source inventories and distinguished passing focused tests from a failed standard gate. Much of this verification is deterministic hash/count/status work, not a job for Jev.

These are historical observations at recorded revisions, not claims about today's active tasks or production state. Do not act on old operational statuses as if current.

## Experiment 1: small retrieval screen

Directory: `recovery/jev-retrieval-pilot-20260919/`.

Full report: `recovery/jev-retrieval-pilot-20260919/RESULTS.md` (local-only, not in this repo; archived in the private first-passage-archive, SHA-256 `c13c1c598a0708535e2996416079d63077a3e7de5697e217c8fb879e22b67ef8`).

- 24 short sanitized/adapted workflow passages; 10 answerable queries and 2 unanswerable queries.
- Same BM25 top-12 shortlist for both arms. Jev assigned per-passage relevance scores. Three queries also reversed candidate order.
- Frozen prediction: at least 20% fewer characters read through the last required passage, no loss in complete evidence coverage at top 3, and abstain on both absent answers.
- Baseline and Jev both had complete evidence at top 3 on 10/10 answerable queries.
- Characters fell from 2,901 to 2,715: **6.41%**, below the target. Jev correctly abstained on 2/2 absent answers; the simple baseline did not. No coverage losses in the three order reversals.
- 16 requests, $0.001614186 reported spend, median evaluation round trip about 0.349 seconds.

**Critical design lesson:** After computing the frozen baseline but before evaluation, we discovered that even oracle ranking could save only 6.41%. Jev achieved that minimum, but the 20% prediction was mathematically impossible on this corpus. We disclosed this and did not change the target. This falsifies the prediction for that corpus; it does not establish that Jev cannot help harder retrieval. The abstention comparison was weak and too small to establish reliability.

Four offline evaluation tests passed. No actual downstream reader or frontier-agent usage was measured.

## Experiment 2: paired evidence retrieval and reading

Directory: `recovery/jev-paired-retrieval-20260919/`.

Full report `recovery/jev-paired-retrieval-20260919/RESULTS.md` (SHA-256 `4a5909001eb43f4c83c4530df362c31d00f191af82c738807b9fa5cd0000f2bc`), protocol `recovery/jev-paired-retrieval-20260919/PROTOCOL.md` (SHA-256 `320717d62747d5bcfd18bc76307067e7046319dda75d94aff8eed5e67b5488c3`), results JSON `recovery/jev-paired-retrieval-20260919/results.json` (SHA-256 `fdbc2d3af2d2a692e6d509bb7df4e1704ea489a966904c95173d6355e83d8ade`). These packet files are local-only, not in this repo; each is archived in the private first-passage-archive under its SHA-256.

64 excerpts split from six existing development-workflow documents, with personal path prefixes and long hashes redacted and selected implementation-detail sections removed. Eight author-selected retrospective tasks, each with two factual subquestions. This was more realistic than pilot 1 but still not a prospective/random sample of live user queries.

Three arms shared a BM25 top-12 shortlist:

1. Broad keyword: all 12 passages.
2. Compact keyword: first 4 passages.
3. Jev: rerank the same 12, return first 4.

The same `openai/gpt-4.1-mini` reader answered from each packet through OpenRouter, temperature 0, JSON output, maximum 600 output tokens, no tools. Subquestions used four fixed choices plus UNKNOWN. Scoring required the correct option and at least one accepted supporting citation present in the packet. Labels and alternative support passages were fixed before inference and not sent to the models. Extra citations were not individually scored for precision.

Frozen success criteria: at least 30% less actual reader input than broad retrieval; preserve its supported-answer and complete-task counts with no case regression; at least two more complete tasks than compact retrieval; no increase in unsupported selections.

| Measure | Broad keyword | Compact keyword | Jev + reader |
|---|---:|---:|---:|
| Actual reader prompt tokens | 29,819 | 10,669 | 10,431 |
| Facts present / supported-correct answers | 16/16 | 13/16 | 16/16 |
| Fully supported tasks | 8/8 | 5/8 | 8/8 |
| Correct options, ignoring citations | 16/16 | 16/16 | 16/16 |
| Median HTTP time, ranking included | 1.464 s | 1.346 s | 1.887 s |
| Reported arm cost, ranking included | $0.0123116 | $0.0050260 | $0.0068505 |

**Outcome:** All four criteria survived after the disclosed technical recovery below. Reader input fell **65.02%** and reported treatment cost fell **44.36%** versus broad reading. Median time increased **0.423 seconds (28.9%)**. There was no speed win.

Jev recovered evidence about the reason for historical test skips, the detached-baseline instruction, and the named acceptance-evidence owner. The compact reader still guessed every expected option despite missing three supporting facts. Choice accuracy alone would have concealed that loss of grounding.

Ranking itself processed 45,403 input tokens. Adding its 10,431 reader tokens gives **55,834 total treatment input tokens**, more than broad reading's 29,819. The mechanism is shifting work to a cheaper model and reducing frontier-reader context, not reducing all-model token processing.

Five focused offline tests passed after expected initial failures. No project production code or dependencies changed; full project suites were not run for these standalone experiments.

### Provider interruption and approved recovery

OpenRouter rejected one reader request with HTTP 402, reason `in_flight_budget_exhausted`, advising Retry-After 120 seconds. This was an outstanding credit-reservation limit, not a model error and not proof that a permanent top-up was required.

The frozen runner stopped without retry. After backoff, the remaining unattempted calls succeeded. Because the failed attempt consumed the original 32-attempt cap, the user explicitly approved one unchanged replay, increasing the cap to 33 while keeping the $0.10 budget. The exact request-body hash was verified; no successful output was rerun. All comparisons then completed.

Total: **33 attempts, 32 successful responses, $0.024188126 reported charges** (about 2.42 cents). The rejected attempt supplied no usage; its conservative reservation remains retained. Original incomplete results, original ledger/failure, recovery amendment and one-shot recovery receipt are all preserved. The extra wait and approval are real operational overhead, excluded from the per-inference latency table. Human supervision time was not measured.

### Stronger deterministic baseline: the main unresolved comparison

After the frozen comparison, we noticed that BM25 indexed only passage bodies while Jev also saw source paths and headings. An explicitly **post hoc, local-only** check indexed those metadata fields too.

- Metadata-aware BM25 top 4 contained **15/16 required facts and complete evidence for 7/8 tasks**.
- It recovered two of the three gaps without Jev. Only the acceptance-owner fact in q06 remained missing.
- This was a retrieval-coverage check, **not a fourth reader arm**: no additional reader responses, measured reader tokens, costs or timings.
- It does not change the frozen pass, but narrows the observed unique coverage benefit to **one fact / one task**. Use this stronger control in the next experiment.

See `exploratory-metadata-keyword.json`. Also, q05's strict label requires explicit detachment; accepting its looser separate-worktree citations would improve the original compact score to 6/8, still below Jev's 8/8. Frozen labels were not revised after seeing outputs.

## What we could still learn, in priority order

1. **Does Jev beat well-configured cheap retrieval on fresh work?** Use source/title/body indexing, reasonable query construction and equal candidate/packet budgets. Capture naturally occurring requests before selecting answers. Use held-out tasks rather than retuning on the eight existing cases. Separate ordinary cases, ambiguous wording, conflicting/stale sources and missing-answer cases; report how each stratum was sampled. Check oracle headroom before spending money, without discarding easy cases just to manufacture a gain.

2. **Does it save actual frontier-agent usage per accepted task?** Run comparable Claude or Codex workflows with and without reranking, holding the agent model, effort, tools and completion criteria fixed. Measure input/output/cache/reasoning usage when available, all tool-result context, source rereads, retries, corrections, elapsed time and human interventions. Include wrapper overhead and lost caching. Do not convert API-reader token percentages into subscription quota percentages. A real tool should return the compact evidence packet rather than make the main agent first read the whole Jev input/output.

3. **Does the evidence survive free-form reasoning?** Replace answer-choice clues with source-grounded free responses or a bounded actual development/review deliverable. Label required facts independently where practical; evaluate citation precision as well as presence of one accepted citation. Count omissions and plausible unsupported claims, and preserve access to omitted original sources. Unknown-answer and conflicting-version cases need their own measured policy; a relevance score is not authority or proof.

4. **Can selective use outperform always-on reranking?** A cheap rule might route only genuinely ambiguous shortlists to Jev. Calibrate any trigger on development cases and evaluate it on separate cases. Compare with simple metadata/query/chunking improvements, caching, deduplication and, only if needed, another reranker. Do not add several interventions at once and credit all gains to Jev.

5. **Will service handling reduce supervision rather than create it?** Predeclare a total attempt budget that includes bounded retries, honor Retry-After, preserve unresolved cost reservations and request identities, avoid replaying successes, and distinguish timeout/unknown completion from explicit rejection. Test these paths locally. Our one extra approval was experiment overhead, not evidence of a supervision benefit.

Only after retrieval earns its place should a separate study consider review-comment clustering, evidence-packet triage or task routing. There is no evidence here that Jev can replace cross-component engineering review. Compute hashes, timestamps, counts, budget arithmetic and exact schema checks in code.

## Suggested next bounded handoff (proposal, not an already-run experiment)

**Selected outcome:** A preregistered held-out comparison of metadata-aware keyword retrieval versus Jev on fresh evidence tasks, with an end-to-end reader/agent measure and a decision about whether any integration is warranted.

**Prerequisites:** Read the two reports and existing code; choose Claude API, Claude Code, Codex or another reader explicitly based on the intended deployment; verify what usage is actually observable. Establish the next data-transfer and spend scope. Prior approvals below were specific experiments, not standing permission for arbitrary uploads.

**Ownership:** Claude is the experiment coordinator and retains combined acceptance. Delegation is optional only when authorized by the user's current environment/instructions.

**Verification:** Freeze tasks, labels, source snapshots, candidate construction, prompts, success/failure thresholds and spend/retry budget before evaluation. Keep strong baseline and treatment matched. Assess quality before claiming savings. Report every case, service failure and protocol deviation. Derive a meaningful minimum effect from expected workload and integration costs rather than copying 20%/30% mechanically.

**Checkpoint:** Show baseline quality, possible improvement and observable usage metrics before live calls. Report the final decision with artifacts and uncertainties; no result-based case replacement.

**Return boundary:** Stop at one interpretable experiment result. No automatic hooks, default agent/model routing, production deployment or new paid services follow merely because a small benchmark passes.

## Environment and artifacts

Installed official TypeSafe skill: `C:/Users/joshu/.codex/skills/typesafe-ai/SKILL.md`, from [typesafe-ai/skills](https://github.com/typesafe-ai/skills), subpath `skills/typesafe-ai`. It is installed for **Codex**, not automatically for Claude. Claude can read the file directly; installation into Claude's own skill configuration was not performed. No local Jev weights, SDK, MCP server or hooks were installed.

The existing process had `OPENROUTER_API_KEY`; `TYPESAFE_API_KEY` was absent. Never print credentials. A new Claude process may not inherit the same environment—verify availability without exposing values. The tested endpoints were:

- Jev: `https://openrouter.ai/api/alpha/decisions`, requested `typesafe/jev-1.13`, resolved `typesafe/jev-1.13-20260917`.
- Reader: `https://openrouter.ai/api/v1/chat/completions`, `openai/gpt-4.1-mini`.
- Current TypeSafe guidance: [documentation index](https://docs.typesafe.ai/llms.txt), [reranking cookbook](https://docs.typesafe.ai/cookbooks/rerank_typesafe), [Score primitive](https://docs.typesafe.ai/primitives/score). Recheck live API/model docs before new integration work.

Existing isolated checkout: `C:/Users/joshu/.codex/worktrees/jev-retrieval-pilot/multi_firm_operations`, tested HEAD `c2e6eb2cbe159b60fdff7873b9e96aef943c46df`. Durable experiment artifacts are in the main workspace, not that disposable checkout. Recheck current status; other development tasks are active, and the main checkout contains unrelated work.

Project Python must follow AGENTS.md: run the selected checkout's `./fp.ps1 doctor`, then use its `./fp.ps1 python ...`. Verified interpreter: `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, Python 3.13.2, 62 matching locked distributions. No dependency installation was needed.

Important paired-experiment files:

- `corpus.json`, `tasks.json`, `source-manifest.json`: passages, labels, provenance.
- `PROTOCOL.md`, `LABEL_REVIEW.md`, `frozen.json`: prior commitments and identities.
- `experiment.py`, `test_experiment.py`, `snapshot.ps1`: implementation and checks. The runner imports helpers from the first pilot, so retain both directories together.
- `request-*.json`, `response-*.json`, `ledger.json`: exact submitted bodies and retained responses/costs. The frozen helper contains no API key.
- `results.json`, `results-original-incomplete.json`, `RESULTS.md`: final and interrupted findings.
- `RECOVERY.md`, `retry_once.py`, `recovery-attempt.json`: exhausted, explicitly approved one-shot recovery. Do not invoke it again.
- `exploratory-metadata-keyword.json`: local-only stronger baseline check.

Safe offline reproduction, from the isolated checkout:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python C:/Users/joshu/multi_firm_operations/recovery/jev-paired-retrieval-20260919/test_experiment.py
.\fp.ps1 python C:/Users/joshu/multi_firm_operations/recovery/jev-paired-retrieval-20260919/experiment.py analyze
```

`analyze` uses saved responses and makes no API calls; it rewrites the derived results JSON. Do not edit frozen experiment inputs, clear ledgers or rerun paid modes to “reproduce” an already-retained result. Start a new directory/protocol for a new experiment.

The user explicitly approved each existing sanitized corpus and its named recipients, and the one recovery replay. These approvals have been fulfilled. This handoff does not move credentials, configure Claude, or authorize an unlimited continuation budget. No commit, push, PR, production configuration or default Jev integration was made.
