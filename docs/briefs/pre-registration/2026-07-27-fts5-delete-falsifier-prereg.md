# Verdict pre-registration — FTS5-as-Delete falsifier (limb A of the Hermes adoption ruling)

**Status:** `FROZEN` — 2026-07-27, **BEFORE any index is built or any recall number is computed**
**Parent brief:** [`docs/briefs/programs/2026-07-27-hermes-agent-adoption-ruling.md`](../programs/2026-07-27-hermes-agent-adoption-ruling.md) §6 limb A
**Operator ruling:** limb A resolved `A3` (Delete) on 2026-07-27
**Bears on:** [`Q-XMEM-1`](../Q-XMEM-1-cross-surface-memory-sidecar-pilot.md) — whose own architecture stays frozen and untouched

---

## What is being tested, and what is not

**Tested:** whether deterministic verbatim search (SQLite FTS5) over session logs plus the 904-file markdown corpus retrieves prior work *well enough to remove the felt cost* that motivated `Q-XMEM-1` — i.e. whether the sidecar question can be **Deleted** rather than answered.

**Not tested:** whether a Mem0 extraction sidecar would work. `Q-XMEM-1`'s frozen v1.1 architecture is untouched by this file. A Delete that succeeds moots that question; a Delete that fails returns it intact. Neither outcome amends it.

**Why a comparator at all.** A Delete must beat *the thing it deletes work from*. Today's incumbent retrieval over this corpus is **ripgrep literal search** (plus the operator's memory of what exists). If FTS5 does not beat `rg` on the queries that actually matter — paraphrases, where the searcher does not recall the exact wording — then FTS5 is a reimplementation of the incumbent, adds a store to maintain, and Deletes nothing.

---

## Threshold correction being frozen here

The parent brief's first draft read: *"if recall on that fixture set is materially worse than the operator's own manual-search baseline."* That is unmeasurable (no such baseline exists as data) and is a Known-Trap-#5 vague gate. Frozen replacement below is binary and computable without the operator in the loop.

---

## Fixture construction (frozen — built mechanically, not hand-picked)

Hand-picking queries would let the fixture be tuned to the result. Construction rule, frozen before any query is written:

1. Enumerate markdown links in `lab/CATALOG.md`, `docs/briefs/INDEX.md`, and `docs/adr/INDEX.md` where the **link text is descriptive prose** (≥4 words, not a bare path/slug/date).
2. For each, the **query** is that descriptive link text with any literal slug, filename, ADR number, or date **stripped** — this is what makes it a paraphrase probe rather than an identifier lookup.
3. The **expected document** is the link target.
4. Drop any pair whose stripped query is <3 remaining words (too little signal to be a fair probe for *either* engine).
5. Take the **first N=20** surviving pairs in deterministic file order. If fewer than 15 survive, the fixture is too thin and the falsifier returns `AMBIGUOUS` rather than a verdict.

Both engines see the identical query string. No per-engine query tuning. FTS5 queries use the corpus's own tokenizer defaults; `rg` uses a literal-alternation of the same terms. Any deviation from this rule is recorded in the results as a protocol departure.

---

## §6 verdict table (frozen)

Let `R_fts5@5` and `R_rg@5` be recall-at-5 over the N pairs — the fraction of pairs whose expected document appears in that engine's top 5 results.

| Verdict | Trigger | Disposition |
|---|---|---|
| `DELETE-HOLDS` | `R_fts5@5 ≥ 0.70` **and** `R_fts5@5 > R_rg@5` | Delete is viable. Build the sidecar (search + staged write only). `Q-XMEM-1` becomes eligible to close `MOOT` — **still gated on the operator confirming the original cost no longer bites**, per parent §6 A3 |
| `DELETE-FAILS` | `R_fts5@5 < 0.70` **or** `R_fts5@5 ≤ R_rg@5` | Delete fails on its merits. Build nothing. `Q-XMEM-1` returns **intact and un-mooted**; A1/A2 become live options again; the embedder question legitimately reopens |
| `AMBIGUOUS` | Fewer than 15 fixture pairs survive construction | Fixture too thin to decide. Do not build; do not moot. Record and stop |

**0.70 rationale (frozen before measurement):** the sidecar's purpose is to stop prior work being missed. At `recall@5 = 0.70`, roughly one probe in three still misses — tolerable for an assistive search box, not for anything claiming to *remove* the cost. Below that, "search exists" would be doing rhetorical work the numbers do not support. The second limb (`> R_rg@5`) is the anti-reimplementation clause and is independent of the absolute level.

---

## Forbidden moves (frozen)

- **Tuning the fixture after seeing results** — construction is mechanical and frozen above; if it produces an awkward fixture, that is the finding.
- **Per-engine query rewriting** to flatter FTS5 (stemming one side only, dropping stopwords one side only).
- **Reporting `recall@k` for a `k` chosen after seeing the curve.** `k=5` is frozen. Other `k` values may be reported as context, never as the verdict.
- **Closing `Q-XMEM-1` `MOOT` on a `DELETE-HOLDS` result alone** — the A3 pre-condition (operator confirms the cost no longer bites) is separate and is not satisfied by a recall number.
- **Treating `DELETE-FAILS` as a reason to adopt Hermes.** The adoption ruling is independent; a failed Delete reopens `Q-XMEM-1`, nothing more.

---

## Commit discipline

This file is committed **before** the fixture is built and before any recall number exists. Results land in a separate artifact referencing this file's commit hash. Any threshold edit after the first measurement requires closing `AMBIGUOUS` and re-registering (Known Trap #12).
