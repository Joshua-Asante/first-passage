# Q-PYRPARITY-1 — does scaling the risk% input scale the whole pyramided stack? (WATCH-1 haircut fidelity, DJ30→MYM / NAS100→MNQ)

**Status:** `CLOSED — FALSIFIED-NONPROPORTIONAL` (2026-07-17) — Phase 0–3 complete; [`closure`](closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md) · [`RESULTS`](../../lab/archive/q_pyrparity_1_2026-07/RESULTS.md). WATCH-1 for pyramided legs → account-multiplier-layer fallback; Q-RAIL-1 F1 = PASS-via-fallback.
**Authored:** 2026-07-17
**Closed:** 2026-07-17
**Authors:** Joshua (TV execution) + Claude Code (authoring + CSV verification)
**Parent question:** N/A — discharges the standing OPEN item at `docs/methodology/strategy_lifecycle.md:113`; consumed by [`Q-RAIL-1`](Q-RAIL-1-c1-execution-rail-go-live-scoping.md) precondition F1.
**Series:** strategy-R&D priorities 2026-07-17 — **rank 2 of 4** (hard dependency of rank 1; independently executable now).
**Loop:** Inquire-phase Pre-Q — closure gates on a paired-run TV observation, verified mechanically from export CSVs.
**Artifact path:** `docs/briefs/Q-PYRPARITY-1-watch1-pyramid-proportionality.md`

---

## §0 — Rule 0 reads (production-source verification; all read 2026-07-17)

**The claim under test, verbatim** — `docs/methodology/strategy_lifecycle.md:113` (anchor `83ba1b2`, 2026-07-12):

> **OPEN — Pine pyramid-parity** (DJ30 750% / NAS100 1000%): the haircut is confirmed on the *input* risk_pct; that scaling the input scales the whole *pyramided* stack proportionally needs TradingView observation (unverifiable from the Python side). **Latent today** (lifecycle all-1.0×); bites only when a *pyramided* leg is first de-risked. If non-proportional, apply the haircut at the account-multiplier layer for those two legs (documented fallback).

**Why it is no longer latent:** c1 was ratified deployable at **WATCH-1 (0.50×)** on 2026-07-17 (`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md`, anchor `d85c10c`) and c1's book is exactly the two pyramided legs. The haircut re-MC that ratified it injected ×0.5 on `daily_100k` — a book-level *return* haircut (`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md`, anchor `d85c10c`, §"Discipline honored"). Whether TV-side execution can *realize* that haircut via the risk input is this brief's question.

**Pine sources (gitignored per `**/*.pine`, but PRESENT on local disk — verified via `find core/strategies -type f` this session; citation-chain mode not required, direct executor reads ARE possible):**

- `core/strategies/striker/striker_dj30_v4.5.pine` — sha pinned `716f8b43…` in `core/strategies/MANIFEST.sha256`.
- `core/strategies/nas/striker_nas100_v1.pine` — sha pinned `f5a567b5…` in `core/strategies/MANIFEST.sha256`.
- Executor Phase 0 reads the **sizing + pyramid qty code paths** in both files (sizing basis: `strategy.initial_capital` vs `strategy.equity`; add-leg qty derivation vs base qty) before the statistic branch in §4 is selected. Rule-0-extends-to-Pine discipline applies (read exit/close-order semantics around the cited lines, ±20 lines).

**Tier-1 derived-mirror corroboration** (gated against Pine input defaults by `scripts/validate_params.py`): `core/config/params.toml` (anchor `784a9ab`) line 69 `pyramid_pct = 750.0` (DJ30), line 94 `pyramid_pct = 1000.0` (NAS100).

**Panels of record this must match:** the c1 scoring panels are TV exports of the locked Pine on CME charts — `Striker_DJ30…MYM…15d8b.csv` / `Striker_NAS100…MNQ…beabf.csv` (sha-pinned; `STATE.md` anchor `e5eca1a`). The parity runs use the **same symbol/TF/settings** as those exports.

**Standing lessons that shape the protocol (memory + repo):**
- *Pyramid IS the strategy for NAS100* (base-only PF 0.31): a haircut that mis-scales adds is not a smaller position — it is a different strategy. This is why F1 in Q-RAIL-1 hard-blocks on this brief.
- *TV CSV compounding artifact*: TV compounds equity; a naive P&L-ratio comparison between two runs conflates sizing-basis feedback with the property under test. The §4 statistic must be selected per the observed sizing basis.
- *Per-cohort measurement* (ECR lesson): measure adds and base legs **separately**; an aggregate ratio can mask clipped adds.
- *TV egress*: no TV automation exists or is permitted — runs are operator-executed; exports land in Downloads → copy local per the standing CSV workflow.

---

## §1 — Context & motivation

The lifecycle governance ADR (2026-07-10) wired the authorization ladder so a WATCH-tier leg sizes down via a multiplier on the risk_pct layer. For flat (non-pyramided) legs that is trivially proportional. For the two pyramided legs, proportionality of the *whole stack* (base + 750%/1000% adds) under an input-risk scaling was explicitly left OPEN — acceptable while all legs sat at 1.00×. The c1 WATCH-1 ratification (2026-07-17) makes it the load-bearing execution-fidelity assumption of the program's only deployable book: the re-MC evidence says "this book is safe at half size"; this brief answers whether "half size" is a thing the TV-side execution can actually produce by turning the risk input down.

---

## §2 — Prior art / lineage

- `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md` — the ladder + the risk_pct-layer haircut design; its Phase-2 open item list names this confirmation.
- `docs/methodology/strategy_lifecycle.md:113` — canonical owner of the OPEN item and of the **documented fallback** (account-multiplier-layer haircut for the two legs if non-proportional).
- c1 haircut re-MC (`RESOLVED-DEPLOYABLE`, 2026-07-17) — the consumer of a RESOLVED verdict here.
- FUTURES_LOCK venue editions (2026-07-03/06) — size in integer contracts (`floor(accountSize·risk%/(slDist·$/pt))` + RESERVE cap); their acceptance checklists are **separate** owed work (Q-RAIL-1 Phase 1/F3). This brief tests the *locked CFD Pine on CME charts* — the panel-of-record configuration — not the editions.
- Feedback lessons: `feedback_pine_offset_port_faithfulness_anchor`, `feedback_rule0_pine_code_check` (read the Pine, not the docs, for behavior claims).

---

## §3 — Question (Q-PYRPARITY-1)

**Pre-Q gate test:** symptom-only rephrase — "the ratified WATCH-1 deployment rests on an unverified TV-side scaling assumption." Passes; no mechanism is presupposed (the answer may be the fallback).

**Q-PYRPARITY-1:** On the panel-of-record TV configurations, does halving the strategy's risk% input halve the entire executed position stack — base and pyramid adds alike — or does the stack scale non-proportionally?

---

## §4 — Falsifiable hypothesis (H-PYRPARITY-1)

**H-PYRPARITY-1:** Halving the risk% input produces a per-trade executed-quantity ratio of 0.500 for **both** cohorts (base entries AND pyramid adds), with identical signal timing, on both legs.

**Protocol statistic (branch selected by the Phase-0 Pine read, pre-committed here):**
- **Branch A — sizing basis is initial-capital (non-compounding):** statistic = per-fill qty ratio `qty(r0/2) / qty(r0)` on entry-time-paired fills.
- **Branch B — sizing basis is strategy.equity (compounding):** statistic = per-fill **normalized** qty ratio `[qty/equity](r0/2) / [qty/equity](r0)` on entry-time-paired fills, with equity taken at entry from the export/recomputation (removes the compounding-feedback confound per the TV-compounding lesson).

**Accept (→ `RESOLVED-PROPORTIONAL`) if, on BOTH legs and BOTH cohorts (base / adds) separately:** ≥ 95% of paired fills have statistic within **0.500 ± 0.02**, median within **0.500 ± 0.005**, AND entry/exit timestamps are identical run-to-run (signal path untouched by the risk input).
**Reject (→ `FALSIFIED-NONPROPORTIONAL`) if:** either cohort's median statistic falls outside 0.500 ± 0.02 on either leg, OR the add cohort's fill count drops run-to-run (adds clipped at lower risk — a structural non-proportionality even if surviving adds scale).
**Ambiguous-hold if:** trade lists misalign for reasons other than clipped adds (count/timing drift ⇒ the risk input touches the signal path — a Pine-behavior finding requiring its own look), or TV min-qty rounding makes the tolerance undecidable at the tested account size (re-run at a larger test account size once; then decide).

Tolerances rationale: 0.02 absorbs TV qty rounding at realistic sizes; the 0.005 median band catches systematic (vs rounding) deviation. Pre-registered before any run.

---

## §5 — Forbidden moves (genuinely tempting)

- **Editing the locked Pine to expose a cleaner sizing hook for the test** — parameter axis is immutable; the test observes locked behavior, it does not instrument it.
- **Testing at 1.00× vs 0.50× on the CFD symbols (US30/NAS100) because those charts are already open, then generalizing to the CME panels silently** — single-asset face-validity discipline; the deployment surface is MYM1!/MNQ1!. (A CFD replicate is *optional corroboration*, labeled as such.)
- **Aggregating base + adds into one ratio** — the edge lives in the adds (NAS100 base-only PF 0.31); an aggregate can pass while the adds are clipped. Cohort-split is mandatory.
- **Accepting a near-miss ("0.47 is basically half") to keep Q-RAIL-1 moving** — the documented fallback exists precisely so a FALSIFIED here is cheap; bending the band is Trap #12.
- **Automating the TV runs** — no TV backtest API; never automate TV (standing assessment). Operator-executed, four runs total.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED-PROPORTIONAL` | §4 accept bands met on both legs × both cohorts | `strategy_lifecycle.md:113` flips to CONFIRMED (dated); Q-RAIL-1 F1 = PASS via risk-input scaling; the WATCH-1 deployment mechanism is TV-native |
| `FALSIFIED-NONPROPORTIONAL` | §4 reject fires on any leg/cohort | Apply the documented fallback: WATCH-1 haircut at the **account-multiplier layer** for the two pyramided legs (`strategy_lifecycle.md:113`); Q-RAIL-1 F1 = PASS-via-fallback; flag in the go-live packet that the haircut re-MC's book-level ×0.5 is then realized by lot-multiplier, not risk input. Also re-opens the **multiplier-spine forward-relevance flag** (STATE 08-08 item) in the affirmative |
| `AMBIGUOUS-HOLD` | Misaligned trade lists (non-add-clipping) or undecidable rounding after the one permitted re-size | Route to a Pine-behavior look (fresh Q; this brief does not chase it); Q-RAIL-1 F1 = BLOCKED-ON-INPUT; carried to the 08-08 packet |

---

## §7 — Execution plan

- **Phase 0 — Pine read (CC, ≤30 min). ✅ DONE 2026-07-17** — [`lab/archive/q_pyrparity_1_2026-07/PHASE0.md`](../../lab/archive/q_pyrparity_1_2026-07/PHASE0.md). Sha-verified both locked sources vs `MANIFEST.sha256` (match). Sizing basis = `strategy.equity` (rolling, compounding) → **Branch B** (recorded in pre-reg §4). Structural proportionality **CONFIRMED-IN-SOURCE (corroborating)**: `size = equity·risk%/stopDist` and `addSize = initialSize·pyramidSize%`, both exactly linear in `riskPerTrade`, no floor/cap/round/min-qty on the sizing path in either file. Phase-2 normalization rule surfaced: normalize the add fill on **entry-bar** equity (not add-bar). TV runs still required — integer-contract rounding on MYM1!/MNQ1! is invisible in source.
- **Phase 1 — TV runs (operator, 4 runs). ✅ DONE 2026-07-17** — MYM `f5ecb` (r0, byte=panel `15d8b`) / `8d6b5` (r½); MNQ `9b6c8` (r0) / `b2723` (r½). Copied to `lab/archive/q_pyrparity_1_2026-07/`.
- **Phase 2 — mechanical verification. ✅ DONE 2026-07-17** — Branch B harness `verify_phase2.py`; [`RESULTS.md`](../../lab/archive/q_pyrparity_1_2026-07/RESULTS.md). **Overall `FALSIFIED-NONPROPORTIONAL`** (MYM medians 0.871 / 0.916 — binding TV qty ceiling at 17/127; below ceiling ratios ≈ 0.50). MNQ leg `AMBIGUOUS-HOLD` (list misalignment + base integer-rounding fill-frac).
- **Phase 3 — verdict + propagation. ✅ DONE 2026-07-17** — §6 `FALSIFIED-NONPROPORTIONAL` fired; `strategy_lifecycle.md:113` → CONFIRMED-FALLBACK; Q-RAIL-1 F1 → PASS-via-fallback; STATE multiplier-spine affirmed YES; closure [`Q-PYRPARITY-1-closure-falsified-nonproportional.md`](closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md).

---

## §8 — Verdict pre-registration

**FROZEN 2026-07-17.** `docs/briefs/pre-registration/Q-PYRPARITY-1-verdict-preregistration.md` — the §4 bands + §6 table transcribed verbatim, committed before Phase 1 runs. Phase 0's branch selection (Branch A/B) is recorded there once the Pine read completes, still before any TV export is opened.

**Operator ratification (chat, 2026-07-17):** "ratify Q-RAIL-1 and Q-PYRPARITY-1, sign the §8 budget." No operator-supplied numbers are needed for this brief — the §4 tolerance bands (0.500 ± 0.02 / ± 0.005 median) were already fully specified at authoring; ratification here is acceptance-to-proceed, not a new figure.

Pre-registration commit hash: this commit — see `git log --oneline -- docs/briefs/pre-registration/Q-PYRPARITY-1-verdict-preregistration.md` · Date: 2026-07-17

---

## §9 — Closure record format

Per standard: `closures/Q-PYRPARITY-1-closure-<verdict>.md` with the four cohort-ratio tables vs bands, branch selected, and (on FALSIFIED) the fallback activation note. Lesson candidate only if the TV behavior surprises the Pine read (that divergence is the lesson).

---

## §10 — Audit hooks (runnable)

```bash
# The claim under test — should read CONFIRMED-FALLBACK after Q-PYRPARITY-1 close
grep -n "CONFIRMED-FALLBACK — Pine pyramid-parity\|OPEN — Pine pyramid-parity" docs/methodology/strategy_lifecycle.md

# Locked sources unchanged since authoring (re-run before Phase 1)
sha256sum core/strategies/striker/striker_dj30_v4.5.pine core/strategies/nas/striker_nas100_v1.pine
grep -n "striker_dj30_v4.5.pine\|striker_nas100_v1.pine" core/strategies/MANIFEST.sha256

# Pyramid mirror values unchanged (750/1000)
grep -n "pyramid_pct" core/config/params.toml

# The executing session cites this brief (Trap #10)
grep -rn "Q-PYRPARITY-1" docs/SESSIONS.md
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-PYRPARITY-1-watch1-pyramid-proportionality.md --type inquire
git log -1 --format='%h %cs' -- docs/methodology/strategy_lifecycle.md core/config/params.toml
```

## Ratification record

Ratified 2026-07-17 (operator, chat: "ratify Q-RAIL-1 and Q-PYRPARITY-1, sign the §8 budget"). §8 pre-registration frozen same date. Next: Phase 0 Pine read (CC) → Phase 1, 4 operator-executed TV runs (MYM1!/MNQ1!, r0 vs r0/2).
