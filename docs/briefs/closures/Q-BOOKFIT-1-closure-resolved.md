# Q-BOOKFIT-1 — CLOSURE: `RESOLVED` (all three priced forks project inside the book-improving band)

**Closed:** 2026-07-20 (same session as lock — single-session execution per §7)
**Parent brief:** [`../Q-BOOKFIT-1-fork-composition-coordinate-triage.md`](../Q-BOOKFIT-1-fork-composition-coordinate-triage.md) (now `CLOSED-RESOLVED`)
**Pre-reg (FROZEN before any projection):** [`../pre-registration/Q-BOOKFIT-1-verdict-preregistration.md`](../pre-registration/Q-BOOKFIT-1-verdict-preregistration.md) — commit `0fc1e05` (19:18 ET), projection first ran after `4046bd2`
**Run artifacts:** [`lab/archive/q_bookfit_1_2026-07/`](../../../lab/archive/q_bookfit_1_2026-07/) — `run_projection.py`, `projection_results.json`
**Execution invariants held:** zero pulls for the projection; zero K; zero manifest opens; the one cost-gated symbology pull (Phase 1b) estimated then billed **$0.00**.

## Verdict (§D asserted against actual numbers)

**`RESOLVED`** — all three forks scoreable; **3/3 PASS** the frozen criteria (`ρ < 1.0` AND `n_eff_risk_delta > 0` at the 0.37% reference weight). The reconcile gate confirmed panel fidelity: measured 2-leg daily $-std **$273.28** vs the Q-COMPOSE-1 anchor $273 (dev 0.1%, tol ±10%); 2-leg risk PR **1.9631** (closure precedent 1.96). Weekly cov eigenvalues {162,742; 214,449} ($²).

| Fork | N_b/yr | σ_d @0.37% | ρ (vs $273) | risk-N_eff Δ | w* (ρ=1) | PASS |
|---|---|---|---|---|---|---|
| F-A ZN auction unwind | 36 | $139.85 | **0.512** | **+0.787** | 0.72% | ✔ |
| F-B CL EIA expression | 52 | $168.08 | **0.615** | **+0.945** | 0.60% | ✔ |
| F-C carry timing (H=21) | 12 | $80.74 | **0.295** | **+0.321** | 1.25% | ✔ |

**Upper-bound caveat (pre-registered, load-bearing):** the risk-N_eff deltas assume projected corr = 0 to both legs — the structural best case. A FAIL under it would have been decisive; a PASS means **"not excluded as a book leg,"** never "confirmed diversifier." The realized-corr and edge questions belong to the probes and, downstream, the frozen engine + the ratified Stage-8 gate (ADR `2026-07-20-stage8-variance-dominance-risk-neff-gate`, which any survivor still faces with *realized* numbers).

## Disclosed-prior scorecard (§4)

Prior: F-C most likely PASS, F-B least. Outcome: **all three passed**, so the prior was not embarrassed on direction but was uninformative at the pass/fail margin. The ρ ordering matched it exactly (F-C 0.295 < F-A 0.512 < F-B 0.615). One genuinely instructive inversion: **F-B carries the *highest* risk-N_eff delta (+0.945)** — under corr=0, a moderate-variance leg adds more risk breadth than a tiny-variance one (F-C +0.321), because risk-PR rewards variance *balance*, not variance minimization. The M-21 coordinates are two-sided: they kill dominance (ORB ρ=1.60) **and** reveal that too-small legs diversify little.

## Fork GO/NO-GO priority recommendation (→ 08-08 packet; judgment, not a frozen gate)

Ordering weighs the gated coordinates plus the reported (ungated) fields — session overlap, regime class, probe cost from the Q-INVENTORY-1 pricing:

1. **F-A ZN auction unwind** — strong delta (+0.787) at comfortable ρ margin; **zero structural session overlap** (post-auction ~13:00 ET vs the book's 08:00–12:00 NY morning); named 1a mechanism (dealer hedging unwind); cheapest probe (~$0, one session, no K until screened).
2. **F-C carry timing** — best ρ margin (0.295) and the only **regime-complementary** class (carry earns in the calm/range regimes the trend book bleeds in — the coordinate that would attack the H1 haircut cost); but the priciest probe (Databento daily bars + **1 family-K** + probe Pre-Q) and lowest projected risk-breadth gain at the reference weight. Its w*(ρ=1)=1.25% shows sizing headroom if δ-extraction succeeds.
3. **F-B CL EIA** — highest delta but its event window (**10:30 ET Wed) sits inside the book's session**, and its published form carries the informed-flow trap (R2) the unconditional re-expression must dodge first.

Funding any fork remains a **fresh operator decision** (Q-INVENTORY-1 closure language; nothing is opened here). All three probes stay δ-extraction probes — this projection says the *risk geometry* fits; it says nothing about edge.

## Phase-1b discharge — JPY micro symbology RESOLVED

Standing proxy-discipline flag (M6J vs MJY + quote inversion) discharged with data: **`M6J.FUT` does not resolve on GLBX.MDP3** (422 symbology_invalid_request); **`MJY.FUT` resolves** (MJYU6/MJYZ6 outrights + calendar spread live 2026-07-13). Quote convention verified by a cost-gated ohlcv-1d pull (estimate $0.00, billed $0.00): MJYU6 close 0.006188/0.006194 vs 6JU6 0.006188/0.006195 — **identical JPY/USD convention; the micro is a 1/10 6J clone; no inversion exists.** Thin listing (2 outrights) is noted for any future liquidity check. `reference/proxy-discipline.md` updated same session.

## Dispositions

- **Q-BOOKFIT-1 CLOSED-RESOLVED.** Fork priority table above rides the **2026-08-08 packet** next to the ratified gate's first binding use.
- **§C coordinate-field proposal** (add the composition coordinates to harvest intake): carried to the 08-08 packet per §6 — not applied unilaterally.
- **M-21 firing note:** this run is a **second use of the coordinate half** of M-21 (ρ + risk-N_eff arithmetic screening candidates before any engine spend — it ordered three forks for $0). The lesson's promotion criterion as written ("next composed-candidate evaluation carrying both a breadth verdict AND a frozen-engine bust verdict") is **not yet met** — no engine arm ran here. M-21 stays CANDIDATE; the paired-verdict promotion trigger is now live on whichever fork is funded first.
- **Accept-idle intact:** no sourcing occurred; no manifest opened; `discovery_manifests/` count unchanged.
- **K-accounting:** zero K consumed or banked.

## Lesson candidates

1. *(sharpens M-21, no new entry)* Under corr=0 injection, risk-N_eff delta is **non-monotonic in leg variance** — maximized when leg weekly variance ≈ book eigenvalue scale, falling toward zero for both tiny and dominant legs. The coordinate pair (ρ, Δ) therefore brackets a *band*, not a floor: ρ kills the top, Δ thins the bottom. Watch for a second instance before registering.

## §10 audit-hook discharge (run this session)

- Pre-reg commit `0fc1e05` predates first projection run ✔ (projection script authored after `4046bd2`)
- `discovery_manifests/` delta 0 ✔ · no `register_search open` ✔ · Q1–Q6 untouched ✔
- Reconcile gate: $273.28 vs $273 anchor, 0.1% ✔
- Proxy-discipline UNRESOLVED flag: updated to RESOLVED this session ✔
