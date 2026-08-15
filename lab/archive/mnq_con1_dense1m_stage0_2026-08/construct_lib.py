"""Q-MNQDTL-CON-1 Stage-0 — ES/NQ divergence construct (frozen PREREG_G0).

Harness only. Real-panel path PnL is gated by explore GO (see run_construct_g0.py).
Unit tests use synthetic fixtures — no vendor bars required.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

# ---- FROZEN (PREREG_G0) ------------------------------------------------------
GATE_G = 10.0
RT_PT = 1.41
LOOKBACK_MIN = 5          # close[t-1] / close[t-6] → 5 completed minutes
THETA_SESSIONS = 20
K_INTRINSIC = 1
DSR_FLOOR = 0.650
RANDOM_SEED = 20260808
PLACEBO_REPS = 1000
RTH_OPEN_MIN = 9 * 60 + 30   # 09:30
RTH_CLOSE_MIN = 16 * 60      # exclusive end → last start 15:59

# Arithmetic bars (G=10, RT=1.41) — disclosure / cheap falsifier
EM1_EDGE_R = 0.40
EM1_PRED_PT = GATE_G * EM1_EDGE_R + RT_PT          # 5.41
NEDGE_PRED_PT = RT_PT                               # 1.41 for net R > 0
EM1_WR_BAR = (1.0 + EM1_EDGE_R + RT_PT / GATE_G) / 2.0   # 0.7705
NEDGE_WR_BAR = (1.0 + RT_PT / GATE_G) / 2.0               # 0.5705

TNEC_LIMBS = ("N-ACT", "N-SURV", "N-EDGE", "N-SHAPE", "N-SIZE")

# Default panel paths (cache reuse; $0) — used only after explore GO
MNQ_DBN_DEFAULT = "ohlcv-1m_continuous_b1fa4ae6b7ba9af2.dbn"
ES_DBN_DEFAULT = "ohlcv-1m_continuous_17b6c454408be685.dbn"


@dataclass(frozen=True)
class CheapFalsifierResult:
    em1_pred_pt: float
    nedge_pred_pt: float
    em1_wr_bar: float
    nedge_wr_bar: float
    prior_art_effect_pt: float | None
    falsified_by_arithmetic: bool
    arithmetic_bar_hit: str | None
    sign_ok: bool
    entry_named: bool
    verdict: str
    detail: str


def arithmetic_bars() -> dict[str, float]:
    return {
        "em1_pred_pt": EM1_PRED_PT,
        "nedge_pred_pt": NEDGE_PRED_PT,
        "em1_wr_bar": EM1_WR_BAR,
        "nedge_wr_bar": NEDGE_WR_BAR,
        "gate_g": GATE_G,
        "rt_pt": RT_PT,
    }


def cheap_falsifier(
    *,
    prior_art_effect_pt: float | None = None,
    entry_named: bool = True,
    sign_relative_contrarian: bool = True,
) -> CheapFalsifierResult:
    """Parent-side cheap falsifier — no path PnL.

    If a prior-art effect (points) is supplied and is < bar/2 for either EM1 or
    N-EDGE pred bar, return FALSIFIED-BY-ARITHMETIC. Unnamed entry / inverted
    sign also fail freeze licensing.
    """
    bars = arithmetic_bars()
    falsified = False
    hit: str | None = None
    if prior_art_effect_pt is not None:
        for name, bar in (
            ("EM1", bars["em1_pred_pt"]),
            ("N-EDGE", bars["nedge_pred_pt"]),
        ):
            if prior_art_effect_pt < (bar / 2.0):
                falsified = True
                hit = name
                break
    if not entry_named:
        return CheapFalsifierResult(
            em1_pred_pt=bars["em1_pred_pt"],
            nedge_pred_pt=bars["nedge_pred_pt"],
            em1_wr_bar=bars["em1_wr_bar"],
            nedge_wr_bar=bars["nedge_wr_bar"],
            prior_art_effect_pt=prior_art_effect_pt,
            falsified_by_arithmetic=False,
            arithmetic_bar_hit=None,
            sign_ok=sign_relative_contrarian,
            entry_named=False,
            verdict="FALSIFIED",
            detail="ENTRY unnamed — Stage-0 STOP (cannot name causal entry)",
        )
    if not sign_relative_contrarian:
        return CheapFalsifierResult(
            em1_pred_pt=bars["em1_pred_pt"],
            nedge_pred_pt=bars["nedge_pred_pt"],
            em1_wr_bar=bars["em1_wr_bar"],
            nedge_wr_bar=bars["nedge_wr_bar"],
            prior_art_effect_pt=prior_art_effect_pt,
            falsified_by_arithmetic=False,
            arithmetic_bar_hit=None,
            sign_ok=False,
            entry_named=True,
            verdict="FALSIFIED",
            detail="sign inverted — own-instrument momentum / C5-dead (D5-RECOST-1)",
        )
    if falsified:
        return CheapFalsifierResult(
            em1_pred_pt=bars["em1_pred_pt"],
            nedge_pred_pt=bars["nedge_pred_pt"],
            em1_wr_bar=bars["em1_wr_bar"],
            nedge_wr_bar=bars["nedge_wr_bar"],
            prior_art_effect_pt=prior_art_effect_pt,
            falsified_by_arithmetic=True,
            arithmetic_bar_hit=hit,
            sign_ok=True,
            entry_named=True,
            verdict="FALSIFIED-BY-ARITHMETIC",
            detail=f"prior-art effect {prior_art_effect_pt} < {hit} bar/2",
        )
    return CheapFalsifierResult(
        em1_pred_pt=bars["em1_pred_pt"],
        nedge_pred_pt=bars["nedge_pred_pt"],
        em1_wr_bar=bars["em1_wr_bar"],
        nedge_wr_bar=bars["nedge_wr_bar"],
        prior_art_effect_pt=prior_art_effect_pt,
        falsified_by_arithmetic=False,
        arithmetic_bar_hit=None,
        sign_ok=True,
        entry_named=True,
        verdict="CHEAP_FALSIFIER_OK",
        detail=(
            "arithmetic bars disclosed; entry named; sign relative-contrarian; "
            "no prior-art effect to compare"
            if prior_art_effect_pt is None
            else "arithmetic bars disclosed; prior-art clears bar/2"
        ),
    )


def format_tnec_verdict(
    limbs: dict[str, str] | None = None,
    *,
    bust: str = "U",
    p_pass: str = "U",
    mu_disclosed: str = "U",
) -> str:
    """TNEC verdict string; unscored limbs typed U until their GO."""
    resolved = {k: "U" for k in TNEC_LIMBS}
    if limbs:
        for k, v in limbs.items():
            if k not in resolved:
                raise KeyError(f"unknown TNEC limb: {k}")
            resolved[k] = v
    limb_s = " ".join(resolved[k] for k in TNEC_LIMBS)
    return f"{limb_s} | {bust} | {p_pass} | {mu_disclosed}"


def r_from_pts(pts: float, stop_pt: float = GATE_G, rt_pt: float = RT_PT) -> float:
    return (pts - rt_pt) / stop_pt


def path_pts_session_flat(
    entry: float,
    side: int,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    start: int,
    stop_pt: float = GATE_G,
) -> tuple[float, str]:
    """Gross points: hard stop G, else flat at last in-session close.

    side: +1 long, -1 short. No 1R take-profit in this cell (PREREG_G0).
    """
    n = len(high)
    stop_level = entry - side * stop_pt
    for j in range(start, n):
        if side > 0:
            hit_stop = low[j] <= stop_level
        else:
            hit_stop = high[j] >= stop_level
        if hit_stop:
            return -stop_pt, "stop"
    return side * (close[n - 1] - entry), "flat"


def log_return_lookback(close: np.ndarray, t: int, lookback: int = LOOKBACK_MIN) -> float:
    """r(t) = log(close[t-1] / close[t-6]) for lookback=5. NaN if unavailable."""
    i1 = t - 1
    i0 = t - 1 - lookback
    if i0 < 0 or i1 < 0 or i1 >= len(close):
        return float("nan")
    c1 = float(close[i1])
    c0 = float(close[i0])
    if c0 <= 0.0 or c1 <= 0.0:
        return float("nan")
    return float(np.log(c1 / c0))


def divergence_series(
    close_es: np.ndarray,
    close_nq: np.ndarray,
    lookback: int = LOOKBACK_MIN,
) -> np.ndarray:
    """d(t) = r_ES(t) - r_NQ(t) on a joined RTH series (same length / alignment)."""
    n = len(close_es)
    if len(close_nq) != n:
        raise ValueError("ES/NQ close series length mismatch")
    d = np.full(n, np.nan, dtype=float)
    for t in range(n):
        r_es = log_return_lookback(close_es, t, lookback)
        r_nq = log_return_lookback(close_nq, t, lookback)
        if np.isfinite(r_es) and np.isfinite(r_nq):
            d[t] = r_es - r_nq
    return d


def session_theta(
    abs_d_by_session: list[np.ndarray],
    session_index: int,
    window: int = THETA_SESSIONS,
) -> float:
    """θ for session at session_index from trailing `window` completed sessions."""
    if session_index < window:
        return float("nan")
    chunks = abs_d_by_session[session_index - window : session_index]
    parts = [c[~np.isnan(c)] for c in chunks if len(c)]
    if not parts:
        return float("nan")
    vals = np.concatenate(parts)
    if len(vals) == 0:
        return float("nan")
    return float(np.median(vals))


def entry_side_at(d_t: float, theta_t: float) -> int:
    """+1 long, -1 short, 0 flat. Relative contrarian — do not invert."""
    if not (np.isfinite(d_t) and np.isfinite(theta_t) and theta_t > 0.0):
        return 0
    if d_t >= theta_t:
        return +1
    if d_t <= -theta_t:
        return -1
    return 0


def _exit_bar(
    entry: float,
    side: int,
    high: np.ndarray,
    low: np.ndarray,
    start: int,
    stop_pt: float,
) -> int:
    n = len(high)
    stop_level = entry - side * stop_pt
    for j in range(start, n):
        if side > 0 and low[j] <= stop_level:
            return j
        if side < 0 and high[j] >= stop_level:
            return j
    return n - 1


def simulate_session_trades(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close_mnq: np.ndarray,
    d: np.ndarray,
    theta: float,
    stop_pt: float = GATE_G,
) -> list[dict]:
    """One RTH session: signals → at most one open position at a time (EM3)."""
    trades: list[dict] = []
    pos_end = -1
    n = len(open_)
    for t in range(n):
        if t <= pos_end:
            continue
        side = entry_side_at(float(d[t]), theta)
        if side == 0:
            continue
        pts, kind = path_pts_session_flat(
            float(open_[t]), side, high, low, close_mnq, t, stop_pt=stop_pt
        )
        exit_bar = _exit_bar(float(open_[t]), side, high, low, t, stop_pt)
        trades.append(
            {
                "entry_i": t,
                "side": side,
                "pts": pts,
                "kind": kind,
                "R": r_from_pts(pts, stop_pt),
                "exit_i": exit_bar,
            }
        )
        pos_end = exit_bar
    return trades


def score_arm_rs(rs: Iterable[float]) -> dict:
    """Minimal arm summary for harness/tests (full CI/DSR at explore GO)."""
    arr = np.asarray(list(rs), dtype=float)
    if len(arr) == 0:
        return {"n": 0, "mean_R": float("nan"), "wr": float("nan")}
    return {
        "n": int(len(arr)),
        "mean_R": float(arr.mean()),
        "wr": float((arr > 0).mean()),
    }


def g0_freeze_verdict_template() -> str:
    """Pre-explore template: all TNEC limbs U."""
    return format_tnec_verdict()


def explore_go_present(here) -> bool:
    """True iff operator dropped the gitignored EXPLORE_GO.md token."""
    from pathlib import Path

    return (Path(here) / "EXPLORE_GO.md").is_file()


# ---- Explore scoring (real panels only after EXPLORE_GO) ---------------------
N_BOOT = 10_000
N_FLOOR_TRADES = 30
DSR_PROB_FLOOR = 0.95  # Bailey–LdP DSR pass threshold
ANN_SR_FLOOR = DSR_FLOOR  # K=1 ladder floor (PREREG "DSR ≥ 0.650")


def log_return_lookback_vec(close: np.ndarray, lookback: int = LOOKBACK_MIN) -> np.ndarray:
    """Vectorized r(t) = log(close[t-1] / close[t-1-lookback])."""
    n = len(close)
    out = np.full(n, np.nan, dtype=float)
    if n <= lookback + 1:
        return out
    t = np.arange(lookback + 1, n)
    c1 = close[t - 1]
    c0 = close[t - 1 - lookback]
    ok = (c0 > 0.0) & (c1 > 0.0)
    out[t[ok]] = np.log(c1[ok] / c0[ok])
    return out


def divergence_series_vec(
    close_es: np.ndarray,
    close_nq: np.ndarray,
    lookback: int = LOOKBACK_MIN,
) -> np.ndarray:
    if len(close_es) != len(close_nq):
        raise ValueError("ES/NQ close series length mismatch")
    r_es = log_return_lookback_vec(close_es, lookback)
    r_nq = log_return_lookback_vec(close_nq, lookback)
    d = r_es - r_nq
    d[~(np.isfinite(r_es) & np.isfinite(r_nq))] = np.nan
    return d


def session_block_bootstrap_mean(
    session_rs: list[np.ndarray],
    n: int = N_BOOT,
    seed: int = RANDOM_SEED,
) -> tuple[float, float]:
    """95% CI on pooled mean R; resample whole sessions with replacement."""
    if not session_rs:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    n_s = len(session_rs)
    means = np.empty(n)
    for i in range(n):
        idx = rng.integers(0, n_s, n_s)
        samp = np.concatenate([session_rs[j] for j in idx])
        means[i] = float(samp.mean()) if len(samp) else float("nan")
    lo, hi = np.nanpercentile(means, [2.5, 97.5])
    return float(lo), float(hi)


def path_r_at_clocks(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    side: int,
    clocks: np.ndarray,
    stop_pt: float = GATE_G,
) -> np.ndarray:
    """Net R for `side` entered at each clock (independent; not EM3-serialized)."""
    out = np.full(len(clocks), np.nan, dtype=float)
    for k, t in enumerate(clocks):
        pts, _ = path_pts_session_flat(
            float(open_[t]), side, high, low, close, int(t), stop_pt=stop_pt
        )
        out[k] = r_from_pts(pts, stop_pt)
    return out


def within_session_r_shuffle_placebo_means(
    session_packs: list[dict],
    n: int = PLACEBO_REPS,
    seed: int = RANDOM_SEED,
) -> np.ndarray:
    """PREREG placebo: within-session path-R shuffle onto entry clocks.

    For each session with trades of a given side, build path-R at every RTH
    clock for that side, shuffle those R values, and assign shuffled R to the
    session's actual entry clocks. Global mean over all such assigned R is one
    placebo draw. (Shuffling observed trade-R alone leaves mean invariant.)
    """
    if not session_packs:
        return np.array([])
    rng = np.random.default_rng(seed)
    stats = np.empty(n)
    for i in range(n):
        vals: list[float] = []
        for pack in session_packs:
            clocks = pack["entry_clocks"]
            if len(clocks) == 0:
                continue
            path_r = pack["path_r_all_clocks"]
            shuffled = path_r.copy()
            rng.shuffle(shuffled)
            # Map entry clocks → shuffled pool via position index into session bars
            for t in clocks:
                vals.append(float(shuffled[int(t)]))
        stats[i] = float(np.mean(vals)) if vals else float("nan")
    return stats


def halves_mean_sign(
    trades: list[dict],
    session_key: str = "session",
) -> tuple[float, float, bool]:
    """Older/newer half by session date; returns (mean_h1, mean_h2, signs_agree)."""
    if not trades:
        return float("nan"), float("nan"), False
    by_sess: dict = {}
    for tr in trades:
        by_sess.setdefault(tr[session_key], []).append(tr["R"])
    dates = sorted(by_sess.keys())
    if len(dates) < 2:
        return float("nan"), float("nan"), False
    mid = len(dates) // 2
    h1 = np.concatenate([by_sess[d] for d in dates[:mid]])
    h2 = np.concatenate([by_sess[d] for d in dates[mid:]])
    m1 = float(h1.mean()) if len(h1) else float("nan")
    m2 = float(h2.mean()) if len(h2) else float("nan")
    if not (np.isfinite(m1) and np.isfinite(m2)):
        return m1, m2, False
    agree = (m1 == 0.0 and m2 == 0.0) or (m1 > 0 and m2 > 0) or (m1 < 0 and m2 < 0)
    return m1, m2, bool(agree)


def ann_sr_and_dsr(daily_r: list[float], k_intrinsic: int = K_INTRINSIC) -> tuple[float, float]:
    """Daily net-R series → annSR and Bailey–LdP DSR (K_intrinsic trials)."""
    import sys
    from pathlib import Path

    lab = Path(__file__).resolve().parents[3]
    if str(lab) not in sys.path:
        sys.path.insert(0, str(lab))
    from research_utils.deflated_sharpe import (  # noqa: WPS433
        deflated_sharpe,
        expected_max_sharpe,
        moments_from_returns,
    )

    if len(daily_r) < 3:
        return float("nan"), float("nan")
    sr, n_days, skew, kurt = moments_from_returns(daily_r)
    ann = float(sr * np.sqrt(252.0))
    sr0 = expected_max_sharpe(k_intrinsic, 1.0 / max(2, n_days))
    dsr = float(deflated_sharpe(sr, n_days, skew, kurt, sr0))
    return ann, dsr


def verdict_arm(
    *,
    n: int,
    mean_r: float,
    ci: tuple[float, float],
    placebo_means: np.ndarray,
    halves_agree: bool,
    ann_sr: float,
    dsr: float,
) -> str:
    """Per-arm explore gate (PREREG §3). Precedence: VOID → FALSIFIED → SHAPE-CLEAR."""
    if n < N_FLOOR_TRADES:
        return "VOID"
    if not (np.isfinite(mean_r) and np.isfinite(ci[0]) and np.isfinite(ci[1])):
        return "VOID"
    # CI must exclude 0; mean must be positive for the arm's intended edge
    if mean_r <= 0.0 or ci[0] <= 0.0 <= ci[1]:
        return "FALSIFIED"
    if len(placebo_means) and np.isfinite(placebo_means).any():
        p = float(np.mean(placebo_means >= mean_r))
        if p >= 0.05:
            return "FALSIFIED"
    if not halves_agree:
        return "VOID"
    if not (np.isfinite(ann_sr) and ann_sr >= ANN_SR_FLOOR):
        return "FALSIFIED"
    if not (np.isfinite(dsr) and dsr >= DSR_PROB_FLOOR):
        return "FALSIFIED"
    return "SHAPE-CLEAR"


def score_arm_full(
    trades: list[dict],
    session_packs: list[dict],
    daily_r: list[float],
) -> dict:
    """Full PREREG §3 arm score (CI / placebo / halves / DSR)."""
    rs = [t["R"] for t in trades]
    n = len(rs)
    mean_r = float(np.mean(rs)) if n else float("nan")
    wr = float(np.mean(np.asarray(rs) > 0)) if n else float("nan")
    by_sess: dict = {}
    for t in trades:
        by_sess.setdefault(t["session"], []).append(t["R"])
    session_rs = [np.asarray(v, float) for v in by_sess.values()]
    ci = session_block_bootstrap_mean(session_rs) if session_rs else (float("nan"), float("nan"))
    placebo = within_session_r_shuffle_placebo_means(session_packs)
    p_placebo = (
        float(np.mean(placebo >= mean_r))
        if n and len(placebo) and np.isfinite(placebo).any()
        else float("nan")
    )
    h1, h2, agree = halves_mean_sign(trades)
    ann_sr, dsr = ann_sr_and_dsr(daily_r) if daily_r else (float("nan"), float("nan"))
    kinds = [t["kind"] for t in trades]
    stop_rate = float(np.mean([k == "stop" for k in kinds])) if kinds else float("nan")
    mae = float(np.max([-t["pts"] for t in trades])) if trades else float("nan")
    mfe = float(np.max([t["pts"] for t in trades])) if trades else float("nan")
    v = verdict_arm(
        n=n,
        mean_r=mean_r,
        ci=ci,
        placebo_means=placebo,
        halves_agree=agree,
        ann_sr=ann_sr,
        dsr=dsr,
    )
    return {
        "n": n,
        "mean_R": mean_r,
        "wr": wr,
        "ci95": [ci[0], ci[1]],
        "placebo_p": p_placebo,
        "halves": {"h1_mean": h1, "h2_mean": h2, "sign_agree": agree},
        "ann_sr": ann_sr,
        "dsr": dsr,
        "stop_rate": stop_rate,
        "mae_pt": mae,
        "mfe_pt": mfe,
        "verdict": v,
    }


def overall_explore_verdict(long_v: str, short_v: str) -> str:
    """Combine per-arm verdicts. Either arm SHAPE-CLEAR → cell SHAPE-CLEAR;
    both FALSIFIED → FALSIFIED; else VOID."""
    arms = {long_v, short_v}
    if "SHAPE-CLEAR" in arms:
        return "SHAPE-CLEAR"
    if arms <= {"FALSIFIED"}:
        return "FALSIFIED"
    return "VOID"
