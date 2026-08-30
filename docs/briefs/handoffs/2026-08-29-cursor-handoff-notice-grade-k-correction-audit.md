# Claude Code / Cursor handoff — report-only Notice-log GRADUATE K-correction auditor

**Status:** **IMPLEMENTED — PR [#217](https://github.com/Joshua-Asante/first-passage/pull/217)** (`cursor/notice-grade-k-correction-audit`, merged 2026-08-30). Cursor returned **DONE_WITH_CONCERNS**; both concerns adjudicated by Claude Code before merge (`check_boundaries`/`repo_map_layers.yml` classification fixed; the `GRADUATE`-substring over-count in the informational scan-count line disclosed, not fixed — does not affect which rows are flagged). Real-corpus run confirmed exactly the 3 expected MNQ notices flagged. **DO NOT RE-DISPATCH.**
**Authority:** root-cause finding from this session's generate/evaluate multiplicity-accounting
work (commit `b7705895df1b21598fcb58ca2d908b6398977e34`, this branch). `promotion_packet.py` now
requires a K-conditional DSR-floor attestation before S5 promotion, but that gate sits downstream
of a pathway most candidates never reach: Notice-log `GRADUATE` routing has zero code check today.
This packet does not build a gate for that pathway (a blocking gate there is a bigger, judgment-
laden design decision, explicitly out of scope — see §5) — it builds a **read-only worklist** so
the operator can see, without hand-grepping, which `GRADUATE` verdicts cite a K above the DSR-
reachable band with no visible correction evidence.

**Layer:** one new standalone script + its test file. No `core/`, Pine, `dd_protection`, ADR,
`STATE.md`, `docs/SESSIONS.md`, `scripts/gates.yml`, or any existing script touched. Report-only —
writes nothing, blocks nothing, not wired into `make check` or the pre-commit hook. $0 spend beyond
the build itself.

---

## §0 — Rule 0 reads (this session, verified before this handoff was written)

- [`lab/discovery/promotion_packet.py`](../../../lab/discovery/promotion_packet.py) — anchor
  `b770589` (2026-08-29, this session). `_check_k_conditional_floor` is the pattern this packet's
  *read-only* check mirrors: `floor_at_k(K) > CAP` means K exceeds the DSR-reachable band. This
  packet does not import or call anything from `promotion_packet.py` — it only reuses the same
  arithmetic function from its actual source.
- [`lab/research_utils/axis_screen.py`](../../../lab/research_utils/axis_screen.py) — anchor
  `027a729` (2026-08-14). `CAP = 1.0` (frozen constant, harvest-intake ADR §5 — do not re-derive or
  hardcode a copy) and `floor_at_k(k: int) -> float` (verified this session: importable as
  `from research_utils.axis_screen import CAP, floor_at_k` with `lab/` on `sys.path`, exactly the
  pattern in [`scripts/beta_cohesion_read.py`](../../../scripts/beta_cohesion_read.py) lines 12-13:
  `REPO = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(REPO / "lab"))`).
- [`docs/notes/notice/`](../../../docs/notes/notice/) — 36 `N-*.md` files present as of this
  session's `git rev-parse HEAD` (`b770589`). Verified directly (not inherited from a paraphrase):
  only 6 of 36 contain the literal substring `discovery_manifests/` anywhere in the file body; 34 of
  36 contain a `**Status:**` line. Read all 6 manifest-citing files in full this session:
  [`N-2026-08-15-blind-channel-cost-geometry-and-first-candidate-kill.md`](../../notes/notice/N-2026-08-15-blind-channel-cost-geometry-and-first-candidate-kill.md),
  [`N-2026-08-29-mnq-bar-volume-regime.md`](../../notes/notice/N-2026-08-29-mnq-bar-volume-regime.md),
  [`N-2026-08-29-mnq-daily-range-persistence.md`](../../notes/notice/N-2026-08-29-mnq-daily-range-persistence.md),
  [`N-2026-08-29-mnq-gap-magnitude-rth-range.md`](../../notes/notice/N-2026-08-29-mnq-gap-magnitude-rth-range.md),
  [`N-2026-08-29-mnq-overnight-rth-range-transfer.md`](../../notes/notice/N-2026-08-29-mnq-overnight-rth-range-transfer.md)
  (anchor `6de26d5`, 2026-08-29),
  [`N-2026-08-29-mym-overnight-gap-joint-gate.md`](../../notes/notice/N-2026-08-29-mym-overnight-gap-joint-gate.md).
  Ground truth this packet's design depends on (§0.5 explains why each matters):
  - 3 of the 6 (`mnq-bar-volume-regime`, `mnq-gap-magnitude-rth-range`,
    `mnq-overnight-rth-range-transfer`) have `**Status:**` lines containing the literal word
    `GRADUATE`, and all three cite
    `discovery_manifests/mnq_dailygeom_notice_20260829.json` (a real, closed, `--lane blind`, `K=5`
    manifest — `floor_at_k(5)` computes above `CAP`, i.e. above the DSR-reachable band).
  - `mnq-daily-range-persistence` cites the SAME manifest but its `**Status:**` line reads `HELD
    until operator scope call` — no `GRADUATE`. Must NOT be flagged.
  - `blind-channel-cost-geometry-and-first-candidate-kill` cites a DIFFERENT, unrelated manifest
    (`disccamp0_gc_2010_18.json`) inside a markdown TABLE CELL, as a historical citation of a prior
    closed campaign — not a claim about this notice's own K. Its `**Status:**` line reads `HELD`.
    Must NOT be flagged.
  - `mym-overnight-gap-joint-gate` cites a third manifest (`mymdd_1_2026_08_29.json`) in body prose
    (`` `discovery_manifests/mymdd_1_2026_08_29.json`'s own `hypothesis` field lists exactly ``),
    not as a K claim. Its `**Status:**` line reads `HELD`. Must NOT be flagged.
- [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md) —
  routing: `scripts/` is not a locked surface (test 1 clear); the extraction rule and pass/fail
  arithmetic are both fully frozen below with a verified worked example (test 2 clear); one new
  file + one new test file — below the fleet threshold, so this is a **single Cursor handoff**, not
  a multi-packet fleet (`.claude/skills/cursor-fleet/SKILL.md` routing table: "One implementation
  build → Single Cursor handoff... Fleet overhead is pure waste at N=1"). A second candidate packet
  from this session's root-cause work (extending the closed-form K cross-check just built for
  `--tool stumpy` to `catch22`/`tsfresh`/`ruptures`) was investigated and **disqualified** before
  authoring this brief: real manifests show `--tool` is "nearest-available token," not a reliable
  discriminator (`disccamp0_gc_2010_18.json` is tagged `tool=catch22` but its true K derivation is
  the combined stumpy+catch22+ruptures formula; `ruptures`-tagged manifests in this repo are single
  frozen-cell `K=1` probes, not penalty-grid searches) — dispatching that packet as originally
  scoped would hand Cursor a spec whose premises don't hold, guaranteeing either a wrong
  implementation or a `NEEDS_CONTEXT` bounce. Not sent.
- No vendor data, no secrets, no gitignored bytes — pure stdlib + `research_utils.axis_screen` +
  markdown/JSON reads. Test 0: **N/A**.

---

## §0.9 — Phase-0 staleness check (run before touching anything)

```bash
# Confirm the script doesn't already exist under a different name (no-op condition).
find . -iname "*notice*grade*" -o -iname "*notice*k*audit*" 2>/dev/null | grep -v archive
# If a file already does this, STOP -- return DONE citing it, do not build a duplicate.

git log --oneline origin/main --since="24 hours ago" -- docs/notes/notice/ lab/discovery/promotion_packet.py lab/research_utils/axis_screen.py
# Confirm none of the cited anchors (b770589 / 027a729 / 6de26d5) have moved. If
# axis_screen.py's floor_at_k/CAP signature changed, re-verify the import still works before
# proceeding -- do not silently adapt to a different signature.

gh pr list --state open --search "notice audit OR grade OR k-correction"
```

If the staleness check finds nothing amiss, proceed. If `docs/notes/notice/` now contains new
`N-*.md` files not in this brief's count of 36, that is expected and fine — the script must operate
on whatever files exist at run time, not a hardcoded list.

---

## §0.5 — Ambiguity surfacing (read before executing)

None load-bearing. The extraction rule, the flag condition, and three known true positives / three
known true negatives are all given verbatim in §2 and §0 above. The one judgment-shaped question —
"should this also check whether a `promotion_packet` gate_attestation exists for the cited
`run_id`" — is explicitly answered **no** in §2: no such attestation can exist for a Notice-log
verdict (Notice-log routing has no packet at all), so the check is bounded to "K exceeds the
reachable band," full stop. Do not invent a stronger check.

---

## §1 — Context

This session's root-cause work found the pipeline has exactly one code-enforced multiplicity
checkpoint (`admission_schema.py`'s K≥4 refusal) and, as of commit `b770589`, a second one at S5
promotion (`promotion_packet.py`). Neither reaches the pathway most discovery candidates actually
travel: Notice-phase `GRADUATE` routing, which is asserted in prose in a Notice-log markdown file
with no code check before or after. Building a blocking gate there needs new lifecycle-admission
infrastructure and real design judgment (out of scope here — see §5). What's mechanical and
well-scoped instead: a **read-only script** that surfaces, as a worklist for the operator, every
`GRADUATE` verdict whose cited discovery manifest carries a K above the DSR-reachable band —
information that exists today but requires hand-grepping to see.

---

## §2 — Frozen scope

**Do — create exactly these two new files, edit nothing else:**

1. `scripts/audit_notice_grade_k_correction.py` — a standalone, report-only CLI script:

   - Add `lab/` to `sys.path` exactly as `scripts/beta_cohesion_read.py` does (§0 above); import
     `CAP, floor_at_k` from `research_utils.axis_screen`.
   - Glob `docs/notes/notice/N-*.md` (repo-relative to the script's own `Path(__file__).resolve().parent.parent`).
   - For each file: find the line matching `^\*\*Status:\*\*` (first match only). If that line does
     not exist, or does not contain the literal substring `GRADUATE`, skip this file entirely — do
     not scan its body for the word "GRADUATE" anywhere else (per §0's `blind-channel`/`mym`
     counter-examples, a stray mention elsewhere must not trip a false positive).
   - For files that pass the `GRADUATE` check: search the ENTIRE file body (not just the Status
     line) with the regex `discovery_manifests/[\w.-]+\.json` and collect every distinct match
     (case-sensitive, exact literal `discovery_manifests/` prefix — do not generalize to other
     directories).
   - For each distinct manifest filename found: resolve it relative to the repo root
     (`discovery_manifests/<match>`), skip with a `[skip] manifest not found: <path>` line to stderr
     if the file doesn't exist (do not hard-fail the whole run over one missing manifest), else load
     the JSON and read its `K` field. If `K` is missing or not a positive int, skip with a
     `[skip] no valid K in manifest: <path>` stderr line.
   - Compute `floor_at_k(int(K))`. If that value is `> CAP`, this is a flagged row: `{notice_file,
     manifest_path, K, floor_at_k(K)}`.
   - Print flagged rows as one line each to stdout, tab-separated, sorted by `notice_file`:
     `<notice_file>\t<manifest_path>\tK=<K>\tfloor_at_k(K)=<value rounded to 4 decimals>\tCAP=<CAP>`.
   - Print a one-line summary at the end: `[audit] N flagged / M GRADUATE notices scanned / T total notices`.
   - Exit code is always `0` — this is a report, never a gate. Do not `sys.exit(1)` on flagged rows.
   - No writes to any file. No mutation of any kind.

2. `tests/test_audit_notice_grade_k_correction.py` — using `tmp_path` fixtures (do NOT depend on
   the real `docs/notes/notice/` corpus for pass/fail assertions; the script's own repo-root
   resolution must be parameterizable or monkeypatched for tests, mirroring how
   `tests/test_register_search_stumpy_k_check.py` monkeypatches `register_search.LEDGER`).
   Required cases, each built as a synthetic fixture, not a copy of a real file:
   - A `GRADUATE` notice citing a manifest with K above the reachable band (e.g. K=5) →
     **flagged**.
   - A `GRADUATE` notice citing a manifest with K within the reachable band (e.g. K=2) → **not
     flagged**.
   - A `HELD` (non-GRADUATE) notice citing a high-K manifest → **not flagged** (mirrors the real
     `daily-range-persistence` counter-example in §0).
   - A `HELD` notice citing a high-K manifest inside a markdown table cell, where "GRADUATE"
     happens to appear elsewhere in the file's body prose (not the Status line) → **not flagged**
     (mirrors the real `blind-channel` / `mym` counter-examples in §0 — this is the single most
     important test in the file; get it wrong and the tool free-hallucinates positives).
   - A `GRADUATE` notice citing a manifest path that doesn't exist on disk → skipped with a stderr
     message, exit code still `0`, no crash.
   - A `GRADUATE` notice citing two distinct manifests → both checked independently.
   - Two `GRADUATE` notices citing the SAME manifest (mirrors the real 3-notices/1-manifest case in
     §0) → both appear as separate flagged rows.

**Do NOT:**

- Add this script to `scripts/gates.yml`, any pre-commit hook, or `make check` — it is a manually
  run report tool, not a new enforced gate. Adding a new gate to the hard-gate stack is a governance
  decision, not part of this packet.
- Touch `lab/discovery/promotion_packet.py`, `lab/discovery/register_search.py`,
  `lab/research_utils/axis_screen.py`, or any file under `docs/notes/notice/` — all are read-only
  inputs to this script.
- Build any blocking/refusing logic, or anything that writes back to a manifest or a notice file.
- Attempt to detect "was this K corrected" beyond the K-vs-floor check — no such correction field
  exists anywhere in a manifest or a Notice-log file today (see §0.5); do not invent one.
- Widen the regex to match manifest paths outside the literal `discovery_manifests/` directory, or
  to catch routing words other than the literal substring `GRADUATE`.

---

## §4 — Falsifiable hypothesis

**H:** a mechanical script can distinguish, using only the `**Status:**` line plus a loose
`discovery_manifests/*.json` path scan, the real `GRADUATE`-with-uncorrected-high-K cases in this
corpus (3 of 36 notices, today) from the superficially-similar non-cases (2 more notices that also
cite a `discovery_manifests/` path but are not `GRADUATE`, or cite it for an unrelated historical
reason) — without any manual judgment call.

**Falsifier / accept-reject:** **ACCEPT** (merge) if, run against this repo's real
`docs/notes/notice/` corpus at merge time, the script's output flags exactly the 3 today's-MNQ-batch
notices (`mnq-bar-volume-regime`, `mnq-gap-magnitude-rth-range`, `mnq-overnight-rth-range-transfer`)
and nothing else, AND every synthetic test in §2 passes. **REJECT** the dispatch (fall back to CC
solo) if it returns `NEEDS_CONTEXT` or `BLOCKED` twice, or if the real-corpus run produces a false
positive on `daily-range-persistence`, `blind-channel-cost-geometry`, or `mym-overnight-gap-joint-gate`
— that specific failure mode means the Status-line/body-text separation wasn't implemented as
frozen, not that the script needs a third try at a looser heuristic.

---

## §5 — Forbidden moves

- Wiring this script into `scripts/gates.yml`, pre-commit, or CI — out of scope, a governance
  decision for later.
- Building any gate for Notice-log `GRADUATE` routing itself (blocking, warning-that-blocks, or
  otherwise) — this packet is read-only reporting only.
- Editing any file under `docs/notes/notice/`, `lab/discovery/`, or `lab/research_utils/`.
- Editing any ADR, `STATE.md`, or `docs/SESSIONS.md` (orchestrator-reserved / locked surfaces).
- Scanning file body text for the word `GRADUATE` outside the `**Status:**` line (this is the exact
  mistake that would reintroduce the false-positive risk this packet exists to avoid).
- Adding a dependency beyond stdlib + `research_utils.axis_screen`.

---

## §6 — Return contract

Branch: `cursor/notice-grade-k-correction-audit`. One PR against `main`. Four-state status:

- **`DONE`** — both files created exactly as scoped, all §2 test cases pass, real-corpus run
  matches §4's exact 3-file expected output, no forbidden move triggered.
- **`DONE_WITH_CONCERNS`** — landed, but something about the regex/extraction felt fragile on an
  edge case not covered by §2's fixtures — flag exactly what, orchestrator adjudicates before merge.
- **`NEEDS_CONTEXT`** — a §0 anchor has moved in a way that changes the expected behavior, or the
  real-corpus run doesn't match §4's expected 3-file output — state the actual output found.
- **`BLOCKED`** — some other structural obstruction — state it plainly.

**Closure report format:**
```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED>
Branch: cursor/notice-grade-k-correction-audit
Diff (files touched): <must be exactly the two new files>
Real-corpus output: <paste the script's actual stdout when run against docs/notes/notice/>
Concerns (if any): <list>
```

---

## §10 — Audit hooks (orchestrator-side, after the packet returns)

```bash
# Diff touches exactly the two new files
git diff origin/main..cursor/notice-grade-k-correction-audit --name-only
# Expected: exactly scripts/audit_notice_grade_k_correction.py and
#           tests/test_audit_notice_grade_k_correction.py

# Tests pass
PYTHONPATH=lab python -m pytest tests/test_audit_notice_grade_k_correction.py -q

# Real-corpus run matches the exact expected 3-file output
PYTHONPATH=lab python scripts/audit_notice_grade_k_correction.py
# Expected: exactly 3 flagged rows, one per: mnq-bar-volume-regime, mnq-gap-magnitude-rth-range,
# mnq-overnight-rth-range-transfer -- all citing discovery_manifests/mnq_dailygeom_notice_20260829.json,
# K=5, floor_at_k(5) > CAP=1.0. Zero rows for daily-range-persistence, blind-channel-cost-geometry,
# or mym-overnight-gap-joint-gate.

# Not wired into the gate stack
grep -n "audit_notice_grade_k_correction" scripts/gates.yml .github/workflows/*.yml 2>/dev/null
# Expected: no match

# Import boundaries still clean
python scripts/check_boundaries.py
```

---

## Verification (parent-side, before declaring this handoff complete)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-08-29-cursor-handoff-notice-grade-k-correction-audit.md --type handoff
# Expected: well-formed (§0 cites repo paths with anchors; §4 carries H:/falsifier; §5 lists
# forbidden moves; §10 has a fenced hook; §6 carries the four-state taxonomy)
```
