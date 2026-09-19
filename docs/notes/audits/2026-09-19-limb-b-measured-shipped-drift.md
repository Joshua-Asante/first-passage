# AUDIT — Limb B v3 verdict detached from the shipped blob (2026-09-19)

**Target:** [`scripts/repo_retrieve.py`](../../../scripts/repo_retrieve.py) and the verdict
registered against it in
[`2026-08-15-fts5-delete-falsifier-prereg-v3.md`](../../briefs/pre-registration/2026-08-15-fts5-delete-falsifier-prereg-v3.md).
**Finding:** the v3 registration's **"Measured = shipped"** binding clause is no longer
satisfied. **Severity:** low, bounded — an attestation-binding defect, not a demonstrated
behaviour regression.

Found incidentally while assessing whether First Passage's retrieval baseline could serve an
external reranking comparison ([disposition](../../briefs/handoffs/2026-09-19-jev-experimentation-disposition.md)).
This note records the drift only; it opens nothing and re-authorises nothing.

## The clause and the drift

The v3 pre-registration binds its verdict to one exact blob:

> The verdict registered here is valid **only** for the exact blob committed at the time the
> harness runs, identified by `git hash-object scripts/repo_retrieve.py`. **Any subsequent edit
> to that file's ranking, corpus (`collect_chunks`), or chunking logic voids this verdict** …
> A new registration is required after any such edit.

| Item | Value |
|---|---|
| Blob bound by v3 Run B | `041535ab9c327dece90053009dde5faf0c4ad654` |
| Blob shipped at HEAD `2943fd3` | `a6fc6ba4e4e25d1a62d68256d2b0fe37543f2f14` |
| Changing commit | `561d8d7` (2026-09-17, on `main`) — *Consolidate configuration ownership with bounded packet designs* |

`561d8d7` replaced the hand-synchronised `HOT_FILES` tuple and `collect_chunks()`'s repeated
collection branches with an ordered `CORPUS_SOURCES` tuple of frozen `CorpusSource` records
plus one dispatcher. That is an edit to corpus and chunking logic — the clause's named
category. The clause is categorical: it voids on edit, not on measured behaviour change.

## Why the severity is low

The refactor was contract-preserving *by design*. Packet 1 of the
[configuration-as-code completion record](../../superpowers/plans/2026-09-17-configuration-as-code-completion.md)
states the contract: "Preserve ordered chunks, duplicates already produced by overlapping
inputs, missing-file behavior, catalog ACTIVE/HOLD row extraction after omitting In flight,
newest 24 session chunks, ADR INDEX/TOMBSTONES exclusions, 20-line closure excerpts and 24-line
ordinary excerpts… Do not change ranking or index staleness behavior."

Observed 2026-09-19 on HEAD `2943fd3`: `tests/test_repo_retrieve.py` — **11 passed**; a
`--rebuild` produced **582 chunks** and `--query` returned ranked path+heading+snippet hits.
So chunk-level behaviour is tested and the tool runs.

The verdict at issue is also *restrictive* — `ASSISTIVE-ONLY`, with the `_fts_companion` call
in `scripts/check_advisor_dedup.py` left commented out as a final disposition. Drift therefore
loosens no control, and [Q-XMEM-1](../../briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md)
has been `CLOSED — SUBTRACT` since 2026-08-19, so nothing is actively riding on the number.

## What is actually wrong

The recorded disposition — `R_shipped@5 = 0.500`, `R_rg@5 = 0.088`, reachability ceiling
`0.735`, "beats the incumbent decisively" — is still presented as current in
[RESULTS](../../../lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md) and in the
Q-XMEM-1 Limb B status cell, while citing a blob that is no longer shipped. No test in the
repo asserts the blob binding, so the clause voided silently. This is the same
*measured ≠ shipped* class the governance-belt audit and the v3 re-registration exist to
catch, recurring one level down.

**Consequence if left:** a future re-authorisation that cites those figures would be citing a
detached measurement — the precise failure v3 was written to close.

## Disposition

- **No re-measurement performed here.** The v3 one-revision cap is spent and its verdict is
  final under that registration; re-measuring would need a fresh registration, which is an
  operator act.
- The harness is **correctly archived**, not lost: `lab/ARCHIVED.json` lists
  `limb_b_remeasure_2026-08/remeasure.py` under `removed_files` with an `archive_url` in
  `first-passage-archive` at `5d47b4dc`. RESULTS' "Reproduce" block names the bare path
  without noting it is archived off-tree — a documentation nit, not a retention defect.
- Suggested minimum repair, operator-paced: annotate the RESULTS verdict and the Limb B status
  cell with "measured against blob `041535ab…`; superseded on disk by `561d8d7`," so the figures
  cannot be cited as attaching to the current artifact. A fresh registration is only needed if
  someone wants a live number again.
