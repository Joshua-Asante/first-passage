# Q-INVENTORY-1 — staged rows + Phase-3 sniff arithmetic

**Date:** 2026-07-17 · **Parent brief:** [`docs/briefs/Q-INVENTORY-1-zero-survivor-replenishment-disposition.md`](lab/archive/../../docs/briefs/Q-INVENTORY-1-zero-survivor-replenishment-disposition.md)
**Burst scope executed as frozen** ([pre-reg](lab/archive/../../docs/briefs/pre-registration/Q-INVENTORY-1-verdict-preregistration.md)): rank-1 Semantic Scholar + OpenAlex forward-citation traversal of Baltussen-Da-Lammers-Martens 2021 (54 S2 + 91 OA citing works, union ≈90 unique, all screened, 15 detail-reviewed — under the 50-cap; only 2 S2-influential, both non-futures); rank-2 survey/meta pass (10 searches); rank-3 futures-native journal pass (12 searches). Three parallel staging passes, coverage logs summarized in §Coverage. Zero manifests opened, zero `register_search`, zero pulls, zero K.
**Sniff constants:** inherited (pre-reg): Clause-K floors 1→0.65 / 2→0.85 / 3→0.98; Clause-N power ≥0.50 at Default-#1 OOS (2019-05-06→, N≈58 FOMC · ≈252 announcement-day · ≈259 ZN-auction · ≈374 weekly · ≈1,800 daily); Req-5 `δ ≥ 4×RT_frac` at panel basis.

---

## Detail-sniffed rows (all staged, none admissible)

### R1 — Pre-FOMC announcement drift (ES) — **KILL: Req-4 power (+ Req-1)**
Lucca & Moench *JF* 2015; Kurov-Wolfe-Gilbert *FRL* 2020 ("The disappearing pre-FOMC announcement drift"). Cohort SP/ES futures. 8 events/yr → N≈58 at Default-#1. Verbatim record: **+49bp**/24h-pre (1994–2011) → **+4.7bp** pooled (2011–2019) / **+9.2bp** (2016–2019 with press conference); Wilcoxon rejects equal halves at 1%. Conservative central (mandated decay reading) = post-2016 ≈9bp; σ(24h ES) ≈110bp → δ/σ ≈0.08 → **power Φ(√58·0.08−1.96) ≈ 0.09 FAIL** (break-even needs ≈28bp/event — only the pre-2015 figure clears, and that is precisely the decayed one). Req-1: 1a no consensus; 1b fails limb (iv) honestly — sign held but magnitude collapsed ~90% (attenuation is a known post-publication condition). K would have passed (ES bank 2 → floor 0.98) — irrelevant. Practitioner rescue claim (QuantSeeker 2025, SPY/QQQ) is rank-6 channel: no independent futures-cohort δ; does not rescue Req-2.

### R2 — Pre-release macro-news drift, ES/ZN (Kurov-Sancetta-Strasser-Wolfe ECB WP1901/*JFQA* 2019) — **KILL: Req-2 (ex-post/informed conditioning) + causal shutoff evidence**
Mechanism named — but it is **prerelease informed access**: per-event γ (0.066–0.154%/1σ surprise on ES) is *signed by the realized surprise*, capturable only with the pre-release signal. Sister paper (Kurov-Sancetta-Wolfe *JIMF* 2022 "Drift Begone!", GBP/USD CME futures): drift ≈40% of total adjustment **disappears entirely** when the UK eliminated prerelease access (Jul 2017) — cleanest causal identification that the anomaly *is* the leak. We are the named loser in this flow, not the collector. No unconditional confirm expression exists to cite. DROP.

### R3 — FX fixing / time-of-day window drift on CME FX futures (Krohn-Mueller-Whelan) — **KILL: Req-5 cost-law (4× hurdle)**
The strongest row staged: per-instrument **net-of-full-traded-spread CME futures** numbers published (2009–2018, n=2515): EUR pre-Europe window **+5.53%/yr net, SR 0.99**; JPY post-Tokyo **+2.41%/yr net, SR 0.52**; JPY pre-Tokyo −11.23%/yr net. Mechanism 1a named (dollar-immediacy demand at fixes + dealer inventory pre-fix hedging; Ranaldo 2009 segmentation support). 6E/6J banks 0 → K_eff 1, floor 0.65. Daily N≈1,800. Arithmetic: EUR window +5.53%/yr ÷252 ≈ **2.2bp/event net → ≈3.3bp gross**; 6E RT_frac ≈1.1bp (1-tick spread $12.50 + $1.90 commissions on ≈$130K notional) → **hurdle 4×1.1 = 4.4bp > 3.3bp gross → Req-5 FAIL**. JPY windows smaller still (≈2bp gross vs ≈4–5bp hurdle) and power-FAIL besides (δ/σ 0.033 → power ≈0.28). **Note for the record:** a published net-positive intraday effect still dies at the 4× doctrine multiple — the cost-wall pattern sharpened, not a novel kill mode. Dedup adjacency: EUR London-fix leg borders the rejected EURUSD fixing-reversal class — moot given the arithmetic kill, but the adjacency is logged. Ops adjacency (not a sniff limb): windows sit at 01:00–04:00 ET, outside any attended-automation posture.

### R4 — Post-FOMC drift in Treasuries (Brooks-Katz-Lustig NBER 25127) — **KILL: Req-2 + Req-4**
Cohort is constant-maturity cash yields, not per-contract futures δ (ZN transplant inadmissible); conditioning event (target change with non-zero Kuttner surprise) ≈4/yr → power dead. Mechanism (mutual-fund flow → slow-moving capital) noted for the record. Pan-Peng long-bond pre-FOMC variant: 0.68bp/event → power dead. DROP both.

### R5 — Announcement-day premium (Savor-Wilson; Knox-Londono-Samadi update) — **KILL: Req-4**
+8.3bp/event (1987–2023 update) vs daily σ ≈110bp → δ/σ 0.075 at N≈252 → power ≈0.22 FAIL. SPX-cohort caveat additionally unresolved. DROP.

### R6 — VIX-complex rows (VIX-futures intraday momentum, Huang et al. *JBF* 2022 net 21.78%/yr; VIX-ETP EOD SPX-futures pressure, Bangsgaard-Kokholm *JBF* 2025) — **KILL: venue/instrument + Tier-C posture**
VX not tradeable at the FRIENDLY firms; the ETP-EOD footprint on ES is D5's Tier-C class sibling with no extractable δ (403-walled) and a documented *subsequent reversal* — Tier-C default posture holds (no size carve-out). DROP.

### R7 — Other venue-walled rows — **KILL: instrument availability**
Coffee KC intraday momentum (ICE), Nikkei 225 cross-market (JPX), BTC option-expiry reversal (Deribit), Chinese commodity reversal (SHFE-class). None expressible at Tradeify/MFFU-class CME micro books. DROP (standing venue-wall lesson).

### R8 — Gold-fix rows (Caminschi-Heaney *JFM* 2014; "Fixing the Fix") — **KILL: Req-3 FAIL-K** (GC/MGC bank 3,177). Logged only.

## UNSCREENABLE stubs staged (named recovery routes — below-the-line, not admissible)

| Stub | Missing input | Recovery route | Cost to recover |
|---|---|---|---|
| **ZN Treasury-auction dealer-hedging unwind** (Smales *A&F* 2021; ~36 events/yr, N≈259 → power viable iff δ/σ ≥0.122; ZN bank 0) | Per-event δ not in abstract | Full-text retrieval + δ extraction (H-TSMOM-1 scrape pattern) | ~$0 data; one session; K unchanged until screened |
| **CL EIA-inventory unconditional event expression** (Rousse-Sévi *Energy J* 2019 ≈25bp conditional pre-release; Ye-Karali 2016; 52/yr, N≈374; CL bank 0) | Unconditional (non-surprise-signed) δ not published; conditional form is R2's informed-flow class | Full-text pull + pre-committed unconditional expression (post-release drift/reversal), then re-sniff | ~$0 data; one session; K unchanged until screened |
| **Carry timing-δ (6J/6E/CL)** — carried from burst-1, re-confirmed dead-ended this burst (ReSolve whitepaper: sector-level only; no per-instrument timing δ anywhere) | Per-instrument carry-timing δ | δ-extraction probe Pre-Q (data spend + K(family) 0→1) | Databento daily bars ≈$0 + 1 family-K + probe session |

## Coverage note

Rank-1: S2 (rate-limited, retried OK) + OpenAlex dual traversal; ≈90 unique citing works screened; excluded bulk = equity/options/China/overnight classes (full lists in the three pass transcripts, retained in session scratchpad). Rank-2: 10 searches; 4 paywalled PDFs locally parsed (NBER w25127, Drift-Begone, ECB WP1901, ReSolve carry). Rank-3: 12 searches; JFM 2023–2025 recent-issue sweep surfaced no new per-contract intraday rows within budget; no peer-reviewed ORB paper with per-contract NQ/ES/YM stats exists to cite. Burst discipline: `discovery_manifests/` count 5 → 5 (delta 0); no `register_search open`; zero pulls; Q1–Q6 untouched.
