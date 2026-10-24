"""Q-ORPREM-1 CLI — g0 (Phase 1 pre-flight) and score (Phase 2 one run).

Both subcommands are guarded by the pre-registration status: the guard reads
only the pre-registration markdown (never data) and REFUSES with exit code 2
unless its ``**Status:**`` line is frozen — it must contain the token
``FROZEN`` and must not carry a not-frozen marker (``NOT FROZEN`` or
``DRAFT``).  The current pre-registration (revision 3, 2026-10-19) is
``OPEN — DRAFT (pre-lock)``; §7 states it "not authorized by this draft", so
every invocation of either subcommand refuses until the freeze is recorded.
``score`` additionally refuses (also exit 2) until the §7 Phase 2 v7 gate is
recorded via ``--v7-gate``: either the 40-hex v7 S4 freeze commit (which must
be an ancestor of the commit this run executes at) or ``ruling:<reference>``
naming Joshua's ruling that this study's exposure enters the v7 disclosure.
It also refuses when an input's sha256 differs from the one G0 recorded.

Usage::

    python run_orprem.py g0   [--prereg P] [--e2-csv CSV]
                               [--e1-csv CSV --e1-csv CSV] [--out G0.json]
    python run_orprem.py score [--prereg P] [--e2-csv CSV] [--g0 G0.json]
                               --v7-gate SHA|ruling:REF [--e1-csv CSV --e1-csv CSV]
                               [--out RECORD.json] [--seed S] [--boot-n N] [--block L]

Phase 0 is synthetic-only: the defaults point at the primary checkout's
gitignored vendor exports (never read while the guard refuses); tests pass
tmp_path inputs explicitly.  This file owns no statistics — everything
numeric lives in orprem.py.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CAMP = Path(__file__).resolve().parent
if str(CAMP) not in sys.path:
    sys.path.insert(0, str(CAMP))

import orprem  # noqa: E402  (camp sibling; see lab/conftest.py)

REPO = Path(__file__).resolve().parents[4]
PREREG_DEFAULT = REPO / "docs" / "briefs" / "pre-registration" / orprem.PREREG_NAME
_E2_NAME = "BAR_EXPORT_v0.2_CME_MINI_MNQ1!_2026-07-21_dd9d8.csv"
_E1_OLD_NAME = "BAR_EXPORT_v0.2_CME_MINI_MNQ1!_2026-07-13_86a38.csv"
E2_DEFAULT = REPO / "core" / "data" / "tv_exports" / "cme" / _E2_NAME
E1_DEFAULTS = (REPO / "core" / "data" / "tv_exports" / "cme" / _E1_OLD_NAME,
               REPO / "core" / "data" / "tv_exports" / "cme" / _E2_NAME)
FROZEN_TOKEN = "FROZEN"
REJECT_TOKENS = ("NOT FROZEN", "DRAFT")
_V7_RE = re.compile(r"[0-9a-f]{40}")


def prereg_status_line(path: Path) -> str | None:
    """The pre-registration's ``**Status:**`` line, or None if unreadable/absent."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError:
        return None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("**Status:**"):
            return s
    return None


def frozen_error(path) -> str | None:
    """None if the pre-registration status line records a freeze, else a reason."""
    line = prereg_status_line(path)
    if line is None:
        return (f"pre-registration {path} is missing or has no '**Status:**' "
                "line; Q-ORPREM-1 is not authorized to run")
    if FROZEN_TOKEN not in line:
        return (f"pre-registration status is not {FROZEN_TOKEN}: {line!r}; "
                "refusing (§7: not authorized by the draft)")
    if any(tok in line for tok in REJECT_TOKENS):
        return (f"pre-registration status line carries a not-frozen marker: "
                f"{line!r}; refusing")
    return None


def _sha256_file(path) -> str:
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _git_commit() -> str | None:
    """The commit this run executes at (§7 Phase 2 record), or None."""
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                             capture_output=True, text=True, timeout=30,
                             check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def v7_gate_error(gate: str | None) -> str | None:
    """None if the §7 Phase 2 v7 gate holds, else the refusal reason."""
    gate = (gate or "").strip()
    if gate.startswith("ruling:") and gate[len("ruling:"):].strip():
        return None
    if _V7_RE.fullmatch(gate.lower()):
        try:
            out = subprocess.run(["git", "merge-base", "--is-ancestor",
                                  gate.lower(), "HEAD"], cwd=REPO,
                                 capture_output=True, text=True, timeout=30,
                                 check=False)
        except (OSError, subprocess.SubprocessError) as exc:
            return f"cannot verify the v7 freeze commit: {exc}"
        if out.returncode == 0:
            return None
        return (f"v7 freeze commit {gate} is not an ancestor of HEAD "
                "(§7 Phase 2: scoring must descend from the recorded freeze)")
    return ("the §7 Phase 2 v7 gate is not recorded: pass --v7-gate with the "
            "40-hex v7 S4 freeze commit or 'ruling:<reference>'")


def _write_json(path: Path, payload: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str)
                    + "\n", encoding="utf-8")


def _gate_read(lad: dict, routing: str, decode_rate: float) -> dict:
    """Mechanical §6 read of the ladder (bounds only; the closure owns wording)."""
    if decode_rate is None or not math.isfinite(decode_rate) \
            or decode_rate < orprem.DECODE_RATE_MIN:
        return {"read": "VOID-PARITY (decode rate)", "primary": None,
                "feed_scoped": None, "label": "VOID-PARITY (decode rate)"}
    primary = "delta3" if routing == "width_matched" else "delta2"
    rung = lad["rungs"][primary]
    lo, hi = rung.get("lo"), rung.get("hi")
    d0 = lad["rungs"]["delta0"]["delta"]
    feed_scoped = not (math.isfinite(d0) and orprem.FEED_SCOPE_BAND[0] <= d0
                       <= orprem.FEED_SCOPE_BAND[1])
    if lo is not None and math.isfinite(lo) and lo > 0:
        read = "FALSIFIED"
    elif hi is not None and math.isfinite(hi) and hi < orprem.M_PREMIUM:
        read = "RESOLVED"
    else:
        read = "AMBIGUOUS-HOLD"
    label = read
    if primary == "delta2":
        label += " (width unmatched; primary Δ₂)"
    if feed_scoped:
        label += " [feed-scoped]"
    return {"read": read, "primary": primary, "feed_scoped": feed_scoped,
            "label": label}


def cmd_g0(args: argparse.Namespace) -> int:
    reason = frozen_error(args.prereg)
    if reason is not None:
        print(f"run_orprem g0: refusing: {reason}", file=sys.stderr)
        return 2
    e1 = list(args.e1_csv) if args.e1_csv else []
    rec = orprem.g0_record(args.e2_csv, e1)
    dates = [v["max_session_date"] for v in rec["inputs"].values()
             if v.get("max_session_date")]
    rec["max_session_date"] = max(dates) if dates else None
    rec["prereg"] = str(args.prereg)
    rec["prereg_sha256"] = _sha256_file(args.prereg)
    _write_json(args.out, rec)
    e2 = rec["panels"]["E2"]
    print(f"g0: wrote {args.out} (sessions={e2['n_sessions']}, "
          f"routing={e2['routing']}, max_session_date={e2['max_session_date']})")
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    reason = frozen_error(args.prereg)
    if reason is not None:
        print(f"run_orprem score: refusing: {reason}", file=sys.stderr)
        return 2
    gate_reason = v7_gate_error(args.v7_gate)
    if gate_reason is not None:
        print(f"run_orprem score: refusing: {gate_reason}", file=sys.stderr)
        return 2
    g0_path = Path(args.g0)
    g0 = json.loads(g0_path.read_text(encoding="utf-8"))
    engine = orprem._engine_sha256()
    if g0.get("orb_lib_sha256") != engine:
        print(f"run_orprem score: refusing: engine drift — G0 recorded "
              f"{g0.get('orb_lib_sha256')}, this harness runs {engine}",
              file=sys.stderr)
        return 2
    if "routing" not in g0["panels"]["E2"]:
        print("run_orprem score: refusing: G0 has no routing decision",
              file=sys.stderr)
        return 2
    routing = g0["panels"]["E2"]["routing"]
    band = tuple(g0["panels"]["E2"]["band"])
    cuts = tuple(g0["panels"]["E2"]["cuts"])

    if _sha256_file(args.e2_csv) != g0["inputs"]["e2"]["sha256"]:
        print("run_orprem score: refusing: the E2 input differs from the one "
              "G0 recorded", file=sys.stderr)
        return 2
    df, info = orprem.decode_export(args.e2_csv)
    elig = orprem.eligible_sessions(df, *orprem.PANEL_E2)
    lad = orprem.ladder(elig["sessions"], band=band, cuts=cuts,
                        block=args.block, n=args.boot_n, seed=args.seed)

    # §4.3 reported-only sensitivity of the primary rung: seeds 123/2026, block 10
    primary = "delta3" if routing == "width_matched" else "delta2"
    _, h_or, h_null, offsets, cost, weighted = next(
        r for r in orprem._RUNGS if r[0] == primary)
    sensitivity = {}
    for label, seed, block in ([(f"seed_{s}", s, args.block)
                                for s in orprem.BOOT_SEEDS_REPORTED]
                               + [(f"block_{orprem.BOOT_BLOCK_REPORTED}",
                                   args.seed, orprem.BOOT_BLOCK_REPORTED)]):
        b = orprem.bootstrap_delta(elig["sessions"], or_offsets=(orprem.W_OR,),
                                   null_offsets=offsets, H_or=h_or, H_null=h_null,
                                   cost_pt=cost, band=band, cuts=cuts,
                                   weighted=weighted, block=block,
                                   n=args.boot_n, seed=seed)
        sensitivity[label] = {"lo": b["lo"], "hi": b["hi"],
                              "seed": int(seed), "block": int(b["block"])}

    e1_report = None
    if args.e1_csv:
        if len(args.e1_csv) != 2:
            print("run_orprem score: refusing: E1 needs exactly two files "
                  "(86a38 then dd9d8)", file=sys.stderr)
            return 2
        g0_e1 = g0["panels"].get("E1")
        if not g0_e1 or not g0_e1.get("overlap_ok"):
            e1_report = {"dropped": "G0 E1 overlap check failed or absent (§6)"}
        elif [_sha256_file(p) for p in args.e1_csv] != [
                g0["inputs"]["e1_0"]["sha256"], g0["inputs"]["e1_1"]["sha256"]]:
            print("run_orprem score: refusing: the E1 inputs differ from the "
                  "ones G0 recorded", file=sys.stderr)
            return 2
        else:
            d_a, _ = orprem.decode_export(args.e1_csv[0])
            d_b, _ = orprem.decode_export(args.e1_csv[1])
            blended = orprem._blend_e1(d_a, d_b)
            el1 = orprem.eligible_sessions(blended, *orprem.PANEL_E1)
            or1 = [rec for s in el1["sessions"]
                   for rec in orprem.score_session(s, (orprem.W_OR,),
                                                   orprem.H_PRIMARY)]
            nu1 = [rec for s in el1["sessions"]
                   for rec in orprem.score_session(s, orprem.W_NULL_D2,
                                                   orprem.H_PRIMARY)]
            e1_report = orprem.delta3(or1, nu1, band, cuts)
            e1_report["n_sessions"] = len(el1["sessions"])

    record = {
        "phase": "score",
        "prereg": str(args.prereg),
        "prereg_sha256": _sha256_file(args.prereg),
        "v7_gate": args.v7_gate.strip(),
        "sensitivity": sensitivity,
        "g0": str(g0_path),
        "g0_sha256": _sha256_file(g0_path),
        "inputs": {"e2": info},
        "orb_lib_sha256": engine,
        "code_commit": _git_commit(),
        "seed": int(args.seed),
        "block": int(args.block),
        "n_boot": int(args.boot_n),
        "max_session_date": info["max_session_date"],
        "decode_rate": info["decode_rate"],
        "routing": routing,
        "n_sessions": len(elig["sessions"]),
        "ladder": lad,
        "e1_report": e1_report,
        "gate_read": _gate_read(lad, routing, info["decode_rate"]),
    }
    out = Path(args.out) if args.out else (
        CAMP / "run_records"
        / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") / "record.json")
    _write_json(out, record)
    print(f"score: wrote {out} (gate_read={record['gate_read']['label']})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="run_orprem.py",
        description="Q-ORPREM-1 g0/score CLI. Refuses with exit code 2 unless "
                    "the pre-registration status line is FROZEN (and, for "
                    "score, the v7 gate commit is recorded).")
    sub = p.add_subparsers(dest="command", required=True)

    g0 = sub.add_parser("g0", help="Phase 1 blind pre-flight (prices only, no R)")
    g0.add_argument("--prereg", type=Path, default=PREREG_DEFAULT,
                    help="pre-registration markdown (default: the Q-ORPREM-1 draft)")
    g0.add_argument("--e2-csv", type=Path, default=E2_DEFAULT,
                    help="E2 export (dd9d8). Default is the primary-checkout path.")
    g0.add_argument("--e1-csv", type=Path, action="append", default=None,
                    help="E1 export; pass twice (86a38, then dd9d8). "
                         "Omit to skip the E1 section.")
    g0.add_argument("--out", type=Path, default=CAMP / "G0.json",
                    help="G0 record destination (default: camp G0.json)")
    g0.set_defaults(func=cmd_g0)

    sc = sub.add_parser("score", help="Phase 2 one scoring run (v7-gated)")
    sc.add_argument("--prereg", type=Path, default=PREREG_DEFAULT)
    sc.add_argument("--e2-csv", type=Path, default=E2_DEFAULT)
    sc.add_argument("--e1-csv", type=Path, action="append", default=None,
                    help="E1 exports (86a38, then dd9d8); optional report-only arm")
    sc.add_argument("--g0", type=Path, default=CAMP / "G0.json",
                    help="the committed G0 record (band/cutpoints/routing source)")
    sc.add_argument("--v7-gate", default=None,
                    help="§7 Phase 2 gate: the 40-hex v7 S4 freeze commit "
                         "(must be an ancestor of HEAD) or 'ruling:<reference>'")
    sc.add_argument("--seed", type=int, default=orprem.BOOT_SEED,
                    help=f"bootstrap seed (frozen default {orprem.BOOT_SEED})")
    sc.add_argument("--boot-n", type=int, default=orprem.BOOT_N,
                    help=f"bootstrap replicates (frozen default {orprem.BOOT_N}; "
                         "smaller values are for synthetic dry runs only)")
    sc.add_argument("--block", type=int, default=orprem.BOOT_BLOCK,
                    help=f"bootstrap block length (frozen default {orprem.BOOT_BLOCK})")
    sc.add_argument("--out", type=Path, default=None,
                    help="record destination (default: camp run_records/<ts>/record.json)")
    sc.set_defaults(func=cmd_score)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (OSError, ValueError, KeyError) as exc:
        print(f"run_orprem {args.command}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
