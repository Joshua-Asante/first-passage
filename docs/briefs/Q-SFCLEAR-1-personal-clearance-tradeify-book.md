# Q-SFCLEAR-1 — Personal clearance of the Tradeify book at E_0 (rung R1)

**Status:** `OPEN` — pre-registration FROZEN 2026-10-11 (ratified by Joshua)
**Authored:** 2026-10-11
**Closed:** N/A
**Authors:** Joshua (rulings) + Claude Code (drafting worker for the Deployment Coordinator)
**Parent question:** N/A — owed item 1 of the [self-funded lane ADR](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#grounds), re-scoped by [addendum 2026-10-11b](https://github.com/Joshua-Asante/first-passage/blob/d7ad4d8d672790dfbe647b22fd9d75a95576f109/docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11b--tradeify-book-reused-on-the-personal-lane-supersedes-the-option-c-split) (PR #784)
**Supersedes:** [Q-SFGROWTH-1](Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md) for the personal lane (PR #752, re-scoped)
**Loop:** Inquire-phase Pre-Q — closure is gated by the [verdict pre-registration](pre-registration/Q-SFCLEAR-1-verdict-preregistration.md)
**Artifact path:** `docs/briefs/Q-SFCLEAR-1-personal-clearance-tradeify-book.md`

---

## §0 — Rule 0 reads (production-source verification)

The [pre-registration §0](pre-registration/Q-SFCLEAR-1-verdict-preregistration.md#0--reads) lists every read. Load-bearing: `ops/c1_rail/book_policy.py` (`LegSize`, `AddsRule`, `validate_size_vector`, `require_policy`) and `ops/c1_rail/qualification/contract.py` (`canonical_json_bytes`) at `origin/main@2cfb3d7`; `discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json` (K = 9); the private pre-screen folder, read in place and hash-verified.

**Dedup:** Q-SFGROWTH-1 is the only prior personal-lane study; this ID re-scopes it (no other study tests the book at `E_0`). The T00 step-3 Tradeify screen (#733) tests a different account and does not clear this lane.

---

## §1 — Context & motivation

Joshua ruled on 2026-10-11 to reuse the Tradeify book on the personal account and qualify its sizing at `E_0` (ADR addendum 2026-10-11b). The zero-K pre-screen found the retained FLOOR-HALF configuration (R0) fails at least one binding pre-screen gate at `E_0` (gate-level standing private); Joshua then ruled R1 (R0 with adds OFF on Striker and Vanguard, ORB OFF) and the gates, buffer, personal policy and routes ("confirm O2, accept all recommendations, go with R1"). [Pre-registration §1](pre-registration/Q-SFCLEAR-1-verdict-preregistration.md#1--context-and-operator-rulings) records them.

**Why a new ID rather than editing Q-SFGROWTH-1 in place:** Q-SFGROWTH-1 is a selection over a searched grid with an Explore/Confirm out-of-sample design and a frozen baseline whose text is immutable; Q-SFCLEAR-1 is a single-tuple clearance on fully exposed history. Keeping one ID per design keeps K, exposure and verdict semantics unambiguous. #752 carries both: its Q-SFGROWTH-1 files now point here.

---

## §2 — Prior art / lineage

- [Q-SFGROWTH-1](Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md): never ran; no data or K consumed. Kept and cited from `b02c173`: §C statistic, F6, F7, F9, and the classification of the book legs ([Phase 0](../../lab/analysis/c1/sfgrowth_2026-10/PHASE0_SIZING_CLASSIFICATION.md)). Dropped: K = 2,375, NAS leg 5, structural-zero artifacts, Explore/Confirm, F8.
- T00 book lineage manifest: trial 9 is FLOOR-HALF under #733; R1 would be one further trial.
- Plan #785 (head `7d2ce02`): the sizing frame, pre-screen and clearance tests this pre-registration freezes.

---

## §3 — Question (Q-SFCLEAR-1)

**Q-SFCLEAR-1:** Does the Tradeify book at rung R1, under the personal policy P0, meet the personal lane's drawdown, growth and margin standards at `E_0` on the exposed history?

---

## §4 — Falsifiable hypothesis (H-SFCLEAR-1)

**H-SFCLEAR-1:** If the book at R1 under P0 is fit for the personal account, then hits ≤ 100/10,000 in all 18 drawdown cells (seeds 42/123/2026 × c ∈ {1, 1.5} × FULL/H1/H2), pooled median terminal > `E_0` at c = 1.5 in FULL, H1 and H2, and the B2 margin check passes.

**Accept H-SFCLEAR-1 if:** the pre-registration §6 RESOLVED row holds.
**Reject H-SFCLEAR-1 if:** any binding cell fails (NOT CLEARED).

---

## §5 — Forbidden moves

- Running any export, replay or scoring at a personal configuration before ratification.
- Changing R1, a gate, a cell or a window after any `E_0` scoring output.
- Walking to another rung after R1 fails.
- Treating the result as out-of-sample or as Tradeify-screen evidence.
- Publishing `E_0`, per-leg quantities or `E_0`-linked ratios.

The pre-registration §5 holds the full list.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Pre-registration §6 RESOLVED row | `INTEGRATE — R1 is the personal sizing binding; label "clears on exposed history (model-fitted)"; plan §8 gates remain` |
| `NOT CLEARED` | Any binding cell fails | `STOP — no automatic second rung; a new rung needs a new ruling, trial and freeze` |
| `VOID` | Pre-registration §6 VOID row | `ITERATE — fix the input and rerun the same frozen design` |

---

## §7 — Execution plan

1. Ratification (pre-registration §12).
2. Build: P0 policy path, personal replay path, Tradovate fee input, #782/#783 re-pin and verification (plan rows 1.2, 2.2).
3. FG PASS (pre-registration §7), including D8.
4. Run locally (plan row 1.3); verdict mechanically, VOID first; closure under `docs/briefs/closures/`.

---

## §8 — Verdict pre-registration

[`docs/briefs/pre-registration/Q-SFCLEAR-1-verdict-preregistration.md`](pre-registration/Q-SFCLEAR-1-verdict-preregistration.md)

Pre-registration commit hash: `734d108efdc4f83234136ad3d4130a1aecc8996b` (freeze commit; status line only)
Pre-registration date: 2026-10-11 (FROZEN). Joshua, 2026-10-11, directly to the Deployment Coordinator: "confirm the §1 rulings, ratify Q-SFCLEAR-1". The R1 trial (trial 10, K 9 → 10) and four exposure-log entries are in `discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json`.

---

## §9 — Closure record format

`docs/briefs/closures/Q-SFCLEAR-1-closure-<verdict>.md`: every binding cell against its threshold, the sensitivities, the frozen tuple hash, and the typed `## Iterate` block.

---

## §10 — Audit hooks (runnable, not vague)

```bash
git log -1 --format=%h -- ops/c1_rail/book_policy.py ops/c1_rail/qualification/contract.py discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json
git log --format='%h %cI' -- docs/briefs/pre-registration/Q-SFCLEAR-1-verdict-preregistration.md | tail -1
rg -n 'Q-SFCLEAR-1' discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-SFCLEAR-1-personal-clearance-tradeify-book.md --type inquire
python scripts/check_brief.py docs/briefs/pre-registration/Q-SFCLEAR-1-verdict-preregistration.md
```
