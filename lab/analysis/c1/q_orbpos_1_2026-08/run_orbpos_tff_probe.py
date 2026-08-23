#!/usr/bin/env python3
"""Q-ORBPOS-1 Phase 1-2 -- CFTC TFF Leveraged-Funds positioning-extremity classifier
vs ORB-MNQ-1's cushion-sizing gate-clearance check.

IMPLEMENTATION A -- independent from-scratch build against the frozen pre-reg:
  docs/briefs/pre-registration/2026-08-22-orbcush-1-tff-positioning-mechanism-prereg.md
Phase 0 contingency resolution (read first, per the task instructions):
  lab/analysis/c1/q_orbpos_1_2026-08/RESULTS.md

Reused UNCHANGED, per the task's own explicit instruction ("this repo's EXISTING,
already-cited harness code for the UNRELATED, already-verified gate-clearance
check"): day_loop_intraday / build_paths_orb / run_policy_orb / pol_cushion /
pol_const (+ build_k_panel / blocks_from_panel / resolve_panel / make_inst /
orb_days_with_excursion / assert_mirror_matches_engine / load_scoring_thresholds /
firm_kwargs / assert_engine_ready), imported from
_imported_run_evalseq_orb_intraday.py -- a byte-for-byte copy of
lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py
with exactly ONE line changed (a stale absolute path to a since-deleted worktree,
corrected to this worktree -- see that file's own header note; nothing algorithmic
touched).

Everything else in THIS file -- the CFTC TFF pull, the standalone-MNQ-line live
re-confirmation, the %OI net-position derivation + cross-check, the
publication-lag-respecting causal day-mapping, the trailing-window +
expanding-causal-median EXTREMITY classifier, and the per-bucket contiguous-run
block construction feeding the reused gate-clearance harness -- is this
implementation's own independent build, written from the frozen pre-reg's own text
without having seen any other session's implementation of this exact question.

$0 / K=0 per pre-reg Sec8. Writes only to this directory. Live network pull
(cftc.gov Socrata public API, free, no key) happens exactly once per run.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import _imported_run_evalseq_orb_intraday as H  # noqa: E402  (harness, imported unchanged bar one path)

CUTOFF = pd.Timestamp("2021-09-28")
MNQ_LAUNCH = pd.Timestamp("2019-05-06")
PANEL_END = pd.Timestamp("2026-07-15")  # ORB-MNQ-1's own price-panel end (pre-reg Sec7 Phase 1 / RESULTS.md)

# CFTC Socrata "Traders in Financial Futures - Futures Only" dataset (free, no key).
# MNQ = standalone "MICRO E-MINI NASDAQ-100 INDEX" reportable line, code 209747 --
# Phase 0 RESULTS.md item 1; re-confirmed LIVE below (independent of that file's
# prose) before any position value is read, per the pre-reg's own order-of-
# operations discipline (Sec4).
TFF_DATASET = "https://publicreporting.cftc.gov/resource/gpe5-46if.json"
MNQ_CFTC_CODE = "209747"

WINDOWS = {"W1": 4, "W2": 13, "W3": 26}  # TFF weekly observations, pre-reg Sec2.3
DATE_CORR_HIGH_FLOOR = 0.75
DATE_CORR_LOW_CEIL = 0.40
MIN_W1_PREBREAK_PRINTS = 4  # Sec4 Ambiguous-hold sparsity trigger, item 1
K = 1

FIELDS = [
    "report_date_as_yyyy_mm_dd", "open_interest_all",
    "lev_money_positions_long", "lev_money_positions_short",
    "pct_of_oi_lev_money_long", "pct_of_oi_lev_money_short",
    "asset_mgr_positions_long", "asset_mgr_positions_short",
    "pct_of_oi_asset_mgr_long", "pct_of_oi_asset_mgr_short",
    "traders_lev_money_long_all", "traders_lev_money_short_all",
    "traders_tot_all", "futonly_or_combined",
]


# ============================================================================
# Phase 1 -- CFTC TFF pull (own independent build)
# ============================================================================

def fetch_json(params: dict) -> list:
    r = requests.get(TFF_DATASET, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def confirm_mnq_standalone_line() -> dict:
    """Live re-confirmation (at pull time, before any position value is read)
    that MNQ is its own standalone TFF reportable line, distinct from NQ --
    independently re-derives Phase 0 RESULTS.md item 1 rather than trusting that
    file's prose. Report-structure-only query (distinct market/contract names +
    codes) -- no position value in this call."""
    rows = fetch_json({
        "$select": "distinct market_and_exchange_names,contract_market_name,cftc_contract_market_code",
        "$where": "upper(market_and_exchange_names) like '%NASDAQ%'",
        "$limit": 100,
    })
    codes = {}
    for r in rows:
        c = r["cftc_contract_market_code"].strip()
        codes.setdefault(c, r["contract_market_name"])
    assert MNQ_CFTC_CODE in codes, f"MNQ code {MNQ_CFTC_CODE} not found among live NASDAQ-family codes: {codes}"
    assert "MICRO" in codes[MNQ_CFTC_CODE].upper(), f"code {MNQ_CFTC_CODE} is not the Micro line: {codes[MNQ_CFTC_CODE]!r}"
    other_lines = {c: n for c, n in codes.items() if c != MNQ_CFTC_CODE}
    return dict(mnq_code=MNQ_CFTC_CODE, mnq_name=codes[MNQ_CFTC_CODE], other_nasdaq_family_lines=other_lines)


def pull_mnq_tff() -> pd.DataFrame:
    rows = fetch_json({
        "$where": f"cftc_contract_market_code='{MNQ_CFTC_CODE}'",
        "$select": ",".join(FIELDS),
        "$order": "report_date_as_yyyy_mm_dd asc",
        "$limit": 50000,
    })
    if not rows:
        raise RuntimeError("empty TFF pull for MNQ code " + MNQ_CFTC_CODE)
    df = pd.DataFrame(rows)
    assert (df["futonly_or_combined"] == "FutOnly").all(), "unexpected combined-report rows in pull"
    df["report_date"] = pd.to_datetime(df["report_date_as_yyyy_mm_dd"]).dt.normalize()
    numeric_cols = [c for c in FIELDS if c not in ("report_date_as_yyyy_mm_dd", "futonly_or_combined")]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c])
    df = df.sort_values("report_date").reset_index(drop=True)
    assert df["report_date"].is_unique, "duplicate TFF report_date rows"
    return df


def add_publication_lag(df: pd.DataFrame) -> pd.DataFrame:
    """Friday-of-report-week publication convention (Phase 0 RESULTS.md item 4,
    CFTC's own 'About the COT Reports' page): weekly TFF reports reflecting a
    Tuesday snapshot are released the FOLLOWING Friday ~3:30pm ET.
    available_date = the Friday on/after report_date. This is a conservative
    approximation for the rare Friday-holiday case (true publication shifts to
    Thursday, one day EARLIER) -- it is never anticipatory (never claims a print
    is available before it truly was), only possibly one day late in that one
    edge case, which is the safe direction for a causal classifier."""
    df = df.copy()
    dow = df["report_date"].dt.weekday  # Mon=0 ... Fri=4
    days_to_fri = (4 - dow) % 7
    df["available_date"] = df["report_date"] + pd.to_timedelta(days_to_fri, unit="D")
    return df


def build_extremity_series(df: pd.DataFrame) -> pd.DataFrame:
    """Primary classifier input: Leveraged Funds NET position as %OI, from the
    directly-published Pct_of_OI_Lev_Money_Long/Short fields (Phase 0 RESULTS.md
    item 3), never derived-then-substituted. `extremity_lf` = |net %OI| -- the
    sign-agnostic crowding measure the pre-reg's Sec2.1 specifies (H-ORBPOS
    predicts no price direction; only whether the MAGNITUDE of one-sided LF
    positioning date-correlates with the break)."""
    df = df.copy()
    df["net_pct_oi_lf"] = df["pct_of_oi_lev_money_long"] - df["pct_of_oi_lev_money_short"]
    # Cross-check (Phase 0 RESULTS.md item 3's own suggested "cheap and worth
    # doing" check): the published %OI fields should numerically equal the
    # raw-contract-derived ratio to within rounding (published fields are
    # rounded to 1 decimal place independently for long and short).
    df["net_pct_oi_lf_derived"] = (
        (df["lev_money_positions_long"] - df["lev_money_positions_short"]) / df["open_interest_all"] * 100.0
    )
    df["net_pct_oi_crosscheck_delta"] = (df["net_pct_oi_lf"] - df["net_pct_oi_lf_derived"]).abs()
    df["extremity_lf"] = df["net_pct_oi_lf"].abs()
    return df


# ============================================================================
# Phase 2a -- trailing causal classifier (own independent build)
# ============================================================================

def build_classifier(df: pd.DataFrame, window: int) -> dict:
    """Trailing, causal |net %OI| extremity classifier at TFF's own weekly
    cadence.

    roll_W[i]  = mean(extremity[i-W+1 .. i])   (rolling window ENDING AT, and
                 INCLUDING, print i -- print i's own value becomes causally
                 usable for print i's own classification once i is published;
                 unlike the prior mean-R round's own-trade R, TFF positioning is
                 an EXTERNAL state variable, not the strategy's own realized
                 outcome, so there is no self-referential-outcome reason to
                 exclude print i via an extra shift(1) here. This is the one
                 deliberate departure from the mean-R round's literal mechanic,
                 made explicit per the task's own auditability requirement.)

    threshold[i] = expanding median of roll_W[0..i]  (causal, never a
                 full-sample/global-percentile statistic) -- the same
                 `.expanding(min_periods=1).median()` mechanic the mean-R round
                 used, applied here to the rolled EXTREMITY series.

    label[i] = HIGHER if roll_W[i] > threshold[i] else LOWER (only where roll_W
                 is valid; WARMUP for the first W-1 prints, which have no full
                 trailing window yet).
    """
    extremity = df["extremity_lf"]
    roll_W = extremity.rolling(window, min_periods=window).mean()
    running_median = roll_W.expanding(min_periods=1).median()
    valid = roll_W.notna()

    label = pd.Series("WARMUP", index=df.index)
    label[valid & (roll_W > running_median)] = "HIGHER"
    label[valid & (roll_W <= running_median)] = "LOWER"

    # Independent (plain-python, not pandas) spot-check of the expanding median,
    # same discipline the mean-R round used, to catch a pandas NaN-handling
    # surprise before trusting it.
    valid_pos = np.flatnonzero(valid.to_numpy())
    spot_pos = valid_pos[:: max(1, len(valid_pos) // 5)][:5] if len(valid_pos) else np.array([], dtype=int)
    spot_ok = True
    for pos in spot_pos:
        seen = roll_W.to_numpy()[: pos + 1]
        seen_valid = seen[~np.isnan(seen)]
        expect = float(np.median(seen_valid))
        got = float(running_median.iloc[pos])
        if not np.isclose(expect, got, rtol=1e-9, atol=1e-9):
            spot_ok = False

    valid_medians = running_median[valid].to_numpy()
    degenerate = bool(len(valid_medians) > 0 and float(np.nanstd(valid_medians)) == 0.0)

    return dict(
        window=window, roll_W=roll_W, running_median=running_median, label=label, valid=valid,
        spotcheck_pass=bool(spot_ok), n_spot_checked=int(len(spot_pos)),
        n_warmup=int((label == "WARMUP").sum()), n_higher=int((label == "HIGHER").sum()),
        n_lower=int((label == "LOWER").sum()), degenerate_threshold=degenerate,
    )


def daily_label_from_weekly(df: pd.DataFrame, label: pd.Series, full_idx: pd.DatetimeIndex) -> pd.Series:
    """Causal day-mapping: day D on ORB-MNQ-1's own business-day panel inherits
    the label of the LATEST TFF print whose available_date (publication Friday,
    not the Tuesday snapshot date) is <= D. Days before the first available print
    are WARMUP (no classification yet exists)."""
    weekly = pd.Series(label.to_numpy(), index=pd.DatetimeIndex(df["available_date"]))
    weekly = weekly[~weekly.index.duplicated(keep="last")].sort_index()
    union_idx = weekly.index.union(full_idx)
    daily = weekly.reindex(union_idx).ffill().reindex(full_idx)
    daily = daily.fillna("WARMUP")
    return daily


def date_correlation(daily_label: pd.Series) -> dict:
    idx_higher = daily_label.index[daily_label == "HIGHER"]
    idx_lower = daily_label.index[daily_label == "LOWER"]
    frac_higher_post = float((idx_higher >= CUTOFF).mean()) if len(idx_higher) else float("nan")
    frac_lower_post = float((idx_lower >= CUTOFF).mean()) if len(idx_lower) else float("nan")
    ok = bool(
        len(idx_higher) > 0 and len(idx_lower) > 0
        and (frac_higher_post >= DATE_CORR_HIGH_FLOOR) and (frac_lower_post <= DATE_CORR_LOW_CEIL)
    )
    return dict(
        n_higher_days=int(len(idx_higher)), n_lower_days=int(len(idx_lower)),
        frac_higher_days_post_cutoff=frac_higher_post, frac_lower_days_post_cutoff=frac_lower_post,
        date_corr_pass=ok,
    )


# ============================================================================
# Phase 2b -- per-bucket block construction + gate-clearance check
# (own independent build; adapter forced by H.blocks_from_panel's own contract,
#  which requires a contiguous Monday-anchored business-day panel slice)
# ============================================================================

def contiguous_runs(mask: np.ndarray):
    n = len(mask)
    i = 0
    while i < n:
        if not mask[i]:
            i += 1
            continue
        j = i
        while j < n and mask[j]:
            j += 1
        yield i, j
        i = j


def blocks_for_label(panel_full: pd.DataFrame, daily_label: pd.Series, want: str):
    lab = daily_label.reindex(panel_full.index)
    mask = (lab == want).to_numpy()
    pnl_parts, low_parts = [], []
    n_runs_used = n_runs_skipped = n_days_used = 0
    for i0, i1 in contiguous_runs(mask):
        sub = panel_full.iloc[i0:i1]
        try:
            bp, bl = H.blocks_from_panel(sub)
        except ValueError:
            n_runs_skipped += 1
            continue
        pnl_parts.append(bp)
        low_parts.append(bl)
        n_runs_used += 1
        n_days_used += (i1 - i0)
    if not pnl_parts:
        raise ValueError(f"no usable Monday-anchored 5-day blocks for label={want}")
    bpnl = np.concatenate(pnl_parts, axis=0)
    blow = np.concatenate(low_parts, axis=0)
    return bpnl, blow, dict(
        n_days_in_label=int(mask.sum()), n_days_in_blocks=n_days_used,
        n_runs_used=n_runs_used, n_runs_skipped=n_runs_skipped, n_blocks=len(bpnl),
    )


def gate_check_bucket(panel_full: pd.DataFrame, daily_label: pd.Series, want: str, thr, fkw) -> dict:
    bpnl, blow, meta = blocks_for_label(panel_full, daily_label, want)
    flat = H.run_policy_orb(bpnl, blow, H.pol_const(1.0), use_intraday=True,
                             horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
    cush = H.run_policy_orb(bpnl, blow, H.pol_cushion, use_intraday=True,
                             horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)

    def gate(bust_pct, pass_pct):
        return bool(bust_pct <= thr.eval_bust_ceiling * 100.0 and pass_pct >= thr.pass_floor * 100.0)

    return dict(
        meta=meta,
        flat=dict(bust_pct=flat["bust_pct"], pass_pct=flat["pass_pct"], gate_pass=gate(flat["bust_pct"], flat["pass_pct"])),
        cushion=dict(bust_pct=cush["bust_pct"], pass_pct=cush["pass_pct"], gate_pass=gate(cush["bust_pct"], cush["pass_pct"])),
    )


def classify_direction(gate_higher: dict, gate_lower: dict) -> str:
    hc = gate_higher["cushion"]["gate_pass"]
    lc = gate_lower["cushion"]["gate_pass"]
    if hc and not lc:
        return "HIGHER_CLEARS_LOWER_DOES_NOT"
    if lc and not hc:
        return "LOWER_CLEARS_HIGHER_DOES_NOT"
    if hc and lc:
        return "BOTH_CLEAR"
    return "NEITHER_CLEARS"


# ============================================================================
# main
# ============================================================================

def main():
    t0 = time.time()
    report: dict = {"cutoff": str(CUTOFF.date()), "K": K, "windows_tff_prints": WINDOWS,
                     "min_w1_prebreak_prints_floor": MIN_W1_PREBREAK_PRINTS}

    print("=" * 100)
    print("Q-ORBPOS-1 IMPLEMENTATION A -- CFTC TFF Leveraged-Funds positioning-extremity classifier")
    print("=" * 100)

    # ---------------------------------------------------------------- Phase 0 re-confirm (live)
    print("\n--- live re-confirmation: MNQ standalone TFF line (Phase 0 RESULTS.md item 1) ---")
    line_check = confirm_mnq_standalone_line()
    print(f"  MNQ code={line_check['mnq_code']}  name={line_check['mnq_name']!r}")
    print(f"  other NASDAQ-family lines (distinct codes): {line_check['other_nasdaq_family_lines']}")
    report["mnq_standalone_line_check"] = line_check

    # ---------------------------------------------------------------- Phase 1 pull
    print("\n--- Phase 1: CFTC TFF pull (Socrata, free, no key) ---")
    tff = pull_mnq_tff()
    tff = add_publication_lag(tff)
    tff = build_extremity_series(tff)
    print(f"  dataset: {TFF_DATASET}  where cftc_contract_market_code='{MNQ_CFTC_CODE}'")
    print(f"  n_rows={len(tff)}  first report_date={tff['report_date'].min().date()}  "
          f"last report_date={tff['report_date'].max().date()}")
    print(f"  MNQ launch (pre-reg): {MNQ_LAUNCH.date()}  first usable TFF print: {tff['report_date'].min().date()}  "
          f"(gap: category not yet broken out at launch -- Phase 0's own caveat)")
    max_crosscheck_delta = float(tff["net_pct_oi_crosscheck_delta"].max())
    print(f"  %OI derived-vs-published cross-check: max |delta|={max_crosscheck_delta:.3f}pp "
          f"({'OK, within 1-decimal rounding' if max_crosscheck_delta < 0.15 else 'CHECK -- larger than expected'})")
    report["pull"] = dict(
        n_rows=len(tff), first_report_date=str(tff["report_date"].min().date()),
        last_report_date=str(tff["report_date"].max().date()),
        mnq_launch=str(MNQ_LAUNCH.date()), max_crosscheck_delta_pp=max_crosscheck_delta,
    )

    n_prebreak_prints = int((tff["available_date"] < CUTOFF).sum())
    print(f"\n  independent published TFF prints available BEFORE the {CUTOFF.date()} break: {n_prebreak_prints}")
    report["n_prebreak_published_prints"] = n_prebreak_prints
    sparsity_trigger_1 = n_prebreak_prints < MIN_W1_PREBREAK_PRINTS
    print(f"  Sec4 Ambiguous-hold trigger 1 (W1 sparsity, floor={MIN_W1_PREBREAK_PRINTS}): "
          f"{'FIRES' if sparsity_trigger_1 else 'does not fire'}")
    report["ambiguous_hold_trigger_1_prebreak_sparsity"] = bool(sparsity_trigger_1)

    # ---------------------------------------------------------------- data + Control B mirror (reused harness)
    print("\n--- ORB-MNQ-1 own panel + Control B mirror (harness reused unchanged) ---")
    inst = H.make_inst()
    panel_pkl = H.resolve_panel()
    df_panel = pd.read_pickle(panel_pkl)
    print(f"  panel: {panel_pkl}")
    print(f"  rows={len(df_panel):,}  span={df_panel['et'].min()} -> {df_panel['et'].max()}")

    piv, meta = H.ol.session_panel(df_panel, inst)
    bt = H.ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = H.orb_days_with_excursion(piv, meta, inst, entry_bar="include")
    H.assert_mirror_matches_engine(recon, bt)
    print(f"  Control B PASS -- n={len(recon)} triggering days  "
          f"recon date span {recon['date'].min().date()} -> {recon['date'].max().date()}")
    report["n_triggering_days"] = len(recon)

    thr = H.load_scoring_thresholds()
    print(f"\n[gate ] {thr.source_path}")
    print(f"[gate ] horizon={thr.horizon}  seeds={thr.seeds}  sims/seed={thr.sims_per_seed}  "
          f"eval_bust_ceiling={thr.eval_bust_ceiling:.1%}  pass_floor={thr.pass_floor:.0%}")
    report["gate_thresholds"] = dict(eval_bust_ceiling_pct=thr.eval_bust_ceiling * 100.0,
                                      pass_floor_pct=thr.pass_floor * 100.0, horizon=thr.horizon,
                                      seeds=list(thr.seeds), sims_per_seed=thr.sims_per_seed)

    H.assert_engine_ready(H.TIER)
    fkw_base = H.firm_kwargs(H.TIER, inactivity_off=True, consistency=H.CONSISTENCY_FRAC)
    if fkw_base["dd_lock_offset_usd"] == H.LOCK_AS_PUBLISHED:
        fkw = dict(fkw_base, dd_lock_offset_usd=H.LOCK_UNREACHABLE)
        print("[firm ] FIRM_RULES still ships the as-published lock; overriding to unreachable (matches published headline).")
    else:
        fkw = dict(fkw_base)
        print(f"[firm ] FIRM_RULES already ships dd_lock_offset_usd={fkw_base['dd_lock_offset_usd']:,.0f} (no override needed).")
    assert fkw["profit_target"] == H.TARGET
    assert fkw["starting_equity"] == H.START
    assert fkw["trailing_dd_pct"] == -H.DD / H.START

    # ---------------------------------------------------------------- fidelity control (reused harness)
    print("\n--- FIDELITY CONTROL: flat policy, m=1.0, full panel, k=1/k=2 (reused day_loop_intraday) ---")
    PUBLISHED = {1: 67.67, 2: 77.01}
    TOL_PP = 2.0
    control = {}
    flat_ok_k1 = True
    for k in (1, 2):
        panel_full_k = H.build_k_panel(recon, k)
        bpnl, blow = H.blocks_from_panel(panel_full_k)
        r = H.run_policy_orb(bpnl, blow, H.pol_const(1.0), use_intraday=True,
                              horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
        delta = r["bust_pct"] - PUBLISHED[k]
        ok = abs(delta) <= TOL_PP
        if k == 1:
            flat_ok_k1 = ok
        control[k] = dict(bust_pct=r["bust_pct"], pass_pct=r["pass_pct"], published=PUBLISHED[k],
                           delta_pp=delta, within_tol=ok)
        print(f"  k={k}  bust={r['bust_pct']:.2f}%  pass={r['pass_pct']:.2f}%  published={PUBLISHED[k]:.2f}%  "
              f"delta={delta:+.2f}pp  {'PASS' if ok else 'FAIL'}  (elapsed {time.time()-t0:.0f}s)")
    report["fidelity_control"] = control
    report["fidelity_control_pass_k1"] = bool(flat_ok_k1)
    if not flat_ok_k1:
        print("\nSTOPPING -- fidelity control at k=1 did not reproduce the published intraday-honest bust "
              "rate within tolerance. Not proceeding to the TFF classifier on an unvalidated harness.")
        (HERE / "results_orbpos_tff_probe.json").write_text(json.dumps(report, indent=2, default=str))
        return 2

    # ---------------------------------------------------------------- Phase 2: classifier + gate, per window
    full_idx = pd.bdate_range(recon["date"].min(), recon["date"].max())
    panel_full_k1 = H.build_k_panel(recon, K)
    print(f"\n[panel] business-day span: {full_idx[0].date()} -> {full_idx[-1].date()}  n_days={len(full_idx)}")

    windows_report = {}
    for wname, wsize in WINDOWS.items():
        print("\n" + "=" * 100)
        print(f"{wname} -- rolling window = {wsize} TFF weekly prints")
        print("=" * 100)

        clf = build_classifier(tff, wsize)
        print(f"[classifier] n_prints_total={len(tff)}  WARMUP={clf['n_warmup']}  "
              f"HIGHER={clf['n_higher']}  LOWER={clf['n_lower']}  "
              f"expanding-median spot-check ({clf['n_spot_checked']} pts): "
              f"{'PASS' if clf['spotcheck_pass'] else 'FAIL'}  "
              f"degenerate-threshold: {'YES' if clf['degenerate_threshold'] else 'no'}")

        daily_label = daily_label_from_weekly(tff, clf["label"], full_idx)
        dc = date_correlation(daily_label)
        print(f"[date-corr] HIGHER bucket: n_days={dc['n_higher_days']}  "
              f"post-cutoff frac={dc['frac_higher_days_post_cutoff']:.1%}  (need >= {DATE_CORR_HIGH_FLOOR:.0%})")
        print(f"[date-corr] LOWER  bucket: n_days={dc['n_lower_days']}  "
              f"post-cutoff frac={dc['frac_lower_days_post_cutoff']:.1%}  (need <= {DATE_CORR_LOW_CEIL:.0%})")
        print(f"[date-corr] window condition: {'FIRES (pass)' if dc['date_corr_pass'] else 'does not fire (fail)'}")

        gate_higher = gate_check_bucket(panel_full_k1, daily_label, "HIGHER", thr, fkw)
        gate_lower = gate_check_bucket(panel_full_k1, daily_label, "LOWER", thr, fkw)
        print(f"[gate] HIGHER  n_blocks={gate_higher['meta']['n_blocks']}  "
              f"flat: bust={gate_higher['flat']['bust_pct']:.2f}% pass={gate_higher['flat']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_higher['flat']['gate_pass'] else 'FAIL'}  |  "
              f"cushion: bust={gate_higher['cushion']['bust_pct']:.2f}% pass={gate_higher['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_higher['cushion']['gate_pass'] else 'FAIL'}")
        print(f"[gate] LOWER   n_blocks={gate_lower['meta']['n_blocks']}  "
              f"flat: bust={gate_lower['flat']['bust_pct']:.2f}% pass={gate_lower['flat']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_lower['flat']['gate_pass'] else 'FAIL'}  |  "
              f"cushion: bust={gate_lower['cushion']['bust_pct']:.2f}% pass={gate_lower['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_lower['cushion']['gate_pass'] else 'FAIL'}   (elapsed {time.time()-t0:.0f}s)")

        direction = classify_direction(gate_higher, gate_lower)
        print(f"[direction] {wname}: {direction}")

        windows_report[wname] = dict(
            window_prints=wsize,
            classifier=dict(n_prints_total=len(tff), n_warmup=clf["n_warmup"], n_higher=clf["n_higher"],
                             n_lower=clf["n_lower"], spotcheck_pass=clf["spotcheck_pass"],
                             degenerate_threshold=clf["degenerate_threshold"]),
            date_correlation=dc,
            gate={"HIGHER": gate_higher, "LOWER": gate_lower},
            direction=direction,
        )

    report["windows"] = windows_report

    # ---------------------------------------------------------------- Phase 4-style verdict assertion
    n_date_corr_pass = sum(1 for w in windows_report.values() if w["date_correlation"]["date_corr_pass"])
    directions = [w["direction"] for w in windows_report.values()]
    signed_directions = {d for d in directions if d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT")}
    direction_same_sign_every_window = (
        len(signed_directions) == 1 and all(d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT") for d in directions)
    )
    any_w1_ambiguous = sparsity_trigger_1 or windows_report["W1"]["classifier"]["degenerate_threshold"]

    if any_w1_ambiguous:
        verdict = "AMBIGUOUS-HOLD"
    elif (n_date_corr_pass >= 2) and direction_same_sign_every_window:
        verdict = "ACCEPT (H-ORBPOS SUPPORTED)"
    else:
        verdict = "REJECT (H-ORBPOS REFUTED)"

    report["summary"] = dict(
        date_correlation_windows_passing=n_date_corr_pass,
        date_correlation_fires_at_ge2_of_3=bool(n_date_corr_pass >= 2),
        directions_by_window={wn: w["direction"] for wn, w in windows_report.items()},
        direction_same_sign_every_window=bool(direction_same_sign_every_window),
        w1_ambiguous_hold_fired=bool(any_w1_ambiguous),
        verdict=verdict,
    )

    print("\n" + "=" * 100)
    print("VERDICT ASSERTION (Sec4/Sec6)")
    print("=" * 100)
    print(f"  date-correlation clears (a)/(b) at >=2 of 3 windows?  {n_date_corr_pass}/3  -> "
          f"{'YES' if n_date_corr_pass >= 2 else 'NO'}")
    print(f"  gate-clearance direction same sign at every window, no exceptions?  "
          f"{'YES' if direction_same_sign_every_window else 'NO'}  (per-window: {report['summary']['directions_by_window']})")
    print(f"  Sec4 Ambiguous-hold (W1 sparsity or degenerate threshold)?  {'FIRES' if any_w1_ambiguous else 'does not fire'}")
    print(f"\n  ==> H-ORBPOS: {verdict}")

    out = HERE / "results_orbpos_tff_probe.json"
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
