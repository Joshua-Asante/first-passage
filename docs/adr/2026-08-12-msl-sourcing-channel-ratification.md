# ADR 2026-08-12 — MSL ratification: sourcing-channel, framing, and Req-scope rulings

**Status:** `Accepted` — operator ratified 2026-08-12 (Board B1); [MSL charter](../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) Status `PROPOSED → RATIFIED` in the same commit (TNEC-1 step-1 pattern). Full tier, compact: ceremony-tiering **limb 4 fires** (this creates standing sourcing doctrine); the earlier light-record framing was a P1 review finding and is withdrawn.
**Decision date:** 2026-08-12
**Note:** drafted this date; ratified same day — three §2 elections marked below. P1 4-lens adversarial review applied pre-ratification.
**Supersedes:** `2026-08-08-edge-cohort-correction-and-necessity-retarget.md` in part — §2-C L2 channel taxonomy **by addition only** (MSL named); nothing else in that ADR moves.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (rulings) + Claude Code (recorder)
**Related:** [MSL charter](../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) · [first slate](../briefs/programs/2026-08-12-msl-first-slate.md) · [program plan](../briefs/programs/2026-08-12-msl-program-plan.md) · [MNQBASE-1 closure](../briefs/closures/MNQBASE-1-closure-intake-dry.md) · [TNEC-1](../spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) · [fade design spec](../superpowers/specs/2026-07-30-tradeify-native-fade-program-design.md) §2.1/§7 · [ceremony tiering](2026-08-08-adr-ceremony-tiering.md)
**Layer:** research-sourcing governance. No locked parameter, allocation, `dd_protection` constant, rail state, Pine, or K ledger is touched. $0 · K=0 · nothing armed.

## §0 — Reads (verified this session at `a77a06e`, 2026-08-12)

`MNQBASE-1-closure-intake-dry.md` (bar's operative sentence quoted in §2) · `2026-08-08-edge-cohort-correction-and-necessity-retarget.md` §2-C L2/L3 · TNEC-1 @ `7e92394` (step 2 sourcing law; N-limbs) · fade spec §2.1 + §7 (both framing precedents) · `docs/rejected_candidates.md` 5th-leg SNAG entry + single-index raised bar · `docs/methodology/strategy_harvest.md` Req 1–5 + Req-3 disclosure rule · `ops/instruments/MYM.md` 2026-08-04 F2 note · `core/firm_rules.py` @ `0356be2`.

## §1 — Context (one paragraph)

Every declared sourcing channel is exhausted at zero admissible seeds (MNQBASE-1 intake-dry; L2 pass zero-yield; 8 consecutive zero-yield closes since 2026-08-08), while the venue clock runs to **2026-11-08** (TNEC-1 FALSIFIED clause). The operator proposes reviving the FXIFY-era manual composition loop as a generation modality. The charter binds it to the existing gate stack; three scope questions are genuinely the operator's, recorded here.

## §2 — Decision (three rulings)

1. **R-CHANNEL.** §2-C L2's ratified channel taxonomy gains **MSL** as a named channel (in-part supersession by addition). The MNQBASE-1 bar's operative sentence is: *"a new sourcing channel (Req 1b-grade published cohort, or a constraint-based WHO not yet enumerated) — not another pass over the same classes… New mechanism evidence does [clear it]."* MSL does not claim either prong by assertion; for MNQ-scoped (MNQBASE-scope) work the bar is cleared per-candidate only under R-REQSCOPE's answer. MNQBASE-1 stays closed (P1–P6, L2 STOP); MNQDTL-1 §3.1 doors C1–C11 stand separately. **Election: ☑ accepted (MSL joins the taxonomy).**
2. **R-FRAMING.** For non-index MSL candidates, the operator rules which precedent governs: the fade spec §2.1 reading (a Tradeify-native survival program sits **outside** the free-data 5th-leg SNAG domain) or §7's adverse-reading-wins clause (*"Choosing the domain framing to clear a gate… if a reviewer thinks a SNAG-domain reading is more honest, that reading wins"*). **Election:** ☑ §2.1 governs (non-index cards proceed, framing recorded per card in the door-check) · ☐ §7 governs (non-index cards need a SNAG route: paid data / new venue class / dated live incident).
3. **R-REQSCOPE.** Whether harvest **Req 1b / Req 2** (published, cohort-cited δ) bind internally-composed candidates. **Election:** ☐ they bind (⇒ every MSL candidate is UNSCREENABLE at Req 2; the channel is stillborn and this ADR closes it honestly) · ☑ they do not bind composition (⇒ MSL candidates enter under the estate's G0/explore-confirm lane discipline — dense-1m precedent — with **Req 1a delete/flip still binding** as the mechanism test, EM0–EM5 + TNEC-1 unchanged).

## §3 — Alternatives considered

Light-record ratification (rejected — limb 4 fires); claiming the MNQBASE bar discharged by MSL's existence (rejected — quote-truncation; the bar's definition is not met by assertion); answering R-FRAMING/R-REQSCOPE editorially in the charter (rejected — both are operator scope rulings; deciding them by authoring is the laundering move the fade spec §7 names).

## §4 — Falsifier / revert

The charter's own Gate line governs: **FALSIFIED(process)** (a card reaches TV without step 2–5 artifacts / out-of-order execution / post-hoc sweep selection) or **FALSIFIED(yield)** (6 consecutive pre-G0 deaths across ≥2 families, or 12 weeks with zero G0 freezes) voids all three rulings pending a superseding ADR. Trigger check: at each plan-B7 weekly walk and at every registry-entry merge (§6 counter).

## §5 — Forbidden moves (genuinely tempting)

Re-running an exhausted channel under the MSL name (the bar's "another pass over the same classes") · answering R-FRAMING per-card by whichever reading admits the card · reading R-REQSCOPE's "does not bind" election as weakening Req 1a, EM0–EM5, or TNEC-1 · citing this ADR as evidence the channel *works* (only the charter's RESOLVED gate can say that, and a kill counts).

## §6 — Consequences

Positive: generation restarts through the full gate stack at $0 marginal governance cost; the stillborn outcome is a legitimate, cheap ruling rather than a discovered failure. Negative: a third standing convention to maintain; the 2026-11-08 clock is unmoved by any of this. Downstream on acceptance: charter Status flip (same commit) · plan §6 manifest row update · SESSIONS entry · `docs/adr/INDEX.md` regenerate.

## §7 — Implementation

Phase 0 ✅ reads + P1 review applied pre-ratification. Phase 1 ✅ operator elections marked in §2, Status flip, same-commit charter flip, **and the in-part supersession edge + reciprocal `Superseded-in-part-by` header + change-history row on the edge-cohort ADR** (A2 discipline). Phase 2: plan B2/B3/B8 unblock per their own rows. Audit hook: `rg -n "R-CHANNEL|R-FRAMING|R-REQSCOPE" docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md docs/adr/2026-08-12-msl-sourcing-channel-ratification.md` — the three ruling names must resolve to identical elections in both files.

| Date | Change | By |
|---|---|---|
| 2026-08-12 | Drafted (light record); escalated to full-tier compact + R-REQSCOPE added after P1 4-lens review (59 findings) | Claude Code |
| 2026-08-12 | **Accepted** — R-CHANNEL ☑ · R-FRAMING ☑ §2.1 · R-REQSCOPE ☑ do-not-bind; charter RATIFIED same commit | Joshua (rulings) + Cursor (recorder) |
