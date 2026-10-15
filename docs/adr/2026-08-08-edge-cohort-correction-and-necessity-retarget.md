# ADR 2026-08-08 — Edge-cohort provenance correction + necessity retarget (strategy OR book, Tradeify incumbent eval)

**Status:** `Accepted` — §8 ratified by JA 2026-08-08; TNEC-1 `PROPOSED → RATIFIED` atomic in the same commit. **TNEC-1 supersedes MNQDTL-1 as the intake gate** (MNQDTL remains `RATIFIED` historical target; §3.1 doors C1–C11 stand). SPECs are outside the ADR graph — in-part supersession of MNQDTL-1 §1 D1/D2/μ + §6 gate and EM-screen §2 EM1 row is recorded on those specs' headers + this ADR §2-B / §8 (not via machine `Supersedes:` edges).
**Decision date:** 2026-08-08
**Authors:** Joshua (direction) + Claude Code (Fable 5, evidence trace + draft); ratification Cursor + JA
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-12-msl-sourcing-channel-ratification.md` — §2-C L2 channel taxonomy **by addition only** (MSL named as a sourcing channel); 2-A/2-B and L1/L3–L5 untouched.
**Superseded-in-part-by:** `2026-08-24-sourcing-phase-channel-retirement.md` — §2-C row L1 only (Route B lane disposition, `PAUSED` → `RETIRED`); L2 (above), L3–L5, and §2-A/§2-B untouched.
**Superseded-in-part-by:** `2026-08-26-striker-legmap-cap-release.md` — §L4 row's "Named ruling owed before any deployment" clause on `LEG_MAP`'s 69/11 allocation only; the rest of L4 (book-shape admission) and every other row untouched.
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0 read table, §1 cost and superseded-by-events narrative (the venue-binding sentence §5 relies on is kept), §2-A not-rewritten list, §2-B item 3 body (historical), the §2-C not-commissioned line, §3 alternatives table, §6 list, §10 hooks 1/2/4/6, Verification and the 2026-08-29 addendum body removed. §1 cohort table, §2-A/B/C rulings, §4 (R1–R4 and its trigger schedule), §5 and §8 unchanged. Pre-trim text at blob `a553325063f4150907487c4805f259a9fe0a2b5d` (commit [`4121e84c95f4990b71962e3b9570c4c3fad88426`](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md)).
**Related:** [TNEC-1 spec](../spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) (the successor target, same packet) · [MNQBASE-1 §1.3](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md) (the correct cohort table) · [ORB re-park ADR](2026-08-03-orb-mnq-repark-payability-falsified.md) · [seed-target-spec RESULTS](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/RESULTS.md) · [S1 ADR](2026-08-07-loop-s1-environment-ratification.md) · [W1 method](../load_bearing_numbers.md#1-standing-rule--eval-bust-figures-are-eod-clock-lower-bounds) · [catalogue K wall](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md) · [MSL ratification](2026-08-12-msl-sourcing-channel-ratification.md)
**Layer:** research-target doctrine + provenance correction. **$0 / K=0.** No `core/`, Pine, allocation, `dd_protection`, lifecycle, `LEG_MAP`, or rail change; nothing armed; no venue action. Full-tier per [ceremony tiering](2026-08-08-adr-ceremony-tiering.md) limbs 3+4 (supersession of ratified surfaces; doctrine), written compact.

---

## §0 — Rule 0 reads (verified this session, 2026-08-08, worktree clean)

Rule-0 reads (verified 2026-08-08, worktree clean): `core/firm_rules.py` `Tradeify_Select_100K` (`45e3cea`), `ops/instruments/MNQ.md` (`af3b776`), the MNQDTL-1 spec, the EM screen, the seed-target study, the survivor-scoring prereg and the four Route B campaigns. The read table is in the pre-trim text (Revision).

---

## §1 — Context: the erratum, and what it was costing

**The error.** A per-trade edge of **0.85R** entered the estate on 2026-08-03 labelled *"measured from the venue-edition exports"* ([inverse-requirements §5](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md)) — the venue editions being the **withdrawn, pyramided Striker NAS100→MNQ leg** (0.35 trades/cal-day, correlated adds). No derivation was ever published; `run_slow.py:108` hard-codes it. On 2026-08-04 the referent silently mutated: [slow-archetype L123–124](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md) re-attributed it to *"N1 … ORB-MNQ-1's realized edge"* — while ORB's realized edge is **+0.0626R** (n=1,846, [re-park ADR](2026-08-03-orb-mnq-repark-payability-falsified.md)) and N1 contains no per-trade R at all. The false binding then propagated: MNQ.md **N13** → EM screen **EM2** ($325 @ 0.85R cell) → **MNQDTL-1** §1.2 (L=$325 elected as "the published MNQ 0.85R EM2 frontier cell"), §1.3 ("0.85R — MNQ best-ever measured (ORB-MNQ-1, N1) … clears (+$26)"), §3.2 O1 ("ORB edge is real: 0.85R per-trade"). [MNQBASE-1 §1.3](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md) — authored 2026-08-04, *before* the target spec — already published the correct table and was not consulted. (`lesson_metric_cohort_provenance_binding` + `lesson_borrowed_numbers_need_connecting_arithmetic`, both firing on a ratified surface.)

**The corrected cohort table (canonical; supersedes every "MNQ best-ever measured 0.85R" quotation):**

| Cohort | Per-trade edge | Cadence | Independent entries? | Admissible at the incumbent eval? |
|---|---|---|---|---|
| Striker NAS100→MNQ (withdrawn) | **0.85R** | 0.35/cal-day | ✗ pyramid = correlated adds | ✗ barred leg; EM3-dead shape |
| Striker DJ30→MYM (withdrawn) | **0.49R** | ~0.35/cal-day | ✗ pyramid | ✗ same |
| ORB-MNQ-1, realized | **+0.0626R** (n=1,846; ~0.09R gross) | ~1/day | ✓ | ✗ T2: intraday-honest bust ≥67.67% at every k |
| Oracle top-1/day ceiling (restart clocks, s=40) | **0.3998 / 0.3984** | 1/day | — | a ceiling, not a construct ([Q-MNQSEL-1](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md)) |

**Venue binding (cited by §5).** The [seed-target study](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/RESULTS.md) measured the eval's binding constraint as "the weekly activity rule and nothing else", with admissibility reaching ≈+0.10R at $75/trade; 0.40R is where the frequency lever dies, not where admissibility dies.

---

## §2 — Decision

### 2-A — Correction (factual; lands with this packet, not gated on §8)

Reader-intercepts land at every surface where the false binding is **read** (frozen bodies byte-intact; banners only):

1. [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) **N13** — ⚠ cohort-correction lead-in inside the row (N10-banner convention).
2. [MNQDTL-1](../spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md) — intercept blockquote above §0 covering §1.2 / §1.3 / O1 / O4.
3. [EM screen](../spec/2026-08-05-eval-mechanism-shape-screen.md) — intercept blockquote above §2 (table unedited per its own change control).
4. [slow-archetype RESULTS](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md) — banner under Status (covers L123–124 and the `run_slow.py` hardcode; MYM 0.49R same caveat).
5. [inverse-requirements RESULTS](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md) — banner at top (covers §5's two-cell table).

### 2-B — Necessity retarget (effective at §8)

The operator's direction is to do **only what is necessary to construct a Tradeify-compatible strategy or book of strategies**. Accordingly:

1. **Adopt [TNEC-1](../spec/2026-08-08-tradeify-necessary-conditions-target-spec.md)** as the standing target: the five venue/program-necessary conditions (weekly activity · frozen survivor gate on the honest clock · positive net edge with CI + DSR-at-K · independence/stop-integrity + session/slot legality · candidate-derived sizing ceiling), for a **single construct or a book scored jointly**.
2. **MNQDTL-1 superseded in part:** D1 (daily cadence), D2 (L=$325), and the §6 μ ≥ $130/day gate are **demoted from gates to recorded preferences** — reportable coordinates, never intake kills. Its §3.1 closed doors (C1–C11) and §3.2 scope pins are ledger facts and **carry forward unchanged**. The income aspiration (μ* ≈ $250/day) is preserved as a *funded-phase design preference*; re-electing it as a gate is a fresh F-E-class ratification against the **corrected** cohort table, never against the phantom.
3. **`Q-MNQDTL-CON-1` re-pointed, not re-scoped.** *(historical — Q-MNQDTL-CON-1 closed FALSIFIED 2026-08-09; see change history)*
4. **EM screen amended in one row (supersession-in-part, not in-place edit):** **EM1** re-types from "≥0.40R net intake-kill" to — *necessity:* net expectancy > 0 after Requirement-5 costs (screen $0.95/side) with a pre-registered 95% CI excluding 0, plus DSR ≥ `floor_at_k(K_intrinsic)` (EM0 unchanged); *disclosure (retained verbatim):* below ~0.40R the frequency lever **inverts** — frequency can never rescue a thin edge, and any re-elected income target re-instates 0.40R-at-L arithmetic explicitly. EM0, EM2 (principle + edge-indexing), EM3, EM4, EM5 are **unchanged**; EM2's published cells are void **as provenance** (the $325 cell traces to the phantom) and re-derive per candidate from its own measured edge at a stated tolerance.

### 2-C — Lane dispositions (effective at §8; each strips non-necessary work)

| # | Lane | Disposition |
|---|---|---|
| L1 | **Route B OF-minute catalogue** | **PAUSED** — no new G0 in the {order-flow aggregate × minute-scale clock × 60 s mid-return × ρ} family. Grounds are design, not market: the \|ρ\|≥0.02 floor ≈ 0.3 pt @1σ vs 0.95 pt RT and the 3–9 pt/trade requirement; EM1/EM2 returned SHAPE-UNSCREENABLE in all four campaigns because no tradeable P&L object was ever the target; zero CONFIRM stages have ever run. Any future catalogue must pre-register a **tradeable-object target** (first-passage / stop-target R at session-relevant horizons) with a promotion floor derived from that cost arithmetic. Answers the open [SESSIONS 08-08j fork](../SESSIONS.md) on the *pause* side. Avenue A Route A/B doctrine itself is untouched. |
| L2 | **Sourcing (the R2 successor bar)** | Next intake pass draws **only from channels with zero or partial recorded coverage** in the ratified taxonomy: rank-3 dedicated futures-journal sweep (*JFM/JBF/JFQA* — the doc's own "under-mined") · rank-1 citation-graph **re-run** (the sole burst logged HTTP-429 partial) · rank-4 COT/TFF direct data read (never executed) · SSRN full-text via the in-browser route (403-walled to date) · a systematic arXiv q-fin sweep (Mesfin was a single entry) · rank-6 δ-extraction probes. The structural-flow census stays closed (5 dry passes). **Harvest Req 1–5 unchanged** — evidence quality is not the binding constraint and is not loosened. This satisfies the MNQBASE-1 STOP's "new sourcing channel" bar within the existing taxonomy. |
| L3 | **Instrument pool** | MES and MGC **re-enter the candidate pool** — their third-leg eliminations (`E-KCAP`/`E-K`) rest on K arithmetic voided by [ADR 2026-08-04](2026-08-04-family-k-bank-disclosure-not-gate.md) and were never revisited. M2K's one-shot bank rule + WSTRUCT sequencing + W4 cost-dry-run gate stand; MCL is measured-never-scored and open (frozen `CONFIG-B-MCL` available). Instrument election per candidate remains an operator choice; data pulls remain cost-dry-run-gated. The instrument lane runs **in parallel with** MNQ work, not sequenced behind a 2026-11-08 falsification. |
| L4 | **Book shape** | Admitted first-class (the "or book of strategies" direction). A book satisfies N-ACT **jointly** (measured co-idleness disclosed — the incumbent book's failure was correlated idleness), N-SURV **composed and both regime halves**, and EM5's compliance limbs (§4a Product-Group sign constraint · S7 order-symbol occupancy · account-aggregate cap). ~~**Named ruling owed before any deployment:** `LEG_MAP`'s 69/11 allocation is retained-not-released under S1 — release/re-derivation is an explicit operator ruling at first deploy, for a single construct as much as for a book.~~ **RULED 2026-08-26** — [`2026-08-26-striker-legmap-cap-release.md`](2026-08-26-striker-legmap-cap-release.md): `cap_alloc` released to 0/0, full 80-micro cap now unclaimed for a future leg's own allocation. |
| L5 | **Explicitly NOT reopened** | MNQDTL §3.1 doors C1–C11 · ORB-MNQ at Tradeify (re-park R2/R3 are the only routes; T2 stands) · both Striker legs · Aegis→6J admission (H1-negative on the H1-covering panels; its blocker is regime sign, not composition — an optional **$0 hygiene cell** (0.50× standalone on the `76620` panel) may be run to make the ledger's stated blocker match reality; watch-don't-act) · harvest Req 1–5 · the M1 arm gate, per-session GO, and every safety invariant. |

> ⚠ **Addendum 2026-08-24 — row L1 superseded from `PAUSED` to `RETIRED`.**
> [`ADR 2026-08-24 — sourcing-phase channel retirement`](2026-08-24-sourcing-phase-channel-retirement.md)
> (`Accepted`) retires Avenue A Route B (generate→confirm) **in full** — not only the one OF-minute
> catalogue family this row paused. Ground: 0/4 campaigns, across the mechanism's entire life (not
> just this family), ever reached the confirm stage; the governing ADR's own empirical falsifier
> cannot fire because it requires a `RESOLVED` CONFIRM verdict that has never existed. Rows L2–L5 and
> §2-A/§2-B above are untouched. The L1 row text above is left unedited (dated-decision integrity);
> this note is the reader intercept.

---

## §3 — Alternatives considered

**Grounds.** Fixing labels alone left an income floor presenting as venue-derived; loosening harvest Req 1–5 would not change the finding rate; only EM1's threshold was elective, so EM1 is re-typed surgically; ORB stays parked because T2 is a venue-survival failure under the necessity gate too.

---

## §4 — Falsifier (for this ADR)

**H:** *after ratification, the TNEC-1 necessity set admits exactly what the venue + standing program law admit — no elective constraint remains disguised as necessity, and no necessary constraint was dropped.*

| # | Trigger | Threshold | Action |
|---|---|---|---|
| R1 | A hidden gate remains | a candidate clears N-ACT…N-SIZE and is then blocked at intake by any constraint not in TNEC-1 or standing law (Req 1–5, EM0, regime gate, K discipline) | name it; supersede TNEC-1 to include or strike it — never block informally |
| R2 | A necessary limb was dropped | a TNEC-1-clear candidate fails the eval in simulation (or live sandbox) on a rule TNEC-1 does not carry | author the missing limb by superseding spec (EM screen §4 F-A analogue) |
| R3 | Phantom residue | any TNEC-1 or amended-EM threshold shown to still trace to the 0.85R cell | re-derive from the corrected cohort table; supersede |
| R4 | Erratum overturned | a panel-derived, independent-entry MNQ construct measurement of ≥0.85R/trade surfaces with published derivation | this ADR's §1 table gains a row; the correction stands (it is about provenance, not possibility) |

**Trigger check schedule:** R1/R2 on each candidate scored; R3 at the first quarterly audit after ratification; R4 on any new MNQ measurement.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Re-introducing an income floor as a side condition** ("candidates below $X/day aren't worth scoring"). That is D1/μ* re-entering by the back door; income shape returns only by explicit re-election against the corrected table.
- **Reading 2-A's banners as authorizing threshold changes before §8.** The banners correct *attribution*; every ratified constant stands until ruled.
- **Editing frozen bodies in place** (EM §2 table, MNQDTL §1.3, lab RESULTS) instead of intercepts — Known Trap #12 / the screen's own change control.
- **Using the eval's ≈+0.10R admissibility to skip DSR-at-K, Req 1–5, or the regime gate.** The venue admitting slow thin edges does not make thin evidence admissible.
- **Treating L1's pause as closing Avenue A or as a verdict on MNQ microstructure.** It is a family-scoped design pause; the nulls measured the instrument, not the market.
- **Letting the book clause admit a negative-expectancy cadence leg.** Q-CADENCE-1's C2 lesson stands: a leg that costs money is a maintenance trade with worse variance.
- **Reading this ADR as a Stage-0 GO, PREREG freeze, or Cap claim for `Q-MNQDTL-CON-1`.** It stays `OPEN`/unpaid exactly as filed (§2 item 3) — genuinely tempting because the re-pointer reads as an endorsement of that specific cell.
- **Deploying anything on this ADR's authority.** M1 `RESOLVED` + separate operator GO + `LEG_MAP` ruling remain the deploy chain; this packet is research-target doctrine only.

---

## §6 — Consequences

Recorded at ratification: candidate intake gated by the five necessary conditions; Route B family paused with grounds; instrument lane unblocked; MNQDTL-1 superseded in part ~1 day after ratification. Full list and ratification-time propagation: pre-trim text (Revision).

---

## §8 — Ratification

```
RATIFICATION:    2-A erratum ACKNOWLEDGED (banners stand as filed).
                 2-B necessity retarget: TNEC-1 ADOPTED; MNQDTL-1 superseded in part
                 as intake gate (D1/D2/μ-gate → recorded preferences; MNQDTL stays
                 RATIFIED historical target; C1–C11 stand); EM1 re-typed per 2-B.
                 2-C lane dispositions L1–L5 RULED as filed.
DATE / INITIALS: 2026-08-08 / JA
```

| Date | Change | By |
|---|---|---|
| 2026-08-08 | §8 Accepted; TNEC-1 RATIFIED atomic | JA |
| 2026-08-12 | `Superseded-in-part-by` → MSL ratification ADR (L2 taxonomy addition only — MSL named) | Joshua (B1) + Cursor |
| 2026-08-29 | Addendum: `Q-MNQDTL-CON-1` closed FALSIFIED 2026-08-09; §2-B item 3 / §10 hook 6 "stays OPEN/unpaid" now historical-only (adr-decay-audit discharge) | Claude Code |
| 2026-10-15 | Trim: §0 table, §1 narrative, §3 detail, §6 list, §10 hooks 1/2/4/6, Verification and the addendum body removed to history (Revision pin); §1 table, §2-A/B/C, §4, §5, §8 kept; R3 rider unchanged pending operator ruling | ADR decay audit |

---

## §10 — Audit hooks (runnable)

```bash
# 3. Venue-necessary geometry unchanged (fires R2-class review if it moves).
python -c "
import sys; sys.path.insert(0,'core')
from firm_rules import FIRM_RULES
t = FIRM_RULES['Tradeify_Select_100K']
assert t['daily_loss_pct'] is None and t['max_dd_pct']==3.0 and t['inactivity_max_idle_days']==5 and t['micro_contract_cap']==80
print('necessary-set geometry OK')"

# 5. TNEC-1 adoption state matches this ADR's Status.
rg -n "^Status:" docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md
```

**Addendum 2026-08-29 (condensed 2026-10-15):** `Q-MNQDTL-CON-1` closed `FALSIFIED` 2026-08-09 (both arms negative, CI below 0); §2-B item 3 is historical; no operative clause depended on it. Full text: prior text (Revision).
