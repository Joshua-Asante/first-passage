# Jev experimentation — handoff to a local session

**Type:** Claude Code handoff / spawn prompt · **Authored:** 2026-09-19 · **Author:** cloud session
(`claude/sweet-cannon-gwryg2`) · **Target:** a **local** session on the operator's machine, which
has what this cloud container does not — the prior experiment artifacts, `OPENROUTER_API_KEY`,
network egress to `openrouter.ai`, and access to `first-passage-archive`.

**Why a local session.** The cloud container blocked all four requirements independently:
the artifacts live in `C:/Users/joshu/multi_firm_operations` and are absent from this clone,
branches and history; `OPENROUTER_API_KEY` / `TYPESAFE_API_KEY` are unset; the network policy
refuses `CONNECT` to `openrouter.ai:443` and `docs.typesafe.ai:443`; and the frozen fixture rule
is archived off-tree. None is fixable from here.

---

## §0 — Rule-0 reads (do these BEFORE proposing anything; paste literal output, not conclusions)

Production/record reads, with anchors, all verified present on `main` at HEAD `2943fd3`:

| Read | Path | Why it is load-bearing |
|---|---|---|
| The baseline itself | [`scripts/repo_retrieve.py`](../../../scripts/repo_retrieve.py) — shipped blob `a6fc6ba4e4e25d1a62d68256d2b0fe37543f2f14` | This *is* the metadata-aware keyword arm. Read `CORPUS_SOURCES` and `collect_chunks()` before treating it as a black box. |
| The measured record | [`lab/.../limb_b_remeasure_2026-08/RESULTS.md`](../../../lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md) | `R@5 = 0.500`, `R_rg@5 = 0.088`, ceiling `0.735`. Read the 2026-09-19 blob-provenance annotation first. |
| The binding clause | [`2026-08-15-fts5-delete-falsifier-prereg-v3.md`](../pre-registration/2026-08-15-fts5-delete-falsifier-prereg-v3.md) | "Measured = shipped", the one-revision cap, and the frozen fixture-construction rule. |
| Why the old number no longer binds | [drift audit](../../notes/audits/2026-09-19-limb-b-measured-shipped-drift.md) | `561d8d7` moved the blob; the v3 verdict no longer attaches to the deployed artifact. |
| What authority exists | [Q-XMEM-1 §Addendum 2026-09-19](../Q-XMEM-1-cross-surface-memory-sidecar-pilot.md) + [pursuit record](../../pursuits/c1-q-xmem-1.md) | Re-entry is **pursuit-layer only**. Read the scope table before building anything. |
| What was already tried, and its limits | [disposition](2026-09-19-jev-experimentation-disposition.md) | Both completed experiments and every disclosed limitation. |

Also run sub-rule 8 (paste-search before new work) against `lab/CATALOG.md` and
`docs/briefs/INDEX.md` — this session found substantial prior art that a topic keyword search
returned empty on.

---

## §0.5 — Clarifying questions to resolve BEFORE any paid call

Answer these in the session; do not assume. Each one changes the work materially.

1. **Which reader/agent is the measurement target?** The deployment intent decides this — Claude
   Code, Claude API, Codex, or the `gpt-4.1-mini` reader used before. Measuring one and deploying
   another is the detachment defect this repo keeps re-learning.
2. **What usage is actually observable for that target?** Confirm input/output/cache/reasoning
   counters exist *before* designing around them. If subscription quota is not observable, say so
   and stop converting API token percentages into quota claims.
3. **What is the data-transfer and spend scope?** Prior approvals were spent on specific corpora
   and one replay. `first-passage` is a **public** repo but its corpus includes governance records;
   confirm what may leave the machine, and the ceiling including retries.
4. **Is the fixture retrievable?** `falsifier_v2.py` (frozen fixture rule) and `remeasure.py` are
   in `first-passage-archive` at `5d47b4dc`. If they cannot be retrieved, the comparison cannot be
   anchored to the v3 series and that must be stated, not worked around with a new fixture.
5. **What minimum effect would justify integration?** Derive it from expected workload and
   integration cost. Do **not** copy 20% / 30% from the prior experiments mechanically — the 20%
   target in pilot 1 was mathematically impossible on its corpus.

---

## §1 — Context

The investigation asks whether a cheap reranker (Jev) reduces frontier-agent usage and supervision
by selecting evidence before a reasoning agent reads it. Two experiments completed. Experiment 2
passed its frozen criteria (reader input −65.02%), but a post hoc control that simply indexed
**paths and headings** recovered most of the unique benefit, narrowing it to **one fact / one
task**. Nothing about agent quota, supervision, review quality or speed was ever measured.

What is new, and why the work belongs here: **First Passage already holds the strong control the
investigation says it lacks.** `repo_retrieve.py` is metadata-aware FTS5 over paths, headings and
bodies, measured against a **rule-constructed** fixture (not author-selected tasks), with a
reachability ceiling of `0.735` against realized `0.500`. That ceiling is the oracle-headroom
pre-check pilot 1 lacked, and RESULTS diagnoses the residual gap as a **ranking-quality** problem —
precisely the category a reranker addresses. This is a better test bed than the original corpus.

Two conditions attach. The operator reopened Q-XMEM-1 on 2026-09-19, so the pursuit layer is live —
but **pursuit layer only**, authorising no build, install, spend or quarantine lift. And the v3
verdict no longer binds the shipped blob, so the baseline must be re-established in the same run
before it can anchor anything.

---

## §4 — Falsifiable hypothesis

**H.** On the frozen rule-constructed fixture, reranking `repo_retrieve.py`'s candidate list with
Jev recovers a material share of the realized-to-ceiling recall gap that metadata-aware keyword
ordering leaves on the table.

**Form.** If, measured in a single run against one recorded blob and one fixture, Jev reranking
raises `recall@5` by **≥ 50% of the (ceiling − baseline) gap** measured in that same run, *and*
does so without lowering recall on any stratum, **then** reranking is a live limb and earns one
scoped follow-up. **Otherwise** the ranking-quality diagnosis is not addressable by reranking at
this corpus size, and that limb closes on this evidence.

**Falsifier.** H is **falsified** if, with reachability confirmed pre-spend, Jev's reranked
`recall@5` fails to clear baseline by ≥ 50% of that run's `(ceiling − baseline)` gap — or clears it
only by trading recall away on another stratum. A falsified H closes the reranking limb on this
evidence; it does not reopen the v3 verdict, and it is not a verdict on Jev in other corpora.

**Mandatory pre-flight, before any paid call:** compute the oracle ceiling and the baseline on the
current blob. If `(ceiling − baseline)` is too small for the threshold to be reachable, **say so
and stop** — pilot 1's 20% target was unreachable by *any* ranker and nobody checked first. Report
reachability as a number, not a judgment.

**Strata to report separately** (sampling method stated per stratum): ordinary cases, ambiguous
wording, conflicting/stale sources, and missing-answer cases. A relevance score is not authority;
unknown-answer and conflicting-version cases need their own measured policy.

---

## §5 — Forbidden moves

Each of these was either live in this session or already bit the prior one.

- **Do not roll the STATE weekly deadline to green CI.** Advancing the recurring schedule is an
  operator act that must carry its record. Week 09-14→09-18 was **missed**, and on 2026-09-19 the
  operator recorded the miss, reported the account still active, and advanced the schedule to
  2026-09-25 — preserving the missed-week record, which STATE now requires explicitly. That is the
  shape: never silence `state-currency` by editing the date alone.
- **Do not cite the v3 recall figures as current.** They bind blob `041535ab…`, not what ships.
- **Do not treat the Q-XMEM-1 reopen as build authority.** Limb A T0/install, Limb C, the
  `repo_retrieve.py` attestation quarantine and the disabled `_fts_companion` call all keep their
  own gates. Re-entry lifted the pursuit disposition, nothing else.
- **Do not convert API-reader token percentages into subscription-quota percentages.** They are
  not the same quantity, and the prior run shifted work to a cheaper model rather than removing it
  (55,834 total treatment input tokens vs 29,819 for broad reading).
- **Do not re-invoke `retry_once.py`.** That one-shot recovery is spent and was explicitly approved
  once. Do not edit frozen experiment inputs, clear ledgers, or rerun paid modes to "reproduce" a
  retained result — start a new directory and protocol.
- **Do not author or revise tasks/labels after seeing model output**, and do not discard easy cases
  to manufacture a gain. Freeze labels before inference; report every case and deviation.
- **Do not stack interventions** (metadata indexing + chunking + caching + reranking) and credit
  the result to Jev. One variable per comparison.
- **Do not widen the corpus or change ranking mid-run** to chase a threshold. The v3 one-revision
  cap is the precedent for why.
- **No agent places a trade**, and nothing here touches strategy parameters, allocations,
  `dd_protection` constants or MC calibration.

---

## §6 — Gate criteria and return status

Binary closure, decided against §4's threshold computed in the same run:

- **`RESOLVED — limb live`** — reachability confirmed pre-spend, and Jev clears the §4 threshold
  with no stratum regression. Earns one scoped follow-up; **not** integration.
- **`FALSIFIED — limb closed`** — reachability confirmed, threshold not cleared. Record and close.
- **`AMBIGUOUS-DESIGN`** — the gap was unreachable, the fixture unrecoverable, or the run could not
  be anchored to one blob. This is a design verdict, not a weak pass; do not report it as either
  outcome.

**Return status taxonomy** (report exactly one):

- **`DONE`** — one interpretable experiment result, artifacts retained, verdict recorded.
- **`DONE_WITH_CONCERNS`** — result obtained, but with a stated deviation, service failure or
  limitation that qualifies it. Name the qualification in the first line.
- **`NEEDS_CONTEXT`** — a §0.5 question could not be answered locally. Name which, and stop.
- **`BLOCKED`** — credentials, archive retrieval, spend scope or authority unavailable. Name the
  exact blocker and the smallest human action that clears it.

**Return boundary.** Stop at one interpretable result. No automatic hooks, no default agent/model
routing, no production deployment, no new paid service, and no lifting of the `repo_retrieve.py`
attestation quarantine follow from a passing benchmark. Re-authorising that quarantine needs a
fresh registration and a real measurement, which is a separate operator act.

**Service-handling discipline** (the prior run's overhead is the anchor): predeclare a total
attempt budget **including** bounded retries, honour `Retry-After`, preserve unresolved cost
reservations and request identities, never replay a success, and distinguish timeout/unknown
completion from explicit rejection. Test those paths locally before spending.

---

## §10 — Audit hooks

Run from the repository root of the local checkout. These are read-only and cost nothing.

```bash
# 1. Anchor the baseline: is the shipped blob still the one you are measuring?
git hash-object scripts/repo_retrieve.py
# v3 Run B bound 041535ab9c327dece90053009dde5faf0c4ad654; drift voids "Measured = shipped".

# 2. Prove the tool runs and is metadata-aware before comparing anything to it.
python scripts/repo_retrieve.py --rebuild
python scripts/repo_retrieve.py --query "dd protection trigger scale frozen"

# 3. Behaviour regression on the collector (expect 11 passed).
python -m pytest tests/test_repo_retrieve.py -q

# 4. Prior art — sub-rule 8 paste-search. An empty result is NOT evidence of none.
python scripts/check_advisor_dedup.py --keywords "retrieval rerank evidence selection"
grep -n -i "xmem\|repo_retrieve\|fts5" lab/CATALOG.md docs/briefs/INDEX.md

# 5. Retrieve the archived fixture + harness (required to anchor to the v3 series).
#    first-passage-archive @ 5d47b4dc — see lab/ARCHIVED.json removed_files.
python -c "import json;print(json.load(open('lab/ARCHIVED.json'))['studies']['limb_b_remeasure_2026-08'])"

# 6. Governance gates before any commit. Expect a clean exit 0 as of 2026-09-19.
#    If state-currency fails, a recurring deadline has lapsed -- that is an
#    operator obligation, never something to fix by editing the date.
make check
```

**Credential check without exposing values:**

```bash
python -c "import os;print({k:bool(os.environ.get(k)) for k in ('OPENROUTER_API_KEY','TYPESAFE_API_KEY')})"
```
