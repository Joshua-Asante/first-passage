# Phase B Lane B1 — CLOSED source-liveness check

**Purpose:** the real-time source check licensed by B1.3's `ADMIT` ruling (2026-08-24).
**Plan owner:** [`Phase B mechanism supply`](../../superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md)
§Lane B1, Task B1.5.
**Falsifier findings owner:** [`B1.0-B1.4 results`](2026-08-23-phase-b-lane-b1-falsifier-results.md).
**Status 2026-09-01:** `STOP — operator closed source pursuit`. No row or price outcome was ever
logged; K=0. The parent strategy pursuit is `DROP` because it lacks a credible high-positive-
expectancy prior and complete expression. Source liveness has no decision-changing consumer.

## Why the 20-session wait was withdrawn

The old protocol tried to use 20 sessions to decide both a 65% win-rate shape requirement and a
mean-capture hurdle. It could do neither reliably:

- 13 wins in 20 is exactly 65%, but its one-sided binomial tail under p=0.50 is ≈0.132 and its
  two-sided 95% Wilson interval is approximately [43.3%, 81.9%];
- the first conventional one-sided 5% rejection point is 15/20 wins, a 75% observed rate, and
  that rule has only ≈24.5% power when the true win rate is the target 65%; and
- no variance prior was frozen for mean capture, so 20 observations had no calibrated power for
  the cost limb either.

Waiting four weeks could therefore produce an attractive point estimate, not a defensible Vet
input. The expected positive outcome was only proof that the proposed free source recurs in time
to trade. That operational question can be answered without reading MES outcomes and without
waiting 20 sessions.

## Withdrawn replacement protocol — do not execute

The following five-session design is retained only to show what was stopped; do not execute it:

1. At 15:50–15:55 ET, check the admitted Financial Juice surface or the already-named public
   mirror for a same-day, timestamped, signed S&P 500 imbalance usable before the proposed 16:01
   entry. Do not substitute a Nasdaq, Dow, or Mag-7 number for the MES proposal.
2. Record only source facts: date, observation time, source status, index, signed value as printed,
   publication timestamp, and whether it was available by 15:55 ET.
3. Do **not** read or record MES entry, exit, return, win/loss, or post-close direction. This is a
   structural source-liveness check, not an effect probe; it remains $0/K=0.
4. Do not backfill the unlogged 2026-08-24→2026-09-01 interval. The first row must be a real-time
   observation made under this replacement protocol.

### Frozen disposition

- **SOURCE-LIVE:** at least 2 of 5 sessions contain a same-day signed S&P 500 figure available by
  15:55 ET. Two is the lower edge of B1's already-declared 2–4 event/week cadence, used here only
  to test whether the claimed route operationally exists.
- **PARK-SOURCE:** fewer than 2 of 5 qualify. Wake only on a verified recurring free source or an
  independently authorized licensed source; do not extend the check until it passes.
- **VOID:** any MES outcome is read or recorded before the five-session disposition. Restart only
  with a prospectively clean source check.

`SOURCE-LIVE` would not be evidence of alpha, cost reachability, win rate, or payoff shape. With the
parent strategy pursuit closed, neither `SOURCE-LIVE` nor `PARK-SOURCE` is live; the terminal
disposition is `STOP`.

## Source log

| # | Date | Checked at ET | Source status | Index | Signed value as printed | Publication time | Available by 15:55? | Notes |
|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | *(no sessions logged)* |

## Running tally

- Eligible sessions checked: 0 / 5
- Qualifying same-day S&P 500 figures: 0
- MES outcomes read: no
- Disposition: **STOP — never started; no rows permitted**

## Audit calculation

```bash
python - <<'PY'
from math import comb, sqrt
n, p, z = 20, 13 / 20, 1.96
for k in (13, 15):
    null_tail = sum(comb(n, i) * 0.5**n for i in range(k, n + 1))
    power_at_065 = sum(comb(n, i) * 0.65**i * 0.35**(n-i) for i in range(k, n + 1))
    print(k, null_tail, power_at_065)
den = 1 + z*z/n
centre = (p + z*z/(2*n)) / den
half = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / den
print(centre-half, centre+half)
PY
```
