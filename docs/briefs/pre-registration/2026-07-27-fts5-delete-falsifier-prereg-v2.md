# Verdict pre-registration v2 — FTS5-as-Delete falsifier (limb A of the Hermes adoption ruling)

**Status:** `FROZEN` — 2026-07-27, **before any recall number exists**
**Supersedes:** [`2026-07-27-fts5-delete-falsifier-prereg.md`](2026-07-27-fts5-delete-falsifier-prereg.md) (v1, commit `f70d46b`), which returned `AMBIGUOUS` on an empty fixture — see [`RESULTS`](../../../lab/analysis/harvest/fts5_delete_falsifier_2026-07-27/RESULTS.md)
**Parent brief:** [`2026-07-27-hermes-agent-adoption-ruling.md`](../programs/2026-07-27-hermes-agent-adoption-ruling.md) §6 limb A — operator ruling `A3` (Delete)
**Bears on:** [`Q-XMEM-1`](../Q-XMEM-1-cross-surface-memory-sidecar-pilot.md) — architecture stays frozen and untouched

---

## Why v1 failed, and what that obliges v2 to do differently

v1 froze a fixture rule (markdown links whose **link text** is ≥4-word descriptive prose, harvested from `lab/CATALOG.md` + the two INDEX files) without checking whether that link shape exists here. It does not: `CATALOG.md` carries **zero** markdown links, and INDEX link texts are 1–2 word identifiers (`closure`, `RESULTS`, `pre-reg`). Fixture size: **0**. That was Known Trap #13 — precision exceeding grounding.

v2's obligation is therefore procedural, not just textual: **every structural assumption below was measured against the repo before this file was frozen.** Verified 2026-07-27:

| Assumption | Verified result | Viable? |
|---|---|---|
| Brief bodies carry prose-text links | 134 files, 758 one-word link texts, 27 two-word, 11 three-word, **1** with ≥4 words | **No — rejected** |
| `docs/SESSIONS.md` has descriptive entry headings | **151** `## ` entries, headings observed 8–14 words | **Yes** |
| Those entries link to real artifacts | **120** of 151 entries have ≥1 link resolving to an existing `.md` | **Yes** |
| Full rule (below) yields ≥15 pairs | **117 pairs, 97 distinct targets** | **Yes** |

**Exploration boundary (the bright line).** Only *fixture viability* — counts, shapes, sample pairs — was inspected pre-freeze. **No recall number, for either engine, was computed before this file was committed.** Choosing a source that yields a non-empty fixture is the correction v1's RESULTS demanded; choosing a threshold or a rule because it produced a favourable *result* would be Trap #12, and did not occur.

---

## Fixture construction (frozen)

1. Split `docs/SESSIONS.md` on `^## ` headings. Each entry = one candidate pair.
2. **Query** = the heading text, with dates, `Q-`ids, filenames, and slug/path tokens stripped, lowercased, punctuation collapsed. This is a paraphrase probe by construction: it is how the operator *described the work*, not the target's own wording.
3. **Expected document** = the **first** markdown link in that entry's body resolving to an existing `.md` file that is not in the SESSIONS family. First-link, not best-link — no discretion.
4. Drop pairs whose stripped query has <3 words.
5. **Drop pairs whose stripped query appears verbatim in the expected document** — those are identifier lookups, not paraphrase probes. (Directly addresses the self-containment confound v1's RESULTS named as unaddressed. Measured: 1 pair dropped.)
6. **Use every surviving pair.** No `N` cap, no ordering choice — v1 capped at `N=20`, which is discretion this design does not need. Report `N`.

**Candidate-pool exclusion (frozen):** the SESSIONS family — `docs/SESSIONS.md` and `docs/ltm/notes/archive/sessions/SESSIONS-*.md` (3 files, verified present) — is excluded from retrieval results for **both** engines. Queries are drawn from that corpus, and `roll_sessions.py` moves entries **verbatim** into the quarterly archives, so leaving them in would let both engines trivially retrieve the query's own source. Everything else in the corpus is eligible, **including the cold store** (`lab/archive/`, `docs/ltm/`) that `.rgignore` hides from default search — recall over that material is part of what a Delete must deliver.

**Engine parity (frozen):** both engines receive the identical term list (whitespace tokens of length >2). FTS5 uses default tokenizer with an `OR` match ranked by `bm25`. The incumbent baseline is ripgrep-style literal alternation over the same terms, ranked by match count, ties broken by path. No per-engine query rewriting.

---

## §6 verdict table (frozen — thresholds **unchanged from v1**)

Let `R_fts5@5` and `R_rg@5` be recall-at-5 over the `N` pairs: the fraction whose expected document appears in that engine's top 5.

| Verdict | Trigger | Disposition |
|---|---|---|
| `DELETE-HOLDS` | `R_fts5@5 ≥ 0.70` **and** `R_fts5@5 > R_rg@5` | Delete viable. Build the sidecar (search + staged write only). `Q-XMEM-1` becomes *eligible* to close `MOOT` — still gated on the operator confirming the original cost no longer bites |
| `DELETE-FAILS` | `R_fts5@5 < 0.70` **or** `R_fts5@5 ≤ R_rg@5` | Delete fails on its merits. Build nothing. `Q-XMEM-1` returns intact and un-mooted; A1/A2 live again; the embedder question reopens |
| `AMBIGUOUS` | `N < 15` | Fixture too thin. Do not build, do not moot |

**Thresholds are carried over verbatim and deliberately.** `0.70` and the `> R_rg` anti-reimplementation clause were justified in v1 on fixture-independent grounds (at `recall@5 = 0.70` roughly one probe in three still misses — tolerable for an assistive search box, not for a claim to *remove* the cost). Re-deriving them now, against a fixture I have measured the size of, would be indistinguishable from tuning. They stand as frozen.

---

## Forbidden moves (frozen)

- **Any threshold or rule change after the first recall number exists** — that closes `AMBIGUOUS` and requires a v3 authored before the next run (Trap #12).
- **Widening the fixture beyond `docs/SESSIONS.md`** if the result disappoints. The source was selected on measured viability *before* freeze; reselecting it after seeing recall is tuning.
- **Per-engine query rewriting** (stemming, stopword handling, or phrase quoting applied to one engine only).
- **Reporting `recall@k` for a `k` chosen after seeing the curve.** `k=5` is frozen; other `k` may be reported as context, never as the verdict.
- **Closing `Q-XMEM-1` `MOOT` on `DELETE-HOLDS` alone** — the A3 pre-condition is a separate operator confirmation.
- **Reading `DELETE-FAILS` as an argument for adopting Hermes.** The adoption ruling is independent; a failed Delete reopens `Q-XMEM-1` and nothing else.

---

## Known residual limitations (stated before the run, not after)

- **First-link selection** may pick an artifact the entry mentions only in passing rather than its principal output. This biases *against* both engines equally; it is a floor on measurable recall, not a differential advantage.
- **Session headings are written by the same author as much of the corpus**, so vocabulary overlap is higher than a naive third-party query would be. Both engines benefit; the comparison stays fair, but the absolute recall is optimistic relative to a stranger searching.
- **The corpus is markdown-only.** Retrieval over code, CSVs, or Pine is out of scope and unmeasured.

## Commit discipline

Committed **before** the harness runs. Results land in a separate artifact citing this file's commit hash.
