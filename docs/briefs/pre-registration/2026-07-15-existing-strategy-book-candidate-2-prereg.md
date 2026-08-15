# Pre-registration — Class-S existing-strategy book candidate #2: 3-leg MYM+MNQ+6J (Aegis-inclusive) native-futures book

> ⚠ **2026-07-22:** this frozen body's "already-discharged four-firms ADR §4" premise was
> **WITHDRAWN** — see [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md).
> §4 is undischarged (hard date 2026-11-08 unchanged). Body left frozen as written (Trap #12); this Q's own verdict is unaffected.

**Status:** `FROZEN` (operator signed §9, 2026-07-15). No item below changes after
signature or after any frozen-tier result is seen (Known Trap #12 — amendments require
closing this candidate and opening a fresh one under the ADR's per-candidate governance).
**Candidate class:** pre-registered existing-strategy book (Class S), admitted by
[`docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md`](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md) (`Accepted` 2026-07-15).
**Gate of record (unchanged, cited not re-decided):**
[`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) (FROZEN 2026-07-13).
**Falsifier status (explicit, up front):** the four-firms ADR §4 primary falsifier is
**already discharged** by candidate #1 (S2, 2-leg MYM+MNQ — `RESOLVED (DISCHARGED)`,
2026-07-15). This candidate carries **no discharge urgency** and the ADR §4 early-fail
branch (which only arms off the *first* candidate's all-four-tier failure) is permanently
moot regardless of this candidate's outcome. Candidate #2 is admissible purely as a
**normal per-candidate operator decision** (ADR §5: "each candidate consumes an explicit
operator decision") — it exists to score the one remaining pre-committed composition axis
(S1) now that its Aegis-input blocker is resolved, feeding the fuller evidence base ahead
of any future G8/portfolio-construction choice between the 2-leg and 3-leg books, not to
re-clear an already-cleared gate.
**Aegis declaration (explicit, mirrors candidate #1's ADR §5 obligation in reverse):**
**this candidate DOES contain an Aegis leg** — JPY-futures (6J), panel-of-record **ae744**,
at risk **0.75%** (half the locked CFD 1.50%, matching the only measured Aegis-bearing
prior inside any ceiling — bustcut row 2b). The BEPAD-TEST provenance caveat on `ae744`
(§0) is carried forward as a standing, unresolved caveat on this candidate's own book, not
merely on a calibration reference as it was for candidate #1.
**Loop of record:** STRATEGIC.
**Feeds:** the four-firms ADR §4 primary falsifier (already discharged; this candidate adds
evidence, not a fresh discharge attempt) — hard date **2026-11-08**, 08-08 progress check.
**Authored:** 2026-07-15 · Claude Code (Sonnet 5), operator-directed ("draft the pre-req for
Class-S candidate #2").

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-15)

All content-read from the working tree; per-file anchors (`git log -1 --format='%h %ci'`):

- **[`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) @ `be6dda6`** —
  unchanged since candidate #1. Part A **bust ≤ 3.0%** (daily+static+trailing via
  `preflight.summarize_outcomes`) **+ P(pass) ≥ 50%** with finite median inside horizon,
  **Run-2 gated**, frozen cross-section exactly `Bulenox_100K · Tradeify_Select_100K ·
  MFFU_Rapid_100K · BluSky_Premium_100K`; discharge = **≥2 distinct firms incl. ≥1
  `trailing_locking`**; seeds **42/123/2026**, 10k × 3, horizon 1500, inactivity disabled,
  `dd_protection` OFF (§7(6)). **Nothing here re-decides any of it.**
- **[`docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md`](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md) @ `507761a`** —
  `Accepted`. §4: early-fail branch is scoped to "the *first* pre-registered existing-strategy
  candidate" — already resolved (candidate #1 DISCHARGED, not early-fail); does not re-arm
  on this candidate's result. §5: "each candidate consumes an explicit operator decision" —
  the governing clause for opening candidate #2 post-discharge.
- **[`docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md`](2026-07-15-existing-strategy-book-candidate-1-prereg.md) @ `58fff1d`** —
  read in full. §1 composition-decision record: three axes inventoried (Q-KBUDGET-1
  Phase-1) — **S1 (3-leg, Aegis ~0.75%-class)**, S2 (2-leg MYM+MNQ, = candidate #1), S3
  (Aegis solo). Candidate #1 sequenced S2 first on higher measured headroom; **"S1 remains
  available as candidate #2 either way, and its Aegis input (ae744 pin) is already
  resolved."** §7 prior-look table rows 1-9 — this pre-reg's own §7 below reproduces them
  plus candidate #1's now-real G4 result and the regime-gate rider finding.
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md) @ `5fd291c`** —
  candidate #1's actual (not coarse-extrapolated) G4 result: `RESOLVED (DISCHARGED)` —
  Tradeify_Select_100K bust 2.65%/pass 97.34% PASS, MFFU_Rapid_100K bust 2.64%/pass 97.35%
  PASS (both `trailing_locking`); Bulenox 3.51% FAIL, BluSky 4.44% FAIL. §3 calibration
  reference (3-leg **full-Aegis @ 1.50%**, ae744) already ran in the same session: **0/4
  tiers clear** (Tradeify Run-2 17.88%) — ceiling discriminates as designed, AMBIGUOUS did
  not fire. **This candidate does not re-run that calibration reference** (§3 below cites
  it, not a duplicate run) — it is a different book (0.75% Aegis risk here vs 1.50% there).
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/REGIME_GATE.md`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/REGIME_GATE.md)** —
  candidate #1's regime-robustness rider (gate §7(7)), status `HALF_ONLY (bootstrap
  deferred)`: half-panel split real result — **H1 (2020–2023) bust 4.36–4.37% FAILS the
  3.0% ceiling on both discharging tiers; H2 (2023–2026) bust ~1.70% PASSES.** Does not
  overturn candidate #1's mechanical DISCHARGED read but stands as a caveat. Cited here as
  context, not as a re-litigation input — candidate #2 is a different book and will need
  its **own** regime-robustness rider if it ever discharges anything.
- **[`lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md`](../../../lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md) @ `eba5030`** —
  this candidate's **direct prior**: sensitivity row **"2b ae744 @ 0.75%: pass=97.98%
  bust=2.02% p99=4.10% med=152d aegAttr=47.8%"** (50K geometry-only, 3-leg, striker 0.70% +
  striker_nas100 0.37% + aegis 0.75% on the clean `ae744` panel — **exactly this
  candidate's composition**, just at 50K instead of the frozen 100K band). Also on this
  panel family: Test 1 (2-leg, = candidate #1's direct prior, 50K bust 0.76%); Test 2 (3-leg,
  `5274c` @ 0.75% — the disqualified/artifact panel, 50K bust 39.43%, **not** this
  candidate's prior — do not conflate rows 2 and 2b).
- **[`lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md`](../../../lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md) @ `eba5030`** —
  panel construction of record (decompound static $200K via roe; `pin_r_basis(full_stop_mean)`):
  striker 1R **$2,535.61 (n=8)** scale 0.5521; striker_nas100 1R **$5,899.32 (n=19)** scale
  0.1254 — identical to candidate #1, reused verbatim (zero new variants on these two legs).
  3-leg 50K→100K deterioration factor **×1.71** (10.33% → 17.70%, at Aegis 1.50%) — the
  same coarse multiplier candidate #1's §1 applied; used again below for the 0.75% case,
  non-bindingly.
- **[`lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md`](../../../lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md) @ `507761a`** —
  operator pick: **ae744**, 1R basis **decompound @ $200K full_stop_mean $2,912.96 (n=11)**,
  no fallback, no thin-cohort warning. §2 classification: "ae744 — PARTIALLY UNKNOWN.
  Filename carries BEPAD-TEST... CSV headers contain no Pine input metadata... **not
  mechanically verified**... operator must confirm whether the BEPAD-TEST label reflects
  intended Pine inputs." Operator accepted the pick "despite PARTIALLY UNKNOWN exact Pine
  inputs" (§2, 2026-07-15) — that acceptance covered admitting ae744 as a prop-candidate
  panel; it did not retroactively resolve the provenance question, which stays open and is
  disclosed again here because this candidate (unlike #1) puts Aegis on the book itself.
- **`core/firm_rules.py` @ `a53ee99`** — unchanged since candidate #1 (re-verified this
  session). All four frozen tier configs present; `ACTIVE_FIRM="FXIFY"` untouched; per-firm
  `cost_per_side_usd` + `consistency_rule_pct` (Tradeify 40 / MFFU 50 / BluSky 34; Bulenox
  none at eval) present.
- **`lab/discovery/prop_survivor_scoring.py` @ `97011c1`** — unchanged since candidate #1.
  `score_candidate()` accepts pre-built scaled arrays; no 1R guard on this path (caller
  responsibility — §8.3 below adopts the same binding guard candidate #1 used).
- **`ops/prop_envelope_default.md` @ `6b94032`** — §2 contract unchanged: pre-register the
  deployable decomposition + frozen binary `DEPLOYABLE-DEFAULT-ENVELOPE` criterion;
  consistency annotation; excursion reporting; exposure-coordinates annotation (§2.5).
- **Panel bytes** — `core/data/tv_exports/cme/SHA256SUMS` (re-verified this session, all
  three present, hashes unchanged since candidate #1):
  `9acfa297…ce01b9e *Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv`;
  `8884e6dd…dc6419 *Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv`;
  `e82a2c25…d148ca38 *Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-11_ae744.csv`.

---

## §1 — Context + composition decision record

Candidate #1 (S2, 2-leg MYM+MNQ) closed `RESOLVED (DISCHARGED)` 2026-07-15 — the four-firms
ADR §4 falsifier is satisfied and rail/account/go-live stay separately gated regardless of
what happens here. Its own §1 explicitly reserved S1 (this candidate) for later: "S1 remains
available as candidate #2 either way, and its Aegis input (ae744 pin) is already resolved."
That reservation is now being exercised, per operator direction, as a normal per-candidate
decision under ADR §5 — not because anything is blocking on it.

**Candidate #2 = S1 (3-leg, Aegis-inclusive), composition fixed by the only measured
Aegis-bearing prior that sits inside the frozen ceiling at any risk level:**

- Row 2b of the bustcut sensitivity block (`ae744 @ 0.75%`, 50K geometry-only) measured
  bust **2.02%** — the only Aegis-bearing configuration examined to date that clears 3.0%
  at 50K. Row 2 (full 1.50% Aegis, keep 3 legs) measured 39.43% on the disqualified `5274c`
  panel and is not this candidate's composition; the clean full-1.50% equivalent is row 5
  (100K: 17.70%), which is exactly the §3 calibration reference already run and already
  failing to discriminate a place for full-Aegis inside the ceiling.
- **Coarse, non-binding extrapolation (same ×1.71 50K→100K deterioration factor candidate
  #1's §1 used):** 2.02% × 1.71 ≈ **3.45%**, Run-2 (consistency-on) plausibly a touch
  higher — **above** the 3.0% ceiling on exactly the geometry the discharge rule requires.
  **This candidate is coarsely predicted to fail Part A.** It is registered anyway,
  honestly, for three reasons: (1) the extrapolation is a single blunt multiplier carried
  over from a *different* Aegis-weight prior (candidate #1's own §1 used it for a 2-leg
  book; applying it to a 3-leg book with a structurally different tail — Aegis attribution
  47.8% of bust at 50K — is a coarser transfer than the original use); (2) a real,
  pre-registered FAIL on the frozen surface is itself falsifier-relevant evidence for the
  program (closes the Aegis-inclusive door with a dated result rather than an untested
  guess); (3) the operator directed it. **The G4 run adjudicates, not this paragraph.**
- The ADR's early-fail branch (§4) is scoped to *the first* candidate — already resolved
  by candidate #1's DISCHARGE. A FAIL here, on any pattern, does **not** re-arm any
  extra-authorization requirement for a hypothetical candidate #3; that stays a normal
  per-candidate decision either way, unchanged by this candidate's outcome.

**Claim (ADR §2 claim-separation, restated — identical to candidate #1's):** this candidate
claims **native-book bust-geometry at the frozen firm tiers** — panels as measured on
CME/CBOT micros, TV-modeled costs included. It does **not** claim CFD-edge preservation;
R5/P2 stay FALSIFIED and this artifact must never be cited against them.

**Provenance caveat (elevated from candidate #1's calibration-reference footnote to a
first-class disclosure here):** `ae744`'s exact Pine inputs are unverified from CSV bytes
alone (PANEL_OF_RECORD §2). The operator's 2026-07-15 pick accepted this panel as the
prop-candidate Aegis panel of record; it did not certify the BEPAD-TEST provenance
question. This candidate's own book — not just a diagnostic reference — now rests on that
unresolved provenance. If it clears, the DISCHARGED verdict inherits the same caveat the
regime-gate rider inherits: mechanically real, provenance-caveated.

---

## §2 — The candidate (FIXED — the entire variant set is this one book)

| Item | Fixed value |
|---|---|
| Book | 3 legs: Striker DJ30 v4.5 → **MYM**; Striker NAS100 v1 → **MNQ**; Aegis USDJPY v0.3 → **6J** (panel `ae744`). **No other leg.** |
| Panels (bytes pinned) | `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv` (sha256 `9acfa29726a9530d2a3de5fc2290cc67672441fac2c805defd524677cce01b9e`, N=267) · `Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv` (sha256 `8884e6dd56c786e1e59a8ab0b962a70be82f34e06af26a9582554c9f8ddc6419`, N=284) · `Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-11_ae744.csv` (sha256 `e82a2c25a94c42b12888f2f8b70daa56f579c6fe02a633418edcf4b3d148ca38`, N=152) |
| Panel window | Union of the three exports — **2020-01-06 → 2026-07-01** (1693 bdays; one day past candidate #1's 2-leg window, per the ae744/5274c export tail observed in the bustcut Test 2 construction) |
| Construction | Decompound static @ $200K via roe → `pin_r_basis(full_stop_mean)` → scale to per-leg risk (identical to the futures3/bustcut/candidate-#1 construction — **zero new variants on the method**) |
| 1R pins (expected; §8.3 asserts) | striker **$2,535.61 (n=8)** → scale **0.5521** (unchanged from candidate #1) · striker_nas100 **$5,899.32 (n=19)** → scale **0.1254** (unchanged) · aegis **$2,912.96 (n=11)** → scale **0.5149** (= 0.0075 × 200,000 / 2,912.96; new to this candidate, computed from the PANEL_OF_RECORD-pinned 1R at this candidate's own risk weight) |
| Per-tier weights (venue variables) | striker **0.70%** · striker_nas100 **0.37%** · aegis **0.75%** per trade. `(portfolio, firm-tier)` venue variables in the dd-geometry concept-not-constant sense — the futures/nas weights are numerically equal to the locked CFD values because that is what every prior look measured (unchanged rationale from candidate #1); the aegis weight (0.75%) is **half** the locked CFD value (1.50%), matching the only Aegis-bearing prior inside any ceiling — re-weighting after seeing results would mint a fresh variant (§5). This is not a deployment of the locked four-strategy CFD book. |
| dd_protection overlay | **OFF** (`NO_PROTECTION_TRIGGER`), per gate §7(6). No tuned `(trigger, scale)` grid registered. |
| Engine params | 10,000 sims × seeds **42/123/2026**; horizon **1500**; inactivity disabled; tiers threaded via `preflight.firm_kwargs` (never module constants; `ACTIVE_FIRM` untouched) |
| Runs | Run-1 (consistency-off) + Run-2 (consistency-on) for Tradeify (40%) / MFFU (50%) / BluSky (34%); Bulenox has no eval consistency → its single run gates. **Part A reads Run-2 wherever consistency exists** (identical rule to candidate #1). |
| Tiers | Exactly the four frozen: `Bulenox_100K` · `Tradeify_Select_100K` · `MFFU_Rapid_100K` · `BluSky_Premium_100K`. All other tiers, if printed, are diagnostics only. |

**Deployable vs research expression (envelope §2.1):** expected to coincide, as for
candidate #1 — the striker/nas100 legs are already EOD-flat per-session; the Aegis 6J leg's
own overnight-hold posture must be **confirmed at G1 from the ae744 panel bytes**, not
assumed from the 2-leg candidate's result (this is new information this candidate
introduces, since Aegis was never in candidate #1's book). If Aegis carries overnight
holds, the deployable/research expressions diverge and G1 must say so — this is not
pre-decided here.

**`DEPLOYABLE-DEFAULT-ENVELOPE` criterion (frozen, binary; annotated YES/NO at closure):**
identical rule to candidate #1 — per-leg gross edge per round trip ≥ **4×** the per-firm RT
cost (`2 × cost_per_side_usd`) at the deployable expression's measured round-trip count
`R_deploy` (G1 output, pyramid entries counted as fills).

**Envelope §2 emissions at G1 (computed from panel bytes, declared at closure; describe,
never filter):** `R_deploy` (expected ≈**703** = 267 + 284 + 152 raw entries, pyramid
recount at G1); deployable/research expectancy ratio; consistency annotation; per-trade
excursion stats vs E3 intraday-trail posture; exposure coordinates {side; entry session
windows (ET) — now spanning three sessions, not two; in-market minutes/yr; **pairwise**
structural overlap MYM×MNQ, MYM×6J, MNQ×6J = simultaneous-in-market minutes/yr ×
sign-agreement per pair}.

---

## §3 — Calibration-reference registration (gate §7(9) rider — already satisfied, not re-run)

The frozen gate's one pre-registered non-candidate calibration reference — the 3-leg native
**full-Aegis book at the locked 1.50% risk** (ae744 @ 1.50% + MYM 0.70% + MNQ 0.37%) — **already
ran** in candidate #1's scoring session ([`RESULTS.md`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md) §3 Calibration reference):
**0/4 tiers clear 3.0%** (Tradeify Run-2 17.88%, matching the prior remc 17.70%/17.88% band).
The AMBIGUOUS gate-level clause did **not** fire; the ceiling discriminates as designed.

**This candidate does not re-register or re-run that reference.** It is cited here to
satisfy the same audit-hook lineage candidate #1's §3 established, and because it is the
adjacent data point this candidate's own result should be read against: candidate #2 tests
whether **halving** the Aegis weight (0.75% vs the calibration reference's 1.50%) is enough
to bring the 3-leg book's bust rate under the ceiling where the full-weight version could
not (17.70–17.88% vs a coarse ≈3.45% prediction here). If this candidate also fails, the
finding is that no Aegis weight this program has examined — half or full — fits inside
3.0% on this panel family; if it clears, halving Aegis weight is the load-bearing lever.

---

## §4 — Falsifiable hypothesis (H-C2; binary)

**H-C2 — if** the §2 book clears Part A (**bust ≤ 3.0%** by `summarize_outcomes`
daily+static+trailing **and P(pass) ≥ 50%** with finite median ≤ 1500d), Run-2 where
consistency exists, on **≥2 of the four frozen tiers including ≥1 `trailing_locking`**
(Tradeify_Select_100K or MFFU_Rapid_100K), **then** this candidate adds a second,
independent piece of §4-falsifier evidence (the falsifier itself is already discharged by
candidate #1) and routes to G8 (lifecycle CANDIDATE @ 1.00×, carrying the G1 envelope
annotations; own regime-robustness rider owed before that trust, per gate §7(7));
**otherwise** H-C2 is falsified for this candidate and it **closes** (no iteration in
place), disposition per §6 — closing FALSIFIED here does **not** demote the program (the
falsifier stays discharged by candidate #1 regardless) and does **not** re-arm the ADR's
early-fail authorization gate (that clause is scoped to the first candidate only, §0/§1).

**Reject/accept thresholds (restated numerically):** accept iff, on ≥2 frozen tiers with ≥1
`trailing_locking`, Run-2 headline bust ≤ 3.0% AND P(pass) ≥ 50% AND median ≤ 1500d; reject
on any other pattern of per-tier results.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Re-weighting Aegis down further (e.g. 0.50%) after a marginal or failing Run-2 result**
  — the temptation the coarse ≈3.45% prediction invites directly. The §2 weight (0.75%) is
  fixed because it is the only measured prior inside any ceiling; tuning it post-result is
  gate-layer tuning the ADR forbids. A failed candidate closes; a lower-weight variant is a
  fresh candidate with its own pre-registration.
- **Dropping the Aegis leg mid-scoring if it's the tier-killer** — that collapses this
  candidate back into candidate #1 (already scored, already DISCHARGED); it would not be a
  new result, just a relabeled duplicate.
- **Treating a FAIL here as evidence the program should demote** — it should not. The
  four-firms ADR §4 falsifier is satisfied by candidate #1 independent of this candidate's
  outcome (§0/§1/§4). Citing this candidate's FAIL against the program's standing is a
  category error this pre-reg exists partly to forestall.
- **Citing MYM/MNQ/6J absolute PF against P2 edge-transfer** — same standing prohibition as
  candidate #1; R5/P2 stay FALSIFIED regardless of this candidate's result.
- **Counting a Bulenox+BluSky-only pair as discharge** — F2 optimistic-lower-bound
  geometry; the ≥1 `trailing_locking` clause is frozen, unchanged from candidate #1.
- **Reading `compute_default_config()['bust_rate']` for any tier** (F1) — headline bust
  comes from `preflight.summarize_outcomes` only.
- **Running any frozen-tier G4 cell before the §9 signature lands** — identical prohibition
  to candidate #1; the prior 50K/2b looks are visible and the temptation to "just peek at
  one tier" is real.
- **Treating the operator's ae744 pick (PANEL_OF_RECORD, 2026-07-15) as having resolved the
  BEPAD-TEST provenance question** — it resolved *which panel to use*, not *what the panel
  actually is*. Citing this candidate's result (either direction) as settling the
  provenance caveat would overstate what was decided.

---

## §6 — Gate criteria (binary dispositions)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** (H-C2 holds) | Part A on ≥2 frozen tiers incl. ≥1 `trailing_locking` | Second independent falsifier-evidence point (falsifier already discharged by candidate #1); candidate → G8 admission (lifecycle CANDIDATE @ 1.00×); rail/account/go-live still gated; own regime-robustness rider owed before trusting into G8, same as candidate #1 |
| **FALSIFIED — partial (NOT-cleared)** | Clears Part A on ≥1 tier but the discharge-pattern is unmet (e.g. a trailing-only pair, or exactly one tier) | Candidate closes; per-tier evidence recorded; program falsifier status unaffected (already discharged) |
| **FALSIFIED — all-four-fail** | Fails Part A on **all four** frozen tiers | Candidate closes; **does not** re-arm the ADR §4 early-fail authorization clause (that clause is scoped to the first candidate only, already resolved by candidate #1's discharge) — a hypothetical candidate #3 remains a normal per-candidate operator decision |
| **AMBIGUOUS (gate-level)** | N/A for this candidate — the §3 calibration reference already ran during candidate #1's session and did not trigger AMBIGUOUS (0/4 clear, ceiling discriminates); this candidate does not re-run it and cannot itself re-trigger this clause | — |

Regime-robustness rider (gate §7(7)): **only owed if this candidate clears** (RESOLVED
row). If so, run the regime gate (6mo block bootstrap + half-panel split per
`docs/methodology/regime_robustness_gate.md`) on this book's own scaled panel before the
DISCHARGED-equivalent verdict is trusted into G8 — candidate #1's rider (`REGIME_GATE.md`)
is a template, not a substitute; this candidate's 3-leg panel is a different book and needs
its own run.

---

## §7 — Prior-look disclosure (complete; the ADR's condition for this artifact)

All looks on this panel family / book-composition layer, in date order. The frozen
$100K×4 cross-section has now been run for **one** S-book (candidate #1, S2); of the four
frozen cells for **this** candidate (S1), all four remain unseen.

| # | Date | Run (path) | Book / form | Numbers seen |
|---|---|---|---|---|
| 1 | 07-10 | selectflex %-equity arm (`lab/archive/tradeify_selectflex_remc_2026-07-10/`) | 3-strat, CFD-host DJ30+NAS + 6J prototype, %-equity | Tradeify geom 25K 7.57% / 50K 7.40% / 100K 13.37% / 150K 13.29% (p99 4.86/4.89/4.51/4.52) |
| 2 | 07-10 | selectflex integer arm, $0-cost bound (same archive) | 2-strat MYM+MNQ, C5 integer sizing, CFD-host panels | 25K 0.06% / 50K 0.09% / 100K 0.80% / 150K 0.92% |
| 3 | 07-10 | selectflex integer arm, $2.22/ctr RT proxy (same) | same | 25K 1.05% / 50K 1.11% / 100K 4.59% / 150K 5.02% |
| 4 | 07-10 | selectflex integer arm @ verified $1.82 — operator-stopped, never completed | same | UNRESOLVED: 100K bracket 0.80% ↔ 4.59% |
| 5 | 07-11 | futures3 remc (`lab/analysis/c1/tradeify_futures3_remc_2026-07-11/`) | 3-leg native (ae744 @ **1.50%** + MYM + MNQ) | Tradeify geom 25K 10.58% / 50K 10.33% / **100K 17.70%** / 150K 17.61%; +40% consistency 10.83/10.56/**17.88**/17.79 — **this is the §3 calibration reference, already run** |
| 6 | 07-11 | bustcut Test 1 (`lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/`) | 2-leg native, %-equity (= **candidate #1**) | 50K geom: bust 0.76%, pass 99.24%, p99 3.86%, med 222d |
| 7 | 07-11 | bustcut Test 2 | 3-leg, 5274c @ 0.75% (spurious 1R median-fallback, scale ~9×) | 50K 39.43% (artifact; 5274c since disqualified; **not** this candidate's prior) |
| 8 | 07-11 | bustcut **2b** | 3-leg, **ae744 @ 0.75%** (= **this candidate's direct prior**) | **50K 2.02%, p99 4.10%, med 152d, Aegis attr 47.8%** |
| 9 | 07-11 | bustcut 2c | 3-leg, 5274c @ 0.75% size-adj (1R $1,869) | 50K 1.28% (artifact-panel; not this candidate's prior) |
| 10 | 07-15 | **candidate #1 G0–G8, real (not extrapolated) result** | 2-leg native, %-equity, frozen $100K×4 | `RESOLVED (DISCHARGED)`: Tradeify 2.65% / MFFU 2.64% PASS; Bulenox 3.51% / BluSky 4.44% FAIL. §3 calibration reference (3-leg full-Aegis 1.50%): 0/4 clear (Tradeify 17.88%) |
| 11 | 07-15 | candidate #1 regime-robustness rider, `HALF_ONLY` | 2-leg native (candidate #1's own book) | H1 (2020-23) bust 4.36-4.37% FAILS 3.0%; H2 (2023-26) bust ~1.70% PASSES; bootstrap still owed. Context only — different book. |

**Freeze-order transparency (carried forward from candidate #1):** the 3.0% ceiling was
frozen 2026-07-13, after rows 1-9 were visible. Candidate #2's composition (row 8's direct
descendant) was itself disclosed as a *known* prior at candidate #1's own freeze time — this
is not new selection-on-results, it is the pre-committed second axis being exercised.

**K accounting:** composition-layer variants examined to date ≈ **10** (rows above; row 7
counted once with its correction row 9; row 10 is candidate #1's real run, not a new
variant; row 11 is a rider on an existing variant). This candidate adds **zero** new
variants on the panel-construction method — it is row 8's book re-run on the unseen frozen
surface, exactly as candidate #1 was row 6's. Class S remains routed out-of-screen-scope
(four-firms ADR / Q-KBUDGET-1 inventory §6.2): no DSR/Clause-K claim is made or needed; the
gate of record has no DSR clause.

---

## §8 — Run protocol (G0–G8 mapping)

1. **G0 intake:** this artifact + §9 signature.
2. **G1 (E1 reduction + envelope emissions):** confirm EOD-flat per-session for **all three**
   legs from panel bytes (striker/nas100 expected 0% overnight holds per candidate #1;
   **Aegis 6J overnight-hold posture is new information, confirm not assume**); emit
   `R_deploy`, expectancy ratio, consistency/excursion/exposure annotations (§2). Emit
   `DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO` per the frozen §2 criterion at closure.
3. **G2 (cost-law kill gate) + 1R guard:** per-leg gross-edge ≥ 4× RT cost at `R_deploy`
   (per-firm `cost_per_side_usd`). **Binding adapter guard (PANEL_OF_RECORD §3, adopted,
   identical to candidate #1):** the scoring adapter hard-fails if `pin_r_basis` returns a
   FALLBACK method or n<5 full-stops for **any** of the three legs — expected striker n=8 /
   nas n=19 / aegis n=11; a violation means the panel bytes changed and the run STOPS
   (`NEEDS_CONTEXT`), it does not proceed on a different 1R basis.
4. **G3:** `preflight.assert_engine_ready` GREEN on all four tiers before any sim.
5. **G4:** the §2 engine params, four frozen tiers, Run-1 + Run-2. No §3 re-run (already on
   record — see §3 above).
6. **G5:** Part A read per tier via `summarize_outcomes` (Run-2 where consistency exists);
   §6 verdict assigned mechanically.
7. **G6:** candidate #2 scores STANDALONE against the gate (candidate #1 already routed
   STANDALONE too — no portfolio-of-two combination is claimed by either candidate
   individually; a future combined-book question, if ever asked, is its own candidate).
8. **G7 (diagnostics, never §4-gating):** funded-geometry ruin read; integer-micro
   granularity + verified-cost sensitivity note; **new for this candidate:** per-pair
   structural-overlap read (MYM×MNQ, MYM×6J, MNQ×6J) as a diagnostic, not a gate input.
9. **G8 (only from RESOLVED):** lifecycle CANDIDATE @ 1.00× intake with annotations + own
   regime-gate rider caveat (owed before trust, §6).

Results land in `lab/analysis/` under a dated slug; the RESULTS header must cite this
pre-registration **and** the frozen gate pre-registration by path (gate §10 hook 6).

---

## §9 — Operator signature (the ADR §4-adjacent per-candidate decision)

```
SIGNED / FROZEN: 2026-07-15 / JA
Authorized as Class-S candidate #2 under ADR 2026-07-14 (Accepted 2026-07-15).
Composition: 3-leg MYM+MNQ+6J (Aegis @ 0.75%, panel ae744) — §2 fixed as drafted.
No frozen-tier G4 cell may run before this block is filled.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature-before-run: confirm §9 is signed (not the placeholder), and that no G4
#    results exist yet if this hook is run before the scoring session.
grep -n "SIGNED / FROZEN: " docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md \
  | grep -v "<date>" || echo "VIOLATION or NOT-YET-SIGNED: signature block not in signed form"

# 2. Variant-set immutability: the fixed weights/seeds/1R pins never edited post-freeze.
grep -n "0.70%\*\* · striker_nas100 \*\*0.37%\*\* · aegis \*\*0.75%\|42/123/2026\|2,535.61\|5,899.32\|2,912.96" \
  docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md

# 3. Panel bytes unchanged since registration (all three, incl. Aegis).
grep -n "15d8b\|beabf\|ae744" core/data/tv_exports/cme/SHA256SUMS   # expect the three pinned hashes

# 4. The Aegis-inclusive declaration is explicit (mirrors candidate #1's no-Aegis obligation).
grep -n "DOES contain an Aegis leg" docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md

# 5. Falsifier-already-discharged framing is present (prevents mis-reading a FAIL as a program demotion).
grep -n "already discharged" docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md

# 6. The scoring session (once run) cites both pre-registrations (Trap #10 guard).
grep -rn "2026-07-15-existing-strategy-book-candidate-2-prereg\|2026-07-13-prop-survivor-scoring-prereg" docs/SESSIONS.md \
  || echo "no scoring session yet (expected while DRAFT)"

# 7. R5/P2 never cited-against (claim-separation honesty).
grep -n "FALSIFIED" docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md | head -3

# 8. §3 calibration reference is cited, not re-run (no duplicate G4 cell for the 1.50% book).
grep -n "does not re-register or re-run" docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md
```

---

## Verification

```bash
# Discipline checks (mechanical)
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md --type inquire

# §0 anchors
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md            # be6dda6
git log -1 --format='%h %ci' -- docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md                 # 507761a
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md  # 58fff1d
git log -1 --format='%h %ci' -- lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md                       # eba5030
git log -1 --format='%h %ci' -- lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md                       # 507761a
git log -1 --format='%h %ci' -- core/firm_rules.py                                                                 # a53ee99

# Panel bytes (all three)
grep -c "15d8b\|beabf\|ae744" core/data/tv_exports/cme/SHA256SUMS    # expect 3

# Engine pre-flight importable (G3 dependency)
python -c "import sys; sys.path.insert(0,'core'); from mc.preflight import summarize_outcomes, firm_kwargs; print('preflight OK')"

# Expected scale factors reproduce (sanity, not a run)
python -c "print(round(0.0075*200000/2912.96,4))"   # expect 0.5149
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-15 | Drafted (`DRAFT — awaiting operator signature`); composition S1 (3-leg, Aegis @ 0.75%, panel ae744) fixed per §1 record, reusing candidate #1's pre-committed axis inventory | Joshua (direction) + Claude Code (Sonnet 5) |
| 2026-07-15 | **Signed / FROZEN** (§9) — operator ratified the S1 recommendation as-drafted, no redraft requested. No item above changed at signature. | Joshua (JA) |
