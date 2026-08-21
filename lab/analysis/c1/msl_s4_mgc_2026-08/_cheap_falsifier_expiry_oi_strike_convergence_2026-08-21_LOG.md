# Cheap falsifier — `expiry-oi-strike-convergence` (MGC) — `NOT DECISIVE`

**Date:** 2026-08-21
**Fills:** [`STAGE1.md`](STAGE1.md) §Step 4 (recorded `NOT AVAILABLE` at G0 freeze — the sourcing
session's cloud container had no `DATABENTO_API_KEY`). Run from a local environment with the key
configured, per the RUNBOOK's own "next steps": *"get a real MGC/GC panel (Databento pull, cost
estimate first)."*
**Cost / K:** $0.00 · K=0 (definition/statistics/ohlcv-1d are $0 GLBX.MDP3 schemas; no K spent — this
is the disclosed cheap falsifier, not the Explore-confirm scoring pass in `PREREG_G0.md` §4)
**Runner:** [`_cheap_falsifier_expiry_oi_strike_convergence_2026-08-21.py`](_cheap_falsifier_expiry_oi_strike_convergence_2026-08-21.py)
**Raw:** [`_cheap_falsifier_expiry_oi_strike_convergence_2026-08-21_RESULTS.json`](_cheap_falsifier_expiry_oi_strike_convergence_2026-08-21_RESULTS.json)
**Panel:** none cached (small per-cycle streaming pulls, not written to a shared parquet panel)

**Disclosure — what this is NOT:** this is the generous/informal Step-4 check, not the pre-registered
Explore-confirm (`PREREG_G0.md` §4). No IS/CONFIRM partition was reserved before this read (§0's own
"Partitions: Not reserved this freeze" stands — a future Explore pass must still name IS/CONFIRM
before *its* read, per charter discipline). No significance test. Monthly OG options only (weeklies
excluded). Expiry-relative windows use `numpy.busday_offset` (Mon–Fri only, no CME holiday calendar) —
generous/approximate by design, not a G0-grade artifact.

## Frozen geometry (as specified in `PREREG_G0.md` §1–§2, unmodified)

| Knob | Value |
|---|---|
| Reference level | Highest-OI strike on the near-month OG (Gold monthly options) chain, ~3 sessions before that chain's own expiry |
| Arm window | Final 3 sessions before expiry (design default N=3) |
| Control window | Length-matched 3-session window, 10 sessions before the arm window (non-expiry-adjacent) |
| Direction check | Delete-test analogue: does displacement from the strike shrink more in the arm window than in control? |
| Proxy | GC (parent) close as the MGC reference price — same underlying, no rescale needed for a strike-*level* comparison (`PREREG_G0.md` §6) |
| Universe | 7 completed OG monthly cycles, Jan–Jul 2026 expiries (the 8th, `OGU6`/2026-08-26, was still open at run time — excluded, no look-ahead) |

Kill (informal, this falsifier only): if the arm-window convergence rate is no better than the
control-window rate, the near-expiry condition — the construct's own load-bearing claim (Γ ∝ 1/√T
intensifying pinning near expiry) — is not distinguishing itself from generic multi-session price
wobble. Not pre-registered as a formal VOID/FALSIFIED gate; informative only.

## Result

| Check | Arm (3 sessions pre-expiry) | Control (3 sessions, 10 sessions earlier) |
|---|---:|---:|
| converged (displacement shrank) | **4/7 (57%)** | **4/7 (57%)** |
| mean displacement change (pts) | **−1.47** (flat) | **−48.0** (net divergence) |
| std displacement change (pts) | 114.8 | 135.0 |

Per-cycle detail in the RESULTS.json — displacement ranged from a 297pt divergence (OGH6) to a
164pt convergence (OGN6); high cycle-to-cycle variance, no consistent direction.

**Verdict: `NOT DECISIVE`** — the arm and control windows converge at an *identical* rate (4/7 both),
which is the signature the construct's own delete-test treats as a kill ("convergence-toward-strike
should disappear on non-expiry control sessions" — here it doesn't clearly disappear, but the arm
window also doesn't clearly beat control). n=7 and no significance test means this cuts neither way
cleanly. This is a generous, informal read, not a scored verdict.

## Disposition

- Does **not** kill the card outright, and does **not** clear it either — per the RUNBOOK's own
  criteria ("if it looks dead on sight... report back; this closes the card cheaply"), this result
  is genuinely ambiguous, not a clean "dead on sight."
- Full Explore-confirm (`PREREG_G0.md` §4: proper IS/CONFIRM partition, weeklies included, delete/flip
  scored with a real significance test) is still the owed step before any TV/live build-out — this
  falsifier does not substitute for it (§5 forbidden moves: "both are owed, not either/or").
- `STAGE1.md` §Step 4 updated to point here rather than leaving the "NOT AVAILABLE" record standing
  as if the gap were still unaddressed.
- No `K_intrinsic` change, no `MECHANISMS.md` change, no disposition flip in `candidates_CARD.md` —
  this is evidence for whoever runs the deferred Explore-confirm next, not a new gate result.
