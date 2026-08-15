# Q-ICT-1H-REVCON-1 — CLOSURE: AMBIGUOUS → CLOSED NOT-CONFIRMED (forward-watch belt)

**Verdict:** `AMBIGUOUS` (PREREG-0B §6 gate) · **Disposition:** `CLOSED — NOT-CONFIRMED` (operator-delegated best-call 2026-06-19) · **Date:** 2026-06-19
**Parent:** [`Q-ICT-REVCON-PLAN.md`](Q-ICT-REVCON-PLAN.md) · **Pre-registration:** [`PREREG-0B.md`](PREREG-0B.md) (committed `760435d` BEFORE this page was scored — firewall clean)
**Confirmatory data:** out-of-sample **2022-bear** regime — `BAR_EXPORT_v0.1_PEPPERSTONE_US500_…08eba.csv`, **14615 1H bars, 2021-01-03 → 2023-06-20, sha256 207b0a1b**, close 4814 → **3508** (the ~−27% 2022 bear) + 2021 top + 2023 recovery. **0 bars overlap** the previewed-benign window (firewall-clean).

---

## §1 — Verdict & gate evidence

| (zone\|bias) direction | rate | stride clr | block clr | placebo (drift floor) | beats drift | halves flip | n_floor |
|---|---|---|---|---|---|---|---|
| **prem\|+1 cont** | 0.5619 | ✓ | **✗** | 0.5372 | +2.5pp | no | 478 |
| **disc\|+1 rev** | 0.5805 | ✓ | **✗** | 0.5372 | +4.3pp | no | 292 |
| prem\|−1 rev *(the 0a-favored cell)* | **0.4578** | ✗ | ✗ | 0.4717 | — | yes | 204 |
| disc\|−1 rev | 0.5402 | ✗ | ✗ | 0.5277 | +1.3pp | no | 188 |
| (other 4 directions) | <0.52 | ✗ | — | — | — | — | — |

`candidates = []` · penalty winner `None` · e_max 0.5458 · `pass_dsr = False`.

**Why AMBIGUOUS (not RESOLVED, not FALSIFIED):** two cells clear the de-overlapped **stride** CI (so not a clean FALSIFIED — PREREG §6 reserves FALSIFIED for *no* stride clearance), but **neither clears the robust moving-block CI** — the dual-CI requirement PREREG imposes precisely because the two estimators can disagree on autocorrelated series. So no cell satisfies the full RESOLVED conjunction (stride **AND** block · beats placebo · halves-stable · survives the 8-way floor-n penalty) → `candidates` empty → AMBIGUOUS-HOLD.

## §2 — What PREREG-0B predicted vs what happened

1. **The 0a headline cell non-replicated — hard.** 0a's promising axis (premium reverts down under bearish bias) was **0.60** on the 6.5-mo benign window. Out-of-sample on the bear it is **0.4578 — below coin-flip**, and `halves_flip=True`. The motivating signal is gone. This is exactly the failure mode the exploratory/confirmatory firewall (parent §5; the lowered-prior note) was built to catch.
2. **The bear-page stride-clearers are bias drift, not edge.** Both are "up under bullish bias" (disc-reverts-up, prem-continues-up); the **drift-floor placebo** (the bucket's own up-rate under bullish bias) is 0.5372, so they beat it by only 2–4pp — and **fail the robust block CI**. Under *bearish* bias, nothing clears at all. The signal reduces to "price drifts up when the weekly bias is bullish" — the bias's own momentum, which the gates correctly refuse to certify.
3. **Well-powered, so not an underpowered near-miss.** Every cell clears the n-floor (188–478 ≫ 30); the stride-vs-block disagreement is about robustness/autocorrelation, not sample size — more data on similar regimes would not obviously firm a 2–4pp-over-drift, block-failing residual.

## §3 — Disposition (operator-delegated best-call)

**CLOSED — NOT-CONFIRMED.** The AMBIGUOUS near-miss is routed to a **forward-watch belt finding**, NOT a re-spec, because: the 0a headline died out-of-sample; the bear-page clearers are drift near-misses failing robustness; the prior was already lowered (cell-instability on the 18-mo benign extension); and the discriminator was the operator's cheap go/no-go — it did **not survive**. Escalation to the full multi-regime panel is not justified.

- **Belt finding (forward-watch):** *discount-reverts-up under bullish weekly bias* ≈ 0.58 (beats the bullish-bucket up-drift by ~4pp, clears stride, **fails the robust block CI**) — a "buy-the-dip-in-an-uptrend" residual, mild and not robust. Re-proposal bar: **new mechanism evidence / a genuinely different regime where it firms under BOTH estimators** — NOT re-tuning the frozen config (a §5 forbidden move).
- **Net:** the 1H premium/discount layer (re-investigated post-cascade) carries **no confirmed, robust, stable conditional edge on either axis** — the ER-regime axis was dropped pre-data (0a: starved + fragile), and the bias-sign axis now fails the out-of-sample confirmatory.

## §4 — Lessons (candidates)

- **The exploratory/confirmatory firewall + the out-of-sample regime test did their job.** A naive in-sample read would have escalated the 0a `prem|bearish ≈ 0.60` cell; the firewall held it as a hypothesis, and the out-of-sample bear killed it (`0.46`). The discipline (parent §5; the 18-mo preview lowering the prior; the operator's cheap-discriminator-first choice) converted a benign-window artifact into a clean negative for ~one export.
- **The drift-floor placebo (re-audit P-1) was load-bearing.** Without it, the bear-page `0.56`/`0.58` "up under bullish bias" cells would read as signal; the drift floor (0.537) showed them as the bias's own momentum. Pair this with the dual-CI (stride AND block) — both were necessary to reach the correct AMBIGUOUS-not-RESOLVED.
- **Audit-before-verdict paid off twice.** The 0b harness's two audit rounds fixed 4 verdict-corrupting penalty/gate defects (F1/F2/F4/F4-1) BEFORE this verdict was ever scored — the same M-15 discipline that caught the 1H harness offset defect in the cascade.

## §5 — Firewall audit hook

Was any criterion moved after the data arrived? **No.** The harness (`revcon_0b.py`) and PREREG-0B were committed at `760435d` **before** the bear page (`…08eba.csv`) existed/was scored. The verdict is mechanical from the committed gate. The page is genuinely out-of-sample (0 overlap with any previewed window). The disposition (close-to-belt vs re-spec, within the AMBIGUOUS branch) was the only judgement call, and it is recorded as operator-delegated.

---

## Verification

```bash
python lab/analysis/ict_revcon_2026-06-19/revcon_0b.py --bar "C:/Users/joshu/Downloads/BAR_EXPORT_v0.1_PEPPERSTONE_US500_2026-06-19_08eba.csv"   # VERDICT: AMBIGUOUS
git log --oneline -1 760435d   # PREREG-0B + harness committed before the bear page was scored (firewall)
```
