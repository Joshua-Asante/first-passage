# Sources log — TNEC step-2 sourcing pass, 2026-08-10

**Authority:** operator pivot instruction this session, executing [TNEC-1](../../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md)
step 2 via [edge-cohort ADR](../../../../docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md) §2-C **L2**
(previously-unrun channels only) + **L3** (MES/MGC re-entered). Harvest Req 1–5 unchanged.
**$0 · K=0 · no manifest · no pull · no PnL/δ computed in-pass.** A staged seed is an observation, not a candidate.

**Dedup executed before plan freeze (output in session record):** `docs/rejected_candidates.md` (no gold/fix/metals
entry) · `docs/methodology/rejected_signals.md` (no hit) · `discovery_manifests/` (GC/MGC bank = DISC-CAMP-0
`disccamp0_gc_2010_18`, **disclosure not gate** per ADR 2026-08-04) · `instrument_profiles cell MGC event-window-reversal`
→ **untested, no binding bar** (adjacencies disclosed below) · forced-flow census passes 2/3/4 (fade-scoped; the
≥2 events/day law is a **fade-program** screening law, not a TNEC limb) · `Q-INVENTORY-1` CANDIDATE_ROWS (the
load-bearing hit — R8, below).

## Frozen channel plan (written before any query was run)

| # | Channel | Prior coverage | This pass |
|---|---|---|---|
| C1 | **Q5 metals mechanism-first re-run** (inherited by reference from Q-KBUDGET-HARVEST-1; blocker "no non-GC metals venue" + Req-3 FAIL-K both VOID — K-bank ADR, L3 re-entry, MGC venue-legal in Tradeify Metals Product Group) | Q5 closed 2026-07 on grounds now void | Re-stage `Q-INVENTORY-1` **R8** (gold-fix rows, Caminschi–Heaney *JFM* 2014) and hunt its Req-2 cohort δ + post-2015-auction-reform replication via Crossref + S2 citations |
| C2 | **Rank-1 citation-graph re-run** — the sole burst logged HTTP-429 partial (Moskowitz 2012 forward citations, influential filter) | Partial 2026-07-16; filtered variant ran 2026-08-01 from 2 seeds only | Retry S2 `/paper/{DOI}/citations` with `isInfluential`, futures-cohort + intraday-expressible shape filter |
| C3 | **arXiv q-fin systematic sweep** | Never run (Mesfin was a single entry) | arXiv API: q-fin.TR + q-fin.ST, futures/intraday/announcement/fix/carry terms, 2019+ |
| C4 | **Rank-3 futures journals, TNEC-shaped** | 2026-08-01 run was oil-AND-reversal-scoped only | Crossref: JFM/JBF/JFQA/Energy Economics × {intraday momentum, benchmark/fix window, announcement drift, term-structure intraday} on CME-micro-expressible instruments |
| C5 | **Rank-4 COT/TFF direct read** | Never executed; census P4-2: literature has no micro cohort δ | **Stub only** — a direct data read that examines returns is a δ-extraction probe (data spend + K). Staged as named recovery route, not run |
| C6 | **SSRN in-browser route** | 403-walled to date | Reserved for any full-text this pass actually needs; not swept blind |

**Shape filter applied to every hit (TNEC, not fade):** venue-legal CME micro (Equity Index long-only ·
Metals/Energy two-sided) · independent entries · intraday-complete, flat ≤16:00 ET build target · daily-or-better
event frequency (Req-4 practical bar) · named 1a constraint or full 1b · cohort δ on the target instrument's own
family. **No ≥N-trades/day floor** — that law was fade-scoped; TNEC N-ACT is weekly.

**Standing walls this pass does NOT relitigate:** index-intraday-OHLCV raised bar (2026-07-21) · EOD-adversity
raised bar (2026-08-02) · free-data 5th-leg SNAG bar (force forward from 2026-08-09; this pass is TNEC intake,
not 5th-leg expansion — routes 1/2 of that bar are the same paid-data/venue tests any survivor here must argue) ·
H-OD-1 / D5 / D3 / D7 / F-A/F-B/F-C closures · Striker legs · ORB unpark.

---

## C1 — R8 re-stage (gold PM-fix window, GC→MGC)

**Basis for re-stage (not a re-proposal):** `Q-INVENTORY-1` R8 verdict was **"KILL: Req-3 FAIL-K (GC/MGC bank
3,177). Logged only."** — no Req-1/2/4/5 screening was recorded. [ADR 2026-08-04](../../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)
withdraws GC/MGC K-kills explicitly ("stand or fall on their own mechanism records"); R8 has **no mechanism
record to stand or fall on**. This is the exact seed class L2/L3 exist to recover.

**Sniff-level screen (sourcing-time, before any manifest):**

| Req | Reading | Status |
|---|---|---|
| 1a | WHO = benchmark-execution flow at the LBMA gold auction (ETF/producer/central-bank fix orders; dealer hedging of fix exposure during the auction) — constraint-shaped, compensated by benchmark compliance. WHEN = PM fix 15:00 London / 10:00 ET (+ AM fix 05:30 ET), declared ex ante, daily. WHY-survives + HOW-dies need full text | **PLAUSIBLE — full text owed** |
| 2 | Caminschi–Heaney 2014 is a **GC-futures cohort** study (not a transplant). ⚠ Pre-2015 fix regime; the 2015 auction reform is a structural break — a post-reform replication is REQUIRED before any δ is read as live, else decay-haircut cannot be priced | **OPEN — the δ hunt below** |
| 3 | GC/MGC bank **3,177** (DISC-CAMP-0) — disclosed. Not a gate | **DISCLOSED** |
| 4 | 1–2 fixes/day → N ≈ 1,500+ per 6y panel → power viable iff δ/σ ≳ 0.05. Best event-frequency profile of any harvest seed to date | **PLAUSIBLE** |
| 5 | MGC RT = 2×$1.00 + 2×$1.06 = **$4.12**; hurdle = 4 × cost_bp at panel-era median gold level — computed at screen time, never at today's level. Order-of-magnitude at $2,000–2,700/oz: cost_bp ≈ 1.5–2.1 bp → hurdle ≈ **6–8 bp/event**. The δ must clear this; FX-fix precedent died at a 4.4 bp hurdle with ~3 bp gross | **OPEN — the binding number** |
| EM5/venue | 10:00 ET inside RTH · Metals two-sided legal · micro-expressible · intraday-complete by construction | **PASS (class)** |

**Disclosed adjacencies (not bars):** WMR-FX-fix cost kills (F3 M6E · Q-INVENTORY R3 · EURUSD fixing-reversal) —
all FX, all sub-3 bp δ vs 4×-hurdles; gold's higher per-event vol is exactly what the δ hunt must establish.
MYM 3rd-Friday settlement (different family). MOC procurement gate (does not bind — LBMA auction results are
published free).

### Query results (executed 2026-08-10; Crossref + S2, $0)

Anchor pinned: **DOI `10.1002/fut.21636`** (Caminschi–Heaney, *JFM*). S2 forward citations: **28 works.**
The Req-2 inputs exist and are named:

| Work | Year / venue | Role for R8 |
|---|---|---|
| Caminschi–Heaney, *Fixing a Leaky Fixing* | *JFM* 2014 | **Pre-reform GC-futures cohort δ** (tables; full text owed) |
| *Benchmarks in the spotlight: the impact on exchange traded markets* — `10.1002/fut.22120` | *JFM* 2020 | **Post-reform structural evidence** (abstract read: reform reduced quoted/effective spreads, improved depth on exchange-listed products) — the regime break is real and priced-in must-read before any δ is used |
| *Fixing the Fix for Silver and Gold* — `10.35944/jofrp.2020.9.1.013` | JoFRP 2020 | Post-reform vol/price change evidence (abstract read); manipulation-framing, no tradeable δ in-abstract |
| *Did the New Fix, Fix the Fix?* — `10.2139/ssrn.2657767` | SSRN 2015 | Immediate post-reform comparison (C6 browser route) |
| *Dealer Misconduct and Price Dynamics at the Fix* — `10.1016/j.jbankfin.2026.107641` | *JBF* 2026 | Most recent fix-dynamics study |
| *Who leads in intraday gold price discovery…* — `10.1002/FUT.22208` | *JFM* 2021 | Cohort structure: **futures lead gold price discovery** 2010–2018 (abstract read) — supports GC/MGC as the right expression instrument |

**R8 disposition: RE-STAGED `SEED-OPEN` → δ-extraction executed same day (operator GO) → `SCREEN-FAIL
(informed-flow + Req-5 cost-law)`.** Full record: [`DELTA_EXTRACTION_R8.md`](DELTA_EXTRACTION_R8.md).
The headline ~9.6+4 bp attaches to fix-direction knowledge (informed-flow, third confirmed instance of the
`H-FBEIA-1` signature); the causal public residue (1.3–3.2 bp/event, pre-reform) fails the 4× hurdle at every
venue-legal expression (MGC 6.3–10.3 bp; even full GC 3.4 bp at the generous top) **before** the mandatory
post-2015-reform decay haircut, whose published direction is adverse. The seed now dies on its own mechanism
record — which is what the re-stage was for.

## C2 — rank-1 citation re-run (Moskowitz 2012, DOI `10.1016/j.jfineco.2011.11.003`)

**COMPLETE this pass — the 2026-07-16 HTTP-429 gap is discharged at full depth.** S2 returned the entire
forward-citation set: **1,364 citing works** (1,000 + 364, no further page). Influential-flagged: **164**.
Futures-cohort among those: **18** (all portfolio/class-level TSMOM/carry/CTA studies — multi-day holds,
inexpressible at a daily-force-flat venue). Futures-cohort **AND** intraday-expressible: **0**.
Replicates the 2026-08-01 partial (94→5→0) at ~14× scale. **Channel verdict: structurally empty for this
venue's shape** — the TSMOM citation neighborhood contains no intraday-expressible futures-cohort δ.

## C3 — arXiv q-fin sweep (systematic; first ever)

`cat:q-fin.TR + all:futures` (200) + `cat:q-fin.ST + all:futures` (200), local shape filter, 2019+:
**31 shape-matched · 0 admissible.** Content: the known Mesfin MNQ cluster (rank-6, corroboration-only,
already dispositioned at N12/MNQBASE-1) · *Is Trend Still Your Friend? A Microstructural Account of the Demise
of Short-Term Trend-Following* (2026-07 — logged as **corroboration** of the D5-RECOST decay finding, rank-6,
no cohort δ) · *Trends and Reversion in Financial Markets on Time Scales from Minutes to Decades* (2025-01 —
logged, no per-instrument δ) · remainder ML-equity noise. No futures-cohort δ anywhere in the sweep.

## C4 — rank-3 TNEC-shaped journal sweep (Crossref; 12 frozen queries, JFM/JBF/JFQA × 4 families, 2015+)

**60 rows returned · 0 stageable.** Every live-looking hit is a dead-family echo, dispositioned by prior:

| Hit | Kill |
|---|---|
| *Understanding intraday momentum strategies* (*JFM* 2022, ×3 families) | D5/D5-RECOST family closed (cost-law + OOS edge decayed negative); mechanism prose does not resurrect a measured-dead edge |
| *Intraday momentum in the VIX futures market* (*JBF* 2023) | VX venue-wall (R6) |
| *Intraday TS momentum: China* (*JFM* 2019) | Req-2 transplant |
| *FOMC announcement returns on bond futures* (*JBF* 2021) | 8 events/yr — Req-4 presumptively dead (D3/D7 class); US Treasuries venue-dead besides |
| *Informed trading in FX futures: payroll news timing* (*JBF* 2022) | Informed-flow (F-B class) + 12 events/yr Req-4 |
| *Price Drift Before U.S. Macro News* (*JFQA* 2018) + *Disagreement and Scheduled Announcements* (*JFQA* 2025) | Pre-announcement leakage class, already killed (Q-INVENTORY / Drift-Begone) |
| *The treasury auction risk premium* (*JBF* 2025) | F-A (H-ZNAUC-1) cost-wall + Treasury venue-wall |
| *Combining momentum with reversal in commodity futures* (*JBF* 2015) | Multi-day hold — EM5-inexpressible |
| *Price Impact in Closing/Opening Auctions* (*JFQA* 2026, `10.1017/s0022109026102592`) | **Abstract checked**: cash-equity execution-cost cohort — NOT the "imbalance → index-futures response δ" the F1/MOC class finding names as its cheapest re-open. That input remains unsupplied |

## C5 — COT/TFF stub

Staged as named recovery route only: direct CFTC read examining positioning-vs-return is a δ-extraction probe
(data spend + K, `register_search open` first). Census P4-2's kill of the *literature* row (no micro cohort δ,
portfolio-class claims only) stands; the probe is the only route that manufactures the missing input. Not run
this pass.

## Verdict

**One re-staged seed — δ-extracted and closed on merits · zero new-mechanism seeds · three channels properly closed.**

- **R8 (gold PM-fix window, GC→MGC): `SCREEN-FAIL (informed-flow + Req-5 cost-law)`** — δ-extraction ran
  same day on operator GO ([`DELTA_EXTRACTION_R8.md`](DELTA_EXTRACTION_R8.md)). The void K-kill is replaced
  by a durable mechanism-record closure; family scope covers benchmark-fix constructs on the venue-legal
  metals set. Re-proposal bar: a post-reform, publicly-conditioned cohort δ clearing the 4× hurdle.
- **C2 closed at full depth** (1,364/1,364; the 07-16 429 gap is discharged): no intraday-expressible
  futures-cohort δ exists in the TSMOM citation neighborhood.
- **C3 run for the first time**: arXiv q-fin holds corroboration, not cohort δ.
- **C4**: the TNEC-shaped families in the rank-3 journals resolve entirely to already-dispositioned classes.
- **C5/C6 stubs stand** as named recovery routes (COT δ-probe costs K; SSRN browser reserved for R8's pull).

**Structural read, now complete:** the literature supplies portfolio-class δ for slow mechanisms and cohort δ
for dead ones. The one family with a venue-legal, daily-frequency, futures-cohort δ that had never been
screened on its merits — **benchmark-fix flow (R8)** — was screened same day on operator GO and died on the
same two walls as its FX siblings (informed-flow + cost-law). The L2 channel set is now exhausted at
**zero admissible seeds**, each closure carrying its own mechanism record. $0 · K=0 · zero pulls ·
`discovery_manifests/` count unchanged.
