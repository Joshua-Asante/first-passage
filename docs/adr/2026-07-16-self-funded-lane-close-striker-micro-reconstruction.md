# ADR 2026-07-16 — Self-funded scale lane CLOSED (parked); Striker→MYM/MNQ venue-native reconstruction is the active research lane

**Status:** Accepted (operator executive decision, recorded)
**Superseded-by:** none
**Superseded-in-part-by:** [`2026-07-31-orb-mnq-unpark-payability-target.md`](2026-07-31-orb-mnq-unpark-payability-target.md) — the 2026-07-24 Addendum's `TERMINAL` clause **only as it applies to Candidate B (ORB-MNQ)**, which is unparked to active research under a payable-Tradeify-leg target. Candidate A (MYM ORC) stays CLOSED; R5/P2 stay FALSIFIED; the c1-execution-quality research interest is unaffected.
**Retain-until:** none
**Decision date:** 2026-07-16
**Authors:** Joshua (decision) + Cursor (recorder)
**Supersedes:** `2026-07-10-r6-nogo-futures-residual-disposition.md` in part - R6's "sole active scale lane = self-funded Aegis->M6J" clause only. R6's locked-book futures-prop fan-out NO-GO, R5/P2 falsifiers, and rail-dormancy stand.
**Related:** R5 DJ30→MYM prototype FALSIFIED ([`lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md`](../../lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md)); P2 as-mapped MNQ/MYM FALSIFIED ([`docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md`](2026-07-03-hardcore-p2-edge-transfer-gate.md)); Aegis→6J panel of record ([`ops/instruments/6J.md`](../../ops/instruments/6J.md)); Phase-A micro floors ([`lab/analysis/legacy/futures_conversion_2026-07-01/RESULTS_phaseA.md`](../../lab/analysis/legacy/futures_conversion_2026-07-01/RESULTS_phaseA.md)).
**Layer:** execution + portfolio research priority — **not** locked-parameter. No change to locked CFD allocations, `dd_protection` constants, FXIFY MC pins, or the locked Striker/Guardian/Aegis Pine sources.

---

## §0 — Rule 0 reads (production-source verification)

Venue/scale-path + research-priority decision. §0 proves no locked risk constant is edited and anchors the spent transfer falsifiers this reconstruction must **not** re-litigate.

- [`docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md`](2026-07-10-r6-nogo-futures-residual-disposition.md) — anchor `fad8984`. §2.2 names self-funded Aegis→M6J as sole active scale lane; §2.1 futures-prop NO-GO for the locked book.
- [`docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) — anchor `936a9e0`. Prop-portfolio program at four FRIENDLY firms; rail/account/live-spend gated; R5/P2 not reopened.
- [`docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md`](2026-07-14-prop-portfolio-existing-strategy-candidates.md) — anchor `507761a`. Class-S admits native-futures *expressions* of locked legs with **immutable** locked Pine; claim = bust-geometry, not CFD-edge preservation.
- [`lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md`](../../lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md) — anchor `fad8984`. R5 Stage-1 NOT CLEARED — OOS PF ratio **0.559 < 0.8×**; miss attributed to structural venue costs; recovery "would require entry-signal changes" (out of locked-transfer scope).
- [`docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md`](2026-07-03-hardcore-p2-edge-transfer-gate.md) — Addendum (2026-07-06). NAS100→MNQ K2-kill + E1 miss; DJ30→MYM E1 miss under locked Pine unchanged.
- [`ops/instruments/6J.md`](../../ops/instruments/6J.md) — anchor `e428f0e`. Aegis→6J J1 panel: PF 2.318 / +0.218R / ~50% venue haircut — real transfer numbers, still not a live mandate.
- [`core/config/params.toml`](../../core/config/params.toml) — anchor `784a9ab`. Locked G/DJ30/A/NAS allocations + `dd_protection` C2 — **unchanged** by this ADR.

**Cheap falsifier (pre-author, this session):** repo-wide ADR grep finds **no** prior ADR that closes the self-funded lane; R6 + four-firms posture still name Aegis→M6J as active/parallel. Reconstruction is therefore a fresh operator posture flip, not a duplicate record.

---

## §1 — Context

R6 (2026-07-10) closed futures-prop fan-out of the **locked** book after P2/R5 edge-transfer falsification and named self-funded Aegis→M6J the sole active scale lane. The four-firms ADR (2026-07-12) reopened a **prop-portfolio** research/ops program without reversing those falsifiers. Class-S (2026-07-15) admitted scoring locked-leg **native-futures expressions** (Pine immutable) on bust-geometry — a different claim from CFD-edge preservation.

Operator directive 2026-07-16: **self-funded is closed as a lane for now**, and research should **reconstruct the Strikers to fit MYM and MNQ**. That reconstruction is exactly the path R5 named as out-of-scope for the spent locked-transfer gate ("entry-signal changes… a different strategy"). It is **not** a re-run of R5/P2 under locked CFD Pine, and it is **not** Class-S as currently scoped (Class-S forbids touching locked Pine).

Aegis→6J retains measured panel evidence (~50% haircut, PF 2.318) but is no longer authorized as an active go-live / scale lane. Guardian-MGC remains parked (unchanged).

**Decision driver (one sentence):** the operator closes the remaining self-funded scale authorization and redirects research effort into venue-native Striker editions for MYM/MNQ — the only path that can answer the cost/force-flat wall without re-litigating spent locked-transfer gates.

---

## §2 — Decision

1. **Self-funded scale lane = CLOSED (parked).** Effective immediately:
   - **Aegis→M6J** is **PARKED** (not killed). Panel/ledger artifacts ([`ops/instruments/6J.md`](../../ops/instruments/6J.md), `lab/analysis/aegis/aegis_6j_transfer_2026-07-05/`) remain provenance. No go-live authorization, no live capital allocation, no rail build *for this lane* may cite R6 §2.2 or this ADR's predecessor posture.
   - **Guardian-MGC (R7)** remains **PARKED** (unchanged from R6).
   - There is **no active self-funded scale lane**. Live automated execution remains nowhere; the standing research/ops program is the **prop-portfolio** track (four FRIENDLY firms), still gated on rail/account/live spend.

2. **Active research priority — Striker→MYM / Striker→MNQ venue-native reconstruction.** Under the prop-portfolio program, authorize a research lane to design **new** Striker-family candidate editions engineered for CME micro microstructure (commission, tick value, integer sizing, EOD force-flat / session calendar, roll seams), using operator-supplied BAR EXPORT panels where available. Survivors that clear a **pre-registered** gate may later enter Class-S-style firm-tier scoring or lifecycle intake — **as new candidates**, not as locked-Pine transfers.

**Claim this research is allowed to make:** a venue-native Striker edition can clear a pre-registered profitability / robustness / (later) prop-bust-geometry gate on MYM and/or MNQ under realistic costs.

**Claim this research is forbidden to make:** that R5/P2 were wrong, or that locked CFD Pine "really" preserves ≥0.8× edge on micros.

**Effective:** immediately upon acceptance (2026-07-16).
**Scope:** scale-path posture + research priority. Locked CFD book, MC pins, and locked Pine sources are **untouched**.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Keep Aegis→M6J as active self-funded lane; reconstruct Strikers in parallel** | Operator explicitly closed self-funded "for now." Leaving the lane "active" without go-live intent recreates the R6 single-lane fiction after the operator withdrew it. |
| **Kill Aegis→M6J / delete panels** | Evidence is real (~50% haircut, PF 2.318); kill would discard measured transfer numbers. Park preserves re-open under §4 without re-deriving the panel. |
| **Re-run R5/P2 locked-Pine transfer on a shifted exit grid** | Spent one-shots; R5 already named free levers as insufficient; Trap-12 / R6 §5. Reconstruction exists *because* locked transfer failed. |
| **Treat reconstruction as Class-S with locked Pine immutable** | Class-S cannot change entry/exit; R5's structural diagnosis requires entry-signal / hold-structure changes. Class-S stays available for scoring *finished* native editions; it is not the rebuild method. |
| **Redeploy locked four-strategy CFD book to FRIENDLY firms** | Still NO-GO under R6 + four-firms R6-boundary; unchanged. |
| **Status quo (no ADR)** | Leaves CLAUDE.md/STATE claiming an active self-funded lane the operator has closed — source-of-truth fracture. |

---

## §4 — Falsifier (revert trigger)

**H (posture holds):** through **2026-11-08**, no operator GO re-opens a self-funded scale lane, AND the Striker reconstruction lane either (a) produces at least one **pre-registered** dated RESULTS artifact with a binary gate verdict, or (b) is explicitly closed FALSIFIED/NO-GO by operator with a closure brief.

**Revert triggers (binary, either limb):**

1. **Self-funded re-open:** operator issues a dated GO for Aegis→M6J (or Guardian-MGC, or any new self-funded lane) with a fresh venue/parity checklist → supersede this ADR's §2.1; park→active is a **new** ADR, never an in-place edit.
2. **Reconstruction idle / spent without artifact:** by **2026-11-08**, no pre-registered reconstruction gate has been run **and** no operator closure brief exists → demote §2.2 to **dormant research intent** (no active-lane claim in CLAUDE.md); reopen requires a fresh pre-registration, not a quiet resume.

**Early-fail (reconstruction content):** if the first pre-registered MYM or MNQ reconstruction candidate fails its own pre-registered gate on **all** declared limbs, a second candidate on that instrument requires fresh operator authorization (no variant-grind through the gate — same discipline as Class-S early-fail).

**Revert action:** supersede with a fresh ADR; never edit §2/§4 in place. Verdict vocabulary for the trigger check: **HOLDS** | **REVERTED** (limb-1 or limb-2 fired) | **AMBIGUOUS** (progress by 08-08 without either limb clear — continue, do not silently demote before 11-08).

**Trigger check schedule:** **2026-08-08** progress check (rides quarterly); **2026-11-08** hard date (aligns with prop-portfolio §4).

---

## §5 — Forbidden moves (under this ADR)

- **Re-running R5 B2 or P2 E1/K2 on locked CFD Pine to "rescue" micros** — spent; reconstruction is the authorized path.
- **Citing MYM/MNQ absolute PF ≈ 2 as proof P2/R5 were wrong** — those gates measured *ratio-to-CFD* / signal-set divergence under locked Pine; they stay FALSIFIED.
- **Editing locked Striker DJ30 v4.5 / NAS100 v1 Pine (or their CFD risk%/pyramid locks) "in place"** — reconstruction lands as **new candidate** artifacts (gitignored + hash-pinned per public-clone posture), never as silent edits to locked sources.
- **Treating this ADR as rail-build, account-registration, or live-spend authorization** — prop-portfolio gating unchanged; no live automated execution.
- **Silently un-parking Aegis→M6J because reconstruction is slow** — discomfort is not a GO; §4 limb-1 is the only re-open path.
- **Skipping pre-registration because "we already know Striker works on CFD"** — CFD edge is not the claim; venue-native editions need their own frozen gates before scoring.

---

## §6 — Consequences

**Positive consequences:**
- CLAUDE.md / STATE posture match the operator's closed self-funded intent (no phantom active lane).
- Research priority is explicit: rebuild Strikers for MYM/MNQ microstructure instead of re-litigating locked transfer.
- Preserves Aegis→6J / Guardian-MGC evidence under park (zero-cost optionality).

**Negative consequences (real cost):**
- **No active scale lane of any kind** until reconstruction (or another program) clears gates and a separate go-live ADR fires — longer go-dark period than R6 already accepted.
- Reconstruction consumes research budget that could have gone to Gen-2 discovery or Class-S Aegis-bearing books.

**Risks:**
- Reconstruction may fail the same structural wall (force-flat + commission) even with entry redesign — disposition would be **FALSIFIED** under the candidate's own pre-reg, not an R5 re-litigation. **Mitigation:** pre-register cost-law + force-flat limbs first; bar-export ATR floors already provisional in Phase A.
- Scope creep into locked-parameter edits. **Mitigation:** §5 + candidate-Pine discipline.
- Progress by 08-08 without a RESULTS artifact is **AMBIGUOUS** (continue to 11-08 idle limb); do not treat ambiguity as authorization to skip pre-registration.

**Downstream artifacts that need updating (this session):**
- `CLAUDE.md` — Live-execution posture pointer: self-funded closed/parked; Striker micro-reconstruction active research; link this ADR.
- `STATE.md` — executed-decisions pointer + dormant Aegis→M6J / open reconstruction line.
- R6 ADR header — add `Superseded in part by` this ADR (sole-lane clause only).
- `docs/SESSIONS.md` — session entry.

---

## §7 — Implementation plan

- **Phase 0** — this session: ADR + posture pointer sweep (§6).
- **Phase 1** — operator lands / points BAR EXPORT (or continuous) panels for MYM1! / MNQ1! (and proxies YM1!/NQ1! if used); parse via `scripts/parse_bar_export.py` into lab-local gitignored paths; refresh Phase-A floors with recent-window ATR if deploy-relevant.
- **Phase 2** — author a Pre-Q / pre-registration for the first reconstruction candidate (mechanism claim, cost-law, force-flat limb, OOS split, forbidden moves) **before** any Pine parameter search.
- **Phase 3** — build candidate Pine + score against the frozen gate; disposition via RESULTS + optional Class-S firm-tier intake if PASS.

Policy + Phase 0 mechanical edits are in-scope for acceptance; Phases 1–3 are forward work gated on operator data + pre-reg.

---

## §10 — Audit hooks (runnable)

```bash
# Posture: CLAUDE.md must not claim Aegis→M6J as sole/active scale lane
rg -n "Aegis→M6J|sole active|self-funded" CLAUDE.md | head -40
# Expected: parked/closed language + pointer to this ADR; no "sole active lane = Aegis→M6J"

# R6 supersede chain
rg -n "Superseded in part by|2026-07-16-self-funded" docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md

# Locked params untouched
git diff -- core/config/params.toml core/dd_protection.py core/firm_rules.py
# Expected: empty for this ADR's commit set (unless unrelated)

# Reconstruction idle check (2026-11-08)
ls lab/analysis/*striker*mym* lab/analysis/*striker*mnq* docs/briefs/*striker*recon* 2>/dev/null | head
# Expected by 11-08: dated RESULTS or operator closure brief

# Quarterly reminder
# 2026-08-08 progress; 2026-11-08 hard date (shared with prop-portfolio §4)
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md --type adr
# Expected: mechanical discipline checks PASS
```

---

## Addendum (2026-07-24, operator ruling — chat) — reconstruction tracks TERMINAL; research posture shifts to c1 execution quality

Both authorized tracks have reached terminal dispositions: **Candidate A (MYM
opening-range continuation)** — `S-MYM-ORC-01` CLOSED-AMBIGUOUS and `S-MYM-ORC-02`
CLOSED-FALSIFIED at development (2026-07-16; any ORC #3 was already gated on a fresh
operator GO that has not been given); **Candidate B (ORB-MNQ)** — admitted lifecycle
`CANDIDATE @ 1.00×` (2026-07-16) then **PARKED** by operator directive #6 (2026-07-23
08-08 posture; standing unchanged, no 08-08 compose/rail/decay must-decide). On
2026-07-24 the operator ruled (chat, Algorithm repo review ruling #8): **"MYM and MNQ
are terminal, and we are still open to improving execution (better fills and exits)."**

Effect: the *reconstruction lane* this ADR authorized as active research is **no longer
the active research priority**; the standing research interest under the prop-portfolio
program is **execution quality on the live c1 rail (fills and exits)** — e.g. entry/exit
microstructure, slippage, and order-type work on the MYM/MNQ c1 legs — not new
reconstruction candidates. Nothing else moves: R5/P2 stay FALSIFIED; ORB-MNQ's
CANDIDATE standing and its open decay-monitor manifest obligation are unchanged; the
prop-portfolio §4 falsifier dates (08-08 progress / 11-08 hard) are program-level and
unaffected; a reconstruction re-open requires a fresh operator GO + pre-registration,
not a revert of this addendum. Provenance: the ruling is recorded in
`docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md` §Rulings.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Initial authoring + acceptance (operator: self-funded closed; Striker MYM/MNQ reconstruction active research) | Joshua + Cursor |
| 2026-07-24 | Addendum — reconstruction tracks TERMINAL (operator ruling #8, Algorithm repo review); research posture = c1 execution quality (fills/exits); CLAUDE.md/STATE.md pointer lines synced same commit | Joshua (chat ruling) + Claude Code |
