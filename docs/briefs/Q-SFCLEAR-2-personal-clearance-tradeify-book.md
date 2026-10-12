# Q-SFCLEAR-2 — Personal clearance of the Tradeify book at E_0 (rung R1), successor

**Status:** `OPEN — DRAFT (pre-ratification)` — the verdict pre-registration is DRAFT — NOT RATIFIED; nothing runs before its §12 freeze
**Authored:** 2026-10-11
**Closed:** N/A
**Authors:** Joshua (rulings) + Claude Code (drafting worker for the Deployment Coordinator)
**Parent question:** N/A — owed item 1 of the [self-funded lane ADR](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#grounds), re-scoped by [addendum 2026-10-11b](https://github.com/Joshua-Asante/first-passage/blob/d7ad4d8d672790dfbe647b22fd9d75a95576f109/docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11b--tradeify-book-reused-on-the-personal-lane-supersedes-the-option-c-split) (PR #784)
**Supersedes:** [Q-SFCLEAR-1](Q-SFCLEAR-1-personal-clearance-tradeify-book.md) (SUPERSEDED-BEFORE-RUN 2026-10-11), which re-scoped [Q-SFGROWTH-1](Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md) (PR #752)
**Loop:** Inquire-phase Pre-Q — closure is gated by the [verdict pre-registration](pre-registration/Q-SFCLEAR-2-verdict-preregistration.md)
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

**Accept H-SFCLEAR-2 if:** the pre-registration §6 RESOLVED row holds.
**Reject H-SFCLEAR-2 if:** any binding cell fails (NOT CLEARED).

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
| `RESOLVED` | Pre-registration §6 RESOLVED row | `INTEGRATE — R1 is the personal sizing binding; label "clears on exposed history (model-fitted)"; plan §8 gates remain` |
| `NOT CLEARED` | Any binding cell fails | `STOP — no automatic second rung; a new rung needs a new ruling, trial and freeze` |
| `FREEZE INVALID` | Pre-registration §6 FREEZE INVALID row (evaluated first) | `No run — only a new pre-registration cures a defective freeze` |
| `VOID` | Pre-registration §6 VOID row | `ITERATE — fix the input and rerun the same frozen design` |

---

## §7 — Execution plan

1. Ratification (pre-registration §12): the G1/G3 calculator bound by sha256 in a committed draft; Joshua's rulings on the step-1 drafting choices, his recorded full tuple re-hash and his ratification words naming that draft commit; then the private freeze record (G1/G3 cells, Vanguard-drift re-check, roll-date list hash), pinned in a freeze commit that changes only the Status line and carries the exposure attestation, including Joshua's re-confirmation knowing the disclosed T00 step-3 exposure.
2. Build: P0 policy path, personal replay path consuming the bound schedule, Tradovate fee input, #782/#783 re-pin and verification (plan rows 1.2, 2.2).
3. FG PASS (pre-registration §7), including D8.
4. Run locally (plan row 1.3); outputs under the private root `C:\Users\joshu\t00-step3-console\sfclear2-run-<UTC>\`, with a committed run record under `lab/analysis/c1/sfclear_2026-10/run_records/` (pre-registration §7); verdict mechanically, VOID first; closure under `docs/briefs/closures/`.

---

## §8 — Verdict pre-registration

[`docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md`](pre-registration/Q-SFCLEAR-2-verdict-preregistration.md)

Pre-registration commit hash: pending (DRAFT — NOT RATIFIED; the freeze commit is recorded here in a later metadata commit)
Pre-registration date: pending

---

## §9 — Closure record format

`docs/briefs/closures/Q-SFCLEAR-2-closure-<verdict>.md`: the verdict label, any VOID reason, each binding cell's pass/fail standing, the frozen tuple hash, the hashes of the private run and cell records, and the typed `## Iterate` block. Cell values, the sensitivities, the residual reports and the drift values stay private (pre-registration §6).

---

## §10 — Audit hooks (runnable, not vague)

```bash
git log -1 --format=%h -- ops/c1_rail/book_policy.py ops/c1_rail/qualification/contract.py ops/calendars discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json
python -I scripts/fp.py python lab/analysis/c1/sfclear_2026-10/build_historical_schedule.py --check   # expect ab44fada…d473 MATCH
sed -n 's/^Pre-registration commit hash: `\([0-9a-f]\{40\}\)`.*/\1/p' docs/briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md   # empty until frozen; then pre-registration §10 hook 4
```

---

## Verification

```bash
python -I scripts/fp.py python .claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md --type inquire
python -I scripts/fp.py python .claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
```
