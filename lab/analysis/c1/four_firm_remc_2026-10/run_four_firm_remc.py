"""Four-firm dated re-MC executor (card ``docs/briefs/handoffs/2026-10-06-four-firm-remc-executor-card.md``).

Frozen contract: ``docs/briefs/pre-registration/2026-10-02-four-firm-dated-remc-prereg-DRAFT.md``
(FROZEN 2026-10-05) under ``docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md``.
Public code: it reads the private inputs only at run time, by pinned path and digest, and
writes every full report to a gitignored private root (``--out``).

Stages:
  prep       start gate, 20-digest re-hash, candidate series build, per-leg G1/G2
  candidate  one score_candidate call (tier_series + mode_trigger)
  reference  one score_candidate call (single series + intraday_low; G1/G2 bypassed)
  verdict    mechanical prereg §4 assignment from the two reports and prep
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[4]
for _p in (REPO / "lab", REPO / "core"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from discovery import remc_series_builder as rsb  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    TierSeries, _consistency_frac, cost_law_kill, load_scoring_thresholds, score_candidate,
)

PRIMARY = Path(r"C:/Users/joshu/multi_firm_operations")
E = PRIMARY / "lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven"
D = Path(r"C:/Users/joshu/Downloads")
C = PRIMARY / "core/data/tv_exports/cme"
REF = PRIMARY / "lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/four-firm-remc-reference-2026-10-06"
I17_MERGE = "debc13363ff3b85ed5ee41bca97a0ae9d76c5767"
EXPORT_TZ = "America/New_York"

SERIES_INPUTS = {  # (leg, mode): (path, sha256) — prereg §1a / #698 §7
    ("aegis_6j", "normal"): (D / "Aegis_6J1_VB_CME_6J1!_2026-09-03_cc310.csv", "71e732fc92d28a56fbc1e4aa358e10b68f317a110f3facc95ed34508fad96eaa"),
    ("dj30_mym_p250", "normal"): (D / "Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-09-03_9d7ea.csv", "5a5006588fa5c87628df7b1c15c8af8d8ae2250be0abb0371ea4d93665ef998e"),
    ("dj30_mym_p250", "protected"): (E / "step6-admission/exports/S-P.csv", "0373f211f5e44fe89976d7bcea2b7252724dc717541116dccb59932dfabc710a"),
    ("vanguard_mgc", "normal"): (D / "Vanguard_Gold_Futures_v0.4_VB_(MGC)_COMEX_MINI_MGC1!_2026-09-03_0e3e3.csv", "7b9cc65c98945055f35d55cdd43f049efc4b5924e2caa59f36d50b3eb872f9f2"),
    ("orb_mnq_v7", "normal"): (E / "step6-admission/exports/O-N.csv", "8e4902c3ee6224f57e29c8e1e0491c5c70695978d38036cfdc380eaded15e861"),
    ("orb_mnq_v7", "protected"): (E / "step6-admission/exports/O-P.csv", "2cb58fb6b0ec81f5859db527821a1701675ba6305553369d9096d5ee2bd93e40"),
}
REFERENCE_INPUTS = {
    C / "Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-11_ae744.csv": "e82a2c25a94c42b12888f2f8b70daa56f579c6fe02a633418edcf4b3d148ca38",
    C / "Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv": "9acfa29726a9530d2a3de5fc2290cc67672441fac2c805defd524677cce01b9e",
    C / "Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv": "8884e6dd56c786e1e59a8ab0b962a70be82f34e06af26a9582554c9f8ddc6419",
    REF / "reference_panel.csv": "a2e9192aec54dd081245232247f5f5306553910a2956f3601364c050f9aa50a2",
}
BOOK_POLICY_SHA = "ffcd3aab3e74235e60c711f266f884f96874072c3d84d0b3e1d25d67abd8567a"
MANIFEST_SHA = "6dc8b6aff1e49512b02d48023c5d5733e919f1aeb3cde39ecc8ab08a6bde252e"


class Blocked(RuntimeError):
    """Card §0.5 item 8: re-hash mismatch / start gate — BLOCKED, no run."""


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, check=True).stdout


def start_gate() -> dict:
    main_sha = _git("rev-parse", "origin/main").strip()
    ok = subprocess.run(["git", "-C", str(REPO), "merge-base", "--is-ancestor", I17_MERGE, "origin/main"]).returncode == 0
    if not ok:
        raise Blocked("I-17 start gate: #708 merge is not an ancestor of origin/main")
    return {"main_sha": main_sha, "i17_merge_sha": I17_MERGE, "i17_branch": "ON"}


def rehash(primary: Path = PRIMARY, *, manifest_sha: str = MANIFEST_SHA,
           series_inputs: dict | None = None, reference_inputs: dict | None = None,
           book_policy_bytes: bytes | None = None, book_policy_sha: str = BOOK_POLICY_SHA) -> dict:
    """Card §0.5 item 2: 20 digests. The manifest bytes are verified BEFORE they are
    parsed, and the eight source pins come from those verified bytes (Codex 4199556590)."""
    series_inputs = SERIES_INPUTS if series_inputs is None else series_inputs
    reference_inputs = REFERENCE_INPUTS if reference_inputs is None else reference_inputs
    manifest_bytes = (primary / "core/strategies/BOOK_SOURCES.sha256").read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest() != manifest_sha:
        raise Blocked("re-hash: BOOK_SOURCES.sha256 manifest bytes do not match the frozen pin")
    results = {"BOOK_SOURCES.sha256": True}
    lines = [l for l in manifest_bytes.decode("utf-8").splitlines() if l and not l.startswith("#")]
    for line in lines:
        digest, rel = line.split(None, 1)
        results[rel.strip()] = _sha(primary / rel.strip()) == digest
    if book_policy_bytes is None:
        book_policy_bytes = subprocess.run(
            ["git", "-C", str(REPO), "show", "origin/main:ops/c1_rail/book_policy.py"],
            capture_output=True, check=True).stdout
    results["book_policy.py"] = hashlib.sha256(book_policy_bytes).hexdigest() == book_policy_sha
    for (leg, mode), (path, pin) in series_inputs.items():
        results[f"{leg}:{mode}"] = _sha(path) == pin
    for path, pin in reference_inputs.items():
        results[Path(path).name] = _sha(path) == pin
    bad = [k for k, v in results.items() if not v]
    if len(results) != 20 or bad:
        raise Blocked(f"re-hash: {len(results)} digests, mismatches {bad}")
    return {"n": len(results), "all_match": True}


def candidate_trigger() -> str:
    """`book_policy.CANDIDATE_TRIGGER` read from main's source (lab may not import ops)."""
    src = _git("show", "origin/main:ops/c1_rail/book_policy.py")
    hits = re.findall(r'^CANDIDATE_TRIGGER = "([0-9.]+)"$', src, re.M)
    if len(hits) != 1:
        raise Blocked(f"CANDIDATE_TRIGGER not uniquely found in book_policy.py: {hits}")
    return hits[0]


def reference_trades() -> list[float]:
    """The I-20 reference's scaled trade P&L (same construction as remc_reference_panel)."""
    from discovery import remc_reference_panel as rp
    paths = {"aegis": "ae744", "striker": "15d8b", "striker_nas100": "beabf"}
    out: list[float] = []
    for strat, tag in paths.items():
        path = next(p for p in REFERENCE_INPUTS if tag in p.name)
        df = rp.load_csv(path)
        t = rp.pair_trades(df)
        exits = df[df["Type"].astype(str).str.startswith("Exit")].sort_values("dt")
        t = rp.reconstruct_static(t, rp.detect_initial(exits))
        _, r_dollars, _, _ = rp.pin_r_basis(pd.Series(t["pnl_static"]), rp.R_BASIS, rp.ACCOUNT)
        scale = rp.HISTORICAL_CHALLENGE_BASE_RISK[strat] * rp.ACCOUNT / r_dollars
        out += list((t["pnl_static"] * scale).astype(float))
    return out


def per_leg_g1_g2(window: tuple[date, date], thr) -> dict:
    """Candidate #1 §2/§8 via prereg I-22: per-leg G2 per tier; G1 envelope from it."""
    spec = rsb.DEFAULT_QUANTITY_SPEC
    legs: dict[str, list[float]] = {}
    for (leg, mode), (path, pin) in SERIES_INPUTS.items():
        if mode != "normal":
            continue
        trades = rsb.load_trade_table(path, pin, leg=leg, export_tz=EXPORT_TZ)
        trades = [t for t in trades if window[0] <= t.session_date <= window[1]]
        trades = rsb.apply_quantity_rule(trades, spec[leg]["normal"], leg=leg, mode="normal")
        legs[leg] = [t.gross_usd for t in trades]
    g2 = {}
    for tier in thr.tier_keys:
        g2[tier] = {leg: cost_law_kill(tier, r_deploy=len(g), gross_edge_usd=float(sum(g)), thresholds=thr).passed
                    for leg, g in legs.items()}
    killed = sorted(t for t, r in g2.items() if not all(r.values()))
    envelope = "YES" if len(killed) < len(thr.tier_keys) else "NO"
    trades_all = [x for g in legs.values() for x in g]
    return {"g2_per_leg": g2, "g2_killed_tiers": killed, "envelope": envelope,
            "r_deploy_by_leg": {k: len(v) for k, v in legs.items()},
            "full_res_trades": trades_all}


def stage_prep(out: Path) -> None:
    gate = start_gate()
    rh = rehash()
    series_dir = out / "series"
    argv = ["--export-tz", EXPORT_TZ, "--out", str(series_dir)]
    for (leg, mode), (path, pin) in SERIES_INPUTS.items():
        argv += ["--input", f"{leg}:{mode}={path}@{pin}"]
    rsb.main(argv)
    manifest = json.loads((series_dir / "manifest.json").read_text())
    window = (date.fromisoformat(manifest["window"]["start"]), date.fromisoformat(manifest["window"]["end"]))
    thr = load_scoring_thresholds()
    g = per_leg_g1_g2(window, thr)
    prep = {**gate, "rehash": rh, "window": [str(window[0]), str(window[1])],
            "window_start_weekday": window[0].strftime("%A"),
            "mffu_admissible": manifest["mffu_admissible"], "mffu_flagged_days": manifest["mffu_flagged_days"],
            "series_manifest_sha256": _sha(series_dir / "manifest.json"), **g}
    (out / "prep.json").write_text(json.dumps(prep, indent=2, default=str) + "\n")
    print(f"[prep] main {gate['main_sha'][:7]} I-17 ON; re-hash 20/20; window {prep['window']} "
          f"({prep['window_start_weekday']}); envelope {g['envelope']}")


def stage_candidate(out: Path) -> None:
    prep = json.loads((out / "prep.json").read_text())
    trigger = float(Fraction(candidate_trigger()))
    assert trigger == 0.01, trigger
    thr = load_scoring_thresholds()
    tier_series = {}
    for tier in thr.tier_keys:
        df = pd.read_csv(out / "series" / f"{tier}.csv")
        tier_series[tier] = TierSeries(daily_pnl=df["normal_pnl"].to_numpy(), intraday_low=df["normal_low"].to_numpy(),
                                       protected_pnl=df["protected_pnl"].to_numpy(), protected_low=df["protected_low"].to_numpy())
    manifest = json.loads((out / "series" / "manifest.json").read_text())
    gross = np.asarray(manifest["columns"]["normal"]["gross"], dtype=float)
    report = score_candidate(strategy_label="four-firm-remc candidate (A) Class-S #3",
                             candidate_daily_pnl=gross, full_res_trades=prep["full_res_trades"],
                             envelope_verdict=prep["envelope"], gross_edge_usd=float(sum(prep["full_res_trades"])),
                             tier_series=tier_series, mode_trigger=trigger)
    (out / "candidate_report.json").write_text(json.dumps(report.to_dict(), indent=2, default=str) + "\n")
    write_depth_record(out / "candidate_report.json", report.to_dict(), thr)
    print("[candidate] report written")


def stage_reference(out: Path) -> None:
    panel = pd.read_csv(REF / "reference_panel.csv")
    legs = ["striker", "striker_nas100", "aegis"]
    daily = panel[legs].sum(axis=1).to_numpy()
    report = score_candidate(strategy_label="four-firm-remc calibration reference (I-20)",
                             candidate_daily_pnl=daily, full_res_trades=reference_trades(),
                             envelope_verdict="YES", gross_edge_usd=float("inf"),
                             intraday_low=panel["intraday_low"].to_numpy())
    (out / "reference_report.json").write_text(json.dumps(report.to_dict(), indent=2, default=str) + "\n")
    write_depth_record(out / "reference_report.json", report.to_dict(), load_scoring_thresholds())
    print("[reference] report written")


def write_depth_record(report_path: Path, report: dict, thr) -> None:
    """Card §0.5 item 7: depth and guard evidence beside the report, bound by its SHA-256.
    The score stages pass no n_sims/horizon override, so the depth is the v2 default."""
    reasons = " ".join(report.get("gate_grade_reasons") or [])
    guard = {t: ("fail" if f"{t}: non-vacuity failed" in reasons else "pass") for t in report.get("tiers", {})}
    record = {"report_sha256": _sha(report_path), "n_sims": thr.sims_per_seed, "seeds": list(thr.seeds),
              "horizon": thr.horizon, "guard": guard}
    report_path.with_suffix(".depth.json").write_text(json.dumps(record, indent=2) + "\n")


def _rate_values(report: dict) -> list[float]:
    vals = []
    for t in report.get("tiers", {}).values():
        for run in (t.get("run1") or {}, t.get("run2") or {}):
            for k in ("headline_bust", "pass_rate"):
                if run.get(k) is not None:
                    vals.append(float(run[k]))
            vals += [float(v) for v in (run.get("rates") or {}).values() if v is not None]
    return vals


def lattice_paths(report: dict) -> int:
    """LCM of the reduced denominators of every rate: each rate is count/N, so N is a
    multiple of this value. Returns 0 if no rate is available."""
    dens = [Fraction(v).limit_denominator(10_000_000).denominator for v in _rate_values(report)]
    return math.lcm(*dens) if dens else 0


def depth_reasons(name: str, report: dict, report_sha: str | None, record: dict | None, thr) -> tuple[list[str], str]:
    """Depth/guard evidence (Codex 4199724903). A record must match the report bytes and the
    frozen depth; without a record, depth is accepted only through the lattice proof."""
    need = thr.sims_per_seed * len(thr.seeds)
    if record is not None:
        r = []
        if report_sha is None or record.get("report_sha256") != report_sha:
            r.append(f"run incomplete: {name} depth record report_sha256 does not match the report")
        if record.get("n_sims") != thr.sims_per_seed:
            r.append(f"run incomplete: {name} n_sims={record.get('n_sims')} is not the frozen {thr.sims_per_seed}")
        if list(record.get("seeds") or []) != list(thr.seeds):
            r.append(f"run incomplete: {name} seeds are not the frozen {list(thr.seeds)}")
        if record.get("horizon") != thr.horizon:
            r.append(f"run incomplete: {name} horizon is not the frozen {thr.horizon}")
        failed = sorted(t for t, g in (record.get("guard") or {}).items() if g != "pass")
        if failed or set(record.get("guard") or {}) != set(thr.tier_keys):
            r.append(f"run incomplete: {name} non-vacuity guard not passed on {failed or 'every tier'}")
        return r, "record"
    paths = lattice_paths(report)
    if paths == 0 or paths % need != 0:
        return [f"run incomplete: {name} lattice proof fails (rate denominators lcm {paths}, "
                f"need a multiple of {need})"], "lattice"
    return [], "lattice"


def _has_bust(run: dict | None) -> bool:
    return bool(run) and run.get("headline_bust") is not None


def required_runs(name: str, tier: str, t: dict) -> tuple[dict | None, list[str]]:
    """Frozen I-7/I-16 + card §0.5 items 6-7: Run-1 is mandatory on every tier; on a
    consistency tier Run-2 is mandatory and gating; on Bulenox Run-1 gates. Returns the
    gating read (None when missing) and every completeness reason. No substitution."""
    reasons = []
    consistency = _consistency_frac(tier) is not None
    if not _has_bust(t.get("run1")):
        reasons.append(f"run incomplete: {name} {tier} run1 missing")
    if consistency:
        if not _has_bust(t.get("run2")):
            reasons.append(f"run incomplete: {name} {tier} run2 missing")
        if t.get("gated_on") != "run2":
            reasons.append(f"run incomplete: {name} {tier} gated_on={t.get('gated_on')!r}, expected 'run2'")
        gating = t.get("run2") if _has_bust(t.get("run2")) else None
    else:
        if t.get("gated_on") != "run1_degenerate":
            reasons.append(f"run incomplete: {name} {tier} gated_on={t.get('gated_on')!r}, expected 'run1_degenerate'")
        gating = t.get("run1") if _has_bust(t.get("run1")) else None
    return gating, reasons


def derive_verdict(prep: dict, cand: dict, ref: dict, thr, *, cand_sha: str | None = None,
                   ref_sha: str | None = None, cand_depth: dict | None = None,
                   ref_depth: dict | None = None) -> dict:
    """Mechanical prereg §4 assignment (card §0.5 items 6-7). Pure: reads reports only."""
    reasons: list[str] = []
    if thr.sims_per_seed != 10_000 or tuple(thr.seeds) != (42, 123, 2026) or thr.horizon != 1500:
        reasons.append("run incomplete: thresholds are not the frozen v2 depth")
    for name, rep in (("candidate", cand), ("reference", ref)):
        if "2026-08-26-prop-survivor-scoring-prereg-v2" not in str(rep.get("thresholds_source", "")):
            reasons.append(f"run incomplete: {name} thresholds_source is not v2")
    evidence = {}
    for name, rep_, sha, rec in (("candidate", cand, cand_sha, cand_depth), ("reference", ref, ref_sha, ref_depth)):
        r, how = depth_reasons(name, rep_, sha, rec, thr)
        reasons += r
        evidence[name] = how
    killed = set(prep["g2_killed_tiers"])
    cand_halted = cand.get("halted_at") == "G1"
    ref_bust: dict[str, float | None] = {}
    for tier in thr.tier_keys:
        gating, r = required_runs("reference", tier, ref["tiers"].get(tier, {}))
        reasons += r
        ref_bust[tier] = None if gating is None else float(gating["headline_bust"])
        if not cand_halted and tier not in killed:
            _, r = required_runs("candidate", tier, cand["tiers"].get(tier, {}))
            reasons += r
    ambiguous = sum(1 for b in ref_bust.values() if b is not None and b <= thr.eval_bust_ceiling) >= 2
    if not cand.get("gate_grade", False):
        reasons.append("candidate gate_grade=False")
    if not ref.get("gate_grade", False):
        reasons.append("reference gate_grade=False (intraday channel not gate-grade)")
    clears = []
    if not cand_halted:
        for tier in thr.tier_keys:
            if tier in killed or (tier == "MFFU_Rapid_100K" and not prep["mffu_admissible"]):
                continue
            if cand["tiers"].get(tier, {}).get("clears_part_a"):
                clears.append(tier)
    locking = set(thr.trailing_locking_tiers)
    if ambiguous:
        verdict = "AMBIGUOUS"
    elif reasons:
        verdict = "INSUFFICIENT"
    elif len(clears) >= 2 and any(t in locking for t in clears):
        verdict = "RESOLVED"
    elif len(clears) >= 2:
        verdict = "FALSIFIED — partial"
    elif len(clears) == 1:
        verdict = "ONE-TIER"
    else:
        verdict = "FALSIFIED — early-fail"
    return {"verdict": verdict, "clears_after_i24_and_g2": clears, "insufficient_reasons": reasons,
            "reference_bust": ref_bust, "ambiguous": ambiguous, "depth_evidence": evidence}


def stage_verdict(out: Path) -> None:
    thr = load_scoring_thresholds()
    prep = json.loads((out / "prep.json").read_text())
    cand = json.loads((out / "candidate_report.json").read_text())
    ref = json.loads((out / "reference_report.json").read_text())
    def _record(name: str):
        f = out / f"{name}_report.depth.json"
        return json.loads(f.read_text()) if f.exists() else None
    result = derive_verdict(prep, cand, ref, thr,
                            cand_sha=_sha(out / "candidate_report.json"), ref_sha=_sha(out / "reference_report.json"),
                            cand_depth=_record("candidate"), ref_depth=_record("reference"))
    result.update({"candidate_report_sha256": _sha(out / "candidate_report.json"),
                   "reference_report_sha256": _sha(out / "reference_report.json"),
                   "prep_sha256": _sha(out / "prep.json")})
    (out / "verdict.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"[verdict] {result['verdict']}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["prep", "candidate", "reference", "verdict"])
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    {"prep": stage_prep, "candidate": stage_candidate, "reference": stage_reference, "verdict": stage_verdict}[a.stage](out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
