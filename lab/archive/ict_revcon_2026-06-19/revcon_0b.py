"""Q-ICT-1H-REVCON-1 / Phase 0b -- CONFIRMATORY bias-conditioned discriminator.

PRE-REGISTERED (PREREG-0B, RATIFIED). Runs ONLY after PREREG-0B is committed (firewall)
and on a GENUINELY OUT-OF-SAMPLE regime page (the operator-chosen bear/chop discriminator,
NOT the benign window already explored in 0a). This module emits a VERDICT against the
PREREG-0B sec-6 gate -- it is not exploratory.

DATA PATH (all validated 2026-06-19):
  * 1H OHLC <- BAR_EXPORT v0.1 pages (decode_bar_signal); the BAR feed is byte-identical to
    the TV chart feed (parity 2922/2922 bars, 0.000000 OHLC diff).
  * zone   <- offline H.zone_series(60, 0.05); reproduces Pine's exported `zone` 100%.
  * structBias <- offline close-vs-weekly-EMA20, PRIOR-week ([1]) lag -- the FAITHFUL gate
    definition (ict_1m_execution_DRAFT.pine L103-105: structBias = sign(wClose[1]-wEma[1]);
    ict_weekly_bias_DRAFT.pine L68-69,116: vStruct=sign(close-wEMA20), gateBias=vStruct;
    L111-112 confirms the live gate is structBias-only, NOT EMA+structure).

FAMILY (PREREG-0B): the SOLE partition is the prior-week structBias sign. Cells =
{prem,disc} x {bias +1,-1}; each cell is tested 2-sided {reversion, continuation} at the
FIXED gate anchor (lookN=60, eqBand=0.05). Penalty = deflated max-stat over the 8
directional rates (4 cells x 2 directions). n-floor = 30 per cell on floor(N_scored/fwdK).

VERDICT (PREREG-0B sec-6, single-regime discriminator):
  RESOLVED      a directional cell clears 0.5 by >=2pp under BOTH stride AND block, beats
                its bias-bucket-local placebo, survives the 8-way penalty, n_floor>=30, and
                does not flip across halves  -> escalate to the FULL multi-regime panel.
  FALSIFIED     no adequately-powered cell's directional rate clears the penalized gate ->
                the bias axis carries no edge in the out-of-sample regime -> close (the 1H
                layer has no stable conditional edge on either axis; forward-watch belt).
  INSUFFICIENT-N every cell below the n-floor -> re-spec (export a longer / different page).
  AMBIGUOUS     a cell clears the CI but fails placebo/penalty/halves -> hold; name re-test.

REUSES (audit-verified, not re-ported): harness_1h.{zone_series, recompute_hits,
stride_rate_ci, block_rate_ci, placebo_random_eq, halves_margin_flip, _week_key_et,
GAMMA, MARGIN_PP, N_FLOOR, FWDK, LOOKN_LOCK, EQBAND_LOCK}; revcon_probe_0a.{recompute_
continuation, weekly_bias_proxy_ema}; core/bar_export_loader.decode_bar_signal.

Run tests:  python -m pytest lab/analysis/ict_revcon_2026-06-19/test_revcon_0b.py -q
Run verdict: python lab/analysis/ict_revcon_2026-06-19/revcon_0b.py --bar <page.csv> [--bar <page2.csv> ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_CASCADE = _HERE.parent / "ict_cascade_2026-06-18"
_CORE = _HERE.parent.parent.parent / "core"
sys.path.insert(0, str(_CORE))
sys.path.insert(0, str(_CASCADE))
sys.path.insert(0, str(_HERE))
import harness_1h as H  # noqa: E402
import _ict_offline as M  # noqa: E402
import revcon_probe_0a as P  # noqa: E402
import bar_export_loader as BX  # noqa: E402

FWDK = H.FWDK
N_CELLS_DIRECTIONAL = 8   # {prem,disc} x {bias +1,-1} x {rev,cont}; declared before run 1


# =============================================================================
# BAR_EXPORT PAGE LOADING (reuse decode_bar_signal; no core symbol-map dependency)
# =============================================================================
def load_bar_pages(paths):
    """Decode one or more BAR_EXPORT v0.1 List-of-Trades CSVs -> 1H OHLCV DataFrame
    (epoch, o, h, l, c, v). Entry rows carry the bar OHLCV in the Signal field; pages are
    concatenated, deduped on bar-open epoch (keep last), and sorted ascending."""
    if isinstance(paths, (str, Path)):
        paths = [paths]
    frames = []
    for p in paths:
        raw = pd.read_csv(p, encoding="utf-8-sig")
        raw.columns = [str(c).strip() for c in raw.columns]
        if "Type" not in raw.columns or "Signal" not in raw.columns:
            raise ValueError(f"BAR_EXPORT missing Type/Signal columns: {p}")
        ent = raw[raw["Type"].astype(str).str.startswith("Entry")]
        price_cols = [c for c in raw.columns if c.lower().startswith("price")]  # e.g. "Price USD"
        pcol = price_cols[0] if price_cols else None
        recs = []
        skipped = 0
        for _i, r in ent.iterrows():
            try:
                d = BX.decode_bar_signal(r["Signal"])
            except ValueError:
                skipped += 1
                continue
            if "epoch_ms" not in d:   # legacy comment format lacks the UTC epoch (re-audit L-1)
                skipped += 1
                continue
            if pcol is not None:      # entry-price == encoded-close format-drift detector (L-2)
                px = float(r[pcol])
                tol = max(1e-5, abs(d["c"]) * 1e-4)
                if abs(px - d["c"]) > tol:
                    raise ValueError(
                        f"BAR_EXPORT format-drift cross-check FAIL in {p} at epoch "
                        f"{int(d['epoch_ms'])}: Price {px} != encoded close {d['c']}")
            recs.append((int(d["epoch_ms"]), d["o"], d["h"], d["l"], d["c"],
                         int(d.get("v", 0))))
        if skipped:
            print(f"=== load_bar_pages: skipped {skipped} undecodable/epoch-less entry rows "
                  f"in {p} ===", file=sys.stderr)
        frames.append(pd.DataFrame(recs, columns=["epoch", "o", "h", "l", "c", "v"]))
    df = (pd.concat(frames, ignore_index=True)
          .drop_duplicates("epoch", keep="last")
          .sort_values("epoch")
          .reset_index(drop=True))
    return df


def hour_export_from_ohlc(df) -> H.HourExport:
    """Build a HourExport from 1H OHLC with the OFFLINE native zone (zone_series, validated
    100% vs Pine). The premHit/discHit/zoneGate columns are placeholders (the verdict
    recomputes hits from zone/close; it never reads exported hit columns)."""
    e = df["epoch"].values.astype("int64")
    o = df["o"].values.astype(float)
    h = df["h"].values.astype(float)
    l = df["l"].values.astype(float)
    c = df["c"].values.astype(float)
    z = H.zone_series(h, l, c, H.LOOKN_LOCK, H.EQBAND_LOCK).astype(float)
    hh, _mm, _dow, dt = M.et_fields(e)
    return H.HourExport(epoch_ms=e, o=o, h=h, l=l, c=c, zone=z, eq=c,
                        prem_hit=np.zeros(len(c)), disc_hit=np.zeros(len(c)),
                        zone_gate=z, zone_agree=np.ones(len(c)),
                        et_hour=hh, et_date=dt, n=len(c))


def structbias_offline(epoch_ms, close, ema_len=20):
    """The FAITHFUL gate structBias (close vs weekly EMA-20, prior-week [1] lag). Delegates
    to the (LA-1-fixed, decision-time-observable) revcon_probe_0a.weekly_bias_proxy_ema --
    the Pine read confirmed the gate object is EMA-only, so this is faithful, not a proxy."""
    return P.weekly_bias_proxy_ema(epoch_ms, close, ema_len)


def load_weekly_gatebias(path):
    """Load a real weekly `gateBias`/`vStruct` export (cols time + gateBias|vStruct|structBias)
    -> (epoch, PRIOR-week sign). The export rows are SORTED ascending + deduped on the weekly
    bar BEFORE the [1] prior-week lag, so the lag is well-defined regardless of export row
    order (AUDIT data-faithfulness: never assume TV row order). The exported gateBias is the
    CURRENT-week structBias (Pine `gateBias=vStruct`); the `[1]` here makes it prior-week,
    matching the live gate's `priorGateBias=gateBias[1]`."""
    wb = pd.read_csv(path)
    cols = {c.lower(): c for c in wb.columns}
    tcol = cols.get("time")
    gcol = cols.get("gatebias", cols.get("vstruct", cols.get("structbias")))
    if tcol is None or gcol is None:
        raise ValueError("weekly gateBias export needs time + gateBias/vStruct/structBias "
                         f"columns; have {list(wb.columns)}")
    epoch = H._to_epoch_ms(wb[tcol]).astype("int64")
    sgn = np.sign(wb[gcol].to_numpy(float))
    df = (pd.DataFrame({"epoch": epoch, "sgn": sgn})
          .sort_values("epoch").drop_duplicates("epoch", keep="last").reset_index(drop=True))
    lagged = np.zeros(len(df))
    if len(lagged) > 1:
        lagged[1:] = df["sgn"].to_numpy()[:-1]   # prior-week sign (week 0 -> 0)
    return (df["epoch"].to_numpy(), lagged)


# =============================================================================
# CELL RATES (per zone x bias bucket; reversion + continuation, de-overlapped)
# =============================================================================
def _bias_per_bar(ex: H.HourExport, structbias):
    wb_epoch, wb_val = structbias
    wk_map = {k: (int(np.sign(v)) if v != 0 else 0)
              for k, v in zip(H._week_key_et(wb_epoch), np.asarray(wb_val, float))}
    return np.array([wk_map.get(w, 0) for w in H._week_key_et(ex.epoch_ms)], float)


def cell_rates(ex: H.HourExport, structbias):
    """Per (zone in {prem,disc}) x (bias in {+1,-1}) cell, per direction {rev,cont}: the
    de-overlapped stride rate + CI clearance, the block-bootstrap cross-check clearance,
    the bias-bucket-local placebo floor (beats_placebo), and halves-stationarity. All the
    per-cell evidence is computed HERE so verdict_0b's gate logic is pure over the cells
    dict (and unit-testable by injection)."""
    bias_bar = _bias_per_bar(ex, structbias)
    p_down, d_up, sc = H.recompute_hits(ex.zone, ex.c, FWDK)         # reversion
    p_up, d_dn, _sc = P.recompute_continuation(ex.zone, ex.c, FWDK)  # continuation
    spec = {"prem": (1, p_down, p_up), "disc": (-1, d_up, d_dn)}
    out = {}
    for zone, (target, rev_hit, cont_hit) in spec.items():
        for bias in (1, -1):
            idx = np.where(sc & (ex.zone == target) & (bias_bar == bias))[0]
            sc_bias = sc & (bias_bar == bias)   # bucket scorable set for the placebo freq-match
            cell = {"n_floor": int(len(idx) // FWDK), "n_scored": int(len(idx))}
            for direction, hit in (("rev", rev_hit), ("cont", cont_hit)):
                stride = H.stride_rate_ci(hit[idx].astype(float), idx)
                block = H.block_rate_ci(hit[idx].astype(float))
                # the forward direction this cell scores: prem-rev/disc-cont = down; else up
                down = (zone == "prem" and direction == "rev") or \
                       (zone == "disc" and direction == "cont")
                placebo = bucket_fwd_floor(ex.c, sc_bias, down, FWDK)
                halves = H.halves_margin_flip(hit[idx].astype(float), idx)
                cell[direction] = {
                    "rate": stride["rate"], "ci_lo": stride["ci_lo"], "ci_hi": stride["ci_hi"],
                    "n_eff": stride["n_eff"], "clears": bool(stride["clears"]),
                    "block_clears": bool(block["clears"]), "block_rate": block["rate"],
                    "placebo": placebo,
                    "beats_placebo": bool(np.isnan(placebo) or stride["rate"] > placebo),
                    "halves_flips": bool(halves["flips"]),
                }
            out[(zone, bias)] = cell
    return out


# =============================================================================
# 8-WAY MULTIPLICITY PENALTY (deflated max-stat over the directional family)
# =============================================================================
def penalty_8way(cells, eligible=None, n_cells=N_CELLS_DIRECTIONAL):
    """Deflated max-stat penalty over the 8 directional rates (PREREG-0B). The E[max]
    threshold is over the FULL declared family (multiplicity = n_cells). The winning rate's
    stride CI lower bound must clear BOTH 0.5+2pp AND e_max.

    AUDIT F1: the variance / e_max and the Bonferroni SE use the **floor n** (`n_floor` =
    floor(N_scored/fwdK), the n-floor gate basis PREREG-0B's Estimator PIN requires), NOT
    stride_rate_ci's inflated greedy-kept count (which would deflate e_max -> false-positive
    PASS). The winner's CI lower bound stays the stride ci_lo (the legit de-overlapped CI),
    mirroring harness_1h.deflated_max_stat_penalty exactly.

    AUDIT F2: `eligible` (a set of (zone,bias,direction) keys) restricts the WINNER to the
    fully-clearing candidate cells, so a high-rate block-failing non-candidate cannot steal
    the verdict-bearing slot. e_max is still over the full family (the multiplicity is what
    you LOOKED at, not what cleared). eligible=None -> winner over all (standalone use)."""
    from scipy.stats import norm
    entries = []
    for (zone, bias), c in cells.items():
        for direction in ("rev", "cont"):
            d = c[direction]
            entries.append({"zone": zone, "bias": bias, "direction": direction,
                            "rate": d.get("rate", np.nan), "ci_lo": d.get("ci_lo", np.nan),
                            "n_floor": c.get("n_floor", 0)})
    valid = [e for e in entries if e["n_floor"] >= 1 and not np.isnan(e["rate"])]
    if not valid:
        return {"winner": None, "pass_dsr": False, "pass_bonf": False, "e_max": np.nan}
    n_floor_arr = np.array([max(e["n_floor"], 1) for e in valid], float)   # FLOOR basis (F1)
    var_cell = np.mean(0.25 / n_floor_arr)
    N = n_cells
    e_max = 0.5 + np.sqrt(var_cell) * (
        (1 - H.GAMMA) * norm.ppf(1 - 1.0 / N) + H.GAMMA * norm.ppf(1 - 1.0 / (N * np.e)))
    pool = valid if eligible is None else [
        e for e in valid if (e["zone"], e["bias"], e["direction"]) in eligible]    # F2
    if not pool:
        return {"winner": None, "pass_dsr": False, "pass_bonf": False, "e_max": float(e_max)}
    winner = max(pool, key=lambda e: e["rate"])
    w_lo = winner["ci_lo"]
    pass_dsr = (not np.isnan(w_lo)) and (w_lo > 0.5 + H.MARGIN_PP) and (w_lo > e_max)
    alpha_b = 0.05 / N
    z_b = norm.ppf(1 - alpha_b / 2.0)
    w_rate, w_nf = winner["rate"], max(winner["n_floor"], 1)
    se_b = np.sqrt(max(w_rate * (1 - w_rate), 1e-12) / w_nf)
    lo_b = w_rate - z_b * se_b
    return {"winner": winner, "pass_dsr": bool(pass_dsr),
            "pass_bonf": bool(lo_b > 0.5 + H.MARGIN_PP), "e_max": float(e_max)}


# =============================================================================
# PLACEBO (bias-bucket-local regression-to-range floor)
# =============================================================================
def bucket_fwd_floor(close, mask, down, fwd_k=FWDK):
    """Regression-to-range / drift floor: the UNCONDITIONAL rate of the forward direction
    (down if `down` else up, over fwd_k bars) among the scorable bars in `mask` (the bias
    bucket). A zone's bias-conditioned directional rate must EXCEED this to be signal BEYOND
    the bucket's own directional drift (e.g. in a bull bucket up-moves are ~baseline, so a
    discount->up cell must beat that baseline, not 0.5).

    RE-AUDIT P-1 fix: replaces the base-rate-DEFLATED placebo_random_eq (which returned
    real_rate*base_freq and was a near-no-op `beats_placebo`). This floor is the correct,
    drift-controlling regression-to-range comparator -- and O(n), not a bootstrap."""
    close = np.asarray(close, float)
    mask = np.asarray(mask, bool)
    n = len(close)
    if n <= fwd_k:
        return np.nan
    fwd = (close[fwd_k:] < close[:-fwd_k]) if down else (close[fwd_k:] > close[:-fwd_k])
    m = mask[:n - fwd_k]
    denom = int(np.sum(m))
    return float(np.sum(fwd & m) / denom) if denom else np.nan


# =============================================================================
# VERDICT (PREREG-0B sec-6 discriminator gate)
# =============================================================================
def verdict_0b(ex: H.HourExport, structbias):
    """Full PREREG-0B sec-6 verdict on a single out-of-sample regime page. The gate logic is
    pure over the cells dict (all per-cell evidence computed in cell_rates)."""
    cells = cell_rates(ex, structbias)
    out = {"cells": cells}
    floors = [c["n_floor"] for c in cells.values()]
    if not floors or max(floors) < H.N_FLOOR:
        out["verdict"] = "INSUFFICIENT-N"
        out["reason"] = (f"every (zone x bias) cell below n-floor {H.N_FLOOR} "
                         f"(max={max(floors) if floors else 0}); re-spec a longer page")
        return out

    # full candidates: powered cell, direction clearing stride AND block CIs, beats placebo,
    # halves-stable. any_stride_clear tracks whether ANY direction clears the stride CI (the
    # FALSIFIED straddle test, per harness_1h.verdict_1h: FALSIFIED iff nothing clears stride).
    candidates = []
    any_stride_clear = False
    for (zone, bias), c in cells.items():
        for direction in ("rev", "cont"):
            d = c[direction]
            if d["clears"]:
                any_stride_clear = True   # over ALL cells incl. STARVED (re-audit F4-1): a
                #                           starved clearer must HOLD (AMBIGUOUS), not FALSIFY
            if (c["n_floor"] >= H.N_FLOOR and d["clears"] and d["block_clears"]
                    and d["beats_placebo"] and not d["halves_flips"]):
                candidates.append({"zone": zone, "bias": bias, "direction": direction,
                                   "rate": d["rate"]})
    elig = {(c["zone"], c["bias"], c["direction"]) for c in candidates}
    pen = penalty_8way(cells, eligible=elig)   # F2: winner among candidates; e_max over all 8
    out["penalty"] = pen
    out["candidates"] = candidates

    # RESOLVED: the best CANDIDATE (penalty winner restricted to candidates) passes the
    # floor-n penalty. (placebo/block/halves already gated candidacy.)
    if candidates and pen.get("winner") is not None and pen["pass_dsr"]:
        out["verdict"] = "RESOLVED"
        out["winner"] = pen["winner"]
        out["reason"] = ("a bias-conditioned directional cell clears 0.5 by >=2pp (stride+"
                         "block), beats its placebo, survives the 8-way (floor-n) penalty, "
                         "n_floor>=30, and is halves-stable -> escalate to the FULL multi-regime panel")
        return out

    # FALSIFIED only when NO cell clears the stride CI in any direction (all straddle 0.5) --
    # the clean falsification. A stride-clears/block-fails (or penalty-failing) near-miss is
    # NOT a clean falsification (AUDIT F4; matches harness_1h.verdict_1h's disposition).
    if not any_stride_clear:
        out["verdict"] = "FALSIFIED"
        out["reason"] = ("no adequately-powered (zone x bias) cell clears the stride CI in any "
                         "direction (all straddle 0.5) -> the bias partition carries no "
                         "out-of-sample edge; the 1H layer has no stable conditional edge "
                         "(forward-watch belt)")
        return out

    out["verdict"] = "AMBIGUOUS"
    out["reason"] = ("a cell cleared the stride CI but failed the block cross-check / placebo / "
                     "halves / 8-way penalty -> HOLD (near-miss, not a clean falsification); "
                     "name the re-test object (longer or additional-regime page)")
    return out


# =============================================================================
# ORCHESTRATOR (skip-clean; confirmatory)
# =============================================================================
def _fmt(x):
    return "  nan" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.4f}"


def run_0b(bar_paths, weekly_gatebias_csv=None, ema_len=20):
    """Run the CONFIRMATORY 0b discriminator on BAR_EXPORT page(s). structBias is offline
    (faithful gate definition); pass weekly_gatebias_csv to override with a real weekly
    `gateBias`/`vStruct` export (time,gateBias) joined with the [1]-lag instead."""
    paths = [bar_paths] if isinstance(bar_paths, (str, Path)) else list(bar_paths)
    missing = [p for p in paths if not Path(p).exists()]
    if missing:
        print(f"[SKIP] BAR_EXPORT page(s) not found: {missing}")
        print("       Phase 0b needs an OUT-OF-SAMPLE bear/chop BAR_EXPORT page (PREREG-0B).")
        return None
    df = load_bar_pages(paths)
    ex = hour_export_from_ohlc(df)
    if weekly_gatebias_csv and Path(weekly_gatebias_csv).exists():
        structbias = load_weekly_gatebias(weekly_gatebias_csv)   # sorted+deduped+[1]-lagged
        src = f"weekly gateBias export ({Path(weekly_gatebias_csv).name}, [1]-lagged)"
    else:
        structbias = structbias_offline(ex.epoch_ms, ex.c, ema_len)
        src = f"offline close-vs-weeklyEMA{ema_len} ([1]-lagged, faithful gate definition)"
    res = verdict_0b(ex, structbias)
    res["_meta"] = {"n_bars": ex.n, "structbias_source": src,
                    "window": (pd.to_datetime(int(ex.epoch_ms[0]), unit="ms", utc=True),
                               pd.to_datetime(int(ex.epoch_ms[-1]), unit="ms", utc=True))}
    print_report_0b(res)
    return res


def print_report_0b(res):
    m = res.get("_meta", {})
    print("=" * 76)
    print("Q-ICT-1H-REVCON-1 / Phase 0b -- CONFIRMATORY bias-conditioned discriminator")
    print("=" * 76)
    if m:
        print(f"bars: {m['n_bars']}  window: {m['window'][0]} -> {m['window'][1]}")
        print(f"structBias: {m['structbias_source']}")
    for (zone, bias), c in res["cells"].items():
        print(f"  {zone}|bias{bias:+d}: rev={_fmt(c['rev']['rate'])} "
              f"(clr={c['rev']['clears']}) cont={_fmt(c['cont']['rate'])} "
              f"(clr={c['cont']['clears']}) n_floor={c['n_floor']}"
              f"{'  STARVED' if c['n_floor'] < H.N_FLOOR else ''}")
    pen = res.get("penalty")
    if pen and pen.get("winner"):
        w = pen["winner"]
        print(f"  penalty winner: {w['zone']}|bias{w['bias']:+d} {w['direction']} "
              f"rate={_fmt(w['rate'])} e_max={_fmt(pen['e_max'])} pass_dsr={pen['pass_dsr']}")
    print("-" * 76)
    print(f"VERDICT: {res['verdict']}")
    print(f"  {res['reason']}")
    print("=" * 76)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Q-ICT-1H-REVCON-1 Phase 0b discriminator")
    ap.add_argument("--bar", action="append", default=[], help="BAR_EXPORT page CSV (repeatable)")
    ap.add_argument("--weekly-gatebias", default=None, help="optional weekly gateBias export")
    ap.add_argument("--ema-len", type=int, default=20)
    args = ap.parse_args()
    if not args.bar:
        print("[SKIP] pass at least one --bar <BAR_EXPORT page CSV>")
    else:
        run_0b(args.bar, weekly_gatebias_csv=args.weekly_gatebias, ema_len=args.ema_len)
