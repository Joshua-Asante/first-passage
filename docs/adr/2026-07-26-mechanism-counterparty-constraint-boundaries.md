# ADR 2026-07-26 — Mechanism boundaries: counterparty-constraint definition, flow-census sourcing, executed-K closure rule

**Status:** `Accepted` — **all three clauses ratified by the operator 2026-07-26** ("Bank executed K per 2-C, and ratify all three clauses"). Drafted same day at operator direction ("question what we require of a 'mechanism'... this is the source of our edge as a strategy research pipeline"). Downstream §6 edits landed with the ratification commit; 2-C's first application (ST-EH-1) executed the same session.
**Decision date:** 2026-07-26
**Authors:** Joshua (direction) + Claude Code (Opus 5, drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Amends-in-part:** [`2026-07-15-external-mechanism-harvest-intake.md`](2026-07-15-external-mechanism-harvest-intake.md) / [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) (Requirement 1a sharpened; §2.3 sourcing channel added; edits land on ratification, not before) and [`2026-07-11-discovery-campaign-defaults-ratified.md`](2026-07-11-discovery-campaign-defaults-ratified.md) Default #5 (decay monitor extended for constraint-flow seeds) + Default #2 K semantics (executed-vs-declared clause for operator-stopped campaigns).
**Related:** [`2026-07-26-regime-candidate-flag-lane.md`](2026-07-26-regime-candidate-flag-lane.md) (sibling ADR, same session, Accepted 2026-08-21); ST-EH-1 closure (first case for §2-C).
**Layer:** methodology (research rules of evidence only). No strategy/risk-control parameter, allocation, `dd_protection` constant, or Pine source is touched.

---

## §0 — Rule 0 reads (production-source verification, this session 2026-07-26)

- `docs/methodology/strategy_harvest.md` @ `8690a81` (2026-07-25) — the five admission requirements verbatim; Requirement 1a currently reads "who systematically loses money and why (dealer hedging flow, rebalancing flow, roll congestion, forced positioning)"; §2.3 ranked channel portfolio (6 literature-centric ranks); §1 relief-valve note "requirement 3 is a permanent kill... the bar is a fact about the ledger"; Clause K cap: PASS iff K_eff ≤ 3 (floors K=2→0.85, 3→0.98, 4→1.06 FAIL); family-bank snapshot "GC/MGC 3,177 · ES 2 · MNQ 1 · all others 0 (re-read the manifests)".
- `lab/discovery/register_search.py` @ `67cc146` — `close` requires p-values; no operator-stopped path exists; `K_banked(family)` is read from **closed** manifests only (per strategy_harvest.md §1 Req 3), so an open manifest banks nothing.
- `discovery_manifests/*.json` (read this session) — `disccamp0_gc_2010_18` closed K=3,177 (GC family); `d5_nq_intraday_mom` closed K=1 (MNQ); `fc_carry_6e6j6cl` closed K=1; `orb_mnq_intraday_breakout` **open** K=1; `st_eh_supertrend_grid` **open** K=84 declared, **zero grid reads executed** (operator-stopped 2026-07-26 pre-Phase-3; auditable: no results artifacts, long-panel data ~100/570 chunks, holdout guard shows nothing scored).
- `core/firm_rules.py` @ `fd95c72` — Tradeify hedging rule (Equity Index Product Group: opposing directions prohibited in/across accounts → index relative-value structures venue-dead); micro FX at Tradeify = M6A + M6E only (M6E $0.80/side Tradeify, $0.72 MFFU); MGC $1.06/side; flat 16:45 ET.
- `docs/rejected_candidates.md` @ `2fbc996` — graveyard classes the census must not silently re-open: month-end (D3/D7/HARV-ES), 3rd-Friday settlement reversal (MYM-3FPS-1), the 2026-07-21 raised bar on single-instrument index-futures intraday OHLCV directional timing.
- `ops/instruments/MNQ.md` / `MYM.md` @ `691fd48` — DEAD lists + "MYM family K bank remains 0" (pre-ST-EH).
- ICT record (memory `project_ict_cascade_true_state_qict1_moot`, corrected f8f9006) — the in-house proof that narrative richness ≠ mechanism: the most story-complete framework examined, closed per-layer under M=65.

---

## §1 — Context

The pipeline's de facto mechanism requirement — "a plausible causal story attached to a price pattern, with reachable gates" — has produced ~15 closures and one survivor, and the survivor (ORB-MNQ-1) is not a pattern-with-story but a **flow event** (opening auction concentrating information where volatility expansion outruns cost scaling). Requirement 1a's current wording ("who loses money and why") admits preference-based behavioral narratives that the record has repeatedly falsified (ICT per-layer; four conditioning gates; the trend/MR/momentum graveyard). Meanwhile the search space the definition implicitly binds to — price transforms of the target instrument's own bars — is exactly where global mining K concentrates, so the pipeline pays first-world DSR floors for third-world seeds. The operator's 2026-07-26 direction: widen where mechanisms may come from, and make the definition earn the widening.

Separately, ST-EH-1's operator-stop exposed a hole in K semantics: `register_search` has no closure path for a campaign stopped before any declared read executed, and the difference (bank 84 vs bank ~1/family) decides whether the MNQ and MYM families remain open to new seeds at all (declared-84 → floors ≈1.44, both families dead to harvest; executed → MYM 0.85 open, MNQ 0.98–1.06 marginal).

**Decision driver (one sentence):** the mechanism definition is the pipeline's edge and its current form neither excludes what the graveyard says to exclude (unfalsifiable narratives) nor admits what the survivor says to admit (constraint flows sourced from market structure), and the ST-EH-1 closure cannot be executed honestly until the K semantics are pinned.

---

## §2 — Decision (three clauses, separable at ratification)

**2-A. Four-clause mechanism definition (sharpens harvest Requirement 1a).** A Path-1a mechanism claim must name all four, ex ante:

1. **WHO pays — a constraint, not a preference.** An identified counterparty class trading under mandate, benchmark, or mechanical rule (rebalance mandates, benchmark-execution windows, expiry mechanics, hedging requirements, index-tracking). The counterparty keeps paying because it is compensated elsewhere (tracking error avoided, mandate compliance). Preference/behavioral stories ("retail chases," "stops get hunted") no longer satisfy 1a — they route to 1b's four-part evidence-robustness test or die. (Path 1b is untouched.)
2. **WHEN it must appear — schedule or trigger declared before any data is read.** The clock/calendar/state condition under which the flow is obligated. This is what downstream placebo tests test.
3. **WHY it survives — a capacity/awkwardness argument.** An explicit reason arbitrage capital has not consumed the rent: capacity below institutional minimum size, assembly-awkward data, or mandate-inelastic demand. "Nobody has noticed" is inadmissible. This clause operationalizes "lesser-mined": mined-ness is a property of (data × expressibility × capacity) triples, and a seed must claim its niche on at least one axis.
4. **HOW it dies — a constraint observable.** For constraint-flow seeds, the Default-#5 decay monitor must watch the constraint's own observable (AUM, fix volume, imbalance size, OI) alongside the edge-series CUSUM. The constraint disappearing is the death certificate; PnL decay is only the symptom.

**2-B. Structural flow census as a sourcing channel.** §2.3's channel portfolio gains a rank: **direct enumeration of mandated/mechanical flows on venue-legal instruments** (census artifact: a Notice-phase log; first instance `docs/notes/notice/N-2026-07-26-forced-flow-census.md`, pruned at the Great Prune; retrieve via `git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md`). A census entry is an observation, not a seed: it consumes **zero K** (no PnL examined) until it graduates via the unchanged admission path — five requirements, δ via citation or extraction probe, screen, pre-registration. Census entries must carry the four §2-A clauses, a venue check, the family K-floor arithmetic, and a graveyard-adjacency attestation.

> ⚠ **Addendum 2026-08-08 — the "family K-floor arithmetic" limb is narrowed to a DISCLOSURE.**
> [`ADR 2026-08-04 — family K-bank is disclosure, not a gate`](2026-08-04-family-k-bank-disclosure-not-gate.md)
> (`Accepted`) sets `K_eff = K_intrinsic` and rules that `K_banked(family)` **cannot fail a seed** — there is no
> floor for the arithmetic above to compute. A census entry must still **disclose** the family bank; it must no
> longer derive or apply a floor from it, and a burned family no longer kills a seed. The §2-B clause text is left
> unedited (dated-decision integrity); this note is the reader intercept. Live enforcement surface:
> `lab/research_utils/axis_screen.py`, which deliberately does **not** sum `k_banked`.

**2-C. Executed-K closure rule for operator-stopped campaigns.** When a campaign is stopped by operator direction before declared reads execute, the manifest closes banking **executed selection events** (reads whose results any human or artifact examined), with the declared K preserved in provenance — subject to ALL of: (i) zero results artifacts exist; (ii) execution impossibility or non-occurrence is git-auditable (missing data, absent outputs, guard evidence); (iii) the closure note enumerates every executed look and its examiner; (iv) the operator signs the closure. Where any condition fails, the declared K banks in full ("abandoned campaigns still bank their K" is unchanged for campaigns that *looked*). First case: ST-EH-1 (declared 84; executed = 2 one-year TV baseline examinations, 1/family; manifest held OPEN pending the operator's ruling, which this clause's ratification would supply).

**Effective:** **2026-07-26**, all three clauses (operator ratification). **Scope:** research rules of evidence; harvest/discovery intake and ledger semantics only.

**2-C first application (same session, recorded here because it is the clause's worked example):** ST-EH-1 closed `operator-stopped`, banking **executed K=2** (one look per instrument family — the two 1-yr TV baseline panels) against **declared K=84**, which is retained in the manifest's `declared_K` field. All four conditions were met and are auditable. Resulting family banks and floors (K_intrinsic=1 seed): **MNQ bank 2 → K_eff 3 → floor 0.98** (open, but AT the cap — a single K_intrinsic=1 seed only; any second expression fails), **MYM bank 1 → K_eff 2 → floor 0.85**, **6E bank 1 → K_eff 2 → floor 0.85**. **Reader warning:** the ST-EH-1 manifest banks `K=2` as one number spanning TWO families — the split is **1 MNQ + 1 MYM**, stated in its `executed_looks` field. Do not add 2 to either family.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep 1a as-is, rely on downstream gates to kill weak stories | The record shows the gates DO kill them — at full campaign cost each (ICT: an entire cascade; conditioning gates: four pre-regs). The definition exists to kill them at admission, for the cost of a paragraph. |
| Widen sourcing without tightening attribution | A wider ontology with the same soft story bar is a HARKing invitation — more surface, same filter. The widen/tighten pairing is the control. |
| Loosen Clause K's cap or family pooling to reopen MNQ/MYM | Methodology-layer p-hacking, and this session banked the K in question — the optics alone disqualify it. The harvest doc's own text ("the bar is a fact about the ledger") stands. §2-C adjudicates what the ledger RECORDS, never what the cap tolerates. |
| Bank declared K always (strict letter) | Creates a perverse incentive to delay pre-registration until certainty (the opposite of the freeze discipline's purpose) and prices an unexecuted declaration identically to a completed search. K measures looks; a campaign that looked at nothing spent nothing. |
| Bank zero for ST-EH-1 (fully unexecuted reading) | The two TV baselines WERE examined (parent session + this one, PF/expectancy read) — banking them is the honest floor. |
| Route all flow ideas through Path 1b instead | 1b demands ≥3 decades / ≥3 cohorts / 10-yr replication — right for anomaly-class patterns, structurally wrong for mandate flows whose persistence argument is the mandate itself, not sample depth. |

---

## §4 — Falsifier (revert trigger)

**H:** constraint-named seeds fail less often and cheaper than story-named seeds; the census sources viable seeds the literature ranks miss; executed-K closure does not get gamed.

**Falsifier — each clause below names the observation on which it is falsified and reverted (a fired trigger falsifies that clause only, not its siblings):**
- **2-A:** if the first **three** four-clause-compliant campaigns all die at Stage-2/Stage-6 with the *constraint-observable confirmed present* (the flow showed up on schedule at claimed size and STILL wasn't harvestable net of costs), the WHO/WHEN clauses are not discriminating — revert 1a to its prior wording by superseding ADR.
- **2-B:** if by the second quarterly audit after ratification the census has produced zero seeds that pass the §3 intake screen, the channel is dead weight — retire the rank (census docs remain as Notice records).
- **2-C:** any instance of a campaign closed under executed-K where a later audit finds an examined read not enumerated in its closure note → the rule is being gamed → revert to declared-K banking for ALL closures, retroactively re-banking every executed-K closure at declared K.

**Trigger check schedule:** rides the programme-audit dates (2026-11-08, 2027-02-08).

---

## §5 — Forbidden moves (under this ADR)

- **Laundering a behavioral story through constraint vocabulary** ("dealers must hedge" without naming the instrument, size driver, and schedule) — the four clauses are each specific; a clause that cannot be written specifically is failing, not pending.
- **Quoting any PnL, edge, or δ inside a census entry** — the census is Notice-phase; the first number comes from a δ-extraction probe or citation under an opened pre-registration, never from the census author "just checking."
- **Using §2-C on a campaign that examined results** — the clause is for stopped-before-looking, and its conditions are auditable; stretching it voids it (§4).
- **Touching Clause K's cap (K_eff ≤ 3), the floor table, or family pooling** — explicitly out of scope here and flagged as the tempting-but-disqualified move this session.
- **Re-opening graveyard classes via census packaging** — month-end from a flow census is still month-end; the registry's new-mechanism-evidence bar binds census entries identically (each entry carries a graveyard-adjacency attestation).
- **Writing an adjacency attestation without executing its searches.** Enforced retrospectively on this ADR's own first census the day it was authored: two entries (LETF rebalance, WMR fix flow) were graded live/"strongest" while already dead by rulings in `docs/briefs/` — the attestations were fields filled, not searches run. An attestation must paste **command output**, searched by **mechanism family** (not instrument), across `rejected_candidates.md` **+ `docs/briefs/**` bar-rulings + closed manifests + `rejected_signals.md`**; bar-rulings do NOT all live in the registry. Without executed output the entry is void.
- **Grading a micro-capacity claim before running the cost-law arithmetic.** Clause 2-A(iii) and Requirement 5 pull in opposite directions for small-δ mechanisms: the littleness that keeps institutions out multiplies fixed per-contract cost against a fixed-size edge (measured: the M6E fix expression is 11.8× over its own break-even, ~4× WORSE than the CFD that was already rejected). Every capacity-niche entry must carry RT-in-δ-units vs the 4× hurdle **before** any comparative grading language.

---

## §6 — Consequences

**Positive:** admission kills narrative seeds at paragraph cost; "lesser-mined" becomes a stated, checkable claim (capacity/awkwardness clause) instead of a hope; sourcing gains a channel whose entries are free until graduated; the ledger gains an honest closure path for stopped campaigns; MYM (0.85) and 6E (0.85) runways stay open under 2-C's first application.

**Negative (real):** 1a gets harder to satisfy — some genuinely good seeds with fuzzy counterparties will route to the slower 1b path or die; census maintenance is ongoing curation work; executed-K closures require enumerated-look bookkeeping that declared-K never needed.

**Risks:** constraint-flow literature is itself a mined channel (LETF rebalance, fix flows are documented) — the capacity clause is the defense, and it may prove optimistic; mitigated by the §4 three-strikes trigger.

**Downstream on ratification:** `strategy_harvest.md` §1 Req 1a text + §2.3 channel row + §5 seed-manifest fields (add the four clauses); `discovery-campaign-template.md` Default #5 note; `register_search.py` gains an `--operator-stopped` closure path (Cursor-eligible mechanical edit); ST-EH-1 manifest closes per 2-C; STATE.md forward board gains the §4 checks.

---

## §7 — Implementation plan

- **Phase 0 — DONE 2026-07-26.** Draft landed `Proposed` with the census Notice doc + the ST-EH-1 closure-note draft.
- **Phase 1 — DONE 2026-07-26.** Operator ratified all three clauses and ruled ST-EH-1 to executed-K banking.
- **Phase 2 — DONE 2026-07-26.** `register_search.py` gained the guarded `--operator-stopped` closure path (implemented in-session rather than via Cursor handoff: ~40 lines on one lab file, needed immediately to execute the ruling; 10 guard tests in `tests/test_register_search_operator_stopped.py`, incl. a regression pinning the normal p-value path byte-unchanged). ST-EH-1 manifest closed at K=2. Downstream doc edits landed: `strategy_harvest.md` (Req 1a four clauses, §2.3 census channel, §5 manifest fields, family-bank snapshot), `discovery-campaign-template.md` (Default #5 constraint-observable note), `STATE.md` forward board.
- **Phase 3** — verification block passes; first §4 check rides 2026-11-08.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Status + amendment references
grep -n "Status:\|Amends-in-part" docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md

# 2. Census is Notice-phase and quotes no PnL (expect zero numeric-PnL hits).
#    Working-tree path was pruned; retrieve then grep (tag is private-archive-only
#    on this public clone — docs/ltm/README.md).
git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md | grep -n "WHO\|WHEN\|WHY\|HOW" | head -5
git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md | grep -niE "pnl|sharpe [0-9]|expectancy \$|delta = [0-9]"

# 3. 2-C's first case closed correctly: banked executed, declared retained, no verdict
python -c "import json; m=json.load(open('discovery_manifests/st_eh_supertrend_grid.json')); print(m['status'], m['K'], m['declared_K'], m['closure_mode'])"
# Expected: closed 2 84 operator-stopped
grep -c "NO campaign verdict exists" discovery_manifests/st_eh_supertrend_grid.json   # expect 1

# 3b. The 2-C path cannot be used to LAUNDER a search (guards are tested, not asserted)
python -m pytest tests/test_register_search_operator_stopped.py -q   # expect 10 passed

# 4. §4 2-C gaming check (run at audits): every executed-K closure enumerates its looks
grep -rln "executed-K" docs/briefs/closures/ 2>/dev/null

# 5. Clause-K cap untouched (expect the cap text unchanged in the harvest doc)
grep -n "K_eff ≤ 3\|K_eff <= 3" docs/methodology/strategy_harvest.md
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md --type adr
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md --type adr

# §0 anchors
git log -1 --format='%h %ci' -- docs/methodology/strategy_harvest.md      # 8690a81
git log -1 --format='%h %ci' -- docs/rejected_candidates.md               # 2fbc996
git log -1 --format='%h %ci' -- core/firm_rules.py                        # fd95c72

# Family-bank arithmetic reproduces from the ledger (closed manifests only)
python -c "
import json, glob
banks = {}
for p in glob.glob('discovery_manifests/*.json'):
    m = json.load(open(p))
    if m['status'] == 'closed':
        print(m['run_id'], m['K'])
"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-26 | Drafted `Proposed` at operator direction (post-ST-EH-1 close): four-clause 1a sharpening, flow-census sourcing channel, executed-K closure rule (ST-EH-1 as first case, manifest held open pending ruling). | Joshua (direction) + Claude Code (Opus 5) |
| 2026-07-26 | **RATIFIED — all three clauses `Accepted`** ("Bank executed K per 2-C, and ratify all three clauses"). Same-session execution: `--operator-stopped` closure path added to `register_search.py` + 10 guard tests; ST-EH-1 closed banking executed K=2 (declared 84 retained); §6 downstream edits landed in `strategy_harvest.md`, `discovery-campaign-template.md`, `STATE.md`. Resulting runways: MNQ floor 0.98 (at cap), MYM / 6E floor 0.85. | Joshua (ratification) |
