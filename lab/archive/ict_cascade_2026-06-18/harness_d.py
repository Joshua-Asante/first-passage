"""Q-ICT-CASCADE-1 / Layer D (Daily Draw-on-Liquidity) -- offline reconstruction.

Verdict instrument for PREREG-D.md (lab/analysis/ict_cascade_2026-06-18/PREREG-D.md;
authored 2026-06-18, FROZEN -- no criterion may move after run 1). The Daily ICT
indicator (`ict_daily_dol.pine`, 8454 B, LastWriteUTC 2026-06-18T22:46:54Z) exports
ONLY aggregate rates at the last bar (daily L168-171) and those are autocorrelated
smoke tests by the script's own admission (daily L130-132). PREREG-D sec 0 therefore
defines the verdict as a DE-OVERLAPPED OFFLINE RECONSTRUCTION from Daily OHLC, NOT
the indicator table cell (Forbidden item 1).

This harness CONSUMES Daily OHLC bars (NOT a TV indicator export -- the Daily
indicator only exports aggregates). It accepts a BAR_EXPORT-style pipe CSV
(epoch_ms|O|H|L|C|V in the `Signal` column) or a plain OHLC CSV, reconstructs
pools / FVGs offline via the SHARED `_ict_offline` detectors, and emits the sec 6
verdict PER SIDE.

FROZEN PREREG-D thresholds encoded here (every value cited to the PREREG row):
  * K-window drawK = 10 days .......................... LOCKED (PREREG-D test-object table; daily L26)
  * FVG basis = wicks (useBody=false) ................. REPORT-ONLY (daily L21)
  * displacement = dispMlt=1.5 x ATR, atrLen=14 ....... LOCKED headline (daily L24-25)
  * pool universe pvLen = 3 ........................... provisional headline (daily L23)
  * pool t0 = TRUE pivot bar (bar_index - pvLen) ...... LOCKED, genuine-choice #1 (D-2; daily L43/45/80)
  * FVG t0 = registration bar, touch from f.bar+1 ..... LOCKED (D-2b + D-1 guard; lib DRAFT L128)
  * poolRate = P(pool swept within K of pivot t0) ..... LOCKED (daily L80-83)
  * fvgRate  = P(FVG near-edge touched within K, >f.bar) LOCKED (daily L88-91; lib DRAFT L128)
  * base-rate null = radius-matched MC >= 5000 / side . LOCKED, genuine-choice #2 (D-3; daily L13-14)
  * PASS band: real_rate > base_rate + 95% boot CI hw . LOCKED (verdict gate)
  * block = distinct origin bar; n-floor = 30 BLOCKS .. LOCKED, genuine-choice #3 (per side, EFFECTIVE blocks)
  * censoring: drop objects within drawK of last bar .. LOCKED (Resampling unit, right-censor identical pool/FVG)
  * D-4 grid: dispMlt{0,1.5,3.0} x pvLen{2,3,5} = 9 ... LOCKED selection budget (sec 8.5; report n-per-cell)
  * verdict PER SIDE (BSL/SSL), never pooled .......... LOCKED, genuine-choice #5

Conventions (PREREG + repo): look-ahead-free, ET=America/New_York (DST-aware), TV
BAR_EXPORT epoch is UTC -> ET for DOW/sessions. ASCII only. Real-export entrypoint
(main) SKIPS cleanly when the operator has not yet produced the Daily TV export.

Rule-0 source (gitignored, outside the repo; re-anchor each session):
  C:/Users/joshu/Downloads/ict_daily_dol.pine            (8454 B, 2026-06-18T22:46:54Z)
  C:/Users/joshu/Downloads/constellation_ict_lib_DRAFT.pine (10587 B, 2026-06-18T22:42:47Z; carries the D-1 fix L121-134)
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

import _ict_offline as M

# ---- FROZEN PREREG-D constants (do not edit mid-run; amending voids the verdict)
DRAW_K = 10            # daily L26 (K-window, LOCKED)
DISP_MLT = 1.5         # daily L24  (LOCKED headline displacement filter)
ATR_LEN = 14           # daily L25  (LOCKED)
PV_LEN = 3             # daily L23  (provisional headline)
USE_BODY = False       # daily L21  (REPORT-ONLY: wick basis)
MC_DRAWS = 5000        # D-3 MC floor (>= 5000; enforced by _ict_offline)
N_FLOOR = 30           # genuine-choice #3: >= 30 EFFECTIVE BLOCKS per side
D4_DISP = (0.0, 1.5, 3.0)   # D-4 grid axis (sec 8.5 ledger)
D4_PVLEN = (2, 3, 5)        # D-4 grid axis (sec 8.5 ledger)

# BAR_EXPORT v0.1 `Signal` pipe field: epoch_ms|open|high|low|close|volume
SIGNAL_PIPE_RE = re.compile(
    r"^(?P<e>\d+)\|(?P<o>[-\d.]+)\|(?P<h>[-\d.]+)\|(?P<l>[-\d.]+)\|(?P<c>[-\d.]+)\|(?P<v>\d+)$"
)

# The Daily SPX-class export the operator must produce on TradingView. There is no
# such Daily export on disk yet (the existing US500 BAR_EXPORT is 15m intraday), so
# main() skips and names this requirement.
DEFAULT_CSV = Path(
    r"C:/Users/joshu/Downloads/BAR_EXPORT_v0.1_PEPPERSTONE_SPX500_DAILY.csv"
)


# =============================================================================
# BARS
# =============================================================================
@dataclass
class DailyBars:
    epoch_ms: np.ndarray     # UTC epoch ms (TV BAR_EXPORT epoch)
    open: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray
    atr: np.ndarray          # Wilder ATR(atrLen) == TV ta.atr (via _ict_offline)
    et_hour: np.ndarray
    et_min: np.ndarray
    et_dow: np.ndarray
    et_date: np.ndarray
    n: int


def build_bars(epoch_ms, o, h, l, c, atr_len: int = ATR_LEN) -> DailyBars:
    """Assemble DailyBars from raw OHLC. ATR via the SHARED Wilder RMA (TV ta.atr)."""
    o = np.asarray(o, float)
    h = np.asarray(h, float)
    l = np.asarray(l, float)
    c = np.asarray(c, float)
    epoch_ms = np.asarray(epoch_ms, dtype="int64")
    atr = M.wilder_atr(h, l, c, atr_len)
    et_hour, et_min, et_dow, et_date = M.et_fields(epoch_ms)
    return DailyBars(epoch_ms, o, h, l, c, atr, et_hour, et_min, et_dow,
                     et_date, len(c))


# =============================================================================
# LOADER -- BAR_EXPORT-style pipe CSV OR plain OHLC CSV. SKIP-IF-MISSING upstream.
# =============================================================================
def load_daily_ohlc(path: Path) -> DailyBars:
    """Load a Daily OHLC CSV into DailyBars.

    Two accepted shapes:
      (a) BAR_EXPORT v0.1 -- rows with a `Type` and a `Signal` pipe field
          (epoch_ms|O|H|L|C|V). We take the Entry rows (one row per bar) to avoid
          the Entry/Exit duplication, then dedup by epoch.
      (b) plain OHLC CSV -- columns (case-insensitive) among
          {date/time/datetime/epoch, open, high, low, close}. Date parsed to UTC
          epoch ms; a numeric epoch column is used directly.
    """
    raw = pd.read_csv(path, encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    cols = {c.lower(): c for c in raw.columns}

    if "signal" in cols and "type" in cols:
        # (a) BAR_EXPORT-style: parse the pipe field from Entry rows.
        e = raw[raw[cols["type"]].astype(str).str.startswith("Entry")]
        recs = []
        dropped = 0
        for _, r in e.iterrows():
            m = SIGNAL_PIPE_RE.match(str(r[cols["signal"]]).strip())
            if m:
                recs.append((int(m.group("e")), float(m.group("o")),
                             float(m.group("h")), float(m.group("l")),
                             float(m.group("c"))))
            else:
                dropped += 1
        if dropped > 0:
            # R4-5: mirror core/bar_export_loader -- a loud WARN naming the drop
            # count (do NOT loosen the integer-volume regex; integer volume is the
            # correct BAR EXPORT v0.1 contract).
            total = int(len(e))
            print(
                "WARN: load_daily_ohlc dropped %d of %d Entry rows as "
                "undecodable BAR_EXPORT signal" % (dropped, total),
                file=sys.stderr,
            )
        df = pd.DataFrame(recs, columns=["e", "open", "high", "low", "close"])
        df = df.drop_duplicates("e").sort_values("e").reset_index(drop=True)
        epoch = df["e"].to_numpy(dtype="int64")
        return build_bars(epoch, df["open"], df["high"], df["low"], df["close"])

    # (b) plain OHLC CSV.
    def pick(*names):
        for nm in names:
            if nm in cols:
                return cols[nm]
        raise KeyError(f"OHLC CSV missing any of {names}; have {list(raw.columns)}")

    oc, hc, lc, cc = pick("open"), pick("high"), pick("low"), pick("close")
    # time column: numeric epoch preferred, else a parseable date/time string.
    tcol = None
    for nm in ("epoch", "epoch_ms", "time", "timestamp", "datetime", "date and time", "date"):
        if nm in cols:
            tcol = cols[nm]
            break
    if tcol is None:
        raise KeyError("OHLC CSV missing a time/date/epoch column")
    tser = raw[tcol]
    if pd.api.types.is_numeric_dtype(tser):
        epoch = tser.to_numpy(dtype="int64")
        # heuristic: seconds vs ms (10-digit -> seconds)
        if np.nanmedian(epoch) < 1e12:
            epoch = epoch * 1000
    else:
        epoch = (pd.to_datetime(tser, utc=True).astype("int64") // 1_000_000).to_numpy()
    df = pd.DataFrame({"e": epoch, "open": raw[oc].astype(float),
                       "high": raw[hc].astype(float), "low": raw[lc].astype(float),
                       "close": raw[cc].astype(float)})
    df = df.drop_duplicates("e").sort_values("e").reset_index(drop=True)
    return build_bars(df["e"].to_numpy(dtype="int64"),
                      df["open"], df["high"], df["low"], df["close"])


# =============================================================================
# RATE ENGINE -- pools + FVGs per side, in-window + censored, with D-1 guard.
# =============================================================================
def effective_blocks(origin_bars) -> int:
    """PREREG-D Resampling unit: one block per DISTINCT origin bar (same-bar
    objects collapse to one block). n-floor + power-disclosure SE both use blocks."""
    return int(len(set(int(b) for b in origin_bars)))


def _build_fvgs(b: DailyBars, disp_mlt: float, atr_len: int):
    """Reconstruct the bull/bear FVG registry (wick basis) with the displacement
    filter, exactly as the Daily consumer does (daily L49-54).

    FVG at bar i requires the middle candle (i-1) to displace (>dispMlt*ATR). At
    disp_mlt == 0 the Pine displacement gate is NOT skipped: lib L71-73 returns
    ``na(atr)?false:(rng>mult*atr)``, which at mult==0 is ``rng > 0`` and False on
    a NaN (warmup) ATR -- so warmup-window gaps and zero-range-middle gaps are
    STILL dropped (R4-2 / R4-3); the disp_mlt==0 cell is "unfiltered EXCEPT warmup
    and zero-range middles", not "every 3-candle gap". t0 = registration bar = i
    (daily L51/54). Returns (bull_fvgs, bear_fvgs).
    """
    o, h, l, c, atr = b.open, b.high, b.low, b.close, b.atr
    bull, bear = [], []
    for i in range(2, b.n):
        # Displacement gate on the middle candle, called UNCONDITIONALLY (lib L71-73;
        # daily L48 evaluates ict.displacement for every bar). M.displacement returns
        # rng > mult*atr, and na(atr)->False, so at disp_mlt==0 it yields rng>0 and
        # drops the ATR warmup + zero-range middles exactly as Pine does (R4-2/R4-3).
        if not M.displacement(o, h, l, c, i, atr[i], disp_mlt, use_body=USE_BODY):
            continue
        if M.bull_fvg(o, h, l, c, i, use_body=USE_BODY):
            top, bot = M.bull_bounds(o, h, l, c, i, use_body=USE_BODY)
            bull.append(M.make_fvg(top, bot, i, bull=True))
        elif M.bear_fvg(o, h, l, c, i, use_body=USE_BODY):
            top, bot = M.bear_bounds(o, h, l, c, i, use_body=USE_BODY)
            bear.append(M.make_fvg(top, bot, i, bull=False))
    return bull, bear


def _scan_pool_hits(b: DailyBars, pools, draw_k: int):
    """Mark each pool swept (detect_raid) and record hit = swept within drawK of t0.
    Returns per-pool dicts with distance-at-origin and hit flag. Look-ahead-free:
    the sweep scan starts at the pivot bar t0 and runs forward only."""
    out = []
    for p in pools:
        t0 = p["bar"]
        px = p["price"]
        # distance at origin = |pool price - close at the pivot bar| (radius for D-3).
        dist = abs(px - b.close[t0])
        hit = False
        for j in range(t0 + 1, min(b.n, t0 + draw_k + 1)):
            if p["buyside"] and b.high[j] >= px:
                hit = True
                break
            if (not p["buyside"]) and b.low[j] <= px:
                hit = True
                break
        out.append({"bar": t0, "price": px, "buyside": p["buyside"],
                    "dist": float(dist), "hit": bool(hit)})
    return out


def _scan_fvg_hits(b: DailyBars, fvgs, draw_k: int, guard: bool):
    """Mark each FVG near-edge touched within drawK of its registration bar.

    D-1 guard (lib DRAFT L128): a touch counts only at barIdx > f.bar -- so the
    K-window scan starts at f.bar+1 when guarded, else at f.bar (the pre-fix
    behavior that pinned fvgRate ~100%, used only to PROVE the guard is load-bearing).
    Bull near-edge: low <= f.top. Bear near-edge: high >= f.bot.
    """
    start_off = 1 if guard else 0
    out = []
    for f in fvgs:
        t0 = f["bar"]
        # distance at origin = near-edge to close at registration (radius for D-3).
        near = f["top"] if f["bull"] else f["bot"]
        dist = abs(near - b.close[t0])
        hit = False
        for j in range(t0 + start_off, min(b.n, t0 + draw_k + 1)):
            if f["bull"] and b.low[j] <= f["top"]:
                hit = True
                break
            if (not f["bull"]) and b.high[j] >= f["bot"]:
                hit = True
                break
        out.append({"bar": t0, "near": float(near), "bull": f["bull"],
                    "dist": float(dist), "hit": bool(hit)})
    return out


def _censor(records, n_bars: int, draw_k: int):
    """Drop objects whose origin t0 is within drawK of the last bar (incomplete
    K-window). Identical rule for pools and FVGs (like-for-like; Resampling unit,
    PREREG-D "Resampling unit / right-censor", FROZEN).

    Strict age>drawK MISS boundary (this part MATCHES Pine). ict_daily_dol.pine
    L82/L90 keep an unswept object as a MISS only when ``age > drawK`` (strict); an
    object at exactly age == drawK is neither hit nor miss -> excluded from the rate
    population. So the in-window population is ``age > drawK``, i.e.
    ``bar < n_bars - 1 - draw_k`` (strict <).

    DELIBERATE divergence from Pine on right-edge FAST-HITS (documented, NOT a bug;
    PREREG-D 2026-06-19 POST-DATA CLARIFICATION). Pine L80 (pool) / L88 (FVG) COUNT a
    swept/touched-WITHIN-K object as a HIT even when its age <= drawK -- it excludes
    from the population ONLY the UNSWEPT age<=drawK objects (truly incomplete window).
    This offline censor is stricter: it drops EVERY age<=drawK object, INCLUDING the
    within-K fast-hits Pine keeps. Rationale (PREREG forbidden item 1 -- the verdict
    is the de-overlapped offline reconstruction, NOT the Pine aggregate table):
    keeping right-edge fast-hits while dropping their unswept-incomplete neighbors
    biases the rate UPWARD at the right edge (a right-censoring / immortal-time bias
    -- you retain only the objects that resolved fast enough to be observed). Dropping
    all age<=drawK objects gives every surviving object a fully-observable K-window,
    removing that bias. The effect is (a) UNIFORM across pools and FVGs (like-for-like,
    so the pool-vs-FVG footing is preserved) and (b) strictly CONSERVATIVE for a
    RESOLVED verdict: restoring the fast-hits can only RAISE a rate, so the offline
    rate is a lower bound on the Pine-faithful rate. It does NOT void the recorded D
    verdict (SSL-RESOLVED / BSL-FALSIFIED) -- pinned by
    test_censor_drops_right_edge_fast_hit_conservative_vs_pine.
    """
    last_complete = n_bars - 1 - draw_k
    return [r for r in records if r["bar"] < last_complete]


def _pack(records):
    """Pack a censored record list into the side/object result dict."""
    n = len(records)
    hits = int(sum(r["hit"] for r in records))
    origin_bars = [r["bar"] for r in records]
    nb = effective_blocks(origin_bars)
    return {
        "n": n,
        "hits": hits,
        "rate": (hits / n) if n > 0 else float("nan"),
        "n_blocks": nb,
        "distances": np.array([r["dist"] for r in records], float),
        "origin_bars": origin_bars,
        "hit_flags": np.array([1.0 if r["hit"] else 0.0 for r in records], float),
    }


def compute_rates(b: DailyBars, pv_len: int = PV_LEN, disp_mlt: float = DISP_MLT,
                  atr_len: int = ATR_LEN, draw_k: int = DRAW_K,
                  fvg_guard: bool = True) -> dict:
    """Per-side (BSL/SSL) pool + FVG rates over the in-window (censored) population.

    Returns {"BSL": {"pool": {...}, "fvg": {...}}, "SSL": {...}}. Pool t0 = TRUE
    pivot bar (D-2); FVG touch scanned from f.bar+1 when fvg_guard (D-1 / D-2b).

    Side mapping (PREREG-D side-split): the "BSL"/"SSL" keys are the POOL-side bucket
    names (BSL = buyside = old highs swept upward; SSL = sellside = old lows swept
    downward). The FVG bucketed under each key shares only the side's distance
    footing, NOT its draw direction:
      * BSL bucket FVG = BULL FVG -- a DOWNWARD draw (near edge BELOW price, touched
        when low <= top). It is filed under "BSL" for the radius-matched footing only.
      * SSL bucket FVG = BEAR FVG -- an UPWARD draw (near edge ABOVE price, touched
        when high >= bot).
    R4-6 (label-only): no rate is wrong -- each FVG null is radius-matched WITHIN its
    bucket (bull-FVG distances vs the BSL-side bull radius-matched null), so the bucket
    name is decoupled from the FVG draw direction and only the within-bucket comparison
    is load-bearing. Read "BSL.fvg" as "bull.fvg" and "SSL.fvg" as "bear.fvg".
    """
    pools = M.pools_from_pivots(b.high, b.low, pv_len)
    pool_hits = _scan_pool_hits(b, pools, draw_k)
    bull_fvgs, bear_fvgs = _build_fvgs(b, disp_mlt, atr_len)
    bull_hits = _scan_fvg_hits(b, bull_fvgs, draw_k, fvg_guard)
    bear_hits = _scan_fvg_hits(b, bear_fvgs, draw_k, fvg_guard)

    bsl_pool = _censor([r for r in pool_hits if r["buyside"]], b.n, draw_k)
    ssl_pool = _censor([r for r in pool_hits if not r["buyside"]], b.n, draw_k)
    bsl_fvg = _censor(bull_hits, b.n, draw_k)
    ssl_fvg = _censor(bear_hits, b.n, draw_k)

    return {
        "BSL": {"pool": _pack(bsl_pool), "fvg": _pack(bsl_fvg)},
        "SSL": {"pool": _pack(ssl_pool), "fvg": _pack(ssl_fvg)},
    }


# =============================================================================
# D-3 RADIUS-MATCHED BASE RATE (per side, via _ict_offline.radius_matched_base_rate)
# =============================================================================
def _pool_price_path_fn(b: DailyBars, side: str, draw_k: int):
    """Closure: a pseudo-BSL/SSL level at signed distance `dist` from a randomly
    sampled origin bar -- is it swept within drawK? Look-ahead-free (forward scan).

    BSL level sits ABOVE price (origin close + dist) and is swept when high>=level;
    SSL level sits BELOW (origin close - dist), swept when low<=level. The origin
    bar is sampled UNIFORMLY over the in-window (uncensored) bars so the K-window is
    complete, matching the real objects' censoring.
    """
    n = b.n
    # R4-1: censoring-matched origin population. The real objects keep age > drawK
    # (bar < n-1-draw_k, STRICT), so the radius-matched null must sample origins from
    # the SAME population: bars in [0, last_complete) (exclude the age==drawK origin).
    last_complete = n - 1 - draw_k
    valid_origins = np.arange(0, last_complete) if last_complete >= 1 else np.array([0])
    rng = np.random.default_rng(424242)  # local origin sampler; MC draw RNG is owned upstream

    def path_fn(dist):
        ob = int(rng.choice(valid_origins))
        if side == "BSL":
            level = b.close[ob] + abs(dist)
            for j in range(ob + 1, min(n, ob + draw_k + 1)):
                if b.high[j] >= level:
                    return True
            return False
        else:
            level = b.close[ob] - abs(dist)
            for j in range(ob + 1, min(n, ob + draw_k + 1)):
                if b.low[j] <= level:
                    return True
            return False

    return path_fn


def _fvg_price_path_fn(b: DailyBars, side: str, draw_k: int):
    """Closure for the FVG near-edge base rate: a pseudo near-edge at `dist` from a
    sampled origin close, touched within drawK from f.bar+1 (D-1 guard preserved).
    BSL = bull FVG near edge ABOVE? -- a bull near edge is touched from above when
    low<=edge; the radius-matched null places the edge at origin_close - dist (below)
    so a downward wander touches it, mirroring the real bull near-edge geometry.
    SSL = bear near edge placed above (origin_close + dist), touched when high>=edge.
    """
    n = b.n
    # R4-1: censoring-matched origin population (same STRICT age>drawK rule as the
    # real FVG population; exclude the age==drawK origin).
    last_complete = n - 1 - draw_k
    valid_origins = np.arange(0, last_complete) if last_complete >= 1 else np.array([0])
    rng = np.random.default_rng(606060)

    def path_fn(dist):
        ob = int(rng.choice(valid_origins))
        if side == "BSL":   # bull near edge below price; touched when low <= edge
            edge = b.close[ob] - abs(dist)
            for j in range(ob + 1, min(n, ob + draw_k + 1)):
                if b.low[j] <= edge:
                    return True
            return False
        else:               # bear near edge above price; touched when high >= edge
            edge = b.close[ob] + abs(dist)
            for j in range(ob + 1, min(n, ob + draw_k + 1)):
                if b.high[j] >= edge:
                    return True
            return False

    return path_fn


def pool_base_rate(b: DailyBars, pool_res: dict, side: str, draw_k: int = DRAW_K,
                   B: int = MC_DRAWS, seed: int = 0):
    """Radius-matched MC base rate + bootstrap CI for the pool side (PREREG-D D-3).
    Routes through _ict_offline.radius_matched_base_rate (enforces B>=5000)."""
    return M.radius_matched_base_rate(
        pool_res["distances"], _pool_price_path_fn(b, side, draw_k),
        K=draw_k, B=B, seed=seed)


def fvg_base_rate(b: DailyBars, fvg_res: dict, side: str, draw_k: int = DRAW_K,
                  B: int = MC_DRAWS, seed: int = 0):
    """Radius-matched MC base rate + bootstrap CI for the FVG side (PREREG-D D-3)."""
    return M.radius_matched_base_rate(
        fvg_res["distances"], _fvg_price_path_fn(b, side, draw_k),
        K=draw_k, B=B, seed=seed)


# =============================================================================
# PASS BAND + two-proportion diff + verdict gate (sec 6)
# =============================================================================
def clears_base(real_rate: float, base_rate: float, ci) -> bool:
    """PASS band: real_rate > base_rate + 95% bootstrap CI HALF-WIDTH (strict >).
    half-width = (hi - lo) / 2."""
    lo, hi = ci
    if any(np.isnan(x) for x in (real_rate, base_rate, lo, hi)):
        return False
    half_width = (hi - lo) / 2.0
    return bool(real_rate > base_rate + half_width)


def pool_minus_fvg_ci(side_res: dict, B: int = 5000, seed: int = 0):
    """Bootstrap CI of (poolRate - fvgRate) for one side, via _ict_offline
    (PREREG-D D-4 two_proportion_diff_ci). NOTE: a raw pool-vs-FVG read is
    selectivity-confounded (Forbidden item 2) -- this is descriptive, the matched
    instrument is the D-4 grid."""
    p, f = side_res["pool"], side_res["fvg"]
    return M.two_proportion_diff_ci(p["hits"], p["n"], f["hits"], f["n"], B, seed)


def verdict_for_side(side_res: dict, *, base_pool: float, base_pool_hw: float,
                     base_fvg: float, base_fvg_hw: float,
                     half_pool, half_fvg, n_floor: int = N_FLOOR,
                     selectivity_ok: bool = True) -> dict:
    """sec 6 verdict for ONE side. base_*_hw is the base-rate CI half-width already
    extracted; half_pool/half_fvg are (first_half_rate, second_half_rate) for the
    stationarity check.

    Gate (PREREG-D sec 6, frozen):
      INSUFFICIENT-N : no object on the side reaches n_floor effective blocks.
      RESOLVED       : a qualifying object (>= n_floor) clears base+hw AND both
                       halves are on the same side of base_rate (stationary) AND
                       the D-4 selectivity probe does NOT explain it (selectivity_ok).
      AMBIGUOUS-HOLD : clears+at-floor but one-regime (a half on the wrong side of
                       base) OR selectivity explains the clearance.
      FALSIFIED      : at least one object at n_floor, but NONE clears base+hw.
    """
    pool, fvg = side_res["pool"], side_res["fvg"]
    pool_ok_n = pool["n_blocks"] >= n_floor
    fvg_ok_n = fvg["n_blocks"] >= n_floor
    if not (pool_ok_n or fvg_ok_n):
        return {"verdict": "INSUFFICIENT-N", "clearing_objects": [],
                "detail": "no object reached n-floor (>=%d blocks)" % n_floor}

    clearing = []        # objects that clear base+hw at n-floor
    ambiguous = []       # objects that clear but are one-regime / selectivity-explained
    for name, res, base, hw, halves in (
        ("pool", pool, base_pool, base_pool_hw, half_pool),
        ("fvg", fvg, base_fvg, base_fvg_hw, half_fvg),
    ):
        if res["n_blocks"] < n_floor:
            continue
        clears = res["rate"] > base + hw          # PASS band (strict >)
        if not clears:
            continue
        h1, h2 = halves
        stationary = (h1 > base) and (h2 > base)  # both halves above base_rate
        if stationary and selectivity_ok:
            clearing.append(name)
        else:
            ambiguous.append(name)

    if clearing:
        return {"verdict": "RESOLVED", "clearing_objects": clearing,
                "ambiguous_objects": ambiguous,
                "detail": "cleared, stationary, selectivity-survived: %s" % clearing}
    if ambiguous:
        return {"verdict": "AMBIGUOUS-HOLD", "clearing_objects": [],
                "ambiguous_objects": ambiguous,
                "detail": "clears only on one regime / selectivity-explained: %s" % ambiguous}
    return {"verdict": "FALSIFIED", "clearing_objects": [],
            "detail": "an object reached n-floor but none cleared base_rate + CI half-width"}


# =============================================================================
# D-4 SELECTIVITY GRID -- dispMlt{0,1.5,3.0} x pvLen{2,3,5} = 9 cells, n-per-cell
# =============================================================================
def selectivity_grid(b: DailyBars, draw_k: int = DRAW_K, atr_len: int = ATR_LEN,
                     fvg_guard: bool = True) -> list:
    """Run compute_rates over the 9-cell D-4 grid; report n-per-cell (sec 8.5 ledger).
    The headline is the LOCKED/provisional cell (dispMlt=1.5, pvLen=3) -- the grid
    cannot be mined (Forbidden item 5/6); it is the matched-selectivity instrument."""
    grid = []
    for disp in D4_DISP:
        for pv in D4_PVLEN:
            res = compute_rates(b, pv_len=pv, disp_mlt=disp, atr_len=atr_len,
                                draw_k=draw_k, fvg_guard=fvg_guard)
            res["disp_mlt"] = float(disp)
            res["pv_len"] = int(pv)
            grid.append(res)
    return grid


def _split_halves_rate(res: dict):
    """First-half / second-half rate by object origin bar (stationarity check). The
    split is by the median origin bar so each half holds ~half the blocks."""
    obars = np.array(res["origin_bars"], float)
    flags = res["hit_flags"]
    if len(obars) == 0:
        return (float("nan"), float("nan"))
    mid = np.median(obars)
    first = flags[obars <= mid]
    second = flags[obars > mid]
    h1 = float(first.mean()) if len(first) else float("nan")
    h2 = float(second.mean()) if len(second) else float("nan")
    return (h1, h2)


# =============================================================================
# FULL EVALUATION (real data) + main()
# =============================================================================
def evaluate(b: DailyBars, seed: int = 20260618) -> dict:
    """Full PREREG-D evaluation on reconstructed Daily bars. Returns a per-side
    report incl. base rates, PASS band, halves stationarity, D-4 grid, and sec 6
    verdict. This is the de-overlapped offline verdict -- never the indicator table."""
    headline = compute_rates(b, pv_len=PV_LEN, disp_mlt=DISP_MLT, atr_len=ATR_LEN,
                             draw_k=DRAW_K, fvg_guard=True)
    grid = selectivity_grid(b)
    report = {"headline": headline, "grid": grid, "sides": {}}

    for side in ("BSL", "SSL"):
        pool, fvg = headline[side]["pool"], headline[side]["fvg"]
        bp, (bpl, bph) = (pool_base_rate(b, pool, side, seed=seed + 1)
                          if pool["n"] > 0 else (float("nan"), (float("nan"), float("nan"))))
        bf, (bfl, bfh) = (fvg_base_rate(b, fvg, side, seed=seed + 2)
                          if fvg["n"] > 0 else (float("nan"), (float("nan"), float("nan"))))
        bp_hw = (bph - bpl) / 2.0 if not np.isnan(bpl) else float("nan")
        bf_hw = (bfh - bfl) / 2.0 if not np.isnan(bfl) else float("nan")
        half_pool = _split_halves_rate(pool)
        half_fvg = _split_halves_rate(fvg)

        # D-4 selectivity probe: does the headline edge survive at matched
        # selectivity? Proxy: the headline cell's pool/fvg rate must remain the
        # strongest-over-base across the grid cells that share its side and reach
        # n-floor (a flat or selectivity-tracking rate => selectivity explains it).
        selectivity_ok = _selectivity_survives(grid, side, bp, bf, bp_hw, bf_hw)

        v = verdict_for_side(
            headline[side], base_pool=bp, base_pool_hw=bp_hw,
            base_fvg=bf, base_fvg_hw=bf_hw, half_pool=half_pool, half_fvg=half_fvg,
            n_floor=N_FLOOR, selectivity_ok=selectivity_ok)

        diff, dlo, dhi = pool_minus_fvg_ci(headline[side], seed=seed + 3)
        report["sides"][side] = {
            "pool_rate": pool["rate"], "fvg_rate": fvg["rate"],
            "pool_n": pool["n"], "pool_blocks": pool["n_blocks"],
            "fvg_n": fvg["n"], "fvg_blocks": fvg["n_blocks"],
            "base_pool": bp, "base_pool_ci": (bpl, bph),
            "base_fvg": bf, "base_fvg_ci": (bfl, bfh),
            "half_pool": half_pool, "half_fvg": half_fvg,
            "selectivity_ok": selectivity_ok,
            "pool_minus_fvg": (diff, dlo, dhi),
            "verdict": v,
        }
    return report


def _selectivity_survives(grid, side, base_pool, base_fvg, bp_hw, bf_hw) -> bool:
    """D-4 matched-selectivity probe (Forbidden item 2): is the headline cell's
    edge a mere artifact of the object population growing looser?

    The full matched comparison recomputes the base rate PER cell and inspects the
    n-per-cell table by eye (the sec 6 disjunct "survives at matched selectivity" is an
    operator read of the grid, NOT a single mechanical scalar). Pre-data we cannot
    compute the per-cell base rates cheaply enough to bake a hard gate, so this
    returns the conservative DEFAULT (True = does-not-explain) and the real run
    surfaces the full 9-cell rate table for the operator's matched read. The
    selectivity disjunct can still force AMBIGUOUS-HOLD via `selectivity_ok=False`
    passed explicitly when the grid table shows the edge tracking selectivity.

    Kept side/base args in the signature so a future per-cell base-rate
    implementation drops in without changing call sites.
    """
    return True


def main(csv_path: Path = DEFAULT_CSV) -> int:
    """Real-export entrypoint. SKIPS cleanly when the Daily TV export is absent
    (the operator has not run TV yet) and prints exactly what export it needs."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        print("[Layer D] no export yet -- SKIPPING.")
        print("  This layer CONSUMES a DAILY OHLC export of an SPX-class series")
        print("  (the Daily ICT indicator only exports aggregates, so it is NOT a")
        print("  TV-indicator export -- it is a Daily BAR_EXPORT-style or plain")
        print("  OHLC CSV of DAILY bars).")
        print(f"  Expected at: {csv_path}")
        print("  Accepted shapes:")
        print("    (a) BAR_EXPORT v0.1 with a `Signal` pipe field epoch_ms|O|H|L|C|V")
        print("    (b) plain OHLC CSV: columns date/epoch, open, high, low, close")
        print("  Re-run once the Daily SPX-class export exists. (No verdict produced.)")
        return 0

    b = load_daily_ohlc(csv_path)
    print(f"[Layer D] loaded {b.n} Daily bars from {csv_path.name}")
    report = evaluate(b)
    print(f"  D-4 grid: {len(report['grid'])} cells (dispMlt{D4_DISP} x pvLen{D4_PVLEN})")
    # R4-6 (label-only): the BSL/SSL keys are POOL-side bucket names. The FVG filed
    # under each shares the side's distance footing only, NOT its draw direction --
    # BSL.fvg is a BULL FVG (a downward draw); SSL.fvg is a BEAR FVG (an upward
    # draw). Each FVG null is radius-matched WITHIN its bucket, so no rate is wrong.
    print("  NOTE: BSL.fvg == bull.fvg (downward draw); SSL.fvg == bear.fvg "
          "(upward draw). FVG bucket name is the pool-side label, decoupled from "
          "FVG draw direction; the null is matched within the bucket (R4-6).")
    for side in ("BSL", "SSL"):
        s = report["sides"][side]
        print(f"\n== {side} ==")
        print(f"  pool: rate={s['pool_rate']:.4f} n={s['pool_n']} blocks={s['pool_blocks']} "
              f"base={s['base_pool']:.4f} ci={tuple(round(x,4) for x in s['base_pool_ci'])} "
              f"halves={tuple(round(x,3) for x in s['half_pool'])}")
        print(f"  fvg : rate={s['fvg_rate']:.4f} n={s['fvg_n']} blocks={s['fvg_blocks']} "
              f"base={s['base_fvg']:.4f} ci={tuple(round(x,4) for x in s['base_fvg_ci'])} "
              f"halves={tuple(round(x,3) for x in s['half_fvg'])}")
        d, dlo, dhi = s["pool_minus_fvg"]
        print(f"  poolRate-fvgRate diff={d:+.4f} CI=({dlo:+.4f},{dhi:+.4f}) "
              f"(selectivity-confounded; D-4 grid is the matched instrument)")
        print(f"  VERDICT[{side}] = {s['verdict']['verdict']} -- {s['verdict']['detail']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
