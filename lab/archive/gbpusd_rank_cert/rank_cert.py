"""Representative-window rank-ρ certification — CONCEPT-GBPUSD-VBR-001 pre-filter.

Context (SESSIONS.md 2026-06-07 "High-level code review + parity-gate"): the
ADR 2026-06-05-sweep-engine §4 rank-correlation falsifier came back ρ=0.714 on
the matched-feed window — sitting ON the 0.70 floor with 2-6 trades/config, so
the pre-filter's rank authority is UNCERTIFIED (not failed). The matched-feed
requirement (TV chart-OHLC export, bar-capped) caps that window to ~weeks —
too thin to rank a low-frequency strategy. This driver executes the candidate
cert path designed there:

* **Native side** — full backtest window (2018-01-01 → 2024-01-01) via the TV
  Strategy Tester (NOT bar-capped; the 894-trade 2018-2024 cfg00 export proves
  it), charted on TV's OANDA feed, exported per config.
* **Python side** — the full-window OANDA REST feed
  (``core/data/bar_data/GBPUSD_M15.csv``).
* **Cross-feed, by design.** Exact anchor parity is unattainable cross-feed
  (feedback memory ``parity_gate_feed_and_pf_calibration``: symmetric gross
  drop), but the §4 falsifier only needs config *ordering* to agree — rank-ρ
  is robust to a roughly-uniform feed offset. Stability of ρ (leave-one-out,
  time-split halves, both score axes) is the evidence that the reading is not
  a small-n accident like the 0.714.

Scope guard (load-bearing): this run certifies (or revokes, per ADR §4) the
PRE-FILTER's rank authority ONLY. It does NOT substitute for the same-feed
anchor parity that ``runner.run_sweep``'s ``_emit_guard`` hard-requires before
an authoritative trial-set emit — that gate is untouched. The pre-registered
floor (``PREFILTER_RANK_RHO_FLOOR = 0.70``) is consumed verbatim; the
stability diagnostics are disposition INPUTS for the human read, not new gates
(no threshold invented here — ADR §5 #3).

Sample-size rationale (why n=12, the ``parity_run`` CLI default): under H0
(no rank agreement) the one-sided 5% critical value for Spearman ρ is ≈0.829
at n=6 — ABOVE the 0.70 floor, so a passing reading at n=6 is indistinguishable
from noise (the 2026-06-07 lesson). At n=12 it is ≈0.50 — below the floor, so
clearing 0.70 means something. cfg00-05 of the n=12/seed=0 sample are
byte-identical to the prior runbook's (deterministic-prefix property of
``make_config_sample``, asserted at runtime), so config identities carry over.

Usage (paths live in the MAIN checkout's gitignored data trees):

    python lab/analysis/gbpusd_rank_cert/rank_cert.py prepare \
        --concept lab/validation/concept_intake/concepts/CONCEPT-GBPUSD-VBR-001.yaml \
        --sidecar core/strategies/candidates/concept-gbpusd-vbr-001.sweep.bounded.yaml \
        --candidate-pine core/strategies/candidates/concept-gbpusd-vbr-001.pine \
        --feed core/data/bar_data/GBPUSD_M15.csv \
        --out-dir core/data/tv_exports/candidates/concept-gbpusd-vbr-001/full_2018_2024 \
        [--anchor-csv <existing full-window cfg00 export>]

    python lab/analysis/gbpusd_rank_cert/rank_cert.py verdict \
        --concept ... --sidecar ... --feed ... \
        --native-dir core/data/tv_exports/candidates/concept-gbpusd-vbr-001/full_2018_2024
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np

_REPO_ROOT = Path(__file__).resolve().parents[3]   # lab/analysis/gbpusd_rank_cert/ -> repo root
for _p in (_REPO_ROOT / "lab", _REPO_ROOT / "core"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from validation.sweep import PREFILTER_RANK_RHO_FLOOR  # noqa: E402
from validation.sweep import grid as _grid  # noqa: E402
from validation.sweep.engine import PythonPrefilterEngine  # noqa: E402
from validation.sweep.parity import parity_check, rank_correlation_falsifier  # noqa: E402
from validation.sweep.parity_run import (  # noqa: E402
    config_csv_name,
    ingest_native_exports,
    make_config_sample,
)

# The 9 SIGNAL-group tunables the sweep grid varies (sidecar params). Order is
# cosmetic (runbook display); membership must cover every key in a grid config.
SIGNAL_PARAMS = (
    "fastLen", "slowLen", "useSession", "atrLength", "atrMaLength",
    "atrExpansion", "exitAtrLength", "stopAtr", "tpAtr",
)

WINDOW_START = "2018-01-01"
WINDOW_END = "2024-01-01"
SPLIT_DEFAULT = "2021-01-01"   # time-split midpoint for the ρ-stability halves


# ── per-config Pine baking (kills the config-identity trap) ──────────────────

def _pine_literal(v) -> str:
    """Python config value -> Pine source literal."""
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def _replace_input_default(text: str, name: str, value) -> str:
    """Replace the default literal in ``<name> = input.<type>(<default>, ...``."""
    pat = re.compile(
        rf"^(?P<head>\s*{re.escape(name)}\s*=\s*input\.(?:int|float|bool)\()"
        rf"(?P<default>[^,]+)(?P<tail>,)",
        re.MULTILINE,
    )
    new, n = pat.subn(lambda m: m["head"] + _pine_literal(value) + m["tail"], text)
    if n != 1:
        raise ValueError(f"input default for {name!r}: expected exactly 1 match, got {n}")
    return new


def _replace_date_input(text: str, name: str, date: str) -> str:
    """Replace the timestamp literal in ``<name> = input.time(timestamp("...")``."""
    pat = re.compile(
        rf"^(?P<head>\s*{re.escape(name)}\s*=\s*input\.time\(timestamp\(\")"
        rf"(?P<date>[^\"]+)(?P<tail>\"\))",
        re.MULTILINE,
    )
    new, n = pat.subn(lambda m: m["head"] + date + m["tail"], text)
    if n != 1:
        raise ValueError(f"date input {name!r}: expected exactly 1 match, got {n}")
    return new


def _extract_input_default(text: str, name: str) -> str:
    m = re.search(
        rf"^\s*{re.escape(name)}\s*=\s*input\.(?:int|float|bool)\((?P<default>[^,]+),",
        text, re.MULTILINE,
    )
    if not m:
        raise ValueError(f"could not re-extract input default for {name!r}")
    return m["default"].strip()


def bake_cfg_pine(
    candidate_text: str, cfg: dict, *, index: int, candidate_id: str,
    start: str = WINDOW_START, end: str = WINDOW_END,
) -> str:
    """Bake one config's input.* defaults + the cert window into the candidate Pine.

    Paste-and-run: the operator never sets inputs by hand (the 2026-06-07
    config-identity trap — Pine defaults backtested a different strategy).
    Self-verifies by re-extracting every baked default and comparing.
    """
    text = candidate_text
    for k in cfg:
        if k not in SIGNAL_PARAMS:
            raise ValueError(f"config key {k!r} is not a known SIGNAL param")
        text = _replace_input_default(text, k, cfg[k])
    text = _replace_date_input(text, "startDate", start)
    text = _replace_date_input(text, "endDate", end)

    # Self-verify: every baked default must read back as the cfg value.
    for k, v in cfg.items():
        got = _extract_input_default(text, k)
        want = _pine_literal(v)
        if isinstance(v, bool):
            ok = got == want
        else:
            ok = float(got) == float(v)
        if not ok:
            raise ValueError(f"bake self-check failed for {k}: baked {got!r} != cfg {want!r}")

    params = " ".join(f"{k}={_pine_literal(cfg[k])}" for k in SIGNAL_PARAMS if k in cfg)
    tz_line = (
        "// >>> useSession=TRUE -> SET TV CHART TIMEZONE TO UTC before running (session-filter parity).\n"
        if cfg.get("useSession") else ""
    )
    header = (
        f"// >>> RANK-ρ CERT (representative window) cfg{index:02d} | {params}\n"
        f"// >>> Chart OANDA:GBPUSD M15 (TV's OANDA feed — same broker as the REST python feed).\n"
        f"// >>> Window {start}..{end} BAKED into Start/End Date inputs — do not change any input.\n"
        f"{tz_line}"
        f"// >>> CROSS-FEED rank run: exact trade-count/net parity NOT expected; config RANKING is the instrument.\n"
        f"// >>> Backtest Mode stays ON (default). Strategy Tester -> List of Trades -> Export\n"
        f"// >>>   -> save as {config_csv_name(candidate_id, index)}\n"
    )
    lines = text.splitlines(keepends=True)
    if not lines or not lines[0].startswith("//@version"):
        raise ValueError("candidate Pine must start with a //@version line")
    return lines[0] + header + "".join(lines[1:])


# ── scoring (mirrors parity_run.sharpe_score; adds per-half stability cuts) ───

def _sharpe(returns: np.ndarray) -> float | None:
    r = np.asarray(returns, dtype=float)
    if len(r) < 2:
        return None
    s = r.std(ddof=1)
    return float(r.mean() / s) if s > 0 else 0.0


def score_block(result, split: str) -> dict:
    """Full-window + per-half scores for one EngineRunResult."""
    cut = np.datetime64(split)
    entry = np.asarray(result.entry_times)
    halves = {}
    for label, mask in (("h1", entry < cut), ("h2", entry >= cut)):
        r = np.asarray(result.returns, dtype=float)[mask]
        p = np.asarray(result.pnl, dtype=float)[mask]
        halves[label] = {
            "n_trades": int(mask.sum()),
            "net_profit": float(p.sum()),
            "sharpe": _sharpe(r),
        }
    return {
        "n_trades": int(result.n_trades),
        "net_profit": float(result.metrics["net_profit"]),
        "profit_factor": float(result.metrics["profit_factor"]),
        "sharpe": _sharpe(result.returns),
        **halves,
    }


def _sample_configs(sidecar: str, n: int, seed: int) -> list[dict]:
    grid = _grid.expand_grid(sidecar, max_configs=200_000)
    sample = make_config_sample(grid, n=n, seed=seed)
    # Deterministic-prefix property: the prior runbook's cfg00-05 identities
    # must carry over unchanged (the native cfg00 export is reused as-is).
    if n >= 6:
        prior = make_config_sample(grid, n=6, seed=seed)
        if sample[:6] != prior:
            raise AssertionError(
                "n=12 sample no longer prefix-matches the n=6 runbook sample — "
                "config identities broken; do NOT reuse existing native exports."
            )
    return sample


def _spec(concept_path: str):
    from codification.compose import candidate_spec_from_hint
    from validation.concept_intake.schema import load_concept
    c = load_concept(concept_path)
    return candidate_spec_from_hint(c.concept_id, c.field_text("logic_family_hint")), c.concept_id


# ── prepare: stage python-side scores + bake pines + write the runbook ────────

def cmd_prepare(args) -> int:
    spec, cid = _spec(args.concept)
    configs = _sample_configs(args.sidecar, args.n, args.seed)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    from validation.sweep.feed_loader import load_bar_feed
    feed = load_bar_feed(args.feed)
    engine = PythonPrefilterEngine()
    py = []
    for i, cfg in enumerate(configs):
        res = engine.run(spec, cfg, feed)
        block = {"index": i, "config": cfg, **score_block(res, args.split)}
        py.append(block)
        print(f"cfg{i:02d}: n={block['n_trades']:4d}  net={block['net_profit']:12.2f}  "
              f"pf={block['profit_factor']:.3f}  sharpe={block['sharpe']}")

    staged = {
        "candidate_id": cid,
        "feed": str(args.feed),
        "feed_source": feed.source,
        "n_bars": int(feed.n_bars),
        "window": {"start": WINDOW_START, "end": WINDOW_END, "split": args.split},
        "n_sample": len(configs),
        "seed": args.seed,
        "score_axis": "sharpe (harness IS-best selection metric); net_profit secondary",
        "py_scores": py,
    }
    scores_path = out_dir / "py_scores.json"
    scores_path.write_text(json.dumps(staged, indent=2), encoding="utf-8")
    print(f"\nstaged python-side scores: {scores_path}")

    candidate_text = Path(args.candidate_pine).read_text(encoding="utf-8")
    for i, cfg in enumerate(configs):
        if i == 0 and args.anchor_csv:
            continue  # anchor native export supplied; no pine needed for cfg00
        baked = bake_cfg_pine(candidate_text, cfg, index=i, candidate_id=cid)
        p = out_dir / f"{cid}__cfg{i:02d}.pine"
        p.write_text(baked, encoding="utf-8")
    print(f"baked per-config pine files -> {out_dir}")

    if args.anchor_csv:
        dst = out_dir / config_csv_name(cid, 0)
        if Path(args.anchor_csv).resolve() != dst.resolve():
            shutil.copyfile(args.anchor_csv, dst)
        print(f"anchor (cfg00) native export seeded: {dst}")

    _write_runbook(cid, configs, out_dir, anchor_seeded=bool(args.anchor_csv))
    print(f"runbook: {out_dir / 'RANK_CERT_RUNBOOK.md'}")
    return 0


def _write_runbook(cid: str, configs: list[dict], out_dir: Path, *, anchor_seeded: bool) -> None:
    lines = [
        f"# Representative-window rank-ρ cert runbook — `{cid}`",
        "",
        "_Generated by `lab/analysis/gbpusd_rank_cert/rank_cert.py`. Executes the",
        "cert path from SESSIONS.md 2026-06-07: full-window native Strategy-Tester",
        "runs vs the full-window REST python feed; CROSS-FEED by design — the §4",
        "falsifier needs config ORDERING, not exact P&L (rank-ρ is offset-robust)._",
        "",
        "## Discipline (differs from the matched-window B5 runbook)",
        "- Chart **OANDA:GBPUSD M15** (TV's OANDA feed — same broker as the python",
        "  REST feed, minimizing the cross-feed offset).",
        "- **Set the TV chart timezone to UTC** once, before any run (the",
        "  `useSession=true` configs gate on UTC bar-hours; harmless for the rest).",
        f"- Window **{WINDOW_START} → {WINDOW_END}** is BAKED into each pine's",
        "  Start/End Date inputs. Make sure the chart has history back to 2018",
        "  (scroll back / load more bars) so the Strategy Tester covers the window.",
        "- Each cfg pine below has ALL inputs baked — **paste and run, change",
        "  nothing** (kills the config-identity trap). `Backtest Mode` stays ON.",
        "- Exact trade-count / net parity vs python is NOT expected here (cross-",
        "  feed). Do not abort on a count mismatch; the verdict ranks.",
        "",
        "## Runs",
    ]
    for i, _cfg in enumerate(configs):
        csv = out_dir / config_csv_name(cid, i)
        if i == 0 and anchor_seeded:
            lines.append(f"- cfg00 — **already seeded** from the 2026-06-06 full-window export (`{csv.name}`). No run needed.")
            continue
        lines.append(f"- cfg{i:02d} — paste `{cid}__cfg{i:02d}.pine`, run, export List of Trades -> `{csv.name}`")
    lines += [
        "",
        "Partial progress is fine: the verdict pairs whatever exports are present",
        "(>=2 required for a ρ; the full n=12 makes the 0.70 floor discriminating —",
        "the one-sided 5% noise threshold is ≈0.83 at n=6 but ≈0.50 at n=12).",
        "",
        "## Verdict",
        "```",
        "python lab/analysis/gbpusd_rank_cert/rank_cert.py verdict \\",
        "    --concept lab/validation/concept_intake/concepts/CONCEPT-GBPUSD-VBR-001.yaml \\",
        "    --sidecar core/strategies/candidates/concept-gbpusd-vbr-001.sweep.bounded.yaml \\",
        "    --feed core/data/bar_data/GBPUSD_M15.csv \\",
        f"    --native-dir {out_dir}",
        "```",
        "- ρ ≥ 0.70 (pre-registered floor) + stable diagnostics → pre-filter rank",
        "  authority CERTIFIED on the representative window (record in SESSIONS +",
        "  programme-audit input).",
        "- ρ < 0.70 on the full sample → ADR §4: revert to native-only for this",
        "  family; record in the ADR.",
        "- Scope: this does NOT replace same-feed anchor parity in",
        "  `runner.run_sweep`'s `_emit_guard` (authoritative emits unchanged).",
    ]
    (out_dir / "RANK_CERT_RUNBOOK.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── verdict: pair native exports, ρ + stability diagnostics ──────────────────

def _scores_vector(blocks: list[dict], axis: str) -> np.ndarray:
    return np.array([b[axis] for b in blocks], dtype=float)


def cmd_verdict(args) -> int:
    spec, cid = _spec(args.concept)
    configs = _sample_configs(args.sidecar, args.n, args.seed)
    native_dir = Path(args.native_dir)

    from validation.sweep.feed_loader import load_bar_feed
    feed = load_bar_feed(args.feed)
    engine = PythonPrefilterEngine()

    native_results, missing = ingest_native_exports(
        configs, native_dir, cid, strategy_key=args.strategy_key,
    )

    # Python side — recompute, and cross-check against the staged py_scores.json
    # (a mismatch means the feed file changed since prepare; flag, don't hide).
    py_blocks, nat_blocks, paired, unrankable = [], [], [], []
    for i, (cfg, nat) in enumerate(zip(configs, native_results)):
        res = engine.run(spec, cfg, feed)
        pb = score_block(res, args.split)
        py_blocks.append(pb)
        if nat is None:
            continue
        nb = score_block(nat, args.split)
        # A config with <2 trades on either side has no Sharpe — it cannot be
        # ranked. Exclude EXPLICITLY (never as a silent NaN in the ρ).
        if pb["sharpe"] is None or nb["sharpe"] is None:
            unrankable.append(i)
            continue
        nat_blocks.append(nb)
        paired.append(i)

    staged_path = native_dir / "py_scores.json"
    staged_note = ""
    if staged_path.exists():
        staged = json.loads(staged_path.read_text(encoding="utf-8"))
        drift = [
            f"cfg{i:02d}" for i, b in enumerate(staged.get("py_scores", []))
            if i < len(py_blocks) and (
                b["n_trades"] != py_blocks[i]["n_trades"]
                or abs(b["net_profit"] - py_blocks[i]["net_profit"]) > 1e-6
            )
        ]
        staged_note = (
            f"PY-SCORE DRIFT vs staged py_scores.json: {drift} — feed changed since prepare?"
            if drift else "python side matches staged py_scores.json"
        )

    out: dict = {
        "candidate_id": cid,
        "feed_source": feed.source,
        "window": {"start": WINDOW_START, "end": WINDOW_END, "split": args.split},
        "n_sample": len(configs),
        "n_paired": len(paired),
        "paired_indices": paired,
        "missing_indices": missing,
        "unrankable_indices": unrankable,
        "staged_check": staged_note,
        "scope_note": (
            "Certifies/revokes ADR §4 pre-filter rank authority on the representative "
            "window ONLY. Cross-feed: anchor parity is informational here and does NOT "
            "satisfy runner._emit_guard's same-feed anchor-parity precondition."
        ),
        "per_config": [
            {
                "index": i,
                "config": configs[i],
                "py": py_blocks[i],
                "native": nat_blocks[paired.index(i)] if i in paired else None,
            }
            for i in range(len(configs))
        ],
    }

    # Informational cross-feed anchor comparison (expected: count/net off-band).
    if native_results and native_results[0] is not None:
        anchor = parity_check(engine.run(spec, configs[0], feed), native_results[0])
        out["anchor_cross_feed_info"] = {
            "passed_strict_band": anchor.passed,
            "reason": anchor.reason,
            "detail": anchor.detail,
        }

    if len(paired) < 2:
        out["verdict"] = "PENDING"
        out["note"] = f"need >=2 paired native exports for a ρ; have {len(paired)}."
        _emit(out, native_dir, args.out)
        return 0

    py_paired = [py_blocks[i] for i in paired]
    primary = rank_correlation_falsifier(
        _scores_vector(py_paired, "sharpe"), _scores_vector(nat_blocks, "sharpe"),
    )
    rho_net = rank_correlation_falsifier(
        _scores_vector(py_paired, "net_profit"), _scores_vector(nat_blocks, "net_profit"),
    )

    # Stability diagnostics (disposition inputs, NOT gates).
    loo = []
    if len(paired) >= 3:
        for drop in range(len(paired)):
            keep = [j for j in range(len(paired)) if j != drop]
            loo.append({
                "dropped_index": paired[drop],
                "rho": rank_correlation_falsifier(
                    _scores_vector([py_paired[j] for j in keep], "sharpe"),
                    _scores_vector([nat_blocks[j] for j in keep], "sharpe"),
                ).rho,
            })

    halves = {}
    for h in ("h1", "h2"):
        ok = [
            j for j in range(len(paired))
            if py_paired[j][h]["sharpe"] is not None and nat_blocks[j][h]["sharpe"] is not None
        ]
        if len(ok) >= 2:
            halves[h] = {
                "n_paired": len(ok),
                "dropped": [paired[j] for j in range(len(paired)) if j not in ok],
                "rho": rank_correlation_falsifier(
                    np.array([py_paired[j][h]["sharpe"] for j in ok]),
                    np.array([nat_blocks[j][h]["sharpe"] for j in ok]),
                ).rho,
            }
        else:
            halves[h] = {"n_paired": len(ok), "rho": None,
                         "note": "fewer than 2 configs with >=2 trades in this half on both sides"}

    py_sharpes = _scores_vector(py_paired, "sharpe")
    ties = [
        (paired[a], paired[b])
        for a in range(len(paired)) for b in range(a + 1, len(paired))
        if py_sharpes[a] == py_sharpes[b]
    ]

    out["rank_falsifier"] = {
        "rho": primary.rho, "floor": primary.floor, "passed": primary.passed,
        "n_configs": primary.n_configs, "reason": primary.reason,
    }
    out["diagnostics"] = {
        "rho_net_axis": rho_net.rho,
        "leave_one_out": loo,
        "loo_min": min((d["rho"] for d in loo), default=None),
        "loo_max": max((d["rho"] for d in loo), default=None),
        "time_split_halves": halves,
        "py_score_ties": ties,
        "min_trades_per_config_py": int(min(b["n_trades"] for b in py_paired)),
        "min_trades_per_config_native": int(min(b["n_trades"] for b in nat_blocks)),
    }
    out["verdict"] = (
        ("PASS" if primary.passed else "FAIL")
        + ("" if len(paired) == len(configs) else f" (partial: {len(paired)}/{len(configs)} paired)")
    )
    _emit(out, native_dir, args.out)
    return 0


def _emit(payload: dict, native_dir: Path, out_arg: str | None) -> None:
    print(json.dumps(payload, indent=2, default=str))
    print(f"\nVERDICT: {payload['verdict']}")
    target = Path(out_arg) if out_arg else native_dir / "rank_cert_verdict.json"
    target.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(f"written: {target}")


# ── CLI ──────────────────────────────────────────────────────────────────────

def _main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Representative-window rank-ρ cert driver.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--concept", required=True, help="concept YAML (id + logic_family_hint)")
    common.add_argument("--sidecar", required=True, help="bounded sweep sidecar")
    common.add_argument("--feed", required=True, help="full-window REST bar CSV")
    common.add_argument("--n", type=int, default=12, help="config-sample size (anchor + n-1)")
    common.add_argument("--seed", type=int, default=0)
    common.add_argument("--split", default=SPLIT_DEFAULT, help="time-split boundary for ρ-stability halves")

    pp = sub.add_parser("prepare", parents=[common],
                        help="stage python-side scores; bake per-config pines + runbook")
    pp.add_argument("--candidate-pine", required=True)
    pp.add_argument("--out-dir", required=True)
    pp.add_argument("--anchor-csv", default=None,
                    help="existing full-window cfg00 native export to seed into out-dir")

    vr = sub.add_parser("verdict", parents=[common], help="pair native exports; ρ + stability")
    vr.add_argument("--native-dir", required=True)
    vr.add_argument("--strategy-key", default="striker")
    vr.add_argument("--out", default=None)

    args = ap.parse_args(argv)
    return cmd_prepare(args) if args.cmd == "prepare" else cmd_verdict(args)


if __name__ == "__main__":
    raise SystemExit(_main())
