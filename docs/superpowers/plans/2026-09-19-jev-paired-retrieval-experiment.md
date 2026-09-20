# Jev Paired Retrieval Experiment Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans. This handoff is executed inline by the coordinator.

**Goal:** Determine whether Jev supplies incremental context savings over both broad and compact keyword retrieval while preserving evidence-supported answers.

**Architecture:** Freeze paragraph excerpts from six existing workflow documents and eight retrospective task questions. Compare BM25 top 12, BM25 top 4, and Jev reranked top 4 with the same GPT-4.1-mini reader through OpenRouter; score fixed answer choices and source citations locally.

**Tech Stack:** Existing operations Python 3.13.2, standard library, installed TypeSafe skill, OpenRouter Decisions and chat APIs.

**Spec:** User request to run the next useful experiment; detailed predeclared protocol in `recovery/jev-paired-retrieval-20260919/PROTOCOL.md`.

**Completion:** All eight paired comparisons completed. The primary outcome criteria survived: 65.02% lower reader input; 16/16 supported answers, matching broad retrieval; 8/8 complete tasks versus compact keyword retrieval's 5/8. Median treatment time was 0.423 seconds slower. The provider rejected one request; the user explicitly approved one unchanged replay, raising the ceiling to 33 attempts with the same $0.10 budget. Reported spend was $0.024188126. [Final evidence and limitations](../../../recovery/jev-paired-retrieval-20260919/RESULTS.md). The coordinator accepts this experiment outcome; actual Codex usage/supervision savings remain unproven and no default integration is enabled.

**Exploratory qualification:** A post hoc local BM25 index including headings/paths recovered 15/16 facts and complete evidence for 7/8 tasks without new API calls. This was not a reader arm and does not revise the frozen verdict, but it narrows Jev's unique coverage advantage to one task. Improve keyword indexing before considering default Jev retrieval; use that stronger baseline in any follow-on trial.

## Global Constraints

- Preserve the first experiment and unrelated work; no production integration, hooks, dependency edits, commits or publication.
- Reuse the isolated Jev worktree launcher at revision c2e6eb2cbe159b60fdff7873b9e96aef943c46df. Doctor passed with 62 matching locked distributions.
- New corpus transfer and downstream reader access must be covered by explicit consent; earlier approval named only the first corpus.
- Freeze corpus, labels, protocol and runner before live evaluation. No outcome-based case replacement or prompt tuning.
- At most 32 external requests and $0.10 budget, no automatic retries. Preserve requests, responses, identities and actual usage.

## Selected handoff

**Selected outcome:** One reproducible three-arm experiment with a predeclared verdict, actual reader-token and latency measurements, and retained evidence.

**Prerequisites:** Jev access verified; OpenRouter credential present; operations environment validated. New export approval pending until exact corpus and requests exist for review. Reader model availability/pricing verified from OpenRouter's current catalog.

**Ownership:** Current agent is executor and coordinator and retains combined acceptance.

**Verification:** Test missing-evidence/citation handling, input exclusion of labels, immutable freeze and request budgets. Verify candidate headroom before live evaluation. Check all response schemas, score every case including failures, preserve complete paired inputs/outputs, and disclose unrun project suites.

**Checkpoint:** Report baseline headroom before inference, request concrete export consent, then report final paired findings and limitations. Evidence lives in the experiment directory.

**Return boundary:** Stop after the frozen batch and report; no default activation, bigger experiment or remote publication follows automatically. If access fails, retain completed comparisons and report incompleteness rather than infer missing results.

- [x] Snapshot six sources into sanitized paragraph excerpts; establish provenance and eight task labels.
- [x] Add focused evaluation tests; observe expected failures before implementing the evaluation behavior.
- [x] Implement three-arm packets, fixed reader prompts, immutable freeze and bounded request ledger.
- [x] Inspect shortlist coverage and headroom; freeze and obtain exact export approval.
- [x] Run the bounded paired batch, score, inspect errors and write the decision report.
