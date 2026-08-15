# 06 — Operator judgement, unadjudicated, and untested

**What this section is.** The three places the claim-alignment audit **deliberately declines to
decide**. Everything in `01`–`05` carries a verdict and a mechanical action; nothing here does.
Ported from round 1 §5.8 (flagged for operator judgement, 10), §5.9 (confirmed but unadjudicated, 2)
and §5.10 (completeness-critic candidates, 22), then reconciled against round 2 and against the four
fixes that landed after the round-1 artifact was written.

**Rows: 34** — 10 tier-1 (1 now **CLOSED** by operator ruling, 9 open) · 2 tier-2 · 22 tier-3
candidates (**18 superseded** by round 2 or already promoted in round 1; **4 residual limbs** survive,
one of them a whole candidate — see §5).
**Evidential standing: three tiers, deliberately not merged.** Tier 1 is verified fact with an
unmade decision. Tier 2 is verified fact with no Algorithm verdict. Tier 3 never passed a refutation
pass at all. Collapsing them would be the single most damaging edit anyone could make to this file.

**Combined-round context and the honesty item both live in** [`README.md`](README.md) — including
why round-2 findings carry slightly lower evidential standing than round-1's. Not restated here.

---

## §0 — How to read this file

| Tier | Section | What is true of every row | What is NOT true |
|---|---|---|---|
| **1** | §2 | The observation was **verified at HEAD** and survived the adversarial refutation pass. | The remedy is settled. Each row's disposition reopens a decided question, spends money, moves an obligation between owners, or elects between two defensible conventions. |
| **2** | §3 | The finding was **confirmed** (each carries an executed direction check and a narrowed `PARTIAL` verdict). | An Algorithm verdict exists. The pass returned none for these two, so **this audit proposes none.** No verdict is invented to square a count. |
| **3** | §4 | The item was surfaced by a **completeness critic**. | It is a finding. These never faced the refutation pass that killed 41 of 192 round-1 raises and narrowed 53.6% of survivors. Round 2 has since swept most of the surfaces they sit on — where it did, **the round-2 row supersedes and carries higher standing.** |

**Three column shapes, three reasons.** Tier 1 has **no Verdict column** — issuing one is the thing
it declines to do. Tier 2 is prose, because each item's whole content is *what refutation narrowed*.
Tier 3 has a **Round-2 disposition** column instead of a Verdict column, because supersession by a
refutation-tested finding is the only adjudication these rows have received.

---

## §1 — RESOLVED since the round-1 artifact — FU-1, the token-trade ruling

**This was an operator-judgement item. It has been ruled. It is recorded here as closed, not as
open, and it is the only row in this file with a disposition.**

| Field | Value |
|---|---|
| **Round-1 identity** | §5.8 **O-C** — the `inactivity_max_idle_days: 5` exposure; first uncovered Mon–Fri week closing **2026-08-07**, one day before fork F2 is due (2026-08-08). Enforcement is a warning email then **irreversible deletion** (art. 12268494 — no pause facility, no reactivation, non-refundable). |
| **What round 1 said** | *"The only preserving action is a token trade — a real-money order on a de-scoped account — which is an operator GO and a §5-forbidden-move question, not an audit remedy."* The audit recorded the date, the mechanism and the irreversibility, and **declined the action**. |
| **Ruling** | Commit `551d5c5`, 2026-08-05. Operator, in session, verbatim: *"We will not let the venue lapse. If no strategy has been found by Friday we will submit a token trade."* |
| **Landing sites** | `docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md` — a new **append-only** `✅ RULED 2026-08-05` block; the pre-existing *"The bind, stated precisely and NOT adjudicated here"* section is **left unedited**, because it is the correct statement of the bind as of its date and this is the adjudication it said was owed. Plus `STATE.md` **row 0**. |

**The ruling's own scope limits — reproduced because they are the load-bearing half:**

1. **Primary path is a deployed strategy.** If a Tradeify-shaped candidate is found and deployed
   before Friday, its own fill covers the week and no token trade occurs.
2. **Fallback is ONE manual token trade, operator-submitted, by 2026-08-07.** One trade, one named
   week. **Not a standing licence.**
3. **It deliberately crosses a standing forbidden move** — the book-composition brief §5 item 5
   admits only *"rail-level answer or accept warnings"*; this is the third option it excluded.
   Recorded as a **reasoned operator override, not a silent boundary erosion** (programme-audit
   degeneration signal #7). The reasoning on the record: the forbidden move exists to keep
   discretionary execution out of a *strategy* path, and a compliance token trade carries **no
   signal, no edge claim and no sizing decision**.
4. **The rail is not the instrument and does not move.** `dry_run` stays `true`; M1 stays unresolved;
   no arming, no GO, no deviation. ⚠ **Operator-placed at the venue. No agent may place it.**
5. **Not a resumption of manual trading** (ADR `2026-06-30` stands) and **not a venue re-scope**
   (ADR `2026-08-04` stands — Tradeify remains de-scoped as a deployment target).
6. **Cost recorded, not minimised:** ~$1.82 RT plus a tick of risk, and the §5 forbidden move's
   deterrent value spent once. What it buys is that **F2 is decided on its merits rather than by a
   deletion timer**.

⚠ **What the ruling did NOT close, stated so it is not read as closed.** The idle rule recurs
**every** Mon–Fri week (26.3% of weeks historically zero-trade, worst run 4 consecutive), and R8 —
the scheduled-maintenance instrument that would answer it durably — remains **undelivered**. Row 0
buys one week; the recurring question is F2's. `STATE.md` row 1 now carries that clause explicitly.
Round 1's warning still holds verbatim: **retiring the disposition spec must not be read as retiring
the exposure.**

---

## §2 — Tier 1: verified, but the disposition is a governance choice (9 open)

**Each row is a verified observation with an unmade decision attached.** They are separated from the
adjudicated sections for one reason: the remedy is a **governance choice**. An audit that rules on
these is doing programme management under an audit's authority, which is the layer contamination the
diagnostics test for. **Each row states the observation, states the choice, and stops.** No row
carries a verdict, including where the audit records what it would *not* do.

Two rows (**O-E**, **O-F**) are the `KEEP-AS-IS` adjudications the round-1 count includes —
`KEEP-AS-IS` means *no edit owed, recorded as deliberate restraint*, logged here so the claim is not
re-raised at the next sweep. The rest are the explicit operator-flags raised inside the MISLEADING
sections, collected so a remediation pass reading only Action cells cannot lose them.

**All nine re-verified present at HEAD on 2026-08-05**, after `d84c5e4` / `a818b3f` / `ae5ffe7` /
`551d5c5`. None of the four fixes touched any of them.

| # | File · anchor | Observation (verified at HEAD) | The choice — operator's, not this audit's |
|---|---|---|---|
| **O-A** | `docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md` F1, L68 (see **M38** in [`04-misleading.md`](04-misleading.md)) | **The canonical row of this section.** F1's factual premise — *"On the days the incumbent leg can fire — **Tuesday and Friday**"* — is dead (verified present at L68). Its *rule* is stated conditionally on its own face (*"on an **occupied** instrument"*; *"calendar-disjointness from **the incumbent** on that symbol"*) and survives, as does lesson L2. But the **S7 symbol-occupancy screen descends from F1**, and S7's output is what adjudicated `ORB-MNQ-1` **SCREEN-DEAD** on the cadence axis 2026-08-04 — a ruling **M39** relies on when it forbids re-nomination. | Whether correcting F1's premise reopens S7, and whether reopening S7 reopens ORB-MNQ's cadence role. **This audit corrects the premise (M38) and does not touch the screen.** Two facts bound the decision without making it: ORB-MNQ's *payability* target is independently **FALSIFIED** (ADR 2026-08-03, §4 T2 FIRED, intraday-honest bust ≥ 67.67%), so a cadence-role reopening would not revive it; and any unpark at a non-Tradeify venue needs a fresh GO **plus** a survivor-scoring pass first. **Do not silently reopen. Correcting a closure must not be executed as a re-nomination.** |
| **O-B** | `STATE.md` decision index — *"already fully consumed by the live 2-leg book … zero headroom … at any size"* (second of two findings on this sentence; see **M5**) | M5 corrects the *ground* — the cap is allocated in full by `LEG_MAP`, untouched by the de-scope. The second finding asserts the **corollary**: that withdrawal *releases* the 69/11 allocation and `MYM1!`/`MNQ1!` occupancy, so third-leg headroom now exists. This is the single most common over-reach in the round-1 sweep (refutation ground 5); `ops/instruments/MYM.md`'s dated 2026-08-04 ruling **expressly withholds release pending F2**. | **Release or retain — decided at fork F2 (2026-08-08), not by an audit.** Until F2 rules, every derived surface must read **retained-not-released**; C31, M5, M22's Y4 clause and M39's C5 note are written that way for exactly that reason. Operational consequence if the audit is followed: **apply one superseded-marker on this sentence, not two** — the two findings share a quote and separate markers would encode the unmade decision by accident. |
| **O-D** | `docs/adr/2026-08-03-lifecycle-ladder-intermediate-rung.md` L3–L6 (see **M12**, which states *"Operator ruling required"*) | Verified at HEAD: `**Status:** `Proposed``, `Supersedes: none`, `Superseded-by: none` — never in force, and **still carrying no withdrawal edge**. ADR 2026-08-04 §6 records **by name** that it *"loses its driver"* — a consequence written down and never propagated. M12 specifies the mechanics: **`Withdrawn-by:`, not `Superseded-by`** — nothing was in force to replace, and the 08-02 ADR is the precedent. The §7 Phase-4 GO *was* given, and its FROZEN spec recommends holding at `Proposed`; that spec's measurement retains independent value. | **Withdrawing an ADR is an operator ruling.** Two things to know before making it: (1) `scripts/retire_adr.py` emits a **false `Superseded-by` edge on `--reason withdrawn`** and is unrepaired, so a withdrawal executed today must be hand-verified against `docs/adr/INDEX.md`; (2) the alternative — hold at `Proposed` until F3 elects a venue — is not obviously worse, since the ladder-granularity question survives as methodology either way. The audit prepares both paths and elects neither. |
| **O-E** | `docs/briefs/closures/Q-COSTGEO-3-closure-ambiguous-needs-depth.md` §8e — *"it now has a fill source"* | **Adjudicated `KEEP-AS-IS`.** The clause is false post-08-04, but it sits in a dated addendum on a frozen body; its forward pointer already resolves to the `STATE.md` 2026-08-04 correction; and the closure's recommendation is venue-independent and unaffected. Recorded verbatim so a future sweep does not re-raise it: *"Q-COSTGEO-3 §8e — KEEP-AS-IS 2026-08-05: dated addendum, frozen body, forward pointer resolves, recommendation unaffected and venue-independent."* | **No edit owed; the audit's answer is to do nothing.** If the operator wants belt-and-braces regardless, the **maximum warranted** is a twelve-word inline strike — `~~it now has a fill source~~ (2026-08-04: gone — see STATE.md)` — and explicitly **not** a banner paragraph. Whether even that is worth the byte is a real call: the meta layer's first Degenerating limb is machinery accumulating faster than it is verified, and banner accretion is the doc-layer form of the same thing. |
| **O-F** | `docs/operational_rules.md` Rule 7 owner table (`KEEP-AS-IS` on the quoted `CLAUDE.md` role note) | **Adjudicated `KEEP-AS-IS` on the quoted note — no edit owed there.** The separate verified observation is the audit's own subject: Rule 7's owner table has **no row for current deployment state**. (The table's dead `core/config/params.toml` row is still present at L170 — that one is **C14**'s, not this row's.) The candidate row names a three-part owner: the owning ADR, plus `ops/instruments/<SYMBOL>.md`'s Status block, plus `LEG_MAP` in `ops/c1_rail/c1_sizing_host_reference.py`. | Whether to name a **split owner** for a fact that has no single home. A three-part owner is a materially weaker guarantee than Rule 7's other rows, and may be worse than an honest blank that forces the reader to the ADR. If the row is added: **do not author a separate rule, a separate register, or a row-only commit** — it lands inside the Rule 6/11 commit (**C11**), alongside the dead `params.toml` row deletion (**C14**). The audit declines to elect. |
| **O-G** | `core/firm_rules.py:412` — BluSky `"cost_per_side_usd": 0.95` (see **M40**) | Verified present at HEAD. BluSky publishes **$0.50/side** micros at Evaluation on Rithmic / Volumetrica / Tradesea and **no figure at all** for funded; the encoded `0.95` is an **NT-schedule proxy** (the file's own comment block says so), and `lab/discovery/cost_model.py::resolve_commission` returns it silently. Live consumer three days out: **F3's EV/$ ranking (2026-08-08)**, with BluSky the only sourced survivor on the cadence axis. M40 lands the comment-layer flag only. **Status change since round 1:** `STATE.md` row 3 now registers this pair *"flagged for operator-directed correction, not applied"* — **registered is not ruled.** | Correcting the encoded value is a **firm-rules change requiring an ADR plus the engine pre-flight** (`CLAUDE.md` §Firm Expansion; precedent 2026-08-05 → 2026-08-05b). Two sub-choices, neither the audit's: whether to open that ADR **before** 08-08, and whether an F3 ranking may run on a proxy basis in the meantime. What the audit does assert, and M40 encodes: the proxy **must not be treated as venue-published in any F3 ranking** while it stands. |
| **O-H** | `core/firm_rules.py` — BluSky `micro_contract_cap` phase scope (see **C12**(b)) | Verified and commented, **not re-encoded**: the field carries the **Evaluation/Buffer** cap while the Sim Funded / Live stage is roughly **half** (Propel Premium $100K = 5 mini / 50 micro; Orbit funded 3/30). Any funded-capacity or composition-fit analysis reading this field is **overstated ~2×**. Same status change as O-G: now on `STATE.md` row 3, still unruled. | Onboarding funded-phase BluSky rows is **firm-rules onboarding** — ADR plus engine pre-flight, plus a re-MC where the run consumes those rows as the simulation target. The sequencing is the choice: land them **before** 08-08 so the F3 ranking runs on funded geometry, or **after**, so 08-08 runs on eval geometry with the ~2× caveat stated on its face. Both are defensible; the audit states the overstatement and does not schedule the work. |
| **O-I** | `docs/adr/2026-07-03-hardcore-p4-tail-survival-gate.md` L11 / §5 (see **M27**) | Verified at HEAD, L11 verbatim: *"P4's kill process is already running (decompound HOLD → 2026-08-08)."* That HOLD's own §4 banner reads *"NEITHER LIMB CAN FIRE TODAY … this HOLD currently has no live falsifier"*, and its quarterly schedule was **struck** 2026-08-03, not deferred. P4's §5 forbidden-move 4 bars it from forking a second process. **So P4 has no disposition process at all**, and the 2026-08-08 quarterly will supply no P4 verdict. ⚠ Coupling: **G21** describes the identical hole from the monitor-spec end — the spec that would discharge the HOLD's limb-2 falsifier is itself gated on a fill that never happens. | M27's action is to record it at 08-08 as **standing-unfalsifiable with a board row** rather than roll it forward silently. What the audit does **not** decide: whether to relieve forbidden-move 4 so P4 may fork its own process; whether to re-arm the struck quarterly; and whether a **hard-core** integrity gate may stand unfalsifiable indefinitely. That last is a hard-core ruling and belongs to the operator at 08-08 — it is also the object layer's third named watch condition, so **deferring it silently is the specific act that converts the object verdict at the next audit**. |
| **O-J** | `lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md` — the retracted `z = −2.90` (see **M11**) | M11 supplies the reader-intercept. The residual observation is mechanical: the retraction lives in `docs/rejected_candidates.md` — a **different file** — so `check_supersession_placement.py` has no addendum-confined token to trigger on and **can never catch this shape.** **C16** widens the glob and documents the early-return hole; neither fix reaches cross-file retractions. | Whether to build a **retraction registry** — a `must-not-re-quote` token list any gate can grep — or to accept the class as a human obligation under Rules 11/14. The audit reports the gap and **builds nothing**, because the counter-argument is the meta-layer verdict itself: the belt is net **+9 at 4 : 1**, the first Degenerating limb is *"machinery is added faster than it is verified"*, and a ninth gate authored inside the audit that found the eighth unbinding is not obviously the right answer. |

**One structural note the operator may want at 08-08.** The new proposed ADR
[`docs/adr/2026-08-05-strategy-venue-binding-axis.md`](../../../../adr/2026-08-05-strategy-venue-binding-axis.md)
(commit `0af62ec`, `Proposed`) gives venue facts an owning level (BOOK → VENUE EDITION →
DEPLOYMENT). **It does not decide any row above** — but it changes the shape of three of them:
**O-B** (whether cap/occupancy release is a deployment-layer or book-layer fact), **O-F** (whether a
three-part owner is a workaround or the correct decomposition), and **O-D** (whether a lifecycle-rung
ADR is even the right layer for a rung whose driver was a venue). If that ADR is ratified, revisit
these three **before** electing on them individually; if it is not, they stand exactly as written.

---

## §3 — Tier 2: confirmed but unadjudicated (2)

The round-1 method table records **138** Algorithm adjudications against **140** confirmed findings.
The two below are the difference. Both survived the adversarial refutation pass — each carries an
executed direction check and a narrowed `PARTIAL` verdict — but **the Algorithm pass returned no
Question → Delete → Simplify → Accelerate verdict for either, so this audit proposes none.** They are
reported at the standing they actually have: verified observations, each with a corrected statement
drafted by the refutation pass and **no disposition attached.** Inventing verdicts to square the
count to 140 would be exactly the retrofit Trap #1 forbids, which is why the count reads 138.

Both are rated **COSMETIC**, which is how the 62 adjudicated COSMETIC findings and these 2 reconcile
exactly to round 1's total of **64**.

**Both re-verified still standing at HEAD 2026-08-05, after all four fixes.**

### U1 — `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` L910, §10 hook 2 baseline

**Claim as filed, verbatim (present at L910 at HEAD):**

```
# Expected 2026-07-31, executed: **5** hits for `DRY_RUN=false` and `"status": "CODE_LANDED"`
# at line 3. Falsifier fires if a NEW dated arming entry pushes that count above 5 while
# status is still CODE_LANDED.
```

**What is verified — re-executed 2026-08-05.** `grep -c "DRY_RUN=false" docs/notes/rail_build/RUNBOOK.md`
returns **4** against a recorded baseline of **5**. The baseline is the stale figure, and the drift is
in the **fail-open** direction: a third armed session would take the count to exactly 5 and *not
exceed it*, so the hook would stay silent on the event it exists to catch. The cause is dated — the
RUNBOOK was edited 2026-08-02 by `cd8b617` / `3b838b4` / `6640141`.

**What refutation narrowed.** The ADR's **operative** falsifier is stated count-free thirty lines
above, at L873–875 (*"a new entry in the RUNBOOK §B7 arming log dated after this addendum whose text
records `DRY_RUN=false`, while `M1_MONITORING_ACCEPTANCE.json` still carries `"status":
"CODE_LANDED"`"*), and **that formulation still binds exactly as written.** Only the §10 convenience
baseline drifted. The same hook block **self-warns two hooks earlier** that *"Count-based hooks fail
open"* (L895) and rebuilt hook 1 specifically to avoid this shape. Add that the subject is now doubly
blocked — by the PR #601 arm interlock and by the de-scope — and COSMETIC is the honest rating.

**The refutation pass's drafted corrected statement, recorded but NOT adopted:** re-measure the
baseline at each check rather than trusting the recorded number; state the 2026-08-05 reading
(**4**, was 5 at 2026-07-31, with the three causing commits named); re-word the trigger as *"above
the CURRENT baseline"* per hook 1's own warning. **This audit issues no verdict on whether to make
that edit.**

### U2 — `docs/spec/c1_watch_realization_multiplier_layer.md` — §0 anchors and their consequences

**Claim as filed, verbatim (present at L13 at HEAD):**

```
- `ops/accounts.py:166-187` (**deleted 2026-07-24** — deliberately not a link) — anchor `8c461bc` (2026-07-11).
  `calc_multiplier = (balance × tier_risk) / (200,000 × BASELINE_RISK)`,
  **`math.floor(x*100)/100` — round down, never up**.
  This is the account-multiplier layer's existing arithmetic doctrine.
```

**What is verified.** `ls ops/` returns `c1_rail cli.py data instruments prop_envelope_default.md
recall sentinel` — `ops/accounts.py` is gone, deleted 2026-07-24 with the continuous-lot spine.

**What refutation narrowed, and it narrowed hard.** The cited line sits inside
`## §0 — Rule 0 reads (production-source verification, all 2026-07-17)` — a **dated provenance record
of what was read at authoring time**, precisely the artifact class this repo freezes rather than edits
(the same shape as every other §0 block). **A §0 anchor naming a since-deleted file is correct
history, not a stale claim.** What genuinely survives is smaller, and is on two *other* lines of the
same file:

* **(a) L3, the Status line** still defers the §6 downstream sweep *"until the in-flight Cursor
  Q-RAIL-1 session lands"* — that session closed `RESOLVED` 2026-07-17 (`STATE.md` L129) and the rail
  was built and dry-fired 07-17 → 07-20, so the deferral reads as pending when it is not. **Verified
  verbatim at HEAD.**
* **(b) the Verification block** runs `git log -1 --format="%h %ci" -- ops/accounts.py
  core/dd_protection.py core/lifecycle.py`, which exits non-zero. ⚠ **Line drift since round 1: this
  is now L163, not L147** — the B3 fix (`d84c5e4`) added lines above it. Anchor by content, not by
  number.

**File-level coupling — status changed since round 1, and the change matters.** Round 1 recorded that
**B3** carried this file at BLOCKER for its `cap_firm` §2 defect and warned that B3's action *"must
not be quietly widened"* to cover U2. **B3 is now FIXED** (`d84c5e4`), and it was **not** widened —
the commit touched §2, the HALT property, the constants gloss and the worked check, and left L3 and
L163 exactly as they were. The restraint held. **U2 therefore still stands, unadjudicated, and now
has no piggyback opportunity attached to it** — anyone acting on it opens the file for U2 alone.

**The refutation pass's drafted corrected statement, recorded but NOT adopted:** leave the §0 read as
filed; change the Status line's deferral to a discharge; note that the round-down doctrine's prior
home was deleted 2026-07-24 and that the surviving realization is the sizing host's integer-quantity
floor at `ops/c1_rail/c1_sizing_host_reference.py`; drop `ops/accounts.py` from the Verification
`git log` line. **No verdict is issued on any of it.**

---

## §4 — Tier 3: completeness-critic candidates (22) — refutation-UNTESTED, mostly superseded

**⚠ Standing of evidence — read this before any row.** The 22 items below were surfaced by round 1's
**completeness critic**, not by its 12 parallel domains, and they **did not pass the adversarial
refutation pass that killed 41 of 192 raised findings (21.4%) and narrowed 53.6% of the survivors.**
**They are candidates, not findings.** No severity label in the `Rated (untested)` column is
comparable to a graded label elsewhere in this audit: in particular the **nine rated BLOCKER here
were NOT added to round 1's three**, which counts refutation-survived findings only. Anyone quoting a
combined BLOCKER count is quoting a number this audit did not produce.

**What round 2 changed, and it changed most of this section.** Round 1 recorded that `.claude/`,
`.cursor/`, `deploy/`, `PIPELINES.md`, `README.md`, `scripts/` and the two spec files *"were swept by
no domain"* — the single largest coverage hole. **Round 2 swept exactly those seven surfaces**, and
its 124 raises → 110 confirmed went through a refutation pass these candidates never had.
**Where a round-2 confirmed finding covers a candidate below, the round-2 row supersedes it and
carries the higher standing** — remediate there, not here. This section is retained so the critic's
coverage stays auditable and so the residue is visible, not so it is worked twice.

**The concentration, restated because it was the critic's most important claim and round 2 bore it
out.** Eight of the 22 sit under `.claude/skills/`, **six on `c1-rail/SKILL.md` alone**. That is the
one surface which **loads automatically on trigger words, ahead of any document a human chooses to
read** — and the trigger words here are exactly `Tradeify`, `c1`, `arming` and `dry_run`. Round 2
returned **71 agent-facing findings, 23 of them in `.claude`**, which is independent corroboration of
the critic's direction from a pass that did face refutation.

**The column shape differs deliberately** — there is no Verdict column, because none was adjudicated.
`Round-2 disposition` is the only adjudication these rows have received, and it is second-hand.

### 4.1 `.claude/skills/c1-rail/SKILL.md` — 6 candidates

**Consolidated disposition: SUPERSEDED — work this file from** [`03-agent-facing.md`](03-agent-facing.md)**, not from here.** Round 2 swept `.claude` and returned 23 agent-facing confirmed findings; this
file is the densest single site in the estate for the false-permission shape. Open it **once**, apply
the round-2 rows in one pass, and use the rows below only as a coverage checklist to confirm nothing
the critic saw was dropped. **G6 is the exception and is residual — see §5.**

| # | Anchor | Class (untested) | Rated (untested) | Round-2 disposition | The candidate, retained as a checklist |
|---|---|---|---|---|---|
| G1 | L8 + frontmatter `description` | orphaned-scope | BLOCKER-rated | **SUPERSEDED → `03`** | Opening sentence and description both assert *"the sole live execution surface"* terminating at the Tradeify Select 100K eval, against `CLAUDE.md` §Purpose's bolded *"There is currently NO live execution surface"*. The skill carries **no reader-intercept of any kind** between frontmatter and safety invariants. This is the first text an agent reads on any rail question. |
| G2 | L15 | premise-dead | BLOCKER-rated | **SUPERSEDED → `03`** | *"**Arming is an operator GO.** … gated on M1 monitoring `RESOLVED` … **plus** a separate operator GO — architecture alone does not arm."* Enumerates **two** conditions and states them as complete. Post-08-04 there is a **third, prior bar**: both legs are withdrawn and redeploying them is barred. The correct fix is a third condition, **not** a rewrite of the two that are accurate. |
| G3 | L42 | premise-dead | MISLEADING-rated | **SUPERSEDED → `03`** | *"so every partition of the deployed rung is now measured and passing) — so **0.50× is a settled number for B7**"*. The same defect **C1**(b) fixes in `CLAUDE.md`, at the agent-facing mirror. The same line also restates MYM 69 / MNQ 11 as a binding venue fact — the premise **O-B** above rules is F2's, not an editor's. **Keep `retained-not-released` wording.** |
| G4 | L62 (§Standing context) | premise-dead | MISLEADING-rated | **SUPERSEDED → `03`** | Frames the live question as **rung selection** — 0.50× versus higher, needing a fresh both-halves regime PASS — when the actual state is that both legs were withdrawn and the lifecycle axis was deliberately **not** moved. The defect is the **asserted deployment**; the lifecycle statement is correct as written. **Do not touch the lifecycle statement.** |
| G5 | L64 | contradiction | BLOCKER-rated | **SUPERSEDED → `03`** | Advertises execution-quality research (fills/exits) as the **standing** interest and routes agents to the cost-gated `databento-data` skill for depth/microstructure pulls. `CLAUDE.md` §Purpose states in bold it is **SUSPENDED — no data source**. Worst-case reading: it authorizes **billable data spend** on a suspended question with no fill source to join against. **M21** caught the same claim at `ops/instruments/NQ.md`; this is the surface that would dispatch the pull. |
| G6 | L23 — the `fly deploy` agent grant | orphaned-scope | MISLEADING-rated | ⚠ **RESIDUAL — see §5** | The grant is dated **2026-08-02**, two days before the de-scope; its six conditions are purely mechanical and none references venue scope, while **F2, the rail's own disposition, is open at 08-08**. The table presents the authority as unconditional and carries no pointer to the fork that may moot it. ⚠ **Whether the operator intends the grant to survive F2 is not characterizable from the artifact.** A question to ask, not a finding to fix. **Do not narrow an operator grant on an audit's initiative** — and note that no refutation pass can settle this, which is why round 2 does not dispose of it. |

### 4.2 The other two agent-instruction surfaces — 2 candidates

**Consolidated disposition: SUPERSEDED → [`03-agent-facing.md`](03-agent-facing.md).** Both are the
same defect shape as G2 (a complete-sounding two-condition arming gate) on files an agent loads
without choosing to.

| # | File · anchor | Class (untested) | Rated (untested) | Round-2 disposition | The candidate, retained as a checklist |
|---|---|---|---|---|---|
| G7 | `.claude/skills/ooda-loop/SKILL.md` L111 (§5 worked example) | premise-dead | BLOCKER-rated | **SUPERSEDED → `03`** | §5 is titled *"Worked example — attended c1 arming day (canonical OODA cycle)"* and lists **arm** among eligible Decide-phase actions, bounded only by GO + M1. There can be no arming day: no strategy is deployed and the venue is de-scoped. Harder to spot than G2 because it is framed as **methodology rather than ops**. Prefer re-keying the example to a venue-neutral attended action over deleting it — the worked example carries the loop's teaching value. |
| G8 | `.claude/skills/prop-firm-challenge/SKILL.md` L12 | premise-dead | MISLEADING-rated | **SUPERSEDED → `03`** | *"the next armed send is gated on M1 monitoring RESOLVED + operator B7 GO"* — the second skill carrying the two-condition gate, under a heading reading *"Current posture (2026-07-24 — verify against CLAUDE.md; trust ADRs over this paragraph)"*. **That hedge is a generic deferral, not a reader-intercept**: it names no superseding artifact and gives no date, and the heading word *"Current"* is what makes the paragraph consumed as current despite the stamp. |

### 4.3 `deploy/c1_rail/README.md` — 2 candidates, both graduated

**Consolidated disposition: SUPERSEDED → [`03-agent-facing.md`](03-agent-facing.md). G9 is the
clearest graduation case in this section and should no longer be read from here.** Round 1 called it
*"the highest-priority row in §5.10"* and *"the most dangerous document"* the critic found, on
untested standing. **Round 2 swept `deploy/` (8 agent-facing confirmed) and confirmed it.** It has
now been through refutation; treat the round-2 row as the operative one. The two candidates share one
file and want **one editing pass**, not two.

| # | Anchor | Class (untested) | Rated (untested) | Round-2 disposition | The candidate, retained as a checklist |
|---|---|---|---|---|---|
| G9 | L78 — the B6 → arming recipe | premise-dead | BLOCKER-rated | ✅ **GRADUATED — confirmed by round 2 → `03`** | A step-by-step arming recipe ending *"Only then flip `dry_run: false`"*, with **neither** gate visible: it predates the 2026-07-31b amendment that made `dry_run=false` illegal while M1 is not `RESOLVED`, **and** it predates the de-scope. An operator or agent following it end-to-end arms a live broker account with no gate in view. |
| G10 | L5 | gate-unbinding | MISLEADING-rated | **SUPERSEDED → `03`** | *"**Nothing here arms trading.** `dry_run` stays `true` … until the GO ADR's B6 dry-fire passes."* **B6 passed 2026-07-20**, so by the clause's own terms its restraint has lapsed. What actually holds the rail disarmed today is the M1 interlock plus the de-scope, neither of which the file names. A reader who verifies "B6 passed" concludes the file authorizes proceeding. Re-anchor the restraint to the two conditions that are actually load-bearing. |

### 4.4 `README.md` and `PIPELINES.md` — 9 candidates, all already promoted in round 1

**Consolidated disposition: ALREADY PROMOTED — remediate at M6 (`README.md`) and M7 (`PIPELINES.md`)
in [`04-misleading.md`](04-misleading.md), never from here.** These nine are the constituent
observations behind two round-1 findings that *did* face refutation. Round 2's root-docs sweep covers
the same two files; check `04` for any additional rows before opening either file, then do **one pass
per file**. **Do not remediate twice.**

| # | File · anchor | Class (untested) | Rated (untested) | Round-2 disposition | The candidate, retained as a checklist |
|---|---|---|---|---|---|
| G11 | `README.md` L60 | premise-dead | BLOCKER-rated | **→ M6 (`04`)** | *"the machine-pinned mirror of live sizing constants (`scripts/validate_params.py`), and the two Striker legs' futures editions (MYM/MNQ) form the **live c1 book**"* — two dead halves in one sentence, on the front door. |
| G12 | `README.md` L5 | contradiction | BLOCKER-rated | **→ M6 (`04`)** | *"The live surface is the c1 execution rail … currently **disarmed**"* against `CLAUDE.md`'s bolded *"There is currently NO live execution surface"* — two root docs asserting incompatible things about the most load-bearing fact in the repo, with a trailing `see CLAUDE.md` that reads as a request for detail rather than a warning. M6 fixes both halves in one pass. |
| G13 | `PIPELINES.md` L127 | premise-dead | BLOCKER-rated | **→ M7 (`04`)** | *"**Active path** (GO 2026-07-17) … 2-leg book at WATCH-1 0.50× … spend ceiling $700"* — a deployed book asserted in the present tense under the heading *"Active path"*. |
| G14 | `PIPELINES.md` L15 | orphaned-scope | MISLEADING-rated | **→ M7 (`04`)** | The at-a-glance row `**P5** … **BUILT · currently DISARMED**` omits both that the rail points at a de-scoped venue and that its disposition is fork F2. Every other row carries its retirement/idle qualifier (`P2` RETIRED 2026-08-02; `P3` IDLE), so the omission reads as deliberate contrast and **P5 looks like the one live thing.** |
| G15 | `PIPELINES.md` L143 | gate-unreachable | MISLEADING-rated | **→ M7 (`04`)** | *"Q-NAS-ECR-1 stays PARKED-DORMANT pending a fresh Pre-Q **after M1 + first fill**"* — parked behind an event ADR §6 states verbatim never happens. `Q-MONSURF-1` exists to re-triage exactly these five threads, so two live documents currently disagree about whether "first fill" is a live gate. |
| G16 | `PIPELINES.md` L155 | stale-figure | MISLEADING-rated | **→ M7 and C14 (`04`)** | The governance table names `scripts/validate_params.py` as **one of only two** mechanisms guarding locked constants; the script does not exist. A reader auditing coverage concludes locked constants are machine-checked when only the soft, Guardian-band-only `verify_lock_anchors.py` remains. **C14** carries this site in its five-site substitution — take the phrasing from C14, do not invent a second wording. |
| G17 | `PIPELINES.md` L160 | stale-figure | COSMETIC-rated | **→ M7 (`04`)** | `make check` is enumerated as `validate` (+ `validate-{params,data,pine}`); the Makefile's `validate` target is `validate-data validate-pine` only, with no `validate-params` target and no `.PHONY` entry. Overstates `make check` coverage by one gate — and is the **second** independent site in this one file asserting the retired gate is live, which is why M7 prescribes a file pass rather than a line patch. |
| G18 | `PIPELINES.md` L121 | overstated-modality | MISLEADING-rated | **→ M7 (`04`)** | *"live spend still gated"* — the vocabulary of a **pending release**, not of a withdrawn deployment. It sits in the P4 section, which a reader reaches while orienting on the prop-portfolio programme rather than the rail, so the P5 pointer to `CLAUDE.md` does not cover it. Post-08-04, $208 of $700 is sunk against a venue that is no longer a deployment target, and whether the programme regains any execution surface is **F3**. |
| G19 | `PIPELINES.md` L3 | contradiction | MISLEADING-rated | **→ M7 (root cause) (`04`)**; ⚠ **generalizable clause RESIDUAL — see §5** | *"**Posture is not restated here** — for what is live, disarmed, or closed, read `CLAUDE.md`"*, then posture restated at L15, L121, L127 and L143. **This is the structural reason the file was missed by all 12 round-1 domains: it exempts itself from posture sweeps in its header.** M7 records it as root cause. |

### 4.5 Specs and operator tooling — 3 candidates

**Consolidated disposition: SUPERSEDED for the file-anchored limbs → [`04-misleading.md`](04-misleading.md)
(specs) and [`03-agent-facing.md`](03-agent-facing.md) (the script). Two limbs are residual — G21's
cross-artifact consequence and G22's proposed taxonomy — see §5.**

| # | File · anchor | Class (untested) | Rated (untested) | Round-2 disposition | The candidate, retained as a checklist |
|---|---|---|---|---|---|
| G20 | `docs/spec/c1_nt8_sizing_host_impl.md` L3 | orphaned-scope | MISLEADING-rated | **SUPERSEDED → `04`**; ⚠ **coupling status changed** | Status is still `Proposed` and the completion checklist still lists **the B6 dry-fire** (passed 2026-07-20) plus three items that each require a live Tradeify/CrossTrade account, so **the spec can never reach `Accepted` on its own stated terms** and carries no intercept saying so. ⚠ **Round-1's coupling advice is now spent:** it said to land this together with B3's `cap_alloc` repair to §2.2 — **B3 is FIXED (`d84c5e4`) and did not widen**, so this is now a standalone open item on a file someone has already touched once. |
| G21 | `docs/superpowers/specs/2026-08-02-venue-native-regime-monitor-design.md` L129 | gate-unreachable | BLOCKER-rated | **SUPERSEDED (four sites) → `04`**; ⚠ **consequence limb RESIDUAL — see §5** | *"**The monitor must exist before the first live fill** (operator queue item 3), not before 08-08."* ADR §6 names this design by role among the five threads stranded because *"the first live fill never happens"*, and the spec repeats the gate at **four sites** — L129 (build rule), L167 (rejected-permanent-posture reasoning), L196 (rejected alternative) and L239 (a literal shell build-gate check). **Treat as one document-level banner, not four patches.** |
| G22 | `scripts/m1_item5_capture.py` L22 | gate-unreachable | MISLEADING-rated | **Limb (1) SUPERSEDED → `03`**; ⚠ **limb (2) RESIDUAL — see §5** | **(1)** Stale pointer: the docstring routes an operator to `B7_STAGE1_DESK_CARD_2026-07-31.md` when three later cards exist (07-28, 08-03, 08-04) and **M17** rules the 08-04 card operative. **(2)** The critic names a **seventh failure shape the six classes do not cover — ORPHANED EXECUTABLE**: live operator tooling (this script, `scripts/m1_item5_dump.ps1`, and `ops/c1_rail/c1_rail_slippage.py` for Stage 2b) whose entire purpose is discharging an obligation that is now undischargeable. Unlike a stale prose claim it does not merely assert something false — **it presents a runnable, documented, `fly ssh`-dependent workflow, so an agent attempts to execute rather than merely believe.** |

---

## §5 — What remains genuinely untested after round 2 (4 limbs)

**18 of the 22 candidates are superseded** by a refutation-tested round-2 finding, or were already
promoted inside round 1. **Four limbs are not**, and they share a property worth naming: **none of
them is a file-anchored claim-alignment finding.** Each is a question of operator intent, a repo-wide
sweep, a cross-artifact consequence, or a taxonomy proposal — and a claim-alignment refutation pass
is structurally incapable of disposing of any of those. **They are untested because nothing tests
this shape, not because two rounds forgot to look.**

| Limb | Source | Why round 2 did not dispose of it | Standing now |
|---|---|---|---|
| **R-1** | **G6** — the `fly deploy` agent grant, `.claude/skills/c1-rail/SKILL.md` L23 | The claim is not *"this sentence is false"*; it is *"the operator may not have intended this authority to survive F2"*. **Operator intent is not characterizable from the artifact**, so there is nothing for a refutation pass to confirm or kill. | Converges on **tier 1**, not tier 3 — a verified observation with an unmade decision. It is left listed at G6 rather than relocated, because moving it would be re-adjudicating it. **Do not narrow an operator grant on an audit's initiative.** The natural vehicle is F2 on 08-08, which decides the rail's disposition anyway. |
| **R-2** | **G19's generalizable clause** — *"any document declaring 'posture is not restated here' is a candidate hiding place"* | Round 2 swept **named surfaces**; the clause proposes a **token sweep across the whole estate**, which is a different instrument. | ✅ **RUN read-only for this section, 2026-08-05 — result NULL beyond the known set.** `rg -i "posture is not restated\|not restated here\|posture is owned by"` over the tree returns **8 files** (excluding `.git`; `lab/archive/external_sourcing_2026-06-30/catalog.md` is an archived hit and out of scope). Seven are the **healthy link-out form** — a named canonical owner for a *specific* class of fact (`ops/instruments/XAUUSD.md:49` → Guardian LOCK.md/baselines; `docs/ltm/superpowers/plans/2026-07-08-…:344` → baselines; `TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md:15` → payout-phase geometry; `docs/adr/2026-07-27-hermes-agent-adoption-nogo.md:32` → the allocation ADR; `docs/briefs/Q-KBUDGET-1-phase1-inventory.md:70` → the parent §4). Only **`ops/instruments/NAS100.md:6`** pairs a self-exemption with a **retired-gate citation** (*"gated by `validate_params.py`"*) — and that site is **already C14 site (4)**. **The generalizable sweep therefore yields zero new sites and can be closed**, not carried forward. `PIPELINES.md` L3 remains the only true instance of the pathology. |
| **R-3** | **G21's consequence limb** — the monitor spec discharges the decompound-HOLD §4 limb-2 falsifier, so an unreachable build gate leaves that HOLD with **no live falsifier** | A specs sweep confirms the four unreachable gate sites **in the file**. It does not, and should not, rule on whether a HOLD elsewhere in the estate is now unfalsifiable — that is a cross-artifact governance consequence. | ⚠ **This is the same hole `O-I` describes from the P4 end, approached from the monitor end.** The two are one question with two entry points and should be **ruled together at 08-08**, not patched separately. The banner G21 prescribes must **not** silently assert a disposition for the HOLD. |
| **R-4** | **G22's limb (2)** — the proposed seventh failure class, **ORPHANED EXECUTABLE** | Round 2 confirms per-file instances (the stale desk-card pointer). The **class-level proposal** — that runnable operator tooling whose purpose is now undischargeable is a distinct failure shape from stale prose, because an agent *executes* rather than *believes* — is a methodology question. No refutation pass adjudicates a taxonomy. | **Recorded, not adopted.** Round 1's six classes were fixed before the critic ran and are **not retrofitted** (Trap #1). The recommendation stands unruled: any remediation plan should treat orphaned tooling as a **distinct bucket** from prose findings. Named instances to price if it is adopted: `scripts/m1_item5_capture.py`, `scripts/m1_item5_dump.ps1`, `ops/c1_rail/c1_rail_slippage.py` (Stage 2b). ⚠ **Adopting a seventh class is belt growth** — weigh it against the meta layer's own Degenerating limb before building anything for it. |

**Round 1's closing claim about this section, retested.** It said §5.10 was *"most likely to be wrong
in detail and least likely to be wrong in direction"*, and staked the direction claim on one row —
**G9**, the arming recipe naming neither gate. **Round 2 swept `deploy/` and confirmed it.** The
direction claim held. The detail claim is untestable in aggregate and is not asserted.

---

## §6 — What this section does not license

Every clause below already appears somewhere above; they are collected so a remediation pass reading
only the tables cannot widen its own mandate.

1. **No row here authorizes an edit.** Tier 1 items are decisions the operator has not made. Tier 2
   items have no verdict. Tier 3 items are superseded or residual. **The only disposition in this
   file is FU-1's ruling in §1, and its scope is one trade in one named week, operator-placed.**
2. **No agent may place the token trade.** Stated in the ruling, restated here because this file is
   where an agent reading about the token trade is most likely to land. The rail is not the
   instrument; `dry_run` stays `true`; M1 stays unresolved.
3. **Nothing here touches the frozen set** — locked strategy parameters, Pine, `dd_protection`
   constants, `core/lifecycle.py` tier multipliers, allocations, `LEG_MAP`, or frozen ADR §2 decision
   text. **O-G** and **O-H** in particular name `core/firm_rules.py` values and **explicitly decline
   to re-encode them**: that route runs through an ADR plus the engine pre-flight, and a re-MC where
   the run consumes those rows as the simulation target.
4. **Dated bodies are not edited in place** (Trap #12). U1's and U2's drafted corrections, if ever
   adopted, land as amendments — and **U2's §0 anchor is explicitly correct history that must be left
   as filed**, whatever is done to the Status and Verification lines around it.
5. **DELETE means retire with a tombstone.** Nothing in tier 3's "superseded" column authorizes
   removing a candidate row; superseded rows are retained here precisely so the critic's coverage
   stays auditable.
6. **The three tiers must not be merged.** A future editor tidying this file into one table would
   destroy its only load-bearing property.
