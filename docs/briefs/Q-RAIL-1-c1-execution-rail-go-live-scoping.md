# Q-RAIL-1 — c1 execution-path scoping: rail, account, and execution-fidelity preconditions for the first live venue

> ⚠ **2026-07-22:** this brief's §1 claim that c1 "discharged the four-firms ADR §4
> falsifier" was **WITHDRAWN** — see
> [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md).
> §4 is undischarged (hard date 2026-11-08 unchanged). This brief's own scoping verdict
> (F1–F5 PASS, rail/account GO) is unaffected — only the §4-discharge premise it cited is
> stale. Also note: ORB-MNQ-1 (cited below as "a second admitted CANDIDATE") was later
> PARKED then the reconstruction track ruled TERMINAL (operator 2026-07-24); and "no live
> fills exist anywhere" no longer holds — canned B4 payloads have since filled (B6
> 2026-07-20, SIM 2026-07-27), though no TV strategy-signal-originated fill has occurred.
> Body left frozen as historical record; see [`CLAUDE.md`](../../CLAUDE.md) §Live-execution
> posture for current state.

**Status:** `CLOSED — RESOLVED 2026-07-17` — **F1–F5 all PASS**; rail TV→CrossTrade→NT8→**Tradovate** ([`PHASE3.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE3.md)); **Phase 4 packet emitted** ([`PHASE4.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE4.md) — Tradeify $328/$258 · MFFU $414 · worst+reset $681; Tradeify Select recommended); **§8 ceiling $700 operator-signed 2026-07-17 → cost clause ACCEPTS at both tiers.** Closure: [`closures/Q-RAIL-1-closure-resolved.md`](closures/Q-RAIL-1-closure-resolved.md). Evidence: [`RESULTS`](../../lab/analysis/c1/q_rail_1_2026-07/RESULTS.md). **F1 = PASS-via-fallback** — [`Q-PYRPARITY-1`](Q-PYRPARITY-1-watch1-pyramid-proportionality.md) `FALSIFIED-NONPROPORTIONAL`. **The rail-build/account GO remains a separate fresh operator decision + ADR.**
**Authored:** 2026-07-17
**Closed:** 2026-07-17 (`RESOLVED`)
**Authors:** Joshua (direction) + Claude Code (authoring)
**Parent question:** N/A (decision-scoping successor to the c1 chain: scoring → regime rider → haircut re-MC → G8 WATCH-1 ratification 2026-07-17)
**Series:** strategy-R&D priorities 2026-07-17 — **rank 1 of 4** (highest leverage). Siblings: [`Q-PYRPARITY-1`](Q-PYRPARITY-1-watch1-pyramid-proportionality.md) (hard dependency, rank 2), [`Q-INVENTORY-1`](Q-INVENTORY-1-zero-survivor-replenishment-disposition.md) (rank 3), [`2026-07-17-0808-packet-delta-and-sequence.md`](2026-07-17-0808-packet-delta-and-sequence.md) (rank 4).
**Loop:** Inquire-phase Pre-Q — closure gates on a decision-ready GO/NO-GO packet (or a named hard blocker), NOT on the GO itself. Rail build, account registration, and any live spend remain operator GO/NO-GO after this brief closes.
**Artifact path:** `docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md`

---

## §0 — Rule 0 reads (production-source verification; all read 2026-07-17, this session)

- `core/firm_rules.py` — anchor `a53ee99` (2026-07-13). Tier-1 verbatim constants for the two discharge tiers:
  - `Tradeify_Select_100K` (lines 227–240): `dd_type: "trailing_locking"`, `max_dd_pct: 3.0` ($3,000 EOD trailing, Select), `dd_lock_offset_usd: 100`, `daily_loss_pct: None`, `profit_target_pct: 6.0`, `min_trading_days: 3`, `weekend_holds: False`, `inactivity_max_idle_days: 5`, `micro_contract_cap: 80`, `cost_per_side_usd: 0.91`, `consistency_rule_pct: 40.0`.
  - `MFFU_Rapid_100K` (lines 286–300): `dd_type: "trailing_locking"`, `max_dd_pct: 3.0` (EOD MLL), `dd_lock_offset_usd: 100`, `daily_loss_pct: None`, `profit_target_pct: 6.0`, `min_trading_days: 2`, `weekend_holds: False`, `inactivity_max_idle_days: 5`, `micro_contract_cap: 80`, `consistency_rule_pct: 50.0`, `news_trading: True`, `cost_per_side_usd: 0.95`.
  - `ACTIVE_FIRM = "FXIFY"` (line 385) — anchor fixture; never switched by this work.
- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` — anchor `be6dda6`. G8: "Rail/account stay separately gated." Freeze item 4: envelope 90-day commission-freshness rule "re-verify at any deployment fork" — **this brief IS a deployment fork**; the re-verify obligation binds in Phase 0.
- `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md` — anchor `d85c10c` (2026-07-17). Ratified disposition: "lifecycle CANDIDATE, deployable at WATCH-1 (0.50×)," book-level; "Still gated: Rail build, account registration, and go-live remain separately gated."
- `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md` — anchor `d85c10c`. 0.50× arm clears the frozen floor on all four partitions × both tiers (H1 0.14%, bootstrap-95th 0.77%, pass-5th 95.76%). Practicality caveat: ~double median days-to-pass. Haircut modeled as ×0.5 on `daily_100k` — a **book-level return injection**, not a TV-side execution mechanism (the gap Q-PYRPARITY-1 closes).
- `docs/ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md` — anchor `fad8984` (LTM; read by path). Tradeify: "bots/algos permitted" w/ sole-ownership + no HFT (FTA §6.6, fetched 2026-07-12); platforms Rithmic + Tradovate; CrossTrade integration page. MFFU: "automated trading strategies tailored to their own specific settings," HFT prohibited (help article 8444599); platforms Tradovate + dxFeed; CrossTrade integration page. Canonical rail reference: **TV → CrossTrade → NT8 → Rithmic/Tradovate** per `docs/notes/2026-07-06-rail-reconciliation-traderspost-vs-crosstrade.md`. Survey performed **no** CrossTrade wiring, NT8 install, or registration.
- `ops/prop_envelope_default.md` — anchor `6b94032` (v1.0 RATIFIED). E6 attended-automation default on the TV→CrossTrade→NT8 rail; §4 overlay rows verified 2026-07-13 (stale ~2026-10-11; fresh at authoring). E1 EOD-flat default 16:00 ET, binding minimum MFFU 16:10 ET.
- `docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md` — anchor `ba943a1`. §5 forbids treating any research ADR as rail-build / account / live-spend authorization. This brief honors that: it produces the decision packet; the GO is a fresh operator decision + ADR.
- `core/strategies/striker/striker_dj30_v4.5_mym_FUTURES_LOCK.md` + `core/strategies/nas/striker_nas100_v1_mnq_FUTURES_LOCK.md` + `core/strategies/PORT_MANIFEST.sha256` (content-read 2026-07-17). MYM edition: AUTHORED 2026-07-03, "NOT TV-compiled, NOT parity-checked, NOT live"; **Bulenox-parameterized** (costs $0.61/side, Bulenox caps/flat times, day-stop default −1.15 promoted for the Bulenox chain); integer sizing `qty = floor(accountSize·risk% / (slDist·$0.50/pt))` + RESERVE cap policy; acceptance checklist (TV compile, per-candle parity vs CFD, C3 attribution, hash re-pin) is **entirely un-executed**. MNQ edition re-authored 2026-07-06 and hash-pinned (`4bb3772…`) — **but the `.pine` was not found on disk this session** (`find core/strategies -type f` lists its FUTURES_LOCK.md only). Gitignored files are unrecoverable from git history — Phase 1 must locate or re-author (re-author precedent exists: the 07-03 vintage was destroyed and re-authored from locked source).
- `STATE.md` — anchor `e5eca1a` (2026-07-17). Provisional micro floors (locked-risk mirror, roll-seam-masked ATR(11)×1.20): MNQ full-median $15,591 / recent-90d $29,559; MYM $3,234 / $4,350. Live-fill-starved threads this brief's success re-arms: Q-NAS-ECR-1 (parked pending an MNQ fill source), Q-DECAY-1 re-arm limb ("a leg goes live somewhere"), lifecycle Call-1 (build-ahead-of-data), ORB-MNQ-1 decay-monitor calibration (manifest held open on it).

**Cross-reference grep (cruft sub-rule, N/A):** nothing is deleted or archived by this brief.

---

## §1 — Context & motivation

As of 2026-07-17 the prop-portfolio program's research existence question is answered: c1 (2-leg MYM+MNQ, Striker-only) discharged the four-firms ADR §4 falsifier and was **ratified lifecycle CANDIDATE, deployable at WATCH-1 (0.50×)**; ORB-MNQ-1 is a second admitted CANDIDATE; Q-COMPOSE-1 closed the last open book-construction lever (breadth FALSIFIED — deploy c1 alone at 0.50×, no compose). Meanwhile every live-data-dependent monitor in the estate is starved by one shared condition — **no live fills exist anywhere** — and the standing gate ("rail build, account registration, live spend gated") has no decision artifact behind it: nothing currently converts "gated" into an operator GO/NO-GO. The four-firms ADR's own program shape is "discover → **productionalize** → execute"; productionalization scoping is authorized now. This brief is that scoping.

---

## §2 — Prior art / lineage

- **c1 chain (all closed/ratified):** candidate pre-reg (`2026-07-15-existing-strategy-book-candidate-1-prereg.md`) → G0–G8 scoring `RESOLVED (DISCHARGED)` → regime rider GATE FAIL at 1.00× → haircut re-MC `RESOLVED-DEPLOYABLE` at WATCH-1 → G8 intake ratified 2026-07-17. This brief consumes those verdicts; it re-litigates none of them.
- **Q-AUTO-FIRM-1** (`RESOLVED` 2026-07-12): 4 FRIENDLY firms under the attended-automation bar + CrossTrade/NT8 rail target. Established ToS quotes + platform chains for Tradeify/MFFU (the discharge pair).
- **Q-BTC-3** (`FALSIFIED`): full lights-out on TradersPost→Tradovate — the attended bar and CrossTrade reference exist because the lights-out framing died. This brief inherits attended-only.
- **R6 ADR §5** forbade commissioning the CrossTrade/NT8 rail *under the R6-era residual program*; the four-firms ADR (2026-07-12) reopened a new program with rail build gated on operator GO — this brief prepares that GO, it does not perform it.
- **Q-COMPOSE-1** (`CLOSED — FALSIFIED` 2026-07-17): no ORB composition; c1 deploys as the 2-leg book at 0.50×.
- **Q-NAS-ECR-1** (PARKED-DORMANT): re-points to an MNQ fill source only via a **fresh Pre-Q** (re-point is not type-preserving). This brief's RESOLVED outcome creates the fill source; it does not resurrect that hypothesis in place.
- **Futures venue editions (Phase B, 2026-07-03/06):** `striker_dj30_v4.5_mym.pine` (on disk, pinned) + `striker_nas100_v1_mnq.pine` (pinned, on-disk presence unresolved) with per-edition FUTURES_LOCK acceptance checklists — the natural starting artifacts for the deployable expression, but Bulenox-parameterized and never parity-checked.

---

## §3 — Question (Q-RAIL-1)

**Pre-Q gate test:** the symptom-only rephrase is: "two ratified/admitted candidates exist with no execution path, and every live-data monitor is starved of fills." No fix is baked in — the answer may be NO-GO.

**Q-RAIL-1:** What would converting c1's ratified WATCH-1 deployability into live fills at ≥1 of the two discharge tiers (`Tradeify_Select_100K`, `MFFU_Rapid_100K`) actually require — execution expression, rail architecture, account, all-in cost, ToS compliance — and does any hard blocker exist?

---

## §4 — Falsifiable hypothesis (H-RAIL-1)

**H-RAIL-1:** A ToS-compliant, attended-automation execution path for c1's deployable expression exists at ≥1 discharge tier, with every execution-fidelity precondition (F1–F5 below) individually satisfiable, at an all-in cost within the operator-signed budget (§8).

**Fidelity preconditions (each scored PASS / FAIL / BLOCKED-ON-INPUT in Phase 2):**
- **F1 — WATCH-1 injection mechanism:** a concrete, verified way to run the book at 0.50× (TV risk-input scaling iff Q-PYRPARITY-1 `RESOLVED-PROPORTIONAL`; else the documented account-multiplier-layer fallback per `strategy_lifecycle.md:113`). **SCORED 2026-07-17: `PASS-via-fallback`** — Q-PYRPARITY-1 `FALSIFIED-NONPROPORTIONAL` ([`closure`](closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md)); injection path = account-multiplier layer for the two pyramided legs.
- **F2 — Integer-sizing feasibility:** at $100K × WATCH-1 effective risks (DJ30 0.35% / NAS100 0.185%), both legs afford ≥1 micro at the provisional floors (STATE floors ×2 under the haircut: MNQ ≈ $59K < $100K; MYM ≈ $8.7K < $100K — to be re-verified against current ATR, not assumed), and pyramid adds survive integer flooring without changing the strategy (NAS100's edge is ~90% in the adds — quantization that kills adds is a FAIL, not a rounding note). **SCORED 2026-07-17: `PASS`** — recomputed on `MYM`/`MNQ` panels (SHA256SUMS `298ab8…`/`ddb14f…`); worst-case WATCH-1 floors MYM **$8,689** / MNQ **$59,039**; both base≥1 and RESERVE adds survive ([`F_SCORECARD.md`](../../lab/analysis/c1/q_rail_1_2026-07/F_SCORECARD.md)).
- **F3 — Deployable expression exists and matches the panel of record:** venue editions located (MNQ `.pine` found or re-authored + re-pinned), re-parameterized from Bulenox to the target firm's constants, and their FUTURES_LOCK acceptance checklists (TV compile + per-candle parity vs CFD source) executed clean. **SCORED 2026-07-17: `PASS`** — Phase 1b + Step-2 + C3 1a→1c ([`PHASE1B.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE1B.md), [`STEP2_PARITY.md`](../../lab/analysis/c1/q_rail_1_2026-07/STEP2_PARITY.md), [`STEP3_1C.md`](../../lab/analysis/c1/q_rail_1_2026-07/STEP3_1C.md)).
- **F4 — Session/EOD semantics:** EOD-flat + firm session calendar implementable on the chosen chain within E1's binding minimum (MFFU 16:10 ET). **SCORED 2026-07-17: `PASS`** — MFFU 16:10 re-confirmed; E1 16:00 ET force-flat implementable; Bulenox editions' ~16:45 fill is a Phase-1 retune obligation, not a chain impossibility.
- **F5 — ToS re-verification:** Tradeify FTA §6.6 / MFFU article 8444599 re-fetched fresh (90-day rule; deployment-fork re-verify) with automation posture unchanged. **SCORED 2026-07-17: `PASS`** — posture unchanged at both firms ([`PHASE0.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE0.md)).

**Reject H-RAIL-1 (→ `FALSIFIED`) if:** any F1–F5 is FAIL at *both* tiers with no documented recovery route, or the costed chain exceeds the §8 budget at both tiers. **Falsifier in one line:** H-RAIL-1 is falsified by a single hard blocker that survives both tiers' recovery routes.
**Accept H-RAIL-1 if:** all five preconditions PASS (or carry an executed fallback) at ≥1 tier and the costed chain is within budget → emit the GO/NO-GO packet.

**Budget-clause status (2026-07-17 ratification):** the operator deferred the §8 dollar ceiling to Phase 4 (no eval-fee pricing is sourced anywhere in the repo yet — that lookup is Phase 0's job, not authoring-time's). Until Phase 4, H-RAIL-1's cost clause is **PENDING**, not waived: F1–F5 and the rail-architecture work (Phases 0–3) proceed fully unblocked (none of them reference a dollar ceiling), and the cost-clause accept/reject only fires once the operator sets a ceiling against the Phase-4 cost table (see §6, §7 Phase 4, §8).
**Ambiguous-hold if:** any precondition is BLOCKED-ON-INPUT (e.g., Q-PYRPARITY-1 unresolved, MNQ edition unlocated and re-author not yet authorized) at the §6 check date.

---

## §5 — Forbidden moves (genuinely tempting)

- **Registering an account or paying an eval fee "to unblock testing"** — spend is gated; this brief's entire output is the packet that makes that decision honest. (Tempting because eval fees are small relative to the research spend already sunk.)
- **Commissioning CrossTrade/NT8/Tradovate wiring during scoping** — Q-AUTO-FIRM-1 explicitly performed none; scoping reads documentation, it does not build. Build starts only after operator GO.
- **Re-using the Bulenox-parameterized venue editions as-is** — their costs ($0.61/side), caps, force-flat times, and the promoted −1.15 day-stop default are all Bulenox-chain decisions; Tradeify/MFFU need a venue-constant re-pass and a fresh hash re-pin. (Tempting because the editions are 90% of the work.)
- **Folding ORB-MNQ-1 go-live into this packet as a co-primary** — multi-question trap; ORB rides as a second-wave annex only (its Pine/rail gates are its own). Its decay-monitor calibration unblock is a *consequence* of c1 going live, not a scope extension.
- **Reading c1's panel PF as a live-expectancy promise** — the Class-S claim is bust-geometry survival, not CFD-edge preservation (Class-S ADR); the packet's return language must stay in bust/pass terms.
- **Quietly widening to lights-out automation** because attended operation is operationally annoying — Q-BTC-3 falsified that lane; attended is the bar.
- **Switching `ACTIVE_FIRM`** to make any engine run convenient — anchor byte-repro guard (scoring pre-reg §5).

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` (decision-ready) | All five F-preconditions carry PASS (or executed fallback) at ≥1 discharge tier; rail chain documented from primary sources end-to-end; all-in cost table complete (eval fee + monthly platform/data + bridge + per-side commission model); **Phase 4 re-requests the deferred §8 ceiling from the operator against the assembled cost table, and the operator confirms it clears** (fresh sign-off — the 2026-07-17 ratification set tier-preference and the deferral mechanism only, not a number); packet presented with the risk framing of §7 Phase 4 | Operator GO/NO-GO on rail build + account (fresh ADR on GO). On GO: Q-NAS-ECR-1 successor Pre-Q authorized; ORB decay-monitor calibration re-scoped to the live venue |
| `FALSIFIED` (hard blocker or cost) | Any F1–F5 FAIL at both tiers with no recovery route; OR at Phase 4 the operator sets a ceiling and the costed chain exceeds it at both tiers | Record blocker; program stays research-only on the deployment axis; re-open requires the blocker's named input to change (a cost-FALSIFIED may re-open cheaply if a cheaper chain is later found — not a hard-blocker-grade close) |
| `AMBIGUOUS-HOLD` | ≥1 precondition BLOCKED-ON-INPUT at **2026-08-01** (pre-08-08 check date); OR Phases 0–3 complete but Phase 4 has not yet obtained the operator's ceiling sign-off | Carry into the 08-08 packet with the blocking input named (for the ceiling case: "cost table ready, awaiting operator ceiling"); do not silently demote |

**Pre-registered before Phase 1 runs.** The §8 thresholds are the only operator-supplied numbers; everything else above is frozen at ratification.

---

## §7 — Execution plan

- **Phase 0 — deployment-fork re-verifies (≤1 hr).** Re-fetch Tradeify FTA §6.6 + MFFU 8444599 + both firms' current 100K eval pricing pages (primary sources; envelope §4 90-day rule). Record dates + quotes. Any automation-posture change → immediate AMBIGUOUS escalation to operator.
- **Phase 1 — execution-expression inventory.** Locate `striker_nas100_v1_mnq.pine` (search local stores; if lost, flag re-author-from-locked-source as an operator-authorized sub-task — precedent 2026-07-06). Diff both FUTURES_LOCK sheets' venue constants against Tradeify/MFFU (`firm_rules.py` + envelope rows): costs, caps (80 micro), EOD times, day-stop default. Emit the per-edition delta list. **No Pine edits in this phase.**
- **Phase 2 — fidelity precondition scoring (F1–F5).** F1 **DONE 2026-07-17** (`PASS-via-fallback` via Q-PYRPARITY-1). F2: recompute floors at current ATR from the CME panels (sha `15d8b`/`beabf`), both legs, at 0.50×; verify add-leg integer survival explicitly (adds cohort, not aggregate — ECR lesson). F4: confirm chart/alert timing fits MFFU 16:10 ET minimum.
- **Phase 3 — rail architecture selection.** Per tier, document the concrete chain (TV alert → CrossTrade → NT8→Rithmic *or* Tradovate direct) from CrossTrade/firm primary docs; attended-operation posture (who is present, when — Mon/Tue/Thu-style session windows per leg); failure modes (missed alert, partial pyramid fill) with manual-intervention protocol.
- **Phase 4 — assemble the GO/NO-GO packet.** One page: F-scorecard, costed chain per tier (eval fee + monthly platform/data + bridge + per-side commission, sourced fresh in Phase 0/1), WATCH-1 practicality restated (~2× median days-to-pass at pass-rate ≥95%), and the standing risk framing the operator must see next to the GO: Q-DECAY-1 (common-mode edge death uncovered — detection is by drawdown), Q-PERSIST-1 (+0.46pp MC bust optimism, decompounded basis), regime-conditionality of the book (H1 rescue is the haircut's doing). **Re-request the §8 ceiling here** — present the assembled cost table and ask the operator to set (or decline) a budget ceiling against it; this is the one place in the plan where a fresh operator number is required. Present the full packet; stop. The GO is not this brief's to make.

---

## §8 — Verdict pre-registration (operator-signed at ratification)

**FROZEN 2026-07-17** at `docs/briefs/pre-registration/Q-RAIL-1-verdict-preregistration.md` — the §6 table plus the two operator-set items below, transcribed verbatim.

**Operator ratification (chat, 2026-07-17):** "ratify Q-RAIL-1 and Q-PYRPARITY-1, sign the §8 budget," followed by an `AskUserQuestion` clarification (the two items below were genuinely operator-only — no eval-fee pricing exists anywhere in the repo to derive a ceiling from, and tier preference is a first-order preference call, not a derivable fact):

- **Target tier preference** if both clear (Tradeify Select vs MFFU Rapid): **"Packet decides"** — operator selected the no-pre-set-preference option; Phase 4 recommends based on whichever tier clears cleaner / costs less once both are scored.
- **Budget ceiling** for all-in cost-to-first-live-fill (eval fee + 3 months of run-rate): **DEFERRED to Phase 4.** Operator selected "defer to post-Phase-0" over "set it now" — no dollar figure is set at ratification. Mechanism (this is the operative rule, not a placeholder): Phases 0–3 proceed fully unblocked (none reference a ceiling); Phase 4 assembles the real cost table from Phase 0/1 sourcing and **re-requests a ceiling from the operator at that point** — a fresh sign-off, not an automatic multiple or a silently-assumed number. H-RAIL-1's cost clause (§4) stays PENDING until that sign-off; §6's RESOLVED/FALSIFIED verdict on the cost axis cannot fire before it.

Pre-registration commit hash: this commit — see `git log --oneline -- docs/briefs/pre-registration/Q-RAIL-1-verdict-preregistration.md` · Date: 2026-07-17

---

## §9 — Closure record format

- `RESOLVED` → `docs/briefs/closures/Q-RAIL-1-closure-resolved.md` + the GO/NO-GO packet as its annex (the packet is the recommendation artifact).
- `FALSIFIED` → `docs/briefs/closures/Q-RAIL-1-closure-falsified.md` with the failed F-limb's evidence quoted.
- `AMBIGUOUS-HOLD` → carried into the 08-08 packet (rank-4 brief) with the blocking input named.

---

## §10 — Audit hooks (runnable)

```bash
# Gating language intact until the operator GO exists (expect matches in all three)
grep -n "separately gated" lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md
grep -n "rail-build, account-registration, or live-spend" docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md
grep -rn "Q-RAIL-1" docs/SESSIONS.md   # the executing session must cite this brief (Trap #10)

# Tier-1 constants unchanged since §0 (re-run before Phase 2 arithmetic)
grep -n "Tradeify_Select_100K\|MFFU_Rapid_100K" -A 13 core/firm_rules.py | grep -n "max_dd_pct\|cost_per_side_usd\|micro_contract_cap\|consistency_rule_pct"
git log -1 --format='%h %cs' -- core/firm_rules.py     # a53ee99 at authoring; investigate any drift

# MNQ edition inventory question (Phase-1 input; MISSING on disk at authoring)
ls core/strategies/nas/striker_nas100_v1_mnq.pine 2>/dev/null || echo "STILL MISSING - Phase 1 must resolve"
grep -n "striker_nas100_v1_mnq.pine" core/strategies/PORT_MANIFEST.sha256

# No build-before-GO (expect zero rail artifacts in-repo until a GO ADR exists)
git log --oneline --all -- "**/crosstrade*" "**/nt8*" | head -5
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md --type inquire
git log -1 --format='%h %cs' -- core/firm_rules.py docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md
grep -n "WATCH-1 (0.50×)" lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md
```

## Ratification record

Ratified 2026-07-17 (operator, chat: "ratify Q-RAIL-1 and Q-PYRPARITY-1, sign the §8 budget"; tier-preference and budget-deferral decisions captured via `AskUserQuestion` same session — see §8). §8 pre-registration frozen same date. Phase 4 owes a fresh operator ceiling sign-off against the assembled cost table before H-RAIL-1's cost clause can resolve. **Phases 0–3 + 1b + F1–F5 complete 2026-07-17** ([`RESULTS`](../../lab/analysis/c1/q_rail_1_2026-07/RESULTS.md)): F1 `PASS-via-fallback` · F2 `PASS` · F3 `PASS` · F4 `PASS` · F5 `PASS`; rail [`PHASE3.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE3.md); C3 [`STEP3_1C.md`](../../lab/analysis/c1/q_rail_1_2026-07/STEP3_1C.md). **Phase 4 complete 2026-07-17:** cost table assembled ([`PHASE4.md`](../../lab/analysis/c1/q_rail_1_2026-07/PHASE4.md)); operator signed the deferred §8 ceiling at **$700** (fresh sign-off per the frozen mechanism) → cost clause ACCEPTS at both tiers → **`RESOLVED`**. The rail-build/account/live-spend GO is a separate fresh operator decision + ADR.
