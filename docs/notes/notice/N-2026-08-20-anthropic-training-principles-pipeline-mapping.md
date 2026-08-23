# Notice — Mapping Anthropic's training-loop principles onto the strategy pipeline: 0/6 proposed mechanisms survive adversarial stress-test

**Notice ID:** N-2026-08-20-anthropic-training-principles-pipeline-mapping
**Observed:** 2026-08-20
**Author:** Joshua (commission: "think outside the box... borrow principles from how Anthropic trains its models to generate better output and apply them to First Passage in how we generate strategies" — scoped via brainstorming to the whole `generate→evaluate→deploy→measure→update` pipeline; angles selected: Constitutional AI/RLAIF, RL-from-verifiable-rewards + self-improvement, Debate/multi-agent+judge; deliverable capped at conceptual synthesis only, no build commitment) + Claude Code
**Source:** workflow `wf_882d7e37-327` (25 agents: 3 public-source research threads → 3 pipeline-mapping passes → 18 adversarial stress-test votes across 6 candidate mechanisms → 1 synthesis pass; full per-agent record in that run's `journal.jsonl`), cross-checked against direct reads of [`docs/methodology/inqhiori-canon.md`](../../methodology/inqhiori-canon.md), [`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md), [`docs/methodology/avenue_a_generate_confirm.md`](../../methodology/avenue_a_generate_confirm.md), [`N-2026-08-18-quintessentials-ml-lifecycle-mapping.md`](N-2026-08-18-quintessentials-ml-lifecycle-mapping.md), [`N-2026-08-18-iteration2-identify-notice.md`](N-2026-08-18-iteration2-identify-notice.md) (+ its closures Q-EXPR-1, Q-TRAINKILL-1/2/3), [`docs/adr/2026-08-09-grand-tier-quintessentials-binding.md`](../../adr/2026-08-09-grand-tier-quintessentials-binding.md).
**Status:** `OPEN` → routed below (primary: `DROP`; one supplementary flag for a future programme-audit)
**Addendum (2026-08-20):** the flagged programme-audit ran, same day, after a third instance (see [`N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md`](N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md)) extended the streak to 3-for-3. Verdict `DEGENERATING` — [`AUDIT-2026-08-20-external-mapping-move-class`](../audits/programme-audit/2026-08-20-external-mapping-move-class-audit.md). Guardrails (canonical, action 4, 2026-08-23): [`external_mapping_guardrails.md`](../../methodology/external_mapping_guardrails.md).
**Lives in:** `docs/notes/notice/N-2026-08-20-anthropic-training-principles-pipeline-mapping.md`

**D-S-A domain:** data (the researched-principle corpus + the pipeline's own governance corpus). This notice does not propose any meta-process/framework change — see §4 for why that exact move was tested and explicitly rejected.

---

## §0 — Source anchors

Sources read at production fidelity:
- **Files on disk (full):** the four methodology docs and two prior Notices listed above, plus their cited closures (`Q-EXPR-1-closure-resolved.md`, `Q-TRAINKILL-1-closure-ambiguous-hold.md`) and the GRAND ADR.
- **Public sources (fetched live by the research agents, not answered from pretrained knowledge):**
  - *Constitutional AI / RLAIF* — Bai et al. 2022 "Constitutional AI: Harmlessness from AI Feedback" ([arXiv:2212.08073](https://arxiv.org/abs/2212.08073), full text via ar5iv), Anthropic's [research page](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback), [Claude's new constitution](https://www.anthropic.com/news/claude-new-constitution), [Teaching Claude why](https://www.anthropic.com/research/teaching-claude-why).
  - *RLVR + self-improvement* — DeepSeek-R1 ([arXiv:2501.12948](https://arxiv.org/abs/2501.12948)), Tülu 3 ([arXiv:2411.15124](https://arxiv.org/html/2411.15124)), Anthropic's reward-hacking work ("Natural Emergent Misalignment from Reward Hacking in Production RL" [arXiv:2511.18397](https://arxiv.org/abs/2511.18397); "Sycophancy to Subterfuge" [arXiv:2406.10162](https://arxiv.org/abs/2406.10162); [Alignment Science blog](https://alignment.anthropic.com/2025/reward-hacking-ooc/)), Anthropic's [Responsible Scaling Policy updates](https://www.anthropic.com/rsp-updates).
  - *Debate / scalable oversight* — Irving, Christiano, Amodei 2018 "AI Safety via Debate" ([arXiv:1805.00899](https://arxiv.org/abs/1805.00899)), Bowman et al. 2022 "Measuring Progress on Scalable Oversight for LLMs" ([arXiv:2211.03540](https://arxiv.org/abs/2211.03540)), Khan et al. ICML 2024 "Debating with More Persuasive LLMs Leads to More Truthful Answers" ([arXiv:2402.06782](https://arxiv.org/abs/2402.06782)), [Anthropic's Fall 2023 debate progress update](https://www.alignmentforum.org/posts/QtqysYdJRenWFeWc4/anthropic-fall-2023-debate-progress-update), Buhl/Pfau/Hilton/Irving 2025 ([arXiv:2505.03989](https://arxiv.org/abs/2505.03989)).
- **User memory:** used as supplementary only (prior framing of "dry discovery channels" from an earlier session) — superseded here by the fresher, sharper `N-2026-08-18-iteration2-identify-notice.md` finding, which is the primary-source anchor for the bottleneck this exercise grounds against.
- **Tools available but unused:** none — WebSearch/WebFetch, repo grep/read, and multi-agent adversarial review were all exercised.

---

## §1 — The observation (what the mapping found, per principle)

Heavier than the canonical §0/§1 shape (a single concrete signal) — this notice reports the outcome of a completed same-session workflow, not a raw first-pass signal awaiting investigation, so the observation itself is the multi-principle mapping result. Declared here per INQHIORI's discipline of naming a deviation rather than silently drifting from template.

Each principle was researched from public sources, then mapped against the live pipeline by an agent that read the full generate→evaluate→deploy→measure→update mechanics plus two hard guardrails (see §4). All three mapping passes independently converged on the same shape of result: **real analogs already exist and are load-bearing; the genuine gaps are either things that should stay absent, or things narrow enough that only 1–2 candidate mechanisms could be honestly proposed.**

### Constitutional AI / RLAIF
*Mechanism (researched): an explicit, editable, natural-language principle set drives both self-critique-and-revise on raw generations (SL-CAI) and forced-choice AI preference labels that train a reward model (RL-CAI/RLAIF) — cheap to re-target versus a human-labeling campaign, at the cost of correlated critic/policy bias and the need for explicit confidence calibration (Anthropic's own 40–60% CoT-confidence clamp) because raw self-confidence is not evidence.*

- **Already exists, load-bearing:** INQHIORI's forbidden/permitted D-test list (`inqhiori-canon.md` §5) *is* a written constitution governing legitimate reasoning moves — the mapping calls this out explicitly as "functionally identical" to CAI's SL-stage critique pass. `strategy_harvest.md`'s five admission requirements are the same move applied to seed intake. `rejected_candidates.md` + dated lesson files are the fixed anchor/critique corpus. Programme audits are the periodic calibration eval.
- **Real but underpowered:** the INQHIORI constitution is applied by self-report at draft time, by the same agent it's meant to check, with enforcement only reactive ("audit on regret," after a deleted datum later proves to matter) — CAI's critique-then-revise pass runs proactively on every generation, this doesn't.
- **Correctly identified as absent and correctly NOT proposed:** RLAIF's actual core move — an AI preference label between two candidates training a reward/ranking model — because the pipeline's ranking function (deflated-Sharpe, cost-law, survivor-scoring) is a fixed, auditable statistical gate that must never be supplanted by an AI preference judgment.
- **Two mechanisms attempted, both killed** (see §3).

### RL from verifiable rewards + iterative self-improvement
*Mechanism (researched): replaces a learned/judged reward proxy with a deterministic, external verifier (executable test, exact-match) as the sole training signal, then closes the loop by harvesting verifier-confirmed outputs back into the next round's data — justified because gaming a hard, non-gameable verifier requires actually solving the task, where a learned reward model can be climbed independently of real success.*

- **Already exists, load-bearing:** the two-clause intake screen (Clause K deflated-Sharpe floor, Clause N confirm-power) is a hard-coded, non-negotiable check that gates every seed before any opinion is consulted — "a PASS never blesses, it only licenses further scoping" is functionally RLVR's verified-signal-gates-but-doesn't-finalize shape. Requirement 5's cost-law inequality is explicitly, in the doc's own words, "a Stage-0 arithmetic check, not a judgment call." The regime-robustness gate (both historical halves must independently clear) is the same deterministic-verifier shape. `rejected_candidates.md`'s re-proposal bar is the mirror image of RLVR's positive-harvest loop, closed for the *negative* class.
- **Real but underpowered:** the gate-reachability/bindingness audit family is the repo's actual "is the verifier itself sound" check, but runs reactively (5 prior firings, always caught post hoc) — never as a precondition on freezing a verdict-computing procedure before it runs. Q-EXPR-1's own RESOLVED finding names its downstream fix ("screen claim horizon vs. the execution envelope") but scopes it as a one-time patch to "the next slate," not standing machinery.
- **Correctly identified as absent and correctly NOT proposed:** harvesting verifier-CONFIRMED-POSITIVE outcomes back into the mining channel's frozen feature catalogue (DeepSeek-R1's actual RL loop) — flagged as sitting close to a real tension with the pipeline's pre-registration-purity discipline, and not grounded against any observed failure, so proposing it would itself have been the ungrounded move.
- **Two mechanisms attempted, both killed** (see §3).

### Debate / multi-agent generation + judge
*Mechanism (researched): a bounded judge who can't verify a compound claim directly can still reach a correct verdict if forced to adjudicate only the single most-contested branch a comparably-capable, symmetrically-incentivized opponent surfaces — but only when evidence is checkable, the opponent has genuine capability/information parity, and the judge has been hardened against known reward-hacks. Khan et al. 2024's load-bearing empirical fact: remove the live opponent and judge accuracy drops from ~70% to ~54%.*

- **Already exists, load-bearing:** pre-registration functions as the held-out set that keeps a judge from grading on data the generator already saw. K-accounting is the multiplicity scaffolding debate research treats as necessary. `fable-judge` and `pre-ratification-adversarial-panel` are the closest existing analog to debate's live-adversary requirement — already wired to ADR/closure/brief ratification.
- **Real but underpowered:** those two skills are wired to deploy-adjacent artifacts, not to harvest requirement (1)'s economic-grounding write-up, which is currently produced and scored as a single unopposed advocate case — precisely the "consultancy" structure Khan et al. showed degrades accuracy.
- **Correctly identified as absent and correctly NOT proposed:** true symmetric self-play debate (no observed failure resembles judge verbosity/positional bias); adaptively retraining the operator's own judgment heuristics (no evidence the operator has been fooled by a specific caught persuasion pattern); standalone mechanical quote-verification for harvest cohort-δ citations (folded into one candidate rather than raised as its own proposal).
- **Two mechanisms attempted, both killed** (see §3).

---

## §2 — Why this stands out (baseline / delta / frequency)

**Baseline:** three well-defined ML-training principles, mapped by a careful multi-lens process onto a pipeline that already carries real ML-training-shaped texture (pre-registration-as-holdout, K-accounting-as-multiplicity-control, INQHIORI-as-constitution, rejected-candidates-as-critique-corpus) and a sharply named, high-stakes open bottleneck (zero-ever conversion to a tradeable expression across full program history, H1/H2/H3 undiscriminated; ~15 train-kills undiscriminated null-vs-underpowered) — going in, the expectation was that at least 1–2 of 6 candidates would survive as a scoped, cheap, stage-bolted mechanism, given how much surface area for "forced discrimination" the bottleneck offers.

**Delta:** zero survived. Every candidate failed feasibility (6/6) — most because the mechanism reduced to an LLM relabeling numbers the pipeline already computes deterministically (Requirement 5's cost-law inequality, Clause N's power formula), discriminating nothing new, or targeted a bottleneck too small in sample (≈3–5 historical conversion deaths) to ever move regardless of tagging discipline. Every candidate also failed domain-conflation (6/6) — each leaked into a second or third pipeline stage despite declaring one, or duplicated existing named machinery (`gate-reachability-audit`, `pre-ratification-adversarial-panel`, `verify-source`) under imported CAI/RLVR/Debate vocabulary. 5/6 also failed evidentiary-substitution — an LLM-generated tag, power figure, or write-up was allowed to "count" toward a downstream classification without a code-enforced, independently-checkable computation behind it, with the anti-substitution language living only in each candidate's own risk-disclosure field rather than its operative logic.

**Frequency:** this is the **second** "map an external decision-quality/training framework onto this pipeline" exercise in **9 days** to land on a domain-conflation-driven DROP — after the Quintessentials mapping was routed DROP on 2026-08-09/19 for the structurally identical reason (a transportable framework belongs one tier above the pipeline, not folded into per-stage mechanics as new operators). Two DROPs on the same move-class in 9 days is itself a SNAG-pattern signal per this repo's own programme-audit trigger ("multiple null/ambiguous loops same domain") — flagged below, not resolved here.

---

## §3 — Candidate mechanisms: all 6 adversarially stress-tested, 0 survived

Not the canonical "informal, loose, not-pre-registered" §3 shape — these were formally tested inline this session rather than left as first-pass ideation for a later Pre-Q, because the whole point of the workflow was to apply adversarial rigor before anything reached this document. Every mapping pass proposed at most 2 mechanisms, each required to name one pipeline stage and ground itself against the measured bottleneck (never a generic pitch). Each candidate then went through three independent adversarial lenses — **feasibility** (does it actually engage H1/H2/H3 or the train-kill power ambiguity?), **evidentiary-substitution risk** (does an LLM output get treated as evidence?), **domain-conflation risk** (does it collide with the GRAND/Quintessentials precedent or duplicate existing machinery?). A candidate needed to clear all three to survive.

| # | Mechanism | Principle | Declared stage | Killed by | Core defect |
|---|---|---|---|---|---|
| 1 | Conversion-death cause-tag (forced-choice H1/H2/H3 triage field) | CAI/RLAIF | evaluate | feasibility + evidentiary + domain | H1/H2 are redundant relabelings of numbers the manifest already has; H3 is a claim about the search *process*, structurally unanswerable from any single candidate's data — the model can never legitimately select it. This is the literal "does this fit my model?" move INQHIORI's own forbidden-D-test list already bans, relocated and relabeled. |
| 2 | Null-vs-underpowered split gate on mining-channel kills | CAI/RLAIF | generate | feasibility + evidentiary + domain | The mining channel's actual pre-registration has no per-cell effect-size-floor field, so "the same formula, one stage earlier" needs new infrastructure, not reuse; it's prospective-only and can't resolve the already-closed 15-kill audit it targets; its own risk field concedes it opens a backdoor around the re-proposal bar. |
| 3 | Pre-registration verdict-route reachability preflight | RLVR | evaluate | feasibility + domain (evidentiary passed) | The Q-TRAINKILL-1 defect it's grounded against was realization-dependent, not design-wide-existential — the proposed check would likely have *passed* the exact table it's cited against. Duplicates the repo's own already-named gate-reachability-audit skill (5 prior firings) without reconciling why a 6th instance needs new machinery. |
| 4 | Standing horizon-reachability admission clause | RLVR | generate | feasibility + evidentiary + domain | A pure cost-avoidance move (kills doomed candidates cheaper/earlier) that doesn't increase conversion *survival* — the bottleneck record states generation supply is explicitly not what's failing. The horizon-extraction step has no citation-verification discipline in its operative logic, only promised in the risk field. |
| 5 | Adversarial admit/reject cross-examination at harvest requirement (1) | Debate | generate | feasibility + evidentiary + domain | Can't reach the population actually dying (in-house-discovered regularities enter via mining/census, not the harvest checklist this patches). Both "debaters" are the same LLM with no genuine capability/information asymmetry — Khan et al.'s own precondition for debate to beat "consultancy" is unmet by construction. |
| 6 | Adversarial atomic-power cross-examination of disputed train-kills | Debate | evaluate | feasibility + evidentiary + domain | The exact bottleneck was already closed two days prior by a more rigorous, pre-registered, code-frozen joint-likelihood scorer (Q-TRAINKILL-1/2/3) that correctly treats this as pooled inference — this candidate's per-family binary flag is strictly coarser than what already ran, and re-running a new lens over the same frozen data is precisely the re-litigation that closure explicitly barred. |

Full per-candidate adversarial reasoning (all three lenses, verbatim) is in the workflow's `journal.jsonl`, cited in §0.

---

## §4 — Routing decision

**Primary: `DROP`.** Zero of 6 candidate mechanisms survived all three adversarial lenses — every candidate failed feasibility, every candidate failed domain-conflation, and 5/6 failed evidentiary-substitution as well. The failures were not narrow implementation gaps fixable by a tweak: each mechanism either (a) reduced to an LLM relabeling of numbers already computed deterministically, (b) targeted a bottleneck too small in sample (n≈3–5 conversion deaths) to ever move, (c) leaked into a stage beyond its declared one, or (d) duplicated existing named repo machinery under imported vocabulary. There is no mechanism to graduate to a cheap pilot and no ambiguous middle ground to hold pending further design — no Pre-Q is warranted.

**Durable output kept despite the DROP — standing guardrail for any future framework-mapping exercise**, distilled from what actually killed all 6 candidates here, not restated generically:

1. **Evidentiary-substitution guardrail.** If a proposed mechanism's core action is an LLM re-prompt, tag, write-up, or debate that produces a number/label which then feeds or weighs on any existing gate (cost-law, Clause N/K, survivor-scoring, a re-proposal decision), the anti-substitution safeguard must be engineered into the mechanism's *operative logic* — not merely asserted in a risk-disclosure field — and must route through an actual, independently-runnable deterministic computation wherever one already exists (Requirement 5's cost-law inequality, Clause N's power formula), rather than having the LLM narrate or re-derive that number itself.
2. **Domain-conflation guardrail.** A mechanism's declared single pipeline stage must match its actual functional reach. If its stated purpose is to inform a decision that properly belongs to a different named stage, it's conflating altitude exactly as the GRAND/Quintessentials precedent did, one register smaller. Before proposing new machinery, check whether the repo already has a same-shaped tool under its own name (`gate-reachability-audit`, `pre-ratification-adversarial-panel`, `verify-source`) that the new proposal would otherwise silently reinvent under imported vocabulary.

Taken together: **a proposal that would survive should look almost boring in pipeline-native terms** — a one-line addition to an existing deterministic check, with zero LLM judgment anywhere in the decision path — and should be treated with default suspicion the moment it needs an LLM to discriminate between hypotheses, extract a number from a source, or argue two sides of a claim.

**Supplementary flag (not a routed action, named for a future programme-audit):** two independent framework-mapping exercises in 9 days (this one; `N-2026-08-18-quintessentials-ml-lifecycle-mapping.md`) both landed on domain-conflation-driven DROP for the same structural reason. Per this repo's own programme-audit trigger ("SNAG pattern — multiple null/ambiguous loops same domain"), a third such exercise should not be attempted on faith — if a future session is tempted to map another external framework (agile/MLOps/some other AI-safety concept) onto this pipeline, that session should read both DROPs first and treat the guardrail above as the standing bar to clear before spending any research budget, or route the question itself to a programme-audit rather than re-running the same shape of exercise a third time.

**What this Notice does not claim:** it does not claim Anthropic's training principles are irrelevant to this program in any generic sense — the mapping in §1 found the pipeline already independently reinvented several of the same underlying ideas (pre-registration, trial-count accounting, a written reasoning-constitution, a critique corpus) under its own vocabulary, arrived at for its own reasons. What it found is that no NEW mechanism, grounded against the pipeline's actual current bottleneck and surviving genuine adversarial review, was available at the surface this exercise searched.

---

## §10 — Audit hooks

```bash
# This notice does not reopen the GRAND ADR's §3 alternatives ruling
grep -rn "N-2026-08-20-anthropic-training-principles-pipeline-mapping" docs/adr/2026-08-09-grand-tier-quintessentials-binding.md
# Expected: no hit

# SNAG-pattern flag is visible to a future programme-audit pass
grep -rln "SNAG" docs/notes/notice/N-2026-08-18-quintessentials-ml-lifecycle-mapping.md docs/notes/notice/N-2026-08-20-anthropic-training-principles-pipeline-mapping.md
# Expected: both files

# Full adversarial record for all 6 candidates is retrievable
python -c "import json; [print(json.loads(l).get('label')) for l in open(r'C:/Users/joshu/.claude/projects/C--Users-joshu-multi-firm-operations--claude-worktrees-n-2026-08-18-iteration2-eabe96/b4320485-0ef0-46bd-a48f-e78bfd3e1e4f/subagents/workflows/wf_882d7e37-327/journal.jsonl') if 'label' in json.loads(l)]" 2>/dev/null || echo "journal path is session-local; see Source line for the run id if relocated"
```

---

## Verification

```bash
$ python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/notes/notice/N-2026-08-20-anthropic-training-principles-pipeline-mapping.md --type notice
# Expected: §0 source / §1 observation / §2 baseline+delta / routing decision all present
```
