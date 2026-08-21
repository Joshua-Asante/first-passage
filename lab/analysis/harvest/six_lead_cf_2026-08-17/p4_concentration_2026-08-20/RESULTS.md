# P4 (L2) — NQ.OPT trade-volume concentration by moneyness/tenor — RESULTS

**Date:** 2026-08-20
**Authority:** [`../P4_DRYRUN.md`](../P4_DRYRUN.md) §3 — *"the next step this memo can license is a small
`definition`+`trades` pull to check volume concentration by moneyness/tenor, not a G0 freeze."*
Operator direction this session: *"run the small definition+trades pull to check volume
concentration by moneyness/tenor."*
**Cost / K:** **$0.00 billed** (all three pulls estimated and confirmed $0.0000) · K=0 — no
`register_search open`, no Cap claim, no CONFIRM read.
**Campaign tag:** `P4-L2-GAMMA-conc` (child of `P4-L2-GAMMA`, distinct tag since window scope
narrowed from the dry-run's full-history estimate windows — see §0)

## Verdict: even the plausible-construction slice is thin, and thinner *relative to the underlying*
## than the complex-wide aggregate suggested — HOLD stands, evidence updated

The near-the-money (≤5% from spot) **and** near-dated (≤30 days to expiry) slice — the specific
region a same-day delta-hedging-flow proxy would actually use, not the complex-wide average —
trades at **~254 trades/session**, only **29.0%** of matched complex-wide volume. That is thinner
in absolute terms than the dry-run's own worry suggested, and it makes the **density gap versus the
underlying future *worse*, not better**: complex-wide the gap was ~367× (`P4_DRYRUN.md` §3,
full-history); restricted to the near-slice it widens to **~1,423×** (361,390 ÷ 254.4), because
narrowing to the plausible-construction region cuts the numerator by 71% while the underlying's own
density is effectively unaffected by that same restriction. **This does not settle the question —
see the caveats below — but it moves the evidence against, not toward, feasibility of a bare
trade-count/size-based signed-flow statistic on this slice.**

---

## §0 — Rule-0 reads (this session)

- [`../P4_DRYRUN.md`](../P4_DRYRUN.md) §3, in full — the exact next step this results doc executes,
  quoted above. Its own caveat carries forward unresolved by this pull: *"this dry-run did not check
  concentration by moneyness/tenor"* — this doc is that check.
- [`../P4_ROUTEMEMO.md`](../P4_ROUTEMEMO.md) — re-read to confirm the construction this evidence
  bears on: a **realized, flow-based** (not OI-snapshot) dealer-hedging proxy, architecturally near
  the near-the-money/near-dated slice by construction (the China paper's own mechanism is same-day
  hedge rebalancing, which concentrates where dealer gamma exposure is largest — near strikes, near
  expiry).
- `docs/rejected_candidates.md` `addback_condition` (dealer-gamma-regime-gate) — unedited this
  session; this results doc does not itself constitute a kill or a re-proposal (see §4).

---

## §1 — Data pulled this session ($0.00 total)

Window narrowed from the dry-run's full-history estimate windows (2010-2019 / 2019-2026) to a
**recent 3-month sample** (2026-05-20 → 2026-08-20, 79 CME sessions) after the full-OOS-era
`definition` pull timed out server-side at 2.8GB / 5.4M records (`504` gateway timeout, no data
lost — nothing was billed, the estimate stays $0.0000 and is still valid; the pull was simply too
large for one streaming request). A recent window is also more representative of *current* market
structure for a candidate that would deploy against today's options chain, not 2010-era liquidity.

| File | Schema | Symbols | Records | Cost |
|---|---|---|---:|---:|
| `definition.parquet` | `definition` | `NQ.OPT` | 285,350 rows | $0.0000 |
| `trades.parquet` | `trades` | `NQ.OPT` | 100,455 rows | $0.0000 |
| `nq_fut_ohlcv1d.parquet` | `ohlcv-1d` | `NQ.FUT` | 334 rows | $0.0000 |

`nq_fut_ohlcv1d.parquet` (all `NQ.FUT` expiries' daily bars) was pulled in addition to the
route memo's literal "definition+trades" because moneyness cannot be computed without an underlying
reference price — disclosed here explicitly rather than silently added; front-month proxy = the
highest-volume `NQ.FUT` contract per session (see `run_concentration_check.py`).

---

## §2 — Match rate (a real limitation, not swept under the results)

Of 100,455 pulled `NQ.OPT` trades, **69,285 (69.0%) matched** to a `definition` record inside the
same 3-month pull window; **31,170 (31.0%) did not** and were dropped. This is a mechanical artifact
of scoping `definition` to the same narrow window as `trades`: Databento emits a `definition` record
at an instrument's *listing or revision* event, not daily — an option series listed before
2026-05-20 that continued trading into the window produces trades with no matching definition record
inside it. **The dropped 31% were not checked for a different moneyness/tenor distribution than the
matched 69%** — if longer-dated, farther-OTM series (listed further in the past, consistent with
CME's option-listing cadence) are systematically over-represented in the unmatched set, the true
near-the-money/near-dated share could differ from what §3 reports. Closing this gap needs a
`definition` pull with an earlier `--start` (e.g. back to the start of the listing cycle for the
longest-dated series traded in the window) — not done here, flagged as the natural next refinement
if this candidate proceeds further.

---

## §3 — Concentration by moneyness and tenor (of the 69,285 matched trades)

**By distance from at-the-money (`|strike − underlying_close| / underlying_close`):**

| Moneyness | Trades | % of trades | Contracts | % of contracts |
|---|---:|---:|---:|---:|
| 0–2% (near ATM) | 16,960 | 24.48% | 53,087 | 20.08% |
| 2–5% | 16,471 | 23.77% | 57,793 | 21.86% |
| 5–10% | 15,766 | 22.76% | 60,304 | 22.81% |
| 10–20% | 12,232 | 17.65% | 55,996 | 21.18% |
| >20% (deep OTM) | 7,856 | 11.34% | 37,236 | 14.08% |

**By tenor (calendar days from trade date to expiration):**

| Tenor | Trades | % of trades | Contracts | % of contracts |
|---|---:|---:|---:|---:|
| 0–7d | 13,732 | 19.82% | 44,735 | 16.92% |
| 8–30d | 17,191 | 24.81% | 68,820 | 26.03% |
| 31–90d | 23,865 | 34.44% | 86,759 | 32.81% |
| >90d | 14,497 | 20.92% | 64,102 | 24.24% |

**Neither axis is sharply concentrated.** Moneyness declines gradually from ATM outward (no cliff);
tenor's *plurality* sits at 31–90 days, not 0–7d — the complex trades more in the 1–3-month bucket
than in the week-of-expiry bucket, contrary to a naive assumption that options activity clusters
near-dated. This is itself informative: the volume that exists isn't concentrated where a same-day
mechanism most needs it.

**Near-the-money (≤5%) AND near-dated (≤30d) — the plausible-construction slice:**

- **20,099 trades = 29.01%** of matched volume.
- **~254.4 trades/session**, vs. **~877.0 trades/session** complex-wide (this window) and
  **~361,390 trades/session** on `NQ.FUT` (from `P4_DRYRUN.md` §2/§3, same OOS-era figure).
- Density gap vs. the underlying: **complex-wide ~412×** (this window) / **~367×** (dry-run's
  full-history figure) → **near-slice ~1,423×**. Restricting to the construction-relevant region
  widens the gap by roughly **3.5–3.9×** rather than closing it.

Full cross-tabulation (moneyness × tenor, % of all matched trades) in
[`concentration_results.json`](concentration_results.json).

---

## §4 — What this does / does not license

**Licensed and done:** the route memo's + dry-run's own named next step, executed — a small,
disclosed `definition`+`trades`(+underlying `ohlcv-1d`) pull, $0.00, checking moneyness/tenor
concentration.

**Not licensed, not done:** any construct design, signal definition, or G0 freeze for L2; a
`register_search open` or Cap claim; a `docs/rejected_candidates.md` kill row; a verdict on whether
254 trades/session is *sufficient or insufficient* for a workable statistic — that depends on the
specific estimator (e.g., whether trade **size**/notional carries most of the signal even at low
trade **count**, which this pull did not test) and is a construct-design question, not a data-
availability one. **This results doc updates the evidence P4 stays `HOLD` against; it does not
itself change P4's disposition** — that remains an operator election, same as the route memo left
it.

**Forbidden moves:** reading the 1,423× figure as a definitive kill (it's a density finding, not a
signal-quality test); reading the 69% match rate as if it were 100% coverage; treating the
tenor/moneyness gradient (no sharp cliff) as evidence *for* feasibility — a smooth decline is
consistent with either a usable slice or a uniformly-thin-everywhere market, and this pull doesn't
distinguish the two without the size/notional-weighted signal test named above.

## §5 — Registry / harvest limb-2

Not admitted through intake (no `register_search open`, no manifest) — matching every other
Phase-1 item on this plan. Harvest §4 limb-2's counter does **not** increment. No
`docs/rejected_candidates.md` row — this is a feasibility measurement, not a mechanism kill.

---

## Verification

```bash
cd lab/analysis/harvest/six_lead_cf_2026-08-17/p4_concentration_2026-08-20
python run_concentration_check.py
# expect: near_the_money_near_dated_slice.trade_count == 20099, pct_of_all_matched_trades == 29.01

python -c "import pandas as pd; d=pd.read_parquet('trades.parquet'); print(len(d))"
# expect: 100455

python -c "import json; r=json.load(open('concentration_results.json')); print(r['trades_dropped_unmatched_definition'])"
# expect: 31170 (the §2 match-rate caveat, reproducible)
```
