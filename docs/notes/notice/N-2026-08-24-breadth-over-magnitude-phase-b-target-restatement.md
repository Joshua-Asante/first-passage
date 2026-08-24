# NOTICE 2026-08-24 — Breadth over magnitude: what Phase B should be sourcing *for*

**Notice ID:** N-2026-08-24-breadth-over-magnitude-phase-b-target-restatement
**Observed:** 2026-08-24
**Author:** Claude Code (Opus 5), operator direction in chat — *"finding 4-6 near independent edges
sounds much more likely than a single edge twice as big… we need to focus more on finding
strategies that have edge and do not trip the drawdown, rather than finding one strategy that
passes the challenge by itself"*, then *"write it up as a note… I will pass it along to the agent
doing the Phase B work currently."*
**Type:** Notice-phase. Derivation + arithmetic over already-committed measurements.
**$0 · K=0 · no camp · no card · no manifest · no Cap seat · nothing armed.** No `core/`,
`firm_rules`, `dd_protection`, Pine, lifecycle, allocation or rail surface touched. No candidate
proposed, admitted, unparked, demoted or retired.
**Status:** `OPEN` — this restates a **target**, which is an operator call. It does not amend
[Phase B](../../superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md), does not
change any lane's kill criteria, and does not authorise anything. Phase B's own
`AUTHORIZATION: AWAITING GO` stands unchanged.

**Read with:**
[`a2_panel_noise_venue_bound_2026-08-24`](../../../lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/RESULTS.md)
(the bound and its validation) ·
[`shape_feasibility_map_2026-08`](../../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md)
(A2, the shape target) ·
[`Q-COMPOSE-1` entry](../../rejected_candidates.md) (the composition kill and its re-proposal bar) ·
[`RESULTS_stage8_neff.md`](../../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage8_neff.md)
(the only measured cross-leg correlation in the estate).

---

## §0 — The one-line restatement

**Phase B is not looking for a strategy that passes the eval. It is looking for the fourth-cheapest
member of a set of four to six mutually-independent strategies that pass it together.**

That is a different sourcing instruction, and it changes three things: the per-candidate edge bar
(down), the per-candidate *realness* bar (unchanged or up), and the selection criterion across
candidates (mechanism-family diversity, which is currently not a criterion at all).

---

## §1 — Why breadth, in the venue's own units

The bound derived in the sibling campaign is `T_min(yr) = (target/rope) · (ln(1/0.03)/2) / annSR²`
— size-invariant, validated 230/232 against A2's own bust-compliant cells. For `k` legs of equal
Sharpe and zero correlation, `annSR → annSR·√k`, so **`T_min ∝ 1/k` exactly.**

At ORB-MNQ-1's 2021+ Tradeify figure (`annSR +1.140` — the best repeatable measurement in the
estate), on `Tradeify_Select_100K`:

| legs | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| portfolio annSR | 1.14 | 1.61 | 1.97 | 2.28 | 2.55 | 2.79 |
| time to pass | 32 mo | 16 mo | 11 mo | **8 mo** | **6.5 mo** | **5.4 mo** |

**The decisive property is not the odds, it is that partial progress pays.** Three legs already buys
a one-year pass. Progress toward one `annSR 2.65` construct is worth **zero** until it arrives, and
would require something with 2.3× the per-trade Sharpe of anything this estate has ever measured —
against a corpus maximum of `+1.28` ([Stage-7](../../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage7.md),
2021+ at 3 ticks of added slip), which is short of even a *one-year* pass on its own.

**The contract cap is not a constraint on this.** Six legs at `$275` risk each is ≈ 11 micros
against an 80-micro account-aggregate cap.

---

## §2 — One correction to the framing, and it changes the screen

The operator phrasing was *"strategies that have edge and do not trip the drawdown."* **Not tripping
the drawdown is free.** That is precisely what size-invariance means: any positive-edge construct can
be sized down until bust ≤ 3%. What it cannot do is be sized down *and still reach the target in
useful time* — sizing trades bust for timeout at constant quality.

Measured instance, from the sibling campaign §4: `pol_cushion` stand-down variants on ORB-MNQ-1 drive
bust to **0.00%** and pass rate to **8–20%**. Perfect rope discipline, no pass.

**Consequence for Phase B:** a screen on drawdown behaviour selects for small-sized constructs that
time out. The screen is **per-trade edge-to-noise**, expressed as annualised Sharpe, which every
campaign in the estate already publishes — including all four TNEC lanes, in their own G0/G2 headline
tables. Drawdown behaviour is downstream of a sizing knob set afterwards, not a candidate property.

---

## §3 — Two things that break `√k`, both already diagnosed in this repo

### §3.1 — A leg that is not real actively subtracts

With `j` genuinely-edged legs out of `k` admitted, portfolio Sharpe is `j·μ/(√k·σ)` — not `√j·(μ/σ)`.
Dead legs contribute variance without drift:

| real / admitted | portfolio annSR | vs. the real legs alone |
|---|---|---|
| 3 of 3 | 1.97 | — |
| 3 of 4 | 1.71 | 13% worse |
| 3 of 5 | 1.53 | **23% worse** |
| 3 of 6 | 1.40 | 29% worse |

Three real legs plus two spurious ones is **worse than the three alone**. So this is emphatically
**not** "lower the bar and admit more." It is: lower the **edge-magnitude** bar, hold or raise the
**realness** bar (CI excluding zero, DSR-at-K, the placebo and era-orthogonality batteries).

That split is already estate precedent — the
[2026-08-08 necessity retarget](../../adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md)
§2-B re-typed **EM1** from a `≥0.40R` intake-kill to *"net expectancy > 0 after Requirement-5 costs
with a pre-registered 95% CI excluding 0, plus DSR ≥ floor_at_k"*. That was exactly this move, made
once, for one gate. §1's arithmetic is the general justification for it.

### §3.2 — Correlation, and specifically correlation in the regime that kills you

For `k` equal-Sharpe legs at equal pairwise correlation `ρ`:
`annSR_portfolio = annSR · √k / √(1 + (k−1)ρ)`.

| legs | ρ = 0 | ρ = 0.15 | ρ = 0.30 | ρ = 0.50 |
|---|---|---|---|---|
| 4 | 8.1 mo | 11.7 mo | 15.4 mo | 20.2 mo |
| 6 | 5.4 mo | 9.4 mo | 13.5 mo | 18.9 mo |

**Moderate correlation is survivable** — even at `ρ = 0.15`, six legs turns 32 months into 9. It is
`ρ ≳ 0.30` that guts the strategy.

Two cautions on assuming `ρ ≈ 0.15`:

1. **It is one measured pair, between two different mechanism families.** Stage-8's `+0.1506` is
   `corr(ORB-MNQ, Striker-MNQ)` over 339 overlapping weeks — an opening-range breakout against a
   pyramided trend construct. Five further opening-range breakouts on MNQ in the same RTH session
   would not sit at 0.15. Nothing in the estate measures that case.
2. **Average correlation is the wrong statistic.** Stage-8 also found ORB's concentration was
   *regime-common-mode* — dead 2020, dead in the chop the book busts in. Legs that are near-independent
   in normal conditions and all go dead in the same regime deliver far less than `√k` precisely when
   it is needed.

**`Q-COMPOSE-1`'s re-proposal bar already states the exact failure mode**, in the estate's own
vocabulary: a breadth leg whose **risk N_eff (PR-cov)**, not merely its **dependence N_eff (PR-corr)**,
also rises under composition. ORB cleared the correlation limb (dependence N_eff 1.9948 → **2.9502**)
and failed the variance limb (risk N_eff 1.9593 → **1.9628**, flat) because it carried ~2× the weekly
dollar volatility of each book leg — it dominated rather than diversified. Any leg admitted under the
restated target must be checked on **both** limbs, and sized to **equal risk contribution**, not equal
nominal risk.

---

## §4 — The restated target, in a form a lane can screen against

A Phase B candidate is admissible toward this target if it can show, on its own measured evidence:

| # | Property | Bar | Where it is already measured |
|---|---|---|---|
| N1 | **Edge-to-noise** | net-of-cost `annSR ≳ 1.0` on the candidate's own cost basis | every TNEC G0/G2 headline table already reports `annSR`; ORB Stage-6/7 reports it per firm |
| N2 | **Realness** | CI excluding 0, DSR ≥ `floor_at_k(K_intrinsic)`, placebo + era-orthogonality — **unchanged, and load-bearing** (§3.1) | EM0 / harvest Req 1–5, untouched by this notice |
| N3 | **Family diversity** | a *different* mechanism family from every already-admitted leg — not a different instrument or parameterisation of the same one | **no current gate tests this** — see §5 |
| N4 | **Composition** | risk N_eff (PR-cov) rises, not just dependence N_eff (PR-corr); sized to equal risk contribution | `Q-COMPOSE-1` re-proposal bar; `research_utils.breadth.participation_ratio` |

**N1 is a lowering** of the effective magnitude bar relative to "find something that passes alone"
(`annSR ≈ 2.65`). **N2 is not lowered.** **N3 and N4 are additions**, and they are the ones with no
current owner.

### Screening the live lanes against N1, for free

Every construct in the estate that publishes an `annSR`, against the six-month Select requirement of
**2.65** (source table: sibling campaign §3):

| construct | annSR | `T_min` on Select_100K |
|---|---:|---:|
| ORB-MNQ-1, 2021+ best cell — **corpus maximum** | 1.280 | 2.1 y |
| ORB-MNQ-1, 2021+ @ Tradeify cost | 1.140 | 2.7 y |
| ORB-MNQ-1, full window @ Tradeify cost | 0.835 | 5.0 y |
| `Q-TNEC-CON-3` HTF native break, long — **best live lane** | 0.405 | 21.4 y |
| `Q-TNEC-CON-4` PDH/PDL break, short | 0.085 | 485 y |
| ICT raid→FVG chain at its frozen DOL target | ~0 | never |
| `Q-TNEC-CON-4` PDH/PDL break, long | −0.128 | never |
| `Q-TNEC-CON-2` compression break, long | −0.404 | never |
| `Q-TNEC-CON-5` impulse/pullback/VWAP, long | −0.532 | never |

**No live TNEC lane is within an order of magnitude of N1.** The screen is a single division on a
number each lane already reports at G0, so it costs nothing and it fires at intake rather than at
Phase C.

---

## §5 — The part that is genuinely new work, and the honest risk

**N3 has no owner.** Nothing in the current pipeline scores a candidate on *family distance from the
already-admitted set*. Phase B's live lanes are B1 (MOC-imbalance wake, MES) and B2 (London-fix wake,
FX futures) — which, notably, **are** two different families, so the current lane set is well shaped
for this target even though it was not chosen for it.

**The honest risk in the restated target:** it is a supply-*diversity* requirement, not a supply-
*volume* one, and diversity is the harder axis. Sourcing five more opening-range-breakout variants
would be comparatively easy and would fail §3.2 — the estate's own registry already carries the
K-bank and Cap-seat machinery that makes near-duplicate candidates expensive, which pushes the right
way here. But the deep-lane supply audit (2026-08-23, `AMBIGUOUS`) found the estate's named free
supply routes number **two**, not six. **Reaching four to six independent families is not obviously
cheaper than the unicorn hunt; it is only more *incremental*.** That trade — lower variance of
outcome, partial progress that counts, against a harder diversity constraint — is the operator's
call, and this notice does not make it.

---

## §6 — What this notice does and does not do

**Does:** restate the target Phase B sources against, in the venue's own units; supply a $0 intake
screen (N1) that every lane can run on a number it already publishes; name two `√k`-breaking failure
modes with the estate's existing measurements behind each; flag N3 as unowned.

**Does not:** amend Phase B, its lanes, or any kill criterion. Authorise a card, a camp, a manifest,
a Cap seat or any spend. Move `EM0`–`EM5`, harvest `Req 1–5`, or `TNEC-1`. Propose unparking
ORB-MNQ-1 (its re-park ADR's R2/R3 remain the only routes; R2 was checked and does not fire —
sibling campaign §7). Claim any of the four TNEC lanes should close: **N1 is a screen against *this*
target, not a verdict on those lanes' own frozen gates.**

**Forbidden moves under this notice:**

- Reading §4's N1 as a licence to relax **N2**. §3.1 is the reason: admitted-but-spurious legs make
  the book strictly worse, so the realness bar carries *more* weight under breadth, not less.
- Treating `ρ = 0.15` as the estate's cross-leg correlation. It is one pair, across two families
  (§3.2), and it is a mean, not a regime-conditional statistic.
- Sizing admitted legs to equal *nominal* risk. `Q-COMPOSE-1` died on exactly this — equal risk
  *contribution* is the N4 requirement.
- Quoting `T_min ∝ 1/k` as a forecast of calendar time to a funded account. It is a floor on the
  eval, conditional on bust ≤ 3%, under the sibling campaign's own §8 limitations (diffusion
  approximation, needs a rope many R deep, i.i.d. trades).

---

## §7 — Routing

| Item | Owner | Action |
|---|---|---|
| Whether the target is restated at all | **Operator** | this notice is the input; no default |
| N1 as a $0 intake screen on B1.4 / B2.3 | [Phase B](../../superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md) card-precheck rows | adopt or decline — it is one division on a published number |
| N3 (family-diversity gate) — **unowned** | needs an owner | no gate currently tests it |
| N4 composition check | `Q-COMPOSE-1` re-proposal bar, already written | reuse verbatim; do not re-derive |
| The bound, its validation and limitations | [sibling campaign](../../../lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/RESULTS.md) | §2 (derivation), §3 (corpus scorecard), §8 (limitations) |

**Durable obligation created:** none. Per this directory's README, a notice is not a second board —
if the operator restates the target, the obligation belongs on `STATE.md` or an owning ADR, not here.

---

## Verification

```bash
# The leg-count and correlation arithmetic (sections 1, 3.1, 3.2)
python lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/venue_bound.py
# Expected: the corpus scorecard and the breadth block at the end

# The measured cross-leg correlation is a single pair
grep -n "Dependence N_eff\|Risk N_eff" lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage8_neff.md
# Expected: 1.9948 -> 2.9502 (corr) and 1.9593 -> 1.9628 (cov)

# Q-COMPOSE-1's re-proposal bar already names the N4 requirement
grep -n "risk N_eff (PR-cov)" docs/rejected_candidates.md
# Expected: the "breadth-leg candidate ... whose risk N_eff (PR-cov)" re-proposal line

# EM1's retarget is the precedent for the N1-down / N2-held split
# (the source bolds the token, so match around the markup, not through it)
grep -n "re-types from" docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md
# Expected: the EM1 line, ">=0.40R net intake-kill" -> "net expectancy > 0 ... CI excluding 0"

# The live TNEC lanes publish annSR in their own headline tables
grep -h "^| Long \|^| Short " lab/analysis/c1/mnq_tnec_con*/RESULTS*.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | Initial authoring, at operator direction, for handoff to the in-flight Phase B worker | Claude Code |
