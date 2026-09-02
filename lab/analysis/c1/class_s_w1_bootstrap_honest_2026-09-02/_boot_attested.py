"""Attested corrected-geometry block-bootstrap helpers.

Frozen primitives live in ``run_class_s_c1_regime_gate``; this module only
wraps them so that (a) every joblib worker applies ``dd_lock_offset_usd``
locally and attests the value it used, and (b) each resample logs the
sampled block-start identities needed for rider-tail attribution.

Parent-only patches silently revert under process pools (joblib re-imports
``firm_rules``) — see ``lab/analysis/q_geofit_1_2026-07/run_envelope_map.py``.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Sequence

# 8 loky workers × OpenBLAS default (all cores) oversubscribes an 8-core box.
# Pin before numpy import; workers inherit env, and boot_one also re-asserts.
for _k, _v in (
    ("OMP_NUM_THREADS", "1"),
    ("MKL_NUM_THREADS", "1"),
    ("OPENBLAS_NUM_THREADS", "1"),
    ("NUMEXPR_NUM_THREADS", "1"),
):
    os.environ.setdefault(_k, _v)

import numpy as np

UNREACHABLE = 1_000_000.0
DEFECTIVE_OFFSET = 100.0
BLOCK_SIZE_BDAYS = 126
N_PANELS_DEFAULT = 100
BOOT_SEED = 20260715  # frozen regime-gate seed


def make_alt_panel_with_starts(
    vals: np.ndarray,
    *,
    target_len: int,
    block_size: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, list[int]]:
    """Same concatenation as regime-gate ``_make_alt_panel``, plus start indices."""
    n_avail = target_len - block_size + 1
    if n_avail < 1:
        raise ValueError(
            f"panel too short for block bootstrap: len={target_len} block={block_size}"
        )
    sampled: list[np.ndarray] = []
    starts: list[int] = []
    tot = 0
    while tot < target_len:
        st = int(rng.integers(0, n_avail))
        blk = vals[st : st + block_size]
        sampled.append(blk)
        starts.append(st)
        tot += len(blk)
    alt = np.concatenate(sampled)[:target_len]
    # All starts in `starts` contributed bytes; the last block may be truncated.
    return alt, starts


def boot_one_attested(
    pid: int,
    vals: np.ndarray,
    target_len: int,
    block_size: int,
    boot_seed: int,
    firm_key: str,
    thr,
    n_sims: int | None,
    *,
    log_blocks: bool = True,
) -> dict:
    """One bootstrap panel in a worker. Patches geometry LOCALLY and attests."""
    # Re-assert in case the worker process inherited a multi-thread BLAS default.
    for _k in (
        "OMP_NUM_THREADS",
        "MKL_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    ):
        os.environ[_k] = "1"
    try:
        from threadpoolctl import threadpool_limits

        _blas_ctx = threadpool_limits(limits=1)
        _blas_ctx.__enter__()
    except Exception:  # pragma: no cover
        _blas_ctx = None

    import firm_rules
    import run_class_s_c1_regime_gate as R

    prior = firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"]
    firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"] = UNREACHABLE
    try:
        rng = np.random.default_rng(boot_seed + pid * 1_000_003)
        if log_blocks:
            alt, starts = make_alt_panel_with_starts(
                vals, target_len=target_len, block_size=block_size, rng=rng
            )
        else:
            alt = R._make_alt_panel(
                vals, target_len=target_len, block_size=block_size, rng=rng
            )
            starts = []
        r = R.run_partition_mc(alt, firm_key, thr, n_sims=n_sims)
        used = float(firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"])
        out = {
            "pid": int(pid),
            "headline_bust": float(r["headline_bust"]),
            "pass_rate": float(r["pass_rate"]),
            "clears_part_a": bool(r["clears_part_a"]),
            "geometry_offset_used": used,
        }
        if log_blocks:
            out["block_starts"] = [int(s) for s in starts]
        return out
    finally:
        firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"] = prior
        if _blas_ctx is not None:
            _blas_ctx.__exit__(None, None, None)


def run_partition_mc_attested(
    daily: np.ndarray,
    firm_key: str,
    thr,
    *,
    n_sims: int | None = None,
) -> dict:
    """In-process partition MC with local corrected-geometry patch + attestation."""
    import firm_rules
    import run_class_s_c1_regime_gate as R

    prior = firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"]
    firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"] = UNREACHABLE
    try:
        r = R.run_partition_mc(daily, firm_key, thr, n_sims=n_sims)
        used = float(firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"])
        return {**r, "geometry_offset_used": used, "floor_ok": (
            float(r["headline_bust"]) <= thr.eval_bust_ceiling
            and float(r["pass_rate"]) >= thr.pass_floor
        )}
    finally:
        firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"] = prior


def half_panel_attested(
    daily: np.ndarray,
    thr,
    firm_key: str,
    *,
    n_sims: int | None = None,
) -> dict:
    import run_class_s_c1_regime_gate as R

    h1, h2, mid = R.half_panel_split(daily)
    r1 = run_partition_mc_attested(h1, firm_key, thr, n_sims=n_sims)
    r2 = run_partition_mc_attested(h2, firm_key, thr, n_sims=n_sims)
    return {
        "mid_index": mid,
        "h1_n_bdays": int(h1.size),
        "h2_n_bdays": int(h2.size),
        "H1": r1,
        "H2": r2,
        "half_panel_ok": bool(r1["floor_ok"] and r2["floor_ok"]),
        "geometry_offsets": [r1["geometry_offset_used"], r2["geometry_offset_used"]],
    }


def _resolve_n_jobs(n_jobs: int) -> int:
    """Map joblib-style -1 to concrete worker count (needed for wave-aligned batches)."""
    if n_jobs == -1:
        import os

        return max(1, int(os.cpu_count() or 1))
    return max(1, int(n_jobs))


def _load_checkpoint_resume(
    checkpoint_path: Path | None,
    *,
    firm_key: str,
    n_panels: int,
    boot_seed: int,
    log_blocks: bool,
) -> list[dict]:
    """Return completed panel rows if checkpoint matches this run's identity."""
    if checkpoint_path is None or not checkpoint_path.exists():
        return []
    try:
        payload = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[boot] checkpoint unreadable ({exc}); starting fresh", flush=True)
        return []
    if payload.get("firm_key") != firm_key or int(payload.get("n_panels", -1)) != n_panels:
        print(
            f"[boot] checkpoint identity mismatch "
            f"(got firm={payload.get('firm_key')} n={payload.get('n_panels')}); "
            f"starting fresh",
            flush=True,
        )
        return []
    if int(payload.get("boot_seed", boot_seed)) != boot_seed:
        # Older ckpts omit boot_seed — treat missing as matching current frozen seed.
        if "boot_seed" in payload:
            print("[boot] checkpoint boot_seed mismatch; starting fresh", flush=True)
            return []
    panels = payload.get("panels") or []
    if not isinstance(panels, list) or not panels:
        return []
    # Require contiguous pid 0..n-1 so resume math stays simple / reproducible.
    pids = [int(p["pid"]) for p in panels]
    if pids != list(range(len(panels))):
        print("[boot] checkpoint pids not contiguous from 0; starting fresh", flush=True)
        return []
    if log_blocks and any("block_starts" not in p for p in panels):
        print("[boot] checkpoint missing block_starts (log_blocks=True); starting fresh", flush=True)
        return []
    print(
        f"[boot] resume {len(panels)}/{n_panels} from {checkpoint_path.name}",
        flush=True,
    )
    return list(panels)


def part_a_bootstrap_attested(
    daily: np.ndarray,
    thr,
    firm_key: str,
    *,
    n_panels: int = N_PANELS_DEFAULT,
    block_size: int = BLOCK_SIZE_BDAYS,
    boot_seed: int = BOOT_SEED,
    n_sims: int | None = None,
    n_jobs: int = -1,
    log_blocks: bool = True,
    checkpoint_path: Path | None = None,
    checkpoint_every: int | None = None,
) -> dict:
    """n-panel block bootstrap with worker-local geometry patch + optional blocks.

    Checkpoint resume: if ``checkpoint_path`` exists and matches firm/n_panels/
    contiguous pids, skip already-done panels. Batch size defaults to the
    resolved worker count so each Parallel call is one full CPU wave (avoids
    the idle half-wave from ``checkpoint_every=10`` on an 8-core box).
    """
    try:
        from joblib import Parallel, delayed

        has_joblib = True
    except ImportError:  # pragma: no cover
        has_joblib = False

    vals = np.asarray(daily, dtype=float).reshape(-1)
    target_len = int(vals.size)
    workers = _resolve_n_jobs(n_jobs)
    # Wave-aligned batches: one Parallel call saturates all workers; checkpoint
    # after each wave. Override via checkpoint_every if an explicit stride is set.
    batch = max(1, int(checkpoint_every) if checkpoint_every is not None else workers)
    print(
        f"[boot] {firm_key} n={n_panels} block={block_size}bd "
        f"jobs={workers} (req={n_jobs}) batch={batch} log_blocks={log_blocks}",
        flush=True,
    )
    t0 = time.time()
    results: list[dict] = _load_checkpoint_resume(
        checkpoint_path,
        firm_key=firm_key,
        n_panels=n_panels,
        boot_seed=boot_seed,
        log_blocks=log_blocks,
    )
    # Wall so far from prior run (if any) is informational only; ETA uses this process.
    done_at_start = len(results)

    def _flush_ckpt(done: list[dict]) -> None:
        if checkpoint_path is None:
            return
        busts = np.array([r["headline_bust"] for r in done], dtype=float)
        passes = np.array([r["pass_rate"] for r in done], dtype=float)
        payload = {
            "firm_key": firm_key,
            "boot_seed": int(boot_seed),
            "n_done": len(done),
            "n_panels": n_panels,
            "bust_95th_so_far": float(np.percentile(busts, 95)) if len(done) >= 2 else None,
            "pass_5th_so_far": float(np.percentile(passes, 5)) if len(done) >= 2 else None,
            "geometry_offsets_unique": sorted({float(r["geometry_offset_used"]) for r in done}),
            "panels": done,
            "wall_s": round(time.time() - t0, 1),
            "resumed_from": done_at_start,
        }
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        checkpoint_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(
            f"[boot] checkpoint {len(done)}/{n_panels} -> {checkpoint_path.name} "
            f"bust95~={payload['bust_95th_so_far']}",
            flush=True,
        )

    start_pid = len(results)
    if start_pid >= n_panels:
        print(f"[boot] checkpoint already complete ({start_pid}/{n_panels})", flush=True)
    elif has_joblib and workers > 1 and (n_panels - start_pid) > 1:
        for start in range(start_pid, n_panels, batch):
            end = min(n_panels, start + batch)
            batch_res = Parallel(n_jobs=workers, prefer="processes")(
                delayed(boot_one_attested)(
                    pid,
                    vals,
                    target_len,
                    block_size,
                    boot_seed,
                    firm_key,
                    thr,
                    n_sims,
                    log_blocks=log_blocks,
                )
                for pid in range(start, end)
            )
            results.extend(batch_res)
            el = time.time() - t0
            newly = len(results) - done_at_start
            rem_panels = n_panels - len(results)
            rem = (el / max(newly, 1)) * rem_panels if newly else 0.0
            print(
                f"[boot]   {len(results)}/{n_panels} ({el:.0f}s this-proc, est rem {rem:.0f}s)",
                flush=True,
            )
            _flush_ckpt(results)
    else:
        for pid in range(start_pid, n_panels):
            results.append(
                boot_one_attested(
                    pid,
                    vals,
                    target_len,
                    block_size,
                    boot_seed,
                    firm_key,
                    thr,
                    n_sims,
                    log_blocks=log_blocks,
                )
            )
            if (pid + 1) % batch == 0 or (pid + 1) == n_panels:
                el = time.time() - t0
                newly = len(results) - done_at_start
                rem_panels = n_panels - len(results)
                rem = (el / max(newly, 1)) * rem_panels if newly else 0.0
                print(
                    f"[boot]   {pid + 1}/{n_panels} ({el:.0f}s this-proc, est rem {rem:.0f}s)",
                    flush=True,
                )
                _flush_ckpt(results)

    offsets = [float(r["geometry_offset_used"]) for r in results]
    bad = [o for o in offsets if o != UNREACHABLE]
    if bad:
        raise RuntimeError(
            f"geometry guard tripped: {len(bad)}/{len(offsets)} panels used "
            f"non-corrected offset (sample={bad[:5]})"
        )

    passes = np.array([r["pass_rate"] for r in results], dtype=float)
    busts = np.array([r["headline_bust"] for r in results], dtype=float)
    pass_5th = float(np.percentile(passes, 5))
    bust_95th = float(np.percentile(busts, 95))
    boot_ok = pass_5th >= thr.pass_floor and bust_95th <= thr.eval_bust_ceiling
    return {
        "n_panels": int(n_panels),
        "block_size_bdays": int(block_size),
        "boot_seed": int(boot_seed),
        "pass_5th": pass_5th,
        "pass_mean": float(passes.mean()),
        "bust_95th": bust_95th,
        "bust_mean": float(busts.mean()),
        "bootstrap_ok": bool(boot_ok),
        "wall_s": float(time.time() - t0),
        "geometry_attestation": {
            "expected_offset": UNREACHABLE,
            "unique_offsets_observed": sorted(set(offsets)),
            "all_attested_corrected": True,
            "n_panels_attested": len(offsets),
        },
        "panels": results,
    }


def pin_match(got: float, published: float, tol: float) -> dict:
    ok = abs(float(got) - float(published)) <= float(tol)
    return {
        "got": float(got),
        "published": float(published),
        "tol": float(tol),
        "ok": bool(ok),
        "label": "MATCH" if ok else "MISMATCH",
    }


def h1_fraction_for_starts(
    starts: Sequence[int],
    *,
    mid: int,
    block_size: int,
) -> float:
    """Mean fraction of each sampled block's days that fall in H1 [0, mid)."""
    if not starts:
        return float("nan")
    fracs = []
    for st in starts:
        lo, hi = int(st), int(st) + int(block_size)
        overlap = max(0, min(hi, mid) - max(lo, 0))
        fracs.append(overlap / float(block_size))
    return float(np.mean(fracs))
