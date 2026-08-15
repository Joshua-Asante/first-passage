# Sources log — radar Tier-A burst 2026-07-16

**Dedup first:** `docs/rejected_candidates.md`, closed discovery manifests, D1–D7 / H-OD-1 / H-TSMOM-1 inventory, `rejected_signals.md`. Month-end / HARV class stays dead (D3/D7). GC/MGC any-design stays FAIL-K (bank 3,177). D5/H-OD-1 closed campaigns not re-emitted.

## Rank-1 — citation neighborhood of H-TSMOM-1 (Moskowitz–Ooi–Pedersen 2012 *JFE*)

| Source | Venue | Disposition |
|---|---|---|
| Moskowitz, Ooi & Pedersen — *Time series momentum* | *JFE* 2012 | **Seed.** Fig.2 per-instrument gross SR digitize extended beyond S&P (see [`FIG2_DIGITIZATION.md`](FIG2_DIGITIZATION.md)). Equity S&P already inventoried as `H-TSMOM-1`. |
| Hurst, Ooi & Pedersen — *Demystifying Managed Futures* | *JOIM* 2013 | **CHEAP RECOVERY (label authority).** Fig.2 prints explicit L→R labels for the same 12 FX pairs as Moskowitz 2012. Digitized 12-Month USD-JPY SR **0.54** (±0.03). Cleared `H-TSMOM-6J` Req-2 via label map + Moskowitz bar-12 corroboration (SR 0.49). See [`CHEAP_RECOVERY_JPY.md`](CHEAP_RECOVERY_JPY.md). |
| Hurst, Ooi & Pedersen — *A Century of Evidence on Trend-Following Investing* | *JPM* 2017 | **EXCLUDE:path-1b-support-not-new-axis** — replication/extension of the same 12m-class TSMOM; no distinct family/design/N/δ 4-tuple vs H-TSMOM-1. |
| Asness, Moskowitz & Pedersen — *Value and Momentum Everywhere* | *JF* 2013 | Logged; cross-sectional momentum/value — not Tier-A time-series confirm without a separate δ extraction. Not staged this burst. |
| Semantic Scholar forward-citations of Moskowitz 2012 | API | **BLOCKED — HTTP 429.** Proceeded without; named as design §5 automate-later.

## Rank-2/3 — carry + term-structure (Tier A)

| Source | Venue | Disposition |
|---|---|---|
| Koijen, Moskowitz, Pedersen & Vrugt — *Carry* | *JFE* 2018 | **Primary carry/basis source.** Table 2: currency carry1m SR **0.68**; commodities carry (=basis) SR **0.60**; global equities carry SR **0.91**. Table 6 timing (vs historical mean): FX **0.53**, commodities **0.75**, equities **0.75**. All are **asset-class portfolios**, not per-contract δ → staged as `UNSCREENABLE:per-instrument-delta-sigma-not-extracted` (`H-CARRY-FX-1`, `H-CARRY-CM-1`). Path 1a clear (interest differential / convenience yield / theory of storage). |
| Basu & Miffre — *Capturing the risk premium… hedging pressure* | *JBF* 2013 | **EXCLUDE:cross-sectional-commodity-sort** — long-short HP portfolios (SR ~0.27–0.93). No single-contract cohort δ; not a confirm-not-mine ≤3 expression on one prop leg without a fresh δ probe. |
| Szymanowska et al. — *An Anatomy of Commodity Futures Risk Premia* | *JF* 2014 | Logged; basis/spot premia decomposition. Points at same basis family as Koijen commodities — no new per-contract row without extractable δ. |
| Erb & Harvey — *Tactical and strategic value of commodity futures* | *FAJ* 2006 | Logged; survey/practitioner. Encyclopedia-tier pointer only (strategy_harvest §2.3 rank 5/6). |

## Explicit non-staged (Tier C / dead classes)

| Item | Reason |
|---|---|
| Baltussen intraday momentum / dealer-gamma siblings | Tier C graveyard-watch; D5 already closed cost-law |
| Overnight drift siblings | H-OD-1 closed cost-law; gate-geometry |
| Month-end / pension-flow | D3/D7 FAIL(N); dead class |
| GC/MGC TSMOM or basis | Req 3 FAIL-K (bank 3,177) |

## Channel coverage (design §4 / §5)

| Step | Done? |
|---|---|
| (1) Citation-graph from Tier-A seed | Partial (direct seed + known influential neighbors; SS API 429) |
| (2) Class-directed pass (TSMOM / carry / term-structure) | Yes |
| (3) Survey/meta pass | Light (Erb–Harvey; century trend paper as Path-1b support only) |
| (4) Stage rows + Req-5 sniff | Yes — [`CANDIDATE_ROWS.md`](CANDIDATE_ROWS.md) |
