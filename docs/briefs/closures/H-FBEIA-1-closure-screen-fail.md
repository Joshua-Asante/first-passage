# H-FBEIA-1 — CLOSURE: `SCREEN-FAIL (informed-flow — no unconditional edge)` (EIA moves CL ~25 bp but only conditional on surprise)

**Closed:** 2026-07-20 (operator asked to complete F-B after F-A + F-C both failed). Databento own-cohort δ-extraction authorized under the 2026-07-20 fork GO.
**Fork:** F-B (CL EIA-inventory unconditional event expression) from the [`Q-BOOKFIT-1`](Q-BOOKFIT-1-closure-resolved.md) fork program (priority F-A → F-C → F-B).
**Pre-registration:** manifest [`discovery_manifests/fb_eia_cl_reversal.json`](../../../discovery_manifests/fb_eia_cl_reversal.json) (`register_search open`, **K=1**, frozen before any return computed) + the pre-committed reversal expression in [`extract_eia_delta.py`](../../../lab/archive/q_fbeia_1_2026-07/extract_eia_delta.py) header.
**Run artifacts:** [`lab/archive/q_fbeia_1_2026-07/`](../../../lab/archive/q_fbeia_1_2026-07/) — `extract_eia_delta.py`, `eia_results.json`, `eia_events.csv`
**Data:** CL.c.0 ohlcv-1m, GLBX.MDP3, IS era 2010-06-06→2018-12-31 (Databento, **est + billed $0.00**, 2.85M bars).

## Verdict

**`SCREEN-FAIL (informed-flow)`.** The EIA release moves CL ~25 bp — but that move is **conditional on the inventory surprise**; strip the surprise and the unconditional tradeable edge is ~1 bp, indistinguishable from zero. Exactly the informed-flow class the scoping flagged.

| Quantity (N=445 EIA events) | Value |
|---|---|
| **Release reaction** \|m0\| (10:30→10:35) | **25.6 bp** — matches Rousse-Sévi (2019) ~25 bp; confirms events correctly dated + mechanism real |
| **PRIMARY unconditional reversal** (fade m0, 10:35→10:50) | δ = **−1.16 bp**, σ 50 bp, δ/σ **−0.023**, t **−0.49**, two-sided p **0.624** |
| **SANITY unconditional long** (10:30→10:45) | δ = −1.89 bp, t −0.68 (≈0, as surprise-symmetry predicts ✔) |
| Manifest survivors (naive / Bonferroni / BH) | **0 / 0 / 0** |

- **Req-4 power FAIL** (|δ/σ| 0.023 ≪ 0.122); **Req-5 cost-law FAIL** (|δ| 1.16 bp ≪ 6–10 bp). Both fail; the informed-flow diagnosis is the *why*.
- **The 25.6 bp reaction is the faithfulness anchor.** It reproduces the published conditional effect almost exactly, proving the event set is correctly dated and the EIA mechanism is real — so the null on the *unconditional* edge is trustworthy: it is not "we missed the events," it is "there is no edge tradeable without the surprise number." The reversal δ is even slightly negative (weak continuation), and continuation = −reversal is equally sub-cost.

## Disposition — the fork program is exhausted, 0/3 on edge

All three priced Q-BOOKFIT forks are now closed, each by a **distinct null mode**:

| Fork | Book-fit (M-21) | Edge verdict | Null mode |
|---|---|---|---|
| **F-A** ZN auction | ✓ ρ 0.512 | `SCREEN-FAIL` | **cost-wall** (mechanism confirmed, δ 1 bp vs 6–10 bp) |
| **F-C** carry 6E/6J/CL | ✓ ρ 0.295 | `SCREEN-FAIL` | **effect-absent** (Sharpe 0.09) |
| **F-B** CL EIA | ✓ ρ 0.615 | `SCREEN-FAIL` | **informed-flow** (25 bp reaction, but conditional on surprise; unconditional δ ~1 bp) |

- **Q-BOOKFIT-1's book-*fit* finding stands, undisturbed:** all three ρ/risk-N_eff projections were "the risk geometry fits," never "edge exists." The edge side is now empty across the entire priced supply — the exact split the M-21 coordinates were built to keep separate.
- **The breadth lever is empty at current supply** (now the *complete* 3/3 evidence, not the interim 2/3). This is the FALSIFIED-shaped disposition Q-BOOKFIT §6 anticipated for its downstream, and it **extends decompound-HOLD "no static counterbalance" from sizing → breadth → the whole priced fork set.**
- **The book's remaining levers are sizing and live-data authorization**, not breadth from these seeds. New book breadth requires **new mechanism evidence** (a fresh Tier-A seed clearing the harvest §2.1 cost-wall) — the 2026-11-08 idle review is its standing home. Not a re-run of any of these three (Trap #12).
- **K:** F-B banked K=1 (manifest committed). Fork-program K spend total = 2 (F-C carry + F-B EIA; F-A was a published-effect confirm, no K). CL family now carries two closed manifests (carry + EIA).

## Lesson note (no new registry entry)

F-B is the cleanest instance yet of the **informed-flow trap** the harvest Requirement-2 guards against: a real, large, published event-reaction (25 bp) that is entirely surprise-conditional and carries **zero** unconditional tradeable edge. The `|m0|=25 bp` faithfulness anchor is the tell — a big reaction with a ~0 unconditional forward δ *is* the informed-flow signature. Already encoded in `strategy_harvest.md` Req-2; logged as its sharpest worked example.

## §10 audit-hook discharge

- Databento pull est + billed **$0.00** ✔ · dry-run before pull ✔
- Manifest opened (K=1) **before** any return computed ✔ (register_search open precedes the extraction; expression frozen in the script header)
- Faithfulness: 25.6 bp release reaction reproduces the published conditional effect ✔ (events correctly dated); unconditional-long sanity ≈0 ✔
- Manifest closed with survivor p (0.624); 0/0/0 at naive/Bonferroni/BH ✔ · K=1 banked ✔
- No expression re-run after seeing the null (Trap #12) ✔
