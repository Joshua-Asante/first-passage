**Theme:** harvest
**Status:** ACTIVE — FTS5-as-Delete falsifier v3 (Limb B re-measurement) results
# FTS5-as-Delete falsifier v3 — RESULTS

**Verdict:** `ASSISTIVE-ONLY` — `scripts/repo_retrieve.py`, as shipped and as widened under
this registration's one-revision cap, beats the `rg` incumbent decisively (limb 2 PASS) but
does not clear the frozen 0.70 recall floor (limb 1 FAIL).
**Pre-registration:** [`2026-08-15-fts5-delete-falsifier-prereg-v3.md`](../../../../docs/briefs/pre-registration/2026-08-15-fts5-delete-falsifier-prereg-v3.md),
frozen at commit `228c84e`, **before** either run below
**Harness:** [`remeasure.py`](remeasure.py) — reuses the 2026-07-27 falsifier's frozen
fixture-construction rule verbatim; imports and calls `scripts/repo_retrieve.py`'s own
`rebuild()`/`query()` directly (measured = shipped; no reimplementation)

---

## Run A — as shipped (pre-widening)

**Blob:** `scripts/repo_retrieve.py` = `55936412252d41b6838728648f0d8cbb57743668`
(`git rev-parse 228c84e:scripts/repo_retrieve.py` — the state immediately after PR #4/#5/#6
merged and the v3 prereg was frozen, before any corpus change)

Fixture: **34 pairs** (SESSIONS roll-off since v2's 117-pair run; frozen `MIN_PAIRS=15` clears
with margin). Corpus: whatever `collect_chunks()` returned at this blob — the 5 hot files +
truncated ADRs + truncated closures.

| Metric | Value |
|---|---|
| `R_shipped@5` | **0.500** (17/34) |
| `R_rg@5` (incumbent) | **0.088** (3/34) |
| Reachability ceiling (target present in corpus at all, any rank) | **0.676** (23/34) |

| Frozen limb | Result |
|---|---|
| 1 — `R_shipped@5 ≥ 0.70` | **FAIL** |
| 2 — `R_shipped@5 > R_rg@5` | **PASS** (0.500 vs 0.088) |

**One-revision-cap check, all three conditions verified before touching any code:**

1. Run A landed in trigger 2 (floor FAIL, beats `rg`) — yes.
2. Reachability ceiling (0.676) sits below the 0.70 floor **independent of ranking quality** —
   even a hypothetically perfect ranker over this corpus could not exceed 67.6% recall, because
   11 of 34 fixture targets do not exist anywhere in `collect_chunks()`'s output. Yes.
3. The fix available is corpus-only, not a ranking/scoring change — yes (ranking was already
   fixed in Phase 1).

All three held. One widening revision authorized and taken.

---

## Corpus widening (Run A → Run B, one-revision cap)

Extended `collect_chunks()` to add `docs/briefs/*.md` (brief bodies — previously only
`INDEX.md` and `closures/` were read), `docs/notes/audits/**` (restored onto this repo by
PR #5, not yet indexed), `docs/methodology/*.md`, `docs/spec/*.md` — continuing to exclude
`docs/ltm/` and `lab/archive/` per the Q-XMEM-1 Limb B denylist. Shipped as a real commit
(`2519926`) before Run B measured it — a hypothetical wider corpus cannot authorize the
narrower artifact that was actually deployed.

## Run B — post-widening (the current record)

**Blob:** `scripts/repo_retrieve.py` = `041535ab9c327dece90053009dde5faf0c4ad654`
(`git hash-object scripts/repo_retrieve.py` at commit `2519926`)

| Metric | Run A (pre-widening) | Run B (post-widening) |
|---|---|---|
| `R_shipped@5` | 0.500 (17/34) | **0.500 (17/34)** |
| `R_rg@5` | 0.088 (3/34) | 0.088 (3/34) |
| Reachability ceiling | 0.676 (23/34) | **0.735 (25/34)** |

| Frozen limb | Result |
|---|---|
| 1 — `R_shipped@5 ≥ 0.70` | **FAIL** |
| 2 — `R_shipped@5 > R_rg@5` | **PASS** |

**`VERDICT: ASSISTIVE-ONLY`** (trigger 2 of the frozen table). Per the one-revision cap, this is
final — **no further widening, no Run C**, regardless of this outcome.

### The counter-intuitive part, reported and not explained away

Widening the corpus raised the reachability ceiling by 2 targets (23→25) but **realized recall
did not move at all** — still 17/34 hits, and not the *same* 17: the miss list's composition
shifted (compare the two runs' printed misses — several queries that missed in Run A still
miss in Run B, joined by at least one query, `same theme collision warn test coverage`, that
was not a miss before). The most likely mechanism, not verified further under this
registration's no-further-investigation rule: FTS5's `bm25()` ranking is corpus-relative
(term/document-frequency statistics shift when ~162 new chunks are added), so widening the
corpus can simultaneously make some previously-unreachable targets reachable **and** push some
previously-well-ranked targets down, for a net-zero change in this measurement. This is
reported as an observation, not used to argue the true number is different from what was
measured — the same discipline the 2026-07-27 v2 RESULTS applied to its own miss pattern.

**What this means for the belt:** the gap between 0.500 and the 0.70 floor is **not** primarily
a corpus-coverage problem — widening already fixed most of the coverage gap the reachability
number diagnosed (0.676→0.735), and it bought nothing in realized recall. The residual gap is a
ranking/query-matching quality problem (the FTS5 term-bag `OR` query, snippet truncation,
`bm25()` default weighting), which this registration's one-revision cap deliberately does not
authorize touching.

---

## Blob-hash integrity note (found and fixed mid-run)

The harness's first draft computed the "as-run" blob hash with a hand-rolled
`sha1("blob <len>\0" + raw_bytes)` over the working-tree file's on-disk bytes. That disagreed
with `git hash-object` and `git rev-parse <commit>:<path>` on this machine
(`core.autocrlf=true` — git LF-normalizes before hashing; the raw disk bytes are CRLF). The
measurement itself was never affected (Python's text-mode file reads normalize line endings
regardless of the hashing bug), but the diagnostic "which blob did this run measure" line was
silently wrong — the exact class of defect this entire re-measurement exists to catch, just one
level down, in the tool built to prevent it. Fixed by shelling out to `git hash-object` instead
of reimplementing git's blob-hashing algorithm. Both blob hashes quoted above are the
git-verified values, cross-checked two independent ways (`hash-object` on the working tree,
`rev-parse <commit>:<path>` on the commit) before being written here.

---

## Disposition, applied

Per the frozen v3 table, trigger 2 (`ASSISTIVE-ONLY`):

- **The `_fts_companion` call in `scripts/check_advisor_dedup.py` stays disabled** — PR #4's
  quarantine is not lifted by this result.
- **`repo_retrieve.py` output stays invalid as a sub-rule 8/10 attestation source.**
  `.cursor/rules/session-discipline.mdc`'s suspension notice stays in force; not reworded here
  beyond citing this file.
- `docs/briefs/INDEX.md` and the Q-XMEM-1 brief's Limb B status cell are updated (separate
  commit, this same PR) to record: beats the incumbent decisively, does not clear the floor,
  re-measured post-widening.
- **Q-XMEM-1 is not closed** by this result, in either direction — it was never proposed to be.
  The A3 pre-condition (operator confirms the original cost no longer bites) is a separate gate
  a recall number cannot satisfy on its own, per both v1/v2 and this file's own forbidden moves.
- **The Limb C (local-embedder vector) question becomes live**, per Q-XMEM-1 v1.2's own
  pre-named trigger ("build only if Limb B is in use and still misses"). This result does
  **not** authorize building it — Q-XMEM-1 §5 requires a Rule 2 cost dry-run first, and that is
  an operator-paced decision, not a consequence of this measurement.

## Reproduce

```bash
python lab/analysis/harvest/limb_b_remeasure_2026-08/remeasure.py .
# expected: N=34, R_shipped@5 = 0.500, R_rg@5 = 0.088, VERDICT: ASSISTIVE-ONLY
# runtime ~1-2s (rg baseline scans the corpus per query; shipped tool uses its own FTS5 index)
```

Absolute values will drift from the numbers above as `docs/SESSIONS.md` rolls off and the
fixture regenerates from a different window — the pre-registration's own limitation, inherited
from v1/v2, and not something this run corrects.
