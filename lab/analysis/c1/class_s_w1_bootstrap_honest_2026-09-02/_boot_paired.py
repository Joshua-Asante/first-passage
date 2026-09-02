"""Paired (EOD + intraday-honest) block-bootstrap worker for the W1 4th partition.

Completes the one partition the 2026-08-09 W1 packet declared out of scope:
``RESULTS_INTRADAY_W1.md`` -- *"Bootstrap-95th remains unmeasured on the honest clock."*

Design constraints this module exists to satisfy, each tied to a dated prior failure:

1. **Worker-local geometry patch + attestation** (M-23 / the 2026-07-28 rider defect):
   a parent-only ``dd_lock_offset_usd`` patch silently reverts under joblib process
   pools because workers re-import ``firm_rules``. Every panel patches locally and
   attests the value it used; ``_boot_attested.boot_one_attested`` is the frozen
   precedent and this module mirrors it exactly.
2. **One RNG draw, both channels** (frozen Phase-4 §1 "resample #1"): the intraday
   channel is never re-drawn independently of the P&L channel. Enforced by delegating
   the draw to the production primitive
   ``lab/discovery/prop_survivor_scoring.make_alt_panel_paired``.
3. **Paired arms off the same panel**: each panel is scored TWICE -- EOD control
   (``intraday_blocks=None``) and honest (``intraday_blocks`` threaded) -- from the
   identical resampled series. The control arm therefore reproduces the published
   corrected-geometry EOD bootstrap (1.20% bust-95th, ``eval_shape_diagnostics_2026-07-28``
   §(a)) and the honest arm is the new measurement. Any control drift is a harness
   defect, not a finding.
4. **Block-builder agreement guard**: the EOD path builds week-blocks via
   ``blocks_from_daily_pnl`` and the honest path via ``paired_blocks_from_daily``.
   These are two code paths for the same object; every panel asserts they agree
   byte-for-byte before either arm is scored.

Nothing here re-decides a threshold, a seed, a block size, or a panel. All frozen
values are read from the pre-registration via ``load_scoring_thresholds`` or imported
from the retrieved regime-gate module.
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Sequence

# Pin BLAS before numpy import (8 loky workers x OpenBLAS default oversubscribes an
# 8-core box). Workers inherit env; boot_one also re-asserts. Mirrors _boot_attested.
for _k, _v in (
    ("OMP_NUM_THREADS", "1"),
    ("MKL_NUM_THREADS", "1"),
    ("OPENBLAS_NUM_THREADS", "1"),
    ("NUMEXPR_NUM_THREADS", "1"),
):
    os.environ.setdefault(_k, _v)

import numpy as np

UNREACHABLE = 1_000_000.0


def assert_paired_draw_matches_eod(
    pnl: np.ndarray,
    low: np.ndarray,
    *,
    target_len: int,
    block_size: int,
    boot_seed: int,
    pids: Sequence[int],
) -> dict:
    """Guard: the paired draw must reproduce the EOD draw's P&L series exactly.

    ``_make_alt_panel`` (regime gate, EOD) accumulates ``tot += len(blk)``;
    ``make_alt_panel_paired`` (production) accumulates ``tot += block_size``. Blocks
    are always full length by construction, so the two loops must consume the same
    number of RNG integers in the same order and emit an identical P&L series. That
    is an argument, not a measurement -- this asserts it on real panel bytes before
    any scoring, so the control arm's equivalence to the published EOD run is
    established rather than assumed.
    """
    import run_class_s_c1_regime_gate as R
    from discovery.prop_survivor_scoring import make_alt_panel_paired

    checked = []
    for pid in pids:
        rng_a = np.random.default_rng(boot_seed + pid * 1_000_003)
        eod = R._make_alt_panel(
            pnl, target_len=target_len, block_size=block_size, rng=rng_a
        )
        rng_b = np.random.default_rng(boot_seed + pid * 1_000_003)
        paired_p, paired_l = make_alt_panel_paired(
            pnl, low, target_len=target_len, block_size=block_size, rng=rng_b
        )
        if not np.array_equal(eod, paired_p):
            raise AssertionError(
                f"paired draw diverges from EOD draw at pid={pid}: "
                f"max|delta|={float(np.max(np.abs(eod - paired_p)))}"
            )
        if paired_l.shape != paired_p.shape:
            raise AssertionError(
                f"paired channels shape mismatch at pid={pid}: "
                f"{paired_p.shape} vs {paired_l.shape}"
            )
        if np.any(paired_l > 0.0):
            raise AssertionError(f"resampled intraday_low has positive entries at pid={pid}")
        checked.append(int(pid))
    return {"pids_checked": checked, "ok": True}


def boot_one_paired(
    pid: int,
    pnl: np.ndarray,
    low: np.ndarray,
    target_len: int,
    block_size: int,
    boot_seed: int,
    firm_key: str,
    thr,
    n_sims: int | None,
) -> dict:
    """One bootstrap panel, scored on BOTH clocks. Geometry patched locally + attested."""
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
    from discovery.prop_survivor_scoring import (
        blocks_from_daily_pnl,
        make_alt_panel_paired,
        paired_blocks_from_daily,
        run_tier_remc,
        score_part_a,
    )

    prior = firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"]
    firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"] = UNREACHABLE
    try:
        rng = np.random.default_rng(boot_seed + pid * 1_000_003)
        alt_p, alt_l = make_alt_panel_paired(
            pnl, low, target_len=target_len, block_size=block_size, rng=rng
        )

        # Block-builder agreement guard (per panel, before scoring).
        blocks_eod = blocks_from_daily_pnl(alt_p)
        blocks_p, blocks_l = paired_blocks_from_daily(alt_p, alt_l)
        if not np.array_equal(blocks_eod, blocks_p):
            raise AssertionError(
                f"block builders disagree at pid={pid}: "
                f"blocks_from_daily_pnl vs paired_blocks_from_daily"
            )

        cons = R._consistency_frac(firm_key)

        # Arm 1 -- EOD control. Same call path as the published corrected-geometry run.
        eod_run = run_tier_remc(
            firm_key, blocks_p, thr, n_sims=n_sims, consistency=cons
        )
        # Arm 2 -- honest clock. Identical except the threaded intraday channel.
        hon_run = run_tier_remc(
            firm_key,
            blocks_p,
            thr,
            n_sims=n_sims,
            consistency=cons,
            intraday_blocks=blocks_l,
        )

        used = float(firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"])
        return {
            "pid": int(pid),
            "geometry_offset_used": used,
            "consistency": cons,
            "n_sims": int(eod_run["n_sims"]),
            "eod": {
                "headline_bust": float(eod_run["headline_bust"]),
                "pass_rate": float(eod_run["pass_rate"]),
                "clears_part_a": bool(score_part_a(eod_run, thr)),
                "intraday_low": bool(eod_run["intraday_low"]),
            },
            "honest": {
                "headline_bust": float(hon_run["headline_bust"]),
                "pass_rate": float(hon_run["pass_rate"]),
                "clears_part_a": bool(score_part_a(hon_run, thr)),
                "intraday_low": bool(hon_run["intraday_low"]),
            },
            "arms_differ": bool(
                float(eod_run["headline_bust"]) != float(hon_run["headline_bust"])
                or float(eod_run["pass_rate"]) != float(hon_run["pass_rate"])
            ),
            "panel_intraday_min": float(alt_l.min()),
        }
    finally:
        firm_rules.FIRM_RULES[firm_key]["dd_lock_offset_usd"] = prior
        if _blas_ctx is not None:
            _blas_ctx.__exit__(None, None, None)


def _summarize(results: list[dict], thr, arm: str) -> dict:
    passes = np.array([r[arm]["pass_rate"] for r in results], dtype=float)
    busts = np.array([r[arm]["headline_bust"] for r in results], dtype=float)
    pass_5th = float(np.percentile(passes, 5))
    bust_95th = float(np.percentile(busts, 95))
    return {
        "pass_5th": pass_5th,
        "pass_mean": float(passes.mean()),
        "bust_95th": bust_95th,
        "bust_mean": float(busts.mean()),
        "bust_max": float(busts.max()),
        "bootstrap_ok": bool(
            pass_5th >= thr.pass_floor and bust_95th <= thr.eval_bust_ceiling
        ),
    }


def part_a_bootstrap_paired(
    pnl: np.ndarray,
    low: np.ndarray,
    thr,
    firm_key: str,
    *,
    n_panels: int,
    block_size: int,
    boot_seed: int,
    n_sims: int | None = None,
    n_jobs: int = -1,
    checkpoint_path: Path | None = None,
) -> dict:
    """n-panel paired block bootstrap; both clocks scored per panel."""
    import json

    try:
        from joblib import Parallel, delayed

        has_joblib = True
    except ImportError:  # pragma: no cover
        has_joblib = False

    pnl = np.asarray(pnl, dtype=float).reshape(-1)
    low = np.asarray(low, dtype=float).reshape(-1)
    if pnl.size != low.size:
        raise ValueError(f"pnl {pnl.size} != low {low.size}")
    target_len = int(pnl.size)
    workers = max(1, int(os.cpu_count() or 1)) if n_jobs == -1 else max(1, int(n_jobs))
    batch = workers

    results: list[dict] = []
    if checkpoint_path is not None and checkpoint_path.exists():
        try:
            payload = json.loads(checkpoint_path.read_text(encoding="utf-8"))
            if (
                payload.get("firm_key") == firm_key
                and int(payload.get("n_panels", -1)) == n_panels
                and int(payload.get("boot_seed", -1)) == boot_seed
                and int(payload.get("n_sims") or -1) == int(n_sims or -1)
            ):
                panels = payload.get("panels") or []
                if [int(p["pid"]) for p in panels] == list(range(len(panels))):
                    results = list(panels)
                    print(
                        f"[boot] resume {len(results)}/{n_panels} from "
                        f"{checkpoint_path.name}",
                        flush=True,
                    )
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            print(f"[boot] checkpoint unusable ({exc}); starting fresh", flush=True)
            results = []

    print(
        f"[boot] {firm_key} n={n_panels} block={block_size}bd seed={boot_seed} "
        f"jobs={workers} batch={batch} sims={n_sims or thr.sims_per_seed}",
        flush=True,
    )
    t0 = time.time()
    done_at_start = len(results)

    def _flush(done: list[dict]) -> None:
        if checkpoint_path is None:
            return
        payload = {
            "firm_key": firm_key,
            "boot_seed": int(boot_seed),
            "n_panels": int(n_panels),
            "n_sims": int(n_sims) if n_sims is not None else None,
            "n_done": len(done),
            "panels": done,
            "wall_s": round(time.time() - t0, 1),
        }
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        checkpoint_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    start_pid = len(results)
    if start_pid >= n_panels:
        print(f"[boot] already complete ({start_pid}/{n_panels})", flush=True)
    elif has_joblib and workers > 1 and (n_panels - start_pid) > 1:
        for start in range(start_pid, n_panels, batch):
            end = min(n_panels, start + batch)
            batch_res = Parallel(n_jobs=workers, prefer="processes")(
                delayed(boot_one_paired)(
                    pid, pnl, low, target_len, block_size, boot_seed,
                    firm_key, thr, n_sims,
                )
                for pid in range(start, end)
            )
            results.extend(batch_res)
            el = time.time() - t0
            newly = len(results) - done_at_start
            rem = (el / max(newly, 1)) * (n_panels - len(results)) if newly else 0.0
            eod_s = _summarize(results, thr, "eod")
            hon_s = _summarize(results, thr, "honest")
            print(
                f"[boot]   {len(results)}/{n_panels} ({el:.0f}s, est rem {rem:.0f}s) "
                f"eod95={eod_s['bust_95th']:.4%} honest95={hon_s['bust_95th']:.4%}",
                flush=True,
            )
            _flush(results)
    else:
        for pid in range(start_pid, n_panels):
            results.append(
                boot_one_paired(
                    pid, pnl, low, target_len, block_size, boot_seed,
                    firm_key, thr, n_sims,
                )
            )
            _flush(results)

    offsets = [float(r["geometry_offset_used"]) for r in results]
    bad = [o for o in offsets if o != UNREACHABLE]
    if bad:
        raise RuntimeError(
            f"geometry guard tripped: {len(bad)}/{len(offsets)} panels used a "
            f"non-corrected offset (sample={bad[:5]})"
        )
    n_differ = sum(1 for r in results if r["arms_differ"])
    if n_differ == 0:
        raise RuntimeError(
            "non-vacuity guard tripped: the honest arm is byte-identical to the EOD "
            "arm on every panel -- the intraday channel was silently dropped."
        )

    return {
        "n_panels": int(n_panels),
        "block_size_bdays": int(block_size),
        "boot_seed": int(boot_seed),
        "eod": _summarize(results, thr, "eod"),
        "honest": _summarize(results, thr, "honest"),
        "n_panels_arms_differ": int(n_differ),
        "wall_s": float(time.time() - t0),
        "geometry_attestation": {
            "expected_offset": UNREACHABLE,
            "unique_offsets_observed": sorted(set(offsets)),
            "all_attested_corrected": True,
            "n_panels_attested": len(offsets),
        },
        "panels": results,
    }
