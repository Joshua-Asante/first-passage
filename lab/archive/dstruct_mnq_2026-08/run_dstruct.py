"""H-DSTRUCT-MNQ-1 — daily structural bias at its own granularity (Tier-1 screen).

Frozen design: PREREG_DSTRUCT.md (same directory), committed before this ran.
Object: b_d = sign(close_{d-1} - EMA20(close)_{d-1}) on CME session-day daily closes;
verdict cell y_d = sign(rth_close_d - rth_open_d) (RTH open->close, the E1-deployable
granularity); disclosure cell = session close-to-close.
Panel: cached _mnq_15m.pkl (primary checkout), truncated to session-day <= 2026-07-15.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ORB_LIB_DIR = ROOT / "lab" / "analysis" / "orb" / "orb_universe_2026-06-22"
sys.path.insert(0, str(ORB_LIB_DIR))
import orb_lib as ol  # noqa: E402

PKL = Path(r"C:\Users\joshu\multi_firm_operations\lab\analysis\orb\orb_mnq_2026-07\_mnq_15m.pkl")
PINNED_SHA_PREFIX = "81c05e9a"          # Q-SESSCONF-1 provenance pin
BOUNDARY = date(2026, 7, 15)            # ORB campaign's already-read boundary
EMA_SPAN = 20
WARMUP = 19                             # bias undefined for daily-bar index < 19
CI_BLOCK, CI_DRAWS, CI_SEED = 10, 4000, 42
PL_BLOCK, PL_PERMS, PL_SEED = 60, 2000, 7

INST = ol.Instrument(
    name="MNQ_screen", path=Path("(in-memory)"), loader="none", feed="databento",
    tick=0.25, spread_pt=0.25, rt_cost_pt=0.0,
    open_tod=ol.OPEN_TOD_US, close_tod=ol.CLOSE_TOD_US, tz="America/New_York",
)


def sign(x):
    return np.sign(np.asarray(x, dtype=float))


def block_shuffle_p95(b: np.ndarray, y: np.ndarray, obs: float,
                      block: int, nperm: int, seed: int):
    """Permute the ORDER of contiguous `block`-day chunks of the bias sequence
    (outcomes fixed) — preserves marginals exactly and within-block clustering."""
    rng = np.random.default_rng(seed)
    n = len(b)
    starts = list(range(0, n, block))
    chunks = [b[s:s + block] for s in starts]
    rates = np.empty(nperm)
    ge = 0
    for i in range(nperm):
        order = rng.permutation(len(chunks))
        bp = np.concatenate([chunks[j] for j in order])[:n]
        rates[i] = float((bp == y).mean())
        if rates[i] >= obs:
            ge += 1
    return dict(mean=float(rates.mean()), p95=float(np.percentile(rates, 95)),
                p=(ge + 1) / (nperm + 1))


def score_cell(days, b, y, label):
    """Full frozen battery for one cell. days/b/y aligned, time-ordered, scored only."""
    n = len(y)
    hits = (b == y).astype(float)
    obs = float(hits.mean())
    lo, hi, _ = ol.block_bootstrap_ci(hits, block=CI_BLOCK, n=CI_DRAWS, seed=CI_SEED)
    h = n // 2
    halves = (float(hits[:h].mean()), float(hits[h:].mean()))
    t = n // 3
    thirds = (float(hits[:t].mean()), float(hits[t:2 * t].mean()), float(hits[2 * t:].mean()))
    pl = block_shuffle_p95(b, y, obs, PL_BLOCK, PL_PERMS, PL_SEED)
    f_up = float((b == 1).mean())
    p_up = float((y == 1).mean())
    closed_form = f_up * p_up + (1 - f_up) * (1 - p_up)
    per_side = {}
    for s, nm in ((1, "bias=+1"), (-1, "bias=-1")):
        m = b == s
        per_side[nm] = dict(n=int(m.sum()), gateHit=float((y[m] == s).mean()),
                            up_rate=float((y[m] == 1).mean()))
    years = pd.Series([d.year for d in days])
    by_year = {int(yy): float(hits[(years == yy).to_numpy()].mean())
               for yy in sorted(years.unique())}
    limbs = dict(
        n_floor=bool(n >= 400),
        ci_lb=bool(lo > 0.50),
        halves=bool(halves[0] > 0.50 and halves[1] > 0.50),
        placebo=bool(obs > pl["p95"]),
    )
    return dict(label=label, n=n, gateHit=obs, ci=(float(lo), float(hi)), halves=halves,
                thirds=thirds, placebo=pl, f_up=f_up, p_up=p_up, closed_form=closed_form,
                per_side=per_side, by_year=by_year, limbs=limbs,
                PASS=bool(all(limbs.values())))


def main():
    sha = hashlib.sha256(PKL.read_bytes()).hexdigest()
    print(f"panel sha256 = {sha}")
    if not sha.startswith(PINNED_SHA_PREFIX):
        print(f"!! sha mismatch vs pinned {PINNED_SHA_PREFIX}… — PREREG §2 says DISCLOSE + STOP")
        sys.exit(2)
    df = pd.read_pickle(PKL)
    df = df[(df["et"] + pd.Timedelta(hours=7)).dt.date <= BOUNDARY].reset_index(drop=True)
    print(f"bars after boundary truncation: {len(df)}  span ET {df['et'].min()} -> {df['et'].max()}")

    # ---- daily closes on CME session-days (Sun 18:00+ belongs to Monday) ----
    sess_day = (df["et"] + pd.Timedelta(hours=7)).dt.date
    daily = df.groupby(sess_day)["close"].last().sort_index()
    ema = daily.ewm(span=EMA_SPAN, adjust=False).mean()
    bias = pd.Series(sign(daily.to_numpy() - ema.to_numpy()), index=daily.index)
    bias.iloc[:WARMUP] = np.nan                      # EMA warm-up: undefined, excluded
    prior_bias = bias.shift(1)                       # prior COMPLETED session-day
    prev_close = daily.shift(1)

    # ---- RTH open/close via the campaign engine's own convention ----
    piv, meta = ol.session_panel(df, INST)
    y_oc = pd.Series(sign(meta["rth_close"].to_numpy() - meta["rth_open"].to_numpy()),
                     index=meta.index)
    y_cc = pd.Series(sign(daily.reindex(meta.index).to_numpy()
                          - prev_close.reindex(meta.index).to_numpy()), index=meta.index)

    pb = prior_bias.reindex(meta.index)
    out = {}
    for cell, yser in (("verdict_open_to_close", y_oc), ("disclosure_close_to_close", y_cc)):
        m = pb.notna() & (pb != 0) & yser.notna() & (yser != 0)
        days = [d for d in meta.index[m]]
        b = pb[m].to_numpy().astype(int)
        y = yser[m].to_numpy().astype(int)
        out[cell] = score_cell(days, b, y, cell)

    v = out["verdict_open_to_close"]
    verdict = ("SIGNAL" if v["PASS"] else
               ("AMBIGUOUS" if not v["limbs"]["n_floor"] else "NULL"))
    out["VERDICT"] = verdict
    out["panel_sha256"] = sha
    out["boundary"] = str(BOUNDARY)

    (HERE / "dstruct_results.json").write_text(json.dumps(out, indent=1, default=str))
    for cell in ("verdict_open_to_close", "disclosure_close_to_close"):
        r = out[cell]
        print(f"\n=== {cell} ===")
        print(f" n={r['n']}  gateHit={r['gateHit']:.4f}  CI=[{r['ci'][0]:.4f},{r['ci'][1]:.4f}]")
        print(f" halves={tuple(round(x,4) for x in r['halves'])}  thirds={tuple(round(x,4) for x in r['thirds'])}")
        print(f" placebo mean={r['placebo']['mean']:.4f} p95={r['placebo']['p95']:.4f} p={r['placebo']['p']:.4f}")
        print(f" f(+1)={r['f_up']:.4f}  P(up)={r['p_up']:.4f}  closed_form={r['closed_form']:.4f}")
        print(f" per_side={r['per_side']}")
        print(f" by_year={ {k: round(vv,4) for k,vv in r['by_year'].items()} }")
        print(f" limbs={r['limbs']}  PASS={r['PASS']}")
    print(f"\nVERDICT: {verdict}")


if __name__ == "__main__":
    main()
