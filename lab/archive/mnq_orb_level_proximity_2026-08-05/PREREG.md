# `MNQPROX-1` — is the MNQFLOW-1 L1 signature ORB-specific, or generic approached-level microstructure?

**Status:** `FROZEN — RUN NOT AUTHORIZED.` This is the gated re-proposal named by
[`mnq_orb_flow_substrate_2026-08-05/RESULTS.md`](lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md)
§6 ("level-proximity discriminator"). It clears Avenue A §6 by construction (survivor-tied to
`ORB-MNQ-1`). **The remaining gate is an operator GO, which this document does not grant and I do
not self-issue.** Frozen before any proximity-contrast quantity has been computed.
**Date:** 2026-08-05 · **Named by:** `MNQFLOW-1` RESULTS §4 limitation 1 / §6 entry packet.
**Parent:** [`MNQFLOW-1`](lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md) → `RESOLVED` (W1).
**Cost if authorized:** **$0.00** — reuses the already-authorized `tbbo` window (S1 identical to
parent); no new schema, no wider calendar, no MBP-10.
**K_intrinsic = 0** — reasoned in §6, not asserted. Disclosed: this cell was **named after** seeing
parent W1 (a follow-up contrast, not an independent discovery of `A`).

---

## §0 — Rule-0 reads (executed this session, at the line level)

| Source | Anchor | What it pins |
|---|---|---|
| [`mnq_orb_flow_substrate_2026-08-05/RESULTS.md`](lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md) **read in full** | `be6b94e` 2026-08-05 | §4 limitation 1 (level-proximity uncontrolled) + §6 entry packet (this cell's charter). W1 difference **−0.009367**, CI **[−0.013430, −0.005354]**, placebo p_emp **0.000**; disposition **watchlist + tripwire; opens nothing** |
| [`mnq_orb_flow_substrate_2026-08-05/PREREG.md`](lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md) | `be6b94e` | Parent S1–S7 (feature `A`, 60 s window, session-block bootstrap, within-session placebo, F2/FM-1). **FM-4** forbade this second cell under the parent sign-off — hence a fresh freeze |
| [`docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md`](lab/archive/../../../docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md) §6 | confirmed present | Qualifying triple; condition 3 = survivor-tied, not blind discovery |
| [`docs/notes/2026-08-05-order-flow-probe-governance-question.md`](lab/archive/../../../docs/notes/2026-08-05-order-flow-probe-governance-question.md) §7 | confirmed present | Blind probes barred; re-aim at ORB clears condition 3 by construction; Avenue A §6 unmodified |
| [`ops/instruments/MNQ.md`](lab/archive/../../../ops/instruments/MNQ.md) F2 GUARD + N14 | confirmed present | ORB filter slices may appear **ONLY** in the DEAD list. N14 records parent W1; this cell must not launder a fifth conditioning gate |
| [`lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py`](lab/archive/../orb/orb_universe_2026-06-22/orb_lib.py) L248–273 | confirmed present | Frozen OR = first `or_bars=2` session bars; entry on first subsequent break — parent event set unchanged |

**Dedup attestation.** `rg --no-ignore -il "level.proximity|approached.level|PDH|prior.day"` over
`rejected_candidates.md`, `rejected_signals.md`, and the parent study → **no prior falsification of
this contrast.** Nearest prior is parent RESULTS §4.1 naming this cell as the gated route.

---

## §1 — The question, and why it is the honest one

`MNQFLOW-1` found that at ORB-MNQ-1's own trigger moments, L1 size asymmetry `A` differs from
time-of-day-matched same-session controls (leans **against** the break). Those controls matched
**intraday liquidity shape only**. A trigger moment is, by construction, a moment when price sits at
a session opening-range extreme — so the measured signature may be the generic microstructure of
*any approached level*, not anything ORB-specific.

**H-MNQPROX-1.** At ORB-MNQ-1's own frozen trigger moments, mean signed L1 asymmetry `A` differs
from mean `A` at **non-ORB approached levels in the same sessions** (prior-day high/low first
touches), under the same feature window and inference stack as `MNQFLOW-1`.

- **Accept (ORB-specific):** CI on `mean(A_ORB) − mean(A_level)` excludes 0 **and** |effect| exceeds
  the within-session label-shuffle placebo p95 → the parent signature is not explained by generic
  level approach; watchlist tagging may name it as ORB-boundary-linked.
- **Reject (generic level microstructure):** CI includes 0, **or** effect ≤ placebo p95 → parent W1
  is consistent with generic approached-level microstructure; do **not** treat `A` as ORB-specific
  without a further cell.
- **A null is informative** — it discharges the parent's largest caveat rather than failing a hope.

---

## §2 — The frozen construct

| # | Element | Frozen value | Source |
|---|---|---|---|
| S1 | Instrument / schema / window | `MNQ.v.0`, **`tbbo`**, 2025-08-06 → 2026-08-04 (identical to parent S1) | parent; entitlement inventory |
| S2 | ORB event set | Parent's frozen trigger set — same engine call (`orb_lib.orb_backtest` unmodified, `or_bars=2`, filters off) on the ratified 1m panel. **Reuse parent `events` where byte-identical; do not re-cut** | parent S2 + panel-refresh ratification |
| S3 | Feature | Identical to parent: `A = (bid_sz − ask_sz)/(bid_sz + ask_sz)`, signed toward the breakout / approach direction, mean over **`[t−60s, t)`** | parent S3 |
| S4 | Level-contrast set | Within each session that has ≥1 ORB trigger: **first touch** of **prior-day high (PDH)** and/or **prior-day low (PDL)** — the first 1m bar whose mid enters within **1 MNQ tick (0.25 pt)** of that level after having been strictly farther on the prior bar. Touch timestamp = that bar's open (ET). Approach side: PDH → `long`; PDL → `short` (signed toward breaking through the level) | this cell's load-bearing definition |
| S4a | Exclusions (frozen) | Drop a level-touch if: (i) \|level − session OR high\| ≤ **4 ticks** or \|level − session OR low\| ≤ **4 ticks** (ORB itself / near-ORB coincidence); (ii) touch is within **15 min** of that session's ORB trigger; (iii) no prior session exists (panel's first calendar day); (iv) level-touch window has zero usable TBBO quotes | confound controls |
| S5 | Statistic | `Δ = mean(A_ORB) − mean(A_level)`, **session-block bootstrap** 95% CI (10,000 reps, seed **20260805b**; blocks = sessions). Only sessions that contribute **≥1 ORB trigger and ≥1 retained level-touch** enter the paired contrast; unpaired ORB-only or level-only sessions are counted in the coverage ledger, not in `Δ` | inherited bootstrap idiom; new seed suffix so this cell is not a silent re-use of parent draws |
| S6 | Placebo | Within each paired session, permute the ORB vs level-touch labels among that session's moments, 1,000 reps, same seed → p95 of \|Δ\| | WLEGB / parent discipline |
| S7 | Coverage / power guards | Report: (a) fraction of ORB triggers with usable `A`; (b) fraction of candidate PDH/PDL first-touches retained after S4a; (c) n_paired sessions; (d) n_ORB and n_level moments in the paired set. **VOID-POWER** if n_paired < 30 **or** n_level moments in the paired set < 50% of n_ORB moments in the paired set | honesty limbs |

**Signing of `A` at level touches** mirrors parent S3: PDH approach uses `long` (positive `A` =
bid-heavy toward an upside break of PDH); PDL uses `short`. ORB triggers keep parent signing.

**Outputs (closed list):** n_paired, coverage ledger (S7), `mean(A_ORB)`, `mean(A_level)`, `Δ` with
CI, placebo p95 / p_emp, by-half split (H1/H2 of the 1-yr panel). **Nothing else** — in particular
**no win/loss split, no MFE/MAE, no per-trade table, no third level class, no MBP-10** (§5).

---

## §3 — Avenue A §6 qualifying triple

**1 — Depth-shape, not category. ✓** Same `A` as parent — resting-size geometry; no participant class.

**2 — Not fill-trivial. ✓** Same as parent — pre-touch window; no fill price; no 1-tick model claim.

**3 — Survivor-tied. ✓** ORB arm is still ORB-MNQ-1's own frozen triggers. Level arm is a **contrast
control inside those sessions**, not a second discovery screen. Without ORB-MNQ-1 there is no paired
cell. **Monitors** limb: answers whether the parent's watchlist observable is ORB-boundary-linked or
generic.

**F2 guard.** This construct still **never conditions on ORB outcomes**. It compares ORB *moments* to
level-approach *moments*, never winners to losers. Converting a positive into a filter remains a
forbidden move (§5 FM-1) and a fresh K-bound axis (§6).

---

## §4 — Cost / data posture

| Item | Value |
|---|---|
| New pull required? | **No**, if the parent `tbbo` cache for S1 is intact. Estimate for the identical request remains **$0.0000** (reproduce with the audit hook; do not `pull` for estimation) |
| New schema? | No — `tbbo` only. MBP-10 remains unauthorized |
| Wider window? | No — S1 identical to parent |
| Transport | Reuse parent windowed subset if present; otherwise identical day-chunk discipline as parent |

⚠ If the cache is missing, an operator GO that authorizes this **run** also re-authorizes the same
S1 `tbbo` bytes already granted for `MNQFLOW-1` — not a broader entitlement.

---

## §5 — Forbidden moves

- **FM-1 — Reading ORB (or level-touch) trade outcomes.** No win/loss, PnL join, or
  outcome-conditioned cell. F2 guard's operative content.
- **FM-2 — Emitting any per-trade / excursion surface** a successor could tune a filter on.
- **FM-3 — Re-framing a positive as tradeable or as a fifth ORB conditioning gate.**
- **FM-4 — Any second cell inside this freeze:** no alternate level class (VWAP, round numbers,
  session running H/L, overnight H/L, …), no τ sweep, no MBP-10 arm, no second instrument, no
  alternate window. Each is a new axis needing fresh authorization.
- **FM-5 — Running before operator GO.**
- **FM-6 — Adjusting §7 thresholds, seeds, S4/S4a, or the placebo after data.**
- **FM-7 — Dropping Databento `degraded` days after seeing results** (disclose and retain, as parent).
- **FM-8 — Quietly editing parent RESULTS / N14 to claim ORB-specificity before this cell resolves.**

---

## §6 — Why `K_intrinsic = 0` (reasoned, not asserted)

Same posture as parent and the Step-1 event-ceiling study: this measures a **structural contrast**,
not a strategy, and **cannot emit a tradeable rule** — FM-1 removes outcome data. `K_banked(MNQ)` is
disclosed at run time from the live manifests (not restated here; Rule 7).

**Selection honesty (load-bearing disclosure, not a K increment):** this cell was **named in the
parent's Iterate block after W1 printed**. It is a follow-up contrast on a known nonzero `A`, not a
blind second search. That fact is recorded so a later reader cannot treat `MNQPROX-1` as independent
discovery of the asymmetry. **If either result is converted into a gate or filter, that conversion
is a fresh K-bound axis** with its own pre-registration — it inherits neither this K=0 nor the
parent's.

---

## §7 — Verdict gates (frozen; precedence as listed)

| # | Condition | Verdict | Disposition |
|---|---|---|---|
| W5 | S7 VOID-POWER fires | `VOID-POWER` | Report coverage ledger only; no `Δ` quoted. Not re-cut to chase n |
| W4 | ORB-arm coverage < 90% (usable `A`) | `VOID-COVERAGE` | Same honesty posture as parent W4 |
| W3 | CI includes 0 | **`FALSIFIED` (generic-level reading)** | **Pre-registered likely branch (§8).** Parent W1 is consistent with generic approached-level microstructure; do not tag `A` as ORB-specific. Watchlist may retain `A` as a *level-approach* observable, not an ORB-boundary one |
| W2 | CI excludes 0 but \|Δ\| ≤ placebo p95 | `AMBIGUOUS-CONFOUND` | Same disposition as W3 |
| W1 | CI excludes 0 ∧ \|Δ\| > placebo p95 | `RESOLVED` (ORB-linked) | Parent signature is not explained by PDH/PDL approach alone → watchlist may name ORB-boundary linkage. **Still opens no gate**; any filter use is a fresh K-bound axis |

A W1 that fails the by-half split reports `RESOLVED-NONSTATIONARY` with W1's disposition plus the
instability flagged. **Board write owed in every branch** (STATE.md, `MNQ.md`, SESSIONS, CATALOG,
parent PREREG amendment log pointer).

---

## §8 — Pre-registered expectation

**W3 (generic-level / null contrast) is the most likely single branch.** The parent's own RESULTS
named level-proximity as the largest caveat; the simplest explanation of a small against-the-break
L1 lean is that approached extremes look like that in general. Recorded now so a null reads as a
discharged prediction and a positive cannot be retrofitted as expected.

---

## §9 — Protocol order (violations void the run)

1. This file committed (**freeze**) — done before any proximity-contrast quantity exists.
2. **OPERATOR GO** on executing this cell (Avenue A sign-off for the *run*; cache reuse is not a new
   pull grant). **Not granted here.**
3. Harness + hand-computed unit tests (including S4 first-touch / S4a exclusion predicates); all pass
   before the runner reads a real quote.
4. Single run. RESULTS discharges exactly one §7 branch. Boards written.

---

## §10 — Audit hooks

```bash
# Freeze ordering (expect this file's freeze commit as the first touch)
git log --oneline -- lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md | tail -1

# Parent named this cell (expect "level-proximity" in §4 / §6)
rg -n "level-proximity|Entry packet" lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md

# Avenue A condition 3 + F2 guard still bind
rg -n "Survivor-tied|not blind discovery" docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md
rg -n "F2 GUARD" ops/instruments/MNQ.md

# Cost dry-run reproduction for the reused window (FREE; never add `pull`)
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate --symbols MNQ.v.0 \
  --stype continuous --schema tbbo --start 2025-08-06 --end 2026-08-04
# Expect: cost $0.0000

# No outcome columns in the closed output list of this PREREG
# (this WILL match — the only hits should be S2's exclusion prose, FM-1, and this
# hook's own line; a match inside a declared Outputs row would be the real failure)
rg -n "win/loss|MFE|MAE|PnL join" lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md

# S4 time-of-day guard (Amendment log, 2026-08-05) landed before any GO
rg -n "W6|VOID-TOD-CONFOUND" lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md
```

---

## Amendment log (append-only — the frozen §§1–9 above are never edited, Trap #12)

- **2026-08-05 — FROZEN.** Authored as the gated re-proposal named by `MNQFLOW-1` RESULTS §6.
  Run **not** authorized at freeze time. No proximity-contrast quantity computed.
- **2026-08-05 — S4 TIME-OF-DAY GUARD ADDED (pre-data, pre-GO — not an FM-6 violation: FM-6 bars
  adjusting S4/S4a *after data*; no data or run exists at this amendment).** Pre-GO review (CC, at
  operator request) found that S2 (ORB arm) and S4/S4a (level arm) are paired **at the session level
  only** — nothing matches or reweights the PDH/PDL first-touch arm to the ORB arm's own time-of-day
  distribution. Parent's own S4 (`mnq_orb_flow_substrate_2026-08-05/PREREG.md` §2 S4) matched
  controls to trigger time-of-day specifically **because** ORB triggers have a non-uniform intraday
  distribution — parent's stated reason: *"controls the intraday liquidity U-shape, which is the
  obvious confound."* Without an analogous guard here, ORB triggers (gated by the OR window) and
  PDH/PDL first-touches (not gated by it) could differ systematically in time-of-day, and a `W1`
  ("ORB-linked") verdict would be unable to distinguish genuine ORB-specificity from a
  **reintroduced U-shape artifact** — exactly the confound `MNQFLOW-1`'s own S4 was built to rule
  out. Left unguarded, this threatens both accept/reject branches of §1's H.

  **New frozen requirement, additive to §2/§7, binding on §9 step 3 before any run:**
  - **S4c — time-of-day disclosure (mandatory report, closed-list addition to S7):** for the paired
    session set, report `median` and `IQR` of minute-of-session (RTH minute, `entry_tod` convention
    per `orb_lib.py`) for the ORB arm and the level arm, separately.
  - **W6 — VOID-TOD-CONFOUND (new gate, evaluated BEFORE W5 — highest precedence in §7):** fires if
    the two arms' minute-of-session IQRs do not overlap, **or** if \|median(ORB tod) −
    median(level tod)\| exceeds **60 minutes**. On fire: report the coverage ledger (S7) and the
    time-of-day disclosure (S4c) only; `Δ` is **not** interpreted as ORB-specific or generic — the
    verdict is `VOID-TOD-CONFOUND`. **Not re-cut to chase a passing split**, mirroring the existing
    S7 VOID-POWER stop-rule.
  - The **60-minute** threshold is frozen now, before any timestamp is read, chosen generous
    (bug/confound-catching, not tuned to split a borderline case) per the standing falsifier
    discipline. It is not adjustable after this amendment without voiding the run (FM-6 applies to
    S4c/W6 exactly as it applies to S4/S4a).

  This does **not** relax anything already frozen — S1–S3, S4/S4a's touch/exclusion logic, S5, S6,
  and the original S7 VOID-POWER guard are unchanged. W6 is additive and evaluates first, so it
  cannot be satisfied by any post-hoc adjustment. §9 step 3's unit tests must cover the S4c
  computation and the W6 predicate, alongside the existing S4/S4a tests, before the runner reads a
  real quote.
- **2026-08-05 — OPERATOR GO GRANTED; §9 step 2 DISCHARGED.** Operator, in session: *"I am giving it
  the GO."* Issued **after** the S4c/W6 amendment above landed, so the GO covers the construct
  **including** the time-of-day guard — not the pre-amendment S4/S4a alone. **What is now
  authorized:** the single `tbbo` reuse named in S1/§4 (`MNQ.v.0`, 2025-08-06 → 2026-08-04,
  estimated **$0.0000**, identical to the parent's already-granted window — not a new entitlement).
  **What is still NOT authorized:** any MBP-10 pull, any second cell or arm (§5 FM-4), any window
  beyond S1's, any conversion of a result into a gate or filter (§6 — a fresh K-bound axis), and any
  run before §9 step 3 (harness + unit tests, now including S4c/W6) passes. **Not yet resolved by
  this GO:** whether the step-3/step-4 implementation runs on this surface (Claude Code) or is
  routed to Cursor per the standing CC/Cursor allocation ADR (`docs/adr/2026-07-14-cc-cursor-
  surface-allocation.md`) — flagged back to the operator, not decided unilaterally here.
- **2026-08-05 — S4 IMPLEMENTATION-PRECISION PIN (pre-data, pre-build; not FM-6 — frozen before
  any data or run, closing gaps the routing to Cursor requires be closed).** S4's prose ("prior-day
  high/low," "mid," "strictly farther on the prior bar") under-specifies three implementation
  choices that a builder would otherwise resolve mid-build. Pinned now, frozen exactly like S4/S4a:
  - **PDH/PDL session boundary:** the immediately preceding entry in the **same session index** S2
    already uses (`orb_lib.session_panel`'s per-session RTH index — identical instrument config,
    identical `open_tod`/`close_tod`). PDH = `piv["high"].loc[prev_session].max()`, PDL =
    `piv["low"].loc[prev_session].min()`, over **all** of that prior session's bars (OR bars + rest
    bars) — not a narrower or extended-hours window.
  - **Bar "mid" for touch detection:** `(bar_high + bar_low) / 2` on the **free 1m OHLCV panel**
    already loaded for S2 (`build_events.py`'s `raw`) — not TBBO. Detection stays on the free panel
    so touch-scanning burns no part of the S1 `tbbo` entitlement; only the retained touches' `[t−60s,
    t)` windows read TBBO, exactly as S2's triggers already do.
  - **"Strictly farther on the prior bar," session boundary case:** a session's **first** RTH bar is
    never eligible as a first-touch (there is no valid intra-session prior bar to confirm strict
    distance against). Touch scanning starts at the session's **second** bar.
  These are definitional completions of S4/S4a as written, not new statistical requirements — they
  do not change S5/S6/S7/S4c/W6. Frozen now so the Cursor-routed build in the forthcoming handoff
  brief has zero mid-build judgment calls, per the CC/Cursor allocation ADR's Q2 ("spec frozen ...
  Cursor never resolves a spec ambiguity unilaterally; it bounces `NEEDS_CONTEXT`").
- **2026-08-05 — CURSOR HANDOFF AUTHORED.** Implementation routed to Cursor per operator election
  (CC/Cursor allocation ADR routing test: Q0 credentials confirmed present locally, Q1 not a
  governed-surface edit, Q2 spec now fully frozen by the two amendments above, Q3 clears the
  handoff-overhead threshold). Brief:
  [`docs/briefs/handoffs/2026-08-05-cursor-handoff-mnqprox-1-run.md`](lab/archive/../../../docs/briefs/handoffs/2026-08-05-cursor-handoff-mnqprox-1-run.md).
  §9 steps 3–4 (harness + tests, single run) execute there; this PREREG gets one more append-only
  entry on completion, pointing to `RESULTS.md`.
- **2026-08-05 — RUN COMPLETE → `VOID-TOD-CONFOUND` (W6).** Cursor executed the frozen handoff ([`docs/briefs/handoffs/2026-08-05-cursor-handoff-mnqprox-1-run.md`](lab/archive/../../../docs/briefs/handoffs/2026-08-05-cursor-handoff-mnqprox-1-run.md)). Level events built from the free 1m panel (75 retained touches / 75 paired sessions after S4a i–iii); S4c measured ORB tod median 602 IQR [600, 616] vs level median 694 IQR [640, 771] (|gap| 92 min > 60; IQRs non-overlap). W6 evaluated **before** any level-arm TBBO pull — pull skipped. Machine + narrative record: [`RESULTS.md`](RESULTS.md) / [`RESULTS.json`](RESULTS.json). §§1–9 and prior amendment entries untouched.
