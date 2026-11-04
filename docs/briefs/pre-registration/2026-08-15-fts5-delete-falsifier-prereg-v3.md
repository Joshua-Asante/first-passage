# Verdict pre-registration — FTS5-as-Delete falsifier v3 (Limb B re-measurement)

**Status:** `FROZEN` — 2026-08-15, **BEFORE any harness runs or recall number is computed
under this file**
**Parent:** [`docs/notes/audits/programme-audit/2026-08-15-governance-belt-meta-audit.md`](../../notes/audits/programme-audit/2026-08-15-governance-belt-meta-audit.md)
§5 action 1 — remediation Phase 2. [PR #4](https://github.com/Joshua-Asante/first-passage/pull/4)
(quarantine), [#5](https://github.com/Joshua-Asante/first-passage/pull/5) (docs restore), [#6](https://github.com/Joshua-Asante/first-passage/pull/6)
(rank/UTF-8/staleness patch) — Phase 0/0b/1 — merged before this file is committed.
**Supersedes (for the re-measurement question only):** [`2026-07-27-fts5-delete-falsifier-prereg-v2.md`](2026-07-27-fts5-delete-falsifier-prereg-v2.md) —
does not reopen v2's own `DELETE-HOLDS` verdict or its measured numbers; this is a fresh
registration testing whether the **shipped artifact** (not a bespoke harness) still clears
the same frozen threshold after the 2026-08-15 quarantine-and-patch cycle.
**Operator ruling:** direction to "proceed with Phase 2" given 2026-08-15, session following
the governance-belt audit. No separate A3-style ruling is required to *run* this measurement —
only to act on a `DELETE-HOLDS` result past re-enabling the mechanism (see Forbidden moves).
**Bears on:** [`Q-XMEM-1`](../Q-XMEM-1-cross-surface-memory-sidecar-pilot.md) Limb B — the
brief's own architecture (§4/§5/§6) stays frozen and untouched by this file.

---

## What is being tested, and what is not

**Tested:** whether **`scripts/repo_retrieve.py` as it exists in the repository right now** —
called through its own public functions (`rebuild()`, `query()`), not a reimplementation —
retrieves prior work well enough to be trusted again as a Rule 8 sub-rule 8/10 attestation
source, after the 2026-08-15 quarantine (missing `ORDER BY rank`, recall@5 = 0.086, tied with
the `rg` incumbent) and the same-day patch (rank restored, UTF-8-safe output, HEAD-stamped
staleness).

**Not tested:** Mem0 / Limb A (untouched, still gated on a separate operator GO). The Q-XMEM-1
architecture itself. Whether a *differently-scoped* corpus could theoretically do better — that
question is answered only if this file's own one-revision clause below is triggered, and even
then the widened corpus must actually ship as real code before its number counts (see
**Measured = shipped** below).

**Why re-register rather than reopen v2.** v2 measured a **bespoke harness** (`falsifier_v2.py`,
inline SQL with `ORDER BY bm25(docs)`, a nearly-unrestricted corpus via `ROOT.rglob("*.md")`)
to decide whether to *build* Limb B at all. That question is settled — `DELETE-HOLDS`,
2026-07-27, `R_fts5@5 = 0.718`. What shipped nine days later did not match what was measured:
different retrieval SQL (no `ORDER BY`), a much narrower corpus (5 hot files + truncated
ADRs/closures, not the whole repo). The governance-belt audit's central finding was exactly
this detachment. This file exists to close it — the verdict must attach to the artifact that
is actually deployed, not to a stand-in for it.

---

## Measured = shipped (binding clause)

The verdict registered here is valid **only** for the exact blob committed at the time the
harness runs, identified by `git hash-object scripts/repo_retrieve.py`. **Any subsequent edit
to that file's ranking, corpus (`collect_chunks`), or chunking logic voids this verdict** —
Rule 8 sub-rule 8/10 attestations may not cite a `DELETE-HOLDS` result measured against a
different blob than the one currently on disk. A new registration is required after any such
edit, per the same Known Trap #12 standard v2 named.

Blob hash at freeze time (this file, `scripts/repo_retrieve.py`, immediately prior to Run A):
`55936412252d41b6838728648f0d8cbb57743668` (repo HEAD `b4eb2fb`, all of PR #4/#5/#6 merged).

The harness (below) **imports and calls** `scripts/repo_retrieve.py`'s own `rebuild()` and
`query()` — it does not re-derive FTS5 SQL. If the shipped code's SQL, corpus, or chunking
changes between freezing this file and running it, the run is invalid and must be redone
against a freshly recorded blob hash.

---

## Fixture construction (frozen — reused verbatim from v2, not re-derived)

**Identical to the v2 pre-registration's frozen rule** — retrieved from the pruned harness at
`git show pre-prune-2026-08-08:lab/analysis/harvest/fts5_delete_falsifier_2026-07-27/falsifier_v2.py`
and ported without modification (`build_fixture()`, `strip_identifiers()`, `is_sessions_family()`,
and the `LINK`/`DATE`/`QID`/`FILENAME`/`SLUGGY`/`NONWORD` patterns, byte-identical):

1. Enumerate `## ` entries in `docs/SESSIONS.md`.
2. Query = the entry heading, identifiers stripped (dates, `Q-` IDs, filenames, slug-shaped
   tokens).
3. Expected document = the **first** markdown link in the entry body pointing to a resolvable,
   non-SESSIONS-family `.md` file.
4. Drop if the stripped query has fewer than 3 words.
5. Drop if the stripped query appears verbatim inside the target document (verbatim-confound
   guard).
6. Keep every surviving pair.

`MIN_PAIRS = 15` (frozen). Fewer than 15 surviving pairs ⇒ `AMBIGUOUS`, not a verdict — same as
v1/v2.

**Not reused from v2:** the corpus-loading and retrieval functions (`load_corpus`, `fts5_topk`).
v2's corpus was `ROOT.rglob("*.md")` minus SESSIONS-family — a different, wider corpus than
`repo_retrieve.py` actually indexes. This run's corpus is whatever
`scripts.repo_retrieve.collect_chunks(repo)` returns, exactly as shipped — that is the entire
point of this re-registration (see **Measured = shipped**).

`rg` baseline (`rg_topk`, frozen, engine-parity `terms_of()`) is reused verbatim from v2 for the
anti-reimplementation limb — same corpus (`ROOT.rglob("*.md")` minus SESSIONS-family) as v2 used
for `rg`, so the comparator is unchanged.

---

## Verdict table (frozen)

`K = 5` (frozen, matches v1/v2). `RECALL_FLOOR = 0.70` (frozen, matches v1/v2, unmoved by the
audit — the governance-belt finding was that the *implementation* drifted from what the floor
was measured against, not that the floor itself was wrong).

Let `R_shipped@5` = recall@5 of `repo_retrieve.py`'s own `rebuild()`/`query()` over its own
corpus. Let `R_rg@5` = recall@5 of the frozen `rg` baseline over its own (wider) corpus.

| # | Trigger | Verdict | Disposition |
|---|---|---|---|
| 1 | `R_shipped@5 ≥ 0.70` **and** `R_shipped@5 > R_rg@5` | `REAUTHORIZE` | Re-enable the `_fts_companion` call in `check_advisor_dedup.py`; resume treating `repo_retrieve.py` output as a valid sub-rule 8/10 attestation source; addendum on Q-XMEM-1 recording the re-measured pass. **Does not close Q-XMEM-1** — the brief's own A3 pre-condition (operator confirms the cost no longer bites) is a separate, later gate this recall number cannot satisfy on its own. |
| 2 | `R_shipped@5 < 0.70` **and** `R_shipped@5 > R_rg@5` | `ASSISTIVE-ONLY` | Tool stays quarantined for attestation purposes; session-discipline's suspension (PR #4) stays in force. INDEX/Q-XMEM-1 status cells updated to record it beats the incumbent but doesn't clear the floor. The Limb C (local-embedder vector) question in Q-XMEM-1 v1.2 becomes live — but building it is **not** authorized by this trigger alone; it needs its own Rule 2 cost dry-run per that brief's existing text. |
| 3 | `R_shipped@5 ≤ R_rg@5` | `WITHDRAW` | The companion call and the `repo_retrieve.py` invocation from session-discipline are removed outright (not just left disabled) — a REMOVE, executed without further litigation. Q-XMEM-1 v1.2 Limb B addendum marked withdrawn; Limb A (Mem0) and Limb C become the live options, per the brief's own §7. |
| — | Fewer than 15 fixture pairs survive | `AMBIGUOUS` | Record and stop. Re-test conditions: next `docs/SESSIONS.md` window with ≥15 surviving pairs. |

---

## One-revision cap (new in v3 — not present in v1/v2)

**Run A** is `repo_retrieve.py` exactly as it exists at the blob hash frozen above. Run A's
result is used for the verdict table **unless** all three of the following hold:

1. Run A lands in trigger 2 or 3 (floor FAIL, or limb-2 FAIL), **and**
2. a **reachability check** — computed *before* looking at query-level recall, by checking what
   fraction of fixture target paths appear anywhere in `collect_chunks(repo)`'s output paths —
   shows the corpus itself cannot reach ≥0.70 of fixture targets **regardless of ranking
   quality** (i.e., the floor is unreachable on reachability grounds alone, not a ranking
   defect), **and**
3. no ranking or scoring change is involved in the fix — only widening which files
   `collect_chunks()` reads.

If, and only if, all three hold: **one** widening revision is permitted. Extend
`collect_chunks()` to include additional hot governance surfaces — candidates named in advance,
before Run A's result is known: `docs/briefs/*.md` (brief bodies, currently only `INDEX.md` and
`closures/` are read), `docs/notes/audits/**` (restored by PR #5, not yet indexed),
`docs/methodology/*.md`, `docs/spec/*.md` — **while continuing to exclude `docs/ltm/` and
`lab/archive/`** per Q-XMEM-1 §5's existing denylist. This widening must land as a real,
committed code change to `scripts/repo_retrieve.py` (its own PR) **before** Run B measures it —
per **Measured = shipped**, a hypothetical wider corpus cannot authorize the narrower shipped
tool.

**Run B**, if triggered, measures the newly-shipped blob. Whatever Run B's result is, it is
final — **no Run C**, regardless of outcome. If Run B still fails, disposition follows the
verdict table above (trigger 2 or 3) against Run B's numbers, and the corpus does not widen
again under this registration.

---

## Forbidden moves (frozen)

- Tuning the fixture after seeing a result — construction is mechanical, reused verbatim from
  v2, frozen above.
- Per-engine query rewriting to flatter `repo_retrieve.py` (the shipped tool's own query
  construction is used exactly as it ships — this run does not hand-tune query terms).
- Reporting `recall@k` for a `k` chosen after seeing the curve — `k = 5` is frozen.
- Widening the corpus for any reason other than the diagnosed reachability gap named in the
  one-revision cap, or running more than one revision.
- Treating a `REAUTHORIZE` verdict as closing Q-XMEM-1 — the brief's A3 pre-condition is
  separate and is not satisfied by a recall number (same forbidden move v1/v2 named).
- Treating a `WITHDRAW` or `ASSISTIVE-ONLY` verdict as a reason to adopt Mem0/Limb A — that
  decision is independent, per v1/v2's identical clause.

## Commit discipline

This file is committed **before** the harness runs and before any recall number under it
exists. Results land in a separate artifact under `lab/analysis/harvest/limb_b_remeasure_2026-08/`
referencing this file's commit hash. Any threshold edit after the first measurement requires
closing this registration `AMBIGUOUS` (if warranted) and re-registering under a fresh v4, not
editing this file in place.
