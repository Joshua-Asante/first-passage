"""Q-ORPREM-1 matched-null harness — Phase 0 build (synthetic data only).

Implements the Phase 0 ticket of the pre-registration
``docs/briefs/pre-registration/2026-10-19-q-orprem-1-matched-null-prereg-DRAFT.md``
(§4.1 data/eligibility, §4.2 trade rule, §4.3 Δ₃ estimator + bootstrap, §6 gate
constants, §7 Phase 0 items (a)-(e)).  The engine is the vendored ``orb_lib.py``
in this camp (LF byte copy of archive ``5d47b4dc:lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py``,
sha256 ``e8b0caf8…5e9259``), imported BY FILE PATH so this harness can only use
that copy.  Every record this module produces carries ``orb_lib_sha256``.

No function here touches real data: decoding goes through ``orb_lib.load_bar_export``
(unchanged) via :func:`decode_export`, and everything downstream operates on
in-memory sessions.  Real-input entry points are the CLI in ``run_orprem.py``,
whose g0/score subcommands refuse (exit 2) unless the pre-registration status
line is FROZEN.

Library items 1–13 (the ticket's numbering):

 1. Constants — the frozen study constants (§4–§7): horizons, offsets, costs,
    thresholds, panel windows, bootstrap settings, support-routing thresholds,
    the vendored-engine sha256 pin.
 2. ``Session`` — one complete, guard-passing 26-bar RTH session (prices only;
    carries Aₐ, the previous complete session's mean bar range).
 3. ``WindowOutcome`` — one (day, w) window: ω, x = ln(ω/Aₐ), entry/exit, R.
 4. ``decode_export`` — ``orb_lib.load_bar_export`` unchanged + the Entry-row
    count / decode rate + the immediate ≤ 2025-08-31 date cut (§4.1).
 5. ``eligible_sessions`` — §4.1 eligibility: 26-bar completeness, the Aₐ
    lookback (may precede the panel window start), and the intra-RTH
    discontinuity guard (no RTH bar opens > 0.5% from the previous export
    row's close; a 09:30 bar with no predecessor makes the session
    ineligible).  Excluded sessions are listed with reasons.  Prices only.
 6. ``exec_win_h(day, w, H)`` — the §4.2 fixed-horizon trade rule.  Returns
    ``None`` iff the window is skipped (ω ≤ 0); ``entered=False`` iff R is
    undefined (no touch).  Parity: with H = remaining bars it reproduces the
    ``exec_win`` closure of ``orb_lib.placebo_within_day``, and at w = 0 it
    reproduces ``orb_lib.orb_backtest``.
 7. ``score_session`` — WindowOutcomes for a set of offsets at horizon ``H``
    (int, or the ``EXIT_CLOSE`` sentinel = run to the 15:45 bar).
 8. ``fit_band_and_cuts`` — §4.3 steps 1–2: trim band [p5, p95] over OR-window
    x (ω > 0), quintile cutpoints c1..c4 over the trimmed OR windows; both
    ``numpy.quantile`` linear (default), band inclusive.
 9. ``delta3`` — §4.3 steps 3–7: strata, R̄_OR, p_OR(s), the matched null N̄
    with p_OR renormalisation over null-empty strata, Δ₃, and the untrimmed
    OR mean reported alongside.
10. ``bootstrap_mean`` — the moving-block resampler of
    ``orb_lib.block_bootstrap_ci`` (same rng scheme, block starts uniform over
    [0, N−block], ⌈N/block⌉ blocks truncated to N), kept as the parity anchor.
11. ``bootstrap_delta`` — §4.3 inference: the session moving-block bootstrap of
    Δ₃ (weighted, band/cutpoints held fixed, p_OR and stratum means
    recomputed per replicate, renormalising replicates counted) and of the
    pooled Δ₀–Δ₂ rungs.
12. ``ladder`` — the §4.3 ladder: Δ₀ (net 1.11, exit at close, null w 1–23),
    Δ₁ (gross, exit at close, null w 2–23), Δ₂ (gross, H=8, null w 2–16),
    Δ₃ (gross, H=8, width-matched), each with its bootstrap interval, plus the
    attribution Δ₀−Δ₁, Δ₁−Δ₂, Δ₂−Δ₃.
13. ``g0_record`` — §7 Phase 1 prices-only pre-flight (no R): decode, date
    cut, eligibility and guard lists, band/cutpoints, per-stratum support and
    balance checks, the VOID-SUPPORT routing decision, optional E1 blend and
    overlap check.

Helper functions and the engine handle are underscore-private; nothing else is
public API.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

CAMP = Path(__file__).resolve().parent


def _load_orb_lib():
    """Import the vendored engine by file path — never another camp's copy."""
    path = CAMP / "orb_lib.py"
    key = "orb_lib"
    mod = sys.modules.get(key)
    if mod is not None and getattr(mod, "__file__", None) \
            and Path(mod.__file__).resolve() == path.resolve():
        return mod
    if mod is not None:
        key = "_orprem_vendored_orb_lib"
    spec = importlib.util.spec_from_file_location(key, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return module


ol = _load_orb_lib()


# ------------------------------------------------------------------ item 1
# Frozen study constants (§4.1–§4.3, §6, §7).  Do not change after any R exists.
OR_BARS: int = 2                    # §4.2 two-bar window
N_RTH_BARS: int = 26                # §4.1 bars 09:30 … 15:45 ET
OPEN_TOD: int = 9 * 60 + 30         # 09:30 ET
CLOSE_TOD: int = 15 * 60 + 45       # 15:45 ET (last bar-open; session ends 16:00)
BAR_MINUTES: int = 15
RTH_TODS: tuple[int, ...] = tuple(range(OPEN_TOD, CLOSE_TOD + 1, BAR_MINUTES))
H_PRIMARY: int = 8                  # §4.2 primary horizon (OR arm ends 12:00)
W_OR: int = 0                       # OR offset
W_NULL_D0: tuple[int, ...] = tuple(range(1, 24))   # Δ₀ null offsets {1..23}
W_NULL_D1: tuple[int, ...] = tuple(range(2, 24))   # Δ₁ null offsets {2..23}
W_NULL_D2: tuple[int, ...] = tuple(range(2, 17))   # Δ₂/Δ₃ null offsets {2..16}
EXIT_CLOSE: str = "close"           # score_session sentinel: run to the 15:45 bar
RT_COST_PT_BULENOX: float = 1.11    # Δ₀ only (§4.3 ladder: recorded Bulenox basis)
RT_COST_PT_TRADEIFY: float = 1.41   # reported context: $0.91/side + 1 tick at $2/pt
M_PREMIUM: float = 0.032            # §4 accept threshold (one-sided 95% upper < m)
FEED_SCOPE_BAND: tuple[float, float] = (0.05, 0.15)  # §6 feed-scoped Δ₀ band (reported)
TRIM_Q: tuple[float, float] = (0.05, 0.95)           # §4.3 trim band quantiles
STRATA_Q: tuple[float, float, float, float] = (0.20, 0.40, 0.60, 0.80)  # c1..c4
N_STRATA: int = 5
BOOT_BLOCK: int = 5                 # §4.3 bootstrap block length
BOOT_N: int = 10_000                # §4.3 B
BOOT_SEED: int = 42                 # §4.3 seed
BOOT_SEEDS_REPORTED: tuple[int, ...] = (123, 2026)   # §4.3 reported-only seeds
BOOT_BLOCK_REPORTED: int = 10       # §4.3 reported-only 10-session block
Q_LOWER: float = 2.5                # one-sided 97.5% lower bound percentile
Q_UPPER: float = 95.0               # one-sided 95% upper bound percentile
GUARD_MAX_JUMP: float = 0.005       # §4.1 intra-RTH discontinuity guard (0.5%)
DATE_CUT: date = date(2025, 8, 31)  # §4.1 date cut, immediately after decoding
PANEL_E2: tuple[date, date] = (date(2021, 1, 1), date(2025, 8, 31))     # primary
PANEL_E1: tuple[date, date] = (date(2019, 9, 1), date(2020, 12, 31))    # report only
E1_BLEND_SPLIT: date = date(2020, 6, 30)  # E1: 86a38 up to this date, dd9d8 after
DECODE_RATE_MIN: float = 0.99       # §6 VOID-PARITY decode-rate gate
OVERLAP_RATE_MIN: float = 0.995     # §6 E1 overlap gate (0.25 pt tolerance below)
OVERLAP_TOL_PT: float = 0.25
SUPPORT_MIN_WINDOWS: int = 200      # §6 VOID-SUPPORT routing, per stratum
SUPPORT_MIN_SESSIONS: int = 100
SUPPORT_MIN_OFFSETS: int = 5
SUPPORT_MAX_X_GAP: float = 0.10
ORB_LIB_SHA256: str = (
    "e8b0caf8032439ced8b565df9ce3a3077c7b685c0ddfe6e093493d78f25e9259"
)
PREREG_NAME: str = "2026-10-19-q-orprem-1-matched-null-prereg-DRAFT.md"

_RUNGS = (  # name, H_or, H_null, null offsets, cost, width-matched
    ("delta0", EXIT_CLOSE, EXIT_CLOSE, W_NULL_D0, RT_COST_PT_BULENOX, False),
    ("delta1", EXIT_CLOSE, EXIT_CLOSE, W_NULL_D1, 0.0, False),
    ("delta2", H_PRIMARY, H_PRIMARY, W_NULL_D2, 0.0, False),
    ("delta3", H_PRIMARY, H_PRIMARY, W_NULL_D2, 0.0, True),
)


# ------------------------------------------------------------------ items 2–3
@dataclass(frozen=True, eq=False)
class Session:
    """One eligible RTH session: 26 bars ordered by tod, plus Aₐ (§4.1)."""

    date: date
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    a_prev: float


@dataclass(frozen=True, eq=False)
class WindowOutcome:
    """One (day, w) window of §4.2.  ``r`` is nan iff no entry (undefined R)."""

    date: date
    w: int
    H: int
    omega: float
    x: float
    side: int          # +1 long, −1 short, 0 no entry
    entered: bool
    stopped: bool
    entry_px: float
    exit_px: float
    r: float


# ------------------------------------------------------------------ helpers
def _engine_sha256() -> str:
    return hashlib.sha256(Path(ol.__file__).read_bytes()).hexdigest()


def _sha256_file(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _h_close(w: int) -> int:
    """Horizon (bars) for 'exit at close': bars w+2 … 25 (the 15:45 bar)."""
    return N_RTH_BARS - OR_BARS - w


def _window_levels(day: Session, w: int):
    hi = float(np.nanmax(day.h[w:w + OR_BARS]))
    lo = float(np.nanmin(day.l[w:w + OR_BARS]))
    return hi, lo


def _window_x(day: Session, w: int):
    """(ω, x) for a window, or None if the window is skipped (ω ≤ 0).  No R."""
    hi, lo = _window_levels(day, w)
    omega = hi - lo
    if not (np.isfinite(hi) and np.isfinite(lo) and np.isfinite(omega)) or omega <= 0:
        return None
    if np.isfinite(day.a_prev) and day.a_prev > 0:
        x = float(np.log(omega / day.a_prev))
    else:
        x = float("nan")
    return omega, x


def _stratum_of(x: float, band, cuts) -> int:
    """Stratum 1–5 for x inside the (inclusive) band; 0 = trimmed out (§4.3)."""
    if not np.isfinite(x) or x < band[0] or x > band[1]:
        return 0
    return 1 + int(np.searchsorted(cuts, x, side="right"))


def _pooled(or_records, null_records) -> dict:
    """Unweighted rung point estimate: OR mean − pooled defined-null mean."""
    orv = [rec.r for rec in or_records if rec is not None and rec.entered]
    nuv = [rec.r for rec in null_records if rec is not None and rec.entered]
    om = float(np.mean(orv)) if orv else float("nan")
    nm = float(np.mean(nuv)) if nuv else float("nan")
    delta = om - nm if (np.isfinite(om) and np.isfinite(nm)) else float("nan")
    return {"delta": delta, "or_mean": om, "null_mean": nm,
            "n_or": len(orv), "n_null": len(nuv)}


def _blend_e1(df_a: pd.DataFrame, df_b: pd.DataFrame) -> pd.DataFrame:
    """E1 blend (§4.1): 86a38 rows through 2020-06-30, dd9d8 rows after."""
    a = df_a[df_a["d"] <= E1_BLEND_SPLIT]
    b = df_b[df_b["d"] > E1_BLEND_SPLIT]
    return (pd.concat([a, b], ignore_index=True)
            .sort_values("time").reset_index(drop=True))


def _overlap_check(df_a: pd.DataFrame, df_b: pd.DataFrame) -> dict:
    """§6 E1 overlap check: RTH bars matched on epoch, o/h/l/c within 0.25 pt."""
    def rth(d):
        m = d[(d["tod"] >= OPEN_TOD) & (d["tod"] <= CLOSE_TOD)]
        return m[["epoch", "open", "high", "low", "close"]]
    m = rth(df_a).merge(rth(df_b), on="epoch", suffixes=("_a", "_b"))
    n = len(m)
    if n == 0:
        return {"n_overlap": 0, "n_agree": 0, "rate": None}
    ok = np.ones(n, bool)
    for f in ("open", "high", "low", "close"):
        ok &= (m[f"{f}_a"] - m[f"{f}_b"]).abs().to_numpy() <= OVERLAP_TOL_PT
    k = int(ok.sum())
    return {"n_overlap": int(n), "n_agree": k, "rate": k / n}


# ------------------------------------------------------------------ item 4
def decode_export(path, *, date_cut: date = DATE_CUT):
    """Decode a BAR_EXPORT v0.2 CSV via the vendored loader, unchanged.

    Returns (df, info).  The date cut (§4.1) is applied immediately after
    decoding: rows dated after ``date_cut`` are dropped before any statistic.
    ``decode_rate`` is the rows the loader returns after its dedup divided by
    the file's ``Entry`` rows (the §6 VOID-PARITY gate; it counts rows only,
    so it is computed on the full decode, before the cut).
    """
    path = Path(path)
    df = ol.load_bar_export(path)
    raw = pd.read_csv(path, encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    n_entry_rows = int(raw["Type"].astype(str).str.startswith("Entry").sum())
    rows_decoded = int(len(df))
    decode_rate = (rows_decoded / n_entry_rows) if n_entry_rows else float("nan")
    max_before = str(df["d"].max()) if len(df) else None
    df = df[df["d"] <= date_cut].reset_index(drop=True)
    info = {"path": str(path), "sha256": _sha256_file(path),
            "n_entry_rows": n_entry_rows, "rows_decoded": rows_decoded,
            "decode_rate": decode_rate, "max_date_before_cut": max_before,
            "rows_after_cut": int(len(df)),
            "max_session_date": str(df["d"].max()) if len(df) else None}
    return df, info


# ------------------------------------------------------------------ item 5
def eligible_sessions(df: pd.DataFrame, start: date, end: date) -> dict:
    """§4.1 eligibility on a decoded (post-cut) dataframe.  Prices only.

    A session is eligible when (i) it has all 26 RTH bars, (ii) no RTH bar
    opens more than GUARD_MAX_JUMP (0.5%) from the close of the previous
    export row (for the 09:30 bar that is the 09:15 Globex bar; a 09:30 bar
    with no predecessor in the export makes the session ineligible), and
    (iii) Aₐ exists: the mean (high − low) over the 26 bars of the most
    recent *earlier* date with a complete RTH session, positive.  That date
    may precede ``start``.  Completeness, not guard status, qualifies a date
    as an Aₐ donor (the spec's wording is completeness only).

    Returns {"sessions": [Session … in date order], "excluded": [[date,
    reason] …], "complete_dates": […]}.
    """
    df = df.sort_values("time").reset_index(drop=True)
    tod = df["tod"].to_numpy()
    dcol = df["d"].to_numpy()
    opens = df["open"].to_numpy(float)
    highs = df["high"].to_numpy(float)
    lows = df["low"].to_numpy(float)
    closes = df["close"].to_numpy(float)
    in_rth = (tod >= OPEN_TOD) & (tod <= CLOSE_TOD)
    want = set(RTH_TODS)

    complete: dict[date, bool] = {}
    for d in pd.unique(dcol[in_rth]):
        t = tod[(dcol == d) & in_rth]
        complete[d] = len(t) == N_RTH_BARS and set(t.tolist()) == want
    complete_dates = sorted(d for d, ok in complete.items() if ok)

    sessions: list[Session] = []
    excluded: list[list] = []
    for d in sorted(x for x in pd.unique(dcol) if start <= x <= end):
        if not complete.get(d, False):
            excluded.append([d, "incomplete_rth"])
            continue
        pos = np.flatnonzero((dcol == d) & in_rth)   # tod-ascending
        # (ii) intra-RTH discontinuity guard, on export-row order
        if pos[0] == 0:
            excluded.append([d, "no_prior_bar"])
            continue
        prev_c = closes[pos - 1]
        o = opens[pos]
        if (not np.all(np.isfinite(prev_c)) or np.any(prev_c <= 0)
                or float(np.max(np.abs(o - prev_c) / prev_c)) > GUARD_MAX_JUMP):
            excluded.append([d, "intra_rth_discontinuity"])
            continue
        # (iii) Aₐ from the most recent earlier complete session
        prior = [p for p in complete_dates if p < d]
        if not prior:
            excluded.append([d, "no_prior_complete_session"])
            continue
        p = prior[-1]
        ppos = np.flatnonzero((dcol == p) & in_rth)
        a_prev = float(np.mean(highs[ppos] - lows[ppos]))
        if not np.isfinite(a_prev) or a_prev <= 0:
            excluded.append([d, "aa_not_positive"])
            continue
        sessions.append(Session(date=d, o=o.copy(), h=highs[pos].copy(),
                                l=lows[pos].copy(), c=closes[pos].copy(),
                                a_prev=a_prev))
    return {"sessions": sessions, "excluded": excluded,
            "complete_dates": complete_dates}


# ------------------------------------------------------------------ item 6
def exec_win_h(day: Session, w: int, H: int, *, cost_pt: float = 0.0):
    """The §4.2 fixed-horizon trade rule for window (w, w+1) of ``day``.

    Window bars w, w+1; horizon bars w+2 … w+1+H.  Entry on the first horizon
    bar touching the window high (long) or low (short), filled at the level; a
    both-touch bar takes the long side iff its open ≤ the window midpoint.
    Stop = opposite extreme, checked from the entry bar through the horizon
    end (the inherited approximation includes the entry bar); otherwise exit
    at the close of the last horizon bar.  R = signed P&L / ω, with
    ``cost_pt`` subtracted before dividing (Δ₀ only).

    Returns None iff the window is skipped (ω ≤ 0); otherwise a
    WindowOutcome whose ``entered`` is False iff R is undefined (no touch).
    """
    n = len(day.o)
    if not isinstance(H, (int, np.integer)) or isinstance(H, bool) or int(H) < 1:
        raise ValueError(f"H must be a positive int, got {H!r}")
    H = int(H)
    if w < 0 or w + OR_BARS - 1 > n - 1:
        raise ValueError(f"window out of range: w={w}, n={n}")
    end = w + 1 + H
    if end > n - 1:
        raise ValueError(f"horizon exceeds session bars: w={w}, H={H}, n={n}")
    hi, lo = _window_levels(day, w)
    omega = hi - lo
    if not (np.isfinite(hi) and np.isfinite(lo) and np.isfinite(omega)) or omega <= 0:
        return None
    if np.isfinite(day.a_prev) and day.a_prev > 0:
        x = float(np.log(omega / day.a_prev))
    else:
        x = float("nan")
    entry = None
    side = 0
    for j in range(w + OR_BARS, end + 1):
        bh = day.h[j]
        if not np.isfinite(bh):
            continue
        bl = day.l[j]
        up = bh >= hi
        dn = bl <= lo
        if up and dn:
            side = 1 if day.o[j] <= (hi + lo) / 2 else -1
            entry = hi if side == 1 else lo
            break
        if up:
            side, entry = 1, hi
            break
        if dn:
            side, entry = -1, lo
            break
    if entry is None:
        return WindowOutcome(day.date, w, H, omega, x, 0, False, False,
                             float("nan"), float("nan"), float("nan"))
    lo_rest = float(np.nanmin(day.l[w + OR_BARS:end + 1]))
    hi_rest = float(np.nanmax(day.h[w + OR_BARS:end + 1]))
    if side == 1:
        stopped = lo_rest <= lo
        exit_px = lo if stopped else float(day.c[end])
        pnl = exit_px - entry
    else:
        stopped = hi_rest >= hi
        exit_px = hi if stopped else float(day.c[end])
        pnl = entry - exit_px
    r = (pnl - cost_pt) / omega
    return WindowOutcome(day.date, w, H, omega, x, side, True, stopped,
                         float(entry), float(exit_px), float(r))


# ------------------------------------------------------------------ item 7
def score_session(day: Session, offsets: Sequence[int], H, *,
                  cost_pt: float = 0.0) -> list[WindowOutcome]:
    """WindowOutcomes for ``offsets`` at horizon ``H``.

    ``H`` is a bar count, or ``EXIT_CLOSE`` ("close"): each window's horizon
    then runs to the 15:45 bar (H = 24 − w).  Skipped windows (ω ≤ 0) are
    omitted from the returned list; undefined-R windows are kept (entered
    False) because §4.3/§6 count windows whether or not they would trade.
    """
    if isinstance(H, str) and H != EXIT_CLOSE:
        raise ValueError(f"unknown horizon sentinel {H!r}")
    out: list[WindowOutcome] = []
    for w in offsets:
        h = _h_close(int(w)) if isinstance(H, str) else int(H)
        rec = exec_win_h(day, int(w), h, cost_pt=cost_pt)
        if rec is not None:
            out.append(rec)
    return out


# ------------------------------------------------------------------ item 8
def fit_band_and_cuts(x_or: Iterable[float]):
    """§4.3 steps 1–2 from the OR windows' x values (ω > 0).

    Band = [p5, p95] (inclusive) over all of them; cutpoints c1..c4 are the
    quintiles of x over the trimmed OR windows.  Both use numpy.quantile with
    the default linear method.  Prices only — no R.
    """
    x = np.asarray(list(x_or), float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        raise ValueError("no OR windows with omega > 0")
    b = np.quantile(x, TRIM_Q)
    band = (float(b[0]), float(b[1]))
    t = x[(x >= band[0]) & (x <= band[1])]
    if t.size == 0:
        raise ValueError("trim band is empty")
    c = np.quantile(t, STRATA_Q)
    cuts = tuple(float(v) for v in c)
    return band, cuts


# ------------------------------------------------------------------ item 9
def delta3(or_records, null_records, band, cuts) -> dict:
    """§4.3 steps 3–7: Δ₃ = R̄_OR − N̄ (both arms trimmed to the band).

    Strata are [blo, c1), [c1, c2), [c2, c3), [c3, c4), [c4, bhi].  R̄_OR and
    p_OR(s) use the defined R of trimmed OR windows; N̄ = Σ p_OR(s) · mean of
    defined null R in s, renormalising p_OR over the non-empty strata when a
    stratum has no defined null R (the dropped strata are reported).  The
    untrimmed OR mean is reported alongside.  The trim uses x only.
    """
    or_defined = [rec for rec in or_records if rec is not None and rec.entered]
    or_kept = [rec for rec in or_defined if _stratum_of(rec.x, band, cuts) > 0]
    or_mean = float(np.mean([rec.r for rec in or_kept])) if or_kept else float("nan")
    untrimmed = (float(np.mean([rec.r for rec in or_defined])) if or_defined
                 else float("nan"))
    n_null = np.zeros(N_STRATA, int)
    s_null = np.zeros(N_STRATA)
    for rec in null_records:
        if rec is None or not rec.entered:
            continue
        s = _stratum_of(rec.x, band, cuts)
        if s == 0:
            continue
        n_null[s - 1] += 1
        s_null[s - 1] += rec.r
    p = np.zeros(N_STRATA, float)
    for rec in or_kept:
        p[_stratum_of(rec.x, band, cuts) - 1] += 1.0
    if len(or_kept):
        p /= p.sum()
    dropped = [s + 1 for s in range(N_STRATA) if p[s] > 0 and n_null[s] == 0]
    use = [s for s in range(N_STRATA) if p[s] > 0 and n_null[s] > 0]
    if use:
        wsum = sum(p[s] for s in use)
        nbar = float(sum(p[s] / wsum * (s_null[s] / n_null[s]) for s in use))
    else:
        nbar = float("nan")
    delta = or_mean - nbar if np.isfinite(nbar) else float("nan")
    return {"delta3": delta, "or_mean": or_mean, "matched_null": nbar,
            "untrimmed_or_mean": untrimmed, "p_or": [float(v) for v in p],
            "n_or": len(or_kept), "n_or_untrimmed": len(or_defined),
            "n_null_by_stratum": [int(v) for v in n_null],
            "renormalised_strata": dropped}


# ----------------------------------------------------------------- item 10
def bootstrap_mean(x, block: int = BOOT_BLOCK, n: int = BOOT_N,
                   seed: int = BOOT_SEED, q=(Q_LOWER, Q_UPPER)):
    """Moving-block bootstrap of a mean — orb_lib.block_bootstrap_ci's scheme.

    Same rng, pool (block starts uniform over [0, N−block]), ⌈N/block⌉ blocks
    truncated to N, and per-replicate draw order as the vendored
    ``orb_lib.block_bootstrap_ci``, so the two agree to floating-point
    equality for identical arguments.  Default q is this study's one-sided
    pair (2.5, 95).  Returns (lo, hi, frac ≤ 0) like the engine function.
    """
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    N = len(x)
    if N < block + 1:
        block = max(1, N // 2)
    nblocks = int(np.ceil(N / block))
    pool = np.arange(0, N - block + 1)
    stats = np.empty(n)
    for i in range(n):
        st = rng.choice(pool, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]).ravel()[:N]
        stats[i] = x[idx].mean()
    lo, hi = np.percentile(stats, q)
    return float(lo), float(hi), float((stats <= 0).mean())


# ----------------------------------------------------------------- item 11
def bootstrap_delta(sessions, *, null_offsets, or_offsets=(W_OR,), H_or,
                    H_null, cost_pt: float = 0.0, band=None, cuts=None,
                    weighted: bool = False, block: int = BOOT_BLOCK,
                    n: int = BOOT_N, seed: int = BOOT_SEED,
                    q=(Q_LOWER, Q_UPPER)) -> dict:
    """§4.3 inference: session moving-block bootstrap of a Δ rung.

    Sessions are resampled in date order, non-circular, exactly as
    ``bootstrap_mean``/``orb_lib.block_bootstrap_ci`` draw blocks; every
    window of a resampled session moves with it.  With ``weighted`` the
    statistic is Δ₃ (p_OR and stratum means recomputed per replicate against
    the fixed band/cutpoints, p_OR renormalised over null-empty strata, those
    replicates counted); otherwise it is the pooled Δ of a Δ₀–Δ₂ rung.
    """
    N = len(sessions)
    if N == 0:
        raise ValueError("no sessions to bootstrap")
    if weighted and (band is None or cuts is None):
        raise ValueError("weighted bootstrap needs the fixed band and cuts")
    K = N_STRATA if weighted else 1
    or_n = np.zeros((N, K))
    or_s = np.zeros((N, K))
    nu_n = np.zeros((N, K))
    nu_s = np.zeros((N, K))
    for i, s in enumerate(sessions):
        for rec in score_session(s, or_offsets, H_or, cost_pt=cost_pt):
            if not rec.entered:
                continue
            k = (_stratum_of(rec.x, band, cuts) - 1) if weighted else 0
            if k < 0:
                continue
            or_n[i, k] += 1.0
            or_s[i, k] += rec.r
        for rec in score_session(s, null_offsets, H_null, cost_pt=cost_pt):
            if not rec.entered:
                continue
            k = (_stratum_of(rec.x, band, cuts) - 1) if weighted else 0
            if k < 0:
                continue
            nu_n[i, k] += 1.0
            nu_s[i, k] += rec.r
    rng = np.random.default_rng(seed)
    blk = int(block)
    if N < blk + 1:
        blk = max(1, N // 2)
    nblocks = int(np.ceil(N / blk))
    pool = np.arange(0, N - blk + 1)
    stats = np.full(n, np.nan)
    renorm = 0
    for i in range(n):
        st = rng.choice(pool, size=nblocks)
        idx = (st[:, None] + np.arange(blk)[None, :]).ravel()[:N]
        on = or_n[idx].sum(axis=0)
        os_ = or_s[idx].sum(axis=0)
        nn = nu_n[idx].sum(axis=0)
        ns = nu_s[idx].sum(axis=0)
        if weighted:
            tot = on.sum()
            if tot <= 0:
                continue
            p = on / tot
            active = p > 0
            if (active & (nn <= 0)).any():
                renorm += 1
            use = active & (nn > 0)
            if not use.any():
                continue
            w = p[use] / p[use].sum()
            nbar = float((w * (ns[use] / nn[use])).sum())
            stats[i] = (os_.sum() / tot) - nbar
        else:
            if on.sum() <= 0 or nn.sum() <= 0:
                continue
            stats[i] = os_.sum() / on.sum() - ns.sum() / nn.sum()
    lo, hi = np.nanpercentile(stats, q)
    return {"lo": float(lo), "hi": float(hi), "stats": stats, "n": int(n),
            "block": int(blk), "seed": int(seed),
            "renormalised_replicates": int(renorm),
            "nan_replicates": int(np.isnan(stats).sum())}


# ----------------------------------------------------------------- item 12
def ladder(sessions, *, band=None, cuts=None, block: int = BOOT_BLOCK,
           n: int = BOOT_N, seed: int = BOOT_SEED) -> dict:
    """The §4.3 ladder Δ₀–Δ₃ on one panel, with intervals and attribution.

    If ``band``/``cuts`` are not given they are fitted once from this panel's
    OR windows (E2 semantics); pass E2's band/cuts unchanged for E1.
    """
    if band is None or cuts is None:
        xs = [rec.x for s in sessions
              for rec in score_session(s, (W_OR,), H_PRIMARY)]
        band, cuts = fit_band_and_cuts(xs)
    rungs = {}
    for name, h_or, h_null, offsets, cost, weighted in _RUNGS:
        or_recs = [rec for s in sessions
                   for rec in score_session(s, (W_OR,), h_or, cost_pt=cost)]
        null_recs = [rec for s in sessions
                     for rec in score_session(s, offsets, h_null, cost_pt=cost)]
        point = (delta3(or_recs, null_recs, band, cuts) if weighted
                 else _pooled(or_recs, null_recs))
        rung = dict(point)
        boot = bootstrap_delta(sessions, or_offsets=(W_OR,), null_offsets=offsets,
                               H_or=h_or, H_null=h_null, cost_pt=cost,
                               band=band, cuts=cuts, weighted=weighted,
                               block=block, n=n, seed=seed)
        rung.update({"lo": boot["lo"], "hi": boot["hi"],
                     "renormalised_replicates": boot["renormalised_replicates"]})
        rungs[name] = rung
    attr = {
        "d0_minus_d1": rungs["delta0"]["delta"] - rungs["delta1"]["delta"],
        "d1_minus_d2": rungs["delta1"]["delta"] - rungs["delta2"]["delta"],
        "d2_minus_d3": rungs["delta2"]["delta"] - rungs["delta3"]["delta3"],
    }
    return {"engine_sha256": _engine_sha256(), "band": list(band),
            "cuts": list(cuts), "n_sessions": len(sessions), "rungs": rungs,
            "attribution": attr,
            "bootstrap": {"block": int(block), "n": int(n), "seed": int(seed)}}


# ----------------------------------------------------------------- item 13
def g0_record(e2_csv, e1_csvs=(), *, date_cut: date = DATE_CUT) -> dict:
    """§7 Phase 1 blind pre-flight: prices only, no R is computed here.

    Decodes the inputs (immediate date cut), asserts the max session date,
    lists eligibility/guard exclusions, fixes the trim band and cutpoints,
    runs the §6 per-stratum support and balance checks on trimmed windows
    (counted whether or not they would trade) and decides the VOID-SUPPORT
    routing.  With two E1 files it also runs the epoch-matched RTH overlap
    check and blends the E1 panel.
    """
    rec = {"phase": "G0", "date_cut": date_cut.isoformat(),
           "orb_lib_sha256": _engine_sha256(), "inputs": {}, "panels": {}}
    df, info = decode_export(e2_csv, date_cut=date_cut)
    if info["max_session_date"] is None \
            or date.fromisoformat(info["max_session_date"]) > date_cut:
        raise ValueError(f"date cut violated: max session date "
                         f"{info['max_session_date']} > {date_cut}")
    rec["inputs"]["e2"] = info
    elig = eligible_sessions(df, *PANEL_E2)
    sessions = elig["sessions"]

    or_x: list[float] = []
    or_n_s = np.zeros(N_STRATA, int)
    or_x_s = np.zeros(N_STRATA)
    for s in sessions:
        g = _window_x(s, W_OR)
        if g is None:
            continue
        or_x.append(g[1])
    band, cuts = fit_band_and_cuts(or_x)
    for xv in or_x:
        st = _stratum_of(xv, band, cuts)
        if st > 0:
            or_n_s[st - 1] += 1
            or_x_s[st - 1] += xv

    null_n = np.zeros(N_STRATA, int)
    null_dates: list[set] = [set() for _ in range(N_STRATA)]
    null_offsets_s: list[set] = [set() for _ in range(N_STRATA)]
    null_x_s = np.zeros(N_STRATA)
    for s in sessions:
        for w in W_NULL_D2:
            g = _window_x(s, w)
            if g is None:
                continue
            st = _stratum_of(g[1], band, cuts)
            if st == 0:
                continue
            k = st - 1
            null_n[k] += 1
            null_dates[k].add(s.date)
            null_offsets_s[k].add(w)
            null_x_s[k] += g[1]

    support = {}
    for k in range(N_STRATA):
        mean_or = float(or_x_s[k] / or_n_s[k]) if or_n_s[k] else float("nan")
        mean_nu = float(null_x_s[k] / null_n[k]) if null_n[k] else float("nan")
        gap = (abs(mean_or - mean_nu)
               if (np.isfinite(mean_or) and np.isfinite(mean_nu)) else float("inf"))
        ok = bool(null_n[k] >= SUPPORT_MIN_WINDOWS
                  and len(null_dates[k]) >= SUPPORT_MIN_SESSIONS
                  and len(null_offsets_s[k]) >= SUPPORT_MIN_OFFSETS
                  and gap <= SUPPORT_MAX_X_GAP)
        support[str(k + 1)] = {
            "null_windows": int(null_n[k]),
            "null_sessions": len(null_dates[k]),
            "null_offsets": len(null_offsets_s[k]),
            "mean_x_or": mean_or, "mean_x_null": mean_nu, "x_gap": gap,
            "pass": ok}
    routing = ("width_matched" if all(v["pass"] for v in support.values())
               else "width_unmatched")

    rec["panels"]["E2"] = {
        "window": [PANEL_E2[0].isoformat(), PANEL_E2[1].isoformat()],
        "max_session_date": info["max_session_date"],
        "decode_rate": info["decode_rate"],
        "n_sessions": len(sessions),
        "excluded": [[str(d), r] for d, r in elig["excluded"]],
        "n_or_windows": len(or_x),
        "band": list(band), "cuts": list(cuts),
        "support": support, "routing": routing}

    e1 = list(e1_csvs)
    if e1:
        if len(e1) != 2:
            raise ValueError("E1 needs exactly two files (86a38 then dd9d8)")
        dfs = []
        for i, p in enumerate(e1):
            d_i, info_i = decode_export(p, date_cut=date_cut)
            rec["inputs"][f"e1_{i}"] = info_i
            dfs.append(d_i)
        overlap = _overlap_check(*dfs)
        blended = _blend_e1(*dfs)
        el1 = eligible_sessions(blended, *PANEL_E1)
        rec["panels"]["E1"] = {
            "window": [PANEL_E1[0].isoformat(), PANEL_E1[1].isoformat()],
            "overlap": overlap,
            "overlap_ok": (overlap["rate"] is not None
                           and overlap["rate"] >= OVERLAP_RATE_MIN),
            "n_sessions": len(el1["sessions"]),
            "excluded": [[str(d), r] for d, r in el1["excluded"]]}
    return rec
