"""Size-feasibility wrapper and opt-in sidecars (prereg 2026-10-08 §2.3, §6). Synthetic only."""
from __future__ import annotations

import csv
import dataclasses
import functools
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
import threading
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from discovery import prop_survivor_scoring as pss
from discovery.prop_survivor_scoring import TierSeries, load_scoring_thresholds, score_candidate

REPO = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "size_feasibility", REPO / "lab/analysis/c1/size_feasibility_2026-10/run_size_feasibility.py")
rsf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rsf)

THR = load_scoring_thresholds()
SMALL = dataclasses.replace(THR, sims_per_seed=8, horizon=60)
T = rsf.TRADEIFY
N = 60
TRIGGER = 0.01


# ── synthetic bundle ──────────────────────────────────────────────────────

def _channels(i: int, low: float | None) -> dict:
    rng = np.random.default_rng(11 + i)
    pnl = rng.normal(400.0, 900.0, N)
    lo = np.minimum(0.0, pnl) - 2500.0 if low is None else np.full(N, low)
    return {"normal_pnl": pnl, "normal_low": lo, "protected_pnl": pnl * 0.4, "protected_low": lo * 0.4}


def _bundle(root: Path, low: float | None = None) -> tuple[Path, str]:
    series = root / "series"
    series.mkdir(parents=True)
    outputs = {}
    for i, tier in enumerate(THR.tier_keys):
        ch = _channels(i, low)
        with (series / f"{tier}.csv").open("w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["date", *ch])
            for r in range(N):
                w.writerow([f"d{r}", *(repr(float(ch[c][r])) for c in ch)])
        outputs[f"{tier}.csv"] = {"sha256": rsf._sha(series / f"{tier}.csv")}
    gross = list(np.random.default_rng(3).normal(300.0, 500.0, N))
    (series / "manifest.json").write_text(json.dumps(
        {"n_days": N, "columns": {"normal": {"gross": gross}}, "outputs": outputs}))
    prep = {"series_manifest_sha256": rsf._sha(series / "manifest.json"),
            "full_res_trades": [200.0, -100.0] * 30, "envelope": "YES"}
    (root / "prep.json").write_text(json.dumps(prep))
    return root, rsf._sha(root / "prep.json")


def _load(path_sha, tiers=(T,)):
    return rsf.load_bundle(path_sha[0], tiers, prep_sha=path_sha[1])


def _score(bundle, d, k, pop="FULL", all_tiers=False):
    step = rsf.Step("x", k, pop, all_tiers)
    return rsf.score_call(bundle, d, k=k, pop=pop, all_tiers=all_tiers, thr=SMALL,
                          mode_trigger=TRIGGER, label=rsf.step_label(step))


def _inproc(path_sha, fail=()):
    def call(step, d, timeout):
        t0 = time.monotonic()
        try:
            b = _load(path_sha, THR.tier_keys if step.all_tiers else (T,))
            _score(b, d, step.k, step.pop, step.all_tiers)
            status = "failed" if step.name in fail else "ok"
        except Exception:  # noqa: BLE001 — a child crash is a failed run record
            status = "failed"
        return {"status": status, "cpu_seconds": time.monotonic() - t0}
    return call


# ── sidecars: opt-in, default bytes unchanged ─────────────────────────────

def _mapping(low=None):
    names = {"normal_pnl": "daily_pnl", "normal_low": "intraday_low", "protected_pnl": "protected_pnl",
             "protected_low": "protected_low"}
    return {t: TierSeries(**{names[k]: v for k, v in _channels(i, low).items()}) for i, t in enumerate(THR.tier_keys)}


def _kw(**over):
    kw = dict(strategy_label="synthetic", candidate_daily_pnl=np.full(N, 100.0),
              full_res_trades=[200.0, -100.0] * 30, envelope_verdict="YES", thresholds=SMALL,
              n_sims=SMALL.sims_per_seed, gross_edge_usd=1.0e9, tier_series=_mapping(), mode_trigger=TRIGGER)
    kw.update(over)
    return kw


def test_default_report_bytes_unchanged_with_sidecars_on_or_off():
    off = json.dumps(score_candidate(**_kw()).to_dict(), indent=2, default=str)
    side: dict = {}
    on = json.dumps(score_candidate(**_kw(), sidecar=side).to_dict(), indent=2, default=str)
    assert on == off
    assert set(side) == set(THR.tier_keys)
    for t, s in side.items():
        assert set(s["guard_arms"]) == {"eod", "zeros", "real"}, t
        assert set(s["days_to_pass"]) == {"run1", "run2"}, t


def test_guard_capture_equals_returned_arms_and_exists_when_guard_raises():
    blocks, lows = pss.paired_blocks_from_daily(_channels(0, None)["normal_pnl"], _channels(0, None)["normal_low"])
    cap: dict = {}
    ret = pss.assert_intraday_channel_nonvacuous(blocks, lows, thresholds=SMALL, firm_key=T, n_sims=8, capture=cap)
    assert cap == ret == pss.assert_intraday_channel_nonvacuous(blocks, lows, thresholds=SMALL, firm_key=T, n_sims=8)
    zero_cap: dict = {}
    with pytest.raises(AssertionError, match=rsf.VACUITY_TEXT):
        pss.assert_intraday_channel_nonvacuous(blocks, np.zeros_like(lows), thresholds=SMALL, firm_key=T,
                                               n_sims=8, capture=zero_cap)
    assert set(zero_cap) == {"eod", "zeros", "real"}


def test_days_to_pass_capture_and_median_equal_a_direct_computation():
    ch = _channels(0, None)
    blocks, lows = pss.paired_blocks_from_daily(ch["normal_pnl"] * 3, ch["normal_low"] * 0.1)
    cap: dict = {}
    ret = pss.run_tier_remc(T, blocks, SMALL, n_sims=8, intraday_blocks=lows, capture=cap)
    assert ret == pss.run_tier_remc(T, blocks, SMALL, n_sims=8, intraday_blocks=lows)
    kw = pss.firm_kwargs(T, inactivity_off=True, consistency=None)
    direct = [d for s in SMALL.seeds for d in pss.run_seed(
        s, 8, blocks, pss.NO_PROTECTION_TRIGGER, pss.DD_SCALE, horizon=SMALL.horizon,
        strats=pss.CANDIDATE_STRAT, firm_kwargs=kw, intraday_blocks=lows)["days_to_pass"]]
    assert cap == {"days_to_pass": direct, "n": 24}
    full = sorted(direct + [math.inf] * (24 - len(direct)))
    want = full[math.ceil(24 / 2) - 1]
    assert rsf.median_days_to_pass(direct, 24) == ("inf" if want == math.inf else want)
    assert rsf.median_days_to_pass([3, 1, 2], 4) == 2 and rsf.median_days_to_pass([3], 4) == "inf"


# ── series, populations, G1/G2 pin ────────────────────────────────────────

def test_scale_by_one_is_bit_equal_and_populations_are_ceil_partition(tmp_path):
    b = _load(_bundle(tmp_path))
    df = b["series"][T]
    s = rsf.scaled_series(df, 1.0, rsf.population(N, "FULL"))
    for got, col in zip((s.daily_pnl, s.intraday_low, s.protected_pnl, s.protected_low),
                        ("normal_pnl", "normal_low", "protected_pnl", "protected_low")):
        assert got.tobytes() == df[col].to_numpy().tobytes()
    half = rsf.scaled_series(df, 0.5, rsf.population(N, "H2"))
    assert half.daily_pnl.tobytes() == (df["normal_pnl"].to_numpy()[30:] * 0.5).tobytes()
    assert [rsf.population(7, p) for p in rsf.POPS] == [slice(0, 7), slice(0, 4), slice(4, 7)]
    assert rsf.population(1020, "H1") == slice(0, 510)


def test_g1g2_inputs_identical_bytes_in_every_call(tmp_path):
    ps = _bundle(tmp_path / "b")
    b = _load(ps)
    for k, pop in (("1.0", "FULL"), ("0.5", "H2"), ("0.2", "H1")):
        _score(b, tmp_path / f"{k}{pop}", k, pop)
    digests = {json.loads((tmp_path / f"{k}{p}" / "call.json").read_text())["g1g2_sha256"]
               for k, p in (("1.0", "FULL"), ("0.5", "H2"), ("0.2", "H1"))}
    assert digests == {rsf.g1g2_digest(rsf.g1g2_inputs(b))}


def test_tradeify_only_entry_equals_four_tier_entry(tmp_path):
    b = _load(_bundle(tmp_path / "b"), THR.tier_keys)
    _score(b, tmp_path / "all", "1.0", all_tiers=True)
    _score(b, tmp_path / "one", "1.0")
    a, o = rsf.read_call(tmp_path / "all"), rsf.read_call(tmp_path / "one")
    assert rsf._canon(a["report"]["tiers"][T]) == rsf._canon(o["report"]["tiers"][T])


# ── vacuity and zeros-check readings ──────────────────────────────────────

def _k1_calls(tmp_path, b):
    return {("1.0", p): (_score(b, tmp_path / f"k1{p}", "1.0", p), rsf.read_call(tmp_path / f"k1{p}"))[1]
            for p in rsf.POPS}


def test_vacuity_sidecar_present_and_k_reads_vacuity_read(tmp_path):
    good = _load(_bundle(tmp_path / "good"))
    vac = _load(_bundle(tmp_path / "vac", low=0.0))
    calls = _k1_calls(tmp_path, good)
    assert all(c["report"]["gate_grade"] for c in calls.values())
    for p in rsf.POPS:
        _score(vac, tmp_path / f"v{p}", "0.5", p)
        calls[("0.5", p)] = rsf.read_call(tmp_path / f"v{p}")
    rd = calls[("0.5", "FULL")]
    assert rd["report"]["gate_grade"] is False
    tier = rd["eod"]["tiers"][T]
    assert set(tier["guard_arms"]) == {"eod", "zeros", "real"}
    assert tier["gate_grade_reasons"] == rd["report"]["gate_grade_reasons"]
    assert rsf.VACUITY_TEXT in tier["gate_grade_reasons"][0]
    res = rsf.assess_k(calls, "0.5", SMALL, h2_pass_binding=False)
    assert res["status"] == "valid" and res["vacuity_read"] == list(rsf.POPS)
    # Without a k = 1 guard pass for that population the same call is INSUFFICIENT.
    calls[("1.0", "H1")] = None
    assert rsf.assess_k(calls, "0.5", SMALL, h2_pass_binding=False)["status"] == "insufficient"


def test_zeros_check_failure_reads_insufficient(tmp_path, monkeypatch):
    good = _load(_bundle(tmp_path / "good"))
    calls = _k1_calls(tmp_path, good)
    real = pss.run_seed

    @functools.wraps(real)  # keeps the kernel signature the mode-switching probe reads
    def skewed(*a, **kw):
        r = real(*a, **kw)
        lows = kw.get("intraday_blocks")
        if lows is not None and not np.any(lows):
            oc = dict(r["outcomes"])
            src = max(oc, key=oc.get)
            oc[src] -= 1
            oc["bust_trailing" if src == "pass" else "pass"] += 1
            r = {**r, "outcomes": oc}
        return r

    monkeypatch.setattr(pss, "run_seed", skewed)
    for p in rsf.POPS:
        _score(good, tmp_path / f"z{p}", "0.5", p)
        calls[("0.5", p)] = rsf.read_call(tmp_path / f"z{p}")
    reasons = calls[("0.5", "FULL")]["report"]["gate_grade_reasons"]
    assert len(reasons) == 1 and "zeros-channel must reproduce EOD" in reasons[0]
    assert (tmp_path / "zFULL" / "eod.json").exists()
    assert rsf.assess_k(calls, "0.5", SMALL, h2_pass_binding=False)["status"] == "insufficient"


# ── §6 labels (fabricated reads) ──────────────────────────────────────────

def _rec(ib, ip, eb, ep, *, gate=True, reasons=(), halted=None, gated="run2", g="G"):
    sha = "s" * 64
    arms = {r: {"n_sims": THR.sims_per_seed, "seeds": list(THR.seeds), "horizon": THR.horizon} for r in ("run1", "run2")}
    summ = lambda b, p: {"headline_bust": b, "pass_rate": p}  # noqa: E731
    return {"report": {"tiers": {T: {"gated_on": gated, "run2": summ(ib, ip)}}, "gate_grade": gate,
                       "gate_grade_reasons": list(reasons), "halted_at": halted, "breach_clock": "intraday_honest"},
            "report_sha256": sha, "depth": {"report_sha256": sha, "arms": {T: arms}},
            "eod": {"report_sha256": sha, "tiers": {T: {"guard_arms": {
                "eod": summ(eb, ep), "zeros": summ(eb, ep), "real": summ(ib, ip)}, "gate_grade_reasons": []}}},
            "median": {"report_sha256": sha, "tiers": {T: {r: {"n": THR.sims_per_seed * len(THR.seeds), "median": "inf"}
                                                            for r in ("run1", "run2")}}},
            "call": {"g1g2_sha256": g}}


FAIL = (0.30, 0.60, 0.30, 0.60)      # no clock bust-clear
EOD_BUST_ONLY = (0.30, 0.40, 0.03, 0.40)
CLEAR = (0.04, 0.60, 0.03, 0.60)


def _grid(default=FAIL, **by_k):
    return {(k, p): _rec(*by_k.get("k" + k.replace(".", "_"), default)) for k in rsf.GRID for p in rsf.POPS}


def _derive(calls, **kw):
    return rsf.derive_label(calls, THR, ref_g1g2="G", h2_pass_binding=kw.pop("h2", False), **kw)


def test_infeasible_when_every_k_fails_an_eod_bust_gate():
    assert _derive(_grid())["label"] == rsf.INFEASIBLE


def test_feasible_reports_every_clearing_k_and_the_largest():
    r = _derive(_grid(k0_5=CLEAR, k0_4=CLEAR))
    assert (r["label"], r["clearing_k"], r["largest_clearing_k"]) == (rsf.FEASIBLE, ["0.5", "0.4"], "0.5")


def test_clock_dependent_when_only_the_eod_clock_clears():
    assert _derive(_grid(k0_5=(0.20, 0.60, 0.03, 0.60)))["label"] == rsf.CLOCK_DEP


GAP = dict(k0_75=(0.30, 0.60, 0.20, 0.60), k0_5=EOD_BUST_ONLY, k0_4=EOD_BUST_ONLY,
           k0_33=(0.30, 0.60, 0.20, 0.60), k0_25=EOD_BUST_ONLY, k0_2=EOD_BUST_ONLY)


def test_grid_gap_selects_the_largest_pair_and_fixed_midpoint():
    r = _derive(_grid(**GAP))
    assert (r["label"], r["gap_pair"], r["midpoint"]) == (rsf.GRID_GAP, ["0.75", "0.5"], {"k": "0.63", "status": "not_run"})


@pytest.mark.parametrize("pair,mid", [(("1.0", "0.75"), "0.88"), (("0.75", "0.5"), "0.63"), (("0.5", "0.4"), "0.45"),
                                      (("0.4", "0.33"), "0.37"), (("0.33", "0.25"), "0.29"), (("0.25", "0.2"), "0.23")])
def test_midpoint_value_is_two_decimals_half_up(pair, mid):
    assert rsf.midpoint(pair) == mid


@pytest.mark.parametrize("mid_rec,label", [(CLEAR, rsf.FEASIBLE), ((0.20, 0.60, 0.03, 0.60), rsf.CLOCK_DEP),
                                           (FAIL, rsf.GRID_GAP), (None, rsf.GRID_GAP)])
def test_midpoint_conclusions(mid_rec, label):
    calls = _grid(**GAP)
    for p in rsf.POPS:
        calls[("0.63", p)] = None if mid_rec is None else _rec(*mid_rec)
    r = _derive(calls, mid="0.63")
    assert r["label"] == label
    if label == rsf.FEASIBLE:
        assert r["clearing_k"] == ["0.63"]
    if mid_rec is None:
        assert r["midpoint"]["status"] == "insufficient"


def test_pass_limited_when_eod_bust_clears_but_no_gap_pair_is_pass_clear():
    assert _derive(_grid(k0_75=(0.30, 0.40, 0.20, 0.40), k0_5=EOD_BUST_ONLY))["label"] == rsf.PASS_LIMITED


def test_inconclusive_when_an_unread_k_could_be_bust_clear():
    calls = _grid()
    calls[("0.2", "H2")] = None
    assert _derive(calls)["label"] == rsf.INCONCLUSIVE


@pytest.mark.parametrize("field", ["halted", "gated", "g1g2"])
def test_invalid_beats_feasible(field):
    calls = _grid(k0_5=CLEAR)
    kw = {"halted": {"halted": "G1"}, "gated": {"gated": "g2_killed"}, "g1g2": {"g": "other"}}[field]
    calls[("0.4", "H1")] = _rec(*FAIL, **kw)
    assert _derive(calls)["label"] == rsf.INVALID


def test_label_precedence_over_insufficient_ks():
    feas = _grid(k0_5=CLEAR)
    feas[("0.2", "FULL")] = None
    assert _derive(feas)["label"] == rsf.FEASIBLE
    pl = _grid(k0_75=(0.30, 0.40, 0.30, 0.40), k0_5=EOD_BUST_ONLY)
    pl[("0.2", "FULL")] = None
    assert _derive(pl)["label"] == rsf.PASS_LIMITED
    cd = _grid(k0_75=(0.20, 0.60, 0.03, 0.60), k0_5=EOD_BUST_ONLY)
    assert _derive(cd)["label"] == rsf.CLOCK_DEP


def test_h2_pass_floor_binding_versus_reported():
    calls = _grid()
    for p in rsf.POPS:
        calls[("0.5", p)] = _rec(0.04, 0.40 if p == "H2" else 0.60, 0.03, 0.60)
    assert _derive(calls)["label"] == rsf.FEASIBLE
    assert _derive(calls, h2=True)["label"] == rsf.CLOCK_DEP


def test_shallow_depth_or_missing_sidecar_is_insufficient():
    calls = _grid(k0_5=CLEAR)
    calls[("0.5", "H1")]["depth"]["arms"][T]["run2"]["n_sims"] = 8
    calls[("0.5", "H2")]["median"] = None
    r = _derive(calls)
    assert r["per_k"]["0.5"]["status"] == "insufficient" and len(r["per_k"]["0.5"]["reasons"]) == 2
    assert r["label"] == rsf.INCONCLUSIVE


# ── orchestration: budget cap, reproduction, digest chain ─────────────────

def _fake_call(table: dict, seconds=1.0):
    def call(step, d, timeout):
        rec = table[(step.k, step.pop)] if not step.all_tiers else table["a"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "report.json").write_bytes((json.dumps(rec["report"]) + "\n").encode())
        sha = rsf._sha(d / "report.json")
        for name in ("depth", "eod", "median"):
            (d / ("report.depth.json" if name == "depth" else f"{name}.json")).write_bytes(
                json.dumps({**rec[name], "report_sha256": sha}).encode())
        (d / "call.json").write_text(json.dumps(rec["call"]))
        return {"status": "ok", "cpu_seconds": seconds}
    return call


def _shas(rec):
    rep = (json.dumps(rec["report"]) + "\n").encode()
    sha = hashlib.sha256(rep).hexdigest()
    return sha, hashlib.sha256(json.dumps({**rec["depth"], "report_sha256": sha}).encode()).hexdigest()


def _run(tmp_path, table, budget_s, repro=None, seconds=1.0):
    rs, ds = repro or _shas(table["a"])
    g = {"candidate_daily_pnl": np.zeros(3), "full_res_trades": [], "envelope_verdict": "YES", "gross_edge_usd": 0.0}
    for rec in table.values():
        rec["call"]["g1g2_sha256"] = rsf.g1g2_digest(g)
    loader = lambda: {"prep": {"full_res_trades": [], "envelope": "YES"},  # noqa: E731
                      "manifest": {"columns": {"normal": {"gross": [0.0, 0.0, 0.0]}}}}
    return rsf.run_check(tmp_path, _fake_call(table, seconds), THR, bundle_loader=loader, budget_s=budget_s,
                         repro_report_sha=rs, repro_depth_sha=ds)


def test_budget_cap_stop_reads_insufficient_never_infeasible(tmp_path):
    table = {**_grid(), "a": _rec(*FAIL)}
    capped = _run(tmp_path / "cap", dict(table), budget_s=8.0)
    assert capped["label"] == rsf.INCONCLUSIVE
    runs = json.loads((tmp_path / "cap" / "run.json").read_text())["runs"]
    assert [r["step"] for r in runs][:6] == ["repro_a_k1.0_FULL_all", "k1.0_FULL", "k1.0_H1", "k1.0_H2",
                                             "k0.2_FULL", "k0.2_H1"]
    assert runs[7]["step"] == "k0.25_FULL" and runs[7]["status"] == "ok"
    assert sum(r["status"] == "skipped: budget cap" for r in runs) == 21 - 7
    assert json.loads((tmp_path / "cap" / "verdict.json").read_text())["label"] == rsf.INCONCLUSIVE
    assert _run(tmp_path / "full", dict(table), budget_s=1e6)["label"] == rsf.INFEASIBLE


def test_arm_completing_over_the_cap_does_not_count(tmp_path):
    r = _run(tmp_path, {**_grid(), "a": _rec(*FAIL)}, budget_s=8.0, seconds=1.5)
    runs = json.loads((tmp_path / "run.json").read_text())["runs"]
    assert runs[5]["status"] == "over budget cap" and runs[5]["cpu_seconds_running_sum"] == 9.0
    assert all(x["status"] == "skipped: budget cap" for x in runs[6:])
    assert r["per_k"]["0.2"]["status"] == "insufficient" and r["label"] == rsf.INCONCLUSIVE


def test_cap_before_reproduction_completes_is_inconclusive(tmp_path):
    assert _run(tmp_path, {**_grid(), "a": _rec(*FAIL)}, budget_s=0.0)["label"] == rsf.INCONCLUSIVE


def test_reproduction_a_mismatch_is_invalid_and_nothing_else_runs(tmp_path):
    r = _run(tmp_path, {**_grid(), "a": _rec(*FAIL)}, budget_s=1e6, repro=("0" * 64, "0" * 64))
    assert r["label"] == rsf.INVALID
    assert len(json.loads((tmp_path / "run.json").read_text())["runs"]) == 1


def test_reproduction_b_mismatch_is_invalid(tmp_path):
    table = {**_grid(), "a": _rec(0.29, 0.60, 0.30, 0.60)}
    r = _run(tmp_path, table, budget_s=1e6)
    assert r["label"] == rsf.INVALID and r["reproduction"]["b"] == "mismatch"


def test_k1_reproduction_on_a_synthetic_bundle(tmp_path, monkeypatch):
    ps = _bundle(tmp_path / "bundle")
    # The run of record's own construction (run_four_firm_remc.stage_candidate), at test depth.
    tier_series = {}
    for tier in THR.tier_keys:
        df = pd.read_csv(ps[0] / "series" / f"{tier}.csv")
        tier_series[tier] = TierSeries(daily_pnl=df["normal_pnl"].to_numpy(), intraday_low=df["normal_low"].to_numpy(),
                                       protected_pnl=df["protected_pnl"].to_numpy(),
                                       protected_low=df["protected_low"].to_numpy())
    manifest = json.loads((ps[0] / "series" / "manifest.json").read_text())
    prep = json.loads((ps[0] / "prep.json").read_text())
    report = score_candidate(strategy_label=rsf.FOUR_FIRM_LABEL,
                             candidate_daily_pnl=np.asarray(manifest["columns"]["normal"]["gross"], dtype=float),
                             full_res_trades=prep["full_res_trades"], envelope_verdict=prep["envelope"],
                             gross_edge_usd=float(sum(prep["full_res_trades"])), tier_series=tier_series,
                             mode_trigger=TRIGGER, thresholds=SMALL, n_sims=SMALL.sims_per_seed)
    target = tmp_path / "target" / "candidate_report.json"
    target.parent.mkdir()
    target.write_text(json.dumps(report.to_dict(), indent=2, default=str) + "\n")
    rsf.ffr.write_depth_record(target, report.to_dict(), SMALL, n_sims=SMALL.sims_per_seed)
    want = (rsf._sha(target), rsf._sha(target.with_suffix(".depth.json")))

    def go(out, repro, loader_sha=ps[1]):
        return rsf.run_check(out, _inproc(ps), SMALL, bundle_loader=lambda: rsf.load_bundle(
            ps[0], THR.tier_keys, prep_sha=loader_sha), budget_s=1e6,
            repro_report_sha=repro[0], repro_depth_sha=repro[1], repro_target=target)

    ok = go(tmp_path / "ok", want)
    assert ok["label"] != rsf.INVALID, ok["invalid_reasons"]
    assert ok["reproduction"]["a"]["report_sha256"] == want[0] and ok["reproduction"]["b"] == "match"
    assert ok["per_k"]["1.0"]["status"] == "valid" and ok["files"]
    bad = go(tmp_path / "bad", ("0" * 64, want[1]))
    assert bad["label"] == rsf.INVALID and bad["reproduction"]["a"]["differing_keys"] == []
    chain = go(tmp_path / "chain", want, loader_sha="0" * 64)
    assert chain["label"] == rsf.INVALID and "digest chain" in chain["invalid_reasons"][0]


def test_digest_chain_mismatch_raises_invalid(tmp_path):
    ps = _bundle(tmp_path)
    with (ps[0] / "series" / f"{T}.csv").open("a") as fh:
        fh.write("d60,0.0,0.0,0.0,0.0\n")
    with pytest.raises(rsf.Invalid, match=T):
        _load(ps)


# ── child process and freeze gate ─────────────────────────────────────────

def test_spawn_records_failure_and_kills_over_cpu_cap(tmp_path):
    fail = rsf.spawn([sys.executable, "-c", "import sys; sys.exit(3)"], 30, tmp_path / "f")
    assert (fail["status"], fail["exit_code"]) == ("failed", 3) and (tmp_path / "f" / "stderr.txt").exists()
    code = (f"import sys, time; sys.path.insert(0, {str(REPO / 'lab/analysis/c1/size_feasibility_2026-10')!r})\n"
            "import importlib.util as u; s = u.spec_from_file_location('m', sys.path[0] + '/run_size_feasibility.py')\n"
            "m = u.module_from_spec(s); s.loader.exec_module(m); from pathlib import Path\n"
            f"m.cpu_heartbeat(Path({str(tmp_path / 's' / 'cpu.json')!r}), every=0.1)\n"
            "t = time.time()\nwhile time.time() - t < 60: pass")
    (tmp_path / "s").mkdir()
    busy = rsf.spawn([sys.executable, "-c", code], 0.5, tmp_path / "s", poll=0.2)
    assert busy["status"] == "over budget cap" and busy["wall_seconds"] < 50
    assert busy["cpu_source"] == "process" and busy["cpu_seconds"] > 0.5
    before = (tmp_path / "s" / "cpu.json").read_bytes()
    time.sleep(0.5)  # the killed arm (behind any venv launcher) no longer reports
    assert (tmp_path / "s" / "cpu.json").read_bytes() == before
    rsf.write_cpu(tmp_path / "c.json")
    assert rsf.read_cpu(tmp_path / "c.json") > 0 and rsf.read_cpu(tmp_path / "none.json") is None


def test_freeze_gate_pins_the_frozen_blob_and_blocks_git_errors():
    rsf.freeze_gate(lambda *a: rsf.FROZEN_PREREG_BLOB + "\n")
    with pytest.raises(rsf.Blocked, match="not the frozen"):
        rsf.freeze_gate(lambda *a: "0" * 40)

    def broken(*a):
        raise subprocess.CalledProcessError(128, ["git", *a])
    with pytest.raises(rsf.Blocked, match="cannot read"):
        rsf.freeze_gate(broken)


def test_call_subcommand_runs_the_freeze_gate_and_out_dir_check(tmp_path, monkeypatch):
    seen = []
    monkeypatch.setattr(rsf, "freeze_gate", lambda: seen.append("freeze"))
    monkeypatch.setattr(rsf.rsb, "assert_out_dir_allowed", lambda out, repo_root: seen.append(repo_root))
    monkeypatch.setattr(rsf, "load_bundle", lambda *a, **k: {})
    monkeypatch.setattr(rsf, "score_call", lambda *a, **k: None)
    assert rsf.main(["call", "--out", str(tmp_path / "o"), "--bundle", str(tmp_path), "--k", "0.5", "--pop", "H2",
                     "--mode-trigger", "1/100", "--label", "x"]) == 0
    assert seen == ["freeze", rsf.REPO, rsf.PRIMARY]


# ── review 6067071065 folds ───────────────────────────────────────────────

def test_cpu_write_retries_while_a_reader_holds_the_file(tmp_path):
    target = tmp_path / "cpu.json"
    rsf.write_cpu(target)
    held = target.open("rb")  # on Windows this blocks os.replace until closed
    threading.Timer(0.05, held.close).start()
    rsf.write_cpu(target)  # must not raise
    assert rsf.read_cpu(target) is not None


def test_heartbeat_survives_write_failures_and_final_write_failure_keeps_exit_0(tmp_path, monkeypatch, capsys):
    calls = []

    def failing(path):
        calls.append(path)
        raise PermissionError("held")
    monkeypatch.setattr(rsf, "write_cpu", failing)
    stop = rsf.cpu_heartbeat(tmp_path / "cpu.json", every=0.02)  # must not raise
    time.sleep(0.2)
    stop.set()
    assert len(calls) >= 3  # the loop kept going after failures
    monkeypatch.setattr(rsf, "freeze_gate", lambda: None)
    monkeypatch.setattr(rsf.rsb, "assert_out_dir_allowed", lambda out, repo_root: None)
    monkeypatch.setattr(rsf, "load_bundle", lambda *a, **k: {})
    monkeypatch.setattr(rsf, "score_call", lambda *a, **k: None)
    rc = rsf.main(["call", "--out", str(tmp_path / "o"), "--bundle", str(tmp_path), "--k", "0.5", "--pop", "H2",
                   "--mode-trigger", "1/100", "--label", "x"])
    assert rc == 0 and "[cpu] " in capsys.readouterr().out


def test_spawn_reads_the_final_cpu_from_stdout(tmp_path):
    rec = rsf.spawn([sys.executable, "-c", "print('[call] done'); print('[cpu] 1.25')"], 30, tmp_path)
    assert (rec["status"], rec["cpu_seconds"], rec["cpu_source"]) == ("ok", 1.25, "process")


def _report_with_source(tmp_path, source):
    (tmp_path / "candidate_report.json").write_bytes(json.dumps({"thresholds_source": source}).encode())
    return rsf._sha(tmp_path / "candidate_report.json")


def test_checkout_preflight_names_the_required_checkout(tmp_path):
    rel = str(pss.DEFAULT_PREREG.relative_to(pss.REPO_ROOT))
    other = str(Path("C:/elsewhere/checkout")) + "\\" + rel if sys.platform == "win32" else "/elsewhere/checkout/" + rel
    sha = _report_with_source(tmp_path, other)
    with pytest.raises(rsf.Blocked, match="elsewhere"):
        rsf.checkout_preflight(tmp_path, expected_sha=sha)
    sha = _report_with_source(tmp_path, str(pss.DEFAULT_PREREG))
    rsf.checkout_preflight(tmp_path, expected_sha=sha)
    with pytest.raises(rsf.Invalid):
        rsf.checkout_preflight(tmp_path, expected_sha="0" * 64)


@pytest.mark.parametrize("tamper", [None, "edge", "daily"])
def test_k05_h2_report_g1_g2_must_equal_k1_full(tmp_path, monkeypatch, tamper):
    b = _load(_bundle(tmp_path / "b"))
    _score(b, tmp_path / "k1", "1.0", "FULL")
    real = rsf.score_candidate

    def regressed(**kw):  # a regression inside score_call that call.json would not see
        if tamper == "edge":
            kw["gross_edge_usd"] *= 0.5
        elif tamper == "daily":
            kw["candidate_daily_pnl"] = kw["candidate_daily_pnl"][30:]
        return real(**kw)
    monkeypatch.setattr(rsf, "score_candidate", regressed)
    _score(b, tmp_path / "h2", "0.5", "H2")
    calls = {("1.0", "FULL"): rsf.read_call(tmp_path / "k1"), ("0.5", "H2"): rsf.read_call(tmp_path / "h2")}
    ref = calls[("1.0", "FULL")]["call"]["g1g2_sha256"]
    assert calls[("0.5", "H2")]["call"]["g1g2_sha256"] == ref  # the digest alone cannot see it
    reasons = rsf._invalid_reasons(calls, ref)
    assert (reasons == []) == (tamper is None), reasons
