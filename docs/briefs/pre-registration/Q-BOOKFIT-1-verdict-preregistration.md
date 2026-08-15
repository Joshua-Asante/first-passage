# Q-BOOKFIT-1 — verdict pre-registration (FROZEN before Phase 1–2)

**Frozen:** 2026-07-20, operator-authorized ("proceed with pre-reg → Phase 1–3", chat 2026-07-20)
**Parent brief:** [`../Q-BOOKFIT-1-fork-composition-coordinate-triage.md`](../Q-BOOKFIT-1-fork-composition-coordinate-triage.md)
**Rule:** nothing in §B–§E moves after any projection number is computed. Amendment = close AMBIGUOUS + fresh brief (Trap #12).

---

## §A — Objects under test (fixed)

The three priced probe forks from the Q-INVENTORY-1 closure (`FALSIFIED` 2026-07-17), exactly as priced there — no additions, no substitutions:

| Fork | Mechanism / instrument | Cited structural basis (already-cited record only) |
|---|---|---|
| F-A | ZN Treasury-auction dealer-hedging unwind | Smales *A&F* 2021; ~36 events/yr; auction-anchored (~13:00 ET), intraday bounded hold |
| F-B | CL EIA-inventory unconditional event expression | Rousse–Sévi 2019 / Ye–Karali 2016; 52 events/yr (Wed 10:30 ET), intraday bounded hold |
| F-C | Carry timing-δ (6J/6E/CL) | Carry-class canonical implementation (monthly-rebalance, continuous hold; Koijen et al. class literature) |

Book under test: the live c1 2-leg book (Striker DJ30→MYM + Striker NAS100→MNQ), weekly panel built from the F3-archived edition CSVs in `core/data/tv_exports/cme/` (2026-07-17 exports), at the Q-COMPOSE-1 $100K basis.

## §B — Frozen projection formulas

1. **Reference weight (precedent-anchored):** w = 0.37% → per-block risk unit `R$ = 0.0037 × $100,000 = $370`. Same weight/basis at which ORB was tested and killed (Q-COMPOSE-1); not tunable.
2. **Independent-risk-block count `N_b` per year (structural):**
   - Episodic intraday mechanism → `N_b = events/yr` (F-A: 36; F-B: 52).
   - Continuous-hold mechanism → `N_b = 252 / H`, H = median holding period in trading days from the class-canonical implementation (F-C: H = 21, monthly rebalance per carry-class literature).
3. **Projected daily $-std:** `σ_d = R$ × σ_R × sqrt(N_b / 252)` with **σ_R = 1.0** (per-block P&L std ≈ 1R for a stop-bounded block; disclosed structural assumption, sensitivity in §E).
4. **ρ (variance-dominance ratio):** `ρ = σ_d / σ_book,d`, σ_book,d = measured daily $-std of the 2-leg panel. **Reconcile gate:** σ_book,d must land within ±10% of the Q-COMPOSE-1 closure anchor $273; if not, HALT (panel-basis mismatch), no verdict.
5. **Projected risk-N_eff delta:** inject a synthetic weekly variance `v = (σ_d × sqrt(5))²` as a third diagonal component with **projected correlation 0 to both legs** (structural best case — the projection cannot estimate realized corr without a return series; corr=0 maximizes the diversification read, so a FAIL under it is decisive and a PASS is an upper bound, stated as such in the closure). `n_eff_risk_delta = PR({λ1, λ2, v}) − PR({λ1, λ2})`, λi = eigenvalues of the measured 2-leg weekly covariance, PR = participation ratio (breadth.py definition, `d83e0f9`).
6. **Reported, not gated:** structural session overlap vs the book's 08:00–12:00 EST window (07-13 companion fields); regime class (trend / reversion / carry / event-flow); episodic flag (in-market <5% of session clock).

## §C — Frozen pass criteria (per fork)

From the brief §6 / ADR `2026-07-20-stage8-variance-dominance-risk-neff-gate` (`Accepted`):

- **PASS** = `ρ < 1.0` **AND** `n_eff_risk_delta > 0`, both at w = 0.37%.
- **FAIL** = either criterion violated.
- **UNSCOREABLE** = the structural signature (events/yr or H, session window) cannot be assembled from the already-cited record without a new pull or new sourcing.

## §D — Verdict table (verbatim from brief §6)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | ≥1 fork PASS, all three scoreable | Fork GO/NO-GO priority order → 08-08 packet; §C-field proposal for harvest intake |
| `FALSIFIED` | All three FAIL, all scoreable | Breadth closed at current supply; 11-08 idle review inherits; sizing + live data remain the book's only levers |
| `AMBIGUOUS-HOLD` | ≥2 forks UNSCOREABLE | Re-test 2026-11-08; missing inputs named to the idle review |

**Disclosed prior (so it can be embarrassed):** F-C most likely PASS; F-B least likely.

## §E — Sensitivity annex (reported alongside any verdict; gates nothing)

- ρ at σ_R ∈ {0.5, 1.0, 1.5} for all forks.
- F-C additionally at H ∈ {5, 21, 63}.
- Weight w* at which ρ = 1.0 per fork (disclosure only; weight-shopping forbidden by brief §5).

## §F — Execution constraints

Zero pulls for the projection itself; zero K; zero manifest opens; Phase-1b symbology resolution (M6J vs MJY) may use free databento symbology/metadata and a cost-gated micro pull ≤ $0.10 with prior estimate (it discharges a standing flag; it feeds no projection number).
