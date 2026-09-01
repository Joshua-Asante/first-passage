# 08-08 packet — delta update (2026-07-12 → 2026-08-01) + execution sequence + pre-work

**Status:** `DRAFT — SUPERSEDED BY EVENTS (see Addendum below); operator sign-off no longer the live path for any residual line item` — updates the **RATIFIED** pre-triage; records
2026-07-23 operator posture **and** verified 2026-07-31 supersessions; adjudicates nothing that
still requires a gate or admitting ADR.
**Authored:** 2026-07-17 · **Revised:** 2026-07-23 (operator tension resolve + slate sync) ·
**Revised:** 2026-08-01 (ORB unpark + forward-board sync; no new operator directives invented) ·
**Revised:** 2026-08-02 (ORB §4 T2 **measured** — three stale "T2 waits on / off-slate until the `intraday_low=` limb lands" clauses corrected at §0, §1 row 6, and the new/revised-rows table; **no directive invented, no trigger adjudicated, nothing struck from the slate**) ·
**Revised:** 2026-08-02 (b) (**acceptance DRAFTED — §11**; H-DELTA walk **run**, `FALSIFIED` on one miss → Sentinel limb-B1 row added → re-walk clean; **A5 + P1 struck** with the Pepperstone feed retirement and §6's now-void *"P1 discharged or A5 `NOT_EXECUTABLE`"* trigger rewritten; **A1 re-scoped not decided**; two record-only rows added. Status stays `DRAFT` — the §11-D sign block is **unsigned**) ·
**Revised:** 2026-08-03 (**ORB §4 T2 RULED FIRED** — the owed disposition is taken, ORB-MNQ-1 re-`PARKED`, payability target **FALSIFIED**; the three "disposition owed / record-only" ORB clauses at §0, §1 row 6, and the new/revised-rows table are now **discharged**, and ORB leaves the slate as a must-decide. Operator ruling recorded, not invented; no other slate row moved. **Merge note:** authored before the 08-02 (b) acceptance draft reached `main`, and reconciled onto it here — the A5/P1 retirement, the H-DELTA repairs, and the Addendum-31b `Accepted` correction are all upstream's and are preserved unchanged) ·
**Addendum:** 2026-08-29 (Rule 14 correction, no body edit — full text in Change history below: the event that actually ran on 2026-08-08 was a disjoint programme audit/prune, not this packet's own gate walk; §2 step 5 / Q-EVALSEQ-1 closed independently `FALSIFIED` 2026-08-16; A1 remains genuinely open, on a different path than this packet's §11; Sentinel limb B1 unaffected; §11-D stays unsigned — see the note above that sign block)
**Parent artifact:** [`2026-07-12-08-08-packet-pretriage.md`](2026-07-12-08-08-packet-pretriage.md) (RATIFIED 2026-07-12, anchor `fad8984`). Classification (A/B/C/off-slate) and no-cascade rule are **inherited**; this brief records deltas, sequences the run, and names dated pre-work. Where this brief and the pretriage disagree, the pretriage wins until the operator accepts a delta row — **except** rows marked `OPERATOR 2026-07-23` (historical posture) or `VERIFIED 2026-07-31` / `OPERATOR 2026-07-31` (live supersessions).
**Companion gate-input:** [`2026-07-23-tradeify-book-composition.md`](2026-07-23-tradeify-book-composition.md) (chain-rate / composition economics; naming collision note on D1 retained there).
**Series:** strategy-R&D priorities 2026-07-17 — **rank 4 of 4**.
**D-S-A domain:** meta-process (slate bookkeeping only).

---

> ⚠ **READER INTERCEPT 2026-08-06 (claim-alignment M30):** this slate **predates** the 2026-08-04
> Tradeify venue de-scope and the same-day operator-queue reset. It contains **no de-scope content**.
> §4 already mandates re-walking the current board at the gate — **do that before step 1**; do not
> treat this packet as the live execution slate.
>
> **Floor list of known additions the old table cannot contain** (floor, **not** a substitute for the walk):
> **F2**, **F3**, the **08-08 audit vehicle**, the four stranded gate falsifiers **G3/G6/G2/G8**,
> venue de-scope §4 **T4**, the **G4 follow-ups**. Re-run the §4 walk against `STATE.md` at the gate.


## §0 — Rule 0 reads (verified 2026-08-01, this revision)

- Parent pretriage — tip `11f8193` (2026-07-29); ratification anchor `fad8984` (still an ancestor of `HEAD`).
- Prior delta body (this file @ `730bb29`, 2026-07-23) — superseded in place by this revision.
- `STATE.md` — tip `2c5f937` (2026-07-31). Forward board + operator queue read for H-DELTA; living-board prune of discharged lines remains a separate owed session (not done here).
- ORB unpark ADR — [`2026-07-31-orb-mnq-unpark-payability-target.md`](../../adr/2026-07-31-orb-mnq-unpark-payability-target.md) @ `b22aef8` (2026-07-31); §4 T1 `PASS`. **SUPERSEDED IN PART 2026-08-03** (`VERIFIED 2026-08-03`): T2 was **RULED FIRED** on the Part A bust reading and the owed disposition is **taken** — ORB-MNQ-1 is re-`PARKED` and the payable-Tradeify-leg target is **FALSIFIED** ([`2026-08-03-orb-mnq-repark-payability-falsified.md`](../../adr/2026-08-03-orb-mnq-repark-payability-falsified.md)). Both frozen survivor-scoring limbs fail at every k (bust 67.67/77.01/80.18% vs 3.0%; P(pass) 32.33/22.99/19.82% vs 50%), and T2's own cap-at-k=1 remedy is **inert**. **H is no longer open.** The 07-31 ADR's §3 evidence, both 31b rulings, and the 31c/08-02 measurements are retained `Accepted`.
- Monitoring ADR — [`2026-07-22-c1-venue-native-monitoring-maturity.md`](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md): body `Accepted` (2026-07-23); Addendum 2026-07-31 (item-5 stands) `Accepted`; **Addendum 2026-07-31b (gate-trigger move) `Accepted` — operator-ratified 2026-07-31** (*"ratify the trigger change"*). ⚠ **Corrected 2026-08-02:** this line read `Proposed` / *"ratification owed"*, which was **stale** — the ADR itself records the ratification at four normative sites. The M1 gate's trigger is the **arm**, not the send: `dry_run=false` may not be set while M1 is not `RESOLVED`. ⚠ **Merge note 2026-08-03:** the 08-03 ORB branch was cut before this correction landed and carried the stale `Proposed` reading; **upstream's corrected line is taken here verbatim** — the ORB ruling touches nothing in the monitoring ADR.
- Substrate retirement ADR — [`2026-07-22-challenge-era-substrate-retirement.md`](../../adr/2026-07-22-challenge-era-substrate-retirement.md) @ `fc14682` (Phase 4 tip): Phases 1–4 landed (`ACTIVE_FIRM` / `FIRM_RULES["FXIFY"]` / `BASELINE_BALANCE` deleted); destructive Phases 5–6 separately gated.
- `core/firm_rules.py` — tip `7781437` (2026-07-31): **no** `ACTIVE_FIRM` selector; live c1 key is explicit `Tradeify_Select_100K` (directive-(4) prose half is discharged in code; forward-board residue prune still owed).
- Fork-B ADR — [`2026-07-23-c1-rung-selection-ev-objective.md`](../../adr/2026-07-23-c1-rung-selection-ev-objective.md) @ `9ab2e8b`, `Accepted` (same-day ratify 2026-07-23).
- Q-EVALSEQ-1 pre-reg — [`2026-07-24-2leg-eval-frontload-schedule-preregistration.md`](pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md) @ `25bd4d8` — OPEN; bounded MC **08-08-gated**, K=4 frozen.
- Methodology 90-day — [`2026-07-29-methodology-90day-rebound-review.md`](../../notes/audits/2026-07-29-methodology-90day-rebound-review.md) **CLOSED 2026-07-29**.
- ~~A5 harness — `regime_gate.py` … `NOT_EXECUTABLE` until a fresh Pepperstone export.~~ **SUPERSEDED 2026-08-02: A5 is RETIRED and no export is owed.** The Pepperstone feed was retired in both tiers and its bytes deleted, so `decompound.py` / `regime_gate.py` are **unrunnable by construction** — the honest state, not a defect. ⚠ This also **orphans the decompound-HOLD §4 limb-2 LIVE falsifier**: it survives on paper and cannot fire, so the HOLD currently has **no live falsifier**. Successor design landed (build gated on the first live fill, not on 08-08) — [feed-retirement ADR](../../adr/2026-08-02-pepperstone-feed-retirement.md) §2-B/§2-D · [monitor design](../superpowers/specs/2026-08-02-venue-native-regime-monitor-design.md).
- ~~GO ADR + RUNBOOK — … B7-REFIRE Stage 1 desk card prepared for **Tue 2026-08-04**…~~ **STRUCK 2026-08-06 (M30)** — desk card mooted by ADR §6; rail retained disarmed pending F2.
- [`2026-07-13-prop-survivor-scoring-prereg.md`](pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) — Part A bust ≤3.0% / pass ≥50% (Trap #12 intact).
- Rescope ADR D2 addendum — [`2026-07-11-challenge-era-claims-rescope.md`](../../adr/2026-07-11-challenge-era-claims-rescope.md): quarterly C2→C0 revert check **RETIRED**; Pepperstone released from successor-diagnostic duty.
- Book-composition brief — [`2026-07-23-tradeify-book-composition.md`](2026-07-23-tradeify-book-composition.md).
- Harnesses on disk: `lab/analysis/regime/decompound_remc_2026-06-07/regime_gate.py` (A5) · `lab/discovery/lifecycle_call1/harness.py` (A3) · `lab/analysis/time_to_pass.py` (C1 harness **exists** but is **no longer a standing 08-08 obligation** — D2 retirement).

---

## §0.5 — Operator posture recorded 2026-07-23 (historical; load-bearing then)

These seven directives were **operator-recorded** on 2026-07-23. They aimed the packet; they did
**not** by themselves amend frozen pre-regs, GO ADRs, or live sizing. Rows superseded after that
date are marked in §0.5b — do not re-apply a superseded consequence as live.

| # | Directive | Packet consequence (as of 2026-07-23) |
|---|---|---|
| 1 | **Recalculate the ratified bust gate** from eval-fee vs funded-upside economics (Q-FUNNEL-1 evidence as input) | New Class-A / pre-work item **P0 / A0** — fresh brief + freeze before any 3.0% → *new* ceiling edit (Trap #12). Standing Part A remains **3.0%** until that brief admits a successor. |
| 2 | **Aim to run both admitted c1 strategies at 1.00×** (MYM + MNQ Striker venue editions) | Target authorization for the armed book; **gated** on (1) clearing the successor bust gate at 1.00× **and** a GO-ADR / lifecycle rung amendment. WATCH-1 0.50× remains the last *ratified* deployable rung until then. |
| 3 | Close the **monitoring gap** in a **separate session** | Off this slate’s execution path. ADR was then Proposed; M1 named as a B7 precondition — not decided here. |
| 4 | Complete **substrate retirement** + resolve **doc-authority drift** in a **separate session** | Off this slate. Included CLAUDE/STATE `ACTIVE_FIRM` prose, forward-board C2→C0 residue, remaining retirement phases. |
| 5 | **Update this 08-08 packet** | The 2026-07-23 revision. |
| 6 | **ORB-MNQ remains PARKED** for now | Book-composition D1 defaults to **HOLD 2-leg**; no ORB rail integration / compose / decay-calibration as an 08-08 must-decide. CANDIDATE standing unchanged; park is operational, not a lifecycle demotion write. |
| 7 | **Spend ceiling $700 stands**; JULY promo **already applied** to the current Tradeify Select challenge | Strike “promo expires 07-31 → urgency” framing from deployment prep. Ceiling and attended bar unchanged; B7 remains a separate GO. |

---

## §0.5b — Posture deltas through 2026-07-31 (verified 2026-08-01; live)

Pointers only — each owner artifact holds the narrative (Rule 7). This section does **not** invent
new operator directives; it records accepted ADRs / closures that supersede §0.5 rows.

| §0.5 # | Live status | Owner / consequence for this slate |
|---|---|---|
| 1 (A0) | **DISCHARGED 2026-07-23** | Q-BUSTGATE-1 `FALSIFIED`; 3.0% retained for admission (Trap #12). |
| 2 (A0b) | **RESOLVED NO-GO 2026-07-23** | Fork-B ADR `Accepted` @ `9ab2e8b`; live rung **WATCH-1 0.50×**; 08-08 calendar dependency removed. |
| 3 (monitoring) | **ADR `Accepted`; M1 not `RESOLVED`** | Architecture in force; M1 spine CODE_LANDED; item 5 + `operator_signoff` still owed. Addendum 2026-07-31b (`Proposed`) is **off this slate** — ratification is a separate operator call. Do **not** fold M1 close into the 08-08 gate session. |
| 4 (substrate / doc-drift) | **Phases 1–4 landed; 5–6 gated** | `ACTIVE_FIRM` deleted in code (`fc14682`). Forward-board / living-board prune of discharged lines **still owed** (separate session). Phase 5 OANDA/Dukascopy wipe remains gated — not 08-08. |
| 5 (packet update) | **This revision** | Syncs the slate to 07-31 facts; operator review still owed on the draft. |
| 6 (ORB) | **RE-PARKED 2026-08-03; target FALSIFIED** (`VERIFIED 2026-08-03`) | The 07-31 unpark is **superseded in part** by [`2026-08-03-orb-mnq-repark-payability-falsified.md`](../../adr/2026-08-03-orb-mnq-repark-payability-falsified.md): T2 **RULED FIRED** on the Part A bust reading, ORB-MNQ-1 returns to `PARKED`, payable-Tradeify-leg target **FALSIFIED**. The 07-23 row's "ORB-MNQ remains PARKED" posture is therefore **restored on the merits**, not merely reinstated. Lifecycle `CANDIDATE @ 1.00×` **unchanged** (no `core/lifecycle.py` write); **no rail integration, no compose, no new K, no book-leg reopen**; `K_banked(MNQ)=2`, Cap seat **unspent**. **ORB is now OFF the slate as a must-decide** — T3 is moot and the T2 disposition is discharged; carry as a **records-pass line only**. Book-composition D1 SHIP path stays blocked (Q-CAPALLOC-2 / rule-pin dependents — operator queue, not §2), unchanged by this. |
| 7 (spend / promo) | **Unchanged** | Ceiling **$700**; promo already applied; B7 separate GO. |

**Also riding the board (not in the 07-23 seven):**

- **Q-EVALSEQ-1** — pre-reg frozen; bounded MC on the **08-08 slate** (K=4). Distinct from ORB k-policy.
- **Q-CAPALLOC-2** — verdict `RESOLVED-FRAGILE`; disposition is **operator queue #5**, not an 08-08 gate step (no default; blocks any `LEG_MAP` change).
- **Fade program** — Stage-0 run on ruled instrument (MCL); **no mechanism proposed**; Cap seat unspent. Sibling of ORB, not a compose candidate.
- **Methodology 90-day** — **CLOSED 2026-07-29** (was “off-slate nearer than the slate”).

---

## §1 — Delta table (pretriage → 2026-08-01)

| Pretriage item | Ratified class | Delta as of 2026-08-01 | 08-08 action now |
|---|---|---|---|
| **B1** envelope v1.0 | B | **DISCHARGED 2026-07-13** | Record only. Overlay 90-day re-verify ~2026-10-11. |
| **11-08 resource collision** | — | **DISCHARGED** (Q-SFRISK-1/D1 closed 2026-07-15) | Strike collision framing; 11-08 binds prop §4 alone. |
| **C7** prop §4 progress | C | Early c1 Part A discharge **WITHDRAWN 2026-07-22** (eval-lock correction); 50K-tier clearers defeat the “no clearer on any tier” demotion clause **without discharging §4**; hard date **2026-11-08** unchanged | **Progress check only** at 08-08 — do not cite superseded 2.65%/2.64% figures. Record withdrawal + 50K caveat. |
| **A2 / D2** | A | **RESOLVED by retirement 2026-07-22** — C2→C0 quarterly check **RETIRED** | **Strike from Class A.** Do **not** run `time_to_pass.py --regime-check` as a standing obligation. |
| **A3** Call-1 first eval | A | Harness landed 2026-07-14; still no strategy-signal live fills in the locked book | Run with explicit inputs → **AMBIGUOUS**; stamp re-confirm 11-08. |
| **A4** flow-data fork | A | **CLOSED DEFER-procurement 2026-07-14** | Leaves Class A. Residue handoff any-time, not 08-08. |
| **A5** decompound-HOLD limb-2 | A | **RETIRED 2026-08-02 with the Pepperstone feed** — `decompound.py:61-78` reads four Pepperstone CSVs, now deleted. A5 monitored regime risk on the locked **CFD** book, on a feed for a **closed venue**, to inform allocations executed as MYM/MNQ on **CME futures**: the same shape D2 retired C1 for | **Strike from Class A.** Not re-pointed — re-pointing it at CME panels would be a new instrument wearing a retired one's ratified standing. The owed **forward** regime monitor survives and re-points venue-native | [ADR](../../adr/2026-08-02-pepperstone-feed-retirement.md) §2-B/§2-D |
| **A1** accept-beta fork | A | **RE-SCOPED 2026-08-02, not decided.** A5 is retired, so *"decide after A5"* has no referent. Evidence base is now venue-native: Q-COMPOSE-1 breadth anti-help; fork program exhausted; ORB-ZB FALSIFIED; **ORB-MNQ reopened 07-31 and closed 08-03 — Tradeify target FALSIFIED** (`VERIFIED 2026-08-03`), so the breadth-lever bench is **empty rather than pending** — it was never a book-leg either way | Decide on the **named venue-native** inputs, stating which it rests on. **Inventing an A5-substitute number to close A1 is forbidden** ([ADR](../../adr/2026-08-02-pepperstone-feed-retirement.md) §5-2). No longer gated on any export, and no longer waiting on an ORB k-policy. |
| **C1** C2→C0 check | C | **RETIRED with D2** (2026-07-22) | **Strike.** Do not conflate with A5. |
| **C3** T2/T3/T4 | C | T4 harness half landed; operating-characteristics study open | Shallow %-complete note. |
| **C4** HARV / inventory | C | Inventory **0**; accept-idle; fork program EXHAUSTED 0/3 edge; fade Stage-0 admits no mechanism | Record inventory=0 + 11-08 idle guard live. |
| **C5/C6** P4 / P3 Kill-D | C | Unchanged | Shallow ratify-or-slip. |
| **C2** Q-USOIL-1 | C | Unchanged | 2-minute re-confirm absent new evidence. |
| **B3** multiplier spine | B | **Affirmed YES** by Q-PYRPARITY-1; substrate Phase 2 **MERGED** (continuous-lot CLI deleted) | Record; live haircut realization path unchanged at WATCH-1 0.50×. |
| **B2** Aegis-6J | B | PARKED 2026-07-16; book-composition D2 reiterates PARKED | Re-price park-consistent; no unpark. |
| **N-2026-07-11** | C | Fire log empty | Ratify-or-slip. |

**New / revised rows riding the packet:**

| Item | Source | 08-08 / pre-gate action |
|---|---|---|
| **A0 — Bust-gate re-derivation** | §0.5 #1; Q-FUNNEL-1; Trap #12 | **DISCHARGED 2026-07-23** — [`Q-BUSTGATE-1`](Q-BUSTGATE-1-bust-gate-re-derivation.md) + [pre-reg](pre-registration/Q-BUSTGATE-1-verdict-preregistration.md) `98d0fa6`; verdict **`FALSIFIED`**; operator elected fork B. 3.0% retained unedited. |
| **A0b — c1 1.00× aim** | §0.5 #2; A0 fork B | **RESOLVED NO-GO (2026-07-23).** Fork-B ADR `Accepted`. Live rung **WATCH-1 0.50×**. Out of the gate sequence. |
| **ORB-MNQ re-PARKED; target FALSIFIED** `VERIFIED 2026-08-03` | §0.5b; [`2026-08-03 ADR`](../../adr/2026-08-03-orb-mnq-repark-payability-falsified.md) `Accepted` | **Supersedes the prior "ORB-MNQ UNPARKED" row.** Record the re-park + the FALSIFIED payability target. The RF&lt;1 / negative-2026 "leading adverse input to any k-policy talk" framing is **discharged** — there is no k-policy talk left to inform; both frozen survivor-scoring limbs fail at every k∈{1,2,3}. **Records-pass line only** — not a must-decide for rail / compose / decay / book-leg, and not a mechanism rejection (scope = one target at one firm). |
| **ORB §4 T2 — RULED FIRED; disposition DISCHARGED** `VERIFIED 2026-08-03` | [`2026-08-03 ADR`](../../adr/2026-08-03-orb-mnq-repark-payability-falsified.md); measurement [`RESULTS_t2_intraday_bust.md`](../../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md) | **Supersedes the prior row's "disposition is operator-owned, record-only" clause — the ruling was made 2026-08-03.** Operator ruled the **Part A bust reading governs**, so T2 fires; and escalated past T2's own Action column because cap-at-k=1 is **inert** (67.67%, 23× the 3.0% ceiling; one contract is the smallest integer expression). Surfaced at adjudication: the frozen gate's **second** limb, P(pass) ≥ 50%, also fails at every k (**32.33/22.99/19.82%**) — **both** limbs fail, not just the one T2 named. **H limb (b) keeps its literal wording** (operator ruling) and stays SATISFIED at $1,432 — deliberately not retrofitted. **Recorded defect:** H's limbs both survive literally while the target dies on criteria H never bound (falsifier-construction class, candidate-status). **Nothing to decide at the gate** — carry as a records-pass line. k policy moot; no new K; rail / compose / book-leg untouched. |
| **c1 cadence / idle rule — token-trade disposition** `VERIFIED 2026-08-02` | [`c1_cadence_inactivity_2026-08-02/RESULTS.md`](../../../lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md) (merged `5417f98`, PR #618) + [Addendum 2026-08-02b](../../../lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md); [compliance §2a](../../notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md); R2 spec [`idle-rule-disposition-options`](../superpowers/specs/2026-08-02-idle-rule-disposition-options.md) | **RULED IN PART 2026-08-02, remainder record-only** — **operator ruling: a hand-POSTed canned payload through the full rail IS "rail-level"**, so the §5(5) fork resolves to its first branch and Option A is the live branch (post-M1). Author's delegated judgments alongside it: **§B8 direct-to-CrossTrade ruled OUT** as an idle-rule mechanism (it bypasses every control the ruling relies on, and leaves no ledger record to mark); the S7-vs-in-book tension resolved to **in-book on Wed/Thu** (both legs' locked Pine filters leave Wed+Thu unoccupied, so session-disjointness satisfies S7 without a foreign leg); recommendation **C now by necessity, A once M1 resolves**. **Status check 2026-08-02: NO warning has arrived, and every complete week has been covered** — 07-20→24 by the B6 dry-fire, 07-27→31 by the SIM `CHAIN_OK`; the account opened Sat 07-18, so 08-03→07 is the **first** week with no coverage yet. The rest is **record-only** — the residual disposition is operator-owned, not a §2 step (same treatment as Q-CAPALLOC-2 above — ⚠ **the ORB §4 T2 comparison this originally also named is void as of 2026-08-03**: T2 was ruled and is no longer operator-owned-and-pending, so Q-CAPALLOC-2 is now the only live exemplar; **not** claimed as an H-DELTA repair — the STATE entry is a pointer-log line, not a forward-board line). **Measured:** a token trade is owed in **82/312 Mon–Fri weeks (26.3%), max 4 consecutive**; the first inactivity-ON Tradeify re-MC prices the mitigation assumption every published pin makes at **92.6–97.6% path death** — **cohort caveat BINDING: panel-geometry, not comparable to the 2.65% / 4.74% / 1.20% pins**, and the semantics caveat (engine rolling-5-idle-bday barrier ≠ venue Mon–Fri bucket) means these are **not a venue forecast**. **NEW and adverse — enforcement is DELETION, not warnings** (art. 12268494, read 2026-08-02): *"your account will be deleted after an email warning"* / *"cannot be reactivated"* / no paused state / non-refundable. This reprices the book-comp §5(5) *accept-warnings* branch from ≈$0 to the eval seat + **$127.40** realized progress + a fresh $700-ceiling draw. **Bind:** the remedy is *"place a trade"*, but the rail form needs `dry_run=false` (**M1-gated**, Addendum 31b — *soft* in code: `--acknowledge-m1-unresolved` exists and has been used twice, so choosing it pre-M1 is a **third knowing deviation**, not an impossibility) while the manual form is §5(5)-forbidden ⇒ pre-M1 the de facto posture is accept-warnings. **Fork is three-way, not two:** manual / rail-level / **direct-to-CrossTrade §B8** (bypasses `dry_run`, `armed_until`, M1, sizing host **and** the EventLedger) — R2 recommends ruling §B8 **OUT** explicitly, since silence permits it. **Finding-2 reading (record):** GO ADR §6 WATCH-1 figures are **DD-survival** figures, silent on cadence — 0.50× cuts DD bust **23.35% → 3.54% (6.6×, −85%)** while **raising** inactivity exposure 93.57% → 97.63%; mechanism = the OFF-arm median days-to-pass 67 → 151 (both ON arms median 11), i.e. a longer eval spans more Mon–Fri weeks; read both levers in any future rung debate. **No pin impeached, no gate moved, nothing armed, $0, K unchanged.** **No ORB relief:** rule is per account, and segregation ADR §5 forbids a foreign leg feeding an inactivity clock at ADR grade. Rail-geometry re-run pre-scoped, runs **only** if consumed at gate grade. |
| **⚠ Segregation ADR §4 revert check — DUE 08-08, was on NO board, and the arithmetic CROSSES the trigger** `NEW 2026-08-02` | [`2026-07-13-prop-account-book-segregation.md`](../../adr/2026-07-13-prop-account-book-segregation.md) §4; [`RUNBOOK.md`](../../notes/rail_build/RUNBOOK.md) spend tally; [R2 spec §7](../superpowers/specs/2026-08-02-idle-rule-disposition-options.md) | **Surfaced, not adjudicated — but it is EVALUABLE and it FAILS on the default reading.** The binary trigger: per-account frictions (eval-fee amortization + **inactivity-clock token-trade drag** + per-account data/rail fees) ≥ **25%** of a registered book's modeled expectancy ⇒ the segregation default **re-opens for that tier class**. Check date **2026-08-08**; it appears on **no STATE forward-board line** (this packet row is the only board entry, added 2026-08-02). **All three limbs have in-repo figures:** token drag **$2.07/mo** + eval-fee **≈$30/mo** + **CrossTrade Pro Monthly Unlimited $49/mo** (the c1 rail's own live subscription, in the c1 spend tally — **not** a Bulenox-era figure) = **$81.07/mo ÷ $299.80 = 27.04% ≥ 25% ⇒ reads `FALSIFIED`**. ⚠ **An earlier draft of this row said the rail-fee limb had "no in-repo figure" and recommended stamping `AMBIGUOUS` — both were wrong**; corrected here rather than silently, since "declared an input missing without searching the rail's own cost record" is the reusable error. **`modeled expectancy` DEFINED 2026-08-02 (operator-directed):** the **renewal-reward chain rate** — expected net payout cash per account-month, expectation-weighted across the eval→funded lifecycle (`pass% × E[cash|funded] / E[cycle]`), **gross of** the three friction limbs = **$299.80/acct-mo**. Chosen on unit match (frictions are per-account-month), lifecycle match (§4 counts the **eval fee**, so a funded-phase denominator would compare pre-funding cost to post-funding revenue), and realizability. Rejected: funded-phase gross P&L, `E[cash|funded]`, panel mean/mo. No double-count — the chain rate is gross of eval fees. **The verdict is N-governed** (only the rail fee amortizes; the subscription is multi-master-account): **N=1 → 27.04% FALSIFIED · N=2 → 18.87% · N=3 → 16.14%**. **Author's delegated judgment: stamp `FALSIFIED (degenerate at N=1)` and take no re-opening action** — the arithmetic is right and should not be softened, but §6 says the ADR was pricing *"account multiplication"*, and at N=1 there is nothing to multiply: segregation imposes **zero** cost, since a co-mingled configuration would incur the identical $81.07. Re-check at N≥2, where the number starts measuring what §4 meant. **What must not happen: stamping `AMBIGUOUS (fee model incomplete)`. No number is missing.** If this check belongs on the forward board, **H-DELTA is already falsified independent of the cadence thread** — the packet's own repair path applies (add row, log miss, re-walk). |
| **Sentinel Tier-2/3 promotion (limb B1)** `H-DELTA REPAIR 2026-08-02` | STATE forward board; re-homed 2026-07-27 from the [Hermes closure](../closures/2026-07-27-hermes-agent-adoption-closure-resolved.md) | **Added by the H-DELTA walk run at acceptance — this row was MISSING and the walk falsified on it.** The obligation is *"no date; blocks nothing; **do before the next quarterly slate**"*, and its own done-condition is *"has run once against the **08-08 slate**"* — so it is a ≤08-08 line and belonged here. It is a **promotion, not a build**: the v1 spec says Tiers 2–3 *"are not new code"* — a saved probe workflow to be promoted to a committed named quarterly workflow. **No workflow artifact is committed anywhere** (`.claude/workflows/` does not exist), so as of acceptance it **cannot** run against this slate. **08-08 action: record as SLIPPED with the reason**, or promote the workflow first. Slipping is acceptable (it blocks nothing) but must be **recorded, not invisible** — that is what the miss showed. Budget-capped ~728K tokens, quarterly by design; import Hermes's fail-closed cron semantics when promoted |
| **Q-EVALSEQ-1** | Advisor-avenue residue; pre-reg `25bd4d8` | Run the frozen K=4 bounded MC on the slate (or stamp blocked if inputs missing). Distinct from ORB k-policy and from Q-FUNDPOL-1. |
| **Q-FUNNEL-1 carry-in** | CLOSED-RESOLVED 2026-07-22 | Evidence input to **A0** (discharged). |
| **Q-COMPOSE-1 / fork exhaustion / ORB-ZB** | Closures 2026-07-17…21 | Record: breadth lever empty at priced supply; vise tightens A1. Unpark does **not** reopen compose. |
| **Book-composition economics** | [`2026-07-23-tradeify-book-composition.md`](2026-07-23-tradeify-book-composition.md) | Feed D4 plan numbers. Composition D1 SHIP path **still blocked** (rule-pin / Q-CAPALLOC-2 dependents) — not opened by ORB unpark. |
| **Q-CAPALLOC-2** | Operator queue #5; `RESOLVED-FRAGILE` | **Record only** at the gate — disposition is operator-owned, not a §2 step. |
| **Stage-8 variance-dominance ADR** | Accepted 2026-07-20 | Binds at compose attempts; no ORB compose on this slate. |
| **Monitoring maturity** | ADR `Accepted`; M1 open; **Addendum 31b `Accepted`** (operator-ratified 2026-07-31) | **Separate session** — not sequenced in §2. ⚠ **Corrected 2026-08-03 (Rule 14):** this row read `Proposed`, the same stale reading the 08-02 revision corrected at the §0 read. The correction landed at one reading site and not this one — repaired here on arrival per [`Rule 14`](../operational_rules.md). No status moved; the ADR was already `Accepted`. |
| **Substrate retirement + doc drift** | Phases 1–4 landed; 5–6 gated; living-board prune owed | **Separate session** — not sequenced in §2. |
| **Spend / promo** | §0.5 #7; Q-RAIL-1 §8 | Ceiling **$700**; promo **already applied** — no promo chase. |
| **Reconstruction-lane §4** | Self-funded-close ADR + unpark + [`re-park 2026-08-03`](../../adr/2026-08-03-orb-mnq-repark-payability-falsified.md) | Progress check; the ORB reopen **ran to a measured verdict and closed** — research progress, never deploy. Lane now has **no active candidate**: A CLOSED, B `PARKED` with its Tradeify target FALSIFIED. |
| **TVCOV MYM AMBIGUOUS** | INDEX | Accept analyst rec or defer — still owed. |
| **Radar own-falsifier** | STATE | Status note (0 new Stage-2 Tier-A since armed). |
| **Methodology 90-day** | Audit note | **CLOSED 2026-07-29** — record; do not re-run inside the gate. |

~~**Off-slate, nearer than the slate:** **B7-REFIRE Stage 1** desk card for **Tue 2026-08-04** (attended; M1 item 5 path). Do not fold into 08-08 prep.~~ **STRUCK 2026-08-06 (M30)** — mooted by ADR 2026-08-04 §6.

---

## §2 — Execution sequence at the gate (2026-08-08)

Order is load-bearing (Call-4 SEQUENCE FIRST; A1 reads A5):

1. **Call-4 beta-death count** — expect vacuous 0/4 (no live-authorized fills driving WATCH); **record the null**. Beta-cohesion diagnostic remains design-in-flight — do not fabricate it.
2. **A5 regime re-MC — REMOVED from the sequence (retired 2026-08-02).** Record the retirement; run nothing. The harness is unrunnable by construction now (inputs deleted), which is the honest state, not a defect.
3. **A1 accept-beta fork** — decide using Q-DECAY-1 + Q-PERSIST-1 + breadth-empty colour + **ORB-closed** colour (reopened as research 07-31, Tradeify target **FALSIFIED** 08-03; never a book-leg). **Step (2) no longer supplies an input** — do not wait on one, and do not invent one. Likewise do not wait on an ORB k-policy: there is none, and the breadth bench is empty rather than pending.
4. **A3 Call-1** — no-strategy-signal-fills ⇒ AMBIGUOUS per leg; re-confirm 11-08.
5. ~~**Q-EVALSEQ-1** — run the frozen K=4 bounded MC (or stamp blocked). Out of A0/A0b; does not touch live rung by itself.~~ **STRUCK 2026-08-06 (M30)** — DORMANT on the board (venue de-scoped; within-eval has no eval).
6. **A0 / A0b status** — **DISCHARGED** (pre-work): record fork-B ADR `Accepted`, 3.0% retained, live rung WATCH-1 0.50×. Out of the gate sequence as decisions; keep as records.
7. **Records pass** — discharges / supersessions (C7 withdrawal + 50K caveat; D2/C1 retirement; Q-FUNNEL→A0; **ORB reopened 07-31 → re-PARKED 08-03, Tradeify payability target FALSIFIED, T2 disposition discharged**; inventory=0; methodology CLOSED; promo/spend note; Q-CAPALLOC-2 disposition still operator-owned); C-class ratify-or-slip; falsifier statuses. **ORB needs no decision at this gate** — the RF&lt;1 adverse-input line is discharged with it.
8. **SESSIONS + STATE sync** — prune discharged forward-board lines **if** the deferred living-board session has not already done so; otherwise leave an explicit “drift session owed” line.

**Explicitly not in this sequence:** M1 `RESOLVED` / Addendum 31b ratification; substrate Phase 5–6; ORB rail integration / compose / new K; C1 `time_to_pass --regime-check`; Q-CAPALLOC-2 disposition; B7 arming.

---

## §3 — Dated pre-work (before the gate)

- **P0 — Bust-gate re-derivation — DISCHARGED 2026-07-23.** [`Q-BUSTGATE-1`](Q-BUSTGATE-1-bust-gate-re-derivation.md) + [pre-reg](pre-registration/Q-BUSTGATE-1-verdict-preregistration.md) (`98d0fa6`) + [closure](../closures/Q-BUSTGATE-1-closure-falsified.md). Fork-B ADR **`Accepted`** @ `9ab2e8b`. `3.0%` in the 2026-07-13 pre-reg **byte-unedited** (Trap #12 held). A0b NO-GO recorded.
- **P1 — fresh 4-leg Pepperstone TV export — STRUCK 2026-08-02. No export is owed.** Retired with the feed and with its only consumer (A5). Operator ruling: *"We do not need pepperstone exports, anything relying on pepperstone can be retired."* Both Pepperstone manifest dirs left the contract and the bytes were deleted after a verified offline copy — [ADR](../../adr/2026-08-02-pepperstone-feed-retirement.md) §2-E, [tombstone](../../ltm/notes/2026-08-02-pepperstone-data-tombstone.md).
- **P2 — evidence pre-assembly (CC, ≤1 hr, by 2026-08-06).** Class-A list + this revision’s rows + book-composition link sheet + ORB correct-clock scorecard pointer + Q-EVALSEQ-1 pre-reg path.
- **P3 — methodology 90-day review — DISCHARGED 2026-07-29.** Closed; may have added lesson rows already — not packet prep.
- **P4 — series ranks 1–3** — already closed (Q-RAIL-1 / Q-PYRPARITY-1 / Q-INVENTORY-1); feed as records, don’t re-litigate.
- **Deferred sessions (not P-items for 08-08):** M1 close + Addendum 31b ratification; substrate Phases 5–6; living-board / STATE prune of discharged lines; Q-CAPALLOC-2 disposition; Q-FUNDPOL-1 §8 pre-reg (event-gated, not calendar-gated).

---

## §4 — Completeness hypothesis (H-DELTA)

**H-DELTA:** §0.5 + §0.5b + §1 + §2 jointly cover every dated obligation on the `STATE.md` forward board that terminates at or before 2026-08-08 **except** items the operator explicitly deferred or queued elsewhere (M1 / Addendum 31b; substrate Phases 5–6 + living-board prune; Q-CAPALLOC-2 disposition; B7 Stage 1) and items already retired (C2→C0 / D2) or discharged off-slate (methodology 90-day).

**Falsifier (at the gate, before step 1):** walk STATE forward board; any ≤08-08 line with no row here and not in the deferred/retired/discharged-off-slate sets ⇒ H-DELTA falsified — add row, log miss, re-walk. Does not block the gate.

**Cheap falsifier already run for this revision (2026-08-01):** ORB unpark ADR `Accepted` + T1 PASS; monitoring ADR `Accepted` with Addendum 31b `Proposed`; substrate Phase 4 on `main` (`fc14682` / PR #572) and `ACTIVE_FIRM` absent from living `firm_rules.py`; methodology 90-day file present and CLOSED; A5 `NOT_EXECUTABLE` claim matches STATE panel-end **2026-06-02**; Q-EVALSEQ-1 pre-reg OPEN and 08-08-gated; fork-B ADR `Accepted`.

---

## §5 — Forbidden moves

- **Silently editing the 3.0% Part A ceiling** without a fresh Trap-#12-compliant brief.
- **Flipping c1 to 1.00× in GO ADR / lifecycle / rail constants** — A0b already NO-GO; a higher rung needs a fresh both-halves regime PASS + admitting path, not an 08-08 improvisation.
- **Treating the ORB reopen (or its 08-03 closure) as compose / rail / book-leg authorization**, or spending the MNQ Cap seat, or opening a new K-binding manifest from this slate. Equally forbidden in the other direction: **reading the 08-03 FALSIFIED as a mechanism rejection** or as licence to re-scope ORB to whichever firm survives — the falsification is one target at one firm, and another venue needs a fresh GO plus a survivor-scoring pass *before* unpark.
- **Inventing an A5 p99 / bust number** when P1 is missing (`NOT_EXECUTABLE` is the honest stamp).
- **Running retired C1** (`time_to_pass --regime-check`) as if it were still a quarterly obligation.
- **Folding M1 close, Addendum 31b ratification, or substrate Phase 5–6 into the 08-08 gate session.**
- **Re-opening JULY promo urgency** — promo already applied; ceiling remains $700.
- **Adjudicating A1/A5/Q-CAPALLOC-2 while writing this delta** — operator accepts rows; gate (or operator queue) decides.
- **Conflating A5 with retired C1.**
- **Re-running the closed 2026-07-29 methodology review inside 08-08 prep.**
- **Citing pre-withdrawal prop §4 Part A figures (2.65%/2.64%) as current.**

---

## §6 — Gate criteria (assembly)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` (packet ready) | Operator accepts §0.5b + §1 rows; **A5 + P1 recorded as RETIRED** (2026-08-02 feed retirement — the old *"P1 discharged or A5 stamped `NOT_EXECUTABLE`"* clause is **void**: neither is available, both are struck); H-DELTA walk **run** and clean-after-repair | Run §2 |
| `FALSIFIED` (slate incomplete) | H-DELTA miss | Add row(s), re-walk, proceed |
| `AMBIGUOUS-HOLD` | Operator rejects ≥1 non-OPERATOR / non-VERIFIED delta row | Parent pretriage classification stands for that row |

---

## §7 — What this brief does NOT do

No finding adjudicated beyond recording accepted ADRs/closures that supersede the 2026-07-23 posture. No live sizing, rail arm, ORB compose/rail, M1 signoff, substrate deletion, or Q-CAPALLOC-2 disposition. No in-place edit of the survivor-scoring pre-registration numbers. No living-board prune of `STATE.md` (separate session).

---

## §10 — Audit hooks

```bash
# This file still points at the ratified parent
rg -n "2026-07-12-08-08-packet-pretriage" docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md

# Historical posture preserved AND both live supersessions present (unpark 07-31 -> re-park 08-03).
# The full arc must be readable: a reader must not land on the unpark without the re-park.
rg -n "OPERATOR 2026-07-23|ORB-MNQ remains PARKED|UNPARKED 2026-07-31|re-PARKED 2026-08-03|VERIFIED 2026-08-03" \
  docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md
# Expected: 07-23 historical row + the 07-31 unpark + the 08-03 re-park/FALSIFIED rows all present

# D2 retirement is cited; C1 not sequenced as standing
rg -n "RETIRED|time_to_pass" docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md

# A5 honesty + Q-EVALSEQ on the slate
rg -n "NOT_EXECUTABLE|Q-EVALSEQ-1" docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md

# Owner ADRs still Accepted / Proposed as claimed
rg -n '^\*\*Status:' \
  docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md \
  docs/adr/2026-07-23-c1-rung-selection-ev-objective.md \
  docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md

# A5 harness present; C1 harness may exist but must not be treated as owed
ls lab/analysis/regime/decompound_remc_2026-06-07/regime_gate.py lab/discovery/lifecycle_call1/harness.py

# Companion brief + Q-FUNNEL evidence + Q-EVALSEQ pre-reg
ls docs/briefs/programs/2026-07-23-tradeify-book-composition.md \
   docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md \
   docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md

# Trap #12 still intact on the frozen pre-reg
rg -n "3\.0%|Trap #12" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md

# ACTIVE_FIRM gone from living firm_rules (Phase 4)
rg -n '^ACTIVE_FIRM\s*=' core/firm_rules.py || echo "ACTIVE_FIRM selector absent (expected)"
```

---

## Verification

```bash
python3 scripts/check_brief.py docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md --type generic
git log -1 --format='%h %cs' -- docs/briefs/programs/2026-07-12-08-08-packet-pretriage.md
```

## §11 — Operator acceptance (DRAFTED 2026-08-02 — awaiting signature)

Per §6, acceptance flips this packet from `DRAFT` to `RESOLVED (packet ready)` and licenses running
§2. This section is the draft; **the sign block below is unsigned and the Status line still reads
`DRAFT`** — only the operator moves it.

### 11-A — The H-DELTA walk was RUN, not asserted — and it FALSIFIED once

> **SUPERSEDED — do not read as discharged (2026-08-06 / M30).** The 2026-08-02 walk (`walk RUN`)
> predates the de-scope / queue reset; re-run the §4 walk at the gate.

The §4 falsifier requires walking the STATE forward board for every ≤08-08 line and confirming a
packet row. **Executed 2026-08-02.** Result: **`FALSIFIED` on exactly one miss**, repaired in place
per §6's own disposition (*"Add row(s), re-walk, proceed"*).

| Forward-board line | Packet row | Walk result |
|---|---|---|
| Advisor-avenue residue (dispositions at 08-08) | Q-EVALSEQ-1 | covered |
| Decompound §4 limb-2 | A5 (**RETIRED**) | covered |
| Per-strategy decay review (Call 1) | A3 | covered |
| Beta-death review (Call 4) | §2 step 1 | covered |
| 08-08 accept-beta fork | A1 (**re-scoped**) | covered |
| Notice N-2026-07-11 re-check | N-2026-07-11 | covered |
| Multiplier-spine forward-relevance flag | B3 | covered |
| Prop-portfolio §4 falsifier | C7 | covered |
| Harvest-intake §4 + idle guard | C4 | covered |
| Mechanism-sourcing radar | Radar own-falsifier | covered |
| Survivor-scoring pre-registration | Trap-#12 rows | covered |
| **Sentinel Tier-2/3 promotion (limb B1)** | **— none —** | ⚠ **MISS ⇒ H-DELTA FALSIFIED** |

**Row added; re-walk clean.** The miss was real: the item reads *"do before the next quarterly
slate"* and its done-condition is *"has run once against the 08-08 slate"*, so it is a ≤08-08 line.
It had no row because it was re-homed from the Hermes closure on 2026-07-27, **after** this packet's
prior revision.

**Checked and correctly ABSENT (not a miss):** *Per-fill add-slippage capture at B7* — gated on the
first armed session (RUNBOOK §B7 Stage 2b) with a blocking prerequisite (the reference price is not
persisted to the ledger). **B7-gated, not date-gated**, so it is not a ≤08-08 forward-board line.

### 11-B — Material changes since the last revision (read before signing)

1. **A5 and P1 are RETIRED, not deferred** — the Pepperstone feed was retired 2026-08-02 in both
   tiers. §6's old RESOLVED trigger (*"P1 discharged or A5 stamped NOT_EXECUTABLE"*) is **void** and
   has been rewritten; neither branch is reachable.
2. **A1 is re-scoped, not decided.** *"Decide after A5"* has no referent. Deciding it on an invented
   A5-substitute is a named forbidden move in the retiring ADR.
3. **§2 is materially shorter.** Call-4 → A5 → A1 was the only load-bearing internal sequence. What
   remains is one real decision (A1), one bounded MC (Q-EVALSEQ-1), and records.
4. **Two new record-only rows** — the c1 cadence / idle-rule disposition (partly ruled 2026-08-02)
   and the segregation §4 revert check.
5. ⚠ **The segregation §4 check is due 08-08 and its arithmetic crosses its trigger** —
   27.04% ≥ 25% on the one-account reading. It reads `FALSIFIED`; the author's judgment is
   `FALSIFIED (degenerate at N=1)` with no re-opening action, which is **operator-owned** and is not
   accepted by signing this packet.
6. **The decompound HOLD currently has no live falsifier** (§4 limb-2 orphaned). Successor design
   landed; build gated on the first live fill.

### 11-C — What acceptance does and does not do

**Does:** accept the §0.5b + §1 delta rows as the slate of record, and license running §2.

**Does NOT:** decide A1; adjudicate the segregation §4 stamp; take the idle-rule disposition; arm
the rail; move any gate, pin, allocation, lifecycle rung or threshold; ratify the L1 limb's force
level (already `Accepted` on its own ADR); or accept the author's delegated judgments — each of
those is a separate call. Per §6, rejecting any non-`OPERATOR`/non-`VERIFIED` row yields
`AMBIGUOUS-HOLD` for that row and the parent pretriage classification stands for it.

### 11-D — Sign block

> **NOT SIGNED — packet superseded before signature; do not backdate a signature now.** See
> Addendum 2026-08-29 in Change history: the operative path for any residual line item here is no
> longer this section.

```
ACCEPTANCE:      08-08 packet delta rows (§0.5b + §1) accepted as the slate of
                 record. H-DELTA walk run 2026-08-02: FALSIFIED on one miss
                 (Sentinel limb B1), row added, re-walk clean. A5 + P1 recorded
                 RETIRED. Licenses running §2 — decides nothing in it.
STATUS ON SIGN:  DRAFT -> RESOLVED (packet ready)
DATE / INITIALS: ____-__-__ / __
```

---

## Change history

| Date | Change |
|---|---|
| 2026-07-17 | Initial delta (ranks 1–3 series; WATCH-1 / Q-COMPOSE carry-ins). |
| 2026-07-23 | Operator posture §0.5 (bust-gate re-derive; 1.00× aim; ORB PARKED; monitoring/substrate deferred; promo applied / $700). D2/C1 retirement folded. Sequence + pre-work rewritten. |
| 2026-08-01 | §0.5b live supersessions: ORB **UNPARKED** (research/payability; no rail/compose); monitoring ADR `Accepted` / M1 open / Addendum 31b `Proposed`; substrate Phases 1–4 landed; A5 `NOT_EXECUTABLE` without P1; Q-EVALSEQ-1 on slate; methodology CLOSED; C7 §4 withdrawal recorded; fork-B ADR `Accepted` throughout. Forbidden moves + audit hooks updated. No new operator directives invented. |
| 2026-08-03 | ORB §4 **T2 RULED FIRED** (operator, Part A bust reading) — ORB-MNQ-1 re-**PARKED**, payable-Tradeify-leg target **FALSIFIED**, T2 disposition **discharged**, ORB **off the slate as a must-decide** (T3 moot). Seven rows synced: §0 read, §1 row 6, both new/revised-rows entries, reconstruction-lane §4, A1 inputs + sequence step 3, records pass. Forbidden moves gained the **reverse** guard (do not read FALSIFIED as a mechanism rejection or as licence to venue-shop); the "ORB not left as PARKED-only" audit hook is **inverted** to assert the full unpark→re-park arc. Packet stays `DRAFT (operator review owed)`; no other slate row moved, no directive invented. |
| 2026-08-29 | **Addendum (Rule 14 correction — no §0–§10 body text or 2026-08-06 banner edited).** (1) **The 2026-08-08 event that actually ran was the quarterly programme audit / Great Prune** — a disjoint 47 ADR-trigger-rider sweep ([`Great Prune ADR`](../../adr/2026-08-08-great-prune.md); [`quarterly audit note`](../../notes/audits/programme-audit/2026-08-08-quarterly-audit.md)) — **not** this packet's own §2/§11 gate walk, which was **never executed**. The 2026-08-06 banner already flags this packet as pre-de-scope-stale; it does not say what actually happened on 2026-08-08 instead, which is the gap this addendum closes. (2) **§2 step 5 / Q-EVALSEQ-1 was subsequently un-dormed and closed independently, `FALSIFIED` 2026-08-16** — see [`2026-08-16-state-policy-scoring-review.md`](2026-08-16-state-policy-scoring-review.md) and [`closures/Q-EVALSEQ-1-closure-falsified.md`](../closures/Q-EVALSEQ-1-closure-falsified.md). That closure ran through its own frozen pre-registration, not through this packet's §2/§6/§11 gate. (3) **A1 (accept-beta fork) has no ratified disposition anywhere in the corpus as of 2026-08-29 and remains genuinely open** — [`docs/adr/2026-08-02-pepperstone-feed-retirement.md`](../../adr/2026-08-02-pepperstone-feed-retirement.md) §2-C re-scoped it (removed the dead A5 input) without deciding it, exactly as this packet's own §1 row and §11-B item 2 already record; no later artifact adjudicates it. But **this packet's own §11 sign-off is no longer the operative path to close it** — §6's `RESOLVED` route licenses running §2, which itself never ran, and §11-C already disclaims that acceptance "does NOT decide A1." A1 needs its own fresh decision artifact, not a signature on this one. (4) **Sentinel Tier-2/3 promotion (limb B1) is unaffected** by any of the above — its 2026-08-02 disposition (§11-A: "record as SLIPPED with the reason, or promote the workflow first," due before the next quarterly slate) stands on its own and does not depend on this packet's §11 signing. **This addendum decides nothing, arms nothing, and moves no gate/pin/allocation/lifecycle rung** — it records what superseded the packet and where each residual line item's live path now runs. |
