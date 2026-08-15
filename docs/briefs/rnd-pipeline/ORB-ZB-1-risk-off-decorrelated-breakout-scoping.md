# Scoping + seed manifest — ORB-ZB-1: risk-off-decorrelated opening-range breakout on 30Y Treasury futures

**Status:** `CLOSED — FALSIFIED at Phase-0` (2026-07-20). Operator GO recorded (§8); Databento ZB pull `$0.00`; K=0 consumed. **P0.1 cost-law KILL on every window, and the ORB breakout has NEGATIVE gross edge on ZB** (full −0.048 R; Treasuries fade the 09:30 opening range rather than continue it — structural placebo p=0.001, breakouts lose on every within-day window). P0.2/P0.3 moot. Phase-1 never reached. Results: [`lab/archive/orb_zb_recon_2026-07/RESULTS.md`](../../../lab/archive/orb_zb_recon_2026-07/RESULTS.md). Disposition: append to [`rejected_candidates.md`](../../rejected_candidates.md); lock HELD (no `core/`/allocation/`dd_protection`/Pine touch).
**Candidate:** ORB-ZB-1 — opening-range breakout (the ORB-MNQ-1 construct) transplanted verbatim to the **ZB** (CBOT 30-Year U.S. Treasury bond) future.

> **⛔ VENUE-AVAILABILITY NOTE (added 2026-07-22 — does not change the closure).** **US Treasury futures are not tradable at the registered firm.** ZB/ZN/ZF/ZT/UB are absent from Tradeify's supported-products list ([`help.tradeify.co/en/articles/10468222`](https://help.tradeify.co/en/articles/10468222), article-dated 2026-05-20, re-verified 2026-07-22): the supported exchanges are CME/COMEX/NYMEX/CBOT, but the CBOT products offered are YM/MYM plus grains only, and the **sole rates products are EUREX bonds (FGBX/FGBS/FGBM/FGBL)**. This brief priced ZB against `firm_rules.cost_per_side_usd` and its P0.2 limb injects the candidate into the **live c1 (MYM+MNQ) book at the $100K basis** — i.e. it targets the c1 account, where the instrument cannot be traded at all.
>
> **This is additive, not a correction of the verdict.** The closure stands on its own P0.1 finding (negative gross edge in every window) and is unaffected. The note exists so a successor cannot read "the only thing wrong was the edge" and re-propose a Treasury construct for this venue: **at Tradeify, a Treasury candidate is venue-dead before its edge is even assessed.** The scoping economics above (`cost_per_side_usd`, RT ≈ 2–3 ticks) were in fact computed on the **Bulenox** $0.61 basis — see the closure's `config_fingerprint` — so they never described the registered firm either way.
>
> **Scope of the bar:** the whole Treasury complex, not just ZB. The sibling closures **H-ZNAUC-1** (ZN) and **RATES-EV-ZF-1** (ZF, closed 2026-07-21) name instruments that are equally unavailable. A rates construct intended for the c1 account must be expressed on **EUREX bonds** (a different complex, different session, additional exchange subscriptions) or routed to a different firm — either of which is a fresh pre-registration, never a re-run of this manifest.
**Lane:** venue-native reconstruction / cross-instrument transplant (kin to ORB-MNQ-1; ADR [`2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](../../adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) §7 active-research reconstruction lane), **not** external-literature harvest and **not** a locked-leg re-run.
**Loop of record:** STRATEGIC (discovery Stage-0). **Authored:** 2026-07-20 · Claude (Opus 4.8), operator-directed.

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-20)

- **`discovery_manifests/*.json` (all 7, parsed this session)** — the K-bank ledger. Verified by hand: **GC/MGC `disccamp0_gc_2010_18` `closed` K=3,177** (`c783533`, 2026-07-13) ⇒ gold family foreclosed (DSR floor 2.05 ≫ Cap 1.0, Requirement 3 permanent kill); ES bank 2 (`harv2026_001`+`h_od_1`); NQ/MNQ bank ~1–2 (`d5_nq_intraday_mom` closed + `orb_mnq_intraday_breakout` open); CL/6-family bank 1 each (`fb_eia`, `fc_carry`). **No ZB/ZN/ZF/ZT manifest exists ⇒ Treasury family K_banked = 0.** This read is the load-bearing instrument-selection input.
- **[`lab/analysis/orb/orb_mnq_2026-07/RESULTS.md`](../../../lab/analysis/orb/orb_mnq_2026-07/RESULTS.md) @ `9620138`** (2026-07-16) — the construct being transplanted. NAS100-ORB-30: 30-min opening range (09:30–10:00 ET), breakout entry both sides, exit-at-close (09:30–15:45 ET); cost model `cost_R = RT_cost_pts / OR_range`, cost-law `mean gross edge_R ≥ 4× mean cost_R`. MNQ numbers: gross +0.0823R (t2.97), cost_R 0.0155R, **ratio 5.31× full / 8.10× 2021+**; OR-range/RT ≈ **82:1** (90.8pt / 1.11pt) — the cost-cheap geometry that let it clear where D5/H-OD-1 died. Engine `orb_universe_2026-06-22/orb_lib.py` reused verbatim (loader-only change).
- **[`lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md`](../../../lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md) @ `9620138`** — the kin-candidate admission pattern (CANDIDATE @1.00×, no `core/lifecycle.py` write, standing caveats). ORB-MNQ was admitted as a **standalone** candidate but is **regime-common-mode + high-variance/risk-dominant** — the exact properties this candidate is designed to *not* share.
- **[`docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md`](../../adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md) @ `7af4224`** (`Accepted`) — the binding gate this candidate's thesis must clear: composed-book admission requires `n_eff_risk_delta ≥ τ_risk` (positive dependence-delta **not** sufficient) + `ρ = candidate daily-$std / book daily-$std < 1.0`. **ORB-MNQ-1 FAILED this** (risk-delta +0.00; ρ = 438/273 = 1.60). ORB-ZB-1 exists to clear it.
- **[`docs/adr/2026-06-07-decompound-remc-hold.md`](../../adr/2026-06-07-decompound-remc-hold.md) @ `ba943a1`** — the book's structural weakness this candidate targets: locked config HELD but regime-split (2020-23 chop bust 9–13% vs 2023-26 trend ~0%); **no static counterbalance is regime-robust**. Q-COMPOSE-1 extended "no static counterbalance" from sizing → breadth. The book has no leg whose P&L lands in its own drawdown window.
- **[`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md) @ `268851b`** — §1 the five admission requirements (Req 3 family-K permanent kill; Req 2 no-cohort-δ ⇒ UNSCREENABLE → δ-extraction route; Req 5 cost-law inequality); §2.1 Tier-A = low-frequency large-per-event-δ (the only surviving class); the confirm-not-mine K discipline.
- **[`docs/rejected_candidates.md`](../../rejected_candidates.md) @ `a3e6cdb`** — dedup + the 5th-leg-domain SNAG bar (2026-07-01). Nearest prior entry: *rates-intraday **mean-reversion** on MICRO10Y/2YY* (chop-native, FALSIFIED). **Not a collision** — that is a fade (MR) on a yield micro; this is a **breakout** on the 30Y bond price future. Different mechanism class, different instrument. Domain-SNAG-bar disposition flagged for operator in §1.
- **[`docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md`](../pre-registration/D5-NQ-intraday-momentum-preregistration.md) @ `fb9b9c9`** — structural model for this brief and for the Phase-1 §R freeze it sketches.
- **H-ZNAUC-1 δ-extraction precedent** ([`docs/briefs/closures/H-ZNAUC-1-closure-screen-fail.md`](../closures/H-ZNAUC-1-closure-screen-fail.md), STATE 2026-07-20) — the Phase-0 shape: operator-authorized own-cohort δ-extraction, native Databento, $0.00, **K consumed 0** (measurement, not a registered search). Phase-0 here is that same no-K probe.

---

## §1 — Context (the symptom this probe addresses)

**The vise (synthesis of the whole graveyard).** Two walls have killed almost every candidate, and they point opposite ways:

- **Cost-law** admits only *large-per-event-δ / directional-capture* mechanisms (breakout, trend). Every small-δ class — MR, fade, carry, event-drift, calendar — is structurally sub-cost on the micros (D5, H-OD-1, H-ZNAUC-1, F-B, F-C, USOIL/EURUSD/USDCAD fades, the DISC-CAMP-0 mine 0/6).
- **Variance-dominance / co-occurrence** (Q-COMPOSE-1 + decompound-HOLD) rejects any leg that adds dollar-variance without lifting **risk N_eff**, or whose drawdown co-occurs with the book's 2020-23 chop/risk-off window.

The only mechanism ever to clear cost-law is **ORB-MNQ-1** (a breakout). But the book is *already* entirely large-directional-capture index momentum — so the one cost-viable class is **variance-redundant** with the book (ORB-MNQ failed the Stage-8 risk-N_eff gate: risk-delta +0.00, ρ 1.60). Cost-viable ⟹ redundant. That is the vise.

**The one direction the vise leaves open.** A mechanism that is *both* (a) large-per-event (clears cost-law → breakout class) *and* (b) **counter-cyclical** to a long-biased index-momentum book (clears the Stage-8 risk-N_eff gate + doesn't co-draw in H1). The instantiation: transplant the one construct that works (ORB) off Nasdaq and onto a **risk-off-benefiting** instrument, where the same breakout that survives cost now lands its P&L in the exact window the book bleeds (flight-to-safety). ORB-on-Nasdaq is redundant; ORB-on-a-haven plausibly is not.

**Why ZB and not gold.** Gold (GC/MGC) is the archetypal haven and the natural first pick — but §0 verified its family K-bank is **3,177** (DISC-CAMP-0 legacy) → DSR floor 2.05 ≫ Cap 1.0 → dead on the Requirement-3 wall before any run. The K-clean haven family is **Treasuries** (ZB/ZN/ZF/ZT, K_banked = 0). ZB (30Y) is chosen over ZN (10Y): most duration ⇒ largest range (best cost-law odds among rates) and most flight-to-safety-reactive (best decorrelation thesis).

**Honest prior (this is not a hot lead).** Index micros have unusually large intraday range relative to cost (MNQ OR/RT ≈ 82:1); Treasuries are tighter-range and more intraday-mean-reverting, so **cost-law is the dominant kill risk and the prior on an ORB edge existing on ZB is < 50%.** The probe is justified not by a strong prior but by **asymmetric payoff at near-zero cost**: ~$0 data, K=0, one session; a PASS is the decorrelated leg the book structurally lacks; a clean FAIL banks a measured ZB-ORB cost-law number in the rejection registry. This is the "cheapest falsifier before authoring" discipline, not an edge claim.

**Standing-doctrine connections (and one open flag).** Lane = venue-native reconstruction (ADR 2026-07-16), the same lane that admitted ORB-MNQ-1 after the free-data 5th-leg domain SNAG-closed. **Operator flag:** ORB-ZB-1 is a *new* instrument+mechanism (no prior in-house ZB work), so it sits closer to the SNAG-closed "new 5th-leg" domain than ORB-MNQ did (which reconstructed an existing NAS100 cohort). I read it as clearing the domain bar via door-2-adjacent (large-δ breakout class on the futures venue — a class the free-data chop-native search structurally never tested), but this is a **judgment call I am surfacing, not assuming** — §8 asks you to ratify the lane placement, not just the spend.

---

## §2 — Seed manifest (strategy_harvest §5 template)

```markdown
# Harvest-seed manifest — ORB-ZB-1

- admission-date: 2026-07-20
- requirement-1 path: 1a (named mechanism) — with a disclosed grounding caveat
- mechanism (req 1a): opening-range breakout captures intraday directional
  continuation seeded by overnight/pre-open information arrival + positioning
  adjustment concentrated at the RTH open; the counterparty is liquidity
  providers / late responders fading the initial thrust who are run over by
  continuation. CAVEAT (disclosed): the specific dealer-short-gamma hedging
  story is equity-index-cohort-specific (Baltussen 2021); for Treasuries the
  grounding is the more general information-arrival continuation claim —
  weaker than the equity cohort. This is a mechanism-plausible transplant,
  not a mechanism-proven one; Phase-0 measures whether the footprint exists.
- source + tier: in-house construct transplant (ORB-MNQ-1 RESULTS @9620138 /
  NAS100 N1). No external ZB literature cohort ⇒ see req-2.
- target instrument + family (req 3): ZB / ZB-family (CBOT 30Y T-bond future)
- K_banked(family): 0 (no ZB/ZN/ZF/ZT manifest; verified 2026-07-20 against
  discovery_manifests/ — §0)
- K_intrinsic (confirm-not-mine): 1 — single fixed ORB-30 construct transplanted
  verbatim (30-min OR, breakout both sides, exit-at-close). NO window/threshold/
  session-anchor search. A different OR window or session anchor is a DIFFERENT
  construct requiring a fresh manifest, never a Phase-0 sweep.
- K_eff + floor(K_eff): K_eff = 1 → floor 0.65 (most beatable; below S_B median)
- δ/σ (req 2): UNSCREENABLE at admission — no ZB cohort exists. Cross-instrument
  δ transplant from MNQ is INADMISSIBLE (req 2). Routed to a Phase-0 in-house
  δ-extraction on ZB's OWN cohort (the req-2 relief valve; D7/H-ZNAUC-1 precedent).
- N + event frequency (req 4): ~1 signal/session, ~250/yr ⇒ N ≈ 1,500+ on the
  native ZB era (2019→2026). Daily frequency clears req-4's structural bar;
  numeric power computed at Phase-0 once δ is extracted.
- power: PENDING Phase-0 δ.
- dedup attestation: rejected_candidates.md + closed manifests + rejected_signals.md
  checked 2026-07-20. Nearest dead class = "rates-intraday-mean-reversion on
  MICRO10Y/2YY" — a FADE (MR) on a YIELD micro; ORB-ZB-1 is a BREAKOUT on the
  30Y PRICE future. Different mechanism class AND instrument ⇒ not a collision.
- screen verdict: UNSCREENABLE(req-2: no cohort δ → Phase-0 δ-extraction probe)
- operator ratification: PENDING (this brief requests the Phase-0 GO, §8)
```

---

## §3 — Phase-0 cheap-falsifier battery (the "cost of one division" gate; all three from one ~$0 run, K=0)

Single native-ZB δ-extraction (Databento GLBX.MDP3 `ZB` continuous, 2019→2026, resampled 15m ET, `orb_lib.py` verbatim), producing all three screens. Any limb failing closes Phase-0 FALSIFIED — the confirmation campaign is never opened.

| # | Screen | Measure | PASS condition | Kills / precedent |
|---|---|---|---|---|
| **P0.1 — cost-law reachability (Req 5)** | δ-extraction: mean gross ORB-30 edge_R, ZB `cost_R = RT_pts/OR_range`, ratio | **edge/cost ≥ 4.0×** at ZB economics (`firm_rules.cost_per_side_usd` + ≤1-tick slip; RT ≈ 2–3 ticks) | The dominant kill risk. D5/H-OD-1/H-ZNAUC-1 all died here; ZB's tighter OR/RT geometry (≪ MNQ's 82:1) makes this a genuine coin-flip |
| **P0.2 — decorrelation pre-flight (Stage-8 ADR)** | inject ZB-ORB into the live c1 (MYM+MNQ) book covariance: `ρ = ZB-ORB daily-$std / c1-book daily-$std` (at a bound weight, $100K basis) + `n_eff_risk_delta` | **ρ < 1.0 AND n_eff_risk_delta > 0** | The exact gate ORB-MNQ FAILED (ρ 1.60, risk-delta +0.00). If ZB-ORB also fails this, it is another redundant leg — close |
| **P0.3 — tail-timing co-occurrence** | per-year + per-regime net P&L; locate the worst drawdowns vs the book's 2020-23 chop/risk-off window | worst-DD does **NOT** concentrate in the book's H1/risk-off window | decompound-HOLD + the domain-SNAG bar's co-occurrence clause (rates-MR, dispersion, chop-native all died here) |

**Ordering (cheapest-decisive first):** P0.1 runs first and alone can close the probe. P0.2/P0.3 are only computed if P0.1 clears — they need the ZB return series P0.1 produces. P0.2's ρ is a seconds-to-compute division (the closure lesson that "the cheap $-std falsifier ran before the expensive engine and was decisive").

---

## §4 — Falsifiable hypothesis (H-ORB-ZB-0; binary)

**H-ORB-ZB-0 — if** the fixed ORB-30 construct on native ZB clears **P0.1 cost-law ≥ 4.0×** *and* **P0.2** (`ρ < 1.0` with `n_eff_risk_delta > 0` on the c1 book) *and* **P0.3** (no H1/risk-off drawdown concentration), **then** ORB-ZB-1 graduates to a Phase-1 K=1 confirmation campaign (register_search open + §R freeze + full Stage 5/6/7/8); **otherwise** it closes FALSIFIED and is appended to `docs/rejected_candidates.md` with the measured cost-law ratio and (if reached) the decorrelation numbers.

**Numeric accept threshold:** graduate iff `edge/cost ≥ 4.0×` AND `ρ < 1.0` AND `n_eff_risk_delta > 0` AND worst-year drawdown not in {2020, 2021, 2022}∩(book-DD window). **Falsified** on any one limb failing. The decorrelation limbs (P0.2/P0.3) are evaluated only conditional on P0.1 passing; a P0.1 failure closes on cost-law alone (the redundancy question is moot if there's no edge to add).

---

## §5 — Forbidden moves (each genuinely tempting)

- **Sweeping the OR window / session anchor to find one that clears cost-law on ZB** — ZB's information flow may concentrate at 08:30 (data) rather than 09:30 (equity open); it is tempting to try both. That is a K-inflating search that voids the K=1 screen. One anchor is pre-committed (09:30 ET, faithful-transplant); a different anchor is a fresh manifest, not a Phase-0 branch (the D5 "H2 dropped at freeze" discipline).
- **Transplanting the MNQ δ/σ to compute ZB power** — inadmissible (Req 2, cross-instrument). ZB's δ must come from ZB's own cohort (the entire point of the Phase-0 extraction).
- **Substituting ZN/UB mid-probe if ZB's cost-law is marginal** — best-of-N over rates instruments. ZB is the pre-committed anchor; UB (bigger range) is a *documented alternative requiring its own fresh pre-reg* if ZB fails, never a same-probe swap.
- **Reading a P0.2 dependence-N_eff (correlation) positive as sufficient** — the precise error that admitted ORB-MNQ. Risk-N_eff-delta is the binding statistic; correlation breadth without risk breadth is the falsified pattern (Stage-8 ADR §5).
- **Opening register_search / pulling the confirm panel before Phase-0 clears and you re-GO** — Phase-0 is a no-K measurement; Phase-1 K binds only on a fresh §R-frozen GO. A pull before that voids the campaign.
- **Quoting a Phase-0 δ-extraction PASS as an edge** — a δ-extraction is in-sample by construction; it licenses the confirmation campaign, it never blesses a candidate (the D5 screen-PASS asymmetry).
- **Retiring the domain-SNAG-bar question by assertion** — §1 flags it as an operator call; do not treat lane placement as settled by this brief.

---

## §6 — Gate criteria (binary)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED (graduate)** | P0.1 ≥ 4.0× AND P0.2 (ρ<1.0, risk-Δ>0) AND P0.3 (no H1-window DD concentration) | Author Phase-1 Stage-0 pre-reg (K=1, §R attestation per D5 model) → fresh operator GO → register_search open → confirm campaign |
| **FALSIFIED (close + register)** | Any P0 limb fails | Close; append ORB-ZB-1 to `rejected_candidates.md` with measured cost-law ratio (+ decorrelation numbers if reached); K=0 spent; ZB family bank stays 0 |
| **AMBIGUOUS** | ZB native era N too low for a stable δ/cost estimate, or data-quality defect | Closure names the re-test condition; no in-place threshold edit |

No calendar hard-date beyond the parent programme's 2026-11-08 idle review; Phase-0 is a single-session run once GO'd.

---

## §R — Reachability attestation (SKELETON — populated only at the Phase-1 freeze)

The HARV HARD gate (ADR 2026-07-13) requires a per-clause plausible-true-world reachability attestation **before register_search open**. It is **not** required for the Phase-0 no-K δ-extraction (measurement, not a registered search — H-ZNAUC-1 precedent). It is drafted here as a skeleton so the Phase-1 path is visible:

- **R.1 — confirm gate (net Sharpe ≥ 0.65 at K=1):** reachable *iff* the Phase-0-extracted ZB δ/σ implies a gross Sharpe > 0.65 with plausible cost survival. **This is exactly what P0.1 measures** — Phase-0 is the reachability evidence, so R.1 cannot be honestly written until Phase-0 returns a δ. (Contrast: if P0.1 fails 4×, R.1 is *unreachable* and Phase-1 is correctly never opened.)
- **R.2 — placebo gate:** the ORB within-day placebo (arbitrary intraday windows, `placebo_within_day`) — disjoint from the OR window by construction, no Q-HARV-0 conditioning-overlap floor. Reachable under a true intraday-continuation world (placebo ≈ 0).

---

## §7 — Run protocol

0. **This brief:** manifest + Phase-0 battery frozen. **Operator reviews §8 → GO/NO-GO on Phase-0.**
1. **On Phase-0 GO:** single native-ZB δ-extraction (Databento `db_fetch estimate` → cost-gate → pull ZB continuous 2019→2026; ~$0 expected, GLBX bar tier) → `orb_lib` verbatim → P0.1 cost-law, then (if pass) P0.2 ρ/risk-N_eff on the c1 covariance + P0.3 per-year timing. **K = 0** (measurement). Results land in `lab/archive/orb_zb_recon_2026-07/`.
2. **On P0 RESOLVED only:** author the Phase-1 Stage-0 pre-reg (D5 model — §R fully populated with the extracted δ, K=1) → **fresh operator §R GO** → `register_search open --lane mechanism-first` → confirm panel pull → Stage 5/6/7/8 → survivor-scoring gate G0–G8 vs prop envelope → (only then) lifecycle CANDIDATE intake.
3. **On P0 FALSIFIED:** append to `rejected_candidates.md`; done.

---

## §8 — Operator GO gate (Phase-0 δ-extraction only; DRAFT until filled)

```
PHASE-0 GO: 2026-07-20 / JA  (operator chat: "Run the Phase-0 δ-extraction")
Authorized: a single-construct, no-K, ~$0 native-ZB ORB-30 δ-extraction (P0.1/P0.2/P0.3).
Lane-placement ratification (§1 flag): MOOT — candidate FALSIFIED at Phase-0, never reached
  admission (where the 5th-leg-domain SNAG bar would bind); recorded un-adjudicated.
Did NOT authorize (none occurred): register_search open, K spend, the Phase-1 confirm panel,
  or any live/Pine/allocation/dd_protection/ACTIVE_FIRM touch. Databento spend $0.00 confirmed.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Phase-0 GO unfilled ⇒ no ZB manifest and no orb_zb pull may exist yet.
grep -n "PHASE-0 GO: ____________" docs/briefs/rnd-pipeline/ORB-ZB-1-risk-off-decorrelated-breakout-scoping.md \
  && echo "GO unfilled — no register_search / pull for ZB" || echo "GO filled"

# 2. ZB family bank is 0 (Requirement-3 basis; re-derive, do not trust prose).
ls discovery_manifests/ | grep -iE 'z[bnft]|treasury|bond' && echo "ZB manifest EXISTS — recheck K" || echo "ZB bank 0 confirmed"

# 3. Gold really is foreclosed (the finding that redirected the target).
python -c "import json; print('GC/MGC K =', json.load(open('discovery_manifests/disccamp0_gc_2010_18.json'))['K'])"  # expect 3177

# 4. K_intrinsic pinned at 1, single construct (no sweep).
grep -n "K_intrinsic (confirm-not-mine): 1\|single fixed ORB-30 construct" docs/briefs/rnd-pipeline/ORB-ZB-1-risk-off-decorrelated-breakout-scoping.md

# 5. Dedup: the nearest dead class is MR-on-yield-micro, not this.
grep -n "rates-intraday-mean-reversion" docs/rejected_candidates.md  # exists; different class (fade vs breakout)

# 6. Stage-8 risk-N_eff gate is the binding decorrelation statistic (not dependence).
grep -n "n_eff_risk_delta" lab/research_utils/breadth.py  # the gate has a real input

# 7. Construct engine reused verbatim (no reimplementation drift).
grep -n "def orb_backtest\|def placebo_within_day\|def session_panel" lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python <brief-authoring>/scripts/check_brief.py docs/briefs/rnd-pipeline/ORB-ZB-1-risk-off-decorrelated-breakout-scoping.md --type inquire
# Expected: all 6 checks PASS

# §0 anchors current
git log -1 --format='%h %ci' -- lab/analysis/orb/orb_mnq_2026-07/RESULTS.md                      # 9620138
git log -1 --format='%h %ci' -- docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md  # 7af4224
git log -1 --format='%h %ci' -- docs/adr/2026-06-07-decompound-remc-hold.md                  # ba943a1

# K-bank ledger reproduces the instrument-selection finding
python -c "import json,glob; [print(p, json.load(open(p))['status'], json.load(open(p))['K']) for p in glob.glob('discovery_manifests/*.json')]"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-20 | Scoping + seed manifest authored; Phase-0 δ-extraction GO requested. Target redirected gold→ZB on the verified K-bank ledger (gold K=3,177 foreclosed, Treasury bank 0). Cost-law disclosed as the dominant kill risk (low prior, asymmetric-payoff justification). | Joshua (direction) + Claude (Opus 4.8) |
| 2026-07-20 | Operator GO (§8); ZB.v.0 pulled `$0.00`; Phase-0 run. **CLOSED FALSIFIED** — P0.1 cost-law KILL every window, negative gross edge (full −0.048 R); ZB fades the 09:30 OR (placebo p=0.001). K=0. Predicted low prior confirmed; asymmetric-payoff probe returned a clean mechanism finding. RESULTS + rejected_candidates disposition. | Joshua (GO) + Claude (Opus 4.8) |
