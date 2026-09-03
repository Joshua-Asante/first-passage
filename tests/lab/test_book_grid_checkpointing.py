"""Regression guards on the checkpointed cell runner in `book_grid.py`.

Why this exists. The finals stage runs FOUR bootstraps per cell (intraday, EOD, and
both regime halves) at 10,000 sims x 3 seeds -- roughly 50x the per-cell work of the
screen stage. It used to run flat, as one `Parallel(...)` over every cell, holding all
results in memory and writing the output only after the last cell returned. On
2026-09-02 that lost two consecutive ~40-minute runs on a 16 GB machine: at jobs=4 two
of four loky workers died and joblib blocked forever waiting on them (8/12 cells, no
traceback, no output file); at jobs=6 the parent process died outright at ~9 minutes.
Both times `grid_final.json` stayed stale while the code that should have produced it
had already changed -- the exact "committed artifacts do not match the code" defect the
first review of PR #260 caught.

`_run_checkpointed` chunks the work and appends each result to a sidecar as it lands, so
a crash costs one chunk instead of the whole run.

⚠ Earlier revisions of this docstring claimed chunking bounded peak memory "since workers
are torn down between chunks". That was FALSE: joblib's loky backend keeps a reusable
executor, so constructing a new `Parallel` reuses the same processes and whatever RSS they
hold -- measured, two successive `Parallel(n_jobs=2)` calls reported the identical worker
PID. Chunking bought crash resilience; the memory relief came from lowering `--jobs`.
`_recycle_workers` now shuts the executor down at each chunk boundary, which is what makes
the claim true, and `test_recycle_workers_actually_replaces_the_loky_pool` holds it to it.
Raised by Codex on PR #271 (round 6).

These tests pin the properties that make it safe to trust a resumed artifact as much as a
cold one:

  * cell identity is exact, so a resume can never silently reuse the wrong cell;
  * a resumed cell is NOT recomputed (that is the whole point);
  * results come back in `jobs` order regardless of the order they completed or were
    checkpointed in, because the renderers index positionally;
  * a sidecar truncated mid-write by a hard kill degrades to recomputing that one cell
    rather than crashing or, worse, loading a half-written record;
  * the sidecar survives `_run_checkpointed` itself -- only `main` removes it, and only
    after the real output is safely on disk;
  * a sidecar built under a DIFFERENT configuration (or carrying no fingerprint at all)
    is refused rather than spliced into a fresh grid -- raised as P1 on PR #271, because
    `_job_key` alone cannot see a change to SEEDS, the engine, the firm rules, the
    session calendar or a vendor export;
  * joblib's negative `n_jobs` ("all CPUs", as used at `core/mc/modes.py`) is normalised
    before being used as a chunk width, instead of becoming a negative `range` step that
    silently runs nothing.

The stubbed scorer must actually be observed, which needs in-process execution: most
tests pass `n_jobs=1`, and the two that deliberately resolve a wider width wrap the call
in `parallel_backend("sequential")`. Under a worker-process backend the monkeypatch would
not propagate and these tests would silently pass for the wrong reason.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib

import pytest

_CAMPAIGN = (pathlib.Path(__file__).resolve().parents[2] / "lab" / "analysis" / "c1"
             / "tradeify_book_composition_2026-09")
_GRID = _CAMPAIGN / "book_grid.py"


@pytest.fixture(scope="module")
def grid():
    if not _GRID.exists():
        pytest.skip(f"absent: {_GRID}")
    if not (_CAMPAIGN / "data" / "cme_equity_sessions.json").exists():
        pytest.skip("session calendar absent")
    spec = importlib.util.spec_from_file_location("book_grid_ckpt_under_test", _GRID)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _job(sizing, tier, n_sims=10, stage="final"):
    return (sizing, tier, n_sims, ("2022-08-01", "2026-07-01"), stage,
            ("mnq", "mym", "aegis"))


def _fp_line(grid, jobs):
    """The fingerprint header a valid sidecar must carry (see the run-fingerprint tests).

    Hand-built sidecars in these tests need it: without it the runner refuses the sidecar
    outright, which is the intended behaviour but not what those tests are probing.
    """
    return json.dumps({"__fingerprint__": grid._run_fingerprint(jobs)},
                      sort_keys=True, default=str) + "\n"


def _pid(_):
    """Module-level so loky can pickle it; returns the worker process's own PID."""
    import os
    return os.getpid()


def _stub(grid, monkeypatch):
    """Replace score_cell with a counting stub that echoes its own cell identity."""
    calls = []

    def fake(job):
        sizing, tier, n_sims, _win, _stage, _legs = job
        calls.append((tier, tuple(sorted(sizing.items())), n_sims))
        return {"tier": tier, "sizing": sizing, "n_sims": n_sims, "marker": len(calls)}

    monkeypatch.setattr(grid, "score_cell", fake)
    return calls


# ------------------------------------------------------------------ cell identity

def test_job_key_is_stable_and_discriminating(grid):
    a = _job({"mnq": 1, "aegis": 2}, "Tradeify_Select_100K")
    assert grid._job_key(a) == grid._job_key(
        _job({"mnq": 1, "aegis": 2}, "Tradeify_Select_100K"))
    # every field that changes the computed result must change the key
    assert grid._job_key(a) != grid._job_key(
        _job({"mnq": 1, "aegis": 3}, "Tradeify_Select_100K"))
    assert grid._job_key(a) != grid._job_key(
        _job({"mnq": 1, "aegis": 2}, "Tradeify_Growth_100K"))
    assert grid._job_key(a) != grid._job_key(
        _job({"mnq": 1, "aegis": 2}, "Tradeify_Select_100K", n_sims=11))
    assert grid._job_key(a) != grid._job_key(
        _job({"mnq": 1, "aegis": 2}, "Tradeify_Select_100K", stage="screen"))


def test_job_key_ignores_dict_insertion_order(grid):
    """A cell is the same cell however its sizing dict happens to be built."""
    lhs = _job({"mnq": 1, "mym": 0, "aegis": 2}, "Tradeify_Select_100K")
    rhs = _job({"aegis": 2, "mnq": 1, "mym": 0}, "Tradeify_Select_100K")
    assert grid._job_key(lhs) == grid._job_key(rhs)


# ------------------------------------------------------------------ resume

def test_resume_does_not_recompute_checkpointed_cells(grid, monkeypatch, tmp_path):
    jobs = [_job({"mnq": 1, "aegis": k}, t)
            for k in (0, 2) for t in ("Tradeify_Select_100K", "Tradeify_Growth_100K")]
    out = str(tmp_path / "grid.json")

    calls = _stub(grid, monkeypatch)
    cold, part = grid._run_checkpointed(jobs, out, 1)
    assert len(calls) == 4, "cold run should compute every cell"
    assert pathlib.Path(part).exists(), "sidecar must outlive the run for a resume to work"

    calls.clear()
    warm, _ = grid._run_checkpointed(jobs, out, 1)
    assert calls == [], f"resume recomputed {len(calls)} cell(s)"
    assert json.dumps(warm, sort_keys=True) == json.dumps(cold, sort_keys=True)


def test_partial_resume_computes_only_the_missing_cells(grid, monkeypatch, tmp_path):
    jobs = [_job({"mnq": 1, "aegis": k}, "Tradeify_Select_100K") for k in (0, 2, 3)]
    out = str(tmp_path / "grid.json")
    part = pathlib.Path(grid.sidecar_path(out, jobs))

    # only the middle cell was checkpointed before the imagined crash
    part.write_text(_fp_line(grid, jobs) + json.dumps({
        "key": grid._job_key(jobs[1]),
        "result": {"tier": "Tradeify_Select_100K", "sizing": {"mnq": 1, "aegis": 2},
                   "n_sims": 10, "marker": "PRESERVED"},
    }) + "\n", encoding="utf-8")

    calls = _stub(grid, monkeypatch)
    res, _ = grid._run_checkpointed(jobs, out, 1)
    assert len(calls) == 2, f"expected 2 recomputes, got {len(calls)}"
    assert res[1]["marker"] == "PRESERVED", "the checkpointed cell was overwritten"
    assert [r["sizing"]["aegis"] for r in res] == [0, 2, 3]


def test_results_follow_job_order_not_checkpoint_order(grid, monkeypatch, tmp_path):
    """The renderers index positionally, so a resume must not permute the grid."""
    jobs = [_job({"mnq": 1, "aegis": k}, "Tradeify_Select_100K") for k in (0, 2, 3)]
    out = str(tmp_path / "grid.json")
    part = pathlib.Path(grid.sidecar_path(out, jobs))

    # sidecar written in REVERSE order, as an interleaved parallel run would produce
    with part.open("w", encoding="utf-8") as fh:
        fh.write(_fp_line(grid, jobs))
        for j in reversed(jobs):
            fh.write(json.dumps({"key": grid._job_key(j),
                                 "result": {"aegis": j[0]["aegis"]}}) + "\n")

    _stub(grid, monkeypatch)
    res, _ = grid._run_checkpointed(jobs, out, 1)
    assert [r["aegis"] for r in res] == [0, 2, 3]


def test_truncated_sidecar_tail_is_tolerated(grid, monkeypatch, tmp_path):
    """A hard kill mid-write leaves a partial line; it must cost one cell, not the run."""
    jobs = [_job({"mnq": 1, "aegis": k}, "Tradeify_Select_100K") for k in (0, 2)]
    out = str(tmp_path / "grid.json")
    part = pathlib.Path(grid.sidecar_path(out, jobs))

    with part.open("w", encoding="utf-8") as fh:
        fh.write(_fp_line(grid, jobs))
        fh.write(json.dumps({"key": grid._job_key(jobs[0]),
                             "result": {"marker": "GOOD"}}) + "\n")
        torn = json.dumps({"key": grid._job_key(jobs[1])})[:-3]   # torn off mid-write
        fh.write(torn)

    calls = _stub(grid, monkeypatch)
    res, _ = grid._run_checkpointed(jobs, out, 1)
    assert res[0]["marker"] == "GOOD", "the intact record should still be reused"
    assert len(calls) == 1, "only the torn cell should be recomputed"


def test_absent_sidecar_is_a_cold_run_not_an_error(grid, monkeypatch, tmp_path):
    jobs = [_job({"mnq": 1, "aegis": 0}, "Tradeify_Select_100K")]
    calls = _stub(grid, monkeypatch)
    res, part = grid._run_checkpointed(jobs, str(tmp_path / "nope.json"), 1)
    assert len(calls) == 1 and len(res) == 1
    assert pathlib.Path(part).exists()


def test_chunking_does_not_change_the_result_set(grid, monkeypatch, tmp_path):
    """Chunk width is a memory knob; it must not be visible in the output."""
    jobs = [_job({"mnq": 1, "aegis": k}, t)
            for k in (0, 2, 3) for t in ("Tradeify_Select_100K", "Tradeify_Growth_100K")]

    _stub(grid, monkeypatch)
    a, _ = grid._run_checkpointed(jobs, str(tmp_path / "a.json"), 1)
    _stub(grid, monkeypatch)
    b, _ = grid._run_checkpointed(jobs, str(tmp_path / "b.json"), 4)

    def strip(rs):
        return [{k: v for k, v in r.items() if k != "marker"} for r in rs]

    assert strip(a) == strip(b)


# ------------------------------------------------------- run fingerprint (PR #271, P1)
#
# `_job_key` identifies a cell by its CLI arguments only. SEEDS, the engine, the firm
# rules, the session calendar and the vendor exports all feed `score_cell` without
# appearing in that tuple, so a resume across a change to any of them would splice stale
# cells into a fresh grid while the output header advertised the new configuration. The
# sidecar therefore carries a fingerprint and a resume is honoured only on an exact match.

def test_fingerprint_covers_seeds(grid, monkeypatch):
    jobs = [_job({"mnq": 1, "aegis": 0}, "Tradeify_Select_100K")]
    before = grid._run_fingerprint(jobs)
    monkeypatch.setattr(grid, "SEEDS", (1, 2, 3))
    assert grid._run_fingerprint(jobs) != before, "changing SEEDS must change the fingerprint"


def test_fingerprint_covers_calendar_inputs_and_code(grid):
    fp = grid._run_fingerprint([_job({"mnq": 1, "aegis": 2}, "Tradeify_Select_100K")])
    for k in ("seeds", "horizon_cap", "tiers", "firm_rules", "sessions_sha",
              "inputs_sha", "code_sha"):
        assert k in fp, f"fingerprint is missing {k}"
    # the calendar is committed, so its hash must actually resolve
    assert fp["sessions_sha"] != "ABSENT"
    assert "book_grid.py" in fp["code_sha"] and fp["code_sha"]["book_grid.py"] != "ABSENT"
    # only the legs actually in play are fingerprinted
    assert set(fp["inputs_sha"]) <= {"mnq", "mym", "aegis"}


def test_sidecar_from_a_different_configuration_is_refused(grid, monkeypatch, tmp_path):
    jobs = [_job({"mnq": 1, "aegis": k}, "Tradeify_Select_100K") for k in (0, 2)]
    out = str(tmp_path / "grid.json")
    part = pathlib.Path(grid.sidecar_path(out, jobs))

    stale = grid._run_fingerprint(jobs)
    stale["seeds"] = [999, 998, 997]          # as if SEEDS had changed since the crash
    with part.open("w", encoding="utf-8") as fh:
        fh.write(json.dumps({"__fingerprint__": stale}, sort_keys=True, default=str) + "\n")
        for j in jobs:
            fh.write(json.dumps({"key": grid._job_key(j),
                                 "result": {"marker": "STALE"}}) + "\n")

    calls = _stub(grid, monkeypatch)
    res, _ = grid._run_checkpointed(jobs, out, 1)
    assert len(calls) == 2, "a sidecar from another configuration must not be reused"
    assert all(r.get("marker") != "STALE" for r in res), "stale results leaked into the grid"


def test_unfingerprinted_sidecar_is_refused(grid, monkeypatch, tmp_path):
    """Pre-fingerprint sidecars establish nothing about which config produced them."""
    jobs = [_job({"mnq": 1, "aegis": k}, "Tradeify_Select_100K") for k in (0, 2)]
    out = str(tmp_path / "grid.json")
    part = pathlib.Path(grid.sidecar_path(out, jobs))
    with part.open("w", encoding="utf-8") as fh:
        for j in jobs:
            fh.write(json.dumps({"key": grid._job_key(j),
                                 "result": {"marker": "OLD"}}) + "\n")

    calls = _stub(grid, monkeypatch)
    res, _ = grid._run_checkpointed(jobs, out, 1)
    assert len(calls) == 2, "an unfingerprinted sidecar must be refused, not trusted"
    assert all(r.get("marker") != "OLD" for r in res)


def test_matching_fingerprint_still_resumes(grid, monkeypatch, tmp_path):
    """Strictness must not have broken the resume it exists to make safe."""
    jobs = [_job({"mnq": 1, "aegis": k}, "Tradeify_Select_100K") for k in (0, 2)]
    out = str(tmp_path / "grid.json")

    calls = _stub(grid, monkeypatch)
    grid._run_checkpointed(jobs, out, 1)
    assert len(calls) == 2
    calls.clear()
    grid._run_checkpointed(jobs, out, 1)
    assert calls == [], "a sidecar written by this same configuration must still resume"


# ------------------------------------------------- joblib's negative n_jobs (PR #271, P2)

def test_negative_jobs_is_all_cpus_not_an_empty_loop(grid, monkeypatch, tmp_path):
    """`--jobs -1` is joblib's "all CPUs" (used at core/mc/modes.py), not a chunk step.

    Used raw it became the step of `range(0, len(pending), -1)` -- empty -- so no cell ran
    and the closing lookup raised KeyError for every one of them.
    """
    from joblib import parallel_backend
    jobs = [_job({"mnq": 1, "aegis": k}, "Tradeify_Select_100K") for k in (0, 2, 3)]
    calls = _stub(grid, monkeypatch)
    # sequential backend so the stub is observed even though n_jobs resolves > 1
    with parallel_backend("sequential"):
        res, _ = grid._run_checkpointed(jobs, str(tmp_path / "g.json"), -1)
    assert len(calls) == 3, f"expected all 3 cells computed, got {len(calls)}"
    assert [r["sizing"]["aegis"] for r in res] == [0, 2, 3]


def test_zero_jobs_does_not_hang_or_crash(grid, monkeypatch, tmp_path):
    from joblib import parallel_backend
    jobs = [_job({"mnq": 1, "aegis": 0}, "Tradeify_Select_100K")]
    calls = _stub(grid, monkeypatch)
    with parallel_backend("sequential"):
        res, _ = grid._run_checkpointed(jobs, str(tmp_path / "g.json"), 0)
    assert len(calls) == 1 and len(res) == 1


def test_effective_jobs_agrees_with_joblib(grid):
    """The resolved width must be whatever joblib itself would use.

    joblib reads negatives as offsets (-1 all CPUs, -2 all but one). Three attempts got
    this wrong before delegating: the raw value (empty `range` step, nothing ran),
    collapsing negatives to `os.cpu_count()` (more parallelism than reserved), and
    computing `os.cpu_count() + 1 + n_jobs` by hand (see the constrained-CPU test).
    """
    from joblib import effective_n_jobs
    for n in (-1, -2, -3, 1, 2, 3, 7):
        assert grid._effective_jobs(n) == max(1, effective_n_jobs(n)), n
    # 0/None mean serial here: joblib rejects n_jobs=0 outright, and for a CLI argument
    # the safe reading of "unspecified" is serial rather than maximal.
    assert grid._effective_jobs(0) == 1
    assert grid._effective_jobs(None) == 1
    # never 0 or negative, whatever is passed
    for n in (-99, -1000):
        assert grid._effective_jobs(n) >= 1


def test_effective_jobs_honours_joblibs_constrained_cpu_count(grid, monkeypatch):
    """`os.cpu_count()` is HOST CPUs; joblib honours cgroup/affinity/LOKY_MAX_CPU_COUNT.

    Measured on an 8-CPU box: under `LOKY_MAX_CPU_COUNT=2`, `joblib.cpu_count()` is 2 and
    `effective_n_jobs(-2)` is 1, while a hand-rolled `os.cpu_count() + 1 + n_jobs` yields
    7. Launching 7 workers inside a 2-CPU allocation reproduces the memory failures this
    checkpointing exists to prevent, so the resolution must come from joblib.
    Raised by Codex on PR #271 (round 5).
    """
    import os as _os
    monkeypatch.setenv("LOKY_MAX_CPU_COUNT", "2")
    hand_rolled = (_os.cpu_count() or 1) + 1 - 2      # the rejected formula, for -2
    got = grid._effective_jobs(-2)
    assert got <= 2, (
        f"resolved {got} workers under a 2-CPU constraint; the host-CPU formula would "
        f"have given {hand_rolled}")


def test_negative_jobs_offset_is_used_as_the_chunk_width(grid, monkeypatch, tmp_path):
    """The resolved count, not the raw negative, must reach the chunking."""
    import os as _os
    from joblib import parallel_backend
    monkeypatch.setattr(_os, "cpu_count", lambda: 4)
    jobs = [_job({"mnq": 1, "aegis": k}, "Tradeify_Select_100K") for k in (0, 2, 3)]
    calls = _stub(grid, monkeypatch)
    with parallel_backend("sequential"):
        res, _ = grid._run_checkpointed(jobs, str(tmp_path / "g.json"), -2)   # => width 3
    assert len(calls) == 3 and [r["sizing"]["aegis"] for r in res] == [0, 2, 3]


# ------------------------------------------------ torn sidecar repair (PR #271, round 4)

# -------------------------------------------- sidecar isolation (PR #271, round 6, P1)

def test_sidecar_name_is_scoped_to_the_configuration(grid, monkeypatch, tmp_path):
    """Two configurations must not be able to name the same sidecar file.

    Header-only scoping left a check-then-create race: a second process could replace the
    sidecar with fingerprint B while the first appended cells computed under fingerprint A,
    and B's next resume would trust them because `_job_key` omits everything the
    fingerprint represents. Putting the fingerprint in the NAME makes that structurally
    impossible instead of merely detectable.
    """
    jobs = [_job({"mnq": 1, "aegis": 2}, "Tradeify_Select_100K")]
    out = str(tmp_path / "grid.json")
    before = grid.sidecar_path(out, jobs)
    monkeypatch.setattr(grid, "SEEDS", (1, 2, 3))
    after = grid.sidecar_path(out, jobs)
    assert before != after, "a changed configuration reused the same sidecar filename"
    assert before.startswith(out) and after.startswith(out)


def test_one_configuration_cannot_consume_anothers_checkpoints(grid, monkeypatch, tmp_path):
    """End-to-end: run config A, switch configuration, confirm nothing of A is reused."""
    jobs = [_job({"mnq": 1, "aegis": k}, "Tradeify_Select_100K") for k in (0, 2)]
    out = str(tmp_path / "grid.json")

    calls = _stub(grid, monkeypatch)
    _, part_a = grid._run_checkpointed(jobs, out, 1)
    assert len(calls) == 2
    a_bytes = pathlib.Path(part_a).read_bytes()

    monkeypatch.setattr(grid, "SEEDS", (7, 8, 9))         # a different configuration
    calls.clear()
    _, part_b = grid._run_checkpointed(jobs, out, 1)
    assert len(calls) == 2, "config B reused config A's checkpointed cells"
    assert part_b != part_a, "both configurations wrote the same sidecar"
    assert pathlib.Path(part_a).read_bytes() == a_bytes, "config B mutated config A's sidecar"


# ------------------------------------------ loky worker recycling (PR #271, round 6, P2)

def test_recycle_workers_actually_replaces_the_loky_pool(grid):
    """The memory bound is only real if the workers genuinely go away.

    The control half matters as much as the assertion: it demonstrates that WITHOUT the
    explicit shutdown loky hands back the same processes, which is exactly why the earlier
    "workers are torn down between chunks" claim was false.
    """
    from joblib import Parallel, delayed

    # control: no shutdown between calls -> loky reuses its executor
    c = Parallel(n_jobs=2)(delayed(_pid)(i) for i in range(4))
    d = Parallel(n_jobs=2)(delayed(_pid)(i) for i in range(4))
    assert set(c) & set(d), (
        "control failed: loky did not reuse workers, so this test cannot show that "
        "_recycle_workers is what makes the teardown happen")

    # with the shutdown, the next chunk runs in fresh processes
    a = Parallel(n_jobs=2)(delayed(_pid)(i) for i in range(4))
    grid._recycle_workers()
    b = Parallel(n_jobs=2)(delayed(_pid)(i) for i in range(4))
    assert not (set(a) & set(b)), f"workers survived the recycle: {sorted(set(a) & set(b))}"

    grid._recycle_workers()      # leave no pool behind for later tests


def test_recycle_workers_is_a_safe_noop_under_a_sequential_backend(grid):
    """Never fatal: failing to recycle costs memory, not correctness."""
    from joblib import parallel_backend
    with parallel_backend("sequential"):
        grid._recycle_workers()
        grid._recycle_workers()


def test_torn_tail_is_removed_so_later_appends_stay_parseable(grid, monkeypatch, tmp_path):
    """Skipping a torn record is not enough -- the bad bytes must go.

    A hard kill can leave the last record truncated with no trailing newline. Skipping it
    on read but appending after it fused the next completed cell onto the junk, producing a
    SECOND invalid line; if that resumed run was itself interrupted before publishing, the
    freshly computed cell was discarded too and could be recomputed indefinitely.
    """
    jobs = [_job({"mnq": 1, "aegis": k}, "Tradeify_Select_100K") for k in (0, 2)]
    out = str(tmp_path / "grid.json")
    part = pathlib.Path(grid.sidecar_path(out, jobs))

    with part.open("w", encoding="utf-8") as fh:
        fh.write(_fp_line(grid, jobs))
        fh.write(json.dumps({"key": grid._job_key(jobs[0]),
                             "result": {"marker": "GOOD"}}) + "\n")
        fh.write(json.dumps({"key": grid._job_key(jobs[1])})[:-3])   # torn, no newline

    calls = _stub(grid, monkeypatch)
    grid._run_checkpointed(jobs, out, 1)
    assert len(calls) == 1, "only the torn cell should be recomputed"

    # every line in the repaired sidecar must parse -- no fused record at the seam
    lines = [ln for ln in part.read_text(encoding="utf-8").splitlines() if ln.strip()]
    for ln in lines:
        json.loads(ln)      # raises if the append fused onto the torn bytes

    # and the recomputed cell must survive a further interruption: a second resume sees both
    calls.clear()
    res, _ = grid._run_checkpointed(jobs, out, 1)
    assert calls == [], "the cell recomputed after the repair was not durably checkpointed"
    assert res[0]["marker"] == "GOOD"
