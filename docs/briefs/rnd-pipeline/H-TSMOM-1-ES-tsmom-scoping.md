# Campaign scoping — H-TSMOM-1 ES Moskowitz–Ooi–Pedersen 12m/1m TSMOM confirm

**Status:** `CLOSED — Clause-N FAIL 2026-07-16 (P1 pinned to reading (c), Default-#1-compliant)`. Operator pinned §0.5 P1 to the **strict ratified-default reading**: statistical OOS = 2019-05-06→present, **N≈86, power=0.34 — below the 0.50 threshold (break-even N≈138)**. The addendum's ratified N=192 (readings a/b, power 0.638/0.598) does not survive strict application of the Campaign-defaults ADR's temporal-not-instrument OOS axis absent a stated §8 override, which was not granted. **Campaign does not proceed to Stage-0 pre-registration, `register_search open`, or any pull.** No K consumed; ES family bank stays at **2** (H-OD-1 only — H-TSMOM-1 never opened). **Net effect on the harvest's 3-axis fundable-PASS set (D5 / H-OD-1 / H-TSMOM-1): zero survivors** — D5 and H-OD-1 both closed Stage-2 cost-law KILLs; H-TSMOM-1 now closes as a scoping-stage Clause-N FAIL under the pinned default. This is a **different failure class** from the other two (screen-stage, before any pull or K-bind — not a Stage-6-confirm closure) and does **not** itself feed the harvest-intake §4 doctrine falsifier count, which requires Stage-6-confirm closures; flagged as a follow-up question in §4, not resolved here. **Synced 2026-07-16 (same session)** to the [inventory addendum](../Q-KBUDGET-HARVEST-1-inventory-addendum.md) §4 (post-ratification correction, original PASS cells left intact), `STATE.md` (three stale "3 PASS.../still fundable" passages corrected), and [`docs/SESSIONS.md`](../../SESSIONS.md) (new top entry).
**Axis:** harvest **H2** — `H-TSMOM-1` Moskowitz–Ooi–Pedersen 12-month/1-month time-series-momentum confirm, S&P 500 cohort → ES expression
**Lane:** mechanism-first, Path **1b** evidence-robustness (HARV ADR `Accepted` — HARD gate)
**Parents:** [`Q-KBUDGET-HARVEST-1`](../Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md) (`CLOSED-RESOLVED` 2026-07-16) · [inventory addendum](../Q-KBUDGET-HARVEST-1-inventory-addendum.md) row H2 · [`PHASE2_RATIFICATION.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE2_RATIFICATION.md) (Path-1b four-bar score) · [`PHASE3_RESULTS.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE3_RESULTS.md) · [`H_TSMOM_1_fig2_scrape.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/H_TSMOM_1_fig2_scrape.md) · Moskowitz, Ooi & Pedersen, *Time Series Momentum*, **JFE 104 (2012) 228–250**
**Inheritance:** Campaign-defaults ADR 2026-07-11 + DSR-K supersession 2026-07-12 + HARV lane ratification 2026-07-13 + harvest-intake ADR 2026-07-15 + **same-units/per-gate/panel-basis attestation ADR 2026-07-16 (`Accepted`)** — this campaign is the first to scope *after* that ADR's acceptance, so its §2.1–§2.3 specification is a Stage-0 requirement here, not a retrofit.
**Sibling precedent:** [`H-OD-1-ES-overnight-drift-scoping.md`](H-OD-1-ES-overnight-drift-scoping.md) (this doc follows its shape; H-OD-1 closed 2026-07-16, Stage-2 cost-law KILL under a gate-geometry defect the same-units ADR now corrects — H-TSMOM-1 was the ES family's expected next campaign, but closes here at the screen stage instead, before ever reaching Stage-2)

---

## §0 — Grounding (Rule-0 anchors, read 2026-07-16, HEAD `61422ff`)

**Provenance note:** the instruction to author this brief named a source handoff, `docs/briefs/handoffs/2026-07-16-cc-spawn-h-tsmom-1-scoping.md`. That path does not exist in this worktree, in `origin/main` (fetched fresh this session), or anywhere in `git log --all`. Per `handoff-verify` Phase-0, this is a hard-fail on "named paths exist" — this brief is therefore grounded directly in the on-disk ratification chain below, not in the missing packet. Flagged for operator confirmation; nothing below depends on the missing file's contents.

| Source | Anchor | Supplies |
|---|---|---|
| [Inventory addendum](../Q-KBUDGET-HARVEST-1-inventory-addendum.md) §1 row H2 | RATIFIED 2026-07-16 (operator "accept both") | Family **ES → K_banked** (see below, now 2 post-H-OD-1); design K_intrinsic **(1, 1)** — single fixed hypothesis, no bundled optional clause; declared **N = 192** monthly events, "post-pub OOS ≈2010–2025"; **δ/σ = 0.167**; Path **1b** |
| [`PHASE2_RATIFICATION.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE2_RATIFICATION.md) | Path-1b four-bar score, all four **PASS** (2026-07-16) | Admission basis: (i) ≥3-decades class-level, (ii) ≥3 non-overlapping equity-index cohorts in Fig. 2, (iii) class-discovery replication pin (Hurst/AQR 2017), (iv) no structural sign-reversal (long-horizon reversal is a *different*, non-overlapping prediction). **Caveat carried forward, not resolved:** if discovery were pinned strictly to Moskowitz's own 2012 coining, no peer-reviewed ≥2022 replication was located this session — the ACCEPT rests on the class-discovery pin. |
| [`PHASE3_RESULTS.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE3_RESULTS.md) | harvest §6 RESOLVED 2026-07-16 | H2 screen **PASS** — Clause K floor 0.85 (K_eff=2 *at ratification time*); Clause N power **0.638** at declared N=192 |
| [`H_TSMOM_1_fig2_scrape.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/H_TSMOM_1_fig2_scrape.md) | δ-extraction, digitized 2026-07-16 | S&P 500 gross annualized Sharpe **0.58** (Fig. 2, ±0.03 digitization tolerance) → δ/σ_monthly = 0.58/√12 = **0.167**. Cohort is **S&P 500 futures only — no NQ/Nasdaq contract in Moskowitz's nine-equity-index universe**; the paper's own **N-sensitivity table is reproduced below** — it is the direct numeric ancestor of §0.5 P1. |
| [`floor_scan.py`](../../../lab/archive/q_kbudget_1_2026-07/floor_scan.py) `floor_at_k` (frozen method) | reproduced this session | `floor_at_k(1)=0.65 · (2)=0.85 · (3)=0.98 · (4)=1.06` (>Cap 1.0). ES family bank is now **2** (H-OD-1 closed 2026-07-16, K=1 banked) ⇒ H-TSMOM-1's own K_intrinsic=1 gives **K_eff = 3, floor = 0.98** — tighter than the 0.85 floor the Phase-3 table shows, because that table ran *before* the H-OD-1 closure incremented the ES bank. **Screen re-run at the current K_eff has not happened in this brief — Stage-0 must re-run it, not inherit the stale 0.85 figure.** |
| [Campaign-defaults ADR 2026-07-11](../../adr/2026-07-11-discovery-campaign-defaults-ratified.md) §2 item 1 ("Default #1") | `Accepted`, operator-ratified standing policy | **Temporal-not-instrument OOS axis:** discovery + all tuning on **2010-01-01→2018-12-31** (parent); **2019-05-06→present** is the statistical OOS; native-micro re-run on that era is a realism gate, not an independence gate. Overriding any ratified default is legal only with a stated reason in the campaign's own §8 (ADR §2 "Inheritance semantics"); **silent override or in-place edit is forbidden (ADR §5)**. |
| [`strategy_harvest.md`](../../methodology/strategy_harvest.md) §1 Requirement 4 + Requirement 5, §2.1 | canonical procedure (owner ADR `Accepted` 2026-07-15) | Requirement 4's practical bar names **monthly-event mechanisms at bp-scale effects as presumptively dead** (D3/D7 kill precedent) — **H-TSMOM-1 is explicitly not that class**: §2.1 names it the **Tier-A "fund-first" reference case** (low-frequency, large-per-event-δ) precisely because its δ (0.167 monthly) is an order of magnitude above the bp-scale month-end mechanisms that died on Clause N alone. Requirement 5 (cost-law reachability, `Accepted` 2026-07-16) is now binding at admission — see §2 below. |
| [`ops/instruments/ES.md`](../../../ops/instruments/ES.md) E4, W1, W2 | instrument ledger, last updated 2026-07-12 | MES cost hurdle **1.71bp single-RT** at the 4373 reference price (4× = 6.84bp; two-RT deployable form 4× = 13.68bp) — re-derive at prevailing price for the actual attestation. **W1** (`.c.0` calendar-roll phantom jumps, +135bp-class at quarterly rolls) and **W2** (UTC-day bucketing / phantom Sunday bars) bind any long-horizon continuous-series construction this campaign's 15-year monthly panel will need. |
| [Same-units attestation ADR 2026-07-16](../../adr/2026-07-16-harv-attestation-same-units-supersession.md) | `Accepted` 2026-07-16 (same day as this brief) | §2.1–§2.3: §R must simulate **every** gate in **that gate's own units**; mandatory cost-law inequality `cohort δ (bp/event) ≥ 4 × RT_frac(panel-era median price, commissions included)`; every reachability quantity computed at the basis the gate actually scores on. Both prior mechanism-first campaigns (D5, H-OD-1) died on exactly the failure this ADR now forecloses — H-TSMOM-1's Stage-0 §R must not repeat it. |

**Honesty riders (ratified campaign-layer, not scoping kills):**
1. **Gross-of-cost:** Fig. 2 is gross Sharpe (same caveat class as D5/H-OD-1). Monthly holding amortizes round-trip cost over ~21 sessions rather than one — qualitatively favorable vs. D5/H-OD-1's per-session cost bleed — but Requirement 5's inequality must be shown explicitly at Stage-0, never waived on this qualitative argument alone.
2. **Monthly event rate is the axis's structural weak point for Clause N**, not its cost profile — see §0.5 P1. A haircut to SR≈0.45 (δ/σ=0.144) already fails Clause N at N=192 (addendum §1 honesty rider); the N-sensitivity table below shows the same fragility from the *denominator* side even at the undiscounted δ/σ=0.167.
3. **No non-circular ES-native replication located this session** for requirement-1b bar (iii) — the ACCEPT rests on the class-discovery pin (Hurst/AQR 2017), not a Moskowitz-specific post-2022 replication. Carried forward, not re-litigated here.

---

## §0.5 — Open operator pins (decide before Stage-0 freeze)

### P1 — Panel / N: which OOS-event count does this campaign actually confirm on? **(the load-bearing fork — DECIDED, see below)**

The ratified inventory addendum declared **N = 192** ("monthly events, post-pub OOS ≈2010–2025") and that is the N the Phase-3 screen scored PASS against (power 0.638). But **192 does not derive from the ratified Campaign-defaults ADR's Default #1 temporal split** — it appears to span the *entire* available ES panel (≈16 years, 2010–2026), including the 2010–2018 window Default #1 reserves for **discovery/tuning**, not statistical OOS. Three internally-consistent readings exist, and they do not agree:

| Reading | OOS window | N (months) | Power at δ/σ=0.167 | Screen |
|---|---|---|---|---|
| **(a) As ratified** — full ES panel, "post-original-sample" (2010→2025) | 2010-01→2025-12 | 192 | **0.638** | PASS (current addendum figure) |
| **(b) Strict post-publication** — paper published 2012 | 2012-01→2026-07 | ≈175 | 0.598 | PASS |
| **(c) Default-#1-compliant** — statistical OOS starts at the ratified split date | 2019-05-06→2026-07 | ≈86 | **0.34** | **FAIL** |

(Reproduced this session: `Φ(√N·0.167 − 1.96)`; break-even N ≈ 138 for power = 0.50.)

**Why this is a genuine fork, not a formality:** every other screened-PASS axis on the harvest slate (D5, H-OD-1) is a daily-or-intraday footprint where Default #1's 2019-05-06 OOS start still leaves thousands of events — the temporal reservation costs power but doesn't flip the verdict. H-TSMOM-1 is the first monthly-frequency confirm to reach scoping, and at monthly frequency the reservation **is** the difference between PASS and FAIL. Two defensible arguments cut opposite ways:

- **For strict Default-#1 compliance (reading c):** the ADR's inheritance semantics are unconditional — "an in-place edit of a ratified default is forbidden," and no campaign has yet been granted a stated exception. Applying it uniformly is the whole point of ratifying defaults once instead of re-arguing per campaign.
- **Against (favoring readings a/b):** Default #1's IS/discovery reservation exists to prevent *in-sample tuning contamination* — but H-TSMOM-1's construct (12m lookback / 1m holding, vol-scaled sign) is frozen from the external paper and involves **zero in-house parameter search on ES data**; there is nothing tuned on the 2010–2018 window to contaminate. Whether a no-tuning confirm should inherit an anti-tuning reservation is exactly the kind of question the ADR's §8-override clause anticipates, not one this brief can resolve by reading the ADR text alone.

**Consequence, now realized:** reading (c) is the only one that applies the ratified default without a stated exception. Absent an explicit, reasoned §8 override to (a) or (b) — which the operator did not grant — the honest disposition is reading (c), and it **fails Clause N**. That is what §0.5's decision below records: the campaign freezes as a Clause-N **FAIL**, not as the "PASS, fundable at K_eff=3" status the addendum had carried forward.

> **P1 DECIDED 2026-07-16 (operator): (c) — Default-#1-compliant.** Statistical OOS = 2019-05-06→present, N≈86, power=0.34. **Clause N FAILS at this N** (threshold power ≥0.50; break-even N≈138). Readings (a)/(b) — the addendum's ratified N=192 and the strict-post-publication N≈175 — do **not** apply: the operator did not grant a stated §8 override of the ratified temporal-not-instrument OOS axis, so the default applies as ratified, without exception. **P2/P3 are moot** — the campaign does not proceed to a construct/pull-expression freeze under this pin. Frozen here, not in a Stage-0 pre-registration (none will be authored for this disposition).

### P2 — Pull expression (default-unless-objection) — **moot under the P1=(c) pin; retained for the record**

Default (H-OD-1 precedent): **ES parent for the discovery/IS-adjacent window, MES for the OOS realism leg**, `.v.0` continuous volume-roll per the ES.md W1 roll-rule finding (never `.c.0` calendar-roll — the +135bp-class phantom-jump risk is structural, not incidental, for a 15-year monthly series that must survive dozens of quarterly rolls). **Corollary of P1(c):** MES only launches 2019-05-06 — if P1 resolves to reading (c), the native-micro realism leg and the statistical-OOS window become the *same* ≈86-month span, collapsing what is normally two independent checks (statistical confirm, realism gate) into one thin sample. This is a second, downstream consequence of P1 that Stage-0 must disclose, not a separate fork.

### P3 — Construct freeze: vol-scaling method (default-unless-objection, cite at freeze) — **moot under the P1=(c) pin; retained for the record**

Moskowitz's construct positions to constant **ex-ante volatility** (paper §4 / Fig. 2 caption), not a raw sign bet. Default: replicate the paper's own estimator (exponentially-weighted lagged daily-return vol, scaled to a fixed annualized target) rather than inventing a substitute — Stage-0 §5 must cite the specific estimator and target vol level verbatim from the paper, not approximate it. No independent vol-scaling design decision is licensed here.

P2/P3 were defaults-unless-objection while P1 was open; with P1 pinned to (c), both are moot — the campaign never reaches a construct/pull-expression freeze.

---

## §1 — Pre-committed hypotheses (draft; retained for the record — formulas do not freeze under the P1=(c) pin)

**Moot under §0.5's P1=(c) disposition** — the campaign closes at the screen stage, before any hypothesis formula freezes. Retained below as the documentary record of what this axis's confirm would have tested, in case a future re-open (new N-extending evidence, not a re-argued default) revisits it. Names only — exact lookback/holding windows, vol-scaling estimator, and cost model would freeze at Stage 0:

1. **H1 (primary, sole hypothesis — K_intrinsic = 1):** ES vol-scaled position sized to the sign of trailing 12-month total return, held 1 month, monthly rebalance (Moskowitz–Ooi–Pedersen TSMOM mechanism-class confirm; Path 1b — no named loser-side mechanism required, evidence-robustness substitutes). The lookback/holding pair is the **cohort's own declared construct**, not a sweep axis — unlike H-OD-1, there is no optional bundled second clause (addendum design is **(1, 1)**, not (1, 2)).
2. **H2 — none.** Path 1b's admission was scored on the single frozen construct; adding a conditional variant now would be a K expansion requiring a fresh screen, not a Stage-0 refinement.
3. **H3 (placebo falsification clause — consumes no selection-K):** a construct with **no overlap with the 12m/1m conditioning window** — e.g. a disjoint, non-overlapping lookback/holding pair the paper's own evidence gives no reason to expect signal from — sized so a plausible-true world can still pass. Exact placebo construct is Stage-0 work; the Q-HARV-0 scar (a placebo nested inside the conditioning window is structurally un-passable) applies here exactly as it did for H-OD-1.

If P1 resolves such that the bundled clause set cannot carry a reachability attestation, **drop or redesign before freeze** rather than shipping an unreachable campaign (D5/H-OD-1 precedent, now doctrine per the same-units ADR).

---

## §2 — HARD gates before any pull (mandatory order) — **moot: campaign closed at screen stage, none of these execute**

Retained for the record only. Under the P1=(c) pin, the campaign never reaches item 1 — there is no Stage-0 pre-registration to author, no attestation to write, no `register_search open` to bind. The steps below describe what *would* have been required had P1 resolved to reading (a) or (b):

1. **Author full campaign brief + verdict pre-registration** (template: [`discovery-campaign-template.md`](../../ltm/briefs/rnd-pipeline/discovery-campaign-template.md); target path `docs/briefs/pre-registration/H-TSMOM-1-ES-tsmom-preregistration.md`). **Cannot freeze responsibly until P1 is pinned** — the declared N is a §5/§8 input, not a downstream detail.
2. **Reachability attestation for every bundled clause** under a plausible-true world (HARV §2.4 HARD gate), written per the **same-units/per-gate/panel-basis specification** (ADR 2026-07-16, `Accepted`, binding on this campaign from the start — not a retrofit):
   - §2.1 — simulate **every** gate this campaign can die at (Stage-2 cost-law if applicable, Stage-6 confirm, placebo, temporal battery) in **that gate's own units**.
   - §2.2 — exhibit the mandatory cost-law inequality `cohort δ (bp/event) ≥ 4 × RT_frac(panel-era median price, commissions included)`. **Directional expectation only, not a substitute for the computation:** monthly holding amortizes round-trip cost over ~21 sessions, unlike D5/H-OD-1's per-session bleed, so this inequality is expected to clear comfortably — but Requirement 5 requires it shown explicitly, at the frozen vol-scaling target's implied position size, never waived as "obviously fine."
   - §2.3 — compute every reachability quantity at the basis the gate actually scores on (the OOS panel P1 resolves to — not a present-day or convenience price level).
   - **Clause-N reachability is itself part of this attestation now** — given the P1 fork, the attestation must show the confirm gate (Stage 6) is reachable **at the N the pre-reg actually freezes**, not at the most favorable of the three readings in §0.5.
3. **`register_search open --lane mechanism-first --reachability-attestation <path>`** — binds K **onto the shared ES family bank** (currently 2; this campaign's K_intrinsic=1 brings it to 3, floor 0.98 — reproduce, do not inherit the stale Phase-3 0.85 figure).
4. **Cost estimate → pull** only after (3); inherit P2/P3 pins; `--max-cost` gate on every pull regardless of $0.00 expectation.
5. **Campaign HARD quality bar:** **net-of-cost** Sharpe vs Clause-K floor **0.98** (K_eff = 3, current bank) at the bound K_eff. Gross numbers never touch the verdict. Confirm this floor is still current at freeze time — a third ES-family closure between this brief and Stage-0 would move it again.

---

## §3 — Forbidden moves

- **Citing this axis as a fundable PASS (K_eff=3, floor 0.98) without disclosing the P1=(c) pin and its Clause-N FAIL** — the Phase-3 screen's PASS was computed at N=192 (reading a), which this brief's operator-pinned disposition has superseded. Any downstream reference (08-08 packet, STATE.md, future harvest sourcing) that quotes the old PASS without the correction repeats exactly the error this pin exists to prevent.
- Re-opening this axis on a re-argued default (disputing P1 again without new N-extending evidence) — a legitimate re-open requires new evidence (e.g., a genuinely different construct or data source that changes the OOS event count), not re-litigating the same three readings
- Pulling data before `register_search open` + attestation
- **NQ/MNQ or MYM expression of this axis** — Moskowitz's nine-equity-index universe has **no Nasdaq contract**; a native NQ δ/σ extraction (not attempted this session) would be a *new axis*, screened separately, same posture as the H-OD-1 MNQ prohibition
- Sweeping the 12m/1m lookback/holding pair, or the vol-scaling estimator/target — these are the cohort's declared construct, not tunables; any variant is a new axis
- Freezing a declared N without pinning P1 first, or quoting the Phase-3 power=0.638 figure without disclosing which of the three §0.5 readings it corresponds to
- Nesting the placebo inside the 12m/1m conditioning window (Q-HARV-0 structural scar)
- Quoting gross Sharpe against the floor, or waiving the cost-law inequality (§2.2) as "obviously fine" without showing the division
- Expanding K after looking (screen PASS voids if bound K exceeds the declared band); re-screening at a stale K_eff (0.85 instead of the current 0.98) rather than re-deriving it at freeze
- Treating screen PASS as survivor-scoring clearance — survivors still go to the frozen prop G4 gate
- Wide mining / STUMPY tiling on ES (Clause-K FAIL class; forecloses the family)

---

## §4 — Next actions

| # | Action | Owner | Status |
|---|---|---|---|
| 1 | Decide P1 (panel/N vs Default #1 — the load-bearing fork) | Operator | **DONE 2026-07-16 — pinned (c)**: strict Default-#1-compliant OOS (2019-05-06→present), N≈86, power=0.34, **Clause N FAILS** |
| 2 | Re-derive current K_eff/floor at the ES family's live bank | CC | **MOOT** — no K binds under this disposition; ES family bank stays at 2 |
| 3 | Freeze Stage-0 pre-reg | CC | **DOES NOT PROCEED** — campaign closes at screen stage |
| 4 | Review §R attestation → GO/NO-GO | Operator | **MOOT** |
| 5 | `register_search open` + cost-gated estimate/pull | Operator + Cursor/CC | **MOOT** |
| 6 | Survivors → frozen prop G4 gate | Lab | **MOOT** |
| 7 | Sync this disposition to [inventory addendum](../Q-KBUDGET-HARVEST-1-inventory-addendum.md) (§4 correction, row H2 cells left intact), `STATE.md` forward board, and `docs/SESSIONS.md` | CC | **DONE 2026-07-16** — same session |

**08-08 packet:** H-TSMOM-1 appears as **CLOSED — Clause-N FAIL under the pinned Default-#1-compliant OOS axis (P1=(c), 2026-07-16)**. Combined with D5 and H-OD-1's Stage-2 cost-law kills, **Q-KBUDGET-HARVEST-1's entire ratified 3-axis fundable set now has zero survivors**. This does not itself fire the harvest-intake §4 doctrine falsifier (that clause is scoped to Stage-6-confirm closures, not scoping-stage screen reversals) — the packet should name this distinction explicitly rather than let "zero survivors" read as "doctrine falsified."

---

## §5 — Audit hooks (runnable)

```bash
# Upstream screen state this brief SUPERSEDES for H-TSMOM-1 (still shows 3 PASS incl.
# H-TSMOM-1 at the Phase-3-era N=192/K_eff — that figure predates this brief's P1 pin
# and is not re-derived here; §4 item 7 is the open follow-up to correct it in place)
python lab/archive/q_kbudget_1_2026-07/floor_scan.py | tail -3

# floor_at_k reproduction — current ES bank is 2 (post H-OD-1 closure) ⇒ this campaign's own
# K_intrinsic=1 brings K_eff to 3, floor 0.98 (NOT the addendum's 0.85, which pre-dates the
# H-OD-1 closure)
python -c "import sys; sys.path.insert(0,'lab'); sys.path.insert(0,'lab/archive/q_kbudget_1_2026-07'); \
from floor_scan import floor_at_k; print([ (k, floor_at_k(k)) for k in (2,3,4) ])"
# expect: [(2, 0.85), (3, 0.98), (4, 1.06)]

# P1 fork numbers reproduce from the frozen Clause-N formula (delta/sigma=0.167 from the Fig.2 scrape).
# P1 is PINNED to (c): N=86 is the live disposition-driving row, not a hypothetical.
python -c "
from math import erf, sqrt
Phi = lambda z: 0.5*(1+erf(z/sqrt(2)))
d = 0.167
for N in (192, 175, 86):
    z = (N**0.5)*d - 1.96
    print(N, round(z,3), round(Phi(z),3))
"
# expect: 192 -> ~0.638 (reading a, superseded) · 175 -> ~0.598 (reading b, superseded)
#         86 -> ~0.34 FAIL (reading c, PINNED — this is the campaign's actual disposition)

# Disposition sync check (§4 item 7, DONE) — "still fundable" should no longer appear at
# all; remaining "3 PASS" hits are historical Phase-3 mentions, each immediately followed
# by its post-ratification correction in the same file
grep -n "3 PASS\|still fundable" docs/briefs/Q-KBUDGET-HARVEST-1-inventory-addendum.md STATE.md 2>/dev/null | head -5

# Ratification + Fig.2-scrape anchors exist
grep -n 'H-TSMOM-1' docs/briefs/Q-KBUDGET-HARVEST-1-inventory-addendum.md | head -5
grep -n 'S&P 500' lab/analysis/harvest/q_kbudget_harvest_1_2026-07/H_TSMOM_1_fig2_scrape.md | head -5

# Campaign-defaults ADR Default #1 text (the P1 conflict source)
grep -n '2019-05-06' docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md

# Same-units attestation ADR is Accepted (binding on this campaign's §2 from the start)
grep -n "Status:" docs/adr/2026-07-16-harv-attestation-same-units-supersession.md
# expect: Accepted

# No manifest opened yet — confirms this brief has not crossed into register_search open
ls discovery_manifests/ | grep -i tsmom || echo "confirmed: no H-TSMOM-1 manifest yet (expected pre-freeze)"

# The handoff this brief was asked to execute genuinely does not exist (provenance disclosure)
git log --all --oneline --diff-filter=A -- "docs/briefs/handoffs/*tsmom*"
# expect: empty
```
