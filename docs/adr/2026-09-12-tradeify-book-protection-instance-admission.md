# ADR 2026-09-12 — Tradeify portfolio protection instance: fixed-instance admission (supersedes-in-part the concept ADR §4 step 2)

**Status:** `PROPOSED` — operator ratification required **before TB-F1** (umbrella D-B11); ratification is recorded as a dated addendum at the foot of this file, never by editing the decision text
**Decision date:** 2026-09-12
**Packet:** TB-P2 of the [Track B umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) (authored 2026-09-12; the ratification date is recorded in the addendum)
**Authors:** Joshua (selection 2026-09-10; D-B11 ruling 2026-09-11) + Claude Code coordinator (drafter)
**Supersedes:** `2026-07-13-dd-protection-concept-not-constant.md` in part — §4 step 2 (the trigger × scale grid run) for the `tradeify_portfolio@Tradeify_Select_100K` instance only; effective on ratification
**Supersedes:** `2026-07-13-dd-protection-concept-not-constant.md` in part — §2 item 2 (the `dd_type` dispatch of `reference_mode`) for that instance only, which records `trailing`; effective on ratification
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** the instance's registry row is retired or superseded
**Related:** [acceptance record](../notes/2026-09-10-tradeify-protection-selection.md) · [campaign record §55/§56](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md) · [ULP rounding](2026-05-10-dd-protection-ulp-rounding.md) · [C2 relock](2026-05-08-dd-trigger-c2-relock.md) · [regime-robustness gate](../methodology/regime_robustness_gate.md) · [TB-R2 read](../notes/2026-09-12-track-b-scaling-faithfulness-read.md)
**Layer:** risk-control governance. **Zero change** to `core/dd_protection.py`, its frozen `DD_TRIGGER` / `DD_SCALE`, `calculate_protection`, `core/dd_geometry.py` or `POLICY_REGISTRY` by this ADR. The registry row itself lands only in **TB-D0** after TB-E1's seal, citing this ADR as ratified.
**Tier:** full (it changes the admission chain for a live-risk instance; light tier is not available).

---

## §0 — Rule 0 reads (verified 2026-09-12 at `origin/main @ c41e2be`)

| Source | Anchor | What it pins |
|---|---|---|
| `core/dd_geometry.py` | `4929c44` | `ProtectionPolicy(reference_mode, trigger, scale, provenance)`; `REFERENCE_MODES = {static, trailing, locking}`; `POLICY_REGISTRY = {}`; rows admitted "only via pre-registration → re-MC → both-halves regime gate → admitting ADR (concept ADR §4)"; `reference_mode_for_dd_type("trailing_locking") == "locking"` |
| `core/dd_protection.py` | `94041d9` | `DD_TRIGGER = 0.015`, `DD_SCALE = 0.40` frozen and import-guarded; `calculate_protection` hard-wired to them with `round(dd, 6) >= DD_TRIGGER`; **cannot evaluate a 1 % trigger** |
| `core/firm_rules.py` `Tradeify_Select_100K` | `d4d1c5e` | `dd_type: trailing_locking`, `max_dd_pct 3.0`, `dd_lock_offset_usd 1_000_000` (the lock is unreachable on the evaluation: the floor is the pure EOD fixed-dollar trail `peak − $3,000`) |
| `ops/c1_rail/book_policy.py` | `bda7a48` | the threaded **candidate** value `ProtectionPolicy("trailing", 0.01, 0.40, "CANDIDATE — unadmitted …")`, `is_protected` = `round((peak − equity)/peak, 6) >= trigger`, `BookProtectionClock` (prior-close mode, EOD peak ratchet, no latch), `frozen_surfaces_untouched()` |
| [Concept ADR](2026-07-13-dd-protection-concept-not-constant.md) §2, §4, §5, Addendum 2026-09-01 | `0e8a5cc` | the invariant (mechanism), the three per-instance variables, the four-step admission chain, "never invent a default instance", the narrowed three-limb gate set |
| [ULP ADR](2026-05-10-dd-protection-ulp-rounding.md) §Decision | `027a729` | six-decimal rounding before the inclusive threshold compare |
| [Acceptance record](../notes/2026-09-10-tradeify-protection-selection.md) | `f1ed626` + alias addendum | the formula, the mode table, prior-close timing, no latch, "unregistered exploratory analysis, not preregistered selection evidence", the private study digests |
| [Campaign record §55](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#55--track-b-release--d-b1d-b15-recorded-2026-09-11) D-B4, D-B11, D-B14; §56 O-1, O-5, O-6 | `origin/main` | K = 1 confirmation of the accepted book; fixed-instance supersession; no policy grid; the per-leg quantity laws |
| [Regime-robustness gate](../methodology/regime_robustness_gate.md) | `origin/main` | mandatory for a new `POLICY_REGISTRY` instance: block bootstrap + half-panel split pinned to the full-panel floor |
| Governing plan §Accepted boundaries, S1/S2 | `3c439f7` | full/H1/H2 ≤ 5 % one-sided 95 % upper failure bound; P(T ≤ 200) lower bound ≥ 0.50; one attempt; no runner-up |

**Cheap falsifier (rev 2 — the first issue quoted a command that fails with `ModuleNotFoundError`; the frozen-surface result had been observed through the test suite, not that command):** `python -c "import sys; sys.path[:0]=['core','ops']; import dd_geometry; from c1_rail import book_policy as b; assert dd_geometry.POLICY_REGISTRY == {}; print(b.frozen_surfaces_untouched())"` → `{'DD_TRIGGER': 0.015, 'DD_SCALE': 0.4, 'registry_empty': True}` (run 2026-09-12 with the corrected import). The candidate is threaded, not admitted.

---

## §1 — Context

The concept ADR admits a protection instance to `POLICY_REGISTRY` only by (1) pre-registering an objective and selection rule, (2) running a trigger × scale grid, (3) passing the both-halves regime gate, (4) freezing the winning row with an admitting ADR. The operator selected the Tradeify portfolio's instance on 2026-09-10 — a 1 % combined-account trigger with 40 % scaling on Aegis / Vanguard / Striker and an ORB response of "base unchanged, adds disabled" — from **unregistered exploratory analysis** (the acceptance record says so in terms), and ruled on 2026-09-11 (D-B4, D-B11) that Track B is a **K = 1 confirmation** of that fixed instance with **no policy grid and no alternative that may win**. A K = 1 confirmation is not step 2. Without a superseding record the admission chain cannot complete for this instance at all, and a `POLICY_REGISTRY` row would be forbidden by the concept ADR §5. This ADR is that record. It keeps steps 1, 3 and 4 intact and replaces step 2 with the operator's selection plus the confirmation evidence that Track B produces.

---

## §2 — Decision

1. **The instance.** Registry key `tradeify_portfolio@Tradeify_Select_100K`; `ProtectionPolicy(reference_mode="trailing", trigger=0.01, scale=0.40, provenance="<this ADR> — ratified <date>; selection 2026-09-10; TB-E1 seal <digest>")`. `trailing` is the geometry of the selection formula (drawdown against the account's own **running EOD equity peak**); the tier's `dd_type` maps to `locking` in `reference_mode_for_dd_type`, and the evaluation's lock offset is unreachable, so the locking geometry degenerates to trailing for this instance. **The row records `trailing`.** Because the concept ADR §2 item 2 says `reference_mode` is "dispatched from `firm_rules` `dd_type`", and that dispatch would yield `locking`, **this ADR also supersedes-in-part the concept ADR §2 item 2 for this instance only** (rev 3): the instance's `reference_mode` is fixed by this record, not dispatched, and TB-D0's admission test asserts that no code path resolves this instance through `reference_mode_for_dd_type` (the helper itself is unchanged for every other tier). If a future tier change makes the lock reachable, the instance is re-admitted, never edited.
2. **The mechanism is the concept ADR's invariant, with one recorded per-leg response map.** Trigger compare with six-decimal rounding, inclusive (ULP ADR); mode for weekday D computed once from the prior settled close (no intraday change, no latch, clears when the drawdown falls below the trigger); the scale **multiplies** normal exposure and compounds with the lifecycle haircut before the integer floor; frozen constants untouched. The per-leg response to the fired instance is a property of the book, recorded here because the concept's "single tier, one factor" invariant does not by itself say what one factor means for four legs: Aegis (fixed 8 → 3), Vanguard (quantity-floor → 0, accepted D-B10), Striker (risk-scaled ladder, O-5 law B; adds from executed base, O-6), **ORB: base unchanged at one micro, adds not placed while protected** (the operator's selection; a mode response, not a multiplier). The map lives in `book_policy.BOOK_LEGS` / TB-S1; the registry row carries the three variables only.
3. **Step 2 of the concept ADR §4 is superseded for this instance by the operator's fixed selection.** No trigger × scale grid is run; no alternative cell may be evaluated or promoted (D-B4, D-B11); a failed confirmation ends the attempt with **no admission** and does not reopen the policy choice.
4. **Steps 1, 3 and 4 are retained and mapped onto Track B:**
   - *Step 1 — pre-registration:* TB-P1 drafts and **TB-F1 freezes** the K = 1 confirmation contract (objective = confirm the fixed instance clears the plan's four acceptance conditions at least sizing intervention; selection rule = none, K = 1; the gate below) **before** TB-E1 runs.
   - *Step 3 — regime-robustness gate, retained in full for the single fixed candidate (rev 2):* **Part B** (half-panel split) is the plan's **H1 and H2 limbs** — each a one-sided 95 % upper failure bound ≤ 5 % on the chronological half — pinned to the full-panel limb; **Part A** (block bootstrap) is retained as its own outer test: 100 alternate-history panels built from **6-month contiguous blocks** of the replay's session series, each replayed at the fixed instance, and the **5th percentile of the per-panel pass-rate distribution must be ≥ the full-panel pass-rate floor** (floor = 0.95, i.e. one minus the 5 % failure ceiling, on per-panel point estimates). Because every path is a continuous replay, the per-panel path count is a frozen field sized to the compute budget (`OWED-BY: TB-F1`); **that reduced per-panel depth is the one amendment to step 3 this ADR asks the operator to ratify**, and it is a reduction in depth, not a removal of the test. **Part A runs once, inside TB-E1, on the n2 stream, and its result is the retained admission evidence; it is not rerun on n3.** TB-E2 evaluates exactly the plan's four n3 conditions (the three failure limbs, of which H1/H2 are Part B, and the speed limb) on the fresh n3 stream; no second bootstrap workload or stream is consumed there.
   - *Step 4 — freeze, admitting ADR and the two-stage admission (rev 2):* TB-E1's sealed **fixed-book replay fingerprint** freezes the row's provenance. **TB-D0 = executable admission:** after TB-E1 passes (legality screen, n1 cutoff, n2 with its H1/H2 limbs and Part A) TB-D0 lands exactly this row with `provenance` naming this ADR and the seal digest, before the Phase 8 live test, so the executable tested, sealed at B7 and used by n3 already carries the final row (umbrella D-B11; the D0-before-B7 order is preserved). Between TB-D0 and TB-E2 the row is admitted **for the Phase 8 dry-run window and the B7 seal only**: `dry_run=true`, `armed_until` unset, no arm (D-B15). **TB-E2 = deployment qualification:** the sole n3 must pass all four conditions (Part B included; Part A's TB-E1 result is retained); only then may TB-D2 request the deployment GO. **Host-visible interlock (rev 3):** `c1_rail_arm.py --arm` refuses unless (i) the admitted row equals the sealed cell **and** (ii) a **deployment-GO artifact** baked into the image — `docs/notes/rail_build/DEPLOYMENT_GO.json`, written only by TB-D2 after a passed n3 and the operator's GO, carrying the n3 result digest, the B7 seal digest and `valid_until` — validates, in the same way the M1 acceptance JSON is baked in and validated today. No such artifact exists before TB-D2, so no arm is possible in the TB-D0 → TB-E2 window without any repository-side marker. **On a failed n3 the row is retired:** the closure record supersedes this ADR, a follow-up commit removes the row from `POLICY_REGISTRY`, and **removal plus redeployment precede any later arm** (a deployed image cannot observe a repository record; the absent GO artifact is what keeps it disarmed meanwhile). Owners: TB-D2 (artifact + validator, extending `validate_c1_monitoring_acceptance`'s pattern), TB-I3 (the interlock, offline-testable: arm refused on a missing, invalid or mismatched artifact).
5. **Evidence class stated honestly.** The selection evidence (`dd-orb-base-only-2026-09-10`, private digests in the acceptance record) is unregistered exploratory analysis and is cited as provenance only; it is not confirmation evidence and no figure from it is quoted. Confirmation evidence is TB-E1 (screen, n1, n2) and TB-E2 (sole n3) on the frozen contract, numbers private per D-B12.

**Effective:** on the operator's dated ratification addendum. Until then this ADR authorizes nothing and `POLICY_REGISTRY` stays empty.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Run the concept ADR's trigger × scale grid on the Tradeify portfolio and let the grid pick | Contradicts D-B4/D-B11 (K = 1, no grid, no alternative may win); re-opens a selection the operator has closed; adds K the campaign did not budget |
| Admit the row now, from the selection evidence | Forbidden by the concept ADR §4/§5 and `dd_geometry.py` lines 88–91; the evidence is unregistered exploratory analysis |
| Express the 1 % / 40 % instance by editing `DD_TRIGGER` / `DD_SCALE` or `calculate_protection` | Breaks the AST lock gates and the MVD self-check; the frozen FXIFY-C2 literals are historical record, not this instance |
| Treat the H1/H2 limbs as unrelated to the regime gate and run a separate 6-month-block bootstrap | Duplicates the campaign's frozen block family with a second, unfrozen one; the gate's two parts are already present in the contract and are pinned to the same full-panel floor |
| Record `reference_mode="locking"` because the tier's `dd_type` is `trailing_locking` | The evaluation's lock is unreachable (`dd_lock_offset_usd 1_000_000`); the selection formula is a running-peak trailing compare; recording `locking` would misdescribe the executable and mismatch `book_policy` |

---

## §4 — Falsifier (revert trigger)

**H (binary):** *the fixed instance `(trailing, 0.01, 0.40)` with the §2.2 response map, confirmed on the frozen K = 1 contract, clears all four acceptance conditions (full/H1/H2 failure bounds ≤ 5 %, P(T ≤ 200) lower bound ≥ 0.50) on the sole n3.*

**Reject (FALSIFIED) if** any acceptance bound fails on TB-E1 or TB-E2 — no admission, no grid, no second cell; the attempt ends. **Accept (RESOLVED) if** all four conditions pass on the sole n3 and TB-D0 lands the row citing this ADR's ratification and the TB-E1 seal. **AMBIGUOUS** only if a frozen field is found unfreezable after TB-F1 — then the attempt closes and any successor needs a new operator decision.

| # | Trigger | Threshold | Action |
|---|---|---|---|
| R1a | TB-E1's legality screen, n1 cutoff, n2 bound or Part A fails | one failed bound | **No admission.** TB-D0 does not land; the attempt ends with no qualifying configuration (D-B4, D33); this ADR is superseded by the closure record; no grid, runner-up or second sample |
| R1b | TB-E2's sole n3 fails any of the four acceptance conditions (Part B included) after TB-D0 has landed | one failed bound | **Row retired.** The closure record supersedes this ADR; a follow-up commit removes the row from `POLICY_REGISTRY` and the image is redeployed before any later arm; no deployment-GO artifact is ever written, so `c1_rail_arm.py --arm` stays refused meanwhile; no grid, no runner-up |
| R2 | A `POLICY_REGISTRY` row for this instance appears before TB-E1's seal, or with a `provenance` that does not name this ADR's ratification and the seal digest | any such row | **Revert the row** (`git revert`), record the deviation in the campaign record; the umbrella §10 registry hook is the mechanical check |
| R3 | `DD_TRIGGER`, `DD_SCALE`, `calculate_protection` or the `_validate_protection_rule` pins change on any Track B branch | any diff | **Revert**; the instance is a registry row and a threaded value, never an edit to the frozen surface |
| R4 | The evaluation's lock becomes reachable (tier rule change) or `book_policy` and the registry disagree on `reference_mode` | mismatch | **Halt** the live path (`c1_rail_arm.py` refuses on a row mismatch); re-admit under a fresh ADR |

**Revert action:** never edit this ADR's decision text; supersede it.
**Trigger check schedule:** R1 at TB-E1 and TB-E2; R2/R3 on every Track B PR (umbrella §10 hooks); R4 at every Tradeify rule re-verification (STATE's 2026-10-11 prop-envelope row) and at TB-D0.

---

## §5 — Forbidden moves (under this ADR)

- Running a trigger × scale grid, a second cell, or any policy comparison inside Track B.
- Landing the registry row before TB-E1's seal, or from a branch other than TB-D0's.
- Editing `core/dd_protection.py`; rebinding `DD_TRIGGER` / `DD_SCALE`; changing `core/dd_geometry.py`'s geometry semantics (`ProtectionPolicy`, `REFERENCE_MODES`, `reference_mode_for_dd_type`). **Permitted, and only in TB-D0:** the one-line addition of this instance's row to `POLICY_REGISTRY` with its `provenance` string.
- Quoting a number from the private selection study as confirmation evidence, or publishing any bound, curve or replay statistic (D-B12).
- Treating a withheld or pending ratification as a technical verdict; it is `BLOCKED — context-problem` for TB-F1.
- Substituting `locking` for `trailing` (or the reverse) in the row on the strength of `reference_mode_for_dd_type` alone.

---

## §6 — Consequences

**Positive:** the concept ADR's admission chain is executable for a K = 1 confirmation without pretending a grid was run; the row's provenance names the exact evidence and seal; the replay, Phase 8 and n3 share one executable policy fingerprint (D-B11); the frozen FXIFY-C2 literals stay historical record.
**Costs / limits:** the instance rides on unregistered exploratory selection evidence, stated plainly; a failed confirmation ends the attempt rather than searching; the per-leg response map is a book property outside the three registry variables, so a future second book at this tier needs its own map and its own admission.
**Obligations created:** TB-P1/TB-F1 pre-register the objective and gate above verbatim; TB-D0 lands the row with the non-vacuous governance-chain test; TB-S1 records the response map; STATE's decision index gains the ratification row when the operator ratifies. **Correction owner for the as-built policy code (rev 3):** `ops/c1_rail/book_policy.py` still implements law A for Striker (it scales the already-rounded normal base and add independently; its committed test pins the protected cap at `(8, 22)`) and lets Vanguard place one contract at WATCH-1; the ruled laws (§56: law B ladder recomputation, `floor(executed_base × 250%)` with the protected ceiling `(22, 55)`, Vanguard zero at every WATCH tier) are implemented by **TB-I1**, whose footprint is extended to `ops/c1_rail/book_policy.py`, `tests/ops/test_book_policy.py` and `tests/ops/test_book_adapters_parity.py` (the coordinator amends the umbrella manifest row); **gate:** TB-I2 may not consume, and TB-E1 may not seal, evidence produced with `book_policy` at the pre-ruling laws — the seal's fingerprint includes `book_policy.py`'s digest and a test pins `(22, 55)` at the protected Striker cap and `0` for Vanguard at WATCH-1.
**Verdict vocabulary:** this ADR's gate is the §4 one — RESOLVED on a passing sole n3 with the row admitted, FALSIFIED on any failed bound, AMBIGUOUS on an unfreezable field; a withheld ratification is `BLOCKED — context-problem` for TB-F1, not a verdict.

---

## §10 — Audit hooks (runnable)

```bash
# Registry still empty until TB-D0 (expected: True)
python -c "import sys; sys.path.insert(0,'core'); import dd_geometry; print(dd_geometry.POLICY_REGISTRY == {})"
# Frozen constants untouched on this branch (expected: no lines, exit=1)
git diff origin/main -- core/dd_protection.py | grep -E "^[+-].*(DD_TRIGGER|DD_SCALE)\s*=" ; echo "exit=$?"
# The candidate is threaded, not admitted (expected: registry_empty True, 0.015 / 0.4)
python -c "import sys; sys.path[:0]=['core','ops']; from c1_rail import book_policy as b; print(b.frozen_surfaces_untouched())"
# Well-formedness
python scripts/check_brief.py docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md --type adr
python scripts/check_adr_graph.py
# Ratification present before TB-F1 (expected after ratification: one line)
grep -n "^## Addendum .* ratification" docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md
```

---

## Change history

- 2026-09-12 — authored (TB-P2), `PROPOSED`; ratification owed before TB-F1.
- 2026-09-12 (rev 3) — second Codex round on #361 folded: host-visible deployment-GO artifact as the failed-n3 interlock (owners TB-D2 / TB-I3) with removal + redeployment before any later arm; Part A runs once in TB-E1 and is retained (not rerun on n3); the concept ADR §2 item 2 dispatch rule enters the supersession scope for this instance; the supersession is encoded in the recognized header field with the reciprocal edge on the concept ADR; TB-I1 named as the correction owner for `book_policy`'s pre-ruling laws with a seal gate.
- 2026-09-12 (rev 2) — Codex review on #361 folded: two-stage admission (TB-D0 executable admission on TB-E1; TB-E2 deployment qualification; row retired on a failed n3), step 3 retained in full with Part A's per-panel depth as the one ratified amendment, the TB-D0 registry-row edit permitted, the audit command's import corrected and the §0 claim restated honestly.
