# MNQ-SIZEDIV-1 — DESIGN FREEZE (pre-data; staged GO elected)

**Campaign:** `lab/analysis/c1/mnq_sizediv_blind_2026-08/`
**Candidate:** `MNQ-SIZEDIV-1` — session-unit aggressor-size-asymmetry **divergence** → next-session two-slot RTH expression
**Channel:** [no-counterparty statistical sourcing channel](../../../../docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) (`--lane blind`; K-cap + pre-G0 addenda apply)
**Status:** `FROZEN 2026-08-15` — authored and committed **before any trades data was pulled or read**. Operator election: **staged GO elected 2026-08-15** (in-session, on the decision packet naming Stages 1/2/3 and their measured prices).
**Spend/K at freeze:** $0 · K=0 · no manifest · no Q-ID — the manifest opens at Stage 3 only (`register_search open` is the boundary, per the pre-G0 addendum).
**Author:** Claude Code (design) + Joshua (election).

---

## §0 Sources (read in full this session, before this freeze)

Channel ADR + K-cap + pre-G0 addenda · [cost-geometry notice](../../../../docs/notes/notice/N-2026-08-15-blind-channel-cost-geometry-and-first-candidate-kill.md) · [analogue-modality route ruling](../../../../docs/adr/2026-08-15-analogue-modality-route-ruling.md) · [CON-5 closure](../../../../docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) (the *"changes level (horizon / unit of analysis / data class), not catalogue"* directive this candidate follows) · [`ops/instruments/MNQ.md`](../../../../ops/instruments/MNQ.md) (N5/N6/N9/N11/N12 + full DEAD list) · `ops/instruments/MECHANISMS.md` §order-flow-depth-imbalance ruling · R2AGRUN/R2VBUCK/R2FLOW/OFCHAN closures (STATE index) · [index raised bar](../../../../docs/rejected_candidates.md) L718–744 · `lab/databento_fetch/db_fetch.py` · panel header (`time,open,high,low,close,volume`, UTC stamps, M15).

Panel: `core/data/bar_data/MNQ_M15.csv` (**primary checkout, read-only**; sha256 recorded into `STAGE1_DIAG.md` at first read). Panel span ends 2026-07-03.

**Dedup executed at freeze (Rule 8.8):** `check_advisor_dedup.py --keywords "size-weighted count-weighted aggressor imbalance divergence trade-size session sizediv"` → 57 term-overlap candidates, **none mechanism-overlapping** (top hits share only generic terms count/session/size/trade; Q-GATECART-1 shares "weighted/divergence" as vocabulary about gate floors). Literal mechanism grep `rg -i --no-ignore "size.?weighted.*(imbalance|aggressor)|I_vw|I_cw" docs/ lab/ ops/` → **zero hits estate-wide** before this campaign.

---

## §1 The candidate, fully specified (no free parameters)

**Statistic**, per RTH session *s* (prints 09:30:00–15:59:59.999 America/New_York; aggressor side ∈ {A, B} only):

- `V_B, V_A` = Σ print size by aggressor side · `N_B, N_A` = print counts by side
- `I_vw = (V_B − V_A) / (V_B + V_A)` · `I_cw = (N_B − N_A) / (N_B + N_A)`
- **`A(s) = I_vw(s) − I_cw(s)`** — positive ⇔ buy prints run systematically larger than sell prints that session.

**Side semantics:** `B` assumed buy-aggressor. Stage-1 verifies by print-level tick-rule agreement; agreement < 0.50 ⇒ the assumption flips **globally and symmetrically** (a semantics correction declared here in advance, not a tune; resolved before any outcome data is read).

**Expression (battery stage):** next session *s+1*, direction `d = sign(A(s))` (`A = 0` ⇒ no trade); two fixed slots — 09:30→12:45 and 12:45→16:00 ET, 1 contract each; hard stop at 1.0 × (TRAIN-era median RTH session range), touch-evaluated on M15 bar extremes; flat by 16:00 (EM5), hard stops (EM3), micro-expressible, ~2 trades/session. **The falsifier stage scores stop-free slot returns** (generous: at these widths stops only truncate tails; they never add edge).

**Slot returns (bp):** `r1 = ln(open_12:45 / open_09:30)·1e4` · `r2 = ln(close_15:45bar / open_12:45)·1e4` (M15 stamps are bar-open times; the 15:45 bar closes 16:00).

**Session calendar authority:** dates whose panel shows the full **26 RTH M15 bars** (analogue-1 precedent); half-days excluded everywhere. For dates **after the panel end (2026-07-03)**: a session qualifies as full iff it is a CME weekday and its RTH print span ≥ 6.0 h (naturally excludes 13:00 half-day closes); battery-stage returns for those dates come from `ohlcv-1s` ($0 full-era) at Stage 3.

**Costs (Tradeify basis, notice §1a):** RT $2.82/contract ≈ **0.911 bp** at panel-median notional. 1×RT = 0.911 bp · 2×RT = 1.822 bp · 4×RT hurdle = **3.645 bp**.

---

## §2 Data plan + measured costs (estimates run 2026-08-15, streaming basis, `GLBX.MDP3 · MNQ.v.0 · trades`)

| Stage | Window | Measured cost | Frozen ceiling |
|---|---|---|---|
| 1 — confirm-year | 2025-08-14 → 2026-08-14 | **$0.00** (12.73 GB · 265.2M records) | $1.00 |
| 2 — TRAIN falsifier semester | 2023-08-14 → 2024-02-14 | ≈ $102 (interpolated from $204/yr tier) | $120.00 |
| 3 — remainder to full 3y | 2024-02-14 → 2025-08-14 | ≈ $360 | $400.00 |

3y total measured **$462.27**; full-era $1,100.53 and tbbo-3y $770.46 are **over the $700 ceiling — not authorized**. tbbo is the fallback only if Stage-1 D1 finds `trades.side` unusable; that outcome = **STOP + operator re-election**, never a silent upgrade. Delivery: **batch API** (streaming died at this size on the OFCHAN precedent), `dbn+zstd`, `split_duration=month`, cache `~/.databento_cache/mnq_sizediv_blind_2026-08/<phase>/`. Free-window note: the entitlement's free year rolls forward — today's free year ages into ~$130 of billable data by early 2027, so Stage 1 has option value in pulling promptly.

---

## §3 Partition + quarantine (frozen before any pull)

- **TRAIN:** 2023-08-14 → 2024-08-14 (sessions ≤ 2024-08-13)
- **CONFIRM:** 2024-08-14 → 2026-08-14 — **virgin to all selection and evaluation until the Stage-3 battery**
- Stage 1 reads the confirm-year **conditioner only** (A(s) distributions, side semantics, degeneracy). **No return series is ever joined to A(s) outside TRAIN until the battery.** Rationale disclosed: the free year is the only $0 trades data; every Stage-1 rule below is outcome-free and pre-frozen, so no selection can leak from those reads.
- The falsifier (Stage 2) joins outcomes on TRAIN-side data only (2023-08 → 2024-02).

---

## §4 Stage gates (frozen; kills generous — failure conclusive, survival licenses spend only)

**Stage 1 — outcome-free diagnostics ($0):**

| Rule | Trigger | Consequence |
|---|---|---|
| D1 | signable share (side∈{A,B}) < 50% of prints, or < 240 parseable full sessions | **KILL** (side field unusable / coverage broken) |
| D2 | corr(I_vw, I_cw) > 0.995 across sessions | **KILL** (divergence degenerate: <1% distinct variance) |
| D3 | tick-rule agreement < 0.50 | flip side semantics (declared correction; report) |
| D4 | — | report-only: sd(A), AC1(A), monthly means, session/print counts |

**Stage 2 — falsifier on the TRAIN semester (ceiling $120):**

| Rule | Trigger | Consequence |
|---|---|---|
| F1 | mean signed gross/trade ≤ +0.911 bp (1×RT) | **KILL** (analogue-1's own bar) |
| F2 | sign-hit rate ≤ majority base rate, same window | **KILL** |
| F3 | \|corr(sign A(s), sign r_s)\| ≥ 0.5 | **KILL** (daily-momentum relabel ⇒ routed-by-omission) |
| F4 | — | report: session-block bootstrap 95% CI (2,000 resamples) on mean signed gross |
| PASS → Stage 3 | mean ≥ +1.822 bp (2×RT) and no KILL | licenses the Stage-3 spend |
| HOLD | mean ∈ (+0.911, +1.822] bp and no KILL | **operator re-election** before Stage 3 |

SE context, disclosed: n ≈ 126 sessions ⇒ SE(mean) ≈ 5.3 bp — a coarse sieve; a true-zero construct reaches PASS ≈ 36% of the time. That is what ~$102 buys; **the battery, not this gate, is the evidence standard.**

**Stage 3 — battery:** complete the 3y series; author `PREREG_G0.md`; `register_search open --lane blind --prereg <it>` at **K=1**; channel §2 battery scored on CONFIRM only; own-series half-split per prereg; N-SURV separately.

---

## §5 Forbidden moves

- Introducing any parameter (size threshold, winsorization, weighting exponent, slot change, lag change) — each is a **new K axis**, never a refinement of this candidate.
- Scanning alternative weighting functionals. This freeze declares **none was computed on any data** before commit.
- Instrument / horizon hop after seeing numbers (standing bars).
- Reading any CONFIRM outcome before the Stage-3 battery.
- Treating a Stage-2 PASS as evidence of edge (it is a spend license at ~36% false-go).
- On a kill: no retune revive — the analogue-1 information-content precedent governs; the channel's pre-G0 kill count increments and is disclosed.
- Reclassifying a battery-stage death as pre-G0 (boundary = `register_search open`, per the addendum).

---

## §6 K + family-bank disclosure

`K_intrinsic = 1` (statistic parameter-free; expression fixed; the D3 semantics flip is symmetric, not selective). Family bank at freeze (disclosure-not-gate, [ADR 2026-08-04](../../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)), from `discovery_manifests/`: `d5_nq_intraday_mom` · `orb_mnq_intraday_breakout` · `st_eh_supertrend_grid` · `mnqflow_depth_imbalance` · `mnqfvg_draw_probe` · `mnqpool_shield_probe` · `mnqsr1_structure_20260806`(+`b`) · `q_txg1_striker_mnq_20260812`.

---

## §7 Distinctness + adjacency disclosures (the harvest-by-omission answer)

- **Not an analogue-1 retune/transplant:** different data class (prints), unit (session), horizon (t+1); no pattern matching; the F3 relabel control is mandatory.
- **Not a CON relabel:** no entry geometry — entries are time-fixed; direction comes from an algorithmic statistic (the analogue ruling's own admissibility test: absence of named entry geometry).
- **Not an R2 retune:** R2AGRUN/R2VBUCK/R2FLOW scored *net signed aggressor size / runs / buckets at minute→60s*; the vw−cw **divergence** functional was never computed at any horizon (mechanism grep: zero estate-wide hits). Their closures' sanctioned re-proposal path is "new G0 / new mechanism" — this is that, under a fresh G0.
- **MNQFLOW-1 re-proposal bar answered:** trades-derived; "a named feature that is NOT top-of-book size imbalance."
- **Index raised bar:** outside its scope ("OHLCV structure alone"); enters via its own route ② (order-flow modality). The route-② **L1 pause** covers top-of-book features; this is not one.
- **Published neighborhood, named rather than omitted:** stealth-trading / PIN-family theory (informed traders and trade size) exists; **no counterparty is claimed and no cohort δ is borrowed** — admission is on the channel's own no-narrative terms, not as a harvest seed. Daily net-flow→return literature (Chordia-class) concerns *net flow* (≈ I_vw alone); the divergence functional is a different object. Baltussen intraday momentum is price-based and measured dead on MNQ (N5); no part of it is used.
- **Buying flow data pre-survivor (skill red flag), justified:** bars cannot carry print sizes/sides by construction; four bar-class catalogues + four minute-scale flow catalogues are exhausted; the channel's named outs are "new modality, instrument, or paid-data route" — this is the paid-data route, cost-gated and staged.

---

## §8 Kill-count exposure

Channel pre-G0 kill count at freeze: **1** (`MNQ-ANALOGUE-1`). A Stage-1/Stage-2 kill here ⇒ count **2**, putting live pressure on the **uncovered consecutive-kill threshold** (STATE queue row 3 on this lineage; note: the 2026-08-15 public STATE roll dropped that queue row — the item survives there only as a decision-index line).

---

## §9 Audit hooks

```bash
# Freeze precedes data: this file's introducing commit predates the first cache file's mtime
git log --format="%h %cI %s" -- lab/analysis/c1/mnq_sizediv_blind_2026-08/DESIGN_FREEZE.md | tail -1
ls -la ~/.databento_cache/mnq_sizediv_blind_2026-08/ 2>/dev/null

# Stage-1 code never touches panel prices (calendar reads the time column only)
grep -n "usecols" lab/analysis/c1/mnq_sizediv_blind_2026-08/sizediv_lib.py

# Mechanism-family dedup was clean at freeze (expect: only this campaign dir)
rg -i --no-ignore -l "size.?weighted.*(imbalance|aggressor)|I_vw" docs/ lab/ ops/ lab/analysis/c1/mnq_sizediv_blind_2026-08/

# Pre-data unit tests were green before any pull
python -m pytest lab/analysis/c1/mnq_sizediv_blind_2026-08/test_sizediv_lib.py -q
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-15 | Freeze authored + committed pre-data; staged GO elected in-session; dedup executed clean | JA (election) + CC |
