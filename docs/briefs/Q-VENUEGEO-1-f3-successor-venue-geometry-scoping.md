# Q-VENUEGEO-1 — Which remaining friendly firms are geometry-viable for a token-trade-compliant micro book at the frozen gate? (DEPLOYMENT)

**Status:** `OPEN — evidence recorded, unconsumed` — F3 ruled **no successor migration now** ([`S1 ADR`](../adr/2026-08-07-loop-s1-environment-ratification.md) 2026-08-07); DP1 + DP2 DISCHARGED; DP3 bust-ceiling half MEASURED; **EV/$ half + precision re-run remain available** if a future GO reopens migration — intaken 2026-08-05 (drafted 2026-08-04 by Joshua + claude.ai advisor from the four-tool-stack research report); `check_brief.py --type inquire` PASS (6/6)
**Authored:** 2026-08-04
**Intaken:** 2026-08-05 (handoff-verify PASS; anchors re-verified at `origin/main` `21e09c8`; DP2 scope amended — see Amendment log)
**Amended at merge (2026-08-05):** DP1 + DP2 item 8 discharged by concurrently-landed work ([PR #647](https://github.com/Joshua-Asante/first-passage/pull/647), ADR 2026-08-05, ADR 2026-08-05b); remaining scope narrowed — see second Amendment log entry below
**Closed:** N/A
**Authors:** Joshua + claude.ai (advisor); intake + amendment by CC
**Parent question:** fork **F3** of ADR 2026-08-04 (successor venue) — this Q is decision support for it, and feeds the four-firms ADR §4 falsifier (2026-11-08)
**Sub-questions opened:** none yet (DP1 cadence axis · DP2 venue-fact verification · DP3 EV/$ ranking · DP4 rail hardening — packages)
**Loop:** Inquire-phase Pre-Q — closure gates whether F3 receives a ranked admissibility input (it never authorizes spend)
**Artifact path:** `docs/briefs/Q-VENUEGEO-1-f3-successor-venue-geometry-scoping.md`
**Spend by authoring:** $0 · K=0 · no manifest · nothing armed

---

## Amendment log (intake, 2026-08-05)

- **§0 re-anchored** at `origin/main` `21e09c8` (was `613aa0d`). The two commits in between
  (`f7c5bec`, and merge `21e09c8` itself) touch only `STATE.md`, `docs/SESSIONS.md`, and the
  `mnq_orb_flow_substrate_2026-08-05/PREREG.md` amendment log — none of this brief's cited files.
  All 21 originally-cited anchors verified present and unchanged; all load-bearing paths confirmed
  extant on disk (`handoff-verify` Phase-0 checklist, run in full before this intake).
- **§1 "queue row 3" reference removed.** The draft cited "queue row 3 states the blocker plainly"
  for F3. STATE.md's operator queue was renumbered 2026-08-05 (discharge of the prior row 1), and F3
  sits at a different row now than it did at authoring time — worse, at the moment the draft was
  written, row 3 was actually the 08-08 audit-vehicle row, not F3, so the citation was never
  numerically exact. Replaced with a reference to the ADR §7 F3 fork directly, which is stable
  against queue reordering (Rule 7 pointer discipline).
- **§1/§7 DP2 sweep list amended: added the per-firm inactivity/idle-rule item.** The original DP2
  enumeration (automation/EA clause, DD method, consistency %, payout cadence, contract caps, MFFU
  2%-of-limit clause, compliance-instrument legality) did not include the activity/cadence rule
  itself — existence, threshold, enforcement hardness, and reset semantics. This is the exact axis
  that killed the Tradeify deployment (`inactivity_max_idle_days: 5` priced at 92.6–97.6% path death
  once the rolling-absorbing engine barrier was modeled; separately, the [activity-rule disposition
  spec](../spec/2026-08-02-tradeify-activity-rule-disposition-spec.md) found the *enforcement
  hardness* itself was originally mis-read — "soft warnings" corrected to "irreversible account
  deletion" from a second help-centre article the first pass never consulted). Scoring three
  candidate firms without independently verifying each one's own idle-rule shape and enforcement
  hardness would repeat exactly the error that took two verification passes to catch here. Added as
  DP2 item 8 below and in §7 Phase 1.

No other content changed. The book-shape pin, the forbidden moves, the gate criteria, and the
execution plan are otherwise as originally scoped.

---

## Amendment log (merge, 2026-08-05) — DP1 + DP2 item 8 discharged; scope narrowed, not closed

**This branch (`claude/preq-intake-venuegeo-monsurf-filltax-mschan`) sat open while three separate
sessions landed [PR #647](https://github.com/Joshua-Asante/first-passage/pull/647) (F3 cadence
study), [ADR 2026-08-05](../adr/2026-08-05-blusky-inactivity-unsourced-encoding.md) (contain
BluSky's unsourced field), and [ADR 2026-08-05b](../adr/2026-08-05b-blusky-inactivity-rule-sourced.md)
(source it) directly on `origin/main`.** Read in full before resolving the merge conflict (per
`feedback_check_origin_main_before_multistep_build` — re-fetch before any multi-step build, not just
at start). What they discharge, and what they do not:

**DP1 (cadence axis) is DISCHARGED.** [`RESULTS`](../../lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md)
measured all three firms against the locked book on the same engine/panel as the Tradeify sibling
study, control-pinned to Δ0.003pp before any F3 cell was read. **Bulenox 90.85–97.54%** and **MFFU
91.77–97.54%** unmitigated inactivity death (idle=5, venue-invariant, same fatal class as Tradeify's
92.60%); **BluSky 4.87–13.14%** (idle=22, sourced from its own Terms of Use art. 11490284 §3.3 +
Brokerage Funded Rules art. 12434442, unit-corrected from a miscoded 30-calendar-day reading).

**DP2 item 8 (the idle/inactivity-rule verification this brief's intake amendment added) is
DISCHARGED for all three firms** — Bulenox and MFFU were already correctly sourced and encoded
(verified 2026-07-03/06); BluSky's was freshly sourced 2026-08-05 with the exact Rule-13 discipline
this brief called for (verbatim article citation, primary source, unit-conversion check caught and
corrected). No further idle-rule verification work is owed on any of the three firms.

**What is NOT discharged, and is the reason this brief stays OPEN rather than closing:** the
"Bulenox + MFFU ELIMINATED" verdict, as recorded in `STATE.md` row 3 and RESULTS §4.1, reads on the
**bare, uninstrumented book** — RESULTS §6 item 3 names this directly: *"mitigation, not venue
choice, is the live lever… the R8 scheduled-maintenance-trade remedy remains owed and remains the
cheapest cadence instrument at every venue measured."* This is exactly the book-shape distinction
§4's H-VENUEGEO-1 was pre-registered to enforce (*"Ranking venues against the uninstrumented shape
would… relocate the exact Tradeify activity failure to a new address under the appearance of a fresh
decision"*) — and it is exactly the shape of Tradeify's own arc, whose unmitigated 96.9% account-
deletion rate became a 99.4% pass once the compliance-instrument was priced in
([`seed-target spec`](../../lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/RESULTS.md)). **This
is not a claim that Bulenox/MFFU survive instrumented** — it may turn out the compliance instrument
is barred at one or both firms (automation posture, minimum-hold, or scalping clauses could rule it
out), in which case ELIMINATED stands confirmed rather than overridden. It is a claim that the test
has not yet been run, and DP2's compliance-instrument-legality item is precisely that test. **This
does not re-litigate ADR 2026-08-05 / 2026-08-05b** — those ADRs answered a narrower, correctly-scoped
question (source and correctly encode BluSky's field) on explicit operator directive; this brief's
scope is complementary, not contradictory, and nothing here proposes reopening either ADR.

**Scope narrowed accordingly:** DP2's remaining Phase 1 work is (a) compliance-instrument legality
(minimum-hold, scalping, no-intent-trade clauses) across **all three firms**, since this is the one
test that could still change the Bulenox/MFFU verdict, and (b) for BluSky specifically, independent
re-verification of consistency %, cost, payout cadence, automation/EA clause, and auto-liquidation
mechanics — ADR 2026-08-05b's own §6 Risks names these as **"un-re-verified"** survivors of the same
2026-07-12 sweep whose collection-scoping (right collection, wrong document class) is what missed the
inactivity rule in the first place. DP1 and DP3's original 3-way EV/$ ranking scope are otherwise
unchanged, except DP3 now runs against a much better-evidenced starting point.

---

## §0 — Rule 0 reads

Read this session (anchored at `origin/main` `21e09c8`, 2026-08-05; content-diffed against the
original `613aa0d` anchor — no cited file changed in between):
- `STATE.md` (operator queue; F2/F3/F1 framing, post-2026-08-05 renumbering), `docs/SESSIONS.md`, `CLAUDE.md` §posture — via `git show` / diff
- `lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/RESULTS.md` (head) — anchor: `536813f` (2026-08-04) — activity rule is the binding constraint; token trade +96.3pp (verified: 0.22 duty → 3.0%/96.9% deletion without token trade; 99.3% with)
- `docs/spec/2026-08-02-tradeify-activity-rule-disposition-spec.md` — anchor: confirmed present at intake — H3 correction (soft-warning reading FALSIFIED by a second primary source; account deletion is irreversible) — grounds for the DP2 amendment above

Read at merge (2026-08-05), full body:
- `lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md` (+ Addendum 2026-08-05b) — DP1 cadence measurement; Bulenox/MFFU 90.85–97.54% unmitigated, BluSky 4.87–13.14% sourced
- `docs/adr/2026-08-05-blusky-inactivity-unsourced-encoding.md` + `docs/adr/2026-08-05b-blusky-inactivity-rule-sourced.md` — BluSky idle-rule sourcing chain; DP2 item 8 discharge for BluSky; §6 Risks flags consistency/cost/auto-liquidation as un-re-verified
- `core/firm_rules.py` `BluSky_Premium_100K` block — current encoded state: `inactivity_max_idle_days: 22`, `inactivity_rule_sourced: True`, `micro_contract_cap: 100`, `consistency_rule_pct: 34.0`, `automation_attended: True`, `cost_per_side_usd: 0.95` — all present but only the first two are independently re-verified; the rest inherit the flagged 2026-07-12 sweep

Anchored, body unread — `[§0-pending content read before lock]`:
- `docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md` incl. Addendum — anchor: `fa4d6e8` (2026-08-04) — forks F1/F2/F3; clause 1–2 deployment bar on the Striker legs
- `docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md` §4 — anchor: `ea0886d` (2026-07-25) — 11-08 HARD falsifier: ≥1 candidate clears bust ceiling on ≥2 of 4 firms
- `core/firm_rules.py` — anchor: `2345095` (2026-08-03) — encoded tiers; frozen $100K×4 set; no eval time-limit key exists; DP2's idle-rule verification target for each firm's tier dict
- `docs/spec/2026-08-04-phase4-both-halves-intraday-rerun-spec.md` — anchor: `dc7adcc` (2026-08-04) — honest-clock MC already GO'd; reuse, don't rebuild
- `docs/notes/rail_build/RUNBOOK.md` §B6–B7 — anchor: `2345095` (2026-08-03) — idempotency DISPROVEN; lapse-while-armed self-brick
- `docs/notes/2026-07-24-tradeify-rulepin-verification.md` — anchor: `cad464f` (2026-08-04) — the Rule-13 verification form (Pin 6 lesson: an unflagged unverified pin was right by luck)

---

## §1 — Context & motivation (with an honest overlap statement)

F3 (2026-08-08 operator fork, ADR `docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md` §7) must rule keep-none / register-successor: none of Bulenox / MFFU / BluSky has the **cadence-axis** measurement — "three firms remain" is a fact about the set, not about viability. The seed-target spec (PR #640) re-derived the eval's binding constraint as the weekly activity rule and nothing else: at the incumbent's 0.22 duty, pass collapses to 3.0% with 96.9% account deletion; a token trade swings it to ~99.4% (+96.3pp) for ~$24/yr. The 11-08 §4 falsifier stands undischarged. **Overlap statement:** the research report's "build a prop-firm Monte-Carlo engine" already exists here (`core/portfolio_mc` + `firm_rules` + the frozen composed engine; the Phase-4 intraday honest-clock re-run is GO'd with a spec). This brief scopes only the deltas: **DP1** cadence axis across the three firms; **DP2** Rule-13 venue-fact verification — including two research-sourced, **UNVERIFIED** facts: (a) MFFU reportedly suspends trading on any contract within 2% of its CME daily price limit, which with the 5% overnight equity-index limit could make MES/MNQ/MYM frequently untradeable there — if confirmed, it materially bears on the ≥2-of-4 falsifier; (b) Bulenox reportedly permits EAs/automation explicitly, on all account types — plus (c, added at intake) **the per-firm idle/inactivity rule itself** (existence, threshold, enforcement hardness, reset semantics), since Tradeify's own version was misread once already; **DP3** pass-EV per eval-dollar ranking at the frozen gate; **DP4** rail kill-switch hardening (CrossTrade Account Manager as an independent flatten+lock layer) — **F2-conditional**, addressing the disproven `order_id` idempotency and the armed-expiry failure class.

---

## §2 — Prior art / lineage

- De-scope ADR + Addendum (`fa4d6e8`) — forks; deployment bar on the withdrawn legs; Tradeify-shaped *research* not barred.
- Four-firms ADR §4 (`ea0886d`) — the standing consequence frame this Q feeds; it is **not restated or moved** here.
- Seed-target spec (`536813f`) + c1 cadence/inactivity study (`92abdbb`) — the machinery DP1 reuses.
- Q-BUSTGATE-1 closure (fork B) — rung selection = EV/dollar-day; WATCH-1 0.50× stands; DP3 ranks in the same currency.
- Rule-pin note (`cad464f`) — the verification form DP2 follows; Pin 6 is the cautionary anchor.
- Activity-rule disposition spec (2026-08-02) — the H3 soft-vs-hard enforcement correction motivating the DP2 idle-rule addition (intake amendment).

---

## §3 — Question (Q-VENUEGEO-1)

**Q-VENUEGEO-1:** F3 must choose among three firms for which no comparable cadence/geometry measurement exists and at least three load-bearing venue facts (including each firm's own idle/inactivity rule) are unverified. What does the frozen gate — cadence axis included, facts verified — say about each firm's admissibility, including the answer "none"?

---

## §4 — Falsifiable hypothesis (H-VENUEGEO-1)

**Book-shape axis is PINNED at freeze — this is load-bearing, not a parameter.** Admissibility is scored on **current book + compliance instrument**, never on the bare book. Grounds: the seed-target spec measured the incumbent's 0.22 duty at **3.0% pass / 96.9% account deletion**, and the *same* book with a token-trade instrument at **~99.4% pass** — a +96.3pp swing for ~$24/yr. Ranking venues against the uninstrumented shape would therefore rank them all near-unpassable and, worse, would relocate the exact Tradeify activity failure to a new address under the appearance of a fresh decision. The bare-book row may be reported as a **contrast row only**, explicitly labelled non-admissible, so the instrument's contribution stays visible.

**H-VENUEGEO-1:** If, at the frozen $100K×4 gate with the activity/cadence axis added, DP2-verified venue facts as inputs (idle-rule shape included), and the book shape pinned to **current book + compliance instrument**, ≥1 firm yields a configuration with simulated bust ≤ that firm's ceiling AND pass-EV per eval dollar ≥ a floor set at freeze, then F3 has at least one admissible successor; otherwise the honest F3 answer is "no admissible successor at current book shapes," and the 11-08 §4 reading sharpens accordingly (per F1's jurisdiction, which this brief must not pre-empt).

**Reject H if:** 0 firms admissible at frozen thresholds with verified facts.
**Accept H if:** ≥1 firm admissible; output is a ranked packet, never a purchase.
**Ambiguous-hold if:** admissibility flips on a fact that cannot be verified from primary sources → name the fact + verification route, dated re-test.

---

## §5 — Forbidden moves

- **Buying an eval because the sim ranks a firm #1** — the standing pattern is explicit: registration and live spend are separately operator-GO'd with a signed ceiling; simulation output licenses a packet, nothing else.
- **Entering the MFFU price-limit or Bulenox automation facts into `firm_rules.py` from the research report** — tempting because they're specific and decision-relevant; both are third-party-sourced and enter only after Rule-13 verbatim-clause verification against the firm's own primary pages (the Pin-6 lesson exists because an unverified pin was right by luck once).
- **Scoring admissibility on the bare 0.22-duty book** — tempting as the "conservative" or "unassumed" baseline; it is neither. It reproduces the 3.0%-pass geometry that just killed the Tradeify eval and would either rank every firm unpassable or pick a winner on noise. Bare book appears as a labelled contrast row, never as the admissibility basis.
- **Assuming the compliance instrument is legal at each successor because it was ruled permitted-in-principle at Tradeify** — the 08-02 Option A ruling is Tradeify-scoped. Instrument legality is a **DP2 verification item per firm** (minimum-hold rules, scalping clauses, and "no-intent" trade prohibitions vary and can void it); if a firm bars it, that firm is scored at its bare-book geometry and the reason is recorded.
- **Assuming a firm's idle/inactivity rule is soft-enforced because Tradeify's first-read was** — Tradeify's own rule was misread once (soft warnings, corrected to irreversible deletion, from a second primary source the first pass never consulted). Each firm's enforcement hardness is independently verified, never inherited from another firm's corrected or uncorrected reading.
- **Reading the Addendum as reopening Striker-on-Tradeify deployment** — it narrowed the *research* bar only; clause 1–2's deployment bar on the two withdrawn legs stands.
- **DP4 touching `dd_protection`, arming anything, or running before F2 rules** — kill-switch hardening is configuration beneath the strategy layer, F2-conditional, and never a backdoor arm.
- **Pre-empting F1 by "deciding early" how §4 reads a de-scoped firm** — the ADR's own F1 fork warns against exactly this; DP3 simulates over the frozen set (Tradeify included, as §4 requires) and leaves the reading to F1.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | ≥1 firm clears bust ceiling + EV/$ floor with verified facts | `INTEGRATE — ranked F3 input packet to operator; any registration/spend is a separate GO with signed ceiling; DP4 proceeds only per F2` |
| `FALSIFIED` | 0 firms clear at frozen thresholds | `STOP — F3 input reads "no admissible successor at current book shapes"; re-proposal bar = a new book shape or changed venue terms, not looser thresholds` |
| `AMBIGUOUS-HOLD` | admissibility hinges on an unverifiable fact | `ITERATE — return target: the named fact's verification route; dated re-test on verification` |

---

## §7 — Execution plan

- **Phase 0** — Rule-0 reads (§0 pending list). **DONE for DP1 + DP2 item 8** (merge amendment above).
- **Phase 1** — **DP2, remaining scope only** (item 8 already discharged for all three firms; DP1 already discharged): **(a) compliance-instrument legality — all three firms** (minimum-hold, scalping, and no-intent-trade clauses) — this is the pivotal test, since it is the one item that could still change Bulenox/MFFU's bare-book "ELIMINATED" read, symmetric to the token trade that rescued Tradeify's own unmitigated figure; **(b) BluSky-specific re-verification** of automation/EA clause (verbatim — is `automation_attended: True` faithful to BluSky's actual text, and does it cover a fixed-qty=1 near-instant-close token instrument specifically?), consistency % (re-verify 34.0, not just re-cite it), payout cadence (not yet encoded anywhere), contract caps (re-verify 100 micro / 10 mini), cost per side (re-verify 0.95), and auto-liquidation mechanics — all five flagged by ADR 2026-08-05b §6 as inheriting the same collection-scoped 2026-07-12 sweep that missed BluSky's inactivity rule the first time; **(c) the MFFU 2%-of-CME-daily-limit clause** (unverified research-sourced fact from the original draft, unaffected by the cadence study). Recorded in the rule-pin note's form, primary sources only, ≥2 independent sources per the Pin-6 lesson.
- **Phase 2** — Freeze (§8): **book shape pinned to current book + compliance instrument** (bare book retained as labelled contrast only), EV/$ floor, bust ceilings per verified method, cadence distributions, idle-rule semantics per firm. Firms where DP2 finds the instrument barred are frozen at bare-book geometry with the barring clause cited.
- **Phase 3** — DP1+DP3 ($0): reuse the cadence-study machinery + seed-spec harness + Phase-4 honest-clock engine; produce the per-firm admissibility table and ranking.
- **Phase 4** — Verdict + closure per §9. **Timing note:** Phases 1–3 are pre-08-08-feasible *if the operator books this as F3 packet input* — nothing here self-adds to the 08-08 slate.
- **DP4** — held entirely behind F2's ruling; separate mini-spec if F2 = keep/re-point.

---

## §8 — Verdict pre-registration

`docs/briefs/pre-registration/Q-VENUEGEO-1-verdict-preregistration.md` — committed before Phase 3. Hash/date: `<at prereg commit>`.

---

## §9 — Closure record format

Per `references/closure_record.md`; typed `## Iterate` block mandatory (gate 14 HARD).

---

## §10 — Audit hooks (runnable)

```bash
# No unverified fact entered firm_rules (every new key traceable to a DP2 verification line)
git log -p --oneline -- core/firm_rules.py | rg -n "VENUEGEO|MFFU|Bulenox|BluSky"
rg -n "verified" docs/notes/2026-07-24-tradeify-rulepin-verification.md

# Clause 1–2 deployment bar untouched
rg -n "clause" docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md

# Prereg predates Phase 3
git log --oneline -- docs/briefs/pre-registration/Q-VENUEGEO-1-* | tail -1

# Book-shape pin held: admissibility rows are instrumented; bare rows labelled contrast-only
rg -n "contrast|bare book|compliance instrument" lab/analysis/**/venuegeo*/RESULTS.md

# Idle-rule verified per firm, not inherited (intake amendment)
rg -n "idle|inactivity" docs/notes/2026-07-24-tradeify-rulepin-verification.md docs/notes/**/venuegeo*
rg -n "instrument legality|minimum.hold|no-intent" docs/notes/2026-07-24-tradeify-rulepin-verification.md docs/notes/**/venuegeo*

# DP4 dormant unless F2 ruled
rg -ln "Account Manager|kill" ops/c1_rail/ | xargs -r git log -1 --format="%h %ad" --

# §4 falsifier language unmodified by this Q
git log -1 --format="%h" -- docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md
```

---

## Verification

`check_brief.py --type inquire` run at intake (2026-08-05): PASS (6/6). §0 anchors re-confirmed against `origin/main` `21e09c8`; seed-spec headline numbers grep-matched against `RESULTS.md` (0.22 duty → 3.0%/96.9%; token trade → 99.3–99.4%/+96.3pp).

## Pre-Lock Checklist

- [x] §0 pending reads completed with anchors (re-verified at intake against `21e09c8`; DP1/DP2-item-8 sources read in full at merge)
- [x] DP1 (cadence axis) — DISCHARGED at merge (RESULTS + ADR 2026-08-05b)
- [x] Idle/inactivity rule (DP2 item 8) verified **per firm**, all three — DISCHARGED at merge (Bulenox/MFFU pre-existing, BluSky sourced 2026-08-05)
- [x] Compliance-instrument legality verified **per firm, all three**, primary sources only — DONE 2026-08-05, [`verification note`](../notes/2026-08-05-f3-compliance-instrument-legality-verification.md). **Bulenox facially open** (no minimum-hold, no genuine-intent clause found — pending 2 non-public docs); **MFFU** plausible-but-discretionary, plus a confirmed standing CME 2%-price-limit risk naming MNQ/MYM directly; **BluSky** a genuine gray zone (no mechanical bar, no safe harbor)
- [x] BluSky consistency %, cost, payout cadence, automation clause, auto-liquidation independently re-verified — DONE 2026-08-05. **Two discrepancies found**: `cost_per_side_usd: 0.95` contradicts BluSky's published $0.50/side (micro, Evaluation); `micro_contract_cap: 100` is Evaluation-phase only — funded/live stage is ~50. Flagged for operator-directed correction (ADR precedent: 2026-08-05→2026-08-05b), **not applied here**
- [x] MFFU 2%-of-CME-limit clause verified — CONFIRMED real (upgraded from unverified research-sourced claim), names MNQ/MYM explicitly
- [x] Book shape pinned to current book + instrument; bare-book rows labelled contrast-only — DONE 2026-08-05 for the bust-ceiling half, [`DP3 RESULTS`](../../lab/analysis/c1/venuegeo_dp3_bustceiling_2026-08-05/RESULTS.md)
- [ ] EV/$ floor + ceilings frozen at §8 — owed, Phase 2 (blocked on eval-price sourcing per firm)
- [x] DP3 bust-ceiling half — MEASURED 2026-08-05, reusing existing control-pin-verified simulation output (caught and worked around a data-staleness trap in the process — see RESULTS §0). **Bulenox and BluSky tied at 2.96% instrumented bust, statistically indistinguishable from the 3.0% ceiling given simulation noise (±0.19pp 95% CI); MFFU fails at 3.54% on DD geometry alone, independent of the token-trade question.** Bare-book bust without the instrument: Bulenox/MFFU ~97.5%, BluSky 15.48% (corrected) — no firm viable unmitigated.
- [ ] DP3 EV/$ half (pass-EV per eval-dollar) — owed. Needs each firm's $100K evaluation-account purchase price (unsourced for all three; Tradeify's own $328/$258-promo pin is the only comparable figure in the estate)
- [ ] Higher-precision re-run of the Bulenox/BluSky instrumented arm — owed. The 2.96% vs 3.0% margin is inside one standard error at the current sim count (30,000 paths/arm) and should not be treated as a confident clearance
- [x] Operator has the 08-08 booking decision for this packet as a live option (F3 queue row now points here)
- [x] Q-ID confirmed unclaimed (checked HEAD + origin/main at intake, 2026-08-05)
