# Catalogue-size K wall — a Route B exploration catalogue on MNQ cannot exceed 3 cells

**Status:** RESOLVED — the DSR floor crosses the ratified Cap of 1.0 at **K=4**, so the maximum
admissible pre-registered exploration catalogue is **3 cells**. A proposed 90-cell order-flow
catalogue is 30× over; the same catalogue after an EM1 cost-law prune (72 cells) is 24× over.
**Both are equally dead, and the EM1 prune is irrelevant at this scale.**

**Date:** 2026-08-05 · **Runner:** [`run_catalogue_k_wall.py`](run_catalogue_k_wall.py) · **Raw:** [`RESULTS.json`](RESULTS.json)
**Repo anchor:** `fb87944`, worktree clean at run time.
**Cost:** **$0.00 · K=0 · no manifest · no data pull · no network.** No candidate is proposed,
admitted, scored, or licensed. Pure arithmetic on committed constants plus the ratified DSR harness.

---

## §1 — Why this exists

Avenue A [Route B](../../../../docs/adr/2026-08-05-avenue-a-generate-confirm-route.md) (`Accepted`
2026-08-05) opens the estate's first non-survivor-tied order-flow path: freeze a feature catalogue,
explore it on a reserved window, confirm one candidate. Its C0 sets **`K_intrinsic` = the number of
exploration cells examined**, and [ADR 2026-08-04](../../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)
sets **`K_eff` = `K_intrinsic`**.

Those two clauses compose into a constraint nobody had priced: **catalogue size alone drives the DSR
floor.** This study prices it before the first Route B campaign is scoped, at zero cost, so the G0
freeze is authored against a real ceiling rather than discovering one after a pull.

The study was commissioned to run a **different** screen — the EM1 cost-law pre-screen from the
[mechanism-shape spec](../../../../docs/spec/2026-08-05-eval-mechanism-shape-screen.md) — on a
proposed catalogue. That screen ran (§3) and **did not** produce the predicted result. The K wall was
found while checking whether the EM1 prune mattered. It does not. §4 records the failed prediction.

---

## §2 — Screen B (dominant): the K wall

`floor_at_k` is **imported unmodified** from the ratified Q-KBUDGET-1 harness
(`lab/archive/q_kbudget_1_2026-07/floor_scan.py`) — this study reimplements no DSR arithmetic and
pins no threshold of its own. `CAP = 1.0` (Q-GATECART-1, resolved 2026-07-14); `DSR_MIN = 0.95`;
most-permissive across trade frequencies {0.5, 1, 2, 4}/day, 6.5 y, Gaussian moments — i.e. **the
generous reading**, so the wall is a lower bound on severity.

| K (catalogue size) | annSR floor | verdict |
|---:|---:|---|
| 1 | 0.650 | open, headroom 0.350 |
| 2 | 0.850 | open, headroom 0.150 |
| 3 | **0.980** | open, headroom **0.020** |
| **4** | **1.060** | **CLOSED** |
| 6 | 1.160 | CLOSED |
| 12 | 1.300 | CLOSED |
| 72 | 1.595 | CLOSED |
| 90 | 1.625 | CLOSED |

**Max admissible catalogue = 3 cells.** At K=3 the headroom is 0.020 annualized Sharpe — narrower
than the gap between MNQ's best-ever measured construct (ORB-MNQ-1 at **+0.835** on the Tradeify
basis) and the Cap. In practice this means **K=1 or K=2**, and K=3 only for a candidate expected to
beat every MNQ result on record.

**This is not new doctrine — it is the same wall three prior artifacts hit from different sides,**
now stated as a general property rather than three separate observations:

- `ops/instruments/M2K.md` already says it verbatim: *"Do not spend this bank on a wide search. One pre-committed mechanism, `K_eff=1`."*
- `DISC-CAMP-0` closed with `k_dsr = 3177` and **zero** candidates reaching stage 4/5.
- The [08-08 pre-triage](../../../../docs/notes/2026-08-05-0808-pretriage-g3-g8-mechanical-findings.md) §G2/G6 reads the DSR gate as *"AMBIGUOUS by zero exposure"* — the gate has never been exercised. **This study supplies the mechanism for that observation:** any catalogue large enough to exercise the gate is automatically over Cap, so zero exposure is the *expected* state, not an accident of one campaign.

---

## §3 — Screen A (does not bind at catalogue scale): EM1 cost law

Retained because its per-cell output is what a ≤3-cell freeze must defend, and because it kills the
2 pt cell on grounds independent of the event-ceiling study's own "near-degenerate" ruling.

MNQ `point_value` **$2.00/pt**; cost **$0.95/side** = $1.90 RT = **0.950 pts** (friendly-firm worst
case, MFFU/BluSky-set; Tradeify is $0.91). `req_gross_R = 0.40 + cost_RT / R`.

| stop | R/contract | cost tax | req. gross | req. move | ticks | qty @ EM2 | vs 0.65R | vs 0.85R |
|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|
| 2 pt | $4.00 | 0.475R | 0.875R | 1.75 pt | 7.0 | 80.0 \* | **DEAD** | **DEAD** |
| 5 pt | $10.00 | 0.190R | 0.590R | 2.95 pt | 11.8 | 32.5 | ok | ok |
| 10 pt | $20.00 | 0.095R | 0.495R | 4.95 pt | 19.8 | 16.2 | ok | ok |
| 20 pt | $40.00 | 0.048R | 0.448R | 8.95 pt | 35.8 | 8.1 | ok | ok |
| 40 pt | $80.00 | 0.024R | 0.424R | 16.95 pt | 67.8 | 4.1 | ok | ok |

\* the eval 80-micro cap binds before the EM2 $325 frontier is reached.

Minimum admissible stop: **3.80 pt** vs the generic 0.65R bar · **2.11 pt** vs MNQ's best-ever 0.85R.

**The squeeze — the finding that survives.** Cost and horizon-feasibility pull in **opposite
directions** along the stop axis. Tight stops need a small absolute move (1.75 pt is plausible at a
5 s horizon) but carry a cost tax of 47.5% of R, pushing the gross requirement past anything ever
measured on the instrument. Wide stops have a negligible cost tax (2.4%) but demand a 16.95 pt —
68-tick — directional prediction that no 5 s order-flow signal supplies. **The viable band is 5–20 pt,
requiring 3–9 points of predicted directional edge per trade.** That is the number a G0 freeze must
defend, and it is now explicit before any byte is pulled.

The 2 pt cell dies on **two independent grounds**: the cost tax here, and the event-ceiling study's
own ruling that tight-`G` cells are *"near-degenerate and should not be quoted."*

---

## §4 — The failed prediction, recorded rather than quietly dropped

The session hypothesis, stated before this ran, was that **EM1 would kill most of a natural
microstructure catalogue** — the reasoning being that order-flow features are thin-per-event and
short-horizon, so the cost law would close the channel.

**It does not.** EM1 kills exactly one of five stop cells (90 → 72 of 90 cells, a 20% prune).

The error was arithmetic, not conceptual: MNQ is $2.00/point, so a $1.90 round trip is **0.95
points** — 19% of a 5-point stop and 2.4% of a 40-point stop. "Microstructure is thin, so cost will
kill it" was asserted without performing that division. This is a live instance of
`lesson_borrowed_numbers_need_connecting_arithmetic` and, more pointedly, of
`lesson_run_cheap_falsifier_before_authoring` — the falsifier took under five minutes and was
available before the claim was made.

Recorded here because a prediction that failed is the cheapest evidence this study produced, and
suppressing it would leave the same reasoning available to the next session.

---

## §5 — What this does NOT establish

1. **It does not close Route B.** It bounds Route B's *generate* stage to a 1–3 cell pre-committed catalogue. That is a severe narrowing — arguably narrow enough that "exploration" is the wrong word for what remains — but it is not a finding that the route is void.
2. **It does not measure any feature's edge.** Screen A computes a *required* gross edge; it says nothing about achieved edge, which needs data this study did not pull.
3. **It does not test the horizon↔stop coupling empirically.** §3's claim that a 5 s signal cannot supply a 17-point prediction is a plausibility argument, not a measurement. The free next step is the realized directional-move distribution at each horizon from the local 1 m panel (bounds the 120 s cell; 5 s needs `tbbo`, free inside the 1-year window).
4. **It licenses no candidate and proposes none.** The catalogue in §3 exists to be measured against, not to be frozen. Harvest Req 1–5, the regime gate, and the operator GO chain are untouched.
5. **The Cap and DSR threshold are inputs, not findings.** If Q-GATECART-1's Cap or the 0.95 DSR threshold is revisited, the wall moves. This study takes both as ratified and does not argue them.
6. **`floor_at_k`'s generosity cuts one way.** The scan is most-permissive across trade frequencies, so the true floor for a specific frequency is **higher**, never lower. The wall is a lower bound on severity.

---

## §6 — Consequence for the first Route B campaign

A campaign whose G0 freeze names more than 3 cells **cannot produce an admissible result no matter
what it finds** — the confirm can never clear DSR. Two implications:

- **A pull sized to explore a wide catalogue buys data for an unwinnable search.** The only pull worth authorizing is one sized to a ≤3-cell pre-committed catalogue — small, and almost certainly free inside the 1-year `tbbo` window.
- **The arithmetic favours Route A.** A survivor-tied cell is naturally K=1 (floor 0.650, headroom 0.350 — the widest available). The ToD-matched level-proximity discriminator that `MNQPROX-1` voided on is exactly that shape and is already the named owed successor to `MNQFLOW-1`'s N14 caveat. It needs a fresh freeze, not a bigger pull.

---

## §7 — Reproduce

```bash
python lab/analysis/c1/catalogue_k_wall_2026-08-05/run_catalogue_k_wall.py
python lab/analysis/c1/catalogue_k_wall_2026-08-05/run_catalogue_k_wall.py --quick   # smoke
```

Stdlib only; imports `floor_at_k`/`CAP` unmodified from the ratified harness. No vendor data, no
repo panels, no network, deterministic.

```bash
# The wall is a property of the ratified harness, not of this file
python -c "
import sys; sys.path.insert(0,'lab'); sys.path.insert(0,'lab/archive/q_kbudget_1_2026-07')
from floor_scan import floor_at_k, CAP
assert floor_at_k(3) <= CAP < floor_at_k(4), 'K wall moved - re-read this study'
print('K wall confirmed at 3/4 boundary')"
```
