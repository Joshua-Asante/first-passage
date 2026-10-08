"""Size-feasibility check for the accepted Tradeify book (uniform k).

Contract: ``docs/briefs/pre-registration/2026-10-08-tradeify-size-feasibility-prereg-DRAFT.md``
(§2.3 build, §3 grid, §4 gates, §6 labels). Public code: it reads the four-firm depth
re-run's private bundle at run time through its digest chain and writes every output to a
gitignored private root (``--out``). It refuses to run until that file is FROZEN on
``origin/main`` (§R).

Subcommands:
  run   the whole check in the §8.1 order: digest chain, reproduction (a) and (b),
        k = 1 H1/H2, then k smallest first (FULL, H1, H2 each), the GRID-GAP midpoint
        when triggered, then ``verdict.json`` and ``run.json``. Each arm is a serial
        child process; its process CPU time is summed against the 12 CPU-hour cap.
  call  one (k, population) score_candidate call with sidecars on (used by ``run``).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import math
import re
import subprocess
import sys
import threading
import time
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from pathlib import Path
from typing import Callable, NamedTuple

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[4]
for _p in (REPO / "lab", REPO / "core"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from discovery import remc_series_builder as rsb  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    TierSeries, load_scoring_thresholds, score_candidate,
)

_spec = importlib.util.spec_from_file_location(
    "four_firm_runner", REPO / "lab/analysis/c1/four_firm_remc_2026-10/run_four_firm_remc.py")
ffr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ffr)

PRIMARY = ffr.PRIMARY
PRIVATE = PRIMARY / "lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts"
BUNDLE = PRIVATE / "four-firm-remc-rerun-2026-10-06-depth"
PREREG = "docs/briefs/pre-registration/2026-10-08-tradeify-size-feasibility-prereg-DRAFT.md"

# §2.1 digest chain and reproduction targets (RESULTS, depth re-run root).
PREP_SHA = "feefa7ab28ff17d8b1a727bae0adf6656369a4ea73eafea2218cdafbd8f4c3b5"
REPRO_REPORT_SHA = "4076857777e67cedd5755ba637693ce45638357a8a5b1fb17077e63ac28ec2ed"
REPRO_DEPTH_SHA = "87a66d8e9d2baf3b474feb7e69e1e2cdb4138f27e911f666d9b57d0118e483f2"
FOUR_FIRM_LABEL = "four-firm-remc candidate (A) Class-S #3"

TRADEIFY = "Tradeify_Select_100K"
GRID = ("1.0", "0.75", "0.5", "0.4", "0.33", "0.25", "0.2")  # §3.1, descending (GRID-GAP pairs)
RUN_ORDER = ("1.0", "0.2", "0.25", "0.33", "0.4", "0.5", "0.75")  # §8.1, smallest k first after k = 1
H2_PASS_BINDING = False  # §4.2 / §9 item 1: H2 pass floor REPORTED
POPS = ("FULL", "H1", "H2")
BUDGET_CPU_HOURS = 12.0  # §8.1 / §9 item 3
MEDIAN_RULE = "LOWER_NEAREST_RANK_INF_INCLUDED"
VACUITY_TEXT = "real intraday_low channel is vacuous"
FROZEN_DEPTH = (10_000, (42, 123, 2026), 1500)

INVALID, FEASIBLE, CLOCK_DEP, GRID_GAP = "INVALID", "FEASIBLE", "CLOCK-DEPENDENT", "GRID-GAP"
PASS_LIMITED, INCONCLUSIVE, INFEASIBLE = "PASS-LIMITED", "INCONCLUSIVE", "INFEASIBLE"


class Invalid(RuntimeError):
    """§6 label 1: digest chain, reproduction, halt, gating run or G1/G2 pin broken."""


class Blocked(RuntimeError):
    """§R: the pre-registration is not FROZEN on origin/main."""


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


# ── freeze gate ───────────────────────────────────────────────────────────

def freeze_gate(text: str | None = None) -> None:
    """§R: refuse to score unless the prereg on origin/main is FROZEN and signed."""
    if text is None:
        text = ffr._git("show", f"origin/main:{PREREG}")
    if not re.search(r"^\*\*Status:\*\* `FROZEN \d{4}-\d{2}-\d{2}`", text, re.M):
        raise Blocked("prereg Status is not FROZEN on origin/main")
    if re.search(r"^- \*\*Signed:\*\* —$", text, re.M):
        raise Blocked("prereg on origin/main is unsigned")


# ── bundle, series, populations ───────────────────────────────────────────

def load_bundle(bundle: Path, tiers, *, prep_sha: str = PREP_SHA) -> dict:
    """§2.1 digest chain: prep.json → series_manifest_sha256 → manifest → tier CSV
    SHA-256s in its ``outputs``. Each file is hashed before it is parsed; any
    mismatch raises Invalid."""
    prep_b = (bundle / "prep.json").read_bytes()
    if hashlib.sha256(prep_b).hexdigest() != prep_sha:
        raise Invalid("digest chain: prep.json does not match its pin")
    prep = json.loads(prep_b)
    man_b = (bundle / "series" / "manifest.json").read_bytes()
    if hashlib.sha256(man_b).hexdigest() != prep["series_manifest_sha256"]:
        raise Invalid("digest chain: series manifest does not match prep.json")
    manifest = json.loads(man_b)
    series = {}
    for tier in tiers:
        csv_b = (bundle / "series" / f"{tier}.csv").read_bytes()
        want = ((manifest.get("outputs") or {}).get(f"{tier}.csv") or {}).get("sha256")
        if hashlib.sha256(csv_b).hexdigest() != want:
            raise Invalid(f"digest chain: {tier}.csv does not match the manifest")
        df = pd.read_csv(io.BytesIO(csv_b))
        if len(df) != manifest["n_days"]:
            raise Invalid(f"digest chain: {tier}.csv has {len(df)} rows, manifest n_days {manifest['n_days']}")
        series[tier] = df
    return {"prep": prep, "manifest": manifest, "series": series}


def population(n: int, pop: str) -> slice:
    """§4.1: FULL = all rows; H1 = first ceil(N/2); H2 = the rest, in order."""
    h = math.ceil(n / 2)
    return {"FULL": slice(0, n), "H1": slice(0, h), "H2": slice(h, n)}[pop]


def scaled_series(df: pd.DataFrame, k: float, sl: slice) -> TierSeries:
    """§1 method: every channel × k, then the population slice."""
    def ch(col):
        return df[col].to_numpy()[sl] * k
    return TierSeries(daily_pnl=ch("normal_pnl"), intraday_low=ch("normal_low"),
                      protected_pnl=ch("protected_pnl"), protected_low=ch("protected_low"))


def g1g2_inputs(b: dict) -> dict:
    """§2.1: the k = 1 FULL G1/G2 inputs, exactly as run_four_firm_remc passes them.
    Never scaled, never sliced."""
    trades = b["prep"]["full_res_trades"]
    return {"candidate_daily_pnl": np.asarray(b["manifest"]["columns"]["normal"]["gross"], dtype=float),
            "full_res_trades": trades, "envelope_verdict": b["prep"]["envelope"],
            "gross_edge_usd": float(sum(trades))}


def g1g2_digest(g: dict) -> str:
    h = hashlib.sha256(np.ascontiguousarray(g["candidate_daily_pnl"], dtype=float).tobytes())
    h.update(_canon([g["full_res_trades"], g["envelope_verdict"], repr(g["gross_edge_usd"])]).encode())
    return h.hexdigest()


def median_days_to_pass(days: list[int], n: int):
    """T00 LOWER_NEAREST_RANK_INF_INCLUDED: the ceil(n/2)-th smallest of n, with every
    non-passer at infinity. Returns an int, or the string "inf"."""
    rank = math.ceil(n / 2)
    return sorted(days)[rank - 1] if rank <= len(days) else "inf"


# ── one call ──────────────────────────────────────────────────────────────

def score_call(bundle: dict, out: Path, *, k: str, pop: str, all_tiers: bool, thr,
               mode_trigger: float, label: str) -> Path:
    """One score_candidate call with sidecars on. Writes report.json, its depth record,
    eod.json, median.json and call.json into ``out``. The sidecars are written even when
    the call raises (bound to no report)."""
    out.mkdir(parents=True, exist_ok=True)
    tiers = thr.tier_keys if all_tiers else (TRADEIFY,)
    n = bundle["manifest"]["n_days"]
    ts = {t: scaled_series(bundle["series"][t], float(k), population(n, pop)) for t in tiers}
    g = g1g2_inputs(bundle)
    (out / "call.json").write_text(json.dumps(
        {"k": k, "pop": pop, "tiers": list(tiers), "rows": len(ts[tiers[0]].daily_pnl),
         "mode_trigger": mode_trigger, "label": label, "g1g2_sha256": g1g2_digest(g)}, indent=2) + "\n")
    sidecar: dict = {}
    report_sha = None
    try:
        report = score_candidate(strategy_label=label, **g, tier_series=ts, mode_trigger=mode_trigger,
                                 thresholds=thr, n_sims=thr.sims_per_seed,
                                 tiers=None if all_tiers else (TRADEIFY,), sidecar=sidecar)
        # Same writer as run_four_firm_remc.stage_candidate (reproduction (a) compares bytes).
        (out / "report.json").write_text(json.dumps(report.to_dict(), indent=2, default=str) + "\n")
        ffr.write_depth_record(out / "report.json", report.to_dict(), thr, n_sims=thr.sims_per_seed)
        report_sha = _sha(out / "report.json")
    finally:
        eod = {t: {"guard_arms": s["guard_arms"], "gate_grade_reasons": s["gate_grade_reasons"]}
               for t, s in sidecar.items()}
        med = {t: {run: {"n": c.get("n"), "n_pass": len(c.get("days_to_pass", [])),
                         "median": median_days_to_pass(c["days_to_pass"], c["n"]) if "n" in c else None}
                   for run, c in s["days_to_pass"].items()} for t, s in sidecar.items()}
        for name, body in (("eod", eod), ("median", med)):
            (out / f"{name}.json").write_text(json.dumps(
                {"report_sha256": report_sha, "rule": MEDIAN_RULE if name == "median" else None,
                 "tiers": body}, indent=2, default=str) + "\n")
    return out / "report.json"


def read_call(d: Path) -> dict | None:
    """Everything §6 reads for one call; None when no report exists."""
    if not (d / "report.json").exists():
        return None
    def j(name):
        f = d / name
        return json.loads(f.read_text()) if f.exists() else None
    return {"report": j("report.json"), "report_sha256": _sha(d / "report.json"),
            "depth": j("report.depth.json"), "eod": j("eod.json"), "median": j("median.json"),
            "call": j("call.json")}


# ── §6 derivation (pure) ──────────────────────────────────────────────────

def _call_validity(rd: dict | None, k: str, thr, k1_guard_passed: bool) -> tuple[str, list[str]]:
    """'valid' | 'vacuity-read' | 'insufficient', with reasons (§6 validity, vacuity)."""
    if rd is None:
        return "insufficient", ["call incomplete: no report"]
    reasons = []
    rep, sha = rd["report"], rd["report_sha256"]
    dep = rd.get("depth") or {}
    if dep.get("report_sha256") != sha:
        reasons.append("no depth record bound to the report")
    else:
        for run in ("run1", "run2"):
            e = ((dep.get("arms") or {}).get(TRADEIFY) or {}).get(run) or {}
            if (e.get("n_sims"), tuple(e.get("seeds") or ()), e.get("horizon")) != (
                    thr.sims_per_seed, tuple(thr.seeds), thr.horizon):
                reasons.append(f"{run} not at frozen depth")
    eod = rd.get("eod") or {}
    arms = ((eod.get("tiers") or {}).get(TRADEIFY) or {}).get("guard_arms") or {}
    if eod.get("report_sha256") != sha or set(arms) != {"eod", "zeros", "real"} or any(
            arms["eod"].get(x) is None for x in ("headline_bust", "pass_rate")):
        reasons.append("no valid EOD sidecar")
    med = ((rd.get("median") or {}).get("tiers") or {}).get(TRADEIFY) or {}
    pooled = thr.sims_per_seed * len(thr.seeds)
    if (rd.get("median") or {}).get("report_sha256") != sha or any(
            (med.get(r) or {}).get("n") != pooled or (med.get(r) or {}).get("median") is None
            for r in ("run1", "run2")):
        reasons.append("no valid median sidecar")
    if (rd.get("call") or {}).get("g1g2_sha256") is None:
        reasons.append("no call record")
    if reasons:
        return "insufficient", reasons
    if rep.get("gate_grade"):
        return "valid", []
    gr = rep.get("gate_grade_reasons") or []
    if (Decimal(k) < 1 and rep.get("breach_clock") == "intraday_honest" and len(gr) == 1
            and VACUITY_TEXT in gr[0] and k1_guard_passed):
        return "vacuity-read", []
    return "insufficient", [f"gate_grade false: {gr}"]


def _reads(rd: dict) -> dict:
    t = rd["report"]["tiers"][TRADEIFY]["run2"]
    e = rd["eod"]["tiers"][TRADEIFY]["guard_arms"]["eod"]
    return {"intraday": (float(t["headline_bust"]), float(t["pass_rate"])),
            "eod": (float(e["headline_bust"]), float(e["pass_rate"]))}


def _invalid_reasons(calls: dict, ref_g1g2: str) -> list[str]:
    out = []
    for (k, pop), rd in calls.items():
        if rd is None:
            continue
        rep = rd["report"]
        if rep.get("halted_at"):
            out.append(f"k={k} {pop}: halted_at={rep['halted_at']}")
        if (rep.get("tiers") or {}).get(TRADEIFY, {}).get("gated_on") != "run2":
            out.append(f"k={k} {pop}: Tradeify gated_on is not run2")
        got = (rd.get("call") or {}).get("g1g2_sha256")
        if got is not None and got != ref_g1g2:
            out.append(f"k={k} {pop}: G1/G2 inputs differ from the k = 1 FULL bytes")
    return out


def assess_k(calls: dict, k: str, thr, *, h2_pass_binding: bool) -> dict:
    """Validity and the clears of one k on both clocks (§4.2, §6 terms)."""
    status, reasons, vac = "valid", [], []
    for pop in POPS:
        k1 = calls.get(("1.0", pop))
        k1_ok = bool(k1 and k1["report"].get("gate_grade"))
        s, r = _call_validity(calls.get((k, pop)), k, thr, k1_ok)
        if s == "insufficient":
            status = "insufficient"
            reasons += [f"{pop}: {x}" for x in r]
        elif s == "vacuity-read":
            vac.append(pop)
    res = {"status": status, "reasons": reasons, "vacuity_read": vac}
    if status != "valid":
        return res
    reads = {pop: _reads(calls[(k, pop)]) for pop in POPS}
    pass_pops = ("FULL", "H2") if h2_pass_binding else ("FULL",)
    for clock in ("intraday", "eod"):
        res[clock] = {
            "bust_clear": all(reads[p][clock][0] <= thr.eval_bust_ceiling for p in ("FULL", "H2")),
            "pass_clear": all(reads[p][clock][1] >= thr.pass_floor for p in pass_pops)}
    return res


def gap_pair(per_k: dict) -> tuple[str, str] | None:
    """§6: the largest adjacent grid pair, both valid, with k_lo EOD bust-clear and
    k_hi not."""
    for hi, lo in zip(GRID, GRID[1:]):
        a, b = per_k[hi], per_k[lo]
        if a["status"] == b["status"] == "valid" and b["eod"]["bust_clear"] and not a["eod"]["bust_clear"]:
            return hi, lo
    return None


def midpoint(pair: tuple[str, str]) -> str:
    """(k_hi + k_lo) / 2 to 2 decimals, half up, in decimal arithmetic."""
    return str(((Decimal(pair[0]) + Decimal(pair[1])) / 2).quantize(Decimal("0.01"), ROUND_HALF_UP))


def derive_label(calls: dict, thr, *, ref_g1g2: str, h2_pass_binding: bool = H2_PASS_BINDING,
                 invalid: list[str] = (), mid: str | None = None) -> dict:
    """§6 labels in order; the first that holds. ``calls`` maps (k, pop) to read_call
    output (None when absent). Pure."""
    bad = list(invalid) + _invalid_reasons(calls, ref_g1g2)
    per_k = {k: assess_k(calls, k, thr, h2_pass_binding=h2_pass_binding) for k in GRID}
    out = {"per_k": per_k, "invalid_reasons": bad, "vacuity_read_k": [k for k in GRID if per_k[k]["vacuity_read"]],
           "clearing_k": [], "gap_pair": None, "midpoint": None}
    if bad:
        return {**out, "label": INVALID}
    valid = [k for k in GRID if per_k[k]["status"] == "valid"]

    def clear(k, clock, info=per_k):
        return info[k][clock]["bust_clear"] and info[k][clock]["pass_clear"]
    feas = [k for k in valid if clear(k, "intraday")]
    if feas:
        return {**out, "label": FEASIBLE, "clearing_k": feas, "largest_clearing_k": feas[0]}
    if any(clear(k, "eod") for k in valid):
        return {**out, "label": CLOCK_DEP}
    pair = gap_pair(per_k)
    if pair and per_k[pair[0]]["eod"]["pass_clear"]:
        out.update(gap_pair=list(pair), midpoint={"k": midpoint(pair), "status": "not_run"})
        if mid is not None:
            m = assess_k(calls, mid, thr, h2_pass_binding=h2_pass_binding)
            out["midpoint"] = {"k": mid, **m}
            if m["vacuity_read"]:
                out["vacuity_read_k"].append(mid)
            if m["status"] != "insufficient":
                if clear(mid, "intraday", {mid: m}):
                    return {**out, "label": FEASIBLE, "clearing_k": [mid], "largest_clearing_k": mid}
                if clear(mid, "eod", {mid: m}):
                    return {**out, "label": CLOCK_DEP}
        return {**out, "label": GRID_GAP}
    if any(per_k[k]["eod"]["bust_clear"] for k in valid):
        return {**out, "label": PASS_LIMITED}
    if any(per_k[k]["status"] == "insufficient" for k in GRID):
        return {**out, "label": INCONCLUSIVE}
    return {**out, "label": INFEASIBLE}


# ── orchestration ─────────────────────────────────────────────────────────

class Step(NamedTuple):
    name: str
    k: str
    pop: str
    all_tiers: bool = False


def step_label(step: Step) -> str:
    """Reproduction (a) carries the four-firm label, so its report bytes can match."""
    return FOUR_FIRM_LABEL if step.all_tiers else f"size-feasibility k={step.k} {step.pop}"


CPU_FILE = "cpu.json"


def write_cpu(path: Path) -> None:
    """Child side: this interpreter's total process CPU time so far (all threads, from
    process start), written atomically. On Windows a venv's python.exe is a launcher
    that runs the real interpreter as a grandchild, so the parent cannot read the arm's
    CPU from the process it spawned; the arm reports its own."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps({"cpu_seconds": time.process_time()}))
    tmp.replace(path)


def cpu_heartbeat(path: Path, every: float = 5.0) -> None:
    def beat():
        while True:
            write_cpu(path)
            time.sleep(every)
    write_cpu(path)
    threading.Thread(target=beat, daemon=True).start()


def read_cpu(path: Path) -> float | None:
    try:
        return float(json.loads(path.read_text())["cpu_seconds"])
    except (OSError, ValueError, KeyError, TypeError):
        return None


def spawn(cmd: list[str], cpu_left: float, logdir: Path, *, poll: float = 1.0) -> dict:
    """Run one child; kill it once its reported CPU time exceeds ``cpu_left`` (it could
    no longer count within the cap). Records PID, exit code, CPU seconds and the SHA-256
    of stdout/stderr (also kept beside the call). The child writes ``logdir/cpu.json``."""
    logdir.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def cpu() -> tuple[float, str]:  # the arm's own report; wall time (>= a serial arm's CPU) without one
        c = read_cpu(logdir / CPU_FILE)
        return (c, "process") if c is not None else (time.monotonic() - t0, "wall")
    while True:
        try:
            so, se = proc.communicate(timeout=poll)
            status = "ok" if proc.returncode == 0 else "failed"
            break
        except subprocess.TimeoutExpired:
            if (read_cpu(logdir / CPU_FILE) or 0.0) > cpu_left:  # no report yet: never killed on wall time
                proc.kill()
                so, se = proc.communicate()
                status = "over budget cap"
                break
    used, source = cpu()
    (logdir / "stdout.txt").write_bytes(so)
    (logdir / "stderr.txt").write_bytes(se)
    return {"cmd": cmd, "pid": proc.pid, "exit_code": proc.returncode, "status": status,
            "cpu_seconds": used, "cpu_source": source, "wall_seconds": time.monotonic() - t0,
            "stdout_sha256": hashlib.sha256(so).hexdigest(), "stderr_sha256": hashlib.sha256(se).hexdigest()}


CAPPED = ("over budget cap", "skipped: budget cap")


def run_check(out: Path, call: Callable[[Step, Path, float], dict], thr, *, bundle_loader: Callable[[], dict],
              budget_s: float = BUDGET_CPU_HOURS * 3600.0, repro_report_sha: str = REPRO_REPORT_SHA,
              repro_depth_sha: str = REPRO_DEPTH_SHA, repro_target: Path | None = None) -> dict:
    """§8.1 fixed run order under the 12 CPU-hour cap: reproduction (a), (b), k = 1 H1
    and H2, then RUN_ORDER (smallest k first, FULL/H1/H2 each), then the GRID-GAP
    midpoint when triggered (§9 item 2). ``call(step, dir, cpu_left)`` leaves
    read_call-able files in ``dir`` and returns a run record with ``status`` and
    ``cpu_seconds``. An arm counts only if the running CPU sum including it is ≤ the cap
    when it completes; otherwise it and every later arm are INSUFFICIENT. Writes
    verdict.json and run.json."""
    runs: list[dict] = []
    spent = 0.0
    calls: dict = {}

    def do(step: Step) -> dict | None:
        nonlocal spent
        d = out / "calls" / step.name
        if spent >= budget_s:
            runs.append({"step": step.name, "status": "skipped: budget cap"})
            return None
        rec = dict(call(step, d, budget_s - spent))
        spent += float(rec["cpu_seconds"])
        if spent > budget_s:
            rec["status"] = "over budget cap"
        runs.append({"step": step.name, **rec, "cpu_seconds_running_sum": spent})
        return read_call(d) if rec["status"] == "ok" else None

    def finish(result: dict) -> dict:
        result.update(budget_cpu_seconds=budget_s, spent_cpu_seconds=spent, h2_pass_binding=H2_PASS_BINDING)
        (out / "run.json").write_text(json.dumps({"runs": runs}, indent=2, default=str) + "\n")
        (out / "verdict.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
        return result

    out.mkdir(parents=True, exist_ok=True)
    try:
        ref = g1g2_digest(g1g2_inputs(bundle_loader()))
    except (Invalid, OSError, KeyError, ValueError) as exc:
        return finish({"label": INVALID, "invalid_reasons": [f"digest chain: {exc!r}"]})
    kw = dict(ref_g1g2=ref, h2_pass_binding=H2_PASS_BINDING)
    repro = {}
    a = do(Step("repro_a_k1.0_FULL_all", "1.0", "FULL", all_tiers=True))
    if a is None:
        if runs[-1]["status"] not in CAPPED:
            return finish({"label": INVALID, "invalid_reasons": ["reproduction (a) failed to complete"]})
        return finish({**derive_label({}, thr, **kw), "reproduction": {"a": "not completed: budget cap"}})
    d_a = out / "calls" / "repro_a_k1.0_FULL_all"
    repro["a"] = {"report_sha256": a["report_sha256"], "depth_sha256": _sha(d_a / "report.depth.json")}
    if a["report_sha256"] != repro_report_sha or repro["a"]["depth_sha256"] != repro_depth_sha:
        if repro_target is not None and repro_target.exists():  # diagnostic only: which keys differ
            want = json.loads(repro_target.read_text())
            repro["a"]["differing_keys"] = sorted(
                x for x in set(want) | set(a["report"]) if _canon(want.get(x)) != _canon(a["report"].get(x)))
        return finish({"label": INVALID, "reproduction": repro,
                       "invalid_reasons": ["reproduction (a): report or depth record bytes differ"]})
    b = calls[("1.0", "FULL")] = do(Step("k1.0_FULL", "1.0", "FULL"))
    if b is None:
        if runs[-1]["status"] not in CAPPED:
            return finish({"label": INVALID, "reproduction": repro,
                           "invalid_reasons": ["reproduction (b) failed to complete"]})
        repro["b"] = "not completed: budget cap"
    else:
        repro["b"] = "match" if _canon(a["report"]["tiers"][TRADEIFY]) == _canon(b["report"]["tiers"][TRADEIFY]) \
            else "mismatch"
        if repro["b"] == "mismatch":
            return finish({"label": INVALID, "reproduction": repro,
                           "invalid_reasons": ["reproduction (b): Tradeify entry differs from (a)"]})
    for k in RUN_ORDER:
        for pop in POPS:
            if (k, pop) not in calls:
                calls[(k, pop)] = do(Step(f"k{k}_{pop}", k, pop))
    result = derive_label(calls, thr, **kw)
    if result["label"] == GRID_GAP:
        mid = result["midpoint"]["k"]
        for pop in POPS:
            calls[(mid, pop)] = do(Step(f"k{mid}_{pop}", mid, pop))
        result = derive_label(calls, thr, mid=mid, **kw)
    result["reproduction"] = repro
    result["files"] = {str(p.relative_to(out)).replace("\\", "/"): _sha(p)
                       for p in sorted((out / "calls").rglob("*")) if p.is_file()}
    return finish(result)


def subprocess_call(bundle: Path, trigger: str) -> Callable[[Step, Path, float], dict]:
    def call(step: Step, d: Path, cpu_left: float) -> dict:
        cmd = [sys.executable, "-I", str(Path(__file__).resolve()), "call", "--bundle", str(bundle),
               "--out", str(d), "--k", step.k, "--pop", step.pop, "--mode-trigger", trigger,
               "--label", step_label(step)]
        return spawn(cmd + (["--all-tiers"] if step.all_tiers else []), cpu_left, d)
    return call


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--out", required=True)
    r.add_argument("--bundle", default=str(BUNDLE))
    c = sub.add_parser("call")
    for a in ("--out", "--bundle", "--k", "--pop", "--mode-trigger", "--label"):
        c.add_argument(a, required=True)
    c.add_argument("--all-tiers", action="store_true")
    a = ap.parse_args(argv)
    thr = load_scoring_thresholds()
    if (thr.sims_per_seed, tuple(thr.seeds), thr.horizon) != FROZEN_DEPTH:
        raise Invalid("thresholds are not the frozen v2 depth")
    out, bundle = Path(a.out), Path(a.bundle)
    if a.cmd == "call":
        if a.k not in GRID and not re.fullmatch(r"0\.\d\d", a.k):
            raise ValueError(f"k={a.k} is neither a grid point nor a 2-decimal midpoint")
        out.mkdir(parents=True, exist_ok=True)
        cpu_heartbeat(out / CPU_FILE)
        trig = float(Fraction(a.mode_trigger))
        b = load_bundle(bundle, thr.tier_keys if a.all_tiers else (TRADEIFY,))
        score_call(b, out, k=a.k, pop=a.pop, all_tiers=a.all_tiers, thr=thr, mode_trigger=trig, label=a.label)
        write_cpu(out / CPU_FILE)
        print(f"[call] k={a.k} {a.pop} report written")
        return 0
    freeze_gate()
    for root in (REPO, PRIMARY):
        rsb.assert_out_dir_allowed(out, repo_root=root)
    trigger = ffr.candidate_trigger()
    if float(Fraction(trigger)) != 0.01:
        raise Blocked(f"CANDIDATE_TRIGGER {trigger} is not the frozen 0.01")
    result = run_check(out, subprocess_call(bundle, trigger), thr,
                       bundle_loader=lambda: load_bundle(bundle, thr.tier_keys),
                       repro_target=bundle / "candidate_report.json")
    print(f"[run] {date.today()} label {result['label']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
