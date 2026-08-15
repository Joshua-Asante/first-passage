"""Layer 1M (Execution) harness for Q-ICT-CASCADE-1.

Verdict instrument for the 1M execution claim: **post-cost E[R] per closed trade**,
R-denominated, off TV's **List-of-Trades** export. Encodes the FROZEN thresholds and
the binary verdict gate from:

    lab/analysis/ict_cascade_2026-06-18/PREREG-1M.md  (Q-ICT-1M, Layer 4)
    (parent: TEST_PLAN.md  -- Layer 1M = section 4 H-1M, section 6 1M row, section 7.B 1M)

This module DOES NOT re-port any detector or re-implement any statistic that the shared
offline module already provides; it imports them from `_ict_offline`:
    moving_block_bootstrap_ci, autocorr_block_len, drop_top_k, max_stat_label_permutation,
    et_fields.
DSR (selection-adjusted significance) is reused from the proven sibling
    lab/archive/usdcad_reverse_2026-06-14/dsr.py  (Bailey & Lopez de Prado).

FROZEN config (PREREG-1M "Test object" table; DRAFT line refs are to
`C:\\Users\\joshu\\Downloads\\ict_1m_execution_DRAFT.pine`, 22182 B,
LastWriteUTC 2026-06-18T18:42:43Z -- CITATION-CHAIN mode; re-anchor on resume):

  - commPct  = 0.00002         (cost-law commission fraction; PREREG-1M L46 / DRAFT L87)
  - slipTk   = 1               (cost-law slippage ticks;      PREREG-1M L47 / DRAFT L89)
  - cost_R per trade = (2*commPct*entryEst + 2*slipTk*mintick) / stopDist
                               (PREREG-1M L51,L55 / DRAFT L228 long, L260 short) -- GEOMETRY,
                               computed BEFORE any outcome is read.
  - tradeability floor: drop trades with stop_dist < max(1pt, cost)   (PREREG-1M L52, ledger F8)
                        -> REPORT the dropped count.
  - HURDLE = 4 * median(cost_R) on the post-floor (tradeable) population (PREREG-1M L55).
            (minRmult = 4.0; PREREG-1M L48. Distinct from the in-code arm-time
             per-trade geometry filter -- both must hold -- PREREG-1M L57.)
  - n-floor = 100 closed trades after the B4 starvation fix -> below it INSUFFICIENT-N / HALT
              (PREREG-1M L69,L79; verdict is unfalsifiable on this data).
  - resample unit = ENTRY EVENT (one block per arming raid / FVG entry), NOT iid by trade-row
              (PREREG-1M L62-63; same ICT-geometry family as the FALSIFIED D2 -> iid understates SE).
  - CIs + DOW/arm-time-killzone permutation resample by entry-event block.
  - gate-ablation = exactly 8 labeled List-of-Trades exports (bias x PD x killzone, all on/off)
              x 2 useBody variants (PREREG-1M L120; assert 8). A retained gate earns its place
              iff its marginal E[R] CI EXCLUDES 0 (not merely prunes n).
  - dolMode: range-extreme is GATE-BEARING (the R-claim is tested against it); nearest-pool is
              REPORT-ONLY -- never in the lock decision, consumes NO best-of-K/perm budget
              (PREREG-1M L42, L89; Forbidden #5).
  - headline currency = R. Any $/DD is REPORT-ONLY off the STATIC-$200K recompute
              (strip strategy.equity compounding; per-trade %*static-$200K) -- PREREG-1M L59,L32.
  - drop-top-k concentration check is MANDATORY (PREREG-1M L63). Default k scales to the
              block count to hold the D2 sibling's ~6% removal fraction:
              k = ceil(0.06 * n_blocks)  (PREREG-1M genuine-choice #5, L132).
  - permutation B >= 5000, max-stat over slices (PREREG-1M genuine-choice #6, L133).

Verdict gate (binary; PREREG-1M section "Verdict gate", L75-79), evaluated SEPARATELY per
useBody variant on the gate-bearing config (dolMode=range-extreme):
  RESOLVED (-> forward, not deploy):
    E[R] block-CI lower bound > 4*median(cost_R)  AT n >= 100
    AND every RETAINED gate (bias/PD/killzone) shows positive marginal E[R] with CI excluding 0
    AND no single DOW slice AND no single arm-time killzone slice carries the edge beyond the
        entry-event permutation null
    AND drop-top-k concentration holds (edge survives removing the top-k entry-event blocks).
  FALSIFIED:
    E[R] CI subset of (-inf, hurdle] (CI lower <= hurdle)
    OR both gates add nothing (no retained gate's marginal-E[R] CI excludes 0)
    OR the edge lives in one slice (one DOW or one arm-time killzone slice beyond the perm null)
    OR drop-top-k removes the edge.
  INSUFFICIENT-N / AMBIGUOUS-HOLD:
    n < 100 after the B4 starvation fix -> claim unfalsifiable on this data; HALT, re-spec the
    DOL target, re-test on an independent multi-regime window.

Conventions (PREREG + repo): look-ahead-free, PnL net of cost / R-denominated, ASCII only,
ET = America/New_York (DST-aware), TV BAR_EXPORT epoch is UTC -> convert UTC->ET for sessions/DOW.

main() SKIPS gracefully when the real List-of-Trades export(s) are absent (operator has not run
TV yet) and prints exactly which exports it needs.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

# Shared offline module (detectors + statistics) -- single source of truth.
import _ict_offline as M

# -----------------------------------------------------------------------------
# FROZEN constants (PREREG-1M -- do not edit without voiding the validation).
# -----------------------------------------------------------------------------
COMM_PCT = 0.00002        # PREREG-1M L46 / DRAFT L87  (= commission_value 0.002%/side)
SLIP_TK = 1               # PREREG-1M L47 / DRAFT L89  (= slippage 1 tick)
MIN_RMULT = 4.0           # PREREG-1M L48,L55  (verdict-gate hurdle multiple)
N_FLOOR = 100             # PREREG-1M L69,L79  (power gate; below -> INSUFFICIENT-N / HALT)
STATIC_EQUITY = 200_000.0 # PREREG-1M L59,L32  (static-$200K recompute base)
RISK_PCT = 0.005          # DRAFT L83 riskPct=0.5% (R-invariant; used only for static-$ recompute)
PERM_B = 5000             # PREREG-1M genuine-choice #6, L133 (permutation B >= 5000)
BOOT_B = 5000             # block-bootstrap resamples for the headline E[R] CI
DROP_TOP_K_FRAC = 0.06    # PREREG-1M genuine-choice #5, L132 (hold the D2 sibling's ~6% fraction)
ALPHA = 0.05              # two-sided -> 95% CI

# The exactly-8 gate-ablation labels (bias x PD x killzone, all on/off combos).
# A verdict claiming gate marginal-E[R] from fewer than 8 distinct exports is VOID
# (PREREG-1M audit-hook L120). Order is canonical (bias, pd, killzone) MSB->LSB.
GATES = ("bias", "pd", "killzone")
ABLATION_LABELS = tuple(
    f"bias{int(b)}_pd{int(p)}_kz{int(k)}"
    for b in (0, 1) for p in (0, 1) for k in (0, 1)
)  # 8 labels

# Arm-time killzone windows (ET; FROZEN, NOT swept -- PREREG-killzone / DRAFT L67-75).
#   London Open 02:00-05:00 ON ; NY AM 07:00-10:00 ON ; NY PM 13:30-16:00 OFF.
# Slice membership for the one-slice permutation is by ARM-TIME zone (entry may spill
# <= raidWin bars past the window -- PREREG-killzone). "out" = none of the zones.
KILLZONES = {
    "london": (2 * 60, 5 * 60),       # [02:00, 05:00) ET in minutes-of-day
    "nyam": (7 * 60, 10 * 60),        # [07:00, 10:00) ET
    "nypm": (13 * 60 + 30, 16 * 60),  # [13:30, 16:00) ET  (OFF zone -- still a slice)
}


def killzone_of(et_hour, et_min):
    """Arm-time killzone label for an ET wall-clock (PREREG-killzone). 'out' if none."""
    mod = int(et_hour) * 60 + int(et_min)
    for name, (lo, hi) in KILLZONES.items():
        if lo <= mod < hi:
            return name
    return "out"


# =============================================================================
# SECTION 1 -- TV List-of-Trades schema adapter + Entry/Exit pairing -> per-trade
# =============================================================================
# TV's "List of Trades" export emits TWO rows per trade (an Entry row and an Exit
# row) sharing a "Trade #". Column names vary slightly across TV versions; the
# adapter normalizes a handful of aliases. The pairing is by trade number; R is
# derived from PnL/risk if a risk column is present, else from (exit-entry)/stop_dist
# with the side sign (PREREG-1M "COMPUTES").

# Canonical -> set of accepted header aliases (lowercased, stripped).
_ALIASES = {
    "trade_num": {"trade #", "trade#", "trade number", "trade no", "trade", "tradeid", "id"},
    "type": {"type", "side", "signal"},                       # Entry/Exit + long/short
    "datetime": {"date/time", "datetime", "date time", "time", "date"},
    "price": {"price", "price usd", "price ($)", "fill price", "entry/exit price"},
    "qty": {"quantity", "qty", "contracts", "size", "amount"},
    "pnl": {"profit", "p&l", "pnl", "net p&l", "profit usd", "profit ($)",
            "net profit", "realized p&l"},
    "runup": {"run-up", "runup", "run up", "mfe", "max favorable excursion",
              "run-up usd", "run-up ($)"},
    "drawdown": {"drawdown", "draw down", "mae", "max adverse excursion",
                 "drawdown usd", "drawdown ($)"},
    "risk": {"risk", "risk usd", "risk ($)", "risk_r", "1r", "one_r", "r_value",
             "risk_per_trade"},
    "stop_dist": {"stop_dist", "stop distance", "stopdist", "stop", "sl_dist"},
    "epoch_ms": {"epoch_ms", "epoch", "time_ms", "ts_ms", "timestamp_ms"},
}


def _norm_header(h):
    return (h or "").strip().lower()


def _build_colmap(headers):
    """Map canonical field -> actual header string, using the alias table."""
    norm = {_norm_header(h): h for h in headers}
    colmap = {}
    for canon, aliases in _ALIASES.items():
        for a in aliases:
            if a in norm:
                colmap[canon] = norm[a]
                break
    return colmap


def _to_float(s):
    """Parse a possibly-formatted numeric cell. '' / None / 'n/a' -> nan."""
    if s is None:
        return float("nan")
    t = str(s).strip()
    if t == "" or t.lower() in ("n/a", "na", "nan", "-", "none"):
        return float("nan")
    neg = False
    # accounting-style parentheses for negatives, and a leading currency symbol.
    if t.startswith("(") and t.endswith(")"):
        neg = True
        t = t[1:-1]
    t = t.replace("$", "").replace(",", "").replace("%", "").replace("+", "").strip()
    if t == "":
        return float("nan")
    try:
        v = float(t)
    except ValueError:
        return float("nan")
    return -v if neg else v


def _datetime_to_epoch_ms(s):
    """Parse a TV 'Date/Time' cell -> UTC epoch ms (R6-1). nan if unparseable.

    A vanilla TV List-of-Trades export carries a human 'Date/Time' cell (e.g.
    '2026-06-18 09:00') and NO epoch_ms column. The export epoch convention is UTC
    (repo BAR_EXPORT rule), so the string is read as a naive wall-clock interpreted
    as UTC. Without this, entry_epoch_ms stays nan -> the ET/killzone block is
    skipped and assign_blocks falls to iid -- double-biasing toward RESOLVED.
    """
    if s is None:
        return float("nan")
    t = str(s).strip()
    if t == "" or t.lower() in ("n/a", "na", "nan", "-", "none"):
        return float("nan")
    try:
        ts = pd.to_datetime(t, utc=True, errors="coerce")
    except (ValueError, TypeError):
        return float("nan")
    if ts is None or (isinstance(ts, float) and math.isnan(ts)) or pd.isna(ts):
        return float("nan")
    return float(ts.value // 1_000_000)   # ns -> ms


def _row_kind(type_str):
    """Classify a TV 'Type' cell into ('entry'|'exit', side) where side in {+1,-1,0}."""
    t = (type_str or "").strip().lower()
    is_entry = "entry" in t
    is_exit = "exit" in t
    side = 0
    if "long" in t or "buy" in t:
        side = 1
    elif "short" in t or "sell" in t:
        side = -1
    kind = "entry" if is_entry else ("exit" if is_exit else "")
    return kind, side


@dataclass
class Trade:
    """One paired Entry/Exit trade (per-trade record after pairing)."""
    trade_num: int
    side: int                  # +1 long, -1 short
    entry_price: float
    exit_price: float
    pnl: float                 # raw TV $ PnL (may be compounded; report-only)
    qty: float
    risk: float                # $ risk (1R) if present, else nan
    stop_dist: float           # price distance to stop if present, else nan
    runup: float               # MFE ($)
    drawdown: float            # MAE ($)
    entry_epoch_ms: float      # UTC epoch ms of entry (for ET fields), nan if absent
    # filled downstream:
    et_hour: int = -1
    et_min: int = -1
    et_dow: int = -1           # Mon=0..Sun=6
    et_date: object = None     # datetime.date in ET (for the multi-regime span check, R6-3)
    killzone: str = "out"
    r_gross: float = float("nan")   # gross R (PnL/risk or (exit-entry)*side/stop_dist)
    cost_r: float = float("nan")    # geometry cost in R (PREREG-1M cost-law)
    r_net: float = float("nan")     # r_gross - cost_r
    block_id: int = -1              # entry-event block index
    tradeable: bool = True          # passes tradeability floor


def pair_trades(rows, colmap):
    """Pair Entry/Exit rows by trade number into Trade records (PREREG-1M R-pairing).

    rows    : list of dict (raw cells keyed by ACTUAL header).
    colmap  : canonical -> actual header (from _build_colmap).
    Returns (trades, parse_stats) where parse_stats counts unpaired / skipped rows.
    """
    def get(row, canon, default=None):
        col = colmap.get(canon)
        return row.get(col, default) if col is not None else default

    by_num = {}
    n_rows = 0
    n_unclassified = 0
    for row in rows:
        n_rows += 1
        kind, side = _row_kind(get(row, "type"))
        if kind == "":
            n_unclassified += 1
            continue
        key = get(row, "trade_num")
        try:
            tn = int(_to_float(key))
        except (ValueError, TypeError):
            tn = key  # keep raw key if non-numeric (still pairs by equality)
        slot = by_num.setdefault(tn, {})
        # R6-1: prefer an explicit epoch_ms column; else parse the human Date/Time
        # alias (declared but previously never consumed) as UTC epoch ms.
        epoch = _to_float(get(row, "epoch_ms"))
        if math.isnan(epoch):
            epoch = _datetime_to_epoch_ms(get(row, "datetime"))
        rec = {
            "side": side,
            "price": _to_float(get(row, "price")),
            "qty": _to_float(get(row, "qty")),
            "pnl": _to_float(get(row, "pnl")),
            "risk": _to_float(get(row, "risk")),
            "stop_dist": _to_float(get(row, "stop_dist")),
            "runup": _to_float(get(row, "runup")),
            "drawdown": _to_float(get(row, "drawdown")),
            "epoch_ms": epoch,
        }
        slot[kind] = rec

    trades = []
    n_unpaired = 0
    for tn, slot in by_num.items():
        if "entry" not in slot or "exit" not in slot:
            n_unpaired += 1
            continue
        e, x = slot["entry"], slot["exit"]
        side = e["side"] if e["side"] != 0 else (-x["side"] if x["side"] != 0 else 0)
        # PnL is reported on the EXIT row in TV; risk/stop on the entry if present.
        pnl = x["pnl"]
        if math.isnan(pnl):
            pnl = e["pnl"]
        risk = e["risk"] if not math.isnan(e["risk"]) else x["risk"]
        stop_dist = e["stop_dist"] if not math.isnan(e["stop_dist"]) else x["stop_dist"]
        try:
            tnum = int(tn)
        except (ValueError, TypeError):
            tnum = -1
        trades.append(Trade(
            trade_num=tnum, side=int(side),
            entry_price=e["price"], exit_price=x["price"],
            pnl=pnl, qty=e["qty"] if not math.isnan(e["qty"]) else x["qty"],
            risk=risk, stop_dist=stop_dist,
            runup=x["runup"] if not math.isnan(x["runup"]) else e["runup"],
            drawdown=x["drawdown"] if not math.isnan(x["drawdown"]) else e["drawdown"],
            entry_epoch_ms=e["epoch_ms"],
        ))
    trades.sort(key=lambda t: t.trade_num)
    stats = {"n_rows": n_rows, "n_unclassified": n_unclassified,
             "n_paired": len(trades), "n_unpaired": n_unpaired}
    return trades, stats


def load_list_of_trades(csv_path):
    """Read a TV List-of-Trades CSV -> (trades, parse_stats). Schema-adapted."""
    csv_path = Path(csv_path)
    with open(csv_path, "r", newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        rows_raw = list(reader)
    if not rows_raw:
        return [], {"n_rows": 0, "n_unclassified": 0, "n_paired": 0, "n_unpaired": 0}
    header = rows_raw[0]
    colmap = _build_colmap(header)
    dict_rows = [dict(zip(header, r)) for r in rows_raw[1:] if any(c.strip() for c in r)]
    return pair_trades(dict_rows, colmap)


# =============================================================================
# SECTION 2 -- cost_R, R-denomination, tradeability floor, hurdle
# =============================================================================
def cost_r(entry_price, stop_dist, mintick, comm_pct=COMM_PCT, slip_tk=SLIP_TK):
    """Per-trade geometry cost in R (PREREG-1M L51,L55 / DRAFT L228/L260).

    cost_R = (2*comm_pct*entry_price + 2*slip_tk*mintick) / stop_dist
    Round-trip: 2x commission (entry+exit), 2x slippage (entry+exit). GEOMETRY -- no
    outcome is read. nan stop_dist/entry -> nan; non-positive stop_dist -> inf (the
    tradeability floor drops it).
    """
    if stop_dist is None or (isinstance(stop_dist, float) and math.isnan(stop_dist)):
        return float("nan")
    if stop_dist <= 0:
        return float("inf")
    comm = 2.0 * comm_pct * float(entry_price)
    slip = 2.0 * slip_tk * float(mintick)
    return (comm + slip) / float(stop_dist)


def r_gross(trade):
    """Gross R per trade (PREREG-1M R-denominate).

    Prefer PnL/risk (TV's own 1R if a risk column is present). Else
    (exit-entry)*side / stop_dist. nan if neither basis is available.
    """
    if trade.risk is not None and not math.isnan(trade.risk) and trade.risk > 0 \
            and not math.isnan(trade.pnl):
        return trade.pnl / trade.risk
    if not math.isnan(trade.stop_dist) and trade.stop_dist > 0 \
            and not math.isnan(trade.entry_price) and not math.isnan(trade.exit_price) \
            and trade.side != 0:
        return (trade.exit_price - trade.entry_price) * trade.side / trade.stop_dist
    return float("nan")


def apply_tradeability_floor(trades, mintick):
    """Drop trades with stop_dist < max(1pt, cost) (PREREG-1M L52, ledger F8).

    "1pt" == 1 mintick for the SPX-class instrument (genuine-choice #7; operator
    confirms at run time -- reported here). "cost" is the absolute round-trip cost in
    PRICE units (2*comm_pct*entry + 2*slip_tk*mintick), the same numerator as cost_R.
    Mutates trade.tradeable; returns the dropped count.
    """
    dropped = 0
    for t in trades:
        sd = t.stop_dist
        if sd is None or math.isnan(sd):
            # no stop distance to test -> cannot certify tradeable; keep but flag.
            # (only matters when R is risk-based; the floor is a stop-geometry test.)
            continue
        cost_price = 2.0 * COMM_PCT * (0.0 if math.isnan(t.entry_price) else t.entry_price) \
            + 2.0 * SLIP_TK * mintick
        floor = max(1.0 * mintick, cost_price)
        if sd < floor:
            t.tradeable = False
            dropped += 1
    return dropped


def compute_per_trade(trades, mintick):
    """Fill r_gross / cost_r / r_net + ET fields + killzone on each trade.

    cost_r is computed BEFORE any outcome is read (geometry). Applies the
    tradeability floor first (PREREG-1M L52). Returns the dropped count.
    """
    dropped = apply_tradeability_floor(trades, mintick)
    # ET fields (UTC epoch -> ET) where epoch present.
    epochs = np.array([t.entry_epoch_ms for t in trades], float)
    has_epoch = ~np.isnan(epochs)
    if has_epoch.any():
        hh, mm, dow, et_date = M.et_fields(epochs[has_epoch])
        j = 0
        for i, t in enumerate(trades):
            if has_epoch[i]:
                t.et_hour, t.et_min, t.et_dow = int(hh[j]), int(mm[j]), int(dow[j])
                t.et_date = et_date[j]          # retained for the multi-regime span check (R6-3)
                t.killzone = killzone_of(t.et_hour, t.et_min)
                j += 1
    for t in trades:
        t.r_gross = r_gross(t)
        t.cost_r = cost_r(t.entry_price, t.stop_dist, mintick)
        t.r_net = t.r_gross - t.cost_r if not (math.isnan(t.r_gross) or math.isnan(t.cost_r)) \
            else float("nan")
    return dropped


def median_hurdle(trades):
    """HURDLE = 4 * median(cost_R) over the TRADEABLE population (PREREG-1M L55)."""
    costs = np.array([t.cost_r for t in trades
                      if t.tradeable and not math.isnan(t.cost_r) and not math.isinf(t.cost_r)],
                     float)
    if len(costs) == 0:
        return float("nan"), float("nan")
    med = float(np.median(costs))
    return MIN_RMULT * med, med


# =============================================================================
# SECTION 3 -- entry-event blocks + block-resampled E[R] CI
# =============================================================================
def assign_blocks(trades, key="auto"):
    """Assign an entry-event block id to each trade (PREREG-1M L62, genuine-choice #4).

    One block per arming raid / FVG entry. The export does not always carry an explicit
    arm key, so the default ("auto") blocks by ENTRY EPOCH-MINUTE (one arming event per
    ET wall-clock minute) when epochs are present, else falls back to one-trade-per-block
    (iid). The iid fallback is FLAGGED (R6-2): the function returns (n_blocks, mode) with
    mode in {"event","iid"} so the operator confirms the block key before CIs run -- it is
    forbidden to switch iid<->block AFTER outcomes, and the entry-event block is the frozen
    verdict instrument (PREREG-1M L62-63). On the iid path a WARN is printed and a STABLE
    key (trade_num, R8-2) is used so block ids are deterministic across runs (not id()).
    Mutates trade.block_id. Returns (n_blocks, mode).
    """
    have_epoch = all(not math.isnan(t.entry_epoch_ms) for t in trades) and len(trades) > 0
    mode = "event"
    if key == "auto" and have_epoch:
        # block key = entry epoch floored to the minute.
        keyfn = lambda t: int(t.entry_epoch_ms // 60000)
    elif key == "trade":
        keyfn = lambda t: t.trade_num
        mode = "iid"
    else:
        # per-trade fallback (iid) when no epoch is available. Use a STABLE key
        # (trade_num, R8-2), NOT the nondeterministic id(t), and WARN.
        keyfn = lambda t: t.trade_num
        mode = "iid"
    if mode == "iid" and key == "auto":
        print("WARN assign_blocks: no usable entry epoch -> iid one-trade-per-block "
              "fallback (entry-event block instrument UNAVAILABLE; PREREG-1M L62-63). "
              "Verdict on a verdict-bearing export will read INSUFFICIENT-N.")
    seen = {}
    nb = 0
    for t in sorted(trades, key=keyfn):
        kk = keyfn(t)
        if kk not in seen:
            seen[kk] = nb
            nb += 1
        t.block_id = seen[kk]
    return nb, mode


def block_means(values, block_ids):
    """Collapse per-trade values into one mean per entry-event block (de-overlap).

    Returns a 1-D array of length n_blocks (the resampling units for the bootstrap and
    the permutation). PREREG-1M L62-63: the bootstrap unit is the entry-event block,
    NOT the iid trade row.
    """
    values = np.asarray(values, float)
    block_ids = np.asarray(block_ids, int)
    out = []
    for b in np.unique(block_ids):
        sel = block_ids == b
        out.append(np.nanmean(values[sel]))
    return np.array(out, float)


def block_ci(values, block_ids, B=BOOT_B, seed=20260618, alpha=ALPHA):
    """Block-resampled CI of the mean (PREREG-1M verdict instrument).

    Collapses to per-block means, then applies the CIRCULAR moving-block bootstrap from
    the shared offline module with a block length set by the per-block autocorrelation
    (PREREG-W GC-1 rule, reused here). Returns (mean, lo, hi, n_blocks, block_len).
    """
    bm = block_means(values, block_ids)
    bm = bm[~np.isnan(bm)]
    if len(bm) == 0:
        return (float("nan"), float("nan"), float("nan"), 0, 0)
    L = M.autocorr_block_len(bm, cutoff=0.10, floor=1, cap=8)
    lo, hi = M.moving_block_bootstrap_ci(bm, block_len=L, B=B, seed=seed, alpha=alpha)
    return (float(bm.mean()), lo, hi, len(bm), L)


# =============================================================================
# SECTION 4 -- gate-ablation marginal E[R] (across the 8 labeled exports)
# =============================================================================
def marginal_gate_er(labelled, gate, B=BOOT_B, seed=20260618):
    """Marginal E[R] of one gate (PREREG-1M L77; "earns its place, CI excludes 0").

    labelled : dict label -> list[Trade] (the 8 ablation exports for ONE useBody variant,
               already per-trade-computed + block-assigned, tradeable-only).
    gate     : one of GATES ("bias"/"pd"/"killzone").
    The marginal effect is E[R | gate ON] - E[R | gate OFF], pooling the 4 ON labels and
    the 4 OFF labels for that gate. CI is a block bootstrap on the DIFFERENCE of the two
    pooled per-block means (resample each side's blocks independently, circular). A gate
    "earns its place" iff this CI excludes 0.
    Returns dict(diff, lo, hi, n_on, n_off, excludes_zero).
    """
    assert gate in GATES, f"unknown gate {gate}"
    gi = GATES.index(gate)
    on_vals, on_blocks, off_vals, off_blocks = [], [], [], []
    boff = 0  # offset off-side block ids so they don't collide with on-side
    bon = 0
    for label, trades in labelled.items():
        # label form bias{b}_pd{p}_kz{k}; gate ON iff that flag is 1.
        flags = _flags_from_label(label)
        rs = [t.r_net for t in trades if t.tradeable and not math.isnan(t.r_net)]
        bids = [t.block_id for t in trades if t.tradeable and not math.isnan(t.r_net)]
        if flags[gi] == 1:
            on_vals += rs
            on_blocks += [b + bon for b in bids]
            bon = (max(on_blocks) + 1) if on_blocks else bon
        else:
            off_vals += rs
            off_blocks += [b + boff for b in bids]
            boff = (max(off_blocks) + 1) if off_blocks else boff
    on_bm = block_means(on_vals, on_blocks) if on_vals else np.array([])
    off_bm = block_means(off_vals, off_blocks) if off_vals else np.array([])
    on_bm = on_bm[~np.isnan(on_bm)]
    off_bm = off_bm[~np.isnan(off_bm)]
    if len(on_bm) == 0 or len(off_bm) == 0:
        return {"diff": float("nan"), "lo": float("nan"), "hi": float("nan"),
                "n_on": int(on_bm.size), "n_off": int(off_bm.size), "excludes_zero": False}
    diff = float(on_bm.mean() - off_bm.mean())
    rng = np.random.default_rng(seed)
    Lon = M.autocorr_block_len(on_bm, 0.10, 1, 8)
    Loff = M.autocorr_block_len(off_bm, 0.10, 1, 8)
    diffs = np.empty(B)
    for b in range(B):
        s_on = _circ_block_resample(on_bm, Lon, rng)
        s_off = _circ_block_resample(off_bm, Loff, rng)
        diffs[b] = s_on.mean() - s_off.mean()
    lo = float(np.quantile(diffs, ALPHA / 2.0))
    hi = float(np.quantile(diffs, 1.0 - ALPHA / 2.0))
    return {"diff": diff, "lo": lo, "hi": hi,
            "n_on": int(on_bm.size), "n_off": int(off_bm.size),
            "excludes_zero": bool(lo > 0.0 or hi < 0.0)}


def _flags_from_label(label):
    """Parse 'bias{b}_pd{p}_kz{k}' -> (b, p, k) ints."""
    parts = label.split("_")
    b = int(parts[0].replace("bias", ""))
    p = int(parts[1].replace("pd", ""))
    k = int(parts[2].replace("kz", ""))
    return (b, p, k)


def _circ_block_resample(x, L, rng):
    """One circular moving-block resample of x to length len(x) (helper for diffs)."""
    n = len(x)
    L = max(1, min(int(L), n))
    n_blocks = int(np.ceil(n / L))
    starts = rng.integers(0, n, size=n_blocks)
    idx = (starts[:, None] + np.arange(L)[None, :]).ravel() % n
    return x[idx[:n]]


# =============================================================================
# SECTION 5 -- DOW / arm-time-killzone one-slice permutation (max-stat, B>=5000)
# =============================================================================
def one_slice_permutation(trades, slice_attr, B=PERM_B, seed=20260618):
    """Max-stat one-slice permutation null (PREREG-1M L77-78; genuine-choice #6).

    slice_attr : 'et_dow' or 'killzone'. The observed statistic is the MAX over slices of
    that slice's mean r_net (per-block-collapsed within the slice). Under the null, slice
    LABELS are permuted across entry-event blocks (so a slice gets a random set of blocks),
    the per-slice block-mean is recomputed, the MAX taken, repeated B times. p = P(null max
    >= observed max). The edge "lives in one slice" iff p < 0.05 (one slice's mean exceeds
    what random slice-labeling produces) AND that slice's mean is the carrier.
    Returns dict(observed_max, slice, p, per_slice).
    """
    trd = [t for t in trades if t.tradeable and not math.isnan(t.r_net)]
    if len(trd) == 0:
        return {"observed_max": float("nan"), "slice": None, "p": float("nan"),
                "per_slice": {}}
    # collapse to per-block: each block keeps its slice label + its mean r_net.
    block_ids = np.array([t.block_id for t in trd], int)
    rnets = np.array([t.r_net for t in trd], float)
    slices = np.array([getattr(t, slice_attr) for t in trd])
    ub = np.unique(block_ids)
    block_slice = []
    block_val = []
    for b in ub:
        sel = block_ids == b
        # a block belongs to the slice of its (first) trade; use the modal slice.
        vals_s = slices[sel]
        block_slice.append(vals_s[0])
        block_val.append(np.nanmean(rnets[sel]))
    block_slice = np.array(block_slice)
    block_val = np.array(block_val, float)
    uniq_slices = np.unique(block_slice)
    per_slice = {}
    obs_max = -np.inf
    obs_slice = None
    for s in uniq_slices:
        m = float(block_val[block_slice == s].mean())
        per_slice[str(s)] = m
        if m > obs_max:
            obs_max, obs_slice = m, s
    n_per = {s: int((block_slice == s).sum()) for s in uniq_slices}
    rng = np.random.default_rng(seed)
    ge = 0
    for _ in range(B):
        perm = rng.permutation(block_slice)
        mx = -np.inf
        for s in uniq_slices:
            sel = perm == s
            if sel.any():
                m = block_val[sel].mean()
                if m > mx:
                    mx = m
        if mx >= obs_max:
            ge += 1
    p = (ge + 1) / (B + 1)   # add-one (Davison-Hinkley)
    return {"observed_max": float(obs_max), "slice": str(obs_slice), "p": float(p),
            "per_slice": per_slice, "n_per_slice": {str(k): v for k, v in n_per.items()}}


# =============================================================================
# SECTION 6 -- drop-top-k concentration (on entry-event blocks)
# =============================================================================
def drop_top_k_check(trades, k=None):
    """Edge survives removing the top-k entry-event BLOCKS (PREREG-1M L63,L132).

    Collapses r_net to per-block means, then removes the k largest blocks. Default
    k = ceil(0.06 * n_blocks) to hold the D2 sibling's ~6% removal fraction at the larger
    block count (genuine-choice #5). Returns dict(full_mean, dropped_mean, k, n_blocks,
    survives) where `survives` is dropped_mean > 0 (edge not carried by a handful).
    """
    trd = [t for t in trades if t.tradeable and not math.isnan(t.r_net)]
    bm = block_means([t.r_net for t in trd], [t.block_id for t in trd]) if trd else np.array([])
    bm = bm[~np.isnan(bm)]
    nb = len(bm)
    if nb == 0:
        return {"full_mean": float("nan"), "dropped_mean": float("nan"), "k": 0,
                "n_blocks": 0, "survives": False}
    if k is None:
        k = int(math.ceil(DROP_TOP_K_FRAC * nb))
    full = float(bm.mean())
    dropped = M.drop_top_k(bm, k)
    return {"full_mean": full, "dropped_mean": dropped, "k": int(k),
            "n_blocks": nb, "survives": bool(not math.isnan(dropped) and dropped > 0.0)}


# =============================================================================
# SECTION 7 -- static-$200K recompute (strip strategy.equity compounding)
# =============================================================================
def static_200k_pnl(trades):
    """Recompute $ PnL on a STATIC $200K base (PREREG-1M L59,L32; REPORT-ONLY).

    Strips strategy.equity compounding: each trade's $ = r_net * (RISK_PCT * $200K),
    a constant 1R = $1000 regardless of running equity. Returns dict with the static $
    series, total, and the static-equity peak-to-trough drawdown (the $/DD currency,
    which is REPORT-ONLY -- never the verdict).
    """
    one_r = RISK_PCT * STATIC_EQUITY   # $1000 on a static $200K @ 0.5%
    dollars = np.array([t.r_net * one_r for t in trades
                        if t.tradeable and not math.isnan(t.r_net)], float)
    equity = STATIC_EQUITY + np.cumsum(dollars) if len(dollars) else np.array([STATIC_EQUITY])
    peak = np.maximum.accumulate(equity)
    dd = (equity - peak)
    max_dd = float(dd.min()) if len(dd) else 0.0
    max_dd_pct = max_dd / STATIC_EQUITY
    return {"one_r": one_r, "total_dollars": float(dollars.sum()),
            "max_dd_dollars": max_dd, "max_dd_pct": float(max_dd_pct),
            "n": int(len(dollars))}


# =============================================================================
# SECTION 8 -- starvation parse (closedtrades vs skip counts)
# =============================================================================
def parse_starvation(skip_json_path):
    """Parse a starvation diagnostic JSON (closedtrades vs skip counts; PREREG-1M B4).

    The 1M Pine prints skip-counter cells (skip:cost/R, skip:no-draw, ...) + closedtrades.
    The operator exports those as a small JSON sidecar. Returns the parsed dict augmented
    with `insufficient_n` = closedtrades < N_FLOOR. SKIPs (returns None) when absent.
    """
    p = Path(skip_json_path)
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    closed = int(d.get("closedtrades", d.get("closed_trades", 0)))
    d["closedtrades"] = closed
    d["insufficient_n"] = closed < N_FLOOR
    return d


# =============================================================================
# SECTION 8b -- multi-regime span check (R6-3) + R-basis diagnostic (R6-5)
# =============================================================================
# PREREG-1M genuine-choice #3 (L130) makes the export window a BINDING SPEC: it MUST
# span BOTH the 2020-2023 chop AND the 2023-2026 trend. A single-regime window is a
# Forbidden #4 move and VOIDS the verdict. The split date is OPERATOR-PARAMETERIZED
# (not hardcoded); this documented default sits at the chop/trend boundary.
DEFAULT_REGIME_SPLIT = "2023-06-15"


def regime_span_check(entry_dates, split=DEFAULT_REGIME_SPLIT):
    """Flag a single-regime (one-side-of-split) entry-date window (R6-3; Forbidden #4).

    entry_dates : iterable of datetime.date (or None). split : 'YYYY-MM-DD' operator value.
    Returns (flagged, (min_date, max_date)). flagged is True iff the [min,max] entry-date
    span lies WHOLLY on one side of the split (a single-regime window that voids the verdict).
    Empty/all-None -> (False, (None, None)) (nothing to test; the n-floor handles emptiness).
    """
    dates = [d for d in entry_dates if d is not None]
    if not dates:
        return False, (None, None)
    split_d = pd.to_datetime(split).date()
    dmin, dmax = min(dates), max(dates)
    # single-regime iff the whole span is strictly before, or on/after, the split.
    single = (dmax < split_d) or (dmin >= split_d)
    return bool(single), (dmin, dmax)


def r_basis_diagnostic(trades):
    """Distinct diagnostic when NO trade has a usable R basis (R6-5).

    When every r_net is nan because neither a risk nor a stop_dist column was found,
    a bare 'n<100' is opaque. Returns a specific message naming the missing columns, or
    None when at least one trade has a usable R basis (no diagnostic needed).
    """
    n = len(trades)
    n_with_basis = sum(
        1 for t in trades
        if (t.risk is not None and not math.isnan(t.risk) and t.risk > 0)
        or (not math.isnan(t.stop_dist) and t.stop_dist > 0)
    )
    if n == 0 or n_with_basis > 0:
        return None
    return (f"{n_with_basis} of {n} trades had a usable R basis: no risk and no stop_dist "
            "column found -- supply a risk/stop column or the L53 data-window hurdleR sidecar")


# =============================================================================
# SECTION 9 -- VERDICT (section 6, per useBody variant)
# =============================================================================
@dataclass
class VariantResult:
    use_body: bool
    n_trades: int
    n_blocks: int
    dropped_floor: int
    er_mean: float
    er_lo: float
    er_hi: float
    hurdle: float
    median_cost_r: float
    gate_marginals: dict = field(default_factory=dict)   # gate -> marginal dict
    dow_perm: dict = field(default_factory=dict)
    kz_perm: dict = field(default_factory=dict)
    droptopk: dict = field(default_factory=dict)
    static: dict = field(default_factory=dict)
    verdict: str = ""
    reasons: list = field(default_factory=list)


def verdict_for_variant(default_trades, labelled, use_body, mintick,
                        boot_seed=20260618, perm_seed=20260618, block_mode=None):
    """Compute the section 6 1M verdict for ONE useBody variant (PREREG-1M L75-79).

    default_trades : the gate-bearing config trades (dolMode=range-extreme, all gates ON)
                     for this variant -- the headline E[R] population.
    labelled       : dict label -> list[Trade] (the 8 ablation exports) for this variant.
    block_mode     : "event" or "iid" for the verdict-bearing (default) export. When None,
                     it is INFERRED ("iid" iff any default trade lacks a usable entry epoch).
                     On mode=="iid" the entry-event block instrument is unavailable, so a
                     verdict-bearing PASS is refused -> INSUFFICIENT-N (R6-2; PREREG-1M L62-63).
    Both must already be per-trade-computed + block-assigned + tradeable-flagged.
    Returns a VariantResult. nearest-pool NEVER enters here (REPORT-ONLY, Forbidden #5).
    """
    trd = [t for t in default_trades if t.tradeable and not math.isnan(t.r_net)]
    n = len(trd)
    if block_mode is None:
        # infer: iid iff any verdict-bearing trade has no usable entry epoch.
        has_all_epochs = bool(default_trades) and all(
            not math.isnan(t.entry_epoch_ms) for t in default_trades)
        block_mode = "event" if has_all_epochs else "iid"
    hurdle, med_cost = median_hurdle(default_trades)
    res = VariantResult(use_body=use_body, n_trades=n,
                        n_blocks=len(set(t.block_id for t in trd)),
                        dropped_floor=sum(1 for t in default_trades if not t.tradeable),
                        er_mean=float("nan"), er_lo=float("nan"), er_hi=float("nan"),
                        hurdle=hurdle, median_cost_r=med_cost)

    # --- n-floor gate (mandatory power gate; PREREG-1M L69,L79) ---
    if n < N_FLOOR:
        res.verdict = "INSUFFICIENT-N"
        res.reasons.append(f"n={n} < n-floor {N_FLOOR}: claim unfalsifiable on this data; "
                           "HALT, re-spec the DOL target, re-test on an independent "
                           "multi-regime window")
        return res

    # --- entry-event block instrument gate (R6-2; PREREG-1M L62-63) ---
    # The verdict instrument is the ENTRY-EVENT block. If the export had no usable entry
    # epoch, assign_blocks fell to iid (one-trade-per-block), which understates SE and
    # degenerates the one-slice permutation -- the instrument is unavailable, so a PASS
    # cannot be earned. Refuse and read INSUFFICIENT-N rather than a biased RESOLVED.
    if block_mode == "iid":
        res.verdict = "INSUFFICIENT-N"
        res.reasons.append("entry-event block instrument UNAVAILABLE: blocks assigned iid "
                           "(no usable entry epoch in the verdict-bearing export). The "
                           "frozen verdict unit is the entry-event block (PREREG-1M L62-63); "
                           "iid understates SE and degenerates the one-slice permutation. "
                           "HALT -- supply parseable entry times (Date/Time or epoch_ms) "
                           "before any verdict.")
        return res

    # --- headline block-resampled E[R] CI ---
    mean, lo, hi, nb, _L = block_ci([t.r_net for t in trd],
                                    [t.block_id for t in trd], B=BOOT_B, seed=boot_seed)
    res.er_mean, res.er_lo, res.er_hi, res.n_blocks = mean, lo, hi, nb

    # --- gate marginals (PREREG-1M L77: each RETAINED gate must show POSITIVE marginal
    #     E[R] with CI excluding 0 -- "earns its place, not merely prunes n"). A gate earns
    #     iff diff > 0 AND its CI lower bound > 0 (positive AND excludes 0). RESOLVED needs
    #     ALL three; FALSIFIED's "both gates add nothing" (L78) is the no-gate-earns case. ---
    for g in GATES:
        res.gate_marginals[g] = marginal_gate_er(labelled, g, B=BOOT_B, seed=boot_seed)

    def _gate_earns(m):
        return bool(m["excludes_zero"] and not math.isnan(m["diff"]) and m["diff"] > 0.0
                    and m["lo"] > 0.0)

    gates_earning = {g: _gate_earns(m) for g, m in res.gate_marginals.items()}
    all_gates_earn = all(gates_earning.values())
    any_gate_earns = any(gates_earning.values())

    # --- one-slice permutations (DOW + arm-time killzone) ---
    res.dow_perm = one_slice_permutation(trd, "et_dow", B=PERM_B, seed=perm_seed)
    res.kz_perm = one_slice_permutation(trd, "killzone", B=PERM_B, seed=perm_seed + 1)
    one_slice_edge = (res.dow_perm.get("p", 1.0) < ALPHA) or (res.kz_perm.get("p", 1.0) < ALPHA)

    # --- drop-top-k concentration ---
    res.droptopk = drop_top_k_check(trd)

    # --- static-$200K (report-only) ---
    res.static = static_200k_pnl(trd)

    # --- VERDICT (binary; PREREG-1M L75-79) ---
    ci_clears = (not math.isnan(lo)) and (not math.isnan(hurdle)) and (lo > hurdle)
    droptopk_holds = res.droptopk.get("survives", False)

    # RESOLVED requires EACH retained gate to earn its place (PREREG-1M L77: "each
    # retained gate ... positive marginal E[R] with CI excluding 0"), not merely one.
    if ci_clears and all_gates_earn and (not one_slice_edge) and droptopk_holds:
        res.verdict = "RESOLVED"
        res.reasons.append(f"E[R] CI lower {lo:+.4f}R > hurdle {hurdle:+.4f}R at n={n}")
        res.reasons.append("each retained gate (bias/PD/killzone) shows positive marginal "
                           "E[R] with CI excluding 0: "
                           + ", ".join(f"{g}={res.gate_marginals[g]['diff']:+.4f}R"
                                       for g in GATES))
        res.reasons.append("no single DOW or arm-time killzone slice carries the edge "
                           f"(DOW p={res.dow_perm['p']:.3f}, KZ p={res.kz_perm['p']:.3f})")
        res.reasons.append(f"drop-top-k holds (dropped mean {res.droptopk['dropped_mean']:+.4f}R, "
                           f"k={res.droptopk['k']}/{res.droptopk['n_blocks']})")
        res.reasons.append("RESOLVED routes to forward / out-of-regime confirmation -- "
                           "NOT lock, NOT deploy (PREREG-1M power disclosure)")
    else:
        res.verdict = "FALSIFIED"
        if not ci_clears:
            res.reasons.append(f"E[R] CI subset of (-inf, hurdle]: lower {lo:+.4f}R "
                               f"<= hurdle {hurdle:+.4f}R")
        if not any_gate_earns:
            res.reasons.append("both gates add nothing: no retained gate's marginal-E[R] "
                               "CI excludes 0")
        elif not all_gates_earn:
            failing = [g for g, e in gates_earning.items() if not e]
            res.reasons.append("not every retained gate earns its place (PREREG-1M L77): "
                               f"gate(s) {failing} have no positive marginal-E[R] CI "
                               "excluding 0")
        if one_slice_edge:
            res.reasons.append(f"edge lives in one slice (DOW p={res.dow_perm['p']:.3f} "
                               f"slice={res.dow_perm['slice']}; KZ p={res.kz_perm['p']:.3f} "
                               f"slice={res.kz_perm['slice']})")
        if not droptopk_holds:
            res.reasons.append(f"drop-top-k removes the edge (dropped mean "
                               f"{res.droptopk['dropped_mean']:+.4f}R)")
    return res


# =============================================================================
# SECTION 10 -- main() (skips gracefully when the export is absent)
# =============================================================================
DEFAULT_EXPORT_DIR = Path(r"C:/Users/joshu/Downloads")
# Default mintick for the SPX-class instrument under test (PREREG-1M genuine-choice #7;
# operator confirms "1pt" = correct minimum tick distance). 0.1 index points is typical
# for SPX500 CFDs; surfaced + reported so a wrong tick is visible, not silent.
DEFAULT_MINTICK = 0.1


def _expected_exports():
    """The exact export set the 1M verdict needs (PREREG-1M; audit-hook L120)."""
    needed = []
    for ub in (False, True):
        for label in ABLATION_LABELS:
            needed.append(f"ict_1m_listoftrades_useBody{int(ub)}_{label}_range-extreme.csv")
    return needed


def load_manifest_or_dir(arg):
    """Resolve `arg` -> dict (use_body, label) -> csv path.

    arg is either a directory (file names matched by the _expected_exports() convention)
    or a JSON manifest mapping "useBody{0,1}_<label>" -> csv path. nearest-pool exports, if
    present, are loaded separately by the caller for REPORT-ONLY (never the verdict).
    Returns (mapping, missing_list).
    """
    p = Path(arg)
    mapping = {}
    missing = []
    if p.is_file() and p.suffix.lower() == ".json":
        with open(p, "r", encoding="utf-8") as fh:
            man = json.load(fh)
        for ub in (False, True):
            for label in ABLATION_LABELS:
                key = f"useBody{int(ub)}_{label}"
                if key in man and Path(man[key]).exists():
                    mapping[(ub, label)] = Path(man[key])
                else:
                    missing.append(key)
        return mapping, missing
    # directory mode
    for ub in (False, True):
        for label in ABLATION_LABELS:
            fname = f"ict_1m_listoftrades_useBody{int(ub)}_{label}_range-extreme.csv"
            fp = p / fname
            if fp.exists():
                mapping[(ub, label)] = fp
            else:
                missing.append(fname)
    return mapping, missing


def run(arg, mintick=DEFAULT_MINTICK, starvation_json=None,
        regime_split=DEFAULT_REGIME_SPLIT):
    """End-to-end 1M layer run on a resolved export set. Returns dict of VariantResults.

    Assumes the export set is COMPLETE (8 labels x 2 variants). The gate-bearing config
    (all gates ON) per variant is label 'bias1_pd1_kz1'. regime_split is the operator-
    supplied chop/trend boundary used for the Forbidden #4 single-regime span check (R6-3).
    """
    mapping, missing = load_manifest_or_dir(arg)
    if missing:
        raise FileNotFoundError(
            "1M verdict needs the FULL ablation matrix (8 labels x 2 useBody = 16 exports). "
            f"Missing: {missing}")
    out = {}
    diagnostics = {}
    for ub in (False, True):
        labelled = {}
        default_mode = "event"
        for label in ABLATION_LABELS:
            trades, _stats = load_list_of_trades(mapping[(ub, label)])
            compute_per_trade(trades, mintick)
            _nb, mode = assign_blocks(trades, key="auto")
            if label == "bias1_pd1_kz1":
                default_mode = mode
            # canonical label form for marginal_gate_er parsing:
            labelled[label] = trades
        default_trades = labelled["bias1_pd1_kz1"]
        # R6-5: distinct R-basis diagnostic on the verdict-bearing export.
        rbasis = r_basis_diagnostic([t for t in default_trades])
        # R6-3: multi-regime span (Forbidden #4) on the verdict-bearing export dates.
        flagged, span = regime_span_check([t.et_date for t in default_trades],
                                          split=regime_split)
        diagnostics[ub] = {"r_basis": rbasis, "regime_flagged": flagged,
                           "regime_span": span, "block_mode": default_mode}
        out[ub] = verdict_for_variant(default_trades, labelled, use_body=ub,
                                      mintick=mintick, block_mode=default_mode)
    out["diagnostics"] = diagnostics
    if starvation_json:
        out["starvation"] = parse_starvation(starvation_json)
    return out


def main(argv=None):
    import sys
    argv = sys.argv[1:] if argv is None else argv
    # operator-parameterized chop/trend split for the Forbidden #4 span check (R6-3):
    #   --regime-split YYYY-MM-DD  (default DEFAULT_REGIME_SPLIT).
    regime_split = DEFAULT_REGIME_SPLIT
    pos = []
    i = 0
    while i < len(argv):
        if argv[i] == "--regime-split" and i + 1 < len(argv):
            regime_split = argv[i + 1]
            i += 2
            continue
        pos.append(argv[i])
        i += 1
    arg = pos[0] if pos else str(DEFAULT_EXPORT_DIR)
    mapping, missing = load_manifest_or_dir(arg)
    if missing:
        print("=" * 72)
        print("Q-ICT-1M (Layer 4 / Execution) -- NO COMPLETE EXPORT SET YET. SKIPPING.")
        print("=" * 72)
        print("The operator has not yet run TV through the full ablation matrix.")
        print(f"Looked in: {arg}")
        print("\nNEED exactly 16 TV 'List of Trades' exports (8 ablation labels x 2 useBody),")
        print("all on the gate-bearing config dolMode=range-extreme (PREREG-1M L41, L120):")
        for f in _expected_exports():
            print(f"  - {f}")
        print("\nOptionally a starvation sidecar JSON {closedtrades, skip:cost/R, ...}")
        print("(PREREG-1M B4). nearest-pool exports are REPORT-ONLY (Forbidden #5) and")
        print("never enter the verdict.")
        print("\nEach export MUST carry parseable entry times (a 'Date/Time' cell or an")
        print("epoch_ms column; UTC) AND a risk OR stop_dist column for the R basis --")
        print("without an entry time the blocks fall to iid (INSUFFICIENT-N), and without")
        print("a risk/stop column 0 of N trades have a usable R basis (R6-5).")
        print("\nMulti-regime span (Forbidden #4): the export window MUST span the")
        print(f"2020-2023 chop AND 2023-2026 trend. Split via --regime-split YYYY-MM-DD "
              f"(default {DEFAULT_REGIME_SPLIT}).")
        print("\nProvide either a directory containing those files, or a JSON manifest")
        print("mapping 'useBody{0,1}_<label>' -> csv path.")
        return 0
    results = run(arg, mintick=DEFAULT_MINTICK, regime_split=regime_split)
    diags = results.get("diagnostics", {})
    for ub in (False, True):
        r = results[ub]
        d = diags.get(ub, {})
        print(f"\n=== useBody={ub} === verdict: {r.verdict}")
        unit = d.get("block_mode", "event")
        print(f"  n={r.n_trades} blocks={r.n_blocks} unit={unit} "
              f"dropped(floor)={r.dropped_floor}")
        print(f"  E[R]={r.er_mean:+.4f}  CI=[{r.er_lo:+.4f},{r.er_hi:+.4f}]  "
              f"hurdle(4*medCost)={r.hurdle:+.4f}")
        span = d.get("regime_span", (None, None))
        print(f"  entry-date span: {span[0]} -> {span[1]} (split {regime_split})")
        if d.get("regime_flagged"):
            print("   - FLAG Forbidden #4 single-regime window: the entry-date span lies "
                  "wholly on one side of the split -> the multi-regime BINDING SPEC "
                  "(PREREG-1M L130) is unmet; this VOIDS the verdict. HALT.")
        if d.get("r_basis"):
            print(f"   - {d['r_basis']}")
        for reason in r.reasons:
            print(f"   - {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
