# Cursor fleet — `scripts/`-side packets (certification-power calculator · `repo_hygiene` without `gh`; same-day letter-order check WITHDRAWN)

**Status:** **C CONVERGED (§44; #303 — operator merges). A: A1 RESOLVED but Codex's round on `b5b3fb4` found 3 × P2 → fix round A2 owed (§6b); #305 waits on A2. #304 to be closed.** Earlier: 22:10Z — A RESOLVED (fix round A1 owed), B built though withdrawn (#304, close without merge), C FALSIFIED (fix round C1 owed); gate read in campaign-state §43; fix rounds frozen in §6b. Was: QUEUED (A, C) — A was blocked on #297 until it merged (`81b35d0`, 2026-09-04); both dispatchable from `main` ≥ `81b35d0`. Re-frozen 2026-09-04 after Codex's pre-dispatch review of this brief ([#302](https://github.com/Joshua-Asante/first-passage/pull/302), 3 P1 + 4 P2, all accepted). Packet B is WITHDRAWN before dispatch: its rule conflicts with the repo's documented label allocator (see §2-B). Dispatch-moment gate passed on main `ba713ee`; open PRs #297 and #301 touch none of these footprints. ⚠ Corrected 22:55Z (Codex P2 on #302): all three workers HAD started (~21:50Z, from the brief as first opened) before the re-freeze landed (~22:03Z) — campaign-state §43 — which is why B was built and C guarded `_run`.**
**Type:** Cursor handoff (fleet umbrella; packet appendices A and C live, B withdrawn)
**Authority:** the seven-strategy Select campaign record, [`campaign state`](../programs/2026-09-03-seven-strategy-select-campaign-state.md) —
§27a/§31a/§33c (three hand-computed sizing tables, two withdrawn under Codex review) and the post-merge
checklist run of 2026-09-04 (`scripts/repo_hygiene.py` crashed on a container without `gh`). Fleet protocol:
[`cursor-fleet`](../../../.claude/skills/cursor-fleet/SKILL.md) under the
[CC/Cursor surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md).

**Layer:** `scripts/` governance tools, their tests, and the **generated** scripts block of `REPO_MAP.md`. **No**
`core/`, Pine, `dd_protection`, ADR, `STATE.md`, `docs/SESSIONS.md`, `scripts/gates.yml`, `Makefile`, or any
campaign artifact is touched by any packet. Nothing is wired into a gate. $0 spend beyond the builds.
**Disjoint file footprints**, each packet independently mergeable.

---

## §0 — Rule 0 reads (this session, verified before this brief was written)

- [`scripts/repo_hygiene.py`](../../../scripts/repo_hygiene.py) — module docstring: *"Requires: git. Optional: gh."*
  `_run()` (line ~64) calls `subprocess.run` with no `FileNotFoundError` guard; `build_report()` (line ~216)
  probes `["gh", "--version"]` through it. Without `gh` the probe raises instead of reaching the already-written
  `"gh not on PATH"` warning branch. A guard in `_run` itself would also swallow a missing **git**, which the
  module declares required — so the guard belongs at the optional probe only.
- [`scripts/check_repo_map_scripts_table.py`](../../../scripts/check_repo_map_scripts_table.py) — the
  `REPO_MAP.md` scripts table is **generated** (`--write`), including the caption
  `_63 tracked scripts/*.py files_`; `--check` exits 1 on drift and is **not** in `gates.yml`. A new tracked
  script therefore needs the regenerated block (row **and** caption), never a hand-added row.
- [`scripts/roll_sessions.py`](../../../scripts/roll_sessions.py) — `next_label_for_date` (line ~953) is
  documented *a-first, gaps filled* ("Gap example: `a` and `c` claimed → `b` (checker-acceptable; duplicates are
  the only label defect)") and pinned by `test_next_label_gap_fills_first_free`. `docs/SESSIONS.md` at `ba713ee`
  carries `2026-08-24` as `c, b, i, a, h, g`. **The same-day letter is an allocation slot, not a recency
  marker** — the premise behind the withdrawn Packet B.
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
- **A — REPO_MAP.** Run `python scripts/check_repo_map_scripts_table.py --write` and commit whatever the
  generator changes inside the scripts block (the new row and the caption). Do not hand-edit the table.
- **C — where the guard lives.** Around the `gh` probe in `build_report()` only. `_run` is unchanged, so a
  missing `git` still raises `FileNotFoundError` and `main()` exits non-zero — that is required behaviour.

If a worker hits an ambiguity not listed here, return `NEEDS_CONTEXT` with the question — do not resolve it.

## §0.9 — Phase-0 staleness check (run before touching anything)

```bash
git fetch origin && git log --oneline origin/main --since="24 hours ago"
# A — no-op condition: the calculator already exists (probe the SYMBOL, not a keyword)
grep -rln "def max_certifying_busts" scripts/ lab/ 2>/dev/null && echo "A: EXISTS -> return DONE citing the commit" || echo "A: absent, proceed"
# C — no-op condition: the gh probe is already guarded
grep -n "FileNotFoundError" scripts/repo_hygiene.py && echo "C: EXISTS -> return DONE citing the commit" || echo "C: absent, proceed"
# ALL — no OPEN PR may touch your footprint. `git log` cannot see open PRs; enumerate them:
gh pr list --state open --json number,headRefName 2>/dev/null \
  || echo "no gh: use the open-PR numbers the operator gave you (2026-09-04: #297, #301, #302)"
git fetch origin '+refs/pull/*/head:refs/remotes/pr/*'
for n in 297 301 302; do echo "== PR #$n =="; git diff --name-only origin/main...pr/$n; done
# Expected: none of the listed files is in your packet's §2 footprint. If one is, STOP and return BLOCKED naming it.
# (2026-09-04 result: #297 touched REPO_MAP.md and blocked A until it merged as 81b35d0; re-run the probe — it should now be clean for both.)
```

If a packet's no-op condition fires, **return `DONE` citing the commit that did it. Do not build a duplicate.**

## §1 — Context

The Select campaign's Phase 3 freeze must state, in order, the **acceptance event** (which bounds, how many
limbs, joint or per-limb), the **certification power**, and only then `n` — because three hand-computed sizing
tables were published and two withdrawn under review (expected-count instead of power; per-limb instead of
joint; independence assumed instead of stated). A tested calculator makes the fourth withdrawal impossible
(**A**). The repo's own post-merge tool cannot run in a container without `gh` (**C**). Both are mechanical,
spec-freezable, and off every locked surface — the fleet lane's exact shape. A third packet (**B**, a same-day
letter-order pass for `SESSIONS`) was authored and **withdrawn before dispatch** when Codex's review of this
brief showed the rule it would enforce contradicts the documented allocator; the details are kept in §2-B so
the idea is not re-derived.

## §2 — Frozen scope (one appendix per packet; footprints are disjoint)

### Packet A — `scripts/certification_power.py` + `tests/test_certification_power.py` + the regenerated `REPO_MAP.md` scripts block

**Files (exactly):** `scripts/certification_power.py` (new), `tests/test_certification_power.py` (new), and
`REPO_MAP.md` — **only the generated scripts block**, produced by
`python scripts/check_repo_map_scripts_table.py --write` (new row + caption `63 → 64`). Nothing else.

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
| `python scripts/check_repo_map_scripts_table.py --check` | exit 0 on the packet head |

### Packet B — WITHDRAWN before dispatch (kept so the idea is not re-derived)

The proposal: a fifth `check_order` pass requiring same-day entries in descending letter order. **Why it is
withdrawn:** `next_label_for_date` is documented and test-pinned as *a-first, gaps filled* — a new entry can
legitimately receive `b` after `c` exists — so a descending-letter invariant contradicts the allocator and would
fail on legitimately authored files (and on the live file's own history: `2026-08-24` is `c, b, i, a, h, g` at
`ba713ee`). Resolving that means choosing between changing a documented allocation convention and abandoning
the invariant — a judgment call, which is exactly what the fleet lane must not delegate. **If the operator
wants the letter to become a recency marker, that is a CC/operator decision touching the allocator, its tests
and the ADR that references it — not a Cursor packet.** The gap round 10 P3 actually exposed is narrower and
already by design: when git cannot date a heading, `_reorder_entries` keeps file order rather than inventing
an age.

### Packet C — `scripts/repo_hygiene.py` degrades without `gh` + a test

**Files (exactly):** `scripts/repo_hygiene.py` (guard at the `gh` probe in `build_report()` only),
`tests/test_repo_hygiene.py` (new).

**Change:** wrap the probe —
```python
try:
    gh_probe = _run(["gh", "--version"])
    report.gh_available = gh_probe.returncode == 0
except FileNotFoundError:
    report.gh_available = False
```
Nothing else changes: `_run` keeps raising for a missing executable, so a missing **git** still fails loudly
(module docstring: *Requires: git*), and the existing `"gh not on PATH"` warning branch does its job.

**Pinned acceptance tests:** create a throwaway git repo under `tmp_path` (`git init`, one commit, `main`
branch), monkeypatch the module's `REPO_ROOT` to it and `subprocess.run` so any `args[0] == "gh"` raises
`FileNotFoundError` (delegate everything else to the real `subprocess.run`); assert `build_report()` returns
with `gh_available is False`, a warning containing `"gh not on PATH"`, and no exception. A second test
monkeypatches `subprocess.run` to raise `FileNotFoundError` for `args[0] == "git"` and asserts
`build_report()` **raises** (git is required; the guard must not swallow it).

## §4 — Falsifiable hypothesis

**H:** each dispatched packet is a mechanical, spec-freezable build whose acceptance tests fully determine
"done" — a worker can complete it with zero judgment calls beyond §0.5's listed defaults.
**Falsifier:** any packet returns `NEEDS_CONTEXT` twice, or a returned diff needs a design decision at
integration (e.g. packet A's pinned numbers cannot be reproduced on the stated grid; packet C cannot keep the
missing-git failure without touching `_run`). Either falsifies the routing for that packet — it drops to CC
solo and is logged against the fleet-level falsifier (skill §7). **Packet B already falsified this way at
review time**, before dispatch, and is recorded as such. If the pinned numbers in A do **not** reproduce, that
is a **finding about the campaign tables**, reported, never "fixed" by editing the pins.

## §5 — Forbidden moves

- No writes outside your packet's file footprint (§2). In particular **no** edits to `STATE.md`,
  `docs/SESSIONS.md`, any campaign artifact, `scripts/gates.yml`, `Makefile`, ADRs, `CLAUDE.md`, Pine, or
  anything under `core/`.
- Do not wire any packet into `gates.yml`, pre-commit, or `make check`. Not a gate.
- Packet A: do not import numpy/scipy; do not change the pinned expected values to make a test pass; do not
  hand-edit the `REPO_MAP.md` table — regenerate it.
- Packet C: do not guard `_run` itself; do not change what the report contains when `gh` **is** present; do
  not add a `gh` dependency.
- No `git commit --no-verify`; no rebase/force-push; no merge — **the operator merges.**
- No vendor bytes, no secrets, no live-account figures anywhere (commit messages and PR bodies included).

## §6 — Return contract and claim manifest

Branch **`cursor/scripts-side-2026-09-04-p<N>`** from **current `origin/main`** (never from another packet's
branch); one PR per packet, tests green on 3.11 and 3.12 (`python -m pytest <your packet's test file>` and
`python scripts/gate_manifest.py --tier check`), PR body stating the four-state status:
**`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`**, plus the exact file list touched.
Gate criterion (binary): a packet is **RESOLVED** when its diff touches exactly its §2 footprint and every pinned
acceptance test in §2 passes; otherwise it is **FALSIFIED** for this fleet and returns with the failing test named
(an unanswerable §0.5 ambiguity is **AMBIGUOUS** → `NEEDS_CONTEXT`, one re-anchor, then CC solo).

| Packet | Branch | Files | Status |
|---|---|---|---|
| A — certification-power calculator | `cursor/scripts-side-2026-09-04-p1` | `scripts/certification_power.py`, `tests/test_certification_power.py`, `REPO_MAP.md` (generated scripts block only) | **FIX ROUND A1 RETURNED @ `b5b3fb4` — RESOLVED** (campaign-state §45; every §2 and §6b pin verified; both Codex threads resolved by the worker; `main` merged in, `--check` exit 0 on the merged head). First return `7b1418b` was RESOLVED on the §2 gate with two Codex P2s (§43). **Codex's round on `b5b3fb4` returned 3 × P2 (22:41Z), all verified → fix round A2 DISPATCHED (§6b). Not converged; not to be merged before A2 returns.** |
| B — same-day letter order pass | `cursor/scripts-side-2026-09-04-p2` (built regardless) | `scripts/roll_sessions.py`, `tests/test_roll_sessions.py` | **WITHDRAWN 2026-09-04** (mis-routed: needs a judgment on the label allocator; §2-B) — nevertheless built from the pre-withdrawal revision `af0203f` and returned `NEEDS_CONTEXT` as [#304](https://github.com/Joshua-Asante/first-passage/pull/304) (draft) with exactly the §2-B contradiction; **close without merge**, no re-anchor; `p2` stays burned |
| C — `repo_hygiene` without `gh` | `cursor/scripts-side-2026-09-04-p3` | `scripts/repo_hygiene.py`, `tests/test_repo_hygiene.py` | **FIX ROUND C1 RETURNED @ `94fa685` — RESOLVED** (campaign-state §44; every §6b pin verified; Codex thread resolved by the worker). First return `0e7ab25` was FALSIFIED (§43: guarded `_run`). **CONVERGED 22:34Z — Codex zero findings on `94fa685`, required check green: the operator merges.** Head moved 22:59Z to `2cc6e9a` by the operator's pure merge of `main` (parents `94fa685` + `5ab079c`; tree byte-identical to `merge-tree(main, 94fa685)`; diff still the two files) — verdicts carry; CI re-runs on that head. |

The orchestrator owns this table (QUEUED → DISPATCHED → RETURNED → MERGED / OVERTAKEN / WITHDRAWN) and writes
the single integration commit (SESSIONS, statuses). Workers never edit this brief. Packet numbering keeps
`p1`/`p3` so the withdrawn `p2` slot is never reused.

### §6b — Fix rounds (Codex-driven, post-return; orchestrator-owned, added 2026-09-04 22:15Z)

Returns are gate-read in campaign-state §43. Each fix round stays on the packet's existing branch (new commits;
no rebase, no force-push, no merge into `main`), merges `origin/main` first, touches only the packet's §2
footprint, and ends with the worker replying on the Codex thread and resolving it. The orchestrator re-runs the
packet's §10 block on the returned head.

| Round | PR | Scope (frozen) | Acceptance |
|---|---|---|---|
| **A1** | [#305](https://github.com/Joshua-Asante/first-passage/pull/305) | (i) Reject out-of-domain arguments at the API layer with `ValueError`: `n < 1`; `true_rate` or `q` non-finite or outside `[0, 1]`; `ceiling` or `alpha` outside the open interval `(0, 1)`; `target` outside `(0, 1]` (**amended by A2: the open interval `(0, 1)`**); `limbs < 1`; `n_max < step`. At the CLI, map `ValueError` to `parser.error` (exit 2, message on stderr, no traceback — this also covers the existing "no n ≤ n_max" case). `n = 5` stays valid (the `-1` / `0.0` pins). (ii) Make `max_certifying_busts` accumulate the lower-tail CDF once, incrementally in log space (or peak-shifted), stopping at the first `k` whose CDF exceeds `alpha` — O(k) per call, not O(k²); `per_limb_power` evaluates the CDF once. Keep the linear grid scan in `size_for_power`: smallest-`n` semantics must stay exact, so **no binary search over `n`** (joint power is not guaranteed monotone on the grid). No numpy/scipy; no API change | Every §2 pin unchanged. New pins: `max_certifying_busts(0)` raises; `per_limb_power(60, -0.03)`, `(60, 1.5)`, `(60, nan)` raise; `joint_power(0.9, 0, "independent")` and `(1.5, 3, "independent")` raise; `size_for_power(0.03, 0.8, ceiling=1.0)`, `(…, alpha=2)`, `(0.03, 0)` (target), `(…, n_max=5)` raise; CLI `--true-rate=-0.03 --power .8`, `--limbs 0 --n 630 --true-rate 0.03`, `--alpha 2 --n 60 --true-rate 0.03` each exit 2 with empty stdout. Regression pins at the grid's end (computed on `7b1418b`): `max_certifying_busts(8000) == 367`; `per_limb_power(8000, 0.049) == 0.1013` (abs 5e-4); `size_for_power(0.049, 0.80, n_max=2000)` raises `ValueError`. PR body reports the wall time of `python scripts/certification_power.py --true-rate 0.049 --power 0.80` at the default `n-max` (must exit 2 in seconds, not minutes)  — **RETURNED @ `b5b3fb4`, RESOLVED (§45)** |
| **A2** | [#305](https://github.com/Joshua-Asante/first-passage/pull/305) | Codex's second round on `b5b3fb4` (22:41Z): three P2, all reproduced by the orchestrator. (i) `target == 1.0` is claimed attained on a rounded CDF (`size_for_power(0.001, 1.0, limbs=1)` → 410 while the exact upper tail is positive): restrict `target` to the **open** interval `(0, 1)` — 100% certification power is unattainable for any true rate above zero — and amend A1's domain test. (ii) `--power` and `--n` silently prioritise `--power` (`--power 0.8 --n 630` sizes to 950, exit 0): make them a required mutually exclusive argparse group. (iii) `_iter_lower_cdf` ends at the accumulated float sum, a hair below 1 (0.99999999885 at n=8000, p=0.9), so an alpha near 1 lets `k = n` certify (`max_certifying_busts(8000, 0.9, 0.999999999)` → 8000): yield exactly `1.0` at `k == n`. Same rules as A1: existing branch, merge `origin/main` first, only the two packet files, no API change beyond the domain narrowing | Every §2 pin and every A1 pin unchanged except the target-domain amendment. New pins: `size_for_power(0.001, 1.0, limbs=1)` raises `ValueError`; CLI `--true-rate 0.03 --power 0.8 --n 630` exits 2 with empty stdout; `list(_iter_lower_cdf(n, p))[-1] == (n, 1.0)` exactly for `(60, 0.05)`, `(8000, 0.9)`, `(8000, 0.049)`; `max_certifying_busts(8000, 0.9, 0.999999999) < 8000`; `check_repo_map_scripts_table.py --check` exit 0 after the merge; `--tier check` exit 0; tests green on 3.11 and 3.12; the worker replies on all three threads and resolves them |
| **C1** | [#303](https://github.com/Joshua-Asante/first-passage/pull/303) | Conform to §2-C exactly: `scripts/repo_hygiene.py` `_run` byte-identical to `origin/main`; the guard wraps only the `gh --version` probe in `build_report()`; `tests/test_repo_hygiene.py` keeps the gh-absent test, deletes `test_run_missing_binary_returns_127`, adds the git-absent test asserting `build_report()` raises `FileNotFoundError` | `git diff origin/main -- scripts/repo_hygiene.py` shows only the `build_report()` hunk; `python -m pytest -q tests/test_repo_hygiene.py` → 2 passed; `--tier check` exit 0; PR body states the brief revision built first (`af0203f`) and the one conformed to (`70f1c47c` or later)  — **RETURNED @ `94fa685`, RESOLVED (§44)** |

## §10 — Audit hooks (orchestrator-side, after each packet returns — run each packet's block on ITS OWN head)

```bash
git fetch origin
# ---- Packet A (worktree at origin/cursor/scripts-side-2026-09-04-p1) ----
git diff --name-only origin/main...origin/cursor/scripts-side-2026-09-04-p1   # expect exactly the 3 A files
python -m pytest -q tests/test_certification_power.py
python scripts/check_repo_map_scripts_table.py --check                         # exit 0
python scripts/certification_power.py --true-rate 0.03 --power 0.80 --limbs 3 --dependence independent   # n=950
python scripts/certification_power.py --true-rate 0.03 --power 0.80 --limbs 3 --dependence frechet       # n=970
python scripts/certification_power.py --n 630 --true-rate 0.03 --limbs 3       # per_limb=0.803 joint_independent=0.518 joint_frechet=0.409
python scripts/gate_manifest.py --tier check
# ---- Packet C (worktree at origin/cursor/scripts-side-2026-09-04-p3) ----
git diff --name-only origin/main...origin/cursor/scripts-side-2026-09-04-p3   # expect exactly the 2 C files
python -m pytest -q tests/test_repo_hygiene.py
python scripts/repo_hygiene.py | head -5                                        # runs on a host without gh
python scripts/gate_manifest.py --tier check
# ---- Both: not wired into any gate ----
grep -n "certification_power\|test_repo_hygiene" scripts/gates.yml Makefile; echo "expect no match"
```

## Verification (parent-side, before dispatch)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-09-04-cursor-fleet-scripts-side-three-packets.md
```
