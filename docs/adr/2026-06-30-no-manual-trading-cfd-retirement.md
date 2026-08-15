# ADR 2026-06-30 — Retire manual execution and the CFD venue; the operator ceases to be the execution layer

**Status:** Accepted (operator executive decision, recorded)
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-06-30
**Authors:** Joshua (decision) + Claude Code (recorder, this session)
**Supersedes:** none directly. **Closes the live-execution arc** that `project_ea_conversion_state` (MT4/MT5 US-jurisdiction blocker) and `project_us_legal_master_research` (FXIFY won't accept a futures master) left at "scale blocked on both fronts" — this ADR records the operator's resolution of that bind: stop manual execution, abandon the CFD venue, route scale through futures.
**Related:** `docs/adr/2026-06-23-tv-backtest-egress-automation.md` (never-automate-the-live-account posture); memories `project_futures_prop_pivot` (the chosen scale lever), `project_ea_conversion_state`, `project_us_legal_master_research` (the two prior venue closures); skill `live-execution-journal` (the off-spec classification used in §1).
**Layer:** execution (live-trading venue + operator role) — **not** strategy/risk-control. No locked parameter, allocation, `dd_protection` constant, or Pine source is touched by this ADR.

---

## §0 — Rule 0 reads (production-source verification)

This ADR is a venue/posture decision. It changes **no** risk-control code or locked parameter; the §0 reads exist to *prove* that, and to anchor the live-execution evidence that drives the decision.

- **Live-execution evidence (decision driver):** operator-provided DXTrade fills export (29–30 Jun 2026) + the two strategy signal panels (Striker NAS100 v1 and Striker DJ30 v4.5, 30 Jun 2026), supplied in-session 2026-06-30. Classified by hand per the `live-execution-journal` skill's TAKEN/SKIPPED/OFF-SPEC scheme. **NOT** a `ops/live_journal/scripts/journal_review.py` edge-captured run — that metric is a 6-week+ window and the wrong instrument for a 2-day discretionary-damage snapshot; the load-bearing fact here is the OFF-SPEC *classification*, which is window-independent (see §1).
- `core/config/params.toml` — anchor `784a9ab` (verified `git log -1 -- core/config/params.toml`, 2026-06-24). Confirms the locked config this ADR does **not** touch: G 0.34% / DJ30 v4.5 0.70% (pyr 750%) / Aegis 1.50% / NAS100 v1 0.37% (pyr 1000%), `dd_protection` C2 1.5%/0.40×, MC anchor 99.83/0.17/4.37. Unchanged.
- `CLAUDE.md` — anchor `efeda82` (verified `git log -1 -- CLAUDE.md`, 2026-06-25). Confirms the operational-posture note added by this ADR (§6) lands outside the `## Strategy Reference (LOCKED — do not modify)` table.
- Memory chain (decision lineage, Tier-4 corroborating — the prior closures that make CFD-retirement the *forced* consequence, not a fresh choice): `project_ea_conversion_state` (US clients cannot host gold/indices on any MT4/MT5 venue — only Aegis/USDJPY runs on OANDA US MT4), `project_us_legal_master_research` (the only US-legal automated chain is TV→TradersPost→Tradovate *futures*; FXIFY won't accept a futures master), `project_futures_prop_pivot` (CME-micro futures-prop is the chosen scale lever).
- `docs/adr/2026-06-23-tv-backtest-egress-automation.md` — anchor `9b60ad2`-era (read this session). The standing "never automate the authenticated live-edge account" posture that this ADR operationalizes by moving the live venue to an isolated futures account.

---

## §1 — Context

The four locked strategies are ~99.83% to pass the FXIFY challenge *if executed per-spec*. They are not the risk. The risk is the execution layer — and the execution layer is the operator, executing FIRE alerts (and non-alerts) by hand on DXTrade. On 29–30 Jun 2026 that layer failed in the most legible possible way: the operator manually opened oversized, off-spec index/Nasdaq longs and tilted into the loss.

**The receipt (hand-classified per `live-execution-journal`):** six manual fills over two days, **net −$4,188.85**. Every one is OFF-SPEC. On 30 Jun (a Tue, all four systems eligible), the Striker NAS100 and Striker DJ30 panels both read **FILTERED / Day P&L $0 / 0-of-2 trades** — the systems carried **zero** exposure on USTec and DJ30, yet the operator ran 25-lot USTec + double 10-lot DJ30 longs (−$3,077.75). On 29 Jun the USTec manual size was 32.5 lots — ~8× the strategy's own sanity tripwire (NAS100 > 4 lots ⇒ wrong). This is not under-capturing the edge (the usual leakage); it is *manufacturing* loss the design never signalled: 0% of the −$4.2K is system, 100% is discretion.

This forces a venue decision the operator has been circling since 2026-06-28. "No more manual trading" means execution must be automated. Automated CFD execution requires MT4/MT5 (or a broker API), and `project_ea_conversion_state` established that **no US-accessible MT4/MT5 venue can host gold/indices** for this operator — only Aegis/USDJPY runs on OANDA US MT4. `project_us_legal_master_research` established that the only US-legal automated chain is TV→TradersPost→Tradovate **futures**, and that FXIFY will not accept a futures master. The CFD venue is therefore un-automatable for this operator, and an un-automatable venue is incompatible with a no-manual-execution rule. The pivot to CME-micro futures-prop (`project_futures_prop_pivot`) is not a new idea — it is the only venue left once manual execution is removed.

**Decision driver (one sentence):** the live execution layer (the operator's hand) just produced −$4.2K of 100%-off-spec loss against flat systems, so the operator removes himself as the execution layer — which, because the CFD venue cannot be automated for a US person, forces abandonment of the CFD/FXIFY path in favour of automatable futures.

---

## §2 — Decision

**Decision:** The operator ceases to be the execution layer. Concretely, two coupled rules take effect:

1. **No manual discretionary execution.** No hand-placed trades on the live edge. Live execution happens only through an automated chain (FIRE alert → bridge → broker) or not at all. The bridge between "stop manual" and "automation live" is *no live trading*, not "careful manual trading."
2. **The CFD venue is retired.** The FXIFY $200K DXTrade challenge is, for all intents and purposes, done. Per the operator's executive call this session, the account is **left idle (no further trades, not formally closed)** — fees are sunk, optionality is preserved at zero cost, and it lapses on its own. Scale routes through **CME-micro futures-prop** (`project_futures_prop_pivot`), the one venue that supports US-legal automated execution of the gold/indices portfolio.

**Effective:** immediately upon acceptance (2026-06-30).
**Scope:** all live execution of the four locked strategies from this date onward. The strategies, allocations, `dd_protection`, and Pine source are **untouched** (Rule 0) — this ADR changes *who/how* executes, not *what* is executed. The futures re-mapping (sizing translation to micro contracts) is separate active work, begun this session (workflow `ws79oe4l5`).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Keep trading FXIFY manually, "with more discipline"** | The −$4,188.85/2-day receipt *is* the disciplined-intent failure mode — the operator knew the systems were flat and traded anyway. The skill's Core Principle #1 ("trade the system, not your opinion") and the Feb-2026 discretionary-override loss already logged this; one more "I'll be disciplined" iteration is the exact pattern the rule exists to break. |
| **Keep the CFD venue, automate it somehow** | Closed three times: `project_ea_conversion_state` (no US-accessible MT4/MT5 host for gold/indices), `project_copygram_migration_state` (FXIFY 1-mo-verified-trades wall), `project_us_legal_master_research` (FXIFY won't accept a futures master). Re-opening requires a jurisdiction/entity change, not a fourth attempt. |
| **Formally close/withdraw the FXIFY account now** | Operator chose idle-not-closed (this session). Closing forfeits residual optionality (a jurisdiction change could reopen it) for no gain — the fees are already sunk and idle costs nothing. |
| **Stay on FXIFY and just wait out the challenge un-traded** | Conflates "stop manual trading" with "make progress." An un-traded challenge times out; it is not a scale path. The point of the pivot is a venue that *can* be automated — idling FXIFY is the disposition of the old venue, not the plan. |
| **Status quo — no decision** | Leaves the operator as a discretionary execution layer that just lost $4.2K against flat systems, on a venue that structurally cannot be automated. The single most likely-to-pass asset in the operation (99.83%) kept at the mercy of tilt. Worse than recording the disposition. |

---

## §4 — Falsifier (revert trigger)

This ADR accepts a real cost (§6): it forfeits a 99.83%-to-pass challenge and opens a go-dark interval with no live execution until the futures chain is built and validated.

**Revert trigger (binary, event-driven):**
1. **CFD-venue reopen:** the operator's US jurisdiction/entity changes such that an automated CFD or MT4/MT5 venue carrying **gold + indices** becomes accessible to the operator (the `project_ea_conversion_state` jurisdiction blocker dissolves), **OR** a US-legal automated execution path for the full four-strategy CFD portfolio is demonstrated end-to-end. → CFD/FXIFY may be re-evaluated as a live venue via a fresh ADR.
2. **No-manual reconsideration:** explicitly **not** triggered by a desire to recover P&L. The no-manual rule holds until automation replaces it. The only evidence that would reopen "may the operator execute manually" is a clean-version `journal_review.py` **edge-captured ratio ≥ 80% over a ≥ 6-week window of system-faithful manual execution** — which, by construction, cannot accrue while manual trading is stopped. The no-manual rule is therefore *permanent-until-automation*: its revert is replacement-by-automation, not return-to-manual.

**Revert action:** supersede this ADR with a fresh one stating the changed jurisdiction/entity or the demonstrated automated CFD path as the anchor. Never edit §4 in place.

> **Note (2026-08-02, no §4 change):** trigger 2 already records that its ≥80% edge-captured
> ratio *cannot accrue* while manual trading is stopped. One further fact, surfaced by the
> 2026-08-02 falsifier-input reachability census: the **measuring instrument itself no longer
> exists** — `journal_review.py` was deleted with the `ops/live_journal` estate on 2026-07-11
> ([`2026-07-11-ops-cfd-estate-retirement.md`](2026-07-11-ops-cfd-estate-retirement.md)) and
> has zero occurrences in any `.py` in the tree. Consequence for re-arming: trigger 2 needs
> the harness **rebuilt against the futures fill microstructure**, not merely a resumption of
> trading — the CFD-era DXTrade-fill semantics do not transfer (same finding as
> [`2026-05-23-allocation-refresh-2.md`](2026-05-23-allocation-refresh-2.md) §Addendum
> 2026-07-01). This strengthens, and does not weaken, the ADR's "permanent-until-automation"
> reading.

**Trigger check schedule:** event-driven (trigger 1 fires at the moment of a jurisdiction/entity change or a demonstrated path); reviewed at each quarterly programme audit / regime trigger — next **2026-08-08**, then 2026-11-08, 2027-02-08, 2027-05-08.

---

## §5 — Forbidden moves (under this ADR)

- **"Just one more manual trade to make back the loss."** This is the exact tilt that produced the −$4.2K receipt (29 Jun's 32.5-lot revenge size into a 4.6-lot reference). The no-manual rule has no recovery exception; the urge to recover *is* the failure mode.
- **Logging back into the idle FXIFY/DXTrade account to trade it discretionarily.** "Idle, not closed" preserves optionality; it does not authorize trading. Treating the quiet account as "still in play" re-opens the execution layer through the back door.
- **Re-opening the MT4/MT5-host / FXIFY-CFD-automation question without a jurisdiction or entity change.** Closed three times (`project_ea_conversion_state`, `project_copygram_migration_state`, `project_us_legal_master_research`). Re-proposing requires the §4 trigger, not renewed effort against the same wall.
- **Letting the futures re-mapping touch locked strategy parameters.** The re-map is *sizing translation* (spot %-risk → integer micro contracts), validated with parity discipline. It is forbidden from changing any SL/TP/ATR/risk%/pyramid/session constant — those stay locked (Rule 0). A "while we're porting, let's tweak X" is a separate lock decision with its own MC re-validation.
- **Loosening the §4 trigger in place after the go-dark interval gets uncomfortable.** "We wished we were still earning, so we lowered the bar to resume manual/CFD" is `p`-hacking at the methodology layer. The discomfort *is* the cost this ADR named; fire the trigger openly (supersede) or hold.

---

## §6 — Consequences

**Positive consequences:**
- Removes the execution-layer single point of failure — the hand that just produced −$4,188.85 of 100%-off-spec loss against flat systems. The strategies' 99.83% pass profile assumes per-spec execution; automation is the only way to actually realize it.
- Aligns the live venue with the one that supports US-legal automation (CME-micro futures via TV→TradersPost→Tradovate), ending the structural bind where the automatable platforms lack the instruments and the instrument-complete platform lacks automation.
- Stops the bleed on the FXIFY account immediately (idle, no further trades).
- Purely subtractive at the strategy layer: no parameter/allocation/`dd_protection`/Pine change, so the locked MC anchor (99.83/0.17/4.37) is untouched and needs no re-MC.

**Negative consequences (real cost):**
- **Forfeits a 99.83%-to-pass challenge** — the single most likely-to-pass asset in the operation, abandoned mid-flight because it cannot be executed without tilt and cannot be automated for a US person. The FXIFY challenge fee is sunk.
- **A go-dark interval:** between today and a validated futures automation chain there is **no live execution anywhere** — no income, no challenge progress. The quiet must not be misread as "still in the game."

**Risks (probabilistic):**
- The futures path has its own unproven blockers: micro-contract **granularity** may not map cleanly to the locked %-risk sizing at small account size (the load-bearing open question in `project_futures_prop_pivot`); quarterly **roll**; per-prop-firm **automation/copy rules**; the TV→TradersPost webhook delay. **Mitigation:** the re-mapping workflow begun this session (`ws79oe4l5`) quantifies the granularity-floor per strategy; firm-selection + automation-rule verification is the explicit next work item. None of these is resolved by *this* ADR; they are the agenda the pivot now owns.

**Downstream artifacts that need updating (this session):**
- `CLAUDE.md` — add an operational-posture note (live execution: manual retired 2026-06-30; FXIFY/CFD idle; scale via futures-prop → this ADR). Outside the LOCKED table.
- Memory: new `project_no_manual_trading_cfd_retirement` (recall hook); `project_futures_prop_pivot` updated (re-mapping started + no-manual as upstream driver); `MEMORY.md` index line.
- `docs/SESSIONS.md` — this session's entry (written at wrap-up, includes the re-mapping findings).
- Skill `fxify-challenge` / `live-execution-journal` — now describe a *historical* live-CFD operation; flagged for operator follow-up via the skill-authoring path (on-disk SKILL.md edits do not persist — `feedback_skill_amendments_via_authoring_path`). Out of scope for this ADR's commit.

---

## §7 — Implementation plan

Largely **policy** — no risk-control code edit. Mechanical edits are documentation/state only.

- **Phase 0** — §0 reads verified this session (params.toml unchanged; CLAUDE.md posture-note target outside the locked table; memory lineage current).
- **Phase 1** — write this ADR; add the `CLAUDE.md` posture note; create/update memory (`project_no_manual_trading_cfd_retirement`, `project_futures_prop_pivot`, `MEMORY.md`).
- **Phase 2** — futures re-mapping (active, separate from this ADR): workflow `ws79oe4l5` (4 strategies × re-map→adversarial-verify) → synthesized per-strategy futures execution spec + granularity floors. This answers the `project_futures_prop_pivot` open question; it does **not** change any lock.
- **Phase 3** — `docs/SESSIONS.md` entry at wrap-up; verification block (check_brief.py + grep sweep) executes; status `Accepted`.
- **Operator follow-up** — skill-authoring-path edits to `fxify-challenge` / `live-execution-journal` (mark live-CFD ops historical); futures-prop **firm-selection + automation-rule** verification (the second `project_futures_prop_pivot` work item).

---

## §10 — Audit hooks (runnable)

```bash
cd "C:/Users/joshu/multi_firm_operations/.claude/worktrees/hopeful-hermann-4850ee"

# This ADR changes NO locked constant — the manifest is byte-untouched by it
git diff --stat HEAD -- core/config/params.toml core/dd_protection.py core/firm_rules.py
# Expected: empty (no staged change to risk-control sources under this ADR)

# The locked MC anchor is unchanged (no re-MC under this ADR)
grep -n "99.83\|0.17\|4.37" core/config/params.toml
# Expected: the [mc_anchor_pepperstone] pass/bust/p99 lines, unchanged

# CLAUDE.md posture note lands OUTSIDE the locked table
grep -n "manual trading\|CFD.*retire\|futures-prop" CLAUDE.md
# Expected: the new posture note; none inside "## Strategy Reference (LOCKED"

# Lock-anchor verification still Closed (proves nothing risk-control drifted)
python scripts/verify_lock_anchors.py
# Expected: ROUTING: Closed (exit 0)

# Weekly zero-fills attestation (added 2026-07-02; audit R5 follow-up).
# The idle FXIFY/DXTrade account stays credential-accessible and nothing
# mechanical watched it between this ADR and 2026-08-08 — this closes that gap.
# Operator downloads the DXTrade fills export weekly (idle => empty), then:
python ops/live_journal/scripts/zero_fills_attestation.py --fills <export.csv|.pdf>
# Expected on the idle account: "ATTESTED: 0 fills since 2026-07-01" (exit 0),
# one dated line appended to ops/live_journal/data/no_manual_attestation_log.md.
# A fill in-window => loud BREACH banner + exit 2 (a no-manual-rule violation,
# = the §5 forbidden move "logging back into the idle account to trade it").

# §4 trigger reminder — next programme audit / regime check: 2026-08-08
```

---

## Verification

```bash
# Discipline checks (mechanical)
python "C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py" docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md --type adr
# Expected: all 6 checks PASS

# Production-source verification (§0 anchors)
git log -1 --format='%h %ci' -- core/config/params.toml   # 784a9ab 2026-06-24
git log -1 --format='%h %ci' -- CLAUDE.md                 # efeda82 2026-06-25

# No risk-control source touched
git diff --stat HEAD -- core/ | grep -E "dd_protection|firm_rules|params.toml" || echo "none (expected)"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-30 | Initial authoring + acceptance (operator executive decision) | Joshua + Claude Code |
| 2026-07-02 | Added §10 runnable audit hook for the weekly zero-fills attestation (`ops/live_journal/scripts/zero_fills_attestation.py`) — the mechanical enforcement of the no-manual rule that the 2026-07-01 programme audit (R5, obj-1 yellow) flagged as missing. No §1–§9 (decision) content changed; enforcement-tooling addendum only. | Joshua + Claude Code |
| 2026-07-10 | Addendum below: FXIFY account **formally closed** (was idle-not-closed); DXTrade credentials removed; weekly zero-fills attestation control **retired** (its idle-account monitoring premise is discharged by closure). Refines §2.2 / §3's idle-not-closed sub-choice; §1–§5 decision content unchanged. | Joshua + Claude Code |

---

## Addendum — 2026-07-10: FXIFY formally closed; credentials removed; attestation retired

**Operator decision (this session).** The three coupled sub-choices this ADR made in §2.2 / §3 — *idle-not-closed*, credentials-accessible, monitored-by-weekly-attestation — are superseded by a single closure:

1. **The FXIFY $200K DXTrade account is formally closed** (no longer "idle, not formally closed"). §3 had ruled formal closure out on the grounds that idle "preserves residual optionality for no gain." Two things changed that calculus: (a) the residual optionality was a jurisdiction-change reopen path that the parallel `docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md` (R6 NO-GO) does not depend on; and (b) the go-dark posture is now settled, not transitional. Closure removes a live-credential attack surface at no strategic cost.
2. **DXTrade credentials are removed.** The `§5` forbidden move "logging back into the idle account to trade it discretionarily" is now enforced by construction (no credentials), not only by policy. This is strictly stronger than the monitored-idle control it replaces.
3. **The weekly zero-fills attestation control is retired.** `ops/live_journal/scripts/zero_fills_attestation.py` existed *because* the idle account stayed credential-accessible and nothing mechanical watched it between this ADR and 2026-08-08 (§10). With the account closed and credentials removed, that monitoring premise is discharged — an account that cannot be logged into cannot receive a manual fill. The script + `ops/live_journal/data/no_manual_attestation_log.md` are frozen (never run in production: the log carries zero attestation lines). The §10 attestation hook is superseded by this closure.

**What does NOT change.** §1–§5 (the no-manual decision, its falsifier, its forbidden moves) stand unchanged. The no-manual rule remains *permanent-until-automation* per §4; formal closure of the CFD venue is the disposition of the old venue, not a change to the rule. No locked parameter, allocation, `dd_protection` constant, or Pine source is touched. The §4 revert trigger (jurisdiction/entity change reopening an automatable CFD/MT-venue) is unaffected — closing this specific account does not foreclose a future venue under a changed jurisdiction; that would be a fresh ADR per §4.

**Scope note (honesty).** This addendum records an operator disposition of the account and the local tooling. Any external/broker-side account-closure action (the actual FXIFY/DXTrade close request) is operator-performed off-repo; this ADR records the decision and retires the in-repo control, it does not itself close the broker account.
