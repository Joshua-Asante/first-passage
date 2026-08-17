"""Stage-2 GENEROUS falsifier for MNQ-SIZEDIV-1 (DESIGN_FREEZE §4, F1-F4).

Outcome-coupled on TRAIN-side data ONLY (trades semester 2023-08-14..2024-02-14;
slot returns from the M15 panel). Committed BEFORE the semester data lands.

Pairing rule (frozen): conditioning session s pairs with the immediately next
FULL session in the panel calendar (weekends/holidays skipped, no max-gap).
Hit = strictly positive signed slot return. Base rate = majority sign share of
the same slot-return set. KILLs are generous: failure conclusive; PASS is a
spend license only (~36% false-go at this n, disclosed in the freeze).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from sizediv_lib import combine_stats, load_slot_returns, session_stats, sizediv  # noqa: E402

try:
    import databento as db
except ImportError:  # scorer stays importable/testable without the vendor lib
    db = None

PANEL_DEFAULT = r"C:\Users\joshu\multi_firm_operations\core\data\bar_data\MNQ_M15.csv"
CACHE_DEFAULT = Path.home() / ".databento_cache" / "mnq_sizediv_blind_2026-08" / "train_sem"
CHUNK = 5_000_000

# FROZEN F-rules (DESIGN_FREEZE §4); bp thresholds on the Tradeify RT basis.
RT_BP = 0.911
F1_KILL_MEAN_BP = 1.0 * RT_BP          # mean signed gross <= 1xRT -> KILL
PASS_MEAN_BP = 2.0 * RT_BP             # mean >= 2xRT (and no KILL) -> PASS
F3_RELABEL_CORR = 0.5
BOOT_N = 2_000
BOOT_SEED = 20260815


def iter_chunks(path: Path):
    if db is None:
        sys.exit("databento not installed (research venv required).")
    store = db.DBNStore.from_file(path)
    try:
        it = store.to_df(count=CHUNK)
    except TypeError:
        yield store.to_df()
        return
    if isinstance(it, pd.DataFrame):
        yield it
        return
    for chunk in it:
        yield chunk


def build_trades_stats(cache_dir: str | Path) -> pd.DataFrame:
    files = sorted(Path(cache_dir).rglob("*.dbn*"))
    files = [f for f in files if f.suffix != ".json" and "metadata" not in f.name]
    if not files:
        sys.exit(f"no DBN files under {cache_dir}")
    parts = []
    for f in files:
        for chunk in iter_chunks(f):
            parts.append(session_stats(chunk))
        print(f"[f2] {f.name} done", flush=True)
    return sizediv(combine_stats(parts))


def pair_and_score(stats: pd.DataFrame, slots: pd.DataFrame) -> pd.DataFrame:
    """One row per TRADE: date s, paired next full session, direction, signed bp."""
    full_dates = sorted(slots["date"])
    nxt = {d: full_dates[i + 1] for i, d in enumerate(full_dates[:-1])}
    sl = slots.set_index("date")
    rows = []
    for _, r in stats.iterrows():
        d = r["date"]
        a = r["A"]
        if pd.isna(a) or a == 0 or d not in nxt:
            continue
        tgt = nxt[d]
        direction = 1.0 if a > 0 else -1.0
        for slot, ret in (("s1", sl.loc[tgt, "r1_bp"]), ("s2", sl.loc[tgt, "r2_bp"])):
            rows.append(dict(cond_date=d, exec_date=tgt, slot=slot, A=a,
                             direction=direction, ret_bp=ret, signed_bp=direction * ret))
    return pd.DataFrame(rows)


def block_bootstrap_ci(trades: pd.DataFrame, n_boot: int = BOOT_N, seed: int = BOOT_SEED):
    """Session-block bootstrap on mean signed bp (blocks = exec_date)."""
    rng = np.random.default_rng(seed)
    blocks = [g["signed_bp"].to_numpy() for _, g in trades.groupby("exec_date")]
    nb = len(blocks)
    means = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, nb, nb)
        means[i] = np.concatenate([blocks[j] for j in idx]).mean()
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def score(stats: pd.DataFrame, slots: pd.DataFrame) -> dict:
    trades = pair_and_score(stats, slots)
    n = len(trades)
    mean_bp = float(trades["signed_bp"].mean())
    hit = float((trades["signed_bp"] > 0).mean())
    pos = float((trades["ret_bp"] > 0).mean())
    base = max(pos, 1 - pos)

    # F3 relabel: sign(A(s)) vs sign(same-session full-day return R(s) = r1+r2)
    sl = slots.set_index("date")
    same = stats[stats["date"].isin(sl.index) & stats["A"].notna() & (stats["A"] != 0)].copy()
    r_same = (sl.loc[same["date"], "r1_bp"].to_numpy() + sl.loc[same["date"], "r2_bp"].to_numpy())
    relabel_corr = float(np.corrcoef(np.sign(same["A"].to_numpy()), np.sign(r_same))[0, 1]) \
        if len(same) > 2 else np.nan

    lo, hi = block_bootstrap_ci(trades) if n else (np.nan, np.nan)

    f1 = mean_bp <= F1_KILL_MEAN_BP
    f2 = hit <= base
    f3 = abs(relabel_corr) >= F3_RELABEL_CORR if not np.isnan(relabel_corr) else False
    if f1 or f2 or f3:
        verdict = "KILL"
    elif mean_bp >= PASS_MEAN_BP:
        verdict = "PASS"
    else:
        verdict = "HOLD"
    return dict(n_trades=n, n_sessions=trades["exec_date"].nunique() if n else 0,
                mean_signed_bp=mean_bp, hit_rate=hit, base_rate=base,
                relabel_corr=relabel_corr, ci_lo=lo, ci_hi=hi,
                f1_kill=f1, f2_kill=f2, f3_kill=f3, verdict=verdict, trades=trades)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-dir", default=str(CACHE_DEFAULT))
    ap.add_argument("--panel", default=PANEL_DEFAULT)
    ap.add_argument("--out", default=str(Path(__file__).parent / "STAGE2_FALSIFIER.md"))
    args = ap.parse_args()

    stats = build_trades_stats(args.cache_dir)
    slots = load_slot_returns(args.panel)
    res = score(stats, slots)
    t = res.pop("trades")
    t.to_csv(Path(__file__).parent / "stage2_trades.csv", index=False)

    lines = [
        "# MNQ-SIZEDIV-1 — STAGE2_FALSIFIER (TRAIN semester; outcome-coupled)",
        "",
        f"**Run:** {pd.Timestamp.now(tz='UTC').isoformat(timespec='seconds')} · cache `{args.cache_dir}` · panel `{args.panel}`",
        "",
        "| Metric | Value | Frozen rule | Fired |",
        "|---|---|---|---|",
        f"| n trades / exec sessions | {res['n_trades']} / {res['n_sessions']} | — | — |",
        f"| mean signed gross (bp) | {res['mean_signed_bp']:+.4f} | F1 KILL if ≤ +{F1_KILL_MEAN_BP:.3f} | {res['f1_kill']} |",
        f"| hit rate vs base | {res['hit_rate']:.4f} vs {res['base_rate']:.4f} | F2 KILL if ≤ base | {res['f2_kill']} |",
        f"| relabel corr sign(A) vs sign(R_s) | {res['relabel_corr']:+.4f} | F3 KILL if \\|·\\| ≥ {F3_RELABEL_CORR} | {res['f3_kill']} |",
        f"| session-block 95% CI (bp) | [{res['ci_lo']:+.3f}, {res['ci_hi']:+.3f}] | F4 report | — |",
        "",
        f"**Verdict: `{res['verdict']}`** (PASS ≥ +{PASS_MEAN_BP:.3f} bp; HOLD ∈ (+{F1_KILL_MEAN_BP:.3f}, +{PASS_MEAN_BP:.3f}]; else KILL)",
        "",
        "PASS is a spend license only (~36% false-go at this n — FREEZE §4); the battery is the evidence standard.",
        "",
    ]
    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"[f2] verdict={res['verdict']} mean={res['mean_signed_bp']:+.3f}bp "
          f"hit={res['hit_rate']:.3f}/{res['base_rate']:.3f} -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
