# ADR 2026-05-23 — Relocate ECR pipeline to live_journal/
**Status:** Accepted - ECR pipeline relocated to live_journal/; companion CC handoff returned DONE with all sections RESOLVED.
**Decision date:** 2026-05-23
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## §0 Rule 0 reads

claude.ai cannot read the working tree directly; the reads below are CC's
PR #100 readout (2026-05-23) plus prior memory anchors. CC re-verifies
during execution Phase 0.

- PR #100 (commit d161850, "feat(ingest): ECR ingest pipeline v0.1 —
  Phase 0 complete, Phase 1 plumbing"), landed pre-2026-05-23.
- `signals/schema.py` (~495 lines) — SignalEvent model, nested
  signal/decision/context/outcome blocks, SCHEMA_VERSION = "0.1" with
  strict field validator.
- `counterfactuals/schema.py` — Counterfactual + CounterfactualAssumptions;
  imports ExitReason from signals.schema.
- `ingest/` — ingest.py, notion_client.py, pine_loader.py, transform.py,
  enum_maps.py. Wired together; 50/50 tests passing in `test_ingest.py`
  on Linux (the doc-claimed baseline); on Windows worktrees, 3
  `TestPhase0Falsifiers::test_F01_*` tests fail with CRLF/LF byte-identity
  mismatch (git autocrlf rewriting LF fixtures as CRLF on checkout) — a
  pre-existing environment artifact, not a regression, baseline-frozen
  for invariance testing.
- `data/signals/signals_YYYY-MM.jsonl` — monthly rotation (per signals/
  schema.py:3 comment).
- `data/ingest_runs/phase0_2026-05-21T214500Z_items2-5_resolution.md` —
  Phase 0 DONE record; Phase 1 awaiting Notion integration.
- `live_journal/scripts/journal_review.py` — predates the ECR pipeline,
  is not part of it, stays put.

## §1 Context

PR #100 landed the ECR pipeline at repo root. The prior "live_journal
absorbs ECR" directive (chat 2026-05-23) was authored against a stale
model assuming Phase 0 hadn't shipped — that misread is documented in
the same chat. The question post-PR-#100 is whether to accept root
layout or post-hoc relocate under live_journal/.

Decision: relocate. Reasoning:

- live_journal/ and ECR share mission: plan-adherence tracking.
  Reconciliation (journal_review.py) is the post-hoc side; ECR ingest
  is the forward-looking side of the same instrument.
- Root layout creates parallel top-level concerns for the same mission —
  organizational sprawl The Algorithm cuts against.
- Eventual ECR ↔ journal_review.py integration becomes a same-directory
  refactor rather than a cross-directory one.
- Phase 1 will land more code into whichever location exists. Relocating
  earlier moves less code than later.

## §2 Decision

Move five paths root → live_journal/:

    signals/             → live_journal/signals/
    counterfactuals/     → live_journal/counterfactuals/
    ingest/              → live_journal/ingest/
    data/signals/        → live_journal/data/signals/
    data/ingest_runs/    → live_journal/data/ingest_runs/
    data/counterfactuals/ → live_journal/data/counterfactuals/

(2026-05-23 execution-time amendment: `data/counterfactuals/` added to the
move list after Step 2.6 surfaced its existence as an empty placeholder
sibling to `data/signals/`. Per spec doc `docs/spec/pine_baseline_csv_format.md`
line 136, Pine emits counterfactual CSVs there; functionally it's ECR-pipeline
output, parallel to data/signals/. Joshua approved the scope extension inline.)

Update imports throughout:

    from signals.X         → from live_journal.signals.X
    from counterfactuals.X → from live_journal.counterfactuals.X
    from ingest.X          → from live_journal.ingest.X

Update hardcoded path references in code, configs (pyproject.toml,
.claude/commands/), and docs (CLAUDE.md, README.md) that point to the
five moved paths. JSONL records under data/signals/ and data/ingest_runs/
are immutable history — their embedded paths stay as-is.

## §3 Alternatives considered

**Accept root layout (zero-move path).** Cheaper now: no file moves,
no import updates. Rejected on Algorithm grounds — defers the sprawl
problem to a more expensive future move once Phase 1 adds more code.

**Move journal_review.py under signals/ or ingest/ instead.** Inverts
the consolidation: brings legacy under new. Rejected — the new pipeline
is well-named for its scope (signals, counterfactuals); the legacy is
well-named for its scope (reconciliation). The umbrella that fits both
is plan-adherence = live_journal/, not either child name.

**Defer until Phase 1 stabilizes.** Risk-mitigation argument: don't
touch working Phase 0 with Phase 1 pending. Rejected — Phase 1 adds
code into whichever location exists. Cheaper to relocate now (small
surface) than later (larger surface).

> **Note (2026-08-02) — this ADR is SPENT; retirement candidate, not a dormancy case.**
> §4 below is a **one-shot migration acceptance test** ("post-hoc relocation is
> test-neutral"), discharged when the relocation landed — not a standing revert trigger.
> Its subject matter is gone: the `ops/live_journal` estate was retired 2026-07-11
> ([`2026-07-11-ops-cfd-estate-retirement.md`](2026-07-11-ops-cfd-estate-retirement.md)), so
> the paths §4 names (`live_journal/signals/schema.py`, the Phase-0 resolution doc under
> `live_journal/data/ingest_runs/`) no longer exist and the pytest baseline it compares
> against is unreproducible. Nothing here needs re-arming — the hypothesis was answered.
> **Owed action:** route this ADR through `scripts/retire_adr.py` (operator-gated; that tool
> requires an `Accepted` successor declaring `Supersedes: <this> full`, which does not yet
> exist). Flagged by the 2026-08-02 falsifier-input reachability census; no §4 edit made.

## §4 Falsifiable hypothesis

H: Post-hoc relocation is test-neutral — every test that passed
pre-relocation passes post-relocation, every test that failed
pre-relocation fails identically (same failure shape), no new
failures, no skipped→passing or passing→skipped transitions. Data
records and locked schema invariants are byte-preserved.

- RESOLVED: post-relocation `pytest tests/ -v --tb=no -q` produces the
  SAME passed/failed/skipped test-name set as the pre-relocation
  baseline (Phase 0 captures the baseline before any move; the diff
  is empty modulo whitespace and timing), AND
  the Phase 0 resolution doc at
  `live_journal/data/ingest_runs/phase0_2026-05-21T214500Z_items2-5_resolution.md`
  is byte-identical to its pre-relocation form, AND
  `live_journal/signals/schema.py` SCHEMA_VERSION still equals "0.1".
- FALSIFIED: any test changes state (pass↔fail↔skip), OR any new test
  name appears that didn't exist pre-relocation (or vice versa), OR
  any data record byte-changed, OR SCHEMA_VERSION drifted, OR any
  moved file's content (other than import lines) changed.
- AMBIGUOUS: tests pass but a path reference is found post-relocation
  that the sweep missed (e.g., in a CI workflow file or a Notion sync
  config). Recoverable, but signals that §0.5 question coverage was
  incomplete.

Note on environment-dependent baselines: the 3 pre-existing
`TestPhase0Falsifiers::test_F01_*` failures on Windows worktrees
(CRLF/LF byte-identity) are baseline state, not relocation damage.
The invariance framing automatically handles this — those 3 tests
should fail identically pre- and post-relocation on Windows, and pass
identically on Linux. Either way the test-name set is preserved.

## §5 Forbidden moves

1. Schema redesign — SignalEvent and Counterfactual fields, nesting,
   validators stay byte-identical except for module-path-driven changes.
2. Rotation policy change — monthly stays monthly. (My earlier
   "delegated decision" advocating daily is moot; landed code wins.)
3. Merging with journal_review.py — they coexist under live_journal/.
   Integration is a separate ADR if/when needed.
4. SCHEMA_VERSION bump — stays "0.1". The strict validator hard-rejects
   any other value; bumping forks all existing records.
5. Rewriting existing JSONL records to "update" embedded paths — records
   are append-only history. Paths inside records stay as-is.
6. Touching live_journal/scripts/journal_review.py or
   live_journal/scripts/m7_anticipation_gap_backfill.py — separate
   workstream.

## §6 Gate criteria

This is a one-shot directory move. No long-term reversal trigger applies.
Closure marker: companion CC handoff returns DONE AND all §4 RESOLVED
conditions hold.

If §4 returns FALSIFIED, that opens a fresh investigation; this ADR
records the attempt and the finding. The ADR is not automatically
reversed — relocation under live_journal/ is still the right end state;
FALSIFIED means the execution path needs adjustment.

## §10 Audit hooks

    # Target directories present under live_journal/
    test -d live_journal/signals
    test -d live_journal/counterfactuals
    test -d live_journal/ingest
    test -d live_journal/data/signals
    test -d live_journal/data/ingest_runs
    test -d live_journal/data/counterfactuals

    # Root-level ECR directories absent
    test ! -d signals
    test ! -d counterfactuals
    test ! -d ingest
    test ! -d data/signals
    test ! -d data/ingest_runs
    test ! -d data/counterfactuals

    # No stale root-level imports anywhere outside archive
    ! grep -rn "^from signals\b\|^import signals$\|^from counterfactuals\b\|^import counterfactuals$\|^from ingest\b\|^import ingest$" \
        --include="*.py" --exclude-dir=archive --exclude-dir=.git

    # Schema version unchanged
    grep -q 'SCHEMA_VERSION = "0.1"' live_journal/signals/schema.py

    # Phase 0 resolution doc preserved at new path
    test -f live_journal/data/ingest_runs/phase0_2026-05-21T214500Z_items2-5_resolution.md

    # Test invariance: pre/post test-name set is identical
    # Phase 0 captures the baseline at the start, post-relocation diff
    # must be empty:
    #   pytest tests/ -v --tb=no -q | grep -E '^tests/.*(PASSED|FAILED|SKIPPED)' \
    #     | sort > /tmp/pre.txt   # before any move
    #   pytest tests/ -v --tb=no -q | grep -E '^tests/.*(PASSED|FAILED|SKIPPED)' \
    #     | sort > /tmp/post.txt  # after the move
    diff /tmp/pre.txt /tmp/post.txt   # exit 0 = invariance held
