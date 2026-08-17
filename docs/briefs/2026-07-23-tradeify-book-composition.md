# BRIEF — Tradeify Book Composition & Prop-Leg Economics (08-08 Gate Input)

**Type:** Inquire-style gate-input brief (feeds the 2026-08-08 quarterly gate)
**Authored:** 2026-07-23, from the four-panel gap-analysis session
**Amended:** 2026-07-23 (posture reconcile + compose-objective split vs Q-COMPOSE-1 / Q-FUNNEL-1);
2026-07-23 later same day (operator: ORB PARKED; bust-gate re-derive + c1 1.00× aim → 08-08 packet)
**Status:** `MEASUREMENT RECORD ONLY` — dispositions §6 are not live gate work; ORB operationally PARKED (operator)
**Harness:** [`lab/analysis/c1/tradeify_book_composition_2026-07-23/`](../../lab/analysis/c1/tradeify_book_composition_2026-07-23/)
**Packet home:** [`2026-07-17-0808-packet-delta-and-sequence.md`](2026-07-17-0808-packet-delta-and-sequence.md) (§0.5 operator posture 2026-07-23)

---

> ⚠ **MEASUREMENT RECORD ONLY (2026-08-06 / claim-alignment M34).** One block for four findings:
> **(1)** §6 **D1 is MOOT** — no deployed book to HOLD, no account to SHIP to, neither branch
> takeable (operator 2026-07-23 note had already defaulted it to HOLD).
> **(2)** §4 **H1 is UNREACHABLE** — needs a B7 arming, an eval pass and 12 funded months;
> record it **stranded, not falsified**.
> **(3)** §10's "6 months live data after B7" re-MC trigger is stranded with H1.
> **(4)** the "not Tue, where the incumbents leave 0" cap clause is dead.
> **Re-arm:** an F3 venue with a deployed book.
>
> **Preserved:** §1/§2 funded-economics measurements (carried into ADR §1); D2's PARKED verdict
> (composed bust geometry). **Do not "correct" the $339 chain rate** — superseded in place to
> $318 then **$299.80** by dated addenda.
>
> §5 item 5 is the forbidden move **FU-1 deliberately crossed** (`551d5c5`); §5 itself is **not**
> edited — meet the override at the FU-1 ruling, not by rewriting this brief.


## §0 — Rule-0 reads (before authoring)

Production data read and verified before any conclusion below:

| Artifact | Anchor | Step-0 |
|---|---|---|
| `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-23_626e8.csv` | n=263, Net $35,121.70, 2020-08-04→2026-07-21 | clean |
| `Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-07-23_0ebc6.csv` | n=262, Net $92,704.38, 2020-08-11→2026-07-21 | clean |
| `Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-23_6aa5d.csv` | n=143, Net $28,562.85, 2020-07-27→2026-07-15 | clean |
| `ORB_MNQ_v0.2_CME_MINI_MNQ1!_2026-07-23_ad732.csv` | n=1,542, Net $23,555.76 (Bulenox-costed), 2020-07-20→2026-07-22 | clean |

Pipeline: `.claude/skills/trade-csv-reconcile/scripts/reconcile.py` (canonical loader,
exits-only P&L, full-stop-mean R-pinning, bf32aa3 fallback) +
`strategy-validation/scripts/step0_battery.py`, run 2026-07-23. Panels and simulation
scripts live under the harness path above (`out/daily_panel.csv`, `out/book_panels.csv`,
`gap_stage1..4.py`).

**Live-ops posture (repo, 2026-07-23 reconcile @ `main`):**
[`STATE.md`](../../STATE.md) · [`docs/notes/rail_build/RUNBOOK.md`](../notes/rail_build/RUNBOOK.md) ·
GO ADR [`docs/adr/2026-07-17-c1-rail-build-account-registration-go.md`](../adr/2026-07-17-c1-rail-build-account-registration-go.md)
— Tradeify Select **100K Evaluation** registered; B6 dry-fire **PASSED 2026-07-20**; rail
**disarmed** (`dry_run=true`); **B7 / first armed session is a separate operator GO** (not taken).
Nothing is live-trading; “2-leg live” below means the **authorized c1 book once armed**, not
current fill state.

**Closed compose / funnel doctrine (must not be elided):**
- [`Q-COMPOSE-1-closure-falsified.md`](closures/Q-COMPOSE-1-closure-falsified.md) (2026-07-17) —
  2-leg + ORB@0.37% bust **2.65% → 38.75%** on Tradeify Select 100K under the survivor-scoring
  floor; disposition = deploy **c1 alone @ WATCH-1 0.50×**, no compose.
- [`Q-FUNNEL-1-closure-resolved.md`](closures/Q-FUNNEL-1-closure-resolved.md) (2026-07-22) —
  funnel-EV vs bust≤3% / WATCH-1 tension; **operator 2026-07-23** routes this to a **fresh
  bust-gate re-derivation** (packet A0 / Trap #12), not an open “weigh both forever” question.
  Naming collision with this brief’s composition D1 — see §6.

Rule pins (Tradeify Select 100K), read 2026-07-23 from help.tradeify.co:
- Eval: target $6,000; EOD trailing DD $3,000; 40% consistency (eval only); min 3 trading days; full 8/80 contract limits; one-time purchase, no time limit.
- Funded Flex: payout every 5 winning days; ≤ min($4,000, 50% of total profit); 90/10; no minimum balance; floor locks at $100,100 on EOD ≥ $103,100 **or first payout**; subsequent payouts require balance > prior request balance; funded contract scaling starts reduced, full 8/80 unlocks at EOD ≥ $103,000.
- FTA: max 5 funded accounts per person/household; ~~**no mixing mini and micro contract types**~~ — **RESCINDED, verified 2026-07-29** (see §0.6); ≥1 trade/week activity.
- ~~⚠ Pinned from secondary sources, **verify in dashboard before relying**~~ — **VERIFIED 2026-07-29** ([help-centre article](https://help.tradeify.co/en/articles/12853966-select-flex-and-select-daily-payout-policies); record: [`2026-07-24-tradeify-rulepin-verification.md`](../notes/2026-07-24-tradeify-rulepin-verification.md)). **1 of 3 matched.** $200 winning-day minimum (100K) **CONFIRMED**. Funded start tier is **3 mini / 30 micro**, not 4/40, and scales in **four** steps (30→40 @ $101,500 → 50 @ $102,000 → 80 @ $103,000) — the harness models a binary 40→80 step, so this needs a harness change, not a flag. Flex has **no minimum payout** at all (the $1,000 was a modelling assumption; $250 belongs to Select *Daily*). Both mismatches fall outside the sensitivity grid that was run.

Baselines file `.claude/skills/trade-csv-reconcile/references/baselines.md` is CFD-era
(last synced **2026-06-04**, CSV vintage 2026-05-24) — **no futures-venue lock anchors exist**;
all four panels above are provisionally accepted, unreconciled against Pine headers.

## §0.5 — Ambiguities surfaced

1. ORB **v0.2** (this export) vs repo pin `orb_mnq_v0_1.pine` / PORT_MANIFEST — version delta
   undocumented in-repo (plausibly the 2026-07-21 OCA same-bar-reversal fix; confirm and record
   before any ORB number is treated as of-record).
2. Aegis 6J export n=143 vs parked-lane anchor n=129/PF 2.318 — config or span variant; which is the panel of record for the parked lane?
3. Winning-day minimum, funded start tier, Flex min payout — see ⚠ above.
4. ~~Whether Tradeify's contract-type mixing clause ("mini and micro") also bars **standard** 6J alongside micros — read literally it does; confirm with support before any 6J thought resurfaces.~~ **RESOLVED 2026-07-29 — the question is moot: the clause itself no longer exists.** No support contact was needed. See §0.6.
5. **Compose-objective split (load-bearing; do not collapse):** this brief measures
   **chain-rate compose** — renewal-reward `$/acct-mo` under Select eval→Flex payout mechanics
   (extraction / cadence / churn). That is a **different objective** from **bust-floor compose**
   already closed by **Q-COMPOSE-1** (`FALSIFIED` 2026-07-17: survivor-scoring bust≤3% ∧
   P(pass)≥50% under trailing_locking; ORB@0.37% devastated the barrier via variance dominance).
   **Q-FUNNEL-1** (`RESOLVED` 2026-07-22) already parks funnel-EV vs the bust≤3% / WATCH-1 floor
   as an 08-08 operator tension. A high chain-rate for 2-leg+ORB does **not** reopen or
   supersede Q-COMPOSE-1; shipping a 3-leg book under bust-floor doctrine requires a **fresh**
   ADR/pre-reg that explicitly chooses chain-rate (accept-churn) over the survivor-scoring floor
   — not a silent D1 flip inside this brief.

## §0.6 — Mixing clause RESCINDED (verified 2026-07-29); M6J still not a Tradeify product

**The §0 FTA pin was wrong as carried, and the §0.5(4) ambiguity is moot.** Read directly
in-browser at [`Rules: Hedging & Correlated Products`](https://help.tradeify.co/en/articles/10495868-rules-hedging-correlated-products)
(help.tradeify.co, "Updated over a week ago"; `WebFetch` 403s this host — browser read, as with
the 07-29 pin pass). Tradeify **previously** prohibited holding mini and micro contracts
simultaneously; that standalone restriction **no longer applies**, having been removed once
broker-side contract fungibility closed the contract-limit gap it existed to prevent.

**Two residuals survive the rescission — the clause was narrowed, not deleted wholesale:**
1. The combined position must stay inside the account contract limit, counted at **10 micros =
   1 mini**. (So a full-size 6J consumes **10** of the 80 micro-equivalents.)
2. A mini and a micro in **opposing** directions on the same or correlated product is still a
   hedging violation — on hedging grounds, not contract-size grounds.

**Corroborating (not verbatim-authoritative — retrieved via a summarizing fetcher):** FTA §6.7(d)
(last modified May 2026) permits positions in full-size, mini and micro contracts held together
provided none oppose. Note this means the two published sources were **already in tension when the
pin was taken on 07-23** — this is not purely post-hoc rule drift, and the pin was never flagged ⚠
because it sat in the unflagged FTA line. *Unflagged ≠ verified.*

> **⚠ Precedence corrected 2026-07-31.** The parenthetical above originally read *"and the FTA wins
> over the help centre on conflict"*. Under FTA **§11** the **help centre** prevails on product
> classifications and groupings, so the help-centre source was governing here. The mixing finding is
> unchanged (both sources agree); only the precedence qualifier was wrong. Canonical:
> [`TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md`](../notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md) §Precedence.

**Product Groups (same source):** Currencies = `6E, M6E, 6B, 6J, 6A, M6A, 6C, 6S` — a **different
group** from Equity Index (`…YM, MYM, …NQ, MNQ…`). A 6J leg therefore has **no hedging
interaction with c1 in either direction**, not merely same-direction safety.

**M6J is still not tradable at Tradeify.** [`Rules: Supported Trading Products / Assets`](https://help.tradeify.co/en/articles/10468222-rules-supported-trading-products-assets)
(dated **May 20, 2026**): the micro-currency products are **M6A and M6E only**; `6J` appears under
Currency Futures at **full size**. The article warns explicitly against assuming a micro version
of a standard contract exists. This **independently reproduces** the repo's existing pin — the
ratified envelope ADR [`2026-07-13-prop-envelope-v1-ratification.md`](../adr/2026-07-13-prop-envelope-v1-ratification.md)
§5 already recorded "**no M6J**" for Tradeify. Two sources, same answer, 16 days apart.

**No re-MC triggered.** §10's trigger is "any change to the ⚠ rule pins"; this was not one of the
three ⚠ pins, and no cap / floor / payout / consistency quantity in the MC depends on it. The
clause is a **legality constraint on configuration**, not a model parameter.

**No §6.1 event on the ratified third-leg spec.** S2 ("expressible in micro contracts") is sourced
to envelope **E5**, whose stated grounding is micro *sizing granularity*, firm scaling plans, and
databento Rule-4 proxy discipline — the mixing clause is **not** cited. S2 survives untouched, and
the rescission opens **no new candidate space**: the screen's binding constraint is the ≈**$125**
per-contract daily-$ std ceiling, and a mini / full-size contract is ~10× a micro per contract,
i.e. strictly **worse** against that ceiling. The door opened onto a wall.

## §1 — Context and standing doctrine

Program: four-firm futures-prop program
([`docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md`](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md)).
**Account state (corrected):** one **Tradeify Select 100K Evaluation** is registered on the c1
rail (Striker NAS / MNQ + Striker DJ30 / MYM). **Last ratified deployable rung = WATCH-1 0.50×**;
**operator aim (2026-07-23) = both c1 legs at 1.00×**, gated on a successor bust ceiling
(packet A0) + admitting ADR — not a silent flip. B6 dry-fire **PASSED 2026-07-20**; rail
**disarmed** (`dry_run=true`); **B7 remains a separate GO**. Spend ceiling **$700**; JULY promo
**already applied** on this challenge. **ORB-MNQ is PARKED** (operator 2026-07-23) — lifecycle
CANDIDATE standing unchanged; no compose / rail / decay work on the 08-08 must-decide path.
The 2026-08-08 gate still carries decompound HOLD + accept-beta; Q-FUNNEL evidence feeds A0.

Operator plan-level frame (2026-07-23, **not repo doctrine**): prop-as-accelerator toward a
self-funded savings path — note self-funded scale is **CLOSED/parked** in-repo
([`docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](../adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md));
do not cite this brief to reopen that lane. Doctrine in force: locked strategies,
dd_protection philosophy, no off-spec discretion (CFD-venue retirement is the anchor), sizing
owned by the account-multiplier layer, ORB lifecycle **CANDIDATE** (pre-reg 2026-07-16),
**Q-COMPOSE-1** disposition = c1 alone @ WATCH-1 (no ORB compose under bust-floor).

**Symptom (Pre-Q form):** the plan's prop leg was budgeted off an assumed 2.5%/month with
monthly-cadence payouts; the measured book's shape (frequency, concentration, extraction
mechanics) had never been passed through the venue's actual rules.

## §2 — Findings (measured, not assumed)

Method: canonical parse → business-day EOD panel (exit-date attribution; all holds
intraday) → Mon-anchored week-block bootstrap, 10K paths × 3 seeds → full Select
eval+funded lifecycle sim (trailing/lock/consistency/winning-day/payout/tier mechanics) →
renewal-reward chain rate = pass% × E[cash|funded] / E[cycle]. ORB re-costed to Tradeify
$0.91/side. "k" = ORB contracts (1R ≈ $160·k; k=6 ≈ $1,000/trade illustration only).

Labels “2-leg live” / “executable” below = **authorized book geometry**, not current armed state.

> **⚠ The eval columns of this table are SUPERSEDED** (2026-07-28). They were produced by an
> `eval_sim` that applied the Funded-only floor lock during the evaluation. Corrected values are in
> [§Addendum 2026-07-28b](#addendum-2026-07-28b--eval-lock-fixed-2-re-derived-h1-retargeted-to-318acct-mo):
> 2-leg **38% / 5.8 mo**, chain **$318** (not 63% / 8.2 mo / $339). Funded-only columns
> (`dead-1y`) are unaffected. Rows kept unedited as the historical record.

| Book | Mean/mo (median) | Win-days/mo | Eval pass / median | Funded dead-1y | Chain $/acct-mo |
|---|---|---|---|---|---|
| 2-leg (c1 geometry) | $1,751 ($0) | 1.00 | 63% / 8.2 mo | 43% | **$339** |
| +ORB@1 (chain-rate scen.) | ~$2.06K | ~2.3 | 59% / 6.2 mo | 69% | **$556** |
| +ORB@6 (chain-rate scen.) | $3,611 ($2,082) | 8.9 | 27% / 1.2 mo | 93% | **$941** |
| +ORB@6 +Aegis (counterfactual, no caps) | $4,002 ($2,430) | 9.0 | 29% / 1.2 mo | 90% | $1,233 |

ORB sizing frontier (2-leg + ORB@k, Tradeify caps): chain rises monotonically
$556→$626→$735→$824→$941 for k=1→6 **while** eval pass falls 59→27% and funded 1-yr
mortality rises 69→93%. Eval fees ≈ $30/mo drag at k=1, ≈ $100–120/mo at k=6 (one-time
purchases; ~3.7 attempts/pass at k=6).

Key structure: (a) the 2-leg book's binding problem is cadence — 1.0 qualifying winning
day/month → 5-month payout cycles; ORB's daily frequency dissolves it (0.6-month cycles
at k=6) and fixes the activity-rule exposure (27%→0% zero-trade weeks). (b) The venue's
economics reward **churn**: cheap immortal evals + fast extraction + floor-lock make
high-k/high-mortality the chain-rate maximum. (c) ORB is not diversification: corr +0.23
to the equity pair, 206 same-direction MNQ hold overlaps (0 opposite-direction — no
netting conflicts), and it deepens the 08-08 common-mode beta. (d) 104.7% of the 2-leg
net comes from days needing >40 micros — the funded start tier clips the current book's
edge exactly where it lives; ORB@k adds little to stacks (3-leg days>40: 4%).
(e) Aegis-6J adds ~+$200/acct-mo frictionless and ~nothing cap-aware; every deployment
gate it faces still stands.

Leg qualities: ORB v0.2 PF **1.156** / WR 47.2% / maxDD $5,764·(k/1) — thin-edge,
high-frequency, unvalidated. Aegis 6J v0.3: PF 2.375 but WR 35% (BE character inverted
on futures ticks) and **1R cohort n=1** — ⚠ **this row scores the n=143 export flagged unreconciled
at §0.5(2); the ledger panel of record (n=129) has full-stop cohort n=10. See D2 (2026-07-29).**
DJ30-MYM: PF 1.80 / WR 40.3% vs CFD lock
2.755 / 72% — species change in the port; carries $35K of $128K net for equal DD room.

## §3 — Constraints to deploying all four legs live

1. **Aegis-6J has no venue** — **legality limb CORRECTED 2026-07-29 (§0.6); the constraint
   survives on other grounds.** No friendly firm lists micro-JPY (M6J is still not a Tradeify
   product, re-verified 07-29). ~~full-size 6J alongside MNQ/MYM micros violates the FTA mixing
   clause as written~~ — **false as of 07-29: the mixing clause is rescinded**, and 6J sits in
   the Currencies Product Group, so it does not even interact with the Equity Index legs on
   hedging grounds. A full-size 6J would consume **10 of the 80** micro-equivalents (fits the
   free capacity on Mon/Wed/Thu/Fri; **not Tue**, where the incumbents leave 0). What still
   binds: **measured bust geometry — ledger J4 puts breach at ~11–12% at cap-12 (5–8% at 0.5×)
   against a 3.0% admission ceiling** (see D2); screen **S2** (6J is not a micro) and an
   unmeasured **R1**; solo-account fork fails the ≥1-trade/week rule 63% of weeks and yields
   $153/acct-mo; lane PARKED 2026-07-16. ~~Aegis falsified out of every deployment path; v0.3
   statistics immature~~ — **both corrected 2026-07-29 (D2): the ledger says `AMBIGUOUS-PARKED`,
   "not falsified by the evidence", and the panel-of-record full-stop cohort is n=10, not n=1.**
   ~~**Four legs on one Tradeify account is not currently a legal configuration; the
   deployable maximum is the 3-leg all-micro book.**~~ → **Four legs on one Tradeify account is
   now a *legal* configuration; it remains an inadvisable one, and D2's other two unpark
   conditions are unmet.** The all-micro shape of the deployable book is now held up by
   envelope **E5 / screen S2** (sizing granularity) and the per-contract variance ceiling —
   **not** by venue legality.
2. **ORB is lifecycle CANDIDATE**: pre-registered 2026-07-16, Pine authored 07-21, rail
   integration / live spend separately gated, and none of its forward gates have data yet.
   PF 1.156 means chain-rate economics are acutely sensitive to a small live haircut — the
   edge-captured falsifier is the load-bearing check. **Bust-floor compose already FALSIFIED
   (Q-COMPOSE-1).**
3. **Contract caps**: 3-leg stacks peak 126 micros (>80 eval cap on rare days — the
   multiplier layer must enforce clipping); funded 40-micro start tier until +$3K EOD.
4. **Version/anchor hygiene**: no futures-venue baselines exist; ORB v0.2 and Aegis
   n=143 deltas unrecorded. Lock anchors must exist before any leg's live activation.
5. **Churn posture is a strategy decision, not a tuning knob**: the k-frontier's maximum
   sits at 90%+ annual account mortality — within written rules, adversarial to firm
   relations and to standing "trade-the-system" doctrine, throughput-limited by the
   5-account/household cap and by breach clustering the week-block MC understates.
6. **Plan arithmetic**: even the frontier maximum (~$800–940/acct-mo net of fees) × 5
   slots ≈ $4–4.7K/mo — prop remains the accelerator, not the engine; the 2×-NDR
   threshold stays out of reach of this venue's structure at any k.
7. **B7 gate**: no composition decision may be executed as ops until B7 arms (or an
   explicit superseding GO); this brief does not arm the rail.

## §4 — Falsifiable hypotheses (forward)

**H:** If the 2-leg c1 book is armed and run to spec, measured net payout cash over the first
12 funded-months lands in [0.5×, 2×] of the modeled $339/acct-mo (H1); separately, any
ORB compose that raises chain rate ≥50% still does not reopen bust-floor compose without
a superseding ADR (H2 limb vs Q-COMPOSE-1).

- **H1 (book economics once armed):** the 2-leg c1 book, run to spec after B7, produces net
  payout cash within [0.5×, 2×] of the modeled $339/acct-mo over the first 12 funded-months
  of program data. Falsified below; superseded above (re-MC trigger either way).
- **H2 (frequency lever, chain-rate objective only):** adding ORB at any k∈[1,6] that
  passes its own gates **and** is admitted under an explicit chain-rate/accept-churn ADR
  (not under silent reopen of Q-COMPOSE-1) raises measured chain rate by ≥50% vs the 2-leg
  baseline over the same window. If ORB passes its gates and the measured lift is <50%, the
  cadence diagnosis is wrong — reopen the composition question rather than re-sizing.
- **H3 (ORB edge reality, owned by the existing pre-reg):** live/forward edge-captured
  ratio ≥0.7 of panel expectancy at matched cost model over the pre-registered N. This
  brief adds nothing to that gate; it only consumes its verdict.

## §5 — Forbidden moves (each was genuinely tempting this session)

1. **Sizing the c1 legs up to close the 2.5% gap** — measured flat-to-negative
  (cash/acct-mo $357→$337→$277→$200 across 0.5×→2×); size converts extraction to breach.
2. **Unparking Aegis-6J on tonight's panel arithmetic** — the expression was falsified
  07-16; re-entry requires new mechanism evidence + a venue, neither of which an MC supplies.
3. **Activating ORB into the account off this analysis** — it is one pre-registered
  forward test away from being evidence; this brief must not become the back door.
4. **Treating chain-rate maxima as a bust-floor GO** — Q-COMPOSE-1 already falsified ORB
  compose under survivor-scoring; adopting k=6 churn because chain rate is highest is a
  posture change requiring its own ADR (firm-relations risk, doctrine conflict, clustering
  risk) and an explicit supersede of Q-COMPOSE-1’s disposition.
5. **Manual token trades to satisfy the activity rule** — off-spec discretion; the CFD
  retirement is the anchor for why not. Rail-level answer or accept warnings.
6. **Re-litigating the payout-policy choice from backtest cadence** — Select Flex is the
  modeled funded path for this account once passed; policy choice re-enters only for
  accounts 2–5.
7. **Arming B7 / treating the eval as Flex “live since 07-21” from this brief** — posture
  confabulation; B7 remains a separate GO.

## §6 — Gate criteria (binary, for 08-08)

**Naming:** this brief’s D1 is **book-composition / chain-rate**. It is **not** the same
object as the Q-FUNNEL-1 finding already routed to the 08-08 packet as funnel-EV vs
bust≤3% — keep both on the board; do not merge labels.

- **D1 — Book composition (two limbs; both required to SHIP 3-leg):**
  - **Limb A — chain-rate (this brief):** ORB’s pre-registered gates report RESOLVED-pass
    **and** the multiplier-layer sizing brief for k exists and is locked.
  - **Limb B — bust-floor / doctrine:** either (i) HOLD the Q-COMPOSE-1 disposition
    (c1 alone; no ORB compose), **or** (ii) a **fresh Accepted ADR** explicitly
    supersedes Q-COMPOSE-1 by choosing chain-rate / accept-churn over the survivor-scoring
    floor, with Q-FUNNEL-1’s funnel-EV evidence named as input.
  - **SHIP 3-leg** ⇔ Limb A **and** Limb B(ii). Otherwise **HOLD** the 2-leg c1 book
    unchanged.
  - **Operator 2026-07-23:** ORB **PARKED** ⇒ D1 defaults to **HOLD 2-leg** without waiting
    on Limb A. Unpark is a fresh operator GO, not an 08-08 automatic. c1 rung aim (**1.00×**)
    is owned by the packet’s A0/A0b path, not by this composition D1.
- **D2 — Aegis-6J:** remains PARKED. Unpark requires ALL of: a venue offering micro-JPY
  at a friendly firm (or a written Tradeify exception to the mixing clause), new
  mechanism evidence per the falsification-re-entry rule, and a v0.x panel with
  full-stop cohort n≥5. Any missing ⇒ PARKED stands without further analysis.
  - **2026-07-29 — condition 1 examined and D2 re-affirmed PARKED. The disposition does not
    move.** Condition 1's *purpose* — is the configuration venue-legal? — is now **satisfied**:
    the mixing clause is rescinded (§0.6), so full-size 6J alongside micro MNQ/MYM is permitted.
    But condition 1 **as written** is satisfied by neither of its two named routes: M6J is still
    not a Tradeify product (re-verified), and no *written exception* was granted — the rule was
    repealed generally, which is a third thing. **Whether repeal-of-the-obstacle counts as
    satisfying a condition that asked for micro-JPY-or-an-exception is a §6 interpretation
    change, and belongs to the operator (Trap #12) — I have not converted it.**
    **Conditions 2 and 3 re-checked against the instrument ledger — and this brief was wrong
    about both:**
    - **Condition 3 is SATISFIED.** [`ops/instruments/6J.md`](../../ops/instruments/6J.md) **J1**
      (panel of record, HIGH confidence, P&L-identity-checked 129/129, 0 off-grid fills) records
      1R **$1,385.74 = full-stop mean, n=10** — clearing the n≥5 floor. This brief's §2
      "**1R cohort n=1**" scores the **n=143 export**, which §0.5(2) itself flags as an
      unreconciled config/span variant. Per operational rule 10 the ledger is the instrument
      source of truth, so **n=10 governs**.
    - **Condition 2's premise is overstated.** The ledger PROFILE cell reads
      `venue-transfer: AMBIGUOUS-PARKED` and states the lane is "parked as a scale-path
      decision, **not falsified by the evidence**." "Falsified out of every deployment path" is
      not what the evidence says, so the falsification-re-entry rule is the wrong instrument
      to apply here.

    **PARKED stands anyway — on survival geometry, which is the real blocker and was never the
    one being cited. RE-RUN EXECUTED 2026-07-29 at the registered `Tradeify_Select_100K` tier**
    ([`RESULTS`](../../lab/analysis/aegis/aegis_6j_trail_tradeify_2026-07-29/RESULTS.md); ledger **J4b**;
    reproduction control **12/12 PASS**, both anchors to the cent):
    - **The PROVISIONAL-basis worry is closed, and it was never load-bearing.** Bulenox Option-2
      and Tradeify Select 100K are **numerically identical** on every parameter the sim uses
      ($3,000 trail, floor lock start+$100, 6% target) — Tradeify-geometry-at-cap-12 reproduces
      J4 digit-for-digit (**11.63% breach / 88.37% pass**).
    - **What actually binds is cap + commission, which J4 never varied:** cap **12 → 8** (inferred
      from Tradeify's published `8/80` mini/micro limit pairs) and commission **$1.30 placeholder
      → $3.10/side**. They **nearly cancel**: cap-8 alone cuts breach to **3.88%**, true
      commission returns it to **12.40%** at full size. Commission is a per-contract subtraction
      that does not shrink with a fixed trail, so **de-risking to survive is partially
      self-defeating once real fees are charged**.
    - **Verdict: FAILS the 3.0% Part-A ceiling in every arm — but by ~1.3–1.8×, not ~4×.** Best
      cell anywhere (verified inputs, 0.5×-until-freeze, exhaustive rotation) = **3.88%**;
      its bootstrap rows **5.00–5.31%**; full-size **10.79–14.66%**; adverse cap-12
      **9.30–18.67%**. *(The earlier "~4× over" framing described the full-size arm only and was
      too harsh for the de-risked one — the correct read is a near-miss, not a blowout.)*
    - **New obstacle J4 could not see — the 40% consistency rule** (eval-only, Tradeify-only):
      only **42–47%** of cap-12 passing paths comply at first touch of +$6,000, rising to
      **77–86%** at cap 8. Non-compliance forces continued trading ⇒ more exposure ⇒ more breach
      risk, a coupling the sim reports but does not compound.
    - **Caveats that do not rescue it:** linear cap re-scale rather than a native replay (F2
      precedent ±2%, which does not close a 0.88pp gap); cap 8 **inferred**, with cap 12 run as
      the adverse case and **both failing**; and this is **standalone** — the gate governs the
      *book*, and composition adds variance, so a standalone fail is a fail **a fortiori** (no
      composition run owed).
    - **⚠ SUPERSEDED SAME DAY — the FAIL above is a wrong-configuration artifact** (ledger **J8**;
      [`RESULTS_GAP`](../../lab/analysis/aegis/aegis_6j_trail_tradeify_2026-07-29/RESULTS_GAP.md)).
      J4's arm (b) is **"0.5× until freeze, then FULL size"** — a Bulenox *ramp-up tactic* that
      re-sizes to full once the floor locks at start+$100, and its post-freeze full-size
      drawdowns are what breach. **No c1 leg runs that**; every deployed leg runs a **constant**
      lifecycle multiplier. At the deployed **WATCH-1 0.50×** constant rung: **breach 0.00%
      rotation / 0.67% L13 / 0.77% L26, eval pass 97.46%, consistency-OK 100%, panel net
      $11,851** — clears the 3.0% ceiling by ~4×. Also settled: the **"0.88pp gap" was never
      measured** (rotation 5/129, 95% CI [1.27%, 8.81%] straddles 3.0%), and the **commission
      break-even is ≤$1.30/side**, which **no published full-size 6J card meets** (Tradeify
      $3.10 / MFFU $2.56 / Bulenox $2.36) — venue shopping cannot close a gap, and does not need
      to. **This admits NOTHING:** the ratified gate is **composed** bust on the frozen engine and
      is **unrun** — Q-COMPOSE-1 took the book 2.65% → **38.75%** on a leg whose standalone
      numbers were fine. **D2 stays PARKED**; next step is a pre-registered composed re-MC at
      constant 0.50×, adversarially reviewed.

    **On the ratified third-leg screen — R1 MEASURED 2026-07-29 and it PASSES** (ledger **J7**;
    [`RESULTS_R1`](../../lab/analysis/aegis/aegis_6j_trail_tradeify_2026-07-29/RESULTS_R1.md)). 6J's
    per-contract daily-$ std is **0.138× (all-days) / 0.402× (trade-days) of ORB**, and ORB sits
    at 1.5× the ceiling ⇒ 6J at **0.21× / 0.61× — PASS under both conventions**, with **1.6–4.8
    contracts** fitting the budget ORB needed 0.66 of. **The granularity-lockout expectation is
    refuted:** R1 is a property of realized per-contract daily P&L, not notional — Aegis-6J is
    flat **89%** of sessions and its 1R is **≈$122/contract**. *(No absolute R1 value is claimed:
    the composed-book $273 anchor did not reproduce, diagnosed as TV equity compounding. The
    verdict rests on a relative calibration to the spec's own negative control.)* **Passing is
    weak evidence here** — excess kurtosis **+43.8**, worst day **5.3σ** — so where R1 passes and
    the direct bust measurement fails, **the direct measurement governs** (§2.3 is explicit that
    R1 is a pre-screen).
    **What remains, therefore:** **bust (measured FAIL)** is now the *only measured* blocker;
    **S2** excludes non-micro contracts by text, but its E5 rationale is **weak for 6J** —
    granularity is refuted above and the databento Rule-4 **proxy** discipline is inapplicable to
    a natively-measured 6J panel (moving S2 is a **§6.1 event and an operator call**, recorded not
    acted on); and **cap accounting is unverified** — Tradeify lists currencies in their own
    table, labelled neither mini nor micro. Plus **J5**: the 12-cap already binds on **76%** of
    trades (~0.5–1.0% effective risk vs a locked 1.5% target), so de-risking to fix bust throttles
    an already-throttled edge.

    **Net:** D2 is no longer blocked by a venue rule *or* by thin data. It is blocked by
    **measured drawdown geometry** — a falsifiable, re-testable claim rather than a wall.
- **D3 — Churn-posture question:** admitted to the gate as a named fork
  (accept-churn vs reject-churn) with the frontier table as its evidence base **and**
  Q-COMPOSE-1 / Q-FUNNEL-1 cited; decided by ADR or explicitly deferred with a revisit
  date. Not decidable inside this brief. D3 is the natural home of Limb B(ii).
- **D4 — Plan numbers:** the prop-leg contribution used in any plan math is replaced by
  the measured band $339 (2-leg geometry) / $556–941 (conditional on D1 SHIP, by k) until
  12 months of live payout data supersede the MC (H1). Do not treat these as bust-floor
  pass rates.
- **Verification duty:** the three ⚠ rule pins (§0) verified in-dashboard before any D1
  SHIP path; failure of any pin re-runs the MC with corrected rules before shipping.
  Checklist scaffold: [`docs/notes/2026-07-24-tradeify-rulepin-verification.md`](../notes/2026-07-24-tradeify-rulepin-verification.md).
  **Ops duty:** B7 remains a separate GO — D1 SHIP does not arm the rail.

## §7 — Forked questions (parent-Q convention; each needs its own Pre-Q if opened)

- Q-ORB-SIZE: what k (and whether eval-k ≠ funded-k) does the multiplier layer run,
  given the frontier's survivability/extraction tradeoff? (Phase-dependent sizing is
  legal and unexplored — it is a question, not a recommendation.)
- Q-DJ30-WEIGHT: is the MYM edition of Striker DJ30 carrying its DD budget? (PF 1.80,
  56% pyramid share vs 94% expected — species-change evidence in §2.)
- Q-BASELINES: author futures-venue lock anchors in `references/baselines.md` for all
  live/candidate legs (currently CFD-era only).

## §10 — Audit hooks (runnable)

```
# Reproduce every number in §2 from the lab harness:
python lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage1.py
python lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage4.py
python lab/analysis/c1/tradeify_book_composition_2026-07-23/assert_anchors.py
# Panels: out/daily_panel.csv (2-leg), out/book_panels.csv (p2/p3/p4 + q2/q3/q4)

# Doctrine citations must remain closed/falsified unless a superseding ADR lands:
git log -1 --format='%h' -- docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md
git log -1 --format='%h' -- docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md
rg -n "disarmed|dry_run|B7" STATE.md docs/notes/rail_build/RUNBOOK.md | head -20

# Rule-pin verification (manual, dashboard): winning-day min $200; funded start tier
# 4/40; Flex min payout. Record results in this brief's §0 before any D1 SHIP path.

# Re-MC triggers: 6 months live data after B7; any leg version bump;
# any k change beyond the locked sizing brief; any change to the ⚠ rule pins.
```

## Addendum 2026-07-28 — `eval_sim` applies the FUNDED-only floor lock; §2 eval + chain-rate numbers are optimistic

**Defect.** [`gap_stage2_capbound.py:179-197`](../../lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py)
(`eval_sim`) computes the drawdown floor as

```python
FLOOR_LOCK_BAL, FLOOR_LOCKED, DD = 103_100.0, 100_100.0, 3_000.0   # line 74
floor = np.where(peak >= FLOOR_LOCK_BAL, FLOOR_LOCKED, peak - DD)  # line 197, inside eval_sim
```

i.e. the floor **freezes at $100,100 once EOD peak reaches $103,100 — during the
evaluation**. That is a **Funded Flex** mechanic. This brief's own §1 venue-fact line
states it correctly and scopes it to funded ("Funded Flex: … floor locks at $100,100 on
EOD ≥ $103,100 **or first payout**"); Tradeify article 10495897 is explicit that
**evaluation accounts do not have drawdown locking**. The venue fact was right in the
prose and wrong in the simulator.

**Direction: optimistic, and structurally so.** The lock engages at $103,100 while the
eval target is $106,000, so **every path that passes must cross the lock region**. At the
target, the modeled floor is $100,100 where the true floor is $103,000 — a **$2,900 gap,
≈97% of the entire $3,000 drawdown allowance**, handed back precisely in the final stretch
where a trailing floor is tightest. Same shape and direction as the
[2026-07-22 firm-rules eval-lock defect](../../lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md).

**Not reachable by the pending config fix.** These are **hard-coded literals**, not reads
of `FIRM_RULES[...]["dd_lock_offset_usd"]`. Applying the still-unapplied `firm_rules`
correction would leave this harness defective. `funded_sim` is **correct** — funded
accounts do lock — so the defect is phase-scoped, not global.

**Contaminated (all §2, all optimistic by an unmeasured amount):** eval pass **63%**,
median **8.2 mo**, chain rate **$339/acct-mo**, and the entire ORB@k frontier (59% / 6.2 mo
/ $556 through 27% / 1.2 mo / $941), since chain rate = pass% × E[cash|funded] / E[cycle]
and both an overstated pass% and an understated cycle inflate it. §2(b)'s characterization
that "the venue's economics reward churn — cheap immortal evals + fast extraction +
**floor-lock**" names the lock as a driver: true for the funded phase, **not** for eval.

**Not contaminated:** the §1 venue-fact table; `funded_sim` mechanics; the cap/quantization
findings that do not route through `eval_sim`.

**Inherited by Q-CAPALLOC-1.** [`run_capalloc.py:179`](../../lab/archive/c1_capalloc_2026-07-27/run_capalloc.py)
calls `G.eval_sim` directly, so its `AMBIGUOUS (d)` closure and the `48/32` dominating-split
finding carry the same defect. **Its owed re-run must fix the lock first** — re-running the
harness unchanged would reproduce the defect and bank it as a decision.

**Magnitude is unmeasured — do not transfer a number.** The frozen-MC analogue cost
+2.10pp bust at 1.00×, but that engine's mechanics differ from this lifecycle sim
(winning-day, payout, tier, funded-start-cap); scaling the delta across harnesses is the
same non-linear error the 07-22 correction warned against. **Fix:** scope the lock to
`funded_sim` only — in `eval_sim`, `floor = peak - DD` unconditionally.

**Frozen artifacts stay unedited (Trap #12).** `Q-CAPALLOC-1-verdict-preregistration.md`
and `Q-BUSTGATE-1-verdict-preregistration.md` cite these figures and are **byte-unedited**;
this addendum is where the impeachment lives. **H1 in §4 above (measured payout cash within
[0.5×, 2×] of $339/acct-mo) is now a falsifier against a contaminated target** — re-derive
$339 before reading H1, or the band is meaningless.

**Q-BUSTGATE-1 / the EV objective are unaffected in verdict.** Their fork rests on the
frozen-MC regime gate, not on this harness; and the eval-fee-vs-funded-upside asymmetry
(≈12–36:1) is a fee/payout-schedule fact, not a simulator output.

---

## Addendum 2026-07-28b — eval-lock FIXED; §2 re-derived; H1 retargeted to $318/acct-mo

**Fix landed.** Every `eval_sim` / `esim` in
[`lab/analysis/c1/tradeify_book_composition_2026-07-23/`](../../lab/analysis/c1/tradeify_book_composition_2026-07-23/)
now uses `floor = peak - DD` unconditionally (Tradeify article 10495897).
`funded_sim` / `fsim` unchanged. Full record + M-24 sweep:
[`RESULTS.md`](../../lab/analysis/c1/tradeify_book_composition_2026-07-23/RESULTS.md).

**Reproduction control (SHA `602b692`, unmodified):** stage4 matched published
2-leg 63% / 8.2 mo / $339, ORB@1 59% / 6.2 / $556, ORB@6 27% / 1.2 / $941
(tolerances ±1 pp / ±0.15 mo / ±$15).

**Corrected §2 table (eval floor = peak − DD):**

| Book | Eval pass / median | Funded dead-1y | Chain $/acct-mo |
|---|---|---|---|
| 2-leg (c1 geometry) | **38% / 5.8 mo** (was 63% / 8.2) | 43% | **$318** (was $339) |
| +ORB@1 | **30% / 4.1 mo** (was 59% / 6.2) | 69% | **$499** (was $556) |
| +ORB@6 | **12% / 0.7 mo** (was 27% / 1.2) | 93% | **$819** (was $941) |
| +ORB@6 +Aegis (no caps) | **13% / 0.7 mo** (was 29% / 1.2) | 90% | **$1,093** (was $1,233) |

ORB@k frontier (corrected): chain **$499 → $558 → $677 → $735 → $797 → $819** for
k=1→6 (still monotonic; absolute levels lower).

**H1 retarget (§4 above).** The falsifier "measured payout cash within [0.5×, 2×]
of the modeled $339/acct-mo" is a band around a contaminated target. **Replace
$339 with $318** — H1 now reads: measured net payout cash within [0.5×, 2×] of
the modeled **$318/acct-mo** over the first 12 funded-months. §6 D4's plan-math
band likewise uses **$318** (2-leg) / **$499–$819** (conditional on D1 SHIP, by k)
until 12 months of live payout data supersede.

**Conclusions shift (expected).** Eval pass rates roughly halve; chain rates fall
~6–13% relative; churn still maximises chain rate but on a harsher pass/mortality
frontier. Cadence / funded findings that do not route through `eval_sim` stand.

**Q-CAPALLOC-1** remains blocked: operator rule-pin verification (STATE.md
operator-queue item 4) **and** this fix are both prerequisites to its re-run —
not discharged here.

**Post-fix SHA:** `d4c340f` (fix commit on branch
`fix/eval-sim-funded-lock-2026-07-28`).

---

## Verification

Discipline checklist (SKILL.md): §0 populated with anchors ✓ · falsifiable H in §4 ✓ ·
§5 moves genuinely tempting ✓ · §6 binary ✓ · question named as symptom (§1) ✓ ·
§10 runnable ✓ · doctrine-connected (§1) ✓ · compose-objective split forced in §0.5 + §6 ✓ ·
live posture corrected in §1 ✓.


## Addendum 2026-07-29 — funded pins corrected; H1 retargeted again to $299.80/acct-mo

The 2026-07-29 rule-pin verification falsified two of the three funded pins, and the four-step
ladder implementing the correction has now landed. §2's **funded** figures move again (its **eval**
figures are unaffected — both corrections are funded-only, and eval pass held at 37.78% across
every arm):

| Metric | Was (07-28b) | Now (verified pins) |
|---|---|---|
| 2-leg chain $/acct-mo | $318.20 | **$299.80** |
| funded dead-1y | 42.77% | **49.06%** |
| ORB@6 chain | $818.73 | **$792.91** |

Cumulative on the chain rate: **$339 → $318 (eval-lock fix) → $299.80 (funded pins)**, −11.6% from
the originally published figure.

**§4 H1 is retargeted a second time.** It now reads: measured net payout cash within
[0.5×, 2×] of the modeled **$299.80/acct-mo** over the first 12 funded-months. The $318 band from
Addendum 2026-07-28b is superseded.

Funded mortality is the larger finding: nearly **half** of funded accounts die within a year at the
verified rules. Evidence + attribution (three arms, super-additive corrections):
[`tradeify_book_composition_2026-07-23/RESULTS.md`](../../lab/analysis/c1/tradeify_book_composition_2026-07-23/RESULTS.md)
§Addendum 2026-07-29.

---

## Addendum 2026-08-06 — §5 item 5 gained ONE named, narrow exception (not a re-scope)

**§5 stays byte-unedited.** *"Manual token trades to satisfy the activity rule — off-spec discretion
… Rail-level answer or accept warnings"* remains the standing forbidden move. A reader landing on
that item alone would now be wrong to conclude it is unqualified — the operator ruled a single,
named exception on 2026-08-05, recorded at
[`docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md`](../notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md)
§2a-RULED and boarded at `STATE.md` operator-queue row 0: *"We will not let the venue lapse. If no
strategy has been found by Friday we will submit a token trade."*

**Scope of the exception, stated so it cannot be over-read:** ONE manual token trade, in ONE named
week (2026-08-03 → 07), submitted by the **operator at the venue** — never the rail, never an agent.
Recorded explicitly as a deliberate crossing with reasoning (programme-audit degeneration signal #7),
not a silent erosion of this item, and it does **not** re-open the CFD-retirement anchor this item
cites. A second week's coverage is a fresh decision, routed through fork **F2** (2026-08-08), not an
extension of this exception.

---

## Addendum 2026-08-16 — §6 D3 ruled MOOT/STRANDED (governance-holes closing pass)

**§6 stays byte-unedited**, same discipline as the addendum above. D3 ("Churn-posture question,"
§6, admitted as a named fork requiring "decided by ADR or explicitly deferred with a revisit date")
was never formally closed by any artifact — a repo-wide sweep (STATE.md, `docs/briefs/INDEX.md`,
`docs/rejected_candidates.md`) found zero references to it outside this brief and one incidental
forward-pointer in a planning doc that was never executed on. This addendum closes that hole with a
**light decision record** (ADR-ceremony-tiering test: no K/$ spend, no live-risk surface, no
locked/frozen surface, and — the one to guard against — **no new doctrine**: this ruling observes
that D3's subject no longer exists, it does not choose accept-churn or reject-churn as standing
posture for any future book).

**Ruling: D3 is MOOT, on the same grounds — and by the same mechanism — as this brief's own D1
(ruled MOOT at the 2026-08-06 claim-alignment pass, top of file).** D3's Limb B(ii) role (the
"fresh Accepted ADR" branch that would supersede Q-COMPOSE-1 by choosing chain-rate/accept-churn)
only matters if D1's SHIP-3-leg path is live — and D1 is already MOOT ("no deployed book to HOLD,
no account to SHIP to, neither branch takeable"). Independently: the composed book D3 would have
adjudicated (2-leg Striker + ORB, +optional Aegis-6J) no longer exists as a deployable
configuration — both Striker legs were withdrawn 2026-08-04
([`ADR`](../adr/2026-08-04-tradeify-venue-descope-eval-included.md) §2: "no further work is
authorized whose sole justification is reaching, holding, or passing a Tradeify account to deploy
those two legs"), and ORB-MNQ, the leg whose sizing drives the entire chain-rate frontier D3 would
weigh, is itself PARKED ([`b3`](../pursuits/b3-orb-mnq-payability-line.md), expiring to SUBTRACT
2026-11-08 absent renewal).

**Q-COMPOSE-1's `FALSIFIED` verdict never answered D3 and is not being read as if it had.** Its
own closure text engages only the survivor-scoring floor (bust ≤3.0%), never posture/churn
language, and this brief's own §0.5(5)/§5(4) explicitly forbid treating chain-rate evidence as a
silent D3/D1 flip. What resolves D3 by default is the *absence* of any superseding ADR under
Limb B(ii) — Limb B(i) (HOLD) stands unchallenged, exactly as D1 already stood before being
declared MOOT.

**Why STRANDED, not permanently CLOSED.** D3 is framed as a general posture question (accept-churn
vs reject-churn), not scoped only to this specific book — a future composed book (a successor
venue under fork F3, or a new MSL-sourced candidate composed against an existing leg) could
re-raise the identical tension. This matches the five-thread stranded-pending-F3 pattern already
tracked at `STATE.md`'s "No fixed date / gated" section — those threads are recorded as "not
closed, not discharged, and not re-homed to a successor venue — F3 was no-migration (S1)." D3 is
recorded here rather than duplicated onto that board — its home is this brief, its trigger is the
same F3 event.

**Re-entry bar:** fork F3 registers a successor venue (or an existing leg re-enters a live book)
**and** a new composed-book candidate reaches this brief's D1-shaped gate. At that point D3
re-opens as a fresh fork citing this addendum, not as an automatic revival of the 2026-07-23
frontier table (which would need re-measurement against the new venue's rules regardless).

**If a future operator instead wants to rule accept-churn or reject-churn as standing doctrine**
for any future composed book — not scoped to this withdrawn one — that is a genuine new-doctrine
act requiring the FULL ADR template (ceremony-tiering limb 4), independent of this mootness
ruling, and this brief's own H2 (§4) already gates any such admission behind its own explicit ADR
requirement regardless.

| Date | Change | By |
|---|---|---|
| 2026-08-16 | Addendum: D3 ruled MOOT/STRANDED — subject (composed Striker+ORB book) withdrawn 2026-08-04, D1 (its parent gate item) already MOOT, ORB-MNQ PARKED. Light decision record (no doctrine created); re-entry bar tied to fork F3. §6 unedited. | Joshua (direction, task start) + Claude Code (draft) |
