# Audit Note — Object-layer audit: `core/` conclusions vs the retired FXIFY/CFD ground truth

**Audit ID:** AUDIT-2026-07-11-core-fxify-anchoring
**Date:** 2026-07-11
**Triggered by:** operator directive (this session): "many of the locked parameters and ground truths were based in numbers that no longer apply (CFD, FXIFY rules oriented) — retire conclusions, question assumptions about what to keep." Formally: retirement back-propagation (operational-rules Rule 11 class) onto the `core/` conclusion set, after the 2026-07-10 batch (FXIFY formally closed; R6 futures-prop NO-GO) foreclosed the prior audit's critical-path re-arm action.
**Authors:** Joshua (operator) + Claude Code (this session, worktree `core-parameter-evaluation-7f4f3a`)
**Scope:** object layer — the FXIFY/CFD-anchored claims carried by `core/` (+ their `ops/` consumers): the MC anchor and its gate semantics, `dd_protection` calibration grounds, `firm_rules` contents, the multiplier system, parsers, and the standing quarterly-trigger criteria. **Not in scope:** any parameter-axis edit (SL/TP/ATR/risk%/pyramid/Pine — LOCKED, immutable), any dd_protection constant change (frozen; re-MC-gated), re-adjudication of individual research closures (spawned as follow-up §5.4).
**Window:** 2026-07-01 → 2026-07-11 (since AUDIT-2026-07-01-portfolio; the events that void the claims land 2026-07-09/10).
**Method:** Rule-0 production reads first (all constants below verified on disk this session, not from docs); prior audit's §10 hooks re-run; evidence assembled (§0–§3) before the verdict (§4) was written.
**Layer discipline:** no conclusion below cites methodology-audit verdicts. Research-loop *outcomes* (venue falsifications, re-MC numbers) are the empirical evidence this layer owns.

---

## §0 — Source anchors (Rule-0 reads, this session)

- `core/firm_rules.py:5-207` — 10 firm configs: FXIFY (venue **formally closed** 2026-07-10), Bulenox ×5 (R6 **NO-GO**, no account ever registered), Tradeify Select ×4 (re-MC **§4 FALSIFIED** — see below). `ACTIVE_FIRM = "FXIFY"` (:206) — the "single switch point" names a closed venue. `BASELINE_BALANCE = 200_000` (:229); `_BASE_RISK` 0.0034/0.0070/0.0150/0.0037 (:225) — byte-stable, untouched.
- `core/dd_protection.py:47-59` — `_F = FIRM_RULES[ACTIVE_FIRM]`; `PROFIT_TARGET`/`DAILY_LOSS_LIMIT`/`STATIC_DD_LIMIT` all FXIFY-derived; `DD_TRIGGER 0.015` / `DD_SCALE 0.40` intact with MVD spec pins (:255-264). `STARTING_EQUITY` hard-locked to 200,000 in state validation (:106-109). Display banner "FXIFY $200K CHALLENGE" (:281), target/halt lines keyed to FXIFY static-DD framing (:287-301). **Latent defect:** `:52` computes `_F["daily_loss_pct"] / 100` — a `TypeError` at import for 9 of the 10 configured firms (`daily_loss_pct: None` on every Bulenox/Tradeify tier). Same pattern `core/mc/modes.py:53`.
- `core/mc/modes.py:1-118` — the MC is by its own docstring a "**challenge-outcome simulator**": `PROFIT_TARGET = 210_000`, ±5% daily/static barriers, `MIN_TRADING_DAYS 5`, `INACTIVITY_LIMIT 60` (FXIFY-correct timeout, ADR 2026-05-16) — the 99.83/0.17/4.37 anchor is **by construction P(pass an FXIFY $200K challenge)**.
- `tests/core/test_mc_anchors.py:81-83,121-130` — anchor pins 0.9983/0.0017/0.0437 (abs 1e-4) + lock gates "bust <1%, p99 DD <5%" — challenge-survival criteria.
- `core/lifecycle.py:1-80` — authorization ladder (1.00/0.50/0.25/0.00×) + beta-death controls; venue-agnostic; behavior-neutral at all-AUTHORIZED.
- `core/csv_parser.py:1-60` — DXTrade (Alchemy/FXIFY) parser; the emitting venue no longer exists.
- `ops/accounts.py:48-85`, `ops/cli.py` — `FxifyChallengeStatus`, `challenge` command (FXIFY validator), `lots` multiplier vs the $200K baseline. Zero accounts exist or can exist (all 10 firm configs reference closed/falsified programs).
- `lab/archive/tradeify_selectflex_remc_2026-07-10/RESULTS_tradeify_remc_2026-07-10.md` — every tier × every config row **FAIL** (best bust 3.03% ≥ 1%); no tier-shopping occurred.
- `docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md` — R6 NO-GO; Bulenox/Tradeify configs retained "for provenance … not as live targets" (§2.1); Aegis→M6J sole active lane (go-live separately gated).
- `scripts/verify_lock_anchors.py` run this session → **ROUTING: Closed** (zero numeric drift anywhere).
- Prior audit §10 hooks re-run: 2026-05-23 ADR + decompound-HOLD both carry the 2026-07-01 DORMANT addenda (§5.1 done); zero-fills attestation retired 2026-07-10 unrun (§5.5 moot); **§5.2 (restore falsifiability via the futures chain) foreclosed by R6 NO-GO** — the prior audit's STABLE-conditional condition failed.

**Failure class:** venue-retirement back-propagation onto a claim set whose referent (the FXIFY challenge) was withdrawn — not parameter drift, not belt-patching.

---

## §1 — The finding in one paragraph

Nothing in `core/` drifted; the *questions* its headline numbers answer were retired out from under them. The MC anchor is a challenge-pass probability for a challenge that is formally closed; the lock gates are challenge-survival criteria; the C2 dd_protection calibration was chosen partly on a days-to-**pass** objective; the quarterly C2→C0 revert trigger is denominated in challenge pass-rate; the multiplier system scales Pine lots to prop accounts of which zero exist or can exist; and `ACTIVE_FIRM="FXIFY"` silently parameterizes both `dd_protection` and the MC while naming a closed venue. Left as "current canonical," these claims become unfalsifiable-by-construction — the exact degradation path the 2026-07-01 audit warned starts "without any of the seven signals firing." The repair is a claim-scope re-classification (retire / keep / re-derive), **not** any parameter or constant change.

---

## §2 — Claim inventory (the deliverable)

### Class R — RETIRE as live claims → re-scope to historical record (operator ratification per item)

| # | Claim / surface | Evidence | Disposition |
|---|---|---|---|
| R1 | **99.83/0.17/4.37 as "current canonical" MC anchor.** It is P(pass FXIFY $200K challenge); the challenge closed 2026-07-10. Can never again be falsified by live outcome. | `core/mc/modes.py:51-65`; ADR 2026-06-30 +07-10 addendum | Re-scope to **historical (challenge-era) calibration record + engine regression pin**. The number stays pinned in tests for byte-reproducibility of the engine; it stops being a claim about anything live. |
| R2 | **Lock gates "bust <1%, p99 DD <5%" as live acceptance criteria.** Challenge-survival gates: the 5% static barrier and pass-timeout don't exist on self-funded capital. | `tests/core/test_mc_anchors.py:121-130` | Retire as live gates; retain as the historical lock criteria. Successor gates derived from operator self-funded risk tolerance (→ D1). |
| R3 | **C2 calibration grounds.** The 2026-05-08 C2 relock accepted a failed regime-robustness gate on (a) broker-feed confirmation and (b) **median-days-to-pass** benefit — a challenge-only objective now void. Constants stay frozen (no edit proposed); the *justification* no longer holds. | `core/dd_protection.py:5-16,55-59`; ADR 2026-05-08 | Flag for the 2026-08-08 review: re-derive the C2-vs-C0 objective as pure DD-tail control (Q-DDTRIG-1's regime-gate findings carry over as inputs) **before** the revert check runs on dead semantics. |
| R4 | **Quarterly C2→C0 revert criterion** ("rolling 6-month MC pass-rate <95% ×2 windows") — denominated in a retired metric; mechanically it simulates a ghost venue. | CLAUDE.md §Protection; STATE.md forward board | Re-derive in venue-neutral terms (DD-tail / bust-line on successor semantics) or explicitly mark the 08-08 run as historical-semantics-only. |
| R5 | **The multiplier system as the repo's operational purpose.** CLAUDE.md §Purpose ("multiplier per account"), `ops/accounts.py`, `cli.py lots/challenge`, `fxify_rule_validator.py`: zero accounts; surviving lane sizes **integer micro-contracts**, not lot multipliers. | `ops/accounts.py:48-85`; `ops/cli.py:197` | Dormant-historical. The Purpose statement itself is a retired conclusion; successor purpose = operational layer for the self-funded futures lane(s). |
| R6 | **`ACTIVE_FIRM="FXIFY"` as live config + the Firm-Expansion doctrine** ("add a firm… everything downstream adapts automatically"). Falsified in production: `daily_loss_pct=None` crashes `dd_protection.py:52` / `mc/modes.py:53` for 9/10 configured firms; each firm class needed bespoke engine branches (`bust_trailing`, `trailing_locking`). Anchor byte-reproducibility currently *depends* on the FXIFY fixture. | `core/firm_rules.py:206`; `core/dd_protection.py:52` | Relabel `ACTIVE_FIRM` as the **historical anchor fixture** it now is; retire the everything-adapts doctrine; any future firm onboarding gets its own engine-support pre-flight. |
| R7 | **DXTrade surfaces:** `core/csv_parser.py` (Alchemy/FXIFY format), contractValue operational lore (DJ30=10 warning), DXTrade-fill-denominated conclusions. | `core/csv_parser.py:1-60` | Archival — retained for historical reconciliation only; no live consumer. |
| R8 | **"AUTHORIZED @ 1.00×" read as live-capital authorization.** The tier is real governance, but it currently authorizes zero live capital anywhere; "LIVE @ x%"-style strategy claims are CFD-era. | `core/lifecycle.py`; CLAUDE.md Strategy Reference | Keep the lifecycle axis (K3); re-read AUTHORIZED as "eligible for a venue that must itself pass its own transfer/go-live gates." |

### Class K — KEEP (venue-agnostic, still earning existence — do not over-retire)

| # | Surface | Why it survives |
|---|---|---|
| K1 | Parameter-axis locks + Pine + `MANIFEST.sha256` | The axis separation (ADR 2026-07-10 lifecycle) is exactly what makes clean retirement possible without touching parameters. |
| K2 | `dd_protection` **mechanism** (peak-DD trigger → scale) + MVD pins + state validation | Venue-agnostic portfolio control. Only its *calibration grounds* are void (R3), not the rule form. |
| K3 | `core/lifecycle.py` ladder + beta-death controls | Born post-pivot; venue-agnostic; the 08-08 machinery rides on it. |
| K4 | MC **engine substrate**: week-block bootstrap, panel ingestion, MVD gates | Importable and already reused (discovery-campaign breadth path). The engine survives; only the FXIFY question it was configured to answer retires. |
| K5 | TV/Pepperstone panels + manifest gates + loaders (`tv_export_loader`, `bar_export_loader`, `tv_schema`) | Canonical research feed, independent of execution venue. |
| K6 | Panel-level empirical findings: 2020-23/2023-26 regime split, 2024 structural shift, decompounded re-MC + withdrawal-model machinery | **More** decision-relevant under self-funded framing, not less — the decompound instrument is the closest existing model of self-funded reality (see D1). |
| K7 | The venue-falsification corpus (DJ30→MYM 0.559×; NAS100 dead on micros; no prop tier clears) + `rejected_candidates.md` re-proposal bars | Freshly earned futures ground truth. **Venue retirement is not new mechanism evidence** — no rejection registry entry re-opens because of this audit. |

### Class D — RE-DERIVE (successor questions; each needs its own pre-registered artifact)

| # | Question | Note |
|---|---|---|
| D1 | **Successor risk framework for self-funded capital.** What replaces P(pass)? Candidates: P(breach operator max-DD line), time-under-water, withdrawal sustainability. | The decompound-remc machinery (2026-06-07, +withdrawal/$200K-reset) is the closest existing instrument — and on it **both old gates breach** (clean vintage 98.53/1.47/5.32, hard regime-split). The successor framing likely *tightens* risk conclusions; retiring the challenge framing is not a loosening. |
| D2 | **dd_protection objective re-derivation** (no pass-time term). | Inputs carry over: Q-DDTRIG-1 (1.0% passes §4, fails regime gate → HOLD), Q-DDP-1 sweep, regime-robustness gate. Operator decision at 08-08; any constant change stays re-MC + ADR-gated. |
| D3 | **Single-lane book ≠ 4-leg portfolio.** If Aegis→M6J goes live alone, the 4-leg anchor and portfolio-peak dd_protection describe a book that isn't live. | Prior audit already pinned: a book that drops legs "must be re-MC'd before it can claim the anchor." Same holds self-funded; the go-live gate needs its own sizing/risk artifact (integer M6J contracts, force-flat venue, ~0.5× preservation). |
| D4 | **$200K Pine baseline.** | Keep as the locked Pine sizing convention (parameter axis); retire the challenge connotation. The M6J translation is a separate parity artifact, not a re-baseline. |

**Re-scope principle for research closures (feeds §5.4):** a closure whose *verdict* rests on challenge-gate numbers (pass/bust %) gets a one-line annotation "gate-denominated; directional/panel-level finding survives"; closures on panel-level grounds (edge, cost-law, regime) stand unmodified. Rejection registry re-proposal bars stand everywhere.

---

## §3 — Seven diagnostics (evidence per §0/§2)

1. **Hard core integrity — YELLOW.** Parameter/code core intact: verifier Closed, MVD pins intact, zero ungoverned changes in-window. But the object layer's empirical hard core is now part-**orphaned** (not violated): its headline claims are about a venue that no longer exists, and no document yet re-scopes them. This audit is that document's precursor.
2. **Belt churn — GREEN.** Window adds: Tradeify ×4 + `trailing_locking` branch (research-scoped, KeyError-safe), lifecycle wiring (behavior-neutral). Removes/closures: FXIFY closed, attestation retired unrun, 4 investigation retirements, R1–R8 + the futures-prop fan-out closed. Prune-dominant again. Watch: `firm_rules` is now **10/10 dead-program configs** retained as provenance — acceptable per R6 §2.1 but must be labeled as provenance, not config (R6 row above).
3. **Progressive evidence — YELLOW.** The falsifier machinery fired correctly and repeatedly (P2 gate → R5 FALSIFIED → residual §4 → R6 NO-GO; Tradeify re-MC reported FAIL on every tier rather than tier-shopping). Real empirical surplus: **venue cost structure is load-bearing to the edge** (0.559× on the strongest transfer candidate). But the live-corroboration channel is now zero with no dated re-arm — worse than 07-01's "narrowed."
4. **Degeneration evidence — GREEN, with the drift vector named.** No post-hoc rescue anywhere in-window; closures were falsifier-driven. The one path to degeneration is *inaction*: keeping "current canonical" framing on challenge-denominated claims after the venue died converts them to unfalsifiable boilerplate. That is precisely what §2 Class R repairs.
5. **Boundary respected — GREEN.** No parameter edits; R6 §5 forbidden moves intact (no rail built, no grid re-run, no GO-CONDITIONAL relabel); lifecycle wiring behavior-neutral at 1.0×; no quiet re-proposals.
6. **Theory-comparison — GREEN.** CFD-vs-futures resolved with real numbers: the CFD-era conclusions were venue-conditional and the venue condition is now *known* load-bearing. This retro-validates M-SWAP-1-class caution about anchor portability and grounds R1/R2.
7. **Falsifier check — YELLOW→RED trend.** Zero numeric drift (verifier Closed). But the dormant-limb population **grew** and acquired second-order dormancy: the 2026-05-23 ADR limbs 2–3 re-arm condition ("when the futures automation chain goes live") is itself foreclosed by R6 NO-GO; decompound-HOLD limb 1 permanently dormant; the C2→C0 revert criterion (R4) and the Call-1 rolling-live-PF feed are semantically void/starved. The majority of the standing falsifier surface for `core/` conclusions is now dormant or denominated in a retired metric.

---

## §4 — Proposed disposition (written after §0–§3)

**Object layer: PROPOSED STABLE — final window under the challenge framing; flips to DEGENERATING at next cycle if the §5 re-scope slate has not landed by 2026-08-08.**

Grades: #1 yellow · #2 green · #3 yellow · #4 green · #5 green · #6 green · #7 yellow-red.

Not Degenerating today: nothing was patched, rationalized, or drifted — the window's discipline was exemplary (falsifiers fired and were honored at real cost). Not Progressive: the corroboration channel is dark and the headline claim set is orphaned. The 07-01 verdict was STABLE *conditional on re-arm*; the primary re-arm path has since been closed NO-GO, so the condition has failed in its original form — the successor condition is the §5 slate. The deadline is 2026-08-08 because the quarterly machinery (C2→C0 check, decay review, beta-death review, accept-beta fork) otherwise executes mechanically on challenge semantics.

---

## §5 — Spawned follow-ups (operator ratification; CC drafts)

1. **Anchor re-scope ADR** (covers R1+R2+R8): re-scope 99.83/0.17/4.37 to historical challenge-era calibration + engine regression pin; retire the lock gates as live criteria; restate CLAUDE.md's MC-anchor and Strategy-Reference framing accordingly. Explicitly NOT a re-pin, NOT a parameter change, NOT a test edit beyond labeling. **Before 2026-08-08.**
2. **Successor risk-framework Pre-Q** (D1, feeds D2/D3): define the self-funded question set (max-DD line, time-under-water, withdrawal model) with the decompound machinery as instrument; pre-register before any number is produced. **Target: alongside the 08-08 slate; blocks Aegis→M6J go-live gate design.**
3. **08-08 trigger-semantics patch** (R3+R4): one-page decision note re-deriving (or explicitly historicizing) the C2→C0 revert criterion before the quarterly run; dd_protection constants untouched pending D2.
4. **Claims-inventory sweep of research closures** (§2 re-scope principle): annotate gate-denominated verdicts ("directional finding survives"); confirm zero rejection-registry re-opens. One session.
5. **Provenance labeling commit** (R5+R6+R7): docstring/comment-level relabels — `ACTIVE_FIRM` as historical anchor fixture, firm_rules header noting 10/10 configs are provenance, CLAUDE.md §Purpose successor statement, csv_parser archival note. No behavior change; validators must stay green.

---

## §7 — Programme-audit signal check (this layer)

- [ ] Belt-patches without independent corroboration? **No.**
- [ ] Belt only grows? **No** — prune-dominant; but firm_rules content is 100% provenance now (label it).
- [x] **Falsifier thresholds drifting? No numeric drift — but the dormant/void share of the falsifier surface is now majority, with second-order dormancy (re-arm conditions foreclosed).** Repair = §5.1/§5.3.
- [ ] Invoked to rationalize? **No** — this audit was operator-triggered to *retire* conclusions, the opposite failure mode; evidence was assembled before the verdict.
- [ ] SNAG pattern? Prior-audit SNAG (5th-leg) closed into the registry; no new same-domain null-run in-window.
- [ ] Cross-layer contamination? None cited.
- [ ] Negative heuristic crossed? **No** — and note the over-correction guard: retiring challenge framing must not become a backdoor to re-optimization (K7 bars stand).

---

## §10 — Audit hooks (runnable at next cycle)

```bash
# Did the re-scope slate land before the quarterly?
grep -n "historical" core/config/params.toml docs/adr/2026-0[78]-*anchor* 2>/dev/null
grep -rn "challenge-era\|historical calibration" CLAUDE.md | head -5
# Is the C2→C0 criterion still pass-rate-denominated?
grep -n "pass-rate\|95%" CLAUDE.md STATE.md | head -5
# ACTIVE_FIRM still silently live-parameterizing?
grep -n "ACTIVE_FIRM" core/firm_rules.py core/dd_protection.py core/mc/modes.py
# Successor framework pre-registered?
ls docs/briefs/pre-registration/ | grep -i "selffunded\|self-funded\|successor" || echo "NOT YET"
# Constants still pinned / zero drift
python scripts/verify_lock_anchors.py   # expect ROUTING: Closed
```

---

## §11 — Closure

- **Status:** `Closed (evidence assembled before verdict; verdict RATIFIED same-day — operator directive "retire, but do not over-retire"; §5 slate partially executed same-day)`
- **Verdict:** object layer **STABLE (final window under challenge framing)** — conditional demotion to DEGENERATING at next cycle if §5.1–§5.3 have not landed by 2026-08-08.
- **§5 execution status (2026-07-15):** §5.1 + §5.3 + §5.5 **DONE** (2026-07-11 rescope ADR). §5.2 (successor risk-framework Pre-Q / D1) **DONE** 2026-07-15 — Q-SFRISK-1 `RESOLVED`, admitting ADR `Accepted` (discharges rescope ADR §4 completion falsifier). §5.4 (gate-denominated-closure annotation sweep) **DONE** 2026-07-15 — inventory + 6 annotations + rejection-registry standfast confirmation at [`2026-07-15-gate-denominated-closure-annotation-sweep.md`](2026-07-15-gate-denominated-closure-annotation-sweep.md). **Parent §5 slate complete.** Remaining broader-board item (not §5): D2 calibration re-derivation at the 2026-08-08 review.
- **What this audit does NOT do:** edit any locked parameter, dd_protection constant, allocation, Pine byte, or test pin; re-open any rejected candidate; authorize any go-live.
- Predecessor: `2026-07-01-portfolio-audit.md` (its STABLE-conditional condition failed in original form; superseded by this audit's §5 slate).
