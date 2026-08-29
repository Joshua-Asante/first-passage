# MSL program plan — sessions, layers, and hand-offs (end to end)

**Status:** ACTIVE · Board B1–B3 + B8 ratified 2026-08-12 · authorizes nothing beyond charter steps ($0 · K=0) · **this document is the claim manifest** for the program — the orchestrator session is its only writer.
**Objective:** run the [MSL charter](../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) loop over the [first slate](2026-08-12-msl-first-slate.md) until one candidate clears TNEC-1 N-ACT…N-SIZE or the program stops honestly — against the **2026-11-08** TNEC-1 FALSIFIED clock (four-firms ADR §4 demotion clause; TNEC-1 adds no second clock).
**Layering:** Board (operator) → Managers (CC sessions, judgment) → Workers (Cursor packets = mechanical builds; Claude subagents = read-only verification fan-outs; operator = the only TV/venue actor). Surface allocation per [ADR 2026-07-14](../adr/2026-07-14-cc-cursor-surface-allocation.md): Pine and doctrine never fleet; lab tooling may.

---

## §1 Board layer (operator — decisions only this layer can make)

| # | Decision | Feeds | When |
|---|---|---|---|
| B1 | ✅ **RATIFIED 2026-08-12** — [ratification ADR](../adr/2026-08-12-msl-sourcing-channel-ratification.md): **R-CHANNEL** ☑ MSL joins §2-C L2 · **R-FRAMING** ☑ §2.1 governs · **R-REQSCOPE** ☑ do not bind composition (Req 1a + EM0–EM5 + TNEC-1 stand) | everything | first |
| B2 | ✅ **Elect slate order C2 → C3 → C1** (serialized) | P3 | with B1 |
| B3 | ✅ **Wrapper + allow-rule** — `scripts/dispatch_cursor.ps1` allow-listed in `.claude/settings.json` (raw `cursor-agent` / `agent.cmd` still blocked; never work around) | P2 | before P2 dispatch |
| B4 | Per-card G0 GO (freeze pre-registration; the only step that turns a card into a candidate) | P3.x | per card |
| B5 | TV runbook execution + CSV export (S2: no login automation; Downloads→local copy). **Chokepoint rule: the runbook must link the step 2–5 artifacts (dedup block · door-check record · screens table · G0 PR#) — refuse the TV seat if any is missing** (this is how the charter's FALSIFIED(process) condition gets detected) | P3.x step 7 | per candidate |
| B6 | Verdict ratification per candidate: kill→registry / survive→TNEC intake | P3.x → P5 | per candidate |
| B7 | Weekly review: manifest walk + SESSIONS scan + clock check (standing: weekly token trade stays operator-placed, unrelated to MSL) | program health | weekly |
| B8 | ✅ **Occupancy release** — [ADR](../adr/2026-08-12-msl-mym-occupancy-release.md): `MYM1!`/`MNQ1!` headroom released for new non-Striker MSL research/G0; S1 keep-warm + Striker redeploy bar untouched; no `LEG_MAP` code edit | unblocks MSL-C1 G0 path | before C1 B4 |

## §2 Manager layer (CC sessions — each row is one chat; hand it this file + its row; it authors its own handoffs per `handoff-verify`)

| ID | Session | Does | Fans out | Done when |
|---|---|---|---|---|
| P1 | **Ratification pack** | Adversarial review of charter+slate+plan BEFORE operator ratifies (the 2026-07-28 lesson: a checker-green brief carried 6 BLOCKERs); apply fixes; draft the full-tier compact ratification ADR for B1 | Claude-subagent review workflow (read-only) | ADR draft + reviewed artifacts on a PR |
| P2 | **Tooling orchestrator** | Freeze specs for the three worker packets (§3), each carrying a one-line frozen solo-build estimate at dispatch (feeds the §7 fleet falsifier); run the cursor-fleet loop (claim manifest §6, disjoint footprints, dispatch-moment staleness checks); review diffs; integrate | Cursor workers W-A/W-B/W-C | all three packets green on their acceptance anchors (W-A, W-B **and** W-C) |
| P3.x | **Campaign manager (one per slate card, serialized)** | Charter steps 1–8 + [5a](../adr/2026-08-14-msl-explore-stage-5a.md) (steps 1–4 pre-GO; the operator's B4 GO gates step 5's G0 freeze and everything after): Stage-0 pins → dedup/door-check (executed) → $0 screens → cheap falsifier → G0 freeze (on B4) → **explore confirm (5a)** → **Pine CC-solo** → runbook for B5 → ingest export → survivor MC → TNEC verdict string → closure/registry or intake packet | Claude-subagent dedup/graveyard sweep; NO Cursor (Pine + judgment) | TNEC verdict string **or** pre-screen rejection recorded + registry/intake artifact merged |
| P4 | **Verification** (invoked, not scheduled) | `fable-judge` any landed claim that matters if wrong (tool acceptance anchors, first verdict string); `blast-radius` after doc-landing sessions | Claude subagents | VERIFIED/REFUTED note attached to the claim |
| P5 | **Post-survivor** (exists only if a candidate survives) | TNEC-1 intake packet → operator GO chain (M1 RESOLVED + per-session GO + LEG_MAP release ruling — none of which this program touches) | — | out of MSL scope; deploy chain owns it |

**Session rules (all managers):** every session lands as a PR and **includes its ≤40-word SESSIONS entry text (W5 classes) in the PR description** — the orchestrator commits SESSIONS/STATE/this-manifest updates in the integration commit (single-writer discipline; merge=union phantom-conflict rule); worktrees per session; every handoff runs Phase-0 staleness checks at dispatch time, not authoring time (3 overtakes in one day, 2026-07-24).

## §3 Worker layer

**Claude subagents (read-only, in-session):** dedup/graveyard sweeps per card · adversarial review panels (P1, P4) · never author repo state.
**Operator-only actions:** everything in §1; plus TV compile is the real Pine gate (`pine_lint` passes code TV rejects — CE10237 precedent).
**Cursor packets (P2; all `lab/`-side, no locked surfaces, disjoint footprints):**

| Packet | Builds | Acceptance (frozen in the packet spec) |
|---|---|---|
| W-A `msl_preflight` | CLI: slate-card YAML → **evidence tables only, no verdicts** (dedup rg raw output · `instrument_profiles.py cell` raw output · cost-law/payability/worst-day/σ_d/implied-SR arithmetic tables). PASS/KILL and route answers are **written by the P3.x campaign manager** in the campaign record — adjudication never lives in a worker tool | Per-limb negative anchors: a fixture card with a known registry hit must **surface the hit** in the dedup block; a fixture on an instrument carrying a BINDING BAR must **emit the bar**; the fade-region fixture must reproduce implied-SR **2.98** in the arithmetic table (matching the ADR); a hand-computed clean card round-trips |
| W-B `msl_score` | **Adapter, not a new MC** (reuse-don't-rewrite): TV trade-list CSV → daily-panel rows (`date`, `pnl_usd`, `intraday_low` — the existing input contract) → `lab/research_utils/nsurv_channel.py::score_nsurv` (single construct; intraday-honest, full + both halves) / `book_score.py` (composed, landed PR #764) → TNEC verdict string JSON. The only new logic is the TV-export→panel conversion (Entry/Exit pairing). **Honesty rule:** an `intraday_low` reconstructed from trade closes omits within-trade open excursion — such a series carries the **LOWER BOUND** label even though the channel will score it, **unless** TV's per-trade Run-up/Drawdown columns are present and used to bound within-trade excursion. Geometry: consume `firm_rules` as-is (`dd_lock_offset_usd` corrected default since 2026-08-04 — verify, never re-patch) | **Primary anchor: the channel's own test pins** (`tests/test_nsurv_channel.py` exact headline_bust fixtures). The ORB k=2 **77.01% ±1.0pp** cross-harness pin is optional and requires git-history retrieval (`run_t2_intraday_bust.py` + panel were pruned — RESULTS-only at HEAD). Plus a hand-paired TV-export fixture round-trips exactly, incl. the LOWER BOUND label branch |
| W-C `tv_static_equity` | Util: TV export (compounded) → static-equity per-trade series for param compares | Matches a hand-recomputed known export; flagged divergence on a compounded fixture |

Packet discipline: umbrella handoff brief once (amortized), four-state returns, `cursor/msl-p<N>` branches from current `origin/main`, no writes outside footprint, no SESSIONS/STATE writes. Two `NEEDS_CONTEXT` bounces on a packet ⇒ that packet reverts to CC-solo (it wasn't freezable).

## §4 Sequence (dependencies, not dates)

```
Phase 0  DONE     charter + slate + this plan drafted
Phase 1  DONE     B1–B3 (+ B8 occupancy) Board-ratified 2026-08-12
Phase 2  DONE     P2 tooling fleet (W-A/W-B/W-C) MERGED
Phase 3  first slate exhausted → P3.4 S2A FALSIFIED → P3.2b C3-K2 FALSIFIED → P3.5 S2B STAGE-1 FAIL → P3.6 slate-3 BLOCKED → P3.7 **RESOLVED (E1 HOLD)** → P3.8 WHO-track **STILL DRY** → P3.9 **new WHO named, E1 discharged 2026-08-21** — MSL-S4 `expiry-oi-strike-convergence` (MGC) G0 FROZEN, Pine authored CC-solo, Explore-confirm deferred by operator override, operator TV backtest owed
Phase 4  P5       survivor → TNEC-1 intake → operator GO chain (outside MSL); not reached — MSL-S4 has no Explore/TV verdict yet
Standing B7       weekly review · 2026-11-08 clock · SESSIONS/STATE discipline
```

**Addendum 2026-08-29:** the Phase 3.9 / Phase 4 lines above are stale as of 2026-08-21 same-day.
MSL-S4's Explore-confirm (5a) was in fact executed later that session and returned
`AMBIGUOUS-HOLD` (real_stat −5.5213 = net divergence, not convergence; p_upper=0.5724; FLIP: FAIL)
— see
[`lab/analysis/c1/msl_s4_mgc_2026-08/_explore_confirm_2026-08-21_LOG.md`](../../lab/analysis/c1/msl_s4_mgc_2026-08/_explore_confirm_2026-08-21_LOG.md).
The operator `PARKED` the candidate the same day — see
[`core/strategies/candidates/candidates_CARD.md`](../../core/strategies/candidates/candidates_CARD.md)
and the 2026-08-21 [`docs/SESSIONS.md`](../SESSIONS.md) entries. No TV backtest is owed; do
not follow the RUNBOOK's superseded next step.

## §5 Report-back protocol (what "report back when each step lands" means)

Each manager chat ends by handing the Board chat one line: `MSL <session-id> <DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED> — <PR#> — <one-clause outcome>`. **Transport:** the line is the first line of the session's PR description; the operator pastes it to the Board chat; the orchestrator additionally polls open `msl`-titled PRs at each B7 walk (no session writes another session's files). The orchestrator updates §6 and, where a verdict landed, quotes the TNEC verdict string verbatim (never a summary word — the failing limb must survive transmission).

## §6 Claim manifest (orchestrator-only writes)

| Item | Holder | Status | PR | Note |
|---|---|---|---|---|
| Charter + slate + plan drafts | orchestrator session (2026-08-12) | REVIEWED | #767 | P1 4-lens review; 59 findings applied |
| P1 ratification pack | orchestrator session (2026-08-12) | DONE | #767 @ `2afc04c` | pack merged; Board elections this session |
| Board B1–B3 + B8 | this Board session | DONE | pending | R-* + C2→C3→C1 + wrapper allow + occupancy release |
| P2 tooling fleet (W-A/W-B/W-C) | — | MERGED | #771 · #774–#776 | umbrella + packets on main; CLI dispatch skipped (no cursor-agent; Task fallback) |
| P3.1 campaign C2 (MGC) | orchestrator Track A | **FALSIFIED** (explore IS) | #780 | B4+explore done; [closure](../closures/MSL-C2-closure-falsified.md) · [`RESULTS_g2`](../../lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md); CONFIRM unread |
| P3.2 campaign C3 (M2K) | orchestrator | **OPERATOR-KILL** (B4 declined) | #782 · #783 · #784 | [closure](../closures/MSL-C3-closure-operator-kill.md) · Stage-1 had PASSed; G0 never frozen; slot → C1 |
| P3.2b C3-K2 dual-axis revive (M2K) | this session | **explore FALSIFIED** (both axes) | #798 | [ADR](../adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) · [`PREREG_G0`](../../lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md) · [`RESULTS_g2`](../../lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md) · [closure](closures/MSL-C3-K2-closure-falsified.md); S2B unblocked |
| P3.3 campaign C1 (MYM reclaim) | orchestrator | **FALSIFIED** (explore IS) | #787 | [closure](../closures/MSL-C1-closure-falsified.md) · [`RESULTS_g2`](../../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md); CONFIRM unread; first slate exhausted |
| P3.4 campaign S2A (MCL continuation) | this session | **FALSIFIED** (explore IS, N-ACT) | #794 | [closure](../closures/MSL-S2A-closure-falsified.md) · [`RESULTS_g2`](../../lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md); CONFIRM unread; Pine unpaid |
| P3.5 campaign S2B (MYM filtered continuation) | this session | **STAGE-1 FAIL** (route) | #817 | [closure](../closures/MSL-S2B-closure-stage1-fail-route.md) · [`STAGE1`](../../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md); G0 never frozen; slate-2 exhausted |
| P3.6 slate-3 (MCL fade WHO) | this session | **BLOCKED** (mechanism-dry) | #819 | [notice](../notes/notice/N-2026-08-14-msl-slate-3-constraints.md) — no WHO outside INTAKE-DRY; camp **not** scaffolded |
| P3.7 §7 slate-generation review | this session | **RESOLVED (E1 HOLD)** | #821 | [packet](2026-08-14-msl-slate-generation-review.md) · [closure](closures/MSL-S7-closure-resolved-e1-hold.md) — Phase 3 HOLD; no slate-4 until NEW WHO; yield **not** fired; charter RATIFIED |
| P3.8 WHO-track (estate-wide) | this session | **STILL DRY** | #822 | [notice](../notes/notice/N-2026-08-14-msl-who-track.md) — every Tradeify product group + census backlog walked; no WHO outside INTAKE-DRY / C1–S2B; no camp; E1 stop rule stands |
| P3.9 MSL-S4 (MGC) | orchestrating session, 2026-08-21 | **G0 FROZEN**, Pine authored CC-solo → see addendum below — PARKED 2026-08-21 | pending | New WHO `expiry-oi-strike-convergence` — first to discharge E1, sourced by a dedicated cross-lane search (databento lane blocked on data access; literature + manual gap-hunt lanes converged on the same door with a resolved disagreement over a dead directional sibling). Explore-confirm deferred by operator override (no data access this session) — not scored. [`STAGE1`](../../lab/analysis/c1/msl_s4_mgc_2026-08/STAGE1.md) · [`PREREG_G0`](../../lab/analysis/c1/msl_s4_mgc_2026-08/PREREG_G0.md) · [`RUNBOOK`](../../lab/analysis/c1/msl_s4_mgc_2026-08/RUNBOOK.md) — **Addendum 2026-08-29:** stale same-day; see the §4 addendum above — Explore-confirm ran later 2026-08-21, `AMBIGUOUS-HOLD`, operator `PARKED` same day; RUNBOOK's TV-backtest next step is superseded. |
| **Stage-1 deaths counter** | orchestrator | **2/3** (functional **3/3**) | — | C3 + S2B counted; slate-3 not a card; E1 HOLD — no increment |
| **G0-to-Pine conversion counter** | orchestrator | **4 G0 freezes / 0 reached step 6 (Pine)** | — | C2 · C1 · S2A · C3-K2 counted (each *card*, not each G0 event — C3→C3-K2 revive counts once); WATCH rung trips at 6, hard FALSIFIED at 10-G0s-zero-survivor or 8-cal-weeks-w/-≥4-G0s-zero-survivor ([survival-limb ADR](../adr/2026-08-14-msl-yield-falsifier-survival-limb.md), added 2026-08-14) |

## §7 Program-level stop rules (pre-committed)

- **Charter FALSIFIED(process) fires** (a card reaches TV without the step 2–5 artifacts, any step out of order, or post-hoc sweep selection) ⇒ channel closes pending superseding ADR. Detection lives at the B5 chokepoint (runbook artifact-links rule).
- **Charter FALSIFIED(yield) fires** (charter Gate line, quoted: "**6 consecutive cards die pre-G0 across ≥2 instrument families**, or **12 calendar weeks pass with zero G0 freezes**") ⇒ channel closes pending superseding ADR.
- **Three Stage-1 deaths without any G0** (§6 counter) ⇒ Board review of the slate-generation method — the earlier rung of the yield ladder, not a substitute for it (not an automatic stop: cheap kills are the win, but three straight means cards are being authored into known-dead space).
- **Charter FALSIFIED(yield-conversion) WATCH rung fires** ([survival-limb ADR](../adr/2026-08-14-msl-yield-falsifier-survival-limb.md), added 2026-08-14: **6 consecutive G0 freezes** with **zero cards reaching step 6 Pine-authored**) ⇒ mandatory Board review of the explore-stage screen calibration — not an automatic stop, mirrors the Three-Stage-1-deaths rung above.
- **Charter FALSIFIED(yield-conversion) hard rung fires** (same ADR: **10 consecutive G0 freezes** with **zero TNEC-1 survivors**, or **8 calendar weeks** from first G0 [2026-08-12] with **zero TNEC-1 survivors** given **≥4 G0 freezes**) ⇒ channel closes pending a superseding ADR — same consequence as FALSIFIED(yield) above.
- **Cursor-fleet falsifier** (2 fleets in 8 weeks with integration cost > the packet's frozen solo estimate — recorded per packet at dispatch per the P2 row — or a spec-interpretation defect lands) ⇒ revert tooling to single-dispatch/CC-solo.
- **2026-11-08** with no N-clear candidate ⇒ TNEC-1 FALSIFIED clause governs; MSL closes with it (no second clock, no extension by re-framing).
- **Anti-goalpost clause** (verbatim from the withdrawal ADR, governing here): a result that misses a threshold narrowly is a miss — "that framing is the degeneration move this ADR exists to block."

## §8 Cost envelope

$0 and K=0 through every Stage 0–1; K_intrinsic per axis declared at each G0 (banks are disclosure, not gate); Cursor tokens on W-A/W-B/W-C only; no data pulls planned (TV exports + existing panels); operator TV time is the scarce resource — the entire pre-TV pipeline exists to protect it.
