# Q-SFCLEAR-2 — Personal clearance of the Tradeify book at E_0 (rung R1), successor

**Status:** `SUPERSEDED-BEFORE-RUN 2026-10-13` — parent brief of [Q-SFCLEAR-3](pre-registration/Q-SFCLEAR-3-verdict-preregistration.md) (FROZEN 2026-10-14 at F₃ `15bea25`), which incorporates this study's pre-registration at F `83867f0` except where its §S changes it; nothing was scored, exported or replayed under F; no run record, no verdict
**Authored:** 2026-10-11
**Closed:** 2026-10-13 for Q-SFCLEAR-2 (superseded before run); Q-SFCLEAR-3 is open under this brief
**Authors:** Joshua (rulings) + Claude Code (drafting worker for the Deployment Coordinator)
**Parent question:** N/A — owed item 1 of the [self-funded lane ADR](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#grounds), re-scoped by [addendum 2026-10-11b](https://github.com/Joshua-Asante/first-passage/blob/d7ad4d8d672790dfbe647b22fd9d75a95576f109/docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11b--tradeify-book-reused-on-the-personal-lane-supersedes-the-option-c-split) (PR #784)
**Supersedes:** [Q-SFCLEAR-1](Q-SFCLEAR-1-personal-clearance-tradeify-book.md) (SUPERSEDED-BEFORE-RUN 2026-10-11), which re-scoped [Q-SFGROWTH-1](Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md) (PR #752)
**Loop:** Inquire-phase Pre-Q — closure is gated by the [Q-SFCLEAR-3 verdict pre-registration](pre-registration/Q-SFCLEAR-3-verdict-preregistration.md); the [Q-SFCLEAR-2 pre-registration](pre-registration/Q-SFCLEAR-2-verdict-preregistration.md) at F governs where Q-SFCLEAR-3 §S does not change it
**Artifact path:** `docs/briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md`

---

## §0 — Rule 0 reads (production-source verification)

The [pre-registration §0](pre-registration/Q-SFCLEAR-2-verdict-preregistration.md#0--reads) lists every read. Load-bearing: `ops/c1_rail/book_policy.py`, `ops/c1_rail/qualification/contract.py`, the calendar sources under `ops/calendars/` and TB-S3 §5, `ops/c1_signal_daemon/book_adapters.py:150-153,175` at `origin/main@b6fff02`; the lineage manifest; the private pre-screen and fact-finding folders, read in place and hash-verified, and the private rulings record (pre-registration §D).

**Dedup:** Q-SFCLEAR-1 (superseded before run) and Q-SFGROWTH-1 (superseded) are the only prior personal-lane studies; neither ran. The T00 step-3 Tradeify screen (#733) tests a different account and does not clear this lane; its result was opened 2026-10-11T23:39:57Z, after every sizing ruling here and before ratification (label `NO-GO-evidence-UNDETERMINED-dependent`; disclosed exposure, pre-registration §D).

---

## §1 — Context & motivation

Q-SFCLEAR-1 was frozen on 2026-10-11 without the operator tuple re-hash its own freeze procedure required, and Codex review 5484097066 on #752 found ten more defects: a public gate-standing sentence, no historical session schedule, a chronology hook bound to the wrong commit, a lower-bound Vanguard stop risk under ceiling gates, Striker's guard classification, Aegis commission scaling, uncounted screened alternatives, and three stale status surfaces. Nothing had run. Joshua ruled (2026-10-11): "accept all four, have the worker draft the successor". The four rulings fix Vanguard's G1/G3 bound, Striker's guard wording and route, the historical schedule, and K = 12 ([pre-registration §1](pre-registration/Q-SFCLEAR-2-verdict-preregistration.md#1--context-and-rulings)). Frozen text is never edited, so the fixes need a successor ID. Joshua then ruled (2026-10-11, verbatim): "go with option 1, accept the E_0 bound" — gate standings and the `E_0` range they imply may be public; the exact value stays private.

---

## §2 — Prior art / lineage

- [Q-SFCLEAR-1](Q-SFCLEAR-1-personal-clearance-tradeify-book.md): same question and the same R1 tuple (sha256 `62d7ae19…671f`); freeze `734d108` void; nothing ran. Its rulings carry forward.
- [Q-SFGROWTH-1](Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md): never ran; cited from `b02c173` for §C, F6, F7, F9 and the [Phase-0 classification](../../lab/analysis/c1/sfgrowth_2026-10/PHASE0_SIZING_CLASSIFICATION.md).
- T00 book lineage manifest: K = 12 (trial 10 = R1, carried; trials 11–12 = screened alternatives R1′ and R2).
- Plan #785 (head `7d2ce02`): the sizing frame, pre-screen and clearance tests.

---

## §3 — Question (Q-SFCLEAR-2)

**Q-SFCLEAR-2:** Does the Tradeify book at rung R1, under the personal policy P0, meet the personal lane's drawdown, growth and margin standards at `E_0` on the exposed history?

---

## §4 — Falsifiable hypothesis (H-SFCLEAR-2)

**H-SFCLEAR-2:** If the book at R1 under P0 is fit for the personal account, then hits ≤ 100/10,000 in all 18 drawdown cells (seeds 42/123/2026 × c ∈ {1, 1.5} × FULL/H1/H2), pooled median terminal > `E_0` at c = 1.5 in FULL, H1 and H2, G1 and G3 hold on the §3 bound, and the B2 margin check passes.

Q-SFCLEAR-3 tests it as H-SFCLEAR-3: the same binding cells, with the 15:55 flatten placed by the convention's R1 run (§S row 1), data-exclusion zero days (§S row 1b) and G1/G3 from its own freeze record ([Q-SFCLEAR-3 §4](pre-registration/Q-SFCLEAR-3-verdict-preregistration.md#4--hypothesis-and-clearance-tests)).

**Accept H-SFCLEAR-3 if:** the Q-SFCLEAR-3 §6 RESOLVED row holds.
**Reject H-SFCLEAR-3 if:** any binding cell fails (NOT CLEARED).

---

## §5 — Forbidden moves

- Running any export, replay or scoring at a personal configuration before the freeze.
- Changing R1, a gate, the G1/G3 bound, the schedule, a cell or a window after any `E_0` scoring output.
- Walking to another rung after R1 fails.
- Treating the result as out-of-sample or as Tradeify-screen evidence.
- Publishing the exact `E_0`, per-leg quantities or any number from which `E_0` follows exactly.

The pre-registration §5 holds the full list.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Pre-registration §6 RESOLVED row | `INTEGRATE — R1 is the personal sizing binding; label "clears on exposed history (model-fitted; 15:55 flatten at the R1 adverse intrabar placement)" (Q-SFCLEAR-3 §S row 3); plan §8 gates remain` |
| `NOT CLEARED` | Any binding cell fails | `STOP — no automatic second rung; a new rung needs a new ruling, trial and freeze` |
| `FREEZE INVALID` | Pre-registration §6 FREEZE INVALID row (evaluated first) | `No run — only a new pre-registration cures a defective freeze` |
| `VOID` | Pre-registration §6 VOID row | `ITERATE — fix the input and rerun the same frozen design` |

---

## §7 — Execution plan

The pre-registration in force is [Q-SFCLEAR-3](pre-registration/Q-SFCLEAR-3-verdict-preregistration.md) (§S row 9, §12).

1. Ratification and freeze: done (Q-SFCLEAR-2 F `83867f0`, 2026-10-12; superseded before run 2026-10-13; Q-SFCLEAR-3 F₃ `15bea25`, 2026-10-14, with its own private freeze record).
2. Build: run-path cards A–D built (#821, #827, #833, #840); card B amendment (c) (R1 15:55 placement, §4-A data-exclusion days) and card E (#839) land before FG.
3. FG PASS (Q-SFCLEAR-2 §7 items 1–3 plus Q-SFCLEAR-3 items 5 and 6), including D8.
4. Run locally or on the §60 VM (addendum 2026-10-14); outputs under the private root `C:\Users\joshu\t00-step3-console\sfclear2-run-<UTC>\` (card E), with a committed run record under `lab/analysis/c1/sfclear_2026-10/run_records/` descending from F₃ (Q-SFCLEAR-3 §S row 8); verdict mechanically, FREEZE INVALID then VOID first; closure `docs/briefs/closures/Q-SFCLEAR-3-*`.

---

## §8 — Verdict pre-registration

[`docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md`](pre-registration/Q-SFCLEAR-2-verdict-preregistration.md) (superseded before run)

[`docs/briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md`](pre-registration/Q-SFCLEAR-3-verdict-preregistration.md) (in force; incorporates the file above at F except where its §S changes it)

Pre-registration commit hash: `83867f0d362931c2a516a62b990bb1c209372527` (freeze commit F, 2026-10-12; ratified draft `b97beaa613f7cd7fbdc2d89d7a7191a0274ea99a`)

Q-SFCLEAR-3 pre-registration commit hash: `15bea250fc8ee9a57b59735c9e8be685c4ddbf22` (freeze commit F₃, 2026-10-14; ratified draft `235f523418119e3aa0c16060465c27d7ff5cadee`; supersedes F before any run)
Pre-registration date: 2026-10-12 (frozen); Q-SFCLEAR-3 2026-10-14 (frozen)

---

## §9 — Closure record format

`docs/briefs/closures/Q-SFCLEAR-3-closure-<verdict>.md` (Q-SFCLEAR-3 §S row 8; Q-SFCLEAR-2 gets no closure): the verdict label, any VOID reason, each binding cell's pass/fail standing, the frozen tuple hash, the hashes of the private run and cell records, and the typed `## Iterate` block. Cell values, the sensitivities, the residual reports and the drift values stay private (pre-registration §6).

---

## §10 — Audit hooks (runnable, not vague)

```bash
git log -1 --format=%h -- ops/c1_rail/book_policy.py ops/c1_rail/qualification/contract.py ops/calendars discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json
python -I scripts/fp.py python lab/analysis/c1/sfclear_2026-10/build_historical_schedule.py --check   # expect ab44fada…d473 MATCH
sed -n 's/^Pre-registration commit hash: `\([0-9a-f]\{40\}\)`.*/\1/p' docs/briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md   # F (superseded before run); Q-SFCLEAR-2 §10 hook 4
sed -n 's/^Q-SFCLEAR-3 pre-registration commit hash: `\([0-9a-f]\{40\}\)`.*/\1/p' docs/briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md   # F₃; then Q-SFCLEAR-3 §10 hooks 4 and 4b
```

---

## Verification

```bash
python -I scripts/fp.py python .claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md --type inquire
python -I scripts/fp.py python .claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
```
