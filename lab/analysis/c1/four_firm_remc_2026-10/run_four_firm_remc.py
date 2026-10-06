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
    TierSeries, cost_law_kill, load_scoring_thresholds, score_candidate,
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


def rehash() -> dict:
    results = {}
    lines = [l for l in (PRIMARY / "core/strategies/BOOK_SOURCES.sha256").read_text().splitlines()
             if l and not l.startswith("#")]
    for line in lines:
        digest, rel = line.split(None, 1)
        results[rel.strip()] = _sha(PRIMARY / rel.strip()) == digest
    bp = hashlib.sha256(subprocess.run(["git", "-C", str(REPO), "show", "origin/main:ops/c1_rail/book_policy.py"],
                                       capture_output=True, check=True).stdout).hexdigest()
    mf = hashlib.sha256(subprocess.run(["git", "-C", str(REPO), "show", "origin/main:core/strategies/BOOK_SOURCES.sha256"],
                                       capture_output=True, check=True).stdout).hexdigest()
    results["book_policy.py"] = bp == BOOK_POLICY_SHA
    results["BOOK_SOURCES.sha256"] = mf == MANIFEST_SHA
    for (leg, mode), (path, pin) in SERIES_INPUTS.items():
        results[f"{leg}:{mode}"] = _sha(path) == pin
    for path, pin in REFERENCE_INPUTS.items():
        results[path.name] = _sha(path) == pin
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
    print("[reference] report written")


def _gating(tier: dict) -> dict:
    return tier.get("run2") or tier.get("run1") or {}


def stage_verdict(out: Path) -> None:
    thr = load_scoring_thresholds()
    prep = json.loads((out / "prep.json").read_text())
    cand = json.loads((out / "candidate_report.json").read_text())
    ref = json.loads((out / "reference_report.json").read_text())
    locking = set(thr.trailing_locking_tiers)
    reasons = []
    # Completeness (card §0.5 item 7)
    killed = set(prep["g2_killed_tiers"])
    for name, rep, skip in (("candidate", cand, killed), ("reference", ref, set())):
        for tier in thr.tier_keys:
            if tier in skip or cand.get("halted_at") == "G1" and name == "candidate":
                continue
            t = rep["tiers"].get(tier, {})
            if not _gating(t) or "headline_bust" not in _gating(t):
                reasons.append(f"run incomplete: {name} {tier}")
    ref_bust = {t: _gating(ref["tiers"].get(t, {})).get("headline_bust") for t in thr.tier_keys}
    ambiguous = sum(1 for b in ref_bust.values() if b is not None and float(b) <= thr.eval_bust_ceiling) >= 2
    if not cand.get("gate_grade", False):
        reasons.append("candidate gate_grade=False")
    if not ref.get("gate_grade", False):
        reasons.append("reference gate_grade=False (intraday channel not gate-grade)")
    clears = []
    if cand.get("halted_at") != "G1":
        for tier in thr.tier_keys:
            t = cand["tiers"].get(tier, {})
            if tier in killed:
                continue
            if tier == "MFFU_Rapid_100K" and not prep["mffu_admissible"]:
                continue
            if t.get("clears_part_a"):
                clears.append(tier)
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
    result = {"verdict": verdict, "clears_after_i24_and_g2": clears, "insufficient_reasons": reasons,
              "reference_bust": ref_bust, "ambiguous": ambiguous,
              "candidate_report_sha256": _sha(out / "candidate_report.json"),
              "reference_report_sha256": _sha(out / "reference_report.json"),
              "prep_sha256": _sha(out / "prep.json")}
    (out / "verdict.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"[verdict] {verdict}")


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
