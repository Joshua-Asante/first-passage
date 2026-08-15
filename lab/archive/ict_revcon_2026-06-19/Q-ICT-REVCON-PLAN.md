# Q-ICT-REVCON — ICT 1H follow-through (reversion vs continuation) + entry-mechanism re-examination

**Status:** `CLOSED 2026-06-19 — NOT-CONFIRMED` (Phase 0b AMBIGUOUS on the out-of-sample 2022-bear → forward-watch belt; the 1H layer carries no confirmed conditional edge on either axis)
**Authored:** 2026-06-19
**Phase 0a result:** [`PHASE-0A-FINDINGS.md`](PHASE-0A-FINDINGS.md) — probe FAITHFUL (no M-15 defect); regime axis starved/contradicts the motivating story; bias-sign axis favored (prem→down|bearish ≈ 0.60). EXPLORATORY, NOT a verdict.
**Phase 0b result:** [`CLOSURE-1H-REVCON-AMBIGUOUS.md`](CLOSURE-1H-REVCON-AMBIGUOUS.md) — confirmatory on the out-of-sample 2022-bear (14615 bars): **AMBIGUOUS** → CLOSED NOT-CONFIRMED. The 0a headline cell non-replicated (0.60→0.46); the bear-page stride-clearers are bias-drift near-misses failing the robust block CI. disc-reverts-up-under-bullish ≈ 0.58 = forward-watch belt.
**Closed:** 2026-06-19 (NOT-CONFIRMED)
**Authors:** Joshua (operator) + Claude Code
**Parent question:** N/A (this IS the parent; two forked sub-questions below, gated)
**Sub-questions opened:** **Q-ICT-1H-REVCON-1** (Phase 0, ungated) · **Q-ICT-1M-ENTRY-1** (Phase 1, GATED on the Phase-0 decision gate §6)
**Loop:** Inquire-phase Pre-Q. Phase 0 closes on its §6 gate; Phase 1 opens only if the Phase-0 gate licenses it. The diagnose-first structure was operator-chosen 2026-06-19 (AskUserQuestion).
**Artifact path:** `lab/analysis/ict_revcon_2026-06-19/Q-ICT-REVCON-PLAN.md`

> **This is a planning artifact authored 2026-06-19 for next-session execution.** It builds on the **CLOSED** Q-ICT-CASCADE-1 (1H FALSIFIED, 1M INSUFFICIENT-N). Those verdicts STAND — this is re-investigation + strategy-dev, not a reopening or a re-tune.

---

## §0 — Rule 0 reads (production-source verification)

All read in-session 2026-06-19. The Pine sources are **gitignored** (`.gitignore:75` → `**/*.pine`) and live in `C:\Users\joshu\Downloads\` → **CITATION-CHAIN mode** (file + bytes + LastWriteUTC; re-anchor on resume, Downloads is mutable). Readable repo files are the Tier-1 corroboration (the harness encodes the Pine definitions verbatim; the closures quote the numbers).

| Source | Tier | Anchor | What it grounds |
|---|---|---|---|
| `lab/analysis/ict_cascade_2026-06-18/harness_1h.py` | 1 (readable) | working tree, modified 2026-06-19 (decision-bar `recompute_hits` post-M-15 fix; `_pine_resolution_hits`; stride/block/placebo/effective_n machinery to be REUSED) | the instrument Phase 0a extends; the de-overlap/placebo/n-floor primitives |
| `lab/analysis/ict_cascade_2026-06-18/CLOSURE-1H-FALSIFIED.md` | 1 (readable) | new this session | the falsified reversion verdict (prem→down 0.4725 / disc→up 0.5430, both straddle 0.5; single benign regime) this re-examines |
| `lab/analysis/ict_cascade_2026-06-18/PREREG-1H.md` | 1 (readable) | committed cascade artifact | frozen 1H config (lookN=60, eqBand=0.05, fwdK=12, zone polarity, bias-conditioned 1H-E3) — Phase 0 reuses the config, NOT the verdict |
| `lab/analysis/ict_cascade_2026-06-18/CLOSURE-1M-INSUFFICIENT-N.md` | 1 (readable) | new this session | the 1M 0%-fill diagnosis (247 placed / 0 filled / all expire) + F9 + the 1m data wall driving Phase 1's TF-agnostic design |
| `ict_1h_premium_discount_DRAFT.pine` | 2 (gitignored, citation-chain) | **7554 B / 2026-06-18T22:42:04Z** (re-anchored 2026-06-19; benign −2B publish substitution vs PREREG-1H §0's 7556 B) | the `zone`/`zoneGate`/follow-through definitions (L44-86, L143-149) Phase 0 measures |
| `ict_1m_execution_DRAFT.pine` | 2 (gitignored, citation-chain) | **22180 B / 2026-06-18T22:42:25Z** (re-anchored 2026-06-19; benign −2B vs PREREG-1M §0's 22182 B) | the entry mechanism under re-design: `entryMode="limit-on-return"` L47, `fillEdge="mid"` L50, `retraceK=6` L54; gate L118-121; arm L171-189; entry/fill L223-295 |
| `ops/instruments/SPX500.md` | 1 (readable) | updated 2026-06-19 (F9; anti-SNAG 3/3) | instrument governance; F9 = execution non-viable on 1m, instrument-general |

**CC verification on resume (Phase 0 of next session):** re-anchor the two `.pine` files (PowerShell `LastWriteTimeUtc`); if bytes/UTC differ from the table → RE-READ before trusting line citations. Confirm `harness_1h.recompute_hits` is the decision-bar form (`zone[i]==1 and close[j]<close[i]`) — the M-15 fix must be in place before any continuation probe is added on top of it.

---

## §1 — Context & motivation

Q-ICT-CASCADE-1 closed 2026-06-19 with **no deployable edge**: the 1H premium/discount layer FALSIFIED (premium→down and discount→up both straddle 0.5 on a single benign uptrend window) and the 1M execution layer hit INSUFFICIENT-N (0% limit-fill, 247 placed/0 filled, plus a 1m multi-regime data wall). The two failures rhyme: **both are mean-reversion premises that didn't pay** — premium "reverted down" (it didn't; it continued up in the trend) and the entry waited for price to "retrace into the FVG" (it didn't; displacement FVGs continued). Standing doctrine that bears: the 1H verdict itself flagged "single benign regime" as its key limitation and routed to a multi-regime re-test (PREREG-1H path-independence note); INQHIORI §6 (reformulate the question, not the hypothesis, at tail-exhaustion); `strategy-validation` (selection/pre-registration before sweeps); F9 (execution non-viability is instrument-general). The operator chose (2026-06-19) to **diagnose before redesigning**.

---

## §2 — Prior art / lineage

- **Q-ICT-CASCADE-1 (CLOSED 2026-06-19)** — parent campaign. W RESOLVED (structure-only), D SSL-RESOLVED/BSL-FALSIFIED, **1H FALSIFIED**, **1M INSUFFICIENT-N**. The 1H + 1M closures are the direct inputs. Lesson **M-15 / M-ICT-1H-OFFSET** (the harness offset defect, fixed) means `recompute_hits` is now trustworthy as the Phase-0a base.
- **Q-ICT-SWEEPFVG-1 / D2 (FALSIFIED 2026-06-17)** — the ICT-geometry sibling on US500 **15m**; its existence proves 15m US500 has multi-regime history (relevant to Phase 1's TF choice). F6 (direction real, p=0.0144) + F8 (pseudo-replication / tradeability floor / single-window-≠-generalizable) bind any re-test.
- **F9 (SPX500 ledger, 2026-06-19)** — the 1M execution layer is un-runnable on the 1m feed; the 0%-fill is an entry-mechanism property (instrument-general), the 1m cap is platform-wide. This is the motivation for Phase 1 being TF-agnostic and gated on data availability.
- **Genuinely new surface:** the *conditional* (regime/bias-dependent) follow-through framing is new — the cascade tested only the unconditional reversion direction + a bias-conditioned variant it never got to evaluate (the 1H verdict's 1H-E3 required a weekly-bias join it did not exercise to a conclusion).

---

## §3 — Question

**Pre-Q gate (symptom-only rephrase):** "The 1H P/D split did not predict subsequent direction (reversion straddled 0.5) on the one window tested, and the 1M entry mechanism filled 0 of 247 orders — what does the split actually predict, is that conditional on regime, and why does the entry not fill?" (Names the symptoms — failed prediction, zero fills — not a fix.)

- **Q-ICT-1H-REVCON-1 (Phase 0, ungated):** Does the 1H premium/discount split carry directional follow-through that is **conditional on regime and/or weekly-bias sign** (e.g. premium reverts *down* in chop/bear but continues *up* in trend/bull), measured de-overlapped, placebo-beating, and multiplicity-penalized on a genuinely multi-regime 1H window?
- **Q-ICT-1M-ENTRY-1 (Phase 1, GATED):** Given a confirmed Phase-0 directional signal, what TF-agnostic entry mechanism produces a *fillable, validatable* population (the locked `limit-on-return/mid/retraceK=6` fills 0%), and on what timeframe can it be validated multi-regime?

---

## §4 — Falsifiable hypotheses

**H-1H-REVCON (Phase 0):** On a multi-regime 1H window, the P/D follow-through direction is **regime/bias-conditional** — there exists a partition (chop-vs-trend, or weekly-bias sign) under which one directional rate (reversion *or* continuation) clears 0.5 by ≥2pp de-overlapped, beats its regression-to-the-range placebo, and survives the multiplicity penalty.
- **Reject H-1H-REVCON if:** in EVERY pre-registered partition, BOTH the reversion rate AND the continuation rate de-overlapped CIs straddle 0.5 after the penalty (the split carries no directional information in any regime/bias bucket — the layer is dead and there is nothing for an entry to gate on).
- **Accept H-1H-REVCON if:** at least one pre-registered partition's directional rate clears 0.5 by ≥2pp under BOTH stride and block estimators, beats placebo, and survives the penalty — AND the partition variable is observable at decision time (not a hindsight regime label).
- **Ambiguous-hold if:** a rate clears in-sample on the existing window but the multi-regime confirmatory run (0b) is starved (effective-N < floor) in the candidate partition → re-spec the export window.

**H-1M-ENTRY (Phase 1, gated):** A TF-agnostic entry variant (chosen by Phase 0's direction) produces ≥100 closed trades on a multi-regime window at the gate-chosen TF, with post-cost E[R] block-CI lower bound > 4× median-hurdle.
- **Reject if:** no entry variant clears the n-floor on any available multi-regime TF (execution remains un-validatable — F9 stands, the concept is undeployable), OR a fillable population's E[R] CI ⊆ (−∞, hurdle].
- **Accept if:** a pre-registered entry variant clears n≥100 AND the E[R] gate AND drop-top-k AND the slice permutation, at a TF with multi-regime history.

---

## §5 — Forbidden moves

- **Treating Phase 0a (existing 6.5-mo export) as a confirmatory verdict.** The reversion FALSIFIED was already produced on that exact data; a second hypothesis (continuation/conditional) scored on the same data is **exploratory / hypothesis-generating only**. Confirmatory evidence MUST come from the fresh multi-regime 0b export, pre-registered before scoring. Reading 0a as a PASS is methodology-layer p-hacking (Known Trap #12; INQHIORI §5).
- **Re-tuning the falsified reversion framing to make it pass.** The continuation/conditional hypothesis is a NEW falsifiable H (INQHIORI §6 reformulate-the-question). Sweeping eqBand/lookN/fwdK on the reversion claim to lift it above 0.5 is a re-tune of a closed verdict — forbidden.
- **Picking the winning partition after seeing the data ("best-of-K regime label").** The partition set (which regimes, which bias buckets) is declared in PREREG-0B before 0b is scored; the multiplicity penalty covers the union of partitions. Choosing the regime split that maximizes the rate post-hoc encodes the conclusion.
- **A hindsight regime label.** A partition variable (e.g. realized chop-vs-trend) must be computable at the decision bar, or it cannot gate a live entry — it would be an unobservable oracle (the Q-REGIME-STRESS-1 / oracle_test failure mode).
- **Keeping the entry variant that wins without pre-committing the set.** All Phase-1 entry variants are pre-registered; "run several, report the best" without the penalty is the strategy-dev analogue of best-of-K.
- **Deploying on 1m forward-only as the validation.** Per the operator's gate choice, the entry is TF-agnostic and validated on a TF with multi-regime history; a forward-only 1m shadow is not a substitute for the backtest gate (F9).
- **Porting any Phase-0/1 result to NAS100 or another instrument.** Verdicts are single-instrument (path-independence); a US500 result does not license NAS100 (closure-1M §5). NAS100 needs its own ledger + its own run.

---

## §6 — Gate criteria

### Phase 0 (Q-ICT-1H-REVCON-1) — decides everything downstream

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED-CONDITIONAL` | A pre-registered, **decision-time-observable** partition's directional rate clears 0.5 by ≥2pp under BOTH stride AND block, beats placebo, survives the 0b multiplicity penalty, AND effective-N ≥ floor in that partition | **Open Phase 1** (Q-ICT-1M-ENTRY-1) in the confirmed direction; the bias∧PD gate logic is re-specified to match (e.g. trade-with-trend in trend regimes); pick execution TF at this gate |
| `FALSIFIED` | In EVERY pre-registered partition, both reversion AND continuation de-overlapped CIs straddle 0.5 after penalty | **Close the cascade-revival; do NOT open Phase 1** (the gate layer carries no directional info — there is nothing to gate an entry on). Capture lesson. |
| `AMBIGUOUS-HOLD` | Clears on the existing window (0a) but 0b is starved (eff-N < floor) in the candidate partition, OR clears unconditionally but the decision-time-observable partition does not | Re-spec the 0b export window (longer / explicitly chop-spanning); name the re-test object |

### Phase 1 (Q-ICT-1M-ENTRY-1) — only reached if Phase 0 = RESOLVED-CONDITIONAL

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | A pre-registered entry variant clears n≥100 + E[R] block-CI lb > 4×median-hurdle + drop-top-k + slice permutation, on a multi-regime TF | route to forward/out-of-regime confirmation (NOT deploy); update SPX500 ledger |
| `FALSIFIED` | A fillable population exists but E[R] CI ⊆ (−∞, hurdle], or gates add nothing, or one-slice edge, or drop-top-k removes it | close; the execution wrapper does not carry the Phase-0 signal to post-cost positive R |
| `INSUFFICIENT-N` | No entry variant clears n≥100 on any available multi-regime TF | F9 stands — execution un-validatable on the canonical feed; concept undeployable |

**Pre-registered before any data touches analysis.** PREREG-0B is committed before 0b is scored; the Phase-1 PREREG is committed before any entry-variant export is scored. Amending mid-investigation → close AMBIGUOUS, open fresh (Known Trap #12).

---

## §7 — Execution plan (next session)

- **Phase 0a — continuation/conditional probe (EXPLORATORY, on-disk, free).** Extend `harness_1h` (on top of the M-15-fixed `recompute_hits`) to also report, on the existing `PEPPERSTONE_US500, 60_a6b6b.csv`: (i) continuation rates (premium→up, discount→down) alongside reversion; (ii) the bias-conditioned split (reuse `bias_conditioned_rates` + the on-disk weekly `gateBias`); (iii) any in-window regime proxy. TDD the additions; reuse stride/block/placebo/effective_n. **Output is a hypothesis, not a verdict.**
- **Phase 0b — multi-regime confirmatory (needs export).** Operator exports the **longest 1H US500 (Pepperstone) window TV serves** (target: spans the 2020-2023 chop + 2023-2026 trend, or as much as the feed allows). **Commit PREREG-0B first** (firewall), then run reversion + continuation + the pre-registered partition test (halves/thirds by regime; bias sign). Apply §6 Phase-0 gate.
- **Decision gate.** Per §6 Phase-0. If RESOLVED-CONDITIONAL → write the Phase-1 PREREG (entry-variant set + TF, chosen by direction + a data-availability check on 15m/1m history) and proceed. If FALSIFIED → close; capture lesson. If AMBIGUOUS → re-spec the export.
- **Phase 1 — TF-agnostic entry redesign (gated).** Parameterize `entryMode` + TF in the Pine strategy + reuse `harness_1m`'s List-of-Trades machinery; pre-register the entry-variant ablation; validate at the gate-chosen TF on a multi-regime window. Closure per §9.

---

## §8 — Verdict pre-registration (mandatory before each phase's first scored run)

- **PREREG-0B** — `lab/analysis/ict_revcon_2026-06-19/PREREG-0B.md` (drafted this session, PROPOSED; **commit before scoring 0b**). Contains the §6 Phase-0 table + exact thresholds: n-floor per partition, the partition set (regime + bias buckets), the placebo design, the multiplicity grid + penalty, the ≥2pp margin, the decision-time-observability requirement on the partition variable.
- **PREREG-1M-ENTRY** — authored at the decision gate (only if Phase 0 RESOLVED-CONDITIONAL), before any entry-variant export is scored: the entry-variant set, the TF, n-floor, E[R]/hurdle/drop-top-k/permutation per PREREG-1M.

Pre-registration commit hash: `<populated at commit time next session>`
Pre-registration date: 2026-06-19 (PREREG-0B drafted; firewall lifts on its commit)

---

## §9 — Closure record format

- Phase 0 RESOLVED-CONDITIONAL → `CLOSURE-1H-REVCON-RESOLVED.md` (+ open Phase 1); FALSIFIED → `CLOSURE-1H-REVCON-FALSIFIED.md` (no Phase 1); AMBIGUOUS → `CLOSURE-1H-REVCON-AMBIGUOUS.md` (+ re-test trigger).
- Phase 1 per its verdict, same convention.
- Each closure: verdict, anchor numbers vs gate thresholds, what PREREG predicted vs happened, lesson candidates (dated/dollar anchor), and an SPX500-ledger disposition append.

---

## §10 — Audit hooks (runnable)

```bash
# §0 re-anchor (gitignored Pine, outside repo) — must match the §0 table or RE-READ:
Get-ChildItem 'C:\Users\joshu\Downloads\ict_1h_premium_discount_DRAFT.pine','C:\Users\joshu\Downloads\ict_1m_execution_DRAFT.pine' | Select Name,LastWriteTimeUtc,Length
#   Expect 1H 7554B/2026-06-18T22:42:04Z ; 1M 22180B/2026-06-18T22:42:25Z

# Confirm the M-15 fix is the base (decision-bar recompute_hits — NOT the inverted forward index):
grep -nE 'zone\[i\] == 1 and close\[j\] < close\[i\]' lab/analysis/ict_cascade_2026-06-18/harness_1h.py
#   Expect a hit (the fixed premium->down decision-bar form). If absent -> the M-15 fix regressed; STOP.

# Phase-0a discipline: the continuation probe must NOT be read as a verdict on the 6.5-mo file.
grep -niE 'exploratory|hypothesis-generating' lab/analysis/ict_revcon_2026-06-19/PREREG-0B.md
#   Expect the 0a-is-exploratory clause present.

# Firewall: PREREG-0B committed BEFORE the 0b export is scored.
git log --oneline -- lab/analysis/ict_revcon_2026-06-19/PREREG-0B.md
#   The pre-registration commit must predate any harness run on the longer 1H export.

# gitignore that drove citation-chain mode (expect line 75):
grep -n '\*\*/\*\.pine' .gitignore
```

---

## Verification

```bash
$ python "C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py" \
    "lab/analysis/ict_revcon_2026-06-19/Q-ICT-REVCON-PLAN.md" --type inquire
#   Expected: §0/§3/§4/§5/§6/§10 all PASS (parent brief with two forked sub-Qs; trap #11 handled by forking + gating).

$ Get-ChildItem 'C:\Users\joshu\Downloads\ict_1h_premium_discount_DRAFT.pine' | Select Name,LastWriteTimeUtc,Length   # §0 anchor
$ grep -n '\*\*/\*\.pine' .gitignore                                                                                  # citation-chain driver
```

---

## Pre-Lock Checklist (DRAFT — remove once locked)

- [x] §0 Pine anchors re-verified at next session start (Downloads is mutable) — 2026-06-19, match (1H 7554B / 1M 22180B)
- [ ] PREREG-0B finalized + committed BEFORE the 0b export is scored (firewall) — pre-data refinements applied 2026-06-19; genuine choices OPEN for operator ratification
- [x] Phase 0a additions TDD'd against synthetic fixtures (reuse `test_harness_1h.py` pattern) — 18/18; adversarially audited (probe FAITHFUL)
- [x] Partition set + decision-time-observability requirement frozen in PREREG-0B before 0b — partition #1 `[1]`-lag + observability guard added (audit LA-1)
- [ ] Phase-1 PREREG authored only at the decision gate (if Phase 0 RESOLVED-CONDITIONAL)
- [x] check_brief PASS; no `core/` touch — no `core/` touch (lab/ only); frozen cascade harness byte-identical
