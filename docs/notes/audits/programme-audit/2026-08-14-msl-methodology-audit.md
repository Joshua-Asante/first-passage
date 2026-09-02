# Audit Note — MSL (Manual Sourcing Loop) methodology audit

**Audit ID:** AUDIT-2026-08-14-msl-methodology
**Date:** 2026-08-14 · **Window:** 2026-08-12 (charter RATIFIED) → 2026-08-14 (this session) — MSL's entire life to date, 2 calendar days
**Triggered by:** degeneration signal #5 (SNAG pattern) — MSL's own track record is 8 consecutive null/dead outcomes in the same domain (C2 · C3 · C3-K2 · C1 · S2A · S2B · slate-3 · WHO-track), found via an unrelated meta-governance sweep, not a scheduled or auto-triggered audit. This is itself load-bearing evidence for §5 of this note (cadence recommendation).
**Authors:** Joshua (operator) + Claude Code (this session).
**Scope:** single methodology (MSL) — meta layer. Layer classification defended in §2.
**Lives in:** `docs/notes/audits/programme-audit/2026-08-14-msl-methodology-audit.md`

---

## §0 — Source anchors

- [MSL charter](../../../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) — last-edit commit `8290b89` 2026-08-13 ("fix(ci): clear validation-controls lab/ collection errors"); the substantive implied-SR content edit landed earlier the same day in `0408a9f` ("demote implied_annualized_sr to report-only; reopen fade cells"); founding commit `0fb4e01` 2026-08-12. *(Corrected during this audit's own adversarial-review pass — the original draft cited `0408a9f` as last-edit; `8290b89` is later same-day.)*
- [MSL program plan](../../../briefs/programs/2026-08-12-msl-program-plan.md) — most recent touch `eb1f7c7` 2026-08-14 ("link PR #822 on WHO-track session + plan §6"), this session's own read
- [Sourcing-channel ratification ADR](../../../adr/2026-08-12-msl-sourcing-channel-ratification.md) — `c0d20bd` 2026-08-12 ("Board B1-B3 + B8 — ratify channel, slate C2->C3->C1... occupancy release")
- [MSL C3-K2 dual-axis revive ADR](../../../adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) · [MSL slate-2 design-box ADR](../../../adr/2026-08-13-msl-slate-2-design-box.md) — both `Accepted`, used as this audit's ADR-header template
- [implied-SR report-only / fade-reopen ADR](../../../adr/2026-08-13-implied-sr-report-only-fade-reopen.md) — `Accepted` 2026-08-13 (touches MSL charter step 3; same content as the `0408a9f` charter edit above)
- Seven closures, each verified against its own add-commit (per-file `git log`, not one shared hash): [C2](../../../briefs/closures/MSL-C2-closure-falsified.md) `1178553` · [C3](../../../briefs/closures/MSL-C3-closure-operator-kill.md) `59673b3` · [C1](../../../briefs/closures/MSL-C1-closure-falsified.md) `a3c4a16` · [S2A](../../../briefs/closures/MSL-S2A-closure-falsified.md) `fb137d3` · [C3-K2](../../../briefs/closures/MSL-C3-K2-closure-falsified.md) `0a20637` · [S2B](../../../briefs/closures/MSL-S2B-closure-stage1-fail-route.md) `8a75ab4` · [S7](../../../briefs/closures/MSL-S7-closure-resolved-e1-hold.md) `ef48b01` — all 2026-08-12/13/14 per file
- Two notices, each verified separately: [slate-3 constraints](../../notice/N-2026-08-14-msl-slate-3-constraints.md) `c4dc069` · [WHO-track (estate-wide)](../../notice/N-2026-08-14-msl-who-track.md) `56be680` — both 2026-08-14
- [Prior quarterly audit](2026-08-08-quarterly-audit.md) — added in `00cdd14` 2026-08-08 (verdict table, verified verbatim: **Meta = Stable — watch flag**, operator ruling §1.3-a; **Object = Degenerating**; **D1 = Degenerating**; read in full, treated as prior state — MSL launched 4 days after this verdict)
- [Programme Audit Protocol](../../../../.claude/skills/programme-audit/SKILL.md) and [`references/audit_note.md`](../../../../.claude/skills/brief-authoring/references/audit_note.md) — both read this session
- `git log --since=2026-08-12` over `docs/adr docs/briefs docs/notes docs/spec` — 39 MSL-tagged commits (re-verified this session; supersedes a slightly stale 34-count from an earlier pass), 0 deletions confirmed via `--diff-filter=D` (empty output)

---

## §1 — Context and trigger

**Programme:** MSL — the FXIFY-era operator+Claude composition loop, ratified 2026-08-12 as a named sourcing channel feeding TNEC-1 intake (`docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md`, Status RATIFIED). Not itself a strategy; it is a candidate-*generation* discipline sitting upstream of the locked 4-strategy portfolio.

**Audit window:** 2026-08-12 → 2026-08-14 — MSL's entire operating history. No prior MSL audit exists; this is a first baseline, stated explicitly per protocol Q2.

**Trigger:** signal #5 (SNAG) per the task framing quoted verbatim at dispatch: "Multiple null/ambiguous loops in the same domain... SNAG budget exhaustion is the right response, not infinite-patching." Verified against MSL's own §6 claim manifest: C2 FALSIFIED, C3 OPERATOR-KILL, C3-K2 FALSIFIED (both axes), C1 FALSIFIED, S2A FALSIFIED (N-ACT), S2B STAGE-1 FAIL, slate-3 BLOCKED (mechanism-dry, no card authored), P3.8 WHO-track STILL DRY (estate-wide sweep). Eight consecutive dead/null results in 2 days. The trigger is confirmed, not asserted.

**Load-bearing context this audit must not re-litigate but does treat as prior state — corrected during this audit's own verification pass:** `docs/operational_rules.md:617` compresses the 2026-08-08 quarterly audit as "(both layers Degenerating; ...)" — that compression does not match the audit's own primary verdict table, checked directly against source this session: **Meta = Stable — watch flag** (operator ruling §1.3-a, 2nd consecutive net-positive belt-churn cycle graded YELLOW, not RED, on the quarterly-cycles-only reading the audit itself rules as governing); **Object = Degenerating**; **D1 = Degenerating**. So the meta layer — the layer MSL itself belongs to (§2 below) — was watch-flagged, not degenerating; it is the object layer and the D1 gate-limb that were Degenerating, plus a mandated Great Prune spanning both. MSL was ratified 2026-08-12, 4 days after that mixed verdict. This is still directly relevant to Q1 and Q4 below (MSL is a brand-new belt item created by an apparatus already carrying a meta-layer watch flag, so its own discipline needed independent verification, not inherited credit) — but the "immediate aftermath of a Degenerating meta-layer finding" framing in an earlier draft of this note was wrong and has been corrected here; `docs/operational_rules.md:617`'s own compression is a separate, lower-priority accuracy issue this audit flags but does not fix (out of this audit's scope).

---

## §2 — Layer classification (first task, per protocol)

**Classification: MSL is a meta-layer (methodology) programme, not an object-layer (portfolio) programme.**

**Defense.** The programme-audit protocol's own test: meta-layer hard cores are *epistemic moves* that generate decisions; object-layer hard cores are *empirical claims about market behavior* and are the *output* of the methodology layer. MSL's hard core — charter steps 1–8 (slate card → dedup/door-check → $0 screens → cheap falsifier → G0 freeze → Pine authoring → operator TV backtest → survivor MC verdict) — is a procedure for generating and screening candidates. It makes no claim about market behavior on its own; every claim it produces (e.g. "PDH/PDL failed-break reclaim nets −0.176R on MYM, CI upper −0.083") is a claim about a *specific candidate*, immediately either killed (6 of 7 cards) or destined for TNEC-1 intake if it ever survives (0 of 7 have). MSL is explicitly named in its own spec as a "**named sourcing channel** feeding TNEC-1 intake" (`docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md:4`) — a generation modality change, sibling to the futures-anomaly-discovery mining stack, not a change to the locked portfolio itself. The program plan's own layering (`docs/briefs/programs/2026-08-12-msl-program-plan.md` §Layering: "Board → Managers → Workers... Pine and doctrine never fleet") is procedural/epistemic, matching the meta-layer definition exactly.

**Consequence for this audit:** portfolio P&L, `dd_protection` state, live account balance, and the locked strategies' authorization tiers are **out of scope** as evidence for MSL's verdict (Q4 below explicitly checks that no such citation crept in). Conversely, MSL's own 0-for-7 record says nothing about the locked portfolio's health, and this audit does not use it that way.

---

## §3 — Seven diagnostic questions (evidence assembled before verdict — see §4)

### Q1 — Hard core integrity

**Preserved in substance; one under-specified (charter-licensed by cross-reference, but not one of the 8 numbered steps) procedural layer found.**

*What held:* every card that reached G0 shows a properly gated freeze — B4 GO cited explicitly in the freeze commit (`96725f8` C2, `0561e09` C1, `76bcbf8` S2A, `5e32cec` C3-K2); every card's Stage-0/1 executed the dedup+door-check with pasted `rg` output (verified in the WHO-track and slate-3 notices, both showing literal `rg -n ...` command blocks with `(empty)` results, not asserted); Req 1a delete/flip ran on every scored card and was never allowed to rescue a FALSIFIED primary — stated explicitly and identically across four closures ("DELETE PASS does not rescue a FALSIFIED primary," C1 closure §2; "DELETE PASS on Axis B does not rescue a FALSIFIED primary," C3-K2 closure §2).

*What is unresolved:* the charter names 8 literal steps, with step 6 = "Pine authored CC-solo" immediately following step 5 (G0 freeze). In practice, every one of the four G0-frozen cards (C2, C1, S2A, C3-K2) died at an **"explore"** stage — gated by its own gitignored `EXPLORE_GO.md` token (e.g. C2 closure: "`EXPLORE_GO.DRAFT.md` (promoted → gitignored `EXPLORE_GO.md` ISSUED 2026-08-13)") — that scores the construct directly against the historical IS panel in Python (session-block bootstrap CI, DELETE/FLIP), **without ever authoring Pine or reaching TV**. *Correction made during this audit's own verification pass:* an earlier draft called this stage "undocumented"/"unlicensed" — too strong. The charter's own R-REQSCOPE election (charter line 9; ratification ADR §2.3, election 3) reads: "MSL candidates enter under the estate's **G0/explore-confirm lane discipline** (dense-1m precedent)" — so "explore" is named and licensed by cross-reference in the charter's own ratified text, in both documents this audit already had open. The real, narrower gap: "explore" is not one of the charter's 8 *numbered* steps and carries no gate criteria of its own spelled out inline — a specification-completeness gap, not an unlicensed procedural layer. Net effect unchanged: **step 6 (Pine) has a 0% execution rate across MSL's entire life** — 4/4 G0 freezes died before Pine was ever authored once. This is plausibly a sanctioned, beneficial elaboration (it protects the scarce operator-TV-time resource exactly as plan §8 states is the point of "the entire pre-TV pipeline"), and no evidence surfaced that it was used to rescue anything — but its 100% historical death rate is exactly the blind spot this audit's §2 deliverable (the falsifier ADR) targets. **Grade: YELLOW** — conduct preserved and licensed by cross-reference; one under-specified (not undocumented) procedural layer flagged for a light follow-up (§5).

### Q2 — Belt churn balance (first baseline, stated explicitly)

MSL has no prior audit — this is the first baseline, per protocol instruction. Measured over the 2-day window: **doc-artifact tally = 17 ADD / 0 REMOVE** since the 5 founding documents (charter, program plan, first slate, ratification ADR, occupancy-release ADR — all committed 2026-08-12, commits `0fb4e01`/`c0d20bd0`). The 17 additions: 4 further ADRs (the implied-SR pair — `2026-08-12-msl-implied-sr-disclosure-not-kill.md`, now `Superseded`, and its 2026-08-13 successor `implied-sr-report-only-fade-reopen.md` — plus C3-K2 revive and slate-2 design-box), 7 closures, 3 notices, 1 handoff card, 1 second-slate brief, 1 slate-generation-review packet (`git log --since=2026-08-12 --diff-filter=A` over `docs/adr docs/briefs docs/notes docs/spec`, re-verified this session — an earlier draft undercounted this as 16 by folding the superseded/superseding implied-SR pair into one bullet; corrected). Zero deletions in the same command. *The implied-SR pair being issued and reversed inside ~24 hours is itself worth naming explicitly here — an ADR authored and superseded in about a day is exactly the texture this belt-churn question exists to surface, and it was invisible in the earlier undercount.*

At the mechanism level (not just doc count): 3 founding constraints (R-CHANNEL / R-FRAMING / R-REQSCOPE) plus 3 constraints layered on since — `K_intrinsic=2` dual-axis licensing (C3-K2 ADR), the slate-2 design-box election (rr/WR/hard-stop), and the E1 HOLD stop rule (S7 closure) — **0 removed**.

Since this is a first baseline the formal "net-positive across ≥2/≥3 consecutive audits" trigger cannot fire (protocol requires prior audits to compare against — there are none). But the **rate** is worth surfacing without over-claiming a verdict from it: 17 artifacts / 2 days ≈ 8.5/day, vs. the **meta layer's own** most recent belt churn — "26–32 ADD / 4 REMOVE... ADR corpus 48→121 in 38 days, zero removed" (2026-08-08 audit §1.1, diagnostic 2) ≈ 0.8/day, graded **YELLOW** on the quarterly-cycles-only reading the 2026-08-08 audit itself rules as governing (2nd consecutive net-positive cycle; the same figure would read RED on a wider all-audits-count reading, which that audit explicitly declines to use). *Corrected during this audit's own verification pass — an earlier draft misattributed this figure to the object layer, to §1.2, and to a RED grade; it is meta-layer, §1.1, and YELLOW.* MSL's raw artifact-production rate is still roughly an order of magnitude faster per calendar day than the comparator, and the comparator is itself the layer MSL belongs to (making it the more apt yardstick, not less) — though the comparison stays imperfect (MSL's artifacts are mostly small, single-card closures with a fixed template, not novel doctrine each time). **Grade: BASELINE (not colorable) — rate flagged for the next audit's first real trend comparison.**

### Q3 — Progressive evidence

**GREEN**, using this repo's own established evidentiary convention (the 2026-08-08 audit graded the meta-layer's Q3 GREEN specifically because "pre-registered expectations recorded WRONG rather than retrofitted" — honest disconfirmation counts as progress, not just confirmed survivals). Every scored MSL card pre-registers its kill/survive routes in a frozen `PREREG_G0.md` *before* touching data, and every route fired exactly as designed: C2 pre-registered "both arms n≥100 ∧ CI upper < 0 → FALSIFIED," then measured CI uppers of −0.071/−0.075 and correctly fired FALSIFIED; S2A pre-registered N-ACT < 1 trade/week as an explore-gate trigger, then measured 0.511 and correctly fired; C3-K2 pre-registered both axes independently and both independently fired FALSIFIED rather than being pooled or rescued. In every case a partial pass (DELETE PASS, FLIP PASS) was explicitly refused as a rescue of a FALSIFIED primary — stated verbatim in four separate closures. This is real Popperian discipline: falsifiers written before data contact, firing on their own terms, never softened after the fact. **Caveat:** this grades the discipline of the kills, not a positive corroborated survival — MSL has never yet tested a *survive* prediction, since nothing has reached step 8.

### Q4 — Degeneration evidence

**No degeneration found.** The one candidate loosening in the window — `implied_annualized_sr` demoted from a freeze-time FAIL (>1.83) to disclosure-only (`docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md`) — was checked specifically for the Q4 pattern ("was the revision predicted by an independent model, or rationalized after the fact"). It was **not** a belt-patch rescuing a specific MSL candidate: (a) it is an estate-wide doctrine ADR, not an MSL-only carve-out (it supersedes the 2026-08-10 predecessor and an interim MSL-only stub in the same motion); (b) none of the seven MSL closures cite implied-SR as their kill trigger — every kill fired on CI-upper<0 or N-ACT<1, both unaffected by this limb; (c) the ADR explicitly preserves DSR-at-K as the measured-result gate and states the falsifier condition for its own reversal (§4: any future kill-on-SR, DSR-skip, or mechanism-laundering reverts it). This is an operator-directed doctrine correction with a stated reversion trigger, not an ad hoc rescue — the same "operator-grounded not rationalized" pattern the 2026-08-08 audit graded as non-degenerate for the analogous 2026-08-04 K-bank→disclosure change. No other belt revision in the window was found to have rescued a killed or marginal candidate.

### Q5 — Boundary respected

**GREEN — all eight charter-forbidden moves checked individually against the seven closures + two notices, none found:**

1. No ORB-at-Tradeify re-entry — confirmed still parked (WHO-track §3: "ORB parked").
2. No post-hoc filters after seeing results — DELETE/FLIP are pre-registered in every `PREREG_G0`, and every closure explicitly refuses to let a post-score partial pass rescue a FALSIFIED primary (Q3 evidence, same anchors).
3. No instrument-hopping after scoring — every card locked one instrument at Stage-0 by mechanism-independent reasoning (C2=MGC, C3/C3-K2=M2K, C1/S2B=MYM, S2A=MCL); C3-K2's M2K revive is a fresh Stage-1 + new B4 under the registry re-proposal bar, not a mid-score swap.
4. No TV-report metric as verdict — moot to date (0 cards have ever reached TV); consistent, not violated.
5. No weakening harvest Req 1–5/EM0/regime gate "because manual" — R-REQSCOPE narrowed Req 1b/Req 2 applicability to internally-composed candidates, but this was a **formal upfront ratified election** (ratification ADR §2.3, 2026-08-12) with Req 1a delete/flip + EM0–EM5 + TNEC-1 explicitly preserved as still binding — not a stealth mid-stream weakening of the kind the forbidden-move clause targets.
6. No Striker-leg redeploy — B8 occupancy release explicitly states "Striker legs stay barred" (plan §1 row B8).
7. No G0 self-freeze — every freeze cites an operator B4 GO by name; C3 and S2B (which never froze G0) are correctly recorded as pre-G0 stops, not self-frozen.
8. K-banks stay disclosure-not-gate — C3-K2 ADR states explicitly "family bank `K_banked(M2K)=0` does not gate."

### Q6 — Theory-comparison performance

**AMBIGUOUS — no real counterfactual exists yet, stated honestly rather than forced.** MSL was the only live generation channel running in this window; there was no parallel channel to compare routing choices against. The one nominal routing choice (slate-1 order C2→C3→C1, elected at B2) is untestable because all three died regardless of order. The channel-level comparison implied by the ratification ADR's own context — MSL vs. continuing to grind the already-8×-zero-yield exhausted channels — is not evidence MSL "outperformed," since MSL has *also* now returned zero yield after 8 dead loops; the only defensible claim is that it did so cheaply ($0, 2 days) and with clean discipline (Q3/Q5), which is a process virtue, not a theory-comparison result.

### Q7 — Falsifier check (grep/diff executed, shown below)

**No drift found.** Charter Gate text, verified byte-for-byte against the version quoted at dispatch:

```
$ grep -n "FALSIFIED (yield)\|6 consecutive cards\|12 calendar weeks" docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md
26: ...FALSIFIED (yield) if **6 consecutive cards die pre-G0 across ≥2 instrument
    families**, or **12 calendar weeks pass with zero G0 freezes**...
```

Matches the dispatch-quoted text exactly. Cross-checked against every place the yield clause is cited in practice (`grep` across the plan, all 7 closures, both notices, and the ratification ADR — 9 hits, raw output captured this session): every citation quotes "6 consecutive... ≥2 instrument families" / "12 calendar weeks... zero G0 freezes" verbatim, with no rewording, no softened paraphrase, and — critically — no session ever claims the clause fired when it hadn't: the S7 review packet explicitly refuses to conflate the counts ("Cite FALSIFIED(yield) — four G0s this week; pre-G0 deaths are two, not six," §5 forbidden-moves), and the Stage-1-deaths counter (2/3: C3 + S2B) is kept as a visibly separate, lower rung on the ladder rather than merged into the yield count. **The threshold numbers have not drifted; the discipline of applying them has held under real temptation** (a session authoring its own closure had every incentive to round 2 up to 6 and didn't).

*Correction made during this audit's own verification pass:* the quote above was originally mis-cited as coming from the S7 closure's §5 forbidden-moves. Re-checked against source: the S7 closure (`docs/briefs/closures/MSL-S7-closure-resolved-e1-hold.md` §3) only lists "citing FALSIFIED(yield)" as a bare forbidden item with no elaboration; the full "four G0s this week; pre-G0 deaths are two, not six" phrasing is verbatim in `docs/briefs/programs/2026-08-14-msl-slate-generation-review.md` §5 line 85 — the Board packet the S7 closure is *of*. Citation corrected; the underlying evidentiary point (discipline held, no rounding-up occurred) stands on the corrected source. This correction is itself evidence for this audit's own §7 self-check discipline (verify content, not the label a prior draft gave it).

**But the check surfaces the gap this audit was asked to name, not a drift:** the yield clause's two limbs — pre-G0 death count and weeks-since-last-G0 — structurally cannot detect a channel that reliably clears G0 and then dies. Currently **4 of 4 G0 freezes (100%) have died at the under-specified "explore" stage** (Q1) with **zero Pine files ever authored and zero survivor-MC computations ever run**, and the yield clause's own counters do not register any of this: the pre-G0 tally sits at a reassuring 2/6, and the weeks-since-G0 clock resets every time a new G0 freezes (four times in 2 days) even though every one of those freezes died within roughly a day. A channel could in principle run this pattern indefinitely — freeze G0 often enough to keep the weeks-clock from ever reaching 12, kill everything at explore, and never once trip the existing falsifier. This is the concrete, evidence-grounded gap Task 2's ADR (§ below) proposes to close.

---

## §4 — Disposition verdict

**Stable — watch flag.**

Reasoning, following from §3 (not preceding it): MSL is not **Progressive** — it has produced zero survivors, zero Pine files, zero TV backtests in its life, and the window (2 days) is too short to claim a trend either way. It is not **Degenerating** — Q4 found no belt-patch without independent corroboration, Q5 found zero boundary violations across all eight named forbidden moves, and Q7 found the falsifier thresholds unmoved and honestly applied under real temptation to round up. It is not **Falsified** — the charter's own pre-committed falsifier has not fired (2 pre-G0 deaths, not 6; 4 G0 freezes in the window, not zero), and this audit is not empowered to declare a different, unratified falsifier fired retroactively. It is not fully **Ambiguous** — six of seven questions have concrete, anchored answers; only Q6 lacks a real counterfactual, which is a data-availability limit, not a verdict blocker.

**Stable** fits the protocol's own definition — "delivering value but not generating new insight in the audit window; continue with watch flag, re-examine cadence" — and matches this repo's own precedent: the 2026-08-08 audit graded the meta layer overall "Stable — watch flag" on a very similar profile (GREEN progressive-evidence discipline, but weaker on belt-churn/theory-comparison/falsifier-reachability). MSL's own SNAG-exhaustion response (E1 HOLD, no slate-4 without a genuinely new WHO, an honest "STILL DRY" estate-wide sweep rather than a manufactured WHO to keep going) is itself the textbook non-degenerate response the protocol prescribes for SNAG budget exhaustion — "SNAG budget exhaustion is the right response, not infinite-patching" — which counts as evidence *for* Stable, not against it.

**Watch flag, named explicitly:** the falsifier's G0-to-survivor blind spot (Q7) is live risk right now — the channel is currently dry with zero candidates in flight and a pending Board election (E1/E2) — and is addressed by the Proposed ADR in §5 below, which this audit does not self-accept.

---

## §5 — Follow-ups

1. **Falsifier survival-limb ADR (this session's Task 2 deliverable).** [`docs/adr/2026-08-14-msl-yield-falsifier-survival-limb.md`](../../../adr/2026-08-14-msl-yield-falsifier-survival-limb.md) — **Proposed**, awaiting a separate operator election. Closes the Q7 gap: a channel that reliably clears G0 and then dies at explore/Pine/TV is currently invisible to the charter's yield falsifier. Owner: operator (election) · target: before the next MSL card is authored (i.e. before any new G0 freeze), since the gap is live now. *Update 2026-08-14 (same-day, separate follow-on session, per this ADR's own §7 Phase-2 grep-sweep instruction):* **Accepted** by operator election; the charter Gate line and plan §6/§7 amendments landed in the same commit as the acceptance. This item is discharged — the original "Proposed, awaiting a separate operator election" text above is now historical (state at audit-authoring time), not current.

2. **"explore" stage specification gap (Q1) — narrower than an earlier draft stated.** The stage is already named and licensed by cross-reference (charter's R-REQSCOPE election, "G0/explore-confirm lane discipline"), so this is not an undocumented procedure; it is a gap in the charter's literal 8-step enumeration and gate criteria for a stage that is currently the sole point of death for 100% of G0-frozen cards. Light-tier follow-up, not urgent (no evidence of misuse, no charter clause currently violated). Recommend a light ADR or charter amendment naming "explore" as an explicit numbered step between G0 freeze and Pine authoring, with its own gate criteria spelled out inline rather than left to cross-reference, before it becomes load-bearing ambiguity. Owner: next MSL manager session · target: before slate-4 (whenever a new WHO unblocks it). *Update 2026-08-14 (same-day, separate follow-on session):* **DONE** — [`docs/adr/2026-08-14-msl-explore-stage-5a.md`](../../../adr/2026-08-14-msl-explore-stage-5a.md), light-tier, Accepted by operator election ("proceed with explore stage"). Charter names it step **5a** (non-disruptive insertion — a grep sweep this session confirmed external citations of steps 5/6/7/8 by number exist outside the charter, e.g. `docs/briefs/programs/2026-08-12-msl-first-slate.md`, `docs/briefs/programs/2026-08-13-msl-second-slate.md`, `docs/SESSIONS.md`, `docs/briefs/closures/MSL-C3-closure-operator-kill.md` — so a full renumber was correctly rejected in favor of "5a"). Gate criteria codified from the four G0-frozen closures, not invented.

3. **Audit-cadence recommendation** (per operator's stated hypothesis this session, engaged directly rather than rubber-stamped):

   The operator's framing — "programme audits are better done weekly rather than quarterly, given the velocity of work in this repo" — is a reasonable read of the *symptom* but not, on the evidence, the most precise fix. Verified this session (`git log --format='%ad %h %s' --date=short` over `docs/notes/audits/programme-audit/*.md`): audit-shaped artifacts landed 2026-07-01 (×2), 2026-07-21, 2026-08-03, 2026-08-05, 2026-08-08 — roughly 6 events in 5.5 weeks, already running far closer to weekly than the stated quarterly/semi-annual backstops in `docs/operational_rules.md` and the skill's own "Scheduled cadence" section. **Calendar frequency was not the failure mode that let MSL's SNAG pattern accumulate to 8 loops before anyone looked** — the skill's own design explicitly subordinates cadence to signal-triggering ("cadence is a backstop, not the primary trigger"), and this session's trigger (§1) confirms the theory works when someone runs it: the SNAG pattern was found by an *unrelated* meta-governance sweep, not by a scheduled or auto-triggered audit. A weekly calendar backstop would not, by itself, have caught this any faster than the routine sweep already did — MSL is only 2 days old.

   **The real gap is detection between audits, not audit frequency.** Recommend a **tiered response**, not a flat cadence change:
   - Keep the *existing* calendar backstops (quarterly meta / semi-annual object) as the outer bound — no evidence in this audit's window says they are too slow in principle, and the operator should not silently absorb a frequency change into force without a decision — this recommendation is not self-executing.
   - Add a **cheap, mechanical SNAG-detection scan** as a new step in the existing `daily-repo-truth-sync` scheduled task (`C:\Users\joshu\.claude\scheduled-tasks\daily-repo-truth-sync\SKILL.md`, verified present this session): a read-only grep/count over each active loop's closure/notice trail for N consecutive dead/null/BLOCKED verdicts in the same domain (the exact SNAG signal), flagged in the digest's lead line the way a CONTRADICTION or OVERTAKEN brief already is (§ "Output format... Lead with the single most important line"). This costs nothing per run (the task is already daily and read-only) and closes the actual gap — nothing currently watches for trigger conditions *between* audits, so they only surface when someone happens to sweep for them.
   - This is a **recommendation for the operator to accept or reject** — this session does not edit the live `programme-audit` SKILL.md's cadence text or the `daily-repo-truth-sync` task itself. Both remain as found.

---

## §6 — Cross-layer contamination self-check (executed, not asserted)

Re-read §2–§5 above specifically hunting for: (a) any citation of locked-portfolio P&L, `dd_protection` state, live account balance, or strategy authorization tiers as evidence for MSL's verdict; (b) any citation of MSL's 0-survivor record as evidence about the locked portfolio. **Result: none found.** The only cross-references in this note are meta-to-meta — citing the 2026-08-08 audit's *meta-layer* grading convention and verdict as precedent for grading another meta-layer programme, and citing that same *meta-layer* belt-churn rate (§3 Q2, corrected this pass to the right layer/section/grade) purely as a numeric yardstick for MSL's own rate observation, not as evidence about MSL's health. Both citations are meta-to-meta, not cross-layer — the object-layer verdict and D1 gate-limb are not cited anywhere in this note as evidence for MSL.

---

## §7 — Discipline checklist self-assessment

| Item | Status |
|---|---|
| Seven questions answered, each with evidence anchor | PASS — §3 |
| Belt churn tallied explicitly (adds vs removes, numbers) | PASS — §3 Q2 (16/0 doc-level; 3/0 mechanism-level) |
| Falsifier check executed (grep/diff shown) | PASS — §3 Q7 |
| Cross-layer contamination check passed (no cross-citations) | PASS — §6 |
| Disposition verdict assigned with reasoning that follows the evidence | PASS — §4 (written after §3, not before) |
| If Degenerating/Falsified: follow-up actions named, owner + date | N/A (verdict is Stable) — follow-ups named anyway, §5 |
| If Ambiguous: re-test conditions + date named | N/A for the overall verdict; Q6's sub-ambiguity is stated as a data limit, not deferred |
| §10 audit hooks runnable at next cycle | PASS — §10 below |

---

## §10 — Audit hooks (next cycle)

```bash
# Yield falsifier: has it fired since this audit? (re-run the same check as §3 Q7)
grep -n "FALSIFIED (yield)\|6 consecutive cards\|12 calendar weeks" docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md

# Has the new survival limb (if the operator accepts the §5 ADR) fired?
grep -rn "consecutive G0" docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md docs/briefs/programs/2026-08-12-msl-program-plan.md

# Has a Pine file ever been authored for an MSL card yet? (0 at this audit)
find lab/analysis/c1 -iname "*.pine" -path "*msl*" 2>/dev/null

# Belt churn re-tally (compare against this audit's 16/0 anchor)
git log --since=2026-08-14 --diff-filter=A --name-only --pretty=format: -- docs/adr docs/briefs docs/notes docs/spec | grep -i msl | sort -u
git log --since=2026-08-14 --diff-filter=D --name-only --pretty=format: -- docs/adr docs/briefs docs/notes docs/spec | grep -i msl | sort -u

# Has the "explore" stage been formally named in the charter yet? (Q1 follow-up)
grep -n "explore" docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md
```

---

## §11 — Closure

- **Status:** `Open` — MSL is an active channel (E1 HOLD, awaiting a new WHO); this audit does not close it, it dispositions the current state.
- **Immediate repair completed:** n/a (Stable verdict, no immediate repair mandated).
- **Structural repair completed:** pending — §5 item 1 (falsifier ADR) is Proposed, not yet operator-elected. *Update 2026-08-14 (same-day, separate follow-on session):* DONE — see §5 item 1's own update note above.
- **Lessons graduated to standing rule:** none this cycle (all findings below the two-incident bar individually; the "explore" stage documentation gap and the yield blind spot are both first-observation).
- **Follow-up audits triggered:** none automatically; §5 item 3 recommends (does not mandate) a mechanical daily SNAG-scan as a detection layer between scheduled audits.

---

## Verification

```bash
python scripts/check_brief.py docs/notes/audits/programme-audit/2026-08-14-msl-methodology-audit.md --type audit
grep -n "FALSIFIED (yield)" docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md
git log --oneline --since=2026-08-12 -- docs/adr docs/briefs docs/notes docs/spec | grep -ci msl
```

Audit notes fail by capturing the trigger without naming the structural cause. The check here: would running §10 hooks next cycle actually detect a recurrence of the G0-to-survivor blind spot? Yes, once the §5 ADR is operator-elected — until then, the hooks detect only whether the *existing* falsifier has fired, which is the honest, narrower claim this audit is entitled to make.
