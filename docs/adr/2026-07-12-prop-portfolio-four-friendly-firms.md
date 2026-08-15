# ADR 2026-07-12 — Prop-portfolio program: multi-firm ops target the four automation-friendly futures firms

**Status:** Accepted (operator executive decision, recorded)
**Superseded-by:** none
**Retain-until:** none
**Decision date:** 2026-07-12
**Authors:** Joshua (decision) + Cursor Cloud Agent (recorder)
**Supersedes:** `2026-07-10-r6-nogo-futures-residual-disposition.md` in part - R6's locked-book futures-prop fan-out and edge-transfer falsifiers stand; R6's "sole active scale lane = self-funded Aegis->M6J" and "no futures-prop operational target" posture is replaced by this program for multi-firm operations.
**Superseded-in-part-by:** `2026-07-14-prop-portfolio-existing-strategy-candidates.md` - accepted 2026-07-15; candidate-class scoping only (Section 2 R6-boundary sentence + Section 5 bullet 2). Firm set, registry, gating, Section 4 falsifier, and every other clause stand.
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - `ACTIVE_FIRM="FXIFY"` retention/prohibition only. Firm set, registry, envelope scoring, and the §4 falsifier stand.
**Superseded-in-part-by:** `2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` - the §4 discharge status only (Class-S candidate #1's 2026-07-15 result withdrawn on corrected eval-lock geometry). Program, four-firm target set, envelope, and the 2026-11-08 hard date stand unchanged.
**Related:** [`docs/ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md`](../ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md) (eligibility survey); [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) (E1–E7 build envelope); [`docs/notes/2026-07-06-rail-reconciliation-traderspost-vs-crosstrade.md`](../notes/2026-07-06-rail-reconciliation-traderspost-vs-crosstrade.md) (KEEP rail = TV→CrossTrade→NT8); [`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](../ltm/briefs/rnd-pipeline/discovery-campaign-template.md) (Gen-2 discover→admit pipeline); [`docs/adr/2026-06-06-firm-constants-single-source.md`](2026-06-06-firm-constants-single-source.md) (`firm_rules` canonical).
**Layer:** execution + portfolio operations — **not** locked-parameter. No change to the locked four-strategy allocations, `dd_protection` constants, Pine source, or FXIFY MC regression pin.

---

## §0 — Rule-0 reads (production-source verification)

- [`docs/ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md`](../ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md) — content-read 2026-07-12. Four `FRIENDLY` firms under attended-automation bar + CrossTrade/NT8 rail: Bulenox, Tradeify, MyFundedFutures, BluSky Trading.
- [`core/firm_rules.py`](../../core/firm_rules.py) — working-tree read 2026-07-12. Bulenox (5 tiers) + Tradeify Select (4 tiers) already encoded; MFFU + BluSky tiers added by this ADR; `ACTIVE_FIRM = "FXIFY"` unchanged (MC anchor pin).
- [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) — content-read 2026-07-12. Default E1–E7 envelope + §4 per-firm overlays for FRIENDLY/CONDITIONAL firms.
- [`docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md`](2026-07-10-r6-nogo-futures-residual-disposition.md) — content-read 2026-07-12. Locked-book fan-out NO-GO + DJ30→MYM falsification — **not reversed** by this ADR.
- [`core/config/params.toml`](../../core/config/params.toml) — HEAD read 2026-07-12. Locked G/DJ30/A/NAS allocations + `dd_protection` C2 unchanged.

---

## §1 — Context

Q-AUTO-FIRM-1 (2026-07-12) resolved that **four** US futures-prop firms clear the **attended-automation** bar on the **TV→CrossTrade→NT8** rail — materially wider than Q-BTC-3's single-firm lights-out result. R6 (2026-07-10) correctly closed the **locked four-strategy book's** futures-prop fan-out after P2/R5 edge-transfer falsification; it also demoted all futures-prop to NO-GO and named self-funded Aegis→M6J the sole active scale lane.

The operator directive (2026-07-12) reframes **multi-firm operations**: not redeploy the falsified locked book, but **discover, productionalize, and execute new portfolio strategies** engineered to **pass prop challenges and scale allocations** across the four automation-friendly firms. Firm targets and constraints must live in `core/firm_rules.py` as the single reference surface (ADR 2026-06-06).

**Decision driver (one sentence):** eligibility evidence + operator intent now justify a **greenfield prop-portfolio program** at four attended-automation firms, with `firm_rules` as the constraint registry — distinct from the R6-falsified locked-book transfer question.

---

## §2 — Decision

**Multi-firm operations targets challenge-passing and post-pass allocation scaling at the four Q-AUTO-FIRM-1 `FRIENDLY` firms:**

| Firm | `firm_rules` family key | Representative eval tiers (this ADR) |
|---|---|---|
| Bulenox | `bulenox` | `Bulenox_25K` … `Bulenox_250K` (pre-existing) |
| Tradeify | `tradeify` | `Tradeify_Select_25K` … `Tradeify_Select_150K` (pre-existing) |
| MyFundedFutures | `myfundedfutures` | `MFFU_Rapid_50K`, `MFFU_Rapid_100K` (added) |
| BluSky Trading | `blusky` | `BluSky_Premium_50K`, `BluSky_Premium_100K` (added) |

**Operational program (end-to-end):**

1. **Discover** — Gen-2 lab pipeline (`lab/` discovery campaigns). Candidates must declare `DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO` against [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) at closure; portfolio composition is a first-class design target (multi-leg books that pass together, not single-strategy heroics).
2. **Productionalize** — admitted survivors (`CANDIDATE` lifecycle intake per [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md)) through codification → sweep → validation; prop-firm constraints pulled from `firm_rules.FIRM_RULES[<tier>]` + envelope overlays, never hard-coded in research artifacts.
3. **Execute** — attended automation on **TV → CrossTrade → NT8 → Rithmic/Tradovate** per the 2026-07-06 rail note. **Rail build and account registration remain gated** — this ADR sets the *target* and *constraint registry*, not a live-start authorization.

**`firm_rules` registry:** `AUTOMATION_FRIENDLY_PROP_FIRMS` maps each family to its tier keys; all tier dicts carry challenge targets/constraints (profit target, DD type/level, flat posture, contract caps, consistency where applicable). `ACTIVE_FIRM` stays **`FXIFY`** — the 99.83/0.17/4.37 MC anchor remains a historical regression pin, not the live prop target.

**R6 boundary (amended 2026-07-15 — candidate class only):** deploying the **locked** Guardian / Striker DJ30 / Aegis / NAS100 book as a futures-prop fan-out at locked CFD allocations, or on any claim of CFD-edge transfer, is still **NO-GO** (R5/P2 remain FALSIFIED). The program builds prop-envelope portfolios from **either** Gen-2 discovery survivors **or** pre-registered existing-strategy books (native-futures expressions of the locked legs, scored at firm tiers on bust-geometry). Amendment vehicle: [`2026-07-14-prop-portfolio-existing-strategy-candidates.md`](2026-07-14-prop-portfolio-existing-strategy-candidates.md).

**Effective:** immediately upon acceptance (2026-07-12).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Keep R6 posture (self-funded Aegis→M6J sole lane; futures-prop dormant)** | Operator directive explicitly retargets multi-firm ops to prop challenge-passing at the four FRIENDLY firms; leaving R6's ops posture unchanged would orphan Q-AUTO-FIRM-1 and block `firm_rules` as a live constraint surface. |
| **Redeploy the locked four-strategy book to Bulenox/Tradeify** | R6 falsifiers stand (DJ30→MYM 0.559 < 0.8×; NAS100 dead on micros). Firm eligibility ≠ edge-transfer clearance. |
| **Include CONDITIONAL firms (Apex, Topstep, TradeDay, Earn2Trade) in the operational target set** | Q-AUTO-FIRM-1 scored rail mismatch or policy caveats; operator scoped to the four `FRIENDLY` firms only. CONDITIONAL firms remain in envelope §4 for a future expansion ADR. |
| **Skip `firm_rules` encoding; keep constraints only in `prop_envelope_default.md` prose** | Violates ADR 2026-06-06 single-source doctrine; MC/re-MC harnesses and ops tooling need machine-readable tier dicts. |
| **Switch `ACTIVE_FIRM` to a prop firm now** | Would break FXIFY MC anchor byte-reproducibility without a deliberate re-MC + engine pre-flight ADR. Prop tiers are **reference configs**, not the active MC fixture. |

---

## §4 — Falsifier (revert trigger)

**H (program success):** at least one **pre-registered** prop-portfolio candidate (multi-leg or single-leg) achieves **challenge-pass simulation** — bust rate below an operator-pre-registered ceiling on **≥2** of the four `FRIENDLY` firm tiers — under attended-automation + EOD-flat envelope modeling, using `firm_rules` configs, before any live account spend.

**Revert trigger (binary):** by **2026-11-08**, no pre-registered portfolio candidate clears the pass-rate ceiling on **any** `AUTOMATION_FRIENDLY_PROP_FIRMS` tier in a dated lab re-MC → demote this program to **research-only** (firm configs retained as reference; no execution-rail ADR may cite this ADR as live mandate without new pass-rate evidence).

**Secondary trigger (eligibility):** any `FRIENDLY` firm issues a written policy reversal banning attended webhook/EA/semi-auto per Q-AUTO-FIRM-1 §4 falsifier → remove that family from `AUTOMATION_FRIENDLY_PROP_FIRMS` and re-run eligibility for the tier only.

**Revert action:** supersede this ADR; restore R6 sole-lane posture if operator confirms; never edit §2 in place.

**Trigger check schedule:** quarterly — next **2026-08-08**, 2026-11-08 (hard date for primary falsifier), 2027-02-08.

---

## §5 — Forbidden moves (under this ADR)

- **Treating firm eligibility as locked-book edge-transfer clearance** — Q-AUTO-FIRM-1 explicitly forbids this; R6 falsifiers are not vacated.
- **Deploying the locked four-strategy portfolio to prop firms under this ADR at locked CFD allocations, or on any claim of CFD-edge transfer** — still forbidden. A pre-registered book of locked-leg *futures* expressions with per-tier weights is admissible as a scoring candidate per [`2026-07-14-prop-portfolio-existing-strategy-candidates.md`](2026-07-14-prop-portfolio-existing-strategy-candidates.md); locked Pine/SL/TP/ATR and the CFD allocation lock stay immutable.
- **Switching `ACTIVE_FIRM` off FXIFY without a firm-onboarding ADR + re-MC** — breaks engine regression pins.
- **Building the CrossTrade/NT8 rail as an implied consequence of this ADR** — execution rail requires its own gated ADR with parity checklist.
- **Hard-coding firm names or challenge constants in `lab/` research artifacts** — envelope §2 rule; constraints enter via `firm_rules` + §4 overlays at the deployment fork only.
- **Full lights-out / unattended 24h operation** — attended bar only (envelope E6); Q-BTC-3 lights-out framing is superseded for ops targeting, not revived.

---

## §6 — Consequences

**Positive:**
- Single ops target across four firms with a machine-readable constraint registry in `firm_rules`.
- Discover→productionalize→execute path aligned with Gen-2 lab pipeline and prop envelope defaults.
- Clear separation from the R6-falsified locked-book question.

**Negative (real cost):**
- Parallel program surface: prop-portfolio work coexists with parked self-funded lanes until explicitly re-ranked.
- `firm_rules` prop tiers use engine semantics (`trailing`, `trailing_locking`) that require pre-flight before trust-pass re-MC (daily_loss_pct `None` hazard documented in module docstring).
- Rail still unbuilt — program can research and productionalize before execution is possible.

**Downstream artifacts updated by this ADR:**
- `core/firm_rules.py` — `AUTOMATION_FRIENDLY_PROP_FIRMS` + MFFU/BluSky tiers
- `tests/core/test_automation_friendly_prop_firms.py` — registry integrity guard

**Downstream artifacts NOT changed (explicit):**
- `ACTIVE_FIRM`, locked allocations, `dd_protection`, Pine, FXIFY MC pins
- `docs/methodology/strategy_lifecycle.md` go-live gates (rail build still separate)

---

## §7 — Implementation plan

- **Phase 0** — §0 reads verified (this session).
- **Phase 1** — `firm_rules.py`: add `AUTOMATION_FRIENDLY_PROP_FIRMS`, MFFU Rapid 50K/100K, BluSky Premium 50K/100K; refresh module provenance docstring.
- **Phase 2** — ADR (this file) + registry test.
- **Phase 3** — audit hooks §10; status `Accepted`.

---

## §10 — Audit hooks

```bash
# ADR accepted + four-firm target
grep -n "Accepted\|AUTOMATION_FRIENDLY_PROP_FIRMS\|FRIENDLY" docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md

# Registry: four families, all keys in FIRM_RULES
python -c "
from firm_rules import AUTOMATION_FRIENDLY_PROP_FIRMS, FIRM_RULES
assert len(AUTOMATION_FRIENDLY_PROP_FIRMS) == 4
for fam, keys in AUTOMATION_FRIENDLY_PROP_FIRMS.items():
    assert keys, fam
    for k in keys:
        assert k in FIRM_RULES, k
print('OK', list(AUTOMATION_FRIENDLY_PROP_FIRMS))
"

# MC anchor pin untouched
python -c "import firm_rules; assert firm_rules.ACTIVE_FIRM == 'FXIFY'"

# Locked constants untouched
git diff --stat HEAD -- core/config/params.toml core/dd_protection.py core/firm_rules.py | grep -v firm_rules || true
pytest tests/core/test_automation_friendly_prop_firms.py tests/core/test_firm_constants_single_source.py -q
```

**Hook staleness note (2026-07-24).** The "MC anchor pin untouched" hook above
(`assert firm_rules.ACTIVE_FIRM == 'FXIFY'`) **hard-fails as written** since substrate-retirement
Phase 1 (`f8f8db1`, 2026-07-22): `ACTIVE_FIRM` is now `Tradeify_Select_100K` and the historical MC
pin is `FIRM_RULES["FXIFY"]` **by name**, not via the selector. The property the hook was written to
guard is intact — read it as *"the anchor path pins FXIFY by name, not through `ACTIVE_FIRM`."* The
hook line is left unedited so the audit trail of what was originally asserted stays legible. The same
staleness in the **frozen** scoring gate's §10 hook 7 is recorded (and deliberately not edited) in
[`docs/notes/2026-07-24-class-s-scoring-chain-coupling-and-stale-hooks.md`](../notes/2026-07-24-class-s-scoring-chain-coupling-and-stale-hooks.md) §1.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-12 | Initial acceptance | Joshua + Cursor Cloud Agent |
| 2026-07-15 | Superseded in part (candidate class) by existing-strategy-candidates ADR — header + §2 R6-boundary + §5 deploy bullet annotated | Joshua + Cursor |
| 2026-07-24 | §10 hook-3 staleness note added (`ACTIVE_FIRM == 'FXIFY'` hard-fails since substrate Phase 1; property intact, hook line unedited). Non-material — no §2/§4 edit, no decision or status change; the §4 falsifier's status is owned by [`2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](2026-07-22-prop-portfolio-s4-discharge-withdrawal.md). | Claude Code |
| 2026-07-25 | `Superseded-in-part-by` reciprocal added for `2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` (§4 discharge status only). Was invisible to `check_adr_graph.py`'s A2 check — the withdrawal ADR's `Supersedes:` line uses markdown-link citation style, which the edge parser silently dropped rather than flagging; fixed in the same pass (`scripts/check_adr_graph.py`). Non-material header repair — no §2/§4 prose edit. | Claude Code |
