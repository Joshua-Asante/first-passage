# Jev experimentation — disposition and preserved evidence (2026-09-19)

Dispatch: continue the Jev (TypeSafe reranking) investigation from its retained evidence and
prioritise testing Jev against metadata-aware keyword retrieval on fresh tasks, measuring
actual agent usage and supervision.

**Disposition: NOT EXECUTED — blocked on environment and on authority.** Nothing was
measured, installed, configured or spent. This note exists because the dispatch also asked
that the completed experiments and their limitations be preserved, and the only durable copy
was the handoff prose itself.

## Why the experiment did not run here

**Environment.** The dispatch's evidence lives in a different workspace
(`C:/Users/joshu/multi_firm_operations`, Windows). None of it is reachable from this clone:
`recovery/jev-retrieval-pilot-20260919/`, `recovery/jev-paired-retrieval-20260919/`, the
research note and the integration roadmap are absent from the working tree, from every branch,
and from history (`git log --all` finds no path matching `*jev*`). The session repository is
`Joshua-Asante/first-passage`, and GitHub scope is limited to it.

The paid arms are independently blocked: `OPENROUTER_API_KEY` and `TYPESAFE_API_KEY` are both
absent from this process, and the environment's network policy refuses `CONNECT` to
`openrouter.ai:443` and `docs.typesafe.ai:443` (gateway 403). No reranking or reader call
could have been made regardless of approval.

**Authority.** Repo-local retrieval is not new ground here, and the ground is closed.
[Q-XMEM-1](../Q-XMEM-1-cross-surface-memory-sidecar-pilot.md) is `CLOSED — SUBTRACT`
(2026-08-19); re-entry requires "a genuine dated cross-surface-memory-invisibility incident,"
which an external handoff about another repository does not supply. Limb C — the local-embedder
vector limb, the closest existing analogue to bolting a reranker onto
[`scripts/repo_retrieve.py`](../../../scripts/repo_retrieve.py) — is recorded as a "live
question, **not authorized**," gated behind a Rule 2 cost dry-run and an operator-paced
decision. Starting a Jev-vs-keyword comparison in this repo would reopen both without the
named trigger.

## Preserved: the two completed experiments

Reported by the originating investigation; **not verified here** — the artifacts are
unreachable from this clone, so every figure below is a retained claim, not a checked one.

**Experiment 1 — small retrieval screen** (24 passages, 10 answerable + 2 unanswerable
queries, shared BM25 top-12). Frozen prediction: ≥20% fewer characters read, no coverage loss
at top 3, abstain on both absent answers. Outcome: baseline and Jev both had complete evidence
at top 3 on 10/10; characters fell 2,901 → 2,715 = **6.41%**, below target; Jev abstained
2/2, the simple baseline did not. 16 requests, $0.001614186, median round trip ~0.349 s.
**Limitation, as disclosed:** after the baseline was computed but before evaluation, even
*oracle* ranking was found to cap at 6.41% on that corpus — the 20% target was mathematically
impossible. The target was not changed. This falsifies the prediction for that corpus only; it
does not show Jev cannot help harder retrieval. The abstention comparison was too small to
establish reliability.

**Experiment 2 — paired evidence retrieval and reading** (64 excerpts from six documents,
8 author-selected retrospective tasks × 2 subquestions; three arms over a shared BM25 top-12;
`openai/gpt-4.1-mini` reader, temperature 0).

| Measure | Broad keyword | Compact keyword | Jev + reader |
|---|---:|---:|---:|
| Reader prompt tokens | 29,819 | 10,669 | 10,431 |
| Supported-correct answers | 16/16 | 13/16 | 16/16 |
| Fully supported tasks | 8/8 | 5/8 | 8/8 |
| Correct options, ignoring citations | 16/16 | 16/16 | 16/16 |
| Median HTTP time (ranking included) | 1.464 s | 1.346 s | 1.887 s |
| Reported arm cost | $0.0123116 | $0.0050260 | $0.0068505 |

All four frozen criteria survived: reader input fell **65.02%**, reported treatment cost fell
**44.36%** versus broad reading. Median time rose **0.423 s (28.9%)** — no speed win.

**Limitations, as disclosed and to be kept attached to those numbers:**

- Ranking itself processed 45,403 input tokens. With the reader's 10,431 that is **55,834
  total treatment input tokens vs broad reading's 29,819**. The mechanism shifts work to a
  cheaper model and shrinks frontier-reader context; it does not reduce all-model tokens.
- A **post hoc, local-only** stronger control — BM25 indexing source paths and headings, not
  just bodies — recovered **15/16 facts and 7/8 tasks** in its top 4, taking two of Jev's three
  unique gaps. Observed unique benefit narrows to **one fact / one task**. That check ran no
  reader, so it has no token, cost or latency figures.
- Tasks were author-selected retrospectively, not a prospective sample of live queries; choice
  accuracy alone (16/16 everywhere) concealed the compact arm's loss of grounding.
- One reader request was rejected `HTTP 402 in_flight_budget_exhausted`; after backoff, one
  explicitly approved unchanged replay completed the run (33 attempts, 32 successes,
  $0.024188126). The extra wait and approval were real operator overhead, excluded from the
  latency table. **Human supervision time was never measured.**
- No downstream frontier-agent usage was measured in either experiment.

**Not established, and not to be reported as established:** Codex/Claude quota savings,
reduced supervision, better code review, faster completion, or "Jev replaced engineering
review." The video's headline 71%/90% figures were never independently substantiated.

## What this repo offers if the question is ever reopened

Recorded as an observation for the operator, **not** a proposal and **not** authority to act.

First Passage already holds the control the investigation says it lacks.
[`scripts/repo_retrieve.py`](../../../scripts/repo_retrieve.py) is metadata-aware FTS5 over
paths, headings and bodies, and it was measured against a *frozen, rule-constructed* fixture
rather than author-selected tasks —
[v3 RESULTS](../../../lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md):
`R_shipped@5 = 0.500`, incumbent `R_rg@5 = 0.088`, reachability ceiling `0.735`. That ceiling
is the oracle-headroom pre-check experiment 1 lacked, and the residual 0.500→0.735 gap is
explicitly diagnosed there as a **ranking-quality** problem, not a corpus-coverage one — the
category a reranker addresses.

Two things would have to be settled first, neither of them an agent's call: the Q-XMEM-1 /
Limb C authority above, and the fact that the v3 verdict is currently detached from the
shipped blob ([audit](../../notes/audits/2026-09-19-limb-b-measured-shipped-drift.md)) — a
baseline whose own number does not attach to the deployed artifact cannot anchor a comparison.

Prerequisites beyond those: credentials and network egress this environment does not have; a
fresh data-transfer and spend scope (prior approvals were spent on specific corpora and one
replay, and this repo is public — see the public-clone posture in `CLAUDE.md`); and held-out
tasks with labels frozen before evaluation.

**This note authorises nothing** — no integration, no hook, no default routing, no paid
service, no re-entry to Q-XMEM-1.
