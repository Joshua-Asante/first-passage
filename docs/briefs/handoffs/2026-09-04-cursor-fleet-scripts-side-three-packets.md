# Cursor fleet — three `scripts/`-side packets (certification-power calculator · same-day letter order check · `repo_hygiene` without `gh`)

**Status:** **QUEUED — dispatch-moment gate passed 2026-09-04 (main `ba713ee`, open PRs #297 and #301 touch none of these footprints). Workers: fire per packet appendix (A/B/C); the orchestrator integrates.**
**Type:** Cursor handoff (fleet umbrella; three packet appendices)
**Authority:** the seven-strategy Select campaign record, [`campaign state`](../programs/2026-09-03-seven-strategy-select-campaign-state.md) —
§27a/§31a/§33c (three hand-computed sizing tables, two withdrawn under Codex review), §36 P3 (a same-day
`SESSIONS` letter filed out of order passed the `sessions-order` gate), and the post-merge checklist run of
2026-09-04 (`scripts/repo_hygiene.py` crashed on a container without `gh`). Fleet protocol:
[`cursor-fleet`](../../../.claude/skills/cursor-fleet/SKILL.md) under the
[CC/Cursor surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md).

**Layer:** `scripts/` governance tools and their tests only. **No** `core/`, Pine, `dd_protection`, ADR,
`STATE.md`, `docs/SESSIONS.md`, `scripts/gates.yml`, `Makefile`, or any campaign artifact is touched by any
packet. Nothing is wired into a gate. $0 spend beyond the builds. Three packets, **disjoint file footprints**,
each independently mergeable.

---

## §0 — Rule 0 reads (this session, verified before this brief was written)

- [`scripts/roll_sessions.py`](../../../scripts/roll_sessions.py) — `check_order` (line ~976) runs four passes:
  separator structure, duplicate lettered labels, **full-file calendar-date monotonicity**, and top-window
  author-time order via git. **No pass consults the same-day letter.** `_reorder_entries` keeps on-disk order
  inside a date group whenever any entry's author time is unresolved (`_FILEPOS`). That is exactly how
  `2026-09-04d, b, c, a` passed the gate on 2026-09-04 (campaign state §36 P3).
- [`tests/test_roll_sessions.py`](../../../tests/test_roll_sessions.py) — helpers `_entry`, `_doc`, `_write`,
  `_repo_with_history`, `_titles`; the test style packet B must match.
- [`scripts/repo_hygiene.py`](../../../scripts/repo_hygiene.py) — `_run()` (line ~64) calls
  `subprocess.run(args, …)` with no `FileNotFoundError` guard; `build_report()` (line ~216) probes
  `["gh", "--version"]` through it. On a host without `gh` the probe raises instead of setting
  `report.gh_available = False`, and the already-written "gh not on PATH" warning branch is never reached.
- [`REPO_MAP.md`](../../../REPO_MAP.md) scripts table — every `scripts/*.py` needs a row (a test enforces it);
  `scripts/repo_hygiene.py`'s row is the pattern for a manual-only governance script.
- [`scripts/check_brief.py`](../../../scripts/check_brief.py) — this brief's own well-formedness gate.
- Campaign state §31a/§33c — the identity every sizing number in packet A rests on: the one-sided 95% CP
  upper bound on the bust rate is ≤ ceiling **iff** `BinomCDF(k; n, ceiling) ≤ α`; certification power at true
  rate `p` is `BinomCDF(k_max; n, p)`; joint power over `L` limbs is `q^L` under independence and
  `max(0, 1 − L(1 − q))` with no dependence assumption (Fréchet).

## §0.5 — Ambiguity surfacing (read before executing)

Recommended defaults, so no worker bounces `NEEDS_CONTEXT` on a routine choice:

- **A — search grid.** The campaign tables were computed on an `n` grid of **10**. The calculator's default is
  `--step 10` so the pinned numbers reproduce exactly; `--step 1` is allowed and gives ≤ the grid answer.
- **A — no certifying count exists.** `max_certifying_busts` returns `-1` (not an exception); power is then 0.
- **B — unlettered entry.** A heading with no letter is letter `a` (matches `archived_letters_for_date`).
- **B — scope.** The packet adds a **check** only; it does not change `_reorder_entries` / `--normalize`.
- **C — return value when `gh` is absent.** `_run` returns a `subprocess.CompletedProcess` with
  `returncode=127`, empty stdout, and `stderr="<exe>: not found"`, so every existing caller keeps working.

If a worker hits an ambiguity not listed here, return `NEEDS_CONTEXT` with the question — do not resolve it.

## §0.9 — Phase-0 staleness check (run before touching anything)

```bash
git fetch origin && git log --oneline origin/main --since="24 hours ago"
# A: no-op if a calculator already exists
ls scripts/certification_power.py 2>/dev/null && echo "A: EXISTS -> return DONE citing the commit" || echo "A: absent, proceed"
grep -rl "def max_certifying_busts\|frechet" scripts/ lab/ --include='*.py' 2>/dev/null | head
# B: no-op if check_order already tests same-day letters
grep -n "letter" scripts/roll_sessions.py | grep -i "order\|inversion\|monoton" && echo "B: EXISTS -> return DONE" || echo "B: absent, proceed"
# C: no-op if _run already guards FileNotFoundError
grep -n "FileNotFoundError" scripts/repo_hygiene.py && echo "C: EXISTS -> return DONE" || echo "C: absent, proceed"
# All: no open PR may touch your footprint (gate passed at dispatch on 2026-09-04; re-check)
git log --oneline origin/main -3
```

If a packet's no-op condition fires, **return `DONE` citing the commit that did it. Do not build a duplicate.**

## §1 — Context

The Select campaign's Phase 3 freeze must state, in order, the **acceptance event** (which bounds, how many
limbs, joint or per-limb), the **certification power**, and only then `n` — because three hand-computed sizing
tables were published and two withdrawn under review (expected-count instead of power; per-limb instead of
joint; independence assumed instead of stated). A tested calculator makes the fourth withdrawal impossible
(**A**). The `sessions-order` gate let a same-day entry sit out of sequence because the check never reads
the letter (**B**). The repo's own post-merge tool cannot run in a container without `gh` (**C**). All three
are mechanical, spec-freezable, and off every locked surface — the fleet lane's exact shape.

## §2 — Frozen scope (one appendix per packet; footprints are disjoint)

### Packet A — `scripts/certification_power.py` + `tests/test_certification_power.py` + one `REPO_MAP.md` row

**Files (exactly):** `scripts/certification_power.py` (new), `tests/test_certification_power.py` (new), and
**one added row** in the `REPO_MAP.md` scripts table, in the style of `scripts/repo_hygiene.py`'s row
(`governance` · `—` · "manual/local only, not in gates.yml; layer fallback (not in SCRIPTS_LAYER)"). Nothing else.

**Module API (stdlib only — `math.comb`; no numpy/scipy):**

```python
def max_certifying_busts(n: int, ceiling: float = 0.05, alpha: float = 0.05) -> int:
    """Largest k with BinomCDF(k; n, ceiling) <= alpha, else -1.
    Equivalent to: the one-sided (1-alpha) Clopper-Pearson upper bound on k/n is <= ceiling."""

def per_limb_power(n: int, true_rate: float, ceiling: float = 0.05, alpha: float = 0.05) -> float:
    """BinomCDF(max_certifying_busts(n); n, true_rate); 0.0 when no count certifies."""

def joint_power(q: float, limbs: int, dependence: str) -> float:
    """dependence='independent' -> q**limbs; 'frechet' -> max(0.0, 1 - limbs*(1-q)); else ValueError."""

def size_for_power(true_rate: float, target: float, *, limbs: int = 3, dependence: str = "independent",
                   ceiling: float = 0.05, alpha: float = 0.05, step: int = 10, n_max: int = 8000) -> int:
    """Smallest n on the grid range(step, n_max+1, step) with joint_power(per_limb_power(n, ...), limbs, dependence) >= target.
    Raises ValueError if none by n_max."""
```

**CLI:** `python scripts/certification_power.py --true-rate 0.03 --power 0.80 --limbs 3 --dependence independent`
prints one line: `n=950 per_limb=0.932 joint=0.809 max_busts=36 (ceiling=0.05 alpha=0.05 limbs=3 dependence=independent step=10)`.
Also `--n 630 --true-rate 0.03 --limbs 3` (no `--power`) evaluates a given `n`:
`n=630 per_limb=0.803 joint_independent=0.518 joint_frechet=0.409 max_busts=22`. Exit 0; no files written.

**Pinned acceptance tests (these numbers are the campaign's, verified twice under review — do not "correct" them):**

| call | expected |
|---|---|
| `max_certifying_busts(60)` / `(160)` / `(340)` / `(630)` / `(950)` | `0` / `3` / `10` / `22` / `36` |
| `per_limb_power(60, 0.005)` / `(160, 0.02)` / `(340, 0.03)` | `0.7403` / `0.6021` / `0.5577` (abs 5e-4) |
| `per_limb_power(630, 0.03)`; `joint_power(0.8030, 3, "independent")`; `joint_power(0.8030, 3, "frechet")` | `0.8030`; `0.5178`; `0.4090` (abs 5e-4) |
| `size_for_power(0.005, 0.80)` / `(0.02, 0.80)` / `(0.03, 0.80)` — limbs 3, independent, step 10 | `130` / `370` / `950` |
| `size_for_power(…, dependence="frechet")` at 0.005 / 0.02 / 0.03 | `130` / `390` / `970` |
| `size_for_power(0.03, 0.80, limbs=1)` (single limb, step 10) | `630` |
| `joint_power(0.9, 3, "bogus")` | raises `ValueError` |
| `max_certifying_busts(5)` | `-1`; `per_limb_power(5, 0.01) == 0.0` |
| CLI smoke: `subprocess.run([sys.executable, "scripts/certification_power.py", "--n", "630", "--true-rate", "0.03"])` | exit 0, stdout contains `per_limb=0.803` |

### Packet B — `scripts/roll_sessions.py` `check_order` same-day letter pass + tests

**Files (exactly):** `scripts/roll_sessions.py` (one new pass inside `check_order`, plus a small helper),
`tests/test_roll_sessions.py` (new tests appended). Nothing else; `_reorder_entries`, `--normalize`, and
`roll()` are **not** changed.

**Rule to add (pass 5, pure text, no git):** within each calendar date, entries must appear in **descending
letter order** — `d` above `c` above `b` above `a`; an unlettered heading counts as `a`. Emit
`f"same-day order: {label_above} sits above {label_below} ({date})"` per violation, in the same style as the
existing `date inversion:` message. The pass runs on the **whole file**, like the date-monotonicity pass.

**Pinned acceptance tests (use the existing `_entry`/`_doc`/`_write` helpers):**

- `d, c, b, a` for one date → `check_order` returns no `same-day order` problem.
- `d, b, c, a` → exactly one problem, naming `2026-09-04b` above `2026-09-04c`.
- unlettered `2026-09-04` sitting **above** `2026-09-04b` → one problem (unlettered is `a`).
- entries from two dates each correctly ordered → no problem; the existing `date inversion` behaviour is unchanged
  (one existing date-inversion test still passes untouched).
- `python scripts/roll_sessions.py --check-order` on the real `docs/SESSIONS.md` at the packet's base commit
  exits 0 (the file is currently `d, c, b, a` after campaign-state §36).

### Packet C — `scripts/repo_hygiene.py` degrades without `gh` + a test

**Files (exactly):** `scripts/repo_hygiene.py` (guard in `_run` only), `tests/test_repo_hygiene.py` (new).

**Change:** in `_run`, catch `FileNotFoundError` and return
`subprocess.CompletedProcess(args, 127, stdout="", stderr=f"{args[0]}: not found")`. Nothing else changes —
the existing `report.gh_available = gh_probe.returncode == 0` and the existing "gh not on PATH" warning then
do their job.

**Pinned acceptance tests:** create a throwaway git repo under `tmp_path` (`git init`, one commit, `main`
branch), monkeypatch the module's `REPO_ROOT` to it and `subprocess.run` so any `args[0] == "gh"` raises
`FileNotFoundError` (delegate everything else to the real `subprocess.run`); assert `build_report()` returns
with `gh_available is False`, a warning containing `"gh not on PATH"`, and no exception. A second test asserts
`_run(["definitely-not-a-binary-xyz"])` returns `returncode == 127` and does not raise.

## §4 — Falsifiable hypothesis

**H:** each packet is a mechanical, spec-freezable build whose acceptance tests fully determine "done" — a
worker can complete it with zero judgment calls beyond §0.5's listed defaults.
**Falsifier:** any packet returns `NEEDS_CONTEXT` twice, or a returned diff needs a design decision at
integration (e.g. packet B cannot express the rule without touching `_reorder_entries`; packet A's pinned
numbers cannot be reproduced on the stated grid). Either falsifies the routing for that packet — it drops to
CC solo and is logged against the fleet-level falsifier (skill §7). If the pinned numbers in A do **not**
reproduce, that is a **finding about the campaign tables**, reported, never "fixed" by editing the pins.

## §5 — Forbidden moves

- No writes outside your packet's file footprint (§2). In particular **no** edits to `STATE.md`,
  `docs/SESSIONS.md`, any campaign artifact, `scripts/gates.yml`, `Makefile`, ADRs, `CLAUDE.md`, Pine, or
  anything under `core/`.
- Do not wire any packet into `gates.yml`, pre-commit, or `make check`. Not a gate.
- Packet A: do not import numpy/scipy; do not change the pinned expected values to make a test pass.
- Packet B: do not change `_reorder_entries`, `--normalize`, `roll()`, or the archive logic; a check only.
- Packet C: do not alter what the report contains when `gh` **is** present; do not add a `gh` dependency.
- No `git commit --no-verify`; no rebase/force-push; no merge — **the operator merges.**
- No vendor bytes, no secrets, no live-account figures anywhere (commit messages and PR bodies included).

## §6 — Return contract and claim manifest

Branch **`cursor/scripts-side-2026-09-04-p<N>`** from **current `origin/main`** (never from another packet's
branch); one PR per packet, tests green on 3.11 and 3.12 (`python -m pytest <your test file>` and
`python scripts/gate_manifest.py --tier check`), PR body stating the four-state status:
**`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`**, plus the exact file list touched.
Gate criterion (binary): a packet is **RESOLVED** when its diff touches exactly its §2 footprint and every pinned
acceptance test in §2 passes; otherwise it is **FALSIFIED** for this fleet and returns with the failing test named
(an unanswerable §0.5 ambiguity is **AMBIGUOUS** → `NEEDS_CONTEXT`, one re-anchor, then CC solo).

| Packet | Branch | Files | Status |
|---|---|---|---|
| A — certification-power calculator | `cursor/scripts-side-2026-09-04-p1` | `scripts/certification_power.py`, `tests/test_certification_power.py`, one `REPO_MAP.md` row | QUEUED |
| B — same-day letter order pass | `cursor/scripts-side-2026-09-04-p2` | `scripts/roll_sessions.py`, `tests/test_roll_sessions.py` | QUEUED |
| C — `repo_hygiene` without `gh` | `cursor/scripts-side-2026-09-04-p3` | `scripts/repo_hygiene.py`, `tests/test_repo_hygiene.py` | QUEUED |

The orchestrator owns this table (QUEUED → DISPATCHED → RETURNED → MERGED / OVERTAKEN) and writes the single
integration commit (SESSIONS, statuses). Workers never edit this brief.

## §10 — Audit hooks (orchestrator-side, after each packet returns)

```bash
# Footprint: the diff touches exactly the packet's files
git fetch origin && git diff --name-only origin/main...origin/cursor/scripts-side-2026-09-04-p1   # expect the 3 A files
git diff --name-only origin/main...origin/cursor/scripts-side-2026-09-04-p2                       # expect the 2 B files
git diff --name-only origin/main...origin/cursor/scripts-side-2026-09-04-p3                       # expect the 2 C files
# Tests and gates, per packet, in a worktree at the packet head
python -m pytest -q tests/test_certification_power.py tests/test_roll_sessions.py tests/test_repo_hygiene.py
python scripts/gate_manifest.py --tier check
# A: the pinned numbers reproduce from the CLI (do not accept a packet whose pins were edited)
python scripts/certification_power.py --true-rate 0.03 --power 0.80 --limbs 3 --dependence independent   # n=950
python scripts/certification_power.py --true-rate 0.03 --power 0.80 --limbs 3 --dependence frechet       # n=970
python scripts/certification_power.py --n 630 --true-rate 0.03 --limbs 3                                 # per_limb=0.803 joint_independent=0.518 joint_frechet=0.409
# B: the real SESSIONS still passes, and a d,b,c,a fixture fails
python scripts/roll_sessions.py --check-order
# C: the tool now runs on a host without gh
python scripts/repo_hygiene.py | head -5
# Not wired into any gate
grep -n "certification_power\|test_repo_hygiene" scripts/gates.yml Makefile; echo "expect no match"
```

## Verification (parent-side, before dispatch)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-09-04-cursor-fleet-scripts-side-three-packets.md
```
