# Where wall-clock actually goes, and the oracle ceiling on reranking

Research date: 2026-09-21. Read-only. Repository HEAD `abb3914`, `scripts/repo_retrieve.py` blob
`a6fc6ba4e4e25d1a62d68256d2b0fe37543f2f14`. No indexed code was edited, no frozen verdict revised, no
Jev or reader inference run, no credential used, no byte sent to a model provider.

Operator framing for this pass (2026-09-21): judge **the cost problem, with Jev as one candidate**, against
**wall-clock time per accepted task**, staying **read-only exploratory** on the frozen Limb B surface, and
produce an **offline decisive analysis plus a pre-registered design** for any later live arm. That reframes
the question the [2026-09-19 research note](2026-09-19-jev-research-workflow-fit.md) and the
[Claude handoff](../../briefs/handoffs/2026-09-19-jev-experimentation-claude.md) left open — both of which
optimised for frontier-agent quota, with wall-clock explicitly unmeasured.

Read in full: the two prior Jev experiment reports and the integration roadmap; the frozen
[v3 pre-registration](../../briefs/pre-registration/2026-08-15-fts5-delete-falsifier-prereg-v3.md) and the
[Limb B RESULTS](../../../lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md); `scripts/repo_retrieve.py`
(313 lines); `scripts/gate_fire_log.py`; `.github/workflows/tests.yml`; `tests/ops/test_qualification_isolation.py`;
`AGENTS.md`; the `s2-linux-run` skill. Measured here: 100 most-recent GitHub Actions runs (the repo has 11,070),
40 `qualification-s2-supervision` runs, and one new offline retrieval probe.

## Verdict

**Reranking — Jev or any other — is the wrong instrument for wall-clock time per accepted task in this
repository, by roughly three orders of magnitude.** The pacing item is a **25.9-minute median CI critical path
per pushed commit**; the measured effect of Jev reranking in our own experiment 2 was **+0.42 s per query**
(28.9% slower). Even a reranker that were instantaneous and perfect could not reach the quantity that sets
task latency here.

Two secondary findings are more actionable than the Jev question itself:

1. **`repo_retrieve.py` indexes 17.8% of the text of the very files it claims to cover** (8.68% of the repo's
   markdown), because ten of its twelve corpus sources truncate each file to its first 20–24 lines. This is a
   deterministic, zero-latency, zero-token defect that caps every downstream consumer — including any future
   reranker. It is the concrete form of the prior research's own instruction to *improve ordinary keyword
   retrieval before attributing savings to Jev*.
2. **53.6% of S2 supervision CI wall-clock produced no accepted evidence** (failures and mid-run cancellations),
   and the single largest item on the critical path — an 18–25 minute qualification child inside the ordinary
   `Tests` job — is invoked with `-n 0`, i.e. deliberately serial.

The Jev investigation is not refuted; it is **out of scope for the chosen metric**. Its remaining live claim is
about *context volume*, not *speed*, and that claim now has a measured ceiling (below) that should be checked
before any further spend.

## 1. Where wall-clock actually goes (measured)

Source: GitHub Actions REST via the 100 most recent runs (window 2026-09-20 → 2026-09-21) and 40
`qualification-s2-supervision` runs. Duration = `run_started_at` → `updated_at`, which includes queueing and
artifact upload. This is a **two-day snapshot, not a census** of 11,070 runs.

Summing durations overstates latency, because a push fires several workflows in parallel. The honest quantity
is the **critical path per pushed commit** — the longest workflow on that SHA, which is what anything waiting
on green actually waits for.

| Quantity | Value |
|---|---:|
| Commits observed | 29 |
| **Critical path per push — median** | **25.9 min** |
| Critical path per push — mean / max | 21.0 min / 43.2 min |
| Sum of critical paths over two days | 10.1 h |
| Total CI wall-clock over the same 100 runs | 18.5 h |

Per workflow, over those 100 runs:

| Workflow | n | median | total | wasted (fail+cancel) |
|---|---:|---:|---:|---:|
| Tests | 13 | 31.9 m | 405.1 m | 0.0% |
| Qualification execution boundary | 21 | 12.5 m | 262.7 m | 0.0% |
| Qualification S2 supervision | 12 | 25.9 m | 246.9 m | **53.6%** |
| Pylint | 13 | 9.7 m | 120.4 m | 0.0% |
| c1 image validation | 11 | 4.2 m | 47.9 m | 0.0% |

`Tests` — not the S2 workflow — is the critical path on most pushes, including on S2 branches where both run.
Its own comment names why: `tests/ops/test_qualification_isolation.py` spawns a child pytest run described in
the workflow as "the 18-25 min child", invoked with **`-n 0`** (no xdist parallelism) on
`tests/ops/qualification` plus `test_phase3_provenance_acceptance.py`. That child fires on **every PR touching
a non-markdown path**.

Over the wider 40-run S2 sample: 792.4 minutes total (13.2 h), of which **440.4 minutes (55.6%) were failures
or cancellations**. The cancellations are the failure mode the `s2-linux-run` skill already documents — a push
to a branch with a run in flight kills it via per-ref `cancel-in-progress`.

**Comparison on the chosen metric.** One CI cycle = 1,554 s median. Jev reranking as we measured it =
**+0.42 s per query**. The intervention is ~3,700× smaller than the pacing item and points the wrong way.

## 2. The oracle ceiling on reranking (new offline probe, zero spend)

Retained at [`2026-09-21-rerank-headroom-probe/`](2026-09-21-rerank-headroom-probe/) (`probe.py`,
`results.json`). Reproduce with
`python docs/notes/audits/2026-09-21-rerank-headroom-probe/probe.py`. It calls the shipped
`repo_retrieve.rebuild()`/`query()` directly and reimplements no retrieval.

**This is not a Run C.** The v3 registration's one-revision cap and its `ASSISTIVE-ONLY` verdict stand
untouched; nothing here revises them, and `scripts/repo_retrieve.py` was not edited.

The argument the probe rests on: **a reranker can only reorder what first-stage retrieval already returned.**
So `recall@N` of the shipped engine *is* the oracle ceiling for a perfect reranker given shortlist depth `N`.
If that curve is flat, reranking cannot help at any price or latency.

**Fixture caveat, load-bearing.** The byte-identical v2/v3 harness is archived outside this clone
(`lab/ARCHIVED.json` → `first-passage-archive`), and retrieving it was not permitted in this session. The
fixture is therefore **reconstructed** from the pre-registration's written six-step rule: 87 surviving pairs
from 99 `## ` entries, against the frozen run's 34. It sits at a **harsher operating point** (R@5 = 0.218 vs the
frozen 0.500) and its absolute numbers are **not comparable to the frozen result**. The finding is the curve's
*shape*, read against this probe's own R@5.

Isolating ranking from corpus coverage — restricted to the 52/87 pairs whose target is in the corpus at all:

| Shortlist depth | Recall (reachable-only) | Oracle gain vs depth 5 | Rerank input tokens/query | Fits one Jev request (64k)? |
|---:|---:|---:|---:|:--|
| 5 | 0.365 | — | 3,054 | yes |
| **12** *(depth our experiments used)* | **0.500** | **+0.135** | 7,331 | yes |
| 20 | 0.500 | +0.135 | 12,218 | yes |
| 50 | 0.615 | +0.250 | 30,546 | yes |
| 100 | 0.731 | +0.365 | 61,092 | **at the limit** |
| 593 *(whole corpus)* | 0.942 | +0.577 | 362,276 | **no — 5.7× over** |

Three things follow.

- **Real ranking headroom exists.** The first stage does eventually surface almost everything reachable
  (0.942 at full depth) but ranks it badly. This **corroborates** the Limb B RESULTS' hypothesis that the
  residual gap is ranking quality rather than coverage — on the reachable subset.
- **Jev's own published request limit caps that headroom.** 64k tokens per request puts the maximum
  single-request shortlist at roughly depth 100. The configuration that would capture most of the ceiling
  (whole-corpus reranking) does not fit in one Jev request and would cost ~362k input tokens per query.
- **At the depth the prior experiments actually ran (12 candidates), the oracle gain is +0.135** — and a real
  reranker achieves strictly less than oracle. That is the honest upper bound on experiment 2's mechanism
  applied to this repository's own retrieval surface.

Across all 87 pairs (coverage *and* ranking), reachability is **0.598** and **43.7% of targets are never
retrieved at any depth ≤ 1000** — invisible to first-stage retrieval, therefore invisible to any reranker.

## 3. The root cause, and the free fix that dominates

`collect_chunks()` truncates: `header_lines` mode keeps only each file's first 20–24 lines.

| Corpus source | Mode | Indexed / full text |
|---|---|---:|
| `docs/briefs/programs/*.md` | header_lines(24) | **4.9%** |
| `docs/notes/audits/**/*.md` | header_lines(24) | 10.3% |
| `docs/adr/*.md` | header_lines(24) | 13.7% |
| `docs/methodology/*.md` | header_lines(24) | 14.8% |
| `docs/SESSIONS.md` | heading_h2(24) | 15.1% |
| `docs/briefs/*.md`, `docs/spec/*.md` | header_lines(24) | 15.8% |
| `docs/briefs/closures/*.md` | header_lines(20) | 20.3% |
| **Whole corpus** | | **17.8%** (8.68% of repo markdown) |

This explains the result the Limb B RESULTS reported as counter-intuitive and declined to explain under its
no-further-investigation rule: the August widening **added files but not bodies**, so the reachability ceiling
rose (0.676 → 0.735) while realized recall did not move at all. The answers live in prose below line 24.

Un-truncating is deterministic, costs **zero tokens and zero latency per query**, and raises the ceiling for
every consumer — including any reranker later placed on top. On the ordering the prior research itself
demanded, this is the intervention that must be tried and measured *before* Jev is priced again.

It is, however, a change to `collect_chunks()` — the exact category the v3 "Measured = shipped" clause voids on
edit, and the one-revision cap forbids under that registration. **It needs a fresh v4 registration, which this
note does not open and did not request.**

## 4. What this means for the Jev question

- **On speed (the chosen metric): no.** Not close, and the sign is wrong.
- **On context volume: still open, now bounded.** The ceiling above is the number to beat, and the
  untruncated-corpus control must exist before the comparison means anything.
- **The strongest prior evidence remains the negative control.** Experiment 2's post-hoc metadata-aware BM25
  recovered 15/16 facts and 7/8 tasks unaided, narrowing Jev's unique benefit to one fact on one task. This
  note's §3 says that control was never run at full strength, because the corpus it would index is 82% discarded.

## 5. Pre-registered design, if a live arm is ever authorized

Not authorized by this note. Recorded so a later session cannot tune it after seeing a result.

- **Question.** Does a reranker over an *untruncated* `repo_retrieve` corpus improve recall@5 enough to change
  an agent's read set, versus the untruncated deterministic baseline alone?
- **Arms, on one frozen fixture and one shortlist depth.** (a) truncated corpus, current ranking *(the shipped
  control)*; (b) untruncated corpus, current ranking; (c) untruncated corpus + reranked to top 5.
- **Freeze before inference:** fixture and labels, corpus snapshot hash, shortlist depth, prompts, spend cap,
  attempt budget including retries, and the decision thresholds.
- **Primary outcome:** recall@5. **Secondary:** added latency per query, measured, and reported even if negative.
- **Minimum effect.** Arm (c) must beat arm (b) — not arm (a). A gain over the truncated control is not
  evidence about Jev; it is evidence about truncation. Derive the threshold from expected workload, not by
  copying 20%/30% from the earlier registrations.
- **Falsifier.** If arm (b) alone reaches the target, the reranker is not adopted regardless of arm (c).
- **Order of operations.** Land and measure (b) under a fresh v4 registration first. Arm (c) needs network
  egress to `openrouter.ai` / `api.typesafe.ai` and a credential, none of which exist in this environment.

## 6. Limits, and what was not measured

- **No Jev inference ran.** `openrouter.ai:443`, `api.typesafe.ai:443` and `docs.typesafe.ai:443` all return
  403 on CONNECT through this environment's proxy; `OPENROUTER_API_KEY` and `TYPESAFE_API_KEY` are unset.
  Every Jev performance figure cited here is a **retained claim from the September 19 reports**, not verified
  in this session.
- **The probe's fixture is a reconstruction**, not the frozen harness, and its absolute recall is not
  comparable to the frozen 0.500. Treated as exploratory throughout.
- **The CI sample is two days of the most recent 100 runs**, not a census of 11,070. Durations include
  queueing. The critical-path figure assumes workflows on one SHA start together, which is approximate.
- **Operator supervision time is still unmeasured** — as it was in both prior experiments. Nothing here
  changes that, and no figure in this note is a proxy for it.
- **`scripts/gate_fire_log.py` is gitignored** (`.cache/`), so no tool-usage telemetry survives a fresh clone.
  The repository presently cannot answer "how often is `repo_retrieve` actually invoked" across sessions —
  which is the denominator any retrieval saving would have to be multiplied by.
- **Carried forward, still unrepaired:** the `Measured = shipped` drift [PR #431](https://github.com/Joshua-Asante/first-passage/pull/431)
  found — v3 bound blob `041535ab…`, shipped `a6fc6ba4…`, voided by `561d8d7` — remains open, and the Limb B
  RESULTS still present `R@5 = 0.500` as attaching to the deployed artifact. Left to the operator, as that PR did.

## 7. If the goal is wall-clock, the levers are in CI

Named, not taken; three of the four are already on the `s2-linux-run` skill's own "faster loops still open" list.

1. **The `-n 0` qualification child** inside `Tests` — the largest single item on the critical path, explicitly serial.
2. **Cancellation waste** — 55.6% of S2 wall-clock; a batching discipline for pushes to branches with runs in flight.
3. **Shard the suite** across hosts; **cache the provisioned venv/worker image**.
4. **Path-filter the child** so markdown-only and `.claude/`-only changes do not pay 25 minutes — `tests.yml`
   already does this at the workflow level; the child does not discriminate further.

Each is worth minutes-to-tens-of-minutes per accepted task. The retrieval question, at its measured best, is
worth sub-seconds and currently costs +0.42 s.
