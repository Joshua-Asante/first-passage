# Closure — Hermes Agent adoption ruling: `RESOLVED-NO-GO`

**Verdict:** `RESOLVED-NO-GO` — ratified by the operator 2026-07-27 (chat directive: "ratify the NO-GO")
**Parent brief:** [`2026-07-27-hermes-agent-adoption-ruling.md`](../programs/2026-07-27-hermes-agent-adoption-ruling.md)
**Decision record (canonical):** [`docs/adr/2026-07-27-hermes-agent-adoption-nogo.md`](../../adr/2026-07-27-hermes-agent-adoption-nogo.md) (`Accepted`)

---

## §6 gate, fired

`RESOLVED-NO-GO` required: the operator reviews the 19-candidate slate and names **no** candidate meeting all three §4 falsifier conditions, **and** limbs A + B are dispositioned. Both satisfied — limb B's disposition is "execute in-stack", with its remaining execution re-homed (below) rather than silently dropped.

No candidate was named. The decisive fact was §1 correction (a): once Question 0 was read as a dispatch-environment test rather than an egress rule, condition (b) — *not deliverable by CC-local* — failed for every survivor.

## Anchor numbers vs gate thresholds

| Limb | Threshold (frozen) | Measured | Result |
|---|---|---|---|
| A — FTS5 recall floor | `R_fts5@5 ≥ 0.70` | **0.718** (84/117) | PASS by **2 pairs**; Wilson CI [0.630, 0.792] **straddles the floor** |
| A — beats incumbent | `R_fts5@5 > R_rg@5` | 0.718 vs **0.222** (3.23×, z≈8.8) | PASS, decisive |
| A — fixture floor | `N ≥ 15` | v1 **0**, v2 **117** | v1 `AMBIGUOUS`; v2 valid |

## What the pre-registration predicted vs what happened

**v1 predicted a measurable fixture and got none.** It froze a construction rule assuming ≥4-word descriptive markdown link text in `lab/CATALOG.md` and the two INDEX files. Those files carry **zero** links and 1–2 word identifiers respectively. Fixture size **0** → `AMBIGUOUS`, no number computed. The defect was in the pre-registration, not the corpus.

**v2 predicted viability and got it, by measuring first.** Its procedural correction — verify every structural assumption *before* freezing — also **rejected the operator-suggested source** (brief bodies: 758 one-word link texts across 134 files, exactly one with ≥4 words) before it could produce a second empty fixture. Had v2 frozen on brief bodies as the plan implied, it would have returned a second `AMBIGUOUS`.

**The verdict landed where the design intended but weaker than hoped.** `DELETE-HOLDS` on point estimates, with limb 1 statistically indistinguishable from its floor. Real-usage testing then reproduced that weakness in the field: 6 natural-language queries, strong on paraphrase, but one clear miss on a document that exists in the cold store (`"five minute"` cannot reach `5m` through verbatim FTS5), and a nonsense control returning four confident hits with no "nothing here" signal.

## Limb dispositions

- **Limb A = `A3` (Delete).** `Q-XMEM-1` **neither amended nor re-instrumented**; its frozen v1.1 architecture is untouched and it **remains OPEN**. `DELETE-HOLDS` makes it *eligible* to close `MOOT` only on a separate operator confirmation that the original cost no longer bites — not supplied by a recall number, and limb 1's 2-pair margin argues for wanting it explicit. Sidecar built: [`ops/recall/`](../../../ops/recall/).
- **Limb B = execute in-stack.** B2 (record the scoped negative ruling) is **discharged** by the ADR. B1 (promote the quarterly Sentinel full-run to a committed named workflow) is **not started** and is re-homed below.

## Obligations this brief hosted — re-homed, not dropped

Closing a brief must enumerate what it was carrying, or the obligations die with it:

| Obligation | New home |
|---|---|
| Limb B1 — promote the quarterly Sentinel run to a committed named workflow | `STATE.md` forward board |
| `Q-XMEM-1` `MOOT`-eligibility (operator confirmation) | `Q-XMEM-1` stays OPEN on the Q-roster; unchanged |
| Import Hermes's fail-closed cron semantics | Rides limb B1 |
| Re-measurement gate on any further retrieval tuning | [FTS5 RESULTS](../../../lab/analysis/harvest/fts5_delete_falsifier_2026-07-27/RESULTS.md) + v2 pre-registration forbidden-moves |

## Lesson candidates

1. **Trap #13 recurred inside a brief that cites Trap #13.** The v1 pre-registration specified word counts, strip lists, deterministic ordering and `N=20` while resting on an unchecked assumption about link shapes in three named files. One `grep` before freezing would have caught it. *Candidate rule: a construction rule must report the yield of its own sources before it is frozen.* Status: **candidate** — one dated incident, no dollar anchor.
2. **Judge-panel conclusions were relayed as findings before their sources were opened.** Both premise corrections were cheap to verify and were reported wrong first. Reinforces the existing `verify_source_not_label` lesson rather than adding a new one.
3. **A generated-view regenerator can destroy committed metadata from a partial checkout.** `archive_lab_analysis.py --regenerate-catalog` run from a worktree rewrites the heavy column of ~6 unrelated rows to `—`; the freshness gate only WARNs, so it commits clean and reviews clean. Captured in agent memory; *candidate for `docs/methodology/lessons/` if it recurs on a second generator* (`instrument_profiles.py` and `check_adr_graph.py --regenerate-index` share the shape and are unaudited for it).

## Verification

```bash
python scripts/check_brief.py docs/briefs/programs/2026-07-27-hermes-agent-adoption-ruling.md --type brief
python scripts/check_adr_graph.py
python -m pytest tests/ops/test_recall_guard.py tests/ops/test_recall_index.py lab/codification/tests/test_lint_controls.py -q
python lab/analysis/harvest/fts5_delete_falsifier_2026-07-27/falsifier_v2.py .   # reproduces 0.718 / 0.222
```
