"""Mechanical validation of f09_gate.py BEFORE scoring (PREREG §7 Phase 2).

Two classes:
  A. LEAKAGE PROOFS (constructive): perturb r_j / close_j, assert the causal state S_t is
     UNCHANGED for t<=j (it may only change for t>j). A failure = look-ahead -> would falsely PASS F09.
  B. POSITIVE/NEGATIVE CONTROLS: feed synthetic series with KNOWN regime structure and confirm the
     harness detects it (Δ>0, low perm p) and does NOT false-positive on noise (Δ~0, high perm p).
     Proves the harness has power and the FALSIFIED branch is not auto-firing.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from f09_gate import rolling_ac1_causal, efficiency_ratio_causal, conditional_delta, cyclic_perm_p, L_PRIMARY

P = "PASS"
F = "FAIL"
fails = 0


def check(name, cond):
    global fails
    print(f"  [{P if cond else F}] {name}")
    if not cond:
        fails += 1


print("=" * 80)
print("A. LEAKAGE PROOFS (the load-bearing checks)")
print("=" * 80)

rng = np.random.default_rng(0)
N = 400
r = pd.Series(rng.standard_normal(N))
S = rolling_ac1_causal(r, L_PRIMARY)
j = 200
r2 = r.copy()
r2.iloc[j] += 8.0  # massive perturbation at r_j
S2 = rolling_ac1_causal(r2, L_PRIMARY)
# S_t uses r through t-1 -> perturbing r_j may only change S_t for t >= j+1.
left_unchanged = np.allclose(S.iloc[:j + 1].fillna(-999).values, S2.iloc[:j + 1].fillna(-999).values)
right_changed = not np.allclose(S.iloc[j + 1:j + 2].fillna(-999).values, S2.iloc[j + 1:j + 2].fillna(-999).values)
check("AC1 state: S_t for t<=j UNCHANGED after perturbing r_j (no look-ahead)", left_unchanged)
check("AC1 state: S_{j+1} DOES change (window ending at t-1=j includes r_j; alignment correct)", right_changed)

# m_t alignment proof: m_t = sign(r_{t-1}) * r_t
m = np.sign(r.shift(1)) * r
m_manual = pd.Series([np.nan] + [np.sign(r.iloc[t - 1]) * r.iloc[t] for t in range(1, N)])
check("m_t == sign(r_{t-1})*r_t (manual recompute matches vectorized)",
      np.allclose(m.fillna(-999).values, m_manual.fillna(-999).values))

# ER state leakage
close = pd.Series(100 + np.cumsum(rng.standard_normal(N)))
rr = np.log(close).diff()
ES = efficiency_ratio_causal(rr, close, L_PRIMARY)
close2 = close.copy()
close2.iloc[j] += 20.0
rr2 = np.log(close2).diff()
ES2 = efficiency_ratio_causal(rr2, close2, L_PRIMARY)
er_left_unchanged = np.allclose(ES.iloc[:j + 1].fillna(-999).values, ES2.iloc[:j + 1].fillna(-999).values)
check("ER state: state_t for t<=j UNCHANGED after perturbing close_j (no look-ahead)", er_left_unchanged)

print("\n" + "=" * 80)
print("B. POSITIVE / NEGATIVE CONTROLS (power + no-auto-FALSIFIED)")
print("=" * 80)


def synth_delta(series_r, seedperm=42):
    r = pd.Series(series_r)
    m = np.sign(r.shift(1)) * r
    Sx = rolling_ac1_causal(r, L_PRIMARY)
    al = pd.DataFrame({"m": m, "S": Sx}).dropna()
    al = al[al["S"] != 0]
    d, em, er_, nm, nr = conditional_delta(al["m"], al["S"])
    p = cyclic_perm_p(al["m"].to_numpy(), al["S"].to_numpy(), d, n=2000, seed=seedperm)
    return d, em, er_, p, len(al)


T = 1600
# Positive control: regime switch — momentum (AR +0.5) first half, reversion (AR -0.5) second half.
# This IS the F09 scenario: a regime that switches, detectable with lead. Both states populated.
e = rng.standard_normal(T)
rs = np.zeros(T)
for t in range(1, T):
    phi = 0.5 if t < T // 2 else -0.5
    rs[t] = phi * rs[t - 1] + e[t]
d, em, er_, p, n = synth_delta(rs)
print(f"  regime-switch(+0.5|-0.5): d={d*1e4:+.2f}bps E[m|mom]={em*1e4:+.2f} E[m|rev]={er_*1e4:+.2f} perm_p={p:.4f} N={n}")
check("positive control (regime switch): d>0 AND E[m|mom]>0 AND E[m|rev]<0 AND perm_p<0.10",
      d > 0 and em > 0 and er_ < 0 and p < 0.10)

# Negative control: pure iid noise — no regime structure -> d~0, perm_p high (no false PASS).
e = rng.standard_normal(T)
d, em, er_, p, n = synth_delta(e)
print(f"  iid noise: d={d*1e4:+.2f}bps E[m|mom]={em*1e4:+.2f} E[m|rev]={er_*1e4:+.2f} perm_p={p:.4f} N={n}")
check("negative control (iid noise): perm_p >= 0.10 (does NOT false-positive)", p >= 0.10)

# Determinism: perm p identical across two calls (seed honored)
e = rng.standard_normal(T)
r0 = pd.Series(e)
m0 = np.sign(r0.shift(1)) * r0
S0 = rolling_ac1_causal(r0, L_PRIMARY)
al0 = pd.DataFrame({"m": m0, "S": S0}).dropna()
al0 = al0[al0["S"] != 0]
p1 = cyclic_perm_p(al0["m"].to_numpy(), al0["S"].to_numpy(), 0.0, n=1000, seed=7)
p2 = cyclic_perm_p(al0["m"].to_numpy(), al0["S"].to_numpy(), 0.0, n=1000, seed=7)
check("permutation determinism (same seed -> same p)", p1 == p2)

print("\n" + "=" * 80)
print(f"RESULT: {'ALL PASS' if fails == 0 else str(fails) + ' FAILURE(S)'}")
print("=" * 80)
sys.exit(1 if fails else 0)
