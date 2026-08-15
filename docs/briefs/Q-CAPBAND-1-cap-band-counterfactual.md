# Q-CAPBAND-1 — Has `CAP = 1.0` ever excluded an axis that would otherwise have survived?

**Status:** `OPEN — DRAFT (pre-lock)` — authored 2026-08-15; **execution requires a separate operator GO** (parent-Q convention: naming is not opening)
**Authored:** 2026-08-15
**Closed:** N/A
**Authors:** Joshua (raised the challenge to the 1.83 anchor) + Claude Code (authoring)
**Parent question:** N/A — opened from the [2026-08-03 gate-stack audit](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) §5.4 item 3, which named this as something the audit could **not** establish
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on a locational read of already-recorded gate facts for two named axes
**Artifact path:** `docs/briefs/Q-CAPBAND-1-cap-band-counterfactual.md`
**Pre-registration:** [`pre-registration/Q-CAPBAND-1-verdict-preregistration.md`](pre-registration/Q-CAPBAND-1-verdict-preregistration.md)

---

## §0 — Rule 0 reads (production-source verification, executed 2026-08-15)

- `lab/research_utils/axis_screen.py` — anchor `2ef7405` (2026-08-04). `CAP = 1.0` at `:31`, frozen with `DSR_MIN = 0.95`, `POWER_MIN = 0.50`, `Z = 1.96`; header states *"no CLI/env override — harvest-intake ADR §5"* and *"Cap resolved by Q-GATECART-1 2026-07-14."*
- `lab/archive/q_kbudget_1_2026-07/floor_scan.py` — the frozen axis table. **Executed this session**; verdicts and floors reproduced live: D1 2.05 FAIL · **D2 (1.925, 2.165) FAIL** · D3 (0.85, 0.98) PASS · D4 2.05 FAIL · D5 (0.65, 0.98) PASS · **D6 1.835 FAIL** · D7 (0.65, 0.98) PASS · H-OD-1 (0.85, 0.98) PASS · H-TSMOM-1 0.85 PASS.
- `docs/methodology/lessons/methodology_lessons.md` M-19 (`:883-891`) — the two-anchor rule verbatim: benchmark against *"(a) the best in-house validated edge and (b) the corrected published top-decile net single-strategy Sharpe. **If the floor exceeds both**, the axis is dead."* K-sweep: floor ≤ Aegis needs K ≤ 441; ≤ Guardian K ≤ 33; ≤ typical-corrected-anomaly (~1.0) K ≤ 3. Forbidden move: *"a larger search raises the floor toward the **overfit-suspect zone (SR > 2)**."*
- `docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md` §5.4 item 3 — *"Whether G2's Cap = 1.0 was the right choice… nothing in the record discriminates. Settled by: a campaign whose axis sits in the [1.0, 2.0] band — D6 (1.835) or D2-low (1.925) — being funded and closed on some other authority… No such campaign is planned, so this may remain permanently open."*
- `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` + its two addenda — anchor `102d0aa`. The K-cap addendum's own appended correction relocates the operative bound from the in-house edge to `CAP`, and points here.

---

## §1 — Context & motivation

`CAP = 1.0` is the frozen screen constant that decides how large a search this programme may fund: it admits an axis only when `floor_at_k(K) ≤ 1.0`, i.e. **K ≤ 3** at current constants. It is therefore the single constant standing between "we can pre-specify a handful of hypotheses" and "we can actually search."

Two independent facts make it worth pricing now, and neither is today's inconvenience:

1. **The 2026-08-03 audit recorded it as unresolved**, twelve days before the dryness that prompts this brief, and named the exact evidence that would settle it (D6 / D2-low). It also recorded the honest reason nothing discriminates: *"DISC-CAMP-0 is excluded under both caps and predates the resolution."*
2. **A same-day correction to the channel ADR** established that the reachability argument had been leaning on the wrong anchor — Aegis 1.83, which is cohort-bound, K-undeclared and un-deflated — and that the operative bound is `CAP`, not the in-house edge. That correction relocates the question here.

Standing doctrine tested: M-19's two-anchor reachability rule; the harvest-intake ADR §5 freeze on screen constants; and the `concept-not-constant` discipline (a frozen constant moves only via pre-registration → re-derivation → admitting ADR).

---

## §2 — Prior art / lineage

- **Q-GATECART-1** (closed) — resolved Cap to 1.0 on 2026-07-14. Per the gate-stack audit, resolved *"at the tight end through a documented adversarial workflow that refused to tune it to a downstream screen's convenience."* This brief does **not** re-litigate that reasoning; it asks whether the choice has since **cost** anything measurable.
- **DISC-CAMP-0** (`FALSIFIED`) — the only wide mine actually run. Excluded under **both** candidate Caps, so it cannot discriminate. Its independent finding (6/6 mined candidates net-negative, p = 1.0000) is evidence about wide mining's *yield*, not about Cap's calibration.
- **M-19 / Q-GATECART-1 cartography** — supplies the anchors and the K-sweep. Its own conclusion was a floor-above-ceiling inversion *at the banked K = 3,177*, which says nothing about the [1.0, 2.0] band.
- **Q-BUSTGATE-1 / Q-BUSTGATE-2** — the worked precedent for this brief's *shape*: a frozen constant is interrogated by a **binary locational read** of closed artifacts, with no free tolerance parameter, and both closed leaving the constant byte-unedited. This brief deliberately copies that shape.

---

## §3 — Question (Q-CAPBAND-1)

**Pre-Q gate test (symptom-only rephrase):** "a frozen screen constant excludes every search larger than K = 3; it is unknown whether that exclusion has ever removed an axis that would otherwise have reached a fundable campaign, or whether every excluded axis dies elsewhere anyway." No fix baked in — the question does not mention raising, lowering, or amending Cap.

**Q-CAPBAND-1:** Of the axes `CAP = 1.0` excludes, does at least one clear **every other** admission gate — making Cap the sole blocker of a fundable axis — or does each independently fail a non-Cap gate, making the exclusion costless?

---

## §4 — Falsifiable hypothesis (H-CAPBAND)

**H-CAPBAND:** If **every** Cap-excluded axis in the [1.0, 2.0] band (**D6**, floor 1.835; **D2-low**, floor 1.925) independently fails at least one **non-Cap** gate — Clause-N confirm power ≥ 0.50, cost-law reachability (4× RT at the axis's own venue-legal expression), venue legality at the incumbent, or a live registry/domain bar — then `CAP = 1.0` has cost the programme **nothing measurable**, and it is ratified on evidence rather than on its authoring argument. **Otherwise** — at least one band axis clears every non-Cap gate — then Cap is the **sole** blocker of a fundable axis, the counterfactual the 2026-08-03 audit asked for is priced, and a decision on the band is owed to a superseding ADR.

**Accept H-CAPBAND → `RESOLVED` (Cap vindicated) if:** both D6 and D2-low each fail ≥1 named non-Cap gate.
**Reject H-CAPBAND → `FALSIFIED` (counterfactual priced) if:** ≥1 band axis clears every named non-Cap gate.
**`AMBIGUOUS-HOLD` if:** for both axes, every non-Cap gate is unevaluable from recorded facts without new spend — i.e. the counterfactual cannot be priced at $0, which is itself the audit's "may remain permanently open" branch, now dated.

**A `FALSIFIED` verdict does not raise the Cap.** It prices a counterfactual and hands the operator a decision. This asymmetry is the brief's central discipline — see §5.

---

## §5 — Forbidden moves

- **Editing `CAP` in `axis_screen.py` under this brief.** It is frozen by harvest-intake ADR §5 with no CLI/env override; any change needs its own pre-registration → re-derivation → admitting ADR. This brief has no authority to move it and must not be cited as if it did.
- **Reading `FALSIFIED` as "therefore Cap = 2.0."** The reject branch establishes only that the exclusion is costly. Where the constant belongs — and whether M-19's *"overfit-suspect zone (SR > 2)"* forbidden move forecloses the top of the band — is a separate decision on separate evidence. Ruled out because it is the exact laundering move Q-BUSTGATE-1's §5 pre-forbade in its own domain ("treating the EV-optimum as itself the new ceiling").
- **Substituting a fresh axis for D6 / D2-low.** The band axes are frozen by the 2026-08-03 audit's own naming. Inventing a new, more sympathetic axis today and testing *that* is selecting the evidence after seeing the question — and would additionally charge K.
- **Scoring an axis on its edge.** This brief reads *gate* facts only. Measuring D6's or D2-low's actual edge would open a campaign, spend K, and moot the whole point (the audit's condition was an axis "being funded and closed **on some other authority**").
- **Citing today's channel dryness as evidence for the reject branch.** Dryness motivates asking; it is not evidence about Cap's calibration. Conflating them is degeneration signal #4 (methodology invoked to rationalize a decision already made).
- **Using Aegis 1.83 as a reachability ceiling anywhere in this brief.** Withdrawn same-day as cohort-bound, K-undeclared and un-deflated; M-19's two-anchor rule governs.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | Both D6 and D2-low each fail ≥1 named non-Cap gate | `INTEGRATE` — record Cap 1.0 as **evidence-ratified**, discharge the 2026-08-03 audit §5.4 item 3, and close the band question. No constant moves. |
| `FALSIFIED` | ≥1 band axis clears every named non-Cap gate | `ITERATE` — the counterfactual is priced; name (do not open) a successor decision packet on the band, carrying M-19's SR > 2 forbidden move as a frozen constraint. No constant moves. |
| `AMBIGUOUS-HOLD` | Non-Cap gates unevaluable at $0 for both axes | `ITERATE` — record the audit's "permanently open" branch as **dated and confirmed**; re-test only if a band axis is ever funded on other authority. |

**Pre-registered before any gate fact is read.** §6 is not amended to match what the read returns (Known Trap #12).

---

## §7 — Execution plan (self-executing; closed-artifact read, $0 / K=0)

- **Phase 0 — Rule-0 reads.** Done (§0).
- **Phase 1 — Freeze the axis set.** D6 (floor 1.835), D2-low (1.925), from `floor_scan.py` as executed in §0. No additions.
- **Phase 2 — Per axis, read the non-Cap gates from recorded facts only.** Clause-N power (recorded in `floor_scan.py`'s own `clause_n` field per axis); cost-law reachability at the axis's venue-legal expression (`cost_model.py`, primary-sourced Tradeify commissions); venue legality (`core/firm_rules.py` + the Tradeify supported-products article); live registry/domain bars (`instrument_profiles.py cell`, `rejected_candidates.md`).
- **Phase 3 — Verdict assertion.** Apply §6 mechanically. Produce the closure per §9.

Estimated cost: **$0, K = 0, no manifest.** If any gate turns out to require a measurement, that axis is scored `unevaluable` and routes to `AMBIGUOUS-HOLD` — it is **not** measured under this brief.

---

## §8 — Verdict pre-registration

Frozen decision rule + pinned axis set: [`pre-registration/Q-CAPBAND-1-verdict-preregistration.md`](pre-registration/Q-CAPBAND-1-verdict-preregistration.md), to be committed **before** Phase 2 reads any gate fact.

---

## §9 — Closure record format

Per `references/closure_record.md`, with the mandatory typed `## Iterate` block. `RESOLVED` → `docs/briefs/closures/Q-CAPBAND-1-closure-resolved.md`; `FALSIFIED` → `…-closure-falsified.md`; `AMBIGUOUS-HOLD` → `…-closure-ambiguous-hold.md` with the re-test trigger named.

---

## §10 — Audit hooks (runnable)

```bash
# The Cap is still frozen and byte-unedited by this brief
grep -n "^CAP = " lab/research_utils/axis_screen.py            # expect: CAP = 1.0

# The band axes and their floors reproduce
python -c "import importlib.util as u;s=u.spec_from_file_location('fs','lab/archive/q_kbudget_1_2026-07/floor_scan.py');m=u.module_from_spec(s);s.loader.exec_module(m);print([(r['axis'][:12], r['floor'], r['clause_k']) for r in m.screen()])"
# expect D6 -> 1.835 FAIL, D2 -> (1.925, 2.165) FAIL

# The audit item this discharges is still open (or closed by this brief's closure)
grep -n "Cap = 1.0 was the right choice" docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md

# No campaign was opened under this brief
ls discovery_manifests/ | grep -i capband                       # expect: no match
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-CAPBAND-1-cap-band-counterfactual.md --type inquire
grep -n "^CAP = " lab/research_utils/axis_screen.py
```

---

## Pre-Lock Checklist (DRAFT)

- [x] §0 paths read with anchors, floor scan executed live
- [x] §3 passes the symptom-only rephrase (no "raise the Cap" in the question)
- [x] §4 hypothesis binary (every axis fails ≥1 non-Cap gate, or ≥1 clears all)
- [x] §5 forbidden moves genuinely tempting — the "FALSIFIED ⇒ Cap 2.0" laundering move is the live hazard
- [x] §6 triggers specific and pre-registered
- [ ] §8 pre-registration committed **before** Phase 2 — owed at execution
- [x] §10 hooks runnable
- [ ] **Operator GO owed before Phase 2** — this brief is named, not opened
