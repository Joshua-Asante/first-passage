# P3 (L5) — curve-slope momentum — paper read + dedup + multi-tenor cost dry-run

**Date:** 2026-08-17
**Authority:** operator un-HOLD → GO on P3 (this session) under
[`docs/briefs/2026-08-17-six-lead-pursuit-plan.md`](../../../../docs/briefs/2026-08-17-six-lead-pursuit-plan.md)
§4 / §13. Licenses the plan's own Phase-1 item only: paper read, USOIL-carry
dedup, Databento `estimate` (no pull).
**Cost / K:** $0.00 billed · K=0 — metadata endpoints only; no
`register_search open`, no Cap claim, no CONFIRM read.
**Campaign tag:** `P3-L5-CURVE`

## Verdict: sleeve CLOSED — venue SCREEN-FAIL (calendar spread)

The dry-run itself is cheap (`ohlcv-1d` / `ohlcv-1m` / `definition` all $0.0000
on the venue-legal parent set). That is not the binding result. The paper's
profitable construction (S-strategy) is a **same-commodity calendar spread**
(long front / short fourth, or the reverse). This estate has already treated
that shape as a Tradeify compliance SCREEN-FAIL — definitionally offsetting
under §4a — before any score
([fade Stage-0 CARD](../../c1/tradeify_fade_stage0_2026-07-30/CARD.md)
2026-08-01 pass: "spreads are structurally illegal at this firm").

PASS on cost licenses only a priced data-extension decision. There is no
legal expression of the paper's S-strategy to extend. An outright-on-Δslope
rewrite is a **different construct**, not licensed here.

Harvest limb-2 does **not** increment (same grounds as P1-CF/P2-CF: never
admitted through intake; this is not a Stage-2 cost-law / Clause-N kill).

---

## §0 Rule-0 / sub-rule 8 (this session, HEAD `e088882`)

Dedup-first before writing into an existing harvest slug (no new
`lab/analysis/` directory opened):

```
# lab/CATALOG.md — six_lead / P3 / curve-slope / Bianchi
six_lead_cf_2026-08-17 | harvest | ACTIVE | six-lead pursuit plan P1/P2 cheap falsifiers …

# docs/briefs/INDEX.md — P3 / curve-slope / Bianchi
(empty)
```

Nearest prior cells (already on the plan §3 item 0.3/0.6 ledger):
`USOIL × commodity-carry-term-structure` → DEAD 2026-06-06 (static curve
**state**, outright, single-name). Fade Stage-0 CARD: calendar-spread
energy-reversion candidates SCREEN-FAIL at this firm.

Paper read this session: Bianchi, Fan, Miffre & Zhang, *Exploiting the
dynamics of commodity futures curves*, *JBF* 154 (2023) 106965; arXiv
`2308.00383` (2023-07-16 version). Not a PDF-bytes pin — construction
extracted from the arXiv text (abstract + §§2.1–2.2 + §3.1 + Table 4
claims). SSRN `3749061` 403'd as expected.

---

## 1. Paper construction (Rule-0, not the screen abstract)

Nelson–Siegel fit **daily**, **nearest four contracts** per commodity.
Three strategies assume one-day continuation of yesterday's parameter
change; portfolios form at close t, hold one day, fully collateralized,
equal capital long/short.

| Strategy | Signal | Trade | Paper result (1992-01 → 2019-06) |
|---|---|---|---|
| L | Δlevel | outright front-month | unprofitable |
| **S** | **Δslope** | **calendar spread: long front / short 4th** (or reverse) | **ann. mean 1.77% (t=7.23), SR 1.41** |
| C | Δcurvature | butterfly (short 1st, long 2nd ×2, short 4th) | SR 1.23 |

S and C profits are "mostly driven by the underperformance of the short
legs." The paper's own factor battery (carry, hedging pressure,
curve-momentum, relative basis, …) does not absorb S. Dual explanation
named in-text: risk (drawdowns in slowdowns) **and** sentiment/behavioral
(short-leg, Friday/Monday split). That is Path **1b** territory, not
Req-1a clause (i) — no mandated counterparty.

**21-name universe** (Szymanowska et al. 2014): crude oil, gasoline,
heating oil; corn, oats, rough rice, wheat; cotton, lumber; feeder cattle,
live cattle, live hogs; copper, gold, silver; soybean meal, soybean oil,
soybeans; cocoa, coffee, orange juice. Sample Jan 1992 – Jun 2019 (CoT
start). Databento GLBX.MDP3 floor is **2010-06-06** — the paper's first
18 years are not reproducible here.

---

## 2. Dedup vs `commodity-carry-term-structure` × USOIL

**Adjudication: DISTINGUISHABLE.** The 2026-06-06 kill
([`rejected_candidates.md`](../../../../docs/rejected_candidates.md);
harness `lab/archive/oil_carry/f1_mechanism.py`) conditioned an
**outright** CL front-month return on **static** curve state
(`close(CL.c.0) > close(CL.c.1)` = backwardation). It did not separate
(5d gap −0.024R; perm p=0.66). Verdict: disguised long-oil trend.

The paper's S-strategy is Δslope (not state), a calendar spread (not
outright), and cross-sectional (not single-name). The paper claims S
alphas survive a carry factor. That is a real construction difference.
It does **not** admit a candidate. It only means the re-proposal bar on
the dead USOIL cell does not by itself forbid *this* shape.

A rewrite that dropped the spread and traded an outright on Δslope would
collapse toward the dead cell's geometry and would need its own
adjudication — not done, not licensed.

---

## 3. Venue map

Tradeify product groups ([`prop_envelope_default.md`](../../../../ops/prop_envelope_default.md) §4a):

| Paper name | CME parent | Venue-legal? | Group |
|---|---|---|---|
| crude oil | `CL.FUT` | yes (CL/MCL) | Energy |
| gasoline | `RB` | **no** | — |
| heating oil | `HO` | **no** | — |
| corn / wheat | `ZC` / `ZW` | yes | Grains |
| oats / rough rice | `ZO` / `ZR` | **no** | — |
| cotton / lumber | `CT` / LBS | **no** | — |
| feeder / live cattle / hogs | `GF` / `LE` / `HE` | yes | Livestock |
| copper / gold / silver | `HG` / `GC` / `SI` | yes | Metals |
| soybeans / meal / oil | `ZS` / `ZM` / `ZL` | yes | Grains |
| cocoa / coffee / OJ | `CC` / `KC` / `OJ` | **no** | — |

**12 / 21** names are on the Tradeify list. The S-strategy still needs
opposing signs on two expiries of the **same** instrument. §4a letter:
"opposing directions on the same instrument *or* two products from the
same Product Group." Estate precedent (fade Stage-0 CARD, quoted above)
already closed that shape as SCREEN-FAIL. E1 (flat by 16:00) is a second,
independent problem for the paper's close-to-close overnight hold — not
reached.

L (outright) is venue-legal in isolation and **unprofitable in the paper**.

---

## 4. Databento `estimate` (no pull)

`--stype parent` · campaign `P3-L5-CURVE` · research venv
`.venv-research` · `DATABENTO_API_KEY` present · runner
`python -m databento_fetch.db_fetch estimate`.

Venue-legal twelve: `CL.FUT,ZC.FUT,ZW.FUT,GF.FUT,LE.FUT,HE.FUT,HG.FUT,GC.FUT,SI.FUT,ZM.FUT,ZL.FUT,ZS.FUT`.

| Schema | Window | Phase | Cost | Billable | Records |
|---|---|---|---:|---:|---:|
| `ohlcv-1d` | 2010-06-06 → 2019-01-01 | discovery | **$0.0000** | 75.4 MB | 1,345,693 |
| `ohlcv-1d` | 2019-01-01 → 2026-08-17 | oos | **$0.0000** | 79.4 MB | 1,417,994 |
| `ohlcv-1m` | 2010-06-06 → 2019-01-01 | discovery | **$0.0000** | 5.87 GB | 104,897,465 |
| `definition` | 2010-06-06 → 2019-01-01 | discovery | **$0.0000** | 10.68 GB | 20,537,878 |
| `definition` | 2019-01-01 → 2026-08-17 | oos | **$0.0000** | 12.18 GB | 23,419,301 |
| `tbbo` (contrast, `CL.FUT` only) | 2010-06-06 → 2019-01-01 | discovery | **$1,543.90** | 59.2 GB | 740,066,034 |

`tbbo` on **one** parent already exceeds the $700 spend ceiling
(12.4×). Matches the deep-lane triad finding: the cost wall is schema,
not the bar/definition ladder this campaign would need.

Dataset floor confirmed live: `2010-06-06`. `mbo` still schema-limited
to `2017-05-21+` (disclosed; unused).

---

## 5. What this does / does not license

**Licensed and done:** P3 GO mark; paper-construction read; USOIL-carry
distinguishability; $0 multi-tenor estimate. Sleeve closed on the
standing calendar-spread SCREEN-FAIL.

**Not licensed:** pull of any schema; NS-curve harness; outright-on-Δslope
rewrite; Phase 2 / Req-1a or 1b admission; `register_search`; Cap;
anything on P4/P5.

**Forbidden moves:** citing $0.00 bar figures as if they covered `tbbo`;
treating DISTINGUISHABLE as ADMIT; treating L-strategy (unprofitable
outright) as a rescue of S; counting this close on harvest limb-2.

## Verification

```
PYTHONPATH=lab .venv-research/Scripts/python.exe -m databento_fetch.db_fetch estimate \
  --symbols CL.FUT,ZC.FUT,ZW.FUT,GF.FUT,LE.FUT,HE.FUT,HG.FUT,GC.FUT,SI.FUT,ZM.FUT,ZL.FUT,ZS.FUT \
  --stype parent --schema ohlcv-1d --start 2010-06-06 --end 2019-01-01 \
  --phase discovery --campaign-id P3-L5-CURVE
# expect: cost $0.0000

rg -n "calendar spread" lab/analysis/c1/tradeify_fade_stage0_2026-07-30/CARD.md
rg -n "P3 \\(L5\\).*GO" docs/briefs/2026-08-17-six-lead-pursuit-plan.md
```
