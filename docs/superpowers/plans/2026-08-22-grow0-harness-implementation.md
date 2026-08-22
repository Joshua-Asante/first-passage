# GROW-0 Synthetic Calibration Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `lab/discovery/grow0_harness.py` (plus two small satellite modules) that runs
GROW-0's Limb A, Limb B, and three RED controls exactly as frozen in
[`docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md`](../../briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md)
(`FROZEN`, operator GO 2026-08-22), and emits a machine-readable `RESOLVED`/`FALSIFIED` verdict
per the prereg's §6.7 Gate table.

**Architecture:** Three small, single-responsibility modules feed one orchestrator. `grow0_dgp.py`
owns the synthetic data-generating process and the `SeedSequence` spawn tree (pure, stateless,
independently testable). `grow0_scoring.py` owns the statistic, nomination rule, and nomination
gates — also pure. `grow0_harness.py` owns everything stateful: running panels through the DGP +
scoring pipeline, the retry ledger, cost-wiring construction check, and the CLI/gate aggregation.
`grow0_red_patch.py` is a fourth, deliberately separate module for RED-PATCH, since the prereg
itself describes it as "independent of the stochastic panels" with no shared state.

**Tech Stack:** Python 3.11+ (this repo's floor), NumPy (`numpy.random.SeedSequence` /
`default_rng`), SciPy (`scipy.stats.binom` for the Limb B/RED-LEAK verdict), `joblib` (already a
repo dependency, used for RED-PATCH's process fan-out), `pytest`.

## Global Constraints

- Every numeric constant below is copied verbatim from the frozen prereg — do not recompute,
  re-derive, or "improve" any of them. If a test's expected value doesn't match a number in this
  plan, the test or the plan has a transcription bug; the prereg is the source of truth.
- `PYTHONPATH=lab` is this repo's standing convention for `lab/`-rooted imports (e.g.
  `from research_utils.axis_screen import floor_at_k`, `from discovery.deep_lane_admission import
  deep_lane_power`) — every code block below assumes it, matching every existing file in
  `lab/discovery/`.
- No live-risk surface, no Pine, no arming, no `LEG_MAP` claim, no Databento pull — synthetic data
  only, `$0/K=0` throughout (prereg §5 forbidden moves; this plan builds nothing that touches any
  of those surfaces).
- `Date.now()`/`datetime.now()`-style self-timestamping is forbidden inside any function this plan
  adds that gets called from a workflow/harness context — the retry ledger's timestamp is always a
  caller-supplied argument (prereg §6.6), never computed internally.
- This machine has a constrained local-compute budget (see repo memory). Every test in this plan
  uses a small N (≤200 panels) for speed; the full N=5,500 production runs (Limb B, RED-LEAK) are
  never executed by the automated test suite — Task 13's manual invocation section says so
  explicitly and estimates the real cost.

---

## File Structure

| File | Responsibility |
|---|---|
| `lab/discovery/grow0_dgp.py` | Synthetic DGP (null/edge daily-P&L draw) + `SeedSequence` spawn tree. Pure functions; no state, no I/O. |
| `lab/discovery/grow0_scoring.py` | Annualized-Sharpe statistic, `argmax` nomination, nomination gates (a)/(b). Pure functions operating on NumPy arrays. |
| `lab/discovery/grow0_harness.py` | Orchestrates one panel run (calls `grow0_dgp` + `grow0_scoring`), Limb A/B runners, RED-LEAK/RED-BLIND runners, cost-wiring check, retry ledger, gate aggregation, CLI entrypoint. |
| `lab/discovery/grow0_red_patch.py` | RED-PATCH: the intraday-channel non-vacuity check + the M-23 parent-only-patch reproduction + the hand-rolled attestation guard. Deliberately independent of the other three modules. |
| `discovery_manifests/grow0_grammar.json` | The frozen K=10 grammar (prereg §2), committed and SHA256-pinned per the existing `lab/discovery/grammar.py` convention. |
| `discovery_manifests/grow0_retry_ledger.jsonl` | Created empty by Task 12's test; the harness appends to it at runtime (never committed with content — gitignored append target, matching `burned_segments.json`'s sibling pattern of being a real repo-root file the harness reads/writes). |
| `tests/test_grow0_dgp.py` | Tests for the DGP + seed tree. |
| `tests/test_grow0_scoring.py` | Tests for the statistic, nomination, gates. |
| `tests/test_grow0_harness.py` | Tests for the panel runner, Limb A/B, RED-LEAK/BLIND, retry ledger, CLI. |
| `tests/test_grow0_red_patch.py` | Tests for RED-PATCH. |

---

### Task 1: Frozen grammar file

**Files:**
- Create: `discovery_manifests/grow0_grammar.json`
- Test: `tests/test_grow0_grammar_file.py`

**Interfaces:**
- Consumes: `lab/discovery/grammar.py`'s existing `load_grammar_with_hash_check(path, *,
  expected_sha256) -> Grammar` (already landed, slice 1 — do not modify this file).
- Produces: a committed grammar file later tasks can point their own `Grammar`-consuming code at.
  No new grammar-loading logic is written in this task; it only exercises the existing loader.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_grammar_file.py
from pathlib import Path

from discovery.grammar import load_grammar_with_hash_check, sha256_of_grammar

GRAMMAR_PATH = Path(__file__).resolve().parents[1] / "discovery_manifests" / "grow0_grammar.json"


def test_grow0_grammar_matches_prereg_section_2():
    sha = sha256_of_grammar(GRAMMAR_PATH)
    grammar = load_grammar_with_hash_check(GRAMMAR_PATH, expected_sha256=sha)
    assert grammar.generation_budget == 10
    assert set(grammar.families.keys()) == {"session_offset_min"}
    assert grammar.families["session_offset_min"] == [0, 15, 30, 45, 60, 75, 90, 105, 120, 135]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_grammar_file.py -v`
Expected: FAIL — `FileNotFoundError` (the grammar file doesn't exist yet).

- [ ] **Step 3: Write the grammar file**

```json
{
  "generation_budget": 10,
  "families": {
    "session_offset_min": [0, 15, 30, 45, 60, 75, 90, 105, 120, 135]
  }
}
```

Save as `discovery_manifests/grow0_grammar.json` (exact JSON above, no trailing content — the
prereg §2 table pins index 5 = value 75 as `TRUE_EDGE_VARIANT_INDEX`, matching this array's index
5).

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_grammar_file.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add discovery_manifests/grow0_grammar.json tests/test_grow0_grammar_file.py
git commit -m "grow0: commit frozen K=10 grammar per prereg §2"
```

---

### Task 2: `grow0_dgp.py` — synthetic DGP draw function

**Files:**
- Create: `lab/discovery/grow0_dgp.py`
- Test: `tests/test_grow0_dgp.py`

**Interfaces:**
- Consumes: nothing from earlier tasks (first pure-logic module).
- Produces:
  - `N_TRAIN_DAYS: int = 1638`
  - `EDGE_DOLLARS: float = 64.4412`
  - `TRUE_EDGE_VARIANT_INDEX: int = 5`
  - `NULL_PARAMS: dict` with keys `p_active, p_win, win_mean, win_sd, loss_mean, loss_sd`
  - `draw_daily_pnl(seed, *, n_days: int = N_TRAIN_DAYS, edge: bool = False) -> np.ndarray` —
    later tasks (3, 5, 7–10) call this by exactly this name/signature.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_dgp.py
import numpy as np

from discovery.grow0_dgp import (
    EDGE_DOLLARS,
    N_TRAIN_DAYS,
    NULL_PARAMS,
    TRUE_EDGE_VARIANT_INDEX,
    draw_daily_pnl,
)


def test_constants_match_prereg_section_3():
    assert N_TRAIN_DAYS == 1638
    assert EDGE_DOLLARS == 64.4412
    assert TRUE_EDGE_VARIANT_INDEX == 5
    assert NULL_PARAMS == {
        "p_active": 0.60,
        "p_win": 0.45,
        "win_mean": 200.0,
        "win_sd": 80.0,
        "loss_mean": -163.60,
        "loss_sd": 60.0,
    }


def test_draw_daily_pnl_shape_and_reproducibility():
    pnl_a = draw_daily_pnl(42, n_days=100)
    pnl_b = draw_daily_pnl(42, n_days=100)
    assert pnl_a.shape == (100,)
    np.testing.assert_array_equal(pnl_a, pnl_b)  # same seed -> bit-identical


def test_draw_daily_pnl_null_vs_edge_differ_only_in_active_day_mean():
    n = 200_000  # large n so sample means are stable to ~1% for this smoke test
    null_pnl = draw_daily_pnl(7, n_days=n, edge=False)
    edge_pnl = draw_daily_pnl(8, n_days=n, edge=True)  # different seed -> independent draw
    # active-day means: null ~= $0.02, edge ~= $64.46 (prereg §3) -- loose bounds, not a
    # statistical power test, just a sanity check the shift is wired correctly
    null_active_mean = null_pnl[null_pnl != 0.0].mean()
    edge_active_mean = edge_pnl[edge_pnl != 0.0].mean()
    assert -5.0 < null_active_mean < 5.0
    assert 55.0 < edge_active_mean < 75.0


def test_draw_daily_pnl_active_fraction_matches_p_active():
    n = 200_000
    pnl = draw_daily_pnl(9, n_days=n)
    active_fraction = float(np.count_nonzero(pnl)) / n
    assert 0.59 < active_fraction < 0.61  # p_active = 0.60
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_dgp.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'discovery.grow0_dgp'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_dgp.py
"""GROW-0 synthetic data-generating process.

Frozen per docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md §3
(FROZEN, operator GO 2026-08-22) -- every constant below is copied verbatim from that prereg, not
re-derived. Do not change any value here without superseding the prereg with a fresh ledgered
PREREG first (prereg §5 forbidden moves).
"""
from __future__ import annotations

import numpy as np

N_TRAIN_DAYS = 1638  # round(252 * 6.5), prereg §3 "Partition"
EDGE_DOLLARS = 64.4412  # prereg §3 "Edge shape", solved via scipy.optimize.brentq for annSR=4.0
TRUE_EDGE_VARIANT_INDEX = 5  # prereg §2, grammar index 5 (session_offset_min=75)

NULL_PARAMS = {
    "p_active": 0.60,
    "p_win": 0.45,
    "win_mean": 200.0,
    "win_sd": 80.0,
    "loss_mean": -163.60,
    "loss_sd": 60.0,
}


def draw_daily_pnl(
    seed,
    *,
    n_days: int = N_TRAIN_DAYS,
    edge: bool = False,
) -> np.ndarray:
    """One draw of a daily P&L series under the frozen null (or edge) shape.

    ``seed`` is anything ``numpy.random.default_rng`` accepts -- an int, or (the harness's own
    usage) a ``numpy.random.SeedSequence`` leaf from the spawn tree in this module.

    Edge shape is a pure location shift on the null shape's win/loss means (prereg §3): variance
    is unchanged, isolating the detection problem to a mean shift.
    """
    rng = np.random.default_rng(seed)
    shift = EDGE_DOLLARS if edge else 0.0
    p = NULL_PARAMS
    active = rng.random(n_days) < p["p_active"]
    win = rng.random(n_days) < p["p_win"]
    win_draw = rng.normal(p["win_mean"] + shift, p["win_sd"], size=n_days)
    loss_draw = rng.normal(p["loss_mean"] + shift, p["loss_sd"], size=n_days)
    return np.where(active, np.where(win, win_draw, loss_draw), 0.0)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_dgp.py -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add lab/discovery/grow0_dgp.py tests/test_grow0_dgp.py
git commit -m "grow0: add frozen synthetic DGP draw function"
```

---

### Task 3: `grow0_dgp.py` — `SeedSequence` spawn tree

**Files:**
- Modify: `lab/discovery/grow0_dgp.py`
- Test: `tests/test_grow0_dgp.py` (append)

**Interfaces:**
- Consumes: nothing new.
- Produces:
  - `GROW0_ROOT_SEED: int = 20260822`
  - `build_root_branches() -> dict[str, np.random.SeedSequence]` — keys
    `"limb_a", "limb_b", "red_leak", "red_blind", "red_patch"`. Later tasks (7–10) call this once
    and index by these exact key names.
  - `spawn_panel_streams(panel_seq, n_variants: int) -> tuple[list, list]` — returns
    `(train_children, confirm_children)`, each a list of length `n_variants` of leaf
    `SeedSequence`s. Later tasks (5, 7–10) call this by exactly this name/signature.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_dgp.py (append to the file from Task 2)
from discovery.grow0_dgp import (
    GROW0_ROOT_SEED,
    build_root_branches,
    spawn_panel_streams,
)


def test_build_root_branches_has_five_named_keys():
    branches = build_root_branches()
    assert set(branches.keys()) == {"limb_a", "limb_b", "red_leak", "red_blind", "red_patch"}
    for seq in branches.values():
        assert isinstance(seq, type(branches["limb_a"]))  # all SeedSequence instances


def test_build_root_branches_is_reproducible():
    a = build_root_branches()
    b = build_root_branches()
    for key in a:
        # spawning the SAME root twice with the SAME spawn-key path yields identical leaves
        leaf_a = a[key].spawn(1)[0].generate_state(4)
        leaf_b = b[key].spawn(1)[0].generate_state(4)
        import numpy as np

        np.testing.assert_array_equal(leaf_a, leaf_b)


def test_spawn_panel_streams_returns_two_lists_of_requested_length():
    branches = build_root_branches()
    panel_seq = branches["limb_a"]
    train_children, confirm_children = spawn_panel_streams(panel_seq, 10)
    assert len(train_children) == 10
    assert len(confirm_children) == 10


def test_spawn_panel_streams_zero_collisions_at_scale():
    """Mirrors the prereg §3/§10 collision check -- 200 panels x 20 leaves each,
    all states unique. Capped at 200 panels per this plan's local-compute-budget
    constraint (the prereg's own full-scale 220,000-leaf check already ran during
    authoring; this test only needs to prove the *code* reproduces that shape)."""
    branches = build_root_branches()
    panels = branches["limb_b"].spawn(200)
    leaves = []
    for p in panels:
        train_children, confirm_children = spawn_panel_streams(p, 10)
        leaves.extend(train_children)
        leaves.extend(confirm_children)
    states = {tuple(s.generate_state(4)) for s in leaves}
    assert len(leaves) == 4000
    assert len(states) == 4000
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_dgp.py -v`
Expected: FAIL — `ImportError: cannot import name 'build_root_branches'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_dgp.py (append to the file from Task 2)

GROW0_ROOT_SEED = 20260822  # dated per repo convention; prereg §3 "Seeding scheme"

_BRANCH_NAMES = ("limb_a", "limb_b", "red_leak", "red_blind", "red_patch")


def build_root_branches() -> dict:
    """The five top-level SeedSequence branches, spawned in the exact order the
    prereg's §3 code block names them -- order matters, it fixes which branch
    each name maps to."""
    root = np.random.SeedSequence(GROW0_ROOT_SEED)
    branches = root.spawn(len(_BRANCH_NAMES))
    return dict(zip(_BRANCH_NAMES, branches))


def spawn_panel_streams(panel_seq, n_variants: int):
    """One panel's train/confirm leaf SeedSequences, ``n_variants`` each.

    Independent sub-branches (spawn(2) then spawn(n) on each) -- this is the
    structural property that makes TRAIN and CONFIRM independent draws, the
    thing RED-LEAK (prereg §6.3) deliberately violates by NOT calling this
    function for its own confirm value.
    """
    train_seq, confirm_seq = panel_seq.spawn(2)
    return train_seq.spawn(n_variants), confirm_seq.spawn(n_variants)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_dgp.py -v`
Expected: PASS (8 tests total)

- [ ] **Step 5: Commit**

```bash
git add lab/discovery/grow0_dgp.py tests/test_grow0_dgp.py
git commit -m "grow0: add SeedSequence spawn tree (collision-proof by construction)"
```

---

### Task 4: `grow0_scoring.py` — statistic and nomination gates

**Files:**
- Create: `lab/discovery/grow0_scoring.py`
- Test: `tests/test_grow0_scoring.py`

**Interfaces:**
- Consumes: nothing (pure functions on plain NumPy arrays — no dependency on `grow0_dgp`).
- Produces:
  - `annualized_sharpe(daily_pnl: np.ndarray) -> float`
  - `gate_a_passes(train_stat: float) -> bool`
  - `gate_b_passes(train_pnl: np.ndarray) -> bool`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_scoring.py
import numpy as np

from discovery.grow0_scoring import annualized_sharpe, gate_a_passes, gate_b_passes


def test_annualized_sharpe_known_value():
    # constant positive series: mean=$100, sd=0 is undefined (div by zero) -- use a
    # simple two-value alternating series with a known closed-form Sharpe
    pnl = np.array([100.0, -100.0] * 819)  # 1638 days, mean=0, sd=100
    assert annualized_sharpe(pnl) == 0.0

    pnl2 = np.full(252, 10.0)
    pnl2[0] = 20.0  # tiny variance so sd != 0
    sr = annualized_sharpe(pnl2)
    expected_mean = pnl2.mean()
    expected_sd = pnl2.std(ddof=0)
    assert sr == expected_mean / expected_sd * np.sqrt(252)


def test_gate_a_passes_boundary():
    assert gate_a_passes(0.0001) is True
    assert gate_a_passes(0.0) is False
    assert gate_a_passes(-0.5) is False


def test_gate_b_passes_active_cadence():
    # 1638 days, active every day -> cadence >> 1/week -> passes
    always_active = np.full(1638, 50.0)
    assert gate_b_passes(always_active) is True

    # 1638 days, active only 1 day total -> cadence << 1/week -> fails
    barely_active = np.zeros(1638)
    barely_active[0] = 50.0
    assert gate_b_passes(barely_active) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_scoring.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'discovery.grow0_scoring'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_scoring.py
"""GROW-0 TRAIN/CONFIRM statistic and nomination gates.

Frozen scoring convention per the prereg §3: annualized Sharpe (sqrt(252)) of the daily net P&L
series, identical formula on TRAIN and CONFIRM. Nomination gates per prereg §6.1 step 4.
"""
from __future__ import annotations

import numpy as np

_TRADING_DAYS_PER_YEAR = 252
_TRADING_DAYS_PER_WEEK = 5.0


def annualized_sharpe(daily_pnl: np.ndarray) -> float:
    mean = daily_pnl.mean()
    sd = daily_pnl.std(ddof=0)
    return float(mean / sd * np.sqrt(_TRADING_DAYS_PER_YEAR))


def gate_a_passes(train_stat: float) -> bool:
    """Prereg §6.1 step 4(a): TRAIN net annSR > 0 (strict)."""
    return train_stat > 0.0


def gate_b_passes(train_pnl: np.ndarray) -> bool:
    """Prereg §6.1 step 4(b): TRAIN average weekly active-day cadence >= 1/week.

    An *average* floor over the full window, not a zero-tolerance-per-week rule
    (DL-1's own gate-2c convention, imported verbatim per the prereg).
    """
    n_days = train_pnl.shape[0]
    n_weeks = n_days / _TRADING_DAYS_PER_WEEK
    active_days = int(np.count_nonzero(train_pnl))
    return (active_days / n_weeks) >= 1.0
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_scoring.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add lab/discovery/grow0_scoring.py tests/test_grow0_scoring.py
git commit -m "grow0: add annualized-Sharpe statistic and nomination gates"
```

---

### Task 5: `grow0_scoring.py` — panel runner (nominate → gate → confirm)

**Files:**
- Modify: `lab/discovery/grow0_scoring.py`
- Test: `tests/test_grow0_scoring.py` (append)

**Interfaces:**
- Consumes: `draw_daily_pnl` (Task 2), `annualized_sharpe`/`gate_a_passes`/`gate_b_passes`
  (Task 4).
- Produces:
  - `PanelResult` — a frozen dataclass with fields `nominee: int`, `train_stat: float`,
    `gate_a: bool`, `gate_b: bool`, `abandoned: bool`, `confirm_stat: float | None`,
    `clears: bool`.
  - `run_panel(train_children, confirm_children, *, edge_variant_index: int | None = None,
    floor: float) -> PanelResult` — the normal (independent-CONFIRM) flow. Used by Tasks 7, 8, 10.
  - `run_panel_leaked(train_children, *, edge_variant_index: int | None = None, floor: float) ->
    PanelResult` — RED-LEAK's flow: CONFIRM is the nominee's own TRAIN value replayed, not an
    independent draw. Used by Task 9.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_scoring.py (append to the file from Task 4)
from discovery.grow0_dgp import build_root_branches, spawn_panel_streams
from discovery.grow0_scoring import PanelResult, run_panel, run_panel_leaked

FLOOR = 1.265  # floor_at_k(10, years=6.5) -- pinned literal for this test, verified in Task 6


def test_run_panel_limb_a_shape_recovers_edge_variant():
    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["limb_a"], 10)
    result = run_panel(
        train_children, confirm_children, edge_variant_index=5, floor=FLOOR
    )
    assert isinstance(result, PanelResult)
    # SR=4.0 planted edge is deterministic-in-practice (prereg §3) -- a fresh seed should
    # essentially always recover it; this is the harness's own correctness check, not a
    # statistical test of the design (that's what Limb A's real 5,500-panel run is for)
    assert result.nominee == 5
    assert result.abandoned is False
    assert result.clears is True


def test_run_panel_null_only_panel_rarely_clears():
    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["limb_b"], 10)
    result = run_panel(train_children, confirm_children, edge_variant_index=None, floor=FLOOR)
    assert isinstance(result, PanelResult)
    assert result.clears in (True, False)  # both legal; nominal_p0 is tiny but nonzero


def test_run_panel_abandoned_has_no_confirm_read(monkeypatch):
    """Nomination-gate failure is rare by design (prereg §6.1 step 4: ~0.14-0.20%
    for a null-only panel), so a real seed only exercises this branch by luck --
    force it deterministically instead of hoping for one, per this plan's own
    no-vacuous-tests standard."""
    import discovery.grow0_scoring as scoring_module

    monkeypatch.setattr(scoring_module, "gate_a_passes", lambda train_stat: False)
    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["red_leak"], 10)
    result = run_panel(train_children, confirm_children, edge_variant_index=None, floor=FLOOR)
    assert result.abandoned is True
    assert result.gate_a is False
    assert result.confirm_stat is None
    assert result.clears is False


def test_run_panel_leaked_confirm_equals_train_stat_of_nominee():
    branches = build_root_branches()
    train_children, _ = spawn_panel_streams(branches["red_leak"], 10)
    result = run_panel_leaked(train_children, edge_variant_index=None, floor=FLOOR)
    if not result.abandoned:
        assert result.confirm_stat == result.train_stat
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_scoring.py -v`
Expected: FAIL — `ImportError: cannot import name 'PanelResult'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_scoring.py (append to the file from Task 4)
from dataclasses import dataclass

from discovery.grow0_dgp import draw_daily_pnl


@dataclass(frozen=True)
class PanelResult:
    nominee: int
    train_stat: float
    gate_a: bool
    gate_b: bool
    abandoned: bool
    confirm_stat: float | None
    clears: bool


def _score_all_variants(train_children, edge_variant_index):
    pnls = [
        draw_daily_pnl(train_children[i], edge=(i == edge_variant_index))
        for i in range(len(train_children))
    ]
    stats = [annualized_sharpe(p) for p in pnls]
    return pnls, stats


def run_panel(
    train_children,
    confirm_children,
    *,
    edge_variant_index: int | None,
    floor: float,
) -> PanelResult:
    """Prereg §6.1 steps 1-6 / §6.2: draw TRAIN for every variant, nominate by
    argmax (unconditional, no fallback), apply nomination gates on the nominee
    only, and -- if both gates pass -- draw an INDEPENDENT CONFIRM for the
    nominee and compare to ``floor``.
    """
    pnls, stats = _score_all_variants(train_children, edge_variant_index)
    nominee = int(max(range(len(stats)), key=lambda i: stats[i]))
    ga = gate_a_passes(stats[nominee])
    gb = gate_b_passes(pnls[nominee])
    if not (ga and gb):
        return PanelResult(
            nominee=nominee,
            train_stat=stats[nominee],
            gate_a=ga,
            gate_b=gb,
            abandoned=True,
            confirm_stat=None,
            clears=False,
        )
    confirm_pnl = draw_daily_pnl(
        confirm_children[nominee], edge=(nominee == edge_variant_index)
    )
    confirm_stat = annualized_sharpe(confirm_pnl)
    return PanelResult(
        nominee=nominee,
        train_stat=stats[nominee],
        gate_a=ga,
        gate_b=gb,
        abandoned=False,
        confirm_stat=confirm_stat,
        clears=confirm_stat >= floor,
    )


def run_panel_leaked(
    train_children,
    *,
    edge_variant_index: int | None,
    floor: float,
) -> PanelResult:
    """Prereg §6.3 RED-LEAK: identical to run_panel, except CONFIRM is the
    nominee's own winning TRAIN value replayed -- no independent draw at all.
    Deliberately violates the TRAIN/CONFIRM independence run_panel relies on.
    """
    pnls, stats = _score_all_variants(train_children, edge_variant_index)
    nominee = int(max(range(len(stats)), key=lambda i: stats[i]))
    ga = gate_a_passes(stats[nominee])
    gb = gate_b_passes(pnls[nominee])
    if not (ga and gb):
        return PanelResult(
            nominee=nominee,
            train_stat=stats[nominee],
            gate_a=ga,
            gate_b=gb,
            abandoned=True,
            confirm_stat=None,
            clears=False,
        )
    leaked_confirm_stat = stats[nominee]
    return PanelResult(
        nominee=nominee,
        train_stat=stats[nominee],
        gate_a=ga,
        gate_b=gb,
        abandoned=False,
        confirm_stat=leaked_confirm_stat,
        clears=leaked_confirm_stat >= floor,
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_scoring.py -v`
Expected: PASS (7 tests total)

- [ ] **Step 5: Commit**

```bash
git add lab/discovery/grow0_scoring.py tests/test_grow0_scoring.py
git commit -m "grow0: add panel runner (nominate/gate/confirm) and RED-LEAK variant"
```

---

### Task 6: `grow0_harness.py` — config + cost-wiring construction check

**Files:**
- Create: `lab/discovery/grow0_harness.py`
- Test: `tests/test_grow0_harness.py`

**Interfaces:**
- Consumes: `lab/discovery/cost_model.py`'s existing `resolve_commission(firm_key, instrument) ->
  float` (raises `ValueError` for unresolvable instruments — do not modify this file).
  `lab/research_utils/axis_screen.py`'s existing `floor_at_k(k, years=...) -> float` (do not
  modify).
- Produces:
  - `FLOOR: float` — module-level constant, `floor_at_k(10, years=6.5)`, computed once at import.
  - `check_cost_wiring() -> None` — raises `AssertionError` if the two-sided check (prereg §3)
    fails; returns `None` on success. Called once by Task 13's CLI entrypoint.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_harness.py
import pytest

from discovery.grow0_harness import FLOOR, check_cost_wiring


def test_floor_matches_prereg():
    assert round(FLOOR, 3) == 1.265


def test_check_cost_wiring_passes():
    check_cost_wiring()  # must not raise


def test_check_cost_wiring_catches_a_broken_mnq_resolution(monkeypatch):
    import discovery.cost_model as cost_model

    def _broken_resolve(firm_key, instrument):
        raise ValueError("simulated breakage")

    monkeypatch.setattr(cost_model, "resolve_commission", _broken_resolve)
    with pytest.raises(AssertionError):
        check_cost_wiring()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'discovery.grow0_harness'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_harness.py
"""GROW-0 synthetic calibration harness orchestrator.

Frozen per docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md
(FROZEN, operator GO 2026-08-22). This module runs Limb A, Limb B, and RED-LEAK/RED-BLIND
exactly as that prereg specifies -- RED-PATCH lives separately in grow0_red_patch.py, per the
prereg's own framing of it as independent of the stochastic panels.
"""
from __future__ import annotations

from discovery.cost_model import resolve_commission
from research_utils.axis_screen import floor_at_k

FLOOR = floor_at_k(10, years=6.5)  # prereg §4: floor_at_k(10, 6.5) = 1.265

_COST_FIRM_KEY = "Tradeify_Select_100K"
_COST_RESOLVABLE_INSTRUMENT = "MNQ"
_COST_UNRESOLVABLE_INSTRUMENT = "MGC"
_COST_RESOLVABLE_EXPECTED = 0.91


def check_cost_wiring() -> None:
    """Prereg §3 'Cost-wiring construction check' -- two-sided: MNQ must resolve
    to the real (index-micro) rate, and MGC must raise rather than silently
    falling back to a hardcoded literal. Called once at harness startup.
    """
    resolved = resolve_commission(_COST_FIRM_KEY, _COST_RESOLVABLE_INSTRUMENT)
    if resolved != _COST_RESOLVABLE_EXPECTED:
        raise AssertionError(
            f"cost_model.resolve_commission({_COST_FIRM_KEY!r}, "
            f"{_COST_RESOLVABLE_INSTRUMENT!r}) returned {resolved}, expected "
            f"{_COST_RESOLVABLE_EXPECTED} -- cost-wiring check failed (resolvable side)"
        )
    try:
        resolve_commission(_COST_FIRM_KEY, _COST_UNRESOLVABLE_INSTRUMENT)
    except ValueError:
        pass
    else:
        raise AssertionError(
            f"cost_model.resolve_commission({_COST_FIRM_KEY!r}, "
            f"{_COST_UNRESOLVABLE_INSTRUMENT!r}) did not raise -- cost-wiring check failed "
            "(unresolvable side; the module should refuse this instrument, not resolve it)"
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add lab/discovery/grow0_harness.py tests/test_grow0_harness.py
git commit -m "grow0: add harness module with floor constant and cost-wiring check"
```

---

### Task 7: `grow0_harness.py` — Limb A runner

**Files:**
- Modify: `lab/discovery/grow0_harness.py`
- Test: `tests/test_grow0_harness.py` (append)

**Interfaces:**
- Consumes: `build_root_branches`/`spawn_panel_streams` (Task 3), `run_panel`/`PanelResult`
  (Task 5), `FLOOR` (Task 6).
- Produces: `run_limb_a() -> tuple[str, PanelResult]` — returns `("PASS", result)` or
  `("FAIL", result)`. Used by Task 13's gate aggregation.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_harness.py (append to the file from Task 6)
from discovery.grow0_dgp import TRUE_EDGE_VARIANT_INDEX
from discovery.grow0_harness import run_limb_a


def test_run_limb_a_passes_with_frozen_seed():
    verdict, result = run_limb_a()
    # SR=4.0 planted edge is deterministic-in-practice per the prereg's own power
    # derivation (confirm-clear probability 1.00000000 at this target) -- a fresh,
    # frozen-tree run should PASS; a FAIL here means the harness code has a bug,
    # not that the design is underpowered (see prereg §3 "Why SR=4.0")
    assert verdict == "PASS"
    assert result.nominee == TRUE_EDGE_VARIANT_INDEX
    assert result.clears is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: FAIL — `ImportError: cannot import name 'run_limb_a'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_harness.py (append to the file from Task 6)
from discovery.grow0_dgp import TRUE_EDGE_VARIANT_INDEX, build_root_branches, spawn_panel_streams
from discovery.grow0_scoring import PanelResult, run_panel


def run_limb_a() -> tuple[str, PanelResult]:
    """Prereg §6.1: single panel, K=10 grammar with theta* at index 5."""
    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["limb_a"], 10)
    result = run_panel(
        train_children,
        confirm_children,
        edge_variant_index=TRUE_EDGE_VARIANT_INDEX,
        floor=FLOOR,
    )
    passed = (not result.abandoned) and result.nominee == TRUE_EDGE_VARIANT_INDEX and result.clears
    return ("PASS" if passed else "FAIL"), result
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: PASS (4 tests total)

- [ ] **Step 5: Commit**

```bash
git add lab/discovery/grow0_harness.py tests/test_grow0_harness.py
git commit -m "grow0: add Limb A runner"
```

---

### Task 8: `grow0_harness.py` — Limb B runner (with runtime seed-diversity assertion)

**Files:**
- Modify: `lab/discovery/grow0_harness.py`
- Test: `tests/test_grow0_harness.py` (append)

**Interfaces:**
- Consumes: `run_panel` (Task 5), `spawn_panel_streams`/`build_root_branches` (Task 3), `FLOOR`
  (Task 6), `scipy.stats.binom` (new dependency for this task, already a repo dependency
  elsewhere — e.g. `lab/research_utils/axis_screen.py` uses `scipy`).
- Produces:
  - `LIMB_B_N: int = 5500`, `LIMB_B_C: int = 7` — frozen prereg §4 constants.
  - `assert_seed_diversity(leaves, *, min_distinct: int) -> None` — the lightweight-review-round
    fix (prereg §3 "Runtime diversity assertion"); raises `AssertionError` if fewer than
    `min_distinct` distinct leaf states were actually consumed.
  - `run_limb_b(n: int = LIMB_B_N, c: int = LIMB_B_C) -> tuple[str, int, list]` — returns
    `(verdict, sum_of_clears, panel_results)`. Used by Task 13.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_harness.py (append to the file from Task 7)
import pytest

from discovery.grow0_harness import (
    LIMB_B_C,
    LIMB_B_N,
    assert_seed_diversity,
    run_limb_b,
)


def test_limb_b_constants_match_prereg_section_4():
    assert LIMB_B_N == 5500
    assert LIMB_B_C == 7


def test_assert_seed_diversity_passes_on_distinct_leaves():
    from discovery.grow0_dgp import build_root_branches, spawn_panel_streams

    branches = build_root_branches()
    panels = branches["limb_b"].spawn(20)
    leaves = []
    for p in panels:
        tr, co = spawn_panel_streams(p, 10)
        leaves.extend(tr)
        leaves.extend(co)
    assert_seed_diversity(leaves, min_distinct=400)  # 20 panels x 20 leaves = 400, all distinct


def test_assert_seed_diversity_catches_a_collapsed_run():
    from discovery.grow0_dgp import build_root_branches

    branches = build_root_branches()
    one_panel = branches["limb_b"].spawn(1)[0]
    collapsed_leaves = [one_panel] * 400  # simulates a broadcast/closure bug: every
    # "panel" resolves to the SAME underlying SeedSequence
    with pytest.raises(AssertionError):
        assert_seed_diversity(collapsed_leaves, min_distinct=400)


def test_run_limb_b_small_n_returns_consistent_shape():
    """Uses a small N for speed (this plan's local-compute-budget constraint) --
    the frozen N=5,500/c=7 pair is exercised only by the manual full-scale
    invocation documented in Task 13, never by the automated test suite."""
    small_n, small_c = 100, 3  # not the frozen pair -- structural test only
    verdict, sum_clears, results = run_limb_b(n=small_n, c=small_c)
    assert verdict in ("PASS", "FAIL")
    assert len(results) == small_n
    assert sum_clears == sum(1 for r in results if r.clears)
    assert (verdict == "FAIL") == (sum_clears >= small_c)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: FAIL — `ImportError: cannot import name 'LIMB_B_N'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_harness.py (append to the file from Task 7)

LIMB_B_N = 5500  # prereg §4 (measured nominal_p0=0.00059070, N/c sized with CI margin)
LIMB_B_C = 7


def assert_seed_diversity(leaves, *, min_distinct: int) -> None:
    """Prereg §3 'Runtime diversity assertion' -- a lightweight-review-round fix.

    The design-time SeedSequence spawn tree is collision-proof by construction, but that does
    NOT prove the harness's own consuming loop reads a distinct panel_seqs[i] per panel i --
    a vectorization broadcast mistake or Python loop-variable-capture bug could silently
    collapse many/all panels onto the same seed while the spawn tree itself stays perfectly
    distinct. This must run against every leaf actually consumed in a real run, not a
    design-time sample.
    """
    states = {tuple(s.generate_state(4)) for s in leaves}
    if len(states) < min_distinct:
        raise AssertionError(
            f"seed-diversity check failed: {len(leaves)} leaves consumed, only "
            f"{len(states)} distinct states (expected >= {min_distinct}) -- likely a "
            "cross-panel seed-collapse bug (prereg §3), not a design-time collision"
        )


def run_limb_b(n: int = LIMB_B_N, c: int = LIMB_B_C):
    """Prereg §6.2: N null-only panels, sum(clears) >= c -> FAIL, else PASS."""
    branches = build_root_branches()
    panel_seqs = branches["limb_b"].spawn(n)
    results = []
    leaves = []
    for panel_seq in panel_seqs:
        train_children, confirm_children = spawn_panel_streams(panel_seq, 10)
        leaves.extend(train_children)
        leaves.extend(confirm_children)
        result = run_panel(
            train_children, confirm_children, edge_variant_index=None, floor=FLOOR
        )
        results.append(result)
    assert_seed_diversity(leaves, min_distinct=n * 20)
    sum_clears = sum(1 for r in results if r.clears)
    verdict = "FAIL" if sum_clears >= c else "PASS"
    return verdict, sum_clears, results
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: PASS (8 tests total)

- [ ] **Step 5: Commit**

```bash
git add lab/discovery/grow0_harness.py tests/test_grow0_harness.py
git commit -m "grow0: add Limb B runner with runtime seed-diversity assertion"
```

---

### Task 9: `grow0_harness.py` — RED-LEAK runner

**Files:**
- Modify: `lab/discovery/grow0_harness.py`
- Test: `tests/test_grow0_harness.py` (append)

**Interfaces:**
- Consumes: `run_panel_leaked` (Task 5), `spawn_panel_streams`/`build_root_branches` (Task 3),
  `FLOOR`, `LIMB_B_N`/`LIMB_B_C` (Task 8).
- Produces: `run_red_leak(n: int = LIMB_B_N, c: int = LIMB_B_C) -> str` — returns
  `"FAILED_AS_EXPECTED"` or `"PASSED_UNEXPECTEDLY"`. Used by Task 13.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_harness.py (append to the file from Task 8)
from discovery.grow0_harness import run_red_leak


def test_run_red_leak_fails_as_expected_at_frozen_scale():
    """RED-LEAK's own expected clear rate is p_leak=0.005891 (~9.97x nominal_p0 per
    prereg §6.3). n=2000/c=1 is sized so a correct implementation is
    deterministic-in-practice: P(zero clears in 2000 trials at p=0.005891), via
    scipy.stats.binom.pmf(0, 2000, 0.005891), is 0.0000066 (~0.0007%) -- a genuinely
    safe margin, unlike this test's own first draft (n=500/c=1, which turned out to
    carry a real ~5.2% spurious-failure rate -- binom.pmf(0,500,0.005891)=0.0521 --
    caught empirically when Task 9's implementer hit that exact tail on the frozen
    seed tree; fixed here rather than papering over with a different seed)."""
    verdict = run_red_leak(n=2000, c=1)
    assert verdict == "FAILED_AS_EXPECTED"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: FAIL — `ImportError: cannot import name 'run_red_leak'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_harness.py (append to the file from Task 8)
from discovery.grow0_scoring import run_panel_leaked


def run_red_leak(n: int = LIMB_B_N, c: int = LIMB_B_C) -> str:
    """Prereg §6.3: same N/c structure as Limb B, but CONFIRM is the panel's own
    TRAIN max replayed (run_panel_leaked) instead of an independent draw.
    Expected clear rate ~0.63% (~9.97x baseline) -- this rig is EXPECTED to make
    Limb B's own binomial check report FAIL; that FAIL is what "FAILED_AS_EXPECTED"
    means (the calibration check correctly detected the injected leak).
    """
    branches = build_root_branches()
    panel_seqs = branches["red_leak"].spawn(n)
    sum_clears = 0
    for panel_seq in panel_seqs:
        train_children, _ = spawn_panel_streams(panel_seq, 10)
        result = run_panel_leaked(train_children, edge_variant_index=None, floor=FLOOR)
        if result.clears:
            sum_clears += 1
    detected_leak = sum_clears >= c  # Limb-B-shaped check applied to this rigged run
    return "FAILED_AS_EXPECTED" if detected_leak else "PASSED_UNEXPECTEDLY"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: PASS (9 tests total)

- [ ] **Step 5: Commit**

```bash
git add lab/discovery/grow0_harness.py tests/test_grow0_harness.py
git commit -m "grow0: add RED-LEAK runner"
```

---

### Task 10: `grow0_harness.py` — RED-BLIND runner

**Files:**
- Modify: `lab/discovery/grow0_harness.py`
- Test: `tests/test_grow0_harness.py` (append)

**Interfaces:**
- Consumes: `run_panel` (Task 5), `spawn_panel_streams`/`build_root_branches` (Task 3), `FLOOR`
  (Task 6), `TRUE_EDGE_VARIANT_INDEX` (Task 2).
- Produces: `run_red_blind() -> str` — returns `"FAILED_AS_EXPECTED"` or
  `"PASSED_UNEXPECTEDLY"`. Used by Task 13.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_harness.py (append to the file from Task 9)
from discovery.grow0_harness import run_red_blind


def test_run_red_blind_fails_as_expected():
    """RED-BLIND draws only the 9 non-theta* grammar indices
    (0,1,2,3,4,6,7,8,9 -- theta*, grammar index 5, is never drawn at all).
    run_red_blind maps the winning ARRAY position (0-8, from a freshly
    spawn_panel_streams'd list) back to its ORIGINAL grammar index before
    comparing against TRUE_EDGE_VARIANT_INDEX -- so 'grammar_nominee == 5' is
    a TRUE structural impossibility (5 is not a member of the 9-index set
    being drawn from), not merely a low-probability coincidence. (An earlier
    draft of this task compared the raw array position directly against 5
    without remapping -- since array positions 0-8 DO include the value 5,
    that would only have been safe by accident, via the separate near-zero
    confirm-clear probability masking a real ~1/9 nominee-position coincidence;
    caught and fixed before implementation, not left as a latent gap.) This is
    deterministic BY CONSTRUCTION, not merely deterministic-in-practice; a
    single frozen-seed run is sufficient (matches Limb A's own single-panel
    design)."""
    verdict = run_red_blind()
    assert verdict == "FAILED_AS_EXPECTED"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: FAIL — `ImportError: cannot import name 'run_red_blind'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_harness.py (append to the file from Task 9)

_RED_BLIND_NULL_INDICES = tuple(i for i in range(10) if i != TRUE_EDGE_VARIANT_INDEX)
# (0, 1, 2, 3, 4, 6, 7, 8, 9) -- the 9 original grammar indices RED-BLIND draws from,
# in the same order spawn_panel_streams(..., 9) below produces its 9 leaves. theta*
# (index 5) is not a member of this tuple by construction.


def run_red_blind() -> str:
    """Prereg §6.4 (v3 mechanism): full K=10 grammar's theta* is structurally
    excluded from RED-BLIND's own draw set (only 9 null-shape leaves, at
    original grammar indices _RED_BLIND_NULL_INDICES, are ever spawned from
    the red_blind branch). run_panel's own `nominee` field is an array
    position (0-8) into THIS 9-element list, not an original grammar index --
    mapping it back via _RED_BLIND_NULL_INDICES[result.nominee] is what makes
    "== TRUE_EDGE_VARIANT_INDEX" a genuine structural impossibility rather
    than comparing two different index spaces as if they were the same one.
    Because the nominee is still the MAXIMUM of several draws (positively
    biased, like the normal flow), it passes nomination gates (a)/(b) in the
    overwhelming majority of trials and reaches the real comparison -- unlike
    v2's abandoned argmin design, which mostly re-tested gate (a) instead.
    """
    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["red_blind"], 9)
    result = run_panel(train_children, confirm_children, edge_variant_index=None, floor=FLOOR)
    grammar_nominee = _RED_BLIND_NULL_INDICES[result.nominee]
    passed = (not result.abandoned) and grammar_nominee == TRUE_EDGE_VARIANT_INDEX and result.clears
    return "PASSED_UNEXPECTEDLY" if passed else "FAILED_AS_EXPECTED"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: PASS (10 tests total)

- [ ] **Step 5: Commit**

```bash
git add lab/discovery/grow0_harness.py tests/test_grow0_harness.py
git commit -m "grow0: add RED-BLIND runner (v3 mechanism: exclude theta* from the draw set)"
```

---

### Task 11: `grow0_red_patch.py` — RED-PATCH

**Files:**
- Create: `lab/discovery/grow0_red_patch.py`
- Test: `tests/test_grow0_red_patch.py`

**Interfaces:**
- Consumes: `core/firm_rules.py`'s existing `FIRM_RULES` dict (do not modify this file — read the
  `"Tradeify_Select_100K"]["dd_lock_offset_usd"]` key, currently `1_000_000.0`, the `UNREACHABLE`
  default per `core/firm_rules.py:339`). `joblib.Parallel`/`delayed` (already a repo dependency).
- Produces: `run_red_patch() -> str` — returns `"FAILED_AS_EXPECTED"` or
  `"PASSED_UNEXPECTEDLY"`. Used by Task 13. This module has no dependency on `grow0_dgp.py` or
  `grow0_scoring.py` — it is deliberately standalone (prereg §6.5).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_red_patch.py
import pytest

from discovery.grow0_red_patch import (
    assert_intraday_channel_required,
    assert_singleton_attestation,
    reproduce_m23_parent_only_patch,
    run_red_patch,
)


def test_assert_intraday_channel_required_raises_on_none():
    with pytest.raises(ValueError):
        assert_intraday_channel_required(None)


def test_assert_intraday_channel_required_accepts_real_blocks():
    import numpy as np

    assert_intraday_channel_required(np.zeros((3, 5)))  # must not raise


def test_assert_singleton_attestation_raises_on_non_singleton_set():
    with pytest.raises(AssertionError):
        assert_singleton_attestation([1.0, 1.0, 2.0, 1.0], expected=1.0)


def test_assert_singleton_attestation_passes_on_singleton_set():
    assert_singleton_attestation([1.0, 1.0, 1.0, 1.0], expected=1.0)  # must not raise


def test_reproduce_m23_parent_only_patch_shows_workers_miss_the_patch():
    """This is the RED control's own 'the bug exists' sanity check -- workers under
    joblib's processes backend re-import firm_rules fresh, so they do NOT see the
    parent process's runtime patch."""
    attestations = reproduce_m23_parent_only_patch()
    assert len(attestations) == 4
    assert set(attestations) != {500.0}  # not all workers saw the parent's patch


def test_run_red_patch_reports_failed_as_expected():
    assert run_red_patch() == "FAILED_AS_EXPECTED"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_red_patch.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'discovery.grow0_red_patch'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_red_patch.py
"""GROW-0 RED-PATCH: the M-23-shaped attestation control.

Prereg §6.5 (FROZEN, operator GO 2026-08-22) -- standalone, independent of the stochastic
Limb A/B/RED-LEAK/RED-BLIND panels (grow0_harness.py / grow0_scoring.py / grow0_dgp.py). Hand-rolls
the F3 attested pattern inline per the GROW spec's own instruction, since
lab/research_utils/attested_patch.py does not exist yet (F3 spec status: PROPOSED, not built).
"""
from __future__ import annotations

from joblib import Parallel, delayed

_FIRM_KEY = "Tradeify_Select_100K"
_PATCH_KEY = "dd_lock_offset_usd"
_PATCHED_VALUE = 500.0  # any value distinct from the UNREACHABLE default (core/firm_rules.py)
_UNREACHABLE_DEFAULT = 1_000_000.0
_N_WORKERS = 4


def assert_intraday_channel_required(intraday_blocks) -> None:
    """Companion non-vacuity check (prereg §6.5 step 1): a construction-time
    guard proving the GROW-0 lane's own N-SURV-shaped wiring does not silently
    accept clock='eod' (intraday_blocks=None) the way
    prop_survivor_scoring.score_candidate's default path does (that gap is
    named, not modified -- prop_survivor_scoring.py is locked production code).
    """
    if intraday_blocks is None:
        raise ValueError(
            "grow0 N-SURV wrapper requires intraday_blocks; clock='eod' construction is refused"
        )


def _worker_read_patch_target():
    """Runs in a fanned-out worker process under joblib's 'processes' backend.
    Each worker re-imports firm_rules fresh, so it reads whatever value THAT
    process's own import resolved -- not necessarily the parent's runtime patch
    (the M-23 shape).
    """
    try:
        from firm_rules import FIRM_RULES
    except ImportError:  # pragma: no cover -- fallback path outside pytest's PYTHONPATH widening
        from core.firm_rules import FIRM_RULES

    return FIRM_RULES[_FIRM_KEY][_PATCH_KEY]


def reproduce_m23_parent_only_patch() -> list:
    """Patches FIRM_RULES in the PARENT process only, fans out _N_WORKERS via
    joblib (processes backend), and collects each worker's own read of the
    same key. Returns the list of attestations (restores the original value
    before returning, success or failure).
    """
    try:
        from firm_rules import FIRM_RULES
    except ImportError:  # pragma: no cover -- same fallback as lab/discovery/cost_mnq.py,
        # needed because bare `PYTHONPATH=lab` (this plan's own Global Constraint) does not
        # put `core/` on sys.path; only pytest's own conftest.py widening does that
        from core.firm_rules import FIRM_RULES

    FIRM_RULES[_FIRM_KEY][_PATCH_KEY] = _PATCHED_VALUE
    try:
        attestations = Parallel(n_jobs=_N_WORKERS, prefer="processes")(
            delayed(_worker_read_patch_target)() for _ in range(_N_WORKERS)
        )
    finally:
        FIRM_RULES[_FIRM_KEY][_PATCH_KEY] = _UNREACHABLE_DEFAULT
    return list(attestations)


def assert_singleton_attestation(attestations, expected) -> None:
    """Hand-rolled equivalent of the pending F3
    attested_patch.assert_singleton_attestation primitive."""
    distinct = set(attestations)
    if distinct != {expected}:
        raise AssertionError(
            f"non-singleton attested set (the M-23 shape): got {distinct}, "
            f"expected {{{expected}}}"
        )


def run_red_patch() -> str:
    """Prereg §6.5 steps 1-4, combined. Returns FAILED_AS_EXPECTED iff the M-23
    bug reproduces (workers do not see the parent's patch) AND the attestation
    guard correctly raises on that non-singleton set.
    """
    try:
        assert_intraday_channel_required(None)
    except ValueError:
        pass
    else:
        raise AssertionError("companion non-vacuity check did not raise on intraday_blocks=None")

    attestations = reproduce_m23_parent_only_patch()
    if set(attestations) == {_PATCHED_VALUE}:
        return "PASSED_UNEXPECTEDLY"  # bug did not reproduce -- nothing for the guard to catch

    try:
        assert_singleton_attestation(attestations, _PATCHED_VALUE)
    except AssertionError:
        return "FAILED_AS_EXPECTED"
    return "PASSED_UNEXPECTEDLY"  # guard should have raised and didn't
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_red_patch.py -v`
Expected: PASS (6 tests)

- [ ] **Step 5: Commit**

```bash
git add lab/discovery/grow0_red_patch.py tests/test_grow0_red_patch.py
git commit -m "grow0: add RED-PATCH (M-23 parent-only-patch attestation control)"
```

---

### Task 12: `grow0_harness.py` — retry ledger

**Files:**
- Modify: `lab/discovery/grow0_harness.py`
- Test: `tests/test_grow0_harness.py` (append)

**Interfaces:**
- Consumes: `research_utils.repo_root.repo_root() -> Path` (already exists, used elsewhere in
  `lab/discovery/` — e.g. `burned_segments.py`).
- Produces:
  - `RETRY_LEDGER_PATH: Path` — `repo_root() / "discovery_manifests" / "grow0_retry_ledger.jsonl"`.
  - `append_retry_ledger(entry: dict, *, path: Path | None = None) -> None` — appends one JSON
    line; never edits or deletes existing lines. Used by Task 13.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_harness.py (append to the file from Task 10)
import json

from discovery.grow0_harness import append_retry_ledger


def test_append_retry_ledger_appends_one_line(tmp_path):
    ledger_path = tmp_path / "grow0_retry_ledger.jsonl"
    entry1 = {"run_id": "test-1", "started_at_arg": "2026-08-22T00:00:00Z", "overall": "PASS"}
    entry2 = {"run_id": "test-2", "started_at_arg": "2026-08-22T00:01:00Z", "overall": "FAIL"}
    append_retry_ledger(entry1, path=ledger_path)
    append_retry_ledger(entry2, path=ledger_path)
    lines = ledger_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0]) == entry1
    assert json.loads(lines[1]) == entry2


def test_append_retry_ledger_creates_parent_dir_if_missing(tmp_path):
    ledger_path = tmp_path / "nested" / "grow0_retry_ledger.jsonl"
    append_retry_ledger({"run_id": "test-3"}, path=ledger_path)
    assert ledger_path.is_file()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: FAIL — `ImportError: cannot import name 'append_retry_ledger'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_harness.py (append to the file from Task 10)
import json
from pathlib import Path

from research_utils.repo_root import repo_root

RETRY_LEDGER_PATH = repo_root() / "discovery_manifests" / "grow0_retry_ledger.jsonl"


def append_retry_ledger(entry: dict, *, path: Path | None = None) -> None:
    """Prereg §6.6: append-only, one JSON line per harness invocation. Never
    edits or deletes an existing line. ``path`` defaults to RETRY_LEDGER_PATH;
    tests override it with a tmp_path.
    """
    target = path if path is not None else RETRY_LEDGER_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: PASS (12 tests total)

- [ ] **Step 5: Commit**

```bash
git add lab/discovery/grow0_harness.py tests/test_grow0_harness.py
git commit -m "grow0: add append-only retry ledger"
```

---

### Task 13: `grow0_harness.py` — gate aggregation and CLI entrypoint

**Files:**
- Modify: `lab/discovery/grow0_harness.py`
- Test: `tests/test_grow0_harness.py` (append)

**Interfaces:**
- Consumes: every function produced by Tasks 6–12 (`check_cost_wiring`, `run_limb_a`,
  `run_limb_b`, `run_red_leak`, `run_red_blind`, `append_retry_ledger`), plus
  `discovery.grow0_red_patch.run_red_patch` (Task 11).
- Produces:
  - `run_grow0(*, run_id: str, started_at_arg: str, limb_b_n: int = LIMB_B_N, limb_b_c: int =
    LIMB_B_C) -> dict` — the full orchestration; returns the same dict it appends to the ledger.
  - `main(argv: list[str] | None = None) -> int` — CLI entrypoint; exit code 0 iff `overall ==
    "RESOLVED"`, else 1. `if __name__ == "__main__": raise SystemExit(main())`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_grow0_harness.py (append to the file from Task 12)
from discovery.grow0_harness import run_grow0


def test_run_grow0_returns_all_five_tokens_and_a_verdict(tmp_path):
    ledger_path = tmp_path / "grow0_retry_ledger.jsonl"
    result = run_grow0(
        run_id="test-run-1",
        started_at_arg="2026-08-22T00:00:00Z",
        limb_b_n=100,  # small N for test speed -- not the frozen 5,500 pair
        limb_b_c=3,
        ledger_path=ledger_path,
    )
    assert set(result.keys()) >= {
        "run_id",
        "started_at_arg",
        "prereg_commit",
        "limb_a",
        "limb_b",
        "red_leak",
        "red_blind",
        "red_patch",
        "overall",
    }
    assert result["limb_a"] in ("PASS", "FAIL")
    assert result["overall"] in ("RESOLVED", "FALSIFIED")
    # ledger got exactly one line for this run
    lines = ledger_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1


def test_run_grow0_overall_resolved_iff_all_five_conditions_hold(tmp_path):
    ledger_path = tmp_path / "grow0_retry_ledger.jsonl"
    result = run_grow0(
        run_id="test-run-2",
        started_at_arg="2026-08-22T00:00:00Z",
        limb_b_n=100,
        limb_b_c=3,
        ledger_path=ledger_path,
    )
    expected_resolved = (
        result["limb_a"] == "PASS"
        and result["limb_b"] == "PASS"
        and result["red_leak"] == "FAILED_AS_EXPECTED"
        and result["red_blind"] == "FAILED_AS_EXPECTED"
        and result["red_patch"] == "FAILED_AS_EXPECTED"
    )
    assert (result["overall"] == "RESOLVED") == expected_resolved


def test_main_exit_code_matches_overall_verdict(tmp_path, monkeypatch, capsys):
    from discovery import grow0_harness

    ledger_path = tmp_path / "grow0_retry_ledger.jsonl"
    monkeypatch.setattr(grow0_harness, "RETRY_LEDGER_PATH", ledger_path)
    exit_code = grow0_harness.main(
        ["--run-id", "test-run-3", "--started-at", "2026-08-22T00:00:00Z", "--limb-b-n", "100", "--limb-b-c", "3"]
    )
    out = capsys.readouterr().out
    assert exit_code in (0, 1)
    assert '"overall"' in out
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: FAIL — `ImportError: cannot import name 'run_grow0'`

- [ ] **Step 3: Write the minimal implementation**

```python
# lab/discovery/grow0_harness.py (append to the file from Task 12)
import argparse
import sys

_PREREG_COMMIT_PLACEHOLDER = "unset"  # overwritten by --prereg-commit at CLI invocation time;
# the prereg itself has no fixed commit hash known ahead of its own freeze commit landing


def run_grow0(
    *,
    run_id: str,
    started_at_arg: str,
    limb_b_n: int = LIMB_B_N,
    limb_b_c: int = LIMB_B_C,
    prereg_commit: str = _PREREG_COMMIT_PLACEHOLDER,
    ledger_path: Path | None = None,
) -> dict:
    """Runs Limb A, Limb B, RED-LEAK, RED-BLIND, RED-PATCH in that order and
    computes the prereg §6.7 Gate verdict. Appends one line to the retry ledger
    (prereg §6.6) regardless of outcome, then returns the same dict.
    """
    from discovery.grow0_red_patch import run_red_patch

    check_cost_wiring()

    limb_a_verdict, _ = run_limb_a()
    limb_b_verdict, _, _ = run_limb_b(n=limb_b_n, c=limb_b_c)
    red_leak_verdict = run_red_leak(n=limb_b_n, c=limb_b_c)
    red_blind_verdict = run_red_blind()
    red_patch_verdict = run_red_patch()

    all_red_green = (
        red_leak_verdict == "FAILED_AS_EXPECTED"
        and red_blind_verdict == "FAILED_AS_EXPECTED"
        and red_patch_verdict == "FAILED_AS_EXPECTED"
    )
    resolved = all_red_green and limb_a_verdict == "PASS" and limb_b_verdict == "PASS"

    result = {
        "run_id": run_id,
        "started_at_arg": started_at_arg,
        "prereg_commit": prereg_commit,
        "limb_a": limb_a_verdict,
        "limb_b": limb_b_verdict,
        "red_leak": red_leak_verdict,
        "red_blind": red_blind_verdict,
        "red_patch": red_patch_verdict,
        "overall": "RESOLVED" if resolved else "FALSIFIED",
    }
    append_retry_ledger(result, path=ledger_path)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="GROW-0 synthetic calibration harness")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--started-at", required=True, help="ISO timestamp, caller-supplied")
    parser.add_argument("--prereg-commit", default=_PREREG_COMMIT_PLACEHOLDER)
    parser.add_argument("--limb-b-n", type=int, default=LIMB_B_N)
    parser.add_argument("--limb-b-c", type=int, default=LIMB_B_C)
    args = parser.parse_args(argv)

    result = run_grow0(
        run_id=args.run_id,
        started_at_arg=args.started_at,
        limb_b_n=args.limb_b_n,
        limb_b_c=args.limb_b_c,
        prereg_commit=args.prereg_commit,
    )
    print(json.dumps(result, indent=2))
    return 0 if result["overall"] == "RESOLVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=lab pytest tests/test_grow0_harness.py -v`
Expected: PASS (15 tests total)

- [ ] **Step 5: Run the FULL test suite for all four new modules**

Run: `PYTHONPATH=lab pytest tests/test_grow0_dgp.py tests/test_grow0_scoring.py tests/test_grow0_harness.py tests/test_grow0_red_patch.py tests/test_grow0_grammar_file.py -v`
Expected: PASS (all tests across all five files, none skipped)

- [ ] **Step 6: Commit**

```bash
git add lab/discovery/grow0_harness.py tests/test_grow0_harness.py
git commit -m "grow0: add gate aggregation, CLI entrypoint, and full verdict computation"
```

- [ ] **Step 7: Manual full-scale invocation (NOT part of the automated test suite)**

The frozen N=5,500/c=7 pair is never exercised by `pytest` — every test above uses a small N for
speed, per this plan's Global Constraints. Producing GROW-0's own actual `RESOLVED`/`FALSIFIED`
verdict against the prereg's real frozen design is a separate, deliberate, one-time invocation:

```bash
PYTHONPATH=lab python -m discovery.grow0_harness \
  --run-id "grow0-real-$(date -u +%Y%m%dT%H%M%SZ)" \
  --started-at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --prereg-commit "$(git log -1 --format=%H -- docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md)"
```

Cost estimate (informational, not a gate): Limb B + RED-LEAK together draw
`5,500 × 10 × 1,638 × 2 ≈ 180 million` synthetic daily values — roughly 180x smaller than the
20,000,000-trial × 1,638-day Monte Carlo already run successfully on this same machine during the
prereg's own authoring (§4/§10), so this single, sequential, non-parallel invocation should be
comfortably within this machine's resources. If it is not, the same invocation runs unmodified on
a cloud instance — nothing about `grow0_harness.py`'s design assumes local execution.

This step produces the artifact the prereg's own Gate (§6.7) exists to produce: a `RESOLVED` or
`FALSIFIED` verdict, recorded in `discovery_manifests/grow0_retry_ledger.jsonl`. Record the
outcome in `docs/SESSIONS.md` and, if `RESOLVED`, in `docs/briefs/closures/` per this repo's
closure-record convention (a fresh decision, not part of this implementation plan) — if
`FALSIFIED`, the prereg's own §6.7 disposition applies (supersede with a fresh ledgered PREREG,
Part B is not filed).

---

## Self-Review

**1. Spec coverage.** Every prereg section this plan needs to implement has a task:
§2 (grammar) → Task 1. §3 DGP → Tasks 2–3. §3 cost-wiring check → Task 6. §4 constants (`FLOOR`,
`LIMB_B_N`/`LIMB_B_C`) → Tasks 6, 8. §6.1 Limb A → Task 7. §6.2 Limb B + the runtime
seed-diversity assertion (lightweight-review fix) → Task 8. §6.3 RED-LEAK → Task 9. §6.4 RED-BLIND
(v3 mechanism) → Task 10. §6.5 RED-PATCH → Task 11. §6.6 retry ledger → Task 12. §6.7 gate
aggregation → Task 13. §1's "RED rigs must invoke the harness's own functions, not a freestanding
reimplementation" requirement (also a lightweight-review fix) is satisfied structurally: Tasks
9–10 call the exact same `run_panel`/`run_panel_leaked` functions Tasks 7–8 use, parameterized
differently (`edge_variant_index`, which draw-count, leaked-vs-independent-confirm) rather than
reimplementing the math — no gap found.

**2. Placeholder scan.** No "TBD"/"add error handling"/"similar to Task N" found — every step has
complete, runnable code. The one deliberately-named placeholder (`_PREREG_COMMIT_PLACEHOLDER =
"unset"`) is a real default value for an optional CLI flag, not an unfinished-code marker; Task
13 Step 7 shows the real invocation always supplies `--prereg-commit` via `git log`.

**3. Type consistency.** `PanelResult` (Task 5) is used identically by Tasks 7–10.
`draw_daily_pnl(seed, *, n_days, edge)` (Task 2) is called with the same keyword names everywhere
it's used (Task 5). `spawn_panel_streams(panel_seq, n_variants)` (Task 3) returns
`(train_children, confirm_children)` in that order everywhere it's consumed (Tasks 5, 7–10).
`FLOOR` (Task 6) is imported, never recomputed, by every task that needs it (7–10). `LIMB_B_N`/
`LIMB_B_C` (Task 8) are the single source for the frozen (5500, 7) pair — Task 9's RED-LEAK reuses
them as defaults but Task 13's tests deliberately override both to a small pair, matching the
Global Constraints' local-compute-budget rule.

---

Plan complete and saved to `docs/superpowers/plans/2026-08-22-grow0-harness-implementation.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
