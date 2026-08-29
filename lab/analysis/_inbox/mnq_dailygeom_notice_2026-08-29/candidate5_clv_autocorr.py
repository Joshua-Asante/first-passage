"""Candidate 5 -- bar closing-location (CLV) lag-1 autocorrelation on MNQ M15,
unconditional on level/session/regime.

CLV_t = (close_t - low_t) / (high_t - low_t) in [0,1] -- where within its own
H-L range the bar closed. Distinct statistic class from candidate 1/2/4's
magnitude (range/TR/gap) series: CLV is a BOUNDED ratio, not a heavy-tailed
magnitude, so the frozen IAAFT corrected-null battery (built and tolerance-
calibrated for True-Range-shaped series) is not reused here -- a fresh,
appropriately-scoped null is used instead: a block-permutation (moving-block
shuffle) null on CLV itself, which is the standard approach for testing serial
dependence in a bounded/ratio statistic under unknown short-range dependence
(Politis-Romano block bootstrap family; distinct citation from the IAAFT
literature this repo already uses for magnitude series). This satisfies the
"fresh batteries need the same check reuse gets" rule: the null-validity
argument is that a block (not iid) shuffle is required because CLV itself may
carry short-range dependence unrelated to the lag-1 claim under test (e.g. a
trending sub-session produces a run of high-CLV bars for reasons that have
nothing to do with bar-to-bar transmission) -- an iid shuffle would systematically
overstate significance by breaking that within-block structure entirely, while a
block shuffle preserves it and asks only about ORDER.

Tested on the FULL continuous bar sequence (RTH + overnight), consecutive M15-
to-M15 pairs in raw chronological order, per the candidate's own framing
("unconditional on any level, session anchor, or volatility regime"). H==L
degenerate bars (data_lib confirms zero in this panel) would be excluded were
any present.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from data_lib import load_raw  # noqa: E402


def main():
    df = load_raw().reset_index(drop=True)
    hi, lo, cl = df["high"].to_numpy(), df["low"].to_numpy(), df["close"].to_numpy()
    rng = hi - lo
    degenerate = rng == 0
    print(f"degenerate H==L bars: {degenerate.sum()} / {len(df)}")
    valid = ~degenerate
    clv = np.where(valid, (cl - lo) / np.where(valid, rng, 1.0), np.nan)

    x = clv[:-1]
    y = clv[1:]
    ok = (~np.isnan(x)) & (~np.isnan(y))
    x, y = x[ok], y[ok]
    n = len(x)
    print(f"scored consecutive pairs: {n}")

    rho, p_asymptotic = spearmanr(x, y)
    print(f"Spearman rho(CLV_t, CLV_t+1) = {rho:.5f}  (asymptotic p={p_asymptotic:.2e}, NOT the governing test)")

    # Block-permutation null: shuffle the ORDER of contiguous blocks of y (the
    # t+1 series), x fixed -- preserves each series' own within-block dependence
    # and marginal distribution exactly; asks only whether the OBSERVED PAIRING
    # (order) carries more lag-1 rank-dependence than a block-reordered pairing.
    block = 96  # ~1 trading day of M15 bars
    rng_gen = np.random.default_rng(20260829)
    starts = list(range(0, n, block))
    chunks_y = [y[s:s + block] for s in starts]
    nperm = 2000
    null_rho = np.empty(nperm)
    for i in range(nperm):
        order = rng_gen.permutation(len(chunks_y))
        y_perm = np.concatenate([chunks_y[j] for j in order])[:n]
        null_rho[i] = spearmanr(x, y_perm).statistic
    p_upper = (1 + int((null_rho >= rho).sum())) / (nperm + 1)
    p_lower = (1 + int((null_rho <= rho).sum())) / (nperm + 1)
    print(f"block-shuffle null (block={block}, nperm={nperm}): "
          f"mean={null_rho.mean():.5f} sd={null_rho.std():.5f} "
          f"p2.5={np.percentile(null_rho,2.5):.5f} p97.5={np.percentile(null_rho,97.5):.5f}")
    print(f"p_upper={p_upper:.5f}  p_lower={p_lower:.5f}")

    # halves stability
    h = n // 2
    rho1 = spearmanr(x[:h], y[:h]).statistic
    rho2 = spearmanr(x[h:], y[h:]).statistic
    print(f"halves: H1 rho={rho1:.5f}  H2 rho={rho2:.5f}")

    out = dict(n_pairs=n, rho=float(rho), block=block, nperm=nperm,
               null_mean=float(null_rho.mean()), null_sd=float(null_rho.std()),
               null_pct=[float(np.percentile(null_rho, q)) for q in (2.5, 5, 50, 95, 97.5)],
               p_upper=p_upper, p_lower=p_lower, halves=dict(H1=float(rho1), H2=float(rho2)))
    (HERE / "candidate5_results.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
