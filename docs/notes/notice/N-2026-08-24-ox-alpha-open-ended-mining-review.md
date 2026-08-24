# NOTICE 2026-08-24 — ox-alpha sanitized review: open-ended agentic mining vs. the K-ledger

**Notice ID:** N-2026-08-24-ox-alpha-open-ended-mining-review
**Observed:** 2026-08-24
**Author:** Claude Code (Sonnet 5), operator direction ("pose the open-ended mining question to
ox-alpha. I want to get its read on it")
**Type:** Notice-phase. External adversarial-lens review, reconciled against real repo state.
$0 · K=0 · no camp · no card. No live-risk surface touched.
**Status:** `RESOLVED` — reconciliation complete; no new candidate, no methodology change proposed;
two genuinely novel threads surfaced for future consideration.

---

## §0 — Governance basis

Sent under [`docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md`](../../adr/2026-08-22-ox-alpha-adversarial-lens-scope.md)
§2's **base scope** (adversarial second-opinion lens on a reasoning/judgment call) — not the
bounded-extension candidate-generation addendum. The trigger was this session's own prior finding
(arXiv 2603.24517, "AVO: Agentic Variation Operators for Autonomous Evolutionary Search" — an
NVIDIA-affiliated GPU-kernel-optimization paper, unrelated to markets) that surfaced a genuine
methodology question: does an unbounded, continuously self-directed agentic evolutionary-search
method (verified safe in its own domain because its fitness oracle is cheap, ground-truth, and
non-gameable) have any legitimate, bounded adaptation to a domain — this repo's discovery pipeline
— whose fitness signal is a backtest on finite historical data, governed by a pre-registered,
capped trial-count (K-ledger) discipline. The ask was framed as testing that judgment against an
independent lens, not as a request for new strategy candidates.

**Sanitization applied:** no firm name, instrument ticker, dollar figure, strategy name, or
campaign identifier appears in the sent prompt. The K-ledger mechanism was described generically
("a research pipeline... its governance requires every look... counted toward a global
multiple-comparisons budget... a deflated/multiplicity-corrected threshold exceeds the best edge
the pipeline has ever found") — the real DSR/Bonferroni figures (K=3,177, floor 2.05, best edge
1.83) are not named. The external paper's own domain (GPU kernels) was described generically as
"automated code optimization." No proprietary content is reconstructable from the sent prompt or
the response.

**Send/receive record:** `stealth/ox-alpha` via OpenRouter chat-completions, 2026-08-24.
prompt_tokens=573 / completion_tokens=8,800. finish_reason=stop. No transcript of the hidden-
reasoning channel is stored in-repo (sanitization bar); only the final content is reconciled below.

---

## §1 — Reconciliation table (claim vs. real repo state)

| ox-alpha claim | Real repo state | Verdict |
|---|---|---|
| **Route 1** — bound the method by sealing a single-shot holdout: let an agent iterate freely against a training partition, pre-declare the exact test/threshold/window, touch virgin data exactly once (or K pre-declared finalists) | Matches existing discipline exactly: `lesson_oos_gate_select_on_insample_only` ("holdout must not see selection"), `lesson_reporting_burns_holdout` ("characterization tables ARE selection"), and the live IS/OOS split in `stage24_runner`/`universe_gate`. | **Confirms existing practice** — not new information, independent convergence. |
| **Route 2** — give the agent a synthetic oracle (calibrated simulator, e.g. block bootstrap) so free iteration costs zero real-data budget; flags Goodhart pressure, sim-argmax ≠ real-argmax | Matches `lesson_offline_fill_port_inflates_native_tv_arbiter` and `lesson_offline_port_needs_real_source_anchor` (offline/simulated infrastructure inflates apparent edge relative to the native/real source — an already-falsified failure mode in this repo). `core/mc/simulation.py` exists but is used for risk/DD simulation of an *already-known* strategy's trade stream, never as a free discovery-phase fitness oracle for searching strategy space. | **Confirms the general risk** (matches a known lesson); **the specific application (simulator-as-search-oracle) has never been tried here** — genuinely unused, not previously considered. |
| **Route 3** — anytime-valid inference (e-processes, confidence sequences) as an alternative to a fixed pre-declared N; claims it converges to the same wall as the pipeline's own fixed-K accounting | Grepped `docs/` for "anytime-valid," "e-process," "confidence sequence," "sequential test" — no hits describing this as a methodology tool. Not present anywhere in `strategy-validation`, `deflated_sharpe.py`, or the K-ledger docs. | **Novel — open thread.** Not previously considered as a complement/alternative framing to the frozen DSR/Bonferroni K_eff formula. Not actionable now (would need its own methodology pre-registration if ever pursued) — recorded here so it isn't lost. |
| **(b)** honesty requirements for a pre-declared iteration budget — never shrink N_eff post hoc (default N_eff = N), frozen components, restart discipline (aborted run's trials still count) | Matches `strategy_harvest.md` §1 "Confirm-not-mine": `K_eff = K_intrinsic`, "post-admission widening ... voids the screen result and is a new axis." Matches the DSR K-rule's refusal to let selection be priced only "sometimes." | **Confirms existing rule independently** — the model re-derived this repo's own K-accounting discipline from first principles without being shown it. |
| **(c)** a new leak class: an LLM agent's pretraining corpus may already contain the pattern of whatever holdout/validation era is used, which date-based purging (the fix for classical lookahead) cannot purge | Grepped `docs/` for "pretrain," "training corpus," LLM-specific contamination language — no hits describing this as a named risk category. `docs/methodology/lessons/methodology_lessons.md` and `docs/rejected_candidates.md` do not carry it. | **Genuinely novel — not currently named anywhere in this repo's methodology docs.** Distinct from every existing leakage lesson on file (all are data/engine/panel leakage, none are model-pretraining leakage). Worth naming explicitly given this repo's operational reliance on LLM agents throughout its research workflow — most relevant if an LLM's judgment is ever wired closer to gate mechanics or holdout release than the current zero-authority adversarial-lens role. |
| **(c)** "the only renewable, non-gameable oracle is prospective time" — a continuous agentic loop against history should really be a multi-quarter outer loop wrapped around a fast inner simulator loop, i.e. forward-tested, not backtested | Matches the Phase B lanes' own pattern exactly (`docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md`: "20-session forward paper-log ($0, zero capital, calendar time only)") and the MSL charter's forward-test steps. | **Confirms existing practice independently.** |
| **(d)** predictable failure sequence: threshold shock → post-hoc N_eff "correlation laundering" → holdout erosion/ratchet → specification gaming (agent exploits backtest defects: lookahead, unrealizable fills, survivorship) → definition creep (repairs booked as zero trials) → overfit ship-and-decay | Maps onto several independently-documented lessons: `feedback_discipline_guards_need_adversarial_tests` (vacuous asserts pass empty — matches "the verifier validates against the same backtest and gets gamed too"), `lesson_reporting_burns_holdout`, `feedback_dedup_attestation_must_be_executed` (matches "definition creep... quietly redefined until the budget stops binding"). | **Confirms multiple existing lessons, independently derived** — a concrete, well-grounded failure narrative, not a generic warning. |

## §2 — Net verdict

**No new candidate mechanism and no methodology change is proposed by this Use.** The core
question — does the AVO-style method (open-ended, continuously self-directed agentic search)
have a legitimate place in this repo's discovery pipeline — gets an independently-derived answer
that **converges exactly** with this session's own prior read: the method transfers only as *"a
fast proposal engine over simulated or already-spent data, coupled to a slow, single-shot
confirmation against virgin data or forward time."* Used as a continuous optimizer directly
against historical backtests, it violates this repo's K-ledger not because the budget is hard to
declare, but because the domain's oracle (a finite historical panel) depletes on use — every
"look" permanently taxes every future inference, unlike the paper's own domain where evaluations
accumulate for free. This is a structural property of the domain, not an accounting convention,
so no clever pre-registration scheme escapes it for a discover-*and*-certify use on one panel.

Two threads survive as **open, not-yet-actionable** for future methodology work (§1, novel rows):

1. **LLM-pretraining-era contamination** as a leak class distinct from classical lookahead —
   worth naming in `docs/methodology/lessons/methodology_lessons.md` or `rejected_signals.md` the
   next time that file is touched, given this repo already runs LLM agents (Claude Code, and now
   `stealth/ox-alpha`) through its research workflow.
2. **Anytime-valid / e-process sequential testing** as a possible alternative framing to the frozen
   DSR/Bonferroni K_eff formula — not a proposal to change the frozen formula, just a pointer that
   this family of statistics exists and independently reproduces the same wall.

**Since this Use produced claims that both confirm existing discipline and surface two genuinely
novel threads, revert trigger (b) (three consecutive zero-value uses) does not tick.**

---

## §3 — What this does NOT license

- Does not open a card, camp, or manifest of any kind. No K was spent — this Use is $0/K=0 by
  design (a methodology consult, not a candidate-generation ask).
- Does not amend `docs/methodology/strategy_harvest.md`, the DSR K-rule, or any frozen constant.
  The two novel threads in §2 are recorded as future-consideration pointers only.
- Does not authorize building a synthetic-oracle discovery lane, a sequential-testing framework,
  or any code touching `core/`, Pine, `dd_protection`, or MC calibration — all out of this Notice's
  scope per the standing methodology-skill wall.
- Carries zero authority over any admission decision, per the parent ADR §2/§5.

---

## §10 — Audit hooks (runnable)

```bash
# The prior-turn paper-relevance finding this Use follows from (same session)
grep -rn "AVO: Agentic Variation Operators" C:/Users/joshu/multi_firm_operations/.claude/worktrees/tradeify-bottleneck-solutions-84e1e6 2>/dev/null || echo "not committed anywhere — conversational finding only"

# Confirm neither novel thread was already named (expect: no real hits beyond this notice)
grep -rn "anytime-valid\|e-process\|confidence sequence" docs/methodology/ docs/spec/ 2>/dev/null
grep -rn "pretrain\|training corpus" docs/methodology/lessons/methodology_lessons.md docs/rejected_candidates.md 2>/dev/null

# Confirm the K-ledger rule this Use independently re-derived
grep -n "K_eff = K_intrinsic" docs/methodology/strategy_harvest.md
grep -n "post-admission widening" docs/methodology/strategy_harvest.md

# Confirm the offline/simulated-inflation lesson this Use's Route-2 caveat matches
grep -rln "offline_fill_port_inflates\|offline_port_needs_real_source_anchor" . 2>/dev/null || echo "memory-only, not a repo file"
```

## Verification

```bash
python scripts/check_brief.py docs/notes/notice/N-2026-08-24-ox-alpha-open-ended-mining-review.md --type notice
```
